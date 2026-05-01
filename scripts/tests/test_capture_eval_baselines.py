"""Tests for ``scripts/capture-eval-baselines.py`` (spec 061 step 8).

The capture script's heavy path spawns real LLM calls and is exercised manually
(see the script's docstring). These tests cover the load-bearing pure-python
contract:

* Calibrated-threshold math (``min - 0.1`` per spec 061 §4.2, clamped at 0).
* Latest-baseline file resolution (timestamp-sorted, ignores noise).
* ``load_calibrated_thresholds`` fallback semantics (no file / malformed file /
  partial keys).
* Snapshot dataclass round-trip through JSON.

The script is loaded via :mod:`importlib` because its filename contains a
hyphen and so cannot be imported with a normal ``import`` statement.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "capture-eval-baselines.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "capture_eval_baselines", SCRIPT_PATH
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["capture_eval_baselines"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def mod():
    return _load_module()


# ---------------------------------------------------------------------------
# compute_calibrated_thresholds
# ---------------------------------------------------------------------------


def test_calibrated_thresholds_compute_min_minus_0_1(mod) -> None:
    """For each metric, threshold == min(observed) - 0.1."""
    snapshots = [
        mod.Snapshot(
            question_slug="q1",
            mode="cooperative",
            agents=["a", "b"],
            scores={
                "review_independence": 0.85,
                "cross_review_adversarial": 0.72,
                "revision_responsiveness": 0.65,
                "dispute_specificity": 0.78,
                "synthesis_grounding": 0.91,
            },
        ),
        mod.Snapshot(
            question_slug="q2",
            mode="winner-take-all",
            agents=["a", "b"],
            scores={
                "review_independence": 0.90,  # higher; q1 is the min
                "cross_review_adversarial": 0.80,
                "revision_responsiveness": 0.70,
                "dispute_specificity": 0.82,
                "synthesis_grounding": 0.88,  # lower; q2 is the min here
            },
        ),
    ]
    out = mod.compute_calibrated_thresholds(snapshots)
    assert out["review_independence"] == pytest.approx(0.75)
    assert out["cross_review_adversarial"] == pytest.approx(0.62)
    assert out["revision_responsiveness"] == pytest.approx(0.55)
    assert out["dispute_specificity"] == pytest.approx(0.68)
    assert out["synthesis_grounding"] == pytest.approx(0.78)


def test_calibrated_thresholds_clamps_to_zero(mod) -> None:
    """If min - 0.1 < 0 the threshold is clamped to 0.0, never negative."""
    snapshots = [
        mod.Snapshot(
            question_slug="q1",
            mode="cooperative",
            agents=["a"],
            scores={
                "review_independence": 0.05,  # 0.05 - 0.1 = -0.05 -> 0.0
                "cross_review_adversarial": 0.0,  # 0.0 - 0.1 -> 0.0
                "revision_responsiveness": 0.5,
                "dispute_specificity": 0.5,
                "synthesis_grounding": 0.5,
            },
        )
    ]
    out = mod.compute_calibrated_thresholds(snapshots)
    assert out["review_independence"] == 0.0
    assert out["cross_review_adversarial"] == 0.0
    # Sanity: non-clamped values are unaffected.
    assert out["revision_responsiveness"] == pytest.approx(0.4)


def test_calibrated_thresholds_falls_back_when_metric_absent(mod) -> None:
    """A metric missing from every snapshot uses the spec default."""
    snapshots = [
        mod.Snapshot(
            question_slug="q1",
            mode="cooperative",
            agents=["a"],
            scores={"review_independence": 0.9},
        )
    ]
    out = mod.compute_calibrated_thresholds(snapshots)
    # review_independence: observed -> 0.9 - 0.1 = 0.8
    assert out["review_independence"] == pytest.approx(0.8)
    # Every other metric falls back to spec defaults.
    assert out["cross_review_adversarial"] == mod.SPEC_DEFAULT_THRESHOLDS[
        "cross_review_adversarial"
    ]
    assert out["synthesis_grounding"] == mod.SPEC_DEFAULT_THRESHOLDS[
        "synthesis_grounding"
    ]


def test_calibrated_thresholds_empty_snapshots_returns_spec_defaults(mod) -> None:
    """Zero snapshots -> every threshold equals the spec default."""
    out = mod.compute_calibrated_thresholds([])
    assert out == dict(mod.SPEC_DEFAULT_THRESHOLDS)


# ---------------------------------------------------------------------------
# find_latest_baseline / load_calibrated_thresholds
# ---------------------------------------------------------------------------


def test_find_latest_baseline_returns_none_when_dir_missing(mod, tmp_path) -> None:
    missing = tmp_path / "no-such-dir"
    assert mod.find_latest_baseline(missing) is None


def test_find_latest_baseline_returns_none_when_dir_empty(mod, tmp_path) -> None:
    (tmp_path / "evals").mkdir()
    assert mod.find_latest_baseline(tmp_path / "evals") is None


def test_find_latest_baseline_picks_lex_largest_filename(mod, tmp_path) -> None:
    """Lex sort of monotonic timestamps == chronological sort."""
    older = tmp_path / "20260101T000000.json"
    newer = tmp_path / "20260201T120000.json"
    noise = tmp_path / "README.md"
    standard = tmp_path / "standard-questions.json"  # not a snapshot file
    older.write_text("{}", encoding="utf-8")
    newer.write_text("{}", encoding="utf-8")
    noise.write_text("# notes", encoding="utf-8")
    standard.write_text("{}", encoding="utf-8")

    assert mod.find_latest_baseline(tmp_path) == newer


def test_load_calibrated_thresholds_falls_back_to_spec_defaults(mod, tmp_path) -> None:
    """No baseline file -> spec defaults verbatim."""
    out = mod.load_calibrated_thresholds(tmp_path)
    assert out == dict(mod.SPEC_DEFAULT_THRESHOLDS)


def test_load_calibrated_thresholds_reads_latest_file(mod, tmp_path) -> None:
    older_path = tmp_path / "20260101T000000.json"
    newer_path = tmp_path / "20260301T120000.json"
    older_path.write_text(
        json.dumps(
            {
                "calibrated_thresholds": {
                    "review_independence": 0.5,
                    "cross_review_adversarial": 0.5,
                    "revision_responsiveness": 0.5,
                    "dispute_specificity": 0.5,
                    "synthesis_grounding": 0.5,
                }
            }
        ),
        encoding="utf-8",
    )
    newer_path.write_text(
        json.dumps(
            {
                "calibrated_thresholds": {
                    "review_independence": 0.81,
                    "cross_review_adversarial": 0.62,
                    "revision_responsiveness": 0.55,
                    "dispute_specificity": 0.68,
                    "synthesis_grounding": 0.79,
                }
            }
        ),
        encoding="utf-8",
    )
    out = mod.load_calibrated_thresholds(tmp_path)
    assert out["review_independence"] == pytest.approx(0.81)
    assert out["synthesis_grounding"] == pytest.approx(0.79)


def test_load_calibrated_thresholds_handles_malformed_json(mod, tmp_path) -> None:
    """Malformed JSON falls through to spec defaults rather than raising."""
    (tmp_path / "20260301T120000.json").write_text("not json {", encoding="utf-8")
    out = mod.load_calibrated_thresholds(tmp_path)
    assert out == dict(mod.SPEC_DEFAULT_THRESHOLDS)


def test_load_calibrated_thresholds_partial_keys_fall_back_per_metric(
    mod, tmp_path
) -> None:
    """A baseline missing a metric uses the spec default for that metric only."""
    (tmp_path / "20260301T120000.json").write_text(
        json.dumps(
            {
                "calibrated_thresholds": {
                    "review_independence": 0.81,
                    # missing the other four
                }
            }
        ),
        encoding="utf-8",
    )
    out = mod.load_calibrated_thresholds(tmp_path)
    assert out["review_independence"] == pytest.approx(0.81)
    assert (
        out["synthesis_grounding"]
        == mod.SPEC_DEFAULT_THRESHOLDS["synthesis_grounding"]
    )


# ---------------------------------------------------------------------------
# Snapshot/BaselineFile round-trip
# ---------------------------------------------------------------------------


def test_snapshot_format_validates(mod) -> None:
    """Snapshot dataclass round-trips through ``json.dumps``."""
    snap = mod.Snapshot(
        question_slug="postgres-vs-mongodb",
        mode="cooperative",
        agents=["alice", "bob"],
        scores={
            "review_independence": 0.85,
            "cross_review_adversarial": 0.72,
            "revision_responsiveness": 0.65,
            "dispute_specificity": 0.78,
            "synthesis_grounding": 0.91,
        },
    )
    serialized = json.dumps(asdict(snap))
    parsed = json.loads(serialized)
    assert parsed["question_slug"] == "postgres-vs-mongodb"
    assert parsed["agents"] == ["alice", "bob"]
    assert parsed["scores"]["synthesis_grounding"] == 0.91


def test_baseline_file_to_json_shape(mod) -> None:
    """The top-level baseline file matches the documented JSON shape."""
    snapshots = [
        mod.Snapshot(
            question_slug="q1",
            mode="cooperative",
            agents=["a", "b"],
            scores={k: 0.8 for k in mod.METRIC_KEYS},
        )
    ]
    baseline = mod.BaselineFile(
        captured_at="2026-05-01T20:00:00Z",
        judge={"provider": "anthropic", "model": "claude-sonnet-4-20250514"},
        deliberation_provider="claude-code",
        snapshots=snapshots,
        calibrated_thresholds=mod.compute_calibrated_thresholds(snapshots),
    )
    payload = baseline.to_json()
    # Every key the docstring example mentions must be present.
    assert set(payload.keys()) == {
        "captured_at",
        "judge",
        "deliberation_provider",
        "snapshots",
        "calibrated_thresholds",
    }
    assert payload["snapshots"][0]["scores"]["synthesis_grounding"] == 0.8
    # Calibrated threshold = 0.8 - 0.1 (single snapshot, single value per key).
    assert payload["calibrated_thresholds"]["synthesis_grounding"] == pytest.approx(
        0.7
    )


# ---------------------------------------------------------------------------
# Standard-question loader + slug helper
# ---------------------------------------------------------------------------


def test_load_standard_questions_returns_five_questions(mod) -> None:
    """The shipped question bank holds the five spec-mandated questions."""
    repo_root = Path(__file__).resolve().parents[2]
    path = repo_root / "evals" / "baselines" / "standard-questions.json"
    questions = mod.load_standard_questions(path)
    assert len(questions) == 5
    slugs = {q["slug"] for q in questions}
    assert "postgres-vs-mongodb" in slugs
    assert "monorepo-vs-polyrepo" in slugs


def test_slugify_handles_punctuation_and_case(mod) -> None:
    assert mod._slugify("Postgres OR MongoDB?") == "postgres-or-mongodb"
    assert mod._slugify("Build vs Buy: auth??") == "build-vs-buy-auth"
    # Empty/symbol-only input falls back to the placeholder slug.
    assert mod._slugify("???") == "question"


# ---------------------------------------------------------------------------
# argparse smoke
# ---------------------------------------------------------------------------


def test_parse_args_defaults(mod) -> None:
    args = mod._parse_args([])
    assert args.questions is None
    assert args.modes is None
    assert args.agents == ["alice", "bob"]
    assert args.dry_run is False


def test_parse_args_overrides(mod, tmp_path) -> None:
    out = tmp_path / "snap.json"
    args = mod._parse_args(
        [
            "--questions",
            "Q1?",
            "Q2?",
            "--modes",
            "cooperative",
            "--output",
            str(out),
            "--dry-run",
        ]
    )
    assert args.questions == ["Q1?", "Q2?"]
    assert args.modes == ["cooperative"]
    assert args.output == out
    assert args.dry_run is True


def test_main_dry_run_writes_baseline_file(mod, tmp_path, monkeypatch) -> None:
    """``--dry-run`` produces a parseable baseline file with no snapshots."""
    out = tmp_path / "baseline.json"
    rc = mod.main(
        [
            "--dry-run",
            "--questions",
            "Should we use Postgres or MongoDB?",
            "--modes",
            "cooperative",
            "--output",
            str(out),
        ]
    )
    assert rc == 0
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["snapshots"] == []
    # Empty snapshots -> spec defaults flow through.
    assert (
        payload["calibrated_thresholds"]
        == dict(mod.SPEC_DEFAULT_THRESHOLDS)
    )
