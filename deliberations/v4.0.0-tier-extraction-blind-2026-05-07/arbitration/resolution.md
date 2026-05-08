# v4.0.0 Blind Verification — Manual Arbitration

**Status:** Manual arbitration performed because the engine's auto-arbitrator crashed at dispatch (2ms, second occurrence of the bug logged in `project_conversus_arbitration_crash_2026_05_06`). Phases 1-5 (review, cross-review, revision, disputes, synthesis) all completed successfully; only the final binding-verdict step failed.

**Recovered from:** synthesis at `summary/final.md`, two dispute documents, two revision documents, two review documents, two cross-reviews — all on disk. Manual arbitration grounded in `../../CONSTITUTION.md` v3.2.3 per spec 067 § balanced-arbiter requirements.

**Bug repeat note:** The crash threshold appears to be lower than initially estimated. Self-consistency: 231K chars → crashed (1ms). Blind: 174K chars → crashed (2ms). Two failures at materially different prompt sizes suggest the bug is in arbiter-specific dispatch logic (likely `build_arbitration_context` template assembly), not a model context limit. Task #23 description should be updated.

---

## Decision framework

Per CONSTITUTION.md § Governance and spec 067 § blind-verification methodology:
- ACCEPT findings must be on **new content** (the proposed amendment text).
- Pre-existing flaws in `../../CONSTITUTION.md` v3.2.3 surfaced incidentally DEFER to follow-on amendment cycles.
- Override-with-rationale applies ONLY when a strict reading would uniformly shrink existing ratified principles (per the 2026-04-29 Principle XXVIII precedent).
- The 5 unanimous bilateral convergences from synthesis Phase 4 are presumptively binding unless rejected with rationale.

## Binding decisions

### Convergence 1 — Linter Algorithm Inadequacy (ACCEPT)

**Position:** Header + first-paragraph substring matching is insufficient for Constitutional Inclusion Criterion 1. Sophisticated duplication patterns can defeat it.

**Ruling:** ACCEPT. Apply Fix #B1 (below).

**Grounding:** Constitutional Inclusion Criterion 1 requires mechanical verification capability. If the verification can be defeated by a duplication pattern that preserves header + first paragraph but duplicates substantive content, the linter does NOT mechanically verify the rule. Criterion 1 is unsatisfied.

**Required fix:** Spec §6.8 Check (a) MUST be strengthened. Replace "header + first-paragraph substring match" with one of:
- (a-i) Cosine similarity over normalized principle bodies with threshold (e.g., >0.85 = duplication suspected, manual review).
- (a-ii) Multi-window n-gram fingerprinting (catches partial duplications even with header rewriting).
- (a-iii) Normalized-AST diff if Markdown allows AST representation.
- Plus: an explicit escape-hatch mechanism for legitimate shared content (Origin attributions, "Extension" sub-blocks) so the strengthened check doesn't false-positive on intentionally repeated boilerplate.

The spec must specify which option(s) and the false-positive/false-negative tradeoff each carries.

### Convergence 2 — Constitutional Debt Acknowledgment (ACCEPT — Override-Adjacent)

**Position:** Universal tier carries pre-gate constitutional debt from grandfathered principles. Red-team initially demanded full re-audit; devils-advocate defended grandfathering. Compromise: explicit acknowledgment without re-audit.

**Ruling:** ACCEPT. Apply Fix #B2 (below).

**Grounding:** This is override-adjacent reasoning per the 2026-04-29 precedent — full Inclusion Criteria re-audit applied to grandfathered Tier 1 principles (I, II, III, IV, VII, VIII, IX, XI, XIV) would uniformly damage them by re-opening their constitutional validity. The compromise (transparent acknowledgment of debt without re-audit) preserves grandfathering while making the debt auditable.

**Required fix:** Spec §3 (Non-goals) and §11 (SIR preview) must include explicit language: "Tier 1 (Universal) carries grandfathered principles ratified pre-Inclusion-Criteria-gate (v2.4.0). Their constitutional validity is preserved per Principle II number-stability and the grandfathering provision; their post-gate compliance with Inclusion Criteria is NOT re-evaluated by the v4.0.0 tier extraction. Future amendments specifically targeting Tier 1 principle conformance to current Inclusion Criteria are deferred as separate cycles."

### Convergence 3 — Cross-Tier Operational Weakening Prohibition (ACCEPT)

**Position:** The spec assumes "lower tiers may strengthen but not weaken upper-tier rules" but provides no operational definition of "weakening." Vulnerable to interpretation-layer attacks (a future Tier 2 amendment that effectively weakens a Tier 1 principle without saying so).

**Ruling:** ACCEPT. Apply Fix #B3 (below).

**Grounding:** Principle II (Stable Interfaces) — without operational definitions, "weakening" is not a stable interface; future readers cannot mechanically determine compliance. Principle XIV (Spec-Implementation Parity) — the inheritance rule is a spec-level claim that needs implementation-level enforceability. The blind agents identified concrete attack scenarios; the operational definition closes the vulnerability.

**Required fix:** Spec must add a new section (suggest §5.1 or §10.1) defining: "A lower-tier amendment 'weakens' an upper-tier principle if any of: (i) the amendment grants relief from the upper-tier principle's enforcement at the lower-tier scope without invoking the formal relief pathway in COMPLIANCE.md Part VI; (ii) the amendment introduces interpretation language that, applied to existing implementations, would cause them to no longer satisfy the upper-tier principle; (iii) the amendment adds a 'suite-specific adaptation' that effectively bypasses an upper-tier principle's MUST clause." The spec must also state that the meta-arbiter for any cross-tier amendment is responsible for catching these patterns, and the tier-coherence linter (§6.8) flags any Tier 2 / Component principle text that contains "relief," "exception," or "adaptation" near the name of a Tier 1 principle for review.

### Convergence 4 — Cross-Reference Audit Methodology Expansion (ACCEPT)

**Position:** The spec's §5 cross-reference patterns table documents 4-5 patterns. Reality has more (Amendment records, inline citations, governance section back-references).

**Ruling:** ACCEPT. Apply Fix #B4 (below).

**Grounding:** Principle II (Stable Interfaces) — cross-reference patterns ARE the stable interface. Incomplete enumeration violates II.

**Required fix:** Spec §5 must expand the patterns table to include:
- Amendment record references: e.g., `(per amendment v2.X.Y)` — these appear inside principle bodies and must update if the principle relocates to a new tier.
- Inline section citations: e.g., `see § Governance` — these refer to the Governance section which stays in the component-tier file; from Tier 1 / Tier 2 they become `../CONSTITUTION.md § Governance`.
- Adjacent-phrase forms: e.g., "Principles I-V" or "see also Principle IX" — these need plural-form-aware rewriting.
- Backward references (Tier 1 → Tier 2 / Component): some governance discussion in the current constitution references higher principle numbers that will be in lower tiers. The patterns table must include these.

### Convergence 5 — Principle IV/XVII Semantic Tension (DEFER — pre-existing)

**Position:** Principle IV ("Documentation Is the Product") and Principle XVII ("Content Classification") have semantic tension; v4.0.0 entrenches the tension across tier boundaries (IV at Tier 1 Universal, XVII at Component) where it's currently flat in one document.

**Ruling:** DEFER per blind verification's pre-existing-flaws boundary.

**Grounding:** The tension is present in `../../CONSTITUTION.md` v3.2.3 today; v4.0.0's relocation makes it visible across tier boundaries but does not CREATE it. Per QUESTION.md § Out of scope, "pre-existing flaws in `../CONSTITUTION.md` v3.2.3 surfaced incidentally — those DEFER to their own follow-on amendment cycle per spec 067 § override-with-rationale boundary."

**Recommended follow-on:** Open a v4.1.x or v4.2.0 amendment cycle specifically reconciling IV and XVII — either by amending IV's body to clarify content-vs-documentation boundary, by amending XVII's body to acknowledge the documentation-equivalence interaction, or by adding cross-reference text to one or both. The reconciliation deliberation runs against both principles in their post-v4.0.0 tiered locations.

### Surviving Dispute 1 — Principle XVI Tier Classification

**Positions:**
- devils-advocate: XVI belongs at Suite-tier (architectural governance applicable to any optimization approach).
- red-team: XVI may be component-specific (engine implementation details).

**Synthesizer recommendation:** Maintain XVI at Suite-tier; add rationale documenting why mathematical transparency applies suite-wide.

**Ruling:** ADOPT synthesizer recommendation. XVI stays at Suite-tier. Spec §4 must add rationale.

**Grounding:** Mathematical transparency as a governance constraint applies to any solver/scorer in the suite. Engine-specific implementation details would belong at Component tier; XVI is about the cross-run determinism / parameter-pinning DISCIPLINE, which transcends specific solver implementations. red-team's empirical concern (what if conversus-enhanced uses neural optimization?) is addressed by maintaining XVI as discipline (constraints on results) rather than implementation (specific math operations).

**Required fix:** Spec §4 Tier 2 row for XVI must add a footnote or sub-bullet explaining "XVI applies suite-wide because mathematical transparency is the governance constraint on ANY scoring/optimization approach — it constrains the assembly form's determinism, not the optimizer's internals. Future suite siblings adopting fundamentally different optimization (e.g., neural) inherit XVI's discipline regardless of mathematical form."

### Surviving Dispute 2 — Implementation Sequencing vs. Constitutional Integrity Priority

**Positions:**
- devils-advocate: sequence structural fixes before operational improvements.
- red-team: cross-tier weakening prohibition is foundational, must ship in v4.0.0.

**Synthesizer recommendation:** Include cross-tier weakening prohibition in v4.0.0 (per red-team); apply sequencing framework to other technical improvements (per devils-advocate).

**Ruling:** ADOPT synthesizer recommendation. The cross-tier weakening prohibition is part of Convergence 3's Required Fix above (#B3) — already an ACCEPT for v3 spec. Other technical improvements (rollback verification, false-positive escape, audit expansion) are sequenced into the impl-PR review per Spec §10 already.

## Combined ACCEPT-level fixes for v3 spec

The blind verification ruled PASS WITH FIXES with five ACCEPT-level findings from the convergences plus dispute-resolution-surfaced concerns:

| # | Fix | Spec section | Grounding |
|---|---|---|---|
| B1 | Strengthen tier-coherence linter algorithm — replace header + first-paragraph match with cosine-similarity / n-gram fingerprinting / AST diff. Add escape-hatch for legitimate shared content. Specify FP/FN tradeoffs. | §6.8 Check (a) | Inclusion Criterion 1 |
| B2 | Add constitutional debt acknowledgment for grandfathered Tier 1 principles | §3 (Non-goals), §11 (SIR preview) | Override-adjacent (2026-04-29 precedent) |
| B3 | Define operational cross-tier weakening prohibition with concrete criteria (i)-(iii) for what counts as "weakening" | §5.1 NEW or §10.1 NEW | II, XIV |
| B4 | Expand cross-reference patterns table — Amendment records, inline citations, adjacent-phrase forms, backward references | §5 | II |
| B5 | Add XVI Suite-tier rationale (per Surviving Dispute 1 ruling) | §4 Tier 2 row | substantive (Dispute 1) |

ACKNOWLEDGE-level findings (non-blocking, listed for record):
- Rollback verification procedure (synthesis P2 #3) — operational improvement; impl-PR review handles
- Prohibition against interpretation-layer attacks (synthesis P2 #4) — overlaps with B3
- Reclassify XIX to Suite or Universal (synthesis P2 #1) — recommended but not blocking; could land in v3 or v4.1.x
- SIR cross-reference preservation check (P3) — operational
- Standardize priority classification (P3) — meta improvement

DEFER-level findings:
- Principle IV/XVII semantic tension — pre-existing per Convergence 5 ruling
- Suriviving Dispute 1 (XVI) — resolved; not deferred
- Suriviving Dispute 2 (sequencing) — resolved; B3 captures the v4.0.0-relevant portion

## Verdict

**BLIND VERIFICATION VERDICT: PASS WITH FIXES — apply 5 fixes (B1-B5), then proceed to impl-PR.**

The spec's structural core (tier classification 10/10/6 with XVI at Suite, verbatim preservation, file-edit enumeration, conditions discharge, self-consistency v2 fixes 1-7) is sound. Blind verification surfaced 4 substantive new-content issues (linter defeat-resistance, debt acknowledgment, weakening prohibition, cross-reference patterns expansion) and 1 dispute-resolution rationale (XVI). v3 incorporates these and proceeds directly to impl-PR — no third verification deliberation required (per spec 067, blind PASS WITH FIXES + applied fixes is sufficient unless the fixes substantively change the amendment, which these do not).

## Process notes

- **Engine arbitration crash (second occurrence):** the auto-arbitrator failed at dispatch in 2ms; same pre-LLM-dispatch failure as 2026-05-06 self-consistency run. The threshold is lower than initially estimated (174K crashed vs 231K crashed). Bug investigation task #23 should reflect this. Likely culprit is now `build_arbitration_context` template assembly in `engine/templates.py` rather than prompt size per se — the disputes-only context fix (per fractal decomposition memory) directly addresses it.
- **Manual arbitration faithfulness:** rulings adopt synthesizer-recommended resolutions exactly per their stated rationales; ACCEPT/ACKNOWLEDGE/DEFER assignments grounded in specific principles + spec 067 § blind-verification scope rules. No introduction of ratification bias — manual step performs only the binding-verdict aggregation that the auto-arbiter would have produced.
- **Override-with-rationale:** not invoked. Convergence 2 (constitutional debt) was override-adjacent in reasoning but the synthesizer's compromise (acknowledgment without re-audit) IS the override pathway taken — the strict reading (full re-audit) would shrink existing principles uniformly, the compromise preserves them.
- **Fix sequencing:** B1 → B5 fixes are independent and can land in any internal v3 ordering. The combined v3 spec carries this resolution.md as evidence of blind PASS WITH FIXES + applied fixes; the impl-PR review verifies all fixes are present.
