# Cross-Review: consistency-auditor reviewing test-coverage-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: 41% P1 test coverage undermines confidence in my cross-spec findings

The test-coverage-auditor reports that only 9 of 22 P1 findings have direct test coverage (41%). My cross-spec inconsistencies (CSI-1 through CSI-4) are all derived from synthesis claims about code behavior. If the underlying P1 findings are untested, the syntheses may be describing intended behavior rather than verified behavior. Specifically:

- **CSI-1** (scaffold `.json` vs `.yml`): The test-coverage-auditor confirms NO test loads a `.yml` scaffold through `score()`. My finding assumes the `.yml` code path works — which is untested.
- **CSI-2** (`DomainScore.variables` omission): The test-coverage-auditor confirms NO test verifies variables are populated after `score()`. My finding assumes the base class path correctly passes `variables=variables` — which is also untested.
- **CSI-3** (equilibrium score discontinuity): The test-coverage-auditor confirms the Kalman filter's third dimension operates on zero data (eq_score always 0.0). My finding about future discontinuity is moot until eq_scores are wired, but the zero-data state makes the current filter effectively 2D — which the existing tests do not account for.

**Bottom line**: My cross-spec findings are architecturally correct but sit on top of untested P1 code. Fixing the bugs I identify without adding the tests the test-coverage-auditor recommends would be risky.

### DC-2: Spec 021's SC-001/SC-002 zero coverage is a cross-spec risk, not just a single-spec gap

The test-coverage-auditor classifies spec 021's missing SC-001/SC-002 tests as "CRITICAL" but scopes the impact to spec 021. My review (CSI-3, MO-1) shows that spec 021's equilibrium scores feed into spec 022's Kalman filter and spec 025's payoff matrices. If spec 021's success criteria are unverified, the downstream specs' integration assumptions are also unverified. The test gap is not just "spec 021 is incomplete" — it is "the solver layer that specs 022, 023, 025, and 026 depend on has no acceptance test."

### DC-3: "No cross-spec integration tests" finding amplifies all of my CSIs

The test-coverage-auditor's Missed Opportunity #1 states: "No test file exercises the pipeline across specs (e.g., equilibrium scorer -> convergence predictor -> config optimizer). Each spec's tests are siloed." This directly validates my concern that cross-spec bugs (CSI-1 through CSI-4) cannot be caught by the existing test suite. The test-coverage-auditor frames this as a missed opportunity; I would elevate it to a structural gap that enables the class of bugs I identified.

---

## Tensions

### T-1: "Fix-then-test" vs. "test-to-confirm-the-fix" ordering

The test-coverage-auditor's recommendations follow a "fix the code, then add tests" pattern (e.g., innovation sequence test is "blocked by Remediation 1 code change"). My recommendations follow a "fix the code as informed by cross-spec context" pattern. The tension: if tests are written after fixes, they may validate the fix without testing the cross-spec interaction. For example, fixing the scaffold `.json` bug (my R-1) and adding a YAML scaffold test (their recommendation #7) would validate the single-spec fix but not test whether `CodeReviewDomain.score()` correctly uses the inherited scoring pipeline — which is the architectural fix (my R-3).

### T-2: Priority ranking of test gaps

The test-coverage-auditor ranks spec 021 SC-001/SC-002 as CRITICAL (#1 recommendation), spec 021 error-path solver key as HIGH (#2), and spec 030 YAML scaffold test as MEDIUM (#7). My cross-spec priority would rank the scaffold test higher because CSI-1 blocks spec 030's architectural promise, which is foundational for all future domains. The disagreement is about whether spec-internal acceptance criteria (SC-001/SC-002) or cross-spec architectural integrity (scaffold handling) is the more urgent test gap.

### T-3: Mock quality assessment

The test-coverage-auditor flags that `TestMockNashoptIntegration` "bypasses the actual `_score_from_solver` post-processing function" (Off-Base Assumption #1). My review does not assess mock quality because my scope is cross-spec consistency. However, this finding strengthens my CSI-3: if the mock tests do not exercise the real post-processing, then the heuristic-vs-solver score discontinuity cannot surface in the test suite. The test-coverage-auditor and I are identifying the same gap from different angles.

### T-4: Completeness of P1 count

The test-coverage-auditor counts 22 P1 findings across all specs. My review identifies 4 additional cross-spec P1s (CSI-1, CSI-2, R-3, R-4) that are not counted in the 22 because they span spec boundaries. The true P1 count may be higher, and the 41% coverage rate may be lower when cross-spec P1s are included.

---

## Safe Agreements

### SA-1: The scaffold `.json` hardcoding has no test coverage and is a real bug

Both reviews confirm the bug exists and is untested. The test-coverage-auditor recommends adding a YAML scaffold loading test (#7); my review recommends the code fix (R-1). These are complementary.

### SA-2: Spec 021 is the weakest link in both reviews

The test-coverage-auditor finds spec 021 has the most untested P1 findings (6+ items). My review finds spec 021 is the source of two cross-spec inconsistencies (CSI-3, CSI-4). Both reviews agree that the solver integration layer needs the most attention.

### SA-3: The Kalman filter third dimension is non-functional

The test-coverage-auditor confirms eq_score is always 0.0 with no test for real data. My review (CSI-3, OBA-2) identifies the architectural consequence: the confidence metric is meaningless for the equilibrium dimension. Both agree this is a known gap that will become a bug when Remediation 6 lands.
