# Spec Compliance — Revised Position

**Reviewer**: spec-compliance
**Date**: 2026-04-01
**Phase**: Cooperative Revision (Phase 3)

---

## Recommendation Dispositions

### Original P1-1: Add SC-001 test (cooperative convergence score >= 0.9)
**KEPT — P1.** Both cross-reviewers either agree or defer to this finding. plugin-engineer explicitly adopts it (DC-3: "Adopting spec-compliance's P1 recommendation for threshold tests"). solver-engineer does not mention success criteria testing, which plugin-engineer and I both identify as a scope gap in the solver-engineer review. The spec's primary acceptance criteria remain unverified. No revision needed.

### Original P1-2: Add SC-002 test (3+ disputes score < 0.5)
**KEPT — P1.** Same rationale as P1-1. Both threshold tests are the spec author's definition of "done" and cannot be deferred.

### Original P1-3: Improve FR-005 agent-not-at-equilibrium accuracy
**KEPT — P1, with expanded scope.** All three reviews converge on this fix (solver-engineer SA-1, plugin-engineer DC-1). solver-engineer's cross-review (T-1) correctly notes that comparing best responses against current strategies requires carrying the strategy profile through to post-processing, making this a more involved refactor than I originally framed. I accept that nuance. The fix should: (a) remove the dead `hasattr(result, "agents_not_at_equilibrium")` guard, (b) derive per-agent deviation by comparing each agent's current strategy against their `best_responses` entry, and (c) thread the strategy profile into the post-processing step. This remains P1 because the spec uses MUST language on best-response reporting.

### Original P2-4: Add a real-timeout integration test
**UPGRADED to P1.** Both cross-reviewers convinced me. plugin-engineer's DC-2 argument is decisive: the mock raises `TimeoutError` inside the submitted callable, but the real code path catches it from `future.result(timeout=)`. These are different exception propagation paths. A test that does not exercise the actual code path creates false confidence. solver-engineer's DC-2 goes further, noting that `ThreadPoolExecutor.__exit__` calls `shutdown(wait=True)`, which may block the calling thread. Whether or not the blocking characterization is fully accurate at runtime (see my cross-review T-2 of solver-engineer), the combination of an untested timeout mechanism and a potentially blocking shutdown pattern is too risky for ship. The fix: write a test that patches `check_equilibrium_nashopt` with a `time.sleep(5)` callable, sets timeout to 0.01s, and verifies `_try_solver` returns `None` and the scorer produces a heuristic result.

### Original P2-5: Document per-agent payoff gap in solver path
**KEPT — P2, reframed.** All three reviews flag the `payoff: 0.0` hardcoding. plugin-engineer's consumer-facing framing is more actionable than my original documentation framing. solver-engineer recommends computing actual payoffs from the payoff matrix. I now agree that documentation alone is insufficient -- the solver path should compute per-agent payoffs from the payoff matrix row at the current strategy profile, matching the heuristic path's data richness. If that is not feasible in this iteration, the minimum is a sentinel value (e.g., `null`) rather than a misleading `0.0`, plus a `"payoff_source": "unavailable"` annotation so consumers can distinguish "zero payoff" from "payoff not computed."

### Original P2-6: Align solver.py with spec API surface (int/str key lookup)
**KEPT — P2.** All three reviews agree the dual int/str lookup for `best_responses` keys is a sign of an unresolved API contract question (solver-engineer SA-3, my OBA-2). No cross-reviewer disputes this. The spec should clarify agent key types, and the code should use a single explicit mapping.

### Original P3-7: Add cancellation for timed-out solver threads
**UPGRADED to P2.** solver-engineer's DC-2 cross-review presents the strongest argument: `shutdown(wait=True)` in the `with` block's `__exit__` may block the calling thread until the solver thread completes, and for JAX workloads this could be significant. Even if the runtime impact is debatable (my cross-review of solver-engineer T-2 argues the timeout fires in the calling thread first), the combination of resource leakage and potential blocking is a production risk. The fix should use `executor.shutdown(wait=False, cancel_futures=True)` (Python 3.9+) or restructure the executor lifecycle to avoid the `with` block's implicit shutdown. Not P1 because the heuristic fallback does fire correctly from the caller's perspective, but P2 because the background resource consumption is a real operational concern for JAX/GPU deployments.

### Original P3-8: Parametrize mode-specific matrix tests
**KEPT — P3.** No cross-reviewer comments on this. It remains a test hygiene improvement with no compliance implications.

### Original P3-9: Add test for unknown mode error message
**KEPT — P3.** No cross-reviewer comments. Unchanged.

### Original P3-10: Verify SolverResult.score rounding consistency
**KEPT — P3.** No cross-reviewer comments. Unchanged.

---

## New Recommendations

### NEW-1 (P1): Add `"solver"` key to error-path PluginResult returns
**Source**: plugin-engineer's P1-1, accepted via my cross-review DC-1.

FR-008 uses MUST language: the `solver` key must always be present so consumers know which path ran. Two error-path returns in `EquilibriumScorer.execute()` (unknown-mode at lines 371-378, computation-failure at lines 394-401) produce `PluginResult` with `data={"error": ...}` and no `solver` key. Consumers that unconditionally access `result.data["solver"]` will crash with `KeyError`. Fix: add `"solver": "error"` to both error-path data dicts. I am upgrading my FR-008 verdict from MET to PARTIALLY MET.

### NEW-2 (P2): Remove dead `total_surface` variable and normalize red-blue fallback branch
**Source**: plugin-engineer's P1-3 and P3-3, corroborated by solver-engineer's MO-8.

The dead `total_surface` variable in `_build_rb_matrix` (lines 255-259) was likely intended to normalize the `max_k == 0` fallback branch. The `max_k > 0` branch returns severity-weighted ratios while the `max_k == 0` branch returns raw counts, creating a scale inconsistency that affects equilibrium computation depending on whether severity vectors are present. This is more than dead code cleanup -- it is a potential correctness issue for the solver. Fix: either apply consistent normalization across both branches, or remove `total_surface` and document why raw counts are acceptable in the no-severity case. Filing as P2 (escalated from plugin-engineer's mixed P1/P3) because the scale inconsistency affects solver output quality but does not violate a specific spec requirement.

### NEW-3 (P2): Validate payoff matrix shape before nashopt call
**Source**: solver-engineer's MO-1/MO-2 (matrix shape concerns), plugin-engineer's P3-1.

solver-engineer identifies that the WTA builder produces N x 1 and the red-blue builder produces 2 x K, while nashopt's API signature expects `np.ndarray (N x N x actions)`. My cross-review of solver-engineer (DC-1, DC-2) argued these are spec-level inconsistencies, not implementation bugs, since the builders follow the spec's Section 2 table. I maintain that position -- the implementation is spec-compliant as written. However, plugin-engineer's P3-1 makes a practical point: if nashopt receives an incompatible shape, the error will be opaque (deep inside JAX). A pre-call shape assertion that validates the matrix dimensions against nashopt's expected input would surface the error early with a clear message, regardless of whether the shape mismatch is a spec bug or an implementation bug. This is a defensive measure, not a spec compliance issue. Filing as P2 rather than the original absence from my review.

---

## Position Summary

After reading the cross-reviews, my original assessment holds on the core findings but shifts in three material ways:

**Verdicts revised:**
- FR-008: MET downgraded to PARTIALLY MET (accepting plugin-engineer's error-path finding).
- FR-005: PARTIALLY MET remains, but the fix is acknowledged as more involved than originally framed (accepting solver-engineer's note about strategy profile threading).

**Priorities revised:**
- Real-timeout test: P2 upgraded to P1. The mock tests a fundamentally different exception propagation path than the production code.
- Thread cancellation: P3 upgraded to P2. The `shutdown(wait=True)` blocking risk under JAX workloads is a real operational concern.

**New items added:**
- P1: `solver` key on error-path returns (from plugin-engineer).
- P2: Dead `total_surface` variable and red-blue scale inconsistency (from plugin-engineer, corroborated by solver-engineer).
- P2: Pre-call shape validation for payoff matrices (synthesized from solver-engineer's shape concerns and plugin-engineer's defensive validation recommendation).

**Items I declined to adopt:**
- solver-engineer's recommendation to reformulate the WTA matrix as N x N. The spec prescribes "N x 1 ranking payoff vector." The implementation follows the spec. If the shape is incompatible with nashopt's API, this is a spec amendment, not a code fix. The new shape validation (NEW-3) will surface the problem at runtime with a clear error.
- solver-engineer's recommendation to pre-normalize payoff matrices. The spec says distance is "normalized by the maximum possible distance for the game form," which describes nashopt's internal behavior. Pre-normalizing would alter game semantics.
- solver-engineer's characterization that the ThreadPoolExecutor timeout is "negated" by `shutdown(wait=True)`. The timeout fires in the calling thread and `_try_solver` returns `None` before `__exit__` runs. The blocking risk is real but the timeout itself is not negated. I adopted the operational concern (upgraded to P2) without adopting the "correctness issue masquerading as robustness" framing.

**Final P1 list (5 items):**
1. SC-001 threshold test (original P1-1)
2. SC-002 threshold test (original P1-2)
3. FR-005 per-agent equilibrium accuracy from `best_responses` (original P1-3, expanded)
4. Real-timeout integration test (upgraded from P2-4)
5. `solver` key on error-path returns (NEW-1, from plugin-engineer)

**Final P2 list (5 items):**
1. Per-agent payoff computation in solver path (original P2-5, reframed)
2. Clarify `best_responses` key types (original P2-6)
3. Thread cancellation / executor lifecycle (upgraded from P3-7)
4. Red-blue `total_surface` dead variable and scale normalization (NEW-2)
5. Pre-call payoff matrix shape validation (NEW-3)

**Final P3 list (3 items):**
1. Parametrize mode-specific matrix tests (original P3-8)
2. Unknown mode error message test (original P3-9)
3. SolverResult rounding consistency (original P3-10)
