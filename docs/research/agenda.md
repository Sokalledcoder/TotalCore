# Research Agenda (v0.1)

Purpose: capture what we must investigate before implementation, what answers we need, and which artifact will document each finding. Every research task below should produce notes in `docs/research/log.md` (or a thematic sub-file) with sources and actionable takeaways.

---

## 1. Gym-Style RL Trading Environment

- **Questions**
  - How do state/action/reward designs look in FinRL, Gymnasium-based repos, and notable papers?
  - What are best practices for multi-discrete action spaces that combine position control, SL/TP, and sizing?
  - How do existing envs deal with transaction costs, slippage, and leverage constraints without leakage?
  - What normalization/feature-scaling approaches help stabilize RL training on OHLCV + indicator stacks?
- **Expected Outputs**
  - Template describing observation tensors, configurable indicators, and agent-state features.
  - Candidate action-space schemas (multi-discrete vs flattened) with pros/cons.
  - Reward-spec catalog with tunable weights and references.
  - Episode/reset protocol covering randomized windows, train/val splits, and data integrity checks.

## 2. RL Training Stack & Libraries

- **Questions**
  - Compare FinRL vs Stable-Baselines3 vs RLlib/CleanRL for extensibility, GPU readiness, and compatibility with custom envs.
  - Determine CUDA/PyTorch combinations that RunPod supports out of the box.
  - Identify how to integrate hyperparameter sweeps or evaluation loops cleanly.
- **Expected Outputs**
  - Decision matrix selecting the primary RL library (with rationale).
  - Dependency list for the base Docker image (CUDA version, Python libs).
  - Outline for experiment runner CLI/serverless handler arguments and logging conventions.

## 3. RunPod Infrastructure Integration

- **Questions**
  - Concrete API/SDK calls for creating GPU pods, attaching network volumes, streaming logs, and terminating jobs.
  - Network volume performance characteristics and any sizing/region constraints relevant to large 1m datasets.
  - Serverless worker limits (runtime, RAM, concurrency) to know which utilities belong there vs full pods.
- **Expected Outputs**
  - Sequence diagrams for: dataset upload, experiment launch, result collection.
  - Reference payload templates (JSON) for pod creation and serverless endpoint deployment.
  - Cost/performance notes per GPU tier relevant to typical experiment sizes.

## 4. Tool & Indicator Packaging

- **Questions**
  - Best patterns for sharing indicator/strategy code between classic backtests and the RL environment.
  - Ways to load user-supplied Python modules safely while preserving flexibility (plugin registry, entry points, etc.).
  - How to represent tool metadata (parameters, expected inputs/outputs) so the RL env can auto-wire them.
- **Expected Outputs**
  - Proposal for a `tools/` module layout, naming conventions, and validation hooks.
  - Schema for tool manifests (JSON/YAML) tying code to metadata.
  - Guidelines for testing/CI around contributed tools.

## 5. Control Plane (Backend, DB, UI)

- **Questions**
  - Recommended stacks for API + job orchestration (e.g., FastAPI + Postgres + Dramatiq/Celery) in similar ML platforms.
  - DB schema patterns for experiment tracking, config versioning, and artifact references.
  - Front-end frameworks and visualization libs suited for RL experiment dashboards (React + Recharts/Plotly, etc.).
  - Strategies for long-running job status updates (polling vs WebSockets vs push notifications).
- **Expected Outputs**
  - Draft ER diagram / table list aligned with datasets, indicators, env versions, experiments, results.
  - Backend architectural sketch showing API, scheduler, RunPod client, and storage interactions.
  - UI wireframe descriptions for dashboard, experiment detail, and env config pages.

## 6. Data Management & Validation

- **Questions**
  - Best practices for organizing multi-symbol historical data, handling missing intervals, and ensuring chronological integrity.
  - Techniques for fast slicing of large 1m datasets (PyArrow, DuckDB, Parquet partitioning).
  - How to track provenance/versions of datasets tied to experiments.
- **Expected Outputs**
  - Data directory conventions (already `/data/<SYMBOL>` baseline) with file format recommendations.
  - Validation checklist/scripts to run before feeding data into RL runs.
  - Storage footprint estimates per symbol/year to plan volume sizing.

## 7. Native Market Data Acquisition (CCXT)

- **Questions**
  - Which exchanges/timeframes expose historical OHLCV or trades via CCXT, and what rate-limit/retention constraints apply?
  - How do we structure incremental backfills (pagination strategy, gap detection, mark/index price variants)?
  - What scheduling/resiliency patterns (retry, resume, alerting) keep the ingestion service reliable?
- **Expected Outputs**
  - Design for the ingestion subsystem (workers, config schema, metadata tables, resume checkpoints).
  - Guidelines for respecting per-exchange rate limits (`enableRateLimit`, concurrency caps) and handling API keys/testnets.
  - Data lifecycle plan covering raw dumps vs curated Parquet (naming, partitioning, deduplication, QC hooks).

## 8. Security, Budget, and Operational Guardrails

- **Questions**
  - RunPod features for auto-shutdown, budget caps, and monitoring to prevent runaway GPU costs.
  - Access control patterns if multiple users eventually interact with the control plane.
  - Backup/retention strategies for experiment artifacts and datasets stored on network volumes.
- **Expected Outputs**
  - Policy recommendations (max concurrent pods, idle timeouts, alerting hooks).
  - Notes on integrating RunPod billing/usage data into the dashboard.
  - Backup/replication plan for network volumes or external storage.

---

## Research Logging Protocol

1. Each deep dive gets a section in `docs/research/log.md` with:
   - Date
   - Topic
   - Sources (URL + short note)
   - Key findings
   - Actionable decisions or open questions
2. Large topics can break into sub-files under `docs/research/<topic>.md`, but they must be linked from the main log.
3. Summaries should stay implementation-focused so we can translate them directly into specs and tasks.
