# Feature Specification: Kalman/Convergence Fixes

**Feature ID**: `034-kalman-convergence-fixes`
**Created**: 2026-04-01
**Status**: Draft
**Files**: `conversus/plugins/nashopt/convergence.py`, `kalman.py`, `predictor.py`, `tests/test_kalman.py`, `tests/test_convergence.py`, `tests/test_cross_plugin.py`

---

## Items (9)

### CRITICAL
- **C-2**: Accumulate eq_scores across rounds. predictor.py:255-261 wraps current score in single-element list. Fix: persist scores in RoundState or predictor history. `_equilibrium_trend` needs 2+ points for real slope.
- **C-3**: Fix zero-score sentinel. convergence.py:268-271 `any(s != 0.0)` discards legit zero scores. Fix: use `None` sentinel for "absent", allow `0.0` as a real value. Invert test `test_2d_with_all_zero_eq_scores`.

### HIGH
- **NEW-1**: Auto-size default Q/R in `run_kalman_filter` from observation dimension. Current `default_Q()`/`default_R()` always return 2x2. Future callers omitting explicit Q/R with 3D data get silent corruption.

### MEDIUM
- **M-1**: 3D Kalman end-to-end test. Feed 3+ rounds of 3D observations, verify state dimension, confidence bounds, convergence.
- **M-5**: Calibrate R[2][2] for eq_score. Current 0.005 trusts it as much as concession_rate. Recommended: 0.05.
- **NEW-7**: Tune initial P for eq_score. P=1.0 too wide for [0,1] range. Recommended: 0.25.
- **RE-1**: Verify Q/R dimension mismatch is fully resolved (defense in depth).

### LOW
- **NEW-2**: Empirical 3D validation — log innovation magnitude ratio (3D/2D) to prove 3D actually helps before shipping as default.
- **NEW-6**: Joseph form covariance update for numerical stability over many 3D iterations.

## Success Criteria
- SC-001: eq_score trend slope is non-zero after 3 rounds with varying scores.
- SC-002: Score of 0.0 enters 3D filter (not discarded as absent).
- SC-003: `run_kalman_filter()` with 3D observations and no explicit Q/R produces 3x3 state.
- SC-004: 3D e2e test passes with realistic observation sequences.
