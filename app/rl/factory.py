"""Factories for loading configs and creating RL environments."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from gymnasium.wrappers import TimeLimit
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecEnv, VecNormalize

from .config import EnvConfig
from .env import TradeEnvironment
from .wrappers import MultiDiscreteActionWrapper


def load_env_config(path: str | Path) -> EnvConfig:
    data = json.loads(Path(path).read_text())
    return EnvConfig.model_validate(data)


def make_env(config: EnvConfig, seed: int | None = None) -> TradeEnvironment:
    env = TradeEnvironment(config)
    if seed is not None:
        env.reset(seed=seed)
    return env


def make_wrapped_env(
    config: EnvConfig,
    seed: int | None = None,
    episode_minutes: int | None = None,
    flatten_actions: bool = False,
):
    env = make_env(config, seed=seed)
    if flatten_actions:
        env = MultiDiscreteActionWrapper(env)
    if episode_minutes is None:
        episode_minutes = config.episode_minutes
    # Ensure episodes never exceed configured minutes.
    env = TimeLimit(env, max_episode_steps=episode_minutes)
    env = Monitor(env, info_keywords=("episode_pnl_usd", "episode_return_pct"))
    return env


def build_vec_env(
    config_path: str,
    seed: int,
    vecnormalize_path: str | None = None,
    num_envs: int = 1,
) -> VecEnv:
    if num_envs < 1:
        raise ValueError("num_envs must be >= 1")
    base_config = load_env_config(config_path)
    config_payload = base_config.model_dump()

    def _make_env_fn(offset: int):
        def _factory():
            cfg = EnvConfig.model_validate(config_payload)
            env_seed = None if seed is None else seed + offset
            return make_wrapped_env(cfg, seed=env_seed, flatten_actions=True)

        return _factory

    env_fns = [_make_env_fn(idx) for idx in range(num_envs)]
    if num_envs == 1:
        env: VecEnv = DummyVecEnv(env_fns)
    else:
        env = SubprocVecEnv(env_fns)
    if vecnormalize_path:
        env = VecNormalize.load(vecnormalize_path, env)
        env.training = False
        env.norm_reward = False
    return env
