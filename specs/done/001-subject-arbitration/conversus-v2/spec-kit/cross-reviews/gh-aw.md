# Spec-Kit Cross-Review of gh-aw's v2 Review

**Cross-reviewer**: spec-kit
**Target review**: gh-aw v2 review (`conversus-v2/gh-aw/review.md`)
**Date**: 2026-03-19

---

## Dangerous Contradictions

### 1. FR-022 vs FR-023 disambiguation: gh-aw sees a spec defect, spec-kit sees correct design

gh-aw's Missed Opportunity 3 and P1-1 identify an "ambiguous state" between FR-022 (failure semantics: no file written) and FR-023 (output validation: file written with warning), arguing the spec conflates agent-level failure with output-level validation and requires an explicit disambiguating sentence. Spec-kit's Alignment 5 reads the same two requirements and concludes the opposite: "correctly distinguishes catastrophic failure from structural non-conformance -- a nuance the synthesis implied but did not explicitly separate." Spec-kit treats the distinction as already present in the spec text; gh-aw treats it as absent.

**Why this is dangerous**: If an implementor follows spec-kit's reading, they build two separate code paths (FR-022 for process failure, FR-023 for content validation) without adding clarifying language. If a second implementor follows gh-aw's reading, they add a disambiguating sentence that changes the meaning of "malformed output" in FR-022 to exclude content-level issues. The two implementations would disagree on what happens when the agent process succeeds but produces output with zero recognizable section headings -- is that FR-022 "malformed output" (no file written) or FR-023 "failed validation" (file written with warning)? The boundary case is an agent that returns an HTTP 200 with garbage prose. gh-aw is correct that the spec needs one sentence to close this gap, even if spec-kit is correct that the design intent is already sound. Intent without explicit language is not a spec.

### 2. Template placement: in-place markers vs. directory separation

gh-aw's Off-Base Assumption 1 directly challenges the Constraints section's adopted compromise (spec-kit's position: non-cooperative templates live at `templates/{mode}/arbitration.md` with a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker, filtered at runtime by content inspection). gh-aw argues this creates technical debt because template discovery everywhere else in the system is location-based, not content-based, and that `templates/_draft/` directory separation is simpler and more reliable. Spec-kit's Alignment 4 endorses the marker approach as correctly resolving the dispute, noting it "preserves the naming convention and makes future activation a config change rather than a file move."

**Why this is dangerous**: This is not a theoretical disagreement -- it determines how every template-consuming tool in the ecosystem discovers and filters templates. If the marker approach ships, every tool that globs `templates/*/arbitration.md` must add content-inspection logic or risk dispatching draft templates. gh-aw's concern is that no other part of the conversus framework requires content-aware template filtering, making this a novel capability that must be built, tested, and maintained for a single use case. Spec-kit's counter -- that file moves are operationally heavier than marker flips -- is valid for authors but irrelevant for engines. The spec adopted spec-kit's position but gh-aw's operational concern remains unaddressed: there is no FR requiring the engine to parse the marker, only a Constraints section MUST with no corresponding testable requirement. gh-aw's P2-3 (add FR-028 for draft template filtering) would close this gap regardless of which placement strategy wins.

### 3. Structured output schema: normative commitment vs. organizational relocation

Spec-kit's Missed Opportunity 1 and P2-4 argue the structured output schema fields must be elevated from non-normative Implementation Guidance to a normative FR (proposed FR-028), making the schema a binding commitment that constrains future design. gh-aw's P3-8 argues the schema section should be extracted from Implementation Guidance to a standalone "Future Work" or "Deferred" section -- an organizational change, not a normative elevation. gh-aw explicitly frames this as "a documentation organization concern, not a correctness concern."

**Why this is dangerous**: These two recommendations, if both adopted, could produce a contradictory outcome. Spec-kit wants the fields to carry RFC 2119 MUST weight so that any future structured extraction implementation is constrained to support `dispute_id`, `ruling_type`, `grounding_citation`, `required_changes`, `affected_target_files`, and `confidence_level`. gh-aw wants the fields moved to a "Deferred" section that by convention is non-normative. If an editor follows gh-aw's recommendation (relocate to Future Work) without also following spec-kit's (elevate to FR), the schema loses even its current advisory status and becomes a wish list. If both are followed, the schema appears as both a normative FR and a deferred future-work item, creating a semantic contradiction. The recommendations must be reconciled: either the fields are normative (spec-kit's position, which gh-aw does not oppose but also does not advocate) or they are organizational (gh-aw's position, which spec-kit explicitly considers insufficient). This cannot be resolved by applying both independently.

---

## Tensions

### 1. "Dispute entry" definition: any non-whitespace vs. unspecified

Both reviews identify the same gap: FR-011's primary marker-based trigger evaluates "whether at least one dispute entry exists" without defining what a "dispute entry" is (gh-aw Missed Opportunity 4, spec-kit Missed Opportunity 2 via the empty-content variant). gh-aw's P1-2 recommends defining it as "any non-whitespace content between the markers." Spec-kit's P1-3 recommends a whitespace check but frames it as "if the structural markers are present but contain only whitespace, the trigger evaluates to `false`." The functional outcome is identical, but the specification approach differs: gh-aw defines what a dispute entry IS (positive definition), spec-kit defines when the trigger does NOT fire (negative definition). A positive definition is more extensible -- it can later be tightened to require specific formatting. A negative definition is more conservative -- it only excludes the degenerate case. The tension is minor but affects how future versions can evolve the trigger without breaking backward compatibility.

### 2. `{REMAINING_DISPUTES}` extraction validation: warning vs. trigger-gate

Both reviews flag the decoupling between trigger evaluation (FR-011) and variable extraction (FR-014) as a gap (gh-aw Missed Opportunity 2 and P3-6, spec-kit Missed Opportunity 2 and P1-3). The tension is in the remedy. gh-aw recommends a diagnostic warning when extraction is empty but the trigger evaluated to true -- non-blocking, informational (P3-6). Spec-kit recommends a harder gate: if markers contain only whitespace, the trigger evaluates to false, preventing Phase 6 from running at all (P1-3). gh-aw's approach preserves `trigger: always` semantics and treats the edge case as a data-flow diagnostic. Spec-kit's approach prevents the edge case entirely but does so by changing trigger semantics -- a trigger that would have fired under the current spec now does not. The question is whether empty-markers-with-trigger-true is an error to warn about (gh-aw) or a condition to prevent (spec-kit). Both are defensible; they produce different runtime behavior.

### 3. `trigger: always` + no disputes: endorsement path specification

Both reviews identify the `trigger: always` with zero remaining disputes scenario as underspecified (gh-aw Off-Base Assumption 2 and P2-5, spec-kit P3-8). The tension is in the prescribed remedy. gh-aw offers three concrete options: (a) define a separate endorsement output format under FR-018, (b) add template conditional logic, or (c) explicitly acknowledge the behavior is implicit. Spec-kit recommends documenting the interaction in the template authoring contract without proposing a new FR or output format. gh-aw's framing treats this as a design gap requiring a spec change; spec-kit treats it as a documentation gap requiring a contract annotation. The practical impact: gh-aw's option (a) would add a new required section structure for endorsements; spec-kit's approach leaves the existing FR-018 sections unchanged and puts the burden on template authors to handle the empty case. For v1, spec-kit's lighter approach is probably sufficient, but gh-aw is correct that the endorsement path will eventually need its own output specification.

### 4. Draft template marker: FR-level requirement vs. defense-in-depth framing

gh-aw makes two recommendations about the draft template marker: P2-3 (add a normative FR for filtering behavior with a specific error message) and P3-7 (clarify the marker as defense-in-depth behind FR-004's config-validation gate). Spec-kit endorses the marker mechanism in Alignment 4 but does not flag the absence of a corresponding FR as a gap. The tension: gh-aw sees the Constraints-section MUST as insufficient without a testable FR; spec-kit sees the Constraints section as sufficient because FR-004 is the primary gate. gh-aw's layered defense model (FR-004 at config time, FR-028 at dispatch time) is architecturally sounder than relying on a single gate, but spec-kit's implicit position -- that the Constraints section language is binding -- is also defensible under RFC 2119 conventions where MUST in any normative section carries requirement weight. The gap is not whether the behavior is required (both agree it is) but whether it is testable without a dedicated FR (gh-aw says no, spec-kit is silent).

### 5. Success criteria coverage

Spec-kit's Missed Opportunity 5 and P1-2 explicitly flag that SC-001 through SC-007 do not cover the post-conversus requirements (FR-022 through FR-027) and recommends adding new SC entries. gh-aw does not mention success criteria at all. This is not a disagreement -- gh-aw's review simply does not examine success criteria -- but it creates a tension in prioritization. Spec-kit classifies this as P1 (Required for Correctness); gh-aw's silence implies it is not a concern from the CI/orchestration perspective. The tension matters because success criteria drive acceptance testing: if gh-aw's implementors do not consider SC coverage a gap, they may ship an implementation that passes the existing SC-001 through SC-007 but does not verify the new requirements.

---

## Safe Agreements

### 1. Failure semantics (FR-022) are correctly specified

Both reviews endorse FR-022 without reservation. gh-aw Alignment 1: "captures the exact semantics gh-aw recommended." Spec-kit Alignment 5: "covers agent failure (timeout, crash, malformed output), preserves Phase 5 as the terminal state." Both agree that the Phase 5 fallback, diagnostic warning, no-partial-output, and record-preservation properties are correct. This was the cleanest consensus point in v1 and remains so in v2.

### 2. Structural HTML markers are the correct primary trigger mechanism (FR-011)

Both reviews endorse the marker-primary, heading-fallback trigger hierarchy. gh-aw Alignment 2: "directly implements gh-aw's revised P1-2 position." Spec-kit Alignment 2: "implements the exact hierarchy the synthesis prescribed." Both reviews also agree the mechanism has a gap in "dispute entry" definition (see Tension 1), but neither disputes the architectural decision to use structural markers as the primary evaluation mechanism.

### 3. The docs-vs-grounding citation boundary (FR-024) is well-calibrated

Both reviews endorse FR-024's formulation. gh-aw Alignment (implied in the executive summary) and Missed Opportunity 5 accept the boundary but note the enforcement gap in template instructions. Spec-kit Alignment 3: "the exact formalization spec-kit requested" with the "sole basis" qualifier as "a pragmatic addition." Both agree the requirement is correct; gh-aw additionally wants FR-015 to carry the enforcement instruction (P2-4), which spec-kit does not oppose. There is no disagreement on the substance of FR-024 itself.

---

## Summary

The two reviews are broadly aligned on what the spec gets right (failure semantics, trigger markers, citation boundaries) and broadly aligned on what gaps remain (dispute entry definition, extraction validation, endorsement path, draft marker enforceability). The dangerous contradictions are concentrated in three areas where the reviews reach opposite conclusions about the same spec text: whether FR-022/FR-023 disambiguation is already present or absent, whether marker-based or directory-based template placement is the correct long-term approach, and whether the structured output schema needs normative elevation or organizational relocation. These three items require explicit resolution before implementation -- adopting both reviews' recommendations without reconciliation would produce contradictory requirements.
