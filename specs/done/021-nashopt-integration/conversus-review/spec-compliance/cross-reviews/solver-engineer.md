# Cross-Review of solver-engineer's Review

**Cross-reviewer**: spec-compliance
**Reviewing**: solver-engineer
**Spec**: 021-nashopt-integration
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1: Winner-take-all matrix shape is not a spec violation — the spec prescribes N x 1

solver-engineer flags the WTA builder returning an N x 1 array as a correctness bug (Missed Opportunity #1) and recommends P1 reformulation into an N x N matrix. However, the spec's own Section 2 table explicitly defines winner-take-all as "N x 1 ranking payoff vector." The implementation matches the spec literally. The real question is whether the spec's prescribed shape is compatible with nashopt's expected input signature (`np.ndarray (N x N x actions)` per spec Section 2 API surface). This is a spec-level inconsistency, not an implementation bug. solver-engineer's P1 recommendation to reformulate as N x N would fix the nashopt API mismatch but would violate the spec as written. The correct action is to flag the spec inconsistency for resolution, not to unilaterally change the matrix shape. Treating a spec-compliant implementation as a P1 code defect misdirects engineering effort and risks introducing a matrix shape the spec did not authorize.

### DC-2: "No normalization" finding overlooks that the spec delegates normalization to nashopt

solver-engineer's Missed Opportunity #7 asserts that payoff matrices should be normalized before passing to nashopt, and the P2 recommendation (#6) says to divide by max absolute value. But the spec states distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form" — this describes nashopt's internal behavior, not a pre-processing step the caller must perform. The implementation's clamping at `solver.py:409` is a defensive post-processing step, not a substitute for normalization. If nashopt's distance metric is already scale-invariant by design (as the spec implies), then pre-normalizing payoff matrices would alter the game semantics — a cooperative game with surviving counts in [0, 20] is a different game from one rescaled to [0, 1]. solver-engineer's recommendation could actively harm correctness by destroying payoff magnitude information that nashopt may rely on.

### DC-3: Cooperative diagonal semantics finding mischaracterizes the design intent

solver-engineer's Missed Opportunity #4 claims that using `surviving_count` on the diagonal while using agreement data off-diagonal "mixes two different payoff semantics." From a spec-compliance perspective, the cooperative matrix's Section 2 definition is "Agreement matrix from features + dispute counts." The diagonal of an agreement matrix (agent i's agreement with itself) is semantically undefined — an agent always agrees with itself. Using `surviving_count` as the self-payoff (the agent's standalone value) is a reasonable game-theoretic construction: the diagonal represents what each agent achieves unilaterally, while off-diagonal entries represent bilateral cooperation gains. This is standard in cooperative game theory. Calling this "non-interpretable" contradicts established normal-form game construction patterns where diagonal and off-diagonal entries encode different strategic relationships.

---

## Tensions

### T-1: Severity of red-blue dimension mismatch

Both reviews identify the red-blue 2-player collapse as problematic. solver-engineer calls it a P1 correctness bug causing "indexing errors or silent misattribution" (Missed Opportunity #2). My review does not flag it explicitly because the spec prescribes "2 x K severity/mitigation matrix" — the implementation follows the spec. The tension: solver-engineer is correct that passing `agent_names` (length N) alongside a 2-row matrix will cause dimension mismatches in the best-response loop. But this is another spec-level inconsistency (spec says 2 x K, API expects N agents). The fix belongs in the spec, and the severity depends on whether nashopt can handle 2-player games with agent aliasing.

### T-2: ThreadPoolExecutor blocking on shutdown — scope of the problem

Both reviews flag the ThreadPoolExecutor timeout mechanism as problematic. solver-engineer's Off-Base Assumption #2 goes further, asserting that `shutdown(wait=True)` in the `with` block "negates the timeout" and is "a correctness issue masquerading as a robustness feature." My review (Off-Base Assumption #3) notes resource leakage but does not claim the timeout is negated. The tension: solver-engineer's analysis is technically accurate for the `with` statement's `__exit__`, but in practice `scorer.py` calls `_try_solver` which returns `None` on timeout, and the executor's shutdown happens asynchronously within `_try_solver`'s scope. The calling code in `scorer.py:288` proceeds to the heuristic path regardless. Whether the `with` block's `__exit__` actually blocks depends on whether `_try_solver` returns before `__exit__` runs (it does, because the timeout fires in the calling thread). solver-engineer's P1 recommendation to restructure is warranted but the characterization of "negating the timeout" overstates the runtime impact.

### T-3: Strategy profile dimension mismatch — implementation bug vs. spec gap

solver-engineer flags strategy profile dimensions not matching action space (Missed Opportunity #3, P1 recommendation #3). My review does not raise this. The tension: the spec does not define strategy profile construction at all — it only shows `strategy_profile` as an input to `check_equilibrium()`. The 4-element fallback vector is an implementation decision not governed by the spec. solver-engineer is right that mismatched dimensions will cause runtime errors, but whether this is a P1 "must fix before merge" or a spec amendment depends on whether the spec should have defined strategy profile construction. From spec-compliance perspective, the implementation has freedom here, and the fix is straightforward (align dimensions), but it should not be conflated with a spec violation.

### T-4: Heuristic vs. solver score comparability

Both reviews identify that heuristic scores (discrete fraction) and solver scores (continuous distance) measure different things. solver-engineer frames this as Missed Opportunity #5 and recommends a reconciliation mechanism (P2 #8). My review flags the `payoff: 0.0` information loss (Missed Opportunity #5) but does not explicitly call out score incomparability. The tension is about priority: solver-engineer's framing suggests the two paths should produce comparable scores, but the spec explicitly says behavior is "identical to the current heuristic" only when nashopt is absent (SC-003). The spec does not require score comparability across paths — it requires the same output format. Score discontinuity on timeout fallback is a UX concern, not a spec violation.

### T-5: Missing SC-001/SC-002 tests — who owns the gap

My review flags the absence of SC-001 and SC-002 threshold tests as a P1 issue. solver-engineer does not mention success criteria testing at all, focusing entirely on numerical correctness of the solver internals. The tension: solver-engineer's review thoroughly analyzes matrix construction and API interaction but never asks whether the end-to-end system meets the spec's acceptance thresholds. From a spec-compliance standpoint, unverified success criteria are the highest-priority gap because they represent the spec author's definition of "done." solver-engineer's P1 items (matrix shapes, dimension mismatches) are important but secondary to demonstrating that the system actually produces the scores the spec demands.

---

## Safe Agreements

### SA-1: FR-005 best-response fallback is too coarse

Both reviews agree that the fallback at `solver.py:438` (listing all agents as not-at-equilibrium when `agents_not_at_equilibrium` is absent) is a lossy heuristic. solver-engineer's Off-Base Assumption #1 and P1 #5 recommend deriving per-agent deviation from `best_responses`. My review's Missed Opportunity #3 and P1 #3 make the identical recommendation. Both reviews also agree that the nashopt API (per the spec) does not include `agents_not_at_equilibrium` as a return field, making the `hasattr` guard dead code in practice. The fix is clear: compare each agent's current strategy against their best response from the nashopt result.

### SA-2: Per-agent payoff data is zeroed in the solver path

solver-engineer's Missed Opportunity #6 and my Missed Opportunity #5 both identify that `_score_from_solver` hardcodes `payoff: 0.0` for all agents. Both reviews agree this creates an information asymmetry between the solver and heuristic paths that undermines downstream consumers. solver-engineer recommends extracting per-agent payoffs from the payoff matrix (P2 #7); my review recommends either extracting payoffs or documenting the gap (P2 #5). The core finding is identical.

### SA-3: nashopt API key types are ambiguous

solver-engineer's Off-Base Assumption #4 and my Off-Base Assumption #2 both flag the dual int/string lookup for `best_responses` keys at `solver.py:417-419`. Both reviews note the spec says `dict[agent, action]` without clarifying agent type. Both recommend pinning down the key type. The defensive dual-lookup is functional but signals an unresolved API contract question that should be settled before the code matures.

---

## Summary

solver-engineer's review is technically rigorous on numerical correctness and API contract analysis. Its strongest contributions are the red-blue dimension mismatch (T-1), strategy profile dimension concern (T-3), and ThreadPoolExecutor shutdown analysis (T-2). The primary risk is that three of its Missed Opportunities (#1 WTA shape, #4 cooperative diagonal, #7 normalization) treat spec-compliant behavior as implementation bugs, which could lead to changes that violate the spec. Recommendations from solver-engineer should be filtered through the spec's explicit prescriptions before acting on them — several require spec amendments rather than code fixes.
