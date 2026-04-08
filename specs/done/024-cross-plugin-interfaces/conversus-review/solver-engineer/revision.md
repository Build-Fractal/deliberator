# Solver-Engineer Revision — Spec 024: Cross-Plugin Interfaces

**Reviewer**: solver-engineer
**Round**: 1, Phase 3 (Revision)
**Date**: 2026-04-01

**Inputs**: Own review, cross-reviews received (plugin-architect, spec-compliance), cross-reviews written (about plugin-architect, spec-compliance).

---

## Positions Revised

### R1. Clarify the contradiction between Alignment 5 and R1

**Original position**: Alignment 5 stated "Q/R auto-sizing in convergence.py is correctly placed." R1 rated the Q/R mismatch as P1-Critical.

**Revision**: Both cross-reviews (plugin-architect DC-2, spec-compliance DC-3) correctly identified this as contradictory. I should have been clearer: the *caller* (`_predict_convergence_kalman`) handles the issue correctly by always passing explicit 3x3 Q/R. The *API* (`run_kalman_filter`) is defective because its defaults do not auto-size. I revise R1 from P1-Critical to **P2-Important**: the fix is defensive hardening for the API contract, not a fix for an active numerical bug. The current caller is safe. I accept the plugin-architect's revised framing of "latent API defect."

### R2. Acknowledge the deep immutability concern

**Original position**: Did not address mutation of mutable values in `plugin_results`.

**Revision**: The plugin-architect's cross-review (DC-4) correctly notes that I praised the frozen state as "properly rebuilt via model_copy" without addressing that mutable values (lists, dicts) in `plugin_results` can be mutated by consumers. Current produced values are floats, so the risk is theoretical. But if future producers store observation histories or score lists, this becomes a real numerical concern -- a consumer modifying a shared array would corrupt subsequent consumers' inputs. I endorse the plugin-architect's revised position: enforce immutable types for produced values at the orchestrator level. This is a P3 concern given current value types.

### R3. Refine the 3D vs 2D superiority argument

**Original position** (Off-Base 1): Stated that "3D observation produces better Kalman predictions than 2D is not unconditionally true" due to signal double-counting.

**Revision**: I maintain the mathematical concern but refine the framing. The plugin-architect's cross-review noted I simultaneously proposed calibration fixes (R5, R6) that assume the 3D path is worth saving. This is not contradictory -- I believe the 3D path *can* improve predictions if (a) scores are accumulated rather than replicated, (b) noise is calibrated to reflect the additional uncertainty, and (c) the double-counting risk is validated with a diagnostic. My position is: the 3D path is conditionally beneficial, not unconditionally beneficial as the spec assumes. The fixes I propose are necessary conditions for the conditional benefit to hold.

---

## Positions Maintained

### M1. SC-001 should be PARTIAL, not MET (DISPUTE)

I align with the plugin-architect: SC-001's intent is quality improvement, not syntactic data flow. The predictor reads the score, but the 3D Kalman path operates on replicated data with miscalibrated noise and a sentinel bug. The numerical benefit is not yet delivered.

**Why maintained**: Spec-compliance's methodology (check FRs and SCs against the spec text) is rigorous but misses the spec's motivating purpose. SC-001 says "ConvergencePredictor uses real eq_score" -- the emphasis should be on "real." A single score replicated across N rounds is not "real" per-round data.

### M2. Replicated-score bias fix (R2) is P1-Critical

The replicated-score problem is the most impactful numerical issue. It affects every 3D Kalman invocation, not just edge cases. The masked observation approach (2D for rounds without data, 3D for rounds with data) is the correct solution but requires more implementation effort than simple accumulation.

**Why maintained**: Spec-compliance's cross-review (DC-2) notes that the masked approach creates a "third state" not covered by current tests. This is true and is precisely why it needs a new test and potentially a new SC. The current binary 2D/3D model is an oversimplification.

### M3. R5 noise calibration is P2-Important

The eq_score noise `R[2][2] = 0.005` is too low. Equilibrium score compounds multiple noise sources and should be `0.05` (10x concession noise). This affects the quality of every 3D prediction.

**Why maintained**: Spec-compliance's cross-review (T1) argues this is "parameter tuning outside the spec's scope." From a spec-compliance perspective, this is correct -- the spec does not specify noise values. From a numerical solver perspective, miscalibrated noise directly undermines the spec's goal of improving predictions. The spec says "use real eq_score"; using it with wrong noise is worse than not using it.

### M4. Joseph form covariance update (R7) is worth implementing

**Why maintained**: Spec-compliance's cross-review (T2) correctly notes this has no connection to spec 024's FRs. I agree. But the 3D extension makes the filter more vulnerable to positive-definiteness loss because there are more off-diagonal terms. This is maintenance work justified by the spec's change in dimensionality, even though it is not a spec requirement.

### M5. End-to-end 3D Kalman test (R8) is necessary

**Why maintained**: No existing test feeds 3+ rounds of 3D observations through the actual Kalman filter and verifies state dimension, confidence bounds, and convergence behavior. Both spec-compliance and plugin-architect focus on integration-level tests (does the data flow through `execute_hooks`?). The numerical layer is untested.

---

## New Positions

### N1. Adopt the plugin-architect's duplicate producer detection recommendation

I did not address this in my original review. The plugin-architect (M1, M7) and spec-compliance (Missed Opportunity 3) both flag silent overwrite of duplicate producer keys. If two plugins produce `equilibrium_score`, the filter would receive unpredictable values depending on sort order. This is a numerical correctness concern I should have identified. I endorse P2-High for detection with a dedicated `DuplicateProducerError` (spec-compliance's suggestion of a distinct error type is correct).

### N2. The signal double-counting concern needs empirical validation before the 3D path ships

Both my Off-Base 1 and the plugin-architect's adoption of it (N1 in their revision) suggest this deserves a diagnostic. I propose: log the innovation magnitude ratio (3D innovation norm / 2D innovation norm) for deliberations where both paths could run. If the ratio is consistently > 1.0 (3D innovations are larger), the third dimension is adding noise rather than signal.

---

## Summary of Priority Changes

| Item | Original Priority | Revised Priority | Reason |
|------|------------------|-----------------|--------|
| Q/R dimension mismatch (R1) | P1-Critical | P2-Important (latent API defect) | Not currently triggered |
| Replicated-score bias (R2) | P1-Critical | P1-Critical | Unchanged |
| Score accumulation (R3) | P1-Critical | P1-Critical | Unchanged |
| Zero-score sentinel (R4) | P2-Important | P2-Important | Unchanged |
| Noise calibration (R5) | P2-Important | P2-Important | Unchanged |
| Initial covariance (R6) | P2-Important | P2-Important | Unchanged |
| Joseph form (R7) | P3-Enhancement | P3-Enhancement | Unchanged |
| 3D Kalman test (R8) | P3-Enhancement | P2-Important | Upgraded: untested numerical path |
| Singular S guard (R9) | P3-Enhancement | P3-Enhancement | Unchanged |
| Docstring drift (R10) | P3-Enhancement | P3-Enhancement | Unchanged |
| Duplicate producer detection | (new) | P2-Important | Adopted from plugin-architect |
| Signal double-counting diagnostic | (new) | P2-Important | Adopted from cross-review analysis |
