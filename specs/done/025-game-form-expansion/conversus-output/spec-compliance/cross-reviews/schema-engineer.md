# Cross-Review: spec-compliance reviewing schema-engineer

**Spec**: 025-game-form-expansion

---

## Agreement

The schema-engineer's review is well-focused on model design quality. I agree with:

- The validator completeness assessment table is accurate
- The duplicate VALID_FIELD_TYPES entry observation is correct
- The suggestion for a discriminated union type is sensible for future work
- The YAML schema consistency assessment is thorough

## Disagreements

### 1. PotentialGame naming is not a compliance issue

The schema-engineer suggests renaming PotentialGame to PotentialGameResult. While this is good design advice, from a compliance perspective the current name does not violate any FR or SC. The spec says "diagnostic MUST be implemented as a check function, not a separate form" -- the model name does not determine whether it's a "form" in the spec sense. I would classify this as a style recommendation, not a finding.

### 2. Missing discriminated union is not a gap for this spec

The schema-engineer notes the lack of a `GameForm = Union[NormalFormGame, GNEPGame, ...]` type. This is a valid design observation, but no FR in spec 025 requires generic deserialization. The current design where each YAML schema is loaded and validated against its specific model (via the `example` field in tests) is sufficient for the spec's requirements.

## Additions

The schema-engineer did not assess FR-003 compliance in detail. The mode-mapping update is verified by tests, but the YAML file `mode-mapping.yml` itself should be checked for structural consistency:

- Each mapping entry should have `form` and optional `note` fields
- The `form` values should reference existing YAML schemas in game-forms/
- New mappings should not conflict with existing ones

The test suite covers functional correctness (lookup returns expected form), but not structural validation of the mapping file itself. This is a minor testing gap, not a compliance failure.
