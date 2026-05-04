# Feature Specification: Spec 070 Closure Correction — Supplemental §9 AC #5 Verification

**Feature ID**: `073-spec-070-closure-correction`
**Created**: 2026-05-03
**Status**: **Closed 2026-05-04** — supplemental blind deliberation completed (`deliberations/070-supplemental-blind-2026-05-04/`); **VERDICT: SUSTAINED WITH FINDINGS**. The §9 AC #5 verification obligation is discharged. The migrations of VI, X (pending cycle 3A path-(c) assessment), and XVI plain-language clause hold under the contrarian standard. Four findings were filed as follow-up issues (#119 cycle 3A path-(c) for X, #120 cycle 3B X error-handling routing, #121 cycle 3C XVI Criterion 1 + determinism-scope retention, #122 cycle 3D gate calibration positive worked example). These follow-ups are tracked independently and do not block spec 073 closure. Spec 070's audit trail is now complete through the §9 AC #5 supplemental verification.
**Depends On**: `067-verification-methodology` (defines the dual-deliberation protocol this spec must satisfy), `070-grandfathered-audit` (the spec whose closure this spec corrects)
**Governed by**: `CONSTITUTION.md` Governance section — amendment process. This spec is governance-meta: it corrects a closure-process gap in spec 070's verification trail. The implementation does not change any constitutional principle; it discharges an outstanding verification obligation.
**Originating context**: 070-closure-verification deliberation 2026-05-03 (`deliberations/070-closure-verification-2026-05-01/`). The deliberation's arbitration ruled **SPEC-070-CLOSURE VERDICT: PREMATURE — REOPEN**: spec 070 §9 AC #5 — which required a blind verification deliberation configured with a contrarian agent explicitly arguing one or more of VI/X/XVI passes the v2.4.0 gate on closer reading and should NOT be migrated, run against a pre-migration document — was not satisfied before PR #99 merged.

> **Explicit closure-gap acknowledgment**: Spec 070's `specs/done/` placement (PR #99, 2026-05-01) preceded §9 AC #5 satisfaction. The cycle 2 blind deliberation ran against `CONSTITUTION-v3.0.0-blind.md`, a post-migration document from which VI and X were already absent, making the required contrarian argument structurally impossible to construct regardless of agent configuration. The cycle 1 blind deliberation ran against XVI under a structural incoherence / redundancy framing, not a passes-the-gate-and-should-NOT-be-migrated framing. Spec 070's `specs/done/` placement is therefore a false certification of completion as of 2026-05-01. This spec exists to discharge the outstanding verification obligation; spec 070 itself remains physically in `specs/done/` to preserve the audit trail of when the false closure happened.

> **Path (b) per the closure-verification verdict**: This spec implements path (b) of the two equivalent remedy paths. Path (a) would have moved spec 070 back to `specs/` and completed the supplemental blind before re-closing. Path (b) leaves spec 070 in `specs/done/` (preserving the audit trail of the false closure timestamp) and creates this named follow-up spec to carry the remaining verification work with its own spec 067 verification trail.

---

## 1. Summary

The closure-verification deliberation 2026-05-03 identified that spec 070's stated acceptance criteria (§9) include AC #5 (blind verification deliberation with a contrarian "passes the gate" agent prompt against a pre-migration document) which was not satisfied at the time PR #99 merged spec 070 to `specs/done/`. This spec authorizes:

1. **A supplemental blind deliberation** (per spec 067 §6.2) against a pre-migration document (v2.4.0 or v2.5.0 era CONSTITUTION.md containing Principles VI, X, and XVI in un-migrated form) with at least one agent explicitly prompted to argue one or more of VI/X/XVI passes the v2.4.0 gate on closer reading and should NOT be migrated.
2. **A determinate verification verdict** from that supplemental blind on whether the migration decisions for VI, X, and XVI hold under the contrarian standard the original AC #5 mandated.
3. **A coordinated CONSTITUTIONAL_CONVERSATIONS.md update** marking that the §9 AC #5 obligation has been discharged (when the supplemental blind completes), with the verification trail filed in CONSTITUTIONAL_CONVERSATIONS.md per spec 070 §9 AC #6.

This spec does NOT re-litigate the migration decisions themselves. The contrarian deliberation's verdict is binding on the closure record but does not automatically reverse migrations that have already been ratified across PRs #95, #98. If the contrarian deliberation surfaces a finding that one or more migrations were incorrect under the gate's strict reading, that finding becomes a separate amendment cycle (subject to the full spec 067 dual-deliberation protocol) — it does not block spec 073 from closing once the verification work is completed and recorded.

## 2. Goals

1. **Discharge §9 AC #5**: run the supplemental blind deliberation per the precise terms of spec 070 §9 AC #5 — pre-migration target, contrarian agent prompt, devils-advocate + balanced-arbiter presets per spec 070 §6.2.
2. **Record the verdict**: file the deliberation in `deliberations/070-supplemental-blind-YYYY-MM-DD/` and append a coordinated entry to `CONSTITUTIONAL_CONVERSATIONS.md` documenting the verdict.
3. **Update spec 070's closure record**: add a note to spec 070's spec.md in `specs/done/` cross-referencing this spec and the supplemental deliberation's verdict.
4. **Restore audit-trail integrity**: the closure of spec 070 was incomplete; this spec's closure restores the verification trail to the state spec 070 §9 required.
5. **Codify the lesson**: future spec 070-class amendments must satisfy AC #5 BEFORE the implementation PRs land, not after. Spec 067 §6.2 should reflect this sequencing constraint.

## 3. Non-goals

- **Reversing the v3.0.0 / v3.1.0 / v3.1.1 / v3.1.2 / v3.1.3 amendments**: those ratifications stand on their own dual-deliberation cycles (cycle 1 self+blind, cycle 2A self+blind, cycle 2B/2C/v3.1.2/v3.1.3 single-PR pathways). The contrarian deliberation may inform future amendment cycles but does not retroactively unwind ratified content.
- **Re-running the cycle 1 or cycle 2A deliberations**: the supplemental blind is a NEW deliberation against a pre-migration target, not a re-run of either prior cycle. Spec 067 explicitly contemplates supplemental verification when AC gaps surface.
- **Adding new constitutional principles**: this spec is purely process-restorative. No principle is added, removed, or amended by this spec's implementation.

## 4. Methodology — supplemental blind deliberation

Per spec 067 §6.2, the supplemental blind MUST satisfy:

### 4.1 Target document

Authenticate (against git history) a pre-migration constitution containing VI, X, and XVI in their pre-cycle-1 form. Candidate targets:
- v2.4.0 CONSTITUTION.md (the state immediately after the Constitutional Inclusion Criteria gate landed but before the cycle 1 XVI rewrite)
- v2.5.0 CONSTITUTION.md (after Principle XXVIII ratified, but before any of the cycle 1/2 grandfathered-principle changes)

The chosen target MUST be the unmodified state at the named tag. The strip-script-for-blind utility runs in its standard configuration; no custom stripping for this deliberation.

### 4.2 Agent configuration

Minimum 2 agents, cooperative or red-blue mode:
- **Agent 1 (mandatory)**: contrarian — preset `presets/role/devils-advocate.yml`. Prompt MUST explicitly argue one or more of VI/X/XVI passes the v2.4.0 gate on closer reading and should NOT be migrated. The argument must be made in good faith — adversarial but coherent — not as a strawman.
- **Agent 2**: gate-faithfulness — argues the v2.4.0 gate is correctly applied to VI/X/XVI. Preset open (`presets/philosophy/pragmatist.yml` is appropriate, as is no preset).

Optional Agent 3: cross-principle-coherence — checks that whatever verdict the deliberation reaches does not introduce inconsistencies with the Constitutional Inclusion Criteria's worked examples (the principle that fails Criterion 1 because "code should be readable", or the principle that fails Criterion 3 because it composes from existing principles).

### 4.3 Arbiter

`presets/role/balanced-arbiter.yml`. The arbiter's grounding document is the pre-migration constitution (target document). The verdict line MUST be one of:
- `SPEC-070 §9 AC #5 VERDICT: SUSTAINED` — migration decisions for VI, X, and XVI hold under the contrarian standard.
- `SPEC-070 §9 AC #5 VERDICT: SUSTAINED WITH FINDINGS` — migrations hold but the deliberation surfaced findings worth preserving in the audit trail.
- `SPEC-070 §9 AC #5 VERDICT: PARTIALLY SUSTAINED` — at least one migration hold; at least one is overturned. This verdict triggers a separate amendment cycle for the overturned migration(s).
- `SPEC-070 §9 AC #5 VERDICT: NOT SUSTAINED` — the contrarian standard finds one or more migrations were incorrect. This verdict triggers a separate amendment cycle for each overturned migration.

### 4.4 Implementation PR for this spec

The implementing PR MUST:
1. Place the deliberation directory at `deliberations/070-supplemental-blind-YYYY-MM-DD/`.
2. Append a coordinated entry to `CONSTITUTIONAL_CONVERSATIONS.md` documenting the verdict and any findings.
3. Add a "Closure record" subsection to `specs/done/070-grandfathered-audit/spec.md` cross-referencing this spec (#073) and the supplemental deliberation's verdict.
4. Move this spec (`073-spec-070-closure-correction.md`) from `specs/` to `specs/done/`.
5. NOT make any other constitutional changes (those are separate cycles).

## 5. Success criteria

This spec is "done" when:

1. The supplemental blind deliberation has run with the configuration in §4.
2. The verdict is one of the four enumerated values in §4.3.
3. The deliberation directory + CONCONV.md entry + spec 070 closure record are filed.
4. This spec is moved to `specs/done/`.

If the verdict is `PARTIALLY SUSTAINED` or `NOT SUSTAINED`, the closure of this spec records that fact; the corrective amendment cycle(s) are separate spec(s).

## 6. Risks and mitigations

- **Risk: contrarian agent fails to construct a credible argument**. Mitigation: cooperative cross-review forces the gate-faithfulness agent to engage with whatever argument the contrarian produces; if cross-review reveals the argument is incoherent, the synthesis records that and the verdict is SUSTAINED on those grounds. The deliberation does not require a "balanced" verdict — it requires a verdict grounded in the pre-migration document.
- **Risk: contrarian agent surfaces a finding that contradicts a ratified migration**. Mitigation: this is a feature, not a bug. The closure-verification deliberation's purpose is to detect exactly this case. If the verdict is `PARTIALLY SUSTAINED` or `NOT SUSTAINED`, the corrective cycle is a separate amendment governed by spec 067's dual-deliberation protocol.
- **Risk: target document selection is gameable**. Mitigation: §4.1 enumerates candidate targets and constrains them to authenticated git tags. The implementing PR MUST cite the specific git tag and commit hash used.

## 7. References

- `070-grandfathered-audit/spec.md` (in `specs/done/`) — the spec this spec corrects.
- `067-verification-methodology` — defines spec 067 §6.2 supplemental verification protocol.
- `deliberations/070-closure-verification-2026-05-01/arbitration/resolution.md` — the verdict that authorized this spec.
- `CONSTITUTIONAL_CONVERSATIONS.md` — running log; will carry the supplemental blind's entry.
- `presets/role/devils-advocate.yml` and `presets/role/balanced-arbiter.yml` — required presets per §9 AC #5.
- `scripts/strip-constitution-for-blind.py` — strip utility (post-PR #108 fix for HTML comment exclusion).
