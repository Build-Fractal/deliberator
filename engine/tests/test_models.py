"""Tests for engine.models — structured deliberation result models."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from engine.events import (
    AgentCompleted,
    PhaseCompleted,
    PhaseStarted,
)
from engine.models import AgentReview, PhaseResult, StructuredDeliberation


# ---------------------------------------------------------------------------
# AgentReview
# ---------------------------------------------------------------------------


class TestAgentReview:
    """AgentReview construction and immutability."""

    def test_construction(self) -> None:
        review = AgentReview(
            agent_name="alice",
            phase="review",
            content="Good spec.",
            duration_ms=1500,
        )
        assert review.agent_name == "alice"
        assert review.phase == "review"
        assert review.content == "Good spec."
        assert review.duration_ms == 1500

    def test_frozen(self) -> None:
        review = AgentReview(
            agent_name="alice",
            phase="review",
            content="Looks fine.",
            duration_ms=100,
        )
        with pytest.raises(Exception):
            review.agent_name = "bob"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# PhaseResult
# ---------------------------------------------------------------------------


class TestPhaseResult:
    """PhaseResult construction and immutability."""

    def test_construction(self) -> None:
        result = PhaseResult(
            phase="review",
            duration_ms=3000,
            agent_count=2,
            success_count=2,
        )
        assert result.phase == "review"
        assert result.duration_ms == 3000
        assert result.agent_count == 2
        assert result.success_count == 2

    def test_frozen(self) -> None:
        result = PhaseResult(
            phase="review",
            duration_ms=3000,
            agent_count=2,
            success_count=2,
        )
        with pytest.raises(Exception):
            result.phase = "disputes"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# StructuredDeliberation
# ---------------------------------------------------------------------------


class TestStructuredDeliberation:
    """StructuredDeliberation construction and from_events classmethod."""

    def test_basic_construction(self) -> None:
        delib = StructuredDeliberation(
            question="Should we use Postgres?",
            mode="cooperative",
            provider="mock",
            agent_reviews=[],
            phase_results=[],
            disputes=[],
            convergence_points=[],
            synthesis_text="",
            headline="",
            summary="",
            total_duration_ms=0,
            rounds_completed=1,
        )
        assert delib.question == "Should we use Postgres?"
        assert delib.mode == "cooperative"
        assert delib.termination_reason is None

    def test_frozen(self) -> None:
        delib = StructuredDeliberation(
            question="Q?",
            mode="cooperative",
            provider="mock",
            agent_reviews=[],
            phase_results=[],
            disputes=[],
            convergence_points=[],
            synthesis_text="",
            headline="",
            summary="",
            total_duration_ms=0,
            rounds_completed=1,
        )
        with pytest.raises(Exception):
            delib.question = "New Q?"  # type: ignore[misc]

    def test_termination_reason_optional(self) -> None:
        delib = StructuredDeliberation(
            question="Q?",
            mode="cooperative",
            provider="mock",
            agent_reviews=[],
            phase_results=[],
            disputes=[],
            convergence_points=[],
            synthesis_text="",
            headline="",
            summary="",
            total_duration_ms=0,
            rounds_completed=1,
            termination_reason="converged",
        )
        assert delib.termination_reason == "converged"

    def test_from_events_with_realistic_sequence(self) -> None:
        """from_events populates reviews, phases, and metadata from engine events."""
        now = datetime.now(timezone.utc)
        events = [
            PhaseStarted(phase="review", agent_count=2, timestamp=now),
            AgentCompleted(
                phase="review",
                agent_name="alice",
                success=True,
                error=None,
                duration_ms=500,
                timestamp=now,
                response_text="Alice's review content.",
            ),
            AgentCompleted(
                phase="review",
                agent_name="bob",
                success=True,
                error=None,
                duration_ms=600,
                timestamp=now,
                response_text="Bob's review content.",
            ),
            PhaseCompleted(
                phase="review",
                agent_count=2,
                success_count=2,
                failure_count=0,
                duration_ms=700,
                timestamp=now,
            ),
            PhaseStarted(phase="synthesis", agent_count=1, timestamp=now),
            PhaseCompleted(
                phase="synthesis",
                agent_count=1,
                success_count=1,
                failure_count=0,
                duration_ms=300,
                timestamp=now,
            ),
        ]

        synthesis_text = "# Synthesis: Test\n\nSome synthesis content."

        result = StructuredDeliberation.from_events(
            events=events,
            synthesis_text=synthesis_text,
            question="Should we use Postgres?",
            mode="cooperative",
            provider="mock",
        )

        assert result.question == "Should we use Postgres?"
        assert result.mode == "cooperative"
        assert result.provider == "mock"
        assert len(result.agent_reviews) == 2
        assert result.agent_reviews[0].agent_name == "alice"
        assert result.agent_reviews[0].content == "Alice's review content."
        assert result.agent_reviews[1].agent_name == "bob"
        assert len(result.phase_results) == 2
        assert result.phase_results[0].phase == "review"
        assert result.phase_results[1].phase == "synthesis"
        assert result.total_duration_ms == 1000  # 700 + 300
        assert result.rounds_completed == 1
        assert result.synthesis_text == synthesis_text

    def test_from_events_skips_failed_agents(self) -> None:
        """from_events only includes agents with response_text (not failures)."""
        now = datetime.now(timezone.utc)
        events = [
            AgentCompleted(
                phase="review",
                agent_name="alice",
                success=True,
                error=None,
                duration_ms=500,
                timestamp=now,
                response_text="Alice's review.",
            ),
            AgentCompleted(
                phase="review",
                agent_name="bob",
                success=False,
                error="RuntimeError: failure",
                duration_ms=100,
                timestamp=now,
                response_text=None,
            ),
            PhaseCompleted(
                phase="review",
                agent_count=2,
                success_count=1,
                failure_count=1,
                duration_ms=600,
                timestamp=now,
            ),
        ]

        result = StructuredDeliberation.from_events(
            events=events,
            synthesis_text="# Synthesis: Test\n\nMinimal synthesis.",
            question="Q?",
            mode="cooperative",
            provider="mock",
        )

        assert len(result.agent_reviews) == 1
        assert result.agent_reviews[0].agent_name == "alice"

    def test_from_events_empty_synthesis(self) -> None:
        """from_events handles empty synthesis text gracefully."""
        result = StructuredDeliberation.from_events(
            events=[],
            synthesis_text="",
            question="Q?",
            mode="cooperative",
            provider="mock",
        )

        assert result.synthesis_text == ""
        assert result.headline == ""
        assert result.agent_reviews == []
        assert result.phase_results == []
        assert result.rounds_completed == 1

    def test_from_events_counts_rounds_from_review_phases(self) -> None:
        """rounds_completed counts the number of review PhaseCompleted events."""
        now = datetime.now(timezone.utc)
        events = [
            PhaseCompleted(
                phase="review", agent_count=2, success_count=2,
                failure_count=0, duration_ms=500, timestamp=now,
            ),
            PhaseCompleted(
                phase="cross-review", agent_count=2, success_count=2,
                failure_count=0, duration_ms=400, timestamp=now,
            ),
            PhaseCompleted(
                phase="review", agent_count=2, success_count=2,
                failure_count=0, duration_ms=600, timestamp=now,
            ),
            PhaseCompleted(
                phase="synthesis", agent_count=1, success_count=1,
                failure_count=0, duration_ms=300, timestamp=now,
            ),
        ]

        result = StructuredDeliberation.from_events(
            events=events,
            synthesis_text="# Synthesis: Test\n\nMulti-round.",
            question="Q?",
            mode="cooperative",
            provider="mock",
        )

        assert result.rounds_completed == 2

    def test_from_events_extracts_disputes_cooperative_headings(self) -> None:
        """Standard cooperative headings: 'Remaining Disputes' and 'Convergence Achieved'."""
        synthesis = (
            "### Remaining Disputes\n"
            "1. Performance vs maintainability trade-off\n"
            "2. Database choice remains contested\n"
            "\n"
            "### Convergence Achieved\n"
            "1. Both agents agree on TypeScript\n"
            "- **Microservices over monolith** — Strength: Unanimous\n"
        )
        result = StructuredDeliberation.from_events(
            events=[], synthesis_text=synthesis,
            question="Q?", mode="cooperative", provider="mock",
        )
        assert len(result.disputes) == 2
        assert "Performance vs maintainability trade-off" in result.disputes[0]
        assert len(result.convergence_points) == 2

    def test_from_events_extracts_dangerous_contradictions(self) -> None:
        """Cooperative template heading: 'Dangerous Contradictions Found'."""
        synthesis = (
            "### Dangerous Contradictions Found\n"
            "1. Agent A says scale up, Agent B says scale out\n"
            "\n### Next Section\n"
        )
        result = StructuredDeliberation.from_events(
            events=[], synthesis_text=synthesis,
            question="Q?", mode="cooperative", provider="mock",
        )
        assert len(result.disputes) == 1

    def test_from_events_extracts_disputed_risks_red_blue(self) -> None:
        """Red-blue template heading: 'Disputed Risks'."""
        synthesis = (
            "### Disputed Risks\n"
            "- **SQL injection surface** — Red claims unmitigated\n"
            "- **Rate limiting gaps** — Blue claims sufficient\n"
            "\n### Verdict\n"
        )
        result = StructuredDeliberation.from_events(
            events=[], synthesis_text=synthesis,
            question="Q?", mode="red-blue", provider="mock",
        )
        assert len(result.disputes) == 2

    def test_from_events_extracts_disputed_boundaries_prisoners(self) -> None:
        """Prisoners-dilemma template heading: 'Disputed Boundaries'."""
        synthesis = (
            "## Disputed Boundaries\n"
            "1. Auth module ownership unclear\n"
            "2. Logging responsibility overlap\n"
            "\n## Recommended Assignments\n"
        )
        result = StructuredDeliberation.from_events(
            events=[], synthesis_text=synthesis,
            question="Q?", mode="prisoners-dilemma", provider="mock",
        )
        assert len(result.disputes) == 2

    def test_from_events_extracts_freeform_dispute_headings(self) -> None:
        """LLMs sometimes use varied headings for free-form questions."""
        for heading in [
            "### Key Disputes",
            "### Unresolved Issues",
            "### Points of Disagreement",
            "### Areas of Disagreement",
            "### Open Disputes",
            "### Unresolved Tensions",
            "### Outstanding Disputes",
        ]:
            synthesis = (
                f"{heading}\n"
                "1. Whether to use React or Vue\n"
                "\n### Next Section\n"
            )
            result = StructuredDeliberation.from_events(
                events=[], synthesis_text=synthesis,
                question="Q?", mode="cooperative", provider="mock",
            )
            assert len(result.disputes) >= 1, f"Failed for heading: {heading}"

    def test_from_events_extracts_freeform_convergence_headings(self) -> None:
        """LLMs sometimes use varied headings for convergence sections."""
        for heading in [
            "### Points of Agreement",
            "### Areas of Consensus",
            "### Common Ground",
            "### Shared Conclusions",
            "### Key Agreements",
            "### Consensus Points",
            "### Convergence Points",
        ]:
            synthesis = (
                f"{heading}\n"
                "1. Both agents recommend TypeScript\n"
                "\n### Next Section\n"
            )
            result = StructuredDeliberation.from_events(
                events=[], synthesis_text=synthesis,
                question="Q?", mode="cooperative", provider="mock",
            )
            assert len(result.convergence_points) >= 1, f"Failed for heading: {heading}"
