# Cross-Review: Devil's Advocate Review of 009-Guided-Execution

**Reviewer**: integration-architect
**Reviewing**: devils-advocate Phase 1 review
**Grounded in**: spec.md, SKILL.md, integration-architect review

---

## Dangerous Contradictions

### 1. Staleness detection: we diagnose the same disease but prescribe incompatible cures

Devil's advocate (Off-Base Assumption #1, Rec #3) proposes replacing mtime-based staleness with content hashing -- storing a hash of `interests.md` inside `conversus.yml` at generation time. My review (Missed Opportunity #4) proposes extending the existing mtime comparison to also cover `problem.md`. These are not additive -- they conflict on the mechanism.

If we adopt content hashing (devil's advocate), extending the comparison to `problem.md` (my review) means the mode handler must also compute and store a hash of `problem.md` inside `conversus.yml`. This adds two hash fields to the config schema, which violates spec 009's constraint that converge "Must NOT add execution logic" and must use "the same schema defined in Run: Execution Step 1" (SKILL.md line 1370). Schema changes to `conversus.yml` belong in spec 008 (mode handler), not spec 009 (converge handler). Both reviews conflate a spec-008 concern with a spec-009 concern.

Devil's advocate is right that mtime is fragile (git operations, editor autosaves). My review is right that one-directional staleness misses `problem.md` drift. But the fix for both belongs in spec 008's config generation, where the mode handler can embed provenance metadata (hashes, source paths) into `conversus.yml`. The converge handler should consume that metadata, not compute it.

**Resolution**: Staleness is a spec 008 problem. Spec 008's mode handler should embed content hashes of both `problem.md` and `interests.md` into `conversus.yml` at generation time. The converge handler reads those hashes and compares. Neither review correctly scoped the fix -- both placed it in the wrong spec.

### 2. The `/conversus arbitrate` dead reference: we agree on the problem but propose incompatible fixes

Devil's advocate (Rec #4, Missed Opportunity #4) says to either remove the speckit integration from the SKILL.md or add it to the spec. My review (P0 recommendation) says to replace the `/conversus arbitrate` suggestion with actionable workaround guidance. But devil's advocate does not flag `/conversus arbitrate` itself as a dead reference -- the recommendation at #4 is about the `/speckit.specify` cross-tool integration, not about `arbitrate`.

However, devil's advocate's Rec #6 says to "make the delegation mechanism explicit" and Rec #2 says to "document the failure recovery position." My P0 recommendation says to replace `/conversus arbitrate` suggestions with manual workaround guidance. These point in different directions: devil's advocate is comfortable keeping the `arbitrate` reference and adding documentation around it; my review says the reference itself is the problem because it produces a dead end for the target persona.

The dispatchtable (SKILL.md line 34) unambiguously lists `arbitrate` as "not yet implemented." A non-expert who reaches the post-execution report with unresolved disputes, follows the `/conversus arbitrate` suggestion, and hits "Unknown subcommand: 'arbitrate'" has been failed by the guided flow. This is not a documentation problem -- it is a routing problem.

**Resolution**: My P0 recommendation stands. The post-execution report should provide the manual workaround ("configure an `arbiter:` section in `conversus.yml` and re-run `/conversus converge`") and note that `/conversus arbitrate` is planned. Devil's advocate's recommendation to document failure recovery (Rec #2) is orthogonal and also valid, but does not solve the dead-reference problem.

---

## Tensions

### 1. Agent launch estimate: devil's advocate says it is meaningless; my review says it is an acceptable upper bound -- the truth is between

Devil's advocate (Missed Opportunity #1) argues that "21 agent launches" is meaningless to non-experts and proposes adding time/token estimates. My review (Off-Base Assumption #2) acknowledges the formula computes an upper bound but accepts the labeling "Estimated agent launches" as accurate enough, recommending only a P3 clarification that it is an upper bound.

Devil's advocate makes the stronger argument here. The target persona (SC-001) is explicitly a non-expert. Telling a non-expert "226 agent launches" provides a number without a frame of reference. My review underweighted the UX impact because I was focused on structural correctness (the formula is mathematically accurate) rather than interpretability (the number is opaque).

However, devil's advocate's proposed fix -- rough token/time estimates -- is impractical without engine instrumentation that does not exist. Token cost varies by model, prompt length, and context size. Time varies by concurrency limits and API latency. Any hardcoded estimate would be wrong for most configurations.

**Tension**: Devil's advocate correctly identifies the problem (opaque number for non-experts) but proposes a fix that requires infrastructure the spec cannot provide. My review correctly accepts the formula's accuracy but underweights the UX gap. The pragmatic middle ground is devil's advocate's alternative suggestion: explain what happens during execution in plain language ("each agent reads the target documents and writes a review, then agents cross-review each other...") without attempting to estimate cost. This is a Rec #1-caliber improvement that does not require engine changes.

### 2. Formula discrepancy: devil's advocate catches a real bug, but the analysis is incomplete

Devil's advocate (Off-Base Assumption #4) identifies that the Step 4 formula and the Important Notes formula disagree for N=3, iterations=1. The Step 4 formula gives 16; Important Notes says 13. Devil's advocate speculates the discrepancy "may come from how `iterations` is handled."

My review does not flag this at all -- I noted the formula is reused from Step 4 (line 1402) but did not verify it against Important Notes. Devil's advocate is right to flag the discrepancy, and I should have caught it.

The root cause is an algebra error in Important Notes (SKILL.md line 1517). The left side of the equation reads: `N + N*(N-1) + N + N + 1`. Expanding: N + N^2 - N + N + N + 1 = N^2 + 2N + 1. But the right side claims this equals `N^2 + N + 1`, which drops a term. For N=3: left side = 9 + 6 + 1 = 16, right side claims 9 + 3 + 1 = 13. The worked example (line 1519: "For 3 agents without arbiter: 13") is consistent with the incorrect simplified form, not the correct expansion.

The phase-by-phase count confirms 16 is correct for N=3, iterations=1: Phase 1 (3) + Phase 2 (6) + Phase 3 (3) + Phase 4 (3) + Phase 5 (1) = 16. Phase 4 (Disputes) launches N agents (SKILL.md lines 481-494), which is the "missing" N that was dropped in the simplification.

The Step 4 formula used by the converge handler (line 1404) is correct. The Important Notes simplified formula is wrong. The converge handler will show the correct number (16 for N=3), but the Important Notes documentation will contradict it. This needs to be fixed in the Important Notes, not in the converge handler.

**Tension**: Devil's advocate correctly identifies the discrepancy and correctly recommends reconciliation (Rec #5). My review missed it entirely. The fix is to correct the Important Notes algebra: `N^2 + 2N + 1` (not `N^2 + N + 1`), and update the worked examples accordingly (13 becomes 16 for N=3 without arbiter; 14 becomes 17 with arbiter).

### 3. Prerequisite chain stability: devil's advocate raises a valid risk my review dismisses by omission

Devil's advocate (Off-Base Assumption #3) argues that building the capstone (spec 009) before the foundation (specs 007, 008) is validated is premature. Spec 009 depends on spec 008 which depends on spec 007, and neither is implemented. If 007 or 008's schemas change during implementation, the converge handler's prerequisite routing and staleness detection break.

My review does not address this risk at all. I verified the FR-to-implementation mapping as if the upstream specs were stable, because the converge handler's coupling to upstream specs is minimal -- it checks file existence and modification times, not file content or schema. The prerequisite routing (SKILL.md lines 1336-1356) only checks whether `problem.md` and `interests.md` exist, not what they contain.

Devil's advocate overstates the risk. The converge handler's exposure to upstream schema changes is limited to: (1) file names (`problem.md`, `interests.md`, `conversus.yml`), and (2) the `conversus.yml` schema (which is defined by the run engine, not by specs 007/008). If spec 007 renames `problem.md`, the converge handler breaks -- but so does everything else in the guided workflow. If spec 008 changes what fields appear in `conversus.yml`, the converge handler still works because it parses using "the same schema defined in Run: Execution Step 1" (line 1370), not a spec-008-specific schema.

**Tension**: Devil's advocate is right that the dependency should be explicitly stated as "spec-drafted, not necessarily implemented." My review should have noted this. But the actual fragility is lower than devil's advocate suggests because the converge handler couples to file names and the run engine schema, not to the internal behavior of specs 007/008.

### 4. Speckit integration: devil's advocate correctly identifies spec drift, my review is silent

Devil's advocate (Missed Opportunity #4) flags the `/speckit.specify --input {output}/summary/final.md` next step (SKILL.md line 1506) as spec drift -- it appears in the implementation but not in the spec. My review does not mention this at all.

Devil's advocate is correct. The spec's FR-008 through FR-010 define the post-execution report's content. None of them mention speckit integration. The SKILL.md handler adds it as a cooperative-mode-specific next step (line 1504-1507). This is functionality not authorized by the spec.

However, I would characterize this differently than devil's advocate. This is not "premature" cross-tool integration -- it is a reasonable UX affordance that the spec underspecified. The "Suggested next steps" section (spec.md line 43, FR-008) says "suggested next steps based on outcome" without enumerating what those steps can be. The implementation fills in a concrete suggestion for the cooperative-mode case. This is an extension, not a violation.

**Tension**: Devil's advocate is right that spec-implementation parity requires either adding this to the spec or removing it from the implementation. But the framing as "spec drift" overstates the severity -- FR-008's "suggested next steps based on outcome" is intentionally open-ended. The fix is to add a brief note to the spec: "Next steps may include cross-tool integrations when relevant (e.g., applying cooperative synthesis to downstream specs)."

### 5. Delegation mechanism: devil's advocate raises a legitimate ambiguity my review glossed over

Devil's advocate (Off-Base Assumption #5, Rec #6) asks how "delegation to `/conversus run`" works mechanically in a SKILL.md context. The SKILL.md is an instruction set for an LLM agent, not code with function calls. "Delegate" could mean re-invoking the skill, jumping to a different section, or something else entirely. My review (SC-002 verification) accepted the delegation at face value, verifying only that the handler "adds pre-flight and post-flight UX but does not modify inputs, outputs, or engine behavior."

Devil's advocate is right that the mechanism is implicit. A SKILL.md reader (the orchestrating LLM) must interpret "Delegate to `/conversus run`" as "now follow the Run: Execution sections (Steps 1-5) using the config already parsed in the pre-execution summary." This is how it works in practice, but the instruction relies on the LLM's ability to navigate the document structure. For a human reader or a less capable LLM, the instruction is ambiguous.

**Tension**: My review focused on structural correctness (what the handler does) and verified it from the spec's perspective. Devil's advocate focused on operational correctness (whether the handler's instructions will be followed correctly by an LLM). Both are valid perspectives. The fix is minor: add a clarifying sentence to line 1426: "Proceed to Run: Execution Step 1 through Step 5 using the config parsed above. Do not re-invoke `/conversus run` as a separate skill invocation."

### 6. No partial re-run or resume: devil's advocate identifies a gap both reviews should have flagged

Devil's advocate (Missed Opportunity #2) notes that a failed 40-agent deliberation offers no recovery -- the user starts over from scratch. My review (Missed Opportunity #3) raises the same concern framed as "no handling of run engine failures in post-execution" and recommends plain-language failure reporting. Both reviews identify the failure experience as a gap.

The tension: devil's advocate frames this as a missing capability (resume/re-run). My review frames it as a missing UX concern (plain-language error message). Devil's advocate's framing is more honest about the scope -- a plain-language error message does not recover 34 wasted agent calls. But a resume capability would require engine changes, which violates spec 009's constraint that converge adds no execution logic.

**Tension**: Both reviews agree on the gap. Devil's advocate correctly notes the spec should at least acknowledge the failure mode, even if the position is "out of scope." My review's proposed fix (plain-language failure handling) is necessary but insufficient -- it addresses the symptom (opaque error) without acknowledging the cost (wasted compute). The spec should state: "If the delegated run fails, the converge handler reports the error in plain language. Partial recovery is not supported; the user must re-run the full deliberation. Resume capability is deferred to future work."

---

## Safe Agreements

### 1. Zero new engine logic is correctly upheld

Both reviews confirm the converge handler adds no execution logic. Devil's advocate (Alignment #1) states: "The handler explicitly states: 'Zero new execution logic.'" My review verifies this through a five-point structural analysis: no phase orchestration, no agent management, no output file creation, no new configuration, and pre/post sections only. No disagreement.

### 2. Prerequisite routing covers all permutations correctly

Devil's advocate (Alignment #2) calls the routing "thorough" and confirms all four permutations of `problem.md` and `interests.md` existence are covered. My review independently verifies the same four permutations with a detailed table mapping each to the spec's FR-004. Both reviews agree the implementation correctly extends the spec's two explicit cases to four.

### 3. Section 4 constraint (no walled garden) is well-designed

Devil's advocate (Alignment #3) praises the constraint that converge works with hand-crafted YAML, not just the define-interests-mode pipeline. My review (Off-Base Assumption #1, spec constraint verification) independently confirms this: "the handler works with a hand-crafted `conversus.yml` that was never produced by `define/interests/mode`." The prerequisite check fires only when `conversus.yml` is absent. Both reviews affirm this is correct.

### 4. Non-expert dispute interpretation needs improvement

Devil's advocate (Off-Base Assumption #2) argues that "3 dispute(s) remain unresolved" is opaque to non-experts who do not know what a "dispute" means in the conversus context. My review (SC-001 verification) notes the post-execution report "interprets results with mode-specific guidance" but flags the `/conversus arbitrate` dead reference as breaking the guided flow "at the moment the user most needs guidance."

Both reviews agree the post-execution dispute messaging is insufficient for the non-expert persona. Devil's advocate's Rec #7 (plain-language dispute explanation) and my P0 recommendation (actionable workaround for arbitration) are complementary, not conflicting. Both should be adopted.

### 5. No config preview or diff capability is missing

Devil's advocate (Missed Opportunity #3) notes there is no way to see the full config, diff it against a previous run, or understand what changed. My review does not raise this explicitly but implicitly supports it through the Missed Opportunity #1 (no validation error preview) and the recommendation for `--dry-run` (P3). Both reviews recognize the pre-execution summary is the only window into the config, and it is lossy by design (one-sentence agent summaries). This is acceptable for the non-expert persona but a gap for advanced users. No disagreement on the observation; the priority is low.

### 6. The cancel option in decline routing is a valid superset

Devil's advocate does not flag the "Cancel entirely" option added to FR-003's decline routing. My review characterizes it as "a superset, not a violation" and notes the spec's "MUST route them" language does not contemplate cancellation. The functional-typing review (FR-003 section) agrees it is "a reasonable UX addition not contradicting the spec." All three reviewers accept this as a valid extension.

### 7. Cost/time estimation is needed but out of scope

Devil's advocate (Missed Opportunity #1) proposes time/token estimates. My review (functional-typing's Missed Opportunity #2) also flags agent count as less meaningful than time or token cost. Both reviews acknowledge this would require engine instrumentation that does not exist. Both treat it as a future improvement. No disagreement on either the need or the scope boundary.
