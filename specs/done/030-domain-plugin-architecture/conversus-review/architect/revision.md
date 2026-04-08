# Phase 3 Revision: architect

**Spec**: 030-domain-plugin-architecture

---

## Position Changes After Cross-Review

### Modified: Concern A (gate/get_router missing from ABC) -- UPGRADED to High

The spec-compliance agent argues the missing gate endpoint should be High, not Medium. I concur. The gate is the architectural differentiator -- the "deterministic harness around indeterminate AI." Without it, the domain plugin architecture delivers scoring and persistence but not the core value proposition of spec 030 (section 3).

The spec-compliance agent also raises the architectural tension: the domains package must not import from engine (coupling rule), but the gate needs the engine. The resolution pattern is dependency injection -- the gate runner would be injected by the API server assembly code, not imported by the domains package. This pattern should be documented in the architecture.

**Revised recommendation**: Add `gate()` and `get_router()` to the ABC as default (non-abstract) methods returning `None`. Implement the `/gate/{id}` API endpoint. Design the gate runner as an injectable dependency.

### Modified: Concern C (hard block string validation) -- MAINTAINED at Medium, action refined

The schema-engineer agrees this is genuine and identified the same asymmetry (try/except in `_check_hard_blocks` but not in `_compute_weighted_score`). The fix has two parts:
1. Validate hard block syntax at scaffold load time in `load_scaffold()`.
2. Add try/except for `float()` conversion in `_compute_weighted_score()` (schema-engineer's Concern A).

### Modified: Concern E (get() searches all domains) -- MAINTAINED at Medium

Both cross-reviewers acknowledge this. The spec-compliance agent correctly notes no FR requires O(1) lookup, but from an architecture perspective, a domain hint on `get()` is the right API. The protocol should be:
```python
def get(self, record_id: str, domain: str | None = None) -> DomainRecord | None:
```
This is backward-compatible (default `None` preserves current behavior) and enables O(1) lookup when the caller knows the domain.

### Modified: Concern G (missing /gate endpoint) -- UPGRADED to High, merged with Concern A

Merging with Concern A above. Both are manifestations of the same gap: the gate lifecycle step is absent.

### Modified: Concern I (JSON vs YAML extension) -- UPGRADED to Medium

The schema-engineer rates this Medium and the spec-compliance agent confirms it contradicts FR-018 ("Scaffolds MUST be YAML files"). I accept the upgrade. The `score()` method should search for `{scaffold}.yml` first, then `.yaml`, then `.json`, rather than hard-coding `.json`.

### Surviving: Concern B (scaffold_dir not enforced) -- MAINTAINED at Low

The schema-engineer correctly notes this is consistent with how `name` and `version` are declared. All three are convention-enforced, not ABC-enforced. Maintaining Low.

### Surviving: Concern D (missing-from-scaffold variables) -- MAINTAINED at Low

No cross-reviewer disputed this. Maintained.

### Surviving: Concern F (scalability note) -- MAINTAINED at Low

Trivially fixable. Maintained.

### Surviving: Concern H (synchronous extraction timeout) -- MAINTAINED at Low

The spec-compliance agent correctly notes this is operational, not a spec concern. Maintained.

### New: _extract_field_value silent failure

My own cross-review of the schema-engineer identified that `_extract_field_value()` silently returns `None` for unknown field names. Combined with the schema-engineer's Concern F (silent filter key ignoring), there is a pattern of silent failure throughout the query/trend path. This should be addressed with logging for unknown fields.

### New: Pydantic frozen dict mutability

I noted in cross-review that `DomainScore.variables` (a `dict[str, Any]`) can be mutated despite the frozen config. This is a known Pydantic limitation. Adding to the architecture notes but not a code fix.
