# v4.0.0 Self-Consistency Verification

**Deliberation type:** Self-consistency (per spec 067 §4 and GOVERNANCE.md Part IV Leg 1).
**Stage:** Step 5 of Phase B per GOVERNANCE.md Part VIII.
**Markers:** VISIBLE (Sync Impact Report, version markers, principle numbers, origin attributions all present).
**Acceptance bar:** 0 ACCEPT-level findings on the new wording or structure of the relocated text. ACKNOWLEDGE and DEFER findings are non-blocking.

## What is being verified

The proposed v4.0.0 amendment specified at `conversus-oss/specs/v4.0.0-tier-extraction/spec.md`. The spec relocates 20 principles from `conversus-oss/CONSTITUTION.md` (the canonical flat constitution at v3.2.3) to two newly-ratified higher-tier documents:

- **Tier 1 (Universal)** at `build-fractal/CONSTITUTION.md` — 10 principles: I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII.
- **Tier 2 (Suite)** at `build-fractal/conversus/CONSTITUTION.md` — 10 principles: V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII.

The reduced `conversus-oss/CONSTITUTION.md` retains 6 component-tier principles: XVII, XVIII, XIX, XX, XXI, XXVI. Plus retired-marker entries for VI and X (per Principle II number-stability).

The spec also formally admits both existing suite repos (conversus-oss + conversus) per their CONFORMANCE.md declarations, in line with the originating deliberation's Q2/Q3 ADMIT-PROVISIONAL rulings.

## What this deliberation must check

Self-consistency verification is the wording-precision and structural-integrity leg. Per spec 067, this leg catches drift, contradiction, and broken cross-references in the proposed amended text. The blind verification (separate deliberation, markers stripped) catches confirmation bias.

Specific checks for this deliberation:

1. **Verbatim preservation contract (spec §5).** For every relocated principle, does the spec's contract (header verbatim, body verbatim, only path-prefix cross-references rewritten) hold? Is the contract specific enough that a reviewer can falsify it?

2. **Tier classification (spec §4) internal consistency.** Are all 26 active principles + 2 retired accounted for? Do the row counts match (10 + 10 + 6 + 2 retired = 28 total slots; 26 active)? Is any principle listed in more than one tier?

3. **File edits (spec §6) completeness.** The spec enumerates 9 edits across constitution files, governance logs, CONFORMANCE.md updates, tier-coherence linter, CHANGELOG. Are any necessary edits missing? Any edit's description ambiguous (e.g., "preserve verbatim" without naming what counts as preserved)?

4. **Conditions from originating (spec §9).** All 4 P1 conditions are claimed discharged or translated. Are the discharge claims accurate per the empirical evidence cited in `VERDICT.md`? Are translations to Provisional remediations actually present in the updated CONFORMANCE.md drafts?

5. **Verification protocol (spec §8) self-application.** This spec invokes spec 067's verification protocol on itself. Does the protocol's invocation cite the right preset names (devils-advocate, balanced-arbiter)? Is the override-with-rationale precedent referenced correctly?

6. **SIR preview (spec §11) completeness.** The preview SIR text in §11 will become the live SIR in conversus-oss/CONSTITUTION.md when the impl-PR merges. Does it correctly: (a) declare 3.2.3 → 4.0.0 MAJOR; (b) enumerate all relocated and retained principles; (c) preserve the v3.2.2 SIR comment block reference for audit trail?

7. **Cross-tier number stability.** Principle II's number-stability rule is invoked across tiers (spec §5). Does the spec correctly state that Tier 1 contains numerals I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII (i.e., NON-CONSECUTIVE because some numerals went to Tier 2 / component / retired)?

8. **Tier-coherence linter (spec §6.8) feasibility.** The linter is the mechanical-verification mechanism this amendment ships with (Constitutional Inclusion Criterion 1). Is the described check actually mechanically feasible (string-match heuristic + name-collision check + version-field consistency)? Or does it require human judgment?

## Files this deliberation reads

The agents read with markers VISIBLE:

- `conversus-oss/specs/v4.0.0-tier-extraction/spec.md` — the proposed amendment text
- `conversus-oss/CONSTITUTION.md` v3.2.3 — current flat constitution (canonical source for relocations)
- `build-fractal/CONSTITUTION.md` — DRAFT Tier 1 (currently a 2-column summary; the spec's §6.1 says it'll be replaced with verbatim text post-ratification)
- `build-fractal/conversus/CONSTITUTION.md` — DRAFT Tier 2 (same)
- `build-fractal/conversus/GOVERNANCE.md` — deliberation philosophy + procedure
- `build-fractal/conversus/COMPLIANCE.md` — compliance contract
- `conversus-oss/CONFORMANCE.md` — admission declaration (5 Provisional)
- `conversus/CONFORMANCE.md` — admission declaration (4 Provisional)
- `conversus-oss/deliberations/v4.0.0-tier-extraction-originating-2026-05-06/VERDICT.md` — empirical follow-through

## Verdict format

The arbiter rules:
- **PASS** — 0 ACCEPT-level findings on new content. The spec is ready for blind verification (step 6).
- **PASS WITH FIXES** — ACCEPT findings exist but are addressable in a v2 spec revision before blind verification. Specify the fixes.
- **FAIL** — fundamental issues. Spec must be substantially redrafted; blind verification deferred.

ACKNOWLEDGE-level findings (issues raised but not blocking) and DEFER-level findings (issues for follow-on amendments) are non-blocking and listed for the record.

## Out of scope

- Pre-existing flaws in `conversus-oss/CONSTITUTION.md` (those are the blind run's domain).
- Implementation details of the impl-PR (the spec is what's being verified, not the post-merge state).
- Governance log entries that don't yet exist (the spec describes what will be added; the deliberation verifies the description, not the eventual content).
