# Feature Specification: v4.1.0 Persistence Contract Discipline

**Feature ID:** `v4.1.0-persistence-contract-discipline`
**Created:** 2026-05-11
**Status:** v5 / post-blind / ratification-ready (2026-05-12).
**Depends On:** v4.0.0-tier-extraction (Tier 1 + Tier 2 hierarchy must exist); spec 067 (verification methodology); spec 070 (Constitutional Inclusion Criteria).
**Governed by:** `https://github.com/clariti-care/payer-index-mono/blob/main/build-fractal/conversus/GOVERNANCE.md` § Pathway Taxonomy (**MINOR** pathway at Tier 2 — strengthens the suite constitution without removing or renaming any existing principle).
**Originating context:** Originating deliberation 2026-05-12, ruling at `deliberations/v4.1.0-persistence-contract-discipline-originating-2026-05-11/arbitration/resolution.md` (commit `026b417`). Cross-product persistence audit 2026-05-11 surfaced: (a) the V remediation revealed conversus output parse contract lives in display text and silently short-circuits across 6 of 8 modes; (b) spec-kit-orc adapter (`scripts/dispatch/adapters/tool/conversus.sh`) hardcodes 3 brittle paths/grep patterns into conversus outputs; (c) spec-kit-orc's own `state-files.md` declared schemas have drifted from production JSONL data — 4 divergent in-tree schemas; (d) cross-product Python API (`linter.output_contract`) consumed without stability guarantee.
**Self-consistency verification:** Initial self-consistency arbitration 2026-05-12 at `deliberations/v4.1.0-persistence-contract-discipline-self-consistency-2026-05-12/arbitration/resolution.md` (commit `8f90e2d`). Ruled **Q1 PASS-WITH-CLARIFICATIONS / Q2 DEMOTE-TO-TIER-2 / Q3 FAIL-OVERSTRETCH**. Seven required changes produced v3. Self-consistency re-run on v3 arbitration 2026-05-12 at `deliberations/v4.1.0-persistence-contract-discipline-self-consistency-rerun-2026-05-12/arbitration/resolution.md` (commit `a17d13a`). Ruled **Q1 PASS-WITH-CLARIFICATIONS / Q2 PASS / Q3 PASS-WITH-EDITS**. Four D-conditions (D1-D4) produced v4.
**Blind verification:** Blind arbitration 2026-05-12 at `deliberations/v4.1.0-persistence-contract-discipline-blind-2026-05-12/arbitration/resolution.md`. Ruled **Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS / Q2 MODERATE-RISK-MANAGEABLE / Q3 PARTIALLY-COHERENT**. Four E-conditions (E1-E4) produced this v5. Combined disposition: **PROCEED TO RATIFICATION**.

## Changelog from v4 (blind-verification E-conditions, 2026-05-12)

The blind verification (stage 3 of 3) returned **Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS / Q2 MODERATE-RISK-MANAGEABLE / Q3 PARTIALLY-COHERENT** — combined disposition **PROCEED TO RATIFICATION** with four E-conditions (E1-E4) applied to produce this v5 (the ratification-ready version). The blind verification arbitration recorded unanimous agent convergence on three wording-level Q1 gaps (E1-E3) plus one Q3 doctrinal-framing tightening (E4); the substantive content of the principle is preserved unchanged.

- **E1 — § 4 sub-clause 3 `schema_version` format mandate.** Per the blind arbitration's Q1 ruling (unanimous agent convergence): the `schema_version` field MUST use semantic versioning (MAJOR.MINOR.PATCH) by default, OR a documented alternative with explicit total-ordering semantics. Products choosing an alternative MUST document the format and its ordering semantics in their `CONSUMER-CONTRACT.md`. *(Applied: § 4 sub-clause 3.)*
- **E2 — § 4 sub-clause 5 declaration mechanism.** Per the blind arbitration's Q1 ruling (unanimous agent convergence — the load-bearing implementability fix): explicit declaration of a display-text surface as a stable contract MUST appear in the producer's `CONSUMER-CONTRACT.md` (or equivalent declared canonical doc), naming the specific display-text surface (heading text, error string, marker) and stating the stability guarantee (e.g., "MAJOR `schema_version` bump required to change"). Spec v4 said display text was not stable by default unless explicitly declared, but did not specify HOW to declare — E2 closes this gap. *(Applied: § 4 sub-clause 5.)*
- **E3 — § 4 sub-clause 1 "discoverable location" criteria.** Per the blind arbitration's Q1 ruling (unanimous agent convergence): a schema-declaration location is "discoverable" if it (a) lives at the producer repo root (or under a suite-convention directory documented in that repo's `CONFORMANCE.md`), (b) follows the suite naming convention (`STATE-FILES.md`, `CONSUMER-CONTRACT.md`, `CONFORMANCE.md`, `schemas/`, or an equivalent declared in the repo's `CONFORMANCE.md`), AND (c) is linked from both the repo's top-level `README.md` AND its `CLAUDE.md` (or the equivalent agent entry-point doc). *(Applied: § 4 sub-clause 1.)*
- **E4 — § 4 preamble unifying statement.** Per the blind arbitration's Q3 ruling (doctrinal-framing tightening): a single-sentence preamble is added at the start of § 4 making the principle's doctrinal frame explicit — "Persistence contracts ARE stable interfaces. This principle elaborates the Tier 1 Principle II stable-interface doctrine specifically for persistent on-disk state — the same doctrinal frame, applied to a different surface category." This integrates the principle into the broader constitutional architecture rather than letting it stand as a separate concern. *(Applied: § 4 preamble.)*

The four E-conditions are wording-level fixes per the blind arbitration; no sub-clause is removed, renamed, or substantively re-scoped. The principle's normative content (declared schema → mechanical enforcement → versioning → cross-product consumer contracts → declaration scope) and its conditions (C1-C8, D1-D4) survive unchanged into v5.

## Changelog from v3 (self-consistency-rerun D-conditions, 2026-05-12)

The self-consistency re-run on v3 (arbitration commit `a17d13a`) returned **Q1 PASS-WITH-CLARIFICATIONS / Q2 PASS / Q3 PASS-WITH-EDITS** — combined disposition PROCEED TO BLIND VERIFICATION with four D-conditions applied to produce this v4:

- **D1 — Q1/Q2 sequencing in verification methodology.** Per the rerun arbitration's ruling on "Evidence Base Verification Priority Classification" (strict-reader adopted, High confidence): within each verification stage (originating, self-consistency, blind), Q1 constitutional coherence assessment MUST complete before Q2 evidence base adequacy analysis. Q1 (internal contradictions with existing principles) is structurally independent of Q2 (tier-placement evidence adequacy). *(Applied: § 9 verification protocol; § 13 methodological lessons.)*
- **D2 — Temporal scope of universal deadline.** Per the rerun arbitration's ruling on "Universal Deadline Temporal Framework" (tier-coherence-auditor adopted, High confidence): the universal 2026-12-01 deadline applies to **products existing at ratification**. Future siblings joining the conversus suite after ratification are governed by their admission process — they receive admission-time deadlines, not retroactive inheritance of this date. Temporal scope preservation avoids the logical impossibility of retroactive obligations on non-existent products (Principle VII constraint). *(Applied: § 2 goals 3-5 + universal-deadline rationale paragraph; § 3 non-goals; § 7 cross-product implications table; § 10.2 C7.)*
- **D3 — Constitutional adequacy precedes enforcement design.** Per the rerun arbitration's ruling on "Constitutional-Enforcement Coordination Priority" (precedent-auditor adopted, Medium confidence): ratification-blocking issues (constitutional contradictions, tier-evidence mismatches, precedent-scope violations) MUST be evaluated before enforcement-mechanism design issues (CI gate placement, fixture requirements, deadlines). The latter are post-ratification operational enhancements; the former are ratification-blocking. Companion to D1. *(Applied: § 9 verification protocol; § 13 methodological lessons.)*
- **D4 — § 11 procedural boundary language.** Per the rerun arbitration's ruling on "Agent Convergence vs Procedural Override Authority Boundaries" (precedent-auditor adopted, High confidence): § 11 (override-with-rationale scope restriction) is extended with explicit language clarifying that **agent convergence on substance cannot cure procedural violations**, but substantive outcomes MAY be preserved when procedures are corrected through proper channels. The v2-Q2 originating-stage override invocation is the worked example: the procedural invocation was rolled back in v3, and the substantive Q2 disposition (format-choice preserved) survived intact by being re-grounded on independent agent-convergence rather than via the invalid override. *(Applied: § 11.)*

## Changelog from v2 (self-consistency fixes, 2026-05-12)

The self-consistency arbitration (commit `8f90e2d`) demoted v2's Tier 1 placement and failed v2's deadline differentiation + override-precedent reuse. v3 applies the seven required changes from that ruling's "Summary of Changes Required":

- **C-SC-1 (P1) — Tier demotion to Tier 2.** Amendment retargeted from `build-fractal/CONSTITUTION.md` (Tier 1 Universal) to `build-fractal/conversus/CONSTITUTION.md` (Tier 2 Suite). Evidence base — conversus-oss output parse contract, conversus-enhanced consumer surfaces, spec-kit-orc adapter — is limited to the conversus product family and does not meet Tier 1's multi-product-family requirement (Tier 1 Authority L44-46). The discipline lands as a **new Tier 2 principle "XXVIII. Persistence Contract Discipline"**, appended after XXVII (Operator-Configurable Tool Surface). The spec branch name `spec/v4.1.0-persistence-contract-discipline` is preserved: Tier 2's current version is 1.0.0 (post-v4.0.0 tier extraction), and a MINOR amendment yields Tier 2 v1.1.0 — the same human-readable identifier `v4.1.0` continues to name this amendment cycle.
- **C-SC-2 (P1) — Removed differentiated deadlines.** Per the arbitration ruling on "Differentiated deadlines constitutional status" (High confidence): "Constitutional violations should be absolute, not contextual. Universal principles, by definition, cannot grant product-specific accommodations." This applies at Tier 2 as much as at Tier 1 — a principle whose scope is "every conversus-family repo" cannot grant per-repo deadline relief without violating its own universality. v3 replaces v2's C7 differentiated dates (2026-12-01 for conversus-oss + conversus-enhanced, 2026-09-01 for spec-kit-orc) with a **single universal deadline of 2026-12-01 applicable to all suite products** subject to the principle. Products MAY self-declare earlier ready dates as opt-in; the principle's normative deadline is uniform.
- **C-SC-3 (P1) — Override-with-rationale scope restriction.** The override-with-rationale precedent (`feedback_amendment_override_precedent.md` and prior amendments) is hereby restricted to **blind-verification verdicts only**. Extension to originating-stage arbitrations (as v2's originating ruling invoked) is procedurally invalid. Any future scope extension requires its own explicit constitutional amendment going through originating + self-consistency + blind verification stages. See § 11 "Override-with-rationale scope restriction" below.
- **C-SC-4 (P1) — Compound constitutional debt acknowledged.** The tier-placement attempt (evidence/scope mismatch) and the override-precedent stretch are recognized as unified governance discipline gaps stemming from ratification bias at the originating stage. Both are addressed in this v3 (substantively, by tier demotion + universal deadline; procedurally, by precedent rollback). See § 12 "Compound constitutional debt" below.
- **C-SC-5 (P2) — Coordinated governance analysis.** § 9 verification protocol now records that tier-placement analysis and precedent-methodology analysis are mutually informing domains; future amendments should conduct them in parallel rather than sequentially.
- **C-SC-6 (P2) — Conditional constitutional coordination analysis preserved.** Cross-tier coordination requirements identified by strict-reader (single atomic change for cross-tier consistency, multi-product evidence for Tier 1 placement) are recorded as established methodological constraints binding on all future amendments. See § 13 "Methodological lessons" below.
- **C-SC-7 (P2) — Originating-stage override documented.** The v2 originating arbitration's invocation of override-with-rationale against pragmatist's Q2 technology mandate was procedurally invalid (the precedent's scope is blind verification only). The substantive Q2 outcome (APPROVE-WITH-FIXES preserving format choice as product-pick) is preserved in v3 based on substantive technical convergence (three of four originating agents agreed on technical grounds independent of override-with-rationale), not by re-asserting the procedural invocation. The v2 "Override-with-rationale invoked" phrasing is rewritten below in the v1→v2 changelog accordingly.

## Changelog from v1 (originating-fixes, 2026-05-12, revised in v3 per C-SC-7)

Originating-deliberation arbitration (2026-05-12, commit `026b417`) ruled APPROVE-variant on all three questions and produced eight binding conditions (C1-C8) applied in v2:

- **Q1 ruling: APPROVE-WITH-FIXES.** Conditions C1-C4 applied (bidirectional drift detection, pre-merge gate placement, consumer-side fixtures, schema surface coverage) — sharpens mechanical verifiability.
- **Q2 ruling: APPROVE-WITH-FIXES.** Conditions C5-C6 applied (strengthened conformance wording + worked-example fixtures); format choice preserved per spec § 3 non-goal. **(Revised in v3 per C-SC-7:)** The originating arbiter invoked "override-with-rationale" against the pragmatist's mandate to require JSON Schema / XSD / Pydantic specifically. v3 disclaims that procedural invocation — override-with-rationale applies to blind-verification verdicts only. The substantive disposition (format-choice preserved) stands on its own merits: three of four originating agents converged on the technical position that schema format should be product-choice subject to mechanical-enforceability constraints, with the gaming concern addressed by C5+C6 wording (machine-executable conformance check with binary pass/fail + field-presence + type + value-constraint verification; three worked-example fixtures including a wrong-field-type fail case). The convergence stands independent of the override-with-rationale invocation.
- **Q3 ruling: APPROVE-WITH-EXTENSION.** Conditions C7-C8 applied (differentiated deadlines + Remediation-Blocked status). **(Superseded in v3 per C-SC-2:)** Differentiated deadlines are removed. C7 is replaced by a universal 2026-12-01 deadline. C8 (Remediation-Blocked status) is preserved with deadline-text scrubbed of differentiation.
- Eight conditions total; § 4 sub-clauses 1-4 tightened (C1-C6); § 2 goals 3-5 deadlines unified at 2026-12-01 in v3; § 10 placeholder C1/C2/C3 superseded by C1-C8 in v2 and further revised by C-SC-1..7 in v3.

> **Scope discipline:** This spec amends `build-fractal/conversus/CONSTITUTION.md` (Tier 2 Suite) by adding a new Principle XXVIII "Persistence Contract Discipline." It does NOT amend Tier 1. It does NOT remove or rename any existing principle. It does NOT prescribe a specific schema format (XSD, JSON Schema, Pydantic, AST validator) — products pick. It does NOT mandate XML for conversus outputs; the XML migration is a follow-on component-tier spec that conforms to this amendment. It DOES mandate mechanical enforcement of declared schemas — declaration without enforcement is itself a violation.

---

## 1. Summary

The conversus suite today has two confirmed gaps in stable-interface discipline at the persistence boundary:

1. **Implicit persistence contracts.** Conversus deliberation output uses mode-specific keyword markers (`**Dispute:`, `**Vulnerability:`, etc.) embedded in markdown display text — the linter parses by regex against these literals. Adding a 9th mode requires updating the parser. 6 of 8 modes currently short-circuit silently in the dispute parser (surfaced by PR #139, marked xfail).

2. **Declared-but-unenforced contracts.** spec-kit-orc has a written state-files contract (`specs/001-orchestrator/contracts/state-files.md`) declaring schemas for JSON, JSONL, and YAML-frontmatter artifacts. Production data has drifted: 4 logically distinct JSONL schemas exist in `.orchestrator/`, two declared-schema sources contradict each other on field names and version syntax, and the canonical contract does not match what scripts emit.

Both gaps fail the spirit of stable-interface discipline within the conversus suite — persistent contracts cannot be stable if their stability is unenforced. The first gap couples conversus consumers to display text; the second gap couples spec-kit-orc consumers to a contract the producer no longer honors.

This amendment adds a new Tier 2 principle, **XXVIII. Persistence Contract Discipline**, to `build-fractal/conversus/CONSTITUTION.md` mandating that every conversus-family product MUST (a) declare a versioned schema for every stateful artifact, (b) mechanically enforce schema conformance in CI, (c) treat declared schema drift as a CI failure. Schema format is product-choice. Cross-product consumer contracts MUST be declared at the producer side; consumers MUST consume the declared contract, not implementation details.

The amendment is **MINOR** under the pathway taxonomy because it adds a new normatively-scoped principle to Tier 2 without removing or renaming any existing principle. The cost of conformance is real (every conversus-family product needs a state-files contract + CI gate) but proportionate to the stability gain.

**Scope rationale (v3, per C-SC-1):** Evidence supporting this principle is drawn from three repos within a single product family (conversus-oss, conversus-enhanced, spec-kit-orc — all conversus suite). Tier 1 (Universal) placement requires multi-product-family evidence per Tier 1 Authority L44-46. Tier 2 placement matches the evidence scope: every conversus-family repo is subject; future Build Fractal product families outside conversus are not bound by this principle until they accumulate analogous evidence and ratify their own (suite-tier or universal-tier) version.

## 2. Goals

1. Tier 2 (conversus suite) constitution gains a new Principle XXVIII "Persistence Contract Discipline" with operational definitions for "declared schema", "mechanical enforcement", "schema drift", and "cross-product consumer contract".
2. Conversus-oss adds a `CONSUMER-CONTRACT.md` at the repo root declaring its cross-product stability surface (output filenames, heading text used by external parsers, the `linter.output_contract` Python API surface).
3. Conversus-oss `CONFORMANCE.md` adds a new Provisional remediation row: implement structured XML output for deliberation phases (closes the V parser gap surfaced by PR #139; deadline **2026-12-01**). This row is the bridge to the follow-on component-tier spec. *(Temporal scope per D2: deadline binds conversus-oss as it exists at ratification, projected 2026-05-12. Future siblings joining the conversus suite after ratification are governed by their admission process, not retroactively bound to this date.)*
4. Conversus-enhanced `CONFORMANCE.md` gains the same Provisional remediation row for ITS persistence artifacts (per-solver run metadata, if any) — deadline **2026-12-01**. *(Temporal scope per D2: deadline binds conversus-enhanced as it exists at ratification, projected 2026-05-12. Future siblings joining the conversus suite after ratification are governed by their admission process, not retroactively bound to this date.)*
5. spec-kit-orc `CONFORMANCE.md` (created 2026-05-10) gains a new Provisional remediation row: reconcile `state-files.md` declared schemas with production JSONL data; add mechanical validator at `bin/validate-state.sh`; deadline **2026-12-01**. *(Temporal scope per D2: deadline binds spec-kit-orc as it exists at ratification, projected 2026-05-12. Future siblings joining the conversus suite after ratification are governed by their admission process, not retroactively bound to this date.)*
6. `build-fractal/conversus/README.md` (or, if absent, suite-level entry-point doc) gains a new section "Persistence Contract Discipline" linking to the Principle XXVIII text and listing each product's CONSUMER-CONTRACT.md.

> **Universal-deadline rationale (v3, per C-SC-2; refined v4 per D2).** A Tier 2 principle applies to every conversus-family repo; granting per-repo deadline relief contradicts the principle's universality claim and would be mechanically verifiable as inconsistent with the principle's own scope. v3 sets a single universal 2026-12-01 deadline — the later of v2's two dates (the universal bar must accommodate the longest realistic remediation, not the shortest). Products MAY self-declare earlier ready dates as opt-in; the principle's normative bar is uniform.
>
> **Temporal scope (v4, per D2):** the 2026-12-01 deadline applies to products **existing at ratification**. Future siblings admitted to the conversus suite after ratification receive their persistence-contract-discipline deadline through their admission process — not retroactive inheritance of 2026-12-01. This preserves the universality claim (uniform within temporal scope) while avoiding the logical impossibility (per Principle VII) of retroactive obligations on products that did not exist when the deadline was set. The temporal-scope distinction is between *membership universality* (every conversus-family repo at the relevant point in time is bound) and *temporal universality* (a single fixed past date binds future entrants). The principle adopts membership universality; temporal universality is rejected as logically impossible.

## 3. Non-goals

- **Does NOT mandate XML.** Product implementations choose XSD, JSON Schema, Pydantic, AST-validator, or any other mechanical schema language. The amendment mandates that SOME mechanical enforcement exists.
- **Does NOT migrate conversus outputs to XML in this spec.** That's a follow-on component-tier spec (`v4.1.1-conversus-structured-output` or similar) that conforms to this amendment.
- **Does NOT rewrite spec-kit-orc's `state-files.md` in this spec.** Spec-kit-orc's reconciliation is its own follow-on under the Provisional remediation goal #5.
- **Does NOT introduce a Tier 1 principle.** v3 placement is Tier 2 per C-SC-1. Cross-tier promotion to Tier 1 requires multi-product-family evidence (a non-conversus Build Fractal sibling exhibiting the same persistence-contract failure pattern) and its own amendment cycle.
- **Does NOT apply retroactively to existing Implicit-Provisional or Compliant-Provisional repos in punitive terms.** Existing conversus-family products gain a Provisional remediation row on a unified 2026-12-01 deadline per § 2 goals 3-5. *(Per D2: the 2026-12-01 deadline binds products existing at ratification only.)* New product admissions to the conversus suite after ratification MUST include a CONSUMER-CONTRACT.md (or equivalent) and CI gate at admission time, **with their persistence-contract-discipline deadline assigned via their admission process** — not retroactive inheritance of 2026-12-01.
- **Does NOT govern transient state.** In-memory state, temp files outside `.conversus/`/`.orchestrator/`, and ephemeral session artifacts are out of scope. The principle governs persistent on-disk state intended to outlive the writing process.
- **Does NOT bind product families outside the conversus suite.** Tier 2 scope is the conversus product family. Cross-suite extension is out of scope for this amendment.

## 4. Principle Amendment — text being added

The following new principle is appended to `build-fractal/conversus/CONSTITUTION.md` after the existing Principle XXVII (Operator-Configurable Tool Surface) and before the "Cross-tier weakening prohibition" section. Existing Tier 2 principles V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII are preserved byte-for-byte unchanged.

```markdown
### XXVIII. Persistence Contract Discipline

Persistence contracts ARE stable interfaces. This principle elaborates
the Tier 1 Principle II stable-interface doctrine specifically for
persistent on-disk state — the same doctrinal frame, applied to a
different surface category.

Persistent on-disk state is itself a stable interface. Every stateful
artifact a conversus-family product writes to disk MUST satisfy:

1. **Declared schema.** The artifact has a written schema declaration
   in a discoverable location (typically `STATE-FILES.md`,
   `CONSUMER-CONTRACT.md`, or an equivalent canonical doc at the repo
   root). A location is "discoverable" if it (a) lives at the
   producer repo root, OR under a suite-convention directory (e.g.,
   `schemas/`) documented in the repo's `CONFORMANCE.md`; (b) follows
   the suite naming convention (`STATE-FILES.md`,
   `CONSUMER-CONTRACT.md`, `CONFORMANCE.md`, `schemas/`, or an
   equivalent declared in the repo's `CONFORMANCE.md`); AND (c) is
   linked from BOTH the repo's top-level `README.md` AND its
   `CLAUDE.md` (or the equivalent agent entry-point doc). The schema
   specifies field names, types, structural requirements, and a
   `schema_version` field. Coverage extends to any
   persisted state regardless of structural shape, including but not
   limited to: field-based formats (JSON, YAML, TOML), JSONL streaming
   (with explicit line semantics — one record per line, record type
   discrimination, ordering guarantees if any), positional formats
   (CSV, TSV, fixed-width), binary formats (with byte-layout or
   serialization-library declaration), and hybrid formats such as
   YAML-frontmatter-plus-markdown (with both the frontmatter schema
   and the body-section structure declared). The discipline applies
   to every persisted on-disk artifact; format shape does not exempt
   an artifact from the declared-schema mandate.

2. **Mechanical enforcement.** A CI gate validates that artifacts
   written during a run conform to the declared schema. The gate MUST
   be PR-required and merge-blocking — not advisory, not post-merge,
   not informational. Schema format is product-choice — XSD, JSON
   Schema, Pydantic model, AST validator, or any other format whose
   conformance check is machine-executable, produces a binary
   pass/fail result with specific failure descriptions, and verifies
   field presence, types, and value constraints — explicitly
   excluding prose descriptions, manual checklists, and subjective
   interpretation. Validation MUST be bidirectional: not only do
   artifacts written by the producer conform to the schema (forward
   validation), but any change to the schema itself MUST trigger
   CI verification that the existing producer code still emits
   conformant artifacts under the new schema (drift detection on
   schema edits). Each product's CI gate MUST ship with at least
   three test fixtures committed to the repo: (a) a known-conformant
   artifact that validation passes, (b) a known-non-conformant
   artifact with a missing required field that validation fails on,
   and (c) a known-non-conformant artifact with a wrong field type
   that validation fails on. Schemas declared without enforcement,
   without bidirectional drift detection, or without the worked-
   example fixtures do not satisfy this discipline.

3. **Versioning.** The schema carries a `schema_version` field with a
   documented bump procedure. The `schema_version` field MUST use
   semantic versioning (MAJOR.MINOR.PATCH) by default, OR a documented
   alternative with explicit total-ordering semantics. Products
   choosing an alternative MUST document the format and its ordering
   semantics in their `CONSUMER-CONTRACT.md`. Schema evolution MUST
   update the version; silent format changes are a violation.

4. **Cross-product consumer contracts.** When a conversus-family
   product B consumes artifacts written by conversus-family product A,
   product A MUST publish a `CONSUMER-CONTRACT.md` (or equivalent) at
   its repo root declaring which output surfaces are stable. Product B
   MUST consume the declared surface, not implementation details
   (heading text, hardcoded paths, English error strings). Changes to
   declared surfaces require a version bump and consumer-coordinated
   migration; changes to undeclared internals are free. Consumer-side
   enforcement: product B MUST ship test fixtures pinning the
   consumed surface from the consumer's perspective, validated in
   *consumer* CI (not only in producer CI). Producer-side fixtures
   alone do not satisfy this sub-clause — the consumer pins the
   contract as it actually depends on it, so producer-side drift
   surfaces as consumer-side CI failure.

5. **Declaration scope.** Display text inside an artifact is NOT a
   stable contract unless explicitly declared as such. **Explicit
   declaration MUST appear in the producer's `CONSUMER-CONTRACT.md`
   (or equivalent declared canonical doc per sub-clause 1), naming
   the specific display-text surface — heading text, error string,
   marker, or other concrete textual token — and stating the
   stability guarantee** (e.g., "the `## Verdict` heading is a stable
   parse target; a MAJOR `schema_version` bump is required to change
   it"). A producer who omits this declaration leaves the display
   text undeclared and therefore unstable; consumers parsing
   undeclared display text are violating sub-clause 4 (cross-product
   consumer contracts) regardless of the producer's behavior. Parsing
   display text for semantic content is forbidden when a structural
   surface exists; if no structural surface exists, declaring display
   text as the contract is permitted (via the mechanism above) but
   creates a debt the product MUST close.

The principle scope is persistent on-disk state intended to outlive
the writing process within the conversus product family. Transient
state (in-memory, ephemeral temp files outside declared state
directories) is out of scope. The principle does not bind product
families outside the conversus suite; cross-suite extension requires
a separate amendment.

*Origin: cross-product persistence audit 2026-05-11. Conversus
deliberation outputs short-circuited silently in 6 of 8 modes because
the parse contract lived in display text. spec-kit-orc's declared
state-files contract drifted from production JSONL data, with 4
divergent in-tree schemas and contradictory schema_version syntax in
the canonical documentation itself.*
```

## 5. Verbatim preservation contract

Existing Tier 1 `build-fractal/CONSTITUTION.md` is NOT amended by this spec. Its content is preserved byte-for-byte.

Existing Tier 2 principles in `build-fractal/conversus/CONSTITUTION.md` (V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII) MUST be preserved byte-for-byte. The new Principle XXVIII is APPENDED after XXVII and before the "Cross-tier weakening prohibition" section, not interleaved with or substituted for existing principles.

Existing component-tier principles in conversus-oss, conversus-enhanced, and spec-kit-orc CONSTITUTION.md files are NOT amended by this spec.

Sync Impact Report comment blocks accumulated across prior Tier 2 amendments are preserved unchanged. v4.1.0 adds a new SIR block per existing convention at the top of Tier 2 CONSTITUTION.md.

## 6. File edits per repo

### 6.1 Tier 2 — `build-fractal/conversus/CONSTITUTION.md`

- Append new principle text (§ 4 above, byte-for-byte) after the existing § XXVII section, before the "---" preceding "Cross-tier weakening prohibition".
- Update the SIR header at the top of the file: bump Version `1.0.0` → `1.1.0` (MINOR). Add a new SIR block recording the v4.1.0 amendment, originating + self-consistency + blind deliberation pointers, and the universal 2026-12-01 deadline.
- Update the "Principles" preamble paragraph (currently "The 10 principles below…") to read "The 11 principles below…".
- Update the table-of-contents-style list in the SIR header (currently "Principles relocated here from conversus-oss/CONSTITUTION.md v3.2.3:") to add a separate "Principle added v4.1.0:" subsection listing "XXVIII. Persistence Contract Discipline".

### 6.2 Tier 1 — `build-fractal/CONSTITUTION.md`

**No edits.** Tier 1 placement was rejected by self-consistency arbitration per C-SC-1. Document this explicitly in the v4.1.0 SIR block at Tier 2 (above): "Tier 1 placement attempted in v2; demoted to Tier 2 in v3 per self-consistency arbitration `8f90e2d` (evidence base limited to conversus product family, fails Tier 1 multi-product-family requirement)."

### 6.3 conversus-oss — `build-fractal/conversus/conversus-oss/`

**New files:**
- `CONSUMER-CONTRACT.md` — declares the cross-product stability surface for consumers (spec-kit-orc adapter is the primary consumer today). Must enumerate:
  - Output filename contracts: `summary/final.md`, `arbitration/resolution.md`, `{agent}/disputes.md`, etc. — which are stable, which are derived.
  - Output structural surfaces: `## Verdict` heading in arbitration is the current de-facto parse target; declare it stable OR mark it deprecated pending the XML migration follow-on.
  - Python API surface: `linter.output_contract` is currently consumed by spec-kit-orc's adapter via `python -m linter.output_contract`. Declare which functions/return values are stable.
  - Provider-error message strings: spec-kit-orc's `KNOWN_PROVIDER_ERROR_PATTERNS` greps English literals — declare these strings stable or move them into a structured error code.
  - Schema-bump procedure: pointer to `CHANGELOG.md` + a documented version-bump policy.
- `schema/output-contract.md` — placeholder for the follow-on component-tier spec's XSD/JSON-Schema definition. May be empty in v4.1.0 (the follow-on creates the actual schema); existing during this amendment to satisfy the "declared schema" mandate for the deliberation-output artifact.

**Edits:**
- `CONFORMANCE.md` Tier 2 row XXVIII: declare status with evidence note (`CONSUMER-CONTRACT.md` present; structured-output schema follow-on tracked). Note: row XXVIII is *new* — added by this amendment, not pre-existing.
- `CONFORMANCE.md` Provisional remediation plan: ADD a new row for "deliberation-output structured schema" with deadline **2026-12-01** and tracking pointer to the follow-on spec.

### 6.4 conversus-enhanced — `build-fractal/conversus/conversus-enhanced/`

**New files:**
- `CONSUMER-CONTRACT.md` — declares stability surface for downstream consumers (mostly: solver outputs, configuration manifests).

**Edits:**
- `CONFORMANCE.md` Tier 2 row XXVIII: declare status + evidence note.
- `CONFORMANCE.md` Provisional remediation plan: ADD row if any stateful artifacts exist that need schema declaration with deadline **2026-12-01**; if no stateful artifacts beyond what's already covered by upstream conversus-oss, mark this row N/A with rationale.

### 6.5 spec-kit-orc — `build-fractal/spec-kit-orc/`

**Edits:**
- `CONFORMANCE.md` Tier 2 row XXVIII: declare status (currently Provisional from the 2026-05-10 initial declaration generalizing to the new principle) with evidence note + the new amendment scope.
- `CONFORMANCE.md` Provisional remediation plan: ADD a row for "reconcile state-files.md declared schemas with production JSONL data; add `bin/validate-state.sh`" with deadline **2026-12-01**.
- Existing `specs/001-orchestrator/contracts/state-files.md` is referenced by this amendment as a positive example (declared contract exists) but flagged as needing mechanical enforcement to satisfy the new principle.

**Note on suite membership:** spec-kit-orc is part of the conversus suite by virtue of its adapter consuming conversus deliberation outputs; its compliance with the new Tier 2 principle is therefore in scope. If spec-kit-orc's suite membership is later revisited, this CONFORMANCE.md row's status follows that membership.

### 6.6 build-fractal/conversus/ suite docs

- `build-fractal/conversus/README.md` (or, if no README exists at the suite directory level, in `build-fractal/conversus/CLAUDE.md`'s "Constitutional reading order" subsection): add a pointer to the new Principle XXVIII and list each product's CONSUMER-CONTRACT.md.

### 6.7 CONSTITUTIONAL_CONVERSATIONS.md entries

- `build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md`: log v4.1.0 amendment per existing convention. Required entries: (a) originating deliberation 2026-05-12 + arbitration ruling `026b417`; (b) self-consistency verification 2026-05-12 + arbitration ruling `8f90e2d` (DEMOTE-TO-TIER-2 / FAIL-OVERSTRETCH); (c) Override-with-rationale scope restriction (per C-SC-3) logged here as a procedural correction; (d) blind verification entry (TBD); (e) ratification entry (TBD).
- Component-tier `conversus-oss/CONSTITUTIONAL_CONVERSATIONS.md`: log the conversus-oss specific impact (new CONSUMER-CONTRACT.md, new Provisional row).
- Component-tier `conversus-enhanced/CONSTITUTIONAL_CONVERSATIONS.md` (if one exists; if not, create per Principle II convention): log impact.
- spec-kit-orc currently has no CONSTITUTIONAL_CONVERSATIONS.md (component constitution not yet declared). Optional: create one as part of this spec; or defer to spec-kit-orc's own follow-on remediation work.

## 7. Cross-product implications

| Product | Today | Post-v4.1.0 (declaration) | Post-remediation (universal 2026-12-01) |
|---|---|---|---|
| conversus-oss | Output parse contract in display text; no CONSUMER-CONTRACT.md; V parser short-circuits on 6/8 modes | CONSUMER-CONTRACT.md declares current surfaces; new Provisional row tracks structured-output migration | Structured XML output (or equivalent) ships; XSD CI gate active; V's 6 xfail tests un-xfail |
| conversus-enhanced | No documented cross-product consumer surface | CONSUMER-CONTRACT.md declares surface (or asserts N/A with rationale) | If applicable: schema enforcement on whatever stateful artifacts the paid layer writes |
| spec-kit-orc | state-files.md exists but drifted from production data; consumer of conversus implementation details (hardcoded paths, awk-grep on `## Verdict`, KNOWN_PROVIDER_ERROR_PATTERNS) | New Provisional row tracks: (a) reconcile state-files.md with production data, (b) add mechanical validator, (c) rewrite Conversus adapter against conversus's CONSUMER-CONTRACT.md | Both gaps closed: spec-kit-orc validates its own state; Conversus adapter consumes only declared surfaces |
| Future conversus-family siblings | No discipline | Admission requires CONSUMER-CONTRACT.md + CI gate at admission time; persistence-contract-discipline deadline assigned via admission process (NOT retroactive inheritance of 2026-12-01 per D2 temporal scope) | (same — admission gate enforces discipline going forward; admission-time deadline applies) |
| Non-conversus Build Fractal products | Out of scope of this amendment | Out of scope | Out of scope (Tier 2 = conversus suite only per C-SC-1) |

## 8. Constitutional Inclusion Criteria gate

Per spec 070, the three Inclusion Criteria for principle additions/extensions are:

1. **Universal applicability (at the principle's declared tier scope)** — does it apply to all products within scope?
2. **Mechanical verifiability** — can conformance be checked deterministically?
3. **Non-redundant** — does it cover something not already addressed by an existing principle?

This amendment passes:

1. **Universal at Tier 2**: persistent on-disk state is a feature of every conversus-family product. ✅ (Tier 1 universality, by contrast, would require non-conversus product evidence, which is absent — hence v3's tier demotion.)
2. **Mechanical**: the discipline literally MANDATES mechanical enforcement; conformance is a CI gate. ✅
3. **Non-redundant**: existing Tier 2 principles V (Observable Deliberation), XV (Plugin Isolation), and XXII (Distribution Surface Integrity) treat operational concerns at runtime + at distribution time; none addresses the persistence-contract surface specifically. ✅

## 9. Verification protocol

Per spec 067, Tier 2 principle additions require **originating + self-consistency + blind** deliberations. The pathway taxonomy permits MINOR Tier 2 amendments with all three.

> **Coordinated governance analysis (v3, per C-SC-5):** future amendments should conduct tier-placement analysis and precedent-methodology analysis as mutually informing domains in parallel rather than sequentially. The self-consistency arbitration in this amendment cycle revealed genuine circular dependency between the two — tier placement affects precedent rules while precedent scope affects constitutional foundation. Sequential treatment creates artificial prioritization where coordinated treatment preserves the structural relationship.

> **Intra-stage Q1/Q2 sequencing (v4, per D1):** within each verification stage (originating, self-consistency, blind), question evaluation MUST proceed in order: **Q1 (constitutional coherence — internal contradictions with existing principles) before Q2 (evidence base adequacy — tier-placement justification) before Q3 (precedent/scope concerns).** Q1 is structurally independent of Q2 — a principle's text either coheres with existing principles or it does not, regardless of whether the evidence base supports its claimed tier. Q2 evidence gaps may affect tier placement but do not create constitutional contradictions. The QUESTION.md framework is itself a stable interface (Principle II) whose tri-question separation must be honored procedurally. Q1 issues are evaluated to completion before Q2 analysis begins; Q2 feeds Q1's completeness check only insofar as evidence informs whether the principle text *as it stands* coheres at the asserted scope.
>
> **Constitutional adequacy before enforcement design (v4, per D3 — companion to D1):** ratification-blocking issues (constitutional contradictions, tier-evidence mismatches, precedent-scope violations) MUST be evaluated and resolved **before** enforcement-mechanism design issues (CI gate placement, fixture requirements, deadline length, conformance-row schema). The former determine whether the principle CAN ratify; the latter are post-ratification operational enhancements that calibrate HOW it operates. Constitutional foundation (behavior, per Principle IX) must be sound before operational superstructure (shape) is built atop it. The cross-review process that produced D1+D3 surfaced this distinction as the load-bearing methodological insight of the rerun: arbiters who collapse adequacy and enforcement into a single P1 axis risk building elaborate enforcement machinery atop constitutionally invalid foundations, or conversely, blocking ratification on enforcement-design refinements that should be post-ratification follow-ups.

### 9.1 Originating deliberation

- Config: `deliberations/v4.1.0-persistence-contract-discipline-originating-2026-05-11/conversus.yml`
- Mode: cooperative
- Agents: pragmatist, devil's advocate, persistence/CI expert; mechanist + architect.
- Arbiter: balanced-arbiter or constitutional-arbiter, grounded in Tier 2 CONSTITUTION.md + this spec.
- Result: arbitration ruling at commit `026b417`. v2 produced.

### 9.2 Self-consistency verification

- Config: `deliberations/v4.1.0-persistence-contract-discipline-self-consistency-2026-05-12/conversus.yml`
- Different agent composition (strict-reader, purist, tier-coherence-auditor, precedent-auditor).
- Result: arbitration ruling at commit `8f90e2d`. Q1 PASS-WITH-CLARIFICATIONS, Q2 DEMOTE-TO-TIER-2, Q3 FAIL-OVERSTRETCH. v3 (this document) produced via seven required changes.

### 9.3 Self-consistency re-run

- Config: `deliberations/v4.1.0-persistence-contract-discipline-self-consistency-rerun-2026-05-12/conversus.yml`
- Fresh agent composition (strict-reader, purist, tier-coherence-auditor, precedent-auditor) targeting v3's substantively re-targeted content (tier demotion + universal deadline).
- Result: arbitration ruling at commit `a17d13a`. Q1 PASS-WITH-CLARIFICATIONS, Q2 PASS, Q3 PASS-WITH-EDITS. Combined disposition: PROCEED TO BLIND VERIFICATION. Four D-conditions (D1-D4) applied to produce v4 (this document).

### 9.4 Blind verification

- Config: `deliberations/v4.1.0-persistence-contract-discipline-blind-2026-05-12/conversus.yml`
- Stripped spec presented to fresh agent composition (naive-reader, implementation-engineer, risk-auditor, external-scholar) with no prior arbitration context.
- Result: arbitration ruling at `deliberations/v4.1.0-persistence-contract-discipline-blind-2026-05-12/arbitration/resolution.md`. Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS, Q2 MODERATE-RISK-MANAGEABLE, Q3 PARTIALLY-COHERENT. Combined disposition: **PROCEED TO RATIFICATION**. Four E-conditions (E1-E4) applied to produce v5 (this document).

### 9.5 Ratification

- All deliberation stages passing (with applied fixes) → flip status to `Status: Ratified` + apply file edits per § 6.
- Update SIR blocks, version footer, CONSTITUTIONAL_CONVERSATIONS.md entries.

## 10. Conditions

### 10.1 Conditions surviving from originating arbitration

C1-C6 from the originating arbitration ruling (commit `026b417`) survive in v3 unchanged. They constrain the content of Principle XXVIII (§ 4 above):

- **C1 — Bidirectional drift detection.** Sub-clause 2 mandates forward validation AND schema-edit-triggered drift detection. *(Applied: § 4 sub-clause 2.)*
- **C2 — Pre-merge gate placement.** § 4 mandates **PR-required / merge-blocking** CI gate. *(Applied: § 4 sub-clause 2.)*
- **C3 — Consumer-side contract validation fixtures.** Consumers ship test fixtures pinning consumed surfaces in *consumer* CI. *(Applied: § 4 sub-clause 4.)*
- **C4 — Schema surface coverage.** Coverage extends to JSONL streaming, positional, binary, hybrid YAML-frontmatter formats. *(Applied: § 4 sub-clause 1.)*
- **C5 — Strengthen conformance wording.** Machine-executable, binary pass/fail, field-presence + type + value-constraint verification — excluding prose/checklists/subjective. *(Applied: § 4 sub-clause 2.)*
- **C6 — Worked-example test fixtures.** Three fixtures per product: conformant pass, missing-required fail, wrong-type fail. *(Applied: § 4 sub-clause 2.)*

### 10.2 C7 — REPLACED in v3 (per C-SC-2): Universal remediation deadline

C7 in v2 specified differentiated deadlines. The self-consistency arbitration ruled this constitutionally invalid (High confidence): differentiated deadlines violate the principle's universality regardless of tier, because a universally-scoped principle cannot grant product-specific accommodations.

**v3 C7 (refined in v4 per D2):** Update spec § 2 goals 3-5 (conversus-oss + conversus-enhanced + spec-kit-orc) to a uniform deadline of **2026-12-01**, reflecting the conversus-suite-wide remediation window. The longer of v2's two dates (2026-12-01 vs 2026-09-01) is chosen because the universal bar must accommodate the longest realistic remediation, not the shortest. Products MAY self-declare earlier ready dates as opt-in; the principle's normative deadline is uniform. **Temporal scope (v4, per D2):** the 2026-12-01 deadline binds products existing at ratification only. Future siblings admitted to the conversus suite after ratification receive their deadline via their admission process, not retroactively. This adopts *membership universality* (every conversus-family repo at the relevant point in time is bound) and rejects *temporal universality* (a single past date binding future entrants), which would be logically impossible per Principle VII. *(Applied: § 2 goals 3-5 + universal-deadline rationale paragraph; § 3 non-goals; § 6.3, § 6.4, § 6.5; § 7 table; § 11; § 12.)*

### 10.3 C8 — preserved in v3 (deadline-text scrubbed of differentiation)

Products that fail to ship their Provisional remediation by the assigned deadline (**2026-12-01** for all conversus-suite products under this amendment; future products per their admission-time assignment) transition to a named compliance status **"Remediation-Blocked"** with the following documented escalation path:

1. **Automatic status flip.** On the day after the assigned deadline passes without a closing remediation PR merged, the product's CONFORMANCE.md row for the Persistence Contract Discipline obligation flips from **Provisional** to **Remediation-Blocked**. The flip is mechanically determinable (date comparison + remediation PR merge check) and not subject to interpretation.

2. **Mandatory follow-up amendment cycle.** Within 30 days of the status flip, a follow-up **MINOR amendment** cycle MUST be opened that either (a) accepts an extended remediation deadline with a re-scoped plan and grounded engineering rationale, or (b) downgrades the product's compliance status (e.g., from Compliant-Provisional to Compliant-Withdrawn per the suite COMPLIANCE.md taxonomy). Inaction is not permitted: the follow-up amendment cycle is the only mechanically valid exit from Remediation-Blocked.

3. **Suite-level visibility.** Each Remediation-Blocked status MUST be logged in the suite-level `CONSTITUTIONAL_CONVERSATIONS.md` on the day of the automatic flip, with a pointer to the open follow-up amendment thread.

This mechanism resolves the apparent tension between fixed-deadline accountability and missed-deadline authority erosion: consequences are concrete and mechanically determinable, while the path forward is structured rather than punitive.

### 10.4 D-conditions from self-consistency Q1 (PASS-WITH-CLARIFICATIONS)

The Q1 ruling required clarifications on coordinated governance analysis and compound-debt acknowledgment. These are recorded as binding methodological constraints:

- **D1 — Coordinated governance analysis.** Tier-placement and precedent-methodology analyses are mutually informing. Recorded in § 9 above and § 13 below. Applied to all future amendments.
- **D2 — Compound constitutional debt acknowledgment.** Both the tier-evidence-mismatch and the override-precedent-stretch are unified governance discipline gaps. Recorded in § 12 below. Both are addressed in v3 (substantive correction via tier demotion + universal deadline; procedural correction via precedent rollback).

## 11. Override-with-rationale scope restriction (per C-SC-3)

The "override-with-rationale" precedent — established by prior amendments and recorded in `feedback_amendment_override_precedent.md` — permits an arbiter to apply a strict reading of a verdict that would shrink existing ratified principles, provided the override is logged in three places (Sync Impact Report + governance log + spec status).

**Scope (binding from this amendment forward):** the precedent applies **only to blind-verification verdicts**. Originating-stage arbitration may not invoke override-with-rationale. Self-consistency verification may not invoke override-with-rationale. Only blind verification — the deliberation stage explicitly designed to test the ratified principle against a stripped, version/date-blind spec — qualifies for this procedure.

**Rationale:** the precedent was established specifically to address blind-verification dynamics (an arbiter agent confronted with a strict reading that would retroactively narrow already-ratified principles). Originating arbitration operates on an unratified spec; the override mechanism has no application there. Self-consistency operates between originating and blind; its purpose is to surface internal contradictions, not to invoke overrides against agents proposing fixes.

**Enforcement:** any future invocation of override-with-rationale at a non-blind-verification stage MUST be flagged as procedurally invalid by the spec's verification log. The substantive disposition may stand if independently supported by agent convergence, but the procedural invocation does not count toward authority.

**Extension procedure:** any future expansion of the override-with-rationale scope (e.g., to self-consistency, to originating, to ratification-stage challenges) requires its own explicit constitutional amendment going through originating + self-consistency + blind verification stages. Implicit scope extension via case-by-case invocation is prohibited.

**Procedural boundary — substance does not cure procedure (v4, per D4):** **Agent convergence on substance CANNOT cure procedural violations.** When an arbiter invokes override-with-rationale outside its blind-verification scope (e.g., at originating or self-consistency), the procedural invocation is invalid regardless of how many agents subsequently converge on the substantive outcome. The invocation does not count toward authority, and the override's documented effects (SIR entry, governance log entry, spec status notation) must NOT be entered as if the procedure had executed validly.

**However, substantive outcomes MAY be preserved when procedures are corrected through proper channels.** When a procedurally invalid invocation is rolled back and the substantive disposition is re-grounded on independent agent-convergence (or other procedurally valid foundations), the substantive outcome can survive intact. The v2-Q2 originating-stage override invocation against pragmatist's technology mandate is the worked example: in v3 the procedural invocation was rolled back (per C-SC-7) and the substantive Q2 disposition (format-choice preserved) was re-grounded on the substantive technical convergence of three of four originating agents — independent of override-with-rationale. The substantive outcome survived; the procedural invocation did not.

**The distinction is load-bearing:** procedure cannot be shortcut via substance (otherwise procedural rules collapse into "whatever the substantive majority wants"), but substance can be re-grounded after procedure is corrected (otherwise every procedurally invalid invocation would force re-litigating substantive outcomes that may be independently supportable). This boundary is itself a stable interface (Principle II) for governance discipline and prevents the failure mode in which procedural violations are retroactively justified by substantive agreement.

## 12. Compound constitutional debt (per C-SC-4)

The self-consistency arbitration identified two governance discipline gaps in v2 that share a common cause:

1. **Tier 1 placement attempt with insufficient evidence base** (evidence drawn from conversus product family only; Tier 1 requires multi-product-family evidence per L44-46).
2. **Override-with-rationale precedent applied outside its established scope** (precedent text restricts application to blind verification; v2 invoked it at originating stage).

Both gaps stem from the same governance discipline pattern: **ratification bias at the originating stage**. When an originating arbiter is grounded in the spec under review, the arbiter is structurally biased toward ratification — toward finding a path to APPROVE rather than toward strict procedural review. v2's originating arbitration exhibited this bias on both axes simultaneously: placement at Tier 1 (where the evidence didn't support it) and override-precedent invocation (outside the precedent's scope).

**Unified remediation in v3:**
- **Substantive correction:** tier demotion to Tier 2 (matches the evidence scope) + universal deadline (matches the principle's universality claim).
- **Procedural correction:** override-precedent scope rollback to blind-verification only (§ 11) + recording the v2 originating override as procedurally invalid (substantive Q2 disposition preserved on independent agent-convergence grounds per C-SC-7).

**Methodological lesson (binding for future amendments):** self-consistency verification's default-defend-status-quo posture is **load-bearing** in the amendment process. Future amendments should treat originating-stage "ratify with rationale" outcomes — particularly outcomes that invoke override-with-rationale or assert universal applicability — with **extra scrutiny** in self-consistency. The originating-stage arbiter's ratification bias is the failure mode self-consistency exists to catch; self-consistency should defend the procedural status quo (existing tier-placement criteria, existing precedent scope) against originating-stage drift, not extend deference to it.

## 13. Methodological lessons (per C-SC-6)

The self-consistency arbitration established methodological constraints binding on all future amendments:

1. **Single atomic change for cross-tier consistency.** A principle that touches both Tier 1 and Tier 2 (e.g., a Tier 1 principle whose Tier 2 expansion would loosen its bite) MUST be amended in a single atomic change rather than across phased amendments. Phased cross-tier amendments create transient inconsistency windows that violate Principle II's stable-interface guarantee.

2. **Multi-product-family evidence for Tier 1 placement.** Tier 1 placement requires evidence from at least two distinct product families (per Tier 1 Authority L44-46). Single-product-family evidence — even if structurally compelling — disqualifies Tier 1 placement and routes the amendment to Tier 2 or lower. v3's tier demotion is the worked example.

3. **Override-with-rationale scope is blind-verification only.** Per § 11 above. Implicit scope extension via case-by-case invocation is prohibited.

4. **Coordinated governance analysis for tier + precedent disputes.** Per § 9 and § 12 above. Tier placement and precedent methodology are mutually informing; sequential treatment creates artificial prioritization.

5. **Self-consistency defends procedural status quo against originating-stage ratification bias.** Per § 12 above. The originating-stage arbiter's bias toward APPROVE is the failure mode self-consistency exists to catch.

6. **Intra-stage Q1/Q2 sequencing (per D1).** Within each verification stage, Q1 constitutional coherence assessment MUST complete before Q2 evidence base adequacy analysis. Q1 (internal contradictions) is structurally independent of Q2 (tier-placement evidence adequacy); the QUESTION.md tri-question separation is a stable interface that must be honored procedurally. Per § 9 above.

7. **Constitutional adequacy precedes enforcement design (per D3).** Ratification-blocking issues (constitutional contradictions, tier-evidence mismatches, precedent-scope violations) MUST be evaluated and resolved before enforcement-mechanism design issues (CI gate placement, fixture requirements, deadline length). The former determine whether the principle CAN ratify; the latter are post-ratification operational enhancements. Per § 9 above.

8. **Substance does not cure procedure (per D4).** Agent convergence on substance cannot cure procedural violations. Substantive outcomes may survive when procedures are corrected through proper channels, but the procedural invocation itself does not count toward authority. Per § 11 above.

These constraints apply regardless of the disposition of this specific amendment.

## 14. Implementation order

Once ratified:

1. **Tier 2 edit** (§ 6.1) — append Principle XXVIII to `build-fractal/conversus/CONSTITUTION.md`, bump version to 1.1.0, add SIR.
2. **Suite-level docs** (§ 6.6) — add Persistence Contract Discipline pointer in `build-fractal/conversus/README.md` (or `CLAUDE.md`).
3. **Per-product CONSUMER-CONTRACT.md drafts** (§§ 6.3, 6.4) — create placeholder files; declare current surfaces; flag follow-on remediation rows.
4. **CONFORMANCE.md updates** (§§ 6.3, 6.4, 6.5) — add Tier 2 row XXVIII + Provisional remediation rows on each affected product with the unified 2026-12-01 deadline.
5. **CONSTITUTIONAL_CONVERSATIONS.md log entries** (§ 6.7) — include the override-with-rationale scope restriction (per C-SC-3) as a procedural correction entry.
6. **Follow-on spec drafts** — `v4.1.1-conversus-structured-output` and `v4.1.2-spec-kit-orc-state-files-reconciliation` open as separate specs implementing the Provisional rows. Each is its own component-tier amendment cycle.

## 15. SIR preview (Tier 2)

```markdown
<!--
Sync Impact Report
Version change: 1.0.0 → 1.1.0 (MINOR — Persistence Contract Discipline principle added to Tier 2 conversus suite constitution).
Governance log entry: 2026-MM-DD in build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md.
Originating deliberation: deliberations/v4.1.0-persistence-contract-discipline-originating-2026-05-11/ (arbitration commit 026b417).
Self-consistency verification: deliberations/v4.1.0-persistence-contract-discipline-self-consistency-2026-05-12/ (arbitration commit 8f90e2d — DEMOTE-TO-TIER-2, FAIL-OVERSTRETCH).
Self-consistency re-run on v3: deliberations/v4.1.0-persistence-contract-discipline-self-consistency-rerun-2026-05-12/ (arbitration commit a17d13a — Q1 PASS-WITH-CLARIFICATIONS, Q2 PASS, Q3 PASS-WITH-EDITS; PROCEED TO BLIND VERIFICATION; four D-conditions D1-D4 applied to produce v4).
Blind verification: deliberations/v4.1.0-persistence-contract-discipline-blind-2026-05-12/ (Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS / Q2 MODERATE-RISK-MANAGEABLE / Q3 PARTIALLY-COHERENT; PROCEED TO RATIFICATION; four E-conditions E1-E4 applied to produce v5).
Inclusion Criteria gate: PASS at Tier 2 (universal applicability within conversus suite + mechanical verifiability + non-redundant).
Pathway: MINOR (new Tier 2 principle XXVIII; no principle removed or renamed).
Per-product impact: new CONSUMER-CONTRACT.md at each suite repo root; new Provisional remediation rows in conversus-oss / conversus-enhanced / spec-kit-orc CONFORMANCE.md with a universal 2026-12-01 deadline (binding products existing at ratification only per v4 D2 temporal scope); follow-on component-tier specs for structured-output (conversus-oss) and state-files reconciliation (spec-kit-orc).
Procedural notes:
  - Tier 1 placement attempted in v2; demoted to Tier 2 in v3 per self-consistency arbitration 8f90e2d.
  - Override-with-rationale precedent restricted to blind-verification scope only (per v3 § 11). v2's originating-stage invocation logged as procedurally invalid; substantive Q2 disposition preserved on independent agent-convergence grounds.
  - v4 D1-D4 applied per self-consistency rerun a17d13a: intra-stage Q1/Q2 sequencing (D1), temporal scope of universal deadline — existing products only (D2), constitutional adequacy precedes enforcement design (D3), § 11 procedural boundary language — substance does not cure procedure (D4).
  - v5 E1-E4 applied per blind verification 2026-05-12: schema_version format mandate — SemVer default (E1), declaration mechanism via producer CONSUMER-CONTRACT.md (E2), discoverable-location criteria (E3), unifying preamble linking Principle XXVIII to Principle II (E4). All wording-level; principle's normative content unchanged.
Prior amendment (v4.0.0): tier extraction — see prior SIR block below.
-->
```

## 16. Status & next steps

- **Status:** v5 / post-blind / ratification-ready (2026-05-12).
- **Blind verification result:** Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS / Q2 MODERATE-RISK-MANAGEABLE / Q3 PARTIALLY-COHERENT; combined disposition **PROCEED TO RATIFICATION**. Four E-conditions (E1-E4) applied to produce this v5. See `deliberations/v4.1.0-persistence-contract-discipline-blind-2026-05-12/arbitration/resolution.md` and the v4 → v5 changelog above.
- **Next step:** ratification per § 9.5 — flip status to `Status: Ratified`, apply file edits per § 6, update SIR blocks, version footer, CONSTITUTIONAL_CONVERSATIONS.md entries.

## 17. Fix ledger

- **v1 → v2 (originating-fixes, 2026-05-12):** Applied conditions C1-C8 from binding arbitration ruling at `deliberations/v4.1.0-persistence-contract-discipline-originating-2026-05-11/arbitration/resolution.md` (commit `026b417`). Q1 APPROVE-WITH-FIXES (C1-C4 applied to § 4 sub-clauses 1, 2, 4). Q2 APPROVE-WITH-FIXES (C5-C6 applied to § 4 sub-clause 2; v2 noted override-with-rationale invoked against pragmatist's technology mandate — that invocation is rolled back in v3 per C-SC-7, with substantive Q2 disposition preserved on independent agent-convergence grounds). Q3 APPROVE-WITH-EXTENSION (C7 differentiated deadlines + C8 missed-deadline consequence; C7 superseded in v3 per C-SC-2). Draft placeholder conditions superseded.
- **v2 → v3 (self-consistency fixes, 2026-05-12):** Applied seven required changes from self-consistency arbitration `deliberations/v4.1.0-persistence-contract-discipline-self-consistency-2026-05-12/arbitration/resolution.md` (commit `8f90e2d`). C-SC-1 tier demotion (Tier 1 → Tier 2; new Principle XXVIII). C-SC-2 universal deadline (2026-12-01 across all suite products; differentiated deadlines removed). C-SC-3 override-with-rationale scope restricted to blind-verification only (§ 11). C-SC-4 compound constitutional debt acknowledged (§ 12). C-SC-5 coordinated governance analysis (§ 9 + § 13). C-SC-6 conditional constitutional coordination analysis preserved (§ 13). C-SC-7 originating-stage override violation documented + v2 Q2 changelog rewritten on substantive-convergence grounds.
- **v3 → v4 (self-consistency-rerun D-conditions, 2026-05-12):** Applied four D-conditions from self-consistency rerun arbitration `deliberations/v4.1.0-persistence-contract-discipline-self-consistency-rerun-2026-05-12/arbitration/resolution.md` (commit `a17d13a`). Rerun ruled Q1 PASS-WITH-CLARIFICATIONS / Q2 PASS / Q3 PASS-WITH-EDITS; combined disposition PROCEED TO BLIND VERIFICATION with four D-conditions applied. D1 intra-stage Q1/Q2 sequencing (§ 9, § 13). D2 temporal scope of universal deadline — products existing at ratification only; future siblings receive admission-time deadlines (§ 2 goals 3-5 + rationale, § 3 non-goals, § 7 table, § 10.2 C7). D3 constitutional adequacy precedes enforcement design (§ 9, § 13). D4 § 11 procedural boundary language — substance does not cure procedure, but substance can be re-grounded after procedure is corrected (§ 11).
- **v4 → v5 (blind-verification E-conditions, 2026-05-12):** Applied four E-conditions from blind verification arbitration `deliberations/v4.1.0-persistence-contract-discipline-blind-2026-05-12/arbitration/resolution.md`. Blind verification ruled Q1 IMPLEMENTABLE-WITH-CLARIFICATIONS / Q2 MODERATE-RISK-MANAGEABLE / Q3 PARTIALLY-COHERENT; combined disposition PROCEED TO RATIFICATION with four E-conditions applied. E1 `schema_version` format mandate — SemVer by default, or documented alternative with explicit total-ordering semantics (§ 4 sub-clause 3). E2 declaration mechanism for sub-clause 5 — explicit declaration MUST appear in the producer's `CONSUMER-CONTRACT.md`, naming the specific display-text surface and stating the stability guarantee (§ 4 sub-clause 5; the load-bearing implementability fix). E3 "discoverable location" criteria for sub-clause 1 — repo root (or documented suite-convention directory) + suite-convention naming + linked from both `README.md` AND `CLAUDE.md` (§ 4 sub-clause 1). E4 unifying preamble — single-sentence statement at start of § 4 linking Principle XXVIII to the Tier 1 Principle II stable-interface doctrine (§ 4 preamble). All four E-conditions are wording-level; the principle's normative content and conditions (C1-C8, D1-D4) survive unchanged. v5 is ratification-ready.
- **v5 → vN (post-ratification errata):** TBD.
