# Cross-Review: spec-compliance reviewing optimization-engineer

**Spec**: 026-optimization-template-library

---

## Dangerous Contradictions

None. The optimization-engineer's mathematical review complements rather than conflicts with the compliance assessment.

---

## Tensions

### T1: Concern severity calibration -- OE-1 and OE-2 should be Info, not Low

- **optimization-engineer's position**: Rates PSD validation (OE-1) and supply_demand sum-to-zero (OE-2) as Info. (Note: the optimization-engineer already rates these as Info, which is correct.)
- **spec-compliance's position**: I confirm Info is the correct severity. Template schemas are declarative specifications, not solver input validators. PSD checking requires eigenvalue decomposition; sum-to-zero requires arithmetic on parsed values. Both are firmly in the solver/assembler layer. The template descriptions correctly *document* these requirements ("Must be symmetric positive semi-definite," "Must sum to zero for feasibility"), which is the appropriate level of enforcement for a YAML schema.
- **Nature**: Agreement. Included for explicitness.

### T2: OE-3 and OE-4 (cross-validation gaps) -- severity agreement

- **optimization-engineer's position**: Rates game_form cross-validation (OE-3) and mode_compatibility cross-validation (OE-4) as Low.
- **spec-compliance's position**: I agree with Low. These are test coverage gaps with a clear fix (two parametric tests). The current values are all valid today, but the invariant is unenforced. A future contributor adding a template could introduce a typo in game_form or mode_compatibility without any test failure. Low is appropriate because the fix is straightforward and the current risk is low (all values are correct).
- **Nature**: Full agreement.

---

## Safe Agreements

1. **All 15 formulations are mathematically correct**: I defer to the optimization-engineer's domain expertise on mathematical soundness. The formulations use standard problem classifications (LP, MIP, QP) with well-known solver support.

2. **Parameters are reasonable with appropriate ranges**: The optimization-engineer's assessment of parameter ranges (e.g., risk_aversion [0, 100], n_agents >= 1) is consistent with the schema's type declarations and range constraints.

3. **Examples produce feasible problem instances**: The optimization-engineer verified feasibility through mathematical analysis. This provides confidence for SC-004 (example validity) and SC-005 (solver solvability) even though SC-005 lacks formal solver testing.

4. **String-encoded matrices are a practical choice**: The optimization-engineer correctly identifies this as an architectural decision that requires parsing downstream. The encoding is consistent and well-documented in parameter descriptions.

---

## Additions from spec-compliance perspective

### A1: Mathematical correctness supports but does not replace testing

The optimization-engineer's "PASS with minor observations" verdict is well-supported. However, from a compliance perspective, mathematical correctness is a necessary but not sufficient condition for spec compliance. The spec requires:

- Schema validation (FR-001, FR-003) -- verified by tests, not by mathematical review
- gap_question presence (FR-002) -- verified by tests
- Constraint reference validity (FR-005) -- verified by tests
- Example presence (FR-006) -- verified by tests and by mathematical review

The optimization-engineer's review provides the *semantic* layer that tests cannot: confirming that the formulations correctly represent their problem classes, that parameters have meaningful mathematical interpretations, and that examples are not just non-empty but actually feasible. This two-layer verification (structural via tests + semantic via expert review) is the gold standard.

### A2: form field is not validated for mathematical correctness

The optimization-engineer assesses form field expressions and finds them all valid. I note that no test validates the `form` field beyond "it is a string." A template with `form: "J = ???"` would pass all tests. The Pydantic model accepts any string for `form`. This is probably correct (mathematical expression parsing is complex), but it means the form field's correctness depends entirely on expert review, not automated testing. The optimization-engineer's review fills this gap for the current template set.

### A3: Mutual consistency across templates

The optimization-engineer notes that no two templates produce conflicting constraint sets for the same problem type. This is an important observation for the construction pipeline: if a user's problem could match multiple templates, the templates should not prescribe contradictory constraints. The clean separation of problem classes (assignment vs. knapsack vs. set cover vs. network flow) makes conflicts unlikely, but this invariant is worth monitoring as the library grows.
