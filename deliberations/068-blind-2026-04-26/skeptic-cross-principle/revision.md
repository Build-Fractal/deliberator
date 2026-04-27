# skeptic-cross-principle: Revision (Phase 3, iteration 1)

This revision processes my Phase 1 dispositions in light of the two cross-reviews of my work (skeptic-mathematical, practitioner) and my own cross-reviews of theirs. Where their critiques landed, I update the recommendation; where I still disagree, I say so.

## Recommendation Dispositions

### Original Recommendation 1 — Merge XVI into VII as an extension

**Disposition: SOFTEN to "merge OR demote, after decomposition."**

skeptic-mathematical's "split first, then absorb" sequencing (their Dangerous Contradiction #1, Suggested Resolution) is correct. My merge-into-VII move and their split-into-XVI-A/XVI-B move are not opposites — they are sequential phases of the same refactor. And the practitioner's Dangerous Contradiction #1 is right that proposing both "merge" and "tighten in place" simultaneously is incoherent.

Updated wording: "Decompose XVI's content along three axes — (a) user-facing transparency, (b) within-run pinning discipline, (c) 3-stage pipeline description — and dispose of each fragment independently. (a) folds into IV. (b) becomes a VII extension or freestanding tight principle. (c) moves to spec 013. The 3-stage description does not survive in any constitutional form."

This preserves my structural concern (XVI has no clean home as currently bundled) while accepting that the merge cannot be performed before the split.

### Original Recommendation 2 — Narrow XVI to transparency-only as alternative

**Disposition: KEEP, demote to fallback.**

This was always offered as the alternative to Recommendation 1. With the decomposition framing above, this becomes the natural disposition for fragment (a): if IV cannot absorb the plain-language requirement (practitioner argues X is also a candidate, my cross-review noted IV is the better fit), then XVI shrinks to transparency-only as a freestanding principle. Either way, the determinism content leaves.

### Original Recommendation 3 — Add VII↔XVI back-reference

**Disposition: KEEP, strengthen.**

Both cross-reviews agree this is the highest-leverage edit (skeptic-mathematical Safe Agreement #4; practitioner Safe Agreement #2). My own cross-review of skeptic-mathematical reinforced this — VII's "non-negotiable" framing must explicitly acknowledge the LLM-mediated exception, otherwise dumping XVI's content into VII makes the contradiction worse, not better.

Strengthened wording: "VII MUST append: 'Principle XVI defines the sole sanctioned exception, scoped to LLM-mediated parameter resolution under within-run pinning discipline.' XVI MUST open with 'Subject to Principle VII, …' This cross-reference is mandatory regardless of which structural disposition (merge / decompose / shrink) is chosen."

### Original Recommendation 4 — Pick one term ("mechanical" vs "deterministic") in XVI

**Disposition: KEEP, sharpen.**

Both cross-reviews agreed (skeptic-mathematical Safe Agreement #3; practitioner Tension #2). The practitioner specifically endorsed my preference to align with VIII's existing "mechanical = antonym of LLM inference" convention. No retreat.

Final wording: "XVI stages 1 and 3 MUST use 'deterministic' (consistent with VII vocabulary). 'Mechanical' is reserved for VIII's antonym-of-inference sense. Stage 1 and stage 3 are deterministic; stage 2 is the bounded LLM-mediated exception."

### Original Recommendation 5 — Define "pinning" as a constitutional term

**Disposition: KEEP and EXTEND with skeptic-mathematical's test-contract.**

skeptic-mathematical's Dangerous Contradiction #3 is fair: a glossary entry alone creates the illusion of resolution while leaving "pinning" unenforceable. My cross-review pushed back on their cache-key-schema overreach (constitutionally inappropriate detail), but their underlying point — "terminology hardens, behavior remains soft" — is correct.

Compromise wording: "Define 'pinning' in II's stable-interface vocabulary as 'a parameter value committed to a run-scoped store, immutable for the duration of the run, with invalidation policy specified in spec 013.' XVI MUST reference a contract test in spec 013 that asserts no within-run drift. The cache key schema itself stays in spec 013, not constitutional prose."

This adopts the test-contract spine (their move) while preserving the constitution/spec abstraction boundary (my move).

### Original Recommendation 6 — XVI ↔ V interaction clause (pinned values must be emitted)

**Disposition: KEEP, strengthen.**

skeptic-mathematical Tension #3 explicitly conceded I caught a gap they missed; the practitioner did not address V at all in their review (which my cross-review of them flagged as an omission). Both cross-reviews of me reinforced rather than weakened this recommendation.

Strengthened wording: "Pinned parameter values MUST be emitted as deliberation output (under V's 'every phase MUST report progress' contract). Without observable pinned values, XVI's transparency claim is hollow regardless of how the principle is named or located."

### Original Recommendation 7 — XVI ↔ XXIV interaction clause

**Disposition: KEEP, narrow scope.**

skeptic-mathematical Tension #4 strengthened this rather than weakening it. My own cross-review of skeptic-mathematical, however, flagged that XXIV's pattern doesn't auto-generalize — XXIV scopes itself to synthesis verdict generation and provider protocols, and I noted that re-purposing XXIV's pattern wholesale violates XI.

Narrowed wording: "When optimization-driven outputs are consumed by synthesis-verdict generation (red-blue, arbitration), XXIV's three-layer defense MUST validate the pinned parameters as part of the synthesis path. Optimization that does NOT feed synthesis verdicts is out of XXIV's scope and remains under XVI/VII alone."

This keeps the safety-critical interaction explicit without letting XVI silently expand XXIV.

### Original Recommendation 8 — Soften solver-substitution claim

**Disposition: KEEP, no change.**

Both cross-reviews concurred. skeptic-mathematical Tension #2 explicitly conceded "the conservative reading should win." The practitioner's Dangerous Contradiction #3 acknowledged my softening preserves their "useful contract gate" reading while closing a real ambiguity. Unchanged final wording: "Changing solvers MUST NOT change the objective function or its parameter semantics."

### Original Recommendation 9 — Generalize XVI away from the 3-stage pipeline

**Disposition: KEEP, with practitioner's relocation refinement.**

The practitioner's Dangerous Contradiction #2 is fair: my "describe the property, not the mechanism" framing and their "physically relocate to spec 013" framing are not identical. I now think the practitioner's version is the right disposition — the 3-stage description should leave XVI entirely (relocated to spec 013), and XVI should not retain a property-form description of it. A property-form residue still produces review burden inside XVI and re-attracts the implementation detail on the next amendment cycle.

Updated wording: "The 3-stage pipeline description MUST be relocated from XVI to spec 013. XVI retains only the user-facing property ('users understand what is being optimized'). No property-form residue — once spec 013 owns the pipeline, XVI does not narrate it at any altitude."

### Original Recommendation 10 — Consider removing XVI entirely

**Disposition: WITHDRAW as standalone, FOLD into Recommendation 1.**

My own cross-review of skeptic-mathematical flagged that removal-without-VII-amendment creates dead infrastructure under XII — specs 012-019 would have dangling pointers. The practitioner's Safe Agreement framing also lists removal as a backstop both reviews accept only as a fallback. As a standalone recommendation it is dangerous (creates the orphan-pointer problem); as a sub-disposition under the decomposition framing in Recommendation 1, it is fine — fragment (b) might land in VII as an extension and fragment (a) might land in IV, which functionally removes XVI without leaving stranded references (specs get redirected to the new homes).

## New Recommendations

### New Recommendation 1 — Sequence the disposition: split → relocate → cross-reference → absorb

The cross-review interaction with skeptic-mathematical surfaced that my Phase 1 review and theirs propose mutually exclusive remedies (merge vs. split) only if read non-sequentially. Read sequentially, they are coherent. The constitution editor should execute the operations in this order:

1. **Split**: decompose XVI into three fragments (transparency / pinning / pipeline) so each can be evaluated independently.
2. **Relocate**: move the pipeline fragment to spec 013 (per Recommendation 9 updated).
3. **Cross-reference**: add VII↔XVI bidirectional reference (per Recommendation 3 strengthened); add V emission requirement (per Recommendation 6 strengthened); add narrowed XXIV interaction (per Recommendation 7 narrowed).
4. **Absorb**: fold the transparency fragment into IV; fold the pinning fragment into VII as a named extension OR keep it freestanding as "Within-Run Parameter Pinning" with a tighter name.

Doing these out of order produces the contradictions both cross-reviews flagged. Doing them in order yields a constitutionally coherent endpoint.

### New Recommendation 2 — Add a "spec author audience" disambiguation to the transparency fragment

The practitioner's review surfaced (and my cross-review of skeptic-mathematical conceded the parallel point) that XVI's transparency claim is unfalsifiable without an audience specifier. The plain-language gloss is for whom? End user, spec author, plugin author? The fragment that lands in IV (or stays in XVI as transparency-only) MUST name its audience.

Suggested wording: "Plain-language explanations target the end user reading deliberation output. Spec-author-facing precision is governed by IV's 'specification text IS the implementation' contract and lives in spec text, not in user-facing output."

This is a new recommendation because Phase 1 did not specifically call for an audience clause; my Phase 1 noted the assumption was unargued (Off-Base Assumption #3) but stopped short of demanding the disambiguation.

### New Recommendation 3 — Treat the "Mathematical Transparency" name as load-bearing, not cosmetic

Both cross-reviews independently flagged the name as too broad (skeptic-mathematical's principle-bundling diagnosis; practitioner's Safe Agreement #3). My Phase 1 review treated the structural problem but did not name the name itself as a remediation target.

Updated wording: "After decomposition, the residual XVI (if any) MUST be renamed to match its surviving content. If only the transparency fragment survives, the name 'Mathematical Transparency' is acceptable. If only the pinning fragment survives, rename to 'Within-Run Parameter Pinning' or fold into VII. The current name is a remediation target, not a cosmetic detail — its breadth is what enabled the bundling defect."

## Position Summary

My Phase 1 review identified XVI as a constitutional drift problem: a principle bundling three independent claims (transparency, pinning, pipeline) under a name too broad to constrain its scope, with a "Clarification" block that was patched in defensively after a prior conflict with VII surfaced. The two cross-reviews of my work largely agreed on the diagnosis. They differed on remediation: skeptic-mathematical wanted to split XVI into A/B fragments to make each fail cleanly; the practitioner wanted to collapse XVI to 4-6 operational lines or remove it entirely. After cross-review, I now read these not as opposites but as sequential phases — split first to disambiguate, then relocate the pipeline fragment to spec 013, then cross-reference VII/V/XXIV, then absorb fragments into existing principles where they fit. This sequenced approach preserves the strongest moves from all three reviews and avoids the contradictions any one of them produces in isolation.

The single highest-leverage edit, on which all three reviews independently converge, is the VII↔XVI bidirectional cross-reference. VII's current "deterministic orchestration is non-negotiable" framing and XVI's stochastic LLM-call admission cannot both stand without explicit mutual acknowledgement. Whichever structural disposition the synthesizer chooses (merge, decompose-and-redistribute, or shrink-to-transparency), this cross-reference must accompany it. Recommendation 10 from my Phase 1 (remove XVI entirely) is withdrawn as a standalone move because removal without VII amendment leaves specs 012-019 with dangling pointers, which is a textbook XII violation — but folded into the decomposition path, the same outcome (XVI has no surviving constitutional surface) becomes safe because the spec references can be redirected to the new homes.

The remaining adjustments are concessions to the cross-reviewers where their critiques landed: I now want the pinning concept enforced via a contract test reference in spec 013 (skeptic-mathematical's test-contract spine, applied without the cache-key-schema overreach); I want the pipeline description physically relocated rather than left in property-form (practitioner's relocation refinement); I want an explicit audience clause for the transparency claim (skeptic-mathematical's audience specification combined with practitioner's reviewer-clarity concern); and I want the principle name itself treated as a remediation target rather than left as cosmetic. Where I held my ground: the V (Observable Deliberation) emission requirement is non-negotiable because both cross-reviewers under-weighted it; the XXIV interaction must be narrowed to synthesis-verdict scope rather than expanded to all of XVI; and the cache contract belongs in spec 013, not constitutional prose, because the constitution legislates vocabulary and contracts, not implementation schemas.
