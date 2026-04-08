# Phase 3 Revision: game-theorist

**Spec**: 025-game-form-expansion
**Agent**: game-theorist

---

## Position Changes After Cross-Review

### UPGRADED: Finding #1 (is_potential_game 2-player limitation) -- HIGH, confirmed

Both cross-reviewers reinforce this finding:

- **schema-engineer** adds a structural nuance: the function signature `payoff_matrix: list[list[float]]` is inherently bimatrix. It cannot accept GNEPGame, ParametricGame, or StackelbergGame objects. The limitation is not just mathematical but also interface-level.
- **spec-compliance** adds a compliance nuance: FR-004's language "existing game forms" covers normal-form, gnep, parametric, stackelberg. The diagnostic applies to a subset of one form (2-player normal-form only).

I accept both additions. The finding is now:
- **Mathematical scope**: 2-player bimatrix only (N-player requires gradient field integrability)
- **Interface scope**: `list[list[float]]` signature excludes non-matrix game representations
- **Compliance scope**: diagnostic applies to ~25% of "existing game forms" by FR-004's language

**Revised recommendation**: (1) Amend spec section 2.1 to say "a check applied to 2-player normal-form games" rather than "existing game forms." (2) Add docstring noting the restriction. (3) Open a follow-up issue for N-player generalization with a note that it requires overloaded signatures per game form type.

### UPGRADED: Finding #2 (BayesianGame prior key validation) -- MEDIUM, confirmed

All three agents converge on this. The schema-engineer provides the implementation recommendation (Cartesian product check). The spec-compliance agent notes it weakens the FR-002 spirit. I maintain MEDIUM severity.

**Revised recommendation**: Add a `model_validator` that:
1. Computes the Cartesian product of all type_spaces values
2. Encodes each product element as a comma-joined sorted string
3. Verifies that the prior keys are a subset of the valid product keys
4. Optionally warns if the prior does not cover all product keys (partial specification)

### DOWNGRADED: Finding #3 (MechanismDesignGame sparseness) -- INFO

The schema-engineer argues this should be INFO rather than LOW, noting that adding speculative fields with no validator or solver would introduce untested surface area. I accept this argument. The sparse model is the correct design for the current phase. Downgraded from LOW to INFO.

### MAINTAINED: Finding #4 (congestion game missing cost_functions) -- INFO

No cross-reviewer contested this. The `cost_type` enum captures the category; actual coefficients are solver inputs not needed for schema validation.

### UPGRADED: Finding #5 (prior tolerance 1e-6) -- LOW

The spec-compliance agent argues this is LOW rather than INFO due to interoperability concerns with computed priors in automated pipelines. I accept the upgrade. A tolerance of `1e-4` would be more robust.

### NEW: Single-player Shapley test gap (from schema-engineer) -- LOW

The schema-engineer identifies a missing boundary test for single-player coalitional games. The formula handles this correctly (trivially returns v({player})), but an explicit test would verify the edge case. Accepted as a LOW test gap.

### NEW: Larger matrix test for is_potential_game (from spec-compliance) -- LOW

The spec-compliance agent notes all potential game tests use 2x2 matrices. A 3x3 or 3x2 test would verify the nested loop over 2x2 sub-games works for non-square matrices. Accepted as a LOW test gap.

---

## Revised Finding Table

| # | Severity | Finding | Status |
|---|----------|---------|--------|
| 1 | HIGH | is_potential_game() limited to 2-player bimatrix (math + interface + compliance) | Surviving -- unanimous |
| 2 | MEDIUM | BayesianGame prior keys not validated against type space Cartesian product | Surviving -- unanimous |
| 3 | INFO | MechanismDesignGame sparse (downgraded from LOW) | Surviving -- noted |
| 4 | INFO | Congestion game missing cost_functions field | Surviving -- noted |
| 5 | LOW | Prior tolerance 1e-6 too tight (upgraded from INFO) | Surviving -- spec-compliance concurs |
| 6 | LOW | Missing single-player Shapley test | New -- from schema-engineer |
| 7 | LOW | Missing larger-matrix potential game test | New -- from spec-compliance |
