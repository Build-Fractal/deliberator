# Spec 068 — Self-Consistency Synthesis

**Target**: `CONSTITUTION-v2.3.2-candidate.md`, Principle XVI (lines 448-503), v2.3.2 clarification (lines 491-498)
**Mode**: cooperative
**Agents**: wording-precision (WP), cross-principle-coherence (CPC), pr-evidence-grounding (PEG)
**Synthesizer**: neutral

---

## Process Summary

- **Agents**: 3 (wording-precision, cross-principle-coherence, pr-evidence-grounding)
- **Total artifacts read**: 13
  - 1 target candidate constitution
  - 3 Phase 1 reviews
  - 6 Phase 2 cross-reviews (each agent reviewed the other two)
  - 3 Phase 3 revisions
  - 3 Phase 4 disputes
- **Per-phase counts**:
  - Phase 1: 30 recommendations proposed (WP: 10, CPC: 10, PEG: 10)
  - Phase 2: 6 cross-review files; 5 dangerous contradictions surfaced across the three pairings; numerous tensions and safe agreements
  - Phase 3: 30 dispositions on original recommendations + 5 new recommendations introduced (WP: New A + New B; CPC: NR-1 + NR-2; PEG: New 1 + New 2)
  - Phase 4: 3 disputes per agent (9 dispute statements; 3-5 of these address the same underlying decision points)
- **Recommendation accounting** (across all three agents combined):
  - **Proposed (Phase 1)**: 30
  - **Withdrawn (Phase 3)**: 1 (CPC Rec #4 — "ambient state" reconciliation, withdrawn because PEG's grounding showed the cache was a phantom)
  - **Modified (Phase 3)**: 23 — most modifications are compositions, not retreats (e.g., adding PEG's `objective.yml` artifact anchor onto WP's MUST framing)
  - **Surviving unchanged (Phase 3)**: 6 (WP Rec 4, WP Rec 9; CPC Rec #6, CPC Rec #7, CPC Rec #10; PEG Rec 8 + 10)
  - **New recommendations added (Phase 3)**: 5
- **Disputes remaining (after Phase 4)**: 3 substantive ones (see Remaining Disputes section)
- **Convergence points**: 5 explicitly named convergences (WP, CPC, PEG all aligned), several at unanimous strength

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|---|---|---|---|---|---|---|
| 1 | WP | Promote pinning from description to obligation (MUST) | P1 | Modified — anchored to `objective.yml` per PEG | PEG (mechanism, not just verb) | Unanimous on artifact anchor | Accepted-Modified |
| 2 | WP | Define "deliberation run" | P1 | Modified — tied to `objective.yml` lifetime | CPC (cross-version foreclosure) | Unanimous (Conv. 5) | Accepted-Modified |
| 3 | WP | Resolve VII ↔ XVI cross-run determinism tension | P1 | Modified — carve-out lives in XVI only | CPC (where to author) | Unanimous (Conv. 1) | Accepted-Modified |
| 4 | WP | Convert "claims" to normative verbs ("requires") | P2 | Surviving | none | All endorse | Accepted |
| 5 | WP | Bound "cross-run variance is acceptable" | P2 | Modified — three nested clauses | CPC (nesting), PEG (failure mode) | All endorse merged form | Accepted-Modified |
| 6 | WP | Specify pinning storage and lifetime | P2 → P1 | Modified — `objective.yml` + Principle X placement | CPC (deterministic location), PEG (artifact name) | Unanimous | Accepted-Modified |
| 7 | WP | Disambiguate two LLM activities in stage 2 | P2 → P3 | Modified — name `GapFiller.fill()` boundary | PEG (protocol level), CPC (kept substep split as NR-2) | Disputed | **Disputed** |
| 8 | WP | Cite spec FR for pinning behavior | P2 | Modified — corrected from spec 013 to spec 014 FR-012/SC-004 | PEG (correct anchor) | Unanimous | Accepted-Modified |
| 9 | WP | Define "fully-pinned parameter set" | P3 | Surviving | none | No objection | Accepted |
| 10 | WP | Name agent that pins parameters | P3 | Modified — adds `SourceProvenance.filled_by` | PEG (audit hook), CPC (VII boundary) | Unanimous (Conv. 4) | Accepted-Modified |
| New A | WP | Add v2.3.2 Sync Impact Report | P1 | New | none | Bilateral (WP+PEG; CPC silent) | Accepted |
| New B | WP | Reconcile mechanical/deterministic vocabulary | P2 | New | (CPC originally P3, promoted to P2) | Unanimous (Conv. 3) | Accepted |
| 1 | CPC | Explicitly scope VII's "structurally identical output" | P1 | Modified — withdrew "amend VII" half | WP (XI duplication risk) | Unanimous (Conv. 1) | Accepted-Modified |
| 2 | CPC | Add Principle XI cross-reference | P1 | Surviving with reframing — anchored to `objective.yml` | PEG (mechanism) | All endorse | Accepted-Modified |
| 3 | CPC | Cross-reference Principle XXIV for re-resolution prohibition | P1 | Surviving with caveat — paired with follow-up test obligation | PEG (no test exists yet), WP (verb upgrade complement) | All endorse | Accepted-Modified |
| 4 | CPC | Reconcile cache with VII "no ambient state" | P2 | **Withdrawn** — phantom cache; replaced with `objective.yml` framing | PEG (no cache exists) | Unanimous on withdrawal | Rejected (superseded) |
| 5 | CPC | Anchor pinned-parameter contract in Principle II | P2 | Modified — anchored to `objective.yml` schema | PEG (artifact already exists) | CPC holds as non-negotiable in disputes | **Disputed** |
| 6 | CPC | Add observability obligation tied to Principle V | P2 | Surviving — folded with `SourceProvenance.filled_by` | PEG (data-structure hook), WP (joint phrasing with Rec 7) | Unanimous (Conv. 4) | Accepted |
| 7 | CPC | Cross-reference VII at line 489 for solver substitution | P2 | Surviving with tightening from Rec #10 | WP (scope qualifier on bit-for-bit) | All endorse | Accepted-Modified |
| 8 | CPC | Acknowledge "mechanical" vs "deterministic" terminology shift in VIII | P3 → P2 | Modified — promoted from P3 to P2 | PEG (three-way drift), WP (independent New B) | Unanimous on drift; CPC disputes placement | **Disputed (placement)** |
| 9 | CPC | Add cache location to Principle X | P3 | Modified — merged into Rec #2 | WP, PEG | Folded into Conv. 2 | Accepted-Modified |
| 10 | CPC | Tighten solver-equivalence claim | P3 | Surviving | WP concedes scope qualifier, PEG concurs | All endorse | Accepted |
| NR-1 | CPC | Add cross-version replay scope statement | P3 | New | none | Folded into Conv. 5 | Accepted |
| NR-2 | CPC | Bound stage-2 stochasticity to two named substeps | P2 | New | WP (implementation lock-in concern) | Disputed | **Disputed** |
| 1 | PEG | "Evidence-pending" hedge OR perform §7 Q1 grep audit | P1 | Modified — refined as gating step | WP (sequencing) | Disputed in Phase 4 | **Disputed** |
| 2 | PEG | Replace "cached values" with `objective.yml` mechanism | P1 | Strengthened | none | Unanimous (Conv. 1 / NN-1) | Accepted |
| 3 | PEG | Reconcile "mechanical" vs "deterministic" terminology | P1 | Strengthened, P1 (CPC and WP at P2) | priority differs | Unanimous on fix | Accepted-Modified |
| 4 | PEG | Cross-reference spec 014 FR-012/SC-004 and spec 016 | P2 | Hold | none | All endorse | Accepted |
| 5 | PEG | Define "deliberation run" via concrete artifact | P2 | Strengthened | none | Unanimous (Conv. 5) | Accepted |
| 6 | PEG | Reference `SourceProvenance.filled_by` as auditable hook | P2 | Hold, merged with V/XXIV | none | Unanimous (Conv. 4) | Accepted |
| 7 | PEG | Acknowledge optimization-layer specs (016-019) under construction | P2 | Hold | (CPC and WP silent) | PEG holds in disputes | **Disputed (silence not consent)** |
| 8 | PEG | Add regression test for SC-004 | P3 | Hold (out-of-band) | none | No objection | Accepted (out-of-band) |
| 9 | PEG | Clarify XVI ↔ VII relationship | P3 | Refined — combined with WP Rec 5 | none | Folded into Conv. 1 | Accepted-Modified |
| 10 | PEG | Follow-up spec for CI lint detecting re-entrant `GapFiller.fill()` | P3 | Hold | none | All endorse | Accepted (out-of-band) |
| New 1 | PEG | Add v2.3.2 Sync Impact Report | P1 | New (concur with WP New A) | none | Bilateral, no objection | Accepted |
| New 2 | PEG | Combine `objective.yml`, Principle X, Principle XI into one anchor sentence | P2 | New | CPC (wants Principle II separate sub-bullet) | Mostly accepted, minor placement dispute | Accepted-Modified |

---

## Dangerous Contradictions Found

### Resolved Contradictions

1. **Pinning mechanism: runtime cache vs. on-disk artifact.**
   - What: Candidate text says "cached values from the first resolution are reused" but PEG's grep showed no runtime cache exists in `conversus/schemas/construction.py`; the actual mechanism is artifact-mediated via `objective.yml` (spec 014 FR-012).
   - Surfaced by: PEG Phase 1 Off-Base #1; WP cross-review of PEG Dangerous Contradiction #1; CPC cross-review of PEG Dangerous Contradiction #1.
   - Who conceded: CPC explicitly withdrew Rec #4 ("ambient state" reconciliation) and reframed Rec #2 to anchor to `objective.yml`. WP modified Rec 1 from generic MUST to `objective.yml`-anchored MUST.
   - Resolution: Replace candidate L463-466 prose with PEG's combined edit text: "Resolved parameter values **MUST** be persisted to `objective.yml` (spec 014 FR-012) for the duration of the deliberation run; the LLM **MUST NOT** be re-invoked for parameter resolution within the same run; values **MUST** be re-loaded from `objective.yml` rather than re-resolved." (See WP disputes Convergence 2; CPC disputes Convergence 2; PEG disputes Convergence 1 / NN-1.)

2. **Where the VII↔XVI carve-out lives.**
   - What: WP wanted the carve-out authored in XVI's clarification; CPC originally wanted it authored into VII; both authoring it produces a Principle XI violation ("same fact in two places").
   - Surfaced by: WP cross-review of CPC, Dangerous Contradiction #1.
   - Who conceded: CPC explicitly withdrew the "amend VII" half of Rec #1 in revision; PEG was always satisfied by either allocation as long as the carve-out is named.
   - Resolution: Carve-out lives once in XVI's v2.3.2 clarification block; VII line 163 receives only a back-reference parenthetical. (See Convergence 1.)

3. **Pinning storage location: "output directory" (WP) vs. deterministic-tree placement (CPC) vs. `objective.yml` (PEG).**
   - What: Three different specificities for where pinning persists.
   - Surfaced by: CPC cross-review of WP Dangerous Contradiction #1; PEG cross-review of WP Dangerous Contradiction #2.
   - Who conceded: WP modified Rec 6 to adopt PEG's `objective.yml` artifact anchor with CPC's deterministic-placement constraint and X-aware language.
   - Resolution: Single sentence — "Pinned parameter values **MUST** be persisted to `objective.yml` (spec 014 FR-012) at a deterministic path inside the run's output directory (per Principle X), or to its successor parameter artifact, and **MUST** be reused for the lifetime of that directory." (See WP revision Rec 6.)

4. **Solver-equivalence "bit-for-bit" claim scope.**
   - What: WP praised "bit-for-bit" precision (line 470) without distinguishing the assembled-objective claim from the solver-equivalence claim (line 489); CPC pushed back on solver-equivalence as a strong claim depending on numerical stability.
   - Surfaced by: WP cross-review of CPC, Dangerous Contradiction #3.
   - Who conceded: WP scoped its "bit-for-bit" praise explicitly to stage 3 mechanical assembly only; CPC's Rec #10 stands and Rec #7's wording was tightened.
   - Resolution: Lines 488-489 receive a tightened claim distinguishing "what is being optimized" (deterministic per VII) from solver numerical output (out-of-scope variance).

5. **Three-way "mechanical" vs. "deterministic" terminology drift.**
   - What: Code (`construction.py:8-14`) and spec 014 FR-012 use "deterministic"; constitution v2.3.2 uses "mechanical" in stage 3.
   - Surfaced by: PEG Off-Base #2; CPC cross-review of PEG Dangerous Contradiction #2; WP New Recommendation B independently.
   - Who conceded: CPC promoted Rec #8 from P3 to P2; WP did not catch in Phase 1 but added independent New B in revision; PEG holds at P1.
   - Resolution: Reconciliation required (rename stage 3 OR add equivalence note). Final priority: P2. **Placement of fix (XVI rename vs. VIII parenthetical) remains disputed** — see Remaining Disputes.

### Unresolved Contradictions (carried into Phase 4)

These are tracked in **Remaining Disputes** below.

---

## Systemic Contradictions

These are 3 patterns across multiple individual contradictions:

1. **Pattern: descriptive prose where normative verbs are needed.**
   - Manifests in: Pinning rule (L463-466), pinning storage location, pinning agent attribution, "claims" verb at L491.
   - Root cause: The candidate's amendment was authored in indicative mood — describing what happens — rather than imperative mood — mandating what must happen. Constitutions are normative; the candidate slipped into status-report tone in the load-bearing paragraph.
   - Implication: Unless every descriptive sentence is converted to MUST / MUST NOT / SHOULD, future PRs have no rule to violate, only descriptions to disagree with.

2. **Pattern: principle text claims runtime properties the codebase has not yet implemented.**
   - Manifests in: "Cached values are reused" (no cache exists); solver substitution claims (no `optimizer/`/`nashopt/`/`ampl/` directories); within-run pinning enforcement (no contract test in `engine/tests/`).
   - Root cause: The candidate amendment was written against the target architecture (specs 016-019) rather than against the current codebase. v2.3.0 set the precedent of codifying discipline over partly-aspirational surfaces (XXII point 3, XXIV future tests); v2.3.2 inherits that posture without explicitly acknowledging it.
   - Implication: Without an "evidence-pending" SIR convention or an audit gate, the constitution accumulates indicative-mood claims about runtime that may or may not exist. PEG holds this is unacceptable; WP holds XXIV's contract-test obligation handles it.

3. **Pattern: cross-principle dependencies left implicit.**
   - Manifests in: VII narrowing without VII being amended; XI not cross-referenced from XVI; II not anchored on `objective.yml` schema; V observability not tied to gap-filling; XXIV enforcement layer not declared; X "one obvious way" not anchored.
   - Root cause: XVI was edited in isolation; the constitution's network of cross-references was not updated to acknowledge the narrowing. CPC's review framed this as the dominant defect; WP's verb upgrades address the local symptoms; both are needed.
   - Implication: Any one fix in isolation leaves a different reviewer's concern untouched. The fixes layer rather than substitute — WP's MUSTs land in the body, CPC's cross-references land in the clarification, PEG's artifact anchors thread through both.

4. **Pattern: vocabulary drift between code, spec, and constitution.**
   - Manifests in: "mechanical" vs "deterministic" stage 3 label; "cache" vs `objective.yml`; "deliberation run" vs `objective.yml` lifetime; "the cache" vs `SourceProvenance.filled_by`.
   - Root cause: The amendment imported new terms ("mechanical assembly," "pinned per deliberation run," "cached values") without auditing against the codebase or the originating spec. Spec 014 already uses "deterministic" and `objective.yml`; the constitution invented parallel vocabulary.
   - Implication: Future readers grepping the codebase for constitutional terms will find nothing. Vocabulary harmonization is a one-edit fix per term but requires explicit convergence on which surface owns the canonical name.

---

## Convergence Achieved

Ordered by strength.

1. **[Unanimous] Pinning is artifact-mediated via `objective.yml`, not via a runtime cache.**
   - Position label: "the candidate's `cache` language describes a phantom; the artifact is the mechanism"
   - Agreed recommendation: Replace L463-466 with: "Resolved parameter values **MUST** be persisted to `objective.yml` (spec 014 FR-012) for the duration of the deliberation run; the LLM **MUST NOT** be re-invoked for parameter resolution within the same run; values **MUST** be re-loaded from `objective.yml` rather than re-resolved."
   - Supporting agents: WP (Rec 1 modified, Rec 6 modified), CPC (Rec #2 reframed, Rec #4 withdrawn), PEG (Rec 2 strengthened, Convergence 1 / NN-1 in disputes)
   - Evidence basis: PEG's grep of `conversus/schemas/construction.py:139-171` and spec 014 FR-012/FR-020/FR-021
   - Earned (during this deliberation; PEG sourced the evidence, WP and CPC retroactively repaired their framings)

2. **[Unanimous] The VII ↔ XVI carve-out lives once in XVI's clarification, with a back-reference parenthetical in VII.**
   - Position label: "single home for the exception; VII gets a pointer, not a copy"
   - Agreed recommendation: Add carve-out to v2.3.2 clarification: "Principle XVI **requires** within-run determinism for the assembled objective function and cross-run reproducibility once parameters are pinned. This carves an explicit exception to Principle VII line 163's unconditional 'structurally identical output': the assembled objective function is the determinism boundary, not the LLM-resolved parameter values that feed into it." Then add to VII line 163: "(narrowed by Principle XVI for LLM gap-filling output)" — version-stable form.
   - Supporting agents: WP (Rec 3 modified), CPC (Rec #1 withdrew amend-VII half), PEG (Rec 9 refined)
   - Evidence basis: WP's identification of the XI-violation if both home the exception; CPC's concession to withdraw the VII amendment half
   - Earned

3. **[Unanimous] `SourceProvenance.filled_by` is the auditable hook; pinning is keyed, explicit persistence (not VII-ambient state).**
   - Position label: "name the existing data-structure hook; the persistence is sanctioned"
   - Agreed recommendation: Add to clarification: "The run orchestrator **MUST** persist resolved parameter values to `objective.yml`; pinning is auditable via `SourceProvenance.filled_by` (`construction.py:262-279`) — a sanctioned form of explicit, keyed persistence distinguished from the ambient state Principle VII line 167 prohibits."
   - Supporting agents: PEG (Rec 6, hook sourced), WP (Rec 10 modified), CPC (Rec #4 withdrawn-and-replaced + Rec #6)
   - Evidence basis: PEG's grounding at construction.py:262-279
   - Earned

4. **[Unanimous] "Deliberation run" is artifact-scoped, defined by `objective.yml` lifetime.**
   - Position label: "anchor abstract terms to concrete artifacts"
   - Agreed recommendation: Add to clarification: "*deliberation run*: the lifetime of one `objective.yml` artifact; retries that reuse the same artifact are part of the same run, separate `/conversus run` invocations producing new artifacts are different runs. Cross-version replay is out of scope of this principle."
   - Supporting agents: WP (Rec 2 modified), CPC (NR-1), PEG (Rec 5 strengthened)
   - Evidence basis: PEG's artifact identification + CPC's foreclosure-risk argument + WP's definition phrasing
   - Earned

5. **[Unanimous] Mechanical/deterministic vocabulary drift requires reconciliation at P2.**
   - Position label: "three-way drift between code, spec 014, and constitution v2.3.2"
   - Agreed recommendation: Either (a) rename "Mechanical assembly" to "Deterministic assembly" in XVI stage 3 to match `construction.py:8-14` and spec 014 FR-012, OR (b) add an equivalence note in XVI's clarification, OR (c) add a parenthetical to VIII line 178 (CPC's preference). Priority P2 (originally PEG P1, CPC P3, settled at P2).
   - Supporting agents: PEG (Rec 3 sourced), CPC (Rec #8 promoted from P3 to P2), WP (New Recommendation B independently)
   - Evidence basis: PEG's three-way grounding (code, spec 014, constitution)
   - Earned (placement of fix remains disputed — see Remaining Disputes)

6. **[Bilateral, no objection] v2.3.2 needs a Sync Impact Report.**
   - Position label: "metadata describes v2.3.1 only; version footer says 2.3.2 — fix the audit trail"
   - Agreed recommendation: Prepend a v2.3.2 SIR block above the v2.3.1 SIR documenting the XVI clarification, the VII narrowing, the spec 068 origin, and the verification status of the pinning discipline.
   - Supporting agents: WP (New Recommendation A, P1), PEG (New Rec 1, P1), CPC (silent in original review, did not contest in revision/disputes)
   - Evidence basis: WP's Phase 1 Scope Creep Check observation
   - Earned

7. **[Unanimous] The falsification clause (L496-498) is the candidate's strongest sentence and should not be touched.**
   - Position label: "preserve what works"
   - Agreed recommendation: When tightening surrounding text, do not edit L496-498. The clause "A future PR that re-resolves parameters mid-deliberation, or that lets parameter values drift during a single optimization run, violates this principle" is enforceable and unusually concrete.
   - Supporting agents: WP (Alignment bullet 1), CPC (Executive Summary, "the strongest part of the amendment"), PEG (Alignment bullet 6)
   - Evidence basis: independent praise from all three reviewers in Phase 1
   - Pre-existing (the candidate already had this clause; the convergence is on preserving it intact)

8. **[Unanimous] The three-stage taxonomy and the v2.3.2 inversion are sound and should not be scrapped.**
   - Position label: "the premise is right; the boundaries are fragile"
   - Agreed recommendation: Preserve the three-stage breakdown (symbolic parsing → LLM gap-filling → mechanical/deterministic assembly) and the inversion ("pin and cache its output" rather than "make the LLM deterministic"). All proposed edits operate within this structure.
   - Supporting agents: WP (Alignment bullets 2-3), CPC (Executive Summary "structurally honest three-stage determinism taxonomy"), PEG (Alignment bullets 1-3)
   - Evidence basis: WP's praise of in-line determinism property tagging; CPC's coherence-fit assessment; PEG's verification that stages 1 and 3 are testably present in code
   - Pre-existing

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

**Dispute: Audit gating of Recommendation 1 (PEG NN-3 vs. WP non-negotiable on direct land)**

- Positions:
  - **PEG**: The audit gate (Phase 4 Dispute 1, NN-3) is real and unresolved. Synthesis must either (a) record an audit result against the actual codebase before merge, or (b) frame the v2.3.2 clarification as "codifies the discipline that spec 014 implements" rather than asserting it as in force. Allowing the principle to merge with indicative-mood claims about an unverified runtime discipline is a constitutional drift this review series exists to prevent.
  - **WP**: The MUST conversion should land in v2.3.2 directly. The artifact mechanism is named in spec 014 FR-012/FR-020/FR-021; the constitution can codify discipline against a documented artifact contract without making the audit a precondition. v2.3.0 itself codified XXII-XXVII over partly-aspirational surfaces; making v2.3.2 wait for a grep that v2.3.0 did not require is inconsistent governance. The XXIV cross-reference is the constitutional mechanism for "rule exists, test follows."
  - **CPC**: Did not engage the gating question directly; its dispositions assume edits land regardless of audit status.

- Arguments:
  - PEG: A hedge below indicative-mood text is a documentation patch over a verification gap; it is not a substitute for verification when the principle is amending discipline into existence. (Phase 4 Dispute 1.)
  - WP: Fixing the indicative-mood-over-aspirational-runtime precedent is a separate amendment (an explicit "evidence-pending" SIR convention applied across all aspirational principles), not a one-off blocker on XVI. (Phase 4 Dispute 1.)
  - WP's proposed compromise: Adopt modified Recommendation 1 text **and** add to the v2.3.2 SIR (New Recommendation A) a one-line audit-status line.

- Synthesizer assessment (editorial only): PEG's framing carries weight because the candidate text is asserting properties of a runtime that PEG has demonstrated is partly absent. WP's compromise (record audit status in the SIR rather than gate the entire merge) is the path of least resistance and aligns with the v2.3.0 governance precedent. The compromise is structurally similar to PEG's (b) — frame the clarification with a verification status — but lighter touch. Both positions are coherent; this is a process question (who pays the verification cost: this PR or a follow-up) more than a substance question.

- Recommended resolution: Adopt WP's compromise. Land the modified Recommendation 1 text in v2.3.2 with the v2.3.2 SIR carrying a one-line audit-status entry recording either the grep result or "evidence-pending — pinning discipline assumes spec 014 FR-012/SC-004 enforcement; contract test (Principle XXIV) follow-up filed as a separate spec." This satisfies WP's "land it now" and PEG's "be honest about evidence status" simultaneously without making them mutually exclusive. If a maintainer or arbiter prefers PEG's stricter gate, the fallback is to perform the grep before merge (PEG's NN-3, option a).

---

**Dispute: Stage-2 prose specificity (WP `GapFiller.fill()` boundary vs. CPC NR-2 named substeps)**

- Positions:
  - **WP**: Name the `GapFiller.fill()` protocol boundary; treat internal calls as implementation detail. The two-substep prose (question generation + answer extraction) describes `InteractiveGapFiller` specifically; future implementations (e.g., a hypothetical `BatchGapFiller`) could collapse the substeps into a single tool-using model call. Constitutional text that names the substeps locks in the implementation.
  - **CPC NR-2**: Bound stage-2 stochasticity to two named substeps explicitly: "(a) translating gap identifiers into natural-language questions, and (b) extracting parameter values from the user's natural-language answers — both of which are pinned together per deliberation run." This drives a more granular V phase-report line.
  - **PEG**: Defer to WP's modified protocol-level framing for the principle text. CPC's V phase-report content should reference `SourceProvenance.filled_by` rather than the substep names.

- Arguments:
  - WP: CPC's V phase-report line ("across question generation and answer extraction") operationalizes the split into a runtime observability contract that is normative. (Phase 4 Dispute 3.)
  - CPC: The two-substep prose is descriptive (explaining what currently happens), not mandatory; the V observability handle is more useful with named substeps. (CPC revision NR-2.)
  - PEG: The orchestrator can observe `filled_by` counts without observing substeps; substep naming is below the protocol boundary.

- Synthesizer assessment (editorial only): WP's protocol-boundary framing better preserves implementation freedom and is grounded in the actual codebase (`GapFiller.fill()` is the protocol seam). CPC's split is descriptively accurate for `InteractiveGapFiller` but constitutionally fragile for hypothetical future implementations. PEG defers to WP. The 2-vs-1 alignment plus the implementation-lock-in concern favors WP's framing.

- Recommended resolution: Adopt WP's modified Rec 7 text — "stochastic at the `GapFiller.fill()` boundary; whether the implementation makes one model invocation or several is an implementation detail; all resulting parameter values **MUST** be pinned together once `fill()` returns." For CPC's V phase-report observability, replace "across question generation and answer extraction" with "across the resolved subcalls of `GapFiller.fill()`" or anchor directly to `SourceProvenance.filled_by` counts. This preserves CPC's observability win without the implementation lock-in. If a maintainer prefers CPC's substep prose, scope the substep names to "currently" / "in InteractiveGapFiller" so future implementations remain free.

---

**Dispute: Stage-3 vocabulary fix placement (XVI rename vs. VIII parenthetical)**

- Positions:
  - **WP and PEG**: Rename "Mechanical assembly" → "Deterministic assembly" inside XVI stage 3 to match `construction.py:8-14` and spec 014 FR-012. Eliminates the drift instead of documenting it.
  - **CPC**: Add the reconciliation as a parenthetical to Principle VIII line 178: "(In v2.3.2, Principle XVI uses 'mechanical' specifically for the post-pinning assembly stage — the term subsumes the determinism XVI describes.)" If WP/PEG insist on renaming, fall back to CPC's Option B (equivalence note inside XVI) as a compromise.

- Arguments:
  - CPC (Phase 4 Dispute 3): WP and PEG optimize for codebase-text alignment; CPC optimizes for principle-to-principle alignment. Renaming inside XVI leaves VIII's "mechanical" treatment unrevised and creates a new principle-vs-principle drift. The principle-level term is "mechanical" (per VIII); XVI is a downstream consumer of that vocabulary.
  - WP/PEG: Code-vs-constitution drift is the more visible failure mode. Future readers grep the codebase, not the constitution; the fix should land where the drift is visible.

- Synthesizer assessment (editorial only): Both positions identify a real risk and are mutually defensible. CPC's principle-to-principle coherence concern is structurally important; WP/PEG's code-text alignment concern is operationally important. The two are not mutually exclusive: renaming XVI stage 3 to "Deterministic assembly" AND adding a one-line parenthetical to VIII line 178 closes both gaps. This is a compose-both, not pick-one, situation.

- Recommended resolution: Rename XVI stage 3 to "Deterministic assembly" (per WP/PEG, 2-of-3 alignment + code grounding) **and** add a one-line parenthetical to VIII line 178 acknowledging the term shift (per CPC, principle-to-principle coherence). One edit each, both at P2. If a maintainer prefers single-fix economy, CPC's Option B (equivalence note inside XVI) is the acceptable single-edit form because it acknowledges both surfaces; the rename-only form leaves VIII unrevised and re-creates a drift CPC is right to flag.

---

**Dispute (lower stakes): Principle II stable-interface sub-bullet for `objective.yml` schema**

- Positions:
  - **CPC (NN, but flexible)**: The clarification block must contain an explicit Principle II cross-reference declaring `objective.yml`'s schema (parameter names, keying, structure) a stable interface. II creates the obligation that schema changes coordinate updates across all consumers; XI alone (no duplication) does not capture this coordination obligation.
  - **PEG New Rec 2**: Combine `objective.yml`, X (findability), and XI (single source) into one anchor sentence — omits II.
  - **WP Rec 6**: Names `objective.yml` as the storage location but does not lift it to II contract status.

- Arguments:
  - CPC (Phase 4 Dispute 2, flexibility item 2): II and XI do different work. PEG's three-anchor merge is efficient but elides the coordination-on-schema-change distinction. CPC offers to defer to a v2.3.3 PATCH if synthesis judges the clarification block at bloat capacity.
  - PEG: The clarification block already absorbs five cross-references (VII, X, XI, XXIV, V); II adds clutter.
  - WP: Did not engage explicitly.

- Synthesizer assessment (editorial only): CPC's coordination-on-schema-change concern is real but does not block the v2.3.2 amendment. CPC itself marks this as flexible — defer to v2.3.3 if needed. The simpler resolution preserves CPC's substantive concern via a one-line sub-bullet without bloating the block.

- Recommended resolution: Add a single sub-bullet adjacent to the XI anchor: "The `objective.yml` schema (parameter names, keying, and structure) is a Principle II stable interface; changes require coordinated update of all consumers." If late-edit pressure removes this, defer to a v2.3.3 PATCH per CPC's flexibility statement.
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

The deliverable. Every change traces back to a specific scorecard recommendation.

### P1 (must land in v2.3.2)

1. **Replace candidate L463-466 with `objective.yml`-anchored MUSTs.**
   - Source: WP Rec 1 (modified) + PEG Rec 2 (strengthened) + CPC Rec #2 (reframed); Convergence 1.
   - Exact description: Replace "the resulting parameter values are **pinned per deliberation run**. Repeating a deliberation with the same input does NOT re-call the LLM for parameters; cached values from the first resolution are reused. Cross-run variance is acceptable; within-run variance is prohibited." with: "Resolved parameter values **MUST** be persisted to `objective.yml` (spec 014 FR-012) for the duration of the deliberation run. The LLM **MUST NOT** be re-invoked for parameter resolution within the same run; values **MUST** be re-loaded from `objective.yml` rather than re-resolved. (a) The LLM MUST NOT be re-invoked for parameter resolution within a single deliberation run; (b) cross-run variance in resolved parameter *values* is acceptable (e.g., two `/conversus mode` invocations on the same `problem.md` MAY produce different `objective.yml` files); (c) cross-run variance in the assembled objective function's *shape* (parameter names, template selection, gap-identifier set) is prohibited."

2. **Author the VII↔XVI carve-out in XVI's v2.3.2 clarification; add a back-reference in VII line 163.**
   - Source: WP Rec 3 (modified) + CPC Rec #1 (modified) + PEG Rec 9 (refined); Convergence 2.
   - Exact description: In XVI clarification (L491-493), replace "Principle XVI claims **within-run** determinism..." with: "Principle XVI **requires** within-run determinism for the assembled objective function and cross-run reproducibility once parameters are pinned. This carves an explicit exception to Principle VII line 163's unconditional 'structurally identical output': the assembled objective function is the determinism boundary, not the LLM-resolved parameter values that feed into it." In Principle VII line 163, append: "(narrowed by Principle XVI for LLM gap-filling output)".

3. **Add v2.3.2 Sync Impact Report.**
   - Source: WP New Recommendation A + PEG New Rec 1; Convergence 6.
   - Exact description: Prepend a v2.3.2 SIR block above the existing v2.3.1 SIR. Document: (a) version 2.3.1 → 2.3.2 (PATCH — XVI determinism scope clarification); (b) modified Principle XVI (3-stage pipeline + clarification block); (c) effect on Principle VII (narrowed via back-reference parenthetical); (d) origin = spec 068 self-consistency deliberation; (e) verification status of the pinning discipline (audit result OR "evidence-pending: pinning discipline assumes spec 014 FR-012/SC-004 enforcement; contract test per Principle XXIV filed as a follow-up to spec 014").

4. **Add `SourceProvenance.filled_by` audit hook + orchestrator attribution + VII line 167 distinction.**
   - Source: WP Rec 10 (modified) + CPC Rec #4 (replacement) + PEG Rec 6; Convergence 3.
   - Exact description: Add to clarification block (after the carve-out): "The run orchestrator **MUST** persist resolved parameter values to `objective.yml`; pinning is auditable via `SourceProvenance.filled_by` (`conversus/schemas/construction.py:262-279`) — a sanctioned form of explicit, keyed persistence distinguished from the ambient state Principle VII line 167 prohibits."

5. **Define "deliberation run" via `objective.yml` lifetime.**
   - Source: WP Rec 2 (modified) + CPC NR-1 + PEG Rec 5 (strengthened); Convergence 4.
   - Exact description: Add to clarification block: "*deliberation run*: the lifetime of one `objective.yml` artifact; retries that reuse the same artifact are part of the same run, separate `/conversus run` invocations producing new artifacts are different runs. Cross-version replay (re-running after a `conversus` upgrade) is out of scope of this principle."

### P2 (should land in v2.3.2)

6. **Convert "claims" to "requires" at L491.** Source: WP Rec 4 (surviving). One-word swap covered by the rewrite in P1 #2 above.

7. **Add Principle XXIV cross-reference for the re-resolution prohibition.**
   - Source: CPC Rec #3 (surviving with caveat) + WP Rec 8 (corrected anchor) + PEG Rec 10 (out-of-band action).
   - Exact description: Append to clarification block: "Enforcement: Principle XXIV applies — a contract test reproducing the re-resolution failure pattern is required (follow-up to spec 014 FR-012/SC-004 acceptance criteria, and to file a CI lint detecting re-entrant `GapFiller.fill()` calls)."

8. **Reconcile mechanical/deterministic vocabulary.**
   - Source: WP New Rec B + CPC Rec #8 (P3 → P2) + PEG Rec 3 (strengthened); Convergence 5; **placement disputed** — see Remaining Disputes Dispute 3.
   - Exact description (recommended compose-both form): Rename "Mechanical assembly" → "Deterministic assembly" inside XVI stage 3 (L468-470) and add a parenthetical to Principle VIII line 178: "(In v2.3.2, Principle XVI uses 'mechanical' co-extensively with the 'deterministic' vocabulary used by spec 014 FR-012 and `conversus/schemas/construction.py:8-14`.)"

9. **Cite spec 014 FR-012/SC-004 in the Origin block (correcting the spec 013 mis-anchor).**
   - Source: WP Rec 8 (modified) + PEG Rec 4 (hold).
   - Exact description: Update Origin block (L500-503) to read: "Origin: game engine vision (specs 012-019) — pinning behavior is specified in **spec 014 FR-012/SC-004** (assembly determinism) and FR-020/FR-021 (artifact contract). Spec 013 supplies the template definitions stage 1 parses. Some referenced runtime layers (specs 016-019, optimizer/nashopt/ampl) are spec'd but partly under construction; this principle codifies the discipline they will satisfy when implemented. Enforcement is verified by a contract test per Principle XXIV at the path declared in spec 014's contracts."

10. **Anchor `objective.yml` schema as Principle II stable interface (sub-bullet form).**
    - Source: CPC Rec #5 (modified) — see **Remaining Disputes Dispute 4**; PEG New Rec 2 (alternative).
    - Exact description: Add a sub-bullet adjacent to the XI anchor: "The `objective.yml` schema (parameter names, keying, and structure) is a Principle II stable interface; changes require coordinated update of all consumers." (Defer to v2.3.3 PATCH if late-edit pressure removes — CPC accepts.)

11. **Tighten solver-equivalence claim at L488-489.**
    - Source: CPC Rec #10 (surviving) + WP cross-review concession.
    - Exact description: Replace "Changing solvers MUST NOT change what is being optimized." with: "The objective function — *what is being optimized* — is the contract between user intent and mathematical optimization. Changing solvers MUST NOT change the objective function (Principle VII applies to the objective-function contract). Numerical optimization output may vary across solvers within documented stability bounds; that variance is solver behavior, not a violation of this principle."

12. **Resolve stage-2 prose specificity (`GapFiller.fill()` boundary).**
    - Source: WP Rec 7 (modified, P3) — see **Remaining Disputes Dispute 2**.
    - Exact description: In stage 2 prose, replace "stochastic at the LLM call, but the resulting parameter values are pinned per deliberation run. Repeating a deliberation with the same input does NOT re-call the LLM for parameters; cached values from the first resolution are reused." with: "stochastic at the `GapFiller.fill()` boundary. The protocol entrypoint is one call; whether the implementation makes one model invocation or several is an implementation detail. All resulting parameter values **MUST** be pinned together once `fill()` returns." (Pair with P1 #1 above.)

### P3 (nice to have / out-of-band)

13. **Define "fully-pinned parameter set" inline.** Source: WP Rec 9 (surviving). Add at L469: "given a template and a *fully-pinned parameter set* (every gap identifier produced by stage 1 has an associated pinned value from stage 2)."

14. **Add Principle V observability obligation for stage-2 phase reporting.** Source: CPC Rec #6 (surviving) + PEG Rec 6 hook. Add to clarification: "Stage 2 emits a Principle V phase report line: `{N} gap identifiers resolved ({K} from cache, {N-K} newly resolved across the resolved subcalls of `GapFiller.fill()`).` The runtime line is backed by `SourceProvenance.filled_by` provenance tagging."

15. **Cross-reference VII at L489 for solver substitution.** Source: CPC Rec #7 (surviving). Already incorporated into P2 #11 above.

16. **File follow-up spec for CI lint detecting re-entrant `GapFiller.fill()` calls.** Source: PEG Rec 10 (out-of-band) + CPC Rec #3 cross-reference; out-of-band action item, not a constitutional edit.

17. **Add regression test for spec 014 SC-004.** Source: PEG Rec 8 (out-of-band). Implementation-side; not a constitutional edit.

---

## Key Concessions

### wording-precision

- **Conceded the cache-vs-artifact framing**: WP's Phase 1 Recommendation 1 framed pinning as a wording problem ("descriptive prose where MUST belongs") and would have, applied verbatim, mandated a non-existent runtime cache. WP modified Rec 1 in revision (revision §"Recommendation 1") to anchor to PEG's `objective.yml` artifact. WP's revision Position Summary explicitly states this: "I framed it as a wording problem; PEG reframed it as a sequenced grounding problem. Adopting only my framing would have locked in a constitutional obligation against a non-existent runtime cache."
- **Conceded the "bit-for-bit" scope qualifier**: WP's Phase 1 Alignment bullet 3 praised "bit-for-bit" without distinguishing stage 3 mechanical assembly from solver substitution. In WP cross-review of CPC (Dangerous Contradiction #3), WP conceded the scope qualifier and tightened the praise to apply only to stage 3 mechanical assembly.
- **Conceded the spec 013 → spec 014 FR-012 anchor correction**: WP's Phase 1 Recommendation 8 named spec 013 as the FR anchor; PEG's cross-review showed spec 014 is the correct anchor. WP modified Rec 8 in revision.
- **Conceded the missed mechanical/deterministic terminology drift**: WP's Phase 1 review missed this drift entirely; WP added New Recommendation B in revision once both PEG (P1) and CPC (P3 → P2) surfaced it.

### cross-principle-coherence

- **Withdrew Recommendation #4 ("ambient state" reconciliation)**: CPC's Phase 1 Rec #4 framed the cache as VII-prohibited-needs-explicit-sanction; PEG's grounding showed there is no cache. CPC's revision (revision §"Rec #4 — Withdrawn — partially supplanted") explicitly withdrew the recommendation, reframing the persistence at `objective.yml`.
- **Withdrew the "amend VII" half of Recommendation #1**: CPC's Phase 1 Rec #1 prescribed amending Principle VII to acknowledge XVI's narrowing. WP cross-review of CPC (Dangerous Contradiction #1) flagged that authoring the carve-out in both VII and XVI violates Principle XI. CPC withdrew the VII-amendment half in revision (revision §"Rec #1 — Modified") and accepted a back-reference parenthetical only.
- **Promoted Rec #8 from P3 to P2**: CPC's Phase 1 Rec #8 marked the mechanical-vs-deterministic terminology drift as P3. PEG's three-way drift evidence promoted the priority; CPC's revision (revision §"Rec #8 — Modified — promoted from P3 to P2") explicitly upgraded.
- **Reframed Rec #2 to anchor on `objective.yml`**: CPC's Phase 1 Rec #2 added a Principle XI cross-reference to "the cache." CPC's revision retained the XI cross-reference but anchored it to `objective.yml` per PEG's grounding.
- **Reframed Rec #5 to anchor on `objective.yml` schema**: CPC's Phase 1 Rec #5 treated pinned parameters as a hypothetical contract surface. CPC's revision lands the II classification on `objective.yml`'s schema.

### pr-evidence-grounding

- **Refined Rec 1 from parallel hedge to gating step**: PEG's Phase 1 Rec 1 prescribed an "evidence-pending" hedge OR audit. After WP's cross-review framed the audit as a sequencing question rather than an alternative to MUST conversion, PEG's revision (revision §"Rec 1") refined the recommendation: the audit must happen pre-merge (gating); the hedge is the fallback. This is a tightening, not a withdrawal — PEG carried the gating concern into Phase 4 disputes (Dispute 1).
- **Withdrew Rec 7 (stage-2 substep split)**: PEG's Phase 1 Missed Opportunity #8 weakened the case for the question/extraction split; PEG's revision Position Summary states "I would now decline to push for that disambiguation."
- **Conceded that the candidate's three-stage taxonomy and the v2.3.2 inversion are sound**: PEG's Phase 1 review focused on grounding gaps, not premise; PEG's Position Summary explicitly endorses the taxonomy and the "pin and cache its output" inversion as the candidate's strongest features.

---

*Synthesizer note*: this is a high-quality cooperative deliberation. All three reviewers stayed cooperative, made concessions when grounded by evidence (most strikingly CPC's withdrawal of Rec #4 and the amend-VII half of Rec #1), and converged on five named convergence points. The remaining four disputes are tractable; three of them recommend compose-both resolutions and one (Dispute 1, audit gating) is a process question with a defensible compromise. The amendment is not fragile in its premise (the three-stage taxonomy and the v2.3.2 inversion both survive across all three reviews); it is fragile at its boundaries with VII, XI, II, V, X, and the codebase, and the boundaries are fixable by the coordinated edit set above.
