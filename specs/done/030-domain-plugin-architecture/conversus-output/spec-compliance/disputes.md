# Phase 4 Disputes: spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Surviving Disputes

### DISPUTE 1: Scaffolds endpoint and extension inconsistency (Medium)

**Status**: Surviving -- all three agents.

Three related issues:
1. API scaffolds endpoint globs `*.json` only
2. Base DomainPlugin.score() resolves `{scaffold}.json`
3. CodeReviewDomain.score() resolves `{scaffold}.yml`

All three should be normalized to support multiple extensions.

### DISPUTE 2: scaffold_dir enforcement on ABC (Medium)

**Status**: Surviving -- architect and schema-engineer.

No enforcement that subclasses set scaffold_dir. Produces confusing errors.

### DISPUTE 3: FR-002/FR-003 plugin discovery not tested (Medium)

**Status**: Surviving -- spec-compliance only.

The spec requires importlib-based plugin loading and graceful handling of missing packages. Neither is implemented or tested. This is the foundation of the multi-domain vision.

### DISPUTE 4: FR-011/FR-012 auth and CORS not implemented (Low)

**Status**: Surviving -- acknowledged.

Required for team/web deployments. Easy to add with FastAPI middleware.

## Withdrawn Disputes

- SC-002 revised to PASS (architectural isolation is clear)
- FR-006 revised to DEFERRED (architecture supports Supabase)
