# Plugin-Engineer Review: Spec 023 -- AMPL Config Optimizer

**Reviewer**: plugin-engineer
**Spec**: `specs/done/023-ampl-config-optimizer/spec.md`
**Implementation files reviewed**: `ampl_model.py`, `ampl_solver.py`, `optimizer.py`, `__init__.py`, `models.py`, `tests/test_ampl.py`

---

### Executive Summary

Spec 023 adds AMPL/HiGHS MIP solving to the existing config optimizer plugin, introduces a general-purpose `solve_ampl()` API, and wires both through a dispatch layer that falls back to grid search when AMPL is unavailable. The plugin architecture is clean: `optimizer.py` delegates to `ampl_solver.py`'s `solve_config()`, which dispatches to AMPL or grid search transparently. The plugin interface (`PluginResult`), hook point (`PRE_EXECUTION`), and output format (`OptimalConfig`) are unchanged, satisfying the spec's backward compatibility requirement.

The dispatch layer in `ampl_solver.py` is well-structured. The separation of concerns -- `ampl_model.py` (formulation + solve), `ampl_solver.py` (dispatch + fallback), `optimizer.py` (plugin interface) -- follows the existing plugin architecture patterns. The `HAS_AMPL` flag propagates correctly, the timeout/fallback logic is robust, and solver metadata flows through to `PluginResult.data`.

The general-purpose `solve_ampl()` API (FR-007) is a strong addition. It supports model strings, file paths, scalar and indexed data parameters, timeout, and solver selection. The API is exported from `__init__.py` and well-documented. However, it has several design gaps: no `data_file` parameter for `.dat` files, no way to extract constraint duals or sensitivity information, and the file-detection heuristic (checking for `.mod` suffix) is fragile.

My most critical finding: the `solve_ampl()` API's error handling is asymmetric with `solve_with_ampl()`. The config-specific function returns `None` on failure (swallowing errors), while the general-purpose function raises `ImportError` on missing amplpy but lets all other exceptions propagate uncaught. Neither approach is ideal. A consistent error-handling strategy across both functions would improve the API's usability and debuggability.

---

### Alignment

- **[Plugin interface unchanged]** (`optimizer.py`, L30-136): `ConfigOptimizer` remains a `Plugin` subclass with `hooks = [HookPoint.PRE_EXECUTION]`. The `execute()` method returns `PluginResult` with the same data keys as before (`recommended_rounds`, `recommended_agent_count`, etc.) plus the new `solver` key. Existing consumers of `PluginResult.data` are unaffected. This directly satisfies the spec requirement: "What does not change: Plugin interface. Hook point. Output format."

- **[Dispatch transparency]** (`ampl_solver.py`, L64-111): `solve_config()` returns `tuple[OptimalConfig, dict]` regardless of backend. The plugin does not need to know which solver ran -- it reads `solver_meta["solver"]` for reporting but makes no behavioral decisions based on it. This is clean plugin architecture: the solver is an implementation detail, not a plugin concern.

- **[Backward compatibility of PluginResult.data]** (`optimizer.py`, L106-118): All fields from the pre-023 plugin are preserved: `recommended_rounds`, `recommended_agent_count`, `recommended_iterations`, `estimated_total_launches`, `estimated_quality`, `solver_status`, `budget_used`. The new fields (`solver`, `solve_time_ms`, `gap`) are additive. The `solver` field is always present; `solve_time_ms` and `gap` are conditionally added only when AMPL solves. This is a non-breaking extension. Tests in `TestPluginSolverField` verify the field set.

- **[General-purpose `solve_ampl()` API]** (`ampl_model.py`, L315-404): The function signature `solve_ampl(model, data, solver, timeout)` is clean and general. It handles both model strings and `.mod` file paths. Data parameters support both scalar values and indexed dicts. The return dict includes `solve_result`, `objective_value`, `solve_time_ms`, and `variables`. This satisfies FR-007 (expose a general-purpose function), FR-008 (supports MIP, LP, NLP, MINLP via solver), and FR-009 (file or string model).

- **[`__init__.py` exports]** (`__init__.py`, L1-22): The package exports `ConfigOptimizer`, `HAS_AMPL`, and `solve_ampl` via `__all__`. This gives users clean import paths: `from conversus.plugins.optimizer import solve_ampl`. The `HAS_AMPL` export lets callers check AMPL availability before attempting a solve.

- **[AMPL resource cleanup]** (`ampl_model.py`, L311-312, L403-404): Both `solve_with_ampl` and `solve_ampl` use `try/finally` to ensure `ampl.close()` is called. The test `test_solve_ampl_close_called` verifies this. Resource cleanup is critical for AMPL (which holds solver licences and temp files).

---

### Missed Opportunities

- **[Asymmetric error handling between `solve_with_ampl` and `solve_ampl`]**: `solve_with_ampl` returns `None` for three distinct failure conditions (no amplpy, infeasible, no variable selected) and never raises exceptions. `solve_ampl` raises `ImportError` for no amplpy and lets all other exceptions propagate. This asymmetry is confusing: a user who learns the API through `solve_ampl` expects exceptions, then encounters `None`-based error signaling in `solve_with_ampl`. A consistent pattern -- either both return result objects with status fields, or both raise typed exceptions -- would be more predictable. Impact: **high**.

- **[No `.dat` file support in `solve_ampl()`]**: The general-purpose API accepts a `data` dict for parameters but does not support AMPL `.dat` files. Many AMPL users maintain separate `.mod` and `.dat` files. Adding a `data_file: str | None = None` parameter that calls `ampl.read_data(data_file)` would round out the API for standard AMPL workflows. FR-009 says "Model files MUST be loadable from disk" but does not mention data files; adding data file support would exceed the spec but improve usability. Impact: **medium**.

- **[File-detection heuristic is fragile]** (`ampl_model.py`, L354): The check `model.strip().endswith(".mod") and "\n" not in model.strip()` determines whether `model` is a file path or a model string. This fails for: (a) AMPL files with other extensions (`.ampl`, `.run`), (b) file paths with trailing whitespace, (c) model strings that happen to end with ".mod" on a single line. A more robust approach: accept `model: str | Path`, where `Path` objects are always treated as files, or add a `model_file: Path | None` parameter separate from `model: str`. Impact: **medium**.

- **[No way to extract duals or sensitivity info from `solve_ampl()`]**: The return dict includes variables and objective but not constraint duals (`ampl.get_constraint(...).dual()`) or sensitivity ranges. For LP problems, duals are often more valuable than primal values. Adding an `include_duals: bool = False` parameter would serve LP/MILP users. Impact: **low** (not required by spec).

- **[`solver_timeout` config key naming inconsistency]**: The `optimizer.py` plugin config uses `solver_timeout` (L91), `ampl_solver.py` uses `solver_timeout` as a parameter name (L70), but `ampl_model.py` uses `timeout` (L319). The `solve_ampl()` public API uses `timeout`. The config key `solver_timeout` is more descriptive, but the inconsistency between the plugin config namespace and the API parameter name means a user of `solve_ampl()` must remember the different name. Impact: **low**.

- **[Plugin config key `cost_per_agent_launch` vs API param `cost_per_launch`]**: `optimizer.py` L90 reads `config.get("cost_per_agent_launch", 1.0)` but passes it to `solve_config` as `cost_per_launch`. `ampl_model.py` uses `cost_per_launch`. The config key differs from the API parameter. Either standardize on one name or document the mapping explicitly. Impact: **low**.

- **[No plugin config key to force a specific solver]**: `optimizer.py` L38-39 documents a `solver` config key ("ampl-highs" or "grid-search") but never reads it. The dispatch in `ampl_solver.py` is controlled entirely by `HAS_AMPL`. A user who wants to force grid search (e.g., for reproducibility) cannot do so via config. Impact: **medium**.

---

### Off-Base Assumptions

- **[FR-010: "API MUST NOT require AMPL license"]**: The implementation correctly uses the AMPL Community Edition (free, bundled with `amplpy`). However, the spec does not document the Community Edition limitation: problems larger than a certain size require a commercial AMPL licence. For the config optimizer (135 variables), this is not an issue. For the general-purpose `solve_ampl()` API, users may hit licence limits without warning. The spec should document the Community Edition constraint or the API should catch and report AMPL licence errors with a helpful message. This is not a code defect but a documentation gap.

- **[Spec claims "HiGHS is free and sufficient for MIP/LP"]**: True, but HiGHS does not support NLP or MINLP (FR-008 claims these are supported "solver permitting"). The general-purpose API passes the solver name through, so NLP/MINLP would require a different solver (e.g., Bonmin, Ipopt). The API supports this by design (user passes `solver="ipopt"`), but the spec implies HiGHS handles all four problem types. This should be clarified: HiGHS for MIP/LP, other solvers for NLP/MINLP.

---

### Actionable Recommendations

1. **Unify error handling across `solve_with_ampl` and `solve_ampl`** (Priority: P1)
   - **Current state**: `solve_with_ampl` returns `None` for three failure modes. `solve_ampl` raises `ImportError` for missing amplpy and propagates other exceptions.
   - **Proposed change**: Define a `SolveResult` protocol or base class. `solve_with_ampl` returns it with a `status` field. `solve_ampl` returns a dict with `solve_result` and `error` fields. Neither function silently swallows exceptions that the caller cannot distinguish. Alternatively, have `solve_with_ampl` raise a `SolverInfeasibleError` or return an `OptimalConfig` with `solver_status="infeasible"` instead of `None`.
   - **Rationale**: API consistency. Two public functions in the same module with incompatible error-handling conventions create confusion and bugs.
   - **Risk if ignored**: Callers of `solve_with_ampl` must guess whether `None` means "install amplpy" or "your problem is infeasible." The test `test_ampl_solve_returns_none_without_amplpy` documents this ambiguity.

2. **Implement the `solver` plugin config key** (Priority: P2)
   - **Current state**: `optimizer.py` L38-39 documents `solver: str` in the docstring but the code never reads it.
   - **Proposed change**: Read `config.get("solver")`. If set to `"grid-search"`, bypass AMPL even when `HAS_AMPL` is True. If set to `"ampl-highs"` and `HAS_AMPL` is False, log a warning. If unset, auto-detect (current behavior).
   - **Rationale**: The docstring promises this feature. Users need solver pinning for reproducibility (grid search is deterministic; AMPL may vary across versions) and for debugging (isolating solver-specific issues).
   - **Risk if ignored**: Dead documentation. Users who try to configure `solver: grid-search` in their plugin config will be silently ignored.

3. **Make file detection in `solve_ampl()` more robust** (Priority: P2)
   - **Current state**: `model.strip().endswith(".mod") and "\n" not in model.strip()` (L354).
   - **Proposed change**: Accept `model: str | Path`. If `isinstance(model, Path)` or `Path(model).suffix in (".mod", ".ampl", ".run")`, treat as file. Otherwise, treat as model string. Or add a separate `model_file` parameter.
   - **Rationale**: The current heuristic produces false positives (model strings ending in ".mod") and false negatives (files with `.ampl` extension).
   - **Risk if ignored**: Users with non-standard AMPL file extensions must work around the detection logic.

4. **Standardize cost parameter naming** (Priority: P3)
   - **Current state**: Plugin config: `cost_per_agent_launch`. API parameter: `cost_per_launch`. Model data key: `cost_per_launch`.
   - **Proposed change**: Use `cost_per_launch` everywhere. In the plugin, accept both `cost_per_launch` and `cost_per_agent_launch` (with deprecation warning for the latter).
   - **Rationale**: Naming consistency reduces cognitive load. The plugin config key is the user-facing name and should match the API.
   - **Risk if ignored**: Minor confusion when users cross-reference plugin config with API docs.

5. **Document AMPL Community Edition limits** (Priority: P3)
   - **Current state**: No documentation of AMPL licence constraints.
   - **Proposed change**: Add a note to the `solve_ampl()` docstring: "Note: The free AMPL Community Edition supports problems up to 500 variables and 500 constraints. Larger problems require a commercial AMPL licence."
   - **Rationale**: Users of the general-purpose API may hit silent licence limits.
   - **Risk if ignored**: Confusing error messages when users exceed the Community Edition limits.

6. **Clarify NLP/MINLP solver requirements** (Priority: P3)
   - **Current state**: FR-008 claims support for NLP and MINLP "solver permitting." HiGHS does not support these.
   - **Proposed change**: Update FR-008 or the `solve_ampl()` docstring to specify: "MIP and LP are supported by the default HiGHS solver. NLP requires `solver='ipopt'`, MINLP requires `solver='bonmin'` (not bundled; must be installed separately)."
   - **Rationale**: FR-008 creates an expectation that the default solver handles all four problem types.
   - **Risk if ignored**: Users pass NLP problems to HiGHS and get cryptic solver errors.

---

### Referenced Documentation

- `conversus/plugins/optimizer/optimizer.py` -- L30-46 (ConfigOptimizer class/docstring), L48-136 (execute method), L38-39 (solver config key documented), L90 (cost_per_agent_launch)
- `conversus/plugins/optimizer/ampl_solver.py` -- L64-111 (solve_config), L114-186 (_solve_with_ampl_fallback), L32-57 (AMPLSolverResult)
- `conversus/plugins/optimizer/ampl_model.py` -- L29-34 (HAS_AMPL), L315-404 (solve_ampl), L218-312 (solve_with_ampl), L354 (file detection)
- `conversus/plugins/optimizer/__init__.py` -- L19-22 (exports)
- `tests/test_ampl.py` -- L304-334 (TestPluginSolverField), L484-591 (TestSolveAMPLAPI), L598-649 (TestTimeoutFallback)
- `specs/done/023-ampl-config-optimizer/spec.md` -- FR-007 (general-purpose API), FR-008 (MIP/LP/NLP/MINLP), FR-009 (file loading), FR-010 (no licence), FR-012 (solve_time_ms, gap), Section 6 (constraints)
