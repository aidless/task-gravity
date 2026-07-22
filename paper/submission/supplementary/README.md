# Task Gravity — Supplementary Material

This directory contains everything needed to reproduce the empirical
results in the Task Gravity position paper.

## Layout

```
supplementary/
├── README.md                       # this file
├── LICENSE                         # MIT
├── requirements.txt                # all dependencies
├── experiment/
│   ├── tabular/                    # NumPy-only baseline
│   │   ├── src/                    # env, agents, metrics, experiment, plot
│   │   ├── results/                # CSVs + PNGs
│   │   └── requirements.txt
│   └── deep/                       # Stable-Baselines3 PPO reproduction
│       ├── src/                    # env, train, evaluate, run, plot
│       └── results/                # CSVs + PNGs
└── paper/
    ├── position/paper.md           # position paper source
    └── theory/task_gravity_theory.tex   # LaTeX theory supplement
```

## Quick reproduction (≤ 5 minutes total)

```bash
cd supplementary

# Install
pip install -r requirements.txt

# 1. Tabular baseline (~30 s)
cd experiment/tabular
python -u -m src.experiment
python -u -m src.plot

# 2. Deep PPO reproduction (~3 min, CPU only)
cd ../deep
python -u -m src.run --timesteps 10000
python -u -m src.plot
python -u -m src.summarize
```

All CSV outputs land in `experiment/{tabular,deep}/results/`.
All figures are pre-included in `experiment/{tabular,deep}/results/*.png`.

## Headline results (already pre-computed)

### Tabular (in `experiment/tabular/results/trr_ctrr_table.csv`)

| agent    | noise | CTRR | unique_states |
|----------|-------|------|---------------|
| qlearn   | 0.0   | 0.01 | 14            |
| qlearn   | 0.3   | 0.98 | 21            |
| qlearn   | 0.7   | 0.85 | 20            |
| greedy_q | 0.0   | 0.00 | 7             |
| greedy_q | 0.7   | 1.00 | **3**         |

### Deep PPO (in `experiment/deep/results/deep_trr_ctrr_table.csv`)

| train_noise | eval_noise | CTRR | trajectory_length |
|-------------|-----------|------|-------------------|
| 0.0         | 0.0       | 0.17 | 313               |
| 0.7         | 0.0       | 0.33 | **660 (max)**     |
| 0.7         | 0.7       | 0.42 | 318               |

## Hardware

All experiments run on CPU. Total disk footprint: < 50 MB. Total
runtime on an Intel i5-class CPU: < 5 minutes.

## Reusing the metrics in your own work

To measure TRR / CTRR on a different agent:

```python
from experiment.tabular.src.metrics import trr_within_episode, ctrr
from experiment.deep.src.evaluate import summarize
```

The metrics are **trajectory-level, agent-agnostic, and require no
architectural changes**. They work on any RL agent that produces a
sequence of observations and a notion of "task id".

## Citing

If you use this material, please cite the position paper (see
`paper/position/paper.md` for the BibTeX entry).

## License

MIT. See `LICENSE`.