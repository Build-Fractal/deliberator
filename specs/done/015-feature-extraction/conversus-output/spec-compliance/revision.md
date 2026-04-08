# Spec Compliance Revision: 015 Feature Extraction Pipeline

**Reviewer**: spec-compliance
**Revision iteration**: 1
**Date**: 2026-03-24

---

## Recommendation Dispositions

#### Recommendation 1: Create per-mode YAML feature schema files

- **Original position**: Create `schema/features/{mode}.yml` files per FR-005.
- **Disposition**: Modified
- **Explanation**: Extraction-engineer DC-1 argues YAML files that duplicate Pydantic models create maintenance drift risk. Schema-engineer R-8 (revised) proposes generating JSON Schema from Pydantic models to satisfy FR-005. Modified recommendation: amend FR-005 to accept machine-generated JSON Schema files as the per-mode schema artifact. Generate `schema/features/{mode}.schema.json` from `FeatureSet.model_json_schema()` at build time. Add the extraction source and rule metadata as `x-conversus-source` and `x-conversus-rule` JSON Schema extensions on each property. This satisfies FR-005's intent (machine-readable, language-agnostic schema) without creating a manually-maintained parallel artifact.

#### Recommendation 2: Implement CLI entry point

- **Original position**: Create CLI per FR-012 at P1 priority.
- **Disposition**: Modified
- **Explanation**: Extraction-engineer T-1 argues the CLI is not on the critical path since plugins use the Python API. Modified to P2 priority. The CLI remains a legitimate FR-012 requirement, but the Python API (FR-011) is the primary interface for the plugin pipeline. The CLI should be implemented but after the parsing and schema fixes are stable.

#### Recommendation 3: Resolve package naming (conversus.schemas vs. conversus-features)

- **Original position**: Amend spec to match actual namespace.
- **Disposition**: Surviving
- **Explanation**: Schema-engineer DC-2 agrees with amending. Extraction-engineer DC-2 agrees. No cross-review argues for creating a standalone package. Amend FR-014 to: "The pipeline MUST ship within the `conversus.schemas` package." Amend FR-016 to: "The package MUST be importable by plugins: `from conversus.schemas import extract_features, FeatureSet`."

#### Recommendation 4: Implement territory_claim_vector extraction

- **Original position**: Implement extraction logic for PD territory claims.
- **Disposition**: Surviving
- **Explanation**: All three reviews flag this gap. The extraction should parse Phase 1 review sections (Core Competencies, Unique Capabilities, Shared Territory, Deferrals) and produce a binary vector per topic area.

#### Recommendation 5: Implement confirmed_count extraction

- **Original position**: Implement extraction logic for red-blue confirmed findings.
- **Disposition**: Surviving
- **Explanation**: All three reviews flag this gap. The extraction should count findings confirmed as valid from the Phase 4 disputes or synthesis.

#### Recommendation 6: Add explicit pre-write validation

- **Original position**: Add model_validate call in write_features().
- **Disposition**: Surviving
- **Explanation**: Extraction-engineer R-7 agrees. Schema-engineer does not contest. The fix ensures FR-013 compliance for all code paths, not just the normal pipeline path.

#### Recommendation 7: Add pyyaml dependency or remove YAML schema reference

- **Original position**: Resolve the dependency mismatch if YAML schemas are created.
- **Disposition**: Withdrawn
- **Explanation**: With R-1 modified to use JSON Schema instead of YAML, the pyyaml question is moot. JSON Schema generation uses only pydantic's built-in `model_json_schema()` with no additional dependencies.

---

## New Recommendations

- **Amend spec Section 2 extraction rules with priority-absent defaults** (Priority: P2)
  - Triggered by: Extraction-engineer M-1/R-8 identifying undocumented defaults for priority-absent position vector construction.
  - Proposed change: Add to spec Section 2, cooperative extraction rules: "When a recommendation section does not include a Priority: P1/P2/P3 label, Surviving recommendations default to position value 2 and Modified recommendations default to position value 1."
  - Rationale: Documents an implementation choice that affects FR-001 determinism. Future implementors need this specification to produce compatible feature vectors.

- **Add `plugins` to non-agent directory exclusion list in extraction** (Priority: P2)
  - Triggered by: Extraction-engineer R-6, endorsed by spec-compliance T-1.
  - Proposed change: Add `"plugins"` to the exclusion set in `_discover_agent_names()`, `_extract_pd_agent_features()`, and `_extract_rb_agent_features()`.
  - Rationale: Forward-compatibility with spec 016's plugin output directory.

---

## Position Summary

Withdrew 1, modified 2, maintained 4. Added 2 new recommendations.

The most significant change is R-1 (YAML schemas), which shifted from manually-authored YAML files to machine-generated JSON Schema. This resolves the cross-review tension between literal FR-005 compliance and practical maintenance concerns. The withdrawal of R-7 (pyyaml dependency) is a direct consequence.

My highest-priority surviving recommendation is R-3 (package naming amendment). The discrepancy between FR-014/FR-016's `conversus-features` naming and the actual `conversus.schemas` namespace affects compliance assessment of three requirements. Amending the spec resolves all three at once.
