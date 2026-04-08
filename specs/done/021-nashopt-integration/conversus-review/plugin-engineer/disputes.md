# Cooperative Disputes — Phase 4

**Agent**: plugin-engineer
**Mode**: cooperative
**Date**: 2026-04-01

---

### Remaining Disputes

- **Dispute: Error-path `solver` key value — `"heuristic"` vs. `"error"`**
  - **My claim**: The error-path `PluginResult.data["solver"]` should be `"heuristic"` to keep the enum binary and avoid silently expanding the consumer contract (revision, P1-1). Consumers that branch on `if data["solver"] == "nashopt"` will correctly skip error cases without any code change. A third sentinel value (`"error"`) forces every consumer to update their branching logic or risk silent misclassification.
  - **Opposing position(s)**: spec-compliance (revision, NEW-1) recommends `"solver": "error"` on both error paths, arguing FR-008 requires the key's presence and that `"error"` accurately represents what happened. solver-engineer's revision does not take a position on the specific value.
  - **Why I will not concede**: The consumer contract is the deciding factor, not the description of the internal event. FR-008 exists so consumers can determine which scoring path produced the result. When no solver ran and no heuristic ran (error), the consumer needs to know the result is not solver-derived. `"heuristic"` communicates this correctly: the result should be treated identically to a heuristic fallback. `"error"` introduces a third state that every downstream consumer must handle, and the spec defines only two scoring paths (solver and heuristic). An error is not a third scoring path -- it is the absence of a scoring path, which defaults to the heuristic treatment.
  - **Counter-argument to their position**: spec-compliance's argument is accuracy-centric ("error" describes what happened). But the `solver` field is not a diagnostic log -- it is a routing tag for consumers. Accuracy of the internal event is served by the `data["error"]` key that already exists on these paths. Adding `"error"` to the `solver` field conflates diagnostics (what went wrong) with routing (which scoring path to trust). Consumers need routing, not diagnostics, from this field.
  - **Proposed resolution path**: The synthesizer should evaluate whether the `solver` field serves a diagnostic or routing purpose. If routing (my position), `"heuristic"` is correct. If diagnostic, `"error"` is correct. I propose `"heuristic"` with an additional `"solver_note": "error_fallback"` key for consumers that need to distinguish error-fallback from genuine heuristic execution. This preserves binary routing while adding diagnostic granularity without breaking existing consumers.

- **Dispute: Spec-level vs. code-level resolution of matrix shape inconsistency**
  - **My claim**: The WTA (N x 1) and red-blue (2 x K) matrix shapes are spec-prescribed and intentional. The implementation bug is in the post-processing layer that maps solver results back to N agents, not in the matrix builders or the spec (revision, N3 and position summary). The code fix belongs in `solver.py` post-processing.
  - **Opposing position(s)**: solver-engineer (revision, N-1) frames this as a spec amendment issue -- the spec must reconcile the Section 2 table (N x 1 / 2 x K) with the nashopt API signature (N x N x actions) before any code change is made. solver-engineer explicitly recommends blocking on a spec amendment and withdraws code-level fixes. spec-compliance (revision, declined items) agrees the spec prescribes these shapes and the implementation follows correctly, but also defers to a shape validation layer (NEW-3) rather than fixing the post-processing directly.
  - **Why I will not concede**: Blocking on a spec amendment delays the fix for a known, concrete post-processing bug. The post-processing loop at `solver.py:416-424` iterates over N agents and indexes into a 2-row result. This will produce wrong results or crash regardless of whether the spec is amended. The spec may need amendment for the shape question (how nashopt ingests non-NxN matrices), but the post-processing mapping bug is independent of that question and can be fixed now. Coupling a concrete code fix to a spec governance process is unnecessary gatekeeping.
  - **Counter-argument to their position**: solver-engineer's revised N-1 treats the spec inconsistency and the post-processing bug as a single issue. They are separable. The spec inconsistency is about whether nashopt can accept non-NxN inputs -- that is a spec/API question. The post-processing bug is about whether the code correctly maps a 2-row result back to N agents -- that is a code correctness question with an unambiguous answer (it does not). solver-engineer's own revision (P1-2, surviving) agrees the post-processing fix is valid and narrowed to the mapping layer. The contradiction is between N-1 (block on spec amendment) and P1-2 (fix the mapping now).
  - **Proposed resolution path**: Decouple the two issues. The post-processing mapping fix (my N3, solver-engineer's narrowed P1-2) proceeds as a code change at P1/P2. The spec shape inconsistency (solver-engineer's N-1) proceeds as a parallel spec amendment request that does not block the code fix. Both reviewers agree the mapping is wrong; the only disagreement is sequencing.

- **Dispute: Cooperative diagonal payoff source — agreement matrix vs. surviving count**
  - **My claim**: The cooperative diagonal should use `agreement_matrix` self-pair values when available, with `surviving_count` as fallback only when agreement data is absent. Silent `max` symmetrization of asymmetric agreement matrices should be replaced with explicit validation and a warning (revision, P3-2 upgraded to P2).
  - **Opposing position(s)**: solver-engineer (revision, P3-9 modified to P3) proposes a log warning for asymmetric matrices rather than fixing the diagonal source. solver-engineer does not address whether the diagonal should come from `agreement_matrix` or `surviving_count`. spec-compliance does not address this item in their revision.
  - **Why I will not concede**: Mixing payoff semantics within a single matrix (count-based diagonal, agreement-based off-diagonal) produces a game where the Nash equilibrium has no coherent interpretation. The diagonal entries represent self-agreement (trivially high) while off-diagonal entries represent pair-agreement (variable). This semantic mismatch biases the equilibrium toward strategies that exploit the inflated diagonal rather than strategies that maximize genuine cooperation. The agreement matrix already contains self-pair data that is semantically consistent with the off-diagonal entries.
  - **Counter-argument to their position**: solver-engineer's revised P3-9 addresses symmetry validation but not the diagonal source. The asymmetry warning is necessary but insufficient -- even a perfectly symmetric matrix with mixed-semantic entries produces uninterpretable equilibria. The diagonal source is the deeper issue. solver-engineer's silence on this point in their revision suggests it was not considered, not that it was rejected.
  - **Proposed resolution path**: Accept solver-engineer's asymmetry validation (log warning) as a complementary measure. The diagonal fix is orthogonal and should proceed independently: use `agreement_matrix[i][i]` when the matrix is populated, fall back to `surviving_count` only when agreement data is absent. The synthesizer should evaluate both measures as separate P2 items rather than treating the warning as a substitute for the diagonal fix.

### Convergence

- **Converged: SC-001 and SC-002 threshold tests are P1 requirements**
  - **Shared position**: The spec's primary acceptance criteria (cooperative convergence >= 0.9, 3+ disputes < 0.5) must have corresponding tests before the implementation can be signed off. These tests should exercise the scoring pipeline with scenarios designed to produce scores on both sides of the threshold.
  - **Agreeing agents**: spec-compliance (revision, P1-1/P1-2 kept), plugin-engineer (revision, N1), solver-engineer (revision, N-2)
  - **Strength**: Unanimous
  - **Path to convergence**: spec-compliance identified this gap in Phase 1. plugin-engineer and solver-engineer both adopted it in Phase 3 revision after recognizing it as a scope gap in their original reviews. Full convergence achieved through the cross-review process.

- **Converged: Per-agent equilibrium deviation must use best_responses, not pessimistic fallback**
  - **Shared position**: The `hasattr(result, "agents_not_at_equilibrium")` guard is dead code. The per-agent equilibrium reporting must derive deviation by comparing each agent's current strategy against their `best_responses` entry. The pessimistic "all agents not at equilibrium" fallback must be removed. This requires carrying the strategy profile through to post-processing.
  - **Agreeing agents**: solver-engineer (revision, P1-5 surviving), plugin-engineer (revision, P2-1 dependency acknowledged), spec-compliance (revision, P1-3 kept with expanded scope)
  - **Strength**: Unanimous
  - **Path to convergence**: All three reviewers independently identified this in Phase 1. Cross-review confirmed universal agreement. No reviewer challenged the diagnosis or the fix direction at any phase.

- **Converged: ThreadPoolExecutor fix is `shutdown(wait=False, cancel_futures=True)`, not multiprocessing/signal**
  - **Shared position**: The `with ThreadPoolExecutor(...)` pattern's implicit `shutdown(wait=True)` is a real resource concern under repeated timeouts. The fix is explicit executor lifecycle management with `shutdown(wait=False, cancel_futures=True)` (Python 3.9+). Replacing with `multiprocessing` or `signal.alarm` introduces disproportionate complexity (pickling constraints, Unix-only behavior). This is P2 severity -- the heuristic fallback fires correctly from the user's perspective.
  - **Agreeing agents**: plugin-engineer (revision, N2), solver-engineer (revision, P1-4 downgraded to P2 with same fix), spec-compliance (revision, P3-7 upgraded to P2 with same fix)
  - **Strength**: Unanimous
  - **Path to convergence**: solver-engineer originally proposed multiprocessing/signal at P1. plugin-engineer and spec-compliance both challenged the severity and the approach in cross-review. solver-engineer conceded in revision, adopting the `shutdown(wait=False)` approach and downgrading to P2. All three now agree on mechanism, severity, and scope.

- **Converged: Matrix shapes are spec-prescribed; the bug is in post-processing mapping**
  - **Shared position**: The WTA (N x 1) and red-blue (2 x K) matrix shapes are intentional per the spec's Section 2 table. Reformulating them to N x N would violate the spec's game-theoretic semantics. The bug is in the post-processing code that maps solver results back to individual agents, specifically the loop that iterates over N agents while indexing into a 2-row or 1-column result.
  - **Agreeing agents**: plugin-engineer (revision, N3 and position summary), solver-engineer (revision, P1-2 narrowed to post-processing mapping), spec-compliance (revision, declined items -- explicitly rejects N x N reformulation)
  - **Strength**: Unanimous
  - **Path to convergence**: solver-engineer originally proposed N x N reformulation. plugin-engineer and spec-compliance both rejected this in cross-review as spec-violating. solver-engineer withdrew the matrix construction fix in revision and narrowed to the post-processing mapping. All three now agree the matrix builders are correct and the post-processing is not.

- **Converged: Pre-call shape validation at the solver boundary**
  - **Shared position**: A shape-compatibility assertion before the nashopt call would surface incompatible matrix dimensions with a clear error message instead of an opaque JAX failure. This is a defensive measure regardless of whether the shape mismatch is a spec inconsistency or an implementation bug.
  - **Agreeing agents**: plugin-engineer (revision, P3-1 upgraded to P2), spec-compliance (revision, NEW-3 at P2), solver-engineer (revision, P1-3 surviving -- strategy dimension validation serves the same purpose at the same boundary)
  - **Strength**: Unanimous
  - **Path to convergence**: plugin-engineer proposed shape validation at P3 in Phase 1. solver-engineer's strategy dimension mismatch finding (P1-3) identified the same boundary from a different angle. Both upgraded in revision. spec-compliance adopted as NEW-3 after synthesizing both inputs.

### Final Position Statement

**Non-Negotiables** (3 items):

- The post-processing mapping fix for non-NxN matrix modes must not be blocked on a spec amendment. The bug at `solver.py:416-424` produces wrong results for red-blue mode regardless of how the spec shape inconsistency is resolved. Decoupling the code fix from the spec governance process is essential to ship a correct implementation. (revision N3; solver-engineer's own P1-2 agrees the mapping is wrong)

- SC-001 and SC-002 threshold tests must be implemented before sign-off. These are the spec author's definition of "done." Without them, there is no verification that the scoring pipeline meets its primary acceptance criteria. (revision N1; unanimous across all three reviewers)

- The `solver` key on error-path returns must use `"heuristic"`, not `"error"`, to maintain a binary consumer contract. The `data["error"]` key already serves the diagnostic purpose. The `solver` field is a routing tag, not a diagnostic log. (revision P1-1)

**Flexibility** (3 items):

- ThreadPoolExecutor shutdown fix: I am committed to `shutdown(wait=False, cancel_futures=True)` as the mechanism, but flexible on severity classification (P2 is acceptable given the heuristic fallback works correctly). If the team prefers to document the `__exit__` blocking as a known limitation rather than fix it in this iteration, I can accept that with a tracking issue.

- Cooperative diagonal payoff source: I strongly prefer using `agreement_matrix` self-pair for the diagonal, but I can accept the current `surviving_count` approach if it is explicitly documented as a known semantic inconsistency with a TODO for future correction. The asymmetry validation warning (solver-engineer's P3-9) should proceed regardless.

- Integration test scope: I proposed both API contract tests and known-equilibrium numerical tests (revision P2-2 expanded). If only one can be implemented this iteration, the known-equilibrium test (solver-engineer's approach) is more valuable for catching numerical regressions. The API contract test can be deferred.
