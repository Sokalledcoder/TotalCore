# Verification Pass Plan

The verification pass is meant to prove that the indicator registry, stop-loss sizing, and fee accounting behave exactly as expected **before** any new knobs or tools reach the UI. The steps below build on the current Session 2 state (VWAP + close z-score manifest, mandatory RiskGuard, maker/taker fees at 0.02%/0.05%).

## 1. Static validations (fast fail)
1. Run `python scripts/validate_tools.py --env-config configs/env/btcusd_1m_sepnov2025.json`.
2. Checks performed:
   - Dataset manifest paths exist and contain the required OHLCV columns.
   - Sample windows (default 512 rows) land inside each slice’s `[start_ts, end_ts]` range.
   - Indicator manifest entries resolve to concrete classes; the registry produces `feature_count` columns and no NaNs after its internal fill.
   - Emits a structured JSON summary (`status=ok` / `status=error`) with per-slice diagnostics.
3. Exit non‑zero if any slice or indicator fails so CI/pods can gate on this.

## 2. Instrumented env episodes (accounting traces)
1. Extend `TradeEnvironment.step` info payload with:
   - `target_position`, `desired_position`, `risk_units`, `risk_capital`, `stop_distance`, and the decoded action indices.
   - `limit_fee` vs `stop_fee` so we can separate maker/taker costs.
2. Update `scripts/run_env_episode.py` with `--log-json <path>`:
   - When enabled, dump one JSON object per step containing action, decision info, the enriched `info` dict, and observation indices (price, indicator vector slice).
   - Useful locally and on RunPod to verify stop triggers and fees without digging into SB3 logs.

## 3. End-to-end experiment smoke test
1. Command (local):
   ```bash
   python scripts/run_experiment.py \
       --train-config configs/train/ppo_cpu_baseline.json \
       --episodes 1 --seed 123 --tag verify-local
   ```
2. Artifacts to inspect:
   - `runs/experiments/<ts>_verify-local/eval_summary.json` → confirm rewards recorded.
   - `models/ppo_cpu_baseline_meta.json`/`.zip` → confirm VecNormalize + algo metadata saved.
   - SB3 stdout for mean reward + std.
3. Repeat on the RunPod pod once instrumentation lands (same command but with `--tag verify-pod` and optional `--archive`).

## 4. Acceptance criteria
- `scripts/validate_tools.py` exits 0 and prints `status: "ok"` for every slice.
- Instrumented episode logs show:
  - RiskGuard never allocates more than `max_position_size` and respects the `risk_pct` formula (position size equals `risk_capital / stop_distance` clamped by desired size).
  - Market stop exits pay `market_fee_bps` and zero out positions.
  - Indicators attach to observations with exactly `IndicatorRegistry.feature_count` extra columns.
- `run_experiment.py` completes locally and on RunPod without missing manifest/data errors.

Once these are green we can expose the knobs in the dashboard without guessing about backend correctness.
