# Phase 5 Synthesis: Spec 021 -- nashopt Solver Integration

**Spec**: 021-nashopt-integration
**Date**: 2026-04-01
**Agents**: solver-engineer, plugin-engineer, spec-compliance

---

## Overall Assessment

The nashopt solver integration is well-implemented. Payoff matrix construction for all four modes is mathematically sound and thoroughly tested. The HAS_NASHOPT flag pattern correctly follows the established optional-dependency plugin convention. Degenerate cases are handled. The SolverResult dataclass is well-designed with consumer-friendly field names. The primary gaps are: (1) FR-007 timeout is not implemented in solver.py (lives in scorer.py, which was not in the review artifacts), (2) FR-004's distance metric is clamped rather than normalized (spec amendment needed), and (3) the WTA mode's non-square payoff matrix may be incompatible with nashopt's API. Full consensus was achieved with no remaining disputes.

---

## Consensus Findings

### 1. Payoff Matrix Construction Correct for All Modes (Consensus)

**Unanimous**. All four mode-specific builders produce matrices of the correct shape with correct formulas:
- Cooperative: N x N with agreement matrix (precise) or surviving/dispute heuristic (approximate).
- Winner-take-all: N x 1 ranking payoff vector.
- Prisoners-dilemma: N x N territory overlap with overreach penalties.
- Red-blue: 2 x K severity/mitigation matrix with team aggregation.

16 dedicated tests cover shape, values, edge cases, and the unknown-mode error path.

### 2. Spec Amendment Needed for FR-004 Distance Metric (Consensus)

**Unanimous**. The spec says distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form." The implementation clamps via `max(0.0, min(1.0, raw_distance))`. These are different operations. All three agents agree the spec should be amended to say "clamped to [0.0, 1.0]" since consumers use the score as a threshold indicator, not a relative ranking across games.

### 3. Timeout Must Move into solver.py (Consensus)

**Unanimous**. FR-007 requires a configurable timeout (default 30s) with heuristic fallback. Currently, the timeout is implemented in scorer.py (not reviewed). All agents agree it should be implemented in `check_equilibrium_nashopt()` via a `timeout_seconds: int = 30` parameter using `concurrent.futures.ThreadPoolExecutor`. This ensures every caller gets timeout protection automatically.

### 4. scorer.py Must Be Included in Future Reviews (Consensus)

**Unanimous**. The scorer dispatch logic, timeout wrapper, and PluginResult construction all live in scorer.py. Without it, FR-007, FR-008, SC-001, SC-002, SC-004 cannot be fully verified. This is the highest-impact process improvement.

### 5. WTA Matrix Shape Compatibility Must Be Verified (Consensus)

**Unanimous**. The WTA builder returns an N x 1 matrix (column vector). If nashopt's `check_equilibrium()` expects square matrices, this will cause a runtime error. A shape compatibility check should be added to `check_equilibrium_nashopt()` before calling nashopt.

### 6. All Constraints MET (Consensus)

**Unanimous** (verified by solver-engineer, confirmed by all):
- No nashopt/jax in core requirements: MET.
- No Plugin interface change: MET.
- No heuristic breakage: MET.
- solver.py independently testable: MET.

### 7. Degenerate Cases Correctly Handled (Consensus)

**Unanimous**. Zero-agent (vacuous equilibrium), single-agent (trivial equilibrium), and zero-variance (any-strategy equilibrium) cases are all handled with correct mathematical justification.

### 8. HAS_NASHOPT Flag Pattern Correct (Consensus)

**Unanimous**. The module-level import with flag is the established pattern across the plugin system (matches HAS_AMPL in spec 023). Minor improvement suggested: separate nashopt and numpy imports for better error diagnostics.

---

<!-- DISPUTES_BEGIN -->

## Unresolved Disputes

None. All disagreements were resolved during the cross-review and revision phases. The specific resolutions:

- **Distance normalization**: Resolved by consensus to amend the spec (clamp, not normalize).
- **Timeout location**: Resolved by consensus to implement in solver.py.
- **Red-blue aggregation**: Resolved -- solver-engineer withdrew after spec-compliance showed the spec explicitly calls for combined rows.
- **FR-007 status**: Resolved as PARTIALLY MET with test evidence; full verification pending scorer.py inclusion.

<!-- DISPUTES_END -->

---

## Compliance Summary

| Requirement | Status | Action |
|------------|--------|--------|
| FR-001 | MET | None |
| FR-002 | MET | None |
| FR-003 | MET | None |
| FR-004 | MET (with amendment) | Amend spec: "clamped" not "normalized" |
| FR-005 | MET | None |
| FR-006 | MET | Add WTA shape check |
| FR-007 | PARTIALLY MET | Move timeout into solver.py |
| FR-008 | MET | None |
| SC-001 | NOT VERIFIED | Requires nashopt at runtime |
| SC-002 | PARTIALLY MET | Math supports; needs runtime verification |
| SC-003 | PARTIALLY MET | Needs scorer.py review |
| SC-004 | PARTIALLY MET | Test evidence; needs scorer.py |

---

## Recommended Actions (Priority Order)

1. **P1**: Amend spec FR-004 wording from "normalized" to "clamped."
2. **P1**: Add `timeout_seconds` parameter to `check_equilibrium_nashopt()` with ThreadPoolExecutor.
3. **P1**: Add WTA matrix shape validation or padding before nashopt call.
4. **P1**: Include scorer.py in review artifacts for next review cycle.
5. **P2**: Separate nashopt/numpy imports in the try block for better diagnostics.
6. **P2**: Add `__all__` to solver.py and verify __init__.py re-exports HAS_NASHOPT.
7. **P2**: Add `@pytest.mark.skipif(not HAS_NASHOPT)` runtime tests for SC-001/SC-002.
8. **P2**: Document cooperative heuristic's uniform dispute penalty limitation.
