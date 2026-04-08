# Test Coverage Audit — Wave 034-038

**Auditor**: test-coverage-auditor
**Date**: 2026-04-01
**Specs reviewed**: 034, 035, 036, 037, 038
**Method**: Test file analysis against spec success criteria and P1 findings

---

## Per-Spec Test Coverage

### Spec 034 — Kalman/Convergence Fixes

| SC/Finding | Test | Status |
|---|---|---|
| SC-001 (eq_score trend non-zero) | test_convergence.py | COVERED (accumulation enables slope) |
| SC-002 (0.0 enters 3D filter) | test_cross_plugin.py | NEEDS VERIFICATION |
| SC-003 (auto-sized Q/R produces 3x3) | test_kalman.py | COVERED (auto-sizing test exists) |
| SC-004 (3D e2e test) | test_kalman.py | CONDITIONAL — needs verification of mathematical property checks |
| RE-1 P1 (Q/R dimension assertion) | MISSING | **GAP** — no test for dimension mismatch crash |
| C-3 test inversion | NEEDS VERIFICATION | **GAP** — test_2d_with_all_zero_eq_scores may be stale |

**Coverage score**: 2/4 SC confirmed, 2/4 conditional. 1 P1 test gap.

### Spec 035 — Plugin Framework Fixes

| SC/Finding | Test | Status |
|---|---|---|
| SC-001 (DuplicateProducerError) | test_cross_plugin.py | COVERED — test exists |
| SC-002 (missing produces warning) | test_plugins.py | COVERED — test exists |
| SC-003 (cross-hook scoping) | MISSING | **GAP** — M-2 test not written |

**Coverage score**: 2/3 SC covered, 1/3 missing.

### Spec 036 — Mode & Template Fixes

| SC/Finding | Test | Status |
|---|---|---|
| SC-001 (40+ tests) | test_mode_expansion.py | COVERED — 40+ tests present |
| SC-002 (rational not resource_allocation) | TestRationRegexFix | COVERED — 5 tests |
| SC-003 (sync test catches drift) | TestValidModesConsistency | COVERED — simulated drift test |
| SC-004 (deliberation per mode) | N/A | OPERATIONAL — not automated |

**Coverage score**: 3/3 automatable SC covered. Best coverage in the wave.

### Spec 037 — Validation Flow Fixes

| SC/Finding | Test | Status |
|---|---|---|
| SC-001 (ConstraintAddition validates) | test_validation.py | COVERED |
| SC-002 (SolverSolution validates) | test_validation.py | COVERED |
| SC-003 (qualitative sensitivity) | test_validation.py | COVERED (has_sensitivity_instructions test) |
| SC-004 (all modes have templates) | test_validation.py | COVERED (config generation per type) |

**Coverage score**: 4/4 SC covered. Full test coverage.

### Spec 038 — Solver & Equilibrium Fixes

| SC/Finding | Test | Status |
|---|---|---|
| SC-001 (spec 021 table matches code) | N/A | DOCUMENTATION — no test applicable |
| SC-002 (cooperative documented as heuristic) | N/A | DOCUMENTATION — code comment, not testable |
| SC-003 (spec 024 section 8 accurate) | N/A | DOCUMENTATION — not testable |
| PAYOFF-NEW P1 (missing payoff functions) | MISSING | **GAP** — no test verifying scorer handles new modes |

**Coverage score**: 0/3 testable SC (all documentation). 1 P1 gap (payoff functions).

---

## Wave-Level Summary

| Spec | SC Covered | SC Total | P1 Test Gaps | Rating |
|---|---|---|---|---|
| 034 | 2 (+ 2 conditional) | 4 | 1 (RE-1 dimension) | FAIR |
| 035 | 2 | 3 | 0 (M-2 is P2) | GOOD |
| 036 | 3 | 3 | 0 | EXCELLENT |
| 037 | 4 | 4 | 0 | EXCELLENT |
| 038 | 0 | 0 (all docs) | 1 (PAYOFF-NEW) | N/A |

---

## P1 Test Gaps (must address)

1. **Spec 034 RE-1**: No test for Q/R dimension mismatch causing crash in `run_kalman_filter`.
2. **Spec 038 PAYOFF-NEW**: No test verifying scorer behavior for new modes (negotiation, resource-allocation, fair-division, mechanism-design). The scorer should return a graceful error, not an unhandled exception.

## P2 Test Gaps (should address)

3. **Spec 035 M-2**: Cross-hook scoping test not written.
4. **Spec 034 C-3**: test_2d_with_all_zero_eq_scores inversion not verified.
5. **Spec 034 SC-004**: 3D e2e test needs mathematical property verification.
