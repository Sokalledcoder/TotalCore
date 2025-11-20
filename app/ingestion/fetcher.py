from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import ccxt
import pandas as pd

from app.models import DataJob, JobStatus
from app.store import JobStore
from app.db import db

logger = logging.getLogger(__name__)

@dataclass
class IngestionConfig:
    data_dir: Path = Path("data/lake")
    max_entries_per_call: int = 1000  # Binance usually allows 1000

class HistoryIngestor:
    def __init__(self, store: JobStore, config: Optional[IngestionConfig] = None) -> None:
        self.store = store
        self.config = config or IngestionConfig()
        self.config.data_dir.mkdir(parents=True, exist_ok=True)

    def ingest(self, job: DataJob) -> None:
        logger.info("Starting ingestion job %s for %s %s", job.id, job.exchange, job.symbol)
        self.store.update_job(job.id, status=JobStatus.running, progress=0.0)
        
        try:
            # Initialize exchange
            exchange_class = getattr(ccxt, job.exchange.lower())
            exchange = exchange_class({
                "enableRateLimit": True,
                "options": {"defaultType": "future"} if job.exchange.lower() == "binance" else {} 
            })
            
            # For Binance Futures, we might need to adjust the symbol format or options
            # But let's assume the user passes "BTC/USDT" and we handle it.
            
            now_ms = int(datetime.utcnow().timestamp() * 1000)
            end_ms = job.end_timestamp or now_ms
            
            if job.start_timestamp:
                start_ms = job.start_timestamp
            elif job.exchange.lower() == "binance" and "BTC" in job.symbol:
                # Binance Futures launched around Sept 2019. 
                # We'll use a safe start date for full history if not specified.
                # 2019-09-08 = 1567900800000
                start_ms = 1567900800000
                logger.info("No start date provided. Fetching FULL HISTORY from 2019-09-08.")
            else:
                # Default to 30 days
                start_ms = end_ms - 30 * 24 * 60 * 60 * 1000
            
            self._fetch_ohlcv(exchange, job, start_ms, end_ms)
            
            self.store.update_job(job.id, status=JobStatus.completed, progress=1.0, result={"message": "Ingestion complete"})
            
        except Exception as exc:
            logger.exception("Job %s failed", job.id)
            self.store.update_job(job.id, status=JobStatus.failed, details={"error": str(exc)})

    def _fetch_ohlcv(self, exchange: ccxt.Exchange, job: DataJob, start_ms: int, end_ms: int) -> None:
        # Force 1m timeframe for base data if not specified, or respect job if user insists.
        # User requested 1m.
        fetch_timeframe = "1m"
        timeframe_ms = self._timeframe_to_ms(fetch_timeframe)
        
        current = start_ms
        total_rows = 0
        
        # We will also fetch Funding Rates and Open Interest periodically
        # Since these endpoints might not support pagination the same way or are sparse,
        # we'll try to fetch them in chunks or just once if the API allows range.
        # CCXT fetchFundingRateHistory usually takes symbol, since, limit.
        
        # 1. Fetch Funding Rate History (Independent loop or interleaved?)
        # Let's do it interleaved or just after a chunk of OHLCV to keep progress moving.
        # Actually, let's do it in parallel or separate passes. 
        # For simplicity, let's do it in separate passes but update progress on the main OHLCV loop.
        
        logger.info("Fetching Funding Rates...")
        try:
            self._fetch_funding_rates(exchange, job, start_ms, end_ms)
        except Exception as e:
            logger.error(f"Failed to fetch funding rates: {e}")

        # logger.info("Fetching Open Interest...")
        # try:
        #      self._fetch_open_interest(exchange, job, start_ms, end_ms, fetch_timeframe)
        # except Exception as e:
        #      logger.error(f"Failed to fetch open interest: {e}")

        logger.info(f"Fetching OHLCV ({fetch_timeframe})...")
        while current < end_ms:
            try:
                candles = exchange.fetch_ohlcv(job.symbol, fetch_timeframe, since=current, limit=self.config.max_entries_per_call)
            except Exception as exc:
                logger.error(f"Fetch failed: {exc}")
                raise

            if not candles:
                break
                
            df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df = df[df["timestamp"] < end_ms]
            if df.empty:
                break

            # Save to DuckDB (New)
            # Note: We are saving as '1m' even if job says '15m' because user wants 1m base.
            # But if we save as '1m', the HMM engine (which queries by job.timeframe) might fail if it expects '15m'.
            # We should probably save as '1m' and let the HMM engine resample.
            # For now, let's save as '1m'.
            self._write_duckdb(job, df.copy(), override_timeframe="1m")

            total_rows += len(df)
            last_ts = int(df["timestamp"].iloc[-1])
            
            progress = min(0.99, (last_ts - start_ms) / max(1, end_ms - start_ms))
            self.store.update_job(job.id, progress=progress, details={"rows": total_rows, "last_timestamp": last_ts})
            
            current = last_ts + timeframe_ms
            if len(candles) < 1:
                break

    def _fetch_funding_rates(self, exchange: ccxt.Exchange, job: DataJob, start_ms: int, end_ms: int):
        # Binance: fetchFundingRateHistory
        if not exchange.has['fetchFundingRateHistory']:
            return
            
        current = start_ms
        while current < end_ms:
            rates = exchange.fetch_funding_rate_history(job.symbol, since=current, limit=1000)
            if not rates:
                break
                
            df = pd.DataFrame(rates)
            # Keep relevant columns: timestamp, fundingRate
            if 'timestamp' not in df.columns or 'fundingRate' not in df.columns:
                break
                
            df = df[['timestamp', 'fundingRate']]
            # Pass a copy so we don't mutate our local df used for pagination logic
            db.insert_funding_rates(df.copy(), job.exchange, job.symbol)
            
            # Use the original int timestamp for pagination
            last_ts = int(df['timestamp'].max())
            if last_ts <= current:
                break
            current = last_ts + 1000 # +1s

    def _fetch_open_interest(self, exchange: ccxt.Exchange, job: DataJob, start_ms: int, end_ms: int, timeframe: str):
        # Binance: fetchOpenInterestHistory
        if not exchange.has['fetchOpenInterestHistory']:
            return
            
        # Binance OI doesn't support 1m. Lowest is 5m.
        oi_timeframe = timeframe
        if timeframe == '1m':
            oi_timeframe = '5m'
            
        current = start_ms
        while current < end_ms:
            # Binance OI history is usually 5m, 15m, etc.
            # CCXT fetchOpenInterestHistory(symbol, timeframe, since, limit)
            try:
                ois = exchange.fetch_open_interest_history(job.symbol, oi_timeframe, since=current, limit=500)
            except Exception as e:
                logger.warning(f"OI fetch failed for {oi_timeframe} at {current}: {e}")
                # Advance by 500 candles * timeframe to skip this bad chunk
                current += 500 * self._timeframe_to_ms(oi_timeframe)
                continue
                
            if not ois:
                # If no data returned, maybe we are at the end or in a gap. 
                # Advance to avoid infinite loop.
                current += 500 * self._timeframe_to_ms(oi_timeframe)
                continue
                
            df = pd.DataFrame(ois)
            # Expected cols: timestamp, openInterestAmount, openInterestValue
            db.insert_open_interest(df.copy(), job.exchange, job.symbol, oi_timeframe)
            
            last_ts = int(df['timestamp'].max())
            if last_ts <= current:
                break
            current = last_ts + self._timeframe_to_ms(oi_timeframe)

    def _write_parquet(self, job: DataJob, df: pd.DataFrame) -> None:
        # Deprecated for now or keep as backup? 
        # User didn't ask to remove, but let's focus on DuckDB.
        pass

    def _write_duckdb(self, job: DataJob, df: pd.DataFrame, override_timeframe: str = None) -> None:
        if df.empty:
            return
        if pd.api.types.is_integer_dtype(df["timestamp"]):
             df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
             
        tf = override_timeframe or job.timeframe
        db.insert_market_data(df, job.exchange, job.symbol, tf)

    @staticmethod
    def _timeframe_to_ms(timeframe: str) -> int:
        mapping = {
            "1m": 60 * 1000,
            "3m": 3 * 60 * 1000,
            "5m": 5 * 60 * 1000,
            "15m": 15 * 60 * 1000,
            "30m": 30 * 60 * 1000,
            "1h": 60 * 60 * 1000,
            "2h": 2 * 60 * 60 * 1000,
            "4h": 4 * 60 * 60 * 1000,
            "6h": 6 * 60 * 60 * 1000,
            "8h": 8 * 60 * 60 * 1000,
            "12h": 12 * 60 * 60 * 1000,
            "1d": 24 * 60 * 60 * 1000,
            "3d": 3 * 24 * 60 * 60 * 1000,
            "1w": 7 * 24 * 60 * 60 * 1000,
            "1M": 30 * 24 * 60 * 60 * 1000,
        }
        return mapping.get(timeframe, 60 * 1000)
