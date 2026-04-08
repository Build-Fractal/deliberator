# Spec Compliance Disputes: Spec 021 — nashopt Solver Integration

**Reviewer**: spec-compliance
**Phase**: 4 (Final Statement)
**Date**: 2026-04-01

---

### Remaining Disputes

**Dispute: `solver` Key on Error Paths — Sentinel Value**

- **My claim**: The two error-path `PluginResult` returns (unknown-mode at lines 371-378, computation-failure at lines 394-401) should include `"solver": "error"` to distinguish error states from both the nashopt and heuristic paths. My revision (NEW-1) frames this as a new ternary value because the error paths represent a distinct execution state: no solver ran and no heuristic ran. FR-008 uses MUST language for the `solver` key's presence, and I downgraded FR-008 from MET to PARTIALLY MET on this basis.
- **Opposing position(s)**: plugin-engineer (P1-1 revision) argues the value should be `"solver": "heuristic"` rather than `"solver": "error"`, reasoning that consumers branch on `if data["solver"] == "nashopt"` and a third value would be silently skipped, producing the same behavior as a missing key. Plugin-engineer's position is that the enum should remain binary to preserve consumer contract simplicity.
- **Why I will not concede**: The binary-enum argument optimizes for consumers who only care whether nashopt ran. But error paths are semantically different from heuristic fallback: the heuristic path computes a real score from feature data, while the error paths return a score of 0.0 with an error message. Labeling an error as `"heuristic"` is a lie -- the heuristic did not run, no features were processed, and the score is not a heuristic output. Consumers who filter on `solver == "heuristic"` to aggregate heuristic-path scores would ingest garbage zeros. The `"error"` value makes the failure explicit, and any consumer that does not handle the third value will discover the gap at integration time rather than silently accumulating bad data.
- **Counter-argument to their position**: Plugin-engineer's consumer contract argument assumes consumers only branch on `== "nashopt"`. But the spec (FR-008) says the field exists "so consumers know which scoring path produced the result." Consumers who want to distinguish "scored by heuristic" from "failed entirely" need a third value. The binary enum collapses two distinct states (successful heuristic, failed computation) into one label, reducing the field's informational value to a boolean. If the concern is consumer breakage from a new enum value, the answer is to document the enum values in the PluginResult contract, not to misrepresent the execution state.
- **Proposed resolution path**: The synthesizer should choose between `"error"` and `"heuristic"`. If `"heuristic"` is chosen, the error-path returns must also set a distinguishing flag (e.g., `"error": true` or `"score_source": "none"`) so consumers can differentiate. The non-negotiable is that the `solver` key must be present -- both reviewers agree on that.

**Dispute: FR-003 Verdict — MET vs. Conditionally MET**

- **My claim**: My original review (FR-003 verdict) marked FR-003 as MET because the four mode-specific matrix builders follow the spec's Section 2 table. My revision maintains this verdict. The builders produce the shapes the spec prescribes (cooperative N x N, WTA N x 1, PD 2 x 2, red-blue 2 x K).
- **Opposing position(s)**: solver-engineer's revision (N-1, Position Summary paragraph 1) argues FR-003 should be conditionally met because the spec is internally inconsistent: the Section 2 table prescribes mode-specific shapes (including N x 1 and 2 x K) while the nashopt API signature at `spec.md:30` specifies `np.ndarray (N x N x actions)`. Solver-engineer frames this as a spec-level blocking question and requests a spec amendment before the code can be considered correct. Solver-engineer explicitly challenges my MET verdict: "I maintain that marking FR-003 as MET when the spec itself is internally inconsistent... [is a] premature green-light."
- **Why I will not concede**: FR-003's requirement is "Construct per-mode payoff matrices from FeatureSet data." The four builders construct matrices from FeatureSet data in the shapes the spec's Section 2 table defines. FR-003 is about construction, not about nashopt compatibility. The API signature at `spec.md:30` governs the solver call boundary (FR-001 territory), not the construction step (FR-003). If the shapes are incompatible with nashopt's input expectations, that is a gap between FR-003 and FR-001 -- a spec-level consistency issue -- but it does not make the construction itself non-compliant. The builders do what FR-003 asks. The question of whether nashopt can consume these shapes is a separate concern that I have already addressed by adopting the pre-call shape validation recommendation (my NEW-3, P2).
- **Counter-argument to their position**: Solver-engineer conflates two questions: "Does the code build the matrices the spec describes?" (yes -- FR-003 MET) and "Can nashopt consume those matrices?" (uncertain -- spec consistency gap). Marking FR-003 as conditionally met would mean the implementation is non-compliant with a requirement it demonstrably satisfies. The spec inconsistency is real, but the remedy is a spec amendment (which solver-engineer now agrees with in N-1), not a verdict downgrade on an FR that the code fulfills as written. My NEW-3 (pre-call shape validation) addresses the practical risk at the solver boundary without misrepresenting the FR-003 compliance status.
- **Proposed resolution path**: The synthesizer should preserve FR-003 as MET for the construction step and separately flag the spec inconsistency between the Section 2 matrix shapes and the nashopt API signature as a spec amendment item (solver-engineer's N-1). The shape validation at the solver boundary (my NEW-3, plugin-engineer's P3-1 upgraded to P2) provides the runtime safety net.

**Dispute: ThreadPoolExecutor Blocking — Severity Characterization**

- **My claim**: My revision (upgraded P3-7 to P2) frames the `shutdown(wait=True)` blocking as an operational concern for JAX/GPU deployments. The timeout mechanism itself is not "negated" -- `_try_solver` returns `None` before `__exit__` runs because the `TimeoutError` is caught inside the `with` block, and the function returns from within the `with` block's try/except. The heuristic fallback fires correctly from the caller's perspective. The blocking occurs when the `with` block's implicit `__exit__` eventually executes during garbage collection or scope exit, but this does not affect the caller's control flow for the current scoring call.
- **Opposing position(s)**: solver-engineer's revision (P1-4, modified to P2) now agrees on P2 severity and the `shutdown(wait=False, cancel_futures=True)` fix, but the Position Summary still frames it as the timeout being "partially negated" and characterizes the original finding as "correctness issue masquerading as robustness." More importantly, solver-engineer's final disagreement paragraph states that marking FR-007 as MET "when the timeout mechanism has a known resource leak" is a "premature green-light."
- **Why I will not concede**: FR-007 requires "configurable timeout with heuristic fallback." The timeout is configurable (`_DEFAULT_SOLVER_TIMEOUT`, overridable via config). The heuristic fallback fires when the timeout triggers. The resource leak from orphaned threads is a real concern but is not part of FR-007's requirement text. FR-007 does not say "and the timed-out computation must be cancelled." The spec does not address cancellation semantics at all (noted in my original review, OBA-3). Downgrading FR-007 from MET to conditionally met based on a property the spec does not require would be spec-compliance overreach -- I would be inventing requirements.
- **Counter-argument to their position**: Solver-engineer argues that a timeout mechanism with a resource leak is not truly "met." But the spec's acceptance test for FR-007 is SC-004: "Solver timeout produces heuristic fallback, not error." SC-004 is MET (both reviewers agree). The resource leak is a quality-of-implementation concern that belongs in the P2 fix recommendation, not in the compliance verdict. If every operational imperfection downgraded a verdict, no FR would ever be fully MET.
- **Proposed resolution path**: FR-007 remains MET. The executor lifecycle fix is P2 (all three reviewers now agree on both the severity and the fix approach: `shutdown(wait=False, cancel_futures=True)`). The synthesizer should not conflate resource management quality with functional requirement compliance.

---

### Convergence

**Converged: SC-001 and SC-002 Threshold Tests Are P1 and Must Exist Before Ship**

- **Shared position**: The spec's two primary acceptance criteria -- cooperative convergence scoring >= 0.9 (SC-001) and 3+ disputes scoring < 0.5 (SC-002) -- have no corresponding tests. Tests must be added that construct realistic feature data and assert the computed score against the defined thresholds. These are the spec author's definition of "done."
- **Agreeing agents**: spec-compliance (original P1-1, P1-2), solver-engineer (N-2), plugin-engineer (N1)
- **Strength**: Unanimous
- **Path to convergence**: spec-compliance identified this in Phase 1. solver-engineer initially missed it but adopted it as N-2 during revision after reading the cross-reviews. plugin-engineer adopted it as N1 during revision, crediting spec-compliance's finding. All three reviewers now list SC-001/SC-002 tests as P1 in their final priority stacks.

**Converged: FR-005 Per-Agent Best-Response Derivation Is P1**

- **Shared position**: The `hasattr(result, "agents_not_at_equilibrium")` guard at `solver.py:429` checks for an attribute not in nashopt's documented API. The fallback at line 438 ("all agents not at best response") is overly pessimistic. The fix is to compare each agent's current strategy against their `best_responses` entry from the nashopt result. This requires threading the strategy profile through to post-processing. The dead `hasattr` guard should be removed.
- **Agreeing agents**: spec-compliance (original P1-3), solver-engineer (P1-5), plugin-engineer (accepts via cross-review DC-1)
- **Strength**: Unanimous
- **Path to convergence**: All three reviewers independently identified the dead `hasattr` code and the overly pessimistic fallback in Phase 1. The cross-review process confirmed universal agreement and refined the implementation approach (solver-engineer noted the strategy-profile threading requirement, which spec-compliance accepted in the revision's expanded scope).

**Converged: ThreadPoolExecutor Fix Is P2, Using `shutdown(wait=False, cancel_futures=True)`**

- **Shared position**: The `with ThreadPoolExecutor(...)` pattern calls `shutdown(wait=True)` on `__exit__`, which may block until timed-out solver threads finish. The fix is to use explicit executor lifecycle management with `executor.shutdown(wait=False, cancel_futures=True)` (Python 3.9+). The `multiprocessing` and `signal.alarm` alternatives are rejected as introducing disproportionate complexity (pickling constraints, Unix-only, thread-safety concerns). The heuristic fallback fires correctly from the caller's perspective, making this an operational concern, not a correctness blocker.
- **Agreeing agents**: spec-compliance (P3-7 upgraded to P2), solver-engineer (P1-4 downgraded to P2), plugin-engineer (N2, P2)
- **Strength**: Unanimous
- **Path to convergence**: solver-engineer originally classified this as P1 with a `multiprocessing`/`signal.alarm` fix. plugin-engineer and spec-compliance both argued in cross-reviews that the user-facing behavior is correct and the severity was overstated. solver-engineer conceded the severity downgrade and dropped the alternative approaches in revision. All three now agree on P2 with the targeted `shutdown(wait=False, cancel_futures=True)` fix.

**Converged: Post-Processing Mapping for Non-NxN Matrix Modes Is a Real Bug**

- **Shared position**: The red-blue mode produces a 2 x K matrix (spec-prescribed), but the post-processing loop at `solver.py:416-424` iterates over N agent names and indexes into a 2-row result. The fix belongs in the result-mapping layer, not in the matrix builders: map red agents to row 0 and blue agents to row 1. The matrix builders should not be reformulated to N x N -- the spec intentionally defines non-NxN game forms for specific modes.
- **Agreeing agents**: spec-compliance (accepted via cross-review), solver-engineer (P1-2 narrowed), plugin-engineer (N3)
- **Strength**: Unanimous
- **Path to convergence**: solver-engineer originally recommended reformulating the matrices to N x N. Both spec-compliance and plugin-engineer argued in cross-reviews that the shapes are spec-prescribed and the bug is in post-processing. solver-engineer conceded the matrix construction point in revision and narrowed the fix to the post-processing mapping. All three now agree the matrices stay as the spec defines and the mapping layer is the fix target.

**Converged: Per-Agent Payoff Data Gap in Solver Path Is P2**

- **Shared position**: `scorer.py` line 173 hardcodes `payoff: 0.0` for all agents in the solver path, losing information that the heuristic path provides. The solver path should compute per-agent payoffs from the payoff matrix when available, with a sentinel (zero or null) only when the matrix is unavailable. This depends on the FR-005 strategy-profile refactor (P1-5 / P1-3) being completed first.
- **Agreeing agents**: spec-compliance (P2-5 reframed), solver-engineer (P2-7), plugin-engineer (P2-1)
- **Strength**: Unanimous
- **Path to convergence**: All three reviewers flagged the zeroed payoffs in Phase 1. The cross-review process established the dependency ordering: FR-005 best-response derivation first (P1), then per-agent payoff computation (P2). spec-compliance shifted from documentation-only to computation in the revision after accepting solver-engineer's argument that documenting an information deficit is not equivalent to fixing it.

---

### Final Position Statement

**Non-Negotiables** (3 items):

1. **SC-001 and SC-002 threshold tests must exist before the spec can be signed off.** These are the spec's own definition of acceptance. Without tests asserting that cooperative convergence scores >= 0.9 and 3+ disputes score < 0.5, the primary success criteria are unverified claims. All three reviewers agree unanimously (spec-compliance P1-1/P1-2, solver-engineer N-2, plugin-engineer N1).

2. **FR-005 per-agent equilibrium accuracy must be derived from `best_responses`, not from a blanket fallback.** The spec uses MUST language on best-response reporting. The current implementation over-reports (all agents flagged when any deviation exists) rather than accurately computing from the available `best_responses` data. The dead `hasattr` guard for a non-existent API attribute must be removed. All three reviewers converge on this fix (spec-compliance P1-3, solver-engineer P1-5, plugin-engineer cross-review acceptance).

3. **FR-003 is MET as a construction requirement; the spec inconsistency between Section 2 matrix shapes and the nashopt API signature is a spec amendment issue, not an FR-003 compliance failure.** The builders produce exactly the shapes the spec's Section 2 table defines. Relabeling FR-003 as conditionally met would penalize compliant code for a spec-level inconsistency. The practical risk is addressed by the pre-call shape validation recommendation (NEW-3, P2), and the root cause is addressed by solver-engineer's spec amendment request (N-1).

**Flexibility** (3 items):

1. **The `solver` key sentinel value on error paths can be `"error"` or `"heuristic"`, provided the execution state is distinguishable.** I prefer `"error"` for semantic accuracy, but I will accept `"heuristic"` if the error-path returns also include a distinguishing annotation (e.g., `"error": true` or `"score_source": "none"`) so consumers can tell the difference between a real heuristic score and a failed computation. What must be preserved: the `solver` key is present on all paths, and error states are not silently indistinguishable from successful heuristic scoring.

2. **The real-timeout integration test can be P1 or P2 depending on how the synthesizer weighs test coverage risk.** I upgraded it to P1 in my revision because the mock tests a different exception propagation path than production. But if the synthesizer determines that the executor lifecycle fix (P2, converged) sufficiently addresses the underlying risk, I can accept P2 for the test as well. What must be preserved: the test must exercise the actual `future.result(timeout=)` path, not a mock side_effect.

3. **The spec inconsistency on matrix shapes (solver-engineer's N-1) can be resolved as a blocking spec amendment or as a documented known issue with a follow-up spec.** I do not insist it block the current merge, provided the shape validation at the solver boundary (NEW-3) is implemented and the inconsistency is tracked. What must be preserved: the inconsistency is formally acknowledged and not silently ignored.
