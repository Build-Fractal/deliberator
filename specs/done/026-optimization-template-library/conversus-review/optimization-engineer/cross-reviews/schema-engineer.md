# Cross-Review: optimization-engineer reviewing schema-engineer

**Spec**: 026-optimization-template-library

---

## Dangerous Contradictions

None. The schema-engineer's findings are consistent with and complementary to the optimization-engineer's mathematical review. No factual claims conflict.

---

## Tensions

### T1: game_form cross-validation severity (Info vs. Low)

- **schema-engineer's position**: Rates game_form cross-validation gap as Low (SE-2). A template with `game_form: nonexistent` would pass all tests.
- **optimization-engineer's position**: I independently flagged the same gap as Low (OE-3). No tension on substance -- both agents agree this is a real gap and both rate it Low. The convergence is notable: we arrived at the same severity independently.
- **Nature**: Reinforcement, not tension. Included here for completeness.

### T2: Constraint count fragility framing

- **schema-engineer's position**: Flags constraint count at exact threshold (10/10) as Info (SE-1). Frames it as a test robustness concern.
- **optimization-engineer's position**: I did not flag this in my Phase 1 review. On reflection, the schema-engineer is correct that exact-threshold tests are fragile. However, I note that the threshold (>= 10) is a success criterion from the spec, not a schema-engineer invention. The test correctly implements SC-002. The fragility is in the spec's threshold, not the test's implementation.
- **Nature**: Minor framing difference. The schema-engineer implies the test threshold could be adjusted; I argue the test faithfully implements the spec's SC-002 as written.

---

## Safe Agreements

1. **All 15 templates follow the YAML schema correctly**: Both agents verify this through different lenses (mathematical correctness vs. structural compliance). Unanimous.

2. **gap_question completeness is verified**: The schema-engineer's parameter-by-parameter audit confirms what the test enforces programmatically. The gap_questions are not only present but semantically meaningful (they ask questions a construction pipeline would actually need answered).

3. **Constraint references are all valid**: The schema-engineer's reference map matches my mathematical assessment of which constraints each template should reference. The templates reference the constraints their formulations actually need -- this is not just structural validity but semantic correctness.

4. **New constraint templates are well-formed**: Both agents agree the 4 new constraints (integrality, cardinality, precedence, flow-conservation) are valid. I can confirm from a mathematical perspective that `form` expressions are correct: integrality (`x_i in {0, 1} or x_i in Z+`), flow-conservation (`sum(f_ji) - sum(f_ik) = b_i for all nodes i`), etc.

5. **mode_compatibility coverage patterns are reasonable**: The schema-engineer observes that some templates have 2 modes while others have 4. From a mathematical perspective, this makes sense: assignment-optimal with `gnep` game form is most natural in cooperative/winner-take-all contexts, while portfolio-markowitz with `parametric` game form applies broadly across all modes.

---

## Additions from optimization-engineer perspective

### A1: Template-to-constraint semantic alignment

The schema-engineer verifies that constraint references resolve to files. I can add that the constraints referenced are also *mathematically correct* for each formulation:

- knapsack-binary references `budget` (weight capacity), `integrality` (binary variables), `non-negativity` (no negative items) -- all three are *required* for a correct 0-1 knapsack formulation.
- network-min-cost references `flow-conservation` (mass balance), `capacity` (arc limits), `non-negativity` (no negative flow) -- these are the *complete* set of constraints for MCNF.
- set-cover references `minimum-coverage` (all elements covered), `integrality` (binary selection), `non-negativity` -- correct and complete.

No template is missing a mathematically required constraint, and no template includes a constraint that is irrelevant to its problem class.

### A2: Example quality beyond structure

The schema-engineer verifies examples have >= 1 key. I can add that the example values are not just structurally valid but produce *meaningful* problem instances:
- The knapsack example is the classic textbook instance with a known optimal solution.
- The network flow example is a minimal but complete graph with balanced supply/demand.
- The portfolio example has a realistic covariance matrix (PSD, reasonable return/risk values).

This matters because the examples serve as documentation and as test fixtures for downstream assembly.
