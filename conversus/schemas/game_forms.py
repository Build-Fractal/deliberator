"""Pydantic models for game theory form validation.

Each model validates YAML instances against the corresponding schema in
schema/game-forms/. Models enforce required fields, type constraints, and
structural invariants (e.g. payoff matrix dimensions match strategy
cardinalities in normal-form).

No solver library imports — pure schema validation only (FR-008).
"""

from __future__ import annotations

import itertools
from pathlib import Path
from typing import Any, Literal, Optional, Union

import yaml
from pydantic import BaseModel, Field, model_validator


# ---------------------------------------------------------------------------
# Closed set of field types (FR-003)
# ---------------------------------------------------------------------------

VALID_FIELD_TYPES: frozenset[str] = frozenset({
    "string",
    "integer",
    "float",
    "list[string]",
    "list[float]",
    "matrix",
    "function",
    "constraint_list",
    "constraint_map",
    "map[string, list[string]]",
    "map[string, string]",
    "map[string, function]",
    "map[string, list[string]]",
    "map[string, float]",
})


# ---------------------------------------------------------------------------
# Schema file location
# ---------------------------------------------------------------------------

def _schema_dir() -> Path:
    """Return the path to schema/game-forms/.

    Uses ``conversus.paths.resolve_package_path`` which works both when
    pip-installed (importlib.resources) and in the dev source tree.
    """
    from conversus.paths import resolve_package_path

    return resolve_package_path("conversus", "schema", "game-forms")


# ---------------------------------------------------------------------------
# GNEP validation mixin (P1-4)
# ---------------------------------------------------------------------------

class _GNEPValidationMixin:
    """Shared validation logic for GNEP-derived game forms.

    Extracts the player-objective correspondence and player-decision-variable
    validation that is common to GNEPGame and ParametricGame.

    NOTE: Downstream dispatch should use the ``form`` discriminator field,
    not ``isinstance`` checks, because the mixin creates a shared validation
    interface — not a subtype hierarchy.
    """

    @staticmethod
    def _validate_player_objectives(
        players: list[str],
        objectives: dict[str, str],
    ) -> None:
        """Validate that objectives have exactly one entry per player."""
        obj_players = set(objectives.keys())
        game_players = set(players)
        if obj_players != game_players:
            missing = game_players - obj_players
            extra = obj_players - game_players
            parts = []
            if missing:
                parts.append(f"missing objectives for: {sorted(missing)}")
            if extra:
                parts.append(f"extra objectives for non-players: {sorted(extra)}")
            raise ValueError(
                f"Objective count mismatch — each player must have exactly one "
                f"objective. {'; '.join(parts)}"
            )

    @staticmethod
    def _validate_player_decision_variables(
        players: list[str],
        decision_variables: dict[str, list[str]],
    ) -> None:
        """Validate that decision variables are defined for each player."""
        dv_players = set(decision_variables.keys())
        game_players = set(players)
        if dv_players != game_players:
            raise ValueError(
                f"Decision variables must be defined for each player. "
                f"Players: {sorted(game_players)}, "
                f"decision_variables keys: {sorted(dv_players)}"
            )


# ---------------------------------------------------------------------------
# Normal Form Game
# ---------------------------------------------------------------------------

class NormalFormGame(BaseModel):
    """Normal form game: finite players, finite strategy sets, payoff matrix.

    Structural invariant: payoff matrix dimensions must match the cardinalities
    of the strategy sets, and each cell must contain one payoff per player.
    """

    form: Literal["normal-form"] = "normal-form"
    players: list[str]
    strategies: dict[str, list[str]]
    payoff_matrix: list[Any]

    @model_validator(mode="after")
    def validate_structure(self) -> NormalFormGame:
        # Every player must have a strategy entry
        for player in self.players:
            if player not in self.strategies:
                raise ValueError(
                    f"Player '{player}' has no entry in strategies. "
                    f"Each player must have a corresponding strategy set."
                )

        # Strategy sets must be non-empty
        for player, strats in self.strategies.items():
            if not strats:
                raise ValueError(
                    f"Player '{player}' has an empty strategy set. "
                    f"Each player must have at least one strategy."
                )

        # Validate payoff matrix dimensions match strategy cardinalities
        expected_dims = [len(self.strategies[p]) for p in self.players]
        num_players = len(self.players)
        self._validate_matrix(self.payoff_matrix, expected_dims, 0, num_players)

        return self

    @staticmethod
    def _validate_matrix(
        matrix: Any,
        dims: list[int],
        depth: int,
        num_players: int,
    ) -> None:
        """Recursively validate payoff matrix dimensions."""
        if depth == len(dims):
            # At leaf: must be a list of per-player payoffs
            if not isinstance(matrix, list) or len(matrix) != num_players:
                raise ValueError(
                    f"Payoff cell must be a list of {num_players} values "
                    f"(one per player), got: {matrix}"
                )
            return

        if not isinstance(matrix, list):
            raise ValueError(
                f"Expected list at matrix depth {depth}, got {type(matrix).__name__}"
            )

        if len(matrix) != dims[depth]:
            raise ValueError(
                f"Payoff matrix dimension {depth} has size {len(matrix)}, "
                f"expected {dims[depth]} (matching strategy set cardinality)."
            )

        for i, sub in enumerate(matrix):
            NormalFormGame._validate_matrix(sub, dims, depth + 1, num_players)


# ---------------------------------------------------------------------------
# GNEP Game
# ---------------------------------------------------------------------------

class GNEPGame(_GNEPValidationMixin, BaseModel):
    """Generalized Nash Equilibrium Problem.

    Structural invariant: objectives must have exactly one entry per player.
    """

    form: Literal["gnep"] = "gnep"
    players: list[str]
    decision_variables: dict[str, list[str]]
    objectives: dict[str, str]
    local_constraints: Optional[dict[str, list[str]]] = None
    coupled_constraints: Optional[list[str]] = None

    @model_validator(mode="after")
    def validate_structure(self) -> GNEPGame:
        self._validate_player_objectives(self.players, self.objectives)
        self._validate_player_decision_variables(
            self.players, self.decision_variables
        )
        return self


# ---------------------------------------------------------------------------
# Parametric Game (extends GNEP via mixin)
# ---------------------------------------------------------------------------

class ParametricGame(_GNEPValidationMixin, BaseModel):
    """Parametric game extending GNEP with external parameter vector.

    Inherits GNEP structural invariants plus requires non-empty parameters.

    NOTE: Uses _GNEPValidationMixin for shared validation — not direct class
    inheritance from GNEPGame. Downstream dispatch should use the ``form``
    discriminator, not ``isinstance``.
    """

    form: Literal["parametric"] = "parametric"
    players: list[str]
    decision_variables: dict[str, list[str]]
    objectives: dict[str, str]
    parameters: list[str]
    local_constraints: Optional[dict[str, list[str]]] = None
    coupled_constraints: Optional[list[str]] = None

    @model_validator(mode="after")
    def validate_structure(self) -> ParametricGame:
        self._validate_player_objectives(self.players, self.objectives)
        self._validate_player_decision_variables(
            self.players, self.decision_variables
        )

        # Parameters must be non-empty
        if not self.parameters:
            raise ValueError("Parametric game must have at least one parameter.")

        return self


# ---------------------------------------------------------------------------
# Stackelberg Game
# ---------------------------------------------------------------------------

class StackelbergGame(BaseModel):
    """Stackelberg (leader-follower) game.

    Structural invariant: follower_objectives must have exactly one entry
    per follower. follower_variables must have entries for each follower.
    """

    form: Literal["stackelberg"] = "stackelberg"
    leader: str
    followers: list[str]
    leader_variables: list[str]
    follower_variables: dict[str, list[str]]
    leader_objective: str
    follower_objectives: dict[str, str]
    leader_constraints: Optional[list[str]] = None
    follower_constraints: Optional[dict[str, list[str]]] = None

    @model_validator(mode="after")
    def validate_structure(self) -> StackelbergGame:
        follower_set = set(self.followers)

        # Follower objectives must match followers
        fo_keys = set(self.follower_objectives.keys())
        if fo_keys != follower_set:
            missing = follower_set - fo_keys
            extra = fo_keys - follower_set
            parts = []
            if missing:
                parts.append(f"missing objectives for: {sorted(missing)}")
            if extra:
                parts.append(f"extra objectives for non-followers: {sorted(extra)}")
            raise ValueError(
                f"Follower objective mismatch — each follower must have exactly "
                f"one objective. {'; '.join(parts)}"
            )

        # Follower variables must match followers
        fv_keys = set(self.follower_variables.keys())
        if fv_keys != follower_set:
            raise ValueError(
                f"Follower variables must be defined for each follower. "
                f"Followers: {sorted(follower_set)}, "
                f"follower_variables keys: {sorted(fv_keys)}"
            )

        return self


# ---------------------------------------------------------------------------
# Potential Game (diagnostic check, spec 025)
# ---------------------------------------------------------------------------

class PotentialGame(BaseModel):
    """Potential game diagnostic check.

    Not a standalone game form — tests whether an existing game's payoff
    structure admits a potential function (symmetric Jacobian). If yes,
    convergence to Nash equilibrium is mathematically guaranteed.
    """

    form: Literal["potential"] = "potential"
    potential_function: str
    is_potential: bool


# ---------------------------------------------------------------------------
# Coalitional Game (Shapley values, spec 025)
# ---------------------------------------------------------------------------

class CoalitionalGame(BaseModel):
    """Cooperative / coalitional game for fair value attribution.

    Uses characteristic function v: 2^N -> R to compute fair distribution
    of the grand coalition's value across players. Solution concepts include
    Shapley values, the core, and the nucleolus.

    Structural invariant: characteristic_function must include the grand
    coalition key (all players sorted and comma-joined).
    """

    form: Literal["coalitional"] = "coalitional"
    players: list[str]
    characteristic_function: dict[str, float]
    solution_concept: Literal["shapley", "core", "nucleolus"]

    @model_validator(mode="after")
    def validate_structure(self) -> CoalitionalGame:
        if not self.players:
            raise ValueError("Coalitional game must have at least one player.")

        # Grand coalition key must be present
        grand_key = ",".join(sorted(self.players))
        if grand_key not in self.characteristic_function:
            raise ValueError(
                f"characteristic_function must include the grand coalition "
                f"key '{grand_key}' (all players sorted and comma-joined)."
            )

        return self


# ---------------------------------------------------------------------------
# Congestion Game (shared resources, spec 025)
# ---------------------------------------------------------------------------

class CongestionGame(BaseModel):
    """Congestion game: shared resources with diminishing returns.

    Every congestion game is a potential game (Rosenthal potential), so
    convergence to Nash equilibrium is guaranteed.

    Structural invariant: every resource in agent_strategies must be in
    the resources list.
    """

    form: Literal["congestion"] = "congestion"
    resources: list[str]
    cost_type: Literal["linear", "polynomial", "step"]
    agent_strategies: dict[str, list[str]]

    @model_validator(mode="after")
    def validate_structure(self) -> CongestionGame:
        if not self.resources:
            raise ValueError("Congestion game must have at least one resource.")

        resource_set = set(self.resources)
        for agent, used_resources in self.agent_strategies.items():
            invalid = set(used_resources) - resource_set
            if invalid:
                raise ValueError(
                    f"Agent '{agent}' uses resources not in the resources "
                    f"list: {sorted(invalid)}. Available: {sorted(resource_set)}"
                )

        return self


# ---------------------------------------------------------------------------
# Bayesian Game (hidden preferences, spec 025 Tier 2)
# ---------------------------------------------------------------------------

class BayesianGame(BaseModel):
    """Bayesian game: games with private information.

    Each agent has a type (hidden preferences) drawn from a known
    prior distribution. Solved via Harsanyi transformation to
    normal-form, then standard equilibrium computation.

    Structural invariant: prior probabilities must sum to 1.0 (within
    tolerance).
    """

    form: Literal["bayesian"] = "bayesian"
    type_spaces: dict[str, list[str]]
    prior: dict[str, float]

    @model_validator(mode="after")
    def validate_structure(self) -> BayesianGame:
        if not self.type_spaces:
            raise ValueError("Bayesian game must have at least one player type space.")

        # Prior probabilities should sum to 1.0
        total = sum(self.prior.values())
        if abs(total - 1.0) > 1e-6:
            raise ValueError(
                f"Prior probabilities must sum to 1.0, got {total:.6f}."
            )

        # Prior keys must be valid Cartesian product combinations of type_spaces.
        # Each key is a comma-joined type profile with one type per player
        # (in the order players appear in type_spaces).
        players = list(self.type_spaces.keys())
        type_lists = [self.type_spaces[p] for p in players]
        valid_keys = {
            ",".join(combo) for combo in itertools.product(*type_lists)
        }
        prior_keys = set(self.prior.keys())
        invalid_keys = prior_keys - valid_keys
        if invalid_keys:
            raise ValueError(
                f"Prior keys must be valid type profile combinations "
                f"(Cartesian product of type_spaces). "
                f"Invalid keys: {sorted(invalid_keys)}. "
                f"Valid keys: {sorted(valid_keys)}"
            )
        missing_keys = valid_keys - prior_keys
        if missing_keys:
            raise ValueError(
                f"Prior must cover all type profile combinations. "
                f"Missing keys: {sorted(missing_keys)}. "
                f"Each element of the Cartesian product of type_spaces "
                f"must have a probability entry."
            )

        return self


# ---------------------------------------------------------------------------
# Repeated Game (multi-round cooperation, spec 025 Tier 2)
# ---------------------------------------------------------------------------

class RepeatedGame(BaseModel):
    """Repeated game: multi-round cooperation dynamics.

    Formalizes why cooperation emerges over multiple rounds via the Folk
    Theorem. The discount factor controls how much agents value future
    payoffs relative to present ones.

    Structural invariant: discount_factor must be in (0, 1).
    """

    form: Literal["repeated"] = "repeated"
    stage_game: str
    discount_factor: float

    @model_validator(mode="after")
    def validate_structure(self) -> RepeatedGame:
        if not (0.0 < self.discount_factor < 1.0):
            raise ValueError(
                f"discount_factor must be in (0, 1), got {self.discount_factor}."
            )

        return self


# ---------------------------------------------------------------------------
# Mechanism Design Game (VCG, spec 025 Tier 2)
# ---------------------------------------------------------------------------

class MechanismDesignGame(BaseModel):
    """Mechanism design game: incentive-compatible rules.

    Designs rules (mechanisms) that elicit truthful preference revelation
    from agents. VCG mechanisms guarantee incentive compatibility and
    allocative efficiency.
    """

    form: Literal["mechanism-design"] = "mechanism-design"
    mechanism_type: Literal["vcg", "first_price", "second_price"]
    valuation_type: Literal["additive", "submodular"]


# ---------------------------------------------------------------------------
# Mode mapping
# ---------------------------------------------------------------------------

class ModeFormMapping(BaseModel):
    """A single mode-to-form mapping entry."""

    form: str
    solver: Optional[str] = None
    note: Optional[str] = None


class ModeMapping(BaseModel):
    """Root model for mode-mapping.yml."""

    mappings: dict[str, ModeFormMapping]

    def lookup(self, mode: str) -> str:
        """Return the game form identifier for a given mode.

        Raises KeyError if the mode is not found.
        """
        if mode not in self.mappings:
            raise KeyError(
                f"Unknown mode '{mode}'. "
                f"Available modes: {sorted(self.mappings.keys())}"
            )
        return self.mappings[mode].form


def load_mode_mapping(path: Path | None = None) -> ModeMapping:
    """Load and validate the mode-mapping.yml file.

    Args:
        path: Path to mode-mapping.yml. Defaults to the bundled schema file.

    Returns:
        Validated ModeMapping instance.
    """
    if path is None:
        path = _schema_dir() / "mode-mapping.yml"
    with open(path) as f:
        data = yaml.safe_load(f)
    return ModeMapping.model_validate(data)
