# Cross-Review: spec-compliance reviewing schema-engineer

**Spec**: 026-optimization-template-library

---

## Agreement

The schema-engineer's review is thorough on structural validation. I agree with:

- Template schema compliance assessment
- gap_question completeness verification
- Constraint reference validation
- Template and constraint count verification

## Disagreements

### game_form cross-validation (schema-engineer's concern #2) -- I agree it should be Low

The schema-engineer correctly identifies that game_form values in templates are not validated against game form YAML schemas. I agree with the optimization-engineer's cross-review that this should be Low (not Info). A template referencing a non-existent game form would be silently invalid. Adding a test that cross-references template game_form values against game-forms/*.yml would be a valuable addition.

## Additions

The schema-engineer did not assess the `mode_compatibility` field values for semantic correctness. While the test verifies the list is non-empty, it does not check that the modes listed are valid mode names from the mode-mapping. For example, a template could declare `mode_compatibility: ["nonexistent-mode"]` and pass all current tests.

This is another cross-reference validation gap, similar to the game_form concern. A test that validates mode_compatibility values against mode-mapping.yml entries would strengthen the schema consistency guarantees.
