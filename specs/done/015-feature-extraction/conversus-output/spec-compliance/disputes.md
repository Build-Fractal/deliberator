# Spec Compliance Disputes — 015 Feature Extraction Pipeline

**Role**: spec-compliance
**Phase**: 4 — Disputes
**Date**: 2026-03-24

---

## Remaining Disputes

- **Dispute: CLI entry point priority — P1 (FR-012 compliance) vs. P2 (practical urgency)**
  - **My claim**: FR-012 is a MUST requirement ("The pipeline MUST also support CLI invocation"). A MUST requirement that is NOT MET should be P1 by definition. Cite: spec-compliance review FR-012 assessment.
  - **Opposing position(s)**: Extraction-engineer T-1 (cross-review) argues the CLI is not on the critical path for the plugin pipeline. Schema-engineer does not address FR-012.
  - **Why I will not concede**: The spec uses RFC 2119 language: "MUST." A MUST requirement is not optional regardless of whether current consumers use it. The distinction between P1 and P2 is whether the requirement blocks the spec from moving to "done" status. An unimplemented MUST requirement blocks it. The CLI can be a minimal implementation (10-20 lines with argparse), but it must exist.
  - **Counter-argument to their position**: Extraction-engineer's argument is about practical urgency, not compliance. The plugin pipeline using Python API does not excuse the missing CLI any more than "nobody reads the docs" excuses missing documentation. The spec says MUST; the implementation must comply.
  - **Proposed resolution path**: Implement a minimal CLI as part of the spec 015 deliverables. If the full `conversus-features` command name is being replaced by `conversus.schemas` import paths (convergence C-3), then the CLI command name should also be updated. The synthesizer should confirm the CLI requirement and command name.

- **Dispute: FR-005 disposition — amend spec vs. implement YAML schemas**
  - **My claim**: FR-005 requires per-mode YAML schema files. The spec should be implemented as written, or formally amended. A build-time JSON Schema generation (schema-engineer R-8, my R-1 revised) is an acceptable alternative, but the spec must be explicitly amended to reflect this change. Simply implementing JSON Schema without amending FR-005 leaves the spec in an inconsistent state.
  - **Opposing position(s)**: Extraction-engineer DC-1 and schema-engineer implicitly treat FR-005 as satisfied by Pydantic models, without formal amendment.
  - **Why I will not concede**: Spec drift without amendment is a process violation. If the implementation diverges from the spec, the spec must be updated. The convergence on JSON Schema is good, but it requires an explicit FR-005 amendment: "Each mode MUST have a feature schema defined as a JSON Schema file generated from the Pydantic model, stored in `schema/features/{mode}.schema.json`."
  - **Counter-argument to their position**: Treating a MUST requirement as implicitly satisfied by a different mechanism than what the spec describes creates a precedent where any spec requirement can be "met" by something vaguely similar. The amendment process exists to prevent this.
  - **Proposed resolution path**: Amend FR-005 explicitly as part of this spec review's output. The synthesizer should include the amendment text in the actionable spec changes.

---

## Convergence

- **Converged: Position vector normalization**
  - **Shared position**: Pad all position vectors to max(recommendation_count) across agents.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Implement territory_claim_vector and confirmed_count**
  - **Shared position**: Both declared-but-unimplemented fields must have extraction logic added.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Amend FR-014/FR-016 package naming**
  - **Shared position**: Use `conversus.schemas` namespace. Amend spec text.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 2.

- **Converged: Add `plugins/` to exclusion list**
  - **Shared position**: Forward-compatibility with spec 016.
  - **Agreeing agents**: extraction-engineer (R-6), spec-compliance (NR-2)
  - **Strength**: Bilateral
  - **Path to convergence**: Proposed Phase 1, endorsed Phase 2.

- **Converged: Pre-write validation in write_features()**
  - **Shared position**: Add model_validate call before JSON serialization.
  - **Agreeing agents**: extraction-engineer (R-7), spec-compliance (R-6)
  - **Strength**: Bilateral
  - **Path to convergence**: Both independently identified in Phase 1.

---

## Final Position Statement

**Non-Negotiables**:
- CLI implementation (FR-012). A MUST requirement must be implemented. It can be minimal, but it must exist. The spec cannot move to "done" with an unimplemented MUST.
- Explicit spec amendments for FR-005, FR-014, FR-016. Implementation divergence from spec text must be reconciled through formal amendment, not implicit acceptance.

**Flexibility**:
- CLI command naming. If the package is `conversus.schemas` (not `conversus-features`), the CLI command name should be updated accordingly. I am flexible on the specific command name as long as it exists.
- AgentFeatures `mode` field. I do not have a strong position on this schema design question. Both approaches (mode field now, or defer entirely) are FR-007 compliant.
