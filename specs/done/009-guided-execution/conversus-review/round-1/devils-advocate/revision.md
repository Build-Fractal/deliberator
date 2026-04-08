# Devil's Advocate Revision: 009-Guided-Execution

**Reviewer**: devils-advocate
**Phase**: 3 (Cooperative Revision)
**Date**: 2026-03-22

---

## Recommendation Dispositions

### Recommendation 1: Add a "What to Expect" narrative to the pre-execution summary
**Original**: Translate agent launch count into approximate time and explain what happens during execution.
**Disposition**: MAINTAIN with refined scope.

All three reviewers agree that the bare agent launch count is opaque to non-experts. functional-typing's cross-review concedes the UX gap but correctly notes that token/time estimates require engine instrumentation that does not exist. integration-architect reaches the same pragmatic middle ground I proposed: explain what happens during execution in plain language without attempting to estimate cost.

I concede that hardcoded token/time estimates are impractical -- model, prompt length, and concurrency all vary. The EC2 pricing analogy in my original review overstated the obligation. But the narrative explanation stands: telling a non-expert "226 agent launches" with no frame of reference is a consent problem. A brief "What to Expect" paragraph ("Each agent reads the target documents and writes a review, then agents cross-review each other's work and revise. This repeats for {iterations} cycle(s) across {rounds} round(s).") costs nothing, requires no engine instrumentation, and transforms an opaque number into a comprehensible process.

### Recommendation 2: Document the failure recovery position
**Original**: State the spec's position on failure recovery, even if the answer is "full re-run required."
**Disposition**: MAINTAIN.

All three reviewers converge on this. functional-typing agrees: "the spec should acknowledge the failure mode" and proposes the exact wording: "Failures require a full re-run. Resume capability is out of scope for this spec." integration-architect independently reaches the same conclusion, proposing: "If the delegated run fails, the converge handler reports the error in plain language. Partial recovery is not supported." This is the rare case where all three perspectives agree on both the problem and the fix. A one-sentence acknowledgment in the spec costs nothing and sets correct expectations. Resume capability is correctly out of scope (it would require engine-level checkpointing, violating the zero-new-engine-logic constraint).

### Recommendation 3: Replace mtime-based staleness with content hashing
**Original**: Store a hash of `interests.md` content inside `conversus.yml` at generation time.
**Disposition**: WITHDRAW.

functional-typing's cross-review lands a decisive blow here. Content hashing creates a coupling between the config generator (spec 008) and the config consumer (spec 009) that does not currently exist. Worse, hand-crafted configs (explicitly permitted by spec 009's Section 4 constraint) would need to manually compute and include the hash, or the staleness check would always fire. This directly contradicts the spec's position that converge works with hand-crafted YAML. integration-architect correctly scopes this further: staleness provenance belongs in spec 008's config generation, not in spec 009's consumption.

I concede. The mtime heuristic is imperfect (git operations and editor autosaves cause false positives), but: (a) the warning is informational, not blocking -- a false positive costs one extra confirmation, not a failed workflow; (b) the right fix belongs in spec 008, not here; and (c) embedding hashes in `conversus.yml` would break the hand-crafted-config path. My original recommendation placed the fix in the wrong spec and would have created worse problems than it solved.

What I retain: the mtime mechanism has known false positives, and the spec or SKILL.md should state this explicitly ("This warning may appear after git operations that update file timestamps. It is safe to proceed if you have not changed your interests."). This is documentation, not a mechanism change.

### Recommendation 4: Remove or spec-authorize the speckit integration
**Original**: The `/speckit.specify --input` next step is spec drift -- remove it or add it to FR list.
**Disposition**: MAINTAIN with softened framing.

functional-typing's cross-review raises a legitimate counter: FR-008's "suggested next steps based on outcome" is intentionally open-ended and does not enumerate permitted suggestions. integration-architect agrees the speckit suggestion is "a reasonable UX affordance that the spec underspecified" rather than unauthorized behavior.

I concede that "spec drift" overstates the severity. FR-008 does not define a closed set of permitted next steps. However, suggesting a command from an entirely different tool system (`/speckit.specify`) without any spec acknowledgment is risky if speckit's interface changes. The pragmatic resolution that both cross-reviewers converge toward is correct: keep the suggestion but add a qualifying note in the spec that cross-tool next steps are informational and tool-availability-dependent. This is not a removal -- it is explicit authorization of an existing behavior.

### Recommendation 5: Reconcile the agent launch formulas
**Original**: The Step 4 formula and the Important Notes formula disagree for N=3, iterations=1.
**Disposition**: MAINTAIN with corrected analysis.

functional-typing's cross-review provides the definitive root cause analysis that my original review lacked. I identified the discrepancy (Step 4 gives 16 for N=3; Important Notes gives 13) but speculated vaguely about iteration handling. functional-typing nails it: the Important Notes section has an internal arithmetic error. The left side of the equation at line 1517 expands to N^2 + 2N + 1, but the right side claims N^2 + N + 1, dropping one N term. The missing term is Phase 4 (Disputes), which launches N agents.

I concede my analysis was incomplete -- I correctly spotted the discrepancy but did not trace it to the algebra error. functional-typing and integration-architect both confirm: the Step 4 formula (used by the converge handler) is correct; the Important Notes simplified formula is wrong. The fix is to correct Important Notes (N^2 + 2N + 1 for without arbiter, N^2 + 2N + 2 for with arbiter) and update the worked examples (13 becomes 16 for N=3 without arbiter; 14 becomes 17 with arbiter; the multi-round examples at lines 1524-1525 also need recalculation).

My original warning -- "if the recommendation to reconcile the two formulas is followed naively by changing the Step 4 formula to match Important Notes, the converge handler would undercount agent launches" -- was the precise danger that functional-typing articulated. The direction of the fix matters. The converge handler is correct; the documentation is wrong.

### Recommendation 6: Make the delegation mechanism explicit
**Original**: Add a constraint or FR stating that delegation means proceeding to Run Step 1-5, not a new skill invocation.
**Disposition**: MAINTAIN as minor clarification.

functional-typing concedes this "is worth a one-line clarification in the spec, though I do not consider it a blocking issue." integration-architect agrees: "add a clarifying sentence to line 1426: 'Proceed to Run: Execution Step 1 through Step 5 using the config parsed above. Do not re-invoke /conversus run as a separate skill invocation.'"

I accept the consensus that this is non-blocking but useful. The delegation works today because the SKILL.md is a single document read by one agent. But as the document grows, the implicit jump from the Converge section to the Run section becomes a real context-window risk in long-context LLM execution. A one-line clarification prevents a class of future failures at zero cost. I will not escalate this beyond the minor clarification all three reviewers agree on.

### Recommendation 7: Add plain-language dispute explanation to the post-execution report
**Original**: Replace "3 dispute(s) remain unresolved" with a plain-language explanation of what disputes mean.
**Disposition**: MAINTAIN, and merge with the `/conversus arbitrate` dead-reference fix.

integration-architect's P0 finding (the `/conversus arbitrate` dead reference) and my recommendation here address the same user journey moment: a non-expert finishes a deliberation, sees unresolved disputes, and needs to understand both what disputes are and what to do about them. These are complementary fixes, not competing ones. functional-typing agrees: "Devil's advocate's Rec #7 and my P0 recommendation are complementary, not conflicting. Both should be adopted."

The combined fix: (a) explain disputes in plain language ("3 areas where agents could not reach agreement -- the synthesis presents both perspectives but does not recommend a resolution"); (b) replace the `/conversus arbitrate` suggestion with an actionable workaround ("configure an `arbiter:` section in `conversus.yml` and re-run `/conversus converge`"); and (c) note that `/conversus arbitrate` is planned. This serves both the interpretability gap (my recommendation) and the dead-reference gap (integration-architect's P0).

---

## New Recommendations

### New Recommendation A: Add prior context disclosure to the pre-execution summary

functional-typing's Missed Opportunity 4 identifies a gap I did not raise: if `prior:` files are configured in `conversus.yml`, the pre-execution summary does not mention them. For a user who inherited a config from a previous run, not knowing that prior context will influence all agents is a significant information gap for informed consent.

This aligns with my Recommendation 1 (making the summary serve informed consent) and extends it. The summary template should include a conditional line: `Prior context: {paths}` when prior files are configured. This is a small addition that prevents a meaningful surprise -- discovering after a 40-agent run that all agents were primed with context you did not know about.

### New Recommendation B: Add `--output <dir>` flag to the converge handler

integration-architect's Missed Opportunity 2 identifies an ergonomic gap I missed: `define`, `interests`, and `mode` all accept `--output <dir>`, but `converge` does not. A user who ran the entire guided workflow with `--output my-delib/` cannot run `converge` without `cd my-delib/` or file relocation. This breaks the guided workflow's consistency guarantee. The fix is minor (one additional parameter) and high-value for the user who followed the guided path with a non-default directory.

### New Recommendation C: Fix the "Problem" label to "Mode" in the pre-execution summary

functional-typing's P1 recommendation identifies that SKILL.md line 1377 labels its field `Problem:` but fills it with the mode. I did not call this out explicitly, though my Missed Opportunity 3 (config preview obscuring details) covers the symptom. functional-typing is right: the label creates a false expectation that the problem definition from `problem.md` would be displayed. The post-execution report correctly uses `Mode:` at line 1439. The pre-execution summary should match.

Beyond the relabeling, this surfaces a deeper omission I raised in my cross-review of functional-typing: the pre-execution summary never surfaces the problem definition at all. The user is confirming execution based on a summary that omits the most important input -- what problem is being deliberated. The summary should include both `Problem: {summary of problem.md content}` and `Mode: {mode in plain language}`. This turns a label fix into a consent improvement.

---

## Position Summary

My original review raised seven recommendations. After cross-review, I withdraw one (content hashing -- wrong spec, wrong mechanism, breaks hand-crafted configs), maintain five with refined analysis (What to Expect narrative, failure recovery documentation, speckit authorization, formula correction, delegation clarification), and maintain one merged with integration-architect's P0 (dispute explanation combined with arbitrate dead-reference fix). I add three new recommendations absorbed from the other reviewers' findings (prior context disclosure, --output flag, Problem/Mode label fix).

The cross-reviews corrected two substantive errors in my analysis. First, my formula discrepancy finding was directionally correct but analytically incomplete -- I identified the disagreement but did not trace it to the algebra error in Important Notes. functional-typing provided the root cause. Second, my content hashing proposal would have created worse problems than it solved by coupling specs 008 and 009 and breaking the hand-crafted-config path. Both corrections improved the final position.

The strongest consensus across all three reviewers is on three items: (1) the `/conversus arbitrate` dead reference must be replaced with an actionable workaround (integration-architect's P0, universally endorsed); (2) the Important Notes formula has an algebra error that must be corrected without touching the Step 4 formula (my finding, confirmed by both cross-reviewers); and (3) the spec should acknowledge that failures require a full re-run (all three reviewers agree on both the gap and the fix).

The remaining open tension is staleness detection scope. I withdrew my content hashing proposal, integration-architect's recommendation to extend mtime to `problem.md` was correctly identified as a spec-008 concern, and functional-typing accepted mtime as a reasonable best-effort heuristic. The resolution is that staleness mechanism improvements belong in spec 008, and spec 009 should document the mtime heuristic's known limitations without attempting to fix them.
