import requests
import zipfile
import io
import pandas as pd
import logging
from datetime import datetime, timedelta
from app.db import db

logger = logging.getLogger(__name__)

BASE_URL = "https://data.binance.vision/data/futures/um/monthly/trades"

def download_monthly_trades(symbol: str, year: int, month: int) -> pd.DataFrame:
    """
    Download monthly trades ZIP from Binance Vision, parse CSV, and return DataFrame.
    """
    month_str = f"{month:02d}"
    file_name = f"{symbol}-trades-{year}-{month_str}"
    url = f"{BASE_URL}/{symbol}/{file_name}.zip"
    
    logger.info(f"Downloading {url}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        logger.error(f"Failed to download {url}: Status {response.status_code}")
        return pd.DataFrame()
        
    logger.info("Download complete. Extracting and parsing...")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        with z.open(f"{file_name}.csv") as f:
            # Binance Trades CSV columns: id, price, qty, quote_qty, time, is_buyer_maker
            # We only need: time, price, qty, is_buyer_maker
            df = pd.read_csv(
                f, 
                header=None, 
                names=["id", "price", "qty", "quote_qty", "time", "is_buyer_maker"],
                usecols=["time", "price", "qty", "is_buyer_maker"]
            )
            
    return df

def load_trades_to_db(symbol: str, year: int, month: int):
    """
    Download, parse, and insert trades into DuckDB.
    """
    df = download_monthly_trades(symbol, year, month)
    if df.empty:
        logger.warning("No data found.")
        return

    logger.info(f"Inserting {len(df)} trades into DuckDB...")
    
    # Add metadata columns
    df["exchange"] = "binance"
    df["symbol"] = symbol
    
    # Rename columns to match DB schema if needed (DB expects: timestamp, price, qty, is_buyer_maker)
    df = df.rename(columns={"time": "timestamp"})
    
    # Insert
    try:
        db.conn.register('temp_trades', df)
        db.conn.execute("""
            INSERT OR IGNORE INTO trades (exchange, symbol, timestamp, price, qty, is_buyer_maker)
            SELECT exchange, symbol, timestamp, price, qty, is_buyer_maker FROM temp_trades
        """)
        db.conn.unregister('temp_trades')
        logger.info("Insertion complete.")
    except Exception as e:
        logger.error(f"Failed to insert trades: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Default to downloading last month's data for BTCUSDT
    # For testing, let's pick a specific month known to have data, e.g., 2024-01
    load_trades_to_db("BTCUSDT", 2024, 1)
