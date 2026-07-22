"""Plot deep-agent CTRR curves."""
import csv
import numpy as np
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT_OUT = "results"
rows = list(csv.DictReader(open(f"{ROOT_OUT}/deep_trr_ctrr_table.csv")))

# Pivot by (train_noise, eval_noise)
by_tn = defaultdict(lambda: defaultdict(list))
for r in rows:
    by_tn[float(r["train_noise"])][float(r["eval_noise"])].append(r)

# CTRR vs eval_noise, one curve per train_noise
plt.figure(figsize=(7, 4.2))
colors = {0.0: "#3a7", 0.3: "#da3", 0.7: "#c33"}
for tn in sorted(by_tn):
    ens = sorted(by_tn[tn])
    means = [np.mean([float(r["CTRR"]) for r in by_tn[tn][en]]) for en in ens]
    stds = [np.std([float(r["CTRR"]) for r in by_tn[tn][en]]) for en in ens]
    plt.errorbar(ens, means, yerr=stds, marker="o",
                 label=f"train_noise={tn}", color=colors[tn], capsize=3)
plt.xlabel("eval task-embedding noise")
plt.ylabel("CTRR (Cross-Task Return Rate)")
plt.title("PPO Agent: CTRR vs Embedding Noise\n(broken lines = trained on noise = Task Gravity locked)")
plt.ylim(0, 0.7)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(f"{ROOT_OUT}/deep_ctrr.png", dpi=140)
print("[plot] deep_ctrr.png")

# unique_states vs eval_noise
plt.figure(figsize=(7, 4.2))
for tn in sorted(by_tn):
    ens = sorted(by_tn[tn])
    means = [np.mean([float(r["unique_states"]) for r in by_tn[tn][en]]) for en in ens]
    stds = [np.std([float(r["unique_states"]) for r in by_tn[tn][en]]) for en in ens]
    plt.errorbar(ens, means, yerr=stds, marker="o",
                 label=f"train_noise={tn}", color=colors[tn], capsize=3)
plt.xlabel("eval task-embedding noise")
plt.ylabel("# unique (row, col, task) states visited")
plt.title("State Coverage under Different Training Noise")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(f"{ROOT_OUT}/deep_unique.png", dpi=140)
print("[plot] deep_unique.png")

# trajectory length vs eval_noise
plt.figure(figsize=(7, 4.2))
for tn in sorted(by_tn):
    ens = sorted(by_tn[tn])
    means = [np.mean([float(r["trajectory_length"]) for r in by_tn[tn][en]]) for en in ens]
    stds = [np.std([float(r["trajectory_length"]) for r in by_tn[tn][en]]) for en in ens]
    plt.errorbar(ens, means, yerr=stds, marker="o",
                 label=f"train_noise={tn}", color=colors[tn], capsize=3)
plt.xlabel("eval task-embedding noise")
plt.ylabel("trajectory length")
plt.title("Failure Mode: Locked Agents Blow Past Step Budget")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(f"{ROOT_OUT}/deep_trajlen.png", dpi=140)
print("[plot] deep_trajlen.png")