# Cooperative Revision: functional-typing

**Spec**: 009-guided-execution
**Reviewer role**: Structural correctness and specification compliance
**Date**: 2026-03-22

---

## Recommendation Dispositions

### P1 #1 — Fix "Problem" label to "Mode" (SKILL.md line 1377)

**Original recommendation**: Change line 1377 from `Problem: {mode in plain language}` to `Mode: {mode in plain language}`.

**Disposition**: ACCEPTED, EXPANDED.

Integration-architect's cross-review (Tensions, item 1) agrees this is a genuine miss from their review and concurs with P1 priority. Devils-advocate's cross-review (Dangerous Contradictions, item 1) goes further: the label is not merely cosmetic but a consent flaw, because the summary never surfaces the problem definition from `problem.md` at all. Devils-advocate argues the summary should include both the problem statement and the mode.

I accept devils-advocate's escalation. Relabeling `Problem:` to `Mode:` is necessary but insufficient. FR-001 requires a "human-readable summary" for informed consent (spec.md line 27). The problem definition is the most fundamental input to the deliberation -- it is what is being deliberated. A user who confirms execution without seeing the problem statement is consenting to something they cannot fully evaluate. The fix should be: (1) relabel the field to `Mode:`, and (2) add a `Problem:` field that displays the first sentence or heading from `problem.md` (or "(hand-crafted config -- no problem.md)" when absent). This preserves the one-line-per-field summary structure while closing the information gap.

**Priority**: P1 (unchanged). The expansion adds one conditional line to the template; the structural risk remains low.

**Citations**: My review (Off-Base Assumptions, item 1; Actionable Recommendations, item 1). Devils-advocate cross-review of functional-typing (Dangerous Contradictions, item 1). Integration-architect cross-review of functional-typing (Tensions, item 1).

---

### P1 #2 — Guard `/conversus arbitrate` suggestion

**Original recommendation**: Gate the `/conversus arbitrate` suggestion behind implementation status, or add a parenthetical with a workaround.

**Disposition**: ACCEPTED, REFINED.

All three reviewers converge on this as the highest-priority issue. Integration-architect rates it P0 and recommends replacing the suggestion with actionable workaround guidance (integration-architect review, Actionable Recommendations, row 1). Devils-advocate confirms it breaks the guided flow (devils-advocate cross-review of functional-typing, Tensions, item 2) and locates the root cause in the spec itself -- FR-009 says "suggest `/conversus arbitrate`" without caveat.

Integration-architect's cross-review of functional-typing (Tensions, item 2) proposes the ideal resolution: replace the suggestion with the `arbiter:`-section workaround AND note that a dedicated `/conversus arbitrate` subcommand is planned. This combines an actionable path with honest expectation-setting.

I adopt this combined approach. The post-execution report at lines 1468-1469 and 1489 should read: "To resolve disputes, add an `arbiter:` section to `conversus.yml` and re-run `/conversus converge`. (A dedicated `/conversus arbitrate` subcommand is planned.)" This gives non-experts something they can do now while signaling the intended trajectory.

**Priority**: Elevated to P0 (accepting integration-architect's severity assessment). A dead-end in the guided flow for the primary persona is flow-breaking, not merely confusing.

**Citations**: My review (Off-Base Assumptions, item 2; Actionable Recommendations, item 2). Integration-architect review (Missed Opportunities, item 1; Actionable Recommendations, P0 row). Integration-architect cross-review of functional-typing (Tensions, item 2). Devils-advocate cross-review of functional-typing (Tensions, item 2). Devils-advocate review (Off-Base Assumptions, item 2).

---

### P2 #3 — Add prior context to pre-execution summary

**Original recommendation**: Add `Prior context: {paths}` to the summary template when `PRIOR_FILES` is non-empty.

**Disposition**: ACCEPTED, UNCHANGED.

Integration-architect's cross-review (Tensions, item 3) acknowledges this is valid but ranks it below the `--output` flag gap. Devils-advocate's cross-review (Tensions, item 1) strengthens the case: omitting prior context from the summary "directly undermines FR-001's 'human-readable summary' requirement" for informed consent. Devils-advocate notes that prior files "silently influence all agents" -- a meaningful information gap.

Integration-architect's silence on prior context (noted in my cross-review of integration-architect, Tensions, item 5) may reflect a judgment that prior files are an advanced feature. However, spec Constraint 2 (line 61) explicitly permits hand-crafted configs, which may include `prior:` sections. The informed-consent principle of FR-001/FR-002 does not carve out advanced features.

I maintain P2. The fix is a single conditional line in the template. It does not block any workflow but closes an information gap that could affect trust.

**Priority**: P2 (unchanged).

**Citations**: My review (Missed Opportunities, item 4; Actionable Recommendations, item 3). My cross-review of integration-architect (Tensions, item 5). Devils-advocate cross-review of functional-typing (Tensions, item 1).

---

### P2 #4 — Clarify dispute-parsing file target

**Original recommendation**: Specify `{output}/summary/final.md` as the file target at line 1464.

**Disposition**: ACCEPTED, UNCHANGED.

Integration-architect's cross-review (Tensions, item 4) agrees this is a documentation clarity improvement and calls it low-risk. Devils-advocate's cross-review (Tensions, item 3) raises the severity: an LLM agent executing the imprecise instruction could parse a per-round synthesis rather than `final.md`, especially in multi-round runs with multiple synthesis files. Devils-advocate argues this is more than documentation -- it is a correctness concern for agent-executed instructions.

I accept devils-advocate's point about fragility in agent execution contexts, but maintain P2. The Dispute-Parsing Subsystem (line 751) requires a path as input. The converge handler at line 1442 already references `{output}/summary/final.md` for display. Making line 1464 consistent with line 1442 is a one-line fix that eliminates ambiguity.

**Priority**: P2 (unchanged).

**Citations**: My review (Post-Execution Report section; Actionable Recommendations, item 4). Integration-architect cross-review of functional-typing (Tensions, item 4). Devils-advocate cross-review of functional-typing (Tensions, item 3).

---

### P3 #5 — Consider `--dry-run` for converge

**Original recommendation**: Allow `converge --dry-run` to display the pre-execution summary and exit without prompting.

**Disposition**: DEFERRED.

Both devils-advocate (Missed Opportunity 3 in devils-advocate review) and I identified this as a future enhancement. Integration-architect's cross-review (Tensions, item 5) confirms both reviewers classify it as out-of-scope. No cross-review escalates its priority.

The `--output` flag gap identified by integration-architect (integration-architect review, Missed Opportunities, item 2) is a more immediate ergonomic concern for the same audience. Dry-run can wait until the core guided flow is complete.

**Priority**: Deferred (deprioritized below new recommendations).

**Citations**: My review (Missed Opportunities, item 3). Devils-advocate review (Missed Opportunities, item 3). Integration-architect cross-review of functional-typing (Tensions, item 5).

---

## New Recommendations

### NEW-1: Add `--output <dir>` flag to converge handler (P1)

Integration-architect's review (Missed Opportunities, item 2) identifies that `define`, `interests`, and `mode` all accept `--output <dir>`, but `converge` does not. A user who ran the upstream pipeline with `--output my-delib/` cannot use converge without changing directories or moving files. This breaks cross-handler workflow continuity.

My cross-review of integration-architect (Tensions, item 2) acknowledges this is a legitimate ergonomic gap that my structural-correctness lens missed. Integration-architect rates it P1; I concur. The fix is straightforward: the converge handler should accept `--output <dir>` and use it as the working directory for config lookup, execution, and report output.

**Priority**: P1. Blocks a workflow that upstream handlers explicitly support.

**Citations**: Integration-architect review (Missed Opportunities, item 2). My cross-review of integration-architect (Tensions, item 2).

---

### NEW-2: Make delegation mechanism explicit (P2)

Devils-advocate's review (Off-Base Assumptions, item 5) raises a legitimate question: what does "delegate to `/conversus run`" mean in a SKILL.md context? The SKILL.md is an instruction set for an LLM agent, not a codebase with function calls. The agent must interpret "delegate" as "proceed to execute Run: Execution Step 1 through Step 5 using the parsed config."

My cross-review of devils-advocate (Tensions, item 3) concedes this is worth a one-line clarification, though I do not consider it blocking. The fragility concern is real in long-context LLM execution: if the agent loses context of the Run handler while executing the Converge handler, implicit delegation fails silently. An explicit statement -- "Delegation means: proceed to execute Run: Execution Step 1 through Step 5 in this document. No new skill invocation occurs." -- eliminates the ambiguity at zero structural cost.

**Priority**: P2. Documentation clarity that prevents a class of agent-execution failures.

**Citations**: Devils-advocate review (Off-Base Assumptions, item 5). My cross-review of devils-advocate (Tensions, item 3).

---

### NEW-3: Correct the Important Notes formula (P2)

Devils-advocate's review (Off-Base Assumptions, item 4) identifies a discrepancy between the Step 4 formula and the Important Notes simplified formula. My cross-review of devils-advocate (Dangerous Contradictions, item 1) demonstrates that the discrepancy is an arithmetic error in Important Notes, not in Step 4. The Important Notes expanded form `N + N*(N-1) + N + N + 1` simplifies to `N^2 + 2N + 1`, not the stated `N^2 + N + 1`. The simplified formula drops Phase 4 entirely.

The converge handler (line 1402) uses the Step 4 formula, which is structurally correct. The risk is that a spec reviewer or an agent reading Important Notes will use the wrong formula and report a false discrepancy -- exactly what happened in this review cycle. The correct fix is to update the Important Notes section to match Step 4, not the reverse.

**Priority**: P2. Does not affect the converge handler (which uses the correct formula) but prevents cross-document confusion.

**Citations**: Devils-advocate review (Off-Base Assumptions, item 4; Actionable Recommendations, item 5). My cross-review of devils-advocate (Dangerous Contradictions, item 1).

---

## Position Summary

The converge handler is a sound implementation of spec 009. All ten functional requirements are satisfied. The zero-new-engine-logic constraint is upheld. The handler is a pure UX wrapper: pre-flight (prerequisite check, staleness warning, summary, confirmation), flight (delegation to run), post-flight (report with interpretation and next steps).

The cooperative review process surfaced meaningful refinements that my initial review missed or underweighted:

1. **The "Problem" label issue is deeper than cosmetic** (devils-advocate). The summary omits the problem definition entirely, not just mislabels a field. The fix should add problem context to the summary, not merely relabel.

2. **The `/conversus arbitrate` dead reference is P0, not P1** (integration-architect). A dead-end in the guided flow for the primary persona is flow-breaking. The combined fix -- actionable workaround plus future-command note -- is the right approach.

3. **The `--output` flag gap is a real workflow break** (integration-architect). Cross-handler consistency is not optional when the upstream handlers establish a pattern the user relies on.

4. **The delegation mechanism should be explicit** (devils-advocate). In an LLM-executed instruction set, implicit cross-section references are fragile. A one-line clarification prevents a class of silent failures.

5. **The Important Notes formula has an arithmetic error** (devils-advocate identified the symptom; my cross-review located the actual bug). The converge handler uses the correct formula, but the inconsistency within SKILL.md should be fixed to prevent future confusion.

My initial review's FR-004 analysis correctly identified the four-case prerequisite routing as a completeness improvement, but integration-architect's cross-review rightly notes that the prescriptive routing is scoped to the guided-workflow path (when `conversus.yml` is absent), which neutralizes the concern about advanced users. Devils-advocate's challenge that the expansion conflicts with Constraint 2 does not hold: the routing only fires when the config is absent, and Constraint 2 protects users who have a config.

The revised recommendation set -- 5 original (one elevated, one expanded, one deferred) plus 3 new -- addresses the structural, integration, and correctness concerns surfaced across all three review perspectives.
