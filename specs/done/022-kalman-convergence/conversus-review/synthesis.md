# Conversus Review Synthesis -- Spec 022 Kalman Convergence

**Phase**: 5 (final synthesis)
**Date**: 2026-04-01
**Reviewers**: solver-engineer, plugin-engineer, spec-compliance
**Spec**: 022-kalman-convergence

---

## Overall Assessment

The Kalman-filtered convergence prediction implementation is architecturally sound, mathematically correct for its stated model, and backward-compatible. The pure Python 3x3 matrix library avoids the scipy dependency entirely. The OLS fallback is preserved and untouched. Test coverage is comprehensive at 1002 lines covering matrix operations, filter mechanics, all four success criteria, plugin integration, and package exports.

Three compliance gaps and one quality gap require remediation before the implementation fully satisfies the spec. All are well-scoped with clear fix paths.

---

## Compliance Summary

| Requirement | Verdict | Notes |
|---|---|---|
| FR-001 | MET | Kalman always available (pure Python), auto activates at 2 rounds |
| FR-002 | MET | OLS fallback via method="ols", auto <2 rounds, or exception |
| FR-003 | MET | 3D state vector [dispute_count, concession_rate, eq_score] |
| FR-004 | MET | Confidence intervals from P[0][0] with 1.96-sigma default |
| FR-005 | PARTIALLY MET | Uses state deltas, not innovation sequence. See Remediation 1 |
| FR-006 | MET | method and confidence_bounds in PluginResult.data |
| FR-007 | PARTIALLY MET | Function layer supports Q/R; plugin config not wired. See Remediation 2 |
| FR-008 | MET | Kalman path computes own rounds_remaining |
| SC-001 | MET | Kalman confidence >= OLS confidence for 5->3->1 |
| SC-002 | PARTIALLY MET | Test assertion relaxed (0.5x threshold). See Remediation 3 |
| SC-003 | MET | Non-linear convergence correctly handled |
| SC-004 | MET | OLS behavior identical to pre-022 |

**Constraints**: All 4 constraints satisfied (no scipy, no interface change, no OLS breakage, 2-point minimum).

---

## Consensus Findings (All 3 Reviewers Agree)

1. **FR-005 innovation sequence gap is the most significant compliance issue.** The innovation vector is computed in `kalman_update()` (line 289 of kalman.py) but discarded. `detect_fixed_point()` checks state estimate deltas instead. The spec explicitly requires the innovation sequence.

2. **FR-007 plugin config wiring for Q/R is missing.** The `predict_convergence()` function accepts Q/R parameters, but `ConvergencePredictor.execute()` does not read them from plugin config.

3. **SC-002 test assertion is too relaxed.** The test uses `stag_width >= conv_width * 0.5` but the spec says "wider confidence bounds."

4. **Confidence calibration formula depends on arbitrary initialization.** `1 - trace(P_final) / trace(P_initial)` is sensitive to the `initial_P` choice, not the observation data. This affects prediction classification reliability.

5. **Equilibrium scores are not wired through.** The third state dimension (eq_score) is always 0.0, degrading filter effectiveness.

6. **Method validation for `convergence_method` config is needed.** Unrecognized values silently resolve to OLS.

7. **F=I (random walk model) is correct for deliberation systems.** No physics/momentum in dispute dynamics. Kalman gain adapts to trends naturally.

8. **The 2-round auto threshold is spec-aligned.** Matches the spec's "2 data points minimum" constraint.

9. **Pure Python approach is superior to optional scipy.** Simpler, no import-time checks, no dependency management.

---

## DISPUTES_BEGIN

### Dispute A: Granularity of Kalman exception recovery

**Solver-engineer**: Catch singular matrix inside `kalman_update()`, return prior state, preserve Kalman state history. OLS fallback should be reserved for structural failures.

**Plugin-engineer**: Both inner recovery (per-observation) and outer recovery (OLS fallback) should exist. Additionally, add `fallback_reason` to output data when outer fallback triggers.

**Spec-compliance**: No position on the mechanism, but any fallback should maintain `method: "ols"` per FR-006 (not a new variant like `"ols_fallback"`).

**Resolution path**: Implement two-layer recovery: inner catch in `kalman_update()` for singular matrix (returns prior), outer catch in `predict_convergence()` for structural failures (falls back to OLS with `fallback_reason` in output). `method` field stays `"ols"` per FR-006.

---

### Dispute B: Whether FR-004 confidence calibration gap warrants a compliance downgrade

**Solver-engineer**: Confidence calibration flaw affects prediction reliability. Should be tracked as a compliance gap.

**Plugin-engineer**: Point confidence drives `min_confidence` classification. Unreliable confidence means unreliable classification.

**Spec-compliance**: FR-004 specifies "calibrated confidence intervals." The intervals (from P[0][0]) are calibrated. The point confidence is a derived internal metric not specified in FR-004. FR-004 remains MET. The calibration flaw is a quality issue tracked separately.

**Resolution path**: FR-004 remains MET with a compliance note. The confidence calibration fix is prioritized as quality P1 (not compliance P1) and ships in the same PR as the compliance fixes.

---

### Dispute C: Priority ordering of the remediation backlog

**Solver-engineer**: Confidence calibration should be P1 (affects prediction reliability).

**Plugin-engineer**: Method validation should be P1 (prevents silent misconfiguration). Confidence calibration can be fixed independently of equilibrium score wiring.

**Spec-compliance**: Two-tier P1: compliance tier (FR-005, FR-007, SC-002) and quality tier (confidence calibration, method validation). Both ship together.

**Resolution path**: Adopt the two-tier approach. Compliance P1 items (FR-005, FR-007, SC-002 test) are the merge gate. Quality P1 items (confidence calibration, method validation) ship in the same PR but can be reviewed independently. Equilibrium score wiring is P2.

## DISPUTES_END

---

## Remediation Plan

### Tier 1: Compliance (must fix before merge)

**Remediation 1 -- FR-005: Innovation sequence for fixed-point detection**
- Modify `kalman_update()` to return or store the innovation vector `z - H*x_pred`.
- Introduce a `KalmanTrace` or extend `KalmanState` with an `innovation: Vec3` field.
- Rewrite `detect_fixed_point()` to accept innovation magnitudes and check those.
- Update tests to verify innovation-based detection.
- **Owner**: solver-engineer
- **Effort**: Small (the innovation is already computed on line 289; it just needs to be surfaced)

**Remediation 2 -- FR-007: Wire Q/R from plugin config**
- In `ConvergencePredictor.execute()`, add:
  ```python
  Q = config.get("process_noise_Q")
  R = config.get("observation_noise_R")
  ```
- Pass `Q=Q, R=R` to `predict_convergence()`.
- Add integration test verifying config passthrough.
- **Owner**: plugin-engineer
- **Effort**: Trivial (3-5 lines of code + test)

**Remediation 3 -- SC-002: Tighten test assertion**
- Replace `stag_width >= conv_width * 0.5` with `stag_width >= conv_width`.
- If the test fails under current defaults, adjust noise parameters to ensure wider stagnation bounds, or add a separate controlled test.
- **Owner**: spec-compliance
- **Effort**: Trivial (1 line change + possible noise parameter adjustment)

### Tier 2: Quality (ship in same PR, review independently)

**Remediation 4 -- Confidence calibration**
- Replace `1 - trace(P_final) / trace(P_initial)` with a formulation invariant to initialization.
- Candidates: `1 - trace(P_final) / trace(P_initial + Q)` (first prediction step), or normalized innovation squared (NIS) averaged over the sequence.
- Update `compute_kalman_confidence()` and its tests.
- **Owner**: solver-engineer
- **Effort**: Small

**Remediation 5 -- Method validation**
- Validate `convergence_method` in `ConvergencePredictor.execute()` against `("auto", "kalman", "ols")`.
- Log warning and default to `"auto"` for unrecognized values.
- Add test for invalid config.
- **Owner**: plugin-engineer
- **Effort**: Trivial

### Tier 3: Enhancement (separate PR)

**Remediation 6 -- Wire equilibrium scores**
- Connect EquilibriumScorer output to the convergence predictor.
- Resolve the TODO in predictor.py line 257.
- Validate that the Kalman filter's third dimension produces meaningful state estimates with real scores.
- **Owner**: plugin-engineer
- **Effort**: Medium (requires understanding inter-plugin data flow)

**Remediation 7 -- Observation validation**
- Add `math.isfinite()` checks for each observation element in `run_kalman_filter()`.
- Skip update and log warning for invalid observations.
- **Owner**: solver-engineer
- **Effort**: Trivial

**Remediation 8 -- Fallback observability**
- Add `fallback_reason: str | None` to `PluginResult.data` when the Kalman-to-OLS exception fallback triggers.
- Implement two-layer recovery: inner catch in `kalman_update()` for singular matrix, outer catch for structural failures.
- **Owner**: plugin-engineer
- **Effort**: Small

---

## Files Referenced

| File | Lines | Role |
|---|---|---|
| `specs/done/022-kalman-convergence/spec.md` | 87 | Feature specification |
| `conversus/plugins/nashopt/kalman.py` | 436 | Kalman filter core |
| `conversus/plugins/nashopt/convergence.py` | 703 | Convergence prediction with Kalman/OLS dispatch |
| `conversus/plugins/nashopt/predictor.py` | 296 | Plugin wrapper with config handling |
| `conversus/plugins/nashopt/__init__.py` | 67 | Package exports |
| `tests/test_kalman.py` | 1002 | Test suite |
