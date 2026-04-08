# Solver-Engineer Revision: Spec 023 -- AMPL Config Optimizer

**Reviewer**: solver-engineer
**Revision iteration**: 1
**Date**: 2026-04-01

---

## Recommendation Dispositions

### Recommendation 1: Document enumeration-based MIP (was P1)

**Disposition: MAINTAINED with modified framing, DOWNGRADED to P2**

spec-compliance's cross-review correctly argues that P1 is too high for a documentation issue. The code is correct; the docstring is misleading but does not cause bugs. plugin-engineer's cross-review adds important context: the AMPL formulation is a platform investment (general-purpose API, solver-agnostic infrastructure, extensibility to larger search spaces), not just a performance play.

I accept both challenges. The documentation should be corrected, but the framing should acknowledge the architectural value. My original recommendation focused too narrowly on the "no algorithmic advantage" observation and did not credit the extensibility investment.

**Revised recommendation**: Update docstrings and spec Section 2 to accurately describe the formulation as "exact enumeration via binary selection MIP" and document both the current equivalence with grid search and the extensibility value (larger search spaces, solver portability, general-purpose API). Priority: P2.

---

### Recommendation 2: Extract quality/cost formulas into shared module (was P2)

**Disposition: WITHDRAWN**

plugin-engineer's cross-review delivers a decisive counterargument: the independent duplication enables the cross-solver consistency tests (`TestQualityModelConsistency`), which are the strongest evidence for SC-001. If the formulas are shared, the tests become tautological -- they verify that a function equals itself. spec-compliance's cross-review reinforces this from a compliance perspective: SC-001 evidence is stronger with independent implementations.

I concede this point. The duplication is intentional isolation, not accidental copy-paste. The test suite (`TestQualityModelConsistency`) serves as the synchronization mechanism. If the formulas diverge, the tests fail. This is a valid engineering pattern: dual implementation with cross-verification.

**Revised recommendation**: Withdraw. Keep the independent implementations in `ampl_model.py` and `search.py` with the cross-solver consistency tests as the synchronization mechanism. Add a code comment in both files: "This function intentionally duplicates the formula from [other file] to enable independent cross-verification. See TestQualityModelConsistency."

---

### Recommendation 3: Extract actual MIP gap from HiGHS (was P2)

**Disposition: MAINTAINED**

All three reviews converge on this issue. spec-compliance notes it as a caveat under FR-012. plugin-engineer did not flag it independently but accepted the finding in their cross-review. No cross-reviewer challenged the recommendation.

The hardcoded `gap: 0.0` is technically a compliance gap: FR-012 says "the result MUST include gap (optimality gap for MIP)." A hardcoded value is not the optimality gap; it is a placeholder. The actual gap should be extracted from the AMPL solve result.

**Revised recommendation**: Unchanged. Query AMPL for the actual gap after `ampl.solve()`. If the solver reports "solved" with proven optimality, gap is 0.0. If "feasible" (timeout), extract the actual gap. Priority: P2.

---

### Recommendation 4: Store config model as `.mod` file (was P2)

**Disposition: MAINTAINED**

Three-way convergence. solver-engineer Rec 4, spec-compliance Rec 2, and plugin-engineer's acceptance in cross-review all point to the same Section 6 constraint. No cross-reviewer challenged this.

**Revised recommendation**: Unchanged. Create `conversus/plugins/optimizer/config_optimizer.mod`. Priority: P2.

---

### Recommendation 5: Richer return type from `solve_with_ampl` (was P3)

**Disposition: MAINTAINED with broader scope**

plugin-engineer's Rec 1 converges on the same problem (asymmetric error handling) but initially proposed exceptions. In their cross-review of my review, plugin-engineer revised to align with my `SolveOutcome` dataclass approach -- acknowledging that infeasibility is a valid solver outcome, not an error. spec-compliance notes this is an internal API concern outside strict spec scope but accepts its value for code quality.

The convergence between solver-engineer and plugin-engineer on the approach (structured return type, not exceptions) strengthens the recommendation. I broaden the scope to include plugin-engineer's concern: `solve_ampl` should also return a structured result rather than a raw dict, for consistency across the module.

**Revised recommendation**: Define a `SolveOutcome` dataclass for `solve_with_ampl` with `config: OptimalConfig | None`, `status: Literal["optimal", "infeasible", "no_amplpy", "no_selection"]`, `solve_time_ms: float | None`. For the general-purpose API, the existing dict return is acceptable (it already has `solve_result` as a status field). Priority: P3.

---

### Recommendation 6: Revise SC-002 (was P3)

**Disposition: MAINTAINED**

spec-compliance rates SC-002 as "WEAK" (convergent finding). No cross-reviewer defended SC-002's current wording. The enumeration-based MIP cannot satisfy "finds infeasibility faster" for a 135-point problem where grid search runs in microseconds.

**Revised recommendation**: Unchanged. Revise SC-002 to acknowledge the equivalence and frame the MIP's value in terms of extensibility to larger search spaces. Priority: P3.

---

## New Recommendations

### New Recommendation A: Check for both amplpy and highspy in HAS_AMPL guard (Priority: P2)

plugin-engineer's cross-review of spec-compliance identifies a genuine gap: the `HAS_AMPL` flag only checks for `amplpy`, not `highspy`. If a user installs `amplpy` without `highspy`, the AMPL path activates but the solver fails at solve time. The broad exception handler catches this, but the diagnostic is misleading ("AMPL solver failed" when the real problem is missing `highspy`).

The fix is simple: `try: from amplpy import AMPL; import highspy; HAS_AMPL = True`. This aligns with FR-001's wording ("amplpy AND highspy are importable").

**Recommendation**: Check for both `amplpy` and `highspy` in the `HAS_AMPL` import guard. Priority: P2.

---

## Position Summary

**Withdrawn** (1):
- Shared formulas module (Rec 2) -- plugin-engineer and spec-compliance both demonstrated that independent duplication with cross-verification tests provides stronger SC-001 evidence than a shared module.

**Modified** (2):
- Enumeration documentation (Rec 1) -- downgraded to P2 per spec-compliance's argument. Framing modified per plugin-engineer's architectural value argument.
- Richer return type (Rec 5) -- broadened scope based on plugin-engineer convergence.

**Maintained** (3):
- MIP gap extraction (Rec 3) -- three-way convergence.
- `.mod` file (Rec 4) -- three-way convergence.
- SC-002 revision (Rec 6) -- convergence with spec-compliance.

**New** (1):
- Both-dependency import check (New Rec A) -- adopted from plugin-engineer's cross-review.

---

### Referenced Documentation

- Cross-reviews received: plugin-engineer and spec-compliance cross-reviews of solver-engineer
- Cross-reviews written: solver-engineer cross-reviews of plugin-engineer and spec-compliance
- `conversus/plugins/optimizer/ampl_model.py` -- L29-34 (HAS_AMPL), L65-102 (model string), L109-145 (formula duplication)
- `conversus/plugins/optimizer/ampl_solver.py` -- L149 (hardcoded gap)
- `tests/test_ampl.py` -- L740-763 (TestQualityModelConsistency)
