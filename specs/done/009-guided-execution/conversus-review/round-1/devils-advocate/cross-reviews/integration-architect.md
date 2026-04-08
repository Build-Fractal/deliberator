# Cross-Review: integration-architect's Review of 009-Guided-Execution

**Cross-reviewer**: devils-advocate
**Reviewing**: integration-architect's review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. Formula discrepancy is invisible in the integration-architect's review

The integration-architect references the agent launch formula (line 155 of their review) as a factual citation and verifies SC-004 as SATISFIED, noting that the implementation "computes `max_total_agents` using the formula from the run engine" and that "an upper-bound estimate is still an estimate." They treat the formula as settled.

It is not settled. The Step 4 formula and the Important Notes formula produce different results for the same inputs. My review (Off-Base Assumption #4) demonstrated the discrepancy: for N=3, iterations=1, Step 4 yields 16 agent launches while Important Notes claims N^2 + N + 1 = 13. The integration-architect's FR-001 alignment check says the converge handler "computed agent launch estimate using the `per_round_agents` formula" -- but which formula? The two disagree.

This is dangerous because the integration-architect's review gives an unqualified ALIGNED verdict on FR-001 while the number shown to the user could be wrong by ~23% (13 vs 16 for 3 agents). If the converge handler is the guided path for non-experts, presenting a materially incorrect agent launch count undermines the trust that SC-001 and SC-004 require. The integration-architect's review should have caught this because they explicitly examined the formula at line 155 and verified SC-004 at lines 143-146.

### 2. The `/conversus arbitrate` dead reference is correctly flagged but the severity assessment conflicts with the "ALIGNED (with caveat)" verdict on FR-009

The integration-architect flags the `/conversus arbitrate` dead reference as their highest-priority finding (P0) and calls it "the highest-priority gap because it breaks the guided flow at the moment the user most needs guidance." This is correct. However, their FR-009 alignment verdict is "ALIGNED (with caveat -- see below)." These two positions are in tension. If a guided user following the post-execution report hits an unknown-subcommand error, that is not alignment with a caveat -- it is a broken user journey. FR-009 says "suggest `/conversus arbitrate`." The implementation does suggest it. But the suggestion leads to an error. Whether that constitutes FR-009 alignment depends on whether you read FR-009 as "suggest the command" (literal compliance) or "give the user a working path forward" (intent compliance). The integration-architect's P0 priority implies they believe intent compliance matters, but their ALIGNED verdict implies they accepted literal compliance. They should pick one.

My review did not call out this specific dead-reference issue (I focused on the opacity of "disputes" to non-experts rather than the command's implementation status), so the integration-architect's identification of it is a genuine addition. But the contradictory severity assessment weakens the finding.

---

## Tensions

### 1. Superset behavior as alignment vs. spec drift

The integration-architect treats FR-003's "Cancel entirely" third option as "ALIGNED (superset)" -- the spec lists two routing targets, the implementation adds a third, and the integration-architect notes "This is a superset, not a violation." My review flagged a structurally identical issue in the opposite direction: the SKILL.md adds a `/speckit.specify` next step in the post-execution report (cooperative mode) that appears nowhere in spec 009, and I called that "spec drift."

Both are cases where the implementation includes behavior not authorized by the spec. The integration-architect's framing ("superset, not a violation") is generous toward the implementation. My framing ("spec drift") is strict. The tension is real: where do you draw the line? Adding "Cancel entirely" is arguably a UX necessity that no reasonable spec would forbid. Adding a cross-tool integration to speckit is arguably scope creep that a different spec should authorize. But the integration-architect's review does not even mention the speckit next step, which means they either missed it or implicitly accepted it under the same "superset" reasoning. If the latter, the standard is inconsistent -- accepting some unauthorized additions while not examining others.

### 2. Staleness detection: pragmatic acceptance vs. fundamental challenge

The integration-architect marks FR-005 as "ALIGNED" and their only staleness-related finding (Missed Opportunity #4) is that the check should be bidirectional (also compare `problem.md` mtime). My review (Off-Base Assumption #1) challenges the entire mtime-based approach as unreliable due to git operations, editor autosaves, and content-irrelevant timestamp changes. The integration-architect's recommendation to extend the check to `problem.md` would make the false-positive problem worse, not better -- more files checked means more chances for spurious warnings.

The tension: the integration-architect accepts the mechanism and wants to expand its scope; I question the mechanism itself and want it either replaced with content hashing or explicitly labeled as best-effort. Both positions have merit. The pragmatic view is that mtime is cheap and catches the common case (user edits interests.md in their editor, mtime updates, config is genuinely stale). The strict view is that a feature targeting non-experts (SC-001) should not produce false-positive warnings that erode trust. Neither review resolves this tension.

### 3. Failure handling scope

The integration-architect raises "No Handling of Run Engine Failures in Post-Execution" as Missed Opportunity #3 (P2). My review raises the same concern more aggressively as "No partial re-run or resume capability" (Missed Opportunity #2), arguing that a non-expert who burns 34 successful agent calls and loses them to a Phase 5 failure has no recovery path. The integration-architect recommends "a brief failure-handling clause" with plain-language errors. I recommend that the spec at minimum document its failure recovery position even if the answer is "full re-run."

The tension is scope: the integration-architect wants the converge handler to translate errors, while I want the spec itself to take a position on recoverability. These are complementary but different asks. The integration-architect's recommendation is implementable within the current spec's constraints ("no new engine logic"). My recommendation may require engine-level changes (resume/checkpoint) that belong in a different spec. The integration-architect's framing is more actionable for this spec; mine is more architecturally complete but potentially out of scope.

### 4. Delegation mechanism: implicit acceptance vs. explicit challenge

The integration-architect verifies the UX wrapper property thoroughly (their "UX Wrapper Verification" section) and confirms "No execution logic" with five specific checks. They take the delegation model at face value: converge says "delegate to run," the run engine exists, therefore it works.

My review (Off-Base Assumption #5) challenges what "delegation" means in a SKILL.md context. There are no function calls, no imports, no invocation mechanism. The agent reading the SKILL.md must interpret "delegate" as "now follow the Run: Execution section." The integration-architect's verification is correct at the specification level but does not address the execution-level ambiguity. Both reviews are correct in their respective frames: the integration-architect verified spec-to-implementation alignment (which is their role), while I challenged whether the implementation can actually be executed as described (which is mine).

---

## Safe Agreements

### 1. FR-006/FR-007: Zero new engine logic is the correct constraint

Both reviews agree that the converge handler correctly avoids adding execution logic. The integration-architect's UX Wrapper Verification (five specific checks) and my review's acknowledgment ("Zero new engine logic is the correct constraint") converge on this point. The implementation delegates entirely, adds no state, extends no schema, and creates no new artifacts. This is the spec's strongest property and both reviews confirm it independently.

### 2. Prerequisite routing is thorough and correctly handles all permutations

The integration-architect's permutation table (four cases for `{problem.md, interests.md}` existence) and my review's agreement ("Prerequisite routing is thorough") both confirm that the SKILL.md handler covers all four cases with correct routing to the earliest missing step in the define-interests-mode chain. The two cases not explicitly in the spec (interests without problem, problem without interests) are handled as reasonable extensions that follow the prerequisite chain logic.

### 3. Constraint 2 (no walled garden) is well-conceived and correctly implemented

Both reviews agree that the spec's constraint "Must NOT require prior guided workflow steps" is important and correctly implemented. The integration-architect verifies: "the handler works with a hand-crafted `conversus.yml` that was never produced by `define/interests/mode`." My review states: "It means `converge` works with hand-crafted YAML, not just the define-interests-mode pipeline. This prevents the guided workflow from becoming a walled garden." The prerequisite check only fires when `conversus.yml` is absent.

### 4. SC-002 (output identity) is satisfied

Both reviews agree that converge produces identical execution output to a direct `/conversus run` invocation. The integration-architect's SC-002 verification and my review's acceptance of FR-006/FR-007 alignment both confirm that the converge handler's pre-flight and post-flight UX are additive, not substitutive. The run engine's own Step 5 report is preserved; the converge report supplements it.

### 5. The `/conversus arbitrate` dead reference is a real problem

The integration-architect's P0 finding and my review's identification of the same command as a downstream dependency (Referenced Documentation, specs/010-guided-arbitration) both recognize that suggesting an unimplemented command to a non-expert user is a gap. We frame it differently -- the integration-architect focuses on the broken user journey, I focus on the premature dependency chain -- but the underlying concern is shared: the post-execution report promises a path that does not yet exist.

### 6. The `--output` flag gap is real

The integration-architect's Missed Opportunity #2 identifies the missing `--output <dir>` flag on converge as an ergonomic gap. My review does not raise this explicitly, but the concern is valid and uncontested. The upstream commands (`define`, `interests`, `mode`) all accept `--output`; converge does not. This breaks the workflow for users who specified a non-default directory upstream.

---

## Summary of Cross-Review Position

The integration-architect's review is methodical and thorough on spec-to-implementation alignment. The FR mapping table, prerequisite permutation verification, and UX wrapper verification are rigorous artifacts. The P0 finding on the `/conversus arbitrate` dead reference is the strongest actionable finding either review produced.

Where the integration-architect's review falls short is in accepting surface-level correctness without probing deeper assumptions. The formula discrepancy (my Off-Base Assumption #4) is a concrete error that their review should have caught given that they cited the formula. The staleness mechanism (my Off-Base Assumption #1) and delegation semantics (my Off-Base Assumption #5) are areas where the integration-architect verified what the spec says without questioning whether what the spec says is sound. That said, the integration-architect's role is alignment verification, not adversarial challenge -- so the gap is expected rather than negligent.

The most actionable synthesis across both reviews: fix the formula discrepancy (concrete error), resolve the arbitrate dead reference (both reviews agree), and decide on the speckit integration (spec drift that one review caught and the other missed).
