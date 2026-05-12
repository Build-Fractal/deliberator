# v4.1.0 Blind Verification — Arbitration Resolution

**Stage:** Blind verification (stage 3 of 3, final)
**Date:** 2026-05-12
**Agents:** naive-reader, implementation-engineer, risk-auditor, external-scholar
**Spec under review:** `specs/v4.1.0-persistence-contract-discipline/spec.md` (commit `8678bc7`)
**Constitutional grounding:** `build-fractal/CONSTITUTION.md` (Tier 1); `build-fractal/conversus/CONSTITUTION.md` (Tier 2)

---

## Process Note

This arbitration was produced **manually** because the engine's `disputes_remain` trigger did not fire on the Phase 5 synthesis. The synthesis output (`summary/final.md`) labelled its closing section "Critical Unresolved Tensions" rather than emitting the engine's expected `DISPUTES_BEGIN`/`DISPUTES_END` markers, so the Phase 6 arbiter never dispatched. The four agents' Phase 4 final positions (`revision_2.md`) and dispute statements (`disputes.md`) nonetheless converged sufficiently for arbitration to rule, but spec 067 requires a formal Q1/Q2/Q3 verdict line before ratification can proceed. This document supplies that formal ruling. It is grounded in the spec text, both constitutions, and the four agents' final-stage outputs only — no prior arbitrations were consulted, preserving the blind-verification property required by spec 067 § 9.4.

---

## Decision Framework

Blind verification's distinctive constitutional property (spec 067; reaffirmed in v4.1.0 spec § 9.4): agents read the spec **without prior arbitration context**, so their convergence — or lack of it — reflects the spec's standalone adequacy rather than the chain of reasoning that produced it. Per Tier 1 `CONSTITUTION.md` Principle II (stable interfaces) and Tier 2's existing principles V, XV, XXII, the constitution treats stability surfaces as load-bearing. The v4 spec extends that posture to the persistence boundary at Tier 2 scope; this arbitration evaluates whether the extension is implementable (Q1), operationally tolerable (Q2), and doctrinally coherent (Q3) when read fresh.

Default posture per spec 067: **defend-status-quo**. Blind verification's job is to catch what prior stages missed, not to extend deference to them. If the four agents genuinely converged on PASS-variants on the substance, the spec proceeds; if they surfaced ratification-blocking issues, ratification is held.

---

## Q1 — Implementability without external context

**Question (from QUESTION.md):** "Can a junior implementation engineer, reading ONLY spec v4 (no prior context, no governance documents beyond what the spec cites), correctly implement the persistence-contract discipline in a Build Fractal product?"

### Agent positions

**naive-reader** (`revision_2.md`, `disputes.md`):
- Final position retains four "surviving" recommendations as blocking implementability gaps: (1) define "discoverable location" criteria; (2) specify `schema_version` field format as SemVer; (3) define explicit-declaration mechanism for sub-clause 5; (5) specify bump-procedure documentation requirements.
- Non-Negotiable from `disputes.md`: "Sub-clause 5 is currently unimplementable without knowing how 'explicit declaration' occurs. This achieved unanimous agreement across all cross-reviews as a blocking constitutional gap."
- Flexibility: accepts that detailed operational procedures may move to separate guidance "provided essential definitional constraints that affect compliance determination remain in the constitutional text."

**implementation-engineer** (`revision_2.md`, `disputes.md`):
- Withdrew 0, modified 6 of 8, kept 2 surviving (Standardize Bump Procedure Format; Define Artifact Scope Boundaries).
- Position Summary: "the technical requirements in spec v4 are implementable with clarifications."
- New P1 recommendation "Separate Constitutional Doctrine from Implementation Guidance" — but framed as moving detail to authoritative implementation guidance, not as a substantive ratification blocker.
- Dispute is about *where* implementation guidance lives (constitutional text vs. separate guidance doc), not whether the principle can be implemented.

**risk-auditor** (`revision_2.md`): "Acknowledge technical implementability while maintaining operational concerns" (new P1 recommendation): "the technical requirements are achievable with clarifications, but operational constraints determine whether implementation can succeed within the mandated timeline." Technical-implementability question is conceded; operational feasibility is Q2 territory.

**external-scholar** (`revision_2.md`): Highest-priority surviving recommendation is "Clarify 'explicit declaration' mechanism" — identifies sub-clause 5 as unanimously flagged across cross-reviews as an "implementability failure." Surviving recommendations 5 (schema_version SemVer), 10 (bidirectional validation trigger conditions) and 6 (explicit declaration mechanism) all surface as gaps.

### Convergence

All four agents converged on three Q1 gaps in their disputes.md "Convergence" sections:

1. **Schema_version field format (SemVer or documented alternative)** — flagged "Unanimous" convergence across all four agents' disputes.md files. Spec v4 § 4 sub-clause 3 says only: *"The schema carries a `schema_version` field with a documented bump procedure"* — format unspecified.

2. **Explicit-declaration mechanism for sub-clause 5** — flagged "Unanimous" by all four. Spec v4 § 4 sub-clause 5: *"Display text inside an artifact is NOT a stable contract unless explicitly declared as such."* The spec does not specify how declaration occurs (CONSUMER-CONTRACT.md entry? STABLE-DISPLAY-SURFACES.md? frontmatter flag?).

3. **"Discoverable location" criteria for sub-clause 1** — Spec § 4 sub-clause 1 says *"a discoverable location (typically `STATE-FILES.md`, `CONSUMER-CONTRACT.md`, or an equivalent canonical doc at the repo root)"* — "typically" + "or equivalent" leaves the discoverability mechanism under-determined.

### Ruling

These three gaps are **wording-level fixes**, not substantive design holes. Each can be closed by a single sentence in the spec text:

- **E1 — `schema_version` format:** add to § 4 sub-clause 3 — *"The `schema_version` field MUST use semantic versioning (MAJOR.MINOR.PATCH) or a documented alternative with explicit total-ordering semantics."*
- **E2 — Explicit-declaration mechanism for sub-clause 5:** add — *"Explicit declaration MUST appear in the producer's `CONSUMER-CONTRACT.md` (or equivalent declared canonical doc), naming the specific display-text surface (heading, error string, marker) and stating its stability guarantee."*
- **E3 — "Discoverable location" criteria for sub-clause 1:** add — *"A location is 'discoverable' if it (a) lives at the repo root, (b) is named per the suite convention (`STATE-FILES.md`, `CONSUMER-CONTRACT.md`, `CONFORMANCE.md`, or an equivalent declared in the repo's `CONFORMANCE.md`), AND (c) is linked from the repo's top-level README or CLAUDE.md."*

implementation-engineer's framing — *"the technical requirements in spec v4 are implementable with clarifications"* — captures the disposition correctly. The remaining gaps are clarifications, not architecture. A junior engineer could implement the principle from v4 + E1/E2/E3 without senior consultation.

**Q1 verdict: IMPLEMENTABLE-WITH-CLARIFICATIONS.** E-conditions E1, E2, E3 apply to produce spec v5.

---

## Q2 — Worst-case operational impact

**Question (from QUESTION.md):** "If spec v4 ratifies as drafted, what is the worst-case operational impact across the conversus suite over the next 12 months?"

### Agent positions

**risk-auditor** (`revision_2.md`, `disputes.md`): The agent whose mandate is Q2. Final position withdrew 2 of 7 original recommendations (precedent-audit methodology; suite-admission persistence requirements) as out-of-scope follow-on work, and modified 5. Non-Negotiables:
- "Phased compliance checkpoints with early warning function" at 2026-09-01 and 2026-10-15.
- "Capacity-feasibility assessment before ratification."
- "Parallel operational and technical workstreams."

Critically, risk-auditor did **not** assert HIGH-RISK-RECONSIDER. The agent's framing: "The technical requirements are achievable with clarifications, but operational constraints determine whether implementation can succeed within the mandated timeline."

**implementation-engineer**: New P1 "Address Timeline Feasibility Before Technical Details" recognizes the 2026-12-01 universal deadline as real constraint but does not call for scope reduction or HIGH-RISK disposition.

**naive-reader** withdrew Recommendation 7 ("Add implementation planning guidance") explicitly because risk-auditor's parallel-processing reframe was correct.

**external-scholar** withdrew Recommendation 8 ("Separate universal deadline from principle requirements") explicitly because the universal deadline serves the principle's universality claim and is constitutionally legitimate (naive-reader's cross-review point that external-scholar conceded).

### Convergence

The four agents converged unanimously on "Parallel operational and constitutional workstreams" (risk-auditor disputes.md). C7 universal deadline of 2026-12-01 (§ 10.2) is accepted as constitutionally legitimate; D2 (§ 2 goals 3-5 temporal scope) and C8 (§ 10.3 Remediation-Blocked status with mandatory follow-up amendment cycle) are accepted as the mitigation framework.

The spec's C8 (§ 10.3) handles the worst-case "missed-deadline cascade" cleanly:
- *"Automatic status flip"* on the day after deadline → mechanically determinable.
- *"Within 30 days of the status flip, a follow-up MINOR amendment cycle MUST be opened"* → structured rather than punitive.
- Per spec § 7 cross-product implications table, a conversus-oss miss does not auto-fail spec-kit-orc; the consumer continues operating against the declared CONSUMER-CONTRACT.md, with producer-side delay surfacing through CONFORMANCE.md status rather than runtime consumer breakage.

### Worst-case-axis findings

1. **Missed-deadline cascade (C7 + C8):** Bounded. C8's status-flip mechanism + mandatory follow-up amendment cycle is structured. No agent argued the cascade is unbounded.

2. **CI gate burden (C1-C6 × three products):** Real but proportionate to stability gain (spec § 1 acknowledges: *"The cost of conformance is real (every conversus-family product needs a state-files contract + CI gate) but proportionate to the stability gain"*). Implementation-engineer's framing: achievable with clarifications.

3. **Forward-sibling onboarding friction (D2 + § 7 row 4):** Resolved by D2's temporal-scope distinction — new siblings get admission-time deadlines, not retroactive inheritance. risk-auditor explicitly withdrew "Define suite admission persistence requirements" as follow-on work for the first post-ratification sibling admission.

4. **Retroactive correction of prior amendments under D4:** risk-auditor explicitly withdrew Recommendation 5 ("Add precedent audit methodology") because D4 documents the v2-override rollback but "doesn't mandate systematic precedent auditing as a general requirement." No retroactive cascade.

5. **Compound debt acknowledgment side effects (§ 12):** risk-auditor's modified Recommendation 7 scopes § 12's compound-debt acknowledgment to this amendment's specific governance violations (tier-evidence mismatch + override-precedent stretch), not as a general precedent for future amendments. Spec § 12 already supports this reading.

### Ruling

The C-conditions (C1-C8) plus D-conditions (D1-D4) provide adequate mitigation. risk-auditor's two non-negotiable additions (phased checkpoints; capacity-feasibility assessment before ratification) are reasonable operational hygiene but are not ratification-blockers; they can be discharged as post-ratification operational follow-ups under the C8 framework (e.g., as voluntary milestones products commit to in their CONFORMANCE.md Provisional rows). The spec text itself does not need additional E-conditions to address Q2.

**Q2 verdict: MODERATE-RISK-MANAGEABLE.** C1-C8 + D1-D4 adequately mitigate the identified worst-case axes. risk-auditor's checkpoint and capacity-assessment recommendations are accepted as **operational guidance for post-ratification execution**, not as spec v5 E-conditions.

---

## Q3 — External doctrinal coherence

**Question (from QUESTION.md):** "Does spec v4, read as a constitutional principle by an external scholar with knowledge of constitutional governance but no Build Fractal context, hold up?"

### Agent positions

**external-scholar** (`revision_2.md`): The agent whose mandate is Q3. Withdrew 1 of 10 original recommendations, modified 3, kept 6 surviving. Critical revisions:
- Recommendation 1 (Extract process archaeology) **modified** based on naive-reader's distinction: *"§11 (override-with-rationale scope restriction) establishes 'a binding procedural rule' that creates ongoing obligations, while §§12-13 are 'historical self-flagellation' that document past events rather than establish future constraints."*
- Recommendation 8 (Separate universal deadline) **withdrawn** because naive-reader's argument that "universal deadlines serving universality claims can be constitutionally legitimate" prevailed.

external-scholar's disputes.md highlights two remaining tensions:
- "Process Archaeology Extraction Scope" — extract §§12-13, preserve §11.
- "Constitutional Doctrinal Unity Assessment" — the five-point structure "risks reading as 'five concerns clustered under a shared name' rather than a unified constitutional doctrine."

Neither dispute escalates to READS-AS-COMPROMISE-RECORD. external-scholar explicitly notes: *"If they create no ongoing constraints for future amendments, they belong in governance records, not constitutional text."* This is an E-condition framing, not a doctrinal-rewrite framing.

**naive-reader**, **implementation-engineer**, **risk-auditor** all accepted the principle's structure without challenging doctrinal unity — implicit acceptance of HOLDS-AS-DOCTRINE for the core principle text (§ 4 sub-clauses 1-5).

### Comparison to established doctrines

Per QUESTION.md Q3, external-scholar's comparison axis: SemVer, Linux stable ABI, Rust stability/edition system.

- **Schema declaration + versioning + bump procedure** (§ 4 sub-clauses 1, 3) ≈ SemVer + Rust edition system.
- **Mechanical CI enforcement** (§ 4 sub-clause 2, C1-C6) ≈ Linux stable-ABI testsuite.
- **Cross-product consumer contracts** (§ 4 sub-clause 4, C3) ≈ Linux's "syscall contract" + consumer-side fixture discipline from Rust crates that test against multiple downstream consumers.
- **Display-text non-stability rule** (§ 4 sub-clause 5) ≈ "implementation details are not part of the stable surface" pattern recognized across all three reference doctrines.

The principle is recognizable as the same kind of artifact. external-scholar's surviving R2 ("Streamline changelog to essential fixes only") and modified R1 ("Extract §§12-13 process archaeology") are tightening recommendations, not doctrinal-rewrite signals.

### Per-axis findings

1. **Five-point doctrinal unity:** The five sub-clauses do hang together — they constitute the discipline (declare → enforce → version → cross-product consume → declaration-scope rule). external-scholar's proposed unifying statement (*"Persistence contracts are themselves stable interfaces subject to the same discipline as runtime interfaces"*) is already implicit in § 4's opening sentence: *"Persistent on-disk state is itself a stable interface."* A minor E-condition could promote that opening to a single-sentence preamble.

2. **Universality at Tier 2:** Genuinely universal within the conversus suite. § 3 non-goals explicitly disclaims cross-suite scope. § 8 Inclusion Criteria gate ✅ for Tier 2.

3. **§ 11 (override-precedent scope restriction):** external-scholar concluded this is "a binding procedural rule that creates ongoing obligations" and should be preserved in the spec. Holds as doctrine.

4. **§ 12 (compound constitutional debt):** external-scholar flagged as historical self-flagellation. The text *does* document past governance failures (v2 tier overreach + v2 override invocation). However, § 12's closing paragraph ("Methodological lesson") establishes a forward-binding constraint: *"self-consistency verification's default-defend-status-quo posture is **load-bearing**."* That sentence is doctrinal, not archival.

5. **§ 13 (methodological lessons):** The 8 numbered items in § 13 are explicitly framed as "binding on all future amendments." They create ongoing obligations, not historical record. § 13 is forward-prescriptive doctrine.

### Ruling

The spec holds as constitutional doctrine. external-scholar's strongest critique — that §§12-13 read as deliberation record — is partially fair for § 12's narrative paragraphs (the v2-history exposition) but does not survive scrutiny of § 12's closing "Methodological lesson" and § 13's eight binding constraints. The doctrinally-integral portions outweigh the archival portions.

A single tightening E-condition is warranted:

- **E4 (optional, doctrinal):** add a single-sentence preamble to § 4 promoting the discipline's unifying claim: *"Principle XXVIII: persistence contracts ARE stable interfaces, subject to the same discipline as runtime interfaces under Principle II."* This makes the doctrinal frame explicit for external readers.

**Q3 verdict: PARTIALLY-COHERENT.** E-condition E4 tightens doctrinal framing without doctrinal rewrite. The principle reads as legitimate constitutional doctrine, not as compromise record.

---

## Critical Unresolved Tensions

The Phase 5 synthesis flagged three tensions. Ruling on each:

1. **Timeline Feasibility vs. Specification Completeness.** **Post-ratification operational concern, not ratification-blocking.** C8's Remediation-Blocked + mandatory-follow-up-amendment mechanism is the spec's answer. risk-auditor's checkpoint-discipline recommendation is sensible operational hygiene to apply during execution but does not need to be in the spec text.

2. **Constitutional Scope vs. Follow-on Work.** **Resolved by D2 + § 3 non-goals.** Spec v4 cleanly delineates: in-scope = persistence-contract discipline at Tier 2 for products existing at ratification; out-of-scope = retroactive cross-suite extension, XML-mandate-for-conversus-outputs, spec-kit-orc's state-files reconciliation (its own follow-on), suite-admission-criteria update for new siblings. No ratification-blocking gap.

3. **Cross-Product Integration Specificity.** **Resolved by E2 (sub-clause 5 declaration mechanism) plus § 4 sub-clause 4's existing consumer-side fixture requirement (C3).** The remaining specificity questions — exact CONSUMER-CONTRACT.md schema, exact fixture format — are appropriately delegated to per-product implementation guidance per implementation-engineer's "Separate Constitutional Doctrine from Implementation Guidance" recommendation. Constitutional text carries the discipline; per-product guidance carries the mechanics.

None of the three tensions blocks ratification.

---

## Combined disposition

- **Q1:** IMPLEMENTABLE-WITH-CLARIFICATIONS (E1, E2, E3)
- **Q2:** MODERATE-RISK-MANAGEABLE
- **Q3:** PARTIALLY-COHERENT (E4)

All three are PASS-variants. Per QUESTION.md "Arbiter ruling format" and spec § 9.4 / § 9.5: **PROCEED TO RATIFICATION** with E-conditions E1-E4 applied to produce spec v5. Spec v5 is then ratified via SIR + governance log + spec status entries.

### E-conditions (applied to produce spec v5)

- **E1** (Q1): § 4 sub-clause 3 — add `schema_version` format requirement (SemVer or documented alternative with explicit total-ordering semantics).
- **E2** (Q1): § 4 sub-clause 5 — add explicit-declaration mechanism (declaration appears in the producer's `CONSUMER-CONTRACT.md` or equivalent declared canonical doc, naming the specific display-text surface and its stability guarantee).
- **E3** (Q1): § 4 sub-clause 1 — add "discoverable location" criteria (repo root + suite-convention naming + linked from top-level README/CLAUDE.md).
- **E4** (Q3): § 4 preamble — add unifying doctrinal statement linking Principle XXVIII to Principle II.

### Post-ratification operational guidance (not spec v5 changes)

- risk-auditor's phased compliance checkpoints (2026-09-01 + 2026-10-15) and capacity-feasibility assessment are accepted as operational guidance products may voluntarily commit to in their CONFORMANCE.md Provisional rows. Not binding under the spec text.
- implementation-engineer's recommendation to maintain authoritative implementation guidance documents (cross-product format compatibility, error message standards, validation checklists) is accepted as a suite-level follow-on under spec § 6.6 (suite docs).

---

## Ruling lines

- **Q1 RULING: IMPLEMENTABLE-WITH-CLARIFICATIONS** — four agents converged unanimously on three wording-level gaps (schema_version format, explicit-declaration mechanism for sub-clause 5, discoverable-location criteria for sub-clause 1); E1-E3 close each in a single sentence.
- **Q2 RULING: MODERATE-RISK-MANAGEABLE** — C1-C8 + D1-D4 adequately mitigate the identified worst-case axes (missed-deadline cascade is bounded by C8's structured Remediation-Blocked + mandatory follow-up amendment mechanism; forward-sibling friction resolved by D2 temporal scope; no retroactive precedent-audit cascade per D4 scope).
- **Q3 RULING: PARTIALLY-COHERENT** — the principle holds as constitutional doctrine recognizable alongside SemVer / Linux stable ABI / Rust stability; E4 tightens doctrinal framing by promoting the spec's existing unifying claim ("persistence contracts ARE stable interfaces") to a Principle XXVIII preamble.

**Combined disposition: PROCEED TO RATIFICATION.** Apply E1-E4 to produce spec v5; ratify v5 via SIR (Tier 2 Version 1.0.0 → 1.1.0), governance log entry in `build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md`, and spec status flip to `Ratified`.
