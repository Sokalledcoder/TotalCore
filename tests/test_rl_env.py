from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from app.rl import EnvConfig, TradeEnvironment
from app.rl.config import ObservationConfig


def _write_sample_dataset(base_path: Path, rows: int = 512) -> tuple[str, int]:
    idx = pd.date_range("2025-09-13", periods=rows, freq="1min", tz="UTC")
    prices = np.linspace(30_000, 31_000, num=rows)
    frame = pd.DataFrame(
        {
            "open": prices,
            "high": prices + 10,
            "low": prices - 10,
            "close": prices + 5,
            "volume": np.linspace(0.5, 1.5, num=rows),
        },
        index=idx,
    )
    data_dir = base_path / "lake" / "kraken" / "BTC-USD" / "1m" / "year=2025"
    data_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = data_dir / "part.parquet"
    frame.to_parquet(parquet_path)
    return str(data_dir), len(frame)


def _write_manifest(path: Path, data_path: str, rows: int) -> Path:
    manifest = {
        "symbol": "BTC/USD",
        "timeframe": "1m",
        "slices": [
            {
                "path": data_path,
                "start_ts": "2025-09-13T00:00:00Z",
                "end_ts": "2025-09-13T23:59:00Z",
                "rows": rows,
            }
        ],
    }
    manifest_path = path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    return manifest_path


def test_env_reset_and_step(tmp_path):
    data_path, rows = _write_sample_dataset(tmp_path)
    manifest_path = _write_manifest(tmp_path, data_path, rows)
    config = EnvConfig(
        dataset_manifest_path=str(manifest_path),
        observation=ObservationConfig(window_size=32),
        episode_minutes=64,
        initial_cash=10_000.0,
        max_position_size=0.5,
    )
    env = TradeEnvironment(config)
    obs, info = env.reset(seed=123)
    assert obs["market"].shape == (32, 6)
    assert obs["account"].shape == (4,)
    assert info["cash"] == config.initial_cash

    action = env.action_space.sample()
    next_obs, reward, terminated, truncated, _ = env.step(action)
    assert isinstance(reward, float)
    assert next_obs["market"].shape == (32, 6)
    assert terminated in (True, False)
    assert truncated is False
