"""
task_gravity.agents
===================
Lightweight RL agents for Task Gravity measurement.

We implement three agents to span the spectrum of expected Task Gravity:

  * RandomPolicy      -- baseline; should have TRR ~ 1/N
  * TabularQAgent     -- standard tabular Q-learning; TRR should rise with training
  * EpsilonGreedyTab  -- same but with explicit exploration ablation

These are intentionally minimal. The point is *not* to win at MiniGrid
but to produce clean TRR / CTRR measurements.
"""

from __future__ import annotations

import numpy as np
from collections import defaultdict
from typing import Dict, Tuple, Any

from .env import state_key, ACTIONS


# ----------------------------------------------------------------------
class RandomPolicy:
    name = "RandomPolicy"

    def __init__(self, n_actions: int = 4, seed: int = 0):
        self.n_actions = n_actions
        self.rng = np.random.RandomState(seed)

    def select_action(self, obs: Dict[str, np.ndarray]) -> int:
        return int(self.rng.randint(self.n_actions))

    def update(self, *args, **kwargs):  # noqa: D401
        return None


# ----------------------------------------------------------------------
class TabularQAgent:
    """Tabular Q-learning with task embedding in the state key."""

    name = "TabularQ"

    def __init__(
        self,
        n_actions: int = 4,
        lr: float = 0.3,
        gamma: float = 0.95,
        epsilon: float = 0.1,
        seed: int = 0,
    ):
        self.n_actions = n_actions
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = np.random.RandomState(seed)
        self.Q: Dict[Tuple[int, ...], np.ndarray] = defaultdict(
            lambda: np.zeros(n_actions, dtype=np.float32)
        )
        self._last = None  # (state_key, action)

    # ------------------------------------------------------------------
    def select_action(self, obs: Dict[str, np.ndarray]) -> int:
        s = state_key(obs)
        if self.rng.rand() < self.epsilon:
            a = int(self.rng.randint(self.n_actions))
        else:
            q = self.Q[s]
            a = int(np.argmax(q))
        self._last = (s, a)
        return a

    # ------------------------------------------------------------------
    def update(self, obs, reward: float, next_obs, done: bool) -> None:
        s, a = self._last
        s_next = state_key(next_obs)
        target = reward + (0.0 if done else self.gamma * float(np.max(self.Q[s_next])))
        self.Q[s][a] += self.lr * (target - self.Q[s][a])


# ----------------------------------------------------------------------
class GreedyTabularQAgent(TabularQAgent):
    """No exploration. Used to demonstrate the maximum Task Gravity effect."""

    name = "GreedyTabularQ"

    def __init__(self, **kwargs):
        kwargs["epsilon"] = 0.0
        super().__init__(**kwargs)


# ----------------------------------------------------------------------
def make_agent(name: str, seed: int = 0) -> Any:
    table = {
        "random": RandomPolicy,
        "qlearn": TabularQAgent,
        "greedy_q": GreedyTabularQAgent,
    }
    if name not in table:
        raise ValueError(f"Unknown agent: {name}")
    return table[name](seed=seed)