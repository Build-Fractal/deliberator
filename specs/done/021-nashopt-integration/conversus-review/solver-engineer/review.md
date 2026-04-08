# Solver-Engineer Review — Spec 021: nashopt Integration

**Reviewer role**: solver-engineer (numerical solver verification)
**Date**: 2026-04-01
**Files reviewed**:
- `conversus/specs/done/021-nashopt-integration/spec.md`
- `conversus/conversus/plugins/nashopt/solver.py`
- `conversus/conversus/plugins/nashopt/scorer.py`
- `conversus/tests/test_solver.py`
- `conversus/conversus/plugins/nashopt/payoffs.py` (heuristic reference)
- `conversus/conversus/schemas/features.py` (data model reference)

---

## Executive Summary

The nashopt solver integration is structurally sound. The dispatch architecture (solver with timeout, heuristic fallback) is well-layered and the `SolverResult` dataclass captures the right dimensions. Payoff matrix construction per mode follows reasonable game-theoretic formulations. However, the review identified several numerical correctness concerns: the winner-take-all mode produces an N x 1 vector instead of a proper payoff matrix, the red-blue mode collapses N agents into a fixed 2-row matrix that drops agent identity, the cooperative diagonal uses `surviving_count` rather than agreement data when available, and the strategy profile dimensions are not guaranteed to match the payoff matrix action space. The `ThreadPoolExecutor` timeout mechanism is adequate for I/O-bound waits but has documented limitations under GIL contention with JAX. Degenerate cases (n=0, n=1, zero-variance) are handled correctly. The heuristic fallback path preserves pre-021 behavior faithfully.

---

## Alignment

- **FR-001/FR-002 (solver dispatch with optional import)**: The `HAS_NASHOPT` flag pattern at `solver.py:27-39` correctly gates the import, and `scorer.py:134` checks it before attempting the solver path. The fallback is seamless. This matches the spec's requirement that nashopt/jax remain optional runtime dependencies.

- **FR-003 (per-mode payoff matrices)**: All four modes have dedicated builders (`solver.py:92-104`). The cooperative N x N, prisoners-dilemma N x N, and red-blue 2 x K shapes align with the spec's Section 2 table. The winner-take-all builder returns N x 1 as specified.

- **FR-004/FR-005 (SolverResult and best-response reporting)**: The `SolverResult` dataclass at `solver.py:47-63` captures `is_equilibrium`, `distance`, `score`, `best_responses`, and `agents_not_at_equilibrium`. The score formula `1.0 - distance` at `solver.py:410` matches the spec's Section 2 scoring formula exactly. Distance clamping to [0.0, 1.0] at `solver.py:409` is correct defensive coding.

- **FR-006 (degenerate cases)**: The solver handles n=0 (`solver.py:362-369`), n=1 (`solver.py:371-379`), and zero-variance (`solver.py:386-394`) all before calling nashopt. Each returns a sensible trivial-equilibrium `SolverResult`. Tests at `test_solver.py:521-552` and `test_solver.py:905-952` confirm these paths.

- **FR-007 (timeout)**: The `_try_solver` function in `scorer.py:124-154` wraps the solver call in a `ThreadPoolExecutor(max_workers=1)` with configurable timeout (default 30s). Timeout and general exceptions both fall back to heuristic with a log warning. The test at `test_solver.py:622-658` validates this behavior.

- **FR-008 (solver provenance)**: Both the solver path (`scorer.py:184`) and heuristic path (`scorer.py:262`) set `data["solver"]` to `"nashopt"` or `"heuristic"` respectively. Backward-compatibility tests at `test_solver.py:585-614` confirm the field is always present and is a valid string.

---

## Missed Opportunities

1. **Winner-take-all matrix is not a proper payoff matrix** (`solver.py:148-176`). The spec says "N x 1 ranking payoff vector" and the builder returns `[[1.0], [0.55], ...]`. But `nashopt.check_equilibrium()` expects a payoff matrix of shape `(N, N, actions)` per the spec's own API signature at `spec.md:30`. An N x 1 array is not a valid normal-form game. The nashopt library will almost certainly reject this shape or produce meaningless results. The winner-take-all payoff should be reformulated as an N x N matrix where entry (i, j) encodes i's payoff given j's strategy, or as a proper N-player game tensor.

2. **Red-blue matrix collapses agent identity** (`solver.py:222-287`). The builder combines all red agents into one row and all blue agents into another, producing a fixed 2 x K matrix regardless of how many agents exist. When `agent_names` has 4 agents (2 red, 2 blue), the matrix has 2 rows but `check_equilibrium_nashopt` passes `agent_names` (length 4) into the best-response loop at `solver.py:416-424`. The row-to-agent mapping is lost. The `agents_not_at_equilibrium` list will reference individual agents by name, but the solver sees only 2 players. This is a dimension mismatch that will cause indexing errors or silent misattribution.

3. **Strategy profile dimension mismatch** (`solver.py:294-326`). When `position_vector` is absent, the fallback strategy is a 4-element vector `[surviving/recs, withdrawn/recs, modified/recs, concession_rate]`. But the payoff matrix action space varies by mode: cooperative is N x N (N actions), PD is N x N, WTA is N x 1 (1 action), red-blue is 2 x K. There is no guarantee the strategy vector length matches the number of columns in the payoff matrix. The `nashopt.check_equilibrium()` API likely requires strategy dimensions to match the action space. This mismatch will cause runtime errors for non-trivial games.

4. **Cooperative diagonal semantics when agreement matrix is present** (`solver.py:120-145`). When `features.agreement_matrix` is truthy, off-diagonal entries use the agreement matrix, but the diagonal still uses `surviving_count` (line 127). The agreement matrix may contain a self-entry `agreement_matrix[name_i][name_i]` that represents a different quantity (e.g., self-consistency score). Using `surviving_count` on the diagonal while using agreement data off-diagonal mixes two different payoff semantics in the same matrix, which can produce a non-interpretable game.

5. **Heuristic and solver scoring are not comparable** (`scorer.py:194-263` vs `solver.py:333-446`). The heuristic path computes score as `agents_at_eq / total_agents` (a fraction, `scorer.py:254`). The solver path computes score as `1.0 - distance` (a continuous metric from nashopt). These measure fundamentally different things: one is a discrete fraction, the other is a continuous distance metric. When the system switches between them (e.g., on timeout), the score can jump discontinuously. Consumers comparing scores across runs where different solvers were used will draw incorrect conclusions.

6. **`_score_from_solver` sets payoff fields to 0.0** (`scorer.py:174`). The per-agent data from the solver path always reports `"payoff": 0.0` and `"best_response_payoff": 0.0`. The heuristic path populates these with actual computed values (`scorer.py:247-248`). Downstream consumers that rely on per-agent payoff data (e.g., to show agents their gap-to-best-response) will get meaningful data from the heuristic path but zeros from the solver path. This is an information loss that undermines the value of the exact solver.

7. **No normalization of payoff matrices before passing to nashopt** (`solver.py:382-383`). The raw payoff values vary wildly by mode: cooperative surviving counts might be in [0, 20], PD territory values in [-10, 15], red-blue severity sums in [0, 100+]. The spec says distance is "normalized to [0.0, 1.0] by the maximum possible distance for the game form" (`spec.md:53`), but the implementation just clamps. If nashopt's distance metric is scale-dependent, unnormalized inputs will produce scale-dependent distances, making the 0.0-1.0 score non-comparable across modes or even across deliberations of different sizes.

8. **`_build_rb_matrix` computes `total_surface` twice** (`solver.py:255-259` and `solver.py:270-274`). The first computation at line 255 is unused when `max_k > 0` (the code falls through to line 270). This is dead code in the severity-vector branch. While not a correctness bug, it signals incomplete refactoring and could mislead future maintainers.

9. **Agreement matrix lookup is not symmetric** (`solver.py:128-133`). The lookup `features.agreement_matrix.get(name_i, {}).get(name_j, 0)` assumes the matrix is stored with both `(i,j)` and `(j,i)` entries. If the agreement matrix is only populated in one direction (upper triangle), off-diagonal entries will asymmetrically default to 0, producing a non-symmetric payoff matrix for what should be a symmetric cooperative game. The test at `test_solver.py:98-103` uses a fully populated matrix, so this path is untested.

---

## Off-Base Assumptions

1. **Assumption that `nashopt.check_equilibrium()` returns `agents_not_at_equilibrium`** (`solver.py:429-434`). The spec's API surface at `spec.md:29-35` shows three return fields: `is_equilibrium`, `distance`, and `best_responses`. There is no `agents_not_at_equilibrium` field. The code uses `hasattr` guards (`solver.py:429`), so it won't crash, but the fallback at `solver.py:436-438` assumes all agents are not at equilibrium when the game is not at equilibrium. This is overly pessimistic for games where only one agent deviates. The per-agent deviation should be computed from `best_responses` by comparing each agent's current strategy to its best response.

2. **Assumption that the ThreadPoolExecutor timeout cancels JAX computation** (`scorer.py:137-142`). `future.result(timeout=...)` raises `TimeoutError` in the calling thread, but it does not cancel or kill the worker thread. JAX computations hold the GIL intermittently during NumPy interop and Python callback phases. The solver thread will continue running in the background until it completes or the process exits. Under repeated timeouts, orphaned solver threads will accumulate, consuming memory and CPU. The ThreadPoolExecutor's `__exit__` calls `shutdown(wait=True)`, which means the `with` block will actually block until the timed-out thread finishes, negating the timeout. This is a correctness issue masquerading as a robustness feature.

3. **Assumption that zero standard deviation implies trivial equilibrium** (`solver.py:386`). A payoff matrix where all entries are identical (std < 1e-12) is indeed a trivial equilibrium, but `np.std(payoff_matrix)` computes the standard deviation across all entries globally. A matrix like `[[1, 3], [3, 1]]` has nonzero global std but is a coordination game with multiple equilibria. Conversely, the threshold `1e-12` is fragile for floating-point matrices derived from integer counts that happen to be equal. The check is correct for its stated purpose (all payoffs identical) but the variable name and comment could mislead someone into thinking it detects broader classes of trivial games.

4. **Assumption that `best_responses` dict from nashopt uses integer indices** (`solver.py:417-419`). The code tries both `result.best_responses.get(idx, ...)` and `result.best_responses.get(name, 0)` as fallback. But the spec's API shows `best_responses: dict[agent, action]` where "agent" is unspecified. The double-lookup is defensive but if nashopt returns agent indices as keys (likely, since it receives arrays not named agents), the fallback to `name` will never match and all agents will get best_response=0. The mapping from nashopt's integer agent indices to agent names needs to be explicit, not speculative.

---

## Actionable Recommendations

### P1 — Correctness (must fix before merge)

1. **Fix winner-take-all payoff matrix shape** (`solver.py:148-176`). Reformulate as an N x N matrix. For WTA, entry (i, j) should represent i's payoff when competing against j: winner gets 1.0, loser gets `1.0 - position_penalty`. Or alternatively, if nashopt supports asymmetric/non-standard game forms, document the exact expected tensor shape and add a converter.

2. **Fix red-blue agent-to-row mapping** (`solver.py:222-287` and `solver.py:416-424`). Either (a) pass the 2-player matrix to nashopt and then map the 2-player result back to individual agents by role, or (b) build an N x N matrix where red-red and blue-blue interactions are encoded. The current code will produce index-out-of-range or misattribution bugs when nashopt returns best_responses for 2 players but the code iterates over N agents.

3. **Ensure strategy profile dimensions match action space** (`solver.py:294-326, 397-398`). Add a validation step after `build_strategy_profile` that pads or truncates each agent's strategy vector to match the number of columns in the payoff matrix. Or, better, derive the strategy representation from the same action space used to build the payoff matrix rather than using a generic 4-element fallback.

4. **Fix ThreadPoolExecutor blocking on `__exit__`** (`scorer.py:137-142`). Replace `with ThreadPoolExecutor(...)` with a non-blocking pattern. Create the executor outside the `with` block, use `future.result(timeout=timeout)`, and on timeout call `executor.shutdown(wait=False, cancel_futures=True)` (Python 3.9+). Alternatively, use `multiprocessing` or `signal.alarm` (Unix) to actually terminate runaway JAX computations. At minimum, add `cancel_futures=True` to `shutdown()`.

5. **Derive per-agent equilibrium deviation from best_responses** (`solver.py:426-438`). Instead of falling back to "all agents not at equilibrium," compare each agent's current strategy (from `build_strategy_profile`) against its best response action index. An agent is not at equilibrium if its current strategy places nonzero weight on non-best-response actions. This requires carrying the strategy profile through to the post-processing step.

### P2 — Numerical Quality (should fix)

6. **Normalize payoff matrices before passing to nashopt** (`solver.py:382-383`). After constructing the raw matrix, normalize to [0, 1] by dividing by the matrix's max absolute value (with a zero guard). This ensures nashopt's distance metric is scale-invariant and scores are comparable across modes and deliberation sizes.

7. **Populate per-agent payoff data from solver path** (`scorer.py:157-187`). Compute each agent's actual payoff from the payoff matrix (the row corresponding to that agent, evaluated at the current strategy profile). This makes the solver path's output informationally equivalent to the heuristic path and lets downstream consumers display gap-to-best-response regardless of which solver ran.

8. **Add a score reconciliation mechanism** (`scorer.py:270-288`). When the solver result is available, also run the heuristic and log a comparison. This provides an ongoing calibration check and alerts if the two paths diverge significantly, catching both heuristic drift and solver integration bugs.

### P3 — Robustness (nice to have)

9. **Add asymmetric agreement matrix handling** (`solver.py:128-133`). Before the lookup loop, symmetrize the agreement matrix: for each (i, j) pair, use `max(matrix[i][j], matrix[j][i])` or raise if the matrix is unexpectedly one-directional. Add a test with a triangular agreement matrix.

10. **Add integration test with a known-equilibrium game** (`test_solver.py`). The current tests mock nashopt entirely. Add at least one test that constructs a 2x2 game with a known Nash equilibrium (e.g., Prisoners' Dilemma: `[[3,0],[5,1]]` / `[[3,5],[0,1]]`) and verifies that the full pipeline (matrix construction, nashopt call, result parsing) produces the expected score. This requires nashopt to be an optional test dependency; skip if not installed.

---

## Referenced Documentation

| Document | Location | Relevance |
|----------|----------|-----------|
| Spec 021 | `conversus/specs/done/021-nashopt-integration/spec.md` | Primary spec defining all FRs and the nashopt API surface |
| Solver wrapper | `conversus/conversus/plugins/nashopt/solver.py` | Core implementation under review |
| Scorer plugin | `conversus/conversus/plugins/nashopt/scorer.py` | Dispatch logic, timeout, heuristic fallback |
| Heuristic payoffs | `conversus/conversus/plugins/nashopt/payoffs.py` | Pre-021 heuristic path (must remain unchanged) |
| Feature schema | `conversus/conversus/schemas/features.py` | Data model for `RoundFeatures`, `AgentFeatures` |
| Plugin base | `conversus/conversus/plugins/base.py` | `Plugin`, `PluginResult`, `DeliberationState` definitions |
| Test suite | `conversus/tests/test_solver.py` | Coverage of all FRs, mock-based nashopt tests |
| Python `concurrent.futures` docs | https://docs.python.org/3/library/concurrent.futures.html | ThreadPoolExecutor shutdown semantics |
| Spec 017 | Referenced as dependency | Original heuristic scorer spec |
| Spec 015 | Referenced as dependency | Feature extraction spec |
