# Final Synthesis: 001-Subject-Arbitration Self-Review

**Date**: 2026-03-19
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Synthesizer**: Neutral (post-process)

---

## Process

| Dimension | Value |
|-----------|-------|
| Artifacts produced | 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes) |
| Agents | APM (Agent Package Manager), spec-kit (SDD framework), gh-aw (GitHub Agentic Workflows) |
| Mode | Cooperative |
| Phases executed | Phase 1 (independent review), Phase 2 (cross-review), Phase 3 (revision), Phase 4 (disputes) |

---

## Recommendation Scorecard

| Tool | Original Recs | Withdrawn | Modified | Surviving | New |
|------|:---:|:---:|:---:|:---:|:---:|
| APM | 10 | 4 (P1-1, P2-4, P2-5, P3-8) | 4 (P1-2, P1-3, P3-9, P3-10) | 2 (P2-6, P2-7 hooks withdrawn but counted in 4 withdrawals) | 4 (N-1, N-2, N-3, N-4) |
| spec-kit | 10 | 1 (P3-9) | 5 (P1-1, P1-3, P1-4, P2-6, P2-7) | 4 (P1-2, P2-5, P3-8, P3-10) | 3 (N-1, N-2, N-3) |
| gh-aw | 10 | 3 (P2-5, P2-6, P2-7) | 2 (P1-2, P1-3) | 5 (P1-1, P2-4, P3-8, P3-9, P3-10) | 2 (N-1, N-2) |
| **Totals** | **30** | **8** | **11** | **11** | **9** |

---

## Dangerous Contradictions Found

The 6 cross-reviews surfaced 18 dangerous contradictions (3 per cross-review). By category:

| Category | Count | Cross-Reviews Flagging |
|----------|:---:|----------------------|
| Non-cooperative mode: ship all vs. gate on analysis | 3 | APM-of-SK DC-1, SK-of-APM DC-1, gh-aw-of-APM DC-2 |
| Grounding cardinality: single path vs. list/expanded scope | 4 | APM-of-SK T-2, SK-of-APM DC-3, gh-aw-of-APM DC-1, gh-aw-of-SK DC-3 |
| Trigger mechanism: structural markers vs. locked heading vs. boolean | 3 | APM-of-gh-aw DC-3, SK-of-gh-aw DC-1, gh-aw-of-SK DC-2 |
| Structured output: inline vs. sidecar vs. engine-extracted | 3 | APM-of-gh-aw DC-2, SK-of-gh-aw DC-2, gh-aw-of-SK DC-1 |
| Arbiter reuse as package vs. context-bound role | 1 | SK-of-APM DC-2 |
| Dry-run mode undermining binding contract | 1 | APM-of-gh-aw DC-1 |
| Schema versioning: premature vs. forward-compatible | 1 | gh-aw-of-APM DC-3 |
| "No new recommendations" vs. observation loophole | 2 | APM-of-SK DC-3, SK-of-APM T-4 |

---

## Systemic Contradictions

### 1. Constraint singularity vs. composability

The deepest tension across all reviews. APM's design philosophy treats everything as composable, distributable, and reusable (grounding as a path list, arbiters as packageable artifacts, context as linked graphs). The arbitration spec's integrity model depends on deliberate singularity: one grounding document, one arbiter bound to context, one citation authority. Every APM proposal to make arbitration more composable was shown to weaken the constraint mechanism that makes it trustworthy. This tension recurred in the grounding cardinality debate, the arbiter-as-package debate, and the citation scope debate. Resolution: APM conceded on all three fronts, recognizing that constraint mechanisms and context mechanisms serve different purposes.

### 2. Templates-as-artifacts vs. templates-as-validated-mechanisms

APM and gh-aw initially treated the existence of non-cooperative templates as evidence the modes were ready to ship. Both cross-reviews (spec-kit, gh-aw's self-correction) demonstrated that a template is a prompt artifact, not a validated mechanism. In adversarial modes (PD, Red-Blue), arbitration changes the game's incentive structure in ways that require formal analysis. The deeper architectural tension: the conversus framework's template-per-mode design makes it trivially easy to add new phases per mode but provides no gate between "template exists" and "mode behavior is safe." This gap has implications beyond Phase 6 for any future mode-specific extensions.

### 3. LLM output as structured contract vs. probabilistic prose

Spec-kit wants the arbiter to produce structured YAML alongside prose. gh-aw and APM argue that LLM output is inherently probabilistic and should not carry structured format obligations. This tension is fundamental to any AI-agent pipeline: the more structure you demand from the agent, the more failure modes you introduce. The compromise position (engine extraction from validated prose) defers rather than resolves the tension -- it still depends on prose regularity that an LLM does not guarantee.

### 4. Enforcement surface: structural vs. semantic

The observation carve-out debate exposed a recurring pattern. APM wants positional enforcement (observations in this section only). gh-aw wants semantic enforcement (observations must not prescribe changes). Spec-kit wants both layers. The underlying tension: structural rules are machine-enforceable but gameable (put prescriptive text in the allowed section). Semantic rules are ungameable but unenforceable by automation. Every constraint on LLM-produced output faces this tradeoff, and the spec has no general policy for how to handle it.

### 5. v1 scope: pipeline integration vs. operational safety

Spec-kit's recommendations optimize for downstream SDD pipeline consumption (structured output, requirement traceability, checklist integration). gh-aw's recommendations optimize for production safety (failure semantics, output validation, idempotency). Both are necessary but compete for v1 scope. The implicit question the spec does not answer: is Phase 6 a pipeline feature (spec-kit) or a runtime safety mechanism (gh-aw)? The answer shapes which concerns are P1.

---

## Convergence Achieved

The following positions are unanimous across all three agents after the full four-phase process. These are high-confidence inputs requiring no further deliberation.

### 1. Singular grounding document is the core integrity mechanism

`grounding` remains a single path. `docs` provides read-only context only. Only the grounding document may be cited as authority in binding decisions. APM withdrew its multi-path proposal. gh-aw withdrew its citation-scope expansion. Three-agent consensus.

### 2. Phase 6 failure falls back to Phase 5 with a warning

If the arbiter agent fails (timeout, crash, malformed output), the conversus completes with Phase 5 output as the terminal state. A diagnostic warning is emitted. No partial `resolution.md` is written. Originated by gh-aw, adopted by APM and spec-kit with zero counterargument.

### 3. Cooperative-only restriction (FR-004) is correct for v1

Non-cooperative modes require separate game-theoretic analysis. APM withdrew its "enable all modes" recommendation. All three agents agree templates exist but must not be activatable in v1. Disagreement remains only on template file placement.

### 4. Backward compatibility design is correct and complete

The `arbiter` field is fully optional. Omitting it produces identical Phase 1-5 behavior (FR-005, SC-004). Additive-only extension. No agent at any point proposed changes. Most thoroughly validated aspect of the spec.

### 5. Template-per-mode extensibility with `{VARIABLE}` substitution is architecturally sound

The `templates/{mode}/arbitration.md` convention and reuse of the substitution system are endorsed by all three reviews. No code changes required for new modes. Convention-based discovery is correct.

### 6. Trigger evaluation must be hardened with structured signals

Heading-based parsing of `### Remaining Disputes` is the spec's most dangerous fragility. All three agents agree on replacing it with machine-readable signals. APM's boundary markers (`<!-- CONVERSUS:DISPUTES_BEGIN/END -->`) are the leading approach, with heading parsing retained as backward-compatible fallback. Spec-kit conditionally concedes to markers if `{REMAINING_DISPUTES}` variable is adopted.

### 7. Information-asymmetry assumption must be reframed

The current assumption is too narrow. Converged reframe: (1) General principle -- subject arbitration is meaningful when the arbiter has decision authority over the target artifact, constrained by a grounding document. (2) Common case -- the subject typically has integration knowledge that individual reviewers lack. Decision authority is the necessary condition; information asymmetry is common but not required.

### 8. Schema versioning is premature

The `arbiter` field is additive and introduces no breaking change. Versioning adds tooling complexity for a migration that is not needed. Introduce when an actual breaking change forces it. APM withdrew after gh-aw's argument.

---

## Remaining Disputes

### Dispute 1: Structured output mechanism

| Agent | Position |
|-------|----------|
| **spec-kit** | Arbiter produces a fenced YAML block at the end of `resolution.md`, validated post-hoc. Graceful degradation if malformed. Will accept engine extraction if the output schema is normatively defined in the spec. |
| **APM** | Engine extracts structured data from validated prose as a post-processing step. Arbiter produces prose only. Non-negotiable that the arbiter must not produce YAML/JSON. Flexible on extraction schema format and timing. |
| **gh-aw** | No structured format requirements in v1 at all. Machine-readable extraction is a v2 concern. Design schemas after observing real arbiter output patterns, not before. |

*Nature*: Build-measure-learn disagreement. Spec-kit and APM share the goal (structured data exists) but disagree on production mechanism. gh-aw disagrees on timing.

### Dispute 2: Non-cooperative template file placement

| Agent | Position |
|-------|----------|
| **spec-kit** | Retain in `templates/{mode}/arbitration.md`. Add `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker inside each file. FR-004 prevents runtime activation. Tooling filters on marker. |
| **APM** | Prefers in-place with frontmatter `status: draft` field. Will accept directory relocation if full template content is preserved. |
| **gh-aw** | Move to `templates/_draft/` or `templates/_future/`. Directory structure is the only reliable mechanism for preventing accidental discovery by template-scanning tooling. |

*Nature*: Tooling-trust disagreement. Spec-kit and APM trust documentation/markers; gh-aw trusts filesystem structure.

### Dispute 3: Observation carve-out enforceability

| Agent | Position |
|-------|----------|
| **APM** | Structural constraint: observations permitted ONLY in Confidence Assessment section. Anything outside that section violates FR-015.5 regardless of labeling. Non-negotiable. |
| **spec-kit** | Both structural AND semantic constraints: section-restricted (APM's rule) plus content-restricted (must not prescribe specific changes). Defense-in-depth. |
| **gh-aw** | Do not formalize the carve-out. Keep FR-015.5 as a hard prohibition and the template's observation guidance as soft instruction. The ambiguity is a feature: professional judgment room with a bright-line rule for accountability. Formalizing without enforcement creates a rule that is neither guidance nor enforceable. |

*Nature*: Rules-vs-guidance disagreement. APM and spec-kit want explicit formal rules; gh-aw argues formalization without enforcement is worse than the status quo.

### Dispute 4: Low-confidence ruling behavior

| Agent | Position |
|-------|----------|
| **spec-kit** | Require one-sentence confidence justification for ALL levels (not just Low). No behavioral triggers, no mandatory follow-up. Informational transparency. |
| **APM** | Supports spec-kit's revised position. P2 priority, deferrable to v2 if needed. |
| **gh-aw** | No special treatment for any confidence level. Confidence is informational as-is. Adding justification requirements creates process weight; perverse incentives are possible even with the all-levels approach. |

*Nature*: Process-weight disagreement. Spec-kit and APM want confidence to be self-documenting; gh-aw wants to keep it lightweight.

---

## Actionable Spec Changes

### P1 -- Required for Correctness

1. **Add Phase 6 failure semantics.** New FR: if the arbiter agent fails, Phase 5 output is the terminal state. Warning emitted. No partial `resolution.md`. Phase 1-5 record is not invalidated. *(Unanimous)*

2. **Harden trigger evaluation with structural HTML markers.** Replace heading-based parsing as the primary trigger mechanism. Add `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` to Phase 5 synthesis templates. Retain heading parsing as backward-compatible fallback. Update FR-011. *(APM + gh-aw aligned; spec-kit conditionally concedes if `{REMAINING_DISPUTES}` is adopted)*

3. **Add post-arbitration output validation.** Engine checks `resolution.md` for required section headings (FR-018) after Phase 6 completes. Warnings emitted on failure; malformed output is flagged, not silently accepted. *(Unanimous on principle; scope dispute on whether structured format validation is included in v1)*

4. **Reconcile FR-015.5 with the template's observation mechanism.** At minimum: add clarifying language that observations noted in the Confidence Assessment, explicitly labeled non-binding, are not new recommendations. The precise enforcement model (structural-only, semantic-only, or both) remains disputed -- adopt at least APM's structural constraint (Confidence Assessment section only) as the minimum enforceable rule.

5. **Formalize the `docs` vs. `grounding` distinction.** New FR or addition to FR-019: `docs` provides read-only context; only `grounding` may be cited as authority in binding decisions. *(Unanimous)*

### P2 -- Required for Design Integrity

6. **Resolve non-cooperative template status.** Acknowledge templates in the spec as draft/experimental. Retain FR-004 cooperative-only restriction. Gate activation behind a separate game-dynamics analysis spec. File placement (in-place with markers vs. `_draft/` directory) is a disputed implementation detail -- choose one and document the rationale. *(Unanimous on restriction; disputed on file placement)*

7. **Introduce `{REMAINING_DISPUTES}` as a Phase 6 template variable.** Parse between the structural markers from item 2 to extract remaining dispute content. Inject as a dedicated variable, making the arbiter's scope machine-defined. *(APM originated, unchallenged on substance)*

8. **Rewrite the information-asymmetry assumption.** Two-part framing: decision authority as the general principle, integration knowledge as the common case. *(Unanimous)*

9. **Add spec-kit project convention.** Non-normative guidance: when the target is a spec-kit project, `arbiter.grounding` SHOULD be the constitution path. *(spec-kit originated, uncontested)*

10. **Require binding decisions to reference target-document identifiers.** Template instruction: when target documents contain numbered requirements (FR-xxx, SC-xxx), Required changes must cite specific identifiers. *(spec-kit originated, uncontested)*

11. **Add template authoring contract documentation.** New section declaring which Phase 5 output elements Phase 6 consumes, what invariants template authors must preserve, and how the engine validates them. *(gh-aw originated as N-1)*

### P3 -- Recommended Improvement

12. **Define structured output schema.** Regardless of whether the arbiter or the engine produces it, normatively define the fields: dispute ID, ruling type, grounding citation, required changes, affected target file, confidence level. Defer the production mechanism to v2 if needed, but define the schema now. *(spec-kit firm position; APM agrees on schema definition; gh-aw wants to defer entirely)*

13. **Add per-file attribution for multi-target runs.** Template instruction: when multiple target files exist, each binding decision's Required changes must specify which file is affected. *(spec-kit originated, uncontested)*

14. **Document grounding document requirements.** Non-normative section: minimum content expectations, recommended structure (numbered principles), anti-patterns. *(gh-aw originated, uncontested)*

15. **Add grounding document stability note.** Assumption/constraint: the grounding document is assumed stable for the run duration. Concurrent modifications should be avoided. *(spec-kit originated, uncontested)*

16. **Add idempotency semantics for re-runs.** Document whether re-running Phase 6 overwrites or preserves previous `resolution.md`. *(gh-aw originated, uncontested)*

17. **Consider `trigger: quorum` option.** Future iteration: run Phase 6 only when N or more disputes remain. Explicitly deferred. *(gh-aw originated, uncontested)*

---

## Key Concessions

### APM

| Concession | Reason |
|------------|--------|
| Withdrew "enable all four modes" (P1-1) | Conceded that templates existing is not evidence modes are safe. Game-theoretic analysis required per mode. Spec-kit's and gh-aw's PD/Red-Blue failure scenarios were decisive. |
| Withdrew "grounding as list of paths" (P2-4) | Accepted spec-kit's "citation laundering" argument: composable grounding weakens the singular constraint that makes arbitration auditable. |
| Withdrew "schema versioning" (P2-5) | Accepted gh-aw's YAGNI argument: additive optional fields do not require version negotiation. |
| Withdrew "arbiter as reusable package" (P3-8) | Accepted spec-kit's argument that arbiters derive legitimacy from contextual relationships, not portability. "You cannot install decision authority from a package manager." |
| Withdrew "lifecycle hooks" (P2-7) | Accepted that hooks are an APM-specific extension model; conversus should use behavioral requirements (gh-aw's built-in validation) instead. |

**Pattern**: APM over-indexed on its own packaging/distribution/composability paradigm and under-indexed on the integrity properties specific to arbitration. Five of five withdrawals were cases where APM projected its own architecture onto a system with different design goals.

### spec-kit

| Concession | Reason |
|------------|--------|
| Withdrew "lock the heading as a contract" (P1-3 original) | Accepted that template ossification is worse than the fragility it prevents. Adopted structured HTML signals as the primary trigger mechanism. |
| Withdrew "mandatory follow-up for Low confidence" (P1-4 original) | Accepted gh-aw's perverse-incentive argument: mandatory process on Low confidence incentivizes reporting Medium. Replaced with one-sentence justification for all levels. |
| Withdrew "checklist output format" (P3-9) | Accepted that a dedicated checklist artifact overspecifies v1. The structured YAML block (if adopted) serves the same purpose. |
| Conditionally conceded trigger mechanism to APM | Will adopt boundary markers over boolean signal if `{REMAINING_DISPUTES}` variable is accepted. |

**Pattern**: Spec-kit's concessions were tactical (mechanism changes) rather than principled (design goals unchanged). Held firm on grounding singularity, cooperative-only restriction, and the need for structured output schemas.

### gh-aw

| Concession | Reason |
|------------|--------|
| Withdrew "dry-run/preview arbitration" (P2-5) | Accepted APM's argument that a non-binding ruling is a contradiction in terms. Adoption risk is operational (start small), not architectural (shadow mode). |
| Withdrew "metadata sidecar" (P2-6) | Accepted that a sidecar breaks the single-artifact-per-phase model and creates sync-drift risk with the prose resolution. |
| Withdrew "expand grounding citation scope" (P2-7) | Self-corrected during cross-review of spec-kit: broadening citations dissolves the single-document accountability model all three reviews praised. |
| Narrowed trigger proposals to APM's markers (P1-2) | Withdrew sidecar metadata and locked-heading options. APM's boundary markers serve both trigger and extraction with one mechanism. |

**Pattern**: gh-aw's withdrawals reflected self-correction on integrity model coherence. The dry-run and citation-scope withdrawals were cases where operational flexibility conflicted with the binding-decision contract that makes Phase 6 valuable.
