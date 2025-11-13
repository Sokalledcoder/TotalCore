# Fetch‑History UI & API Spec (Kraken via CCXT)

## Goals
- Let users request historical OHLCV data (initially Kraken spot BTC/USD and ETH/USD) through a simple form.
- Queue/monitor ingestion jobs driven by our CCXT downloader.
- Surface coverage metadata (what’s already stored) and allow incremental refreshes or data downloads.

## User Flow
1. Navigate to **Data > Fetch History**.
2. Fill the form:
   - **Exchange**: dropdown from `data_sources` (initially only `kraken`).
   - **Pair**: dropdown filtered by exchange (BTC/USD, ETH/USD for now, but fed by `markets` table later).
   - **Timeframe**: dropdown of allowed CCXT intervals (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 2w).
   - **Date range**: start/end pickers (UTC). Optional “Full history” toggle sets `start = earliest_known`.
   - **Seed via official ZIP** (checkbox, default on): use Kraken’s OHLCVT dump if available before REST pagination kicks in.
3. Click **Fetch** → POSTs a `data_jobs` entry. UI immediately shows job card: status (queued/running/completed/failed), submitted range, requested timeframe.
4. Job runner updates status/progress (e.g., “42% – fetched up to 2021‑06‑01 12:00 UTC”). Front-end polls `GET /data-jobs/{id}` every few seconds.
5. When done:
   - Show summary (rows ingested, actual start/end stored, any gaps flagged).
   - Provide buttons: **Download Parquet**, **Download CSV**, **Run Validation**, **Link to RL dataset**.
6. Coverage table on the same page lists each stored `(exchange, pair, timeframe)` with `start_ts`, `end_ts`, last sync date, and actions (refresh/resume/download).

## API Endpoints

### POST `/api/data-jobs`
Payload:
```json
{
  "exchange": "kraken",
  "symbol": "BTC/USD",
  "timeframe": "1m",
  "start_timestamp": "2015-01-01T00:00:00Z",
  "end_timestamp": "2025-11-12T00:00:00Z",
  "options": {
    "seed_from_zip": true,
    "full_history": false
  }
}
```
Response: job record `{id, status, submitted_at}`.

Validation rules:
- verify exchange/pair/timeframe exist in metadata tables.
- enforce reasonable max range per request (e.g., 5 years for 1m to avoid runaway storage).

### GET `/api/data-jobs/{id}`
Returns job status:
```json
{
  "id": "job-uuid",
  "status": "running",
  "progress": 0.42,
  "details": {
    "last_timestamp": "2021-06-01T12:00:00Z",
    "batches_completed": 123,
    "messages": ["Fetched 720 candles per call", "Rate limit hit, backing off"]
  },
  "result": {
    "rows": 1234567,
    "start_timestamp": "2013-09-10T00:00:00Z",
    "end_timestamp": "2025-11-12T00:00:00Z",
    "artifacts": [{"type": "parquet", "path": "s3://..."}]
  }
}
```

### GET `/api/data-coverage?exchange=kraken&symbol=BTC/USD`
Returns current ranges per timeframe:
```json
[
  {
    "timeframe": "1m",
    "start_timestamp": "2013-09-10T00:00:00Z",
    "end_timestamp": "2025-11-12T00:00:00Z",
    "last_job_id": "job-uuid",
    "validated_at": "2025-11-12T05:00:00Z"
  },
  ...
]
```

### POST `/api/data-jobs/{id}/actions`
Handle actions like `validate`, `resume`, `download`. Payload: `{ "action": "validate" }`.

## Job Runner Expectations
- Resolve CCXT symbol via `exchange.market(symbol)` mapping. Persist human-readable label alongside raw ID.
- If `seed_from_zip` true and local cache missing, download Kraken’s OHLCVT ZIP for the pair, store raw CSV -> Parquet.
- After seeding or when `start_timestamp` > available ZIP range, run REST pagination loop:
  - default batch size 720 candles (Kraken limit) unless user overrides `maxEntriesPerRequest`.
  - use CCXT `fetch_ohlcv` (with `paginate` option or manual loop) until `start_timestamp` satisfied or API stops returning data.
  - obey `enableRateLimit`; if Kraken returns 520/525 errors, back off and retry up to N times.
- Write Parquet partitions grouped by `exchange/pair/timeframe/year`.
- Emit `data_job_events` for each milestone so UI can stream updates (optional).

## UX Notes
- Show warnings inline (e.g., “REST API only returns 720 candles per call; long ranges may take time”).
- Pre-fill form with latest stored `start` (for refresh) when coverage exists.
- Provide quick links to documentation about rate limits, 720-cap, etc.

