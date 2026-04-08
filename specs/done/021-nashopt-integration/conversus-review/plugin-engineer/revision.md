# Plugin Engineer Revision — Spec 021: nashopt Solver Integration

**Reviewer**: plugin-engineer
**Date**: 2026-04-01
**Phase**: Cooperative Revision (Phase 3)

---

## Recommendation Dispositions

### P1-1: `PluginResult.data["solver"]` missing on error paths — REVISED

**Original**: Add `"solver": "unavailable"` or `"solver": "error"` to both error-path data dicts.

**Revision**: Adopting solver-engineer's refinement (DC-1). A third sentinel value silently changes the consumer contract from a binary enum to a ternary one. Consumers that branch on `if data["solver"] == "nashopt"` would silently skip error cases. The correct fix is to include `"solver": "heuristic"` on error paths, since no solver ran and the consumer should treat the result identically to a heuristic fallback. This keeps the enum binary and spec-compliant.

**Status**: RETAINED as P1, fix approach changed.

### P1-2: Timeout test does not exercise real mechanism — REVISED

**Original**: Patch `check_equilibrium_nashopt` to `time.sleep(5)` with a 0.01s timeout.

**Revision**: Adopting solver-engineer's complementary finding (DC-2). The timeout test and the timeout mechanism are two separate problems. solver-engineer correctly identifies that `ThreadPoolExecutor.__exit__` calls `shutdown(wait=True)`, meaning the `with` block will block until the timed-out thread finishes even after `future.result(timeout=)` raises. However, I maintain that solver-engineer's proposed replacement with `multiprocessing` or `signal.alarm` overstates the required fix at P1 severity. The user-facing behavior is correct: `TimeoutError` is raised, the heuristic fallback runs, and `PluginResult` is returned. The blocked `__exit__` is a resource leak (thread holds until solver completes), not a correctness bug. The fix should be two-tiered:

1. **P1** (test fix): Rewrite the timeout test with a blocking mock and a short timeout, so the test exercises the real `future.result(timeout=)` path. This will also expose the `__exit__` blocking behavior, documenting it as a known limitation.
2. **P2** (mechanism fix): Replace `with ThreadPoolExecutor(...)` with explicit `executor = ThreadPoolExecutor(...)` plus `executor.shutdown(wait=False, cancel_futures=True)` in the timeout branch. This releases the thread pool without blocking. `multiprocessing` and `signal.alarm` introduce their own complexity (pickling constraints, Unix-only) and are not warranted unless JAX GPU resource leakage is demonstrated.

**Status**: RETAINED as P1 for the test fix. Mechanism fix added as new P2 (see below).

### P1-3: Dead `total_surface` variable in `_build_rb_matrix` — DOWNGRADED to P2

**Original**: Remove dead variable or use it to normalize payoffs.

**Revision**: Both cross-reviewers challenge the P1 classification. solver-engineer (DC-3) argues that the matrix shape bugs (WTA N x 1, red-blue 2-row) are the real P1 issues and my dead variable is at most P3. spec-compliance (DC-3) escalates the related P3-3 (scale inconsistency between branches) to P2 but does not dispute the dead variable itself. On reflection, a dead variable alone is not a must-fix-before-ship item. However, the dead variable is a smoking gun for an incomplete normalization step -- the `max_k > 0` branch uses severity-weighted ratios while the `max_k == 0` branch returns raw counts. This scale inconsistency could affect nashopt's equilibrium computation. Combining the dead variable removal with the normalization fix (my original P3-3) into a single P2.

**Status**: DOWNGRADED to P2, merged with P3-3 into a unified normalization recommendation.

### P2-1: Add `solver` field to heuristic per_agent data for output parity — RETAINED

**Original**: Populate real values from solver or document the zero-value contract.

**Revision**: solver-engineer (T-2) argues that documenting zeros "locks in an information deficit that makes the premium solver path less useful than the free heuristic." This is a stronger framing. The fix should attempt to compute real per-agent payoffs from the payoff matrix when solver results are available, with zero-value fallback only if the matrix is unavailable. However, as my cross-review of solver-engineer noted (T-3), this depends on solver-engineer's P1-5 (deriving per-agent equilibrium deviation from `best_responses`), so the two recommendations are coupled. The ordering dependency should be explicit: implement per-agent best-response deviation first, then per-agent payoff extraction.

**Status**: RETAINED as P2, with noted dependency on per-agent best-response derivation.

### P2-2: Add `pytest.importorskip` conditional integration test — RETAINED

**Original**: Test class guarded by skip-if-no-nashopt that validates mock contract matches real API.

**Revision**: solver-engineer (T-3) argues that a known-equilibrium game test (e.g., Prisoner's Dilemma) catches more bugs because it validates numerical correctness, not just API shape. Both are needed, but if only one is implemented, solver-engineer's approach is more valuable. Revised to recommend both in a single test class: (1) API shape validation (argument types, return types), and (2) known-equilibrium numerical validation (2x2 PD with analytically known Nash solution). Both guarded behind `pytest.importorskip("nashopt")`.

**Status**: RETAINED as P2, scope expanded to include known-equilibrium numerical test.

### P2-3: Add INFO-level log line when solver path is selected — RETAINED

No cross-reviewer challenged this. Straightforward observability improvement.

**Status**: RETAINED as P2, unchanged.

### P3-1: Validate payoff matrix shape before passing to nashopt — UPGRADED to P2

**Original**: Pre-call shape assertion (matrix shape vs. strategy profile length).

**Revision**: solver-engineer's DC-3 and T-4 make a compelling case that matrix shape validity is the most critical gap my review missed. The winner-take-all builder produces N x 1 (spec-sanctioned but incompatible with nashopt's `N x N x actions` signature), and the red-blue builder produces 2 x K while post-processing iterates over N agents. My cross-review of solver-engineer (DC-1, DC-2) argued that both shapes are spec-sanctioned and the fix belongs in mapping/post-processing, not matrix construction. I still hold that position on the matrix construction itself -- the spec defines these shapes intentionally. But the absence of any shape validation before the nashopt call means an opaque JAX error is the only signal when shapes are incompatible. A shape-compatibility check at the solver boundary (between matrix construction and nashopt call) would surface the problem clearly. This is more important than I originally assessed.

**Status**: UPGRADED to P2, focused on solver-boundary validation rather than matrix reformulation.

### P3-2: Cooperative diagonal should consider agreement_matrix self-pair — UPGRADED to P2

**Original**: Add a comment explaining why, or use agreement data.

**Revision**: solver-engineer (T-1) frames this as a numerical correctness risk, not a documentation gap. spec-compliance's cross-review confirms the diagnosis. On reflection, mixing `surviving_count` for diagonal and `agreement_matrix` for off-diagonal produces a game where self-pair payoffs follow a different semantic than pair payoffs. This is not just undocumented -- it may produce a game whose equilibria have no meaningful interpretation. However, solver-engineer's cross-review (T-1 in their cross-review of me) suggests using `max` symmetrization to fix agreement matrix asymmetry. My cross-review of solver-engineer (T-4) argued that silent `max` repair masks upstream bugs. I maintain that the agreement matrix should be validated for symmetry (not silently repaired), and the diagonal should come from the agreement matrix when available, with `surviving_count` as fallback only when agreement data is absent.

**Status**: UPGRADED to P2. Use agreement_matrix self-pair when present, validate symmetry rather than silently repair.

### P3-3: Normalize red-blue fallback payoffs — MERGED into P1-3 revision (now P2)

See P1-3 disposition above. The scale inconsistency between `max_k == 0` (raw counts) and `max_k > 0` (severity-weighted ratios) is merged with the dead variable fix into a single P2 normalization recommendation.

**Status**: MERGED, covered by revised P1-3.

---

## New Recommendations

### N1 (P1): Add SC-001 and SC-002 threshold tests

Adopted from spec-compliance's finding (their P1-1, P1-2), which my original review missed entirely. The spec's primary acceptance criteria -- cooperative convergence scoring >= 0.9 (SC-001) and 3+ disputes scoring < 0.5 (SC-002) -- have no corresponding tests. These are the two most important spec guarantees and they are unverified. Tests should either: (a) mock nashopt to return a realistic low distance for SC-001 and a high distance for SC-002, or (b) exercise the heuristic path with feature sets that represent converged vs. disputed states and verify the thresholds hold. Both approaches validate that the scoring logic produces spec-compliant outputs for the defined scenarios.

### N2 (P2): Fix ThreadPoolExecutor shutdown semantics in timeout branch

Extracted from the P1-2 revision discussion above. The current `with ThreadPoolExecutor(...)` pattern calls `shutdown(wait=True)` on `__exit__`, blocking until the timed-out solver thread finishes. Replace with explicit executor lifecycle management: `executor = ThreadPoolExecutor(max_workers=1)`, submit the task, call `future.result(timeout=...)`, and in the timeout/exception handler call `executor.shutdown(wait=False, cancel_futures=True)` (Python 3.9+). This prevents the calling thread from blocking on a slow solver while still cleaning up correctly on the happy path. This is preferable to `multiprocessing` (pickling constraints) or `signal.alarm` (Unix-only, not thread-safe).

### N3 (P2): Fix post-processing mapping for non-NxN matrix modes

Adopted from solver-engineer's structural observation, scoped to the fix I argued for in my cross-review (DC-1, DC-2). The winner-take-all and red-blue modes produce non-NxN matrices (N x 1 and 2 x K respectively) as the spec requires. The issue is not the matrix shape but the post-processing code that maps solver results back to individual agents. The post-processing loop iterates over N agents using indices that assume the result maps 1:1 to agents, which breaks for 2-player red-blue results mapped onto N agents. The fix is in the result-mapping layer (`solver.py` post-processing), not in the matrix builders: (a) for red-blue, map the 2-player result back to individual agents by role assignment, (b) for winner-take-all, ensure the N x 1 result is interpreted as agent rankings, not as a matrix row. The matrix builders themselves should not be reformulated to N x N -- that would destroy the intended game-theoretic semantics the spec defines.

---

## Position Summary

After reading both cross-reviews and reconsidering my original findings, the revised position is:

**Severity recalibration was the primary correction needed.** solver-engineer correctly identified that my P1 priorities were inverted -- I elevated a dead variable (cosmetic) to P1 while missing structural issues in matrix shape mapping and success criteria testing. The dead variable is now P2 (merged with its normalization sibling), and the true P1 gaps are: (1) the missing `solver` key on error paths (retained), (2) the timeout test exercising the wrong code path (retained), and (3) the missing SC-001/SC-002 threshold tests (newly adopted from spec-compliance).

**Matrix shape is a mapping problem, not a construction problem.** I maintain my cross-review position that the spec intentionally defines non-NxN matrices for winner-take-all and red-blue modes. solver-engineer's recommendation to reformulate these as N x N would violate the spec. The real bug is in the post-processing that maps solver results back to N agents from a 2-player or N x 1 result. This is added as N3.

**Timeout mechanism is a two-layer problem.** The test is P1 (wrong code path tested). The executor shutdown semantics are P2 (resource leak, not correctness). solver-engineer's `multiprocessing`/`signal.alarm` recommendation introduces more problems than it solves. Explicit `shutdown(wait=False, cancel_futures=True)` is the right fix at the right severity.

**The cooperative diagonal is a real numerical issue, not a documentation gap.** I upgraded P3-2 to P2 after accepting that mixed payoff semantics in a single matrix can produce uninterpretable equilibria. Silent `max` symmetrization of the agreement matrix (solver-engineer's suggestion) is rejected in favor of explicit validation.

**Final priority stack (revised):**
- **P1**: Missing `solver` key on error paths (P1-1, revised fix), timeout test rewrite (P1-2, test only), SC-001/SC-002 threshold tests (N1)
- **P2**: ThreadPoolExecutor shutdown fix (N2), post-processing mapping for non-NxN modes (N3), dead variable + normalization (P1-3 downgraded), per-agent payoff parity (P2-1), integration test with known-equilibrium game (P2-2 expanded), INFO logging (P2-3), shape validation at solver boundary (P3-1 upgraded), cooperative diagonal from agreement matrix (P3-2 upgraded)
