"""Registry + loader for indicator tools."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .base import Indicator
from .indicators.vwap import VWAPIndicator
from .indicators.zscore import ZScoreIndicator

_INDICATOR_MAP: Dict[str, type[Indicator]] = {
    "vwap": VWAPIndicator,
    "zscore": ZScoreIndicator,
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
            indicator_cls = _INDICATOR_MAP.get(name)
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
