from __future__ import annotations

import pandas as pd


class MACDIndicator:
    name = "macd"

    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9, field: str = "close"):
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.field = field

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        price = frame[self.field].astype(float)
        ema_fast = price.ewm(span=self.fast, adjust=False).mean()
        ema_slow = price.ewm(span=self.slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal, adjust=False).mean()
        histogram = macd_line - signal_line

        return pd.DataFrame(
            {
                self.macd_column: macd_line,
                self.signal_column: signal_line,
                self.hist_column: histogram,
            }
        ).astype(float)

    @property
    def macd_column(self) -> str:
        return f"macd_{self.fast}_{self.slow}_{self.signal}"

    @property
    def signal_column(self) -> str:
        return f"macd_signal_{self.fast}_{self.slow}_{self.signal}"

    @property
    def hist_column(self) -> str:
        return f"macd_hist_{self.fast}_{self.slow}_{self.signal}"

    @property
    def output_columns(self) -> list[str]:
        return [self.macd_column, self.signal_column, self.hist_column]
