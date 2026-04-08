"""
Tests for linter.output_contract — canonical output format parser.

Exercises parse_synthesis() against all 3 reference outputs and verifies
model constraints (frozen, correct field extraction).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest
from pydantic import ValidationError

from linter.output_contract import (
    ConversusOutput,
    QualityIndicators,
    parse_synthesis,
    _extract_cross_reviews_performed,
    _extract_resolved_contradictions_count,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

REFERENCE_DIR = Path("quality-floor/reference-outputs")
MONOREPO_PATH = REFERENCE_DIR / "passing/monorepo-vs-polyrepo/summary/final.md"
LEASE_PATH = REFERENCE_DIR / "passing/lease-vs-buy/summary/final.md"
FACTUAL_PATH = REFERENCE_DIR / "failing/factual-capital/summary/final.md"


@pytest.fixture
def monorepo_text() -> str:
    return MONOREPO_PATH.read_text(encoding="utf-8")


@pytest.fixture
def lease_text() -> str:
    return LEASE_PATH.read_text(encoding="utf-8")


@pytest.fixture
def factual_text() -> str:
    return FACTUAL_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Model constraint tests
# ---------------------------------------------------------------------------


class TestModelConstraints:
    """Verify Pydantic models are frozen per Constitution Principle IX."""

    def test_quality_indicators_frozen(self) -> None:
        qi = QualityIndicators(
            agent_count=2,
            mode="cooperative",
            phases_completed=5,
            cross_reviews_performed=2,
            genuine_disagreements_surfaced=3,
            genuine_disagreements_surviving=3,
        )
        with pytest.raises(ValidationError):
            qi.agent_count = 99  # type: ignore[misc]

    def test_conversus_output_frozen(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        with pytest.raises(ValidationError):
            result.headline = "mutated"  # type: ignore[misc]

    def test_quality_indicators_has_all_six_fields(self) -> None:
        """QualityIndicators must have exactly the 6 D004 fields."""
        expected = {
            "agent_count",
            "mode",
            "phases_completed",
            "cross_reviews_performed",
            "genuine_disagreements_surfaced",
            "genuine_disagreements_surviving",
        }
        actual = set(QualityIndicators.model_fields.keys())
        assert actual == expected

    def test_conversus_output_has_all_five_fields(self) -> None:
        """ConversusOutput must have exactly the 5 contract fields."""
        expected = {
            "headline",
            "summary",
            "full_analysis",
            "quality_indicators",
            "debate_transcript",
        }
        actual = set(ConversusOutput.model_fields.keys())
        assert actual == expected


# ---------------------------------------------------------------------------
# Parser tests — monorepo reference output
# ---------------------------------------------------------------------------


class TestParseMonorepo:
    """Parser correctness against monorepo-vs-polyrepo reference output."""

    def test_agent_count(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert result.quality_indicators.agent_count == 2

    def test_mode(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert result.quality_indicators.mode == "cooperative"

    def test_phases_completed(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert result.quality_indicators.phases_completed == 5

    def test_cross_reviews_performed(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert result.quality_indicators.cross_reviews_performed == 2

    def test_disputes_surfaced(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        # 3 surviving disputes + 4 resolved contradictions = 7 surfaced
        assert result.quality_indicators.genuine_disagreements_surfaced == 7

    def test_disputes_surviving(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert result.quality_indicators.genuine_disagreements_surviving == 3

    def test_headline(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert "schema compatibility checks" in result.headline.lower()

    def test_full_analysis_contains_text(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert result.full_analysis == monorepo_text

    def test_debate_transcript_equals_full_analysis(self, monorepo_text: str) -> None:
        """In M001, debate_transcript == full_analysis."""
        result = parse_synthesis(monorepo_text)
        assert result.debate_transcript == result.full_analysis

    def test_summary_contains_structural_facts(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        assert "2 agents" in result.summary
        assert "cooperative" in result.summary
        assert "5 phases" in result.summary


# ---------------------------------------------------------------------------
# Parser tests — lease-vs-buy reference output
# ---------------------------------------------------------------------------


class TestParseLease:
    """Parser correctness against lease-vs-buy reference output."""

    def test_agent_count(self, lease_text: str) -> None:
        result = parse_synthesis(lease_text)
        assert result.quality_indicators.agent_count == 2

    def test_mode(self, lease_text: str) -> None:
        result = parse_synthesis(lease_text)
        assert result.quality_indicators.mode == "cooperative"

    def test_phases_completed(self, lease_text: str) -> None:
        result = parse_synthesis(lease_text)
        assert result.quality_indicators.phases_completed == 5

    def test_disputes_surfaced(self, lease_text: str) -> None:
        result = parse_synthesis(lease_text)
        # 4 surviving disputes + 3 resolved contradictions = 7 surfaced
        assert result.quality_indicators.genuine_disagreements_surfaced == 7

    def test_disputes_surviving(self, lease_text: str) -> None:
        result = parse_synthesis(lease_text)
        assert result.quality_indicators.genuine_disagreements_surviving == 4

    def test_headline(self, lease_text: str) -> None:
        result = parse_synthesis(lease_text)
        assert "cost model" in result.headline.lower()

    def test_summary_contains_structural_facts(self, lease_text: str) -> None:
        result = parse_synthesis(lease_text)
        assert "2 agents" in result.summary


# ---------------------------------------------------------------------------
# Parser tests — factual-capital reference output
# ---------------------------------------------------------------------------


class TestParseFactual:
    """Parser correctness against factual-capital reference output (0 disputes)."""

    def test_agent_count(self, factual_text: str) -> None:
        result = parse_synthesis(factual_text)
        assert result.quality_indicators.agent_count == 2

    def test_mode(self, factual_text: str) -> None:
        result = parse_synthesis(factual_text)
        assert result.quality_indicators.mode == "cooperative"

    def test_disputes_surfaced(self, factual_text: str) -> None:
        result = parse_synthesis(factual_text)
        assert result.quality_indicators.genuine_disagreements_surfaced == 0

    def test_disputes_surviving(self, factual_text: str) -> None:
        result = parse_synthesis(factual_text)
        assert result.quality_indicators.genuine_disagreements_surviving == 0

    def test_headline(self, factual_text: str) -> None:
        result = parse_synthesis(factual_text)
        assert "paris" in result.headline.lower()

    def test_full_analysis_contains_text(self, factual_text: str) -> None:
        result = parse_synthesis(factual_text)
        assert result.full_analysis == factual_text


# ---------------------------------------------------------------------------
# C1: Cross-review count formula tests
# ---------------------------------------------------------------------------


class TestCrossReviewFormula:
    """Verify _extract_cross_reviews_performed returns agent_count * (agent_count - 1)."""

    @pytest.mark.parametrize(
        "agent_count, expected",
        [
            (0, 0),
            (1, 0),
            (2, 2),
            (3, 6),
            (4, 12),
        ],
    )
    def test_cross_review_count(self, agent_count: int, expected: int) -> None:
        # text is unused by the function; it infers from agent_count only
        assert _extract_cross_reviews_performed("irrelevant", agent_count) == expected


# ---------------------------------------------------------------------------
# C2: Surfaced vs surviving disagreements
# ---------------------------------------------------------------------------


class TestResolvedContradictions:
    """Verify _extract_resolved_contradictions_count and surfaced != surviving."""

    def test_monorepo_has_resolved_contradictions(self, monorepo_text: str) -> None:
        count = _extract_resolved_contradictions_count(monorepo_text)
        assert count == 4  # 4 resolved items in monorepo reference

    def test_lease_has_resolved_contradictions(self, lease_text: str) -> None:
        count = _extract_resolved_contradictions_count(lease_text)
        assert count == 3  # 3 resolved items in lease reference

    def test_factual_has_zero_resolved_contradictions(self, factual_text: str) -> None:
        count = _extract_resolved_contradictions_count(factual_text)
        # Factual has no numbered resolved contradictions (only framework items)
        assert count == 0

    def test_monorepo_surfaced_greater_than_surviving(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        qi = result.quality_indicators
        assert qi.genuine_disagreements_surfaced > qi.genuine_disagreements_surviving

    def test_monorepo_surfaced_equals_disputes_plus_resolved(self, monorepo_text: str) -> None:
        result = parse_synthesis(monorepo_text)
        qi = result.quality_indicators
        resolved = _extract_resolved_contradictions_count(monorepo_text)
        assert qi.genuine_disagreements_surfaced == qi.genuine_disagreements_surviving + resolved

    def test_factual_surfaced_equals_surviving(self, factual_text: str) -> None:
        result = parse_synthesis(factual_text)
        qi = result.quality_indicators
        assert qi.genuine_disagreements_surfaced == qi.genuine_disagreements_surviving == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Edge cases and error handling."""

    def test_empty_string_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            parse_synthesis("")

    def test_whitespace_only_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            parse_synthesis("   \n\t  ")

    def test_mode_parameter_used_as_fallback(self) -> None:
        """When text has no mode header, the mode parameter is used."""
        text = "# Synthesis: Test\n\nSome content with no mode header."
        result = parse_synthesis(text, mode="winner-take-all")
        assert result.quality_indicators.mode == "winner-take-all"

    def test_minimal_valid_input(self) -> None:
        """A minimal non-empty string should not crash."""
        text = "# Synthesis: Minimal Test\n\nJust some text."
        result = parse_synthesis(text)
        assert result.headline == "Minimal Test"
        assert result.quality_indicators.agent_count == 0
        assert result.quality_indicators.genuine_disagreements_surfaced == 0

    def test_output_serializes_to_valid_json(self, monorepo_text: str) -> None:
        """model_dump_json() must produce valid, parseable JSON."""
        result = parse_synthesis(monorepo_text)
        raw = result.model_dump_json(indent=2)
        parsed = json.loads(raw)
        assert "headline" in parsed
        assert "quality_indicators" in parsed
        assert parsed["quality_indicators"]["genuine_disagreements_surfaced"] == 7


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestCLI:
    """CLI entry point exit codes and JSON output."""

    def test_cli_monorepo_exits_zero(self) -> None:
        r = subprocess.run(
            ["uv", "run", "python3", "-m", "linter.output_contract", str(MONOREPO_PATH)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["quality_indicators"]["genuine_disagreements_surfaced"] == 7

    def test_cli_factual_exits_zero(self) -> None:
        r = subprocess.run(
            ["uv", "run", "python3", "-m", "linter.output_contract", str(FACTUAL_PATH)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        assert data["quality_indicators"]["genuine_disagreements_surfaced"] == 0

    def test_cli_nonexistent_file_exits_two(self) -> None:
        r = subprocess.run(
            ["uv", "run", "python3", "-m", "linter.output_contract", "/nonexistent/path.md"],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 2

    def test_cli_lease_has_all_five_fields(self) -> None:
        r = subprocess.run(
            ["uv", "run", "python3", "-m", "linter.output_contract", str(LEASE_PATH)],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        for field in ("headline", "summary", "full_analysis", "quality_indicators", "debate_transcript"):
            assert field in data, f"Missing top-level field: {field}"

    def test_cli_mode_flag(self) -> None:
        r = subprocess.run(
            [
                "uv", "run", "python3", "-m", "linter.output_contract",
                str(MONOREPO_PATH), "--mode", "winner-take-all",
            ],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 0
        data = json.loads(r.stdout)
        # monorepo has explicit mode header, so --mode flag is overridden
        assert data["quality_indicators"]["mode"] == "cooperative"
