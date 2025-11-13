#!/usr/bin/env python
"""Run one or more sample episodes against the TradeEnvironment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from app.rl import EnvConfig, TradeEnvironment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to EnvConfig JSON file.")
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--log-json",
        help="Optional path to write per-step traces (JSON Lines).",
    )
    return parser.parse_args()


def _to_python(value: Any):
    if isinstance(value, (np.generic,)):
        return value.item()
    return value


def _snapshot_obs(obs: Dict[str, np.ndarray]) -> Dict[str, List[float]]:
    market_tail = obs["market"][-1]
    account_vec = obs["account"]
    return {
        "market_tail": [float(x) for x in np.asarray(market_tail, dtype=np.float64).tolist()],
        "account": [float(x) for x in np.asarray(account_vec, dtype=np.float64).tolist()],
    }


def run_episode(env: TradeEnvironment, seed: int, capture_steps: bool, episode_idx: int) -> tuple[dict, list[dict]]:
    obs, info = env.reset(seed=seed)
    done = False
    total_reward = 0.0
    steps = 0
    step_logs: list[dict] = []
    while not done:
        sampled_action = env.action_space.sample()
        if not isinstance(sampled_action, dict):
            raise TypeError("Expected dict action from MultiDiscrete wrapper")
        action = {key: int(value) for key, value in sampled_action.items()}
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        steps += 1
        done = terminated or truncated
        if capture_steps:
            record = {
                "episode": episode_idx,
                "step": steps,
                "action": action,
                "reward": float(reward),
                "terminated": bool(terminated),
                "truncated": bool(truncated),
                "info": {k: _to_python(v) for k, v in info.items()},
            }
            record.update(_snapshot_obs(obs))
            step_logs.append(record)
    return {
        "steps": steps,
        "total_reward": total_reward,
        "final_equity": info.get("equity"),
        "drawdown": info.get("drawdown"),
    }, step_logs


def main() -> None:
    args = parse_args()
    config_data = json.loads(Path(args.config).read_text())
    config = EnvConfig.model_validate(config_data)
    env = TradeEnvironment(config)

    capture = args.log_json is not None
    all_logs: list[dict] = []
    for episode in range(args.episodes):
        metrics, logs = run_episode(env, seed=args.seed + episode, capture_steps=capture, episode_idx=episode)
        print(
            f"Episode {episode + 1}: steps={metrics['steps']} total_reward={metrics['total_reward']:.4f} "
            f"final_equity={metrics['final_equity']:.2f} drawdown={metrics['drawdown']:.4f}"
        )
        if capture:
            all_logs.extend(logs)

    if capture and args.log_json:
        log_path = Path(args.log_json)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w") as fh:
            for record in all_logs:
                fh.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
