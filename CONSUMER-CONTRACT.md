# conversus-oss — Consumer Contract

**Status:** DRAFT — pending v4.1.0 amendment ratification. This contract becomes binding once v4.1.0 (Persistence Contract Discipline) lands.

**Purpose:** Declare the cross-product stability surface that downstream Build Fractal products may consume. Anything declared stable here is governed by Tier 1 Principle II (Stable Interfaces) and may not change without a version bump and consumer-coordinated migration. Anything NOT declared here is an implementation detail; consumers depend on it at their own risk and a breakage is not a contract violation.

**Inherits from:**
- Tier 1 — `build-fractal/CONSTITUTION.md` § Principle II (Stable Interfaces) + Persistence Contract Discipline sub-clause (added v4.1.0).
- Tier 2 — `build-fractal/conversus/CONSTITUTION.md` § Principle V (Observable Deliberation).

**Known consumers (today):**
- `build-fractal/spec-kit-orc/scripts/dispatch/adapters/tool/conversus.sh` — the orchestrator's Conversus dispatch adapter. Consumes output filenames, the `## Verdict` heading in arbitration, the `linter.output_contract` Python module, and English provider-error literals.

---

## 1. Output filename contracts

Conversus deliberation runs write artifacts under a per-run output directory (`conversus_output_dir`). The following relative paths are declared:

| Path | Status | Notes |
|---|---|---|
| `summary/final.md` | **Stable** | Final synthesis produced by the synthesis phase. Consumers may read this file path verbatim. |
| `arbitration/resolution.md` | **Stable** | Arbiter resolution document produced when arbitration runs. Presence indicates an arbitration phase fired. |
| `{agent}/disputes.md` | **Stable** | Per-agent dispute artifact. `{agent}` is the agent slug declared in `conversus.yml`. |
| `{agent}/revision.md` | **Stable** | Per-agent revision artifact (cooperative-mode iteration output). |
| `{agent}/cross-reviews/{other-agent}.md` | **Stable** | Per-agent cross-review of another agent's output. |
| `summary/`, `arbitration/`, `{agent}/` directories | **Stable** | Directory layout is part of the contract; consumers may walk these. |
| Any path containing `_internal`, `_tmp`, `_debug`, or under `_engine/` | **Derived / internal** | Not stable; do not consume. |
| Any path not enumerated above | **Derived / internal** | Treat as unstable until explicitly listed here. |

**De-facto-stable-pending-XML-migration note:** All of the above paths currently render in markdown. The structural surfaces inside those files (headings, list items, paragraph order) are NOT part of the filename contract — see § 2 for the structural-surface declarations. Once the follow-on `v4.1.1-conversus-structured-output` spec lands, these files will additionally carry XML payloads; the filenames stay stable across that migration.

## 2. Output structural surfaces

Some downstream consumers parse content inside the declared files. The following in-file surfaces are declared:

| Surface | File | Status | Notes |
|---|---|---|---|
| `## Verdict` heading | `arbitration/resolution.md` | **Stable in current markdown rendering; deprecated after v4.1.1 structured-output migration.** | spec-kit-orc's adapter (`scripts/dispatch/adapters/tool/conversus.sh:732-743`) extracts the paragraph(s) following `## Verdict` via awk. Consumers may rely on this heading until v4.1.1 ships an XML schema replacement; once XML lands, the markdown heading remains for human readers but consumers SHOULD migrate to the structured path. Removal of the markdown heading requires a MAJOR bump and consumer-coordinated migration. |
| `conversus_output_dir:` frontmatter line | gate-result.md (consumer-written) | **De-facto-stable** | Convention used by spec-kit-orc to locate per-agent artifacts. Documented here as the canonical pointer back to the run output root. |
| Any other heading, bullet, table inside declared files | (all) | **NOT a stable contract.** | Display text. Parsing display text for semantic content is forbidden by Principle II § 5 (Declaration scope) when a structural surface exists; if no structural surface exists, consumers MAY parse display text but the producer carries a documented debt to close that gap. |

**Debt entry (closes with v4.1.1):** Today, `## Verdict` is the only structural surface consumers parse inside artifact bodies. Migrating to a declared XML/JSON-Schema structured output is tracked as a Provisional remediation in `CONFORMANCE.md` (Persistence Contract Discipline row) with deadline 2026-09-01.

## 3. Python API surface

The following `linter.*` module surface is declared for downstream Python consumers:

| Module / Symbol | Status | Consumer Notes |
|---|---|---|
| `linter.output_contract` (module exists) | **Stable** | Module path is stable. |
| `linter.output_contract.validate_output(path: str | Path) -> ValidationResult` | **Stable** | Function name + signature. `path` accepts a string or `pathlib.Path`. Returns a `ValidationResult` (see below). May raise `FileNotFoundError` if path doesn't exist. |
| `ValidationResult.ok: bool` | **Stable** | `True` if the output conformed to its mode contract. |
| `ValidationResult.errors: list[str]` | **Stable** | Empty on success; each entry is a human-readable error string suitable for surfacing to operators. |
| Any `linter.output_contract.*` symbol not enumerated above | **Internal.** | May change without notice; do not import directly. |
| `linter.dead_infra`, `linter.tier_coherence`, `linter.spec_parity`, `linter.validate` | **Internal CI helpers, not consumer-facing.** | These ship as part of the repo's own CI machinery. Consumers MUST NOT depend on them; semantics may shift to satisfy this repo's CONFORMANCE.md needs. |
| Direct entry: `python -m linter.output_contract <path>` | **Stable CLI surface** | spec-kit-orc's adapter invokes this form. Exit code 0 = ok; non-zero = validation failure. Stderr carries human-readable error text. |

## 4. Provider-error message strings

spec-kit-orc's adapter (`KNOWN_PROVIDER_ERROR_PATTERNS`, `conversus.sh:217`) greps deliberation outputs for English literals that indicate a provider produced stub content rather than a real response. The following strings are declared:

| String | Status | Notes |
|---|---|---|
| `"There's an issue with the selected model"` | **De-facto-stable; DEBT.** | Emitted by `claude-code` provider when an unreachable model ID is requested. Consumers grep for this literal to fail-closed against stub-PASS outputs. Changing this string requires a coordinated update across consumers. |

**Debt entry:** Grepping English literals is a Principle II § 5 violation in spirit (parsing display text where a structural surface should exist). The right shape is a structured error code emitted alongside any provider stub. This is logged as a follow-on item — see CONFORMANCE.md (Persistence Contract Discipline row). Removal of this literal without a structured replacement requires consumer-coordinated migration.

## 5. Schema-bump procedure

Changes to declared surfaces in this document follow the standard pathway taxonomy documented in `CONSTITUTION.md` § Governance:

- **PATCH** (bug-fix, no surface change): no CONSUMER-CONTRACT.md update needed; document via CHANGELOG.md.
- **MINOR** (additive — new declared surface, new optional field): update CONSUMER-CONTRACT.md to enumerate the new surface; CHANGELOG.md entry; no consumer migration required.
- **MAJOR** (breaking — declared surface removed, renamed, or semantically changed): requires a constitutional amendment under the pathway taxonomy + consumer-coordinated migration plan + deprecation window. CHANGELOG.md entry calls out the break loudly.

The structured-output schema referenced in § 2 is tracked in `schema/output-contract.md` (currently a placeholder; populated by the follow-on `v4.1.1-conversus-structured-output` spec).

## 6. Status & next steps

- **Status:** DRAFT, staged on `spec/v4.1.0-impl-staging` ahead of amendment ratification. Not yet binding.
- **Becomes binding when:** v4.1.0 amendment passes originating + self-consistency + blind verifications and merges to main.
- **Next surface to declare:** the structured-output XSD/JSON-Schema (follow-on `v4.1.1-conversus-structured-output`), at which point § 2's `## Verdict` deprecation timer starts.
