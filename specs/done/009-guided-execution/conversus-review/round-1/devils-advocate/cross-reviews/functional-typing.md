# Cross-Review of functional-typing

**Cross-reviewer**: devils-advocate
**Reviewing**: functional-typing's review of spec 009-guided-execution
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. The "Problem" label mislabeling finding is correct but undersells the structural risk

functional-typing identifies that line 1377 labels its field `Problem:` but fills it with the mode (Off-Base Assumptions, item 1; Actionable Recommendation P1). This is accurate. However, the review treats it as a cosmetic labeling issue -- "a one-line fix that eliminates confusion."

It is more than cosmetic. The pre-execution summary is the single point where a non-expert decides whether to spend tokens. If the first field says "Problem: Find common ground" the user reads that as a problem statement, not a mode. They may believe the system has summarized their `problem.md` content and already trust the summary -- when in fact the summary never surfaces the problem definition at all. This is a consent flaw, not a label flaw. The user is confirming execution based on a summary that omits the most important input (what problem is being deliberated). functional-typing's P1 recommendation to relabel it `Mode:` fixes the label but does not fix the omission. The summary should include both: the problem statement from `problem.md` and the mode.

### 2. The FR-004 expansion is endorsed too easily

functional-typing's verdict on FR-004 is "Satisfied with expansion" -- the two extra sub-cases (interests-without-problem, problem-without-interests) are called "a well-motivated completeness improvement." I disagree with characterizing unspec'd behavior as harmless.

The sub-case at SKILL.md line 1344-1346 ("interests.md exists but problem.md does not") routes to `/conversus define` -- the full define workflow. But the spec's constraint at line 61 says converge "works with a hand-crafted conversus.yml." A user who hand-crafted `interests.md` without a `problem.md` (because they do not use the define workflow) is told to go through define anyway. The functional-typing review acknowledges this as a "minor tension" in Off-Base Assumptions item 3 but contradicts itself by blessing the same routing as a "well-motivated completeness improvement" in the FR-004 verdict. Either the extra routing is benign or it conflicts with the hand-crafted-config constraint. It cannot be both.

The spec intentionally underspecifies the intermediate states (both exist, neither exists). The SKILL.md fills the gap, which is fine -- but the review should flag that the fill conflicts with the spec's own constraint rather than approving it as a "completeness improvement."

### 3. The formula discrepancy is not identified

functional-typing's review does not mention the agent launch formula discrepancy between Step 4 (line 315) and Important Notes (lines 1517-1518). This is the most dangerous omission in the review.

Step 4 formula for N=3, iterations=1: `per_round_agents = 3 + 1*(3*2 + 3) + 3 + 1 = 16`. Important Notes (line 1519): "For 3 agents without arbiter: 13 total agent launches across 5 sequential phases." The simplified formula `N^2 + N + 1 = 13` omits Phase 4's N agents from the count. The discrepancy is 3 agents (23% of the total for N=3).

The converge handler (line 1402) explicitly says it uses the Step 4 formula. It will show "16" to the user. The Important Notes (which a spec reviewer, or an agent reading the full SKILL.md, will also reference) says "13." A review focused on "structural correctness and specification compliance" should have caught that the converge handler references a formula that disagrees with another section of the same document.

functional-typing's review item 4 in the Zero New Engine Logic Assessment actually says: "Item 4 reuses the formula from Run Step 4 (line 315)" -- confirming they read the formula -- but never cross-checks it against the Important Notes. This is a verification gap, not a disagreement about severity.

---

## Tensions

### 1. Scope of "fully satisfied" verdicts vs. missed opportunities

functional-typing gives "Fully satisfied" verdicts to all ten FRs, then lists four "Missed Opportunities" that describe significant gaps (no validation warning preview, no cost/time estimation, no dry-run, no prior context disclosure). There is a tension between declaring full compliance and then identifying material gaps in the same review.

For example, Missed Opportunity 4 (no prior context in pre-execution summary) directly undermines FR-001's "human-readable summary" requirement. If `prior:` files silently influence all agents and the user is not told about them, the summary is incomplete for informed consent. functional-typing correctly identifies this gap but does not downgrade FR-001 from "Fully satisfied" to something like "Satisfied with caveat." The review structure creates a reading where everything passes and the missed opportunities feel advisory, when at least one of them (prior context omission) is arguably a compliance gap.

My own review takes a harder position: the pre-execution summary's omission of prior context and its meaningless launch count (without time/cost framing) make the summary inadequate for SC-001's non-expert persona. We agree on the facts but disagree on whether they constitute compliance gaps or enhancement suggestions.

### 2. The `/conversus arbitrate` dead-end is P1 vs. documentation

functional-typing flags that `/conversus arbitrate` does not exist yet and the post-execution report routes non-experts to a dead end (Off-Base Assumptions, item 2). This is correctly identified and matches my own review's concern about the prerequisite chain. However, functional-typing's recommendation is to either gate the suggestion or add a parenthetical "(coming soon)."

I would go further: the spec itself (FR-009) says "suggest `/conversus arbitrate`" without any caveat that this command does not exist. This is a spec-level gap, not just an implementation concern. functional-typing's review correctly identifies the symptom but locates the fix in the SKILL.md when the root cause is in the spec. If the spec says to suggest a non-existent command, the implementation is technically compliant -- the fix belongs in the spec, not just the handler.

### 3. Dispute-Parsing Subsystem file target ambiguity -- severity difference

functional-typing identifies that the converge handler's dispute-parsing instruction (line 1464) does not specify which file to parse (Actionable Recommendation P2 item 4). The review concludes "this is a documentation clarity issue rather than a functional bug" because `{output}/summary/final.md` is the correct file in both single-round and multi-round cases.

This is more fragile than functional-typing suggests. The Dispute-Parsing Subsystem (line 751) takes "Path to a synthesis file" as input. The converge handler says "Check the run engine's output" but does not pass a path. An LLM agent executing this instruction could parse the wrong file -- for instance, a per-round synthesis from round 2 rather than `final.md`, especially in multi-round runs where multiple synthesis files exist in the output tree. The distinction between "documentation clarity issue" and "functional bug" depends on whether you trust the executing agent to infer the correct file. For a spec whose target audience is non-expert users (and therefore likely non-expert orchestrating agents), explicit is safer.

### 4. The speckit integration is unaddressed

functional-typing's review does not mention the `/speckit.specify --input` next step at SKILL.md lines 1504-1507. My review flags this as spec drift -- cross-tool integration behavior that appears only in the SKILL.md handler and is not authorized by any FR in spec 009. This is a notable gap in a review focused on "structural correctness and specification compliance." If the review's scope includes checking that the implementation does not exceed the spec, undocumented integrations should be flagged.

---

## Safe Agreements

### 1. Zero new engine logic constraint is upheld

Both reviews agree that the zero-new-engine-logic constraint (FR-006, FR-007) is fully satisfied. functional-typing provides a thorough verification in the "Zero New Engine Logic Assessment" section, checking for absence of phase orchestration, agent management, and output file creation. My review concurs: "Zero new engine logic is the correct constraint." No tension here.

### 2. FR-002 and FR-003 are correctly implemented

Both reviews agree that user confirmation (FR-002) and decline routing (FR-003) are cleanly implemented. functional-typing notes the "Cancel entirely" addition as a reasonable UX enhancement. My review does not challenge these FRs. The language in the SKILL.md exactly mirrors the spec requirement.

### 3. Staleness detection is mtime-based and fragile

functional-typing calls FR-005 "Fully satisfied" (the implementation matches the spec). My review calls the underlying mechanism fragile (git operations, editor autosaves trigger false positives). These are compatible positions: the implementation satisfies what the spec requires, but the spec requires something fragile. We agree on the facts; functional-typing assesses against the spec text, I assess against real-world behavior. Both assessments are valid in their respective frames.

### 4. Post-execution report structure exceeds the spec requirement

Both reviews agree that FR-008 through FR-010 are satisfied, and that the post-execution report adds useful structure beyond the minimum (mode-specific interpretation guidance, conditional arbiter information, outcome-based next steps). functional-typing's detailed mapping of report sections to FR requirements is thorough and I have no disputes with the line-level analysis.

### 5. The "Cancel entirely" addition to FR-003 is appropriate

functional-typing notes that the SKILL.md adds "Cancel entirely" as a third option to the decline routing (FR-003 specifies routing to interests or mode). Both reviews treat this as a reasonable UX addition that does not contradict the spec. Agreed -- the spec says "route them to the appropriate prior step" and cancellation is a valid routing outcome.

### 6. Pre-execution summary quality is generally high

Both reviews agree that the plain-language mode explanations (lines 1397-1400), one-sentence agent perspective summaries, and launch estimate are well-designed relative to the spec's expectations. The disagreements are about what the summary omits (prior context, cost framing, problem definition), not about the quality of what it includes.
