"""
Test suite for the conversus quality gate checker (linter/quality.py).

Exercises both gates (substantive disagreement + agent attributions) against
all 3 S01 reference outputs with known expected results, plus edge cases.

NOTE: All quality gate tests use cooperative-mode output from a single 2-agent
pair (pragmatist + devils-advocate). Additional fixtures for 3-agent configs
and non-cooperative modes should be added before M002 engine extraction.
"""

from pathlib import Path

import pytest

try:
    from .quality import (
        AttributionResult,
        DisagreementResult,
        DisputeInfo,
        QualityResult,
        check_attributions,
        check_disagreement,
        check_quality_floor,
        check_quality_floor_file,
    )
except ImportError:
    from quality import (
        AttributionResult,
        DisagreementResult,
        DisputeInfo,
        QualityResult,
        check_attributions,
        check_disagreement,
        check_quality_floor,
        check_quality_floor_file,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# Root of reference outputs relative to this file
_REF_ROOT: Path = Path(__file__).resolve().parent.parent / "conversus" / "quality_floor" / "reference-outputs"


@pytest.fixture(scope="session")
def ref_root() -> Path:
    """Return the reference-outputs directory path."""
    assert _REF_ROOT.is_dir(), f"Reference outputs not found at {_REF_ROOT}"
    return _REF_ROOT


def _load_ref(relative: str) -> str:
    """Load a reference output file by path relative to the reference-outputs dir."""
    path = _REF_ROOT / relative
    assert path.exists(), f"Reference file not found: {path}"
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def monorepo_text() -> str:
    return _load_ref("passing/monorepo-vs-polyrepo/summary/final.md")


@pytest.fixture(scope="session")
def lease_text() -> str:
    return _load_ref("passing/lease-vs-buy/summary/final.md")


@pytest.fixture(scope="session")
def factual_text() -> str:
    return _load_ref("failing/factual-capital/summary/final.md")


# ---------------------------------------------------------------------------
# TestDisagreementGate — Gate 1: Substantive Disagreement
# ---------------------------------------------------------------------------


class TestDisagreementGate:
    """Tests for check_disagreement()."""

    # --- Reference outputs ---

    def test_monorepo_passes_with_3_disputes(self, monorepo_text: str) -> None:
        result = check_disagreement(monorepo_text)
        assert result.passed is True
        assert result.dispute_count == 3

    def test_monorepo_dispute_labels(self, monorepo_text: str) -> None:
        result = check_disagreement(monorepo_text)
        labels = [d.label for d in result.disputes]
        assert "Deferral Timeline Shape" in labels
        assert "Shared Repo Necessity and Scope" in labels
        # Third label contains "Migration Estimation Gap" (may include parenthetical detail)
        assert any("Migration Estimation Gap" in lbl for lbl in labels)

    def test_monorepo_disputes_have_agents(self, monorepo_text: str) -> None:
        result = check_disagreement(monorepo_text)
        for dispute in result.disputes:
            assert len(dispute.agent_names) >= 2, (
                f"Dispute '{dispute.label}' has fewer than 2 agents: {dispute.agent_names}"
            )

    def test_lease_passes_with_4_disputes(self, lease_text: str) -> None:
        result = check_disagreement(lease_text)
        assert result.passed is True
        assert result.dispute_count == 4

    def test_lease_dispute_labels(self, lease_text: str) -> None:
        result = check_disagreement(lease_text)
        labels = [d.label for d in result.disputes]
        assert "Spec Directional Neutrality" in labels
        assert "Mileage Overage Visibility" in labels
        assert "Residual Value Stress-Testing Depth" in labels
        assert "Children as Planning-Horizon Risk Factor" in labels

    def test_lease_disputes_have_agents(self, lease_text: str) -> None:
        result = check_disagreement(lease_text)
        for dispute in result.disputes:
            assert len(dispute.agent_names) >= 2, (
                f"Dispute '{dispute.label}' has fewer than 2 agents: {dispute.agent_names}"
            )

    def test_factual_capital_fails_with_0_disputes(self, factual_text: str) -> None:
        result = check_disagreement(factual_text)
        assert result.passed is False
        assert result.dispute_count == 0
        assert result.disputes == []

    # --- Edge cases ---

    def test_empty_string(self) -> None:
        result = check_disagreement("")
        assert result.passed is False
        assert result.dispute_count == 0
        assert result.disputes == []

    def test_no_disputes_begin_marker(self) -> None:
        text = "# Synthesis\nSome text without any structural markers.\n"
        result = check_disagreement(text)
        assert result.passed is False
        assert result.dispute_count == 0

    def test_empty_block_between_markers(self) -> None:
        text = (
            "# Synthesis\n"
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
        )
        result = check_disagreement(text)
        assert result.passed is False
        assert result.dispute_count == 0

    def test_markers_with_only_none_negation(self) -> None:
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "### Remaining Disputes\n\n"
            "**None.**\n\n"
            "There are no remaining disputes.\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
        )
        result = check_disagreement(text)
        assert result.passed is False
        assert result.dispute_count == 0

    def test_markers_with_no_remaining_disputes(self) -> None:
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "### Remaining Disputes\n\n"
            "no remaining disputes\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
        )
        result = check_disagreement(text)
        assert result.passed is False
        assert result.dispute_count == 0

    def test_begin_marker_only_no_end(self) -> None:
        """BEGIN without END — should parse everything after BEGIN."""
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "**Dispute: Test Dispute**\n\n"
            "*Pragmatist:* Position A\n"
            "*Devil's Advocate:* Position B\n"
        )
        result = check_disagreement(text)
        assert result.passed is True
        assert result.dispute_count == 1
        assert result.disputes[0].label == "Test Dispute"

    def test_result_model_is_frozen(self) -> None:
        result = check_disagreement("")
        with pytest.raises(Exception):
            result.passed = True  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestInfluenceAwareDisputeCounting — spec 006 FR-P2-4 (FR-009 to FR-012)
#
# Accounting-only tests: exercise the influence + arbiter_addressed kwargs of
# check_disagreement directly. End-to-end pipeline tests for SC-002 (advisory
# leaves disputes counted across rounds) and SC-003 (recommended re-opens when
# the addressed party re-raises) require the resolution.md parser and live in
# the follow-up FR.
#
# TODO(spec-006-FR-P2-4-followup): once the resolution.md parser ships and
# populates `arbiter_addressed` from the prior round, add round-level tests for
# SC-002 (advisory) and SC-003 (recommended re-open) in
# engine/tests/test_006_inter_round_arbitration.py.
# ---------------------------------------------------------------------------


class TestInfluenceAwareDisputeCounting:
    """Tests for the influence + arbiter_addressed kwargs on check_disagreement."""

    # Three-dispute fixture — all three named "D1", "D2", "D3" inside their
    # labels so a substring match against ["D2"] removes exactly one.
    _THREE_DISPUTE_TEXT: str = (
        "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
        "**Dispute: D1 — first disagreement**\n\n"
        "*Pragmatist:* Position A\n"
        "*Devil's Advocate:* Position B\n\n"
        "**Dispute: D2 — second disagreement**\n\n"
        "*Pragmatist:* Position C\n"
        "*Devil's Advocate:* Position D\n\n"
        "**Dispute: D3 — third disagreement**\n\n"
        "*Pragmatist:* Position E\n"
        "*Devil's Advocate:* Position F\n"
        "<!-- CONVERSUS:DISPUTES_END -->\n"
    )

    def test_check_disagreement_binding_removes_addressed_disputes(self) -> None:
        """BINDING + arbiter_addressed=['D2'] removes exactly the matching dispute."""
        from linter.models import InfluenceLevel

        result = check_disagreement(
            self._THREE_DISPUTE_TEXT,
            influence=InfluenceLevel.BINDING,
            arbiter_addressed=["D2"],
        )
        assert result.passed is True
        assert result.dispute_count == 2
        labels = [d.label for d in result.disputes]
        assert not any("D2" in lbl for lbl in labels)
        assert any("D1" in lbl for lbl in labels)
        assert any("D3" in lbl for lbl in labels)

    def test_check_disagreement_recommended_removes_addressed_disputes(self) -> None:
        """RECOMMENDED also removes addressed disputes (caller handles re-open)."""
        from linter.models import InfluenceLevel

        result = check_disagreement(
            self._THREE_DISPUTE_TEXT,
            influence=InfluenceLevel.RECOMMENDED,
            arbiter_addressed=["D2"],
        )
        assert result.passed is True
        assert result.dispute_count == 2
        assert not any("D2" in d.label for d in result.disputes)

    def test_check_disagreement_advisory_leaves_disputes_counted(self) -> None:
        """ADVISORY: even with arbiter_addressed populated, no disputes removed."""
        from linter.models import InfluenceLevel

        result = check_disagreement(
            self._THREE_DISPUTE_TEXT,
            influence=InfluenceLevel.ADVISORY,
            arbiter_addressed=["D2"],
        )
        assert result.passed is True
        assert result.dispute_count == 3

    def test_check_disagreement_no_influence_backward_compat(self) -> None:
        """influence=None (default) preserves existing behavior exactly."""
        baseline = check_disagreement(self._THREE_DISPUTE_TEXT)
        with_kwargs = check_disagreement(
            self._THREE_DISPUTE_TEXT,
            influence=None,
            arbiter_addressed=None,
        )
        assert baseline.passed is with_kwargs.passed
        assert baseline.dispute_count == with_kwargs.dispute_count == 3
        assert [d.label for d in baseline.disputes] == [
            d.label for d in with_kwargs.disputes
        ]

    def test_check_disagreement_empty_arbiter_addressed(self) -> None:
        """BINDING + arbiter_addressed=None or [] → no removal (no info to act on)."""
        from linter.models import InfluenceLevel

        result_none = check_disagreement(
            self._THREE_DISPUTE_TEXT,
            influence=InfluenceLevel.BINDING,
            arbiter_addressed=None,
        )
        assert result_none.dispute_count == 3

        result_empty = check_disagreement(
            self._THREE_DISPUTE_TEXT,
            influence=InfluenceLevel.BINDING,
            arbiter_addressed=[],
        )
        assert result_empty.dispute_count == 3

    def test_check_disagreement_substring_matching_robust(self) -> None:
        """Substring matching tolerates whitespace, leading dashes, and case drift."""
        from linter.models import InfluenceLevel

        # Each addressed entry has different formatting but should still match.
        result = check_disagreement(
            self._THREE_DISPUTE_TEXT,
            influence=InfluenceLevel.BINDING,
            arbiter_addressed=[
                "  - d2 — second disagreement  ",  # leading dash + lowercase
            ],
        )
        assert result.dispute_count == 2
        assert not any("D2" in d.label for d in result.disputes)


# ---------------------------------------------------------------------------
# TestAttributionGate — Gate 2: Agent Attributions Present
# ---------------------------------------------------------------------------


class TestAttributionGate:
    """Tests for check_attributions()."""

    # --- Reference outputs ---

    def test_monorepo_passes(self, monorepo_text: str) -> None:
        result = check_attributions(monorepo_text)
        assert result.passed is True

    def test_monorepo_has_at_least_2_agents(self, monorepo_text: str) -> None:
        result = check_attributions(monorepo_text)
        assert len(result.agent_names) >= 2

    def test_monorepo_has_challenges(self, monorepo_text: str) -> None:
        result = check_attributions(monorepo_text)
        assert result.challenge_count >= 1

    def test_monorepo_has_concessions(self, monorepo_text: str) -> None:
        result = check_attributions(monorepo_text)
        assert result.concession_count >= 1

    def test_monorepo_has_phase_references(self, monorepo_text: str) -> None:
        result = check_attributions(monorepo_text)
        assert result.phase_reference_count >= 3

    def test_lease_passes(self, lease_text: str) -> None:
        result = check_attributions(lease_text)
        assert result.passed is True

    def test_lease_has_at_least_2_agents(self, lease_text: str) -> None:
        result = check_attributions(lease_text)
        assert len(result.agent_names) >= 2

    def test_lease_has_challenges(self, lease_text: str) -> None:
        result = check_attributions(lease_text)
        assert result.challenge_count >= 1

    def test_lease_has_concessions(self, lease_text: str) -> None:
        result = check_attributions(lease_text)
        assert result.concession_count >= 1

    def test_lease_has_phase_references(self, lease_text: str) -> None:
        result = check_attributions(lease_text)
        assert result.phase_reference_count >= 3

    def test_factual_capital_passes(self, factual_text: str) -> None:
        """Factual-capital attributions are present even though disagreement fails."""
        result = check_attributions(factual_text)
        assert result.passed is True

    def test_factual_capital_has_at_least_2_agents(self, factual_text: str) -> None:
        result = check_attributions(factual_text)
        assert len(result.agent_names) >= 2

    # --- Edge cases ---

    def test_empty_string(self) -> None:
        result = check_attributions("")
        assert result.passed is False
        assert result.agent_names == []
        assert result.challenge_count == 0
        assert result.concession_count == 0
        assert result.phase_reference_count == 0

    def test_no_scorecard(self) -> None:
        text = "# Synthesis\nSome text with no scorecard or agent attributions.\n"
        result = check_attributions(text)
        assert result.passed is False
        assert result.agent_names == []

    def test_single_agent_insufficient(self) -> None:
        """A single agent is not enough for the attribution gate (needs ≥2)."""
        text = (
            "| P-R1 | Pragmatist | Some recommendation | P1 | Active | — | Strong | Adopted |\n"
            "| P-R2 | Pragmatist | Another rec | P2 | Active | — | Strong | Adopted |\n"
        )
        result = check_attributions(text)
        # Only 1 distinct agent — should fail (need ≥2 agents AND challenge + concession)
        assert result.passed is False

    def test_result_model_is_frozen(self) -> None:
        result = check_attributions("")
        with pytest.raises(Exception):
            result.passed = True  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestQualityFloor — Combined gate
# ---------------------------------------------------------------------------


class TestQualityFloor:
    """Tests for check_quality_floor() and check_quality_floor_file()."""

    # --- Parametrized test across all 3 reference outputs ---

    @pytest.mark.parametrize(
        "ref_path,expected_passed",
        [
            ("passing/monorepo-vs-polyrepo/summary/final.md", True),
            ("passing/lease-vs-buy/summary/final.md", True),
            ("failing/factual-capital/summary/final.md", False),
        ],
        ids=["monorepo-pass", "lease-pass", "factual-fail"],
    )
    def test_quality_floor_expected_result(
        self, ref_path: str, expected_passed: bool
    ) -> None:
        text = _load_ref(ref_path)
        result = check_quality_floor(text)
        assert result.passed is expected_passed

    # --- Verify composed result logic ---

    @pytest.mark.parametrize(
        "ref_path",
        [
            "passing/monorepo-vs-polyrepo/summary/final.md",
            "passing/lease-vs-buy/summary/final.md",
            "failing/factual-capital/summary/final.md",
        ],
        ids=["monorepo", "lease", "factual"],
    )
    def test_passed_equals_both_gates(self, ref_path: str) -> None:
        """QualityResult.passed must equal (disagreement.passed AND attributions.passed)."""
        text = _load_ref(ref_path)
        result = check_quality_floor(text)
        assert result.passed == (
            result.disagreement.passed and result.attributions.passed
        )

    # --- Specific sub-gate values per reference ---

    def test_monorepo_sub_gates(self, monorepo_text: str) -> None:
        result = check_quality_floor(monorepo_text)
        assert result.disagreement.passed is True
        assert result.disagreement.dispute_count == 3
        assert result.attributions.passed is True

    def test_lease_sub_gates(self, lease_text: str) -> None:
        result = check_quality_floor(lease_text)
        assert result.disagreement.passed is True
        assert result.disagreement.dispute_count == 4
        assert result.attributions.passed is True

    def test_factual_sub_gates(self, factual_text: str) -> None:
        result = check_quality_floor(factual_text)
        assert result.disagreement.passed is False
        assert result.disagreement.dispute_count == 0
        assert result.attributions.passed is True

    # --- Convenience wrapper: check_quality_floor_file ---

    def test_file_wrapper_monorepo(self) -> None:
        path = _REF_ROOT / "passing/monorepo-vs-polyrepo/summary/final.md"
        result = check_quality_floor_file(path)
        assert result.passed is True
        assert result.disagreement.dispute_count == 3

    def test_file_wrapper_factual(self) -> None:
        path = _REF_ROOT / "failing/factual-capital/summary/final.md"
        result = check_quality_floor_file(path)
        assert result.passed is False

    def test_file_wrapper_nonexistent_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            check_quality_floor_file(Path("/nonexistent/path/file.md"))

    # --- Empty / edge cases ---

    def test_empty_string_fails(self) -> None:
        result = check_quality_floor("")
        assert result.passed is False
        assert result.disagreement.passed is False
        assert result.disagreement.dispute_count == 0
        assert result.attributions.passed is False

    def test_empty_string_structured_failure(self) -> None:
        """Empty input produces a full structured result, never crashes."""
        result = check_quality_floor("")
        # Every field must be populated with a zero/empty value
        assert isinstance(result, QualityResult)
        assert isinstance(result.disagreement, DisagreementResult)
        assert isinstance(result.attributions, AttributionResult)
        assert result.disagreement.disputes == []
        assert result.attributions.agent_names == []

    def test_result_model_is_frozen(self) -> None:
        result = check_quality_floor("")
        with pytest.raises(Exception):
            result.passed = True  # type: ignore[misc]


# ---------------------------------------------------------------------------
# TestModeSpecificDisagreement — Mode-specific dispute parsing
# ---------------------------------------------------------------------------


class TestModeSpecificDisagreement:
    """Tests for mode-specific dispute parsing in check_disagreement().

    Covers marker-based (mode-agnostic) and heading-based (mode-specific
    fallback) parsing for all 4 competition modes.
    """

    # --- Winner-Take-All: Marker-based ---

    def test_wta_marker_based_finds_disputes(self) -> None:
        """WTA with DISPUTES markers uses standard marker parsing."""
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "**Dispute: Benchmark Representativeness**\n\n"
            "*Agent-A:* Position A\n"
            "*Agent-B:* Position B\n\n"
            "**Dispute: Scope Creep**\n\n"
            "*Agent-A:* Position C\n"
            "*Agent-B:* Position D\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
        )
        result = check_disagreement(text, "winner-take-all")
        assert result.passed is True
        assert result.dispute_count == 2

    # --- Winner-Take-All: Heading-based fallback ---

    def test_wta_runner_up_heading_counts_as_dispute(self) -> None:
        """WTA without markers: ## Runner-Up heading counts as 1 dispute."""
        text = (
            "## Winner\n\nFastAPI selected.\n\n"
            "## Runner-Up\n\nExpress.js retained as fallback.\n"
        )
        result = check_disagreement(text, "winner-take-all")
        assert result.passed is True
        assert result.dispute_count == 1
        assert "Runner-Up" in result.disputes[0].label

    def test_wta_runner_up_plus_remaining_disputes(self) -> None:
        """WTA without markers: Runner-Up + Remaining Disputes = combined count."""
        text = (
            "## Winner\n\nFastAPI selected.\n\n"
            "## Runner-Up\n\nExpress.js retained as fallback.\n\n"
            "### Remaining Disputes\n\n"
            "**Dispute: Benchmark Validity**\n\n"
            "**Dispute: Migration Timeline**\n"
        )
        result = check_disagreement(text, "winner-take-all")
        assert result.passed is True
        assert result.dispute_count == 3  # 1 runner-up + 2 remaining disputes

    def test_wta_no_runner_up_no_disputes(self) -> None:
        """WTA without markers and without Runner-Up or Remaining Disputes headings."""
        text = "## Winner\n\nFastAPI selected unanimously.\n"
        result = check_disagreement(text, "winner-take-all")
        assert result.passed is False
        assert result.dispute_count == 0

    # --- Red-Blue: Marker-based ---

    def test_red_blue_marker_based_finds_disputes(self) -> None:
        """Red-blue with DISPUTES markers uses standard marker parsing."""
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "**Dispute: RISK-002 VPC Flow Log Gap**\n\n"
            "*Red-Team:* Position A\n"
            "*Blue-Team:* Position B\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
        )
        result = check_disagreement(text, "red-blue")
        assert result.passed is True
        assert result.dispute_count == 1

    # --- Red-Blue: Heading-based fallback ---

    def test_red_blue_heading_counts_risk_entries(self) -> None:
        """Red-blue without markers: counts **[RISK-ID] entries under ### Disputed Risks."""
        text = (
            "### Risk Register\n\nSome risks...\n\n"
            "### Disputed Risks\n\n"
            "**[RISK-002]: VPC Flow Log Gap**\n\n"
            "Details about this risk.\n\n"
            "**[RISK-003]: Key Rotation Gap**\n\n"
            "Details about this risk.\n\n"
            "## Next Section\n"
        )
        result = check_disagreement(text, "red-blue")
        assert result.passed is True
        assert result.dispute_count == 2
        assert "[RISK-002]" in result.disputes[0].label
        assert "[RISK-003]" in result.disputes[1].label

    def test_red_blue_no_disputed_risks_heading(self) -> None:
        """Red-blue without markers and without ### Disputed Risks heading."""
        text = "### Risk Register\n\nAll risks mitigated.\n"
        result = check_disagreement(text, "red-blue")
        assert result.passed is False
        assert result.dispute_count == 0

    def test_red_blue_empty_disputed_risks_section(self) -> None:
        """Red-blue with ### Disputed Risks heading but no entries beneath."""
        text = (
            "### Disputed Risks\n\n"
            "No risks remain disputed.\n\n"
            "## Next Section\n"
        )
        result = check_disagreement(text, "red-blue")
        assert result.passed is False
        assert result.dispute_count == 0

    # --- Prisoner's Dilemma: Marker-based ---

    def test_pd_marker_based_finds_disputes(self) -> None:
        """PD with DISPUTES markers uses standard marker parsing."""
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "**Dispute: Alert Routing Ownership**\n\n"
            "*Platform-Advocate:* Position A\n"
            "*Product-Advocate:* Position B\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
        )
        result = check_disagreement(text, "prisoners-dilemma")
        assert result.passed is True
        assert result.dispute_count == 1

    # --- Prisoner's Dilemma: Heading-based fallback ---

    def test_pd_heading_counts_boundary_subheadings(self) -> None:
        """PD without markers: counts ### [ sub-headings under ## Disputed Boundaries."""
        text = (
            "## Converged Boundaries\n\nSome converged stuff.\n\n"
            "## Disputed Boundaries\n\n"
            "### [B4: Alert Routing Ownership]\n\n"
            "Details about B4.\n\n"
            "### [B5: Custom Metric Rate Limits]\n\n"
            "Details about B5.\n\n"
            "## Next Section\n"
        )
        result = check_disagreement(text, "prisoners-dilemma")
        assert result.passed is True
        assert result.dispute_count == 2
        assert "[B4: Alert Routing Ownership]" in result.disputes[0].label
        assert "[B5: Custom Metric Rate Limits]" in result.disputes[1].label

    def test_pd_no_disputed_boundaries_heading(self) -> None:
        """PD without markers and without ## Disputed Boundaries heading."""
        text = "## Responsibility Map\n\nAll boundaries converged.\n"
        result = check_disagreement(text, "prisoners-dilemma")
        assert result.passed is False
        assert result.dispute_count == 0

    def test_pd_empty_disputed_boundaries_section(self) -> None:
        """PD with ## Disputed Boundaries heading but no ### [ entries."""
        text = (
            "## Disputed Boundaries\n\n"
            "No boundaries remain disputed.\n\n"
            "## Next Section\n"
        )
        result = check_disagreement(text, "prisoners-dilemma")
        assert result.passed is False
        assert result.dispute_count == 0

    # --- Cooperative: Existing marker path still works ---

    def test_cooperative_marker_based_unchanged(self) -> None:
        """Cooperative marker-based parsing still works as before."""
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "**Dispute: Timeline Shape**\n\n"
            "*Pragmatist:* Position A\n"
            "*Devil's Advocate:* Position B\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
        )
        result = check_disagreement(text, "cooperative")
        assert result.passed is True
        assert result.dispute_count == 1

    def test_cooperative_heading_fallback(self) -> None:
        """Cooperative without markers falls back to ### Remaining Disputes."""
        text = (
            "### Remaining Disputes\n\n"
            "**Dispute: Timeline Shape**\n\n"
            "**Dispute: Scope Creep**\n"
        )
        result = check_disagreement(text, "cooperative")
        assert result.passed is True
        assert result.dispute_count == 2

    # --- Edge cases ---

    def test_empty_text_all_modes(self) -> None:
        """Empty text returns zero disputes for all modes."""
        for mode in ("cooperative", "winner-take-all", "red-blue", "prisoners-dilemma"):
            result = check_disagreement("", mode)
            assert result.passed is False, f"Expected False for mode={mode}"
            assert result.dispute_count == 0, f"Expected 0 disputes for mode={mode}"

    def test_no_markers_no_headings_all_modes(self) -> None:
        """Text with no markers and no mode-specific headings returns zero disputes."""
        text = "# Some Synthesis\n\nNothing relevant here.\n"
        for mode in ("cooperative", "winner-take-all", "red-blue", "prisoners-dilemma"):
            result = check_disagreement(text, mode)
            assert result.passed is False, f"Expected False for mode={mode}"
            assert result.dispute_count == 0, f"Expected 0 disputes for mode={mode}"

    def test_markers_present_heading_absent_uses_markers(self) -> None:
        """When markers are present, heading-based fallback is NOT used."""
        text = (
            "<!-- CONVERSUS:DISPUTES_BEGIN -->\n"
            "**Dispute: Marker Dispute**\n\n"
            "*Agent-A:* X\n"
            "*Agent-B:* Y\n"
            "<!-- CONVERSUS:DISPUTES_END -->\n"
            "### Disputed Risks\n\n"
            "**[RISK-001]: Should be ignored**\n"
        )
        result = check_disagreement(text, "red-blue")
        assert result.passed is True
        assert result.dispute_count == 1
        assert result.disputes[0].label == "Marker Dispute"

    def test_unknown_mode_returns_empty(self) -> None:
        """Unknown mode with no markers returns zero disputes."""
        text = "### Remaining Disputes\n\n**Dispute: Something**\n"
        result = check_disagreement(text, "unknown-mode")
        assert result.passed is False
        assert result.dispute_count == 0

    # --- Fixture file tests ---

    def test_wta_fixture_marker_parsing(self) -> None:
        """Load WTA fixture and verify marker-based parsing finds 2 disputes."""
        text = _load_ref("passing/winner-take-all-fixture/summary/final.md")
        result = check_disagreement(text, "winner-take-all")
        assert result.passed is True
        assert result.dispute_count == 2
        labels = [d.label for d in result.disputes]
        assert any("Benchmark" in lbl for lbl in labels)
        assert any("Sidecar" in lbl or "Scope" in lbl for lbl in labels)

    def test_wta_fixture_heading_fallback(self) -> None:
        """Load WTA fixture, strip markers, verify heading fallback."""
        text = _load_ref("passing/winner-take-all-fixture/summary/final.md")
        # Remove DISPUTES markers to force heading-based fallback
        text = text.replace("<!-- CONVERSUS:DISPUTES_BEGIN -->", "")
        text = text.replace("<!-- CONVERSUS:DISPUTES_END -->", "")
        result = check_disagreement(text, "winner-take-all")
        assert result.passed is True
        # Should find: 1 Runner-Up + 2 Remaining Disputes = 3
        assert result.dispute_count >= 1

    def test_red_blue_fixture_marker_parsing(self) -> None:
        """Load red-blue fixture and verify marker-based parsing."""
        text = _load_ref("passing/red-blue-fixture/summary/final.md")
        result = check_disagreement(text, "red-blue")
        assert result.passed is True
        assert result.dispute_count == 2

    def test_red_blue_fixture_heading_fallback(self) -> None:
        """Load red-blue fixture, strip markers, verify heading fallback."""
        text = _load_ref("passing/red-blue-fixture/summary/final.md")
        text = text.replace("<!-- CONVERSUS:DISPUTES_BEGIN -->", "")
        text = text.replace("<!-- CONVERSUS:DISPUTES_END -->", "")
        result = check_disagreement(text, "red-blue")
        assert result.passed is True
        assert result.dispute_count == 2
        labels = [d.label for d in result.disputes]
        assert any("RISK-002" in lbl for lbl in labels)
        assert any("RISK-003" in lbl for lbl in labels)

    def test_pd_fixture_marker_parsing(self) -> None:
        """Load PD fixture and verify marker-based parsing."""
        text = _load_ref("passing/prisoners-dilemma-fixture/summary/final.md")
        result = check_disagreement(text, "prisoners-dilemma")
        assert result.passed is True
        assert result.dispute_count == 2

    def test_pd_fixture_heading_fallback(self) -> None:
        """Load PD fixture, strip markers, verify heading fallback."""
        text = _load_ref("passing/prisoners-dilemma-fixture/summary/final.md")
        text = text.replace("<!-- CONVERSUS:DISPUTES_BEGIN -->", "")
        text = text.replace("<!-- CONVERSUS:DISPUTES_END -->", "")
        result = check_disagreement(text, "prisoners-dilemma")
        assert result.passed is True
        assert result.dispute_count == 2
        labels = [d.label for d in result.disputes]
        assert any("B4" in lbl for lbl in labels)
        assert any("B5" in lbl for lbl in labels)


# ---------------------------------------------------------------------------
# TestModels — Pydantic model structure
# ---------------------------------------------------------------------------


class TestModels:
    """Tests for Pydantic model structure and constraints."""

    def test_dispute_info_frozen(self) -> None:
        info = DisputeInfo(label="Test", agent_names=["A", "B"])
        with pytest.raises(Exception):
            info.label = "Changed"  # type: ignore[misc]

    def test_quality_result_type_hierarchy(self) -> None:
        result = check_quality_floor("")
        assert hasattr(result, "passed")
        assert hasattr(result, "disagreement")
        assert hasattr(result, "attributions")
        assert hasattr(result.disagreement, "dispute_count")
        assert hasattr(result.disagreement, "disputes")
        assert hasattr(result.attributions, "agent_names")
        assert hasattr(result.attributions, "challenge_count")
        assert hasattr(result.attributions, "concession_count")
        assert hasattr(result.attributions, "phase_reference_count")


# ---------------------------------------------------------------------------
# TestQualityCLI — CLI entry point via `python3 -m linter.quality`
# ---------------------------------------------------------------------------


class TestQualityCLI:
    """Tests for the __main__ CLI entry point."""

    @staticmethod
    def _run_cli(*args: str) -> "subprocess.CompletedProcess[str]":
        """Run the quality CLI and return the completed process."""
        import subprocess

        return subprocess.run(
            ["uv", "run", "python3", "-m", "linter.quality", *args],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_cli_passing_output(self) -> None:
        """Passing reference output → exit 0, JSON with passed=true."""
        import json

        proc = self._run_cli(
            str(_REF_ROOT / "passing" / "lease-vs-buy" / "summary" / "final.md")
        )
        assert proc.returncode == 0
        data = json.loads(proc.stdout)
        assert data["passed"] is True
        assert "disagreement" in data
        assert "attributions" in data

    def test_cli_failing_output(self) -> None:
        """Failing reference output → exit 1, JSON with passed=false."""
        import json

        proc = self._run_cli(
            str(_REF_ROOT / "failing" / "factual-capital" / "summary" / "final.md")
        )
        assert proc.returncode == 1
        data = json.loads(proc.stdout)
        assert data["passed"] is False
        assert data["disagreement"]["passed"] is False

    def test_cli_file_not_found(self) -> None:
        """Nonexistent path → exit 2, JSON error on stderr."""
        import json

        proc = self._run_cli("/nonexistent/path/file.md")
        assert proc.returncode == 2
        err = json.loads(proc.stderr)
        assert "error" in err
        assert "File not found" in err["error"]

    def test_cli_mode_flag(self) -> None:
        """Explicit --mode cooperative produces the same result as default."""
        import json

        proc_default = self._run_cli(
            str(_REF_ROOT / "passing" / "lease-vs-buy" / "summary" / "final.md")
        )
        proc_explicit = self._run_cli(
            str(_REF_ROOT / "passing" / "lease-vs-buy" / "summary" / "final.md"),
            "--mode", "cooperative",
        )
        assert proc_default.returncode == proc_explicit.returncode == 0
        assert json.loads(proc_default.stdout) == json.loads(proc_explicit.stdout)
