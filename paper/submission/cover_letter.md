# Cover Letter — Task Gravity

**Status:** Draft letter. Not accepted. Not submitted.
**Suggested routing (not a venue that has this paper):** a workshop track that takes position papers. See `venues.md`. Nothing in that list is an acceptance.

---

Dear Program Committee,

We are pleased to submit **"Task Gravity: Policy Attractors and Cross-Task Compulsivity in Reinforcement Learning Agents"** for consideration as a workshop position paper.

## Why this paper

A phenomenon routinely observed in long-running RL agents — *the agent cannot stop returning to a high-reward task, even when the operator no longer requests it* — has been described under many names (reward hacking, wireheading, behavioral sink, mode collapse) but has not been isolated, named, formalized, or measured. This paper does all four:

1. We **name** the phenomenon *Task Gravity*.
2. We **formalize** it as the basins of attraction of a Langevin SDE on the policy-parameter landscape, and define the *gravity operator* G(θ) as a measurable time-averaged reward-policy alignment.
3. We **measure** it with two lightweight trajectory-level metrics, **TRR** (Trajectory Revisitation Rate) and **CTRR** (Cross-Task Return Rate), which require no architectural changes to the agent.
4. We **bridge** it to a class of human compulsive behaviors (addiction, OCD, depressive rumination) — establishing that the critic network is functionally isomorphic to the basal-ganglia dopaminergic pathway.

## Headline empirical result

Two committed tables, not a single file:

- **Tabular** (`experiment/results/trr_ctrr_table.json`, seeds 0–2): mean CTRR for `qlearn` is 0.01 / 0.98 / 0.86 and for `greedy_q` is 0.00 / 0.90 / 1.00 at noise 0.0 / 0.3 / 0.7. Random stays at 0.59. agent greedy_q noise 0.7 unique_states seeds: 3, 9, 7. The mean is 6.3. Seed 0 is the short coverage row; seeds 1 and 2 are not.
- **PPO** (`experiment/deep/results/deep_trr_ctrr_table.json`): cell-mean CTRR at eval noise 0.7 is 0.23, 0.34, 0.42. train_noise 0.7 / eval_noise 0.0 CTRR seeds are 0.5, 0.5, and 0.0. The training budget is UNKNOWN. This run is not in CI.

The tabular sweep is rerun by `tests/test_offline.py`. The PPO table is not.

## What we are not claiming

This is a position paper. We are *not* claiming a closed-form solution to the problem, nor a unified theory of compulsive behavior. We are claiming a vocabulary, two metrics, and a falsifiable theoretical bridge. The empirical results are illustrative, not benchmark-leading; we invite the community to take them further.

## Why a workshop

The work is most useful as a community-shared vocabulary and a measurement instrument. Workshop feedback will inform the choice of (a) a Procgen / MiniGrid benchmark with deep agents, (b) a cross-task training corpus, and (c) a joint paper with a neuroscience collaborator on the human-compulsion mapping.

## Declarations

- **Code & data:** open source, MIT license, in the supplementary zip.
- **Conflict of interest:** none.
- **Funding:** self-funded.
- **Length:** 8 pages + 2 appendix pages.

We thank the committee for their consideration.

Sincerely,
The Authors