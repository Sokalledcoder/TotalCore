from __future__ import annotations

import json
import logging
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.coverage import scan_coverage
from app.experiment_store import ExperimentJobRecord, ExperimentStore
from app.ingestion.kraken import KrakenHistoryIngestor
from app.models import (
    DataJob,
    DataJobCreate,
    ExperimentJob,
    ExperimentLaunchRequest,
    ExperimentRunSummary,
    JobAction,
    JobStatus,
)
from app.rl.datasets import load_manifest
from app.rl.training_config import load_training_config
from app.store import JobRecord, JobStore
from app.tools import list_indicator_specs

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = REPO_ROOT / "tmp" / "experiment_jobs"
RUNS_ROOT = REPO_ROOT / "runs" / "experiments"

app = FastAPI(title="TradeCore Data Service")
store = JobStore()
ingestor = KrakenHistoryIngestor(store)
experiment_store = ExperimentStore()
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def root():
    return FileResponse("frontend/fetch-history.html")


@app.get("/control-panel")
def control_panel():
    control_path = REPO_ROOT / "frontend" / "control-panel.html"
    if not control_path.exists():
        raise HTTPException(status_code=404, detail="Control panel page is not available yet")
    return FileResponse(control_path)


@app.post("/api/data-jobs", response_model=DataJob)
def create_job(payload: DataJobCreate, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    now = datetime.utcnow()
    record = JobRecord(
        id=job_id,
        exchange=payload.exchange,
        symbol=payload.symbol,
        timeframe=payload.timeframe,
        start_timestamp=payload.start_timestamp,
        end_timestamp=payload.end_timestamp,
        status=JobStatus.queued,
        progress=0.0,
        created_at=now,
        updated_at=now,
        options=payload.options,
        details={},
        result={},
    )
    store.create_job(record)
    background_tasks.add_task(_run_job, job_id)
    return record.to_data_job()


def _run_job(job_id: str) -> None:
    job = store.get_job(job_id)
    if not job:
        return
    ingestor.ingest(job.to_data_job())


@app.get("/api/data-jobs/{job_id}", response_model=DataJob)
def get_job(job_id: str):
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_data_job()


@app.get("/api/data-coverage")
def list_coverage(exchange: str, symbol: str):
    return scan_coverage(KrakenHistoryIngestor(store).config.data_dir, exchange, symbol)


@app.post("/api/data-jobs/{job_id}/actions")
def job_action(job_id: str, action: JobAction):
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if action.action == "validate":
        store.update_job(job_id, details={**job.details, "validation": "pending"})
    elif action.action == "resume":
        store.update_job(job_id, status=JobStatus.queued)
    elif action.action == "download":
        return {"message": "Download ready", "paths": []}
    return {"status": "ok"}


@app.get("/api/run-options")
def list_run_options():
    return {
        "env_configs": _scan_env_configs(),
        "indicator_manifests": _scan_indicator_manifests(),
        "training_configs": _scan_training_configs(),
        "indicator_catalog": list_indicator_specs(),
    }


@app.get("/api/dataset-manifests")
def list_dataset_manifests():
    return _scan_dataset_manifests()


@app.get("/api/experiment-runs", response_model=List[ExperimentRunSummary])
def list_experiment_runs():
    return _scan_experiment_runs()


@app.get("/api/experiment-jobs", response_model=List[ExperimentJob])
def list_experiment_jobs():
    return experiment_store.list_jobs()


@app.get("/api/experiment-jobs/{job_id}", response_model=ExperimentJob)
def get_experiment_job(job_id: str):
    record = experiment_store.get_job(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="Experiment job not found")
    return record.to_model()


@app.post("/api/experiment-jobs", response_model=ExperimentJob)
def create_experiment_job(payload: ExperimentLaunchRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    env_rel, train_rel, overrides, workdir = _prepare_job_configs(job_id, payload)
    now = datetime.utcnow()
    record = ExperimentJobRecord(
        id=job_id,
        status=JobStatus.queued,
        tag=_normalize_tag(payload.tag),
        train_config_path=str(train_rel),
        env_config_path=str(env_rel),
        episodes=payload.episodes,
        seed=payload.seed,
        overrides=overrides,
        result={},
        error=None,
        workdir=str(workdir.relative_to(REPO_ROOT)),
        created_at=now,
        updated_at=now,
    )
    experiment_store.create_job(record)
    background_tasks.add_task(_run_experiment_job, job_id)
    return record.to_model()


def _prepare_job_configs(job_id: str, payload: ExperimentLaunchRequest):
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    job_dir = WORK_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    env_base = _resolve_repo_path(payload.env_config_path, expected_prefix="configs/env")
    env_data = json.loads(env_base.read_text())
    overrides: Dict[str, Any] = {}

    if payload.indicator_manifest_inline:
        manifest_data = {
            "indicators": [selection.model_dump() for selection in payload.indicator_manifest_inline],
        }
        manifest_path = job_dir / "indicator_manifest.json"
        manifest_path.write_text(json.dumps(manifest_data, indent=2))
        relative_indicator = manifest_path.relative_to(REPO_ROOT)
        env_data["indicator_manifest_path"] = str(relative_indicator)
        overrides["indicator_manifest_inline"] = manifest_data["indicators"]
    elif payload.indicator_manifest_path:
        indicator_path = _resolve_repo_path(
            payload.indicator_manifest_path, expected_prefix="configs/tools"
        )
        relative_indicator = indicator_path.relative_to(REPO_ROOT)
        env_data["indicator_manifest_path"] = str(relative_indicator)
        overrides["indicator_manifest_path"] = str(relative_indicator)

    if payload.risk_pct is not None:
        env_data["risk_pct"] = payload.risk_pct
        overrides["risk_pct"] = payload.risk_pct
    if payload.limit_fee_pct is not None:
        limit_bps = payload.limit_fee_pct * 100.0
        env_data["limit_fee_bps"] = limit_bps
        overrides["limit_fee_pct"] = payload.limit_fee_pct
    if payload.market_fee_pct is not None:
        market_bps = payload.market_fee_pct * 100.0
        env_data["market_fee_bps"] = market_bps
        overrides["market_fee_pct"] = payload.market_fee_pct
    if payload.stop_loss_steps is not None:
        action_cfg = env_data.setdefault("action", {})
        action_cfg["stop_loss_steps"] = payload.stop_loss_steps
        overrides["stop_loss_steps"] = payload.stop_loss_steps

    env_path = job_dir / "env_config.json"
    env_path.write_text(json.dumps(env_data, indent=2))

    train_base = _resolve_repo_path(payload.train_config_path, expected_prefix="configs/train")
    train_cfg = load_training_config(train_base)
    save_path = Path(train_cfg.save_path)
    sanitized_tag = _normalize_tag(payload.tag)
    unique_suffix = job_id[:8]
    new_name = f"{save_path.name}_{sanitized_tag}_{unique_suffix}"
    train_cfg = train_cfg.merge_overrides(
        {
            "env_config_path": str(env_path.relative_to(REPO_ROOT)),
            "save_path": str(save_path.with_name(new_name)),
        }
    )
    train_path = job_dir / "train_config.json"
    train_path.write_text(json.dumps(train_cfg.model_dump(), indent=2))

    overrides["train_config_path"] = str(train_base.relative_to(REPO_ROOT))
    overrides["env_config_path"] = str(env_base.relative_to(REPO_ROOT))

    return (
        env_path.relative_to(REPO_ROOT),
        train_path.relative_to(REPO_ROOT),
        overrides,
        job_dir,
    )


def _run_experiment_job(job_id: str) -> None:
    record = experiment_store.get_job(job_id)
    if not record:
        logger.warning("Experiment job %s missing", job_id)
        return
    experiment_store.update_job(job_id, status=JobStatus.running)
    train_path = REPO_ROOT / record.train_config_path
    cmd = [
        sys.executable,
        "scripts/run_experiment.py",
        "--train-config",
        str(train_path),
        "--episodes",
        str(record.episodes),
        "--seed",
        str(record.seed),
        "--tag",
        record.tag,
    ]
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Experiment job %s crashed", job_id)
        experiment_store.update_job(
            job_id,
            status=JobStatus.failed,
            result={"stdout": "", "stderr": ""},
            error=str(exc),
        )
        return

    stdout_tail = _tail(completed.stdout)
    stderr_tail = _tail(completed.stderr)
    result_payload = {"stdout": stdout_tail, "stderr": stderr_tail}

    if completed.returncode != 0:
        error_msg = completed.stderr.strip() or completed.stdout.strip() or "Experiment failed"
        experiment_store.update_job(
            job_id,
            status=JobStatus.failed,
            result=result_payload,
            error=error_msg,
        )
        return

    run_info = _extract_run_info(completed.stdout)
    if run_info:
        result_payload.update(run_info)
    experiment_store.update_job(
        job_id,
        status=JobStatus.completed,
        result=result_payload,
        error=None,
    )


def _scan_indicator_manifests() -> List[Dict[str, Any]]:
    base = REPO_ROOT / "configs" / "tools"
    if not base.exists():
        return []
    items: List[Dict[str, Any]] = []
    for path in sorted(base.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        items.append(
            {
                "name": path.stem,
                "path": str(path.relative_to(REPO_ROOT)),
                "indicator_count": len(data.get("indicators", [])),
                "indicators": data.get("indicators", []),
            }
        )
    return items


def _scan_env_configs() -> List[Dict[str, Any]]:
    base = REPO_ROOT / "configs" / "env"
    if not base.exists():
        return []
    entries: List[Dict[str, Any]] = []
    for path in sorted(base.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        action_cfg = data.get("action", {})
        entries.append(
            {
                "name": path.stem,
                "path": str(path.relative_to(REPO_ROOT)),
                "risk_pct": data.get("risk_pct"),
                "stop_loss_bps": data.get("stop_loss_bps"),
                "stop_loss_steps": action_cfg.get("stop_loss_steps"),
                "limit_fee_bps": data.get("limit_fee_bps"),
                "market_fee_bps": data.get("market_fee_bps"),
                "indicator_manifest_path": data.get("indicator_manifest_path"),
            }
        )
    return entries


def _scan_training_configs() -> List[Dict[str, Any]]:
    base = REPO_ROOT / "configs" / "train"
    if not base.exists():
        return []
    configs: List[Dict[str, Any]] = []
    for path in sorted(base.glob("*.json")):
        try:
            cfg = load_training_config(path)
        except Exception:  # pylint: disable=broad-except
            continue
        configs.append(
            {
                "name": path.stem,
                "path": str(path.relative_to(REPO_ROOT)),
                "algorithm": cfg.algorithm,
                "total_timesteps": cfg.total_timesteps,
                "seed": cfg.seed,
                "num_envs": cfg.num_envs,
                "device": (cfg.algo_kwargs or {}).get("device"),
            }
        )
    return configs


def _scan_experiment_runs(limit: int = 15) -> List[ExperimentRunSummary]:
    if not RUNS_ROOT.exists():
        return []
    runs: List[ExperimentRunSummary] = []
    for path in sorted(RUNS_ROOT.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if not path.is_dir():
            continue
        exp_path = path / "experiment.json"
        if not exp_path.exists():
            continue
        try:
            data = json.loads(exp_path.read_text())
        except json.JSONDecodeError:
            continue
        created_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        tag = path.name.split("_", 1)[1] if "_" in path.name else path.name
        runs.append(
            ExperimentRunSummary(
                name=path.name,
                run_dir=str(path.relative_to(REPO_ROOT)),
                created_at=created_at,
                tag=tag,
                train_meta=data.get("train_meta", {}),
                eval_summary=data.get("eval_summary", {}),
            )
        )
        if len(runs) >= limit:
            break
    return runs


def _scan_dataset_manifests() -> List[Dict[str, Any]]:
    manifests_dir = REPO_ROOT / "data" / "manifests"
    if not manifests_dir.exists():
        return []
    entries: List[Dict[str, Any]] = []
    for path in sorted(manifests_dir.glob("*.json")):
        try:
            manifest = load_manifest(path)
        except Exception:
            continue
        start_ts = min(slice.start_ts for slice in manifest.slices)
        end_ts = max(slice.end_ts for slice in manifest.slices)
        total_rows = sum(slice.rows for slice in manifest.slices)
        entries.append(
            {
                "name": path.stem,
                "path": str(path.relative_to(REPO_ROOT)),
                "symbol": manifest.symbol,
                "timeframe": manifest.timeframe,
                "start_ts": start_ts.isoformat(),
                "end_ts": end_ts.isoformat(),
                "total_rows": total_rows,
                "slice_count": len(manifest.slices),
            }
        )
    return entries


def _resolve_repo_path(value: str, expected_prefix: Optional[str] = None) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / candidate).resolve()
    else:
        candidate = candidate.resolve()
    if expected_prefix:
        expected = (REPO_ROOT / expected_prefix).resolve()
        try:
            candidate.relative_to(expected)
        except ValueError as exc:
            raise HTTPException(
                status_code=400, detail=f"Path {value} must live under {expected_prefix}"
            ) from exc
    if not candidate.exists():
        raise HTTPException(status_code=400, detail=f"Path {value} not found")
    if REPO_ROOT not in candidate.parents and candidate != REPO_ROOT:
        raise HTTPException(status_code=400, detail="Path must reside in repository")
    return candidate


def _normalize_tag(tag: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in tag).strip("-_")
    return safe or "run"


def _tail(text: str, max_lines: int = 40) -> str:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[-max_lines:])


def _extract_run_info(stdout: str) -> Dict[str, Any]:
    for line in reversed(stdout.splitlines()):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            data = json.loads(stripped)
            if isinstance(data, dict) and "run_dir" in data:
                return data
        except json.JSONDecodeError:
            continue
    return {}
