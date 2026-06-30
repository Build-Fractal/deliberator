"""Feature extraction pipeline for deliberator deliberation artifacts (spec 015).

Deterministic pipeline that converts markdown deliberation output into
numerical feature vectors.  No LLM calls, no randomness -- pure structured
parsing of the predictable deliberator template output format.

Primary entry point:
    extract_features(output_dir, mode) -> FeatureSet

The pipeline reads:
  - Phase 1 reviews  (per-agent: review.md)
  - Phase 2 cross-reviews  (per-agent: cross-reviews/*.md)
  - Phase 3 revisions  (per-agent: revision.md)
  - Phase 4 disputes  (per-agent: disputes.md)
  - Phase 5 synthesis  (summary/final.md)

No heavyweight dependencies (FR-015).  No file writes to agent directories.
"""

from __future__ import annotations

import json
import logging
import re
import warnings
from pathlib import Path
from typing import Any

from deliberator.schemas.features import (
    VALID_MODES,
    AgentFeatures,
    FeatureSet,
    RoundFeatures,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Structural marker patterns (FR-002)
# ---------------------------------------------------------------------------

_DISPUTES_BEGIN = re.compile(
    r"<!--\s*DELIBERATOR:DISPUTES_BEGIN\s*-->", re.IGNORECASE,
)
_DISPUTES_END = re.compile(
    r"<!--\s*DELIBERATOR:DISPUTES_END\s*-->", re.IGNORECASE,
)

# Disposition labels in cooperative/revision output
_DISPOSITION_PATTERN = re.compile(
    r"\*\*(?:Disposition|DISPOSITION)\*?\*?\s*:\s*"
    r"(Withdrawn|Modified|Surviving)",
    re.IGNORECASE,
)

# Alternative: standalone uppercase labels like **WITHDRAWN.** or **SURVIVING.**
_STANDALONE_DISPOSITION = re.compile(
    r"^\*\*(WITHDRAWN|SURVIVING(?:,\s*modified)?|Modified)[.*]*\*\*",
    re.IGNORECASE | re.MULTILINE,
)

# Dispute entries in synthesis
_DISPUTE_ENTRY = re.compile(
    r"^\s*-\s*\*\*Dispute:\s*", re.MULTILINE,
)
_DISPUTE_HEADING = re.compile(
    r"^###?\s+Dispute\s+\d+", re.MULTILINE,
)

# Convergence entries in Phase 4 disputes
_CONVERGENCE_ENTRY = re.compile(
    r"^\s*-\s*\*\*Converged:\s*", re.MULTILINE,
)

# Phase 1 recommendations (cooperative)
_RECOMMENDATION_NUMBERED = re.compile(
    r"^\s*\d+\.\s+\*\*", re.MULTILINE,
)

# New recommendations in revision
_NEW_REC_ITEM = re.compile(
    r"^\s*-\s+\*\*[A-Z]", re.MULTILINE,
)

# Priority labels
_PRIORITY_PATTERN = re.compile(
    r"Priority:\s*(P1|P2|P3)", re.IGNORECASE,
)

# Cross-review safe agreements
_SAFE_AGREEMENT = re.compile(
    r"^\s*-\s*\*\*.*?\*\*", re.MULTILINE,
)

# Red-blue severity labels
_SEVERITY_PATTERN = re.compile(
    r"severity:\s*(critical|high|medium|low)", re.IGNORECASE,
)

# Red-blue threat catalog entries
_THREAT_ENTRY = re.compile(
    r"^\s*-\s*\*\*\[?(?:THREAT-?\w*:?\s*)?[^\]]*\]?\*\*\s*\(severity:\s*(critical|high|medium|low)\)",
    re.IGNORECASE | re.MULTILINE,
)

# Red-blue cascading failure scenarios
_CASCADING_SCENARIO = re.compile(
    r"^\s*-\s*\*\*Scenario\s+(?:name|:)", re.IGNORECASE | re.MULTILINE,
)

# Red-blue safeguards
_SAFEGUARD_ENTRY = re.compile(
    r"^\s*-\s*\*\*\[?.*?\]?\*\*\s*\(spec\s+ref", re.IGNORECASE | re.MULTILINE,
)

# Red-blue acknowledged limitations
_LIMITATION_ENTRY = re.compile(
    r"^\s*-\s*\*\*What\*?\*?:", re.IGNORECASE | re.MULTILINE,
)

# WTA rebuttal / concession sections
_REBUTTED_SECTION = re.compile(
    r"^###?\s+Rebutted:\s*", re.IGNORECASE | re.MULTILINE,
)
_CONCEDED_SECTION = re.compile(
    r"^###?\s+Conceded:\s*", re.IGNORECASE | re.MULTILINE,
)

# WTA criterion score table row
_CRITERION_SCORE_ROW = re.compile(
    r"^\|[^|]+\|\s*(\d+(?:\.\d+)?)\s*\|", re.MULTILINE,
)

# PD overreach / sandbagging flags
_OVERREACH_FLAG = re.compile(
    r"overreach", re.IGNORECASE,
)
_SANDBAGGING_FLAG = re.compile(
    r"sandbagging", re.IGNORECASE,
)

# PD section headers for counting items
_PD_SECTION_ITEMS = re.compile(
    r"^\s*-\s+\*\*", re.MULTILINE,
)

# PD accepted/rebutted in recalibration
_PD_ACCEPTED = re.compile(
    r"^###?\s+Accepted:\s*", re.IGNORECASE | re.MULTILINE,
)
_PD_REBUTTED = re.compile(
    r"^###?\s+Rebutted:\s*", re.IGNORECASE | re.MULTILINE,
)

# Red-blue revision patterns
_RB_WITHDRAWN_ATTACK = re.compile(
    r"^\s*-\s*\*\*\[", re.MULTILINE,
)

# Landed / mitigated / accepted risk sections in RB synthesis
_RISK_ENTRY = re.compile(
    r"^\s*-\s*\*\*\[?(?:RISK-?\w*:?\s*)?", re.MULTILINE,
)

# Responsibility map confidence
_HIGH_CONFIDENCE = re.compile(
    r"\|\s*High\s*\|", re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# File reading helpers
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> str:
    """Read a file's text content.  Returns empty string if missing (FR-003)."""
    if not path.exists():
        warnings.warn(
            f"Feature extraction: file not found, defaulting to empty: {path}",
            stacklevel=2,
        )
        return ""
    return path.read_text(encoding="utf-8")


def _extract_section(text: str, heading: str) -> str:
    """Extract text under a markdown heading until the next same-level heading.

    Supports both ## and ### level headings.
    """
    # Determine the heading level
    level = 0
    for ch in heading:
        if ch == "#":
            level += 1
        else:
            break
    if level == 0:
        level = 3  # default

    # Build pattern
    escaped = re.escape(heading.lstrip("#").strip())
    pattern = re.compile(
        rf"^(#{{{level}}})\s+{escaped}.*?\n(.*?)(?=^#{{{1},{level}}}\s|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    match = pattern.search(text)
    if match:
        return match.group(2)
    return ""


def _extract_between_markers(text: str) -> str:
    """Extract text between DISPUTES_BEGIN and DISPUTES_END markers."""
    begin = _DISPUTES_BEGIN.search(text)
    end = _DISPUTES_END.search(text)
    if begin and end and end.start() > begin.end():
        return text[begin.end():end.start()]
    return ""


def _count_section_items(text: str, heading: str) -> int:
    """Count bolded list items under a section heading."""
    section = _extract_section(text, heading)
    return len(_PD_SECTION_ITEMS.findall(section))


# ---------------------------------------------------------------------------
# Cooperative mode extraction
# ---------------------------------------------------------------------------

def _parse_dispositions(revision_text: str) -> dict[str, int]:
    """Parse disposition labels from a cooperative Phase 3 revision.

    Returns dict with keys: withdrawn, modified, surviving.
    """
    counts = {"withdrawn": 0, "modified": 0, "surviving": 0}

    # Try structured disposition labels first
    for match in _DISPOSITION_PATTERN.finditer(revision_text):
        label = match.group(1).lower().strip()
        if label in counts:
            counts[label] += 1

    # If nothing found, try standalone labels
    if sum(counts.values()) == 0:
        for match in _STANDALONE_DISPOSITION.finditer(revision_text):
            raw = match.group(1).lower().strip()
            if "withdrawn" in raw:
                counts["withdrawn"] += 1
            elif "modified" in raw:
                counts["modified"] += 1
            elif "surviving" in raw:
                counts["surviving"] += 1

    return counts


def _build_position_vector(revision_text: str, rec_count: int) -> list[int]:
    """Build position vector from Phase 3 dispositions.

    P1=3, P2=2, P3=1, Withdrawn=0.  When priority is not detectable,
    Surviving defaults to 2, Modified to 1.
    """
    vector: list[int] = []

    # Split into recommendation sections
    sections = re.split(
        r"(?:^|\n)(?:####?\s+Recommendation\s+\d+|^###?\s+P\d+-\d+)",
        revision_text,
        flags=re.IGNORECASE,
    )

    for section in sections[1:]:  # skip preamble before first recommendation
        # Determine disposition
        disp_match = _DISPOSITION_PATTERN.search(section)
        standalone_match = _STANDALONE_DISPOSITION.search(section)

        disposition = ""
        if disp_match:
            disposition = disp_match.group(1).lower()
        elif standalone_match:
            raw = standalone_match.group(1).lower()
            if "withdrawn" in raw:
                disposition = "withdrawn"
            elif "modified" in raw:
                disposition = "modified"
            elif "surviving" in raw:
                disposition = "surviving"

        if disposition == "withdrawn":
            vector.append(0)
        elif disposition == "modified":
            # Try to find priority
            pri_match = _PRIORITY_PATTERN.search(section)
            if pri_match:
                level = int(pri_match.group(1)[1])
                vector.append(max(0, 4 - level))  # P1=3, P2=2, P3=1
            else:
                vector.append(1)
        elif disposition == "surviving":
            pri_match = _PRIORITY_PATTERN.search(section)
            if pri_match:
                level = int(pri_match.group(1)[1])
                vector.append(max(0, 4 - level))
            else:
                vector.append(2)
        else:
            # Unknown disposition -- default to 1
            vector.append(1)

    # Pad or trim to match recommendation count
    while len(vector) < rec_count:
        vector.append(0)
    vector = vector[:rec_count] if rec_count > 0 else vector

    return vector


def _count_recommendations(review_text: str) -> int:
    """Count numbered recommendations in Phase 1 review."""
    section = _extract_section(review_text, "### Actionable Recommendations")
    if section:
        return len(_RECOMMENDATION_NUMBERED.findall(section))
    # Fallback: count any numbered list items in the review
    return len(_RECOMMENDATION_NUMBERED.findall(review_text))


def _count_new_recommendations(revision_text: str) -> int:
    """Count new recommendations added in Phase 3 revision."""
    section = _extract_section(revision_text, "### New Recommendations")
    if not section:
        section = _extract_section(revision_text, "## New Recommendations")
    if not section:
        return 0
    # Check for "No new recommendations" text
    if re.search(r"no new recommendations", section, re.IGNORECASE):
        return 0
    return len(_NEW_REC_ITEM.findall(section))


def _extract_cooperative_agent_features(
    agent_name: str,
    agent_dir: Path,
) -> tuple[AgentFeatures, int]:
    """Extract cooperative features for a single agent."""
    review_text = _read_file(agent_dir / "review.md")
    revision_text = _read_file(agent_dir / "revision.md")
    disputes_text = _read_file(agent_dir / "disputes.md")

    rec_count = _count_recommendations(review_text)
    dispositions = _parse_dispositions(revision_text)
    position_vector = _build_position_vector(revision_text, rec_count)
    new_recs = _count_new_recommendations(revision_text)

    total = dispositions["withdrawn"] + dispositions["modified"] + dispositions["surviving"]
    concession_rate = 0.0
    if total > 0:
        concession_rate = (dispositions["withdrawn"] + dispositions["modified"]) / total

    # Count convergence entries from this agent's disputes
    convergence_count = len(_CONVERGENCE_ENTRY.findall(disputes_text))

    return AgentFeatures(
        agent_name=agent_name,
        recommendation_count=rec_count,
        position_vector=position_vector,
        concession_rate=round(concession_rate, 4),
        withdrawn_count=dispositions["withdrawn"],
        modified_count=dispositions["modified"],
        surviving_count=dispositions["surviving"],
        new_recommendation_count=new_recs,
    ), convergence_count


def _count_disputes_from_synthesis(synthesis_text: str) -> int:
    """Count disputes in Phase 5 synthesis using structural markers or fallback."""
    # Primary: DISPUTES_BEGIN / DISPUTES_END markers
    disputes_section = _extract_between_markers(synthesis_text)
    if disputes_section:
        # Count dispute entries within markers
        count = len(_DISPUTE_ENTRY.findall(disputes_section))
        if count == 0:
            # Try heading-based counting within markers
            count = len(_DISPUTE_HEADING.findall(disputes_section))
        if count == 0:
            # Try any bolded list items
            count = len(_PD_SECTION_ITEMS.findall(disputes_section))
        # Check for "no remaining disputes" type text
        if re.search(
            r"no\s+remaining\s+disputes|no\s+disputes|verdict\s+is\s+decisive",
            disputes_section,
            re.IGNORECASE,
        ):
            return 0
        return count

    # Fallback: heading-based (FR-002)
    section = _extract_section(synthesis_text, "### Remaining Disputes")
    if not section:
        section = _extract_section(synthesis_text, "## Remaining Disputes")
    if section:
        count = len(_DISPUTE_ENTRY.findall(section))
        if count == 0:
            count = len(_DISPUTE_HEADING.findall(section))
        return count

    return 0


def _build_agreement_matrix(
    output_dir: Path,
    agent_names: list[str],
) -> dict[str, dict[str, int]]:
    """Build pairwise agreement matrix from Phase 2 cross-reviews.

    Matrix[reviewer][reviewed] = count of safe agreements listed.
    """
    matrix: dict[str, dict[str, int]] = {}
    for reviewer in agent_names:
        matrix[reviewer] = {}
        cross_review_dir = output_dir / reviewer / "cross-reviews"
        for reviewed in agent_names:
            if reviewer == reviewed:
                matrix[reviewer][reviewed] = 0
                continue
            cr_path = cross_review_dir / f"{reviewed}.md"
            cr_text = _read_file(cr_path)
            section = _extract_section(cr_text, "### Safe Agreements")
            if not section:
                section = _extract_section(cr_text, "## Safe Agreements")
            agreement_count = len(_SAFE_AGREEMENT.findall(section)) if section else 0
            matrix[reviewer][reviewed] = agreement_count
    return matrix


def _normalize_position_vectors(
    agent_features: dict[str, AgentFeatures],
) -> dict[str, AgentFeatures]:
    """Pad all agents' position vectors to the same length with 0s.

    This ensures position vectors are comparable across agents even when
    agents have different numbers of recommendations (FR-015 P1 fix).
    """
    if not agent_features:
        return agent_features

    max_len = max(
        len(af.position_vector) for af in agent_features.values()
    )
    if max_len == 0:
        return agent_features

    normalized: dict[str, AgentFeatures] = {}
    for name, af in agent_features.items():
        vec = af.position_vector
        if len(vec) < max_len:
            padded = list(vec) + [0] * (max_len - len(vec))
            # Reconstruct with padded vector (frozen model)
            data = af.model_dump()
            data["position_vector"] = padded
            normalized[name] = AgentFeatures.model_validate(data)
        else:
            normalized[name] = af
    return normalized


def _extract_cooperative_features(
    output_dir: Path,
    agent_names: list[str],
) -> RoundFeatures:
    """Extract all cooperative mode features for a single round."""
    agent_features: dict[str, AgentFeatures] = {}
    total_convergence = 0

    for name in agent_names:
        agent_dir = output_dir / name
        features, convergence = _extract_cooperative_agent_features(name, agent_dir)
        agent_features[name] = features
        total_convergence += convergence

    # Normalize position vector lengths across agents
    agent_features = _normalize_position_vectors(agent_features)

    # Synthesis-level features
    synthesis_text = _read_file(output_dir / "summary" / "final.md")
    dispute_count = _count_disputes_from_synthesis(synthesis_text)

    # Agreement matrix
    agreement_matrix = _build_agreement_matrix(output_dir, agent_names)

    return RoundFeatures(
        round_number=1,
        agent_features=agent_features,
        dispute_count=dispute_count,
        convergence_count=total_convergence,
        agreement_matrix=agreement_matrix,
    )


# ---------------------------------------------------------------------------
# Winner-take-all mode extraction
# ---------------------------------------------------------------------------

def _extract_wta_agent_features(
    agent_name: str,
    agent_dir: Path,
    synthesis_text: str,
) -> AgentFeatures:
    """Extract winner-take-all features for a single agent."""
    review_text = _read_file(agent_dir / "review.md")
    revision_text = _read_file(agent_dir / "revision.md")

    # Count rebutted/conceded from revision
    rebutted = len(_REBUTTED_SECTION.findall(revision_text))
    conceded = len(_CONCEDED_SECTION.findall(revision_text))

    # Extract criterion scores from synthesis per-agent scorecard
    criterion_scores: list[float] = []
    # Find this agent's scorecard section
    agent_section = _extract_section(synthesis_text, f"### {agent_name}")
    if not agent_section:
        # Try with different capitalization
        for heading_pattern in [f"### {agent_name}", f"## {agent_name}"]:
            agent_section = _extract_section(synthesis_text, heading_pattern)
            if agent_section:
                break
    if agent_section:
        for row_match in _CRITERION_SCORE_ROW.finditer(agent_section):
            try:
                score = float(row_match.group(1))
                criterion_scores.append(score)
            except ValueError:
                pass

    # Determine ranking position
    ranking = 0
    # Check if winner
    winner_section = _extract_section(synthesis_text, "## Winner")
    if winner_section and agent_name.lower() in winner_section.lower():
        ranking = 1
    # Check if runner-up
    runner_section = _extract_section(synthesis_text, "## Runner-Up")
    if runner_section and agent_name.lower() in runner_section.lower():
        ranking = 2
    # Check eliminated
    if ranking == 0:
        elim_section = _extract_section(synthesis_text, "## Eliminated Competitors")
        if elim_section and agent_name.lower() in elim_section.lower():
            ranking = 3  # or higher if multiple eliminated

    return AgentFeatures(
        agent_name=agent_name,
        ranking_position=ranking,
        criterion_scores=criterion_scores,
        attacks_received=0,  # Would need synthesis parsing for accurate count
        attacks_rebutted=rebutted,
        attacks_conceded=conceded,
    )


def _extract_wta_features(
    output_dir: Path,
    agent_names: list[str],
) -> RoundFeatures:
    """Extract all winner-take-all mode features for a single round."""
    synthesis_text = _read_file(output_dir / "summary" / "final.md")

    agent_features: dict[str, AgentFeatures] = {}
    for name in agent_names:
        agent_dir = output_dir / name
        features = _extract_wta_agent_features(name, agent_dir, synthesis_text)
        agent_features[name] = features

    dispute_count = _count_disputes_from_synthesis(synthesis_text)

    # Score differential: difference between winner and runner-up total scores
    score_diff = 0.0
    winner_scores = []
    runner_scores = []
    for name, feats in agent_features.items():
        if feats.ranking_position == 1 and feats.criterion_scores:
            winner_scores = feats.criterion_scores
        elif feats.ranking_position == 2 and feats.criterion_scores:
            runner_scores = feats.criterion_scores
    if winner_scores and runner_scores:
        score_diff = sum(winner_scores) - sum(runner_scores)

    return RoundFeatures(
        round_number=1,
        agent_features=agent_features,
        dispute_count=dispute_count,
        score_differential=round(score_diff, 4),
    )


# ---------------------------------------------------------------------------
# Prisoners-dilemma mode extraction
# ---------------------------------------------------------------------------

def _extract_pd_agent_features(
    agent_name: str,
    agent_dir: Path,
) -> AgentFeatures:
    """Extract prisoners-dilemma features for a single agent."""
    review_text = _read_file(agent_dir / "review.md")
    revision_text = _read_file(agent_dir / "revision.md")

    # Phase 1: count declarations by section
    core_count = _count_section_items(review_text, "## Core Competencies")
    unique_count = _count_section_items(review_text, "## Unique Capabilities")
    shared_count = _count_section_items(review_text, "## Shared Territory")
    deferral_count = _count_section_items(review_text, "## Deferrals")

    # Phase 2 cross-reviews: count overreach/sandbagging flags received
    cr_dir = agent_dir / "cross-reviews"
    overreach_total = 0
    sandbagging_total = 0
    # Note: cross-reviews are written BY other agents ABOUT this agent
    # The cross-review dir inside agent_dir contains reviews this agent wrote
    # Flags AGAINST this agent are in other agents' cross-review dirs
    # We need the parent dir to find cross-reviews about this agent
    parent_dir = agent_dir.parent
    for other_dir in parent_dir.iterdir():
        if not other_dir.is_dir() or other_dir.name == agent_name:
            continue
        if other_dir.name in ("summary", "arbitration"):
            continue
        cr_file = other_dir / "cross-reviews" / f"{agent_name}.md"
        if cr_file.exists():
            cr_text = cr_file.read_text(encoding="utf-8")
            overreach_total += len(_OVERREACH_FLAG.findall(cr_text))
            sandbagging_total += len(_SANDBAGGING_FLAG.findall(cr_text))

    # Phase 3: accepted / rebutted from recalibration
    overreach_section = _extract_section(revision_text, "## Overreach Responses")
    overreach_accepted = len(_PD_ACCEPTED.findall(overreach_section)) if overreach_section else 0
    overreach_rebutted = len(_PD_REBUTTED.findall(overreach_section)) if overreach_section else 0

    return AgentFeatures(
        agent_name=agent_name,
        core_competency_count=core_count,
        unique_capability_count=unique_count,
        shared_territory_count=shared_count,
        deferral_count=deferral_count,
        overreach_count=overreach_total,
        overreach_accepted=overreach_accepted,
        overreach_rebutted=overreach_rebutted,
        sandbagging_count=sandbagging_total,
    )


def _extract_pd_features(
    output_dir: Path,
    agent_names: list[str],
) -> RoundFeatures:
    """Extract all prisoners-dilemma mode features for a single round."""
    agent_features: dict[str, AgentFeatures] = {}
    for name in agent_names:
        agent_dir = output_dir / name
        features = _extract_pd_agent_features(name, agent_dir)
        agent_features[name] = features

    synthesis_text = _read_file(output_dir / "summary" / "final.md")
    dispute_count = _count_disputes_from_synthesis(synthesis_text)

    # Boundary clarity: count high-confidence assignments in responsibility map
    boundary_clarity = len(_HIGH_CONFIDENCE.findall(synthesis_text))

    return RoundFeatures(
        round_number=1,
        agent_features=agent_features,
        dispute_count=dispute_count,
        boundary_clarity=boundary_clarity,
    )


# ---------------------------------------------------------------------------
# Red-blue mode extraction
# ---------------------------------------------------------------------------

def _extract_rb_agent_features(
    agent_name: str,
    agent_dir: Path,
    role: str | None = None,
) -> AgentFeatures:
    """Extract red-blue features for a single agent."""
    review_text = _read_file(agent_dir / "review.md")
    revision_text = _read_file(agent_dir / "revision.md")

    # Detect role from review text if not provided
    if role is None:
        if re.search(r"attack\s+surface|threat\s+catalog|red\s+team", review_text, re.IGNORECASE):
            role = "red"
        elif re.search(r"defense\s+brief|safeguards?\s+in\s+place|blue\s+team", review_text, re.IGNORECASE):
            role = "blue"

    severity_vector: list[int] = []
    threat_count = 0
    cascading_count = 0
    safeguard_count = 0
    limitation_count = 0
    mitigation_rate = 0.0

    severity_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}

    if role == "red":
        # Extract severity vector from Threat Catalog
        for match in _THREAT_ENTRY.finditer(review_text):
            sev = match.group(1).lower()
            severity_vector.append(severity_map.get(sev, 1))
            threat_count += 1

        # Fallback: count any severity labels in review
        if threat_count == 0:
            for match in _SEVERITY_PATTERN.finditer(review_text):
                sev = match.group(1).lower()
                severity_vector.append(severity_map.get(sev, 1))
                threat_count += 1

        # Cascading failures
        cascading_section = _extract_section(review_text, "### Cascading Failures")
        if cascading_section:
            cascading_count = len(_CASCADING_SCENARIO.findall(cascading_section))
            if cascading_count == 0:
                # Count bolded items
                cascading_count = len(_PD_SECTION_ITEMS.findall(cascading_section))

        # Red revision: count withdrawn attacks
        withdrawn_section = _extract_section(revision_text, "### Withdrawn Attacks")
        withdrawn = len(_RB_WITHDRAWN_ATTACK.findall(withdrawn_section)) if withdrawn_section else 0
        if threat_count > 0:
            mitigation_rate = round(withdrawn / threat_count, 4)

    elif role == "blue":
        # Safeguards count
        safeguard_section = _extract_section(review_text, "### Safeguards in Place")
        if safeguard_section:
            safeguard_count = len(_SAFEGUARD_ENTRY.findall(safeguard_section))
            if safeguard_count == 0:
                safeguard_count = len(_PD_SECTION_ITEMS.findall(safeguard_section))

        # Acknowledged limitations
        limitation_section = _extract_section(review_text, "### Acknowledged Limitations")
        if limitation_section:
            limitation_count = len(_PD_SECTION_ITEMS.findall(limitation_section))

        # Blue revision: count conceded vulnerabilities
        conceded_section = _extract_section(revision_text, "### Conceded Vulnerabilities")
        conceded = len(_PD_SECTION_ITEMS.findall(conceded_section)) if conceded_section else 0
        # Get total threats received (from all cross-reviews of this agent)
        parent_dir = agent_dir.parent
        total_threats = 0
        for other_dir in parent_dir.iterdir():
            if not other_dir.is_dir() or other_dir.name == agent_name:
                continue
            if other_dir.name in ("summary", "arbitration"):
                continue
            cr_file = other_dir / "cross-reviews" / f"{agent_name}.md"
            if cr_file.exists():
                cr_text = cr_file.read_text(encoding="utf-8")
                total_threats += len(_SEVERITY_PATTERN.findall(cr_text))
        if total_threats > 0:
            mitigation_rate = round(conceded / total_threats, 4)

    return AgentFeatures(
        agent_name=agent_name,
        role=role,
        severity_vector=severity_vector,
        threat_count=threat_count,
        cascading_failure_count=cascading_count,
        safeguard_count=safeguard_count,
        acknowledged_limitation_count=limitation_count,
        mitigation_rate=mitigation_rate,
    )


def _extract_rb_features(
    output_dir: Path,
    agent_names: list[str],
) -> RoundFeatures:
    """Extract all red-blue mode features for a single round."""
    agent_features: dict[str, AgentFeatures] = {}
    for name in agent_names:
        agent_dir = output_dir / name
        features = _extract_rb_agent_features(name, agent_dir)
        agent_features[name] = features

    synthesis_text = _read_file(output_dir / "summary" / "final.md")
    dispute_count = _count_disputes_from_synthesis(synthesis_text)

    # Count landed / mitigated / accepted from synthesis sections
    landed_section = _extract_section(synthesis_text, "### Landed Attacks")
    if not landed_section:
        landed_section = _extract_section(
            synthesis_text, "### Landed Attacks — Unmitigated Risks",
        )
    landed = len(_RISK_ENTRY.findall(landed_section)) if landed_section else 0

    mitigated_section = _extract_section(synthesis_text, "### Mitigated Attacks")
    if not mitigated_section:
        mitigated_section = _extract_section(
            synthesis_text, "### Mitigated Attacks — Risks Successfully Defended",
        )
    mitigated = len(_RISK_ENTRY.findall(mitigated_section)) if mitigated_section else 0

    accepted_section = _extract_section(synthesis_text, "### Accepted Risks")
    accepted = len(_RISK_ENTRY.findall(accepted_section)) if accepted_section else 0

    total_surface = landed + mitigated + accepted
    coverage = round(mitigated / total_surface, 4) if total_surface > 0 else 0.0

    return RoundFeatures(
        round_number=1,
        agent_features=agent_features,
        dispute_count=dispute_count,
        landed_attack_count=landed,
        mitigated_attack_count=mitigated,
        accepted_risk_count=accepted,
        coverage_score=coverage,
    )


# ---------------------------------------------------------------------------
# Agent name discovery
# ---------------------------------------------------------------------------

def _discover_agent_names(output_dir: Path) -> list[str]:
    """Discover agent names from the output directory structure.

    Agent directories are any subdirectory that is not 'summary' or
    'arbitration' and contains at least a review.md.
    """
    names: list[str] = []
    if not output_dir.is_dir():
        return names
    for child in sorted(output_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name in ("summary", "arbitration", "__pycache__"):
            continue
        if (child / "review.md").exists() or (child / "revision.md").exists():
            names.append(child.name)
    return names


# ---------------------------------------------------------------------------
# Multi-round detection
# ---------------------------------------------------------------------------

def _detect_rounds(output_dir: Path) -> list[Path]:
    """Detect round directories.  Returns [output_dir] for single-round runs.

    Multi-round output uses round-N/ subdirectories.
    """
    round_dirs = sorted(
        p for p in output_dir.iterdir()
        if p.is_dir() and re.match(r"round-\d+$", p.name)
    ) if output_dir.is_dir() else []

    if round_dirs:
        return round_dirs

    # Single-round: use output_dir itself
    return [output_dir]


# ---------------------------------------------------------------------------
# Public API (FR-011)
# ---------------------------------------------------------------------------

_MODE_EXTRACTORS = {
    "cooperative": _extract_cooperative_features,
    "winner-take-all": _extract_wta_features,
    "prisoners-dilemma": _extract_pd_features,
    "red-blue": _extract_rb_features,
}


def extract_features(
    output_dir: Path,
    mode: str,
    agent_names: list[str] | None = None,
) -> FeatureSet:
    """Extract feature vectors from a deliberator deliberation output directory.

    This is the primary entry point for the feature extraction pipeline (FR-011).
    The function is deterministic: same input directory and mode always produce
    the same FeatureSet (FR-001).

    Args:
        output_dir: Path to the deliberator output directory (e.g. specs/X/deliberator/).
        mode: Game theory mode string (cooperative, winner-take-all, etc.).
        agent_names: Optional explicit list of agent names.  When None, names
            are discovered from the directory structure.

    Returns:
        Validated FeatureSet containing per-round, per-agent feature vectors.

    Raises:
        ValueError: If mode is not valid.
        FileNotFoundError: If output_dir does not exist.
    """
    if mode not in VALID_MODES:
        raise ValueError(
            f"Invalid mode '{mode}'. Valid modes are: {sorted(VALID_MODES)}."
        )

    output_dir = Path(output_dir)
    if not output_dir.exists():
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")

    extractor = _MODE_EXTRACTORS[mode]
    round_dirs = _detect_rounds(output_dir)

    rounds: list[RoundFeatures] = []
    for i, round_dir in enumerate(round_dirs, start=1):
        names = agent_names or _discover_agent_names(round_dir)
        if not names:
            warnings.warn(
                f"No agents discovered in {round_dir}. Skipping round {i}.",
                stacklevel=2,
            )
            continue

        round_features = extractor(round_dir, names)
        # Override round number for multi-round
        if len(round_dirs) > 1:
            round_features = RoundFeatures(
                round_number=i,
                **{
                    k: v
                    for k, v in round_features.model_dump().items()
                    if k != "round_number"
                },
            )
        rounds.append(round_features)

    metadata: dict[str, Any] = {
        "output_dir": str(output_dir),
        "agent_count": len(agent_names or _discover_agent_names(output_dir)),
        "round_count": len(rounds),
    }

    return FeatureSet(
        mode=mode,
        rounds=rounds,
        metadata=metadata,
    )


def write_features(feature_set: FeatureSet, output_path: Path) -> None:
    """Write a FeatureSet to a JSON file (FR-008).

    The output is deterministic: same FeatureSet always produces the same
    bytes (sort_keys=True, consistent indent).
    """
    output_path = Path(output_path)
    data = feature_set.model_dump()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
