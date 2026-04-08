"""conversus.schemas: Game theory form schemas for the conversus deliberation engine.

Provides Pydantic models for validating game form instances (normal-form, GNEP,
parametric, Stackelberg), a mode-to-form mapping lookup, objective function
template validation (FR-008, FR-009, FR-010), guided objective construction
pipeline (spec 014), and feature extraction pipeline (spec 015).

NOTE: This package ships as ``conversus.schemas`` (not ``conversus-features``
as FR-014 originally stated in the spec).
"""

from conversus.schemas.construction import (
    GENERAL_TEMPLATE_NAMES,
    PROBLEM_MD_STDIN,
    AssembledObjective,
    DecisionType,
    GapFiller,
    GapList,
    InteractiveGapFiller,
    InteractiveTemplateSelector,
    NonInteractiveGapFiller,
    NonInteractiveTemplateSelector,
    ParameterGap,
    SourceProvenance,
    TemplateSelector,
    assemble_objective,
    classify_decision_type,
    construct_objective,
    extract_explicit_parameters,
    fill_parameter_gaps,
    identify_gaps,
    load_constraint_templates,
    load_objective_templates,
    select_candidate_templates,
)
from conversus.schemas.game_forms import (
    VALID_FIELD_TYPES,
    BayesianGame,
    CoalitionalGame,
    CongestionGame,
    GNEPGame,
    MechanismDesignGame,
    NormalFormGame,
    ParametricGame,
    PotentialGame,
    RepeatedGame,
    StackelbergGame,
    load_mode_mapping,
)
from conversus.schemas.solvers import (
    compute_potential,
    compute_shapley_values,
    is_potential_game,
)
from conversus.schemas.extraction import (
    extract_features,
    write_features,
)
from conversus.schemas.features import (
    AgentFeatures,
    FeatureSet,
    RoundFeatures,
)
from conversus.schemas.objectives import (
    VALID_PARAMETER_TYPES,
    ConstraintTemplate,
    ObjectiveTemplate,
    ParameterDefinition,
)
from conversus.schemas.validation import (
    SensitivityFinding,
    ValidationVerdict,
    generate_validation_config,
    has_sensitivity_instructions,
)

__all__ = [
    # Game forms
    "VALID_FIELD_TYPES",
    "BayesianGame",
    "CoalitionalGame",
    "CongestionGame",
    "GNEPGame",
    "MechanismDesignGame",
    "NormalFormGame",
    "ParametricGame",
    "PotentialGame",
    "RepeatedGame",
    "StackelbergGame",
    "load_mode_mapping",
    # Solvers (spec 025)
    "compute_potential",
    "compute_shapley_values",
    "is_potential_game",
    # Objectives
    "VALID_PARAMETER_TYPES",
    "ConstraintTemplate",
    "ObjectiveTemplate",
    "ParameterDefinition",
    # Construction pipeline (spec 014)
    "GENERAL_TEMPLATE_NAMES",
    "PROBLEM_MD_STDIN",
    "AssembledObjective",
    "DecisionType",
    "GapFiller",
    "GapList",
    "InteractiveGapFiller",
    "InteractiveTemplateSelector",
    "NonInteractiveGapFiller",
    "NonInteractiveTemplateSelector",
    "ParameterGap",
    "SourceProvenance",
    "TemplateSelector",
    "assemble_objective",
    "classify_decision_type",
    "construct_objective",
    "extract_explicit_parameters",
    "fill_parameter_gaps",
    "identify_gaps",
    "load_constraint_templates",
    "load_objective_templates",
    "select_candidate_templates",
    # Feature extraction pipeline (spec 015)
    "AgentFeatures",
    "FeatureSet",
    "RoundFeatures",
    "extract_features",
    "write_features",
    # Validation flow (spec 027)
    "SensitivityFinding",
    "ValidationVerdict",
    "generate_validation_config",
    "has_sensitivity_instructions",
]
