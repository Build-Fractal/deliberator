# v4.2.0 Originating Deliberation — Arbitration Resolution

**Stage:** Originating (stage 1 of 3)
**Date:** 2026-05-13
**Agents:** engineer, schema-design-expert, adapter-consumer, devils-advocate
**Spec under review:** `specs/v4.2.0-structured-deliberation-outputs/spec.md` (v1 / draft)
**Constitutional grounding:** Tier 2 `build-fractal/conversus/CONSTITUTION.md` Principle XXVIII (L490-644), ratified 2026-05-12 in commit `551f647`.

---

## Process Note

This arbitration was produced **manually** because the Phase 6 arbiter dispatch did not fire. The Phase 5 synthesis labelled its disputes section "Remaining Disputes" rather than emitting the engine's expected `DISPUTES_BEGIN`/`DISPUTES_END` markers (or the `<disputes>` structural element that this very spec proposes to mandate). This is the **same class of trigger miss** that hit the v4.1.0 blind verification arbitration on 2026-05-12 — engine quirk: grep-based dispute detection against non-canonical synthesizer prose. Manual arbitration was produced from the Phase 3-iter-2 `revision_2.md` positions, Phase 4 `disputes.md` final positions, and the Phase 5 synthesis (which produced an unusually rich recommendation scorecard and convergence map).

**Pedagogical observation (load-bearing for Q2).** The very deliberation tasked with verifying v4.2.0's schema-standardization proposal *just hit, in real time, the exact bug v4.2.0 proposes to fix.* Bug C in spec § 1.1 reads: *"the v4.1.0 blind-verification synthesis used 'Critical Unresolved Tensions' terminology where the engine grep-matches for `DISPUTES_BEGIN`/`DISPUTES_END` markers. Arbiter didn't fire even though tensions existed; manual arbitration was required."* The v4.2.0 originating deliberation reproduces this failure: the Phase 5 synthesizer wrote "Remaining Disputes" rather than the grep-recognized marker pair, and the Phase 6 trigger silently missed. Under the spec's proposed XML schema, the trigger becomes `count(synthesis/disputes/dispute) > 0` (spec § 1.1, § 4.6) — a structural check that cannot be evaded by prose drift. This is concrete real-time evidence — not hypothetical — that the spec's structural-detection thesis is correct.

---

## Decision Framework

Default posture per spec 067 originating-deliberation methodology: **defend-status-quo for the spec under review**. The originating arbiter rules on whether the spec — as drafted, with the four agents' surfaced gaps — is feasible (Q1), schema-adequate (Q2), and correctly tier-placed (Q3).

Constitutional grounding: Tier 2 Principle XXVIII (L490-644) mandates declared schemas, mechanical CI enforcement, `schema_version` (SemVer), `CONSUMER-CONTRACT.md` on producer side, and explicit declaration of display-text contracts. Sub-clause 2's "schema declaration without mechanical enforcement is itself a violation" is the load-bearing enforcement clause that drives Q1's validator-write-time-vs-CI question. The 2026-12-01 universal remediation deadline is constitutionally binding and was not contested by any agent in their final positions (the two timeline-relief recommendations — engineer Rec 7 and various deferral proposals — were withdrawn on cross-review per the synthesis Key Concessions).

Schema definitions evaluated against spec § 4 sub-sections 4.1-4.8 and § 5.1's `engine/schema_validator.py` requirement.

---

## Q1 — Implementation feasibility

**Question (QUESTION.md):** Can the proposed schema + validator + template migration + downstream-consumer migration realistically land within the 2026-12-01 deadline that Principle XXVIII binds conversus-oss to?

### Agent positions

**engineer** (`revision_2.md`, `disputes.md`): Concluded migration is feasible within deadline conditional on (a) JSON Schema as canonical format (Rec 1 surviving, unanimous support), (b) early performance testing to establish a <100ms per-output validation budget before locking validation scope (Rec 2 modified), (c) dependency-ordered template migration: review → cross-review → revision → disputes → synthesis → arbitration (Rec 3 surviving, unanimous). **Withdrew** the validation-fallback mechanism (Rec 4) — conceded that Principle XXVIII's mechanical-enforcement clause forbids advisory validation. **Withdrew** the 3-month deadline extension (Rec 7) — conceded the deadline is constitutionally binding and requires formal amendment, not spec-level negotiation.

**schema-design-expert** (`revision_2.md`): Modified 7 of 9 recommendations under timeline pressure. New P1 "Timeline-constrained schema staging" — basic structural validation by 2026-12-01 for constitutional compliance, advanced features (cross-reference integrity, full constraint validation) deferred to v0.2.0/v1.1.0 after performance validation. The timeline IS achievable if scope stages.

**adapter-consumer** (`revision_2.md`): New P1 "Phase consumer protections" — phased rather than comprehensive consumer protection from day one. Withdrew format-discovery and validation-failure-artifact recommendations as obviated by JSON Schema convergence. The orchestrator (formerly spec-kit-orc) adapter migration is the load-bearing downstream-consumer risk; new P1 demands the arbiter resolve format choice in Q2 before consumer migration planning detailed-design proceeds (since XML vs JSON have *completely different* tooling stacks — xmllint/lxml vs ubiquitous shell parsing).

**devils-advocate** (`revision_2.md`): Withdrew the fundamental scope challenge (targeted fixes vs comprehensive schema) after cross-review evidence demonstrated display-text contract drift is systemic, not three isolated bugs. New P1 "Coordinate dependency-ordered migration" supports engineer's sequencing. Maintains rollback-mechanism recommendation (Rec 7 surviving) as production-safety escape hatch.

### Per-axis findings

1. **Schema scope boundedness.** Six output types × per-type body schemas × common envelope. The synthesis records *zero* dissent on whether the scope is bounded; all four agents engaged with concrete schema fragments without claiming the surface is undefinable. Bounded.

2. **Validator runtime cost.** Engineer's <100ms-per-output budget (Rec 2 modified) was acknowledged by schema-design-expert; bilateral convergence. The synthesis's recommended resolution — tiered validation, with basic structural validation at write-time and advanced validation (cross-references, complex constraints) deferred to a separate CI-time phase — is operationally sound and respects Principle XXVIII's mechanical-enforcement mandate (basic write-time validation IS mechanical enforcement; CI-time advanced validation is *also* mechanical enforcement, just at a different gate). Feasible.

3. **Template migration.** Engineer Rec 3 + devils-advocate New P1: dependency-ordered migration (review → cross-review → revision → disputes → synthesis → arbitration) with one-mode pilot before rollout. Unanimous support. Feasible.

4. **Adapter (orchestrator) migration.** Spec § 6.2 already provides for parallel-format support during the migration window (§ 11.1: engine reads both formats; spec-kit-orc adapter supports both formats). Adapter-consumer's New P1 "Phase consumer protections" aligns with this. Feasible **provided** format choice resolves cleanly in Q2 (since XML vs JSON tooling stacks are non-interchangeable).

5. **OQ2 (validator format).** This is the load-bearing Q1↔Q2 coupling. The synthesis records **unanimous convergence on JSON Schema preference** across all four agents reaching the same conclusion through independent analytical frameworks — XML syntax conflicts with agent prose (`<`, `>`, `&` characters require CDATA escaping; spec § 4 has no CDATA strategy), Python ecosystem integration, validation error message quality, consumer tooling ubiquity. The spec's strawman is XSD with "product-choice with XSD default" framing (§ 3 non-goals; § 5.1 strawman). All four agents say that framing does not hold up against the technical evidence.

6. **OQ3 (companion MD renderer).** Spec § 5.2 strawmans Python renderer over XSLT. No agent challenged this. Settled.

7. **OQ4 (deprecation cliff date).** Spec § 11.7 proposes 2026-12-01 alignment with Principle XXVIII deadline. The synthesis's "Constitutional Deadline Non-Negotiability" convergence (unanimous) confirms 2026-12-01 stands. The two timeline-relief proposals were withdrawn. Settled.

### Ruling

Implementation is feasible within the constitutional deadline. The agents converged on three load-bearing fixes: format change (XSD → JSON Schema), tiered validation (basic at write-time, advanced at CI-time), and dependency-ordered template migration. The orchestrator-side adapter risk is real but is bounded by spec § 11.1's parallel-format window and adapter-consumer's phased-protection framework.

**Q1 verdict: APPROVE-WITH-FIXES.** Conditions to apply to produce spec v2:

- **C1 (P1):** § 4 + § 5.1 — switch canonical format from XML+XSD to **JSON Schema**. Update all six body-schema definitions and the common envelope to JSON Schema syntax. Update § 3 non-goals to remove the "XSD strawman" framing. (Sources: engineer Rec 1 surviving, schema-design-expert Rec 1 modified, adapter-consumer New P1, devils-advocate New P1 — unanimous P1 convergence.)
- **C2 (P1):** § 5.1 — establish **<100ms per-output validation performance budget** for write-time validation with early performance testing to fix scope before commitment. (Sources: engineer Rec 2 modified, schema-design-expert acknowledgment — bilateral.)
- **C3 (P1):** § 11 — specify **dependency-ordered template migration**: review → cross-review → revision → disputes → synthesis → arbitration, with one-mode pilot. (Sources: engineer Rec 3 surviving, devils-advocate New P1 — unanimous.)
- **C4 (P1):** § 11.1 — explicitly enumerate **semantic equivalence testing** as a CI gate during the migration window: structured-parsed verdicts must match grep-extracted verdicts on all historical arbitration outputs. (Sources: engineer Rec 5 surviving, adapter-consumer Rec 6 surviving, devils-advocate acknowledgment — unanimous.)
- **C5 (P2):** § 11 — adopt **tiered/staged implementation**: v1.0.0 basic structural validation by 2026-12-01, advanced features (cross-reference integrity, full constraint validation) in v1.1.0 after performance validation. (Sources: schema-design-expert New P1.)

---

## Q2 — Schema design adequacy

**Question:** Does the proposed XML schema correctly cover the six output types' structural needs, and does the arbitration schema specifically address the Phase 6 `disputes_remain` trigger bug?

### Agent positions

**schema-design-expert** (`revision_2.md`): The agent whose mandate is Q2. Confirmed the structural design — common envelope plus per-type bodies — is sound. Surviving Rec 2 demands three additional required envelope fields: `deliberation_stage`, `engine_version`, `source_commit`, citing audit-trail completeness gaps. Modified Rec 3 splits field-level validation (length bounds, non-empty content) into v1.0.0 basics vs v1.1.0 advanced under performance pressure. Surviving Rec 8 confirms CDATA-style encoding concerns are real (and dissolve under JSON Schema). Surviving Rec 9 specifies a validator error-object schema (`field_path`, `error_code`, `human_message`).

**engineer** (`revision_2.md`): Concurs with schema-design-expert on identity fields and validator error format. Surviving Rec 5 (round-trip consistency testing) directly tests whether the schema preserves semantic content across re-renders.

**adapter-consumer** (`revision_2.md`): Surviving Rec 2 (version discovery mechanism), surviving Rec 4 (consumer fixture update procedure), surviving Rec 6 (semantic equivalence testing) — all about consumer-side adequacy of the schema's evolution surface.

**devils-advocate** (`revision_2.md`): Surviving Rec 7 (rollback mechanism) and the schema-versioning dispute (1.0.0-rc.1 vs 0.x namespaces). The synthesis ruled on this dispute: 1.0.0-rc.1 wins because Principle XXVIII deadline requires production-ready stability signals, not experimental schemas.

### Per-axis findings

1. **Common envelope completeness.** The spec § 4.1 envelope (`schema_version`, `output_type`, `agent_name`, `deliberation_id`, `phase_iteration`, `timestamp`, `target_files`) is **incomplete** per schema-design-expert Rec 2 (majority-supported, no challenge): `deliberation_stage` (originating / self-consistency / blind), `engine_version`, and `source_commit` are missing. The v4.1.0 blind-verification audit-trail re-rendering test case would lose stage identity and engine-version provenance under the current envelope.

2. **Per-type body schemas — arbitration in particular.** Spec § 4.7's `<arbitration>` body — with `<per_question_rulings>` containing per-question `<verdict>`/`<rationale>`/`<conditions>` AND the denormalized `<ruling_lines>` projection — is **structurally adequate** for the load-bearing use case. The denormalized `<ruling_lines>` block is explicit adapter-convenience accommodation (spec § 4.7: *"exists for adapter convenience — spec-kit-orc currently grep-extracts one-line ruling summaries and benefits from a flat list"*); validator enforces consistency between the two representations. This design correctly anticipates adapter migration costs.

3. **Synthesis `<disputes>` element.** Spec § 4.6 (`<synthesis>`) declares `<disputes>` as a structural element with `<dispute>` children — making `count(synthesis/disputes/dispute) > 0` (the proposed structural trigger replacement, per § 1.1 Bug C) operative. **This is the load-bearing structural fix for Bug C.** It is concretely correct as drafted. Real-time evidence supporting this finding: *this very arbitration is being produced manually because Phase 6 didn't fire on a synthesizer who wrote "Remaining Disputes" instead of the engine-expected marker pair.* Under the proposed schema, that phrasing variation cannot evade the structural trigger.

4. **Schema versioning.** Spec § 4.8 maps SemVer cleanly to MAJOR (removed elements / removed enum values / type narrowing), MINOR (added optional elements / added enum values / new output types), PATCH (clarifying restrictions). Schema-design-expert Rec 6 modified adds the consumer-impact qualification (some renames break consumers without being technical breaking changes). Sound design; small refinement needed.

5. **Schema format choice (OQ2).** The synthesis's unanimous P1 convergence — JSON Schema over XML+XSD — is the dominant Q2 finding. The convergence rests on technical merits, not stylistic preference: XML's CDATA-escaping burden on agent prose containing `<`, `>`, `&` characters; JSON Schema's Python `jsonschema` library being a near-universal dependency; JSON Schema's superior validation error messages; ubiquitous shell-tool parsing (`jq`) vs xmllint specialized tooling.

6. **Edge cases (XML special chars in agent prose).** Spec § 4 has no CDATA strategy. This is a *real* schema-design defect — agent prose routinely contains code blocks with `<`, `>`. Under JSON Schema (the recommended format change per C1) this defect dissolves entirely (JSON's `<`/etc. string-escape semantics handle it transparently). Under XML retention, an explicit `<![CDATA[...]]>` strategy would be required.

### Ruling

The schema design is **structurally sound** for the arbitration use case (the load-bearing one — `disputes_remain` trigger). The envelope needs three additional identity fields. The XSD strawman fails on agent-prose syntax handling; JSON Schema dissolves the defect. The bug-fix thesis is validated in real-time by this very deliberation hitting the same trigger miss.

**Q2 verdict: APPROVE-WITH-FIXES.** Conditions:

- **C6 (P1):** § 4.1 envelope — add required fields `deliberation_stage`, `engine_version`, `source_commit`. (Source: schema-design-expert Rec 2 surviving, majority-supported.)
- **C7 (P1):** § 4 + § 5.1 — adopt **JSON Schema** as canonical format (subsumed by C1; restated here as the Q2-axis ruling). The arbitration schema's structural elements (`<per_question_rulings>`, `<ruling_lines>`, `<disputes>/<dispute>`) translate cleanly to JSON Schema with identical semantics. (Sources: unanimous P1 convergence across all four agents.)
- **C8 (P2):** § 4.8 — refine SemVer bump policy with explicit consumer-impact qualification (field rename = MAJOR even if technically additive when consumer parses by name). (Source: schema-design-expert Rec 6 modified, adapter-consumer Rec 7 modified.)
- **C9 (P2):** § 5.1 — specify validator error-object schema (`field_path`, `error_code`, `human_message`). (Source: schema-design-expert Rec 9 surviving.)
- **C10 (P3):** § 4.8 — adopt **1.0.0-rc.1 versioning** strategy with bounded iteration period ending by constitutional deadline, rather than 0.x namespaces (the synthesis-ruled dispute resolution per Disputes Remaining section). (Source: devils-advocate position; schema-design-expert conceded under timeline pressure.)

---

## Q3 — Tier placement + methodological recursion

**Question:** Should the spec land at Tier 3 (Component) or Tier 2 (Suite), and should the spec require XML for its OWN verification outputs?

### Agent positions

**engineer** (`revision_2.md`): Treats recursion as P2 clarification (New P1 "Address methodological recursion paradox" was added under pressure but framed as elevation-of-priority, not resolution-substance). Engineer's substantive position: recursion question should not block technical delivery within constitutional deadline; markdown for v4.2.0's own verification is operationally appropriate.

**schema-design-expert**: Did not engage substantively with tier placement; deferred to existing Principle XXVIII framing (Tier 2 doctrine, Tier 3 implementation).

**adapter-consumer**: Did not directly oppose Tier 3 placement; the consumer concern (spec-kit-orc adapter migration) is conversus-oss-specific, supporting Tier 3 evidence base.

**devils-advocate** (`revision_2.md`): Maintains Rec 3 (surviving): the methodological-recursion paradox is constitutionally load-bearing and requires explicit arbiter resolution. Position: spec's invocation of Principle VII "retroactive obligation" exemption is "creative interpretation rather than established precedent."

### Per-axis findings

1. **Tier placement (OQ1).** Evidence base for Tier 3: only conversus-oss produces deliberation outputs today; conversus-enhanced produces solver outputs (not deliberation outputs); no other suite sibling exists. Evidence base for Tier 2: speculative — depends on future siblings that don't yet exist. The same reasoning that drove v4.1.0's *demotion* from Tier 1 to Tier 2 (place at the lowest tier the evidence supports; promote when evidence accumulates) applies recursively. **Tier 3 confirmed.** Re-evaluate at the first conversus-suite sibling that produces deliberation-like artifacts, exactly as spec § 12 OQ1 recommendation-lean states.

2. **Methodological recursion (OQ5).** Spec § 9.1 + § 13 + § 12 OQ5: this deliberation runs against current (markdown) templates; subsequent specs ratifying after v4.2.0 produce XML; the v4.2.0 verification trail itself stays markdown — "a fixed point in the migration." Spec § 13 cites Principle VII (no retroactive obligations on outputs predating the rule).

   The devils-advocate critique is partially correct that "retroactive obligation" is an *interpretation* rather than an established Build-Fractal precedent. But the alternative — pause this verification, implement XML schema first, then re-run verification — would itself violate Tier 1 Principle II (stable interfaces): the verification methodology is itself an interface, and asking it to migrate its substrate mid-deliberation is exactly the kind of mid-flight interface change Principle II forbids.

   The synthesis's recommended resolution holds: "Document the recursion question as constitutional clarification item for post-implementation governance review rather than blocking requirement. Implementation proceeds with markdown verification for this spec, XML mandatory for subsequent specs." This is recursion-EXEMPTED.

   **Note:** the very real-time evidence that v4.2.0's bug-fix thesis is sound (Bug C trigger miss reproducing in this deliberation) is *not* a counter-argument for recursion-MANDATED. It is, if anything, evidence that *blocking* on schema implementation before completing verification would be operationally infeasible — the engine bug doesn't prevent the verification from completing (manual arbitration suffices); it just confirms the spec is needed.

### Ruling

Tier 3 is the lowest tier the evidence supports, per the same demote-when-evidence-thin posture used in v4.1.0. The methodological-recursion paradox is real but is correctly resolved by the spec's existing § 13 "fixed point in the migration" framing, supported by Principle VII analog reasoning. Devils-advocate's critique is noted but does not survive scrutiny against Principle II's stability-of-interface principle applied to verification methodology itself.

**Q3 verdict: TIER-3-CONFIRMED + RECURSION-EXEMPTED.** No conditions needed beyond what the spec already drafts. The spec's § 13 framing of "fixed point in the migration" + spec § 12 OQ5 recommendation-lean are accepted as drafted.

---

## Notable dispute resolutions

The synthesis surfaced six disputes the engine didn't auto-route. Ruling on each:

1. **Format choice resolution timing.** The arbiter rules **definitively in favor of JSON Schema** (C1 + C7). Adapter-consumer's position that consumer migration cannot proceed against an undefined target was correct; the technical evidence convergence makes evaluation ceremonial. Product-choice framing per Principle XXVIII non-format-mandate is preserved by framing JSON Schema as the spec's *recommended* implementation, not as a constitutional mandate — consistent with the synthesis's recommended resolution.

2. **Constitutional recursion priority.** Engineer's framing prevails (Q3 ruling). Devils-advocate's concern is documented for post-ratification governance review but does not block.

3. **Schema versioning approach.** 1.0.0-rc.1 prevails over 0.x namespaces (C10). Timeline pressure requires production-ready stability signals.

4. **Performance vs validation sophistication.** Tiered validation approach prevails (C2 + C5): basic structural validation in v1.0.0 within <100ms budget, advanced features (cross-reference integrity) in v1.1.0 after performance analysis.

5. **Timeline pressure accommodation.** Constitutional deadline non-negotiability is unanimous and binding. Spec staging — not deadline modification — is the response.

6. **Consumer protection implementation timing.** Adapter-consumer's phased approach prevails (covered under C4 semantic-equivalence-testing minimum + spec § 11.1's existing parallel-format window).

---

## Combined disposition

- **Q1:** APPROVE-WITH-FIXES (C1, C2, C3, C4, C5)
- **Q2:** APPROVE-WITH-FIXES (C6, C7, C8, C9, C10) — C7 subsumed by C1; restated for Q2-axis traceability.
- **Q3:** TIER-3-CONFIRMED + RECURSION-EXEMPTED (no conditions)

All three are PASS-variants. Per QUESTION.md: **PROCEED-TO-SELF-CONSISTENCY** with C1-C10 applied to produce spec v2.

### Conditions for spec v2 (consolidated, P1 first)

**P1 (must-fix before self-consistency):**
- **C1** — Switch canonical format to JSON Schema (subsumes C7); update § 4 + § 5.1.
- **C2** — Establish <100ms per-output write-time validation performance budget; § 5.1.
- **C3** — Specify dependency-ordered template migration with one-mode pilot; § 11.
- **C4** — Semantic equivalence testing as CI gate during migration window; § 11.1.
- **C6** — Add `deliberation_stage`, `engine_version`, `source_commit` as required envelope fields; § 4.1.

**P2 (should-fix):**
- **C5** — Tiered/staged implementation: v1.0.0 basic + v1.1.0 advanced; § 11.
- **C8** — Refine SemVer bump policy with consumer-impact qualification; § 4.8.
- **C9** — Validator error-object schema; § 5.1.

**P3 (consider):**
- **C10** — 1.0.0-rc.1 versioning over 0.x namespaces; § 4.8.

### Post-ratification operational guidance (not spec v2 changes)

- Phased consumer protections (adapter-consumer New P1) and rollback mechanism (devils-advocate Rec 7 surviving) are accepted as operational guidance for the migration window per § 11.1, not as spec v2 conditions.
- Methodological-recursion question is logged for post-ratification governance review per Q3 ruling; not a spec-text condition.

---

## Ruling lines

- **Q1 RULING: APPROVE-WITH-FIXES** — implementation is feasible within the 2026-12-01 deadline conditional on format change to JSON Schema (C1), <100ms write-time validation budget (C2), dependency-ordered template migration (C3), semantic equivalence testing (C4), and tiered staging (C5); all derived from unanimous or bilateral agent convergence with constitutional deadline accepted as binding.
- **Q2 RULING: APPROVE-WITH-FIXES** — the schema design is structurally sound (arbitration `<per_question_rulings>`/`<ruling_lines>` and synthesis `<disputes>/<dispute>` correctly address Bug C, validated in real-time by this very deliberation reproducing the trigger miss the spec proposes to fix), with envelope identity fields (C6), JSON Schema canonical format (C7), and SemVer/error-object refinements (C8, C9, C10) needed.
- **Q3 RULING: TIER-3-CONFIRMED + RECURSION-EXEMPTED** — Tier 3 is the lowest tier the evidence base supports (only conversus-oss produces deliberation outputs); methodological recursion is resolved by the spec's existing § 13 "fixed point in the migration" framing supported by Principle II stability-of-interface reasoning applied to verification methodology itself.

**Combined disposition: PROCEED-TO-SELF-CONSISTENCY.** Apply C1-C10 to produce spec v2; self-consistency verification runs against spec v2 with C-conditions applied.
