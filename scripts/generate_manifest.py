#!/usr/bin/env python
"""Generate dataset manifests by scanning Parquet candle directories."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import pyarrow.dataset as ds


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", required=True, help="Directory containing Parquet files for a timeframe.")
    parser.add_argument("--output", required=True, help="Where to write the manifest JSON.")
    parser.add_argument("--symbol", default="BTC/USD")
    parser.add_argument("--timeframe", default="1m")
    parser.add_argument("--min-rows-per-day", type=int, default=1300, help="Require at least this many rows per day.")
    parser.add_argument(
        "--max-rows-per-day",
        type=int,
        default=2000,
        help="Reject days exceeding this many rows (helps skip duplicates).",
    )
    parser.add_argument(
        "--min-slice-days",
        type=int,
        default=7,
        help="Emit slices only when contiguous qualifying days reach this length.",
    )
    return parser.parse_args()


def _load_frame(dataset_dir: Path) -> pd.DataFrame:
    dataset = ds.dataset(str(dataset_dir), format="parquet")
    table = dataset.to_table()
    df = table.to_pandas()
    if "timestamp" in df.columns:
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
    elif "__index_level_0__" in df.columns:
        ts = pd.to_datetime(df["__index_level_0__"], utc=True, errors="coerce")
        df = df.drop(columns="__index_level_0__")
    else:
        ts = pd.to_datetime(df.index, utc=True, errors="coerce")
    df.index = ts
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    return df


def _find_slices(
    df: pd.DataFrame,
    min_rows: int,
    max_rows: int,
    min_days: int,
) -> List[Tuple[pd.Timestamp, pd.Timestamp, int]]:
    daily_counts = df.groupby(df.index.normalize()).size().sort_index()
    slices: List[Tuple[pd.Timestamp, pd.Timestamp, int]] = []
    run_start = None
    run_rows = 0
    previous_day = None

    def flush():
        nonlocal run_start, run_rows, previous_day
        if run_start is not None and previous_day is not None:
            days = (previous_day - run_start).days + 1
            if days >= min_days:
                mask = (df.index.normalize() >= run_start) & (df.index.normalize() <= previous_day)
                subset = df.loc[mask]
                slices.append((subset.index.min(), subset.index.max(), len(subset)))
            run_start = None
            run_rows = 0

    for day, count in daily_counts.items():
        day = pd.Timestamp(day)
        if day.tzinfo is None:
            day = day.tz_localize("UTC")
        else:
            day = day.tz_convert("UTC")
        qualifies = min_rows <= count <= max_rows
        if previous_day is not None and (day - previous_day).days > 1:
            flush()
        if qualifies:
            if run_start is None:
                run_start = day
            run_rows += count
        else:
            flush()
        previous_day = day

    flush()
    return slices


def main() -> None:
    args = parse_args()
    dataset_dir = Path(args.dataset_dir)
    if not dataset_dir.exists():
        raise SystemExit(f"Dataset directory does not exist: {dataset_dir}")

    frame = _load_frame(dataset_dir)
    slices = _find_slices(
        frame,
        min_rows=args.min_rows_per_day,
        max_rows=args.max_rows_per_day,
        min_days=args.min_slice_days,
    )
    if not slices:
        raise SystemExit("No qualifying slices found with current thresholds")

    manifest = {
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "slices": [
            {
                "path": str(dataset_dir),
                "start_ts": start.isoformat().replace("+00:00", "Z"),
                "end_ts": end.isoformat().replace("+00:00", "Z"),
                "rows": rows,
            }
            for start, end, rows in slices
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2))

    print(f"Wrote {len(slices)} slice(s) to {output_path}")
    for idx, slice_info in enumerate(manifest["slices"], start=1):
        print(
            f"[{idx}] {slice_info['start_ts']} → {slice_info['end_ts']} | rows={slice_info['rows']} | path={slice_info['path']}"
        )


if __name__ == "__main__":
    main()
