# Handoff Report — Session 1

## Summary
- FastAPI backend + static UI now ingest Kraken candles via CCXT trades, track jobs in SQLite, and write Parquet partitions under `data/lake/kraken/<PAIR>/<TF>/year=YYYY/`.
- Dark-themed dashboard (HTML/CSS/JS) lets us submit jobs, see progress/errors, and inspect coverage.
- `scripts/run_api.sh` gives reproducible uvicorn restarts (PID + health log).
- `KrakenTradeAggregator` paginates trades correctly; latest job backfilled BTC/USD 1m candles from **2025‑01‑01 → 2025‑11‑12** (~93k rows). Older 2024 data was removed to keep only the recent window.

## Current State
- Backend (`app/api.py`) serves `/api/data-jobs`, `/api/data-jobs/{id}`, `/api/data-coverage`, `/api/data-jobs/{id}/actions`.
- Ingestion: `_run_trade_backfill` paginates trades, aggregates via `build_ohlcvc`, writes Parquet; `_fetch_rest` tops off the latest 720 bars. Jobs now complete successfully for the requested window.
- Frontend dashboard is fully functional for new requests; dedup/cleanup is manual (delete overlapping `year=*` directories before reruns).
- Scripts: `scripts/run_api.sh` is the standard way to restart uvicorn.

## Problems / Open Items
1. **Retention management** — Current dataset only covers 2025. Reruns that overlap existing partitions will create duplicates unless we prune beforehand. Need tooling for automated cleanup/dedup when we decide to ingest earlier years.
2. **Data validation** — No automated QC (gap detection, continuity checks) yet. Manual inspection only.
3. **Downstream work** — RL environment, tools framework, and RunPod orchestration are still ahead.

## Planned Next Steps
- **Streaming CCXT Pro integration:** add a long-lived worker that subscribes to `watchTrades`/`watchOHLCV` so new candles append in near real time after a backfill completes.
- **RL environment kick-off:** start Phase 4 from `docs/research/execution_plan.md` (observation builder, action space, reward schema, config files) using the current 2025 dataset for initial testing.
- **Optional when needed:** add resumable checkpoints (persist cursor outside SQLite) and formal QC scripts. These can wait until after the first RL prototype.

## Useful Commands & Files
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
scripts/run_api.sh   # restart uvicorn, print PID/log snippet
curl -s http://localhost:8000/   # health check
```
Key files:
- `app/api.py`, `app/models.py`, `app/store.py`
- `app/ingestion/kraken.py`, `app/ingestion/trade_aggregator.py`
- `frontend/fetch-history.html|js|css`
- `docs/research/*` for requirements
- `scripts/run_api.sh`

## Data & Logs
- `data/jobs.db`: SQLite job metadata (inspect with `sqlite3 data/jobs.db "SELECT * FROM jobs;"`).
- `data/lake/kraken/BTC-USD/1m/year=2025`: current candle store (93k rows, Jan→Nov 2025). Delete overlapping year folders before large reruns.
- `server.log`: backend logs; check after each job or restart.

## Session Context
This report covers Session 1 (initial build + debugging + successful 2025 backfill). Next session should follow the “Planned Next Steps” section (streaming integration + RL environment v1).
