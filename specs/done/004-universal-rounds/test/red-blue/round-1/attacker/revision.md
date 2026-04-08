# Revised Attack Position: Spec 004 — Universal Rounds

**Role**: Red Team Attacker (Revised Position)
**Date**: 2026-03-20
**Prior documents**: attacker/review.md, defender/cross-reviews/attacker.md, attacker/cross-reviews/defender.md

---

## Threat Disposition Summary

| Threat | Original Severity | Revised Severity | Disposition |
|--------|-------------------|------------------|-------------|
| THREAT-01 | CRITICAL | **CRITICAL** | Surviving |
| THREAT-02 | HIGH | **MEDIUM** | Modified |
| THREAT-03 | MEDIUM | — | Withdrawn |
| THREAT-04 | HIGH | **MEDIUM** | Modified |
| THREAT-05 | MEDIUM | **MEDIUM** | Modified |
| THREAT-06 | MEDIUM | **LOW** | Modified |
| THREAT-07 | MEDIUM | — | Withdrawn |
| THREAT-08 | LOW | — | Withdrawn |
| THREAT-09 | LOW | — | Withdrawn |
| THREAT-10 | HIGH | **HIGH** | Surviving |
| THREAT-11 | LOW | — | Withdrawn |
| THREAT-12 | LOW | — | Withdrawn |

---

## Surviving Threats

### THREAT-01: Missing `{PRIOR_ROUND_SECTION}` in all non-cooperative Phase 1 templates — SURVIVING (CRITICAL)

**Blue's defense**: Blue conceded this threat fully. Blue's cross-review (L65-77) states: "This is a genuine and correctly rated threat. The evidence is unambiguous." Blue confirms the fix is straightforward: add `{PRIOR_ROUND_SECTION}` to each non-cooperative review template. Blue also acknowledged their Phase 1 defense missed this entirely (Gap 1, L153-158): "Our Phase 1 defense claimed 'Template Variable Completeness'... but did not verify that Phase 1-5 review templates for non-cooperative modes include `{PRIOR_ROUND_SECTION}`."

**Why it survives**: This is the single most important finding in the entire red-blue deliberation. The threat is conceded by both sides. Re-verification during this revision confirms the evidence:
- `templates/cooperative/review.md` contains `{PRIOR_ROUND_SECTION}`.
- `templates/red-blue/review.md`, `templates/winner-take-all/review.md`, and `templates/prisoners-dilemma/review.md` do not contain `{PRIOR_ROUND_SECTION}`.

The Cascade 1 scenario ("Blind Round 2") remains the most dangerous failure mode. Multi-round non-cooperative runs will produce parallel independent analyses instead of iterative deepening. This defeats the stated purpose of the feature — the entire game-theory analysis in Section 3 of the spec (red agents adapting attacks, blue agents strengthening defenses, competitors reading prior rankings, PD agents observing prior cooperation/defection) depends on agents receiving explicit round-awareness instructions via `{PRIOR_ROUND_SECTION}`.

Blue's partial mitigation note — that `{PRIOR_SYNTHESIS_PATH}` is populated for all modes and an LLM agent *might* follow a path variable without explicit instructions — is acknowledged but does not change severity. The difference between a populated variable and an instructional block ("You MUST engage with the prior round's synthesis") is material. Relying on an LLM to spontaneously read an unreferenced file path is not a design guarantee.

**Severity**: CRITICAL. Unchanged.

---

### THREAT-10: Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers — SURVIVING (HIGH)

**Blue's defense**: Blue conceded this threat fully. Blue's cross-review (L92-98) states: "This is a genuine gap... the stable interface contract (SKILL.md L683) is violated: if markers are a 'stable interface,' they should be present in all synthesis outputs, including cross-round synthesis."

**Why it survives**: Re-verification confirms the evidence:
- All four per-round synthesis templates (`templates/*/synthesis.md`) contain `DISPUTES_BEGIN`/`DISPUTES_END` markers.
- Zero cross-round synthesis templates (`templates/*/cross-round-synthesis.md`) contain these markers.

For multi-round runs with an arbiter, Phase 6 reads the cross-round synthesis (`{output}/summary/final.md`) per SKILL.md L540. Since cross-round synthesis templates lack markers, dispute extraction always falls to the degraded heading-based fallback. The stable interface contract at SKILL.md L683 is violated.

Blue correctly noted the three-tier fallback prevents Phase 6 from being skipped (default-to-true behavior). This is acknowledged — the functional safety net works. But the quality degradation is systematic: every multi-round run with an arbiter uses degraded dispute extraction. The marker contract was defined as "stable" precisely to prevent this degradation path.

**Severity**: HIGH. Unchanged.

---

## Modified Threats

### THREAT-02: Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates — MODIFIED (HIGH -> MEDIUM)

**Blue's defense**: Blue conceded the gap is genuine but argued the severity is overstated. Blue's key argument (cross-review L83-88): the non-cooperative arbitration templates DO instruct the arbiter to focus on the appropriate synthesis section — red-blue says "Pay special attention to the synthesis's 'Disputed Risks' section," WTA says "Pay special attention to the verdict's 'Runner-Up' section," PD says "Pay special attention to the synthesis's 'Disputed Boundaries' section." The arbiter also receives the full synthesis path (`{SYNTHESIS_PATH}`) and is an LLM capable of reading and extracting relevant content.

**Why modified**: Blue's argument has merit here in a way it did not for THREAT-01. The distinction is:
- THREAT-01: agents receive NO instruction about prior rounds (no variable, no prose, no hint). The information is completely absent from their prompt.
- THREAT-02: agents receive PROSE instructions directing them to the correct section ("Pay special attention to...") but lack the PRE-EXTRACTED content via `{REMAINING_DISPUTES}`.

The difference between "no instruction" (THREAT-01) and "prose instruction without pre-extraction" (THREAT-02) is material. An LLM arbiter reading a synthesis document and told to "pay special attention to the Disputed Risks section" will reliably find that section. The `{REMAINING_DISPUTES}` pre-extraction is a quality-of-life improvement — it saves the arbiter from having to locate the section itself — but it is not a correctness requirement.

However, the gap remains real: the cooperative template provides both pre-extraction AND a fallback instruction for the empty case ("If this section is empty, read the full synthesis to identify any remaining disputes"). The non-cooperative templates have neither the pre-extraction nor the empty-case fallback. This asymmetry means the cooperative arbitration path is more robust than the non-cooperative paths.

**Severity**: Downgraded from HIGH to MEDIUM. Quality gap, not functional impairment.

### THREAT-04: Spec FR-009 heading table contradicts deployed SKILL.md heading table — MODIFIED (HIGH -> MEDIUM)

**Blue's defense**: Blue argued (cross-review L110-121) that the spec is a design-time document, SKILL.md is the runtime specification, the implementation is internally consistent (SKILL.md and templates agree), and SKILL.md L594 directs maintainers to use templates as the source of truth. The spec is also marked "Draft" status.

**Why modified**: Blue's argument is convincing. My original severity of HIGH was based on the three-way mismatch creating maintenance risk. But Blue correctly points out:
1. No runtime behavior is affected — SKILL.md and templates agree.
2. SKILL.md L594 explicitly says: "if a template's heading instructions change, update this table" — directing maintainers to templates, not the spec.
3. The spec is Draft status, meaning it has not been finalized.

The threat remains real — the spec should be updated to match reality before it leaves Draft status. A spec that diverges from implementation on the day of creation provides negative value. But the blast radius is documentation debt, not functional failure.

**Severity**: Downgraded from HIGH to MEDIUM. Documentation drift, not functional risk.

### THREAT-05: Winner-take-all stagnation detection uses `## Runner-Up` presence, not dispute count — MODIFIED (scope clarified, MEDIUM maintained)

**Blue's defense**: Blue argued (cross-review L123-133) that the primary marker-based path handles WTA stagnation correctly because the WTA synthesis template includes `DISPUTES_BEGIN`/`DISPUTES_END` markers around `### Remaining Disputes`. The `## Runner-Up` fallback is only used when markers are absent. Blue concluded: "Should be LOW for the primary path, MEDIUM only for the degraded fallback scenario."

**Why modified**: Blue's defense on the primary path is correct. When structural markers are preserved by the LLM, the `### Remaining Disputes` content within the markers is what gets counted, not `## Runner-Up`. My original analysis conflated the fallback heading with the primary parsing path. The primary path works correctly for WTA.

However, I maintain the threat at MEDIUM for two reasons:

1. **The fallback IS the safety net, and it is broken for WTA.** The entire point of the three-tier fallback is to handle the case where the LLM drops structural markers — a known failure mode acknowledged by the spec itself (SKILL.md L569: "The marker upgrade should be tracked as a continuation item"). When the fallback fires for WTA, it finds `## Runner-Up` (always present), yields a boolean true, and produces a count of 1 for every round. This causes false stagnation on Round 2. Blue's own cross-review (Gap 3, L163-169) admits: "Our Limitation 5 said 'may miss stagnation' when the actual failure mode is 'always detects stagnation.' This is a factual error in our defense."

2. **Blue conceded the fallback heading choice is suboptimal** and included it in their remediation table (L185): "Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in the Dispute-Parsing Subsystem (SKILL.md L675)."

The scope is narrower than I originally claimed (fallback path only, not primary path), but the severity remains MEDIUM because the fallback IS the safety net, and a broken safety net is a real concern.

**Severity**: MEDIUM. Scope narrowed (fallback path only), severity maintained.

### THREAT-06: Winner-take-all stagnation detection is structurally undefined for count-based comparison — MODIFIED (MEDIUM -> LOW)

**Blue's defense**: Blue argued (cross-review L135-143) that the primary marker-based path counts "any non-whitespace content beyond the section heading itself" within the marker range, which handles the WTA case. The WTA synthesis template provides a clear binary: either disputed content exists or the declarative sentence "No remaining disputes — verdict is decisive" exists. This makes the count effectively 0 or N.

**Why modified**: Blue's argument about the marker-based primary path is convincing. When markers are present, the counting mechanism works adequately because the WTA template creates a clear binary state. The absence of a named entry pattern (like `**Dispute:` or `**[RISK-ID]:`) matters less when the marker-bounded content is binary (disputed content vs. declarative "no disputes" sentence).

The concern remains valid for the heading-based fallback path — but this overlaps with THREAT-05's scope and should not be double-counted.

**Severity**: Downgraded from MEDIUM to LOW. The primary path handles WTA adequately; the fallback concern is already captured in THREAT-05.

---

## Withdrawn Threats

### THREAT-03: No round-aware variables (`{ROUND}`, `{MAX_ROUNDS}`) in non-cooperative Phase 1-5 templates — WITHDRAWN

**Blue's defense holds**: Blue correctly argued (cross-review L17-27) that the cooperative template also does not contain `{ROUND}` or `{MAX_ROUNDS}` directly — it receives round context via `{PRIOR_ROUND_SECTION}` expansion, not via direct variable usage. The non-cooperative templates are in the same position as the cooperative template with respect to these specific variables. The real gap is `{PRIOR_ROUND_SECTION}` (THREAT-01), not `{ROUND}` or `{MAX_ROUNDS}`. This threat is a derivative of THREAT-01, not an independent finding.

Additionally, Blue correctly noted that the orchestrator populates `{PRIOR_SYNTHESIS_PATH}` for all modes, and the round number is embedded in the directory structure path itself. Agents can infer round context from the path structure even without explicit `{ROUND}` variables.

**Withdrawn**: This threat adds no value beyond THREAT-01.

### THREAT-07: Non-cooperative arbitration templates lack dispute-extraction section — WITHDRAWN

**Blue's defense holds**: Blue correctly argued (cross-review L145-147) that this threat is not independent — it restates THREAT-02 from the arbiter's perspective. The remediation is identical: add `{REMAINING_DISPUTES}` to non-cooperative arbitration templates. Counting this separately inflates the threat count without adding analytical value.

**Withdrawn**: Merged into THREAT-02.

### THREAT-08: Red-blue arbitration "Updated Risk Register" heading mismatch with Phase 6 validation — WITHDRAWN

**Blue's defense holds**: Blue correctly argued (cross-review L29-35) that this threat is entirely speculative. The headings currently match (SKILL.md L590 and the red-blue arbitration template agree). The threat requires a future developer to read the spec, trust it over the implementation, and change SKILL.md without checking templates — a chain of events made less likely by SKILL.md L594's explicit instruction to use templates as the source of truth. This is subsumed by THREAT-04 (spec documentation drift) and adds no independent value.

**Withdrawn**: Subsumed by THREAT-04.

### THREAT-09: Red-blue Phase 4 disputes template uses `### Remaining Disputes`, not `### Disputed Risks` — WITHDRAWN

**Blue's defense holds**: Blue correctly argued (cross-review L37-43) that the Phase 4 disputes template is agent-facing scaffolding — it organizes the agent's own output document. The Dispute-Parsing Subsystem reads the Phase 5 SYNTHESIS output, not Phase 4 dispute documents. The heading in the Phase 4 template is never parsed by any automated system. The naming inconsistency is cosmetic with zero functional impact.

**Withdrawn**: No functional impact.

### THREAT-11: `stagnation: detect` with `arbiter` and `trigger: disputes_remain` creates conflicting termination — WITHDRAWN

**Blue's defense holds**: Blue correctly argued (cross-review L45-51) that stagnation-then-arbitration is actually the correct behavior by design, not a contradiction. Stagnation answers "should we keep iterating?" (no — the round loop is not reducing disputes). Phase 6 answers "should we escalate?" (yes — disputes remain). A system that stagnated and then had disputes resolved by arbitration demonstrates that the arbiter added value the round loop could not. The "contradictory narrative" framing was mine, not an inherent system problem.

**Withdrawn**: The behavior is intentional and correct.

### THREAT-12: Cooperative mode backward compatibility is preserved — but fragile — WITHDRAWN

**Blue's defense holds**: Blue provided detailed verification evidence (cross-review L53-58). The cooperative row in the SKILL.md validation table is unchanged. Validation is informational, not blocking. I verified this in my original review and rated it LOW. Blue's evidence is adequate and I concede the fragility concern is unfounded — the change was additive (new rows), not modifying.

**Withdrawn**: Verified safe.

---

## New Threats from Cross-Review

### THREAT-NEW-01: Blue's defense contains a factual error about WTA stagnation direction

During cross-review of Blue's defense, I identified that Blue's Limitation 5 stated WTA stagnation detection "may miss stagnation in some cases (leading to extra rounds) but will not falsely declare stagnation." This is backwards — when the fallback fires, `## Runner-Up` is always present, causing the count to always be 1, which triggers stagnation on Round 2 (false stagnation, not missed stagnation). Blue's own cross-review of my attack (Gap 3, L163-169) concedes this: "Our Limitation 5 said 'may miss stagnation' when the actual failure mode is 'always detects stagnation.' This is a factual error in our defense."

This is not a new threat to the system — it is already captured in THREAT-05. But it is a factual correction to Blue's defense document and confirms that the WTA fallback stagnation detection failure mode is premature termination (Round 2 always stagnates), not unbounded rounds.

**Disposition**: Captured in THREAT-05. No new system threat.

---

## Cascading Failures — Revised

### Cascade 1: "Blind Round 2" — SURVIVING

Unchanged. THREAT-01 is conceded by both sides. Multi-round non-cooperative runs will produce parallel independent analyses. This is the highest-impact failure.

### Cascade 2: "Phantom Stagnation in WTA" — MODIFIED (scope narrowed to fallback path)

Modified per THREAT-05 revision. When the primary marker-based path works (markers preserved by LLM), WTA stagnation detection is correct. When markers are dropped and the fallback fires, false stagnation occurs on Round 2. The cascade exists but only on the degraded path.

### Cascade 3: "Markerless Arbiter" — SURVIVING (simplified)

THREAT-10 is conceded by both sides. Cross-round synthesis templates lack structural markers. For multi-round runs with an arbiter, dispute extraction always falls to degraded heading-based parsing. The compound effect with THREAT-02 (non-cooperative arbitration templates lack `{REMAINING_DISPUTES}`) is still present but downgraded: the arbiter receives prose instructions directing it to the correct section, so the degradation is quality rather than functional.

---

## Position Summary

After deliberation, the attack surface is narrower but sharper than my original review suggested. Six of twelve threats have been withdrawn — Blue's defenses on derivative findings (THREAT-03, THREAT-07, THREAT-08), cosmetic issues (THREAT-09), intentional design (THREAT-11), and verified backward compatibility (THREAT-12) were convincing.

The surviving and modified threats form a coherent picture of a single root problem: **template completeness was not verified for multi-round non-cooperative execution**. The engine is mode-agnostic and correct. The templates are the carriers of mode-specific behavior. But three template-level gaps were not caught:

1. **CRITICAL — THREAT-01**: Non-cooperative review templates lack `{PRIOR_ROUND_SECTION}`, making Round 2+ agents blind to prior rounds. Both sides agree this is the highest-priority fix.
2. **HIGH — THREAT-10**: Cross-round synthesis templates lack structural markers, forcing degraded dispute extraction for all multi-round arbiter runs. Both sides agree this violates the stable interface contract.
3. **MEDIUM — THREAT-02**: Non-cooperative arbitration templates lack `{REMAINING_DISPUTES}` pre-extraction. Mitigated by prose instructions directing the arbiter to the correct section, but asymmetric with the cooperative template.
4. **MEDIUM — THREAT-04**: Spec FR-009 heading table diverges from SKILL.md/template reality. Documentation debt only — no runtime impact.
5. **MEDIUM — THREAT-05**: WTA fallback heading (`## Runner-Up`) causes false stagnation when structural markers are absent. Primary marker-based path is correct.
6. **LOW — THREAT-06**: WTA dispute counting lacks a named entry pattern. Adequately handled by binary content detection in the primary marker path.

**Recommended remediation priority**:

| Priority | Fix | Threats Resolved |
|----------|-----|------------------|
| P1 | Add `{PRIOR_ROUND_SECTION}` to `templates/red-blue/review.md`, `templates/winner-take-all/review.md`, `templates/prisoners-dilemma/review.md` | THREAT-01, Cascade 1 |
| P2 | Add `DISPUTES_BEGIN`/`DISPUTES_END` markers to all four `cross-round-synthesis.md` templates | THREAT-10, Cascade 3 |
| P2 | Add `{REMAINING_DISPUTES}` and fallback instruction to non-cooperative arbitration templates | THREAT-02 |
| P3 | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675 | THREAT-05, THREAT-06 |
| P3 | Update spec.md FR-009 heading table to match SKILL.md/template headings | THREAT-04 |

The P1 fix is a single-variable addition to three template files. The P2 fixes are additive template edits. The P3 fixes are documentation corrections. None require engine changes. The total remediation surface is small — the architecture is sound, the templates just need to be completed.
