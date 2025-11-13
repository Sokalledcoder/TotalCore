# Handoff Report — Session 2

## Summary
- The RL environment now loads indicator stacks via a new manifest-driven tool registry (`app/tools/**`). VWAP and rolling z-score are the initial features, and future indicators drop in through JSON manifests.
- Execution has a mandatory risk guard: before every order the agent must specify a stop-loss bucket; the guard computes allowable position size using `risk_pct` and enforces limit/market fees (0.02 % maker, 0.05 % taker). Stops auto-trigger as market exits.
- The BTC/USD 1m manifest and parquet partition are versioned inside the repo (`data/manifests/…`, `data/lake/…`), so pods or local clones have a consistent dataset out of the box.
- RunPod workflow is documented (`docs/ops/pod_startup.md`) and verified on spot pod `alqaw7msy850ww`—smoke tests run on CUDA with archived outputs under `/workspace/TradeCore/runs/experiments/...`.
- “Next Sessions Plan” (`docs/research/next_sessions_plan.md`) captures the agreed priority order: (1) indicator/tool feature set, (2) RL env knobs, (3) data/automation, (4) web UX.

## Current State
- Indicators: `configs/tools/default.json` enables VWAP + close z-score; `EnvConfig.indicator_manifest_path` points to it. Observation builder concatenates these features automatically when present.
- Execution: `RiskGuard` computes stop distance from the stop-loss slot, caps position size via the risk formula, and stores the stop price. `ExecutionEngine` charges the correct fee type and closes positions at stop triggers.
- Fees & Stops: Config now exposes `risk_pct`, `stop_loss_bps`, `limit_fee_bps`, `market_fee_bps`; default env uses 1 % risk, 50 bps stop steps, 0.02 % maker, 0.05 % taker.
- Dataset: `data/lake/kraken/BTC-USD/1m/year=2025` (~23 MB) + manifest are part of git, so pods don’t require manual uploads. (`configs/tools/` and `MM-Experiments/` archive are also versioned.)
- RunPod pods: VolumeCore (`6wlciwn57c`) holds the repo and venv; `docs/ops/pod_startup.md` lists exact image (`runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`), commands, and failure fixes.

## Problems / Open Items
1. **Testing pass** — Need a structured smoke suite (local + RunPod) to prove indicators, risk guard, and fees behave as expected before exposing knobs.
2. **Web frontend knobs** — UI still only covers ingestion requests; no panel yet for enabling indicators, risk settings, or experiment runs.
3. **Tool expansion** — Only VWAP/z-score exist; additional indicators (ATR, RSI, volatility bands, order-flow stats) still to be implemented once the testing pass is complete.
4. **Automation backlog** — CCXT Pro streaming, retention tooling, and RunPod auto-submit remain paused per the agreed priority order.

## Planned Next Steps (per priority agreement)
1. **Verification pass**
   - Run `scripts/run_experiment.py` locally and on pod to confirm indicator outputs, stop-loss enforcement, and fee accounting (log cash/fee deltas per step).
   - Add a CLI validator (e.g., `scripts/validate_tools.py`) that loads manifests + datasets to catch missing columns before training.
2. **Expose knobs on the frontend**
   - Add a “Control” panel letting you pick indicator manifest, risk %, stop distance, fee overrides, and tool toggles before launching an experiment.
   - Wire the panel to call the existing experiment runner (locally first, then via RunPod once automation is ready).
3. **Tool layering**
   - After UI knobs work, implement additional indicators (ATR, RSI variants, volatility bands, order-flow metrics) and extend manifests accordingly.
   - Keep RiskGuard always-on; other execution helpers (e.g., trailing stop) can be optional once the base workflow is validated.
4. **Later (not immediate)**
   - Resume CCXT Pro streaming + retention tooling.
   - Replace the mock RunPod client with real GraphQL submissions/polling and tie experiment archives to the S3 endpoint.

## Useful References / How-Tos
- **Pod bootstrap:** `docs/ops/pod_startup.md` (template image, volume attach, env vars, pip cache tweaks, smoke test command).
- **Indicators & manifests:** `configs/tools/default.json`, `app/tools/indicator_registry.py`, `app/tools/indicators/*.py`.
- **Risk guard & fees:** `app/tools/execution/risk_guard.py`, `app/rl/execution.py`, `configs/env/btcusd_1m_sepnov2025.json`.
- **Experiment runner:** `scripts/run_experiment.py` (handles training + eval + archiving in one command).
- **Plan overview:** `docs/research/next_sessions_plan.md` for the agreed order of future work.

## Session Context
Session 2 covered the indicator framework, risk guard, fee rules, RunPod bootstrap, and current plan alignment. Next session should start with the verification pass + UI knob work described above before we expand indicators or tackle automation.
