# Cover Letter — Task Gravity

**Submission target:** Workshop on Aligned AI / ICML Workshop on Reinforcement Learning Theory / AGI Safety Workshop (please route to the most relevant track).

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

We provide a reference implementation (NumPy + Stable-Baselines3) and run two experiments:

- **Tabular baseline** (3 tasks, biased rewards): CTRR climbs from 0.01 to **1.0** as the task embedding becomes unreliable. The greedy agent visits only **3** distinct states instead of 7.
- **PPO deep agent** (vector obs, 3 tasks): CTRR monotonically increases with training-time noise; an agent trained under noise = 0.7 cannot route even when evaluated under noise = 0.0. Locked agents blow past the step budget when forced onto non-attractor tasks.

The empirical signature is reproducible in <30 s on a CPU laptop, and the code is provided as a single-file reference.

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