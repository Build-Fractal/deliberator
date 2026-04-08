# Phase 3 Revision: spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Position Changes After Cross-Review

### Modified: SC-002 -- UPGRADED from NOT TESTED to PASS

The architect argues SC-002 should be PASS based on architectural analysis: separate router prefixes, separate store files/tables, no shared state between domains. I accept this reasoning. The isolation is enforced by the design, not just tested by accident.

### Modified: FR-006 -- RECLASSIFIED from PARTIAL to DEFERRED

The schema-engineer argues this should be DEFERRED (architecture supports it, backend not written) rather than PARTIAL. I accept -- the DomainStore protocol is complete and both existing backends demonstrate it. Supabase is a new backend implementation, not a missing architectural piece.

### New: Scaffolds endpoint glob bug (Medium)

All three agents confirm the API scaffolds endpoint globs `*.json` but production scaffolds are `*.yml`. This is a bug affecting FR-010 (standard endpoints).

### New: JSON/YAML extension inconsistency

Base DomainPlugin.score() resolves `f"{scaffold}.json"`, CodeReviewDomain.score() resolves `f"{scaffold}.yml"`. This inconsistency should be normalized to try multiple extensions.

### Surviving: FR-002, FR-003 NOT TESTED (importlib discovery)

No change. Plugin discovery via importlib is not implemented or tested.

### Surviving: FR-011, FR-012 NOT IMPLEMENTED (auth, CORS)

No change. These are configuration-level additions to the FastAPI app.

### Surviving: FR-015 NOT IMPLEMENTED (gate equilibrium scoring)

No change. Depends on gate infrastructure.
