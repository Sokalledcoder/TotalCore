#!/usr/bin/env python
"""End-to-end local experiment runner (train + eval)."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from app.rl.training_config import load_training_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-config", required=True, help="Path to TrainingConfig (JSON/YAML)")
    parser.add_argument("--episodes", type=int, default=3, help="Eval episodes after training")
    parser.add_argument("--seed", type=int, default=0, help="Evaluation seed")
    parser.add_argument("--tag", default="local", help="Label appended to run directory")
    parser.add_argument(
        "--output-root",
        default="runs/experiments",
        help="Directory where experiment artifacts will be stored",
    )
    parser.add_argument(
        "--archive",
        help="Optional path (tar.gz) to store an archive of the run directory",
    )
    return parser.parse_args()


def run_train(train_config_path: str) -> dict:
    cmd = [
        "python",
        "scripts/train_sb3.py",
        "--train-config",
        train_config_path,
    ]
    subprocess.run(cmd, check=True)
    cfg = load_training_config(train_config_path)
    meta_path = Path(f"{cfg.save_path}_meta.json")
    if not meta_path.exists():
        raise FileNotFoundError(f"Expected metadata file not found: {meta_path}")
    meta = json.loads(meta_path.read_text())
    return meta


def run_eval(meta: dict, episodes: int, seed: int, summary_path: Path) -> dict:
    model_path = f"{meta['save_path']}.zip"
    env_config = meta["env_config_path"]
    vec_path = meta.get("vecnormalize_path")

    cmd = [
        "python",
        "scripts/eval_sb3.py",
        "--model",
        model_path,
        "--env-config",
        env_config,
        "--algo",
        meta["algorithm"],
        "--episodes",
        str(episodes),
        "--seed",
        str(seed),
        "--output",
        str(summary_path),
    ]
    if vec_path:
        cmd.extend(["--vecnormalize", vec_path])
    subprocess.run(cmd, check=True)
    return json.loads(summary_path.read_text())


def main() -> None:
    args = parse_args()
    train_cfg = load_training_config(args.train_config)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = Path(args.output_root) / f"{timestamp}_{args.tag}"
    run_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(args.train_config, run_dir / Path(args.train_config).name)

    print("[run] training...")
    train_meta = run_train(args.train_config)

    summary_path = run_dir / "eval_summary.json"
    print("[run] evaluating...")
    eval_summary = run_eval(train_meta, args.episodes, args.seed, summary_path)

    combined = {
        "train_meta": train_meta,
        "eval_summary": eval_summary,
        "train_config": args.train_config,
        "episodes": args.episodes,
        "seed": args.seed,
        "run_dir": str(run_dir),
    }
    (run_dir / "experiment.json").write_text(json.dumps(combined, indent=2))
    if args.archive:
        archive_path = Path(args.archive)
        if archive_path.suffix not in {".tar", ".gz", ".tgz", ".tar.gz"}:
            archive_path = archive_path.with_suffix(".tar.gz")
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(run_dir, arcname=run_dir.name)
        print(f"[run] archived artifacts -> {archive_path}")
    print(json.dumps({"run_dir": str(run_dir), "mean_reward": eval_summary["mean_reward"]}, indent=2))


if __name__ == "__main__":
    main()
