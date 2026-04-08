# Meta-Review Phase 1: Dependency Auditor — Wave 024-028

**Scope**: Specs 024, 027, 028
**Date**: 2026-04-01
**Auditor role**: Do 024->027->028 dependency chains hold in code? Import boundaries respected?

---

## 1. Import Boundary Map

### Layer 1: Engine (`engine/config.py`)
- Imports: `yaml`, `pydantic`, `re`, `pathlib` (stdlib + pydantic only)
- No imports from `conversus.plugins` or `conversus.schemas`
- Defines its own `VALID_MODES` tuple

### Layer 2: Schemas (`conversus/schemas/`)
- `features.py`: Imports `pydantic` only. Defines its own `VALID_MODES` frozenset.
- `objectives.py`: Imports `pydantic` only. Defines its own `VALID_MODES` frozenset.
- `construction.py`: Imports from `conversus.schemas.objectives` (VALID_MODES, ObjectiveTemplate, etc.)
- `validation.py`: Imports from `pydantic` only. No imports from plugins or engine.
- **No schema module imports from `conversus.plugins`** — BOUNDARY RESPECTED

### Layer 3: Plugins (`conversus/plugins/`)
- `base.py`: Imports `pydantic` + stdlib only. No imports from schemas or engine.
- `nashopt/scorer.py`: Imports from `conversus.plugins.base` and `conversus.schemas.features`
- `nashopt/predictor.py`: Imports from `conversus.plugins.base`, `conversus.plugins.nashopt.convergence`, `conversus.schemas.features`
- `nashopt/convergence.py`: Imports from `conversus.plugins.nashopt.kalman`, `conversus.schemas.features`
- **Plugins import from schemas (downward dependency) but schemas never import from plugins** — BOUNDARY RESPECTED

### Layer 4: Tests (`tests/`)
- `test_cross_plugin.py`: Imports from `conversus.plugins.base`, `conversus.plugins.nashopt.convergence`, `conversus.schemas.features`
- `test_validation.py`: Imports from `conversus.schemas.validation` only
- `test_mode_expansion.py`: Empty file — no imports

---

## 2. Dependency Chain Analysis: 024 -> 027 -> 028

### 2.1 Does 024 depend on 027?
**NO.** Spec 024 (cross-plugin interfaces) operates entirely within:
- `conversus/plugins/base.py` (Plugin ABC, topological sort, execute_hooks)
- `conversus/plugins/nashopt/` (scorer, predictor, convergence, kalman)
- `conversus/schemas/features.py` (RoundFeatures, AgentFeatures)

None of these files import from `conversus.schemas.validation` (027's domain). The dependency is **unidirectional**: 027 Phase 3 depends on 024, not the reverse.

### 2.2 Does 027 depend on 024?
**YES, in Phase 3 only.** The synthesis explicitly notes:
- SC-003 (equilibrium scorer integration): BLOCKED on spec 021, which in turn requires 024's plugin framework
- FR-006, FR-007 (solver integration): BLOCKED on spec 021

In Phase 1 (current implementation), 027 is independent. `validation.py` has zero imports from the plugin layer. The dependency only materializes when 027 needs to run equilibrium scoring within validation deliberations.

### 2.3 Does 028 depend on 024 or 027?
**WEAKLY.** Spec 028 (mode expansion) modifies:
- `engine/config.py`: VALID_MODES tuple (independent)
- `conversus/schemas/construction.py`: DecisionType enum, _DECISION_TYPE_PATTERNS, _DECISION_TYPE_MODE (independent)
- `templates/*/`: 7 template files per mode (independent)
- `schema/modes/`: Mode schema YAML files (independent)

The modes defined by 028 are consumed by 024's scorer (`VALID_MODES` check in scorer.py) and could eventually be consumed by 027's validation config generator (if new problem types are added). But 028's code changes do not import from 024 or 027.

The **indirect dependency** is that 028's modes must appear in `features.VALID_MODES` for 024's scorer to accept them, and they do (all 8 modes present in features.py, objectives.py, and engine/config.py).

---

## 3. VALID_MODES Synchronization Audit

Three files define VALID_MODES independently (not imported from a single source):

| File | Type | Count | Modes |
|------|------|-------|-------|
| `engine/config.py` | tuple | 8 | cooperative, winner-take-all, prisoners-dilemma, red-blue, negotiation, resource-allocation, fair-division, mechanism-design |
| `conversus/schemas/features.py` | frozenset | 8 | Same 8 |
| `conversus/schemas/objectives.py` | frozenset | 8 | Same 8 |

**Finding**: All three are in sync with the same 8 modes. However, having three independent definitions is a DRY violation. If a 9th mode is added, all three must be updated manually.

**Risk**: MEDIUM — This is a maintenance hazard. A future mode addition that updates one file but not the others would cause silent validation mismatches (engine accepts a mode that schemas reject, or vice versa).

**Recommendation**: Consolidate into a single canonical definition (e.g., in `conversus/schemas/features.py`) and import from there. This is outside the scope of specs 024/027/028 but should be tracked.

---

## 4. Template-to-Mode Consistency

028 requires 7 templates per mode. Verified file counts:

| Mode | Template Dir | Files | Status |
|------|-------------|-------|--------|
| cooperative | templates/cooperative/ | 7 | OK |
| winner-take-all | templates/winner-take-all/ | 7 | OK |
| prisoners-dilemma | templates/prisoners-dilemma/ | 7 | OK |
| red-blue | templates/red-blue/ | 7 | OK |
| negotiation | templates/negotiation/ | 7 | OK |
| resource-allocation | templates/resource-allocation/ | 7 | OK |
| fair-division | templates/fair-division/ | 7 | OK |
| mechanism-design | templates/mechanism-design/ | 7 | OK |

All 8 modes have exactly 7 templates each (arbitration, cross-review, cross-round-synthesis, disputes, review, revision, synthesis). Schema/modes/ has 8 YAML files matching.

---

## 5. Cross-Plugin Data Flow Dependencies

The 024 synthesis identifies the following produces/consumes chain:

```
EquilibriumScorer  --produces-->  "equilibrium_score"
                                        |
ConvergencePredictor  --consumes--<-----+
                                        |
ScenarioPlugin  --consumes--<-----------+

ConfigOptimizer  --produces-->  "optimal_config"
                                        |
ScenarioPlugin  --consumes--<-----------+
```

**Verified in code**:
- `EquilibriumScorer.produces = ["equilibrium_score"]` (scorer.py:349)
- `ConvergencePredictor.consumes = ["equilibrium_score"]` (predictor.py:181)
- `ConfigOptimizer.produces = ["optimal_config"]` (verified via test_cross_plugin.py:781)
- `ScenarioPlugin.consumes = ["equilibrium_score", "optimal_config"]` (verified via test_cross_plugin.py:784-785)

**No circular dependencies exist.** The topological sort in base.py would raise `PluginDependencyCycleError` if any were introduced.

---

## 6. Missing: DuplicateProducerError

024's synthesis (P2 item 3) calls for a `DuplicateProducerError` when two plugins declare the same `produces` key. Searching the codebase:
- `DuplicateProducerError` appears only in review artifacts (synthesis, dispute, revision files) — NOT in production code
- `base.py:333-336` silently overwrites in the `producers` dict:
  ```python
  producers: dict[str, Plugin] = {}
  for p in plugins:
      for key in getattr(p, "produces", []):
          producers[key] = p
  ```

**Finding**: The duplicate-producer detection recommended by 024's synthesis has NOT been implemented. This is a known P2 item, not a regression. But it means two plugins declaring `produces = ["equilibrium_score"]` would silently shadow each other.

---

## 7. Verdict

| Boundary | Status |
|----------|--------|
| Schemas -> Plugins | CLEAN (no imports) |
| Plugins -> Schemas | CLEAN (downward only) |
| Engine -> Schemas/Plugins | CLEAN (no imports) |
| 024 -> 027 | NO DEPENDENCY (correct) |
| 027 -> 024 | PHASE 3 ONLY (correctly identified as blocked) |
| 028 -> 024/027 | NO DIRECT DEPENDENCY (correct) |
| VALID_MODES sync | IN SYNC (3 independent definitions, DRY risk) |
| Template completeness | ALL 8 MODES x 7 TEMPLATES (56 total) |
| DuplicateProducerError | NOT IMPLEMENTED (024 P2 item) |

**Import boundaries are fully respected.** Dependency chains hold in code. The VALID_MODES synchronization is the main maintenance risk.
