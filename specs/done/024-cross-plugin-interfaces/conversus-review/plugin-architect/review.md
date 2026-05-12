# Plugin Architect Review — Spec 024: Cross-Plugin Interfaces

**Reviewer**: plugin-architect
**Round**: 1 of 3
**Date**: 2026-04-01

---

## Executive Summary

Spec 024 introduces a well-motivated produces/consumes declaration system that solves a real quality regression (the 3D-to-2D Kalman downgrade). The implementation in `base.py` is structurally sound: Kahn's algorithm for topological sort, frozen Pydantic state passing, and per-hook accumulation of `plugin_results` are all defensible choices. However, the current design has a significant coupling asymmetry (producers must know their output keys leak into consumer internals), the Kalman 2D/3D dimension-switching has a data alignment bug when equilibrium score history is shorter than round history, and the `plugin_results` dict on frozen `DeliberationState` creates a subtlety around cross-hook data lifetime that is neither documented nor tested. The test suite covers the primary happy paths for SC-001 through SC-005 but leaves several edge cases and failure modes unexercised.

---

## Alignment (What the Spec Gets Right)

### A1. Correct problem identification (spec.md:7-8, 16-19)

The origin statement nails the root cause: the 3D Kalman state was reduced to 2D because `eq_score` was always zero. This is a real quality loss, not a theoretical concern. The spec traces the problem to plugin isolation and proposes the narrowest fix that restores the lost signal.

### A2. Graceful degradation via optional consumes (base.py:158-159, spec.md:74)

FR-004 requiring that missing consumed keys MUST NOT crash the consumer is the right default. The implementation delivers: `state.plugin_results.get("equilibrium_score")` in `predictor.py:255` returns `None` when the scorer is absent, and the Kalman path falls back to 2D observations (`convergence.py:268-271`). This means the system degrades monotonically — adding plugins can only improve signal, never break existing behavior.

### A3. Topological sort preserving declaration order for ties (base.py:306-393)

Kahn's algorithm with declaration-order tiebreaking (line 368: `queue.sort(key=lambda p: plugin_index[id(p)])`) satisfies FR-007 and FR-009 simultaneously. Plugins without dependency declarations see zero behavioral change — their relative order is preserved exactly. This is the correct stability property for backward compatibility.

### A4. Clean separation: declarations on ABC, execution in orchestrator (base.py:125-159, 401-504)

The `Plugin` ABC owns the `produces`/`consumes` class attributes. The `execute_hooks()` function owns the sort, the state-threading, and the result extraction. Plugins never need to know about the orchestration machinery. This separation means existing plugins require zero code changes unless they want to participate in data sharing.

### A5. Frozen state prevents mutation-based coupling (base.py:88-89, 466)

`DeliberationState` is frozen Pydantic (`model_config = {"frozen": True}`). The orchestrator creates a new copy via `state.model_copy(update={"plugin_results": plugin_results})` (line 466) for each plugin. This means a misbehaving plugin cannot poison the shared state by mutating the dict in-place — the dict is rebuilt on each iteration.

### A6. Cycle detection with clear error message (base.py:381-393)

The `PluginDependencyCycleError` includes the names of the plugins involved and the hook point, which is sufficient for debugging. The test at `test_cross_plugin.py:381-386` validates this path.

---

## Missed Opportunities

### M1. No data key registry or namespace collision prevention

**Location**: `base.py:158-159` (produces/consumes are bare string lists)

Two independently developed plugins could both declare `produces = ["score"]` and silently overwrite each other in `plugin_results`. The current implementation at `base.py:333-336` builds `producers: dict[str, Plugin]` which maps each key to the *last* plugin that declares it — earlier producers are silently shadowed with no warning. The spec does not address this. A namespace convention (e.g., `"equilibrium-scorer.score"` or a uniqueness check at load time) would prevent a class of subtle runtime bugs.

### M2. Cross-hook data lifetime is undefined

**Location**: `base.py:462` (`plugin_results: dict[str, Any] = dict(state.plugin_results)`)

At the start of `execute_hooks()`, `plugin_results` is initialized from whatever was in `state.plugin_results`. But the spec never addresses whether data produced at `POST_PHASE_5` should be visible at `POST_DELIBERATION`. If the engine creates a fresh `DeliberationState` for each hook invocation (likely), prior-hook results are lost. If it reuses the same state, they persist. The ScenarioPlugin (`scenarios/plugin.py:60`) consumes `equilibrium_score` at `POST_DELIBERATION`, but the EquilibriumScorer produces it at both `POST_PHASE_5` *and* `POST_DELIBERATION` (`scorer.py:348`). This works today only because the scorer runs at both hooks. If the scorer were removed from `POST_DELIBERATION`, the scenario plugin would silently get `None`. The spec should define cross-hook lifetime semantics explicitly.

### M3. No validation that produced keys appear in result.data

**Location**: `base.py:474-477`

The orchestrator extracts produced keys from `result.data` only if the key exists: `if key in result.data`. But there is no warning when a plugin declares `produces = ["foo"]` and then returns a `PluginResult` whose `data` dict lacks `"foo"`. This is a silent contract violation. A debug-level log would catch integration mistakes early.

### M4. EquilibriumScorer self-nesting of output key

**Location**: `scorer.py:413`

The scorer does `score_data["equilibrium_score"] = score_data["score"]` — it copies the score into a key that matches its `produces` declaration. This is a workaround for the fact that the orchestrator extracts *named keys* from `result.data` rather than the entire `data` dict. This pattern forces every producer to know its own key name and explicitly copy the value, which is boilerplate-prone and easy to forget. A convention where the orchestrator stores the entire `result.data` under a plugin-namespaced key would eliminate this.

### M5. Equilibrium score history is only a single element

**Location**: `predictor.py:255-261`

The predictor receives only the current round's equilibrium score via `plugin_results.get("equilibrium_score")` and wraps it in a single-element list (`equilibrium_scores = [float(eq_score)]`). The Kalman path in `convergence.py:282-287` then reuses this single value for all historical rounds via `eq_idx = min(i, len(equilibrium_scores) - 1)`. This means rounds 1 through N all get the same eq_score from round N. The 3D Kalman filter is operating on fabricated data for all but the latest observation, which mathematically degrades the state estimate rather than improving it. The spec's data flow diagram (spec.md:48-56) implies per-round eq_score availability, but the implementation delivers only a snapshot.

### M6. No typed contract for produced values

**Location**: `base.py:158` (`produces: list[str]`)

The `produces` declaration is just a list of string keys with no type annotation on the values. A consumer has no compile-time or runtime guarantee about the shape of what it receives. A dictionary mapping key names to expected types (`produces: dict[str, type]`) would enable runtime validation and better documentation.

### M7. Multiple producers for the same key are silently allowed

**Location**: `base.py:333-336`

The `producers` dict is built in declaration order. If two plugins both produce `"equilibrium_score"`, the second silently wins. Combined with the topological sort, this creates unpredictable behavior — the consumer depends on whichever producer the sort places last. At minimum, this should log a warning; ideally, it should raise an error.

### M8. `_topological_sort_plugins` performance on large plugin sets

**Location**: `base.py:366-369`

`queue.sort(key=lambda p: plugin_index[id(p)])` runs on every iteration of the while loop. For N plugins, this gives O(N^2 log N) worst case. This is fine for the expected plugin count (under 20), but the comment on line 367 ("stable sort") is misleading — Python's sort is stable, but re-sorting the entire queue every iteration is not the conventional approach. A priority queue (heapq) keyed on declaration index would be both clearer and O(N log N).

### M9. Test gap: no test for producer that fails mid-chain

**Location**: `test_cross_plugin.py`

The test suite has no test where a producer plugin raises an exception and the subsequent consumer must handle `None`. The orchestrator handles this path (`base.py:496-503` catches the exception), but the consumer's `plugin_results` will lack the expected key. This is a critical real-world scenario (e.g., nashopt solver timeout) that should be explicitly tested.

---

## Off-Base Assumptions

### O1. "All-zero eq_scores means 2D fallback" is too aggressive a heuristic

**Location**: `convergence.py:268-271`

```python
use_3d = (
    equilibrium_scores is not None
    and len(equilibrium_scores) > 0
    and any(s != 0.0 for s in equilibrium_scores)
)
```

A legitimate equilibrium score of exactly `0.0` (no agents at equilibrium) is a valid, informative observation — it means the system is maximally far from equilibrium. Treating it as "no data" conflates "no scorer installed" with "scorer ran but found no equilibrium." The correct sentinel for "no data" is `None`, which is already the value when the scorer is absent. The `0.0` check was appropriate when the workaround was in place (scores were always zero because of the wiring bug), but now that spec 024 provides real scores, this heuristic should be `eq_score is not None` only.

### O2. Frozen Pydantic dict provides deep immutability

**Location**: `base.py:88-89, 98`

`DeliberationState` is frozen, which prevents *reassignment* of `plugin_results`. But the dict *values* are `Any` — if a producer stores a mutable object (e.g., a list or nested dict), a consumer can mutate it and affect subsequent consumers. The `model_copy(update=...)` at line 466 creates a shallow copy of the dict, not a deep copy of its values. Example: if producer A stores `data={"my_list": [1,2,3]}`, consumer B could do `state.plugin_results["my_list"].append(4)` and consumer C would see the mutated list. Pydantic's frozen mode does not protect against this.

### O3. The Kalman filter handles dimension switching transparently

**Location**: `kalman.py:272-282 (default_Q), convergence.py:330-343`

The Kalman filter's `run_kalman_filter()` uses `default_Q()` and `default_R()` which return 2x2 matrices (`kalman.py:228-251`). When the convergence module passes 3D observations, it must *also* pass 3x3 Q and R matrices (`convergence.py:330-343`). If someone calls `run_kalman_filter(observations_3d)` without explicit Q/R, the filter will receive 3D observations but 2x2 noise matrices. The `kalman_update` function will attempt `_mat_add` on matrices of different dimensions, which will silently produce a corrupted matrix (Python list comprehension uses `range(n)` where `n = len(a)` — it won't crash for 2x2 + 3x3, it will just silently use the smaller dimension and drop the third row/column). The dimension auto-detection in `run_kalman_filter` (line 379: `n = len(observations[0])`) is only used for the initial covariance, not for Q and R defaults. This is a latent bug waiting to be triggered by any caller that omits Q/R with 3D data.

---

## Actionable Recommendations

### P1 (Critical): Fix Q/R dimension mismatch in `run_kalman_filter` default handling

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/kalman.py`, lines 370-376

**Problem**: `default_Q()` and `default_R()` always return 2x2. When 3D observations are passed without explicit Q/R, the filter operates with mismatched dimensions.

**Fix**: Auto-size default Q/R to match observation dimension:
```python
if Q is None:
    n = len(observations[0])
    if n == 2:
        Q = default_Q()
    elif n == 3:
        Q = [[1.0, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.01]]
    else:
        Q = _eye(n)  # generic fallback
# Same for R
```
Alternatively, add dimension validation that raises early if `len(Q) != len(observations[0])`.

### P1 (Critical): Fix the all-zero equilibrium score sentinel logic

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/convergence.py`, lines 268-271

**Problem**: `any(s != 0.0 for s in equilibrium_scores)` treats a legitimate score of 0.0 as "no data." Now that spec 024 wires real scores, a 0.0 score is meaningful.

**Fix**: Replace with a check that the list is non-empty and not `None`:
```python
use_3d = (
    equilibrium_scores is not None
    and len(equilibrium_scores) > 0
)
```

### P1 (Critical): Accumulate per-round equilibrium score history

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/predictor.py`, lines 255-261

**Problem**: Only the current round's score is available. Prior rounds' scores are lost between hook invocations. The Kalman filter receives fabricated repeated values instead of real per-round data.

**Fix**: Store equilibrium scores in a list on `DeliberationState.plugin_results` keyed as `"equilibrium_score_history"`, with the scorer appending each round. Alternatively, have the predictor maintain an internal accumulator across calls (though this conflicts with stateless plugin design). The cleanest fix is for the orchestrator to maintain a persistent `plugin_results` dict across rounds (not just across plugins within a single hook invocation), or for the spec to define a `"equilibrium_score_history": list[float]` key that the scorer appends to each round.

### P2 (High): Add duplicate producer key detection

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, lines 333-336

**Problem**: Two plugins producing the same key silently overwrites.

**Fix**: After building the `producers` dict, check for collisions:
```python
seen: dict[str, str] = {}
for p in plugins:
    for key in getattr(p, "produces", []):
        if key in seen:
            raise PluginDependencyCycleError(
                f"Duplicate producer for key '{key}': "
                f"'{seen[key]}' and '{p.name}' at hook '{hook.value}'."
            )
        seen[key] = p.name
```

### P2 (High): Log a warning when a plugin declares produces but omits the key from result.data

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, lines 474-477

**Problem**: Silent contract violation when a plugin fails to include its declared key.

**Fix**:
```python
for key in getattr(plugin, "produces", []):
    if key in result.data:
        plugin_results[key] = result.data[key]
    else:
        logger.warning(
            "Plugin '%s' declares produces=['%s'] but "
            "result.data does not contain key '%s'.",
            plugin.name, key, key,
        )
```

### P2 (High): Define cross-hook data lifetime in the spec

**File**: `<HOME>/code/payer-index-mono/conversus/specs/024-cross-plugin-interfaces/spec.md`

**Problem**: The spec does not define whether `plugin_results` persists across hook points or is reset per hook.

**Fix**: Add an FR specifying behavior: "FR-011: `plugin_results` is scoped to a single hook invocation. Data produced at `POST_PHASE_5` is NOT automatically available at `POST_DELIBERATION`. Producers that need cross-hook visibility MUST register for both hooks."

### P3 (Medium): Deep-copy plugin_results values to prevent mutation leakage

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, line 477

**Problem**: Mutable values in `plugin_results` can be mutated by consumers.

**Fix**: Use `copy.deepcopy(result.data[key])` when extracting produced values, or document that produced values MUST be immutable (frozen dataclasses, primitives).

### P3 (Medium): Add test for producer failure followed by consumer graceful degradation

**File**: `<HOME>/code/payer-index-mono/conversus/tests/test_cross_plugin.py`

**Problem**: No test covers a producer raising an exception and the consumer handling the absence.

**Fix**: Add a `FailingProducerPlugin` that raises in `execute()`, and verify the consumer receives `None` for the missing key and does not crash.

### P3 (Medium): Replace queue re-sort with heapq in topological sort

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, lines 366-369

**Problem**: O(N^2 log N) worst case. Negligible now but poor algorithmic hygiene.

**Fix**: Use `heapq` with `(declaration_index, plugin)` tuples to maintain O(N log N) total.

### P3 (Medium): Eliminate the self-nesting boilerplate in scorer

**File**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/scorer.py`, line 413

**Problem**: `score_data["equilibrium_score"] = score_data["score"]` is manual boilerplate that every producer must remember.

**Fix**: Consider having the orchestrator store the entire `result.data` dict and look up produced keys within it, rather than requiring producers to self-nest. Alternatively, document the convention clearly in the Plugin ABC docstring.

---

## Referenced Documentation

| File | Lines | Topic |
|------|-------|-------|
| `specs/024-cross-plugin-interfaces/spec.md` | 1-133 | Full spec |
| `conversus/plugins/base.py` | 125-159 | Plugin ABC with produces/consumes |
| `conversus/plugins/base.py` | 306-393 | Topological sort (Kahn's algorithm) |
| `conversus/plugins/base.py` | 401-504 | `execute_hooks()` orchestration |
| `conversus/plugins/nashopt/scorer.py` | 335-421 | EquilibriumScorer with produces |
| `conversus/plugins/nashopt/predictor.py` | 164-307 | ConvergencePredictor with consumes |
| `conversus/plugins/nashopt/convergence.py` | 242-292 | `_build_observation_sequence` 2D/3D switching |
| `conversus/plugins/nashopt/convergence.py` | 294-488 | Kalman prediction path |
| `conversus/plugins/nashopt/kalman.py` | 228-251 | Default 2x2 Q/R matrices |
| `conversus/plugins/nashopt/kalman.py` | 344-392 | `run_kalman_filter` dimension handling |
| `conversus/plugins/optimizer/optimizer.py` | 30-144 | ConfigOptimizer with produces |
| `conversus/plugins/scenarios/plugin.py` | 47-153 | ScenarioPlugin with consumes |
| `tests/test_cross_plugin.py` | 1-787 | Full cross-plugin test suite |
