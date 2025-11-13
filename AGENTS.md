# Repository Guidelines

## Project Structure & Modules
- `app/`: FastAPI backend. Key modules include `api.py` (routes), `models.py` (Pydantic schemas), `store.py` (SQLite job tracking), and `ingestion/` (Kraken fetchers). Treat this as the canonical source for business logic.
- `frontend/`: Static HTML/CSS/JS for the Fetch History dashboard. `fetch-history.js` talks to the `/api/*` endpoints; styles live in `styles.css`.
- `scripts/`: Helper utilities such as `run_api.sh` for reliable uvicorn restarts. Add new automation here.
- `docs/` & `research.txt`: Design briefs, research notes, and specs. Read before altering ingestion behavior.
- `data/`: Local Parquet/SQLite artifacts (`data/lake`, `data/jobs.db`). Never commit these.

## Build, Test, and Development Commands
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
scripts/run_api.sh        # restart uvicorn in the background
curl -s http://localhost:8000/ # health check
```
No automated test suite yet; add pytest invocations under this section when available.

## Coding Style & Naming
- Python files follow PEP 8, 4-space indent, snake_case functions, PascalCase classes. Prefer type hints (`from __future__ import annotations` already enabled).
- Frontend JS uses ES modules and camelCase for variables. Keep CSS tokens kebab-case.
- Config/constants belong near usage (`KrakenIngestionConfig`, etc.). Avoid global singletons beyond `app = FastAPI()`.

## Testing Guidelines
- Currently manual: trigger jobs via the UI and inspect `data/lake` + `server.log`. When introducing unit tests, place them under `tests/` and run with `pytest`.
- Name future tests `test_<module>.py` and cover both ingestion success paths and failure reporting (`JobStatus`).

## Commit & Pull Request Practice
- Use descriptive, present-tense commit messages (e.g., `Add trade aggregator guard for empty chunks`). Group related changes together.
- For PRs include: scope summary, screenshots for UI tweaks, reproduction steps for bugs, and references to research docs or issues. Mention any data migrations or scripts (`scripts/run_api.sh`) that reviewers must run.

## Security & Configuration Tips
- Never commit `.venv/`, `data/lake/`, or API keys. If CCXT credentials are needed, read from environment variables.
- Before handing off, run `scripts/run_api.sh` and verify `curl http://localhost:8000/` returns `200` so reviewers can reproduce locally.
