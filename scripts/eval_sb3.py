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
    env = build_vec_env(args.env_config, args.seed, args.vecnormalize, num_envs=1)
    algo_cls = ALGORITHMS[args.algo]
    model = algo_cls.load(args.model, env=env)

    returns = []
    lengths = []
    profits = []
    return_pcts = []
    for episode in range(args.episodes):
        obs = env.reset()
        score = 0.0
        steps = 0
        episode_profit = 0.0
        last_info = None
        while True:
            action, _ = model.predict(obs, deterministic=True)
            obs, rewards, dones, infos = env.step(action)
            reward_value = float(np.asarray(rewards).squeeze())
            score += reward_value
            steps += 1
            info = infos[0] if infos else {}
            last_info = info or last_info
            if info and "equity_delta" in info:
                episode_profit += info["equity_delta"]
            if dones[0]:
                final_profit = info.get("episode_pnl_usd", episode_profit)
                final_return_pct = info.get("episode_return_pct")
                returns.append(score)
                lengths.append(steps)
                profits.append(final_profit)
                if final_return_pct is not None:
                    return_pcts.append(final_return_pct)
                print(
                    f"Episode {episode + 1}: reward={score:.4f} steps={steps} profit={final_profit:.2f}"
                )
                break

    summary = {
        "mean_reward": sum(returns) / len(returns) if returns else 0.0,
        "mean_length": sum(lengths) / len(lengths) if lengths else 0,
        "mean_profit_usd": sum(profits) / len(profits) if profits else 0.0,
        "mean_return_pct": sum(return_pcts) / len(return_pcts) if return_pcts else 0.0,
        "profits": profits,
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
