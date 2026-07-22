"""
task_gravity.experiment
=======================
End-to-end pipeline:

  1. Train each agent on the multi-task grid (biased toward T0).
  2. Evaluate on long rollouts; record TRR (across episodes).
  3. Force task switches; record CTRR.
  4. Write CSV table to experiment/results/.

Run:

    python -m src.experiment
"""

from __future__ import annotations

import os
import csv
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiment"))
sys.path.insert(0, str(ROOT / "experiment" / "src"))

from src.env import MultiTaskGrid, state_key
from src.agents import make_agent
from src.metrics import (
    trr_within_episode,
    trr_across_episodes,
    ctrr,
    summary,
)


# ----------------------------------------------------------------------
def train_one(
    agent_name: str,
    n_episodes: int = 400,
    attractor_task_id: int = 0,
    attractor_bias: float = 0.7,
    seed: int = 0,
    task_emb_noise: float = 0.0,
) -> object:
    """Train the agent. With probability attractor_bias, sample the attractor task."""
    env = MultiTaskGrid(seed=seed, task_emb_noise=task_emb_noise)
    agent = make_agent(agent_name, seed=seed)
    rng = np.random.RandomState(seed + 1)

    for ep in range(n_episodes):
        if rng.rand() < attractor_bias:
            task_id = attractor_task_id
        else:
            task_id = rng.randint(0, 3)
        obs = env.reset(task_id=task_id)
        done = False
        while not done:
            a = agent.select_action(obs)
            next_obs, r, done, _ = env.step(a)
            if hasattr(agent, "update"):
                agent.update(obs, r, next_obs, done)
            obs = next_obs
    return agent


# ----------------------------------------------------------------------
def evaluate_episodes(
    agent,
    n_episodes: int = 30,
    attractor_task_id: int = 0,
    max_steps_per_ep: int = 200,
    seed: int = 999,
    task_emb_noise: float = 0.0,
) -> Tuple[List[List[Dict]], List[Dict]]:
    """
    Evaluate the agent on the attractor task for `n_episodes` short episodes.
    Returns (per-episode-trajectories, flat-trajectory).
    """
    env = MultiTaskGrid(seed=seed, task_emb_noise=task_emb_noise)
    episodes: List[List[Dict]] = []
    flat: List[Dict] = []
    for i in range(n_episodes):
        obs = env.reset(task_id=attractor_task_id)
        traj = [obs]
        done = False
        steps = 0
        while not done and steps < max_steps_per_ep:
            a = agent.select_action(obs)
            next_obs, r, done, _ = env.step(a)
            traj.append(next_obs)
            obs = next_obs
            steps += 1
        episodes.append(traj)
        flat.extend(traj)
    return episodes, flat


# ----------------------------------------------------------------------
def evaluate_ctrr(
    agent,
    n_segments: int = 30,
    segment_len: int = 200,
    attractor_task_id: int = 0,
    seed: int = 1000,
    task_emb_noise: float = 0.0,
) -> List[Tuple[int, List[Dict]]]:
    """Force non-attractor tasks and roll out."""
    env = MultiTaskGrid(seed=seed, task_emb_noise=task_emb_noise)
    candidates = [t for t in range(3) if t != attractor_task_id]
    segments = []
    for i in range(n_segments):
        task_id = candidates[i % len(candidates)]
        obs = env.reset(task_id=task_id)
        traj = [obs]
        done = False
        steps = 0
        while not done and steps < segment_len:
            a = agent.select_action(obs)
            next_obs, r, done, _ = env.step(a)
            traj.append(next_obs)
            obs = next_obs
            steps += 1
        segments.append((task_id, traj))
    return segments


# ----------------------------------------------------------------------
def run_experiment(
    agents=("random", "qlearn", "greedy_q"),
    seeds=(0, 1, 2),
    n_episodes: int = 400,
    n_eval_episodes: int = 30,
    noise_levels=(0.0,),
    out_dir: str | None = None,
) -> List[Dict]:
    """
    Sweep noise_levels and produce one row per (agent, seed, noise).
    """
    if out_dir is None:
        out_dir = str(ROOT / "experiment" / "results")
    os.makedirs(out_dir, exist_ok=True)
    rows: List[Dict] = []
    for noise in noise_levels:
        for agent_name in agents:
            for seed in seeds:
                print(f"[run] agent={agent_name} seed={seed} noise={noise}", flush=True)
                agent = train_one(
                    agent_name,
                    n_episodes=n_episodes,
                    seed=seed,
                    task_emb_noise=noise,
                )
                episodes, flat = evaluate_episodes(
                    agent,
                    n_episodes=n_eval_episodes,
                    seed=seed + 10_000,
                    task_emb_noise=noise,
                )
                segs = evaluate_ctrr(
                    agent,
                    seed=seed + 20_000,
                    task_emb_noise=noise,
                )
                row = {
                    "agent": agent_name,
                    "seed": seed,
                    "noise": noise,
                    "trajectory_length": len(flat),
                    "unique_states": len({state_key(o) for o in flat}),
                    "TRR_within": trr_within_episode(flat),
                    "TRR_across_episodes": trr_across_episodes(episodes),
                    "CTRR": ctrr(segs),
                }
                rows.append(row)
                print(f"   -> {row}", flush=True)
    csv_path = os.path.join(out_dir, "trr_ctrr_table.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with open(os.path.join(out_dir, "trr_ctrr_table.json"), "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\n[done] wrote {csv_path}", flush=True)
    return rows


# ----------------------------------------------------------------------
if __name__ == "__main__":
    rows = run_experiment(noise_levels=(0.0, 0.3, 0.7))
    print("\n========= SUMMARY (mean ± std) =========", flush=True)
    by: Dict[Tuple[str, float], List[Dict]] = {}
    for r in rows:
        by.setdefault((r["agent"], r["noise"]), []).append(r)
    header = (
        f"{'agent':<12}{'noise':<8}{'TRR_within':<16}{'TRR_across_ep':<18}"
        f"{'CTRR':<14}{'unique_states':<14}"
    )
    print(header, flush=True)
    for (a, n), rs in by.items():
        trr_w = np.array([r["TRR_within"] for r in rs])
        trr_a = np.array([r["TRR_across_episodes"] for r in rs])
        ctrrs = np.array([r["CTRR"] for r in rs])
        us = np.array([r["unique_states"] for r in rs])
        print(
            f"{a:<12}{n:<8}"
            f"{trr_w.mean():.3f}±{trr_w.std():.3f}     "
            f"{trr_a.mean():.3f}±{trr_a.std():.3f}       "
            f"{ctrrs.mean():.3f}±{ctrrs.std():.3f}    "
            f"{us.mean():.1f}",
            flush=True,
        )