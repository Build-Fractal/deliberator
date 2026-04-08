# Solver-Engineer Revised Position — Spec 021: nashopt Integration

**Reviewer role**: solver-engineer
**Phase**: Cooperative Revision (Phase 3)
**Date**: 2026-04-01

---

## Recommendation Dispositions

### P1-1: Fix winner-take-all payoff matrix shape — MODIFIED

**Original**: Reformulate WTA as N x N so nashopt can accept it.

**Cross-review input**: Both plugin-engineer (DC-1) and spec-compliance (DC-1) correctly point out that the spec's Section 2 table explicitly prescribes "N x 1 ranking payoff vector." My own Alignment section acknowledged this. The real bug is an internal spec inconsistency: the Section 2 table says N x 1, but the API signature at `spec.md:30` says `np.ndarray (N x N x actions)`. I conflated "the implementation does not match the spec" with "the implementation does not match nashopt" without distinguishing which authority governs.

**Revised position**: Withdraw the P1 code fix. Escalate as a **spec amendment request**: the spec must reconcile the WTA matrix shape (N x 1 in the table) with the nashopt API input requirement (N x N x actions in the signature). The code should not be changed until the spec is updated. If the spec amends to N x N, the code follows. If the spec formalizes N x 1 as a special case that nashopt handles (e.g., a ranking game variant), the code is already correct. Tag this as a spec-level blocking question, not an implementation bug.

### P1-2: Fix red-blue agent-to-row mapping — MODIFIED

**Original**: Either map the 2-player result back to individual agents or build an N x N matrix.

**Cross-review input**: plugin-engineer (DC-2) correctly narrows the bug: the 2 x K matrix is the intended game formulation per the spec. The matrix construction is correct. The bug is specifically in the post-processing loop at `solver.py:416-424`, which iterates over N agent names but indexes into a 2-row result. spec-compliance (T-1) agrees the 2 x K shape is spec-prescribed and the fix belongs in the mapping layer, not the matrix.

**Revised position**: Downgrade the matrix construction half of this recommendation (building N x N was wrong -- it would violate the spec's game semantics). **Surviving as P1** but narrowed: fix the post-processing at `solver.py:416-424` to map the 2-player nashopt result back to individual agents by role (red agents map to row 0, blue agents map to row 1). The matrix stays 2 x K. The agent-to-row mapping must be explicit and documented.

### P1-3: Ensure strategy profile dimensions match action space — SURVIVING

**Original**: Validate or derive strategy profiles to match payoff matrix action-space dimensions.

**Cross-review input**: spec-compliance (T-3) notes the spec does not define strategy profile construction, so this is an implementation decision rather than a spec violation. plugin-engineer's review did not address this at all. spec-compliance agrees the dimension mismatch will cause runtime errors but frames it as a spec gap rather than a code bug.

**Revised position**: **Surviving as P1**. Regardless of whether the spec defines strategy profile construction, the code must produce inputs that nashopt can consume. A 4-element vector fed alongside an N x N payoff matrix will crash. The fix is straightforward: derive strategy vector length from the payoff matrix's action dimension. This is an implementation correctness issue that does not require a spec amendment -- the spec left it to the implementer, and the implementer got it wrong.

### P1-4: Fix ThreadPoolExecutor blocking on `__exit__` — MODIFIED

**Original**: Replace `with ThreadPoolExecutor(...)` with a non-blocking pattern; consider `multiprocessing` or `signal.alarm`.

**Cross-review input**: plugin-engineer (DC-3) correctly argues I overstated the severity. The user-facing behavior (TimeoutError raised, heuristic fallback runs, PluginResult returned) is correct. The `__exit__` blocking is a resource management issue, not a user-visible correctness bug. spec-compliance (T-2) agrees the calling thread does proceed with the heuristic result regardless. Both note that recommending `multiprocessing` or `signal.alarm` introduces new problems (pickling constraints, Unix-only) that I did not acknowledge.

**Revised position**: Downgrade from P1 to **P2**. The timeout does surface the TimeoutError correctly and the heuristic fallback fires. The `shutdown(wait=True)` blocking and orphaned-thread accumulation are real resource concerns under repeated timeouts, but they are operational degradation, not correctness failures. Revised fix: use `executor.shutdown(wait=False, cancel_futures=True)` (Python 3.9+) as a targeted improvement rather than a full architectural replacement. Drop the `multiprocessing`/`signal.alarm` suggestions.

### P1-5: Derive per-agent equilibrium deviation from best_responses — SURVIVING

**Original**: Compare each agent's current strategy against its best response rather than falling back to "all agents not at equilibrium."

**Cross-review input**: All three reviewers agree on this finding. spec-compliance (SA-1) and plugin-engineer both independently identified the same `hasattr` dead code and overly pessimistic fallback. No disagreement on the diagnosis or the fix direction.

**Revised position**: **Surviving as P1**. Universal agreement across all reviewers. Note the dependency acknowledged by plugin-engineer (T-3): this requires carrying the strategy profile through to post-processing, which couples with P1-3 (strategy dimension fix). These two should be implemented together.

### P2-6: Normalize payoff matrices before passing to nashopt — WITHDRAWN

**Original**: Normalize all payoff matrices to [0, 1] by dividing by max absolute value.

**Cross-review input**: spec-compliance (DC-2) makes a strong argument that the spec says distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form," describing nashopt's internal behavior. Pre-normalizing could alter game semantics (mixed-strategy equilibria are scale-sensitive). plugin-engineer (T-1) notes that normalization could duplicate or conflict with nashopt's own normalization. Both reviewers point out that I framed this as conditional ("if nashopt's distance metric is scale-dependent") but then recommended it unconditionally.

**Revised position**: **Withdrawn**. The spec delegates normalization to nashopt. Pre-normalizing would change the game's strategic structure and potentially conflict with nashopt internals. The defensive clamping at `solver.py:409` is sufficient post-processing. If cross-mode score comparability becomes a real problem in practice, it should be addressed by understanding nashopt's normalization behavior rather than by guessing at a pre-processing step.

### P2-7: Populate per-agent payoff data from solver path — SURVIVING

**Original**: Compute each agent's actual payoff from the payoff matrix row at the current strategy profile.

**Cross-review input**: All three reviewers flag the zeroed payoffs. spec-compliance (SA-2) and plugin-engineer (T-2) agree this is real information loss. plugin-engineer notes this is coupled with P1-5 (carrying strategy profile through to post-processing). spec-compliance suggests documentation as an alternative, but I maintain that documenting an information deficit is not equivalent to fixing it.

**Revised position**: **Surviving as P2**. Implement after P1-5 resolves the strategy profile plumbing, since both require the same refactor (carrying strategy profile through to post-processing). The solver path should be at least as informative as the heuristic path.

### P2-8: Add a score reconciliation mechanism — WITHDRAWN

**Original**: Run both solver and heuristic, log comparison for calibration.

**Cross-review input**: plugin-engineer (T-2) correctly identifies that doubling computation cost for every scoring call is excessive, and that the two scores are fundamentally incommensurable (discrete fraction vs. continuous distance), making any divergence threshold arbitrary and uninterpretable. spec-compliance (T-4) notes the spec does not require score comparability across paths.

**Revised position**: **Withdrawn**. The cost/benefit is unfavorable. The two scoring regimes measure different things by design. A runtime comparison would produce a number without a meaningful interpretation. If calibration is needed, it belongs in a one-time validation study, not in the hot path. The score discontinuity on timeout fallback is a known trade-off documented by the `solver` provenance field (FR-008) -- consumers can filter by solver type.

### P3-9: Add asymmetric agreement matrix handling — MODIFIED

**Original**: Symmetrize with `max(matrix[i][j], matrix[j][i])`.

**Cross-review input**: plugin-engineer (T-4) argues that silent symmetrization with `max` is a data repair that masks upstream bugs. The correct response to an asymmetric matrix that should be symmetric is to fail loud, not fix silently. spec-compliance did not address this.

**Revised position**: **Modified, surviving as P3**. Replace silent `max` symmetrization with a validation check: if `matrix[i][j] != matrix[j][i]` for any pair, log a warning (not an error -- the game can still be solved with an asymmetric matrix, it just changes the game-theoretic interpretation). Do not silently repair. Add a test with a triangular agreement matrix to verify the warning fires.

### P3-10: Add integration test with a known-equilibrium game — SURVIVING

**Original**: Test with a 2x2 game (e.g., Prisoners' Dilemma) with known Nash equilibrium.

**Cross-review input**: plugin-engineer (T-5) proposes a complementary API contract test (validate shapes and types). Both are needed. spec-compliance does not comment specifically. Plugin-engineer is right that API contract tests are more stable across nashopt version changes, but my test catches a broader class of bugs (shape-compatible but numerically wrong results).

**Revised position**: **Surviving as P3**. Both test types should exist: an API contract test (plugin-engineer's approach) for interface stability, and a known-equilibrium test (my approach) for numerical correctness. Mark both as `pytest.importorskip("nashopt")`.

---

## New Recommendations

### N-1 (P1): Resolve spec internal inconsistency on matrix shapes before merging

The spec defines WTA as "N x 1 ranking payoff vector" in the Section 2 table but specifies the nashopt API input as `np.ndarray (N x N x actions)`. The red-blue mode is "2 x K" but the API expects N agents. These contradictions must be resolved at the spec level. The implementation cannot be correct until the spec is self-consistent. Recommend a spec amendment that either (a) defines a shape adapter layer that converts non-standard matrices to nashopt's expected format, or (b) documents which modes use non-standard game forms and how nashopt handles them.

**Source**: Emerged from the convergence across all three reviewers that my original WTA/red-blue P1 recommendations were treating spec-compliant code as buggy. The root cause is the spec, not the code.

### N-2 (P1): Add SC-001 and SC-002 threshold tests

spec-compliance's review identifies that the spec's two primary success criteria (cooperative convergence score >= 0.9, 3+ disputes score < 0.5) have no corresponding tests. My original review did not address success criteria testing. These are the spec author's definition of "done" and their absence means the spec cannot be signed off. These tests require constructing deliberation scenarios that exercise the full pipeline (feature extraction through scoring) and asserting the score thresholds.

**Source**: spec-compliance's review, confirmed as a gap in my own analysis.

---

## Position Summary

The cross-reviews sharpened my analysis in three important ways:

**First**, I was wrong to treat spec-compliant matrix shapes as implementation bugs. The WTA N x 1 shape and red-blue 2 x K shape are prescribed by the spec. The real problem is that the spec contradicts itself between the matrix table and the API signature. This is a spec amendment issue (new recommendation N-1), not a code fix. My original P1-1 is withdrawn as a code recommendation and reframed as a spec question.

**Second**, I overstated the ThreadPoolExecutor severity. The timeout mechanism works correctly from the user's perspective: the heuristic fallback fires, the PluginResult is returned, the consumer is unaffected. The resource leak from orphaned threads is real but is a P2 operational concern, not a P1 correctness blocker. My recommendation to introduce `multiprocessing` or `signal.alarm` would have created new problems without proportionate benefit.

**Third**, the normalization recommendation was speculative. I recommended pre-normalizing payoff matrices without confirming that nashopt's distance metric is scale-dependent. The spec explicitly says nashopt handles normalization internally. Pre-normalizing would change game semantics. This recommendation is withdrawn.

What survives with high confidence: the red-blue post-processing mapping bug (P1-2, narrowed), the strategy profile dimension mismatch (P1-3), the per-agent best-response derivation (P1-5), and the per-agent payoff data gap (P2-7). These are issues where all three reviewers converge or where the technical argument is uncontested. The new recommendations (spec amendment N-1, threshold tests N-2) address gaps that my original review missed entirely.

The strongest remaining disagreement is with spec-compliance on FR-003 and FR-007 verdicts. I maintain that marking FR-003 as MET when the spec itself is internally inconsistent, and marking FR-007 as MET when the timeout mechanism has a known resource leak, are premature green-lights. Both should be conditionally met pending resolution of the spec inconsistency and the executor fix respectively.
