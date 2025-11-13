# Next Sessions Plan (Nov 2025)

This document captures the agreed priority order and the specific knobs we’ll expose with plain-language names so we both know what each tweak actually does.

## Priority Order
1. **Indicators & Tools Framework** (Phase 3)
2. **RL Environment Enhancements** (remaining Phase 4 items)
3. **Data/Automation cleanup** (retention, CCXT Pro streaming, RunPod auto-launch)
4. **Web Frontend Extensions** (dashboards, UI controls for the new knobs)

Everything else waits until the first three bullets are solid.

---

## 1. Indicators & Tools (We’re building next)
| Internal Name | Friendly Name | Why it matters | Work Items |
| --- | --- | --- | --- |
| Indicator manifests | **“Drink Menu”** | Pick which feature cocktails go into the env | - Spec manifest format (YAML/JSON)<br>- Build loader in `/tools` with entrypoints<br>- Write 2 starter indicators (e.g., VWAP, rolling z-score)<br>- Add unit tests + CLI validation (`scripts/validate_tools.py`) |
| Sliding window utils | **“Blender”** | Consistent way to mix price + indicators | - Generalize rolling window helper in `app/rl/state_builder.py`<br>- Ensure tools can request different window lengths |
| Tool registry API | **“Card Catalog”** | Lets web front + configs reference tools by alias | - Expose `GET /api/tools` in FastAPI<br>- Sync with frontend dropdown |

**Deliverable:** tool manifest + loader + at least two real indicators wired into the observation builder.

---

## 2. RL Environment Enhancements (after tools land)
| Setting | Friendly Name | Explanation |
| --- | --- | --- |
| VecNormalize toggles | **“Brain Shampoo”** | Turn observation/reward normalization on/off per run |
| Clip range VF | **“Safety Scissors”** | Keeps value estimates from swinging too far |
| Normalize advantage | **“Mood Stabilizer”** | Keeps PPO advantage scale consistent |
| Entropy / value coeffs | **“Explorer Boost” / “Piggy Bank Weight”** | Balance exploration vs. profit focus |
| Action slots (stop/take tweaks) | **“Nudge Bars”** | Adjusts how aggressive stop-loss / take-profit nudges are |

**Work plan:**
1. Extend `TrainingConfig` schema with user-friendly names & defaults.
2. Surface the knobs in config JSON + web frontend (form labels use the friendly names above).
3. Add tests to ensure each knob actually changes the behavior (SB3 `check_env`, regression tests).

---

## 3. Data & Automation (later)
### Retention + Streaming
- “Broom Closet” script: prune overlapping parquet partitions before reruns.
- CCXT Pro worker (“Live DJ”): stream ticks/candles, append to `/data/lake`.

### RunPod Automation
- Replace mock client with real GraphQL submission & status polling.
- Archive uploads (S3 endpoint) once runs finish.

---

## 4. Web Frontend Tasks (after env tweaks are ready)
1. **Knob Panel (“Control Tower”)** – expose the friendly-named options (Drink Menu, Brain Shampoo, etc.) so we can launch experiments from the UI.
2. **Experiment Timeline (“Flight Log”)** – visualize runs/experiments + metrics.
3. **Tool Inspector (“X-Ray”)** – charts showing indicator outputs over the dataset.
4. **Data Coverage View** – highlight manifest slices, gaps, retention actions.

---

## Setup Cheat Sheet (pods)
Keep using `docs/ops/pod_startup.md`. TL;DR: volume mounted at `/workspace`, activate venv, run smoke test. If pods get deleted, relaunch using the template/image + volume instructions in that doc.

