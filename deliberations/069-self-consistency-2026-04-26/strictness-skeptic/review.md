# Strictness-Skeptic Review — Constitutional Inclusion Criteria (v2.4.0)

**Role**: strictness-skeptic
**Methodology**: self-consistency (v2.4.0 markers visible)
**Target**: `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-self-consistency-2026-04-26/CONSTITUTION-v2.4.0-candidate.md`
**Position**: The proposed gate is too strict and structurally mis-calibrated. It would have rejected principles that have empirically generated value, and as written it will systematically push qualitative-but-essential invariants out of the constitution and into operational guidance — where they will drift, degrade, and disappear.

---

### Executive Summary

The Constitutional Inclusion Criteria added to §Governance in v2.4.0 enumerates three requirements (mechanical verification capability, falsifiable scope, distinct from existing) joined by an implicit AND ("only if it satisfies **all three**"). Spec 069 §5's worked-examples analysis concedes that 3 of 27 grandfathered principles — VI (Scripts Over Markdown), X (Zen of Python Output), and XVI (Mathematical Transparency) — would fail this gate today. The drafters treat this as acceptable collateral via grandfathering. It is not acceptable. A gate calibrated correctly should approximately reproduce the existing constitution it is governing. A gate that would reject ~11% of its own corpus is not a high bar — it is a wrong bar.

The deeper problem is structural. The three criteria are AND'd, so a principle must clear *all three* tests. But the criteria are not equally load-bearing: mechanical verification is a desirable property; distinctness is a hygiene property; falsifiable scope is the actual *gating* property. AND'ing a value test with a hygiene test with a tooling test produces a screen biased against precisely the kind of foundational, cross-cutting, qualitative invariants (taste, transparency, output ergonomics, executability-of-prose) that distinguish a constitution from a linter ruleset. The grandfathering escape hatch admits this implicitly: the drafters know the gate would have starved the document, and they are protecting the past from the gate while subjecting the future to it.

This review identifies six concrete miscalibrations, three plausible future principles the gate would wrongly reject, and recommends restructuring the AND into a weighted two-of-three with criterion 2 (falsifiability) as required, criteria 1 and 3 as either-or, plus a softening of criterion 1's "concrete one-paragraph sketch" requirement.

---

### Alignment (where the gate is correctly calibrated)

1. **The grandfather clause is correctly scoped.** Principles I–XXVII are not retroactively re-evaluated. This is the right call: re-litigating settled invariants under a new gate would destabilize the document's authority. The grandfathering acknowledges that the gate is a forward-looking filter, not a purge order.

2. **Criterion 2 (falsifiable scope) is the correct primary gate.** Constitutions adjudicate disputes; disputes require falsifiability. A principle that cannot flag a hypothetical violation cannot govern. This criterion is load-bearing and well-worded.

3. **Criterion 3 (distinct from existing) prevents principle inflation.** v2.3.0 already added 6 principles + 2 extensions in a single amendment. Without a duplication check, the document would balloon. The "extend the existing principle's body, not as a new principle" instruction is a clean, actionable rule that mirrors the v2.3.0 IX/XI extensions pattern.

4. **The "operational guidance" sink is correctly named.** Routing rejected proposals to `CONTRIBUTING.md`, the relevant spec, `SKILL.md`, or domain references gives reviewers a real destination, not a wastebasket. This is better than the alternative ("just reject it") because it preserves the proposing author's effort.

5. **Prospective application is the right policy choice.** Applying the gate to *future* amendments only avoids the chilling effect of immediate enforcement against a corpus the gate was clearly not calibrated against.

6. **The amendment is correctly versioned MINOR.** Adding a procedural gate is a material expansion of governance, not a clarification (PATCH) and not a removal/redefinition (MAJOR). v2.4.0 is correctly chosen.

---

### Missed Opportunities (where the gate is too strict or mis-calibrated)

#### MO-1. The AND'ing of the three criteria is the central structural error.

The text reads: "a principle qualifies for constitutional inclusion only if it satisfies **all three**." This is a logical conjunction. But the three criteria are heterogeneous:

- **Criterion 1** (mechanical verification capability) is a *tooling-feasibility* test.
- **Criterion 2** (falsifiable scope) is a *clarity-of-wording* test.
- **Criterion 3** (distinct from existing) is a *hygiene* test.

Conjunction on heterogeneous criteria over-rejects. A principle that is unambiguously falsifiable (passes 2), unambiguously novel (passes 3), but happens to govern a domain where a mechanical check is genuinely awkward (fails 1) gets rejected — even though its constitutional value is high.

Worked example: a hypothetical Principle XXVIII "Privacy of User Inputs" — "user-supplied prompt content MUST NOT be logged to telemetry, written to artifacts on disk, or embedded in error messages without explicit operator opt-in." This is sharply falsifiable (criterion 2 PASS), distinct from existing principles (criterion 3 PASS), but mechanical verification requires data-flow analysis across the codebase that is *expensive* to build a CI lint for. Under the current AND, this principle is rejected. Under a weighted two-of-three, it qualifies.

**Recommendation**: convert the AND on criteria 1 and 3 to an OR, and require criterion 2 unconditionally. See Recommendation R-1.

#### MO-2. Criterion 1's "concrete one-paragraph sketch" bar is too high for cross-cutting invariants.

The text reads: "the path to building it MUST be concrete enough that an engineer reading the principle can sketch the check in one paragraph." This biases the gate toward *local* invariants (one file, one schema, one parser) and against *cross-cutting* invariants (architectural taste, output coherence, mathematical legibility).

Principle X (Zen of Python Output) cannot be sketched as a one-paragraph CI check. "Errors should never pass silently" is locally checkable; "sparse is better than dense" is not. "If the implementation is hard to explain, it's a bad idea" is fundamentally a peer-review criterion, not a lint. Yet Principle X has demonstrably influenced design — the flat output tree in `summary/`, `{agent}/review.md`, the warning-not-blocking semantics in V — and removing it would weaken the document's voice.

Principle XVI (Mathematical Transparency) similarly fails the one-paragraph sketch test. "Plain-language explanations alongside numerical outputs" is checkable per artifact, but the broader principle ("users parameterize the math; they do not need to understand it") is an *interface taste* invariant. Spec 069 §5 admits XVI would fail and proposes routing future analogous principles to operational guidance. This will systematically downgrade taste-level invariants.

**Recommendation**: weaken criterion 1 from "concrete enough to sketch in one paragraph" to "at least one observable failure mode is amenable to mechanical or peer-review-based detection." See Recommendation R-2.

#### MO-3. The gate has no vocabulary for *foundational* principles that govern the constitutional grammar itself.

Principles VI (Scripts Over Markdown) and IV (Documentation Is the Product) are in tension; VI says "prefer scripts" and IV says "in a prompt-orchestrated system, specification text IS the implementation." This tension is *generative* — it is exactly the kind of dialectical pair that gives a constitution depth. Under the new gate, VI fails criterion 2 (falsifiable scope: "when an artifact drives behavior" is judgment-laden — a reviewer must reason "well, X drives behavior in some sense"). The drafters concede this in spec 069 §5.

But VI is doing real work: it is the principle that justifies why `schema/variables.yml` is YAML and not markdown, why `mode_in_phases` lives in YAML and not in SKILL.md prose, why `conversus.yml` is structured config. Its failure under the gate is a *false negative* of the gate, not a real defect of VI.

The gate has no concept of a *meta-principle* — a principle whose primary function is to shape the form of *other* artifacts in the system. Such principles are inherently broader and less mechanically checkable than domain principles, and AND'ing them through criterion 1 is wrong.

**Recommendation**: add an explicit carve-out for meta-principles, or accept that criterion 1 is satisfied when "the principle is *cited by* the construction of other mechanically-checkable artifacts." See Recommendation R-3.

#### MO-4. Criterion 3 (distinct from existing) is under-specified about *how distinct* is distinct enough.

The text says "covers concerns not already addressable by composing existing principles." But composition is a reasoning move; for any new principle, a sufficiently determined reviewer can construct a composition path from existing principles. Principle XXVII (Operator-Configurable Tool Surface) could plausibly be derived from XV (Plugin Isolation) + III (Backward-Compatible Extension) + XI (Single Source of Truth). The 2026-04-25 arbiter ruled it standalone anyway, on the (correct) judgment that *coordinative wording with XV* required it to be standalone rather than buried.

A literal application of criterion 3 to a future analogue would reject the proposal because composition is "available." This punishes the very kind of explicit coordination that v2.3.0/v2.3.1 prized (XV ↔ XXVII clarification, IX extension for behavior-over-shape).

**Recommendation**: reword criterion 3 to require "covers concerns not *cleanly* addressable by composing existing principles, where 'cleanly' means the composition would not require operators or contributors to *infer* the coordination at runtime." See Recommendation R-4.

#### MO-5. The grandfathering admission is evidence the gate is mis-calibrated, not evidence the gate is sound.

Spec 069 §5 frames grandfathering as a feature: "Existing principles I-XXVII are grandfathered." But a well-calibrated gate should approximately reproduce its own corpus. If 3 of 27 (~11%) of grandfathered principles would fail a forward-going gate, the gate is rejecting at a rate that *exceeds* the historical false-positive rate of the constitutional amendment process itself (zero principles have been removed; the worst case has been extension/clarification). The gate is therefore configured to be more aggressive than any historical reviewer.

This is not a stable equilibrium. Future amendments authored under the gate will produce a constitution whose voice and breadth differ from the grandfathered corpus, creating a stylistic discontinuity at v2.4.0 that future contributors will notice and have to work around.

**Recommendation**: calibrate against the corpus. If the gate would reject more than ~5% of historical principles, loosen until it would reject fewer. See Recommendation R-5.

#### MO-6. The gate has no failure mode for *false positives* (admitting bad principles).

The criteria are all AND'd against admission. There is no symmetric review for principles that pass the gate but turn out to be redundant, vague-in-practice, or inert. The v2.3.0 deliberation produced 6 new principles in a single amendment; if the gate had been in place, it would have filtered which of those passed, but it would not have provided any retrospective check on the survivors. Distribution Surface Integrity (XXII), Provider Robustness Contract (XXIII), and Safety-Critical Defense-in-Depth (XXIV) are all credible — but XXII and XXIII overlap on "test from a fresh environment in CI" (XXII.3) and "every safety-critical path has at least one test that reproduces the original bug" (XXIV.3). A symmetric retrospective review at the next MINOR would catch this.

**Recommendation**: pair the inclusion gate with a retrospective review at every MINOR amendment, checking whether prior new principles have been cited, enforced, or would fail their own gate today. See Recommendation R-6.

#### MO-7. The gate does not distinguish between principles that constrain *behavior* and principles that constrain *form*.

Principle II (Stable Interfaces) is a behavioral constraint: don't break dispute-marker syntax. Principle X (Zen of Python Output) is a form constraint: produce clean output. Principle XVI (Mathematical Transparency) is a form constraint: produce legible explanations alongside numerical outputs. The gate's criterion 1 (mechanical verification) is well-suited to behavioral constraints (you can lint for marker syntax) and ill-suited to form constraints (you cannot lint for legibility).

The grandfathered corpus contains roughly 9 form constraints (IV, V, VI, X, XVI, XVII, XVIII narrowly, XX, XXI). Under the new gate, the rate at which form constraints are admitted will drop sharply, because they consistently struggle with criterion 1. This will skew the constitution toward behavioral and away from formal/aesthetic concerns — exactly the opposite of what a "Documentation Is the Product" / "Specification text IS the implementation" system should do.

**Recommendation**: explicitly recognize form constraints as a category and relax criterion 1 for them. See Recommendation R-7.

#### MO-8. The gate's "operational guidance" sink will degrade what it receives.

Operational guidance documents (`CONTRIBUTING.md`, `SKILL.md` instructions, domain reference docs) are *consumed differently* from the constitution. They are read by contributors when starting work, not by reviewers when adjudicating disputes. A principle relegated to `CONTRIBUTING.md` does not show up in conversus deliberation prompts (which load constitution text). It does not show up in `/speckit.constitution check`. It is, in practical effect, downgraded from "binding invariant" to "suggestion."

This is a one-way ratchet: principles that are *currently* operational (e.g., "use Pydantic for config validation") are sometimes promoted to constitutional status when they prove load-bearing (Principle IX absorbed explicit-typing requirements in 2.0.x). The gate creates the demotion path but not the promotion path; this asymmetry will accumulate.

**Recommendation**: define the *promotion* criteria for moving guidance back into the constitution, symmetric to the demotion criteria. See Recommendation R-8.

#### MO-9. Criterion 1's "the check does NOT have to exist at amendment time" is a loophole that will be abused.

The text says the check is sketchable, not that it must exist. This is sensible — building lints lags principle creation. But the loophole means a sufficiently determined author can satisfy criterion 1 by handwaving "an engineer could imagine a parity test for this" for almost any principle. Conversely, a principle whose author *honestly* cannot sketch a check (because the principle is a cross-cutting form constraint) gets rejected. The criterion thus rewards rhetorical confidence, not actual checkability.

**Recommendation**: require either (a) a sketched check OR (b) a citation of an existing peer-review prompt or rubric that operationalizes the principle. See Recommendation R-9.

---

### Off-Base Assumptions

#### OB-1. The gate assumes principles are independent units that can be admitted or rejected one at a time.

In the v2.3.0 deliberation, 4 of the new principles were admitted *together* on the strength of inter-principle coordination (XXII–XXVI all touch distribution/testing/safety boundaries). The gate has no representation for "this principle is weaker alone but strong as part of a coordinated bundle." Under the gate, each must clear independently — which would have produced a different (and probably worse) v2.3.0.

#### OB-2. The gate assumes "operational guidance" is a stable, well-defined location.

In practice, `CONTRIBUTING.md` does not exist in this repo (root-level search would find no file by that name). `SKILL.md` is heavily structured around runtime orchestration, not contribution rules — by Principle XVII (Content Classification), contribution guidelines belong in `AGENTS.md`. Domain reference docs are loaded conditionally (Principle XVIII). The gate hand-waves a destination that is itself underspecified; a rejected principle has no canonical home.

#### OB-3. The gate assumes the cost of a missed-good principle equals the cost of a wrong-admitted principle.

The asymmetry runs the other way. An admitted principle that is later found redundant can be migrated out (the text explicitly provides the mechanism). A *rejected* principle that should have been admitted leaves a constitutional gap that may not be detected until a real-world failure (cf. PRs #5–#11 producing the v2.3.0 amendments). Asymmetric costs should produce asymmetric gates: prefer Type II errors (admit a few weak principles) over Type I errors (reject a few strong ones).

#### OB-4. The gate assumes "self-consistency methodology" eliminates reviewer bias toward strictness.

The v2.4.0 markers in the candidate document advertise that this amendment was authored under self-consistency. But self-consistency reduces variance, not bias. If the underlying disposition of the deliberating agents skews toward "more rigor is better," self-consistency will produce a *consistent* over-strict gate rather than a calibrated one. The grandfathering admission is the smoking gun: the agents themselves notice that the gate would reject some of its own corpus and treat that as acceptable.

---

### Hypothetical Future Principles the Gate Would Wrongly Reject

#### HF-1. "Prompt Compactness" — every load-trigger-resolved bundle stays under N tokens.

Wording: "The total context loaded by any single subcommand invocation MUST stay under a documented per-subcommand budget. Exceeding the budget without a corresponding budget amendment is a regression." This is a form constraint about output of the load process. Falsifiable (criterion 2 PASS — there is a token count). Distinct from existing (criterion 3 PASS — Principle XVIII speaks to root SKILL.md size, not per-invocation totals). But criterion 1 is *checkable in principle* yet operationally hard: token counts vary by tokenizer, model, and content. A reviewer might rule "the path to a check is not concrete enough." Under the AND, rejected.

This is exactly the kind of empirical engineering invariant a maturing system needs.

#### HF-2. "Adversarial Symmetry" — no agent in a deliberation gets context the others don't.

Wording: "All agents in a single phase MUST receive structurally identical context. Privileged context (agent-specific extra files, cached prior reviews) is prohibited unless explicitly part of the mode definition." This is a fairness invariant for adversarial deliberation. Falsifiable (criterion 2 PASS — the orchestrator either passes the same files or it doesn't). Distinct from existing (criterion 3 borderline — XIX mentions "each agent is context-isolated" but does not explicitly require *symmetry*). Criterion 1: mechanically checkable via hash comparison of agent prompts.

This one might pass — but it might also be rejected on criterion 3 ("addressable by composing XIX with V"). A determined reviewer could argue either way, which means the gate produces high variance on a high-value principle.

#### HF-3. "Reproducibility of Synthesis" — given identical phase 1–5 outputs, phase 6 synthesis MUST be deterministic up to LLM sampling noise.

Wording: "Re-running phase 6 against the same upstream artifacts MUST produce structurally identical synthesis (same dispute count, same headline structure, same arbitration triggers) modulo LLM sampling noise. Structural variance is a bug." This sharpens VII (Reproducibility) for a specific phase. Falsifiable (criterion 2 PASS). Mechanically verifiable (criterion 1 PASS — diff two synthesis runs). Distinct from VII? Borderline — VII says "structurally identical output," and a strict reviewer would route this to a VII extension.

The gate would correctly route this to a VII extension. But the asymmetry is informative: when the gate works, it produces extensions of existing principles, never new principles. Over time this will produce a constitution that is broad-but-shallow at the edges and ossified at the core.

---

### Actionable Recommendations

**R-1 (highest priority): Convert criterion 1 AND criterion 3 to an OR, with criterion 2 required.**
Replace "satisfies all three" with: "satisfies criterion 2 (falsifiable scope), AND satisfies at least one of criterion 1 (mechanical verification) or criterion 3 (distinct from existing)." This admits principles that are sharply worded and either checkable-or-novel, while still rejecting principles that are vague (fail 2) or are checkable restatements of existing rules (pass 1, fail 2 and 3).

**R-2: Weaken criterion 1's "one-paragraph sketch" requirement.**
Change to: "at least one observable failure mode is amenable to mechanical detection, peer-review rubric, or test-against-historical-incident." This admits form constraints whose checks live in human review rather than CI.

**R-3: Add a meta-principle carve-out.**
After criterion 3, add: "Principles whose primary function is to shape the form of other artifacts (config formats, output structure, mathematical legibility) are evaluated against criterion 1 by their *citation in the construction of mechanically-checkable artifacts*, not by direct sketchability of a check." This gives VI, X, XVI a defensible category.

**R-4: Sharpen criterion 3 with a "cleanliness" qualifier.**
Replace "not already addressable by composing existing principles" with "not *cleanly* addressable by composing existing principles, where cleanly means contributors and reviewers do not have to infer the coordination at runtime." This preserves the spirit (no near-duplicates) while admitting principles whose value is explicit coordination (XV ↔ XXVII).

**R-5: Calibrate against the corpus.**
Add a sentence: "This gate is calibrated such that it would admit at least 90% of the grandfathered principles I-XXVII if applied retroactively. Future tightening of the gate requires re-verifying this calibration." This anchors the gate's strictness to historical evidence.

**R-6: Pair with a retrospective review at each MINOR.**
Add: "Each MINOR amendment MUST include a retrospective review of principles added in the prior MINOR, checking citation rate, enforcement, and gate-pass status under current criteria. Principles found inert are candidates for migration to operational guidance." Symmetric admission/migration prevents one-way accumulation.

**R-7: Recognize form constraints explicitly.**
Insert before criterion 1: "Principles are categorized as *behavioral* (constraining what the system *does*) or *formal* (constraining what its outputs *look like*). Criterion 1 applies in full to behavioral principles. For formal principles, criterion 1 is satisfied if the principle can be cited in a peer-review rubric or affects the construction of a mechanically-checked artifact." This is the cleanest fix.

**R-8: Define the promotion path.**
Add a third sub-section after the "operational guidance" routing: "Operational guidance items MAY be promoted to constitutional principles if they (a) are cited as authoritative in three or more specs, (b) survive a deliberation review, and (c) pass the inclusion gate as amended. Promotion requires the same MINOR amendment process as new principles." Symmetric to demotion.

**R-9: Tighten criterion 1's loophole.**
Change "The check does NOT have to exist at amendment time, but the path to building it MUST be concrete enough" to: "The check does NOT have to exist at amendment time, but EITHER (a) the path to building it MUST be sketched in the amendment rationale, OR (b) the principle MUST cite an existing peer-review prompt or rubric that operationalizes it." This closes the handwaving loophole while keeping the door open for review-based enforcement.

**R-10: Document the failure mode of the gate itself.**
Add a final sentence to the §Governance Constitutional Inclusion Criteria block: "The gate is itself subject to constitutional review. If a future deliberation finds that the gate has rejected three or more proposed principles that were later validated by real-world incidents, the gate MUST be loosened in the amendment that follows." This makes the gate falsifiable on its own terms — fitting for a self-consistency-authored amendment.

---

### Referenced Documentation

- **Target document**: `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-self-consistency-2026-04-26/CONSTITUTION-v2.4.0-candidate.md` (lines 872–905 for the new gate; lines 146–159 for VI; lines 278–296 for X; lines 448–478 for XVI; lines 627–826 for the v2.3.0 additions XXII–XXVII as calibration anchors)
- **Spec 069 §5 worked-examples analysis** (referenced in the prompt, asserts 3 of 27 grandfathered principles fail the gate)
- **v2.3.0 Sync Impact Report** (lines 23–60 of target) documenting the 6-new-principles + 2-extensions amendment that this gate would have filtered
- **v2.3.1 Sync Impact Report** (lines 1–21) documenting the XV/XXVII coordination clarification — used here as evidence that explicit coordination between principles has constitutional value the gate undervalues
- **CONSTITUTIONAL_CONVERSATIONS.md** governance log (referenced at lines 17–18, 56–57, 822) — the historical record against which the gate's calibration should be checked

---

**Bottom line**: the gate's criterion 2 is correct. Its criterion 3 is hygiene-good but vulnerable to literal application. Its criterion 1, AND'd with the others and with a "concrete one-paragraph sketch" bar, is the structural defect — it systematically rejects form constraints, meta-principles, and cross-cutting taste invariants, exactly the categories that distinguish a constitution from a linter. The grandfathering admission is the gate authors' own acknowledgement that the calibration is off. R-1 (AND→partial-OR), R-2 (sketch→peer-review-allowed), and R-7 (form-constraint carve-out) are the three most important fixes. Adopt them and the gate becomes a calibrated filter; leave them and v2.4.0 quietly closes the door on the next Principle X.
