"""
task_gravity.env
================
Minimal multi-task grid-world for measuring Task Gravity.

Why this environment?
---------------------
We need a controllable setting where:
  * there are at least 3 distinct tasks,
  * one task (the "gravitational attractor") is significantly
    easier / higher-reward than the others,
  * we can switch tasks mid-episode to measure CTRR.

This env is a 7x7 grid with three goal cells. The agent's policy
must learn to navigate to the active goal. The agent has no
built-in task prior: it observes a one-hot task embedding, which
is what allows us to study "meta-learning lock-in" (mechanism 3
in the theory paper).
"""

from __future__ import annotations

import numpy as np
from typing import Tuple, Dict, Any

# Action codes
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
ACTIONS = (UP, RIGHT, DOWN, LEFT)
ACTION_DELTAS = {UP: (-1, 0), RIGHT: (0, 1), DOWN: (1, 0), LEFT: (0, -1)}


class MultiTaskGrid:
    """
    7x7 grid with three goals: easy (T0), medium (T1), hard (T2).
    The 'active goal' is chosen by setting `task_id` in `reset`.

    Observation: dict with
        'pos'      : (row, col) int
        'task_emb' : (3,) one-hot
    """

    GRID_SIZE = 7
    GOALS = {0: (1, 5), 1: (5, 1), 2: (5, 5)}      # T0 is the easy "attractor"
    REWARDS = {0: 1.0, 1: 0.6, 2: 0.3}             # T0 has the highest reward
    WALLS = {(3, 3), (3, 4)}                       # central wall

    def __init__(
        self,
        max_steps: int = 200,
        seed: int = 0,
        task_emb_noise: float = 0.0,
    ):
        """
        Args:
            task_emb_noise: in [0,1]. Probability that the one-hot task
                embedding is replaced by a *uniform* embedding. This
                simulates "the agent cannot reliably tell which task
                it is on", which is the regime where meta-learning
                lock-in becomes probable.
        """
        self.max_steps = max_steps
        self.rng = np.random.RandomState(seed)
        self.pos = (0, 0)
        self.task_id = 0
        self.steps = 0
        self.task_emb_noise = task_emb_noise

    # ------------------------------------------------------------------
    def reset(self, task_id: int | None = None) -> Dict[str, np.ndarray]:
        if task_id is None:
            task_id = self.rng.randint(0, 3)
        self.task_id = task_id
        self.pos = (0, 0)
        self.steps = 0
        return self._obs()

    def _obs(self) -> Dict[str, np.ndarray]:
        emb = np.zeros(3, dtype=np.float32)
        if self.rng.rand() < self.task_emb_noise:
            emb[:] = 1.0 / 3.0  # uniform = "I don't know what task I'm on"
        else:
            emb[self.task_id] = 1.0
        return {"pos": np.array(self.pos, dtype=np.int64), "task_emb": emb}

    # ------------------------------------------------------------------
    def step(self, action: int) -> Tuple[Dict[str, np.ndarray], float, bool, Dict[str, Any]]:
        dr, dc = ACTION_DELTAS[int(action)]
        r, c = self.pos
        nr = max(0, min(self.GRID_SIZE - 1, r + dr))
        nc = max(0, min(self.GRID_SIZE - 1, c + dc))
        # wall collision
        if (nr, nc) in self.WALLS:
            nr, nc = r, c
        self.pos = (nr, nc)
        self.steps += 1

        done = False
        reward = -0.01  # small step cost
        if self.pos == self.GOALS[self.task_id]:
            reward = self.REWARDS[self.task_id]
            done = True
        if self.steps >= self.max_steps:
            done = True
        return self._obs(), float(reward), bool(done), {"task_id": self.task_id}

    # ------------------------------------------------------------------
    def render_ascii(self) -> str:
        grid = [["." for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        for (r, c) in self.WALLS:
            grid[r][c] = "#"
        for tid, (r, c) in self.GOALS.items():
            grid[r][c] = "012"[tid]
        r, c = self.pos
        grid[r][c] = "A"
        return "\n".join(" ".join(row) for row in grid)


# ----------------------------------------------------------------------
def state_key(obs: Dict[str, np.ndarray]) -> Tuple[int, ...]:
    """Hashable state representation for TRR."""
    return (int(obs["pos"][0]), int(obs["pos"][1]), int(np.argmax(obs["task_emb"])))