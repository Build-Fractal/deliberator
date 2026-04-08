# Cross-Review of kalman-mathematician

**Reviewer**: plugin-integration-engineer
**Reviewing**: kalman-mathematician's Phase 1 review

---

## Agreements

- **F-1 through F-5**: All verdicts are correct. The filter math is accurately assessed.
- **F-6 (Joseph form)**: Agree P3 is appropriate for max-5-round constraint.
- **F-7 (det/inverse limitation)**: Agree this is by-design and P3.

## Challenges

### On F-9 (Q/R dimension mismatch)

The mathematician rates this P2. I agree it matters but from a *wiring* perspective: if the engine or a future caller constructs Q/R incorrectly, the crash would be confusing (`IndexError` in `_mat_mul` rather than a clear dimension mismatch error). This is P1 for usability — a single assertion at `run_kalman_filter` entry point prevents a class of confusing crashes.

**Agreement with mathematician's recommendation**: Add `assert len(Q) == n and len(R) == n`.

### On F-8 (3D e2e test)

The mathematician flags this correctly. From an integration perspective, the test should also verify that the predictor plugin, when receiving 3D observations via the cross-plugin interface, produces a prediction with method="kalman" and non-None confidence_bounds. The unit-level Kalman test and the integration-level predictor test should be separate.

## Additions

### Missing: Error message quality in Kalman exceptions

When `_mat_inverse` raises `ValueError("Singular matrix -- cannot invert.")`, the fallback in `predict_convergence` catches it and logs. But the log message says "Kalman prediction failed" without indicating which step (predict, update, inverse). Adding the matrix step to the exception would improve debuggability.

**Priority**: P3 — nice-to-have for debugging.

## Overall Assessment

The kalman-mathematician's review is the deepest analysis of the filter correctness. All findings are accurate. The Q/R dimension assertion recommendation should be P1.
