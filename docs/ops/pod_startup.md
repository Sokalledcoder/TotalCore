# RunPod Pod Bootstrap Guide (RTX A4500 + VolumeCore)

Follow these steps whenever you spin up a fresh pod. The network volume **VolumeCore** (`6wlciwn57c`) already holds the repo, venv, manifests, and parquet data—so once the pod is configured you only need to activate the environment and run.

## 1. Launch the Pod

### Option A – UI (On-Demand / Spot)
1. Pods → **Deploy Pod** → choose **RTX A4500 (1x)** and region **EU-RO-1** (must match the volume).
2. Container Image: `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404`.
3. Container Disk: `40 GB`.
4. “Interruptable” (spot) is fine if you want the cheaper tier.
5. In the Storage section, attach network volume **VolumeCore (6wlciwn57c)** and keep mount path `/workspace`.
6. Start command (Advanced → Container Start Command):
   ```bash
   bash -lc "cd /workspace/TradeCore && sleep infinity"
   ```
7. Launch and note the Pod ID once it turns RUNNING.

### Option B – API/CLI (GraphQL)
```
mutation {
  podFindAndDeployOnDemand(
    input: {
      name: "tradecore-a4500-run",
      imageName: "runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404",
      gpuTypeId: "NVIDIA RTX A4500",
      cloudType: SECURE,
      gpuCount: 1,
      dataCenterId: "EU-RO-1",
      containerDiskInGb: 40,
      ports: "22/tcp,8888/http",
      volumeInGb: 0,
      volumeMountPath: "/workspace",
      templateId: "8zdlcdci5m",
      networkVolumeId: "6wlciwn57c"
    }
  ) {
    id
  }
}
```
Use the RunPod GraphQL endpoint with your API key to run the mutation; the response returns the new Pod ID.

## 2. Verify the Volume Mount
```
ssh -p <public-port> root@<public-ip>
df -h /workspace
ls /workspace
```
You should see `TradeCore` under `/workspace`. If not, stop the pod and relaunch with the volume attached.

## 3. Repo + Environment Setup
```
cd /workspace/TradeCore
git pull       # repo already cloned on the volume
python3 -m venv .venv   # only if .venv is missing
source .venv/bin/activate
export PYTHONPATH=/workspace/TradeCore:$PYTHONPATH
export PIP_CACHE_DIR=/workspace/pip-cache
export TMPDIR=/workspace/tmp
mkdir -p $PIP_CACHE_DIR $TMPDIR
pip install --no-cache-dir -e .[dev]
```
*(Put the `export` lines in `~/.bashrc` if you want them to apply automatically on each login.)*

## 4. Smoke Test (ensures data + env are ready)
```
source .venv/bin/activate
python scripts/run_experiment.py --train-config configs/train/ppo_cpu_baseline.json \
    --episodes 1 --seed 1 --tag pod-smoke \
    --archive runs/experiments/pod-smoke.tar.gz
```
Expected output: PPO runs ~4k steps, evaluation prints a JSON summary, and `runs/experiments/<timestamp>_pod-smoke/` plus `models/ppo_cpu_baseline*.{zip,pkl}` are created under `/workspace/TradeCore`.

## 5. Uploading / Updating Data
- **Manifests & parquet** are now tracked in git (`data/manifests/...`, `data/lake/...`). A simple `git pull` brings them down on every pod.
- If you add new data locally, commit + push and then `git pull` inside the pod.
- For ad-hoc files (extra configs, artifacts), either commit them or scp them over `ssh -p <port> root@<ip>`; everything under `/workspace` persists as long as VolumeCore exists.

## 6. Common Issues & Fixes
| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: app` | Ensure `PYTHONPATH=/workspace/TradeCore` before running scripts |
| `Disk quota exceeded` during pip | Use the `/workspace` volume for cache/tmp (`PIP_CACHE_DIR`, `TMPDIR`) and reinstall with `--no-cache-dir` |
| `FileNotFoundError: data/manifests/...` | Run `git pull` so the manifest + parquet files are present |
| Pod won’t pull image | Use `runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404` (current verified tag) |
|

Keep this checklist handy when launching transient pods—once VolumeCore is mounted, the environment is ready within a couple of minutes.
