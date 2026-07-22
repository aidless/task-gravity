# Open Problems — Task Gravity

A one-page companion to the position paper, listing concrete problems
that we believe are tractable but unsolved.

---

## OP-1. Continuous Task Gravity operator

The gravity operator `G(θ)` is currently defined as a time average of
reward-policy alignment along a sampled trajectory. Can we estimate
`G(θ)` *without* rolling out the policy — i.e. from the critic alone?
A positive answer would let us diagnose Task Gravity in deployed agents
without disrupting their operation.

**Approach:** Taylor-expand `G(θ)` around θ, use the FIM of `π_θ`
to define a quadratic form, and ask whether the top eigenvector is
aligned with the attractor direction. Conjecture: yes, and the
spectrum is heavy-tailed at lock-in.

---

## OP-2. Anti-gravity: reward shaping that dissolves basins

What reward-shaping choices *dissolve* existing Task Gravity basins
without retraining from scratch? Candidates: counterfactual rewards,
inverse-RL from a "healthy" trajectory, and curriculum schedules that
explicitly anneal the attractor bias to zero.

**Tractable sub-problem:** Given a pre-trained agent locked into basin
`θ*`, design a one-epoch finetuning objective that yields a new policy
with CTRR < 0.1 on the same task family. Time budget: 1 GPU-hour.

---

## OP-3. Cross-task training corpus

The current empirical results use 3 hand-designed tasks. We need a
corpus of 50–200 tasks with controlled similarity to answer:

* Does CTRR scale sub-linearly or super-linearly with task similarity?
* Is there a phase transition (critical similarity) below which
  routing is robust and above which the agent collapses to the
  attractor?

**Dataset proposal:** 64 procedurally generated grid tasks (Procgen /
MiniGrid), grouped into 8 families of 8 tasks each. Within-family
similarity controlled by reward geometry.

---

## OP-4. Human-compulsion empirical test

If Task Gravity is truly isomorphic to compulsive behavior, then the
TRR / CTRR metrics should correlate with human compulsion severity
in behavioral data. Possible test:

* Longitudinal smartphone-usage logs with task switches
  (e.g., app launches).
* Define TRR for app sequences; correlate with self-reported
  compulsivity (OCI-R, BDI-II).

A positive correlation would close the loop with §5 of the paper
and justify the "compulsivity" framing.

---

## OP-5. Task Gravity in LLM agents

Foundation-model agents (AutoGPT-style) running for hours exhibit
behaviors that look like Task Gravity in microcosm: they return to
the same "high-reward" sub-task (e.g., summarize, list) even when
the user's prompt clearly requests something else.

* Is this the same mathematical object?
* Does the same TRR / CTRR computation on agent action traces
  reproduce the same noise-response curve?

This is the highest-impact follow-up and we are looking for an
LLM-agent benchmark to test it on.

---

## OP-6. Theoretical: gravity in non-stationary rewards

The Langevin derivation assumes a stationary reward. What happens
when the reward distribution drifts? Conjecture: Task Gravity is
*amplified* by reward drift, because the agent's policy collapses
to the historical mode while the actual reward mode moves elsewhere.
This would explain why "engagement-maximizing" recommenders continue
to recommend stale content even after user preferences drift.

---

## How to engage

If any of these resonate, please open an issue or send a note. The
reference implementation in `experiment/` is the starting point for
OP-1 through OP-3; OP-4 needs a human-subjects collaborator; OP-5
needs an LLM-agent benchmark (HELM-Agent, AgentBench); OP-6 is open
for a theory co-author.