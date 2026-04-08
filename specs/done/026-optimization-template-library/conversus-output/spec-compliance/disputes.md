# Phase 4 Disputes: spec-compliance

**Spec**: 026-optimization-template-library

---

## Surviving Disputes

### DISPUTE 1: Cross-reference validation gaps (Low)

**Status**: Surviving -- all three agents flag this.

Two cross-reference validation gaps exist:
1. Template game_form values not checked against game-forms/*.yml
2. Template mode_compatibility values not checked against mode-mapping.yml

These are test coverage gaps, not implementation gaps. The actual values are all valid today, but the tests do not enforce this invariant.

## Withdrawn Disputes

- SC-004 revised to PASS after cross-review consensus
- PSD and supply-demand validation correctly deferred to solver layer
