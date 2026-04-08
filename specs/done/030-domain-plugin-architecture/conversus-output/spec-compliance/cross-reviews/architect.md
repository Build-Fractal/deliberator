# Cross-Review: spec-compliance reviewing architect

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The architect's review provides valuable design-level analysis. I agree with:

- DomainPlugin ABC is well-designed with clean separation of concerns
- DomainStore protocol is generic and extensible
- The scaffolds endpoint glob bug is real (Concern #1)
- JSONLStore.get() scanning all files is a performance concern (Concern #4)

## Disagreements

### Concern #1 (scaffolds glob bug) severity -- I agree with Medium

The architect rates the scaffolds endpoint glob pattern as Medium. The schema-engineer's cross-review confirms this by noting the test uses JSON scaffolds (so the test passes) but production code-review scaffolds are YAML. I concur with Medium severity -- this is a bug that would manifest in any production deployment using YAML scaffolds.

### SC-002 (two domains on same API server) -- I accept architect's argument for PASS

The architect argues SC-002 should be PASS based on architectural analysis: each domain gets its own router prefix and store files, with no shared state. While I originally rated it NOT TESTED, the architectural isolation is clear and the test infrastructure (ConcreteDomainPlugin) could easily be duplicated. I accept PASS.

## Additions

The architect identified the dual scoring path issue (base.py vs CodeReviewDomain hard block parsing). I want to flag a related concern: the base DomainPlugin.score() loads scaffolds from `self.scaffold_dir / f"{scaffold}.json"` (line 447), while CodeReviewDomain.score() loads from `SCAFFOLD_DIR / f"{scaffold}.yml"` (line 375). The extension mismatch (.json vs .yml) means the base class and the code-review domain use different scaffold file formats by default.

This is another manifestation of the JSON/YAML inconsistency. The base class assumes JSON scaffolds, the code-review domain uses YAML. The `load_scaffold()` function handles both formats based on extension, but the callers use hardcoded extensions. This should be normalized.
