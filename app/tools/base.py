"""Base classes for indicator and execution tools."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class Indicator(Protocol):
    name: str

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return a DataFrame with the indicator columns (aligned to frame)."""

    @property
    def output_columns(self) -> list[str]:
        ...


@dataclass
class RiskContext:
    capital: float
    risk_pct: float
    entry_price: float
    stop_price: float

    def position_size(self) -> float:
        denom = max(self.entry_price - self.stop_price, 1e-9)
        return (self.capital * self.risk_pct) / denom
