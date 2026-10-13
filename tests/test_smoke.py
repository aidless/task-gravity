"""Smoke tests for the tabular core (experiment/src). Offline, seeded."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "experiment"))

from src.agents import RandomPolicy, make_agent
from src.env import ACTIONS, MultiTaskGrid, state_key
from src.metrics import ctrr, summary, trr_within_episode


def run_episode(env, agent, max_steps=50):
    obs = env.reset(task_id=0)
    traj = [obs]
    total = 0.0
    for _ in range(max_steps):
        a = agent.select_action(obs)
        obs, r, done, _ = env.step(a)
        agent.update(obs, r, obs, done)
        traj.append(obs)
        total += r
        if done:
            break
    return traj, total


def test_env_reset_step():
    env = MultiTaskGrid()
    obs = env.reset(task_id=0)
    assert isinstance(state_key(obs), tuple)
    obs2, r, done, _ = env.step(0)
    assert isinstance(float(r), float) and isinstance(done, bool)


def test_random_episode_finishes():
    env = MultiTaskGrid()
    traj, total = run_episode(env, RandomPolicy(n_actions=len(ACTIONS), seed=0))
    assert len(traj) >= 2
    assert 0.0 <= trr_within_episode(traj) <= 1.0


def test_metrics_range():
    env = MultiTaskGrid()
    trajs = [run_episode(env, RandomPolicy(n_actions=len(ACTIONS), seed=s))[0]
             for s in range(3)]
    segments = [(1, t) for t in trajs]  # non-attractor task id
    c = ctrr(segments, attractor_task_id=0)
    assert 0.0 <= c <= 1.0
    d = summary(trajs[0], segments, episodes=trajs)
    assert set(d) == {"trajectory_length", "unique_states", "TRR_within",
                      "TRR_across_episodes", "CTRR"}


def test_make_agent_names():
    for name in ["random", "qlearn", "greedy_q"]:
        assert make_agent(name, seed=0) is not None
