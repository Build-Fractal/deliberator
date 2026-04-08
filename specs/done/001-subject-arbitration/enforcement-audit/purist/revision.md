# Purist Revision: Enforcement Audit of SKILL.md

**Author**: The Purist
**Date**: 2026-03-19
**Inputs**: Original review, cross-reviews from The Mechanist and The Pragmatist, my cross-reviews of both.

---

## Disposition of Original Findings

### Gap 1.1 — `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` undefined in SKILL.md

**HELD.**

All three reviewers agree this is the highest-priority blocking defect. The Mechanist (SA-1) confirms: "No disagreement on diagnosis, severity, or remediation." The Pragmatist (SA-3) confirms: "unambiguously correct... should be the highest-priority fix from either review." Three undefined template variables in four red-blue templates is a specification-template contract failure that prevents correct implementation of an entire mode.

Original severity and fix unchanged: add explicit variable definitions to the Phase 1, 2, 3, and 4 variable sections mapping `config.agents[].role` to the template variables.

---

### Gap 1.2 — `{ITERATION}` defined but unused by any template

**MODIFIED.** Reclassified from "dead variable" to "underutilized orchestrator-and-template variable." Severity raised from Low to Medium.

The Mechanist (DC-1) argues `{ITERATION}` may be orchestrator state, not a template variable, and that injecting iteration awareness into agents "could change their behavior." The Pragmatist (DC-3) argues it is a "forward-compatible hook" that costs nothing to keep defined.

Both critiques have merit on narrow points, but both miss the functional argument I advanced in my cross-review of the Pragmatist (DC-2): without an iteration signal in the prompt, revision agents in iteration 2+ have no explicit mechanism to distinguish a refinement pass from a first pass. Convergence depends entirely on cross-review content carrying that signal implicitly. This is fragile for vague cross-reviews.

I concede the Mechanist's point that templates should not be forced to consume the variable merely for completeness. But I reject the conclusion that it should remain defined-but-unused. The correct resolution: keep `{ITERATION}` defined, add it to Phase 3 revision templates as optional context (e.g., a metadata line: "This is revision iteration {ITERATION}"), and document in SKILL.md that the orchestrator uses it for file-path computation AND that templates may reference it for convergence signaling. This is neither the Mechanist's "remove from templates" nor the original "must have a consumer for completeness" -- it is a functional addition motivated by convergence quality.

---

### Gap 1.3 — `{PRIOR_FILES}` injection point inconsistent with template headings; dual injection mechanism

**MODIFIED.** Conceded on mechanism, held on heading inconsistency.

The Mechanist (DC-3) argues the dual mechanism (placeholder substitution + section appending) is the root problem, and proposes normalizing to a `{PRIOR_FILES_SECTION}` placeholder in every Phase 1 template. I initially defended the section-appending design in my cross-review of the Mechanist (DC-1), arguing the Mechanist's fix "papers over" the heading inconsistency.

On reflection, the Mechanist is correct that two injection mechanisms is worse than one. A single `{PRIOR_FILES_SECTION}` placeholder that expands to either the formatted block or empty string is simpler, more uniform, and eliminates the heading-name dependency entirely. If the placeholder is in the template, the heading names become irrelevant to injection.

I concede the mechanism fix to the Mechanist. The heading inconsistency ("What to Read" vs. "Files to Read") should still be standardized for readability, but it is no longer a functional defect once injection is placeholder-based. Downgraded from Medium to Low for the heading standardization; the mechanism fix is the substantive action.

---

### Gap 2.1 — 11 of 14 validation rules lack specified error messages

**MODIFIED.** Conceded on the remedy, held on the finding.

The Mechanist (DC-2) argues that specifying natural-language error templates for a system with no deterministic error renderer is "specification theater" that creates "false determinism." The Pragmatist (DC-1) argues that mandating 14 exact error strings "calcifies the spec" and flattens signal between tricky validations and obvious ones.

Both critiques land. I was wrong to propose exact message templates as if they were machine-readable contracts. The executor LLM will paraphrase regardless of what the spec says. The finding stands -- the inconsistency between 3 formal arbiter messages and 11 informal everything-else messages is real -- but the remedy changes.

Revised fix: do NOT add 11 new message templates. Instead, (1) add a general validation rule stating that all config validation errors must name the offending field, the invalid value, and the constraint violated, and (2) keep the 3 existing arbiter messages as examples of the expected format. This gives the executor sufficient guidance without creating untestable string contracts.

---

### Gap 3.1 — `run_in_background` not stated per-phase, only in bottom notes

**HELD.** Severity remains Low.

Neither cross-reviewer disputed this finding. The Pragmatist (SA-2) calls it "a valid documentation improvement but not a correctness issue." The Mechanist does not address it. Original assessment stands: the information exists but is in the wrong location. A Low-priority documentation fix.

---

### Gap 4.1 — Prior injection section heading mismatch across modes

**CONCEDED (subsumed).** This gap is resolved by the mechanism fix from Gap 1.3. Once `{PRIOR_FILES}` injection uses a placeholder rather than section appending, the heading names no longer determine injection behavior. Residual heading standardization is cosmetic and absorbed into Gap 1.3's revised fix.

---

### Gap 4.2 — Prior injection scope (Phase 1 only? all phases?) ambiguous

**HELD.** Scope is Phase 1 only.

The Pragmatist (DC-2) confirms the pragmatic reading: "Phase 1-only injection is sufficient and should be the documented behavior. The prior context propagates naturally -- Phase 1 agents absorb it into their reviews, and every subsequent phase reads those reviews." The Mechanist does not dispute this.

I agree with the Pragmatist that injecting prior context into synthesis and arbitration phases would be redundant and potentially harmful (biasing the arbiter toward prior positions). The fix: SKILL.md should explicitly state that `{PRIOR_FILES_SECTION}` (per the revised Gap 1.3 mechanism) applies only to Phase 1 review templates.

---

### Gap 5.1 — Final revision path formula not stated as single rule

**HELD.** Severity remains Low.

Both cross-reviewers agree the iteration loop mechanics are correct but need boundary clarification (Pragmatist SA-3, Mechanist implicit). The formula is inferable but never stated. Original fix: add a single explicit formula to SKILL.md.

---

### Gap 5.2 — `{ALL_REVISIONS}` scope for iterations > 1

**HELD.** Severity remains Medium.

No cross-reviewer disputed this finding. The ambiguity is real: does Phase 5 synthesis receive all intermediate revisions or only the final ones? Original fix: explicitly state that `{ALL_REVISIONS}` contains only final revision paths.

---

### Gap 5.3 — Cross-review overwrite side effect not communicated to Phase 5 agent

**HELD.** Severity remains Low.

No cross-reviewer disputed this finding or its severity.

---

### Gap 6.1 — No error behavior for missing templates

**MODIFIED.** Held on finding, modified on remedy to incorporate the Pragmatist's algorithm concern.

The Pragmatist (T-2 in the Mechanist cross-review and Finding 7 in own review) argues the resolution algorithm itself is fragile and should be fixed, not just wrapped in error messages. In my cross-review of the Pragmatist (DC-3), I noted that the Pragmatist's proposed three-step resolution introduces multi-anchor ambiguity.

Revised fix: (1) anchor template resolution to the config file's parent directory as the single root, not CWD with walk-up, and (2) specify error messages for the two remaining failure cases (template directory not found relative to config, specific template file missing). This combines the Pragmatist's insight (fix the algorithm) with the Purist's requirement (specify failure behavior), while avoiding the multi-anchor ambiguity I identified in the Pragmatist's original proposal.

---

### Gap 7.1 — Agent model selection not addressed

**HELD.** Severity remains Low.

Neither cross-reviewer disputed this finding. The spec should explicitly state that all subagents use the orchestrator's model.

---

### Gap 8.1 — Output overwrite behavior on re-run not specified

**MODIFIED.** Held on finding, modified on remedy.

The Pragmatist (T-3) correctly notes that "the user should delete the output directory" is a documentation patch, not a design solution. I concede this. But I also maintain that specifying re-run behavior in a v1 spec is appropriate because the behavior will occur naturally (users will re-run) and the result should be predictable.

Revised fix: state explicitly that the skill overwrites files produced by the current run without warning and does not delete stale files from previous runs. This documents the actual behavior rather than prescribing user action.

---

### Gap 8.2 — Stale artifact cleanup not addressed

**HELD.** Severity remains Low.

Subsumed into Gap 8.1's revised fix: documenting that stale files are not cleaned up.

---

### Gap 9.3 — List variable formatting (bare paths vs. markdown prefixed) not specified

**HELD.** Severity remains Low.

Neither cross-reviewer disputed this finding. Original fix: state that path-list variables expand to one bare absolute path per line.

---

### Additional finding from Appendix — Prisoners-dilemma missing `{AGENT_DOCS}` in Phases 3-4

**HELD and PROMOTED.** Severity raised from implicit appendix note to explicit Medium.

This was an appendix observation in my original review that I did not promote to the main gap list. The Pragmatist's audit did not catch it (DC-1 in my cross-review of Pragmatist: the `{AGENT_DOCS}` fix "misses prisoners-dilemma template omission"). The Mechanist's variable audit (Claim 10) also does not flag this specific template-level absence.

Prisoners-dilemma agents lose access to their grounding documentation in Phases 3 and 4. If intentional, SKILL.md must state this exception and its rationale. If unintentional, the templates have a bug. Either way, the spec is silent where it must speak. Promoted to the main fix list.

---

### Additional finding from cross-reviews — Agent name validation

**ADOPTED from the Pragmatist.** New finding, Medium severity.

The Pragmatist identified that agent names with special characters can cause invalid filesystem paths or silent overwrites on case-insensitive filesystems. I agreed in my cross-review (SA-2) that this is consistent with the Purist methodology: unspecified behavior is a spec bug. The proposed validation pattern (`[a-z0-9][a-z0-9-_]*`) is reasonable and should be added to config validation.

---

### Additional finding from cross-reviews — `{TARGET_FILES}` missing from Phase 5 synthesis

**ADOPTED.** Already noted in my appendix; promoted by universal agreement.

All three reviewers independently identified this. The Pragmatist calls it P1; the Mechanist calls it "Broken (partially)." In my cross-review of the Mechanist (DC-3), I argued that the spec and templates are currently consistent (both omit `{TARGET_FILES}` from Phase 5), so "Broken" is too strong. However, for multi-target deliberations, the synthesis agent genuinely needs access to all target files. This is a design enhancement that all three reviewers agree is necessary. Medium severity (the current behavior is consistent-but-insufficient, not contradictory).

---

## Prioritized Fix List

### P0 — Blocking (prevents correct implementation of a mode)

| # | Gap | Fix |
|---|---|---|
| 1 | 1.1 | Add `{AGENT_ROLE}`, `{REVIEWER_ROLE}`, `{REVIEWED_ROLE}` variable definitions to SKILL.md Phase 1-4 variable sections, mapping from `config.agents[].role` |

### P1 — High (produces incorrect output or silent degradation)

| # | Gap | Fix |
|---|---|---|
| 2 | 1.3 (revised) | Replace section-appending injection with `{PRIOR_FILES_SECTION}` placeholder in all Phase 1 review templates; expand to formatted block or empty string; scope to Phase 1 only |
| 3 | New (PD `{AGENT_DOCS}`) | Either add `{AGENT_DOCS}` to prisoners-dilemma revision.md and disputes.md templates, or document the intentional omission in SKILL.md with rationale |
| 4 | New (`{TARGET_FILES}` Phase 5) | Add `{TARGET_FILES}` to Phase 5 variable definitions and all synthesis templates for multi-target support |
| 5 | 6.1 (revised) | Anchor template resolution to config file parent directory; specify error messages for template-directory-not-found and template-file-missing |

### P2 — Medium (ambiguity that affects output quality or causes confusion)

| # | Gap | Fix |
|---|---|---|
| 6 | 1.2 (revised) | Add `{ITERATION}` to Phase 3 revision templates as convergence context; document dual purpose (orchestrator file-path computation + agent convergence signaling) |
| 7 | 5.2 | Explicitly state `{ALL_REVISIONS}` contains only final revision paths, not intermediate |
| 8 | 2.1 (revised) | Add general validation-error format rule (name field, value, constraint) instead of 11 exact message templates; keep 3 existing arbiter messages as examples |
| 9 | 8.1 (revised) | Document overwrite-without-warning behavior for current-run files; document that stale files from removed agents are not cleaned |
| 10 | New (agent names) | Add agent name validation rule to config schema: `[a-z0-9][a-z0-9-_]*` |

### P3 — Low (documentation improvements, cosmetic, forward-compatibility)

| # | Gap | Fix |
|---|---|---|
| 11 | 5.1 | State the final-revision-path formula as a single explicit rule with the iteration-1 special case |
| 12 | 3.1 | Elevate `run_in_background` directive to phase execution headers or add per-phase execution mode |
| 13 | 7.1 | State explicitly that all subagents use the orchestrator's model |
| 14 | 9.3 | State that path-list variables expand to one bare absolute path per line, no prefix characters |
| 15 | 5.3 | Note in Phase 5 variable definitions that cross-reviews represent only the final iteration |
| 16 | 4.2 | Add explicit "Phase 1 only" scope qualifier to prior-files injection (may be subsumed by P1 #2) |

---

## Concession Summary

| Original Position | Conceded To | Reason |
|---|---|---|
| Gap 1.3: Fix heading inconsistency to repair injection | Mechanist: Replace dual mechanism with single placeholder | One injection mechanism is simpler; heading names become irrelevant to function |
| Gap 2.1: Add 11 exact error message templates | Mechanist + Pragmatist: Specify format rule, not exact strings | LLM executor cannot produce deterministic messages; exact templates are untestable |
| Gap 4.1: Standardize section headings across modes | Subsumed by Gap 1.3 concession | Placeholder mechanism eliminates heading dependency |
| Gap 8.1: "User should delete output directory" | Pragmatist: Document actual behavior, not user action | Spec should describe system behavior, not prescribe workarounds |

## Items Held Against Critique

| Original Position | Challenged By | Why Held |
|---|---|---|
| Gap 1.1: Blocking defect, red-blue mode broken | None (universal agreement) | All three reviewers confirm |
| Gap 1.2: Should not remain defined-but-unused | Mechanist (orchestrator state) + Pragmatist (forward hook) | Functional convergence argument outweighs both: agents need iteration awareness for quality |
| Gap 5.2: `{ALL_REVISIONS}` ambiguity is Medium | None | Uncontested |
| Gap 6.1: Missing template error behavior | Pragmatist (fix algorithm instead) | Both are needed; algorithm fix does not eliminate need for specified error behavior |
| Gap 7.1: Model selection must be stated | None | Uncontested |
| Gap 9.3: Path format must be specified | None | Uncontested |
