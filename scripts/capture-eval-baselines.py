#!/usr/bin/env python3
"""Capture deepeval baseline snapshots for spec 061 step 8.

This script runs the deliberation pipeline once per ``(question, mode)`` pair,
scores every Phase artifact with the five GEval metrics defined in
``engine/tests/test_evals.py``, and writes the raw scores plus a calibrated
threshold table to ``evals/baselines/<timestamp>.json``.

The output JSON has this shape::

    {
      "captured_at": "2026-05-01T20:00:00Z",
      "judge": {"provider": "anthropic", "model": "claude-sonnet-4-20250514"},
      "deliberation_provider": "claude-code",
      "snapshots": [
        {
          "question_slug": "postgres-vs-mongodb",
          "mode": "cooperative",
          "agents": ["alice", "bob"],
          "scores": {
            "review_independence": 0.85,
            "cross_review_adversarial": 0.72,
            "revision_responsiveness": 0.65,
            "dispute_specificity": 0.78,
            "synthesis_grounding": 0.91
          }
        }
      ],
      "calibrated_thresholds": {
        "review_independence": 0.75,
        "cross_review_adversarial": 0.62,
        "revision_responsiveness": 0.55,
        "dispute_specificity": 0.68,
        "synthesis_grounding": 0.81
      }
    }

Calibration math
----------------

For each metric, ``calibrated_thresholds[metric]`` is computed as::

    max(0.0, min(score across snapshots) - 0.1)

That is: take the worst observed score for that metric across every captured
snapshot and subtract a 0.1 margin (clamped at zero). The 0.1 floor matches
spec 061 §4.2 ("set thresholds at ``baseline - 0.1`` margin"). Subtracting a
margin from the *minimum* — not the mean — guarantees that every single
captured deliberation would still pass the calibrated threshold, so the
recalibrated suite cannot regress on a known-good run.

If no snapshots exist for a metric (empty input), the calibrated threshold
falls back to the spec default (see :data:`SPEC_DEFAULT_THRESHOLDS`).

CLI
---

::

    uv run python scripts/capture-eval-baselines.py \
        --questions "Postgres or MongoDB?" "Build vs buy auth?" \
        --modes cooperative winner-take-all \
        --output evals/baselines/$(date +%Y%m%dT%H%M%S).json

If ``--questions`` is omitted, the standard five-question bank from
``evals/baselines/standard-questions.json`` is used. If ``--modes`` is
omitted, the four primary modes (``cooperative``, ``winner-take-all``,
``prisoners-dilemma``, ``red-blue``) are used.

The script does **not** run automatically in CI — it triggers real LLM calls
across ~20 deliberations with five judge calls each (~100+ paid LLM calls per
full matrix). Invoke it manually when you have provider credentials and a
budget for the run.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

# ---------------------------------------------------------------------------
# Public constants
# ---------------------------------------------------------------------------

# Names match the snapshot ``scores`` dict keys, which are the canonical
# identifiers for the five GEval metrics in ``engine/tests/test_evals.py``.
METRIC_KEYS: tuple[str, ...] = (
    "review_independence",
    "cross_review_adversarial",
    "revision_responsiveness",
    "dispute_specificity",
    "synthesis_grounding",
)

# Spec 061 §3.2.1 thresholds — the fallback used when no baseline file has
# been captured yet. Engine/tests/test_evals.py imports this dict via
# ``_load_calibrated_thresholds`` so the test suite stays runnable on a
# fresh checkout.
SPEC_DEFAULT_THRESHOLDS: Mapping[str, float] = {
    "review_independence": 0.7,
    "cross_review_adversarial": 0.7,
    "revision_responsiveness": 0.6,
    "dispute_specificity": 0.7,
    "synthesis_grounding": 0.8,
}

# Baseline-file naming format (matches the CLI ``--output`` example above).
# We sort baseline files lexically; the format below is monotonic by capture
# time so lex sort matches chronological sort.
BASELINE_FILENAME_RE = re.compile(r"^(\d{8}T\d{6})\.json$")

CALIBRATION_MARGIN = 0.1


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Snapshot:
    """One captured ``(question, mode)`` snapshot.

    ``scores`` keys must match :data:`METRIC_KEYS` — extra/missing keys raise
    in :func:`compute_calibrated_thresholds`.
    """

    question_slug: str
    mode: str
    agents: list[str]
    scores: dict[str, float]


@dataclass
class BaselineFile:
    """Top-level JSON shape written to ``evals/baselines/<timestamp>.json``."""

    captured_at: str
    judge: dict[str, str]
    deliberation_provider: str
    snapshots: list[Snapshot] = field(default_factory=list)
    calibrated_thresholds: dict[str, float] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "captured_at": self.captured_at,
            "judge": self.judge,
            "deliberation_provider": self.deliberation_provider,
            "snapshots": [asdict(s) for s in self.snapshots],
            "calibrated_thresholds": self.calibrated_thresholds,
        }


# ---------------------------------------------------------------------------
# Core math (pure, testable without LLM calls)
# ---------------------------------------------------------------------------


def compute_calibrated_thresholds(
    snapshots: Iterable[Snapshot],
    *,
    margin: float = CALIBRATION_MARGIN,
    metric_keys: Iterable[str] = METRIC_KEYS,
    fallback: Mapping[str, float] = SPEC_DEFAULT_THRESHOLDS,
) -> dict[str, float]:
    """Return ``{metric: threshold}`` calibrated from the observed snapshots.

    For each metric, threshold = ``max(0.0, min(observed) - margin)``. A
    metric with zero observations falls back to ``fallback[metric]``.
    """
    snapshot_list = list(snapshots)
    out: dict[str, float] = {}
    for key in metric_keys:
        observed = [s.scores[key] for s in snapshot_list if key in s.scores]
        if not observed:
            out[key] = float(fallback.get(key, 0.0))
            continue
        out[key] = max(0.0, min(observed) - margin)
    return out


def find_latest_baseline(baselines_dir: Path) -> Path | None:
    """Return the newest ``<timestamp>.json`` file or ``None`` if none exist.

    "Newest" is determined by sorted filename — the timestamp format is
    monotonic, so lex sort matches chronological sort.
    """
    if not baselines_dir.is_dir():
        return None
    candidates = [
        p
        for p in baselines_dir.iterdir()
        if p.is_file() and BASELINE_FILENAME_RE.match(p.name)
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.name)[-1]


def load_calibrated_thresholds(
    baselines_dir: Path,
    *,
    fallback: Mapping[str, float] = SPEC_DEFAULT_THRESHOLDS,
) -> dict[str, float]:
    """Load ``calibrated_thresholds`` from the latest baseline file.

    Falls back to :data:`SPEC_DEFAULT_THRESHOLDS` when no baseline file
    exists, the file is malformed, or it is missing any metric key. The
    fallback is per-key, so a partially populated baseline still wins where
    it has data.
    """
    latest = find_latest_baseline(baselines_dir)
    if latest is None:
        return dict(fallback)
    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(fallback)
    thresholds = data.get("calibrated_thresholds")
    if not isinstance(thresholds, dict):
        return dict(fallback)
    out: dict[str, float] = {}
    for key in METRIC_KEYS:
        value = thresholds.get(key)
        if isinstance(value, (int, float)):
            out[key] = float(value)
        else:
            out[key] = float(fallback.get(key, 0.0))
    return out


# ---------------------------------------------------------------------------
# Question-set loading
# ---------------------------------------------------------------------------


def _slugify(prompt: str, *, max_len: int = 40) -> str:
    """Cheap deterministic slug for ad-hoc ``--questions`` inputs."""
    text = re.sub(r"[^a-z0-9]+", "-", prompt.lower()).strip("-")
    return text[:max_len] or "question"


def load_standard_questions(path: Path) -> list[dict[str, str]]:
    """Read the standard question bank from ``standard-questions.json``."""
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    if not isinstance(questions, list):
        raise ValueError(f"{path}: 'questions' must be a list")
    return [
        {"slug": q["slug"], "prompt": q["prompt"]}
        for q in questions
    ]


# ---------------------------------------------------------------------------
# Optional capture path (heavy — pulls in deepeval + pipeline)
# ---------------------------------------------------------------------------


def capture_snapshot(
    question_slug: str,
    prompt: str,
    mode: str,
    *,
    deliberation_provider: str,
    agents: list[str],
    work_root: Path,
) -> Snapshot:  # pragma: no cover — exercised manually with real providers
    """Run one deliberation and score its artifacts with the GEval metrics.

    This function is intentionally not covered by unit tests: it spawns a
    real provider call and a real LLM judge call per metric. The unit-test
    coverage for this script lives at ``scripts/tests/test_capture_eval_baselines.py``
    and exercises :func:`compute_calibrated_thresholds`,
    :func:`find_latest_baseline`, :func:`load_calibrated_thresholds`, and
    the slug/dataclass helpers — the calibration math is the load-bearing
    contract; the heavy-LLM capture is documented and invoked manually.
    """
    import asyncio

    # Defer heavy imports until the user actually triggers a capture; the
    # unit-test path never reaches this branch and so doesn't pay for them.
    from engine.config import AgentConfig, EngineConfig
    from engine.events import NullEmitter
    from engine.phases import run_pipeline
    from engine.run import resolve_execution_provider

    # Late import — the test module owns the metric-kwargs definitions.
    from engine.tests.test_evals import (
        _CROSS_REVIEW_ADVERSARIAL_KW,
        _DISPUTE_SPECIFICITY_KW,
        _REVIEW_INDEPENDENCE_KW,
        _REVISION_RESPONSIVENESS_KW,
        _SYNTHESIS_GROUNDING_KW,
        _build_metric,
    )
    from deepeval.test_case import LLMTestCase

    work_dir = work_root / f"{question_slug}__{mode}"
    work_dir.mkdir(parents=True, exist_ok=True)
    target = work_dir / "target.md"
    target.write_text(f"# Decision context\n\n{prompt}\n", encoding="utf-8")
    output_dir = work_dir / "output"
    output_dir.mkdir(exist_ok=True)

    config = EngineConfig(
        mode=mode,
        target_files=[target],
        output=output_dir,
        agents=[
            AgentConfig(
                name=name,
                prompt=(
                    f"You are reviewer {name}. Read the target and answer the "
                    f"question with concrete claims; do not hedge."
                ),
                docs=[],
            )
            for name in agents
        ],
        iterations=1,
        rounds=1,
        stagnation="detect",
        prior_files=[],
        arbiter=None,
        validate_templates=True,
    )
    provider = resolve_execution_provider(deliberation_provider)
    config_path = work_dir / "conversus.yml"
    config_path.write_text("# capture-eval-baselines stub\n", encoding="utf-8")
    result = asyncio.run(
        run_pipeline(config, provider, NullEmitter(), config_path=config_path)
    )
    out = result.output_dir

    reviews = {
        p.parent.name: p.read_text(encoding="utf-8")
        for p in sorted(out.glob("*/review.md"))
    }
    cross_reviews = {
        (p.parent.parent.name, p.stem): p.read_text(encoding="utf-8")
        for p in sorted(out.glob("*/cross-reviews/*.md"))
    }
    revisions = {
        p.parent.name: p.read_text(encoding="utf-8")
        for p in sorted(out.glob("*/revision.md"))
    }
    disputes = {
        p.parent.name: p.read_text(encoding="utf-8")
        for p in sorted(out.glob("*/disputes.md"))
    }
    synthesis_path = out / "summary" / "final.md"
    synthesis = (
        synthesis_path.read_text(encoding="utf-8") if synthesis_path.exists() else ""
    )

    # Score by taking the *minimum* per-metric score across all sub-artifacts —
    # this matches the corresponding test-evals assertion (every artifact must
    # clear the threshold) so the calibrated threshold reflects worst-case
    # observed behaviour, not the mean.
    def _score(metric_kw: dict, cases: list[LLMTestCase]) -> float | None:
        if not cases:
            return None
        metric = _build_metric(metric_kw)
        scores: list[float] = []
        for case in cases:
            metric.measure(case)
            if metric.score is not None:
                scores.append(float(metric.score))
        return min(scores) if scores else None

    review_cases = [
        LLMTestCase(
            input=f"Question: {prompt}\nCompare review by '{agent}' against the others.",
            actual_output=text,
        )
        for agent, text in reviews.items()
    ]
    cross_cases = [
        LLMTestCase(
            input=(
                f"Question: {prompt}\nOriginal review by '{reviewed}' that "
                f"'{reviewer}' is challenging:\n{reviews.get(reviewed, '')}"
            ),
            actual_output=text,
        )
        for (reviewer, reviewed), text in cross_reviews.items()
    ]
    revision_cases = []
    for agent, revision_text in revisions.items():
        challenges = [
            text
            for (reviewer, reviewed), text in cross_reviews.items()
            if reviewed == agent
        ]
        if challenges:
            revision_cases.append(
                LLMTestCase(
                    input=f"Question: {prompt}\nChallenges to '{agent}'.",
                    actual_output=revision_text,
                    context=challenges,
                )
            )
    dispute_cases = [
        LLMTestCase(
            input=f"Question: {prompt}\nDisputes from '{agent}'.",
            actual_output=text,
        )
        for agent, text in disputes.items()
    ]
    synthesis_cases = []
    if synthesis:
        synthesis_cases.append(
            LLMTestCase(
                input=f"Question: {prompt}\nPipeline produced reviews/revisions/disputes.",
                actual_output=synthesis,
                context=(
                    [f"Review by {a}:\n{t}" for a, t in reviews.items()]
                    + [f"Revision by {a}:\n{t}" for a, t in revisions.items()]
                    + [f"Disputes by {a}:\n{t}" for a, t in disputes.items()]
                ),
            )
        )

    scores: dict[str, float] = {}
    pairs = (
        ("review_independence", _REVIEW_INDEPENDENCE_KW, review_cases),
        ("cross_review_adversarial", _CROSS_REVIEW_ADVERSARIAL_KW, cross_cases),
        ("revision_responsiveness", _REVISION_RESPONSIVENESS_KW, revision_cases),
        ("dispute_specificity", _DISPUTE_SPECIFICITY_KW, dispute_cases),
        ("synthesis_grounding", _SYNTHESIS_GROUNDING_KW, synthesis_cases),
    )
    for key, kw, cases in pairs:
        s = _score(kw, cases)
        if s is not None:
            scores[key] = s
    return Snapshot(
        question_slug=question_slug,
        mode=mode,
        agents=list(agents),
        scores=scores,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="capture-eval-baselines",
        description=(
            "Capture deepeval baseline snapshots for spec 061 step 8. "
            "Runs the deliberation pipeline once per (question, mode) pair, "
            "scores artifacts with the five GEval metrics, and writes a "
            "JSON file containing snapshots plus a calibrated threshold "
            "table (min - 0.1)."
        ),
    )
    parser.add_argument(
        "--questions",
        nargs="*",
        default=None,
        help=(
            "Question prompts to capture. Defaults to the five-question bank "
            "in evals/baselines/standard-questions.json."
        ),
    )
    parser.add_argument(
        "--modes",
        nargs="*",
        default=None,
        help=(
            "Deliberation modes to capture. Defaults to the four primary modes: "
            "cooperative, winner-take-all, prisoners-dilemma, red-blue."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Output JSON path. Defaults to "
            "evals/baselines/<UTC-timestamp>.json relative to the repo root."
        ),
    )
    parser.add_argument(
        "--deliberation-provider",
        default=os.environ.get("CONVERSUS_EVAL_PROVIDER", "claude-code"),
        help="Provider used to run the deliberation. Defaults to CONVERSUS_EVAL_PROVIDER or claude-code.",
    )
    parser.add_argument(
        "--judge-provider",
        default=os.environ.get("CONVERSUS_EVAL_JUDGE_PROVIDER", "anthropic"),
        help="Judge provider used to score artifacts. Defaults to anthropic.",
    )
    parser.add_argument(
        "--judge-model",
        default=os.environ.get(
            "CONVERSUS_EVAL_JUDGE_MODEL", "claude-sonnet-4-20250514"
        ),
        help="Judge model name. Defaults to claude-sonnet-4-20250514.",
    )
    parser.add_argument(
        "--agents",
        nargs="+",
        default=["alice", "bob"],
        help="Agent names for the captured deliberation. Defaults to alice/bob.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip the pipeline run; emit a stub baseline file with empty snapshots.",
    )
    return parser.parse_args(argv)


def _default_output_path(repo_root: Path) -> Path:
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%S")
    return repo_root / "evals" / "baselines" / f"{timestamp}.json"


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(list(sys.argv[1:] if argv is None else argv))
    repo_root = Path(__file__).resolve().parents[1]

    # Resolve question set
    if args.questions:
        questions = [
            {"slug": _slugify(q), "prompt": q} for q in args.questions
        ]
    else:
        questions = load_standard_questions(
            repo_root / "evals" / "baselines" / "standard-questions.json"
        )

    modes = args.modes or [
        "cooperative",
        "winner-take-all",
        "prisoners-dilemma",
        "red-blue",
    ]

    output_path = args.output or _default_output_path(repo_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    snapshots: list[Snapshot] = []
    if not args.dry_run:  # pragma: no cover — heavy, manual path
        work_root = output_path.parent / f"_run-{output_path.stem}"
        for question in questions:
            for mode in modes:
                snap = capture_snapshot(
                    question_slug=question["slug"],
                    prompt=question["prompt"],
                    mode=mode,
                    deliberation_provider=args.deliberation_provider,
                    agents=list(args.agents),
                    work_root=work_root,
                )
                snapshots.append(snap)

    baseline = BaselineFile(
        captured_at=datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        judge={"provider": args.judge_provider, "model": args.judge_model},
        deliberation_provider=args.deliberation_provider,
        snapshots=snapshots,
        calibrated_thresholds=compute_calibrated_thresholds(snapshots),
    )

    output_path.write_text(
        json.dumps(baseline.to_json(), indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote baseline to {output_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
