# Phase 3 Revision: test-coverage-auditor

**Date**: 2026-04-01

---

## Cross-Reviews Received From

- **consistency-auditor**: 3 DCs, 4 Ts, 3 SAs
- **dependency-auditor**: 3 DCs, 3 Ts, 3 SAs
- **implementation-verifier**: 3 DCs, 4 Ts, 4 SAs

---

## Recommendation Dispositions

### CRITICAL #1: Add SC-001/SC-002 threshold tests for spec 021
**Status**: MAINTAINED — the consistency-auditor (T-2) argues the scaffold test should be ranked higher due to cross-spec architectural impact. I maintain that spec 021's acceptance criteria are more critical because they are the foundation for the solver layer that specs 022, 023, 025, and 026 depend on. **Rationale: a spec without passing acceptance criteria is fundamentally unvalidated; a spec with a known bug in a related spec is at least partially validated.**

However, I accept the consistency-auditor's point that these are different scopes. **Amended: create two CRITICAL categories — "acceptance criteria gaps" (SC-001/SC-002 tests) and "cross-spec regression gaps" (scaffold YAML test, DomainScore.variables test). Both are CRITICAL, for different reasons.**

### HIGH #2: Add error-path `solver` key test for spec 021
**Status**: MAINTAINED — the implementation-verifier (DC-2 in their review of me) notes that the `solver` key belongs on `PluginResult` in the plugin wrapper, not in `solver.py`. **Amended: the test should assert `"solver" in result.data` on error paths in the plugin wrapper test file (likely `test_equilibrium_scorer.py`), not in `test_solver.py`. If no such test file exists, create one.**

### HIGH #3: Replace mock timeout test with real blocking test for spec 021
**Status**: MAINTAINED — no reviewer challenged this. The implementation-verifier's Off-Base Assumption #1 (mock tests bypass real post-processing) strengthens the case. **No amendment needed.**

### HIGH #4: Tighten SC-002 assertion in test_kalman.py
**Status**: MAINTAINED WITH RISK NOTE — the implementation-verifier (T-3) notes the test "WILL fail with the tighter assertion" due to Kalman confidence formula's initialization dependence. **Amended: the tightening should be accompanied by a parameter adjustment. If the test fails with `stag_width >= conv_width`, investigate whether adjusting the stagnation sequence (not the assertion threshold) produces the expected behavior. If it does not, this is a spec compliance failure, not just a test failure.**

### MEDIUM #5: BayesianGame prior key validation test
**Status**: MAINTAINED — no opposition.

### MEDIUM #6: Constraint gap_question tests for spec 026
**Status**: MAINTAINED — no opposition.

### MEDIUM #7: YAML scaffold loading test for spec 030
**Status**: UPGRADED TO CRITICAL — accept the consistency-auditor's DC-1 and T-1: this test would immediately surface CSI-1, confirming the cross-spec bug with a single test. The consistency-auditor's new recommendation R-11 (write failing tests for CSI-1 and CSI-2 before fixing code) aligns with my test-first philosophy. **Amended: write this test as part of the R-11 batch, expect it to fail, then fix R-1.**

### LOW #8: Two-domain isolation test for spec 030
**Status**: MAINTAINED — no opposition, no urgency change.

### MEDIUM #9: Post-processing mapping test for spec 021 red-blue mode
**Status**: MAINTAINED, NO LONGER BLOCKED — accept the implementation-verifier's DC-3: tests can be written against current (buggy) behavior to establish a regression baseline. The test would document the current behavior (which may include the dimension mismatch runtime error the implementation-verifier identified). **Amended: write the test, expect it to reveal the dimension mismatch. This becomes a failing test that documents the bug.**

### MEDIUM #10: Innovation-sequence fixed-point detection test for spec 022
**Status**: MAINTAINED, PARTIALLY UNBLOCKED — the implementation-verifier's Fix 3 amendment breaks this into 3 steps: (a) add field, (b) store innovation, (c) update detection. Tests for steps a/b can be written now. Step c remains blocked by design decision. **Amended: write tests for innovation storage (steps a/b) now. Detection test (step c) remains blocked.**

---

## New Recommendations

### CRITICAL-NEW-1: Write failing tests for ALL cross-spec P1 findings (CSI-1 through CSI-4)

Accept the consistency-auditor's R-11. Expand scope to all 4 CSIs:
- **CSI-1 test**: Load a `.yml` scaffold through `DomainPlugin.score()`. Expected: fails (`.json` hardcoded).
- **CSI-2 test**: Assert `DomainScore.variables` is populated after `CodeReviewDomain.score()`. Expected: fails (variables not passed).
- **CSI-3 test**: Pass non-zero equilibrium scores through the Kalman filter. Expected: passes but reveals initialization-dependent confidence. (This is a characterization test, not a bug-confirming test, since the bug is dormant.)
- **CSI-4 test**: Assert `"solver"` key exists on `PluginResult` error-path returns in both nashopt and optimizer plugin wrappers. Expected: fails for at least one path.

These 4 tests collectively validate the cross-spec findings and create regression protection.

### HIGH-NEW-1: Add integration test for the 029/030 scoring pipeline

The consistency-auditor identified that `CodeReviewDomain` reimplements the scoring pipeline instead of delegating to `super().score()`. An integration test that runs code-review inputs through both `DomainPlugin.score()` and `CodeReviewDomain.score()` and compares results would:
1. Document the current behavioral divergence
2. Serve as a regression test when the refactor (consistency-auditor R-3) lands
3. Test the 029-to-030 dependency that the dependency-auditor identified

This is the first cross-spec integration test and addresses my Missed Opportunity #1.

---

## Position Summary

The cross-reviews refined my recommendations without challenging my core finding: **41% P1 test coverage is inadequate and the gap pattern is systematic** (the most critical findings are the least tested). The main adjustments:

1. **Priority split**: Accept the consistency-auditor's argument that cross-spec regression tests deserve CRITICAL status alongside acceptance criteria tests. The revised priority system has two CRITICAL categories.

2. **Unblocking "blocked" tests**: The implementation-verifier correctly noted that tests can be written against current (buggy) behavior. I unblocked recommendations #9 and #10 and reframed them as characterization/failing tests rather than post-fix validation tests.

3. **Cross-spec failing tests (R-11 expansion)**: The consistency-auditor's R-11 is the single most valuable new recommendation from the cross-review process. Expanding it to all 4 CSIs creates a cross-spec regression test suite that did not exist before.

4. **File attribution corrections**: The implementation-verifier's correction that `PluginResult` error-path tests belong in the plugin wrapper test file, not `test_solver.py`, is accepted. This changes where the test is written but not what it tests.

My overall assessment is unchanged: the test suite is strong for lower-risk behavior and weak for the highest-risk P1 findings. The cross-review process produced actionable adjustments to my recommendations, particularly around test sequencing and the creation of cross-spec regression tests.
