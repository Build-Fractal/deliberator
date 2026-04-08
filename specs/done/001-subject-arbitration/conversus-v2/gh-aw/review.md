# gh-aw v2 Review: Subject Arbitration (Phase 6)

**Reviewer**: gh-aw (GitHub Agentic Workflows)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Review Round**: v2 (post-synthesis integration review)
**Perspective**: CI dispatch, workflow automation, multi-phase orchestration, agent safety, output validation

---

## Executive Summary

The spec has integrated 17 changes from the conversus synthesis with high fidelity. Of gh-aw's 10 original recommendations, 5 surviving positions and 2 new positions were addressed. The areas where gh-aw pushed hardest -- failure semantics (FR-022), trigger hardening via structural markers (FR-011), output validation (FR-023), idempotency (FR-027), and grounding document guidance (Implementation Guidance section) -- are now normative requirements in the spec. The template authoring contract (FR-014/FR-015 + Implementation Guidance) is a direct adoption of gh-aw's N-1 recommendation. The quorum trigger is deferred exactly as proposed.

The spec is materially stronger than the pre-synthesis version. However, the four remaining disputes from the synthesis -- structured output mechanism, template file placement, observation enforceability, and low-confidence behavior -- were resolved by compromise rather than full adoption of any single position. The compromises are reasonable for v1 but leave specific integration gaps visible from gh-aw's operational perspective.

Three new concerns emerge in this review: (1) the relationship between FR-023 output validation and FR-022 failure semantics creates an ambiguous state for structurally-valid-but-semantically-malformed output, (2) the `{REMAINING_DISPUTES}` variable (FR-014) creates a tight coupling between Phase 5 marker placement and Phase 6 template correctness that has no validation step, and (3) the non-cooperative template status marker (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`) in the Constraints section is underspecified -- there is no requirement for the engine to parse it, making it advisory rather than enforceable.

---

## Alignment

### 1. Failure semantics are correctly specified (FR-022)

FR-022 captures the exact semantics gh-aw recommended in P1-1: Phase 6 failure falls back to Phase 5 as the terminal state, a diagnostic warning is emitted, no partial `resolution.md` is written, and the Phase 1-5 record is not invalidated. This was the cleanest consensus point in the synthesis and the spec reflects it precisely. The language "malformed output" is included alongside timeout and crash, covering the failure modes gh-aw identified.

### 2. Structural HTML markers are the primary trigger mechanism (FR-011)

FR-011 now specifies `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` as the primary trigger evaluation mechanism with heading-based parsing as a backward-compatible fallback. This directly implements gh-aw's revised P1-2 position and resolves the fragile heading-parsing concern from the v1 review. The dual-mechanism approach (structured primary, heading fallback) mirrors gh-aw's own pattern of compile-time validation with runtime fallbacks.

### 3. Output validation is a normative requirement (FR-023)

FR-023 requires the engine to validate that `resolution.md` contains the required section headings from FR-018 after Phase 6 completes. Warnings are emitted for malformed output, but the file is still written. This matches gh-aw's P1-3 recommendation: heading-presence check, informational rather than blocking. The decision not to silently accept malformed output while still preserving the file is the correct balance between safety and data preservation.

### 4. Idempotency semantics are explicit (FR-027)

FR-027 specifies that re-running Phase 6 overwrites any existing `resolution.md` and does not preserve previous output. This resolves gh-aw's P3-9 recommendation. The guidance to commit to version control before re-running is pragmatic and avoids adding complexity to the engine. The overwrite-not-archive approach is cleaner than timestamp-based renaming.

### 5. Template authoring contract is documented (Implementation Guidance)

The "Template Authoring Contract" section under Implementation Guidance captures the Phase 5-to-Phase 6 data flow: which variables are consumed, what invariants template authors must preserve, and how the engine validates output. This is a direct adoption of gh-aw's N-1 recommendation and provides the contract surface that was missing from the v1 spec. The four invariants (read grounding first, output to `{OUTPUT_PATH}`, no contradiction of FR-015, engine validates against FR-018) are the right set.

### 6. Grounding document guidance exists (Implementation Guidance)

The "Grounding Document Requirements" section addresses gh-aw's P3-8 recommendation with minimum content expectations, recommended structure (numbered principles), and anti-patterns. The guidance is non-normative, which is correct -- grounding document quality is a user concern, not an engine enforcement concern.

---

## Missed Opportunities

### 1. No engine-level enforcement for the draft template marker

The Constraints section states that non-cooperative mode templates "MAY exist in `templates/{mode}/arbitration.md` with a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker but MUST be filtered out by the engine at runtime." The MUST is clear, but the spec does not define HOW the engine filters. There is no FR requiring the engine to parse this marker, no validation requirement for its presence in non-cooperative templates, and no error message specified when a non-cooperative template is discovered without the marker. Compare this to FR-004, which specifies a clear error message for `arbiter` on non-cooperative modes. The draft marker needs equivalent specificity or it becomes advisory text that implementors may interpret inconsistently.

### 2. No validation of `{REMAINING_DISPUTES}` extraction correctness

FR-014 defines `{REMAINING_DISPUTES}` as content extracted from between the structural markers in Phase 5 output. FR-011 uses the same markers for trigger evaluation. But there is no requirement to validate that the extraction produced non-empty content when the trigger evaluated to `true`. A scenario: Phase 5 output contains the markers but with only whitespace between them. FR-011's trigger evaluates to `false` (no dispute entries), so Phase 6 does not run -- correct. But if `trigger: always` is set, Phase 6 runs with an empty `{REMAINING_DISPUTES}` variable. The template tells the arbiter to resolve disputes in that variable, but there are none. The spec does not address this edge case. The arbiter would produce a "subject endorsement" per User Story 1, Scenario 3, but the endorsement template path and the dispute-resolution template path appear to use the same template, creating ambiguity about what the arbiter should produce when `{REMAINING_DISPUTES}` is empty under `trigger: always`.

### 3. FR-023 and FR-022 create an ambiguous state for semantically-malformed output

FR-022 specifies that malformed output triggers the failure path (no `resolution.md` written, fall back to Phase 5). FR-023 specifies that the engine validates section headings and emits a warning if validation fails, but the file is still written. These two requirements appear to conflict: FR-022 says malformed output means no file; FR-023 says failed validation means file is written with a warning. The resolution is likely that FR-022 covers agent-level failure (the agent process itself fails) while FR-023 covers output-level validation (the agent succeeded but produced incomplete prose), but this distinction is not explicit in the spec. An implementor could reasonably interpret "malformed output" in FR-022 to include outputs that fail FR-023 validation.

### 4. No specification of what "at least one dispute entry exists" means for trigger evaluation

FR-011 states the engine checks "whether at least one dispute entry exists" between the structural markers. But "dispute entry" is not defined. Is it any non-whitespace content? A line starting with `**Dispute:`? A heading at any level? The heading-based fallback specifies `**Dispute:` entries, but the primary marker-based mechanism has no such definition. This leaves the trigger evaluation underspecified for the primary mechanism while being well-specified for the fallback.

### 5. The `docs` citation boundary (FR-024) is sound but may be operationally confusing

FR-024 correctly constrains `docs` to factual context and prohibits it as the sole basis for a ruling. This resolves the citation-scope debate cleanly. However, the distinction between "citing docs for factual context" and "citing docs as the basis for a ruling" is a semantic judgment that neither the engine nor the output validator can enforce. The template instruction must carry this weight, and there is no requirement in the spec for the template to explicitly instruct the arbiter on this distinction. FR-015 item 1 says "Read the grounding document first" but does not say "Only cite the grounding document as authority; cite docs only for context."

---

## Off-Base Assumptions

### 1. The draft template marker resolves the template/constraint mismatch

The Constraints section's compromise -- templates MAY exist in `templates/{mode}/` with a draft marker and the engine MUST filter them at runtime -- appears to resolve the three-way dispute (spec-kit: in-place with markers; APM: in-place with frontmatter; gh-aw: relocate to `_draft/`). But runtime filtering of templates by content inspection is a pattern that gh-aw's compilation model explicitly avoids. In gh-aw, a file's discoverability is determined by its location, not its content. A file at `templates/prisoners-dilemma/arbitration.md` will be discovered by `templates/*/arbitration.md` globs regardless of what HTML comments it contains. The compromise adopted spec-kit's position (in-place with markers) and relies on implementors building content-aware template filtering, which is a new engine capability not required by any other part of the conversus framework. gh-aw maintains that directory-based separation (`templates/_draft/`) is simpler, more reliable, and consistent with how template discovery works everywhere else in the system. This is not a blocking concern for v1 since FR-004 prevents activation regardless, but the marker-based approach creates technical debt.

### 2. The "subject endorsement" path under `trigger: always` with no disputes is well-defined

User Story 1, Scenario 3 states the arbiter "produces a subject endorsement document confirming the synthesis positions" when no disputes remain under `trigger: always`. But there is no template for this path. The arbitration template (FR-013, FR-015) is designed for dispute resolution: it instructs the arbiter to read disputes, issue rulings, cite the grounding document. When `{REMAINING_DISPUTES}` is empty and `{ALL_DISPUTES}` contains no unresolved items, the template instructions become vacuous -- the arbiter is told to resolve disputes that do not exist. The spec should either (a) define a separate endorsement output format under FR-018, (b) add template conditional logic for the no-disputes path, or (c) acknowledge that the endorsement is the arbiter's interpretation of the dispute-resolution template when given no disputes. Currently this is an implicit behavior, not a specified one.

---

## Actionable Recommendations

### P1 -- Required for Correctness

**1. Disambiguate FR-022 and FR-023 failure states.**

FR-022 covers agent-process failure (timeout, crash) and should specify that no `resolution.md` is written. FR-023 covers output-content validation (agent succeeded but output is structurally incomplete) and should specify that the file IS written with a warning. Add a single sentence to FR-022 clarifying that "malformed output" in FR-022 refers to agent-level failure (the process did not complete), not output-level validation (the process completed but produced incomplete content). Output-level validation is governed exclusively by FR-023.

**2. Define "dispute entry" for the primary trigger mechanism in FR-011.**

The marker-based trigger evaluation checks "whether at least one dispute entry exists" between `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->`. Specify what constitutes a dispute entry for the primary mechanism. Recommendation: any non-whitespace content between the markers constitutes at least one dispute entry. This is simple, unambiguous, and avoids coupling the trigger to specific formatting conventions that may evolve.

### P2 -- Required for Design Integrity

**3. Add a normative FR for draft template filtering.**

The Constraints section states the engine "MUST" filter draft templates at runtime, but this behavior is not captured in any FR. Add FR-028 (or equivalent): "The engine MUST NOT dispatch templates containing a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker. If a template matching `templates/{mode}/arbitration.md` contains this marker, the engine MUST skip it and emit a diagnostic message: 'Template for {mode} arbitration is draft and cannot be activated.'" This makes the filtering behavior testable and gives implementors an unambiguous requirement.

**4. Add explicit template instruction for the `docs` vs. `grounding` citation boundary.**

FR-024 defines the boundary but FR-015 does not instruct the arbiter to observe it. Add to FR-015 a seventh instruction: "Cite the grounding document as authority for rulings; cite docs entries only for factual context, never as the sole basis for a binding decision." This ensures the template carries the enforcement weight that FR-024 requires.

**5. Address the `trigger: always` + no disputes endorsement path.**

Add a sentence to FR-015 or FR-018 specifying the expected output when Phase 6 runs under `trigger: always` but no disputes remain. Either: (a) FR-018's required sections still apply, but the Binding Decisions section contains a "No disputes to resolve" statement and the arbiter produces a Confidence Assessment of the synthesis positions, or (b) the template includes conditional instructions for the endorsement case. The current spec leaves this to implicit interpretation.

### P3 -- Recommended Improvement

**6. Add validation for `{REMAINING_DISPUTES}` extraction.**

After extracting content between the structural markers for the `{REMAINING_DISPUTES}` variable, the engine should log a diagnostic if the extraction is empty when the trigger evaluated to `true` (possible indicator of marker placement error or extraction failure). This does not need to be blocking -- a warning is sufficient. This prevents silent data-flow errors between Phase 5 output and Phase 6 input.

**7. Specify the relationship between the draft template marker and FR-004.**

FR-004 rejects `arbiter` on non-cooperative modes at config validation time. The draft template marker operates at template dispatch time. Clarify that FR-004 is the primary gate (validation rejects the config before any template is loaded) and the draft marker is a defense-in-depth mechanism for cases where a future mode might be added to the cooperative-mode enum without templates being updated. This layered defense model is consistent with gh-aw's own approach of pre-activation validation plus runtime checks.

**8. Consider extracting the structured output schema definition from Implementation Guidance to a standalone section.**

The "Structured Output Schema (Deferred)" subsection under Implementation Guidance defines fields (`dispute_id`, `ruling_type`, `grounding_citation`, etc.) that are referenced as "deferred to a future version." Because this schema will inform future FRs, it warrants a standalone "Future Work" or "Deferred" section rather than being nested under implementation guidance. This is a documentation organization concern, not a correctness concern, but it would make the deferred scope more visible in the spec's table of contents.

---

## Referenced Documentation

| Document | Relevance |
|----------|-----------|
| `gh-aw/docs/src/content/docs/reference/compilation-process.md` | Template discovery via directory structure (Phases 1-5) -- informs the template marker vs. directory-placement debate |
| `gh-aw/docs/src/content/docs/reference/threat-detection.md` | Post-agent output validation pipeline -- analogy to FR-023 output validation and the FR-022/FR-023 disambiguation |
| `gh-aw/docs/src/content/docs/reference/staged-mode.md` | Preview-before-commit pattern -- context for gh-aw's withdrawn dry-run recommendation and why the `trigger: always` endorsement path needs specification |
| `gh-aw/docs/src/content/docs/reference/safe-outputs-pull-requests.md` | Protected files policy with explicit error messages for each state -- model for how the draft template marker should have equivalent specificity |
| `gh-aw/docs/src/content/docs/reference/templating.md` | Variable substitution and conditional templating -- informs the `{REMAINING_DISPUTES}` extraction validation concern |
| `gh-aw/docs/src/content/docs/guides/deterministic-agentic-patterns.md` | Multi-phase pipeline with data handoff between jobs -- analogy to Phase 5-to-Phase 6 data flow and the template authoring contract |
| `gh-aw/docs/src/content/docs/patterns/spec-ops.md` | W3C-style specification maintenance with RFC 2119 keywords -- informs the normative language expectations (MUST/SHOULD/MAY) used throughout the spec |
| `gh-aw/docs/src/content/docs/patterns/orchestration.md` | Orchestrator/worker pattern -- Phase 6 as a conditional worker dispatched after Phase 5 synthesis completes |
| `gh-aw/README.md` | Guardrails and safety as foundational principles -- context for gh-aw's consistent focus on failure semantics, validation, and defense-in-depth |
