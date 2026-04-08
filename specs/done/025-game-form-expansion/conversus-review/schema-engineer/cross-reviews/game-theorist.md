# Cross-Review: schema-engineer reviewing game-theorist

**Spec**: 025-game-form-expansion
**Reviewer**: schema-engineer
**Subject**: game-theorist Phase 1 review

---

## Verified Claims

### 1. Shapley formula implementation is correct

The game-theorist's line-by-line verification of the weight formula `factorial(size) * factorial(n - size - 1) / n_factorial` is accurate. I independently verify that this matches the standard Shapley formula. The axiom-by-axiom verification (efficiency, symmetry, null player, additivity) is rigorous and well-mapped to specific test cases.

### 2. Potential game check is mathematically sound for 2 players

The cross-partial symmetry condition is the standard characterization from Monderer & Shapley (1996). The `compute_potential()` path-integration construction is correct -- anchoring at Phi(0,0) = 0, filling via player 1's payoff differences along the first column, then player 2's payoff differences along rows. Path independence holds precisely when the game is potential, which is pre-verified.

### 3. Coalition key encoding is deterministic

Sorted comma-join is a canonical encoding for subsets. The empty string for the empty coalition is handled correctly via `dict.get()` defaulting to 0.0. Confirmed.

### 4. BayesianGame prior key validation gap is real

The example of arbitrary keys passing validation is demonstrably correct. I independently confirm that:

```python
BayesianGame(
    type_spaces={"p1": ["H", "L"], "p2": ["H", "L"]},
    prior={"INVALID_KEY": 0.5, "ALSO_INVALID": 0.5},
)
```

passes all validators. This is a genuine gap.

---

## Disagreements

### 1. Finding #3 (MechanismDesignGame sparse) -- severity should be INFO, not LOW

The game-theorist rates MechanismDesignGame sparseness as "Low." I would rate it **Info**. The model correctly serves as a type discriminator within the schema validation layer. The spec explicitly places mechanism design in Tier 2, and Tier 2 solver integration is deferred. There is no validator or solver that would consume additional fields today. Adding speculative fields (valuation_functions, allocation_rule, payment_structure) would introduce untested, unvalidated surface area.

The sparse model is the right design for the current phase. When Tier 2 solver work begins, the model should be expanded. But until then, two Literal enum fields are exactly what's needed for form identification and template routing.

### 2. Finding #1 (is_potential_game 2-player limitation) -- agree with HIGH

The game-theorist rates this HIGH based on the spec's stated scope ("existing game forms"). I concur. However, I want to add a schema-level nuance: the `is_potential_game()` function signature takes `payoff_matrix: list[list[float]]`, which is structurally a bimatrix representation. The function cannot accept a GNEPGame or ParametricGame as input because those models have different structures (decision_variables, objectives, constraints -- not a payoff matrix). So the limitation is not just mathematical but also structural -- the function's interface constrains it to normal-form bimatrix games.

To generalize, the function would need either:
(a) Overloaded signatures accepting different game form models, or
(b) A preprocessing step that extracts a payoff representation from arbitrary game forms

Both are non-trivial and support the recommendation to document the limitation rather than attempt generalization in this phase.

---

## Additions

### Test gap: single-player coalitional game

The game-theorist's review covers multi-player Shapley scenarios (3-player, 2-player symmetric, null player, N>10 guard) but does not note the absence of a single-player test. For a single-player game:

```python
game = CoalitionalGame(
    players=["solo"],
    characteristic_function={"solo": 42},
    solution_concept="shapley",
)
```

The Shapley value should trivially equal v({solo}) = 42. This is a boundary case that the formula handles correctly (the outer loop iterates over size=0 only, with weight 0! * 0! / 1! = 1, and marginal contribution v({solo}) - v({}) = 42 - 0 = 42). An explicit test would strengthen the suite.

### compute_potential() return value semantics

The game-theorist correctly describes the path-integration construction but does not comment on the return value semantics. The function returns `max(phi[i][j])` -- the maximum potential value across all strategy profiles. This is a summary statistic, not the full potential matrix. For diagnostic purposes (reporting to the user), a more informative return would be the full potential matrix or the argmax (the strategy profile that maximizes the potential -- i.e., the Nash equilibrium). The current scalar return is acceptable but limits downstream use.
