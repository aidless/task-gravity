# Failure modes

These are properties of the committed measurements. They are not cleaned out of the tables. Headline means in `README.md` are rounded from `experiment/results/trr_ctrr_table.json` and `experiment/deep/results/deep_trr_ctrr_table.json`. The lines below are the per-seed record `tests/test_drift.py` checks.

## Seed fragility

Tabular `greedy_q` at noise 0.7 has CTRR 1.0 on every seed. Coverage and length do not. One seed collapses; two do not.

agent greedy_q noise 0.7 unique_states seeds: 3, 9, 7

agent greedy_q noise 0.7 trajectory_length seeds: 6030, 270, 210

The mean unique-state count is 6.3, not 3. The mean length is 2170 because seed 0 contributes 6030. Seeds 1 and 2 (lengths 270 and 210) are in the same committed file and stay in the claim. A sentence that says the agent "visits only 3 states" is the seed-0 row.

`qlearn` at noise 0.7 does not collapse coverage either (unique states 17, 18, 26; mean 20.3, up from 14.3 at noise 0.0). Its CTRR mean is 0.86 because one seed is 0.6:

agent qlearn noise 0.7 CTRR seeds: 0.9666666666666667, 0.6, 1

`greedy_q` at noise 0.3 is the cleaner tabular cell: unique states stay 7, 7, 7 while CTRR seeds are 0.7, 1.0, 1.0 (mean 0.90).

## CTRR definition

CTRR definition in code (`experiment/src/metrics.py`, and the PPO copy in `experiment/deep/src/evaluate.py`): a non-attractor segment counts as a return if the rollout ever enters the attractor goal cell. The tabular horizon is 200 steps on a 7×7 grid. The random policy's mean CTRR is already 0.59 at every noise level, so the metric has a high floor. A policy that wanders more will touch the cell more often. `qlearn` unique states rise with noise (14.3 → 21.0 → 20.3) while CTRR rises, which is compatible with extra wandering and not only with lock-in.

The position paper §4.2 writes a different formula (task-switch events where the old policy is replayed, over task switches). The code does not implement that formula. Reported numbers are the goal-cell fraction. Quoting §4.2 as if it were the measured quantity is definition gaming.

On the PPO env, `state_key` labels a noised uniform embedding as task 0 via `argmax`. Unique-state and TRR counts under noise therefore mix in a labeling artifact. CTRR itself uses agent position against cell (1, 5) and does not use that argmax. Separately, `_obs` concatenates the true goal coordinates, so embedding noise does not remove the goal from the observation. "The agent cannot tell which task it is on" is false for this env.

## Short PPO runs

The deep table is 27 rows, 3 seeds, a 6×6 grid, and a 32-step cap. The training budget is UNKNOWN: `experiment/deep/src/run.py` defaults to 30000 timesteps and an older README invoked `--timesteps 10000`, and neither value is stored in the JSON. The path is not in CI. `minigrid` is not imported. Procgen, Crafter, SAC, and RecurrentPPO were not run (UNKNOWN).

Cell-mean CTRR at eval noise 0.7 is 0.23, 0.34, 0.42 as train noise goes 0.0, 0.3, 0.7. That is not a license to say the curve is monotone in general, or that the basin is permanent. The clean-eval cell after noisy training is three seeds, one of which has CTRR 0:

train_noise 0.7 eval_noise 0.0 CTRR seeds: 0.5, 0.5, 0

`trajectory_length` is the attractor-task evaluation (`evaluate_ppo`: 20 episodes, cap 32). 660 = 20 × 33 observations, meaning every episode hit the cap. It is not "forced onto non-attractor tasks." The cap is also hit when training noise is 0:

train_noise 0.0 eval_noise 0.0 trajectory_length seeds: 140, 140, 660

Calling 660 a signature of lock-in drops seed 2 of the clean training cell.

## Partial deep artifact

`experiment/experiment/deep/results/deep_trr_ctrr_table.json` is a 2-row file. It is not the headline table. It disagrees with the canonical deep JSON on the overlapping row:

partial (train_noise 0.0, eval_noise 0.0, seed 0) trajectory_length is 660; canonical is 140

The partial file is kept. Do not overwrite it with the canonical table to make the tree look consistent. Its CTRR values on those two rows are 0.0.

## Figures

`experiment/results/figure_series.json` and `experiment/deep/results/deep_figure_series.json` are the means and population standard deviations of the committed tables (the error bars `plot.py` computes with `numpy.std`). PNG byte identity is UNKNOWN: the committed PNGs were not re-rendered in the honesty pass. Deep PNG title pixels may still say that agents are locked; the current `experiment/deep/src/plot.py` titles do not.
