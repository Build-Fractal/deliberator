# v4.1.0 Self-Consistency Re-Run — Three Questions (v3 spec)

This is the **rerun** of stage 2 (self-consistency) triggered by the original self-consistency stage's `Q2 DEMOTE-TO-TIER-2` disposition. Per the original stage's QUESTION.md combined disposition rule: "Q2 DEMOTE-TO-TIER-2: spec rewrites under Tier 2; this stage re-runs."

The spec has been rewritten as **v3** (commit `3a7a43a` on `spec/v4.1.0-persistence-contract-discipline`). v3 applies all seven Summary-of-Changes items from the original self-consistency arbitration (`8f90e2d`'s `arbitration/resolution.md`):

- **Change 1** — Tier 1 → Tier 2 placement (new Tier 2 Principle XXVIII)
- **Change 2** — Differentiated deadlines removed; universal 2026-12-01 deadline
- **Change 3** — Override-with-rationale precedent restricted to blind-verification scope only (new spec § 11)
- **Change 4** — Compound constitutional debt acknowledgment (new spec § 12)
- **Change 5** — Coordinated governance analysis methodology noted
- **Change 6** — Conditional constitutional coordination analysis preserved
- **Change 7** — v2 originating Q2 rationale rewritten to drop override-with-rationale invocation; preserved on substantive technical convergence grounds

This rerun verifies that v3's changes correctly address the original verdict and that no new contradictions or scope-stretches were introduced in the process.

The agent composition is the same as the first self-consistency stage: same four agents, same default-defend-status-quo posture, same orthogonality to the originating composition. The rerun is NOT a "find new problems" exercise; it's a "verify the changes hold up" exercise. Agents that find no further issues should rule PASS.

---

## Q1 — Internal contradiction check (v3)

**Question:** Does spec v3 § 4 (the new Tier 2 Principle XXVIII text) contradict, override, or implicitly modify any existing principle in Tier 1 `build-fractal/CONSTITUTION.md` or Tier 2 `build-fractal/conversus/CONSTITUTION.md`?

The amendment is now a new Tier 2 principle, not a sub-clause appended to Tier 1 Principle II. The mechanical-enforcement sub-clauses (declared schemas with version fields, PR-required CI gates, versioning bump procedure, cross-product CONSUMER-CONTRACT.md surfaces, declaration scope) live at suite level.

Re-examine the previous round's vectors of concern with v3 as the subject:

- **Tier 1 Principle II's named-surface list** — v3 no longer touches Principle II. Check whether v3's new Tier 2 Principle XXVIII inadvertently restates or weakens Principle II's named-surface coverage.
- **Tier 1 Principles VII/VIII (xfail surfaces)** — v3's universal deadline is now 2026-12-01 for all conversus-suite products. Does this clash with any Tier 1 xfail-allowance principle?
- **Tier 2 conversus-specific principles** — v3 adds principle XXVIII alongside the existing Tier 2 set (V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII). Does XXVIII contradict, duplicate, or weaken any of them? XXII (Distribution Surface Integrity) is the closest neighbor — verify no contradiction.

Output: per-principle finding with quoted text. If no contradictions found, say so explicitly and list which principles were examined.

---

## Q2 — Tier 2 placement coherence

**Question:** Does v3's Tier 2 placement match the suite-level evidence base correctly?

Spec v3 § 1 still cites the original two evidence pieces (conversus-oss V xfail; spec-kit-orc adapter drift). Both are conversus-suite products. For Tier 2 (Suite) placement to be justified, the evidence must apply uniformly across the suite — i.e., the discipline should apply to all conversus-family products including future siblings (conversus-pro, conversus-solvers, etc.).

Re-examine:
- **Suite-wide applicability.** Does the principle apply uniformly to ALL conversus-suite products, or only to the two products that surfaced the evidence?
- **Tier 2's named-surface logic.** Tier 2 CONSTITUTION.md L62-65 says lower tiers may strengthen but not weaken upper-tier principles. Does v3's Tier 2 Principle XXVIII inadvertently weaken or restate any Tier 1 principle's persistence-surface coverage?
- **Forward sibling fit.** When a paid conversus-* sibling joins, does the principle apply automatically, or does it need a tier-specific exception? If the latter, that's a sign the placement still doesn't fit.

Output: a verdict (PASS / DEMOTE-TO-TIER-3 / NEEDS-MORE-EVIDENCE) with concrete reasoning grounded in Tier 2 CONSTITUTION.md's tier-applicability logic.

---

## Q3 — Override-precedent restriction documentation adequacy

**Question:** Does v3's new § 11 (Override-with-rationale Scope Restriction) adequately document the precedent's blind-verification-only scope, and is the v2-Q2-rationale rewrite (per Change 7) substantively sound?

The previous round's Q3 FAIL-OVERSTRETCH ruling required: "Document immediate restriction of override-with-rationale precedent to blind-verification scope only. Require explicit constitutional amendment for any future scope extensions."

v3 § 11 is the documentation. Verify:
- **Scope clarity.** Does § 11 unambiguously state the precedent applies only to blind-verification verdicts? Is the immediate-effect date clear?
- **Future-extension constraint.** Does § 11 require explicit constitutional amendment (originating + self-consistency + blind verification) for any scope extension? Is the bar high enough?
- **v2 rationale rewrite.** v3's "Changelog from v1 (revised in v3 per Change 7)" should describe the originating Q2 ruling as APPROVE-WITH-FIXES based on three-of-four substantive technical convergence, NOT on override-with-rationale invocation. Verify the language is clean.
- **Compound debt acknowledgment.** v3 § 12 (Compound Constitutional Debt) acknowledges both the Tier 1 placement and the override-precedent stretch as unified governance gaps. Verify the acknowledgment is honest and not just performative.

Output: a verdict (PASS / PASS-WITH-EDITS / FAIL-INADEQUATE) with specific evidence from spec v3.

---

## Arbiter ruling format

For each question:

**Q1 (Internal contradiction check, v3):**
- PASS — no contradictions; v3's Tier 2 principle XXVIII coheres with existing Tier 1 + Tier 2 principles.
- PASS-WITH-CLARIFICATIONS — minor harmonization needed; specify D2-conditions.
- FAIL — substantive contradiction; specify which principle and what evidence would change the verdict.

**Q2 (Tier 2 placement coherence):**
- PASS — Tier 2 placement justified by suite-wide evidence.
- DEMOTE-TO-TIER-3 — evidence is actually conversus-oss-component-only; should be Tier 3.
- NEEDS-MORE-EVIDENCE — suite-wide applicability needs explicit forward-sibling fit analysis.

**Q3 (Override-precedent restriction adequacy):**
- PASS — § 11 documentation is clear; v2 rationale rewrite is clean.
- PASS-WITH-EDITS — minor wording fixes specified.
- FAIL-INADEQUATE — § 11 doesn't sufficiently constrain future scope extensions OR the v2 rationale rewrite still implicitly invokes override-with-rationale.

The combined verdict determines the next stage:
- **Q1+Q2+Q3 all PASS (any variant): proceed to blind verification** with any D-conditions applied to produce spec v4.
- Any FAIL: spec returns to v3 review; blind verification does not run until the FAIL is addressed.
- Q2 DEMOTE-TO-TIER-3: spec rewrites at Tier 3 (component); this stage re-runs once more.

Per the established pattern: this is the **second** attempt at stage 2. If it doesn't pass cleanly, the amendment's scope problems may be more fundamental than the demote alone can fix.
