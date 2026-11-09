# Task Gravity — Supplementary Material

Unsubmitted draft package. Not accepted. Zenodo and ChinaXiv DOIs are not minted.

The tabular numbers below are means from `experiment/tabular/results/trr_ctrr_table.json`. The deep numbers are means from `experiment/deep/results/deep_trr_ctrr_table.json`. Rounding matches the repository README. Seed-level rows that pull against the mean are in those JSON files and in the repository `FAILURE_MODES.md` (not copied into this folder).

## Tabular offline path

NumPy only. This is the path CI runs from the repository root (`python -m pytest tests -q`). It does not install or train PPO.

The supported command is at the repository root, where CI runs it:

```bash
pip install -r requirements.txt
python -m pytest tests -q
```

From the repository `experiment/` directory (not this snapshot):

```bash
python -m src.experiment --out-dir /tmp/tg-tabular
```

`experiment/tabular/src/experiment.py` in this folder is a copy. Its default output path is `parents[2] / experiment / results`, which is not `experiment/tabular/results/` here. Prefer the repository-root command. Wall-clock on other machines is UNKNOWN.

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

agent greedy_q noise 0.7 unique_states seeds: 3, 9, 7

## Deep PPO (not in CI)

Custom gymnasium grid, not MiniGrid and not Procgen. The true goal coordinates are in the observation. The training budget is UNKNOWN. Running `python -m src.run` is not known to reproduce the committed JSON.

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

## License

MIT. See `LICENSE`.
