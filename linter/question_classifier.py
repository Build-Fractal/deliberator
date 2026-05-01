"""
Heuristic question classifier for conversus deliberation input.

Evaluates whether a user's input question is sufficient for multi-agent
deliberation. Supports two modes:

- **interactive**: Returns one focused clarification question when input
  is insufficient.
- **non-interactive**: Returns a structured error listing missing fields
  when input is insufficient.

The classifier is heuristic-based — no LLM call required. This keeps it
fast for MCP validation (S05's conversus_validate imports classify_question)
and suitable for the M001 prototype.

Public API:
    classify_question(question, mode) -> ClassificationResult

Models:
    ClassificationResult — classification verdict with reason and guidance

Usage:
    from linter.question_classifier import classify_question

    result = classify_question("Should I use React or Vue?", mode="interactive")
    if not result.sufficient:
        print(result.clarification_question)

CLI:
    python3 -m linter.question_classifier "help me decide" --mode non-interactive
    # Exits 0 if sufficient, 1 if insufficient
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel

from conversus.schemas.duration import TemporalMatch, parse_temporal
from linter.utils import word_count as _word_count


# ---------------------------------------------------------------------------
# Pydantic model — frozen per Constitution Principle IX
# ---------------------------------------------------------------------------


class ClassificationResult(BaseModel):
    """Result of classifying a question for deliberation sufficiency.

    Fields:
        sufficient: Whether the question is suitable for multi-agent deliberation.
        reason: Human-readable explanation of the classification.
        clarification_question: A focused follow-up question to improve input
            (interactive mode only; None when sufficient or non-interactive).
        missing_fields: List of what the input lacks for deliberation
            (non-interactive mode only; None when sufficient or interactive).
    """

    model_config = {"frozen": True}

    sufficient: bool
    reason: str
    clarification_question: str | None
    missing_fields: list[str] | None


# ---------------------------------------------------------------------------
# Heuristic constants
# ---------------------------------------------------------------------------

# Words that signal a decision or trade-off context
_DECISION_WORDS: frozenset[str] = frozenset({
    "should", "whether", "trade-off", "tradeoff", "trade", "compare",
    "choose", "decide", "better", "pros", "cons", "advantage",
    "disadvantage", "benefit", "drawback", "recommend", "prefer",
    "alternative", "option", "evaluate", "assess", "weigh", "advice",
})

# Patterns that signal alternatives are being compared
_ALTERNATIVE_PATTERN: re.Pattern[str] = re.compile(
    r"\b(?:vs\.?|versus|or)\b", re.IGNORECASE
)

# Factual question starters — questions likely to have a single correct answer
_FACTUAL_STARTERS: re.Pattern[str] = re.compile(
    r"^\s*(?:"
    r"what\s+is\s+the\b|"
    r"what\s+are\s+the\b|"
    r"what\s+was\s+the\b|"
    r"who\s+(?:is|was|invented|discovered|created|founded|wrote)\b|"
    r"when\s+(?:did|was|is|were)\b|"
    r"where\s+(?:is|was|are|were)\b|"
    r"how\s+(?:many|much|old|long|tall|far)\b|"
    r"define\b|"
    r"what\s+does\s+\S+\s+mean\b|"
    r"name\s+the\b"
    r")",
    re.IGNORECASE,
)

# Non-temporal constraint/context indicators — signals real-world context
# *other than* temporal references. Temporal detection now lives in
# `conversus.schemas.duration.parse_temporal` (spec 047, FR-011).
_NON_TEMPORAL_PATTERN: re.Pattern[str] = re.compile(
    r"\b(?:"
    r"team|budget|timeline|deadline|constraint|requirement|"
    r"given|considering|assuming|because|since|"
    r"person|people|employee|member|"
    r"\$\d|€\d|£\d|\d+k\b|\d+\s*(?:miles?|km)|"
    r"remote|in-office|hybrid|"
    r"service|microservice|monolith|"
    r"project|company|startup|enterprise"
    r")\b",
    re.IGNORECASE,
)

# Temporal categories that imply a planning constraint — used by
# has_constraints(). "duration" alone is too weak to count as a constraint
# (e.g. a bare "3 months" without context).
_CONSTRAINT_TEMPORAL_CATEGORIES: frozenset[str] = frozenset(
    {"deadline", "ttl", "window", "latency_bound"}
)

# Backward-compat fallback (FR-009): the old regex flagged temporal
# keywords without category disambiguation. The new structured parser
# may label some of those as bare "duration" rather than a constraint
# category. This permissive whitelist preserves the original boolean
# output for inputs like "what should I do about my career in 6 months".
_TEMPORAL_KEYWORD_FALLBACK: re.Pattern[str] = re.compile(
    r"\b(?:months?|years?|weeks?|days?|hours?|minutes?|seconds?|deadline)\b",
    re.IGNORECASE,
)

# Minimum word count for sufficient questions
_MIN_SUFFICIENT_WORDS: int = 10

# Maximum word count for factual detection (long questions are rarely factual lookups)
_MAX_FACTUAL_WORDS: int = 20

# Minimum word count to pass the "not too short" check
_MIN_WORDS: int = 5


# ---------------------------------------------------------------------------
# Heuristic helpers
# ---------------------------------------------------------------------------


def _has_decision_words(text: str) -> bool:
    """Check if text contains any decision/trade-off vocabulary."""
    words = set(re.findall(r"[a-z\-]+", text.lower()))
    return bool(words & _DECISION_WORDS)


def _has_alternatives(text: str) -> bool:
    """Check if text mentions alternatives (or, vs, versus)."""
    return bool(_ALTERNATIVE_PATTERN.search(text))


def _has_constraints(text: str) -> bool:
    """Check if text includes real-world constraints or context.

    Combines non-temporal pattern detection with the structured temporal
    parser (spec 047). Returns True when:

    * the non-temporal pattern matches (team/budget/people/etc.), OR
    * the structured parser yields a match in a constraint-implying
      category (deadline, ttl, window, latency_bound), OR
    * the legacy temporal keyword fallback matches (FR-009 backward
      compatibility — preserves boolean behaviour for inputs the old
      regex flagged, even when the structured parser only labels them
      as bare "duration").
    """
    if _NON_TEMPORAL_PATTERN.search(text):
        return True
    matches = parse_temporal(text)
    if any(m.category in _CONSTRAINT_TEMPORAL_CATEGORIES for m in matches):
        return True
    if matches and _TEMPORAL_KEYWORD_FALLBACK.search(text):
        return True
    return False


def has_constraints(text: str) -> bool:
    """Public boolean API — preserved for backward compatibility (FR-009)."""
    return _has_constraints(text)


def extract_temporal_constraints(text: str) -> list[TemporalMatch]:
    """Return structured temporal matches found in *text* (FR-010).

    Wraps :func:`conversus.schemas.duration.parse_temporal` so callers in
    the linter layer can avoid importing across packages.
    """
    return parse_temporal(text)


def _is_factual(text: str) -> bool:
    """Detect pure factual questions with a single definitive answer.

    A question is classified as factual when:
    1. It starts with a factual-answer indicator (What is, Who invented, etc.)
    2. It is short (< 20 words) — long questions are rarely simple lookups
    3. It does NOT contain decision/comparison vocabulary
    """
    if not _FACTUAL_STARTERS.search(text):
        return False
    if _word_count(text) >= _MAX_FACTUAL_WORDS:
        return False
    if _has_decision_words(text) or _has_alternatives(text):
        return False
    return True


# ---------------------------------------------------------------------------
# Main classifier
# ---------------------------------------------------------------------------


def classify_question(
    question: str,
    mode: Literal["interactive", "non-interactive"] = "interactive",
) -> ClassificationResult:
    """Classify whether a question is sufficient for multi-agent deliberation.

    Applies heuristic rules in priority order:
    1. Pure factual lookup — insufficient for deliberation
    2. Empty/trivially short — insufficient
    3. Sufficient decision structure — sufficient
    4. Too vague (no decision structure) — insufficient with guidance

    Args:
        question: The user's input question.
        mode: "interactive" returns a clarification question,
              "non-interactive" returns missing_fields list.

    Returns:
        ClassificationResult with classification verdict and guidance.
    """
    stripped = question.strip() if question else ""
    words = _word_count(stripped) if stripped else 0

    # --- Rule 1: Pure factual question (checked first to catch short factual queries) ---
    if stripped and _is_factual(stripped):
        return ClassificationResult(
            sufficient=False,
            reason=(
                "This appears to be a factual question with a single correct "
                "answer. Multi-agent deliberation works best for decisions "
                "and trade-offs."
            ),
            clarification_question=(
                "Could you reframe this as a decision or trade-off? For "
                "example, instead of a factual lookup, describe the competing "
                "options or constraints you're weighing."
                if mode == "interactive"
                else None
            ),
            missing_fields=(
                ["a decision or trade-off (not a factual lookup)"]
                if mode == "non-interactive"
                else None
            ),
        )

    # --- Rule 2: Empty or trivially short ---
    # Inputs under 5 words that lack genuine deliberation framing are too short.
    # Inputs with 3+ words that express deliberation intent (decision word + first-person
    # or question framing, e.g., "help me decide", "I need advice") pass through
    # to the vague heuristic for better guidance. Bare imperatives like "decide for me"
    # stay in the short bucket.
    _has_deliberation_framing = (
        stripped
        and _has_decision_words(stripped)
        and words >= 3
        and bool(re.search(r"\b(?:I|my|me|we|our|help|should|what|how)\b", stripped, re.IGNORECASE))
    )
    if words < _MIN_WORDS and not _has_deliberation_framing:
        return ClassificationResult(
            sufficient=False,
            reason="Question is too short to support meaningful deliberation.",
            clarification_question=(
                "What specific decision or trade-off are you trying to evaluate?"
                if mode == "interactive"
                else None
            ),
            missing_fields=(
                ["a complete question with enough context for analysis"]
                if mode == "non-interactive"
                else None
            ),
        )

    # --- Rule 3: Check for sufficient decision structure ---
    has_decision = _has_decision_words(stripped)
    has_alts = _has_alternatives(stripped)
    has_context = _has_constraints(stripped)

    # Sufficient: has decision/trade-off language OR alternatives,
    # AND at least 10 words of substantive content
    if (has_decision or has_alts) and words >= _MIN_SUFFICIENT_WORDS:
        return ClassificationResult(
            sufficient=True,
            reason="Question is suitable for multi-agent deliberation.",
            clarification_question=None,
            missing_fields=None,
        )

    # --- Rule 4: Too vague — has some words but lacks decision structure ---
    missing: list[str] = []
    if not has_alts and not has_decision:
        missing.append("the specific options being considered")
    if not has_context:
        missing.append("relevant constraints or context")
    if words < _MIN_SUFFICIENT_WORDS:
        missing.append("more detail about the situation")

    # If we somehow have nothing missing but didn't pass sufficiency,
    # add a generic missing field
    if not missing:
        missing.append("clearer framing as a decision or trade-off")

    # Build a focused clarification question for interactive mode
    clarification: str | None = None
    if mode == "interactive":
        if not has_alts and not has_decision:
            clarification = (
                "What specific options or alternatives are you considering?"
            )
        elif not has_context:
            clarification = (
                "What constraints or context should the analysis consider "
                "(e.g., team size, budget, timeline)?"
            )
        elif words < _MIN_SUFFICIENT_WORDS:
            clarification = (
                "Could you provide more detail about the situation and "
                "what you're trying to decide?"
            )
        else:
            clarification = (
                "Could you describe the specific trade-off or decision "
                "you're trying to evaluate?"
            )

    return ClassificationResult(
        sufficient=False,
        reason="The question lacks enough context for a structured deliberation.",
        clarification_question=clarification if mode == "interactive" else None,
        missing_fields=missing if mode == "non-interactive" else None,
    )


# ---------------------------------------------------------------------------
# CLI entry point — invoked via `python3 -m linter.question_classifier`
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Conversus question classifier. "
        "Evaluates whether input is sufficient for multi-agent deliberation. "
        "Exits 0 if sufficient, 1 if insufficient.",
    )
    parser.add_argument(
        "question",
        help="The question to classify.",
    )
    parser.add_argument(
        "--mode",
        choices=["interactive", "non-interactive"],
        default="interactive",
        help="Classification mode (default: interactive).",
    )
    args = parser.parse_args()

    result = classify_question(args.question, mode=args.mode)
    print(result.model_dump_json(indent=2))
    sys.exit(0 if result.sufficient else 1)
