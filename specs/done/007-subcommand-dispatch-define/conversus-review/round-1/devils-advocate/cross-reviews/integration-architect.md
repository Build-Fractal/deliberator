# Cross-Review: Integration Architect (from Devil's Advocate)

## Dangerous Contradictions

### 1. Post-write validation vs. no consumer contract

Integration-architect's top recommendation (P1 #1) is post-write schema validation: verify all 7 headings exist in `problem.md` after the agent writes it. My P1 #2 asks for something structurally different: a validation contract that downstream consumers enforce before reading. These look complementary but are actually in tension about where responsibility lives.

Integration-architect places validation at the producer boundary: the define handler checks its own output. I place it at the consumer boundary: `/conversus interests` checks its input. The danger is that implementing only the producer-side check (integration-architect's recommendation) creates false confidence -- the file had 7 headings when written, so it must be valid. But post-write mutations are the real threat: the user manually edits `problem.md` to resolve `[CLARIFY:]` tags and accidentally deletes the `## Type` heading, or reformats constraints from a bulleted list to prose. Producer-side validation catches agent generation errors; consumer-side validation catches the full failure space.

If the spec adopts integration-architect's recommendation without mine, `problem.md` is validated exactly once, at the moment it is least likely to be wrong (the agent just generated it from a template), and never again at the moment it is most likely to be wrong (after human editing). This is the validation equivalent of checking your parachute in the factory and never checking it before you jump.

**Resolution**: Both are needed. The spec should mandate producer-side heading validation (integration-architect's recommendation) AND consumer-side contract validation (my recommendation). These are different failure modes and require different checkpoints.

[Integration-architect review, Recommendation #1; Devil's advocate review, Recommendation #2]

### 2. Refine semantics: operational rules vs. acknowledging the problem

Integration-architect's P1 #2 proposes detailed merge semantics for the refine operation: replace the Decision, merge Constraints (deduplicated), merge Open Questions (remove resolved ones), re-evaluate Type, union Source Documents, rewrite Context. My review flags the same gap but stops at identifying it as underspecified (SKILL.md L791).

The contradiction: integration-architect's proposed semantics are themselves unvalidated. "Merge constraints (deduplicated)" assumes constraints are atomic items that can be compared for equality. But constraints in natural language are not deduplicate-able -- "Must support 10,000 concurrent users" and "The system needs to handle 10K simultaneous connections" are duplicates that no markdown parser can detect. "Remove resolved open questions" requires determining which questions are answered by the new input, which is a judgment call the agent makes differently every time.

Integration-architect's recommendation presents these merge operations as if they were deterministic algorithms. They are not. They are heuristics that the agent will interpret variably across invocations -- which is exactly the non-determinism problem integration-architect claims the recommendation solves. The recommendation replaces one ambiguity ("preserving existing structure") with six smaller ambiguities dressed up as precision.

I am not arguing against specifying refine semantics. I am arguing that the spec should acknowledge refine as inherently heuristic and bound the acceptable variance rather than pretending it can be made deterministic through prose rules.

[Integration-architect review, Recommendation #2; Devil's advocate review, Missed Opportunities bullet on underspecified refine behavior -- implicit in the "no idempotency guarantee" point]

### 3. Pipeline overview creates a dead-end promise

Integration-architect's P2 #4 proposes adding a "Pipeline Overview" section showing the full three-command chain: `define` -> `interests` -> `mode`. The proposed text says: "Each command's output feeds the next. The pipeline produces a runnable `conversus.yml` without requiring manual config authoring."

My review's Off-Base Assumption #1 points out that `[CLARIFY:]` tags are treated as gates by the spec but as decoration by the implementation -- nothing stops a user from running `interests` with unresolved clarifications. Adding a pipeline overview that says "each command's output feeds the next" reinforces the assumption that the outputs are valid when they may not be. It also promises commands (`interests`, `mode`) that do not exist yet (SKILL.md L29: "Future subcommands (not yet implemented)").

The contradiction: integration-architect's own observation (Recommendation #4) notes that the "Next step: /conversus interests" reference at L869 is "a dead end" because interests does not exist. Yet the proposed fix is to add more text describing a pipeline that also does not exist. This replaces one dead-end reference with a detailed dead-end map. The user goes from "I don't know what to do next" to "I know exactly what to do next, but I can't do any of it."

The spec should either defer the pipeline overview until spec 008 is implemented, or add it with an explicit caveat that only `define` and `run` are currently available.

[Integration-architect review, Recommendation #4; Devil's advocate review, Off-Base Assumption #1]

---

## Tensions

### 1. Handler isolation praise vs. missing cross-handler contracts

Integration-architect highlights handler isolation as a strength: "The define handler references zero engine internals -- no template variables, no phase numbers, no mode logic" (Alignment, bullet 3). I agree the isolation is clean. But my review's P1 #1 (the `[CLARIFY:]` gate) and P2 #1 (staleness tracking) point out that this isolation comes at a cost: there is no contract between the define handler and future handlers.

The tension is real: handler isolation is good software engineering, but handlers in a pipeline cannot be completely isolated. They produce and consume shared artifacts. Integration-architect praises the isolation but then recommends adding schema validation and a pipeline overview -- both of which are cross-handler contracts that reduce isolation. The question is where to draw the line: isolated enough that handlers cannot break each other (good), but connected enough that they can validate each other's artifacts (also necessary).

This is not a contradiction -- it is a design tension that the spec should acknowledge explicitly rather than letting it be resolved ad hoc by each future spec.

[Integration-architect review, Alignment bullet 3; Devil's advocate review, Recommendations #1 and #3]

### 2. Single --context path: same conclusion, different urgency

Both reviews identify the single `--context` path as a limitation. Integration-architect rates it P2 #3 ("medium" impact in missed opportunities). I rate it P2 #5 ("low" impact in missed opportunities). We agree on the fix (allow multiple `--context` flags).

The tension is in framing. Integration-architect says users "will work around this by copying documents into a single directory, creating stale duplicates that drift from their sources." I say "the `run` engine supports list-based targets (SKILL.md L57-68); `define` should too." Integration-architect's framing is stronger -- the workaround creates real data integrity problems. My framing is weaker -- consistency with another command is nice but not urgent. On reflection, integration-architect's impact assessment is more rigorous here.

[Integration-architect review, Recommendation #3; Devil's advocate review, Recommendation #5]

### 3. The --dry-run flag: different scopes

Integration-architect proposes `--dry-run` as a missed opportunity (medium impact) to preview output before writing. My review proposes both `--force` and `--dry-run` as a P2 recommendation, but frames them differently: not as preview tools but as composability requirements for automated/scripted invocations and CI pipelines (citing spec 011's gates).

The tension: integration-architect sees `--dry-run` as user convenience. I see it as an architectural requirement for non-interactive contexts. If we accept integration-architect's framing, `--dry-run` is nice-to-have. If we accept mine, `--dry-run` (and `--force`) are prerequisites for the spec 011 integration that is already on the roadmap. The priority depends on whether we plan for the guided workflow to remain interactive-only or to support automated invocation.

[Integration-architect review, Missed Opportunities bullet 2; Devil's advocate review, Recommendation #6]

### 4. Anchor link fragility: different threat models

Integration-architect's P2 #6 raises anchor link fragility for colon-containing headings (`## Define: Problem Definition` -> `#define-problem-definition`). The concern is that the agent runtime's markdown parser may not follow GitHub-Flavored Markdown slug rules.

My review does not raise this issue. Having considered it now, the concern is legitimate but the threat model is narrow: the dispatch table is read by the agent as navigation instructions, not as parsed hyperlinks. The agent sees "Routes to [Define: Problem Definition](#define-problem-definition)" and navigates to the heading `## Define: Problem Definition` -- it does not need to resolve the anchor algorithmically. The agent is a language model, not a markdown renderer.

The residual risk is if a future automation layer parses the dispatch table programmatically. Integration-architect is right to flag it, but the priority should be P3 (documentation) rather than P2 (implementation concern).

[Integration-architect review, Recommendation #6]

---

## Safe Agreements

### 1. problem.md needs validation before downstream consumption

Both reviews independently identify this as their highest-priority issue. Integration-architect frames it as "post-write schema validation" (P1 #1). I frame it as "define a validation contract for consumers" (P1 #2). The specific mechanisms differ (see Dangerous Contradictions #1), but the diagnosis is identical: an unvalidated `problem.md` creates a garbage-in-garbage-out risk for the entire guided workflow pipeline.

This is the single most important gap in the spec. Both reviews agree.

[Integration-architect review, Recommendation #1; Devil's advocate review, Recommendation #2]

### 2. Error handling for unreadable context paths is missing

Integration-architect's P3 #8 and my P2 #7 identify the same gap: the spec does not specify what happens when `--context` points to a nonexistent or unreadable path. Both reviews reference the `run` engine's path validation at SKILL.md L195-196 as the pattern to follow. Both propose the same fix: fail with a clear error message naming the bad path.

The only difference is priority (integration-architect: P3, me: P2). I rate it higher because silent context loss directly degrades `problem.md` quality with no visible signal -- the user gets a structurally valid file that is substantively wrong. Integration-architect may rate it lower because the define handler is interactive and the user would likely notice missing context. Both framings are reasonable.

[Integration-architect review, Recommendation #8; Devil's advocate review, Recommendation #7]

### 3. Backward compatibility is solid

Both reviews confirm that FR-002 and FR-003 are correctly implemented. Integration-architect verifies via git diff that only heading renames touched the existing engine content (Alignment, bullet 2). My review confirms the same through the dispatch table structure and the constraint C2 (spec L88). Neither review identifies any risk to existing `/conversus run` behavior.

This is the spec's strongest property and it is uncontested.

[Integration-architect review, Alignment bullet 2, FR mapping FR-002/FR-003; Devil's advocate review, Alignment bullet 1]

### 4. Handler isolation is correctly implemented

Integration-architect provides detailed evidence that the define handler is self-contained (Alignment, bullet 3). My review does not contest this. The define handler's independence from engine internals is a clean design that prevents accidental regressions. Both reviews treat this as a settled positive.

[Integration-architect review, Alignment bullet 3]

### 5. The [CLARIFY:] tag pattern is sound but unenforced

Integration-architect does not explicitly call out the enforcement gap (their review focuses on the output side), but their missed opportunity about schema validation implicitly supports it. My review makes this explicit: `[CLARIFY:]` tags are the spec's primary ambiguity mechanism, but nothing prevents downstream commands from ignoring them (Off-Base Assumption #1, Recommendation #1).

We agree that the mechanism is well-designed. The disagreement is about what to do next: integration-architect's recommendations address output validation (does the file have the right headings?), while mine address semantic enforcement (do the downstream commands respect the signals in the file?). Both are needed, and neither alone is sufficient.

[Integration-architect review, Missed Opportunities bullet 1; Devil's advocate review, Recommendation #1, Off-Base Assumption #1]

### 6. All 12 functional requirements are satisfied

Integration-architect provides a complete FR-to-implementation mapping table covering FR-001 through FR-012 and SC-001 through SC-005. My review confirms satisfaction of the same requirements without a formal table. Neither review identifies a functional requirement that is unimplemented or incorrectly implemented.

The spec does what it says it does. The concerns from both reviews are about what the spec does not say, not about what it says incorrectly.

[Integration-architect review, FR-to-Implementation Mapping; Devil's advocate review, Executive Summary]
