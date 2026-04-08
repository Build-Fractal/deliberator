# Cross-Review of Devil's Advocate — by Integration Architect

**Spec**: `008-interests-mode`
**Reviewing**: `devils-advocate/review.md`
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. Dismissing interests.md as "coupling artifact" contradicts the prerequisite routing architecture

Devil's advocate argues that `interests.md` "duplicates information that ends up in `conversus.yml`" and suggests making it optional or collapsing `interests` and `mode` into a single step (DA review lines 49-57). This directly contradicts the prerequisite routing architecture that both the spec and SKILL.md carefully construct.

The mode handler's three-case prerequisite check (SKILL.md lines 1099-1115) relies on `interests.md` existing as a discrete artifact to route users through the correct workflow sequence. The staleness warning (SKILL.md lines 1117-1122) uses `interests.md` mtime against `conversus.yml` mtime to detect drift. Both mechanisms depend on `interests.md` as a persisted file with its own lifecycle.

More critically, `interests.md` is not a simple pass-through. It contains the user's confirmed interest structure after potentially multiple rounds of add/remove/modify (SKILL.md lines 996-1004). The `Perspective` field that DA dismisses as "human-readable metadata, not machine-consumed input" is actually the field presented in the mode handler's confirmation display (SKILL.md line 1203: "Agents: {count} (from interests.md)" and the report at lines 1286-1288 listing each agent's perspective). It is machine-consumed -- the mode handler reads it to generate the summary.

DA's claim that "interests named after products/tools/approaches" as a secondary heuristic signal "could be extracted at mode-selection time by reading `problem.md` directly" (DA review line 55) is wrong about the data source. The interest naming signal comes from `interests.md` interest headings, not from `problem.md`. The user may have renamed, added, or removed interests during the interactive confirmation flow. The interest structure after user editing is not recoverable from `problem.md`.

Making `interests.md` optional would create a mode handler that must support two code paths -- one with the file, one without -- doubling the prerequisite logic, staleness detection, and existing-file-check complexity. This is an integration architecture regression, not a simplification.

### 2. Recommending winner-take-all for integration problems misapplies mode semantics

DA argues that "some integration problems are zero-sum on specific dimensions, and winner-take-all would surface that reality better" (DA review line 36). This misreads what winner-take-all actually does in the engine.

Winner-take-all's synthesis template produces a `## Runner-Up` heading (SKILL.md line 762) and a single verdict. Its dispute-parsing subsystem looks for `## Runner-Up` as evidence of a contested decision (SKILL.md line 762). The entire mode is structured around selecting one winner and discarding alternatives. For integration problems -- where the spec says "all interests must survive in the outcome" (spec line 66) -- applying winner-take-all would produce a synthesis that declares one team's requirements as the winner and relegates others to runner-up status. That directly violates the integration problem's defining characteristic.

The correct response to integration problems with zero-sum dimensions is cooperative mode with dispute escalation to arbitration (Phase 6), which produces `### Remaining Disputes` entries (SKILL.md line 761) that surface irreconcilable tensions without declaring a winner. DA's recommendation would lead users into a mode that structurally cannot produce the outcome their problem requires.

---

## Tensions

### 1. Confidence label semantics: "Default" vs "High" vs undefined

DA argues the decision matrix confidence should be downgraded from "High" to "Default" (DA recommendation 1). My review accepted the "High" labels as achievable because the implementation traces cleanly from problem type to mode to schema. Both positions have merit, but they are in tension about what "confidence" measures.

DA interprets confidence as empirical accuracy -- how often does this mapping produce better deliberation than alternatives? That is a valid reading, and DA is correct that no empirical evidence is cited.

I interpret confidence as schema determinism -- given a problem type, how unambiguously does the matrix select a mode? For all four non-ambiguous types, the answer is "completely deterministic: one type maps to exactly one mode." The matrix is a function, not a heuristic.

The tension is real. The word "confidence" is doing double duty. DA's proposed fix (rename to "Default") is less informative than the current label. A better resolution: rename the column from "Confidence" to "Determinism" or split into two columns -- "Default/Override" and "Empirical Confidence: untested." This preserves the information that the mapping is deterministic while acknowledging DA's valid point that empirical validation has not been performed.

### 2. Heuristic formalization: how much is enough?

DA argues the heuristic detection is "a suggestion" not a spec (DA review lines 39-47) and contrasts it unfavorably with the Dispute-Parsing Subsystem's exact markers (SKILL.md lines 743-770). My review noted the same gap (my review, missed opportunity 3: "Heuristic detection signals are documented but not structured") but rated it lower severity.

DA is right that the dispute-parsing subsystem is significantly more formal -- it defines exact markers, fallback strategies, ordered parsing rules, and a default behavior. The heuristic detection section has none of these. However, the two systems serve different purposes. Dispute parsing operates on structured machine output (synthesis files with known heading conventions). Heuristic mode detection operates on freeform natural language (problem descriptions written by humans). Demanding the same formalism from both ignores that the input spaces are categorically different.

DA's proposed fix -- "weighted keywords, minimum threshold for 'clear lead,' explicit tie-breaking rules" -- risks false precision. Assigning a weight of 0.3 to "choose between" and 0.2 to "pick one" would look formal but would be equally arbitrary without empirical calibration. DA's alternative proposal -- "demote the heuristics from 'detection' to 'suggestion'" -- is more honest and implementable.

There is real agreement here beneath the tension: both reviews want the spec to be explicit about the advisory nature of mode inference. The disagreement is about remediation granularity, not about the diagnosis.

### 3. Agent-launch cost transparency: when to surface it

DA recommends adding an agent-launch cost estimate to the interests confirmation step (DA recommendation 3). My review does not raise this. DA is correct that the cost implications are significant (N^2 + N + 1 per round, SKILL.md lines 1304-1306), and users should be informed.

The tension is about placement. DA says the estimate belongs at interest confirmation time. But at that point, the mode is not yet selected, and the mode affects the launch formula (red-blue has asymmetric launch counts). The accurate cost can only be calculated after mode selection. The better placement is in the mode handler's confirmation display (SKILL.md lines 1197-1208), where both agent count and mode are known. DA's recommendation targets the right problem but the wrong handler.

### 4. Problem-type vs interest-structure cross-validation

DA identifies a real gap: if a user defines a `selection` problem but creates interests that look like integration interests, the mode command will recommend `winner-take-all` without cross-checking (DA missed opportunity 3). My review does not raise this.

DA is right that this is a gap, but the proposed fix -- "fire heuristic detection when interest structure contradicts the stated problem type" -- creates a new tension. The heuristic detection section (SKILL.md lines 1147-1156) is explicitly scoped to "when the problem type from `problem.md` is ambiguous or missing." Expanding its trigger to include "problem type present but interests contradict it" changes the heuristic from a fallback to a validator, which is a different role. The cleaner fix would be a separate validation step in the mode handler that compares interest naming patterns against the problem type and warns if they diverge, without re-invoking the full heuristic scoring.

---

## Safe Agreements

### 1. The implementation faithfully realizes the spec

Both reviews agree that all thirteen functional requirements (FR-001 through FR-013) have traceable counterparts in SKILL.md. DA explicitly confirms schema compatibility (DA alignment 1), subcommand dispatch integration (DA alignment 2), preset integration (DA alignment 3), agent name validation (DA alignment 4), and user confirmation gates (DA alignment 5). My review provides a line-by-line FR-to-implementation mapping. There is no disagreement on implementation completeness.

### 2. Post-write validation is correct but preset resolution is a gap

DA does not raise preset resolution, but my review's R-1 (validate preset-backed agent roundtrip) and DA's alignment point 3 (preset integration) are compatible. DA confirms the preset integration design is correct; my review notes the post-write validation does not resolve presets to verify existence. These are complementary observations, not conflicts.

### 3. User confirmation gates are correctly placed

Both reviews explicitly verify that SKILL.md lines 1020 and 1210 enforce user confirmation before writing `interests.md` and `conversus.yml` respectively. DA alignment point 5 and my FR-004, FR-012 mappings both confirm this. No disagreement.

### 4. The `problem.md` draft status gap is real

DA recommendation 6 asks what happens when `problem.md` has `status: draft` -- the spec is silent. My review does not raise this directly, but my missed opportunity 2 (no draft/ready status on `interests.md`) is in the same territory. Both reviews identify that the status lifecycle is underspecified across the guided workflow. DA's framing is sharper: the define spec explicitly says downstream commands define whether `draft` is blocking (SKILL.md line 889), but spec 008 never exercises that option. This is an unambiguous gap that both reviews support addressing.

### 5. No feedback loop from run results

DA missed opportunity 1 (no feedback from `/conversus run` results back to the guided workflow) is a legitimate observation. The `prior:` mechanism (SKILL.md lines 75-80) exists but is not surfaced in the guided workflow's "next step" prompts. My review does not raise this, but it is consistent with my observation about the unidirectional nature of the command chain (define -> interests -> mode -> run). This is a design observation, not a spec violation, and both reviews treat it appropriately as a missed opportunity rather than a defect.

### 6. Heuristic detection needs clarification

Both reviews agree the heuristic mode detection (SKILL.md lines 1147-1156, spec lines 63-68) is underspecified relative to other subsystems. DA calls it "a suggestion" dressed as a spec. My missed opportunity 3 calls it "documented but not structured." The diagnosis is the same; only the severity assessment differs. The resolution both reviews point toward -- making the advisory nature explicit and adding at least minimal structure -- is convergent.

---

## Summary

DA's review surfaces three strong challenges (confidence labels, heuristic formalization, draft status gap) and one dangerous recommendation (making `interests.md` optional). The optional-interests proposal would break the prerequisite routing architecture and the staleness detection mechanism. The recommendation to use winner-take-all for integration problems misapplies the mode's synthesis semantics. The remaining challenges are valid and would improve the spec if addressed with the nuances noted above.
