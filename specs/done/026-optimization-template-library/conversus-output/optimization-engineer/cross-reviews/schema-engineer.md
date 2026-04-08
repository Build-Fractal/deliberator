# Cross-Review: optimization-engineer reviewing schema-engineer

**Spec**: 026-optimization-template-library

---

## Agreement

The schema-engineer's assessment is thorough and accurate. I agree with:

- All 15 templates follow the YAML schema correctly
- gap_question completeness is verified by parametric tests
- Constraint references are all valid
- The template and constraint counts meet thresholds

## Disagreements

None. The schema-engineer's review is focused on structural correctness, which complements my mathematical correctness review well.

## Additions

### 1. game_form validation gap (supporting schema-engineer's concern #2)

The schema-engineer notes that game_form values in templates are not validated against existing game form YAML schemas. I can confirm this matters:

- `assignment-optimal` uses `gnep` -- exists
- `portfolio-markowitz` uses `parametric` -- exists
- `knapsack-binary` uses `parametric` -- exists
- `network-min-cost` uses `parametric` -- exists
- `set-cover` uses `parametric` -- exists

All game_form references are valid, but this is not enforced by any test. A future template could reference a non-existent game form without detection. I would upgrade this from Info to Low severity.

### 2. Constraint count fragility

The schema-engineer notes the constraint count is exactly 10. I agree this is fragile. The existing constraints (6) + new constraints (4) = 10. If any constraint file were accidentally deleted or renamed, the count test would fail. Adding 1-2 buffer constraints (e.g., `symmetry`, `precedence-dag`) would make the count more robust. However, this is a test robustness issue, not a spec compliance failure.
