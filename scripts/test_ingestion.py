import asyncio
from app.store import JobStore, JobRecord, JobStatus
from app.models import DataJob
from app.ingestion.fetcher import HistoryIngestor
from app.db import db
from datetime import datetime, timedelta
import uuid

def test_ingestion():
    store = JobStore()
    ingestor = HistoryIngestor(store)
    
    # Create a test job
    job_id = str(uuid.uuid4())
    now = datetime.utcnow()
    start = now - timedelta(days=1) # Fetch last 1 day
    
    job = DataJob(
        id=job_id,
        exchange="binance",
        symbol="BTC/USDT",
        timeframe="15m",
        start_timestamp=int(start.timestamp() * 1000),
        end_timestamp=int(now.timestamp() * 1000),
        status=JobStatus.queued,
        progress=0.0,
        created_at=now,
        updated_at=now,
        options={},
        details={},
        result={}
    )
    
    # Register job in store
    store.create_job(JobRecord(
        id=job.id,
        exchange=job.exchange,
        symbol=job.symbol,
        timeframe=job.timeframe,
        start_timestamp=job.start_timestamp,
        end_timestamp=job.end_timestamp,
        status=job.status,
        progress=job.progress,
        created_at=job.created_at,
        updated_at=job.updated_at,
        options=job.options,
        details=job.details,
        result=job.result
    ))

    print(f"Starting ingestion for job {job_id}...")
    ingestor.ingest(job)
    
    # Verify DuckDB
    print("Verifying DuckDB...")
    df = db.get_market_data("binance", "BTC/USDT", "15m")
    print(f"DuckDB has {len(df)} rows.")
    print(df.head())
    
    if not df.empty:
        print("SUCCESS: Data found in DuckDB.")
    else:
        print("FAILURE: No data in DuckDB.")

if __name__ == "__main__":
    test_ingestion()
