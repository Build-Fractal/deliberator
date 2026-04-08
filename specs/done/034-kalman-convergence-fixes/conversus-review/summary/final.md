# Spec 034 — Kalman/Convergence Fixes: Final Synthesis

**Date**: 2026-04-01
**Deliberation**: 3 agents, 5 phases, 1 round
**Spec**: 034-kalman-convergence-fixes
**Files**: convergence.py, kalman.py, predictor.py, test_kalman.py, test_convergence.py, test_cross_plugin.py

---

## 1. Process Summary

| Agent | Role | Key Findings |
|---|---|---|
| **kalman-mathematician** | Filter correctness | All 9 spec items verified; Q/R dimension assertion needed |
| **plugin-integration-engineer** | Wiring/integration | Cross-plugin accumulation correct; engine persistence dependency identified |
| **spec-compliance** | Compliance audit | 7/9 items MET, 1 PARTIAL, 1 DEFERRED; all success criteria achievable |

---

## 2. Recommendation Scorecard

### Unanimous (all 3 agents agree)

| ID | Priority | Recommendation | Status |
|---|---|---|---|
| C-2 | IMPLEMENTED | eq_score accumulation across rounds | Confirmed in predictor.py:252-274 |
| C-3 | IMPLEMENTED | None sentinel replaces 0.0 comparison | Confirmed in convergence.py:277-281 |
| NEW-1 | IMPLEMENTED | Auto-sized Q/R from observation dimension | Confirmed in kalman.py:230-275, 399-407 |
| M-5 | IMPLEMENTED | R[2][2] = 0.05 for eq_score | Confirmed in kalman.py:270 |
| NEW-7 | IMPLEMENTED | Initial P = 0.25 for eq_score | Confirmed in kalman.py:416-417 |
| NEW-2 | IMPLEMENTED | 3D innovation diagnostic logging | Confirmed in kalman.py:431-444 |
| RE-1 | **P1** | Add Q/R dimension assertion at run_kalman_filter entry | Crash prevention |
| M-1 | **P2** | Verify/write 3D e2e test with mathematical property checks | SC-004 |
| C-3-TEST | **P2** | Verify test_2d_with_all_zero_eq_scores was inverted per spec | Compliance |

### Majority (2 of 3 agree)

| ID | Priority | Recommendation | Dissent |
|---|---|---|---|
| ENGINE-1 | **REQUIRED-ELSEWHERE** | Engine must persist plugin_results into RoundState | kalman-mathematician: P2 here; others: engine spec |

### Deferred

| ID | Priority | Recommendation | Rationale |
|---|---|---|---|
| NEW-6 | P3 | Joseph form covariance update | Acceptable for max-5-round constraint |
| Q/R-PASS | P3 | Forward plugin_config Q/R to convergence module | Auto-sizing covers all real-world usage |
| NONE-CARRY | P3 | Document None-to-last-known carry-forward assumption | Modeling decision, not a bug |

---

## 3. Success Criteria

| SC | Verdict | Evidence |
|---|---|---|
| SC-001 | **PASS** | Accumulation enables real slope computation (depends on engine persistence) |
| SC-002 | **PASS** | None sentinel — 0.0 enters 3D filter |
| SC-003 | **PASS** | Auto-sizing from observation dimension |
| SC-004 | **CONDITIONAL** | 3D e2e test needs verification with enhanced criteria |

---

## 4. Convergence

All agents converged in Round 1. No P1 disputes remain.

Key concessions:
- plugin-integration-engineer downgraded F-4 (history roundtrip) from P1 to REQUIRED-ELSEWHERE
- kalman-mathematician upgraded F-9 (dimension assertion) from P2 to P1
- All agents accepted test inversion gap as P2

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
## 5. Remaining Disputes

**None.** All disputes resolved in Phase 3/4.

The only outstanding concern (R[2][2] calibration basis for heuristic vs. exact solver) is P3 and does not block.
<!-- CONVERSUS:DISPUTES_END -->

---

## 6. Implementation Completeness

**7 of 9 spec items are implemented.** The remaining 2 are:
- RE-1 (dimension assertion): Not implemented, needs P1 fix
- NEW-6 (Joseph form): Deferred with TODO, acceptable

**Recommended merge sequence**: Fix RE-1 assertion -> verify M-1 test -> merge.
