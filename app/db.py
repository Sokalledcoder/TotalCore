import duckdb
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = "tradecore.duckdb"

# Supported output timeframes derived from 1m base data
TIMEFRAME_BUCKET_MS = {
    "1m": 60_000,
    "5m": 5 * 60_000,
    "13m": 13 * 60_000,
    "15m": 15 * 60_000,
    "30m": 30 * 60_000,
    "1h": 60 * 60_000,
    "4h": 4 * 60 * 60_000,
    "1d": 24 * 60 * 60_000,
}

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = duckdb.connect(self.db_path)
        self._init_schema()

    def _init_schema(self):
        """Initialize the database schema if it doesn't exist."""
        try:
            # Market Data Table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    exchange VARCHAR,
                    symbol VARCHAR,
                    timeframe VARCHAR,
                    timestamp TIMESTAMP,
                    open DOUBLE,
                    high DOUBLE,
                    low DOUBLE,
                    close DOUBLE,
                    volume DOUBLE,
                    PRIMARY KEY (exchange, symbol, timeframe, timestamp)
                );
            """)

            # HMM Results Table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS hmm_results (
                    exchange VARCHAR,
                    symbol VARCHAR,
                    timeframe VARCHAR,
                    timestamp TIMESTAMP,
                    regime INTEGER,
                    prob_0 DOUBLE,
                    prob_1 DOUBLE,
                    prob_2 DOUBLE,
                    prob_3 DOUBLE,
                    prob_4 DOUBLE,
                    model_id VARCHAR,
                    PRIMARY KEY (exchange, symbol, timeframe, timestamp, model_id)
                );
            """)

            # Ensure backward compatibility if table existed before prob_4 was added
            self.conn.execute("""
                ALTER TABLE hmm_results ADD COLUMN IF NOT EXISTS prob_4 DOUBLE;
            """)

            # Funding Rates Table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS funding_rates (
                    exchange VARCHAR,
                    symbol VARCHAR,
                    timestamp TIMESTAMP,
                    funding_rate DOUBLE,
                    PRIMARY KEY (exchange, symbol, timestamp)
                );
            """)

            # Open Interest Table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS open_interest (
                    exchange VARCHAR,
                    symbol VARCHAR,
                    timeframe VARCHAR,
                    timestamp TIMESTAMP,
                    open_interest DOUBLE,
                    open_interest_value DOUBLE,
                    PRIMARY KEY (exchange, symbol, timeframe, timestamp)
                );
            """)
            
            logger.info("Database schema initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize schema: {e}")
            raise

    def insert_market_data(self, df: pd.DataFrame, exchange: str, symbol: str, timeframe: str):
        """
        Insert market data from a DataFrame.
        Expected DF columns: timestamp (datetime), open, high, low, close, volume
        """
        try:
            # Add metadata columns if they don't exist
            df['exchange'] = exchange
            df['symbol'] = symbol
            df['timeframe'] = timeframe
            
            # Ensure correct column order for insert
            # DuckDB is smart, but explicit is better
            insert_df = df[['exchange', 'symbol', 'timeframe', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
            # Register the dataframe as a virtual table
            self.conn.register('temp_market_data', insert_df)
            
            # Insert or Ignore (to handle duplicates)
            self.conn.execute("""
                INSERT OR IGNORE INTO market_data 
                SELECT * FROM temp_market_data
            """)
            
            self.conn.unregister('temp_market_data')
            logger.info(f"Inserted {len(df)} rows for {exchange} {symbol} {timeframe}")
        except Exception as e:
            logger.error(f"Failed to insert market data: {e}")
            raise

    def insert_funding_rates(self, df: pd.DataFrame, exchange: str, symbol: str):
        try:
            df['exchange'] = exchange
            df['symbol'] = symbol
            # Ensure timestamp is datetime
            if pd.api.types.is_integer_dtype(df["timestamp"]):
                 df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            
            insert_df = df[['exchange', 'symbol', 'timestamp', 'fundingRate']]
            self.conn.register('temp_funding', insert_df)
            self.conn.execute("INSERT OR IGNORE INTO funding_rates SELECT * FROM temp_funding")
            self.conn.unregister('temp_funding')
        except Exception as e:
            logger.error(f"Failed to insert funding rates: {e}")

    def insert_open_interest(self, df: pd.DataFrame, exchange: str, symbol: str, timeframe: str):
        try:
            df['exchange'] = exchange
            df['symbol'] = symbol
            df['timeframe'] = timeframe
            if pd.api.types.is_integer_dtype(df["timestamp"]):
                 df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            
            # CCXT usually returns 'openInterestAmount' and 'openInterestValue'
            # Map them to our schema
            if 'openInterestAmount' in df.columns:
                df['open_interest'] = df['openInterestAmount']
            if 'openInterestValue' in df.columns:
                df['open_interest_value'] = df['openInterestValue']
                
            insert_df = df[['exchange', 'symbol', 'timeframe', 'timestamp', 'open_interest', 'open_interest_value']]
            self.conn.register('temp_oi', insert_df)
            self.conn.execute("INSERT OR IGNORE INTO open_interest SELECT * FROM temp_oi")
            self.conn.unregister('temp_oi')
        except Exception as e:
            logger.error(f"Failed to insert open interest: {e}")

    def insert_hmm_results(self, df: pd.DataFrame, model_id: str, exchange: str, symbol: str, timeframe: str):
        """Persist HMM probabilities/labels for a given model_id."""
        if df.empty:
            return
        try:
            df = df.copy()
            df['model_id'] = model_id
            df['exchange'] = exchange
            df['symbol'] = symbol
            df['timeframe'] = timeframe

            # Ensure fixed columns exist; fill missing prob columns with nulls
            for col in ["prob_0", "prob_1", "prob_2", "prob_3", "prob_4"]:
                if col not in df.columns:
                    df[col] = None

            insert_cols = [
                'exchange', 'symbol', 'timeframe', 'timestamp', 'regime',
                'prob_0', 'prob_1', 'prob_2', 'prob_3', 'prob_4', 'model_id'
            ]

            self.conn.register('temp_hmm_results', df[insert_cols])
            self.conn.execute("""
                INSERT OR REPLACE INTO hmm_results
                SELECT * FROM temp_hmm_results
            """)
            self.conn.unregister('temp_hmm_results')
        except Exception as e:
            logger.error(f"Failed to insert hmm_results: {e}")

    def delete_hmm_results_by_model(self, model_id: str):
        try:
            self.conn.execute("DELETE FROM hmm_results WHERE model_id = ?", (model_id,))
        except Exception as e:
            logger.error(f"Failed to delete hmm_results for {model_id}: {e}")

    def delete_hmm_results_by_prefix(self, prefix: str):
        try:
            self.conn.execute("DELETE FROM hmm_results WHERE model_id LIKE ?", (f"{prefix}%",))
        except Exception as e:
            logger.error(f"Failed to delete hmm_results for prefix {prefix}: {e}")

    def get_hmm_results(self, exchange: str, symbol: str, timeframe: str, model_id: str, limit: int = 500, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        query = """
            SELECT timestamp, regime, prob_0, prob_1, prob_2, prob_3, prob_4
            FROM hmm_results
            WHERE exchange = ? AND symbol = ? AND timeframe = ? AND model_id = ?
        """
        params = [exchange, symbol, timeframe, model_id]
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        df = self.conn.execute(query, params).df()
        return df.iloc[::-1] if not df.empty else df

    def get_market_data(self, exchange: str, symbol: str, timeframe: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Fetch market data at requested timeframe, aggregating from 1m base if needed."""

        base_tf = "1m"
        if timeframe not in TIMEFRAME_BUCKET_MS:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        # If requesting raw 1m, read directly
        if timeframe == base_tf:
            query = """
                SELECT timestamp, open, high, low, close, volume
                FROM market_data
                WHERE exchange = ? AND symbol = ? AND timeframe = ?
            """
            params = [exchange, symbol, base_tf]
            if start_date:
                query += " AND timestamp >= ?"
                params.append(start_date)
            if end_date:
                query += " AND timestamp <= ?"
                params.append(end_date)
            query += " ORDER BY timestamp ASC"
            return self.conn.execute(query, params).df()

        bucket_ms = TIMEFRAME_BUCKET_MS[timeframe]

        # Aggregate from 1m base data using epoch bucketing
        query = """
            WITH base AS (
                SELECT timestamp, open, high, low, close, volume
                FROM market_data
                WHERE exchange = ? AND symbol = ? AND timeframe = ?
            )
            SELECT 
                to_timestamp(floor(epoch(timestamp) * 1000 / ?) * ? / 1000.0) AS timestamp,
                first(open ORDER BY timestamp) AS open,
                max(high) AS high,
                min(low) AS low,
                last(close ORDER BY timestamp) AS close,
                sum(volume) AS volume
            FROM base
            WHERE 1=1
        """
        params = [exchange, symbol, base_tf, bucket_ms, bucket_ms]

        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        query += " GROUP BY 1 ORDER BY 1 ASC"

        return self.conn.execute(query, params).df()

    def get_market_data_for_timestamps(self, exchange: str, symbol: str, timeframe: str, timestamps: list) -> pd.DataFrame:
        if not timestamps:
            return pd.DataFrame()
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM market_data
            WHERE exchange = ? AND symbol = ? AND timeframe = ? AND timestamp IN (%s)
            ORDER BY timestamp ASC
        """
        placeholders = ",".join(["?"] * len(timestamps))
        query = query % placeholders
        params = [exchange, symbol, timeframe] + timestamps
        return self.conn.execute(query, params).df()

    def get_recent_market_data(self, exchange: str, symbol: str, timeframe: str, limit: int = 400) -> pd.DataFrame:
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM market_data
            WHERE exchange=? AND symbol=? AND timeframe=?
            ORDER BY timestamp DESC
            LIMIT ?
        """
        df = self.conn.execute(query, [exchange, symbol, timeframe, limit]).df()
        return df.iloc[::-1] if not df.empty else df

    def close(self):
        self.conn.close()

# Global instance
db = Database()
