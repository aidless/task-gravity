"""Headline numbers in the docs must match committed JSON/CSV.

The check is independent of plot.py: it recomputes means and population
standard deviations from the JSON. PNG byte identity is not claimed.
"""
from __future__ import annotations

import csv
import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TAB_JSON = ROOT / "experiment" / "results" / "trr_ctrr_table.json"
TAB_CSV = ROOT / "experiment" / "results" / "trr_ctrr_table.csv"
DEEP_JSON = ROOT / "experiment" / "deep" / "results" / "deep_trr_ctrr_table.json"
DEEP_CSV = ROOT / "experiment" / "deep" / "results" / "deep_trr_ctrr_table.csv"
PARTIAL_DEEP = (
    ROOT / "experiment" / "experiment" / "deep" / "results" / "deep_trr_ctrr_table.json"
)
# Locked so a noisy partial run cannot be reformatted or deleted quietly.
PARTIAL_DEEP_SHA256 = (
    "68d0ebad4ec8e14b1f1685538653cf341be3a3c6d58f0d7145550d47357ef75d"
)

TAB_HEADER = ["agent", "noise", "CTRR", "unique_states", "trajectory_length"]
DEEP_HEADER = [
    "train_noise",
    "eval_noise",
    "CTRR",
    "unique_states",
    "trajectory_length",
]
METRICS = ("CTRR", "unique_states", "trajectory_length")
TAB_DOCS = (
    ROOT / "README.md",
    ROOT / "experiment" / "results" / "REPORT.md",
    ROOT / "paper" / "submission" / "supplementary" / "README.md",
    ROOT
    / "paper"
    / "submission"
    / "supplementary"
    / "experiment"
    / "tabular"
    / "results"
    / "REPORT.md",
)
DEEP_DOCS = (
    ROOT / "README.md",
    ROOT / "paper" / "submission" / "supplementary" / "README.md",
)
PAPER_DOCS = (
    ROOT / "paper" / "position" / "paper.md",
    ROOT / "paper" / "position" / "paper.html",
    ROOT / "paper" / "submission" / "supplementary" / "paper" / "position" / "paper.md",
    ROOT / "paper" / "submission" / "supplementary" / "paper" / "position" / "paper.html",
)


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _rows_match(json_rows, csv_rows) -> None:
    assert len(json_rows) == len(csv_rows)
    for a, b in zip(json_rows, csv_rows):
        for key, value in a.items():
            if isinstance(value, str):
                assert b[key] == value
            elif isinstance(value, int) and key in ("seed", "unique_states", "trajectory_length"):
                assert int(float(b[key])) == value
            else:
                assert abs(float(b[key]) - float(value)) < 1e-12


def _split_row(line: str):
    if not line.strip().startswith("|"):
        return []
    return [part.replace("*", "").strip() for part in line.strip().strip("|").split("|")]


def _tables(text: str, header: list[str]):
    lines = text.splitlines()
    found = []
    i = 0
    while i < len(lines):
        cells = _split_row(lines[i])
        if cells == header:
            i += 1
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = _split_row(lines[i])
                i += 1
                if not row or set(row[0]) <= set("-: "):
                    continue
                rows.append(row)
            found.append(rows)
        else:
            i += 1
    return found


def _mean(rows, key):
    return statistics.fmean(float(r[key]) for r in rows)


def _pstdev(rows, key):
    return statistics.pstdev(float(r[key]) for r in rows)


def _grouped(rows, key_fields):
    buckets = defaultdict(list)
    for row in rows:
        buckets[tuple(row[k] for k in key_fields)].append(row)
    return buckets


def _check_tabular(rows, tab):
    buckets = _grouped(tab, ("agent", "noise"))
    assert len(rows) == len(buckets)
    seen = set()
    for row in rows:
        assert len(row) == len(TAB_HEADER)
        agent, noise_s, ctrr_s, uniq_s, traj_s = row
        key = (agent, float(noise_s))
        assert key in buckets, key
        assert key not in seen
        seen.add(key)
        group = buckets[key]
        assert abs(float(ctrr_s) - round(_mean(group, "CTRR"), 2)) < 1e-9
        assert abs(float(uniq_s) - round(_mean(group, "unique_states"), 1)) < 1e-9
        assert int(float(traj_s)) == int(round(_mean(group, "trajectory_length")))


def _check_deep(rows, deep):
    buckets = _grouped(deep, ("train_noise", "eval_noise"))
    assert len(rows) == len(buckets)
    seen = set()
    for row in rows:
        assert len(row) == len(DEEP_HEADER)
        tn_s, en_s, ctrr_s, uniq_s, traj_s = row
        key = (float(tn_s), float(en_s))
        assert key in buckets, key
        assert key not in seen
        seen.add(key)
        group = buckets[key]
        assert abs(float(ctrr_s) - round(_mean(group, "CTRR"), 2)) < 1e-9
        assert abs(float(uniq_s) - round(_mean(group, "unique_states"), 1)) < 1e-9
        assert int(float(traj_s)) == int(round(_mean(group, "trajectory_length")))


def _series_points(rows, key_fields):
    points = []
    buckets = _grouped(rows, key_fields)
    for metric in METRICS:
        for key, group in buckets.items():
            point = {
                "metric": metric,
                "mean": _mean(group, metric),
                "pstdev": _pstdev(group, metric),
                "n": len(group),
            }
            for field, value in zip(key_fields, key):
                point[field] = value
            points.append(point)
    return points


def _assert_series(path: Path, rows, key_fields):
    payload = _load_json(path)
    assert payload["std"] == "population"
    assert payload["png_byte_identity"] == "UNKNOWN"
    expected = _series_points(rows, key_fields)
    got = payload["points"]
    assert len(got) == len(expected)

    def sort_key(point):
        return tuple(point[k] for k in ("metric", *key_fields))

    for exp, act in zip(sorted(expected, key=sort_key), sorted(got, key=sort_key)):
        assert act["metric"] == exp["metric"]
        assert act["n"] == exp["n"]
        for field in key_fields:
            if isinstance(exp[field], float):
                assert abs(float(act[field]) - float(exp[field])) < 1e-12
            else:
                assert act[field] == exp[field]
        assert abs(float(act["mean"]) - exp["mean"]) < 1e-9
        assert abs(float(act["pstdev"]) - exp["pstdev"]) < 1e-9


def _seed_phrase(rows, label_fields, metric):
    ordered = sorted(rows, key=lambda r: r["seed"])
    prefix = " ".join(f"{name} {ordered[0][name]}" for name in label_fields)
    values = ", ".join(_fmt_seed_value(r[metric]) for r in ordered)
    return f"{prefix} {metric} seeds: {values}"


def _fmt_seed_value(value):
    if isinstance(value, float):
        text = format(value, ".16g")
        return text
    return str(value)


def test_csv_matches_json():
    tab = _load_json(TAB_JSON)
    with TAB_CSV.open(encoding="utf-8") as handle:
        _rows_match(tab, list(csv.DictReader(handle)))
    deep = _load_json(DEEP_JSON)
    with DEEP_CSV.open(encoding="utf-8") as handle:
        _rows_match(deep, list(csv.DictReader(handle)))


def test_supplementary_tables_match_canonical():
    pairs = [
        (
            TAB_JSON,
            ROOT
            / "paper"
            / "submission"
            / "supplementary"
            / "experiment"
            / "tabular"
            / "results"
            / "trr_ctrr_table.json",
        ),
        (
            DEEP_JSON,
            ROOT
            / "paper"
            / "submission"
            / "supplementary"
            / "experiment"
            / "deep"
            / "results"
            / "deep_trr_ctrr_table.json",
        ),
    ]
    for left, right in pairs:
        assert left.read_bytes() == right.read_bytes()


def test_headline_tables_match_committed_means():
    tab = _load_json(TAB_JSON)
    deep = _load_json(DEEP_JSON)
    for path in TAB_DOCS:
        tables = _tables(path.read_text(encoding="utf-8"), TAB_HEADER)
        assert tables, f"{path} has no tabular headline table"
        for table in tables:
            _check_tabular(table, tab)
    for path in DEEP_DOCS:
        tables = _tables(path.read_text(encoding="utf-8"), DEEP_HEADER)
        assert tables, f"{path} has no deep headline table"
        for table in tables:
            _check_deep(table, deep)


def test_figure_series_match_committed_tables():
    _assert_series(
        ROOT / "experiment" / "results" / "figure_series.json",
        _load_json(TAB_JSON),
        ("agent", "noise"),
    )
    _assert_series(
        ROOT / "experiment" / "deep" / "results" / "deep_figure_series.json",
        _load_json(DEEP_JSON),
        ("train_noise", "eval_noise"),
    )


def test_readme_problem_and_status():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    start = lines.index("## Problem") + 1
    body = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    nonempty = [line for line in body if line.strip()]
    assert len(nonempty) <= 3
    blob = " ".join(nonempty)
    assert "OBSERVED" in blob
    assert "does not claim" in blob
    assert "unsubmitted" in blob
    assert "UNKNOWN" in blob
    assert "STATUS: WORK-IN-PROGRESS" in text
    assert "No external validation" in text
    assert "No venue has accepted" in text
    assert "not in CI" in text
    assert "training budget is UNKNOWN" in text
    for banned in ("14 → 3", "is *permanent*", "basin is permanent", "workshop-ready"):
        assert banned not in text


def test_failure_modes_keep_seed_level_disagreements():
    text = (ROOT / "FAILURE_MODES.md").read_text(encoding="utf-8")
    tab = _load_json(TAB_JSON)
    deep = _load_json(DEEP_JSON)

    def group(rows, **pred):
        return [r for r in rows if all(r[k] == v for k, v in pred.items())]

    phrases = [
        _seed_phrase(
            group(tab, agent="greedy_q", noise=0.7),
            ("agent", "noise"),
            "unique_states",
        ),
        _seed_phrase(
            group(tab, agent="greedy_q", noise=0.7),
            ("agent", "noise"),
            "trajectory_length",
        ),
        _seed_phrase(
            group(tab, agent="qlearn", noise=0.7),
            ("agent", "noise"),
            "CTRR",
        ),
        _seed_phrase(
            group(deep, train_noise=0.7, eval_noise=0.0),
            ("train_noise", "eval_noise"),
            "CTRR",
        ),
        _seed_phrase(
            group(deep, train_noise=0.0, eval_noise=0.0),
            ("train_noise", "eval_noise"),
            "trajectory_length",
        ),
    ]
    for phrase in phrases:
        assert phrase in text, phrase

    digest = hashlib.sha256(PARTIAL_DEEP.read_bytes()).hexdigest()
    assert digest == PARTIAL_DEEP_SHA256
    partial = _load_json(PARTIAL_DEEP)
    assert len(partial) == 2
    canon = next(
        r
        for r in deep
        if r["train_noise"] == 0.0 and r["eval_noise"] == 0.0 and r["seed"] == 0
    )
    part = next(
        r
        for r in partial
        if r["train_noise"] == 0.0 and r["eval_noise"] == 0.0 and r["seed"] == 0
    )
    disclosure = (
        "partial (train_noise 0.0, eval_noise 0.0, seed 0) trajectory_length is "
        f"{part['trajectory_length']}; canonical is {canon['trajectory_length']}"
    )
    assert disclosure in text
    assert "not the headline table" in text
    assert "not re-rendered" in text
    assert "CTRR definition" in text
    plot = (ROOT / "experiment" / "deep" / "src" / "plot.py").read_text(encoding="utf-8")
    assert "Task Gravity locked" not in plot
    assert "Locked Agents" not in plot


def test_paper_does_not_claim_acceptance_or_unrun_benchmarks():
    required = (
        "Not accepted",
        "DOIs are not minted",
        "The code's CTRR is the fraction of non-attractor segments that visit the attractor goal cell, which is not the task-switch formula in §4.2.",
        "Procgen, Crafter, SAC, and RecurrentPPO were not run (UNKNOWN).",
    )
    for path in PAPER_DOCS:
        text = path.read_text(encoding="utf-8")
        for phrase in required:
            assert phrase in text, f"{path} missing {phrase!r}"
        assert "workshop-ready" not in text.lower()
        assert "Workshop-ready" not in text
        assert "cannot unlearn" not in text
        assert "DONE (deep/)" not in text


def test_cover_letter_and_citation_stay_unaccepted():
    letter = (ROOT / "paper" / "submission" / "cover_letter.md").read_text(encoding="utf-8")
    tab = _load_json(TAB_JSON)
    phrase = _seed_phrase(
        [r for r in tab if r["agent"] == "greedy_q" and r["noise"] == 0.7],
        ("agent", "noise"),
        "unique_states",
    )
    assert phrase in letter
    assert "training budget is UNKNOWN" in letter
    assert "Not accepted" in letter
    for banned in ("monotonically", "cannot route", "only **3**"):
        assert banned not in letter

    citation = (ROOT / "paper" / "submission" / "CITATION.cff").read_text(encoding="utf-8")
    zenodo = (ROOT / "paper" / "submission" / ".zenodo.json").read_text(encoding="utf-8")
    for text in (citation, zenodo):
        assert "< 5 minutes" not in text
        assert "__DOI_" not in text
        assert "not minted" in text


def test_pull_request_ci_does_not_install_the_ppo_stack():
    for name in ("checks.yml", "ci.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        assert "pull_request" in text
        assert "experiment/deep/requirements.txt" not in text
        assert "stable-baselines3" not in text
    ppo = (ROOT / ".github" / "workflows" / "ppo.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch" in ppo
    assert "pull_request" not in ppo
    assert "does not train" in ppo
