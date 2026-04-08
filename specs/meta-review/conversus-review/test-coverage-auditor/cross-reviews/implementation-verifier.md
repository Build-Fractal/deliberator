# Cross-Review: test-coverage-auditor reviewing implementation-verifier

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: 18/21 verification rate creates unwarranted confidence when combined with 41% P1 test coverage

The implementation-verifier's headline result (86% accuracy, corrected to 18/21) establishes that syntheses accurately describe the code. However, this accuracy metric measures synthesis-to-code alignment, not code-to-correctness. My audit shows 59% of P1 findings are untested. Combining these: we have high confidence that the code matches the synthesis descriptions, but low confidence that the code actually works for the most critical findings. The danger is that the 86% figure reassures stakeholders that the review process is reliable, when in fact the code underneath the reviews is largely untested at the P1 level.

### DC-2: The "immediate fix" list does not account for test-first development

The implementation-verifier lists 5 immediate fixes as "verified as real bugs." Each fix is described as a code change, not as a test-then-fix. For 4 of these 5 bugs, I identified that no test currently exercises the buggy code path:
1. `DomainScore.variables` not populated — NO TEST for the buggy path
2. `HAS_AMPL` guard missing highspy — NO TEST for highspy presence
3. Innovation sequence discarded — NO TEST for innovation-based detection
4. Plugin config Q/R not wired — NO TEST for config passthrough
5. BayesianGame prior key validation — NO TEST for invalid keys

Fixing these bugs without first writing failing tests means there is no regression safety net. If any fix is accidentally reverted or broken by a future change, the test suite will not catch it.

### DC-3: "Stale" count of 0 may be optimistic given test skip patterns

The implementation-verifier found 0 stale claims (revised from initial 1). However, my audit found `pytest.skip("Base layer not yet available")` in spec 029 tests, meaning some test assertions may be stale (they exist but are not executed). If the implementation-verifier's verification of spec 029 claims assumed the base layer is available (which it is in the codebase), but the tests skip base-layer-dependent assertions, then the code is verified but the test suite is stale for those claims.

---

## Tensions

### T-1: What "verified" means in each review

The implementation-verifier: "the code at line X matches the synthesis claim." Me: "a test exercises the code at line X and asserts the expected behavior." These are different levels of verification. The implementation-verifier's work is necessary (confirms syntheses are not hallucinating), and my work is complementary (confirms the code is exercised). The combined verification pipeline is: synthesis -> code (86% accurate) -> test (41% exercised at P1 level).

### T-2: Spec 021 weakness assessment

The implementation-verifier calls spec 021 "the weakest" based on 2 inaccuracies (both file misattributions). I call spec 021 the weakest based on the most untested P1 findings (6+ items). Both identify the same spec but for different reasons: the implementation-verifier found synthesis quality issues, while I found test coverage issues. The combined picture is worse than either alone: spec 021 has both the least accurate synthesis AND the least tested P1 findings.

### T-3: Strategy profile dimension mismatch severity

The implementation-verifier's Missed Opportunity #3 states the 4-element fallback vector mismatch "would cause a runtime error in nashopt, not just a wrong result." My audit confirms no test exercises this path. The implementation-verifier rates this as "more severe than stated" but it remains untested. The severity upgrade is theoretical without a test to demonstrate the runtime error.

### T-4: The corrected verification count

The implementation-verifier's executive summary says 17/3/1 but the detailed work produces 18/2/0. The correction is noted in a footnote. From a test perspective, this kind of inconsistency between summary and detail is exactly what regression tests prevent: if the summary were generated from the detail table automatically, the mismatch would not exist. The meta-review process itself could benefit from the kind of verification automation we recommend for the codebase.

---

## Safe Agreements

### SA-1: Mathematical correctness assessments do not need test coverage changes

The implementation-verifier confirmed Shapley formula, Kalman mechanics, potential game diagnostic are all correctly assessed. My audit confirms these mathematical functions have strong test coverage (the Shapley tests check all 4 axioms; the Kalman tests cover 26 matrix operations; the potential game diagnostic has 5 test cases). This is the area with the best synthesis-to-code-to-test alignment.

### SA-2: The DomainScore.variables bug is the most thoroughly validated finding

The implementation-verifier confirmed it in code. I confirmed it has no test. The consistency-auditor identified its cross-spec impact. The dependency-auditor confirmed the fix is dependency-safe. Four independent reviews converge on this single bug.

### SA-3: Specs 025 and 026 verification is the strongest

The implementation-verifier verified all 6 claims across these specs. I confirmed all SC tests pass. Both agree these are the healthiest specs. The alignment between code verification and test coverage is highest for these two specs.

### SA-4: Frozen Pydantic models are verified and tested

The implementation-verifier confirmed all 5 domain state models are frozen at the code level. My audit confirmed `test_domains.py` has frozen tests for all 5 models. This is a clean verification-to-test pipeline.
