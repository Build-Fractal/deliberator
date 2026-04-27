# Spec 069 BLIND Verification — Arbitration Resolution

**Arbiter persona**: balanced-arbiter (impartial, weighs all perspectives, binding)
**Scope**: Governance section, "Constitutional Inclusion Criteria" subsection, lines 811-844 of `CONSTITUTION-v2.4.0-blind.md`.
**Authority**: binding decision authority over the three remaining disputes named in the Phase 5 synthesis.
**Methodology**: blind — the gate is judged on its own merits, with no incumbency advantage.

---

## Process Note

- **Trigger**: `always` — synthesis identified 3 substantive disputes after Phase 4.
- **Disputes remaining**: 3, all on the gate subsection (in scope for spec 069).
- **Agents**: skeptic-mathematical (SM), skeptic-cross-principle (SCP), practitioner (Pr).
- **Mode**: cooperative with subject arbitration.
- **Convergent fixes already adopted by synthesis** (not re-litigated here): structured `Verification:` block replacing the "one paragraph" sub-clause; PR template + CI lint + non-author CODEOWNER review as a non-separable bundle; CODEOWNERS-grounded maintainer role; at least two worked examples; withdrawal of governance auto-anything; retention of three-criterion structure.

This arbitration only resolves the three remaining disputes on which Phase 4 reviewers did not converge.

---

## Decision Framework

The constitution itself supplies the principles that bear on these disputes. Each is cited by line range from the grounding document.

- **[Prospective-Only Migration]**: "This gate applies **prospectively** — to amendments landing once the gate is in force. Existing principles I-XXVII are grandfathered. Migrating any of them to operational guidance is a separate, intentional act governed by the same amendment process (with the receiving document identified explicitly in the migration spec)." (lines 840-844). This is the gate's own self-imposed scope discipline and bears directly on Disputes 1 and 3.

- **[Falsifiable Scope (Criterion 2)]**: "the principle's wording MUST be specific enough to flag a hypothetical future PR as violating, without requiring 'interpretation.'" (lines 822-826). Bears on Dispute 2 — whether a structured block or worked examples better satisfy the gate's own falsifiability standard.

- **[Mechanical Verification Capability (Criterion 1)]**: "at least one form of automated check ... MUST be feasible such that a future PR violating the principle would fail the check." (lines 814-820). Bears on Dispute 3 — whether Extension blocks introducing new normative requirements are themselves subject to the artifact requirement.

- **[Distinct from Existing Principles (Criterion 3)]**: "the principle MUST cover concerns not already addressable by composing existing principles ... Refining or extending an existing principle goes in that principle's body, not as a new principle." (lines 828-833). Bears on Dispute 2 — distinctness as content test versus procedural surface.

- **[Single Source of Truth (Principle XI)]**: "Every piece of information MUST have exactly one authoritative source. ... When two sources disagree, it is always a bug — and the fix is always to eliminate the duplicate, not reconcile it." (lines 239-256). Bears on Dispute 2 — whether a distinctness block restates Criterion 3 in template form (duplication) or operationalizes it (derivation).

- **[Backward-Compatible Extension (Principle III)]**: "New features MUST extend existing behavior rather than restructuring it. Omitting optional fields MUST preserve existing behavior exactly." (lines 43-55). Bears on all three disputes as the load-bearing constraint on what the amendment can responsibly ship — the gate must not retroactively restructure pre-gate principles' modification surface.

- **[No Dead Infrastructure (Principle XII)]**: "Every provisioned capability MUST have at least one consumer." (lines 283-305). Bears on Dispute 2 — a structured block that authors fill mechanically without it changing reviewer behavior is provisioned procedure with no real consumer.

---

## Binding Decisions

### Dispute 1: Grandfathering Disposition

**Positions:**
- **SM (R-N2)**: non-precedential footnote naming well-modeled principles (XI, XII, XIII, XXII, XXIV, XXVI) as positive guidance; explicitly disclaims any procedural force against pre-gate principles. No tiering, no deadline, no migration-candidate list.
- **SCP (revised Rec 4)**: tiered classification *now* (exemplar / tolerated / migration-candidate); migration-candidates (VI, X, XVI, XX, XXI) bound to a v3.0.0 disposition deadline; tolerated principles persist with documented permanent exception listing failing criteria.
- **Pr (revised, withdrew #6)**: defer the entire disposition to a follow-up amendment. Ship the gate prospectively-only. Will accept SM's footnote as fallback if maintainer judges deferral unacceptable; will NOT accept SCP's tiering.

**Synthesizer's assessment:** "the practitioner's defer-to-follow-up is procedurally cleanest — it respects the migration-spec discipline and keeps this amendment's blast radius narrow. SM's footnote is acceptable as a calibration aid if the maintainer judges deferral unacceptable. SCP's tiered classification with deadline is the only proposal with a forcing mechanism, but it is also the only proposal that pre-litigates migration."

**Ruling:** **REJECT (SCP's tiering)** + **ACCEPT (SM's footnote, light form)** + **DEFER (full disposition to follow-up).**

This is a single integrated ruling with three parts because the dispute has three positions:
- SCP's tiered classification with v3.0.0 deadline is **REJECTED**. It is a real concern (grandfathered principles do create calibration risk), but the proposed remedy directly contradicts the gate's own Prospective-Only Migration clause (lines 840-844). The clause expressly states that migrating pre-gate principles "is a separate, intentional act governed by the same amendment process (with the receiving document identified explicitly in the migration spec)." Tiering principles as "migration-candidate" with a v3.0.0 deadline pre-litigates that act without the migration spec actually existing — it hands future authors a procedural lever to demote principles via deadline rather than via the amendment process the constitution mandates. The "permanent exception listing failing criteria" for tolerated principles is precisely the procedural cudgel that two of three reviewers (SM, Pr) explicitly withdrew their own variants of in Phase 3.
- SM's non-precedential footnote in **light form only** is **ACCEPTED**: a single sentence in the gate text stating "future amendments SHOULD be modeled on principles whose verification path is named (e.g., XI, XII, XIII, XXII, XXIV, XXVI)" — *positive guidance only*, naming no "do-not-model-on" principles, asserting no demotion of any principle's ratified status. This is the lowest-friction calibration aid and does not pre-litigate migration.
- Full grandfathering disposition (whether to migrate VI, X, XVI, XX, XXI; whether to tier; whether to set deadlines) is **DEFERRED** to a follow-up spec. Practitioner's diagnosis is correct: shipping a corpus audit with this amendment expands its blast radius from "add a gate" to "audit the corpus."

**Grounding citation:** Prospective-Only Migration (lines 840-844); Backward-Compatible Extension (Principle III, lines 43-55).

**Rationale:** The gate's text already commits to prospective-only migration via separate amendment. Shipping SCP's tiering inside the same amendment that creates the gate would have the gate violate its own scope clause on day one — the strongest possible signal that the gate is not internally coherent. SM's footnote, restricted to positive examples without naming negative ones, provides calibration without demotion. Practitioner's defer-to-follow-up is honored for the substantive corpus audit. SCP's concern that "tolerated status without a deadline is permanent" is real but procedurally addressable: a follow-up spec can debate migration candidates properly, with the migration spec the constitution mandates. Intentional permanence under the original ratification rules is not a defect to be fixed by deadline; it is the prospective-only design's deliberate choice.

**Rejected position:** SCP's tiered classification with v3.0.0 deadline. SCP argues that without a forcing mechanism, the two-tier constitution never collapses. The arbiter's response: collapse should happen via the standard amendment process per the gate's own text, not via deadlines bolted onto the amendment that creates the gate. The argument "footnote is a `# TODO` comment" is not wrong, but the alternative — a deadline that fires regardless of whether anyone has done the migration work — is structurally worse, because it codifies a violation of the prospective-only clause inside the very gate that establishes the clause.

**Required changes:**

In the gate text, after the prospective-only paragraph (current lines 840-844), append a single sentence:

> "When drafting new principles, prefer the structural pattern of principles whose verification artifact is named explicitly (e.g., Principles XI, XII, XIII, XXII, XXIV, XXVI). This is calibration guidance only and does not affect the ratified status of any pre-gate principle."

No other text changes required for this dispute. The migration-candidate list (VI, X, XVI, XX, XXI), tiering, and deadlines do **not** ship with this amendment.

---

### Dispute 2: Criterion 3 Operational Test (Distinctness Block vs. Worked Examples)

**Positions:**
- **SCP (N1)**: structured `Existing-Principle-Distinctness:` block in the PR template citing (a) 2-3 closest existing principles, (b) the novel predicate, (c) why an Extension block would be insufficient. Block as enforcement, examples as calibration.
- **SM (modified Rec 3 + R-N1)**: free-form distinctness statement plus two worked rejection examples in the gate text. Examples bind reviewers; structured blocks become mechanically satisfiable boilerplate.
- **Pr (Rec 4 expanded)**: criteria stay in Governance prose with mandated structural blocks; PR template requires filled blocks; two worked examples (one rejection + one accepted scope-extension citing XXVII as precedent). Lighter structured form than SCP's three-part.

**Synthesizer's assessment:** "the block and examples are not mutually exclusive — practitioner's middle-ground correctly identifies that. The disagreement is about how rigid the block should be. SCP's three-part form is the strongest enforcement surface but introduces 'show your work' overhead that may produce ritualized compliance. SM's free-form is the lightest but provides no enforcement floor beyond 'section non-empty.' Practitioner's lighter structured form (name closest principle + one sentence on insufficiency) is the operational sweet spot."

**Ruling:** **ACCEPT (Practitioner's middle ground).**

This adopts the synthesizer's recommended resolution: ship two worked examples in the gate text (one mechanical-falsifiability rejection, one distinctness/composition rejection); require the PR template's distinctness section to name the closest existing principle and state in one sentence why an Extension would be insufficient. SCP's three-part (a)/(b)/(c) sub-structure is **rejected** for this amendment but reservable for a future revision if the lighter form proves insufficient in practice.

**Grounding citation:** Falsifiable Scope (Criterion 2, lines 822-826); Single Source of Truth (Principle XI, lines 239-256); No Dead Infrastructure (Principle XII, lines 283-305).

**Rationale:** SM's diagnosis that SCP's full block inherits the satisfy-mechanically failure mode is partially correct — author self-certification of "novel predicate" is exactly the rhetoric-as-rigor failure the gate exists to exclude. But SM's "examples-only, free-form section" does provide too thin an enforcement floor: a CI lint can only check for non-empty content, and "I considered other principles and this is distinct" satisfies that vacuously. Practitioner's middle ground — name the closest existing principle and explain insufficiency in one sentence — is the structural minimum that creates falsifiability (a reviewer can disagree with the cited principle being closest, can disagree with the insufficiency claim) without manufacturing a three-part procedure that ritualizes compliance. Worked examples in gate text (SM's contribution) bind reviewers' calibration; the lighter block (Pr's contribution) binds authors' enumeration. Both surfaces are needed and they are complementary, not duplicative.

**Rejected position:** SCP's full three-part block. SCP argues the block "forces authors to enumerate proximate principles and articulate the predicate, which is harder to fake than free-form prose." The arbiter's response: the (b) "novel predicate" sub-field is the weak link — predicate-novelty is exactly what the withdrawn vocabulary-novelty test (SM Rec 7, withdrawn unanimously) failed to operationalize, and "novel predicate" inherits the same failure mode in a different costume. The lighter form (a + (c only — name + insufficiency) preserves the enforceable parts and drops the ceremonial part. Also rejected: SM's examples-only stance, because it leaves the Distinctness section as a checkbox lint with no real enforcement floor.

**Required changes:**

1. In the gate text, immediately after the three numbered criteria (after line 833), insert a new paragraph:

> "**Worked examples.** A principle proposing 'code should be readable' fails Criterion 1: no automated check is feasible. A principle proposing 'all template variables MUST be lowercase' fails Criterion 3: it composes from Principle IX (typing/style discipline) and Principle XI (single source of truth in `schema/variables.yml`); the refinement belongs in IX's body or as a schema constraint, not as a new principle."

2. In the gate text, in the enforcement paragraph that establishes the PR template (per synthesis P1 fix #2), specify that the template's Distinctness section MUST contain: (a) the name of the closest existing principle and (b) one sentence explaining why an Extension block on that principle would be insufficient. The (b)/(c)-style "novel predicate" sub-field is **not** required.

---

### Dispute 3: Extension-Block Treatment

**Positions:**
- **SCP (Rec 8, retained)**: Extension blocks landing post-ratification MUST satisfy criteria 1, 2, 3 even when extending a grandfathered principle.
- **SM (silent)**: cross-review tension #5 noted Extension-block gating retroactively pulls grandfathered principles into the gate, destabilizing the prospective-only design.
- **Pr (silent)**: sidestepped the question; cross-review acknowledged SCP's position is more rigorous but did not adopt it.

**Synthesizer's assessment:** "SCP's diagnosis is correct — without explicit treatment, Extension blocks are a loophole. The other two agents did not engage substantively, so the dispute is asymmetric: one reviewer pressing, two silent. ... Treating Extension blocks as full amendments (subject to all three criteria) is structurally sound but strict; treating them as out-of-scope leaves the loophole."

**Ruling:** **ACCEPT (synthesizer's middle position — Criterion 1 only).**

Extension blocks landing post-ratification of the gate that introduce new normative requirements MUST include the structured `Verification:` block (Criterion 1's artifact requirement). Criterion 3 (distinctness) is implicitly satisfied because the extension is, by construction, an extension of an existing principle; the extension MUST declare why the new content belongs in the parent principle's body rather than as a new principle (which is the inverse of Criterion 3's question and the operational test that prevents Extension blocks from becoming a backdoor for content that should be a new principle). Criterion 2 (falsifiable scope) is enforced by Criterion 1's artifact requirement — if the artifact is named, the scope is by definition falsifiable.

**Grounding citation:** Mechanical Verification Capability (Criterion 1, lines 814-820); Prospective-Only Migration (lines 840-844); Backward-Compatible Extension (Principle III, lines 43-55).

**Rationale:** SCP is correct that the loophole is real and concrete — Principle IX (v2.3.0 Extension), Principle XI (v2.3.0 Extension), Principle XV (v2.3.1 Clarification) postdate ratification of those principles. Without explicit treatment, every grandfathered principle becomes a backdoor admission channel for prose-only additions, and the prospective-only rule has a hole large enough to drive every future amendment through. SM's implicit retroactivity concern is also correct — full-gate application to Extension blocks would convert grandfathering from "existing principles retain ratified status" to "existing principles retain ratified status only until next touched," which is a stricter rule than the constitution states. The middle position resolves both: applying Criterion 1 (the load-bearing artifact requirement) closes the substantive loophole (prose-only normative additions), while exempting Criterion 3 application avoids the retroactivity problem (an Extension to a grandfathered principle does not need to argue distinctness from the principle it is extending — that is incoherent). Pr's and SM's silence is a signal that the dispute was under-engaged in Phase 4, but SCP's diagnosis of the loophole is independently verifiable from the constitution's own corpus (three named Extensions postdate ratification of their parents). The loophole is real; the narrowest fix that closes it without destabilizing grandfathering is the right ruling.

**Rejected position:** Both extreme positions. SCP's full-gate-on-Extensions is rejected because Criterion 3 (distinctness from existing principles) is incoherent when applied to an Extension of an existing principle — the Extension is by construction non-distinct from its parent. SM's and Pr's silent default is rejected because it leaves the loophole open and the constitution's own corpus already shows the pattern in practice.

**Required changes:**

In the gate text, append a new paragraph after the prospective-only paragraph (after the calibration sentence required by Dispute 1):

> "**Extension blocks.** Extension or Clarification blocks added to a grandfathered principle after the gate's ratification MUST include the structured `Verification:` block (Criterion 1) when they introduce new normative requirements. The block MAY cite the parent principle's verification artifact if the extension reuses it. The Distinctness criterion (Criterion 3) does not apply to Extension blocks — by construction, they are extensions of an existing principle — but the Extension MUST declare in one sentence why the new content belongs in the parent principle's body rather than as a new principle. Wording-level clarifications (typo fixes, reformattings, cross-references) are exempt from this rule."

---

## Summary of Changes Required

### REQUIRED FIXES BEFORE MERGE

The synthesis already enumerated the convergent P1 and P2 fixes (structured `Verification:` block, PR template + CI lint + CODEOWNER review bundle, two worked examples, etc.). The arbitration adds the following dispute-resolution fixes on top of those:

1. **Calibration sentence (Dispute 1).** After the prospective-only paragraph (current lines 840-844), append:

   > "When drafting new principles, prefer the structural pattern of principles whose verification artifact is named explicitly (e.g., Principles XI, XII, XIII, XXII, XXIV, XXVI). This is calibration guidance only and does not affect the ratified status of any pre-gate principle."

2. **Worked examples in gate text (Dispute 2).** After the three numbered criteria (after line 833), insert:

   > "**Worked examples.** A principle proposing 'code should be readable' fails Criterion 1: no automated check is feasible. A principle proposing 'all template variables MUST be lowercase' fails Criterion 3: it composes from Principle IX (typing/style discipline) and Principle XI (single source of truth in `schema/variables.yml`); the refinement belongs in IX's body or as a schema constraint, not as a new principle."

3. **PR template Distinctness section (Dispute 2).** In the enforcement paragraph that establishes the PR template, specify the Distinctness section MUST contain (a) the name of the closest existing principle and (b) one sentence explaining why an Extension block would be insufficient. Do NOT require the (a)/(b)/(c) three-part block.

4. **Extension-block treatment paragraph (Dispute 3).** Append after the calibration sentence:

   > "**Extension blocks.** Extension or Clarification blocks added to a grandfathered principle after the gate's ratification MUST include the structured `Verification:` block (Criterion 1) when they introduce new normative requirements. The block MAY cite the parent principle's verification artifact if the extension reuses it. The Distinctness criterion (Criterion 3) does not apply to Extension blocks — by construction, they are extensions of an existing principle — but the Extension MUST declare in one sentence why the new content belongs in the parent principle's body rather than as a new principle. Wording-level clarifications (typo fixes, reformattings, cross-references) are exempt from this rule."

### NOT SHIPPED WITH THIS AMENDMENT (deferred or rejected)

- SCP's tiered classification (exemplar / tolerated / migration-candidate) — REJECTED for this amendment; deferable to a follow-up grandfathering disposition spec.
- SCP's v3.0.0 deadline for migration-candidates — REJECTED.
- SCP's "permanent exception listing failing criteria" for tolerated principles — REJECTED.
- SCP's full-gate Extension-block requirement — REJECTED in favor of Criterion 1 only.
- SCP's three-part `Existing-Principle-Distinctness:` block — REJECTED for this amendment; lighter form adopted.
- Migration-candidate list (VI, X, XVI, XX, XXI) — DEFERRED to follow-up spec.
- "Do-not-model-on" negative-precedent naming in the calibration sentence — REJECTED; positive examples only.

### RECOMMENDED FIXES (borderline; not blocking)

- Synthesis P3 fix #14 (reorder the gate to lead with enforcement) is supported but not load-bearing — accept synthesis's recommendation to ship as P3.
- Synthesis P3 fix #13 (state false-admit/false-reject asymmetry) is calibration-aid; ship as one-sentence clause if word budget allows, otherwise defer.

---

## Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---|---|---|---|
| 1. Grandfathering Disposition | REJECT SCP tiering + ACCEPT SM footnote (light) + DEFER full disposition | High | Gate's own Prospective-Only Migration clause directly forbids the SCP remedy; two of three reviewers preferred the lighter resolution. |
| 2. Criterion 3 Operational Test | ACCEPT Practitioner middle ground | High | Synthesizer explicitly identified this as the operational sweet spot; both extreme positions have known failure modes (mechanical satisfaction or vacuous lint). |
| 3. Extension-Block Treatment | ACCEPT synthesizer's middle position (Criterion 1 only) | Medium-High | Loophole is concrete and demonstrable in the corpus; full-gate application is structurally incoherent for Criterion 3; the narrowest fix that closes the loophole without retroactivity is the disciplined choice. Pr and SM's silence is a procedural concern but not a substantive objection. |

### Overall Deliberation Quality

The deliberation produced exceptionally strong convergence on the load-bearing fixes (structured `Verification:` block, PR template + CI lint + CODEOWNER review as a non-separable bundle, withdrawal of governance auto-anything) and properly defeated each agent's most aggressive simplification proposals through symmetric cross-review pressure. The three remaining disputes are not failures of the deliberation — they are the residual content where reviewers' lenses diverged on real tradeoffs. The synthesizer's framing of each dispute is accurate and the recommended resolutions for Disputes 2 and 3 are adopted with minor refinement. Dispute 1's resolution diverges slightly from the synthesizer's recommendation by adopting SM's footnote (in light form) rather than treating it as merely fallback — the calibration value of positive guidance is small enough that shipping it costs nothing and large enough that it makes the gate's intent legible to future authors.

The blind methodology held: the gate is judged on its own internal coherence (does it satisfy its own Prospective-Only Migration clause? Does it avoid the Single-Source-of-Truth duplication trap? Does it avoid Dead Infrastructure?) rather than on incumbency. The gate, with the synthesis's convergent P1/P2 fixes plus the four arbitration fixes above, satisfies all three of those tests. Without those fixes, it would not — particularly the original "sketch in one paragraph" sub-clause, which would have failed the gate's own Criterion 1 if applied to itself.

---

SPEC-069 BLIND VERIFICATION VERDICT: PASS WITH FIXES
