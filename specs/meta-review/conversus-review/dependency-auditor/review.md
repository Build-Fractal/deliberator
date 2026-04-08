# Meta-Review Phase 1: Dependency Chain Audit

**Auditor**: dependency-auditor
**Date**: 2026-04-01
**Scope**: Specs 021, 022, 023, 029, 030 -- cross-package import boundaries verified against actual code

---

## Executive Summary

The dependency chain rules documented across all five synthesis files hold in actual code. Every import boundary claim made by the review agents is verified as correct. The conversus codebase enforces a strict layered architecture:

1. **schemas/** is a leaf package -- imports only from itself and stdlib/pydantic. Zero upstream dependencies.
2. **plugins/** import from `plugins.base` (peer within the package) and `schemas/` (downward only). No plugin imports from another plugin.
3. **domains/** imports from itself and stdlib/pydantic only. Does not import from `plugins/`, `schemas/`, `engine/`, `linter/`, `web/`, or `mcp_server`.
4. **engine/** and **linter/** do not import from `plugins/`, `domains/`, or `schemas/`.

All five synthesis files correctly identify these boundaries. No cross-boundary violations were found.

One documentation inaccuracy was found: the `domains/__init__.py` docstring claims it imports from `conversus.plugins.base` and `conversus.schemas`, but no module within `domains/` actually does so.

---

## Alignment

### What the syntheses got right

**1. Spec 030 (Domain Plugin Architecture) -- coupling rule enforcement: VERIFIED**

The 030 synthesis states: "All three modules (`base.py`, `store.py`, `api.py`) import nothing from `engine/`, `linter/`, `web/`, or `mcp_server`." Grep confirms zero matches for any of these imports across the entire `conversus/domains/` tree.

**2. Spec 029 (Code Review Domain) -- coupling rules in code_review/__init__.py: VERIFIED**

The docstring declares: "MAY import from conversus.domains.base, conversus.schemas, stdlib. MUST NOT import from engine.*, linter.*, web.*, mcp_server." In practice, `code_review/` imports only from `conversus.domains.base` and `conversus.domains.code_review.extractors` (intra-package). It does not exercise the `conversus.schemas` permission, making its actual coupling surface even narrower than claimed.

**3. Spec 021 (nashopt Integration) -- plugin isolation: VERIFIED**

The 021 synthesis discusses the nashopt plugin's internal architecture (scorer, solver, payoffs, kalman, convergence, predictor). All internal imports stay within `conversus.plugins.nashopt.*`. External imports go only to `conversus.plugins.base` (the plugin ABC) and `conversus.schemas.features` (the FeatureSet/AgentFeatures/RoundFeatures models). No cross-plugin imports exist.

**4. Spec 022 (Kalman Convergence) -- nashopt package scope: VERIFIED**

The 022 synthesis references files within `conversus/plugins/nashopt/` (kalman.py, convergence.py, predictor.py). These all import exclusively from `conversus.plugins.nashopt.*`, `conversus.plugins.base`, and `conversus.schemas.features`. The Kalman implementation is correctly contained within the nashopt plugin boundary.

**5. Spec 023 (AMPL Config Optimizer) -- optimizer isolation: VERIFIED**

The optimizer plugin imports from `conversus.plugins.optimizer.*` (internal) and `conversus.plugins.base` (the plugin ABC). It does not import from `schemas/` at all -- it is even more isolated than the nashopt plugin. No cross-plugin imports to nashopt or scenarios exist.

**6. Plugin-to-plugin isolation: VERIFIED**

Zero cross-plugin imports across all three plugin packages:
- `nashopt/` does not import from `optimizer/` or `scenarios/`
- `optimizer/` does not import from `nashopt/` or `scenarios/`
- `scenarios/` does not import from `nashopt/` or `optimizer/`

Each plugin is a self-contained vertical slice: `plugins.base` -> plugin package -> (optionally) `schemas/`.

**7. schemas/ independence: VERIFIED**

`schemas/` imports only from itself (`conversus.schemas.*` submodules) and third-party dependencies (pydantic, stdlib). It has zero imports from `engine/`, `plugins/`, `domains/`, `linter/`, `web/`, or `mcp_server`. This confirms schemas is a true leaf package, safe to depend on from anywhere.

---

## Missed Opportunities

### 1. Domains docstring claims `plugins.base` dependency that does not exist

The `conversus/domains/__init__.py` docstring (line 8) states:

> Domain plugins are decoupled from the engine -- they import only from ``conversus.plugins.base`` and ``conversus.schemas``.

Neither `domains/base.py`, `domains/store.py`, `domains/api.py`, nor `domains/code_review/` imports from `conversus.plugins.base` or `conversus.schemas`. The domains package has its own `DomainPlugin` ABC in `domains/base.py` that is independent of the `plugins.base.Plugin` ABC. The `code_review/domain.py` coupling rule docstring is more precise -- it says "MAY import from conversus.domains.base, conversus.schemas, stdlib" -- but even the `schemas` permission is not exercised.

**None of the five synthesis files flagged this docstring-reality mismatch.** The 030 synthesis correctly verified that coupling rules are enforced at the code level but did not verify the docstring's dependency claims against actual imports.

**Impact**: Low (documentation-only), but misleading for new contributors who read the docstring and expect to find `plugins.base` imports in domains.

**Recommendation**: Update the `domains/__init__.py` docstring to accurately state: "Domain plugins are decoupled from the engine -- they import only from ``conversus.domains.base``, stdlib, and pydantic."

### 2. No synthesis verified the engine-to-plugins integration boundary

The engine (`engine/`) contains zero imports from `plugins/`, `domains/`, or `schemas/`. This means the plugin system is wired at a layer above the engine (likely a CLI or orchestration entry point not covered by these five specs). None of the syntheses explored where plugin execution actually happens. This is relevant because:

- The 030 synthesis's Dispute 1 identifies the absent gate lifecycle step and suggests dependency injection as the resolution pattern, but does not verify that any orchestration layer exists to perform that injection.
- The 022 synthesis's Remediation 6 (wire equilibrium scores from EquilibriumScorer to ConvergencePredictor) requires inter-plugin data flow, but no synthesis identifies the mechanism for this.

**Recommendation**: A follow-up audit should trace the orchestration layer that wires plugins into the engine lifecycle to confirm the injection pattern is feasible.

### 3. The `code_review/extractors.py` does not import from `domains/base.py`

The extractors module implements the `VariableExtractor` protocol declared in `domains/base.py`, but it does so structurally (duck typing / Protocol) without importing the protocol. This is fine for Python's `@runtime_checkable Protocol` pattern, but no synthesis explicitly verified that the extractors satisfy the protocol at runtime. The 029 synthesis states "Protocol-based pluggable extractors" (FR-002 MET) but does not verify the structural conformance was tested.

---

## Off-Base Assumptions

### 1. Spec 029 synthesis assumes `conversus.schemas` is a dependency of domains -- it is not

The 029 synthesis's referenced coupling rule says "MAY import from conversus.domains.base, conversus.schemas, stdlib." While this is a permission (MAY), the synthesis treats it as if it describes actual usage. In fact, the code_review domain has zero imports from `conversus.schemas`. The domain layer is fully independent of the schemas layer.

This is not wrong per se -- the permission exists for future use -- but it means the dependency chain `domains -> schemas` does not actually exist today. The 030 synthesis also references this permission but likewise does not verify it.

### 2. Spec 030 synthesis assumes domains will need `conversus.plugins.base` for gate integration

Dispute 1 of the 030 synthesis states: "The domains package must not import from `engine/` (coupling rule), but the gate needs the engine. Resolution: dependency injection." This is correct. However, the docstring in `domains/__init__.py` already claims a `plugins.base` dependency that does not exist. If the gate integration follows the dependency injection pattern (recommended), domains would depend on an injected callable, not on `plugins.base`. The assumed `plugins.base` dependency is a red herring.

---

## Actionable Recommendations

### P1 -- Must address

1. **Fix `domains/__init__.py` docstring** (line 8): Replace the claim about importing from `conversus.plugins.base` and `conversus.schemas` with the actual dependency list: `conversus.domains.base`, `pydantic`, `stdlib`. This prevents incorrect mental models in downstream spec reviews.

### P2 -- Should address

2. **Audit the orchestration layer**: Identify and document how plugins are loaded and executed within the engine lifecycle. The five synthesis files collectively identify three inter-component data flows that require orchestration:
   - Plugin hook execution at lifecycle points (spec 021: POST_PHASE_5, POST_DELIBERATION)
   - Inter-plugin data flow: EquilibriumScorer output -> ConvergencePredictor input (spec 022 Remediation 6)
   - Gate lifecycle injection into domains (spec 030 Dispute 1)

   None of these can be verified without understanding the orchestration layer.

3. **Verify VariableExtractor protocol conformance at test time**: The 029 synthesis marks FR-002 as MET (protocol-based pluggable extractors), but the extractors module does not import the protocol it implements. Add `isinstance(extractor, VariableExtractor)` assertions to the test suite to catch structural conformance regressions.

### P3 -- Nice to have

4. **Map the full dependency DAG**: Produce a formal dependency graph showing which packages are allowed to import from which, and verify it against actual imports. The current rules are distributed across docstrings in 5+ init files. A single source of truth (e.g., an architecture diagram or an import-linting tool like `import-linter`) would catch violations automatically.

5. **Reconcile the `code_review/domain.py` MAY-import-schemas permission with reality**: Either exercise the permission (if schemas types will be needed for gate integration) or narrow the docstring to match actual usage. Overly broad permissions accumulate coupling debt.

---

## Referenced Documentation

| Document | Location | Key Findings |
|----------|----------|--------------|
| Spec 021 synthesis | `specs/done/021-nashopt-integration/conversus-review/summary/final.md` | nashopt plugin isolation verified; imports only from `plugins.base` and `schemas.features` |
| Spec 022 synthesis | `specs/done/022-kalman-convergence/conversus-review/synthesis.md` | Kalman code contained within nashopt boundary; inter-plugin data flow (eq_score wiring) identified as P2 |
| Spec 023 synthesis | `specs/done/023-ampl-config-optimizer/conversus-review/summary/final.md` | Optimizer plugin fully isolated; does not even import from `schemas/` |
| Spec 029 synthesis | `specs/029-code-review-domain/conversus-review/summary/final.md` | code_review domain coupling rules verified; 030 base layer proven |
| Spec 030 synthesis | `specs/030-domain-plugin-architecture/conversus-review/summary/final.md` | Domain plugin ABC and scoring are engine-independent; gate integration requires DI pattern |
| `conversus/plugins/nashopt/__init__.py` | Package init | Exports: EquilibriumScorer, ConvergencePredictor, SolverResult, Kalman types |
| `conversus/plugins/optimizer/__init__.py` | Package init | Exports: ConfigOptimizer, solve_ampl, HAS_AMPL |
| `conversus/plugins/scenarios/__init__.py` | Package init | Exports: ScenarioPlugin, models, FileScenarioStore |
| `conversus/schemas/__init__.py` | Package init | Leaf package: game forms, features, objectives, construction, extraction, solvers |
| `conversus/domains/__init__.py` | Package init | Docstring inaccuracy: claims `plugins.base` and `schemas` imports that do not exist |
| `conversus/domains/code_review/__init__.py` | Package init | Coupling rules correctly documented; actual imports narrower than permissions |
| `conversus/domains/base.py` | Core ABC | Dependencies: pydantic + stdlib only. No upstream imports. |
| `conversus/domains/store.py` | Store implementations | Imports only from `domains.base`. No upstream imports. |
| `conversus/domains/api.py` | API router factory | Imports from `domains.base`, `domains.store`, `fastapi`. No engine/linter/mcp imports. |
| `conversus/domains/code_review/domain.py` | Domain implementation | Imports from `domains.base` and `code_review.extractors` only |
| `conversus/domains/code_review/extractors.py` | Variable extractors | Pure stdlib imports. Does not import `VariableExtractor` protocol (structural typing). |
| `conversus/plugins/base.py` | Plugin ABC | Dependencies: pydantic + stdlib. No engine imports. |

---

## Dependency DAG (Verified)

```
engine/         (no imports from plugins, domains, or schemas)
linter/         (no imports from plugins, domains, or schemas)

plugins/base    -> pydantic, stdlib
plugins/nashopt -> plugins/base, schemas/features, nashopt (optional)
plugins/optimizer -> plugins/base, amplpy/highspy (optional)
plugins/scenarios -> plugins/base

schemas/        -> pydantic, stdlib  (leaf package)

domains/base    -> pydantic, stdlib  (leaf package, independent of schemas and plugins)
domains/store   -> domains/base
domains/api     -> domains/base, domains/store, fastapi
domains/code_review -> domains/base  (does NOT exercise schemas permission)
```

All arrows point downward. No cycles. No boundary violations.
