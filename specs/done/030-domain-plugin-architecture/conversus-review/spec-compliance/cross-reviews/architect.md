# Cross-Review: spec-compliance reviewing architect

**Spec**: 030-domain-plugin-architecture

---

## Agreement

The architect's review is structurally sound and identifies the right architectural concerns. I agree with:

- **Concern A (gate/get_router missing)**: This is the most significant gap. The spec's lifecycle is a 5-step sequence. The implementation delivers 3 of 5 steps. From a compliance perspective, this maps to my FR-001 PARTIALLY MET (or NOT MET per the schema-engineer's argument).
- **Concern C (hard block string validation)**: Valid. Malformed conditions are a scaffold quality issue that should be caught at load time, not silently at score time.
- **Concern E (get() performance)**: Valid, though from a compliance perspective this is not a spec violation -- no FR requires O(1) lookup.
- **Coupling rules enforced**: Confirmed. I independently verified zero engine imports across all three modules.

## Disagreements

### 1. Concern G severity -- should be HIGH, not Medium

The architect rates the missing `/gate/{id}` endpoint as Medium. From a compliance perspective, this is **HIGH**. FR-010 explicitly lists "gate" in the required endpoint set. FR-015 requires the gate's output to include an equilibrium score. The gate is the architectural differentiator of conversus -- it is the "deterministic harness around indeterminate AI" that the spec's section 3 describes as the core value proposition. Omitting the gate endpoint means the API cannot run deliberations, which is the primary use case for team deployments.

I recognize that implementing the gate requires integration with the conversus engine (which would violate the coupling rules). This is a genuine architectural tension: the domains package must not import from engine, but the gate needs the engine. The resolution is likely a gate runner that is injected via the API server assembly code, not imported by the domains package. This design pattern is not documented.

### 2. Concern H (synchronous extraction) -- AGREE but not a spec concern

The architect raises the risk of synchronous extraction timing out. This is a valid operational concern but not a spec compliance issue. FR-005 through FR-012 do not require async. SC-005 requires the full pipeline to complete in 90 seconds, which is an end-to-end requirement. Synchronous extraction only matters if individual extractors are slow, which is domain-dependent.

### 3. Concern I (JSON vs YAML extension) -- AGREE, and it contradicts FR-018

The architect correctly identifies that `score()` hard-codes `.json` while `load_scaffold()` supports YAML. I add that this directly contradicts FR-018 ("Scaffolds MUST be YAML files"). If the spec says YAML, the code should default to `.yml`, not `.json`. The `score()` method should search for `{scaffold}.yml` first, then fall back to `.json`, or accept any supported extension.

## Additions

The architect's review did not assess the spec's constraint from section 8: "The API server is optional -- domains work as libraries without it." This is satisfied: `base.py` and `store.py` have no FastAPI dependency. `api.py` imports FastAPI, but it is an optional module. Domains can extract, score, and persist without the API layer. This constraint is well-preserved by the module structure.

The architect also did not note that the `conversus.yml` configuration for spec 030 itself (the review config) lists `validate_templates: false`. This suggests the review was configured without template validation, which is appropriate for a first-pass review of new code.
