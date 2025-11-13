"""Observation builder utilities."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from gymnasium import spaces

from .config import ObservationConfig
from .execution import AccountState
from app.tools.indicator_registry import IndicatorRegistry


@dataclass
class ObservationSpec:
    market_features: int
    account_features: int


class ObservationBuilder:
    def __init__(
        self,
        config: ObservationConfig,
        account_scale: float,
        max_position: float,
        indicator_registry: IndicatorRegistry | None = None,
    ):
        self.config = config
        self.account_scale = account_scale
        self.max_position = max_position
        self.indicator_registry = indicator_registry
        indicator_features = indicator_registry.feature_count if indicator_registry else 0
        self.market_feature_count = 5 + (1 if config.include_returns else 0) + indicator_features
        self.account_feature_count = 4
        self.space = spaces.Dict(
            {
                "market": spaces.Box(
                    low=-np.inf,
                    high=np.inf,
                    shape=(config.window_size, self.market_feature_count),
                    dtype=np.float32,
                ),
                "account": spaces.Box(
                    low=-np.inf,
                    high=np.inf,
                    shape=(self.account_feature_count,),
                    dtype=np.float32,
                ),
            }
        )

    @property
    def window_size(self) -> int:
        return self.config.window_size

    def build(self, frame: pd.DataFrame, account: AccountState) -> dict[str, np.ndarray]:
        window = frame.iloc[-self.config.window_size :].copy()
        market = window[["open", "high", "low", "close", "volume"]].to_numpy(dtype=np.float32)

        if self.config.normalize_prices:
            ref_price = max(abs(market[-1, 3]), 1e-6)
            market[:, :4] = (market[:, :4] / ref_price) - 1.0
        volume_scale = max(self.config.volume_scale, 1e-6)
        market[:, 4] = market[:, 4] / volume_scale

        features = []
        if self.config.include_returns:
            returns = np.zeros((market.shape[0], 1), dtype=np.float32)
            close_prices = window["close"].to_numpy(dtype=np.float32)
            denom = np.clip(close_prices[:-1], 1e-6, None)
            returns[1:, 0] = (close_prices[1:] - close_prices[:-1]) / denom
            features.append(returns)

        if self.indicator_registry is not None:
            indicators = self.indicator_registry.compute(window)
            features.append(indicators.to_numpy(dtype=np.float32))

        if features:
            market = np.concatenate([market] + features, axis=1)

        account_vec = np.array(
            [
                account.position / self.max_position,
                account.cash / self.account_scale,
                account.equity / self.account_scale,
                account.drawdown,
            ],
            dtype=np.float32,
        )
        return {"market": market, "account": account_vec}
