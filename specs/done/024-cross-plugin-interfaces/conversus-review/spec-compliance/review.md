# Spec-Compliance Review: 024-cross-plugin-interfaces

**Reviewer**: spec-compliance
**Phase**: 1 (Round 1 of 3)
**Date**: 2026-04-01

---

## Executive Summary

The implementation of spec 024 is **substantially complete and well-structured**. All ten functional requirements (FR-001 through FR-010) are MET. Four of five success criteria (SC-001 through SC-003, SC-005) are MET; SC-004 is MET. The core mechanism -- `produces`/`consumes` declarations on the Plugin ABC, topological sort in `_topological_sort_plugins`, and `plugin_results` propagation in `execute_hooks` -- faithfully implements the spec's proposed solution. The motivating example (EquilibriumScorer feeding ConvergencePredictor via 3D Kalman) is fully wired. Test coverage maps directly to every FR and SC with dedicated test classes. The implementation goes beyond the spec's minimum by also wiring ConfigOptimizer (produces `optimal_config`) and ScenarioPlugin (consumes `equilibrium_score`, `optimal_config`), anticipating the "Future Examples" table from section 6.

---

## Alignment

### Functional Requirements

| Requirement | Verdict | Evidence |
|---|---|---|
| **FR-001**: Plugins MAY declare `produces: list[str]` | **MET** | `Plugin` ABC declares `produces: list[str] = []` (base.py:158). `EquilibriumScorer.produces = ["equilibrium_score"]` (scorer.py:349). `ConfigOptimizer.produces = ["optimal_config"]` (optimizer.py:47). Test: `TestPluginDeclarations.test_producer_has_produces` (test_cross_plugin.py:331). |
| **FR-002**: Plugins MAY declare `consumes: list[str]` | **MET** | `Plugin` ABC declares `consumes: list[str] = []` (base.py:159). `ConvergencePredictor.consumes = ["equilibrium_score"]` (predictor.py:181). `ScenarioPlugin.consumes = ["equilibrium_score", "optimal_config"]` (plugin.py:60). Test: `TestPluginDeclarations.test_consumer_has_consumes` (test_cross_plugin.py:336). |
| **FR-003**: Both fields optional; plugins without them behave as today | **MET** | Default values `[]` on Plugin ABC (base.py:158-159). `PlainPlugin` has no declarations and passes validation. Test: `TestPluginDeclarations.test_produces_defaults_to_empty` (test_cross_plugin.py:323), `test_consumes_defaults_to_empty` (test_cross_plugin.py:328), `test_plugin_without_declarations_valid` (test_cross_plugin.py:339). |
| **FR-004**: Consumed key absent MUST NOT crash consumer | **MET** | `ConsumerPlugin.execute` uses `state.plugin_results.get("test_data")` which returns `None` when absent (test_cross_plugin.py:71). ConvergencePredictor uses `state.plugin_results.get("equilibrium_score")` (predictor.py:255) and handles `None` gracefully by passing `equilibrium_scores=None` to `predict_convergence`. Test: `TestExecuteHooksCrossPlugin.test_consumer_without_producer_gets_none` (test_cross_plugin.py:483-495). |
| **FR-005**: Orchestrator MUST execute producers before consumers at each hook | **MET** | `_topological_sort_plugins` (base.py:306-393) builds a dependency graph from `produces`/`consumes` and applies Kahn's algorithm. `execute_hooks` calls `_topological_sort_plugins` before iterating (base.py:456). Test: `TestTopologicalSort.test_producer_before_consumer` (test_cross_plugin.py:354-364), `TestSC003ExecutionOrder` (test_cross_plugin.py:676-722). |
| **FR-006**: Cycle MUST fail with clear error | **MET** | `_topological_sort_plugins` detects cycles when `len(sorted_plugins) != len(plugins)` (base.py:381) and raises `PluginDependencyCycleError` with plugin names (base.py:387-391). Test: `TestTopologicalSort.test_cycle_detection_raises` (test_cross_plugin.py:381-386), `TestExecuteHooksCrossPlugin.test_cycle_detection_in_execute_hooks` (test_cross_plugin.py:497-509). |
| **FR-007**: Execution order: topological sort by produces/consumes, declaration order for ties | **MET** | Kahn's algorithm with `queue.sort(key=lambda p: plugin_index[id(p)])` (base.py:368) ensures declaration order as tiebreaker. Test: `TestTopologicalSort.test_plain_plugins_maintain_declaration_order` (test_cross_plugin.py:366-379), `test_mixed_declared_and_undeclared` (test_cross_plugin.py:406-419). |
| **FR-008**: `DeliberationState.plugin_results: dict[str, Any]` populated by orchestrator | **MET** | `plugin_results` declared on `DeliberationState` as `dict[str, Any] = {}` (base.py:98). `execute_hooks` accumulates results: after each plugin executes, it extracts `produces` keys from `result.data` into `plugin_results` (base.py:474-477) and passes the updated dict to the next plugin via `state.model_copy(update=...)` (base.py:466-467). Test: `TestExecuteHooksCrossPlugin.test_plugin_results_populated_after_producer` (test_cross_plugin.py:430-449). |
| **FR-009**: Plugins without `produces`/`consumes` MUST work identically to today | **MET** | `PlainPlugin` (no declarations) executes normally. Declaration order is preserved for undeclared plugins in topological sort. Tests: `TestSC005UnchangedBehavior.test_plain_plugin_declaration_order_preserved` (test_cross_plugin.py:733-746), `test_plain_plugin_reverse_order` (test_cross_plugin.py:748-761). |
| **FR-010**: `plugin_results` MUST be empty by default | **MET** | `DeliberationState` field defaults to `{}` (base.py:98). Docstring explicitly cites FR-010 (base.py:86). Test: `TestDeliberationStatePluginResults.test_defaults_to_empty_dict` (test_cross_plugin.py:287-294). |

### Success Criteria

| Criterion | Verdict | Evidence |
|---|---|---|
| **SC-001**: ConvergencePredictor uses real eq_score when EquilibriumScorer is installed | **MET** | ConvergencePredictor reads `state.plugin_results.get("equilibrium_score")` (predictor.py:255) and passes it to `predict_convergence` as `equilibrium_scores` (predictor.py:268). `_build_observation_sequence` switches to 3D when non-zero scores exist (convergence.py:268-272, 282-287). Test: `TestSC001ConvergencePredictorUsesEqScore.test_predictor_receives_eq_score_via_plugin_results` (test_cross_plugin.py:599-637). Observation-level tests: `TestObservationSequence.test_3d_with_nonzero_eq_scores` (test_cross_plugin.py:565-575). |
| **SC-002**: ConvergencePredictor falls back to 2D when EquilibriumScorer is absent | **MET** | When `eq_score is None`, `equilibrium_scores` stays `None` (predictor.py:256-261). `_build_observation_sequence` produces 2D vectors when scores are `None`, empty, or all-zero (convergence.py:268-272). Test: `TestSC002FallbackTo2D.test_predictor_without_scorer_uses_2d` (test_cross_plugin.py:648-668). Observation-level: `test_2d_without_eq_scores`, `test_2d_with_none_eq_scores`, `test_2d_with_empty_eq_scores`, `test_2d_with_all_zero_eq_scores` (test_cross_plugin.py:540-563). |
| **SC-003**: Plugin execution order at POST_PHASE_5 is scorer then predictor | **MET** | `EquilibriumScorer.produces = ["equilibrium_score"]` (scorer.py:349), `ConvergencePredictor.consumes = ["equilibrium_score"]` (predictor.py:181). Topological sort guarantees scorer first. Tests: `TestSC003ExecutionOrder.test_scorer_before_predictor_in_topological_sort` (test_cross_plugin.py:679-696), `test_scorer_before_predictor_even_when_predictor_declared_first` (test_cross_plugin.py:698-722). |
| **SC-004**: Cycle declaration raises a clear error | **MET** | `PluginDependencyCycleError` raised with message containing plugin names and "Cycle detected" (base.py:387-391). Test: `TestTopologicalSort.test_cycle_detection_raises` (test_cross_plugin.py:381-386) with `match="Cycle detected"`. |
| **SC-005**: Plugins without produces/consumes work unchanged | **MET** | `PlainPlugin` and `PlainPluginB` execute normally, declaration order preserved. Tests: `TestSC005UnchangedBehavior` class (test_cross_plugin.py:730-761), `TestExecuteHooksCrossPlugin.test_plain_plugins_work_unchanged` (test_cross_plugin.py:469-481). |

---

## Missed Opportunities

1. **No cross-hook `plugin_results` accumulation.** The spec says `plugin_results` is populated "after each plugin executes" (FR-008), and the orchestrator resets `plugin_results` per hook invocation (base.py:462). This means a score produced at `POST_PHASE_5` is not available at `POST_DELIBERATION` unless re-produced. The EquilibriumScorer registers for both hooks and re-produces, so this works today, but the spec's data flow diagram (section 3) implies a single accumulation context per hook point, not across hooks. This is correct per spec but worth documenting explicitly.

2. **ConvergencePredictor receives only the current round's eq_score.** The predictor wraps the single score in a one-element list (predictor.py:261), but `_equilibrium_trend` requires 2+ values to compute a trend (convergence.py:152). This means the equilibrium trend bonus is never applied when using the cross-plugin path. Historical scores could be accumulated across rounds if `plugin_results` were persisted or if the predictor maintained internal state.

3. **No validation that `produces` keys are unique across plugins.** If two plugins both declare `produces = ["equilibrium_score"]`, the second one silently overwrites the first in the `producers` dict (base.py:334-336). The spec requires a DAG (section 8), but duplicate producers create an ambiguous graph that is not detected.

4. **`_topological_sort_plugins` uses `id(p)` as dict key.** Python `id()` values are not guaranteed stable across garbage collection cycles. In practice this is safe because all plugins are alive during the sort call, but using an integer index or plugin name would be more robust.

5. **Test for SC-001 does not assert that 3D Kalman was actually used.** The test (`test_predictor_receives_eq_score_via_plugin_results`, test_cross_plugin.py:599-637) verifies the predictor produces a valid prediction but does not check that the `method` is `"kalman"` or that the observation sequence was 3D. The observation-level tests cover dimensionality separately, but an end-to-end assertion would strengthen SC-001 coverage.

---

## Off-Base Assumptions

1. **None identified in the core implementation.** The implementation faithfully follows the spec's proposed solution without making unsupported leaps. The constraint from section 8 -- "This spec adds declarations to the Plugin ABC. It does NOT implement the orchestration layer (#6/ORC)" -- is respected: the orchestration is minimal and scoped to `execute_hooks`, not a full orchestration engine.

2. **Minor: EquilibriumScorer publishes `equilibrium_score` as a nested key.** The scorer puts `score_data["equilibrium_score"] = score_data["score"]` (scorer.py:413), duplicating the value under a new key in `result.data`. This is not strictly specified by the spec but is necessary because `execute_hooks` extracts only keys listed in `produces` from `result.data` (base.py:475-477). The approach is correct but the duplication is subtle.

---

## Actionable Recommendations

### P1 (High Priority)

1. **Add duplicate-producer detection to `_topological_sort_plugins`.** If two plugins at the same hook point both declare the same `produces` key, raise a clear error rather than silently choosing the last one. This enforces the spec's DAG constraint (section 8) and prevents data-corruption bugs.
   - File: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, function `_topological_sort_plugins` (line 306).
   - Add: after building the `producers` dict (lines 333-336), check for collisions and raise `PluginDependencyCycleError` or a new `DuplicateProducerError`.

2. **Add a test asserting that the Kalman path receives 3D observations end-to-end.** Current SC-001 test only checks that the predictor returns a valid prediction when the scorer runs first. Add an assertion on `results[1].data["method"] == "kalman"` or mock `_build_observation_sequence` to capture its `equilibrium_scores` argument.
   - File: `<HOME>/code/payer-index-mono/conversus/tests/test_cross_plugin.py`, class `TestSC001ConvergencePredictorUsesEqScore`.

3. **Document `plugin_results` lifetime explicitly.** Add a note to the `execute_hooks` docstring or the spec clarifying that `plugin_results` is scoped to a single hook invocation (not accumulated across hooks). This prevents future consumers from assuming cross-hook availability.
   - File: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, function `execute_hooks` docstring (line 401).

### P2 (Medium Priority)

4. **Accumulate historical equilibrium scores for multi-round trend analysis.** The predictor currently receives only the current round's score (predictor.py:261). Consider having the engine pass prior `plugin_results` from previous rounds via the state's `history` or a new `historical_plugin_results` field, so that `_equilibrium_trend` can compute a meaningful slope.
   - Files: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py` (DeliberationState), `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/predictor.py`.

5. **Add a test for multiple producers feeding a single consumer.** The `MultiProducerPlugin`/`MultiConsumerPlugin` helpers exist (test_cross_plugin.py:128-155) and the topological sort test covers ordering (test_cross_plugin.py:397-404), but there is no `execute_hooks` integration test verifying that both `alpha` and `beta` values propagate through `plugin_results` to the consumer.
   - File: `<HOME>/code/payer-index-mono/conversus/tests/test_cross_plugin.py`, add a new test in `TestExecuteHooksCrossPlugin`.

6. **Consider using plugin name instead of `id(p)` in the topological sort.** Replace `id(p)` keys in `plugin_index`, `predecessors`, `successors`, and `in_degree` with `p.name` for readability and stability. Plugin names are already required to be unique non-empty strings by the `__init_subclass__` validation.
   - File: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, function `_topological_sort_plugins` (lines 340-392).
   - Caveat: Plugin names are unique per class but not validated unique per instance at runtime. If two instances of the same class can coexist, `id()` is actually correct. Validate uniqueness first.

### P3 (Low Priority)

7. **Add a negative test for a plugin that declares `produces` but omits the key from `result.data`.** Currently, if a producer declares `produces = ["foo"]` but returns `data={}`, the key silently stays absent from `plugin_results` (base.py:476: `if key in result.data`). This is arguably correct (graceful degradation) but a warning log would aid debugging.
   - File: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`, line 476.

8. **Consider a `PluginManifest` frozen dataclass for declarations.** Rather than class-level list attributes, a `manifest: PluginManifest` field with `produces`, `consumes`, `hooks`, and `name` would make the contract more explicit, enable schema validation, and simplify serialization for future tooling.

9. **Test cycle detection with 3+ plugins in a chain.** Current cycle test covers a simple A<->B cycle. Add a test with A->B->C->A to verify Kahn's algorithm handles longer cycles.
   - File: `<HOME>/code/payer-index-mono/conversus/tests/test_cross_plugin.py`.

10. **Spec section 8 states "This spec adds declarations to the Plugin ABC. It does NOT implement the orchestration layer (#6/ORC)."** But the implementation does wire orchestration logic in `execute_hooks`. This is strictly beyond spec scope -- it works correctly, but the spec should be updated to reflect that orchestration was implemented inline rather than deferred.

---

## Referenced Documentation

- **Spec**: `<HOME>/code/payer-index-mono/conversus/specs/024-cross-plugin-interfaces/spec.md`
- **Plugin ABC**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py`
- **EquilibriumScorer**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/scorer.py`
- **ConvergencePredictor**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/predictor.py`
- **Convergence functions**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/nashopt/convergence.py`
- **ConfigOptimizer**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/optimizer/optimizer.py`
- **ScenarioPlugin**: `<HOME>/code/payer-index-mono/conversus/conversus/plugins/scenarios/plugin.py`
- **Tests**: `<HOME>/code/payer-index-mono/conversus/tests/test_cross_plugin.py`
