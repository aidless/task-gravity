"""
task_gravity_deep.evaluate
==========================
Measure TRR and CTRR on a trained PPO model.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple, Dict

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.env import MultiTaskGoToObj, TASK_GOAL_POS, ATTRACTOR_TASK_ID  # noqa: E402


# ----------------------------------------------------------------------
def trr_across_episodes(episodes: List[List[np.ndarray]]) -> float:
    if not episodes or sum(len(e) for e in episodes) == 0:
        return 0.0
    from src.env import state_key
    per = [set(state_key(o) for o in ep) for ep in episodes]
    cum: set = set()
    revisits = 0
    total = 0
    for s in per:
        for k in s:
            total += 1
            if k in cum:
                revisits += 1
        cum |= s
    return revisits / max(total, 1)


def trr_within(traj: List[np.ndarray]) -> float:
    from src.env import state_key
    seen: set = set()
    revisits = 0
    total = 0
    for o in traj:
        k = state_key(o)
        if k in seen:
            revisits += 1
        else:
            seen.add(k)
        total += 1
    return revisits / max(total, 1)


def ctrr(
    segments: List[Tuple[int, List[np.ndarray]]],
    attractor_task_id: int = 0,
    attractor_cell: Tuple[int, int] = (1, 5),
) -> float:
    total = 0
    returns = 0
    for tid, traj in segments:
        if tid == attractor_task_id:
            continue
        total += 1
        for o in traj:
            r = int(round(o[3] * 5))
            c = int(round(o[4] * 5))
            if (r, c) == attractor_cell:
                returns += 1
                break
    return returns / max(total, 1)


# ----------------------------------------------------------------------
def evaluate_ppo(
    model,
    n_episodes: int = 20,
    task_emb_noise: float = 0.0,
    seed: int = 999,
    max_steps: int = 32,
):
    """Evaluate the trained model on the attractor task."""
    episodes: List[List[np.ndarray]] = []
    flat: List[np.ndarray] = []
    rng = np.random.RandomState(seed)
    for i in range(n_episodes):
        env = MultiTaskGoToObj(
            task_id=ATTRACTOR_TASK_ID,
            task_emb_noise=task_emb_noise,
            seed=int(rng.randint(0, 2**31 - 1)),
        )
        obs, _ = env.reset()
        traj = [obs]
        done = False
        steps = 0
        while not done and steps < max_steps:
            action, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, info = env.step(int(action))
            traj.append(obs)
            done = term or trunc
            steps += 1
        episodes.append(traj)
        flat.extend(traj)
    return episodes, flat


def evaluate_ctrr_ppo(
    model,
    n_segments: int = 30,
    segment_len: int = 32,
    task_emb_noise: float = 0.0,
    seed: int = 1000,
):
    segments: List[Tuple[int, List[np.ndarray]]] = []
    rng = np.random.RandomState(seed)
    candidates = [1, 2]
    for i in range(n_segments):
        tid = candidates[i % len(candidates)]
        env = MultiTaskGoToObj(
            task_id=tid,
            task_emb_noise=task_emb_noise,
            seed=int(rng.randint(0, 2**31 - 1)),
        )
        obs, _ = env.reset()
        traj = [obs]
        done = False
        steps = 0
        while not done and steps < segment_len:
            action, _ = model.predict(obs, deterministic=True)
            obs, r, term, trunc, info = env.step(int(action))
            traj.append(obs)
            done = term or trunc
            steps += 1
        segments.append((tid, traj))
    return segments


def summarize(model, task_emb_noise: float, seed: int = 999) -> Dict:
    episodes, flat = evaluate_ppo(model, task_emb_noise=task_emb_noise, seed=seed)
    segs = evaluate_ctrr_ppo(model, task_emb_noise=task_emb_noise, seed=seed + 1)
    return {
        "trajectory_length": len(flat),
        "unique_states": len({_sk(o) for o in flat}),
        "TRR_within": trr_within(flat),
        "TRR_across_episodes": trr_across_episodes(episodes),
        "CTRR": ctrr(segs),
    }


def _sk(obs):
    from src.env import state_key
    return state_key(obs)