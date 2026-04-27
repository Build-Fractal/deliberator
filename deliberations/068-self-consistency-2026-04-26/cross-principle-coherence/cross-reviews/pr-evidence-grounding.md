# Cross-Review of pr-evidence-grounding's Review

**Reviewer**: cross-principle-coherence
**Target reviewer**: pr-evidence-grounding
**Subject**: pr-evidence-grounding's review of `CONSTITUTION-v2.3.2-candidate.md` Principle XVI

## Framing

pr-evidence-grounding and I converged on the same target principle (XVI lines 448-503, particularly the v2.3.2 clarification at 491-498) from complementary angles. Their review grounds the wording against actual code at `conversus/schemas/construction.py` and spec 014; mine grounds it against the surrounding constitutional text (Principles VII, VIII, X, XI, XXIV). Read together, their review answers "does the codebase do what XVI says?" and mine answers "does the rest of the constitution support what XVI says?" — both questions matter and the candidate amendment is fragile against either lens. This cross-review surfaces where their evidence-grounded findings sharpen, soften, or genuinely conflict with my coherence-based findings, so the orchestrator can synthesize without double-counting and without dropping a real contradiction.

## Dangerous Contradictions

**1. Their "no cache layer exists" finding undermines my Principle VII reconciliation framing.**
pr-evidence-grounding's Off-Base Assumptions section reports that no module in `conversus/schemas/construction.py`, `conversus/registry/`, or any optimizer module persists or caches LLM gap-filled values across deliberation runs — "the pinning is achieved by writing `objective.yml` to disk and re-reading it — artifact-based persistence, not a runtime cache." My review (Off-Base Assumptions, item 1) accepted XVI's "cached values from the first resolution are reused" wording at face value and built a Principle VII reconciliation around it ("the cache is sanctioned persistence, distinguishing it from the 'ambient state' VII prohibits"). If their grep is correct, then my recommendation P2 ("Reconcile XVI's caching discipline with Principle VII's 'no ambient state' prohibition") is partially aimed at a phantom — there is no runtime cache, only an artifact. The orchestrator should treat their finding as the senior one here: my coherence work on the cache/ambient-state interaction needs to be **re-pointed at `objective.yml` as the persistence boundary**, not a cache. This does not invalidate the coherence concern — `objective.yml` is also persisted state that conditions later behavior — but the framing changes substantially.

**2. Their "spec 014 FR-012 says 'Assembly is deterministic'" finding contradicts my acceptance of the "mechanical assembly" terminology.**
pr-evidence-grounding's Off-Base Assumptions item 2 reports that `conversus/schemas/construction.py:8-14` and spec 014 FR-012 both still call stage 3 "deterministic," not "mechanical." My review (Alignment, bullet 2) treated "mechanical assembly" as locally coherent with Principle VIII's "mechanical" vocabulary and only flagged the VIII↔XVI vocabulary harmonization as a P3 concern. Their evidence makes the issue more urgent: the constitution is now using a word for stage 3 that neither the code nor the originating spec uses. This is a **three-way drift** (code: "deterministic", spec 014: "deterministic", constitution v2.3.2: "mechanical"), not a two-way harmonization. If the orchestrator accepts the candidate as-is, future readers grepping `construction.py` for "mechanical" will find nothing and grepping spec 014 for "mechanical" will find nothing, and the constitutional vocabulary becomes orphaned at exactly the layer XVI is trying to anchor. My P3 should be promoted to at least P2.

**3. Their "objective.yml is the pinning artifact" finding repositions my Principle X recommendation.**
pr-evidence-grounding's Missed Opportunities item 1 ("No mention of `objective.yml` as the pinning artifact … `objective.yml` is written once, and subsequent runs load it instead of re-calling the LLM") and my Missed Opportunities item 4 ("Lines 463-467 do not say where the cache lives … XVI should at minimum note that pinned parameters land in a deterministic location in the output tree") are converging on the same constitutional gap from different sides — they identified the artifact name from spec 014, I identified the absence of any location anchor from Principle X. **Combined, this is a single P1 actionable**: XVI should reference `objective.yml` (their evidence) as the artifact that satisfies Principle X's "one obvious way to find the result" (my coherence). The orchestrator should merge our two findings rather than treat them as separate recommendations.

## Tensions

**1. Their "evidence-pending hedge" P1 vs my "scope VII's claim" P1 — same problem, different remedies.**
pr-evidence-grounding's Actionable Recommendation 1 asks for an "evidence-pending hedge" on lines 469-471 because the cached-reuse mechanism is not implemented as described. My Recommendation 1 asks Principle VII to be explicitly scoped to "the assembly stage … not to the first-run gap-filling stage." Both fix the cold-run determinism problem but at different layers: theirs adds a temporal hedge to XVI ("this is target state, not implemented"), mine adds a conditional carve-out to VII ("the unconditional claim has a stage exception"). These are not contradictory — both could be applied — but if only one is taken, theirs is likelier to be reversed when the code catches up, while mine is structural and survives implementation. The orchestrator should consider whether to recommend both or pick the more durable one.

**2. Their "no enforcement principle backing" observation parallels my Principle XXIV cross-reference recommendation but stops short.**
pr-evidence-grounding's Off-Base Assumptions item 4 ("'Pinned per deliberation run' boundary is not enforced anywhere. No test in `engine/tests/` asserts within-run pinning; no Pydantic validator flags re-resolution; no CI gate") describes the same enforcement vacuum my Recommendation 3 identifies (cross-reference XXIV for the contract-test obligation). They observed the absence; I named the constitutional home for the obligation. Combined, this is a stronger case than either alone: there's a vacuum in the code AND a constitutional principle (XXIV) that should be filled to address it.

**3. Their spec-014 cross-reference recommendation aligns with my XI cross-reference but at a different anchor point.**
pr-evidence-grounding's Recommendation 4 asks XVI to add "cross-references … to spec 014 FR-012/SC-004 and spec 016 (plugin system)." My Recommendation 2 asks XVI to add a Principle XI (Single Source of Truth) cross-reference. Both are about anchoring XVI's claims in something the reader can verify, but theirs anchors **outward to specs** (which describe the implementation contract) and mine anchors **inward to other principles** (which describe the constitutional discipline). The candidate currently does neither well. If the orchestrator wants a single tightening pass, both anchors should land in the same edit.

**4. Their "Repeating a deliberation" prose critique vs my Principle III silence observation.**
pr-evidence-grounding repeatedly flags that "cached values from the first resolution are reused" is wrong-as-described (Off-Base Assumptions item 1, Recommendation 2). My Missed Opportunities item 7 raises a downstream version of the same concern — Principle III (Backward-Compatible Extension) is silent on what happens when a deliberation is re-run *after the pipeline implementation changes*. Their finding is that the mechanism is misdescribed; mine is that even if it were correctly described, III doesn't tell us how to handle cross-version replay. These layer naturally — fix theirs first (describe the mechanism correctly), then mine becomes addressable (state the cross-version contract).

**5. Their "Provenance tracking provides the within-run discipline hook" alignment vs my Principle V observability gap.**
pr-evidence-grounding's Alignment bullet 5 cites `SourceProvenance.filled_by` (construction.py:262-279) as the natural CI hook for the pinning discipline. My Missed Opportunities item 5 calls for an explicit Principle V cross-reference so the gap-filling step emits an observability line ("parameters resolved: 7 pinned (3 from cache, 4 newly resolved)"). These are the same discipline at different layers — provenance tagging at the data-structure layer (theirs) and phase reporting at the runtime layer (mine). A combined recommendation would tie `SourceProvenance.filled_by` (their evidence) to a Principle V phase report (my coherence anchor).

## Safe Agreements

**1. Both reviews independently identify the v2.3.2 clarification block (lines 491-498) as the strongest part of the amendment.**
pr-evidence-grounding's Alignment bullet 6 calls "the clarification's testable invariant … well-formed." My Executive Summary calls it "the strongest part of the amendment from a cross-principle perspective." Two independent lenses converging on the same favorable judgment increases confidence that this block, at least, can survive into v2.3.2 without further work.

**2. Both reviews flag that "deliberation run" and the within-run-vs-cross-run boundary are underspecified.**
pr-evidence-grounding's Missed Opportunities item 3 says "'Per deliberation run' is undefined." My Off-Base Assumptions item 3 says "XVI assumes a finer distinction that VIII does not articulate." We are pointing at the same ambiguity from different sides — theirs says no artifact pins the boundary, mine says no principle pins the boundary. Convergence here is strong; the orchestrator should treat boundary-definition as a non-controversial P1.

**3. Both reviews accept the three-stage taxonomy itself as a structural improvement.**
pr-evidence-grounding ("Three-stage naming matches code … Stage 3 mechanical determinism is verifiable … Stage 1 symbolic parsing determinism is verifiable") and my Executive Summary ("structurally honest three-stage determinism taxonomy that broadly fits the constitution's existing reproducibility commitments") agree the *taxonomy* is sound; the disagreement is about whether the supporting wording around it is grounded. Neither review proposes scrapping the three-stage framing.

**4. Both reviews note spec 016 / plugin-system silence as a coherence gap.**
pr-evidence-grounding's Missed Opportunities item 4 ("Spec 016 plugin-system reference is missing"). My Missed Opportunities item 8 ("Principle II (Stable Interfaces) is not referenced even though pinned parameters are now effectively a contract surface") points at the same underlying concern: the constitutional document is silent on how XVI's pinned-parameter contract relates to the plugin/extension surface. Theirs anchors to spec 016; mine anchors to Principle II. Both gaps are real and a single edit could close both.

## Referenced Documentation

- `deliberations/068-self-consistency-2026-04-26/pr-evidence-grounding/review.md` — Executive Summary, Alignment, Missed Opportunities, Off-Base Assumptions, Actionable Recommendations
- `deliberations/068-self-consistency-2026-04-26/cross-principle-coherence/review.md` — Executive Summary, Alignment, Missed Opportunities, Off-Base Assumptions, Actionable Recommendations
- `CONSTITUTION-v2.3.2-candidate.md` — Principle XVI lines 448-503, Clarification 491-498, Principles VII (161-175), VIII (176-194), X (277-296), XI (298-322), XXIV (712-741)
- `conversus/schemas/construction.py` — per pr-evidence-grounding spot-check (no cache layer)
- `specs/done/014-guided-objective-construction/spec.md` — FR-012 ("Assembly is deterministic") per pr-evidence-grounding
