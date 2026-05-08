# Blind Verification — Tier Extraction Amendment

**Deliberation type:** Blind verification (per spec 067 §4 Leg 2 and GOVERNANCE.md Part IV).
**Markers:** STRIPPED via `scripts/strip-constitution-for-blind.py` recipe applied to the spec at `blind-inputs/spec-stripped.md`. Status markers removed; ratification-state signals removed; verbatim "PASSED WITH FIXES" / "v2 fix ledger" / dated references redacted to "(date redacted)".
**Acceptance bar:** 0 ACCEPT-level findings on **new content specifically**. Pre-existing flaws in source documents (`../CONSTITUTION.md` v3.2.3) DEFER to their own follow-on amendment cycle.

## What is being verified

A proposed structural amendment to the constitution at `../CONSTITUTION.md` (currently version 3.2.3). The amendment relocates 20 of 26 active principles to two newly-created higher-tier documents:

- 10 principles → `../../build-fractal/CONSTITUTION.md` (Tier 1 — Universal: I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII).
- 10 principles → `../../build-fractal/conversus/CONSTITUTION.md` (Tier 2 — Suite: V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII).
- 6 principles retained at component tier in `../CONSTITUTION.md` (XVII, XVIII, XIX, XX, XXI, XXVI).
- 2 retired principles (VI, X) keep their tombstone markers in `../CONSTITUTION.md` per Principle II number-stability.

The proposal text is at `blind-inputs/spec-stripped.md`. Read that as the primary subject of the deliberation.

## What this deliberation must check

The agents and arbiter MUST evaluate the spec without anchoring on any "approved" or "verified" framing. Treat the spec as a fresh proposal under contested review. Specifically:

1. **Should the tier classification (10/10/6) actually hold?** Would a strict reviewer accept that all 10 "Universal" principles really apply universally? Are any of them suite-specific masquerading as universal? Same question for Tier 2 — are any actually component-specific?

2. **Verbatim preservation contract — is "byte-for-byte identical" actually achievable?** The spec claims principles can be relocated byte-equal modulo only documented cross-reference rewrites. Read 2-3 principles in `../CONSTITUTION.md` and trace what relocation would need to preserve. Does the contract hold? Are there normative interactions between principles that the contract overlooks?

3. **Is the tier-coherence linter (spec §6.8) actually sufficient for Constitutional Inclusion Criterion 1?** The Criterion requires mechanical verification capability. The linter's algorithm is "header + first-paragraph substring match with normalization." Would this catch a real cross-tier duplication? Would it produce false positives that block legitimate amendments?

4. **Does the dependency chain (§10) actually prevent inconsistent intermediate states?** The spec claims monolithic atomicity. Is the atomicity verification described actually enforceable? What invariants would a partial application violate?

5. **Cross-section consistency.** Does the spec internally agree with itself? E.g., §5 says one preservation standard; §7 (concrete check) and §6.8 (linter) should enforce the same standard. Is there drift?

6. **What does the spec NOT say** that a strict reviewer would expect? Missing topics that would block ratification?

## Files this deliberation reads

(Limited to 5 to keep arbiter prompt assembly under cap)

- `blind-inputs/spec-stripped.md` — the proposed amendment (blind)
- `../CONSTITUTION.md` v3.2.3 — current constitution (source of relocations; not stripped because it's not being verified, only consulted as the pre-amendment state)
- `../../build-fractal/CONSTITUTION.md` — DRAFT Tier 1 (currently a 2-column summary; the spec describes how it'll be filled in)
- `../../build-fractal/conversus/CONSTITUTION.md` — DRAFT Tier 2 (same)
- `QUESTION.md` — this file

## Verdict format

The arbiter rules:
- **PASS** — 0 ACCEPT-level findings on new content. The spec ratifies as-is at v4.0.0.
- **PASS WITH FIXES** — ACCEPT findings exist but are addressable in a v3 spec revision. Specify the fixes.
- **FAIL** — fundamental issues. Spec must be substantially redrafted; ratification deferred.
- **OVERRIDE-WITH-RATIONALE** — only if the blind judge's standard, applied uniformly, would shrink existing ratified principles in `../CONSTITUTION.md`. The override must be logged in three places per `feedback_amendment_override_precedent` precedent.

ACKNOWLEDGE-level findings (issues raised but not blocking) and DEFER-level findings (issues for follow-on amendments) are non-blocking and listed for the record.

## Out of scope

- Pre-existing flaws in `../CONSTITUTION.md` v3.2.3 surfaced incidentally — those DEFER to their own follow-on amendment cycle per spec 067 § override-with-rationale boundary.
- Implementation details that the spec correctly defers to the impl-PR stage.
- The build-fractal/CONSTITUTION.md and build-fractal/conversus/CONSTITUTION.md DRAFT documents themselves — they're advisory until the amendment ratifies; their final content is described BY the spec, not BY their current draft text.
