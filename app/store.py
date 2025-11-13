from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from app.models import DataJob, JobStatus, JobOptions


@dataclass
class JobRecord:
    id: str
    exchange: str
    symbol: str
    timeframe: str
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    status: JobStatus
    progress: float
    created_at: datetime
    updated_at: datetime
    options: JobOptions
    details: Dict[str, Any]
    result: Dict[str, Any]

    def to_data_job(self) -> DataJob:
        return DataJob(
            id=self.id,
            exchange=self.exchange,
            symbol=self.symbol,
            timeframe=self.timeframe,
            start_timestamp=self.start_timestamp,
            end_timestamp=self.end_timestamp,
            status=self.status,
            progress=self.progress,
            created_at=self.created_at,
            updated_at=self.updated_at,
            options=self.options,
            details=self.details,
            result=self.result,
        )


class JobStore:
    def __init__(self, db_path: Path = Path("data/jobs.db")) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    exchange TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    start_ts INTEGER,
                    end_ts INTEGER,
                    status TEXT NOT NULL,
                    progress REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    options TEXT NOT NULL,
                    details TEXT NOT NULL,
                    result TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def create_job(self, job: JobRecord) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO jobs (id, exchange, symbol, timeframe, start_ts, end_ts, status, progress, created_at, updated_at, options, details, result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.exchange,
                    job.symbol,
                    job.timeframe,
                    job.start_timestamp,
                    job.end_timestamp,
                    job.status.value,
                    job.progress,
                    job.created_at.isoformat(),
                    job.updated_at.isoformat(),
                    job.options.json(),
                    json.dumps(job.details),
                    json.dumps(job.result),
                ),
            )
            conn.commit()

    def update_job(self, job_id: str, *, status: Optional[JobStatus] = None, progress: Optional[float] = None, details: Optional[Dict[str, Any]] = None, result: Optional[Dict[str, Any]] = None) -> None:
        row = self.get_job(job_id)
        if row is None:
            raise ValueError(f"Job {job_id} not found")
        record = row
        kwargs = {
            "status": status or record.status,
            "progress": progress if progress is not None else record.progress,
            "details": details if details is not None else record.details,
            "result": result if result is not None else record.result,
        }
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE jobs
                SET status=?, progress=?, details=?, result=?, updated_at=?
                WHERE id=?
                """,
                (
                    kwargs["status"].value if isinstance(kwargs["status"], JobStatus) else kwargs["status"],
                    kwargs["progress"],
                    json.dumps(kwargs["details"]),
                    json.dumps(kwargs["result"]),
                    datetime.utcnow().isoformat(),
                    job_id,
                ),
            )
            conn.commit()

    def list_jobs(self) -> List[DataJob]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
        return [self._row_to_record(row).to_data_job() for row in rows]

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        return self._row_to_record(row) if row else None

    def _row_to_record(self, row: sqlite3.Row) -> JobRecord:
        return JobRecord(
            id=row["id"],
            exchange=row["exchange"],
            symbol=row["symbol"],
            timeframe=row["timeframe"],
            start_timestamp=row["start_ts"],
            end_timestamp=row["end_ts"],
            status=JobStatus(row["status"]),
            progress=row["progress"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            options=JobOptions.parse_raw(row["options"]),
            details=json.loads(row["details"]),
            result=json.loads(row["result"]),
        )
