from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from app.models import CoverageEntry


def scan_coverage(data_dir: Path, exchange: str, symbol: str) -> List[CoverageEntry]:
    entries: List[CoverageEntry] = []
    base = data_dir / exchange / symbol.replace("/", "-")
    if not base.exists():
        return entries
    for timeframe_dir in base.iterdir():
        if not timeframe_dir.is_dir():
            continue
        timestamps = []
        for year_dir in timeframe_dir.glob("year=*"):
            for file in year_dir.glob("*.parquet"):
                timestamps.append(file.stat().st_mtime)
        if not timestamps:
            continue
        start_ts = min(timestamps)
        end_ts = max(timestamps)
        entries.append(
            CoverageEntry(
                exchange=exchange,
                symbol=symbol,
                timeframe=timeframe_dir.name,
                start_timestamp=int(start_ts * 1000),
                end_timestamp=int(end_ts * 1000),
                last_job_id=None,
                validated_at=None,
            )
        )
    return entries
