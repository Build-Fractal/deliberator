# Final Disputes: devils-advocate

**Spec**: 009-guided-execution
**Phase**: 4 (Cooperative Disputes)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: The pre-execution summary should include the problem statement, not just the mode label fix

**My position**: The pre-execution summary must include a `Problem:` field sourcing the problem definition from `problem.md` alongside the relabeled `Mode:` field. A user who confirms execution without seeing what problem is being deliberated is consenting to something they cannot evaluate.

**Opposing position**: Integration-architect accepts the label fix (rename `Problem:` to `Mode:`) but defers the problem-statement inclusion, arguing it expands scope beyond the current spec. FR-001 lists "mode (plain-language explanation)" as a required summary element but does not list the problem definition. Integration-architect frames problem-statement inclusion as a spec amendment, not a bug fix.

**Why I maintain this dispute**: Integration-architect's literal reading of FR-001 is technically correct -- the spec does not list the problem definition as a required summary element. But FR-001's purpose is informed consent (SC-001, SC-004), and the mode label alone does not serve that purpose. "Mode: Find common ground" tells you how the deliberation will run but not what it will deliberate. The problem definition is the single most important input -- it is the reason the entire pipeline exists. Functional-typing accepted my escalation and expanded P1 #1 to include both the relabeled field and a `Problem:` field. Integration-architect's deferral creates a state where two of three reviewers agree the summary is materially incomplete for consent, and the third agrees on the symptom but not the fix. A one-line conditional addition (first sentence of `problem.md`, or a fallback note for hand-crafted configs) does not constitute a spec amendment -- it is the same category of "reasonable extension" that all three reviewers accepted for FR-004's sub-case expansion.

**Severity**: The label fix alone is a half-measure. The summary will say `Mode: Find common ground` where it previously said `Problem: Find common ground`. The user still does not know the problem. The information gap is reduced by removing the false suggestion that a problem statement is present, but it is not closed.

---

### Dispute 2: Prior context disclosure priority -- P2 vs. P3

**My position**: Prior context disclosure in the pre-execution summary should be P2. Prior files silently influence every agent in the deliberation. Omitting them from the consent summary creates a material information gap that violates the spirit of FR-001's informed-consent requirement.

**Opposing position**: Integration-architect accepts the recommendation but downgrades it to P3, arguing that prior files are an advanced configuration dimension and that users who set them are more likely to be aware of their influence than the SC-001 non-expert persona.

**Why I maintain this dispute**: Integration-architect's downgrade rests on an assumption about user awareness that the spec does not support. Constraint 2 explicitly permits hand-crafted configs. A user who inherits a `conversus.yml` from a colleague or a previous run may not know that `prior:` files are configured. The user who set the prior files is aware; the user who runs converge with the config is not necessarily the same person. For a feature whose stated purpose is informed consent, "the person who configured it probably knows" is insufficient -- the person who confirms execution needs to know. Functional-typing rates this P2 and provides the consent argument. Two of three reviewers place it at P2; integration-architect's P3 is the outlier.

**Severity**: Low in isolation (one conditional line in the template), but the principle matters. If advanced configuration dimensions are exempt from the consent summary, the summary's guarantees degrade as the config schema grows.

---

### Dispute 3: The spec should acknowledge mtime staleness limitations explicitly

**My position**: The spec or SKILL.md should include a one-sentence note that the mtime-based staleness warning has known false positives from git operations and editor autosaves, and that it is safe to proceed if the user has not changed their interests.

**Opposing position**: No reviewer explicitly opposes this. Integration-architect withdrew the staleness-check extension (acknowledging it belongs in spec 008). Functional-typing accepted mtime as a reasonable best-effort heuristic without commenting on documentation of its limitations. The issue is not opposition but omission -- the documentation fix I proposed in my revision (a single sentence about false positives) was not contested but also was not adopted by either reviewer into their consolidated recommendation lists.

**Why I maintain this dispute**: The absence of opposition is not the same as consensus. All three reviewers agree that mtime is fragile (I raised it, functional-typing did not contest it, integration-architect's cross-review of my review confirmed it). But the consolidated recommendation lists from all three revisions focus on mechanism changes (withdrawn) or scope reassignment (to spec 008) and drop the documentation fix. A non-expert who sees "Your interests have been modified since the config was generated" after a `git stash pop` -- when they changed nothing -- will lose trust in the guided flow. One sentence in the SKILL.md handler ("This warning may appear after git operations that update file timestamps. It is safe to proceed if you have not changed your interests.") costs nothing and prevents a real user-experience failure.

**Severity**: Minor. This is a documentation addition, not a behavioral change. But it addresses a real false-positive scenario that the target persona will encounter.

---

## Convergence

The following items achieved full or near-full convergence across all three reviewers. These are settled.

### Fully Converged

1. **`/conversus arbitrate` dead reference (P0)**: All three reviewers agree the suggestion must be replaced with an actionable workaround (configure `arbiter:` section, re-run converge) plus a note that `/conversus arbitrate` is planned. Integration-architect's P0 severity was accepted by functional-typing's revision. The combined fix -- actionable path today, honest expectation-setting for the future -- was independently proposed by two reviewers and endorsed by all three.

2. **`--output <dir>` flag for converge (P1)**: Uncontested across all three reviews. Every upstream handler accepts `--output`; converge does not. The fix is minor and the gap breaks a legitimate workflow. No reviewer disputes the priority or the recommendation.

3. **Important Notes formula arithmetic correction (P1)**: All three reviewers agree the Step 4 formula is correct and the Important Notes simplified formula has an algebra error (drops Phase 4's N agents). The fix direction is unanimous: correct Important Notes to match Step 4, not the reverse. The worked examples at lines 1519-1525 need recalculation. I identified the discrepancy; functional-typing traced the root cause; integration-architect confirmed and provided line-level corrections.

4. **Failure recovery position acknowledgment (P2)**: All three reviewers independently converge on the same fix: add a one-sentence statement that failures require a full re-run and resume capability is out of scope. The exact wording varies but the substance is identical across all three revisions.

5. **"Mode" label fix at line 1377 (P1)**: All three reviewers agree the field labeled `Problem:` should be relabeled `Mode:`. The label fix itself is uncontested. The dispute on whether to also add a problem-statement field (Dispute 1 above) is separate from the label correction, which is settled.

6. **Delegation semantics clarification (P2)**: All three reviewers agree a one-line clarification should be added to line 1426 making explicit that delegation means "proceed to Run: Execution Step 1 through Step 5 in this document" and not a new skill invocation. No reviewer considers this blocking, but all consider it worth adding.

7. **Dispute-parsing file target specification (P2)**: Functional-typing and integration-architect agree that line 1464 should name `{output}/summary/final.md` explicitly. I escalated the severity in cross-review (agent could parse wrong file in multi-round runs). The fix is uncontested.

8. **"What to Expect" narrative for agent launch count (P2)**: All three reviewers agree the bare agent launch count is opaque to non-experts. The converged solution is a brief plain-language explanation of what happens during execution (agents read, review, cross-review, synthesize) without attempting token or time estimates. I proposed this; integration-architect adopted it as NEW-1; functional-typing's lens did not contest it.

9. **Speckit integration spec acknowledgment (P2)**: All three reviewers converge on keeping the `/speckit.specify` suggestion but adding spec-level acknowledgment that cross-tool next steps are informational and tool-availability-dependent. My original recommendation to remove it was too aggressive; functional-typing's open-set reading of FR-008's "suggested next steps" was persuasive. The fix is to explicitly authorize the behavior rather than remove it.

10. **Content hashing for staleness (WITHDRAWN)**: All three reviewers agree this belongs in spec 008, not spec 009. I withdrew the recommendation after functional-typing demonstrated it would break the hand-crafted-config path. The mechanism concern is real but the fix was in the wrong spec.

### Near-Converged (with minor priority disagreements)

11. **Plain-language dispute explanation in post-execution report**: I proposed explaining what disputes mean in plain language. Integration-architect's P0 fix for the arbitrate dead reference subsumes the actionable-path component. Functional-typing endorsed both as complementary. The combined fix (explain disputes + provide workaround + note planned command) is agreed in substance; only the question of whether the plain-language explanation is part of the P0 fix or a separate P2 remains.

---

## Final Position Statement

The cooperative review process worked. My original seven recommendations were stress-tested by two reviewers with different analytical frames -- structural correctness (functional-typing) and integration alignment (integration-architect). One recommendation was decisively refuted (content hashing breaks hand-crafted configs and belongs in spec 008). One was analytically completed by another reviewer (I found the formula discrepancy; functional-typing found the root cause). The rest survived with refined framing.

The spec and its SKILL.md implementation are sound. The converge handler correctly functions as a UX wrapper around the run engine. The zero-new-engine-logic constraint is genuinely upheld. The prerequisite routing is thorough. The core architecture is not in question.

What is in question is the adequacy of the consent surface. The pre-execution summary is the single decision point where a non-expert commits to spending tokens. Three findings cluster around this surface: the mode/problem labeling confusion (converged), the opaque agent launch count (converged via narrative explanation), and the omission of both the problem statement and prior context from the summary (disputed on scope). My remaining disputes (1 and 2) are both about whether the consent summary tells the user enough to make an informed decision. Integration-architect reads FR-001 as a checklist of required fields; I read it as a standard for informed consent. The checklist reading produces a narrower fix; the consent reading produces a more complete one.

Dispute 3 (mtime false-positive documentation) is procedurally unresolved -- no reviewer opposes it, but it fell through the cracks of the revision consolidation. It is the least consequential of my remaining disputes and I would accept its omission if the other two were adopted.

If I could adopt only one change from the remaining disputes, it would be Dispute 1: including the problem statement in the pre-execution summary. The problem definition is the anchor of the entire conversus pipeline. A consent surface that shows the mode, the agents, the targets, and the launch count -- but not the problem being deliberated -- is structurally incomplete regardless of what FR-001's field list says. The field list is a minimum, not a maximum, and the minimum is not sufficient for the spec's own stated purpose.

My withdrawn recommendation (content hashing) and my corrected analysis (formula discrepancy root cause) both demonstrate that the cooperative process improved my position. I entered with seven recommendations; I exit with three remaining disputes, all of which are low-severity refinements rather than structural objections. The spec is ready to implement with the converged fixes applied.
