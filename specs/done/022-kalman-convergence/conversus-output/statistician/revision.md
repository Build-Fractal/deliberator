# Phase 3 Revision: statistician

**Agent**: statistician
**Spec**: 022-kalman-convergence
**Date**: 2026-04-01
**Inputs**: plugin-engineer cross-review, spec-compliance cross-review

---

## Disposition of Original Recommendations

### P1-1. Document initial covariance bias -- MAINTAINED

**Original**: Document that `diag(10, 1, 1)` makes confidence 83% dispute-driven.

**Cross-review response**: plugin-engineer agrees it is worth documenting. spec-compliance does not dispute.

**Priority**: Remains P1.

---

### P2-1. Consider Joseph form for covariance update -- MODIFIED to P3

**Original**: Recommend Joseph form for numerical stability.

**Cross-review challenges**:
- plugin-engineer argues the Joseph form adds code complexity for a theoretical benefit.
- spec-compliance classifies it as P3, noting neither form is specified and the simple form is correct for the expected input range.

**Revised position**: I accept the downgrade. The Joseph form is mathematically superior but the practical benefit for 3x3 diagonal-dominant matrices is negligible. Keep the simple form with a code comment noting the Joseph form as an option if numerical issues are observed.

**Priority**: Downgraded to P3.

---

### P2-2. Validate default Q and R values -- MODIFIED

**Original**: Validate Q and R across a range of deliberation patterns.

**Cross-review challenges**:
- plugin-engineer suggests a lighter approach: test that the filter does not diverge for extreme inputs.
- spec-compliance notes that R[0][0] = 0.5 seems high for integer dispute counts with near-zero extraction noise.

**Revised position**: I accept plugin-engineer's lighter approach AND incorporate spec-compliance's observation. The specific concern: R[0][0] = 0.5 models observation noise on dispute counts. Since disputes are extracted as integers from structured output, extraction noise should be near-zero. R[0][0] = 0.5 is conservative (the filter trusts the process model over observations), which produces smoother estimates but slower responsiveness. This is arguably the right trade-off for a predictor (smoothness over reactivity), but it should be documented.

**Priority**: Remains P2 (with narrower scope).

---

### P3-1. Configurable fixed-point threshold -- MAINTAINED

**Original**: Consider making the 0.1 threshold configurable.

**Cross-review response**: No objections.

**Priority**: Remains P3.

---

## New Recommendations from Cross-Reviews

### N-1. Observation construction bimodality concern (from my cross-review of plugin-engineer)

The `_build_observation_sequence()` function averages concession rates across agents. If agents have very different rates (e.g., one rigid, one flexible), the average hides the distribution. The Kalman filter assumes Gaussian observations. A bimodal concession rate distribution violates this assumption.

**Recommendation**: Document that the Kalman filter operates on agent-averaged features and that heterogeneous agent behavior may reduce filter accuracy. Consider adding agent-count-weighted variance as a second dimension in future iterations.

**Priority**: P2 (documentation) / P3 (future enhancement).

---

### N-2. Initial state sensitivity (from plugin-engineer MO-2)

plugin-engineer raises a valid concern: the initial state is set from the first round's raw observation. An outlier first round biases the entire filter. The high initial P (diag(10, 1, 1)) mitigates this -- the filter will correct quickly with subsequent observations. But for very short deliberations (2 rounds), the first observation has outsized influence.

**Recommendation**: For the initialization concern, the high initial P is the standard Kalman approach ("uninformative prior"). The filter will converge within 2-3 updates even with a bad initial estimate. No code change needed, but document the sensitivity for 2-round deliberations.

**Priority**: P3 (documentation).

---

### N-3. Asymptotic confidence ceiling (from spec-compliance MO-2)

spec-compliance calculates that confidence plateaus at ~91.5% after many rounds (steady-state P approaches Q). This is correct and desirable: irreducible process noise means confidence should never reach 100%. But if a user expects confidence to reach 0.95 after enough rounds, they will be surprised.

**Recommendation**: Document the asymptotic confidence ceiling in the default_Q docstring.

**Priority**: P3 (documentation).
