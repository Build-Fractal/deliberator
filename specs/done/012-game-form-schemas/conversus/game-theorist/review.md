# Game-Theorist Review: 012-game-form-schemas

**Reviewer**: game-theorist
**Date**: 2026-03-22
**Target**: spec 012 + YAML schemas + Pydantic models + tests

---

### Executive Summary

Spec 012 sets out to formalize the game-theoretic vocabulary underlying conversus deliberation modes as machine-readable YAML schemas with Pydantic validation. It covers four game forms — normal form, GNEP, parametric game, and Stackelberg game — and provides a mode-to-form mapping table. The intent is correct: separating the mathematical structure of games from solver logic is standard practice in computational game theory, and establishing this vocabulary first is the right sequencing decision.

The implementation captures the surface structure of each game form competently. Player sets, strategy/variable definitions, objective functions, and constraint partitioning are all present. The structural invariants enforced by the Pydantic validators (player-objective bijection, payoff tensor dimensionality, non-empty parameter vectors) are mathematically necessary conditions. The decision to use symbolic expression strings rather than executable functions is appropriate for a schema-only layer.

However, the schemas suffer from several mathematical omissions that will cause problems for downstream specs (013-020). The most consequential: the GNEP schema does not distinguish between minimization and maximization (the `sense` of each objective), the normal-form schema cannot represent mixed strategies, the Stackelberg schema does not model the bilevel optimization structure that makes Stackelberg games mathematically distinct from sequential games, and no schema captures the information structure (who observes what, when). The single most important recommendation is: **add an explicit optimization sense field (`minimize`/`maximize`) to every objective in every continuous-variable game form (GNEP, parametric, Stackelberg), because without it the schemas are mathematically ambiguous and every downstream solver spec will have to guess or re-parse string prefixes.**

### Alignment

- **[Finite player sets]** (spec L29, L39, normal-form.yml L19-24, gnep.yml L21-26): All game forms correctly require finite, named player sets. This matches the standard definition in both normal-form and GNEP literature where the player set N = {1, ..., n} is always finite and fixed before the game is played.

- **[Per-player strategy/variable partitioning]** (spec L30-31, L40-41, game_forms.py L59, L131): Normal-form uses per-player strategy sets; GNEP/parametric use per-player decision variable vectors. This correctly captures that in a normal-form game each player i chooses from S_i, while in a GNEP each player controls x_i from a continuous decision space. The Pydantic validators enforce the bijection between players and their strategy/variable sets.

- **[Coupled vs. local constraint separation]** (gnep.yml L42-56, game_forms.py L133-134): The GNEP schema correctly distinguishes local constraints g_i(x_i) that depend only on player i's variables from coupled constraints h(x_1,...,x_N) that involve multiple players. This is the defining structural difference between a standard NEP (Nash Equilibrium Problem) and a GNEP — the coupled constraints are what make feasible sets interdependent.

- **[Payoff tensor dimensionality validation]** (game_forms.py L80-116): The recursive `_validate_matrix` enforces that the payoff tensor has shape |S_1| x |S_2| x ... x |S_N| x N, matching the mathematical requirement that a normal-form game's payoff function u: S_1 x S_2 x ... x S_N -> R^N must be defined for every joint strategy profile.

- **[Parametric extension of GNEP]** (spec L47-56, parametric.yml): The parametric game correctly models J_i(x_i, x_{-i}; p) where p is exogenous. This is the standard formulation in parametric optimization and sensitivity analysis. The non-emptiness check on parameters is appropriate — a parametric game with no parameters is just a GNEP.

- **[Leader-follower role separation]** (stackelberg.yml L26-59): The Stackelberg schema separates leader and follower identities, variables, objectives, and constraints. This captures the asymmetric information structure where the leader commits first and followers respond.

### Missed Opportunities

- **[Optimization sense]**: Every continuous-variable objective (GNEP, parametric, Stackelberg) is stored as a plain string like `"minimize x1^2 + x2^2 - y1"`. The sense (minimize vs. maximize) is embedded in the string and must be parsed heuristically. A dedicated `sense: minimize | maximize` field per objective would make the mathematical structure machine-readable without string parsing. This is how every standard optimization modeling language (AMPL, GAMS, Pyomo, CVXPY) structures objectives. **Impact: high.**

- **[Mixed strategy support in normal form]**: The normal-form schema only captures pure strategies. In game theory, the foundational result (Nash 1950) guarantees equilibrium existence in mixed strategies. The schema should support an optional `mixed_strategies` field or at minimum a `strategy_type: pure | mixed` indicator so downstream solvers know whether to search over simplices. Without this, the schema cannot represent the solution concept that makes normal-form games most useful. **Impact: high.**

- **[Variable bounds and domains]**: GNEP and parametric game decision variables are listed as names only — there is no way to specify that x_i is real-valued, integer, or bounded (e.g., x_i in [0, 1]). In optimization, variable domains are structurally distinct from constraints. A `variable_domain` or `bounds` field per variable would prevent downstream specs from having to encode `x >= 0, x <= 1` as separate constraints when they are actually box constraints. **Impact: medium.**

- **[Bilevel structure in Stackelberg]**: The Stackelberg schema stores the leader objective as `J_leader(x_leader, x_followers*(x_leader))` in description but does not structurally represent the bilevel program. Mathematically, the leader solves: min_{x_L} J_L(x_L, x_F*(x_L)) subject to x_F*(x_L) = argmin_{x_F} J_F(x_F, x_L) s.t. constraints. The follower's best-response mapping is the inner optimization problem, and it is structurally what makes Stackelberg different from a sequential game. The schema should have a `follower_best_response` or `inner_problem` structural marker. **Impact: medium.**

- **[Information structure / timing]**: None of the schemas capture the information structure — who observes what before making decisions. Normal-form games are simultaneous (no observation). Stackelberg has sequential observation. But the schemas do not encode this, and the GNEP schema does not specify whether decisions are simultaneous or have a protocol. An `information_structure: simultaneous | sequential | partial` field would make the mathematical assumptions explicit. **Impact: medium.**

- **[Constraint qualification / regularity conditions]**: The GNEP schema accepts arbitrary constraint expressions but does not provide a field for specifying constraint qualification conditions (e.g., Slater's condition, LICQ, MFCQ). For downstream solver specs (017-019), knowing which regularity conditions hold determines which solution algorithms are applicable. An optional `constraint_qualification` metadata field would save solvers from having to infer this. **Impact: low.**

- **[Solution concept specification]**: The schemas define the game structure but not the target solution concept. A normal-form game could be solved for Nash equilibrium, correlated equilibrium, or dominant strategy equilibrium. A GNEP could target variational equilibrium (VE) or normalized equilibrium. The schema should have an optional `solution_concept` field so that the schema carries intent, not just structure. **Impact: medium.**

- **[N-player normal form]**: The schema and example show a 2-player game, and the field descriptions say `list[string]` for strategies (spec L77, normal-form.yml L27-31) rather than `dict[string, list[string]]`. The Pydantic model correctly uses `dict[str, list[str]]`, but the YAML schema's `type: list[string]` for the strategies field is misleading — it is actually a mapping, not a flat list. This type mismatch between the YAML schema description and the Pydantic model will confuse implementors of downstream specs. **Impact: medium.**

### Off-Base Assumptions

- **[Prisoner's dilemma as GNEP]**: The mode-mapping (mode-mapping.yml L28-33) maps `prisoners-dilemma` to GNEP form. This is mathematically imprecise. The prisoner's dilemma is a specific 2-player, 2-strategy normal-form game with a particular payoff ordering (T > R > P > S, where T=temptation, R=reward, P=punishment, S=sucker). It is the canonical example of a normal-form game, not a GNEP. The mapping note justifies the choice by referencing "individual incentives constrained by shared outcomes," but the prisoner's dilemma has no coupled constraints — the payoff interdependence is entirely through the payoff function, not through shared feasibility constraints. If the conversus prisoners-dilemma mode genuinely has coupled constraints (e.g., shared document convergence), then it is not actually modeling a prisoner's dilemma in the game-theoretic sense; it is modeling a GNEP with PD-like payoff incentives. The mapping should acknowledge this distinction or the mode should be renamed.

- **[GNEP local constraints depend only on own variables]**: The GNEP schema description (gnep.yml L44-48) states local constraints are `g_i(x_i) <= 0`, depending only on player i's variables. This is the standard definition. However, in many practical formulations (including some GNEP literature), local constraints can depend on other players' variables: `g_i(x_i, x_{-i}) <= 0`. The distinction matters because when all constraints are shared (coupled), the GNEP reduces to a jointly-constrained problem, which has different solution properties. The schema should clarify whether it intends the strict definition (own variables only) or the relaxed definition.

- **[Strategies field type declaration]**: The normal-form YAML schema declares `strategies` as `type: list[string]` (normal-form.yml L27-28), but the Pydantic model types it as `dict[str, list[str]]` (game_forms.py L59), and the example (normal-form.yml L46-52) shows a mapping. The YAML schema's type declaration is wrong — `list[string]` means a flat list of strings, not a per-player mapping. This is not an assumption about game theory per se, but it creates a mathematical ambiguity: if someone reads the YAML schema literally, they would think all players share a single strategy set (symmetric game), which is a much stronger condition than the general normal-form definition.

### Actionable Recommendations

1. **Add optimization-sense field** (Priority: P1)
   - **Current state**: Objectives are plain strings like `"minimize x1^2"`. The sense is embedded in the string.
   - **Proposed change**: Add a structured objective representation to GNEP, parametric, and Stackelberg schemas. Replace `objectives: dict[str, str]` with `objectives: dict[str, Objective]` where `Objective` has fields `sense: Literal["minimize", "maximize"]` and `expression: str`. In YAML: `objectives: { agent_1: { sense: minimize, expression: "x1^2 + x2^2" } }`.
   - **Rationale**: Every optimization modeling framework distinguishes sense from expression structurally. Downstream solver plugins (specs 017-019) must know the sense to formulate the problem correctly. Parsing it from a string prefix is fragile and error-prone.
   - **Risk if ignored**: Solver plugins will implement ad-hoc string parsing, leading to bugs when expressions use non-standard phrasing or when sense is omitted.

2. **Fix strategies type declaration in normal-form YAML** (Priority: P1)
   - **Current state**: normal-form.yml declares `strategies` as `type: list[string]`, but the Pydantic model uses `dict[str, list[str]]` and the example shows a per-player mapping.
   - **Proposed change**: Change the YAML schema field type from `type: list[string]` to `type: dict[string, list[string]]` or introduce a `mapping` type to the closed type set (FR-003).
   - **Rationale**: The current type declaration is mathematically incorrect. In a normal-form game, each player i has their own strategy set S_i. A flat list would imply all players share the same strategy set, which is only true in symmetric games.
   - **Risk if ignored**: Downstream implementors reading the YAML schema (not the Pydantic source) will build incorrect parsers. The inconsistency between schema and implementation erodes trust in the schema as documentation.

3. **Add variable bounds/domain fields** (Priority: P1)
   - **Current state**: Decision variables in GNEP/parametric/Stackelberg are bare string names with no type or bound information.
   - **Proposed change**: Extend decision variable definitions to include optional bounds and domain: `decision_variables: { agent_1: [ { name: x1, domain: real, lower: 0, upper: 1 } ] }`. Add `domain` (values: `real`, `integer`, `binary`) and optional `lower`/`upper` fields.
   - **Rationale**: In mathematical programming, variable bounds are structurally distinct from general constraints. They define the feasible set geometry (box constraints vs. general nonlinear constraints) and determine which solver algorithms are applicable. Without bounds, every `x >= 0` must be encoded as a constraint, losing structural information.
   - **Risk if ignored**: Solver plugins lose structural information needed for algorithm selection. Box-constrained problems that could use efficient projected-gradient methods get treated as general constrained problems.

4. **Correct prisoner's-dilemma mode mapping** (Priority: P2)
   - **Current state**: `prisoners-dilemma` maps to `gnep` with a note about coupled constraints.
   - **Proposed change**: Either (a) map `prisoners-dilemma` to `normal-form` with a note that the PD payoff structure (T > R > P > S) can be validated as a schema invariant, or (b) keep the GNEP mapping but rename the note to explicitly state: "This mode uses PD-like payoff incentives within a GNEP structure, not the classical 2x2 prisoner's dilemma game."
   - **Rationale**: The prisoner's dilemma is the most well-known normal-form game in all of game theory. Mapping it to GNEP without explanation will confuse anyone with game theory training and undermines the credibility of the mathematical vocabulary this spec establishes.
   - **Risk if ignored**: Downstream specs and users will misunderstand what game is actually being modeled, leading to incorrect solution concept application.

5. **Add solution-concept field** (Priority: P2)
   - **Current state**: Schemas define game structure only. There is no indication of which equilibrium concept to target.
   - **Proposed change**: Add an optional `solution_concept` field to each game form. Valid values: for normal-form: `nash | dominant-strategy | correlated | minimax`; for GNEP: `variational-equilibrium | normalized-equilibrium | quasi-variational`; for Stackelberg: `strong-stackelberg | weak-stackelberg`; for parametric: inherit from GNEP.
   - **Rationale**: The same game structure admits different solution concepts with different existence guarantees, computational complexity, and welfare properties. A schema that carries intent (not just structure) enables solver plugins to select the correct algorithm.
   - **Risk if ignored**: Solver plugins must infer the solution concept from mode or configuration, creating an implicit coupling that the schema layer was meant to eliminate.

6. **Add mixed-strategy indicator to normal form** (Priority: P2)
   - **Current state**: Normal-form schema only represents pure strategies. The payoff matrix structure assumes deterministic strategy selection.
   - **Proposed change**: Add an optional field `strategy_space: pure | mixed` (default: `pure`). When `mixed`, the interpretation is that players choose probability distributions over their strategy sets, and the payoff matrix provides expected payoff computation. The schema structure does not change — only the interpretation.
   - **Rationale**: Nash's existence theorem guarantees equilibrium in mixed strategies for finite games. Without this field, the schema cannot express the most fundamental solution concept in game theory.
   - **Risk if ignored**: Winner-take-all mode solvers that need mixed equilibria will have to extend the schema ad-hoc, breaking the "shared vocabulary" intent of this spec.

7. **Model bilevel structure in Stackelberg** (Priority: P2)
   - **Current state**: Stackelberg schema lists leader and follower objectives/variables/constraints as flat parallel structures. The bilevel nature is only described in comments.
   - **Proposed change**: Add a `bilevel_structure` field or restructure the schema to nest the follower problem as an explicit inner problem: `inner_problem: { players: [followers], objectives: ..., constraints: ... }`. Add a `leader_anticipates_best_response: true` boolean to make the anticipation assumption explicit.
   - **Rationale**: The bilevel structure (outer problem optimizes over inner problem's solution mapping) is the mathematical essence of Stackelberg games. Without it, the schema is indistinguishable from a sequential game without anticipation — which has fundamentally different equilibria.
   - **Risk if ignored**: Solver plugins cannot distinguish between Stackelberg equilibrium (with anticipation) and backward-induction equilibrium (without), leading to incorrect solutions.

8. **Add information-structure field** (Priority: P3)
   - **Current state**: No schema captures timing or observation structure.
   - **Proposed change**: Add an optional `information_structure` field with values `simultaneous` (normal-form, GNEP default), `sequential` (Stackelberg default), or `partial` (for future extensive-form extensions). For Stackelberg, this is redundant with the form itself but makes the assumption explicit.
   - **Rationale**: The information structure determines the equilibrium concept. Simultaneous games use Nash equilibrium; sequential games use subgame-perfect equilibrium or Stackelberg equilibrium. Making this explicit prevents mathematical ambiguity.
   - **Risk if ignored**: Low immediate risk since the form names imply the information structure, but as the game form library grows, the implicit convention will break down.

9. **Expand closed type set for schema correctness** (Priority: P3)
   - **Current state**: FR-003 defines types: `string`, `integer`, `float`, `list[string]`, `list[float]`, `matrix`, `function`, `constraint_list`. The `strategies` field needs `dict[string, list[string]]`, and proposed variable-bound fields need `dict[string, object]`.
   - **Proposed change**: Add `dict[string, list[string]]`, `dict[string, object]`, and `dict[string, string]` to the closed type set. Alternatively, introduce a generic `mapping` type with key/value type parameters.
   - **Rationale**: The current type set cannot express the actual types used by the Pydantic models. A closed type set that does not include the types actually in use is worse than no type set at all.
   - **Risk if ignored**: The YAML schemas remain inconsistent with their Pydantic implementations, and the type system provides false guarantees.

10. **Add local-constraint generality note** (Priority: P3)
    - **Current state**: GNEP schema states local constraints are `g_i(x_i) <= 0`, depending only on own variables.
    - **Proposed change**: Add a note in gnep.yml clarifying: "In the strict GNEP formulation used here, local constraints depend only on the owning player's variables. Constraints involving other players' variables must be placed in coupled_constraints. This differs from some GNEP formulations in the literature where local constraints may depend on x_{-i}."
    - **Rationale**: There are two conventions in the GNEP literature. The spec should state which it follows so downstream implementors know whether to check constraint variable scoping.
    - **Risk if ignored**: Ambiguity about whether the schema enforces variable scoping in local constraints leads to silent modeling errors.

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/012-game-form-schemas/spec.md`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/normal-form.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/gnep.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/parametric.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/stackelberg.yml`
- `<HOME>/code/payer-index-mono/conversus/schema/game-forms/mode-mapping.yml`
- `<HOME>/code/payer-index-mono/conversus/src/conversus_schemas/game_forms.py`
- `<HOME>/code/payer-index-mono/conversus/src/conversus_schemas/__init__.py`
- `<HOME>/code/payer-index-mono/conversus/tests/test_game_forms.py`
