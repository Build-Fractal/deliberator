# Cross-Review of solver-engineer's Review

**Cross-reviewer**: plugin-engineer
**Reviewing**: solver-engineer's review of Spec 021: nashopt Integration
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1: Winner-take-all matrix shape -- catastrophic failure vs. spec-sanctioned design

Solver-engineer flags the N x 1 WTA matrix as "not a proper payoff matrix" that nashopt will "almost certainly reject" (Missed Opportunity 1), and elevates it to P1 requiring reformulation as N x N. However, the spec explicitly defines the WTA structure as "N x 1 ranking payoff vector" in the Section 2 matrix table. Solver-engineer's own Alignment section acknowledges this: "The winner-take-all builder returns N x 1 as specified." These two positions directly contradict each other -- one says the shape matches the spec, the other says it must be reformulated as N x N. The real question is whether the spec itself is wrong about the nashopt API's shape requirements (`N x N x actions` per `spec.md:30`), but solver-engineer conflates "implementation doesn't match spec" with "implementation doesn't match nashopt" without cleanly distinguishing which is broken. If the spec's API signature is authoritative, the spec has an internal inconsistency (N x 1 in the matrix table vs. `N x N x actions` in the API signature), and the fix belongs in the spec, not just the code. If implemented as N x N per solver-engineer's recommendation without a spec amendment, the code would violate its own spec.

### DC-2: Red-blue dimensionality -- index error vs. semantic design choice

Solver-engineer's Missed Opportunity 2 claims the 2-row red-blue matrix will cause "indexing errors or silent misattribution" when iterating over N agents with a 2-row matrix. This is a legitimate structural concern, but the recommendation (P1-2) proposes either mapping the 2-player result back to individuals by role or building an N x N matrix. Both options fundamentally change the game-theoretic semantics of the red-blue mode. The spec defines red-blue as a "2 x K severity/mitigation matrix" -- it is intentionally a 2-player game (red team vs. blue team), not an N-player game. My review did not flag this as a correctness bug because the 2-player reduction is the intended game formulation. The actual bug is narrower than solver-engineer states: it is specifically in the post-processing loop at `solver.py:416-424` that maps 2-player results back to N agents, not in the matrix construction itself. Solver-engineer's recommendation to rebuild the matrix as N x N would destroy the red-blue game semantics that the spec explicitly requires. The safe fix is to fix the mapping, not the matrix.

### DC-3: ThreadPoolExecutor timeout -- "correctness issue" severity vs. practical risk

Solver-engineer's Off-Base Assumption 2 claims the `with ThreadPoolExecutor(...)` pattern negates the timeout entirely because `__exit__` calls `shutdown(wait=True)`. This is technically accurate regarding the `__exit__` behavior, but the severity is overstated. The P1-4 recommendation to replace with `multiprocessing` or `signal.alarm` is a significant architectural change. My review flagged the timeout test as not exercising the real mechanism (P1-2) but did not escalate the executor pattern itself to P1 because in practice the timeout still surfaces the `TimeoutError` to the calling code path, the heuristic fallback still runs, and the `PluginResult` is still returned correctly. The user-facing behavior is correct; the resource leak from orphaned threads is a P2 operational concern, not a P1 correctness blocker. Solver-engineer's framing as "a correctness issue masquerading as a robustness feature" conflates user-visible correctness (which is maintained) with resource management (which is degraded). Recommending `multiprocessing` or `signal.alarm` introduces its own set of problems (pickling constraints for multiprocessing, Unix-only for signal.alarm) that solver-engineer does not acknowledge.

---

## Tensions

### T-1: Payoff matrix normalization -- required or optional?

Solver-engineer's Missed Opportunity 7 and P2-6 recommend normalizing all payoff matrices to [0, 1] before passing to nashopt, arguing that scale-dependent distances make scores non-comparable across modes. My review's P3-3 flagged a narrower version of this (red-blue branch inconsistency only). The tension: normalization changes the game's strategic structure. Dividing all payoffs by max absolute value preserves ordinal rankings but changes mixed-strategy equilibria. If nashopt's distance metric is already scale-invariant (which solver-engineer acknowledges as conditional -- "if nashopt's distance metric is scale-dependent"), normalization is unnecessary and potentially harmful. The spec says distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form" (`spec.md:53`), which implies nashopt handles normalization internally. Solver-engineer's recommendation may duplicate or conflict with nashopt's own normalization.

### T-2: Score reconciliation mechanism -- valuable or overengineered?

Solver-engineer's P2-8 recommends running both solver and heuristic paths simultaneously and logging a comparison for ongoing calibration. My review did not propose this. While the idea has diagnostic value, it doubles computation cost for every scoring call, and the two scores are fundamentally incommensurable (as solver-engineer's own Missed Opportunity 5 explains -- one is a discrete fraction, the other a continuous distance). Comparing them produces a number, but it is unclear what threshold or divergence pattern would actually be actionable. The tension is between solver-engineer's desire for runtime validation and the practical cost and interpretability of the comparison.

### T-3: Per-agent payoff data from solver path -- zero values vs. computed values

Both reviews flag that `_score_from_solver` hardcodes `payoff: 0.0` and `best_response_payoff: 0.0` (my Missed Opportunity 4, solver-engineer's Missed Opportunity 6). However, we differ on severity. Solver-engineer escalates this to P2 and states it "undermines the value of the exact solver." My review also placed it at P2 but framed it as an output parity issue. The tension: computing per-agent payoffs from the solver path requires evaluating each agent's row in the payoff matrix at the current strategy profile, which means carrying the strategy profile through to post-processing. Solver-engineer's P1-5 (deriving per-agent equilibrium deviation from best_responses) is a prerequisite for this. The two recommendations are coupled but presented independently, and implementing P2-7 without P1-5 is impossible. This ordering dependency is not acknowledged.

### T-4: Agreement matrix symmetry -- defensive fix vs. data contract enforcement

Solver-engineer's P3-9 recommends symmetrizing the agreement matrix with `max(matrix[i][j], matrix[j][i])`. My review flagged the same diagonal semantics issue (P3-2) but did not address symmetry. The tension: symmetrizing with `max` is a silent data repair that masks upstream bugs. If the agreement matrix is supposed to be symmetric (which is a property of the feature extraction in spec 015), the correct fix is to validate symmetry and raise an error if violated, not silently repair it. Solver-engineer's `max` approach could hide a bug in feature extraction where one direction is systematically missing.

### T-5: Integration test strategy -- mock purity vs. real-library validation

Both reviews recommend adding integration tests with real nashopt (my P2-2, solver-engineer's P3-10). But solver-engineer goes further and proposes testing with a known-equilibrium game (e.g., Prisoners' Dilemma with specific payoff values), while my recommendation focuses on validating the API contract (argument shapes, return types). These are complementary but have different failure modes: solver-engineer's approach validates numerical correctness end-to-end but is fragile to nashopt version changes in equilibrium computation; my approach validates the interface contract but not the math. The tension is which risk to prioritize given that nashopt is an external dependency with its own release cycle.

---

## Safe Agreements

### SA-1: Missing `solver` key on error paths is a spec violation

Solver-engineer's Alignment table marks FR-008 as fully passing, while my review identifies two error-path returns that omit the `solver` key (P1-1). Despite this difference in the Alignment section, solver-engineer's broader review does not dispute that error paths should include provenance. The underlying principle is agreed: every `PluginResult` must include the `solver` key per FR-008. The disagreement is only on whether the current implementation satisfies this -- a factual question resolvable by code inspection.

### SA-2: Timeout test does not exercise the real timeout mechanism

Both reviews independently identify that the timeout test patches the solver function to raise `TimeoutError` directly rather than letting the `ThreadPoolExecutor` timeout naturally (my P1-2, solver-engineer's Off-Base Assumption 2 discussion). Both agree the test passes for the wrong reason. Both recommend a test where the mock blocks (e.g., `time.sleep`) and the timeout is set short. This is a clean agreement on both the diagnosis and the fix.

### SA-3: Dead `total_surface` variable in `_build_rb_matrix`

Both reviews flag the unused `total_surface` computation in the `max_k == 0` branch (my P1-3, solver-engineer's Missed Opportunity 8). Both agree it is dead code from incomplete refactoring. My review escalates it to P1 (because dead code in a numerical path is a maintenance hazard), while solver-engineer places it lower. Regardless of priority, the fix is agreed: remove the dead variable or use it for normalization.

### SA-4: Cooperative diagonal semantics are inconsistent when agreement matrix is present

Both reviews flag that `_build_cooperative_matrix` uses `surviving_count` for diagonal entries even when `agreement_matrix` is provided and may contain self-pair data (my Off-Base Assumption 2 / P3-2, solver-engineer's Missed Opportunity 4). Both agree this mixes two payoff semantics. The fix direction differs slightly (solver-engineer says use agreement data when available; I say add a clarifying comment or use agreement data), but the diagnosis is shared.
