"""
task_gravity_deep.run
=====================
End-to-end pipeline:

  for each (training_noise, eval_noise) in grid:
      train PPO (or load from cache)
      measure TRR / CTRR at multiple eval_noise levels
      append to CSV

Usage:

    python -u -m src.run                   # full grid
    python -u -m src.run --quick           # 1 noise setting, fewer timesteps
    python -u -m src.run --skip-train      # only evaluate (assume checkpoints exist)
"""

from __future__ import annotations

import os
import sys
import csv
import json
import argparse
from pathlib import Path
from typing import List, Dict

import numpy as np
from stable_baselines3 import PPO

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.train import train_ppo
from src.evaluate import summarize


CKPT_DIR = ROOT / "checkpoints"
RESULTS_DIR = ROOT / "results"
LOG_DIR = ROOT / "logs"


def _ckpt_path(noise: float, seed: int) -> Path:
    name = f"ppo_noise{noise:.2f}_seed{seed}.zip"
    return CKPT_DIR / name


def get_or_train(
    train_noise: float,
    seed: int,
    timesteps: int,
    force_retrain: bool = False,
) -> PPO:
    path = _ckpt_path(train_noise, seed)
    if path.exists() and not force_retrain:
        # SB3 needs the .zip suffix to load
        return PPO.load(str(path).replace(".zip", ""), device="cpu")
    print(f"[train] noise={train_noise} seed={seed} timesteps={timesteps}", flush=True)
    model = train_ppo(
        timesteps=timesteps,
        attractor_bias=0.7,
        task_emb_noise=train_noise,
        seed=seed,
        save_path=str(path).replace(".zip", ""),
    )
    return model


def run_full(
    train_noises=(0.0, 0.3, 0.7),
    eval_noises=(0.0, 0.3, 0.7),
    seeds=(0, 1, 2),
    timesteps: int = 30_000,
    skip_train: bool = False,
) -> List[Dict]:
    os.makedirs(RESULTS_DIR, exist_ok=True)
    rows: List[Dict] = []
    for tn in train_noises:
        for seed in seeds:
            if skip_train:
                model = PPO.load(str(_ckpt_path(tn, seed)).replace(".zip", ""), device="cpu")
            else:
                model = get_or_train(tn, seed, timesteps)
            for en in eval_noises:
                s = summarize(model, task_emb_noise=en, seed=seed + 1000)
                row = {
                    "train_noise": tn,
                    "eval_noise": en,
                    "seed": seed,
                    **s,
                }
                rows.append(row)
                print(f"   tn={tn} en={en} seed={seed} -> {row}", flush=True)
    csv_path = RESULTS_DIR / "deep_trr_ctrr_table.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    json_path = RESULTS_DIR / "deep_trr_ctrr_table.json"
    with open(json_path, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"[done] wrote {csv_path}", flush=True)
    return rows


def print_summary(rows: List[Dict]) -> None:
    from collections import defaultdict
    by: Dict = defaultdict(list)
    for r in rows:
        by[(r["train_noise"], r["eval_noise"])].append(r)
    header = f"{'train_n':<8}{'eval_n':<8}{'TRR_within':<14}{'TRR_x_ep':<14}{'CTRR':<10}{'unique':<8}{'traj_len':<10}"
    print(header, flush=True)
    for (tn, en), rs in sorted(by.items()):
        trr_w = np.array([r["TRR_within"] for r in rs])
        trr_a = np.array([r["TRR_across_episodes"] for r in rs])
        ctrrs = np.array([r["CTRR"] for r in rs])
        us = np.array([r["unique_states"] for r in rs])
        tls = np.array([r["trajectory_length"] for r in rs])
        print(
            f"{tn:<8}{en:<8}"
            f"{trr_w.mean():.3f}±{trr_w.std():.3f}   "
            f"{trr_a.mean():.3f}±{trr_a.std():.3f}   "
            f"{ctrrs.mean():.3f}±{ctrrs.std():.3f}  "
            f"{us.mean():.1f}    "
            f"{tls.mean():.0f}",
            flush=True,
        )


# ----------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true",
                        help="Reduced sweep (1 noise, 1 seed, 5k steps)")
    parser.add_argument("--skip-train", action="store_true",
                        help="Only evaluate (use cached checkpoints)")
    parser.add_argument("--timesteps", type=int, default=30_000)
    args = parser.parse_args()

    if args.quick:
        rows = run_full(
            train_noises=(0.0,),
            eval_noises=(0.0, 0.7),
            seeds=(0,),
            timesteps=5_000,
            skip_train=args.skip_train,
        )
    else:
        rows = run_full(
            train_noises=(0.0, 0.3, 0.7),
            eval_noises=(0.0, 0.3, 0.7),
            seeds=(0, 1, 2),
            timesteps=args.timesteps,
            skip_train=args.skip_train,
        )
    print("\n========= DEEP-AGENT SUMMARY =========", flush=True)
    print_summary(rows)