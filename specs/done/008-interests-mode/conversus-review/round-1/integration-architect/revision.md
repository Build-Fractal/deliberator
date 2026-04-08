# Integration Architect — Revised Review

**Spec**: `008-interests-mode`
**Original review**: `integration-architect/review.md`
**Revision date**: 2026-03-22

---

## Recommendation Dispositions

### R-1: Validate preset-backed agent roundtrip (was: Medium)

**Status**: Escalated to High.

Devil's advocate's cross-review correctly argues that Medium understates the severity (DA cross-review, Dangerous Contradictions #2). The post-write validation at SKILL.md lines 1263-1273 checks that each agent has `name` and `prompt` (or `preset`) but does not resolve the preset to verify the file exists on disk. Validation rule 7 (SKILL.md line 1271: "If `docs` paths are specified, they exist on disk") already establishes the pattern of path-existence checking at generation time. The same pattern must extend to preset paths.

The failure mode is concrete: a user runs `/conversus interests`, accepts a preset match, then runs `/conversus mode`. The generated `conversus.yml` passes all stated validation checks. Later, the preset file is moved or deleted. `/conversus run` fails with a resolution error that the user has no reason to anticipate because generation-time validation told them the config was valid.

**Revised recommendation**: Add preset file existence validation to the post-write check (SKILL.md ~line 1269). Validate that referenced preset files exist on disk at generation time, using the same existence-check pattern already applied to `docs` paths and `target` paths. Priority: High.

---

### R-2: Clarify target path handling when Source Documents is "(none)" (was: Medium)

**Status**: Retained at Medium, scope expanded.

Devil's advocate's cross-review (Tensions #4) correctly observes that the `(none)` sentinel is broader than my original framing. The sentinel is an ad-hoc convention from the define handler (SKILL.md line 891) with no formal definition. Both the interests handler (which reads Source Documents for the Problem Reference section) and the mode handler (SKILL.md line 1254) must handle it, but neither defines what it means -- they inherit it implicitly. A user editing `problem.md` by hand might write "none", "N/A", "TBD", or delete the section entirely. Only the exact string `(none)` triggers the special handling.

**Revised recommendation**: Define the `(none)` sentinel explicitly as a cross-handler convention. Add a note near the interests handler's problem.md reading logic and the mode handler's target mapping (SKILL.md ~line 1254) stating: "The sentinel value `(none)` in Source Documents means no source documents were provided. Treat any of `(none)`, empty list, or missing section as equivalent. Other text values (e.g., 'N/A', 'TBD') should be treated as literal paths and will fail the target existence check."

---

### R-3: Coordinate interest name validation across handlers (was: Low)

**Status**: Retained at Low, but devil's advocate's escalation is noted.

Devil's advocate's cross-review (Tensions #2) argues this triple-specification (`[a-z0-9][a-z0-9-_]*` at SKILL.md lines 964, 1268, and 198) is a design tension that worsens with each new handler. The point is valid: if the pattern ever changes, three sections must be updated. However, SKILL.md is a single file consumed by a single agent, not a distributed system with independent deployments. The maintenance cost is a single find-and-replace. The right fix is not centralizing the pattern (which would require cross-referencing that complicates the SKILL.md's linear reading model) but ensuring test coverage exercises the pattern in each handler.

**Revised recommendation**: Keep at Low. If a future spec adds additional handlers that also validate names, revisit centralization at that point.

---

### R-4: Consider adding `--dry-run` to mode handler (was: Low)

**Status**: Retained at Low.

Both cross-reviews endorsed this without challenge. Devil's advocate explicitly called it "a sensible suggestion" (DA cross-review, Safe Agreements #6). No change needed.

---

### Original finding: "No Off-Base Assumptions"

**Status**: Revised. Two reviewers correctly challenged this.

Functional-typing's cross-review (Dangerous Contradictions #2) identifies that the `Preset` field in the `interests.md` schema (SKILL.md line 1041) is absent from the spec's schema (spec.md lines 72-87). My original review noted the Preset field approvingly in the FR-006 mapping and the schema alignment table but never flagged the spec-implementation divergence, then declared "None identified" under Off-Base Assumptions. That was too strong.

I accept functional-typing's correction on the factual point: the implementation's output schema is a strict superset of the spec schema. However, I maintain my cross-review framing (integration-architect cross-review of functional-typing, Dangerous Contradictions #2): this is a spec omission, not implementation drift. FR-006 mandates preset support, and the data-flow from interests to config requires the Preset field to carry the preset reference. Removing the field to "align with spec" would break the pipeline. The correct resolution is updating the spec schema, not the implementation.

**Revised position**: One off-base assumption identified -- my original review's claim of zero off-base assumptions was itself overconfident. The implementation makes one assumption beyond the spec: that the `interests.md` schema should include a `Preset` field. That assumption is correct and necessary, but it IS an assumption beyond the spec text.

---

### Original finding: FR-007 "Satisfied"

**Status**: Downgraded to "Partially Satisfied." Functional-typing's challenge is valid.

Functional-typing's cross-review (Dangerous Contradictions #1) identifies that my review marked FR-007 as "Satisfied" while the spec's decision matrix (spec.md line 52) defines a fifth row: `| ambiguous | cooperative | Low -- present alternatives |`. SKILL.md replaces this with heuristic detection (line 1145) routing to signal-based inference (lines 1147-1156) and mixed-signal handling (lines 1158-1176). The heuristic path can recommend any mode depending on signal density -- it does not guarantee the spec's prescribed `cooperative` default.

I originally acknowledged the heuristic path in my review's Missed Opportunity #3 ("Heuristic detection signals are documented but not structured") but never connected that observation back to the FR-007 verdict. Functional-typing is right that this disconnect is a gap in my analysis.

However, I maintain my cross-review position (integration-architect cross-review of functional-typing, Dangerous Contradictions #1) that the SKILL.md behavior is intentionally more correct than a static default. A genuinely ambiguous problem with zero detectable signals benefits more from "Which approach fits your situation better?" than from silently assigning `cooperative` at Low confidence. The spec's intent (line 103: "Must NOT require game theory knowledge") is better served by asking the user than by defaulting.

**Revised position**: FR-007 is partially covered. The four concrete rows are correct. The fifth row is functionally replaced, not omitted. The resolution should be a spec amendment that replaces the `ambiguous` row with: "When the problem type is ambiguous or unset, use heuristic mode detection. If no mode has detectable signals, present the top candidates and ask the user to choose." This aligns the spec to the SKILL.md's more user-interactive behavior rather than adding a silent fallback.

---

## New Recommendations

### N-1: Add explicit handling for `[CLARIFY: ...]` tags in the Type field (Priority: Medium)

Functional-typing raises this (their review, Missed Opportunities #4, lines 196-199) and their cross-review confirms it as a gap I missed. The define handler (SKILL.md ~line 845) can produce `[CLARIFY: best-guess-type -- reason]` in the Type field. The interests handler's calibration table (SKILL.md lines 957-962) lists four concrete types with no instruction for a CLARIFY-tagged Type. The mode handler's heuristic detection (SKILL.md line 1145: "When the problem type is unset or ambiguous") covers the mode path, but the interests handler has no equivalent fallback.

**Recommendation**: Add a note to the Interest Generation section (SKILL.md ~line 955): "If the Type field contains a `[CLARIFY: ...]` tag, extract the best-guess type from the tag text and use it for prompt calibration. Warn the user: 'The problem type is unconfirmed. Using {best-guess-type} for interest calibration. Run `/conversus define` to confirm the type.'"

This pairs with the mode handler's heuristic detection to provide consistent handling of ambiguous types across both handlers.

---

### N-2: Specify behavior when `problem.md` has `status: draft` (Priority: Medium)

Devil's advocate raises this (DA review, recommendation 6) and my cross-review of devil's advocate (Safe Agreements #4) confirms it as an unambiguous gap. The define spec explicitly says: "whether downstream commands treat `draft` as blocking is defined by those commands' specs" (SKILL.md line 889). Spec 008 never exercises that option. This means the behavior when a user runs `/conversus interests` on a draft `problem.md` is undefined and implementation-dependent.

**Recommendation**: Add a note to the interests handler's prerequisite check (SKILL.md ~line 941): "If `problem.md` has `status: draft`, warn: 'problem.md is marked as draft with {count} unresolved [CLARIFY:] tags. Interest generation will use the current content, but results may change after clarifications are resolved.' Proceed without blocking." This is consistent with the informational warning pattern used throughout the guided workflow (e.g., staleness warning, NEEDS DOCS warning) and avoids blocking users while making the draft state visible.

---

### N-3: Relocate agent-launch cost estimate to mode confirmation (Priority: Low)

Devil's advocate recommends adding an agent-launch cost estimate at interest confirmation time (DA review, recommendation 3). The concern is valid -- SKILL.md lines 1304-1306 document the launch formula (N^2 + N + 1 per round) and 5 agents produce 31 launches per round, but this information is never surfaced in the guided workflow. However, my cross-review of devil's advocate (Tensions #3) identifies that interest confirmation time is premature: the mode is not yet selected, and mode affects the launch structure (red-blue has asymmetric counts).

**Recommendation**: Add the agent-launch estimate to the mode handler's confirmation display (SKILL.md ~line 1203), where both agent count and mode are known. After "Agents: {count} (from interests.md)", add: "Estimated launches per round: {N^2 + N + 1} (based on {count} agents in {mode} mode)." This gives users cost visibility at the decision point where they can still cancel or reduce agent count.

---

## Position Summary

My original review correctly verified that all 13 functional requirements have traceable implementations, all five success criteria are achievable, the dispatch table and prerequisite routing are correctly wired, and the generated conversus.yml schema aligns field-by-field with the run engine. These findings stand unchallenged across all three reviewers.

The cross-review process surfaced three corrections to my original analysis:

1. **FR-007 was overstated.** I marked it "Satisfied" when the spec's `ambiguous` row is not preserved. Functional-typing is right that this is a partial coverage gap. I maintain that the SKILL.md behavior (heuristic detection + user choice) is superior to the spec's static `cooperative` default, but the two documents must agree. The spec should be amended to match the SKILL.md's interactive approach.

2. **"No off-base assumptions" was too strong.** The `Preset` field in the `interests.md` schema is a necessary addition that the spec schema omits. It is the right addition, but it is an addition. The spec schema should be updated to include it.

3. **Preset validation severity was understated.** R-1 should be High, not Medium. A config that passes all generation-time validation checks but deterministically fails at run time due to a missing preset file is a validation gap, not an enhancement opportunity.

The cross-review process also surfaced three gaps I did not originally identify: `[CLARIFY:]` tag handling in the interests handler, undefined `status: draft` behavior, and agent-launch cost visibility. All three are addressed in the New Recommendations section.

The revised assessment is that the implementation is substantially correct and faithful to the spec, with one partial-coverage finding (FR-007 ambiguous row), one spec-update needed (Preset field in interests.md schema), one validation gap to close (preset existence at generation time), and three operational notes to add (CLARIFY tag handling, draft status behavior, launch cost estimate). None of these are blocking defects; all are resolvable within the current architecture.
