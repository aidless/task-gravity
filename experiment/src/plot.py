"""
task_gravity.plot
=================
Generate the headline figures from results/trr_ctrr_table.csv.

Outputs (to experiment/results/):
  * ctrr_vs_noise.png
  * unique_states_vs_noise.png
  * trajectory_length_vs_noise.png
"""

from __future__ import annotations

import csv
import os
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def load_rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def group_by_agent_noise(rows):
    by = defaultdict(list)
    for r in rows:
        key = (r["agent"], float(r["noise"]))
        by[key].append(r)
    return by


def mean_std(values):
    a = np.array(values, dtype=float)
    return a.mean(), a.std()


def plot_metric(rows, metric, ylabel, title, out_path, ylim=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    by = group_by_agent_noise(rows)
    noises = sorted({float(r["noise"]) for r in rows})
    agents = ["random", "qlearn", "greedy_q"]
    colors = {"random": "#888", "qlearn": "#3a7", "greedy_q": "#c33"}

    plt.figure(figsize=(7, 4.2))
    for a in agents:
        ys, es = [], []
        for n in noises:
            rows_n = by.get((a, n), [])
            if not rows_n:
                ys.append(np.nan); es.append(0); continue
            m, s = mean_std([float(r[metric]) for r in rows_n])
            ys.append(m); es.append(s)
        plt.errorbar(noises, ys, yerr=es, marker="o", label=a, color=colors[a], capsize=3)
    plt.xlabel("task embedding noise  (0 = clean, 1 = uniform)")
    plt.ylabel(ylabel)
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=140)
    plt.close()
    print(f"[plot] {out_path}")


def main():
    csv_path = ROOT / "experiment" / "results" / "trr_ctrr_table.csv"
    if not csv_path.exists():
        print(f"[plot] missing {csv_path}; run `python -m src.experiment` first.")
        return
    rows = load_rows(csv_path)
    out_dir = ROOT / "experiment" / "results"
    plot_metric(rows, "CTRR", "CTRR",
                "Cross-Task Return Rate vs Task-Embedding Noise",
                out_dir / "ctrr_vs_noise.png", ylim=(0, 1.05))
    plot_metric(rows, "unique_states", "# unique (row,col,task) states",
                "State Coverage vs Task-Embedding Noise",
                out_dir / "unique_states_vs_noise.png")
    plot_metric(rows, "trajectory_length", "trajectory length",
                "Trajectory Length vs Task-Embedding Noise",
                out_dir / "trajectory_length_vs_noise.png")


if __name__ == "__main__":
    main()