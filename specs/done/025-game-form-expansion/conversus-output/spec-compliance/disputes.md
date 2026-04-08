# Phase 4 Disputes: spec-compliance

**Spec**: 025-game-form-expansion

---

## Surviving Disputes

### DISPUTE 1: is_potential_game() scope limitation (High)

**Status**: Surviving -- all three agents flag this.

FR-004 says the diagnostic is "a check applied to existing game forms." The current implementation is restricted to 2-player normal-form games. This is a compliance gap against the spec's stated scope.

**My position**: The spec should be amended to clarify that Phase 1 implements the 2-player diagnostic, with N-player generalization deferred. This keeps the implementation compliant while acknowledging the limitation.

### DISPUTE 2: SC-005 threshold mismatch (Low)

**Status**: Surviving -- spec says >= 10 forms, implementation has 9.

The 10th form would need to be either an additional game form (evolutionary, mean-field, auction-specific) or counting the potential diagnostic as a form. Since FR-004 explicitly says potential is not a form, the spec threshold should be amended.

### DISPUTE 3: BayesianGame prior key validation (Medium)

**Status**: Surviving -- all agents agree this validation is missing.

The prior dict accepts arbitrary keys. A validator checking keys against the type space Cartesian product would catch configuration errors at model validation time rather than at solver runtime.

## Withdrawn Disputes

- FR-004 verdict: Revised to PASS after cross-review consensus
- YAML example coverage: Now properly credited in the assessment
