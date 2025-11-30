"""
Live Order Book Streaming via CCXT Pro WebSocket

Streams real-time order book data from Binance Futures and stores snapshots
for heatmap visualization. Uses CCXT Pro for WebSocket connectivity.

Storage Strategy:
- Keep last N snapshots in memory for immediate visualization
- Periodically aggregate and store to DuckDB for historical analysis
- Aggregate by rounding to configurable price buckets to save space
"""
from __future__ import annotations

import asyncio
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class OrderBookSnapshot:
    """A single order book snapshot at a point in time"""
    timestamp_ms: int
    symbol: str
    bids: List[Tuple[float, float]]  # [(price, quantity), ...]
    asks: List[Tuple[float, float]]  # [(price, quantity), ...]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp_ms,
            "symbol": self.symbol,
            "bids": self.bids,
            "asks": self.asks
        }


@dataclass
class OrderBookStreamConfig:
    """Configuration for order book streaming"""
    symbol: str = "BTC/USDT:USDT"  # CCXT unified symbol for Binance Futures
    depth_limit: int = 500  # Number of price levels to keep (500 = covers ~$2K each side)
    snapshot_interval_ms: int = 500  # How often to capture snapshots
    max_snapshots_in_memory: int = 1000  # Rolling window of snapshots
    aggregate_price_bucket: float = 5.0  # Aggregate prices to $5 buckets for storage
    exchange: str = "binanceusdm"  # Binance USDT-M Futures
    persist_interval_ms: int = 10000  # How often to persist to storage (10s)
    persist_bucket_size: float = 10.0  # Price bucket size for persistence


class OrderBookStreamer:
    """
    Streams live order book data via CCXT Pro WebSocket.
    
    Usage:
        streamer = OrderBookStreamer()
        await streamer.start()
        
        # Get recent snapshots for visualization
        snapshots = streamer.get_recent_snapshots(limit=100)
        
        # Stop streaming
        await streamer.stop()
    """
    
    def __init__(self, config: Optional[OrderBookStreamConfig] = None):
        self.config = config or OrderBookStreamConfig()
        self.exchange = None
        self.running = False
        self.snapshots: deque[OrderBookSnapshot] = deque(
            maxlen=self.config.max_snapshots_in_memory
        )
        self.last_snapshot_time = 0
        self.last_persist_time = 0
        self.callbacks: List[Callable[[OrderBookSnapshot], None]] = []
        self._task: Optional[asyncio.Task] = None
        self._storage = None  # Lazy-loaded storage
        
    async def start(self) -> None:
        """Start the order book streaming"""
        if self.running:
            logger.warning("OrderBookStreamer already running")
            return
            
        # Import ccxt.pro for WebSocket support
        try:
            import ccxt.pro as ccxtpro
        except ImportError:
            logger.error("ccxt.pro not available. Install with: pip install ccxt[async]")
            raise ImportError("CCXT Pro required for WebSocket streaming")
        
        # Create exchange instance
        exchange_class = getattr(ccxtpro, self.config.exchange)
        self.exchange = exchange_class({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
            }
        })
        
        self.running = True
        self._task = asyncio.create_task(self._stream_loop())
        logger.info(f"Started order book streaming for {self.config.symbol}")
        
    async def stop(self) -> None:
        """Stop the order book streaming"""
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
            
        logger.info("Stopped order book streaming")
        
    async def _stream_loop(self) -> None:
        """Main streaming loop"""
        while self.running:
            try:
                # Watch the order book
                orderbook = await self.exchange.watch_order_book(
                    self.config.symbol,
                    limit=self.config.depth_limit
                )
                
                # Check if enough time has passed for a new snapshot
                now_ms = int(time.time() * 1000)
                if now_ms - self.last_snapshot_time >= self.config.snapshot_interval_ms:
                    self._capture_snapshot(orderbook, now_ms)
                    self.last_snapshot_time = now_ms
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in order book stream: {e}")
                await asyncio.sleep(1)  # Back off on error
                
    def _capture_snapshot(self, orderbook: Dict[str, Any], timestamp_ms: int) -> None:
        """Capture a snapshot from the order book"""
        # Extract bids and asks
        bids = [(float(price), float(qty)) for price, qty in orderbook.get('bids', [])]
        asks = [(float(price), float(qty)) for price, qty in orderbook.get('asks', [])]
        
        snapshot = OrderBookSnapshot(
            timestamp_ms=timestamp_ms,
            symbol=self.config.symbol,
            bids=bids,
            asks=asks
        )
        
        self.snapshots.append(snapshot)
        
        # Persist to storage periodically
        if timestamp_ms - self.last_persist_time >= self.config.persist_interval_ms:
            self._persist_snapshot(snapshot)
            self.last_persist_time = timestamp_ms
        
        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback(snapshot)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def _persist_snapshot(self, snapshot: OrderBookSnapshot) -> None:
        """Persist a snapshot to storage"""
        try:
            if self._storage is None:
                from app.ingestion.orderbook_storage import get_orderbook_storage
                self._storage = get_orderbook_storage()
            
            rows = self._storage.store_snapshot(
                timestamp_ms=snapshot.timestamp_ms,
                symbol=snapshot.symbol,
                bids=snapshot.bids,
                asks=snapshot.asks,
                price_bucket_size=self.config.persist_bucket_size
            )
            logger.debug(f"Persisted {rows} order book rows")
        except Exception as e:
            logger.error(f"Failed to persist snapshot: {e}")
                
    def add_callback(self, callback: Callable[[OrderBookSnapshot], None]) -> None:
        """Add a callback to be notified on each snapshot"""
        self.callbacks.append(callback)
        
    def remove_callback(self, callback: Callable[[OrderBookSnapshot], None]) -> None:
        """Remove a callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
            
    def get_recent_snapshots(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent snapshots for visualization"""
        snapshots = list(self.snapshots)[-limit:]
        return [s.to_dict() for s in snapshots]
    
    def get_latest_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get the most recent snapshot"""
        if self.snapshots:
            return self.snapshots[-1].to_dict()
        return None
    
    def get_aggregated_depth(
        self, 
        price_bucket: Optional[float] = None,
        levels: int = 50
    ) -> Dict[str, Any]:
        """
        Get aggregated order book depth for visualization.
        Aggregates quantities at price buckets for cleaner display.
        
        Returns:
            {
                "timestamp": int,
                "bids": {price_bucket: total_qty, ...},
                "asks": {price_bucket: total_qty, ...}
            }
        """
        if not self.snapshots:
            return {"timestamp": 0, "bids": {}, "asks": {}}
            
        latest = self.snapshots[-1]
        bucket = price_bucket or self.config.aggregate_price_bucket
        
        def aggregate(orders: List[Tuple[float, float]], is_bid: bool) -> Dict[float, float]:
            result = {}
            for price, qty in orders[:levels]:
                # Round to bucket
                if is_bid:
                    bucket_price = (price // bucket) * bucket
                else:
                    bucket_price = ((price // bucket) + 1) * bucket
                    
                if bucket_price not in result:
                    result[bucket_price] = 0
                result[bucket_price] += qty
            return result
        
        return {
            "timestamp": latest.timestamp_ms,
            "bids": aggregate(latest.bids, True),
            "asks": aggregate(latest.asks, False)
        }


# Global instance for the application
_orderbook_streamer: Optional[OrderBookStreamer] = None


def get_orderbook_streamer() -> OrderBookStreamer:
    """Get or create the global OrderBookStreamer instance"""
    global _orderbook_streamer
    if _orderbook_streamer is None:
        _orderbook_streamer = OrderBookStreamer()
    return _orderbook_streamer


async def start_orderbook_streaming(config: Optional[OrderBookStreamConfig] = None) -> OrderBookStreamer:
    """Start the global order book streamer"""
    global _orderbook_streamer
    if _orderbook_streamer is None:
        _orderbook_streamer = OrderBookStreamer(config)
    await _orderbook_streamer.start()
    return _orderbook_streamer


async def stop_orderbook_streaming() -> None:
    """Stop the global order book streamer"""
    global _orderbook_streamer
    if _orderbook_streamer:
        await _orderbook_streamer.stop()
        _orderbook_streamer = None
