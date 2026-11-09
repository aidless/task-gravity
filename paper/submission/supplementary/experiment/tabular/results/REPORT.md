# Task Gravity — Empirical Report

Numbers below are means over seeds 0, 1, and 2 from `results/trr_ctrr_table.json`, rounded like the README (CTRR 2 decimals, unique states 1 decimal, length to an integer). Per-seed rows are in that JSON. This file does not drop the seeds that weaken a one-line story.

## 1. Setup

- **Environment.** 7×7 grid with three goals. The observation is position plus a one-hot task embedding. With probability `noise`, the embedding is replaced by a uniform 3-vector.
- **Tasks.** T0 goal `(1, 5)` reward `+1.0` (70% of training episodes). T1 goal `(5, 1)` reward `+0.6`. T2 goal `(5, 5)` reward `+0.3`.
- **Agents.** `random`, `qlearn` (ε = 0.1), `greedy_q` (ε = 0).
- **Sweep.** noise ∈ {0.0, 0.3, 0.7} × 3 seeds × 3 agents. 400 training episodes. CTRR: 30 non-attractor segments, up to 200 steps. The metric is "did the segment visit the T0 goal cell?", not the task-switch formula in the position paper.

## 2. Means

| agent | noise | CTRR | unique_states | trajectory_length |
| --- | --- | --- | --- | --- |
| random | 0.0 | 0.59 | 47.0 | 3377 |
| random | 0.3 | 0.59 | 47.0 | 3377 |
| random | 0.7 | 0.59 | 47.0 | 3377 |
| qlearn | 0.0 | 0.01 | 14.3 | 249 |
| qlearn | 0.3 | 0.98 | 21.0 | 1769 |
| qlearn | 0.7 | 0.86 | 20.3 | 4204 |
| greedy_q | 0.0 | 0.00 | 7.0 | 210 |
| greedy_q | 0.3 | 0.90 | 7.0 | 210 |
| greedy_q | 0.7 | 1.00 | 6.3 | 2170 |

Random is noise-invariant in this table, including its CTRR of 0.59. That floor is why CTRR by itself is not the claim.

## 3. What is stable, and what is one seed

Mean CTRR for `qlearn` and `greedy_q` is higher at noise 0.3 and 0.7 than at noise 0.0. `greedy_q` at noise 0.3 keeps unique states at 7 while CTRR seeds are 0.7, 1.0, and 1.0.

`greedy_q` at noise 0.7 is not a uniform collapse:

agent greedy_q noise 0.7 unique_states seeds: 3, 9, 7

agent greedy_q noise 0.7 trajectory_length seeds: 6030, 270, 210

Seed 0 visits 3 states and runs to length 6030. Seeds 1 and 2 stay near the short paths (9 and 7 states; lengths 270 and 210). CTRR is 1.0 on all three. The mean unique-state count is 6.3.

`qlearn` coverage moves the other way (14.3 at noise 0.0, 21.0 at 0.3, 20.3 at 0.7). Its noise-0.7 CTRR mean is 0.86 only because the seeds are mixed:

agent qlearn noise 0.7 CTRR seeds: 0.9666666666666667, 0.6, 1

The random policy's CTRR stays 0.59 with unique states 47. High CTRR plus high coverage is the accident the metric allows on a small grid. High CTRR plus flat coverage (`greedy_q`, noise 0.3) is the sharper tabular observation. High CTRR plus a coverage collapse is seed 0 at noise 0.7, not the mean.

## 4. Figures

`ctrr_vs_noise.png`, `unique_states_vs_noise.png`, and `trajectory_length_vs_noise.png` were not re-rendered here. The numbers they are supposed to show are `figure_series.json` (population std, matching `numpy.std`). PNG byte identity is UNKNOWN.

## 5. Predictions versus this run

| Prediction | In this JSON |
| --- | --- |
| Learned-agent mean CTRR rises with task-embedding noise | Yes for `qlearn` and `greedy_q` means. Random does not move. |
| State coverage collapses for every learned agent | No. `qlearn` coverage rises. `greedy_q` collapse to 3 states is seed 0 only. |
| Alternative tasks always exceed the step budget | No. Only `greedy_q` seed 0 at noise 0.7 has length 6030. |
| Random CTRR is flat across noise | Yes, and the level is 0.59, not near zero. |

## 6. Limits

One 7×7 grid, three tasks, three seeds, 400 episodes. No anti-gravity (uniform reward) control. The deep PPO table is a different env and is not a confirmation of this one; see `FAILURE_MODES.md`.
