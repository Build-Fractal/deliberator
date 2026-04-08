# Meta-Review Phase 1: Test Coverage Auditor — Wave 024-028

**Scope**: Specs 024, 027, 028
**Date**: 2026-04-01
**Auditor role**: Do tests match synthesis claims? Are P1 findings tested? Blind spots?

---

## 1. Spec 024 — Cross-Plugin Interfaces

### Test File: `tests/test_cross_plugin.py` (788 lines)

#### Coverage Map

| Synthesis Finding | Test Coverage | Status |
|-------------------|--------------|--------|
| SC-001: ConvergencePredictor uses real eq_score | `TestSC001ConvergencePredictorUsesEqScore` (1 test) | COVERED but SHALLOW |
| SC-002: Fallback to 2D when scorer absent | `TestSC002FallbackTo2D` (1 test) | COVERED |
| SC-003: Scorer before predictor (topo sort) | `TestSC003ExecutionOrder` (2 tests) | COVERED |
| SC-004: Cycle detection | `TestTopologicalSort.test_cycle_detection_raises` | COVERED |
| SC-005: Undeclared plugins unchanged | `TestSC005UnchangedBehavior` (2 tests) | COVERED |
| P1-1: Accumulate eq_scores across rounds | NO TEST | **BLIND SPOT** |
| P1-2: Zero-score sentinel gate | `test_2d_with_all_zero_eq_scores` tests the current (buggy) behavior | TESTS WRONG BEHAVIOR |
| P2-3: Duplicate producer detection | NO TEST | ACCEPTABLE (feature not implemented) |
| P2-5: 3D Kalman end-to-end test | NO TEST | **BLIND SPOT** |
| P2-8: Cross-hook plugin_results scoping | NO TEST | **BLIND SPOT** |

#### Detailed Analysis

**SC-001 test is shallow**: `test_predictor_receives_eq_score_via_plugin_results` verifies that the predictor runs and produces a valid prediction string, but does NOT verify that the eq_score actually influences the prediction numerically. It does not check whether 3D observations are built, whether the Kalman filter state dimension is 3, or whether the prediction differs from the 2D case. The test proves wiring, not behavior.

**P1-1 (accumulate history) has no test**: No test verifies that eq_scores are accumulated across multiple rounds. The existing `multi_round_state` fixture has 3 rounds of history but the predictor only receives a single eq_score from the current hook invocation. A test should run `execute_hooks` across 3 simulated rounds and verify the predictor receives all 3 scores.

**P1-2 (zero sentinel) tests the wrong thing**: `test_2d_with_all_zero_eq_scores` asserts that all-zero scores produce 2D observations. Per the synthesis, this behavior is the BUG — a score of 0.0 is meaningful (no agents at equilibrium) and should trigger 3D. The test would need to be INVERTED after the fix lands.

**P2-5 (3D Kalman)**: The `TestObservationSequence` class tests 2D/3D observation CONSTRUCTION but no test feeds 3D observations through the actual Kalman filter to verify state dimension, convergence, and confidence bounds.

**P2-8 (cross-hook scoping)**: No test verifies that `plugin_results` is reset between hook invocations at different hook points. The synthesis flags this as load-bearing undocumented behavior.

---

## 2. Spec 027 — Solver Validation Flow

### Test File: `tests/test_validation.py` (462 lines)

#### Coverage Map

| Synthesis Finding | Test Coverage | Status |
|-------------------|--------------|--------|
| FR-002: Problem type agents | `TestGenerateValidationConfig` (3 type tests) | COVERED |
| FR-003: Target list construction | 4 tests for solution/problem/objective combinations | COVERED |
| FR-004: Sensitivity instructions | `TestSensitivityInstructions` (6 tests) | WELL COVERED |
| FR-008/009: ValidationVerdict model | `TestValidationVerdict` (9 tests) | WELL COVERED |
| FR-005: SensitivityFinding model | `TestSensitivityFinding` (2 tests) | COVERED |
| SC-001: Bad assignment flagged | `TestSC001BadAssignmentFlagged` (2 tests) | COVERED |
| SC-003: Robust solution accept | `TestSC003RobustSolutionAccept` (2 tests) | COVERED |
| SC-005: Timing (16 LLM calls) | NOT DIRECTLY TESTED | IMPLICIT |
| Phase 1 gap: ConstraintAddition model | NO TEST (model not yet defined) | EXPECTED |
| Phase 1 gap: SolverSolution model | NO TEST (model not yet defined) | EXPECTED |
| Phase 1 gap: scheduling/negotiation templates | NO TEST (not yet added) | EXPECTED |
| Redundant confidence validator | NOT TESTED SPECIFICALLY | LOW PRIORITY |

#### Detailed Analysis

**Tests are well-structured and thorough for Phase 1 scope.** The test file covers positive cases, negative cases (invalid verdict, confidence out of range), boundary conditions (confidence 0.0 and 1.0), and specific SC scenarios.

**SC-005 (timing) is implicitly tested**: The test verifies config generates 3 agents with rounds=1, iterations=1. The 16-call calculation follows from the engine's 5-phase pipeline definition. No test directly counts LLM calls, which is correct — that would require an integration test.

**Redundant field_validator**: The synthesis notes that `confidence_in_range` is redundant with `ge=0.0, le=1.0` Field constraints. The tests exercise both paths (Pydantic Field constraint and the validator), so removing the validator would not lose coverage — the `ge`/`le` constraints would still catch out-of-range values.

**Missing problem types**: The synthesis notes that scheduling and negotiation templates are missing from `_AGENT_TEMPLATES`. The test `test_unknown_problem_type_raises` correctly tests that "scheduling" raises ValueError, confirming the gap.

---

## 3. Spec 028 — Mode Expansion

### Test File: `tests/test_mode_expansion.py` (EMPTY — 1 line)

#### Coverage Map

| Synthesis Finding | Test Coverage | Status |
|-------------------|--------------|--------|
| P1-1: Mode count >= 8 | NO TEST | **CRITICAL BLIND SPOT** |
| P1-2: ration regex bug | NO TEST | **CRITICAL BLIND SPOT** |
| P1-3: Spec text update | N/A (documentation) | N/A |
| FR-001 through FR-012 | NO TEST | **CRITICAL BLIND SPOT** |
| SC-001 through SC-005 | NO TEST | **CRITICAL BLIND SPOT** |
| Template completeness (7 per mode) | NO TEST | **BLIND SPOT** |
| Keyword classification routing | NO TEST | **BLIND SPOT** |
| Backward compatibility regression | NO TEST | **BLIND SPOT** |
| DecisionType enum completeness | NO TEST | **BLIND SPOT** |
| VALID_MODES consistency across files | NO TEST | **BLIND SPOT** |

#### Detailed Analysis

**This is the most critical gap across all three specs.** The synthesis unanimously identified this as the #1 action item. Every claim about mode expansion — correct mappings, no redundancy, template completeness, keyword routing — is unverified by tests.

**Partial mitigation**: Some mode-related behavior is tested indirectly:
- `test_construction.py` tests `classify_decision_type()` for the original 4 types (SELECTION, INTEGRATION, SCOPING, STRESS_TEST)
- `engine/config.py` tests (if they exist) would validate the VALID_MODES tuple
- Template loading tests (if they exist) would validate template discovery

But NONE of the 4 new modes (negotiation, resource-allocation, fair-division, mechanism-design) have dedicated classification, template, or routing tests.

---

## 4. Cross-Spec Test Gaps

### Gap 1: No integration test for scorer -> predictor -> validation

No test verifies the full chain: EquilibriumScorer produces a score, ConvergencePredictor consumes it and makes a prediction, and that prediction could feed into a validation deliberation. This spans 024 and 027.

### Gap 2: No test for new modes through the plugin pipeline

No test verifies that the 4 new modes (028) work correctly with the equilibrium scorer (024). The scorer has a mode-based payoff dispatch (`compute_payoff(mode, ...)`) but no test exercises it with "negotiation", "resource-allocation", "fair-division", or "mechanism-design".

### Gap 3: No test for VALID_MODES consistency

No test verifies that `engine/config.py:VALID_MODES`, `features.py:VALID_MODES`, and `objectives.py:VALID_MODES` contain the same set. A single assertion test would catch drift.

---

## 5. P1 Findings vs. Test Coverage Summary

| Spec | P1 Finding | Tested? | Risk if Untested |
|------|-----------|---------|-----------------|
| 024 | Accumulate eq_scores across rounds | NO | HIGH — silent data loss each round |
| 024 | Fix zero-score sentinel gate | TESTS WRONG BEHAVIOR | HIGH — test will fail after fix (expected) |
| 027 | ConstraintAddition model | NO (not yet built) | MEDIUM — future Phase 1 |
| 027 | SolverSolution model | NO (not yet built) | MEDIUM — future Phase 1 |
| 028 | Populate test_mode_expansion.py | NO (the finding IS the gap) | CRITICAL — no mode expansion verification |
| 028 | Fix ration regex | NO | MEDIUM — misclassification edge case |
| 028 | Update spec text | N/A | N/A |

---

## 6. Verdict

| Spec | Test Quality | P1 Coverage | Blind Spots |
|------|-------------|-------------|-------------|
| 024 | GOOD structure, SHALLOW on numerical correctness | 0/2 P1 items tested | 3D Kalman e2e, cross-hook scoping, eq_score accumulation |
| 027 | STRONG for Phase 1 scope | N/A (Phase 1 items are additive) | Phase 2/3 entirely untested (expected) |
| 028 | ABSENT | 0/2 testable P1 items tested | Everything — empty test file |

**Overall test health**: 024 has good structural coverage but numerical blind spots. 027 is the strongest. 028 has zero test coverage and is the top priority for remediation.
