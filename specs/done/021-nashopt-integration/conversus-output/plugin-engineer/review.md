# Phase 1 Review: plugin-engineer

**Spec**: 021-nashopt-integration
**Reviewer**: plugin-engineer
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: Plugin dispatch pattern, HAS_NASHOPT flag, backward compatibility, integration with plugin system

---

## Executive Summary

The plugin integration layer is well-designed. The HAS_NASHOPT flag pattern follows the established precedent from other optional-dependency plugins (HAS_AMPL in spec 023, scipy in spec 022). The heuristic fallback path is preserved with no behavioral change. The `solver` field in PluginResult.data correctly identifies which path ran. However, there are two concerns: (1) the scorer.py dispatch logic (which bridges the heuristic and nashopt paths) is not included in the review artifacts, making it impossible to verify FR-001/FR-002 dispatch correctness from solver.py alone, and (2) the HAS_NASHOPT flag imports both `nashopt` and `numpy` in a single try block, meaning a broken numpy installation would disable nashopt even if nashopt itself is importable.

---

## HAS_NASHOPT Flag (FR-001, FR-002)

### Design

The flag is set at module import time via a try/except block:

```python
try:
    import nashopt as _nashopt
    import numpy as _np
    nashopt = _nashopt
    np = _np
    HAS_NASHOPT = True
except ImportError:
    pass
```

This is the correct pattern. Module-level imports with a flag enable O(1) dispatch at call time (no repeated import attempts). The flag is a plain bool, which is the simplest correct approach.

### Concern: Coupled Imports

The try block imports both `nashopt` and `numpy` together. If numpy is installed but broken (e.g., linked against a missing BLAS library), the ImportError will set `HAS_NASHOPT = False` even though nashopt itself may be fine. Conversely, if nashopt is installed but numpy is not, the same thing happens. Since nashopt depends on numpy transitively (via JAX), the coupling is pragmatically acceptable -- you cannot use nashopt without numpy. But a more informative pattern would catch the imports separately and log which dependency is missing:

```python
try:
    import numpy as _np
except ImportError:
    _np = None
try:
    import nashopt as _nashopt
except ImportError:
    _nashopt = None
HAS_NASHOPT = _np is not None and _nashopt is not None
```

This is a minor improvement that aids debugging when dependencies are partially installed.

### Backward Compatibility

When `HAS_NASHOPT is False`, the solver module exposes only the flag and the pure-Python functions (`build_payoff_matrix`, `build_strategy_profile`, `SolverResult`). The `check_equilibrium_nashopt()` function raises `RuntimeError` if called without nashopt. This is correct -- callers should check the flag before calling. The existing heuristic path in scorer.py is completely untouched.

---

## Plugin Dispatch Pattern

### Architecture

The dispatch follows the standard conversus plugin pattern:
1. EquilibriumScorer plugin checks `HAS_NASHOPT`.
2. If True, calls `check_equilibrium_nashopt()` with a timeout wrapper.
3. If False (or timeout), falls back to the heuristic scorer.
4. PluginResult.data includes `solver: "nashopt"` or `solver: "heuristic"`.

This is the same pattern used by ConfigOptimizer (HAS_AMPL) and ConvergencePredictor (Kalman vs OLS). Consistency across plugins is a strength.

### Gap: Scorer Dispatch Not in Review Artifacts

The spec lists `conversus/plugins/nashopt/solver.py` as a target file but not `scorer.py`, which is where the dispatch logic lives. From solver.py alone, I can verify:
- `HAS_NASHOPT` is correctly set.
- `check_equilibrium_nashopt()` raises on missing dependency.
- `SolverResult` is properly structured.
- Payoff matrix construction is pure and testable.

But I cannot verify:
- That the scorer actually checks HAS_NASHOPT before calling the solver.
- That the timeout wrapper is implemented correctly.
- That the heuristic fallback is invoked on timeout.
- That the `solver` field is set correctly in PluginResult.data.

The test file (test_solver.py) includes tests for scorer dispatch and the `solver` field, which provides indirect evidence of correct implementation. But the code-level review is incomplete without scorer.py.

---

## SolverResult Structure

The dataclass is well-designed:
- `frozen=True` prevents mutation after creation.
- All fields have explicit types.
- `agents_not_at_equilibrium` is a list[str] (agent names), not a list[int] (indices), which is consumer-friendly.
- `best_responses` maps agent names to action indices.

The separation between `distance` (raw metric) and `score` (derived, consumer-facing) is clean. Consumers use `score`; advanced users can inspect `distance` and `best_responses`.

---

## FR-008: solver Field in PluginResult.data

The spec requires `PluginResult.data` to include `solver: "nashopt"` or `solver: "heuristic"`. The solver.py module does not set this field (it returns SolverResult, not PluginResult). The field must be set by the scorer plugin when constructing the PluginResult. The test file verifies this:

```python
def test_solver_field_grid_search(self, basic_state):
    plugin = EquilibriumScorer(plugin_config={})
    result = plugin.execute(basic_state)
    assert result.data["solver"] == "heuristic"
```

This is correctly delegated to the plugin layer. solver.py is a pure computation module; it should not be concerned with plugin result formatting.

---

## Test Coverage Assessment

The test file is thorough:
- Payoff matrix tests for all 4 modes with shape, value, and edge case checks.
- Strategy profile tests with position vectors, derived metrics, empty features, and zero vectors.
- Degenerate case tests for single agent, zero agents, and zero-variance matrices.
- SolverResult frozen-dataclass tests.
- HAS_NASHOPT flag tests.
- Mock nashopt integration tests.
- Scorer dispatch tests with patched HAS_NASHOPT.
- Timeout fallback tests.

The test design correctly uses `unittest.mock` for nashopt (which is not installed in CI) and direct calls for pure-Python functions. This is the right testing strategy for optional-dependency modules.

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Include scorer.py in the review artifacts. The dispatch logic is the most critical part of the integration and cannot be verified from solver.py alone.

### P2 (Should Fix)

2. **P2-1**: Separate the nashopt and numpy imports in the try block. Log which dependency is missing to aid debugging.

3. **P2-2**: Add a `__all__` export list to solver.py to make the public API explicit: `__all__ = ["HAS_NASHOPT", "SolverResult", "build_payoff_matrix", "build_strategy_profile", "check_equilibrium_nashopt"]`.

### P3 (Consider)

4. **P3-1**: Add type annotations for the module-level `nashopt` and `np` variables. Currently they are typed as `Any`, which is correct but loses IDE support. A `TYPE_CHECKING` block could provide better hints.
