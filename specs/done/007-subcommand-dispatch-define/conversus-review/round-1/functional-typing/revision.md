# Revision — functional-typing Review of 007-subcommand-dispatch-define

**Reviewer**: functional-typing (structural correctness & specification compliance)
**Revision iteration**: 1
**Date**: 2026-03-22

---

## Recommendation Dispositions

### Recommendation 1: Add dispatch precedence rule — MODIFIED

**Original position**: Non-matching first arguments should be treated as config file paths routed to `run`. Proposed rule: "If [the first argument] does not exactly match any known subcommand, it is treated as a config file path and routed to `run`" (P1).

**Cross-review challenges**: Both integration-architect and devils-advocate independently argued that this proposal undermines the error path at SKILL.md L31-32. integration-architect's cross-review (Dangerous Contradictions, section 1) demonstrated the concrete failure mode: `/conversus definee` (typo) would silently route to `run` with `definee` as the config path, producing "Config file not found: definee" instead of the immediately actionable "Unknown subcommand: 'definee'." devils-advocate's cross-review (Dangerous Contradictions, section 2) raised a forward-compatibility concern: a future subcommand whose name collides with a config filename (e.g., `test` subcommand vs. `test.yml`) creates silent rerouting under my proposed rule.

**Revised position**: I withdraw the fallback-to-`run` behavior. The challengers are correct that the current error-on-unknown behavior at SKILL.md L31-32 is the safer default. The error path preserves FR-004's intent ("helpful error listing available commands") and avoids masking typos or future name collisions. However, the underlying concern remains valid: the spec does not specify matching semantics. I modify the recommendation to:

Add after SKILL.md L27: "Subcommand matching is exact and case-sensitive. If the first argument does not exactly match a known subcommand, the error at L31-32 fires." This preserves the error path while closing the ambiguity about matching behavior (exact vs. prefix vs. case-insensitive). The case-sensitivity concern raised by devils-advocate ("SKILL.md's dispatch table does not specify case sensitivity") is well-taken and motivates this narrower addition.

Priority remains P1 -- the matching semantics are still unspecified, which is a routing correctness gap. But the resolution is now a clarification of the existing error behavior, not a new fallback behavior.

**Credit**: integration-architect (concrete typo failure mode), devils-advocate (forward name-collision risk).

---

### Recommendation 2: Add `--context` path validation to define handler — SURVIVING

**Original position**: Add validation for `--context` path existence to Context Ingestion (SKILL.md L797-802), mirroring the `run` handler's validation at L195-196 (P1).

**Cross-review response**: All three reviewers converged on this finding. integration-architect's cross-review (Tensions, section 5) conceded that my P1 rating was "more appropriate" than their initial P3, stating "I concede that P1 is the correct priority." devils-advocate's cross-review (Safe Agreements, section 4) confirmed "Same finding, same fix, same rationale."

devils-advocate raised a broader architectural concern (Dangerous Contradictions, section 1): per-handler validation silos will drift apart as new subcommands are added. This is a legitimate design concern. However, I maintain that the fix belongs in spec 007 as a local addition to the define handler. The dispatch layer (SKILL.md L18-34) is a routing table, not a validation framework. Pushing validation into the dispatch layer would conflate routing with input validation -- two distinct concerns. Each handler has different inputs (`--context` for define, config paths for run) and therefore different validation requirements. The structural parallel with L195-196 is not "copy-paste" as devils-advocate characterizes it; it is applying the same principle (validate input paths before processing) in the appropriate handler-local scope.

**Proposed change** (unchanged): Add to Context Ingestion after SKILL.md L797: "If the `--context` path does not exist, fail with: 'Context path does not exist: {path}'. If the path is a directory containing no `.md` files, warn: 'No .md files found in context directory: {path}' and proceed without context."

---

### Recommendation 3: Acknowledge frontmatter change in spec — MODIFIED

**Original position**: The spec should acknowledge that the SKILL.md frontmatter `description` field (L3-10) was updated (P2).

**Cross-review challenges**: devils-advocate's cross-review (Tensions, section 4) identified an internal inconsistency in my own review: I dismissed anchor breakage from the heading renames as irrelevant because "the SKILL.md is self-contained" (Off-Base Assumptions, bullet 1), but then argued frontmatter changes must be documented because "agent runtimes use it for discovery" -- an external consumer concern. devils-advocate is right: either external consumers matter (both anchors and frontmatter are significant) or they do not (neither needs acknowledgment). I cannot hold both positions.

**Revised position**: I resolve the inconsistency by maintaining the frontmatter concern and retracting the self-containedness dismissal for anchors. The frontmatter `description` (SKILL.md L3-10) and the `compatibility` field (L11-13) are the skill's external API. The internal heading anchors are internal navigation aids consumed by the dispatch table within the same file. These are different categories: the frontmatter faces outward (agent runtime discovery), the anchors face inward (intra-file routing). The inconsistency devils-advocate identified was real but the resolution is category distinction, not abandonment of either concern.

The recommendation stands but is narrowed: the spec should acknowledge the frontmatter `description` update because it changes the skill's external presentation. Priority reduced to P3 -- integration-architect treated this as obviously correct and not worth flagging, and they have a point that the change is a natural corollary of adding subcommands. It is worth documenting for spec completeness, not for risk mitigation.

**Credit**: devils-advocate (identifying the internal inconsistency between my anchor-breakage dismissal and frontmatter concern).

---

### Recommendation 4: Add `--output` directory creation semantics — SURVIVING

**Original position**: Specify that the define handler creates the output directory if it does not exist, mirroring the `run` handler's Step 2 (SKILL.md L234-266) (P2).

**Cross-review response**: No reviewer challenged this recommendation. devils-advocate's cross-review (Dangerous Contradictions, section 1) grouped it with `--context` path validation under the broader "per-handler validation silos" concern but did not object to the substance. The recommendation remains as stated.

**Proposed change** (unchanged): Add to the Output section after SKILL.md L822: "If the output directory does not exist, create it (including intermediate directories). If creation fails, fail with: 'Cannot create output directory: {path}'."

---

### Recommendation 5: Specify empty-section handling for Constraints and Success Criteria — MODIFIED

**Original position**: Add `[CLARIFY:]` tags for empty Constraints and Success Criteria sections, since SKILL.md L854 only covers Source Documents and Open Questions (P2).

**Cross-review challenges**: devils-advocate's cross-review (Dangerous Contradictions, section 3) raised a consequential interaction: if devils-advocate's Recommendation 1 (adding a `[CLARIFY:]` gate to spec 008) is also adopted, then every `[CLARIFY:]` tag I recommend adding becomes a blocking gate. A vague one-word input like "architecture" would produce a `problem.md` that blocks `/conversus interests` on multiple fields. In my own cross-review of devils-advocate, I acknowledged this interaction (Dangerous Contradictions, item 2): "If both are adopted, the combined effect is that vague inputs produce artifacts that cannot be consumed until every empty section is manually filled -- a significant UX change."

Additionally, devils-advocate's cross-review (Tensions, section 2) notes a schema-level tension: my approach says "the schema is correct; the data is incomplete" (fill empty sections with `[CLARIFY:]` tags), while their approach questions whether the schema itself might need to flex.

**Revised position**: The recommendation stands in substance but needs scoping. The `[CLARIFY:]` tags for empty Constraints and Success Criteria sections are correct under FR-010 (SKILL.md L852: "Any field where the agent cannot confidently determine the content MUST include a `[CLARIFY: ...]` tag"). An empty section is definitionally a field where the agent cannot confidently determine content. This is not a new rule -- it is the logical consequence of the existing FR-010 rule applied uniformly.

However, I modify the recommendation to acknowledge the interaction with downstream gates. The proposed text should be: "If no constraints can be determined, include: `- [CLARIFY: No constraints identified. What requirements or limitations apply?]`. If no success criteria can be determined, include: `[CLARIFY: What does a successful outcome look like?]`." This is unchanged from my original. But I add the following note: "These tags are advisory markers per FR-010's existing semantics. Whether downstream commands treat them as blocking gates is a spec 008 decision, not a spec 007 decision." This prevents the interaction devils-advocate identified from becoming an unintended UX regression.

Priority remains P2.

**Credit**: devils-advocate (identifying the interaction between `[CLARIFY:]` tag expansion and downstream gate enforcement).

---

### Recommendation 6: Explicitly state that `define` is a single-agent command — MODIFIED

**Original position**: Add "This command executes entirely in the main conversation. No subagents are launched." to the define handler (P2).

**Cross-review challenges**: devils-advocate's cross-review (Tensions, section 3) raised a forward-compatibility concern: "What if a future iteration of `define` wants to launch a research agent to scan a large context directory?" They suggested wording the declaration as "a current constraint, not an architectural principle."

**Revised position**: The recommendation stands but with revised wording. devils-advocate's concern is legitimate -- hardcoding "No subagents are launched" as a permanent rule may prematurely constrain future iterations. I adopt their suggested framing.

**Proposed change** (revised): Add after SKILL.md L771: "In this version, the define command executes entirely in the main conversation. No subagents are launched." The phrase "In this version" scopes the constraint to the current spec without prohibiting future evolution.

Priority remains P2.

**Credit**: devils-advocate (forward-compatibility concern on permanent vs. versioned constraints).

---

### Recommendation 7: Add dispatch rule to Baseline Features inventory — SURVIVING

**Original position**: Add the dispatch mechanism to the Baseline Features section or a new "Spec-Backed Features" section after spec 007 is implemented (P3).

**Cross-review response**: No reviewer challenged this recommendation. It is a housekeeping item. The recommendation stands as stated.

---

### Recommendation 8: Clarify `--context` multiple-path semantics — SURVIVING

**Original position**: Clarify whether `--context` accepts one or multiple paths (P3).

**Cross-review response**: integration-architect's cross-review (Tensions, section 4) agreed that my conservative reading ("document the single-path constraint") is appropriate for spec 007's scope, stating: "functional-typing's conservative reading is appropriate for spec 007's scope. Multi-path support is a feature enhancement better deferred to a follow-up spec." No reviewer challenged the substance.

**Proposed change** (unchanged): State: "`--context` accepts exactly one path. To include multiple context sources, point to a directory containing them."

---

## New Recommendations

### New Recommendation A: Add post-write schema validation for `problem.md` (Priority: P1)

**Source**: integration-architect's cross-review (Dangerous Contradictions, section 2) identified that my review did not address runtime conformance of the `problem.md` output to its schema. Their framing is compelling: "a faithful schema definition without runtime validation is like a type declaration without a type checker."

**Rationale**: The `run` handler has template validation (SKILL.md L286-295) and output validation (L659-676). The `define` handler specifies a schema (L824-850) but has no validation step. Since `define` uses LLM generation (not template filling) to produce `problem.md`, structural conformance is not guaranteed. An agent that writes `## Constraint` (singular) instead of `## Constraints` or omits `## Open Questions` entirely produces a file that breaks downstream parsing by `/conversus interests`.

**Proposed change**: Add after the schema block (after SKILL.md L850): "After writing `problem.md`, validate that the file contains all seven required headings: `# Problem Definition`, `## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`. If any heading is missing, add it with a `[CLARIFY: ...]` placeholder and re-write the file."

This is complementary to my Recommendation 5 (empty-section handling). Recommendation 5 addresses semantically empty sections; this recommendation addresses structurally absent sections.

**Credit**: integration-architect (identifying the type-declaration-without-type-checker gap).

---

### New Recommendation B: Scope `[CLARIFY:]` tags as advisory within spec 007 (Priority: P2)

**Source**: The tension between my Recommendation 5 and devils-advocate's Recommendation 1 (cross-review Dangerous Contradictions, section 3) revealed that `[CLARIFY:]` tags have no defined enforcement semantics. My review treats them as advisory markers; devils-advocate treats them as blocking contracts.

**Rationale**: FR-010 (spec L39) says ambiguities "MUST be marked with `[CLARIFY: ...]` tags for the user to resolve before proceeding." The phrase "before proceeding" is ambiguous: does it mean "before proceeding to the next `/conversus` command" (a gate) or "before proceeding to use `problem.md` as final" (advisory)? Spec 007 should clarify its own semantics without prescribing spec 008's consumption behavior.

**Proposed change**: Add to the `problem.md` schema preamble (after SKILL.md L822): "`[CLARIFY:]` tags are advisory markers indicating fields that benefit from user review. The `define` command writes the file regardless of how many `[CLARIFY:]` tags are present. Whether downstream commands enforce these tags as gates is defined by those commands' own specifications."

This is not a normative change -- it makes explicit what is currently implicit. It prevents the unintended interaction where expanding `[CLARIFY:]` coverage (Recommendation 5) silently creates blocking behavior in downstream commands.

**Credit**: devils-advocate (identifying the advisory-vs-blocking ambiguity in `[CLARIFY:]` semantics).

---

## Position Summary

My original review correctly identified the spec's structural soundness: dispatch table completeness, backward-compatible defaults, run-path preservation, schema fidelity, and full FR coverage. These findings were confirmed by all three reviewers and remain unchallenged. The spec is well-constructed and the SKILL.md implementation is faithful to it.

The most significant correction to my original review is the withdrawal of the fallback-to-`run` dispatch behavior (original Recommendation 1). Both integration-architect and devils-advocate demonstrated that the proposed rule would mask typos and create forward-compatibility risks with future subcommand names. The underlying concern -- unspecified matching semantics -- remains valid, but the resolution is a clarification of the existing error behavior (exact, case-sensitive matching that fires the error at L31-32), not a new fallback path. I also accept integration-architect's point about post-write schema validation, which my original review overlooked entirely. The `define` handler uses LLM generation to produce `problem.md`, making structural conformance a runtime concern that the spec should address with an explicit validation step. This is now my New Recommendation A and sits alongside my surviving recommendations on path validation and empty-section handling.

The remaining modifications are refinements rather than reversals. The frontmatter acknowledgment (Recommendation 3) was narrowed after devils-advocate exposed an internal inconsistency in my treatment of external consumers. The single-agent declaration (Recommendation 6) was reworded to be version-scoped rather than permanent. The empty-section handling (Recommendation 5) gained a note about the interaction with downstream gate enforcement. These changes sharpen the recommendations without altering their direction. Across seven surviving or modified recommendations and two new ones, the common thread is structural completeness: the spec defines a schema but omits the validation discipline that makes the schema enforceable, and it routes to handlers but leaves matching semantics implicit. Both gaps are closable within spec 007's scope.
