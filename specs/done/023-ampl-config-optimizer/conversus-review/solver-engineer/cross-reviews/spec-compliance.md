# Cross-Review of spec-compliance's Review

**Cross-reviewer**: solver-engineer
**Reviewing**: spec-compliance's review of spec 023
**Date**: 2026-04-01

---

### Dangerous Contradictions

- **FR-004: "PARTIAL PASS" assessment may be too lenient**
  - **spec-compliance claims**: FR-004 is a "PARTIAL PASS" because the tolerance criterion (5%) is trivially satisfied by exact enumeration.
  - **solver-engineer claims**: FR-004 describes a specific implementation technique ("piecewise linear approximation") that was not implemented. The requirement is not just about tolerance -- it specifies an approach that enables LP relaxation and continuous variable support. Trivially satisfying the tolerance while ignoring the technique is more accurately a "PASS on tolerance, FAIL on approach." The distinction matters because the PWL approach would have given the MIP solver the ability to prune via LP relaxation (my Rec 1: the MIP adds no algorithmic value).
  - **Why this is dangerous**: Rating FR-004 as PARTIAL PASS suggests the gap is minor. In reality, the gap is architectural -- the entire rationale for choosing AMPL over grid search (LP relaxation, branch-and-bound pruning) depends on the quality model being a continuous approximation, not a discrete lookup. The enumeration approach eliminates the solver's ability to reason about the problem structure.
  - **Suggested resolution**: Rate FR-004 as "PASS on correctness, FAIL on approach" and tie it to my Rec 1 (document the formulation as enumeration-based). Alternatively, if the project considers the approach aspect non-binding (only the tolerance matters), rate it PASS with a note.

### Tensions

- **SC-002 assessment convergence**
  - spec-compliance rates SC-002 as "WEAK." solver-engineer's review identifies SC-002 as an "off-base assumption" and recommends revising it (Rec 6). Both reviews agree the success criterion is not achievable with the current formulation. spec-compliance's "WEAK" is more diplomatic; solver-engineer's "off-base" is more direct. The substantive finding is identical: enumeration-based MIP cannot outperform O(n) grid search for n=135.
  - I accept spec-compliance's WEAK rating as accurate and appropriate for a compliance review. My "off-base" framing is appropriate for a solver-focused review. No contradiction -- both point to the same spec revision.

- **Gap hardcode assessment**
  - spec-compliance notes the hardcoded gap as a "caveat" under FR-012 but rates FR-012 as PASS. solver-engineer rates this as a P2 recommendation (Rec 3). spec-compliance's compliance perspective (the field exists, requirement met) and solver-engineer's correctness perspective (the value is wrong, diagnostic purpose defeated) are both valid. The question is whether FR-012 requires the gap to be *accurate* or merely *present*. FR-012 says "the result MUST include solve_time_ms and gap (optimality gap for MIP)" -- the parenthetical "optimality gap for MIP" implies the value should reflect the actual gap, not a hardcoded zero.
  - I maintain that this is a compliance gap, not just a caveat. The field's value contradicts its documented semantics.

- **Integration test recommendation**
  - spec-compliance recommends `@pytest.mark.skipunless(HAS_AMPL)` integration tests (Rec 5). solver-engineer did not make this recommendation. On reflection, spec-compliance is correct: the test suite's exclusive reliance on mocks means the AMPL model string has never been parsed by a real AMPL instance in CI. A syntax error in `CONVERSUS_CONFIG_MODEL` would not be caught. This is a valid testing gap.

### Safe Agreements

- **FR-001, FR-002, FR-003, FR-005, FR-006, FR-007, FR-010, FR-011 are fully compliant**: Both reviews agree on these. The dispatch logic, fallback, cost formula, infeasibility handling, timeout, general-purpose API, licence freedom, and solver field are all correctly implemented.

- **SC-001 is strong**: Both reviews agree that the enumeration approach guarantees SC-001 by construction. The quality/cost consistency tests provide additional confidence.

- **SC-004 is fully satisfied**: Both reviews agree that the grid search path is unchanged when AMPL is unavailable.

- **Config model should be a `.mod` file**: spec-compliance flags the Section 6 violation (FR-009 partial). solver-engineer's Rec 4 makes the same point. Both reviews converge on creating a `.mod` file for the config optimization model.

- **Compliance summary table is well-structured**: spec-compliance's table provides a clear at-a-glance assessment. The ratings are defensible. The asterisks on FR-008 and FR-012 appropriately flag the documentation/accuracy concerns.
