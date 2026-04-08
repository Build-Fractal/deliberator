# Integration Architect Disputes: 009-Guided-Execution

**Reviewer**: integration-architect
**Spec**: `009-guided-execution`
**Phase**: 4 (Cooperative Disputes)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: Problem statement inclusion in pre-execution summary

**My position (revision)**: Accept FT's P1 label fix (rename `Problem:` to `Mode:` at line 1377) but defer the problem-statement inclusion DA proposes. FR-001 lists "mode (plain-language explanation)" as a required summary element. It does not list the problem definition. Adding it is a spec amendment, not a bug fix.

**FT's revised position**: Accept DA's escalation. Relabel to `Mode:` AND add a `Problem:` field showing the first sentence or heading from `problem.md` (or a fallback for hand-crafted configs).

**DA's revised position**: The summary should include both `Problem: {summary of problem.md content}` and `Mode: {mode in plain language}`. The label fix alone is insufficient -- it is a "consent flaw, not a label flaw."

**Why this remains disputed**: FT and DA converge on a position I do not share. The label fix is a one-line bug fix with zero spec-amendment risk. Adding problem-statement extraction introduces new logic: reading `problem.md`, extracting a summary, handling the absent-file case for hand-crafted configs. This is useful but it is a feature addition, not a fix, and it should be proposed as a spec amendment to FR-001 rather than smuggled in as a label correction.

The informed-consent argument is genuine -- a user who does not see the problem definition is consenting to something incomplete. But the pre-execution summary already omits other inputs (template content, constitution rules, prior file content). The summary is by design a lossy preview, not a full disclosure. Adding one omitted dimension without addressing the others creates an inconsistency in the level of detail.

**What I accept**: The label fix (P1). **What I dispute**: Coupling it with problem-statement inclusion at the same priority without a spec amendment.

---

### Dispute 2: Prior context disclosure priority

**My position (revision)**: Accept FT's recommendation to add `Prior context: {paths}` to the pre-execution summary, but rate it P3 because prior files are an advanced configuration dimension and users who set them are more likely to be aware of their influence.

**FT's revised position**: Maintain P2. The fix is a single conditional line in the template, and the informed-consent principle of FR-001/FR-002 does not carve out advanced features.

**DA's revised position**: Align with FT. Prior files "silently influence all agents" and their omission "directly undermines FR-001's 'human-readable summary' requirement."

**Why this remains disputed**: The disagreement is about who the target user is when prior files are in play. Prior files appear in `conversus.yml` through one of two paths: (1) the guided workflow's mode handler sets them based on multi-round history, in which case the user already knows about them, or (2) the user hand-crafted the config, in which case they wrote the `prior:` section themselves. In neither case is the user unaware of prior files.

FT's principle -- that FR-001's informed-consent obligation applies uniformly regardless of feature complexity -- is clean but leads to a disclosure obligation that scales with config complexity. If prior files must be disclosed, then template paths, constitution content, and iteration counts also deserve expanded disclosure. The summary becomes a config dump, which SC-004 explicitly rejects.

I accept the recommendation. I dispute the priority. P3 captures the correct cost-benefit: low implementation cost, low user impact, worth doing when the higher-priority items are resolved.

---

### Dispute 3: Speckit integration -- authorization vs. removal

**My position (revision)**: Accept as P2. Keep the speckit suggestion in the post-execution report. Add a spec note that FR-008's "suggested next steps based on outcome" may include cross-tool suggestions when contextually relevant. This makes the integration spec-authorized rather than spec-drifted.

**DA's revised position**: Maintain with softened framing. Keep the suggestion but add a qualifying note that cross-tool next steps are "informational and tool-availability-dependent."

**FT's revised position**: Did not raise this in original review. In cross-review, FT characterizes it as a reasonable implementation choice under FR-008's open-ended next-steps language, not unauthorized behavior. Agrees the pragmatic resolution is to keep it with a qualifying note.

**Why this remains disputed**: All three reviewers now agree to keep the suggestion with a qualifying note. The dispute is narrow: the form of the qualification. My recommendation is a positive authorization in the spec ("next steps may include cross-tool suggestions when contextually relevant"). DA's recommendation is a negative qualifier ("informational and tool-availability-dependent"). These produce different failure modes. Positive authorization encourages future cross-tool suggestions without review; negative qualification warns against overreliance.

The resolution is closer to convergence than dispute. I note the gap but do not consider it blocking. Either qualification achieves the goal: the speckit integration is no longer undocumented behavior.

---

### Dispute 4: Formula correction scope

**My position (revision)**: Accept as P1. Correct the Important Notes arithmetic at lines 1517-1525. The Step 4 formula is correct; the Important Notes simplified formula drops Phase 4 (Disputes, N agents). Specific line-level corrections enumerated in my revision.

**FT's revised position**: Accept as NEW-3, P2. Agrees the Important Notes has an internal arithmetic error, that the Step 4 formula is correct, and that the fix direction is Important Notes to Step 4 (not the reverse).

**DA's revised position**: Maintain with corrected analysis. Concedes the original analysis was incomplete, accepts FT's root cause (algebra error, not iteration handling), and agrees the Step 4 formula is correct.

**Why this remains disputed**: All three reviewers agree on the diagnosis and the fix direction. The dispute is purely about priority. I rate it P1 because the converge handler is the guided-workflow entry point -- a non-expert reading Important Notes alongside the converge output will see contradictory numbers, eroding trust in the exact feature designed to build trust. FT rates it P2 because the converge handler uses the correct formula, so users see the right number; the bug is in documentation that users may never read.

The disagreement reflects a scope question: does "the converge handler works correctly" mean the documentation it lives alongside is out of scope for severity assessment? I argue no -- SKILL.md is a single document, and internal contradictions within it affect the reliability of any section. FT argues yes -- the handler's behavior is correct, so downstream documentation errors are lower priority. Both positions are defensible. I maintain P1.

---

## Convergence

The following items reached full three-reviewer convergence through the revision process. No disputes remain on these.

### 1. `/conversus arbitrate` dead reference (P0)

All three reviewers agree this is the highest-priority finding. FT elevated from P1 to P0 in revision. DA's combined fix (plain-language dispute explanation + actionable workaround + planned-command note) is accepted by all. The fix targets three locations (SKILL.md lines 1469, 1488-1489, and the spec's FR-009 text) and provides a working path today while setting expectations for future capability.

### 2. `--output <dir>` flag for converge (P1)

Uncontested across all three reviews. All reviewers agree this blocks a workflow that the upstream handlers (`define`, `interests`, `mode`) explicitly support. FT adopted it as NEW-1 in revision. DA adopted it as New Recommendation B. No reviewer challenges priority or scope.

### 3. "Problem" to "Mode" label fix (P1 -- the label itself)

All three reviewers agree that line 1377 should read `Mode:`, not `Problem:`. The dispute on problem-statement inclusion (Dispute 1 above) is separate from this label fix, which is a one-line change that all reviewers endorse without qualification.

### 4. Important Notes formula correction (direction agreed, priority disputed)

All three reviewers agree the Important Notes simplified formula is wrong, the Step 4 formula is correct, and the fix must update Important Notes to match Step 4. The specific corrections are enumerated and agreed. Only the priority is disputed (see Dispute 4).

### 5. Plain-language failure handling with recovery-position statement (P2)

All three reviewers converge on both the problem and the fix: add a failure-handling clause that translates errors to plain language, states that failures require a full re-run, and defers resume capability to future work. DA originally framed it as a missing capability; my revision and FT's revision both reframe it as a one-paragraph spec acknowledgment that sets correct expectations within the zero-new-engine-logic constraint. No remaining disagreement.

### 6. Delegation semantics clarification (P2)

All three reviewers agree that "Delegate to `/conversus run`" should be made explicit with a one-line clarification: proceed to Run: Execution Step 1 through Step 5 using the parsed config; do not re-invoke as a separate skill invocation. FT adopted this as NEW-2. DA softened from a constraint/FR request to a minor clarification. No remaining disagreement.

### 7. Dispute-parsing file target specification (P2)

All three reviewers agree that line 1464 should specify `{output}/summary/final.md` as the explicit file target. FT raised it, DA escalated the severity rationale (LLM agent could parse wrong file in multi-round runs), and I accepted it. No remaining disagreement.

### 8. Staleness detection belongs in spec 008 (structural agreement)

All three reviewers converge on the meta-conclusion: staleness mechanism improvements belong in spec 008's config generation, not in spec 009's consumption. I withdrew my mtime extension. DA withdrew content hashing. FT accepted mtime as a reasonable best-effort heuristic for spec 009. DA retains one documentation request: the SKILL.md should note that the mtime warning may fire after git operations. This is uncontested.

### 9. "What to Expect" narrative in pre-execution summary (P2)

All three reviewers agree the bare agent launch count is opaque to non-experts. The agreed fix is a brief plain-language explanation of what happens during execution (agents read, review, cross-review, revise, synthesize) added after the launch estimate line. This requires no engine instrumentation and serves SC-001. No remaining disagreement.

---

## Final Position Statement

The cooperative review process for spec 009-guided-execution has been unusually productive. Of twelve substantive recommendations in the consolidated set, eight reached full convergence. Four disputes remain, and all four are narrow -- they concern priority levels and scope boundaries, not fundamental disagreements about what is broken or what the fix should be.

### What the process validated

The converge handler is a sound implementation. All ten functional requirements are satisfied. Both spec constraints (no new engine logic, no walled garden) are upheld. All four success criteria are met. The handler is a pure UX wrapper: pre-flight, flight (delegation), post-flight. Three independent reviewers with different analytical lenses -- structural correctness, integration architecture, adversarial challenge -- independently verified these properties and reached identical conclusions.

### What the process corrected

Three findings emerged that no single reviewer would have caught alone.

First, the Important Notes formula error. DA identified the symptom (the formulas disagree). FT provided the root cause (an algebra error that drops Phase 4). I confirmed the line-level corrections. The three-reviewer chain was necessary: symptom identification, root cause analysis, and fix verification each required a different analytical approach.

Second, the `/conversus arbitrate` dead reference sharpened from a documentation concern (FT's original P1) to a flow-breaking gap (my P0) to a combined fix with three components (DA's dispute explanation + my workaround + FT's planned-command note). Each reviewer added a dimension the others missed.

Third, the staleness detection scoping. DA challenged the mechanism (mtime is fragile). I challenged the scope (should include `problem.md`). FT challenged my scope extension (content hashing would break hand-crafted configs). Through mutual challenge, all three converged on a conclusion none of us started with: the fix belongs in spec 008, not spec 009.

### Where I was wrong

I missed the "Problem" label mislabeling entirely -- a concrete inconsistency within the handler that FT caught on first pass. I cited the agent launch formula without cross-checking it against Important Notes -- DA caught the discrepancy that my citation should have surfaced. I implicitly accepted the speckit integration as covered under "superset" reasoning without examining it -- DA correctly identified it as unspec'd behavior I did not review. The cross-review process corrected all three blind spots.

### Where I held my ground

The `/conversus arbitrate` dead reference remains P0. DA's cross-review challenged the tension between my "ALIGNED (with caveat)" verdict and my P0 severity, and that challenge was correct. I revised FR-009 to "ALIGNED (literal) / MISALIGNED (intent)" in my revision, resolving the tension. The implementation does what FR-009 says; what FR-009 says does not serve its own intent when the command does not exist.

The `--output <dir>` flag gap remains P1. No reviewer contested this finding at any phase. It is the cleanest uncontested gap in the review set.

The Important Notes formula correction remains P1 in my assessment. The converge handler uses the correct formula, but the SKILL.md is a single document, and internal contradictions within it degrade trust in the document as a whole. FT's P2 rating is reasonable but reflects a narrower scope of concern.

### The four remaining disputes are resolvable

Disputes 1 and 2 (problem-statement inclusion and prior-context priority) are about where to draw the line on informed consent in a summary that is lossy by design. The underlying principle -- that the pre-execution summary should give users enough information to make an informed decision -- is shared. The disagreement is about what "enough" means. This is a product decision, not a technical one.

Dispute 3 (speckit qualification language) is functionally converged. The remaining gap between positive authorization and negative qualification is a drafting preference that does not affect behavior.

Dispute 4 (formula priority) is a severity calibration that will resolve when the fix is applied. Whether it ships as P1 or P2, the same lines change.

None of the four disputes block implementation. The eight converged items constitute a complete, actionable revision plan for spec 009 and its SKILL.md implementation.
