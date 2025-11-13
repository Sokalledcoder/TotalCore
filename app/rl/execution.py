"""Order execution and account state tracking."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AccountState:
    cash: float
    position: float
    equity: float
    peak_equity: float
    drawdown: float
    last_price: float
    total_fees: float = 0.0
    stop_price: float | None = None

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
    """Handles limit and market executions with fees."""

    def __init__(self, max_position: float, limit_fee_rate: float, market_fee_rate: float, slippage_rate: float):
        self.max_position = max_position
        self.limit_fee_rate = limit_fee_rate
        self.market_fee_rate = market_fee_rate
        self.slippage_rate = slippage_rate

    def execute_limit(self, target_units: float, price: float, account: AccountState) -> float:
        delta = target_units - account.position
        if abs(delta) < 1e-12:
            return 0.0

        slippage = 1.0 + self.slippage_rate * (1 if delta > 0 else -1)
        fill_price = price * slippage
        notional = delta * fill_price
        account.cash -= notional
        fee = abs(notional) * self.limit_fee_rate
        account.cash -= fee
        account.position += delta
        account.total_fees += fee
        return fee

    def close_position_market(self, price: float, account: AccountState) -> float:
        position = account.position
        if abs(position) < 1e-12:
            return 0.0
        notional = position * price
        account.cash -= notional
        fee = abs(notional) * self.market_fee_rate
        account.cash -= fee
        account.total_fees += fee
        account.position = 0.0
        account.stop_price = None
        return fee
