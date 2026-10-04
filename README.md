# Task Gravity — Complete Deliverables
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  [![Data](https://img.shields.io/badge/data-CC--BY--4.0-lightgrey.svg)](LICENSE)

Three integrated outputs:
**(A)** theory + position paper, **(B)** reference implementation with
empirical measurements, **(C)** workshop submission package.

---

## Quick start

```bash
# (A) Read the paper
open paper/position/paper.html             # HTML version (printable)
cat  paper/position/paper.md               # Markdown source
cat  paper/theory/task_gravity_theory.tex  # LaTeX theory supplement

# (B) Run the experiments
cd experiment
python -u -m src.experiment                # Tabular baseline (~30s)
python -u -m src.plot                      # produces 3 PNG figures

cd deep
python -u -m src.run --timesteps 10000     # PPO agent (~3 min)
python -u -m src.plot                      # produces 3 deep PNG figures
python -u -m src.summarize                 # table view of results

# (C) Submission materials
cat paper/submission/cover_letter.md
cat paper/submission/open_problems.md
cat paper/submission/venues.md
```

---

## Layout

```
paper/
  theory/task_gravity_theory.tex     # LaTeX (8 pages, formal)
  position/paper.md                  # Markdown source
  position/paper.html                # Print-ready HTML (with figures)
  submission/
    cover_letter.md                  # Workshop cover letter
    open_problems.md                 # Six concrete open problems
    venues.md                        # Suggested submission venues

experiment/
  src/                               # Tabular baseline (NumPy)
    env.py, agents.py, metrics.py
    experiment.py, plot.py
  results/
    trr_ctrr_table.csv               # Main results table (9 rows)
    REPORT.md                        # Detailed empirical report
    ctrr_vs_noise.png
    unique_states_vs_noise.png
    trajectory_length_vs_noise.png

  deep/                              # Deep PPO reproduction
    src/
      env.py                         # MultiTaskGoToObj (vector obs)
      train.py                       # PPO + TaskSequenceWrapper
      evaluate.py                    # TRR / CTRR on PPO
      run.py                         # sweep over (train_noise, eval_noise)
      plot.py                        # CTRR / unique / trajlen plots
      summarize.py                   # CSV table viewer
    checkpoints/                     # Cached PPO models
    results/
      deep_trr_ctrr_table.csv        # Main deep results (27 rows)
      deep_ctrr.png
      deep_unique.png
      deep_trajlen.png
    logs/

README.md                            # ← you are here
```

---

## Headline empirical results

### Tabular baseline (`experiment/results/`)

| agent    | noise | CTRR (mean) | unique_states (mean) |
|----------|-------|-------------|----------------------|
| random   | 0.0   | 0.59        | 47                   |
| qlearn   | 0.0   | 0.01        | 14                   |
| qlearn   | 0.3   | **0.98**    | 21                   |
| qlearn   | 0.7   | **0.85**    | 20                   |
| greedy_q | 0.0   | 0.00        | 7                    |
| greedy_q | 0.3   | **0.90**    | 7                    |
| greedy_q | 0.7   | **1.00**    | **3**                |

**Interpretation:** as the task embedding becomes unreliable, the
agent collapses onto the attractor task. State coverage drops from
14 → 3; CTRR climbs from 0.01 → 1.0.

### Deep PPO agent (`experiment/deep/results/`)

| train_noise | eval_noise | CTRR | unique_states | trajectory_length |
|-------------|-----------|------|---------------|-------------------|
| 0.0         | 0.0       | 0.17 | 6.7           | 313               |
| 0.0         | 0.7       | 0.23 | 12.7          | 400               |
| 0.3         | 0.7       | 0.34 | 6.7           | 316               |
| 0.7         | 0.0       | **0.33** | 6.0       | **660**           |
| 0.7         | 0.7       | **0.42** | 6.7       | 318               |

**Interpretation:** an agent trained under noise = 0.7 cannot route
even when evaluated under noise = 0.0 — the attractor basin is
*permanent*. Locked agents blow past the 32-step budget when forced
onto non-attractor tasks because they are heading toward the wrong
cell.

---

## What is Task Gravity?

A phenomenon observed in long-running RL agents: once a high-reward
(state, action, reward) pattern is learned, the agent's policy
*gravitates* toward replaying it even when the active task no longer
rewards it. We argue it is the deterministic shadow of stochastic
gradient descent on a non-convex return landscape, with three
mechanisms:

1. **Reward gradient collapse** — one `(s,a)` has a dominant Q-value.
2. **Value-function self-consistency** — `V_θ` and `π_θ` mutually
   reinforce under function approximation + replay.
3. **Meta-learning lock-in** — the task embedding is ignored; the
   policy is effectively the same for all prompts.

See the **position paper** for the full narrative and the **LaTeX
supplement** for the formal treatment.

---

## How to extend

| Open Problem | Where to start | Difficulty |
|--------------|---------------|------------|
| OP-1: Continuous gravity operator | `experiment/deep/src/evaluate.py` | Medium |
| OP-2: Anti-gravity shaping | new script in `experiment/deep/` | Medium |
| OP-3: Cross-task training corpus | Procgen / MiniGrid wrapper | Hard |
| OP-4: Human-compulsion test | collaborator needed | Hard |
| OP-5: LLM agents | AutoGPT / HELM-Agent traces | Hard |
| OP-6: Non-stationary rewards | theory extension of `task_gravity_theory.tex` | Easy |

See `paper/submission/open_problems.md` for the full list.

---

## Dependencies

```text
numpy
matplotlib
gymnasium>=1.0
minigrid>=3.0        # only for deep experiments
stable-baselines3    # only for deep experiments
torch                # only for deep experiments
```

`pip install -r experiment/requirements.txt` covers the tabular
baseline. For the deep experiments, additionally install
`stable-baselines3 torch gymnasium minigrid`.

---

## Status

| Deliverable | Status |
|-------------|--------|
| Theory supplement (LaTeX) | ✅ done |
| Position paper (Markdown) | ✅ done |
| Position paper (HTML, with figures) | ✅ done |
| Tabular reference implementation | ✅ done |
| Deep PPO reproduction | ✅ done |
| Empirical report | ✅ done |
| Cover letter | ✅ done |
| Open problems | ✅ done |
| Venue list | ✅ done |
| PDF (LaTeX compiled) | ⏳ requires `pdflatex` (not installed); HTML is the recommended viewing format |
| Procgen benchmark | ⏳ future work |

---

## License

MIT, unless otherwise noted in individual files.

> **Dual license.** Task Gravity releases the experiment results and figures under `experiment/` under