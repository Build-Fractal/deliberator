# Phase 4 Disputes: test-coverage-auditor

**Date**: 2026-04-01

---

## Remaining Disputes

### Dispute 1: `domains/__init__.py` docstring — P1 (dependency-auditor) or P2 (my position)

The dependency-auditor maintains P1 for the docstring rewrite, arguing it is "the only coupling enforcement mechanism" until import-linter lands. The consistency-auditor endorses the coupling RULE reframe (their R-12) but does not explicitly take a priority position. The implementation-verifier supports the reframe without committing to priority.

**My position**: I maintain P2. The docstring is important but does not cause runtime failures, test failures, or data corruption. The P1 bugs identified by other reviewers (scaffold extension, DomainScore.variables, highspy guard) have direct behavioral impact. A docstring fix is a documentation improvement that prevents future mistakes; P1 bugs are current mistakes causing incorrect behavior now.

**Concession path**: If the dependency-auditor's import-linter recommendation (P3-4) is bundled with the docstring fix as a single work item ("establish coupling enforcement for domains/"), I would accept P1 for the combined item. The docstring alone is P2; the docstring + automated enforcement is P1.

### Dispute 2: CSI-3 characterization test — useful or noise?

The implementation-verifier argues that the CSI-3 test (pass non-zero eq_scores through Kalman filter) "tests hypothetical behavior that the codebase does not currently produce" and should be a design note instead. The consistency-auditor downgraded CSI-3 to P3.

**My position**: The characterization test is valuable even for dormant bugs. Writing `test_kalman_with_nonzero_eq_scores()` documents the current behavior of the filter when the third dimension receives real data. This test will:
1. Establish a baseline for when Remediation 6 lands
2. Verify the implementation-verifier's claim that confidence is initialization-dependent
3. Cost 10-15 lines of test code

However, I concede it is not CRITICAL or HIGH. **Amended: classify the CSI-3 characterization test as MEDIUM. It is useful characterization, not urgently needed.**

---

## Convergence

### Full convergence on:

1. **41% P1 test coverage is the correct metric and the gap is real**: No reviewer challenged the count or methodology. The consistency-auditor, dependency-auditor, and implementation-verifier all incorporated this finding into their revisions.

2. **Test-first development for P1 fixes**: All 4 reviews explicitly agree. The consistency-auditor's R-11 (write failing tests for CSIs) and the implementation-verifier's amended fix sequencing (write failing test -> fix -> verify) both adopt this principle. This is the strongest process convergence.

3. **Two CRITICAL categories**: The consistency-auditor accepted my two-category system (acceptance criteria gaps + cross-spec regression gaps). No reviewer objected.

4. **Unblocked "blocked" tests**: The implementation-verifier's observation that tests can be written against current buggy behavior unblocked my recommendations #9 and #10. No reviewer disagreed.

5. **Cross-spec integration test (HIGH-NEW-1)**: My recommendation for a 029/030 scoring pipeline integration test was not challenged. This would be the first cross-spec test in the codebase.

6. **File attribution for solver key test**: The implementation-verifier's correction (test belongs in plugin wrapper test file, not `test_solver.py`) is accepted by all.

7. **SC-002 assertion tightening requires parameter investigation**: My HIGH #4 amendment (investigate parameter adjustment, not just assertion change) was not challenged.

8. **Specs 025/026 are merge-ready**: All 4 reviews agree these specs have excellent test coverage, clean dependencies, verified implementations, and no cross-spec issues. The remaining Low-priority items (potential game N-player test, constraint gap_question test) are quality improvements, not blockers.

9. **Spec 021 needs the most work**: All 4 reviews converge. The combined diagnosis: missing acceptance tests (me), cross-spec inconsistencies (consistency-auditor), mislocated synthesis findings (implementation-verifier), untested P1 code (all four).

10. **The DomainScore.variables bug is the exemplar**: All 4 reviews independently confirmed this from different angles, making it the most validated finding and a proof-of-concept for the multi-perspective meta-review process.

---

## Final Position

My core finding — that 41% P1 test coverage creates systemic risk — is unchallenged and incorporated into all 4 revisions. The deliberation refined my recommendations:

1. **Cross-spec failing tests (R-11 expansion)**: The consistency-auditor's R-11 + my expansion to all 4 CSIs creates a new category of tests that did not exist before. This is the deliberation's most actionable output for test infrastructure.

2. **Unblocked tests**: The implementation-verifier's insight that characterization tests against buggy code are valuable expanded my recommendation scope without increasing the code change surface.

3. **Two CRITICAL categories**: Separating acceptance criteria gaps from cross-spec regression gaps provides clearer prioritization for test development.

4. **File attribution**: Several test recommendations now target the correct files (plugin wrapper tests, not pure function module tests).

My remaining dispute (docstring P1 vs P2) is the smallest remaining gap in the deliberation. It affects prioritization of a single work item, not the architectural assessment or the bug inventory.
