# Feature Specification: Game Form Expansion (Tier 1 + Tier 2)

**Feature ID**: `025-game-form-expansion`
**Created**: 2026-03-27
**Status**: Draft
**Depends On**: `012-game-form-schemas` (existing models), `021-nashopt-integration` (solver wrapper)
**Origin**: Research — `.firecrawl/research-game-theory-forms.md`

---

## 1. Feature Summary

Expand the game form library from 4 forms to 10, covering the standard game theory toolkit needed for general-purpose optimization problem formulation.

**Tier 1** (no new solver deps): Potential game diagnostic, cooperative/coalitional games (Shapley), congestion games.

**Tier 2** (needs nashopt/scipy): Bayesian games, repeated games, mechanism design (VCG).

---

## 2. New Game Forms

### 2.1 Potential Game (Diagnostic, not a separate form)

A check applied to existing game forms. Tests whether the extracted payoff structure admits a potential function — if yes, convergence is mathematically guaranteed.

```
Potential function Φ(s) exists iff:
  ∂²Φ/∂s_i∂s_j is symmetric for all i,j
  (equivalently: the payoff Jacobian is symmetric)
```

- **Implementation**: `is_potential_game(payoff_matrix) -> bool` + `compute_potential(payoff_matrix) -> float`
- **Solver**: scipy.linalg (symmetry check on Jacobian)
- **User parameters**: None (automatic diagnostic)
- **Conversus integration**: POST_PHASE_5 check — "This deliberation has a potential game structure; convergence is guaranteed."

### 2.2 Cooperative / Coalitional Game

Models: "How much did each agent contribute to the outcome?" Computes fair value attribution via Shapley values.

```
Characteristic function v: 2^N → ℝ
  v(S) = value of coalition S (subset of agents)

Shapley value φ_i = Σ_{S⊆N\{i}} |S|!(|N|-|S|-1)!/|N|! × [v(S∪{i}) - v(S)]
```

- **Schema fields**: `players`, `characteristic_function` (or derivation from synthesis), `solution_concept` (shapley | core | nucleolus)
- **Solver**: Pure Python for Shapley (N≤10), sampling approximation for N>10, LP via HiGHS for nucleolus
- **User parameters**: `solution_concept`, optional `coalition_structure`
- **Conversus integration**: POST_DELIBERATION — "Agent X contributed 35% of converged recommendations, agent Y contributed 22%"

### 2.3 Congestion Game

Formalizes territory/scoping where multiple agents claim shared resources with diminishing returns.

```
Resources: R = {r_1, ..., r_m}
Strategy: s_i ⊆ R (subset of resources agent i uses)
Cost: c_r(n_r) = cost of resource r when n_r agents use it
Payoff: J_i = -Σ_{r∈s_i} c_r(n_r)
```

- **Special property**: Every congestion game is a potential game → convergence guaranteed
- **Schema fields**: `resources`, `cost_functions`, `agent_strategies`
- **Solver**: scipy.optimize on the Rosenthal potential
- **User parameters**: `resources` (list), `cost_type` (linear | polynomial | step)
- **Conversus integration**: Maps naturally to prisoners-dilemma/scoping mode

### 2.4 Bayesian Game (Tier 2)

Games with private information. Each agent has a type (hidden preferences) drawn from a known distribution.

```
Type space: T_i for each player i
Prior: p(t) over type profiles
Strategy: σ_i: T_i → A_i (maps type to action)
Expected utility: E_t[u_i(σ_i(t_i), σ_{-i}(t_{-i}), t_i)]
```

- **Implementation**: Harsanyi transformation expands to normal-form, then nashopt solves
- **Schema fields**: `type_spaces`, `prior_distribution`, `utility_functions`
- **Solver**: nashopt (on expanded game)
- **User parameters**: `type_distribution` (how preferences are distributed), `private_context_schema`
- **Conversus integration**: Maps to negotiation — agents have private docs that inform positions

### 2.5 Repeated Game (Tier 2)

Formalizes why cooperation emerges over multiple rounds. Folk Theorem bounds.

```
Stage game: G (any normal-form game)
Discount factor: δ ∈ (0, 1)
Feasible payoff set: F = conv{u(a) : a ∈ A}
Individually rational payoffs: IR_i = min_{a_{-i}} max_{a_i} u_i(a)
Folk Theorem: any payoff v ∈ F with v_i > IR_i is supportable for δ close to 1
```

- **Implementation**: Compute F and IR from stage game, identify supportable outcomes
- **Schema fields**: `stage_game`, `discount_factor`, `punishment_strategy`
- **Solver**: LP for feasible set computation
- **User parameters**: `discount_factor` (how much agents value future rounds)
- **Conversus integration**: Explains convergence dynamics — "At the current cooperation level, the Folk Theorem supports continued cooperation if agents value future rounds at δ > 0.7"

### 2.6 Mechanism Design / VCG (Tier 2)

Incentive-compatible rules for truthful preference revelation.

```
Social welfare: W(θ) = Σ_i v_i(f(θ), θ_i)  (maximize)
VCG payment: p_i = max_{a} Σ_{j≠i} v_j(a, θ_j) - Σ_{j≠i} v_j(f(θ), θ_j)
Incentive compatibility: truthful reporting is dominant strategy
```

- **Implementation**: Social welfare maximization as MIP, VCG payment computation
- **Schema fields**: `mechanism_type` (vcg | first_price | second_price), `valuation_functions`, `allocation_rule`
- **Solver**: HiGHS for allocation MIP, pure Python for VCG payments
- **User parameters**: `mechanism_type`, `valuation_type` (additive | submodular)
- **Conversus integration**: "Design the arbiter as a VCG mechanism — agents report true preferences, optimal allocation computed, payments ensure truthfulness"

---

## 3. Functional Requirements

### Game Form Schemas
- **FR-001**: Each new game form MUST have a YAML schema in `schema/game-forms/` following existing conventions.
- **FR-002**: Each new game form MUST have a Pydantic model in `conversus/schemas/game_forms.py` with validators.
- **FR-003**: The mode-mapping MUST be updated to include new forms where applicable.
- **FR-004**: Potential game diagnostic MUST be implemented as a check function, not a separate form.

### Solver Integration
- **FR-005**: Tier 1 forms (potential, coalitional, congestion) MUST work with pure Python + scipy only.
- **FR-006**: Tier 2 forms (Bayesian, repeated, VCG) MAY require nashopt or AMPL.
- **FR-007**: All solver dependencies are optional — missing solvers produce graceful fallbacks.

### Templates
- **FR-008**: Each game form MUST have at least one objective template in `schema/objective-functions/`.
- **FR-009**: New templates MUST include `gap_question` fields for the construction pipeline (spec 014).
- **FR-010**: New constraint templates for integrality and cardinality MUST be added.

### Tests
- **FR-011**: Each game form MUST have Pydantic validation tests.
- **FR-012**: Each solver function MUST have unit tests with mock data.
- **FR-013**: The potential game diagnostic MUST have tests for known potential and non-potential games.

---

## 4. Success Criteria

- **SC-001**: `is_potential_game()` correctly identifies a 2-player coordination game as potential and a matching pennies game as non-potential.
- **SC-002**: Shapley values for a 3-player game sum to the grand coalition value.
- **SC-003**: Congestion game equilibrium matches the potential function minimizer.
- **SC-004**: Bayesian Nash equilibrium of a first-price auction matches the known analytical solution.
- **SC-005**: After Tier 1+2, `len(game_forms) >= 10` and `len(objective_templates) >= 25`.

---

## 5. Constraints

- Tier 1 MUST NOT require nashopt, jax, or AMPL.
- Tier 2 MAY require nashopt but MUST degrade gracefully.
- No new mandatory dependencies in the core `conversus` package.
- Potential game diagnostic is a check, not a mode — it augments existing modes.
