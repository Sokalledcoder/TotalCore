"""
Book depth data processing pipeline for heatmap visualization.

Handles:
- Loading book depth CSV files
- Converting percentage bands to absolute price levels
- Querying depth data for time ranges
- Providing data for liquidity heatmap visualization
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

import pandas as pd
import duckdb

logger = logging.getLogger(__name__)

# Default paths for book depth data
BOOKDEPTH_DATA_DIR = Path("TRADES-DATA/BTC-USDT-BOOKDEPTH-BINANCE-FUTURES")


class BookDepthDB:
    """
    Manages book depth data loading and querying using DuckDB.
    
    The book depth data contains aggregated order book snapshots at percentage
    bands from the current price (±1% to ±5%).
    """
    
    def __init__(self, data_dir: Path = BOOKDEPTH_DATA_DIR):
        self.data_dir = Path(data_dir)
        self.conn = duckdb.connect(":memory:")
        self._table_created = False
        
    def _ensure_table(self):
        """Create the book depth table if it doesn't exist."""
        if self._table_created:
            return
            
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS book_depth (
                timestamp TIMESTAMP,
                timestamp_ms BIGINT,
                percentage INTEGER,
                depth DOUBLE,
                notional DOUBLE
            )
        """)
        self._table_created = True
        
    def load_csv_files(self, symbol: str = "BTCUSDT") -> int:
        """
        Load all book depth CSV files for the given symbol.
        
        Returns the number of rows loaded.
        """
        self._ensure_table()
        
        # Clear existing data
        self.conn.execute("DELETE FROM book_depth")
        
        csv_files = sorted(self.data_dir.glob(f"{symbol}-bookDepth-*.csv"))
        if not csv_files:
            logger.warning(f"No book depth files found in {self.data_dir}")
            return 0
            
        total_rows = 0
        for csv_file in csv_files:
            logger.info(f"Loading book depth: {csv_file.name}")
            
            # Load CSV into DuckDB - timestamp is string in format 'YYYY-MM-DD HH:MM:SS'
            self.conn.execute(f"""
                INSERT INTO book_depth
                SELECT 
                    strptime(CAST(timestamp AS VARCHAR), '%Y-%m-%d %H:%M:%S') as timestamp,
                    epoch_ms(strptime(CAST(timestamp AS VARCHAR), '%Y-%m-%d %H:%M:%S')) as timestamp_ms,
                    CAST(percentage AS INTEGER) as percentage,
                    CAST(depth AS DOUBLE) as depth,
                    CAST(notional AS DOUBLE) as notional
                FROM read_csv_auto('{csv_file}')
            """)
            
            count = self.conn.execute("SELECT COUNT(*) FROM book_depth").fetchone()[0]
            total_rows = count
            
        logger.info(f"Loaded {total_rows} book depth records")
        return total_rows
        
    def get_depth_for_range(
        self,
        start_ts: int,
        end_ts: int,
        reference_prices: Optional[Dict[int, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get book depth data for a time range.
        
        Args:
            start_ts: Start timestamp in milliseconds
            end_ts: End timestamp in milliseconds  
            reference_prices: Optional dict mapping timestamp_ms -> price
                             Used to convert percentage bands to absolute prices
        
        Returns:
            List of depth records with timestamp, percentage, depth, notional
        """
        result = self.conn.execute("""
            SELECT 
                timestamp_ms,
                percentage,
                depth,
                notional
            FROM book_depth
            WHERE timestamp_ms >= ? AND timestamp_ms <= ?
            ORDER BY timestamp_ms, percentage
        """, [start_ts, end_ts]).fetchall()
        
        records = []
        for row in result:
            record = {
                "timestamp_ms": row[0],
                "percentage": row[1],
                "depth": row[2],
                "notional": row[3]
            }
            
            # If we have reference prices, calculate absolute price levels
            if reference_prices:
                # Find closest reference price
                closest_ts = min(reference_prices.keys(), 
                                key=lambda x: abs(x - row[0]), 
                                default=None)
                if closest_ts:
                    ref_price = reference_prices[closest_ts]
                    record["price"] = ref_price * (1 + row[1] / 100)
                    
            records.append(record)
            
        return records
    
    def get_depth_snapshots(
        self,
        start_ts: int,
        end_ts: int
    ) -> List[Dict[str, Any]]:
        """
        Get book depth snapshots grouped by timestamp.
        
        Returns a list of snapshots, each containing bid/ask depth at all levels.
        """
        result = self.conn.execute("""
            SELECT 
                timestamp_ms,
                percentage,
                depth,
                notional
            FROM book_depth
            WHERE timestamp_ms >= ? AND timestamp_ms <= ?
            ORDER BY timestamp_ms, percentage
        """, [start_ts, end_ts]).fetchall()
        
        # Group by timestamp
        snapshots = {}
        for row in result:
            ts = row[0]
            if ts not in snapshots:
                snapshots[ts] = {
                    "timestamp_ms": ts,
                    "bids": {},  # percentage -> {depth, notional}
                    "asks": {}
                }
            
            pct = row[1]
            data = {"depth": row[2], "notional": row[3]}
            
            if pct < 0:
                snapshots[ts]["bids"][pct] = data
            else:
                snapshots[ts]["asks"][pct] = data
                
        return list(snapshots.values())
    
    def get_time_range(self) -> tuple[Optional[int], Optional[int]]:
        """Get the min and max timestamps in the loaded data."""
        result = self.conn.execute("""
            SELECT MIN(timestamp_ms), MAX(timestamp_ms)
            FROM book_depth
        """).fetchone()
        return result[0], result[1]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the loaded book depth data."""
        count = self.conn.execute("SELECT COUNT(*) FROM book_depth").fetchone()[0]
        min_ts, max_ts = self.get_time_range()
        
        unique_timestamps = self.conn.execute(
            "SELECT COUNT(DISTINCT timestamp_ms) FROM book_depth"
        ).fetchone()[0]
        
        return {
            "total_records": count,
            "unique_snapshots": unique_timestamps,
            "min_timestamp": min_ts,
            "max_timestamp": max_ts,
            "levels_per_snapshot": 10  # 5 bid + 5 ask
        }


# Global instance for the application
_bookdepth_db: Optional[BookDepthDB] = None


def get_bookdepth_db() -> BookDepthDB:
    """Get or create the global BookDepthDB instance."""
    global _bookdepth_db
    if _bookdepth_db is None:
        _bookdepth_db = BookDepthDB()
    return _bookdepth_db
