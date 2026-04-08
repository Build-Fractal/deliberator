# solver-engineer Cross-Review of spec-compliance

**Cross-reviewer**: solver-engineer
**Reviewing**: spec-compliance Phase 1 review of spec 021
**Date**: 2026-04-01

---

## Agreements

### 1. FR-004 normalization mismatch is correctly identified

spec-compliance's distinction between clamping and normalization is mathematically precise. The spec says "normalized by the maximum possible distance for the game form." The implementation clamps. These are different operations. I independently noted this (my P1-2) with the same technical analysis. This should be resolved before the spec is finalized.

### 2. SC-001 and SC-002 are runtime criteria, not code review criteria

spec-compliance correctly classifies these as NOT VERIFIED / PARTIALLY MET. The mathematical structure of the payoff matrices supports the criteria (converged games -> low distance -> high score; disputed games -> high distance -> low score), but runtime verification requires nashopt. The recommendation to add `@pytest.mark.skipif` runtime tests (P2-1) is the right approach.

### 3. FR-003 compliance matrix is thorough

The per-mode breakdown with test counts provides clear traceability. All four mode builders are accounted for. The `ValueError` for unknown modes is correctly noted.

---

## Tensions

### 1. FR-007 classification

spec-compliance classifies FR-007 as NOT VERIFIED because the timeout is not in solver.py. I would classify it as PARTIALLY MET rather than NOT VERIFIED. The test file (test_solver.py) contains timeout tests that demonstrate the mechanism works via mock. The tests are part of the review artifacts. While the production code implementing the timeout is not in the reviewed files, the tests provide evidence that the feature exists and works. NOT VERIFIED implies no evidence at all; PARTIALLY MET better reflects the situation where tests pass but production code is not directly reviewed.

### 2. SC-003 may be overstated as MET

spec-compliance marks SC-003 (identical heuristic behavior without nashopt) as MET. While it is true that no heuristic code was modified, SC-003 requires that behavior is "identical to the current heuristic implementation." If the scorer.py dispatch logic has a bug where it accidentally passes different parameters to the heuristic path when HAS_NASHOPT is True (but solver times out) versus when HAS_NASHOPT is False, the behavior would differ. Without reviewing scorer.py, we can say the heuristic code is unchanged but not that the behavior is identical in all dispatch scenarios. I would mark SC-003 as PARTIALLY MET.

---

## Missed Opportunities

### 1. No analysis of payoff matrix mathematical properties

spec-compliance verifies that the matrix builders match the spec's table structure (N x N, N x 1, etc.) and that tests exist. But the compliance review does not assess whether the mathematical formulas in the code match the spec's prose descriptions. For example, the spec says the cooperative matrix uses "Agreement matrix from features + dispute counts." The code's heuristic path uses `avg_surviving - dispute_count / n`, which is a specific interpretation of that prose. spec-compliance should have verified that the formula is a faithful encoding of the spec's intent, not just that a matrix of the right shape exists.

### 2. Constraint verification is incomplete

The spec has 4 constraints:
- Must NOT add nashopt/jax to core package requirements.
- Must NOT change the Plugin interface or output format.
- Must NOT break the heuristic fallback path.
- solver.py must be independently testable with mock payoff matrices.

spec-compliance does not explicitly verify these. The first three are implicitly covered (the import is optional, the output format is unchanged, the heuristic is untouched), but the fourth (independent testability) deserves explicit mention -- it is met because `build_payoff_matrix()` and `build_strategy_profile()` are pure functions that accept plain data and return plain data.
