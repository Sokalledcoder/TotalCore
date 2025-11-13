#!/usr/bin/env python
"""Run one or more sample episodes against the TradeEnvironment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.rl import EnvConfig, TradeEnvironment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to EnvConfig JSON file.")
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def run_episode(env: TradeEnvironment, seed: int) -> dict:
    obs, info = env.reset(seed=seed)
    done = False
    total_reward = 0.0
    steps = 0
    while not done:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        steps += 1
        done = terminated or truncated
    return {
        "steps": steps,
        "total_reward": total_reward,
        "final_equity": info.get("equity"),
        "drawdown": info.get("drawdown"),
    }


def main() -> None:
    args = parse_args()
    config_data = json.loads(Path(args.config).read_text())
    config = EnvConfig.model_validate(config_data)
    env = TradeEnvironment(config)

    for episode in range(args.episodes):
        metrics = run_episode(env, seed=args.seed + episode)
        print(
            f"Episode {episode + 1}: steps={metrics['steps']} total_reward={metrics['total_reward']:.4f} "
            f"final_equity={metrics['final_equity']:.2f} drawdown={metrics['drawdown']:.4f}"
        )


if __name__ == "__main__":
    main()
