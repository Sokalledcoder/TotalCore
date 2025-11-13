from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import ccxt
import pandas as pd

from app.ingestion.trade_aggregator import KrakenTradeAggregator
from app.models import DataJob, JobStatus
from app.store import JobStore

logger = logging.getLogger(__name__)


@dataclass
class KrakenIngestionConfig:
    data_dir: Path = Path("data/lake")
    max_entries_per_call: int = 720  # Kraken OHLC cap


class KrakenHistoryIngestor:
    def __init__(self, store: JobStore, config: Optional[KrakenIngestionConfig] = None) -> None:
        self.store = store
        self.config = config or KrakenIngestionConfig()
        self.config.data_dir.mkdir(parents=True, exist_ok=True)
        self.trade_aggregator = KrakenTradeAggregator()

    def ingest(self, job: DataJob) -> None:
        logger.info("Starting ingestion job %s", job.id)
        self.store.update_job(job.id, status=JobStatus.running, progress=0.0)
        try:
            now_ms = int(datetime.utcnow().timestamp() * 1000)
            end_ms = job.end_timestamp or now_ms
            start_ms = job.start_timestamp or (end_ms - 30 * 24 * 60 * 60 * 1000)
            if start_ms >= end_ms:
                start_ms = end_ms - self._timeframe_to_ms(job.timeframe) * 10

            self._run_trade_backfill(job, start_ms, end_ms)
            self._fetch_rest(job, max(start_ms, end_ms - self.config.max_entries_per_call * self._timeframe_to_ms(job.timeframe)), end_ms)

            self.store.update_job(job.id, status=JobStatus.completed, progress=1.0, result={"message": "Ingestion complete"})
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Job %s failed", job.id)
            self.store.update_job(job.id, status=JobStatus.failed, details={"error": str(exc)})

    def _run_trade_backfill(self, job: DataJob, start_ms: int, end_ms: int) -> None:
        progress_span = max(1, end_ms - start_ms)
        total_rows = 0
        last_ts = start_ms

        def checkpoint(cursor: int) -> None:
            self.store.update_job(job.id, details={"cursor": cursor, "aggregated_rows": total_rows})

        for df in self.trade_aggregator.aggregate(job.symbol, job.timeframe, start_ms, end_ms, checkpoint=checkpoint):
            if df.empty:
                continue
            last_ts = int(df["timestamp"].max()) if "timestamp" in df.columns else last_ts
            self._write_parquet(job, df.copy())
            total_rows += int(df.shape[0])
            progress = min(0.9, (last_ts - start_ms) / progress_span)
            self.store.update_job(
                job.id,
                progress=progress,
                details={"aggregated_rows": total_rows, "last_timestamp": last_ts},
            )

        if total_rows == 0:
            logger.warning("Trade backfill yielded no rows for %s", job.symbol)

    def _fetch_rest(self, job: DataJob, start_ms: int, end_ms: int) -> None:
        exchange = ccxt.kraken({"enableRateLimit": True})
        exchange.load_markets()
        timeframe_ms = self._timeframe_to_ms(job.timeframe)
        current = start_ms
        total_rows = 0
        while current < end_ms:
            try:
                candles = exchange.fetch_ohlcv(job.symbol, job.timeframe, since=current, limit=self.config.max_entries_per_call)
            except Exception as exc:  # pylint: disable=broad-except
                self.store.update_job(job.id, details={"error": str(exc)})
                raise
            if not candles:
                break
            df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
            self._write_parquet(job, df)
            total_rows += len(df)
            last_ts = int(candles[-1][0])
            current = last_ts + timeframe_ms
            progress = min(0.99, (current - start_ms) / max(1, end_ms - start_ms))
            self.store.update_job(job.id, progress=progress, details={"rest_rows": total_rows, "last_timestamp": last_ts})
            if len(df) < self.config.max_entries_per_call:
                break

    def _write_parquet(self, job: DataJob, df: pd.DataFrame) -> None:
        if df.empty:
            return
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)
        year_groups = df.groupby(df.index.year)
        for year, chunk in year_groups:
            target_dir = self.config.data_dir / job.exchange / job.symbol.replace("/", "-") / job.timeframe / f"year={year}"
            target_dir.mkdir(parents=True, exist_ok=True)
            file_path = target_dir / f"part-{datetime.utcnow().timestamp()}.parquet"
            chunk.to_parquet(file_path)

    @staticmethod
    def _timeframe_to_ms(timeframe: str) -> int:
        mapping = {
            "1m": 60 * 1000,
            "5m": 5 * 60 * 1000,
            "15m": 15 * 60 * 1000,
            "30m": 30 * 60 * 1000,
            "1h": 60 * 60 * 1000,
            "4h": 4 * 60 * 60 * 1000,
            "1d": 24 * 60 * 60 * 1000,
            "1w": 7 * 24 * 60 * 60 * 1000,
            "2w": 14 * 24 * 60 * 60 * 1000,
        }
        return mapping[timeframe]
