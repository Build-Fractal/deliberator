# Cross-Review: dependency-auditor reviewing test-coverage-auditor

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: 41% P1 test coverage means my "verified" dependency claims rest on untested code

My audit verified import boundaries by examining actual code. The test-coverage-auditor reveals that 59% of P1 findings have no test coverage. This means the code I verified is correct *as written* but may not behave as intended at runtime. Specifically:
- I verified that `plugins/nashopt/` imports only from `plugins/base` and `schemas/features`. But if the nashopt solver's post-processing (untested per the test-coverage-auditor) silently corrupts data, the clean import boundary is irrelevant — the data contract is broken.
- I verified that `domains/code_review/` imports only from `domains/base`. But if `CodeReviewDomain.score()` does not populate `DomainScore.variables` (untested), the behavioral contract with `domains/base` is violated despite clean imports.

My "VERIFIED" verdicts are import-level verdicts. The test-coverage-auditor's findings reveal that import-level verification is necessary but insufficient for dependency health.

### DC-2: Cross-spec integration test absence invalidates orchestration layer claims

My Missed Opportunity #2 identifies that the engine-to-plugins integration boundary is unverified. The test-coverage-auditor's Missed Opportunity #1 states there are NO cross-spec integration tests. These findings compound: not only is the orchestration layer unaudited (my finding), but even if it existed, there would be no tests to verify it works (their finding). The combined gap means the entire plugin execution lifecycle is verified only through documentation and per-spec unit tests.

### DC-3: `pytest.skip("Base layer not yet available")` undermines 029/030 coupling verification

The test-coverage-auditor notes that spec 029 tests use `pytest.skip` when the base layer import fails, meaning SC-001 and SC-002 may be untested in some environments. My audit verified that `code_review/domain.py` imports from `domains/base`. If those imports fail at test time, the coupling I verified at the source level is not validated at runtime. The dependency arrow `code_review -> domains/base` exists in code but may not be exercised in CI.

---

## Tensions

### T-1: What counts as "verified" for dependency health

I define dependency health as: import boundaries are clean, no cycles, arrows point downward. The test-coverage-auditor implicitly defines dependency health as: the code paths that cross boundaries produce correct results. Both definitions are valid; together they form a complete picture. Independently, each is incomplete.

### T-2: Priority of test gaps relative to dependency gaps

The test-coverage-auditor's #1 CRITICAL recommendation is spec 021 SC-001/SC-002 threshold tests. My #1 P1 recommendation is the `domains/__init__.py` docstring fix. These target different layers: the test-coverage-auditor prioritizes behavioral verification of the most foundational spec; I prioritize documentation accuracy of the most foundational package. Both are correct within their scopes, but a combined priority list would need to merge them.

### T-3: Mock quality as a dependency concern

The test-coverage-auditor flags that `TestMockNashoptIntegration` bypasses the real `_score_from_solver` post-processing. From a dependency perspective, this means the integration boundary between `solver.py` (which produces `SolverResult`) and the plugin wrapper (which produces `PluginResult`) is tested only through mocks that skip the conversion layer. The mock boundary does not align with the dependency boundary, which means the tests verify a simplified version of the real dependency flow.

### T-4: "Blocked" test recommendations

The test-coverage-auditor marks several test recommendations as "blocked" by code changes that haven't landed (e.g., innovation sequence test blocked by Remediation 1, post-processing mapping test blocked by P1-5 code fix). From a dependency perspective, these blocked tests represent dependency chains in the development process itself: test A depends on fix B, which depends on architecture decision C. My audit does not cover development-process dependencies, but these blocking chains may delay the testing that would validate my import-level findings.

---

## Safe Agreements

### SA-1: Each spec's tests are properly isolated within their dependency boundary

The test-coverage-auditor confirms that test files correspond to their spec's implementation files and do not import across spec boundaries. This matches my finding that the runtime code itself maintains clean boundaries.

### SA-2: The Kalman filter third dimension is non-functional

The test-coverage-auditor confirms eq_score is always 0.0 with no test for real data. My audit confirms the data flow path (`convergence.py -> kalman.py`) exists at the import level but is not exercised. Both agree this is a dormant dependency that will become active when Remediation 6 lands.

### SA-3: Spec 025 and 026 test suites are well-aligned

Both reviews find minimal issues with specs 025 and 026. The test-coverage-auditor confirms all SC tests pass; my audit confirms schemas/ is a clean leaf package. These specs have the healthiest combination of dependency integrity and test coverage.
