"""
Quality gate checker for conversus synthesis output.

Structurally parses any conversus cooperative deliberation synthesis and returns
pass/fail on two binary gates:

1. **Substantive Disagreement** — at least one named dispute within the
   DISPUTES_BEGIN/END block, with positions attributed to ≥2 distinct agents.
2. **Agent Attributions Present** — ≥2 distinct agent names with phase-level
   attribution in the scorecard, challenges, and concessions.

Public API:
    check_disagreement(text, mode) -> DisagreementResult
    check_attributions(text) -> AttributionResult
    check_quality_floor(text, mode) -> QualityResult
    check_quality_floor_file(path, mode) -> QualityResult

Models:
    DisputeInfo, DisagreementResult, AttributionResult, QualityResult

Usage:
    from linter.quality import check_quality_floor

    result = check_quality_floor(synthesis_text)
    if not result.passed:
        print(f"Failed: disagreement={result.disagreement.passed}, "
              f"attributions={result.attributions.passed}")
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Pydantic models — frozen per Constitution Principle IX
# ---------------------------------------------------------------------------


class DisputeInfo(BaseModel):
    """A single dispute entry with its label and participating agent names."""

    model_config = {"frozen": True}

    label: str
    agent_names: list[str]


class DisagreementResult(BaseModel):
    """Result of the substantive-disagreement quality gate."""

    model_config = {"frozen": True}

    passed: bool
    dispute_count: int
    disputes: list[DisputeInfo]


class AttributionResult(BaseModel):
    """Result of the agent-attributions quality gate."""

    model_config = {"frozen": True}

    passed: bool
    agent_names: list[str]
    challenge_count: int
    concession_count: int
    phase_reference_count: int


class QualityResult(BaseModel):
    """Combined result of both quality gates."""

    model_config = {"frozen": True}

    passed: bool
    disagreement: DisagreementResult
    attributions: AttributionResult


# ---------------------------------------------------------------------------
# Regex constants — adapted from conversus/quality_floor/structural-definitions.md
# ---------------------------------------------------------------------------

# Dispute block boundaries
DISPUTES_BEGIN: re.Pattern[str] = re.compile(
    r"<!--\s*CONVERSUS:DISPUTES_BEGIN\s*-->"
)
DISPUTES_END: re.Pattern[str] = re.compile(
    r"<!--\s*CONVERSUS:DISPUTES_END\s*-->"
)

# Individual dispute entries — handles BOTH formats:
#   **Dispute: [Label]**   (bold)
#   #### Dispute: [Label]  (heading level)
DISPUTE_MARKER: re.Pattern[str] = re.compile(
    r"(?:^|\n)\s*(?:\*\*Dispute:\s*|#{1,4}\s*Dispute:\s*)(.+?)(?:\*\*)?(?:\s*$)",
    re.MULTILINE,
)

# Agent positions within disputes — handles multiple reference output formats:
#   *Pragmatist:*                        (italic with colon inside)
#   **Pragmatist position:**             (bold with "position" keyword)
#   - *Agent:*                           (list item with italic)
#   *Devil's Advocate:*                  (italic, apostrophe in name)
#   **Devil's Advocate position:**       (bold with "position")
DISPUTE_POSITION: re.Pattern[str] = re.compile(
    r"\*{1,2}([A-Za-z\s\-\']+?)(?:\s+position)?:?\s*\*{1,2}"
)

# Scorecard agent names — format: | P-R1 | Pragmatist | ... or | DA-R1 | Devil's Advocate |
SCORECARD_AGENT: re.Pattern[str] = re.compile(
    r"\|\s*[A-Z]{1,3}-[A-Z]?\d+\s*\|\s*([A-Za-z\s\-\']+?)\s*\|"
)

# Scorecard fallback for tables without ID prefixes (e.g., factual-capital format):
# | # | Recommendation | Pragmatist | Devil's Advocate | Status |
# Detects header rows with agent names as column headers
SCORECARD_HEADER_AGENTS: re.Pattern[str] = re.compile(
    r"\|\s*(?:#|Recommendation)\s*\|.*?"
    r"((?:[A-Z][a-z]+(?:\s+[A-Za-z\-\']+)*)"
    r"(?:\s*\|\s*[A-Z][a-z]+(?:\s+[A-Za-z\-\']+)*)*)\s*\|",
)

# Concession — bold-name format: **Agent conceded:**
CONCESSION_AGENT: re.Pattern[str] = re.compile(
    r"\*\*([A-Za-z\s\-\']+?)\s+concede[ds]?"
)

# Concession — table format:
# | Agent | Withdrew/Absorbed/Adopted/Accepted/Reduced/Kept/Acknowledged... |
# Must be the FIRST column with a short agent name, followed by an action verb column.
# Agent names are typically ≤3 words; this prevents matching long description text.
CONCESSION_TABLE: re.Pattern[str] = re.compile(
    r"\|\s*([A-Za-z](?:[A-Za-z\s\-\']{0,25}))\s*\|\s*"
    r"(?:Withdrew|Absorbed|Adopted|Accepted|Reduced|Kept|Acknowledged)"
)

# Challenged By — agents in the Challenged By column (not dashes)
CHALLENGED_BY: re.Pattern[str] = re.compile(
    r"(?:Challenged\s+By|challenged\s+by)[^\|]*?\|\s*"
    r"(?!—)([A-Za-z\s\-\']+?)(?:\s*\(|cross-review|\s*\|)",
    re.IGNORECASE,
)

# Alternative: detect challenge attributions within scorecard rows
# e.g., "DA cross-review (scope conflict)" or "Pragmatist cross-review"
# or "Pragmatist (mixed signals with deferral)"
CHALLENGE_IN_ROW: re.Pattern[str] = re.compile(
    r"\|\s*(?!—\s*\|)([A-Za-z\s\-\']+?)\s*"
    r"(?:cross-review|(?:\([^)]+\)))\s*\|"
)

# Phase references — citations linking positions to specific deliberation phases.
# Matches any parenthetical containing phase-related keywords:
#   (revision R3, R7)
#   (DA cross-review DC§1 → Pragmatist revision R3, R7)
#   (Sources: Pragmatist cross-review Tensions §1; DA revision Recommendation 1.)
#   (Phase 4 Dispute 1)
#   (Both agents; converged through revision.)
PHASE_REFERENCE: re.Pattern[str] = re.compile(
    r"\([^)]*(?:cross-review|revision|Phase\s+\d)[^)]*\)",
    re.IGNORECASE,
)

# Negation patterns within a dispute block
NEGATION_PATTERN: re.Pattern[str] = re.compile(
    r"(?:\*\*None\.?\*\*|no\s+remaining\s+disputes)",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Gate 1: Substantive Disagreement
# ---------------------------------------------------------------------------


def _extract_dispute_block(text: str) -> str | None:
    """Extract the text between DISPUTES_BEGIN and DISPUTES_END markers.

    Returns None if the DISPUTES_BEGIN marker is absent.
    """
    begin_match = DISPUTES_BEGIN.search(text)
    if begin_match is None:
        return None

    end_match = DISPUTES_END.search(text, begin_match.end())
    if end_match is None:
        # BEGIN present but no END — take everything after BEGIN
        return text[begin_match.end():]

    return text[begin_match.end():end_match.start()]


def _normalize_agent_name(name: str) -> str:
    """Normalize an agent name: strip whitespace and title-case.

    Handles apostrophes correctly (e.g., "Devil's Advocate" not "Devil'S Advocate").
    """
    stripped = name.strip()
    if not stripped:
        return stripped
    # Use capwords-style but preserve lowercase after apostrophes
    words = stripped.split()
    result_words: list[str] = []
    for word in words:
        if "'" in word:
            # Capitalize only the first letter, keep the rest as-is after lowering
            parts = word.split("'")
            result_words.append(
                "'".join(p.capitalize() if i == 0 else p.lower() for i, p in enumerate(parts))
            )
        else:
            result_words.append(word.capitalize())
    return " ".join(result_words)


def _extract_dispute_agents(dispute_text: str) -> list[str]:
    """Extract unique agent names from a single dispute's text.

    Only looks at the Positions section of the dispute, not the full text,
    to avoid picking up section headers like 'Synthesizer Assessment'.
    """
    # Try to find the positions section — look between "Positions:" and the next
    # section header (Arguments:, Synthesizer assessment:, Recommended resolution:)
    positions_match = re.search(
        r"(?:\*\*)?Positions:?\s*(?:\*\*)?\s*\n(.*?)(?=\n\s*\*\*(?:Arguments|Synthesizer|Recommended)|$)",
        dispute_text,
        re.DOTALL | re.IGNORECASE,
    )

    # If no explicit Positions section, look for the pattern in the broader text
    # but only up to the "Synthesizer assessment" or "Arguments" section
    search_text = dispute_text
    if positions_match:
        search_text = positions_match.group(1)
    else:
        # Look for agent position patterns before any assessment/arguments section
        cutoff = re.search(
            r"\n\s*\*\*(?:Synthesizer|Arguments|Recommended)",
            dispute_text,
            re.IGNORECASE,
        )
        if cutoff:
            search_text = dispute_text[:cutoff.start()]

    matches = DISPUTE_POSITION.findall(search_text)
    seen: set[str] = set()
    names: list[str] = []

    # Known non-agent words to filter
    non_agent = {
        "positions", "arguments", "none", "status",
        "recommendation", "converged", "disputed",
        "synthesizer assessment", "recommended resolution",
        "synthesizer", "within", "before", "and",
    }

    for raw in matches:
        normalized = _normalize_agent_name(raw)
        if (
            normalized
            and normalized.lower() not in non_agent
            and len(normalized) > 1
        ):
            if normalized not in seen:
                seen.add(normalized)
                names.append(normalized)
    return names


def _split_disputes(block: str, markers: list[re.Match[str]]) -> list[str]:
    """Split a dispute block into individual dispute texts using marker positions."""
    texts: list[str] = []
    for i, m in enumerate(markers):
        start = m.start()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(block)
        texts.append(block[start:end])
    return texts


def _parse_marker_disputes(block: str) -> list[DisputeInfo]:
    """Parse disputes from a DISPUTES_BEGIN/END block using standard markers.

    Returns an empty list if the block is empty, contains only negation
    patterns, or has no ``**Dispute:`` / ``#### Dispute:`` entries.
    """
    stripped = block.strip()
    if not stripped:
        return []

    has_negation = NEGATION_PATTERN.search(block) is not None
    dispute_matches = list(DISPUTE_MARKER.finditer(block))

    if has_negation and not dispute_matches:
        return []

    if not dispute_matches:
        return []

    dispute_texts = _split_disputes(block, dispute_matches)
    disputes: list[DisputeInfo] = []
    for match, dtext in zip(dispute_matches, dispute_texts):
        label = match.group(1).strip().rstrip("*").strip()
        agents = _extract_dispute_agents(dtext)
        disputes.append(DisputeInfo(label=label, agent_names=agents))
    return disputes


# ---------------------------------------------------------------------------
# Mode-specific heading-based fallback parsers
# ---------------------------------------------------------------------------

# Mode dispatch table: heading regex, entry regex, and optional extra logic
# Each mode defines a `synthesis_heading` and `entry_pattern` in its schema.
# The fallback is invoked when DISPUTES_BEGIN/END markers are absent.


def _extract_section_after_heading(
    text: str, heading_pattern: str
) -> str | None:
    """Extract text from a heading to the next heading of same or higher level.

    Args:
        heading_pattern: A regex matching the target heading line.

    Returns:
        The text under the heading, or None if heading not found.
    """
    heading_re = re.compile(heading_pattern, re.MULTILINE)
    match = heading_re.search(text)
    if match is None:
        return None

    # Determine heading level from the number of leading '#' characters
    line = match.group(0).lstrip()
    level = 0
    for ch in line:
        if ch == "#":
            level += 1
        else:
            break

    # Find the next heading of same or higher (≤) level
    start = match.end()
    next_heading = re.compile(r"^#{1," + str(level) + r"}\s", re.MULTILINE)
    next_match = next_heading.search(text, start)
    if next_match:
        return text[start:next_match.start()]
    return text[start:]


def _fallback_cooperative(text: str) -> list[DisputeInfo]:
    """Cooperative fallback: count ``**Dispute:`` under ``Remaining Disputes``.

    Accepts heading levels H1–H4 to tolerate synthesizer heading drift.
    """
    section = _extract_section_after_heading(
        text, r"^#{1,4}\s+Remaining\s+Disputes"
    )
    if section is None:
        return []
    entries = re.findall(r"\*\*Dispute:\s*(.+?)(?:\*\*)?$", section, re.MULTILINE)
    return [
        DisputeInfo(label=e.strip().rstrip("*").strip(), agent_names=[])
        for e in entries
    ]


def _fallback_winner_take_all(text: str) -> list[DisputeInfo]:
    """Winner-take-all fallback.

    1. ``Runner-Up`` heading (H1–H4) presence = 1 dispute (contested selection).
    2. ``Remaining Disputes`` section with ``**Dispute:`` entries = additional.
    """
    disputes: list[DisputeInfo] = []

    runner_up_section = _extract_section_after_heading(
        text, r"^#{1,4}\s+Runner-Up"
    )
    if runner_up_section is not None:
        # Extract a label from the first non-empty line
        for raw_line in runner_up_section.strip().splitlines():
            stripped_line = raw_line.strip()
            if stripped_line:
                label = stripped_line.lstrip("#").lstrip("*").strip().rstrip("*").strip()
                if label:
                    disputes.append(DisputeInfo(label=f"Runner-Up: {label}", agent_names=[]))
                break
        else:
            disputes.append(DisputeInfo(label="Runner-Up", agent_names=[]))

    # Also check for ### Remaining Disputes (same as cooperative)
    disputes.extend(_fallback_cooperative(text))
    return disputes


# Red-blue risk-entry pattern. Tolerates two surface forms the synthesizer
# may produce under a Landed/Disputed section:
#   - bold list item: ``- **[RISK-ID]: Description** ...``
#   - heading entry:  ``### [RISK-ID]: Description``
# LLM output has been observed to use either style, and to shift heading levels
# as the surrounding section heading drifts between H1–H3.
_RED_BLUE_ENTRY: re.Pattern[str] = re.compile(
    r"(?:^#{2,5}\s+|\*\*)\[([^\]]+)\][:\s]",
    re.MULTILINE,
)

# Authoritative fallback: parse counts straight out of the Scorecard table.
# Template-declared rows: "Landed (unmitigated)" and "Disputed (unresolved)".
_SCORECARD_LANDED_ROW: re.Pattern[str] = re.compile(
    r"\|\s*Landed[^\|]*\|\s*(\d+)\s*\|", re.IGNORECASE
)
_SCORECARD_DISPUTED_ROW: re.Pattern[str] = re.compile(
    r"\|\s*Disputed[^\|]*\|\s*(\d+)\s*\|", re.IGNORECASE
)


def _fallback_red_blue(text: str) -> list[DisputeInfo]:
    """Red-blue fallback: count surviving unresolved risk entries.

    Counts two kinds of surviving risk as disputes:

    1. Entries under ``Landed Attacks — Unmitigated Risks`` — Red Team's
       attacks the arbiter ruled Blue Team could not adequately mitigate.
    2. Entries under ``Disputed Risks`` — risks where Red and Blue
       fundamentally disagreed and the arbiter could not rule.

    Mitigated Attacks and Accepted Risks are NOT counted.

    Heading levels H1–H3 are accepted for both section and entry lines, and
    entries may be either bold list items or heading entries. If the prose
    sections are absent or malformed, falls back to the Scorecard table's
    authoritative Landed/Disputed row counts.
    """
    # Dedupe by RISK-ID across both sections. The template mandates every
    # threat appear in exactly one category (Landed, Mitigated, Accepted,
    # Disputed), but LLM synthesizers sometimes re-list critical risks under
    # both Landed AND Disputed. The parser must be resilient to that
    # violation: count each RISK-ID once, preferring Landed classification
    # (the stronger verdict) over Disputed.
    disputes: list[DisputeInfo] = []
    seen_ids: set[str] = set()

    landed = _extract_section_after_heading(
        text, r"^#{1,3}\s+Landed\s+Attacks"
    )
    if landed is not None:
        for e in _RED_BLUE_ENTRY.findall(landed):
            risk_id = e.strip()
            if risk_id in seen_ids:
                continue
            seen_ids.add(risk_id)
            disputes.append(
                DisputeInfo(label=f"[Landed] [{risk_id}]", agent_names=[])
            )

    disputed = _extract_section_after_heading(
        text, r"^#{1,3}\s+Disputed\s+Risks"
    )
    if disputed is not None:
        for e in _RED_BLUE_ENTRY.findall(disputed):
            risk_id = e.strip()
            if risk_id in seen_ids:
                continue
            seen_ids.add(risk_id)
            disputes.append(
                DisputeInfo(label=f"[Disputed] [{risk_id}]", agent_names=[])
            )

    if disputes:
        return disputes

    # Authoritative fallback: the Scorecard table is template-declared as the
    # canonical summary, so when prose parsing returns nothing we trust it.
    return _scorecard_disputes(text)


def _scorecard_disputes(text: str) -> list[DisputeInfo]:
    """Read Landed/Disputed counts from the Scorecard table and synthesize
    a matching number of DisputeInfo stubs. Returns [] if no Scorecard."""
    scorecard_section = _extract_section_after_heading(
        text, r"^#{1,3}\s+Scorecard"
    )
    if scorecard_section is None:
        return []
    disputes: list[DisputeInfo] = []
    landed_match = _SCORECARD_LANDED_ROW.search(scorecard_section)
    if landed_match:
        for i in range(int(landed_match.group(1))):
            disputes.append(
                DisputeInfo(label=f"[Landed] [scorecard #{i + 1}]", agent_names=[])
            )
    disputed_match = _SCORECARD_DISPUTED_ROW.search(scorecard_section)
    if disputed_match:
        for i in range(int(disputed_match.group(1))):
            disputes.append(
                DisputeInfo(label=f"[Disputed] [scorecard #{i + 1}]", agent_names=[])
            )
    return disputes


def _fallback_prisoners_dilemma(text: str) -> list[DisputeInfo]:
    """Prisoner's-dilemma fallback: count ``[...]`` sub-headings under ``Disputed Boundaries``."""
    section = _extract_section_after_heading(
        text, r"^#{1,3}\s+Disputed\s+Boundaries"
    )
    if section is None:
        return []
    entries = re.findall(r"^#{2,5}\s+\[([^\]]+)\]", section, re.MULTILINE)
    return [
        DisputeInfo(label=f"[{e.strip()}]", agent_names=[])
        for e in entries
    ]


_FALLBACK_DISPATCH: dict[str, object] = {
    "cooperative": _fallback_cooperative,
    "winner-take-all": _fallback_winner_take_all,
    "red-blue": _fallback_red_blue,
    "prisoners-dilemma": _fallback_prisoners_dilemma,
}


def check_disagreement(
    synthesis_text: str, mode: str = "cooperative"
) -> DisagreementResult:
    """Check the substantive-disagreement quality gate.

    Parsing strategy (two-tier):
      1. **Marker-based** — look for ``DISPUTES_BEGIN``/``DISPUTES_END`` HTML
         comments. This path is mode-agnostic and works for all modes when
         agents include structural markers.
      2. **Heading-based fallback** — when markers are absent, dispatch to a
         mode-specific parser that uses the heading and entry patterns defined
         in ``schema/modes/*.yml``.

    Args:
        synthesis_text: Full text of the synthesis output.
        mode: Deliberation mode (``cooperative``, ``winner-take-all``,
              ``red-blue``, or ``prisoners-dilemma``).

    Returns:
        DisagreementResult with ``passed=True`` if ≥1 dispute found.
    """
    _empty = DisagreementResult(passed=False, dispute_count=0, disputes=[])

    # --- Tier 1: marker-based parsing (mode-agnostic) ---
    block = _extract_dispute_block(synthesis_text)
    if block is not None:
        disputes = _parse_marker_disputes(block)
        if disputes:
            return DisagreementResult(
                passed=True,
                dispute_count=len(disputes),
                disputes=disputes,
            )
        # Markers present but empty/negated → no disputes
        return _empty

    # --- Tier 2: mode-specific heading-based fallback ---
    fallback_fn = _FALLBACK_DISPATCH.get(mode)
    if fallback_fn is None:
        return _empty

    # All values in _FALLBACK_DISPATCH are callables that accept str
    disputes = fallback_fn(synthesis_text)  # type: ignore[operator]
    if not disputes:
        return _empty

    return DisagreementResult(
        passed=True,
        dispute_count=len(disputes),
        disputes=disputes,
    )


# ---------------------------------------------------------------------------
# Gate 2: Agent Attributions Present
# ---------------------------------------------------------------------------


def _extract_scorecard_agents(text: str) -> set[str]:
    """Extract unique agent names from the recommendation scorecard."""
    agents: set[str] = set()

    # Primary: ID-prefixed rows (e.g., | P-R1 | Pragmatist |)
    for match in SCORECARD_AGENT.finditer(text):
        name = _normalize_agent_name(match.group(1))
        if name and name.lower() not in {"agent", "recommendation", "status", "#"}:
            agents.add(name)

    # Fallback: header-row format (factual-capital style, lease style)
    # Look for table headers containing agent-like names after known column headers.
    # e.g., | # | Recommendation | Pragmatist | Devil's Advocate | Status |
    # or:   | Recommendation | Pragmatist | Devil's Advocate | Status |
    if not agents:
        # Match header rows: must start with a table pipe and contain "Recommendation"
        # as a standalone cell (not as part of a data value)
        header_pattern = re.compile(
            r"^\|\s*(?:#\s*\|)?\s*Recommendation\s*\|[^\n]*$",
            re.MULTILINE,
        )
        for hm in header_pattern.finditer(text):
            row = hm.group(0)
            cells = [c.strip() for c in row.split("|") if c.strip()]
            for cell in cells:
                # Skip known non-agent column headers
                if cell.lower() in {
                    "#", "recommendation", "status", "phase 1 priority",
                    "phase 3 disposition", "challenged by", "convergence",
                    "final status", "agent",
                }:
                    continue
                # Accept title-cased multi-word names (2-4 words, ≤30 chars)
                if (
                    re.match(r"^[A-Z][a-z]+(?:['\s\-][A-Za-z]+){0,3}$", cell)
                    and len(cell) <= 30
                ):
                    agents.add(_normalize_agent_name(cell))

    # Also extract from concession sections (agents who conceded are agents)
    for match in CONCESSION_AGENT.finditer(text):
        name = _normalize_agent_name(match.group(1))
        if name and len(name) <= 30:
            agents.add(name)

    for match in CONCESSION_TABLE.finditer(text):
        name = _normalize_agent_name(match.group(1))
        if name and name.lower() not in {"agent"} and len(name) <= 30:
            # Filter out phase names and other non-agent strings
            if name.lower() not in {
                "revision", "cross-review", "review", "phase",
                "disputes", "synthesis",
            }:
                agents.add(name)

    return agents


def _count_challenges(text: str) -> int:
    """Count cross-review challenges attributed to specific agents."""
    count = 0

    # Check for "Challenged By" column entries
    for match in CHALLENGED_BY.finditer(text):
        name = match.group(1).strip()
        if name and name != "—" and name.lower() not in {"—", "none", "n/a", ""}:
            count += 1

    # Also check inline challenge attributions in scorecard rows
    # e.g., "DA cross-review (scope conflict)" in a cell
    challenge_inline = re.compile(
        r"\|\s*([A-Za-z\s\-\']+?)\s+cross-review\s*(?:\([^)]*\))?\s*\|"
    )
    for match in challenge_inline.finditer(text):
        name = match.group(1).strip()
        if name and name.lower() not in {"challenged by", "none", "—"}:
            count += 1

    # Also detect challenge references like "Pragmatist (mixed signals with deferral)"
    challenge_parens = re.compile(
        r"\|\s*([A-Za-z\s\-\']+?)\s*\([^)]+\)\s*\|"
    )
    for match in challenge_parens.finditer(text):
        name = match.group(1).strip()
        if name and name.lower() not in {
            "challenged by", "none", "—", "", "modified",
            "surviving", "adopted", "converged", "dropped",
            "disputed", "merged", "new in phase 3",
        }:
            count += 1

    return count


def _count_concessions(text: str) -> int:
    """Count concession attributions in both bold-name and table formats."""
    count = 0

    # Bold-name format: **Agent conceded:**
    for _ in CONCESSION_AGENT.finditer(text):
        count += 1

    # Table format: | Agent | Withdrew/Absorbed/Adopted... |
    for match in CONCESSION_TABLE.finditer(text):
        name = match.group(1).strip()
        if name.lower() not in {"agent", ""}:
            count += 1

    return count


def _count_phase_references(text: str) -> int:
    """Count phase-level references (citations linking positions to phases)."""
    return len(PHASE_REFERENCE.findall(text))


def check_attributions(synthesis_text: str) -> AttributionResult:
    """Check the agent-attributions quality gate.

    Verifies that the synthesis contains named agent attributions in the
    scorecard, challenges, concessions, and phase references.

    Args:
        synthesis_text: Full text of the synthesis output.

    Returns:
        AttributionResult with pass/fail and detailed attribution counts.

    Thresholds for passing:
        - ≥2 distinct agent names
        - ≥1 cross-review challenge attributed
        - ≥1 concession attributed
        - ≥3 phase references
    """
    agent_names_set = _extract_scorecard_agents(synthesis_text)
    agent_names = sorted(agent_names_set)
    challenge_count = _count_challenges(synthesis_text)
    concession_count = _count_concessions(synthesis_text)
    phase_reference_count = _count_phase_references(synthesis_text)

    passed = (
        len(agent_names) >= 2
        and challenge_count >= 1
        and concession_count >= 1
        and phase_reference_count >= 3
    )

    return AttributionResult(
        passed=passed,
        agent_names=agent_names,
        challenge_count=challenge_count,
        concession_count=concession_count,
        phase_reference_count=phase_reference_count,
    )


# ---------------------------------------------------------------------------
# Composing function & convenience wrapper
# ---------------------------------------------------------------------------


def check_quality_floor(
    synthesis_text: str, mode: str = "cooperative"
) -> QualityResult:
    """Check both quality gates and return a combined result.

    The quality floor passes only when BOTH gates pass:
    - Substantive Disagreement: ≥1 named dispute with ≥2 agent positions
    - Agent Attributions: ≥2 agents, ≥1 challenge, ≥1 concession, ≥3 phase refs

    Args:
        synthesis_text: Full text of the synthesis output.
        mode: Deliberation mode (default: 'cooperative').

    Returns:
        QualityResult with combined pass/fail and sub-gate details.
    """
    disagreement = check_disagreement(synthesis_text, mode)
    attributions = check_attributions(synthesis_text)

    return QualityResult(
        passed=disagreement.passed and attributions.passed,
        disagreement=disagreement,
        attributions=attributions,
    )


def check_quality_floor_file(
    path: Path, mode: str = "cooperative"
) -> QualityResult:
    """Read a synthesis file and check both quality gates.

    Convenience wrapper that reads the file at the given path and delegates
    to check_quality_floor.

    Args:
        path: Path to the synthesis markdown file.
        mode: Deliberation mode (default: 'cooperative').

    Returns:
        QualityResult with combined pass/fail and sub-gate details.

    Raises:
        FileNotFoundError: If the path does not exist.
        OSError: If the file cannot be read.
    """
    text = Path(path).read_text(encoding="utf-8")
    return check_quality_floor(text, mode)


# ---------------------------------------------------------------------------
# CLI entry point — invoked via `python3 -m linter.quality <path>`
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(
        description="Conversus quality gate checker. "
        "Exits 0 on pass, 1 on fail, 2 on file-not-found.",
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

    try:
        result = check_quality_floor_file(Path(args.path), args.mode)
    except FileNotFoundError:
        print(
            json.dumps({"error": f"File not found: {args.path}"}),
            file=sys.stderr,
        )
        sys.exit(2)

    print(result.model_dump_json(indent=2))
    sys.exit(0 if result.passed else 1)
