# Phase 1 Review: game-theorist

**Spec**: 025-game-form-expansion
**Agent**: game-theorist
**Focus**: Mathematical correctness of new forms. Shapley correct? Potential game check sound? Bayesian prior validation?

---

## Overall Assessment

The implementation demonstrates rigorous treatment of the core game-theoretic concepts. Shapley value computation, potential game diagnostics, and the coalitional/congestion/Bayesian/repeated/mechanism-design models are mathematically grounded. The solver module (`solvers.py`) is clean, pure-Python, and correct for its stated scope.

**Verdict**: PASS with three substantive findings.

---

## Detailed Findings

### 1. Shapley Value Computation -- CORRECT

The formula in `solvers.py` (lines 24-71) correctly implements:

```
phi_i = sum_{S subset N\{i}} |S|!(|N|-|S|-1)!/|N|! * [v(S union {i}) - v(S)]
```

**Verification of four Shapley axioms**:

- **Efficiency**: Tested by `test_three_player_shapley_sums_to_grand_coalition` (sum of Shapley values = v(N) = 60). The formula's weight structure guarantees this algebraically -- the weights over all S for a fixed i sum to 1 when summed over all i and applied to marginal contributions.
- **Symmetry**: Tested by `test_symmetric_players_get_equal_shapley` (both get 5.0 in a symmetric 2-player game). Correct -- symmetric players have identical marginal contributions to every coalition.
- **Null player**: Tested by `test_null_player_gets_zero`. The null player adds zero marginal value to every coalition, so all terms vanish.
- **Additivity**: Not explicitly tested, but inherent to the linear formula. No test needed.

**Coalition key encoding**: Sorted comma-joined strings (`",".join(sorted(coalition))`) are a deterministic encoding. The empty coalition key `""` is handled correctly via `cf.get(coalition_key, 0.0)` defaulting to zero. This implicit v(empty) = 0 is standard.

**Complexity guard**: The N <= 10 cap is appropriate. Exact computation requires iterating over all 2^N subsets per player, giving O(N * 2^N) total work. At N=10 this is ~10K iterations; at N=20 it would be ~20M, making the cap sensible.

### 2. Potential Game Diagnostic -- CORRECT BUT SCOPE-LIMITED

The `is_potential_game()` function (lines 79-131) implements the Monderer-Shapley (1996) characterization for bimatrix (2-player) games. For every 2x2 sub-game within the payoff matrix, it checks:

```
a(i1,j1) - a(i2,j1) - a(i1,j2) + a(i2,j2) == b(i1,j1) - b(i1,j2) - b(i2,j1) + b(i2,j2)
```

This is the discrete analogue of the Jacobian symmetry condition: the cross-partial differences of player 1's payoffs (with respect to player 2's strategy changes) must equal the cross-partial differences of player 2's payoffs (with respect to player 1's strategy changes). Mathematically sound.

The `compute_potential()` function (lines 134-176) correctly constructs the potential matrix via path integration:
- Anchor Phi(0,0) = 0
- Fill first column: Phi(i,0) = Phi(i-1,0) + [a(i,0) - a(i-1,0)] (player 1 deviations)
- Fill rows: Phi(i,j) = Phi(i,j-1) + [b(i,j) - b(i,j-1)] (player 2 deviations)

This construction is path-independent precisely when the game is potential, which is verified by the prior `is_potential_game()` check. The max-potential summary statistic is a reasonable scalar reduction.

**Critical scope limitation**: The spec (section 2.1) describes the diagnostic as "a check applied to existing game forms." Existing forms include N-player GNEP and parametric games. The implementation only handles 2-player bimatrix games. For N-player games, the potential game check requires verifying integrability of the payoff gradient field -- specifically, that the mixed partial derivatives of distinct players' payoff functions with respect to each other's strategies are equal. This is substantially harder and is not implemented.

**Severity**: HIGH. The diagnostic cannot fulfill its stated spec purpose for N>2 games without generalization or explicit scope documentation.

### 3. Coalitional Game -- CORRECT

The `CoalitionalGame` model enforces:
- Non-empty player set
- Grand coalition key present in characteristic_function

The characteristic function encoding `dict[str, float]` with sorted comma-joined keys is a clean representation of v: 2^N -> R. The solver code correctly defaults missing coalition keys to 0.0, which implicitly enforces the standard convention v(empty) = 0.

**Superadditivity not enforced**: The model does not check v(S union T) >= v(S) + v(T) for disjoint S, T. This is intentional -- not all cooperative games are superadditive, and the Shapley value is well-defined regardless.

### 4. Congestion Game -- CORRECT

The model correctly validates that agent strategies reference only declared resources. The Rosenthal potential existence is noted in the docstring. The `cost_type` enum covers the standard families.

**Missing cost_functions field**: The spec (section 2.3) lists `cost_functions` as a schema field, but the model only has `cost_type`. Actual cost function coefficients (e.g., `c_r(n) = 3n + 1` for linear) are not representable. This is acceptable for type-level validation but insufficient for equilibrium computation via the Rosenthal potential.

### 5. Bayesian Game -- CORRECT WITH VALIDATION GAP

The prior probability sum-to-one check (tolerance 1e-6) is mathematically correct. The strict open-interval check would reject priors that don't sum exactly to 1.0.

**Validation gap**: The prior keys are not validated against the Cartesian product of type_spaces. Example:
```python
BayesianGame(
    type_spaces={"p1": ["H", "L"], "p2": ["H", "L"]},
    prior={"INVALID_KEY": 0.5, "ALSO_INVALID": 0.5},
)
```
This passes validation despite the keys having no relation to the type spaces. The prior keys should be comma-joined sorted type tuples from T_1 x T_2 x ... x T_N. Without this check, the Harsanyi transformation to normal form would produce a malformed game.

**Severity**: MEDIUM. Silent acceptance of semantically invalid inputs.

### 6. Repeated Game -- CORRECT

The discount_factor constraint `0 < delta < 1` is exactly right:
- delta = 0: degenerate (agents completely myopic, Folk Theorem inapplicable)
- delta = 1: infinite patient limit (technical subtlety -- Folk Theorem is stated for delta approaching 1, not at 1)
- delta outside [0,1]: meaningless

The `stage_game` string reference is a clean design for decoupling form definition from game embedding.

### 7. Mechanism Design Game -- MINIMAL BUT CORRECT

Two enum fields (`mechanism_type`, `valuation_type`) serve as a type discriminator. VCG payment computation, social welfare maximization, and allocation rules from the spec are not modeled. This is sufficient for form identification but not for solver integration.

---

## Summary of Findings

| # | Severity | Finding |
|---|----------|---------|
| 1 | HIGH | `is_potential_game()` restricted to 2-player games; spec implies general applicability to N-player existing forms |
| 2 | MEDIUM | BayesianGame prior keys not validated against type space Cartesian product; semantically invalid inputs accepted silently |
| 3 | LOW | MechanismDesignGame sparse -- serves as discriminator only, no solver-facing fields |
| 4 | INFO | Congestion game missing `cost_functions` field from spec section 2.3 |
| 5 | INFO | Prior tolerance 1e-6 may be too tight for computed/normalized priors |

---

## Recommendation

ACCEPT with mandatory action on Finding #1 (document 2-player limitation or generalize) and recommended action on Finding #2 (add prior key validation).
