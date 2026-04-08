# Dependency Audit — Wave 034-038

**Auditor**: dependency-auditor
**Date**: 2026-04-01
**Specs reviewed**: 034, 035, 036, 037, 038
**Method**: Import graph analysis + cross-spec dependency chain verification

---

## Import Boundary Analysis

### conversus/schemas/ (foundation layer)
- `modes.py`: No imports from other conversus modules. Pure constant definition. **CLEAN**.
- `features.py`: Imports `VALID_MODES` from `modes.py`. **CLEAN**.
- `objectives.py`: Imports `VALID_MODES` from `modes.py`. **CLEAN**.
- `construction.py`: Imports from `objectives.py`. **CLEAN**.
- `validation.py`: No imports from other conversus modules. **CLEAN**.

### conversus/plugins/ (plugin layer)
- `base.py`: Imports only `pydantic` and stdlib. No imports from `schemas/` or `engine/`. **CLEAN**.
- `nashopt/kalman.py`: No imports from other conversus modules. Pure math. **CLEAN**.
- `nashopt/convergence.py`: Imports `kalman` (same package) and `features` (schemas). **CLEAN**.
- `nashopt/predictor.py`: Imports `base` (plugin infra) and `convergence` (same package). **CLEAN**.
- `nashopt/payoffs.py`: Imports `features` (schemas). **CLEAN**.
- `nashopt/solver.py`: Imports `features` (schemas). Optional `nashopt`/`numpy`. **CLEAN**.
- `nashopt/scorer.py`: Imports `base`, `payoffs`, `solver`, `features`. **CLEAN**.

### engine/ (engine layer)
- `config.py`: Imports `modes.py`. **CLEAN**.

---

## Cross-Spec Dependency Chain

```
Spec 036 (modes.py) ──────────┐
                               ├── Spec 034 (convergence, kalman, predictor)
                               ├── Spec 035 (base.py)
Spec 038 (solver.py, payoffs.py, scorer.py) ──┤
                               ├── Spec 037 (validation.py)
                               └── engine/config.py
```

### Dependency Health

| Dependency | Status |
|---|---|
| modes.py -> features.py | CLEAN — features imports from modes |
| features.py -> convergence.py | CLEAN — convergence imports RoundFeatures |
| base.py -> scorer.py | CLEAN — scorer imports Plugin, PluginResult, etc. |
| predictor.py -> convergence.py | CLEAN — within same package |
| scorer.py -> payoffs.py, solver.py | CLEAN — within same package |
| validation.py | ISOLATED — no cross-module imports |

### Circular Dependencies

**None found.** All imports are directed acyclic.

---

## Cross-Spec Data Flow Dependencies

### eq_score pipeline (specs 034 + 035 + 038)

```
scorer.py (spec 038)
  produces: ["equilibrium_score"]
  ↓ via base.py execute_hooks (spec 035)
predictor.py (spec 034)
  consumes: ["equilibrium_score"]
```

This is the only cross-spec data dependency in the wave. It works correctly via the topological sort in base.py.

### VALID_MODES consistency (spec 036 -> all)

modes.py is the single source of truth. All modules that need modes import from it. No drift possible because the imports are direct.

---

## Findings

### DEP-1: Optional dependency pattern [OBSERVATION]

solver.py uses try-import for nashopt/numpy. kalman.py uses NO optional imports (pure Python). This is consistent within the wave.

### DEP-2: Validation module is isolated [OBSERVATION]

validation.py has no imports from other conversus modules (only Pydantic and stdlib). This makes it independently testable and deployable. Good modular design.

### DEP-3: No engine/ imports in plugins/ [CORRECT]

The design rule "plugin package imports nothing from engine/" is respected. Verified across all plugin files. **CLEAN**.

---

## Conclusion

All import boundaries are clean. No circular dependencies. The one cross-spec data flow (eq_score pipeline) is correctly implemented via the topological sort mechanism. The VALID_MODES consolidation (spec 036) eliminates drift risk across all modules.
