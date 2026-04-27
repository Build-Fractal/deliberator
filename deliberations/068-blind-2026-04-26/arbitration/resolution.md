# Spec 068 BLIND Verification — Arbitration Resolution

**Arbiter persona**: balanced-arbiter (impartial, weights all perspectives equally)
**Authority**: binding
**Trigger**: always
**Methodology**: BLIND — judging Principle XVI on its merits, not on incumbency
**Scope**: Principle XVI specifically; findings on other principles surfaced incidentally are DEFER
**Date**: 2026-04-26

---

## Process Note

- **Trigger**: `always` — arbiter rules on every remaining dispute regardless of agent unanimity preconditions.
- **Disputes remaining per synthesis**: 4 (structural fork; test-contract sequencing; cross-reference graph asymmetry; XXIV scope residual).
- **Agents**: skeptic-mathematical, skeptic-cross-principle, practitioner.
- **Mode**: cooperative with subject arbitration.
- **Deliberation shape**: 3 reviews → 6 cross-reviews → 3 revisions → 3 dispute filings → synthesis → this arbitration.
- **Convergence already settled (out of scope here)**: VII↔XVI bilateral cross-reference (Convergence 1), solver-substitution semantic softening (Convergence 2), no-removal of XVI (Convergence 3), VII template/registry pre-conditions (Convergence 4), V-emission required (Convergence 5), 3-stage pipeline relocates to spec 013 (Convergence 6), "pinning" glossary in II + spec-013-routed test contract (Convergence 7). I do not re-litigate these — they bind regardless of my rulings below.

---

## Decision Framework

The grounding document is `CONSTITUTION-v2.3.2-blind.md`. The principles below directly govern the four disputes.

- **[VII — Reproducibility Over Inconsistency]**: "Given the same inputs, conversus MUST produce structurally identical output. Deterministic orchestration is non-negotiable" (lines 140–153). Owns determinism and the input-set boundary.

- **[V — Observable Deliberation]**: "Every phase MUST report progress. Output validation MUST catch malformed results. Agents MUST NOT silently swallow errors" (lines 113–122). Owns the progress-reporting contract that V-emission of pinned values flows under.

- **[II — Stable Interfaces]**: "Structural markers, template variables, the dispute-parsing subsystem, the preset schema, reference file paths, and the dispatch table are stable contracts" (lines 58–80). Owns the term-of-art glossary host for "pinning."

- **[XI — Single Source of Truth]**: "Every piece of information MUST have exactly one authoritative source. … When two sources disagree, it is always a bug — and the fix is always to eliminate the duplicate, not reconcile it" (lines 277–300). Governs the cross-reference graph and forbids parallel doctrine across principles.

- **[XII — No Dead Infrastructure]**: "Every provisioned capability MUST have at least one consumer. … Variables defined in the schema MUST be referenced in templates" (lines 322–344). Forbids constitutional pointers to artifacts that do not exist.

- **[XXIV — Safety-Critical Defense-in-Depth]**: Three-layer defense (schema-required field + parser validation + contract test reproducing the failure scenario) for synthesis verdict generation and provider protocol implementation (lines 681–706). The principle's scope is explicitly enumerated; expansion requires amendment.

- **[XVI — Mathematical Transparency]** (the subject of review): governs LLM-mediated parameter pinning, plain-language plugin output, solver-substitution semantics, and the 3-stage pipeline (lines 426–481).

---

## Binding Decisions

### Dispute: Structural fork (collapse vs. decompose-and-redistribute vs. tightened-standalone)

**Positions:**
- **practitioner**: keep XVI as a tight standalone principle (4–6 operational lines), transparency and pinning co-located. Will accept skeptic-mathematical's "no new principle numbers, transparency stays inline" as the convergence point.
- **skeptic-cross-principle**: execute four-step sequence (split → relocate → cross-reference → absorb). Transparency fragment lands in IV; pinning fragment folds into VII as named extension OR keeps freestanding under tighter name. In Phase 4, conceded "I now treat this as a synthesizer decision rather than a Devil's-Advocate hill."
- **skeptic-mathematical**: analytic decomposition along transparency/determinism/pinning axis, but no new principle numbers. Most likely outcome: tightened-standalone XVI with transparency surviving as residual kernel and pinning collapsed to one operational sentence.

**Synthesizer's assessment:** "The lowest-risk path is the practitioner's 'tight standalone XVI' outcome, because it (a) preserves the operationally crisp gate inline, (b) avoids the spec-redirect cleanup that absorption requires for specs 012-019, and (c) respects the convergence-floor edits (VII↔XVI cross-reference, V-emission, II glossary) which all three reviewers agreed land regardless of structural form. … skeptic-mathematical's 'no new principle numbers, transparency stays inline' outcome is functionally equivalent to practitioner's tight-standalone but framed as the result of analytic decomposition rather than as a starting position. Practitioner explicitly accepts this as the convergence point. This is the strongest available consensus."

**Ruling: ACCEPT — adopt tightened-standalone XVI with the synthesizer-recommended shrinkage.**

**Grounding citation:** XI (Single Source of Truth) and XII (No Dead Infrastructure).

**Rationale:** XI forbids putting overlapping content in two locations; the synthesizer-recommended shape places each fact in one home (pipeline → spec 013, "pinning" definition → II, V-emission requirement → XVI cross-referenced from V). XII forbids stranding specs 012–019's references to "Principle XVI" by dissolving the principle entirely. The four-step decompose-and-redistribute path generates exactly the spec-redirect cleanup that creates dead pointers during the transition window — a textbook XII hazard at scale, as skeptic-mathematical correctly named. The tightened-standalone outcome preserves XVI as a constitutional pointer (XII-safe), keeps the operationally crisp gate against re-resolving parameters mid-run inline at the principle's own number (the gate practitioner correctly identified would dilute if buried inside VII whose lead sentence is "Deterministic orchestration is non-negotiable"), and absorbs all seven convergence edits without forcing cross-reference debt that XI would later flag as overlap.

**Rejected position:** skeptic-cross-principle's full four-step absorption. Their own Phase 4 disputes acknowledge they would "not dispute a synthesizer decision to define inline if the V-emission cross-reference is wired correctly." The fork resolves on the path that preserves their non-negotiables (VII↔XVI cross-reference, V-emission wired to II glossary, XVI stays as a numbered principle) while avoiding the operationally diffuse PR-review path practitioner correctly flagged.

**Required changes (concrete edits to lines 426–481 of CONSTITUTION-v2.3.2-blind.md):**

Replace the current XVI body (lines 427–481) with the following tightened-standalone form:

```
### XVI. Mathematical Transparency

Subject to Principle VII, when LLM-mediated parameter resolution is
required for objective-function assembly, parameter values MUST be
*pinned* (per the term-of-art defined in II) for the duration of a
single deliberation run. The LLM is called at most once per parameter
per run; cached values are reused for the remainder of the run. A
parameter re-resolution mid-run is a contract violation.

- Pinned parameter values MUST be emitted as deliberation output (e.g.,
  `optimization/pinned_parameters.yml`) under V's progress-reporting
  contract, subject to VII's reproducibility pre-conditions (config,
  template registry, capability registry byte-identical between runs).
  This makes pinning observable and auditable.
- Plugin recommendations (equilibrium scores, convergence predictions,
  config suggestions) MUST include plain-language explanations
  alongside numerical outputs. "Equilibrium quality: 0.87" is
  insufficient; "87% of agents are at their best possible position
  given others' positions" is required.
- Changing solvers (nashopt, AMPL, future alternatives) MUST NOT change
  the objective function expression or its parameter semantics.
  Numerical results may differ within solver-tolerance bounds; the
  objective function is the contract, not the solver's output.
- This clause constrains plugin *output content*; Principle XV
  constrains plugin *isolation from core state*. The two are
  independent.
- The 3-stage pipeline (symbolic parsing → LLM gap-filling → mechanical
  assembly), the cache-key contract, the contract test demonstrating
  no within-run drift, and the per-template documentation form live in
  spec 013, not in this principle.

*Origin: game engine vision (specs 012-019) — the transition from
template-driven prompts to mathematical optimization must not make the
system opaque. Users parameterize the math; they do not need to
understand it.*
```

Note: the prior "Clarification: determinism scope" footnote (lines 469–476) is removed as part of this rewrite (per Convergence 1 + P3 #4); it becomes unnecessary once the bilateral VII↔XVI cross-reference lands.

---

### Dispute: Test-contract sequencing (same-PR mandate vs. aspirational caveat vs. spec-013-routed)

**Positions:**
- **practitioner** (revised Rec 4): same-PR mandate — XVI amendment must ship together with `tests/test_parameter_pinning.py::test_no_within_run_drift`; constitutional pointer to a missing artifact violates XII.
- **skeptic-mathematical** (modified Rec 3): aspirational framing — "Until that test exists, this principle is aspirational; first PR adding the test removes the aspirational caveat." Decouples constitutional amendment (governance-weighted) from test design (engineering-weighted).
- **skeptic-cross-principle** (revised Rec 5): spec-013-routed — XVI references a contract test in spec 013; cache-key schema lives in spec 013, not constitutional prose.

**Synthesizer's assessment:** "skeptic-cross-principle's spec-013-routed shape is the strongest. It (a) avoids the same-PR governance/engineering coupling that skeptic-mathematical correctly identified as risky, (b) avoids the dead-infrastructure pattern practitioner correctly identified as forbidden, (c) leverages the spec-013 indirection the constitution already uses for cache-contract content. … The synthesizer should also note skeptic-mathematical's Phase 4 closing observation that this converges practitioner's same-PR mandate with their decoupling concern by making the dependency *spec 013 ships first*, not *test ships in same PR as constitution*."

**Ruling: ACCEPT — adopt shape C (spec-013-routed).**

**Grounding citation:** XII (No Dead Infrastructure) and XI (Single Source of Truth).

**Rationale:** XII is dispositive: a constitutional pointer to a non-existent test file path is exactly the dead-infrastructure pattern XII was written to prevent. Practitioner is right that the aspirational caveat is itself a tell that the pointer is a false promise. But practitioner's same-PR mandate trades one XII-tension for a different operational risk that skeptic-mathematical correctly diagnosed: bundling governance amendment with test-implementation creates a PR needing both quorum sign-off on the constitutional change and code review on test design, with the failure mode that disagreement on test design (what counts as "drift," scope of parameters exercised, assertion mechanism) blocks the constitutional clarification. Spec-013 routing solves both problems: the constitutional pointer is generic ("see spec 013's parameter-pinning contract test"), spec 013's existence and the test within it are the artifact dependency (XII-satisfied), and test design lands in the implementation PR for spec 013 where it belongs (XI-satisfied: cache-contract content has one home, not two). Rather than the aspirational caveat (which advertises its own dead-infrastructure status), the dependency becomes "spec 013 ships first."

**Rejected positions:**
- *skeptic-mathematical's aspirational framing* — the caveat does not cure the XII violation; it documents it. Once spec 013 is required to ship first, no caveat is needed.
- *practitioner's same-PR mandate* — correctly identifies the XII pattern but couples two governance domains (constitutional and engineering) that v2.3.0 onward have deliberately separated by routing implementation through specs.

**Required changes:** Already absorbed into the XVI rewrite above (final bullet: "the … contract test demonstrating no within-run drift … live in spec 013"). Additionally, the merge gate for this constitutional amendment is: spec 013 must contain the parameter-pinning contract test before the v2.3.3 amendment lands. This gate is procedural (PR description / merge checklist), not a further constitutional edit.

---

### Dispute: Cross-reference graph asymmetry (which node owns which edge)

**Positions:**
- **skeptic-cross-principle** (Phase 4 Dispute 2): convergent edits create a star graph centred on VII for some edges (template versioning, capability registry) and on XVI for others (V-emission, XXIV-synthesis). The three revisions never reconcile the centring choice — if template versioning lands in VII and V-emission lands in XVI, then XVI's V-emission depends on VII's reproducibility pre-conditions, but neither revision states the dependency. A future spec author editing a template breaks VII's reproducibility, which silently invalidates XVI's V-emission as an audit artifact.
- **skeptic-mathematical** and **practitioner**: did not surface this as a separate dispute; treated each cross-reference edit as independent.

**Synthesizer's assessment:** "This is a real residual gap surfaced only by skeptic-cross-principle's Phase 4 audit. The other two reviewers did not contest it (silent, not opposed). The fix is straightforward: the V-emission clause (wherever it lands) MUST cross-reference VII's reproducibility pre-conditions, so a reader understands that observable pinned values depend on (config, template registry, capability registry) being byte-identical for the audit to be meaningful."

**Ruling: ACCEPT — wire V-emission to VII's pre-conditions in one composed rule.**

**Grounding citation:** XI (Single Source of Truth) — when two sources disagree, eliminate the duplicate; here, two principles touch the same audit invariant and the dependency must be named explicitly to compose without ambiguity.

**Rationale:** skeptic-cross-principle correctly identifies a residual coupling that the other two reviewers missed. The defect is operationally subtle but real: emitted pinned values are only an audit artifact if VII's reproducibility pre-conditions hold; a registry change between runs makes the emission misleading. The fix is the smallest possible edit (a subordinate clause "subject to VII's reproducibility pre-conditions") rather than relocating the rule. Per XI, the V-emission rule's one home stays in XVI (where the synthesizer placed it) but its dependency on VII is explicit so future readers understand the composition. The alternative — silent dependency — would re-create the very class of defect Pattern 4 of the synthesis identified (single-source-of-truth applied to constitutional prose itself).

**Rejected position:** the implicit "treat each cross-reference as independent" stance held by skeptic-mathematical and practitioner. Their non-objection in Phase 4 is read as silence rather than opposition; skeptic-cross-principle's diagnosis is the only one in the record, and it stands unrefuted.

**Required changes:** Already absorbed into the XVI rewrite above. The first bullet of XVI's body explicitly states: "subject to VII's reproducibility pre-conditions (config, template registry, capability registry byte-identical between runs)." This wires the V/XVI/VII edges into one composed rule per the synthesizer's recommendation.

---

### Dispute: XXIV scope narrowing (residual coverage of optimization → synthesis-verdict path)

**Positions:**
- **skeptic-cross-principle** (Phase 4 Dispute 4, narrowed Rec 7): restricted XVI/XXIV interaction to "optimization-driven outputs consumed by synthesis-verdict generation." Acknowledged residual gap: optimization output authored before it becomes synthesis-bearing is not retroactively covered by XXIV. Will not block a synthesizer decision to drop the XXIV citation entirely.
- **skeptic-mathematical** (modified Rec 3): dropped XXIV citation entirely in favour of a generic test-contract clause; cited XXIV's literal scope (synthesis verdicts and provider protocols) and XI's prohibition on parallel doctrine.
- **practitioner**: did not address XXIV in disputes; deliberately stayed at V/VII surface.

**Synthesizer's assessment:** "The disagreement is small in operational impact. … The residual coverage gap is real but is a downstream evolution concern, not a v2.3.3 blocker. … Drop the explicit XXIV cross-reference from XVI per skeptic-mathematical's modified Rec 3. The generic test-contract clause (spec-013-routed per the test-sequencing dispute) covers the verification surface without expanding XXIV's authorized scope. Note in deliberation log: when an optimization output later becomes a synthesis-verdict input via a downstream spec, that downstream spec MUST add the XXIV three-layer defense at that point."

**Ruling: ACCEPT — drop the XXIV cross-reference from XVI; generic test-contract clause (via spec 013) carries the verification load.**

**Grounding citation:** XXIV (Safety-Critical Defense-in-Depth) explicit scope (lines 682–706) and XI (Single Source of Truth) prohibition on parallel doctrine.

**Rationale:** XXIV's scope is explicitly enumerated in its own text: "synthesis verdict generation … AND provider protocol implementation." The text further says the principle's scope was extended *to provider protocols* on enumerated evidence, which establishes the precedent that scope extension requires the principle's own amendment, not a sibling principle's cross-reference doing the work. Citing XXIV from XVI to cover optimization outputs would either silently expand XXIV's scope (XI violation: parallel doctrine appearing in two homes that disagree) or create a rule that the constitution simultaneously says is and is not safety-critical. The narrowing skeptic-cross-principle proposed is constitutionally clean but operationally fragile (their own admission); skeptic-mathematical's drop is constitutionally cleaner. The residual coverage gap (optimization outputs that later become synthesis-bearing) is a real downstream concern but is correctly handled at the point a downstream spec promotes the output to synthesis-bearing — the synthesizer's note belongs in the deliberation log, not in v2.3.3 prose.

**Rejected position:** skeptic-cross-principle's narrowed-XXIV citation. They themselves yielded on this in Phase 4 ("Either disposition is constitutionally defensible; … I will not block a synthesizer decision to drop the XXIV citation entirely if the test-contract clause stands on its own"). Per XI, when two equivalent dispositions exist, prefer the one with fewer cross-reference edges; dropping the citation honors that.

**Required changes:** Already absorbed into the XVI rewrite above — XVI's body contains no reference to XXIV. The verification surface is covered via spec 013's contract test (final bullet of XVI). No further constitutional edit needed. Deliberation log addendum (procedural, not constitutional): future specs that promote an optimization output to synthesis-bearing MUST add the XXIV three-layer defense at the point of promotion.

---

## Summary of Changes Required

### REQUIRED FIXES BEFORE MERGE

1. **Replace XVI body (lines 427–481) with the tightened-standalone form** specified in Dispute 1's Required changes section. This rewrite simultaneously:
   - executes the structural ruling (tightened-standalone, no new principle numbers, ~4–8 operational bullets);
   - removes the "Clarification: determinism scope" footnote (lines 469–476);
   - relocates the 3-stage pipeline narration to spec 013 (Convergence 6);
   - opens with "Subject to Principle VII, …" (Convergence 1, the XVI side of the bilateral edit);
   - places the V-emission requirement under VII's pre-conditions (Dispute 3 ruling + Convergence 5);
   - softens solver-substitution wording to semantic (Convergence 2);
   - cross-references XV for plugin-isolation independence (P2 #5);
   - routes the contract test through spec 013 (Dispute 2 ruling);
   - drops the XXIV cross-reference (Dispute 4 ruling).

2. **Append to VII (after current line 153)**:
   - "Principle XVI defines the sole sanctioned exception, scoped to LLM-mediated parameter resolution under within-run pinning discipline." (Convergence 1, the VII side of the bilateral edit)
   - "Reproducibility is conditional on (config, template registry, capability registry) being byte-identical between runs. Changes to any of these constitute a different input set." (Convergence 4)

3. **Add to II's stable-interface vocabulary** (within the bullet list lines 64–80, alongside the existing "stable contracts" enumeration):
   - "*Pinning* — a parameter value committed to a run-scoped store, immutable for the duration of the run, with invalidation policy specified in spec 013. Pinned values MUST be observable as deliberation output per Principle V; see Principle XVI." (Convergence 7, with the V-emission cross-reference required by Dispute 3 ruling)

4. **Procedural merge gate (not constitutional text)**: spec 013 must contain the parameter-pinning contract test (asserting no within-run drift) and the cache-key schema before the v2.3.3 amendment merges. This satisfies XII for the Dispute 2 ruling.

### RECOMMENDED FIXES

1. **CI hook for template description fields** (P3 #1) — linter check scanning `templates/optimization/*.yml` for missing `description:` and `plain_language:` fields. Operationalizes the plain-language rule. Non-blocking; lands in a follow-up PR.

2. **Rename XVI** (P3 #3) — under the tightened-standalone outcome, "Mathematical Transparency" remains acceptable because both transparency and pinning content survive in XVI. Skeptic-cross-principle's name-as-remediation-target concern is honored implicitly because the bundling defect is repaired by the body rewrite. If a future amendment relocates either the transparency clause or the pinning clause, rename becomes required at that point.

3. **Sync Impact Report update** — the existing Sync Impact block (lines 1–38) is for the v2.3.0 amendment; v2.3.3 needs its own block at the top of the file documenting this PATCH-level amendment (clarifications + cross-references; no new principles, no removals, no semantic-MAJOR changes).

---

## Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---|---|---|---|
| Structural fork | ACCEPT (tightened-standalone) | High | Practitioner explicitly accepts this as convergence point; skeptic-cross-principle yielded ("I now treat this as a synthesizer decision rather than a Devil's-Advocate hill"); skeptic-mathematical's preferred outcome is functionally equivalent. The synthesizer's lowest-risk argument lands cleanly under XII (avoids spec-redirect cleanup) and XI (each fact one home). |
| Test-contract sequencing | ACCEPT (spec-013-routed) | High | All three reviewers' non-negotiables are honored. XII dispositive on the same-PR-mandate's underlying motivation; XI dispositive on routing the cache contract through one home (spec 013). skeptic-mathematical's Phase 4 closing converges to the same shape ("spec 013 ships first, not test ships in same PR"). |
| Cross-reference graph asymmetry | ACCEPT (subordinate-clause wiring) | High | Defect is real (skeptic-cross-principle's diagnosis stands unrefuted). Fix is the smallest possible edit. Both other reviewers were silent rather than opposed. XI grounding is direct: composed rules require named dependencies. |
| XXIV scope residual | ACCEPT (drop citation) | Medium-High | Skeptic-cross-principle yielded explicitly. XXIV's own text bounds the scope, and XI prohibits parallel doctrine. Confidence is "medium-high" rather than "high" only because the residual coverage gap (optimization output becoming synthesis-bearing later) is a real downstream concern that this ruling defers to the promotion point. The deferral is correct, but it carries a future-evolution obligation that must not be dropped. |

**Overall deliberation quality.** This was a high-quality blind verification. Three reviewers operating under different lenses (math/logic-coherence, cross-principle audit, developer ergonomics) independently converged on five major fixes (VII↔XVI cross-reference, solver-substitution softening, no-removal, template-version pre-conditions, V-emission) and surfaced four genuine residual disputes that the synthesis correctly enumerated. Phase 3 revisions show meaningful concession patterns (skeptic-mathematical withdrew Recs 4, 5, 7, 10; practitioner withdrew Recs 5, 7; skeptic-cross-principle softened Rec 1, narrowed Rec 7), evidencing real engagement with adversarial cross-review rather than rote position-defense. The Phase 4 disputes were correctly scoped to live forks rather than retreaded P1 disagreements. The synthesizer's editorial assessments on each dispute were defensible and grounded in named patterns from the constitution itself.

The four ACCEPT rulings together move XVI from a bundled three-claim principle with an unenforced clarification footnote to a tightened-standalone principle with one operationally crisp gate, observable pinned values, semantic solver-substitution promise, plugin output transparency rule, XV/XVI independence cross-reference, and a real verification anchor via spec 013. Each ruling cites a specific grounding principle (XI, XII, XXIV scope text). No defensive amendments are introduced; the corrective shape is constitutionally minimal.

Two minor concerns worth recording (not blocking, not deferred-as-out-of-scope but flagged for the merge author): (a) the rewritten XVI body is meaningfully shorter than the current text, but length is not a constitutional constraint — readability and operational crispness are; the rewrite optimizes for both. (b) The procedural merge gate (spec 013 ships first) introduces a cross-repository sequencing requirement; whoever sequences the v2.3.3 amendment PR must verify spec 013's contract test exists before merging this PR, or the XII rationale for Dispute 2 is undermined.

---

**SPEC-068 BLIND VERIFICATION VERDICT: PASS WITH FIXES**

Four ACCEPT rulings on Principle XVI:
1. Structural fork → tightened-standalone XVI (rewrite body).
2. Test-contract sequencing → spec-013-routed (no specific test path in constitutional prose; spec 013 ships first as merge gate).
3. Cross-reference graph asymmetry → V-emission clause subordinate to VII's reproducibility pre-conditions (one composed rule).
4. XXIV scope residual → drop the XXIV cross-reference; generic test-contract clause carries the verification load.

Zero DEFER findings (the blind-methodology guarantee held: no incidental findings on principles other than XVI surfaced as standalone items). Zero REJECT rulings — every dispute the synthesis enumerated reflects a real defect with a constitutionally-grounded fix.

The amendment is fundamentally sound; the required edits are constitutionally minimal and converge with the seven Phase 3 convergences already settled. Once edits 1–3 in "REQUIRED FIXES BEFORE MERGE" land in the constitution PR and edit 4 (spec 013 procedural gate) is satisfied, v2.3.3 is ready to merge.
