# Phase 3 Revision: architect

**Spec**: 030-domain-plugin-architecture

---

## Position Changes After Cross-Review

### Modified: Concern #1 (scaffolds endpoint glob) -- MAINTAINED at Medium

Both the schema-engineer and spec-compliance agent confirm this is a real bug. The API endpoint globs `*.json` but the code-review domain uses `*.yml` scaffolds. The test passes because the test fixture creates a `.json` file.

**Revised recommendation**: Change the scaffolds endpoint to glob `*.json`, `*.yml`, and `*.yaml`. Also normalize the base DomainPlugin.score() to try multiple extensions when resolving scaffold names.

### Modified: Concern #2 (scaffold_dir enforcement) -- UPGRADED to Medium

The schema-engineer argues this should be Medium due to the confusing error message when scaffold_dir is unset. I accept. A subclass forgetting to set scaffold_dir would get `FileNotFoundError: Scaffold file not found: ./default.json` which is unhelpful.

**Revised recommendation**: Add `__init_subclass__` check or a runtime check in score() with a clear error message.

### Modified: Concern #3 (dual scoring paths) -- MAINTAINED at Low

Cross-review consensus supports Low. Domain authors override score() for customization. The base scoring is a convenience.

### New: JSON/YAML extension inconsistency across the codebase

The spec-compliance agent identified that base DomainPlugin.score() assumes `.json` scaffolds while CodeReviewDomain uses `.yml`. This is a broader manifestation of Concern #1. The fix should normalize scaffold resolution to try multiple extensions.

### New: API submit endpoint missing error handling for invalid scaffold names

The schema-engineer's cross-review of spec-compliance identified this. An invalid scaffold name in the submit endpoint produces a 500 instead of a 400. Should add try/except with HTTPException(400).

### Withdrawn: JSONLStore.get() performance concern

The spec-compliance agent notes this is expected behavior for a file-based store. For < 10K records (documented limit), the scan is acceptable. Maintaining as Info observation, not a concern.
