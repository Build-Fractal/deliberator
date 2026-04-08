# statistician Cross-Review of plugin-engineer

**Cross-reviewer**: statistician
**Reviewing**: plugin-engineer Phase 1 review of spec 022
**Date**: 2026-04-01

---

## Agreements

### 1. Broad exception catch is a real concern

plugin-engineer correctly identifies that catching all exceptions masks bugs. A `TypeError` from passing wrong types to matrix operations would be silently converted to an OLS fallback. The suggestion to narrow to `(ValueError, ArithmeticError)` is sound. I would add `ZeroDivisionError` since the matrix inverse can encounter near-zero determinants that might produce division errors in edge cases.

### 2. confidence_bounds documentation needs improvement

The Optional field semantics (None for OLS, populated for Kalman) should be explicitly documented. Consumers should not have to inspect `method` to know whether `confidence_bounds` is populated.

### 3. Q/R threading is correct

The parameter threading from `predict_convergence()` through `_predict_convergence_kalman()` to `run_kalman_filter()` to `kalman_update()` is correctly traced. The default functions (`default_Q()`, `default_R()`) are called at each level when None is passed, which is correct (avoids mutable default argument issues).

---

## Tensions

### 1. Exception handling philosophy

plugin-engineer recommends catching specific exceptions and letting unexpected ones propagate. From a statistical perspective, I would argue for a different approach: catch all exceptions in production, but log at ERROR level (not WARNING) for unexpected types. The Kalman filter is a probabilistic model -- it should never crash the system. But unexpected errors should trigger alerts, not be silently handled.

The tension is between plugin-engineer's "fail fast during development" and my "never crash in production." Both are valid. The resolution is environment-aware logging: WARNING for expected failures (singular matrix, bad data), ERROR for unexpected failures (TypeError, AttributeError).

---

## Missed Opportunities

### 1. No assessment of numerical conditioning

plugin-engineer reviews the dispatch logic and integration pattern but does not assess the numerical properties of the Kalman filter. Key questions:
- What happens when the innovation covariance S is nearly singular? The `_mat_inverse(S)` call will raise `ValueError` (detected by `abs(det) < 1e-12`). This is caught by the broad exception handler and falls back to OLS. Is this the right behavior? I would argue yes -- a singular S means the observation provides no information gain, so falling back to the simpler model is correct.
- What is the condition number of typical S matrices? With the default Q and R, S = P + Q + R. For early rounds (P large), S is well-conditioned. For later rounds (P small), S approaches Q + R, which is diagonal and well-conditioned. So numerical issues are unlikely in practice.

### 2. No discussion of the observation construction

plugin-engineer does not review `_build_observation_sequence()`, which transforms `RoundFeatures` into `[dispute_count, avg_concession_rate, eq_score]` vectors. This is where data enters the Kalman filter and is critical for correctness. Two concerns:
- The concession rate is averaged across agents. If agents have very different concession rates (e.g., one at 0.0 and one at 0.8), the average (0.4) hides the bimodality. The Kalman filter assumes Gaussian observations -- a bimodal distribution violates this assumption.
- The equilibrium score defaults to 0.0 when not provided. This means the Kalman filter starts with a zero equilibrium score and updates from there. If the actual equilibrium score is high (e.g., 0.8), the initial zero will pull the filtered estimate down until enough observations correct it.
