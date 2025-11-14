from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, List

from app.models import ExperimentJob, JobStatus


@dataclass
class ExperimentJobRecord:
    id: str
    status: JobStatus
    tag: str
    train_config_path: str
    env_config_path: str
    episodes: int
    seed: int
    overrides: Dict[str, Any]
    result: Dict[str, Any]
    error: Optional[str]
    workdir: str
    created_at: datetime
    updated_at: datetime

    def to_model(self) -> ExperimentJob:
        return ExperimentJob(
            id=self.id,
            status=self.status,
            tag=self.tag,
            train_config_path=self.train_config_path,
            env_config_path=self.env_config_path,
            episodes=self.episodes,
            seed=self.seed,
            overrides=self.overrides,
            result=self.result,
            error=self.error,
            workdir=self.workdir,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class ExperimentStore:
    def __init__(self, db_path: Path = Path("data/experiments.db")) -> None:
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
                CREATE TABLE IF NOT EXISTS experiment_jobs (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    tag TEXT NOT NULL,
                    train_config_path TEXT NOT NULL,
                    env_config_path TEXT NOT NULL,
                    episodes INTEGER NOT NULL,
                    seed INTEGER NOT NULL,
                    overrides TEXT NOT NULL,
                    result TEXT NOT NULL,
                    error TEXT,
                    workdir TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def create_job(self, record: ExperimentJobRecord) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO experiment_jobs (
                    id, status, tag, train_config_path, env_config_path, episodes, seed,
                    overrides, result, error, workdir, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.status.value,
                    record.tag,
                    record.train_config_path,
                    record.env_config_path,
                    record.episodes,
                    record.seed,
                    json.dumps(record.overrides),
                    json.dumps(record.result),
                    record.error,
                    record.workdir,
                    record.created_at.isoformat(),
                    record.updated_at.isoformat(),
                ),
            )
            conn.commit()

    def update_job(
        self,
        job_id: str,
        *,
        status: Optional[JobStatus] = None,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        row = self.get_job(job_id)
        if not row:
            raise ValueError(f"Experiment job {job_id} not found")
        updated_result = result if result is not None else row.result
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE experiment_jobs
                SET status=?, result=?, error=?, updated_at=?
                WHERE id=?
                """,
                (
                    (status or row.status).value,
                    json.dumps(updated_result),
                    error,
                    datetime.utcnow().isoformat(),
                    job_id,
                ),
            )
            conn.commit()

    def list_jobs(self) -> List[ExperimentJob]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM experiment_jobs ORDER BY created_at DESC"
            ).fetchall()
        return [self._row_to_record(row).to_model() for row in rows]

    def get_job(self, job_id: str) -> ExperimentJobRecord | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM experiment_jobs WHERE id=?", (job_id,)
            ).fetchone()
        return self._row_to_record(row) if row else None

    def _row_to_record(self, row: sqlite3.Row) -> ExperimentJobRecord:
        return ExperimentJobRecord(
            id=row["id"],
            status=JobStatus(row["status"]),
            tag=row["tag"],
            train_config_path=row["train_config_path"],
            env_config_path=row["env_config_path"],
            episodes=row["episodes"],
            seed=row["seed"],
            overrides=json.loads(row["overrides"]),
            result=json.loads(row["result"]),
            error=row["error"],
            workdir=row["workdir"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
