"""Pydantic models for feature extraction output (spec 015).

Defines the data models that represent extracted feature vectors from
conversus deliberation artifacts.  Models are frozen (immutable) and
validated via Pydantic to ensure consumers receive well-typed data.

No solver library imports -- pure schema validation only (FR-006, FR-015).
"""

from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from conversus.schemas.modes import VALID_MODES


# ---------------------------------------------------------------------------
# Per-agent feature vector (FR-006)
# ---------------------------------------------------------------------------

class AgentFeatures(BaseModel):
    """Feature vector for a single agent within a single round.

    All numeric fields default to zero so that missing-phase extraction
    gracefully degrades (FR-003).
    """

    model_config = {"frozen": True}

    agent_name: str

    # Common across modes
    recommendation_count: int = 0
    withdrawn_count: int = 0
    modified_count: int = 0
    surviving_count: int = 0
    new_recommendation_count: int = 0
    concession_rate: float = 0.0
    position_vector: list[int] = Field(default_factory=list)

    # Winner-take-all specific
    ranking_position: int = 0
    criterion_scores: list[float] = Field(default_factory=list)
    attacks_received: int = 0
    attacks_rebutted: int = 0
    attacks_conceded: int = 0

    # Prisoners-dilemma specific
    core_competency_count: int = 0
    unique_capability_count: int = 0
    shared_territory_count: int = 0
    deferral_count: int = 0
    territory_claim_vector: list[int] = Field(default_factory=list)
    overreach_count: int = 0
    overreach_accepted: int = 0
    overreach_rebutted: int = 0
    sandbagging_count: int = 0

    # Red-blue specific
    role: Optional[str] = None  # "red" or "blue"
    severity_vector: list[int] = Field(default_factory=list)
    threat_count: int = 0
    cascading_failure_count: int = 0
    safeguard_count: int = 0
    acknowledged_limitation_count: int = 0
    mitigation_rate: float = 0.0
    confirmed_count: int = 0

    # Negotiation-specific
    zopa_coverage: float = 0.0
    party_satisfaction: float = 0.0
    reservation_price: float = 0.0
    aspiration_price: float = 0.0

    # Negotiation-specific — time-ranged ZOPA (spec 047 Phase 5
    # sub-integration #1). Values in seconds for engine independence;
    # callers convert from `Duration.as_seconds()` (the parser output
    # for temporal constraints in agent positions). Default 0.0 means
    # "no temporal constraint extracted" — the agent's negotiation
    # position carries no time bound. This default mirrors the
    # missing-phase graceful-degrade pattern (FR-003).
    reservation_duration_seconds: float = 0.0
    aspiration_duration_seconds: float = 0.0
    temporal_zopa_overlap: float = 0.0

    # Resource-allocation specific
    utilization_efficiency: float = 0.0
    allocation_inequality: float = 0.0
    shapley_value: float = 0.0

    # Fair-division specific
    proportionality_score: float = 0.0
    envy_count: int = 0
    envy_free: bool = False

    # Mechanism-design specific
    social_welfare_contribution: float = 0.0
    gaming_vulnerability_count: int = 0
    incentive_compatibility: float = 0.0


# ---------------------------------------------------------------------------
# Per-round aggregate features
# ---------------------------------------------------------------------------

class RoundFeatures(BaseModel):
    """Aggregate features for a single deliberation round.

    Contains both per-agent feature vectors and round-level aggregates
    like dispute count and convergence count.
    """

    model_config = {"frozen": True}

    round_number: int = 1
    agent_features: dict[str, AgentFeatures] = Field(default_factory=dict)

    # Aggregate features (derived from synthesis / disputes)
    dispute_count: int = 0
    convergence_count: int = 0

    # Agreement matrix: agent_name -> agent_name -> 0/1
    agreement_matrix: dict[str, dict[str, int]] = Field(default_factory=dict)

    # Winner-take-all specific aggregates
    score_differential: float = 0.0

    # Red-blue specific aggregates
    landed_attack_count: int = 0
    mitigated_attack_count: int = 0
    accepted_risk_count: int = 0
    coverage_score: float = 0.0

    # Prisoners-dilemma specific aggregates
    boundary_clarity: int = 0

    # Negotiation-specific aggregates
    zopa_size: float = 0.0
    agreement_efficiency: float = 0.0

    # Negotiation-specific — time-ranged ZOPA aggregate (spec 047
    # Phase 5 sub-integration #1). Total time-range overlap across
    # all parties' temporal constraints, in seconds. Computed from
    # AgentFeatures.reservation_duration_seconds and
    # aspiration_duration_seconds across the round's agents.
    temporal_zopa_size_seconds: float = 0.0

    # Resource-allocation specific aggregates
    total_utilization: float = 0.0
    gini_coefficient: float = 0.0

    # Fair-division specific aggregates
    total_envy_pairs: int = 0
    max_envy_depth: float = 0.0

    # Mechanism-design specific aggregates
    total_social_welfare: float = 0.0
    total_gaming_vulnerabilities: int = 0


# ---------------------------------------------------------------------------
# Top-level FeatureSet (FR-008, FR-009, FR-010)
# ---------------------------------------------------------------------------

class FeatureSet(BaseModel):
    """Top-level feature set for a complete deliberation.

    Contains mode, all rounds' feature vectors, and metadata.
    Plugins import and validate against this model (FR-009, FR-016).
    Multi-round features are a list of per-round sets (FR-010).
    """

    model_config = {"frozen": True}

    mode: str
    rounds: list[RoundFeatures] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_feature_set(self) -> FeatureSet:
        if self.mode not in VALID_MODES:
            raise ValueError(
                f"Invalid mode '{self.mode}'. "
                f"Valid modes are: {sorted(VALID_MODES)}."
            )
        return self
