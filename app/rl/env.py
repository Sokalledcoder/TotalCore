"""Gymnasium-compatible trading environment."""
from __future__ import annotations

from typing import Any, Dict

import gymnasium as gym
import numpy as np
import pandas as pd

from .actions import ActionSpec
from .config import EnvConfig
from .datasets import DatasetWindowSource, SampledWindow, load_manifest
from .execution import AccountState, ExecutionEngine
from .rewards import RewardCalculator
from .state_builder import ObservationBuilder
from app.tools import IndicatorRegistry, RiskGuard


class TradeEnvironment(gym.Env):
    metadata = {"render.modes": []}

    def __init__(self, config: EnvConfig):
        self.config = config
        self.manifest = load_manifest(config.dataset_manifest_path)
        self.dataset = DatasetWindowSource(self.manifest)
        self.rng = np.random.default_rng()

        self.indicators = None
        if config.indicator_manifest_path:
            self.indicators = IndicatorRegistry.from_manifest(config.indicator_manifest_path)

        self.action_spec = ActionSpec(config.action)
        self.execution = ExecutionEngine(
            max_position=config.max_position_size,
            limit_fee_rate=config.limit_fee_rate,
            market_fee_rate=config.market_fee_rate,
            slippage_rate=config.slippage_rate,
        )
        self.risk_guard = RiskGuard(
            risk_pct=config.risk_pct,
            stop_loss_bps=config.stop_loss_bps,
            max_position=config.max_position_size,
            sizing_mode=config.risk_sizing_mode,
        )
        self.reward_calc = RewardCalculator(config.reward, scale=config.initial_cash)
        self.obs_builder = ObservationBuilder(
            config.observation,
            account_scale=config.initial_cash,
            max_position=config.max_position_size,
            indicator_registry=self.indicators,
        )
        self.action_space = self.action_spec.space
        self.observation_space = self.obs_builder.space

        self._current_window: pd.DataFrame | None = None
        self._cursor: int = 0
        self._account: AccountState | None = None

    def reset(self, *, seed: int | None = None, options: Dict[str, Any] | None = None):
        super().reset(seed=seed)
        if seed is not None:
            self.rng = np.random.default_rng(seed)

        sampled = self.dataset.sample_window(
            rng=self.rng,
            window_size=self.obs_builder.window_size,
            episode_minutes=self.config.episode_minutes,
        )
        self._current_window = sampled.frame
        self._cursor = self.obs_builder.window_size

        initial_price = float(self._current_window.iloc[self._cursor - 1]["close"])
        self._account = AccountState(
            cash=self.config.initial_cash,
            position=0.0,
            equity=self.config.initial_cash,
            peak_equity=self.config.initial_cash,
            drawdown=0.0,
            last_price=initial_price,
        )
        self._account.mark_to_market(initial_price)
        obs = self.obs_builder.build(self._current_window.iloc[: self._cursor], self._account)
        info = self._build_info()
        return obs, info

    def step(self, action: Dict[str, int]):
        if self._current_window is None or self._account is None:
            raise RuntimeError("Environment must be reset before stepping")

        decoded = self.action_spec.decode(action)
        current_price = float(self._current_window.iloc[self._cursor - 1]["close"])
        risk_plan = self.risk_guard.plan(decoded, current_price, self._account)
        fees_paid = self.execution.execute_limit(risk_plan.target_units, current_price, self._account)
        self._account.stop_price = risk_plan.stop_price
        prev_equity = self._account.equity

        self._cursor += 1
        terminated = False
        if self._cursor >= len(self._current_window):
            self._cursor = len(self._current_window)
            terminated = True
            next_price = current_price
        else:
            next_price = float(self._current_window.iloc[self._cursor - 1]["close"])

        self._account.mark_to_market(next_price)
        stop_fees = self._apply_stop_if_triggered(next_price)
        equity_delta = self._account.equity - prev_equity
        reward_result = self.reward_calc.compute(equity_delta, fees_paid + stop_fees, self._account)

        if terminated:
            obs_window = self._current_window.iloc[self._cursor - self.obs_builder.window_size : self._cursor]
        else:
            obs_window = self._current_window.iloc[self._cursor - self.obs_builder.window_size : self._cursor]
        obs = self.obs_builder.build(obs_window, self._account)

        info = self._build_info()
        info.update(
            {
                "target_position": risk_plan.target_units,
                "desired_position": decoded.direction * risk_plan.desired_units,
                "risk_units": risk_plan.risk_units,
                "risk_capital": risk_plan.risk_capital,
                "stop_distance": risk_plan.stop_distance,
                "limit_fee": fees_paid,
                "stop_fee": stop_fees,
                "decision_direction": decoded.direction,
                "decision_size_fraction": decoded.size_fraction,
                "decision_stop_loss_idx": decoded.stop_loss_idx,
                "decision_take_profit_idx": decoded.take_profit_idx,
            }
        )
        info.update(reward_result.info)
        truncated = False
        return obs, reward_result.reward, terminated, truncated, info

    def render(self):
        return None

    def _build_info(self) -> Dict[str, Any]:
        if self._account is None:
            return {}
        return {
            "cash": self._account.cash,
            "position": self._account.position,
            "equity": self._account.equity,
            "drawdown": self._account.drawdown,
            "stop_price": self._account.stop_price,
        }

    def _apply_stop_if_triggered(self, price: float) -> float:
        if self._account is None or self._account.stop_price is None:
            return 0.0
        stop_price = self._account.stop_price
        position = self._account.position
        if position > 0 and price <= stop_price:
            return self.execution.close_position_market(stop_price, self._account)
        if position < 0 and price >= stop_price:
            return self.execution.close_position_market(stop_price, self._account)
        return 0.0
