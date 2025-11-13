"""Risk guard tool enforcing stop-loss sizing."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from app.rl.execution import AccountState
from app.rl.actions import ActionDecision


@dataclass
class RiskGuard:
    risk_pct: float
    stop_loss_bps: float
    max_position: float

    def plan(self, decision: ActionDecision, price: float, account: AccountState) -> tuple[float, float | None]:
        direction = decision.direction
        if direction == 0:
            return 0.0, None

        step = max(decision.stop_loss_idx + 1, 1)
        distance = (self.stop_loss_bps * step / 10_000.0) * price
        distance = max(distance, 1e-6)

        stop_price = price - distance if direction > 0 else price + distance

        equity = max(account.equity, 1e-6)
        risk_capital = equity * self.risk_pct
        risk_units = risk_capital / distance

        desired_units = abs(decision.size_fraction) * self.max_position
        units = min(risk_units, desired_units, self.max_position)
        target_units = direction * units
        return target_units, stop_price
