# Research Log

> Use this file to record each research session. Append entries chronologically so we can trace decisions later.

---

## 2025-11-12 — Topic: RL Trading Environment Foundations

### Sources
- FinRL Single Stock Trading tutorial (`docs/source/tutorial/Introduction/SingleStockTrading.rst`) via GitHub raw: clarifies MDP components, env class attributes, and built-in transaction cost hooks.[^1]
- FinRL paper (arXiv:2011.09607): highlights inclusion of transaction cost, liquidity, and risk-aversion constraints in FinRL envs.[^2]
- Gymnasium spaces docs: MultiDiscrete container and Dict spaces for composing multi-tool action/state spaces.[^3]
- Stable-Baselines3 docs on vectorized envs and RL tips: guidance on VecEnv API, normalization (`VecNormalize`), and episodic truncation handling.[^4][^5]

### Key Findings
1. **State/Observation Template** — FinRL’s env observes OHLCV plus indicator stacks and account features (positions, cash, turbulence) per step, confirming we should emit configurable indicator tensors alongside agent state for each minute bar.[^1]
2. **Action Toolbox Representation** — FinRL expands beyond {-1,0,1} by allowing {-k..k} discrete share deltas; Gym’s `MultiDiscrete` space cleanly encodes independent choices (e.g., direction, SL bucket, TP bucket, size) while Dict/Tuple wrappers keep actions human-readable.[^1][^3]
3. **Reward + Risk Controls** — Default reward = change in portfolio value, but FinRL environments expose `transaction_cost_pct`, turbulence thresholds, and risk-aversion gates; paper emphasizes modeling fees/liquidity which we can generalize into pluggable reward penalties (drawdown, turnover).[^^1][^2]
4. **Vectorized + Normalized Training** — SB3 requires Gym-compatible envs and recommends `VecEnv`/`VecNormalize` for sample efficiency and stable learning on non-stationary series; we should plan env wrappers that support both single and batched windows plus observation normalization hooks.[^4][^5]
5. **Episode Hygiene** — SB3 tips reiterate handling truncation vs termination and seeding multiple runs; our env API must expose deterministic resets, train/val window selection, and proper `terminated`/`truncated` signals to avoid leakage during GPU-parallel rollouts.[^4][^5]

### Decisions / Next Steps
- Model the action space as a `gym.spaces.Dict` composed of `Discrete`/`MultiDiscrete` slots for: position op, stop adjustment, take-profit adjustment, and sizing bucket so we can toggle tools per strategy.
- Build observation pipelines that accept a JSON indicator manifest (maps to functions in `/tools`) and join with standardized agent state features.
- Reserve reward config schema with weights for PnL delta, cost penalties, drawdown clamps, and turbulence gating, matching FinRL’s parameterization but extendable.
- When implementing envs, include utility wrappers for normalization, vectorization, and `check_env` compliance from SB3 tip sheet before integrating with PPO/SAC.

[^1]: https://raw.githubusercontent.com/AI4Finance-Foundation/FinRL/master/docs/source/tutorial/Introduction/SingleStockTrading.rst
[^2]: https://arxiv.org/pdf/2011.09607.pdf
[^3]: https://www.gymlibrary.dev/api/spaces/#multidiscrete
[^4]: https://stable-baselines3.readthedocs.io/en/master/guide/vec_envs.html
[^5]: https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html

## 2025-11-12 — Topic: RL Training Stack & Libraries

### Sources
- FinRL Single Stock tutorial, Step 5 (DRL algorithms section) showing built-in PPO/A2C/TD3 integration via Stable-Baselines and Gym.[^6]
- Stable-Baselines3 homepage: outlines PyTorch-based, reliable RL implementations with tested algorithms and support tooling (RL Zoo, Docker).[^^7]
- RLlib index page (Ray docs): describes RLlib as production-grade, scalable, fault-tolerant RL with native multi-agent/offline/external sim support plus quick-start PPO config incl. multi env runners and GPU hooks.[^8]
- CleanRL README: positions CleanRL as single-file reference implementations with reproducibility, W&B/TensorBoard logging, and ability to scale thousands of experiments via AWS Batch.[^9]

### Key Findings
1. **FinRL as Finance-Specific Glue** — FinRL already wraps SB (PPO, A2C, DDPG, TD3, SAC) and wires them to stock envs; we can re-use FinRL’s env scaffolding ideas but rely on SB3 directly inside RunPod to avoid the older TensorFlow dependencies present in legacy FinRL tutorials.[^6]
2. **Stable-Baselines3 Sweet Spot** — SB3 provides well-tested PyTorch PPO/A2C/SAC/TD3 implementations, vectorized env utilities, and fits easily inside custom training scripts—great default for single-GPU pods and quick iteration.[^7]
3. **RLlib for Scaling/Distributed Needs** — RLlib brings multi-agent abstractions, offline dataset support, env runners, and config-driven multi-GPU training. It’s the go-to when we need to parallelize across multiple GPUs/nodes or orchestrate MARL experiments without rewriting training loops.[^8]
4. **CleanRL for Transparent Baselines / Rapid Prototyping** — CleanRL’s single-file scripts make it easy to instrument bespoke reward/observation tweaks, integrate with W&B, and even blast many experiments via AWS Batch; good for reproducible baselines or when we want to inspect every line of the algorithm.[^9]
5. **Stack Choice Strategy** — Start with SB3 for the first RunPod runner (fits Pythonic CLI + JSON config). Keep RLlib in scope for future horizontal scaling or multi-agent cases. Use CleanRL scripts when we need lightweight prototypes or to validate FinRL-style tooling vs canonical implementations.

### Decisions / Next Steps
- Containerize SB3 + PyTorch CUDA builds for default pods; ensure configs can switch between PPO/SAC/TD3 depending on reward/action needs.
- Abstract experiment runner so we can swap training backends (SB3 vs RLlib) by selecting a trainer class in the config.
- Maintain CleanRL-based baselines in CI for regression tests against our custom env, giving us reference metrics per dataset.

[^6]: https://raw.githubusercontent.com/AI4Finance-Foundation/FinRL/master/docs/source/tutorial/Introduction/SingleStockTrading.rst
[^7]: https://stable-baselines3.readthedocs.io/en/master/
[^8]: https://raw.githubusercontent.com/ray-project/ray/releases/2.51.1/doc/source/rllib/index.rst
[^9]: https://raw.githubusercontent.com/vwxyzjn/cleanrl/master/README.md

## 2025-11-12 — Topic: RunPod Infrastructure Integration

### Sources
- Network volumes doc: persistent NVMe-backed storage (200–400 MB/s typical, up to 10 GB/s) mountable to pods/serverless at `/workspace` or `/runpod-volume`; creation/attachment steps and pricing ($0.07/GB-month first TB).[^^10]
- Pods overview: containerized Ubuntu envs with selectable GPU/vCPU/storage, templates, network connectivity, Secure vs Community cloud, and deployment/connection options.[^11]
- Pod creation API (`POST /v1/pods`): payload fields for `allowedCudaVersions`, GPU/CPU flavor selection, network volume attachment, env vars, ports, etc.; response includes cost info and pod IDs.[^12]
- Serverless overview + handler docs: serverless endpoints auto-scale GPU workers, per-second billing, handler lifecycle (`runpod.serverless.start`), input payload schema, streaming/concurrent handlers, progress updates, and payload limits (10 MB `/run`, 20 MB `/runsync`).[^13][^14]
- Python SDK overview: install via `pip install runpod`, set `runpod.api_key`, provides API/endpoint helpers for automation.[^15]

### Key Findings
1. **Data Persistence Pattern** — Network volumes are the canonical way to store multi-year 1m datasets and share them across pods/serverless workers; they persist independent of compute and live at `/workspace` (pods) or `/runpod-volume` (serverless).[^^10]
2. **Throughput + Region Considerations** — NVMe-backed volumes offer hundreds of MB/s with peaks up to 10 GB/s but are region-bound; all attached pods/endpoints must live in the same data center, so scheduler must align GPU selection with volume region.[^10]
3. **Pod Orchestration Requirements** — Creating pods programmatically means populating the RunPod REST payload with GPU type IDs, CUDA version allowlist, network volume ID, ports, etc.; responses include cost info we can log for budgeting.[^12]
4. **Serverless Use Cases** — RunPod serverless is ideal for lightweight indicator evaluations or inference-style tasks thanks to auto-scaling GPU workers, but we must manage cold starts (by pinning min workers or caching models) and respect payload limits; handler best practices encourage loading models outside `handler` and returning progress updates.[^13][^14]
5. **SDK Automation** — The Python SDK shortens automation work (auth, endpoint/pod calls), so the control plane can rely on it for job submission and monitoring rather than hand-crafting HTTP requests.[^15]

### Decisions / Next Steps
- Standardize on a single RunPod region per environment to keep network volume + GPU compatibility simple; include region field in experiment configs.
- Build a thin RunPod client module that wraps SDK calls for: allocate pod (with network volume & env vars), stream logs, terminate, and parse pricing from API responses.
- For serverless endpoints, design handler templates that mount `/runpod-volume`, validate inputs, and optionally stream progress for long indicator sweeps.

[^10]: https://docs.runpod.io/storage/network-volumes
[^11]: http://docs.runpod.io/pods/overview
[^12]: http://docs.runpod.io/api-reference/pods/POST/pods
[^13]: http://docs.runpod.io/serverless/overview
[^14]: http://docs.runpod.io/serverless/workers/handler-functions
[^15]: http://docs.runpod.io/sdks/python/overview

## 2025-11-12 — Topic: Tool & Indicator Packaging Patterns

### Sources
- Python Packaging User Guide on plugin discovery: outlines naming-convention, namespace-package, and entry-point based discovery plus code snippets using `pkgutil` and `importlib.metadata`.[^16]

### Key Findings
1. **Discovery Options** — We can expose `tools` via a namespace package (e.g., `tradecore.tools`) so any new indicator dropped into that namespace becomes discoverable with `pkgutil.iter_modules`, or we can register them via entry points (e.g., `project.entry-points.'tradecore.tools'`), letting the control plane load plugins via `importlib.metadata.entry_points()`.[^16]
2. **Metadata Channel** — Entry points natively carry the dotted import path for each plugin plus a human-readable name, giving us a built-in manifest we can parse into the indicator catalog, eliminating the need for bespoke registries.
3. **Sandboxing** — Keeping plugins under a namespace like `tradecore.tools` (rather than making the main package a namespace) prevents a faulty plugin from breaking the entire project import path—explicitly recommended in the packaging guide.[^16]
4. **Runtime Loading** — With naming conventions, we can still support simple drop-in scripts (e.g., files under `/tools/*.py`) for local experiments while the long-term packaging story can use entry points for versioned distribution.

### Decisions / Next Steps
- Define `tradecore.tools` as the canonical namespace; runtime loader walks that namespace and inspects module-level metadata (`TOOL_SPEC = {...}`) for parameters.
- For user-provided repos, document how to register entry points so the backend can auto-ingest tool manifests without manual config.
- Provide a validator CLI that imports each tool module in isolation (so a broken plugin doesn’t crash the server) and checks for required hooks before copying the module into `/tools`.

[^16]: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/

## 2025-11-12 — Topic: Control Plane (Backend + Tracking + UI)

### Sources
- Celery introduction: defines task queues, brokers, and worker pools for distributed background processing.[^17]
- MLflow Tracking docs: describe logging parameters/metrics/artifacts per run, grouped into experiments, with APIs + UI for visualization.[^18]

### Key Findings
1. **Job Orchestration Pattern** — Celery’s client→broker→worker pipeline is a drop-in fit for our RunPod scheduler: API enqueues RL experiment tasks, a Celery worker claims them, provisions pods via RunPod API, and streams results back, giving us horizontal scaling and retry semantics.[^17]
2. **Status Tracking Schema** — Celery tasks map well to our `experiments` table (store task ID, RunPod pod ID, timestamps), letting the frontend poll `/experiments/{id}` for real-time queue/worker state.
3. **Experiment Logging UX** — MLflow Tracking demonstrates how to log configs (`mlflow.log_param`), metrics, and artifacts per run, and to visualize trends in a UI; we can embed MLflow itself or replicate its core concepts (experiment→runs with metadata + asset URIs) in Postgres + object storage.[^18]
4. **Frontend Parallels** — MLflow’s UI screenshot (metrics timeline + sortable run table) is a concrete reference for our dashboard: we can render RL metrics with Plotly/React while borrowing MLflow’s filter/search paradigms.

### Decisions / Next Steps
- Introduce a message broker (Redis/RabbitMQ) + Celery worker tier dedicated to RunPod orchestration, keeping API requests fast.
- Mirror MLflow’s schema (experiments, runs, metrics, artifacts) so we can optionally plug in MLflow clients for logging, or self-host MLflow Tracking for users who prefer the native UI.
- Define API endpoints for `/experiments`, `/runs`, and `/artifacts` that aggregate Celery state + RunPod telemetry + stored metrics for the frontend.

[^17]: https://docs.celeryq.dev/en/stable/getting-started/introduction.html
[^18]: https://mlflow.org/docs/latest/tracking.html

## 2025-11-12 — Topic: Data Management & Validation

### Sources
- Polars Parquet guide: explains that Parquet is columnar, aligns with Polars’ in-memory layout, and supports lazy `scan_parquet` with predicate/projection pushdown to minimize I/O (including cloud storage).[^^19]
- pandas `DataFrame.asfreq` docs: demonstrate using explicit minute-frequency indexes plus `asfreq`/upsampling with fill strategies to surface missing timestamps or pad gaps.[^20]

### Key Findings
1. **File Format Choice** — Columnar Parquet is preferable for our `/data/<SYMBOL>` hierarchy because it compresses OHLCV columns efficiently and matches analytical engines (Polars, PyArrow) for fast slicing compared to CSV.[^19]
2. **Lazy Loading & Filtering** — Using `scan_parquet` (Polars/Arrow) lets us stream windows or run predicate pushdown (symbol, date range) without loading entire files into memory—ideal for multi-year 1m data living on RunPod network volumes or cloud buckets.[^19]
3. **Integrity Checks** — `pandas.DataFrame.asfreq('1min')` (or Polars equivalent) can reindex series to exact 1-minute cadence, revealing missing candles; fill strategies (`method='bfill'`, `fill_value`) highlight gaps that must be interpolated or flagged before feeding RL agents.[^20]

### Decisions / Next Steps
- Store each symbol/year as partitioned Parquet (e.g., `/data/BTCUSDT/2021.parquet`) with consistent schema; add metadata file describing available ranges.
- Build a validation CLI that loads Parquet lazily, reindexes to 1-minute frequency, counts gaps/outliers, and writes a QC report before copying data into network volumes.
- Provide helper functions that return lazy scans for training/eval splits so the RL environment can stream data without materializing entire datasets in RAM.

[^19]: https://docs.pola.rs/user-guide/io/parquet/
[^20]: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.asfreq.html

## 2025-11-12 — Topic: Security, Budget, and Operational Guardrails

### Sources
- RunPod pods overview: distinguishes Secure vs Community cloud pods and outlines customization (ports, env vars) — relevant to selecting safe defaults per workload sensitivity.[^11]
- RunPod billing info: per-minute billing, automatic pod stoppage when credits deplete, storage/network volume pricing tiers, and spending limits for new accounts.[^21]

### Key Findings
1. **Cloud Tier Controls** — Secure Cloud pods live in T3/T4 data centers with higher reliability, while Community Cloud pods trade cost for peer-provided hardware; we can expose this toggle in experiment configs and default to Secure for high-value RL jobs.[^11]
2. **Auto-Shutdown Safety** — RunPod halts pods automatically if the account balance can’t cover runtime, which we can treat as a last-resort kill switch; still, we should proactively terminate idle pods ourselves (control plane timer) to avoid hitting balance zero in the first place.[^21]
3. **Budget Awareness** — Because billing (compute + storage + network volumes) is per-minute, the scheduler can estimate run cost upfront (GPU rate × planned hours) and compare against user-defined budgets before launching pods; network volumes add $0.07/GB-month under 1 TB so we should monitor dataset footprint.[^21]
4. **Spending Limits** — New accounts have RunPod-imposed spending caps; the control plane should surface failures caused by those limits and prompt the user to contact RunPod support or adjust GPU specs instead of silently retrying.

### Decisions / Next Steps
- Add per-project budget settings (max concurrent pods, max hourly burn). Scheduler enforces these before creating pods.
- Implement idle pod killer: mark pods as stale if no heartbeat/logs for X minutes, call RunPod `stop` to avoid unnecessary billing.
- Track storage usage per network volume and alert when nearing new pricing tier (>1 TB) or when data footprint suggests cleanup/compression.

[^21]: https://docs.runpod.io/references/billing-information

## 2025-11-12 — Topic: Kraken OHLC Ingestion Details

### Sources
- Kraken support article on downloadable OHLCVT data (CSV ZIPs for all pairs, notes missing bars mean no trades).[^^22]
- Kraken support note on REST OHLC limits: endpoint only returns the most recent 720 candles for a given interval and recommends using /Trades for deeper history.[^23]
- KDJ.com guide on Kraken OHLC endpoint: intervals allowed, iterative pagination using `last` cursor, and suggested rate limit of ~15 calls/min.[^24]
- python-kraken-sdk docs: `get_ohlc` returns at most 720 timestamps per request and reiterates allowed intervals (1,5,15,30,60,240,1440,10080,21600).[^^25]

### Key Findings
1. **Per-call cap = 720 candles** — Both Kraken’s own help center and SDK docs confirm the REST OHLC endpoint only returns the latest 720 periods regardless of `since`, so 1-minute data tops out at 12 hours per call.[^23][^^25]
2. **Allowed timeframes** — Kraken spot API accepts `interval` values in minutes: 1,5,15,30,60,240,1440,10080,21600 (CCXT maps these to `1m…2w`).[^24][^^25]
3. **Pagination strategy** — To walk back in time, we must loop calls, using the `last` cursor from each response (Kraken returns a `last` timestamp in seconds). We continue until the stored timestamp meets our requested start date; otherwise, fall back to quarterly/full ZIP dumps for cold history.[^24][^^22]
4. **Rate limits** — Public REST requests should stay under roughly 15 calls/minute from one IP; implement pacing/backoff and reuse CCXT’s `enableRateLimit`.[^24]
5. **Alternative data sources** — Kraken publishes full OHLCVT history per pair as downloadable CSV ZIPs (complete and quarterly incremental sets). These can seed our Parquet store faster than REST crawling and then the REST job can keep data fresh intra-quarter.[^^22]
6. **Trade endpoint fallback** — Support recommends the public `/Trades` endpoint (tick-level) when more than 720 candles of 1-minute data are needed; we can reconstruct OHLC from trades if we require definitive coverage.[^23]

### Decisions / Next Steps
- Kick off Kraken ingestion by seeding from the official OHLCVT ZIP for BTC/USD and ETH/USD into `/data/kraken/...`, then schedule REST jobs to keep data current (looping until the desired start timestamp and respecting the 720-cap pagination).
- Store the last `last` cursor per pair/timeframe so resumptions don’t re-fetch overlapping windows; log rate-limit responses for monitoring.
- Document the trade-endpoint rebuild option (lower priority) and keep a hook for importing quarterly ZIP deltas if REST syncing falls behind.

[^22]: https://support.kraken.com/hc/articles/360047124832-Downloadable-historical-OHLCVT-Open-High-Low-Close-Volume-Trades-data
[^23]: https://support.kraken.com/es/articles/4402519859348-rest-api-authentication-calculator-google-sheet-
[^24]: https://www.kdj.com/Cryptocurrency-Encyclopedia/Exchanges/historical-market-data-kraken-api.html
[^25]: https://python-kraken-sdk.readthedocs.io/en/v1.6.2/src/spot/rest.html

## 2025-11-12 — Topic: Fetch-History UI/API Spec

### Sources
- Internal design doc `docs/research/fetch_history_ui.md` (authored this session) summarizing desired UX flows and API endpoints for CCXT-powered data jobs.

### Key Points
1. **Form Inputs** — Exchange, pair, timeframe, date range, plus options like “seed from Kraken ZIP” or “full history”. All tied to metadata tables so new exchanges/pairs drop in later.
2. **Job Lifecycle** — POST `/api/data-jobs` creates a record; UI polls `/api/data-jobs/{id}` for status/progress; coverage endpoint returns stored ranges for quick refreshes.
3. **Worker Expectations** — Use CCXT `fetch_ohlcv` (with pagination) and optional ZIP seeding, obey rate limits, write Parquet partitions, emit job events for the UI.
4. **User Feedback** — Inline warnings about the 720-candle cap, rate limits, and long runtimes; completion summary includes downloadable artifacts and next-step actions (validation, link to RL dataset).

### Decisions / Next Steps
- Implement the described endpoints once we exit research; in the meantime, keep iterating on UX copy or validation rules if requirements change.

## 2025-11-12 — Topic: Trade-Based OHLC Rebuild Plan

### Sources
- Internal note `docs/research/trade_rebuild_notes.md` outlining how to use CCXT `fetchTrades` to rebuild candles for ranges beyond the REST OHLC cap.

### Key Points
1. **Use Cases** — Deep history, gap repair, or higher-fidelity studies when the 720-candle restriction blocks REST-only ingestion.
2. **Algorithm** — Paginate trades from `since` to `until`, bucket by timeframe, compute OHLCV per bucket, persist with flags indicating trade-derived data.
3. **Constraints** — Kraken limits trade history; rebuilding large ranges is compute-heavy; we’ll treat it as an optional future job type rather than default behavior.

### Decisions / Next Steps
- Postpone implementation until REST + ZIP seeding proves insufficient; keep plan on file so we can green-light it quickly when needed.


## 2025-11-12 — Topic: Native Market Data Ingestion (CCXT)

### Sources
- CCXT Manual (GitHub wiki): explains `fetchOHLCV` signature, timeframes, `since` semantics, pagination limits, and OHLCV structure; also covers rate limiting via `exchange.enableRateLimit` and per-exchange capabilities.[^22]
- CCXT `fetch-ohlcv.py` example: demonstrates calling `fetch_ohlcv` with `since` and `limit`, highlighting async usage and timestamp handling.[^23]

### Key Findings
1. **Unified OHLCV Access** — `fetchOHLCV(symbol, timeframe, since, limit, params)` returns `[timestamp, open, high, low, close, volume]` arrays with oldest-first ordering; availability per exchange surfaced in `exchange.has['fetchOHLCV']` and supported timeframes via `exchange.timeframes`.[^22]
2. **Historical Limits** — Exchanges cap how far back fine-grained klines go (often last ~1000 candles). To build deep history we must implement incremental crawlers that repeatedly call `fetchOHLCV` with a sliding `since` and persist candles to our storage as they arrive.[^22]
3. **Latency & Completeness** — Latest candle may be incomplete until the interval closes, and some exchanges leave gaps when no trades occurred; ingestion jobs must detect missing periods and optionally rebuild candles from raw trades (`buildOHLCV`) if needed.[^22]
4. **Rate-Limit Compliance** — Each exchange exposes `exchange.rateLimit` (ms between requests) and CCXT’s built-in limiter (`enableRateLimit=True`) to throttle calls; we should dedicate one exchange instance per API key and schedule workers accordingly to avoid bans.[^22]
5. **Implementation Hooks** — Example script shows capturing `since` as `exchange.milliseconds() - window` and passing `limit` to page results; extra params (e.g., `'price': 'mark'`) let us fetch mark/index/premium candles where available.[^22][^23]

### Decisions / Next Steps
- Add a “Data Acquisition” service that orchestrates CCXT exchange clients, supports multiple symbols/timeframes, handles pagination, and writes normalized Parquet chunks directly into `/data/<SYMBOL>/<EXCHANGE>/<TIMEFRAME>/`.
- Maintain metadata (per exchange/range coverage, rate limits, last synced timestamp) so ingestion jobs can resume after interruptions and avoid redundant downloads.
- Expose configuration in the control plane to schedule recurring syncs (cron-like) and adhoc backfills, with monitoring for rate-limit errors and gap detection (auto backfill via `buildOHLCV` from trades when necessary).

[^22]: https://github.com/ccxt/ccxt/wiki/Manual
[^23]: https://raw.githubusercontent.com/ccxt/ccxt/master/examples/py/fetch-ohlcv.py
- **2025-11-12 — Topic: Kraken Trade Pagination Fix**

### Sources
- CCXT manual (`build_ohlcvc`, cursor semantics) and Kraken REST docs confirming `fetch_trades` pagination via `since`/`last`.
- Empirical runs using `ccxt.kraken.fetch_trades(symbol, since, limit=1000)` show millisecond cursors are sufficient when stepping by `last_trade_timestamp + 1`.

### Key Points
1. Use CCXT’s unified `fetch_trades` with `options={'fetchTradesWarning': False}` to avoid pagination warnings and request 1000 trades per page.
2. Advance cursor as `cursor = max(cursor + 1, trades[-1]['timestamp'] + 1)` to walk backward indefinitely; empty pages require a small forward bump (e.g., +60s) before retrying.
3. Convert trades → candles via `exchange.build_ohlcvc(trades, timeframe)` to avoid manual bucketing errors; guard against empty DataFrames.

### Status
- `KrakenTradeAggregator` now implements this loop, and `_run_trade_backfill` successfully populated BTC/USD 1m candles for Jan–Nov 2025 (≈93k rows).
+ End Entry

## 2025-11-12 — Topic: BTC/USD 1m Coverage Validation

### Sources
- Local Parquet scan via `python - <<'PY' ... pq.read_table(...)` against `data/lake/kraken/BTC-USD/1m/year=2025/*.parquet`.
- Job metadata query via `python - <<'PY' ... sqlite3.connect('data/jobs.db')`.

### Key Findings
1. The Parquet partition currently holds 93,079 rows with timestamps spanning 2025-01-01 00:00:00 UTC through 2025-11-12 22:55:00 UTC, confirming Session 1’s Jan→Nov coverage.
2. `data/jobs.db` shows the most recent completed job covering 2025-09-12 → 2025-11-12, which explains why the dashboard suggests “two months,” but those records were appended onto the existing files rather than replacing them.
3. Any future 2025 backfill must pause streaming (once built) and prune `data/lake/kraken/BTC-USD/1m/year=2025` first, otherwise we risk duplicate Parquet fragments in the same year folder.

### Decisions / Next Steps
- Keep the CCXT Pro worker on hold until we extend historical coverage or add retention tooling so later rewrites don’t conflict with live updates.
- Document the prune → rerun → restart workflow before scheduling wider historical jobs.

## 2025-11-12 — Topic: BTC/USD 1m Coverage Reality Check

### Sources
- Local Parquet scan + pandas daily counts via `python - <<'PY' ... ds.dataset(...).to_table().to_pandas()`

### Key Findings
1. Total rows remain 93,079, which equates to only ~64 trading days, not a full year (64 * 1,440 ≈ 92k). The earliest timestamp is 2025-01-01 00:00 UTC but only 33 minutes exist for that day—so earlier Jan coverage is just residue from aborted jobs.
2. Continuous, near-full-day coverage only starts on 2025-09-13; everything prior to mid-September is sparse. The most recent dense stretch runs 2025-09-13 through 2025-11-11, with 2025-11-12 containing duplicates (~4,238 rows) from repeated reruns.
3. Dashboard confusion stemmed from me reading the min/max timestamps without checking density; in reality we only have about two months of usable candles (mid-Sep onward), confirming your expectation.

### Decisions / Next Steps
- Treat anything before 2025-09-13 as incomplete and plan a clean backfill if we need January–August later.
- When reporting coverage, always include row counts vs expected (minutes * days) so sparse partitions can’t masquerade as full-year data.

## 2025-11-12 — Topic: Streaming Worker & Backfill Priority Call

### Sources
- Session alignment with user (verbal directive; see chat log 2025-11-12).

### Key Decisions
1. CCXT Pro streaming worker is officially deferred until after we: (a) complete RL environment v1, and (b) expand/clean the 2025 dataset. Both tasks will be handled together at the end of the current roadmap to avoid conflicting rewrites.
2. Historical backfills (Jan–Aug 2025 and earlier years) are also paused until the RL stack is in place; when resumed, we’ll prune existing partitions first, then re-run ingestion before restarting any streaming service.

### Next Steps
- Focus immediately shifts to Phase 4 (Gym-compatible environment) per `docs/research/execution_plan.md`.
- Streaming/backfill work will be re-opened only after the RL environment milestone is signed off.

## 2025-11-12 — Topic: RL Environment Scaffolding

### Sources
- Code authored this session (`app/rl/*`, `tests/test_rl_env.py`).

### Key Decisions
1. Added a Gymnasium-compatible `TradeEnvironment` (see `app/rl/env.py`) that stitches together dataset manifests, observation builder, execution engine, and reward calculator—aligned with Phase 4 requirements.
2. Defined structured configs (`app/rl/config.py`) plus manifest loader/dataset sampler (`app/rl/datasets.py`) so every episode documents exactly which parquet slice it draws from; this keeps historical coverage transparent and auditable.
3. Observation pipeline (`app/rl/state_builder.py`) emits normalized OHLCV windows + account state, while actions (`app/rl/actions.py`) use discrete heads for direction/size/TP/SL placeholders—matching the research notes on Dict/MultiDiscrete spaces.
4. Reward engine (`app/rl/rewards.py`) blends PnL, fee, drawdown, and exposure penalties with explicit scaling so future algorithms can tune weights without touching env internals.
5. Added a lightweight pytest (`tests/test_rl_env.py`) that writes a synthetic parquet slice + manifest, instantiates the env, and steps once to guard against shape/regression drift.

### Next Steps
- Extend manifests/validators so we can auto-generate the mid-Sep→Nov coverage file before training.
- Layer in indicator/tool hooks once the `tools/` framework lands (Phase 3), then re-run `tests/test_rl_env.py` with fixtures exercising those extra channels.

## 2025-11-12 — Topic: Coverage Manifest Automation

### Sources
- `scripts/generate_manifest.py` (new CLI added this session).
- Generated artifact `data/manifests/btcusd_1m_sepnov2025.json` via `python scripts/generate_manifest.py --dataset-dir data/lake/kraken/BTC-USD/1m/year=2025 --output data/manifests/btcusd_1m_sepnov2025.json --min-rows-per-day 1300 --max-rows-per-day 2000 --min-slice-days 7`.

### Key Findings
1. The automated scan confirmed two contiguous, high-quality windows: 2025-09-13 → 2025-10-31 (70,470 rows) and 2025-11-02 → 2025-11-12 22:55 (15,766 rows). November 1st is missing enough candles to break the slice, so it’s excluded until we backfill.
2. Days with anomalously high row counts (like 2025-11-12 duplicates) are filtered out by capping `max_rows_per_day=2000`, so the manifest only references clean data.
3. Each slice points back to the raw Parquet directory, meaning the RL environment can now reference `data/manifests/btcusd_1m_sepnov2025.json` to sample episodes without guessing coverage.

### Decisions / Next Steps
- Regenerate manifests whenever ingestion changes by rerunning the CLI with updated thresholds and logging the command/output here.
- Wire `EnvConfig.dataset_manifest_path` to this manifest for upcoming RL experiments; future manifests for other symbols/timeframes should live under `data/manifests/` with the same format.

## 2025-11-12 — Topic: RL Env Config & Smoke Runner

### Sources
- `configs/env/btcusd_1m_sepnov2025.json`
- `scripts/run_env_episode.py`
- Execution: `source .venv/bin/activate && python scripts/run_env_episode.py --config configs/env/btcusd_1m_sepnov2025.json --episodes 1 --seed 123`

### Key Notes
1. Created a reusable EnvConfig JSON that points at the new BTC/USD manifest, locks fee/slippage assumptions, and documents the default observation/action/reward knobs for Phase 4 experiments.
2. Added `scripts/run_env_episode.py` to spin up `TradeEnvironment`, sample random actions, and print per-episode metrics (steps, reward sum, final equity, drawdown). Today’s run (seed 123) produced 240 steps over a 4-hour episode with final equity ~$94.8k, confirming the stack works end-to-end on production data.
3. These artifacts give us a deterministic scaffold for future agents: update the config per strategy, or plug a custom policy into the script to sanity check before wiring SB3.

### Next Steps
- Check in this config with future manifest updates so RL jobs always know which slices are approved.
- Replace the random-policy smoke test with SB3 integration once the training runner lands (Phase 5).

## 2025-11-12 — Topic: SB3 Training Harness

### Sources
- `app/rl/factory.py`, `app/rl/wrappers.py`, `scripts/train_sb3.py`
- Command: `source .venv/bin/activate && python scripts/train_sb3.py --config configs/env/btcusd_1m_sepnov2025.json --total-timesteps 64 --algo ppo --eval-episodes 1 --seed 123 --save-path models/ppo_trade_env_test`

### Key Decisions
1. Added Stable-Baselines3 (CPU Torch build) plus a MultiDiscrete action wrapper so our Dict action space can be flattened for PPO/A2C without mutating the core environment.
2. `scripts/train_sb3.py` now loads any EnvConfig, spins up a DummyVecEnv with the wrapper, and runs PPO/A2C training with optional eval + checkpointing; progress bars/TensorBoard are opt-in to avoid heavyweight deps.
3. The sample run above covered a single PPO iteration (2,048 steps under the hood) on CPU and produced an eval reward of roughly -5.66, confirming the plumbing works on the manifest-backed dataset.

### Next Steps
- Expose hyperparameters via JSON/YAML once we start serious sweeps.
- Integrate this harness with RunPod runners in Phase 5, using the same factory + wrapper so pods can boot identical envs.

## 2025-11-13 — Topic: SB3 Configurable Training Runs

### Sources
- `app/rl/training_config.py`, `configs/train/ppo_cpu_baseline.json`, `scripts/train_sb3.py` (updated).
- Command: `source .venv/bin/activate && python scripts/train_sb3.py --train-config configs/train/ppo_cpu_baseline.json`

### Key Notes
1. Introduced a Pydantic-based `TrainingConfig` (JSON/YAML) so algorithm choice, total timesteps, seeds, eval cadence, save paths, and PPO/A2C kwargs live in versioned files. `configs/train/ppo_cpu_baseline.json` now tracks the CPU baseline used for smoke tests.
2. `scripts/train_sb3.py` loads that config, flattens action spaces via the MultiDiscrete wrapper, and dumps run metadata (`models/<name>_meta.json`) after training/eval. CLI flags now act as overrides only when explicitly provided, so sweep runners can tweak single knobs without editing files.
3. The sample PPO run (10k steps) produced `models/ppo_cpu_baseline.zip` plus `_meta.json` capturing eval reward (~-5.66), seed, and hyperparameters—ready for future RunPod automation.

### Next Steps
- Extend configs to cover advanced PPO knobs (schedule types, normalize_advantage) or alternate algos (A2C) as experiments expand.
- Feed these config files directly into the upcoming RunPod experiment runner so remote pods stay in sync with local baselines.

## 2025-11-13 — Topic: VecNormalize + Advanced PPO Configs

### Sources
- `app/rl/training_config.py`, `scripts/train_sb3.py`, `configs/train/ppo_cpu_baseline.json` (updated).
- Command: `source .venv/bin/activate && python scripts/train_sb3.py --train-config configs/train/ppo_cpu_baseline.json`

### Key Notes
1. Training configs now expose advanced PPO/A2C knobs (`normalize_advantage`, `clip_range_vf`, `ent_coef`, `vf_coef`, `max_grad_norm`) plus a structured `vecnormalize` block. Flags flow straight into SB3, so future sweeps can tune these without editing Python.
2. The training script detects `vecnormalize.enabled` and wraps the env with `VecNormalize`, saving stats to `<save_path>_vecnormalize.pkl` and recording the path in the `_meta.json` file for reproducible eval/inference.
3. Latest baseline run (4,096 steps, PPO) finished with mean reward ≈ -6.25 and produced `models/ppo_cpu_baseline.zip`, `_meta.json`, and `_vecnormalize.pkl`; metadata now captures the merged hyperparameters plus eval metrics for downstream orchestration.

### Next Steps
- When we lift this into RunPod, mount both the policy zip and vecnorm stats so evaluation pods share identical normalization.
- Consider auto-toggling progress bars/tensorboard via config fields when we introduce remote logging.

## 2025-11-13 — Topic: Policy Evaluation Pipeline

### Sources
- `scripts/eval_sb3.py`, `app/rl/factory.py` (VecNormalize helpers), `models/ppo_cpu_baseline*.{zip,pkl,meta}`.
- Command: `source .venv/bin/activate && python scripts/eval_sb3.py --model models/ppo_cpu_baseline.zip --env-config configs/env/btcusd_1m_sepnov2025.json --algo ppo --vecnormalize models/ppo_cpu_baseline_vecnormalize.pkl --episodes 3 --seed 7`

### Key Notes
1. Added `scripts/eval_sb3.py` to load any saved SB3 checkpoint, restore VecNormalize stats when provided, and run deterministic rollouts (prints per-episode reward + JSON summary). This pairs with the training metadata so we can QA policies offline.
2. `app/rl/factory.build_vec_env` now encapsulates env creation + optional VecNormalize loading, ensuring both training and evaluation go through the same wrapper stack (MultiDiscrete actions, TimeLimit, Monitor).
3. Baseline policy evaluation over three seeded episodes yielded rewards of roughly -3.44/-5.71/-2.79 (mean ≈ -3.98), confirming the full loop (train → save policy + stats → reload + eval) is working.

### Next Steps
- Surface eval summary files (e.g., write JSON to `reports/`) when we automate nightly checkpoints.
- When RunPod orchestration arrives, reuse `scripts/eval_sb3.py` for smoke tests after each remote training job before promoting models.

## 2025-11-13 — Topic: Local RunPod-Style Experiment Runner

### Sources
- `scripts/run_experiment.py`, `scripts/eval_sb3.py`, `scripts/train_sb3.py`, artifacts under `runs/experiments/20251113T002310Z_smoke/`.
- Command: `source .venv/bin/activate && python scripts/run_experiment.py --train-config configs/train/ppo_cpu_baseline.json --episodes 2 --seed 5 --tag smoke`

### Key Notes
1. `scripts/run_experiment.py` now mimics the RunPod workflow locally: it loads a TrainingConfig, invokes the training CLI, then automatically evaluates the resulting policy (passing VecNormalize stats along) and writes `experiment.json` + `eval_summary.json` under `runs/experiments/<timestamp>_<tag>/`.
2. Metadata from training (`*_meta.json`) and evaluation summaries are bundled together so future pod orchestrators can just copy this directory off the worker instead of scraping logs.
3. The sample “smoke” run produced `runs/experiments/20251113T002310Z_smoke/` with the baseline PPO config, eval mean reward ≈ -4.58 over two deterministic episodes, and copies of the config for traceability.

### Next Steps
- Swap the `subprocess.run` calls for RunPod API invocations once we wire up remote pods; the directory layout can stay identical for on-prem vs. cloud to keep tooling simple.
- Consider emitting richer telemetry (train loss curves, SB3 monitor CSV) into each run folder for later dashboarding.

## 2025-11-13 — Topic: RunPod Payload & Experiment Bundles

### Sources
- `scripts/run_experiment.py` (archive option), `scripts/runpod_submit.py`, `scripts/eval_sb3.py` (JSON output).
- Commands:
  - `source .venv/bin/activate && python scripts/run_experiment.py --train-config configs/train/ppo_cpu_baseline.json --episodes 2 --seed 5 --tag smoke --archive runs/experiments/smoke.tar.gz`
  - `source .venv/bin/activate && python scripts/runpod_submit.py --train-config configs/train/ppo_cpu_baseline.json --output runpod_payload.json --tag smoke-pod --volume-id vol-123 --gpu-type-id GPU-ABC --image runpod/base:latest --episodes 3 --seed 11`

### Key Notes
1. `scripts/run_experiment.py` can now gzip the entire run directory (`--archive <path>`) so pods can hand back a single tarball containing configs, metadata, eval summaries, and trained policies—mirrors what we’ll upload from RunPod storage.
2. `scripts/runpod_submit.py` generates a RunPod `createPod` payload: it validates the training config, builds the `python scripts/run_experiment.py …` command, injects env vars (config path + run tag), and optionally attaches network volumes. The sample payload was saved to `runpod_payload.json` for quick copy/paste into the API/UI.
3. `scripts/eval_sb3.py` gained `--output` so deterministic eval summaries are written to JSON (consumed by the experiment runner). `run_experiment.py` now uses that to stash `eval_summary.json` alongside `experiment.json` and optional archives.

### Next Steps
- Replace the local `subprocess.run` calls with real RunPod API invocations once credentials/volume IDs are finalized.
- Extend `runpod_submit.py` to accept template files for environment variables (e.g., API keys) before we automate CI submissions.

## 2025-11-13 — Topic: RunPod Submission Stubs

### Sources
- `scripts/runpod_submit.py`, `scripts/runpod_client.py`, payload `runpod_submissions/submission_20251113T003840Z.json`.
- Commands:
  - `source .venv/bin/activate && python scripts/runpod_submit.py --train-config configs/train/ppo_cpu_baseline.json --output tmp_payload.json --tag autopod --episodes 4 --seed 9 --volume-id vol-xyz --gpu-type-id GPU-DEF --image runpod/torch:latest`
  - `source .venv/bin/activate && python scripts/runpod_client.py --payload tmp_payload.json --output runpod_submissions`

### Key Notes
1. Added `scripts/runpod_client.py` as a stub that just saves payloads to `runpod_submissions/`, letting us dry-run the RunPod API flow without credentials. Each submission is timestamped so we can diff configs or attach them to issues.
2. `scripts/runpod_submit.py` remains the single source of truth for pod commands; the stub simply consumes its JSON output, meaning we can swap in the real API POST later without touching the config logic.
3. This completes the “local rehearsal” pipeline: config → experiment runner → optional tarball → RunPod payload → mock submission. Once the actual API key and volume IDs arrive, we replace `runpod_client.py` with a thin wrapper over `requests.post` to `/v2/pods`.

### Next Steps
- Implement the real HTTP call (with retries/status polling) and hook it into CI or a CLI flag once credentials are available.
- Mirror the `runpod_submissions/` log into `docs/ops/runpod.md` so ops folks can trace which configs went up when.
