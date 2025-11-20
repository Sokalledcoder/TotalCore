# Handoff Report – Session 6 (TradeCore HMM Lab)
Date: 2025-11-20 (current backend session)

## State of the System
- Backend: FastAPI/uvicorn on http://localhost:8000. Check `ps -ef | grep uvicorn` for the active PID (last start while writing this: 2728756 then 2729957 then 2709906, current run: 2709906/2728756/2729957 sequence; most recent start shows 200 OK). DuckDB `tradecore.duckdb` is locked while the server runs.
- Frontend: `frontend/hmm-dashboard.html` (JS cache-bust v=5). Profiles dropdown controls modes.
- Data: 1m Binance BTC/USDT stored; higher timeframes are aggregated on the fly (5m/13m/15m/30m/1h/4h/1d).
- Scheduler: On startup, catch-up ingest from last 1m to now; scheduled incremental ingest every 5 minutes for Binance BTC/USDT 1m. Need stable uptime to confirm “Incremental ingest completed” logs.

## Key Backend Changes
- Model training/profiles:
  - Legacy: full covariance, no scaling, exact K, fit on full window. Auto-K ignored.
  - Scaled: z-scored features, diag covariance, strict K.
  - Scaled+Auto-K: K search (2–4) with train/val split, BIC/val diagnostics.
- Label mapping: K=3 → Bear/Chop/Bull; K=4 → Strong Bear/Bear/Chop/Bull; K>=5 adds Chop 1/2… then Bull/Strong Bull.
- Persistence: models saved with timestamped IDs `exchange_symbol_timeframe_ts`. `/regime` returns {data, labels}; saved runs no longer overwrite.
- `/api/hmm/regime`: supports model_id; safer OHLC join; bounds window when no dates on aggregated frames.
- `/api/hmm/latest`: returns latest bar probs (uses persisted if available, otherwise computes from recent window).
- `/api/price/latest`: lightweight last candle.
- DB helpers: `get_market_data_for_timestamps`, `get_recent_market_data`.
- Incremental ingest: `app/api.py` now uses APScheduler for 5-min ingest + startup catch-up.

## Frontend Changes
- Profiles dropdown (Legacy, Scaled, Scaled+Auto-K); legacy checkbox removed.
- Saved Runs: timestamped entries; Load Run immediately loads charts (no extra refresh) with loading state.
- Probability card under Regime Analysis shows numeric latest probs + timestamp; auto-refresh (15s) pulls `/api/hmm/latest`.
- Timeframe chips; candle limit (default 1000); start/end pickers. Auto-refresh now refreshes probs only; charts remain static until Refresh View.
- Color map cleaned for multi-state runs; labels preserved from backend response.

## Feature/Model Pipeline (current)
- Features: log return, rolling vol (14), volume z-score (28), ADX(14), RSI(14). Legacy uses raw; Scaled uses z-score.
- HMM: hmmlearn.GaussianHMM; diag covariance (modern) or full (legacy); n_iter=100; random_state=42.
- Diagnostics on train: k, loglik_train/val, BIC, state_counts, mode (legacy/modern).

## Known Issues / Watchpoints
- DuckDB: single-writer; stop uvicorn to inspect DB (lock errors otherwise).
- Scheduler: need to observe “Incremental ingest completed” after stable uptime; restarts interrupt it.
- `/api/hmm/latest`: requires model_id or exchange/symbol/timeframe; bounded to ~400 buckets when aggregating.
- Prob card updates only when the auto-refresh toggle is ON.

## Recommended Next Steps
- Let the server run >5 minutes and watch `server.log` for ingest completion; otherwise kick off a manual catch-up.
- Add “last updated” badge near the prob card.
- Add feature-profile variants (e.g., MA slopes + ATR replacing RSI) without touching legacy.
- Add degenerate-state warning in stats (state count <5%).
- Clean up old non-timestamped model files (ts=0) after verifying needed runs.

## How to Reproduce the “Good” Look
- Profile: Legacy; States: 3; Auto-K OFF. Train; load the resulting timestamped run from Saved Runs. Colors: Bear/Chop/Bull.

## Saved Runs Snapshot (from /api/hmm/models when checked)
- binance_BTC-USDT_5m_1763610368
- binance_BTC-USDT_15m_1763610031
- binance_BTC-USDT_1h_1763609719
- plus earlier 1h timestamped models and some old non-ts IDs (ts=0).

## Quick Ops
- Start backend: `bash scripts/run_api.sh`
- Hard refresh dashboard (uses `hmm-dashboard.js?v=5`).
- Load run: select in Saved Runs → Load Run (charts render; prob card updates). Auto-refresh toggle re-pulls probs every 15s.
- Manual DB access: stop uvicorn first to avoid DuckDB lock.
- Manual ingest (if scheduler not caught up): use HistoryIngestor with start=last_ts+1m to now.

## Session Context
- This report replaces the deleted “HMM RESEARCH V1” file; the new research doc is `HMM-RESEARCH-V1.md`.
- Untracked/completed files staged: app/api.py, app/db.py, app/routers/hmm.py, app/services/hmm_engine.py, frontend/hmm-dashboard.html/.js, scripts/check_db.py/test_ingestion.py/verify_hmm.py, ccxt-binance.md, hmm-implementation-v1.md, walkthrough.md, HMM-RESEARCH-V1.md.
- Unstaged/untracked: DuckDB files (`tradecore.duckdb`/wal) and `backend.log` (keep untracked). EOF
