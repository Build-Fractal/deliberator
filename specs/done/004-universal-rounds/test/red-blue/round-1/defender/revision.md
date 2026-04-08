# Defender Revision: Spec 004 — Universal Rounds, Stagnation Detection, and Arbitration

**Role**: Blue Team Defender (revised position after cross-reviews)
**Date**: 2026-03-20
**Revision basis**: Original defense brief, Red Team cross-review of defense, Blue Team cross-review of attack

---

## Revision Summary

The Red Team's cross-review exposed three genuine blind spots in the original defense. The most damaging was a category error: the defense verified that the engine POPULATES round-aware variables for all modes but never verified that the TEMPLATES CONSUME them. This is precisely the failure that the defense's own architectural thesis ("all mode-specific behavior lives in templates") should have predicted. When templates are the mode-specific layer, template completeness is the correctness condition -- not engine completeness.

Three defense points are withdrawn, two are modified, and five survive. The overall position shifts from "spec 004 is correct and complete" to "spec 004's engine changes are correct, but the template layer has three gaps that must be remediated before non-cooperative multi-round runs are production-ready."

---

## Point-by-Point Classification

### 1. "All mode-specific behavior lives in templates, not the engine" (Architecture Rationale)

**Classification: SURVIVING**

The Red Team explicitly concedes this point in their cross-review (Conceded Points, item 1): "The defender's analysis of the round loop, stagnation detection algorithm, Phase 6 trigger evaluation, and template loading as mode-agnostic code paths is correct and well-evidenced." The engine IS mode-agnostic. The round loop, stagnation detection, Phase 6 trigger evaluation, and template variable population are mode-unaware code paths.

However, the Red Team correctly observes that this architectural argument is a double-edged sword: if templates carry all mode-specific behavior, then template incompleteness means feature incompleteness. The defense used this thesis to justify removing engine guards but failed to apply it to verifying template readiness. The architecture rationale survives as a correct description of the system; the failure was in the defense's APPLICATION of the thesis, not in the thesis itself.

### 2. "Template Variable Completeness" -- Evidence 5 and Evidence 2 (same variable set claims)

**Classification: WITHDRAWN**

The Red Team's cross-review is correct and the defense's claim is verifiably false. The original defense stated:

- Evidence 2: "Same template variables: Yes" across all arbitration templates.
- Evidence 5: "The arbitration templates use the same variable set as the cooperative template."

These claims were based on checking the spec's variable LIST (spec.md L144), not the actual template content. The cooperative arbitration template (`templates/cooperative/arbitration.md` L38) contains `{REMAINING_DISPUTES}`. The red-blue, winner-take-all, and prisoners-dilemma arbitration templates do not contain this variable anywhere. This is confirmed by grep across all templates under `templates/`.

Similarly, the defense's claim of Phase 1 template variable completeness (implicit in the "engine populates variables for all modes" argument) confused population with consumption. The cooperative review template (`templates/cooperative/review.md` L21) contains `{PRIOR_ROUND_SECTION}`. The three non-cooperative review templates do not. The orchestrator populates the variable, but the templates never include it, so the expansion is never injected into the agent's prompt.

The defense committed the exact category error the Red Team identified: conflating variable availability with variable usage. This was the most significant analytical failure in the original defense.

### 3. "Dispute-Parsing Subsystem was already mode-aware" (Evidence 4)

**Classification: MODIFIED**

The original defense argued that since the Dispute-Parsing Subsystem already had mode-specific fallback headings for all four modes, extending to non-cooperative modes required no new parsing logic. This is partially correct: the subsystem IS mode-aware and no new parsing code is needed. But the defense understated two problems:

**Modification 1 -- WTA stagnation direction error**: The original defense's Limitation 5 stated that WTA stagnation detection "may miss stagnation in some cases (leading to extra rounds) but will not falsely declare stagnation." The Red Team correctly identifies this as backwards. When structural markers are absent and the heading-based fallback fires, `## Runner-Up` is always present in WTA synthesis (it is a mandatory section), so the boolean is always true and the "count" is effectively always 1. Round 1 count = 1, Round 2 count = 1: stagnation IS declared (count >= prior count). The fallback causes premature stagnation detection, not missed stagnation. The defense got the failure direction wrong.

However, the defense's cross-review of the attacker correctly noted that the PRIMARY path (structural markers present) handles WTA correctly. The WTA per-round synthesis template DOES include `DISPUTES_BEGIN`/`DISPUTES_END` markers around `### Remaining Disputes`, and the marker-based path counts entries within that range. The fallback heading problem only manifests when the LLM drops the structural markers from its output. This is a possible but not certain failure mode. The severity is real but the likelihood is conditional.

**Modification 2 -- Cross-round synthesis markers absent**: The original defense's Safeguard 2 discussed the three-tier fallback as a defense mechanism but only examined per-round synthesis templates. The cross-round synthesis templates for ALL four modes (including cooperative) lack `DISPUTES_BEGIN`/`DISPUTES_END` markers. This means that for multi-round runs, when Phase 6 reads the "definitive synthesis" (`{output}/summary/final.md`), it always falls to heading-based parsing. The defense never verified whether the NEW cross-round synthesis templates honor the stable interface contract stated at SKILL.md L683.

**Revised position**: The Dispute-Parsing Subsystem is mode-aware as claimed, and the primary marker-based path works correctly for per-round synthesis. But the defense failed to verify (a) that WTA's fallback heading produces the correct failure mode, and (b) that cross-round synthesis templates honor the marker contract. Both are genuine gaps.

### 4. "Draft-gate mechanism was a real safeguard" (Safeguard 1)

**Classification: SURVIVING**

The Red Team concedes this point explicitly (Conceded Points, item 2): "The defender's analysis of the `TEMPLATE_STATUS: draft` mechanism as defense-in-depth is convincing." The system had two layers of protection (validation rules + draft markers), both were removed simultaneously when the feature was ready, and no draft markers remain in any template. This defense point is unchallenged.

### 5. "Dispute-Parsing Subsystem default-to-true is the correct failure mode" (Safeguard 2, partial)

**Classification: SURVIVING**

The Red Team concedes this point (Conceded Points, item 4): "The defender correctly identifies that the Dispute-Parsing Subsystem's default behavior (return true / has disputes when parsing fails) is the correct failure mode. Running an unnecessary arbitration is preferable to skipping a necessary one."

The Red Team's critique is about extraction QUALITY (heading-based parsing is less precise than marker-based parsing), not about the trigger DECISION (whether Phase 6 runs or not). The defense's analysis of the trigger decision is correct: default-to-true is the safe failure mode. The quality degradation from heading-based fallback is a valid concern addressed under point 3 above, but it does not undermine this specific safeguard.

### 6. "Phase 6 output validation headings match templates" (Safeguard 3)

**Classification: SURVIVING**

The Red Team confirmed that SKILL.md L587-592 and the actual template headings agree. The spec's FR-009 headings are different, but the defense correctly identified this as a spec documentation gap (Limitation 1), not a functional issue. The Red Team downgraded THREAT-04 from HIGH to MEDIUM in their cross-review, agreeing it is documentation drift. SKILL.md L594 explicitly directs maintainers to treat templates as the source of truth.

### 7. "Cooperative mode isolation is verified" (Safeguard 5)

**Classification: SURVIVING**

The Red Team concedes this point (Conceded Points, item 3): "The defender's claim that no cooperative-mode artifact was modified is verifiable and correct." No cooperative template was changed. The SKILL.md validation table change was additive (new rows; cooperative row unchanged). Phase 6 failure handling is mode-agnostic and was not modified.

The Red Team correctly notes that this safeguard is irrelevant to the FORWARD completeness problem -- the issue is not that cooperative artifacts were harmed, but that non-cooperative artifacts were left incomplete. This criticism is valid but does not undermine the safeguard's claim, which is specifically about backward compatibility.

### 8. "Phase 6 failure handling is mode-agnostic and adequate" (Safeguard 4)

**Classification: SURVIVING**

The Red Team concedes this point (Conceded Points, item 5): "The defender correctly notes that Phase 6 failure handling applies equally to all modes and was not modified by spec 004." If Phase 6 fails, partial output is cleaned up and the Phase 1-5 record remains valid. This safety net applies equally to all modes.

### 9. "Structural consistency across cross-round synthesis templates" (Evidence 1)

**Classification: MODIFIED**

The original defense cataloged structural parity across the four cross-round synthesis templates (same variable set, same section types, same rules). This structural consistency is real -- the templates DO follow a common pattern with mode-appropriate adaptations. The Red Team does not dispute the structural elements cataloged in the defense's table.

However, the defense missed that ALL four cross-round synthesis templates (including cooperative) lack the `DISPUTES_BEGIN`/`DISPUTES_END` structural markers. The structural consistency claim is correct at the template-design level but incomplete at the interface-contract level. The templates are structurally consistent with EACH OTHER but inconsistent with the stable interface contract (SKILL.md L683) that per-round synthesis templates honor.

**Revised position**: The cross-round synthesis templates are structurally consistent with each other (Evidence 1 table survives) but all four violate the structural marker contract. This is not a spec-004-specific regression -- the cooperative cross-round synthesis template (from spec 002) also lacks markers. Spec 004's templates are consistent with the existing cooperative template. The gap is real but predates spec 004.

### 10. "Heading-level inconsistency is cosmetic" (Limitation 4)

**Classification: MODIFIED**

The original defense dismissed the PD cross-round synthesis template's use of `## Disputed Boundaries` (heading level 2) versus `###` (heading level 3) in other modes as "a minor cosmetic issue." The Red Team argues this affects content extraction scope: a `##` heading encompasses all `###` content below it until the next `##`, meaning heading-based extraction captures a broader scope.

The defense's claim that "heading matching is level-insensitive" (SKILL.md L681) is correct for FINDING the heading. But the Red Team raises a valid concern about how much content falls "under" the heading for extraction purposes. The Dispute-Parsing Subsystem extracts content beneath a heading until the next heading of equal or higher level. A `##` heading captures more downstream content than a `###` heading.

**Revised position**: The heading-level inconsistency is not purely cosmetic. It affects extraction scope in the heading-based fallback path. However, the practical impact is limited: the PD disputes section is the last major section in the cross-round synthesis template, so the `##` heading does not inadvertently capture unrelated content below it. The concern is valid in principle but low-impact in the current template layout.

---

## Concessions to Red Team

### Concession 1: THREAT-01 is CRITICAL and undefended

The Red Team is correct. The missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates is the highest-severity finding. The defense never examined whether existing Phase 1 templates for non-cooperative modes contain round-aware variables. The defense focused entirely on the NEW templates (cross-round synthesis, arbitration) and verified their completeness, while ignoring the EXISTING templates that needed updating.

The fix is straightforward: add `{PRIOR_ROUND_SECTION}` to `templates/red-blue/review.md`, `templates/winner-take-all/review.md`, and `templates/prisoners-dilemma/review.md`. Without this fix, Round 2+ agents in non-cooperative modes receive no instruction to read or engage with the prior round's synthesis, defeating the purpose of multi-round deliberation.

There IS a partial mitigation: the orchestrator populates `{PRIOR_SYNTHESIS_PATH}` for all templates (SKILL.md L339, L359), and this path is substituted into the template via general variable substitution. An LLM agent receiving a path variable may follow it. But the INSTRUCTIONAL block -- "You MUST engage with the prior round's synthesis" -- is absent. The difference between having a path and having explicit instructions to read and engage with that path is material. The defense concedes this is a real gap.

### Concession 2: THREAT-02 is a valid quality gap

The non-cooperative arbitration templates do not include `{REMAINING_DISPUTES}` or a fallback instruction. The cooperative template provides pre-extracted disputes and handles the empty-extraction case explicitly. This asymmetry is real.

The defense maintains that the severity is MEDIUM rather than HIGH: the non-cooperative templates explicitly direct the arbiter to the correct synthesis section ("Pay special attention to the synthesis's 'Disputed Risks' section"), and the arbiter is an LLM agent receiving the full synthesis as a readable document. The pre-extraction is a quality-of-life improvement, not a structural requirement. But the gap exists and should be remediated.

### Concession 3: THREAT-10 is a valid interface contract violation

The cross-round synthesis templates for ALL four modes lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers. This violates the stable interface contract at SKILL.md L683. The defense's Safeguard 2 analysis applied to per-round synthesis but never checked cross-round synthesis.

Notably, this gap predates spec 004 -- the cooperative cross-round synthesis template (from spec 002) also lacks these markers. Spec 004's three new cross-round synthesis templates are consistent with the existing cooperative template. The gap is real, but it is inherited, not introduced.

### Concession 4: WTA stagnation failure direction was wrong

The defense's Limitation 5 stated "may miss stagnation" when the actual failure mode (in the heading-based fallback path) is "always detects stagnation" (premature termination at Round 2). The Red Team's analysis is correct: when markers are absent and the fallback heading `## Runner-Up` fires, stagnation is always detected because the heading is always present. The defense got the direction of the failure wrong.

---

## Surviving Defenses

1. **Engine mode-agnosticism**: The round loop, stagnation detection algorithm, Phase 6 trigger evaluation, template loading, and variable population are mode-agnostic. This is confirmed by both teams and is the architectural foundation that makes spec 004 possible.

2. **Draft-gate mechanism**: The `TEMPLATE_STATUS: draft` safeguard was a real defense-in-depth mechanism that was properly managed. Conceded by Red Team.

3. **Default-to-true failure mode**: The Dispute-Parsing Subsystem's default behavior (return true when parsing fails) is the correct failure mode for Phase 6 triggering. Conceded by Red Team.

4. **Cooperative backward compatibility**: No cooperative-mode artifact was modified. The Phase 6 heading validation table change was additive. The cooperative row matches the cooperative arbitration template. Verified by both teams.

5. **Phase 6 failure handling**: Mode-agnostic cleanup and preservation of Phase 1-5 record. Conceded by Red Team.

6. **Phase 6 validation headings**: SKILL.md and templates agree. Spec FR-009 is stale documentation, not a functional issue. Acknowledged by both teams.

7. **Cross-round synthesis structural consistency**: The four templates follow the same structural contract with mode-appropriate adaptations. The Red Team does not dispute this. The marker absence is a separate concern (Concession 3).

---

## Position Summary

The original defense's thesis -- "spec 004 is correct, complete, and safe because the engine is mode-agnostic and the templates provide mode-specific behavior" -- was architecturally sound but operationally incomplete. The defense correctly identified the engine's mode-agnosticism and verified the NEW artifacts (cross-round synthesis templates, arbitration templates, validation table). The defense failed to verify the EXISTING artifacts (Phase 1 review templates for non-cooperative modes) and committed a category error by conflating variable population with variable consumption.

**Revised overall assessment**: Spec 004's engine changes (removing validation guards, adding Phase 6 heading rows) are correct and safe. The new templates (cross-round synthesis, arbitration) are structurally sound and follow the cooperative templates' patterns. Three gaps require remediation before non-cooperative multi-round runs are production-ready:

| Priority | Issue | Fix | Source |
|----------|-------|-----|--------|
| P1 | `{PRIOR_ROUND_SECTION}` absent from non-cooperative review templates | Add the variable to `templates/{red-blue,winner-take-all,prisoners-dilemma}/review.md` | THREAT-01 (conceded) |
| P2 | `DISPUTES_BEGIN`/`DISPUTES_END` markers absent from all cross-round synthesis templates | Add markers to all four `cross-round-synthesis.md` templates (including cooperative -- inherited gap) | THREAT-10 (conceded) |
| P2 | `{REMAINING_DISPUTES}` absent from non-cooperative arbitration templates | Add the variable and fallback instruction to all three non-cooperative arbitration templates | THREAT-02 (conceded) |
| P3 | WTA fallback heading `## Runner-Up` causes premature stagnation | Change WTA fallback heading to `### Remaining Disputes` in SKILL.md L675 | THREAT-05 (conceded direction error) |
| P3 | Spec FR-009 heading table stale | Update spec.md to match SKILL.md/template reality | THREAT-04 (acknowledged) |

None of these gaps represent engine-level correctness failures. They are template-layer completeness issues that the spec's "template-first" approach should have caught during implementation. The engine architecture is validated -- it IS mode-agnostic as claimed. The templates need finishing.

**Final verdict**: Spec 004 is architecturally correct but template-incomplete. The defense's core thesis (engine mode-agnosticism enables template-first extension) is confirmed by both teams. The Red Team's strongest contribution was exposing the template completeness gap that the defense's own thesis should have predicted. With the five remediation items above, spec 004 achieves its stated goal of extending rounds, stagnation detection, and arbitration to all four competition modes.
