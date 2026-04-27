# Governance-Skeptic Review — v2.4.0 Constitutional Inclusion Criteria

### Executive Summary

The proposed Governance amendment introduces a three-criterion gate
("Constitutional Inclusion Criteria") between the Versioning bullet and
the Compliance bullet. The intent is sound — the constitution has
visibly grown from XV principles to XXVII in roughly a year, several of
the newer entries (XXIV, XXV, XXVI) are themselves admissions that the
prior gate was loose, and a structural filter is the right corrective.
The gate's three criteria — mechanical verification capability,
falsifiable scope, and distinctness from existing principles — are each
defensible on their own merits and individually align with how the
existing constitution behaves in practice (Origin notes, Operational
test clauses, derivation requirements).

However, as drafted the gate has several governance soundness issues
that merit attention before the v2.4.0 cut. Most importantly: the gate
is a *procedural* requirement, but it is buried as a third bullet
inside Governance with no enforcement hook ("plans MUST pass this gate"
language is reserved for the Compliance bullet, which speaks to
implementation plans, not constitutional amendments). The gate is also
self-referentially weak — by its own falsifiability criterion, the
phrases "concrete enough that an engineer reading the principle can
sketch the check in one paragraph," "without requiring 'interpretation,'"
and "concerns not already addressable by composing existing principles"
each require the very interpretation the gate prohibits.

The grandfathering boundary is the most exploitable surface. The text
says "Existing principles I-XXVII are grandfathered" but does not
define what counts as an "extension" to a grandfathered principle
versus a "new principle." Principle IX already accreted a
behavior-over-shape extension in v2.3.0, and Principle XI accreted a
Registry-First extension; either of those would have failed the
distinctness criterion if proposed as standalone principles. The gate
does not explicitly govern extensions, and a future amendment could
route around the gate by appending to an existing principle's body.

### Alignment

- The three-criterion structure mirrors the constitution's existing
  preference for explicit, enumerated rules (cf. Principle XXII's three
  invariants, Principle XXIII's four guarantees, Principle XXIV's three
  layers). Tone and shape match Governance's neighbors.
- The "operational guidance" escape hatch is well-named and correctly
  identifies the four plausible homes (`CONTRIBUTING.md`, the relevant
  spec, `SKILL.md`, domain-specific reference). This matches Principle
  XVII's content classification model, so the gate inherits an existing
  vocabulary rather than inventing one.
- The mechanical verification criterion's relaxation ("does NOT have to
  exist at amendment time, but the path… MUST be concrete enough… in
  one paragraph") is calibrated correctly — strict "must already exist"
  would block legitimate principles whose tooling lags ratification.
- The prospective application clause ("applies prospectively — to
  amendments landing after v2.4.0") is the right default; retroactively
  applying the gate to I-XXVII would force a destabilizing audit during
  what is otherwise a clarification release.
- The instruction that grandfathered migration is "a separate,
  intentional act governed by the same amendment process" closes the
  obvious dodge of silently demoting principles to operational
  guidance. The "receiving document identified explicitly in the
  migration spec" language is auditable.
- MAY/MUST usage in the gate text is internally consistent — every
  obligation uses MUST, and the body avoids spurious SHOULD where MUST
  is meant. (See Missed Opportunities for the inconsistency *with the
  rest of Governance.*)

### Missed Opportunities

- **No keyword-level harmony with existing Governance bullets.** The
  Amendments bullet uses plain imperative ("Require documentation…"),
  Versioning uses none, Compliance uses MUST. The new gate uses MUST in
  several places. This is fine in isolation but jarring when Governance
  is read end-to-end. Consider rewriting the gate's leader sentence to
  match Amendments' bullet-noun style ("Require…") so the four
  Governance bullets parse uniformly.
- **No enforcement hook tying the gate to the amendment workflow.** The
  Amendments bullet says "Use `/speckit.constitution` to update," but
  the gate does not require `/speckit.constitution` (or a Constitution
  Check analogue) to evaluate the three criteria. As written, the gate
  is aspirational — there is no procedural step that *forces* an
  amendment author to address the criteria.
- **"Concrete enough… can sketch the check in one paragraph" is itself
  a vague test.** Whose paragraph? Which engineer? The gate's own
  falsifiability criterion (#2) prohibits this kind of construction.
  Either constrain it ("the amendment PR description MUST contain a
  one-paragraph sketch of the proposed check") or remove the
  qualifier and accept that #1 is asking for a check that *could*
  exist.
- **Criterion #3 ("distinct from existing principles") provides no
  decision procedure.** The gate offers two options (extend existing
  principle vs. reject) without addressing the harder cases:
  cross-cutting principles that legitimately span multiple existing
  ones, or principles whose distinctness is contested. Compare with
  Principle XX's clear precedence rule and Principle XXI's ordered
  list. The gate would benefit from a tie-breaker.
- **Silence on extensions.** Principles IX and XI both have
  v2.3.0 extensions inside their body. The gate does not say whether a
  future "Extension (vN.N.N): …" sub-section to an existing principle
  is subject to the gate or grandfathered. The natural reading is
  "extensions ride on the host principle's grandfather status," which
  is exactly the loophole.
- **No interaction with the Versioning bullet.** Versioning says MINOR
  is for "new principles or material expansions" and PATCH is for
  "clarifications." If the gate is enforced and rejects a proposed
  principle, the Versioning rule is unaffected — but the gate doesn't
  say how a borderline case (rejected as a principle, accepted as an
  extension) should be classified. Today this would be a judgment call.
- **No appeal/override mechanism.** Every other gate in the
  constitution (Phase 6 validation in V; preset gate in XVII; plan
  Constitution Check in Compliance) describes either soft-warning
  behavior or a path through. The new gate is binary with no
  documented override. A constitution that has 27 principles will see
  edge cases — a documented override (e.g., "rejection MAY be
  overridden by unanimous arbiter ruling, recorded in the Sync Impact
  Report") prevents the gate itself from becoming a chokepoint.
- **The gate is a meta-rule but not labeled as such.** The constitution
  separates Core Principles, Development Workflow, Known Antipatterns,
  and Governance. The gate is governance-of-governance. Consider
  promoting it to its own subsection within Governance ("### Inclusion
  Criteria") rather than burying it as a third bullet — Governance has
  three bullets today and will have four after this amendment, which
  visually obscures that one of them is structurally larger and more
  procedural than the others.
- **No Sync Impact Report contract.** Existing amendments (see lines
  1-60) include a structured Sync Impact Report with version delta,
  added/modified principles, removed sections, and rationale. The gate
  doesn't require future amendments to include a "Inclusion Criteria
  Self-Assessment" section in the Sync Impact Report. Without that, the
  gate's audit trail is invisible.

### Off-Base Assumptions

- The gate assumes "operational guidance" is a well-defined home, but
  the four candidate destinations have very different review/version
  models. `SKILL.md` is the executable runtime spec (Principle IV);
  pushing a principle there is *not* demoting it — it may be promoting
  it to enforcement. The gate's framing ("rules of thumb belong in
  operational guidance") undersells what `SKILL.md` actually is.
- The gate assumes "Restating an existing principle in different words
  is rejected by this gate," but the constitution itself contains
  cross-references that look like restatements (XV ↔ XXVII coordination
  is the most explicit example). Coordination is not duplication, and
  the gate's wording does not distinguish them.

### Actionable Recommendations

1. **[P1] Lift the gate to a subsection.**
   - *Current state*: The gate is a third bullet inside the Governance
     section, between Versioning and Compliance.
   - *Proposed change*: Promote to `### Constitutional Inclusion
     Criteria` as a sibling subsection under Governance. Keep the
     other three bullets intact.
   - *Rationale*: The gate is structurally larger and procedurally
     different from the surrounding bullets; making it a peer of
     Amendments/Versioning/Compliance is misleading about its weight.
   - *Risk if ignored*: Future readers skim past the gate as "just
     another bullet"; amendment authors fail to address the criteria
     because the gate visually does not present as a distinct step.

2. **[P1] Wire the gate into the amendment workflow explicitly.**
   - *Current state*: Amendments bullet says "Use `/speckit.constitution`
     to update"; the gate is silent on workflow integration.
   - *Proposed change*: Add to the Amendments bullet: "Amendments
     proposing a new principle MUST include an Inclusion Criteria
     Self-Assessment in the Sync Impact Report, addressing each of
     the three criteria with concrete evidence."
   - *Rationale*: A gate without an enforcement step is aspirational.
     The Sync Impact Report is the natural enforcement surface — it
     already exists, is required for amendments, and is auditable in
     git history.
   - *Risk if ignored*: The gate becomes ceremonial; amendment authors
     skip it because there is no procedural forcing function.

3. **[P1] Define extension semantics.**
   - *Current state*: "This gate applies prospectively — to amendments
     landing after v2.4.0. Existing principles I-XXVII are
     grandfathered."
   - *Proposed change*: Add a fourth paragraph: "Extensions to
     grandfathered principles (sub-sections introduced via 'Extension
     (vN.N.N):' or 'Clarification (vN.N.N):' headers) ARE subject to
     this gate. The host principle's grandfathered status does not
     transfer to additions made after v2.4.0."
   - *Rationale*: The single most exploitable surface in the current
     draft is appending to an existing principle to bypass the gate.
     Closing this explicitly removes the loophole.
   - *Risk if ignored*: Future amendments route new content through
     existing-principle bodies (as IX and XI already did in v2.3.0)
     and the gate never fires.

4. **[P2] Tighten falsifiability of criterion #1.**
   - *Current state*: "concrete enough that an engineer reading the
     principle can sketch the check in one paragraph."
   - *Proposed change*: "the amendment PR description MUST contain a
     one-paragraph sketch of the proposed check, identifying the
     check type (CI lint, parity test, structural assertion, schema
     validation, contract test, meta-test) and the specific artifact
     it would inspect."
   - *Rationale*: The current wording asks the reader to imagine
     whether a sketch is possible. Asking the author to actually
     sketch it is concrete, falsifiable, and verifiable in PR review.
   - *Risk if ignored*: Criterion #1 collapses into criterion #2 (both
     reduce to "specific enough to evaluate"); the gate is
     effectively two criteria.

5. **[P2] Add tie-breaker for criterion #3.**
   - *Current state*: "covers concerns not already addressable by
     composing existing principles."
   - *Proposed change*: "covers concerns not already addressable by
     composing existing principles. When distinctness is contested,
     the burden is on the amendment author to identify which existing
     principle(s) cover ≥80% of the proposed scope and explain why
     the residual ≥20% requires a new principle rather than an
     extension."
   - *Rationale*: "Compose existing principles" is itself contested
     (Principle XV ↔ XXVII pair shows that coordinated principles can
     be legitimately distinct). A burden-of-proof rule resolves
     ambiguity without requiring an arbiter.
   - *Risk if ignored*: Distinctness becomes the most-litigated
     criterion; coordination patterns get blocked.

6. **[P2] Document a documented override path.**
   - *Current state*: No override mechanism.
   - *Proposed change*: Add: "Rejection by any criterion MAY be
     overridden by an arbiter ruling in a deliberation where ≥3
     independent agents converged on the principle's necessity. The
     override MUST be recorded in the Sync Impact Report with a link
     to the deliberation transcript."
   - *Rationale*: Conversus's own deliberation pattern (used to
     produce v2.3.0) is the natural override mechanism; using it
     keeps the constitution self-consistent with how the project
     reasons.
   - *Risk if ignored*: Edge cases force the gate to either reject
     legitimate principles or be quietly bypassed, both of which
     erode trust in the gate.

7. **[P2] Harmonize MUST/SHOULD/MAY across Governance.**
   - *Current state*: Amendments bullet uses no modal verbs;
     Versioning uses none; Compliance uses MUST; the new gate uses
     MUST extensively.
   - *Proposed change*: Rewrite Amendments as "Amendments MUST
     document the change, rationale, impact on existing specs, and an
     Inclusion Criteria Self-Assessment if a new principle is
     proposed. Use `/speckit.constitution` to update." Rewrite
     Versioning leader as "Version bumps MUST follow: MAJOR for…"
   - *Rationale*: The constitution explicitly references RFC 2119-ish
     modal verbs throughout (Stable Interfaces, Plugin Isolation,
     etc.). Governance is currently the loosest section in this
     regard, and the new gate amplifies the inconsistency.
   - *Risk if ignored*: Inconsistent modal verbs in Governance dilute
     the contract; the gate's MUSTs become harder to enforce when
     surrounded by un-modal'd bullets.

8. **[P3] Clarify the relationship to Versioning classification.**
   - *Current state*: Versioning says "MINOR for new principles or
     material expansions, PATCH for clarifications." The gate creates
     a third state: "rejected as principle, accepted as extension."
   - *Proposed change*: Add a Versioning sub-bullet: "An amendment
     redirected from a new principle to an extension of an existing
     principle is MINOR ('material expansion'), not PATCH."
   - *Rationale*: Without this, an amendment author who fails the
     gate but is allowed to extend an existing principle could
     plausibly classify it as PATCH ("just clarification"), erasing
     the version-history signal that the constitution grew.
   - *Risk if ignored*: The gate becomes a way to route new content
     through the constitution at PATCH, hiding the principle-growth
     signal that motivated the gate in the first place.

9. **[P3] Disambiguate "operational guidance" from `SKILL.md`.**
   - *Current state*: "Principles that fail any criterion belong in
     **operational guidance**: `CONTRIBUTING.md`, the relevant spec,
     `SKILL.md` instructions, or domain-specific reference documents."
   - *Proposed change*: Either drop `SKILL.md` from the list (since
     Principle IV elevates it to executable truth, not "operational
     guidance"), or add a parenthetical: "(noting that `SKILL.md`
     content is *runtime-enforced*, not advisory — placing a rule
     there strengthens it relative to the constitution's
     descriptive prose)."
   - *Rationale*: The current phrasing implies all four destinations
     are equivalent in weight; they aren't. `SKILL.md` is the only
     destination where placement makes the rule mechanically
     enforced.
   - *Risk if ignored*: Amendment authors interpret "demote to
     operational guidance" as weakening, and route runtime-enforceable
     rules to `CONTRIBUTING.md` where they will not fire.

10. **[P3] Add a cross-reference to Principle XVII.**
    - *Current state*: The gate's "operational guidance vs.
      constitution" distinction overlaps significantly with Principle
      XVII (Content Classification), which already governs execution
      logic vs. contribution guidelines.
    - *Proposed change*: Add at the end of the operational guidance
      paragraph: "(Cf. Principle XVII for the broader classification
      between execution logic and contribution guidelines.)"
    - *Rationale*: Two sections describing similar classifications
      without cross-reference is exactly the duplication Principle XI
      forbids. A single cross-reference resolves it.
    - *Risk if ignored*: Future readers treat the gate's "operational
      guidance" and Principle XVII's "contribution guidelines" as
      independent vocabularies, drift accumulates, and one or both
      becomes stale.

### Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus-oss/deliberations/069-self-consistency-2026-04-26/CONSTITUTION-v2.4.0-candidate.md`
  - Sync Impact Reports (lines 1-60) — amendment audit-trail format
  - Principle IX (lines 196-275) — host of v2.3.0 behavior-over-shape extension
  - Principle XI (lines 298-342) — host of v2.3.0 Registry-First extension
  - Principle XV (lines 415-446) — Plugin Isolation, registry coordination
  - Principle XVII (lines 480-508) — Content Classification, overlaps gate
  - Principle XX (lines 568-595) — Decomposition Mechanism Precedence,
    a model for tie-breaker rules
  - Principle XXII-XXVII (lines 627-825) — recently-added principles
    that motivated the gate
  - Governance section (lines 861-907) — host of the amendment under
    review
