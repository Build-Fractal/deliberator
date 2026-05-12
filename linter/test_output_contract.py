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

REFERENCE_DIR = Path("conversus/quality_floor/reference-outputs")
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
        """When text has no mode header, the mode parameter is used.

        Fixture includes a metadata block with no ``mode:`` field so the
        structural-evidence guard is satisfied (agent_count > 0) while the
        mode-extraction path still falls through to the caller default.
        """
        text = (
            "<!-- CONVERSUS:METADATA\n"
            "agents: 2\n"
            "agent_names: a, b\n"
            "phases_completed: 5\n"
            "iterations: 1\n"
            "-->\n\n"
            "# Synthesis: Test\n\nSome content with no mode header."
        )
        result = parse_synthesis(text, mode="winner-take-all")
        assert result.quality_indicators.mode == "winner-take-all"

    def test_minimal_valid_input(self) -> None:
        """A minimal synthesis (metadata block + title + empty body) must
        parse, even with zero disputes and zero convergence. This is the
        legitimate "clean pass" shape.

        The guard explicitly refuses pure-prose fixtures with no structural
        markers at all — that behavior is covered in
        TestUnparseableSynthesisGuard; here we confirm the minimum-valid
        shape still parses.
        """
        text = (
            "<!-- CONVERSUS:METADATA\n"
            "agents: 2\n"
            "agent_names: a, b\n"
            "mode: cooperative\n"
            "phases_completed: 5\n"
            "iterations: 1\n"
            "-->\n\n"
            "# Synthesis: Minimal Test\n\nJust some text."
        )
        result = parse_synthesis(text)
        assert result.headline == "Minimal Test"
        assert result.quality_indicators.agent_count == 2
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


# ---------------------------------------------------------------------------
# Layer 2/3 regression tests — red-blue Landed Attacks + parse-failure guard
# ---------------------------------------------------------------------------


class TestRedBlueLandedAttacksCount:
    """_fallback_red_blue must count Landed Attacks, not just Disputed Risks.

    Rationale (spec 027 postmortem): a red-blue deliberation where the
    arbiter rules Red's attack landed and Blue could not defend it is a
    surviving unresolved risk — it must flow into
    genuine_disagreements_surviving. Previously only ``### Disputed Risks``
    was counted, producing false-PASS verdicts on deliberations that
    concluded with P0 required mitigations.
    """

    SYNTHESIS_WITH_LANDED = """# Synthesis: Red-Blue Risk Register

**Agents:** red-advocate, blue-advocate
**Deliberation mode:** red-blue
**Phases completed:** 4

## Process Summary

| Agents | 2 (red-advocate, blue-advocate) |
| Mode | red-blue |

### Landed Attacks — Unmitigated Risks

- **[RISK-001]: Constitutional violation on evidence-before-claims** (Severity: Critical)
  - Red's case: proposal claims parity without audit.
  - Blue's response: deferred to follow-up.
  - Arbiter's assessment: landed. Mitigation required.

- **[RISK-002]: Arbiter component contract undefined** (Severity: High)
  - Red's case: five callers depend on PASS/BLOCK.
  - Blue's response: insufficient.
  - Arbiter's assessment: landed.

### Mitigated Attacks — Risks Successfully Defended

- **[RISK-007]: Schema drift** (Severity: Medium)
  - Defense: schema pin validated.

### Accepted Risks

- **[RISK-009]: Cold-start latency** (Severity: Low)
  - Nature of risk: 1-3s per invocation.

### Disputed Risks

- **[RISK-011]: Semantics of synthesis wording**
  - Red's final: problematic.
  - Blue's final: acceptable.

### Verdict

Proceed with Conditions.
"""

    def test_fallback_counts_landed_attacks(self) -> None:
        result = parse_synthesis(
            self.SYNTHESIS_WITH_LANDED, mode="red-blue"
        )
        qi = result.quality_indicators
        # 2 landed + 1 disputed = 3 surviving disagreements
        assert qi.genuine_disagreements_surviving == 3, (
            f"Expected 3 (2 landed + 1 disputed), got "
            f"{qi.genuine_disagreements_surviving}"
        )

    def test_fallback_ignores_mitigated_and_accepted(self) -> None:
        # RISK-007 (Mitigated) and RISK-009 (Accepted) must NOT count
        result = parse_synthesis(
            self.SYNTHESIS_WITH_LANDED, mode="red-blue"
        )
        # Parse the disputes directly — with 2 landed + 1 disputed,
        # mitigated/accepted are excluded (would have been 5 otherwise).
        qi = result.quality_indicators
        assert qi.genuine_disagreements_surviving == 3

    def test_landed_only_still_counts(self) -> None:
        text = (
            "# Synthesis: only-landed\n"
            "**Deliberation mode:** red-blue\n"
            "**Phases completed:** 4\n\n"
            "### Landed Attacks — Unmitigated Risks\n\n"
            "- **[RISK-A]: Thing A** landed.\n"
            "- **[RISK-B]: Thing B** landed.\n"
            "- **[RISK-C]: Thing C** landed.\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.genuine_disagreements_surviving == 3

    def test_no_landed_no_disputed_is_zero(self) -> None:
        # Includes a Scorecard heading because the red-blue template mandates
        # one in every synthesis — without it, the tightened unparseable
        # guard would (correctly) refuse a fixture this minimal.
        text = (
            "# Synthesis: clean-proposal\n"
            "**Deliberation mode:** red-blue\n"
            "**Phases completed:** 4\n\n"
            "### Mitigated Attacks — Risks Successfully Defended\n\n"
            "- **[RISK-A]: All defended**.\n\n"
            "### Scorecard\n\n"
            "| Metric | Count |\n"
            "|--------|-------|\n"
            "| Landed (unmitigated) | 0 |\n"
            "| Disputed (unresolved) | 0 |\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.genuine_disagreements_surviving == 0


class TestUnparseableSynthesisGuard:
    """parse_synthesis must raise UnparseableSynthesisError on meta-prose.

    Rationale (spec 027 postmortem): when a tool-use agent returns a
    conversational receipt rather than the synthesis document itself, the
    text lacks every structural marker. Silently returning an all-zeros
    QualityIndicators looks identical to a legitimate clean-PASS to
    downstream gates, producing false-PASS verdicts. The guard surfaces
    this as an explicit error so callers can decide: BLOCK, retry, or
    escalate.
    """

    META_PROSE_FROM_027 = (
        "I've completed the comprehensive risk synthesis for the red-blue "
        "deliberation on spec 027. The analysis shows a significant evolution "
        "in the debate, with the Blue Team making three major concessions "
        "while the Red Team maintained all attacks.\n\n"
        "## Key Findings:\n\n"
        "**Critical Issues Identified:**\n"
        "- Constitutional violation (Evidence Before Claims)\n"
        "- Arbiter component crisis\n"
    )

    def test_meta_prose_raises(self) -> None:
        from linter.output_contract import UnparseableSynthesisError

        with pytest.raises(UnparseableSynthesisError) as exc_info:
            parse_synthesis(self.META_PROSE_FROM_027, mode="red-blue")
        assert "no recognizable structural markers" in str(exc_info.value)

    def test_well_formed_synthesis_does_not_raise(self) -> None:
        text = (
            "# Synthesis: well-formed\n"
            "**Deliberation mode:** red-blue\n"
            "**Phases completed:** 4\n\n"
            "## Process Summary\n\n"
            "| Agents | 2 (red-advocate, blue-advocate) |\n\n"
            "### Landed Attacks — Unmitigated Risks\n\n"
            "- **[RISK-A]: Thing** landed.\n"
        )
        # Must not raise — all three guard-relevant fields populate.
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.agent_count == 2

    def test_empty_text_raises_value_error_not_unparseable(self) -> None:
        # Empty text is the pre-existing ValueError path; guard should not
        # swallow it or upgrade it to UnparseableSynthesisError.
        with pytest.raises(ValueError) as exc_info:
            parse_synthesis("", mode="red-blue")
        assert "empty synthesis text" in str(exc_info.value)

    def test_cli_exits_three_on_meta_prose(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.md"
        bad.write_text(self.META_PROSE_FROM_027, encoding="utf-8")
        r = subprocess.run(
            [
                "uv", "run", "python3", "-m", "linter.output_contract",
                str(bad), "--mode", "red-blue",
            ],
            capture_output=True,
            text=True,
        )
        assert r.returncode == 3, (
            f"expected exit 3, got {r.returncode}: stdout={r.stdout} "
            f"stderr={r.stderr}"
        )
        err = json.loads(r.stderr)
        assert err["error"] == "unparseable_synthesis"

    def test_phase_keyword_prose_alone_raises(self) -> None:
        """Prose that narrates the 5 phases but has no structured sections
        must raise. This is the exact shape of the false-PASS bug — the old
        guard counted prose-keyword matches as phases_completed > 0 and
        silently returned all-zeros."""
        from linter.output_contract import UnparseableSynthesisError

        narrative = (
            "I ran the deliberation. We went through review, cross-review, "
            "revision, disputes, and synthesis. Red Team argued the "
            "proposal was unsafe. Blue Team defended it. In the end the "
            "teams reached consensus and I wrote the synthesis to disk.\n"
        )
        with pytest.raises(UnparseableSynthesisError):
            parse_synthesis(narrative, mode="red-blue")


class TestHeadingLevelDrift:
    """Parser must tolerate synthesizer heading-level drift (H1 vs H2 vs H3).

    Observed across real runs: LLM synthesizers inconsistently choose heading
    levels for section anchors like "Landed Attacks" and "Disputed Risks".
    The same deliberation produced H2 (##) on one run and H1 (#) on another.
    The parser must yield identical dispute counts regardless of level.
    """

    @staticmethod
    def _synthesis_at_level(hashes: str) -> str:
        return (
            "# Risk Register — Example\n\n"
            f"{hashes} Landed Attacks — Unmitigated Risks\n\n"
            f"{hashes}# [RISK-A]: Thing A\n"
            "- Red's case: landed.\n"
            "- Blue's response: insufficient.\n\n"
            f"{hashes}# [RISK-B]: Thing B\n"
            "- Red's case: landed.\n"
            "- Blue's response: insufficient.\n\n"
            f"{hashes} Mitigated Attacks — Risks Successfully Defended\n\n"
            f"{hashes}# [RISK-C]: Thing C\n"
            "- Defense held.\n\n"
            f"{hashes} Disputed Risks\n\n"
            f"{hashes}# [RISK-D]: Thing D\n"
            "- Red's final: problematic.\n"
            "- Blue's final: acceptable.\n"
        )

    def test_h1_sections_parse(self) -> None:
        text = self._synthesis_at_level("#")
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.genuine_disagreements_surviving == 3

    def test_h2_sections_parse(self) -> None:
        text = self._synthesis_at_level("##")
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.genuine_disagreements_surviving == 3

    def test_h3_sections_parse(self) -> None:
        text = self._synthesis_at_level("###")
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.genuine_disagreements_surviving == 3

    def test_h2_sections_match_spec_027_fixture_shape(self) -> None:
        """Spec 027's real synthesizer output uses H2 sections + H3 heading
        entries. This mirrors that exact shape and confirms it parses."""
        text = (
            "# Risk Register — Spec 027\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [CONSTITUTIONAL-01]: Evidence Before Claims Violation\n"
            "- Red's case: landed.\n\n"
            "### [ARBITER-02]: Arbiter Component Mismatch\n"
            "- Red's case: landed.\n\n"
            "## Disputed Risks\n\n"
            "### [FALLBACK-06]: Graceful Fallback Chain\n"
            "- Arbiter's ruling: Red wins.\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        # 2 landed + 1 disputed = 3
        assert result.quality_indicators.genuine_disagreements_surviving == 3


class TestScorecardFallback:
    """When prose sections are missing or malformed, the Scorecard table's
    Landed/Disputed row counts are the template-declared authoritative source
    of surviving-risk counts."""

    def test_scorecard_counts_used_when_sections_absent(self) -> None:
        text = (
            "# Risk Register — Scorecard-only\n\n"
            "## Deliberation Summary\n\n"
            "A full narrative summary appears here.\n\n"
            "## Scorecard\n\n"
            "| Metric | Count |\n"
            "|--------|-------|\n"
            "| Total threats identified | 8 |\n"
            "| Landed (unmitigated) | 5 |\n"
            "| Mitigated (defended) | 2 |\n"
            "| Disputed (unresolved) | 1 |\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        # Scorecard says 5 landed + 1 disputed = 6 surviving
        assert result.quality_indicators.genuine_disagreements_surviving == 6

    def test_scorecard_presence_alone_blocks_unparseable(self) -> None:
        """A synthesis with a Scorecard heading but zero-count rows is still
        structurally valid — it must not raise UnparseableSynthesisError."""
        text = (
            "# Risk Register — Clean\n\n"
            "## Deliberation Summary\n\n"
            "Narrative.\n\n"
            "## Scorecard\n\n"
            "| Metric | Count |\n"
            "|--------|-------|\n"
            "| Landed (unmitigated) | 0 |\n"
            "| Disputed (unresolved) | 0 |\n"
        )
        # Must not raise — Scorecard heading is structural evidence even at 0.
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.genuine_disagreements_surviving == 0

    def test_prose_sections_preferred_over_scorecard(self) -> None:
        """When both prose entries and a Scorecard are present, prose wins.
        (Prevents double-counting the same risks.)"""
        text = (
            "# Risk Register — Both\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: A\n"
            "- landed.\n\n"
            "### [RISK-B]: B\n"
            "- landed.\n\n"
            "## Scorecard\n\n"
            "| Landed (unmitigated) | 99 |\n"
            "| Disputed (unresolved) | 99 |\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        # Prose shows 2 entries; scorecard's 99s must NOT override.
        assert result.quality_indicators.genuine_disagreements_surviving == 2


class TestRiskIdDedup:
    """_fallback_red_blue must count each RISK-ID once even when the
    synthesizer re-lists a critical risk in both Landed and Disputed
    (template violation, but observed in real runs)."""

    def test_same_id_in_landed_and_disputed_counts_once(self) -> None:
        text = (
            "# Risk Register — Duplicate IDs\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: A (critical)\n"
            "- landed.\n\n"
            "### [RISK-B]: B\n"
            "- landed.\n\n"
            "### [RISK-C]: C\n"
            "- landed.\n\n"
            "## Disputed Risks\n\n"
            "### [RISK-A]: A (re-mentioned, template violation)\n"
            "- arbiter undecided.\n\n"
            "### [RISK-D]: D (genuinely disputed)\n"
            "- arbiter undecided.\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        # 3 landed + 1 new disputed (RISK-A dedup'd, RISK-D new) = 4
        assert result.quality_indicators.genuine_disagreements_surviving == 4

    def test_duplicates_within_landed_collapse(self) -> None:
        text = (
            "# Risk Register — Duplicates Inside Landed\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: first mention\n"
            "- landed.\n\n"
            "### [RISK-A]: second mention of same ID\n"
            "- landed.\n\n"
            "### [RISK-B]: B\n"
            "- landed.\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        # RISK-A once + RISK-B once = 2
        assert result.quality_indicators.genuine_disagreements_surviving == 2


class TestMetadataBlock:
    """Engine injects a ``<!-- CONVERSUS:METADATA ... -->`` block at the top
    of every synthesis. Parser must trust it over LLM prose so ``agent_count``
    and ``phases_completed`` stop reading zero just because the synthesizer
    failed to recite them."""

    METADATA_ONLY = (
        "<!-- CONVERSUS:METADATA\n"
        "agents: 2\n"
        "agent_names: blue-advocate, red-advocate\n"
        "mode: red-blue\n"
        "phases_completed: 6\n"
        "iterations: 1\n"
        "round: 1\n"
        "-->\n\n"
        "# Risk Register — Example\n\n"
        "## Landed Attacks — Unmitigated Risks\n\n"
        "### [RISK-A]: A\n"
        "- landed.\n"
    )

    def test_metadata_supplies_agent_count(self) -> None:
        result = parse_synthesis(self.METADATA_ONLY, mode="red-blue")
        assert result.quality_indicators.agent_count == 2

    def test_metadata_supplies_phases_completed(self) -> None:
        result = parse_synthesis(self.METADATA_ONLY, mode="red-blue")
        # Authoritative 6 (deliberation + arbitration), not a prose inference.
        assert result.quality_indicators.phases_completed == 6

    def test_metadata_supplies_mode(self) -> None:
        result = parse_synthesis(self.METADATA_ONLY, mode="cooperative")
        # Metadata says red-blue; caller default must be overridden.
        assert result.quality_indicators.mode == "red-blue"

    def test_metadata_overrides_prose_values(self) -> None:
        """When both metadata and prose headers are present, metadata wins —
        the engine is authoritative about its own run state."""
        text = (
            "<!-- CONVERSUS:METADATA\n"
            "agents: 3\n"
            "agent_names: a, b, c\n"
            "mode: red-blue\n"
            "phases_completed: 6\n"
            "iterations: 2\n"
            "-->\n\n"
            "# Synthesis\n\n"
            "**Agents:** only-one-agent\n"
            "**Phases completed:** 1\n\n"
            "## Process Summary\n\n"
            "| Agents | 99 (bogus) |\n\n"
            "## Scorecard\n\n"
            "| Landed (unmitigated) | 0 |\n"
        )
        result = parse_synthesis(text, mode="cooperative")
        assert result.quality_indicators.agent_count == 3
        assert result.quality_indicators.phases_completed == 6
        assert result.quality_indicators.mode == "red-blue"

    def test_missing_metadata_falls_back_to_prose(self) -> None:
        """Fixtures from before metadata injection (no block) must still
        parse using the prose-header fallbacks."""
        text = (
            "# Synthesis: legacy\n"
            "**Agents:** pragmatist, devils-advocate\n"
            "**Deliberation mode:** cooperative\n"
            "**Phases completed:** 4\n\n"
            "### Convergence Achieved\n\n"
            "1. **Converged.**\n"
        )
        result = parse_synthesis(text, mode="cooperative")
        assert result.quality_indicators.agent_count == 2
        assert result.quality_indicators.mode == "cooperative"

    def test_risk_register_prose_fallback_counts_agents(self) -> None:
        """Legacy red-blue Risk Register fixtures (pre-metadata-block) must
        still extract agent_count from the canonical prose introduction
        pattern: ``(blue-advocate)`` / ``(red-advocate)``."""
        text = (
            "# Red-Blue Synthesis — example\n\n"
            "## Deliberation Summary\n\n"
            "The Blue Team (blue-advocate) argued for the proposal. "
            "The Red Team (red-advocate) challenged it. (blue-advocate) "
            "and (red-advocate) each revised their positions.\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: A\n"
            "- landed.\n\n"
            "## Scorecard\n\n"
            "| Landed (unmitigated) | 1 |\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        # Two distinct agent identifiers, deduped despite multiple mentions.
        assert result.quality_indicators.agent_count == 2

    def test_risk_register_prose_ignores_non_agent_parens(self) -> None:
        """Parenthetical noise like ``(OQ-9)``, ``(M011/M013/M014)``, and
        ``(e.g., partially)`` must not be mistaken for agent names."""
        text = (
            "# Red-Blue Synthesis\n\n"
            "## Deliberation Summary\n\n"
            "Red pointed to smoke findings (OQ-9) through (OQ-15), affecting "
            "M011/M013/M014 consumers. (e.g., mock providers).\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: A\n"
            "- landed.\n\n"
            "## Scorecard\n\n"
            "| Landed (unmitigated) | 1 |\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.agent_count == 0

    def test_scorecard_heading_alone_supplies_phases_completed(self) -> None:
        """Legacy Risk Register without **Phases completed:** header must
        still report phases_completed == 5 — a Scorecard section only
        appears at the end of a completed phase-5 synthesis."""
        text = (
            "# Red-Blue Synthesis\n\n"
            "## Deliberation Summary\n\n"
            "Body paragraph.\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: A\n"
            "- landed.\n\n"
            "## Scorecard\n\n"
            "| Landed (unmitigated) | 1 |\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.phases_completed == 5

    def test_verdict_leader_becomes_headline(self) -> None:
        """Red-blue synthesis headline falls through to the Verdict
        section's first bold recommendation."""
        text = (
            "# Red-Blue Synthesis\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: A\n"
            "- landed.\n\n"
            "## Scorecard\n\n"
            "| Landed (unmitigated) | 1 |\n\n"
            "## Verdict\n\n"
            "**Do not proceed** in the current form. The critical issues…\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        assert result.headline == "Do not proceed"

    def test_top_title_becomes_headline_when_no_verdict(self) -> None:
        """Final fallback: if no Convergence / Spec Changes / Verdict /
        Synthesis-title matches, the top-level ``# ...`` title wins."""
        text = (
            "# Custom Risk Register Title\n\n"
            "## Landed Attacks — Unmitigated Risks\n\n"
            "### [RISK-A]: A\n"
            "- landed.\n\n"
            "## Scorecard\n\n"
            "| Landed (unmitigated) | 1 |\n"
        )
        result = parse_synthesis(text, mode="red-blue")
        assert result.headline == "Custom Risk Register Title"

    def test_metadata_block_alone_is_structural_evidence(self) -> None:
        """A metadata block means the engine wrote the file — the guard
        must not fire even if the synthesizer returned no prose content.
        (This is the engine's own receipt of a run; prose absence is a
        different failure to diagnose elsewhere.)"""
        text = (
            "<!-- CONVERSUS:METADATA\n"
            "agents: 2\n"
            "agent_names: a, b\n"
            "mode: red-blue\n"
            "phases_completed: 5\n"
            "iterations: 1\n"
            "-->\n\n"
            "(synthesizer returned empty body)\n"
        )
        # Must not raise — agent_count from metadata is structural evidence.
        result = parse_synthesis(text, mode="red-blue")
        assert result.quality_indicators.agent_count == 2


# ---------------------------------------------------------------------------
# Cross-mode coverage — Tier 2 Principle V (Observable Deliberation)
# ---------------------------------------------------------------------------
#
# The conversus suite ships 8 deliberation modes (see ``templates/`` and the
# CONFORMANCE.md Tier 2 declaration). ``linter/output_contract.py`` was
# originally written when only ``cooperative`` mode existed. Principle V
# requires every deliberation phase to emit observable output that downstream
# tooling can validate against the canonical contract — and that the linter
# enforcing the contract MUST be verified across every mode the suite
# supports.
#
# These parametrized tests are the cross-mode coverage gate. They:
#   1. Exercise ``parse_synthesis`` against a representative synthesis-output
#      fixture for each of the 8 modes.
#   2. Assert the mode-agnostic guarantees (the metadata block + structural
#      evidence path) hold for every mode.
#   3. Assert dispute-counting for modes where it works today, and pin
#      ``xfail`` the modes where it is genuinely broken so the gap is visible
#      as failing-but-expected coverage rather than silent absence.
#
# Follow-on (see PR body for details): 6 of 8 modes have a genuine bug in the
# marker-tier dispute parser — ``_parse_marker_disputes`` only recognizes the
# literal ``**Dispute:`` entry keyword, so modes whose templates use mode-
# specific keywords inside the ``DISPUTES_BEGIN/END`` block
# (``**Disputed:``, ``**Vulnerability:``, ``**Term:``, ``**Contested:``, plus
# the heading-style entries used by ``red-blue`` and ``prisoners-dilemma``)
# fall through to ``return _empty`` instead of dispatching to the fallback
# parser. The fix belongs in ``linter/quality.py`` and is tracked separately.
# These tests document the gap.

ALL_MODES = [
    "cooperative",
    "red-blue",
    "winner-take-all",
    "prisoners-dilemma",
    "fair-division",
    "mechanism-design",
    "negotiation",
    "resource-allocation",
]


def _metadata_only_synthesis(mode: str) -> str:
    """Engine-injected metadata block + minimal title. The metadata block alone
    is structural evidence (see :class:`TestMetadataBlock`) and the parser must
    accept it for every mode."""
    return (
        "<!-- CONVERSUS:METADATA\n"
        "agents: 2\n"
        "agent_names: a, b\n"
        f"mode: {mode}\n"
        "phases_completed: 5\n"
        "iterations: 1\n"
        "-->\n\n"
        f"# Synthesis: Cross-mode coverage probe — {mode}\n\n"
        "Body content.\n"
    )


# Mode → DISPUTES_BEGIN/END inner body, modelled directly on the
# ``templates/<mode>/synthesis.md`` "For each:" entry shape. Each fixture
# contains exactly 2 dispute entries so a working parser must yield 2.
#
# Note on fixture style: templates show entries as list items (``- **Dispute:
# [Label]**``), but real synthesizer outputs frequently drop the list dash
# (compare ``conversus/quality_floor/reference-outputs/passing/monorepo-vs-
# polyrepo/summary/final.md`` — entries are flush-left ``**Dispute: ...**``).
# These fixtures use the flush-left form to mirror what reference outputs
# actually look like; the marker-tier regex anchors to ``(?:^|\n)\s*`` so
# both forms should ultimately be supported by a correct parser.
_MODE_DISPUTE_BODIES: dict[str, str] = {
    "cooperative": (
        "### Remaining Disputes\n\n"
        "**Dispute: Item A**\n"
        "- Positions: X vs Y.\n\n"
        "**Dispute: Item B**\n"
        "- Positions: X vs Y.\n"
    ),
    "winner-take-all": (
        "### Remaining Disputes\n\n"
        "**Dispute: tie on criterion A**\n"
        "- text\n\n"
        "**Dispute: tie on criterion B**\n"
        "- text\n"
    ),
    "red-blue": (
        "### Disputed Risks\n\n"
        "**[RISK-A]: First risk**\n"
        "- text\n\n"
        "**[RISK-B]: Second risk**\n"
        "- text\n"
    ),
    "prisoners-dilemma": (
        "## Disputed Boundaries\n\n"
        "### [Capability-A]\n\n"
        "- text\n\n"
        "### [Capability-B]\n\n"
        "- text\n"
    ),
    "fair-division": (
        "### Disputed Valuations\n\n"
        "**Disputed: Item-A**\n"
        "- Valuations: A=100 vs B=50.\n\n"
        "**Disputed: Item-B**\n"
        "- Valuations: A=30 vs B=80.\n"
    ),
    "mechanism-design": (
        "### Mechanism Vulnerabilities\n\n"
        "**Vulnerability: V-A**\n"
        "- text\n\n"
        "**Vulnerability: V-B**\n"
        "- text\n"
    ),
    "negotiation": (
        "### Unresolved Terms\n\n"
        "**Term: T-A**\n"
        "- text\n\n"
        "**Term: T-B**\n"
        "- text\n"
    ),
    "resource-allocation": (
        "### Contested Allocations\n\n"
        "**Contested: R-A**\n"
        "- text\n\n"
        "**Contested: R-B**\n"
        "- text\n"
    ),
}


def _synthesis_with_disputes(mode: str) -> str:
    """A realistic synthesis: metadata block + title + Process Summary table +
    a DISPUTES_BEGIN/END section whose inner body matches the mode's
    ``templates/<mode>/synthesis.md`` "For each:" entry shape exactly."""
    return (
        "<!-- CONVERSUS:METADATA\n"
        "agents: 2\n"
        "agent_names: a, b\n"
        f"mode: {mode}\n"
        "phases_completed: 5\n"
        "iterations: 1\n"
        "-->\n\n"
        f"# Synthesis: Cross-mode dispute probe — {mode}\n\n"
        "## Process Summary\n\n"
        "| Agents | 2 (a, b) |\n\n"
        "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
        + _MODE_DISPUTE_BODIES[mode]
        + "<!-- CONVERSUS:DISPUTES_END -->\n"
    )


# Modes whose dispute parser is genuinely broken today (see follow-on note
# above). When the fix lands, remove the relevant entries from this set and
# the corresponding xfail markers will start failing as XPASS, prompting
# removal of the strict-xfail annotation.
_DISPUTE_PARSER_BROKEN_MODES: set[str] = {
    "red-blue",
    "prisoners-dilemma",
    "fair-division",
    "mechanism-design",
    "negotiation",
    "resource-allocation",
}


class TestCrossModeMetadataCoverage:
    """Mode-agnostic guarantees: the metadata block is authoritative for every
    one of the 8 modes the suite supports. Failure of any parametrization
    means a regression in the metadata extraction path, not a per-mode bug."""

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_metadata_supplies_agent_count(self, mode: str) -> None:
        result = parse_synthesis(_metadata_only_synthesis(mode), mode=mode)
        assert result.quality_indicators.agent_count == 2

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_metadata_supplies_mode(self, mode: str) -> None:
        # Pass a deliberately wrong caller default to confirm metadata wins.
        result = parse_synthesis(
            _metadata_only_synthesis(mode), mode="cooperative"
        )
        assert result.quality_indicators.mode == mode

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_metadata_supplies_phases_completed(self, mode: str) -> None:
        result = parse_synthesis(_metadata_only_synthesis(mode), mode=mode)
        assert result.quality_indicators.phases_completed == 5

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_metadata_block_is_structural_evidence(self, mode: str) -> None:
        """A metadata block alone must be sufficient structural evidence to
        satisfy the unparseable-synthesis guard for every mode."""
        result = parse_synthesis(_metadata_only_synthesis(mode), mode=mode)
        # Reaching this line means the guard did not fire.
        assert result.full_analysis  # non-empty

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_output_serializes_to_valid_json(self, mode: str) -> None:
        """``model_dump_json()`` must produce valid, parseable JSON containing
        the canonical contract fields for every mode."""
        result = parse_synthesis(_metadata_only_synthesis(mode), mode=mode)
        parsed = json.loads(result.model_dump_json())
        for field in (
            "headline",
            "summary",
            "full_analysis",
            "quality_indicators",
            "debate_transcript",
        ):
            assert field in parsed, f"missing field {field} for mode={mode}"
        assert parsed["quality_indicators"]["mode"] == mode


class TestCrossModeDisputeCoverage:
    """Per-mode dispute parsing across all 8 modes.

    For each mode we synthesize a realistic DISPUTES_BEGIN/END block whose
    inner entries match the mode's template shape exactly, then assert the
    parser returns ``surviving == 2``. Modes whose parser is genuinely
    broken today are marked ``strict xfail`` so:
      - the gap is visible as failing-but-expected coverage (not silent
        absence);
      - fixing the parser will flip them to XPASS and force a follow-up
        commit to drop the xfail marker.
    """

    @pytest.mark.parametrize(
        "mode",
        [
            pytest.param(
                m,
                marks=pytest.mark.xfail(
                    strict=True,
                    reason=(
                        "Output-contract follow-on: marker-tier "
                        "_parse_marker_disputes only matches `**Dispute:`; "
                        "mode-specific entry keywords short-circuit to "
                        "return _empty before the fallback dispatch runs."
                    ),
                ),
            )
            if m in _DISPUTE_PARSER_BROKEN_MODES
            else m
            for m in ALL_MODES
        ],
    )
    def test_dispute_block_yields_two_surviving(self, mode: str) -> None:
        result = parse_synthesis(_synthesis_with_disputes(mode), mode=mode)
        qi = result.quality_indicators
        assert qi.genuine_disagreements_surviving == 2, (
            f"mode={mode}: expected 2 surviving disputes from the "
            f"template-shaped fixture, got "
            f"{qi.genuine_disagreements_surviving}"
        )

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_dispute_fixture_parses_without_raising(self, mode: str) -> None:
        """Independent of dispute-count correctness: the fixture must parse
        for every mode — the structural-evidence guard must not fire on a
        well-formed metadata block + DISPUTES_BEGIN/END section."""
        # Must not raise UnparseableSynthesisError or ValueError.
        result = parse_synthesis(_synthesis_with_disputes(mode), mode=mode)
        assert result.quality_indicators.mode == mode
