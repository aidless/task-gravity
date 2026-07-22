"""Print deep-agent summary from CSV."""
import csv
import numpy as np
from collections import defaultdict

rows = list(csv.DictReader(open('results/deep_trr_ctrr_table.csv')))
by = defaultdict(list)
for r in rows:
    by[(float(r['train_noise']), float(r['eval_noise']))].append(r)

print(f"{'train_n':<8}{'eval_n':<8}{'TRR_w':<10}{'TRR_x':<10}{'CTRR':<10}{'unique':<10}{'traj_len':<10}")
for (tn, en), rs in sorted(by.items()):
    trr_w = np.array([float(r['TRR_within']) for r in rs])
    trr_a = np.array([float(r['TRR_across_episodes']) for r in rs])
    ctrrs = np.array([float(r['CTRR']) for r in rs])
    us = np.array([float(r['unique_states']) for r in rs])
    tls = np.array([float(r['trajectory_length']) for r in rs])
    print(f"{tn:<8}{en:<8}{trr_w.mean():.3f}      {trr_a.mean():.3f}      {ctrrs.mean():.3f}      {us.mean():.1f}       {tls.mean():.0f}")