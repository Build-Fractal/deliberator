# v4.0.0 Originating Deliberation — Tier Extraction & Suite Admission

**Pathway:** MAJOR (CONSTITUTION.md § Pathway Taxonomy)
**Date:** 2026-05-06
**Stage:** Originating (per GOVERNANCE.md Part VIII step 3 — produces proposed amendment list for spec drafting)

---

## What this deliberation decides

Three bundled questions:

### Question 1 — Tier classification

The current `conversus-oss/CONSTITUTION.md` (v3.2.3) carries 26 active principles in a flat list. The proposed v4.0.0 amendment splits them into three tiers:

- **Tier 1 (Universal)** — applies to every Build Fractal product. Lives at `build-fractal/CONSTITUTION.md`.
- **Tier 2 (Suite)** — applies to all conversus-family repos. Lives at `build-fractal/conversus/CONSTITUTION.md`.
- **Component** — applies only to one repo. Stays at `conversus-oss/CONSTITUTION.md` (reduced).

Proposed classification (from Phase 1 exploration):

| Tier | Principles | Count |
|---|---|---|
| Universal (Tier 1) | I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII | 10 |
| Suite (Tier 2) | V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII | 10 |
| Component | XVII, XVIII, XIX, XX, XXI, XXVI | 6 |
| Retired (no tier) | VI, X | 2 |

Total: 10 + 10 + 6 = 26 active. Plus 2 retired (numbers preserved per Principle II).

**Decide:** Is this classification correct? For each principle, does its proposed tier match its actual scope? Are there principles that should move?

### Question 2 — conversus-oss admission

The repo `conversus-oss` currently carries the constitution; under the new structure it will be a **suite member** with its own `CONFORMANCE.md` declaring compliance against Tier 1 + Tier 2 + its own retained component-tier principles.

DRAFT declaration: `conversus-oss/CONFORMANCE.md` (2026-05-06).
- 0 N/A claims
- 2 Provisional remediations (XII no-dead-infra linter, XXII vendoring CI)
- 0 Relief claims

**Decide:** Does the declaration accurately reflect repo state? Are the two Provisional remediations adequate? Should anything be reclassified (Satisfied → Provisional, or vice versa)?

### Question 3 — conversus admission

The repo `conversus` (paid layer, package `conversus-enhanced`) joins the suite as a sibling under Tier 1 + Tier 2 inheritance, with no component-tier principles of its own (yet).

DRAFT declaration: `conversus/CONFORMANCE.md` (2026-05-06, post PR #30).
- 4 N/A claims (V Observable Deliberation, VIII Templating Engines, XIII Enum Completeness, XXIII Provider Robustness)
- 4 Provisional remediations (III CHANGELOG, XIV parity check, XVI determinism harness, XXII vendoring)
- 0 Relief claims

**Decide:** Do the four N/A claims have sufficient structural justification? Are the four Provisional remediations adequate and timely? Is admission appropriate?

---

## Verdict format

The arbiter rules on each question:

- **Question 1:** APPROVE-AS-DRAFTED / APPROVE-WITH-RECLASSIFICATIONS (specify which) / REJECT-EXTRACTION
- **Question 2:** ADMIT / ADMIT-PROVISIONAL (specify additional remediations) / DEFER (specify findings) / REJECT
- **Question 3:** ADMIT / ADMIT-PROVISIONAL / DEFER / REJECT

If Question 1 is APPROVE (any variant), proceed to spec drafting (`conversus-oss/specs/v4.0.0-tier-extraction/spec.md`), then self-consistency verification, then blind verification per `build-fractal/conversus/GOVERNANCE.md` Part IV.

If Question 1 is REJECT, the entire build-fractal/ scaffolding remains as advisory drafts and the constitution stays at v3.2.3 single-tier.

If Question 2 or Question 3 is REJECT, that repo does not enter the suite at v4.0.0 (re-attempt later). Question 1 may still proceed independently.

## Files this deliberation reads

The agents read:
- `conversus-oss/CONSTITUTION.md` v3.2.3 — current flat constitution (canonical source)
- `build-fractal/CONSTITUTION.md` — DRAFT Tier 1 (proposed)
- `build-fractal/conversus/CONSTITUTION.md` — DRAFT Tier 2 (proposed)
- `build-fractal/conversus/GOVERNANCE.md` — deliberation philosophy + procedure
- `build-fractal/conversus/COMPLIANCE.md` — compliance contract
- `conversus-oss/CONFORMANCE.md` — DRAFT admission for OSS engine
- `conversus/CONFORMANCE.md` — DRAFT admission for paid layer

## Out of scope

This originating deliberation does NOT:
- Draft the actual amendment text (that's a downstream spec).
- Run self-consistency verification (separate deliberation per spec 067).
- Run blind verification (separate deliberation per spec 067).
- Decide Phase C submodule path migration (deferred per the build-fractal plan).

If the originating deliberation passes, the next step is drafting `conversus-oss/specs/v4.0.0-tier-extraction/spec.md` with the verbatim amendment text, then running both verifications before any constitution edits land.
