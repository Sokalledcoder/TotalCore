# Handoff Report — Session 5 (RTX PRO / ADX+MACD / Action Logging)

Date: 2025-11-19

## 1) What changed this session
- Added **ADX** and **MACD** indicators (`app/tools/indicators/adx.py`, `macd.py`), registered in `indicator_registry.py`, and included them in `configs/tools/extended.json` (now part of the risk-based env inputs).
- Created the **RTX PRO transformer preset** `configs/train/ppo_gpu_transformer_rtxpro.json` for a 96 GB GPU (20 env workers, larger transformer, 1.2M timesteps).
- Enabled **per-step action logging** via `ActionLoggerCallback` in `scripts/train_sb3.py` (writes `models/<save_name>_actions.csv`).
- Added **replay tooling**: `scripts/replay_policy.py` replays a saved checkpoint (with VecNormalize) to a CSV; documented in `docs/transformer_policy.md`.
- Fixed ADX numeric/NaN issues and silenced most pandas downcast spam; patched replay script to handle Gym reset and SB3 schedule deserialization.

## 2) Latest run (RTX PRO transformer)
- Folder (VolumeCore mirror): `VolumeCore_latest/runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/`
  - `experiment.json`, `eval_summary.json`, `ppo_gpu_transformer_rtxpro.json`
  - Replay CSV: `ppo_gpu_transformer_rtxpro_replay.csv` (240 steps)
  - Plot: `replay_equity_direction.png`
- Models/logs (VolumeCore): `VolumeCore_latest/models/ppo_gpu_transformer_rtxpro.{zip,vecnormalize.pkl,actions.csv,meta.json}`
- To display in Run Insights, copy the run folder into `runs/experiments/` here and restart the backend (`scripts/run_api.sh restart`).

### Eval metrics (from eval_summary.json)
- Episodes: 3 (240 steps each)
- Mean reward: **2008.64**
- Mean profit (USD): **$2,008,702** (per-episode profits: +0.86K, +6.03M, +0.084K)
- Mean return: ~20.09%
> These profits look unrealistically high; treat with caution until replay/backtest confirms no sim exploit.

## 3) Current RTX PRO preset details
- Algo: PPO (SB3 2.3.2), transformer extractor
- Transformer: d_model=420, nheads=12, num_layers=6, FF=2048, dropout=0.1, context_attention_layers=2 (heads=12), features_dim=896
- Parallel envs: 20 SubprocVecEnv workers
- Timesteps: 1.2M; n_steps=4096; batch_size=4096; lr=1e-4; gamma=0.995; gae_lambda=0.92; clip_range=0.2; ent_coef=0.01; vf_coef=0.5; grad_clip=0.6
- Observations: 64× BTC/USD 1m OHLCV + returns + indicators (VWAP, ZScore, ATR, RSI, Bollinger, ADX, MACD); account state (position, cash, equity, drawdown)
- Actions: direction (short/flat/long), size bucket (0.5/1/1.5/2×), stop-loss bucket (10 steps).
- Risk sizing: `risk_sizing_mode=risk_based`, `risk_pct=1%`, `stop_loss_bps=25`, `max_position_size=10 BTC`; fees: limit 0.02%, market 0.05%, slippage 5 bps; reward penalizes fees and drawdown.

## 4) Replay
- Replay script now runs; CSV at `VolumeCore_latest/.../ppo_gpu_transformer_rtxpro_replay.csv` (240 rows, episode 1). Warnings are cosmetic (pandas future warning, torch nested_tensor).
- Generated quick plot `replay_equity_direction.png` (equity vs. action direction).

## 5) Gaps / risks
- Unrealistically high PnL in eval → needs deeper replay/backtest to verify.
- Run folder not yet in `runs/experiments/` locally → Run Insights won’t show it until copied.
- Remaining pandas FutureWarning from ADX fillna (harmless noise).
- Other algorithms (SAC/TD3, wider MLP) not yet tested as controls.

## 6) How to sync the latest run locally (if only on VolumeCore)
```bash
# example from pod to S3
aws s3 cp --recursive runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/ \
  s3://6wlciwn57c/TradeCore/runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/ \
  --endpoint-url https://s3api-eu-ro-1.runpod.io --region eu-ro-1 --exclude "*/__pycache__/*"

# then on this machine
aws s3 cp --recursive s3://6wlciwn57c/TradeCore/runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/ \
  runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/ \
  --endpoint-url https://s3api-eu-ro-1.runpod.io --region eu-ro-1 --exclude "*/__pycache__/*"
scripts/run_api.sh restart
```

## 7) Suggested next steps
- Plot replay CSV with price/position/fees to sanity-check the huge PnL; confirm no sim pathology.
- Run a slimmer transformer or a SAC/TD3 baseline as a control on the same data.
- Automate post-run sync of `models/` and action logs to avoid missing artifacts.
- (Optional) quiet the remaining pandas warning in ADX.

## 8) Quick run command (RTX PRO preset)
```bash
cd /workspace/TradeCore
source .venv/bin/activate
pip install -e . tensorboard tqdm rich
CUDA_VISIBLE_DEVICES=0 python scripts/run_experiment.py \
  --train-config configs/train/ppo_gpu_transformer_rtxpro.json \
  --episodes 3 \
  --seed 505 \
  --tag runpod-transformer-rtxpro
```
Use tmux: `tmux new -s rtxpro` / `tmux attach -t rtxpro`.

## 9) Key files (local mirrors)
- Run artifacts: `VolumeCore_latest/runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/`
- Model & logs: `VolumeCore_latest/models/ppo_gpu_transformer_rtxpro.{zip,vecnormalize.pkl,actions.csv,meta.json}`
- Replay CSV: `.../ppo_gpu_transformer_rtxpro_replay.csv`
- Plot: `.../replay_equity_direction.png`
