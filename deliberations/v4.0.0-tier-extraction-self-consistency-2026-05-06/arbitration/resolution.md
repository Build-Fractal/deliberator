# v4.0.0 Self-Consistency Verification — Manual Arbitration

**Status:** Manual arbitration performed because the engine's auto-arbitrator crashed at dispatch (1ms, suspected prompt-size overflow — assembled prompts in synthesis hit 231K chars; arbitration would have been larger). Phases 1-5 (review, cross-review, revision, disputes, synthesis) all completed successfully; only the final binding-verdict step failed.

**Recovered from:** synthesis at `summary/final.md`, three dispute documents, three revision documents, and three review documents — all on disk. Manual arbitration grounded in `conversus-oss/CONSTITUTION.md` v3.2.3 per spec 067 § balanced-arbiter requirements.

---

## Decision framework

Per CONSTITUTION.md § Governance:
- **Constitutional Inclusion Criteria** (Criterion 1: mechanical verification capability) — applies to the v4.0.0 amendment's structural integrity itself.
- **Principle II — Stable Interfaces** — cross-reference patterns are stable interfaces; their documentation must be complete enough that consumers (impl-PR reviewers, future amendments) don't have to infer.
- **Principle XI — Single Source of Truth** — the verbatim preservation contract has one canonical wording; contradictory phrasings between §5 and §7 violate XI.
- **Principle XIV — Spec-Implementation Parity** — the spec must specify what implementation is being committed to. Underspecification is parity drift.
- **Spec 067 § verification methodology** — self-consistency leg catches wording drift, internal contradictions, broken cross-references in proposed amended text.

## Binding decisions

### Dispute 1 — Linter Algorithm Scope and Implementation Details

**Positions:**
- structural-integrity: implementation details (file paths, validation rules) AND precise algorithm.
- mechanical-verifiability: exact substring match of header + first paragraph with normalization rules.
- wording-precision: full-body-text matching for comprehensive duplication detection.

**Synthesizer assessment:** all three aspects are necessary for complete linter specification — algorithm precision, implementation context, and sufficient scope.

**Ruling:** ADOPT synthesizer's combined resolution.

**Grounding:** Constitutional Inclusion Criterion 1 requires mechanical verification capability. The criterion is satisfied by ANY working algorithm. However, Principle XIV (Spec-Implementation Parity) requires the spec to specify the algorithm precisely enough that a reviewer can sketch the check in one paragraph (per Inclusion Criterion language). Without all three layers — algorithm, scope, implementation details — the spec leaves implementation under-specified.

**Required fix (ACCEPT-level):** Spec §6.8 must specify:
- Algorithm: exact substring match of `### {Roman}. {Name}` header line + the first paragraph following it (post-normalization).
- Normalization: collapse multiple whitespace runs to single spaces; strip leading/trailing whitespace per line.
- Scope rationale: "header + first paragraph is sufficient because principle bodies vary heavily in length but their headers and opening paragraphs are stable identification surfaces; comprehensive duplication of a relocated principle would inevitably duplicate the header and at least the opening sentence."
- File paths: `conversus-oss/CONSTITUTION.md`, `build-fractal/CONSTITUTION.md`, `build-fractal/conversus/CONSTITUTION.md`.
- CI integration: invoked from `linter/validate.py`'s existing entry point.

**Rejected position:** wording-precision's full-body-text matching is overkill — it would produce false positives on shared boilerplate (Origin attributions, Extension blocks). Header + first paragraph is the minimum sufficient detection surface.

### Dispute 2 — Cross-Reference Documentation Completeness vs Implementation-Time Validation

**Positions:**
- wording-precision: documentation completeness must precede mechanical validation; spec only documents 2 of 6 possible tier reference patterns.
- mechanical-verifiability + structural-integrity: implementation-time mechanical validation suffices; exhaustive matrices are overkill.

**Synthesizer assessment:** both address real failure modes; evidence supports wording-precision that at least the patterns actually used in the constitution must be documented.

**Ruling:** ADOPT synthesizer's resolution — document patterns that actually appear; mechanical validation as complement.

**Grounding:** Principle II (Stable Interfaces) — cross-reference syntax is a stable interface in the relocated principles. Without complete documentation of the patterns in use, a future amendment author re-relocating a principle has no canonical guide. Principle XI (Single Source of Truth) — the documentation IS the canonical reference; mechanical validation enforces it but doesn't substitute for it.

**Required fix (ACCEPT-level):** Spec §5 must enumerate the cross-reference patterns that appear in the current constitution. Minimum:
- Tier 2 → Tier 1: `../CONSTITUTION.md` (relative reach from `build-fractal/conversus/` to `build-fractal/`).
- Component → Tier 1: `../build-fractal/CONSTITUTION.md` (relative reach from `conversus-oss/` to `build-fractal/`).
- Component → Tier 2: `../build-fractal/conversus/CONSTITUTION.md`.
- Tier 1 → Tier 2: `conversus/CONSTITUTION.md` (relative reach from `build-fractal/` to `build-fractal/conversus/`).
- Plus any backward references actually in current text.

**Mechanical validation:** the tier-coherence linter (§6.8) extends to parse Markdown links in relocated principles and verify each target resolves to an existing file. Documented as "cross-reference resolution validation" within §6.8's scope.

**Rejected position:** "exhaustive matrices" was a strawman — the requirement is patterns-that-actually-appear, not all-theoretically-possible.

### Dispute 3 — Priority Classification for Preservation Language vs Algorithm Specification

**Positions:**
- wording-precision: language unification is highest P1 (load-bearing for verbatim preservation commitment).
- mechanical-verifiability: algorithm specification is highest P1 (without enforcement, language fails Criterion 1).

**Synthesizer assessment:** both genuinely P1; treat as co-equal with explicit sequencing.

**Ruling:** ADOPT synthesizer's resolution — both P1, with explicit dependency ordering (language unification → algorithm specification → automation).

**Grounding:** Principle XI (Single Source of Truth) — contradictory language in §5 ("every word ... is preserved") vs §7 ("byte-equal content") violates XI by creating two competing authoritative phrasings of the same standard. Principle XIV — automated verification built on contradictory standards would institutionalize the wrong rule. Inclusion Criterion 1 — without algorithm spec, mechanical verification fails. Both genuinely block.

**Required fix (ACCEPT-level):** Spec §5 and §7 must use a unified preservation phrasing — pick one (e.g., "byte-for-byte identical content of the principle's normative text"), apply consistently. §10 (Implementation order) must explicitly sequence: language unification → algorithm specification (§6.8 detail) → linter implementation. The dependency is bidirectional — language can't be enforced without algorithm; algorithm can't be correct without language.

## Combined ACCEPT-level fixes (the verdict's required-changes block)

The following 7 fixes are required before blind verification proceeds. Each is grounded in a specific principle and addresses a specific gap surfaced by the deliberation.

| # | Fix | Spec section | Grounding |
|---|---|---|---|
| 1 | Unify preservation contract language: replace "every word ... preserved" with "byte-for-byte identical content" (or equivalent unified phrase) consistently across §5 and §7 | §5, §7 | XI (SSoT) |
| 2 | Specify tier-coherence linter algorithm: header + first-paragraph substring match with whitespace normalization, plus the implementation-detail scope (file paths, CI integration) | §6.8 | Inclusion Criterion 1, XIV |
| 3 | Add explicit SIR audit trail preservation: §6.3 and §11 must require all existing SIR comment blocks (v3.2.2, v3.2.1, v3.2.0, v3.0.0, v2.x...) be preserved as comment blocks below the v4.0.0 SIR | §6.3, §11 | Existing pattern in CONSTITUTION.md (governance integrity) |
| 4 | Add file-edit dependency ordering with atomicity: §10 must specify constitution-file updates before governance-log updates, plus all-or-nothing impl-PR commitment | §10 | XI (consistent state across files) |
| 5 | Implement multi-layer cross-reference validation: §6.8 extended to include cross-reference resolution validation alongside duplication detection | §6.8 | II (Stable Interfaces) |
| 6 | Sequence language unification before automation: §10 must enumerate the dependency (language → algorithm → automation) | §10 | XIV |
| 7 | Document cross-reference patterns: §5 must enumerate the 4-5 patterns that actually appear in the current constitution | §5 | II |

ACKNOWLEDGE-level findings (non-blocking, listed for record): items 7-16 from synthesis Actionable Spec Changes (P2/P3) — bundled accuracy fixes, verbatim preservation automation (SHA-256 hashes), backward cross-reference handling, etc. These can be incorporated into the v2 spec opportunistically but do not block blind verification.

DEFER-level findings (out of v4.0.0 scope): pre-existing flaws in `conversus-oss/CONSTITUTION.md` itself surfaced incidentally are out of self-consistency-leg scope. The blind verification leg may surface them; if so, they go to their own follow-on amendment cycle.

## Verdict

**SELF-CONSISTENCY VERDICT: PASS WITH FIXES — apply 7 fixes, then proceed to blind verification.**

The spec's structural core (tier classification 10/10/6, verbatim preservation principle, file-edit enumeration, conditions discharge) is sound. The 7 fixes refine underspecified sections (linter algorithm, cross-reference patterns, SIR preservation, dependency ordering, language unification) without altering the substantive amendment.

Blind verification (Leg 2) runs against spec v2 (post-fixes), not against this v1.

## Process notes

- **Engine arbitration crash:** the auto-arbitrator failed at dispatch in 1ms; suspected cause is prompt-size overflow (synthesis prompt was 231K chars). This is a real engine bug — phases 1-5 ran cleanly; the engine should chunk/summarize when arbitration prompt size exceeds claude-code's effective context budget rather than failing silently. Logged as a follow-on issue for conversus-oss engine work, separate from this amendment.
- **Manual arbitration faithfulness:** this manual ruling is grounded in the same constitution v3.2.3 the auto-arbitrator would have read, applies the same balanced-arbiter standard (per spec 067), and integrates the synthesizer's resolutions exactly per their stated rationales. The manual step does not introduce ratification bias — the rulings on each dispute follow the synthesizer's recommended resolutions, which were produced from the deliberation's actual content.
- **Originating deliberation precedent:** the originating deliberation's auto-arbitrator succeeded at 154,855ms processing time. This deliberation's synthesis produced larger artifacts (3 dispute docs, 6 cross-reviews, more detailed convergence analysis) — likely the trigger for the prompt-size threshold breach.
