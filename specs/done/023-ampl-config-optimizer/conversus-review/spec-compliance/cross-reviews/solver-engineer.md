# Cross-Review of solver-engineer's Review

**Cross-reviewer**: spec-compliance
**Reviewing**: solver-engineer's review of spec 023
**Date**: 2026-04-01

---

### Dangerous Contradictions

- **"MIP adds no algorithmic value" framing vs. spec intent**
  - **solver-engineer claims**: The MIP adds no algorithmic value and the docstring claim ("solves the mixed-integer program exactly rather than enumerating the entire grid") is inaccurate (Rec 1, P1 impact).
  - **spec-compliance claims**: solver-engineer's technical analysis is correct -- the enumeration-based binary selection is mathematically equivalent to iterating the grid. However, the P1 priority rating is too high for what is essentially a documentation/framing issue. The code is provably correct. The spec's FR-003 (exact cost encoding) and SC-001 (same optimal config) are both satisfied. The docstring inaccuracy does not create bugs or compliance failures.
  - **Why this is dangerous**: Elevating docstring inaccuracy to P1 conflates documentation debt with correctness risk. If implementation bandwidth is limited, a P1 label could divert effort from genuine compliance gaps (FR-004 alignment, Section 6 `.mod` file requirement, hardcoded gap value) to wordsmithing.
  - **Suggested resolution**: Downgrade solver-engineer's Rec 1 to P2. The documentation should be corrected, but the code and compliance profile are unaffected. The P1 slot should be reserved for the error handling unification (which affects API correctness) or the FR-004/spec alignment (which affects spec-implementation integrity).

### Tensions

- **Shared formulas module (Rec 2) vs. independent verification**
  - solver-engineer recommends extracting quality/cost formulas into `formulas.py` (Rec 2, P2). From a compliance perspective, this is neutral -- FR-003 requires the AMPL model to encode D007 exactly, regardless of where the code lives. However, the independent duplication enables the cross-solver consistency tests (`TestQualityModelConsistency`), which are the primary evidence for SC-001. If the formulas are shared, SC-001's test evidence becomes tautological. From a compliance standpoint, I prefer the current duplication-with-verification approach because it provides stronger SC-001 evidence.
  - This is a judgment call, not a compliance requirement. I flag it as a tension because solver-engineer's recommendation (single source of truth) and spec-compliance's interest (testable SC-001 evidence) pull in opposite directions.

- **Richer return type (Rec 5) and spec scope**
  - solver-engineer proposes a `SolveOutcome` dataclass (Rec 5, P3). The spec does not define the internal API between `ampl_model.py` and `ampl_solver.py` -- it only specifies the plugin output (FR-011, FR-012) and the general-purpose API (FR-007). Internal refactoring of `solve_with_ampl`'s return type is outside spec scope but may improve code quality. From a compliance perspective, this is a recommendation for code quality, not for spec compliance. P3 is appropriate.

### Safe Agreements

- **SC-002 is the weakest success criterion**: Both reviews identify SC-002 as problematic. solver-engineer rates it as an "off-base assumption" and recommends revision (Rec 6). spec-compliance rates it as "WEAK" in the compliance table. The technical analysis is identical: enumeration-based MIP cannot outperform O(n) grid search for the current problem size.

- **Section 6 `.mod` file requirement is violated**: solver-engineer's Rec 4 and spec-compliance's Rec 2 converge on creating a `.mod` file. Both identify the same Section 6 constraint and the same implementation gap.

- **Hardcoded gap defeats FR-012's purpose**: solver-engineer's Rec 3 and spec-compliance's FR-012 caveat converge. Both identify the hardcoded `gap: 0.0` as undermining the diagnostic value of the gap field.

- **FR-004 needs spec alignment**: solver-engineer's Off-Base Assumptions section and spec-compliance's FR-004 PARTIAL PASS both identify the mismatch between the spec's "piecewise linear approximation" and the implementation's exact enumeration. Both recommend aligning the spec text with the implementation.

- **Quality/cost consistency is the strongest evidence**: solver-engineer's Alignment section and spec-compliance's SC-001 analysis both identify the `TestQualityModelConsistency` tests as the primary evidence that the AMPL and grid search paths produce equivalent results. This is the most important test class in the suite.

- **HAS_AMPL pattern is correct**: Both reviews validate the optional import pattern. spec-compliance notes the amplpy-only check (vs. spec's "amplpy AND highspy") as acceptable; solver-engineer's review does not flag it. The existing broad exception handler in `_solve_with_ampl_fallback` provides a safety net for missing highspy.
