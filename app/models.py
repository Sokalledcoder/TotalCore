from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional, List, Literal, Dict, Any

from pydantic import BaseModel, Field, validator, model_validator


SUPPORTED_EXCHANGES = {"kraken"}
SUPPORTED_TIMEFRAMES = {"1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "2w"}
DEFAULT_SYMBOLS = {"BTC/USD", "ETH/USD"}


def _ensure_timestamp(value: datetime | int | str | None) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return int(value.timestamp() * 1000)
    if isinstance(value, str) and value:
        try:
            return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp() * 1000)
        except ValueError:
            raise ValueError("Invalid datetime format") from None
    return int(value)


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class JobOptions(BaseModel):
    full_history: bool = False


class DataJobCreate(BaseModel):
    exchange: Literal["kraken"]
    symbol: str = Field(..., description="Unified CCXT symbol, e.g., BTC/USD")
    timeframe: str = Field(..., description="CCXT timeframe string")
    start_timestamp: Optional[int] = Field(None, description="Unix ms")
    end_timestamp: Optional[int] = Field(None, description="Unix ms")
    options: JobOptions = Field(default_factory=JobOptions)

    @validator("symbol")
    def validate_symbol(cls, value: str) -> str:
        if value not in DEFAULT_SYMBOLS:
            raise ValueError(f"Unsupported symbol {value}. Allowed: {sorted(DEFAULT_SYMBOLS)}")
        return value

    @validator("timeframe")
    def validate_timeframe(cls, value: str) -> str:
        if value not in SUPPORTED_TIMEFRAMES:
            raise ValueError(f"Unsupported timeframe {value}")
        return value

    @validator("start_timestamp", "end_timestamp", pre=True)
    def coerce_ts(cls, v):  # type: ignore
        return _ensure_timestamp(v)


class DataJob(BaseModel):
    id: str
    exchange: str
    symbol: str
    timeframe: str
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    status: JobStatus
    progress: float = 0.0
    created_at: datetime
    updated_at: datetime
    options: JobOptions
    details: Dict[str, Any] = Field(default_factory=dict)
    result: Dict[str, Any] = Field(default_factory=dict)


class CoverageEntry(BaseModel):
    exchange: str
    symbol: str
    timeframe: str
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    last_job_id: Optional[str]
    validated_at: Optional[datetime]


class JobAction(BaseModel):
    action: Literal["validate", "resume", "download"]
    payload: Dict[str, Any] = Field(default_factory=dict)


class IndicatorSelection(BaseModel):
    name: str
    params: Dict[str, Any] = Field(default_factory=dict)


class ExperimentLaunchRequest(BaseModel):
    env_config_path: str
    train_config_path: str
    indicator_manifest_path: Optional[str] = None
    indicator_manifest_inline: Optional[List[IndicatorSelection]] = None
    risk_pct: Optional[float] = Field(None, gt=0)
    stop_loss_steps: Optional[int] = Field(None, ge=1, le=10)
    limit_fee_pct: Optional[float] = Field(None, ge=0)
    market_fee_pct: Optional[float] = Field(None, ge=0)
    tag: str = Field(..., min_length=1, max_length=32)
    episodes: int = Field(1, ge=1, le=25)
    seed: int = 0

    @model_validator(mode="after")
    def validate_manifest_choice(cls, values: "ExperimentLaunchRequest") -> "ExperimentLaunchRequest":
        if values.indicator_manifest_path and values.indicator_manifest_inline:
            raise ValueError("Provide either indicator_manifest_path or indicator_manifest_inline, not both")
        return values


class ExperimentJob(BaseModel):
    id: str
    status: JobStatus
    tag: str
    train_config_path: str
    env_config_path: str
    episodes: int
    seed: int
    overrides: Dict[str, Any] = Field(default_factory=dict)
    result: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    workdir: str
    created_at: datetime
    updated_at: datetime


class ExperimentRunSummary(BaseModel):
    name: str
    run_dir: str
    created_at: datetime
    tag: str
    train_meta: Dict[str, Any] = Field(default_factory=dict)
    eval_summary: Dict[str, Any] = Field(default_factory=dict)
