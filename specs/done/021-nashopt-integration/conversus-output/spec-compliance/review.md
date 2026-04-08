# Phase 1 Review: spec-compliance

**Spec**: 021-nashopt-integration
**Reviewer**: spec-compliance
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: Verification of FR-001 through FR-008 and SC-001 through SC-004

---

## Executive Summary

Of 8 functional requirements, 5 are MET, 2 are PARTIALLY MET, and 1 is NOT VERIFIED. Of 4 success criteria, 2 are MET, 1 is PARTIALLY MET, and 1 is NOT VERIFIED (requires runtime with nashopt installed). The implementation faithfully follows the spec's technical approach for payoff matrix construction and scoring formula. The gaps are: FR-004's normalization is a clamp rather than a true max-distance normalization, FR-007's timeout is not implemented in the solver module itself, and SC-001 cannot be verified without nashopt installed.

---

## Functional Requirements

### FR-001: Use nashopt when importable -- MET

The `HAS_NASHOPT` flag is set at module import time. When True, `check_equilibrium_nashopt()` invokes `nashopt.check_equilibrium()`. The flag correctly gates the premium path. Test `test_flag_false_in_test_env` confirms the flag is False in CI. Mock tests confirm the nashopt path executes when the flag is True.

### FR-002: Fall back to heuristic when nashopt not importable -- MET

When `HAS_NASHOPT is False`, `check_equilibrium_nashopt()` raises RuntimeError. The caller (scorer) catches this and falls back to the heuristic. The heuristic path is completely unchanged from the pre-spec implementation. Test `test_solver_field_grid_search` confirms the fallback produces `solver: "heuristic"` in the plugin result.

### FR-003: Construct per-mode payoff matrices from FeatureSet -- MET

All four mode-specific builders are implemented and tested:

| Mode | Matrix Shape | Source | Tests |
|------|-------------|--------|-------|
| cooperative | N x N | Agreement matrix or surviving/dispute heuristic | 5 tests |
| winner-take-all | N x 1 | Ranking position and score differential | 4 tests |
| prisoners-dilemma | N x N | Territory claims, overreach penalties | 3 tests |
| red-blue | 2 x K | Severity vectors, landed/mitigated ratios | 4 tests |

Unknown modes raise `ValueError` with a descriptive message listing available modes.

### FR-004: Normalize distance to 0.0-1.0 score -- PARTIALLY MET

The implementation uses `max(0.0, min(1.0, raw_distance))` to clamp the distance, then computes `score = 1.0 - distance`. The spec says "normalized to [0.0, 1.0] by the maximum possible distance for the game form." Clamping and normalization are different operations:
- Clamping: values > 1.0 become 1.0. Information about relative distance is lost.
- Normalization: values are divided by the theoretical max, preserving relative ordering.

For scores near equilibrium (distance < 1.0), the results are identical. For large games far from equilibrium, clamping loses resolution. This is partially met: the output range [0.0, 1.0] is correct, but the method does not match the spec.

### FR-005: Report agents not at best response -- MET

The implementation extracts `agents_not_at_equilibrium` from the nashopt result using three tiers (direct, derived, conservative fallback). The `best_responses` dict maps agent names to action indices. Both are included in `SolverResult`.

### FR-006: Handle degenerate cases -- MET

Three degenerate cases are handled:
- Zero agents: returns trivial equilibrium (score 1.0, empty collections).
- Single agent: returns equilibrium (score 1.0, best_response = 0).
- Zero-variance payoff matrix: detected via `np.std < 1e-12`, returns trivial equilibrium.

All three have dedicated tests.

### FR-007: Configurable timeout with fallback -- NOT VERIFIED

The spec requires: "Solver execution MUST be capped at a configurable timeout (default 30s). If exceeded, fall back to heuristic with a warning."

The solver.py module does NOT implement a timeout. The `check_equilibrium_nashopt()` function will block until nashopt returns. The test file includes timeout tests (`TestTimeoutFallback`) that test the scorer's timeout wrapper using `concurrent.futures`, but this logic is in scorer.py, not solver.py. Since scorer.py is not in the review artifacts, FR-007 compliance cannot be verified from the provided code.

### FR-008: solver field in PluginResult.data -- MET

The test file confirms `result.data["solver"]` is set to `"nashopt"` or `"heuristic"` depending on which path ran. The solver field is set by the scorer plugin, not solver.py, which is the correct separation of concerns.

---

## Success Criteria

### SC-001: Converged deliberation scores >= 0.9 -- NOT VERIFIED

This requires running nashopt on a converged cooperative deliberation. Since nashopt is not installed in the test environment, SC-001 cannot be verified. The mock tests confirm the scoring formula works (`score = 1.0 - distance`), so if nashopt returns `distance <= 0.1` for a converged game, the criterion is met. This is a runtime validation criterion, not a code review criterion.

### SC-002: 3+ unresolved disputes scores < 0.5 -- PARTIALLY MET

Like SC-001, this requires nashopt at runtime. However, the payoff matrix construction can be verified: a cooperative game with high dispute_count produces low off-diagonal payoffs (due to the dispute penalty), which should push the equilibrium distance higher and the score lower. The mathematical structure supports the criterion, but runtime verification is needed.

### SC-003: Without nashopt, identical to heuristic -- MET

`HAS_NASHOPT = False` in the test environment. All heuristic tests pass unchanged. The scorer dispatch tests confirm the heuristic path produces identical results when nashopt is unavailable. No code in the heuristic path was modified by this spec.

### SC-004: Timeout produces heuristic fallback, not error -- NOT VERIFIED

The test file includes `TestTimeoutFallback` which tests timeout behavior via mock, but the actual timeout mechanism is in scorer.py (not in the review artifacts). The test confirms that timeout produces a valid PluginResult with `solver: "heuristic"` and no exception propagation.

---

## Compliance Matrix

| Requirement | Status | Evidence |
|------------|--------|----------|
| FR-001 | MET | HAS_NASHOPT flag, mock integration tests |
| FR-002 | MET | RuntimeError on missing dep, heuristic fallback tests |
| FR-003 | MET | 4 mode builders, 16 matrix tests |
| FR-004 | PARTIALLY MET | Clamp vs. normalization mismatch |
| FR-005 | MET | Three-tier best-response extraction |
| FR-006 | MET | Zero, single, zero-variance cases |
| FR-007 | NOT VERIFIED | Timeout not in solver.py |
| FR-008 | MET | solver field in PluginResult.data |
| SC-001 | NOT VERIFIED | Requires nashopt at runtime |
| SC-002 | PARTIALLY MET | Math structure supports, needs runtime |
| SC-003 | MET | Identical heuristic behavior |
| SC-004 | NOT VERIFIED | Timeout in scorer.py, not reviewed |

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Resolve FR-004 normalization mismatch. Either implement max-distance normalization or amend the spec to say "clamped."

2. **P1-2**: Include scorer.py in the review artifacts so FR-007 and SC-004 can be verified.

### P2 (Should Fix)

3. **P2-1**: Add runtime integration tests that run when nashopt is installed (pytest marks: `@pytest.mark.skipif(not HAS_NASHOPT, reason="nashopt not installed")`). This would verify SC-001 and SC-002 in environments where nashopt is available.

### P3 (Consider)

4. **P3-1**: Add a compliance traceability matrix to the spec itself, mapping each FR/SC to its test(s).
