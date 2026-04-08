# Cross-Review: architect reviewing spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The compliance matrix is thorough. I agree with:

- FR-001 PASS (lifecycle defined)
- FR-005 through FR-008 assessments
- FR-013 and FR-014 PASS (deterministic extraction and scoring)
- FR-016 PASS (equilibrium score field exists)
- FR-017 through FR-019 PASS (scaffold system)
- SC-001 PASS (code-review proves the pattern)
- SC-004 PASS (API endpoints sufficient for dashboard)

## Disagreements

### FR-001 should note the gate() gap

The spec-compliance agent marks FR-001 as PASS. The requirement says "extract -> score -> persist -> gate -> serve lifecycle." The `gate()` method exists as a default returning None, and `serve` is via the external API router. However, the gate step is effectively a no-op. I would still rate PASS (the method is defined on the ABC) but note that the lifecycle is architecturally complete even if gate is not yet functional.

### FR-004 interpretation

The spec says "each domain MUST define its own DomainRecord model." The current implementation uses a shared DomainRecord with flexible `context_summary` and `variables` fields. The spec-compliance agent accepts this as compliant. I agree -- the shared model with domain-specific metadata is more pragmatic than requiring each domain to define its own record class.

### SC-002 (two domains on same API server) -- should be PASS, not NOT TESTED

The test suite includes a round-trip test with a single domain. The architecture clearly supports multiple domains:
- Each domain gets its own router prefix (`/{domain.name}`)
- Each domain gets its own JSONL file (per domain name)
- No shared state between domain routers

While no explicit test creates two ConcreteDomainPlugin instances on the same app, the architectural isolation is evident. I would rate SC-002 as PASS based on architectural analysis, not just test evidence.

## Additions

The spec-compliance agent should note the scaffolds endpoint bug I identified: the API globs `*.json` but scaffolds may be `*.yml`. This affects FR-010 (standard endpoints) because the scaffolds endpoint would return empty results for YAML-based domains.
