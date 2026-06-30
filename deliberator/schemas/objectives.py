"""Pydantic models for objective function template validation.

Each model validates YAML instances against the corresponding schema in
schema/objective-functions/. Models enforce required fields, type constraints,
and cross-field invariants (e.g. derived_from required for function-type
parameters, mode_compatibility entries must be valid mode names).

No solver library imports — pure schema validation only (FR-008, FR-009, FR-010).
"""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from deliberator.schemas.modes import VALID_MODES


# ---------------------------------------------------------------------------
# Closed sets of valid values
# ---------------------------------------------------------------------------

VALID_PARAMETER_TYPES: frozenset[str] = frozenset({
    "float",
    "integer",
    "string",
    "function",
    "boolean",
})

VALID_GAME_FORMS: frozenset[str] = frozenset({
    "normal-form",
    "gnep",
    "parametric",
    "stackelberg",
    "coalitional",
    "congestion",
    "bayesian",
    "repeated",
    "mechanism-design",
})


# ---------------------------------------------------------------------------
# Parameter Definition (FR-010)
# ---------------------------------------------------------------------------

class ParameterDefinition(BaseModel):
    """Validates an individual parameter entry within a template.

    Cross-field invariants:
    - Parameters of type ``function`` must specify ``derived_from`` (FR-005).
    - When ``range`` has ``min`` and ``max`` and ``default`` is present,
      ``min <= default <= max``.
    """

    name: str
    type: Literal["float", "integer", "string", "function", "boolean"]
    description: str
    range: Optional[dict[str, Any]] = None
    default: Optional[Any] = None
    gap_question: Optional[str] = None
    derived_from: Optional[str] = None

    @model_validator(mode="after")
    def validate_parameter(self) -> ParameterDefinition:
        # FR-005: function-type parameters require derived_from
        if self.type == "function" and not self.derived_from:
            raise ValueError(
                f"Parameter '{self.name}' has type 'function' but no "
                f"'derived_from' field. Function-type parameters must "
                f"specify which deliberation artifact provides the value."
            )

        # FR-010: range + default consistency
        if (
            self.range is not None
            and self.default is not None
            and "min" in self.range
            and "max" in self.range
        ):
            range_min = self.range["min"]
            range_max = self.range["max"]
            if not (range_min <= self.default <= range_max):
                raise ValueError(
                    f"Parameter '{self.name}' default value {self.default} "
                    f"is outside the valid range [{range_min}, {range_max}]."
                )

        return self


# ---------------------------------------------------------------------------
# Constraint Template (FR-009)
# ---------------------------------------------------------------------------

class ConstraintTemplate(BaseModel):
    """Validates a constraint YAML file.

    Constraint templates define reusable mathematical constraints that can
    be attached to any objective function template. Each constraint specifies
    a symbolic form, its parameters, and which modes it applies to.
    """

    name: str
    description: str
    form: str
    parameters: list[ParameterDefinition]
    mode_compatibility: list[str]

    @model_validator(mode="after")
    def validate_constraint(self) -> ConstraintTemplate:
        # FR-009: mode_compatibility entries must be valid mode names
        invalid_modes = set(self.mode_compatibility) - VALID_MODES
        if invalid_modes:
            raise ValueError(
                f"Invalid mode_compatibility entries: {sorted(invalid_modes)}. "
                f"Valid modes are: {sorted(VALID_MODES)}."
            )

        # mode_compatibility must not be empty
        if not self.mode_compatibility:
            raise ValueError(
                "mode_compatibility must not be empty. "
                "Specify at least one compatible mode."
            )

        # Duplicate parameter names
        param_names = [p.name for p in self.parameters]
        dupes = [n for n in param_names if param_names.count(n) > 1]
        if dupes:
            raise ValueError(
                f"Duplicate parameter names: {sorted(set(dupes))}. "
                f"Each parameter must have a unique name."
            )

        return self


# ---------------------------------------------------------------------------
# Objective Template (FR-008)
# ---------------------------------------------------------------------------

class ObjectiveTemplate(BaseModel):
    """Validates an objective function template YAML file.

    Objective templates define canonical mathematical forms that bridge mode
    selection (spec 008) and guided construction (spec 014). Each template
    specifies a symbolic objective, its parameters, compatible constraints,
    and which game forms / modes it applies to.

    Cross-field invariants:
    - ``mode_compatibility`` entries must be valid mode names.
    - ``game_form`` must be a known game form from spec 012.
    """

    name: str
    description: str
    form: str
    game_form: str
    mode_compatibility: list[str]
    parameters: list[ParameterDefinition]
    constraints: list[str] = Field(default_factory=list)
    example: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_template(self) -> ObjectiveTemplate:
        # FR-008: mode_compatibility entries must be valid mode names
        invalid_modes = set(self.mode_compatibility) - VALID_MODES
        if invalid_modes:
            raise ValueError(
                f"Invalid mode_compatibility entries: {sorted(invalid_modes)}. "
                f"Valid modes are: {sorted(VALID_MODES)}."
            )

        # FR-008: game_form must be a known form from spec 012
        if self.game_form not in VALID_GAME_FORMS:
            raise ValueError(
                f"Unknown game_form '{self.game_form}'. "
                f"Valid game forms are: {sorted(VALID_GAME_FORMS)}."
            )

        # mode_compatibility must not be empty
        if not self.mode_compatibility:
            raise ValueError(
                "mode_compatibility must not be empty. "
                "Specify at least one compatible mode."
            )

        # Duplicate parameter names
        param_names = [p.name for p in self.parameters]
        dupes = [n for n in param_names if param_names.count(n) > 1]
        if dupes:
            raise ValueError(
                f"Duplicate parameter names: {sorted(set(dupes))}. "
                f"Each parameter must have a unique name."
            )

        return self
