# v4.2.0 Self-Consistency Re-Run — Three Questions (v3 spec)

This is the **rerun** of stage 2 (self-consistency) triggered by Q3 FAIL-CONTRADICTION in the original round (commit `b09f227`). v2 § 5.1's blocking validation contradicted ratified Tier 2 Principle V; v3 reversed § 5.1 to non-blocking warning-based validation and applied 14 additional D-conditions (D2-D15).

Spec v3 is commit `3208bd3` on `spec/v4.2.0-structured-deliberation-outputs`.

Same agent composition as the first self-consistency stage (strict-reader, purist, principle-xxviii-fit-auditor, recursion-precedent-auditor). Same default-defend-status-quo posture. This rerun is NOT a "find new problems" exercise; it's a "verify the fixes hold up" exercise.

---

## Q1 — Principle XXVIII fit check (v3)

**Question:** Does v3 correctly implement Tier 2 Principle XXVIII after applying D9, D10, D11, D12, D14, D15?

The original Q1 returned PASS-WITH-CLARIFICATIONS with these D-conditions:
- **D9** Declare schema location in CONFORMANCE.md
- **D10** README + CLAUDE.md links (both required, per E3)
- **D11** Complete CONSUMER-CONTRACT.md content specification
- **D12** Bidirectional drift detection (per XXVIII C1)
- **D14** Fixture scope (per XXVIII C6 — 3 fixture types)
- **D15** Schema-version-bump CI detection

Verify each fix landed correctly in v3:
- v3 § 4.0 + § 6.1 (D9): schema location declared in CONFORMANCE.md
- v3 § 6.1 (D10): README.md AND CLAUDE.md both linked
- v3 § 7.1 (D11): six-section CONSUMER-CONTRACT.md content spec
- v3 § 5.4 (D12): bidirectional drift-detection job
- v3 § 5.3 (D14): four fixture types
- v3 § 5.4 (D15): schema-version-bump detection job

Plus the meta-check: did v3 introduce any NEW Principle XXVIII fit gaps while applying these fixes?

Output: per-sub-clause finding (SATISFIES / PARTIALLY-SATISFIES / UNDERSATISFIES / OVERSATISFIES); Q1 verdict (PASS / PASS-WITH-CLARIFICATIONS / FAIL-INCOMPLETE-IMPLEMENTATION).

---

## Q2 — Temporal-constraint reframing + Tier 3 coherence

**Question:** Does v3's temporal-constraint reframing (replacing RECURSION-EXEMPTED, D4+D5) hold up structurally? Is the anti-precedent language tight enough to prevent future invocations?

The original Q2 returned PASS-WITH-CLARIFICATIONS, finding RECURSION-EXEMPTED structurally similar to v4.1.0's rejected override-with-rationale stretch but REDEEMABLE via temporal-constraint reframing (bootstrap paradox vs. ongoing relief).

v3 implements the redemption in:
- § 9.1: explicit retirement of "RECURSION-EXEMPTED" label; replaced with bootstrap-paradox temporal-constraint language
- § 9.1 D5 paragraph + § 9.2 (i) assessment: anti-precedent containment ("adjacent," "similar," or "schema-touching" framings are explicitly barred from invoking the same exemption)
- § 9.2 (new): cross-tier weakening assessment per D3 (criteria i/ii/iii — v3 claims none are triggered)
- § 9.3 (new): forward-promotion pathway (Tier 3 → Tier 2 when sibling joins)

Examine:
- **Temporal-constraint logic.** Bootstrap paradox claim: "this spec can't be required to use a schema that doesn't yet exist." Is this a logical impossibility (acceptable framing) or a procedural convenience (rejectable framing)? Compare carefully against v4.1.0's temporal-vs-membership precedent.
- **Anti-precedent tightness.** v3 § 9.1's D5 language bars future invocations under "adjacent," "similar," or "schema-touching" framings. Is "schema-touching" tight enough, or could future amendments creatively re-frame their case? Stress-test with hypothetical future amendments.
- **Cross-tier weakening assessment.** v3 § 9.2 claims criteria (i)/(ii)/(iii) are NOT triggered. Audit this claim against the actual criteria text in Tier 2 CONSTITUTION.md L475-488.
- **Forward-promotion pathway.** v3 § 9.3 specifies how Tier 3 → Tier 2 promotion happens. Is the pathway concrete enough that a future sibling joining the suite knows what to do?

Output: per-axis finding; Q2 verdict (PASS / PASS-WITH-CLARIFICATIONS / TIER-2-PROMOTE-RECOMMENDED / RECURSION-PRECEDENT-FAIL).

---

## Q3 — Principle V contradiction reversal + new contradiction check

**Question:** Does v3's § 5.1 fully reverse the v2 contradiction with Principle V? AND does v3 introduce any new contradictions while fixing the old one?

The original Q3 returned FAIL-CONTRADICTION on v2's § 5.1 blocking validation. v3 § 5.1 is fully rewritten per D1:
- Opens with the Principle V quote
- States validator MUST NOT raise/abort
- Persistence layer pseudocode shows `path.write_bytes(content)` called UNCONDITIONALLY before any error handling
- Warning emission goes to event stream + sidecar `.validation-warnings.json`
- Mechanical enforcement bite moved entirely to § 5.4 PR-time CI gate

Verify:
- **D1 reversal is complete.** § 5.1 has no residual blocking language. Every validator call path is non-blocking.
- **PR-time CI gate enforcement (in § 5.4) is constitutional.** A PR-blocking CI gate is different from a write-blocking validator. The PR gate prevents merging non-conformant code; it doesn't prevent runtime persistence. This is the right shape per Principle V — but verify the spec text doesn't blur the distinction.
- **No NEW contradictions introduced.** Walk through v3's new sections (§ 4.0, § 5.3, § 5.4, § 6.1, § 7.1, § 9.2, § 9.3) and check each against Tier 1 + Tier 2 + component principles. A 156-line addition is large enough to risk introducing new contradictions.
- **D2 strike of Principle II misattribution** — did v3 remove the misattribution cleanly?
- **D3 cross-tier weakening assessment** — does the new § 9.2 honestly assess against the criteria, or does it conveniently conclude no weakening?

Output: per-axis finding; Q3 verdict (PASS / PASS-WITH-CLARIFICATIONS / FAIL-CONTRADICTION).

---

## Arbiter ruling format

**Q1 (XXVIII fit, v3):**
- PASS — fixes landed correctly + no new gaps
- PASS-WITH-CLARIFICATIONS — specify E-conditions for spec v4
- FAIL-INCOMPLETE-IMPLEMENTATION — substantive XXVIII gap remains

**Q2 (temporal-constraint reframing):**
- PASS — reframing holds + anti-precedent language tight
- PASS-WITH-CLARIFICATIONS — specify E-conditions
- TIER-2-PROMOTE-RECOMMENDED — Tier 3 instability surfaced
- RECURSION-PRECEDENT-FAIL — reframing didn't redeem

**Q3 (Principle V reversal + new-contradiction check):**
- PASS — § 5.1 reversal clean + no new contradictions
- PASS-WITH-CLARIFICATIONS — specify E-conditions
- FAIL-CONTRADICTION — residual or new contradiction

Conclude with three ruling lines:
- `Q1 RULING: <verdict> — <one-line rationale>`
- `Q2 RULING: <verdict> — <one-line rationale>`
- `Q3 RULING: <verdict> — <one-line rationale>`

Combined disposition:
- All PASS-variant: proceed to blind verification with any E-conditions applied to produce spec v4.
- Any FAIL: spec returns to v3 review; blind doesn't run until FAIL addressed.
- TIER-2-PROMOTE-RECOMMENDED: rewrite at Tier 2 and re-run this stage.

This is the SECOND attempt at stage 2. If it doesn't pass cleanly, v4.2.0's scope problems may be more fundamental than D-condition patches can fix.
