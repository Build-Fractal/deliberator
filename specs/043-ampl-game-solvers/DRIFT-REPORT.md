# Drift Report: Specs 043 and 044 vs. Current Codebase

**Date**: 2026-04-05
**Specs**: `043-ampl-game-solvers`, `044-ampl-model-templates`
**Codebase snapshot**: post-spec-042 (`ExecutionProvider` refactor landed)

---

## Summary

Neither spec has been implemented yet — `game_solvers/` does not exist, the template library does not exist, and the `EquilibriumScorer` has no Tier 1 (AMPL) dispatch path. The critical question is whether the **ExecutionProvider refactor (spec 042)** breaks assumptions baked into the specs. The answer is: **it does not break solver semantics**, but it does create a naming confusion worth clarifying and has one structural implication for the template system. Details below.

---

## 1. Implementation Status

### What exists

| Component | State |
|---|---|
| `conversus/plugins/nashopt/scorer.py` | Full two-tier dispatch: nashopt → heuristic |
| `conversus/plugins/nashopt/solver.py` | nashopt wrapper, `HAS_NASHOPT` flag, `SolverResult` |
| `conversus/plugins/nashopt/payoffs.py` | All 8 mode heuristic payoff functions (spec 039 done) |
| `conversus/plugins/optimizer/ampl_model.py` | Config optimizer MIP model (spec 023 done) |
| `conversus/plugins/optimizer/ampl_solver.py` | AMPL/grid dispatch for config optimizer |

### What does not exist

| Component | Expected by spec | Status |
|---|---|---|
| `conversus/plugins/nashopt/game_solvers/` | spec 043 §4 File Structure | Not created |
| `BaseSolver` protocol + registry | spec 043 §4 | Not created |
| 6 mode-specific AMPL game solvers | spec 043 §3 | Not created |
| Three-tier dispatch in `EquilibriumScorer` | spec 043 §5 | Not implemented |
| `ampl-templates/` directory | spec 044 §3.1 | Not created |
| `.meta.yml` template metadata | spec 044 §3.2 | Not created |
| `conversus/plugins/ampl/bindings.py` | spec 044 §5 | Not created |
| AMPL model builder skill | spec 044 §4.1 | Not created |

Both specs are greenfield. There is no partial implementation to reconcile.

---

## 2. The ExecutionProvider Question

### What spec 042 changed

`engine/dispatch.py` and `engine/run.py` now route all agent dispatch through `ExecutionProvider.execute(task: ExecutionTask) → ExecutionResult`. Legacy `ModelProvider` instances are wrapped in `ModelProviderExecutionAdapter`. The `dispatch_agent` / `dispatch_phase` functions accept `AnyProvider = ExecutionProvider | ModelProvider` but internally convert everything to `ExecutionProvider` before calling.

### What specs 043 and 044 assume

Both specs describe **in-process optimization solvers** — Python code calling `amplpy` to build and solve AMPL models synchronously. The word "dispatch" in spec 043 §5 refers to the three-tier scoring dispatch within `EquilibriumScorer._compute_score()`, not engine dispatch of agents to LLMs. The word "provider" in spec 044 §3.3 refers to AMPL solver software (HiGHS, Gurobi, CPLEX) — not `ModelProvider` or `ExecutionProvider`.

**The specs are architecturally orthogonal to the ExecutionProvider refactor.** Game solvers live inside the plugin layer (`conversus/plugins/nashopt/`). Plugins receive a `DeliberationState` snapshot and return a `PluginResult`. They have no dependency on `engine/` modules and are explicitly prohibited from importing from `engine/` (see `conversus/plugins/base.py` docstring: "The plugin package imports nothing from engine/"). The `ExecutionProvider` protocol is an `engine/` concern.

### Verdict: No breaking conflict

The ExecutionProvider refactor does not break any solver assumption because game solvers are not dispatched through the execution layer. They run synchronously inside `EquilibriumScorer.execute()`, which is called by `execute_hooks()` in `base.py`. The execution provider is never involved.

---

## 3. Naming / Terminology Confusion to Address in Implementation

### 3.1 "solver" collision

The word "solver" now has three distinct meanings in the codebase:

| Term | Means |
|---|---|
| nashopt solver | `nashopt.check_equilibrium()` — exact Nash check on heuristic payoffs |
| AMPL game solver | Proposed spec 043 `GameSolver` — exact AMPL formulation per mode |
| AMPL config solver | Existing spec 023 `ampl_solver.py` — config MIP optimizer |

Spec 043's `PluginResult.data["solver"]` field already uses `"ampl-{mode}"` / `"nashopt"` / `"heuristic"` to distinguish. That is correct. But the import paths will need care: `conversus/plugins/nashopt/game_solvers/` sits inside the nashopt package, while the existing `conversus/plugins/optimizer/ampl_solver.py` is a different thing entirely. This is fine as long as implementation follows the spec's proposed file structure exactly.

### 3.2 `HAS_AMPL` symbol collision

`conversus/plugins/optimizer/ampl_model.py` already defines `HAS_AMPL` and exports it via `conversus/plugins/optimizer/__init__.py`. Spec 043 §5 uses `HAS_AMPL` in pseudocode for the three-tier scorer dispatch. During implementation, the scorer must import `HAS_AMPL` from the correct location. If the game solver tier uses its own `amplpy` instance, it may define its own `HAS_AMPL` in `game_solvers/base.py` — which is fine, but the name will shadow the optimizer's `HAS_AMPL` if both are imported in the same file. Implementation should either reuse the optimizer's flag (they both check `amplpy` + `highspy`) or define a canonical `conversus.plugins.ampl.HAS_AMPL` that both import from.

---

## 4. Structural Drift: Spec 044 Template Location vs. Package Layout

Spec 044 §3.1 places templates at `ampl-templates/{category}/{name}.mod` (relative to something unspecified), and §6 FR-005 requires templates to be "loadable via `importlib.resources` (pip-installable)."

The current package has no `ampl-templates/` directory anywhere. The existing `ampl_model.py` embeds the config optimizer model as a **Python string constant** — not a `.mod` file. Spec 043 §9 Constraints says "Game solver models are AMPL strings embedded in Python (not .mod files) for portability." Spec 044 contradicts this for the template library: it wants actual `.mod` files with `importlib.resources`.

**This is a direct conflict between spec 043 and spec 044:**
- 043: AMPL models embedded as Python strings in each solver module
- 044: AMPL models as `.mod` files loadable via `importlib.resources`

In practice both can coexist — the game solver modules (043) use inline strings, while the template library (044) uses `.mod` files. But the 6 core templates in spec 044 Phase 1 are explicitly the "6 templates from spec 043" (cooperative Nash, red-blue minimax, etc.). This means the same AMPL model must live in two forms: inline string in the solver module AND as a `.mod` file in the template library.

**Recommendation for implementation plan**: resolve this before coding. Either:
- The game solver modules load their AMPL strings from the template `.mod` files (spec 044 approach, single source of truth), or
- The template library generates `.mod` files from the solver modules' string constants (spec 043 approach, keep solvers self-contained)

The `importlib.resources` requirement in spec 044 FR-005 is stronger and more maintainable. The implementation should follow it: solvers load `.mod` files from `ampl-templates/`, not hardcode strings. This means spec 043 Phase 1 and spec 044 Phase 1 must be built together, not sequentially.

---

## 5. Mode Coverage Gaps

### 5.1 Payoff function coverage vs. game solver coverage

Heuristic payoffs (spec 039, done) cover all 8 modes. The nashopt solver's `build_payoff_matrix()` covers only 4 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue). Spec 043 Phase 1 adds AMPL game solvers for 6 modes (adds fair-division and resource-allocation). Negotiation and mechanism-design remain deferred.

The `EquilibriumScorer._compute_score()` currently does nashopt-or-heuristic. When adding the AMPL tier, the scorer will call the game solver for modes where one exists and fall through to nashopt (if available) for all others. The fallback chain as described in spec 043 §4 is sound and consistent with what exists.

### 5.2 `build_payoff_matrix()` scope

`solver.py`'s `build_payoff_matrix()` raises `ValueError` for modes beyond the 4 it supports. Negotiation, resource-allocation, fair-division, and mechanism-design will fall through to the heuristic in the nashopt tier even after game solvers exist for them (because nashopt only covers the 4 modes). This is the correct behavior — the spec says nashopt is Tier 2 and falls through to heuristic. No code change needed for existing behavior; only the Tier 1 AMPL path is added.

---

## 6. Plugin Protocol: `execute(state)` Still the Right Interface

Spec 043 proposes `GameSolver.solve(features, timeout)` as the protocol method. The `EquilibriumScorer.execute(state: DeliberationState)` method extracts features internally (via `_try_extract_features` or `_round_features_from_state`) and passes `RoundFeatures` to the solver. This two-step — engine passes `DeliberationState` to plugin, plugin extracts features internally — is intact and unchanged by spec 042.

The spec's pseudocode for the three-tier scorer (`_compute_score(features, mode)`) aligns exactly with the existing `_compute_equilibrium_score(mode, features, config)` function signature in `scorer.py`. No restructuring is needed; the AMPL tier is added as an early-return inside that function.

---

## 7. `solver_tier` Config Option

Spec 043 §10 Open Question 4 proposes adding `solver_tier: "ampl" | "nashopt" | "heuristic" | "auto"` to plugin config. The existing scorer reads config via `self.plugin_config` (set in `Plugin.__init__`). Adding this key requires no infrastructure change — the config dict already flows through. This is additive and non-breaking.

---

## 8. Self-Modeling During Deliberation (Spec 044)

Spec 044 §4.2 / FR-013 requires solving optimization problems "DURING a deliberation phase (not just post-hoc)." This has an implication for the plugin system that the spec does not address: plugins currently run at hook points (`POST_PHASE_5`, `POST_DELIBERATION`) — they are post-hoc by design. The self-modeling capability described in spec 044 (agent reads features, selects template, binds, solves, interprets within a single deliberation phase) would require either:

1. A new hook point triggered mid-phase, or
2. The agent running the AMPL solve as part of its LLM prompt response (e.g., via tool use if on an `ExecutionProvider` with `supports_tool_use=True`), or
3. A new agent skill loaded into the agent's context that the LLM calls during synthesis

This is not a blocker for spec 043 (game solvers are post-hoc scoring). But it is an unresolved architecture question for spec 044 Phase 2. The self-modeling capability cannot be built purely within the existing plugin hook system.

---

## 9. Implementation Prerequisites

Before coding either spec, confirm:

1. **`amplpy` + `highspy` dependency model**: The optimizer already imports them and sets `HAS_AMPL`. Game solvers will need the same. Confirm `conversus-ampl` premium package scope covers both the config optimizer and game solvers, or whether they ship separately.

2. **Resolve inline-string vs. `.mod` file conflict** (see §4 above). This affects spec 043 Phase 1 scope.

3. **`GAME_SOLVER_REGISTRY`**: The spec describes a registry but doesn't specify where it lives. Given that the config optimizer has no registry (just a single `ampl_solver.py` dispatch), a simple `dict[str, GameSolver]` in `game_solvers/__init__.py` is the natural pattern.

4. **Spec 044 Phase 1 depends on spec 043 Phase 1**: The 6 core templates in 044 are the same models as the 6 solvers in 043. These should be built together in a single implementation pass.

---

## 10. What the Specs Got Right

- The three-tier fallback architecture (AMPL → nashopt → heuristic) aligns perfectly with the existing two-tier code. Adding Tier 1 is surgical: one early-return block in `_compute_equilibrium_score()`.
- `GameResult` and `GameSolver` as frozen dataclass and Protocol respectively matches the conventions established by `SolverResult` and the existing plugin base class.
- Keeping AMPL as an optional runtime dependency with `HAS_AMPL` flag is consistent with how the config optimizer already works.
- `PluginResult.data["solver"]` reporting which tier ran is already the pattern (`"nashopt"` vs `"heuristic"` in existing code).
- The plugin isolation principle (plugins don't import from `engine/`) means the ExecutionProvider refactor has zero impact on any game solver or template library code.
