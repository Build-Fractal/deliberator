# Drift Report: 007-game-engine

**Spec**: `specs/007-game-engine/spec.md`
**Checked against**: `engine/phases.py`, `engine/dispatch.py`, `engine/config.py`, `engine/models.py`, `conversus/plugins/`
**Date**: 2026-04-05

---

## DONE

These spec sections match what is implemented.

- **Plugin base class** (spec §3, FR-006/007/008): `conversus/plugins/base.py:126–208` implements `Plugin` ABC with `name`, `hooks`, and `execute(state) → PluginResult`. `DeliberationState` exposes `mode`, `round`, `agents`, `synthesis`, `history`, `output_dir` (FR-007). `PluginResult` has `recommendation`, `data`, `advisory` (FR-008). Line 197 matches the spec's API shape.

- **HookPoint enum** (spec §3 "Plugin Lifecycle Hooks"): All four hook points are implemented — `PRE_EXECUTION`, `POST_PHASE_5`, `POST_DELIBERATION`, `POST_ARBITRATION` at `conversus/plugins/base.py:33–44`. Matches spec exactly.

- **Plugin loading with graceful degradation** (spec §3, FR-003/FR-005): `load_plugins()` at `base.py:229–295` uses `importlib.import_module`, logs a warning and continues if a package is not installed. Plugin failures do not crash the run.

- **Plugin output to `plugins/` subdirectory** (spec §3, FR-004): `execute_hooks()` at `base.py:474–476` creates `{output_dir}/plugins/` and writes per-plugin JSON there. Core artifacts are never modified.

- **Plugin config in `conversus.yml`** (spec §3, FR-001): `conversus/plugins/config.py` parses `plugins:` list with `name`, `package`, `config` fields. Duplicate name rejection is implemented.

- **EquilibriumScorer** (spec §2, §4): Implemented at `conversus/plugins/nashopt/scorer.py`. Hooks `POST_PHASE_5` and `POST_DELIBERATION`. Computes score in `[0.0, 1.0]`, produces `equilibrium_score`. Has heuristic path + nashopt solver dispatch with timeout (`base.py:124–154`).

- **ConvergencePredictor** (spec §2, §4): Implemented at `conversus/plugins/nashopt/predictor.py`. Hook `POST_PHASE_5`. Produces CONVERGE/STAGNATE/UNCERTAIN prediction with confidence and estimated rounds remaining. Uses Kalman filter (`kalman.py`) as the "gnep-learn active learning" analog.

- **ConfigOptimizer** (spec §2, §4): Implemented at `conversus/plugins/optimizer/optimizer.py`. Hook `PRE_EXECUTION`. Accepts `budget` and quality constraints, dispatches to AMPL/HiGHS MIP solver or grid search fallback. Produces `optimal_config`.

- **Feature extraction schema** (spec §4 "Feature Extraction"): `conversus/schemas/features.py` defines `AgentFeatures`, `RoundFeatures`, `FeatureSet`. Fields cover `recommendation_count`, `withdrawn_count`, `concession_rate`, `dispute_count`, `convergence_count`. Feature schemas exist per mode in `schema/features/`.

- **Objective function templates** (spec §11 Approach 2): Implemented in `schema/objective-functions/`. Templates exist for `competitive-selection.yml`, `cooperative-integration.yml`, `territory-claiming.yml`, `risk-severity.yml`, `budget-constrained.yml`, and many others. Matches spec §11 table.

- **Cross-plugin data flow** (spec §3 Principle 4): `produces`/`consumes` declarations and topological sort implemented at `base.py:311–404`. `ConvergencePredictor` consumes `equilibrium_score` produced by `EquilibriumScorer` (predictor.py:181).

- **nashopt optional dependency** (spec §8, §9): `pyproject.toml:37–51` has `nashopt`, `jax`, `jaxlib` as optional extras. Core has zero numerical dependencies. `HAS_NASHOPT` flag in `nashopt/solver.py` enables heuristic fallback.

- **Scenario storage** (spec §12): Implemented in `conversus/plugins/scenarios/`. `FileScenarioStore` writes `scenarios/{id}.yml`. `ScenarioPlugin` auto-saves at `POST_DELIBERATION`. `ScenarioStore` protocol supports future backend swapping.

---

## DIVERGED

Things where code deviates from what the spec describes.

- **Plugin `execute()` signature** (spec §3 "Plugin API" code block, line 138): Spec shows `execute(self, state: DeliberationState, config: dict) → PluginResult`. Implemented signature is `execute(self, state: DeliberationState) → PluginResult` (`base.py:197`). Config is stored at init time in `self.plugin_config` instead of passed per-call. Functional difference: plugins cannot receive dynamic config per execution.

- **Plugin output filenames** (spec §3, SC-002 line 298): Spec promises `plugins/equilibrium-score.json`. Actual filename written is `{name}-{hook.value}-round-{N}.json` (e.g., `equilibrium-scorer-post_phase_5-round-1.json`) per `base.py:503–504`. SC-002 will fail as written.

- **Package separation** (spec §8, §9 "conversus-nashopt"): Spec defines `conversus-nashopt` as a separate `pip install` package. Code ships `EquilibriumScorer`, `ConvergencePredictor`, `ConfigOptimizer`, and `ScenarioPlugin` all inside the monolithic `conversus` package under `conversus/plugins/`. The `packages/core.toml`, `packages/scenarios.toml`, `packages/solvers.toml` suggest future splitting, but today there is one package.

- **Stagnation Forecaster** (spec §2 Plugin table, line 48): Listed as a distinct paid plugin. Not implemented as a named plugin class. Forecasting functionality is absorbed into `ConvergencePredictor` (PRE_EXECUTION hook not present on it; it only registers `POST_PHASE_5`).

- **`conversus-embeddings` tier** (spec §8, §10): Spec defines a "Tier 1" embeddings plugin using `sentence-transformers` for semantic stagnation and convergence scoring. No embeddings plugin exists anywhere in `conversus/plugins/`. The embedding-based features described in §10 are absent.

---

## MISSING

Spec promises not present in the codebase.

- **Engine wiring of plugin hooks** (spec §5 Phase 1, FR-002): `execute_hooks()` exists but is **never called from `engine/phases.py`**. The comment at `base.py:439–451` explicitly acknowledges this: "The actual wiring into `engine/phases.py` is deferred to a follow-up PR." No call sites for `execute_hooks`, `load_plugins`, or `HookPoint` exist in any file under `engine/`. Plugins are fully implemented but dead — they cannot run.

- **`plugins:` field in `EngineConfig`** (spec FR-001/FR-002): `engine/config.py` has no `plugins` field in `EngineConfig` (line 75–91). `parse_config()` does not read or validate the `plugins:` YAML key. Plugin config parsing (`conversus/plugins/config.py`) is never invoked from the config layer.

- **SC-001 / SC-002** (spec §7): Both success criteria are unachievable today. SC-001 ("run with `plugins: []` produces identical output") fails because the field isn't parsed. SC-002 ("equilibrium scorer produces `plugins/equilibrium-score.json`") fails because (a) the hook isn't called and (b) the filename format is wrong.

- **LLM-guided gap-filling** (spec §11 Approach 3): The interactive pipeline (symbolic parsing → gap identification → LLM questions → objective construction) is not implemented. `conversus/schemas/construction.py` exists but the interactive question-asking workflow described in §11 steps 1–6 is absent.

- **Approach 4: Embedding-Assisted Feature Mapping** (spec §11 Approach 4): Not implemented anywhere.

- **`/conversus replay` command** (spec §12 "Replay Workflow"): The CLI replay workflow (`/conversus replay {id} --target ...`) described in §12 is not implemented. `ScenarioPlugin` saves scenarios, but no CLI entry point or replay orchestration exists.

- **Scenario storage in `conversus.yml`** (spec §12): No mechanism to declare a `scenario_id` to replay in the config file. The replay workflow is file-save only; loading to re-run is unimplemented.

---

## UNDOCUMENTED

Code features not mentioned in spec 007.

- **Cross-plugin `produces`/`consumes` dependency DAG** (`base.py:311–404`): Topological sort of plugins so producers run before consumers. Spec 007 says nothing about inter-plugin data dependencies; this is a spec 024 concern wired into the base.

- **`RoundState.plugin_results`** (`base.py:77`): Plugin results are persisted per-round in `RoundState` and forwarded into `DeliberationState.plugin_results` for cross-hook consumption. Spec 007 does not describe this accumulation mechanism.

- **AMPL/HiGHS MIP solver** (`conversus/plugins/optimizer/ampl_solver.py`, `ampl_model.py`): Spec §4 mentions `nash_mpqp` for parametric config optimization. Code uses AMPL + HiGHS as the MIP backend with `amplpy`/`highspy` optional deps (pyproject.toml:47–49). `nash_mpqp` is not used.

- **Kalman filter convergence prediction** (`conversus/plugins/nashopt/kalman.py`): Spec §4 references "gnep-learn's active learning approach" with Kalman filter. Code implements its own pure-Python Kalman filter (`kalman.py`) rather than calling the `gnep-learn` library. `gnep-learn` is not a dependency.

- **`DuplicateProducerError`** (`base.py:308`): Error raised when two plugins claim the same `produces` key. Not mentioned in spec.

- **Domain system** (`conversus/domains/`): A full domain plugin layer (`code_review`, with stubs for `medical`, `legal`) providing domain-specific feature extractors and agent presets. Not mentioned in spec 007 at all.

- **Solver registry / `conversus/schemas/solvers.py`**: Solver abstraction for dispatching between heuristic, nashopt, and AMPL backends. Spec 007 does not describe this layer.

- **`conversus-embeddings` referenced but absent**: Spec §8/§10 promises this tier exists. It does not — not even a stub.

---

## CONTRADICTIONS

Outright conflicts where spec says X and code does Y.

- **Free core depends only on PyYAML** (spec §9 "Must NOT", line 337): Spec states the free tier runs with "only PyYAML." `pyproject.toml:14–22` lists `anthropic`, `fastapi`, `httpx`, `pydantic`, `openai`, `supabase`, `uvicorn`, `rich`, `mcp` as non-optional core dependencies. PyYAML is one of many, not the only one. (The spirit of the constraint — no numerical solver in core — is respected.)

- **Plugin output filename** (spec SC-002 / §3 file tree, line 125): Spec shows `plugins/equilibrium-score.json` as the output artifact name. Code produces `equilibrium-scorer-post_deliberation-round-1.json`. These are different filenames; SC-002 is a direct contradiction.

- **`execute(self, state, config)` vs `execute(self, state)`** (spec §3 line 138 vs `base.py:197`): Spec explicitly shows `config: dict` as a second parameter. Code removed it in favor of `self.plugin_config` set at construction. Any third-party plugin written against the spec's API will fail to load.
