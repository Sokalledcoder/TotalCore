# RL Trading Lab – Working Requirements

This document captures the current understanding of what we are building, based on the research brief in `research.txt` and the additional clarifications provided afterward. It will evolve as we learn more.

## Project Goals
- Build an RL-driven trading lab that can train agents on multi-year 1-minute data using RunPod GPUs.
- Provide a configurable toolbox of trading actions (entries/exits, SL/TP, sizing, indicator-driven logic) for the agents.
- Keep pure indicator backtests local; GPU pods focus on RL workloads.

## Data & Assets
- Historical data lives under `data/<SYMBOL>/...` (e.g., `data/BTCUSDT/`).
- Datasets likely include OHLCV and any supplementary features we prepare.
- Shared storage on RunPod (network volumes) will hold canonical datasets for pod access.

## Tools & Indicators
- All indicator logic, strategy snippets, and utility “tools” (e.g., stop-loss management) live under a `tools/` folder.
- Indicators are treated as tools we can hand to the agent; adding a new indicator/tool means dropping Python code into this folder and wiring it into configs.
- No pre-existing indicator catalog—each document/spec you provide will be converted into Python and validated before exposing it to agents.

## RL Environment Expectations
- No initial draft exists—we must design and implement the first version from scratch.
- Environment should follow Gymnasium conventions with configurable observation/action/reward spaces.
- Actions should reflect the toolbox mindset (open/close positions, adjust SL/TP, select position sizing, etc.).
- Rewards must be parameterized to combine PnL, drawdown penalties, transaction costs, and other risk controls.
- Episodes traverse contiguous time windows with no lookahead bias; execution should model realistic fills, slippage, and fees.

## System Architecture Snapshot
- Control plane: backend + DB for datasets, indicators, RL env versions, experiments, and results; web UI for dashboards, experiment drill-downs, and environment config editing.
- Compute plane: RunPod GPU pods (and optionally serverless endpoints) using our Docker image and shared network volumes.
- Experiment runner: JSON-configurable CLI/handler that loads data, instantiates the environment + RL algorithm, trains, evaluates, logs metrics, and stores artifacts.

## Open Design Decisions (pending research)
1. Final RL stack (FinRL vs Stable-Baselines3 vs hybrid) and best algorithms for our use case.
2. Specific Docker base image, CUDA version, and dependency pinning strategy for RunPod pods.
3. Backend + frontend tech stack (greenfield choice).
4. Queue/orchestration mechanism for managing RunPod jobs and budget constraints.
5. Exact storage formats for datasets (Parquet/CSV/Feather) and any preprocessing pipeline steps.

This document will be updated as soon as we answer the outstanding research questions and lock in architectural choices.
