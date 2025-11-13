"""Dataset manifest loading and window sampling utilities."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import pyarrow.dataset as ds

from .config import DatasetManifest, DatasetSlice


def load_dataset_frame(path: str | Path) -> pd.DataFrame:
    """Load a parquet directory/file into a timestamp-indexed DataFrame."""

    dataset = ds.dataset(path, format="parquet")
    table = dataset.to_table()
    df = table.to_pandas()
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        df = df.set_index("timestamp")
    elif "__index_level_0__" in df.columns:
        df["timestamp"] = pd.to_datetime(df["__index_level_0__"], utc=True, errors="coerce")
        df = df.drop(columns="__index_level_0__").set_index("timestamp")
    else:
        df.index = pd.to_datetime(df.index, utc=True, errors="coerce")
    return df.sort_index()


def _to_utc_timestamp(value) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        return ts.tz_localize("UTC")
    return ts.tz_convert("UTC")


def load_manifest(path: str) -> DatasetManifest:
    """Load a dataset manifest from disk."""

    data = json.loads(Path(path).read_text())
    return DatasetManifest.model_validate(data)


@dataclass
class SampledWindow:
    frame: pd.DataFrame


class DatasetWindowSource:
    """Caches parquet slices and produces contiguous windows for the env."""

    def __init__(self, manifest: DatasetManifest):
        self.manifest = manifest
        self._cache: Dict[str, pd.DataFrame] = {}

    def _load_path(self, path: str) -> pd.DataFrame:
        cached = self._cache.get(path)
        if cached is not None:
            return cached

        df = load_dataset_frame(path)
        self._cache[path] = df
        return df

    def sample_window(
        self,
        rng: np.random.Generator,
        window_size: int,
        episode_minutes: int,
    ) -> SampledWindow:
        required = window_size + episode_minutes
        eligible: list[DatasetSlice] = [s for s in self.manifest.slices if s.rows >= required]
        if not eligible:
            raise ValueError("No dataset slices satisfy the requested window length")

        slice_cfg = eligible[int(rng.integers(0, len(eligible)))]
        frame = self._load_path(slice_cfg.path)
        start = _to_utc_timestamp(slice_cfg.start_ts)
        end = _to_utc_timestamp(slice_cfg.end_ts)
        subset = frame.loc[start:end]
        if len(subset) < required:
            raise ValueError(
                f"Slice {slice_cfg.path} only has {len(subset)} rows between {start} and {end}, need {required}"
            )

        max_offset = len(subset) - required
        offset = int(rng.integers(0, max_offset + 1)) if max_offset > 0 else 0
        window = subset.iloc[offset : offset + required].copy()
        return SampledWindow(frame=window)
