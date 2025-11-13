#!/usr/bin/env python
"""Generate a RunPod pod payload for a training/eval experiment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.rl.training_config import load_training_config

DEFAULT_IMAGE = "runpod/pytorch:2.5.1"
DEFAULT_CMD_PREFIX = "cd /workspace/TradeCore &&"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-config", required=True, help="Path to TrainingConfig file on the attached volume")
    parser.add_argument("--pod-name", default="tradecore-rl", help="Friendly pod name")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="Container image")
    parser.add_argument("--gpu-type-id", default="GPU-1234", help="RunPod gpuTypeId")
    parser.add_argument("--cloud-type", default="SECURE", help="RunPod cloud type")
    parser.add_argument("--volume-id", help="Network volume ID (if using volumes)")
    parser.add_argument("--volume-path", default="/workspace", help="Mount path for the network volume")
    parser.add_argument("--storage-gb", type=int, default=40, help="Container disk size in GB")
    parser.add_argument("--command-prefix", default=DEFAULT_CMD_PREFIX, help="Command prefix (cd into repo, etc.)")
    parser.add_argument("--episodes", type=int, default=2, help="Eval episodes to pass to run_experiment")
    parser.add_argument("--seed", type=int, default=5, help="Eval seed")
    parser.add_argument("--tag", default="pod", help="Suffix for experiment tag")
    parser.add_argument("--output", help="Optional path to save JSON payload")
    return parser.parse_args()


def build_payload(args: argparse.Namespace) -> dict:
    train_cfg = load_training_config(args.train_config)
    run_cmd = (
        f"{args.command_prefix} python scripts/run_experiment.py --train-config {args.train_config} "
        f"--episodes {args.episodes} --seed {args.seed} --tag {args.tag}"
    )

    env_vars = [
        {"key": "TRAIN_CONFIG", "value": args.train_config},
        {"key": "RUN_TAG", "value": args.tag},
    ]

    payload = {
        "name": args.pod_name,
        "imageName": args.image,
        "gpuTypeId": args.gpu_type_id,
        "cloudType": args.cloud_type,
        "containerDiskInGb": args.storage_gb,
        "env": env_vars,
        "ports": [],
        "cmd": run_cmd,
    }
    if args.volume_id:
        payload["volumeId"] = args.volume_id
        payload["volumeMountPath"] = args.volume_path
    return payload


def main() -> None:
    args = parse_args()
    payload = build_payload(args)
    text = json.dumps(payload, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(text)
        print(f"Saved payload to {output_path}")
    print(text)


if __name__ == "__main__":
    main()
