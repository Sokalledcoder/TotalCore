# Execution Plan – RL Trading Lab

This plan sequences the work from research through deployment. Each phase assumes we keep refining requirements as new information becomes available.

> **Status snapshot (2025-11-12):** Phases 0–2 are partially complete. We now have a working ingestion service and ~11 months of BTC/USD 1m candles (Jan–Nov 2025). Next priorities are “Phase 2 – Data Handling Foundations (remaining validation)” and “Phase 4 – RL Environment v1,” plus the streaming ingestion noted in long-term steps.

## Phase 0 – Research & Architecture Alignment
1. Work through the research checklist (`docs/research/research_todo.md`) to lock in:
   - Preferred RL stack (FinRL vs SB3) and algorithm shortlist.
   - RunPod pod + serverless configurations, including base images and CUDA support.
   - Data format decisions and normalization strategies.
2. Produce architecture decision records (ADRs) for:
   - RL framework selection.
   - Backend/front-end stack.
   - Job orchestration approach.

## Phase 1 – Repo Structure & Tooling Scaffolding
1. Create base directories: `data/`, `tools/`, `apps/backend`, `apps/frontend`, `infra/`, etc.
2. Add placeholder README files explaining each directory’s purpose.
3. Set up Python environment management (Poetry/uv/conda) for shared packages.
4. Establish linting/formatting/testing baselines (ruff, black, pytest) to keep the codebase consistent.

## Phase 2 – Data Handling Foundations
1. Define canonical schema for 1-minute bars + metadata (likely Parquet).
2. Implement ingestion scripts to load existing datasets into `data/<SYMBOL>/`.
3. Create validation utilities (missing data checks, timezone alignment, split verification).
4. Document procedures for syncing data to RunPod network volumes.

## Phase 3 – Tools & Indicator Framework
1. Design a plugin-style loader for `tools/` so new indicators/logic can be registered via metadata (e.g., entry point definitions or manifest files).
2. Implement shared abstractions:
   - Tool base class with config schema + feature computation hooks.
   - Utility functions for sliding-window feature generation.
3. Convert first sample indicator/logic document into code to validate the workflow.
4. Provide tests that confirm indicators can be parameterized and produce expected outputs on historical snippets.

## Phase 4 – RL Environment v1
1. Draft the Gymnasium-compatible environment:
   - Observation builder (OHLCV window + configured tool outputs + account state).
   - Action space definition (multi-discrete or composite actions for trade + risk controls).
   - Reward module with pluggable components (PnL, drawdown penalty, trade cost).
2. Implement episode management, execution model (fills, slippage, fees), and logging.
3. Create configuration schemas allowing per-run customization (window sizes, tool lists, reward weights).
4. Write unit tests and synthetic data simulations to ensure the environment behaves deterministically.

## Phase 5 – Experiment Runner & Docker Image
1. Build the experiment runner CLI/handler:
   - Parses JSON configs.
   - Instantiates environment + selected RL algorithm.
   - Handles training/evaluation splits and artifact output.
2. Package dependencies into a Docker image (CUDA/PyTorch base, RL libs, RunPod SDK).
3. Automate image builds via `infra/docker/` scripts and push to the chosen registry.

## Phase 6 – RunPod Integration
1. Implement a small SDK/wrapper for creating/monitoring pods:
   - Pod provisioning, volume attachment, env vars, command execution.
   - Graceful teardown + idle kill logic.
2. (Optional) Build serverless worker handler for lightweight indicator/backtest jobs.
3. Integrate artifact syncing between pods and control-plane storage (results, logs, model weights).

## Phase 7 – Control Plane Backend
1. Choose backend stack (e.g., FastAPI + SQLAlchemy + Postgres).
2. Define DB schema for datasets, tools, RL env versions, experiments, and results.
3. Implement APIs for:
   - Managing datasets and tools.
   - Creating/updating RL environment configs.
   - Scheduling experiments and tracking RunPod jobs.
4. Add background workers or job queue to orchestrate pod lifecycle and enforce budget constraints.
5. Provide API tests and seed data for development.

## Phase 8 – Frontend & UX
1. Scaffold the frontend (e.g., Next.js/React + Tailwind/Chakra).
2. Build pages:
   - Dashboard with experiment summaries.
   - Experiments list/detail views with metrics and plots.
   - RL environment config editor with form validation.
3. Integrate charts for equity curves and metric comparisons.
4. Implement real-time or periodic status updates (polling or WebSockets).

## Phase 9 – End-to-End Validation
1. Run a full dry-run:
   - Register dataset + tool.
   - Configure RL environment.
   - Launch an experiment on RunPod and verify metrics/logs flow back.
2. Add automated tests for the orchestration pipeline (mocking RunPod interactions where needed).
3. Document operational playbooks (starting/stopping pods, interpreting metrics, onboarding new tools).

## Phase 10 – Iteration & Enhancements
1. Incorporate additional tools/indicators as you supply new strategy documents.
2. Optimize performance (vectorized envs, batched data loading, mixed precision training).
3. Explore hyperparameter sweeps, ensemble agents, and evaluation automation.

This phased roadmap keeps us focused: research → scaffolding → tooling → environment → infrastructure → control plane → UX → validation → iteration. We can adjust scope per phase based on discoveries or changing priorities.
