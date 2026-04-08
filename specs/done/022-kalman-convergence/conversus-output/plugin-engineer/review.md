# Phase 1 Review: plugin-engineer

**Spec**: 022-kalman-convergence
**Reviewer**: plugin-engineer
**Date**: 2026-04-01
**Phase**: 1 (Initial Review)
**Perspective**: Integration with predictor plugin, method dispatch, backward compatibility with OLS

---

## Executive Summary

The Kalman integration with the convergence predictor plugin is well-structured. The `predict_convergence()` function provides a clean dispatch API with `method` parameter supporting `"auto"`, `"kalman"`, and `"ols"`. The auto-dispatch logic (Kalman when 2+ rounds, OLS otherwise) is sensible. The OLS fallback is fully preserved with no behavioral change. The `method` field in ConvergencePrediction correctly identifies which path ran. The Q/R configurability via function parameters satisfies FR-007. However, there are two concerns: (1) the Kalman path silently catches all exceptions and falls back to OLS, which could mask bugs during development, and (2) the `confidence_bounds` field is Kalman-only but part of the shared ConvergencePrediction dataclass, which could confuse consumers who always expect it.

---

## Method Dispatch (FR-001, FR-002)

### Design

```python
def predict_convergence(..., method="auto", Q=None, R=None):
    if method == "kalman":
        use_kalman = True
    elif method == "auto" and num_rounds >= 2:
        use_kalman = True
    # else: OLS
```

The dispatch logic is clear and correct. Auto-mode uses Kalman when there are 2+ rounds (minimum for meaningful Kalman updates) and OLS otherwise. Explicit `method="ols"` always uses OLS. Explicit `method="kalman"` always uses Kalman (even with 1 round, though this would produce high-uncertainty results).

The fallback on exception is:

```python
try:
    return _predict_convergence_kalman(...)
except Exception as exc:
    logger.warning("Kalman prediction failed (%s), falling back to OLS.", exc)
```

### Concern: Broad Exception Catch

Catching all exceptions is correct for production robustness (the predictor should never crash), but during development it masks bugs. A `TypeError` from a bad argument or a `ValueError` from invalid data would be silently swallowed. Consider catching specific expected exceptions (ValueError for bad data, ArithmeticError for matrix singularity) and re-raising unexpected ones during development via an environment flag or log level check.

---

## Backward Compatibility with OLS

### OLS Path Preservation

The `_predict_convergence_ols()` function is the original spec 018 implementation, extracted into a named function. All OLS logic (trend computation, confidence calculation, prediction classification) is unchanged. The only structural change is that it is now called via dispatch rather than being the sole path.

### ConvergencePrediction Dataclass Extension

The dataclass gained two new fields for the Kalman path:
- `method: str = "ols"` (default preserves backward compatibility)
- `confidence_bounds: tuple[float, float] | None = None` (optional, Kalman-only)

The defaults ensure that existing consumers of OLS results see no behavioral change. The `method` field defaults to `"ols"`, so any prediction not explicitly tagged is backward-compatible.

### Concern: confidence_bounds Semantics

When `method="ols"`, `confidence_bounds` is `None`. Consumers who access `result.confidence_bounds` without checking `method` will get `None` and must handle it. This is acceptable (Optional types require None checks), but the docstring should be clearer about when confidence_bounds is populated vs. None.

---

## Q/R Configurability (FR-007)

The `Q` and `R` parameters are threaded from `predict_convergence()` through to `_predict_convergence_kalman()` and into `run_kalman_filter()`. Default values are provided by `default_Q()` and `default_R()`. The parameter path is:

```
predict_convergence(Q=user_Q) ->
  _predict_convergence_kalman(Q=user_Q) ->
    run_kalman_filter(observations, Q=user_Q) ->
      kalman_update(prior, obs, Q=user_Q)
```

This is correct. Users can tune noise parameters via plugin config without modifying code.

---

## FR-008: Cost Estimation via Kalman

The spec requires that cost estimation use the Kalman model's predicted rounds remaining, not the linear estimate. The implementation computes rounds remaining from the Kalman state:

```python
avg_reduction = abs(dispute_delta) / max(len(states) - 1, 1)
if avg_reduction > 0:
    raw = dispute_est / avg_reduction
    rounds_remaining = max(1, min(10, int(raw) + ...))
```

This derives rounds remaining from the Kalman-filtered dispute trajectory, not from the linear trend slope. FR-008 is met.

---

## FR-006: method Field in PluginResult.data

The ConvergencePrediction includes `method: str`, which is set to `"kalman"` or `"ols"`. The predictor plugin transfers this to `PluginResult.data["method"]`. This satisfies FR-006.

---

## Recommendations

### P1 (Must Fix)

1. **P1-1**: Narrow the exception catch in the Kalman fallback. Catch `(ValueError, ArithmeticError)` explicitly. Let unexpected exceptions (TypeError, AttributeError) propagate during testing. Add a flag or log-level check to control this behavior.

### P2 (Should Fix)

2. **P2-1**: Clarify confidence_bounds documentation. State explicitly that it is `None` when `method="ols"` and always populated when `method="kalman"`.

3. **P2-2**: Add `__all__` to convergence.py: `__all__ = ["ConvergencePrediction", "predict_convergence"]`.

### P3 (Consider)

4. **P3-1**: The auto-dispatch threshold (2+ rounds for Kalman) is hardcoded. Consider making it configurable for domains where even 2 rounds of Kalman filtering is unreliable.
