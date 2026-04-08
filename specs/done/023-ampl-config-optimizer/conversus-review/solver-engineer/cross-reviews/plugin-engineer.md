# Cross-Review of plugin-engineer's Review

**Cross-reviewer**: solver-engineer
**Reviewing**: plugin-engineer's review of spec 023
**Date**: 2026-04-01

---

### Dangerous Contradictions

- **Error handling unification vs. backward compatibility**
  - **plugin-engineer claims**: The asymmetric error handling between `solve_with_ampl` (returns `None`) and `solve_ampl` (raises exceptions) is the highest-priority issue (P1). Proposes a `SolveResult` protocol or having `solve_with_ampl` raise `SolverInfeasibleError`.
  - **solver-engineer claims**: `solve_with_ampl` returning `None` for infeasibility is the correct MIP convention -- solvers return "infeasible" as a status, not an exception. Raising `SolverInfeasibleError` for infeasibility conflates a normal solver outcome with an error condition. Infeasibility is not an error; it is a valid answer to "is this problem feasible?"
  - **Why this is dangerous**: If `solve_with_ampl` raises on infeasibility, the caller (`_solve_with_ampl_fallback`) must catch it separately from solver crashes. The current `except Exception` block would catch both, losing the distinction. If infeasibility is an exception, the fallback path in `ampl_solver.py` L153-171 (which delegates to grid search for the detailed report) would need to be restructured to catch `SolverInfeasibleError` before the general `Exception` catch.
  - **Suggested resolution**: I agree with plugin-engineer that the three `None` cases in `solve_with_ampl` should be distinguishable, but the mechanism should be a richer return type (my Rec 5: `SolveOutcome` dataclass), not exceptions for non-error conditions. Infeasibility returns `SolveOutcome(config=None, status="infeasible")`. Missing amplpy returns `SolveOutcome(config=None, status="no_amplpy")`. This preserves the non-exception semantics for normal solver outcomes while giving the caller the information plugin-engineer correctly identifies as missing.

### Tensions

- **Solver config key implementation priority**
  - plugin-engineer rates the unimplemented `solver` config key as P2, arguing it is "dead documentation." solver-engineer did not flag this issue. On reflection, plugin-engineer is correct that the docstring in `optimizer.py` L38-39 promises a feature that does not exist. However, this is a plugin config concern, not a solver formulation concern. The P2 rating is appropriate -- it is a usability issue, not a correctness issue. I accept this finding.

- **`.dat` file support**
  - plugin-engineer recommends `.dat` file support for the general-purpose API. This is a reasonable extension but was not in the spec (FR-009 specifies `.mod` files only). Implementing it would expand the API surface beyond what spec 023 requires. I consider this a future enhancement, not a spec 023 gap. Impact is correctly rated as medium.

- **File detection heuristic**
  - plugin-engineer identifies the `.mod` suffix check as fragile. I agree -- the heuristic fails for `.ampl` and `.run` files. The `str | Path` approach plugin-engineer proposes is cleaner. This is a real API design issue that should be addressed.

### Safe Agreements

- **AMPL resource cleanup is properly implemented**: Both reviews agree that the `try/finally` pattern with `ampl.close()` is correct. plugin-engineer explicitly notes this as an alignment point; solver-engineer's review implicitly validates it through the formulation analysis.

- **Plugin interface is backward compatible**: Both reviews confirm that `PluginResult.data` is a non-breaking extension. The new `solver` field is additive; `solve_time_ms` and `gap` are conditional.

- **Naming inconsistency is real but low priority**: plugin-engineer flags `cost_per_agent_launch` vs `cost_per_launch` and `solver_timeout` vs `timeout`. These are genuine inconsistencies. solver-engineer did not flag them because they are naming concerns, not formulation concerns. I accept plugin-engineer's P3 rating.

- **NLP/MINLP documentation gap**: plugin-engineer correctly identifies that HiGHS does not support NLP/MINLP. solver-engineer's review focused on the MIP formulation and did not evaluate general-purpose API completeness. plugin-engineer's finding is valid.
