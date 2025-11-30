from __future__ import annotations

import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.backtests.adapters import BacktestingPyAdapter, PyBrokerAdapter
from app.backtests.registry import strategy_specs
from app.backtests.service import BacktestService
from app.backtests.store import BacktestStore
from app.models import BacktestJobCreate, BacktestJob

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/backtests", tags=["backtests"])

store = BacktestStore()
adapters_map = {
    "backtesting_py": BacktestingPyAdapter(),
    "pybroker": PyBrokerAdapter(),
}
service = BacktestService(store=store, adapters=adapters_map)
ARTIFACTS_ROOT = Path("data/backtests_artifacts").resolve()


@router.get("/strategies")
def list_strategies():
    return [spec.to_dict() for spec in strategy_specs()]


@router.get("/jobs", response_model=list[BacktestJob])
def list_jobs(limit: int = 50):
    return store.list_jobs(limit=limit)


@router.post("/jobs", response_model=BacktestJob)
def submit_job(payload: BacktestJobCreate, background_tasks: BackgroundTasks):
    job_id = service.submit_job(payload)
    background_tasks.add_task(service.run_job, job_id)
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=500, detail="Failed to create job")
    return job.to_model()


@router.get("/jobs/{job_id}", response_model=BacktestJob)
def get_job(job_id: str):
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_model()


@router.delete("/jobs/{job_id}")
def delete_job(job_id: str):
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    store.delete_job(job_id)
    return {"status": "deleted", "id": job_id}


@router.get("/jobs/{job_id}/artifacts/{artifact_name}")
def get_artifact(job_id: str, artifact_name: str):
    job = store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    path_rel = job.artifacts.get(artifact_name)
    if not path_rel:
        raise HTTPException(status_code=404, detail="Artifact not found")
    path = (ARTIFACTS_ROOT / path_rel).resolve()
    if not path.is_file() or ARTIFACTS_ROOT not in path.parents:
        raise HTTPException(status_code=404, detail="Artifact path invalid")
    return FileResponse(path)
