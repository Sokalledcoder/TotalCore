#!/usr/bin/env python
"""Evaluate a saved SB3 policy on the TradeEnvironment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.vec_env import VecNormalize

from app.rl.factory import build_vec_env

ALGORITHMS = {
    "ppo": PPO,
    "a2c": A2C,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Path to SB3 .zip checkpoint")
    parser.add_argument("--env-config", required=True, help="EnvConfig JSON path")
    parser.add_argument("--algo", choices=ALGORITHMS.keys(), default="ppo")
    parser.add_argument("--vecnormalize", help="Optional VecNormalize stats (.pkl)")
    parser.add_argument("--episodes", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", help="Optional path to write JSON summary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    env = build_vec_env(args.env_config, args.seed, args.vecnormalize)
    algo_cls = ALGORITHMS[args.algo]
    model = algo_cls.load(args.model, env=env)

    returns = []
    lengths = []
    for episode in range(args.episodes):
        obs = env.reset()
        done = False
        score = 0.0
        steps = 0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _ = env.step(action)
            score += float(np.asarray(reward).squeeze())
            steps += 1
        returns.append(score)
        lengths.append(steps)
        print(f"Episode {episode + 1}: reward={score:.4f} steps={steps}")

    summary = {
        "mean_reward": sum(returns) / len(returns) if returns else 0.0,
        "mean_length": sum(lengths) / len(lengths) if lengths else 0,
        "episodes": args.episodes,
        "model": args.model,
        "env_config": args.env_config,
        "vecnormalize": args.vecnormalize,
    }
    print("Summary:", json.dumps(summary, indent=2))
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
