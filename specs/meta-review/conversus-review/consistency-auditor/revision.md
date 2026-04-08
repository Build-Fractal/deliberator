# Phase 3 Revision: consistency-auditor

**Date**: 2026-04-01

---

## Cross-Reviews Received From

- **dependency-auditor**: 3 DCs, 3 Ts, 3 SAs
- **implementation-verifier**: 3 DCs, 4 Ts, 3 SAs
- **test-coverage-auditor**: 3 DCs, 4 Ts, 4 SAs

---

## Recommendation Dispositions

### R-1 [P1]: Fix scaffold file extension in `base.py:447`
**Status**: MAINTAINED — all 3 reviewers confirm the bug. Implementation-verifier verified at code level. Test-coverage-auditor confirms no test coverage. Dependency-auditor confirms fix is within the domains boundary.

**Adjustment**: Accept the implementation-verifier's DC-1 that R-1 must land BEFORE R-3. Adding explicit sequencing: R-1 -> R-3.

### R-2 [P1]: Fix `DomainScore.variables` omission in `domain.py:448`
**Status**: MAINTAINED — unanimously confirmed across all 4 reviews. This is the most thoroughly validated finding in the meta-review (test-coverage-auditor SA-2, implementation-verifier SA-2).

### R-3 [P1]: Refactor `CodeReviewDomain.score()` to delegate to `super().score()`
**Status**: MAINTAINED WITH CAVEATS — the implementation-verifier correctly notes that R-1 must land first. The test-coverage-auditor correctly notes that the refactored code path would have zero test coverage until tests are rewritten. **Amended ordering: R-1 -> scaffold delegation tests -> R-3 -> update test suite.**

### R-4 [P1]: Add `highspy` to the AMPL import guard
**Status**: MAINTAINED — unanimously confirmed. No reviewer challenged this.

### R-5 [P2]: Shared optional-import convention
**Status**: MAINTAINED — no opposition. The dependency-auditor and implementation-verifier both agree the pattern works but should be formalized.

### R-6 [P2]: Document equilibrium score discontinuity as precondition for spec 022 remediation 6
**Status**: DOWNGRADED TO P3 — accept the implementation-verifier's tension T-3 and the dependency-auditor's DC-2. The bug is real but dormant: eq_score is always 0.0 today, the integration path does not exist, and the orchestration layer is unverified. The documentation is still valuable but is not blocking anything currently. **Re-evaluate when spec 022 Remediation 6 is scheduled.**

### R-7 [P2]: Align mode support between `solver.py` and `mode-mapping.yml`
**Status**: MAINTAINED — accept the implementation-verifier's DC-3 that coalitional/bayesian/repeated games use different solution concepts than payoff matrices. **Amended**: the alignment should not extend `build_payoff_matrix()` for all new forms. Instead, `mode-mapping.yml` should annotate each mode with its solver type (`payoff_matrix`, `shapley`, `type_conditional`, etc.) and `solver.py` should only be responsible for `payoff_matrix`-type modes.

### R-8 [P2]: Standardize solver provenance keys across plugins
**Status**: MAINTAINED — accept the implementation-verifier's DC-2 that the standardization targets plugin wrappers, not the pure function modules. **Amended**: the recommendation now specifies that `solver` and `solver_status` keys belong on `PluginResult` in the plugin wrappers (`equilibrium_scorer.py`, `config_optimizer.py`), not on `SolverResult` in `solver.py` or `ampl_model.py`.

### R-9 [P2]: Add BayesianGame prior key validation
**Status**: MAINTAINED — no opposition. The test-coverage-auditor confirms no test exists; the implementation-verifier verified the gap.

### R-10 [P3]: Cross-spec dependency map
**Status**: MAINTAINED WITH AMENDMENT — accept the implementation-verifier's T-4 to distinguish verified (code-level) dependencies from aspirational (synthesis-described) dependencies. Accept the test-coverage-auditor's DC-3 to pair each dependency with a required integration test. **Amended**: the dependency matrix should have 3 columns per entry: dependency type (verified/aspirational), implementation status, and integration test status.

---

## New Recommendations

### R-11 [P1]: Write failing tests for CSI-1 and CSI-2 BEFORE fixing the code

Accept the test-coverage-auditor's cross-review (DC-1, T-1): all cross-spec P1 bugs lack test coverage. Write a test that loads a `.yml` scaffold through `DomainPlugin.score()` (confirming CSI-1 fails) and a test that asserts `DomainScore.variables` is populated after `CodeReviewDomain.score()` (confirming CSI-2 fails). These tests establish the regression baseline, document the bugs, and validate the fixes when they land. **Sequencing: R-11 -> R-1 -> R-2 -> R-3.**

### R-12 [P2]: Rewrite the `domains/__init__.py` docstring as a coupling RULE, not a dependency CLAIM

Accept the implementation-verifier's DC-2 (cross-review of dependency-auditor): the docstring should specify "MUST NOT import from engine, linter, web, mcp_server" (following the `code_review/__init__.py` pattern) rather than claiming specific imports. This avoids the premature fix problem (dependency-auditor's P1) and the aspirational dependency ambiguity (implementation-verifier's T-1).

---

## Position Summary

The cross-reviews strengthened my findings in every case. All 4 cross-spec inconsistencies (CSI-1 through CSI-4) were confirmed. Two adjustments were necessary:

1. **Sequencing**: R-1 must precede R-3 (implementation-verifier's contribution). This is a real dependency I missed.
2. **Severity calibration**: R-6 downgraded from P2 to P3 because the bug is dormant and the integration path does not exist. I overweighted the future risk.

The most important insight from the cross-reviews is the test-coverage-auditor's DC-1: all my cross-spec P1 findings lack test coverage. This means my findings are architecturally correct but empirically unverified. Adding R-11 (write failing tests first) addresses this gap and strengthens the reliability of the entire set of recommendations.

My confidence in the remaining recommendations is higher after the cross-review process. No reviewer challenged the existence of CSI-1, CSI-2, or R-4. The disagreements were about severity, sequencing, and file attribution — important details but not challenges to the core findings.
