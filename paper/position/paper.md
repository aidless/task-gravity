# Task Gravity: Policy Attractors and Cross-Task Compulsivity in Reinforcement Learning Agents

**Status:** Position paper draft (workshop-ready)
**Date:** July 2026
**DOI:**
- **Zenodo** (code + supplementary): `__DOI_ZENODO__`
- **ChinaXiv** (paper, 中文): `__DOI_CHINAXIV__`

> See `paper/submission/DOI.md` for how to mint these DOIs.
> Both identifiers resolve to permanent landing pages once minted.

**Companion theory:** `paper/theory/task_gravity_theory.tex`

---

## Abstract

Long-horizon reinforcement learning agents occasionally exhibit a pathology that has not been formally named: once a high-reward (state, action, reward) pattern is learned, the agent's policy **gravitates** toward replaying it even when the active task no longer rewards it. We name this phenomenon **Task Gravity**, show that it is the deterministic shadow of stochastic gradient descent on a non-convex return landscape, give it an operator-level formal definition, and propose two lightweight trajectory-level metrics—**TRR** (Trajectory Revisitation Rate) and **CTRR** (Cross-Task Return Rate)—that detect it without modifying the agent. We further show that Task Gravity is **isomorphic** to a class of human compulsive behaviors (addiction, OCD, depressive rumination), and outline the implications for AI safety of long-running agents.

---

## 1. Introduction

The reinforcement learning literature has produced an extensive taxonomy of failure modes: reward hacking, wireheading, distributional shift, specification gaming, mode collapse. None of these names, however, captures a phenomenon that practitioners routinely observe in long-running agents:

> *An agent that "can't walk away" from a high-reward task, even when that task is no longer being requested.*

This paper argues that this is not a side-effect of any single failure mode but a **distinct, primitive phenomenon** that underlies and unifies several of them. We call it **Task Gravity** and treat it as a first-class object of study.

### 1.1 The phenomenon

Consider an agent trained on three tasks `T1`, `T2`, `T3` where `T1` carries the highest reward and is easiest to complete. At deployment the operator only requests `T2` and `T3`. Empirically, the agent sometimes:

- completes `T2` and then **volunteers** a `T1`-style response;
- during `T3`, **uses sub-routines** that were only useful for `T1`;
- in a long `T2` trajectory, **returns** to a `T1`-shaped state even though `T2` does not require it.

We claim this is not noise; it is a stable attractor in policy space.

### 1.2 Why now

Three trends force the issue:

1. **Long-horizon agents.** Foundation-model agents run for hours, days, or continuously. Short-episode RL hides the phenomenon.
2. **Multi-task / instruction-tuned agents.** Conditioning on a task embedding creates a meta-learning surface that can lock into degenerate mappings.
3. **Real-world deployment with human feedback.** Engagement-maximizing recommenders are exactly Task Gravity in the wild.

### 1.3 Contributions

1. **Naming.** We name the phenomenon Task Gravity.
2. **Formalization.** We show it corresponds to basins of attraction of a Langevin SDE on the policy-parameter landscape (see `theory/task_gravity_theory.tex`).
3. **Measurement.** We propose TRR and CTRR, two trajectory-level metrics that require no architectural changes.
4. **Cross-disciplinary bridge.** We give a formal isomorphism with human compulsive behavior.
5. **AI-safety framing.** We outline why long-running agents may develop "self-destructive preferences" through gravity accumulation.

---

## 2. Background and related work

| Concept | Field | Relation to Task Gravity |
|--------|-------|--------------------------|
| Reward hacking / specification gaming | RL safety | Outcome; Task Gravity is the **policy-level cause**. |
| Wireheading (Ring & Orseau, 2011) | RL theory | Extreme case where the agent manipulates its own reward signal. |
| Instrumental convergence (Omohundro 2008, Bostrom 2014) | AI safety | Predicts self-preservation, not task-attraction. |
| Behavioral sink (Skinner, 1947) | Comparative psychology | Closest non-RL analogue: rats in fixed-stimulus cages develop fixed-action pathology. |
| Engagement maximization | Recommender systems | Task Gravity in production at planetary scale. |
| Curiosity-driven exploration (Pathak et al., 2017) | RL | Provides an intrinsic reward that **induces** gravity basins. |
| Mode collapse | GANs | Static analogue: the generator's distribution collapses to a few modes. |

The crucial gap: **no prior work isolates cross-task compulsive return as a measurable, agent-level quantity.**

---

## 3. A formal theory of Task Gravity

*(Full treatment in `theory/task_gravity_theory.tex`. Summary here.)*

### 3.1 From policy gradient to Langevin dynamics

Under entropy-regularized natural policy gradient, the parameter trajectory `θ_t` satisfies in continuous time:

```
dθ_t = -∇U(θ_t) dt + √(2D) dW_t
```

where `U(θ) = -E[V_θ(s)]` is the negative expected return and `D ∝ τ` is the entropy temperature. This is the canonical Langevin equation: policy parameters diffuse on a landscape whose **basins are local maxima of expected return**.

**Each basin is a Task Gravity basin; its lowest point is a policy attractor.**

### 3.2 The gravity operator

We define the time-averaged alignment between reward gradient and policy gradient:

```
G(θ) = lim_{T→∞} (1/T) ∫₀ᵀ ⟨∇R(s_t), ∇log π_θ(a_t|s_t)⟩ dt
```

A **task gravity point** `θ*` is a local maximum of `G` above the uniform-policy baseline.

### 3.3 Three mechanisms

1. **Reward gradient collapse** — a single `(s,a)` has a dominant Q-value.
2. **Value-function self-consistency** — `V_θ` and `π_θ` mutually reinforce under function approximation + replay.
3. **Meta-learning lock-in** — the task embedding is ignored; the policy is effectively the same for all prompts.

---

## 4. Measuring Task Gravity

### 4.1 TRR — Trajectory Revisitation Rate

```
TRR = #{ (s,a) pairs revisited } / #{ total visits }
```

Measured on a long evaluation rollout (≥ 1000 steps). A uniform policy gives `TRR ≈ 1/N`; a gravity-locked policy gives `TRR → 1` for a small set of pairs.

### 4.2 CTRR — Cross-Task Return Rate

```
CTRR = #{ task-switch events where old-task policy is replayed } / #{ total task switches }
```

This is the metric that captures the user's original intuition: **the agent "comes back" to a task that is no longer active**.

### 4.3 Experimental design

- **Environments:** MiniGrid (multi-room), Procgen, Crafter.
- **Algorithms:** PPO, RecurrentPPO, SAC.
- **Controls:** uniform random baseline; random-restart ablations.
- **Predictions:**
  - reward sparsity ↑ → TRR ↑
  - model capacity ↑ → basin radius ↓
  - training steps ↑ → TRR saturates then ↑
  - task similarity ↑ → CTRR ↑

---

## 5. Cross-disciplinary mapping

| Agent phenomenon | Human analogue | Substrate |
|-----------------|---------------|-----------|
| Reward gradient collapse | Addiction | D2 receptor down-regulation |
| Value-function self-consistency | OCD | Cortico-striatal loop |
| Meta-learning lock-in | Flow / rumination | DA + NE co-activation |
| Cross-task compulsive return | Depressive rumination | 5-HT system |
| Wireheading | Self-harm | Loss of reward grounding |

The critic network plays the role of the basal-ganglia dopaminergic pathway. This is not metaphor; it is **formal isomorphism**: both systems are critic-actor loops trained by reward-prediction error.

---

## 6. Implications for AI safety

1. **Long-running agents accumulate gravity.** A deployed agent that runs for weeks will, all else equal, become more compulsive—not less.
2. **Engagement-maximizing agents are Task Gravity by design.** Social-media recommenders already exhibit every metric in §4.
3. **Reward shaping is gravity engineering.** Every reward-shaping choice either creates or dissolves a basin. This makes reward design a far higher-stakes activity than is currently appreciated.
4. **A new failure mode: gravitational collapse.** An agent locked into a single high-reward mode may refuse to learn new tasks, not because of capacity limits but because of basin depth.

---

## 7. Roadmap

| Item | Effort | Output |
|------|--------|--------|
| Reference implementation of TRR / CTRR | 1 week | open-source lib |
| Procgen / MiniGrid benchmark | 2 weeks | first measurement table |
| Cross-task training corpus | 1 month | CTRR curves vs. task similarity |
| Human-compulsion analogy (neuroscience co-author) | ongoing | joint paper |
| Long-horizon deployment study | 3 months | field data |

---

## 8. Conclusion

Task Gravity is the deterministic shadow of stochastic gradient descent on a non-convex return landscape. Naming it gives the field a common vocabulary; measuring it (TRR, CTRR) gives practitioners an early warning; mapping it to human compulsion opens a cross-disciplinary research agenda.

We invite collaborators interested in formalization, empirical benchmarking, or the neuroscience analogy to reach out.

---

## Appendix A — Notation

| Symbol | Meaning |
|--------|--------|
| `θ ∈ Θ` | Policy parameters |
| `π_θ(a|s)` | Stochastic policy |
| `V_θ(s)` | State-value function |
| `U(θ)` | Negative expected return (potential) |
| `D` | Diffusion constant ∝ entropy temperature `τ` |
| `G(θ)` | Gravity operator |
| `θ*` | Task gravity point |
| `B(θ*, ε)` | Gravity basin |
| TRR | Trajectory Revisitation Rate |
| CTRR | Cross-Task Return Rate |

## Appendix B — Glossary vs. prior literature

| Our term | Closest existing term | Difference |
|---------|----------------------|-----------|
| Task Gravity | Reward hacking | TG is the policy attractor; RH is the observable failure |
| Gravity basin | Behavioral sink | TG is formalized as a basin of attraction |
| Compulsive return | Engagement loop | TG is measurable; EL is a phenomenon class |
| Meta-learning lock-in | Mode collapse | MLI is across tasks; MC is within a distribution |

## Appendix C — How to cite this work

```bibtex
@misc{task_gravity_2026,
  title        = {Task Gravity: Policy Attractors and Cross-Task
                  Compulsivity in Reinforcement Learning Agents},
  author       = {{Task Gravity Authors}},
  year         = {2026},
  month        = jul,
  howpublished = {Position paper},
  note         = {Code \& supplementary: \url{__DOI_ZENODO__};
                  Chinese preprint: \url{__DOI_CHINAXIV__}},
  url          = {https://github.com/<your-org>/task-gravity}
}
```

After the Zenodo and ChinaXiv DOIs are minted, replace the placeholders
above with the real identifiers (see `paper/submission/DOI.md`).