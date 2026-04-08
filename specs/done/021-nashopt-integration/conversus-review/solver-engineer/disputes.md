# Solver-Engineer Final Statement — Spec 021: nashopt Integration

**Reviewer role**: solver-engineer
**Phase**: Cooperative Disputes (Phase 4)
**Date**: 2026-04-01

---

## Remaining Disputes

### D-1: The `solver` key on error paths should be `"heuristic"`, not `"error"`

**With**: spec-compliance (NEW-1)
**About**: spec-compliance recommends adding `"solver": "error"` to the two error-path `PluginResult` returns. plugin-engineer's revised P1-1 argues for `"solver": "heuristic"` instead. I side with plugin-engineer.

**My position**: The FR-008 contract defines the `solver` key as signaling which scoring path produced the result. The consumer's branching logic is `if data["solver"] == "nashopt"` vs. everything else. A third sentinel `"error"` silently expands a binary enum to a ternary one, and any consumer that does not explicitly handle the new value will silently skip error cases -- the exact class of bug this key is supposed to prevent. On the error paths, no solver ran, so the result is semantically equivalent to a heuristic fallback. The value should be `"heuristic"`. If consumers need to distinguish "heuristic by design" from "heuristic by failure," that information already lives in the `"error"` key present in the same data dict.

**Impact if unresolved**: Consumer-facing contract ambiguity. A deployed consumer encountering `"solver": "error"` for the first time at runtime will either crash (if it expects only two values) or silently drop the result (if it defaults on unknown values). Both outcomes are worse than the current missing-key bug.

### D-2: FR-003 and FR-007 should be PARTIALLY MET, not MET

**With**: spec-compliance (verdicts)
**About**: spec-compliance marks FR-003 (payoff matrix construction) as MET and FR-007 (timeout and fallback) as MET. I maintain both should be PARTIALLY MET.

**My position on FR-003**: The spec's Section 2 table prescribes matrix shapes (N x 1 for WTA, 2 x K for red-blue) that contradict the nashopt API signature (N x N x actions) documented in the same spec at line 30. All three reviewers now agree this inconsistency exists. Marking FR-003 as MET means "the implementation correctly constructs payoff matrices." But "correctly" relative to which part of the spec? The builders follow the Section 2 table. They violate the API signature. The implementation cannot satisfy both simultaneously. A PARTIALLY MET verdict acknowledges that the code is faithful to one half of a contradictory requirement and flags the spec amendment (my N-1) as a prerequisite for a definitive verdict.

**My position on FR-007**: The timeout fires correctly and the heuristic fallback runs. That much is MET. However, `shutdown(wait=True)` in the `with` block's `__exit__` means the calling thread blocks after returning from `_try_solver` until the solver thread completes. For JAX GPU workloads, this could be tens of seconds of blocked thread time per timeout event. All three reviewers now agree the executor lifecycle needs fixing (variously at P2). A requirement whose implementation has a known, agreed-upon deficiency in the mechanism it specifies (timeout and resource cleanup) should be PARTIALLY MET, not MET.

**Impact if unresolved**: If these remain MET, the spec sign-off implies the matrix construction and timeout mechanisms are complete and correct. They are not. The spec amendment (N-1) and executor fix (P2) are agreed-upon follow-ups, and the verdicts should reflect that dependency.

### D-3: Silent `max` symmetrization vs. validation-with-warning for asymmetric agreement matrices

**With**: plugin-engineer (P3-2 revision)
**About**: My original P3-9 recommended `max(matrix[i][j], matrix[j][i])` symmetrization. plugin-engineer argued silent repair masks upstream bugs. In my revision I accepted the critique and proposed a validation check with a warning log. plugin-engineer's revised P3-2 proposes using the agreement matrix self-pair for diagonal values and validating symmetry but does not specify what happens when asymmetry is detected. The gap is in the failure mode: warn-and-proceed vs. warn-and-fail.

**My position**: Warn-and-proceed. An asymmetric agreement matrix changes the game-theoretic interpretation (it becomes a non-symmetric bimatrix game rather than a symmetric one), but nashopt can still solve it. Failing on asymmetry would make the solver path fragile to upstream data quality issues that the heuristic path silently tolerates. The warning log gives operators visibility. If the team later determines that asymmetry always indicates a bug, the warning can be promoted to an error.

**Impact if unresolved**: Minor. Both positions agree on validation. The disagreement is only about severity of the response (warn vs. fail). Defaulting to warn-and-proceed is strictly more available.

---

## Convergence

### C-1: Matrix shapes are spec-prescribed; post-processing is the real bug

All three reviewers converge: the WTA N x 1 and red-blue 2 x K matrices are intentional per the spec's Section 2 table. My original recommendation to reformulate as N x N is withdrawn. The bug is in the post-processing loop at `solver.py:416-424` which iterates over N agents but indexes into a result shaped for fewer players. plugin-engineer's N3 and my narrowed P1-2 describe the same fix: map the 2-player result back to individual agents by role assignment. This is universally agreed.

### C-2: SC-001 and SC-002 threshold tests are blocking P1 items

All three reviewers now include these. spec-compliance originated the finding (P1-1, P1-2). plugin-engineer adopted it as N1. I adopted it as N-2 in my revision. The spec's primary acceptance criteria have no corresponding test coverage. This is the single most important gap identified across all three reviews and it is unanimous.

### C-3: Per-agent equilibrium deviation must use `best_responses`, not the pessimistic fallback

Universal agreement across all three reviews. The `hasattr(result, "agents_not_at_equilibrium")` guard is dead code. The fix is to compare each agent's current strategy against their `best_responses` entry. solver-engineer (P1-5), plugin-engineer (DC-1 of solver-engineer), and spec-compliance (P1-3) all converge on diagnosis and direction. The implementation dependency on carrying the strategy profile through to post-processing is acknowledged by all parties.

### C-4: ThreadPoolExecutor fix is `shutdown(wait=False, cancel_futures=True)`, not `multiprocessing`

All three reviewers converge on the targeted fix. My original `multiprocessing`/`signal.alarm` recommendation is withdrawn. The `with` block's implicit `shutdown(wait=True)` is the problem, and the Python 3.9+ explicit shutdown API is the proportionate solution. The severity is P2 (operational, not correctness). The timeout test rewrite is a separate P1 item.

### C-5: Pre-call shape validation at the solver boundary

plugin-engineer (P3-1, upgraded to P2) and spec-compliance (NEW-3) agree that validating matrix dimensions before passing to nashopt prevents opaque JAX errors. I accept this as a practical defensive measure. This does not resolve the spec inconsistency (my N-1) but it does surface the problem clearly at runtime rather than letting it propagate into JAX internals.

---

## Final Position

### Non-Negotiables

1. **Post-processing agent-to-row mapping must be fixed before merge (P1-2, narrowed).** The loop at `solver.py:416-424` will produce wrong results for every red-blue mode invocation. This is a silent correctness bug, not a warning or a resource concern. The 2-player result must be mapped back to N agents by role assignment.

2. **Strategy profile dimensions must match the payoff matrix action space (P1-3).** A 4-element strategy vector fed alongside an N x N payoff matrix will crash nashopt at runtime. This is not a spec gap -- it is a dimension mismatch the implementer introduced. The strategy vector length must be derived from the payoff matrix's action dimension.

3. **Per-agent equilibrium deviation must use `best_responses` (P1-5).** The current fallback marks all agents as not-at-equilibrium regardless of the solver result. This defeats the purpose of running the solver. The dead `hasattr` guard must be removed and replaced with per-agent best-response comparison.

4. **SC-001 and SC-002 threshold tests must exist before sign-off (N-2).** The spec's own acceptance criteria are untested. Without these tests, the spec cannot be declared complete by its own definition.

5. **The spec must resolve its internal matrix shape inconsistency (N-1).** The Section 2 table and the API signature contradict each other. The implementation cannot be verified as correct until the spec is self-consistent. This is a blocking spec amendment, not a code change.

### Flexibility

1. **Severity of the `solver` key on error paths.** I agree with plugin-engineer that the value should be `"heuristic"`, not `"error"`, but I am flexible on whether this is P1 or P2. The key must be present; the value is debatable.

2. **ThreadPoolExecutor fix severity.** I accept P2. The user-facing timeout behavior is correct. The resource leak is real but not a ship-blocker. `shutdown(wait=False, cancel_futures=True)` is the right fix and I defer to the group on timing.

3. **Pre-call shape validation scope.** I support this (plugin-engineer's P3-1 upgraded to P2, spec-compliance's NEW-3) but I am flexible on whether the validation raises an exception or logs a warning and skips the solver. The spec inconsistency (N-1) makes it unclear what the "correct" shape is, so a hard assertion may be premature.

4. **Cooperative diagonal semantics (plugin-engineer's P3-2).** I accept plugin-engineer's position that agreement matrix self-pair should be used when present. I proposed `max` symmetrization originally and have withdrawn it in favor of validation. I am flexible on the priority (P2 or P3) since the numerical impact depends on how often the diagonal/off-diagonal scale divergence is material.

5. **Per-agent payoff data (P2-7).** This should be implemented but I accept sequencing it after the strategy profile plumbing is in place. If the team decides to ship with sentinel values (`null` rather than `0.0`) as an interim step, that is acceptable as long as the sentinel is distinguishable from a real zero payoff.

6. **Red-blue normalization / dead `total_surface` variable.** I accept plugin-engineer's merged P2 treatment. The scale inconsistency between branches is real but the severity depends on how often the `max_k == 0` fallback fires in practice. P2 is appropriate.
