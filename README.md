# Task Gravity

[![CI](https://github.com/aidless/task-gravity/actions/workflows/checks.yml/badge.svg)](https://github.com/aidless/task-gravity/actions/workflows/checks.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  [![Data](https://img.shields.io/badge/data-CC--BY--4.0-lightgrey.svg)](LICENSE)

## Problem

Task Gravity claims that, on this 7×7 grid, task-embedding noise raises Cross-Task Return Rate for the learned policies (OBSERVED means in `experiment/results/trr_ctrr_table.json`: greedy_q CTRR 0.00, 0.90, 1.00 at noise 0.0, 0.3, 0.7).
It does not claim a venue acceptance, a minted DOI, a PyPI package, or an external replication; `paper/submission/` is an unsubmitted workshop draft, and the position paper's Langevin and human-compulsion arguments are not results of these runs.
CTRR alone is not that claim: random CTRR is already 0.59, greedy_q unique states at noise 0.7 are seeds 3, 9, 7 (mean 6.3), and the deep PPO table is a short custom-grid run whose training budget is UNKNOWN.

## Paths

### Tabular offline (this is what CI runs)

NumPy only. No torch, no GPU, no PPO. From a fresh clone:

```bash
pip install -r requirements.txt
python -m pytest tests -q
```

`tests/test_offline.py` reruns the full sweep (3 agents × seeds 0–2 × noise 0.0/0.3/0.7, 400 training episodes) into a temp directory and checks it against `experiment/results/trr_ctrr_table.json`. A non-destructive manual run:

```bash
cd experiment
python -m src.experiment --out-dir /tmp/tg-tabular
```

Defaults match the committed table. `--episodes 1 --ctrr-segments 2` is a smoke run, not a new result. Wall-clock on other machines is UNKNOWN. The sweep is the CI path and is sized to finish well inside a 15-minute fresh clone, including the NumPy install.

### Deep PPO (not in CI)

`experiment/deep/` is a custom 6×6 gymnasium grid (`MultiTaskGoToObj`). It is not MiniGrid and not Procgen: `minigrid` is listed in `experiment/deep/requirements.txt` and is not imported by `experiment/deep/src`. The true goal coordinates are part of the observation (`env.py`, `_obs`), so task-embedding noise does not hide the goal. The committed table's training budget is UNKNOWN (the CLI default is 30000 steps; an older README line said `--timesteps 10000`; the JSON does not record which one produced the file). Do not treat a new PPO run as a reproduction of that file.

`.github/workflows/ppo.yml` is `workflow_dispatch` only. It does not train. Pull-request CI does not install the deep stack.

## Numbers

Means over seeds 0, 1, and 2. CTRR is rounded to 2 decimals, `unique_states` to 1 decimal, `trajectory_length` to an integer. Population standard deviations and the per-seed rows live in the JSON. `tests/test_drift.py` fails if a headline table disagrees with those files. Figure PNGs are not byte-checked (`png_byte_identity` is UNKNOWN); `figure_series.json` and `deep_figure_series.json` are the plotted means.

### Tabular baseline

Source: `experiment/results/trr_ctrr_table.json` (same bytes as the CSV).

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

What this supports: for `greedy_q` and `qlearn`, mean CTRR is higher at noise 0.3 and 0.7 than at noise 0.0, and the random policy's CTRR does not move with noise. What it does not support: a uniform collapse of state coverage to 3 cells, or a uniform blow-up of trajectory length. See `FAILURE_MODES.md`.

### Deep PPO

Source: `experiment/deep/results/deep_trr_ctrr_table.json`. Training budget is UNKNOWN. These are cell means, not a monotone law. Per-seed values overlap; `FAILURE_MODES.md` lists them.

| train_noise | eval_noise | CTRR | unique_states | trajectory_length |
| --- | --- | --- | --- | --- |
| 0.0 | 0.0 | 0.17 | 6.7 | 313 |
| 0.0 | 0.3 | 0.14 | 12.7 | 239 |
| 0.0 | 0.7 | 0.23 | 12.7 | 400 |
| 0.3 | 0.0 | 0.17 | 6.3 | 487 |
| 0.3 | 0.3 | 0.22 | 6.7 | 327 |
| 0.3 | 0.7 | 0.34 | 6.7 | 316 |
| 0.7 | 0.0 | 0.33 | 6.0 | 660 |
| 0.7 | 0.3 | 0.27 | 6.7 | 345 |
| 0.7 | 0.7 | 0.42 | 6.7 | 318 |

`trajectory_length` 660 is the attractor-task evaluation hitting the step cap (20 episodes × 33 observations). It is not the non-attractor CTRR rollout. The same cap value appears for `train_noise` 0.0, seed 2, `eval_noise` 0.0.

A second committed file, `experiment/experiment/deep/results/deep_trr_ctrr_table.json`, has 2 rows and is not the headline table. It disagrees with the canonical file on the overlapping seed. It is kept.

## What the position paper adds

`paper/position/paper.md` is a draft argument: a name, a Langevin-style sketch, and a proposed link to compulsive behavior. The implemented CTRR (`experiment/src/metrics.py`) is the fraction of non-attractor segments that visit the attractor goal cell. That is not the task-switch formula written in §4.2 of the draft. Procgen, Crafter, SAC, and RecurrentPPO were not run (UNKNOWN).

## Status

STATUS: WORK-IN-PROGRESS — not A yet. The package is internally rerunnable on the tabular path. It is not externally validated.

Gaps:

- No external validation and no independent replication.
- No venue has accepted this draft. The workshop files are unsubmitted.
- Zenodo and ChinaXiv DOIs are not minted. There is no PyPI release.
- Seed-level coverage and length effects are fragile (`FAILURE_MODES.md`).
- The deep PPO path is not in CI. Its training budget is UNKNOWN. Goal coordinates are inside the observation.
- PNG byte identity against a fresh matplotlib render is UNKNOWN. Drift checks the numeric series, not the image bytes.
- The position-paper CTRR formula and the code disagree.

| Deliverable | Status |
| --- | --- |
| Theory supplement (LaTeX) | Draft text in the repo. Not peer-reviewed. |
| Position paper | Draft. Not accepted. |
| Tabular sweep | Committed JSON, regenerated by `tests/test_offline.py`. |
| Deep PPO table | Committed JSON only. Not in CI. Budget UNKNOWN. |
| Workshop package | Unsubmitted draft. |
| Procgen / Crafter / SAC / RecurrentPPO | Not run (UNKNOWN). |

## Layout

```
paper/position/paper.md          # draft
paper/theory/task_gravity_theory.tex
paper/submission/                # unsubmitted workshop package
experiment/src/                  # tabular NumPy sweep
experiment/results/              # committed tabular table, series, figures
experiment/deep/                 # PPO code and committed table (not CI)
experiment/experiment/deep/      # 2-row partial run; not the headline table
FAILURE_MODES.md
tests/test_drift.py              # docs vs JSON
tests/test_offline.py            # fresh tabular run vs JSON
```

## License

Code is MIT. Data, documentation, and figures under `experiment/` are CC-BY-4.0. See `LICENSE`.
