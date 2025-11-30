from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.models import BacktestEngine, BacktestJob, BacktestJobCreate, BacktestDataRef, JobStatus


@dataclass
class BacktestJobRecord:
    id: str
    strategy_id: str
    engine: BacktestEngine
    status: JobStatus
    progress: float
    created_at: datetime
    updated_at: datetime
    params: Dict[str, Any]
    data: BacktestDataRef
    cv_config: Dict[str, Any]
    optimizer: Dict[str, Any]
    metrics: Dict[str, Any]
    artifacts: Dict[str, Any]
    error: Optional[str] = None

    def to_model(self) -> BacktestJob:
        return BacktestJob(
            id=self.id,
            status=self.status,
            progress=self.progress,
            created_at=self.created_at,
            updated_at=self.updated_at,
            engine=self.engine,
            strategy_id=self.strategy_id,
            params=self.params,
            data=self.data,
            cv_config=self.cv_config,
            optimizer=self.optimizer,
            metrics=self.metrics,
            artifacts=self.artifacts,
            error=self.error,
        )


class BacktestStore:
    def __init__(self, db_path: Path | str = Path("data/backtests.db")) -> None:
        self.db_path = Path(db_path)
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
                CREATE TABLE IF NOT EXISTS backtest_jobs (
                    id TEXT PRIMARY KEY,
                    strategy_id TEXT NOT NULL,
                    engine TEXT NOT NULL,
                    status TEXT NOT NULL,
                    progress REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    params TEXT NOT NULL,
                    data_ref TEXT NOT NULL,
                    cv_config TEXT NOT NULL,
                    optimizer TEXT NOT NULL,
                    metrics TEXT NOT NULL,
                    artifacts TEXT NOT NULL,
                    error TEXT
                )
                """
            )
            conn.commit()

    def create_job(self, job: BacktestJobRecord) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO backtest_jobs
                (id, strategy_id, engine, status, progress, created_at, updated_at, params, data_ref, cv_config, optimizer, metrics, artifacts, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.strategy_id,
                    job.engine.value,
                    job.status.value,
                    job.progress,
                    job.created_at.isoformat(),
                    job.updated_at.isoformat(),
                    json.dumps(job.params),
                    job.data.model_dump_json(),
                    json.dumps(job.cv_config),
                    json.dumps(job.optimizer),
                    json.dumps(job.metrics),
                    json.dumps(job.artifacts),
                    job.error,
                ),
            )
            conn.commit()

    def update_job(
        self,
        job_id: str,
        *,
        status: Optional[JobStatus] = None,
        progress: Optional[float] = None,
        metrics: Optional[Dict[str, Any]] = None,
        artifacts: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        record = self.get_job(job_id)
        if record is None:
            raise ValueError(f"Backtest job {job_id} not found")
        new_status = status or record.status
        new_progress = progress if progress is not None else record.progress
        new_metrics = metrics if metrics is not None else record.metrics
        new_artifacts = artifacts if artifacts is not None else record.artifacts
        new_error = error if error is not None else record.error
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE backtest_jobs
                SET status=?, progress=?, metrics=?, artifacts=?, error=?, updated_at=?
                WHERE id=?
                """,
                (
                    new_status.value,
                    new_progress,
                    json.dumps(new_metrics),
                    json.dumps(new_artifacts),
                    new_error,
                    datetime.utcnow().isoformat(),
                    job_id,
                ),
            )
            conn.commit()

    def list_jobs(self, limit: int = 50) -> List[BacktestJob]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM backtest_jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [self._row_to_record(row).to_model() for row in rows]

    def get_job(self, job_id: str) -> Optional[BacktestJobRecord]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM backtest_jobs WHERE id=?", (job_id,)).fetchone()
        return self._row_to_record(row) if row else None

    def delete_job(self, job_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM backtest_jobs WHERE id=?", (job_id,))
            conn.commit()

    def _row_to_record(self, row: sqlite3.Row) -> BacktestJobRecord:
        return BacktestJobRecord(
            id=row["id"],
            strategy_id=row["strategy_id"],
            engine=BacktestEngine(row["engine"]),
            status=JobStatus(row["status"]),
            progress=row["progress"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            params=json.loads(row["params"]),
            data=BacktestDataRef.model_validate_json(row["data_ref"]),
            cv_config=json.loads(row["cv_config"]),
            optimizer=json.loads(row["optimizer"]),
            metrics=json.loads(row["metrics"]),
            artifacts=json.loads(row["artifacts"]),
            error=row["error"],
        )
