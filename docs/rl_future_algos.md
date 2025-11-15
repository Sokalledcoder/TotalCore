# RL Algorithm Backlog

This note captures the ideas we discussed for future experiments so we can track them in one place and expose them through the control panel once each preset is ready.

## 1. PPO Baseline (current)
- Multi-input MLP policy with 8 parallel envs and large batches.
- Risk-based position sizing preset (`ppo_gpu_risk_medium.json`).
- Pros: simple, stable. Cons: CPU-bound, limited model capacity.

## 2. PPO + Transformer Policy (in progress)
- Replace the MLP backbone with `TransformerFeatureExtractor`.
- Intended to use the GPU more fully by processing the 64×N window via attention blocks.
- Config: `ppo_gpu_transformer.json` (target run tag: `runpod-transformer-test`).

## 3. PPO + Wider/Deeper MLP
- Keep PPO but set `policy_kwargs` with larger hidden layers (e.g., `[1024, 1024, 512]`).
- Goal: increase per-update GPU work without changing the algorithm.

## 4. PPO + CNN/Hybrid Extractor
- Add Conv1D layers over the window before the policy head.
- Alternative to the transformer for feature-rich encodings.

## 5. Off-Policy Algorithms (SAC/TD3)
- Leverage replay buffers so each sample is reused multiple times on GPU.
- Requires adapting the action space (likely continuous size/direction heads) or wrapping the MultiDiscrete actions in a hybrid policy.

## 6. Model-Free + Pretraining (Decision/Trend Transformer)
- Use sequence models trained via imitation or supervised pretraining before RL fine-tuning.
- More engineering effort (custom trainer, data pipelines) but opens the door to larger transformer stacks.

## 7. Async/Vectorized Env Enhancements
- Beyond SubprocVecEnv: investigate PyTorch dataloaders or ray actors to overlap environment stepping with policy updates.

## 8. Instrumentation & Metrics
- Add GPU/FPS logging per run so Run Insights can compare throughput across presets.
- Track USD PnL (already added) and drawdown for each eval episode.

### Next Steps
1. Stabilize the transformer PPO preset and surface it in the control panel.
2. Prototype wider MLP + CNN extractors (low engineering cost) to baseline GPU usage.
3. Scope a SAC/TD3 branch once we are happy with positional sizing.

