# Cross-Review: test-coverage-auditor reviewing consistency-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: Cross-spec bugs (CSI-1 through CSI-4) are all in the untested 59% of P1 findings

The consistency-auditor identifies 4 cross-spec inconsistencies and elevates several to P1. My audit shows that NONE of these have direct test coverage:
- **CSI-1** (scaffold `.json` vs `.yml`): No test loads a `.yml` scaffold through `score()`. The bug is real but undiscoverable by the test suite.
- **CSI-2** (`DomainScore.variables` omission): No test verifies variables are populated after `CodeReviewDomain.score()`.
- **CSI-3** (equilibrium score discontinuity): The Kalman filter third dimension is entirely untested with real data (eq_score is always 0.0).
- **CSI-4** (solver provenance keys): No test verifies the `solver` key exists on error-path `PluginResult` returns across specs 021 and 023.

This means the consistency-auditor's findings are derived from code reading, not from test failures. They are likely correct (the implementation-verifier confirms the code matches), but they cannot be validated or prevented from regressing without new tests. **Every cross-spec P1 the consistency-auditor found also needs a corresponding test.**

### DC-2: R-3 (refactor to `super().score()`) would create a new untested code path

The consistency-auditor recommends refactoring `CodeReviewDomain.score()` to delegate to `super().score()`. The current test suite tests the override's behavior directly. If the refactor lands, the test suite would need to be rewritten to test the delegation path. The consistency-auditor's recommendation is architecturally sound but creates a testing gap: the refactored code would have zero test coverage until the tests are updated. My recommendation: write the delegation tests first (testing `DomainPlugin.score()` with code review inputs), then do the refactor.

### DC-3: The cross-spec dependency map (R-10) has no testability plan

The consistency-auditor proposes a cross-spec dependency matrix (R-10, P3). From a test coverage perspective, a dependency matrix is only useful if it drives integration test creation. Currently there are zero cross-spec integration tests (my Missed Opportunity #1). The dependency matrix without tests is documentation; the dependency matrix with tests is a regression safety net. R-10 should explicitly link each dependency to a required integration test.

---

## Tensions

### T-1: Priority ranking of my test recommendations vs. the consistency-auditor's code fix recommendations

My CRITICAL #1 is spec 021 SC-001/SC-002 threshold tests. The consistency-auditor's P1 #1 is the scaffold extension fix (R-1). Both are correct within their scopes. The tension: should we fix bugs first (consistency-auditor) or prove the fixes work first (test-coverage-auditor)? For the scaffold bug specifically, my recommendation #7 (add YAML scaffold loading test) would fail today (confirming the bug), then pass after R-1 lands. Writing the test first is a TDD approach that would validate the fix.

### T-2: Whether "fix-then-test" or "test-first" is appropriate

The consistency-auditor's recommendations assume code fixes land first and tests follow. My recommendations include several that are "blocked by code change." The tension is philosophical: do we write failing tests to document bugs (my preference, expressed in my recommendation style), or do we fix bugs first and then add tests (the consistency-auditor's implied approach)? For the cross-spec bugs specifically, failing tests would be valuable documentation of the inconsistency even before the fix.

### T-3: CSI-3 severity accounting for test absence

The consistency-auditor rates CSI-3 as P2. I note that the equilibrium score system is entirely untested — the Kalman filter's third dimension has zero test coverage because eq_score is always 0.0. The consistency-auditor's P2 rating assumes the bug will manifest when Remediation 6 lands. But without tests, even the current 2D behavior of the filter is inadequately verified. The gap is wider than CSI-3 alone: the entire Kalman-to-convergence pipeline has no integration test.

### T-4: Missed Opportunity scope

The consistency-auditor identifies 3 missed opportunities (MO-1 through MO-3) focused on cross-spec planning. My missed opportunities focus on cross-spec testing. Both are valid but address different audiences: the consistency-auditor's MOs are for spec authors; mine are for test authors. A combined view would pair each cross-spec planning gap with a cross-spec test gap.

---

## Safe Agreements

### SA-1: The scaffold bug is confirmed from all angles

The consistency-auditor found it as CSI-1 (cross-spec inconsistency). I confirmed it has no test coverage. The implementation-verifier confirmed the code. All three agree on the bug, its severity, and the fix. This is the single most validated finding in the meta-review.

### SA-2: Spec 021 is the weakest spec in both reviews

The consistency-auditor finds spec 021 is the source of 2 cross-spec inconsistencies. I find spec 021 has the most untested P1 findings. Both reviews converge on the solver integration layer as the highest-risk area in the codebase.

### SA-3: Specs 025 and 026 are the healthiest

The consistency-auditor notes these specs have no P1 cross-spec issues. I confirm all SC tests pass with excellent alignment. Both reviews agree these specs are merge-ready modulo their Low-priority action items.

### SA-4: The optional-import pattern formalization is a quality improvement

The consistency-auditor's R-5 (shared optional-import convention) aligns with my finding that the pattern is tested independently in each spec. Formalizing would reduce duplication in both code and tests.
