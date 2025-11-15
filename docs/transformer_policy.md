# Transformer Policy Preview

This prototype replaces the MLP policy backbone with a lightweight transformer encoder:

- Each 64×N market window is linearly projected to `d_model=300`, positional encodings are added, and the sequence is passed through 4 encoder blocks (6 heads, FF dim 1536) plus two stacked context-attention blocks that re-attend the pooled representation over the sequence.
- A learnable CLS token pools the sequence output, which is concatenated with a projected account vector and fed through a linear head (512-dim features) for the actor/critic.
- The extractor lives at `app/rl/policies/transformer.py` and is plugged into SB3 via `policy_kwargs` in `configs/train/ppo_gpu_transformer.json`.

## Running on RunPod

1. Pull the latest repo inside your pod and reinstall editable deps: `pip install -e . tensorboard tqdm rich` (stable-baselines3 2.7+ required).
2. Launch:
   ```bash
   CUDA_VISIBLE_DEVICES=0 python scripts/run_experiment.py \
     --train-config configs/train/ppo_gpu_transformer.json \
     --episodes 3 \
     --seed 404 \
     --tag runpod-transformer-test
   ```
3. As with other remote runs, sync `runs/experiments/<timestamp>` back into the repo so the Run Insights dashboard can visualize the metrics.

This is an early experiments preset; expect to tune `d_model`, number of layers, and learning-rate/batch settings as we gather results. For quick experiments you can override `--num-envs` or tweak `features_extractor_kwargs` in the JSON without editing code.
