# Cross-Review of devils-advocate by functional-typing

**Reviewer**: functional-typing (structural correctness & specification compliance)
**Reviewing**: devils-advocate's Phase 1 review of spec 007-subcommand-dispatch-define

---

## Dangerous Contradictions

### 1. Taxonomy closure vs. spec fidelity: we disagree on what the spec actually requires

devils-advocate treats the four-type taxonomy (spec L37-38) as potentially incomplete, listing "prioritization," "migration," "compliance," and "decomposition" as missing types (devils-advocate Off-Base Assumptions, second bullet). This framing implies the spec has a gap that should be filled.

My review did not flag taxonomy completeness at all because it is outside my remit as a structural reviewer: the spec explicitly states the four types and the SKILL.md implementation (L806-813) reproduces them 1:1. The taxonomy is structurally correct against the spec. devils-advocate's concern is a design-level challenge, not a compliance finding.

The contradiction becomes dangerous when devils-advocate's Recommendation 4 proposes adding a "Design Note" to the type table (spec L52). This would introduce normative text ("The taxonomy is intentionally closed... users should bypass `define` and write `conversus.yml` directly") that is not present in the current spec. From a structural standpoint, adding escape-hatch guidance to a section that currently contains only a classification table changes the section's contract. If downstream spec 008 already maps types 1:1 to modes (as devils-advocate correctly notes), then any text acknowledging the taxonomy might be extended creates an implicit promise of extensibility that the current 008 mode matrix does not support. The Design Note should either commit to closure (no extension without a companion 008 update) or commit to extensibility (with a schema versioning mechanism). devils-advocate's proposed text does both ("intentionally closed" but "may be extended in a future spec"), which is a structural contradiction.

### 2. `[CLARIFY:]` gate enforcement: we agree on the problem but propose incompatible solutions

devils-advocate's top recommendation (Recommendation 1, Priority P1) is to add a `[CLARIFY:]` gate to spec 008: "/conversus interests MUST present them and ask the user to resolve them before proceeding." My review does not address cross-spec enforcement because spec 008 is outside the structural scope of a 007 review.

The contradiction: devils-advocate frames the `[CLARIFY:]` gate as a spec 007 responsibility ("Add to spec 007 section 2 or to spec 008 FR-001"). If the gate is added to spec 007, it changes the contract of `problem.md` from "artifact with advisory markers" to "artifact with blocking markers." This would require my review's Recommendation 5 (empty-section handling for Constraints and Success Criteria, which proposes adding `[CLARIFY:]` tags to empty sections) to be re-evaluated: every `[CLARIFY:]` tag I recommend adding would become a gate that blocks downstream progression. A vague one-word input like "architecture" would produce a `problem.md` that blocks `/conversus interests` on multiple fields. This is arguably correct behavior, but it means my Recommendation 5 and devils-advocate's Recommendation 1 interact in ways neither review acknowledges. If both are adopted, the combined effect is that vague inputs produce artifacts that cannot be consumed until every empty section is manually filled -- a significant UX change that should be evaluated holistically, not as two independent patches.

### 3. Validation contract scope: producer-side vs. consumer-side

devils-advocate's Recommendation 2 (Priority P1) proposes adding a "problem.md Validation" subsection to spec 007 with structural rules ("Decision must be exactly one sentence," "Constraints must be a bulleted list with at least one entry"). My review found the schema fidelity between spec L45-71 and SKILL.md L824-850 to be exact (my Alignment, fourth bullet), meaning the structural contract already exists implicitly in the schema definition.

The contradiction: devils-advocate wants explicit validation rules for consumers (spec 007 defining what consumers must check). My review focuses on producer correctness (SKILL.md must output conforming artifacts). These are complementary but they clash on where the responsibility sits. If spec 007 mandates "Decision must be exactly one sentence," the enforcement point matters: should the `define` handler refuse to write a multi-sentence Decision (producer validation), or should `/conversus interests` refuse to read one (consumer validation)? devils-advocate says "Any consumer of `problem.md` MUST validate" -- but the `define` handler is the producer, not a consumer. The spec would simultaneously tell the producer "write this schema" and tell consumers "validate this schema," without specifying which side owns the canonical check. This is a classic dual-validation problem that needs a single source of truth.

---

## Tensions

### 1. Automation readiness vs. current spec scope

devils-advocate's Recommendation 6 proposes `--force` and `--dry-run` flags for `/conversus define`, citing spec 011 (gates) as the justification (devils-advocate Missed Opportunities, second bullet). My review did not raise automation flags because the spec explicitly targets non-expert human users (spec L87: "Must NOT require coding knowledge to use") and the SKILL.md compatibility note (L11-13) already scopes the runtime to conversational agents.

The tension: devils-advocate is correct that spec 011 envisions automated invocations, and my review is correct that spec 007 targets interactive use. Both are true simultaneously. The question is whether spec 007 should pre-invest in automation affordances for a future spec or remain minimal. My structural position is that adding flags not required by any current FR creates spec sprawl. devils-advocate's design position is that omitting them creates technical debt. This is a legitimate prioritization disagreement, not a factual one.

### 2. `--context` path validation: same finding, different severity

Both reviews independently flagged missing `--context` path validation. My review (Missed Opportunities, third bullet; Recommendation 2, Priority P1) cited the asymmetry with the `run` handler's validation at SKILL.md L195-196. devils-advocate's review (Missed Opportunities, fifth bullet; Recommendation 7, Priority P2) cited the same lines and proposed the same fix.

The tension is in severity: I rated this P1 because it is a structural completeness gap (the `define` handler omits validation that the `run` handler requires, breaking internal consistency). devils-advocate rated it P2 because their P1 slots are occupied by cross-spec concerns (`[CLARIFY:]` gates, validation contracts). The underlying finding is identical; the disagreement is about whether intra-spec consistency outranks cross-spec robustness. I maintain that structural consistency within SKILL.md is the higher priority because it can be resolved within spec 007's scope, whereas cross-spec gates require coordination with spec 008.

### 3. Frontmatter change acknowledgment: structural concern vs. non-issue

My review (Off-Base Assumptions, first item; Recommendation 3, Priority P2) flagged that the SKILL.md frontmatter `description` field (L3-10) was updated to mention subcommands, but this change is not listed in the spec's "what changes" section (spec L17). devils-advocate did not mention the frontmatter at all.

The tension: from a structural completeness standpoint, the frontmatter is the skill's external interface -- agent runtimes use it for discovery. From a devil's-advocate standpoint, the frontmatter change is cosmetic and does not affect the spec's core claims. I continue to hold that the spec should acknowledge what it changes, even if the change is minor, because spec trustworthiness depends on completeness of the change inventory. But I acknowledge this is a structural-purity concern, not a functional-risk concern.

### 4. Single-agent execution model: explicit negation vs. inferability

My review (Missed Opportunities, fifth bullet; Recommendation 6, Priority P2) proposed explicitly stating that `define` does not launch subagents. devils-advocate did not raise this.

The tension: devils-advocate's review focuses on what happens when artifacts cross command boundaries (007 to 008), while my review focuses on what happens within a single command's execution model. Both are valid scopes. However, the absence of an execution model statement in the `define` handler (SKILL.md L769-876) is a structural gap that could cause implementer confusion, especially given that the `run` handler (L312-324) extensively documents its multi-agent model. The gap is real even if devils-advocate did not prioritize it.

### 5. Staleness tracking: different boundaries, same pattern

devils-advocate's Recommendation 3 (Priority P2) proposes staleness tracking between `problem.md` and `interests.md`, noting that spec 008 already tracks staleness between `interests.md` and `conversus.yml` (008 L59). My review did not address cross-artifact staleness because it is a spec 008 concern.

The tension: devils-advocate is right that the staleness pattern should be consistent across all artifact boundaries. My omission is a scope decision, not a disagreement. If spec 007 is responsible for defining `problem.md`'s contract, then staleness metadata (timestamp, hash) should arguably be part of the `problem.md` schema defined here. This would affect my schema fidelity finding (Alignment, fourth bullet) -- adding a `## Generated From` section would break the current character-for-character match between spec and SKILL.md. The tension is between schema stability (my concern) and cross-artifact consistency (devils-advocate's concern).

---

## Safe Agreements

### 1. Dispatch mechanism is correct and backward-compatible

Both reviews confirm that the dispatch table (SKILL.md L22-27) correctly implements FR-001 through FR-004 and that the backward-compatible default to `run` (L26) satisfies FR-003/SC-004. devils-advocate's Alignment, first bullet, cites spec L29 and L88; my Alignment, first and second bullets, cite the same SKILL.md lines and spec references. Neither review found a structural or design flaw in the dispatch mechanism itself.

### 2. Schema fidelity between spec and SKILL.md is exact

devils-advocate does not explicitly flag schema drift (confirming absence of the issue), and my review (Alignment, fourth bullet) verified character-for-character match between spec L45-71 and SKILL.md L824-850. Both reviews accept the schema as implemented correctly. The disagreements are about what should be added to the schema (validation rules, staleness metadata), not about what is currently there.

### 3. `--context` path validation is missing and should be added

As noted in the Tensions section, both reviews independently identified this gap with the same evidence (SKILL.md L797 vs. L195-196) and proposed equivalent fixes. The disagreement is priority (P1 vs. P2), not substance. This is the strongest consensus finding across both reviews.

### 4. `problem.md` overwrite protection is correctly specified

devils-advocate's Alignment, fifth bullet, confirms that FR-011's overwrite protection (spec L40) matches the pattern established by spec 008. My review's FR-to-section mapping (Alignment, fifth bullet) confirms SKILL.md L788-793 implements FR-011 with the correct interactive flow (present existing file, ask refine or replace, never silently overwrite). Neither review found a gap in this requirement's implementation.

### 5. `[CLARIFY:]` tags are structurally sound but behaviorally underspecified

devils-advocate notes that `[CLARIFY:]` tags are "a direct analogue to the dispute-parsing subsystem's structural markers" (Alignment, second bullet, citing SKILL.md L750-751). My review confirms the tag syntax is correctly reproduced in the schema (Alignment, fourth bullet). Both reviews agree the tags are well-defined as a structural mechanism. The disagreement (covered in Dangerous Contradictions, item 2) is about enforcement semantics, not tag syntax.

### 6. The run path is behaviorally unchanged

Both reviews confirm the heading renames (`Input` to `Run: Input`, `Execution` to `Run: Execution`) are cosmetic and do not alter step content. devils-advocate's Alignment, first bullet, calls the dispatch "additive-only" (citing spec L88). My Alignment, third bullet, states "All content beneath these headings is untouched." SC-003 (spec L79) is satisfied by both accounts.

---

## Summary

The most consequential disagreement is about `[CLARIFY:]` gate enforcement (Dangerous Contradictions, item 2). If devils-advocate's Recommendation 1 is adopted alongside my Recommendation 5, the combined effect transforms vague inputs from "producing artifacts with advisory markers" into "producing artifacts that block all downstream progression." This interaction must be evaluated as a single design decision, not two independent patches.

The most actionable shared finding is missing `--context` path validation (Safe Agreements, item 3). Both reviews propose the same fix with the same evidence. This should be adopted regardless of any other decisions.

The structural concerns I raise (dispatch precedence, frontmatter acknowledgment, single-agent execution model) and the design concerns devils-advocate raises (taxonomy closure, staleness tracking, automation flags) are complementary rather than conflicting -- they operate at different levels of the spec and can be addressed independently.
