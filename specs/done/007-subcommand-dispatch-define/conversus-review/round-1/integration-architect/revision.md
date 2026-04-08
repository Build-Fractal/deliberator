# Integration Architect — Revised Review (Iteration 1)

## Recommendation Dispositions

### Recommendation 1: Post-write schema validation for problem.md (was P1)

**Status**: MODIFIED — retain P1, but expand scope to dual-layer validation.

My original recommendation was to add a post-write heading validation step in the define handler, mirroring the engine's Phase 6 output validation (SKILL.md L659-676). Both cross-reviews agreed this is the single most important gap in the spec. However, devil's advocate correctly identified that producer-side validation alone creates false confidence: the file is validated at the moment it is least likely to be wrong (immediately after agent generation) and never validated again after the user manually edits it to resolve `[CLARIFY:]` tags.

Devil's advocate proposes consumer-side validation instead. I argued in my cross-review of devil's advocate that distributing validation across specs 008, 009, and 010 is an integration nightmare. I still hold that position. However, devil's advocate's underlying concern -- that post-write mutation breaks producer-only validation -- is legitimate.

**Revised recommendation**: Producer-side heading validation remains P1 for this spec. The define handler MUST verify all 7 required headings exist after writing `problem.md`. Additionally, the spec should define a `problem.md` validation function (even if only as a prose contract) that downstream consumers can reference rather than each reimplementing. This keeps validation logic centralized at the schema level while allowing both producer and consumer checkpoints. The engine precedent supports producer-side as the primary checkpoint (SKILL.md L286-295 validates templates before agents launch; L659 validates after the arbiter writes), and I maintain that producer-side is structurally prior.

### Recommendation 2: Specify refine semantics for existing problem.md (was P1)

**Status**: MODIFIED — retain P1, but reduce prescriptiveness.

Devil's advocate's cross-review landed a strong hit: my proposed merge rules (replace Decision, merge Constraints with deduplication, remove resolved Open Questions, re-evaluate Type, union Source Documents, rewrite Context) present heuristic operations as if they were deterministic algorithms. Natural-language deduplication of constraints is not a well-defined operation. "Remove resolved open questions" requires judgment that will vary across agent invocations. I was prescribing false precision.

Functional-typing's cross-review reinforced this from a different angle: FR-011 only requires "present and ask whether to refine or replace; never silently overwrite." The spec intentionally leaves refinement to agent judgment. My six sub-rules over-constrain agent behavior.

**Revised recommendation**: The spec should define a minimal contract for "refine" rather than prescriptive merge rules. Specifically: (a) all 7 required headings MUST be present in the refined output, (b) existing content in each section MUST NOT be silently deleted -- it may be revised, extended, or consolidated but not dropped, (c) `## Source Documents` MUST union old and new paths, (d) `## Type` MUST be re-evaluated against the combined input. This preserves agent flexibility while bounding the acceptable variance. The six detailed sub-rules from my original review are withdrawn as normative requirements but remain useful as implementation guidance.

### Recommendation 3: Support multiple --context paths (was P2)

**Status**: WITHDRAWN — defer to a follow-up spec.

Functional-typing's cross-review convinced me on this point. Their conservative position -- document the single-path constraint now, defer multi-path support -- is appropriate for spec 007's scope. My cross-review of functional-typing conceded this: "functional-typing's conservative reading is appropriate for spec 007's scope. Multi-path support is a feature enhancement better deferred to a follow-up spec or addressed when `/conversus interests` is specified."

The engine's multi-target support (SKILL.md L57-68) exists because the engine was designed for multi-file deliberation. The define handler's `--context` has different semantics -- it is supplementary context, not targets of analysis. The workaround I cited (copying documents into a single directory) is real but low-frequency. The right fix for spec 007 is functional-typing's: add a note to SKILL.md L778 clarifying that `--context` accepts a single path and that a directory path can be used to include multiple documents.

### Recommendation 4: Add a forward pipeline reference in the report (was P2)

**Status**: MODIFIED — scale down from a "Pipeline Overview" subsection to a single cautionary sentence.

Devil's advocate's cross-review exposed the core problem: my proposed pipeline overview describes commands (`interests`, `mode`) that do not exist yet (SKILL.md L29: "Future subcommands (not yet implemented)"). As devil's advocate put it: "This replaces one dead-end reference with a detailed dead-end map." Adding a subsection that says "each command's output feeds the next" when only `define` exists is speculative documentation in an implementation document.

Functional-typing's cross-review echoed this: "Adding a pipeline overview describing commands that do not yet exist introduces speculative content into an implementation document."

**Revised recommendation**: Replace my proposed multi-line "Pipeline Overview" subsection with a single sentence appended to the existing "Next step" line at SKILL.md L869: "Next step: `/conversus interests` (not yet implemented — this is the first of a series of guided setup commands)." This acknowledges the pipeline without describing unimplemented commands. The full pipeline overview belongs in spec 008 or a dedicated pipeline spec, not here.

### Recommendation 5: Add --type override flag (was P2)

**Status**: WITHDRAWN.

Functional-typing's cross-review correctly notes that this is a feature addition not motivated by any FR. FR-008 requires classification, not skipping classification. Adding `--type` expands the define handler's interface surface without an identified user need. My analogy to `validate_templates: false` (SKILL.md L55) was a stretch -- that escape hatch exists because template validation can fail on novel template structures, whereas type classification is a best-effort heuristic that always produces a usable result (with `[CLARIFY:]` tags on ambiguity). Expert users who disagree with the classification can simply edit the `## Type` line in `problem.md` -- that is the intended resolution mechanism.

### Recommendation 6: Verify anchor link rendering for colon-containing headings (was P2)

**Status**: MODIFIED — downgrade to P3.

Devil's advocate's cross-review reframed this correctly: the agent is a language model, not a markdown renderer. It reads "Routes to [Define: Problem Definition](#define-problem-definition)" and navigates to the heading `## Define: Problem Definition` by text matching, not by resolving the anchor algorithmically. The residual risk is real only if a future automation layer parses the dispatch table programmatically.

**Revised recommendation**: Retain as P3 documentation concern. Add a comment in spec.md noting the GFM slug convention used for anchor links, so that future spec authors who add headings with special characters are aware of the pattern. No implementation change needed.

### Recommendation 7: Document that define does not use the Agent tool (was P3)

**Status**: UPHELD — upgrade to P2.

Both cross-reviews independently converged on this recommendation with near-identical wording. Functional-typing rated it P2; devil's advocate did not contest it. The engine's prominent NON-NEGOTIABLE MULTI-AGENT RULES (SKILL.md L312-324) create a strong expectation that all conversus commands use sub-agents. Explicitly stating that `define` runs in the main conversation thread is a one-sentence addition that prevents misunderstanding about execution model, latency characteristics, and error handling behavior.

**Revised recommendation**: Upgrade to P2. Add after SKILL.md L771: "This command executes in the main conversation. No subagents are launched."

### Recommendation 8: Add error handling for unreadable context documents (was P3)

**Status**: MODIFIED — upgrade to P1.

Both functional-typing (P1) and devil's advocate (P2) rated this higher than my original P3. Functional-typing's framing was decisive in my cross-review: the run handler validates all paths in Step 1 (SKILL.md L195-196: "All resolved `TARGET_FILES` exist" and "All agent `docs` paths exist"). The define handler's `--context` is functionally equivalent to the engine's `docs`. Breaking this validation pattern is an internal inconsistency, not an edge case. A mistyped `--context` path silently produces a `problem.md` without the intended context, and nothing in the output indicates the context was missing. This is a silent data-quality failure with no visible signal.

**Revised recommendation**: Upgrade to P1. Add after SKILL.md L797: "If the path does not exist, fail with: 'Context path does not exist: {path}'. If a file within a context directory is unreadable, warn and skip that file." This mirrors the engine's path validation at L195-196.

---

## New Recommendations

### New Recommendation 1: Add `[CLARIFY:]` gate status to problem.md (Priority: P1)

Devil's advocate's cross-review (Dangerous Contradiction #2 and Rec #1) identified a genuine integration gap: `[CLARIFY:]` tags are advisory, not blocking. SKILL.md L872-875 warns the user about unresolved clarifications, but nothing prevents downstream consumers from proceeding with a `problem.md` full of `[CLARIFY:]` tags. My cross-review of devil's advocate proposed centralizing this in the artifact rather than distributing gate logic across consumer specs.

**Recommendation**: The define handler should set a status indicator in the `problem.md` output. When `[CLARIFY:]` tags are present, append a `## Status` section at the top (after `# Problem Definition`, before `## Decision`):

```markdown
## Status
draft — 3 items need clarification before this problem definition is ready for downstream use.
```

When no `[CLARIFY:]` tags are present, set `## Status` to `ready`. Downstream consumers (specs 008, 009) check this single section rather than each scanning for `[CLARIFY:]` tags independently. This centralizes the gate in the artifact itself, consistent with my position that producer-side validation is structurally prior to consumer-side checks.

### New Recommendation 2: Add empty-section [CLARIFY:] coverage for Constraints and Success Criteria (Priority: P2)

Functional-typing's review (Rec #5) correctly identified that SKILL.md L854 specifies empty-section handling only for Source Documents and Open Questions. It does not address what happens when the agent cannot determine any constraints or success criteria from a vague input. FR-010 (SKILL.md L852) says "any field where the agent cannot confidently determine the content MUST include a `[CLARIFY: ...]` tag" -- this logically applies to Constraints and Success Criteria, but L854 does not enumerate them.

**Recommendation**: Extend L854 to cover all sections: "If no constraints can be determined from the input, the Constraints section should contain `- [CLARIFY: No constraints identified — what limitations or requirements apply?]`. If no success criteria can be determined, the Success Criteria section should contain `[CLARIFY: What does a good outcome look like?]`." This makes FR-010's universal rule explicit for the two sections most likely to be affected by vague input.

### New Recommendation 3: Clarify dispatch behavior for file-path-like first arguments (Priority: P2)

Functional-typing's review raised dispatch precedence as a P1 concern. In my cross-review, I argued that the error path (SKILL.md L31-32) is the safer default: `/conversus definee` (typo) should produce "Unknown subcommand: 'definee'" rather than silently routing to `run` where it would fail with a confusing "Config file not found" error. I maintain that position. However, functional-typing's underlying concern is valid: the spec should be explicit about whether the dispatch table is exhaustive.

**Recommendation**: Add a clarifying sentence after SKILL.md L32: "The dispatch table is exhaustive. Any first argument that does not exactly match a known subcommand triggers this error. To pass a config file to the run handler, use the explicit form: `/conversus run <config-path>`." This eliminates ambiguity without introducing fallback routing. It also improves the error message by adding a suggestion: "Unknown subcommand: '{cmd}'. Available commands: run, define. Did you mean: `/conversus run {cmd}`?"

---

## Position Summary

The cross-reviews from functional-typing and devil's advocate exposed three significant adjustments in my original review. First, my refine semantics recommendation (original Rec #2) prescribed false determinism through six merge sub-rules that treat natural-language operations as algorithmic. Devil's advocate's critique was sharp and correct: "The recommendation replaces one ambiguity with six smaller ambiguities dressed up as precision." The revised position defines a minimal contract (all headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated) while leaving merge heuristics to agent judgment. Second, my `--context` path validation (original Rec #8) was severely underweighted at P3. Both cross-reviews independently rated it higher, and functional-typing's framing -- that breaking the engine's established validation pattern (SKILL.md L195-196) is an internal inconsistency, not an edge case -- was compelling enough that I conceded in my cross-review and now upgrade it to P1. Third, my pipeline overview recommendation (original Rec #4) fell to devil's advocate's observation that documenting a pipeline of unimplemented commands is speculative content in an implementation document; it is now reduced to a single cautionary sentence.

Two recommendations are withdrawn entirely. The `--type` override flag (original Rec #5) was a feature addition without FR motivation, and the multi-`--context` path support (original Rec #3) is correctly scoped for a follow-up spec rather than spec 007. Three new recommendations emerge from the cross-review synthesis: a `[CLARIFY:]` gate status in `problem.md` (centralizing downstream readiness in the artifact rather than distributing gate logic across consumer specs), explicit empty-section `[CLARIFY:]` coverage for Constraints and Success Criteria (extending FR-010's universal rule to the sections most affected by vague input), and dispatch exhaustiveness clarification (resolving the ambiguity functional-typing identified without introducing silent fallback routing).

The revised position retains the core architectural finding from my original review: the spec is well-implemented, all 12 FRs are satisfied, handler isolation is clean, and backward compatibility is preserved. The highest-priority gaps are now three: post-write schema validation (Rec #1, unchanged), context path validation (Rec #8, upgraded), and `[CLARIFY:]` gate status (New Rec #1). These three address the same systemic risk -- unvalidated artifacts flowing through the guided workflow pipeline -- from producer, input, and status perspectives respectively. The spec's strongest property remains the complete isolation between the define handler and the engine internals, which ensures that no define-related change can regress the existing `/conversus run` behavior.
