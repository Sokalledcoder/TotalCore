#!/usr/bin/env python
"""Validate indicator manifests against dataset slices before training."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from app.rl.config import EnvConfig
from app.rl.datasets import DatasetManifest, load_dataset_frame, load_manifest
from app.tools import IndicatorRegistry

REQUIRED_COLUMNS = ("open", "high", "low", "close", "volume")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-config", help="EnvConfig JSON file to infer manifest paths")
    parser.add_argument("--dataset-manifest", help="Override dataset manifest path")
    parser.add_argument("--indicator-manifest", help="Override indicator manifest path")
    parser.add_argument("--sample-rows", type=int, default=512, help="Rows to sample per slice")
    parser.add_argument("--max-slices", type=int, default=2, help="How many slices to validate (0 = all)")
    parser.add_argument("--window-size", type=int, default=128, help="Observation window (if no env config)")
    parser.add_argument("--output", help="Optional path to write JSON summary")
    return parser.parse_args()


def _load_env_config(path: str | None) -> Optional[EnvConfig]:
    if not path:
        return None
    data = json.loads(Path(path).read_text())
    return EnvConfig.model_validate(data)


def _load_indicator_registry(path: str | None) -> IndicatorRegistry | None:
    if not path:
        return None
    return IndicatorRegistry.from_manifest(path)


def _validate_slice(
    slice_idx: int,
    manifest_slice,
    sample_rows: int,
    indicator_registry: IndicatorRegistry | None,
) -> tuple[Dict[str, Any], list[str]]:
    errors: list[str] = []
    df = load_dataset_frame(manifest_slice.path)
    window = df.loc[manifest_slice.start_ts : manifest_slice.end_ts]
    if window.empty:
        errors.append(
            f"slice#{slice_idx} [{manifest_slice.start_ts} → {manifest_slice.end_ts}] returned 0 rows in {manifest_slice.path}"
        )
        return {
            "slice_index": slice_idx,
            "path": manifest_slice.path,
            "rows_manifest": manifest_slice.rows,
            "rows_available": 0,
            "columns_ok": False,
            "indicator_features": indicator_registry.feature_count if indicator_registry else 0,
        }, errors

    sample = window.iloc[:sample_rows]
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in sample.columns]
    columns_ok = not missing_cols
    if missing_cols:
        errors.append(f"slice#{slice_idx} missing columns: {missing_cols}")

    indicator_report: Dict[str, Any] = {}
    if indicator_registry:
        indicator_frame = indicator_registry.compute(sample)
        indicator_nan = bool(np.isnan(indicator_frame.to_numpy(dtype=np.float64)).any())
        if indicator_frame.shape[1] != indicator_registry.feature_count:
            errors.append(
                f"slice#{slice_idx} expected {indicator_registry.feature_count} indicator cols, got {indicator_frame.shape[1]}"
            )
        if indicator_nan:
            errors.append(f"slice#{slice_idx} indicator output contains NaN values")
        indicator_report = {
            "indicator_columns": indicator_frame.columns.tolist(),
            "indicator_features": indicator_registry.feature_count,
        }

    slice_report = {
        "slice_index": slice_idx,
        "path": manifest_slice.path,
        "rows_manifest": manifest_slice.rows,
        "rows_available": int(len(window)),
        "sampled_rows": int(len(sample)),
        "start_ts": manifest_slice.start_ts.isoformat(),
        "end_ts": manifest_slice.end_ts.isoformat(),
        "columns_ok": columns_ok,
        "missing_columns": missing_cols,
    }
    slice_report.update(indicator_report)
    return slice_report, errors


def main() -> None:
    args = parse_args()
    env_cfg = _load_env_config(args.env_config)
    dataset_manifest_path = args.dataset_manifest or (env_cfg.dataset_manifest_path if env_cfg else None)
    indicator_manifest_path = args.indicator_manifest or (env_cfg.indicator_manifest_path if env_cfg else None)
    if not dataset_manifest_path:
        raise SystemExit("Provide --dataset-manifest or an --env-config with dataset_manifest_path")

    indicator_registry = _load_indicator_registry(indicator_manifest_path)
    manifest = load_manifest(dataset_manifest_path)

    sample_rows = max(args.sample_rows, env_cfg.observation.window_size if env_cfg else args.window_size)
    max_slices = args.max_slices if args.max_slices > 0 else len(manifest.slices)

    reports: List[Dict[str, Any]] = []
    errors: List[str] = []
    for idx, manifest_slice in enumerate(manifest.slices[:max_slices]):
        report, slice_errors = _validate_slice(idx, manifest_slice, sample_rows, indicator_registry)
        reports.append(report)
        errors.extend(slice_errors)

    summary = {
        "dataset_manifest": dataset_manifest_path,
        "indicator_manifest": indicator_manifest_path,
        "sample_rows": sample_rows,
        "slices_checked": len(reports),
        "status": "ok" if not errors else "error",
        "slices": reports,
        "errors": errors,
    }

    output_text = json.dumps(summary, indent=2)
    print(output_text)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text)

    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
