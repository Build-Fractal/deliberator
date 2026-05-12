# Deliberation Output Schema — Placeholder

**Status:** DRAFT placeholder — pending v4.1.0 amendment ratification AND the follow-on `v4.1.1-conversus-structured-output` component-tier spec.

**Purpose:** This file exists to satisfy the "declared schema" mandate of the Persistence Contract Discipline sub-clause (Tier 1 Principle II, added v4.1.0) for the deliberation-output artifact family. The actual structured-output XSD or JSON Schema is forthcoming.

## Scope

Deliberation outputs (the per-run artifact tree under `conversus_output_dir`, enumerated in `CONSUMER-CONTRACT.md` § 1) currently render as markdown. The cross-product parse contract that consumers (notably spec-kit-orc's dispatch adapter) depend on lives in display text — specifically the `## Verdict` heading inside `arbitration/resolution.md`. This is a Principle II § 5 (Declaration scope) gap: parsing display text where a structural surface should exist.

The follow-on `v4.1.1-conversus-structured-output` spec will:

1. Define a versioned XSD or JSON Schema for deliberation outputs (mode-specific dispute markers, arbitration verdicts, per-agent cross-reviews, synthesis outcomes).
2. Have the engine emit structured payloads alongside (or embedded in) the existing markdown renderings.
3. Add a CI gate that validates every artifact written during a run against the schema.
4. Wire `linter.output_contract.validate_output()` to consume the structured surface instead of regex-against-display-text.

## Why this file exists now

Per the Persistence Contract Discipline sub-clause:

> **Declared schema.** The artifact has a written schema declaration in a discoverable location (typically `STATE-FILES.md`, `CONSUMER-CONTRACT.md`, or an equivalent canonical doc at the repo root).

This placeholder is the discoverable location. The CONFORMANCE.md Provisional remediation row (deadline 2026-09-01) tracks the work to populate it with a real, mechanically-enforced schema. Until v4.1.0 ratifies, this file is advisory; once it ratifies, the empty-placeholder state is a documented debt with a closure deadline rather than a passive omission.

## Forward-looking shape (non-normative sketch)

The eventual schema is expected to cover at minimum:

- `schema_version` — semver-shaped string with documented bump procedure.
- Per-mode dispute markers (today encoded as `**Dispute:`, `**Vulnerability:`, etc. in display text — 8 modes total).
- Arbitration verdict structure (today encoded as the `## Verdict` heading + free-text paragraph).
- Per-agent cross-review structure (today: free-form markdown).
- Synthesis outcome (today: free-form markdown under `summary/final.md`).

Format choice (XSD, JSON Schema, Pydantic models, hybrid) is deferred to the follow-on spec. The Persistence Contract Discipline sub-clause is format-agnostic — it mandates declared + mechanically enforced + versioned, not any specific schema language.

## See also

- `CONSUMER-CONTRACT.md` — the consumer-facing surface declaration this schema supports.
- `CONFORMANCE.md` Provisional remediation plan — tracks the 2026-09-01 deadline.
- `specs/v4.1.0-persistence-contract-discipline/spec.md` — the amendment introducing the sub-clause.
