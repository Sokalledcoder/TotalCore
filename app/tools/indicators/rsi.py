from __future__ import annotations

import pandas as pd


class RSIIndicator:
    name = "rsi"

    def __init__(self, window: int = 14, field: str = "close"):
        self.window = window
        self.field = field

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        series = frame[self.field]
        delta = series.diff()
        gains = delta.clip(lower=0)
        losses = -delta.clip(upper=0)

        avg_gain = gains.ewm(alpha=1 / self.window, adjust=False).mean()
        avg_loss = losses.ewm(alpha=1 / self.window, adjust=False).mean()
        rs = avg_gain / avg_loss.replace(0, 1e-9)
        rsi = 100 - (100 / (1 + rs))
        return pd.DataFrame({self.column_name: rsi})

    @property
    def column_name(self) -> str:
        suffix = self.field if self.field != "close" else "close"
        return f"rsi_{suffix}_{self.window}"

    @property
    def output_columns(self) -> list[str]:
        return [self.column_name]
