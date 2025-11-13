# Research Checklist

These items require web search or external references once tools become available.

## RL Environment & Algorithms
- Survey recent Gym/Gymnasium-compatible trading envs (FinRL, gym-trading, QuantConnect RL examples) for state/action/reward patterns and multi-discrete action implementations.
- Identify best practices for financial time series normalization, especially when mixing OHLCV data with indicator outputs and account state.
- Review RL reward shaping strategies in finance (PnL vs Sharpe/Sortino proxies, drawdown penalties) to avoid degenerate behaviors like “never trade.”
- Compare FinRL vs Stable-Baselines3 vs RLlib/CleanRL in terms of customization, vectorized env support, and GPU performance.

## RunPod Platform
- Document exact steps/payloads for creating pods via API/SDK (GPU selection, cloud type, attaching network volumes, env vars).
- Research recommended CUDA/PyTorch base images or RunPod templates suitable for Stable-Baselines3/FinRL workloads.
- Confirm creation/attachment procedures and performance considerations for RunPod network volumes (latency, throughput).
- Explore RunPod serverless limits (timeouts, memory/GPU availability) and deployment workflow for custom Docker workers.

## Orchestration & Tooling
- Identify proven patterns for orchestrating long-running GPU jobs (e.g., queue + worker models) that interact with external APIs like RunPod.
- Collect references for tracking remote job status, log streaming, and artifact collection (possible frameworks: Celery, Dramatiq, Temporal, custom state machines).
- Research best practices for experiment tracking dashboards in ML (Metaflow, MLflow UI, custom React dashboards) to inform front-end design.

## Data Engineering
- Evaluate storage formats (Parquet vs Feather vs HDF5) and ingestion pipelines optimized for 1-minute multi-year histories on shared volumes.
- Investigate tooling for validating and cataloging indicator/tool definitions (maybe pydantic schemas or plugin registries).

We will iterate on this list as we uncover new unknowns or answer existing questions.
