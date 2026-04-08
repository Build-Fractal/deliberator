# The Mechanist: Final Disputes

**Agent**: The Mechanist (operational/engine perspective)
**Date**: 2026-03-19
**Stage**: Final disputes after revisions
**Inputs**: Revised positions from all three agents (Mechanist, Pragmatist, Purist)

---

## Remaining Disputes

### Dispute 1: `{PRIOR_FILES}` injection mechanism -- placeholder vs. runtime append

The three revisions propose incompatible injection mechanisms for `{PRIOR_FILES}`:

- **Mechanist**: Fragile, Medium. Standardize section headings OR specify injection target per mode. Keep the runtime append mechanism but fix the heading mismatch.
- **Pragmatist**: Fragile, P1. Keep runtime append. Move instruction to a standalone "Cross-Phase Injections" section. Explicitly scope to Phases 1-3 only. Reject placeholder substitution because it produces empty section headers when no prior files exist.
- **Purist**: P1. Concede to the Mechanist's placeholder approach. Replace section-appending with a `{PRIOR_FILES_SECTION}` placeholder in all Phase 1 templates that expands to a formatted block or empty string. Scope to Phase 1 only.

The Purist conceded to my mechanism critique (two injection mechanisms is worse than one) and adopted a `{PRIOR_FILES_SECTION}` placeholder. The Pragmatist explicitly rejects the placeholder, arguing it degrades prompt quality with empty section headers.

The Pragmatist's objection is technically correct -- a naive placeholder expansion to an empty string leaves orphaned headers or whitespace. But the Purist's formulation handles this: "expand to formatted block or empty string." A well-implemented placeholder that expands to nothing (not to an empty section with a header) avoids the Pragmatist's concern entirely. The placeholder does not require an empty section header; it requires a conditional expansion that is either the full block (header + paths) or nothing at all.

I side with the Purist's revised mechanism. A single injection surface (placeholder substitution) is mechanically simpler and eliminates the heading-name dependency that caused the original defect. The Pragmatist's scoping insight (Phases 1-3 only, or Phase 1 only) is valuable regardless of mechanism choice. The injection scope question (Phase 1 only vs. Phases 1-3) is a secondary decision that the arbiter should resolve; I lean toward the Pragmatist's Phase 1-3 scope because Phase 2-3 agents benefit from knowing what prior context informed the reviews they are evaluating.

This dispute is narrow but consequential: it determines the spec's injection architecture. The arbiter should rule on mechanism (placeholder vs. append) and scope (Phase 1 only vs. Phases 1-3).

### Dispute 2: `{ITERATION}` -- remove, keep as orchestrator state, or add to templates

Three distinct positions remain:

- **Mechanist**: Low severity. Either remove `{ITERATION}` from SKILL.md entirely or document it as orchestrator-only state for file-path computation. Do not inject into templates -- iteration awareness changes agent behavior in ways that are difficult to predict and test.
- **Pragmatist**: P2 (upgraded from P3). Add `{ITERATION}` to the revision template header (e.g., "Revision (Iteration {ITERATION})") so agents have explicit convergence signaling.
- **Purist**: Medium (upgraded from Low). Keep `{ITERATION}` defined, add to Phase 3 revision templates as optional convergence context, document dual purpose (orchestrator file-path computation + agent convergence signaling).

The Pragmatist and Purist converge on adding `{ITERATION}` to templates for convergence signaling. I remain the dissenting voice.

My objection is operational: injecting iteration numbers into agent prompts risks changing revision behavior in unpredictable ways. An agent told "this is iteration 3" may over-concede to reach closure, or may treat its position as more authoritative ("I have been through more rounds"). The convergence ratchet should be driven by the substance of cross-reviews, not by a meta-signal about how many rounds have elapsed. The cross-review content already carries the convergence signal -- if a cross-reviewer says "no remaining objections," the revising agent knows to converge regardless of iteration number.

However, I acknowledge the 2:1 weight against me and the Purist's functional argument (vague cross-reviews in late iterations benefit from an explicit iteration signal). If the arbiter rules for template inclusion, the variable should be presented as neutral metadata ("This is revision iteration {ITERATION}") rather than as a convergence directive ("This is a late-stage revision -- prioritize convergence").

### Dispute 3: `{TARGET_FILES}` Phase 5 -- severity classification

All three agents agree on the fix (add `{TARGET_FILES}` to Phase 5 synthesis templates and SKILL.md variable list). The dispute is classification:

- **Mechanist**: Design gap, Medium severity. The spec and templates are internally consistent (both use `{TARGET_PATH}` only). This is a design enhancement, not a contract failure.
- **Pragmatist**: Fragile, P1. Silent wrong output in multi-target adversarial modes justifies the higher priority.
- **Purist**: Medium severity. Consistent-but-insufficient, not contradictory.

The Mechanist and Purist agree on Medium. The Pragmatist rates it P1. Since the fix is identical regardless of classification, this dispute affects only prioritization. The Pragmatist's P1 argument rests on adversarial modes where agents may selectively cite sources -- a valid concern, but one that applies only to multi-file targets in adversarial modes, which is a narrow intersection. For single-file targets (the common case) and cooperative modes, the current behavior is correct.

I maintain Medium. The arbiter may reasonably upgrade to P1 if the adversarial-mode argument is deemed sufficient, but the fix should not block cooperative-mode deployment.

---

## Convergence

### Convergence 1: P0 fix is unanimous -- red-blue role variables are a blocking defect

All three agents agree without reservation that `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, and `{REVIEWED_ROLE}` must be defined in SKILL.md with explicit mappings from `config.agents[].role`. This is the single P0 item. The Pragmatist originally missed this (scoped to cooperative only) and conceded upon cross-review. The fix is identical in all three revisions: add variable definitions to the Phase 1-4 variable sections.

### Convergence 2: `{AGENT_DOCS}` must be added to Phase 2 and prisoners-dilemma templates

All three agents independently identified the `{AGENT_DOCS}` gap. The Mechanist flagged it as part of disaggregated Claim 10 (Broken, Medium). The Pragmatist initially scoped to Phase 2 cooperative only, then conceded the Purist's expansion to prisoners-dilemma Phases 3-4. The Purist promoted it from an appendix observation to the main fix list. The fix is agreed: add `{AGENT_DOCS}` to the SKILL.md Phase 2 variable list and to prisoners-dilemma `revision.md` and `disputes.md` templates.

### Convergence 3: Template structure is the enforcement surface, with no fallback

All three agents converge on the same architectural understanding. My original "zero enforcement surface" framing was challenged by both cross-reviewers and I conceded. The Pragmatist's "well-structured instructions ARE enforcement" and the Purist's "spec-template alignment is the meaningful metric" both contributed to the revised systemic finding. The shared model: templates constrain agent behavior through structural means (explicit file paths, output targets, section headings). Where templates and SKILL.md agree, the system works reliably. Where they disagree, no amount of executor intelligence compensates. The priority ordering follows directly: fix spec-template contradictions first (Broken items), then reduce ambiguity (Fragile items), then harden documentation (Low items).

### Convergence 4: Iteration file-naming boundary must be explicitly documented

All three agents independently identified the same boundary problem: when iteration N=2, the cross-review phase reads `revision.md` (the iteration-1 output with no suffix), not `revision_1.md`. The fix is a single clarifying sentence in SKILL.md. Priority is P2 across all three revisions. No disagreement on diagnosis or remedy.

### Convergence 5: Template path resolution should use a single anchor

The Pragmatist originally proposed a three-step resolution algorithm with multiple anchors. The Purist identified the multi-anchor ambiguity risk. The Pragmatist conceded and adopted the Purist's single-anchor approach: the config file's parent directory is the resolution root. I agree. The three revisions converge on: (1) resolve template directory relative to `conversus.yml` parent, (2) verify the expected template files exist post-resolution, (3) abort with a clear error message on failure.

---

## Final Position Statement

The enforcement audit process has produced a clear, prioritized fix list with broad agreement. Of the 8-10 substantive fixes identified across three independent reviews, only 3 remain in genuine dispute, and all 3 share the same remediation -- the disagreement is over mechanism, severity, or scope, not over whether the fix is needed.

The three remaining disputes are resolvable:

**Dispute 1** (`{PRIOR_FILES}` mechanism) is the most consequential. It determines the injection architecture for the spec. The placeholder approach is mechanically cleaner; the runtime append approach preserves the original design intent. I favor the placeholder, but the system works under either mechanism as long as the heading inconsistency or scope ambiguity is resolved.

**Dispute 2** (`{ITERATION}` template inclusion) is a 2:1 against me. I have stated my operational concern and acknowledged the counter-argument. The arbiter should rule.

**Dispute 3** (`{TARGET_FILES}` severity) is classification-only. The fix is identical at any priority level.

The convergence items are the more important outcome. Universal agreement on P0 (role variables), P1 (`{AGENT_DOCS}`, template path resolution), the enforcement-surface model, iteration naming, and the overall fix ordering means the spec can be updated with high confidence. The disputes are refinements within a settled structure, not challenges to the structure itself.

My final mechanist position on the enforcement audit: **the spec's enforcement depends entirely on template-SKILL.md alignment, and the revisions have identified every material misalignment.** The P0 and P1 fixes close the contract failures. The P2 fixes improve convergence quality. The P3 fixes are documentation hygiene. An implementor applying P0 + P1 can produce a working executor for cooperative and prisoners-dilemma modes, and unblock red-blue mode. The remaining disputes do not block that outcome.
