# Feature Specification: Cross-Plugin Interfaces

**Feature ID**: `024-cross-plugin-interfaces`
**Created**: 2026-04-01
**Status**: Draft
**Depends On**: `016-plugin-system` (plugin framework), `021-nashopt-integration` (equilibrium scorer), `022-kalman-convergence` (convergence predictor)
**Origin**: Meta-review finding — equilibrium scores always zero in Kalman filter because plugins can't share data. The 3D Kalman state was reduced to 2D as a workaround (this spec is the real fix).

---

## 1. Problem

Plugins are isolated by design (Principle XV). They observe state and write output — they don't talk to each other. But some plugins produce data that other plugins need:

- **EquilibriumScorer** produces a score that **ConvergencePredictor** wants for its Kalman state
- **ConfigOptimizer** produces a recommended config that **ScenarioPlugin** wants to store
- **FeatureExtraction** produces vectors that **both** nashopt plugins consume

Currently each plugin re-extracts or operates without the data. The Kalman filter was reduced from 3D to 2D because eq_score was always zero — a real quality loss.

---

## 2. Proposed Solution: Explicit Plugin Dependencies

Plugins declare what they produce and what they consume:

```python
class EquilibriumScorer(Plugin):
    name = "equilibrium-scorer"
    hooks = [HookPoint.POST_PHASE_5, HookPoint.POST_DELIBERATION]
    produces = ["equilibrium_score"]  # NEW

class ConvergencePredictor(Plugin):
    name = "convergence-predictor"
    hooks = [HookPoint.POST_PHASE_5]
    consumes = ["equilibrium_score"]  # NEW — optional dependency
```

The orchestration layer (when it exists) uses these declarations to:
1. **Order plugin execution**: producers run before consumers at the same hook point
2. **Pass data**: consumer receives producer's output via `plugin_results` on state
3. **Handle absence**: if producer isn't installed, consumed field is `None` (graceful degradation)

---

## 3. Data Flow

```
POST_PHASE_5 hook fires:
  1. EquilibriumScorer.execute(state) → score = 0.87
     state.plugin_results["equilibrium_score"] = 0.87

  2. ConvergencePredictor.execute(state) → reads state.plugin_results["equilibrium_score"]
     Kalman observation = [disputes, concession_rate, 0.87]  ← real value, not zero
     Prediction confidence improves because 3D state is fully observed
```

Without the producer installed:
```
POST_PHASE_5 hook fires:
  1. ConvergencePredictor.execute(state)
     state.plugin_results.get("equilibrium_score") → None
     Kalman observation = [disputes, concession_rate]  ← falls back to 2D
```

---

## 4. Functional Requirements

### Plugin Declarations
- **FR-001**: Plugins MAY declare `produces: list[str]` — named data keys they output.
- **FR-002**: Plugins MAY declare `consumes: list[str]` — named data keys they want from other plugins.
- **FR-003**: Both fields are optional. Plugins without them behave exactly as today.
- **FR-004**: `consumes` is always optional — a consumed key being absent MUST NOT crash the consumer.

### Orchestration
- **FR-005**: At each hook point, the orchestrator MUST execute producers before consumers.
- **FR-006**: If two plugins both produce and consume each other (cycle), the orchestrator MUST fail with a clear error.
- **FR-007**: Plugin execution order within a hook: topological sort by produces/consumes, then declaration order for ties.
- **FR-008**: `DeliberationState.plugin_results: dict[str, Any]` — populated by the orchestrator after each plugin executes.

### Backward Compatibility
- **FR-009**: Plugins without `produces`/`consumes` declarations MUST work identically to today.
- **FR-010**: `plugin_results` MUST be empty by default (no data leakage when orchestrator isn't wired).

---

## 5. Motivating Example: Equilibrium → Kalman

When this spec is implemented, the convergence predictor restores 3D Kalman:

```python
# convergence.py — after spec 024
def _build_observation(features, plugin_results):
    eq_score = plugin_results.get("equilibrium_score", 0.0)
    if eq_score > 0.0:
        return [features.dispute_count, avg_concession, eq_score]  # 3D
    else:
        return [features.dispute_count, avg_concession]  # 2D fallback
```

The Kalman filter dynamically adjusts its dimensionality based on what data is available. No configuration needed — the produces/consumes declarations handle the wiring.

---

## 6. Future Examples

| Producer | Key | Consumer | Use Case |
|----------|-----|----------|----------|
| EquilibriumScorer | `equilibrium_score` | ConvergencePredictor | 3D Kalman state |
| ConfigOptimizer | `optimal_config` | ScenarioPlugin | Auto-save recommended config |
| FeatureExtraction | `feature_set` | EquilibriumScorer | Skip re-extraction |
| CodeReviewDomain | `review_score` | ConvergencePredictor | Domain-specific convergence |

---

## 7. Success Criteria

- **SC-001**: ConvergencePredictor uses real eq_score when EquilibriumScorer is installed.
- **SC-002**: ConvergencePredictor falls back to 2D when EquilibriumScorer is absent.
- **SC-003**: Plugin execution order at POST_PHASE_5 is: scorer → predictor (not reverse).
- **SC-004**: Declaring a cycle (A produces X, consumes Y; B produces Y, consumes X) raises a clear error.
- **SC-005**: Plugins without produces/consumes work unchanged.

---

## 8. Constraints

- This spec adds declarations to the Plugin ABC. It implements minimal orchestration within `execute_hooks` (topological sort of plugins by `produces`/`consumes` declarations, and `plugin_results` propagation after each plugin executes). This satisfies FR-005 through FR-008 at runtime.
- Full orchestration (engine integration, hook lifecycle management, cross-hook result propagation) remains for future work.
- The dependency graph between plugins MUST be a DAG (no cycles).
