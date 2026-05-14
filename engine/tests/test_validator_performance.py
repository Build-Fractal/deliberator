"""Performance budget validation framework — v4.2.0 spec § 5.1.1.

Measures the validator against the worked-example fixture corpus in two modes:
warm-cache (validator constructed once, fixtures validated 100× each) and
cold-cache (validator reconstructed per measurement, fixtures validated 10×
each). Emits a `validator-performance-report.json` artifact that CI uploads.

The asserted budget: warm-cache p99 < 100ms across the corpus (per § 5.1 D13
operational target). If the assertion fails, the validator is the bug; first
remediation is to profile and fix.

The v4.1.0 synthesis-corpus subset described in the spec is NOT present in this
repo at F2c time (those deliberations live in build-fractal-mono / consumer
repos). The framework reads any JSON files under `engine/tests/fixtures/v4_2_0/`
including the 6 conformant + 18 non-conformant fixtures, exercising the
validator's normal-case and error-case branches across all six output types.
When a future PR adds the synthesis-corpus subset to this repo, the framework
picks it up automatically (rglob over the fixture root).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pytest

from engine.schema_validator import SchemaValidator

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schema" / "v1"
FIXTURES_ROOT = Path(__file__).resolve().parent / "fixtures" / "v4_2_0"
REPORT_PATH = Path("validator-performance-report.json")

# Budget per § 5.1 D13. Warm-cache p99 must stay below this. The constant lives
# here (not in schema_validator.py) so changing the budget is a single-file edit
# and the spec citation is co-located with the assertion.
WARM_P99_BUDGET_MS = 100.0

# Iteration counts per § 5.1.1 measurement methodology.
WARM_ITERATIONS = 100
COLD_ITERATIONS = 10


def _percentile(samples: list[float], pct: float) -> float:
    """Compute the percentile pct (0-100) of a sorted-on-demand sample list.

    Linear-interpolated percentile — same convention NumPy uses by default.
    """
    if not samples:
        return 0.0
    ordered = sorted(samples)
    if len(ordered) == 1:
        return ordered[0]
    rank = (pct / 100.0) * (len(ordered) - 1)
    lo = int(rank)
    hi = min(lo + 1, len(ordered) - 1)
    frac = rank - lo
    return ordered[lo] + (ordered[hi] - ordered[lo]) * frac


def _stats(samples: list[float]) -> dict[str, float]:
    return {
        "n": len(samples),
        "p50_ms": _percentile(samples, 50),
        "p95_ms": _percentile(samples, 95),
        "p99_ms": _percentile(samples, 99),
        "max_ms": max(samples) if samples else 0.0,
    }


def _read_schema_version(content: bytes) -> str:
    try:
        envelope = json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "1.0.0-rc.1"
    if isinstance(envelope, dict):
        v = envelope.get("schema_version")
        if isinstance(v, str) and v:
            return v
    return "1.0.0-rc.1"


def _measure_warm(fixtures: list[Path]) -> dict[str, dict[str, float]]:
    """Validator constructed ONCE; each fixture validated WARM_ITERATIONS times."""
    validator = SchemaValidator(SCHEMA_DIR)
    per_fixture: dict[str, dict[str, float]] = {}
    for fixture in fixtures:
        content = fixture.read_bytes()
        version = _read_schema_version(content)
        samples: list[float] = []
        for _ in range(WARM_ITERATIONS):
            start = time.perf_counter_ns()
            validator.validate(content, version)
            samples.append((time.perf_counter_ns() - start) / 1_000_000.0)
        per_fixture[fixture.name] = _stats(samples)
    return per_fixture


def _measure_cold(fixtures: list[Path]) -> dict[str, dict[str, float]]:
    """Validator RECONSTRUCTED per sample; each fixture COLD_ITERATIONS times.

    Reflects production startup cost where the engine process boots, builds the
    validator, validates one output, then may not validate again for many
    seconds. Worst case for cache amortization.
    """
    per_fixture: dict[str, dict[str, float]] = {}
    for fixture in fixtures:
        content = fixture.read_bytes()
        version = _read_schema_version(content)
        samples: list[float] = []
        for _ in range(COLD_ITERATIONS):
            start = time.perf_counter_ns()
            validator = SchemaValidator(SCHEMA_DIR)
            validator.validate(content, version)
            samples.append((time.perf_counter_ns() - start) / 1_000_000.0)
        per_fixture[fixture.name] = _stats(samples)
    return per_fixture


def _all_fixtures() -> list[Path]:
    return sorted(
        p for p in FIXTURES_ROOT.rglob("*.json")
        if not p.name.endswith(".validation-warnings.json")
    )


@pytest.fixture(scope="module")
def performance_report() -> dict[str, Any]:
    """Build the full report once per test session and reuse across assertions."""
    fixtures = _all_fixtures()
    assert fixtures, f"no fixtures found under {FIXTURES_ROOT}"
    warm = _measure_warm(fixtures)
    cold = _measure_cold(fixtures)

    # Aggregate corpus-wide percentiles from all warm samples flattened.
    all_warm_samples: list[float] = []
    for stats in warm.values():
        all_warm_samples.extend(
            stats[k]
            for k in ("p50_ms", "p95_ms", "p99_ms")
            if stats[k] > 0.0
        )

    report = {
        "spec_section": "§ 5.1.1 performance budget validation framework",
        "warm_p99_budget_ms": WARM_P99_BUDGET_MS,
        "fixture_count": len(fixtures),
        "warm": warm,
        "cold": cold,
        "corpus_warm_p99_ms": _percentile(all_warm_samples, 99) if all_warm_samples else 0.0,
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def test_warm_cache_p99_under_budget(performance_report: dict[str, Any]) -> None:
    """The asserted operational target from § 5.1 D13 / § 5.1.1.

    Failure here means the validator's warm-cache p99 exceeds 100ms on the
    fixture corpus. Per spec: the validator is the bug — profile and fix.
    """
    over_budget: list[tuple[str, float]] = []
    for fixture_name, stats in performance_report["warm"].items():
        if stats["p99_ms"] > WARM_P99_BUDGET_MS:
            over_budget.append((fixture_name, stats["p99_ms"]))

    assert not over_budget, (
        f"Warm-cache p99 exceeded {WARM_P99_BUDGET_MS}ms budget on "
        f"{len(over_budget)} fixture(s): {over_budget}"
    )


def test_report_artifact_written(performance_report: dict[str, Any]) -> None:
    """The CI workflow uploads validator-performance-report.json — assert it exists."""
    assert REPORT_PATH.exists()
    parsed = json.loads(REPORT_PATH.read_text())
    assert parsed["fixture_count"] >= 6  # at minimum: 6 conformant fixtures


def test_cold_cache_samples_recorded(performance_report: dict[str, Any]) -> None:
    """Cold-cache measurements are present for the diagnostic record.

    No budget assertion on cold-cache — it's diagnostic. The warm path is what
    real production hits. Cold numbers exist to detect regression in
    construction cost (e.g., someone adds a slow schema-load step).
    """
    assert performance_report["cold"]
    for stats in performance_report["cold"].values():
        assert stats["n"] == COLD_ITERATIONS
