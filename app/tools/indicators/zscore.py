from __future__ import annotations

import pandas as pd


class ZScoreIndicator:
    name = "zscore"

    def __init__(self, window: int = 60, field: str = "close"):
        self.window = window
        self.field = field

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        series = frame[self.field]
        rolling = series.rolling(self.window)
        mean = rolling.mean()
        std = rolling.std().replace(0, 1e-9)
        z = (series - mean) / std
        return pd.DataFrame({self.column_name: z})

    @property
    def column_name(self) -> str:
        return f"z_{self.field}"

    @property
    def output_columns(self) -> list[str]:
        return [self.column_name]
