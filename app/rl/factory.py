"""Factories for loading configs and creating RL environments."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from gymnasium.wrappers import TimeLimit
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize

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
    env = Monitor(env)
    return env


def build_vec_env(config_path: str, seed: int, vecnormalize_path: str | None = None) -> DummyVecEnv:
    config = load_env_config(config_path)

    def _factory():
        return make_wrapped_env(config, seed=seed, flatten_actions=True)

    env = DummyVecEnv([_factory])
    if vecnormalize_path:
        env = VecNormalize.load(vecnormalize_path, env)
        env.training = False
        env.norm_reward = False
    return env
