# Plugin-Engineer Final Disputes: Spec 023 -- AMPL Config Optimizer

**Reviewer**: plugin-engineer
**Phase**: 4 (Final Disputes and Convergence)
**Date**: 2026-04-01

---

## Remaining Disputes

### Dispute 1: Priority of file detection fix (Rec 3) -- P2 or P3?

**Parties**: plugin-engineer vs. spec-compliance

plugin-engineer maintains this as P2. spec-compliance argues the false-positive risk is outside strict FR-009 scope because the spec only requires `.mod` file support. The dispute is narrow: both agree the false-positive risk exists; they disagree on priority.

My argument for P2: `solve_ampl()` is a public API exported in `__init__.py`. A user who passes a model string that happens to end with ".mod" on a single line gets incorrect behavior -- the function tries to read a non-existent file instead of parsing the model. This is a correctness bug in a public API, not an edge case. Public API bugs warrant P2.

spec-compliance's argument for P3: FR-009 only requires `.mod` file support, so the fix is a quality improvement beyond spec scope.

**Status**: Active dispute. I maintain P2. If the synthesizer agrees with spec-compliance that this is outside spec scope, I will accept P3 with the caveat that the public API has a known correctness issue.

---

### Dispute 2: Enumeration documentation framing -- "no algorithmic value" is misleading

**Parties**: plugin-engineer vs. solver-engineer

solver-engineer's revised Rec 1 (P2) still describes the MIP as having "current equivalence with grid search." While technically correct, this framing undervalues the AMPL integration. The MIP formulation provides:

1. **Formal verification**: The AMPL model is a mathematical specification that can be independently verified, audited, or extended by optimization engineers. The grid search is an imperative loop.
2. **Solver portability**: Changing from HiGHS to Gurobi is a one-line config change. Changing the grid search to use a different algorithm requires rewriting the loop.
3. **General-purpose API foundation**: The `solve_ampl()` API would not exist without the AMPL infrastructure.

solver-engineer's revision accepts the "extensibility investment" framing, which is progress. My dispute is that the documentation should lead with the positive value (formal specification, solver portability, general-purpose API) rather than leading with the limitation ("equivalent to grid search"). The limitation should be noted, but it should not be the headline.

**Status**: Minor dispute. I accept solver-engineer's factual claim (enumeration equivalence) but dispute the documentation emphasis. The synthesizer should determine the appropriate framing balance.

---

## Convergence

### Full convergence (all three reviewers agree)

1. **`.mod` file for config model**: Three-way convergence. Section 6 requires it. Priority: P2.

2. **Real MIP gap extraction**: Three-way convergence. FR-012 requires actual gap, not placeholder. Priority: P2.

3. **Both-dependency HAS_AMPL check**: Three-way convergence. FR-001 requires both amplpy and highspy. Priority: P2.

4. **Dead docstring removal**: plugin-engineer (revised Rec 2) and spec-compliance (New Rec B) converge. solver-engineer did not address but has no objection. Priority: P3.

5. **Cross-verification tests are load-bearing**: Three-way convergence (solver-engineer's withdrawal of Rec 2 is contingent on these tests being maintained).

6. **Integration tests**: spec-compliance and plugin-engineer converge. solver-engineer accepted. Priority: P3.

7. **FR-004 spec alignment**: solver-engineer and spec-compliance converge. plugin-engineer defers (formulation concern). Priority: P1-P2.

8. **SC-002 revision**: solver-engineer and spec-compliance converge. plugin-engineer defers. Priority: P2-P3.

### Convergence between two reviewers

1. **`SolveOutcome` return type**: solver-engineer and plugin-engineer converge on structured return with discriminated status. spec-compliance accepts but considers outside spec scope. Priority: P2-P3.

2. **Robust file detection**: plugin-engineer maintained (P2). solver-engineer accepted in cross-review. spec-compliance considers it outside FR-009 scope. Priority: disputed (P2 vs P3).

---

## Final Position Statement

### Non-Negotiables

1. **Public API correctness matters.** `solve_ampl()` is exported in `__init__.py` and documented as a general-purpose function. Known false-positive behavior in its file detection heuristic is a public API bug. It should be fixed.

2. **Dead documentation is harmful.** The `solver` config key in `ConfigOptimizer`'s docstring promises a feature the code does not deliver. This creates false expectations and debugging frustration. It should be removed until the feature is specced and implemented.

3. **Error handling in public APIs must be consistent.** `solve_with_ampl` and `solve_ampl` are sibling functions in the same module with incompatible error conventions. The `SolveOutcome` approach resolves this without exceptions for non-error conditions.

### Flexibility

1. **File detection priority.** I maintain P2 but will accept P3 if the synthesizer agrees with spec-compliance's scope argument.

2. **Documentation framing.** I want the AMPL value story to lead with positive architectural value, not with "equivalent to grid search." But this is a framing preference, not a technical disagreement. I will accept solver-engineer's framing if the synthesizer prefers it.

3. **NLP/MINLP documentation.** P3 editorial improvement. Will accept deferral.

4. **Naming standardization.** P3 cosmetic fix. Will accept deferral.

5. **AMPL Community Edition limits.** P3 documentation improvement. Will accept deferral.

---

### Referenced Documentation

- `conversus/plugins/optimizer/ampl_model.py` -- L354 (file detection), L315-404 (solve_ampl)
- `conversus/plugins/optimizer/optimizer.py` -- L38-39 (dead solver docstring)
- `conversus/plugins/optimizer/__init__.py` -- L19-22 (exports)
- Revised positions: solver-engineer/revision.md, plugin-engineer/revision.md, spec-compliance/revision.md
