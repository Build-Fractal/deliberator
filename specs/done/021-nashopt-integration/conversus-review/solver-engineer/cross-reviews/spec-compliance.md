# Cross-Review of spec-compliance's Review

**Cross-reviewer**: solver-engineer
**Reviewing**: spec-compliance's review of Spec 021 (nashopt integration)
**Date**: 2026-04-01

---

## Dangerous Contradictions

### DC-1: FR-003 alignment verdict obscures fatal matrix shape problems

spec-compliance marks FR-003 as **MET**, stating "Each follows the matrix structure documented in the spec's Section 2 table." My review identified that the winner-take-all builder produces an N x 1 vector while the nashopt API signature at `spec.md:30` expects `np.ndarray (N x N x actions)`, and the red-blue builder produces a fixed 2 x K matrix that drops individual agent identity when N > 2 agents exist. Calling FR-003 "MET" gives implementers a green light to ship code that will produce runtime errors or meaningless solver output when nashopt actually processes these matrices. The spec table says "N x 1 ranking payoff vector" for WTA, but the spec also defines `payoff_matrix` as `np.ndarray (N x N x actions)` in the API signature. spec-compliance should have flagged this internal spec contradiction rather than treating the table as authoritative and ignoring the API shape requirement.

### DC-2: ThreadPoolExecutor timeout assessed as functional when it can block indefinitely

spec-compliance marks FR-007 as **MET** and notes only that the test "uses `side_effect` rather than exercising the actual timeout path" (Missed Opportunity #1). My review identified a more severe problem: the `with ThreadPoolExecutor(...)` context manager calls `shutdown(wait=True)` on exit, which means the calling thread will block until the timed-out solver thread finishes. This negates the timeout entirely for long-running JAX computations. spec-compliance's assessment that the timeout mechanism works correctly -- with the test gap being merely a test fidelity issue -- is dangerous because the mechanism itself is broken at the implementation level, not just at the test level. The distinction matters: a test gap is P2, a broken timeout that blocks indefinitely is P1.

### DC-3: Strategy profile dimension mismatch completely absent from spec-compliance review

spec-compliance does not mention the mismatch between the fixed 4-element strategy vector produced by `build_strategy_profile` and the variable action-space dimensions of the per-mode payoff matrices. The nashopt API takes both `payoff_matrix` and `strategy_profile` as inputs; if their dimensions are incompatible, the solver call will fail at runtime. spec-compliance's review covers FR-003 (payoff matrices) and FR-004/FR-005 (solver result handling) but entirely skips the bridge between them -- the strategy profile that is the second mandatory input to `check_equilibrium()`. This is a P1 correctness issue that should have appeared as an alignment gap on FR-003 or FR-004, since neither requirement can be meaningfully "MET" if the solver call itself will crash on dimension mismatch.

---

## Tensions

### T-1: FR-005 severity assessment differs significantly

Both reviews identify that the fallback at `solver.py:436-438` (listing all agents as not at equilibrium when `agents_not_at_equilibrium` is absent) is a problem. However, spec-compliance frames it as a "completeness gap" and a P1 fix, while my review frames it as an architectural problem tied to the off-base assumption that nashopt returns an `agents_not_at_equilibrium` field not present in the spec's API surface. The tension: spec-compliance's P1 recommendation (#3) says "compare each agent's best response action against their current strategy," which is exactly my P1 recommendation (#5), but spec-compliance does not flag that this requires carrying the strategy profile through to post-processing -- a non-trivial refactor that interacts with the strategy dimension mismatch I identified. The fix is more involved than spec-compliance's framing suggests.

### T-2: Heuristic vs. solver score comparability not raised by spec-compliance

My review (Missed Opportunity #5) identifies that the heuristic computes score as `agents_at_eq / total_agents` (a discrete fraction) while the solver computes `1.0 - distance` (a continuous metric), making scores non-comparable across solver switches. spec-compliance does not raise this at all. This tension matters because spec-compliance marks SC-003 ("behavior identical to current heuristic") as **MET**, focusing on output format compatibility. But SC-003's intent is broader: if a consumer stores scores over time and the solver availability changes between runs, the score semantics change silently. Whether this is within SC-003's scope is debatable, but it is a real operational risk that spec-compliance's review should at least acknowledge.

### T-3: Payoff matrix normalization absent from spec-compliance's analysis

My review (Missed Opportunity #7) flags that raw payoff values vary by mode (cooperative counts in [0, 20], PD territory values in [-10, 15], red-blue severity sums in [0, 100+]) and that unnormalized inputs may produce scale-dependent distances from nashopt. The spec says distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form" but the implementation just clamps. spec-compliance does not mention normalization at all. This is a tension because spec-compliance's FR-004 verdict (**MET**) relies on the clamping at `solver.py:409` being sufficient, while my analysis questions whether clamping without prior normalization satisfies the spec's "normalized by the maximum possible distance" language.

### T-4: Per-agent payoff zeros assessed at different priority levels

Both reviews note that `_score_from_solver` hardcodes `payoff: 0.0` for all agents. spec-compliance lists it as P2 recommendation #5 ("document the gap or extract payoffs from the matrix"). My review lists it as P2 recommendation #7 with a concrete fix: compute each agent's actual payoff from the payoff matrix row at the current strategy profile. The tension is in the proposed remediation: spec-compliance suggests documentation as an acceptable fix, while my review argues for computation because the information loss undermines the value proposition of the exact solver path. If the solver path provides less per-agent detail than the heuristic, the upgrade is a partial regression in output richness.

### T-5: Agreement matrix symmetry risk not addressed by spec-compliance

spec-compliance's review does not mention the asymmetric agreement matrix lookup at `solver.py:128-133`, where `features.agreement_matrix.get(name_i, {}).get(name_j, 0)` will produce a non-symmetric payoff matrix if the source data only populates one triangle. My review identifies this as a P3 robustness concern. The tension is whether the test suite (which uses a fully populated matrix) provides sufficient coverage. spec-compliance's silence on this suggests implicit trust in the test data, while my position is that the code should defensively symmetrize or validate the input.

---

## Safe Agreements

### SA-1: SC-001 and SC-002 lack threshold tests and must be added before ship

Both reviews independently identify that SC-001 (cooperative convergence score >= 0.9) and SC-002 (3+ disputes score < 0.5) have no corresponding tests. spec-compliance calls this out explicitly as "NOT MET" for both success criteria, and my review does not have dedicated SC testing but implicitly requires it through the score comparability concerns. Both reviews agree this is a P1 gap. The absence of threshold tests means the spec's two primary acceptance criteria are unverified.

### SA-2: The `agents_not_at_equilibrium` attribute assumption is off-base

Both reviews identify that the code at `solver.py:429` checks for `hasattr(result, "agents_not_at_equilibrium")`, but the spec's API surface at `spec.md:29-35` only documents `is_equilibrium`, `distance`, and `best_responses`. spec-compliance lists this as Off-Base Assumption #1; my review lists it as Off-Base Assumption #1. Both agree the `hasattr` guard prevents a crash but the fallback (all agents not at equilibrium) is overly pessimistic, and that per-agent deviation should instead be derived from `best_responses`.

### SA-3: ThreadPoolExecutor timeout does not cancel the solver thread

Both reviews agree that `future.result(timeout=...)` raises `TimeoutError` in the caller but does not stop the worker thread. spec-compliance frames this as a P3 "nice to have" (recommendation #7: "consider using `Future.cancel()` or a threading event"). My review frames it more urgently due to the `shutdown(wait=True)` blocking issue, but we agree on the fundamental mechanism: timed-out JAX solver threads will continue consuming resources. The disagreement is on severity, not on the technical finding.

---
