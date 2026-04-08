# Phase 4 Disputes: optimization-engineer

**Spec**: 026-optimization-template-library

---

## Surviving Disputes

### DISPUTE 1: Cross-reference validation for game_form and mode_compatibility (Low)

**Status**: Surviving -- all agents agree.

Template game_form and mode_compatibility values are not validated against their respective source-of-truth files (game-forms/*.yml, mode-mapping.yml). This allows silently invalid references.

**Recommended resolution**: Add two parametric tests:
1. For each template, verify game_form value matches a filename in schema/game-forms/
2. For each template, verify each mode_compatibility value is a key in mode-mapping.yml

## Withdrawn Disputes

- PSD validation: Downgraded to Info, not a dispute
- Supply-demand sum-to-zero: Downgraded to Info, not a dispute
- String-encoded matrices: Info observation, no dispute
