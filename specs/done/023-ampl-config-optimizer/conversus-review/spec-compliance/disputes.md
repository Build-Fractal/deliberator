# Spec-Compliance Final Disputes: Spec 023 -- AMPL Config Optimizer

**Reviewer**: spec-compliance
**Phase**: 4 (Final Disputes and Convergence)
**Date**: 2026-04-01

---

## Remaining Disputes

### Dispute 1: FR-004 spec alignment priority -- P1 or P2?

**Parties**: spec-compliance (P1) vs. solver-engineer (P2)

spec-compliance maintains P1. solver-engineer downgraded to P2 in their revision, arguing the code is correct and only the documentation is wrong.

My argument for P1: spec-implementation alignment is the core concern of compliance review. When a functional requirement describes a specific technical approach ("piecewise linear approximation") and the implementation uses a different approach (exact enumeration), the spec is wrong or the implementation is wrong. Either way, this is the highest-priority compliance gap -- it undermines the spec as a trustworthy contract. The code being correct does not make the spec correct. A correct implementation with an incorrect spec is still a compliance failure.

solver-engineer's P2 argument (docstring inaccuracy does not cause bugs) conflates code correctness with spec correctness. From a compliance perspective, an inaccurate spec is a first-order concern regardless of code behavior.

**Status**: Active dispute. I maintain P1. The synthesizer should resolve the priority based on the project's relative weighting of spec integrity vs. code correctness.

---

### Dispute 2: File detection priority scope -- spec compliance vs. API quality

**Parties**: spec-compliance (P3 / outside scope) vs. plugin-engineer (P2)

FR-009 requires ".mod files" to be loadable. The implementation supports `.mod` files. The false-positive risk for model strings ending in ".mod" is a quality concern, not a compliance concern. From spec-compliance's perspective, this is outside FR-009 scope and rates P3 at most.

plugin-engineer argues it is a public API correctness bug warranting P2. This is a valid argument from a code quality perspective, but it is not a compliance argument. The spec does not define how the API should distinguish file paths from model strings -- that is an implementation decision.

**Status**: Active dispute. I maintain this is outside spec scope. I do not dispute the bug's existence, only its priority relative to spec-defined requirements.

---

## Convergence

### Full convergence (all three reviewers agree)

1. **`.mod` file for config model** (Section 6): Three-way convergence. The spec explicitly requires user-readable `.mod` storage. The implementation stores it as a Python string. This must be fixed. Priority: P2.

2. **Real MIP gap from solver** (FR-012): Three-way convergence. The hardcoded `gap: 0.0` satisfies FR-012's letter but misrepresents the solver's actual assessment. The gap should be extracted from AMPL output. Priority: P2.

3. **Both-dependency import check** (FR-001): Three-way convergence. The spec says "amplpy AND highspy." The code checks only amplpy. This is a compliance gap that all three reviewers identified. Priority: P2.

4. **SC-002 must be revised**: solver-engineer and spec-compliance converge with strong evidence. plugin-engineer does not dispute. The enumeration-based formulation cannot find infeasibility faster than O(n) grid search. Priority: P2.

5. **FR-004 must be aligned with implementation**: solver-engineer and spec-compliance converge. The spec describes PWL approximation; the implementation uses exact enumeration. Priority: P1 (spec-compliance) or P2 (solver-engineer) -- disputed.

6. **Dead `solver` config key must be removed from docstring**: plugin-engineer and spec-compliance converge. The docstring promises an unimplemented feature. Priority: P3.

7. **Cross-verification tests are essential**: Three-way convergence. The intentional duplication of quality/cost formulas is safe only because `TestQualityModelConsistency` exhaustively verifies equivalence. These tests must be maintained.

8. **`SolveOutcome` structured return type**: solver-engineer and plugin-engineer converge. spec-compliance accepts as a code quality improvement outside strict spec scope. Priority: P2-P3.

9. **Integration tests**: spec-compliance and plugin-engineer converge. solver-engineer accepted. Priority: P3.

---

## Final Position Statement

### Non-Negotiables

1. **Spec-implementation alignment is P1.** When a functional requirement describes a specific technical approach and the implementation uses a different approach, the gap is first-order. The spec is the contract; if it describes something other than what was built, either the spec or the implementation must change. For spec 023, the spec should be updated to reflect the implementation (exact enumeration is correct and defensible). But the update must happen.

2. **FR-012 gap accuracy.** The gap field must reflect the solver's actual optimality assessment. A hardcoded value defeats the diagnostic purpose defined by the requirement.

3. **FR-001 dependency check.** The spec says "amplpy AND highspy." The code must check both.

### Flexibility

1. **File detection priority.** I consider this outside spec scope (P3). If the synthesizer determines public API correctness warrants P2, I will accept.

2. **`SolveOutcome` return type.** This is outside spec scope but improves code quality. I have no objection to any priority the synthesizer assigns.

3. **SC-002 wording.** I proposed a specific revision. If the synthesizer prefers different wording that acknowledges the limitation, I will accept.

4. **Integration tests.** P3 is appropriate. The mock tests are sufficient for compliance verification; integration tests are a defense-in-depth improvement.

5. **Naming standardization, Community Edition docs, NLP/MINLP docs.** All P3 editorial improvements. Will accept deferral.

---

### Referenced Documentation

- `specs/done/023-ampl-config-optimizer/spec.md` -- FR-001, FR-004, FR-009, FR-012, SC-002, Section 6
- `conversus/plugins/optimizer/ampl_model.py` -- L29-34 (HAS_AMPL), L65-102 (model string)
- `conversus/plugins/optimizer/ampl_solver.py` -- L149 (hardcoded gap)
- Revised positions: solver-engineer/revision.md, plugin-engineer/revision.md, spec-compliance/revision.md
