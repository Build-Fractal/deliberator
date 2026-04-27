# Phase 4 Disputes — wording-precision

**Reviewer**: wording-precision
**Phase**: 4 (final disputes before synthesis)
**Target**: `CONSTITUTION-v2.3.2-candidate.md`, Principle XVI + adjacent surfaces

---

### Remaining Disputes

**Dispute: Sequencing — promote-to-MUST vs gate-on-grep**

- **My claim**: The MUST conversion of L463-466 (Recommendation 1, modified — the `objective.yml`-anchored MUST set) should land in v2.3.2 directly. The artifact mechanism is named in spec 014 FR-012, FR-020, FR-021; the constitution can codify discipline against a documented artifact contract without making the audit a precondition. If the runtime does not yet enforce the discipline, that is a Principle XXIV contract-test obligation (which I and PEG both already routed through XXIV), not a reason to stall the MUST. (revision §"Recommendation 1: Promote pinning from description to obligation"; revision §"Recommendation 8: Cite a spec FR for the pinning behavior".)
- **Opposing position(s)**: PEG holds that Recommendation 1 must be **gated on a code grep**, with their Rec 1 reframed as "the gating step for the other recommendations rather than a parallel hedge" (PEG revision §"Rec 1 (P1): Hold, with refinement"; PEG revision §"Rec 2 (P1): Strengthened" — strong on artifact, but conditioned on the grep). PEG's framing is that a constitution asserting properties of partly-aspirational code is itself a precision failure.
- **Why I will not concede**: The constitution is meant to be normative, not descriptive. v2.3.0 itself codified Principles XXII-XXVII over partly-aspirational implementation surfaces (e.g., XXII point 3 on end-to-end install testing was authored over a known CI gap; XXIV explicitly cites future contract tests). Making v2.3.2 wait for a grep that v2.3.0 did not require for analogous text would be inconsistent governance. The XXIV cross-reference is the constitutional mechanism for "the rule exists, the test that enforces it is a follow-up" — using it here is exactly what XXIV was designed for.
- **Counter-argument**: PEG could fairly respond that "v2.3.0 set a bad precedent and v2.3.2 should not perpetuate it." That is a coherent position; my answer is that fixing the precedent is a separate amendment (an explicit "evidence-pending" SIR convention applied across **all** aspirational principles), not a one-off blocker on XVI.
- **Proposed resolution path**: Adopt the modified Recommendation 1 text in v2.3.2 **and** add to the v2.3.2 SIR (New Recommendation A) a one-line audit-status line: "Pinning discipline as written assumes spec 014 FR-012/SC-004 enforcement; if the contract test (Principle XXIV) does not yet exist, file as follow-up to spec 014." This satisfies my "land it now" position and PEG's "be honest about evidence status" position without making them mutually exclusive. If the synthesis arbiter prefers PEG's gating, my fallback is PEG's hedge wording — but I dispute that gating is the better default.

**Dispute: Where the VII↔XVI carve-out lives — XVI clarification (mine) vs back-reference parenthetical only (CPC's revised position)**

- **My claim**: The full VII-narrowing carve-out text MUST live in XVI's clarification block, with a single back-reference parenthetical inserted into VII line 163. (revision §"Recommendation 3: Resolve the VII ↔ XVI cross-run determinism tension explicitly".) CPC's Rec #1 (modified) agrees on this allocation — but I disagree with their *proposed wording* of the back-reference: "(narrowed by Principle XVI for LLM-resolved parameters; see XVI Clarification v2.3.2)" mentions the version-tagged clarification block, which is the kind of forward-pointing reference that ages badly (when v2.3.3 arrives, the parenthetical points at stale text).
- **Opposing position(s)**: CPC revision §"Rec #1 — Modified" prescribes the version-tagged back-reference. PEG did not engage this specific wording.
- **Why I will not concede**: My phrasing — "(narrowed by Principle XVI for LLM gap-filling output)" — is version-stable. CPC's phrasing is version-fragile. Constitutional cross-references should point at *principles*, not *amendments to principles*, because the latter rot. CPC's framing ("see XVI Clarification v2.3.2") would require updating VII line 163 every time XVI is amended; mine never needs touching.
- **Counter-argument**: CPC could argue the version tag is *more* auditable — a reader can tell exactly which clarification authored the carve-out. That is a real benefit, but the audit trail belongs in the SIR, not in the cross-reference itself.
- **Proposed resolution path**: Adopt my version-stable parenthetical for VII line 163 (`"(narrowed by Principle XVI for LLM gap-filling output)"`) and let the v2.3.2 SIR record the audit trail. If synthesis prefers CPC's version-tagged form, demand at minimum that the cross-reference be paired with a SIR-update obligation in the governance section so the rot is detected.

**Dispute: Rec 7 stage-2 disambiguation — keep CPC's NR-2 split or accept PEG's `GapFiller.fill()` boundary**

- **My claim**: My modified Recommendation 7 (revision §"Recommendation 7: Disambiguate the two LLM activities in stage 2") accepted PEG's reframing — name the `GapFiller.fill()` protocol boundary, treat internal substep count as implementation detail. CPC, however, reaffirmed their NR-2 in revision (CPC revision §"NR-2 — Bound stage-2 stochasticity to two named substeps. **[P2]**") which prescribes the exact two-substep prose I dropped: "(a) translating gap identifiers into natural-language questions, and (b) extracting parameter values from the user's natural-language answers."
- **Opposing position(s)**: CPC's NR-2 prescribes the two-substep split as P2 with concrete edit text. PEG explicitly weakened my original Rec 7 to P3 and converged on the protocol-boundary framing in PEG revision §"Rec 7 (P3): Stage 2 split"-equivalent disposition (PEG explicitly noted in their position summary they would "decline to push for that disambiguation").
- **Why I will not concede**: The two-substep split describes *the current implementation* (`InteractiveGapFiller`) and may not describe future implementations. A future `BatchGapFiller` could collapse question-generation and answer-extraction into a single tool-using model call. Constitutional text that names the substeps locks in the implementation; constitutional text that names the protocol boundary does not. PEG's grounding (the boundary is `GapFiller.fill()` returning, not "after substep b finishes") is correct, and CPC's NR-2 silently re-introduces the lock-in.
- **Counter-argument**: CPC could argue the two-substep prose is descriptive (explaining what *currently* happens), not normative (mandating the split). That is a fair reading of their proposed text — but the V phase-report line they tie it to (`{N} gap identifiers resolved ({K} from cache, {N-K} newly resolved across question generation and answer extraction)`) operationalizes the split into a runtime-emitted observability contract, which **is** normative.
- **Proposed resolution path**: Adopt my modified Rec 7 (`GapFiller.fill()` boundary, internal calls are implementation detail) for the principle prose. For CPC's V phase-report line, replace "across question generation and answer extraction" with the implementation-agnostic "across the resolved subcalls of `GapFiller.fill()`" — that preserves CPC's observability win without the implementation lock-in. If synthesis prefers CPC's substep-named prose, my fallback is to mark the names as "currently" or "in InteractiveGapFiller" so future implementations remain free.

---

### Convergence

**Converged: VII↔XVI carve-out belongs in XVI, not VII**

- **Shared position**: The carve-out (assembled objective is the determinism boundary, not LLM-resolved parameter values) lives textually inside XVI's v2.3.2 clarification block; VII receives only a back-reference parenthetical. Authoring full text in both principles violates Principle XI.
- **Agreeing agents**: wording-precision, cross-principle-coherence, pr-evidence-grounding (PEG endorsed the carve-out direction; CPC explicitly withdrew the "amend VII" half of their original Rec #1).
- **Strength**: Unanimous (all three agents).
- **Path to convergence**: I drove the XI-violation argument; CPC conceded by withdrawing half of Rec #1; PEG was always satisfied by either allocation as long as the carve-out was named. Stable convergence — no synthesis ambiguity.

**Converged: `objective.yml` is the load-bearing artifact anchor**

- **Shared position**: The pinning discipline anchors to the `objective.yml` artifact (spec 014 FR-012, FR-020/021), not to a runtime cache. The candidate's "cached values from the first resolution are reused" is mechanism-incorrect prose and must be replaced with artifact-mediated language.
- **Agreeing agents**: wording-precision (revision §"Recommendation 1, modified" + §"Recommendation 6, modified"), cross-principle-coherence (revision §"Rec #2 — Surviving with reframing" + §"Rec #4 — Withdrawn — partially supplanted"), pr-evidence-grounding (revision §"Rec 2 (P1): Strengthened" + §"New Rec 2 (P2)").
- **Strength**: Unanimous, with PEG as the originator of the artifact-vs-cache distinction.
- **Path to convergence**: PEG's grounding work disproved CPC's and my mechanism-agnostic framings. Both of us composed PEG's artifact anchor into our proposals. CPC withdrew their "cache as sanctioned persistence" Rec #4 entirely. This is the deliberation's highest-confidence shared finding.

**Converged: "mechanical" vs "deterministic" three-way drift requires harmonization**

- **Shared position**: Spec 014 FR-012 and `construction.py:8-14` use "deterministic"; the v2.3.2 candidate uses "mechanical" in stage 3 of XVI; future readers grepping the codebase will find no match. Either rename stage 3 to "Deterministic assembly" or add an explicit equivalence sentence.
- **Agreeing agents**: pr-evidence-grounding (revision §"Rec 3 (P1): Strengthened, with priority elevation acknowledged"), cross-principle-coherence (revision §"Rec #8 — Modified — promoted from P3 to P2"), wording-precision (revision §"New Recommendation B — P2").
- **Strength**: Unanimous, with PEG and CPC originally diverging on priority (P1 vs P3) and converging on P2 after my New Recommendation B independently surfaced the same drift.
- **Path to convergence**: PEG provided the three-way grounding; CPC promoted their original P3 to P2; I added the same drift independently. All three agree on the fix; the only residual is whether to rename (cleaner) or annotate equivalence (more honest about historical drift). I lean rename, CPC offered both options, PEG leans rename. Likely Unanimous on rename if synthesis pushes.

**Converged: v2.3.2 needs a Sync Impact Report**

- **Shared position**: The candidate's top-of-file SIR describes v2.3.1 only; the version footer says 2.3.2. A v2.3.2 SIR block must precede the v2.3.1 SIR, naming the XVI clarification, the VII narrowing, and the spec 068 origin.
- **Agreeing agents**: wording-precision (revision §"New Recommendation A: P1"), pr-evidence-grounding (revision §"New Rec 1 (P1)"). CPC did not surface this in either review (they did not engage SIR metadata), so this is bilateral, not unanimous — but with no opposing view.
- **Strength**: Bilateral with no objection from CPC.
- **Path to convergence**: I surfaced the gap during my Phase 1 Scope Creep Check; PEG's Tension #2 confirmed it as the natural place to record evidence-pending status. Stable convergence.

**Converged: `SourceProvenance.filled_by` is the auditable hook for pinning attribution**

- **Shared position**: Naming `SourceProvenance.filled_by` (`construction.py:262-279`) inside XVI's clarification ties the pinning discipline to a verifiable code surface and distinguishes the keyed persistence from the "ambient state" Principle VII line 167 prohibits.
- **Agreeing agents**: pr-evidence-grounding (revision §"Rec 6 (P2): Hold"), wording-precision (revision §"Recommendation 10: Modified"), cross-principle-coherence (revision §"Rec #4 — Withdrawn but folded into Rec #1's clarification edit" + §"Rec #6 — Surviving").
- **Strength**: Unanimous.
- **Path to convergence**: PEG identified the hook; I composed it into my agent-naming Rec 10; CPC layered their V observability cross-reference on top of it. Three independent angles, one shared anchor.

---

### Final Position Statement

**Non-Negotiables**

1. **VII↔XVI carve-out MUST live in XVI's clarification with version-stable back-reference in VII**. Authoring full carve-out text in both principles violates Principle XI ("information in two places that disagreed"). VII line 163 receives only `"(narrowed by Principle XVI for LLM gap-filling output)"` — version-stable, not version-tagged. Reference: revision §"Recommendation 3" + Dispute #2 above. This is non-negotiable because the alternative produces a self-falsifying constitution: an XI-violating fix to a VII-violating principle.

2. **The pinning MUST set must anchor to `objective.yml`, not to "the cache"**. Constitutional obligations cannot mandate a non-existent runtime cache when the actual mechanism is artifact-mediated via spec 014 FR-012/FR-020/FR-021. Reference: revision §"Recommendation 1, modified" + §"Recommendation 6, modified". Non-negotiable because PEG's grounding evidence is dispositive — the alternative is a constitutional rule that cannot be enforced because it describes an artifact that does not exist.

3. **A v2.3.2 Sync Impact Report MUST precede the v2.3.1 SIR**. The version footer says 2.3.2 but the metadata describes only v2.3.1. This is a one-edit precision failure independent of any disputed substance. Reference: revision §"New Recommendation A: P1". Non-negotiable because metadata-content drift is exactly the class of bug Principle XI exists to prohibit, and the fix is mechanical.

**Flexibility**

1. **Sequencing of Recommendation 1 — direct land vs evidence-pending hedge**. My preference is direct land with XXIV cross-reference handling the enforcement-test obligation (Dispute #1). My flexibility: if PEG's gating wins synthesis, the fallback is their explicit "evidence-pending" SIR line. What MUST be preserved: the MUST verbs and the `objective.yml` anchor. What is flexible: whether merge happens before or after a code grep verifies enforcement.

2. **Stage-3 vocabulary harmonization — rename vs annotate equivalence**. My preference is renaming "Mechanical assembly" → "Deterministic assembly" (revision §"New Recommendation B"). My flexibility: CPC's Option B (equivalence note) is acceptable if synthesis prefers preserving the v2.3.2 wording for audit-trail reasons. What MUST be preserved: explicit reconciliation of the three-way drift (code, spec 014, constitution). What is flexible: rename vs annotate.

3. **Stage-2 prose specificity — protocol boundary (mine) vs named substeps (CPC's NR-2)**. My preference is `GapFiller.fill()` boundary with internal calls treated as implementation detail (Dispute #3). My flexibility: CPC's two-substep prose is acceptable if the V phase-report line is reworded to "resolved subcalls of `GapFiller.fill()`" or if the substep names are explicitly scoped to "currently" / "in InteractiveGapFiller". What MUST be preserved: stochasticity attribution lives at a boundary the codebase actually has. What is flexible: how granular the prose gets above that boundary.
