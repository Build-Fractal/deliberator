# The Pragmatist: Final Disputes

**Agent**: The Pragmatist
**Date**: 2026-03-19
**Inputs**: Revised positions from all three agents (Mechanist, Pragmatist, Purist)

---

## Remaining Disputes

### Dispute 1: FR-023 grounding-reference check -- MUST vs. SHOULD

The Mechanist and the Purist disagree on the normative level of the grounding-reference check in FR-023. The Purist's revised FR-023 uses MUST for both heading validation and grounding-reference validation. The Mechanist's revised FR-023 uses MUST for heading validation but downgrades the grounding-reference check to SHOULD, on the grounds that it is a heuristic rather than a deterministic enforcement.

Both are wrong at their respective extremes.

The Purist's MUST is too strong. The check is string-presence: does the grounding document's filename appear in the Binding Decisions section? As the Mechanist correctly argued, string presence does not prove citation-as-authority. An arbiter could mention the filename in a parenthetical aside while grounding every ruling in a docs entry. MUST-level language implies the check is sufficient for compliance. It is not. It is a necessary-condition heuristic that catches gross omissions.

The Mechanist's SHOULD is too weak. A SHOULD-level check is one that implementors can skip with justification. But there is no justification for skipping a one-string-search check that catches the most egregious class of citation violation. The implementation cost is trivial. The signal value is high. SHOULD invites "we'll add it later" indefinitely, and the Mechanist's own position throughout these disputes has been that deferred work tends to stay deferred.

**My position**: MUST for performing the check, with an explicit scope qualifier that names what the check does and does not guarantee. The normative weight attaches to performing the check, not to treating its result as proof of compliance. The Pragmatist's revised FR-023 text already does this: "Both warnings are informational -- the file is still written." The check fires; the file ships; the warning surfaces the concern. That is the right behavior at the right normative level.

This dispute is narrow. The three agents agree on the check itself, the implementation mechanism, and the non-blocking outcome. The disagreement is one keyword in one sentence. But normative keywords in specs are load-bearing, and this one determines whether the check ships in every v1 implementation or only in implementations that feel like it.

---

### Dispute 2: Prose conventions -- template-author MAY vs. template-author SHOULD

The three revisions produced three different normative levels for prose conventions in the template:

- **Mechanist**: No spec language at all. Template authors are "free to use labeled sub-fields as instructional hints." This is a description of what is permitted, not a recommendation.
- **Pragmatist** (my revision): Template authors MAY use labeled sub-fields. Documented in Implementation Guidance.
- **Purist**: Template authors SHOULD use labeled sub-fields. Documented in the deferred schema section. Output that omits them is still compliant.

The Mechanist's position is the most internally consistent but produces the worst outcome. If the spec says nothing about prose conventions, template authors will independently invent their own labels. One template uses `**Ruling:**`, another uses `**Decision:**`, a third uses `**Outcome:**`. When v2 extraction arrives, the corpus contains three naming conventions instead of one. The Mechanist is correct that the engine cannot enforce label consistency. The Mechanist is incorrect that silence is therefore the right spec-level response. Specs shape human behavior, not just machine behavior. A recommendation in Implementation Guidance costs nothing and reduces naming entropy.

The Purist's SHOULD is the position I retreated from in my revision, and I retreated for the reasons the Mechanist identified: SHOULD-level language in the spec creates a pseudo-contract that downstream consumers treat as a real contract. I stand by that retreat.

**My position remains MAY** in Implementation Guidance. MAY communicates "here is a useful pattern" without creating an expectation that the pattern will be present. It is the correct normative level for a convention that the engine does not validate and that the spec does not require. The Purist's SHOULD is a half-step back toward the problem all three of us identified in the cross-review round.

---

### Dispute 3: Vacuous-output detection -- SC-014 vs. FR-022 amendment

The Purist's revision proposes extending FR-022's three-tier failure model with a fourth category: "arbiter completes but resolves zero disputes." My revision proposes SC-014 as a success criterion that makes vacuous output detectable via a validation warning. Both address the same gap. They disagree on the mechanism.

The Purist's approach modifies the failure model itself. This is architecturally cleaner -- the failure taxonomy is the right home for this concept -- but it changes FR-022, which is a unanimously agreed requirement. Reopening FR-022 to add a fourth tier risks re-litigating the three-tier model that all agents and all upstream reviewers converged on.

My approach adds an SC that describes the expected engine behavior when vacuous output occurs. This does not change FR-022. It adds a testable expectation: when the arbiter produces zero binding decisions, the engine emits a specific warning. The failure model remains three tiers; the SC describes how a specific edge case within tier 3 (complete, parseable, but substantively empty) should be surfaced.

**My position**: SC-014 is the correct vehicle. It is additive (no existing agreement reopened), testable (Given/When/Then with a specific warning string), and scoped to the problem the Purist identified. If the project later decides that vacuous output warrants its own failure tier, that is a v2 decision informed by v1 data on how often vacuous output actually occurs.

---

## Convergence

### Convergence 1: Blocker 1 -- Option B (content-negative) is settled

All three agents now select Option B as the primary trigger mechanism. The Purist conceded in revision, adopting content-negative primary with pattern-match fallback. The Mechanist held Option B throughout. I held Option B throughout. The Purist's revision adds a useful refinement: primary and fallback should be intentionally different predicates to provide independent detection paths. All three agents accept this. The cost-asymmetry argument (false positives are visible and recoverable; false negatives are invisible and catastrophic) carried the day and is now unanimous.

**Agreed spec text**: FR-011 defines a "dispute entry" as any line between the markers containing non-whitespace content that is not an HTML comment. Fallback uses the `**Dispute` bold-label pattern. Primary and fallback test different predicates.

---

### Convergence 2: Blocker 3 -- P1 priority, Given/When/Then format, expanded SC scope

All three agents agree that SCs are P1. All three agents now agree on Given/When/Then format (the Mechanist adopted it in revision; the Purist's format is equivalent). All three agents agree on six SCs covering FR-022 through FR-027, with SC-010 rewritten as a string-presence check rather than a sub-field parsing check. The Mechanist and I agree on splitting SC-010 into engine-checkable and human-verifiable tiers. The Purist's conditioned SC-012 ("when the grounding document contains numbered requirements") is a sensible refinement that all parties should accept.

**Agreed**: P1 priority, six or seven SCs (depending on SC-014 resolution), Given/When/Then structure, observable outputs (stderr or structured log), SC-010 as grounding-path string-presence check.

---

### Convergence 3: Blocker 4 -- Option C (all three surfaces) is settled

All three agents select Option C. The Mechanist held it. The Purist held it. I modified my weighting but retained Option C. The remaining calibration (MUST vs. SHOULD for FR-023 grounding check) is Dispute 1 above, but the architectural decision -- spec defines the rule, template enforces it at generation time, engine validates post-hoc -- is unanimous.

**Agreed spec changes**: (1) FR-015 amended to require the template to instruct the arbiter on citation boundaries. (2) Template authoring contract gains a citation-boundary invariant. (3) FR-023 amended to include grounding-path string-presence check in Binding Decisions (normative level per Dispute 1). (4) Semantic citation-source analysis deferred to v2.

---

### Convergence 4: Blocker 2 -- Headings-only v1 contract with deferred schema section

All three agents now agree that FR-018 section headings are the sole v1 output contract. I retreated from SHOULD-level prose conventions in my revision. The Mechanist held headings-only throughout. The Purist modified to accept headings-only as the contract while adding SHOULD-level prose conventions as non-contractual guidance. The deferred schema section is agreed by all three agents, including the six advisory fields. The disagreement on prose-convention normative level (Dispute 2) is narrow -- all agree the fields exist and are advisory; the question is whether the spec says anything about template-level naming patterns.

**Agreed**: FR-018 headings are the v1 contract. A standalone "Deferred: Structured Output" section exists with six advisory fields and a process-level note (not a machine-checkable activation condition). Template-level prose conventions are addressed at MAY or SHOULD level (Dispute 2).

---

### Convergence 5: Engine validation is heuristic, not deterministic, for citation checks

All three agents now agree that v1 engine validation of citation boundaries is a string-presence heuristic, not semantic parsing. The Mechanist conceded this explicitly ("I overstated the engine check's reliability when I called it 'deterministic enforcement'"). The Purist scoped FR-023 to string-presence. I acknowledged the check is a necessary-condition test, not sufficient-condition. This convergence dissolves the sharpest tension from the cross-review round: the Mechanist is no longer claiming engine validation is the only surface that matters, and I am no longer dismissing engine validation as a v2 concern. The check is cheap, useful, and honestly labeled. All three agents endorse it.

**Agreed**: The engine checks for the grounding document path string in the Binding Decisions section. This catches gross omissions. It does not catch subtle citation-authority violations. Full semantic validation is a v2 concern. The check's limitations are documented in the spec text, not hidden behind a MUST that implies sufficiency.

---

## Final Position Statement

Three rounds of adversarial review produced a result I did not expect: the most important concession I made was not to the Mechanist or the Purist, but to my own stated principles. I built my entire review around "favor the recoverable error" and then proposed a template-only citation enforcement that made citation violations unrecoverable because they were undetectable. The Mechanist and the Purist both caught this, independently, from different analytical frameworks. That is the value of the process.

The remaining disputes are narrow. Dispute 1 is one normative keyword in one sentence. Dispute 2 is the difference between saying nothing, saying MAY, and saying SHOULD about a non-contractual convention. Dispute 3 is whether a gap is filled by an SC or an FR amendment. None of these disputes block implementation. Any of the three positions on any of the three disputes produces a workable spec. The convergences are what matter: content-negative triggers, P1 success criteria with expanded scope, all-three-surfaces citation enforcement, and headings-only v1 contracts with an honest deferral.

The Pragmatist's test has not changed: if the resolution requires new architecture, it is not a calibration fix. Every remaining dispute and every convergence point resolves with text changes to existing spec sections. No new mechanisms. No new abstractions. No new phases. The spec is ready to ship once these text changes land. The three disputes can be resolved by the spec owner with a coin flip and less damage than another review cycle would cost.

Ship it.
