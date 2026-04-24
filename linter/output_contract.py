"""
Canonical output contract for conversus deliberation results.

Defines Pydantic models for the structured output format that downstream
consumers (MCP server, CI, dashboards) use to read deliberation results.

Public API:
    parse_synthesis(text, mode) -> ConversusOutput

Models:
    QualityIndicators — structural facts about the deliberation process
    ConversusOutput — the canonical output: headline, summary, full analysis,
                      quality indicators, and debate transcript

The QualityIndicators model replaces a confidence float (per D004) with
verifiable structural facts: agent count, mode, phases completed,
cross-reviews performed, and disagreement counts.

Usage:
    from linter.output_contract import parse_synthesis

    result = parse_synthesis(synthesis_text, mode="cooperative")
    print(result.model_dump_json(indent=2))

CLI:
    python3 -m linter.output_contract <path> [--mode cooperative]
"""

from __future__ import annotations

import re

from pydantic import BaseModel

from linter.quality import check_disagreement


class UnparseableSynthesisError(ValueError):
    """Raised when synthesis text contains none of the expected structural markers.

    The linter defaults every :class:`QualityIndicators` field to 0 when its
    regex probes miss. That's indistinguishable from a legitimate
    "0 disputes, clean convergence" result — silent failure looks like a
    clean PASS to downstream gates.

    This error is raised when BOTH ``agent_count`` and ``phases_completed``
    extract to 0, which means every explicit structural probe missed and no
    phase keywords were found anywhere in the text. That's not a valid
    deliberation output — it's almost always meta-prose from a tool-use-capable
    agent that called Write and returned a chat-message receipt (see
    spec 027 postmortem).

    Callers can catch this to distinguish parse failure from convergence and
    choose to BLOCK/retry/escalate rather than treat as PASS.
    """


# ---------------------------------------------------------------------------
# Pydantic models — frozen per Constitution Principle IX
# ---------------------------------------------------------------------------


class QualityIndicators(BaseModel):
    """Structural facts about the deliberation process.

    Replaces a single confidence float with verifiable metrics extracted
    from the synthesis output. Every field is deterministically derivable
    from the synthesis text — no LLM judgment required.
    """

    model_config = {"frozen": True}

    agent_count: int
    mode: str
    phases_completed: int
    cross_reviews_performed: int
    genuine_disagreements_surfaced: int
    genuine_disagreements_surviving: int


class ConversusOutput(BaseModel):
    """Canonical output format for a conversus deliberation.

    This is the contract that downstream consumers import:
    - S05 MCP server returns this as its response schema
    - CI gates can inspect quality_indicators fields
    - Dashboards render headline + summary for quick review

    In M001, debate_transcript == full_analysis (same raw text).
    Future milestones may split these when transcript includes
    per-phase artifacts beyond the synthesis.
    """

    model_config = {"frozen": True}

    headline: str
    summary: str
    full_analysis: str
    quality_indicators: QualityIndicators
    debate_transcript: str


# ---------------------------------------------------------------------------
# Regex patterns for parsing synthesis output
# ---------------------------------------------------------------------------

# Engine-injected authoritative metadata block. Format (written verbatim by
# engine.phases._build_metadata_block):
#   <!-- CONVERSUS:METADATA
#   agents: 2
#   agent_names: blue-advocate, red-advocate
#   mode: red-blue
#   phases_completed: 5
#   iterations: 1
#   round: 1
#   -->
# When present, these fields are treated as the canonical source of truth —
# LLM prose heuristics are only consulted as a fallback for older fixtures
# written before the engine began injecting this block.
_METADATA_BLOCK: re.Pattern[str] = re.compile(
    r"<!--\s*CONVERSUS:METADATA\s*\n(.*?)\n\s*-->",
    re.DOTALL,
)
_METADATA_FIELD: re.Pattern[str] = re.compile(
    r"^(\w+)\s*:\s*(.+?)\s*$", re.MULTILINE
)

# Agent count — table format: | Agents | 2 (pragmatist, devils-advocate) |
_AGENTS_TABLE: re.Pattern[str] = re.compile(
    r"\|\s*Agents\s*\|\s*(\d+)", re.IGNORECASE
)

# Agent count — header format: **Agents:** Pragmatist, Devil's Advocate
_AGENTS_HEADER: re.Pattern[str] = re.compile(
    r"\*\*Agents:\*\*\s*(.+)", re.IGNORECASE
)

# Mode — **Deliberation mode:** Cooperative
_MODE_DELIB: re.Pattern[str] = re.compile(
    r"\*\*Deliberation mode:\*\*\s*(\S+)", re.IGNORECASE
)

# Mode — **Mode:** Cooperative
_MODE_SHORT: re.Pattern[str] = re.compile(
    r"\*\*Mode:\*\*\s*(\S+)", re.IGNORECASE
)

# Phases completed — **Phases completed:** 4
_PHASES_HEADER: re.Pattern[str] = re.compile(
    r"\*\*Phases completed:\*\*\s*(\d+)", re.IGNORECASE
)

# Convergence section — heading levels H1–H4 tolerated for synthesizer drift.
_CONVERGENCE_SECTION: re.Pattern[str] = re.compile(
    r"#{1,4}\s*Convergence Achieved.*?\n"
    r"(.*?)(?=\n#{1,4}\s|\n<!--\s*CONVERSUS|$)",
    re.DOTALL,
)

# Numbered bold items in convergence: "1. **Some headline text.**"
_CONVERGENCE_ITEM: re.Pattern[str] = re.compile(
    r"^\d+\.\s+\*\*(.+?)\*\*", re.MULTILINE
)

# Actionable Spec Changes section for fallback headline
_SPEC_CHANGES_SECTION: re.Pattern[str] = re.compile(
    r"#{1,4}\s*Actionable Spec Changes.*?\n(.*?)(?=\n#{1,4}\s|$)",
    re.DOTALL,
)

# Scorecard heading (red-blue) — presence alone is a strong structural signal.
_SCORECARD_HEADING: re.Pattern[str] = re.compile(
    r"^#{1,4}\s+Scorecard\s*$", re.MULTILINE | re.IGNORECASE
)

# P1 item in spec changes: "1. **Deploy Buf-based...**"
_P1_ITEM: re.Pattern[str] = re.compile(
    r"^\d+\.\s+\*\*(.+?)\*\*", re.MULTILINE
)

# Synthesis title line: # Synthesis: <title>
_SYNTHESIS_TITLE: re.Pattern[str] = re.compile(
    r"^#\s+Synthesis:\s*(.+)", re.MULTILINE
)


# ---------------------------------------------------------------------------
# Extraction helpers
# ---------------------------------------------------------------------------


def _extract_metadata(text: str) -> dict[str, str]:
    """Parse the engine-injected metadata block, if present.

    Returns a dict of field-name → raw-string-value. Empty dict when no
    block exists (older synthesis outputs, or a synthesis written before
    engine metadata injection was added).
    """
    block_match = _METADATA_BLOCK.search(text)
    if not block_match:
        return {}
    block = block_match.group(1)
    return {
        field.lower(): value.strip()
        for field, value in _METADATA_FIELD.findall(block)
    }


def _extract_agent_count(text: str) -> int:
    """Extract agent count.

    Priority order:
    1. Engine-injected metadata block's ``agents:`` field (authoritative).
    2. Process Summary table: ``| Agents | 2 (pragmatist, devils-advocate) |``.
    3. Header: ``**Agents:** Pragmatist, Devil's Advocate``.
    """
    meta = _extract_metadata(text)
    if "agents" in meta:
        try:
            return int(meta["agents"])
        except ValueError:
            pass
    # Fallback: agent_names line — count comma-separated entries.
    if "agent_names" in meta and meta["agent_names"]:
        return len([n for n in meta["agent_names"].split(",") if n.strip()])

    m = _AGENTS_TABLE.search(text)
    if m:
        return int(m.group(1))

    m = _AGENTS_HEADER.search(text)
    if m:
        names = [n.strip() for n in m.group(1).split(",") if n.strip()]
        return len(names)

    return 0


def _extract_mode(text: str, default: str) -> str:
    """Extract deliberation mode.

    Priority order:
    1. Engine-injected metadata block's ``mode:`` field (authoritative).
    2. ``**Deliberation mode:**`` prose header.
    3. ``**Mode:**`` prose header.
    4. Caller-supplied default.
    """
    meta = _extract_metadata(text)
    if "mode" in meta and meta["mode"]:
        return meta["mode"].lower()

    m = _MODE_DELIB.search(text)
    if m:
        return m.group(1).strip().lower()

    m = _MODE_SHORT.search(text)
    if m:
        return m.group(1).strip().lower()

    return default.lower()


def _extract_phases_completed(text: str) -> int:
    """Extract phases completed.

    Priority order:
    1. Engine-injected metadata block's ``phases_completed:`` field
       (authoritative — the engine knows this from its own run state).
    2. ``**Phases completed:**`` prose header.
    3. Keyword-match fallback on phase-related section names.
    """
    meta = _extract_metadata(text)
    if "phases_completed" in meta:
        try:
            return int(meta["phases_completed"])
        except ValueError:
            pass

    m = _PHASES_HEADER.search(text)
    if m:
        count = int(m.group(1))
        # The header says "4 (Review → Cross-Review → Revision → Disputes)"
        # but the synthesis itself is phase 5 — add 1 if the document is
        # a synthesis (which it always is when this parser runs on it)
        if _SYNTHESIS_TITLE.search(text):
            return count + 1
        return count

    # Infer from section structure: check for phase-related keywords
    phase_indicators = [
        (r"Phase\s*1|review", "review"),
        (r"cross.?review", "cross-review"),
        (r"Phase\s*3|revision", "revision"),
        (r"Phase\s*4|[Dd]isputes?\s", "disputes"),
        (r"Synthesis:", "synthesis"),
    ]
    found_phases: set[str] = set()
    for pattern, phase_name in phase_indicators:
        if re.search(pattern, text, re.IGNORECASE):
            found_phases.add(phase_name)

    return len(found_phases) if found_phases else 0


def _extract_cross_reviews_performed(text: str, agent_count: int) -> int:
    """Infer cross-review count from agent count.

    In cooperative mode, each agent cross-reviews every other agent's work
    per iteration. For 2 agents, that's 2 cross-reviews per iteration.
    """
    if agent_count < 2:
        return 0
    # Each agent reviews every other agent's work: agent_count * (agent_count - 1)
    # For 2 agents: 2 × 1 = 2, for 3 agents: 3 × 2 = 6, etc.
    return agent_count * (agent_count - 1)


def _extract_convergence_count(text: str) -> int:
    """Count convergence items from the Convergence Achieved section."""
    m = _CONVERGENCE_SECTION.search(text)
    if not m:
        return 0
    section = m.group(1)
    items = _CONVERGENCE_ITEM.findall(section)
    return len(items)


# Dangerous Contradictions Found section
_CONTRADICTIONS_SECTION: re.Pattern[str] = re.compile(
    r"#{1,4}\s*Dangerous Contradictions Found\s*\n"
    r"(.*?)(?=\n#{1,4}\s|\n---|\Z)",
    re.DOTALL,
)

# Numbered items under a **Resolved:** header or containing **Resolved in revision:**
# (Not used as a compiled pattern — resolution matching is inline in the function)


def _extract_resolved_contradictions_count(text: str) -> int:
    """Count resolved contradictions from the Dangerous Contradictions Found section.

    Looks for the ### Dangerous Contradictions Found section and counts
    numbered items that are explicitly resolved. Two formats are supported:

    1. Items under a **Resolved:** header with numbered sub-items (monorepo style)
    2. Bold-numbered items containing **Resolved in revision:** inline (lease style)

    Sections starting with **None** (factual-question style) return 0.
    """
    m = _CONTRADICTIONS_SECTION.search(text)
    if not m:
        return 0

    section = m.group(1)

    # If section starts with **None — no contradictions on the actual question
    stripped = section.strip()
    if stripped.startswith("**None"):
        return 0

    # Pattern 1 (monorepo style): Explicit **Resolved:** header followed by
    # numbered items, then **Unresolved:** header. Count items between them.
    resolved_header = re.search(r"\*\*Resolved", section)
    unresolved_header = re.search(r"\*\*Unresolved", section)

    if resolved_header and unresolved_header:
        resolved_block = section[resolved_header.end():unresolved_header.start()]
        return len(re.findall(r"^\d+\.\s+", resolved_block, re.MULTILINE))

    # Pattern 2 (lease style): Bold-numbered items like **1. Title.**
    # containing "Resolved in revision:" or "Resolution:" inline.
    # Items start with **N. (bold number prefix)
    resolved_count = 0
    items = re.split(r"(?=\*\*\d+\.)", section)
    for item in items:
        if not item.strip():
            continue
        if re.search(r"\*\*Resolved|\*\*Resolution", item):
            resolved_count += 1

    return resolved_count


def _extract_headline(text: str) -> str:
    """Extract headline from the synthesis output.

    Priority order:
    1. First bold text from ### Convergence Achieved numbered list
    2. First P1 bold text from ### Actionable Spec Changes
    3. The # Synthesis: title line
    4. Empty string
    """
    # Try convergence section first
    m = _CONVERGENCE_SECTION.search(text)
    if m:
        section = m.group(1)
        item = _CONVERGENCE_ITEM.search(section)
        if item:
            return item.group(1).strip().rstrip(".")

    # Try Actionable Spec Changes P1
    m = _SPEC_CHANGES_SECTION.search(text)
    if m:
        section = m.group(1)
        item = _P1_ITEM.search(section)
        if item:
            return item.group(1).strip().rstrip(".")

    # Fall back to synthesis title
    m = _SYNTHESIS_TITLE.search(text)
    if m:
        return m.group(1).strip()

    return ""


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------


def parse_synthesis(text: str, mode: str = "cooperative") -> ConversusOutput:
    """Parse a cooperative synthesis markdown into the canonical output format.

    Extracts structured fields from the synthesis using regex-based parsing
    and the existing quality gate's dispute counter. All extracted values
    are deterministic — no LLM judgment involved.

    Args:
        text: Full text of the synthesis markdown.
        mode: Deliberation mode (default: "cooperative"). Used as fallback
              if mode cannot be extracted from the text.

    Returns:
        ConversusOutput with all fields populated.

    Raises:
        ValueError: If text is empty or None.
    """
    if not text or not text.strip():
        raise ValueError(
            "Cannot parse empty synthesis text. "
            "Provide the full markdown output from a conversus deliberation."
        )

    # Extract quality indicators
    agent_count = _extract_agent_count(text)
    extracted_mode = _extract_mode(text, default=mode)
    phases_completed = _extract_phases_completed(text)
    cross_reviews = _extract_cross_reviews_performed(text, agent_count)

    # Reuse the tested dispute parser from linter.quality
    disagreement = check_disagreement(text, mode=extracted_mode)
    dispute_count = disagreement.dispute_count

    # Count resolved contradictions for surfaced vs surviving distinction
    resolved_contradictions = _extract_resolved_contradictions_count(text)

    convergence_count = _extract_convergence_count(text)
    has_scorecard = _SCORECARD_HEADING.search(text) is not None

    # Guard against silent parse failure: a real synthesis produces *some*
    # structural marker — an Agents header/table, a dispute section the mode
    # fallback can parse, a Convergence block, resolved-contradictions list,
    # or a Scorecard heading. If every one of those is absent, the text is
    # almost always meta-prose from a misbehaving tool-use agent returning a
    # chat-message receipt (see spec 027 postmortem). The phases-completed
    # prose-keyword heuristic is intentionally excluded here — it pops
    # positive on any paragraph that narrates review/revision/dispute/
    # synthesis and so cannot distinguish a real synthesis from a well-
    # written receipt.
    structural_evidence = (
        agent_count > 0
        or dispute_count > 0
        or convergence_count > 0
        or resolved_contradictions > 0
        or has_scorecard
    )
    if not structural_evidence:
        raise UnparseableSynthesisError(
            "Synthesis text contains no recognizable structural markers "
            "(no agent count, no dispute/landed-attack sections, no "
            "convergence block, no scorecard). This is typically meta-prose "
            "returned by a tool-use-capable agent that wrote the real "
            "synthesis to disk via a Write tool and returned only a "
            "conversational receipt as its response — which the engine "
            "then clobbered over the real file. Check the agent's "
            "system/tool config, or that the mode template instructs the "
            "agent to return the synthesis as its response (not Write it)."
        )

    # Extract headline and build deterministic summary
    headline = _extract_headline(text)

    summary = (
        f"{agent_count} agents in {extracted_mode} mode completed "
        f"{phases_completed} phases. {convergence_count} convergence "
        f"points, {dispute_count} surviving disputes."
    )

    quality_indicators = QualityIndicators(
        agent_count=agent_count,
        mode=extracted_mode,
        phases_completed=phases_completed,
        cross_reviews_performed=cross_reviews,
        genuine_disagreements_surfaced=dispute_count + resolved_contradictions,
        genuine_disagreements_surviving=dispute_count,
    )

    return ConversusOutput(
        headline=headline,
        summary=summary,
        full_analysis=text,
        quality_indicators=quality_indicators,
        debate_transcript=text,
    )


# ---------------------------------------------------------------------------
# CLI entry point — invoked via `python3 -m linter.output_contract <path>`
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Parse conversus synthesis output into the canonical "
        "ConversusOutput JSON format. "
        "Exits 0 on success, 2 on file-not-found.",
    )
    parser.add_argument(
        "path",
        help="Path to a conversus synthesis markdown file.",
    )
    parser.add_argument(
        "--mode",
        default="cooperative",
        help="Deliberation mode (default: cooperative).",
    )
    args = parser.parse_args()

    filepath = Path(args.path)
    if not filepath.exists():
        print(
            json.dumps({"error": f"File not found: {args.path}"}),
            file=sys.stderr,
        )
        sys.exit(2)

    text = filepath.read_text(encoding="utf-8")
    try:
        result = parse_synthesis(text, mode=args.mode)
    except UnparseableSynthesisError as exc:
        print(
            json.dumps({
                "error": "unparseable_synthesis",
                "message": str(exc),
                "path": args.path,
                "mode": args.mode,
            }),
            file=sys.stderr,
        )
        sys.exit(3)
    print(result.model_dump_json(indent=2))
    sys.exit(0)
