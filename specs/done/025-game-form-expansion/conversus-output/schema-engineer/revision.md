# Phase 3 Revision: schema-engineer

**Spec**: 025-game-form-expansion

---

## Position Changes After Cross-Review

### Modified: BayesianGame prior key validation -- UPGRADED to Medium

The game-theorist's cross-review makes a compelling case: invalid prior keys silently produce a valid model that would fail at solver time. I accept the upgrade from Info to Medium.

**Revised recommendation**: Add a model_validator that computes the Cartesian product of type_space values and verifies that all prior keys correspond to valid type profile tuples (comma-joined sorted types).

### Withdrawn: PotentialGame naming suggestion

Both cross-reviewers note this is a style preference, not a functional issue. The spec-compliance agent correctly observes it's not a compliance concern. I withdraw the suggestion to rename PotentialGame to PotentialGameResult. The `form: Literal["potential"]` discriminator makes the intent clear.

### Surviving: Duplicate VALID_FIELD_TYPES entry

No cross-reviewer disputed this. It's a cosmetic issue but should be fixed to avoid confusion.

### Surviving: Discriminated union type suggestion

The spec-compliance agent notes no FR requires this. I agree it's not a compliance issue, but maintain it as a design recommendation for future work. With 9+ game forms, a `GameForm = Annotated[Union[...], Field(discriminator="form")]` type would improve the developer experience significantly.

### New: Single-player Shapley test gap

The spec-compliance agent's cross-review of the game-theorist identified this. I concur -- adding a test for a single-player coalitional game (where Shapley value trivially equals v({player})) would improve coverage. This is a Low-severity test gap.
