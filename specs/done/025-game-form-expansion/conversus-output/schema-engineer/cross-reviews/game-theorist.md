# Cross-Review: schema-engineer reviewing game-theorist

**Spec**: 025-game-form-expansion

---

## Agreement

The game-theorist's mathematical analysis is rigorous and accurate. I concur with:

- The Shapley computation is correct (weight formula verified)
- The potential game diagnostic is mathematically sound for 2-player games
- The coalitional game grand coalition validation is appropriate
- The concern about `is_potential_game()` being limited to 2 players is valid

## Disagreements

### 1. Concern #3 (MechanismDesignGame "too sparse") -- I disagree on severity

The game-theorist rates this as "Low" but I think it's appropriate for the current stage. The MechanismDesignGame model serves as a type discriminator within the schema validation layer. The spec explicitly places mechanism design in Tier 2, and Tier 2 solver integration is deferred. Adding fields now that have no validator or solver to consume them would be speculative. The sparse model correctly represents what can be validated today.

When Tier 2 solver work begins, the model should be expanded with `valuation_functions`, `allocation_rule`, and payment structure fields. But that's future work, not a current gap.

### 2. Missing cost_functions in CongestionGame (Info, not Low)

The game-theorist rates this as "Info." I agree with Info severity. The `cost_type` enum (linear, polynomial, step) declares the *category* of cost function. The actual cost function coefficients would be needed for solver integration but are not needed for schema validation. This is consistent with how other models separate schema validation from solver inputs.

## Additions

The game-theorist did not assess the test coverage for edge cases in `compute_shapley_values()`:

- The `test_null_player_gets_zero` test is excellent -- it verifies the null player axiom
- The `test_too_many_players_raises` test correctly verifies the N > 10 guard
- Missing: no test for a single-player game (trivial case where Shapley value = v({player}))

This is a minor gap -- the single-player case is mathematically trivial and the formula handles it correctly, but explicit verification would strengthen the test suite.
