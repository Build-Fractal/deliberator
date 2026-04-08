# Solver-Engineer Final Disputes: Spec 023 -- AMPL Config Optimizer

**Reviewer**: solver-engineer
**Phase**: 4 (Final Disputes and Convergence)
**Date**: 2026-04-01

---

## Remaining Disputes

### Dispute 1: Shared formulas module -- withdrawn but with conditions

**Parties**: solver-engineer (original Rec 2) vs. plugin-engineer (cross-review) and spec-compliance (cross-review)

I withdrew Rec 2 (shared formulas module) in my revision, accepting that independent duplication with cross-verification tests provides stronger SC-001 evidence. However, I want to record the conditions under which this withdrawal holds:

The current approach is only safe because `TestQualityModelConsistency` exhaustively verifies equivalence at every grid point. If the test suite is ever weakened (e.g., reduced to spot-check sampling) or the quality model becomes more complex (e.g., additional dimensions beyond rounds/agents/iterations), the duplication risk increases. The cross-verification tests are load-bearing -- removing or weakening them re-opens the shared module question.

**Status**: Resolved. I accept the withdrawal. This is a conditional note, not an active dispute.

---

## Convergence

### Full convergence (all three reviewers agree)

1. **Store config model as `.mod` file**: All three reviewers converge. solver-engineer Rec 4, spec-compliance Rec 2, plugin-engineer acceptance. Section 6 of the spec explicitly requires this. Priority: P2.

2. **Extract real MIP gap from solver output**: All three reviewers converge. solver-engineer Rec 3, spec-compliance Rec 4, plugin-engineer acceptance. FR-012 requires `gap` to reflect the actual optimality gap. Priority: P2.

3. **Check for both amplpy and highspy in HAS_AMPL**: All three reviewers converge. FR-001 says "amplpy AND highspy." Implementation checks only amplpy. Priority: P2.

4. **Revise SC-002**: solver-engineer and spec-compliance converge. plugin-engineer did not address SC-002 but did not dispute the finding. The enumeration-based MIP cannot find infeasibility faster than grid search for 135 points. Priority: P2-P3.

5. **Align FR-004 with implementation**: solver-engineer and spec-compliance converge. The spec says "piecewise linear approximation"; the implementation uses exact enumeration. Priority: P1 (spec-compliance) to P2 (solver-engineer).

6. **Quality/cost duplication with cross-verification tests is the right approach**: solver-engineer withdrew the shared module recommendation. plugin-engineer and spec-compliance provided the arguments. The `TestQualityModelConsistency` tests are the synchronization mechanism for the intentional duplication.

7. **Remove dead `solver` config key from docstring**: plugin-engineer (revised Rec 2) and spec-compliance (New Rec B) converge. The docstring promises a feature the code does not implement. Priority: P3.

### Convergence between two reviewers

1. **`SolveOutcome` structured return type for `solve_with_ampl`**: solver-engineer (Rec 5) and plugin-engineer (revised Rec 1) converge on a dataclass with discriminated status rather than exceptions. spec-compliance considers this outside spec scope but does not dispute it. Priority: P2-P3.

2. **Integration tests with real AMPL solver**: spec-compliance (Rec 5) and plugin-engineer (New Rec B) converge. solver-engineer accepted in cross-review. Priority: P3.

3. **Robust file detection in `solve_ampl()`**: plugin-engineer (Rec 3) maintained. solver-engineer accepted in cross-review. spec-compliance notes it is outside strict FR-009 scope but acknowledges the false-positive risk. Priority: P2.

---

## Final Position Statement

### Non-Negotiables

1. **The enumeration-based MIP is mathematically equivalent to grid search for the current search space.** This is a mathematical fact, not an opinion. The documentation must not claim otherwise. The AMPL formulation has value as platform infrastructure and extensibility investment, but it does not outperform grid search for n=135.

2. **The MIP gap must be extracted from the solver, not hardcoded.** FR-012 requires "optimality gap for MIP." A hardcoded 0.0 is not an optimality gap -- it is a placeholder. If the solver times out with a feasible incumbent, the gap is non-zero, and reporting 0.0 is misleading.

3. **Cross-verification tests (`TestQualityModelConsistency`) are load-bearing.** The intentional duplication of quality/cost formulas is only safe because these tests exhaustively verify equivalence. Weakening or removing these tests would be a regression.

### Flexibility

1. **FR-004 priority.** spec-compliance rates the spec alignment as P1; solver-engineer rates it P2. I will defer to the synthesizer. The edit is the same either way -- only the priority differs.

2. **SC-002 wording.** I proposed replacing the speed claim with an extensibility framing. If the synthesizer prefers a different formulation that acknowledges the current limitation while preserving the aspirational direction, I will accept it.

3. **Shared formulas module.** I withdrew this, but if the quality model grows more complex in future specs, I would re-raise it. For now, the cross-verification tests are sufficient.

4. **`SolveOutcome` scope.** Whether this is a `dataclass` or a `TypedDict` or a `NamedTuple` is a minor design choice. The requirement is discriminated status, not a specific type.

---

### Referenced Documentation

- `conversus/plugins/optimizer/ampl_model.py` -- L109-145 (duplicated formulas), L65-102 (model string)
- `conversus/plugins/optimizer/ampl_solver.py` -- L149 (hardcoded gap)
- `tests/test_ampl.py` -- L740-763 (TestQualityModelConsistency)
- `specs/done/023-ampl-config-optimizer/spec.md` -- FR-004, FR-012, SC-002, Section 6
- Revised positions: solver-engineer/revision.md, plugin-engineer/revision.md, spec-compliance/revision.md
