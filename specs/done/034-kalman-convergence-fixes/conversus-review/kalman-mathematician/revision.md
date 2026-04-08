# Kalman-Mathematician — Phase 3 Revision

**Incorporating cross-review feedback from**: plugin-integration-engineer, spec-compliance

---

## Revisions

### F-9 (Q/R dimension mismatch): Upgraded to P1

Both reviewers argue the dimension mismatch would cause a confusing `IndexError` crash in `_mat_mul`, not silent corruption. I accept this: an explicit assertion is crash prevention, which is P1 defense-in-depth.

**Revised priority**: P1. Add `assert len(Q) == n and all(len(row) == n for row in Q)` at `run_kalman_filter` entry.

### F-4 (History roundtrip): Agree with REQUIRED-ELSEWHERE

I originally rated this as out-of-scope. Both reviewers confirm: spec 034 does not own engine persistence. The correct action is to track this in the engine pipeline spec.

**Revised status**: REQUIRED-ELSEWHERE (engine spec).

### F-8 (3D e2e test): Accept enhanced criteria

The spec-compliance agent correctly notes that a 3D e2e test must verify mathematical properties (PSD, narrowing bounds), not just "no exception." I add this to my open recommendations.

### New: Q/R passthrough from plugin config (from integration engineer)

I accept this as a P3 wiring gap. The `ConvergencePredictor` plugin does not forward `plugin_config.get("Q")` or `plugin_config.get("R")` to the convergence module. This means user-configured Q/R in conversus.yml has no effect.

### New: test_2d_with_all_zero_eq_scores inversion (from spec-compliance)

I accept this as a P2 compliance gap. The spec explicitly calls for inverting this test. Verification needed.

## Concessions

- I concede that F-4 (history roundtrip) is not a spec 034 concern but an engine concern.
- I upgrade F-9 from P2 to P1 based on the crash analysis.

## Maintained Positions

- F-6 (Joseph form) remains P3 — acceptable for max-5-round constraint.
- F-7 (det/inverse 3x3 limit) remains P3 — no 4D state expected.
