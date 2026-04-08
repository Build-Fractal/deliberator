# APM v2 Revision: Subject Arbitration (Phase 6)

**Agent**: APM (Agent Package Manager)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Revision Type**: Post-cross-review position revision
**Inputs**: spec-kit cross-review of APM, gh-aw cross-review of APM, APM cross-reviews of spec-kit and gh-aw

---

## Disposition of Original Recommendations

### P1-1. Sync SKILL.md trigger evaluation with FR-011 — MODIFIED

**Original**: Update SKILL.md to reference structural HTML markers as primary, heading-based as fallback.

**Cross-review challenge (gh-aw DC-3)**: gh-aw identifies that syncing SKILL.md to FR-011 as currently written would propagate an underspecified definition -- "dispute entry" is undefined for the marker-based path. Updating SKILL.md before defining "dispute entry" bakes ambiguity into the executable skill definition.

**Revised position**: APM accepts gh-aw's sequencing constraint. The correct order is: (1) define "dispute entry" for the marker-based path in FR-011, then (2) sync SKILL.md. However, APM rejects gh-aw's proposed definition ("any non-whitespace content") as too permissive -- stray HTML comments, template artifacts, or non-breaking space entities between the markers would trigger a false-positive dispatch of an expensive LLM arbitration call. The definition should be: any line between the markers that matches the `**Dispute:**` pattern (consistent with the heading-based fallback) or, at minimum, any line beginning with a Markdown bold marker (`**`). This keeps the primary and fallback mechanisms structurally aligned rather than introducing a semantic gap between them.

**Priority**: Remains P1. The two steps (define dispute entry, then sync SKILL.md) are a single logical unit.

---

### P1-2. Add per-file attribution to the template authoring contract — MODIFIED

**Original**: The template authoring contract should include FR-026's per-file attribution requirement.

**Cross-review challenges**: (1) spec-kit (T-2 in spec-kit's cross-review) notes a tension between APM expanding the contract and spec-kit narrowing its scope to cooperative mode. (2) APM's own cross-review of spec-kit (DC-3) identifies that the sequencing of scope-narrowing vs. invariant-expansion matters -- whichever lands first constrains the other.

**Revised position**: APM accepts that the contract should be explicitly scoped to cooperative mode (spec-kit's P2-6) before new invariants are added. Per-file attribution should be added as a cooperative-mode invariant. The revised recommendation is: (1) scope the contract header to cooperative mode, (2) add per-file attribution as a fifth invariant within that scoped contract. This makes the contract more complete within its declared scope rather than implicitly universal.

**Priority**: Remains P1. The scoping is a prerequisite, not a demotion.

---

### P1-3. Define internal structure convention for Binding Decisions entries — WITHDRAWN

**Original**: Specify that each binding decision entry uses consistent sub-headings (`**Dispute:**`, `**Ruling:**`, `**Grounding:**`, etc.) to make future extraction viable.

**Cross-review challenges**: (1) spec-kit (DC-1 in spec-kit's cross-review) identifies that APM's prose-convention approach and spec-kit's normative-FR approach are incompatible remediation strategies. If both are adopted, the spec contains two sources of truth for the same contract. (2) gh-aw (DC-2 in gh-aw's cross-review) identifies that embedding proto-structured output into prose constrains the future structured output design, inverting the spec's deliberate deferral. (3) APM's own cross-review of spec-kit (DC-1) acknowledges the tension but frames it as "one must be primary."

**Reason for withdrawal**: Both cross-reviewers correctly identify that baking structure into the prose template is a premature commitment that conflicts with the spec's intentional deferral of the structured output mechanism. APM's concern (future extraction viability) is real, but the remedy was wrong. The schema fields should be the normative commitment (spec-kit's position), and the prose should remain free-form for v1. Constraining prose structure now would create a de facto schema that either duplicates or conflicts with the eventual normative schema. APM concedes this point.

**Replaced by**: New Recommendation 1 (below).

---

### P2-4. Extend FR-027 idempotency to cover the arbitration directory — SURVIVING

**Original**: Clarify whether re-running Phase 6 cleans the `{output}/arbitration/` directory or only overwrites `resolution.md`.

**Cross-review status**: Neither spec-kit nor gh-aw raised this concern or contested it. No cross-review challenged or endorsed it. It remains a minor gap.

**Disposition**: Surviving, unchanged. Recommended resolution: overwrite `resolution.md` only; leave other files untouched. Priority remains P2.

---

### P2-5. Add forward-compatibility note to the trigger enum — MODIFIED

**Original**: Document the `trigger` field as an extensible enum with unknown values producing validation errors.

**Cross-review challenges**: (1) gh-aw (T-5 in gh-aw's cross-review) identifies that extending the enum before the existing values are fully specified risks compounding underspecification -- the `trigger: always` endorsement path is itself not fully defined. (2) spec-kit's cross-review does not contest but does not endorse.

**Revised position**: APM accepts gh-aw's point that the existing enum values need full specification before extensibility is formalized. The revised recommendation is narrower: add a note that unknown trigger values MUST produce a validation error (preventing typos from silently passing), but defer the extensibility framing until the existing values (`disputes_remain`, `always`) are fully specified -- including the endorsement path under `trigger: always` with zero disputes. The forward-compatibility note becomes a validation-hardening measure rather than an extension-point declaration.

**Priority**: Downgraded from P2 to P3. Validation hardening is useful but not design-critical.

---

### P2-6. Cross-reference Phase 5 synthesis template in the template authoring contract — SURVIVING

**Original**: The template authoring contract should reference the Phase 5 synthesis template or document its output schema so Phase 6 template authors can verify their template consumes correct inputs.

**Cross-review status**: Neither cross-review contested this. gh-aw's T-1 (template authoring scope) is adjacent but does not conflict -- gh-aw's concern is about enforcement of existing invariants, not about cross-referencing upstream templates. Spec-kit's P2-6 (scope the contract to cooperative mode) is complementary, not conflicting.

**Disposition**: Surviving, unchanged. Priority remains P2.

---

### P3-7. Add arbiter prompt sizing guidance to Edge Cases — SURVIVING

**Original**: Note that `arbiter.prompt` should be concise because the grounding document and dispute content provide the substantive input.

**Cross-review status**: Not raised or contested by either cross-reviewer.

**Disposition**: Surviving, unchanged. Priority remains P3.

---

### P3-8. Clarify "binding" in the Key Entities section — MODIFIED

**Original**: Add a sentence clarifying that "binding" refers to deliberation-record finality, not enforcement on downstream actors.

**Cross-review challenges**: (1) gh-aw (T-3 in gh-aw's cross-review) identifies that APM's clarification weakens the authority of `trigger: always` endorsement that gh-aw's recommendation tries to formalize. If "binding does not imply enforcement on downstream actors," the endorsement output's authority is undermined. (2) spec-kit (T-5 in spec-kit's cross-review) considers the term self-evident from context but the clarifying sentence "harmless."

**Revised position**: gh-aw's tension is valid. The clarification as originally worded was too broad -- it would apply to both dispute-resolution output and endorsement output, undermining the endorsement use case where downstream consumers are expected to treat the arbiter's output as authoritative. The revised formulation: "Binding refers to the finality of the deliberation record -- no further conversus phases revisit the decision. The arbiter's output is authoritative within the conversus process; its effect on downstream actors is governed by the consuming system's integration, not by this spec." This preserves the deliberation-finality meaning without disclaiming downstream authority, which is the consuming system's decision.

**Priority**: Remains P3.

---

## Disposition of Off-Base Assumptions

### OB-1. Grounding document stability verification — SURVIVING (deferred)

**Original**: Hash the grounding document at config validation time; warn if it differs at Phase 6 dispatch time.

**Cross-review status**: (1) spec-kit (T-4 in spec-kit's cross-review) treats the stability assumption as a correctly stated precondition the spec is not obligated to enforce. (2) gh-aw (T-2 in gh-aw's cross-review) accepts the stability assumption because CI contexts use immutable workspaces. (3) APM's own cross-reviews acknowledged the environmental difference.

**Revised position**: APM accepts that this is environmental, not spec-level. In CI contexts (gh-aw's model), the assumption holds naturally. In distributed packaging contexts (APM's model), it does not, but the mitigation belongs in the engine implementation, not the spec. APM withdraws the recommendation to add this to the spec but notes it as an implementation consideration for engines operating in non-CI contexts. No spec change required.

---

### OB-2. "Binding" semantics — addressed under P3-8 above.

---

### OB-3. Template authoring contract assumes Phase 5 output format knowledge — addressed under P2-6 above.

---

## New Recommendations

### N-1. Support spec-kit's normative schema FR with a cardinality fix (replaces withdrawn P1-3)

APM withdrew P1-3 (prose structure conventions) because both cross-reviewers correctly identified it as a premature commitment that conflicts with the deferred structured output strategy. However, APM's underlying concern -- future extraction viability -- remains valid. Spec-kit's proposed FR-028 (normative schema fields, deferred mechanism) is the correct approach, but it needs one fix identified in APM's cross-review of spec-kit (DC-2): the `affected_target_file` field must be pluralized to `affected_target_files` (list type) because a single dispute may affect multiple files. Without this fix, the normative schema bakes in a cardinality assumption that will force either duplicate entries or lossy representation.

**Recommendation**: Endorse spec-kit's proposed FR-028 with the pluralization fix. The normative schema fields should be: `dispute_id`, `ruling_type`, `grounding_citation`, `required_changes`, `affected_target_files` (list), `confidence_level`. The production mechanism remains deferred.

**Priority**: P2. The schema is normatively important for future versions but does not affect v1 runtime behavior.

---

### N-2. Add success criteria for post-conversus requirements

Spec-kit's cross-review (DC-3) correctly identifies that APM's review did not flag the absence of success criteria for FR-022 through FR-027. APM acknowledges this as a gap. The existing SC-001 through SC-007 do not cover failure fallback, output validation, docs-citation constraints, or idempotency. For a spec consumed by spec-kit's SDD pipeline, missing SCs are a structural defect. For APM's packaging model, SCs are less load-bearing but still serve as the acceptance bar for any automated verification.

**Recommendation**: Add at minimum four success criteria, as spec-kit's P1-2 specifies: (a) Phase 6 failure produces Phase 5 terminal state with diagnostic warning (FR-022), (b) malformed resolution triggers validation warning (FR-023), (c) `docs` citations never serve as sole basis for binding ruling (FR-024), (d) re-running Phase 6 overwrites previous output (FR-027).

**Priority**: P1. A spec without acceptance criteria for its requirements is incomplete by any consumption model.

---

### N-3. Adopt gh-aw's FR-022/FR-023 disambiguation with a three-tier model

gh-aw's DC-1 (in the cross-review of APM) correctly identifies that APM treated FR-023 as settled without acknowledging the boundary ambiguity with FR-022. APM's own cross-review of gh-aw (DC-1) proposed a three-tier failure model instead of gh-aw's two-tier disambiguation. APM maintains that three tiers are necessary:

1. **Process failure** (FR-022): Agent timeout, crash, or non-termination. No `resolution.md` written. Phase 5 is terminal state.
2. **Structural unintelligibility** (new, assign to FR-022 as a sub-case): Agent completes but output is not parseable prose (e.g., raw YAML dump, refusal message, output in wrong language). No `resolution.md` written. Diagnostic emitted.
3. **Incomplete but parseable prose** (FR-023): Agent completes, output is recognizably prose but fails section-heading validation. File IS written with warning.

gh-aw's two-tier model (process failure vs. content validation) collapses tiers 1 and 2, routing structurally unintelligible output to FR-023, which would preserve garbage as a deliverable. APM's three-tier model prevents this while respecting gh-aw's core insight that the FR-022/FR-023 boundary needs explicit definition.

**Recommendation**: Add a clarifying sentence to FR-022: "Failure includes agent-process failure (timeout, crash) and structurally unintelligible output (output that cannot be parsed as prose). Output-level validation of parseable prose (section headings, structure completeness) is governed by FR-023." This draws the line at parseability rather than at process completion.

**Priority**: P1. The ambiguity is a correctness issue that affects engine implementation.

---

### N-4. Adopt gh-aw's normative FR for draft template filtering

gh-aw's P2-3 recommends adding a normative FR (proposed FR-028 or equivalent) requiring the engine to skip templates with the draft marker and emit a diagnostic. APM endorsed this in its cross-review of gh-aw (DC-2, final paragraph). The Constraints section's MUST language is clear but not captured in any testable FR. Making it a normative FR makes the behavior verifiable.

**Recommendation**: Add an FR (number to be assigned, avoiding collision with spec-kit's proposed FR-028 for the schema): "The engine MUST NOT dispatch templates containing a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker. If a matching template contains this marker, the engine MUST skip it and emit a diagnostic message." This is defense-in-depth behind FR-004's config-level rejection.

**Priority**: P2. The behavior is already implied by the Constraints section; this makes it testable.

---

### N-5. Add content-presence guard scoped to `trigger: disputes_remain`

Spec-kit's P1-3 recommends that structural markers containing only whitespace should cause the trigger to evaluate to `false`. APM's cross-review of spec-kit (DC-4) identified that this guard must be explicitly scoped to `trigger: disputes_remain` and documented as inapplicable to `trigger: always`, which legitimately fires with empty dispute content (the endorsement path per US1-AS3).

**Recommendation**: Add to FR-011: "For `trigger: disputes_remain`, if the structural markers are present but contain only whitespace or no content matching the dispute-entry definition, the trigger evaluates to `false`. For `trigger: always`, the trigger evaluates to `true` regardless of content between the markers." This prevents false-positive dispatch under `disputes_remain` while preserving the endorsement path under `always`.

**Priority**: P2. Prevents a real edge case but does not affect the common path.

---

## Concessions

### C-1. Structured output: APM concedes to spec-kit's normative-FR approach

APM's original position (P1-3) was to embed extractability into prose conventions. Both spec-kit and gh-aw independently identified this as premature commitment that conflicts with the deferred structured output strategy. APM concedes: the schema fields should be normatively committed via an FR (spec-kit's approach), and the prose template should remain free-form for v1. APM's forward-compatibility concern is adequately addressed by normative schema fields without requiring prose-level structural constraints.

### C-2. Success criteria gap: APM concedes to spec-kit's identification

APM's original review did not flag the missing success criteria for FR-022 through FR-027. Spec-kit's cross-review (DC-3) correctly identifies this as a material gap that APM's review understated. APM accepts that a spec without acceptance criteria for its requirements is incomplete regardless of consumption model.

### C-3. Grounding document stability: APM concedes the mechanism does not belong in the spec

APM's original position proposed a hash-based verification mechanism in the spec. Both cross-reviewers' implicit positions (spec-kit: assumption is correctly stated; gh-aw: immutable workspaces make it moot) are environment-specific but collectively demonstrate that the mitigation belongs in engine implementation, not in the spec's normative text.

### C-4. Observation carve-out audit trail: APM partially concedes to spec-kit

APM's original review declared FR-015.5 "faithful to the synthesis" without noting the missing rationale for rejected alternatives. Spec-kit's DC-2 correctly identifies that "adopts a position" is not equivalent to "resolves a dispute" -- resolution requires documented rationale. APM concedes that the audit trail for the observation enforceability resolution is incomplete and endorses spec-kit's P2-5 (add rationale for disputed resolutions to the Conversus Review section).

---

## Position Summary

### What APM now advocates (final positions)

| # | Recommendation | Priority | Status | Origin |
|---|---------------|----------|--------|--------|
| 1 | Define "dispute entry" as `**Dispute:**`-pattern match in FR-011, then sync SKILL.md | P1 | Modified from P1-1 | APM original + gh-aw sequencing constraint |
| 2 | Scope template authoring contract to cooperative mode, then add per-file attribution | P1 | Modified from P1-2 | APM original + spec-kit scoping |
| 3 | Add success criteria for FR-022, FR-023, FR-024, FR-027 | P1 | New (N-2) | Concession to spec-kit |
| 4 | Three-tier FR-022/FR-023 disambiguation (process failure / unintelligible / incomplete prose) | P1 | New (N-3) | APM cross-review of gh-aw + gh-aw DC-1 |
| 5 | Endorse spec-kit's normative schema FR-028 with `affected_target_files` pluralization | P2 | New (N-1), replaces withdrawn P1-3 | Concession to spec-kit + cardinality fix |
| 6 | Normative FR for draft template filtering (engine MUST skip, emit diagnostic) | P2 | New (N-4) | Endorsement of gh-aw P2-3 |
| 7 | Content-presence guard scoped to `trigger: disputes_remain` only | P2 | New (N-5) | Spec-kit P1-3 + APM scoping constraint |
| 8 | Extend FR-027 idempotency to cover arbitration directory | P2 | Surviving (P2-4) | APM original |
| 9 | Cross-reference Phase 5 synthesis template in template authoring contract | P2 | Surviving (P2-6) | APM original |
| 10 | Endorse spec-kit's P2-5: add rationale for disputed resolutions | P2 | New (concession C-4) | Spec-kit |
| 11 | Validation-error on unknown trigger values (narrowed from extensibility framing) | P3 | Modified from P2-5 | APM original, narrowed per gh-aw |
| 12 | Arbiter prompt sizing guidance in Edge Cases | P3 | Surviving (P3-7) | APM original |
| 13 | Clarify "binding" as deliberation-record finality without disclaiming downstream authority | P3 | Modified from P3-8 | APM original + gh-aw tension |

### What APM withdrew

| # | Recommendation | Reason |
|---|---------------|--------|
| W-1 | Internal structure convention for Binding Decisions prose (P1-3) | Both cross-reviewers correctly identified premature commitment conflicting with deferred structured output. Replaced by N-1 (endorse normative schema FR). |
| W-2 | Grounding document hash verification in spec (OB-1) | Environmental concern; belongs in engine implementation, not spec normative text. |

### Key shifts in APM's position

1. **From prose conventions to normative schema**: APM's v2 review tried to solve future extractability through prose-level structure. Cross-reviews demonstrated this conflicts with the deferral strategy. APM now endorses spec-kit's normative-FR approach as the correct commitment level.

2. **From contract expansion to scoped-then-expanded contract**: APM's v2 review added invariants to the template authoring contract without questioning its scope. Spec-kit's cooperative-mode scoping is the right prerequisite before adding invariants.

3. **From two-tier to three-tier failure model**: gh-aw surfaced the FR-022/FR-023 boundary ambiguity that APM's v2 review missed. APM's cross-review of gh-aw identified that gh-aw's two-tier fix was insufficient. The three-tier model (process failure, unintelligible output, incomplete prose) is APM's new position.

4. **From implicit acceptance to explicit endorsement of success criteria**: APM's v2 review treated success criteria coverage as adequate. Spec-kit's cross-review demonstrated it was not. APM now treats missing SCs as a P1 gap.

5. **From spec-level stability verification to implementation-level concern**: The grounding document hash check is valid engineering but does not belong in normative spec text.
