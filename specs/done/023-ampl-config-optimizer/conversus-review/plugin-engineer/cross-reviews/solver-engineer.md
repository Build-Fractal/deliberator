# Cross-Review of solver-engineer's Review

**Cross-reviewer**: plugin-engineer
**Reviewing**: solver-engineer's review of spec 023
**Date**: 2026-04-01

---

### Dangerous Contradictions

- **"MIP adds no algorithmic value" vs. extensibility investment**
  - **solver-engineer claims**: The MIP formulation "adds no algorithmic value over grid search" (Missed Opportunities, first bullet, rated **high** impact) because it enumerates all grid points and uses binary selection. solver-engineer recommends documenting this as equivalent to grid search (Rec 1, P1).
  - **plugin-engineer claims**: The AMPL integration is a platform investment, not a performance optimization. The value is: (a) the general-purpose `solve_ampl()` API for future optimization problems, (b) a proven-correct formulation that can be extended to larger search spaces without changing the dispatch layer, (c) solver-agnostic infrastructure (swap HiGHS for Gurobi/CPLEX by changing a config key).
  - **Why this is dangerous**: solver-engineer's P1 recommendation to "document as equivalent to grid search" could be read as "AMPL provides no value and should be removed." If this framing reaches stakeholders, the general-purpose API (FR-007) and the extensibility story lose their justification. The documentation should acknowledge the equivalence for the *current* search space while explaining the architectural value for *future* extensions.
  - **Suggested resolution**: Adopt solver-engineer's Rec 1 with modified framing: "For the current 135-point search space, the MIP and grid search produce identical results. The MIP formulation provides: (1) a verified-correct optimization model that serves as the reference implementation, (2) a framework for extending to larger or continuous search spaces, and (3) the infrastructure for the general-purpose solve_ampl() API." This acknowledges solver-engineer's valid technical observation without undermining the architectural value.

- **Shared formulas module vs. test-verified duplication**
  - **solver-engineer claims**: The duplicated quality/cost functions in `ampl_model.py` and `search.py` should be extracted to a shared `formulas.py` module (Rec 2, P2).
  - **plugin-engineer claims**: The duplication is intentional isolation. `search.py` uses `engine.cost.estimate_cost` (the canonical D007 implementation), while `ampl_model.py` reimplements the formula for AMPL data generation. A shared module would create a coupling between the grid search path and the AMPL path. If `engine.cost.estimate_cost` changes, the AMPL path should independently validate whether the change applies to its data generation. The test suite (`TestQualityModelConsistency`) exists precisely to catch divergence.
  - **Why this is dangerous**: Extracting a shared module removes the independent verification layer. Currently, a change to `search.py`'s quality model that does not propagate to `ampl_model.py` will be caught by the cross-solver consistency tests. With a shared module, both paths use the same code, and the consistency tests become tautological.
  - **Suggested resolution**: Keep the current duplication with the consistency tests. If the functions must be unified, the test suite should be restructured to test the formula against a hardcoded expected-value table, not against itself. This preserves the verification property.

### Tensions

- **Richer return type for `solve_with_ampl` -- convergence on approach**
  - solver-engineer's Rec 5 proposes a `SolveOutcome` dataclass with `status: Literal["optimal", "infeasible", "no_amplpy", "no_selection"]`. plugin-engineer's Rec 1 proposes a `SolveResult` protocol or raising exceptions. Both reviewers agree the current `None`-overloaded return type is problematic. The specific mechanism differs -- solver-engineer prefers a dataclass (consistent with MIP conventions where infeasibility is a status, not an error); plugin-engineer's initial proposal included exceptions but also mentioned a result type with a `status` field.
  - On reflection, solver-engineer's approach is more appropriate for a solver function. Infeasibility is a valid solver outcome, not an error. I modify my Rec 1 to align with solver-engineer's `SolveOutcome` approach rather than exceptions. The unified pattern: both `solve_with_ampl` and `solve_ampl` return structured result types; the general-purpose API's dict already has `solve_result` as a status field.

- **`.mod` file recommendation**
  - Both reviews converge on storing the AMPL model as a `.mod` file. solver-engineer rates it P2 (Rec 4); plugin-engineer did not flag this but accepts it as valid. The spec Section 6 constraint is explicit. No tension -- agreement.

- **Hardcoded gap**
  - solver-engineer rates this P2 (Rec 3). plugin-engineer did not flag it directly. On review, solver-engineer is correct: a hardcoded `gap: 0.0` defeats the purpose of FR-012's gap reporting. I accept this finding.

### Safe Agreements

- **HAS_AMPL pattern is sound**: Both reviews validate the module-level `try/except ImportError` pattern for optional dependencies.

- **Fallback logic is robust**: Both reviews agree the `_solve_with_ampl_fallback` exception handling (broad `except Exception` with grid search fallback) is correct for production reliability.

- **Test suite design is appropriate**: Both reviews accept the mock-based testing approach given AMPL's optional nature. solver-engineer's implicit acceptance aligns with plugin-engineer's explicit acknowledgement.

- **Quality/cost consistency tests are valuable**: solver-engineer explicitly praises these; plugin-engineer's review recognizes them as part of the dispatch verification story. The `TestQualityModelConsistency` class provides the highest confidence that SC-001 holds.
