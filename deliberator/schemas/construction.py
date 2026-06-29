"""Guided objective function construction pipeline (spec 014).

Three-stage pipeline that turns a natural-language problem description into a
parameterized objective function:

  Stage 1 (deterministic): classify decision type, select template, extract
  explicit parameters, identify gaps.

  Stage 2 (interactive): fill parameter gaps via a pluggable GapFiller protocol.

  Stage 3 (deterministic): assemble and validate the objective function.

No solver logic, no LLM imports.  Stage 2 uses a GapFiller protocol — the
caller provides the implementation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Protocol, runtime_checkable

import yaml
from pydantic import BaseModel, Field, model_validator

from deliberator.schemas.objectives import (
    VALID_MODES,
    ConstraintTemplate,
    ObjectiveTemplate,
    ParameterDefinition,
)


# ---------------------------------------------------------------------------
# Sentinel for problem text read from stdin (FR-020)
# ---------------------------------------------------------------------------

PROBLEM_MD_STDIN: str = "<stdin>"


# ---------------------------------------------------------------------------
# General templates — candidates for ALL decision types (FR-018)
# ---------------------------------------------------------------------------

GENERAL_TEMPLATE_NAMES: frozenset[str] = frozenset({
    "weighted-sum",
    "general-linear",
    "general-quadratic",
    "lexicographic",
    "minimax",
})


# ---------------------------------------------------------------------------
# Decision Type (FR-001, FR-019)
# ---------------------------------------------------------------------------

class DecisionType(Enum):
    """Classification of problem descriptions into canonical decision types.

    Each member carries keyword patterns used for fallback classification when
    ``problem.md`` does not include an explicit Type field.
    """

    SELECTION = "SELECTION"
    INTEGRATION = "INTEGRATION"
    SCOPING = "SCOPING"
    STRESS_TEST = "STRESS_TEST"
    NEGOTIATION = "NEGOTIATION"
    RESOURCE_ALLOCATION = "RESOURCE_ALLOCATION"
    FAIR_DIVISION = "FAIR_DIVISION"
    MECHANISM_DESIGN = "MECHANISM_DESIGN"


# Keyword patterns for each decision type.  Compiled once.
_DECISION_TYPE_PATTERNS: dict[DecisionType, re.Pattern[str]] = {
    DecisionType.SELECTION: re.compile(
        r"choose\s+between|pick\s+one|select\s+one|A\s+vs\.?\s+B"
        r"|winner.take.all|compete|ranking|rank\s+|best\s+option"
        r"|which\s+(?:one|option)|choose\s+(?:the\s+)?best",
        re.IGNORECASE,
    ),
    DecisionType.INTEGRATION: re.compile(
        r"work\s+together|integrat|align|cooperat|consensus"
        r"|collaborat|combine|merge|joint|unified|agree",
        re.IGNORECASE,
    ),
    DecisionType.SCOPING: re.compile(
        r"who\s+owns|responsibilit|boundar|territor|scope"
        r"|ownership|delineat|partition|divid|domain",
        re.IGNORECASE,
    ),
    DecisionType.STRESS_TEST: re.compile(
        r"what\s+could\s+go\s+wrong|risk|adversar|stress.?test"
        r"|failure|worst.?case|threat|vulnerabilit|attack",
        re.IGNORECASE,
    ),
    DecisionType.NEGOTIATION: re.compile(
        r"negotiat|bargain|deal|contract\s+with|ZOPA|BATNA"
        r"|counter.?offer|mutual.?accept|terms\s+of|settle",
        re.IGNORECASE,
    ),
    DecisionType.RESOURCE_ALLOCATION: re.compile(
        r"\bresource.?allocat|distribut|budget|resource\s+pool|capacity"
        r"|headcount|assign\s+resource|fair\s+share",
        re.IGNORECASE,
    ),
    DecisionType.FAIR_DIVISION: re.compile(
        r"fair.?divis|envy.?free|valuat|split\s+fairly|cake.?cut"
        r"|proportional\s+share|subjective\s+value|divide\s+among",
        re.IGNORECASE,
    ),
    DecisionType.MECHANISM_DESIGN: re.compile(
        r"mechanism\s+design|incentive.?compat|truthful|auction\s+design"
        r"|VCG|game\s+the\s+system|rule\s+design|strategyproof",
        re.IGNORECASE,
    ),
}

# FR-018: decision type to mode mapping
_DECISION_TYPE_MODE: dict[DecisionType, str] = {
    DecisionType.SELECTION: "winner-take-all",
    DecisionType.INTEGRATION: "cooperative",
    DecisionType.SCOPING: "prisoners-dilemma",
    DecisionType.STRESS_TEST: "red-blue",
    DecisionType.NEGOTIATION: "negotiation",
    DecisionType.RESOURCE_ALLOCATION: "resource-allocation",
    DecisionType.FAIR_DIVISION: "fair-division",
    DecisionType.MECHANISM_DESIGN: "mechanism-design",
}


# ---------------------------------------------------------------------------
# GapFiller protocol (FR-022)
# ---------------------------------------------------------------------------

@runtime_checkable
class GapFiller(Protocol):
    """Protocol for filling parameter gaps in Stage 2.

    Implementations convert a plain-language question + context into a string
    answer that the pipeline maps to a typed parameter value.
    """

    def fill(self, question: str, context: str) -> str:
        """Return a string answer to *question* given *context*."""
        ...  # pragma: no cover


class InteractiveGapFiller:
    """GapFiller that prompts the user via ``input()`` (CLI / conversation use)."""

    def fill(self, question: str, context: str) -> str:
        """Prompt the user with the question and return their answer."""
        print(f"\n[Context] {context}")
        return input(f"{question}\n> ")


class NonInteractiveGapFiller:
    """GapFiller that refuses to fill gaps (FR-023).

    All parameters without defaults are reported as errors.
    """

    def fill(self, question: str, context: str) -> str:
        raise RuntimeError(
            f"Cannot fill parameter gap non-interactively. "
            f"Question: {question}"
        )


# ---------------------------------------------------------------------------
# TemplateSelector protocol (FR-003)
# ---------------------------------------------------------------------------

@runtime_checkable
class TemplateSelector(Protocol):
    """Protocol for selecting a template from a list of candidates.

    Implementations choose one ``ObjectiveTemplate`` from the candidate
    list produced by ``select_candidate_templates()``.
    """

    def select(
        self, candidates: list[ObjectiveTemplate], problem_text: str,
    ) -> ObjectiveTemplate:
        """Return the chosen template from *candidates* given *problem_text*."""
        ...  # pragma: no cover


class NonInteractiveTemplateSelector:
    """TemplateSelector that picks the first (highest-ranked) candidate.

    This preserves the existing default behaviour where ``candidates[0]``
    is used without user interaction.
    """

    def select(
        self, candidates: list[ObjectiveTemplate], problem_text: str,
    ) -> ObjectiveTemplate:
        """Return the first candidate."""
        return candidates[0]


class InteractiveTemplateSelector:
    """TemplateSelector that presents candidates and asks the user to choose."""

    def select(
        self, candidates: list[ObjectiveTemplate], problem_text: str,
    ) -> ObjectiveTemplate:
        """Present candidates to the user and return the chosen template."""
        if len(candidates) == 1:
            return candidates[0]

        print("\nCandidate templates:")
        for i, t in enumerate(candidates, 1):
            print(f"  {i}. {t.name} — {t.description[:60]}")

        while True:
            choice = input(f"Select a template (1-{len(candidates)}): ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(candidates):
                    return candidates[idx]
            except ValueError:
                pass
            print(f"  Invalid choice. Enter a number between 1 and {len(candidates)}.")


# ---------------------------------------------------------------------------
# Gap identification dataclasses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ParameterGap:
    """A single parameter that needs a value from the user."""

    name: str
    definition: ParameterDefinition
    gap_question: str


@dataclass(frozen=True)
class GapList:
    """Stage 1 output: categorised parameter gaps for a template."""

    gaps: list[ParameterGap] = field(default_factory=list)
    defaults: dict[str, Any] = field(default_factory=dict)
    deferred: dict[str, str] = field(default_factory=dict)
    explicit: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Source provenance model (FR-020)
# ---------------------------------------------------------------------------

_VALID_PROVENANCE_TAGS = {"explicit", "default", "gap_filled", "deferred"}


class SourceProvenance(BaseModel):
    """Provenance metadata for an assembled objective (FR-020).

    Tracks where the problem description came from and how each parameter
    value was obtained (explicit extraction, default, gap-filling, or
    deferred computation).
    """

    problem_md: str = Field(
        description=(
            "Path to the problem.md file that was parsed, or the "
            "sentinel ``PROBLEM_MD_STDIN`` when text was piped."
        ),
    )
    filled_by: dict[str, Literal["explicit", "default", "gap_filled", "deferred"]] = Field(
        default_factory=dict,
        description="Maps each parameter name to its provenance tag.",
    )


# ---------------------------------------------------------------------------
# Assembled Objective model (FR-020)
# ---------------------------------------------------------------------------

class AssembledObjective(BaseModel):
    """Validated output of the construction pipeline (FR-020).

    Represents a fully-parameterized objective function ready for plugin
    consumption or serialisation to ``objective.yml``.
    """

    template_name: str
    game_form: str
    mode: str
    parameters: dict[str, Any]
    constraints: list[str] = Field(default_factory=list)
    symbolic_form: str
    source: SourceProvenance

    @model_validator(mode="after")
    def validate_assembled(self) -> AssembledObjective:
        if self.mode not in VALID_MODES:
            raise ValueError(
                f"Invalid mode '{self.mode}'. "
                f"Valid modes are: {sorted(VALID_MODES)}."
            )
        # Every parameter must have a source entry
        for param_name in self.parameters:
            if param_name not in self.source.filled_by:
                raise ValueError(
                    f"Parameter '{param_name}' has no source entry. "
                    f"Each parameter must be tagged as 'explicit', 'default', "
                    f"'gap_filled', or 'deferred'."
                )
        return self


# ---------------------------------------------------------------------------
# Schema directory helpers
# ---------------------------------------------------------------------------

def _objective_functions_dir() -> Path:
    """Return ``schema/objective-functions/``.

    Uses ``deliberator.paths.resolve_package_path`` which works both when
    pip-installed (importlib.resources) and in the dev source tree.
    """
    from deliberator.paths import resolve_package_path

    return resolve_package_path("deliberator", "schema", "objective-functions")


# ---------------------------------------------------------------------------
# Template and constraint loading (FR-017)
# ---------------------------------------------------------------------------

def load_objective_templates(
    templates_dir: Path | None = None,
) -> dict[str, ObjectiveTemplate]:
    """Discover and validate all YAML templates in *templates_dir*.

    Args:
        templates_dir: Path to the objective-functions directory.  Defaults to
            the bundled ``schema/objective-functions/`` directory.

    Returns:
        Dict mapping template name to validated ``ObjectiveTemplate``.
    """
    if templates_dir is None:
        templates_dir = _objective_functions_dir()

    templates: dict[str, ObjectiveTemplate] = {}
    for yml_path in sorted(templates_dir.glob("*.yml")):
        with open(yml_path) as f:
            data = yaml.safe_load(f)
        template = ObjectiveTemplate.model_validate(data)
        templates[template.name] = template
    return templates


def load_constraint_templates(
    constraints_dir: Path | None = None,
) -> dict[str, ConstraintTemplate]:
    """Discover and validate all constraint YAML files in *constraints_dir*.

    Args:
        constraints_dir: Path to the constraints directory.  Defaults to
            ``schema/objective-functions/constraints/``.

    Returns:
        Dict mapping constraint name to validated ``ConstraintTemplate``.
    """
    if constraints_dir is None:
        constraints_dir = _objective_functions_dir() / "constraints"

    constraints: dict[str, ConstraintTemplate] = {}
    for yml_path in sorted(constraints_dir.glob("*.yml")):
        with open(yml_path) as f:
            data = yaml.safe_load(f)
        constraint = ConstraintTemplate.model_validate(data)
        constraints[constraint.name] = constraint
    return constraints


# ---------------------------------------------------------------------------
# Stage 1: Classification (FR-001, FR-019)
# ---------------------------------------------------------------------------

def classify_decision_type(
    problem_text: str,
    explicit_type: str | None = None,
) -> DecisionType:
    """Classify a problem description into a ``DecisionType``.

    Args:
        problem_text: The raw text of the problem description.
        explicit_type: An explicit type string (e.g. from ``problem.md``'s Type
            field).  When valid, used directly; keyword matching is fallback.

    Returns:
        The matched ``DecisionType``.

    Raises:
        ValueError: When no decision type can be determined.
    """
    # FR-019: explicit type takes precedence
    if explicit_type is not None:
        normalised = explicit_type.strip().upper().replace("-", "_").replace(" ", "_")
        try:
            return DecisionType(normalised)
        except ValueError:
            pass  # fall through to keyword matching

    # Keyword pattern matching
    scores: dict[DecisionType, int] = {}
    for dtype, pattern in _DECISION_TYPE_PATTERNS.items():
        matches = pattern.findall(problem_text)
        if matches:
            scores[dtype] = len(matches)

    if not scores:
        raise ValueError(
            "Cannot determine decision type from problem text. "
            "No keyword patterns matched for SELECTION, INTEGRATION, "
            "SCOPING, STRESS_TEST, NEGOTIATION, RESOURCE_ALLOCATION, "
            "FAIR_DIVISION, or MECHANISM_DESIGN. Provide an explicit type."
        )

    # Highest match count wins; ties broken by enum definition order
    return max(scores, key=lambda dt: (scores[dt], -list(DecisionType).index(dt)))


# ---------------------------------------------------------------------------
# Stage 1: Template selection (FR-002, FR-018)
# ---------------------------------------------------------------------------

def select_candidate_templates(
    decision_type: DecisionType,
    mode: str,
    templates: dict[str, ObjectiveTemplate],
    max_candidates: int = 3,
) -> list[ObjectiveTemplate]:
    """Select the top candidate templates for a decision type and mode.

    Mode-specific templates are ranked first, then general templates.

    Args:
        decision_type: The classified decision type.
        mode: The game-theory mode string (e.g. ``"cooperative"``).
        templates: All loaded objective templates.
        max_candidates: Maximum number of candidates to return (1-3).

    Returns:
        Sorted list of candidate ``ObjectiveTemplate`` instances (mode-specific
        first, general second), limited to *max_candidates*.
    """
    target_mode = _DECISION_TYPE_MODE.get(decision_type, mode)

    mode_specific: list[ObjectiveTemplate] = []
    general: list[ObjectiveTemplate] = []

    for template in templates.values():
        if target_mode not in template.mode_compatibility:
            continue
        if template.name in GENERAL_TEMPLATE_NAMES:
            general.append(template)
        else:
            mode_specific.append(template)

    # Rank mode-specific templates by relevance to decision type.
    # Templates whose name contains the decision type keyword rank first.
    _TYPE_KEYWORDS: dict[DecisionType, list[str]] = {
        DecisionType.SELECTION: ["competitive", "selection", "ranking"],
        DecisionType.INTEGRATION: ["cooperative", "integration", "consensus"],
        DecisionType.SCOPING: ["territory", "boundary", "claiming"],
        DecisionType.STRESS_TEST: ["risk", "adversarial", "coverage"],
        DecisionType.NEGOTIATION: ["negotiation", "bargaining", "deal"],
        DecisionType.RESOURCE_ALLOCATION: ["allocation", "resource", "budget"],
        DecisionType.FAIR_DIVISION: ["division", "envy-free", "valuation"],
        DecisionType.MECHANISM_DESIGN: ["mechanism", "incentive", "auction"],
    }
    keywords = _TYPE_KEYWORDS.get(decision_type, [])

    def _relevance_key(t: ObjectiveTemplate) -> tuple[int, str]:
        """Sort by keyword match (0=match, 1=no match), then alphabetically."""
        for kw in keywords:
            if kw in t.name:
                return (0, t.name)
        return (1, t.name)

    mode_specific.sort(key=_relevance_key)
    general.sort(key=lambda t: t.name)

    candidates = mode_specific + general
    return candidates[:max_candidates]


# ---------------------------------------------------------------------------
# Stage 1: Parameter extraction (FR-004)
# ---------------------------------------------------------------------------

# Pattern for extracting numeric values attached to parameter-like keywords
_NUMBER_PATTERN = re.compile(
    r"""
    (?:^|\s)                  # start or whitespace
    (?P<name>[a-zA-Z_]\w*)    # potential parameter name
    \s*(?:is|=|:)\s*          # separator: "is", "=", or ":"
    [$]?                      # optional dollar sign
    (?P<value>-?\d+(?:\.\d+)?)  # numeric value
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Pattern for "budget is $500" style (name may precede or follow value)
_BUDGET_PATTERN = re.compile(
    r"""
    [$](?P<value>\d+(?:\.\d+)?)  # dollar-prefixed value
    (?:\s*/\s*\w+)?              # optional /month, /year etc.
    """,
    re.VERBOSE,
)


def extract_explicit_parameters(
    problem_text: str,
    template: ObjectiveTemplate,
) -> dict[str, Any]:
    """Extract parameter values explicitly stated in the problem text.

    Conservative: only extracts clearly stated values where the problem text
    mentions a parameter name (or close alias) with a numeric value.

    Args:
        problem_text: The raw problem description text.
        template: The selected objective template.

    Returns:
        Dict mapping parameter name to extracted value.
    """
    extracted: dict[str, Any] = {}
    param_names = {p.name.lower(): p for p in template.parameters}

    # Try to match "name is/=/: value" patterns
    for match in _NUMBER_PATTERN.finditer(problem_text):
        name_candidate = match.group("name").lower()
        value_str = match.group("value")

        if name_candidate in param_names:
            param = param_names[name_candidate]
            value = _coerce_value(value_str, param.type)
            if value is not None and _value_in_range(value, param):
                extracted[param.name] = value

    # Look for budget/cost patterns when template has budget-like params
    for param in template.parameters:
        if param.name in extracted:
            continue
        if param.name.lower() in ("budget", "b", "cost", "budget_constraint"):
            for match in _BUDGET_PATTERN.finditer(problem_text):
                value_str = match.group("value")
                value = _coerce_value(value_str, param.type)
                if value is not None and _value_in_range(value, param):
                    extracted[param.name] = value
                    break

    return extracted


def _coerce_value(value_str: str, param_type: str) -> Any | None:
    """Attempt to coerce a string to the parameter's declared type."""
    try:
        if param_type == "float":
            return float(value_str)
        elif param_type == "integer":
            return int(float(value_str))
        elif param_type == "string":
            return value_str
        elif param_type == "boolean":
            lower = value_str.strip().lower()
            if lower in ("true", "yes", "1", "on"):
                return True
            elif lower in ("false", "no", "0", "off"):
                return False
            return None
        else:
            return None
    except (ValueError, TypeError):
        return None


def _value_in_range(value: Any, param: ParameterDefinition) -> bool:
    """Check whether *value* satisfies the parameter's range constraints."""
    if param.range is None:
        return True
    range_min = param.range.get("min")
    range_max = param.range.get("max")
    try:
        if range_min is not None and value < range_min:
            return False
        if range_max is not None and value > range_max:
            return False
    except TypeError:
        return True
    return True


# ---------------------------------------------------------------------------
# Stage 1: Gap identification
# ---------------------------------------------------------------------------

def identify_gaps(
    template: ObjectiveTemplate,
    explicit_params: dict[str, Any],
) -> GapList:
    """Identify which parameters still need values after extraction.

    Categories:
    - **explicit**: value was extracted from problem text.
    - **defaults**: parameter has a default value (user can accept or override).
    - **deferred**: function-type parameters with ``derived_from`` (FR-021).
    - **gaps**: everything else — needs interactive gap-filling.

    Returns:
        A ``GapList`` with all four categories populated.
    """
    gaps: list[ParameterGap] = []
    defaults: dict[str, Any] = {}
    deferred: dict[str, str] = {}
    explicit: dict[str, Any] = dict(explicit_params)

    for param in template.parameters:
        if param.name in explicit_params:
            continue

        # FR-021: function-type parameters are deferred
        if param.type == "function" and param.derived_from:
            deferred[param.name] = param.derived_from
            continue

        # Parameters with defaults
        if param.default is not None:
            defaults[param.name] = param.default
            continue

        # Remaining parameters are gaps
        question = param.gap_question or (
            f"What value should '{param.name}' have? "
            f"({param.description.strip()})"
        )
        gaps.append(ParameterGap(
            name=param.name,
            definition=param,
            gap_question=question,
        ))

    return GapList(
        gaps=gaps,
        defaults=defaults,
        deferred=deferred,
        explicit=explicit,
    )


# ---------------------------------------------------------------------------
# Stage 2: Gap filling (FR-005 through FR-008)
# ---------------------------------------------------------------------------

def fill_parameter_gaps(
    gap_list: GapList,
    template: ObjectiveTemplate,
    problem_context: str,
    filler: GapFiller,
    max_retries: int = 3,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Fill parameter gaps using the provided ``GapFiller``.

    For each gap, the filler is asked a contextualised question.  Answers are
    validated against the parameter's type and range constraints.

    For parameters with defaults (FR-008), the filler is asked whether the
    default is acceptable.

    Args:
        gap_list: The gap identification output from ``identify_gaps``.
        template: The objective template being parameterised.
        problem_context: A summary of the problem for contextualising questions.
        filler: A ``GapFiller`` implementation.
        max_retries: Number of retries on invalid answers before raising.

    Returns:
        Tuple of (filled_params, source_map) where filled_params maps parameter
        name to filled value, and source_map maps parameter name to provenance
        tag (``"explicit"``, ``"default"``, ``"gap_filled"``, ``"deferred"``).
    """
    filled: dict[str, Any] = dict(gap_list.explicit)
    source: dict[str, str] = {k: "explicit" for k in gap_list.explicit}

    # Deferred parameters (FR-021)
    for name, derived_from in gap_list.deferred.items():
        filled[name] = f"<deferred: {derived_from}>"
        source[name] = "deferred"

    # Parameters with defaults (FR-008)
    for name, default in gap_list.defaults.items():
        param_def = _find_param(template, name)
        question = (
            f"The default for '{name}' is {default!r}. "
            f"Is this acceptable, or would you like to adjust? "
            f"(press enter to accept, or provide a new value)"
        )
        try:
            answer = filler.fill(question, problem_context)
        except RuntimeError:
            # NonInteractiveGapFiller: use default
            filled[name] = default
            source[name] = "default"
            continue

        answer = answer.strip()
        if not answer:
            filled[name] = default
            source[name] = "default"
        else:
            value = _coerce_value(answer, param_def.type)
            if value is not None and _value_in_range(value, param_def):
                filled[name] = value
                source[name] = "gap_filled"
            else:
                filled[name] = default
                source[name] = "default"

    # True gaps — no default, must be filled
    for gap in gap_list.gaps:
        value = _fill_single_gap(gap, problem_context, filler, max_retries)
        filled[gap.name] = value
        source[gap.name] = "gap_filled"

    return filled, source


def _fill_single_gap(
    gap: ParameterGap,
    problem_context: str,
    filler: GapFiller,
    max_retries: int,
) -> Any:
    """Fill a single parameter gap, retrying on invalid answers (FR-007)."""
    param = gap.definition
    for attempt in range(max_retries):
        answer = filler.fill(gap.gap_question, problem_context)
        answer = answer.strip()

        value = _coerce_value(answer, param.type)
        if value is not None and _value_in_range(value, param):
            return value

        # Build guidance message for retry
        guidance_parts = [f"Could not map '{answer}' to a valid {param.type} value."]
        if param.range:
            range_min = param.range.get("min")
            range_max = param.range.get("max")
            if range_min is not None and range_max is not None:
                guidance_parts.append(
                    f"Value must be between {range_min} and {range_max}."
                )
            elif range_min is not None:
                guidance_parts.append(f"Value must be >= {range_min}.")
            elif range_max is not None:
                guidance_parts.append(f"Value must be <= {range_max}.")
        # For string type, any non-empty answer is accepted
        if param.type == "string" and answer:
            return answer

    raise ValueError(
        f"Failed to fill parameter '{gap.name}' after {max_retries} attempts. "
        f"Last answer: '{answer}'"
    )


def _find_param(template: ObjectiveTemplate, name: str) -> ParameterDefinition:
    """Find a parameter definition by name within a template."""
    for p in template.parameters:
        if p.name == name:
            return p
    raise KeyError(f"Parameter '{name}' not found in template '{template.name}'.")


# ---------------------------------------------------------------------------
# Stage 3: Assembly (FR-010 through FR-012)
# ---------------------------------------------------------------------------

def assemble_objective(
    template: ObjectiveTemplate,
    filled_params: dict[str, Any],
    source_map: dict[str, str] | None,
    constraints: list[str] | None = None,
    mode: str | None = None,
    problem_md: str = PROBLEM_MD_STDIN,
) -> AssembledObjective:
    """Assemble and validate the final objective function (FR-010).

    Args:
        template: The selected objective template.
        filled_params: All parameter values (explicit + default + gap-filled +
            deferred).
        source_map: Dict mapping parameter name to provenance string.
        constraints: Constraint names to attach.  Defaults to the template's
            constraint list.
        mode: The game mode.  Defaults to the first entry in the template's
            ``mode_compatibility``.
        problem_md: Path to the source problem.md or ``PROBLEM_MD_STDIN``.

    Returns:
        Validated ``AssembledObjective``.
    """
    if constraints is None:
        constraints = list(template.constraints)
    if mode is None:
        mode = template.mode_compatibility[0]

    # Build source dict from the gap-filling process
    if source_map is None:
        source_map = {k: "explicit" for k in filled_params}

    # FR-012: deterministic symbolic form — substitute known values
    symbolic_form = _substitute_symbolic_form(template.form, filled_params)

    provenance = SourceProvenance(
        problem_md=problem_md,
        filled_by=source_map,  # type: ignore[arg-type]
    )

    return AssembledObjective(
        template_name=template.name,
        game_form=template.game_form,
        mode=mode,
        parameters=filled_params,
        constraints=constraints,
        symbolic_form=symbolic_form,
        source=provenance,
    )


def _substitute_symbolic_form(
    form: str,
    params: dict[str, Any],
) -> str:
    """Substitute known parameter values into the symbolic form string.

    Only substitutes non-deferred values.  Deferred placeholders are left
    as-is so the symbolic form remains readable.

    Uses word-boundary-aware regex to prevent substring collisions (e.g.,
    parameter ``w`` corrupting ``overlap`` into ``o2.0erlap``).
    """
    result = form
    # Sort by length descending so longer names match first
    for name, value in sorted(params.items(), key=lambda kv: -len(kv[0])):
        # Skip deferred placeholders
        if isinstance(value, str) and value.startswith("<deferred:"):
            continue
        # Use word boundary to prevent substring collisions
        result = re.sub(rf"\b{re.escape(name)}\b", str(value), result)
    return result


# ---------------------------------------------------------------------------
# Top-level orchestrator
# ---------------------------------------------------------------------------

def construct_objective(
    problem_text: str,
    mode: str | None = None,
    templates_dir: Path | None = None,
    constraints_dir: Path | None = None,
    filler: GapFiller | None = None,
    explicit_type: str | None = None,
    output_path: Path | None = None,
    template_selector: TemplateSelector | None = None,
    problem_md: str = PROBLEM_MD_STDIN,
) -> AssembledObjective:
    """Run the full 3-stage construction pipeline.

    Args:
        problem_text: Raw text of the problem description (``problem.md``).
        mode: Game mode override.  When ``None``, derived from decision type.
        templates_dir: Path to objective-function templates.
        constraints_dir: Path to constraint templates.
        filler: A ``GapFiller`` implementation.  Defaults to
            ``NonInteractiveGapFiller`` (fails on gaps without defaults).
        explicit_type: Explicit decision type override.
        output_path: Where to write ``objective.yml``.  When ``None``, the
            assembled objective is returned without writing.
        template_selector: A ``TemplateSelector`` implementation for choosing
            among candidate templates.  Defaults to
            ``NonInteractiveTemplateSelector`` (picks first candidate).
        problem_md: Path to the source problem.md or ``PROBLEM_MD_STDIN``.

    Returns:
        The validated ``AssembledObjective``.
    """
    if filler is None:
        filler = NonInteractiveGapFiller()
    if template_selector is None:
        template_selector = NonInteractiveTemplateSelector()

    # --- Stage 1 ---
    decision_type = classify_decision_type(problem_text, explicit_type)

    if mode is None:
        mode = _DECISION_TYPE_MODE[decision_type]

    templates = load_objective_templates(templates_dir)
    candidates = select_candidate_templates(decision_type, mode, templates)

    if not candidates:
        raise ValueError(
            f"No candidate templates found for decision type "
            f"{decision_type.value} and mode '{mode}'."
        )

    # Use the TemplateSelector to choose from candidates
    template = template_selector.select(candidates, problem_text)

    explicit_params = extract_explicit_parameters(problem_text, template)
    gap_list = identify_gaps(template, explicit_params)

    # --- Stage 2 ---
    filled_params, source_map = fill_parameter_gaps(
        gap_list, template, problem_text, filler,
    )

    # --- Stage 3 ---
    objective = assemble_objective(
        template=template,
        filled_params=filled_params,
        source_map=source_map,
        mode=mode,
        problem_md=problem_md,
    )

    # Write objective.yml if output_path is given
    if output_path is not None:
        data = objective.model_dump()
        with open(output_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    return objective
