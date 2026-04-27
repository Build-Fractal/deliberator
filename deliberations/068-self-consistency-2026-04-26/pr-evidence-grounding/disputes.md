# Phase 4 Disputes — pr-evidence-grounding

**Reviewer**: pr-evidence-grounding
**Phase**: 4 (final phase before synthesis)
**Target**: CONSTITUTION-v2.3.2-candidate.md, Principle XVI

---

## Remaining Disputes

### Dispute 1 — Whether the audit MUST happen pre-merge or whether the hedge can stand alone

**Status**: Open. wording-precision (WP) Recommendation 1 disposition treats the code grep as a precondition that, if it fails, triggers an "evidence-pending" hedge preceding the MUST conversion. That phrasing is sequenced but conditional — "if a code grep proves the discipline is not yet implemented, an evidence-pending hedge precedes the MUST conversion." My Phase 3 revision (Rec 1, refined) is stricter: the audit MUST happen before merge; the hedge is a fallback only if the audit cannot be performed in this iteration. cross-principle-coherence (CPC) does not engage this gating question directly — its dispositions assume the artifact anchor edits land regardless of audit status.

**Why it matters**: WP's framing permits the v2.3.2 candidate to merge with a hedge in place of verification. Mine does not. The two are not reconcilable by composition — one of them governs the merge gate. If the principle is asserted in the indicative ("MUST be persisted to `objective.yml`") about a discipline that is not actually implemented, the constitution accumulates a false claim regardless of whether the hedge appears below it. A hedge is a documentation patch over a verification gap; it is not a substitute for verification when the underlying discipline is what the principle is amending into existence.

**What evidence would resolve**: A grep over `conversus/schemas/construction.py` and the run-engine entrypoint for: (a) reads of `objective.yml` after first-write within a single run, (b) any path where `GapFiller.fill()` is invoked more than once per gap identifier per run, (c) the test path that would fail if re-resolution were introduced. If (a) is present and (b) is impossible at the call-graph level and (c) exists, the discipline is verified and Rec 1's MUST conversion lands clean. If any of the three is absent, the hedge is required and the principle text must say "v2.3.2 codifies a discipline currently being implemented in spec 014" rather than describing it as in force.

**My position**: Hold the stricter gate. Synthesis should record this as an open question for the arbiter or for the merge author, not paper over it.

### Dispute 2 — Where Rec 7 (stage-2 disambiguation) lands

**Status**: Partial. WP Recommendation 7 disposition modified — names the `GapFiller.fill()` boundary, lets stochasticity be a property of that one call, and downgrades P2 → P3. CPC's New Recommendation NR-2 goes the other direction — splits stage 2 into two named substeps (question generation + answer extraction) at P2, with the split surfaced in the V phase-report line. My Phase 3 revision withdrew Rec 7 entirely on the grounds that the `GapFiller.fill()` boundary is the protocol-level abstraction the principle should name; CPC's split describes implementation detail that may shift.

**Why it matters**: Three different positions on the same five lines. WP's modified text at the protocol boundary is the right level of abstraction for the principle but loses the V observability handle. CPC's split is more granular and more useful for V phase reporting but writes a substantive claim about retry semantics into the constitution that the implementation may not preserve. My withdrawal collapses both into "stochastic at one boundary" but loses the V phase-report content CPC's NR-2 intended to drive.

**What evidence would resolve**: Read `conversus/schemas/construction.py` at the `GapFiller.fill()` site and `InteractiveGapFiller` implementation. If `fill()` is in fact a single call from the orchestrator's perspective and the question-generation/answer-extraction split lives entirely below the protocol boundary, WP's modified text is correct and the V phase report should reference `SourceProvenance.filled_by` counts (which are below `fill()`'s boundary anyway) rather than naming the substeps. If the orchestrator can observe the substeps directly, CPC's split is feasible and the constitution can name them.

**My position**: Defer to WP's modified protocol-level framing for the principle text. CPC's V phase-report content should reference `SourceProvenance.filled_by` rather than the substep names — that re-grounds the observability obligation in the data structure that already records the answer.

### Dispute 3 — Whether the "Origin" footer should hedge that some referenced runtimes (specs 016-019) are partly under construction

**Status**: Open. My Phase 3 Rec 7 surfaced the Principle XII (No Dead Infrastructure) concern: declaring discipline over runtime layers (`conversus/optimizer/`, `nashopt/`, `ampl/`) that do not yet exist potentially codifies sanction for not-yet-built infrastructure. My recommended edit appends to the Origin block: "Some referenced runtime layers (specs 016-019, optimizer/nashopt/ampl) are spec'd but partly under construction; this principle codifies the discipline they will satisfy when implemented." Neither WP nor CPC engaged this directly. WP's revision did not surface XII; CPC's revision treated specs 016-019 as in-scope without flagging the construction status.

**Why it matters**: Without the hedge, a future PR author reading XVI at face value would conclude that the optimizer layer exists and that the principle's stage-3 mechanical-assembly claim has runtime code under it. Spec 014's `construction.py` is the only code that exists today; spec 016+ are aspirational. The Origin footer is the right place to record this — the principle text proper should not dilute its normative force, but the footer is auditable provenance and the natural carrier for the construction-status caveat.

**What evidence would resolve**: A directory listing under `conversus/` showing whether `optimizer/`, `nashopt/`, `ampl/`, or equivalent paths exist, plus a check of which specs in 016-019 have moved to `specs/done/`. If none of the runtime directories exist and none of 016-019 are done, the hedge is required. If the runtime exists and is referenced from `construction.py`, the hedge is not required.

**My position**: Hold. This is a P2 from my revision and neither cross-reviewer rebutted it; their silence is not consent, but the evidence question is concrete and the footer-only edit is low-blast-radius. Synthesis should keep this on the recommendation list.

---

## Convergence

### Convergence 1 — `objective.yml` is the artifact anchor; no runtime cache exists

All three reviewers ground the pinning mechanism to `objective.yml` (spec 014 FR-012) rather than the candidate's "cached values" prose. WP modified Rec 1 to "MUST be persisted to `objective.yml` for the duration of the deliberation run." CPC withdrew Rec 4 on the grounds that the "cache" framing was solving a phantom problem and replaced it with `objective.yml` as the sanctioned, keyed, explicit persistence form. My Rec 2 strengthened on the same evidence, and CPC's NR-2 + WP's modified Rec 6 both fold the X/XI cross-references onto the same artifact. This is the load-bearing convergence — the candidate's cache language is replaced by the artifact name, with MUSTs and cross-principle anchors landing on the same noun.

### Convergence 2 — The VII ↔ XVI carve-out lives in XVI's clarification, not VII's body

All three reviewers agree the carve-out belongs in XVI's clarification block with at most a one-line back-reference parenthetical inserted into VII line 163. WP Rec 3 modified to "full carve-out lives in XVI's clarification, with a single back-reference parenthetical inserted into VII." CPC Rec 1 withdrew its "amend VII" half on Principle XI grounds (writing the same fact in two places violates SSOT). My Rec 9 (refined) accepted the carve-out placement and added the cross-run example ("two `/conversus mode` invocations on the same `problem.md` MAY produce different `objective.yml` files"). This convergence avoids the XI duplication failure and keeps the amendment surface narrow.

### Convergence 3 — Mechanical/deterministic terminology drift is real and warrants a P2 fix

All three reviewers ended up at P2 on the mechanical-vs-deterministic vocabulary mismatch. CPC Rec 8 self-promoted from P3 to P2 on the three-way drift evidence (code: deterministic, spec 014 FR-012: deterministic, constitution v2.3.2: mechanical). WP New Recommendation B framed the same drift at P2. My Rec 3 held at P1 in my Phase 3 revision but acknowledged the cross-reviewers landed at P2. Compromise: P2 is the right priority — it is precision-affecting, not safety-critical. The concrete edit (rename "Mechanical assembly" to "Deterministic assembly" in stage 3, OR add an equivalence note) is uncontested across all three reviewers; only the priority differed and P2 is now the agreed level.

### Convergence 4 — A v2.3.2 Sync Impact Report is a P1 metadata gap

WP New Recommendation A and my New Recommendation 1 independently identified the same defect: the candidate's top-of-file SIR describes v2.3.1 while the version footer is 2.3.2. CPC did not raise this directly, but its Position Summary did not contest it. Both WP and I priority-promoted to P1 because metadata consistency is a one-edit fix that should not block to a follow-up. The v2.3.2 SIR is also the natural place to record the audit result from Dispute 1 (verified or evidence-pending). This is uncontested across all reviewers who engaged the issue.

### Convergence 5 — `SourceProvenance.filled_by` is the auditable hook; V observability lands here

All three reviewers converge on `SourceProvenance.filled_by` (`conversus/schemas/construction.py:262-279`) as the existing data-structure hook for pinning attribution. WP modified Rec 10 to "pinning is auditable via `SourceProvenance.filled_by`." CPC Rec 6 ties V's runtime observability ("phase reporting without `filled_by` underneath is performative; `filled_by` without surfacing is invisible") to the same field. My Rec 6 holds the recommendation with the same anchor. This is a clean three-way agreement: the constitution names the field, V's phase report references it, and the audit hook is concrete rather than aspirational.

---

## Final Position Statement

### Non-Negotiables

**NN-1**: The pinning discipline is grounded in `objective.yml` (spec 014 FR-012), not in a runtime cache. This is uncontested across all three reviewers and is the load-bearing edit. The candidate's lines 463-466 prose ("cached values from the first resolution are reused") MUST be replaced with artifact-anchored MUSTs naming `objective.yml`. Adopting any softer formulation reverts a finding all three Phase 3 revisions endorsed.

**NN-2**: The VII ↔ XVI carve-out lives in XVI's clarification block only. A back-reference parenthetical at VII line 163 is permitted; a duplicate carve-out in VII's body is prohibited (Principle XI). This placement is uncontested across all three reviewers in their Phase 3 dispositions. Synthesis MUST NOT split the carve-out into two locations.

**NN-3**: The audit gate (Dispute 1) is real and unresolved. Synthesis MUST either (a) record an audit result against the actual codebase before merge, or (b) frame the v2.3.2 clarification as "codifies the discipline that spec 014 implements" rather than asserting the discipline as currently in force. Allowing the principle to merge with indicative-mood claims about an unverified runtime discipline is a constitutional drift this review series exists to prevent.

### Flexibility

**F-1**: Rec 7's stage-2 framing is negotiable. WP's protocol-boundary framing (`GapFiller.fill()` is one call) and CPC's substep split (question generation + answer extraction) are both defensible. I would prefer WP's modified protocol-level text with V phase-report observability anchored to `SourceProvenance.filled_by` rather than to substep names — but if synthesis prefers CPC's NR-2 split because V's phase report reads more naturally with named substeps, that is acceptable. The principle does not turn on this disambiguation.

**F-2**: The mechanical-vs-deterministic edit (Convergence 3) accepts either P2 form: (a) rename stage 3 to "Deterministic assembly" or (b) add an equivalence-note sentence. Either resolves the drift. I prefer (a) for cleanliness — the rename eliminates the drift instead of documenting it — but (b) is acceptable if rename ripples too widely through the constitution's surrounding prose.

**F-3**: The "Origin" footer hedge for specs 016-019 construction status (Dispute 3) can be replaced with an equivalent placement in the v2.3.2 SIR's rationale block. Either location records the provenance; the footer is more local but the SIR is more discoverable. Synthesis may pick whichever placement reads cleaner adjacent to the surrounding metadata, as long as the construction-status caveat is recorded somewhere auditable.
