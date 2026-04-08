"""Template loading, filling, and context construction for the conversus engine.

Provides:
- ``find_templates_dir()`` — locate templates/ relative to the conversus root
- ``load_template()`` — load a mode-specific phase template, rejecting drafts
- ``fill_template()`` — substitute {VARIABLE} placeholders from a TemplateContext
- ``build_review_context()`` — construct a ReviewContext for Phase 1
- ``build_cross_review_context()`` — construct a CrossReviewContext for Phase 2
- ``build_revision_context()`` — construct a RevisionContext for Phase 3
- ``build_disputes_context()`` — construct a DisputesContext for Phase 4
- ``build_synthesis_context()`` — construct a SynthesisContext for Phase 5

All template errors are raised as ``TemplateError`` with actionable messages
that include the template path and the specific problem.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from linter.models import (
    ArbitrationContext,
    CrossReviewContext,
    CrossRoundSynthesisContext,
    DisputesContext,
    PathList,
    ReviewContext,
    RevisionContext,
    SynthesisContext,
    TemplateContext,
)

from engine.config import EngineConfig, AgentConfig, ArbiterConfig
from engine.output import OutputManager

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

UNFILLED_VAR_RE = re.compile(r"\{[A-Z_]+\}")

DRAFT_MARKER = "<!-- CONVERSUS:TEMPLATE_STATUS: draft -->"


class TemplateError(Exception):
    """Raised when a template cannot be loaded, filled, or is invalid."""

    pass


# ---------------------------------------------------------------------------
# Template directory discovery
# ---------------------------------------------------------------------------

def find_templates_dir(config_path: Path) -> Path:
    """Locate the ``templates/`` directory relative to the conversus project root.

    Resolution order:
    1. Walk up from the config file's directory.
    2. ``importlib.resources`` via ``conversus.paths`` (works when pip-installed).
    3. ``Path(__file__).parent.parent`` (engine/ is a child of conversus root).
    4. Current working directory.

    Args:
        config_path: Path to the conversus YAML config file.

    Returns:
        Resolved path to the ``templates/`` directory.

    Raises:
        TemplateError: If templates/ cannot be found.
    """
    # Strategy 1: walk up from config file location
    candidate = config_path.resolve().parent
    for _ in range(10):  # safety bound
        templates = candidate / "templates"
        if templates.is_dir():
            return templates
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent

    # Strategy 2: importlib.resources (works when pip-installed)
    try:
        from conversus.paths import get_templates_dir
        return get_templates_dir()
    except (ImportError, FileNotFoundError):
        pass

    # Strategy 3: engine/ is a child of conversus root (dev fallback)
    engine_root = Path(__file__).resolve().parent.parent
    templates = engine_root / "templates"
    if templates.is_dir():
        return templates

    # Strategy 4: cwd
    templates = Path.cwd() / "templates"
    if templates.is_dir():
        return templates

    raise TemplateError(
        "Cannot locate templates/ directory. "
        "Ensure it exists relative to the config file or the conversus root."
    )


# ---------------------------------------------------------------------------
# Template loading
# ---------------------------------------------------------------------------

def load_template(templates_dir: Path, mode: str, phase: str) -> str:
    """Load a template file from ``templates/{mode}/{phase}.md``.

    Rejects templates marked as draft via the
    ``<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`` marker on the first line.

    Args:
        templates_dir: Path to the ``templates/`` directory.
        mode: Competition mode (e.g. ``cooperative``).
        phase: Phase name (e.g. ``review``).

    Returns:
        The raw template content as a string.

    Raises:
        TemplateError: If the file is missing or marked as draft.
    """
    path = templates_dir / mode / f"{phase}.md"
    if not path.exists():
        raise TemplateError(
            f"Template not found: {path}. "
            "Ensure templates/ directory exists relative to the config file."
        )

    content = path.read_text(encoding="utf-8")

    # Check first line for draft marker
    first_line = content.split("\n", 1)[0].strip()
    if DRAFT_MARKER in first_line:
        raise TemplateError(
            f"Template {path} is marked as draft and cannot be used in production runs."
        )

    return content


# ---------------------------------------------------------------------------
# Template filling
# ---------------------------------------------------------------------------

def _serialize_value(value: Any) -> str:
    """Convert a context field value to its template string representation.

    - ``None`` → empty string
    - ``list[Path]`` (PathList) → newline-separated bare paths (no bullets)
    - ``Path`` → string representation
    - ``int`` → string representation
    - ``str`` → as-is
    """
    if value is None:
        return ""
    if isinstance(value, list):
        # PathList: one bare path per line
        return "\n".join(str(p) for p in value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, int):
        return str(value)
    return str(value)


def fill_template(template: str, context: TemplateContext) -> str:
    """Substitute all ``{VARIABLE}`` placeholders in a template.

    Uses ``context.model_dump()`` to extract field values and serializes
    each value appropriately (Path→str, PathList→newline-separated, None→"",
    int→str).

    After substitution, verifies no ``{VARIABLE}`` patterns remain.

    Args:
        template: Raw template content with ``{VARIABLE}`` placeholders.
        context: A TemplateContext (or subclass) with the variable values.

    Returns:
        The filled template with all placeholders resolved.

    Raises:
        TemplateError: If unfilled variables remain after substitution.
    """
    # Get raw field values (not serialized by Pydantic)
    values = context.model_dump(mode="python")
    filled = template
    for key, value in values.items():
        placeholder = "{" + key + "}"
        if placeholder in filled:
            filled = filled.replace(placeholder, _serialize_value(value))

    # Verify no unfilled variables remain
    remaining = UNFILLED_VAR_RE.findall(filled)
    if remaining:
        unique = sorted(set(remaining))
        raise TemplateError(
            f"Unfilled template variables remain after substitution: {unique}. "
            "Ensure all required context fields are provided."
        )

    return filled


# ---------------------------------------------------------------------------
# Phase 1 context construction
# ---------------------------------------------------------------------------

def build_review_context(
    config: EngineConfig,
    agent: AgentConfig,
    output_dir: Path,
    *,
    round: int = 1,
    prior_synthesis_path: str | None = None,
    prior_round_dir: str | None = None,
    prior_arbitration_path: Path | None = None,
) -> ReviewContext:
    """Construct a ``ReviewContext`` for Phase 1 review templates.

    Builds the context from the engine config and agent definition.
    For single-round (S01), prior sections are empty strings.

    Args:
        config: The parsed engine configuration.
        agent: The specific agent to build context for.
        output_dir: The base output directory.
        round: Current round number (default 1).
        prior_synthesis_path: Path to prior round's synthesis (if round > 1).
        prior_round_dir: Path to prior round's directory (if round > 1).
        prior_arbitration_path: Path to prior round's arbitration (if exists).

    Returns:
        A frozen ``ReviewContext`` instance ready for template filling.
    """
    mgr = OutputManager(output_dir)

    return ReviewContext(
        OUTPUT_PATH=mgr.get_review_path(agent.name),
        TARGET_FILES=config.target_files,
        AGENT_NAME=agent.name,
        AGENT_PROMPT=agent.prompt,
        AGENT_DOCS=agent.docs,
        MODE=config.mode,
        PRIOR_FILES_SECTION="",
        PRIOR_ROUND_SECTION="",
        ROUND=round,
        MAX_ROUNDS=config.rounds,
        PRIOR_SYNTHESIS_PATH=prior_synthesis_path,
        PRIOR_ROUND_DIR=prior_round_dir,
        PRIOR_ARBITRATION_PATH=prior_arbitration_path,
        # AGENT_ROLE: only set for red-blue mode, otherwise None
        AGENT_ROLE=agent.role if config.mode == "red-blue" else None,
    )


# ---------------------------------------------------------------------------
# Phase 2 context construction
# ---------------------------------------------------------------------------

def _find_agent(config: EngineConfig, name: str) -> AgentConfig:
    """Look up an agent by name from the config."""
    for a in config.agents:
        if a.name == name:
            return a
    raise TemplateError(f"Agent '{name}' not found in config.")


def build_cross_review_context(
    config: EngineConfig,
    reviewer: str,
    reviewed: str,
    output_dir: Path,
    iteration: int = 1,
    *,
    round: int = 1,
    prior_synthesis_path: str | None = None,
    prior_round_dir: str | None = None,
    prior_arbitration_path: Path | None = None,
) -> CrossReviewContext:
    """Construct a ``CrossReviewContext`` for Phase 2 cross-review templates.

    Args:
        config: The parsed engine configuration.
        reviewer: Name of the agent writing the cross-review.
        reviewed: Name of the agent being reviewed.
        output_dir: The base output directory.
        iteration: Current iteration (determines which position to read).
        round: Current round number (default 1).
        prior_synthesis_path: Path to prior round's synthesis (if round > 1).
        prior_round_dir: Path to prior round's directory (if round > 1).
        prior_arbitration_path: Path to prior round's arbitration (if exists).

    Returns:
        A frozen ``CrossReviewContext`` instance ready for template filling.
    """
    mgr = OutputManager(output_dir)
    reviewer_agent = _find_agent(config, reviewer)
    reviewed_agent = _find_agent(config, reviewed)

    return CrossReviewContext(
        OUTPUT_PATH=mgr.get_cross_review_path(reviewer, reviewed),
        TARGET_FILES=config.target_files,
        REVIEWER_NAME=reviewer,
        REVIEWER_PROMPT=reviewer_agent.prompt,
        REVIEWED_NAME=reviewed,
        REVIEWED_REVIEW_PATH=mgr.position_path(reviewed, iteration),
        REVIEWER_REVIEW_PATH=mgr.position_path(reviewer, iteration),
        AGENT_DOCS=reviewer_agent.docs,
        MODE=config.mode,
        ROUND=round,
        MAX_ROUNDS=config.rounds,
        PRIOR_SYNTHESIS_PATH=prior_synthesis_path,
        PRIOR_ROUND_DIR=prior_round_dir,
        PRIOR_ARBITRATION_PATH=prior_arbitration_path,
        REVIEWER_ROLE=reviewer_agent.role if config.mode == "red-blue" else None,
        REVIEWED_ROLE=reviewed_agent.role if config.mode == "red-blue" else None,
    )


# ---------------------------------------------------------------------------
# Phase 3 context construction
# ---------------------------------------------------------------------------

def build_revision_context(
    config: EngineConfig,
    agent: str,
    output_dir: Path,
    iteration: int,
    other_agents: list[str],
    *,
    round: int = 1,
    prior_synthesis_path: str | None = None,
    prior_round_dir: str | None = None,
    prior_arbitration_path: Path | None = None,
) -> RevisionContext:
    """Construct a ``RevisionContext`` for Phase 3 revision templates.

    Args:
        config: The parsed engine configuration.
        agent: Name of the agent writing the revision.
        output_dir: The base output directory.
        iteration: Current iteration number (1-based).
        other_agents: Names of all other agents in the deliberation.
        round: Current round number (default 1).
        prior_synthesis_path: Path to prior round's synthesis (if round > 1).
        prior_round_dir: Path to prior round's directory (if round > 1).
        prior_arbitration_path: Path to prior round's arbitration (if exists).

    Returns:
        A frozen ``RevisionContext`` instance ready for template filling.
    """
    mgr = OutputManager(output_dir)
    agent_config = _find_agent(config, agent)

    # Cross-reviews written about this agent's work (by other agents)
    cross_reviews_of_me = [
        mgr.get_cross_review_path(other, agent) for other in other_agents
    ]

    # Cross-reviews this agent wrote about others
    my_cross_reviews = [
        mgr.get_cross_review_path(agent, other) for other in other_agents
    ]

    return RevisionContext(
        OUTPUT_PATH=mgr.get_revision_path(agent, iteration),
        TARGET_FILES=config.target_files,
        AGENT_NAME=agent,
        AGENT_PROMPT=agent_config.prompt,
        AGENT_DOCS=agent_config.docs,
        MY_REVIEW_PATH=mgr.get_review_path(agent),
        CROSS_REVIEWS_OF_ME=cross_reviews_of_me,
        MY_CROSS_REVIEWS=my_cross_reviews,
        ITERATION=iteration,
        MODE=config.mode,
        ROUND=round,
        MAX_ROUNDS=config.rounds,
        PRIOR_SYNTHESIS_PATH=prior_synthesis_path,
        PRIOR_ROUND_DIR=prior_round_dir,
        PRIOR_ARBITRATION_PATH=prior_arbitration_path,
        AGENT_ROLE=agent_config.role if config.mode == "red-blue" else None,
    )


# ---------------------------------------------------------------------------
# Phase 4 context construction
# ---------------------------------------------------------------------------

def build_disputes_context(
    config: EngineConfig,
    agent: str,
    output_dir: Path,
    iterations: int,
    all_agents: list[str],
    *,
    round: int = 1,
    prior_synthesis_path: str | None = None,
    prior_round_dir: str | None = None,
    prior_arbitration_path: Path | None = None,
) -> DisputesContext:
    """Construct a ``DisputesContext`` for Phase 4 disputes templates.

    Args:
        config: The parsed engine configuration.
        agent: Name of the agent writing the disputes.
        output_dir: The base output directory.
        iterations: Total number of iterations completed.
        all_agents: Names of all agents in the deliberation.
        round: Current round number (default 1).
        prior_synthesis_path: Path to prior round's synthesis (if round > 1).
        prior_round_dir: Path to prior round's directory (if round > 1).
        prior_arbitration_path: Path to prior round's arbitration (if exists).

    Returns:
        A frozen ``DisputesContext`` instance ready for template filling.
    """
    mgr = OutputManager(output_dir)
    agent_config = _find_agent(config, agent)

    all_revision_paths = mgr.get_all_final_revision_paths(all_agents, iterations)

    return DisputesContext(
        OUTPUT_PATH=mgr.get_disputes_path(agent),
        TARGET_FILES=config.target_files,
        AGENT_NAME=agent,
        AGENT_PROMPT=agent_config.prompt,
        AGENT_DOCS=agent_config.docs,
        ALL_REVISION_PATHS=all_revision_paths,
        MY_REVISION_PATH=mgr.get_final_revision_path(agent, iterations),
        MODE=config.mode,
        ROUND=round,
        MAX_ROUNDS=config.rounds,
        PRIOR_SYNTHESIS_PATH=prior_synthesis_path,
        PRIOR_ROUND_DIR=prior_round_dir,
        PRIOR_ARBITRATION_PATH=prior_arbitration_path,
        AGENT_ROLE=agent_config.role if config.mode == "red-blue" else None,
    )


# ---------------------------------------------------------------------------
# Phase 5 context construction
# ---------------------------------------------------------------------------

def build_synthesis_context(
    config: EngineConfig,
    output_dir: Path,
    iterations: int,
    active_agents: list[str] | None = None,
    *,
    round: int = 1,
    prior_synthesis_path: str | None = None,
    prior_round_dir: str | None = None,
    prior_arbitration_path: Path | None = None,
) -> SynthesisContext:
    """Construct a ``SynthesisContext`` for Phase 5 synthesis templates.

    Args:
        config: The parsed engine configuration.
        output_dir: The base output directory.
        iterations: Total number of iterations completed.
        active_agents: If provided, only include these agents (for failure
            isolation). Defaults to all agents from config.
        round: Current round number (default 1).
        prior_synthesis_path: Path to prior round's synthesis (if round > 1).
        prior_round_dir: Path to prior round's directory (if round > 1).
        prior_arbitration_path: Path to prior round's arbitration (if exists).

    Returns:
        A frozen ``SynthesisContext`` instance ready for template filling.
    """
    mgr = OutputManager(output_dir)
    agent_names = active_agents if active_agents is not None else [a.name for a in config.agents]

    return SynthesisContext(
        OUTPUT_PATH=mgr.get_synthesis_path(),
        TARGET_FILES=config.target_files,
        AGENT_NAMES=", ".join(agent_names),
        ALL_REVIEWS=mgr.get_all_review_paths(agent_names),
        ALL_CROSS_REVIEWS=mgr.get_all_cross_review_paths(agent_names),
        ALL_REVISIONS=mgr.get_all_final_revision_paths(agent_names, iterations),
        ALL_DISPUTES=mgr.get_all_disputes_paths(agent_names),
        MODE=config.mode,
        TARGET_PATH=config.target_files[0],
        ROUND=round,
        MAX_ROUNDS=config.rounds,
        PRIOR_SYNTHESIS_PATH=prior_synthesis_path,
        PRIOR_ROUND_DIR=prior_round_dir,
        PRIOR_ARBITRATION_PATH=prior_arbitration_path,
    )


# ---------------------------------------------------------------------------
# Dispute extraction helper (shared between quality gate and context builders)
# ---------------------------------------------------------------------------

# Marker regexes — must match linter/quality.py constants exactly.
_DISPUTES_BEGIN_RE = re.compile(r"<!--\s*CONVERSUS:DISPUTES_BEGIN\s*-->")
_DISPUTES_END_RE = re.compile(r"<!--\s*CONVERSUS:DISPUTES_END\s*-->")

# Mode-specific dispute headings for fallback extraction.
# New modes (spec 028): negotiation, resource-allocation, fair-division, mechanism-design.
_MODE_DISPUTE_HEADINGS: dict[str, str] = {
    "cooperative": r"^###\s+Remaining\s+Disputes",
    "winner-take-all": r"^##\s+Runner-Up",
    "red-blue": r"^###\s+Disputed\s+Risks",
    "prisoners-dilemma": r"^##\s+Disputed\s+Boundaries",
    "negotiation": r"^###\s+Unresolved\s+Terms",
    "resource-allocation": r"^###\s+Contested\s+Allocations",
    "fair-division": r"^###\s+Disputed\s+Valuations",
    "mechanism-design": r"^###\s+Mechanism\s+Vulnerabilities",
}


def _extract_section_text(text: str, heading_pattern: str) -> str | None:
    """Extract text from a heading to the next heading of same or higher level.

    Lightweight copy of ``linter.quality._extract_section_after_heading``
    to avoid a circular-import-risk dependency on the linter's internal API.
    """
    heading_re = re.compile(heading_pattern, re.MULTILINE)
    match = heading_re.search(text)
    if match is None:
        return None

    line = match.group(0).lstrip()
    level = sum(1 for ch in line if ch == "#")

    start = match.end()
    next_heading = re.compile(r"^#{1," + str(level) + r"}\s", re.MULTILINE)
    next_match = next_heading.search(text, start)
    if next_match:
        return text[start:next_match.start()]
    return text[start:]


def _extract_remaining_disputes(synthesis_text: str, mode: str) -> str:
    """Extract the remaining disputes section from synthesis text.

    Two-tier extraction matching the quality gate's parsing strategy:

    1. **Marker-based (primary):** Text between ``DISPUTES_BEGIN`` and
       ``DISPUTES_END`` HTML comment markers.
    2. **Heading-based (fallback):** Text under a mode-specific heading
       (e.g. ``### Remaining Disputes`` for cooperative).

    Returns an empty string when neither tier finds content.
    """
    # Tier 1: marker-based
    begin = _DISPUTES_BEGIN_RE.search(synthesis_text)
    if begin is not None:
        end = _DISPUTES_END_RE.search(synthesis_text, begin.end())
        if end is not None:
            return synthesis_text[begin.end():end.start()].strip()
        # BEGIN without END — take everything after BEGIN
        return synthesis_text[begin.end():].strip()

    # Tier 2: heading-based fallback
    heading_pattern = _MODE_DISPUTE_HEADINGS.get(mode)
    if heading_pattern is not None:
        section = _extract_section_text(synthesis_text, heading_pattern)
        if section is not None:
            return section.strip()

    return ""


# ---------------------------------------------------------------------------
# Phase 6 context construction — Arbitration
# ---------------------------------------------------------------------------

def build_arbitration_context(
    config: EngineConfig,
    output_dir: Path,
    synthesis_text: str,
    round_num: int,
    *,
    round_base: Path | None = None,
) -> ArbitrationContext:
    """Construct an ``ArbitrationContext`` for Phase 6 arbitration templates.

    Requires ``config.arbiter`` to be set; raises ``TemplateError`` otherwise.

    Args:
        config: The parsed engine configuration (must have ``arbiter``).
        output_dir: The base output directory for this round.
        synthesis_text: The text of the synthesis output to extract remaining
            disputes from.
        round_num: The current round number.
        round_base: Optional explicit round base for path computation.

    Returns:
        A frozen ``ArbitrationContext`` instance ready for template filling.
    """
    if config.arbiter is None:
        raise TemplateError(
            "Cannot build arbitration context: config.arbiter is not configured."
        )

    arbiter = config.arbiter
    mgr = OutputManager(output_dir)
    agent_names = [a.name for a in config.agents]

    remaining = _extract_remaining_disputes(synthesis_text, config.mode)

    return ArbitrationContext(
        OUTPUT_PATH=mgr.get_arbitration_path(round_base=round_base),
        TARGET_FILES=config.target_files,
        ARBITER_NAME=arbiter.name,
        ARBITER_PROMPT=arbiter.prompt,
        ARBITER_DOCS="\n".join(str(d) for d in arbiter.docs) if arbiter.docs else "",
        GROUNDING_PATH=arbiter.grounding,
        SYNTHESIS_PATH=mgr.get_synthesis_path(round_base=round_base),
        ALL_DISPUTES=mgr.get_all_disputes_paths(agent_names),
        TRIGGER=arbiter.trigger,
        REMAINING_DISPUTES=remaining,
        AGENT_NAMES=", ".join(agent_names),
        MODE=config.mode,
    )


# ---------------------------------------------------------------------------
# Cross-round synthesis context construction
# ---------------------------------------------------------------------------

def build_cross_round_synthesis_context(
    config: EngineConfig,
    output_dir: Path,
    round_syntheses: list[str],
    rounds_completed: int,
    termination_reason: str,
    *,
    arbitration_paths: list[Path] | None = None,
    arbitration_rulings: str | None = None,
) -> CrossRoundSynthesisContext:
    """Construct a ``CrossRoundSynthesisContext`` for cross-round synthesis.

    Called after all rounds complete (2+) to produce a final synthesis that
    integrates each round's synthesis output.

    Args:
        config: The parsed engine configuration.
        output_dir: The root output directory (not a round subdirectory).
        round_syntheses: List of synthesis text content, one per round.
        rounds_completed: Total number of rounds that ran.
        termination_reason: Why deliberation stopped (``converged``,
            ``stagnation``, ``max_rounds``).
        arbitration_paths: Paths to arbitration outputs, if any rounds had them.
        arbitration_rulings: Pre-formatted text of arbitration rulings, if any.

    Returns:
        A frozen ``CrossRoundSynthesisContext`` instance.
    """
    mgr = OutputManager(output_dir)
    agent_names = [a.name for a in config.agents]

    # Pre-format round syntheses into a single block with round headers
    formatted_parts: list[str] = []
    for i, text in enumerate(round_syntheses, 1):
        formatted_parts.append(f"## Round {i} Synthesis\n\n{text.strip()}")
    formatted = "\n\n---\n\n".join(formatted_parts)

    return CrossRoundSynthesisContext(
        OUTPUT_PATH=mgr.get_cross_round_synthesis_path(),
        TARGET_FILES=config.target_files,
        AGENT_NAMES=", ".join(agent_names),
        MODE=config.mode,
        TARGET_PATH=config.target_files[0],
        ROUNDS_COMPLETED=rounds_completed,
        MAX_ROUNDS=config.rounds,
        ROUND_SYNTHESES=formatted,
        TERMINATION_REASON=termination_reason,
        ARBITRATION_PATHS=arbitration_paths,
        ARBITRATION_RULINGS=arbitration_rulings,
    )
