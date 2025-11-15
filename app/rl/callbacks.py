"""Custom SB3 callbacks."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Sequence

from stable_baselines3.common.callbacks import BaseCallback


def _clean_value(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


class ActionLoggerCallback(BaseCallback):
    """Logs per-step action metadata to a CSV file."""

    def __init__(self, log_path: Path, verbose: int = 0) -> None:
        super().__init__(verbose)
        self.log_path = Path(log_path)
        self._file = None
        self._writer: csv.DictWriter | None = None
        self._episode_steps: List[int] | None = None
        self._fieldnames = [
            "global_step",
            "env_index",
            "episode_step",
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

    def _on_training_start(self) -> bool:
        envs = self.training_env.num_envs
        self._episode_steps = [0 for _ in range(envs)]
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.log_path.open("w", newline="")
        self._writer = csv.DictWriter(self._file, fieldnames=self._fieldnames)
        self._writer.writeheader()
        return True

    def _on_training_end(self) -> None:
        if self._file:
            self._file.flush()
            self._file.close()
            self._file = None
            self._writer = None

    def _on_step(self) -> bool:
        infos: Sequence[dict] | None = self.locals.get("infos")
        dones: Sequence[bool] | None = self.locals.get("dones")
        if infos is None or self._writer is None or self._episode_steps is None:
            return True
        for idx, info in enumerate(infos):
            if info:
                self._episode_steps[idx] += 1
                row = {
                    "global_step": int(self.num_timesteps),
                    "env_index": idx,
                    "episode_step": self._episode_steps[idx],
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
                self._writer.writerow({k: _clean_value(v) for k, v in row.items()})
            if dones is not None and idx < len(dones) and dones[idx]:
                self._episode_steps[idx] = 0
        if self._file:
            self._file.flush()
        return True
