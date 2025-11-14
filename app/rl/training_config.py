"""Training configuration models for SB3 runners."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Literal, Optional

import yaml
from pydantic import BaseModel, Field


AlgoName = Literal["ppo", "a2c"]


class VecNormalizeConfig(BaseModel):
    enabled: bool = False
    norm_obs: bool = True
    norm_reward: bool = True
    clip_obs: float = 10.0
    clip_reward: float = 10.0
    gamma: float = 0.99

    def to_kwargs(self) -> Dict[str, Any]:
        return {
            "norm_obs": self.norm_obs,
            "norm_reward": self.norm_reward,
            "clip_obs": self.clip_obs,
            "clip_reward": self.clip_reward,
            "gamma": self.gamma,
        }


class TrainingConfig(BaseModel):
    env_config_path: str = Field(..., description="Path to EnvConfig JSON")
    algorithm: AlgoName = Field("ppo")
    total_timesteps: int = Field(10_000, ge=1)
    seed: int = 0
    eval_episodes: int = Field(2, ge=0)
    num_envs: int = Field(1, ge=1, description="How many parallel env instances to launch")
    save_path: str = "models/agent"
    log_dir: Optional[str] = None
    progress_bar: bool = False
    algo_kwargs: Dict[str, Any] = Field(default_factory=dict)
    normalize_advantage: Optional[bool] = None
    clip_range_vf: Optional[float] = None
    ent_coef: Optional[float] = None
    vf_coef: Optional[float] = None
    max_grad_norm: Optional[float] = None
    vecnormalize: VecNormalizeConfig = Field(default_factory=VecNormalizeConfig)

    def merge_overrides(self, overrides: Dict[str, Any]) -> "TrainingConfig":
        data = self.model_dump()
        for key, value in overrides.items():
            if value is None:
                continue
            data[key] = value
        return TrainingConfig.model_validate(data)


def load_training_config(path: str | Path) -> TrainingConfig:
    p = Path(path)
    text = p.read_text()
    if p.suffix.lower() in {".yml", ".yaml"}:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    return TrainingConfig.model_validate(data)
