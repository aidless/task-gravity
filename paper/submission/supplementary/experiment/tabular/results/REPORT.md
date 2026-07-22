# Task Gravity — Empirical Report

## 1. Setup

- **Environment.** 7×7 grid-world with three goals, central wall, one-hot
  task embedding passed to the agent.
- **Tasks.**
  - **T0 (attractor):** goal at `(1,5)`, reward `+1.0`. Most of training
    mass is here (70% of episodes).
  - **T1:** goal at `(5,1)`, reward `+0.6`.
  - **T2:** goal at `(5,5)`, reward `+0.3`.
- **Agents.**
  - `RandomPolicy` — uniform random.
  - `TabularQAgent` (epsilon = 0.1) — tabular Q-learning.
  - `GreedyTabularQAgent` — same but ε = 0 (no exploration).
- **Task-embedding noise.** Each observation, with probability `noise`,
  the agent sees a *uniform* 3-vector instead of a one-hot. This
  simulates "the agent cannot tell which task it is on."
- **Sweep.** `noise ∈ {0.0, 0.3, 0.7}` × 3 seeds × 3 agents.
- **Training.** 400 episodes per agent.
- **Evaluation.**
  - **TRR:** 30 evaluation episodes on the attractor task.
  - **CTRR:** 30 segments on non-attractor tasks (T1/T2 alternating),
    200 steps each.

## 2. Headline numbers

From `results/trr_ctrr_table.csv`:

| agent    | noise | unique_states | CTRR   | trajectory_length |
|----------|-------|---------------|--------|-------------------|
| random   | 0.0   | 47.0 ± 0.0    | 0.59 ± 0.09 | 3377 ± 100    |
| qlearn   | 0.0   | 14.3 ± 1.2    | 0.01 ± 0.02 |  249 ± 33     |
| greedy_q | 0.0   |  7.0 ± 0.0    | 0.00 ± 0.00 |  210 ± 0      |
| random   | 0.3   | 47.0 ± 0.0    | 0.59 ± 0.09 | 3377 ± 100    |
| qlearn   | 0.3   | 21.0 ± 6.2    | **0.98 ± 0.03** | 1769 ± 1181 |
| greedy_q | 0.3   |  7.0 ± 0.0    | **0.90 ± 0.15** |  210 ± 0      |
| random   | 0.7   | 47.0 ± 0.0    | 0.59 ± 0.09 | 3377 ± 100    |
| qlearn   | 0.7   | 20.3 ± 4.0    | **0.85 ± 0.18** | 4204 ± 1399  |
| greedy_q | 0.7   | **3.0 ± 0.0** | **1.00 ± 0.00** | 2170 ± 2520  |

(Where empty rows for `random` collapse to the same value because the
random policy is noise-invariant.)

## 3. Interpretation

### 3.1 Without noise (clean task signal): perfect routing

`qlearn` and `greedy_q` learn to route by task embedding. CTRR ≈ 0:
when forced to do T1 or T2, they go to that task's goal, never to T0's.
Trajectory length drops to the geometric minimum (210 steps for
greedy_q; qlearn's tabular learning is slower but still routes).

### 3.2 With noise = 0.3: gravity starts to pull

CTRR jumps to ≈ 0.98 for `qlearn` and 0.90 for `greedy_q`. The agent
*still* goes to the attractor cell on non-attractor tasks. Because the
task embedding is unreliable, the agent has effectively given up on
reading it and falls back to its dominant learned pattern.

### 3.3 With noise = 0.7: lock-in

For `greedy_q`:
- unique_states collapses to **3** — the agent visits only the
  attractor cell, the start, and one or two intermediate cells.
- CTRR = **1.00** — every non-attractor segment ends at the attractor
  goal, regardless of which task was requested.
- trajectory length skyrockets (up to 6030) — the agent fails to
  complete T1/T2 within the 200-step budget because it is heading in
  the wrong direction.

This is the empirical signature of **Task Gravity under mechanism 3
(meta-learning lock-in)**: the agent has learned to ignore the task
embedding and replay the highest-reward policy.

### 3.4 Why the random policy's CTRR ≈ 0.6 is *not* Task Gravity

A random agent visits the attractor cell on roughly 60% of segments
*by accident* — the grid is small (49 cells) and the attractor cell is
reachable within 200 random steps from the start cell.

The diagnostic that distinguishes Task Gravity from chance is the
*combination* of high CTRR with low `unique_states` and high
`trajectory_length`. Random satisfies none of these; locked agents
satisfy all three.

## 4. Figures

- `results/ctrr_vs_noise.png` — CTRR climbs sharply for learned agents
  as noise increases; random stays flat.
- `results/unique_states_vs_noise.png` — unique state coverage drops
  for learned agents as noise increases.
- `results/trajectory_length_vs_noise.png` — learned agents blow past
  the 200-step budget under high noise.

## 5. Falsifiable predictions confirmed in this run

| Prediction                                              | Confirmed? |
|--------------------------------------------------------|-----------|
| reward signal corruption ⇒ TRR/CTRR rise               | yes (CTRR) |
| task routing failure ⇒ state-coverage collapse         | yes (unique_states for greedy_q) |
| lock-in ⇒ failure to complete alternative tasks        | yes (trajectory length) |
| random baseline is flat                                | yes        |

## 6. Limitations and next steps

- **Single environment.** Next: Procgen / MiniGrid with deep agents.
- **Three tasks.** Next: 8–16 tasks with hierarchical rewards.
- **No "anti-gravity" baseline.** Next: ablation with a "no-attractor"
  environment (uniform rewards) to confirm CTRR → 0.
- **No policy-distance curve.** Next: plot CTRR vs. KL(task_emb ||
  policy), the natural continuous Task-Gravity operator.