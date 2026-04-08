# Kalman/Convergence Review — Phase 1

**Agent**: plugin-integration-engineer
**Spec**: 034-kalman-convergence-fixes
**Date**: 2026-04-01
**Files reviewed**: convergence.py, kalman.py, predictor.py, test_kalman.py, test_convergence.py, test_cross_plugin.py

---

## Executive Summary

The plugin wiring between EquilibriumScorer (producer) and ConvergencePredictor (consumer) is well-implemented. The cross-plugin interface correctly accumulates eq_scores across rounds. The integration seam between predictor.py and convergence.py is clean. Two wiring issues require attention.

---

## Findings

### F-1: Cross-plugin eq_score accumulation works correctly [CRITICAL — C-2]

**Location**: predictor.py:252-274
**Status**: CORRECT

The accumulation pattern is:
1. Iterate `state.history` (completed rounds), appending `plugin_results.get("equilibrium_score")` per round (lines 256-261).
2. Append current round's live `state.plugin_results.get("equilibrium_score")` (lines 264-268).
3. If all entries are None, pass `None` to signal "no eq data at all" (lines 271-274).

This correctly handles: (a) scorer absent entirely, (b) scorer present but score is 0.0, (c) mixed rounds with/without scores.

**Verdict**: C-2 is fully resolved. The wiring is correct.

### F-2: consumes declaration alignment [HIGH]

**Location**: predictor.py line 181
**Status**: CORRECT

`ConvergencePredictor.consumes = ["equilibrium_score"]` matches `EquilibriumScorer.produces = ["equilibrium_score"]` (scorer.py:349). The topological sort in `base.py:_topological_sort_plugins` ensures scorer runs before predictor at POST_PHASE_5.

### F-3: plugin_results scoping across hooks [MEDIUM]

**Location**: base.py:477-478
**Status**: DOCUMENTED but under-tested

`execute_hooks` starts with `plugin_results = dict(state.plugin_results)` — a shallow copy of the incoming state's results. This means results from a previous hook invocation are NOT automatically carried forward unless the engine explicitly passes them in the state.

The predictor reads eq_score from `state.plugin_results` (the live dict) AND from `state.history[].plugin_results` (historical rounds). The historical path works because `RoundState.plugin_results` is populated by the engine after each round. The live path works because `execute_hooks` accumulates results within a single hook invocation.

**Risk**: If the engine calls POST_PHASE_5 for scorer and predictor in separate `execute_hooks` calls (instead of one call with both plugins), the predictor would miss the scorer's output for the current round.

**Verdict**: Wiring is correct IF both plugins are registered for the same hook and executed in the same `execute_hooks` call. The test in test_cross_plugin.py should verify this.

### F-4: History roundtrip — RoundState.plugin_results preservation [HIGH]

**Location**: predictor.py:257
**Status**: DEPENDS ON ENGINE

`round_state.plugin_results.get("equilibrium_score")` assumes the engine stores plugin results back into `RoundState.plugin_results` after each round. This is an engine responsibility (in `phases.py`). If the engine does NOT do this, historical eq_scores will always be None, and the predictor will fall back to 2D Kalman even when the scorer runs every round.

**Mitigation**: test_cross_plugin.py should include a multi-round integration test that verifies historical scores survive the round boundary.

**Priority**: P1 — if this wiring is broken, eq_score trend (C-2) silently fails.

### F-5: Fallback path when Kalman raises [MEDIUM]

**Location**: convergence.py:723-738
**Status**: CORRECT

`predict_convergence` catches all exceptions from the Kalman path and falls back to OLS with a warning. This is correct defensive design.

### F-6: test_cross_plugin.py coverage gaps [MEDIUM]

**Location**: test_cross_plugin.py
**Status**: NEEDS EXPANSION

The test file covers single-round cross-plugin execution and topological sort. It should also cover:
- Multi-round eq_score accumulation via `state.history[].plugin_results`
- 0.0 as a legitimate eq_score (not treated as absent)
- Mixed rounds (some with scorer, some without)

**Priority**: P2 — add integration tests for multi-round cross-plugin scenarios.

---

## Wiring Diagram

```
EquilibriumScorer (POST_PHASE_5)
  produces: ["equilibrium_score"]
  -> execute_hooks accumulates into plugin_results
  -> scorer.py:413 sets data["equilibrium_score"] = score

ConvergencePredictor (POST_PHASE_5)
  consumes: ["equilibrium_score"]
  -> predictor.py:264 reads state.plugin_results.get("equilibrium_score")
  -> predictor.py:257 reads state.history[].plugin_results.get("equilibrium_score")
  -> Passes accumulated scores to predict_convergence()
  -> convergence.py:_build_observation_sequence() decides 2D vs 3D
```

## Spec Compliance Summary

| Item | Status | Priority |
|---|---|---|
| C-2 (accumulate eq_scores) | IMPLEMENTED — wiring correct | -- |
| C-3 (zero-score sentinel) | IMPLEMENTED — None sentinel correct | -- |
| Cross-plugin ordering | CORRECT via topological sort | -- |
| History roundtrip | DEPENDS ON ENGINE | P1 |
| Multi-round integration test | MISSING | P2 |
