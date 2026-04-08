# Extraction Engineer Disputes — 015 Feature Extraction Pipeline

**Role**: extraction-engineer
**Phase**: 4 — Disputes
**Date**: 2026-03-24

---

## Remaining Disputes

- **Dispute: Disposition regex strictness — primary-strict vs. permissive-only**
  - **My claim**: The primary `_DISPOSITION_PATTERN` should require balanced `\*\*` markers, with a permissive fallback as a separate second-pass regex (revision R-2). Cite: extraction-engineer revision R-2.
  - **Opposing position(s)**: Schema-engineer T-1 argues the current permissive pattern is the better default for LLM-generated markdown, because tightening the primary pattern would cause silent extraction failures on truncated output.
  - **Why I will not concede**: FR-002 requires extraction to "use structured parsing of conversus output format." The format is defined by the template, which prescribes `**Disposition**: Label`. A regex that also matches `**Disposition*: Label` is not matching the output format -- it is matching a corruption of it. The permissive fallback (separate regex, with logging) handles the resilience case without violating FR-002's correctness guarantee for well-formed output.
  - **Counter-argument to their position**: The permissive-only approach fails silently on a broader class of non-label text. A pattern that matches `\*?\*?` at the close can match partial bold markers in arbitrary markdown (e.g., `**This Disposition** is fine:\s*Surviving` in a narrative paragraph). The strict primary + permissive fallback pattern isolates the two concerns: correctness first, resilience second.
  - **Proposed resolution path**: Adopt two-pass parsing. Primary: strict `\*\*Disposition\*\*:\s*(Withdrawn|Modified|Surviving)`. Fallback (if zero matches): permissive `\*?\*?` variant with `logger.warning()`. The synthesizer should decide whether this two-pass approach is the adopted standard.

- **Dispute: AgentFeatures discriminated union staging — mode field now vs. later**
  - **My claim**: The discriminated union refactoring should be deferred entirely until the extraction pipeline is stable. Adding a `mode` field to AgentFeatures now (schema-engineer NR-1) is a half-measure that adds surface area without providing type discrimination. Cite: extraction-engineer DC-1 in cross-review of schema-engineer.
  - **Opposing position(s)**: Schema-engineer revision R-1 recommends adding `mode: str | None = None` as an interim step. Schema-engineer argues this enables consumers to filter relevant fields by mode.
  - **Why I will not concede**: A `mode` field on AgentFeatures is informational, not discriminatory. No Pydantic validator will use it to restrict which other fields are valid. A consumer that checks `if af.mode == "cooperative"` is doing runtime type checking that the type system should handle at construction time. The interim `mode` field trains consumers to code against a pattern that will be deprecated when per-mode subclasses arrive. Better to have no mode field than a mode field that does not discriminate.
  - **Counter-argument to their position**: The "stepping stone" argument assumes the discriminated union will be built on top of the `mode` field. But Pydantic discriminated unions use `Literal` types, not runtime `str` values. The stepping stone does not actually step toward the destination.
  - **Proposed resolution path**: Either refactor fully (per-mode subclasses) or defer entirely. No interim `mode` field. The synthesizer should choose based on the scope of this spec.

---

## Convergence

- **Converged: Position vector normalization to max recommendations**
  - **Shared position**: Position vectors must be padded to the maximum recommendation count across all agents in a round, so that all vectors have equal length.
  - **Agreeing agents**: extraction-engineer (R-1), spec-compliance (DC-1 cross-review), schema-engineer (DC-1 agrees fix location is extraction code)
  - **Strength**: Unanimous
  - **Path to convergence**: All three reviews independently identified this as a correctness issue. No disagreement at any phase.

- **Converged: Implement territory_claim_vector and confirmed_count extraction**
  - **Shared position**: Both fields are declared in the model and defined in the spec but not extracted. Extraction logic must be implemented.
  - **Agreeing agents**: extraction-engineer, schema-engineer (O-1, O-2, R-5), spec-compliance (R-4, R-5)
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1. No disagreement.

- **Converged: Amend FR-014/FR-016 package naming to match actual namespace**
  - **Shared position**: Amend the spec to use `conversus.schemas` import paths instead of `conversus_features`.
  - **Agreeing agents**: extraction-engineer (DC-2 cross-review), schema-engineer (DC-2 cross-review), spec-compliance (R-3)
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 2 cross-reviews. No one argues for creating a standalone package.

- **Converged: Add `plugins/` to non-agent directory exclusion list**
  - **Shared position**: Forward-compatibility with spec 016 requires excluding `plugins/` from directory iteration.
  - **Agreeing agents**: extraction-engineer (R-6), spec-compliance (T-1, NR-2)
  - **Strength**: Bilateral (schema-engineer does not address)
  - **Path to convergence**: Extraction-engineer proposed in Phase 1; spec-compliance endorsed in Phase 2.

- **Converged: Use JSON Schema instead of manual YAML for FR-005 compliance**
  - **Shared position**: Generate per-mode JSON Schema from Pydantic models at build time. Amend FR-005 to accept JSON Schema as the per-mode schema artifact.
  - **Agreeing agents**: schema-engineer (R-8 revised), spec-compliance (R-1 revised)
  - **Strength**: Bilateral (extraction-engineer does not address FR-005 directly)
  - **Path to convergence**: Schema-engineer proposed JSON Schema in Phase 1. Spec-compliance adopted it as a replacement for YAML schemas in Phase 3 revision.

---

## Final Position Statement

**Non-Negotiables**:
- Position vector normalization to max recommendations across agents (R-1). Without this, cooperative feature vectors are incomparable, which undermines the entire extraction pipeline's purpose.
- The two-pass disposition regex approach (R-2 revised). FR-002 compliance requires matching the prescribed format; FR-003 resilience requires handling corruptions. Two separate patterns satisfy both without compromise.

**Flexibility**:
- AgentFeatures refactoring approach. I prefer full deferral, but will accept the discriminated union if the scope is defined in this spec rather than left as "future work."
- CLI implementation timing (FR-012). I agree it is needed but am flexible on whether it is P1 or P2.
