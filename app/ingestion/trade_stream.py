"""
Live Trade Streaming via CCXT Pro WebSocket

Streams real-time trade executions from Binance Futures for building
live footprint charts and volume profiles.
"""
from __future__ import annotations

import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class Trade:
    """A single trade execution"""
    id: str
    timestamp_ms: int
    symbol: str
    price: float
    amount: float  # Base currency amount
    cost: float    # Quote currency cost (price * amount)
    side: str      # 'buy' or 'sell'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp_ms,
            "symbol": self.symbol,
            "price": self.price,
            "amount": self.amount,
            "cost": self.cost,
            "side": self.side
        }


@dataclass
class LiveCandle:
    """A live candle being built from trades"""
    timestamp_ms: int  # Candle start time
    open: float
    high: float
    low: float
    close: float
    volume: float  # Total volume
    buy_volume: float
    sell_volume: float
    trade_count: int
    profiles: Dict[float, Dict[str, float]] = field(default_factory=dict)  # price_bucket -> {buy_vol, sell_vol}
    
    def to_dict(self) -> Dict[str, Any]:
        # Convert profiles to list format expected by frontend
        profile_list = []
        for price, vols in sorted(self.profiles.items()):
            profile_list.append({
                "price": price,
                "bid_vol": vols.get("sell", 0),  # Bid = market sell
                "ask_vol": vols.get("buy", 0),   # Ask = market buy
                "delta": vols.get("buy", 0) - vols.get("sell", 0)
            })
        
        return {
            "timestamp": self.timestamp_ms,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "buy_volume": self.buy_volume,
            "sell_volume": self.sell_volume,
            "total_delta": self.buy_volume - self.sell_volume,
            "trade_count": self.trade_count,
            "profiles": profile_list
        }


@dataclass
class TradeStreamConfig:
    """Configuration for trade streaming"""
    symbol: str = "BTC/USDT:USDT"
    exchange: str = "binanceusdm"
    candle_interval_ms: int = 60000  # 1 minute candles
    price_bucket_size: float = 1.0   # $1 price buckets for profiles
    max_trades_in_memory: int = 10000
    max_candles_in_memory: int = 100


class TradeStreamer:
    """
    Streams live trade executions via CCXT Pro WebSocket.
    Builds live candles with volume profiles for footprint display.
    """
    
    def __init__(self, config: Optional[TradeStreamConfig] = None):
        self.config = config or TradeStreamConfig()
        self.exchange = None
        self.running = False
        self.trades: deque[Trade] = deque(maxlen=self.config.max_trades_in_memory)
        self.candles: deque[LiveCandle] = deque(maxlen=self.config.max_candles_in_memory)
        self.current_candle: Optional[LiveCandle] = None
        self.callbacks: List[Callable[[Trade], None]] = []
        self.candle_callbacks: List[Callable[[LiveCandle], None]] = []
        self._task: Optional[asyncio.Task] = None
        
    async def start(self) -> None:
        """Start the trade streaming"""
        if self.running:
            logger.warning("TradeStreamer already running")
            return
            
        try:
            import ccxt.pro as ccxtpro
        except ImportError:
            logger.error("ccxt.pro not available")
            raise ImportError("CCXT Pro required for WebSocket streaming")
        
        exchange_class = getattr(ccxtpro, self.config.exchange)
        self.exchange = exchange_class({
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        
        self.running = True
        self._task = asyncio.create_task(self._stream_loop())
        logger.info(f"Started trade streaming for {self.config.symbol}")
        
    async def stop(self) -> None:
        """Stop the trade streaming"""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        if self.exchange:
            await self.exchange.close()
            self.exchange = None
            
        logger.info("Stopped trade streaming")
        
    async def _stream_loop(self) -> None:
        """Main streaming loop"""
        while self.running:
            try:
                # Watch trades - returns new trades since last call
                trades = await self.exchange.watch_trades(self.config.symbol)
                
                for trade_data in trades:
                    self._process_trade(trade_data)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in trade stream: {e}")
                await asyncio.sleep(1)
                
    def _process_trade(self, trade_data: Dict[str, Any]) -> None:
        """Process a single trade"""
        trade = Trade(
            id=str(trade_data.get('id', '')),
            timestamp_ms=int(trade_data.get('timestamp', time.time() * 1000)),
            symbol=self.config.symbol,
            price=float(trade_data.get('price', 0)),
            amount=float(trade_data.get('amount', 0)),
            cost=float(trade_data.get('cost', 0)),
            side=trade_data.get('side', 'buy')
        )
        
        self.trades.append(trade)
        
        # Update current candle
        self._update_candle(trade)
        
        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback(trade)
            except Exception as e:
                logger.error(f"Trade callback error: {e}")
    
    def _update_candle(self, trade: Trade) -> None:
        """Update the current candle with a new trade"""
        candle_start = (trade.timestamp_ms // self.config.candle_interval_ms) * self.config.candle_interval_ms
        
        # Check if we need a new candle
        if self.current_candle is None or self.current_candle.timestamp_ms != candle_start:
            # Save the old candle
            if self.current_candle is not None:
                self.candles.append(self.current_candle)
                # Notify candle callbacks
                for callback in self.candle_callbacks:
                    try:
                        callback(self.current_candle)
                    except Exception as e:
                        logger.error(f"Candle callback error: {e}")
            
            # Start new candle
            self.current_candle = LiveCandle(
                timestamp_ms=candle_start,
                open=trade.price,
                high=trade.price,
                low=trade.price,
                close=trade.price,
                volume=0,
                buy_volume=0,
                sell_volume=0,
                trade_count=0,
                profiles={}
            )
        
        # Update candle
        candle = self.current_candle
        candle.high = max(candle.high, trade.price)
        candle.low = min(candle.low, trade.price)
        candle.close = trade.price
        candle.volume += trade.amount
        candle.trade_count += 1
        
        if trade.side == 'buy':
            candle.buy_volume += trade.amount
        else:
            candle.sell_volume += trade.amount
        
        # Update profile
        bucket = round(trade.price / self.config.price_bucket_size) * self.config.price_bucket_size
        if bucket not in candle.profiles:
            candle.profiles[bucket] = {"buy": 0, "sell": 0}
        candle.profiles[bucket][trade.side] += trade.amount
    
    def add_trade_callback(self, callback: Callable[[Trade], None]) -> None:
        """Add callback for individual trades"""
        self.callbacks.append(callback)
        
    def add_candle_callback(self, callback: Callable[[LiveCandle], None]) -> None:
        """Add callback for completed candles"""
        self.candle_callbacks.append(callback)
        
    def get_recent_trades(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent trades"""
        trades = list(self.trades)[-limit:]
        return [t.to_dict() for t in trades]
    
    def get_current_candle(self) -> Optional[Dict[str, Any]]:
        """Get the current (incomplete) candle"""
        if self.current_candle:
            return self.current_candle.to_dict()
        return None
    
    def get_recent_candles(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent completed candles"""
        candles = list(self.candles)[-limit:]
        result = [c.to_dict() for c in candles]
        # Add current candle if exists
        if self.current_candle:
            result.append(self.current_candle.to_dict())
        return result


# Global instance
_trade_streamer: Optional[TradeStreamer] = None


def get_trade_streamer() -> TradeStreamer:
    """Get or create the global TradeStreamer instance"""
    global _trade_streamer
    if _trade_streamer is None:
        _trade_streamer = TradeStreamer()
    return _trade_streamer


async def start_trade_streaming(config: Optional[TradeStreamConfig] = None) -> TradeStreamer:
    """Start the global trade streamer"""
    global _trade_streamer
    if _trade_streamer is None:
        _trade_streamer = TradeStreamer(config)
    await _trade_streamer.start()
    return _trade_streamer


async def stop_trade_streaming() -> None:
    """Stop the global trade streamer"""
    global _trade_streamer
    if _trade_streamer:
        await _trade_streamer.stop()
        _trade_streamer = None
