# Devil's Advocate Review: 009-Guided-Execution (Round 2)

**Reviewer**: devils-advocate
**Spec**: `009-guided-execution`
**Phase**: Round 2 of 2
**Date**: 2026-03-22
**Prior artifacts**: Round 1 synthesis (`final.md`), arbiter resolution (`resolution.md`), all Round 1 review/revision/dispute artifacts.

---

## Preamble: Engagement with Prior Synthesis and Arbitration

Round 1 produced a strong synthesis. Eight recommendations converged fully, four disputes remain on scope and priority rather than on diagnosis or fix direction. The arbiter's advisory opinions are well-reasoned and largely align with the 2-1 majorities I was part of. I do not reverse any concessions from Round 1 -- my withdrawal of content hashing, my acceptance of mtime as a best-effort heuristic for spec 009, my concession that the formula root cause was an algebra error (not iteration handling), and my softened framing on the speckit integration all stand.

This round engages with the synthesis and arbiter opinions to sharpen the remaining disputes, identify any gaps the synthesis itself introduced, and confirm that the converged recommendations remain sound after a second reading of the target files.

---

## Remaining Disputes: Refined Positions

### Dispute 1: Problem statement inclusion in the pre-execution summary

**Round 1 position**: The pre-execution summary should include a `Problem:` field sourcing the problem definition from `problem.md` alongside the relabeled `Mode:` field. A user who confirms execution without seeing what problem is being deliberated is consenting to something they cannot evaluate.

**Arbiter opinion**: The 2-1 majority position is stronger. The problem definition is "categorically different" from templates and constitutions. The arbiter recommends applying the label fix at P1 and treating the problem-statement addition as P2 -- "not deferred indefinitely, but sequenced after the label fix."

**Round 2 position**: I accept the arbiter's sequencing proposal. The label fix ships at P1. The problem-statement addition ships as P2 immediately after. This is a genuine bridge between my position and integration-architect's scope concern -- the problem-statement addition is not smuggled into the label fix, but it is also not deferred to some unspecified future.

However, I want to sharpen why the arbiter's reasoning is correct and integration-architect's slippery-slope objection fails. Integration-architect argues that adding the problem statement "without addressing the others creates an inconsistency in the level of detail." The arbiter correctly identifies that the problem statement is not comparable to templates, constitutions, or other config dimensions. Here is the structural argument: the pre-execution summary already discloses mode, agents, targets, rounds, iterations, launch count, and arbiter configuration. Every one of these is an instrumentality -- they describe how the deliberation will run. The problem statement is the only input that describes what the deliberation is about. Disclosing seven instrumentalities and zero purposes is not "lossy by design" -- it is a category error in the disclosure model. Templates describe output format (visible in results). Constitutions describe meta-rules (visible in synthesis structure). The problem statement describes the purpose (invisible in output unless the reader already knows it). The slippery slope from "add the problem" to "add everything" does not exist because the problem is the only undisclosed item in the "purpose" category.

I do not escalate beyond P2 for the problem-statement addition. The arbiter's P2 recommendation is the right landing point. But I want the record to reflect that this is not a marginal enhancement -- it is the most structurally important missing field in the consent surface.

---

### Dispute 2: Prior context disclosure priority -- P2 vs. P3

**Round 1 position**: P2. Prior files silently influence every agent. The informed-consent principle does not carve out advanced features.

**Arbiter opinion**: P2 is more defensible. Integration-architect's slippery-slope argument (if prior files, then templates, then constitutions) does not hold because prior files are "the only configured input that influences all agents and is absent from the summary." Templates and constitutions are already visible in results or synthesis structure.

**Round 2 position**: I maintain P2, aligned with the arbiter. I do not have new arguments beyond what the arbiter articulated. The arbiter's analysis is the strongest version of the case: prior files are unique in being both (a) invisible in the output and (b) influential over every agent. Templates are visible in output structure. Constitutions are visible in synthesis process. Prior files inject substantive content that biases agents' starting positions with no trace in the deliverables. The user discovers their influence only by reading the config YAML, which the entire guided workflow exists to make unnecessary.

Integration-architect's user-awareness assumption -- "the person who configured it probably knows" -- was already refuted in Round 1 by the inherited-config scenario that Constraint 2 explicitly enables. I will not relitigate this. P2 is the correct priority. The practical difference from P3 is negligible in implementation cost, but the signal matters: P2 says "this is a real gap in the consent surface," P3 says "this is a nice-to-have for advanced users." The former is the accurate characterization.

---

### Dispute 3: Mtime staleness false-positive documentation

**Round 1 position**: The SKILL.md should include one sentence noting that the mtime warning may fire after git operations. No reviewer opposes this. It fell through the consolidation process.

**Arbiter opinion**: Adopt as P3. "The fact that no reviewer opposes it is sufficient basis for inclusion." The cost-benefit analysis is "unambiguous: zero implementation cost, meaningful UX improvement for a known false-positive path."

**Round 2 position**: I accept the arbiter's P3 recommendation. This is the least consequential of my remaining disputes, and P3 is an appropriate priority for a one-sentence documentation addition that no one contests.

I want to note one thing the arbiter got exactly right that the synthesis underweighted: the false-positive scenario occurs at the consent surface -- the one moment the guided flow asks the user to trust it. A user who sees "Your interests have been modified since conversus.yml was generated" when they changed nothing (because `git stash pop` updated timestamps) will question the tool's reliability at precisely the moment they need confidence. The mtime heuristic is acceptable. Undocumented false positives in that heuristic are not. One sentence fixes this.

This dispute is resolved from my perspective. P3, adopted. I will not raise it again.

---

### Dispute 4: Important Notes formula correction priority -- P1 vs. P2

**Round 1 position**: I aligned with the fix direction without taking a strong position on P1 vs. P2.

**Arbiter opinion**: P1. "An internal contradiction in an instruction document for automated agents is functionally closer to a code bug than a documentation typo." The tiebreaker is the document's audience -- SKILL.md is read by LLM agents executing the pipeline, and an agent referencing Important Notes during execution planning will compute wrong estimates.

**Round 2 position**: I now explicitly align with integration-architect and the arbiter at P1. The arbiter's reasoning persuades me on a point I did not fully appreciate in Round 1: SKILL.md is not documentation in the traditional sense. It is an executable instruction set for LLM agents. An arithmetic error in an executable instruction set is a bug, not a documentation issue. The fact that the converge handler happens to reference the correct formula (Step 4) rather than the incorrect one (Important Notes) is fortunate but does not change the nature of the error.

Moreover, this review cycle itself is empirical evidence. I identified the discrepancy in Round 1 but was led astray by the wrong formula -- I speculated about iteration handling when the real cause was a dropped term. The error actively interfered with my analysis. An error that misleads its own reviewers has demonstrated harm, not hypothetical harm. P1 is correct.

This shifts the Round 1 dispute from 1-1-neutral (integration-architect P1, functional-typing P2, devils-advocate unstated) to 2-1 in favor of P1 (integration-architect + devils-advocate P1, functional-typing P2). I consider this dispute resolved.

---

## Engagement with Converged Recommendations

I have re-read the target files (spec.md and SKILL.md lines 1326-1545) against the eight converged recommendations from Round 1. All eight remain sound. I have no objections to any converged item and no basis to reopen them. Specific notes on three:

### 1. The `/conversus arbitrate` dead reference fix (P0) is correctly scoped

Re-reading the post-execution report (SKILL.md lines 1466-1489), the `/conversus arbitrate` reference appears in three locations: line 1469 (disputes section), line 1488 (next steps, disputes remain without arbiter), and line 1489 (same). The converged fix -- replace with `arbiter:` section workaround plus planned-command note -- must hit all three locations. The synthesis correctly identifies this. The spec's FR-009 text also needs updating to avoid prescribing a specific unimplemented subcommand. This is comprehensive and correct.

### 2. The delegation semantics clarification (P2) addresses a real LLM execution risk

Re-reading line 1426 ("Delegate to `/conversus run` using the `conversus.yml` in the working directory"), I confirm my Round 1 assessment: this is genuinely ambiguous in a SKILL.md context. The converged fix -- "Proceed to Run: Execution Step 1 through Step 5 using the config already parsed in the pre-execution summary. Do not re-invoke `/conversus run` as a separate skill invocation -- continue within the current conversation." -- is precise and eliminates the ambiguity. I note that the phrase "config already parsed in the pre-execution summary" also serves an efficiency purpose: it tells the agent not to re-parse `conversus.yml`, avoiding redundant work in the context window.

### 3. The "What to Expect" narrative (P2) must not become a process tutorial

The converged recommendation adds a brief process explanation after the launch estimate. Re-reading the pre-execution summary template (lines 1374-1393), I want to flag a scope risk: the narrative should be exactly one or two sentences, not a multi-paragraph tutorial on the conversus pipeline. The converged wording ("Each agent reads the target documents and writes a review. Agents then cross-review each other's work, revise, and a synthesis is produced.") is the right length. The implementation should resist the temptation to elaborate. SC-004 prohibits a YAML dump; the same principle should prohibit a process dump. The current converged wording is good. I flag this only to prevent scope creep during implementation.

---

## Engagement with Arbiter's Considerations

### Consideration 1: The consent-surface design question is broader than spec 009

The arbiter proposes a principled selection criterion for summary fields: "disclose any configured input that (a) influences agent output and (b) is not visible in the results." This is a useful framework. Under this criterion:

- Problem statement: influences all agents, not directly visible in output structure. **Include.**
- Prior files: influence all agents, invisible in results. **Include.**
- Templates: visible as output structure. **Exclude.**
- Constitutions: visible as synthesis rules. **Exclude.**
- Iteration count: already disclosed in the summary. **Already included.**

This criterion would resolve Disputes 1 and 2 from Round 1 and provide a framework for future summary-field decisions. I endorse this as a design principle for a future spec amendment. However, I note it does not need to be formalized to resolve the current disputes -- the problem statement and prior files both satisfy the criterion under any reasonable reading. The arbiter's framework validates the 2-1 majority positions on both disputes. It is useful but not necessary.

### Consideration 4: Priority disputes as calibration signals

The arbiter frames P-level disagreements as "calibration signals rather than failures to converge." I agree. My Round 1 disputes were all refinements, not structural objections. The fact that three reviewers with different analytical lenses arrive at the same diagnosis and fix direction for every item -- differing only on severity weighting -- is evidence that the cooperative process works. The remaining priority disputes are correctly characterized as product-level judgment calls, not technical disagreements.

### Consideration 5: The "no new execution logic" constraint held

The arbiter notes this constraint "survived through adversarial review." Confirmed. I tested it explicitly in Round 1 (checking for phase orchestration, agent management, output file creation, and schema extension). The converge handler is a pure UX wrapper. This is the spec's most important architectural property and it is verified.

---

## New Observations from Second Reading

### 1. The converge handler's error path for config parsing failures is underspecified

Re-reading SKILL.md line 1370: "Parse the configuration using the same schema defined in Run: Execution Step 1. If parsing fails, report the validation error and stop." This is the only error handling in the converge handler, and it is a single sentence. The converged P2 recommendation on failure recovery addresses mid-execution failures (when the delegated run fails), but the pre-execution parsing failure also needs attention.

What does "report the validation error" mean for a non-expert? If the user hand-crafted `conversus.yml` with a typo (e.g., `mode: cooperativ`), the raw schema validation error may be opaque. The failure recovery recommendation should be expanded to cover both pre-execution parsing failures (translate schema validation errors to plain language, suggest what to fix) and mid-execution run failures (translate engine errors, state that re-run is required).

This is not a new recommendation -- it is a scope refinement of the converged P2 failure recovery item. The synthesis focused on mid-execution failures; pre-execution parsing failures are the same category of "translate errors for non-experts" and should be addressed by the same fix.

### 2. The post-execution report's conditional speckit suggestion has an audience mismatch

Re-reading SKILL.md lines 1504-1507, the speckit suggestion fires for cooperative mode "regardless of dispute status." The converged P2 recommendation adds spec acknowledgment for this cross-tool next step. I do not dispute the recommendation.

However, on second reading, I notice the suggestion fires even when all disputes have converged and the deliberation produced a clean consensus. In that case, the next steps read:

```
- Review the synthesis: {output}/summary/final.md
- No further deliberation needed
- To apply changes: /speckit.specify --input {output}/summary/final.md
```

The "No further deliberation needed" line followed immediately by "To apply changes" is well-structured -- it says the deliberation is done, here is how to act on it. This is good UX. No change needed. I retract this observation; it is not a gap.

### 3. Arbiter influence field in pre-execution summary may confuse non-experts

Re-reading SKILL.md lines 1390-1391: `Arbiter: {arbiter name} (trigger: {trigger}, timing: {timing}, influence: {influence})`. The terms "trigger," "timing," and "influence" are engine-internal concepts defined in spec 001. A non-expert following the guided workflow may not understand what "trigger: dispute-threshold, timing: post-round, influence: advisory" means.

This is a minor concern and I do not elevate it to a recommendation. The arbiter disclosure is conditional (only shows if configured), and a user who configured an arbiter through the guided workflow will have encountered these terms during mode configuration. The issue only arises for users who inherit a hand-crafted config with an arbiter -- a narrow audience. I flag it for the record but do not dispute the current design.

---

## Summary of Round 2 Position

### Concessions maintained from Round 1

All Round 1 concessions stand:
- Content hashing belongs in spec 008, not spec 009. Withdrawn.
- Mtime is an acceptable best-effort heuristic for spec 009. Accepted.
- The formula root cause is an algebra error in Important Notes (dropped Phase 4 term), not an iteration-handling ambiguity. Accepted.
- The speckit integration is spec-underauthorized rather than spec-drifted. Softened framing accepted.
- The FR-004 sub-case expansion is scoped to the guided-workflow path (when `conversus.yml` is absent) and does not conflict with Constraint 2. Accepted.

### Dispute resolutions in Round 2

Two disputes move toward resolution:

1. **Dispute 3 (mtime false-positive documentation)**: Resolved. I accept P3 per the arbiter. One sentence, zero cost, no opposition. This should be adopted.

2. **Dispute 4 (formula fix priority)**: I now explicitly support P1, aligning with integration-architect and the arbiter. SKILL.md is an executable instruction set, not traditional documentation. An arithmetic error in it is a bug. The error demonstrably misled this review cycle. The dispute shifts to 2-1 in favor of P1.

### Disputes maintained in Round 2

Two disputes remain, both narrowed:

1. **Dispute 1 (problem statement inclusion)**: I accept the arbiter's P2 sequencing. Label fix at P1, problem-statement addition as immediate P2 follow-up. The gap is real, the fix is proportionate, and the arbiter's distinction between "purpose" and "instrumentality" is the correct framing. Integration-architect's slippery-slope objection does not hold because the problem statement is categorically different from the config dimensions it is compared to.

2. **Dispute 2 (prior context disclosure priority)**: I maintain P2, aligned with functional-typing and the arbiter. The arguments are fully developed in Round 1 and the arbiter's opinion. I do not relitigate.

### New observation (not a new recommendation)

The converged P2 failure recovery recommendation should be scoped to cover both pre-execution parsing failures and mid-execution run failures. Both are instances of "translate errors for non-experts." This is a scope refinement, not a new item.

### Consolidated position

The spec and its SKILL.md implementation are sound. The converge handler is a well-designed UX wrapper that upholds the zero-new-engine-logic constraint. The Round 1 synthesis produced a comprehensive and actionable revision plan. The eight converged recommendations should be implemented as specified. The four Round 1 disputes are narrowing: two are resolved in this round (Dispute 3 resolved at P3, Dispute 4 resolved at P1), and two remain as product-level judgment calls where the 2-1 majority positions (supported by the arbiter) should prevail.

The spec is ready for implementation.

---

## Updated Recommendation Table (devils-advocate perspective, Round 2)

| Priority | Recommendation | Status |
|----------|---------------|--------|
| **P0** | Replace `/conversus arbitrate` dead reference with actionable workaround + planned-command note | Consensus (Round 1) |
| **P1** | Add `--output <dir>` flag to converge handler | Consensus (Round 1) |
| **P1** | Fix "Problem" label to "Mode" at SKILL.md line 1377 | Consensus on label fix (Round 1) |
| **P1** | Fix Important Notes formula arithmetic (lines 1517-1525) | Was disputed; now 2-1 for P1 (Round 2) |
| **P2** | Add problem statement to pre-execution summary | Was disputed; arbiter recommends P2 sequencing. 2-1 majority + arbiter support. |
| **P2** | Document failure recovery position (cover both parsing and mid-execution failures) | Consensus (Round 1); scope refinement in Round 2 |
| **P2** | Make delegation semantics explicit in Execution section | Consensus (Round 1) |
| **P2** | Add "What to Expect" narrative to pre-execution summary | Consensus (Round 1) |
| **P2** | Specify dispute-parsing file target as `{output}/summary/final.md` | Consensus (Round 1) |
| **P2** | Add spec acknowledgment for cross-tool next steps (speckit) | Consensus (Round 1) |
| **P2** | Add prior context disclosure to pre-execution summary | Was disputed P2/P3; I maintain P2. 2-1 + arbiter. |
| **P3** | Document mtime staleness false-positive limitation | Resolved at P3 (Round 2); unopposed. |
| **Deferred** | `--dry-run` capability for converge | Consensus (Round 1) |
| **Withdrawn** | Content hashing for staleness (belongs in spec 008) | Consensus (Round 1) |
| **Withdrawn** | Extend staleness check to `problem.md` (belongs in spec 008) | Consensus (Round 1) |
