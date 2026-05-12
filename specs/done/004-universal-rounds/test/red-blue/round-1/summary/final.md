# Red-Blue Deliberation Synthesis: Spec 004 -- Universal Rounds

**Synthesizer**: Neutral (post-deliberation)
**Date**: 2026-03-20
**Target**: Spec 004 -- Universal Rounds, Stagnation Detection, and Arbitration
**Spec path**: `<HOME>/code/payer-index-mono/conversus/specs/004-universal-rounds/spec.md`

---

## Process Summary

| Metric | Value |
|--------|-------|
| Agents | 2 (Red Team Attacker, Blue Team Defender) |
| Phases completed | 4 (Initial reviews, Cross-reviews, Revisions, Disputes) |
| Artifacts produced | 10 (spec, 2 reviews, 2 cross-reviews, 2 revisions, 2 dispute statements, this synthesis) |
| Threats proposed (Phase 1) | 12 (THREAT-01 through THREAT-12) |
| Threats withdrawn (Phase 3) | 6 (THREAT-03, THREAT-07, THREAT-08, THREAT-09, THREAT-11, THREAT-12) |
| Threats modified (Phase 3) | 4 (THREAT-02, THREAT-04, THREAT-05, THREAT-06) |
| Threats surviving unchanged | 2 (THREAT-01, THREAT-10) |
| Convergence points | 11 (CONV-1 through CONV-11) |
| Remaining disputes | 3 (severity of THREAT-10, THREAT-02, THREAT-05) |
| New threats from cross-review | 0 (THREAT-NEW-01 was captured within existing THREAT-05) |

---

## Threat Scorecard

| THREAT-ID | Description | Phase 1 (Red) | Phase 1 (Blue) | Phase 2 Cross-Review | Phase 3 (Red Revised) | Phase 3 (Blue Revised) | Phase 4 Final |
|-----------|-------------|---------------|----------------|----------------------|-----------------------|------------------------|---------------|
| THREAT-01 | Missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates | CRITICAL | Not addressed | Red: undefended; Blue: conceded CRITICAL | CRITICAL -- Surviving | Conceded CRITICAL, P1 | **CRITICAL** -- Both agree, blocking gate |
| THREAT-02 | Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates | HIGH | Not addressed | Red: undefended; Blue: conceded, argues MEDIUM | MEDIUM -- Modified (downgraded) | Conceded gap, argues LOW | **MEDIUM** -- disputed (Red: MEDIUM, Blue: LOW) |
| THREAT-03 | `{ROUND}`, `{MAX_ROUNDS}` unused in non-coop templates | MEDIUM | Not addressed | Blue: mitigated (derivative of THREAT-01) | Withdrawn | N/A | **Withdrawn** |
| THREAT-04 | Spec FR-009 heading table contradicts SKILL.md | HIGH | Acknowledged (Limitation 1) | Red: unaddressed; Blue: argues MEDIUM | MEDIUM -- Modified (downgraded) | Acknowledged, P3 | **MEDIUM** -- Both agree |
| THREAT-05 | WTA stagnation uses `## Runner-Up` (always present) | MEDIUM | Acknowledged (Limitation 5, direction error) | Red: upgraded to HIGH; Blue: corrected direction error | MEDIUM -- Modified (scope narrowed to fallback) | Conceded direction error, P3 | **MEDIUM** -- disputed (Red: MEDIUM, Blue: LOW) |
| THREAT-06 | WTA has no countable dispute entry pattern | MEDIUM | Not directly addressed | Red: unaddressed; Blue: primary path adequate | LOW -- Modified (downgraded) | Agreed LOW | **LOW** -- Both agree |
| THREAT-07 | Non-coop arbitration lacks dispute-extraction section | MEDIUM | Not addressed | Blue: derivative of THREAT-02 | Withdrawn (merged into THREAT-02) | N/A | **Withdrawn** |
| THREAT-08 | Red-blue arbitration heading spec-vs-impl mismatch | LOW | Acknowledged (Limitation 1) | Blue: mitigated, subsumed by THREAT-04 | Withdrawn | N/A | **Withdrawn** |
| THREAT-09 | Red-blue Phase 4 disputes heading mismatch | LOW | Not addressed | Blue: mitigated (cosmetic, no parsing impact) | Withdrawn | N/A | **Withdrawn** |
| THREAT-10 | Cross-round synthesis templates lack structural markers | HIGH | Not addressed | Red: undefended; Blue: conceded, notes inheritance | HIGH -- Surviving | Conceded, argues MEDIUM (inherited) | **HIGH** -- disputed (Red: HIGH, Blue: MEDIUM) |
| THREAT-11 | Stagnation + arbitration conflicting termination narrative | LOW | Not addressed | Blue: mitigated (behavior intentional by design) | Withdrawn | N/A | **Withdrawn** |
| THREAT-12 | Cooperative backward compatibility fragility | LOW | Defended (Safeguard 5) | Red: adequately defended | Withdrawn | N/A | **Withdrawn** |

---

## Landed Attacks

These are confirmed risks where both teams agree on the existence, nature, and severity of the threat.

### THREAT-01: Missing `{PRIOR_ROUND_SECTION}` in non-cooperative Phase 1 review templates (CRITICAL)

Both teams unanimously agree this is the single most consequential finding in the deliberation. The non-cooperative review templates (`templates/red-blue/review.md`, `templates/winner-take-all/review.md`, `templates/prisoners-dilemma/review.md`) do not contain the `{PRIOR_ROUND_SECTION}` variable. The cooperative template (`templates/cooperative/review.md` L21) does. The orchestrator populates this variable for all modes, but since the non-cooperative templates do not include it, the expansion is never injected into the agent's prompt.

**Impact**: Round 2+ agents in non-cooperative modes receive no instruction to read or engage with the prior round's synthesis. Multi-round red-blue, winner-take-all, and prisoners-dilemma runs produce parallel independent analyses instead of iterative deepening. This defeats the spec's stated purpose (Section 3 game-theory analysis) and prevents success criteria SC-001 through SC-004 from being met.

**Cascade**: "Blind Round 2" -- agents repeat Round 1 analysis independently, stagnation is falsely triggered (dispute counts stay the same because agents did not engage with prior rounds), and the cross-round synthesis reports "stagnation" when the real cause is template incompleteness.

**Fix**: Add `{PRIOR_ROUND_SECTION}` to each non-cooperative review template. Single variable addition to three files.

**Status**: **Blocking gate.** Both teams agree this must be fixed before spec 004 exits Draft status. Red frames it as a blocking prerequisite; Blue concedes fully and agrees on P1 priority.

### THREAT-04: Spec FR-009 heading table diverges from SKILL.md/template reality (MEDIUM)

Both teams agree the spec's FR-009 heading table (spec.md L173-178) uses different headings than what SKILL.md (L587-592) and the actual templates implement. For example, spec says "Risk Framework, Binding Risk Decisions, Residual Risk Summary" for red-blue; SKILL.md and templates say "Decision Framework, Binding Decisions, Updated Risk Register." SKILL.md and templates agree with each other -- only the spec is wrong.

**Impact**: Documentation drift. No runtime behavior is affected. SKILL.md L594 directs maintainers to use templates as the source of truth. The spec is Draft status.

**Fix**: Update spec.md FR-009 heading table to match SKILL.md/template reality before the spec exits Draft.

**Status**: P3 remediation. Both teams agree on MEDIUM severity.

### THREAT-06: WTA stagnation detection lacks a named dispute entry pattern (LOW)

Both teams agree the winner-take-all mode has no named entry pattern for dispute counting (unlike cooperative's `**Dispute:`, red-blue's `**[RISK-ID]:`, or prisoners-dilemma's `### [` sub-headings). The primary marker-based path handles this adequately: the WTA synthesis template creates a binary state (disputed content exists within markers, or the declarative sentence "No remaining disputes -- verdict is decisive" exists), which is sufficient for count-based stagnation comparison. The concern about the heading-based fallback is captured by THREAT-05.

**Fix**: No immediate fix needed. The primary path is adequate. The fallback concern is addressed by THREAT-05's fix.

**Status**: LOW severity. Both teams agree.

---

## Mitigated Attacks

These are threats Red proposed that Blue successfully defended, leading Red to withdraw them.

### THREAT-03: `{ROUND}`, `{MAX_ROUNDS}` unused in non-cooperative Phase 1-5 templates -- WITHDRAWN

Blue demonstrated that the cooperative template also does not contain `{ROUND}` or `{MAX_ROUNDS}` directly -- it receives round context via `{PRIOR_ROUND_SECTION}` expansion. The non-cooperative templates are in the same position as the cooperative template with respect to these specific variables. Red agreed this is purely derivative of THREAT-01 and adds no independent value.

### THREAT-07: Non-cooperative arbitration templates lack dispute-extraction section -- WITHDRAWN

Blue correctly identified this as a restatement of THREAT-02 from the arbiter's perspective. The remediation is identical. Red agreed that counting it separately inflates the threat count without analytical value. Merged into THREAT-02.

### THREAT-08: Red-blue arbitration heading spec-vs-implementation mismatch -- WITHDRAWN

Blue demonstrated that the headings currently match between SKILL.md and templates. The threat is entirely speculative (requiring a future developer to trust the spec over the implementation) and is subsumed by THREAT-04. SKILL.md L594 directs maintainers to templates as the source of truth.

### THREAT-09: Red-blue Phase 4 disputes template uses wrong heading -- WITHDRAWN

Blue demonstrated that the Phase 4 disputes template organizes the agent's own output document, and the Dispute-Parsing Subsystem reads the Phase 5 SYNTHESIS output, not Phase 4 documents. The heading in the Phase 4 template is never parsed by any automated system. Zero functional impact.

### THREAT-11: Stagnation + arbitration conflicting termination -- WITHDRAWN

Blue reframed this as intentional design, not a contradiction. Stagnation answers "should we keep iterating?" (no -- disputes are not decreasing). Phase 6 answers "should we escalate?" (yes -- disputes remain). A system that stagnated then had disputes resolved by arbitration demonstrates the arbiter added value the round loop could not. Red accepted this reframing.

### THREAT-12: Cooperative backward compatibility fragility -- WITHDRAWN

Blue provided detailed verification that no cooperative-mode artifact was modified. The SKILL.md validation table change was additive (new rows; cooperative row unchanged). Phase 6 validation is informational (non-blocking). Red verified this independently and conceded.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Disputed Risks

Three threats have agreed-upon fixes and priority ordering but contested severity classifications.

**[RISK-THREAT-10]: Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers**

- **Red's position**: HIGH. All four cross-round synthesis templates (including cooperative, inherited from spec 002) lack structural markers. This violates the stable interface contract at SKILL.md L683. For multi-round runs with an arbiter, Phase 6 reads the cross-round synthesis (`{output}/summary/final.md`), and dispute extraction always falls to the degraded heading-based fallback. Spec 004 extends cross-round synthesis to three additional modes with different fallback characteristics (particularly WTA, where the fallback heading causes false stagnation per THREAT-05). The inheritance argument does not excuse spec 004 -- spec 004 is the spec that makes the gap consequential by extending it to modes where heading-based fallback is less reliable.
- **Blue's position**: MEDIUM. The gap is inherited from spec 002 -- spec 004 replicated an existing pattern, not introducing a regression. The three-tier fallback prevents functional failure (Red concedes: "The functional safety net works"). Quality degradation with a working fallback is MEDIUM, not HIGH. HIGH should be reserved for threats where the system fails to perform its function.
- **Synthesizer assessment**: Both teams agree the gap is real, the fix is P2 priority, and all four cross-round synthesis templates need markers added. The dispute is whether a contract violation with a functional fallback is HIGH (contract violation framing) or MEDIUM (degraded-but-functional framing). Red's argument that spec 004 amplifies the blast radius of the inherited gap is substantive -- the gap was latent in cooperative-only mode but becomes active in three additional modes with varying fallback reliability. The fix applies to all four templates.

**[RISK-THREAT-02]: Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates**

- **Red's position**: MEDIUM. The non-cooperative arbitration templates lack the `{REMAINING_DISPUTES}` variable and the empty-case fallback instruction that the cooperative template provides. The asymmetry means cooperative arbitration is more robust than non-cooperative arbitration. The empty-case fallback instruction is particularly important: when extraction fails, the cooperative arbiter is told to fall back to reading the full synthesis; the non-cooperative arbiter receives no such guidance and may conclude there are no disputes.
- **Blue's position**: LOW. The non-cooperative templates contain specific prose instructions directing the arbiter to the correct synthesis section by name ("Pay special attention to the synthesis's 'Disputed Risks' section"). The arbiter receives the full synthesis via `{SYNTHESIS_PATH}`. An LLM arbiter instructed to "pay special attention to" a named section will reliably locate it. The asymmetry with cooperative is a polish gap, not a quality gap.
- **Synthesizer assessment**: Both teams agree the gap is real and the fix is P2 priority. The non-cooperative templates DO contain prose instructions directing the arbiter to the correct section -- this is a genuine partial mitigation that Blue documented. The gap is the absence of pre-extracted content and the empty-case fallback instruction. The fix is additive (add `{REMAINING_DISPUTES}` and fallback instruction to three templates).

**[RISK-THREAT-05]: WTA fallback heading (`## Runner-Up`) causes false stagnation when structural markers are absent**

- **Red's position**: MEDIUM. The fallback heading `## Runner-Up` is a mandatory section in WTA synthesis -- it is always present. When the primary marker-based path fails (LLM drops markers), the fallback fires, finds `## Runner-Up`, returns count=1 for every round, and triggers false stagnation on Round 2. The fallback IS the safety net, and a broken safety net is a real concern.
- **Blue's position**: LOW. The primary marker-based path works correctly (both teams agree). The fallback fires only when the LLM drops structural markers -- a possible but not certain failure mode with decreasing likelihood as markers become more established. False stagnation (premature termination at Round 2) is wasteful but not harmful: each round's output is complete and correct, no data is corrupted, and the user can re-run with `stagnation: ignore`. This is an operational annoyance, not a quality degradation. The threat requires three conditions simultaneously: (a) LLM drops markers, (b) mode is WTA, (c) rounds > 1.
- **Synthesizer assessment**: Both teams agree the primary marker-based path works correctly. Both teams agree the fallback heading choice is suboptimal and should be changed (P3: change `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675). Both teams agree that Blue's original Phase 1 analysis of the failure direction was wrong (Blue stated "may miss stagnation" when the actual failure mode is "always detects stagnation" / premature termination). The dispute is whether the conditional, fallback-path-only nature of the threat makes it LOW or MEDIUM. The fix is the same regardless of classification.
<!-- CONVERSUS:DISPUTES_END -->

---

## Final Risk Register

| ID | Threat | Severity | Priority | Fix | Blocking? | Status |
|----|--------|----------|----------|-----|-----------|--------|
| THREAT-01 | Missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates | **CRITICAL** | P1 | Add variable to `templates/{red-blue,winner-take-all,prisoners-dilemma}/review.md` | **Yes** -- spec 004 cannot exit Draft until fixed | Agreed (both teams) |
| THREAT-10 | Cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` markers | **HIGH** (disputed: Blue argues MEDIUM) | P2 | Add markers to all four `cross-round-synthesis.md` templates (including cooperative) | Red: Yes; Blue: No (P2 remediation) | Severity disputed |
| THREAT-02 | Missing `{REMAINING_DISPUTES}` in non-cooperative arbitration templates | **MEDIUM** (disputed: Blue argues LOW) | P2 | Add variable and empty-case fallback instruction to three non-cooperative arbitration templates | No | Severity disputed |
| THREAT-05 | WTA fallback heading causes false stagnation | **MEDIUM** (disputed: Blue argues LOW) | P3 | Change WTA fallback heading from `## Runner-Up` to `### Remaining Disputes` in SKILL.md L675 | No | Severity disputed |
| THREAT-04 | Spec FR-009 heading table stale | **MEDIUM** | P3 | Update spec.md FR-009 to match SKILL.md/template headings | No | Agreed (both teams) |
| THREAT-06 | WTA lacks named dispute entry pattern | **LOW** | -- | No immediate fix; primary marker path adequate; fallback concern captured by THREAT-05 | No | Agreed (both teams) |

**Overall assessment**: Spec 004's engine changes (removing validation guards, adding Phase 6 heading rows) are correct and safe. The engine is mode-agnostic as the spec claims. The template layer has five identified gaps requiring remediation, one of which (THREAT-01) is a blocking gate for spec acceptance. All fixes are template-layer edits or documentation corrections -- no engine changes are needed.

---

## Key Concessions

### Red Team concessions
1. **THREAT-02 downgraded HIGH to MEDIUM.** Red accepted Blue's argument that prose instructions ("Pay special attention to the synthesis's 'Disputed Risks' section") provide adequate partial mitigation. The distinction between "no instruction" (THREAT-01) and "prose instruction without pre-extraction" (THREAT-02) is material.
2. **THREAT-04 downgraded HIGH to MEDIUM.** Red accepted that SKILL.md and templates agree with each other; only the spec document is wrong. SKILL.md L594 directs maintainers to templates as source of truth. Documentation drift, not functional risk.
3. **THREAT-06 downgraded MEDIUM to LOW.** Red accepted Blue's argument that the primary marker-based path handles WTA adequately via binary content detection.
4. **Six threats withdrawn (THREAT-03, 07, 08, 09, 11, 12).** Red acknowledged these were derivative, cosmetic, speculative, or correctly designed behavior. Notable: THREAT-11 (stagnation + arbitration "conflict") was reframed by Blue as intentional design -- stagnation means "stop iterating," Phase 6 means "escalate remaining disputes," and the sequence is correct.

### Blue Team concessions
1. **THREAT-01 conceded as CRITICAL.** Blue's strongest analytical failure -- the defense verified that the engine POPULATES round-aware variables but never verified that templates CONSUME them. Blue's own architectural thesis ("all mode-specific behavior lives in templates") predicts the attack's strongest finding.
2. **THREAT-10 conceded as genuine gap.** Blue acknowledged cross-round synthesis templates violate the stable interface contract at SKILL.md L683. Blue added the mitigating observation that the gap is inherited from spec 002.
3. **WTA stagnation direction error corrected.** Blue's Phase 1 defense stated WTA stagnation detection "may miss stagnation" (leading to extra rounds). Blue conceded in their revision that the actual failure mode is "always detects stagnation" (premature termination at Round 2). This was a factual error in the original defense.
4. **"Same template variables: Yes" claim withdrawn.** Blue's Evidence 2 table claimed variable parity across all arbitration templates. This was verifiably false for `{REMAINING_DISPUTES}`. Blue acknowledged conflating variable availability (spec list) with variable usage (template content).
5. **Population-vs-consumption category error acknowledged.** Blue conceded that verifying the orchestrator populates variables is necessary but not sufficient -- templates must also consume them. This was the root cause of the defense's failure to detect THREAT-01.

### Shared concessions (convergence)
- The engine is mode-agnostic and architecturally correct (CONV-1).
- Template completeness is the correctness condition for a template-first architecture (CONV-2).
- All remediation is template-layer or documentation -- no engine changes needed (CONV-11).
- Default-to-true is the correct failure mode for dispute parsing (CONV-6).
- Cooperative backward compatibility is fully preserved (CONV-5).
- The draft-gate mechanism was a genuine and properly managed safeguard (CONV-9).
