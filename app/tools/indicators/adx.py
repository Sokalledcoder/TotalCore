from __future__ import annotations

import pandas as pd


class ADXIndicator:
    name = "adx"

    def __init__(self, window: int = 14):
        self.window = window
        self.alpha = 1.0 / window

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        high = frame["high"].astype(float)
        low = frame["low"].astype(float)
        close = frame["close"].astype(float)

        up_move = high.diff().fillna(0.0).astype(float)
        down_move = (low.shift(1) - low).fillna(0.0).astype(float)

        plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
        minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

        tr_components = pd.concat(
            [
                (high - low).abs(),
                (high - close.shift(1)).abs(),
                (low - close.shift(1)).abs(),
            ],
            axis=1,
        )
        true_range = tr_components.max(axis=1)

        atr = true_range.fillna(0.0).ewm(alpha=self.alpha, adjust=False).mean()
        plus_di = 100 * (plus_dm.ewm(alpha=self.alpha, adjust=False).mean() / atr.replace(0, pd.NA))
        minus_di = 100 * (minus_dm.ewm(alpha=self.alpha, adjust=False).mean() / atr.replace(0, pd.NA))

        dx = (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, pd.NA)
        dx *= 100
        adx = dx.ewm(alpha=self.alpha, adjust=False).mean()

        return pd.DataFrame({self.column_name: adx.astype(float)})

    @property
    def column_name(self) -> str:
        return f"adx_{self.window}"

    @property
    def output_columns(self) -> list[str]:
        return [self.column_name]
