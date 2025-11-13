"""Action specification helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence

import numpy as np
from gymnasium import spaces

from .config import ActionConfig


@dataclass
class ActionDecision:
    direction: int
    size_fraction: float
    take_profit_idx: int
    stop_loss_idx: int


class ActionSpec:
    """Maps multi-head discrete actions into semantic decisions."""

    def __init__(self, config: ActionConfig):
        self.config = config
        self.direction_values: Sequence[int] = tuple(config.direction_values)
        self.size_buckets: Sequence[float] = tuple(config.size_buckets)
        self.space = spaces.Dict(
            {
                "direction": spaces.Discrete(len(self.direction_values)),
                "size": spaces.Discrete(len(self.size_buckets)),
                "take_profit": spaces.Discrete(config.take_profit_steps),
                "stop_loss": spaces.Discrete(config.stop_loss_steps),
            }
        )

    def sample(self, rng: np.random.Generator) -> Dict[str, int]:
        return {
            "direction": int(rng.integers(0, len(self.direction_values))),
            "size": int(rng.integers(0, len(self.size_buckets))),
            "take_profit": int(rng.integers(0, self.config.take_profit_steps)),
            "stop_loss": int(rng.integers(0, self.config.stop_loss_steps)),
        }

    def decode(self, action: Dict[str, int] | np.ndarray | int) -> ActionDecision:
        if isinstance(action, dict):
            direction_idx = int(action.get("direction", 0))
            size_idx = int(action.get("size", 0))
            tp_idx = int(action.get("take_profit", 0))
            sl_idx = int(action.get("stop_loss", 0))
        else:
            raise TypeError("Action must be a dict compatible with the action space")

        direction_idx = int(np.clip(direction_idx, 0, len(self.direction_values) - 1))
        size_idx = int(np.clip(size_idx, 0, len(self.size_buckets) - 1))
        tp_idx = int(np.clip(tp_idx, 0, self.config.take_profit_steps - 1))
        sl_idx = int(np.clip(sl_idx, 0, self.config.stop_loss_steps - 1))

        return ActionDecision(
            direction=self.direction_values[direction_idx],
            size_fraction=self.size_buckets[size_idx],
            take_profit_idx=tp_idx,
            stop_loss_idx=sl_idx,
        )
