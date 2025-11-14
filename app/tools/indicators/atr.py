from __future__ import annotations

import pandas as pd


class ATRIndicator:
    name = "atr"

    def __init__(self, window: int = 14):
        self.window = window

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        high = frame["high"]
        low = frame["low"]
        close = frame["close"]
        prev_close = close.shift(1)

        tr_components = pd.concat(
            [
                (high - low).abs(),
                (high - prev_close).abs(),
                (low - prev_close).abs(),
            ],
            axis=1,
        )
        true_range = tr_components.max(axis=1)
        atr = true_range.rolling(self.window).mean()
        return pd.DataFrame({self.column_name: atr})

    @property
    def column_name(self) -> str:
        return f"atr_{self.window}"

    @property
    def output_columns(self) -> list[str]:
        return [self.column_name]
