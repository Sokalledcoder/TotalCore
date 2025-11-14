"""Configuration models for the RL environment."""
from __future__ import annotations

from datetime import datetime
from typing import List, Sequence, Literal

from pydantic import BaseModel, Field, field_validator


class DatasetSlice(BaseModel):
    """Represents a contiguous block of data available for sampling."""

    path: str
    start_ts: datetime = Field(description="Inclusive UTC timestamp for the start of the slice")
    end_ts: datetime = Field(description="Inclusive UTC timestamp for the end of the slice")
    rows: int = Field(ge=1, description="Number of rows stored within the slice range")

    @property
    def duration_minutes(self) -> int:
        return max(0, int((self.end_ts - self.start_ts).total_seconds() // 60) + 1)


class DatasetManifest(BaseModel):
    """Manifest describing the available dataset windows."""

    symbol: str
    timeframe: str
    slices: List[DatasetSlice]

    @field_validator("slices")
    @classmethod
    def validate_slices(cls, value: List[DatasetSlice]) -> List[DatasetSlice]:
        if not value:
            raise ValueError("Dataset manifest must define at least one slice")
        return value


class ObservationConfig(BaseModel):
    window_size: int = Field(64, ge=16)
    normalize_prices: bool = True
    include_returns: bool = True
    volume_scale: float = Field(1_000.0, gt=0)


class ActionConfig(BaseModel):
    direction_values: Sequence[int] = Field(default=(-1, 0, 1), description="Mapping for direction head: -1 short, 0 flat, 1 long")
    size_buckets: Sequence[float] = Field(default=(0.0, 0.25, 0.5, 1.0), description="Fractions of `max_position_size` to target")
    take_profit_steps: int = Field(1, ge=1)
    stop_loss_steps: int = Field(1, ge=1)


class RewardConfig(BaseModel):
    pnl_weight: float = 1.0
    fee_weight: float = 1.0
    drawdown_weight: float = 0.0
    position_penalty_weight: float = 0.0
    reward_scale: float = Field(1_000.0, gt=0)


class EnvConfig(BaseModel):
    dataset_manifest_path: str
    indicator_manifest_path: str | None = None
    initial_cash: float = Field(100_000.0, gt=0)
    max_position_size: float = Field(1.0, gt=0, description="Maximum absolute position in base units (e.g., BTC)")
    fee_bps: float = Field(1.0, ge=0, description="Commission in basis points per notional traded")
    slippage_bps: float = Field(2.0, ge=0)
    episode_minutes: int = Field(240, ge=32)
    risk_pct: float = Field(0.01, gt=0)
    stop_loss_bps: float = Field(50.0, gt=0)
    limit_fee_bps: float = Field(0.02, ge=0)
    market_fee_bps: float = Field(0.05, ge=0)
    observation: ObservationConfig = Field(default_factory=ObservationConfig)
    action: ActionConfig = Field(default_factory=ActionConfig)
    reward: RewardConfig = Field(default_factory=RewardConfig)
    risk_sizing_mode: Literal["bucketed", "risk_based"] = "bucketed"

    @property
    def fee_rate(self) -> float:
        return self.fee_bps / 10_000.0

    @property
    def slippage_rate(self) -> float:
        return self.slippage_bps / 10_000.0

    @property
    def limit_fee_rate(self) -> float:
        return self.limit_fee_bps / 10_000.0

    @property
    def market_fee_rate(self) -> float:
        return self.market_fee_bps / 10_000.0
