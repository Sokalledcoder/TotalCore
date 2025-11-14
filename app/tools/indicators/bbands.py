from __future__ import annotations

import pandas as pd


class BollingerBandsIndicator:
    name = "bollinger"

    def __init__(self, window: int = 20, std_mult: float = 2.0, field: str = "close"):
        self.window = window
        self.std_mult = std_mult
        self.field = field

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        series = frame[self.field]
        rolling = series.rolling(self.window)
        mid = rolling.mean()
        std = rolling.std(ddof=0).fillna(0.0)
        upper = mid + self.std_mult * std
        lower = mid - self.std_mult * std
        width = (upper - lower).replace(0, 1e-9) / mid.replace(0, 1e-9)
        return pd.DataFrame(
            {
                self.upper_column: upper,
                self.lower_column: lower,
                self.width_column: width,
            }
        )

    @property
    def prefix(self) -> str:
        suffix = self.field if self.field != "close" else "close"
        return f"bb_{suffix}_{self.window}"

    @property
    def upper_column(self) -> str:
        return f"{self.prefix}_upper"

    @property
    def lower_column(self) -> str:
        return f"{self.prefix}_lower"

    @property
    def width_column(self) -> str:
        return f"{self.prefix}_width"

    @property
    def output_columns(self) -> list[str]:
        return [self.upper_column, self.lower_column, self.width_column]
