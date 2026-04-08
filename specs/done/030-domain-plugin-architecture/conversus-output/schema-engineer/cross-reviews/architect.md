# Cross-Review: schema-engineer reviewing architect

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The architect's review is comprehensive and identifies important design observations. I agree with:

- DomainPlugin ABC design is clean with proper separation of concerns
- DomainStore protocol is generic and extensible
- API router factory pattern is sound
- The scaffolds endpoint glob bug (Concern #1) is real and should be fixed

## Disagreements

### Concern #2 (scaffold_dir not enforced) severity -- should be Medium, not Low

The architect rates the missing scaffold_dir enforcement as Low. I believe it's **Medium** because:

- It's a common footgun: a domain author subclassing DomainPlugin might forget to set scaffold_dir
- The error when score() is called with a string scaffold name would be: `FileNotFoundError: Scaffold file not found: ./{scaffold_name}.json`
- This error message doesn't mention scaffold_dir at all, making debugging difficult

**Recommendation**: Either make `scaffold_dir` a required abstract class variable (via `__init_subclass__`), or add a check in `score()` that produces a clear error message.

### Concern #3 (dual scoring paths) -- I agree with Low

The base scoring uses `_check_hard_blocks()` (3-part conditions only), while CodeReviewDomain uses `_evaluate_hard_block()` (also supports bare variable truthy checks). This inconsistency is Low because domain authors typically override score() to customize for their domain. The base scoring is a convenience, not the primary path.

## Additions

The architect identified the scaffolds endpoint glob pattern bug but did not verify the test impact. The test `TestDomainAPI.test_scaffolds` creates a `default.json` scaffold file, so the test passes. But in production with YAML scaffolds, the endpoint would return empty. This reinforces the Medium severity of the bug.

I would also note that the `load_scaffold()` function correctly handles both `.yml` and `.json` extensions, but the caller in the API (api.py line 208) only globs `.json`. The fix is simple: glob `*.json` + `*.yml` + `*.yaml`.
