#!/usr/bin/env python
"""Stub RunPod client for local testing."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", required=True, help="Path to pod payload JSON")
    parser.add_argument("--output", default="runpod_submissions", help="Directory to store mock submissions")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(Path(args.payload).read_text())
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = out_dir / f"submission_{timestamp}.json"
    target.write_text(json.dumps(payload, indent=2))
    print(f"[mock-runpod] saved payload -> {target}")


if __name__ == "__main__":
    main()
