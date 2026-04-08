# Schema Engineer Disputes — 015 Feature Extraction Pipeline

**Role**: schema-engineer
**Phase**: 4 — Disputes
**Date**: 2026-03-24

---

## Remaining Disputes

- **Dispute: AgentFeatures interim `mode` field — useful stepping stone vs. false signal**
  - **My claim**: Adding `mode: str | None = None` to AgentFeatures is a non-breaking, immediately useful improvement that enables consumers to filter relevant fields by mode. Cite: schema-engineer revision NR-1.
  - **Opposing position(s)**: Extraction-engineer disputes R-1 argues that the `mode` field is "informational, not discriminatory" and trains consumers to code against a pattern that will be deprecated. They prefer full deferral or full refactoring, with no interim step.
  - **Why I will not concede**: The `mode` field has concrete immediate value independent of the future discriminated union. A plugin receiving an AgentFeatures today has no way to know which fields are semantically meaningful. The plugin must either (a) assume the mode from the parent FeatureSet and hardcode a mapping of mode-to-relevant-fields, or (b) check every field for non-zero values and infer. Both are worse than reading `af.mode`. The field is not a "stepping stone" in the sense that the discriminated union will build on it; it is a self-contained improvement that makes the current flat model usable.
  - **Counter-argument to their position**: Extraction-engineer argues Pydantic discriminated unions use `Literal` types, not runtime `str` values, so the `mode` field does not step toward subclasses. This is technically correct for the type system, but it conflates two consumers: the Pydantic validator (which uses Literal) and the application code (which reads the string value). Application code reading `af.mode == "cooperative"` is not "runtime type checking" -- it is domain-logic branching, which is legitimate and necessary regardless of schema design.
  - **Proposed resolution path**: Add `mode: str | None = None` to AgentFeatures now. If the discriminated union is later adopted, the `mode` field becomes the `Literal` discriminator on the base class, not a deprecated field. The two designs are compatible, not sequential. The synthesizer should decide.

- **Dispute: Disposition regex approach — two-pass vs. single permissive**
  - **My claim**: The single permissive regex is safer for LLM-generated output. Cite: schema-engineer T-1 in cross-review of extraction-engineer.
  - **Opposing position(s)**: Extraction-engineer disputes R-2 insists on a strict primary regex with a permissive fallback (two-pass). They argue FR-002 requires matching the prescribed format.
  - **Why I will not concede**: The two-pass approach has a failure mode that extraction-engineer does not address: if the strict regex matches N items and the permissive regex matches N+1 (because one disposition uses a slightly malformed marker), the pipeline uses the strict count (N), silently losing one recommendation. The correct behavior is to extract all dispositions, including slightly malformed ones, and log anomalies. A single-pass permissive regex with anomaly logging achieves this without the N-vs-N+1 discrepancy risk.
  - **Counter-argument to their position**: Extraction-engineer argues the permissive pattern can match non-label text. This is mitigated by context: the pattern is applied within recommendation sections (split by `#### Recommendation N` headings), not against the entire document. Within a recommendation section, there is at most one disposition label, and the permissive pattern will not produce false positives in that scoped context.
  - **Proposed resolution path**: Single-pass permissive regex scoped within recommendation sections, with `logger.warning()` when the matched text does not have balanced `\*\*` markers. The synthesizer should choose between two-pass and scoped-permissive.

---

## Convergence

- **Converged: Position vector normalization**
  - **Shared position**: All position vectors in a round must be padded to the same length (max recommendations across agents).
  - **Agreeing agents**: extraction-engineer (R-1), schema-engineer (DC-1), spec-compliance (DC-1)
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1. No disagreement at any phase.

- **Converged: Implement territory_claim_vector and confirmed_count**
  - **Shared position**: Both fields must have extraction logic implemented.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1.

- **Converged: Amend FR-014/FR-016 to conversus.schemas namespace**
  - **Shared position**: No standalone `conversus-features` package. Use `conversus.schemas` import paths.
  - **Agreeing agents**: All three reviewers.
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 2.

- **Converged: JSON Schema for FR-005**
  - **Shared position**: Generate JSON Schema from Pydantic models to satisfy per-mode schema requirement.
  - **Agreeing agents**: schema-engineer (R-8), spec-compliance (R-1 revised)
  - **Strength**: Bilateral
  - **Path to convergence**: Emerged through cross-review when spec-compliance adopted schema-engineer's JSON Schema proposal as the replacement for YAML files.

- **Converged: FeatureSetMetadata with extra="allow"**
  - **Shared position**: Create a typed model for metadata with `extra="allow"` for forward-compatible extensibility.
  - **Agreeing agents**: schema-engineer (R-6 revised), spec-compliance (T-2)
  - **Strength**: Bilateral
  - **Path to convergence**: Spec-compliance proposed the compromise in cross-review; schema-engineer adopted it in revision.

---

## Final Position Statement

**Non-Negotiables**:
- The `mode` field on AgentFeatures (NR-1). Without it, consumers have no programmatic way to determine which fields are semantically relevant. This is a usability gap, not a schema purity question.
- Implementing territory_claim_vector and confirmed_count (R-5). Declared-but-empty fields are worse than absent fields.

**Flexibility**:
- Disposition regex approach. I prefer single-pass permissive, but will accept two-pass if the scoping concern (applied within recommendation sections) is acknowledged.
- VALID_MODES deduplication (R-3). Correct but low-urgency. Flexible on timing.
