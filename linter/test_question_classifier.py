"""
Tests for linter.question_classifier — heuristic question classifier
for conversus deliberation input sufficiency.

Covers:
- Empty/trivially short inputs
- Factual question detection
- Vague inputs (both modes)
- Sufficient inputs with decision structure
- Mode differences (interactive vs non-interactive)
- Model immutability (frozen=True)
- CLI entry point exit codes and JSON output
"""

from __future__ import annotations

import json
import subprocess
import sys

import pytest
from pydantic import ValidationError

from conversus.schemas.duration import Duration, TemporalMatch
from linter.question_classifier import (
    ClassificationResult,
    classify_question,
    extract_temporal_constraints,
    has_constraints,
)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestClassificationResultModel:
    """ClassificationResult Pydantic model constraints."""

    def test_all_four_fields_present(self) -> None:
        r = ClassificationResult(
            sufficient=True,
            reason="test",
            clarification_question=None,
            missing_fields=None,
        )
        assert r.sufficient is True
        assert r.reason == "test"
        assert r.clarification_question is None
        assert r.missing_fields is None

    def test_frozen_immutability(self) -> None:
        r = ClassificationResult(
            sufficient=False,
            reason="frozen",
            clarification_question="ask",
            missing_fields=None,
        )
        with pytest.raises(ValidationError):
            r.sufficient = True  # type: ignore[misc]
        with pytest.raises(ValidationError):
            r.reason = "changed"  # type: ignore[misc]

    def test_optional_fields_accept_values(self) -> None:
        r = ClassificationResult(
            sufficient=False,
            reason="test",
            clarification_question="What options?",
            missing_fields=["constraints", "alternatives"],
        )
        assert r.clarification_question == "What options?"
        assert r.missing_fields == ["constraints", "alternatives"]

    def test_json_round_trip(self) -> None:
        r = ClassificationResult(
            sufficient=False,
            reason="test reason",
            clarification_question="clarify?",
            missing_fields=["field_a"],
        )
        data = json.loads(r.model_dump_json())
        assert data["sufficient"] is False
        assert data["reason"] == "test reason"
        assert data["clarification_question"] == "clarify?"
        assert data["missing_fields"] == ["field_a"]


# ---------------------------------------------------------------------------
# Empty / short inputs
# ---------------------------------------------------------------------------


class TestEmptyShortInputs:
    """Empty and trivially short inputs should be classified as insufficient."""

    @pytest.mark.parametrize(
        "question",
        [
            "",
            "help",
            "what?",
        ],
    )
    def test_short_inputs_insufficient(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert r.sufficient is False

    @pytest.mark.parametrize(
        "question",
        [
            "",
            "help",
            "what?",
        ],
    )
    def test_short_inputs_reason_mentions_short(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert "too short" in r.reason.lower()

    def test_empty_non_interactive_has_missing_fields(self) -> None:
        r = classify_question("", mode="non-interactive")
        assert r.sufficient is False
        assert r.missing_fields is not None
        assert len(r.missing_fields) > 0

    def test_decide_for_me_insufficient(self) -> None:
        """'decide for me' is a low-effort delegation, not a question."""
        r = classify_question("decide for me", mode="non-interactive")
        assert r.sufficient is False


# ---------------------------------------------------------------------------
# Factual inputs
# ---------------------------------------------------------------------------


class TestFactualInputs:
    """Factual questions with single correct answers should be caught."""

    @pytest.mark.parametrize(
        "question",
        [
            "What is the capital of France?",
            "Who invented the telephone?",
            "Define photosynthesis",
            "When did World War 2 end?",
            "Where is the Eiffel Tower?",
            "How many planets are in the solar system?",
        ],
    )
    def test_factual_insufficient(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert r.sufficient is False

    @pytest.mark.parametrize(
        "question",
        [
            "What is the capital of France?",
            "Who invented the telephone?",
            "Define photosynthesis",
        ],
    )
    def test_factual_reason_mentions_factual(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert "factual" in r.reason.lower()

    def test_factual_interactive_has_clarification(self) -> None:
        r = classify_question("What is the capital of France?", mode="interactive")
        assert r.clarification_question is not None
        assert "reframe" in r.clarification_question.lower()

    def test_factual_non_interactive_has_missing_fields(self) -> None:
        r = classify_question("What is the capital of France?", mode="non-interactive")
        assert r.missing_fields is not None
        assert any("factual" in f.lower() for f in r.missing_fields)

    def test_factual_with_decision_words_is_not_factual(self) -> None:
        """A question starting with 'What is' but containing decision words
        should not be classified as factual."""
        r = classify_question(
            "What is the better approach for handling errors — "
            "exceptions or result types in a large codebase?",
            mode="interactive",
        )
        # Should NOT be classified as factual because it has decision words
        assert "factual" not in r.reason.lower()


# ---------------------------------------------------------------------------
# Vague inputs
# ---------------------------------------------------------------------------


class TestVagueInputs:
    """Vague inputs that lack decision structure should be insufficient."""

    @pytest.mark.parametrize(
        "question",
        [
            "help me decide",
            "what should I do about my career",
            "I need advice",
        ],
    )
    def test_vague_insufficient(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert r.sufficient is False

    @pytest.mark.parametrize(
        "question",
        [
            "help me decide",
            "what should I do about my career",
            "I need advice",
        ],
    )
    def test_vague_interactive_has_clarification(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert r.clarification_question is not None
        assert len(r.clarification_question) > 10

    @pytest.mark.parametrize(
        "question",
        [
            "help me decide",
            "what should I do about my career",
            "I need advice",
        ],
    )
    def test_vague_non_interactive_has_missing_fields(self, question: str) -> None:
        r = classify_question(question, mode="non-interactive")
        assert r.missing_fields is not None
        assert len(r.missing_fields) > 0


# ---------------------------------------------------------------------------
# Sufficient inputs
# ---------------------------------------------------------------------------


class TestSufficientInputs:
    """Questions with decision/trade-off structure should pass."""

    @pytest.mark.parametrize(
        "question",
        [
            "Should I use a monorepo or polyrepo for my 15-person team with 3 polyglot services?",
            "Lease vs buy a mid-size sedan given 12k miles/year and $400-500/month budget",
            "Should I take the remote job at higher pay or the in-office role with better growth?",
            "Whether to use PostgreSQL or MongoDB for a social media app with complex relationships and 10M users",
            "Compare React and Vue for a team of 5 junior developers building an internal dashboard",
        ],
    )
    def test_sufficient_inputs(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert r.sufficient is True

    @pytest.mark.parametrize(
        "question",
        [
            "Should I use a monorepo or polyrepo for my 15-person team with 3 polyglot services?",
            "Lease vs buy a mid-size sedan given 12k miles/year and $400-500/month budget",
        ],
    )
    def test_sufficient_reason(self, question: str) -> None:
        r = classify_question(question, mode="interactive")
        assert "suitable" in r.reason.lower()

    def test_sufficient_no_clarification(self) -> None:
        r = classify_question(
            "Should I use a monorepo or polyrepo for my 15-person team?",
            mode="interactive",
        )
        assert r.clarification_question is None

    def test_sufficient_no_missing_fields(self) -> None:
        r = classify_question(
            "Should I use a monorepo or polyrepo for my 15-person team?",
            mode="non-interactive",
        )
        assert r.missing_fields is None


# ---------------------------------------------------------------------------
# Mode differences
# ---------------------------------------------------------------------------


class TestModeDifferences:
    """Interactive and non-interactive modes should return different fields."""

    def test_interactive_returns_clarification_not_missing(self) -> None:
        r = classify_question("help me decide", mode="interactive")
        assert r.sufficient is False
        assert r.clarification_question is not None
        assert r.missing_fields is None

    def test_non_interactive_returns_missing_not_clarification(self) -> None:
        r = classify_question("help me decide", mode="non-interactive")
        assert r.sufficient is False
        assert r.missing_fields is not None
        assert r.clarification_question is None

    def test_sufficient_same_in_both_modes(self) -> None:
        q = "Should I use a monorepo or polyrepo for my 15-person team with 3 services?"
        r_i = classify_question(q, mode="interactive")
        r_ni = classify_question(q, mode="non-interactive")
        assert r_i.sufficient is True
        assert r_ni.sufficient is True
        assert r_i.clarification_question is None
        assert r_ni.missing_fields is None

    def test_default_mode_is_interactive(self) -> None:
        r = classify_question("help me decide")
        assert r.clarification_question is not None
        assert r.missing_fields is None

    def test_factual_interactive_has_clarification(self) -> None:
        r = classify_question("What is the capital of France?", mode="interactive")
        assert r.clarification_question is not None

    def test_factual_non_interactive_has_missing(self) -> None:
        r = classify_question("What is the capital of France?", mode="non-interactive")
        assert r.missing_fields is not None


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestCLI:
    """CLI entry point: JSON output, exit codes."""

    def _run_cli(self, question: str, mode: str = "interactive") -> tuple[int, dict]:
        """Run the CLI and return (exit_code, parsed_json)."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "linter.question_classifier",
                question,
                "--mode",
                mode,
            ],
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout) if result.stdout.strip() else {}
        return result.returncode, data

    def test_sufficient_exits_0(self) -> None:
        code, data = self._run_cli(
            "Should I use a monorepo or polyrepo for my 15-person team?",
            mode="interactive",
        )
        assert code == 0
        assert data["sufficient"] is True

    def test_insufficient_exits_1(self) -> None:
        code, data = self._run_cli("help", mode="non-interactive")
        assert code == 1
        assert data["sufficient"] is False

    def test_non_interactive_missing_fields_populated(self) -> None:
        code, data = self._run_cli("help", mode="non-interactive")
        assert code == 1
        assert data["missing_fields"] is not None
        assert len(data["missing_fields"]) > 0

    def test_factual_exits_1(self) -> None:
        code, data = self._run_cli("What is the capital of France?")
        assert code == 1
        assert "factual" in data["reason"].lower()

    def test_output_is_valid_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "linter.question_classifier",
                "help me decide",
                "--mode",
                "non-interactive",
            ],
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        assert "sufficient" in data
        assert "reason" in data
        assert "clarification_question" in data
        assert "missing_fields" in data

    def test_empty_string_non_interactive_exits_1(self) -> None:
        """Failure-path: empty string produces structured error, exits 1."""
        code, data = self._run_cli("", mode="non-interactive")
        assert code == 1
        assert data["sufficient"] is False
        assert data["missing_fields"] is not None
        assert len(data["missing_fields"]) > 0


# ---------------------------------------------------------------------------
# Spec 047 integration — extract_temporal_constraints + has_constraints
# ---------------------------------------------------------------------------


class TestExtractTemporalConstraints:
    """Structured temporal extraction (FR-010)."""

    def test_returns_temporal_match_list(self) -> None:
        out = extract_temporal_constraints("ship by 3 months")
        assert isinstance(out, list)
        assert all(isinstance(m, TemporalMatch) for m in out)

    def test_extracts_numeric_duration(self) -> None:
        out = extract_temporal_constraints("response under 100ms")
        assert any(
            m.duration == Duration(milliseconds=100) and m.category == "performance"
            for m in out
        )

    def test_extracts_fiscal_deadline(self) -> None:
        out = extract_temporal_constraints("ship by Q2 2026")
        assert any(m.duration is None and m.category == "deadline" for m in out)

    def test_empty_returns_empty_list(self) -> None:
        assert extract_temporal_constraints("") == []

    def test_garbage_returns_empty_list(self) -> None:
        assert extract_temporal_constraints("xyzzy plugh") == []


class TestHasConstraintsBackwardCompat:
    """FR-009 — boolean output preserved for inputs the old regex flagged."""

    @pytest.mark.parametrize(
        "text",
        [
            "given 3 months of runway",
            "deadline next Friday",
            "by 6 months from now",
            "the team has 5 people",
            "$10k budget",
            "remote-first company with 12 employees",
            "valid for 30 days then expires",
            "alert within 5 minutes",
            "over the last 2 weeks performance dropped",
        ],
    )
    def test_known_constraints_still_true(self, text: str) -> None:
        assert has_constraints(text) is True

    @pytest.mark.parametrize(
        "text",
        [
            "what color is the sky",
            "tell me a joke",
            "",
        ],
    )
    def test_no_constraints_returns_false(self, text: str) -> None:
        assert has_constraints(text) is False
