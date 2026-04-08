# Devil's Advocate — Disputes (Phase 4)

**Spec**: `008-interests-mode`
**Role**: devils-advocate
**Date**: 2026-03-22

---

## Remaining Disputes

### 1. Generated configs as "starter templates" — the spec's promise is still broken

All three revisions treat the intentionally omitted fields (`rounds`, `stagnation`, `validate_templates`, `prior`, `arbiter`) as a settled design decision. Integration-architect calls them "advanced fields that users add manually" and frames this as correct. Functional-typing does not challenge it. My own revision raised this as New Recommendation 3 but did not push hard enough.

The dispute is not about whether these fields should be auto-generated. They should not — that would expand scope beyond spec 008. The dispute is about honesty. Spec line 19 says the guided workflow eliminates "the need for users to understand game theory or YAML schemas." The implementation generates a config that is deliberately incomplete. These two statements are in direct tension, and no revision addresses the tension itself.

The fix is small: add a sentence to the spec's Feature Summary acknowledging that generated configs are ready-to-run with single-round defaults, and that multi-round deliberation, stagnation detection, prior context, and arbitration require manual YAML edits or future guided commands. This is not a P1 implementation issue — it is a P2 expectation-setting issue. But it remains unresolved across all three revisions, and the synthesis should not silently accept the contradiction between "no YAML knowledge needed" and "you need YAML knowledge for advanced features."

### 2. The `(none)` sentinel is still an ad-hoc convention with no formal definition

Integration-architect's revision (R-2) expands the scope of the `(none)` sentinel handling and proposes treating `(none)`, empty list, and missing section as equivalent. This is a good improvement. But it does not resolve the fragility I identified in my cross-review: the sentinel is a string literal in a markdown file that users may edit by hand.

Integration-architect's proposed equivalence set (`(none)`, empty list, missing section) helps with machine-authored `problem.md` files. It does not help when a user opens `problem.md` in their editor and writes "none", "N/A", "TBD", "no documents", or "TODO: add source documents." All of these are plausible human edits that express the same intent as `(none)` but would be treated as literal file paths, failing the target existence check at mode generation time.

I acknowledge this is a low-severity issue — the failure mode is a clear error message, not silent corruption. But it is symptomatic of a broader pattern: the guided workflow assumes machine-authored intermediate files while also encouraging human editing (FR-005 explicitly supports modifying `interests.md`; the define handler encourages reviewing `problem.md`). The synthesis should note this tension even if the resolution is deferred. A future spec could define a sentinel convention (e.g., any value matching `^[\[(]?(?:none|n\/a|tbd|todo)[\])]?$` case-insensitively) or use YAML frontmatter for structured fields instead of markdown sections.

### 3. Interest deduplication remains unaddressed

My original review (Missed Opportunity 4) raised the case where two interests have substantially overlapping perspectives — e.g., "backend-team" and "infrastructure-team" with near-identical prompts that would produce correlated reviews and waste agent launches. No cross-reviewer challenged this point. No revision addressed it. No one disagreed with it.

This is a gap that slipped through the process because no one contested it. It is not high-severity — users can see the interest list at confirmation time and should notice duplication themselves. But the interests handler already performs preset matching (SKILL.md lines 985-992) by comparing interest descriptions against preset catalogs. The same similarity-detection logic could flag high-overlap interests: "Interests 'backend-team' and 'infrastructure-team' have similar perspectives. Consider merging them or differentiating their prompts." This would reduce wasted launches in the N^2 cross-review phase where correlated agents produce redundant critique.

I acknowledge this is at most P2 and likely a candidate for a future spec rather than spec 008. But it should appear in the synthesis as a noted gap, not be silently dropped.

---

## Convergence

### Settled positions I accept without further challenge

**1. `interests.md` earns its keep as a separate artifact.** I conceded this in my revision and I do not revisit it. Integration-architect and functional-typing demonstrated concrete architectural dependencies — prerequisite routing, user-modified interest structures not recoverable from `problem.md`, the Perspective field being machine-consumed — that my original challenge failed to account for. The three-file chain is justified.

**2. The `ambiguous` row should be resolved by updating the spec to match the SKILL.md.** All three reviewers converge on this. The SKILL.md's heuristic detection plus user choice is superior to the spec's static `cooperative` default. The spec should drop the `ambiguous` row and reference heuristic detection with user choice as the terminal fallback. This is the cleanest consensus in the entire review cycle.

**3. Heuristic detection should be advisory, not formalized.** I conceded my demand for weighted keyword scoring. Both cross-reviewers correctly argued that demanding formal scoring for a classifier operating on freeform natural language is false precision. The fix is a single sentence stating the heuristic output is advisory and always subject to user confirmation. I accept this and will not push further.

**4. The `Preset` field belongs in the spec's `interests.md` schema.** All three reviewers agree this is a spec omission, not implementation drift. FR-006 mandates preset support; the data flow requires carrying the preset reference through `interests.md`. The field is necessary and the spec should include it.

**5. Preset existence should be validated at generation time.** All three reviewers converge on this — integration-architect's R-1 (escalated to High), my original cross-review escalation, and functional-typing's N-1. The post-write validation should check that preset files resolve, following the same pattern as docs path existence checks.

**6. CLARIFY-tagged types should route through user confirmation, not silent extraction.** Functional-typing accepted my correction on this in their revision. The define handler's `[CLARIFY:]` tag is an intentional ambiguity marker. Extracting the best-guess type and proceeding undermines that signal. The correct behavior is to ask the user to confirm the type, treating CLARIFY-tagged types as equivalent to "ambiguous."

**7. `--output` dual semantics should be documented in the spec.** Functional-typing escalated this from P2 to P1 based on my identification of the read/write override footgun. The spec should document that `--output` overrides both write and read paths, in a Common Options section.

**8. Agent-launch cost estimate belongs at mode confirmation, not interests confirmation.** Both cross-reviewers corrected my original placement. The cost can only be calculated accurately when both agent count and mode are known, which is at mode confirmation time. I conceded this in my revision and it stands.

**9. Interest-vs-type cross-validation should be a warning, not a heuristic re-invocation.** Integration-architect's cleaner mechanism — a separate validation step comparing interest naming patterns against the stated problem type, emitting a warning if inconsistent — is better than my original proposal to re-invoke heuristic detection. I conceded this in my revision.

**10. Draft status behavior should be specified.** All three reviewers independently identified this gap. The interests handler should warn when `problem.md` has `status: draft` or unresolved CLARIFY tags, but should not block. This is universally agreed.

### Positions where I yield to majority but note reservations

**11. Zero-signal edge case.** Functional-typing's N-2 proposes adding an explicit statement for the case where heuristic detection finds no signals for any mode: present all four modes and ask the user to choose. I agree this is the right behavior. My reservation is that "no signals detected" may be functionally indistinguishable from "the LLM did not look hard enough for signals" given the unformalized nature of the heuristic. But since we have all agreed the heuristic is advisory, this distinction collapses — the user always confirms regardless. I accept N-2 without further dispute.

**12. Confidence column rename.** Integration-architect suggests renaming the decision matrix column from "Confidence" to "Default Strength" or adding a footnote. I suggested dropping "High" labels entirely. Both approaches solve the same problem (the column implies empirical validation that does not exist). I prefer dropping the labels but accept that renaming the column is an adequate resolution. The synthesis can pick either.

---

## Final Position Statement

The review cycle has been productive. Of my six original recommendations, one was withdrawn (interests.md as optional — I was wrong), three were revised with better mechanisms from the cross-reviewers, and two were retained with universal agreement. The cross-review process surfaced three new recommendations that I endorse. The deliberation worked as designed: positions were challenged, the weak ones fell, the strong ones survived in refined form.

**What the synthesis must include:**

Six items have full three-reviewer consensus and should be treated as settled recommendations:

1. Update spec: replace the `ambiguous` row with reference to heuristic detection and user choice (P1)
2. Update spec: add optional `Preset` field to `interests.md` schema (P1)
3. Update SKILL.md: add preset file existence validation to post-write check (P1, High severity per integration-architect)
4. Update SKILL.md: route CLARIFY-tagged types through user confirmation (P1)
5. Update spec: document `--output` dual semantics in a Common Options section (P1)
6. Update SKILL.md: specify draft status warning behavior for the interests handler (P1)

Four items have consensus on substance with minor variation on mechanism:

7. Add heuristic-is-advisory sentence to SKILL.md (P1) — all agree, exact wording TBD
8. Add agent-launch cost estimate to mode confirmation display (P1) — all agree on placement
9. Add interest-vs-type cross-validation warning to mode handler (P1) — integration-architect's mechanism preferred
10. Add zero-signal edge case handling to heuristic detection (P2) — present all modes, ask user

**What the synthesis should note but may defer:**

11. Generated configs are starter templates — the spec's "no YAML knowledge" promise has a boundary that should be stated (P2)
12. The `(none)` sentinel needs formal definition or a more robust convention (P2)
13. Interest deduplication/overlap detection is a gap worth noting for a future spec (P2)
14. Confidence column should be renamed or footnoted to avoid implying empirical validation (P2)

**What I concede was wrong:**

- `interests.md` as optional. The separate file is architecturally necessary. I failed to account for prerequisite routing dependencies, user-modified interest structures, and the Perspective field's machine consumption.
- Demanding formalized scoring for heuristic detection. Weighted keyword scores on freeform text would be false precision. The advisory framing plus user confirmation is sufficient.
- Placing the agent-launch cost estimate at interests confirmation. Mode is not yet selected at that point; the cost formula depends on mode.

The spec is sound. The implementation is faithful and in specific cases (ambiguous-type handling, mixed-signal user choice) superior to the spec. The gaps that remain are documentation, expectation-setting, and edge-case handling — not architectural flaws. The synthesis has a clear path forward.
