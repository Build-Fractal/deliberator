# Phase 4 Disputes: architect

**Spec**: 030-domain-plugin-architecture

---

## Surviving Disputes

### DISPUTE 1: Gate lifecycle step absent from ABC and API (High)

**Status**: Surviving -- all three agents agree.

The `DomainPlugin` ABC does not define `gate()` or `get_router()`. The API router factory does not include a `/gate/{id}` endpoint. The gate is the only indeterminate component in the pipeline (spec section 3) and the core architectural differentiator of conversus.

The coupling rule creates a genuine tension: the domains package must not import from engine, but the gate needs the engine. The resolution is dependency injection -- the gate runner is injected by the API server assembly code.

**Recommended resolution**:
1. Add `gate()` and `get_router()` as non-abstract default methods on `DomainPlugin` (returning `None`).
2. Add `/gate/{id}` endpoint to the router factory, accepting an optional gate runner dependency.
3. Document the injection pattern.

### DISPUTE 2: Plugin discovery/loading not implemented (Medium)

**Status**: Surviving -- spec-compliance rates FR-002 and FR-003 as NOT MET; architect and schema-engineer concur.

No `importlib`-based plugin loading exists. The spec references `load_domain_plugins()` (section 4) for dynamic mounting. The `__init__.py` does static imports only. Without discovery, the "installable vertical product" vision (spec section 9) cannot be realized.

**Recommended resolution**: Implement `load_domain_plugins()` using `importlib.metadata.entry_points()` or a similar discovery mechanism. Handle missing packages with warning + skip.

### DISPUTE 3: score() hard-codes .json extension, contradicting FR-018 (Medium)

**Status**: Surviving -- all three agents agree after cross-review.

`DomainPlugin.score()` constructs `self.scaffold_dir / f"{scaffold}.json"` (line 447). FR-018 says scaffolds MUST be YAML files. Domains following the spec would ship YAML scaffolds that the generic `score()` method cannot find.

**Recommended resolution**: Change `score()` to search for `{scaffold}.yml`, then `.yaml`, then `.json`. Or accept any extension by searching the scaffold_dir for files matching `{scaffold}.*`.

### DISPUTE 4: Hard block condition strings not validated at load time (Medium)

**Status**: Surviving -- architect identified, schema-engineer confirmed the asymmetry.

Malformed hard block strings (e.g., missing space: `"safety <0.2"`) are silently skipped at scoring time. The `load_scaffold()` function does not validate syntax. Combined with the non-numeric variable handling gap in `_compute_weighted_score()`, the scoring path has two silent failure modes.

**Recommended resolution**:
1. Add hard block syntax validation in `load_scaffold()` -- check that each condition has exactly 3 space-separated parts with a valid operator.
2. Add try/except for `float()` in `_compute_weighted_score()`.

## Withdrawn Disputes

- **Zero total weight edge case**: Withdrawn. All agents agree this is Low and belongs in scaffold validation, not scoring runtime.
- **Exact threshold boundary behavior**: Withdrawn. The operators are standard; this is a documentation concern only.
- **Record ID as str not UUID**: Withdrawn. Pragmatic choice, Low severity.
- **SQLiteStore check_same_thread**: Withdrawn. Correct for expected scale; architectural note only.
- **Pydantic frozen dict mutability**: Withdrawn. Known framework limitation; convention-based immutability is sufficient.

## Non-Disputed Observations (for synthesis)

- Silent failure pattern in query/trend path (unknown filter keys, unknown field names) should be logged.
- YAML scaffold loading path is untested.
- SupabaseStore (FR-006) is the expected follow-up for the data layer.
- CORS and auth middleware (FR-011, FR-012) are trivial additions.
