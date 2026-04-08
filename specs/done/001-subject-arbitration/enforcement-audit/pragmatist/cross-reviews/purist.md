# Cross-Review of The Purist's Enforcement Audit

**Reviewer**: The Pragmatist
**Reviewed**: The Purist
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Error Message Completeness as a Requirement Will Calcify the Spec

The Purist (Gap 2.1) demands that all 14 validation rules have formally specified error message templates, calling out the inconsistency between the three arbiter-specific messages and the eleven unspecified ones. This contradicts the stated purpose of the spec.

SKILL.md is instructions to an LLM orchestrator, not a compiler. An LLM receiving "If validation fails, report the error and stop" will produce a sensible error message every time -- the failure mode is not silence, it is a slightly different wording. Mandating 14 exact error strings transforms the spec from a behavioral contract into a string-literal contract. Every future config field addition now requires a parallel error template, creating a maintenance burden that will cause the spec and implementation to drift. The three arbiter messages exist because arbiter validation is the most subtle rule (grounding path existence, trigger enum). Elevating every trivial check ("at least 2 agents required") to the same formality level flattens the signal: an implementer cannot distinguish which validations are tricky and which are obvious.

The dangerous part: if adopted, this creates a false sense of completeness. An implementer sees 14 message templates, assumes validation is "done," and never considers the 15th rule they need when a new config field is added. The spec becomes a checklist to satisfy rather than a guide to follow.

### DC-2: `{PRIOR_FILES}` Injection Scope -- The Purist's Fix Creates a Worse Problem Than It Solves

The Purist identifies Gaps 4.1 and 4.2 (prior injection heading mismatch and scope ambiguity) and proposes either standardizing all template headings to "What to Read" or specifying the injection target per mode. Both proposals are dangerous.

My review (Finding 4) reaches the same diagnosis but the opposite conclusion: Phase 1-only injection is sufficient and should be the documented behavior. The prior context propagates naturally -- Phase 1 agents absorb it into their reviews, and every subsequent phase reads those reviews. Injecting prior context into every phase prompt (as the Purist's "every agent prompt" literal reading would require) means Phase 5 synthesis and Phase 6 arbitration agents receive both the raw prior files AND the fully-deliberated outputs that already incorporate that prior context. This is redundant at best and actively harmful at worst: it biases the arbiter toward the prior position rather than the deliberation's conclusions.

The Purist treats "every agent prompt" as an ambiguity to resolve by making it literally true. The pragmatic reading is that this is a Phase 1 instruction with sloppy phrasing, and the fix is to explicitly scope it to Phase 1, not to propagate it everywhere.

### DC-3: Demanding `{ITERATION}` Be Used or Removed Misreads Its Purpose

The Purist (Gap 1.2) flags `{ITERATION}` as a "dead variable" and demands it either be consumed by templates or removed from the spec. This is a false dichotomy that misunderstands why spec authors define variables before templates consume them.

`{ITERATION}` is a forward-compatible hook. The spec defines it because the orchestrator needs to compute it anyway (to determine file paths), and exposing it as a template variable costs nothing. Removing it from the spec means a future template author who wants to add "## Iteration 3 Revision" to a template header has to go modify the spec first. Keeping it defined but unused is cheap insurance. The Purist's framework -- "every defined variable must have a consumer" -- is a compiler-era constraint that does not apply to a template system where templates evolve independently of the variable registry.

---

## Tensions

### T-1: Exhaustive Variable Audit vs. Operational Fragility

The Purist's variable audit (Section 1) is the most thorough analysis in either review. The cross-reference table catching `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` as undefined (Gap 1.1) is a genuine blocking defect -- red-blue mode cannot work without these definitions. I did not audit red-blue templates at all; my review focused on cooperative mode end-to-end. The Purist's breadth caught something my depth missed.

However, the Purist's audit of all 24 templates produces a long tail of low-severity findings (9.3 on list formatting, appendix notes on `{MODE}` usage inconsistency, prisoners-dilemma `{AGENT_DOCS}` omission) that dilute the signal. Thirteen "Missing" items at the end of the summary table makes it hard to distinguish "red-blue mode is broken" (Gap 1.1, truly blocking) from "list variables might render with or without markdown prefixes" (Gap 9.3, cosmetic). My review's tiered scorecard (Works / Fragile / Broken with P1-P3 priorities) is a more actionable format for the same class of findings.

The tension: the Purist's methodology is more rigorous and catches more, but the flat severity model (Missing / Implied / Specified) lacks the triage dimension that makes an audit actionable.

### T-2: Template Path Resolution -- Different Failure Models

Both reviews identify template path resolution as problematic. The Purist (Gap 6.1) frames it as a missing-error-message problem: what error do you show when templates are not found? I frame it (Finding 7) as a behavioral problem: the "walk up" instruction is not how LLMs naturally operate, so the first execution step is likely to fail or stall.

The Purist wants the spec to define error messages for three template-loading failure modes. I want the spec to change the resolution algorithm so the failures do not occur. These are complementary -- you need both a better algorithm and defined error behavior -- but if forced to pick one, the algorithm fix prevents the errors that the messages would report. The Purist's approach accepts the fragile algorithm and adds error reporting around it; my approach fixes the algorithm and considers error reporting secondary.

### T-3: Output Overwrite and Stale Artifacts

The Purist raises a real concern I missed entirely: Gaps 8.1 and 8.2 on re-run behavior and stale artifact cleanup. If a user removes an agent between runs, the old agent's output directory persists. This is a legitimate operational hazard.

However, the Purist's proposed fix ("the user should delete the output directory before re-running") is a documentation patch, not a design solution. If the spec is going to address re-runs at all, it should specify behavior (overwrite current, ignore stale) rather than punt to the user. But I also recognize that specifying re-run behavior for a v1 spec adds scope. The tension is whether this belongs in the initial spec or in a future iteration.

---

## Safe Agreements

### SA-1: Cross-Review Ordering Is Unambiguous

Both reviews confirm that Phase 2 cross-review directionality is fully specified. The Purist's Section 10 ("Specified. The file naming convention encodes directionality. No ambiguity.") and my Phase 2 variable audit both find the output path pattern `{output}/{REVIEWER}/cross-reviews/{REVIEWED}.md` to be clear and correct. No action needed.

### SA-2: Phase Sequencing Is Correct

Both reviews agree the iteration loop and phase ordering are well-specified. The Purist's Section 3 ("Specified, with one gap" on background mode placement) and my Finding 2a ("Works") reach the same conclusion: the diagram and rules are unambiguous. The Purist's note about `run_in_background` not being stated per-phase (Gap 3.1) is a valid documentation improvement but not a correctness issue, which aligns with my assessment.

### SA-3: Red-Blue Role Variables Are a Blocking Defect

The Purist's Gap 1.1 identifies `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` as used in red-blue templates but undefined in SKILL.md. While my review did not audit red-blue mode, this finding is unambiguously correct. Three template variables with no definition in the spec is a blocking defect for that mode. The Purist's proposed fix (explicit variable definitions mapping `config.agents[].role` to template variables) is the right solution. This should be the highest-priority fix from either review.
