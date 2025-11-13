# RunPod Workflow (Draft)

## 1. Prepare Training Config
1. Edit/clone a config under `configs/train/` (JSON/YAML supported via `TrainingConfig`).
2. Ensure `save_path` points at `/workspace/TradeCore/models/<name>` so pods write artifacts to the attached volume.
3. Commit or copy the config to the network volume before launching the pod.

## 2. Local Dry Run (Optional)
```bash
source .venv/bin/activate
python scripts/run_experiment.py --train-config configs/train/ppo_cpu_baseline.json \
  --episodes 2 --seed 5 --tag smoke --archive runs/experiments/smoke.tar.gz
```
- Output: `runs/experiments/<timestamp>_<tag>/` + optional `.tar.gz` for review.

## 3. Generate Pod Payload
```bash
python scripts/runpod_submit.py --train-config configs/train/ppo_cpu_baseline.json \
  --tag autopod --episodes 4 --seed 9 --volume-id <VOL_ID> \
  --gpu-type-id <GPU_TYPE> --image runpod/torch:latest --output pod_payload.json
```
- Payload fields:
  - `cmd`: `cd /workspace/TradeCore && python scripts/run_experiment.py ...`
  - `env`: `TRAIN_CONFIG`, `RUN_TAG` (extend as needed for secrets).
  - `volumeId` / `volumeMountPath`: required for network volume access.

## 4. Submit to RunPod (Placeholder)
- Until API credentials arrive, run:
```bash
python scripts/runpod_client.py --payload pod_payload.json --output runpod_submissions
```
- Real submission: POST the payload to `https://api.runpod.io/v2/pods` with API key header; capture `podId` for polling.

## 5. Pod Execution Expectations
- Entry command runs `scripts/run_experiment.py` which:
  1. Executes SB3 training per config.
  2. Evaluates the saved policy via `scripts/eval_sb3.py`.
  3. Writes `experiment.json`, `eval_summary.json`, and (optional) `.tar.gz` bundle.
- Artifacts land under `runs/experiments/<timestamp>_<tag>/` on the network volume plus `models/<name>.zip` and `models/<name>_vecnormalize.pkl`.

## 6. Retrieval & Cleanup
1. After pod completion, download the tarball or copy the run directory from the volume to cold storage.
2. Remove stale pods/volumes to avoid charges.
3. Record the payload + run directory in `docs/ops/runpod.md` (expand this doc) for auditability.

## 7. TODO (Next Integration Steps)
- Implement real RunPod client with:
  - `POST /v2/pods` + status polling (`GET /v2/pods/{podId}`).
  - Log streaming or S3 upload of `runs/experiments/*.tar.gz`.
  - Secrets injection (API keys) via `env` or `volumeMount` once defined.
