"""Tabular path: a fresh run must match the committed table, and a tiny CLI run must not need PPO."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiment"
COMMITTED = ROOT / "experiment" / "results" / "trr_ctrr_table.json"


def test_fresh_tabular_run_matches_committed_json(tmp_path):
    sys.path.insert(0, str(EXPERIMENT))
    from src.experiment import run_experiment

    rows = run_experiment(noise_levels=(0.0, 0.3, 0.7), out_dir=str(tmp_path))
    committed = json.loads(COMMITTED.read_text(encoding="utf-8"))
    assert rows == committed


def test_cli_short_run_writes_elsewhere_and_does_not_import_torch(tmp_path):
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.experiment",
            "--out-dir",
            str(tmp_path),
            "--episodes",
            "1",
            "--eval-episodes",
            "1",
            "--seeds",
            "0",
            "--agents",
            "random",
            "--noises",
            "0.0",
            "--ctrr-segments",
            "2",
            "--segment-len",
            "5",
        ],
        cwd=EXPERIMENT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    payload = json.loads((tmp_path / "trr_ctrr_table.json").read_text(encoding="utf-8"))
    assert len(payload) == 1
    assert 0.0 <= payload[0]["CTRR"] <= 1.0
    assert "torch" not in (proc.stdout + proc.stderr).lower()
