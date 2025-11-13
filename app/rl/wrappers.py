"""Custom Gym wrappers for the TradeEnvironment."""
from __future__ import annotations

import numpy as np
from gymnasium import ActionWrapper, spaces


class MultiDiscreteActionWrapper(ActionWrapper):
    """Expose dict action space as MultiDiscrete for SB3."""

    def __init__(self, env):
        super().__init__(env)
        spec = getattr(env, "action_spec", None)
        if spec is None:
            raise ValueError("Environment must define action_spec for wrapping")

        self._lengths = (
            len(spec.direction_values),
            len(spec.size_buckets),
            spec.config.take_profit_steps,
            spec.config.stop_loss_steps,
        )
        self.action_space = spaces.MultiDiscrete(self._lengths)
        self._keys = ("direction", "size", "take_profit", "stop_loss")

    def action(self, action):
        action = np.asarray(action, dtype=np.int64)
        mapped = {}
        for idx, key in enumerate(self._keys):
            mapped[key] = int(np.clip(action[idx], 0, self._lengths[idx] - 1))
        return mapped

    def reverse_action(self, action_dict):
        return np.array([action_dict[key] for key in self._keys], dtype=np.int64)
