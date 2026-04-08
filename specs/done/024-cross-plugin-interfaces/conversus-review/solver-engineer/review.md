# Solver-Engineer Review — Spec 024 Cross-Plugin Interfaces

**Reviewer role**: Numerical solver engineer
**Spec under review**: `024-cross-plugin-interfaces`
**Files reviewed**: `spec.md`, `base.py`, `scorer.py`, `predictor.py`, `convergence.py`, `kalman.py`, `features.py`, `test_cross_plugin.py`
**Date**: 2026-04-01

---

## Executive Summary

The eq_score wiring from EquilibriumScorer through plugin_results to ConvergencePredictor is structurally sound. The topological sort guarantees execution order, the scorer correctly publishes `equilibrium_score` in its `PluginResult.data`, and the predictor reads it from `state.plugin_results`. However, the dynamic 2D/3D dimension switching in the Kalman filter contains a critical dimension mismatch bug in `run_kalman_filter`, the 3D initial covariance uses inappropriate variance for the eq_score dimension, and the single-element equilibrium_scores list propagated from the predictor systematically defeats the 3D path for its intended use case. The mathematical scaffolding is correct but the wiring has several gaps that will produce silent numerical degradation rather than clean failures.

---

## Alignment

The following aspects are well-executed and aligned with spec 024's intent:

1. **Topological sort is correct.** Kahn's algorithm in `_topological_sort_plugins` properly orders scorer before predictor. The cycle detection and declaration-order tie-breaking are sound (FR-005 through FR-007).

2. **Data flow through plugin_results is clean.** The `execute_hooks` function correctly copies `plugin_results`, runs plugins sequentially, and extracts produced keys from `PluginResult.data` after each execution. The frozen `DeliberationState` is properly rebuilt via `model_copy` for each consumer.

3. **Graceful degradation on missing producer.** When the scorer is absent, `plugin_results.get("equilibrium_score")` returns `None`, `equilibrium_scores` stays `None`, and `_build_observation_sequence` correctly produces 2D vectors. The fallback path is clean.

4. **The Kalman filter's NxN generalization is well-structured.** The matrix helpers (`_eye(n)`, `_zeros(n)`, `_mat_mul`, etc.) are dimension-agnostic and the `run_kalman_filter` function infers dimension from the first observation. The state transition matrix `F` and observation matrix `H` are both auto-sized to identity.

5. **Q/R auto-sizing in convergence.py is correctly placed.** The 3D defaults in `_predict_convergence_kalman` (lines 331-343) are constructed before calling `run_kalman_filter`, so the caller's Q/R override the 2x2 defaults that `run_kalman_filter` would otherwise use.

---

## Missed Opportunities

1. **No accumulation of equilibrium scores across rounds.** The predictor (line 258-261) builds a single-element list `[float(eq_score)]` from the current round's plugin_results. Prior rounds' scores are lost because `plugin_results` is per-hook-execution. This means `_equilibrium_trend` always returns 0.0 (needs >= 2 values), and the 3D Kalman path gets only one real eq_score value replicated across all history rounds. The spec acknowledges this ("prior rounds are not available") but doesn't propose a solution. Persisting eq_scores in state.history or a plugin-local accumulator would unlock the full value of the 3D filter.

2. **No cross-validation of 2D vs 3D prediction quality.** There is no mechanism to compare whether 3D actually improves predictions over 2D for a given deliberation. A simple diagnostic (e.g., innovation magnitude ratio) could be logged to validate the spec's central claim.

3. **The OLS path ignores equilibrium_scores entirely for confidence beyond trend.** The `_equilibrium_trend` function returns 0.0 when given a single score, so the OLS confidence bonus from eq_score is never activated in the current wiring.

---

## Off-Base Assumptions

1. **"3D observation produces better Kalman predictions than 2D" is not unconditionally true.** The spec (line 19) claims 3D with real eq_score is superior to 2D. This holds only when: (a) eq_score carries information not already captured by dispute_count and concession_rate, and (b) the observation noise R for eq_score is well-calibrated. With the current defaults (R_eq = 0.005), the filter trusts eq_score almost as much as concession_rate. If eq_score is derived partly from the same concession data (which it is — concession_rate feeds payoff computation in the heuristic scorer), the 3D filter double-counts that signal, inflating confidence without improving accuracy.

2. **Single eq_score replicated to all historical rounds is not "observing 3D."** The `_build_observation_sequence` function (lines 284-287) uses `eq_idx = min(i, len(equilibrium_scores) - 1)`, which maps all historical rounds to the single available score. This is mathematically equivalent to asserting that eq_score was constant across all rounds — a false prior that biases the filter toward the most recent value. The filter treats this as strong evidence of stability in the third dimension, artificially shrinking covariance.

3. **The `any(s != 0.0 for s in equilibrium_scores)` gate (line 271) conflates "no data" with "score is exactly zero."** A legitimate eq_score of 0.0 (no agents at equilibrium) is informative and distinct from "scorer didn't run." The current gate discards valid zero scores.

---

## Actionable Recommendations

### P1 — Critical (silent numerical bugs)

**R1. Fix Q/R dimension mismatch in `run_kalman_filter` default path.**
When `convergence.py` passes 3D observations with explicit 3D Q and R, everything works. But if `Q` or `R` is omitted and the observation is 3D, `run_kalman_filter` calls `default_Q()` and `default_R()` which return 2x2 matrices. The `kalman_update` function then multiplies a 3x3 P by a 2x2 Q, producing silent dimension errors or wrong results. Fix: make `run_kalman_filter` auto-size default Q/R from `len(observations[0])` when no override is provided, rather than always calling `default_Q()`/`default_R()`.
- **File**: `kalman.py`, `run_kalman_filter` (lines 372-376)

**R2. Fix the replicated-score bias in `_build_observation_sequence`.**
When `equilibrium_scores` has 1 element and history has N rounds, the same score is broadcast to all N observations. This tells the filter that eq_score has been constant, artificially collapsing variance in that dimension. Fix: when `len(equilibrium_scores) < len(history)`, only attach eq_score to the rounds where data exists, and use 2D observations for rounds without data. Alternatively, pad missing rounds with NaN and skip the Kalman update for the third dimension on those steps (requires a masked observation update, more complex but correct).
- **File**: `convergence.py`, `_build_observation_sequence` (lines 284-287)

**R3. Accumulate equilibrium scores across rounds in the predictor.**
The single-element list defeats both the 3D Kalman and OLS equilibrium_trend paths. Store eq_scores in a round-indexed structure that persists across hook invocations. Options: (a) extend `RoundState` with an `eq_score: float | None` field, (b) use a plugin-local instance variable (predictor already has `self.plugin_config`, could add `self._score_history`), or (c) have the orchestrator append to a cumulative plugin_results history.
- **Files**: `predictor.py` (lines 255-261), `base.py` (`RoundState` or `execute_hooks`)

### P2 — Important (correctness/robustness)

**R4. Fix the zero-score gate to distinguish "no data" from "score = 0.0".**
Replace `any(s != 0.0 for s in equilibrium_scores)` with a sentinel-based check. When `equilibrium_scores is None`, use 2D. When it is a list (even of zeros), use 3D. A score of 0.0 means "no agents at best response" — that is meaningful data the filter should track.
- **File**: `convergence.py`, `_build_observation_sequence` (lines 268-272)

**R5. Calibrate the 3D observation noise R for eq_score independently.**
The default `R[2][2] = 0.005` is identical to `R[1][1]` (concession rate noise). Equilibrium score is computed from payoff functions that compound extraction noise, concession noise, and mode-specific logic. A more defensible default is `R[2][2] = 0.05` (10x concession noise), reflecting the additional uncertainty. Consider exposing this as a config parameter.
- **File**: `convergence.py`, `_predict_convergence_kalman` (lines 339-343)

**R6. Add 3D initial covariance tuning for eq_score dimension.**
In `run_kalman_filter` (line 380), the initial P diagonal is `[10.0, 1.0, ...]` — the third dimension gets variance 1.0 (same as concession_rate). Equilibrium score ranges [0,1] with typical values clustered in [0.5, 1.0]; initial variance of 1.0 is too wide relative to the signal range. Use `0.25` (std = 0.5, covering the full [0,1] range at 2-sigma).
- **File**: `kalman.py`, `run_kalman_filter` (line 380)

### P3 — Enhancement

**R7. Use the Joseph form for covariance update.**
The current P update `P_post = (I - K*H) * P_pred` (line 339 of kalman.py) is numerically fragile: floating-point errors can cause P to lose symmetry or positive-definiteness over many iterations. The Joseph form `P_post = (I-KH) * P_pred * (I-KH)^T + K * R * K^T` is algebraically equivalent but numerically stable. This matters more in 3D where there are more off-diagonal terms to accumulate error.
- **File**: `kalman.py`, `kalman_update` (lines 337-339)

**R8. Add a test that exercises the actual 3D Kalman path end-to-end.**
The test suite (`test_cross_plugin.py`) tests observation sequence dimensionality and integration via `execute_hooks`, but no test verifies that the Kalman filter itself runs correctly with 3D data and produces reasonable state estimates. Add a test in `test_cross_plugin.py` or a dedicated Kalman test file that: (a) feeds 3+ rounds of 3D observations, (b) verifies state dimension is 3, (c) checks that confidence bounds are finite and ordered, and (d) confirms the prediction is not "uncertain" with strongly convergent data.
- **File**: `tests/test_cross_plugin.py` (new test class)

**R9. Guard against singular S matrix in the 3D case.**
The `_mat_inverse` function raises `ValueError` when `abs(det) < 1e-12`. In the 3D case, if two observation dimensions are highly correlated (eq_score tracks concession_rate closely), the innovation covariance S can become near-singular. Add a fallback: when S is near-singular, skip the Kalman update for that step and carry forward the prior, rather than crashing the entire prediction.
- **File**: `kalman.py`, `kalman_update` (around line 329)

**R10. Docstring drift in `predict_convergence` and `kalman.py`.**
The `predict_convergence` docstring (line 703-704) still says Q/R are "2x2" and the module docstring for `kalman.py` (line 7) still says "2D state vector." These should reflect the 2D/3D dynamic behavior introduced by spec 024.
- **Files**: `convergence.py` (line 703-704), `kalman.py` (lines 1-25)

---

## Referenced Documentation

| Document | Relevance |
|----------|-----------|
| `specs/024-cross-plugin-interfaces/spec.md` | Primary spec under review; defines produces/consumes, data flow, success criteria |
| `conversus/plugins/base.py` | Plugin ABC, topological sort, execute_hooks orchestration |
| `conversus/plugins/nashopt/scorer.py` | EquilibriumScorer — produces equilibrium_score |
| `conversus/plugins/nashopt/predictor.py` | ConvergencePredictor — consumes equilibrium_score, builds feature history |
| `conversus/plugins/nashopt/convergence.py` | Core prediction logic: OLS and Kalman paths, observation building, Q/R auto-sizing |
| `conversus/plugins/nashopt/kalman.py` | Kalman filter core: NxN matrix ops, state tracking, confidence, fixed-point detection |
| `conversus/schemas/features.py` | RoundFeatures, AgentFeatures — observation source data |
| `tests/test_cross_plugin.py` | Test coverage for spec 024 success criteria and observation dimensionality |
