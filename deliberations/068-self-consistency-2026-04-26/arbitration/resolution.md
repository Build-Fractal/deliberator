# Spec 068 Self-Consistency Arbitration — Binding Decisions

**Arbiter**: spec-068-arbiter (balanced-arbiter preset)
**Influence**: binding
**Trigger**: always
**Target**: `CONSTITUTION-v2.3.2-candidate.md` (Principle XVI v2.3.2 clarification, lines 491-498, plus adjacent edits)
**Scope**: 4 unresolved disputes named in `summary/final.md` between `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->`
**Acceptance bar (per spec 067 §4.4)**: 0 ACCEPT-level findings on the spec 068 amendment specifically before the implementation PR can merge.

---

## Process Note

- Trigger: `always` — arbitration was activated unconditionally for this self-consistency run.
- Disputes remaining per synthesis: 4.
- Agents: wording-precision (WP), cross-principle-coherence (CPC), pr-evidence-grounding (PEG).
- Mode: cooperative with subject arbitration. Synthesizer offered editorial recommendations on three of four disputes; the arbiter is binding.
- Convergence already locked (not re-litigated): 8 named convergence points in synthesis §"Convergence Achieved" (artifact anchor on `objective.yml`, single-home VII↔XVI carve-out, `SourceProvenance.filled_by` hook, deliberation-run definition, vocabulary-drift acknowledgment at P2, v2.3.2 SIR, falsification-clause preservation, three-stage taxonomy preservation). All four binding decisions below operate within these convergences.
- The synthesis's "Actionable Spec Changes" §P1 1-5 and §P2 6-11 are the convergence-driven base edit set; the rulings below resolve which of the disputed alternatives layers onto that base.

---

## Decision Framework

The grounding document is the v2.3.2 candidate constitution. The principles below are quoted from it (line numbers refer to the candidate file).

- **[XI. Single Source of Truth — anti-duplication]**: "If you find yourself writing the same fact in two places, stop. One of them is wrong, or will be soon." (Principle XI, lines 316-317.) Authoritative-source-or-derive. Bears on Disputes 3 and 4.

- **[XI. Registry-First Declaration / single authoritative source]**: Extension v2.3.0 establishes that artifact contracts (registry, schema YAML) are the single source of truth and that hand-written declarations diverging from them are violations. (Principle XI extension, lines 324-342.) Bears on Dispute 4 (whether `objective.yml`'s schema needs II coverage on top of its XI single-source coverage).

- **[II. Stable Interfaces — coordinated change]**: "Changing a stable interface requires updating every consumer (specs, templates, SKILL.md sections, reference files) in a single atomic change. New interfaces SHOULD be marked stable only after at least one spec has consumed them successfully." (Principle II, lines 98-102.) Bears on Dispute 4 (the coordination obligation that XI alone does not capture, and the maturity gate before declaring an interface stable).

- **[VIII. Templating Engines Over Inference — implementation freedom]**: "Mode-specific behavior is encoded in templates, not inferred by agents at runtime. The template dictates the output shape — the agent provides the content within that shape." (Principle VIII, lines 185-187.) The principle preserves implementation freedom above the protocol boundary. Bears on Dispute 2 (whether to name internal substeps or the protocol seam).

- **[XII. No Dead Infrastructure — current consumers]**: "Every provisioned capability MUST have at least one consumer." (Principle XII, line 345.) Distinct corollary: the constitution may not silently sanction infrastructure that has no implementation today. Bears on Dispute 1 (whether the v2.3.2 clarification asserts properties of code that does not yet exist).

- **[XIV. Spec-Implementation Parity]**: "Specs and implementations MUST agree on what was built. A spec that says 'Phase 1-5' when the implementation does 'Phase 1 only' is a bug in the spec, even if the implementation is correct." (Principle XIV, lines 392-396.) Bears directly on Dispute 1: an indicative-mood constitutional claim about a discipline the codebase does not currently enforce is a parity gap, not merely a wording gap.

- **[XXIV. Safety-Critical Defense-in-Depth — three-layer enforcement]**: Schema-required, parser-validated, contract-tested. "every safety-critical path has at least one test that **reproduces the original bug or failure pattern** the principle was created to prevent." (Principle XXIV, lines 712-738.) Bears on Dispute 1 (the constitutional mechanism for "rule exists, enforcement test follows") and Dispute 4 (II's coordination obligation pairs with XXIV's test obligation).

- **[Governance — versioning]**: "MAJOR for principle removals or redefinitions, MINOR for new principles or material expansions, PATCH for clarifications." (Governance, line 896.) v2.3.2 is a PATCH; PATCH amendments are permitted to clarify discipline against documented spec contracts (here: spec 014 FR-012/FR-020/FR-021) without the contract test having yet shipped, provided the clarification declares its enforcement layer (XXIV).

---

## Binding Decisions

### Dispute 1: Audit gating of Recommendation 1 (PEG NN-3 vs. WP direct-land)

**Positions:**
- **PEG (NN-3)**: The audit MUST happen pre-merge or the v2.3.2 clarification MUST be reframed as "codifies the discipline that spec 014 implements" rather than asserting the discipline as in force. Allowing the principle to merge with indicative-mood claims about an unverified runtime discipline is a constitutional drift this review series exists to prevent.
- **WP (direct-land)**: The MUST conversion lands in v2.3.2 directly. The artifact contract is documented in spec 014 FR-012/FR-020/FR-021; XXIV is the constitutional mechanism for "rule exists, contract test follows." Making v2.3.2 wait for a grep that v2.3.0 did not require for analogous text would be inconsistent governance.
- **CPC**: Did not engage the gating question; assumed edits land regardless of audit status.

**Synthesizer's assessment:** "PEG's framing carries weight because the candidate text is asserting properties of a runtime that PEG has demonstrated is partly absent. WP's compromise (record audit status in the SIR rather than gate the entire merge) is the path of least resistance and aligns with the v2.3.0 governance precedent... Both positions are coherent; this is a process question (who pays the verification cost: this PR or a follow-up) more than a substance question."

**Ruling:** ACCEPT (with WP's compromise form) — the v2.3.2 SIR MUST carry an explicit audit-status line; the indicative MUST text lands as written.

**Grounding citation:** Principle XIV (Spec-Implementation Parity, lines 392-396) requires that the constitution and the implementation agree on what was built; Principle XXIV (lines 712-738) supplies the constitutional mechanism for "rule exists, enforcement test follows"; Governance §Versioning (line 896) permits PATCH clarifications against documented spec contracts.

**Rationale:** PEG's parity concern is real — XIV explicitly makes asymmetry between spec text and implementation a bug — but the parity remedy XIV describes is to update the spec to match reality, not to block PATCH amendments that codify documented contracts. Spec 014 FR-012/FR-020/FR-021 is the documented contract; XXIV is the mechanism for the test that enforces it. The constitution is permitted to codify discipline against a documented artifact contract provided it routes enforcement through XXIV and is honest about evidence status. WP's compromise (adopt §P2 #7's XXIV cross-reference plus a v2.3.2 SIR audit-status line) satisfies both PEG's "be honest about evidence status" and XIV's parity obligation without creating the inconsistent-governance precedent WP correctly identifies (v2.3.0's XXII point 3 and XXIV future-test references shipped under the same posture).

**Rejected position:** PEG's NN-3 stricter gate (pre-merge grep as a hard precondition). PEG is right that a hedge is not a substitute for verification when verification is feasible — but the verification PEG names is feasible in the follow-up to this PR (file the contract test as a spec 014 acceptance criterion), and gating v2.3.2 on it would block a precision-affecting clarification on enforcement work that XXIV already obligates. The XIV parity bug PEG identifies is a constitutional concern about all amendments asserting properties of partly-aspirational code, not a defect specific to spec 068's XVI clarification; fixing it via a one-off block on this PR is exactly the inconsistent governance WP flags.

**Required changes:**
1. Adopt synthesis §P1 #1 (`objective.yml`-anchored MUST set, replacing candidate L463-466) verbatim.
2. Adopt synthesis §P1 #3 (v2.3.2 SIR) AND extend its bullet (e) to read literally: *"verification status of the pinning discipline: evidence-pending — pinning discipline assumes spec 014 FR-012/SC-004 enforcement; contract test per Principle XXIV filed as a follow-up to spec 014 (and CI lint detecting re-entrant `GapFiller.fill()` per spec 068 follow-up)."*
3. Adopt synthesis §P2 #7 (XXIV cross-reference for the re-resolution prohibition) verbatim — this is the load-bearing enforcement-routing edit and must not be dropped.

If the implementer prefers to perform the grep before merge (PEG's option a) and the result is positive, replace bullet (e) with the grep result and the XXIV cross-reference in §P2 #7 still lands.

---

### Dispute 2: Stage-2 prose specificity (WP `GapFiller.fill()` boundary vs. CPC NR-2 named substeps)

**Positions:**
- **WP**: Name the `GapFiller.fill()` protocol boundary; treat internal calls as implementation detail. Future implementations (e.g., a hypothetical `BatchGapFiller`) could collapse the substeps into a single tool-using model call. Constitutional text that names the substeps locks in the implementation.
- **CPC NR-2**: Bound stage-2 stochasticity to two named substeps explicitly: "(a) translating gap identifiers into natural-language questions, and (b) extracting parameter values from the user's natural-language answers — both of which are pinned together per deliberation run." Drives a more granular V phase-report line.
- **PEG**: Defer to WP's modified protocol-level framing. CPC's V phase-report content should reference `SourceProvenance.filled_by` rather than the substep names.

**Synthesizer's assessment:** "WP's protocol-boundary framing better preserves implementation freedom and is grounded in the actual codebase (`GapFiller.fill()` is the protocol seam). CPC's split is descriptively accurate for `InteractiveGapFiller` but constitutionally fragile for hypothetical future implementations. PEG defers to WP. The 2-vs-1 alignment plus the implementation-lock-in concern favors WP's framing."

**Ruling:** ACCEPT WP's modified Rec 7 (`GapFiller.fill()` protocol boundary) as the principle text; ACCEPT a softened form of CPC's V observability obligation anchored to `SourceProvenance.filled_by`.

**Grounding citation:** Principle VIII (lines 185-187) preserves implementation freedom above the protocol seam; Principle XI (line 316-317) prohibits restating implementation detail in the constitution when an authoritative source already exists; Principle XIV (lines 392-396) bars the constitution from prescribing structure the implementation may not preserve.

**Rationale:** CPC's substep names are accurate today (for `InteractiveGapFiller`) but become a XIV parity bug the moment a future implementation collapses them. The protocol seam is the load-bearing abstraction — VIII says the agent provides content within the template's shape, and the constitutional analogue is that the principle names the seam, not what happens below it. CPC's V observability concern is real and survives intact when re-anchored to `SourceProvenance.filled_by` (the data structure that records *what* was pinned, regardless of how many subcalls produced it). PEG's deference and the codebase grounding (`GapFiller.fill()` is the orchestrator-visible boundary) settle the alignment 2-of-3 plus codebase evidence in favor of WP.

**Rejected position:** CPC's NR-2 substep-named prose at the principle level. CPC correctly identifies a V observability win, but the win does not require naming substeps in the constitution — anchoring the V phase-report line to `filled_by` counts captures the same observability without locking in the implementation. CPC's flexibility statement (Phase 4 disputes §"Flexibility 1") explicitly accepts the rename if VIII receives a footnote; the analogous compromise here is that CPC's substep-named V phase-report line is replaced with a `filled_by`-anchored form, which CPC's own framing endorsed in Convergence 4 ("`SourceProvenance.filled_by` is the auditable hook").

**Required changes:**
1. In Principle XVI stage 2 prose (candidate L462-466), apply the WP-modified Rec 7 text in place of the candidate's "stochastic at the LLM call, but the resulting parameter values are pinned per deliberation run. Repeating a deliberation with the same input does NOT re-call the LLM for parameters; cached values from the first resolution are reused." Replacement (combined with §P1 #1's `objective.yml` MUSTs):

   *"stochastic at the `GapFiller.fill()` boundary. The protocol entrypoint is one call; whether the implementation makes one model invocation or several is an implementation detail. All resulting parameter values **MUST** be pinned together once `fill()` returns. Resolved parameter values **MUST** be persisted to `objective.yml` (spec 014 FR-012) for the duration of the deliberation run; the LLM **MUST NOT** be re-invoked for parameter resolution within the same run; values **MUST** be re-loaded from `objective.yml` rather than re-resolved."*

2. For synthesis §P3 #14 (Principle V observability obligation), the V phase-report line MUST read: *"Stage 2 emits a Principle V phase report line: `{N} gap identifiers resolved ({K} from `objective.yml`, {N-K} newly resolved via `GapFiller.fill()` and recorded under `SourceProvenance.filled_by`).`"* — that is, no substep names; observability anchored to the data-structure hook all three reviewers converged on.

---

### Dispute 3: Stage-3 vocabulary fix placement (XVI rename vs. VIII parenthetical)

**Positions:**
- **WP and PEG**: Rename "Mechanical assembly" → "Deterministic assembly" inside XVI stage 3 to match `construction.py:8-14` and spec 014 FR-012. Eliminates the drift instead of documenting it.
- **CPC**: Add the reconciliation as a parenthetical to Principle VIII line 178: "(In v2.3.2, Principle XVI uses 'mechanical' specifically for the post-pinning assembly stage — the term subsumes the determinism XVI describes.)" Renaming inside XVI without touching VIII leaves VIII's "mechanical" treatment unrevised and creates a new principle-vs-principle drift.

**Synthesizer's assessment:** "Both positions identify a real risk and are mutually defensible. CPC's principle-to-principle coherence concern is structurally important; WP/PEG's code-text alignment concern is operationally important. The two are not mutually exclusive: renaming XVI stage 3 to 'Deterministic assembly' AND adding a one-line parenthetical to VIII line 178 closes both gaps. This is a compose-both, not pick-one, situation."

**Ruling:** ACCEPT both edits (compose-both). Rename "Mechanical assembly" → "Deterministic assembly" in XVI stage 3 AND add CPC's one-line parenthetical to VIII.

**Grounding citation:** Principle XI anti-duplication clause (lines 316-317) is the operative constraint in both directions: code-vs-constitution drift and principle-vs-principle drift are both the same class of bug ("information in two places that disagreed"). Closing both gaps satisfies XI on both axes; closing only one leaves a residual drift XI prohibits.

**Rationale:** WP/PEG are right that renaming inside XVI eliminates the code-vs-constitution drift PEG sourced. CPC is right that renaming inside XVI alone creates a new drift between VIII's "mechanical" vocabulary and XVI's renamed stage 3. Both concerns are XI violations of the same shape; both deserve a fix; the cost of composing both is one extra line. WP's flexibility statement (§"Flexibility 2") accepts CPC's Option B if rename ripples too widely; CPC's flexibility (Phase 4 §"Flexibility 1") accepts the XVI rename if VIII receives a footnote. The composition is exactly the meet of both flexibilities. This is the synthesizer's recommended resolution and the arbiter concurs without modification.

**Rejected position:** Single-edit forms (rename-only or parenthetical-only) are rejected. CPC's framing at Phase 4 §"Flexibility 1" — the rename is acceptable on the condition that VIII line 178 receives at minimum a footnote acknowledging the term shift — is the exact form ACCEPTed here, so CPC's substantive concern is preserved. WP and PEG's preference for codebase-text alignment is also preserved by the rename. No reviewer's load-bearing position is overridden.

**Required changes:**
1. In Principle XVI stage 3 (candidate line 468-470), rename the label and update the body:
   - **Old (line 468)**: `3. **Mechanical assembly**: deterministic — given a template`
   - **New**: `3. **Deterministic assembly**: given a template`
   (The descriptor "deterministic" no longer needs to follow the colon since it is now in the label; preserve the rest of the sentence as-is.)
2. In Principle VIII (candidate line 178), append the CPC parenthetical immediately after "Prefer mechanical template-driven behavior over LLM inference and improvisation.":
   - Append: *"(In v2.3.2, Principle XVI uses 'deterministic' for the post-pinning assembly stage; the term is co-extensive with VIII's 'mechanical' — both denote rule-based, non-inference-driven execution.)"*
   (Note: CPC's original parenthetical referenced "mechanical" subsuming "determinism"; with the rename the relationship inverts. The wording above preserves CPC's intent while acknowledging the rename.)
3. Update the v2.3.2 SIR (synthesis §P1 #3) to mention this rename in the "Modified principles" line: *"XVI (3-stage pipeline + clarification block; stage 3 renamed 'Mechanical assembly' → 'Deterministic assembly' for spec 014 / `construction.py` vocabulary alignment)"* and the "VIII coordination" line: *"VIII line 178 receives a parenthetical co-extensive note."*

---

### Dispute 4: Principle II stable-interface sub-bullet for `objective.yml` schema

**Positions:**
- **CPC (NN, but flexible)**: Add a Principle II cross-reference declaring `objective.yml`'s schema (parameter names, keying, structure) a stable interface. II creates the obligation that schema changes coordinate updates across all consumers; XI alone (no duplication) does not capture this. CPC offers to defer to v2.3.3 PATCH if the clarification block is at bloat capacity.
- **PEG New Rec 2**: Combine `objective.yml`, X (findability), and XI (single source) into one anchor sentence — omits II.
- **WP Rec 6**: Names `objective.yml` as the storage location but does not lift it to II contract status.

**Synthesizer's assessment:** "CPC's coordination-on-schema-change concern is real but does not block the v2.3.2 amendment. CPC itself marks this as flexible — defer to v2.3.3 if needed. The simpler resolution preserves CPC's substantive concern via a one-line sub-bullet without bloating the block."

**Ruling:** DEFER to v2.3.3 PATCH.

**Grounding citation:** Principle II (lines 100-102) — *"New interfaces SHOULD be marked stable only after at least one spec has consumed them successfully."* Principle XII (line 345) — every provisioned capability must have at least one consumer. Governance §Versioning (line 896) — PATCH for clarifications.

**Rationale:** Principle II's own maturity gate is the operative consideration. The candidate text marks `objective.yml` as the artifact anchor for pinning (spec 014); spec 014 is the only spec consuming the schema today, and the schema itself is still under construction (PEG's grounding showed `construction.py:262-279` exists but several optimizer-layer consumers in specs 016-019 do not). II's "SHOULD be marked stable only after at least one spec has consumed them successfully" cuts against lifting `objective.yml`'s schema to a stable interface in v2.3.2 when the second consumer is partly aspirational. CPC's substantive concern (schema changes silently breaking downstream consumers) is real but premature — when spec 016+ ship and add the second consumer, II's coordination obligation becomes load-bearing and the v2.3.3 PATCH is the natural place to record the elevation. CPC's own flexibility statement explicitly accepts this disposition. No ACCEPT-level finding is created against v2.3.2 by deferring.

**Rejected position:** CPC's preferred form (add the II sub-bullet now). CPC's substantive concern is real but II's own SHOULD-clause makes the elevation premature in v2.3.2. PEG's three-anchor merge (PEG New Rec 2) is fine as authored — XI single-source + X findability are the principle anchors load-bearing for v2.3.2's pinning discipline; II joins them when the second consumer arrives.

**Required changes:** None for v2.3.2. The synthesis §P2 #10 sub-bullet is dropped from the v2.3.2 implementation set.

**Unblock condition for v2.3.3** (documented for the future PR author): when spec 016 (or any other consumer beyond spec 014's `construction.py`) lands a second reader of `objective.yml`'s schema, file a v2.3.3 PATCH adding the II sub-bullet adjacent to the XI anchor: *"The `objective.yml` schema (parameter names, keying, and structure) is a Principle II stable interface; changes require coordinated update of all consumers."* The work belongs in the spec that introduces the second consumer (it is that spec's responsibility to update the constitution that governs its contract surface).

---

## Summary of Changes Required

Prioritized list of all implementation actions emerging from these rulings. Synthesis §"Actionable Spec Changes" §P1 #1-5 and §P2 #6-9, #11 are unaffected (already converged) and remain in scope; the items below are arbiter-introduced or arbiter-modified.

### P1 (block merge if missing)

- **P1-A** *(Dispute 1, ACCEPT with compromise)*: In synthesis §P1 #3 (v2.3.2 SIR), bullet (e) MUST read: *"verification status of the pinning discipline: evidence-pending — pinning discipline assumes spec 014 FR-012/SC-004 enforcement; contract test per Principle XXIV filed as a follow-up to spec 014 (and CI lint detecting re-entrant `GapFiller.fill()` per spec 068 follow-up)."* If the implementer chooses to perform the grep pre-merge and confirms enforcement, replace with the grep result.

- **P1-B** *(Dispute 2, ACCEPT WP-modified Rec 7)*: In Principle XVI stage 2 prose (replacing candidate L462-466), use WP's `GapFiller.fill()` protocol-boundary text composed with synthesis §P1 #1's `objective.yml` MUSTs. Exact wording in §"Required changes" of Dispute 2 above.

- **P1-C** *(Dispute 3, ACCEPT compose-both)*: Rename "Mechanical assembly" → "Deterministic assembly" in XVI stage 3 (candidate line 468) AND append a one-line parenthetical to Principle VIII (candidate line 178). Exact wording in §"Required changes" of Dispute 3 above. The v2.3.2 SIR records the rename and the VIII coordination edit.

### P2 (should land in v2.3.2; convergence-driven, not arbiter-disputed)

- Synthesis §P2 #6, #7, #8, #9, #11 retain as authored. Note that §P2 #8 (mechanical/deterministic vocabulary) is now realized as P1-C above — promoted from P2 to P1 by the compose-both ruling because the VIII coordination edit and the XVI rename are now both load-bearing for the same fix.

- Synthesis §P3 #14 (Principle V observability obligation) is upgraded to P2 by the Dispute 2 ruling because it is the load-bearing carrier for CPC's V observability concern that would otherwise be lost when CPC's substep-named prose is rejected. Use the `SourceProvenance.filled_by`-anchored wording in Dispute 2's §"Required changes" #2.

### P3 (out-of-band)

- Synthesis §P3 #13 (define "fully-pinned parameter set"), #15 (cross-reference VII at L489 — already absorbed into P2 #11), #16 (CI lint follow-up spec), #17 (regression test for spec 014 SC-004) — unchanged.

### Deferred (DEFER, no v2.3.2 action)

- **Dispute 4**: Principle II stable-interface sub-bullet for `objective.yml` schema. Defer to v2.3.3 PATCH. Unblock condition: the spec that introduces the second consumer of `objective.yml`'s schema (likely spec 016+) files the v2.3.3 PATCH adding the II sub-bullet adjacent to the XI anchor. Synthesis §P2 #10 is dropped from the v2.3.2 implementation set.

---

## Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---|---|---|---|
| Dispute 1 — Audit gating | ACCEPT (WP compromise) | High | XIV + XXIV pair gives explicit constitutional mechanism for "rule exists, test follows"; Governance §Versioning permits PATCH against documented spec contracts; v2.3.0 governance precedent (XXII point 3, XXIV future-test references) is the same posture; PEG's flexibility statement permits SIR-recorded evidence status. |
| Dispute 2 — Stage-2 prose | ACCEPT (WP boundary + filled_by V hook) | High | 2-of-3 reviewer alignment (WP, PEG); codebase grounding (`GapFiller.fill()` is the orchestrator-visible boundary per PEG's grounding); CPC's substantive V observability concern is preserved via `filled_by` anchoring per Convergence 4; CPC's own flexibility statement allows compromises that preserve V observability via different surface. |
| Dispute 3 — Stage-3 vocabulary | ACCEPT (compose-both: rename + VIII parenthetical) | High | Synthesizer explicitly recommended compose-both; both reviewer flexibility statements (CPC §"Flexibility 1", WP §"Flexibility 2") accept the compose-both form; XI applies symmetrically to code-vs-constitution and principle-vs-principle drift; cost is one additional line for full XI coverage on both axes. |
| Dispute 4 — Principle II sub-bullet | DEFER to v2.3.3 | High | Principle II's own SHOULD-clause requires successful consumption by at least one spec before stable marking; second consumer is partly aspirational (specs 016+); CPC explicitly marked the recommendation as flexible and accepted the v2.3.3 deferral path; deferring creates no ACCEPT-level finding against v2.3.2. |

**Overall deliberation quality**: high. All three reviewers stayed cooperative and made grounded concessions when evidence demanded — most strikingly CPC's withdrawal of Rec #4 (ambient-state cache reconciliation) and the amend-VII half of Rec #1, on PEG's `objective.yml` grounding. The synthesizer's recommended resolutions for Disputes 2-4 were broadly defensible; the arbiter concurs with synthesizer recommendations on Disputes 2 and 3 (with minor wording tightening for Dispute 2's V observability handle), accepts a slightly different framing for Dispute 1 (anchoring the compromise to XIV + XXIV + Governance §Versioning rather than to WP's "v2.3.0 governance precedent" alone, which is an argument from precedent rather than from principle), and confirms the synthesizer's deferral disposition for Dispute 4 with explicit grounding in Principle II's maturity gate.

The amendment is structurally sound: the three-stage taxonomy, the v2.3.2 inversion ("pin and cache its output" rather than "make the LLM deterministic"), and the falsification clause (L496-498) all survived all three reviews intact. The disputes were boundary disputes — XVI's interaction with VII, VIII, XI, II, V, and XXIV — and the rulings above resolve each at its principle interaction surface without scrapping any load-bearing convergence.

Three of four disputes resolve to ACCEPT-level findings; ACCEPT findings on a v2.3.2 amendment block merge per spec 067 §4.4 until addressed. The required changes are concrete, line-localized, and can be applied in the same PR that lands the convergence-driven base edit set.

---

**SPEC-068 SELF-CONSISTENCY VERDICT: PASS WITH FIXES**

3 ACCEPT-level findings (Disputes 1, 2, 3) requiring concrete edits in the spec 068 implementation PR before merge. 1 DEFER-level finding (Dispute 4) carried to v2.3.3 with documented unblock condition. 0 REJECT findings. The spec 068 amendment is structurally sound; its boundaries with VII, VIII, XI, II, V, and XXIV are repairable by the coordinated edit set above.
