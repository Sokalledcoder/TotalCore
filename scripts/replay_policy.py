#!/usr/bin/env python
"""Replay a trained policy and log per-step actions for analysis."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

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
    parser.add_argument("--algo", choices=ALGORITHMS.keys(), required=True)
    parser.add_argument("--env-config", required=True, help="EnvConfig JSON path")
    parser.add_argument("--vecnormalize", help="Optional VecNormalize stats (.pkl)")
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", required=True, help="CSV file to write action traces")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    env = build_vec_env(args.env_config, args.seed, args.vecnormalize, num_envs=1)
    if isinstance(env, VecNormalize):
        env.training = False
        env.norm_reward = False
    algo_cls = ALGORITHMS[args.algo]
    model = algo_cls.load(args.model, env=env)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as csvfile:
        fieldnames = [
            "episode",
            "episode_step",
            "reward",
            "decision_direction",
            "decision_size_fraction",
            "target_position",
            "stop_price",
            "limit_fee",
            "stop_fee",
            "cash",
            "position",
            "equity",
            "drawdown",
            "last_price",
            "episode_pnl_usd",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for episode in range(args.episodes):
            obs, _ = env.reset()
            done = False
            step_idx = 0
            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, rewards, dones, infos = env.step(action)
                info = infos[0] if infos else {}
                step_idx += 1
                writer.writerow(
                    {
                        "episode": episode + 1,
                        "episode_step": step_idx,
                        "reward": float(rewards[0]),
                        "decision_direction": info.get("decision_direction"),
                        "decision_size_fraction": info.get("decision_size_fraction"),
                        "target_position": info.get("target_position"),
                        "stop_price": info.get("stop_price"),
                        "limit_fee": info.get("limit_fee"),
                        "stop_fee": info.get("stop_fee"),
                        "cash": info.get("cash"),
                        "position": info.get("position"),
                        "equity": info.get("equity"),
                        "drawdown": info.get("drawdown"),
                        "last_price": info.get("last_price"),
                        "episode_pnl_usd": info.get("episode_pnl_usd"),
                    }
                )
                done = bool(dones[0])


if __name__ == "__main__":
    main()
