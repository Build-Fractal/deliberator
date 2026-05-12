# Arbitration Ruling — v4.1.0 Persistence Contract Discipline Originating Deliberation

**Arbiter:** v4.1.0-persistence-originating-arbiter (preset: `role/balanced-arbiter`)
**Grounding:** `build-fractal/CONSTITUTION.md` Tier 1 Principle II + `specs/v4.1.0-persistence-contract-discipline/spec.md` § 4
**Trigger:** `disputes_remain`. Two substantive disputes survive Phase 4 (Dispute A — schema format strictness; Dispute B — deadline mechanism). Per `conversus.yml`, this ruling is **binding**.
**Stage:** Phase 6 (Arbitration) — produced manually after Phase 5 engine crash. See Recovery Note below.

---

## Recovery Note

This arbitration was produced manually on 2026-05-12 after the Phase 5 synthesizer crashed with `RateLimitError: Anthropic rate limit exceeded after 3 attempts: Error code: 429` at `01:17:35`. The inputs to this manual arbitration are identical to those Phase 5 → Phase 6 would have consumed: the four agents' `revision_2.md` files (Phase 3 iteration 2 final positions) and `disputes.md` files (Phase 4 dispute consolidation), plus the spec under deliberation, Tier 1 Principle II grounding text, and QUESTION.md. The companion manual synthesis (`summary/final.md`) was produced in the same recovery operation; this arbitration is grounded in those same inputs, not in the synthesis document itself, so any synthesis bias does not propagate. No new agent rounds were run; no positions invented.

---

## Constitutional grounding

Tier 1 Principle II current text (CONSTITUTION.md L84-113) governs **stable interfaces** abstractly: structural markers, template variables, the dispute-parsing subsystem, preset schema, reference file paths, and the dispatch table. The principle is **list-based** today — it enumerates which named surfaces are stable and what changes count as breaking. It does **not** today address the persistence surface specifically.

Spec § 4 proposes a five-point sub-clause appended below the existing bullet list:
1. Declared schema (with `schema_version`).
2. Mechanical enforcement (CI gate; format product-choice).
3. Versioning (documented bump procedure).
4. Cross-product consumer contracts (CONSUMER-CONTRACT.md at producer root).
5. Declaration scope (display text is not a stable contract unless explicitly declared).

The amendment is **MINOR** per the pathway taxonomy: it appends normative content to existing Principle II without removing or renaming any principle. Verification protocol per spec 067 still requires originating + self-consistency + blind — this ruling closes the originating stage.

---

## Q1 — Constitutional Inclusion Criteria gate

Spec § 8 claims the amendment passes universal applicability, mechanical verifiability, and non-redundance.

### Findings from the four agents

The strongest *available* Q1 BLOCK argument was devils-advocate's Phase 1 Recommendation 3: "Split this into a separate Principle XXIX with its own inclusion criteria review because five detailed sub-points constitute a principle, not a sub-clause." In revision_2.md the devils-advocate **withdrew** that recommendation: *"the attachment to Principle II (Stable Interfaces) is conceptually coherent — persistent state is indeed a type of interface that requires stability."* No other agent picked up the challenge in cross-review. This forecloses the cosmetic-attachment attack vector.

The pragmatist's Q1 posture is APPROVE-WITH-FIXES — their disposition table treats principle adoption as given and concentrates recommendations on tightening mechanics (Recommendations 1, 4, 5, 7; new recommendations on bidirectional drift detection and gate placement). Their Recommendation 4 (graduated enforcement with 30-day warning periods) was **withdrawn** after ci-expert pointed out that advisory enforcement defeats mechanical verifiability. That withdrawal is the pragmatist effectively conceding the mechanical-verifiability prong of Q1, which was the most cost-sensitive concern shippability-wise.

Persistence-expert and ci-expert hold APPROVE-WITH-FIXES on Q1 (inferred from their domain-expertise findings, which uniformly sharpen mechanical verifiability rather than oppose it). 3 of 4 explicitly support APPROVE-WITH-FIXES; ci-expert's position on Q1 is implicit — inferred from their CI-readiness focus and absence of any challenge to the Inclusion Criteria gate itself.

### Grounding check against Tier 1 Principle II

The existing Principle II bullet list (CONSTITUTION.md L91-113) treats stability through a **named-surfaces** approach — each surface gets a paragraph declaring what's stable and what counts as a breaking change. The proposed sub-clause continues exactly this pattern for the persistence surface: it names what must be declared (schemas with version fields), what counts as breaking (silent format changes; consumption of undeclared internals; display-text parsing), and what the discipline scope is. The structural fit with Principle II is genuine, not cosmetic.

Universal applicability is supported by spec § 1's motivating evidence — every Build Fractal product writes persistent state by definition of being a product, and the two confirmed gaps (conversus output parse contract in display text; spec-kit-orc declared-but-drifted state-files) demonstrate the principle applies and bites in the live ecosystem. Mechanical verifiability is the prong all four agents focused on tightening but none rejected; the sub-clause **mandates** mechanical enforcement by text. Non-redundance is established by the fact that existing Principle II bullets enumerate specific named surfaces (markers, dispatch table, preset schema, file paths) but do **not** mention persistent on-disk state as a class — the sub-clause is the operational definition for a surface category the current principle leaves abstract.

### Conditions emerging from Q1

Per the Phase 4 unanimous convergences, the spec text needs these tightenings before self-consistency verification can run cleanly. These are all engineering fixes to mechanical verifiability, not gate-failing concerns:

- **C1 — Bidirectional drift detection.** Sub-clause 2 currently mandates only forward validation (artifacts written conform to schema). Append a requirement that schema *changes* are validated against existing producer code — i.e., the producer can still emit conformant artifacts after a schema edit. All four agents converged on this in Phase 3-4.

- **C2 — Pre-merge gate placement.** Sub-clause 2 is silent on whether the CI gate runs as PR-required, post-merge, or advisory. Spec § 4 must mandate **PR-required / merge-blocking**. Ci-expert's surviving Recommendation 1; unanimous adoption in cross-review.

- **C3 — Consumer-side contract validation fixtures.** Sub-clause 4 mandates consumers consume declared surfaces but does not specify the enforcement mechanism. Spec § 4 sub-clause 4 must add: consumers SHIP test fixtures pinning consumed surfaces and validated in *consumer* CI. This addresses devils-advocate's enforceability objection through persistence-expert's resolution — accepted by all four agents.

- **C4 — Schema surface coverage.** Sub-clause 1's mandate of "field names, types, structural requirements" implicitly assumes a field-based schema shape. Spec § 4 must extend coverage to JSONL streaming (line semantics), positional formats, binary formats, and hybrid YAML-frontmatter-plus-markdown. Spec-kit-orc's `state-files.md` already uses two of these formats; coverage gaps would undermine the universal-applicability claim. Persistence-expert + ci-expert bilateral; pragmatist and devils-advocate did not object.

### Ruling

**Q1: APPROVE-WITH-FIXES.** Conditions C1-C4 above must be applied to produce spec v2 before self-consistency verification runs. The Inclusion Criteria gate clears: universal applicability is supported by the cross-product audit evidence; mechanical verifiability is mandated by sub-clause 2 (sharpened by C1-C2); non-redundance is established by the named-surface pattern in existing Principle II not addressing the persistence-surface category. The strongest available BLOCK argument (the new-principle-in-disguise attack) was raised, cross-reviewed, and withdrawn by the originating agent.

---

## Q2 — Schema-format flexibility

Spec § 3 non-goals: "Product implementations choose XSD, JSON Schema, Pydantic, AST-validator, or any other mechanical schema language. The amendment mandates that SOME mechanical enforcement exists." Spec § 4 sub-clause 2: "Schema format is product-choice ... or any other format with a deterministic conformance check. Schemas declared without enforcement do not satisfy this discipline." Spec § 10 condition C1 named the prose-loophole risk in the draft itself.

### Findings from the four agents

This is the question with the most surviving disagreement. The split is 3-of-4 vs. pragmatist.

**Pragmatist (REJECT-FLEXIBILITY):** Non-negotiable per disputes.md — mandate JSON Schema, XSD, or Pydantic only. Their argument: even strengthened wording ("machine-executable validation with binary pass/fail") leaves a creative-interpretation loophole. A validator returning `pass` for any artifact containing the declared field names technically satisfies the wording while providing no actual enforcement.

**Devils-advocate, persistence-expert, ci-expert (APPROVE-WITH-FIXES):** Three independent technical arguments converge on preserving format choice while tightening wording:

1. **Spec non-goal contradiction.** Mandating technologies contradicts spec § 3's explicit non-goal — the spec was *drafted* with format choice as a deliberate design property.

2. **Format does not equal validation strength.** Ci-expert in disputes.md: "a poorly written JSON Schema can still accept 'any valid JSON' just as easily as prose documentation. The enforcement gap exists in validation implementation, not format choice." Technology mandate does not actually close pragmatist's gaming concern.

3. **Non-field-format coverage.** The Build Fractal ecosystem already uses formats (JSONL streaming logs in spec-kit-orc `.orchestrator/`, YAML-frontmatter-plus-markdown specs) where field-based schema languages (JSON Schema, Pydantic) fit poorly. Mandating those formats forces suboptimal validation for surfaces that already exist.

The persistence-expert's substitute wording — "machine-executable validation with binary pass/fail result that verifies field presence, types, and value constraints, excluding prose descriptions, manual checklists, or subjective interpretation" — is endorsed verbatim by ci-expert and accepted by devils-advocate (modified Recommendation 2 in revision_2.md).

### Override-with-rationale precedent check

The pragmatist's strict reading, if applied uniformly, would shrink the spec's deliberately drafted flexibility (§ 3 non-goal). Per the established override-with-rationale precedent (memory `feedback_amendment_override_precedent.md`), when a strict reading of one agent's position would shrink existing ratified-or-drafted scope, the correct response is **override with rationale logged**, not iterate or demote the strict-reading agent.

Here the rationale is multilayered: (a) three independent technical experts converge against the strict reading on different grounds (non-goal preservation, format-strength decoupling, non-field-format coverage); (b) the substitute wording closes the loophole pragmatist correctly identified, addressing the substantive concern without the strict-reading remedy; (c) the spec's non-goal § 3 represents a prior design decision the originating deliberation does not have the standing to overturn without stronger evidence than one agent's disputed position.

### Grounding check against spec § 4 sub-clause 2

The drafted text already attempts to close the prose-loophole with "deterministic conformance check." The four agents agree this is too weak. The fix is to replace that phrase with the persistence-expert's stronger wording. The format-choice property is preserved; the gaming vector is closed by precise wording.

### Conditions emerging from Q2

- **C5 — Strengthen conformance wording.** Replace spec § 4 sub-clause 2 phrase "any other format with a deterministic conformance check" with: "any other format whose conformance check is machine-executable, produces a binary pass/fail result with specific failure descriptions, and verifies field presence, types, and value constraints — explicitly excluding prose descriptions, manual checklists, and subjective interpretation."

- **C6 — Worked-example test fixtures.** To pre-empt the validator-that-only-checks-field-names loophole pragmatist raised, spec § 4 sub-clause 2 should require each product's CI gate to ship with at least three test fixtures: (a) a known-conformant artifact that validation passes, (b) a known-non-conformant artifact with a missing required field that validation fails on, (c) a known-non-conformant artifact with a wrong field type that validation fails on. This is mechanically verifiable (the fixture pair must exist in the repo) and forecloses the "validator returns pass for anything containing field names" gaming scenario without technology mandate.

### Ruling

**Q2: APPROVE-WITH-FIXES.** Format flexibility is preserved per spec § 3 non-goal. Conditions C5-C6 close the prose-loophole pragmatist correctly identified by tightening wording and mandating worked-example fixtures, rather than restricting to JSON Schema / XSD / Pydantic. The pragmatist's strict reading is overridden with rationale (this paragraph + the substantive arguments in disputes.md from three other agents).

---

## Q3 — 2026-09-01 deadline realism

Spec § 2 goals 3-5 assign 2026-09-01 to three remediation tracks: conversus-oss structured output + V un-xfail; conversus-enhanced schema enforcement on stateful artifacts; spec-kit-orc state-files reconciliation + `bin/validate-state.sh`. Spec § 10 condition C3 flagged this as needing operational-feasibility confirmation.

### Findings from the four agents

No agent backs the spec as drafted.

**Pragmatist (APPROVE-WITH-EXTENSION):** Differentiated dates per cross-product coordination analysis — 2026-12-01 for conversus (structured-output migration plus spec-kit-orc adapter rewrite is the cross-product dependency that drives schedule risk); 2026-09-01 for spec-kit-orc (self-contained reconciliation, no cross-product coordination).

**Devils-advocate:** Reject the fixed-deadline mechanism entirely; require products to declare their own compliance paths and timelines. Their disputes.md non-negotiable: fixed dates create missed-deadline authority erosion no matter how the dates are set.

**Persistence-expert:** Did not vote on Q3 explicitly in revision_2.md or disputes.md. Their Recommendation 7 (cross-repository schema coordination protocols) and the recurring "coordination complexity" theme tacitly support pragmatist's extension. Position **inferred from absence of objection**: APPROVE-WITH-EXTENSION compatible.

**Ci-expert (APPROVE-WITH-EXTENSION):** Modified Recommendation 4 explicitly adopts pragmatist's differentiated timeline and explicitly rejects devils-advocate's mechanism — "Enforcement without consequences creates compliance theater. The devils-advocate's approach allows products to declare indefinite 'transition plans' without accountability."

### Grounding check against spec § 4 and § 10

Sub-clause 2 mandates mechanical enforcement; sub-clause 4 mandates cross-product consumer contracts. The conversus structured-output remediation is *itself* the proof of concept for both sub-clauses (a structured XML schema with XSD CI gate, plus the spec-kit-orc adapter consuming it via CONSUMER-CONTRACT.md). If that remediation slips past its deadline, the first product to test the new principle is in violation of the new principle — which is exactly the missed-deadline authority erosion both pragmatist and devils-advocate worry about, from opposite directions.

The pragmatist's differentiated approach handles this by recognizing the cross-product dependency: conversus structured output → spec-kit-orc adapter rewrite is a two-product coordination problem with serial dependency. Spec-kit-orc's *own* state-files reconciliation is independent of the conversus migration. Splitting the deadlines per dependency structure produces a schedule consistent with the engineering reality.

The devils-advocate's mechanism critique has substance — fixed deadlines do erode authority when missed — but ci-expert's counter is decisive: self-declared timelines produce the same erosion through a different vector (indefinite transition states). The mechanism trade-off favors fixed dates with concrete consequences over self-declared timelines without accountability, conditional on the dates being engineering-realistic, which the pragmatist's differentiation achieves.

### Conditions emerging from Q3

- **C7 — Differentiated remediation deadlines.** Update spec § 2 goals 3-4 (conversus-oss + conversus-enhanced) to deadline **2026-12-01**, reflecting cross-product coordination complexity with spec-kit-orc adapter. Preserve spec § 2 goal 5 (spec-kit-orc state-files reconciliation) at **2026-09-01**, reflecting its self-contained scope. Update the matching CONFORMANCE.md Provisional rows in spec § 6.2 / § 6.3 / § 6.4.

- **C8 — Missed-deadline consequence specified.** Per ci-expert's surviving Recommendation 4, spec § 10 must specify that products missing their differentiated deadline transition to a named status (e.g., "Remediation-Blocked") with a documented escalation path, not an indefinite transition state. This addresses devils-advocate's authority-erosion concern by making the consequence mechanically determinable rather than ambiguous.

### Ruling

**Q3: APPROVE-WITH-EXTENSION.** Adopt pragmatist's differentiated dates (2026-12-01 conversus-oss + conversus-enhanced; 2026-09-01 spec-kit-orc) per condition C7. Add missed-deadline consequence specification per condition C8. The devils-advocate's self-declared-timeline mechanism is rejected on the ground that it allows indefinite transition states (ci-expert's accountability argument); the substantive missed-deadline authority concern is addressed by C8 rather than by mechanism change.

---

## Combined disposition

All three questions APPROVE-variant. Per QUESTION.md combined disposition rules:

> All three APPROVE (any variant): proceed to self-consistency verification with any specified fixes applied to produce spec v2.

Conditions C1-C8 populate spec § 10. Spec v2 applies these fixes and proceeds to the self-consistency verification stage per spec § 9.2.

The spec § 10 placeholder conditions (C1 schema-format-loophole, C2 cross-product enforceability, C3 deadline feasibility) are **superseded** by this ruling's C1-C8. Note the numbering collision: spec § 10's draft C1/C2/C3 are now superseded by this ruling's C1-C8. Renumbering is editorial and happens in the spec v2 edit, not here.

## Per-agent disposition handling

- **Pragmatist's non-negotiable on Q2 (technology mandate):** overridden with rationale (Q2 ruling above). The substantive gaming concern that motivated the non-negotiable is addressed by C5 + C6.

- **Pragmatist's non-negotiable on Q3 (differentiated extension):** accepted (Q3 ruling above; C7).

- **Devils-advocate's non-negotiable on Q3 (self-declared timelines):** rejected on accountability grounds (Q3 ruling above). The substantive authority-erosion concern is addressed by C8.

- **Devils-advocate's non-negotiable on enforcement-mechanism specification:** accepted as the cluster C1-C3 (bidirectional drift detection, pre-merge gate placement, consumer-side validation fixtures) — these collectively constitute the enforcement mechanism specification devils-advocate demanded.

- **Persistence-expert's non-negotiables (bidirectional drift detection, schema surface coverage, consumer-side validation fixtures):** all accepted (C1, C4, C3).

- **Ci-expert's non-negotiables (pre-merge gate placement, bidirectional drift detection, binary pass/fail validation results):** all accepted (C2, C1, C5).

Every non-negotiable from the disputes.md files except pragmatist's Q2 technology mandate is preserved in conditions. The override-with-rationale precedent is invoked exactly once, on Q2, with full rationale logged here.

---

## Ruling lines

- `Q1 RULING: APPROVE-WITH-FIXES — Inclusion Criteria gate passes; conditions C1-C4 tighten mechanical verifiability before self-consistency verification.`
- `Q2 RULING: APPROVE-WITH-FIXES — format flexibility preserved per spec § 3 non-goal; conditions C5-C6 close the prose-loophole via wording strengthening and worked-example fixtures rather than technology mandate.`
- `Q3 RULING: APPROVE-WITH-EXTENSION — differentiated deadlines (2026-12-01 conversus-oss + conversus-enhanced; 2026-09-01 spec-kit-orc) per C7; missed-deadline consequence specified per C8.`
