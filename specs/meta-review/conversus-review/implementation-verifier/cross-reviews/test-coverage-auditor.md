# Cross-Review: implementation-verifier reviewing test-coverage-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: The 41% P1 coverage finding does not change the accuracy of verified code claims, but changes their reliability

The test-coverage-auditor finds 59% of P1 findings have no test coverage. My verification checked actual code (not test code) and confirmed 18/21 claims match the implementation. The 41% coverage gap means: the code I verified *is* what the syntheses describe, but whether it *works correctly at runtime* is unverified for the majority of P1 items. This is a subtle but important distinction. My "VERIFIED" verdict means "the code says what the synthesis claims." The test-coverage-auditor's "NO TEST" verdict means "the code has not been proven to work." Both can be simultaneously true, and both matter.

### DC-2: Off-Base Assumption #1 (mock nashopt coverage) is more severe than the test-coverage-auditor states

The test-coverage-auditor notes that `TestMockNashoptIntegration` "bypasses the actual `_score_from_solver` post-processing function." My verification found that the 021 synthesis attributes `PluginResult` error-path behavior to `solver.py`, but `solver.py` only returns `SolverResult` — the `PluginResult` wrapping happens in the plugin wrapper. This means the mock tests not only bypass post-processing (the test-coverage-auditor's finding) but are also testing at the wrong abstraction level (my finding). The mock creates `SolverResult` objects and patches at the scorer level, skipping both the `solver.py -> PluginResult` conversion AND the post-processing. The test gap is two layers deep, not one.

### DC-3: "Blocked" test recommendations may not actually be blocked

The test-coverage-auditor marks several recommendations as "blocked by code change" (e.g., innovation sequence test blocked by Remediation 1, post-processing mapping test blocked by P1-5). My verification shows the current code has specific, well-defined behavior at those locations. Tests could be written against the *current* (buggy) behavior to establish a regression baseline, then updated when the fix lands. Marking them as "blocked" implies tests can only be written after the fix, which is not true. Regression tests that document current behavior are valuable even for known bugs.

---

## Tensions

### T-1: The "VERIFIED" bar

My verification standard is: does the code match the synthesis claim? The test-coverage-auditor's standard is: does a test exercise the claimed behavior? These are different bars. A claim can be "VERIFIED by code reading" and "UNTESTED by test execution." Consumers of both reports need to understand that my 86% accuracy rate describes synthesis-to-code alignment, while the test-coverage-auditor's 41% rate describes code-to-test alignment. The combined pipeline is: synthesis -> code (86% accurate) -> test (41% covered).

### T-2: Priority of test gaps

The test-coverage-auditor's #1 CRITICAL recommendation is spec 021 SC-001/SC-002 threshold tests. My own priority would be the `DomainScore.variables` bug fix (which I confirmed) plus the scaffold extension fix (which I confirmed), because these are cross-spec bugs that affect the domain plugin architecture — the foundation for future domains. SC-001/SC-002 are important but are single-spec acceptance criteria. The test-coverage-auditor prioritizes by coverage criticality; I would prioritize by architectural impact.

### T-3: The SC-002 relaxed assertion

The test-coverage-auditor notes spec 022's SC-002 test uses `stag_width >= conv_width * 0.5` instead of `stag_width >= conv_width`. The synthesis marks this as PARTIALLY MET and says "1 line change." The test-coverage-auditor correctly notes this "underestimates the effort if the assertion change causes the test to fail with current defaults." My verification of the Kalman confidence formula (initialization-dependent) suggests the test WILL fail with the tighter assertion, because the confidence formula's sensitivity to initialization means the bounds may not behave as the spec expects. The "1 line change" framing is optimistic.

### T-4: Spec 029 base layer availability

The test-coverage-auditor notes `pytest.skip("Base layer not yet available")` in spec 029 tests. I did not encounter this in my verification because I read source code, not test execution logs. This is a runtime concern invisible to my static verification. If the base layer is unavailable at test time, the coupling I verified (`code_review/domain.py` imports from `domains/base`) may produce import errors in CI.

---

## Safe Agreements

### SA-1: Specs 025 and 026 have the best verification + coverage alignment

My verification found all 6 claims across specs 025 and 026 to be VERIFIED. The test-coverage-auditor found all SC tests present and passing. Both agree these specs are the healthiest in the batch.

### SA-2: The DomainScore.variables bug is confirmed at every level

I verified the bug in code. The test-coverage-auditor confirms no test covers it. The consistency-auditor identifies its cross-spec impact. This is the most thoroughly triangulated finding across all four reviews.

### SA-3: The HAS_AMPL guard gap has no test coverage

I verified the import guard code. The test-coverage-auditor confirms `TestHasAMPLFlag` does not test for `highspy` presence. Both agree the bug is real and the fix is straightforward.
