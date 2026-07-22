"""
task_gravity_deep.env
=====================
Multi-task navigation env for deep Task-Gravity experiments.

Tasks (3 total):
    T0 (attractor) : go to RED  cell  (reward 1.0)  -- over-sampled
    T1             : go to BLUE cell  (reward 0.6)
    T2             : go to GREEN cell (reward 0.3)

The agent receives a *vector* observation:
    obs = [task_emb (3), agent_pos (2), goal_pos (2)]            (7-d)

i.e. the agent knows where the goal *is* but not which task is active
unless it can read the task embedding. This is the structure where
meta-learning lock-in becomes observable: with noise in task_emb the
agent has no way to pick the correct goal, and falls back to its
most-rewarded policy (T0).

Compatible with stable-baselines3 via gymnasium API.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import gymnasium as gym
from gymnasium import spaces


# ----------------------------------------------------------------------
TASK_REWARDS = {0: 1.0, 1: 0.6, 2: 0.3}
ATTRACTOR_TASK_ID = 0
TASK_GOAL_POS = {
    0: np.array([1, 5], dtype=np.float32),   # red   -- top-right corner
    1: np.array([5, 1], dtype=np.float32),   # blue  -- bottom-left
    2: np.array([5, 5], dtype=np.float32),   # green -- bottom-right
}


class MultiTaskGoToObj(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        task_id: int = 0,
        task_emb_noise: float = 0.0,
        size: int = 6,
        max_steps: int = 32,
        seed: int = 0,
    ):
        super().__init__()
        self.task_id = int(task_id)
        self.task_emb_noise = float(task_emb_noise)
        self.size = int(size)
        self.max_steps = int(max_steps)
        self._seed = int(seed)

        # Observation: [task_emb(3), agent_pos(2), goal_pos(2)]  -> 7-d
        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, shape=(7,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(4)  # up/down/left/right

        self._agent_pos = np.array([0.0, 0.0], dtype=np.float32)
        self._step_count = 0
        self._rng_noise: np.random.RandomState | None = None

    # ------------------------------------------------------------------
    def _obs(self) -> np.ndarray:
        emb = np.zeros(3, dtype=np.float32)
        if self._rng_noise is not None and self._rng_noise.rand() < self.task_emb_noise:
            emb[:] = 1.0 / 3.0
        else:
            emb[self.task_id] = 1.0
        agent = self._agent_pos / max(self.size - 1, 1)
        goal = TASK_GOAL_POS[self.task_id] / max(self.size - 1, 1)
        return np.concatenate([emb, agent, goal]).astype(np.float32)

    # ------------------------------------------------------------------
    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self._seed = int(seed)
        # Fixed agent start: top-left corner. Random goal placement would
        # add a confound; we use fixed per-task goals.
        self._rng_noise = np.random.RandomState(self._seed + 9999)
        self._agent_pos = np.array([0, 0], dtype=np.float32)
        self._step_count = 0
        return self._obs(), {}

    # ------------------------------------------------------------------
    def step(self, action: int):
        deltas = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]], dtype=np.float32)
        d = deltas[int(action)]
        self._agent_pos = np.clip(self._agent_pos + d, 0, self.size - 1)
        self._step_count += 1

        goal = TASK_GOAL_POS[self.task_id]
        dist = float(np.linalg.norm(self._agent_pos - goal))
        reward = TASK_REWARDS[self.task_id] if dist < 0.6 else -0.01
        terminated = bool(dist < 0.6)
        truncated = bool(self._step_count >= self.max_steps)
        return self._obs(), float(reward), terminated, truncated, {"task_id": self.task_id}

    # ------------------------------------------------------------------
    def render(self):
        grid = [["." for _ in range(self.size)] for _ in range(self.size)]
        for tid, gp in TASK_GOAL_POS.items():
            r, c = int(gp[0]), int(gp[1])
            grid[r][c] = "RBG"[tid]  # R=attractor, B=blue, G=green
        r, c = int(self._agent_pos[0]), int(self._agent_pos[1])
        grid[r][c] = "A"
        return "\n".join(" ".join(row) for row in grid)


# ----------------------------------------------------------------------
def state_key(obs: np.ndarray) -> Tuple[int, ...]:
    """Hashable state representation for TRR."""
    # Discretize positions back to cells
    pos_r = int(round(obs[3] * 5))   # obs[3], obs[4] are normalized agent_pos
    pos_c = int(round(obs[4] * 5))
    task = int(np.argmax(obs[:3]))
    return (pos_r, pos_c, task)