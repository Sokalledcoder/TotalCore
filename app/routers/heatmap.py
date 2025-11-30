"""
Heatmap API endpoints for volume bubbles and liquidity depth visualization.

Provides:
- Volume bubbles: Large executed trades for highlighting whale activity
- Depth data: Order book depth snapshots for liquidity heatmap
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
import logging

import math
from app.ingestion.trades import TradesDB, PARQUET_DIR
from app.ingestion.bookdepth import BookDepthDB, BOOKDEPTH_DATA_DIR, get_bookdepth_db
from app.ingestion.bybit_orderbook import BybitOrderBookDB, BYBIT_ORDERBOOK_PARQUET_DIR

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/heatmap", tags=["heatmap"])

# Lazy-loaded database instances
_trades_db: Optional[TradesDB] = None
_bookdepth_db: Optional[BookDepthDB] = None


def get_trades_db() -> TradesDB:
    """Lazy-load the TradesDB instance."""
    global _trades_db
    if _trades_db is None:
        if not PARQUET_DIR.exists() or not list(PARQUET_DIR.glob("*.parquet")):
            raise HTTPException(
                status_code=503,
                detail="Trade data not available. Run: python -m app.ingestion.trades convert"
            )
        _trades_db = TradesDB()
    return _trades_db


def get_depth_db() -> BookDepthDB:
    """Lazy-load the BookDepthDB instance."""
    global _bookdepth_db
    if _bookdepth_db is None:
        _bookdepth_db = BookDepthDB()
        # Load all available CSV files
        try:
            _bookdepth_db.load_csv_files()
        except Exception as e:
            logger.error(f"Failed to load book depth data: {e}")
            raise HTTPException(
                status_code=503,
                detail=f"Book depth data not available: {e}"
            )
    return _bookdepth_db


# ============================================================================
# Pydantic Models
# ============================================================================

class VolumeBubble(BaseModel):
    """Represents a large executed trade for volume bubble visualization."""
    timestamp_ms: int
    price: float
    qty: float
    quote_qty: float
    is_buy: bool  # True = buy aggressor, False = sell aggressor


class VolumeBubblesResponse(BaseModel):
    """Response containing volume bubbles for a time range."""
    symbol: str
    start_ts: int
    end_ts: int
    min_size_usd: float
    bubbles: List[VolumeBubble]
    total_count: int


class DepthLevel(BaseModel):
    """Depth at a specific percentage band."""
    percentage: int
    depth: float
    notional: float


class DepthSnapshot(BaseModel):
    """A single order book depth snapshot."""
    timestamp_ms: int
    bids: Dict[int, Dict[str, float]]  # percentage -> {depth, notional}
    asks: Dict[int, Dict[str, float]]


class DepthDataResponse(BaseModel):
    """Response containing book depth snapshots."""
    start_ts: int
    end_ts: int
    snapshots: List[DepthSnapshot]
    total_snapshots: int


class HeatmapStats(BaseModel):
    """Statistics about available heatmap data."""
    trades_available: bool
    depth_available: bool
    trades_count: Optional[int] = None
    depth_snapshots: Optional[int] = None
    min_timestamp: Optional[int] = None
    max_timestamp: Optional[int] = None


# ============================================================================
# Endpoints
# ============================================================================

@router.get("/stats", response_model=HeatmapStats)
def get_heatmap_stats():
    """Get statistics about available heatmap data sources."""
    stats = HeatmapStats(trades_available=False, depth_available=False)
    
    # Check trades data
    try:
        trades_db = get_trades_db()
        trades_stats = trades_db.get_stats()
        stats.trades_available = True
        stats.trades_count = trades_stats.get("total_trades", 0)
    except Exception as e:
        logger.debug(f"Trades data not available: {e}")
    
    # Check depth data
    try:
        depth_db = get_depth_db()
        depth_stats = depth_db.get_stats()
        stats.depth_available = True
        stats.depth_snapshots = depth_stats.get("unique_snapshots", 0)
        stats.min_timestamp = depth_stats.get("min_timestamp")
        stats.max_timestamp = depth_stats.get("max_timestamp")
    except Exception as e:
        logger.debug(f"Depth data not available: {e}")
    
    return stats


@router.get("/bubbles", response_model=VolumeBubblesResponse)
def get_volume_bubbles(
    symbol: str = Query("BTCUSDT", description="Trading pair"),
    start_ts: Optional[int] = Query(None, description="Start timestamp (ms)"),
    end_ts: Optional[int] = Query(None, description="End timestamp (ms)"),
    min_size_usd: float = Query(50000, description="Minimum trade size in USD"),
    max_size_usd: Optional[float] = Query(None, description="Maximum trade size in USD"),
    limit: int = Query(1000, description="Maximum number of bubbles to return")
):
    """
    Get large executed trades for volume bubble visualization.
    
    Filters trades by min/max USD size to show trades within a specific range.
    """
    trades_db = get_trades_db()
    
    # Get time range if not specified
    if start_ts is None or end_ts is None:
        stats = trades_db.get_stats()
        if start_ts is None:
            # Default to last 24 hours
            start_ts = stats.get("max_timestamp", 0) - 86400000
        if end_ts is None:
            end_ts = stats.get("max_timestamp", 0)
    
    # Build max size filter if specified
    max_filter = f"AND quote_qty <= {max_size_usd}" if max_size_usd else ""
    
    # Query large trades using DuckDB
    query = f"""
        SELECT 
            timestamp,
            price,
            qty,
            quote_qty,
            is_buyer_maker
        FROM trades
        WHERE timestamp >= {start_ts} 
          AND timestamp <= {end_ts}
          AND quote_qty >= {min_size_usd}
          {max_filter}
        ORDER BY quote_qty DESC
        LIMIT {limit}
    """
    
    try:
        result = trades_db.conn.execute(query).fetchall()
    except Exception as e:
        logger.error(f"Failed to query large trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    bubbles = []
    for row in result:
        bubbles.append(VolumeBubble(
            timestamp_ms=row[0],
            price=row[1],
            qty=row[2],
            quote_qty=row[3],
            is_buy=not row[4]  # is_buyer_maker=True means SELL aggressor
        ))
    
    # Sort by time for display
    bubbles.sort(key=lambda x: x.timestamp_ms)
    
    return VolumeBubblesResponse(
        symbol=symbol,
        start_ts=start_ts,
        end_ts=end_ts,
        min_size_usd=min_size_usd,
        bubbles=bubbles,
        total_count=len(bubbles)
    )


@router.get("/depth", response_model=DepthDataResponse)
def get_depth_data(
    start_ts: Optional[int] = Query(None, description="Start timestamp (ms)"),
    end_ts: Optional[int] = Query(None, description="End timestamp (ms)"),
    max_snapshots: int = Query(500, description="Maximum snapshots to return")
):
    """
    Get order book depth snapshots for liquidity heatmap visualization.
    
    Returns depth data at percentage bands (±1% to ±5%) from price.
    """
    depth_db = get_depth_db()
    
    # Get time range if not specified
    if start_ts is None or end_ts is None:
        min_ts, max_ts = depth_db.get_time_range()
        if start_ts is None:
            start_ts = min_ts or 0
        if end_ts is None:
            end_ts = max_ts or 0
    
    # Get snapshots
    snapshots_raw = depth_db.get_depth_snapshots(start_ts, end_ts)
    
    # Limit results if needed
    if len(snapshots_raw) > max_snapshots:
        # Sample evenly across the range
        step = len(snapshots_raw) // max_snapshots
        snapshots_raw = snapshots_raw[::step][:max_snapshots]
    
    # Convert to response format
    snapshots = []
    for snap in snapshots_raw:
        snapshots.append(DepthSnapshot(
            timestamp_ms=snap["timestamp_ms"],
            bids=snap["bids"],
            asks=snap["asks"]
        ))
    
    return DepthDataResponse(
        start_ts=start_ts,
        end_ts=end_ts,
        snapshots=snapshots,
        total_snapshots=len(snapshots)
    )


@router.get("/depth/range")
def get_depth_time_range():
    """Get the available time range for depth data."""
    depth_db = get_depth_db()
    min_ts, max_ts = depth_db.get_time_range()
    
    return {
        "min_timestamp": min_ts,
        "max_timestamp": max_ts,
        "min_date": datetime.fromtimestamp(min_ts / 1000, tz=timezone.utc).isoformat() if min_ts else None,
        "max_date": datetime.fromtimestamp(max_ts / 1000, tz=timezone.utc).isoformat() if max_ts else None
    }


# ============================================================================
# Bybit Historical Order Book Endpoints
# ============================================================================

# Lazy-loaded Bybit order book DB
_bybit_orderbook_db: Optional[BybitOrderBookDB] = None

def get_bybit_orderbook_db() -> BybitOrderBookDB:
    """Lazy-load the BybitOrderBookDB instance."""
    global _bybit_orderbook_db
    if _bybit_orderbook_db is None:
        if not BYBIT_ORDERBOOK_PARQUET_DIR.exists() or not list(BYBIT_ORDERBOOK_PARQUET_DIR.glob("*.parquet")):
            raise HTTPException(
                status_code=503,
                detail="Bybit order book data not available. Run: python -m app.ingestion.bybit_orderbook convert"
            )
        _bybit_orderbook_db = BybitOrderBookDB()
    return _bybit_orderbook_db


@router.get("/bybit/depth")
def get_bybit_depth_heatmap(
    start_ts: Optional[int] = Query(None, description="Start timestamp (ms)"),
    end_ts: Optional[int] = Query(None, description="End timestamp (ms)"),
    price_bucket: float = Query(1.0, description="Price aggregation bucket size in $"),
    time_bucket_sec: int = Query(5, description="Time aggregation in seconds (5-60)"),
    price_min: Optional[float] = Query(None, description="Minimum price to include"),
    price_max: Optional[float] = Query(None, description="Maximum price to include"),
):
    """
    Get aggregated order book depth for heatmap visualization.
    
    Returns bid/ask liquidity aggregated by price and time buckets.
    Use small time_bucket_sec (5-10s) for fine-grained horizontal bands.
    Use price_min/price_max to filter to visible chart area.
    """
    try:
        db = get_bybit_orderbook_db()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    stats = db.get_stats()
    
    # Default time range
    if start_ts is None:
        start_ts = stats.get("min_timestamp", 0)
    if end_ts is None:
        end_ts = stats.get("max_timestamp", 0)
    
    # Clamp time bucket to reasonable range (1 second to 5 minutes)
    time_bucket_sec = max(1, min(time_bucket_sec, 300))
    time_bucket_ms = time_bucket_sec * 1000
    
    # Build price filter clause for visible range
    price_filter = ""
    if price_min is not None:
        price_filter += f" AND price >= {price_min}"
    if price_max is not None:
        price_filter += f" AND price <= {price_max}"
    
    # Query aggregated depth using FLOOR for proper bucketing
    query = f"""
        SELECT 
            CAST(FLOOR(timestamp / {time_bucket_ms}) * {time_bucket_ms} AS BIGINT) as time_bucket,
            side,
            FLOOR(price / {price_bucket}) * {price_bucket} as price_bucket,
            SUM(size) as total_size,
            AVG(mid_price) as avg_mid
        FROM orderbook
        WHERE timestamp >= {start_ts} AND timestamp < {end_ts}
        {price_filter}
        GROUP BY 1, 2, 3
        ORDER BY 1, 3
    """
    
    rows = db.conn.execute(query).fetchall()
    
    # ========================================================================
    # FILL-FORWARD LIQUIDITY PERSISTENCE
    # ========================================================================
    # Orders don't disappear when they go out of the order book range.
    # We need to persist the last known size at each price level until it's
    # updated with new data. This creates continuous horizontal bands.
    #
    # Algorithm:
    # 1. Collect all unique time buckets and price levels
    # 2. For each time bucket, carry forward prices from previous bucket
    # 3. Update with new data when available
    # 4. Apply decay to old data (optional, based on time since last update)
    # ========================================================================
    
    from collections import defaultdict
    
    # Group raw data by time bucket
    raw_by_time = defaultdict(dict)  # {time_bucket: {(side, price): size}}
    all_times = set()
    
    for row in rows:
        ts, side, price, size, mid = row
        raw_by_time[int(ts)][(side, float(price))] = float(size)
        all_times.add(int(ts))
    
    sorted_times = sorted(all_times)
    
    if not sorted_times:
        return {
            "start_ts": start_ts,
            "end_ts": end_ts,
            "price_bucket": price_bucket,
            "time_bucket_sec": time_bucket_sec,
            "price_range": {"min": price_min, "max": price_max},
            "data_points": 0,
            "data": []
        }
    
    # Build filled-forward data
    # State: {(side, price): (size, last_update_ts)}
    liquidity_state = {}
    heatmap_data = []
    
    # Decay factor: reduce size of stale levels (not updated recently)
    # After ~60 seconds without update, size drops to ~50%
    decay_half_life_ms = 30000  # 30 seconds
    
    for ts in sorted_times:
        current_data = raw_by_time[ts]
        
        # Update state with new data
        for (side, price), size in current_data.items():
            liquidity_state[(side, price)] = (size, ts)
        
        # Emit all known levels with decay applied
        for (side, price), (size, last_update) in liquidity_state.items():
            # Calculate decay based on staleness
            age_ms = ts - last_update
            if age_ms > 0:
                # Exponential decay
                decay = math.exp(-age_ms * math.log(2) / decay_half_life_ms)
                effective_size = size * decay
            else:
                effective_size = size
            
            # Only emit if size is meaningful (above 0.1% of original)
            if effective_size > size * 0.001:
                heatmap_data.append({
                    "timestamp": ts,
                    "side": side,
                    "price": price,
                    "size": effective_size,
                    "mid": 0  # Not tracking mid for fill-forward
                })
        
        # Prune very old entries (> 5 minutes stale) to prevent unbounded growth
        prune_threshold_ms = 300000  # 5 minutes
        to_remove = [k for k, (_, last_update) in liquidity_state.items() 
                     if ts - last_update > prune_threshold_ms]
        for k in to_remove:
            del liquidity_state[k]
    
    logger.info(f"Heatmap fill-forward: {len(rows)} raw -> {len(heatmap_data)} filled points")
    
    return {
        "start_ts": start_ts,
        "end_ts": end_ts,
        "price_bucket": price_bucket,
        "time_bucket_sec": time_bucket_sec,
        "price_range": {"min": price_min, "max": price_max},
        "data_points": len(heatmap_data),
        "fill_forward": True,
        "raw_points": len(rows),
        "data": heatmap_data
    }


@router.get("/bybit/depth/stats")
def get_bybit_depth_stats():
    """Get statistics about Bybit order book data availability."""
    try:
        db = get_bybit_orderbook_db()
        stats = db.get_stats()
        return {
            "available": True,
            **stats,
            "min_date": datetime.fromtimestamp(stats.get("min_timestamp", 0) / 1000, tz=timezone.utc).isoformat() if stats.get("min_timestamp") else None,
            "max_date": datetime.fromtimestamp(stats.get("max_timestamp", 0) / 1000, tz=timezone.utc).isoformat() if stats.get("max_timestamp") else None
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


@router.get("/bybit/orderbook/snapshot")
def get_bybit_orderbook_snapshot(
    timestamp: int = Query(..., description="Timestamp (ms) to get nearest snapshot"),
    levels: int = Query(1000, description="Max number of price levels each side (0 = no limit)"),
    price_min: Optional[float] = Query(None, description="Minimum price to include"),
    price_max: Optional[float] = Query(None, description="Maximum price to include")
):
    """
    Get a single historical order book snapshot nearest to the given timestamp.
    Used for populating the DOM (Depth of Market) panel with historical data.
    
    Returns the FULL order book - all levels within the price range.
    The DOM should display the ENTIRE depth, not just a few levels.
    """
    try:
        db = get_bybit_orderbook_db()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    # Find the nearest snapshot timestamp
    query = f"""
        SELECT timestamp 
        FROM orderbook 
        WHERE timestamp <= {timestamp}
        ORDER BY timestamp DESC
        LIMIT 1
    """
    result = db.conn.execute(query).fetchone()
    
    if not result:
        # Try forward if nothing before
        query = f"""
            SELECT timestamp 
            FROM orderbook 
            WHERE timestamp >= {timestamp}
            ORDER BY timestamp ASC
            LIMIT 1
        """
        result = db.conn.execute(query).fetchone()
    
    if not result:
        return {"error": "No snapshot found", "timestamp": timestamp}
    
    snap_ts = result[0]
    
    # Build price filter clause
    price_filter = ""
    if price_min is not None:
        price_filter += f" AND price >= {price_min}"
    if price_max is not None:
        price_filter += f" AND price <= {price_max}"
    
    # Build limit clause - if levels=0 or price range is specified, get ALL levels
    limit_clause = "" if (levels == 0 or (price_min is not None and price_max is not None)) else f"LIMIT {levels}"
    
    # Get ALL bids within price range (descending price)
    bids_query = f"""
        SELECT price, size
        FROM orderbook
        WHERE timestamp = {snap_ts} AND side = 'bid' {price_filter}
        ORDER BY price DESC
        {limit_clause}
    """
    bids = [[row[0], row[1]] for row in db.conn.execute(bids_query).fetchall()]
    
    # Get ALL asks within price range (ascending price)
    asks_query = f"""
        SELECT price, size
        FROM orderbook
        WHERE timestamp = {snap_ts} AND side = 'ask' {price_filter}
        ORDER BY price ASC
        {limit_clause}
    """
    asks = [[row[0], row[1]] for row in db.conn.execute(asks_query).fetchall()]
    
    # Calculate mid and spread
    mid_price = (bids[0][0] + asks[0][0]) / 2 if bids and asks else 0
    spread = asks[0][0] - bids[0][0] if bids and asks else 0
    
    return {
        "timestamp": snap_ts,
        "requested_ts": timestamp,
        "bids": bids,
        "asks": asks,
        "total_bid_levels": len(bids),
        "total_ask_levels": len(asks),
        "mid_price": mid_price,
        "spread": spread,
        "exchange": "bybit",
        "price_range": {"min": price_min, "max": price_max} if price_min or price_max else None
    }


@router.get("/bybit/orderbook/snapshots")
def get_bybit_orderbook_snapshots(
    start_ts: int = Query(..., description="Start timestamp (ms)"),
    end_ts: int = Query(..., description="End timestamp (ms)"),
    max_snapshots: int = Query(100, description="Maximum number of snapshots"),
    levels: int = Query(20, description="Number of price levels each side")
):
    """
    Get multiple historical order book snapshots for a time range.
    Used for historical heatmap rendering.
    """
    try:
        db = get_bybit_orderbook_db()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    # Get evenly spaced timestamps
    time_range = end_ts - start_ts
    interval = max(time_range // max_snapshots, 1000)  # At least 1 second apart
    
    snapshots = []
    current_ts = start_ts
    
    while current_ts < end_ts and len(snapshots) < max_snapshots:
        # Get nearest snapshot
        query = f"""
            SELECT DISTINCT timestamp 
            FROM orderbook 
            WHERE timestamp >= {current_ts} AND timestamp < {current_ts + interval}
            ORDER BY timestamp ASC
            LIMIT 1
        """
        result = db.conn.execute(query).fetchone()
        
        if result:
            snap_ts = result[0]
            
            # Get bids
            bids = [[row[0], row[1]] for row in db.conn.execute(f"""
                SELECT price, size FROM orderbook
                WHERE timestamp = {snap_ts} AND side = 'bid'
                ORDER BY price DESC LIMIT {levels}
            """).fetchall()]
            
            # Get asks
            asks = [[row[0], row[1]] for row in db.conn.execute(f"""
                SELECT price, size FROM orderbook
                WHERE timestamp = {snap_ts} AND side = 'ask'
                ORDER BY price ASC LIMIT {levels}
            """).fetchall()]
            
            if bids and asks:
                snapshots.append({
                    "timestamp": snap_ts,
                    "bids": bids,
                    "asks": asks,
                    "mid_price": (bids[0][0] + asks[0][0]) / 2
                })
        
        current_ts += interval
    
    return {
        "start_ts": start_ts,
        "end_ts": end_ts,
        "count": len(snapshots),
        "snapshots": snapshots
    }
