# Cross-Review of The Pragmatist's Enforcement Audit

**Cross-Reviewer**: The Purist
**Date**: 2026-03-19
**Subject**: The Pragmatist's enforcement audit of SKILL.md
**Method**: Identify where The Pragmatist's conclusions create risk if adopted uncritically.

---

## Dangerous Contradictions

### DC-1: "Phase 2 `{AGENT_DOCS}` is a P1 fix" masks a deeper structural absence

The Pragmatist identifies that `{AGENT_DOCS}` is used in the cross-review template but not listed in the Phase 2 variable definitions, and calls it a P1 fix. The proposed remedy is to add `{AGENT_DOCS}` to the Phase 2 variable list. This is correct but dangerously narrow.

The Pragmatist's audit checks only cooperative mode templates. My audit found that `{AGENT_DOCS}` is also missing from the prisoners-dilemma `revision.md` and `disputes.md` templates entirely -- meaning those templates strip agents of their grounding documentation in Phases 3 and 4. The Pragmatist's fix ("add `{AGENT_DOCS}` to the Phase 2 variable list in SKILL.md") addresses the spec's silence but does not address the template-level omission in prisoners-dilemma mode. Applying the Pragmatist's fix gives a false sense of completeness: the variable is now "defined" for Phase 2, but two templates in another mode still lack it.

**The danger**: An implementer reads the Pragmatist's fix, adds the variable definition, and believes the problem is solved. Meanwhile, prisoners-dilemma agents in Phases 3-4 still lose their documentation grounding, producing revisions and dispute declarations without access to their own reference materials. This is a silent quality degradation, not a crash, so it will pass functional testing.

### DC-2: Dismissal of `{ITERATION}` as "dead weight" is wrong -- it is a traceability gap

The Pragmatist identifies that `{ITERATION}` is defined in SKILL.md but unused in any revision template, and concludes: "it's dead weight." The proposed fix is either "add it to the template" or "remove it from the variable list," with a preference for adding it.

This framing misses the actual risk. The `{ITERATION}` variable is the only mechanism by which a revision agent knows which iteration it is operating in. Without it, the revision agent in iteration 3 has no way to distinguish its context from iteration 1. The agent receives `{CROSS_REVIEWS_OF_ME}` (which differ per iteration because cross-reviews are overwritten), but it has no explicit signal that this is a later refinement pass versus the first one. The behavioral consequence: iteration-2+ agents may restate positions from scratch rather than narrowing toward convergence, because nothing in their prompt says "this is your Nth revision -- your goal is to converge, not restart."

The Pragmatist treats this as cosmetic ("useful metadata"). It is functional: without an iteration signal, the multi-iteration convergence loop has no ratchet mechanism in the prompt itself. The convergence is entirely implicit, depending on the cross-review content to carry the signal. For well-written cross-reviews this works; for vague or repetitive cross-reviews it does not.

**The danger**: Accepting "dead weight, add it for metadata" understates the fix priority. This should be a P2 (iteration convergence quality), not a P3 (cosmetic metadata).

### DC-3: Template path resolution fix is too permissive

The Pragmatist proposes a three-step resolution algorithm for finding the template directory: (1) check for `conversus/` subdirectory of the config's parent, (2) check the config's parent itself, (3) walk up parent directories. The Pragmatist correctly identifies this as a P1 failure point.

However, the proposed fix introduces ambiguity the current spec does not have. The current spec says "walk up from CWD looking for `conversus/templates/`" -- one algorithm, one anchor (CWD). The Pragmatist's fix introduces three search strategies with two different anchors (config file parent and CWD implicitly via walk-up). If a user has nested `conversus/` directories (e.g., a `conversus/` at the monorepo root and another inside a submodule), the three-step algorithm can resolve to the wrong one depending on where the config file lives.

**The danger**: The fix trades a fragile-but-deterministic algorithm for a robust-but-ambiguous one. A better fix is the Pragmatist's own principle applied consistently: resolve once during config parsing. The config file's location should be the single anchor, and the template directory should be a path relative to it -- stated once, with no fallback chain.

---

## Tensions

### T-1: Pragmatism on Phase 6 trigger fragility vs. specification rigor

The Pragmatist evaluates the Phase 6 trigger mechanism (parsing `### Remaining Disputes` and `**Dispute:` from synthesis output) and concludes: "fragile but defensible" because the fallback is fail-safe (defaults to running arbitration). The Pragmatist explicitly says: "No critical fix needed" and calls the idea of adding a machine-readable marker "over-engineering."

I agree the fail-safe fallback is correct engineering. But "no fix needed" understates the cost of false-positive triggers. Every unnecessary Phase 6 invocation is a full arbitration agent launch, reading the entire deliberation record, producing a binding ruling on disputes that do not exist. The output directory then contains an arbitration ruling that references phantom disputes. Downstream consumers of the output (users reading the results, or automated pipelines ingesting the output directory) cannot distinguish "arbitration was needed" from "arbitration was triggered by parse failure." The fail-safe prevents missed arbitration but introduces phantom arbitration artifacts.

The Pragmatist is right that this is not a blocking defect. But "no fix needed" should be "low-priority fix" -- the cost of the failure mode is nonzero and scales with usage.

### T-2: Scope of the audit -- cooperative-only vs. all modes

The Pragmatist's variable audit (Section 3) traces template variables exhaustively for cooperative mode and Phase 6 (shared across modes), finding two mismatches. This is thorough work within its scope. But the audit does not trace variables for winner-take-all, prisoners-dilemma, or red-blue modes.

My audit found Gap 1.1 (`{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` undefined for red-blue mode) -- a blocking defect that the Pragmatist's scope would not catch. The Pragmatist's summary says the SKILL.md "will produce correct output for the happy path (cooperative mode, 3 agents, 1 iteration, single target file, run from monorepo root)" and frames the four P1 fixes as sufficient for "all configurations." But red-blue mode is broken independently of those four fixes.

This is not a factual error in the Pragmatist's review -- the scope was stated ("will an LLM following SKILL.md produce correct behavior end-to-end?") and the cooperative path was tested. The tension is that the conclusion ("apply those four and this skill works end-to-end for all configurations") overstates what was verified.

### T-3: Silent failures vs. specified error messages

The Pragmatist does not audit error messages or validation failure behavior. My audit found that 11 of 14 validation rules lack specified error messages (Gap 2.1). The Pragmatist's focus is on happy-path execution ("will it produce correct output?"), not on failure-path specification.

This is a legitimate difference in audit scope, but it creates a tension: the Pragmatist's P1 fix list does not include any error-message specifications, meaning an implementer following only the Pragmatist's recommendations will have formally correct execution but informal, inconsistent, and potentially confusing failure messages. For a tool that will be run by LLM orchestrators (not humans reading stderr), poor error messages degrade the orchestrator's ability to self-correct.

---

## Safe Agreements

### SA-1: `{TARGET_FILES}` missing from Phase 5 synthesis is a real defect

Both reviews independently identify that the Phase 5 synthesis template uses only `{TARGET_PATH}` (a single file) when the system supports multi-target deliberations. The Pragmatist calls this "Mismatch 2" (P1); I identify it as the `{TARGET_PATH}` vs `{TARGET_FILES}` tension in my appendix. The diagnosis is identical: the synthesis agent cannot read all target files in a multi-target configuration because the template only references the primary. The fix is identical: add `{TARGET_FILES}` to the synthesis template and the Phase 5 variable list. This is safe to implement.

### SA-2: Agent name validation is necessary to prevent silent path corruption

The Pragmatist identifies Edge Cases 2 and 3 (agent names with special characters causing invalid paths or silent overwrites on case-insensitive filesystems). I did not call this out as a separate gap but it is consistent with my methodology: any behavior not specified is a spec bug. The Pragmatist's proposed validation (`[a-z0-9][a-z0-9-_]*`) is a reasonable pattern. Both reviews agree this should be enforced at config validation time. Safe to implement as proposed.

### SA-3: The iteration loop mechanics are correct but need boundary clarification

Both reviews agree the iteration loop diagram is sound and the file-naming convention is specified. Both reviews identify the same boundary friction: when iteration 2's cross-reviews need to read the output of iteration 1, the filename is `revision.md` (no suffix), but the general formula `revision_{N-1}.md` when N=2 yields `revision_1.md`, which does not exist. The Pragmatist's proposed note ("if N-1 equals 1, the path is `revision.md`") and my Gap 5.1 (the formula is inferable but never stated as a single rule) describe the same problem with the same solution. Safe to implement.

---

## Summary

| Category | # | Finding |
|---|---|---|
| Dangerous Contradiction | DC-1 | `{AGENT_DOCS}` fix is too narrow -- misses prisoners-dilemma template omission |
| Dangerous Contradiction | DC-2 | `{ITERATION}` is functional (convergence ratchet), not cosmetic metadata |
| Dangerous Contradiction | DC-3 | Template resolution fix introduces multi-anchor ambiguity |
| Tension | T-1 | "No fix needed" for Phase 6 trigger ignores phantom arbitration cost |
| Tension | T-2 | Audit scope covers cooperative mode only; "all configurations" conclusion is overstated |
| Tension | T-3 | No audit of error messages leaves failure paths unspecified |
| Safe Agreement | SA-1 | `{TARGET_FILES}` missing from Phase 5 synthesis |
| Safe Agreement | SA-2 | Agent name validation prevents silent path corruption |
| Safe Agreement | SA-3 | Iteration loop boundary clarification needed |
