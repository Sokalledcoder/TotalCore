"""
Bybit Trade data processing pipeline for footprint/volume profile analysis.

Handles:
- CSV.gz extraction and Parquet conversion
- Loading into DuckDB
- Aggregation into volume profiles per candle

Bybit CSV format:
- timestamp: seconds with decimal (e.g., 1764288000.3181)
- symbol: e.g., BTCUSDT
- side: Buy/Sell
- size: BTC amount
- price: trade price
- tickDirection: ZeroPlusTick, MinusTick, etc.
- trdMatchID: unique trade ID
- grossValue: value in base units
- homeNotional: BTC amount
- foreignNotional: USD value
- RPI: (unused)
"""

from __future__ import annotations

import gzip
import logging
from pathlib import Path
from typing import Optional, Iterator, List, Dict, Any

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb

logger = logging.getLogger(__name__)

# Schema for Bybit trades (normalized to match Binance format)
BYBIT_TRADES_SCHEMA = pa.schema([
    ('trade_id', pa.string()),  # Bybit uses UUID strings
    ('price', pa.float64()),
    ('qty', pa.float64()),
    ('quote_qty', pa.float64()),
    ('timestamp', pa.int64()),  # ms since epoch
    ('is_buyer_maker', pa.bool_()),
    ('exchange', pa.string()),
])

# Paths
BYBIT_DATA_DIR = Path("TRADES-DATA/BTC-USDT-TRADES-BYBIT-FUTURES")
BYBIT_PARQUET_DIR = Path("data/bybit_trades_parquet")


def extract_and_convert_bybit_trades(
    csv_gz_path: Path,
    output_dir: Path = BYBIT_PARQUET_DIR,
    chunk_size: int = 500_000,
) -> Path:
    """
    Extract a Bybit CSV.gz file and convert to Parquet format.
    
    Processes in chunks to handle large files efficiently.
    Returns the output Parquet file path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Output filename based on input
    stem = csv_gz_path.stem.replace('.csv', '')  # BTCUSDT2025-11-28
    output_path = output_dir / f"{stem}.parquet"
    
    if output_path.exists():
        logger.info(f"Parquet file already exists: {output_path}")
        return output_path
    
    logger.info(f"Extracting and converting {csv_gz_path} to Parquet")
    
    writer = None
    total_rows = 0
    
    try:
        # Read gzipped CSV in chunks
        for i, chunk in enumerate(pd.read_csv(
            csv_gz_path,
            compression='gzip',
            chunksize=chunk_size,
            dtype={
                'timestamp': 'float64',
                'symbol': 'str',
                'side': 'str',
                'size': 'float64',
                'price': 'float64',
                'tickDirection': 'str',
                'trdMatchID': 'str',
                'grossValue': 'float64',
                'homeNotional': 'float64',
                'foreignNotional': 'float64',
            },
            on_bad_lines='skip'
        )):
            # Transform to normalized schema
            df = pd.DataFrame({
                'trade_id': chunk['trdMatchID'],
                'price': chunk['price'],
                'qty': chunk['size'],
                'quote_qty': chunk['foreignNotional'],  # USD value
                'timestamp': (chunk['timestamp'] * 1000).astype('int64'),  # Convert to ms
                'is_buyer_maker': chunk['side'] == 'Sell',  # Seller is maker when side=Sell
                'exchange': 'bybit',
            })
            
            # Convert to PyArrow table
            table = pa.Table.from_pandas(df, schema=BYBIT_TRADES_SCHEMA, preserve_index=False)
            
            if writer is None:
                writer = pq.ParquetWriter(output_path, BYBIT_TRADES_SCHEMA, compression='snappy')
            
            writer.write_table(table)
            total_rows += len(df)
            
            if (i + 1) % 5 == 0:
                logger.info(f"  Processed {total_rows:,} rows...")
    
    finally:
        if writer:
            writer.close()
    
    logger.info(f"Converted {total_rows:,} rows to {output_path}")
    return output_path


def convert_all_bybit_trades(data_dir: Path = BYBIT_DATA_DIR) -> List[Path]:
    """Convert all Bybit CSV.gz files in the directory to Parquet."""
    parquet_files = []
    
    for csv_gz in sorted(data_dir.glob("*.csv.gz")):
        output = extract_and_convert_bybit_trades(csv_gz)
        parquet_files.append(output)
    
    return parquet_files


class BybitTradesDB:
    """
    Query interface for Bybit trade data stored in Parquet format.
    Uses DuckDB for efficient analytical queries.
    """
    
    def __init__(self, parquet_dir: Path = BYBIT_PARQUET_DIR):
        self.parquet_dir = parquet_dir
        self.conn = duckdb.connect()
        self._register_parquet_files()
    
    def _register_parquet_files(self) -> None:
        """Register all Parquet files as a unified 'trades' view."""
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
            CREATE OR REPLACE VIEW trades AS 
            SELECT * FROM read_parquet('{files_pattern}')
        """)
        
        logger.info(f"Registered {len(parquet_files)} Bybit Parquet files")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get basic statistics about the loaded trades."""
        try:
            result = self.conn.execute("""
                SELECT 
                    COUNT(*) as total_trades,
                    MIN(timestamp) as min_ts,
                    MAX(timestamp) as max_ts,
                    SUM(qty) as total_volume,
                    SUM(quote_qty) as total_quote_volume,
                    MIN(price) as min_price,
                    MAX(price) as max_price
                FROM trades
            """).fetchone()
            
            if result:
                from datetime import datetime, timezone
                min_ts = result[1]
                max_ts = result[2]
                
                return {
                    "total_trades": result[0],
                    "min_timestamp": min_ts,
                    "max_timestamp": max_ts,
                    "last_trade_ts": max_ts,  # For footprint API compatibility
                    "total_volume": result[3],
                    "total_volume_btc": result[3],
                    "total_volume_usd": result[4],
                    "min_price": result[5],
                    "max_price": result[6],
                    "first_trade_date": datetime.fromtimestamp(min_ts/1000, tz=timezone.utc).isoformat() if min_ts else "",
                    "last_trade_date": datetime.fromtimestamp(max_ts/1000, tz=timezone.utc).isoformat() if max_ts else "",
                    "exchange": "bybit"
                }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
        
        return {"total_trades": 0, "exchange": "bybit"}
    
    def build_candles_with_profiles(
        self,
        start_ts: int,
        end_ts: int,
        candle_ms: int = 60000,
        tick_size: float = 1.0,
        ticks_per_row: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Build OHLCV candles with embedded volume profiles.
        
        Compatible with TradesDB interface for footprint API.
        
        Args:
            start_ts: Start timestamp in milliseconds
            end_ts: End timestamp in milliseconds
            candle_ms: Candle size in milliseconds
            tick_size: Price tick size
            ticks_per_row: Ticks per row for binning
        
        Returns:
            List of candles with volume profiles
        """
        bin_size = tick_size * ticks_per_row
        
        # Build OHLCV from trades
        # Use FLOOR() for proper integer division with large timestamps
        ohlcv_query = f"""
            SELECT 
                CAST(FLOOR(timestamp / {candle_ms}) * {candle_ms} AS BIGINT) AS timestamp,
                FIRST(price ORDER BY timestamp) AS open,
                MAX(price) AS high,
                MIN(price) AS low,
                LAST(price ORDER BY timestamp) AS close,
                SUM(qty) AS volume,
                SUM(CASE WHEN NOT is_buyer_maker THEN qty ELSE -qty END) AS total_delta
            FROM trades
            WHERE timestamp >= {start_ts} AND timestamp < {end_ts}
            GROUP BY 1
            ORDER BY 1
        """
        
        # Build profiles in a single query
        profile_query = f"""
            SELECT 
                CAST(FLOOR(timestamp / {candle_ms}) * {candle_ms} AS BIGINT) AS candle_ts,
                FLOOR(price / {bin_size}) * {bin_size} AS price_bin,
                SUM(qty) AS total_volume,
                SUM(CASE WHEN NOT is_buyer_maker THEN qty ELSE 0 END) AS buy_volume,
                SUM(CASE WHEN is_buyer_maker THEN qty ELSE 0 END) AS sell_volume,
                SUM(CASE WHEN NOT is_buyer_maker THEN qty ELSE -qty END) AS delta,
                COUNT(*) AS trade_count
            FROM trades
            WHERE timestamp >= {start_ts} AND timestamp < {end_ts}
            GROUP BY 1, 2
            ORDER BY 1, 2
        """
        
        # Fetch OHLCV
        ohlcv_rows = self.conn.execute(ohlcv_query).fetchall()
        
        # Fetch all profiles at once and group by candle
        profiles_by_candle: Dict[int, List[Dict]] = {}
        for row in self.conn.execute(profile_query).fetchall():
            candle_ts = int(row[0])
            if candle_ts not in profiles_by_candle:
                profiles_by_candle[candle_ts] = []
            profiles_by_candle[candle_ts].append({
                'price_bin': row[1],
                'total_volume': row[2],
                'buy_volume': row[3],
                'sell_volume': row[4],
                'delta': row[5],
                'trade_count': row[6]
            })
        
        # Build result
        result = []
        for row in ohlcv_rows:
            ts = int(row[0])
            profile = profiles_by_candle.get(ts, [])
            
            # Find POC (price with max volume)
            poc = None
            vah = None
            val = None
            
            if profile:
                max_vol = 0
                total_vol = 0
                for p in profile:
                    if p['total_volume'] > max_vol:
                        max_vol = p['total_volume']
                        poc = p['price_bin']
                    total_vol += p['total_volume']
                
                # Calculate VAH/VAL (70% of volume)
                if total_vol > 0:
                    target_vol = total_vol * 0.70
                    cum_vol = 0
                    val_set = False
                    for p in sorted(profile, key=lambda x: x['total_volume'], reverse=True):
                        cum_vol += p['total_volume']
                        if not val_set:
                            val = p['price_bin']
                            vah = p['price_bin']
                            val_set = True
                        else:
                            val = min(val, p['price_bin'])
                            vah = max(vah, p['price_bin'])
                        if cum_vol >= target_vol:
                            break
            
            result.append({
                'timestamp': ts,
                'open': row[1],
                'high': row[2],
                'low': row[3],
                'close': row[4],
                'volume': row[5],
                'total_delta': row[6],
                'profile': profile,
                'poc': poc,
                'vah': vah,
                'val': val
            })
        
        return result
    
    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()


# CLI for testing
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1 and sys.argv[1] == "convert":
        # Convert all CSV.gz files
        files = convert_all_bybit_trades()
        print(f"Converted {len(files)} files")
    else:
        # Show stats
        db = BybitTradesDB()
        stats = db.get_stats()
        print("Bybit Trades Stats:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
        db.close()
