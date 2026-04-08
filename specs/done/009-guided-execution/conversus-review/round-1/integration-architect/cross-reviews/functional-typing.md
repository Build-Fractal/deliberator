# Cross-Review: functional-typing

**Cross-reviewer**: integration-architect
**Original reviewer**: functional-typing
**Spec**: 009-guided-execution
**Date**: 2026-03-22

---

## Dangerous Contradictions

### 1. FR-004 Sub-Case Expansion: Completeness Improvement vs. Prescriptive Overreach

functional-typing correctly identifies that the implementation adds two sub-cases to FR-004 that the spec does not enumerate (interests-without-problem, problem-without-interests) and calls them a "well-motivated completeness improvement." My review reaches the same conclusion but uses different language: "sound engineering -- the spec's two-case description was an underspecification, not a constraint."

Where we could contradict each other is in functional-typing's Off-Base Assumption #3, which flags the `interests.md`-without-`problem.md` case as "unnecessarily prescriptive for advanced users," noting that a user might legitimately create `interests.md` manually. This concern is valid in isolation but misses a critical detail: these routing messages only fire when `conversus.yml` is absent (SKILL.md line 1336-1338). A user with a hand-crafted `interests.md` who also has a hand-crafted `conversus.yml` will never see the routing message -- the handler proceeds directly to the pre-execution summary. The spec's Constraint 2 (line 61) says converge must work with a hand-crafted `conversus.yml`, which it does. The prerequisite routing only applies to users who are missing the config entirely, and such users are by definition in the guided workflow, where prescriptive routing is the correct behavior.

**Resolution**: No actual contradiction. functional-typing's concern is self-qualified ("minor tension rather than a contradiction"), and the implementation correctly scopes the prescriptive routing to the guided-workflow path. No change needed.

### 2. No Contradiction on Zero-New-Engine-Logic Constraint

Both reviews independently verify that the converge handler upholds the zero-new-engine-logic constraint. functional-typing enumerates five categories of "logic" in the handler (file existence checks, staleness comparison, config parsing, launch estimation, dispute-parsing invocation) and classifies them as "pure UX" or reuse of existing subsystems. My review verifies the same via a five-point UX wrapper checklist (no execution logic, no new state, no new configuration, pre/post only, dispute parsing reuse).

No contradiction. The classifications align.

---

## Tensions

### 1. "Problem" Label Fix: Same Conclusion, Different Priority

functional-typing's P1 recommendation #1 calls for renaming the `Problem:` label at line 1377 to `Mode:` to match FR-001's language and the post-execution report's `Mode:` label at line 1439. My review does not flag this issue at all -- it appears in neither my Missed Opportunities nor my Actionable Recommendations.

This is a genuine miss on my part. functional-typing is correct: the pre-execution summary labels its first field `Problem:` but fills it with the mode and its plain-language explanation, while the post-execution report correctly uses `Mode:` at line 1439. This creates an inconsistency within the handler itself and a misleading label for users who expect the problem definition from `problem.md`. The fix is a one-line change with no structural risk. I agree with P1 priority.

### 2. `/conversus arbitrate` Dead Reference: Same Finding, Different Framing

Both reviews identify the `/conversus arbitrate` dead reference as the highest-priority issue. functional-typing rates it P1 (#2) and suggests either gating the suggestion behind implementation status or adding "(coming soon)" with a workaround. My review rates it P0 and recommends replacing the suggestion with guidance on configuring an `arbiter:` section in `conversus.yml` and re-running.

The tension is in framing: functional-typing treats this as a labeling issue that can be fixed with a parenthetical note, while my review treats it as a flow-breaking gap that requires a substantive workaround. The difference matters because a non-expert (SC-001 persona) who sees "/conversus arbitrate (coming soon)" still has no actionable path forward. My recommendation to provide the actual workaround (configure `arbiter:` in `conversus.yml` and re-run `/conversus converge`) gives the user something they can do right now. However, functional-typing's "(coming soon)" framing is more honest about the intended design trajectory -- `/conversus arbitrate` is planned, not abandoned.

**Resolution**: Both approaches have merit. The ideal fix combines them: replace the suggestion with the `arbiter:`-section workaround and add a note that a dedicated `/conversus arbitrate` subcommand is planned. This gives users an actionable path and sets expectations for future capability.

### 3. Prior Context Disclosure vs. `--output` Flag

functional-typing's P2 recommendation #3 calls for adding `Prior context: {paths}` to the pre-execution summary when `PRIOR_FILES` is non-empty. My review does not flag prior context at all, but raises a different ergonomic gap: the missing `--output <dir>` flag (my recommendation #2, P1).

These are not contradictory but reveal different reviewer priorities. functional-typing focuses on information completeness within the existing flow (the user should see all configuration dimensions before confirming). My review focuses on workflow continuity across handlers (a user who used `--output` on `define/interests/mode` cannot use the same flag on `converge`).

Both are valid. The `--output` gap is arguably higher priority because it blocks a workflow that the upstream handlers explicitly support, while the prior context omission is an information gap within an otherwise functional workflow. However, functional-typing's point is well-taken: prior files silently influencing all agents without disclosure in the pre-execution summary undermines the informed-consent principle that FR-001 and FR-002 establish.

### 4. Dispute-Parsing File Target Ambiguity

functional-typing's P2 recommendation #4 notes that line 1464 says "Check the run engine's output" without specifying which file to parse, and recommends explicitly stating `{output}/summary/final.md`. My review does not flag this.

functional-typing then self-resolves this by noting that `{output}/summary/final.md` is the correct file in both single-round and multi-round cases, making it "a documentation clarity issue rather than a functional bug." I agree with this assessment. The Dispute-Parsing Subsystem (lines 747-775) takes a file path as input, so the converge handler needs to specify which file. The post-execution report at line 1442 already references `{output}/summary/final.md`, so the instruction at line 1464 should do the same for consistency. This is a low-risk documentation improvement.

### 5. Cost/Time Estimation and Dry-Run

functional-typing's Missed Opportunity #2 (cost/time estimation beyond agent count) and #3 (dry-run capability) are absent from my review. These are reasonable suggestions but both reviewers correctly classify them as out-of-scope or future considerations. functional-typing explicitly notes cost estimation "may be out of scope for 009" and that dry-run is "acknowledged as a future consideration in the Define handler." My review does not mention them because they fall outside the spec's 10 FRs and 4 SCs.

No tension. Both reviews implicitly agree these are enhancement ideas, not gaps.

---

## Safe Agreements

### 1. All 10 Functional Requirements Are Satisfied

Both reviews independently verify FR-001 through FR-010 and conclude all are satisfied. functional-typing uses a per-FR narrative format with "Verdict" annotations. My review uses a tabular FR-to-Implementation mapping with "Status" annotations. The conclusions are identical across all 10 requirements.

### 2. The Handler Is a Pure UX Wrapper

Both reviews independently verify that the converge handler adds no execution logic. functional-typing's "Zero New Engine Logic Assessment" section and my "UX Wrapper Verification" section reach the same conclusion through different analytical approaches. functional-typing enumerates what the handler does not contain (no phase orchestration, no agent management, no output file creation). My review enumerates what the handler does contain (no execution logic, no new state, no new configuration, pre/post only, dispute parsing reuse). Both approaches confirm the same constraint satisfaction.

### 3. FR-003's "Cancel Entirely" Option Is a Reasonable Superset

Both reviews note that the spec's FR-003 lists two decline routing targets (`/conversus interests`, `/conversus mode`) while the implementation adds "Cancel entirely" as a third option. Both reviews agree this is a superset, not a violation. functional-typing calls it "a reasonable UX addition not contradicting the spec." My review notes "the spec's 'MUST route them' language does not contemplate cancellation" but classifies it as "ALIGNED (superset)."

### 4. FR-004's Two Additional Sub-Cases Are Correctly Handled

Both reviews agree that the implementation's four-case permutation for missing prerequisites (vs. the spec's two cases) is correct behavior. functional-typing calls it a "well-motivated completeness improvement." My review calls it "sound engineering" addressing an "underspecification, not a constraint." Both note that the routing follows the `define -> interests -> mode` prerequisite chain.

### 5. All Four Success Criteria Are Met

Both reviews verify SC-001 through SC-004. My review provides explicit per-SC verification. functional-typing verifies the same criteria implicitly through its FR-by-FR analysis (SC-001 maps to FR-001/002/003 coverage, SC-002 maps to FR-006/007, SC-003 maps to FR-004, SC-004 maps to FR-001's summary quality analysis).

### 6. The `/conversus arbitrate` Dead Reference Is the Highest-Priority Issue

Both reviews identify this as the most important gap. functional-typing places it at P1 in the actionable recommendations. My review places it at P0. The difference in priority label is a framing tension (see Tensions #2 above), but both reviews agree this is the single issue most likely to break the guided flow for the target persona.

### 7. Staleness Check Is Correctly Implemented but Could Be Extended

functional-typing verifies FR-005's staleness warning is fully satisfied (comparing `interests.md` vs `conversus.yml` modification times). My review agrees on satisfaction but notes the check is one-directional -- `problem.md` could also be stale. Both reviews treat the extension as a secondary recommendation (functional-typing does not mention it; my review places it at P2).

### 8. Dispute-Parsing Subsystem Reuse Is Correct

Both reviews verify that the post-execution report delegates to the Dispute-Parsing Subsystem (SKILL.md lines 747-775) rather than implementing its own parsing. functional-typing notes the subsystem's mode-specific headings are inherited correctly. My review confirms this through the "dispute parsing reuse" item in the UX wrapper verification.

### 9. The Spec's Two Constraints Are Respected

Both reviews verify Constraint 1 ("Must NOT add execution logic") and Constraint 2 ("Must NOT require prior guided workflow steps"). functional-typing verifies Constraint 1 through its zero-new-engine-logic assessment. My review verifies both explicitly in the Off-Base Assumptions section, noting that the prerequisite check (lines 1336-1356) only fires when `conversus.yml` is absent, preserving Constraint 2.
