"""Numeric series behind the figures.

PNG byte identity across matplotlib versions is UNKNOWN. The drift test
compares these points to the committed JSON, using the population standard
deviation (the same default as numpy.std, which plot.py draws as error bars).
"""
from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
METRICS = ("CTRR", "unique_states", "trajectory_length")


def _points(rows, key_fields):
    buckets = defaultdict(list)
    for row in rows:
        buckets[tuple(row[field] for field in key_fields)].append(row)
    points = []
    for metric in METRICS:
        for key in sorted(buckets, key=lambda item: tuple(str(part) for part in item)):
            group = buckets[key]
            values = [float(row[metric]) for row in group]
            point = {
                "metric": metric,
                "mean": statistics.fmean(values),
                "pstdev": statistics.pstdev(values),
                "n": len(group),
            }
            for field, value in zip(key_fields, key):
                point[field] = value
            points.append(point)
    return points


def _dump(path: Path, source: str, points) -> None:
    payload = {
        "source": source,
        "std": "population",
        "png_byte_identity": "UNKNOWN",
        "points": points,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_all() -> None:
    tabular = json.loads(
        (ROOT / "experiment" / "results" / "trr_ctrr_table.json").read_text(encoding="utf-8")
    )
    deep = json.loads(
        (ROOT / "experiment" / "deep" / "results" / "deep_trr_ctrr_table.json").read_text(
            encoding="utf-8"
        )
    )
    _dump(
        ROOT / "experiment" / "results" / "figure_series.json",
        "experiment/results/trr_ctrr_table.json",
        _points(tabular, ("agent", "noise")),
    )
    _dump(
        ROOT / "experiment" / "deep" / "results" / "deep_figure_series.json",
        "experiment/deep/results/deep_trr_ctrr_table.json",
        _points(deep, ("train_noise", "eval_noise")),
    )


if __name__ == "__main__":
    write_all()
