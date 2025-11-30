# VolumeCore Inventory (for restore)

Generated: 2025-11-22
Source bucket: `s3://6wlciwn57c/TradeCore/`
Goal: Recreate the bucket later by re‑uploading these objects. Hashes are omitted; sizes/timestamps are from S3 listings.

## Top-level entries (remote)
From `aws s3 ls s3://6wlciwn57c/TradeCore/`:
- Directories: `.git/`, `.venv/`, `app/`, `configs/`, `data/`, `docs/`, `frontend/`, `models/`, `runpod_payloads/`, `runs/`, `scripts/`, `tests/`, `tradecore.egg-info/`
- Files: `--archive`, `--episodes`, `--seed`, `--tag`, `--train-config`, `.gitignore` (336 B, 2025-11-14 22:35:55), `AGENTS.md` (3.2 KB), `deploy_runpod.sh` (691 B), `handoff-session-1..4.md`, `pyproject.toml` (744 B), `research.txt` (16 KB), `server.log` (88 KB)

## Models (remote list)
From `aws s3 ls s3://6wlciwn57c/TradeCore/models/`:
- 960,251  (2025-11-13) `ppo_cpu_baseline.zip`
- 665      (2025-11-13) `ppo_cpu_baseline_meta.json`
- 17,765   (2025-11-13) `ppo_cpu_baseline_vecnormalize.pkl`
- 1,474,097 (2025-11-15) `ppo_gpu_medium.zip`
- 744      (2025-11-15) `ppo_gpu_medium_meta.json`
- 27,365   (2025-11-15) `ppo_gpu_medium_vecnormalize.pkl`
- 19,934,674 (2025-11-15) `ppo_gpu_risk_medium.zip`
- 856      (2025-11-15) `ppo_gpu_risk_medium_meta.json`
- 50,878   (2025-11-15) `ppo_gpu_risk_medium_vecnormalize.pkl`
- 95,163,940 (2025-11-15) `ppo_gpu_transformer.zip`
- 1,181    (2025-11-15) `ppo_gpu_transformer_meta.json`
- 57,592   (2025-11-15) `ppo_gpu_transformer_vecnormalize.pkl`
- 237,489,215 (2025-11-15) `ppo_gpu_transformer_rtxpro.zip`
- 176,335,886 (2025-11-15) `ppo_gpu_transformer_rtxpro_actions.csv`
- 1,212    (2025-11-15) `ppo_gpu_transformer_rtxpro_meta.json`
- 118,314  (2025-11-15) `ppo_gpu_transformer_rtxpro_vecnormalize.pkl`

### Local mirror status (models)
- Complete mirror stored under `VolumeCore_latest/full/models/` (all items above copied).
- Additional working copies: `models/` (select items) and `VolumeCore_latest/models/` (RTX Pro set). The mirror path is the canonical restore source.

## Runs / experiments (remote list)
Per-run `aws s3 ls s3://6wlciwn57c/TradeCore/runs/experiments/<run>/`:

- 20251113T193359Z_verify-pod: `ppo_cpu_baseline.json`
- 20251113T204007Z_verify-pod: `eval_summary.json`, `experiment.json`, `ppo_cpu_baseline.json`
- 20251114T213807Z_runpod-gpu-test: `ppo_gpu_medium.json`
- 20251114T214951Z_runpod-gpu-test: `ppo_gpu_medium.json`
- 20251114T215306Z_runpod-gpu-test: `ppo_gpu_medium.json`
- 20251114T215812Z_runpod-gpu-test: `eval_summary.json`, `experiment.json`, `ppo_gpu_medium.json`
- 20251115T000905Z_runpod-risk-test: `ppo_gpu_risk_medium.json`
- 20251115T001102Z_runpod-risk-test: `ppo_gpu_risk_medium.json`
- 20251115T001210Z_runpod-risk-test: `ppo_gpu_risk_medium.json`
- 20251115T001629Z_runpod-risk-test: `eval_summary.json`, `experiment.json`, `ppo_gpu_risk_medium.json`
- 20251115T005421Z_runpod-transformer-test: `ppo_gpu_transformer.json`
- 20251115T005818Z_runpod-transformer-test: `ppo_gpu_transformer.json`
- 20251115T022243Z_runpod-transformer-test: `ppo_gpu_transformer.json`
- 20251115T023305Z_runpod-transformer-test: `ppo_gpu_transformer.json`
- 20251115T030325Z_runpod-transformer-test: `eval_summary.json`, `experiment.json`, `ppo_gpu_transformer.json`
- 20251115T141920Z_runpod-transformer-rtxpro: `ppo_gpu_transformer_rtxpro.json`
- 20251115T142455Z_runpod-transformer-rtxpro: `ppo_gpu_transformer_rtxpro.json`
- 20251115T143352Z_runpod-transformer-rtxpro: `ppo_gpu_transformer_rtxpro.json`
- 20251115T144139Z_runpod-transformer-rtxpro: `ppo_gpu_transformer_rtxpro.json`
- 20251115T145441Z_runpod-transformer-rtxpro: `ppo_gpu_transformer_rtxpro.json`
- 20251115T150013Z_runpod-transformer-rtxpro: `eval_summary.json`, `experiment.json`, `ppo_gpu_transformer_rtxpro.json`
- verify-pod.tar.gz (in runs/experiments root)

### Local mirror status (runs)
- `VolumeCore_latest/full/runs/experiments/`: empty (run downloads blocked by RunPod S3 pagination bug).
- `runs/experiments/` in the repo contains several runs already synced manually: `20251113T002310Z_smoke`, `20251113T155224Z_verify-local`, `20251113T194417Z_verify-pod`, `20251114T215812Z_runpod-gpu-test`, `20251115T001629Z_runpod-risk-test`, `20251115T030325Z_runpod-transformer-test`, `20251115T150013Z_runpod-transformer-rtxpro`, plus `verify-pod.tar.gz`.
- Missing locally: the other run directories listed above (all except those noted). These should be re-downloaded if a full restore is required.

## How to restore later
1. Upload models:
   ```bash
   aws s3 cp VolumeCore_latest/full/models/ s3://<new-bucket>/TradeCore/models/ --recursive
   ```
2. Upload run artifacts you care about (after re-downloading the missing ones if desired). Example for RTX Pro latest run:
   ```bash
   aws s3 cp runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/ s3://<new-bucket>/TradeCore/runs/experiments/20251115T150013Z_runpod-transformer-rtxpro/ --recursive
   ```
3. Recreate top-level text assets if needed (`AGENTS.md`, handoff files, etc.) from the repo root.

## Known issues
- RunPod S3 pagination is flaky (repeated continuation tokens) when listing large prefixes; per-run `aws s3 ls` without recursion works reliably. Bulk recursive listings may fail; prefer per-run copies.
- Local mirror does not currently include run folders beyond those listed under local status.

## References
- Remote listings saved under `VolumeCore_latest/index/`: `remote_root_listing.txt`, `remote_models_listing.txt`, `remote_runs_listing.txt`.
- Local mirror listing: `VolumeCore_latest/index/local_full_listing.txt` (files under `VolumeCore_latest/full/`).
