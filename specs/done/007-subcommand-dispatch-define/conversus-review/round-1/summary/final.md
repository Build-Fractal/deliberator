# Neutral Synthesis: 007-subcommand-dispatch-define

**Synthesizer**: neutral (no agent affiliation)
**Date**: 2026-03-22
**Deliberation mode**: cooperative
**Agents**: functional-typing, integration-architect, devils-advocate

---

## Process Summary

Three agents reviewed spec 007-subcommand-dispatch-define across four phases of deliberation. The spec introduces subcommand dispatch routing to SKILL.md and implements the first guided workflow command, `/conversus define`, which converts natural-language problem descriptions into structured `problem.md` artifacts.

**Phase 1 (Reviews)**: All three agents confirmed that the spec's 12 functional requirements (FR-001 through FR-012) and 5 success criteria (SC-001 through SC-005) are fully satisfied in the SKILL.md implementation. The dispatch table is correct, backward compatibility is preserved, the `problem.md` schema matches the spec character-for-character, and the define handler is cleanly isolated from the engine internals. No agent found a functional requirement that is unimplemented or incorrectly implemented. Differences arose in what the spec *omits*: functional-typing focused on dispatch matching semantics and structural completeness, integration-architect on output validation and cross-handler contracts, and devils-advocate on downstream enforcement gaps and taxonomy assumptions.

**Phase 2 (Cross-reviews)**: The most consequential cross-review finding was the rejection of functional-typing's P1 proposal to route unrecognized first arguments to `run` as a fallback. Both integration-architect and devils-advocate independently demonstrated that this would mask typos and create forward name-collision risks. Functional-typing withdrew the proposal in Phase 3. Cross-reviews also revealed agreement on `--context` path validation (all three agents identified the same gap independently) and disagreement on `[CLARIFY:]` tag enforcement semantics (advisory vs. gate), producer-side vs. consumer-side validation responsibility, and whether multi-path `--context` support belongs in spec 007.

**Phase 3 (Revisions)**: Functional-typing withdrew the fallback-to-`run` dispatch rule and adopted integration-architect's post-write schema validation as a new P1 recommendation. Integration-architect withdrew the `--type` override flag and multi-path `--context` support, conceded P1 priority for context path validation, reduced refine semantics from six prescriptive rules to four minimal post-conditions, and scaled the pipeline overview from a multi-line subsection to a single sentence. Devils-advocate revised the `[CLARIFY:]` gate from consumer-side enforcement (in spec 008) to producer-side status field (in `problem.md`), adopted content hash over timestamp for staleness tracking, and fixed a self-contradiction in the taxonomy closure language.

**Phase 4 (Disputes)**: Five disputes remain. Three are scope disputes (multi-path `--context`, `--force`/`--dry-run` flags, shared validation architecture) where the majority position is to defer. Two are structural disputes (`[CLARIFY:]` enforcement semantics and refine contract depth) where agents hold genuinely different design positions.

---

## Recommendation Scorecard

| ID | Recommendation | functional-typing | integration-architect | devils-advocate | Consensus Priority |
|----|---------------|-------------------|----------------------|-----------------|-------------------|
| R1 | Post-write schema validation for `problem.md` | P1 (New Rec A) | P1 (Rec #1) | P1 (Rec #2 revised) | **P1 -- unanimous** |
| R2 | `--context` path validation before ingestion | P1 (Rec #2) | P1 (Rec #8 revised) | P1 (Rec #7 revised) | **P1 -- unanimous** |
| R3 | Dispatch matching explicit: exact, case-sensitive | P1 (Rec #1 revised) | P2 (New Rec #3) | not contested | **P1 -- consensus** |
| R4 | Single-agent execution model statement (version-scoped) | P2 (Rec #6 revised) | P2 (Rec #7 revised) | not contested | **P2 -- consensus** |
| R5 | Empty-section `[CLARIFY:]` coverage (Constraints, Success Criteria) | P2 (Rec #5) | P2 (New Rec #2) | not contested | **P2 -- consensus** |
| R6 | `--output` directory creation semantics | P2 (Rec #4) | not addressed | not contested | **P2 -- uncontested** |
| R7 | Refine semantics minimal contract | flexible (defers) | P1 (Rec #2 revised) | P2 (New Rec #2) | **P2 -- majority** |
| R8 | Taxonomy closure design note | accepts (P2) | accepts (P2) | P2 (Rec #4 revised) | **P2 -- consensus** |
| R9 | `[CLARIFY:]` advisory scoping within spec 007 | P2 (New Rec B) | opposes (wants status field) | opposes (wants status field) | **disputed** |
| R10 | `## Status` section in `problem.md` | opposes | P1 (New Rec #1) | P1 (Rec #1 revised) | **disputed** |
| R11 | Staleness tracking (content hash, problem.md to interests.md) | flexible | agrees | P2 (Rec #3 revised) | **P2 -- deferred to spec 008** |
| R12 | Pipeline overview (single sentence) | accepts | P2 (Rec #4 revised) | accepts | **P2 -- consensus** |
| R13 | Frontmatter change acknowledged in spec | P3 (Rec #3 revised) | not flagged | not flagged | **P3 -- single advocate** |
| R14 | Dispatch rule in Baseline Features inventory | P3 (Rec #7) | not addressed | not addressed | **P3 -- single advocate** |
| R15 | Single `--context` path documented | P3 (Rec #8) | agrees (Rec #3 withdrawn) | dissents (wants multi-path) | **P3 -- majority** |
| R16 | Anchor link rendering note | not raised | P3 (Rec #6 revised) | P3 (deprioritized) | **P3 -- low priority** |
| R17 | Multi-path `--context` support | opposes (defer) | withdrawn (defer) | P2 (Rec #5 maintained) | **deferred -- majority** |
| R18 | `--force` and `--dry-run` flags | opposes (defer) | not addressed (implicit defer) | P2 (Rec #6 maintained) | **deferred -- majority** |
| R19 | Shared validation layer in dispatch section | flexible | opposes (schema-layer, not dispatch) | P2 (New Rec #1) | **deferred -- majority** |
| R20 | Escape hatch documentation (guided workflow is optional) | not raised | not raised | P3 (Rec #8 maintained) | **P3 -- single advocate** |
| R21 | Artifact size soft guidance | not raised | agrees (P3) | P3 (Rec #9 maintained) | **P3 -- low priority** |
| R22 | Refine diff summary | not raised | not raised | disputed (own New Rec) | **not adopted** |

---

## Dangerous Contradictions Found

### DC-1: `[CLARIFY:]` enforcement — advisory markers vs. status gate

This is the most consequential unresolved disagreement in the deliberation. Functional-typing insists that `[CLARIFY:]` tags are advisory within spec 007's scope, with enforcement deferred to consuming specs (functional-typing revision, New Rec B). Integration-architect and devils-advocate both argue for a `## Status` section (`draft` / `ready`) in `problem.md` that centralizes the gate signal in the artifact itself (integration-architect revision New Rec #1; devils-advocate revision Rec #1).

The danger: if tags are purely advisory and no status field exists, the spec creates a signaling mechanism with no obligation to read. Non-expert users -- the spec's explicit audience (spec.md L87) -- will ignore tag warnings and run `/conversus interests` on incomplete problem definitions. Conversely, if the status field is added without spec 008 existing to consume it, spec 007 grows the schema to solve a problem that has no consumer yet.

**Traced to**: functional-typing revision New Rec B; integration-architect revision New Rec #1; devils-advocate revision Rec #1; functional-typing disputes Dispute 1; integration-architect disputes Dispute 2; devils-advocate disputes Dispute 2.

### DC-2: Validation responsibility — producer-only vs. shared function

All three agents agree on producer-side post-write schema validation. The contradiction is whether consumer-side validation is also architecturally required. Integration-architect's revised position says "producer validates; define a validation function consumers can reference." Devils-advocate argues the shared function is non-negotiable because post-write user edits can break schema compliance after producer validation has already run. Functional-typing treats consumer validation as out of scope for spec 007.

The danger: if only producer-side validation is mandated, a user who edits `problem.md` to resolve `[CLARIFY:]` tags and accidentally deletes a heading creates a malformed artifact that no checkpoint catches. If consumer validation is required, the validation contract must be defined once (not reimplemented per-consumer), but spec 007 may not be the right place to define it since the consumers do not yet exist.

**Traced to**: integration-architect revision Rec #1; devils-advocate disputes Dispute 1; functional-typing revision New Rec A.

---

## Systemic Contradictions

### SC-1: Spec 007 as hermetic boundary vs. pipeline first step

The deliberation revealed a tension that runs through multiple disputes. Functional-typing treats spec 007 as a self-contained specification: its artifacts are advisory, its schema does not grow to serve unwritten consumers, and its scope is the minimal viable interface. Devils-advocate and integration-architect treat spec 007 as the first step in a pipeline: its artifacts must carry enough metadata for downstream consumption, and leaving integration contracts unspecified creates garbage-in-garbage-out risk.

Both positions are internally consistent. The contradiction is systemic: the spec simultaneously declares itself foundational ("establishes the dispatch infrastructure all guided workflow commands use" -- spec.md L6) and scoped ("this spec adds subcommand routing and implements the first guided command" -- spec.md L13). Foundational specs carry integration obligations; scoped specs defer them. The spec claims both identities.

**Traced to**: functional-typing disputes Dispute 1 (advisory vs. gate); integration-architect disputes Dispute 2 (status field); devils-advocate disputes Dispute 2 (advisory semantics are design failure); functional-typing revision Rec #8 (single-path as scope discipline); devils-advocate revision Rec #5 (multi-path as integration need).

### SC-2: Per-handler validation vs. shared architecture

All three agents independently recommended `--context` path validation in the define handler, all citing the same structural parallel (SKILL.md L195-196). Devils-advocate then noted that three reviews recommending the same copy-paste pattern is itself evidence of an architectural gap: if every handler replicates validation, the dispatch architecture has no shared validation layer. Functional-typing rejected this framing, arguing that routing and validation are distinct concerns. Integration-architect proposed a middle path: define the validation contract at the schema layer, not the dispatch layer.

The systemic tension: the deliberation produced a consensus fix (per-handler validation for spec 007) while simultaneously identifying that fix as the wrong long-term architecture. This is not a contradiction in the spec itself, but a contradiction in the review consensus -- the agents agreed on what to do now while disagreeing about whether it is the right thing to do.

**Traced to**: devils-advocate revision New Rec #1; functional-typing revision Rec #2; integration-architect disputes Dispute 4; devils-advocate disputes Dispute 3.

---

## Convergence Achieved

The following items reached genuine consensus across all three agents. They are listed in priority order.

### C-1: Post-write schema validation for `problem.md` (P1)

All three agents independently converged on this as the single most important structural addition. The define handler must validate that `problem.md` contains all 7 required headings after writing. If any heading is missing, add it with a `[CLARIFY:]` placeholder and re-write. This mirrors the engine's template validation (SKILL.md L286-295) and Phase 6 output validation (SKILL.md L659-676).

**Traced to**: integration-architect review Rec #1; functional-typing revision New Rec A; devils-advocate revision Rec #2; all three disputes files confirm convergence.

### C-2: `--context` path validation before ingestion (P1)

Universal convergence. All three agents rate this P1. The define handler must fail with "Context path does not exist: {path}" if the `--context` path does not exist, and warn with "No .md files found in context directory: {path}" if the path is a directory containing no markdown files. This mirrors the `run` handler's validation at SKILL.md L195-196.

**Traced to**: functional-typing review Rec #2; integration-architect revision Rec #8; devils-advocate revision Rec #7; all three disputes files confirm convergence.

### C-3: Dispatch matching is exact and case-sensitive (P1)

All three agents agree. Functional-typing withdrew the fallback-to-`run` proposal. The spec must explicitly state that subcommand matching is exact and case-sensitive, and that the dispatch table is exhaustive -- any non-matching first argument triggers the error at SKILL.md L31-32. Integration-architect additionally proposes a "Did you mean: `/conversus run {cmd}`?" suggestion in the error message.

**Traced to**: functional-typing revision Rec #1; integration-architect revision New Rec #3; devils-advocate disputes Convergence #3.

### C-4: `define` runs in main conversation, no subagents (P2)

All three agents agree on substance. Wording settled as: "In this version, the define command executes entirely in the main conversation. No subagents are launched." The phrase "In this version" scopes the constraint without prohibiting future evolution.

**Traced to**: functional-typing revision Rec #6; integration-architect revision Rec #7; devils-advocate disputes Convergence #4.

### C-5: Empty-section `[CLARIFY:]` coverage for Constraints and Success Criteria (P2)

Functional-typing and integration-architect converge. Devils-advocate does not contest. SKILL.md L854 must be extended to specify `[CLARIFY:]` behavior for empty Constraints and Success Criteria sections, applying FR-010's universal rule (SKILL.md L852) uniformly.

**Traced to**: functional-typing review Rec #5; integration-architect revision New Rec #2; integration-architect disputes Convergence #5.

### C-6: Refine semantics as minimal contract (P2)

Integration-architect and devils-advocate agree on four post-conditions: (a) all 7 headings preserved, (b) existing content not silently deleted, (c) Source Documents unioned, (d) Type re-evaluated. Functional-typing defers to integration-architect's formulation. The original six prescriptive merge rules are withdrawn as normative but retained as implementation guidance.

**Traced to**: integration-architect revision Rec #2; devils-advocate revision New Rec #2; functional-typing disputes Convergence (implicit flex).

### C-7: `--output` directory creation semantics (P2)

Uncontested. The define handler creates the output directory (including intermediates) if it does not exist. Fails with "Cannot create output directory: {path}" on failure.

**Traced to**: functional-typing review Rec #4; functional-typing revision Rec #4.

### C-8: Taxonomy closure design note (P2)

Integration-architect and devils-advocate agree. Functional-typing does not contest. The four-type taxonomy is acknowledged as intentionally closed. Revised language: "This taxonomy is intentionally closed. Each type maps to a specific mode in `/conversus interests`. Extending this taxonomy requires a companion update to the mode mapping in spec 008."

**Traced to**: devils-advocate revision Rec #4; integration-architect disputes Convergence #8.

### C-9: Pipeline overview as single sentence (P2)

All three agents agree the original multi-line pipeline overview was speculative. Scaled to a single sentence appended at SKILL.md L869: "Next step: `/conversus interests` (not yet implemented -- this is the first of a series of guided setup commands)."

**Traced to**: integration-architect revision Rec #4; functional-typing cross-review of integration-architect (Tensions, pipeline overview); devils-advocate cross-review of integration-architect (Dangerous Contradictions #3).

### C-10: Single `--context` path documented for spec 007 (P3)

Functional-typing and integration-architect agree. Devils-advocate dissents (prefers multi-path) but acknowledges this is a prioritization disagreement. The spec should state: "`--context` accepts exactly one path. To include multiple context sources, point to a directory containing them."

**Traced to**: functional-typing revision Rec #8; integration-architect revision Rec #3 (withdrawn, conceding to functional-typing); integration-architect disputes Convergence #6.

### C-11: Staleness tracking via content hash (P2, deferred to spec 008)

Devils-advocate and integration-architect agree on mechanism (SHA-256 content hash over modification timestamp). Functional-typing is flexible. Implementation deferred to spec 008 since `interests.md` does not yet exist.

**Traced to**: devils-advocate revision Rec #3; integration-architect disputes Convergence #7.

### C-12: `--type` override flag withdrawn

Integration-architect withdrew. Functional-typing correctly noted no FR motivates it. No dissent.

**Traced to**: integration-architect revision Rec #5.

### C-13: Backward compatibility preserved

All three agents confirm the run path is behaviorally unchanged. The dispatch mechanism is additive. The define handler references zero engine internals.

**Traced to**: all three Phase 1 reviews (Alignment sections); all three Phase 4 disputes (Convergence sections).

---

## Remaining Disputes

DISPUTES_BEGIN

### RD-1: `[CLARIFY:]` tags -- advisory vs. `## Status` section

**Positions**:
- **functional-typing** (AGAINST status field): `[CLARIFY:]` tags are advisory within spec 007. Adding a `## Status` section is unnecessary schema expansion. Gate enforcement is a spec 008 decision. The define handler writes the file regardless of tag count. (functional-typing revision New Rec B; functional-typing disputes Dispute 1)
- **integration-architect** (FOR status field): A `## Status` section (`draft` / `ready`) with clarification count centralizes the gate signal. The producer sets the status; the consumer checks one field instead of scanning for tags. (integration-architect revision New Rec #1; integration-architect disputes Dispute 2)
- **devils-advocate** (FOR status field, with RFC 2119 SHOULD): Agrees with integration-architect's mechanism but wants spec 007 to state: "Downstream commands SHOULD check the Status section before proceeding." Advisory semantics without any downstream expectation is a design failure. (devils-advocate revision Rec #1; devils-advocate disputes Dispute 2)

**Synthesis assessment**: The 2-1 split favors adding the status section, but functional-typing's boundary argument has structural merit -- spec 007 should not prescribe consumer behavior for specs that do not exist. The compromise position is: add the `## Status` section as a factual declaration (the artifact has N unresolved items), but scope the enforcement language to this spec only. Spec 007 states that `define` sets the status. What consumers do with it is their specification's decision. This satisfies integration-architect's "centralized signal" requirement and devils-advocate's "non-advisory" requirement without violating functional-typing's boundary principle. The status section is a factual annotation, not a gate directive.

### RD-2: Shared validation function -- mandatory vs. optional vs. deferred

**Positions**:
- **devils-advocate** (MANDATORY): The spec must mandate a named shared validation function ("validate problem.md schema") that both producer and consumer call. Without it, post-write user edits are an unguarded threat. Per-handler validation is copy-paste engineering. (devils-advocate disputes Dispute 1, Dispute 3)
- **integration-architect** (SCHEMA-LAYER): Define the validation contract at the schema layer (alongside the `problem.md` schema at SKILL.md L822-850), not in the dispatch section. Future handlers reference the same contract. Per-handler validation is correct for spec 007 as the pragmatic fix. (integration-architect disputes Dispute 4)
- **functional-typing** (HANDLER-LOCAL): Validation belongs in each handler. The dispatch layer is a routing table. Path validation is handler-specific (different handlers have different inputs). (functional-typing revision Rec #2)

**Synthesis assessment**: For spec 007, per-handler validation is the pragmatic and correct fix -- there is only one handler consuming `--context` paths. Devils-advocate's architectural concern about drift is valid but premature when only one consumer handler exists. Integration-architect's compromise (define the validation contract alongside the schema) is the appropriate forward-looking addition: a prose contract that says "any producer or consumer of `problem.md` validates against these 7 headings" defined once at the schema level. This is not a dispatch-layer concern (functional-typing is correct on that point) but it is more than pure per-handler scope (devils-advocate is correct that the pattern needs naming).

### RD-3: Multi-path `--context` -- spec 007 vs. follow-up

**Positions**:
- **devils-advocate** (IN SPEC 007): The single-path limitation forces stale-copy workarounds that degrade input quality. Implementation cost is trivial. No FR prohibits it. (devils-advocate revision Rec #5; devils-advocate disputes Dispute 4)
- **functional-typing** (DEFER): Spec 007 should ship a minimal interface. Multi-path is a feature addition with interaction concerns (ordering, deduplication, conflict resolution) that no FR motivates. (functional-typing revision Rec #8; functional-typing disputes Dispute 2)
- **integration-architect** (DEFER): Conceded to functional-typing's conservative scoping. Multi-path is appropriate for a follow-up spec. (integration-architect revision Rec #3 withdrawn)

**Synthesis assessment**: The 2-1 majority favors deferral. Devils-advocate's data-integrity concern is legitimate but speculative for spec 007's stated audience (non-expert users). The spec should document the limitation as a known constraint (not present it as the intended design) and note that multi-path support is a candidate for a future spec.

### RD-4: `--force` and `--dry-run` flags

**Positions**:
- **devils-advocate** (IN SPEC 007, P2): Spec 011 envisions automated invocations. Without `--force`, `/conversus define` is unusable in non-interactive contexts. `--dry-run` enables preview. (devils-advocate revision Rec #6)
- **functional-typing** (DEFER): Spec 007 targets non-expert human users. These flags add cognitive surface area for a use case that does not yet exist. FR-011's interactive safeguard is the correct behavior. (functional-typing disputes Dispute 3)
- **integration-architect** (DEFER): Sides with functional-typing. Flags expand the interface by 50% without immediate need. (integration-architect disputes Dispute 3)

**Synthesis assessment**: The 2-1 majority favors deferral. The flags are legitimate future features but spec 007's constraint (spec.md L87: "Must NOT require coding knowledge to use") argues against expanding the interface for automation scenarios that no current spec defines. A documentation note acknowledging that automation flags will be needed when spec 011 is implemented is the appropriate compromise.

### RD-5: Refine semantics -- minimal contract depth

**Positions**:
- **integration-architect** (FOUR RULES): Four verifiable post-conditions: all headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated. These are structural invariants, not algorithmic prescriptions. (integration-architect disputes Dispute 5)
- **devils-advocate** (FOUR RULES + DIFF SUMMARY): Agrees with the four rules but adds a fifth: the define handler should print a visible diff summary after refining ("Added 2 constraints, updated Context, Type unchanged") to make the heuristic operation auditable. (devils-advocate disputes Dispute 5)
- **functional-typing** (FLEXIBLE): Defers to integration-architect's formulation. Does not contest the four rules. (functional-typing disputes Convergence)

**Synthesis assessment**: Integration-architect's four-rule contract is the consensus minimum. Devils-advocate's diff summary is a useful UX addition but is implementation guidance rather than a schema-level requirement. The spec should adopt the four rules as normative and note the diff summary as a recommended practice.

DISPUTES_END

---

## Actionable Spec Changes

These are the primary deliverables of this synthesis, ordered by priority. Each change traces to specific deliberation artifacts and is supported by consensus or majority position.

### P1 Changes (must be adopted)

**Change 1: Add post-write schema validation for `problem.md`**

Add after the schema block in the define handler Output section (SKILL.md, after the schema at approximately L850):

> After writing `problem.md`, validate that the file contains all required headings: `# Problem Definition`, `## Decision`, `## Type`, `## Context`, `## Constraints`, `## Success Criteria`, `## Open Questions`, `## Source Documents`. If any heading is missing, add it with a `[CLARIFY: ...]` placeholder and re-write the file. Warn the user: "Added missing section: {heading}."

*Traced to*: integration-architect review Rec #1; functional-typing revision New Rec A; devils-advocate revision Rec #2. Unanimous P1.

**Change 2: Add `--context` path validation to the define handler**

Add to Context Ingestion in the define handler (SKILL.md, after the path resolution step at approximately L797):

> If the `--context` path does not exist, fail with: "Context path does not exist: {path}". If the path is a directory containing no `.md` files, warn: "No .md files found in context directory: {path}" and proceed without context.

*Traced to*: functional-typing review Rec #2; integration-architect revision Rec #8; devils-advocate revision Rec #7. Unanimous P1.

**Change 3: Add explicit dispatch matching semantics**

Add after the dispatch table (SKILL.md, after approximately L27):

> Subcommand matching is exact and case-sensitive. The dispatch table is exhaustive. Any first argument that does not exactly match a known subcommand triggers the unknown-subcommand error. To pass a config file to the run handler, use the explicit form: `/conversus run <config-path>`.

And enhance the error message at L31-32 to include a suggestion:

> Unknown subcommand: '{cmd}'. Available commands: run, define. (Future: interests, mode, converge, arbitrate, gate). Did you mean: `/conversus run {cmd}`?

*Traced to*: functional-typing revision Rec #1; integration-architect revision New Rec #3. Consensus P1.

### P2 Changes (should be adopted)

**Change 4: Add single-agent execution model statement**

Add after the Define: Problem Definition heading (SKILL.md, after approximately L771):

> In this version, the define command executes entirely in the main conversation. No subagents are launched.

*Traced to*: functional-typing revision Rec #6; integration-architect revision Rec #7. Consensus P2.

**Change 5: Extend empty-section `[CLARIFY:]` coverage**

Extend the empty-section handling rules (SKILL.md, at approximately L854) to include:

> If no constraints can be determined from the input, the Constraints section must contain: `- [CLARIFY: No constraints identified. What requirements or limitations apply?]`. If no success criteria can be determined, the Success Criteria section must contain: `[CLARIFY: What does a successful outcome look like?]`.

*Traced to*: functional-typing review Rec #5; integration-architect revision New Rec #2. Consensus P2.

**Change 6: Specify `--output` directory creation semantics**

Add to the Output section of the define handler (SKILL.md, after approximately L822):

> If the output directory does not exist, create it (including intermediate directories). If creation fails, fail with: "Cannot create output directory: {path}".

*Traced to*: functional-typing review Rec #4. Uncontested P2.

**Change 7: Add refine semantics minimal contract**

Expand the refine step in the define handler (SKILL.md, at approximately L791) from "incorporate the user's new input while preserving existing structure" to:

> Refine merges the new input with the existing `problem.md`. The following invariants apply: (a) All 7 required headings must be present in the refined output. (b) Existing content must not be silently deleted -- it may be revised, extended, or consolidated but not dropped without replacement. (c) Source Documents must union old and new paths. (d) Type must be re-evaluated against the combined input. Within these constraints, the agent uses judgment to update sections. The refined `problem.md` must pass the same post-write schema validation as a fresh definition.

*Traced to*: integration-architect revision Rec #2; devils-advocate revision New Rec #2; functional-typing disputes (defers to integration-architect). Consensus P2.

**Change 8: Add taxonomy closure design note**

Add after the problem type classification table in the define handler (SKILL.md, after the four-type table at approximately L818):

> Design note: This taxonomy is intentionally closed. Each type maps to a specific mode in `/conversus interests`. Problems that do not fit these types should be reframed in terms of the closest type, or users should bypass the guided workflow and configure `conversus.yml` directly. Extending this taxonomy requires a companion update to the mode mapping in spec 008.

*Traced to*: devils-advocate revision Rec #4; integration-architect disputes Convergence #8. Consensus P2.

**Change 9: Scale pipeline reference to single sentence**

Replace the "Next step" line in the define handler Report section (SKILL.md, at approximately L869):

> Next step: `/conversus interests` (not yet implemented -- this is the first of a series of guided setup commands).

*Traced to*: integration-architect revision Rec #4. Consensus P2.

**Change 10: Add `## Status` section to `problem.md` schema (disputed -- recommended)**

Add a `## Status` section to the `problem.md` schema between `# Problem Definition` and `## Decision`:

> ```
> ## Status
> <draft | ready> -- <N> items need clarification (if draft)
> ```
>
> The define handler sets `status: draft` when any `[CLARIFY:]` tag is present in the output. It sets `status: ready` when none are present. This is a factual annotation of the artifact's completeness. Whether downstream commands treat `draft` status as blocking or advisory is defined by those commands' specifications.

This change reflects the 2-1 majority position (integration-architect and devils-advocate FOR; functional-typing AGAINST). The recommended language satisfies integration-architect's "centralized signal" requirement, devils-advocate's "non-advisory" requirement, and functional-typing's boundary principle (no prescribing consumer behavior from spec 007). See RD-1 for the full dispute record.

*Traced to*: integration-architect revision New Rec #1; devils-advocate revision Rec #1; functional-typing disputes Dispute 1.

### P3 Changes (optional, low-risk)

**Change 11: Document single `--context` path constraint**

Add to the define handler Input section (SKILL.md, at approximately L778):

> `--context` accepts exactly one path. To include multiple context sources, point to a directory containing them.

*Traced to*: functional-typing revision Rec #8; integration-architect revision Rec #3 (withdrawn, conceding). Majority P3.

**Change 12: Acknowledge frontmatter change in spec**

Amend spec.md L17 ("What changes") to mention the frontmatter `description` update:

> SKILL.md gains a "Subcommand Dispatch" section before Step 1, the frontmatter description is updated to list supported subcommands, and a new `/conversus define` command handler is added. The existing `/conversus run` handler headings are namespaced (Input to Run: Input, Execution to Run: Execution) but behaviorally unchanged.

*Traced to*: functional-typing revision Rec #3. Single advocate, P3.

**Change 13: Note `--force`/`--dry-run` as future consideration**

Add a documentation note (spec.md, Constraints section or define handler):

> Future consideration: `--force` (overwrite without interactive prompt) and `--dry-run` (preview output without writing) flags may be added in a future spec to support non-interactive and automated invocations.

*Traced to*: devils-advocate revision Rec #6 (maintained P2); functional-typing disputes Dispute 3; integration-architect disputes Dispute 3. Majority defers, but acknowledges future need.

**Change 14: Note shared validation as architectural direction**

Add a documentation note to the `problem.md` schema section:

> The post-write validation step above defines the canonical schema check for `problem.md`. Future commands that consume this artifact should apply the same heading validation at read time. See this validation as a shared contract, not a handler-specific check.

*Traced to*: devils-advocate revision New Rec #1 (shared validation layer); integration-architect disputes Dispute 4 (schema-layer contract); functional-typing revision Rec #2 (handler-local). Compromise position.

---

## Key Concessions

### functional-typing concessions
1. **Withdrew fallback-to-`run` dispatch behavior** (original Rec #1) after both other agents demonstrated typo-masking and forward name-collision risks. The underlying concern (unspecified matching semantics) was preserved in a narrower form.
2. **Adopted post-write schema validation** as a new P1 recommendation (New Rec A) after integration-architect identified that schema definition without runtime validation is "a type declaration without a type checker."
3. **Narrowed frontmatter change acknowledgment** from P2 to P3 after devils-advocate exposed an internal inconsistency between dismissing anchor breakage as irrelevant (self-contained file) and demanding frontmatter documentation (external consumers).
4. **Accepted version-scoped wording** for single-agent declaration ("In this version") after devils-advocate raised forward-compatibility concern about permanently constraining future iterations.

### integration-architect concessions
1. **Withdrew multi-path `--context` support** (original Rec #3) after functional-typing argued it is a feature enhancement beyond spec 007's scope.
2. **Withdrew `--type` override flag** (original Rec #5) after functional-typing noted no FR motivates it.
3. **Reduced refine semantics** from six prescriptive merge rules to four minimal post-conditions after devils-advocate demonstrated that the original rules present heuristic operations as deterministic algorithms.
4. **Scaled pipeline overview** from multi-line subsection to single sentence after both other agents identified it as speculative documentation of unimplemented commands.
5. **Upgraded `--context` path validation** from P3 to P1 after functional-typing's structural-consistency framing proved more compelling.
6. **Downgraded anchor link rendering** from P2 to P3 after devils-advocate reframed the threat model (agent is a language model, not a markdown renderer).

### devils-advocate concessions
1. **Revised `[CLARIFY:]` gate mechanism** from consumer-side enforcement in spec 008 to producer-side status field in `problem.md` after integration-architect demonstrated that distributing gate logic across consuming specs is an integration nightmare.
2. **Revised validation contract** from consumer-only enforcement to producer-primary with shared function after integration-architect argued that distributing validation across specs 008-010 guarantees divergence.
3. **Adopted content hash** over modification timestamp for staleness tracking after integration-architect noted timestamps are fragile.
4. **Fixed taxonomy closure self-contradiction** ("intentionally closed" but "may be extended") after functional-typing identified the logical flaw.
5. **Partially reversed own position on refine semantics** -- originally argued refine is "inherently heuristic," then in disputes accepted integration-architect's four-rule minimal contract as necessary structural invariants.
