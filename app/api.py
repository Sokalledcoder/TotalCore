from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.coverage import scan_coverage
from app.ingestion.kraken import KrakenHistoryIngestor
from app.models import DataJobCreate, JobStatus, DataJob, JobAction
from app.store import JobStore, JobRecord

app = FastAPI(title="TradeCore Data Service")
store = JobStore()
ingestor = KrakenHistoryIngestor(store)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def root():
    return FileResponse("frontend/fetch-history.html")


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
