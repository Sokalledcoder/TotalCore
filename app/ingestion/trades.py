"""
Trade data processing pipeline for footprint/volume profile analysis.

Handles:
- CSV to Parquet conversion (memory-efficient chunked processing)
- Loading into DuckDB
- Aggregation into volume profiles per candle
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Iterator
from datetime import datetime, timezone

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb

logger = logging.getLogger(__name__)

# Schema for trades
TRADES_SCHEMA = pa.schema([
    ('trade_id', pa.int64()),
    ('price', pa.float64()),
    ('qty', pa.float64()),
    ('quote_qty', pa.float64()),
    ('timestamp', pa.int64()),  # ms since epoch
    ('is_buyer_maker', pa.bool_()),
])

# Default paths
TRADES_DATA_DIR = Path("TRADES-DATA")
PARQUET_DIR = Path("data/trades_parquet")


def csv_to_parquet(
    csv_path: Path,
    output_dir: Path = PARQUET_DIR,
    chunk_size: int = 1_000_000,
    exchange: str = "binance",
    symbol: str = "BTCUSDT"
) -> Path:
    """
    Convert a large trades CSV to Parquet format.
    
    Processes in chunks to handle multi-GB files without running out of memory.
    Returns the output Parquet file path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract month from filename (e.g., BTCUSDT-trades-2025-09.csv)
    stem = csv_path.stem  # BTCUSDT-trades-2025-09
    output_path = output_dir / f"{stem}.parquet"
    
    if output_path.exists():
        logger.info(f"Parquet file already exists: {output_path}")
        return output_path
    
    logger.info(f"Converting {csv_path} to Parquet (chunk_size={chunk_size:,})")
    
    # Process in chunks
    writer = None
    total_rows = 0
    
    try:
        for i, chunk in enumerate(pd.read_csv(
            csv_path,
            chunksize=chunk_size,
            dtype={
                'id': 'int64',
                'price': 'float64',
                'qty': 'float64',
                'quote_qty': 'float64',
                'time': 'int64',
                'is_buyer_maker': 'bool'
            }
        )):
            # Rename columns to match our schema
            chunk = chunk.rename(columns={
                'id': 'trade_id',
                'time': 'timestamp'
            })
            
            # Convert to PyArrow table
            table = pa.Table.from_pandas(chunk, schema=TRADES_SCHEMA, preserve_index=False)
            
            if writer is None:
                writer = pq.ParquetWriter(output_path, TRADES_SCHEMA, compression='snappy')
            
            writer.write_table(table)
            total_rows += len(chunk)
            
            if (i + 1) % 10 == 0:
                logger.info(f"  Processed {total_rows:,} rows...")
    
    finally:
        if writer:
            writer.close()
    
    logger.info(f"Converted {total_rows:,} rows to {output_path}")
    return output_path


def convert_all_csvs(
    input_dir: Path = TRADES_DATA_DIR,
    output_dir: Path = PARQUET_DIR
) -> list[Path]:
    """
    Find and convert all trade CSV files in the input directory.
    """
    parquet_files = []
    
    for csv_path in input_dir.rglob("*.csv"):
        if "trades" in csv_path.name.lower():
            parquet_path = csv_to_parquet(csv_path, output_dir)
            parquet_files.append(parquet_path)
    
    return parquet_files


class TradesDB:
    """
    Interface for querying trade data from Parquet files using DuckDB.
    
    Uses DuckDB's ability to query Parquet files directly without loading
    into tables, which is memory-efficient for large datasets.
    
    Performance optimizations:
    - Parallel query execution
    - Predicate pushdown to Parquet
    - Memory-efficient scanning
    """
    
    def __init__(self, parquet_dir: Path = PARQUET_DIR):
        self.parquet_dir = Path(parquet_dir)
        self.conn = duckdb.connect(":memory:")
        self._configure_performance()
        self._register_parquet_files()
    
    def _configure_performance(self):
        """Configure DuckDB for optimal performance."""
        # Enable parallel execution
        self.conn.execute("SET threads TO 4")
        # Use more memory for better query performance
        self.conn.execute("SET memory_limit = '2GB'")
        # Enable progress bar for long queries
        self.conn.execute("SET enable_progress_bar = false")
        # Optimize for analytical queries
        self.conn.execute("SET preserve_insertion_order = false")
        logger.info("DuckDB performance settings configured")
    
    def _register_parquet_files(self):
        """Create a view that unions all Parquet files."""
        parquet_files = list(self.parquet_dir.glob("*.parquet"))
        
        if not parquet_files:
            logger.warning(f"No Parquet files found in {self.parquet_dir}")
            return
        
        # Create a view over all Parquet files
        file_list = ", ".join(f"'{f}'" for f in parquet_files)
        self.conn.execute(f"""
            CREATE OR REPLACE VIEW trades AS
            SELECT * FROM read_parquet([{file_list}])
        """)
        
        logger.info(f"Registered {len(parquet_files)} Parquet files as 'trades' view")
    
    def get_trades_in_range(
        self,
        start_ts: int,
        end_ts: int,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Get trades within a timestamp range.
        
        Args:
            start_ts: Start timestamp (ms)
            end_ts: End timestamp (ms)
            limit: Optional row limit
        """
        query = """
            SELECT trade_id, price, qty, quote_qty, timestamp, is_buyer_maker
            FROM trades
            WHERE timestamp >= ? AND timestamp < ?
            ORDER BY timestamp
        """
        params = [start_ts, end_ts]
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        return self.conn.execute(query, params).df()
    
    def build_volume_profile(
        self,
        start_ts: int,
        end_ts: int,
        tick_size: float = 1.0,
        ticks_per_row: int = 10
    ) -> pd.DataFrame:
        """
        Build a volume profile for a time range.
        
        Aggregates trades into price bins with buy/sell volume split.
        
        Args:
            start_ts: Start timestamp (ms)
            end_ts: End timestamp (ms)
            tick_size: Minimum price increment (e.g., 0.1 for BTCUSDT futures)
            ticks_per_row: Number of ticks per price bin
            
        Returns:
            DataFrame with columns: price_bin, total_volume, buy_volume, sell_volume, delta, trade_count
        """
        bin_size = tick_size * ticks_per_row
        
        query = f"""
            SELECT 
                floor(price / {bin_size}) * {bin_size} AS price_bin,
                sum(qty) AS total_volume,
                sum(CASE WHEN NOT is_buyer_maker THEN qty ELSE 0 END) AS buy_volume,
                sum(CASE WHEN is_buyer_maker THEN qty ELSE 0 END) AS sell_volume,
                sum(CASE WHEN NOT is_buyer_maker THEN qty ELSE -qty END) AS delta,
                count(*) AS trade_count
            FROM trades
            WHERE timestamp >= ? AND timestamp < ?
            GROUP BY 1
            ORDER BY 1
        """
        
        return self.conn.execute(query, [start_ts, end_ts]).df()
    
    def build_candle_profiles(
        self,
        start_ts: int,
        end_ts: int,
        candle_ms: int = 300_000,  # 5 minutes
        tick_size: float = 1.0,
        ticks_per_row: int = 10
    ) -> dict:
        """
        Build volume profiles for each candle in a time range.
        
        Returns:
            Dict mapping candle_start_ts -> profile DataFrame
        """
        bin_size = tick_size * ticks_per_row
        
        query = f"""
            SELECT 
                floor(timestamp / {candle_ms}) * {candle_ms} AS candle_ts,
                floor(price / {bin_size}) * {bin_size} AS price_bin,
                sum(qty) AS total_volume,
                sum(CASE WHEN NOT is_buyer_maker THEN qty ELSE 0 END) AS buy_volume,
                sum(CASE WHEN is_buyer_maker THEN qty ELSE 0 END) AS sell_volume,
                sum(CASE WHEN NOT is_buyer_maker THEN qty ELSE -qty END) AS delta,
                count(*) AS trade_count
            FROM trades
            WHERE timestamp >= ? AND timestamp < ?
            GROUP BY 1, 2
            ORDER BY 1, 2
        """
        
        df = self.conn.execute(query, [start_ts, end_ts]).df()
        
        # Group by candle
        profiles = {}
        for candle_ts, group in df.groupby('candle_ts'):
            profiles[int(candle_ts)] = group.drop(columns=['candle_ts']).reset_index(drop=True)
        
        return profiles
    
    def build_candles_with_profiles(
        self,
        start_ts: int,
        end_ts: int,
        candle_ms: int = 300_000,
        tick_size: float = 1.0,
        ticks_per_row: int = 10
    ) -> list[dict]:
        """
        Build OHLCV candles with embedded volume profiles.
        
        Returns list of candles, each with:
        - timestamp, open, high, low, close, volume
        - profile: list of {price, total, buy, sell, delta}
        - poc: point of control (price with max volume)
        - vah, val: value area high/low (70% of volume)
        - total_delta: sum of all bin deltas
        """
        bin_size = tick_size * ticks_per_row
        
        # Build OHLCV from trades
        ohlcv_query = f"""
            SELECT 
                floor(timestamp / {candle_ms}) * {candle_ms} AS timestamp,
                first(price ORDER BY timestamp) AS open,
                max(price) AS high,
                min(price) AS low,
                last(price ORDER BY timestamp) AS close,
                sum(qty) AS volume,
                sum(CASE WHEN NOT is_buyer_maker THEN qty ELSE -qty END) AS total_delta
            FROM trades
            WHERE timestamp >= ? AND timestamp < ?
            GROUP BY 1
            ORDER BY 1
        """
        
        ohlcv_df = self.conn.execute(ohlcv_query, [start_ts, end_ts]).df()
        
        # Build profiles
        profiles = self.build_candle_profiles(
            start_ts, end_ts, candle_ms, tick_size, ticks_per_row
        )
        
        # Combine
        result = []
        for _, row in ohlcv_df.iterrows():
            ts = int(row['timestamp'])
            profile_df = profiles.get(ts, pd.DataFrame())
            
            candle = {
                'timestamp': ts,
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume'],
                'total_delta': row['total_delta'],
                'profile': [],
                'poc': None,
                'vah': None,
                'val': None
            }
            
            if not profile_df.empty:
                # Convert profile to list of dicts
                candle['profile'] = profile_df.to_dict('records')
                
                # Find POC (price with max total volume)
                poc_idx = profile_df['total_volume'].idxmax()
                candle['poc'] = profile_df.loc[poc_idx, 'price_bin']
                
                # Calculate Value Area (70% of volume)
                candle['vah'], candle['val'] = self._calculate_value_area(
                    profile_df, target_pct=0.70
                )
            
            result.append(candle)
        
        return result
    
    def _calculate_value_area(
        self,
        profile: pd.DataFrame,
        target_pct: float = 0.70
    ) -> tuple[float, float]:
        """
        Calculate Value Area High and Low.
        
        Starting from POC, expand up and down until target_pct of volume is covered.
        """
        if profile.empty:
            return None, None
        
        total_vol = profile['total_volume'].sum()
        target_vol = total_vol * target_pct
        
        # Start from POC
        poc_idx = profile['total_volume'].idxmax()
        prices = profile['price_bin'].values
        volumes = profile['total_volume'].values
        
        # Find POC position in sorted array
        sorted_indices = profile.sort_values('price_bin').index.tolist()
        poc_pos = sorted_indices.index(poc_idx)
        
        # Expand from POC
        included = {poc_pos}
        current_vol = volumes[sorted_indices[poc_pos]]
        
        up = poc_pos + 1
        down = poc_pos - 1
        
        while current_vol < target_vol and (up < len(sorted_indices) or down >= 0):
            vol_up = volumes[sorted_indices[up]] if up < len(sorted_indices) else 0
            vol_down = volumes[sorted_indices[down]] if down >= 0 else 0
            
            if vol_up >= vol_down and up < len(sorted_indices):
                included.add(up)
                current_vol += vol_up
                up += 1
            elif down >= 0:
                included.add(down)
                current_vol += vol_down
                down -= 1
            else:
                break
        
        included_prices = [prices[sorted_indices[i]] for i in included]
        return max(included_prices), min(included_prices)
    
    def get_stats(self) -> dict:
        """Get summary statistics about the trade data."""
        try:
            stats = self.conn.execute("""
                SELECT 
                    count(*) AS total_trades,
                    min(timestamp) AS first_trade_ts,
                    max(timestamp) AS last_trade_ts,
                    min(price) AS min_price,
                    max(price) AS max_price,
                    sum(qty) AS total_volume
                FROM trades
            """).df().iloc[0].to_dict()
            
            # Convert timestamps to dates
            if stats['first_trade_ts']:
                stats['first_trade_date'] = datetime.fromtimestamp(
                    stats['first_trade_ts'] / 1000, tz=timezone.utc
                ).isoformat()
            if stats['last_trade_ts']:
                stats['last_trade_date'] = datetime.fromtimestamp(
                    stats['last_trade_ts'] / 1000, tz=timezone.utc
                ).isoformat()
            
            return stats
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}
    
    def close(self):
        self.conn.close()


# CLI for processing
if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    if len(sys.argv) > 1 and sys.argv[1] == "convert":
        # Convert all CSVs to Parquet
        print("Converting CSV files to Parquet...")
        files = convert_all_csvs()
        print(f"Converted {len(files)} files")
        
        # Test loading
        print("\nTesting TradesDB...")
        db = TradesDB()
        stats = db.get_stats()
        print(f"Stats: {stats}")
        db.close()
    else:
        print("Usage: python -m app.ingestion.trades convert")
