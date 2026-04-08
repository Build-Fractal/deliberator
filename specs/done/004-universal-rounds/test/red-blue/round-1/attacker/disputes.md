# Final Attacker Disputes — Spec 004: Universal Rounds

**Role**: Red Team Attacker (Final Statement)
**Date**: 2026-03-20
**Phase**: Final disputes before synthesis

---

### Remaining Disputes

**Dispute: THREAT-01 remediation must be a blocking prerequisite, not a backlog item (CRITICAL)**

- **Red's claim**: The missing `{PRIOR_ROUND_SECTION}` in all three non-cooperative review templates (`templates/red-blue/review.md`, `templates/winner-take-all/review.md`, `templates/prisoners-dilemma/review.md`) is not merely P1 in a prioritized backlog — it is a gate condition. Spec 004 should not exit Draft status until this is fixed. Without this variable, multi-round non-cooperative runs produce parallel independent analyses instead of iterative deepening. This defeats the stated purpose of the feature described in spec.md Section 3 (game-theory analysis requiring round-awareness). The spec's own success criteria (SC-001 through SC-004) cannot be met as written.
- **Blue's position**: Blue concedes the threat fully and agrees on P1 priority. Blue frames it as a remediation item in a priority table. Blue acknowledges the fix is "straightforward" — a single variable addition to three template files.
- **Why I won't concede**: The disagreement is not about severity (both teams agree: CRITICAL) or about the fix (both teams agree: add `{PRIOR_ROUND_SECTION}`). The disagreement is about disposition. Blue's language — "remediation item," "before non-cooperative multi-round runs are production-ready" — implies spec 004 can be accepted with known critical gaps. I dispute this framing. A spec that enables multi-round non-cooperative execution but ships templates that produce blind Round 2 agents is a spec that ships a broken feature. The fix must be applied before spec 004 leaves Draft, not tracked as a follow-up.
- **Proposed resolution**: The synthesis must classify THREAT-01 as a **blocking gate** — spec 004 cannot be marked complete/accepted until `{PRIOR_ROUND_SECTION}` is present in all three non-cooperative review templates. This is not a "nice to have" remediation; it is a correctness condition for the feature the spec defines.

---

**Dispute: THREAT-10 cross-round synthesis marker absence is a contract violation regardless of inheritance (HIGH)**

- **Red's claim**: All four `cross-round-synthesis.md` templates (cooperative and the three new non-cooperative ones) lack `DISPUTES_BEGIN`/`DISPUTES_END` structural markers. This violates the stable interface contract at SKILL.md L683, which declares these markers a "stable interface." For multi-round runs with an arbiter, Phase 6 reads the cross-round synthesis (`{output}/summary/final.md`), and dispute extraction always falls to the degraded heading-based fallback.
- **Blue's position**: Blue concedes the gap is real and agrees on P2 priority. Blue adds a mitigating observation: the gap predates spec 004 because the cooperative cross-round synthesis template (from spec 002) also lacks markers. Spec 004's three new templates are "consistent with the existing cooperative template." Blue frames this as an inherited gap, not a regression introduced by spec 004.
- **Why I won't concede**: Blue's "inherited gap" framing is factually accurate but strategically misleading. Spec 004 is the spec that ENABLES multi-round non-cooperative execution. Before spec 004, only cooperative mode could run multi-round. The cooperative cross-round synthesis marker absence was low-impact because cooperative mode's dispute heading (`### Remaining Disputes`) produces reliable heading-based fallback parsing. But spec 004 extends cross-round synthesis to modes where heading-based fallback is less reliable — particularly WTA, where the fallback heading `## Runner-Up` causes false stagnation (THREAT-05). Spec 004 inherited a latent defect and amplified its blast radius by extending it to three additional modes with different fallback characteristics. The fact that spec 002 also had this gap does not excuse spec 004 from fixing it, especially since spec 004 is the spec that makes the gap consequential.
- **Proposed resolution**: The synthesis must classify THREAT-10 as **blocking for spec 004**, with the fix applied to all four cross-round synthesis templates (including cooperative). Spec 004 should fix the inherited gap because spec 004 is the spec that makes it matter.

---

**Dispute: THREAT-02 severity should remain MEDIUM, but the asymmetry must be explicitly documented (MEDIUM)**

- **Red's claim**: Non-cooperative arbitration templates lack `{REMAINING_DISPUTES}` and the empty-case fallback instruction that the cooperative template provides. This creates a quality asymmetry between cooperative and non-cooperative arbitration paths.
- **Blue's position**: Blue concedes the gap but argues the non-cooperative templates provide adequate prose instructions ("Pay special attention to the synthesis's 'Disputed Risks' section") and the arbiter receives the full synthesis as a readable document. Blue rates this MEDIUM — quality gap, not functional impairment.
- **Why I won't concede**: I accept Blue's MEDIUM severity — the prose instructions are a genuine partial mitigation, and I downgraded this threat in my own revision. But I dispute the implication that the gap is acceptable as-is. The cooperative template provides BOTH pre-extraction AND a fallback instruction for the empty case ("If this section is empty, read the full synthesis to identify any remaining disputes"). The non-cooperative templates have NEITHER. The empty-case handling is particularly important: when `{REMAINING_DISPUTES}` is empty, the cooperative arbiter is explicitly told to fall back to reading the full synthesis. The non-cooperative arbiter receives no such instruction and may conclude there are no disputes to resolve when the extraction simply failed.
- **Proposed resolution**: P2 remediation as both teams agree. But the synthesis must note that the empty-case fallback instruction is the more important missing element — not just the pre-extraction convenience.

---

### Convergence

**CONV-1: Engine mode-agnosticism is architecturally correct**
- **Shared assessment**: The round loop, stagnation detection algorithm, Phase 6 trigger evaluation, template loading, and variable population are mode-agnostic. The engine correctly implements a generic orchestration framework where all mode-specific behavior is delegated to templates. No engine changes are needed beyond removing validation guards (FR-001) and adding Phase 6 heading rows (FR-009).
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-2: Template completeness is the correctness condition**
- **Shared assessment**: Because the engine is mode-agnostic and templates carry all mode-specific behavior, template completeness IS feature completeness. The defense's own architectural thesis predicts the attack's strongest finding: if templates are incomplete, the feature is incomplete. Both teams agree that the three template-level gaps (THREAT-01, THREAT-02, THREAT-10) are real and must be remediated.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-3: THREAT-01 is the highest-priority finding (CRITICAL)**
- **Shared assessment**: The missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates is the single most consequential gap. It causes Round 2+ agents to operate without awareness of prior rounds, producing parallel independent analyses instead of iterative deepening. Both teams agree on CRITICAL severity and P1 remediation priority. The fix is a single variable addition to three template files.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-4: THREAT-10 is a genuine interface contract violation (HIGH)**
- **Shared assessment**: All four cross-round synthesis templates lack `DISPUTES_BEGIN`/`DISPUTES_END` markers, violating the stable interface contract at SKILL.md L683. Both teams agree this forces degraded heading-based dispute extraction for all multi-round arbiter runs. Both teams agree on P2 remediation priority.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-5: Cooperative backward compatibility is verified**
- **Shared assessment**: No cooperative-mode artifact was modified by spec 004. The SKILL.md validation table change was additive (new rows; cooperative row unchanged). All existing cooperative-mode behavior is preserved.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-6: Default-to-true is the correct failure mode for dispute parsing**
- **Shared assessment**: The Dispute-Parsing Subsystem's default behavior (return true / has disputes when parsing fails) is the correct safety-net failure mode. Running an unnecessary Phase 6 is preferable to skipping a necessary one.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-7: WTA fallback heading causes premature stagnation, not missed stagnation**
- **Shared assessment**: When structural markers are absent and the heading-based fallback fires for WTA mode, `## Runner-Up` is always present (mandatory section), causing a count of 1 every round. This triggers false stagnation on Round 2. Blue's original defense stated the opposite direction ("may miss stagnation"); Blue conceded this error in their revision. Both teams agree the primary marker-based path works correctly for WTA.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-8: Spec FR-009 heading table is stale documentation, not a functional risk**
- **Shared assessment**: The spec's FR-009 heading table diverges from SKILL.md and template reality, but SKILL.md and templates agree with each other. SKILL.md L594 directs maintainers to use templates as the source of truth. The spec is Draft status. This is documentation debt only — no runtime behavior is affected. Both teams agree on MEDIUM severity and P3 priority.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-9: Draft-gate mechanism was a genuine safeguard**
- **Shared assessment**: The `TEMPLATE_STATUS: draft` mechanism was a real defense-in-depth safeguard that was properly managed during development and cleanly removed when the feature was ready. No draft markers remain.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-10: Six original threats correctly withdrawn**
- **Shared assessment**: THREAT-03 (derivative of THREAT-01), THREAT-07 (restates THREAT-02), THREAT-08 (speculative, subsumed by THREAT-04), THREAT-09 (cosmetic, no functional impact), THREAT-11 (behavior is intentional by design), and THREAT-12 (backward compatibility verified) were correctly withdrawn. The original attack over-counted by treating derivative and cosmetic issues as independent threats.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

**CONV-11: Remediation requires no engine changes**
- **Shared assessment**: All five remediation items (P1 through P3) are template-layer edits or documentation corrections. No engine code changes are required. The engine architecture is validated as mode-agnostic and correct.
- **Agreeing agents**: Red Team, Blue Team
- **Strength**: Unanimous

---

### Final Position Statement

**Non-Negotiables:**

1. **THREAT-01 is a blocking gate for spec 004 acceptance.** The missing `{PRIOR_ROUND_SECTION}` in non-cooperative review templates is not a backlog item — it is a correctness condition. Spec 004 cannot exit Draft status until this variable is present in `templates/red-blue/review.md`, `templates/winner-take-all/review.md`, and `templates/prisoners-dilemma/review.md`. Without this fix, the feature the spec defines does not work. Both teams agree on the severity; the synthesis must classify it as blocking, not merely high-priority.

2. **THREAT-10 must be fixed in spec 004's scope, not deferred.** The cross-round synthesis marker absence may have been inherited from spec 002, but spec 004 is the spec that extends cross-round synthesis to three additional modes and makes the gap consequential. Fixing the inherited gap in all four templates is spec 004's responsibility because spec 004 is the spec that makes it matter.

3. **The synthesis must state that spec 004's engine changes are correct but the template layer is incomplete.** This is the consensus finding of both teams. The synthesis should not hedge with "mostly complete" or "minor gaps." The framing should be precise: engine correct, templates incomplete, five specific fixes required, two of which are blocking.

**Flexibility:**

1. **THREAT-02 severity (MEDIUM) is acceptable.** Blue's argument about prose instructions providing adequate mitigation for the non-cooperative arbitration templates is convincing enough to accept MEDIUM rather than HIGH. The gap should be fixed at P2, but it is not blocking.

2. **THREAT-05 and THREAT-06 can be combined into a single P3 remediation item.** The WTA fallback heading issue and the WTA dispute counting concern are closely related and have the same fix (change fallback heading from `## Runner-Up` to `### Remaining Disputes`). They can be tracked as one item.

3. **THREAT-04 (spec documentation drift) can be deferred to whenever the spec exits Draft.** Since the spec is Draft status and SKILL.md is the runtime authority, updating FR-009's heading table is not urgent. It should be done before the spec is finalized but does not need to block any other work.
