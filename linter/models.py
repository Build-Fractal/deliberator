"""
Pydantic models for deliberator template variable typing.

These models enforce type safety at two levels:
1. Schema validation — structure of variables.yml and modes/*.yml (used by linter)
2. Value validation — runtime values populated by the orchestrator (used at execution time)

Constitution Principle IX mandates: ALL data structures MUST use Pydantic models
for validation and type safety. Raw dicts from YAML/JSON parsing MUST be loaded
into typed Pydantic models before use.
"""

from enum import StrEnum
from pathlib import Path
from typing import Annotated, Optional, Union

from pydantic import BaseModel, BeforeValidator, Field, PlainSerializer, field_validator


# ---------------------------------------------------------------------------
# Behavioral enums — closed sets with distinct code paths per value
# ---------------------------------------------------------------------------

class InfluenceLevel(StrEnum):
    """Arbiter influence level — controls authority of arbiter positions.

    Each value triggers different template language, dispute counting,
    and heading validation. Plugins may extend via factory function
    that produces a new StrEnum with additional members.
    """
    BINDING = "binding"
    RECOMMENDED = "recommended"
    ADVISORY = "advisory"


class ArbiterTiming(StrEnum):
    """When the arbiter intervenes in the deliberation.

    FINAL: arbiter rules once after all rounds complete.
    INTER_ROUND: arbiter rules between rounds, feeding decisions into next round.
    """
    FINAL = "final"
    INTER_ROUND = "inter-round"


# ---------------------------------------------------------------------------
# Custom types
# ---------------------------------------------------------------------------

def _parse_path_list(v: str | list[Path]) -> list[Path]:
    """Parse a newline-separated string into a list of Paths, or pass through a list."""
    if isinstance(v, list):
        return v
    return [Path(p) for p in v.strip().split("\n") if p.strip()]


def _serialize_path_list(v: list[Path]) -> str:
    """Serialize a list of Paths back to a newline-separated string for template substitution."""
    return "\n".join(str(p) for p in v)


PathList = Annotated[list[Path], BeforeValidator(_parse_path_list), PlainSerializer(_serialize_path_list)]


# ---------------------------------------------------------------------------
# Schema-level models (validate the structure of YAML schema files)
# ---------------------------------------------------------------------------

# Open registry — types are schema metadata with no per-value branching logic.
# New types can be added without code changes (e.g., "float" for spec 007).
VALID_VARIABLE_TYPES: frozenset[str] = frozenset({
    "string", "integer", "path", "path-list",
    "conditional-block", "extracted-content",
})


class Phase(StrEnum):
    """Deliberation phases — each has its own template, context model, and variable set.

    Closed behavioral enum: adding a phase requires a new TemplateContext
    subclass, a new template file per mode, and orchestrator logic changes.
    """
    REVIEW = "review"
    CROSS_REVIEW = "cross-review"
    REVISION = "revision"
    DISPUTES = "disputes"
    SYNTHESIS = "synthesis"
    ARBITRATION = "arbitration"
    CROSS_ROUND_SYNTHESIS = "cross-round-synthesis"


# Backward-compatible alias — frozenset of Phase values for set operations
VALID_PHASES: frozenset[str] = frozenset(Phase)


class ErrorType(StrEnum):
    """Linter error classifications — each has distinct detection logic in check_* functions.

    Closed behavioral enum: adding an error type requires a new check_*
    function or new detection branch. Plugins extend via factory function.
    """
    MISSING_VARIABLE = "missing_variable"
    UNKNOWN_VARIABLE = "unknown_variable"
    MISSING_HEADING = "missing_heading"
    MISSING_MARKER = "missing_marker"
    MISSING_MODE_VARIABLE = "missing_mode_variable"


# Backward-compatible alias
KNOWN_ERROR_TYPES: frozenset[str] = frozenset(ErrorType)


def get_valid_modes(schema_dir: Path) -> frozenset[str]:
    """Scan schema/modes/*.yml to discover valid mode names.

    Used by validate.py to dynamically determine available modes
    rather than relying on a hardcoded set.
    """
    return frozenset(p.stem for p in schema_dir.glob("*.yml"))


class ConfigCondition(BaseModel):
    """A condition under which a variable is required, based on config field values.

    Examples:
        ConfigCondition(field="rounds", value="> 1")
        ConfigCondition(field="arbiter.timing", operator="==", value="inter-round")
    """

    field: str
    operator: str = "=="
    value: str


class VariableDefinition(BaseModel):
    """A single template variable definition from schema/variables.yml.

    Validates that each variable entry has the required metadata fields
    and that the declared type is one of the known variable types.
    """

    type: str
    description: str
    phases: list[str]
    required: bool = True
    modes: Optional[list[str]] = None
    condition: Optional[str] = None
    config_conditions: Optional[list[ConfigCondition]] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in VALID_VARIABLE_TYPES:
            raise ValueError(
                f"Invalid variable type '{v}'. "
                f"Must be one of: {', '.join(sorted(VALID_VARIABLE_TYPES))}"
            )
        return v

    @field_validator("phases")
    @classmethod
    def validate_phases(cls, v: list[str]) -> list[str]:
        invalid: set[str] = set(v) - VALID_PHASES
        if invalid:
            raise ValueError(
                f"Invalid phase(s): {invalid}. "
                f"Must be from: {', '.join(sorted(VALID_PHASES))}"
            )
        return v


class VariablesSchema(BaseModel):
    """Root model for schema/variables.yml."""

    schema_version: str = "1.0.0"
    variables: dict[str, VariableDefinition]

    @property
    def all_names(self) -> frozenset[str]:
        return frozenset(self.variables.keys())


class DisputeConfig(BaseModel):
    """Dispute-parsing subsystem interface from a mode schema."""

    synthesis_heading: str = ""
    entry_pattern: str = ""
    structural_markers: bool = False


class ArbitrationConfig(BaseModel):
    """Phase 6 output validation config from a mode schema."""

    required_headings: list[str] = Field(default_factory=list)
    influence_headings: dict[str, list[str]] = Field(default_factory=dict)


class CrossRoundSynthesisConfig(BaseModel):
    """Cross-round synthesis requirements from a mode schema."""

    structural_markers: bool = False
    dispute_heading: str = ""


class ModeSchema(BaseModel):
    """Root model for schema/modes/{mode}.yml.

    Mode validity is enforced by file existence in load_mode_schema
    rather than by a hardcoded validator. Use get_valid_modes() to
    dynamically discover available modes from schema/modes/*.yml.
    """

    mode: str
    variables: list[str] = Field(default_factory=list)
    templates: list[str] = Field(default_factory=list)
    mode_in_phases: list[str] = Field(default_factory=list)
    disputes: DisputeConfig = Field(default_factory=DisputeConfig)
    arbitration: ArbitrationConfig = Field(default_factory=ArbitrationConfig)
    cross_round_synthesis: CrossRoundSynthesisConfig = Field(default_factory=CrossRoundSynthesisConfig)


class LintError(BaseModel):
    """A single validation error found by the linter."""

    file_path: str
    error_type: ErrorType
    message: str
    schema_ref: Optional[str] = None
    suggestion: Optional[str] = None


# ---------------------------------------------------------------------------
# Value-level models (validate runtime values before template substitution)
# ---------------------------------------------------------------------------

class TemplateContext(BaseModel):
    """Base context for all template variable values.

    Subclassed per phase to enforce exactly which variables are required.
    The orchestrator constructs the appropriate context model before
    substitution — Pydantic validates all values at construction time.

    Using model_config to forbid extra fields ensures no undeclared
    variables sneak through. frozen=True makes context instances
    immutable after construction.
    """

    model_config = {"extra": "forbid", "frozen": True}

    OUTPUT_PATH: Path
    TARGET_FILES: Optional[PathList] = None


class ReviewContext(TemplateContext):
    """Variables required for Phase 1 review templates."""

    AGENT_NAME: str
    AGENT_PROMPT: str
    AGENT_DOCS: PathList
    MODE: Optional[str] = None
    PRIOR_FILES_SECTION: str = ""
    PRIOR_ROUND_SECTION: str = ""
    PRIOR_ARBITRATION_SECTION: str = ""
    ROUND: Optional[int] = None
    MAX_ROUNDS: Optional[int] = None
    PRIOR_SYNTHESIS_PATH: Optional[str] = None
    PRIOR_ROUND_DIR: Optional[str] = None
    PRIOR_ARBITRATION_PATH: Optional[Path] = None
    # Mode-specific (red-blue)
    AGENT_ROLE: Optional[str] = None


class CrossReviewContext(TemplateContext):
    """Variables required for Phase 2 cross-review templates."""

    REVIEWER_NAME: str
    REVIEWER_PROMPT: str
    REVIEWED_NAME: str
    REVIEWED_REVIEW_PATH: Path
    REVIEWER_REVIEW_PATH: Path
    AGENT_DOCS: PathList
    MODE: Optional[str] = None
    ROUND: Optional[int] = None
    MAX_ROUNDS: Optional[int] = None
    PRIOR_SYNTHESIS_PATH: Optional[str] = None
    PRIOR_ROUND_DIR: Optional[str] = None
    PRIOR_ARBITRATION_PATH: Optional[Path] = None
    # Mode-specific (red-blue)
    REVIEWER_ROLE: Optional[str] = None
    REVIEWED_ROLE: Optional[str] = None


class RevisionContext(TemplateContext):
    """Variables required for Phase 3 revision templates."""

    AGENT_NAME: str
    AGENT_PROMPT: str
    AGENT_DOCS: PathList
    MY_REVIEW_PATH: Path
    CROSS_REVIEWS_OF_ME: PathList
    MY_CROSS_REVIEWS: PathList
    ITERATION: int
    MODE: Optional[str] = None
    ROUND: Optional[int] = None
    MAX_ROUNDS: Optional[int] = None
    PRIOR_SYNTHESIS_PATH: Optional[str] = None
    PRIOR_ROUND_DIR: Optional[str] = None
    PRIOR_ARBITRATION_PATH: Optional[Path] = None
    # Mode-specific (red-blue)
    AGENT_ROLE: Optional[str] = None


class DisputesContext(TemplateContext):
    """Variables required for Phase 4 disputes templates."""

    AGENT_NAME: str
    AGENT_PROMPT: str
    AGENT_DOCS: PathList
    ALL_REVISION_PATHS: PathList
    MY_REVISION_PATH: Path
    MODE: Optional[str] = None
    ROUND: Optional[int] = None
    MAX_ROUNDS: Optional[int] = None
    PRIOR_SYNTHESIS_PATH: Optional[str] = None
    PRIOR_ROUND_DIR: Optional[str] = None
    PRIOR_ARBITRATION_PATH: Optional[Path] = None
    # Mode-specific (red-blue)
    AGENT_ROLE: Optional[str] = None


class SynthesisContext(TemplateContext):
    """Variables required for Phase 5 synthesis templates."""

    AGENT_NAMES: str
    ALL_REVIEWS: PathList
    ALL_CROSS_REVIEWS: PathList
    ALL_REVISIONS: PathList
    ALL_DISPUTES: PathList
    MODE: str
    TARGET_PATH: Path
    ROUND: Optional[int] = None
    MAX_ROUNDS: Optional[int] = None
    PRIOR_SYNTHESIS_PATH: Optional[str] = None
    PRIOR_ROUND_DIR: Optional[str] = None
    PRIOR_ARBITRATION_PATH: Optional[Path] = None


class ArbitrationContext(TemplateContext):
    """Variables required for Phase 6 arbitration templates."""

    ARBITER_NAME: str
    ARBITER_PROMPT: str
    ARBITER_DOCS: str
    GROUNDING_PATH: Path
    SYNTHESIS_PATH: Path
    ALL_DISPUTES: PathList
    TRIGGER: str
    REMAINING_DISPUTES: str
    AGENT_NAMES: str
    MODE: str
    INFLUENCE_LEVEL: InfluenceLevel = InfluenceLevel.BINDING


class CrossRoundSynthesisContext(TemplateContext):
    """Variables required for cross-round synthesis templates."""

    AGENT_NAMES: str
    MODE: str
    TARGET_PATH: Path
    ROUNDS_COMPLETED: int
    MAX_ROUNDS: int
    ROUND_SYNTHESES: str  # pre-formatted synthesis content per round
    TERMINATION_REASON: str
    ARBITRATION_PATHS: Optional[PathList] = None
    ARBITRATION_RULINGS: Optional[str] = None


# Map phase names to their context models for runtime validation
PHASE_CONTEXT_MODELS: dict[str, type[TemplateContext]] = {
    "review": ReviewContext,
    "cross-review": CrossReviewContext,
    "revision": RevisionContext,
    "disputes": DisputesContext,
    "synthesis": SynthesisContext,
    "arbitration": ArbitrationContext,
    "cross-round-synthesis": CrossRoundSynthesisContext,
}

# Runtime assertion: VALID_PHASES must match PHASE_CONTEXT_MODELS keys exactly.
# This catches drift if a new phase is added to one but not the other.
assert VALID_PHASES == frozenset(PHASE_CONTEXT_MODELS.keys()), (
    f"VALID_PHASES and PHASE_CONTEXT_MODELS keys have diverged. "
    f"VALID_PHASES: {sorted(VALID_PHASES)}, "
    f"PHASE_CONTEXT_MODELS: {sorted(PHASE_CONTEXT_MODELS.keys())}"
)
