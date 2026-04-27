# Cross-Principle Coherence Review — Phase 3 Revision (Iteration 1)

**Reviewer**: cross-principle-coherence
**Target**: `CONSTITUTION-v2.3.2-candidate.md`, Principle XVI (lines 448-503), v2.3.2 clarification (lines 491-498)
**Inputs**: Phase 1 review + cross-reviews from wording-precision (WP) and pr-evidence-grounding (PEG)

---

## Recommendation Dispositions

### Rec #1 — Explicitly scope Principle VII's "structurally identical output" claim. **[Modified]**

Both cross-reviews confirm this is the largest defect. WP independently rated it P1 and prescribed the carve-out in XVI's clarification rather than amending VII (WP cross-review of CPC, Dangerous Contradiction #1). PEG concurred this is the highest-confidence shared finding (PEG cross-review of CPC, Safe Agreement #1). However, WP correctly flagged that authoring the exception in *both* VII and XVI would itself violate Principle XI ("two places that disagree"). I withdraw the "amend VII" half of the original recommendation.

**Modified form**: Place the carve-out in XVI's v2.3.2 clarification (where the amendment is already in flight). Add a single back-reference parenthetical in VII line 163-164: `"(narrowed by Principle XVI for LLM-resolved parameters; see XVI Clarification v2.3.2)"`. Concrete edit to clarification block: replace "Principle XVI claims" (line 491) with "Principle XVI requires within-run determinism for the assembled objective function and cross-run reproducibility once parameters are pinned. This carves an explicit exception to Principle VII line 163's unconditional 'structurally identical output': the assembled objective function is the determinism boundary, not the LLM-resolved parameter values that feed into it."

### Rec #2 — Add Principle XI cross-reference inside XVI's pinning discipline. **[Surviving, with reframing]**

PEG's grounding work (PEG cross-review of CPC, Dangerous Contradiction #1) materially reframes this: the actual persistence mechanism in `conversus/schemas/construction.py` is artifact-based via `objective.yml` (per spec 014 FR-012), not a runtime cache. My original framing — "pinned parameters become *the* authoritative source" — survives, but the artifact name should be `objective.yml`, not "the cache." The XI cross-reference still applies (a re-resolution mid-run would create the SSOT-violation failure mode XI exists to prohibit) but anchored to `objective.yml` as the single source.

**Concrete edit**: Append to the clarification block: "The pinned parameter set MUST be persisted to `objective.yml` in the run's output directory and treated as the single authoritative source for that run's assembled objective (Principle XI applies)."

### Rec #3 — Cross-reference Principle XXIV for the re-resolution prohibition. **[Surviving, with caveat]**

Both cross-reviews independently endorse routing the falsification clause's enforcement through XXIV (WP cross-review of CPC, Tension #3; PEG cross-review of CPC, Tension #2). PEG sharpens the picture: no within-run pinning test currently exists in `engine/tests/`, so the XXIV cross-reference would land on an empty enforcement layer (PEG cross-review, Tension #1). The cross-reference is still correct — it's how the obligation gets constitutional weight — but it must be paired with a follow-up to author the contract test, otherwise the rule is paper.

**Concrete edit**: Append to clarification block: "Enforcement: Principle XXIV applies — a contract test reproducing the re-resolution failure pattern is required (follow-up to spec 013 / spec 014 acceptance criteria)."

### Rec #4 — Reconcile XVI's caching discipline with VII's "no ambient state". **[Withdrawn — partially supplanted]**

PEG's evidence (no runtime cache exists; persistence is artifact-based via `objective.yml`) renders the original framing — "the cache is sanctioned persistence" — partially aimed at a phantom (PEG cross-review of CPC, Dangerous Contradiction #1). The VII line 167 concern survives, but the right framing is: **`objective.yml` is sanctioned, keyed, explicit persistence and is therefore not the "ambient state or hidden context" VII prohibits**. WP captured the same insight at the orchestrator-attribution layer (WP cross-review, Tension #4) — naming the run orchestrator as the pinning agent makes the persistence attributable.

**Replacement language** (folds into Rec #1's clarification edit): "The run orchestrator MUST persist resolved parameter values to `objective.yml` — a sanctioned form of explicit, keyed persistence distinguished from the ambient state Principle VII line 167 prohibits."

### Rec #5 — Anchor pinned-parameter contract in Principle II (Stable Interfaces). **[Modified]**

PEG's reframing applies: if the artifact is `objective.yml`, II's stable-interface surface already exists at the file's schema layer (PEG cross-review of CPC, Tension #4). The recommendation survives but lands more naturally — `objective.yml` schema is the II contract, and changes to its keying or shape are II amendments. Original recommendation overcomplicated this by treating "the cache" as a new contract surface.

**Concrete edit**: Add to clarification block: "The `objective.yml` schema (parameter names, keying, and structure) is a Principle II stable interface. Changes require coordinated update of all consumers."

### Rec #6 — Add observability obligation tied to Principle V. **[Surviving]**

Both cross-reviews endorse and strengthen this. WP coordinates the V phase-report line with their stage 2 disambiguation (WP cross-review, Tension #3): one joint sentence covers question generation and answer extraction. PEG ties V's runtime observability to the `SourceProvenance.filled_by` data-structure hook already present in `construction.py:262-279` (PEG cross-review of CPC, Tension #5) — phase reporting without `filled_by` underneath is performative; `filled_by` without surfacing is invisible.

**Concrete edit**: Append to clarification: "Stage 2 emits a Principle V phase report line: `{N} gap identifiers resolved ({K} from cache, {N-K} newly resolved across question generation and answer extraction).` The runtime line is backed by `SourceProvenance.filled_by` provenance tagging on the underlying parameter records."

### Rec #7 — Cross-reference VII at line 489 for solver substitution. **[Surviving, with tightening from Rec #10]**

WP's praise of "bit-for-bit" (WP review Alignment bullet 3) cited line 470, not line 489 — WP's cross-review of CPC concedes this scope qualifier (WP cross-review of CPC, Dangerous Contradiction #3). The "(Principle VII applies)" parenthetical at line 489 is still appropriate for the *what is being optimized* claim, separate from numerical-stability concerns about solver *output*. PEG's evidence that no `conversus/optimizer/`, `nashopt/`, or `ampl/` directory exists yet (PEG cross-review of CPC, Dangerous Contradiction #3) compounds the issue but does not block the cross-reference.

**Concrete edit**: Line 489 — append "(Principle VII applies to the objective-function contract; numerical stability of solver output is out of scope for this principle)."

### Rec #8 — Acknowledge "mechanical" vs "deterministic" terminology shift in VIII. **[Modified — promoted from P3 to P2]**

PEG's three-way drift finding upgrades this materially (PEG cross-review of CPC, Dangerous Contradiction #2): code (`construction.py:8-14`) uses "deterministic", spec 014 FR-012 uses "deterministic", constitution v2.3.2 uses "mechanical." Future readers grepping `construction.py` for "mechanical" will find nothing. WP did not surface this drift (WP cross-review of CPC, Tension #4 acknowledges the gap). Promoting to P2 is justified.

**Concrete edit (one of two options, recommend first)**:
- **Option A**: Add a one-line parenthetical to Principle VIII line 178: `"(In v2.3.2, Principle XVI uses 'mechanical' specifically for the post-pinning assembly stage — the term subsumes the determinism XVI describes.)"`
- **Option B**: In XVI's clarification, add: "Stage 3 'mechanical assembly' is equivalent to the 'deterministic assembly' label used in `conversus/schemas/construction.py:8-14` and spec 014 FR-012 — the v2.3.2 wording shift is constitutional vocabulary harmonization, not a mechanism change."

Option B is more honest because it acknowledges the drift exists in code; Option A is structurally cleaner.

### Rec #9 — Add cache location to Principle X's "one obvious way to find the result". **[Modified — merged with Rec #2]**

WP and PEG both convergently identified location-naming as a needed fix, but at different specificity levels (WP cross-review of CPC, Dangerous Contradiction #1; PEG identified `objective.yml` as the artifact name). The Rec #2 edit above already names `objective.yml` adjacent to the run output directory, which satisfies X. Standalone X cross-reference becomes redundant.

**Concrete edit**: Roll into Rec #2's `objective.yml` language. No separate clarification line needed.

### Rec #10 — Tighten solver-equivalence claim on lines 488-489. **[Surviving]**

WP cross-review of CPC concedes this point explicitly (Dangerous Contradiction #3) — WP's "bit-for-bit" praise was scoped to stage 3 mechanical assembly, not to solver substitution. PEG's evidence of an aspirational optimizer layer (PEG cross-review of CPC, Dangerous Contradiction #3) reinforces the case. The claim "Changing solvers MUST NOT change what is being optimized" is correct; "solvers MUST produce identical optimization output" would not be — and the current wording is read by a careless reader as the latter.

**Concrete edit**: Line 488-489: "Solver choice (nashopt, AMPL, future alternatives) is an implementation detail. The objective function — *what is being optimized* — is the contract between user intent and mathematical optimization. Changing solvers MUST NOT change the objective function (Principle VII applies). Numerical optimization output may vary across solvers within documented stability bounds; that variance is solver behavior, not a violation of this principle."

---

## New Recommendations

### NR-1 — Add cross-version replay scope statement. **[P3]**

Source: WP's "deliberation run" definition (WP review Rec #2) implicitly forecloses cross-version cache reuse (different invocation = different run). My original review's Missed Opportunity on Principle III raised the parallel concern. Combined fix surfaced in WP cross-review of CPC, Dangerous Contradiction #3.

**Concrete edit**: Append to clarification block: "Cross-version replay (re-running a deliberation after a `conversus` upgrade) is out of scope for this principle. If a future spec requires version-stable pinning, it must extend Principle III."

### NR-2 — Bound stage-2 stochasticity to two named substeps. **[P2]**

Source: WP review Rec #7 (split stage 2 into question-generation + answer-extraction); my original review treated stage 2 monolithically. WP's split is more defensible — the prose at lines 473-475 already names two distinct LLM activities. Folds cleanly into Rec #6's V phase-report line.

**Concrete edit**: Lines 462-464 — replace "stochastic at the LLM call, but the resulting parameter values are pinned per deliberation run" with "stochastic at the LLM call across two substeps — (a) translating gap identifiers into natural-language questions, and (b) extracting parameter values from the user's natural-language answers — both of which are pinned together per deliberation run."

---

## Position Summary

My original review's biggest error was treating XVI's pinning discipline as a textual property to be reconciled, when PEG's grounding evidence shows the discipline is partly artifact-based (`objective.yml`) and partly aspirational (no within-run pinning test, no cache layer in the codebase). This reframing forces three substantial modifications: Rec #2 anchors to `objective.yml` instead of "the cache"; Rec #4 is withdrawn because the "ambient state" reconciliation was solving a phantom problem; Rec #5's stable-interface anchor lands on `objective.yml`'s schema rather than a hypothetical contract surface. The reframing strengthens rather than weakens the cross-principle coherence argument — `objective.yml` is a more concrete anchor than a runtime cache and lets XVI satisfy Principles X (findability), XI (SSOT), and II (stable interfaces) at a single named artifact.

WP's complementary work on intra-principle normative grammar (verb upgrades, term definitions, agent attribution) closes gaps my review either missed or addressed obliquely. The largest single coordination point — where WP authors the VII↔XVI carve-out — drove me to withdraw the "amend VII" half of Rec #1, retaining only a back-reference parenthetical to avoid the Principle XI duplication failure WP correctly flagged. WP also exposed a terminology drift (mechanical vs deterministic) that PEG's grounding promoted from P3 cosmetic to P2 substantive.

The surviving recommendations layer cleanly: WP's MUST/verbs and term definitions land in the bullet body (lines 460-470); my cross-references and PEG's spec-FR anchors land in the clarification block (lines 491-498) as a consolidated parenthetical or sub-section to avoid paragraph bloat. Principle XVI's three-stage taxonomy and the v2.3.2 inversion ("pin and cache its output" rather than "make the LLM deterministic") survive intact across all three reviews — this is a stable foundation. The amendment is *not* fragile in its premise; it is fragile in its boundaries with VII, XI, II, V, X, and the codebase, and the boundaries are fixable by coordinated edits the three reviews collectively specify.
