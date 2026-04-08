# Phase 1 Review: game-theorist

**Spec**: 025-game-form-expansion
**Agent**: game-theorist
**Focus**: Mathematical correctness of new game forms

---

## Overall Assessment

The implementation demonstrates solid mathematical understanding of game theory fundamentals. The six new game forms (potential diagnostic, coalitional, congestion, Bayesian, repeated, mechanism design) are correctly formulated and their Pydantic models enforce the right structural invariants. The solver module implements Shapley values and potential game diagnostics cleanly in pure Python.

**Verdict**: PASS with minor concerns.

---

## Detailed Findings

### 1. Shapley Value Computation (solvers.py, lines 24-71) -- CORRECT

The Shapley formula is correctly implemented:

```
phi_i = sum over S subset of N\{i}: |S|! * (|N|-|S|-1)! / |N|! * [v(S union {i}) - v(S)]
```

- The weight `factorial(size) * factorial(n - size - 1) / n_factorial` is mathematically correct.
- Coalition keys are sorted and comma-joined, consistent with the CoalitionalGame model's grand coalition key convention.
- The empty coalition key `""` is handled correctly (line 59).
- The 10-player cap is reasonable given combinatorial explosion (2^10 = 1024 subsets per player).

Test SC-002 correctly verifies the efficiency axiom (Shapley values sum to grand coalition value). The null player and symmetry tests verify two additional Shapley axioms. The additivity axiom is not tested but is inherent to the formula.

### 2. Potential Game Diagnostic (solvers.py, lines 79-176) -- CORRECT WITH NOTES

The `is_potential_game()` function checks whether a 2-player game admits a potential function by verifying that the cross-partial differences are symmetric across all 2x2 sub-games. This is the correct characterization for 2-player games (Monderer & Shapley, 1996).

**Concern**: The function only handles 2-player games. The spec describes a general diagnostic applicable to "existing game forms" (section 2.1), but the implementation is restricted to bimatrix games. For N-player potential games, one needs to check the integrability condition on the payoff gradient field -- substantially harder. This limitation is not documented.

The `compute_potential()` function correctly constructs the potential matrix using path integration from Phi(0,0) = 0, filling first column via player 1's payoffs, then filling rows via player 2's payoffs. The max-potential summary statistic is a reasonable choice.

### 3. Coalitional Game Model (game_forms.py, lines 315-344) -- CORRECT

The model correctly requires:
- Non-empty player set
- Grand coalition key present in the characteristic function

The characteristic function type `dict[str, float]` with sorted comma-joined keys is a clean encoding of v: 2^N -> R. The grand coalition validation is sound -- without it, Shapley computation would silently produce wrong results.

**Minor note**: The model does not validate that v(empty set) = 0, which is a standard convention in cooperative game theory. The solver code handles this via `cf.get(coalition_key, 0.0)` which defaults missing keys to 0. This implicit treatment is acceptable but could be documented.

### 4. Congestion Game Model (game_forms.py, lines 351-380) -- CORRECT

Every congestion game is a potential game via the Rosenthal potential -- this is correctly noted in the docstring. The model validates that agent strategies only reference declared resources. The `cost_type` enum (linear, polynomial, step) covers the standard cost function categories.

**Missing**: No `cost_functions` field despite the spec listing it (section 2.3). The model captures the structure but not the actual cost functions, which would be needed for solver integration. This is acceptable for schema validation but would block actual equilibrium computation.

### 5. Bayesian Game Model (game_forms.py, lines 387-414) -- CORRECT WITH CONCERN

The prior probability sum-to-one validation (tolerance 1e-6) is correct. The type spaces model is clean.

**Concern**: The prior dictionary keys should correspond to type profiles (combinations of types across players). The model does not validate that the prior keys are consistent with the declared type spaces. For example, with `type_spaces = {"p1": ["H", "L"], "p2": ["H", "L"]}`, valid prior keys should be the Cartesian product. Currently, any string keys are accepted.

### 6. Repeated Game Model (game_forms.py, lines 421-442) -- CORRECT

The discount factor validation `0 < delta < 1` is exactly right -- delta = 0 means agents don't value the future (degenerate), delta = 1 means infinite horizon (Folk Theorem breaks down for exact equality).

The `stage_game` field is a string reference rather than an embedded game model. This is a reasonable design choice for schema flexibility but means validation of the reference is deferred.

### 7. Mechanism Design Game Model (game_forms.py, lines 449-459) -- MINIMAL

The model has only two fields: `mechanism_type` and `valuation_type`. This is the sparsest of the new forms. The spec describes VCG payment computation, social welfare maximization, and allocation rules, but the model has no fields for valuation functions, allocation rules, or payment structure.

This is sufficient as a discriminator (identifying that a game uses mechanism design) but insufficient for solver integration.

---

## Summary of Concerns

| # | Severity | Item |
|---|----------|------|
| 1 | Medium | `is_potential_game()` limited to 2-player games; spec implies general applicability |
| 2 | Low | Prior key validation missing in BayesianGame -- keys not checked against type space Cartesian product |
| 3 | Low | MechanismDesignGame model too sparse for solver integration |
| 4 | Low | v(empty) = 0 convention not enforced in CoalitionalGame |
| 5 | Info | Congestion game missing cost_functions field from spec |

---

## Recommendation

Accept. The mathematical foundations are correct. Concern #1 should be addressed in a follow-up (generalize potential game diagnostic to N players or document the 2-player limitation). The remaining concerns are schema completeness issues that do not affect correctness.
