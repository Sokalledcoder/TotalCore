from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Sequence

from app.models import BacktestEngine


@dataclass(frozen=True)
class ParamSpec:
    name: str
    type: str
    default: Any
    description: str
    min: float | None = None
    max: float | None = None
    step: float | None = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StrategySpec:
    id: str
    label: str
    description: str
    engines: Sequence[BacktestEngine]
    params: Sequence[ParamSpec]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "engines": [e.value for e in self.engines],
            "params": [p.to_dict() for p in self.params],
        }


def _sma_cross_spec() -> StrategySpec:
    return StrategySpec(
        id="sma_cross",
        label="SMA Crossover",
        description="Fast/slow moving average crossover with optional stop and take-profit.",
        engines=(BacktestEngine.backtesting_py, BacktestEngine.pybroker),
        params=(
            ParamSpec("fast", "int", 10, "Fast SMA window", min=2, max=200, step=1),
            ParamSpec("slow", "int", 50, "Slow SMA window", min=5, max=400, step=1),
            ParamSpec("risk_pct", "float", 0.02, "Fraction of equity per trade", min=0.0001, max=0.2, step=0.001),
            ParamSpec("take_profit", "float", 0.0, "Take profit % (0 disables)", min=0.0, max=0.5, step=0.001),
            ParamSpec("stop_loss", "float", 0.0, "Stop loss % (0 disables)", min=0.0, max=0.5, step=0.001),
        ),
    )


def _rsi_reversion_spec() -> StrategySpec:
    return StrategySpec(
        id="rsi_reversion",
        label="RSI Mean Reversion",
        description="Buy oversold / sell overbought based on RSI thresholds.",
        engines=(BacktestEngine.backtesting_py, BacktestEngine.pybroker),
        params=(
            ParamSpec("rsi_period", "int", 14, "RSI period", min=2, max=100, step=1),
            ParamSpec("rsi_buy", "int", 30, "RSI buy threshold", min=1, max=50, step=1),
            ParamSpec("rsi_sell", "int", 70, "RSI sell threshold", min=50, max=99, step=1),
            ParamSpec("risk_pct", "float", 0.02, "Fraction of equity per trade", min=0.001, max=0.2, step=0.001),
        ),
    )


def strategy_specs() -> List[StrategySpec]:
    return [_sma_cross_spec(), _rsi_reversion_spec()]


def get_strategy_spec(strategy_id: str) -> StrategySpec | None:
    return next((spec for spec in strategy_specs() if spec.id == strategy_id), None)
