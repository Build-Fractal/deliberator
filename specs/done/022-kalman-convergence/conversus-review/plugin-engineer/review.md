# Plugin Engineer Review -- Spec 022 Kalman Convergence

**Reviewer**: plugin-engineer
**Phase**: 1 (independent review)
**Date**: 2026-04-01
**Spec**: 022-kalman-convergence
**Files reviewed**: spec.md, kalman.py, convergence.py, predictor.py, test_kalman.py

---

## Executive Summary

The method dispatch between Kalman and OLS is clean and well-structured. Backward compatibility is maintained: OLS behavior is untouched, the plugin interface is unchanged, prediction categories are preserved, and the hook point remains POST_PHASE_5. The `convergence_method` config key controls dispatch, `method` and `confidence_bounds` are added to the output without breaking existing consumers. However, there are gaps in config passthrough (Q/R matrices are not accessible from plugin config), the OLS fallback on Kalman exception is silent with only a log warning, and the `equilibrium_scores` integration is stubbed out with a TODO.

---

## Alignment

### What the implementation gets right

1. **Clean method dispatch.** The `predict_convergence()` function uses a `method` parameter with `Literal["auto", "kalman", "ols"]` typing. The "auto" mode defaults to Kalman with 2+ rounds and OLS otherwise. This is a clean, predictable dispatch strategy that requires no runtime dependency detection.

2. **Backward-compatible output format.** The `ConvergencePrediction` dataclass adds `method` (default `"ols"`) and `confidence_bounds` (default `None`) as optional fields with defaults, so existing code consuming the OLS path sees identical output shapes. The plugin's `PluginResult.data` dict now includes `method` and `confidence_bounds` keys, but these are additive -- no existing keys were removed or renamed.

3. **Plugin interface preserved.** `ConvergencePredictor` still implements `Plugin`, hooks to `POST_PHASE_5`, and returns `PluginResult`. The `execute()` method signature is unchanged. This satisfies the spec constraint "Must NOT change the Plugin interface."

4. **Prediction categories preserved.** The output is still one of `"converge"`, `"stagnate"`, `"uncertain"`. No new categories were introduced. This satisfies "Must NOT change prediction categories."

5. **Config-driven method selection.** The `convergence_method` key in `plugin_config` allows runtime selection of the prediction method. This follows the established pattern where plugin behavior is controlled through `conversus.yml` config.

6. **Graceful Kalman failure fallback.** If the Kalman path raises any exception, `predict_convergence()` catches it, logs a warning, and falls back to OLS. This ensures the predictor never crashes the deliberation pipeline.

7. **`__init__.py` exports are complete.** All Kalman-related symbols (`KalmanState`, `KalmanPrediction`, `run_kalman_filter`, `detect_fixed_point`, `kalman_update`, `kalman_predict`, `compute_confidence_bounds`, `compute_kalman_confidence`) are exported from `conversus.plugins.nashopt` and included in `__all__`. Tests verify importability.

---

## Missed Opportunities

### M1: Q and R matrices not configurable from plugin config

The spec (FR-007) requires: "Process noise Q and observation noise R MUST be configurable via plugin config." The `predict_convergence()` function accepts `Q` and `R` as parameters, and they flow through to the Kalman filter. However, the `ConvergencePredictor.execute()` method does not read `Q` and `R` from `plugin_config`:

```python
# predictor.py line 253 -- Q and R are not passed
prediction = predict_convergence(
    current_features=current,
    history=history,
    equilibrium_scores=None,
    min_confidence=min_confidence,
    method=convergence_method,
)
```

The `Q` and `R` keyword arguments are absent. Users can configure `convergence_method` and `min_confidence` via plugin config but not noise matrices. This is a gap in FR-007 compliance at the plugin layer.

### M2: Equilibrium scores not wired through

In `predictor.py` line 257: `equilibrium_scores=None,  # TODO: read from scorer output`. The Kalman filter's third state variable is `equilibrium_score`, which is always 0.0 when equilibrium scores are not provided. This means 1/3 of the state vector carries no information. The EquilibriumScorer runs at the same hook point (POST_PHASE_5), so scores should be available from prior rounds' plugin results. This TODO needs resolution for the filter to work at full capacity.

### M3: No method validation at the plugin config level

The `convergence_method` config value is passed directly to `predict_convergence()` as the `method` parameter. If a user puts `convergence_method: "bayesian"` in their config, it will fall through to the `elif method == "auto"` check (since it is neither "kalman" nor "auto"), evaluate as false, and silently use OLS. There is no validation or warning that an unknown method was requested.

### M4: Silent exception swallowing on Kalman failure

When the Kalman path fails, the exception is logged at WARNING level and OLS takes over. This is good for resilience, but the OLS result does not indicate that it was a fallback. The `method` field will say `"ols"` with no indication that Kalman was attempted and failed. A `method: "ols_fallback"` or a `fallback_reason` field in the output data would give operators visibility.

### M5: Cost estimation not delegated to Kalman model

FR-008 from spec 022 states cost estimation "MUST use the Kalman model's predicted rounds remaining, not the linear estimate." The `_build_recommendation()` function in `predictor.py` uses `prediction.estimated_rounds_remaining` regardless of method, which is correct -- the Kalman path computes its own `rounds_remaining`. However, the OLS fallback still computes cost with the linear estimate when the method is "auto" and falls back to OLS (e.g., 1-round case). This is acceptable since the Kalman model is not applicable with < 2 rounds, but the boundary is worth documenting.

---

## Off-Base Assumptions

### O1: "auto" mode threshold of 2 rounds is arbitrary

The auto mode switches to Kalman at >= 2 rounds. With only 2 observations and a 3D state vector, the filter is underdetermined. The spec says the filter "must work with as few as 2 data points" but also says it should produce "high-uncertainty predictions" in that case. The threshold is defensible but could be 3 to avoid noisy early Kalman predictions.

### O2: The Kalman path does not use the OLS trends at all

The OLS path computes dispute trend, concession trend, and equilibrium trend as separate linear regressions. The Kalman path ignores these entirely and uses its own state estimation. This is architecturally clean (each path is self-contained), but it means the two methods cannot be blended or compared internally. A future "ensemble" mode might want access to both.

---

## Actionable Recommendations

### P1 (Critical)

1. **Wire Q and R from plugin config to `predict_convergence()`.** In `ConvergencePredictor.execute()`, read `config.get("process_noise_Q")` and `config.get("observation_noise_R")` and pass them as `Q=` and `R=` keyword arguments. This closes the FR-007 gap at the plugin layer.

2. **Validate `convergence_method` config value.** Add validation at the top of `execute()`: if the value is not in `("auto", "kalman", "ols")`, log a warning and default to `"auto"`. This prevents silent misconfiguration.

### P2 (High)

3. **Wire equilibrium scores from prior plugin results.** The `DeliberationState` should carry prior plugin outputs (or the predictor should accept them via config). At minimum, document the integration pathway and remove the TODO.

4. **Add a `fallback_reason` field to PluginResult.data when Kalman falls back to OLS.** This gives operators visibility into why the Kalman path was not used, without changing the output format (it is a new additive key).

5. **Add integration test for config passthrough.** Write a test that verifies `plugin_config={"process_noise_Q": [[...]], "observation_noise_R": [[...]]}` flows through to the Kalman filter and affects the output.

### P3 (Medium)

6. **Document the "auto" threshold decision.** Add a code comment explaining why 2 rounds is the threshold and what trade-offs were considered (underdetermined state vs. early availability).

7. **Add a test for invalid `convergence_method` config.** Verify that an unrecognized method value does not crash and falls back to a sensible default.

8. **Consider adding a `kalman_diagnostics` sub-dict to output data.** Include innovation magnitude, covariance trace, and fixed-point status as nested data for observability. This does not change the top-level format but gives operators filter health visibility.

### P4 (Low)

9. **Refactor `_predict_convergence_kalman` branching.** The function has 5 nested if/elif/else branches for classification (fixed_point + low disputes, delta < 0, delta > 0, flat + fixed_point, flat). This could be simplified with a lookup table or a classification function that returns (prediction, reasoning_template).

10. **Add type alias for the method literal.** Define `ConvergenceMethod = Literal["auto", "kalman", "ols"]` at module level and reuse it in `predict_convergence()` and `ConvergencePredictor.execute()` for consistency and single-source-of-truth for valid values.

---

## Referenced Documentation

- `conversus/plugins/nashopt/kalman.py` -- Kalman filter core (436 lines)
- `conversus/plugins/nashopt/convergence.py` -- Convergence prediction with dispatch (703 lines)
- `conversus/plugins/nashopt/predictor.py` -- Plugin wrapper with config handling (296 lines)
- `conversus/plugins/nashopt/__init__.py` -- Package exports (67 lines)
- `tests/test_kalman.py` -- Test suite covering all paths (1002 lines)
- `specs/done/022-kalman-convergence/spec.md` -- Feature specification (87 lines)
