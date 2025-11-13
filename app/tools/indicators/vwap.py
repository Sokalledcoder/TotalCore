from __future__ import annotations

import pandas as pd


class VWAPIndicator:
    name = "vwap"

    def __init__(self, window: int = 30):
        self.window = window

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        price = frame["close"]
        volume = frame["volume"].replace(0, 1e-9)
        typical_price = (frame["high"] + frame["low"] + frame["close"]) / 3
        vwap = (typical_price * volume).rolling(self.window).sum() / volume.rolling(self.window).sum()
        return pd.DataFrame({"vwap": vwap})

    @property
    def output_columns(self) -> list[str]:
        return ["vwap"]
