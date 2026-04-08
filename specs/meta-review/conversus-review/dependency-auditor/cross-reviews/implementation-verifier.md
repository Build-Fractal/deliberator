# Cross-Review: dependency-auditor reviewing implementation-verifier

**Date**: 2026-04-01
**Phase**: 2 — Cross-Reviews

---

## Dangerous Contradictions

### DC-1: Off-Base Assumption #1 (solver.py vs. plugin wrapper) confirms an import-boundary blind spot in the 021 synthesis

The implementation-verifier identifies that spec 021's synthesis repeatedly references `PluginResult` returns in `solver.py`, but `solver.py` is a pure function module returning `SolverResult`. The `PluginResult` construction happens in the plugin wrapper (`equilibrium_scorer.py`). My audit verified that the nashopt plugin's internal architecture (`scorer, solver, payoffs, kalman, convergence, predictor`) has all imports within `conversus.plugins.nashopt.*`. The misattribution in the 021 synthesis is not a dependency violation — both files are in the same package — but it reveals that the synthesis reviewers treated the solver module and the plugin wrapper as the same component. This means findings about `PluginResult` error-path behavior (which my audit touches indirectly via "plugin hook execution at lifecycle points") may need reattribution.

### DC-2: Implementation-verifier's "immediate fix" list does not distinguish dependency-safe from dependency-risky changes

The implementation-verifier lists 5 immediate fixes and 3 architecture improvements. From a dependency perspective:
- Fixes 1 (DomainScore.variables), 2 (HAS_AMPL guard), 3 (innovation sequence), 5 (BayesianGame keys) are **dependency-safe**: they modify a single file within a single package boundary.
- Fix 4 (wire Q/R from plugin config) requires `predictor.py` to read config keys and pass them through to `convergence.py -> kalman.py`. This is intra-package (all within `plugins/nashopt/`) so it is also **dependency-safe**, but it adds a new data flow path through 3 files.
- Architecture improvement 8 (scaffold extension search) modifies `base.py` which is imported by `code_review/domain.py` — this is a **cross-boundary change** that affects the domains/code_review dependency arrow.

The implementation-verifier does not flag which fixes cross boundaries. This distinction matters for sequencing: cross-boundary changes need testing in both the base and subclass, while single-file fixes do not.

### DC-3: Verification of store protocol compliance is import-validated but not structurally validated

The implementation-verifier confirms that `JSONLStore` and `SQLiteStore` implement all 5 `DomainStore` protocol methods. My audit confirms `store.py` imports only from `domains/base`. However, the implementation-verifier also notes that `code_review/extractors.py` does NOT import the `VariableExtractor` protocol it implements (structural typing). These two findings use different validation standards: protocol compliance is verified by method enumeration for stores but assumed by duck typing for extractors. A consistent approach would verify both structurally.

---

## Tensions

### T-1: Scope of "immediate fix" vs. dependency impact analysis

The implementation-verifier's recommendation list is ordered by code-level urgency. My perspective would reorder by dependency impact: fixes within leaf packages (schemas, domains/base) first, then fixes that cross boundaries, then fixes that require new integration mechanisms. The implementation-verifier and I agree on what needs fixing but would sequence differently.

### T-2: The `_matches_filters` silent ignore

The implementation-verifier flags `_matches_filters` silently ignoring unknown filter keys as a data integrity concern. My audit confirms this is within `store.py`, which is part of the domains layer and has no upstream imports. The fix (adding `logger.warning()`) is dependency-safe. However, the implementation-verifier's concern about unfiltered data return implies a contract between the store and its callers that my audit does not verify — I verify import boundaries, not behavioral contracts.

### T-3: AMPL model `.mod` file extraction

The implementation-verifier recommends extracting `CONVERSUS_CONFIG_MODEL` from a Python string constant to a `.mod` file. From a dependency perspective, this would introduce a filesystem dependency: `ampl_model.py` would need to read from a file path at runtime. Currently the model is self-contained. The `.mod` file approach adds a deployment dependency (the file must be distributed with the package). The implementation-verifier frames this as a code organization fix; I note it changes the dependency surface.

---

## Safe Agreements

### SA-1: Bug identification accuracy is high across both reviews

The implementation-verifier's 18/21 verification rate (86%) confirms that the synthesis findings I used as inputs for my dependency audit are reliable. The 2 inaccuracies are misattributions within the same package, not across dependency boundaries, so they do not affect my audit's conclusions.

### SA-2: The coupling rules declared in docstrings match actual code

Both reviews confirm that declared coupling rules (in `__init__.py` docstrings and synthesis claims) match actual imports. My audit found one docstring inaccuracy (`domains/__init__.py` claiming `plugins.base` imports). The implementation-verifier did not flag this specific docstring but confirmed the underlying architectural claims are correct.

### SA-3: Frozen Pydantic models and pure-function patterns are verified

The implementation-verifier confirmed all 5 domain state models are frozen. My audit confirmed domains/base has only pydantic + stdlib dependencies, which is consistent with frozen model usage. Both confirm the architectural foundation is sound.
