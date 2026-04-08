# Phase 4 Disputes: spec-compliance

**Spec**: 030-domain-plugin-architecture

---

## Surviving Disputes

### DISPUTE 1: Gate lifecycle absent -- FR-001 NOT MET, FR-010 PARTIALLY MET, FR-015 NOT MET (High)

**Status**: Surviving -- all three agents reached consensus.

Three functional requirements depend on the gate: FR-001 (lifecycle definition), FR-010 (standard endpoint set), FR-015 (gate output includes equilibrium score). None are fully met. This is the highest-priority gap.

From a compliance perspective, this is not just a missing feature -- it is a missing architectural component. The gate is where the "deterministic harness around indeterminate AI" (spec section 3) is realized. Without it, the domain plugin architecture is a scoring and persistence framework, not a deliberation framework.

**Evidence**: base.py lines 377-503 (no gate/serve methods); api.py lines 97-225 (no /gate endpoint).

### DISPUTE 2: Plugin discovery -- FR-002 NOT MET, FR-003 NOT MET (Medium)

**Status**: Surviving -- consensus.

No `importlib`-based discovery. No `load_domain_plugins()` function. No graceful handling of missing packages. The spec's section 5 (Domain Plugin Registry) describes a configuration-driven discovery system that does not exist.

**Evidence**: `__init__.py` has only static imports. No entry_points registration. No config-driven factory.

### DISPUTE 3: score() extension vs FR-018 (Medium)

**Status**: Surviving -- consensus.

FR-018 says "Scaffolds MUST be YAML files." `DomainPlugin.score()` (base.py line 447) constructs paths with `.json` extension. Direct contradiction.

**Evidence**: base.py line 447: `scaffold_path = self.scaffold_dir / f"{scaffold}.json"`.

### DISPUTE 4: Hard block validation + non-numeric variables (Medium)

**Status**: Surviving -- architect and schema-engineer both identified facets.

Two silent failure modes in the scoring path:
1. Malformed hard block strings silently skipped (no validation in `load_scaffold()`).
2. Non-numeric variables cause `ValueError` in `_compute_weighted_score()` (no try/except).

These are not FR violations per se, but they degrade the deterministic guarantees of FR-013 and FR-014: if extraction produces unexpected types, scoring is not deterministic (it either crashes or skips variables depending on which function processes them).

### DISPUTE 5: Silent query/trend degradation (Medium)

**Status**: Surviving -- schema-engineer identified, architect confirmed.

Unknown filter keys and unknown trend field names produce silent incorrect results. Not a direct FR violation, but undermines the trust calibration promised by FR-016 (if trend data is wrong due to a typo, calibration is unreliable).

## Withdrawn Disputes

- **FR-007 (backend selection via config)**: Upgraded from PARTIALLY MET to NOT MET after architect's cross-review. Not disputed -- accepted.
- **FR-001**: Upgraded from PARTIALLY MET to NOT MET after schema-engineer's cross-review. Not disputed -- accepted.
- **All Low/Info items**: Consensus reached. Not disputed.

## Non-Disputed Gaps for Follow-Up

| FR/SC | Status | Follow-Up |
|-------|--------|-----------|
| FR-006 | PARTIALLY MET | Implement SupabaseStore |
| FR-007 | NOT MET | Implement config-driven store factory |
| FR-009 | PARTIALLY MET | Implement dynamic router mounting via plugin discovery |
| FR-011 | NOT MET | Add API key / OAuth middleware |
| FR-012 | NOT MET | Add CORS middleware |
| FR-017 | NOT ASSESSED | Per-domain: ensure 3+ scaffolds per domain |
| FR-019 | PARTIALLY MET | Add scaffold CLI tooling or documentation |
| SC-003 | NOT MET | Requires SupabaseStore implementation |
| SC-005 | NOT ASSESSED | Requires gate implementation for end-to-end benchmark |
