# Practitioner Review — Constitution v2.4.0 Self-Consistency

**Persona**: Pragmatist (future amendment author)
**Target**: `CONSTITUTION-v2.4.0-candidate.md` — the Constitutional Inclusion Criteria gate added under Governance
**Lens**: If I am writing the next amendment (v2.5.0 or v2.4.1), can I actually use this gate without phoning a maintainer?

---

## Executive Summary

The v2.4.0 gate is *directionally correct* and *operationally fragile*. The three criteria (mechanical verification capability, falsifiable scope, distinct from existing principles) describe real failure modes that have actually happened in this constitution's history — Principle XXVII almost duplicating XV, the v2.3.0 "behavioral validation per domain" sprawl that Principle IX's extension consolidated, and the dead-infrastructure cluster (XII–XIV) that could each have been merged into XI if anyone had run this gate. So the criteria are *retrodictively justified*: if applied earlier, they would have caught real bugs.

But as a *prospective* tool for an amendment author, the gate has three practitioner-level problems. First, criterion 1 ("the path to building it MUST be concrete enough that an engineer reading the principle can sketch the check in one paragraph") sets an ambiguity threshold I cannot calibrate without a worked example. The constitution offers none. Second, the gate is described as a self-assessment with no enforcement hook — the speckit pipeline does not currently lint amendment PRs, and "Use `/speckit.constitution`" is the only governance-process bullet. A self-assessment without a CI gate is a rubber stamp by default. Third, the boundary between "constitution" and "operational guidance" is named (`CONTRIBUTING.md`, the relevant spec, `SKILL.md`, domain reference docs) but the routing rule is flat — "fails any criterion belongs in operational guidance" — with no guidance on *which* operational document should receive it. An author who's been told their proposed principle fails criterion 2 still has to make a four-way choice with no decision tree.

The slowdown to legitimate amendments is real but small (probably one extra deliberation round, or one author-side iteration). The bug-prevention value is large *if* the gate is enforced, near-zero if it remains advisory. The recommendations below focus on making the gate enforceable and giving amendment authors enough scaffolding to apply it without maintainer interpretation.

**Bottom line**: ship the gate, but with a self-assessment template embedded in the spec template, an amendment-PR CI lint that requires the template to be filled in, and an explicit routing table for the four operational-guidance destinations.

---

## Alignment — Where the Gate Is Operationally Usable

The gate has real strengths that a future amendment author can lean on:

1. **The three criteria each map to a recognizable failure mode.** Criterion 1 catches "vibes principles" (Principle X "Zen of Python Output" would arguably fail this — but it's grandfathered). Criterion 2 catches mushy invariants like "code should be clean." Criterion 3 catches near-duplicates like the early version of XXVII before the arbiter split it from XV. An author who reads these criteria recognizes the failure mode in their own draft.

2. **Grandfathering is explicit and bounded.** "Existing principles I-XXVII are grandfathered. Migrating any of them to operational guidance is a separate, intentional act governed by the same amendment process." This prevents the gate from becoming a Trojan horse for re-litigating the existing 27 principles. An author proposing v2.5.0 can ignore the prior corpus and only defend their new contribution. That's a usable boundary.

3. **Criterion 1 hedges correctly on tooling cost.** "The check does NOT have to exist at amendment time, but the path to building it MUST be concrete enough that an engineer reading the principle can sketch the check in one paragraph." This is the right tradeoff — requiring the lint to exist before the principle merges would slow amendments to a crawl. Allowing a sketched implementation path keeps velocity while preventing pure aspirational principles. The XXVI meta-test pattern is the obvious worked example: principle merged before every parametrized capability set had a meta-test, but the path was clear.

4. **The operational-guidance escape valve is correctly framed as a *destination*, not a *demotion*.** "Operational guidance is the explicit home for 'judgment calls' and 'rules of thumb'; the constitution is the home for invariants." This wording matters — it tells an amendment author that being routed to `CONTRIBUTING.md` is not a rejection, just a different file. That changes author behavior: they're more likely to propose well-scoped operational rules instead of overreaching for constitutional status.

5. **The version-bump rule (PATCH for v2.4.0) is internally consistent.** Adding the gate doesn't add or remove a principle — it adds a meta-rule about *how* principles get added. That's a clarification, hence PATCH. The Sync Impact Report top section shows v2.3.0→2.3.1 PATCH for the XV clarification; v2.3.1→2.4.0 should arguably also be PATCH if consistency with prior precedent matters. (See Off-Base Assumptions #1.)

6. **The gate composes cleanly with Principle XI (Single Source of Truth).** Criterion 3 ("distinct from existing principles") is essentially XI applied to the constitution itself: don't duplicate principles. That's a nice piece of constitutional self-reflection — the document eats its own dogfood.

---

## Missed Opportunities — Where Friction or Unenforceability Is High

These are the places I, as a future amendment author, would get stuck:

1. **No self-assessment template.** The gate says "satisfies all three" but provides no form, checklist, or template for the amendment PR. I would have to write three free-form paragraphs from scratch and hope they meet the bar. A reviewer would have to free-form-evaluate them. A template (one paragraph per criterion, with a worked example in the spec) would convert this from a judgment call into a fill-in-the-blank exercise. This is the single highest-leverage gap.

2. **No CI hook is named, even speculatively.** The Compliance bullet says "The plan template includes a Constitution Check gate. Plans MUST pass this gate before proceeding to implementation." But that gate is for *plans*, not for *amendments to the constitution itself*. There is no mechanical check on amendment PRs. A future amendment that violates criterion 3 (duplicates an existing principle) would not fail any test — it would only fail if a reviewer notices. The gate is a self-assessment with no second pair of eyes mechanically required.

3. **Criterion 1's "one paragraph sketch" threshold is uncalibrated.** What counts as concrete? "A CI lint could grep for X" is one paragraph. So is "a parity test could compare the registry to the manifest." Both are vague. The constitution does not show me a pass example or a fail example. Without a worked dichotomy, I will write the most defensible paragraph I can and trust the reviewer's interpretation — which is exactly the failure mode criterion 2 is trying to prevent. The gate's own criterion 1 fails its own criterion 2.

4. **Criterion 2's "without requiring interpretation" is itself an interpretation.** Every principle requires *some* interpretation when applied to a specific PR. Principle XXIV (Safety-Critical Defense-in-Depth) requires interpreting "safety-critical" — the principle defines the term explicitly, but a reviewer still has to judge whether a new path is safety-critical. That's interpretation. Criterion 2 as written would arguably reject XXIV. The criterion needs a phrase like "without requiring interpretation *of the principle's scope* — the principle MUST define its scope explicitly" to track what XXIV actually does well.

5. **The boundary between "refining/extending an existing principle" and "new principle" is fuzzy.** Criterion 3 says "Refining or extending an existing principle goes in that principle's body, not as a new principle." The v2.3.0 amendment did this twice (extensions to IX and XI). But XXVII was split off from XV instead of folded in, and the rationale ("operator configuration scope extends beyond plugin isolation to the core tool surface") is a judgment call. A future author drafting "Operator Audit Logging" could plausibly argue it's a new principle OR an extension of XXVII. The gate does not give me a discriminator.

6. **No routing table for the four operational-guidance destinations.** "`CONTRIBUTING.md`, the relevant spec, `SKILL.md` instructions, or domain-specific reference documents" is a flat list. Which gets what? A naming-convention rule clearly belongs in `CONTRIBUTING.md`. A runtime-enforced check belongs in `SKILL.md` or its references. But what about a code-review heuristic that's mechanical-ish but only applies to one subsystem? An amendment author reading this list has to make a four-way choice with no decision tree. Principle XVII (Content Classification) actually gives a good two-way split (execution logic → SKILL.md, contribution guidelines → AGENTS.md) that the v2.4.0 gate could cite directly.

7. **The gate doesn't mention the "blind verification" deliberation pattern that produced the v2.3.1 fix.** The Sync Impact Report at the top of the document tells me a 3-agent blind deliberation found a remainder fix that the original v2.3.0 deliberation missed. That's strong evidence for *requiring* a verification deliberation as part of the amendment process. Spec 066 §7's "Run a verification deliberation against this amended text to catch inter-principle conflicts" is mentioned in the prior sync report's Follow-up TODOs but not codified into Governance. The v2.4.0 gate is the natural place to lift that practice from a TODO into a procedural requirement.

8. **No friction model for low-cost amendments.** Some amendments are tiny (typo fix, cross-reference update, single-word clarification). The gate as written would technically apply to any amendment. PATCH-level clarifications probably should *not* require the three-criterion self-assessment — they're not adding a principle, they're refining one. The gate's grandfathering clause says "Migrating any of them to operational guidance is a separate, intentional act governed by the same amendment process" but doesn't carve out PATCH refinements. A future author proposing a one-line clarification will either skip the gate (treating it as MINOR-only) or fill in three paragraphs of throat-clearing for a typo fix. Neither is good.

9. **No precedent-tracking discipline.** Once the gate is in force, decisions like "we routed proposal X to `CONTRIBUTING.md` because it failed criterion 2" become precedent. There is no log, no decision record, no place where a future author can read "here's how prior amendments interpreted criterion 1." Without this, every amendment re-litigates the criteria. Spec 066 §8 Q3 is the closest thing — but it's a one-time decision log, not an ongoing precedent registry. A `deliberations/governance-decisions.md` log indexed by criterion would solve this.

---

## Off-Base Assumptions

Two assumptions in the gate are doing more work than they should:

1. **The version-bump rule treats this as MINOR (v2.3.1 → 2.4.0).** The Sync Impact Report's *opening paragraph* is for a different change (v2.3.0 → 2.3.1 XV clarification, PATCH). The v2.4.0 bump itself does not have a sync impact report at the top of the file, even though it should — it adds a new Governance subsection that materially changes how future amendments are processed. A pragmatist reading this would expect a v2.4.0 sync impact report explaining: (a) what's new (the inclusion criteria), (b) which existing principles are grandfathered (all of I–XXVII), (c) which templates need updating (the amendment PR template, if one exists). The absence of this report is itself a self-consistency violation: the constitution requires sync impact reports for amendments, and this amendment does not have one for its own version bump.

2. **"Self-assessment" is treated as a viable enforcement mode.** The word "self-assessment" appears nowhere in the gate text — the user's framing introduced it. But the gate as written is functionally a self-assessment: an amendment author writes the principle, the author claims it satisfies the three criteria, the reviewer evaluates the claim. There is no third-party check, no automated lint, no required external verification. In every other part of this constitution, self-assessment is treated as inadequate (Principle V: "Output validation MUST catch malformed results"; Principle XXIV: three-layer defense including parser-level validation independent of schema). The gate's enforcement model is inconsistent with the constitution's broader "defense in depth" stance. If the gate is worth having, it deserves a parity test or amendment-PR lint, not just an honor system.

3. **The gate assumes amendments come through `/speckit.constitution`.** The Governance section says "Amendments: Require documentation of the change, rationale, and impact on existing specs. Use `/speckit.constitution` to update." But emergency amendments (security disclosures, regulatory changes) might bypass speckit. The gate has no provision for expedited paths, nor does it specify which criteria can be relaxed under what conditions. This is a small gap in normal operation but a significant one for incident response.

---

## Actionable Recommendations

Concrete changes to make the gate usable for a future amendment author:

1. **Add a self-assessment template to the amendment spec template, not just to Governance.** The template should be three named sections — "Mechanical Verification (criterion 1)", "Falsifiable Scope (criterion 2)", "Distinctness (criterion 3)" — with one worked example each. The example for criterion 1 could be Principle XXVI's meta-test pattern. The example for criterion 3 could be the XV/XXVII split rationale. Without worked examples, the criteria are unfalsifiable in the same way the gate accuses bad principles of being.

2. **Codify a CI lint for amendment PRs that requires the self-assessment template to be filled in.** This does not have to be sophisticated — a simple grep that fails the PR if `## Mechanical Verification` is missing or empty. The lint enforces the *form* of self-assessment even before semantic enforcement is feasible. This is the minimum credible enforcement hook and matches Principle XXII's "force-include discipline" pattern (declare it explicitly or it doesn't ship).

3. **Add a routing table mapping amendment-failure modes to operational-guidance destinations.** Format: "Fails criterion 1 (no mechanical check) AND is a contribution rule → `AGENTS.md`. Fails criterion 1 AND is a runtime-enforced rule → `SKILL.md` or references. Fails criterion 2 (vague scope) → the relevant spec's clarifications section. Fails criterion 3 (duplicate) → fold into the existing principle's body as an extension." This converts the four-way choice into a decision tree. Cite Principle XVII (Content Classification) as the precedent for this kind of routing.

4. **Carve out PATCH-level amendments from the three-criterion self-assessment.** Add a sentence: "PATCH amendments (clarifications to existing principles, cross-reference updates, wording refinements) are exempt from the three-criterion self-assessment but MUST still document the clarification rationale in the Sync Impact Report. MINOR and MAJOR amendments — those adding, removing, or redefining principles — MUST satisfy all three criteria." This prevents throat-clearing on typo fixes while preserving the gate where it matters.

5. **Codify the verification deliberation requirement.** Lift from spec 066 §7 into Governance: "MINOR and MAJOR amendments MUST be validated by a verification deliberation (separate from the proposal deliberation) against the amended text. Zero disputes from the verification deliberation is the acceptance bar before merge." This is what the v2.3.1 PATCH actually demonstrated catches real bugs. The pattern is proven; codifying it costs nothing.

6. **Add a v2.4.0 sync impact report to the top of the document.** Match the format of the v2.3.0 → 2.3.1 report. Specifically: (a) new section: Governance / Constitutional Inclusion Criteria, (b) grandfathered: all principles I–XXVII, (c) templates requiring updates: amendment PR template (if it exists in `.specify/templates/`; if not, note that the spec template needs the self-assessment section added). This makes the constitution self-consistent on its own change-tracking discipline.

7. **Fix criterion 2's "without requiring interpretation" wording.** Replace with: "the principle's wording MUST define its own scope and terms explicitly. A reviewer applying the principle to a hypothetical PR MUST be able to determine *whether the principle applies* without consulting external definitions. Application within scope MAY require judgment; scope determination MUST NOT." This tracks what Principle XXIV does well (defines "safety-critical" inline) and prevents the criterion from rejecting principles that legitimately need scoped judgment in application.

8. **Add a precedent log at `deliberations/governance-decisions.md`.** Each future amendment that exercises the gate — pass or fail — adds an entry: principle name, criteria evaluation, decision, rationale, alternative routing if rejected. This converts the gate from "self-assessment in isolation" into "self-assessment against accumulated precedent." It also makes the gate auditable: if criterion 1 has been interpreted inconsistently across three amendments, the inconsistency becomes visible.

9. **Specify the expedited amendment path.** Add a paragraph: "Amendments responding to security disclosures, license-compliance issues, or regulatory changes MAY merge without the verification deliberation step. They MUST still satisfy the three inclusion criteria and MUST trigger a verification deliberation within 14 days of merge, with any findings landing as a follow-up amendment." This closes the incident-response gap without weakening the gate for normal amendments.

10. **Cross-link the gate from Principle XVII (Content Classification).** XVII is the existing principle that does the same job *within the codebase* (execution logic vs. contribution guidelines). The v2.4.0 gate does the same job *within the constitution itself*. Adding a one-line cross-reference in XVII ("See Governance / Constitutional Inclusion Criteria for the parallel rule applied to constitutional amendments") makes the symmetry visible and helps amendment authors discover the gate when they're reading XVII for guidance on their codebase changes.

---

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-self-consistency-2026-04-26/CONSTITUTION-v2.4.0-candidate.md` — primary target, lines 872–905 (the new gate), lines 862–871 (surrounding Governance section), lines 1–60 (Sync Impact Reports as precedent format)
- Principle XI (lines 298–342) — Single Source of Truth, the dogfooded basis for criterion 3
- Principle XVII (lines 480–508) — Content Classification, the precedent for routing rules
- Principle XXII (lines 627–654) — Distribution Surface Integrity, the precedent for "declare explicitly or it doesn't ship" enforcement
- Principle XXIV (lines 687–716) — Safety-Critical Defense-in-Depth, the model for three-layer enforcement (schema / parser / contract test) that the gate should adopt
- Principle XXVI (lines 763–789) — Meta-Testing for Parametrized Capabilities, the worked example for criterion 1's "concrete sketch" threshold
- Spec 066 §7 (referenced in Sync Impact Report line 47–48) — "Run a verification deliberation against this amended text to catch inter-principle conflicts; 0 disputes is the acceptance bar" — the codification target for recommendation #5
- Sync Impact Report v2.3.0 → 2.3.1 (lines 2–21) — the format precedent for recommendation #6
