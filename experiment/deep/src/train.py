"""
task_gravity_deep.train
=======================
Train a PPO policy on the multi-task env with biased task sampling.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Callable

import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import DummyVecEnv, VecEnv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.env import MultiTaskGoToObj  # noqa: E402


# ----------------------------------------------------------------------
class TaskSequenceWrapper(gym.Wrapper):
    """
    Cyclic task-sampling wrapper. With probability `attractor_bias`
    the next episode uses task_id = 0 (attractor); otherwise a random
    non-attractor task.
    """

    def __init__(self, env_factory: Callable[[], gym.Env], attractor_bias: float = 0.7,
                 task_emb_noise: float = 0.0, seed: int = 0):
        super().__init__(env_factory())
        self._factory = env_factory
        self.attractor_bias = float(attractor_bias)
        self.task_emb_noise = float(task_emb_noise)
        self._rng = np.random.RandomState(seed)

    def reset(self, **kwargs):
        if self._rng.rand() < self.attractor_bias:
            tid = 0
        else:
            tid = int(self._rng.randint(1, 3))
        # rebuild underlying env with the chosen task id
        self.env = self._factory(task_id=tid, task_emb_noise=self.task_emb_noise)
        return self.env.reset(**kwargs)


class AttractorBiasCallback(BaseCallback):
    """Logs the per-episode task distribution for sanity checking."""

    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_tasks: list[int] = []

    def _on_step(self) -> bool:
        infos = self.model.ep_info_buffer
        for info in infos:
            if info and "task_id" in info:
                self.episode_tasks.append(int(info["task_id"]))
        return True


# ----------------------------------------------------------------------
def make_train_env(attractor_bias: float, task_emb_noise: float, seed: int) -> gym.Env:
    def _factory(task_id: int = 0, task_emb_noise: float = 0.0) -> gym.Env:
        return MultiTaskGoToObj(
            task_id=task_id,
            task_emb_noise=task_emb_noise,
            seed=seed,
        )

    return TaskSequenceWrapper(
        _factory,
        attractor_bias=attractor_bias,
        task_emb_noise=task_emb_noise,
        seed=seed,
    )


# ----------------------------------------------------------------------
def train_ppo(
    timesteps: int = 30_000,
    attractor_bias: float = 0.7,
    task_emb_noise: float = 0.0,
    seed: int = 0,
    save_path: str | None = None,
    verbose: int = 0,
) -> PPO:
    """Train a PPO policy with the given bias / noise settings."""
    env = DummyVecEnv([lambda: make_train_env(attractor_bias, task_emb_noise, seed)])
    model = PPO(
        policy="MlpPolicy",
        env=env,
        n_steps=256,
        batch_size=64,
        gae_lambda=0.95,
        gamma=0.99,
        learning_rate=3e-4,
        ent_coef=0.05,
        clip_range=0.2,
        verbose=verbose,
        seed=seed,
    )
    cb = AttractorBiasCallback()
    model.learn(total_timesteps=timesteps, callback=cb, progress_bar=False)
    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        model.save(save_path)
    return model