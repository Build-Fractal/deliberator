# Spec Compliance Cross-Review of Schema Engineer
# Spec: 015-feature-extraction

**Cross-reviewer**: spec-compliance
**Reviewing**: schema-engineer's review at `conversus-output/schema-engineer/review.md`
**My review**: `conversus-output/spec-compliance/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: AgentFeatures discriminated union — spec compliance vs. architectural improvement

Schema-engineer R-1 recommends refactoring AgentFeatures into per-mode discriminated unions. My review marks FR-007 (extensibility) as PARTIALLY MET but does not recommend a specific model restructuring. The contradiction is in the compliance assessment: if the flat model is architecturally deficient for extensibility (schema-engineer's position), then FR-007 should be NOT MET rather than PARTIALLY MET.

**My position**: FR-007 says "new features can be added without breaking existing consumers." Adding a field with a default to the current flat model does not break existing consumers. The flat model is FR-007 compliant by the letter of the requirement. Schema-engineer's concern is about clean extensibility (adding new modes), which is a design quality concern beyond what FR-007 literally requires. I maintain PARTIALLY MET because the flat model is extensible but not cleanly extensible.

### DC-2: VALID_MODES deduplication — shared module vs. current structure

Schema-engineer M-3 recommends deduplicating VALID_MODES into a shared module. My review does not flag this. The two identical frozensets create a theoretical maintenance risk but not a practical one: adding a new mode is a spec-level change that touches dozens of files. The deduplication is correct but low-priority compared to the parsing and packaging gaps I identify.

---

## Tensions

### T-1: FR-005 YAML schemas vs. Pydantic-only schemas

Schema-engineer does not address FR-005 at all, implicitly accepting Pydantic models as sufficient. My review marks FR-005 as NOT MET because the spec explicitly requires YAML files. This tension reflects a broader question: is the spec's requirement for YAML schema files an architectural decision or a documentation preference? If architectural, Pydantic models do not satisfy it. If documentation, they partially do.

**My position**: The spec's FR-005 is a deliberate design choice: YAML files serve as language-agnostic contracts that external tools can consume without importing Python. Schema-engineer's R-8 (JSON Schema export) is a better solution to the same problem: generate the schema from the Pydantic model at build time. If R-8 is adopted, FR-005 should be amended to accept either YAML or JSON Schema as the per-mode schema file.

### T-2: FeatureSetMetadata typed model — value vs. complexity

Schema-engineer R-6 recommends replacing `metadata: dict[str, Any]` with a typed `FeatureSetMetadata` model. My review does not address metadata typing. The typed model improves discoverability but adds a maintenance obligation: every new metadata field requires a model change. The current `dict[str, Any]` is pragmatic for a metadata bag whose contents may evolve.

**My position**: Compromise: create a `FeatureSetMetadata` model with `extra="allow"` so that known fields are typed but unknown fields pass through. This gives discoverability for common fields without blocking extension.

---

## Safe Agreements

- **SA-1: Frozen models are correct** — Both reviews agree frozen Pydantic models are the right choice.

- **SA-2: FeatureSet mode validation works** — Both reviews confirm the model_validator catches invalid modes.

- **SA-3: Default values enable FR-003 compliance** — Both reviews agree zero defaults are correct for graceful degradation.

- **SA-4: Unpopulated fields should be resolved** — Schema-engineer O-1/O-2 and my review R-4/R-5 both flag territory_claim_vector and confirmed_count.

- **SA-5: FR-015 dependencies are minimal** — Both reviews confirm no heavyweight dependencies.

- **SA-6: __all__ should be added** — Schema-engineer R-7 recommends adding `__all__` to features.py. My review does not flag this but agrees it is good practice.
