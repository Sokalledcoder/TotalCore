from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import pandas as pd

from app.backtests.adapters import EngineAdapter, BacktestResult
from app.backtests.registry import get_strategy_spec
from app.backtests.store import BacktestStore, BacktestJobRecord
from app.models import BacktestJobCreate, BacktestEngine, JobStatus

logger = logging.getLogger(__name__)


class BacktestService:
    def __init__(self, store: BacktestStore, adapters: Dict[BacktestEngine, EngineAdapter], artifacts_root: Path | str = Path("data/backtests_artifacts")) -> None:
        self.store = store
        self.adapters = adapters
        self.artifacts_root = Path(artifacts_root)
        self.artifacts_root.mkdir(parents=True, exist_ok=True)

    def submit_job(self, payload: BacktestJobCreate) -> str:
        job_id = str(uuid.uuid4())
        now = datetime.utcnow()
        record = BacktestJobRecord(
            id=job_id,
            strategy_id=payload.strategy_id,
            engine=payload.engine,
            status=JobStatus.queued,
            progress=0.0,
            created_at=now,
            updated_at=now,
            params=payload.params or {},
            data=payload.data,
            cv_config=payload.cv_config or {},
            optimizer=payload.optimizer or {},
            metrics={},
            artifacts={},
        )
        self.store.create_job(record)
        return job_id

    def run_job(self, job_id: str) -> None:
        job = self.store.get_job(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        # quick validation
        if not get_strategy_spec(job.strategy_id):
            self.store.update_job(job_id, status=JobStatus.failed, error=f"Unknown strategy_id {job.strategy_id}")
            return

        adapter = self.adapters.get(job.engine)
        if adapter is None:
            self.store.update_job(job_id, status=JobStatus.failed, error=f"No adapter registered for engine {job.engine}")
            return

        self.store.update_job(job_id, status=JobStatus.running, progress=0.05)
        try:
            result = adapter.run(job.strategy_id, job.params, job.data, job.cv_config)
            artifacts = self._persist_artifacts(job_id, result)
            metrics = self._merge_metrics(result)
            self.store.update_job(
                job_id,
                status=JobStatus.completed,
                progress=1.0,
                metrics=metrics,
                artifacts=artifacts,
            )
        except Exception as exc:
            logger.exception("Backtest job %s failed", job_id)
            self.store.update_job(job_id, status=JobStatus.failed, error=str(exc))

    def _persist_artifacts(self, job_id: str, result: BacktestResult) -> Dict[str, Any]:
        run_dir = self.artifacts_root / job_id
        run_dir.mkdir(parents=True, exist_ok=True)

        equity_path = run_dir / "equity.csv"
        trades_path = run_dir / "trades.csv"
        metrics_path = run_dir / "metrics.json"
        chart_path = run_dir / "chart_preview.json"

        result.equity_curve.to_frame("equity").to_csv(equity_path, index=True)
        result.trades.to_csv(trades_path, index=False)
        metrics_payload = {k: float(v) if hasattr(v, "__float__") else v for k, v in result.metrics.items()}
        metrics_path.write_text(json.dumps(metrics_payload, indent=2))

        # Build chart preview (up to 3000 rows for better context)
        chart_limit = 3000
        chart_payload = self._build_chart_preview(result, limit=chart_limit)
        chart_path.write_text(json.dumps(chart_payload))

        return {
            "equity_csv": str(equity_path.relative_to(self.artifacts_root)),
            "trades_csv": str(trades_path.relative_to(self.artifacts_root)),
            "metrics_json": str(metrics_path.relative_to(self.artifacts_root)),
            "chart_preview": str(chart_path.relative_to(self.artifacts_root)),
        }

    def _merge_metrics(self, result: BacktestResult) -> Dict[str, Any]:
        metrics = dict(result.metrics)
        metrics.setdefault("n_trades", int(len(result.trades)))
        metrics.setdefault("engine", result.engine)
        return metrics

    def _build_chart_preview(self, result: BacktestResult, limit: int = 50000) -> Dict[str, Any]:
        df = result.price.copy()
        if "Timestamp" in df.columns:
            df = df.reset_index()
            df.rename(columns={"Timestamp": "timestamp"}, inplace=True)
        if "timestamp" not in df.columns:
            df["timestamp"] = df.index
        if limit and len(df) > limit:
            df = df.tail(limit)

        price_rows = []
        for row in df.itertuples():
            price_rows.append(
                {
                    "t": int(pd.Timestamp(row.timestamp).timestamp()),
                    "o": float(row.Open),
                    "h": float(row.High),
                    "l": float(row.Low),
                    "c": float(row.Close),
                }
            )

        indicators = {}
        for name, series in (result.indicators or {}).items():
            s = series
            if len(s) > limit:
                s = s.tail(limit)
            indicators[name] = [
                {
                    "t": int(pd.Timestamp(idx).timestamp()),
                    "v": float(val) if pd.notna(val) else None,
                }
                for idx, val in s.items()
            ]

        trades_rows = []
        trades = result.trades
        if not trades.empty:
            for row in trades.itertuples():
                entry_t = getattr(row, "EntryTime", None)
                exit_t = getattr(row, "ExitTime", None)
                trades_rows.append(
                    {
                        "entry_t": entry_t.isoformat() if hasattr(entry_t, "isoformat") else str(entry_t),
                        "exit_t": exit_t.isoformat() if hasattr(exit_t, "isoformat") else str(exit_t),
                        "entry_price": float(getattr(row, "EntryPrice", 0.0)),
                        "exit_price": float(getattr(row, "ExitPrice", 0.0)),
                        "side": getattr(row, "Direction", ""),
                        "size": float(getattr(row, "Size", 0.0)),
                    }
                )

        return {"price": price_rows, "indicators": indicators, "trades": trades_rows}
