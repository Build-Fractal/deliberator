# Cross-Review of Defender's Brief: Spec 004 — Universal Rounds

**Role**: Red Team Attacker (cross-reviewing Blue Team defense)
**Date**: 2026-03-20
**Verdict**: The defense is well-structured and architecturally literate but fails to address the most dangerous attack vectors. Three CRITICAL/HIGH threats from my review are either ignored or dismissed with arguments that do not survive scrutiny.

---

## Undefended Attack Surfaces

These are threats from my review that the defender's brief either does not mention or mentions only in passing without adequate defense.

### 1. THREAT-01: Missing `{PRIOR_ROUND_SECTION}` in non-cooperative Phase 1 templates (CRITICAL) -- UNDEFENDED

This is the single most dangerous finding in my review, and the defender does not address it at all.

The defender's brief makes a sweeping claim at L35-36: "the round loop, stagnation detection, and Phase 6 dispatch are mode-unaware code paths." This is true of the engine. But the engine is not where round-awareness fails -- it fails in the templates. The defender's own architecture rationale (L66-73) argues that "all mode-specific prompt engineering [lives] in templates, not in the orchestrator." This is precisely the problem: **the non-cooperative templates do not contain the round-awareness instructions.**

I verified this again during cross-review:
- `templates/cooperative/review.md` L21: contains `{PRIOR_ROUND_SECTION}`.
- `templates/red-blue/review.md`: does not contain `{PRIOR_ROUND_SECTION}` or any round-aware variable.
- `templates/winner-take-all/review.md`: same -- no round-aware variables.
- `templates/prisoners-dilemma/review.md`: same -- no round-aware variables.

The defender's Evidence 5 (L203-206) states: "The cross-round synthesis templates use the same variable set as the cooperative template" and "The arbitration templates use the same variable set as the cooperative template." This evidence addresses the NEW templates (cross-round synthesis and arbitration) but completely ignores the EXISTING Phase 1-5 templates. The Phase 1 review templates for non-cooperative modes were written before spec 004 and were never updated to include `{PRIOR_ROUND_SECTION}`. Spec 004's FR-010 says to verify that round-aware variables "populate for all modes" -- the defender confirms population (Evidence 5) but never verifies consumption.

The defender's Safeguard 5 (L126-136) claims "No cooperative-mode artifact was modified" and lists untouched items. This safeguard is irrelevant to the attack -- the problem is that non-cooperative artifacts were also not modified when they needed to be. The defender confused "backward compatibility" with "forward completeness."

**Verdict**: The defender's entire architectural argument ("templates contain mode-specific behavior; the engine is mode-agnostic; therefore removing engine guards is sufficient") actually strengthens the attack. If templates are the carriers of mode-specific behavior, then templates that lack round-awareness instructions produce agents that are round-unaware. The engine populating `{PRIOR_ROUND_SECTION}` is necessary but not sufficient -- the template must also include it. The cooperative template does; the others do not. This is a template authoring omission that the defense never examines.

### 2. THREAT-02/THREAT-07: Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates (HIGH) -- UNDEFENDED

The defender's brief does not mention `{REMAINING_DISPUTES}` anywhere. Zero occurrences. The defender's Evidence 5 (L206) states the arbitration templates use "the same variable set as the cooperative template" and lists `{REMAINING_DISPUTES}` in the variable enumeration. But this refers to the spec's variable LIST, not to the templates' actual variable USAGE.

I verified again:
- `templates/cooperative/arbitration.md` L34-40: includes `## Extracted Remaining Disputes` section with `{REMAINING_DISPUTES}`.
- `templates/red-blue/arbitration.md`: no occurrence of `{REMAINING_DISPUTES}`.
- `templates/winner-take-all/arbitration.md`: no occurrence of `{REMAINING_DISPUTES}`.
- `templates/prisoners-dilemma/arbitration.md`: no occurrence of `{REMAINING_DISPUTES}`.

The defender's Evidence 2 (L164-180) catalogs structural elements of the arbitration templates (subject-as-arbiter framing, grounding citation, scope limited to disputes, same template variables, etc.) and declares parity. The "Same template variables" row says "Yes" for all modes. This is verifiably false for `{REMAINING_DISPUTES}`. The cooperative template consumes this variable; the other three do not. The defender either did not check actual template content or conflated the spec's variable specification with template implementation.

**Verdict**: The arbitration templates for non-cooperative modes instruct the arbiter to "Pay special attention to the synthesis's 'Disputed Risks/Boundaries' section" (a prose instruction) instead of providing pre-extracted disputes via `{REMAINING_DISPUTES}`. This degrades arbitration precision. The cooperative template handles the empty-extraction case with a fallback instruction ("If this section is empty, read the full synthesis to identify any remaining disputes" -- L40). The non-cooperative templates have no such scaffolding. The defender claims parity but the templates are structurally asymmetric.

### 3. THREAT-10: Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers (HIGH) -- UNDEFENDED

The defender does not mention structural markers in cross-round synthesis templates at all. The defender's Safeguard 2 (L92-100) discusses the Dispute-Parsing Subsystem's three-tier fallback (markers, headings, default-to-true) as a defense mechanism. But this safeguard analysis only examines the per-round Phase 5 synthesis templates, not the cross-round synthesis templates.

I verified again:
- All four per-round synthesis templates contain `DISPUTES_BEGIN`/`DISPUTES_END` markers.
- Zero cross-round synthesis templates contain these markers.

For multi-round runs with an arbiter, Phase 6 reads the cross-round synthesis (`{output}/summary/final.md`) -- not the per-round synthesis. SKILL.md L540 is explicit: "Read the definitive synthesis output file (`{output}/summary/final.md`). For multi-round runs, this is the cross-round synthesis." Since the cross-round synthesis lacks markers, dispute extraction always falls to the degraded heading-based fallback for multi-round runs.

The defender's Safeguard 2 default-to-true behavior (L98-100) does prevent Phase 6 from being skipped. But it does not address the quality of `{REMAINING_DISPUTES}` extraction -- which falls back to heading-based parsing or empty string. Combined with THREAT-02 (non-cooperative arbitration templates do not consume `{REMAINING_DISPUTES}` anyway), the compound effect is that multi-round non-cooperative arbitration receives no pre-extracted disputes from any pathway.

**Verdict**: The defender's fallback analysis is correct in isolation (default-to-true prevents Phase 6 from being skipped) but misses the quality degradation. The marker contract stated at SKILL.md L683 is violated by the cross-round synthesis templates, and the defender does not address this.

---

## Weak Defenses

These are arguments the defender made that do not withstand scrutiny.

### 1. "Same template variables" claim (Evidence 2 and Evidence 5)

The defender's Evidence 2 (L172) states all arbitration templates have "Same template variables: Yes" across all modes. Evidence 5 (L206) states arbitration templates "use the same variable set as the cooperative template." Both claims are incorrect. The cooperative arbitration template uses `{REMAINING_DISPUTES}` (L38); the other three do not. The defender appears to have checked the spec's variable LIST (spec.md L144, which lists `{REMAINING_DISPUTES}` in the variable set for FR-006/007/008) and assumed the templates implemented the full list. They did not verify actual template content.

This is a category error: the spec defines what variables SHOULD be available to templates; it does not guarantee templates USE them. Population and consumption are independent. The defender's architectural argument (templates are the mode-specific layer) actually requires checking template content, not spec variable lists.

### 2. "Dispute-Parsing Subsystem was already mode-aware" (Evidence 4, L196-201)

The defender argues that since the Dispute-Parsing Subsystem already had mode-specific fallback headings for all four modes, "stagnation detection and Phase 6 trigger evaluation for the new modes use the same parsing code path that has been tested with cooperative mode." This is partially correct but obscures a critical problem: the WTA fallback heading (`## Runner-Up`) is a section that is always present in WTA synthesis, not a disputes section. It is a boolean presence check masquerading as a dispute-count mechanism.

The defender acknowledges this in Limitation 5 (L243-248) but underestimates its severity. The defender says "it may miss stagnation in some cases (leading to extra rounds) but will not falsely declare stagnation." This analysis is backwards. When structural markers are absent and the fallback fires, `## Runner-Up` is always present, so the boolean is always true, and the "count" is always 1. Round 1 count = 1, Round 2 count = 1: stagnation IS declared (count >= prior). The fallback does not cause missed stagnation -- it causes false stagnation on Round 2 for every WTA run where the LLM drops the structural markers.

### 3. "Heading-level inconsistency is a minor cosmetic issue" (Limitation 4, L233-241)

The defender identifies that the PD cross-round synthesis template uses `## Disputed Boundaries` (heading level 2) while other modes use `###` (heading level 3). The defender dismisses this as "a minor cosmetic issue, not a functional one" because "heading matching is level-insensitive" (L241).

This is correct for the Dispute-Parsing Subsystem. But it ignores a different concern: the heading level determines what content falls "beneath" a heading for extraction purposes. A `##` heading encompasses all `###` content below it until the next `##`, while a `###` heading only encompasses content until the next `###` or higher. If heading-based extraction reads "content under" the heading, a `##` heading captures a much larger scope than a `###` heading. This is not purely cosmetic -- it affects how much content the heading-based fallback extracts.

### 4. "Validation is informational, not blocking" used as a safety net (Safeguard 3, L119)

The defender repeatedly notes that Phase 6 output validation is "informational (warning, not blocking)" as evidence of resilience. This is double-edged. If the validation is informational, it provides no enforcement. A template that produces output missing required headings will succeed silently with only a warning. The defender treats non-blocking validation as a safeguard ("malformed output is better than no output"), but it is also a gap: there is no mechanism to REQUIRE correctly structured output from the new non-cooperative arbitration templates. The templates are untested at runtime (the defender acknowledges this in Limitation 3), and the only validation that exists is non-blocking.

---

## Conceded Points

These are areas where the defender's analysis is genuinely strong and my attack does not apply or has been adequately addressed.

### 1. Engine mode-agnosticism is real (Architecture Rationale, L35-44)

The defender's analysis of the round loop, stagnation detection algorithm, Phase 6 trigger evaluation, and template loading as mode-agnostic code paths is correct and well-evidenced with specific SKILL.md line references. My attacks do not dispute that the engine is mode-agnostic -- they dispute that mode-agnostic engine + mode-incomplete templates = correct behavior. The defender correctly identifies the architecture; the failure is in template completeness, not engine design.

### 2. Draft-gate mechanism was a real safeguard (Safeguard 1, L80-91)

The defender's analysis of the `TEMPLATE_STATUS: draft` mechanism as defense-in-depth is convincing. The system had two layers of protection (validation rules + draft markers), and both were removed simultaneously when the feature was ready. The defender verified that no draft markers remain. This is a genuine safeguard that was properly managed.

### 3. Cooperative mode isolation is verified (Safeguard 5, L126-136)

The defender's claim that no cooperative-mode artifact was modified is verifiable and correct. The cooperative review template, cooperative arbitration template, and cooperative cross-round synthesis template were not changed. The SKILL.md validation table change was additive (new rows; cooperative row unchanged). THREAT-12 from my review acknowledged this as LOW severity and the defender's verification is adequate.

### 4. Default-to-true is the correct failure mode for Phase 6 triggering (Safeguard 2, L92-100)

The defender correctly identifies that the Dispute-Parsing Subsystem's default behavior (return true / has disputes when parsing fails) is the correct failure mode. Running an unnecessary arbitration is preferable to skipping a necessary one. My attacks do not dispute this design -- they address the quality of dispute extraction, not the boolean trigger decision.

### 5. Phase 6 failure handling is mode-agnostic and adequate (Safeguard 4, L121-124)

The defender correctly notes that Phase 6 failure handling (clean up partial output, preserve Phase 1-5 record) applies equally to all modes and was not modified by spec 004. This is a genuine safety net.

### 6. Spec-implementation heading mismatch is acknowledged honestly (Limitation 1, L212-219)

The defender proactively identifies the three-way heading mismatch between spec FR-009, SKILL.md, and templates. The defender correctly concludes that the implementation chose to align with template content rather than spec text, and that the spec needs updating. This matches my THREAT-04 finding. The defender's honesty here is appropriate.

---

## Risk Reassessment

After reading the defense, my severity assessments are updated as follows:

| Threat | Original Severity | Updated Severity | Rationale |
|--------|-------------------|------------------|-----------|
| THREAT-01 (Missing `{PRIOR_ROUND_SECTION}`) | CRITICAL | **CRITICAL** | Undefended. Defender's architecture argument actually strengthens the attack. If templates carry mode behavior, then templates without round-awareness produce round-unaware agents. |
| THREAT-02 (Missing `{REMAINING_DISPUTES}`) | HIGH | **HIGH** | Undefended. Defender claims variable parity but did not verify template content. |
| THREAT-03 (`{ROUND}`, `{MAX_ROUNDS}` unused in non-coop templates) | MEDIUM | **MEDIUM** | Not addressed by defender. Confirmed that cooperative template gets round context via `{PRIOR_ROUND_SECTION}` expansion, not via direct `{ROUND}` usage. Non-cooperative templates have neither path. |
| THREAT-04 (Spec/SKILL.md heading mismatch) | HIGH | **MEDIUM** | Downgraded. Defender acknowledged this honestly in Limitation 1 and correctly identified that SKILL.md aligns with templates. The risk is documentation drift, not functional failure. |
| THREAT-05 (WTA stagnation uses `## Runner-Up`) | MEDIUM | **HIGH** | Upgraded. Defender's analysis in Limitation 5 is backwards -- the fallback causes false stagnation (always triggers on Round 2), not missed stagnation. The defender misanalyzed the direction of the error. |
| THREAT-06 (WTA has no countable entry pattern) | MEDIUM | **MEDIUM** | Not substantively addressed. Defender's Limitation 5 acknowledges the indirectness but does not address the absence of a parseable entry pattern for counting. |
| THREAT-07 (Non-coop arbitration lacks dispute-extraction section) | MEDIUM | **MEDIUM** | Compound of THREAT-02. Undefended. |
| THREAT-08 (Red-blue heading mismatch, spec vs impl) | LOW | **LOW** | Subsumed by THREAT-04. Defender acknowledged. |
| THREAT-09 (Red-blue Phase 4 uses wrong heading) | LOW | **LOW** | Unaddressed but limited blast radius. Phase 4 outputs are not parsed by the Dispute-Parsing Subsystem. |
| THREAT-10 (Cross-round synthesis lacks markers) | HIGH | **HIGH** | Undefended. Defender's fallback analysis applies to per-round synthesis, not cross-round synthesis. |
| THREAT-11 (Stagnation + arbitration conflicting narrative) | LOW | **LOW** | Unaddressed but genuinely low severity. User-experience concern only. |
| THREAT-12 (Cooperative backward compat) | LOW | **LOW** | Adequately defended. Verification was provided. |

### Summary of Post-Defense Risk Profile

- **CRITICAL (1)**: THREAT-01 -- Undefended. Multi-round non-cooperative runs will produce parallel independent analyses instead of iterative deepening. This defeats the stated purpose of the feature.
- **HIGH (3)**: THREAT-02, THREAT-05, THREAT-10 -- All undefended or misanalyzed. These create systematic quality degradation in non-cooperative arbitration and false stagnation detection in WTA mode.
- **MEDIUM (3)**: THREAT-03, THREAT-06, THREAT-07 -- Unaddressed but with less severe immediate impact.
- **LOW (4)**: THREAT-04, THREAT-08, THREAT-09, THREAT-11, THREAT-12 -- Either acknowledged by defender or limited in blast radius.

### Bottom Line

The defender built a strong architectural case for WHY the engine design supports universal rounds. That argument is correct. But the defense never verified that the TEMPLATES support universal rounds. The defender's own thesis -- "all mode-specific behavior lives in templates" -- is the precise reason that template completeness matters. The defense treated template creation as a solved problem (Evidence 1 and 2 catalog structural parity in the NEW templates) while ignoring that the EXISTING non-cooperative Phase 1 templates were never updated for round-awareness. This is the blind spot that makes THREAT-01 critical: the defense looked at what was added but not at what was left unchanged and needed updating.
