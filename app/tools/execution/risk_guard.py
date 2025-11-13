"""Risk guard tool enforcing stop-loss sizing."""
from __future__ import annotations

from dataclasses import dataclass

from app.rl.execution import AccountState
from app.rl.actions import ActionDecision


@dataclass
class RiskPlan:
    target_units: float
    stop_price: float | None
    stop_distance: float
    risk_capital: float
    risk_units: float
    desired_units: float
    stop_steps: int


@dataclass
class RiskGuard:
    risk_pct: float
    stop_loss_bps: float
    max_position: float

    def plan(self, decision: ActionDecision, price: float, account: AccountState) -> RiskPlan:
        equity = max(account.equity, 1e-6)
        risk_capital = equity * self.risk_pct
        direction = decision.direction
        size_fraction = abs(decision.size_fraction)
        if direction == 0 or size_fraction <= 0.0:
            return RiskPlan(
                target_units=0.0,
                stop_price=None,
                stop_distance=0.0,
                risk_capital=risk_capital,
                risk_units=0.0,
                desired_units=0.0,
                stop_steps=0,
            )

        step = max(decision.stop_loss_idx + 1, 1)
        distance = (self.stop_loss_bps * step / 10_000.0) * price
        distance = max(distance, 1e-6)
        stop_price = price - distance if direction > 0 else price + distance

        risk_units = risk_capital / distance
        desired_units = size_fraction * self.max_position
        units = min(risk_units, desired_units, self.max_position)
        target_units = direction * units

        return RiskPlan(
            target_units=target_units,
            stop_price=stop_price,
            stop_distance=distance,
            risk_capital=risk_capital,
            risk_units=risk_units,
            desired_units=desired_units,
            stop_steps=step,
        )
