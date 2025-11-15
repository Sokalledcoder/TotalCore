#!/usr/bin/env python
"""Train an SB3 agent on the TradeEnvironment."""
from __future__ import annotations

import argparse
import json
from importlib import import_module
from pathlib import Path

from stable_baselines3 import A2C, PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import VecNormalize

from app.rl.factory import build_vec_env
from app.rl.training_config import TrainingConfig, load_training_config

ALGORITHMS = {
    "ppo": PPO,
    "a2c": A2C,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="EnvConfig JSON path (override or fallback)")
    parser.add_argument("--train-config", help="Training config JSON/YAML path")
    parser.add_argument("--algo", choices=ALGORITHMS.keys(), help="Override algorithm")
    parser.add_argument("--total-timesteps", type=int, help="Override total timesteps")
    parser.add_argument("--seed", type=int, help="Override seed")
    parser.add_argument("--log-dir", help="Optional tensorboard log dir; omit to disable")
    parser.add_argument("--save-path", help="Override model save path")
    parser.add_argument("--eval-episodes", type=int, help="Override eval episode count")
    parser.add_argument("--num-envs", type=int, help="Override number of parallel envs")
    parser.add_argument("--progress-bar", action="store_true", help="Enable SB3 progress bar (requires tqdm/rich)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.train_config:
        train_cfg = load_training_config(args.train_config)
    else:
        if not args.config:
            raise SystemExit("Either --train-config or --config must be provided")
        train_cfg = TrainingConfig(
            env_config_path=args.config,
            algorithm=args.algo or "ppo",
            total_timesteps=args.total_timesteps or 10_000,
            seed=args.seed or 0,
            eval_episodes=args.eval_episodes or 2,
            save_path=args.save_path or "models/ppo_trade_env",
            log_dir=args.log_dir,
            progress_bar=args.progress_bar,
        )

    overrides = {}
    if args.config:
        overrides["env_config_path"] = args.config
    if args.algo:
        overrides["algorithm"] = args.algo
    if args.total_timesteps is not None:
        overrides["total_timesteps"] = args.total_timesteps
    if args.seed is not None:
        overrides["seed"] = args.seed
    if args.eval_episodes is not None:
        overrides["eval_episodes"] = args.eval_episodes
    if args.num_envs is not None:
        overrides["num_envs"] = args.num_envs
    if args.save_path:
        overrides["save_path"] = args.save_path
    if args.log_dir is not None:
        overrides["log_dir"] = args.log_dir
    if args.progress_bar:
        overrides["progress_bar"] = args.progress_bar
    if overrides:
        train_cfg = train_cfg.merge_overrides(overrides)

    tensorboard_log = None
    if train_cfg.log_dir:
        log_dir = Path(train_cfg.log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        tensorboard_log = str(log_dir)
    save_path = Path(train_cfg.save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    vec_env = build_vec_env(
        train_cfg.env_config_path,
        train_cfg.seed,
        vecnormalize_path=None,
        num_envs=train_cfg.num_envs,
    )
    vecnormalize_path: Path | None = None
    if train_cfg.vecnormalize.enabled:
        vecnorm_kwargs = train_cfg.vecnormalize.to_kwargs()
        vec_env = VecNormalize(vec_env, **vecnorm_kwargs)
        vecnormalize_path = Path(f"{train_cfg.save_path}_vecnormalize.pkl")

    algo_cls = ALGORITHMS[train_cfg.algorithm]
    algo_kwargs = dict(train_cfg.algo_kwargs or {})
    _resolve_policy_classes(algo_kwargs)
    for field in [
        "normalize_advantage",
        "clip_range_vf",
        "ent_coef",
        "vf_coef",
        "max_grad_norm",
    ]:
        value = getattr(train_cfg, field)
        if value is not None:
            algo_kwargs[field] = value
    model = algo_cls(
        "MultiInputPolicy",
        vec_env,
        verbose=1,
        seed=train_cfg.seed,
        tensorboard_log=tensorboard_log,
        **algo_kwargs,
    )
    model.learn(total_timesteps=train_cfg.total_timesteps, progress_bar=train_cfg.progress_bar)
    model.save(str(save_path))
    if vecnormalize_path is not None and isinstance(vec_env, VecNormalize):
        vec_env.save(str(vecnormalize_path))

    eval_metrics = None
    if train_cfg.eval_episodes > 0:
        eval_env = model.get_env()
        if isinstance(eval_env, VecNormalize):
            eval_env.training = False
            eval_env.norm_reward = False
        mean_reward, std_reward = evaluate_policy(
            model,
            eval_env,
            n_eval_episodes=train_cfg.eval_episodes,
            deterministic=False,
        )
        eval_metrics = {"mean_reward": float(mean_reward), "std_reward": float(std_reward)}
        print(f"Eval reward: mean={mean_reward:.4f} ± {std_reward:.4f}")

    metadata = {
        "env_config_path": train_cfg.env_config_path,
        "algorithm": train_cfg.algorithm,
        "total_timesteps": train_cfg.total_timesteps,
        "seed": train_cfg.seed,
        "eval_episodes": train_cfg.eval_episodes,
        "save_path": train_cfg.save_path,
        "log_dir": train_cfg.log_dir,
        "progress_bar": train_cfg.progress_bar,
        "algo_kwargs": algo_kwargs,
        "eval_metrics": eval_metrics,
        "vecnormalize_path": str(vecnormalize_path) if vecnormalize_path else None,
    }
    meta_path = Path(f"{train_cfg.save_path}_meta.json")
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()


def _resolve_policy_classes(algo_kwargs: dict) -> None:
    policy_kwargs = algo_kwargs.get("policy_kwargs")
    if not isinstance(policy_kwargs, dict):
        return
    extractor_path = policy_kwargs.get("features_extractor_class")
    if isinstance(extractor_path, str):
        policy_kwargs["features_extractor_class"] = _import_from_string(extractor_path)


def _import_from_string(path: str):
    module_name, _, attr = path.rpartition(".")
    if not module_name:
        raise ValueError(f"Invalid import path: {path}")
    module = import_module(module_name)
    return getattr(module, attr)
