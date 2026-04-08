# Phase 3 Revision: spec-compliance

**Agent**: spec-compliance
**Spec**: 023-ampl-config-optimizer
**Date**: 2026-04-01
**Inputs**: optimization-engineer cross-review, plugin-engineer cross-review

---

## Disposition of Original Recommendations

### P1-1. Extract actual optimality gap (FR-012) -- MAINTAINED

**Original**: Read gap from HiGHS rather than hardcoding 0.0.

**Cross-review support**: All three reviewers agree. optimization-engineer provides implementation guidance (check `solve_result_num`).

**Priority**: Remains P1.

---

### P2-1. Add runtime integration tests -- MAINTAINED

**Original**: `@pytest.mark.skipif(not HAS_AMPL)` tests for SC-001 and SC-003.

**Cross-review response**: optimization-engineer argues SC-001 is MET by mathematical construction. plugin-engineer supports a runtime test as a safety net.

**Revised position**: I accept that SC-001 is MET by construction (the MIP and grid search solve the same problem). Runtime tests are still valuable as end-to-end validation. Maintain the recommendation as P2.

**Priority**: Remains P2.

---

### P2-2. Verify constraints -- MAINTAINED

**Original**: Explicitly verify all 4 constraints from Section 6.

Constraints verified:
- No amplpy/highspy in core requirements: MET (not in pyproject.toml).
- No Plugin interface change: MET.
- No grid search breakage: MET.
- AMPL model readable/editable: PARTIALLY MET (Python string, not .mod file).

The 4th constraint is partially met. The `write_config_model()` helper (plugin-engineer N-2) would resolve this.

**Priority**: Remains P2.

---

### P3-1. Document MIP-vs-grid-search performance -- MAINTAINED

Downgraded from optimization-engineer's original P1 to P3 per my cross-review recommendation.

**Priority**: Remains P3.

---

## Revised Compliance Matrix

| Requirement | Original | Revised | Note |
|------------|----------|---------|------|
| FR-001 | MET | MET | HAS_AMPL should also check highspy (P1 fix) |
| FR-002 | MET | MET | No change |
| FR-003 | MET | MET | No change |
| FR-004 | MET | MET | No change |
| FR-005 | MET | MET | No change |
| FR-006 | MET | MET | HiGHS time_limit sufficient per FR-006 wording |
| FR-007 | MET | MET | No change |
| FR-008 | MET | MET | No change |
| FR-009 | MET | MET | No change |
| FR-010 | MET | MET | No change |
| FR-011 | MET | MET | No change |
| FR-012 | PARTIALLY MET | PARTIALLY MET | Gap still hardcoded, P1 fix |
| SC-001 | NOT VERIFIED | MET (construction) | Math proof + P2 runtime test |
| SC-002 | NOT VERIFIED | NOT VERIFIED | Performance criterion, needs runtime |
| SC-003 | PARTIALLY MET | PARTIALLY MET | Mock test only; P2 runtime test |
| SC-004 | MET | MET | No change |
| Constraints | - | 3 MET, 1 PARTIALLY MET | .mod file storage not met |

---

## New Recommendations from Cross-Reviews

### N-1. Amend spec for grid-point lookup approach (from optimization-engineer N-3)

The spec describes "piecewise linear approximation" but the implementation uses grid-point binary selection. The implementation is exact (0% error), exceeding the spec's "within 5%" requirement. The spec should be amended.

**Priority**: P2 (spec hygiene).

### N-2. Check highspy in HAS_AMPL (from plugin-engineer P1-1, adopted by all)

Consensus P1 finding.

### N-3. Solver name convention for non-HiGHS solvers (from my cross-review of plugin-engineer)

FR-011 says `solver: "ampl-highs"`. If a user uses `solver="gurobi"` in the general-purpose API, the dispatch layer still reports "ampl-highs". The convention should be `"ampl-{solver}"`.

**Priority**: P3 (extensibility concern).
