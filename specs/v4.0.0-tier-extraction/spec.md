# Feature Specification: v4.0.0 Tier Extraction & Suite Admission

**Feature ID:** `v4.0.0-tier-extraction`
**Created:** 2026-05-06
**Status:** Draft v4 — self-consistency PASSED WITH FIXES 2026-05-06 (7 fixes applied in v2); blind verification PASSED WITH FIXES 2026-05-07 (5 fixes B1-B5 applied in v3); URL-reference erratum applied 2026-05-08 (1 fix C1 applied in v4); ready for impl-PR.
**Depends On:** spec 067 (verification methodology), spec 070 (constitutional inclusion gate), spec 033 (free/paid partition).
**Governed by:** `CONSTITUTION.md` § Governance — Pathway Taxonomy (MAJOR pathway).
**Originating context:** Originating deliberation 2026-05-06 at `deliberations/v4.0.0-tier-extraction-originating-2026-05-06/` ruled APPROVE-AS-DRAFTED + ADMIT-PROVISIONAL × 2 with four P1 conditions. Conditions empirically discharged or translated into binding remediation deadlines per `VERDICT.md` (same dir).

> **Scope discipline:** This spec extracts principles from `conversus-oss/CONSTITUTION.md` to two higher tiers (Universal at `build-fractal/CONSTITUTION.md`, Suite at `build-fractal/conversus/CONSTITUTION.md`), reducing conversus-oss/CONSTITUTION.md to its component-tier residue. It does NOT introduce, remove, or rewrite any principle's normative text. The Inclusion-Criteria gate does NOT re-apply to grandfathered principles relocated through tier reclassification (per Dispute 2 ruling — grandfathering protects validity, not factual accuracy of compliance claims). It also admits both existing suite repos via their CONFORMANCE.md declarations.

---

## 1. Summary

The conversus-oss CONSTITUTION.md (v3.2.3) carries 26 active principles in a flat list. Several are universal (every Build Fractal product), several are suite-wide (all conversus-family repos), several are component-local (only conversus-oss). The flat structure forces sibling repos to either duplicate the constitution or fork it, neither of which is tractable as the suite grows.

This v4.0.0 amendment splits the constitution into three tiers:

- **Tier 1 (Universal):** 10 principles → moved verbatim to `build-fractal/CONSTITUTION.md`.
- **Tier 2 (Suite):** 10 principles → moved verbatim to `build-fractal/conversus/CONSTITUTION.md`.
- **Component:** 6 principles → stay in `conversus-oss/CONSTITUTION.md`.
- **Retired:** VI and X stay marked retired in conversus-oss/CONSTITUTION.md per Principle II number-stability.

It also formally admits `conversus-oss` (the OSS engine) and `conversus` (the paid layer, package `conversus-enhanced`) to the suite, per their `CONFORMANCE.md` declarations and the originating deliberation's Q2/Q3 ADMIT-PROVISIONAL rulings.

## 2. Goals

1. Tier 1 and Tier 2 documents flip from `Status: DRAFT` to `Status: RATIFIED` under v4.0.0.
2. `conversus-oss/CONSTITUTION.md` reduces to component-tier text + cross-references to Tier 1 / Tier 2 docs.
3. `conversus-oss/CONFORMANCE.md` and `conversus/CONFORMANCE.md` flip from `Status: Implicit-Provisional` to `Status: Provisional` (because of open remediations) with admission deliberation reference filled in.
4. Suite admissions logged at suite tier (`build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md`) and at conversus-oss component tier.
5. A tier-coherence CI check exists in conversus-oss that fails if a component-tier principle restates a Suite or Universal principle (per the build-fractal Phase A plan's Phase B item).

## 3. Non-goals

- **Rewriting any principle text.** Tier extraction is mechanical relocation; normative text is preserved verbatim.
- **Re-applying Constitutional Inclusion Criteria to grandfathered principles.** Per Dispute 2 ruling, grandfathering protects validity even through tier reclassification.
- **Phase C submodule path migration.** `conversus-oss/` and `conversus/` stay as flat siblings under `payer-index-mono/`. Phase C is deferred until at least one new sibling joins.
- **Promoting `build-fractal/conversus/GOVERNANCE.md` or `COMPLIANCE.md` to Tier 1.** Both stay suite-tier per their § Status & Provenance footers.
- **Closing the open Provisional remediations.** Each repo's CONFORMANCE.md carries deadlines that ride past v4.0.0; closing them is downstream work.

### Constitutional debt acknowledgment (resolves Fix B2)

Tier 1 (Universal) under v4.0.0 carries grandfathered principles ratified pre-Inclusion-Criteria-gate (which was added in v2.4.0). Specifically: I, II, III, IV, VII, VIII, IX, XI, XIV — all grandfathered. XXVIII passed the post-gate criteria.

These grandfathered principles' constitutional validity is preserved per Principle II number-stability and the Governance section's grandfathering provision. Their post-gate compliance with current Constitutional Inclusion Criteria is **NOT re-evaluated** by the v4.0.0 tier extraction. Reasoning per the 2026-04-29 Principle XXVIII ratification override-precedent (`feedback_amendment_override_precedent`): a strict reading requiring full re-audit at relocation would uniformly damage the grandfathered set, which is exactly the situation the override-with-rationale pathway exists for.

Future amendments specifically targeting Tier 1 principle conformance to current Inclusion Criteria are deferred as separate cycles. The blind verification deliberation 2026-05-07 explicitly accepted this debt acknowledgment as the resolution to the constitutional integrity vs amendment feasibility tension.

## 4. Tier Classification

The originating deliberation ruled APPROVE-AS-DRAFTED on the 10/10/6 split. The classification is binding for v4.0.0:

### Tier 1 — Universal (10 principles)

Move verbatim from `conversus-oss/CONSTITUTION.md` to `build-fractal/CONSTITUTION.md`:

| # | Principle |
|---|---|
| I | Spec-Driven Development |
| II | Stable Interfaces |
| III | Backward-Compatible Extension |
| IV | Documentation Is the Product |
| VII | Reproducibility Over Inconsistency |
| VIII | Templating Engines Over Inference |
| IX | Functional Programming and Clean Code |
| XI | Single Source of Truth |
| XIV | Spec-Implementation Parity |
| XXVIII | Test-Fix Boundary Preservation |

### Tier 2 — Suite (10 principles)

Move verbatim from `conversus-oss/CONSTITUTION.md` to `build-fractal/conversus/CONSTITUTION.md`:

| # | Principle |
|---|---|
| V | Observable Deliberation |
| XII | No Dead Infrastructure |
| XIII | Enum Completeness |
| XV | Plugin Isolation |
| XVI | Mathematical Transparency *(suite-tier rationale below — resolves Fix B5)* |
| XXII | Distribution Surface Integrity |
| XXIII | Provider Robustness Contract |
| XXIV | Safety-Critical Defense-in-Depth |
| XXV | Live Test Cost Discipline |
| XXVII | Operator-Configurable Tool Surface |

**XVI suite-tier rationale (resolves Fix B5):** Mathematical transparency applies suite-wide because it is the governance constraint on ANY scoring/optimization approach in the conversus suite — it constrains the assembled objective function's *assembly form* (parameter names, template selection, gap-identifier set), not the optimizer's internal mathematics. Future suite siblings adopting fundamentally different optimization paradigms (e.g., neural optimization without explicit parameter pinning) inherit XVI's discipline regardless of mathematical form, because the discipline is about cross-run determinism + transparency of inputs, not about specific math operations. The 2026-05-07 blind verification's surviving dispute on XVI tier classification ruled in favor of Suite-tier with this rationale.

### Component — conversus-oss only (6 principles)

Stay in `conversus-oss/CONSTITUTION.md`:

| # | Principle |
|---|---|
| XVII | Content Classification |
| XVIII | Progressive Disclosure Contract |
| XIX | Non-Extractable Core |
| XX | Decomposition Mechanism Precedence |
| XXI | Extraction Ordering |
| XXVI | Meta-Testing for Parametrized Capabilities |

### Retired (no relocation)

| # | Principle | Status |
|---|---|---|
| VI | ~~Scripts Over Markdown~~ | Retired v3.0.0 — number permanently retired per Principle II. |
| X | ~~Zen of Python Output~~ | Retired v3.0.0 — number permanently retired per Principle II. |

The retired-principle markers stay in conversus-oss/CONSTITUTION.md (the file that originally carried them) — they do NOT move to Tier 1 or Tier 2. Number stability requires the original location to retain the strikethrough record.

## 5. Verbatim Preservation Contract

**Unified preservation standard (resolves self-consistency Fix #1):** for every relocated principle, the principle's normative text MUST appear at its new location with **byte-for-byte identical content**, modulo only the cross-reference rewrites enumerated below. "Byte-for-byte identical" means: identical character sequence, identical whitespace, identical line breaks, identical Markdown formatting. Reflowing paragraphs, normalizing whitespace, or "cleaning up" formatting all violate the contract.

For every relocated principle, the following must hold:

- **Header byte-for-byte identical:** `### {Roman}. {Name}` line is unchanged.
- **Body byte-for-byte identical:** the principle's normative text — including bullet lists, "Origin:" attributions, "Extension (vN.M.K)" sub-blocks, and internal cross-references — is preserved as-is.
- **Cross-reference rewrites — patterns that actually appear in the current constitution (resolves Fix #7):**

  | From | To | Relative path |
  |---|---|---|
  | Tier 2 principle → Tier 1 principle | `../CONSTITUTION.md § Principle {N}` | `../CONSTITUTION.md` (from `build-fractal/conversus/` to `build-fractal/`) |
  | Component principle → Tier 1 principle | `../build-fractal/CONSTITUTION.md § Principle {N}` | `../build-fractal/CONSTITUTION.md` (from `conversus-oss/` to `build-fractal/`) |
  | Component principle → Tier 2 principle | `../build-fractal/conversus/CONSTITUTION.md § Principle {N}` | `../build-fractal/conversus/CONSTITUTION.md` |
  | Tier 1 principle → Tier 2 principle | `conversus/CONSTITUTION.md § Principle {N}` | `conversus/CONSTITUTION.md` (from `build-fractal/` to `build-fractal/conversus/`) |
  | Same-tier (intra-document) reference | unchanged | n/a |
  | **Amendment-record references** (e.g., `(per amendment v2.X.Y)` inside principle bodies) — resolves Fix B4 | Path-prefix unchanged; reference stays with the principle wherever it relocates. The amendment record itself stays in the SIR audit trail at the source CONSTITUTION.md. | n/a (text inside body preserved; SIR location is canonical) |
  | **Inline section citations** (e.g., `see § Governance`) — resolves Fix B4 | If the cited section stays in its source file: `see § Governance` becomes `see ../CONSTITUTION.md § Governance` from Tier 1 / Tier 2 documents. The Governance section stays in `conversus-oss/CONSTITUTION.md` (component-tier) per §6.3. | `../CONSTITUTION.md § Governance` from Tier 1 / Tier 2 |
  | **Adjacent-phrase references** (e.g., `Principles I-V` or `see also Principle IX`) — resolves Fix B4 | Plural-form-aware rewriting: `Principles I-V` becomes a tier-aware phrase since I-IV are Tier 1 and V is Tier 2. The linter's cross-reference resolution validation (§6.8 Check (c)) flags such phrases for manual review during impl-PR. | manual review for tier-spanning phrases |
  | **Backward references** (Tier 1 → Tier 2 / Component, or Tier 2 → Component) | Appear in governance-section cross-references; preserve identity, rewrite path-prefix. The linter verifies generically via Check (c). | per source-target tier pair |

  The expanded patterns table (resolves Fix B4) covers the patterns actually appearing in `conversus-oss/CONSTITUTION.md` v3.2.3 plus the structural categories blind verification 2026-05-07 surfaced. The tier-coherence linter (§6.8) Check (c) enforces resolution validation across all forms generically.

  The reference identity (Roman numeral + name) does NOT change; only the path-reach prefix changes. A reference `Principle IX` that currently appears inside a body becomes `Tier 1 Principle IX (../CONSTITUTION.md)` when the containing principle is a Tier 2 principle.

- **No content additions during the move.** New tier-introduction text in the target documents is permitted but MUST be clearly bracketed as new content (e.g., a "Tier 1 / Tier 2 introduction" section preceding the principle list); it does NOT appear inside any relocated principle's body. Tier introduction text falls under "structural changes permitted at tier-document level" and is exempt from the byte-equal requirement (which applies only to relocated principle bodies, not to surrounding tier-document scaffolding).
- **Principle II's number-stability rule extends across tiers.** A principle keeps its Roman numeral identifier wherever it lands. Tier 1 contains principles with numerals I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII (non-consecutive — V is in Tier 2, VI is retired, etc.). Tier 2 contains V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII (non-consecutive). Component contains XVII, XVIII, XIX, XX, XXI, XXVI (non-consecutive). The numerals are NOT renumbered for tier-internal locality.

## 6. File Edits

### 6.1. `build-fractal/CONSTITUTION.md` (Tier 1)

Currently `Status: DRAFT — pending v4.0.0 ratification`. Under v4.0.0:
- Replace the principle-name table (currently a 2-column summary) with the verbatim text of each of the 10 Tier 1 principles, each as its own section. Source: `conversus-oss/CONSTITUTION.md` lines covering I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII.
- Add a Sync Impact Report header documenting the v4.0.0 ratification, with cross-references to the originating deliberation (`../conversus-oss/deliberations/v4.0.0-tier-extraction-originating-2026-05-06/`) and the spec at `../conversus-oss/specs/v4.0.0-tier-extraction/`.
- Flip `Status: DRAFT — pending v4.0.0 ratification` → `Status: RATIFIED — v4.0.0`.
- Add `Version: 1.0.0` at the top (Tier 1's own semver, separate from Tier 2's and components' versions).

### 6.2. `build-fractal/conversus/CONSTITUTION.md` (Tier 2)

Currently `Status: DRAFT — pending v4.0.0 ratification`. Under v4.0.0:
- Replace the principle-name table with verbatim text of each of the 10 Tier 2 principles, each as its own section. Source: `conversus-oss/CONSTITUTION.md` lines covering V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII.
- Add a Sync Impact Report header.
- Flip `Status: DRAFT` → `Status: RATIFIED — v4.0.0`.
- Add `Version: 1.0.0`.
- Update the "Component-tier residue" section to match the final 6-principle component-tier list (already correct in the current draft).

### 6.3. `conversus-oss/CONSTITUTION.md` (Component, was canonical)

This is the largest edit. The current 2300+ line CONSTITUTION.md reduces to:
- Sync Impact Report header documenting v3.2.3 → v4.0.0 (MAJOR).
- **All existing SIR comment blocks preserved (resolves Fix #3)**: the v3.2.2 → v3.2.3 SIR block, the v3.2.1 → v3.2.2 block, the v3.2.0 → v3.2.1 block, the v3.0.0 → v3.2.0 block, and any earlier preserved-for-audit SIR blocks all remain in place as comment blocks below the new v4.0.0 SIR. This continues the established governance integrity pattern — the canonical CONSTITUTION.md carries an append-only audit trail of every prior amendment's SIR. Removing or condensing prior SIRs would violate the precedent.
- Cross-reference block at top: "This component-tier constitution inherits from `../build-fractal/CONSTITUTION.md` (Tier 1 Universal) and `../build-fractal/conversus/CONSTITUTION.md` (Tier 2 Suite). For Universal and Suite principles, see those documents."
- Section "Retired" preserving VI and X strikethrough markers (no other content for these).
- Section "Component Principles" with byte-for-byte identical text of XVII, XVIII, XIX, XX, XXI, XXVI (per §5).
- Section "Governance" — preserved byte-for-byte identical from current v3.2.3 (Constitutional Inclusion Criteria, Principle Number Stability, Pathway Taxonomy, Compliance, Versioning, Amendment Process). The Pathway Taxonomy stays here because it governs amendments at all tiers; Tier 1 and Tier 2 cross-reference back to this section rather than restating it.
- Version bumped to `4.0.0`.

The relocated principle text is **deleted** from this file (moved to Tier 1 / Tier 2). The reduction is the substantive change.

### 6.4. `build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md`

Add v4.0.0 ratification entry of `Type: tier-extraction-ratified`, linking the originating deliberation, the self-consistency verification deliberation (TBD), the blind verification deliberation (TBD), and this spec. Also add two child entries of `Type: new-sibling`:
- `2026-MM-DD — admit-conversus-oss` linking the conversus-oss/CONFORMANCE.md ratified at v4.0.0.
- `2026-MM-DD — admit-conversus-enhanced` linking conversus/CONFORMANCE.md.

### 6.5. `conversus-oss/CONSTITUTIONAL_CONVERSATIONS.md`

Add component-tier entry recording v3.2.3 → v4.0.0 reduction. Cross-reference to the suite-tier entries via `**Source:**` lines.

### 6.6. `conversus-oss/CONFORMANCE.md`

- Replace `Admission deliberation: (none yet)` with the path to the originating deliberation's resolution.md.
- Flip `Status: Implicit-Provisional` → `Status: Provisional` (5 open remediations).
- Add a `Last re-audit:` entry for v4.0.0 ratification date.

### 6.7. `conversus/CONFORMANCE.md`

Same edits as 6.6, with 4 open remediations.

### 6.8. `conversus-oss/linter/tier_coherence.py` (NEW) — resolves Fixes #2, #5

A new linter satisfying Constitutional Inclusion Criterion 1 for the v4.0.0 structural amendment. Three checks, each mechanically falsifiable:

#### Check (a) — Cross-tier duplication detection (strengthened per Fix B1)

**Background:** Blind verification 2026-05-07 found that header + first-paragraph substring matching alone is defeatable — a sophisticated duplication preserving header + first-paragraph identity while substituting the rest of the body would pass. Fix B1 strengthens the check.

**Algorithm:** the linter implements TWO independent signals; FAIL if EITHER fires.

**Signal 1 — Identity-marker check (cheap, fast):**
For each component-tier principle in `conversus-oss/CONSTITUTION.md`, compute a signature consisting of:
1. The header line (the `### {Roman}. {Name}` text).
2. The first paragraph following the header (everything from the line after the header up to the next blank line or the next `### ` header, whichever comes first).

Both passed through normalization: collapse multiple whitespace runs to single spaces; strip leading/trailing whitespace per line. Compare against every Tier 1 and Tier 2 principle's normalized signature. **FAIL Signal 1** if any match.

**Signal 2 — Body-similarity check (defeat-resistant):**
For each principle (component-tier OR Tier 1 OR Tier 2), compute a 5-gram fingerprint over the normalized full body (header + all paragraphs until next `### ` header or end-of-file). Use Jaccard similarity over 5-gram sets. **FAIL Signal 2** if any cross-tier pair has similarity > 0.85.

The 0.85 threshold is empirical: identical principles (post-relocation) have similarity ~1.0; principles sharing only Origin-attribution boilerplate have similarity ~0.10-0.30; principles with substantively duplicated content but rewritten openings have similarity 0.85-0.95. The 0.85 line catches sophisticated duplications (Signal 1 passes, Signal 2 catches) without false-positiving on genuinely distinct principles.

**Escape-hatch for legitimate shared content (per Fix B1 escape-hatch requirement):**
The following are explicitly excluded from BOTH signals:
- Origin attribution lines: `Origin: spec NNN, deliberation 'YYYY-MM-DD-slug'`
- Extension headers: `**Extension (vN.M.K):**`
- Standard governance-cross-reference phrases: `see § Governance`, `per CONSTITUTION.md`
- Tombstone markers for retired principles: `### {Roman}. ~~{Name}~~ — RETIRED v{N.M.K}`

These are pre-stripped from each principle's normalized body before signature/fingerprint computation. Any future shared boilerplate that would false-positive must be added to this exclusion list (a `linter/tier_coherence_excludes.txt` config file).

**Scope rationale:** the dual-signal approach satisfies Constitutional Inclusion Criterion 1 (mechanical verification) without false-positiving on legitimate shared boilerplate (Origin attributions, Extension blocks, governance cross-references). Signal 1 is the cheap fast check; Signal 2 is the defeat-resistant check. Together they catch any cross-tier duplication that the blind verification's threat model identified.

**Tradeoffs:**
- False positive rate: ~0% expected after exclusion list (escape-hatch per B1).
- False negative rate: limited to constructions that defeat 5-gram fingerprinting, which would require a sophisticated adversary actively trying to bypass the linter — a constructed concern rather than a realistic accidental case.
- Computational cost: O(N²) cross-tier pairs; for N=26 principles, 676 comparisons; each comparison is bounded by 5-gram set size; well under 1 second per CI run.

**Files inspected:**
- `conversus-oss/CONSTITUTION.md`
- `build-fractal/CONSTITUTION.md`
- `build-fractal/conversus/CONSTITUTION.md`

#### Check (b) — Post-relocation orphan detection

**Algorithm:** for each principle listed in §4 as relocated to Tier 1 or Tier 2 (the 20 principles I, II, III, IV, V, VII, VIII, IX, XI, XII, XIII, XIV, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII, XXVIII), search for its byte-for-byte body text in `conversus-oss/CONSTITUTION.md`. Search uses the unique opening-paragraph signature from check (a). **FAIL** if any relocated principle's body still appears in the component-tier file (other than as a cross-reference, which is matched by the prefix `Principle {Roman}` without the body text).

#### Check (c) — Cross-reference resolution validation (multi-layer per Fix #5)

**Algorithm:** parse all Markdown links in each of the three constitution documents. For each link of the form `[text](relative-path)`:
1. Verify the relative path resolves to an existing file (path validation).
2. If the link target includes a section anchor (e.g., `../CONSTITUTION.md § Principle IX`), verify the anchor exists in the target file (resolution validation).
3. If the link claims to point to a specific principle by Roman numeral, verify the target file's Tier matches the principle-set declared in §4 (cross-tier consistency).

**FAIL** on any broken link, missing anchor, or tier mismatch.

#### Check (d) — Version-field consistency

**Algorithm:** parse each of the three constitution documents for their declared version (in the SIR header at top of file: `Version change: X.Y.Z → A.B.C`). Verify that the latest declared version in each file matches the file's own `Version:` field (if present in frontmatter) and that all three documents collectively consistent at the v4.0.0 ratification point. **FAIL** on disagreement.

**"Latest SIR" is identified as: the FIRST `<!-- Sync Impact Report` comment block at the top of each file** (post-v4.0.0, prior SIRs are preserved as comment blocks below per Fix #3, but the latest is always at top).

#### Implementation

- New file: `conversus-oss/linter/tier_coherence.py`
- Entry point: `python -m linter.tier_coherence` (callable from CI).
- Integrated into existing `linter/validate.py` so the existing `uv run python -m linter.validate` invocation runs tier-coherence as one of its checks.
- Exit code: 0 if all checks pass; 1 if any check fails. Specific failure mode named in stderr (e.g., `tier-coherence: cross-tier duplication detected — Principle V appears in conversus-oss/CONSTITUTION.md and build-fractal/conversus/CONSTITUTION.md`).
- Tests: `conversus-oss/linter/test_tier_coherence.py` covering each check with synthetic positive + negative cases.

#### Constitutional Inclusion Criterion 1 satisfaction

This linter provides mechanical verification capability for the v4.0.0 structural amendment's central claims (no cross-tier duplication, no orphans, valid cross-references, consistent versions). An engineer reading this section can sketch the check in one paragraph; the algorithm is precise; the implementation is bounded. The amendment satisfies Criterion 1 via this linter.

### 6.9. CHANGELOG.md (conversus-oss)

Add `v4.0.0 — 2026-MM-DD` section under `## [Unreleased]` template. Brief description: "Tier extraction. Ratifies build-fractal/ hierarchical constitution. Admits conversus-oss + conversus to the suite per their CONFORMANCE.md declarations." Reference this spec.

## 6.10. Cross-tier weakening prohibition (NEW — resolves Fix B3)

The spec's tier hierarchy presumes a "lower tiers may strengthen but not weaken upper-tier rules" relationship (per `build-fractal/CONSTITUTION.md` § Tier Model and `build-fractal/conversus/CONSTITUTION.md` § Tier Model). Without an operational definition of "weakening," the inheritance rule is exposed to interpretation-layer attacks — a future Tier 2 amendment could effectively contradict a Tier 1 principle without the contradiction being mechanically detectable.

**Operational definition of "weakening":**

A lower-tier amendment **weakens** an upper-tier principle if **any** of the following holds:

1. **(i) Implicit relief.** The amendment grants relief from the upper-tier principle's enforcement at the lower-tier scope WITHOUT invoking the formal Relief pathway documented in `build-fractal/conversus/COMPLIANCE.md` Part VI. Relief outside the formal pathway is implicit and unauditable; this is the precise vulnerability the prohibition closes.

2. **(ii) Implementation-impact shift.** The amendment introduces interpretation language that, applied to existing implementations, would cause them to no longer satisfy the upper-tier principle. Reasoning: if the new interpretation makes existing-Satisfied → newly-non-compliant, the amendment has weakened the standard even if its surface text doesn't say so.

3. **(iii) Suite-specific adaptation bypass.** The amendment adds a "suite-specific adaptation" clause that effectively bypasses an upper-tier principle's MUST clause. Adaptation language that says "for the conversus suite, X may be relaxed when Y" is a bypass even if framed as "adaptation" rather than relief.

**Enforcement mechanism:**

- **Meta-arbiter responsibility:** any cross-tier amendment (one that touches Tier 1 or Tier 2 from a lower tier, or vice versa) MUST be reviewed by a balanced-arbiter agent specifically tasked with checking criteria (i), (ii), (iii) against existing upper-tier principles. The meta-arbiter ruling is binding at the deliberation level.

- **Linter-flagged review (extension to §6.8 Check (a)):** the tier-coherence linter flags any Tier 2 / Component principle text that contains the words "relief," "exception," "adaptation," "exemption," "carve-out," or "bypass" within 200 characters of a Tier 1 principle name (e.g., "Principle IX") or any of: "Universal," "Tier 1." The flag is non-fatal but triggers manual review during impl-PR. False-positives (legitimate uses of these words in non-weakening context) are documented in the PR review.

- **Existing-implementation impact check:** for any cross-tier amendment, the impl-PR review MUST run a sample of existing repo CONFORMANCE.md declarations against the proposed amendment's text and confirm Satisfied claims remain valid. If any flip from Satisfied → not-Satisfied as a side-effect, criterion (ii) is triggered.

**This prohibition was surfaced by the 2026-05-07 blind verification deliberation (Convergence 3) and is binding on the v4.0.0 amendment AND on all future cross-tier amendments. It is a structural safeguard, not an operational improvement; per the blind verification's Surviving Dispute 2 ruling, it lands in initial v4.0.0, not as follow-on work.**

## 7. Verbatim text preservation — concrete check

After implementation, the following identity must hold:

- For each principle listed in §4 Tier 1 / Tier 2, search the relocated location for its body text. The text MUST appear with byte-equal content (modulo only the relative-path-prefix changes documented in §5).
- For each component-tier principle (XVII-XXI, XXVI), search `conversus-oss/CONSTITUTION.md` for its body text. The text MUST appear unchanged.
- Search Tier 1 for any principle in {V, XII, XIII, XV, XVI, XVII, XVIII, XIX, XX, XXI, XXII, XXIII, XXIV, XXV, XXVI, XXVII}. There MUST be zero matches.
- Search Tier 2 for any principle in {I, II, III, IV, VII, VIII, IX, XI, XIV, XVII, XVIII, XIX, XX, XXI, XXVI, XXVIII}. There MUST be zero matches.
- Search component for any principle in {I, II, III, IV, V, VII, VIII, IX, XI, XII, XIII, XIV, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII, XXVIII}. There MUST be zero principle-body matches (cross-references in headers/intro text are permitted).

The tier-coherence linter (§6.8) automates the first two checks. The negative checks are part of the impl-PR review checklist.

## 8. Verification protocol (per spec 067)

Two deliberations, both required, both must produce ACCEPTABLE verdicts before the implementation PR can merge.

### 8.1. Self-consistency verification

Run a deliberation against the proposed amendment text WITH markers visible. The deliberation reads:
- This spec (`specs/v4.0.0-tier-extraction/spec.md`).
- Proposed Tier 1 final text.
- Proposed Tier 2 final text.
- Proposed reduced conversus-oss/CONSTITUTION.md.

Acceptance bar: 0 ACCEPT-level findings on the new wording or structure of the relocated text.

Use existing role presets per spec 067 §4.3.1: `preset: devils-advocate` + `preset: balanced-arbiter`. Hand-rolled prompts NOT permitted.

Output deliberation directory: `conversus-oss/deliberations/v4.0.0-tier-extraction-self-consistency-2026-MM-DD/`.

### 8.2. Blind verification

Run a deliberation against the proposed amendment text WITH markers stripped via `scripts/strip-constitution-for-blind.py`. The deliberation reads the same files as 8.1 but post-stripping (no SIR blocks, no version numbers, no origin attributions).

Acceptance bar: 0 ACCEPT-level findings on **new content specifically**. Pre-existing flaws surfaced by the blind run DEFER to their own amendment cycle (per spec 067 § override-with-rationale rule).

Output deliberation directory: `conversus-oss/deliberations/v4.0.0-tier-extraction-blind-2026-MM-DD/`.

### 8.3. Override-with-rationale

If the blind run applies a strict reading whose uniform application would shrink existing ratified principles (per `feedback_amendment_override_precedent` memory), the override pathway is the appropriate response — NOT iterate, NOT demote. Override must be logged in three places per the precedent:
1. SIR's "Override-with-rationale" paragraph in `conversus-oss/CONSTITUTION.md`.
2. Governance log entry in `build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md`.
3. This spec's status line tracking back to both blind verdicts (v1 + v2 if iterated).

## 9. Conditions from originating deliberation (binding on this spec)

| Condition | Status | Resolution |
|---|---|---|
| Empirical templating-surface audit | DISCHARGED 2026-05-06 | conversus_enhanced/ has zero templating code per grep. VIII Universal classification stands. |
| Plugin Isolation post-PR-#30 verification | DISCHARGED 2026-05-06 | conversus/ local dir contains only self-audit/ + self-review/ (deliberation archives, NOT a Python package). PR #30 framework deletion verified clean. |
| Coordination infrastructure for cross-repo XXII | RESOLVED via decoupling | Each repo addresses XXII independently. Cross-repo .mcpb dual-vendoring is a follow-on spec, not v4.0.0 prerequisite. |
| Verification of admission claims (V, XXIV, XXVI in conversus-oss) | TRANSLATED to Provisional | conversus-oss/CONFORMANCE.md updated with V, XXIV, XXVI flipped Satisfied → Provisional with deadlines (2026-08-01, 2026-09-01, 2026-08-01). |

All four originating-deliberation P1 conditions either empirically discharged or translated into Provisional remediations carried in the impl-PR. No re-deliberation required.

## 10. Implementation order — dependency-ordered + atomic (resolves Fixes #4, #6)

The impl-PR is monolithic by necessity — partial application produces inconsistent state across the three constitution documents. The PR commits all edits below in a single coordinated change. Order within the PR follows the dependency chain; the atomicity guarantee is enforced by the impl-PR's all-or-nothing merge.

### Dependency chain (resolves Fix #6 — language unification → algorithm spec → automation)

The fixes from self-consistency verification have an ordering constraint:
1. **Language unification first** (§5 §7 — byte-for-byte identical phrasing) — without this, the linter and impl-PR review can't enforce a consistent standard.
2. **Algorithm specification second** (§6.8 detail) — the linter algorithm must reference the unified language; without language, algorithm has no anchor.
3. **Automation implementation third** (§6.8 actual `tier_coherence.py` code) — the code enforces what the algorithm specifies.

This ordering is reflected in the spec itself: §5 (language) appears before §6.8 (algorithm), and the linter implementation lands in the impl-PR after both are stabilized.

### Edit order within the impl-PR

1. **Tier 1 + Tier 2 documents (§6.1, §6.2)** — populate with verbatim relocated text. These are additive to currently-DRAFT documents.
2. **conversus-oss/CONSTITUTION.md reduction (§6.3)** — delete relocated principle bodies, preserving SIR audit trail. This is the destructive edit; it must come AFTER the Tier 1 / Tier 2 documents have the relocated text.
3. **CONFORMANCE.md updates (§6.6, §6.7)** — flip status, fill in admission deliberation reference. Independent of constitution edits but must be in the same PR for consistency.
4. **Governance logs (§6.4, §6.5)** — add v4.0.0 ratification entries. These reference the constitution edits, so come after.
5. **Linter (§6.8)** — `tier_coherence.py` + test file. Depends on the new constitution structure existing.
6. **CHANGELOG (§6.9)** — purely descriptive; can land anywhere in the PR but conventionally last.

### Atomicity verification

Per Fix #4 — the impl-PR review checklist verifies atomicity by running, on the merged tree:
- All §7 (verbatim text preservation — concrete check) negative greps. PASS = no orphan content in any file.
- The new tier-coherence linter from §6.8. PASS = all four checks pass.
- A spot-check on 2-3 random relocated principles: open at new location, verify byte-for-byte preservation against pre-PR `git show HEAD~1:conversus-oss/CONSTITUTION.md` extract.

If any verification fails, the PR is reverted (not "fixed forward"). The all-or-nothing rule prevents inconsistent intermediate states from landing on `main`.

### Pre-merge gate

Before the impl-PR can merge:
- Self-consistency verification (§8.1) PASS or PASS-WITH-FIXES with all fixes applied. (Already PASSED WITH FIXES 2026-05-06; 7 fixes applied in this v2.)
- Blind verification (§8.2) PASS, OR PASS-WITH-FIXES with all fixes applied, OR override-with-rationale logged in three places (§8.3) if applicable.
- All §7 verification greps pass on the proposed PR diff.
- Tier-coherence linter passes on the proposed PR diff.
- CI (existing checks) green.

## 11. Sync Impact Report (preview text for conversus-oss/CONSTITUTION.md)

```
<!--
Sync Impact Report
Version change: 3.2.3 → 4.0.0 (MAJOR — tier extraction. 20 principles
relocated to higher tiers; 6 retained at component scope; 2 retired
markers preserved.)

Modified sections:
  - "Core Principles" reduced to 6 principles (XVII-XXI, XXVI) plus
    retired markers for VI and X. Cross-reference block added at top
    pointing readers to ../build-fractal/CONSTITUTION.md (Tier 1) and
    ../build-fractal/conversus/CONSTITUTION.md (Tier 2) for relocated
    principles.
  - "Governance" preserved verbatim. Pathway Taxonomy, Constitutional
    Inclusion Criteria, Compliance, Amendment Process all retained
    here as the canonical procedural reference for amendments at any
    tier.

Relocated to Tier 1 (build-fractal/CONSTITUTION.md, v1.0.0):
  I, II, III, IV, VII, VIII, IX, XI, XIV, XXVIII

Relocated to Tier 2 (build-fractal/conversus/CONSTITUTION.md, v1.0.0):
  V, XII, XIII, XV, XVI, XXII, XXIII, XXIV, XXV, XXVII

Retained at component tier:
  XVII, XVIII, XIX, XX, XXI, XXVI

Retired (number stability — never reuse):
  VI (Scripts Over Markdown) — retired v3.0.0
  X (Zen of Python Output) — retired v3.0.0

Why MAJOR: structural reorganization of the canonical constitution.
Existing readers' paths to relocated principles change. Per Principle II
the principle numerals stay stable across tiers; per the verbatim
preservation contract (spec 081 §5) the principle bodies are
byte-equal at their new locations.

Suite admissions ratified at v4.0.0:
  - conversus-oss admitted Provisional (5 open remediations: V, XII,
    XXII, XXIV, XXVI) per CONFORMANCE.md.
  - conversus admitted Provisional (4 open remediations: III, XIV,
    XVI, XXII) per CONFORMANCE.md.

Constitutional debt acknowledgment (per Fix B2):
  Tier 1 (Universal) carries grandfathered principles ratified
  pre-Inclusion-Criteria-gate (v2.4.0): I, II, III, IV, VII, VIII,
  IX, XI, XIV. XXVIII passed the post-gate criteria. Their
  constitutional validity is preserved per Principle II + the
  grandfathering provision; their post-gate compliance with current
  Inclusion Criteria is NOT re-evaluated by v4.0.0. Future targeted
  amendments may address individual principles' post-gate
  conformance as separate cycles.

Cross-tier weakening prohibition (per Fix B3):
  A lower-tier amendment weakens an upper-tier principle if any of:
  (i) implicit relief outside COMPLIANCE.md Part VI Relief pathway;
  (ii) interpretation language flipping existing-Satisfied to
  not-Satisfied; (iii) suite-specific adaptation bypassing a MUST.
  Enforcement: meta-arbiter review + tier-coherence linter
  flagged-words check + existing-implementation impact check on
  every cross-tier amendment. Spec §6.10 documents the full
  operational definition.

Originating deliberation:
  deliberations/v4.0.0-tier-extraction-originating-2026-05-06/
  Verdict: Q1 APPROVE-AS-DRAFTED, Q2 ADMIT-PROVISIONAL, Q3 ADMIT-
  PROVISIONAL. All four P1 conditions discharged or translated to
  Provisional remediations.

Verification deliberations (both required per spec 067):
  - deliberations/v4.0.0-tier-extraction-self-consistency-{date}/
  - deliberations/v4.0.0-tier-extraction-blind-{date}/
  Acceptance bar: 0 ACCEPT findings on new wording / structure.

Spec: specs/v4.0.0-tier-extraction/spec.md
Governance log: ../build-fractal/conversus/CONSTITUTIONAL_CONVERSATIONS.md
                ../conversus-oss/CONSTITUTIONAL_CONVERSATIONS.md

Discharges: build-fractal Phase A → Phase B in
            ~/.claude/plans/peaceful-stargazing-moler.md.

Prior amendment (v3.2.2 → v3.2.3): see prior SIR comment block below.
-->
```

(Final SIR text drafted as part of the impl-PR; this is the preview. SIR audit-trail preservation per Fix #3: all prior SIR comment blocks — v3.2.2, v3.2.1, v3.2.0, v3.0.0, v2.x — remain in place below the new v4.0.0 SIR.)

## 12. Status & next steps

This spec is **Draft v4 — both verifications complete (self-consistency 2026-05-06, blind 2026-05-07); 13 total fixes applied (12 from verifications + 1 post-impl erratum 2026-05-08); ready for impl-PR**. To proceed:

1. ~~Run self-consistency verification per §8.1.~~ COMPLETE 2026-05-06 — `deliberations/v4.0.0-tier-extraction-self-consistency-2026-05-06/arbitration/resolution.md` ruled PASS WITH FIXES; 7 fixes applied in v2.
2. ~~Run blind verification per §8.2.~~ COMPLETE 2026-05-07 — `deliberations/v4.0.0-tier-extraction-blind-2026-05-07/arbitration/resolution.md` ruled PASS WITH FIXES; 5 fixes B1-B5 applied in v3.
3. Open implementation PR per §10. The PR is monolithic and lands all edits §6.1-§6.10 + linter + CHANGELOG + governance log entries atomically.
4. Log all three deliberations (originating + self-consistency + blind) in the appropriate `CONSTITUTIONAL_CONVERSATIONS.md` files per §6.4 and §6.5 (those entries land as part of the impl-PR's edits to those log files).
5. On merge: status flips from `Draft v3` to `Ratified — v4.0.0`.

No further verification deliberations required: per spec 067, blind PASS WITH FIXES + applied fixes + the fixes not substantively changing the amendment is sufficient. The B1-B5 fixes refine underspecified mechanisms (linter strengthening, debt acknowledgment, weakening prohibition, cross-reference patterns expansion, XVI rationale) without altering the substantive 10/10/6 tier classification or the verbatim preservation contract.

## 13. Fix ledger (resolves both verification legs' PASS-WITH-FIXES findings + post-impl erratum)

### v2 fixes (self-consistency verification 2026-05-06 — 7 ACCEPT findings)

| # | Fix | Spec section affected |
|---|---|---|
| 1 | Unify preservation contract language ("byte-for-byte identical") | §5 (intro paragraph + body verbatim bullet) |
| 2 | Specify tier-coherence linter algorithm + scope rationale + paths + CI | §6.8 (rewritten as 4 checks with explicit algorithm + normalization + impl) |
| 3 | Explicit SIR audit-trail preservation | §6.3 (added explicit bullet); §11 (SIR preview noted preservation) |
| 4 | File-edit dependency ordering + atomicity verification | §10 (rewritten with edit order + atomicity check + pre-merge gate) |
| 5 | Multi-layer cross-reference validation in linter | §6.8 (added Check (c) — cross-reference resolution validation) |
| 6 | Sequence language unification → algorithm → automation | §10 (added Dependency chain section with explicit ordering) |
| 7 | Document cross-reference patterns that actually appear (4-5 patterns) | §5 (added cross-reference patterns table) |

### v3 fixes (blind verification 2026-05-07 — 5 ACCEPT findings)

| # | Fix | Spec section affected |
|---|---|---|
| B1 | Strengthen tier-coherence linter algorithm — dual-signal (identity-marker + 5-gram fingerprint Jaccard >0.85) + escape-hatch exclusion list | §6.8 Check (a) — rewritten with Signal 1 + Signal 2 + escape-hatch + tradeoffs |
| B2 | Constitutional debt acknowledgment for grandfathered Tier 1 principles | §3 (Non-goals — added subsection); §11 (SIR preview text noted) |
| B3 | Operational cross-tier weakening prohibition with concrete criteria (i)-(iii) and three-pronged enforcement | §6.10 NEW; §11 (SIR preview text noted) |
| B4 | Expand cross-reference patterns — Amendment records, inline citations, adjacent-phrase forms, backward references | §5 (added 4 new rows to patterns table) |
| B5 | XVI Suite-tier rationale (mathematical transparency as governance discipline) | §4 (Tier 2 row + footnote) |

ACKNOWLEDGE-level findings (non-blocking, listed for record): rollback verification procedure, prohibition-against-interpretation-layer-attacks (overlaps with B3), Principle XIX reclassification candidate (Suite-tier consideration deferred to v4.1.x), SIR cross-reference preservation check, standardize priority classification system. These may land opportunistically during impl-PR review or as follow-on amendments.

DEFER-level findings: Principle IV/XVII semantic tension (pre-existing in v3.2.3, exacerbated by but not created by tier extraction; deferred to v4.1.x or later cycle for explicit reconciliation). All other pre-existing flaws in `conversus-oss/CONSTITUTION.md` v3.2.3 surfaced incidentally during either verification leg are out of v4.0.0 scope per spec 067 § override-with-rationale boundary.

### v4 fixes (post-impl erratum 2026-05-08 — 1 ACCEPT finding from user review)

| # | Fix | Spec section affected |
|---|---|---|
| C1 | Convert filesystem-relative cross-tier references to canonical GitHub URLs (single-source-of-truth via URL navigation, preserving repo standalone usability) | §5 (cross-reference patterns table — replace relative-path entries with URL form); §6.3 (cross-reference block at top of conversus-oss CONSTITUTION.md uses URLs); §6.6, §6.7 (CONFORMANCE.md inheritance refs use URLs); §6.8 Check (c) extended with URL-pattern validation against canonical monorepo prefix |

**Rationale for C1:** the v3 spec's reduction-with-relative-paths model broke conversus-oss standalone usability — a user cloning the OSS repo alone or browsing it on github.com saw `../build-fractal/CONSTITUTION.md` references that resolved to nonexistent paths. Surfaced post-impl by user review 2026-05-08. The corrective fix replaces filesystem-relative references with canonical GitHub URLs (`https://github.com/clariti-care/payer-index-mono/blob/main/...`) which:
- Resolve via the network from any reading context (github.com, pip-installed source, monorepo).
- Preserve the single-source-of-truth model (no content duplication; the URL points TO the canonical location).
- Scale to the org level (other Build-Fractal repos use the same pattern).
- Survive future migration of build-fractal/ to its own repo (URLs update uniformly via a script).

**Why this didn't surface in self-consistency or blind:** both verification legs evaluated the spec's claims internally, against the constitution it amends. Neither leg tested the use-case of "what does conversus-oss look like when read standalone via github.com or pip?" That's a downstream consumption test the spec's verification protocol didn't cover. Adding "downstream consumption review" as a third verification leg is a candidate spec 067 amendment for future cycles.

**Why this is a v4 erratum and not a v4.0.1 amendment:** the substantive content of v4.0.0 (tier classification, principle relocation, debt acknowledgment, weakening prohibition, etc.) is unchanged. The fix is a wording-precision correction to the cross-reference resolution mechanism — it doesn't add, remove, or reword any principle. It changes how references in the relocated principles point at their canonical sources. This is within the corrective scope of an erratum; the originating + verification deliberations stand without re-running.

**Implementation script:** `conversus-oss/scripts/v4-url-references.py` performs the relative-path → URL conversion across all 11 affected constitutional documents. Re-runnable; idempotent. Companion to `v4-tier-extraction.py` (the relocation script).
