from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
import logging

from app.ingestion.trades import TradesDB, PARQUET_DIR
from app.ingestion.bybit_trades import BybitTradesDB, BYBIT_PARQUET_DIR

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/footprint", tags=["footprint"])

# Initialize TradesDB instances per exchange
_trades_db_binance: Optional[TradesDB] = None
_trades_db_bybit: Optional[BybitTradesDB] = None

def get_trades_db(exchange: str = "binance"):
    """Get the appropriate TradesDB based on exchange."""
    global _trades_db_binance, _trades_db_bybit
    
    if exchange == "bybit":
        if _trades_db_bybit is None:
            if not BYBIT_PARQUET_DIR.exists() or not list(BYBIT_PARQUET_DIR.glob("*.parquet")):
                raise HTTPException(
                    status_code=503,
                    detail="Bybit trade data not available. Run: python -m app.ingestion.bybit_trades convert"
                )
            _trades_db_bybit = BybitTradesDB()
        return _trades_db_bybit
    else:
        # Default to Binance
        if _trades_db_binance is None:
            if not PARQUET_DIR.exists() or not list(PARQUET_DIR.glob("*.parquet")):
                raise HTTPException(
                    status_code=503,
                    detail="Binance trade data not available. Run: python -m app.ingestion.trades convert"
                )
            _trades_db_binance = TradesDB()
        return _trades_db_binance

class FootprintProfile(BaseModel):
    price: float
    total_volume: float
    buy_volume: float
    sell_volume: float
    delta: float

class FootprintCandle(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    total_delta: float
    poc: Optional[float] = None
    vah: Optional[float] = None
    val: Optional[float] = None
    profiles: List[FootprintProfile]


class FootprintResponse(BaseModel):
    symbol: str
    timeframe: str
    tick_size: float
    ticks_per_row: int
    candles: List[FootprintCandle]


class TradesStats(BaseModel):
    total_trades: int
    first_trade_date: str
    last_trade_date: str
    min_price: float
    max_price: float
    total_volume: float


# Timeframe to milliseconds mapping
TIMEFRAME_MS = {
    "1m": 60_000,
    "5m": 300_000,
    "15m": 900_000,
    "30m": 1_800_000,
    "1h": 3_600_000,
    "4h": 14_400_000,
    "1d": 86_400_000
}


@router.get("/stats", response_model=TradesStats)
def get_trades_stats(
    exchange: str = Query(default="binance", description="Exchange: binance or bybit")
):
    """Get summary statistics about available trade data."""
    db = get_trades_db(exchange)
    stats = db.get_stats()
    
    if not stats or stats.get('total_trades') is None:
        raise HTTPException(status_code=503, detail="No trade data available")
    
    return TradesStats(
        total_trades=int(stats['total_trades']),
        first_trade_date=stats.get('first_trade_date', ''),
        last_trade_date=stats.get('last_trade_date', ''),
        min_price=float(stats.get('min_price', 0)),
        max_price=float(stats.get('max_price', 0)),
        total_volume=float(stats.get('total_volume', 0))
    )


@router.get("/candles", response_model=FootprintResponse)
def get_footprint_candles(
    symbol: str = Query(default="BTCUSDT", description="Trading pair symbol"),
    exchange: str = Query(default="binance", description="Exchange: binance or bybit"),
    timeframe: str = Query(default="5m", description="Candle timeframe"),
    tick_size: float = Query(default=1.0, description="Minimum price tick"),
    ticks_per_row: int = Query(default=10, description="Ticks per profile row"),
    limit: int = Query(default=100, ge=1, le=5000, description="Number of candles"),
    start_ts: Optional[int] = Query(default=None, description="Start timestamp (ms)"),
    end_ts: Optional[int] = Query(default=None, description="End timestamp (ms)")
):
    """
    Get footprint candles with per-candle volume profiles.
    
    Each candle includes:
    - OHLCV data
    - Volume profile (price bins with buy/sell/delta)
    - POC (Point of Control - price with highest volume)
    - VAH/VAL (Value Area High/Low - 70% volume range)
    """
    if timeframe not in TIMEFRAME_MS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported timeframe: {timeframe}. Use: {list(TIMEFRAME_MS.keys())}"
        )
    
    candle_ms = TIMEFRAME_MS[timeframe]
    db = get_trades_db(exchange)
    
    # Determine time range
    if start_ts is None or end_ts is None:
        # Default: get last N candles based on data availability
        stats = db.get_stats()
        if not stats or stats.get('last_trade_ts') is None:
            raise HTTPException(status_code=503, detail="No trade data available")
        
        last_ts = int(stats['last_trade_ts'])
        if end_ts is None:
            end_ts = last_ts
        if start_ts is None:
            start_ts = end_ts - (limit * candle_ms)
    
    try:
        candles_raw = db.build_candles_with_profiles(
            start_ts=start_ts,
            end_ts=end_ts,
            candle_ms=candle_ms,
            tick_size=tick_size,
            ticks_per_row=ticks_per_row
        )
    except Exception as e:
        logger.error(f"Failed to build candles: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    # Convert to response model
    candles = []
    for c in candles_raw[-limit:]:  # Limit to last N
        profiles = [
            FootprintProfile(
                price=p['price_bin'],
                total_volume=p['total_volume'],
                buy_volume=p['buy_volume'],
                sell_volume=p['sell_volume'],
                delta=p['delta']
            )
            for p in c.get('profile', [])
        ]
        
        candles.append(FootprintCandle(
            timestamp=c['timestamp'],
            open=c['open'],
            high=c['high'],
            low=c['low'],
            close=c['close'],
            volume=c['volume'],
            total_delta=c.get('total_delta', 0),
            poc=c.get('poc'),
            vah=c.get('vah'),
            val=c.get('val'),
            profiles=profiles
        ))
    
    return FootprintResponse(
        symbol=symbol,
        timeframe=timeframe,
        tick_size=tick_size,
        ticks_per_row=ticks_per_row,
        candles=candles
    )
