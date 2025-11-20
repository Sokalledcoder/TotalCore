# Handoff Report – Session 7 (TradeCore HMM Lab)
Date: 2025-11-20

## 0) Quick status
- Backend: FastAPI/uvicorn on http://localhost:8000 (latest start during this handoff: PID 2709906 → restarted multiple times; current at writing: PID 2728756/2729957/2709906 chain, last reported 200 OK). DuckDB `tradecore.duckdb` locked while server runs.
- Frontend: `frontend/hmm-dashboard.html` using `hmm-dashboard.js?v=5` (cache-bust). Profile dropdown controls modes.
- Data: 1m Binance BTC/USDT ingested historically; higher TFs aggregated on the fly (5m/13m/15m/30m/1h/4h/1d).
- Scheduler: On startup does catch-up; incremental ingest every 5 minutes for Binance BTC/USDT 1m. Needs stable uptime to see “Incremental ingest completed” in `server.log`.

## 1) What changed this session
- **Model persistence**
  - Models now saved with unique timestamped IDs: `exchange_symbol_timeframe_ts`; avoids overwrites. `/api/hmm/regime` can load by `model_id` or latest matching prefix.
- **Profiles / modes**
  - Legacy: full covariance, no scaling, exact K, fit on full window; Auto-K ignored.
  - Scaled: z-scored features, diag covariance, strict K.
  - Scaled+Auto-K: K search (2–4) with train/val split; returns diagnostics (loglik train/val, BIC, state counts, mode).
- **Labels/colors**
  - K=3 → Bear/Chop/Bull; K=4 → Strong Bear/Bear/Chop/Bull; K>=5 adds Chop i then Bull/Strong Bull. Color map updated to distinct reds/greys/greens.
- **Endpoints**
  - `/api/hmm/regime`: safer OHLC join, bounded window when no dates on aggregated TFs, supports `model_id`.
  - `/api/hmm/latest`: returns latest bar regime probs (uses persisted row if present; else computes on recent window).
  - `/api/price/latest`: lightweight last candle.
- **DB helpers**
  - `get_market_data_for_timestamps` and `get_recent_market_data` to speed saved-run loading.
- **Scheduler**
  - Added APScheduler in `app/api.py`: startup catch-up ingest + 5-minute incremental ingest for Binance BTC/USDT 1m.
- **Frontend**
  - Saved Runs list shows timestamped models; Load Run immediately loads data (no extra refresh) with loading state.
  - Probability card under Regime Analysis shows numeric latest probs + timestamp.
  - Auto-refresh now re-fetches latest probabilities every 15s (charts remain static unless Refresh View).
  - Profiles dropdown replaces legacy checkbox.
  - Timeframe chips, candle limit (default 1000), start/end pickers retained.

## 2) Current feature/model pipeline
- Features: log return, rolling vol(14), volume z-score(28), ADX(14), RSI(14). Legacy uses raw; Scaled uses z-score.
- HMM: hmmlearn.GaussianHMM; diag covariance (modern) or full (legacy); n_iter=100; random_state=42.
- Diagnostics on train: k, loglik train/val, BIC, state_counts, mode (legacy/modern).

## 3) Data & ingestion
- Stored base: 1m Binance BTC/USDT.
- Aggregation: on-the-fly for 5m/13m/15m/30m/1h/4h/1d in `db.get_market_data`.
- Scheduler:
  - On startup: catch-up from last stored 1m to now.
  - Every 5 minutes: incremental ingest for 1m BTC/USDT. Needs server to stay up; no confirmed completion logs yet (due to frequent restarts). Monitor `server.log` for “Incremental ingest completed”.

## 4) UX flows (current)
- To reproduce “good” legacy look: Profile=Legacy, States=3, Auto-K off; train; load the new timestamped run from Saved Runs. Colors: Bear/Chop/Bull.
- Saved run loading: select run → Load Run (charts + prob card update). No extra refresh needed.
- Auto-refresh toggle: updates the numeric probability card every 15s via `/api/hmm/latest`; chart remains static until Refresh View.

## 5) Pending issues / watchpoints
- DuckDB single-writer: stop uvicorn to inspect DB directly.
- Scheduler confirmation: need stable uptime to verify periodic ingest (no “Incremental ingest completed” seen yet).
- `/api/hmm/latest` requires model_id or exchange/symbol/timeframe; bounded to ~400 buckets for aggregated TFs.
- Prob card only updates when auto-refresh is ON.
- Old non-timestamped models (ts=0) still listed; safe to clean once desired runs are confirmed saved.

## 6) Recommended next steps
- Let backend run >5 minutes; tail `server.log` for ingest completion. If absent, trigger manual catch-up (HistoryIngestor from last_ts+1m to now).
- Add “last updated” badge to probability card; consider shorter auto-refresh (e.g., 10s) if stable.
- Add new feature profile (e.g., swap RSI for MA slopes + ATR) without touching legacy.
- Add warning in stats card when any state count <5% to flag degenerate runs.
- Clean up old non-ts model files after verification.

## 7) Saved runs snapshot (from `/api/hmm/models`)
- binance_BTC-USDT_5m_1763610368
- binance_BTC-USDT_15m_1763610031
- binance_BTC-USDT_1h_1763609719
- Additional older 1h timestamped runs and ts=0 legacy runs.

## 8) Quick ops
- Start backend: `bash scripts/run_api.sh`
- Hard refresh dashboard: uses `hmm-dashboard.js?v=5`.
- Load run: select Saved Run → Load Run (charts render; prob card updates). Auto-refresh checkbox pulls `/api/hmm/latest` every 15s.
- Manual DB access: stop uvicorn first to avoid DuckDB lock.
- Manual ingest: run HistoryIngestor from last_ts+1m to now if scheduler didn’t catch up.

## 9) Files staged (this session)
- app/api.py, app/db.py, app/ingestion/fetcher.py, app/routers/hmm.py, app/services/hmm_engine.py
- frontend/hmm-dashboard.html, frontend/hmm-dashboard.js
- HMM-RESEARCH-V1.md, hmm-implementation-v1.md, ccxt-binance.md
- scripts/check_db.py, scripts/test_ingestion.py, scripts/verify_hmm.py, walkthrough.md
- handoff-session-6.md (prior report) and this handoff-session-7.md

## 10) Untracked / leave uncommitted
- tradecore.duckdb, tradecore.duckdb.wal (DB) — keep untracked/locked by server
- backend.log (keep untracked)

## 11) If you need to inspect data immediately
- Stop uvicorn to free DuckDB, then `duckdb tradecore.duckdb` and query `market_data`.
- To check latest 1m timestamp: `select max(timestamp) from market_data where exchange='binance' and symbol='BTC/USDT' and timeframe='1m';`
- Restart backend afterward with `bash scripts/run_api.sh`.

