# v4.2.0 Self-Consistency Re-Run — Manual Arbitration Verdict

**Spec commit reviewed:** `3208bd3` (`spec/v4.2.0-structured-deliberation-outputs`, v3)
**Deliberation:** `deliberations/v4.2.0-structured-deliberation-outputs-self-consistency-rerun-2026-05-13/`
**Round:** Self-consistency RE-RUN (second attempt; first run produced `D1-D15` to fix v2's Q3 FAIL-CONTRADICTION)
**Arbiter:** Manual (Phase 6 did not fire)

---

## Process Note

**Phase 6 did not fire — fourth consecutive occurrence of the bug v4.2.0 is fixing.** The engine produced `summary/final.md` (Phase 5 synthesis) and all four agent revisions + disputes (Phases 3-4), but the arbitration dispatch silently failed to materialize a Phase 6 verdict file. This is now the *fourth* deliberation in v4.2.0's verification arc that has reproduced exactly the failure mode v4.2.0 is being ratified to prevent: structured outputs are required by the methodology, the methodology emits the structure unevenly across phases, and downstream consumers (here, the arbiter or arbiter-equivalent) silently get nothing rather than getting a malformed-but-recoverable record. Every cycle of verifying this spec demonstrates the spec's structural-detection thesis in real time. The pattern is not noise; it *is* the evidence base. The four occurrences (originating dispatch, original self-consistency arbitration, originating-→-self-consistency hand-off, and now this rerun) constitute the strongest empirical justification for v4.2.0 that could be assembled — short of writing fabricated examples, which would not be admissible under any of the agents' purity standards.

**This rerun's role is narrow.** It is not a "find new problems" round. The first self-consistency stage produced fifteen D-conditions to address Q1 PASS-WITH-CLARIFICATIONS gaps, Q2 PASS-WITH-CLARIFICATIONS recursion-precedent risks, and Q3 FAIL-CONTRADICTION (v2 § 5.1 blocking-validation contradicting Tier 2 Principle V). v3 (commit `3208bd3`) applied all fifteen. This rerun verifies the fixes held up and did not introduce new contradictions. The default posture is **defend the status quo**: v3 stays in force unless the rerun surfaces a residual or new contradiction. The agents' job here was confirmation; the arbiter's job is to confirm their confirmation.

---

## Decision Framework

The framework for this rerun is identical to the first self-consistency stage, plus the constraint that confirmation-stage outputs cannot retroactively re-litigate scope decisions already settled in the originating arbitration (Tier-3 placement) or the first self-consistency arbitration (D1 reversal as the right shape).

**Tier 2 Principle V** (`build-fractal/conversus/CONSTITUTION.md` L76-78):
> "Output validation (e.g., Phase 6 heading checks) emits **warnings** for malformed output but **does NOT block file writes**. Malformed output is better than no output."

This is the load-bearing constraint v2 § 5.1 violated. v3 § 5.1 inverts the architecture: `engine/persistence.py` writes the file unconditionally before any error-handling branch; validation produces a warning record (event-stream + `.validation-warnings.json` sidecar) but never raises. The mechanical-enforcement bite Principle XXVIII requires moves entirely to the PR-time CI gate (§ 5.4), which is a different surface from the write-time persistence layer and therefore not in tension with Principle V.

**Tier 2 Principle XXVIII** (`build-fractal/conversus/CONSTITUTION.md` L490-644). Six sub-clauses Q1 audits against v3:
- Sub-clause 1: schema location declared in `CONFORMANCE.md`, discoverable surface linked from both `README.md` and `CLAUDE.md`. v3 § 4.0 + § 6.1 (D9, D10).
- Sub-clause 2: bidirectional validation (artifacts→schema AND schema→artifacts) with mechanical CI bite + at least three test fixtures covering field-presence, types, value-constraints. v3 § 5.3 (D14, four fixtures) + § 5.4 forward + drift jobs (D12).
- Sub-clause 3: silent format changes are a violation; schema edits MUST be accompanied by a version-bump signal. v3 § 5.4 schema-version-bump detection job (D15).
- Sub-clause 4: cross-product consumer contract obligations; producer-side fixtures alone do not satisfy this sub-clause; consumer-side CI must validate against versioned fixtures. v3 § 7.1 sec. 4 + § 6.2 orchestrator adapter CI.
- Sub-clause 5: `CONSUMER-CONTRACT.md` MUST explicitly name each declared stable surface AND state its stability guarantee. v3 § 7.1 (D11) — six-section content specification.
- Sub-clause 6 (implicit, derived from C6): fixture corpus must mechanically demonstrate enforcement bite. v3 § 5.3 covers field-presence (b), types (c), value-constraints (d), end-to-end conformant (a).

**Cross-tier weakening prohibition** (`build-fractal/conversus/CONSTITUTION.md` L475-488 / L649-664):
Any component-tier amendment is assessed against three criteria:
- (i) Implicit relief without invoking the formal Relief pathway in `COMPLIANCE.md` Part VI.
- (ii) Interpretation language that would cause existing implementations to no longer satisfy the upper-tier principle.
- (iii) Suite-specific adaptation clause effectively bypassing an upper-tier MUST.
v3 § 9.2 walks all three and concludes none are triggered. Q2 audits this conclusion.

---

## Per-Question Rulings

### Q1 — Principle XXVIII fit on v3: **PASS-WITH-CLARIFICATIONS**

The principle-xxviii-fit-auditor's revision (revision_2.md) modified 1 recommendation, kept 6 as surviving, and added 3 new P1 items. Crucially, the auditor confirmed that the six mechanical D-conditions landed correctly:

- **D9 (CONFORMANCE.md schema location)** — v3 § 4.0 + § 6.1 satisfy sub-clause 1's textual requirement. The Persistence-Contract row in `CONFORMANCE.md` is updated to name `engine/schema/v1/`, the file-naming convention, the `$id` URI base, and to cross-reference `CONSUMER-CONTRACT.md`. **SATISFIES.**
- **D10 (README + CLAUDE links)** — v3 § 6.1 names both `README.md` and `CLAUDE.md` as required link surfaces, mirroring the constitutional "BOTH" qualifier at L508-510. **SATISFIES.**
- **D11 (CONSUMER-CONTRACT.md content)** — v3 § 7.1 specifies six required sections (title + declaration, declared schema surfaces with explicit stability prose, display-text surfaces, consumer obligations, pointer to producer enforcement, pointer to schema directory). The stability guarantee is stated as explicit prose, not gesture, satisfying sub-clause 5's "explicitly name" requirement. **SATISFIES.**
- **D12 (bidirectional drift detection)** — v3 § 5.4 second job re-runs forward-validation against the entire pre-existing `deliberations/**` corpus whenever a PR modifies `engine/schema/v1/`. This is the schema→artifacts direction that sub-clause 2 explicitly mandates. **SATISFIES.**
- **D14 (fixture types)** — v3 § 5.3 ships four fixtures: (a) conformant baseline, (b) missing-required-field, (c) wrong-type, (d) enum violation. § 5.3's "Fixture scope coverage" paragraph explicitly maps each to sub-clause 2's named enforcement surface (field-presence, types, value-constraints). **SATISFIES** (oversatisfies by adding the enum fixture beyond the three constitutionally required).
- **D15 (version-bump CI)** — v3 § 5.4 third job asserts one of three branches on every schema edit ($id increment, schema_version pattern bump, or `[schema:no-bump-justified]` token in the PR description). The escape hatch is bounded and auditable. **SATISFIES.**

The auditor's three new P1 recommendations (strengthen § 9.2 cross-tier analysis; tighten anti-precedent containment; add constitutional authority citation for CI gates) are not Principle XXVIII fit issues — they are Q2/Q3-adjacent constitutional-coherence concerns the auditor was right to surface but which belong to the other two questions for ruling purposes. Q1 itself shows no XXVIII fit gap.

**Meta-check: did v3 introduce new XXVIII fit gaps?** No. Every section v3 added (§ 4.0, § 5.3, § 5.4, § 6.1, § 7.1) tightens an XXVIII sub-clause rather than relaxing one. The strict-reader's Recommendation 5 (Principle XIV implementation-parity check, i.e. a CI job that validates engine-generated outputs against the declared schema) is a reasonable engineering refinement but is not constitutionally required — XXVIII sub-clause 2's bidirectional CI requirement is satisfied by D12's schema→corpus job, and the strict-reader's parity check is the same job in different framing.

**Q1 verdict: PASS-WITH-CLARIFICATIONS.** E-condition E1 (below) carries the auditor's authority-citation concern into v4 without reopening the XXVIII fit ruling.

### Q2 — Temporal-constraint reframing on v3: **PASS-WITH-CLARIFICATIONS**

The recursion-precedent-auditor's revision is the primary input. The auditor kept 6 recommendations surviving, modified 1 (the layered anti-precedent approach), and added 1 new P1: "Clarify bootstrap paradox logical foundation," triggered by the purist's cross-review challenge that draft schemas could make conformance possible before ratification, thereby reducing the bootstrap paradox from logical impossibility to procedural convenience.

This new P1 is the substantive question Q2 must answer. **The arbiter rejects the purist's challenge, and rules the bootstrap framing structurally distinct from v4.1.0's rejected override-with-rationale stretch, for three reasons:**

**First — the draft-schema counter-argument does not survive contact with the actual artifact stream.** The purist argues that schemas "could exist in draft form during verification, making conformance possible before ratification." But the verification cycle for v4.2.0 is what is currently producing the artifacts in question. The originating deliberation (commit `35d869b`) ran on `2026-05-12` and emitted markdown outputs — there was no draft schema at the time those outputs were emitted, because the spec proposing the schema was the deliberation's subject. The self-consistency stage ran on `2026-05-13` against v2 (commit `edf80b4`) — still no schema artifact in existence. This rerun is itself emitting markdown outputs against a v3 spec whose schema files are described in prose, not yet shipped. The bootstrap paradox is therefore not a hypothetical that "could" be dissolved by writing a draft schema first; it is a concrete property of the artifact stream that already exists in the repository's git history. Writing a "draft schema" retroactively to make pre-ratification outputs conformant would be the same anti-pattern (post-hoc rationalization) the purist's own framework forbids.

**Second — v3's anti-precedent containment language in § 9.1 D5 paragraph is materially stronger than v4.1.0's override-with-rationale framing was.** v3 names three concrete exclusions: "amendments adjacent to schema infrastructure," "amendments touching validation pathways," and "the bootstrap paradox of a spec standing up its own schema substrate" — and explicitly states that "the one and only case the accommodation covers" is the substrate-standup case. Future MAJOR `schema_version` bumps, future schema additions for new output types, and future validator-implementation amendments are all named as **NOT covered**. v4.1.0's override-with-rationale stretch had no comparable containment — it offered the framing as a generally-available pathway and was rejected on exactly that ground. The structural distinction holds: v4.1.0 created an exit valve; v3 § 9.1 creates a one-time scope clarification with a named termination condition (substrate exists; subsequent amendments are bound).

**Third — the purist's own modification accepts this.** Purist revision_2.md Recommendation 1 was modified from "eliminate temporal accommodation entirely" to a one-time bootstrap exception with formal constitutional-amendment process for future similar accommodations. That is the same shape as v3's § 9.1 + § 9.2 + § 9.3 stack. The purist's "non-negotiable" in disputes.md is the *resolution* of the bootstrap paradox question, not its outcome — and the resolution above is grounded in the concrete artifact stream, not in assumed logical impossibility. The recursion-precedent-auditor's new P1 asked for "definitive resolution" of this question; the arbiter resolves it here.

**Anti-precedent tightness stress test.** Could a future amendment creatively re-frame to invoke § 9.1's accommodation? The auditor and strict-reader converged on a layered approach (technical conditions primary, categorical prohibitions secondary). v3 § 9.1's current language is closer to categorical than technical. **This is a real residual gap.** A future amendment that says "this is also a bootstrap-paradox case because we are standing up a *new* schema directory at v2/" could plausibly invoke § 9.1 unless the technical condition is sharpened. E-condition E2 (below) closes this gap by adding the technical condition "the accommodation applies only when NO JSON Schema validation exists for the artifact type in question, and the spec's own ratification is what stands up that validation" — which mechanically excludes the v2/ scenario because v1/ schemas would already exist at that point.

**Cross-tier weakening assessment audit.** v3 § 9.2 walks all three criteria. The strict-reader and recursion-precedent-auditor both flagged § 9.2 as conclusory rather than systematic — this is the unanimous P1 finding of the rerun. The arbiter agrees the prose is light, but disagrees that the *conclusion* is wrong. Each criterion is correctly traced: (i) no Relief invocation because there is no ongoing inability — the situation is one-time logical impossibility, structurally identical to v4.1.0's ratified temporal-vs-membership distinction; (ii) Principle V satisfaction is strengthened by v3 (the entire D1 inversion of v2 was *to* satisfy Principle V), so no existing implementation's compliance is degraded; (iii) no MUST clause is being bypassed for outputs in the schema's temporal scope — only outputs that precede the schema's existence are out of scope, and that's not bypassing a MUST, it's the MUST not applying. The agents' demand for "systematic verification matrix against existing Principle V implementations" is reasonable for v4 but is an evidentiary upgrade, not a conclusion-changing finding. E-condition E3 adds the matrix.

**Forward-promotion pathway.** v3 § 9.3 specifies a concrete trigger (second conversus-suite product producing deliberation-like artifacts + either independent CONSUMER-CONTRACT or schema vendoring) and a concrete pathway (Tier-3 → Tier-2 MINOR amendment if substance unchanged, MAJOR if substance changes). This is concrete enough. **No E-condition needed on § 9.3.**

**Q2 verdict: PASS-WITH-CLARIFICATIONS.** Not TIER-2-PROMOTE-RECOMMENDED — the agents' criticism is about the *prose* of § 9.2 and the *tightness* of § 9.1's anti-precedent language, not about Tier-3 placement being structurally unstable. Tier-3 placement was settled by the originating arbitration's TIER-3-CONFIRMED ruling on Q3; this rerun is not a vehicle for reopening that decision. Not RECURSION-PRECEDENT-FAIL — the reframing is structurally distinct from v4.1.0's stretch, per the three reasons above.

### Q3 — Principle V reversal + new-contradiction check: **PASS-WITH-CLARIFICATIONS**

The strict-reader's revision is the primary input. The strict-reader modified 5 of 7 recommendations and kept 2, with the highest-priority surviving item being the layered anti-precedent containment (which Q2 already addressed). On Q3 specifically — the D1 reversal and the new-contradiction check — the strict-reader's analysis is the most informative.

**D1 reversal verification.** v3 § 5.1 has been read in full. The text is explicit:

- The section opens with the verbatim Principle V quote at L76-78.
- The validator signature is `validate_output(path, content) -> ValidationResult` with the explicit constraint "The validator MUST NOT raise on non-conformance; it MUST return the `ValidationResult` and let the caller decide."
- The persistence layer pseudocode is unambiguous: `path.write_bytes(content)` is called **before** any conformance check on the result. The comment reads "ALWAYS write the file, regardless of conformance (Principle V)." There is no `SchemaViolation` exception path in the persistence layer.
- Warning emission goes to the event stream + `.validation-warnings.json` sidecar — a structured side-channel, not an abort.
- The `--validate-outputs` flag's purpose is explicitly disclaimed as not-an-enforcement-bypass: "the file would be written either way; disabling validation only suppresses the warning record."

**There is no residual blocking language in § 5.1.** The reversal is complete.

**PR-time CI gate constitutionality (§ 5.4).** A PR-blocking CI gate is constitutionally different from a write-blocking validator. The PR gate prevents merging non-conformant code into the producer codebase; it does not prevent runtime persistence of any artifact already produced by an in-flight deliberation. This is the right shape per Principle V. v3 § 5.4's text preserves the distinction cleanly — the gate operates on `pull_request` triggers against the *producer code's* repository, not against the deliberation event stream.

**The principle-xxviii-fit-auditor and strict-reader both raised a legitimacy concern: the CI gate lacks explicit constitutional authority citation.** This is the third agent-converged P1 of the rerun. The arbiter agrees the citation is missing and rules it an E-condition (E4) rather than a contradiction. PR-blocking CI gates derive authority from Tier 1 Principle II (stable interface enforcement) and Tier 2 Principle XXVIII sub-clause 2 (mechanical CI bite). The principle is implicit but real; v4 should make it explicit. This does not affect the Q3 verdict.

**D2 (Principle II misattribution strike).** v3 § 9.1's first paragraph explicitly states: "v3 strikes the Principle II citation and replaces 'exemption' with **temporal-constraint scope** language." Verified — there is no residual Principle II citation in § 9.1 supporting the temporal-constraint argument. The misattribution is cleanly removed. **D2 satisfied.**

**D3 (cross-tier weakening assessment honesty).** Covered under Q2. v3 § 9.2 honestly assesses all three criteria; the conclusion that none are triggered is supported, though the prose is lighter than agents would prefer. E-condition E3 addresses the prose gap.

**New-contradiction walk-through across the 156-line addition.** The arbiter walked the new sections:

- **§ 4.0** (schema location declaration). Adds metadata; declares `engine/schema/v1/` as canonical, cites `$id` base URI. No principle conflict — this is the textual surface XXVIII sub-clause 1 demands.
- **§ 5.3** (worked-example fixtures). Names four fixture files with expected validator outputs. No principle conflict — this is XXVIII sub-clause 2's enforcement surface.
- **§ 5.4** (CI gate). Defines four jobs (forward-validation, bidirectional drift, schema-version-bump, fixture+renderer). The third job's `[schema:no-bump-justified]` escape hatch is the only place that touched a soft surface; the escape requires a rationale referencing a specific clarification-only edit, so it is bounded and reviewable. No principle conflict.
- **§ 6.1** (file edits per repo). Names the file deltas to land. Mechanical; no principle conflict.
- **§ 7.1** (CONSUMER-CONTRACT.md content specification). Names six required sections with explicit stability prose. No principle conflict — this *is* XXVIII sub-clause 5's "explicitly name" requirement.
- **§ 9.2** (cross-tier weakening assessment). Discussed under Q2.
- **§ 9.3** (forward-promotion pathway). Names trigger + pathway. No principle conflict.

**No new contradiction surfaces in the walk.** The 156-line addition is on net constitution-strengthening: it adds XXVIII sub-clause discharge surfaces, tightens cross-tier accommodation containment, and operationalizes forward-promotion.

**Q3 verdict: PASS-WITH-CLARIFICATIONS.** D1 reversal is clean. No new contradictions. E-conditions handle the agents' remaining clarifications (authority citation, technical-condition tightening, evidentiary upgrade to § 9.2).

---

## Combined Disposition

All three questions return PASS-variant verdicts. The default-defend-status-quo posture is satisfied: v3 stands, with E-conditions applied to produce v4 for blind verification.

**Disposition: PROCEED TO BLIND VERIFICATION with E-conditions applied to produce spec v4.**

### E-Conditions for spec v4

- **E1** — § 5.4: Add explicit constitutional authority citation for PR-blocking CI gates, grounding the gate's authority in **Tier 1 Principle II (stable interface enforcement)** + **Tier 2 Principle XXVIII sub-clause 2 (mechanical CI bite)**. One sentence is sufficient; the goal is to close the implicit-authority gap the principle-xxviii-fit-auditor identified, not to create new constitutional framework.

- **E2** — § 9.1 D5 paragraph: Add **technical condition** for anti-precedent containment, layered on top of the existing categorical prohibitions. Specifically: "The accommodation applies only when (a) no JSON Schema validation exists for the artifact type in question at the time verification begins, AND (b) the spec's own ratification is what stands up that validation. Any spec for which condition (a) is false — including future MAJOR `schema_version` bumps, additions of new output types to an existing schema directory, and validator-implementation amendments — does not satisfy the technical precondition for accommodation invocation and remains bound by the schema in force at verification time." This mechanically excludes the v2/ scenario and similar creative re-framings.

- **E3** — § 9.2: Add a **systematic verification matrix** appendix enumerating current Principle V-compliant implementations (engine warning-based validators across all phase types) and demonstrating that each remains compliant under v3's architecture. Replace conclusory prose with citation-backed analysis for each of the three criteria. This is an evidentiary upgrade, not a conclusion change; agents unanimously requested it.

- **E4** — § 9.1: Add **precedent-citation requirement**. Any future constitutional amendment invoking temporal-constraint reasoning MUST explicitly cite this spec (v4.2.0) + the v4.1.0 self-consistency arbitration (commit `8f90e2d`) and trigger mandatory constitutional-coherence review at originating stage. This makes precedent-stretching visible per the recursion-precedent-auditor's surviving Recommendations 3 + 4.

E-conditions are clarifications, not contradictions. They preserve v3's structural decisions and tighten the surrounding text. Blind verification runs against v4 (v3 + E1-E4).

### What this disposition does NOT do

- It does not reopen the originating arbitration's TIER-3-CONFIRMED ruling on Q3 (Tier 3 placement is settled; § 9.3 forward-promotion pathway handles future evolution).
- It does not eliminate the temporal-constraint accommodation (Q2 ruled the reframing structurally distinct from v4.1.0's rejected stretch).
- It does not require the purist's preferred 1.0.0-direct schema launch (RC versioning is a non-constitutional engineering decision; the purist's Recommendation 2 surviving status is noted but is not Q-bearing).
- It does not require collapsing the tiered rollout to a single cutover (migration philosophy is implementation, not constitutional).

---

## Ruling Lines

- `Q1 RULING: PASS-WITH-CLARIFICATIONS — D9-D15 land correctly across § 4.0, § 5.3, § 5.4, § 6.1, § 7.1; XXVIII sub-clauses 1-5 all SATISFY; no new XXVIII fit gaps; E1 carries authority-citation clarification forward.`
- `Q2 RULING: PASS-WITH-CLARIFICATIONS — bootstrap-paradox reframing is structurally distinct from v4.1.0's rejected override stretch (named exclusions in § 9.1 D5, concrete artifact-stream grounding, purist's own modification converges on this shape); E2 tightens anti-precedent technical condition; E3 upgrades § 9.2 to systematic matrix.`
- `Q3 RULING: PASS-WITH-CLARIFICATIONS — § 5.1 D1 reversal is complete (unconditional write_bytes pseudocode, no SchemaViolation exception path, no residual blocking language); D2 Principle II misattribution cleanly struck; 156-line addition introduces no new contradictions; E1 + E4 carry forward remaining clarifications.`
