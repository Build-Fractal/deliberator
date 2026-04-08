# Phase 4 Disputes: architect

**Spec**: 030-domain-plugin-architecture

---

## Surviving Disputes

### DISPUTE 1: Scaffolds endpoint glob bug (Medium)

**Status**: Surviving -- all three agents confirm.

The API scaffolds endpoint (api.py line 208) globs `*.json` but the code-review domain uses `*.yml` scaffolds. This would return empty results in production.

**Recommended resolution**: Change the glob to include `*.json`, `*.yml`, and `*.yaml`. Also normalize scaffold name resolution in DomainPlugin.score() to try multiple extensions rather than hardcoding `.json`.

### DISPUTE 2: scaffold_dir enforcement (Medium)

**Status**: Surviving -- architect and schema-engineer agree.

DomainPlugin ABC declares scaffold_dir but does not enforce it. A subclass that forgets to set it gets a confusing FileNotFoundError.

**Recommended resolution**: Add `__init_subclass__` validation or a runtime check in score() with a descriptive error message like "scaffold_dir is not set on this DomainPlugin subclass."

### DISPUTE 3: API submit endpoint error handling (Low)

**Status**: Surviving -- schema-engineer and spec-compliance.

An invalid scaffold name produces a 500 error instead of a 400 from the submit endpoint.

**Recommended resolution**: Wrap load_scaffold() call in try/except, return HTTPException(status_code=400, detail=f"Unknown scaffold: {request.scaffold}").

## Withdrawn Disputes

- JSONLStore.get() performance: Info, expected for file-based store
- Dual scoring paths: Low, expected for domain customization
