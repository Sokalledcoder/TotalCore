"""Order execution and account state tracking."""
from __future__ import annotations

from dataclasses import dataclass

from .actions import ActionDecision


@dataclass
class AccountState:
    cash: float
    position: float
    equity: float
    peak_equity: float
    drawdown: float
    last_price: float
    total_fees: float = 0.0

    def mark_to_market(self, price: float) -> None:
        self.last_price = price
        self.equity = self.cash + self.position * price
        if self.equity > self.peak_equity:
            self.peak_equity = self.equity
        if self.peak_equity > 0:
            self.drawdown = (self.peak_equity - self.equity) / self.peak_equity
        else:
            self.drawdown = 0.0

    @property
    def position_value(self) -> float:
        return self.position * self.last_price


class ExecutionEngine:
    """Simplified market-order execution model."""

    def __init__(self, max_position: float, fee_rate: float, slippage_rate: float):
        self.max_position = max_position
        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate

    def apply(self, decision: ActionDecision, price: float, account: AccountState) -> float:
        target_units = decision.direction * decision.size_fraction * self.max_position
        delta = target_units - account.position
        if abs(delta) < 1e-12:
            return 0.0

        slippage = 1.0 + self.slippage_rate * (1 if delta > 0 else -1)
        fill_price = price * slippage
        notional = delta * fill_price
        account.cash -= notional
        fee = abs(notional) * self.fee_rate
        account.cash -= fee
        account.position += delta
        account.total_fees += fee
        return fee
