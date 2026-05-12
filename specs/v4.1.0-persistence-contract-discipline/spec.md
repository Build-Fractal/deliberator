# Feature Specification: v4.1.0 Persistence Contract Discipline

**Feature ID:** `v4.1.0-persistence-contract-discipline`
**Created:** 2026-05-11
**Status:** Draft — pending originating deliberation.
**Depends On:** v4.0.0-tier-extraction (Tier 1 + Tier 2 hierarchy must exist); spec 067 (verification methodology); spec 070 (Constitutional Inclusion Criteria).
**Governed by:** `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/conversus-oss/CONSTITUTION.md` § Governance — Pathway Taxonomy (**MINOR** pathway; strengthens Tier 1 Principle II without removing or renaming any existing principle).
**Originating context:** None yet. Spec drafted from cross-product persistence audit 2026-05-11 surfacing: (a) the V remediation revealed conversus output parse contract lives in display text and silently short-circuits across 6 of 8 modes; (b) spec-kit-orc adapter (`scripts/dispatch/adapters/tool/conversus.sh`) hardcodes 3 brittle paths/grep patterns into conversus outputs; (c) spec-kit-orc's own `state-files.md` declared schemas have drifted from production JSONL data — 4 divergent in-tree schemas; (d) cross-product Python API (`linter.output_contract`) consumed without stability guarantee.

> **Scope discipline:** This spec amends Tier 1 Principle II (Stable Interfaces) by adding a Persistence Contract Discipline sub-clause. It does NOT remove or rename any existing principle. It does NOT prescribe a specific schema format (XSD, JSON Schema, Pydantic, AST validator) — products pick. It does NOT mandate XML for conversus outputs; the XML migration is a follow-on component-tier spec that conforms to this amendment. It DOES mandate mechanical enforcement of declared schemas — declaration without enforcement is itself a violation.

---

## 1. Summary

The build-fractal/ namespace today has two confirmed Principle II (Stable Interfaces) gaps:

1. **Implicit persistence contracts.** Conversus deliberation output uses mode-specific keyword markers (`**Dispute:`, `**Vulnerability:`, etc.) embedded in markdown display text — the linter parses by regex against these literals. Adding a 9th mode requires updating the parser. 6 of 8 modes currently short-circuit silently in the dispute parser (surfaced by PR #139, marked xfail).

2. **Declared-but-unenforced contracts.** spec-kit-orc has a written state-files contract (`specs/001-orchestrator/contracts/state-files.md`) declaring schemas for JSON, JSONL, and YAML-frontmatter artifacts. Production data has drifted: 4 logically distinct JSONL schemas exist in `.orchestrator/`, two declared-schema sources contradict each other on field names and version syntax, and the canonical contract does not match what scripts emit.

Both gaps fail the spirit of Principle II — "stable interfaces" cannot be stable if their stability is unenforced. The first gap couples conversus consumers to display text; the second gap couples spec-kit-orc consumers to a contract the producer no longer honors.

This amendment strengthens Principle II at Tier 1 with a **Persistence Contract Discipline** sub-clause mandating that every Build Fractal product MUST (a) declare a versioned schema for every stateful artifact, (b) mechanically enforce schema conformance in CI, (c) treat declared schema drift as a CI failure. Schema format is product-choice. Cross-product consumer contracts MUST be declared at the producer side; consumers MUST consume the declared contract, not implementation details.

The amendment is **MINOR** under the pathway taxonomy because it adds normative content to an existing principle without removing or renaming any. The cost of conformance is real (every product needs a state-files contract + CI gate) but proportionate to the stability gain.

## 2. Goals

1. Tier 1 Principle II gains a Persistence Contract Discipline sub-clause with operational definitions for "declared schema", "mechanical enforcement", "schema drift", and "cross-product consumer contract".
2. Conversus-oss adds a `CONSUMER-CONTRACT.md` at the repo root declaring its cross-product stability surface (output filenames, heading text used by external parsers, the `linter.output_contract` Python API surface).
3. Conversus-oss `CONFORMANCE.md` adds a new Provisional remediation row: implement structured XML output for deliberation phases (closes the V parser gap surfaced by PR #139; deadline 2026-09-01). This row is the bridge to the follow-on component-tier spec.
4. Conversus-enhanced `CONFORMANCE.md` gains the same Provisional remediation row for ITS persistence artifacts (per-solver run metadata, if any) — deadline 2026-09-01.
5. spec-kit-orc `CONFORMANCE.md` (created 2026-05-10) gains a new Provisional remediation row: reconcile `state-files.md` declared schemas with production JSONL data; add mechanical validator at `bin/validate-state.sh`; deadline 2026-09-01.
6. `build-fractal/README.md` gains a new section "Persistence Contract Discipline" linking to the Principle II extension and listing each product's CONSUMER-CONTRACT.md.

## 3. Non-goals

- **Does NOT mandate XML.** Product implementations choose XSD, JSON Schema, Pydantic, AST-validator, or any other mechanical schema language. The amendment mandates that SOME mechanical enforcement exists.
- **Does NOT migrate conversus outputs to XML in this spec.** That's a follow-on component-tier spec (`v4.1.1-conversus-structured-output` or similar) that conforms to this amendment.
- **Does NOT rewrite spec-kit-orc's `state-files.md` in this spec.** Spec-kit-orc's reconciliation is its own follow-on under the Provisional remediation goal #5.
- **Does NOT introduce a new principle.** This is an extension of existing Principle II (Stable Interfaces), not a new principle slot. No retired-principle reuse, no renumbering.
- **Does NOT apply retroactively to existing Implicit-Provisional or Compliant-Provisional repos in punitive terms.** Existing products gain Provisional remediation rows on a 2026-09-01 timeline. New product admissions after ratification MUST include a CONSUMER-CONTRACT.md (or equivalent) and CI gate at admission time.
- **Does NOT govern transient state.** In-memory state, temp files outside `.conversus/`/`.orchestrator/`, and ephemeral session artifacts are out of scope. The principle governs persistent on-disk state intended to outlive the writing process.

## 4. Principle Amendment — text being added

The following sub-clause is appended to Principle II in `build-fractal/CONSTITUTION.md`. Existing Principle II text is preserved verbatim; this sub-clause sits below the existing bullet list as a new "Persistence Contract Discipline" subsection.

```markdown
#### Persistence Contract Discipline (added v4.1.0)

Persistent on-disk state is itself a stable interface. Every stateful
artifact a Build Fractal product writes to disk MUST satisfy:

1. **Declared schema.** The artifact has a written schema declaration
   in a discoverable location (typically `STATE-FILES.md`,
   `CONSUMER-CONTRACT.md`, or an equivalent canonical doc at the repo
   root). The schema specifies field names, types, structural
   requirements, and a `schema_version` field.

2. **Mechanical enforcement.** A CI gate validates that artifacts
   written during a run conform to the declared schema. Schema format
   is product-choice — XSD, JSON Schema, Pydantic model, AST validator,
   or any other format with a deterministic conformance check. Schemas
   declared without enforcement do not satisfy this discipline.

3. **Versioning.** The schema carries a `schema_version` field with a
   documented bump procedure. Schema evolution MUST update the version;
   silent format changes are a violation.

4. **Cross-product consumer contracts.** When a Build Fractal product
   B consumes artifacts written by Build Fractal product A, product A
   MUST publish a `CONSUMER-CONTRACT.md` (or equivalent) at its repo
   root declaring which output surfaces are stable. Product B MUST
   consume the declared surface, not implementation details (heading
   text, hardcoded paths, English error strings). Changes to declared
   surfaces require a version bump and consumer-coordinated migration;
   changes to undeclared internals are free.

5. **Declaration scope.** Display text inside an artifact is NOT a
   stable contract unless explicitly declared as such. Parsing display
   text for semantic content is forbidden when a structural surface
   exists; if no structural surface exists, declaring display text as
   the contract is permitted but creates a debt the product MUST
   close.

The principle scope is persistent on-disk state intended to outlive
the writing process. Transient state (in-memory, ephemeral temp files
outside declared state directories) is out of scope.

*Origin: cross-product persistence audit 2026-05-11. Conversus
deliberation outputs short-circuited silently in 6 of 8 modes because
the parse contract lived in display text. spec-kit-orc's declared
state-files contract drifted from production JSONL data, with 4
divergent in-tree schemas and contradictory schema_version syntax in
the canonical documentation itself.*
```

## 5. Verbatim preservation contract

Existing Tier 1 Principle II body text MUST be preserved byte-for-byte. The sub-clause above is APPENDED below the existing content, not interleaved or substituted.

Existing Tier 2 principles are NOT amended by this spec. Existing component-tier principles in conversus-oss, conversus-enhanced, and spec-kit-orc are NOT amended.

Sync Impact Report comment blocks accumulated across v0.1.0 → v4.0.0 in conversus-oss `CONSTITUTION.md` are preserved unchanged. v4.1.0 adds a new SIR block per existing convention.

## 6. File edits

### 6.1 Tier 1 — `build-fractal/CONSTITUTION.md`

- Append `#### Persistence Contract Discipline` sub-clause to § Principle II (text above, byte-for-byte).
- Update version footer: `**Version**: 1.0.0` → `**Version**: 1.1.0` (MINOR bump).
- Add v4.1.0 SIR comment block at top of file (after the v4.0.0 SIR) using the existing convention.
- Optional: update the principles table-of-contents if one is rendered separately.

### 6.2 conversus-oss — `build-fractal/conversus/conversus-oss/`

**New files:**
- `CONSUMER-CONTRACT.md` — declares the cross-product stability surface for consumers (spec-kit-orc adapter is the primary consumer today). Must enumerate:
  - Output filename contracts: `summary/final.md`, `arbitration/resolution.md`, `{agent}/disputes.md`, etc. — which are stable, which are derived.
  - Output structural surfaces: `## Verdict` heading in arbitration is the current de-facto parse target; declare it stable OR mark it deprecated pending the XML migration follow-on.
  - Python API surface: `linter.output_contract` is currently consumed by spec-kit-orc's adapter via `python -m linter.output_contract`. Declare which functions/return values are stable.
  - Provider-error message strings: spec-kit-orc's `KNOWN_PROVIDER_ERROR_PATTERNS` greps English literals — declare these strings stable or move them into a structured error code.
  - Schema-bump procedure: pointer to `CHANGELOG.md` + a documented version-bump policy.
- `schema/output-contract.md` — placeholder for the follow-on component-tier spec's XSD/JSON-Schema definition. May be empty in v4.1.0 (the follow-on creates the actual schema); existing during this amendment to satisfy the "declared schema" mandate for the deliberation-output artifact.

**Edits:**
- `CONFORMANCE.md` Tier 1 row II: status update with evidence note (`CONSUMER-CONTRACT.md` present; structured-output schema follow-on tracked).
- `CONFORMANCE.md` Provisional remediation plan: ADD a new row for "deliberation-output structured schema" with deadline 2026-09-01 and tracking pointer to the follow-on spec.

### 6.3 conversus-enhanced — `build-fractal/conversus/conversus-enhanced/`

**New files:**
- `CONSUMER-CONTRACT.md` — declares stability surface for downstream consumers (mostly: solver outputs, configuration manifests).

**Edits:**
- `CONFORMANCE.md` Tier 1 row II: same status update + evidence note.
- `CONFORMANCE.md` Provisional remediation plan: ADD row if any stateful artifacts exist that need schema declaration; if no stateful artifacts beyond what's already covered by upstream conversus-oss, mark this row N/A with rationale.

### 6.4 spec-kit-orc — `build-fractal/spec-kit-orc/`

**Edits:**
- `CONFORMANCE.md` Tier 1 row II (currently Provisional from the 2026-05-10 initial declaration): update with evidence note + the new amendment scope.
- `CONFORMANCE.md` Provisional remediation plan: ADD a row for "reconcile state-files.md declared schemas with production JSONL data; add `bin/validate-state.sh`" with deadline 2026-09-01.
- Existing `specs/001-orchestrator/contracts/state-files.md` is referenced by this amendment as a positive example (declared contract exists) but flagged as needing mechanical enforcement to satisfy the new sub-clause.

### 6.5 build-fractal/ — `build-fractal/README.md`

- Add a new section "Persistence Contract Discipline" linking to:
  - Tier 1 Principle II sub-clause (the canonical statement)
  - Each suite/product's CONSUMER-CONTRACT.md
  - The amendment spec (this document, by URL)

### 6.6 CONSTITUTIONAL_CONVERSATIONS.md entries

- `build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md`: log v4.1.0 amendment per existing convention (originating + verifications + ratification entries; spans rows as deliberation produces them).
- Component-tier `conversus-oss/CONSTITUTIONAL_CONVERSATIONS.md`: log the conversus-oss specific impact (new CONSUMER-CONTRACT.md, new Provisional row).
- Component-tier `conversus-enhanced/CONSTITUTIONAL_CONVERSATIONS.md` (if one exists; if not, create per Principle II convention): log impact.
- spec-kit-orc currently has no CONSTITUTIONAL_CONVERSATIONS.md (component constitution not yet declared). Optional: create one as part of this spec; or defer to spec-kit-orc's own follow-on remediation work.

## 7. Cross-product implications

| Product | Today | Post-v4.1.0 (declaration) | Post-remediation (2026-09-01) |
|---|---|---|---|
| conversus-oss | Output parse contract in display text; no CONSUMER-CONTRACT.md; V parser short-circuits on 6/8 modes | CONSUMER-CONTRACT.md declares current surfaces; new Provisional row tracks structured-output migration | Structured XML output (or equivalent) ships; XSD CI gate active; V's 6 xfail tests un-xfail |
| conversus-enhanced | No documented cross-product consumer surface | CONSUMER-CONTRACT.md declares surface (or asserts N/A with rationale) | If applicable: schema enforcement on whatever stateful artifacts the paid layer writes |
| spec-kit-orc | state-files.md exists but drifted from production data; consumer of conversus implementation details (hardcoded paths, awk-grep on `## Verdict`, KNOWN_PROVIDER_ERROR_PATTERNS) | New Provisional row tracks: (a) reconcile state-files.md with production data, (b) add mechanical validator, (c) rewrite Conversus adapter against conversus's CONSUMER-CONTRACT.md | Both gaps closed: spec-kit-orc validates its own state; Conversus adapter consumes only declared surfaces |
| Future products | No discipline | Admission requires CONSUMER-CONTRACT.md + CI gate at admission time | (same — admission gate enforces discipline going forward) |

## 8. Constitutional Inclusion Criteria gate

Per spec 070, the three Inclusion Criteria for principle additions/extensions are:

1. **Universal applicability** — does it apply to all Build Fractal products?
2. **Mechanical verifiability** — can conformance be checked deterministically?
3. **Non-redundant** — does it cover something not already addressed by an existing principle?

This amendment passes:

1. **Universal**: persistent on-disk state is a feature of every Build Fractal product. ✅
2. **Mechanical**: the discipline literally MANDATES mechanical enforcement; conformance is a CI gate. ✅
3. **Non-redundant**: existing Principle II treats "stable interfaces" abstractly. The sub-clause is the operational definition for the persistence interface specifically; no other principle covers this. ✅

## 9. Verification protocol

Per spec 067, principle amendments require **originating + self-consistency + blind** deliberations. The pathway taxonomy permits MINOR amendments with all three (the same protocol as MAJOR, distinguished only by what changes — MINOR adds normative content without removing or renaming).

### 9.1 Originating deliberation

- Config: `deliberations/v4.1.0-persistence-contract-discipline-originating-2026-MM-DD/conversus.yml`
- Mode: cooperative (or red-blue if a P1-priority dispute is expected)
- Agents: at minimum a pragmatist, a devil's advocate, and a domain-grounded persistence/CI expert. Mechanist + architect roles complete the spread.
- Arbiter: balanced-arbiter or constitutional-arbiter, grounded in Tier 1 CONSTITUTION.md + this spec.
- Target files: `spec.md` (this file), Tier 1 Principle II current text, spec-kit-orc's `state-files.md`, the cross-product audit report from 2026-05-11.
- Expected questions: (Q1) Does Persistence Contract Discipline meet Inclusion Criteria? (Q2) Is the schema-format flexibility (product-choice) appropriate, or should the amendment mandate a specific format? (Q3) Is the 2026-09-01 remediation deadline reasonable for affected products?

### 9.2 Self-consistency verification

- Re-deliberate with a different agent composition and the SAME spec text.
- Expected output: PASS, PASS-WITH-FIXES (small remediations), or BLOCK.
- Apply fixes (if any) to produce spec v2.

### 9.3 Blind verification

- Strip candidate version/date markers from spec v2 using the existing `scripts/strip-constitution-for-blind.py` pattern (applied to this spec rather than CONSTITUTION.md — adapt as needed).
- Run blind deliberation with agents not exposed to the originating verdict.
- Expected output: PASS, PASS-WITH-FIXES, or BLOCK.
- Apply fixes (if any) to produce spec v3.

### 9.4 Ratification

- All three deliberations passing (with applied fixes) → flip status to `Status: Ratified` + apply file edits per § 6.
- Update SIR blocks, version footer, CONSTITUTIONAL_CONVERSATIONS.md entries.

## 10. Conditions from originating

Placeholders to be filled during deliberation. Expected condition shapes:

- **C1**: Confirm the schema-format flexibility clause does not create a loophole (e.g., a product declaring "schema: this paragraph" trivially conforms).
- **C2**: Confirm the cross-product consumer-contract requirement is enforceable for the conversus-oss ↔ spec-kit-orc surface specifically (the only known live integration today).
- **C3**: Confirm the 2026-09-01 remediation deadlines are operationally feasible (conversus structured-output migration is non-trivial).

(Conditions to be revised based on actual originating deliberation rulings.)

## 11. Implementation order

Once ratified:

1. **Tier 1 edit** (§ 6.1) — append sub-clause to `build-fractal/CONSTITUTION.md`, bump version, add SIR.
2. **build-fractal/README.md** (§ 6.5) — add Persistence Contract Discipline section.
3. **Per-product CONSUMER-CONTRACT.md drafts** (§§ 6.2, 6.3) — create placeholder files; declare current surfaces; flag follow-on remediation rows.
4. **CONFORMANCE.md updates** (§§ 6.2, 6.3, 6.4) — add Provisional remediation rows on each affected product with 2026-09-01 deadlines.
5. **CONSTITUTIONAL_CONVERSATIONS.md log entries** (§ 6.6).
6. **Follow-on spec drafts** — `v4.1.1-conversus-structured-output` and `v4.1.2-spec-kit-orc-state-files-reconciliation` open as separate specs implementing the Provisional rows. Each is its own component-tier amendment cycle.

## 12. SIR preview

```markdown
<!--
Sync Impact Report
Version change: 1.0.0 → 1.1.0 (MINOR — Persistence Contract Discipline sub-clause added to Tier 1 Principle II).
Governance log entry: 2026-MM-DD in build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md.
Originating deliberation: deliberations/v4.1.0-persistence-contract-discipline-originating-2026-MM-DD/.
Self-consistency verification: deliberations/v4.1.0-persistence-contract-discipline-self-consistency-2026-MM-DD/.
Blind verification: deliberations/v4.1.0-persistence-contract-discipline-blind-2026-MM-DD/.
Inclusion Criteria gate: PASS (universal applicability + mechanical verifiability + non-redundant).
Pathway: MINOR (text appended to existing Principle II; no principle removed or renamed).
Per-product impact: new CONSUMER-CONTRACT.md at each suite repo root; new Provisional remediation rows in conversus-oss / conversus-enhanced / spec-kit-orc CONFORMANCE.md with 2026-09-01 deadlines; follow-on component-tier specs for structured-output (conversus-oss) and state-files reconciliation (spec-kit-orc).
Prior amendment (v4.0.0): tier extraction — see prior SIR block below.
-->
```

## 13. Status & next steps

- **Status:** Draft — pending originating deliberation.
- **Next step:** stage originating deliberation config under `deliberations/v4.1.0-persistence-contract-discipline-originating-2026-MM-DD/`. Recommend bundling the cross-product audit report from 2026-05-11 as a target file alongside this spec.
- **Sequencing recommendation:** do NOT run deliberation until Batch 1 (V/XXVI/XXIV) and Batch 2 (XXII × 2) PRs are merged. The empirical evidence from those merges informs the amendment — specifically, the V remediation's xfail discovery is the primary motivating example, and locking that empirical observation in before deliberating makes the spec stronger.

## 14. Fix ledger

(Empty at draft. Populated during deliberation cycles per spec 067 convention: v1 → v2 (self-consistency fixes) → v3 (blind fixes) → vN (errata).)
