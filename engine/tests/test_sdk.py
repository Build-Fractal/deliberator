"""SDK tests — prove every public surface of engine.sdk works correctly.

Tests cover:
- Config-path mode: ``Deliberation(config_path=...).run()`` returns ``Result``
- Ad-hoc question mode: ``Deliberation(question=...).run()`` returns ``Result``
- Event subscription: ``on(PhaseStarted, cb)`` fires during pipeline execution
- Validation: ``validate()`` with valid and invalid config paths
- Classification: ``classify()`` with sufficient and insufficient questions
- Model immutability: ``Result`` frozen — attribute assignment raises
- Error cases: missing config_path *and* question raises ``ValueError``
- Cost estimate: ``Deliberation.cost_estimate`` property works for both modes

All tests use ``MockProvider`` — no real API calls.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from engine.events import PhaseCompleted, PhaseStarted
from engine.sdk import (
    Deliberation,
    Result,
    ValidateResult,
    classify,
    validate,
)
from linter.question_classifier import ClassificationResult


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sdk_config_path(tmp_path: Path) -> Path:
    """Create a minimal but valid conversus config in a temp directory.

    Returns the path to the config file.  Output is routed to tmp_path so
    tests never pollute the project tree.
    """
    spec = tmp_path / "spec.md"
    spec.write_text("# SDK Test Spec\n\nThis is a spec for SDK tests.\n")

    output_dir = tmp_path / "output"

    config_data = {
        "mode": "cooperative",
        "target": "spec.md",
        "output": str(output_dir),
        "iterations": 1,
        "agents": [
            {"name": "agent-alpha", "prompt": "Alpha perspective."},
            {"name": "agent-beta", "prompt": "Beta perspective."},
        ],
    }
    config_path = tmp_path / "conversus.yml"
    config_path.write_text(yaml.dump(config_data, sort_keys=False))
    return config_path


# ---------------------------------------------------------------------------
# Config-path mode
# ---------------------------------------------------------------------------


class TestDeliberationConfigPath:
    """Deliberation(config_path=...).run() returns a fully populated Result."""

    @pytest.mark.asyncio
    async def test_run_returns_result_with_all_fields(
        self, sdk_config_path: Path, tmp_path: Path
    ) -> None:
        d = Deliberation(config_path=sdk_config_path, provider="mock")
        result = await d.run()

        assert isinstance(result, Result)
        # Core content fields (mock returns minimal text, but fields are present)
        assert isinstance(result.headline, str)
        assert isinstance(result.summary, str)
        assert isinstance(result.full_analysis, str)
        assert isinstance(result.debate_transcript, str)

        # Quality indicators
        assert result.quality_indicators is not None
        assert isinstance(result.quality_indicators.agent_count, int)
        assert isinstance(result.quality_indicators.mode, str)

        # Pipeline metadata
        assert result.rounds_completed >= 1
        assert isinstance(result.written_files, list)
        assert len(result.written_files) > 0
        assert result.output_dir.exists()

    @pytest.mark.asyncio
    async def test_output_dir_contains_synthesis(
        self, sdk_config_path: Path
    ) -> None:
        d = Deliberation(config_path=sdk_config_path, provider="mock")
        result = await d.run()

        synthesis_path = result.output_dir / "summary" / "final.md"
        assert synthesis_path.exists()
        content = synthesis_path.read_text(encoding="utf-8")
        assert len(content) > 0


# ---------------------------------------------------------------------------
# Ad-hoc question mode
# ---------------------------------------------------------------------------


class TestDeliberationAdHocQuestion:
    """Deliberation(question=...).run() returns a valid Result."""

    @pytest.mark.asyncio
    async def test_ad_hoc_question_returns_result(self) -> None:
        d = Deliberation(
            question="Should we use SQLite or Postgres for the user session store?",
            provider="mock",
        )
        result = await d.run()

        assert isinstance(result, Result)
        assert isinstance(result.headline, str)
        assert isinstance(result.summary, str)
        assert isinstance(result.full_analysis, str)
        assert result.rounds_completed >= 1

    @pytest.mark.asyncio
    async def test_ad_hoc_with_custom_mode(self) -> None:
        d = Deliberation(
            question="Should we use microservices or monolith?",
            provider="mock",
            mode="winner-take-all",
        )
        result = await d.run()

        assert isinstance(result, Result)
        assert result.rounds_completed >= 1


# ---------------------------------------------------------------------------
# Event subscription
# ---------------------------------------------------------------------------


class TestEventSubscription:
    """on(event_type, callback) fires registered callbacks during pipeline execution."""

    @pytest.mark.asyncio
    async def test_phase_started_callback_fires(
        self, sdk_config_path: Path
    ) -> None:
        started_events: list[PhaseStarted] = []

        d = Deliberation(config_path=sdk_config_path, provider="mock")
        d.on(PhaseStarted, lambda e: started_events.append(e))
        await d.run()

        assert len(started_events) >= 1
        assert all(isinstance(e, PhaseStarted) for e in started_events)
        # A full cooperative pipeline emits 5 PhaseStarted events
        phases = [e.phase for e in started_events]
        assert "review" in phases

    @pytest.mark.asyncio
    async def test_phase_completed_callback_fires(
        self, sdk_config_path: Path
    ) -> None:
        completed_events: list[PhaseCompleted] = []

        d = Deliberation(config_path=sdk_config_path, provider="mock")
        d.on(PhaseCompleted, lambda e: completed_events.append(e))
        await d.run()

        assert len(completed_events) >= 1
        assert all(isinstance(e, PhaseCompleted) for e in completed_events)

    @pytest.mark.asyncio
    async def test_multiple_callbacks_for_same_event(
        self, sdk_config_path: Path
    ) -> None:
        counts = {"a": 0, "b": 0}

        d = Deliberation(config_path=sdk_config_path, provider="mock")
        d.on(PhaseStarted, lambda e: counts.update(a=counts["a"] + 1))
        d.on(PhaseStarted, lambda e: counts.update(b=counts["b"] + 1))
        await d.run()

        assert counts["a"] >= 1
        assert counts["b"] >= 1
        assert counts["a"] == counts["b"]  # both fired the same number of times


# ---------------------------------------------------------------------------
# validate()
# ---------------------------------------------------------------------------


class TestValidate:
    """validate() returns structured ValidateResult for valid and invalid configs."""

    def test_valid_config_returns_valid_result(
        self, sdk_config_path: Path
    ) -> None:
        result = validate(sdk_config_path)

        assert isinstance(result, ValidateResult)
        assert result.valid is True
        assert result.errors == []
        assert result.config is not None
        assert result.cost_estimate is not None
        assert isinstance(result.cost_estimate, dict)
        assert "review" in result.cost_estimate
        assert "synthesis" in result.cost_estimate

    def test_invalid_path_returns_invalid_result(self) -> None:
        result = validate(Path("/nonexistent/conversus.yml"))

        assert isinstance(result, ValidateResult)
        assert result.valid is False
        assert len(result.errors) > 0
        assert result.config is None
        assert result.cost_estimate is None

    def test_validate_never_raises(self, tmp_path: Path) -> None:
        """validate() captures errors — never raises exceptions."""
        # Write an invalid YAML config (missing required fields)
        bad_config = tmp_path / "bad.yml"
        bad_config.write_text("mode: cooperative\n# missing target and agents\n")

        result = validate(bad_config)

        assert isinstance(result, ValidateResult)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_valid_config_cost_estimate_structure(
        self, sdk_config_path: Path
    ) -> None:
        """Cost estimate contains expected phase keys with integer counts."""
        result = validate(sdk_config_path)

        assert result.valid is True
        cost = result.cost_estimate
        assert cost is not None
        expected_phases = {"review", "cross_review", "revision", "disputes", "synthesis"}
        assert expected_phases.issubset(cost.keys())
        for phase, count in cost.items():
            assert isinstance(count, int)
            assert count >= 1

    def test_iterations_3_cost_estimate_scales_linearly(
        self, tmp_path: Path
    ) -> None:
        """iterations=3 with 2 agents → cross_review=6, revision=6.

        Closes spec 061 step 13 §3.1.9 cost estimate gap (issue #109)
        per the strip-script-061-substeps deliberation 2026-05-01.

        Pins the documented per-iteration multiplier: with N agents and
        I iterations, cross_review = I * N * (N-1) and revision =
        I * N. For N=2, I=3: cross_review = 3 * 2 * 1 = 6; revision =
        3 * 2 = 6. The pre-existing iterations=1 default gives
        cross_review = 2; iterations=2 (covered by the pre-existing
        execution test in test_phases.py) gives cross_review = 4;
        iterations=3 fills the matrix at the cost-estimate API layer.
        """
        spec = tmp_path / "spec.md"
        spec.write_text("# Test Spec\n\nIterations=3 cost-estimate test.\n")
        output_dir = tmp_path / "output"

        config_data = {
            "mode": "cooperative",
            "target": "spec.md",
            "output": str(output_dir),
            "iterations": 3,
            "agents": [
                {"name": "agent-alpha", "prompt": "Alpha perspective."},
                {"name": "agent-beta", "prompt": "Beta perspective."},
            ],
        }
        config_path = tmp_path / "conversus.yml"
        config_path.write_text(yaml.dump(config_data, sort_keys=False))

        result = validate(config_path)

        assert result.valid is True
        cost = result.cost_estimate
        assert cost is not None

        # Linear scaling assertions
        assert cost["review"] == 2, "review = N agents (1 per iteration entry, but only run once)"
        assert cost["cross_review"] == 6, (
            f"cross_review must scale as iterations × N × (N-1) = 3 × 2 × 1 = 6, got {cost['cross_review']}"
        )
        assert cost["revision"] == 6, (
            f"revision must scale as iterations × N = 3 × 2 = 6, got {cost['revision']}"
        )
        assert cost["disputes"] == 2
        assert cost["synthesis"] == 1


# ---------------------------------------------------------------------------
# classify()
# ---------------------------------------------------------------------------


class TestClassify:
    """classify() classifies question sufficiency for deliberation."""

    def test_sufficient_question(self) -> None:
        result = classify(
            "Should our team adopt Redis or Memcached for caching given our 10ms latency requirement?"
        )

        assert isinstance(result, ClassificationResult)
        assert result.sufficient is True
        assert isinstance(result.reason, str)

    def test_insufficient_question(self) -> None:
        result = classify("hi")

        assert isinstance(result, ClassificationResult)
        assert result.sufficient is False
        assert isinstance(result.reason, str)

    def test_classification_returns_frozen_model(self) -> None:
        result = classify(
            "Should our team adopt Redis or Memcached for caching given our 10ms latency requirement?"
        )
        with pytest.raises(ValidationError):
            result.sufficient = not result.sufficient  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Model immutability
# ---------------------------------------------------------------------------


class TestModelImmutability:
    """Frozen Pydantic models reject attribute mutation."""

    def test_result_is_frozen(self) -> None:
        from linter.output_contract import QualityIndicators

        result = Result(
            headline="Test headline",
            summary="Test summary",
            full_analysis="Full analysis text",
            quality_indicators=QualityIndicators(
                agent_count=2,
                mode="cooperative",
                phases_completed=5,
                cross_reviews_performed=2,
                genuine_disagreements_surfaced=1,
                genuine_disagreements_surviving=0,
            ),
            debate_transcript="Debate transcript text",
            rounds_completed=1,
            termination_reason=None,
            written_files=[],
            output_dir=Path("/tmp/test"),
        )

        with pytest.raises(ValidationError):
            result.headline = "Mutated"  # type: ignore[misc]

    def test_validate_result_is_frozen(self) -> None:
        vr = ValidateResult(valid=True, errors=[])
        with pytest.raises(ValidationError):
            vr.valid = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------


class TestErrorCases:
    """Deliberation raises clear errors for invalid construction."""

    def test_no_config_path_or_question_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="config_path.*question"):
            Deliberation()

    def test_empty_question_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="config_path.*question"):
            Deliberation(question="")

    def test_whitespace_only_question_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="config_path.*question"):
            Deliberation(question="   ")


# ---------------------------------------------------------------------------
# Cost estimate property
# ---------------------------------------------------------------------------


class TestCostEstimate:
    """Deliberation.cost_estimate returns per-phase launch counts without running."""

    def test_config_path_cost_estimate(self, sdk_config_path: Path) -> None:
        d = Deliberation(config_path=sdk_config_path, provider="mock")
        cost = d.cost_estimate

        assert cost is not None
        assert isinstance(cost, dict)
        assert "review" in cost
        assert "synthesis" in cost
        # 2 agents → review = 2, cross_review = 2, etc.
        assert cost["review"] == 2
        assert cost["synthesis"] == 1

    def test_ad_hoc_question_cost_estimate(self) -> None:
        d = Deliberation(
            question="Should we use Redis or Memcached?",
            provider="mock",
        )
        cost = d.cost_estimate

        assert cost is not None
        assert isinstance(cost, dict)
        assert "review" in cost
        # Default ad-hoc mode uses 2 agents
        assert cost["review"] == 2
        assert cost["synthesis"] == 1

    def test_invalid_config_path_cost_estimate_returns_none(
        self, tmp_path: Path
    ) -> None:
        bad_path = tmp_path / "nonexistent.yml"
        d = Deliberation(config_path=bad_path, provider="mock")
        cost = d.cost_estimate

        assert cost is None


# ---------------------------------------------------------------------------
# Import sanity
# ---------------------------------------------------------------------------


class TestImports:
    """Public API is importable from engine top-level and engine.sdk."""

    def test_top_level_imports(self) -> None:
        from engine import Deliberation, Result, validate

        assert Deliberation is not None
        assert Result is not None
        assert validate is not None

    def test_sdk_module_imports(self) -> None:
        from engine.sdk import (
            Deliberation,
            Result,
            ValidateResult,
            classify,
            validate,
        )

        assert Deliberation is not None
        assert Result is not None
        assert ValidateResult is not None
        assert classify is not None
        assert validate is not None
