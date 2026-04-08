# Spec-Kit Revised Position: Subject Arbitration (Phase 6) -- v2

**Reviewer**: spec-kit (SDD framework)
**Revision Date**: 2026-03-19
**Inputs**: APM cross-review of spec-kit, gh-aw cross-review of spec-kit, spec-kit cross-reviews of APM and gh-aw

---

## Disposition of Original Recommendations

### P1-1: Update SKILL.md trigger evaluation to match FR-011 (marker-primary, heading-fallback)

**Surviving.**

All three agents agree this is the highest-priority fix. APM's cross-review (SA-1) calls it "the strongest convergence point -- identical problem, identical severity, identical fix." gh-aw's cross-review (T-4) confirms the drift is real and notes that if SKILL.md is used as the runtime prompt, the engine would silently ignore the primary trigger path. The only tension is severity framing: APM characterizes it as "will produce incorrect behavior"; spec-kit maintains it is a consistency fix because the heading-based fallback would still function correctly. This framing difference does not change the recommendation. The fix is identical regardless.

### P1-2: Add success criteria for post-conversus requirements

**Surviving.**

APM's cross-review (T-4) notes the asymmetry: APM does not flag this gap at all. gh-aw's cross-review (DC-3) goes further, identifying it as a dangerous contradiction -- spec-kit treats missing SCs as a P1 correctness gap, gh-aw's silence implies SCs are downstream artifacts that do not affect spec completeness. gh-aw's position is that RFC 2119 language in FRs is self-verifying; spec-kit's position is that explicit SCs are the bridge between spec and test plan.

Spec-kit maintains this recommendation. The argument that MUST/SHOULD/MAY language is inherently testable conflates "testable in principle" with "has a defined acceptance test." FR-022 says Phase 6 failure MUST fall back to Phase 5 with a warning. An SC that says "Given Phase 6 agent timeout, the engine produces Phase 5 output with a diagnostic warning and no resolution.md" is the concrete verification statement that turns the MUST into a test case. Without it, every implementor independently interprets what "testing FR-022" means. The SCs exist to prevent that divergence.

### P1-3: Add content-presence check between trigger evaluation and variable extraction

**Modified.**

Both APM (DC-4) and gh-aw (T-1) identify a real interaction problem with spec-kit's original recommendation. Spec-kit proposed: if markers contain only whitespace, the trigger evaluates to `false`. APM observes this interacts unsafely with `trigger: always`, which legitimately fires with empty dispute content (the subject-endorsement use case, US1-AS3). gh-aw frames the same concern differently: spec-kit wants to prevent Phase 6 from running (change trigger semantics), gh-aw wants Phase 6 to run but emit a warning (preserve trigger semantics, add observability).

APM is right that the whitespace guard must not apply to `trigger: always`. gh-aw is right that a diagnostic warning is more appropriate than blocking for this edge case.

Revised position: The content-presence check applies **only to `trigger: disputes_remain`**. For that trigger mode: if the structural markers are present but contain only whitespace, the trigger evaluates to `false`. For `trigger: always`: the trigger fires regardless of content, but the engine SHOULD log a diagnostic if `{REMAINING_DISPUTES}` extraction produces empty content. This preserves the subject-endorsement path while preventing the degenerate case where `trigger: disputes_remain` fires on empty markers.

gh-aw's positive definition ("any non-whitespace content between the markers constitutes at least one dispute entry") is cleaner than spec-kit's original negative definition. Adopting gh-aw's framing for the `disputes_remain` trigger.

### P2-4: Elevate structured output schema fields to a normative FR

**Modified.**

This is the most contested recommendation. APM's cross-review (DC-1) identifies a direct contradiction: spec-kit wants normative schema fields, APM wants normative prose structure conventions. Both applied simultaneously create "a double-binding where a future implementor must satisfy both the field contract and the prose convention, with no guarantee the two remain aligned." gh-aw's cross-review (DC-1) makes a different argument: premature normative commitment to deferred features is how specs accumulate dead-letter requirements, and the fields should remain non-normative until at least one implementation validates the field model.

Both objections have merit. APM is correct that the prose structure and the output schema must have a single source of truth. gh-aw is correct that normative commitment before implementation experience creates rigidity risk.

Revised position: **Withdraw the normative FR proposal. Instead, adopt a hybrid approach.** Move the schema fields from Implementation Guidance to a dedicated "Deferred: Structured Output" section (adopting gh-aw's organizational recommendation). Within that section, state: "The following fields represent the target schema for structured extraction. They are advisory for v1 and will be evaluated for normative elevation after implementation experience. Future structured extraction SHOULD target these fields but MAY revise their names, types, or cardinality based on implementation findings: `dispute_id`, `ruling_type`, `grounding_citation`, `required_changes`, `affected_target_files` (list), `confidence_level`." Separately, adopt APM's prose convention recommendation (labeled fields like `**Dispute:**`, `**Ruling:**`, `**Grounding:**` inside Binding Decisions entries) as a template instruction in FR-015, not as a normative schema. The prose conventions are the v1 contract; the schema fields are the v2 aspiration. One source of truth per version.

The pluralization of `affected_target_files` survives from the original recommendation -- the multi-file concern is valid regardless of normative status.

### P2-5: Add Conversus Review Rationale for disputed resolutions

**Modified.**

APM's cross-review (T-2) frames this as a factual disagreement: APM considers FR-015.5 "faithfully reconciled" and sees no need for rationale documentation; spec-kit considers rationale a structural requirement of deliberation outputs. gh-aw's cross-review (T-5) is silent on this, implying it is not a concern from the operational perspective. Spec-kit's own cross-review of APM (DC-2) states: "A deliberation process that produces rulings without reasons is procedurally deficient regardless of whether the ruling itself is correct."

Spec-kit maintains that rationale documentation is important but concedes the scope. The original recommendation asked for rationale for all 4 dispute resolutions. Given that APM and gh-aw both consider this low-priority, the revised recommendation narrows to: add rationale **only for the observation carve-out (FR-015.5)**, which is the resolution where the three agents held the most divergent positions. The other three resolutions (structured output: deferred; template placement: markers; low-confidence: informational) are adequately documented by their own Implementation Guidance text. FR-015.5's choice of "structural + labeling" over "structural-only" (APM) and "no formalization" (gh-aw) is the one decision that benefits most from a brief rationale note.

### P2-6: Scope template authoring contract to cooperative mode

**Surviving.**

APM's cross-review (DC-3) identifies a sequencing dependency: if the contract is scoped to cooperative mode first, APM's additions become cooperative-mode-specific, and non-cooperative modes get no contract. If APM's additions land first, the contract grows but remains implicitly universal. This is a valid integration concern but does not invalidate the recommendation.

Spec-kit maintains scoping is correct. The template authoring contract currently lists variables (`{SYNTHESIS_PATH}`, `{REMAINING_DISPUTES}`, etc.) and invariants that are specific to the cooperative Phase 5 output structure. Non-cooperative modes (Prisoner's Dilemma, Red-Blue) produce fundamentally different Phase 5 outputs. Writing the contract as if it is universal is more dangerous than scoping it narrowly, because it creates a false promise that the contract covers modes it does not.

APM's additions (per-file attribution, Phase 5 cross-references) can be adopted within the cooperative-mode scope. The sequencing concern dissolves if both changes are applied simultaneously: scope the contract to cooperative mode AND add APM's invariants within that scope.

### P3-7: Add `{TRIGGER_REASON}` template variable

**Withdrawn.**

On reflection, this is overengineering for v1. The trigger mode (`disputes_remain` or `always`) is already available context. The dispute count can be derived from `{REMAINING_DISPUTES}` content. A dedicated variable adds a template contract obligation without sufficient payoff. gh-aw's cross-review (T-3) reinforces this indirectly: the `trigger: always` + no-disputes path already needs design attention, and adding more template variables increases the surface area that must handle that edge case.

### P3-8: Document the `trigger: always` + empty `{REMAINING_DISPUTES}` interaction

**Modified.**

gh-aw's cross-review (T-3) argues this is a design gap, not just a documentation gap: the template instructions become "vacuous" when no disputes exist, and the spec needs either a separate endorsement format, conditional template logic, or an explicit acknowledgment. Spec-kit's original recommendation treated it as a documentation annotation in the template authoring contract.

gh-aw is right that "document the edge case" is insufficient. But gh-aw's option (a) -- a separate endorsement output format -- adds scope that v1 does not need.

Revised position: Adopt gh-aw's option (c) with a concrete specification. Add to FR-015 or the template authoring contract: "When Phase 6 runs under `trigger: always` and `{REMAINING_DISPUTES}` is empty, the arbiter operates in endorsement mode. The required sections from FR-018 still apply: Process Note reflects the trigger reason, Binding Decisions contains a statement that no disputes require resolution, and Confidence Assessment evaluates the synthesis positions." This makes the endorsement path explicit without adding a new template or output format. It is the minimum viable specification that eliminates ambiguity.

---

## New Recommendations

### N-1: Disambiguate FR-022 and FR-023 failure states (from gh-aw, challenged in spec-kit's cross-review)

Spec-kit's cross-review of gh-aw (DC-1) acknowledged that gh-aw is correct about the disambiguation need. Spec-kit's Alignment 5 stated the distinction was "already present," but the cross-review analysis concluded: "If two careful reviewers disagree on whether a distinction is explicit, implementors will also disagree." gh-aw's P1-1 and APM's framing (FR-022 for process failure, FR-023 for content validation) are both pointing at the same gap.

**Recommendation (P1):** Add a single disambiguating sentence to FR-022: "In FR-022, 'malformed output' refers to agent-process failure (the process did not complete or produced no parseable output). Output-content validation (the process completed but produced structurally incomplete content) is governed by FR-023." This is gh-aw's exact recommendation and spec-kit now endorses it. The design intent was always correct; the language needs one sentence of clarification.

### N-2: Add normative FR for draft template filtering (from gh-aw P2-3)

gh-aw's cross-review (DC-2) and spec-kit's own cross-review of gh-aw (Tension 4) both identify that the Constraints section MUST for draft template filtering has no corresponding testable FR. gh-aw proposed FR-028 with a specific error message. Spec-kit endorsed the marker mechanism in Alignment 4 but did not flag the absence of an FR as a gap.

gh-aw is right. A MUST in the Constraints section without a testable FR is a spec structure defect. FR-004 is the primary gate (config-time validation), but the runtime marker check is defense-in-depth that needs its own requirement.

**Recommendation (P2):** Adopt gh-aw's FR-028 proposal: "The engine MUST NOT dispatch templates containing a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker. If a matching template contains this marker, the engine MUST skip it and emit a diagnostic message." Additionally, adopt gh-aw's P3-7: document the relationship between FR-004 (config-time gate) and FR-028 (dispatch-time gate) as layered defense. This resolves the architectural disagreement about markers vs. directories pragmatically: the marker mechanism is specified with enough rigor that content-aware filtering becomes a testable requirement, not an advisory comment.

Spec-kit acknowledges gh-aw's ongoing concern that content-based filtering is architecturally novel for the conversus engine. The FR makes it testable; whether the implementation uses content inspection or directory separation to satisfy the FR is an implementation choice.

### N-3: Add per-file attribution to the template authoring contract (from APM P1-2)

APM's cross-review (DC-2) and APM's review (Missed Opportunity 3) identify that FR-026 requires per-file attribution in binding decisions, but the template authoring contract's invariant list does not include it. A template author could write a contract-compliant template that violates FR-026.

**Recommendation (P1):** Add to the template authoring contract invariants: "When multiple target files exist, binding decisions must specify which file each required change applies to (per FR-026)." This is APM's exact recommendation, adopted without modification.

### N-4: Adopt APM's prose structure convention for Binding Decisions (from APM P1-3)

APM's review (Missed Opportunity 2, P1-3) recommends defining internal structure for Binding Decisions entries: labeled fields like `**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Required Changes:**`. This makes the deferred structured extraction viable without requiring agent-produced YAML. Per the revised P2-4 above, this prose convention becomes the v1 contract while the schema fields remain advisory for v2.

**Recommendation (P2):** Add to FR-015 or FR-018 a template instruction specifying that each binding decision entry SHOULD use labeled sub-fields: `**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Rejected Positions:**`, `**Required Changes:**`. SHOULD (not MUST) because the arbiter is an AI agent that may vary in formatting, and FR-023 already handles structural non-conformance with warnings. The convention makes extraction feasible; the SHOULD allows graceful degradation.

---

## Position Summary

Spec-kit's revised v2 position retains 4 of 8 original recommendations (2 surviving, 2 modified), withdraws 1, and modifies 3 others. Four new recommendations are added from cross-review findings. The most significant shifts:

1. **Structured output schema** (P2-4): The normative FR proposal is withdrawn. gh-aw's argument against premature normative commitment and APM's argument about dual-binding risk are both persuasive. The revised approach separates the v1 contract (prose conventions in the template, per APM) from the v2 aspiration (advisory schema fields in a dedicated section, per gh-aw's organizational recommendation). This is spec-kit's largest concession.

2. **Content-presence check** (P1-3): Scoped to `trigger: disputes_remain` only. The `trigger: always` endorsement path is preserved with a diagnostic warning. gh-aw's positive "dispute entry" definition adopted over spec-kit's negative formulation.

3. **FR-022/FR-023 disambiguation** (N-1): Spec-kit reverses its Alignment 5 position. The cross-review evidence -- two careful reviewers reading the same text and reaching opposite conclusions about its clarity -- is dispositive. One disambiguating sentence is warranted.

4. **Rationale documentation** (P2-5): Narrowed from all 4 dispute resolutions to only the observation carve-out, where the three-way position divergence was greatest.

5. **`trigger: always` endorsement** (P3-8): Elevated from documentation annotation to explicit specification of endorsement-mode behavior in FR-015, adopting gh-aw's framing that this is a design gap.

The core thesis remains: arbitration output must be traceable, grounding must be singular, success criteria must cover all requirements, and implementation guidance must track normative spec text. The revisions make the position more pragmatic on schema normativity (defer until implementation experience) while holding firm on structural completeness (SCs, SKILL.md sync, template contract scoping, draft template filtering).
