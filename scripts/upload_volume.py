#!/usr/bin/env python
"""
Upload local parquet slices to the RunPod S3-backed network volume in batches.
Reads AWS credentials from the environment.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterator, Set

import boto3


def iter_existing_keys(s3, bucket: str, prefix: str) -> Iterator[str]:
    continuation_token = None
    while True:
        kwargs = {"Bucket": bucket, "Prefix": prefix}
        if continuation_token:
            kwargs["ContinuationToken"] = continuation_token
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp.get("Contents", []):
            yield obj["Key"]
        if not resp.get("IsTruncated"):
            break
        continuation_token = resp.get("NextContinuationToken")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bucket", default="6wlciwn57c")
    parser.add_argument("--endpoint", default="https://s3api-eu-ro-1.runpod.io")
    parser.add_argument("--region", default="eu-ro-1")
    parser.add_argument("--source", default="data/lake/kraken/BTC-USD/1m")
    parser.add_argument("--prefix", default="TradeCore/data/lake/kraken/BTC-USD/1m")
    parser.add_argument("--start", type=int, default=0, help="Start index in the sorted file list")
    parser.add_argument("--limit", type=int, default=500, help="Max files per run to avoid CLI timeouts")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip S3 objects that already exist (slower due to listing)",
    )
    args = parser.parse_args()

    if not os.environ.get("AWS_ACCESS_KEY_ID") or not os.environ.get("AWS_SECRET_ACCESS_KEY"):
        raise SystemExit("AWS credentials not found in environment")

    s3 = boto3.client("s3", endpoint_url=args.endpoint, region_name=args.region)

    source_root = Path(args.source)
    if not source_root.exists():
        raise SystemExit(f"Source directory {source_root} not found")

    all_files = sorted(source_root.rglob("*.parquet"))
    selection = all_files[args.start : args.start + args.limit]
    if not selection:
        print("No files to upload for the requested slice.")
        return

    existing: Set[str] = set()
    if args.skip_existing:
        existing = set(iter_existing_keys(s3, args.bucket, args.prefix))
        print(f"Skip-existing enabled: found {len(existing)} existing keys")

    uploaded = 0
    for local_path in selection:
        rel = local_path.relative_to(source_root)
        key = f"{args.prefix}/{rel.as_posix()}"
        if existing and key in existing:
            continue
        s3.upload_file(str(local_path), args.bucket, key)
        uploaded += 1
        if uploaded % 100 == 0:
            print(f"Uploaded {uploaded} files in this batch...")
    print(f"Uploaded {uploaded} files (requested slice start={args.start}, limit={args.limit})")


if __name__ == "__main__":
    main()
