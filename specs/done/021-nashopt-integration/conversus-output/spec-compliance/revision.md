# Phase 3 Revision: spec-compliance

**Agent**: spec-compliance
**Spec**: 021-nashopt-integration
**Date**: 2026-04-01
**Inputs**: solver-engineer cross-review, plugin-engineer cross-review

---

## Disposition of Original Recommendations

### P1-1. Resolve FR-004 normalization mismatch -- MODIFIED

**Original**: Either implement max-distance normalization or amend the spec.

**Cross-review convergence**: All three reviewers agree on the gap. solver-engineer now leans toward option (b): amend the spec to say "clamped" rather than "normalized." The reasoning is that consumers use the score as a threshold indicator (>= 0.9 for converged, < 0.5 for disputed), not as a relative ranking across games.

**Revised position**: I accept option (b). The spec should be amended from "normalized to [0.0, 1.0] by the maximum possible distance for the game form" to "clamped to [0.0, 1.0]". This is a spec change, not a code change. The current implementation is correct under the amended spec.

**Priority**: Remains P1 (spec amendment needed).

---

### P1-2. Include scorer.py in review artifacts -- MAINTAINED

**Original**: Include scorer.py to verify FR-007 and SC-004.

**Cross-review support**: Unanimous across all three reviewers.

**Priority**: Remains P1.

---

### P2-1. Add runtime integration tests -- MAINTAINED

**Original**: Add `@pytest.mark.skipif(not HAS_NASHOPT)` tests for SC-001 and SC-002.

**Cross-review response**: No objections. solver-engineer implicitly supports this by noting that SC-001 and SC-002 are runtime criteria.

**Priority**: Remains P2.

---

### P3-1. Compliance traceability matrix in spec -- WITHDRAWN

**Original**: Add a matrix mapping each FR/SC to tests in the spec itself.

**Revised position**: Traceability matrices belong in the review output (which I already provide) or in the test file (via test docstrings referencing FR/SC numbers, which the test file already does). Putting it in the spec would couple the spec to its own implementation artifacts.

---

## Revised Compliance Matrix

Incorporating cross-review findings:

| Requirement | Status | Revised Note |
|------------|--------|-------------|
| FR-001 | MET | No change |
| FR-002 | MET | No change |
| FR-003 | MET | No change |
| FR-004 | PARTIALLY MET -> MET (with spec amendment) | Amend spec to "clamped" per consensus |
| FR-005 | MET | No change |
| FR-006 | MET | Add WTA shape check per solver-engineer N-1 |
| FR-007 | NOT VERIFIED -> PARTIALLY MET | Test evidence exists; production code in scorer.py. Consensus: move timeout into solver.py. |
| FR-008 | MET | No change |
| SC-001 | NOT VERIFIED | No change (runtime requirement) |
| SC-002 | PARTIALLY MET | No change |
| SC-003 | MET -> PARTIALLY MET | solver-engineer's point about dispatch scenarios is valid; full verification needs scorer.py |
| SC-004 | NOT VERIFIED -> PARTIALLY MET | Test evidence confirms behavior; production code not reviewed |

---

## New Recommendations from Cross-Reviews

### N-1. Verify constraints explicitly (from solver-engineer N-2)

solver-engineer verified all 4 constraints from spec section 6. I incorporate this into the compliance record:

| Constraint | Status |
|-----------|--------|
| No core nashopt/jax dependency | MET (pyproject.toml) |
| No Plugin interface change | MET (base class unchanged) |
| No heuristic breakage | MET (tests pass) |
| Independent testability | MET (pure functions tested without nashopt) |

### N-2. Add WTA shape validation (from solver-engineer N-1, plugin-engineer N-2)

Both solver-engineer and plugin-engineer identify the WTA N x 1 matrix shape as a potential incompatibility with nashopt's API. This should be classified under FR-006 (degenerate/edge cases) or as a new implementation note in the spec.

**Priority**: P1.
