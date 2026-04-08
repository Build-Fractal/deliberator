# Cross-Review: schema-engineer reviewing spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The compliance matrix is comprehensive and well-structured. I agree with:

- FR-001 through FR-004 assessments
- FR-005 through FR-008 assessments
- FR-013, FR-014 PASS (deterministic harness)
- SC-001 PASS (code-review validates the pattern)

## Disagreements

### FR-006 (3 backends) -- severity distinction

The spec-compliance agent marks FR-006 as PARTIAL (2 of 3 backends). I would note that the two implemented backends (JSONL and SQLite) cover the primary use cases:
- JSONL: CLI/local development (zero deps)
- SQLite: single-machine deployments

Supabase is for team/web deployments, which is a more advanced use case. The protocol makes adding it straightforward. I would classify this as DEFERRED rather than PARTIAL -- the architecture supports it, the backend just hasn't been written yet.

### FR-011 and FR-012 (auth and CORS) -- NOT IMPLEMENTED is correct, but note architectural support

The FastAPI framework supports both authentication middleware and CORS middleware as first-class features. Adding them to the API is a configuration step:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

These are framework features, not architectural gaps. The implementation effort is minimal.

## Additions

The spec-compliance agent did not assess the `create_domain_router` function's error handling. If a domain's scaffold directory doesn't exist, the scaffolds endpoint returns an empty list (line 205: `if not domain.scaffold_dir.exists(): return scaffolds`). This is graceful degradation -- no 500 error. Good practice.

However, the submit endpoint (line 128: `score = domain.score(variables, request.scaffold)`) would raise an exception if the scaffold name is invalid. This would produce a 500 error rather than a 400. Consider adding a try/except with HTTPException(400) for invalid scaffold names.
