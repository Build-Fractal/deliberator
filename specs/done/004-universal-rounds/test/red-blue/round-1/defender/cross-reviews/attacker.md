# Blue Team Cross-Review of Red Team Attack Surface Analysis

**Reviewer**: Blue Team Defender
**Reviewing**: Red Team (attacker) Phase 1 review
**Date**: 2026-03-20

---

## Executive Assessment

The Red Team's analysis is thorough and well-structured. Several threats are genuine and deserve remediation. However, the review overstates severity in multiple cases by conflating "template does not contain a variable" with "the feature is broken," ignoring that conversus is an LLM-orchestrated system where the orchestrator's variable population and the agent's prompt context work together. The attacker's strongest findings concern the missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates (THREAT-01) and the missing structural markers in cross-round synthesis templates (THREAT-10). The weakest findings involve inflated severity on heading mismatches and WTA stagnation detection.

---

## Mitigated Threats

### THREAT-03: No round-aware variables (`{ROUND}`, `{MAX_ROUNDS}`) in non-cooperative Phase 1-5 templates

**Attacker's claim**: Non-cooperative Phase 1-5 agents receive no context about which round they are executing in.

**Defense**: The attacker's own evidence disproves this at MEDIUM severity. The attacker acknowledges: "The cooperative review template also does not contain `{ROUND}` directly but receives it via `{PRIOR_ROUND_SECTION}` expansion." This means the cooperative template is in the exact same position as non-cooperative templates with respect to `{ROUND}` and `{MAX_ROUNDS}` -- neither uses them directly. The cooperative template does not demonstrate a pattern that non-cooperative templates violate.

Furthermore, SKILL.md L336-340 defines `{ROUND}`, `{MAX_ROUNDS}`, `{PRIOR_SYNTHESIS_PATH}`, and `{PRIOR_ROUND_DIR}` as "available in ALL Phase 1-5 templates." The orchestrator populates these variables and they ARE substituted into the template output. The fact that the template text does not literally contain `{ROUND}` or `{MAX_ROUNDS}` as visible text in its instructions does not mean agents lack round context. The `{PRIOR_SYNTHESIS_PATH}` variable -- which IS populated for all modes -- gives agents a path to read that inherently communicates "this is not Round 1." The round number is embedded in the directory structure (`round-2/summary/final.md`).

The real round-awareness gap is `{PRIOR_ROUND_SECTION}` (covered by THREAT-01), not `{ROUND}` or `{MAX_ROUNDS}`. This threat is a derivative of THREAT-01, not an independent finding.

**Verdict**: Mitigated. The severity is inflated by treating variable population as distinct from variable consumption in a context where the orchestrator substitutes all available variables into every template regardless of whether the template text explicitly references them.

### THREAT-08: Red-blue arbitration "Updated Risk Register" heading mismatch with Phase 6 validation

**Attacker's claim**: If someone "fixes" the implementation to match the spec, validation will break against the template.

**Defense**: The attacker rates this LOW and even acknowledges: "These currently match." The threat is entirely speculative -- it requires a future developer to (a) read the spec, (b) trust the spec over the implementation, (c) change the SKILL.md heading table, and (d) not check the actual templates. This is a documentation drift issue, not a security or correctness threat. We already acknowledged this in our Phase 1 review (Limitation 1). The SKILL.md table at L594 explicitly states: "The headings correspond to those instructed by each mode's `templates/{mode}/arbitration.md` -- if a template's heading instructions change, update this table." This instruction directs future developers to the templates as the source of truth, not the spec.

**Verdict**: Mitigated by existing documentation guidance in SKILL.md L594.

### THREAT-09: Red-blue Phase 4 disputes template uses `### Remaining Disputes`, not `### Disputed Risks`

**Attacker's claim**: Heading mismatch between Phase 4 output and Phase 5/Dispute-Parsing Subsystem.

**Defense**: The attacker correctly identifies this as LOW and acknowledges: "the parsing subsystem reads synthesis, not disputes." The Phase 4 disputes template instructs agents what headings to use in their OWN output. The Dispute-Parsing Subsystem reads the Phase 5 SYNTHESIS output, which correctly uses `### Disputed Risks` (verified at `templates/red-blue/synthesis.md` L114). The heading in the Phase 4 template is agent-facing scaffolding for organizing the agent's own document -- it is never parsed by any automated system.

**Verdict**: Mitigated. No functional impact. The naming inconsistency is cosmetic.

### THREAT-11: `stagnation: detect` with `arbiter` and `trigger: disputes_remain` creates conflicting termination

**Attacker's claim**: Stagnation-then-arbitration produces contradictory narratives.

**Defense**: The attacker rates this LOW and correctly identifies it as a "user-experience issue," not a functional failure. The behavior is actually correct by design: stagnation means "the round loop is not reducing disputes," which is the right time to escalate to arbitration. Stagnation detection and Phase 6 trigger evaluation are independent by design (SKILL.md L474-479 and L539-541) because they serve different purposes. Stagnation answers "should we keep iterating?" while Phase 6 answers "should we escalate?" A system that stagnated AND had disputes resolved by arbitration is a success story, not a contradiction -- it means the arbiter added value that the round loop could not.

**Verdict**: Mitigated. The "contradictory narrative" framing mischaracterizes intentional design.

### THREAT-12: Cooperative mode backward compatibility is preserved -- but fragile

**Attacker's claim**: The Phase 6 heading validation table change touches cooperative mode's validation path.

**Defense**: The attacker rates this LOW and confirms: "The cooperative row... matches the cooperative arbitration template's actual headings. Verified." The attacker further notes validation is informational, not blocking. Our Phase 1 review provided detailed verification evidence (Safeguard 3, Safeguard 5). The change was additive (new rows), not modifying (the cooperative row is unchanged at SKILL.md L589).

**Verdict**: Mitigated with evidence. No regression risk.

---

## Valid Threats

### THREAT-01: Missing `{PRIOR_ROUND_SECTION}` in all non-cooperative Phase 1 templates (CRITICAL)

**Concession**: This is a genuine and correctly rated threat. The evidence is unambiguous:

- `templates/cooperative/review.md` L21 contains `{PRIOR_ROUND_SECTION}`.
- `templates/red-blue/review.md`, `templates/winner-take-all/review.md`, and `templates/prisoners-dilemma/review.md` do not contain this variable.
- SKILL.md L368-375 defines this variable as a Phase 1 template variable with a multi-paragraph expansion that instructs agents to read the prior round's synthesis.

The attacker is correct that without this variable, Round 2+ agents in non-cooperative modes will not receive explicit instructions to read the prior round's synthesis. The orchestrator populates `{PRIOR_ROUND_SECTION}`, but since the template does not include the variable, the expansion is never injected into the agent's prompt.

**Partial mitigation note**: The orchestrator DOES populate `{PRIOR_SYNTHESIS_PATH}` for all templates (SKILL.md L339, L359), and this variable IS present in the template via the general variable substitution mechanism. An LLM agent receiving a path variable in its prompt may or may not follow it without explicit instructions. However, the attacker is right that the *instructional block* -- "You MUST engage with the prior round's synthesis" -- is absent. The difference between having a path and having instructions to read and engage with that path is material.

**Verdict**: Valid. This is the highest-priority remediation item. The fix is straightforward: add `{PRIOR_ROUND_SECTION}` to each non-cooperative review template.

### THREAT-02: Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates (HIGH)

**Concession**: This is a genuine gap, though the severity is slightly overstated (see Overstated Threats below for the severity calibration). The cooperative arbitration template (L34-40) provides pre-extracted disputes via `{REMAINING_DISPUTES}` and includes a fallback instruction ("If this section is empty, read the full synthesis"). The non-cooperative templates do not include this variable or the fallback.

However, the non-cooperative arbitration templates DO instruct the arbiter to focus on the appropriate disputes section:
- Red-blue (L32): "Pay special attention to the synthesis's 'Disputed Risks' section"
- WTA (L32): "Pay special attention to the verdict's 'Runner-Up' section and 'Conditions for reconsideration'"
- PD (L32): "Pay special attention to the synthesis's 'Disputed Boundaries' section"

These instructions direct the arbiter to the correct section of the synthesis. The `{REMAINING_DISPUTES}` pre-extraction is a quality-of-life improvement, not a structural requirement. The arbiter receives the full synthesis path (`{SYNTHESIS_PATH}`) and is explicitly told where to look.

**Verdict**: Valid as a quality gap. The fix is to add `{REMAINING_DISPUTES}` and a fallback instruction to all non-cooperative arbitration templates.

### THREAT-10: Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers (HIGH)

**Concession**: This is a genuine gap. The per-round synthesis templates for all four modes include structural markers. The cross-round synthesis templates for all four modes do not. Since the cross-round synthesis becomes the "definitive synthesis" (`{output}/summary/final.md`) that Phase 6 reads, the Phase 6 trigger evaluation and `{REMAINING_DISPUTES}` extraction will fall back to heading-based parsing for all multi-round runs.

The Dispute-Parsing Subsystem's three-tier fallback (SKILL.md L666-679) handles this gracefully -- heading-based parsing works, and the default-to-true behavior (L679) provides a safety net. But the attacker is correct that the stable interface contract (SKILL.md L683) is violated: if markers are a "stable interface," they should be present in all synthesis outputs, including cross-round synthesis.

**Verdict**: Valid. The fix is to add `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers to all four cross-round synthesis templates around their respective disputes sections.

---

## Overstated Threats

### THREAT-02 severity: HIGH is slightly overstated; should be MEDIUM

The attacker rates this HIGH based on "reduced arbitration precision." However, the non-cooperative arbitration templates explicitly direct the arbiter to the correct synthesis section (see evidence under Valid Threats above). The arbiter is an LLM agent receiving the full synthesis as a readable document -- it is not a regex parser that needs pre-extracted content. The `{REMAINING_DISPUTES}` variable improves precision at the margin, but an LLM instructed to "pay special attention to the 'Disputed Risks' section" will find that section reliably. The cooperative template's pre-extraction is a usability improvement, not a correctness requirement.

The gap is real but should be MEDIUM (quality degradation), not HIGH (functional impairment).

### THREAT-04: Spec FR-009 heading table contradicts deployed SKILL.md heading table -- severity HIGH is overstated; should be MEDIUM

The attacker rates this HIGH. The actual impact is documentation drift between the spec document and the implementation. The attacker's own analysis confirms: "SKILL.md and templates now agree" -- meaning the implementation is internally consistent. The only artifact that is wrong is the spec document itself.

Specs are design-time documents. SKILL.md is the runtime specification. Our Phase 1 review already acknowledged this limitation (Limitation 1) and noted: "The implementation chose to align the validation headings with the actual template headings rather than the spec's theoretical headings. This is the correct decision." The attacker is essentially re-reporting a limitation we already disclosed.

The threat is real (the spec should be updated) but its severity as HIGH is overstated because:
1. No runtime behavior is affected.
2. SKILL.md L594 explicitly directs maintainers to use templates as the source of truth.
3. The spec is marked as "Draft" status (spec.md L4).

Should be MEDIUM -- documentation debt, not a functional or safety risk.

### THREAT-05: Winner-take-all stagnation detection uses `## Runner-Up` presence, not dispute count -- severity MEDIUM is overstated

The attacker claims stagnation detection for WTA is "trivially true from Round 1" because `## Runner-Up` is always present. This mischaracterizes how the Dispute-Parsing Subsystem works.

SKILL.md L666-671 defines the **primary** parsing path as structural markers. The WTA per-round synthesis template DOES include `DISPUTES_BEGIN`/`DISPUTES_END` markers (at L106/L110 of `templates/winner-take-all/synthesis.md`). The fallback heading (`## Runner-Up`) is only used when markers are absent. For per-round synthesis outputs (which is what stagnation detection reads -- it reads `{round_base}/summary/final.md`, which is the per-round Phase 5 synthesis), the markers SHOULD be present because the synthesis template includes them.

The attacker's scenario requires the LLM to drop the structural markers from its output -- a possible but not certain failure mode. The attacker acknowledges this: "depends on whether the LLM preserves structural markers." This is a degraded-fallback scenario, not the primary path. The primary path (markers present) correctly counts disputes in the `### Remaining Disputes` section.

Furthermore, the actual `### Remaining Disputes` section in the WTA synthesis template (L107-109) is inside the markers and IS the correct section for counting. The fallback heading `## Runner-Up` is a secondary detection method that is admittedly poorly chosen for count-based stagnation. But the primary path works correctly.

**Verdict**: The fallback heading choice is suboptimal (valid concern), but the severity is overstated because the primary marker-based path handles WTA stagnation correctly. Should be LOW for the primary path, MEDIUM only for the degraded fallback scenario.

### THREAT-06: Winner-take-all stagnation detection is structurally undefined for count-based comparison -- severity MEDIUM is overstated

The attacker claims WTA has "no defined entry pattern." This is partially true for the free-form text in the `### Remaining Disputes` section but overstates the impact.

SKILL.md L670-671 states: "Check whether at least one dispute entry exists within that range (any non-whitespace content beyond the section heading itself)." The primary parsing path counts non-whitespace content entries, not pattern-matched entries. The mode-specific patterns (`**Dispute:`, `**[RISK-ID]:`, `### [`) are FALLBACK patterns used when markers are absent. When markers ARE present (as they are in the WTA synthesis template), the subsystem counts entries within the marker range.

Additionally, the WTA synthesis template (L109) explicitly tells the synthesizer: "If the verdict is clear, state: 'No remaining disputes -- verdict is decisive.'" This creates a binary: either disputed content exists within the markers or a single declarative sentence exists. The count is effectively 0 or N, which is sufficient for stagnation detection (count >= prior count).

**Verdict**: The concern about entry pattern ambiguity is a valid observation for the fallback path, but the primary marker-based path handles this adequately. Should be LOW.

### THREAT-07: Non-cooperative arbitration templates lack dispute-extraction section -- severity MEDIUM is accurate but this is a derivative of THREAT-02

This threat is not independent. It restates THREAT-02 from the arbiter's perspective rather than the template's perspective. Counting it separately inflates the threat count. The remediation is the same: add `{REMAINING_DISPUTES}` to non-cooperative arbitration templates.

---

## Defense Gaps

### Gap 1: Our Phase 1 defense missed the `{PRIOR_ROUND_SECTION}` absence entirely

The Red Team correctly identified that our Phase 1 defense claimed "Template Variable Completeness" (Evidence 5) by verifying the cross-round synthesis and arbitration variables, but did not verify that Phase 1-5 review templates for non-cooperative modes include `{PRIOR_ROUND_SECTION}`. Our defense focused on the NEW templates (cross-round synthesis, arbitration) and verified their variable sets against the cooperative templates. We did not audit the EXISTING Phase 1 review templates for the presence of round-aware variables.

This is the most significant gap in our defense. The spec's FR-010 said "must be verified" and work_done.md L50 says "Verified." But the verification checked that the orchestrator POPULATES the variables, not that the templates CONSUME them. Population without consumption is inert -- the attacker's framing is correct.

### Gap 2: Our defense did not address structural marker absence in cross-round synthesis templates

Our Phase 1 defense discussed the Dispute-Parsing Subsystem's three-tier fallback as a safeguard (Safeguard 2) but did not verify that cross-round synthesis templates include the structural markers that make the primary tier work. We correctly identified the subsystem as already mode-aware, but we did not check whether the NEW cross-round synthesis templates honor the stable interface contract.

### Gap 3: Our defense understated the WTA stagnation detection weakness

Our Phase 1 defense acknowledged this as Limitation 5: "Winner-Take-All Stagnation Detection Is Indirect." However, our framing -- "conservative -- it may miss stagnation in some cases (leading to extra rounds) but will not falsely declare stagnation" -- is actually the opposite of the attacker's analysis. The attacker argues the fallback heading (`## Runner-Up`) is always present, which would cause FALSE stagnation (always stagnating, not never stagnating). Our defense got the direction of the failure wrong. The correct analysis:
- With markers (primary path): stagnation detection works correctly.
- Without markers (fallback path): `## Runner-Up` is always present, so stagnation is always detected, causing premature termination at Round 2.

Our Limitation 5 said "may miss stagnation" when the actual failure mode is "always detects stagnation." This is a factual error in our defense.

### Gap 4: Our defense did not distinguish between `{REMAINING_DISPUTES}` presence in cooperative vs. non-cooperative arbitration templates

Our Phase 1 Evidence 2 table claimed "Same template variables: Yes" across all arbitration templates. This is correct at the orchestrator level (all variables are populated for all modes) but incorrect at the template consumption level -- the cooperative template explicitly references `{REMAINING_DISPUTES}` while the other three do not. Our defense's claim of parity was based on variable availability, not variable usage. The attacker correctly distinguished between population and consumption.

---

## Summary of Remediation Priorities

| Priority | Threat | Fix |
|----------|--------|-----|
| P1 | THREAT-01 | Add `{PRIOR_ROUND_SECTION}` to `templates/red-blue/review.md`, `templates/winner-take-all/review.md`, `templates/prisoners-dilemma/review.md` |
| P2 | THREAT-10 | Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four `cross-round-synthesis.md` templates |
| P2 | THREAT-02 | Add `{REMAINING_DISPUTES}` and fallback instruction to all non-cooperative arbitration templates |
| P3 | THREAT-04 | Update spec.md FR-009 heading table to match SKILL.md/template reality |
| P3 | THREAT-05 | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in the Dispute-Parsing Subsystem (SKILL.md L675) |
