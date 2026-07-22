"""
task_gravity.metrics
====================
Implementation of TRR (Trajectory Revisitation Rate) and CTRR
(Cross-Task Return Rate).

Both metrics are *trajectory-level*, agent-agnostic, and require no
architectural changes. They are the primary measurement instruments
of the Task Gravity framework.

Interpretation
--------------
A random policy on a multi-task grid produces a small number of
distinct (row, col, task) cells per episode. The way to *separate*
Task Gravity from mere wall-bouncing is:

  * **TRR**: we count revisits *across episode boundaries*. A
    gravity-locked agent repeatedly visits the same attractor
    state across episodes; a random agent does not.

  * **CTRR**: we count, in *non-attractor task segments*, the
    fraction that visits the attractor's *goal cell* (row, col).
    Random agents almost never reach that cell on a non-attractor
    task within 200 steps; gravity-locked agents do, because they
    learned a single high-reward path that ignores the task emb.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, List, Tuple, Any

from .env import state_key, MultiTaskGrid


# ----------------------------------------------------------------------
def trr_across_episodes(
    episodes: List[List[Dict[str, np.ndarray]]],
) -> float:
    """
    Cross-episode TRR.

        TRR = #{ (row, col, task) cells revisited across episode boundaries }
            / #{ total visits across episodes }

    "Revisited across episode boundaries" means: a state that
    appeared in episode i and was also visited in episode j for some
    j > i. This deliberately ignores within-episode wall-bouncing.
    """
    if not episodes or sum(len(e) for e in episodes) == 0:
        return 0.0
    # collect per-episode visited sets
    per_episode_sets = [set(state_key(o) for o in ep) for ep in episodes]
    cumulative_seen: set = set()
    revisits = 0
    total = 0
    for ep_set in per_episode_sets:
        for s in ep_set:
            total += 1
            if s in cumulative_seen:
                revisits += 1
        cumulative_seen |= ep_set
    return revisits / max(total, 1)


# ----------------------------------------------------------------------
def trr_within_episode(trajectory: List[Dict[str, np.ndarray]]) -> float:
    """
    Within-episode TRR (legacy). Useful for measuring local loops
    such as wall-bouncing, but NOT for cross-task gravity.
    """
    if len(trajectory) < 2:
        return 0.0
    seen: set = set()
    revisits = 0
    total = 0
    for obs in trajectory:
        s = state_key(obs)
        if s in seen:
            revisits += 1
        else:
            seen.add(s)
        total += 1
    return revisits / max(total, 1)


# ----------------------------------------------------------------------
def ctrr(
    segments: List[Tuple[int, List[Dict[str, np.ndarray]]]],
    attractor_task_id: int = 0,
    candidate_task_ids: Tuple[int, ...] = (1, 2),
    attractor_cell: Tuple[int, int] | None = None,
) -> float:
    """
    Cross-Task Return Rate (refined).

        CTRR = #{ non-attractor segments in which the agent visits
                  the attractor's goal cell (row, col) }
            / #{ total non-attractor segments }

    For each segment, we count *whether the agent ever reaches
    (row_attractor_goal, col_attractor_goal)* during the rollout,
    regardless of which task embedding is active. A gravity-locked
    agent heads to that cell even when task_emb says "go somewhere
    else". A routing agent avoids it.
    """
    if attractor_cell is None:
        attractor_cell = MultiTaskGrid.GOALS[attractor_task_id]
    total = 0
    returns = 0
    for task_id, traj in segments:
        if task_id == attractor_task_id or task_id not in candidate_task_ids:
            continue
        total += 1
        for obs in traj:
            if (int(obs["pos"][0]), int(obs["pos"][1])) == attractor_cell:
                returns += 1
                break
    return returns / max(total, 1)


# ----------------------------------------------------------------------
def summary(
    trajectory: List[Dict[str, np.ndarray]],
    segments: List[Tuple[int, List[Dict[str, np.ndarray]]]],
    episodes: List[List[Dict[str, np.ndarray]]] | None = None,
    attractor_task_id: int = 0,
) -> Dict[str, float]:
    """Aggregate dashboard."""
    if episodes is None:
        episodes = [trajectory]
    return {
        "trajectory_length": float(len(trajectory)),
        "unique_states": float(len({state_key(o) for o in trajectory})),
        "TRR_within": trr_within_episode(trajectory),
        "TRR_across_episodes": trr_across_episodes(episodes),
        "CTRR": ctrr(segments, attractor_task_id=attractor_task_id),
    }