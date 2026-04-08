# Phase 1 Review: game-theorist

**Spec**: 017-equilibrium-scorer
**Reviewer**: game-theorist
**Date**: 2026-03-24
**Phase**: 1 (Initial Review)

---

## Scope

Evaluate the mathematical soundness of payoff functions per mode, correctness of the equilibrium check, and reasonableness of the heuristic fallback.

---

## Payoff Function Analysis

### Cooperative Mode (Section 2.1 / `cooperative_payoff`)

The spec defines `J_i = recommendations_accepted_in_synthesis`. The implementation maps this to `surviving_count`, which is a reasonable proxy for "recommendations that survived to synthesis."

The best-response heuristic uses `max(surviving_count)` across all agents. This is a defensible simplification: in a cooperative game, the best response is to have as many recommendations accepted as the top performer. However, this conflates two things: (1) the agent's actual payoff and (2) what the agent could have achieved by deviating. In a true Nash check, best response means "given others' strategies fixed, what payoff could I achieve by changing MY strategy?" Using max surviving count as the upper bound assumes that an agent's ceiling is determined by the best performer, which is only correct if the synthesis process is symmetric.

**Assessment**: Mathematically reasonable as a heuristic. The key assumption -- that any agent could in principle achieve the max surviving count -- is a simplification but not unreasonable for a first-order approximation.

### Winner-Take-All Mode (Section 2.2 / `winner_take_all_payoff`)

Binary payoff `J_i = 1 if winner, 0 otherwise` is correctly implemented. The winner is always at equilibrium (payoff=1, best_response=1).

The loser equilibrium check uses a threshold on `score_differential`: if differential > 2.0, the loser "couldn't have won" and is at equilibrium (best_response=0); if differential <= 2.0, the loser "might have won" (best_response=1, not at equilibrium).

**Concern**: The threshold of 2.0 is arbitrary and undocumented. There is no justification for why 2.0 is the cutoff. In game theory, a Nash equilibrium check should be based on whether a unilateral deviation could improve the agent's payoff, not an arbitrary score gap. The score differential is a post-hoc metric that does not directly measure deviation potential.

**Assessment**: The structure is correct (winner at equilibrium, losers conditionally), but the threshold is a magic number that should be configurable or derived from the scoring system.

### Prisoners-Dilemma Mode (Section 2.3 / `prisoners_dilemma_payoff`)

`J_i = territory_held - gamma * overreach_penalty` is correctly implemented with:
- `territory = core_competency + unique_capability + shared_territory - deferral`
- `overreach_penalty = max(0, overreach_count - overreach_rebutted)`

The best-response estimate removes deferrals and overreach penalty: `best_territory = core_competency + unique_capability + shared_territory`. This models the ideal case where the agent claims all territory without overreaching.

**Concern**: The best-response estimate does not account for the strategic interaction. In a true PD, the best response depends on what the other agent does. If agent B cooperates, agent A's best response is to defect (claim more territory). The heuristic ignores this strategic dimension and treats the best response as a solo optimization.

**Assessment**: Adequate for a heuristic scorer. The payoff function correctly captures the PD structure (cooperation vs. overreach). The best-response is a reasonable upper bound.

### Red-Blue Mode (Section 2.4 / `red_blue_payoff`)

Red: `J_red = severity_sum * (landed_attacks / total_surface)`
Blue: `J_blue = red_severity * (mitigated_attacks / total_surface)`

This is a well-structured adversarial payoff. Red benefits from confirmed attacks, Blue from mitigations.

**Concern**: The best-response for Red is `severity_sum` (all attacks land), and for Blue is `red_severity` (all attacks mitigated). These are correct upper bounds but represent ideal scenarios that are mutually exclusive. In a zero-sum-like game, if Red achieves best response, Blue cannot, and vice versa. The equilibrium score will typically reflect this tension.

**Assessment**: Sound. The adversarial structure is correctly modeled.

---

## Equilibrium Check Logic

The equilibrium determination (`at_eq = payoff >= best_response - 1e-9`) is a standard epsilon-tolerance comparison. The tolerance of 1e-9 is appropriate for floating-point arithmetic.

The aggregate score `agents_at_equilibrium / total_agents` correctly produces a ratio in [0.0, 1.0] as required by FR-006.

The code correctly handles edge cases: zero agents produces score 0.0, payoff computation failures are logged and treated as not-at-equilibrium.

---

## Heuristic Fallback

The `_NASHOPT_AVAILABLE` flag gates between `nashopt.check_equilibrium()` and the heuristic path. However, I observe that the code NEVER actually calls `nashopt.check_equilibrium()` -- even when `_NASHOPT_AVAILABLE` is True, the `_compute_equilibrium_score` function always uses the heuristic payoff functions. The `_NASHOPT_AVAILABLE` flag only affects the `solver` field in the output (`"nashopt"` vs `"heuristic"`).

**Issue**: The nashopt integration described in FR-005 ("The scorer MUST use nashopt's `check_equilibrium()`") is not implemented. The code imports nashopt to check availability but never delegates computation to it. The `solver` field in the output is misleading -- it reports "nashopt" when nashopt is installed, even though the heuristic is always used.

---

## Summary

| Area | Verdict |
|------|---------|
| Cooperative payoff | Sound heuristic, reasonable proxy |
| WTA payoff | Correct structure, magic threshold (2.0) |
| PD payoff | Adequate, ignores strategic interaction |
| Red-Blue payoff | Sound adversarial model |
| Equilibrium check | Correct epsilon comparison |
| Heuristic fallback | **Misleading**: nashopt never actually called |
| Edge cases | Well handled |

### Key Issues

1. **nashopt integration gap**: FR-005 requires `check_equilibrium()` usage but the code never calls it.
2. **Magic threshold in WTA**: The 2.0 score differential cutoff is arbitrary and undocumented.
3. **PD best-response oversimplification**: Ignores strategic interaction (acceptable for v1 but should be noted).
