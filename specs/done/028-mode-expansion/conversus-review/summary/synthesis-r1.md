# Spec 028 Mode Expansion — Round 1 Synthesis

## Process Summary

- **Agents**: 3 — template-engineer, game-theorist, spec-compliance
- **Total artifacts**: 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes)
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 9 across all agents
- **Recommendations withdrawn** (Phase 3): 2 (TE-R1-03 negotiation structure concern, GT-R1-06 voting/social choice gap)
- **Recommendations modified** (Phase 3): 3 (GT-R1-01 reframed to spec update, GT-R1-03 downgraded, FR-005/FR-010/FR-011 upgraded)
- **Recommendations surviving** (Phase 3): 4 (empty tests, ration bug, spec text update, cross-round DISPUTES verification)
- **New recommendations added** (Phase 3): 1 (TE-R1-04 adopted ration bug from game theorist)
- **Disputes remaining** (Phase 4): 2
- **Convergence points** (Phase 4): 5 unanimous + 1 bilateral

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| 1 | template-engineer | Populate test_mode_expansion.py | P1 | Surviving | None | Unanimous | **Accepted** |
| 2 | template-engineer | Verify cross-round-synthesis DISPUTES markers | P2 | Modified (downgraded to P3) | spec-compliance | Bilateral | Accepted-Modified |
| 3 | template-engineer | Evaluate negotiation review structure | P3 | Withdrawn | game-theorist | N/A | **Rejected** |
| 4 | game-theorist | Document negotiation bayesian-only mapping | P1 | Modified (update spec instead) | spec-compliance | Unanimous | **Accepted-Modified** |
| 5 | game-theorist | Fix "ration" regex false positive | P2 | Surviving (upgraded to P1) | None | Unanimous | **Accepted** |
| 6 | game-theorist | Add disambiguation for resource-alloc vs. fair-division | P3 | Surviving | None | Bilateral | Accepted |
| 7 | game-theorist | Flag voting/social choice gap | P3 | Withdrawn | template-engineer | N/A | **Rejected** |
| 8 | spec-compliance | Verify FR-005 CLI and FR-010 linter | P1 | Modified (assumptions accepted) | template-engineer, game-theorist | Unanimous | Accepted-Modified |
| 9 | spec-compliance | Add regression tests for keyword classifier | P2 | Surviving | None | Bilateral | Accepted |
| 10 | game-theorist | Add "Modes Considered and Excluded" section | — | New (Phase 4) | None | None | **Disputed** |

---

## Dangerous Contradictions Found

**Resolved Contradictions:**

1. **Negotiation review template structure** (TE-R1-03 vs. game-theorist): Template engineer questioned whether the structured 4-section format was overly constraining. Game theorist argued the structure is a necessary information revelation mechanism for Bayesian games. Template engineer conceded — the structure enables ZOPA analysis by forcing controlled preference disclosure. **Resolved: game theorist's position adopted.**

2. **Negotiation game form mapping** (GT-R1-01 vs. spec-compliance): Game theorist rated the bayesian mapping as "partially correct" due to missing Stackelberg. Spec compliance classified this as a spec-implementation deviation. Game theorist revised to recommend updating the spec rather than the code. **Resolved: unanimous agreement to update spec Section 2.1.**

3. **FR-005 and FR-010 compliance** (spec-compliance vs. template-engineer/game-theorist): Spec compliance rated these PARTIALLY MET because CLI and linter were not in target files. Other agents argued the underlying data infrastructure is complete. **Resolved: upgraded to MET with assumptions.**

**Unresolved Contradictions:**

None between agents' revised positions. The two remaining disputes are about documentation scope and verification methodology, not about the mode expansion's correctness.

---

## Systemic Contradictions

1. **Spec-as-source-of-truth vs. implementation-as-source-of-truth**
   - **Manifests in**: GT-R1-01 (spec says "Bayesian + Stackelberg," implementation has bayesian only), SC-R1-01 (spec defines behaviors, tests verify them, but no tests exist)
   - **Root cause**: The mode expansion was implemented before spec 028 was finalized. The spec describes INTENDED behavior; the implementation made design choices that deviate from the spec in minor ways.
   - **Implication for spec**: Spec 028 should be treated as a post-hoc specification. Update it to match the implementation where the implementation's design choice is superior (bayesian mapping), and flag areas where the spec's intent is not yet verified (SC-005).

2. **Template quality vs. compliance verification**
   - **Manifests in**: FR-001 (template existence vs. template quality), FR-008 (heading existence vs. heading correctness), FR-011 (design argument vs. empirical test)
   - **Root cause**: Spec 028's requirements are binary (MUST) but the real quality bar is continuous. Templates can exist but be poorly written. Headings can match but be semantically wrong.
   - **Implication for spec**: The spec should include quality criteria alongside existence criteria. E.g., FR-001 should say "complete and quality-comparable template set" not just "complete template set."

---

## Convergence Achieved

- **Test file population** — Strength: Unanimous
  - **Agreed recommendation**: `tests/test_mode_expansion.py` must contain tests for: (a) `len(VALID_MODES) >= 8`, (b) each new mode has 7 templates, (c) keyword classifier routes new types correctly, (d) existing classification unchanged.
  - **Supporting agents**: template-engineer [review.md], game-theorist [review.md], spec-compliance [review.md]
  - **Evidence basis**: Empty test file is objectively verifiable. SC-005 is unverifiable without tests.
  - **Pre-existing or earned**: Pre-existing — all agents identified independently in Phase 1.

- **"ration" keyword regex fix** — Strength: Unanimous
  - **Agreed recommendation**: Fix `_DECISION_TYPE_PATTERNS[RESOURCE_ALLOCATION]` regex. Replace `ration` with `\bration(?:ing|ed)?\b` or equivalent to prevent matching "rational."
  - **Supporting agents**: game-theorist [review.md GT-R1-04], template-engineer [revision.md], spec-compliance [revision.md]
  - **Evidence basis**: "rational" appears frequently in analytical texts and would cause false classification as RESOURCE_ALLOCATION.
  - **Pre-existing or earned**: Earned — game theorist identified in Phase 1, others adopted in Phase 3.

- **Spec Section 2.1 update** — Strength: Unanimous
  - **Agreed recommendation**: Change "Game forms: Bayesian (hidden preferences) + Stackelberg (sequential offers)" to "Game forms: Bayesian (hidden preferences). Note: Sequential offer dynamics are captured by the engine's 5-phase structure rather than the game form schema."
  - **Supporting agents**: game-theorist [revision.md], template-engineer [disputes.md], spec-compliance [revision.md]
  - **Evidence basis**: Implementation maps negotiation to bayesian only. Stackelberg dynamics are procedural.
  - **Pre-existing or earned**: Earned — evolved from GT-R1-01 through cross-review discussion.

- **All mode-to-form mappings correct** — Strength: Unanimous
  - **Agreed recommendation**: The 4 new mappings (negotiation->bayesian, resource-allocation->coalitional, fair-division->coalitional, mechanism-design->mechanism-design) are formally correct.
  - **Supporting agents**: game-theorist [review.md], template-engineer [cross-review of game-theorist], spec-compliance [FR-002 MET]
  - **Evidence basis**: Game theory analysis confirms each form matches its mode's decision structure.
  - **Pre-existing or earned**: Pre-existing — game theorist assessed in Phase 1, others corroborated.

- **No redundant modes** — Strength: Bilateral
  - **Agreed recommendation**: All 8 modes are distinct. Each has a different decision structure, deliverable, and game form.
  - **Supporting agents**: game-theorist [review.md differentiation table], template-engineer [cross-review]
  - **Evidence basis**: Each mode produces structurally distinct synthesis output with mode-specific sections.
  - **Pre-existing or earned**: Pre-existing — game theorist's differentiation table in Phase 1.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

- **Dispute: SC-005 Verification Methodology**
  - **Positions**: spec-compliance insists SC-005 is NOT VERIFIABLE without running the test suite [spec-compliance/disputes.md, "Non-Negotiables" #1]. template-engineer and game-theorist argue FR-011 MET BY DESIGN logically implies SC-005 would pass [template-engineer/revision.md, game-theorist/cross-reviews/spec-compliance.md].
  - **Arguments**: Spec compliance argues that existing tests might contain hardcoded constants (e.g., `assert len(VALID_MODES) == 4`) that would fail after expansion. Template engineer and game theorist argue all changes are additive and the theoretical risk is low.
  - **Synthesizer assessment**: Spec compliance has the stronger position. The design argument is compelling but not definitive — a hardcoded constant in an existing test IS a realistic failure mode. SC-005 SHOULD be verified empirically. However, the resolution is not to dispute the design argument but to populate the test file and run it. Both sides agree on this action.
  - **Recommended resolution**: Mark SC-005 as "MET BY DESIGN, pending empirical confirmation." When tests are written and run, upgrade to MET. This satisfies both the design argument (it IS met by design) and the empirical requirement (confirmation is still needed).

- **Dispute: "Modes Considered and Excluded" Documentation**
  - **Positions**: game-theorist requests an explicit section in spec 028 documenting decision types that were considered and excluded (voting/social choice, repeated games, coalition attribution) [game-theorist/disputes.md, "Remaining Disputes" #1]. template-engineer does not object but considers it low priority. spec-compliance does not object but notes it is not an FR requirement.
  - **Arguments**: Game theorist argues this prevents future contributors from re-discovering the same gaps. Others consider it useful but optional.
  - **Synthesizer assessment**: This is a documentation quality improvement, not a functional requirement. It has no compliance impact. However, it is a genuinely useful addition that costs nothing to implement.
  - **Recommended resolution**: Accept as a P3 recommendation. Add a Section 6 "Modes Considered and Excluded" to spec 028 documenting: voting/social choice (approximated by winner-take-all), repeated games (handled by multi-round infrastructure), coalition attribution (existing mode-mapping entry).
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

**P1 — Must implement** (blocking issues or unanimous convergence):
1. **Populate test_mode_expansion.py**: Add tests for `len(VALID_MODES) >= 8`, template set completeness for each new mode, keyword classification routing, backward compatibility regression. Source: Recommendations #1, #9. Convergence: unanimous.
2. **Fix "ration" regex**: In `conversus/schemas/construction.py`, change `ration` in `_DECISION_TYPE_PATTERNS[RESOURCE_ALLOCATION]` to `\bration(?:ing|ed)?\b`. Source: Recommendation #5. Convergence: unanimous.
3. **Update spec Section 2.1**: Change negotiation game forms from "Bayesian + Stackelberg" to "Bayesian" with note about procedural Stackelberg dynamics. Source: Recommendation #4. Convergence: unanimous.

**P2 — Should implement** (majority convergence or strong single-agent case):
1. **Verify FR-005 and FR-010 assumptions**: Confirm CLI mode command derives from `_DECISION_TYPE_MODE` and linter dynamically discovers `schema/modes/` schemas. Source: Recommendation #8.
2. **Add quality criteria to spec FRs**: Update FR-001 to say "complete and quality-comparable template set." Source: Systemic contradiction #2.

**P3 — Consider implementing** (bilateral agreement or strong but disputed):
1. **Add "Modes Considered and Excluded" section**: Document voting/social choice, repeated games, coalition attribution as deliberately excluded. Source: Recommendation #10 (disputed but recommended).
2. **Verify cross-round-synthesis DISPUTES markers**: Check that all 4 new modes' cross-round-synthesis templates contain DISPUTES_BEGIN/END. Source: Recommendation #2.
3. **Add resource-allocation vs. fair-division disambiguation**: Add guidance to `/conversus mode` output. Source: Recommendation #6.

---

## Key Concessions

**template-engineer**:
- Withdrew TE-R1-03 (negotiation review structure concern) after game theorist demonstrated the structure is a necessary information revelation mechanism for Bayesian games. [template-engineer/revision.md, Concession 1]
- Downgraded TE-R1-01 (variable injection concern) to non-issue after spec compliance argued it is a core engine concern, not a mode-expansion concern. [template-engineer/revision.md, Concession 2]

**game-theorist**:
- Withdrew GT-R1-06 (voting/social choice gap) after template engineer argued it is out of scope for spec 028. [game-theorist/revision.md, Concession 1]
- Reframed GT-R1-01 from "partially correct mapping" to "spec text should be updated." [game-theorist/revision.md, Modification 1]

**spec-compliance**:
- Upgraded FR-005, FR-010, and FR-011 from PARTIALLY MET/NOT VERIFIABLE to MET based on cross-review evidence from template engineer and game theorist. [spec-compliance/revision.md, Upgrades 1-3]
