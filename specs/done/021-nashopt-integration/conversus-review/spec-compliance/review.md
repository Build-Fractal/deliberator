# Spec Compliance Review — 021-nashopt-integration

**Reviewer Role**: spec-compliance
**Date**: 2026-04-01
**Files Reviewed**:
- `conversus/plugins/nashopt/solver.py`
- `conversus/plugins/nashopt/scorer.py`
- `tests/test_solver.py`
- `specs/done/021-nashopt-integration/spec.md`

---

## Executive Summary

The implementation is broadly aligned with the spec. All eight functional requirements (FR-001 through FR-008) have corresponding code paths, and all four success criteria (SC-001 through SC-004) are at least partially addressed. The solver wrapper, scorer dispatch, heuristic fallback, timeout mechanism, and degenerate-case handling are structurally sound. The primary gaps are: (1) SC-001 and SC-002 lack dedicated tests that assert the specific score thresholds the spec demands, (2) the timeout mechanism in `_try_solver` catches `concurrent.futures.TimeoutError` but the test mocks a side_effect rather than exercising the actual timeout path, and (3) FR-005 best-response reporting degrades to "all agents not at equilibrium" when the nashopt result object lacks a per-agent breakdown, which is a silent accuracy loss. No spec violations were found — all issues are completeness gaps, not contradictions.

---

## Alignment

### FR-001: Use nashopt.check_equilibrium() when importable — **MET**

**Evidence**: `solver.py` lines 31-39 conditionally import `nashopt` and set `HAS_NASHOPT = True`. `scorer.py` line 134 checks `HAS_NASHOPT` in `_try_solver()` and dispatches to `check_equilibrium_nashopt()` at line 142. `scorer.py` line 283 calls `_try_solver()` before falling back. Tests `TestMockNashoptIntegration.test_solver_path_at_equilibrium` (line 683) and `test_solver_called_with_correct_args` (line 776) verify the dispatch path with mocked nashopt.

### FR-002: Fall back to heuristic when nashopt is not importable — **MET**

**Evidence**: `scorer.py` lines 134-135 return `None` from `_try_solver` when `HAS_NASHOPT is False`, causing line 288 to call `_compute_equilibrium_score_heuristic()`. Test `TestScorerHeuristicFallback.test_uses_heuristic_when_no_nashopt` (line 560) confirms `solver == "heuristic"` when nashopt is absent. `TestHasNashoptFlag.test_flag_false_in_test_env` (line 264) confirms the flag is False in the test environment.

### FR-003: Construct per-mode payoff matrices from FeatureSet data — **MET**

**Evidence**: `solver.py` function `build_payoff_matrix()` (line 70) dispatches to four mode-specific builders: `_build_cooperative_matrix` (line 107), `_build_wta_matrix` (line 148), `_build_pd_matrix` (line 179), `_build_rb_matrix` (line 222). Each follows the matrix structure documented in the spec's Section 2 table. Tests cover all four modes: `TestBuildPayoffMatrixCooperative`, `TestBuildPayoffMatrixWTA`, `TestBuildPayoffMatrixPD`, `TestBuildPayoffMatrixRB`.

### FR-004: Normalize equilibrium distance to 0.0-1.0 score — **MET**

**Evidence**: `solver.py` lines 407-410 compute `distance = max(0.0, min(1.0, raw_distance))` and `score = 1.0 - distance`, matching the spec formula exactly. Tests `test_distance_clamped_to_one` (line 954) and `test_negative_distance_clamped_to_zero` (line 984) verify boundary clamping.

### FR-005: Report which agents are NOT at best response — **PARTIALLY MET**

**Evidence**: `solver.py` lines 413-438 build `agents_not_at_equilibrium`. When the nashopt result provides `agents_not_at_equilibrium`, it is consumed (lines 429-434). When it does not, the code falls back to listing all agents if distance > 0 (line 438). The `SolverResult` dataclass includes the field (line 63), and `scorer.py` lines 165-166 use it in `_score_from_solver`. Tests `test_solver_path_per_agent_data` (line 736) and `test_not_at_equilibrium` (line 871) verify the field is populated.

**Gap**: The fallback at line 438 ("assume all agents may not be at best response") is a lossy heuristic. The spec says the solver "MUST report which agents are NOT at their best response." If nashopt's result object does not provide per-agent equilibrium status, the implementation over-reports rather than accurately computing from the best-response map. The `best_responses` dict from nashopt is already available at line 416-419 but is not used to derive per-agent equilibrium status by comparing each agent's current strategy against its best response.

### FR-006: Handle degenerate cases — **MET**

**Evidence**: `solver.py` lines 362-394 handle three degenerate cases: zero agents (returns trivial equilibrium), single agent (returns trivial equilibrium), and zero-variance payoff matrix (returns trivial equilibrium). Tests in `TestDegenerateCases` (line 521) cover empty and single-agent matrix construction. `TestCheckEquilibriumNashoptMocked` tests `test_single_agent_degenerate` (line 905), `test_empty_agents_degenerate` (line 916), and `test_zero_variance_degenerate` (line 928).

### FR-007: Configurable timeout with heuristic fallback — **MET**

**Evidence**: `scorer.py` line 53 defines `_DEFAULT_SOLVER_TIMEOUT = 30.0`. `_try_solver` (line 124) wraps the solver call in `concurrent.futures.ThreadPoolExecutor` with `future.result(timeout=timeout)` at line 142. Timeout is read from config at line 280: `config.get("solver_timeout", _DEFAULT_SOLVER_TIMEOUT)`. `TimeoutError` is caught at line 143, logging a warning and returning `None` to trigger fallback. Test `test_timeout_falls_back_to_heuristic` (line 623) verifies the fallback, though via mock side_effect rather than actual timeout.

### FR-008: PluginResult.data includes solver field — **MET**

**Evidence**: `scorer.py` line 184 sets `"solver": "nashopt"` in `_score_from_solver()`. Line 213 sets `"solver": "heuristic"` in `_compute_equilibrium_score_heuristic()`. Tests in `TestSolverFieldInResult` (line 585) verify the field is present, is a string, and contains valid values. `test_all_modes_have_solver_field` (line 606) checks across all four modes.

### SC-001: Cooperative convergence produces score >= 0.9 — **NOT MET** (no test)

**Evidence**: No test asserts that a cooperative deliberation where all agents converge produces a solver score >= 0.9. The mock integration tests (`test_solver_path_at_equilibrium`, line 683) hard-code `score=1.0` into the mock return value, which does not exercise the scoring formula against realistic converged features. A proper SC-001 test would construct features representing full convergence and assert the computed score exceeds 0.9.

### SC-002: 3+ unresolved disputes produces score < 0.5 — **NOT MET** (no test)

**Evidence**: No test constructs a scenario with 3+ unresolved disputes and asserts the solver or heuristic produces a score below 0.5. The existing tests do not parametrize dispute counts to validate this threshold behavior.

### SC-003: With nashopt uninstalled, behavior identical to current heuristic — **MET**

**Evidence**: `TestScorerHeuristicFallback` (line 559) and `TestBackwardCompatibility` (line 1020) collectively verify that without nashopt, the scorer produces valid scores, returns `PluginResult`, sets `advisory=True`, includes all required fields, and handles edge cases. `TestHasNashoptFlag.test_flag_false_in_test_env` (line 264) confirms nashopt is not present in the test environment, meaning every non-mocked scorer test exercises the heuristic path.

### SC-004: Solver timeout produces heuristic fallback, not error — **MET**

**Evidence**: `TestTimeoutFallback.test_timeout_falls_back_to_heuristic` (line 623) mocks a `TimeoutError` and verifies `result.data["solver"] == "heuristic"` and `isinstance(result.data["score"], float)`. `test_solver_exception_falls_back_to_heuristic` (line 642) verifies that a `RuntimeError` from the solver also falls back cleanly. Neither test results in an unhandled error.

---

## Missed Opportunities

1. **No real-timeout integration test.** The timeout test (line 623) uses `side_effect` to raise `TimeoutError` immediately. It never exercises the actual `ThreadPoolExecutor` timeout mechanism with a blocking callable, leaving the real timeout path untested.

2. **No SC-001/SC-002 threshold tests.** The spec defines two concrete acceptance thresholds (>= 0.9 for convergence, < 0.5 for disputes). Neither has a corresponding test that feeds realistic feature data through the actual scoring formula and asserts against the threshold.

3. **Best-response derivation from solver output.** The `best_responses` dict returned by nashopt (line 416-419) could be compared against each agent's current strategy to accurately determine which agents deviate, rather than the blanket fallback at line 438.

4. **No validation that `FeatureSet` (as named in FR-003) is the input.** The spec says "per-mode payoff matrices from FeatureSet data." The implementation uses `RoundFeatures`, which is a sub-model of `FeatureSet`. This is correct in practice but the naming mismatch is not documented.

5. **`_score_from_solver` sets `payoff: 0.0` for all agents.** At `scorer.py` line 173, per-agent payoff is hardcoded to `0.0` with a comment "Detailed payoffs not available from solver." This information loss means consumers comparing heuristic vs. solver results see different data shapes.

---

## Off-Base Assumptions

1. **Assumption that nashopt returns `agents_not_at_equilibrium` attribute.** The spec's nashopt API surface (Section 2) shows only `is_equilibrium`, `distance`, and `best_responses`. The code at `solver.py` line 429 checks `hasattr(result, "agents_not_at_equilibrium")` -- this field is not in the documented API. The fallback covers this, but the code structure suggests the implementer expected a richer API than specified.

2. **Assumption that `result.best_responses` keys may be either ints or strings.** Line 418 tries `result.best_responses.get(idx, result.best_responses.get(name, 0))`. The spec documents `dict[agent, action]` without clarifying whether agent is an index or name. The dual-lookup is defensive but undocumented.

3. **ThreadPoolExecutor for timeout.** The spec says "capped at a configurable timeout." The implementation uses a thread pool, which means a timed-out solver thread continues running in the background after fallback. For a JAX-based solver that may hold GPU resources, this could cause resource leakage. The spec does not address cancellation semantics.

---

## Actionable Recommendations

### P1 — Must fix before ship

1. **Add SC-001 test: cooperative convergence score >= 0.9.** Create a test that constructs `RoundFeatures` with high surviving counts, zero disputes, full agreement matrix, and either (a) mocks nashopt to return a realistic low distance, or (b) runs through the heuristic path with converged features. Assert `score >= 0.9`. Without this, the spec's primary acceptance criterion is unverified.

2. **Add SC-002 test: 3+ disputes score < 0.5.** Create a test with `dispute_count >= 3`, low surviving counts, and no agreement. Assert `score < 0.5` for both solver and heuristic paths. This is the spec's negative-case acceptance criterion.

3. **Improve FR-005 agent-not-at-equilibrium accuracy.** In `check_equilibrium_nashopt()` lines 426-438, when the nashopt result lacks `agents_not_at_equilibrium` but provides `best_responses`, compare each agent's best response action against their current strategy to determine which agents deviate. The current blanket "all agents" fallback violates the precision requirement of FR-005.

### P2 — Should fix

4. **Add a real-timeout integration test.** Replace or supplement the mock-based timeout test with one that submits a `time.sleep(10)` callable to `_try_solver` with a 0.1s timeout, verifying the actual `ThreadPoolExecutor` timeout mechanism fires and fallback occurs.

5. **Document the per-agent payoff gap in solver path.** At `scorer.py` line 173, `payoff: 0.0` is a data fidelity loss. Either (a) extract per-agent payoffs from the payoff matrix used for the solver call, or (b) add a `"note"` field indicating payoffs are not available from the solver path, so consumers do not silently consume zero values.

6. **Align `solver.py` with spec API surface.** The spec (Section 2) documents `result.best_responses` as `dict[agent, action]`. The code at line 418 does a dual int/str lookup. Pin down whether nashopt uses int indices or string names and simplify accordingly, or add a comment explaining the defensive lookup rationale.

### P3 — Nice to have

7. **Add cancellation for timed-out solver threads.** When `_try_solver` times out, the solver thread continues executing. Consider using `concurrent.futures.Future.cancel()` or a threading event to signal the solver to abort, preventing resource leakage with JAX/GPU workloads.

8. **Parametrize mode-specific matrix tests.** The four `TestBuildPayoffMatrix*` classes share structural assertions (shape, value types, non-negative values). A parametrized test across all modes would reduce duplication and make it easier to add new modes.

9. **Add test for `build_payoff_matrix` with unknown mode.** While `TestBuildPayoffMatrixUnknownMode` (line 445) covers the ValueError, add a test that verifies the error message includes the available modes list, ensuring the user gets actionable feedback.

10. **Verify `SolverResult.score` rounding consistency.** `check_equilibrium_nashopt` rounds score to 4 decimal places (line 445: `round(score, 4)`) and distance to 6 (line 444: `round(distance, 6)`). The heuristic path also rounds to 4 (scorer.py line 256). Document this precision choice or make it configurable to avoid surprising consumers who compare across paths.

---

## Referenced Documentation

| Document | Location | Relevance |
|----------|----------|-----------|
| Spec 021 (nashopt integration) | `specs/done/021-nashopt-integration/spec.md` | Primary specification under review |
| Solver wrapper | `conversus/plugins/nashopt/solver.py` | Core implementation: payoff matrix construction, nashopt dispatch, degenerate handling |
| Scorer plugin | `conversus/plugins/nashopt/scorer.py` | Integration layer: timeout, fallback dispatch, PluginResult construction |
| Test suite | `tests/test_solver.py` | 1063-line test file covering FR-001 through FR-008 and SC-003/SC-004 |
| Feature schemas | `conversus/schemas/features.py` | Data models: `AgentFeatures`, `RoundFeatures`, `FeatureSet` |
