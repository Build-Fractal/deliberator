# Phase 3 Revision: plugin-engineer

**Agent**: plugin-engineer
**Spec**: 022-kalman-convergence
**Date**: 2026-04-01
**Inputs**: statistician cross-review, spec-compliance cross-review

---

## Disposition of Original Recommendations

### P1-1. Narrow exception catch -- MODIFIED

**Original**: Catch `(ValueError, ArithmeticError)` explicitly. Let unexpected exceptions propagate.

**Cross-review response**: statistician suggests catching all exceptions in production but logging at ERROR for unexpected types. spec-compliance notes the broad catch does not violate any FR.

**Revised position**: I accept the compromise. Catch all exceptions but differentiate logging levels:
- `(ValueError, ArithmeticError, ZeroDivisionError)`: WARNING (expected Kalman failures).
- All other exceptions: ERROR (unexpected, indicating a bug).

Both fall back to OLS, but ERROR-level logging triggers alerts in production monitoring.

**Priority**: Remains P1.

---

### P2-1. Clarify confidence_bounds documentation -- MAINTAINED

**Original**: Document when confidence_bounds is None vs. populated.

**Cross-review response**: spec-compliance notes the type annotation IS documentation (Optional). statistician agrees documentation would help.

**Priority**: Remains P2. The type annotation is necessary but not sufficient. A docstring explaining the semantics (None for OLS, populated for Kalman) helps consumers who do not read type annotations.

---

### P2-2. Add __all__ to convergence.py -- MAINTAINED

No cross-review comments.

**Priority**: Remains P2.

---

### P3-1. Configurable auto-dispatch threshold -- WITHDRAWN

**Original**: Consider making the 2-round threshold configurable.

**Cross-review challenge (spec-compliance T-2)**: The threshold is an implementation choice within the spec's intent. Making it configurable adds API surface without spec justification.

**Revised position**: I accept the withdrawal. The 2-round threshold is well-motivated (minimum for meaningful Kalman updates) and does not need user configurability.

---

## New Recommendations from Cross-Reviews

### N-1. Review convergence.py classification logic (from spec-compliance MO-1)

spec-compliance raises a valid concern about the if/elif chain in `_predict_convergence_kalman()`. The 9-branch classification logic maps Kalman state to user-facing predictions. Edge cases:

- `dispute_est = 0.99` with fixed_point -> "converge" (threshold is 1.0). Is this correct? A fixed point at 0.99 disputes means the system has stabilized near (but not at) zero. The prediction is reasonable.
- `dispute_delta = 0.0001` (very small negative) -> "converge" branch. Technically decreasing but effectively flat. The confidence check mitigates this: very small deltas produce low confidence -> "uncertain."

**Recommendation**: Add test cases for edge values near the classification boundaries (dispute_est near 1.0, dispute_delta near 0.0).

**Priority**: P2.

---

### N-2. Verify OLS path produces identical results (from spec-compliance MO-1)

spec-compliance asks whether extracting OLS into a named function introduced bugs. This is a valid regression concern.

**Recommendation**: Add a regression test that compares OLS output before and after spec 022 refactoring. Alternatively, verify by code diff that `_predict_convergence_ols()` is byte-for-byte identical to the original `predict_convergence()` (minus the dispatch logic).

**Priority**: P2.
