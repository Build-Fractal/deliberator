# Spec-Compliance — Phase 3 Revision

**Incorporating cross-review feedback from**: kalman-mathematician, plugin-integration-engineer

---

## Revisions

### RE-1 (Q/R dimension mismatch): Upgraded to P1

Both reviewers present compelling arguments. The crash path (IndexError in _mat_mul) is a real failure mode when callers provide explicit Q/R with wrong dimensions. An assertion at `run_kalman_filter` entry converts a confusing crash into a clear error message.

**Revised**: PARTIAL / P1.

### SC-004: Enhanced criteria from mathematician

I accept the strengthened test requirements:
1. State dimension is 3 throughout
2. P remains positive semi-definite
3. Confidence bounds narrow over converging sequence
4. Innovation magnitude decreases

**Revised**: SC-004 remains CONDITIONAL but with explicit criteria.

### New: test_2d_with_all_zero_eq_scores inversion

I should have caught this in Phase 1. The spec explicitly says "Invert test." If the test was not updated, it is a compliance gap.

**Priority**: P2 — test correctness.

### SC-001 engine dependency (from integration engineer)

I accept that SC-001 implicitly depends on engine persistence of plugin_results. Adding a note: "SC-001 PASS assumes engine persists plugin_results into RoundState.plugin_results for completed rounds."

## Concessions

- RE-1 upgraded from P2 to P1.
- SC-004 criteria strengthened.
- Added test inversion compliance gap.

## Maintained Positions

- Overall compliance score remains 7/9 MET, 1/9 PARTIAL (RE-1), 1/9 DEFERRED (NEW-6).
- Both CRITICALs (C-2, C-3) are correctly implemented.
