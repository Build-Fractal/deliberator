# Phase 4 Disputes: game-theorist

**Spec**: 025-game-form-expansion

---

## Surviving Disputes

### DISPUTE 1: is_potential_game() 2-player limitation (High)

**Status**: Surviving -- all agents agree this is a genuine gap.

The spec says the diagnostic applies to "existing game forms." Existing forms include N-player games (GNEP, parametric). The implementation only handles 2-player normal-form games.

**Recommended resolution**: Document the limitation in the function docstring and add a note to the spec that N-player potential game detection is deferred to a future iteration. The 2-player case covers the primary use case (coordination games, prisoners dilemma analysis).

### DISPUTE 2: BayesianGame prior key validation (Medium)

**Status**: Surviving -- game-theorist and schema-engineer agree; spec-compliance did not dispute.

The model validates that prior probabilities sum to 1.0 but does not check that the prior keys correspond to valid type profiles from the Cartesian product of type_spaces. Invalid keys pass validation silently.

**Recommended resolution**: Add a model_validator that verifies prior keys against the type space Cartesian product.

## Withdrawn Disputes

- v(empty) = 0 convention: Withdrawn (implicitly handled by solver defaults)
- PotentialGame naming: Withdrawn (style preference, not functional)
- MechanismDesignGame sparseness: Maintained as Low observation, not a dispute
