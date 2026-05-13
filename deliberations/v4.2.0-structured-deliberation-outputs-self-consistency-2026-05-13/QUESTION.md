# v4.2.0 Self-Consistency Verification — Three Questions

This is **stage 2 of 3** in the v4.2.0 verification protocol per spec 067. The originating stage (`6478ac7`) returned APPROVE-WITH-FIXES on Q1+Q2 and TIER-3-CONFIRMED + RECURSION-EXEMPTED on Q3. Ten C-conditions (C1-C10) were applied in spec v2 (commit `edf80b4`), including the load-bearing C1 flip from XSD to JSON Schema as the canonical schema language AND file format.

The agent composition is intentionally orthogonal to originating:
- Originating used: engineer, schema-design-expert, adapter-consumer, devils-advocate
- Self-consistency uses: **strict-reader, purist, principle-xxviii-fit-auditor, recursion-precedent-auditor**

Default posture: **defend the status quo.** Ratification bias is strong by this stage — the originating already approved.

---

## Q1 — Principle XXVIII fit check

**Question:** Does spec v2 correctly implement Tier 2 Principle XXVIII (Persistence Contract Discipline)? Walk through each sub-clause of Principle XXVIII and verify v2's mechanisms satisfy it.

Principle XXVIII (in `build-fractal/conversus/CONSTITUTION.md` L490-644) has:
- Sub-clause 1: declared schema with `schema_version`, discoverable location
- Sub-clause 2: mechanical CI enforcement, PR-required, machine-executable conformance
- Sub-clause 3: documented versioning bump procedure (SemVer or documented alternative)
- Sub-clause 4: cross-product CONSUMER-CONTRACT.md
- Sub-clause 5: declaration scope (explicit declaration in CONSUMER-CONTRACT.md naming surface + stability guarantee)

For each sub-clause, verify v2's corresponding mechanism:
- Sub-clause 1 → v2's `engine/schema/v1/*.schema.json` files at documented location, with `$id` and version field
- Sub-clause 2 → v2's `schema_validator.py` + <100ms budget + PR-required CI gate per C3
- Sub-clause 3 → v2's § 4.8 SemVer policy (consumer-impact rule)
- Sub-clause 4 → v2's CONSUMER-CONTRACT.md authoring for conversus-oss + orchestrator
- Sub-clause 5 → v2's envelope + per-output declaration of stable surfaces

Examine: does v2 actually satisfy what XXVIII mandates, or does it satisfy something narrower / broader?

Output: per-sub-clause finding (SATISFIES / PARTIALLY-SATISFIES / UNDERSATISFIES / OVERSATISFIES); Q1 verdict (PASS / PASS-WITH-CLARIFICATIONS / FAIL-INCOMPLETE-IMPLEMENTATION).

---

## Q2 — Tier 3 placement coherence with recursion-exempted ruling

**Question:** Does v2's Tier 3 (Component) placement + RECURSION-EXEMPTED status create any precedent problem for future amendments?

The originating arbitration's Q3 ruling combined two decisions:
1. **Tier 3 placement** — only conversus-oss produces deliberation outputs today, so Component tier matches evidence base
2. **RECURSION-EXEMPTED** — this spec's own verification uses markdown, not the schema it's about to mandate

Examine:
- **Tier 3 stability.** If a future conversus-* sibling produces deliberation-like artifacts (e.g., a hypothetical `conversus-investigations`), the schema discipline would need to either (a) re-litigate at Tier 2, or (b) inherit via some Tier-3-component-pattern-promotion mechanism. Is option (b) defined anywhere in v2? If not, future amendment friction.
- **Recursion-exempted as precedent.** v2 § 9 documents the exemption (per Q3). Does the exemption create a precedent where future amendments to schema-related specs can claim "we're amending the meta-schema, exempt from the schema we're amending"? This is the kind of slippery precedent the override-with-rationale debacle in v4.1.0 self-consistency was about.
- **Markdown deprecation cliff (2026-12-01).** v2 § 11 sets a tiered rollout T1-T4. The cliff date aligns with Principle XXVIII's universal deadline. But if v4.2.0 ratifies AFTER 2026-12-01 (verification cycles take time), the cliff is in the past at ratification. Does v2 handle this temporal hazard?
- **Schema versioning interaction with C10 (`1.0.0-rc.1`).** v2 starts at rc.1 with a 30-day-clean-operation bump to 1.0.0. Does this rc cycle interact with Principle XXVIII sub-clause 3's SemVer mandate cleanly?

Output: per-axis finding; Q2 verdict (PASS / PASS-WITH-CLARIFICATIONS / TIER-2-PROMOTE-RECOMMENDED / RECURSION-PRECEDENT-FAIL).

---

## Q3 — Internal contradiction check

**Question:** Does spec v2 contradict any existing principle in Tier 1, Tier 2, or component-tier conversus-oss CONSTITUTION.md?

Particular vectors of concern:
- **Tier 1 Principle II (Stable Interfaces).** v2 mandates schemas as stable surfaces. Does this duplicate, conflict with, or extend Principle II's existing stable-interface coverage? Per spec § 4 preamble of XXVIII (E4): "Persistence contracts ARE stable interfaces." Does v2 honor that framing or quietly redefine it?
- **Tier 2 Principle XXVIII itself.** v2 IS the implementation of XXVIII for conversus-oss. Does v2 mandate anything XXVIII doesn't require? OR fail to mandate something XXVIII does require? Either direction is a problem.
- **Tier 2 Principle V (Output Contract Coverage).** Conversus engine's V remediation was the load-bearing track cited in spec v4.1.0 § 1 motivating evidence. Does v4.2.0 conflict with or supersede V's enforcement model?
- **Tier 2 Principle XXII (Distribution Surface Integrity).** XXII covers build-time/distribution surfaces. v4.2.0 covers deliberation output surfaces. Adjacent but distinct — verify no overlap creates double-binding.
- **Component-tier conversus-oss CONSTITUTION.md.** Check whether v4.2.0's mandates clash with any component-level principle (e.g., principles about engine architecture, provider abstraction, etc.).

Default posture: defend the status quo. Existing principles are ratified; v4.2.0 is the candidate.

Output: per-principle finding (CONTRADICTS / OVERRIDES / MODIFIES / HARMONIZES); Q3 verdict (PASS / PASS-WITH-CLARIFICATIONS / FAIL-CONTRADICTION).

---

## Arbiter ruling format

**Q1 (Principle XXVIII fit):**
- PASS — v2 correctly implements all five XXVIII sub-clauses.
- PASS-WITH-CLARIFICATIONS — specify D-conditions for spec v3.
- FAIL-INCOMPLETE-IMPLEMENTATION — substantive gap; specify which sub-clause and what's missing.

**Q2 (Tier 3 + recursion-exempted coherence):**
- PASS — Tier 3 + exemption stable; no precedent problem.
- PASS-WITH-CLARIFICATIONS — minor wording fixes for precedent boundaries.
- TIER-2-PROMOTE-RECOMMENDED — Tier 3 instability surfaced; recommend promotion.
- RECURSION-PRECEDENT-FAIL — exemption creates slippery precedent.

**Q3 (Internal contradiction check):**
- PASS — no contradictions across examined principles.
- PASS-WITH-CLARIFICATIONS — specify D-conditions.
- FAIL-CONTRADICTION — substantive contradiction; specify principle + evidence.

Conclude with three ruling lines:
- `Q1 RULING: <verdict> — <one-line rationale>`
- `Q2 RULING: <verdict> — <one-line rationale>`
- `Q3 RULING: <verdict> — <one-line rationale>`

Combined disposition:
- All PASS-variant: proceed to blind verification with D-conditions applied to produce spec v3.
- Any FAIL: spec returns to v2 review.
- TIER-2-PROMOTE-RECOMMENDED: spec rewrites at Tier 2; this stage re-runs.
