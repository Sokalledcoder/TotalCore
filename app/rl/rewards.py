"""Reward computation helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .config import RewardConfig
from .execution import AccountState


@dataclass
class RewardResult:
    reward: float
    info: Dict[str, float]


class RewardCalculator:
    def __init__(self, config: RewardConfig, scale: float):
        self.config = config
        self.scale = scale

    def compute(self, equity_delta: float, fees_paid: float, account: AccountState) -> RewardResult:
        scaled_pnl = equity_delta / self.config.reward_scale
        scaled_fees = fees_paid / self.config.reward_scale
        position_penalty = (abs(account.position_value) / self.scale) * self.config.position_penalty_weight
        drawdown_penalty = account.drawdown * self.config.drawdown_weight

        reward = (
            self.config.pnl_weight * scaled_pnl
            - self.config.fee_weight * scaled_fees
            - position_penalty
            - drawdown_penalty
        )

        info = {
            "equity_delta": equity_delta,
            "fees": fees_paid,
            "drawdown": account.drawdown,
            "position_value": account.position_value,
        }
        return RewardResult(reward=reward, info=info)
