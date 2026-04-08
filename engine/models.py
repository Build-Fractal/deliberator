"""Structured deliberation result models.

Pydantic models for per-agent, per-phase, and whole-deliberation
results.  ``StructuredDeliberation`` is the primary data model
returned by the FastAPI handler after a deliberation completes.
"""

from __future__ import annotations

from pydantic import BaseModel

from engine.events import (
    AgentCompleted,
    EngineEvent,
    PhaseCompleted,
)
from linter.output_contract import parse_synthesis


# ---------------------------------------------------------------------------
# Component models
# ---------------------------------------------------------------------------


class AgentReview(BaseModel):
    """A single agent's contribution in a specific phase."""

    model_config = {"frozen": True}

    agent_name: str
    phase: str
    content: str
    duration_ms: int


class PhaseResult(BaseModel):
    """Aggregate stats for a completed pipeline phase."""

    model_config = {"frozen": True}

    phase: str
    duration_ms: int
    agent_count: int
    success_count: int


# ---------------------------------------------------------------------------
# Top-level result model
# ---------------------------------------------------------------------------


class StructuredDeliberation(BaseModel):
    """Complete structured output from a deliberation run.

    This is the canonical result model that the FastAPI endpoint
    serialises into the final SSE event and persists to Supabase.
    """

    model_config = {"frozen": True}

    question: str
    mode: str
    provider: str
    agent_reviews: list[AgentReview]
    phase_results: list[PhaseResult]
    disputes: list[str]
    convergence_points: list[str]
    synthesis_text: str
    headline: str
    summary: str
    executive_summary: str = ""
    total_duration_ms: int
    rounds_completed: int
    termination_reason: str | None = None

    @classmethod
    def from_events(
        cls,
        events: list[EngineEvent],
        synthesis_text: str,
        question: str,
        mode: str,
        provider: str,
    ) -> StructuredDeliberation:
        """Reconstruct a ``StructuredDeliberation`` from captured engine events.

        This is the primary construction path for the FastAPI handler.
        Agent reviews are assembled from ``AgentCompleted`` events that
        carry ``response_text``; phase stats come from ``PhaseCompleted``
        events; headline/summary/disputes/convergence come from parsing
        the synthesis text through the output contract parser.

        Args:
            events: Captured ``EngineEvent`` list from a pipeline run.
            synthesis_text: The raw synthesis markdown produced by the
                synthesizer agent.
            question: The original question being deliberated.
            mode: The deliberation mode (e.g. ``"cooperative"``).
            provider: The provider name used (e.g. ``"mock"``).

        Returns:
            A fully-populated ``StructuredDeliberation``.
        """
        # -- Agent reviews from AgentCompleted events with response_text --
        agent_reviews: list[AgentReview] = []
        for ev in events:
            if isinstance(ev, AgentCompleted) and ev.response_text:
                agent_reviews.append(
                    AgentReview(
                        agent_name=ev.agent_name,
                        phase=ev.phase,
                        content=ev.response_text,
                        duration_ms=ev.duration_ms,
                    )
                )

        # -- Phase results from PhaseCompleted events --
        phase_results: list[PhaseResult] = []
        for ev in events:
            if isinstance(ev, PhaseCompleted):
                phase_results.append(
                    PhaseResult(
                        phase=ev.phase,
                        duration_ms=ev.duration_ms,
                        agent_count=ev.agent_count,
                        success_count=ev.success_count,
                    )
                )

        # -- Total duration: sum of all phase durations --
        total_duration_ms = sum(pr.duration_ms for pr in phase_results)

        # -- Rounds completed: count distinct 'review' PhaseCompleted events --
        rounds_completed = sum(
            1 for pr in phase_results if pr.phase == "review"
        )
        if rounds_completed == 0:
            rounds_completed = 1

        # -- Parse synthesis for headline, summary, disputes, convergence --
        disputes: list[str] = []
        convergence_points: list[str] = []
        headline = ""
        summary = ""

        # Derive real agent count from events (not synthesis text parsing)
        unique_agents = {
            ev.agent_name
            for ev in events
            if isinstance(ev, AgentCompleted)
        }
        agent_count = len(unique_agents)

        if synthesis_text.strip():
            try:
                parsed = parse_synthesis(synthesis_text, mode=mode)
                headline = parsed.headline
                summary = parsed.summary
            except (ValueError, Exception):
                # Synthesis parsing is best-effort; fall back to defaults
                headline = ""
                summary = ""

            # Extract disputes and convergence from synthesis markdown
            import re

            # Disputes: match a wide range of heading patterns that LLMs use
            # for dispute/contradiction/tension sections across all modes.
            # Cooperative: "Remaining Disputes", "Dangerous Contradictions Found"
            # Red-blue: "Disputed Risks"
            # Prisoners-dilemma: "Disputed Boundaries"
            # Winner-take-all: "Remaining Disputes"
            # Free-form: "Key Disputes", "Unresolved Issues", "Points of Disagreement", etc.
            dispute_section = re.search(
                r"###?\s*(?:"
                r"(?:Remaining|Key|Open|Unresolved|Outstanding)\s+Disputes?"
                r"|Dangerous\s+Contradictions\s+Found"
                r"|Disputed\s+(?:Risks|Boundaries|Areas|Points)"
                r"|(?:Unresolved|Remaining)\s+(?:Tensions?|Disagreements?|Issues?|Contradictions?)"
                r"|Points?\s+of\s+Disagreement"
                r"|Areas?\s+of\s+(?:Disagreement|Contention|Conflict)"
                r")\s*\n(.*?)(?=\n#{2,4}\s|\Z)",
                synthesis_text,
                re.DOTALL,
            )
            if dispute_section:
                for line in dispute_section.group(1).strip().splitlines():
                    stripped = line.strip()
                    if stripped and re.match(r"^\d+\.", stripped):
                        disputes.append(re.sub(r"^\d+\.\s*", "", stripped))
                    elif stripped.startswith("- **") or stripped.startswith("- "):
                        # Also match bullet-style disputes
                        cleaned = re.sub(r"^-\s*\*?\*?", "", stripped).strip().rstrip("*")
                        if cleaned:
                            disputes.append(cleaned)

            # Convergence: match heading patterns for agreement/convergence sections.
            # Cooperative: "Convergence Achieved"
            # Free-form: "Points of Agreement", "Areas of Consensus", "Common Ground", etc.
            convergence_section = re.search(
                r"###?\s*(?:"
                r"Convergence\s+(?:Achieved|Points?)"
                r"|(?:Points?|Areas?)\s+of\s+(?:Agreement|Convergence|Consensus|Alignment)"
                r"|Common\s+Ground"
                r"|(?:Shared|Agreed|Unanimous)\s+(?:Positions?|Conclusions?|Recommendations?)"
                r"|Key\s+(?:Agreements?|Convergences?)"
                r"|Consensus\s+(?:Points?|Areas?|Reached)"
                r")\s*\n(.*?)(?=\n#{2,4}\s|\Z)",
                synthesis_text,
                re.DOTALL,
            )
            if convergence_section:
                for line in convergence_section.group(1).strip().splitlines():
                    stripped = line.strip()
                    if stripped and re.match(r"^\d+\.", stripped):
                        convergence_points.append(
                            re.sub(r"^\d+\.\s*", "", stripped)
                        )
                    elif stripped.startswith("- **") or stripped.startswith("- "):
                        cleaned = re.sub(r"^-\s*\*?\*?", "", stripped).strip().rstrip("*")
                        if cleaned:
                            convergence_points.append(cleaned)

        # Always rebuild summary from real event data — the synthesis text
        # parser's agent count is unreliable for non-spec-review questions.
        summary = (
            f"{agent_count} agent{'s' if agent_count != 1 else ''} "
            f"in {mode} mode completed {len(phase_results)} "
            f"phase{'s' if len(phase_results) != 1 else ''}. "
            f"{len(convergence_points)} convergence "
            f"point{'s' if len(convergence_points) != 1 else ''}, "
            f"{len(disputes)} surviving "
            f"dispute{'s' if len(disputes) != 1 else ''}."
        )

        return cls(
            question=question,
            mode=mode,
            provider=provider,
            agent_reviews=agent_reviews,
            phase_results=phase_results,
            disputes=disputes,
            convergence_points=convergence_points,
            synthesis_text=synthesis_text,
            headline=headline,
            summary=summary,
            total_duration_ms=total_duration_ms,
            rounds_completed=rounds_completed,
        )
