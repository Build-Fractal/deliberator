# Cross-Review of devils-advocate

**Reviewer**: functional-typing
**Reviewing**: devils-advocate's review of 009-guided-execution
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. The formula discrepancy claim is incorrect and risks introducing a real bug

Devil's advocate claims the Step 4 formula and the Important Notes formula disagree for N=3, iterations=1. The Step 4 formula gives 16; the Important Notes simplified formula gives 13. Devil's advocate calls this a contradiction that must be reconciled (Recommendation 5).

This is wrong. The two formulas are not equivalent expressions -- they describe different phase structures. The Important Notes formula (N^2 + N + 1, yielding 13 for N=3) is a simplification that counts: N*(N-1) cross-reviews + N revisions + N reviews + 1 synthesis = N^2 - N + N + N + 1 = N^2 + N + 1. The Step 4 formula (per_round_agents = N + iterations*(N*(N-1) + N) + N + 1) counts: N reviews + iterations*(N*(N-1) cross-reviews + N revisions) + N disputes + 1 synthesis. For N=3, iterations=1: 3 + 1*(6+3) + 3 + 1 = 16.

The difference is Phase 4 (disputes). The Important Notes formula (line 1517) lists "N + N*(N-1) + N + N + 1" and simplifies to "N^2 + N + 1" -- but N + N*(N-1) + N + N + 1 = N + N^2 - N + N + N + 1 = N^2 + 2N + 1, not N^2 + N + 1. So the Important Notes section has an internal arithmetic error: its expanded form and its simplified form disagree. The Step 4 formula, which includes Phase 4 disputes (N agents), is structurally correct. The Important Notes simplified formula drops Phase 4 entirely.

Devil's advocate identified a real inconsistency but misattributed it. If the recommendation to "reconcile the two formulas" is followed naively -- by changing the Step 4 formula to match Important Notes -- the converge handler would undercount agent launches by N, misleading users. The correct fix is to correct the Important Notes simplified formula, not to question the Step 4 formula.

### 2. Recommending content hashing creates a coupling that violates the zero-new-engine-logic constraint

Devil's advocate's Recommendation 3 says to replace mtime-based staleness with content hashing: "store a hash of interests.md content inside conversus.yml when it is generated." This requires the mode handler (spec 008) to compute and embed a hash during config generation, and the converge handler to verify it.

This is architecturally dangerous for two reasons. First, it adds a coupling between the config generator (spec 008) and the config consumer (spec 009) that does not exist in the current design. The converge handler would need to know the hashing algorithm, the field name in conversus.yml, and the content normalization strategy. Second, embedding a content hash in conversus.yml means hand-crafted configs (permitted by spec 009's Section 4 constraint) would need to manually compute and include the hash, or the staleness check would always fire. This contradicts the spec's explicit position that converge works with hand-crafted YAML.

The mtime heuristic is imperfect, but it is the right trade-off for a UX wrapper. My review did not flag staleness detection as a concern because it is informational (line 1364: "The user may proceed or regenerate") -- a false positive costs the user one extra confirmation, not a blocked workflow.

---

## Tensions

### 1. Cost/time estimation: we agree on the gap but diverge on the solution boundary

Devil's advocate (Missed Opportunity 1) and my review (Missed Opportunity 2) both identify that "42 agent launches" is opaque to non-experts. We agree this is the single most impactful UX gap.

The tension is scope. Devil's advocate wants the spec to "provide a rough token/time estimate" or acknowledge why it cannot. My review notes this "would require engine instrumentation" and flags it as potentially out of scope. Devil's advocate's framing is more aggressive -- the EC2 pricing analogy implies the feature is irresponsible without cost estimation. I view it as a valid future enhancement rather than a current irresponsibility. The launch count is better than nothing; the spec's SC-004 example ("estimated 21 agent launches") shows intent to communicate scale, even if the unit is imperfect. Adding a "What to Expect" narrative (devil's advocate's Recommendation 1) is a reasonable middle ground that does not require engine instrumentation.

### 2. Speckit integration: spec drift vs. useful cross-tool routing

Devil's advocate (Missed Opportunity 4) identifies that the `/speckit.specify --input` next step in the converge handler (line 1506) appears only in SKILL.md, not in spec 009, and calls this "spec drift" requiring either spec coverage or removal.

My review did not flag this. On reflection, devil's advocate has a structural point: the SKILL.md includes behavior not authorized by any spec. However, the suggested next steps in the post-execution report are inherently open-ended UX guidance, not functional requirements. The spec says FR-008 requires "suggested next steps based on outcome" -- it does not enumerate which next steps are permitted. A cross-tool suggestion under FR-008's umbrella is a reasonable implementation choice, not unauthorized behavior. The tension is whether "suggested next steps" is an open or closed set. Devil's advocate reads it as closed (only spec-authorized suggestions); I read it as open (any contextually useful suggestion).

That said, suggesting a command (`/speckit.specify`) that belongs to an entirely different tool system without any spec acknowledgment is risky if speckit's interface changes. A pragmatic resolution: keep the suggestion but add a qualifying note in the spec that cross-tool next steps are informational and tool-availability-dependent.

### 3. Delegation mechanism: implicit vs. explicit

Devil's advocate (Off-Base Assumption 5) argues that the delegation from converge to run is underspecified in a SKILL.md context. How does an LLM agent "delegate" to another handler section? Devil's advocate wants the spec to state explicitly: "the agent proceeds to execute Run: Execution Step 1 through Step 5."

My review treated delegation as unproblematic because the SKILL.md is a single document read by one agent -- "delegate to /conversus run" means "follow the Run handler instructions." However, devil's advocate raises a legitimate fragility concern: if the SKILL.md grows large enough that the agent loses context of the Run handler while executing the Converge handler, the implicit delegation breaks. This is a real risk in long-context LLM execution, not a theoretical one.

The tension: I see this as an implementation detail that works today; devil's advocate sees it as an architectural weakness that should be made explicit. I concede this is worth a one-line clarification in the spec, though I do not consider it a blocking issue.

### 4. Prerequisite chain stability

Devil's advocate (Off-Base Assumption 3) argues that building the capstone (spec 009) before the foundation (specs 007, 008) is validated is a risk the spec does not acknowledge.

My review did not raise this concern. The dependency is declared (`Depends On: 008-interests-mode`), the converge handler's prerequisite checks are structurally simple (file existence, not schema validation), and the handler explicitly works without the guided workflow (Section 4 constraint). If upstream schemas change, the prerequisite routing messages change -- but the converge handler's core logic (read config, summarize, confirm, delegate, report) is independent of upstream artifacts.

The tension: devil's advocate sees implementation risk in the dependency chain; I see spec 009 as deliberately decoupled from upstream details. Both positions are defensible, but I maintain that the zero-new-engine-logic constraint and the hand-crafted-YAML constraint together make 009 resilient to upstream changes. The prerequisite routing is convenience UX, not load-bearing architecture.

### 5. Partial re-run / resume capability

Devil's advocate (Missed Opportunity 2) wants the spec to state its position on failure recovery, even if the position is "out of scope." My review did not raise this.

I agree the spec should acknowledge the failure mode -- a 34-agent-launch failure with no recovery is a poor experience. However, resume capability would require engine changes (checkpointing, idempotent phase execution), which violates the zero-new-engine-logic constraint. The right resolution is a one-sentence acknowledgment in the spec: "Failures require a full re-run. Resume capability is out of scope for this spec." This costs nothing and sets correct expectations.

---

## Safe Agreements

### 1. Zero new engine logic is the correct constraint and is upheld

Both reviews confirm that the converge handler introduces no execution logic. Devil's advocate's Alignment point 1 and my Zero New Engine Logic Assessment reach the same conclusion via different analysis paths. The handler is pure UX: prerequisite checks, config parsing for display, confirmation, delegation, and report formatting.

### 2. FR-004 prerequisite routing is thorough and well-motivated

Devil's advocate's Alignment point 2 acknowledges the routing is thorough. My review (FR-004 analysis) notes the two additional sub-cases (interests-without-problem, problem-without-interests) are a well-motivated completeness improvement. We agree the implementation exceeds the spec in a beneficial direction.

### 3. The "Problem" label should be "Mode"

My review (P1 recommendation 1) identifies the mislabeling at line 1377 where `Problem:` is used but the field contains the mode. Devil's advocate does not call this out explicitly, but the underlying concern surfaces in devil's advocate's Missed Opportunity 3 (config preview), which notes that the summary "may actually obscure details." The label fix is uncontroversial and should be applied.

### 4. The `/conversus arbitrate` suggestion needs a guard

My review (P1 recommendation 2) flags that suggesting `/conversus arbitrate` to a non-expert when the command does not exist yet creates a dead end. Devil's advocate's Off-Base Assumption 2 makes the same point about interpreting dispute status. We agree the post-execution report should either gate the suggestion or add a parenthetical noting the command is not yet available.

### 5. Dry-run capability is a reasonable future enhancement

Devil's advocate (Missed Opportunity 3) and my review (Missed Opportunity 3) both identify a `--dry-run` or equivalent as useful. Neither considers it blocking for this spec. We agree it is a P3 enhancement.

### 6. The spec's independence from guided workflow is correctly designed

Devil's advocate's Alignment point 3 and my FR-006/FR-007 analysis both confirm that the Section 4 constraint ("Must NOT require prior guided workflow steps") prevents converge from becoming a walled garden. This is a shared structural endorsement.
