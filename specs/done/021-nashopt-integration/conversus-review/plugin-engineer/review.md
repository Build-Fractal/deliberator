# Plugin Engineer Review — Spec 021: nashopt Solver Integration

**Reviewer**: plugin-engineer
**Date**: 2026-04-01
**Scope**: Plugin architecture correctness, flag patterns, dispatch logic, backward compatibility, import safety

---

## Executive Summary

The nashopt solver integration is architecturally sound. The `HAS_NASHOPT` flag pattern, the solver-to-heuristic dispatch, and the `PluginResult.data["solver"]` contract are implemented correctly for the happy path and the primary fallback scenarios. The design preserves full backward compatibility with spec 017 -- when nashopt is absent, behavior is byte-identical to the pre-021 heuristic path. Import guards are properly structured behind a single `try/except ImportError` block. However, there are several issues worth addressing: the `solver` key is missing from two error-path `PluginResult` returns, there is an unused variable in the red-blue matrix builder, the timeout test does not actually exercise the `concurrent.futures` timeout mechanism, and the cooperative matrix builder has a semantic inconsistency between diagonal (self-payoff from surviving count) and off-diagonal (agreement matrix entry that also includes self-pair). These are catalogued below as actionable recommendations.

---

## Alignment

### What spec 021 requires and what the implementation delivers

| Spec Requirement | Status | Notes |
|---|---|---|
| FR-001: Use `nashopt.check_equilibrium()` when importable | PASS | `_try_solver` dispatches to `check_equilibrium_nashopt()` when `HAS_NASHOPT is True` |
| FR-002: Fall back to heuristic when not importable | PASS | `_try_solver` returns `None`, `_compute_equilibrium_score` falls through to heuristic |
| FR-003: Per-mode payoff matrices from FeatureSet data | PASS | `build_payoff_matrix()` dispatches to four mode-specific builders |
| FR-004: Normalize distance to 0.0-1.0 score | PASS | `max(0.0, min(1.0, raw_distance))` then `1.0 - distance` |
| FR-005: Report agents not at best response | PASS | `agents_not_at_equilibrium` populated from nashopt result or heuristic |
| FR-006: Handle degenerate cases | PASS | 0-agent, 1-agent, zero-variance all handled before nashopt call |
| FR-007: Configurable timeout with heuristic fallback | PASS | `concurrent.futures.ThreadPoolExecutor` with `future.result(timeout=)` |
| FR-008: `PluginResult.data["solver"]` always populated | PARTIAL | Missing on two error-path returns (see P1-1 below) |

### Backward compatibility with spec 017

The implementation preserves all spec 017 guarantees:
- Plugin name remains `equilibrium-scorer`
- Hooks remain `[POST_PHASE_5, POST_DELIBERATION]`
- Output format includes all FR-007 fields from spec 017 (`score`, `agents_at_equilibrium`, `total_agents`, `per_agent`, `mode`, `round`, `hook`)
- The heuristic path is functionally unchanged -- same `compute_payoff()` dispatcher, same per-agent equilibrium check logic
- `advisory=True` on all returns
- The `solver` key is additive, not breaking

---

## Missed Opportunities

1. **No integration test with real nashopt**. All solver-path tests use mocks. This is defensible for CI (no JAX dependency), but the spec states the solver wrapper "must be independently testable with mock payoff matrices" (Constraints, bullet 4). A conftest fixture that conditionally skips when nashopt is unavailable (`pytest.importorskip("nashopt")`) would give confidence that the actual API contract matches the mock contract.

2. **Payoff matrix builders return plain lists but are never tested against the actual numpy conversion**. The `check_equilibrium_nashopt()` function calls `np.array(raw_matrix, dtype=np.float64)` -- if a mode builder returns a ragged matrix (e.g., red-blue returns `[[a, b, c], [d, e, f]]` for 2 rows but other modes return NxN), the numpy conversion may produce unexpected shapes. The spec's matrix structure table (Section 2) implies heterogeneous shapes per mode, but nashopt's `check_equilibrium()` signature is not validated against these shapes.

3. **No metric or log for solver vs. heuristic path selection**. The `solver` field in `PluginResult.data` records the outcome, but there is no structured logging at INFO level when the solver is selected. This makes debugging in production harder -- you only see warnings on failure.

4. **`_score_from_solver` hardcodes `payoff: 0.0` and `best_response_payoff: 0.0` for all agents**. The comment says "Detailed payoffs not available from solver" but nashopt's result object may provide these. This means consumers comparing heuristic vs. solver output get different per-agent data structures, which could break downstream analytics.

---

## Off-Base Assumptions

1. **The timeout test (`TestTimeoutFallback.test_timeout_falls_back_to_heuristic`) does not actually test the timeout mechanism**. It patches `check_equilibrium_nashopt` to raise `concurrent.futures.TimeoutError` directly, but the real code path wraps the call in `ThreadPoolExecutor` and catches `concurrent.futures.TimeoutError` from `future.result(timeout=)`. The mock bypasses the thread pool entirely. Because `_try_solver` catches `Exception` broadly after the `TimeoutError` catch, the test passes, but it is testing the wrong code path -- it tests that `_try_solver` catches exceptions from the solver function, not that it catches timeouts from the futures executor. The mock raises `TimeoutError` inside the submitted function, not from `future.result()`.

2. **The cooperative matrix builder uses surviving_count for diagonal entries even when an agreement_matrix is provided**. The agreement_matrix may contain a self-pair entry (`agent-a -> agent-a`), but the builder always uses `surviving_count` for `i == j`. The test `test_with_agreement_matrix` asserts `matrix[0][0] == 4.0` (surviving_count) rather than the agreement_matrix value of 1. This is internally consistent but may not match the game-theoretic semantics where the agreement matrix should be the authoritative payoff source.

3. **The `_build_rb_matrix` function computes `total_surface` in the `max_k == 0` branch but never uses it** -- `red_payoff` and `blue_payoff` are derived directly from `landed_attack_count` and `mitigated_attack_count` without dividing by `total_surface`. This is a dead variable.

---

## Actionable Recommendations

### P1 — Must Fix

**P1-1: `PluginResult.data["solver"]` is NOT always populated (FR-008 violation)**

Two early-return paths in `EquilibriumScorer.execute()` produce `PluginResult` without a `solver` key:
- Line 371-378: Unknown mode error path returns `data={"error": ...}` -- no `solver` key.
- Line 394-401: Computation failure error path returns `data={"error": ...}` -- no `solver` key.

Spec 021 FR-008 states: "The `PluginResult.data` dict MUST include `solver: 'nashopt'` (or `solver: 'heuristic'`) so consumers know which path ran."

Consumers that unconditionally access `result.data["solver"]` will get a `KeyError` on these paths. Fix: add `"solver": "unavailable"` (or `"solver": "error"`) to both error-path data dicts.

**P1-2: Fix the timeout test to actually exercise the timeout mechanism**

The current mock patches the solver function to raise `TimeoutError` directly. The real timeout comes from `future.result(timeout=)`, not from inside the submitted callable. Write a test that patches `check_equilibrium_nashopt` to sleep longer than the timeout, and verify that `_try_solver` returns `None` and the scorer falls back to heuristic. This requires the mock to actually block (e.g., `time.sleep(5)` with a 0.01s timeout).

**P1-3: Remove the dead `total_surface` variable in `_build_rb_matrix` (lines 255-259)**

In the `max_k == 0` branch of `_build_rb_matrix`, `total_surface` is computed but never used. The `red_payoff` and `blue_payoff` are assigned directly from `features.landed_attack_count` and `features.mitigated_attack_count`. Either remove the dead variable or use it to normalize the payoffs (which may be the intended behavior -- see the `max_k > 0` branch where ratios are used).

### P2 — Should Fix

**P2-1: Add `solver` field to heuristic per_agent data for output parity**

The heuristic path's `per_agent` dict contains `payoff` and `best_response_payoff` with real values. The solver path's `per_agent` dict hardcodes both to `0.0` with an additional `best_response_action` key. This asymmetry means downstream consumers cannot treat the two paths uniformly. Either populate real values from the solver (if nashopt provides them) or document the zero-value contract explicitly.

**P2-2: Add a `pytest.importorskip` conditional integration test**

Add a test class guarded by `@pytest.mark.skipif(not HAS_NASHOPT, reason="nashopt not installed")` that exercises `check_equilibrium_nashopt` with real (small) payoff matrices. This validates that the mock contract matches the real nashopt API.

**P2-3: Add INFO-level log line when solver path is selected**

In `_try_solver`, after a successful solver call, log at INFO: `"nashopt solver returned in %.2fs (distance=%.4f)"`. This aids production debugging without requiring inspection of the PluginResult.

### P3 — Consider

**P3-1: Validate payoff matrix shape before passing to nashopt**

`check_equilibrium_nashopt` passes the raw numpy array directly to `nashopt.check_equilibrium()` without validating that the shape is compatible with the strategy profile. Different modes produce different matrix shapes (NxN, Nx1, 2xK). If nashopt expects a specific shape, a shape mismatch will produce an opaque error from inside nashopt/JAX. A pre-call shape assertion (e.g., matrix shape vs. strategy profile length) would surface the error earlier with a clear message.

**P3-2: Consider whether cooperative diagonal should use agreement_matrix self-pair**

The `_build_cooperative_matrix` builder unconditionally uses `surviving_count` for diagonal entries, even when `agreement_matrix` is provided and contains self-pair data. If the agreement_matrix is meant to be authoritative, the diagonal should come from it too. If surviving_count is intentionally preferred for diagonal, add a comment explaining why.

**P3-3: Normalize red-blue fallback payoffs like the severity-vector path**

The `max_k == 0` branch in `_build_rb_matrix` returns raw counts (`landed_attack_count`, `mitigated_attack_count`) while the `max_k > 0` branch returns severity-weighted ratios. This scale difference could affect nashopt's equilibrium computation. Consider normalizing both branches consistently.

---

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/specs/done/021-nashopt-integration/spec.md` -- Spec 021 (target spec)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/done/017-equilibrium-scorer/spec.md` -- Spec 017 (backward compatibility baseline)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/plugins/nashopt/solver.py` -- Solver wrapper
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/plugins/nashopt/scorer.py` -- Scorer plugin (dispatch logic)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/plugins/nashopt/payoffs.py` -- Heuristic payoff functions (spec 017)
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/plugins/nashopt/__init__.py` -- Package exports
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/plugins/base.py` -- Plugin base class, PluginResult
- `/Users/business-daddy/code/payer-index-mono/conversus/conversus/schemas/features.py` -- RoundFeatures, AgentFeatures
- `/Users/business-daddy/code/payer-index-mono/conversus/tests/test_solver.py` -- Test suite
