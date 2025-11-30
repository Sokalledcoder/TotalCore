"""
Bybit Order Book data processing for heatmap visualization.

Handles:
- NDJSON file parsing (Line-delimited JSON)
- Snapshot and delta processing
- Conversion to efficient storage format (Parquet)

Bybit Order Book NDJSON format:
{
    "topic": "orderbook.200.BTCUSDT",
    "type": "snapshot" | "delta",
    "ts": 1764288001116,  // Receive timestamp (ms)
    "data": {
        "s": "BTCUSDT",
        "b": [["91284.10", "3.590"], ...],  // Bids [price, size]
        "a": [["91284.20", "3.739"], ...],  // Asks [price, size]
        "u": 12724436,  // Update ID
        "seq": 489397002815
    },
    "cts": 1764288001005  // Cross timestamp
}
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional, Iterator, List, Dict, Any, Tuple
from dataclasses import dataclass, field

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb

logger = logging.getLogger(__name__)

# Paths
BYBIT_BOOKDEPTH_DIR = Path("TRADES-DATA/BTC-USDT-BOOKDEPTH-BYBIT-FUTURES")
BYBIT_ORDERBOOK_PARQUET_DIR = Path("data/bybit_orderbook_parquet")


@dataclass
class OrderBookSnapshot:
    """A single order book snapshot."""
    timestamp_ms: int
    bids: List[Tuple[float, float]]  # [(price, size), ...]
    asks: List[Tuple[float, float]]  # [(price, size), ...]
    symbol: str = "BTCUSDT"
    exchange: str = "bybit"
    
    @property
    def mid_price(self) -> float:
        """Calculate mid price from best bid/ask."""
        if self.bids and self.asks:
            return (self.bids[0][0] + self.asks[0][0]) / 2
        return 0.0
    
    @property
    def spread(self) -> float:
        """Calculate spread from best bid/ask."""
        if self.bids and self.asks:
            return self.asks[0][0] - self.bids[0][0]
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp_ms,
            "bids": self.bids,
            "asks": self.asks,
            "mid_price": self.mid_price,
            "spread": self.spread,
            "exchange": self.exchange
        }


def parse_ndjson_file(
    file_path: Path,
    max_snapshots: Optional[int] = None,
    snapshot_interval_ms: int = 100  # Only keep snapshots at least 100ms apart
) -> Iterator[OrderBookSnapshot]:
    """
    Parse a Bybit order book NDJSON file with delta updates.
    
    Bybit sends an initial snapshot, then delta updates. This function
    maintains order book state and applies deltas incrementally.
    
    Args:
        file_path: Path to the .data file
        max_snapshots: Maximum number of snapshots to return (for testing)
        snapshot_interval_ms: Minimum interval between snapshots (reduces data)
    
    Yields:
        OrderBookSnapshot objects (reconstructed from deltas)
    """
    count = 0
    last_yield_ts = 0
    
    # Current order book state
    current_bids: Dict[float, float] = {}  # price -> size
    current_asks: Dict[float, float] = {}  # price -> size
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f):
            if not line.strip():
                continue
            
            try:
                data = json.loads(line)
                msg_type = data.get('type')
                ts = data.get('ts', 0)
                ob_data = data.get('data', {})
                
                if msg_type == 'snapshot':
                    # Reset order book with snapshot
                    current_bids = {float(b[0]): float(b[1]) for b in ob_data.get('b', [])}
                    current_asks = {float(a[0]): float(a[1]) for a in ob_data.get('a', [])}
                    
                elif msg_type == 'delta':
                    # Apply delta updates
                    # In Bybit: size=0 means remove the level
                    for b in ob_data.get('b', []):
                        price, size = float(b[0]), float(b[1])
                        if size == 0:
                            current_bids.pop(price, None)
                        else:
                            current_bids[price] = size
                    
                    for a in ob_data.get('a', []):
                        price, size = float(a[0]), float(a[1])
                        if size == 0:
                            current_asks.pop(price, None)
                        else:
                            current_asks[price] = size
                else:
                    continue
                
                # Rate limit output snapshots
                if ts - last_yield_ts < snapshot_interval_ms:
                    continue
                
                # Build sorted lists
                bids = sorted(current_bids.items(), key=lambda x: -x[0])  # Descending
                asks = sorted(current_asks.items(), key=lambda x: x[0])   # Ascending
                
                if not bids or not asks:
                    continue
                
                snapshot = OrderBookSnapshot(
                    timestamp_ms=ts,
                    bids=bids,
                    asks=asks,
                    symbol=ob_data.get('s', 'BTCUSDT')
                )
                
                yield snapshot
                count += 1
                last_yield_ts = ts
                
                if max_snapshots and count >= max_snapshots:
                    break
                
                if count % 10000 == 0:
                    logger.info(f"  Processed {count} snapshots, line {line_num:,}...")
                    
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse line {line_num}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Error processing line {line_num}: {e}")
                continue
    
    logger.info(f"Parsed {count} snapshots from {file_path}")


def convert_to_parquet(
    ndjson_path: Path,
    output_dir: Path = BYBIT_ORDERBOOK_PARQUET_DIR,
    snapshot_interval_ms: int = 500,  # Keep 2 snapshots per second for smooth heatmap
    levels_to_keep: int = 100  # Keep 100 levels each side (full depth coverage)
) -> Path:
    """
    Convert NDJSON order book file to compact Parquet format.
    
    We store flattened snapshots with aggregated levels for efficient
    heatmap rendering.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output filename
    stem = ndjson_path.stem  # 2025-11-28_BTCUSDT_ob200
    output_path = output_dir / f"{stem}.parquet"
    
    if output_path.exists():
        logger.info(f"Parquet file already exists: {output_path}")
        return output_path
    
    logger.info(f"Converting {ndjson_path} to Parquet (interval={snapshot_interval_ms}ms)")
    
    records = []
    count = 0
    
    for snapshot in parse_ndjson_file(
        ndjson_path, 
        snapshot_interval_ms=snapshot_interval_ms
    ):
        # Store each price level as a row for efficient querying
        for side, levels in [('bid', snapshot.bids[:levels_to_keep]), 
                             ('ask', snapshot.asks[:levels_to_keep])]:
            for price, size in levels:
                records.append({
                    'timestamp': snapshot.timestamp_ms,
                    'side': side,
                    'price': price,
                    'size': size,
                    'mid_price': snapshot.mid_price
                })
        
        count += 1
        if count % 10000 == 0:
            logger.info(f"  Processed {count} snapshots...")
    
    if not records:
        logger.warning("No records to write")
        return output_path
    
    # Convert to Parquet
    df = pd.DataFrame(records)
    df.to_parquet(output_path, compression='snappy', index=False)
    
    logger.info(f"Wrote {len(records):,} records ({count} snapshots) to {output_path}")
    return output_path


def convert_all_bybit_orderbooks(
    data_dir: Path = BYBIT_BOOKDEPTH_DIR,
    snapshot_interval_ms: int = 1000
) -> List[Path]:
    """Convert all Bybit order book files to Parquet."""
    parquet_files = []
    
    for data_file in sorted(data_dir.glob("*.data")):
        output = convert_to_parquet(data_file, snapshot_interval_ms=snapshot_interval_ms)
        parquet_files.append(output)
    
    return parquet_files


class BybitOrderBookDB:
    """
    Query interface for Bybit order book data stored in Parquet format.
    Uses DuckDB for efficient analytical queries.
    """
    
    def __init__(self, parquet_dir: Path = BYBIT_ORDERBOOK_PARQUET_DIR):
        self.parquet_dir = parquet_dir
        self.conn = duckdb.connect()
        self._register_parquet_files()
    
    def _register_parquet_files(self) -> None:
        """Register all Parquet files as a unified 'orderbook' view."""
        if not self.parquet_dir.exists():
            logger.warning(f"Parquet directory does not exist: {self.parquet_dir}")
            return
        
        parquet_files = list(self.parquet_dir.glob("*.parquet"))
        if not parquet_files:
            logger.warning(f"No Parquet files found in {self.parquet_dir}")
            return
        
        # Create a view over all Parquet files
        files_pattern = str(self.parquet_dir / "*.parquet")
        self.conn.execute(f"""
            CREATE OR REPLACE VIEW orderbook AS 
            SELECT * FROM read_parquet('{files_pattern}')
        """)
        
        logger.info(f"Registered {len(parquet_files)} Bybit order book Parquet files")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get basic statistics about the loaded order book data."""
        try:
            result = self.conn.execute("""
                SELECT 
                    COUNT(*) as total_records,
                    COUNT(DISTINCT timestamp) as snapshot_count,
                    MIN(timestamp) as min_ts,
                    MAX(timestamp) as max_ts,
                    AVG(mid_price) as avg_mid_price
                FROM orderbook
            """).fetchone()
            
            if result:
                return {
                    "total_records": result[0],
                    "snapshot_count": result[1],
                    "min_timestamp": result[2],
                    "max_timestamp": result[3],
                    "avg_mid_price": result[4],
                    "exchange": "bybit"
                }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
        
        return {"total_records": 0, "exchange": "bybit"}
    
    def get_heatmap_data(
        self,
        start_ts: int,
        end_ts: int,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        time_bucket_ms: int = 60000,  # 1 minute buckets
        price_bucket_size: float = 10.0  # $10 price buckets
    ) -> List[Dict[str, Any]]:
        """
        Get aggregated order book data for heatmap visualization.
        
        Returns data bucketed by time and price for efficient rendering.
        """
        price_filter = ""
        if price_min is not None:
            price_filter += f" AND price >= {price_min}"
        if price_max is not None:
            price_filter += f" AND price <= {price_max}"
        
        query = f"""
            SELECT 
                (timestamp / {time_bucket_ms}) * {time_bucket_ms} as time_bucket,
                FLOOR(price / {price_bucket_size}) * {price_bucket_size} as price_bucket,
                side,
                AVG(size) as avg_size,
                MAX(size) as max_size,
                COUNT(*) as sample_count
            FROM orderbook
            WHERE timestamp >= {start_ts} AND timestamp < {end_ts}
            {price_filter}
            GROUP BY time_bucket, price_bucket, side
            ORDER BY time_bucket, price_bucket
        """
        
        results = []
        for row in self.conn.execute(query).fetchall():
            results.append({
                "time_bucket": row[0],
                "price_bucket": row[1],
                "side": row[2],
                "avg_size": row[3],
                "max_size": row[4],
                "sample_count": row[5]
            })
        
        return results
    
    def get_snapshots_for_timerange(
        self,
        start_ts: int,
        end_ts: int,
        max_snapshots: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get raw order book snapshots for a time range.
        
        Returns snapshots with full bid/ask arrays for DOM visualization.
        """
        # First get distinct timestamps
        ts_query = f"""
            SELECT DISTINCT timestamp
            FROM orderbook
            WHERE timestamp >= {start_ts} AND timestamp < {end_ts}
            ORDER BY timestamp
            LIMIT {max_snapshots}
        """
        
        timestamps = [row[0] for row in self.conn.execute(ts_query).fetchall()]
        
        snapshots = []
        for ts in timestamps:
            # Get bids for this timestamp
            bids_query = f"""
                SELECT price, size
                FROM orderbook
                WHERE timestamp = {ts} AND side = 'bid'
                ORDER BY price DESC
            """
            bids = [(row[0], row[1]) for row in self.conn.execute(bids_query).fetchall()]
            
            # Get asks for this timestamp
            asks_query = f"""
                SELECT price, size
                FROM orderbook
                WHERE timestamp = {ts} AND side = 'ask'
                ORDER BY price ASC
            """
            asks = [(row[0], row[1]) for row in self.conn.execute(asks_query).fetchall()]
            
            if bids and asks:
                mid_price = (bids[0][0] + asks[0][0]) / 2
                spread = asks[0][0] - bids[0][0]
            else:
                mid_price = 0
                spread = 0
            
            snapshots.append({
                "timestamp": ts,
                "bids": bids,
                "asks": asks,
                "mid_price": mid_price,
                "spread": spread,
                "exchange": "bybit"
            })
        
        return snapshots
    
    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()


# CLI for testing
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1 and sys.argv[1] == "convert":
        # Convert all NDJSON files
        files = convert_all_bybit_orderbooks()
        print(f"Converted {len(files)} files")
    elif len(sys.argv) > 1 and sys.argv[1] == "stats":
        # Show stats
        db = BybitOrderBookDB()
        stats = db.get_stats()
        print("Bybit Order Book Stats:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        db.close()
    else:
        print("Usage: python -m app.ingestion.bybit_orderbook [convert|stats]")
