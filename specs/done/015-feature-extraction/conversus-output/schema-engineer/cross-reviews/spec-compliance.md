# Schema Engineer Cross-Review of Spec Compliance
# Spec: 015-feature-extraction

**Cross-reviewer**: schema-engineer
**Reviewing**: spec-compliance's review at `conversus-output/spec-compliance/review.md`
**My review**: `conversus-output/schema-engineer/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: FR-005 YAML schemas — necessary artifact vs. redundant duplication

Spec-compliance marks FR-005 as NOT MET and gives creating YAML schema files P1 priority. My review does not address YAML schemas at all because I evaluate the Pydantic models as the definitive schema layer. The contradiction is in what constitutes a "feature schema": spec-compliance reads FR-005 as requiring physical YAML files in `schema/features/`; my implicit position is that Pydantic models are the schema.

**My position**: Spec-compliance is correct that FR-005 literally requires YAML files. However, the YAML files as specified serve a dual purpose: (a) human-readable documentation of features, and (b) machine-readable validation contracts. The Pydantic models already serve purpose (b). For purpose (a), the extraction source and rule metadata that FR-005 requires ("extraction source (phase, file pattern), and extraction rule (parsing logic reference)") is genuinely useful documentation that does not exist in the Pydantic models. The resolution is to create the YAML files as documentation artifacts (not validation artifacts) that reference the Pydantic models as the normative validator. This satisfies FR-005's letter while avoiding a redundant validation layer.

### DC-2: FR-014 package naming — spec amendment vs. restructuring

Spec-compliance R-3 recommends amending the spec to match the actual `conversus.schemas` namespace. My review does not address packaging. Both positions (amend spec or create separate package) are viable. The architectural argument for `conversus.schemas` is that feature models share types with game_forms and objectives (both use VALID_MODES, both are frozen Pydantic models, both are re-exported through `__init__.py`). Creating a separate `conversus-features` package would require either duplicating these shared types or introducing a `conversus-schemas` base package -- neither is worth the coupling overhead.

**Resolution**: Amend FR-014 and FR-016 to use `conversus.schemas.extraction` and `conversus.schemas.features` import paths.

---

## Tensions

### T-1: FR-007 extensibility assessment — PARTIALLY MET vs. structurally deficient

Spec-compliance marks FR-007 as PARTIALLY MET, noting that "new features can be added without breaking existing consumers" is technically true. My review M-1 argues more strongly that the flat AgentFeatures god-object is structurally deficient for extensibility. The tension is in the severity assessment: spec-compliance gives it a pass with caveats; I flag it as the highest-priority structural issue. Both assessments are defensible -- the question is whether "extensible" means "can add fields" (spec-compliance) or "can add modes cleanly" (my reading).

### T-2: CLI priority — P1 vs. deferred

Spec-compliance gives the CLI implementation (FR-012) P1 priority. My review does not address it. The CLI has no current consumers and is not on the critical path for the plugin pipeline. A P2 or P3 priority is more appropriate.

### T-3: SC-005 verifiability

Spec-compliance marks SC-005 as NOT DIRECTLY VERIFIABLE due to the packaging structure. This is accurate but somewhat academic: the dependency constraint (no numpy, no torch) is trivially verifiable by inspecting the import statements in `extraction.py` and `features.py`. The "clean pip install" framing in SC-005 is tied to the `conversus-features` package naming (FR-014), which is itself a spec-vs-implementation discrepancy. If FR-014 is amended to accept the current namespace, SC-005 should be reformulated as "the extraction modules have no dependencies beyond pydantic and stdlib."

---

## Safe Agreements

- **SA-1: FR-001 (determinism) is MET** — All three reviews agree with identical evidence.

- **SA-2: FR-002 (structural parsing) is MET** — All three reviews agree.

- **SA-3: FR-003 (graceful degradation) is MET** — All three reviews agree.

- **SA-4: FR-011 (Python API) is MET** — Both reviews confirm the API signature matches the spec.

- **SA-5: FR-015 (minimal dependencies) is MET** — Both reviews confirm stdlib + pydantic only.

- **SA-6: Unpopulated fields need implementation** — Spec-compliance R-4/R-5 and my review O-1/O-2 both identify territory_claim_vector and confirmed_count as declared but unimplemented.

- **SA-7: FR-013 pre-write validation gap** — Both reviews identify that `write_features()` does not re-validate. Spec-compliance marks FR-013 as PARTIALLY MET; my review does not address it but agrees with the diagnosis.
