# Cooperative Disputes: functional-typing

**Spec**: 009-guided-execution
**Reviewer role**: Structural correctness and specification compliance
**Phase**: 4 (Final)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: Problem statement inclusion in the pre-execution summary — scope of the P1 fix

**Parties**: functional-typing + devils-advocate vs. integration-architect

In my revision, I expanded P1 #1 beyond a label rename: the fix should (1) relabel `Problem:` to `Mode:`, and (2) add a `Problem:` field displaying the first sentence or heading from `problem.md`. Devils-advocate's revision (New Recommendation C) independently reaches the same conclusion: "The summary should include both `Problem: {summary of problem.md content}` and `Mode: {mode in plain language}`."

Integration-architect's revision accepts the label fix but explicitly defers problem-statement inclusion: "Adding it would be a spec amendment, not a bug fix. I agree it would improve informed consent, but it belongs in a follow-up, not in this fix."

The disagreement is real. Integration-architect is correct that FR-001 lists "mode (plain-language explanation)" as a required summary element and does not list the problem definition. Adding it is technically a spec expansion. However, FR-001's overarching purpose -- stated in the spec's own language -- is a "human-readable summary" for informed consent. The problem definition is the most fundamental input to any deliberation. A user who confirms execution without seeing what problem is being deliberated is consenting to something they cannot evaluate. This is not an edge case; it is the central information the summary exists to communicate. The one-line conditional addition ("Problem: {first sentence from problem.md}" or "(hand-crafted config -- no problem.md)") is proportionate to the gap.

I maintain my expanded position. The label fix alone is necessary but insufficient. Whether this is implemented as part of the P1 fix or as an immediate follow-up is a sequencing question I am willing to defer to the implementer, but the gap should not be deferred indefinitely.

---

### Dispute 2: Prior context disclosure priority — P2 vs. P3

**Parties**: functional-typing vs. integration-architect

My revision maintains prior context disclosure at P2. Integration-architect's revision accepts it but deprioritizes to P3, reasoning that "prior files are an advanced configuration dimension, and users who set them are more likely to be aware of their influence than the non-expert persona SC-001 targets."

Integration-architect's reasoning has a gap. The argument that prior-file users are advanced users who already know what they configured applies equally to every configuration dimension. By that logic, the entire pre-execution summary is unnecessary for anyone competent enough to write `conversus.yml`. The summary exists precisely because FR-001 requires informed consent regardless of the user's expertise level. Constraint 2 explicitly permits hand-crafted configs, and hand-crafted configs are the most likely source of `prior:` sections. Omitting prior files from the summary means the summary is incomplete for the exact user population most likely to configure them.

The implementation cost is one conditional line. The information gap affects every agent's behavior. P2 is the correct priority. I do not escalate this beyond noting the disagreement -- the difference between P2 and P3 for a one-line addition is unlikely to affect implementation order.

---

### Dispute 3: Formula fix priority — P1 vs. P2

**Parties**: integration-architect vs. functional-typing

Integration-architect's revision rates the Important Notes formula correction as P1. My revision rates it P2. Both agree on the root cause (the Important Notes arithmetic drops Phase 4), the direction of the fix (correct Important Notes to match the Step 4 formula, not the reverse), and the specific line changes required (lines 1517-1525).

The disagreement is about impact scope. The Important Notes section is documentation that supplements the SKILL.md for human readers. The converge handler (line 1404) uses the Step 4 formula, which is correct. No agent execution path reads the Important Notes formula. The risk is that a future reviewer or spec reader will use the wrong formula and report a false discrepancy -- which is exactly what happened in this review cycle. That is a documentation-quality concern, not a functional concern.

I maintain P2. The formula must be fixed, but it does not block any workflow, does not affect any execution path, and its primary harm is confusion during review -- a harm that this review cycle has already surfaced and documented. Integration-architect may reasonably prefer P1 to prevent recurrence; I consider the recurrence risk adequately mitigated by the review record itself.

---

## Convergence

The three-reviewer cooperative process reached consensus on the following items. These are no longer in dispute and represent the collective position.

### Full consensus (all three reviewers agree on problem, fix, and priority)

1. **P0: Replace `/conversus arbitrate` dead reference with actionable workaround.** The post-execution report should replace `/conversus arbitrate` with guidance to configure an `arbiter:` section in `conversus.yml` and re-run `/conversus converge`, with a note that a dedicated `/conversus arbitrate` subcommand is planned. All three reviewers agree on the combined fix. Integration-architect's P0 severity assessment is accepted. The spec's FR-009 text should be updated to say "suggest how to resolve disputes" rather than naming a specific subcommand.

2. **P1: Add `--output <dir>` flag to the converge handler.** Uncontested across all three reviews. The upstream handlers (`define`, `interests`, `mode`) all accept this flag. Its absence from `converge` breaks cross-handler workflow continuity for users who specify a non-default output directory.

3. **P1: Fix "Problem" label to "Mode" at SKILL.md line 1377.** All three reviewers agree the label is wrong and the one-line fix is required. The scope of the fix (label-only vs. label-plus-problem-statement) remains disputed (see Dispute 1), but the minimum fix is uncontested.

4. **Fix the Important Notes formula arithmetic.** All three reviewers agree on the root cause (the expanded form `N + N*(N-1) + N + N + 1` simplifies to `N^2 + 2N + 1`, not the stated `N^2 + N + 1`), the direction of the fix (correct Important Notes to match Step 4, not the reverse), and the specific lines requiring correction (1517-1525). Priority is disputed (P1 vs. P2; see Dispute 3), but the fix itself is not.

5. **P2: Document the failure recovery position.** All three reviewers converge independently: the spec should state that failures require a full re-run, resume capability is out of scope, and the user should be told this explicitly when a failure occurs. Integration-architect expands the scope to include plain-language error translation, which functional-typing and devils-advocate accept.

6. **P2: Make the delegation mechanism explicit.** All three reviewers agree that "Delegate to `/conversus run`" should be clarified to mean "proceed to execute Run: Execution Step 1 through Step 5 using the parsed config; do not re-invoke `/conversus run` as a separate skill invocation." Devils-advocate raised it; functional-typing and integration-architect accepted it as a one-line clarification.

7. **P2: Add a "What to Expect" narrative to the pre-execution summary.** All three reviewers agree that the bare agent launch count is opaque to non-experts. Integration-architect proposed the narrative explanation as NEW-1; devils-advocate and functional-typing concur. The narrative explains the process in plain language ("Each agent reads the target documents and writes a review. Agents then cross-review each other's work, revise, and a synthesis is produced.") without requiring engine instrumentation.

8. **P2: Specify dispute-parsing file target as `{output}/summary/final.md`.** Functional-typing raised it; integration-architect and devils-advocate accepted it. Line 1464 should name the specific file rather than "the run engine's output" to eliminate ambiguity in multi-round runs.

9. **P2: Add spec acknowledgment for cross-tool next steps (speckit integration).** Devils-advocate raised it as spec drift; integration-architect reframed it as under-authorization rather than unauthorized behavior. All three agree the pragmatic resolution is to keep the suggestion but add a qualifying note in the spec that cross-tool next steps are informational and tool-availability-dependent. The speckit suggestion is not removed.

10. **Staleness mechanism improvements belong in spec 008, not spec 009.** Devils-advocate withdrew the content-hashing proposal. Integration-architect withdrew the `problem.md` mtime extension. All three agree that provenance metadata (content hashes, source file tracking) should be embedded by the config generator (spec 008), not verified by the config consumer (spec 009). Devils-advocate retains a documentation-only request: the spec or SKILL.md should note that the mtime heuristic has known false positives from git operations.

11. **`--dry-run` is deferred.** All three reviewers identify it as a reasonable future enhancement. None consider it blocking for spec 009.

### Near-consensus (agreement on substance, minor priority disagreement)

12. **Prior context disclosure in the pre-execution summary.** All three reviewers agree the gap is real and the fix is a single conditional line. Functional-typing rates it P2; integration-architect rates it P3 (see Dispute 2). The fix will be implemented regardless of which priority label prevails.

13. **Important Notes formula priority.** All three agree on the fix. Integration-architect rates it P1; functional-typing rates it P2 (see Dispute 3). The correction will be applied regardless of priority classification.

---

## Final Position Statement

The converge handler is a structurally sound implementation of spec 009. All ten functional requirements are satisfied. The zero-new-engine-logic constraint is upheld. The handler correctly functions as a pure UX wrapper: pre-flight confirmation, delegation to the run engine, and post-flight interpretation.

The cooperative review process worked as designed. Each reviewer's lens caught issues the others missed. Integration-architect identified the `--output` flag gap and elevated the `/conversus arbitrate` dead reference to P0. Devils-advocate forced the staleness mechanism to be reconsidered (resulting in a correct reassignment to spec 008) and identified the delegation-semantics fragility. My structural-correctness lens caught the "Problem" label mislabeling, the prior-context omission, and the dispute-parsing file ambiguity. The cross-review phase corrected two analytical errors: devils-advocate's incomplete formula analysis (I provided the root cause), and my underweighting of the `/conversus arbitrate` severity (integration-architect's P0 assessment was correct).

The three remaining disputes are narrow. Two are priority disagreements (P2 vs. P3 for prior context; P1 vs. P2 for the formula fix) where the fix is identical regardless of classification. The third (problem-statement inclusion in the summary) is a scope question where the minimum fix is agreed and the expansion is deferred to implementation judgment. None of the disputes affect the consolidated recommendation set or block implementation.

**Consolidated recommendation set from the functional-typing perspective:**

| Priority | Recommendation | Status |
|----------|---------------|--------|
| P0 | Replace `/conversus arbitrate` dead reference with workaround + planned note | Consensus |
| P1 | Add `--output <dir>` flag to converge handler | Consensus |
| P1 | Fix "Problem" label to "Mode" + add problem statement to summary | Consensus on label fix; disputed on problem-statement expansion |
| P1 or P2 | Fix Important Notes formula arithmetic (lines 1517-1525) | Consensus on fix; disputed on priority |
| P2 | Document failure recovery position (full re-run required) | Consensus |
| P2 | Add "What to Expect" narrative to pre-execution summary | Consensus |
| P2 | Make delegation semantics explicit in Execution section | Consensus |
| P2 | Add spec acknowledgment for cross-tool next steps (speckit) | Consensus |
| P2 | Specify dispute-parsing file target as `{output}/summary/final.md` | Consensus |
| P2 or P3 | Add prior context disclosure to pre-execution summary | Consensus on fix; disputed on priority |
| Deferred | `--dry-run` capability for converge | Consensus (out of scope) |
| Withdrawn | Extend staleness check to `problem.md` (belongs in spec 008) | Consensus |
| Withdrawn | Replace mtime with content hashing (belongs in spec 008) | Consensus |

The spec is ready for implementation with these amendments applied.
