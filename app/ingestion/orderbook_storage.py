"""
Order Book Storage - Efficient persistent storage for order book snapshots.

Stores aggregated order book data to DuckDB for historical heatmap visualization.
Uses price bucketing and time sampling to minimize storage while preserving visual fidelity.

Storage Strategy:
- Store one snapshot per N seconds (configurable, default 10s)
- Aggregate quantities at price buckets (e.g., $10 buckets)
- Keep top M price levels per side (configurable, default 50)
- Estimated storage: ~2KB per snapshot, ~17MB per day at 10s intervals
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import duckdb

logger = logging.getLogger(__name__)

# Default database path
DEFAULT_DB_PATH = Path("data/orderbook.db")


class OrderBookStorage:
    """
    Persistent storage for order book snapshots.
    
    Usage:
        storage = OrderBookStorage()
        storage.store_snapshot(timestamp_ms, symbol, bids, asks)
        snapshots = storage.get_snapshots(symbol, start_ts, end_ts)
    """
    
    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._init_tables()
        
    def _init_tables(self) -> None:
        """Initialize database tables"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orderbook_snapshots (
                timestamp_ms BIGINT NOT NULL,
                symbol VARCHAR NOT NULL,
                price_bucket DOUBLE NOT NULL,
                bid_qty DOUBLE DEFAULT 0,
                ask_qty DOUBLE DEFAULT 0,
                PRIMARY KEY (timestamp_ms, symbol, price_bucket)
            )
        """)
        
        # Index for time-range queries
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_ob_time_symbol 
            ON orderbook_snapshots (symbol, timestamp_ms)
        """)
        
        logger.info(f"OrderBook storage initialized at {self.db_path}")
        
    def store_snapshot(
        self,
        timestamp_ms: int,
        symbol: str,
        bids: List[Tuple[float, float]],
        asks: List[Tuple[float, float]],
        price_bucket_size: float = 10.0,
        max_levels: int = 50
    ) -> int:
        """
        Store an order book snapshot.
        
        Args:
            timestamp_ms: Timestamp in milliseconds
            symbol: Trading pair symbol
            bids: List of (price, quantity) tuples for bids
            asks: List of (price, quantity) tuples for asks
            price_bucket_size: Size of price buckets for aggregation
            max_levels: Maximum number of price levels to store per side
            
        Returns:
            Number of rows stored
        """
        # Aggregate into buckets
        bid_buckets: Dict[float, float] = {}
        ask_buckets: Dict[float, float] = {}
        
        for price, qty in bids[:max_levels]:
            bucket = (price // price_bucket_size) * price_bucket_size
            bid_buckets[bucket] = bid_buckets.get(bucket, 0) + qty
            
        for price, qty in asks[:max_levels]:
            bucket = (price // price_bucket_size) * price_bucket_size
            ask_buckets[bucket] = ask_buckets.get(bucket, 0) + qty
        
        # Combine buckets
        all_buckets = set(bid_buckets.keys()) | set(ask_buckets.keys())
        
        # Insert rows
        rows = [
            (timestamp_ms, symbol, bucket, 
             bid_buckets.get(bucket, 0), 
             ask_buckets.get(bucket, 0))
            for bucket in all_buckets
        ]
        
        if rows:
            self.conn.executemany(
                """
                INSERT OR REPLACE INTO orderbook_snapshots 
                (timestamp_ms, symbol, price_bucket, bid_qty, ask_qty)
                VALUES (?, ?, ?, ?, ?)
                """,
                rows
            )
            
        return len(rows)
    
    def get_snapshots(
        self,
        symbol: str,
        start_ts: int,
        end_ts: int,
        max_snapshots: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Get order book snapshots for a time range.
        
        Returns:
            List of snapshots, each containing:
            {
                "timestamp": int,
                "bids": [[price, qty], ...],
                "asks": [[price, qty], ...]
            }
        """
        # Get unique timestamps in range
        timestamps = self.conn.execute(
            """
            SELECT DISTINCT timestamp_ms 
            FROM orderbook_snapshots
            WHERE symbol = ? AND timestamp_ms >= ? AND timestamp_ms <= ?
            ORDER BY timestamp_ms
            LIMIT ?
            """,
            [symbol, start_ts, end_ts, max_snapshots]
        ).fetchall()
        
        if not timestamps:
            return []
        
        result = []
        for (ts,) in timestamps:
            # Get data for this timestamp
            rows = self.conn.execute(
                """
                SELECT price_bucket, bid_qty, ask_qty
                FROM orderbook_snapshots
                WHERE symbol = ? AND timestamp_ms = ?
                ORDER BY price_bucket
                """,
                [symbol, ts]
            ).fetchall()
            
            bids = [[price, bid_qty] for price, bid_qty, _ in rows if bid_qty > 0]
            asks = [[price, ask_qty] for price, _, ask_qty in rows if ask_qty > 0]
            
            # Sort: bids descending, asks ascending
            bids.sort(key=lambda x: -x[0])
            asks.sort(key=lambda x: x[0])
            
            result.append({
                "timestamp": ts,
                "bids": bids,
                "asks": asks
            })
            
        return result
    
    def get_stats(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get storage statistics"""
        if symbol:
            count = self.conn.execute(
                "SELECT COUNT(DISTINCT timestamp_ms) FROM orderbook_snapshots WHERE symbol = ?",
                [symbol]
            ).fetchone()[0]
            
            time_range = self.conn.execute(
                "SELECT MIN(timestamp_ms), MAX(timestamp_ms) FROM orderbook_snapshots WHERE symbol = ?",
                [symbol]
            ).fetchone()
        else:
            count = self.conn.execute(
                "SELECT COUNT(DISTINCT timestamp_ms) FROM orderbook_snapshots"
            ).fetchone()[0]
            
            time_range = self.conn.execute(
                "SELECT MIN(timestamp_ms), MAX(timestamp_ms) FROM orderbook_snapshots"
            ).fetchone()
        
        return {
            "snapshot_count": count,
            "min_timestamp": time_range[0],
            "max_timestamp": time_range[1],
            "db_path": str(self.db_path)
        }
    
    def cleanup_old_data(self, older_than_days: int = 7) -> int:
        """Delete snapshots older than specified days"""
        cutoff = int((time.time() - older_than_days * 24 * 3600) * 1000)
        
        result = self.conn.execute(
            "DELETE FROM orderbook_snapshots WHERE timestamp_ms < ?",
            [cutoff]
        )
        
        deleted = result.rowcount
        logger.info(f"Cleaned up {deleted} old order book rows")
        return deleted
    
    def close(self) -> None:
        """Close database connection"""
        self.conn.close()


# Global storage instance
_storage: Optional[OrderBookStorage] = None


def get_orderbook_storage() -> OrderBookStorage:
    """Get or create the global OrderBookStorage instance"""
    global _storage
    if _storage is None:
        _storage = OrderBookStorage()
    return _storage
