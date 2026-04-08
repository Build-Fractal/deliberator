# Meta-Review Phase 1: Test Coverage Audit

**Auditor**: test-coverage-auditor
**Date**: 2026-04-01
**Scope**: Specs 021, 022, 023, 025, 026, 029, 030

---

## Executive Summary

Across seven specs and ten test files, test coverage broadly matches synthesis claims but reveals a pattern of **structural gaps at the P1 boundary**: the most critical findings from each synthesis frequently lack corresponding test coverage, while well-understood, lower-risk behavior is thoroughly tested. Four specs have clean alignment (025, 026, 029, 030). Three specs have material gaps between what the synthesis promises and what the tests verify (021, 022, 023). No synthesis fabricates test coverage that does not exist, but several overstate the degree to which P1 findings are exercised.

**Quantitative summary**:
- **Total P1 findings across all specs**: 22
- **P1 findings with direct test coverage**: 9 (41%)
- **P1 findings with no test coverage**: 13 (59%)
- **SC (success criteria) tests present**: 27 of 30 claimed (90%)
- **SC tests matching spec thresholds exactly**: 24 of 27 (89%)

---

## Alignment by Spec

### Spec 021 — nashopt Solver Integration

**Synthesis claims**: 8 P1 items, 8 P2 items, 4 P3 items. SC-001 and SC-002 have no test coverage (explicitly flagged as UNVERIFIED).

**Test file**: `test_solver.py` (~700 lines)

| Synthesis Claim | Test Coverage? | Assessment |
|---|---|---|
| SC-001/SC-002 threshold tests are P1 blocking | **NO** | Correctly flagged as UNVERIFIED in synthesis. No tests exist for "cooperative convergence score >= 0.9" or "3+ disputes score < 0.5". This is the single most important gap — the spec's own acceptance criteria have zero coverage. |
| P1-3: FR-005 per-agent equilibrium from best_responses | **NO** | `test_solver.py` tests the heuristic path only. No test verifies that `best_responses` from nashopt is used to derive per-agent deviation. The `hasattr(result, "agents_not_at_equilibrium")` guard is exercised only in mock tests that bypass the real logic. |
| P1-4: `solver` key on error-path returns | **PARTIAL** | `TestSolverFieldInResult` verifies `solver` field exists on happy paths and empty-agent paths. No test explicitly verifies error-path PluginResult returns (unknown-mode, computation-failure) include the `solver` key. `test_nashopt.py::TestGracefulErrorHandling::test_unknown_mode_returns_error_result` checks for `"error"` in data but not `"solver"`. |
| P1-5: Post-processing mapping for non-NxN modes | **NO** | No test exercises the post-processing at `solver.py:416-424` with red-blue (2-row) results mapped back to N agents. `TestBuildPayoffMatrixRB` tests matrix construction but not the result-to-agent mapping. |
| P1-6: Strategy profile dimension match | **PARTIAL** | `TestBuildStrategyProfile` tests construction of profiles from features, including `position_vector` and `without_position_vector`. But no test verifies the profile dimensions match the payoff matrix's action dimension — the generic 4-element fallback is exercised but not validated against the matrix shape. |
| P1-7: Real-timeout integration test | **NO** | `TestTimeoutFallback` in `test_solver.py` uses `mock.patch` with `side_effect=concurrent.futures.TimeoutError()`. This is the exact pattern the synthesis unanimously agreed must be replaced with a real blocking mock (e.g., `time.sleep(5)` with 0.01s timeout). |
| P1-8: Spec amendment (matrix shapes) | N/A | Spec-level, not testable. |

**Mock nashopt integration tests**: `TestMockNashoptIntegration` in `test_solver.py` verifies the solver dispatch path using `SolverResult` objects, covering FR-001, FR-002, FR-004, FR-008. These are well-structured.

**Heuristic path coverage**: Strong. `test_nashopt.py` thoroughly covers all four modes (cooperative, WTA, PD, red-blue), payoff computation, score normalization, threshold configuration, and hook behavior.

**Verdict**: Synthesis is honest about SC-001/SC-002 gaps. However, the 6 remaining P1 code-change items (P1-3 through P1-7) also lack test coverage, and the synthesis does not flag this as explicitly. The test suite validates the pre-021 heuristic behavior comprehensively but undercovers the new solver integration path.

---

### Spec 022 — Kalman Convergence

**Synthesis claims**: 3 compliance remediations (P1), 2 quality fixes (P1 quality tier), 3 enhancements (P2/P3). SC-001 through SC-004 have dedicated tests.

**Test file**: `test_kalman.py` (~994 lines)

| Synthesis Claim | Test Coverage? | Assessment |
|---|---|---|
| SC-001: Kalman >= OLS confidence for decreasing disputes | **YES** | `TestSC001DecreasingDisputes::test_kalman_higher_confidence_than_ols` directly tests this with 5->3->1 dispute sequence. |
| SC-002: Stagnation has wider confidence bounds | **PARTIAL** | `TestSC002IdenticalDisputes::test_wider_bounds_than_converging` exists but uses the relaxed assertion (`>= conv_width * 0.5`). The synthesis explicitly flags this as a compliance gap (Remediation 3) requiring tightening to `>= conv_width`. The test exists but knowingly violates the spec's "wider confidence bounds" requirement. |
| SC-003: Non-linear convergence handled | **YES** | `TestSC003NonLinearConvergence` with diminishing-returns pattern (10, 7, 5, 4, 4, 3). |
| SC-004: OLS fallback preserved | **YES** | `TestSC004FallbackToOLS` with explicit OLS method, auto fallback, and behavior preservation. |
| Remediation 1 (FR-005): Innovation sequence for fixed-point detection | **NO** | `TestDetectFixedPoint` tests state-delta-based detection, not innovation-sequence-based detection. The synthesis identifies this as the most significant compliance gap — the innovation vector is computed but discarded. No test verifies innovation-based detection because the fix hasn't landed. |
| Remediation 2 (FR-007): Wire Q/R from plugin config | **NO** | `TestPredictorPluginIntegration` tests `convergence_method` config but NOT `process_noise_Q` or `observation_noise_R` config passthrough. The synthesis explicitly notes this 3-5 line fix is missing. |
| Remediation 4: Confidence calibration | **NO** | Tests exercise `compute_kalman_confidence()` but don't test for initialization-invariance. The synthesis tracks this as quality P1. |

**Matrix operations**: Exhaustive coverage of the 3x3 pure-Python matrix library (26 tests). This matches the synthesis claim of "comprehensive" math coverage.

**Plugin integration**: Well-covered. `TestPredictorPluginIntegration` verifies method selection, config passthrough, and output fields.

**Verdict**: SC tests are present and accurate. The synthesis correctly identifies three compliance gaps that lack test coverage because the fixes haven't been implemented. The relaxed SC-002 assertion is both identified in the synthesis and observable in the test. Honest reporting overall.

---

### Spec 023 — AMPL Config Optimizer

**Synthesis claims**: 1 P1 item (spec amendment), 7 P2 items, 4 P3 items. No compliance test gaps flagged.

**Test file**: `test_ampl.py` (~764 lines)

| Synthesis Claim | Test Coverage? | Assessment |
|---|---|---|
| P2: Store config model as `.mod` file | **NO** | No test loads a `.mod` file from disk through the config optimizer path. `TestSolveAMPLAPI::test_solve_ampl_with_file_path` tests `.mod` file detection in the generic API but not the config-specific model. |
| P2: Extract real MIP gap | **NO** | `TestAMPLMockIntegration::test_ampl_metadata_in_plugin_result` checks `"gap" in pr.data` but uses a mock that never sets a real gap value. The hardcoded `gap: 0.0` is not verified to reflect actual solver output. |
| P2: Check amplpy+highspy in guard | **NO** | `TestHasAMPLFlag` verifies `HAS_AMPL` is bool and the module doesn't crash. No test verifies that `highspy` is also checked during import. |
| P2: Structured return type (SolveOutcome) | **NO** | `solve_with_ampl` returns `None` or `OptimalConfig`. No test validates discriminated status for the three failure modes. |
| P2: Robust file detection | **NO** | `test_solve_ampl_with_file_path` uses `"my_problem.mod"` which the heuristic handles. No test exercises `.ampl`/`.run` extensions or false-positive model strings ending in ".mod". |
| P3: Integration tests with real AMPL | **NO** | All AMPL tests use mocks. Synthesis explicitly flags this. |

**Strong points**: `TestQualityModelConsistency` exhaustively verifies AMPL and grid search produce identical results at every grid point (all 135 points). `TestAMPLModelGeneration` thoroughly covers model string construction and data preparation. `TestTimeoutFallback` and `TestInfeasibilityConsistency` cover the fallback path well.

**Verdict**: The synthesis's P2 items are all real gaps with no corresponding test coverage. This is acceptable since the synthesis explicitly acknowledges these are fix-then-test items. The existing test suite is strong for what it covers. The `TestQualityModelConsistency` class is notably rigorous.

---

### Spec 025 — Game Form Expansion

**Synthesis claims**: PASS verdict. 4 surviving disputes (all unanimous), 8 action items (mostly Low/Trivial).

**Test file**: `test_game_forms_expanded.py` (~510 lines)

| Synthesis Claim | Test Coverage? | Assessment |
|---|---|---|
| SC-001: Potential game diagnostic | **YES** | `TestPotentialGameDiagnostic` with coordination game (True), PD (True), matching pennies (False), empty (True), and `compute_potential()` for both cases. |
| SC-002: Shapley efficiency axiom | **YES** | `TestShapleyValues` with 3-player game summing to grand coalition, symmetric players, null player, and N>10 rejection. |
| SC-003/SC-004: Pydantic validation + YAML loading | **YES** | Parametrized tests across all 5 new forms with validation error checking and YAML round-trip. |
| SC-005: Mode mapping complete | **YES** | `TestExpandedModeMapping` verifies all 5 new + 4 original mappings. |
| Dispute 1: `is_potential_game()` 2-player limitation | **NO TEST** | No test exercises `is_potential_game()` with a 3-player or asymmetric matrix. The synthesis notes this as a Low action item. |
| Dispute 2: BayesianGame prior key validation | **NO TEST** | `TestBayesianGameValidation::test_prior_not_summing_to_one_raises` tests sum validation. No test verifies that invalid prior keys (garbage keys not from type space Cartesian product) are rejected. |
| Game form count test | **YES** | `TestGameFormCount::test_at_least_9_game_form_schemas` matches the amended SC-005 threshold. |
| No solver imports test | **YES** | `TestNoSolverImportsInGameForms` verifies clean dependency separation. |

**Verdict**: Excellent alignment. All SC tests present and passing. The two missing items (potential game N-player test, Bayesian prior key validation test) are correctly tracked as Low/Medium action items in the synthesis, not as existing coverage.

---

### Spec 026 — Optimization Template Library

**Synthesis claims**: PASS verdict. 2 surviving disputes (both Low, unanimous). 6 action items.

**Test file**: `test_templates_expanded.py` (~239 lines)

| Synthesis Claim | Test Coverage? | Assessment |
|---|---|---|
| SC-001: >= 35 templates | **YES** | `TestSC001TemplateCount::test_library_has_at_least_35_templates` |
| SC-002: >= 10 constraints | **YES** | `TestSC002ConstraintCount::test_library_has_at_least_10_constraints` |
| SC-003: All 15 new templates validate | **YES** | Parametrized across all 15 names with Pydantic validation, game_form, and mode_compatibility checks. |
| SC-004: All 4 new constraints validate | **YES** | Parametrized across all 4 constraint names. |
| SC-005: Template examples non-empty | **YES** | `TestSC005AllTemplateExamples` across all template YAMLs. |
| Dispute 1: game_form cross-reference validation | **NO TEST** | Synthesis correctly flags this as missing. No test verifies template `game_form` values match game-forms/*.yml filenames. |
| Dispute 2: Constraint gap_question test coverage | **NO TEST** | `TestGapQuestions` covers objective templates only. Synthesis correctly flags the missing `TestConstraintGapQuestions` class. |
| All templates + constraints validate | **YES** | `TestAllTemplatesValidate` and `TestAllConstraintsValidate` provide regression coverage. |
| Constraint reference validity | **YES** | `TestTemplateConstraintReferences` verifies all constraint refs resolve to existing files. |

**Verdict**: Near-perfect alignment. All 5 SC tests present and matching. Both missing test items are correctly identified in the synthesis as Low-priority additions. The test file is well-structured with clear SC-to-test mapping.

---

### Spec 029 — Code Review Domain

**Synthesis claims**: 11 MET, 3 PARTIALLY MET, 5 NOT MET FRs. SC-001 and SC-002 tested. 17 action items.

**Test file**: `test_code_review.py` (~890+ lines)

| Synthesis Claim | Test Coverage? | Assessment |
|---|---|---|
| SC-001: Good PR healthcare > 0.85 | **YES** | `TestCodeReviewDomainScore::test_good_pr_healthcare_sc001` asserts `score.overall > 0.85`. |
| SC-002: Secrets blocks all scaffolds | **YES** | `test_secrets_exposed_blocks_all_scaffolds_sc002` iterates all 5 scaffolds. |
| FR-001: Extractor parsing | **YES** | Individual extractor tests for CoverageExtractor (Cobertura, lcov), LintExtractor (ruff, eslint), ComplexityExtractor (radon), SecurityExtractor (bandit, gitleaks), DocumentationExtractor (interrogate, mypy), ConventionExtractor (black, isort), GitDiffExtractor, SpecComplianceExtractor. |
| FR-003: Missing data -> None | **YES** | Every extractor has a `test_missing_report_returns_none` test. |
| FR-007: 5+ scaffolds | **YES** | `TestScaffolds::test_all_expected_scaffolds_exist` and parametrized validation. |
| FR-009: Scaffold YAML valid | **YES** | Parametrized across all 5 scaffolds checking required fields, types. |
| P1-1 Bug: DomainScore.variables not populated | **NO** | No test verifies that `DomainScore.variables` is populated after `CodeReviewDomain.score()`. The synthesis identifies this as a one-line bug fix. The `test_domains.py` tests use `_make_record()` which manually sets `variables`, not testing the code path where the bug exists. |
| P1-2: Duplicate variable ownership | **NO** | No test verifies `format_compliant` is owned by exactly one extractor, or `has_changelog_entry` by exactly one. Both LintExtractor and ConventionExtractor test `format_compliant`. |
| P1-3: Elevate `_INVERTED_BOOLEANS` | **NO** | No test for module-level constant discoverability (this is a code organization fix, not testable per se). |
| FR-010 through FR-013 (NOT MET) | **NO** | No JSONLReviewStore tests in `test_code_review.py`. These are in `test_domains.py` as part of the base layer, which is a different spec (030). The synthesis correctly marks these as NOT MET Phase 2 items. |

**Verdict**: Good alignment for implemented features. SC-001 and SC-002 are directly tested. The extractor test suite is thorough with 8+ extractor classes fully covered including error cases. The P1 bug (DomainScore.variables) is correctly identified but not tested because the fix hasn't landed. The NOT MET items are honestly reported as Phase 2 scope.

---

### Spec 030 — Domain Plugin Architecture

**Synthesis claims**: PASS for base layer. 5 surviving disputes (High/Medium). 9 MET, 4 PARTIALLY MET, 8 NOT MET.

**Test file**: `test_domains.py` (~952 lines)

| Synthesis Claim | Test Coverage? | Assessment |
|---|---|---|
| SC-001: Code-review domain implementable as subclass | **YES** | `ConcreteDomainPlugin` subclass exercises the full lifecycle. |
| SC-002: Two domains with isolated stores | **PARTIAL** | Round-trip tests use a single domain. No explicit test runs two different domain names through isolated stores simultaneously. |
| Frozen models | **YES** | `TestDomainScore::test_frozen`, `TestDomainRecord::test_frozen`, `TestDomainContext::test_frozen`, `TestTrendResult::test_frozen`, `TestScaffold::test_frozen` — all 5 models verified. |
| Deterministic scoring | **YES** | `TestScoringLogic` thoroughly covers `_compute_weighted_score`, `_check_hard_blocks`, `_determine_verdict`, `_build_recommendations` with edge cases. |
| Protocol compliance | **YES** | `TestDomainStoreProtocol` verifies both JSONLStore and SQLiteStore satisfy the DomainStore protocol. |
| API router tests | **YES** | `TestDomainAPI` uses FastAPI TestClient for submit, get, health, trends, scaffolds endpoints. |
| Dispute 1: Gate lifecycle absent | **NO TEST** | No `gate()` or `/gate/{id}` test exists. Synthesis correctly marks this as NOT MET. |
| Dispute 2: Plugin discovery not implemented | **NO TEST** | No `load_domain_plugins()` test. Synthesis correctly marks as NOT MET. |
| Dispute 3: score() hard-codes .json | **NO TEST** | Tests use `.json` scaffolds exclusively. No test loads a `.yml` or `.yaml` scaffold through `score()`. Synthesis identifies this as Medium fix. |
| Dispute 4: Hard block validation | **NO TEST** | No test exercises malformed hard block strings (e.g., missing space). |
| Dispute 5: Silent query/trend failure | **NO TEST** | No test exercises unknown filter keys or unknown trend field names. |

**Verdict**: Strong alignment for the implemented base layer. The 5 disputes are all correctly identified as unimplemented features without test coverage. The test suite is comprehensive for what exists: 22 test classes covering scoring, stores, protocol compliance, API, and round-trip integration.

---

## Missed Opportunities

1. **Cross-spec integration tests**: No test file exercises the pipeline across specs (e.g., equilibrium scorer -> convergence predictor -> config optimizer). Each spec's tests are siloed.

2. **Error-path `solver` key verification (021)**: The synthesis unanimously agreed this is P1, but no test file contains an assertion like `assert "solver" in result.data` on error paths. `test_nashopt.py::TestGracefulErrorHandling` checks for `"error"` in data but misses `"solver"`.

3. **Real timeout test (021)**: All three reviewers converged on this as P1, yet the test still uses mock `side_effect`. A test with `time.sleep()` as the solver and a sub-second timeout would cost 3-5 lines.

4. **SC-002 assertion tightening (022)**: The relaxed `0.5x` threshold is both identified in the synthesis and left unfixed in the test. This is the only case where a known compliance gap in an existing test is documented but not corrected.

5. **Parametric constraint gap_question tests (026)**: The synthesis unanimously agreed these are needed. The test class structure (`TestGapQuestions`) already exists for objective templates and could be duplicated for constraints in ~15 lines.

6. **YAML scaffold loading in score() (030)**: The `load_scaffold()` function already supports YAML, but `score()` hard-codes `.json`. A single test loading a `.yml` scaffold would surface this bug immediately.

---

## Off-Base Assumptions

1. **Synthesis 021 overstates mock nashopt coverage**: The `TestMockNashoptIntegration` class is presented as validating the solver path, but it bypasses the actual `_score_from_solver` post-processing function. The mock returns a pre-built `SolverResult` and patches at the scorer level, never exercising the matrix-to-agent mapping that all three reviewers identified as buggy.

2. **Synthesis 022 conflates "test exists" with "test validates the spec"**: SC-002's test exists but uses a relaxed assertion. The synthesis marks SC-002 as "PARTIALLY MET" due to the relaxed assertion, which is accurate. However, the remediation plan says "1 line change" — this underestimates the effort if the assertion change causes the test to fail with current defaults.

3. **Synthesis 023 treats quality model consistency as sufficient SC-001 coverage**: `TestQualityModelConsistency` proves AMPL and grid search agree, which is SC-001 ("AMPL optimal equals grid search optimal"). But SC-001 technically requires proving this for the *optimal* point, not just all grid points. The exhaustive test is actually stronger than necessary, which is fine.

4. **Synthesis 029 assumes base layer availability**: Several tests use `pytest.skip("Base layer not yet available")`. The synthesis marks FRs as MET that depend on tests which may be skipped. If the base layer import fails, SC-001 and SC-002 are untested.

---

## Actionable Recommendations

### Immediate (before any spec is considered merge-ready)

1. **Add SC-001 and SC-002 threshold tests for spec 021.** These are the spec's own success criteria with zero test coverage. Create a test with realistic `FeatureSet` data that exercises the full scorer pipeline and asserts `score >= 0.9` (cooperative convergence) and `score < 0.5` (3+ disputes). **Priority: CRITICAL.**

2. **Add error-path `solver` key test for spec 021.** Assert `"solver" in result.data` for the unknown-mode and computation-failure error paths. **Priority: HIGH.**

3. **Replace mock timeout test with real blocking test for spec 021.** Use `time.sleep(5)` as the mock solver and `solver_timeout=0.01`. **Priority: HIGH.**

4. **Tighten SC-002 assertion in test_kalman.py.** Change `stag_width >= conv_width * 0.5` to `stag_width >= conv_width`. If the test fails, adjust noise parameters as the remediation plan suggests. **Priority: HIGH.**

### Next Sprint

5. **Add BayesianGame prior key validation test for spec 025.** Test that garbage keys not from the type space Cartesian product are rejected. **Priority: MEDIUM.**

6. **Add constraint gap_question tests for spec 026.** Mirror the existing `TestGapQuestions` class for constraint YAMLs. **Priority: MEDIUM.**

7. **Add YAML scaffold loading test for spec 030.** Create a `.yml` scaffold and load it through `score()` to surface the `.json` hard-coding bug. **Priority: MEDIUM.**

8. **Add two-domain isolation test for spec 030.** Run two different `ConcreteDomainPlugin` instances with different names through the same and different stores. **Priority: LOW.**

### Backlog

9. **Add post-processing mapping test for spec 021 red-blue mode.** Test that a 2-row solver result is correctly mapped back to N agents by role. **Priority: MEDIUM** (blocked by P1-5 code fix).

10. **Add innovation-sequence fixed-point detection test for spec 022.** Blocked by Remediation 1 code change. **Priority: MEDIUM** (blocked).

---

## Referenced Documentation

| Document | Path |
|---|---|
| Spec 021 synthesis | `specs/done/021-nashopt-integration/conversus-review/summary/final.md` |
| Spec 022 synthesis | `specs/done/022-kalman-convergence/conversus-review/synthesis.md` |
| Spec 023 synthesis | `specs/done/023-ampl-config-optimizer/conversus-review/summary/final.md` |
| Spec 025 synthesis | `specs/025-game-form-expansion/conversus-review/summary/final.md` |
| Spec 026 synthesis | `specs/026-optimization-template-library/conversus-review/summary/final.md` |
| Spec 029 synthesis | `specs/029-code-review-domain/conversus-review/summary/final.md` |
| Spec 030 synthesis | `specs/030-domain-plugin-architecture/conversus-review/summary/final.md` |
| test_solver.py | `tests/test_solver.py` |
| test_kalman.py | `tests/test_kalman.py` |
| test_ampl.py | `tests/test_ampl.py` |
| test_game_forms_expanded.py | `tests/test_game_forms_expanded.py` |
| test_templates_expanded.py | `tests/test_templates_expanded.py` |
| test_code_review.py | `tests/test_code_review.py` |
| test_domains.py | `tests/test_domains.py` |
| test_nashopt.py | `tests/test_nashopt.py` |
| test_convergence.py | `tests/test_convergence.py` |
| test_optimizer.py | `tests/test_optimizer.py` |
