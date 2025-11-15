"""Registry + loader for indicator tools."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .base import Indicator
from .indicators.adx import ADXIndicator
from .indicators.atr import ATRIndicator
from .indicators.bbands import BollingerBandsIndicator
from .indicators.macd import MACDIndicator
from .indicators.rsi import RSIIndicator
from .indicators.vwap import VWAPIndicator
from .indicators.zscore import ZScoreIndicator

_INDICATOR_DEFINITIONS: Dict[str, Dict] = {
    "vwap": {
        "class": VWAPIndicator,
        "label": "VWAP",
        "description": "Rolling volume-weighted average price.",
        "params": [
            {"key": "window", "label": "Window", "type": "int", "default": 30, "min": 1, "max": 500, "step": 1},
        ],
    },
    "zscore": {
        "class": ZScoreIndicator,
        "label": "Z-Score",
        "description": "Standard score of a price field over a rolling window.",
        "params": [
            {"key": "window", "label": "Window", "type": "int", "default": 60, "min": 5, "max": 500, "step": 1},
            {
                "key": "field",
                "label": "Field",
                "type": "choice",
                "options": ["open", "high", "low", "close"],
                "default": "close",
            },
        ],
    },
    "atr": {
        "class": ATRIndicator,
        "label": "ATR",
        "description": "Average true range (volatility).",
        "params": [
            {"key": "window", "label": "Window", "type": "int", "default": 14, "min": 1, "max": 500, "step": 1},
        ],
    },
    "rsi": {
        "class": RSIIndicator,
        "label": "RSI",
        "description": "Relative Strength Index oscillator.",
        "params": [
            {"key": "window", "label": "Window", "type": "int", "default": 14, "min": 2, "max": 200, "step": 1},
            {
                "key": "field",
                "label": "Field",
                "type": "choice",
                "options": ["open", "high", "low", "close"],
                "default": "close",
            },
        ],
    },
    "bollinger": {
        "class": BollingerBandsIndicator,
        "label": "Bollinger Bands",
        "description": "Upper/lower bands and width based on rolling std dev.",
        "params": [
            {"key": "window", "label": "Window", "type": "int", "default": 20, "min": 5, "max": 500, "step": 1},
            {
                "key": "std_mult",
                "label": "Std Multiplier",
                "type": "float",
                "default": 2.0,
                "min": 0.5,
                "max": 5.0,
                "step": 0.1,
            },
            {
                "key": "field",
                "label": "Field",
                "type": "choice",
                "options": ["open", "high", "low", "close"],
                "default": "close",
            },
        ],
    },
    "adx": {
        "class": ADXIndicator,
        "label": "ADX",
        "description": "Average Directional Index (trend strength).",
        "params": [
            {"key": "window", "label": "Window", "type": "int", "default": 14, "min": 5, "max": 200, "step": 1},
        ],
    },
    "macd": {
        "class": MACDIndicator,
        "label": "MACD",
        "description": "Moving Average Convergence Divergence.",
        "params": [
            {"key": "fast", "label": "Fast EMA", "type": "int", "default": 12, "min": 2, "max": 100, "step": 1},
            {"key": "slow", "label": "Slow EMA", "type": "int", "default": 26, "min": 2, "max": 200, "step": 1},
            {"key": "signal", "label": "Signal EMA", "type": "int", "default": 9, "min": 1, "max": 100, "step": 1},
            {
                "key": "field",
                "label": "Field",
                "type": "choice",
                "options": ["open", "high", "low", "close"],
                "default": "close",
            },
        ],
    },
}


class IndicatorRegistry:
    def __init__(self, indicators: List[Indicator]):
        self._indicators = indicators
        self.feature_count = sum(len(ind.output_columns) for ind in indicators)

    @classmethod
    def from_manifest(cls, path: str | Path) -> IndicatorRegistry:
        data = json.loads(Path(path).read_text())
        indicators = []
        for item in data.get("indicators", []):
            name = item.get("name")
            params = item.get("params", {})
            indicator_cls = _INDICATOR_DEFINITIONS.get(name, {}).get("class")
            if not indicator_cls:
                raise ValueError(f"Unknown indicator: {name}")
            indicators.append(indicator_cls(**params))
        return cls(indicators)

    def compute(self, frame: pd.DataFrame) -> pd.DataFrame:
        if not self._indicators:
            return pd.DataFrame(index=frame.index)

        columns = []
        for indicator in self._indicators:
            indicator_frame = indicator.compute(frame)
            aligned = indicator_frame.reindex(frame.index)
            columns.append(aligned)
        return pd.concat(columns, axis=1).fillna(0.0)


def list_indicator_specs() -> List[Dict]:
    specs: List[Dict] = []
    for name, meta in _INDICATOR_DEFINITIONS.items():
        specs.append(
            {
                "name": name,
                "label": meta.get("label", name.title()),
                "description": meta.get("description", ""),
                "params": meta.get("params", []),
            }
        )
    return sorted(specs, key=lambda entry: entry["label"].lower())
