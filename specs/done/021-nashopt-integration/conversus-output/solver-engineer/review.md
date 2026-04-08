# Phase 1 Review: solver-engineer

**Spec**: 021-nashopt-integration
**Reviewer**: solver-engineer
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: Mathematical correctness of payoff matrices, nashopt wrapper design, timeout/fallback robustness

---

## Executive Summary

The nashopt solver integration is mathematically sound in its core design. The per-mode payoff matrix constructors correctly encode the game-theoretic structure for each deliberation mode, the SolverResult normalization is correct, and degenerate-case handling covers the necessary edge cases. However, there are three issues of varying severity: (1) the cooperative mode's heuristic off-diagonal formula applies a per-agent dispute penalty that should arguably be a per-pair penalty, (2) the red-blue payoff matrix construction loses information by collapsing multiple red agents into a single aggregated row rather than preserving per-agent structure, and (3) the timeout mechanism described in FR-007 is specified in the spec but not implemented in solver.py -- the caller (scorer.py) must implement timeout wrapping externally, which is not documented.

---

## Payoff Matrix Correctness (FR-003)

### Cooperative Mode -- Correct with Minor Formula Concern

The cooperative matrix builder produces an N x N agreement/dispute matrix. The diagonal (self-payoff = surviving_count) is correct -- an agent's value to itself is the number of recommendations that survived deliberation. The off-diagonal logic has two paths:

1. **Agreement matrix path**: When `features.agreement_matrix` is populated, the off-diagonal entry is taken directly. This is correct.

2. **Heuristic path**: When no agreement matrix is available, the formula is `avg_surviving - dispute_count / max(n, 1)`. The dispute penalty term `dispute_count / n` divides the total dispute count evenly across all agents. This is a reasonable simplification but creates a subtle issue: in a 3-agent game where agent A has 0 disputes with agent B but 3 disputes with agent C, both off-diagonal entries for A get the same penalty (3/3 = 1.0). The payoff matrix cannot distinguish between these pairwise relationships. This is acceptable for a heuristic -- the agreement matrix path handles the precise case -- but the docstring should note this limitation.

### Winner-Take-All Mode -- Correct

The N x 1 ranking payoff vector is mathematically clean. The winner (position 1) gets 1.0. Other agents receive `1.0 - (position - 1) * min(score_differential / n, 1.0)`. The clamping via `min(..., 1.0)` prevents negative payoffs. The `max(0.0, ...)` outer clamp is redundant when score_differential is non-negative but harmless as a safety net. Agents with `ranking_position == 0` (unranked) correctly receive 0.0.

### Prisoners-Dilemma Mode -- Correct

The territory overlap matrix correctly computes:
- Diagonal: net territory (core + unique + shared - deferrals) minus net overreach (overreach_count - overreach_rebutted, floored at 0). This incentivizes claiming territory while penalizing overreach.
- Off-diagonal: shared territory minus overlap cost (0.5 * net overreach). The 0.5 coefficient is a design choice that makes overreach costly but not catastrophic for interactions. This is a reasonable calibration.

The formula is well-suited for the prisoners-dilemma game form because it creates the tension between cooperation (shared territory benefit) and defection (overreach penalty).

### Red-Blue Mode -- Correct Structure, Information Loss

The 2 x K matrix structure is correct for the adversarial two-team game. The severity vector aggregation (summing across red agents) and the landed/mitigated ratio scaling are mathematically sound. The fallback to a 2x1 matrix when no severity vectors exist is correctly handled.

**Concern**: When there are multiple red agents, their severity vectors are summed element-wise. This loses per-agent severity information. If red-team-A found a critical vulnerability (severity [10, 0, 0]) and red-team-B found minor issues (severity [0, 1, 1]), the aggregated row is [10, 1, 1] -- which masks the fact that the critical finding came from a specific agent. For equilibrium analysis purposes, this aggregation is acceptable because the red team acts as a collective, but it limits the ability to identify which specific red agent drove the equilibrium state.

---

## Scoring Formula and Normalization (FR-004)

The core formula `score = 1.0 - distance` is correct, with `distance` clamped to [0.0, 1.0]. The clamping is important because nashopt's raw distance can exceed 1.0 for large games. The rounding to 6 decimal places for distance and 4 for score is appropriate for numerical stability.

One subtlety: the spec says distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form." The implementation uses `max(0.0, min(1.0, raw_distance))` -- a clamp, not a normalization by max distance. If nashopt returns a raw distance of 2.5 for a large game, the clamped distance is 1.0 (score = 0.0), which loses resolution. True normalization would divide by the theoretical maximum distance for the game form, preserving the relative ordering of non-equilibrium states. This is a spec-implementation mismatch. For the current use case (score -> consumer), the clamp is pragmatically sufficient, but it is not mathematically what the spec describes.

---

## Degenerate Case Handling (FR-006)

### Zero-agent game: Correct
Returns equilibrium with score 1.0, empty best_responses and agents_not_at_equilibrium. This is the vacuous truth interpretation -- with no agents, the system is trivially at equilibrium.

### Single-agent game: Correct
Returns equilibrium with score 1.0 and best_response = 0. A single agent is always at its best response (no opponents to deviate against).

### Zero-variance payoff matrix: Correct
Detected via `np.std(payoff_matrix) < 1e-12`. When all payoffs are identical, any strategy profile is an equilibrium. The threshold 1e-12 is tight enough to avoid false positives from floating-point noise.

---

## Best-Response Reporting (FR-005)

The logic for extracting agents_not_at_equilibrium has three tiers:
1. If nashopt returns `agents_not_at_equilibrium`, use it directly.
2. If nashopt says not at equilibrium but does not provide per-agent info, assume ALL agents are not at best response.
3. If at equilibrium, agents_not_at_equilibrium is empty.

Tier 2 is conservative (assumes worst case), which is correct for a safety-critical analysis tool. The `hasattr` checks protect against nashopt API changes, which is good defensive programming.

---

## Timeout/Fallback (FR-007)

**Gap**: The solver.py module does not implement timeout logic. The spec requires a configurable timeout with default 30s and fallback to heuristic. The `check_equilibrium_nashopt()` function will block indefinitely if nashopt itself hangs. The timeout must be implemented at the call site (scorer.py) using `concurrent.futures.ThreadPoolExecutor` or `signal.alarm`, but this responsibility is not documented in solver.py and no guidance is provided to callers.

The test file (test_solver.py) references timeout testing but the mechanism is external to the module under review.

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Document the timeout responsibility. Add a docstring note to `check_equilibrium_nashopt()` stating that callers must wrap the call in a timeout mechanism per FR-007, or implement timeout internally.

2. **P1-2**: Clarify the distance normalization. Either implement true max-distance normalization per the spec or update the spec to say "clamped to [0.0, 1.0]" rather than "normalized by maximum possible distance."

### P2 (Should Fix)

3. **P2-1**: Document the cooperative heuristic limitation. Add a docstring note to `_build_cooperative_matrix` explaining that the heuristic path applies a uniform dispute penalty rather than per-pair, and that the agreement matrix path should be preferred when available.

4. **P2-2**: Document the red-blue aggregation trade-off. Note in `_build_rb_matrix` that per-agent severity information is lost during aggregation.

### P3 (Consider)

5. **P3-1**: The `build_payoff_matrix()` return type is `list[list[float]]` for numpy-free testability. This is a good design decision. Consider adding a `to_numpy()` convenience method if numpy is available, to avoid the conversion at the call site.
