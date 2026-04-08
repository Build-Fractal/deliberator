# Dispute Resolution: Final Synthesis

**Synthesizer**: Neutral arbiter
**Date**: 2026-03-19
**Scope**: 4 blockers from `problem.md`, resolved across 4 phases by 3 agents (Mechanist, Pragmatist, Purist)

---

## Process

| Metric | Value |
|--------|-------|
| Agents | 3 (Mechanist, Pragmatist, Purist) |
| Phases | 4 (Initial review, Cross-review, Revision, Final disputes) |
| Files produced | 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 dispute declarations) |
| Blockers entered | 4 |
| Blockers fully resolved | 3 (Blockers 1, 3, 4) |
| Blockers resolved with narrow residual dispute | 1 (Blocker 2) |
| Concessions made | Mechanist: 3, Pragmatist: 3, Purist: 3 |
| Positions held without modification | Mechanist: 1 (Blocker 1), Pragmatist: 1 (Blocker 1), Purist: 1 (Blocker 4 architecture) |
| Phase 1 alignment | Blockers 1 and 3 had 2:1 majorities; Blockers 2 and 4 had 3-way splits |
| Phase 4 alignment | All 4 blockers at unanimous or 2:1; 3 narrow micro-disputes remain |

---

## Blocker Verdicts

### Blocker 1: "Dispute entry" definition

**Final positions after Phase 4**:
- **Mechanist**: Option B (content-negative). Held throughout all 4 phases.
- **Pragmatist**: Option B (content-negative). Held throughout all 4 phases.
- **Purist**: Option B primary + Option A fallback. *Conceded from Option A in Phase 3*, after the Mechanist and Pragmatist independently demonstrated that (a) pattern-matching as the primary mechanism collapses two trigger paths into one predicate, defeating the architectural purpose of structural markers, and (b) the Purist's own defense-in-depth philosophy from Blocker 4 contradicted selecting the under-detecting mechanism in Blocker 1.

**Verdict**: Option B (content-negative) wins. **Unanimous after Phase 3.**

**Decisive evidence**:
1. FR-012's fail-open directive ("better to run the arbiter unnecessarily than to skip it when disputes exist") establishes a system-level design value favoring false positives over false negatives. All three agents accepted this cost asymmetry as governing.
2. The Mechanist's argument that if primary and fallback use the same pattern, they are one mechanism in two costumes. Defense-in-depth requires independent predicates: content-negative (broad) for primary, pattern-match (narrow) for fallback.
3. The Purist's own concession: "I was applying defense-in-depth selectively [...] I cannot hold both positions simultaneously without a principled distinction between them, and I do not have one."

**Spec text**:

> **FR-011** (amended): [...] the engine looks for content between `<!-- CONVERSUS:DISPUTES_BEGIN -->` and `<!-- CONVERSUS:DISPUTES_END -->` markers and checks whether at least one line contains non-whitespace content that is not an HTML comment. A "dispute entry" is any line within the marker range whose text content, after stripping leading whitespace, is non-empty and is not an HTML comment (i.e., not matching `<!-- ... -->`). The engine does not interpret the formatting or semantics of dispute entries; it evaluates content presence only. This definition intentionally decouples the primary trigger mechanism from Markdown formatting conventions. If the markers contain non-dispute content (template artifacts, preamble text), Phase 6 runs and the arbiter evaluates the content -- the cost of a false-positive trigger is one agent invocation, which is strictly preferable to a false-negative that silently suppresses dispute resolution. If the primary mechanism cannot locate markers, the fallback mechanism checks whether the `### Remaining Disputes` heading contains at least one line matching the pattern `**Dispute` (bold-label prefix). The primary and fallback mechanisms are intentionally different predicates to provide independent detection paths.

---

### Blocker 2: Structured output -- normative weight for v1

**Final positions after Phase 4**:
- **Mechanist**: Option A (headings only) + process-level review trigger. Template authors MAY use labeled sub-fields (not stated in spec). Held headings-only core throughout; added process trigger in Phase 3.
- **Pragmatist**: Option A (headings only) + deferred schema with activation condition + MAY-level template guidance in Implementation Guidance. *Conceded from Option B in Phase 3*, withdrawing SHOULD-level prose conventions after both other agents demonstrated that unenforceable SHOULD conventions create de facto contracts without engine backing.
- **Purist**: Option A core (headings-only contract) + SHOULD-level prose conventions in the deferred section. Modified original Option C in Phase 3 by withdrawing the machine-checkable activation condition. Retained SHOULD for template conventions.

**Verdict**: Option A (headings only for v1) wins. **Unanimous on the core contract.** The Purist's SHOULD for template prose conventions is overruled in favor of MAY, per 2:1 majority (Mechanist + Pragmatist).

**Decisive evidence**:
1. The Mechanist's argument, endorsed by the Pragmatist in concession: "Once the template tells the arbiter to use `**Ruling:**`, downstream consumers will expect `**Ruling:**` to appear. The developer who sees `**Ruling:**` in 95% of real output will write code that depends on it. The SHOULD did not protect them -- it lured them."
2. The Purist's own cross-review concession that the distinction between "constraint instructions" (endorsed for Blocker 4) and "formatting instructions" (rejected for Blocker 2) was "unprincipled." Yet the Purist's correction was to re-introduce SHOULD conventions rather than to accept the inconsistency resolution the other two agents reached (MAY or silence).
3. The Pragmatist's self-diagnosis: "I was doing purist work under a pragmatist banner" -- acknowledging that pre-specifying six labeled sub-fields before any real arbiter output exists contradicts the "iterate from real usage" philosophy.

**Spec text**:

> ### Deferred: Structured Output
>
> The following schema fields are defined as targets for future structured extraction from arbitration output. For v1, the output contract is FR-018 section headings only.
>
> | Field | Type | Description |
> |-------|------|-------------|
> | `dispute_id` | string | Identifier for the dispute being resolved |
> | `ruling_type` | enum | One of `accept`, `reject`, `modify`, `unresolved` |
> | `grounding_citation` | string | Specific principle/requirement cited from the grounding document |
> | `required_changes` | list | Concrete changes required |
> | `affected_target_files` | list | Which target files the changes apply to (per FR-026) |
> | `confidence_level` | string | Arbiter's confidence in the ruling |
>
> **Process note**: This schema is advisory for v1. Promotion to a normative requirement is a future spec decision triggered by downstream consumption needs (CI integration, automated change application, cross-conversus chaining). The v1 implementation SHOULD collect real arbiter output samples to inform the extraction strategy. When a sufficient sample corpus exists (recommended: 50+ arbitration runs), the project SHOULD evaluate whether output consistency justifies formalizing extraction conventions.

Add to Implementation Guidance:

> Template authors MAY use labeled sub-fields (e.g., `**Dispute:**`, `**Ruling:**`, `**Grounding:**`, `**Required Changes:**`) as instructional hints to improve output regularity. This is a template-author design decision, not a spec-level contract. The engine does not validate sub-field presence or format.

---

### Blocker 3: Success criteria priority

**Final positions after Phase 4**:
- **Mechanist**: P1 with 6 SCs in Given/When/Then format. Modified in Phase 3 to adopt Pragmatist's format, Purist's observability standard, and split SC-010 into engine-checkable and human-verifiable tiers.
- **Pragmatist**: P1 with 7 SCs (SC-008--SC-014) in Given/When/Then format. Modified in Phase 3 to expand coverage from 4 to 7 SCs, adding FR-025/FR-026 coverage and SC-014 for vacuous-output detection.
- **Purist**: P1 with 6 SCs. Held priority classification throughout; modified SC-010 to remove sub-field parsing dependency and conditioned SC-012 in Phase 3.

**Verdict**: Option A (P1) wins. **Unanimous from Phase 1.** The Pragmatist's 7-SC set (SC-008 through SC-014) is the most complete and is adopted as the baseline, with the Purist's conditioned SC-012 refinement incorporated.

**Decisive evidence**:
1. Universal agreement from Phase 1. No agent ever contested P1 classification. The Mechanist's framing -- "a requirement without a test is dead letter" -- and the Purist's framing -- "untestable requirements are indistinguishable from aspirations" -- converge from different axioms.
2. APM's concession from the upstream deliberation: "A spec without acceptance criteria for its requirements is incomplete by any consumption model."
3. The Pragmatist's pragmatic argument settled any residual doubt: "The cost of writing SCs is measured in minutes. The cost of discovering incompatible implementations is measured in debugging sessions."

**Spec text**:

> - **SC-008**: Given a Phase 6 agent that fails (timeout, crash, or output containing zero FR-018 section headings), When the engine processes the result, Then no `resolution.md` is written, Phase 5 output is the terminal state, and a diagnostic warning is emitted to stderr identifying the failure reason.
>
> - **SC-009**: Given Phase 6 output containing at least one FR-018 section heading but missing others, When the engine validates the output, Then `resolution.md` is written and a validation warning is emitted to stderr listing the missing headings.
>
> - **SC-010**: Given a `resolution.md` whose Binding Decisions section contains zero textual references to the grounding document (by filename, path, or explicit title), When post-hoc validation runs, Then the engine emits a warning. (Note: v1 validation implements this as a string-presence check for the grounding document path. Full citation-source validation -- verifying that no individual ruling cites only a docs entry -- is a v2 concern requiring structured output.)
>
> - **SC-011**: Given binding decisions that reference requirements in target documents using vague references (e.g., "the validation requirement") instead of specific identifiers (e.g., "FR-003"), When the grounding document contains numbered requirements or identifiers, Then a validation warning is emitted. (This is a SHOULD-level quality check, not a blocking validation.)
>
> - **SC-012**: Given multiple target files in the conversus, When a binding decision's Required Changes section does not specify which file is affected, Then a validation warning is emitted for the unattributed entry.
>
> - **SC-013**: Given an existing `resolution.md` from a previous Phase 6 run, When Phase 6 runs again, Then the engine overwrites the file completely. No merge, no append, no conflict resolution, no confirmation prompt.
>
> - **SC-014**: Given a Phase 6 run where the arbiter produces output with all FR-018 section headings but zero binding decisions in the Binding Decisions section, When the engine validates the output, Then `resolution.md` is written and a validation warning is emitted: "Arbitration produced zero binding decisions -- verify dispute trigger content."

---

### Blocker 4: Citation boundary enforcement surface

**Final positions after Phase 4**:
- **Mechanist**: Option C (all three surfaces), rebalanced from engine-weighted to co-load-bearing. Modified in Phase 3, conceding that engine citation validation is heuristic, withdrawing the claim that the engine is "the only surface that matters," and upgrading the check back to MUST in Phase 4.
- **Pragmatist**: Option C, rebalanced from template-weighted to co-load-bearing. Modified in Phase 3, conceding that deferring the engine check to v2 was "negligent" when the cost is one string comparison, and adopting MUST for the check.
- **Purist**: Option C (all three surfaces), with FR-023 scoped to string-presence. Held the three-surface architecture throughout; scoped the validation check in Phase 3.

**Verdict**: Option C (all three surfaces) wins. **Unanimous from Phase 1.** FR-023 grounding-reference check is MUST-level (3:0 after Phase 4 convergence), scoped to string-presence of the grounding document path in the Binding Decisions section. Semantic citation-source analysis deferred to v2.

**Decisive evidence**:
1. The architectural asymmetry argument, originated by the Purist: FR-015 already restates six behavioral constraints as template instructions. FR-024 is architecturally identical. If one gets template enforcement, both should. No agent contested this.
2. The Pragmatist's self-correction was decisive for dissolving the weighting dispute: "I built my entire review around 'favor the recoverable error' and then proposed a template-only citation enforcement that makes citation violations unrecoverable because they were undetectable."
3. All three agents independently converged on the functional decomposition: template for prevention (shapes the probability distribution at generation time), engine for detection (catches violations after the fact), spec for normative definition. This replaced the original "which surface gets weighted?" question entirely.

**Spec text**:

Amend FR-023:

> **FR-023** (amended): After Phase 6 completes, the engine MUST validate that `resolution.md` contains (a) the required section headings defined in FR-018, and (b) at least one textual reference to the grounding document (by filename, path, or explicit title) in the Binding Decisions section. If heading validation fails, the engine MUST emit a warning to stderr flagging the malformed output. If the grounding-reference check fails, the engine MUST emit a separate warning: "No grounding document citation detected in Binding Decisions (FR-024)." Both warnings are informational -- the file MUST still be written. Semantic citation-source analysis (verifying that individual rulings cite grounding rather than docs as sole authority) is deferred to v2 when structured output makes per-ruling extraction tractable.

Add to FR-015 instruction list:

> 7. Cite ONLY the `grounding` document as authority in binding decisions. Documents provided via `docs` may be referenced for factual context but MUST NOT serve as the sole basis for any ruling.

Add to the Template Authoring Contract invariants:

> - The template must restate the citation boundary constraint from FR-024: only the grounding document may be cited as authority in binding decisions.

---

## Remaining Micro-Disputes

These survived the 4-phase process but do not block implementation. Any resolution produces a workable spec.

### Micro-Dispute A: Prose conventions -- MAY vs. SHOULD (Blocker 2 residual)

The Purist maintains that template-author prose conventions (`**Dispute:**`, `**Ruling:**`, etc.) should be SHOULD-level in the deferred section for visibility to template authors. The Mechanist and Pragmatist maintain MAY-level in Implementation Guidance, arguing that SHOULD creates unenforceable pseudo-contracts. The verdict above adopts the 2:1 majority (MAY), but the Purist's argument about visibility -- that Implementation Guidance is where implementors look for engine behavior, not where template authors look for output expectations -- is a legitimate UX concern about document organization, even if the normative-level question is settled.

### Micro-Dispute B: Vacuous-output arbiter instruction (Blocker 1 / Blocker 3 residual)

The Purist proposes a one-sentence addition to FR-015's behavioral constraints: "If the arbiter determines that no actionable disputes exist in the input, the Binding Decisions section MUST state this explicitly rather than producing fabricated or speculative rulings." The Pragmatist considers SC-014 (post-hoc detection) sufficient. The Mechanist endorsed SC-014 and the Purist's report-level distinction as complementary but did not explicitly address the FR-015 instruction. This is a low-cost addition (one sentence) that addresses a foreseeable input condition created by the content-negative trigger. Recommended for inclusion.

### Micro-Dispute C: SC-011 normative level -- SHOULD vs. MUST for requirement identifiers

The Purist conditioned SC-011 (now SC-012 in the adopted numbering): "When the grounding document contains numbered requirements or identifiers, binding decisions SHOULD reference specific identifiers rather than vague references." The Pragmatist's version emits a validation warning (implying MUST-level detection). The difference is whether vague references produce a warning (Pragmatist) or are merely discouraged (Purist). This is a calibration question for implementation; neither position breaks anything.

---

## Convergence Map

All positions where all 3 agents agree after the full 4-phase process:

| # | Convergence Point | Phase Reached |
|---|-------------------|---------------|
| 1 | Content-negative is the correct primary trigger definition (Option B) | Phase 3 (Purist conceded) |
| 2 | Primary and fallback triggers must be intentionally different predicates | Phase 3 |
| 3 | False positives are cheaper than false negatives (FR-012 cost asymmetry) | Phase 1 (implicit), Phase 3 (explicit) |
| 4 | FR-018 section headings are the sole enforceable v1 output contract | Phase 3 (Pragmatist conceded) |
| 5 | A standalone "Deferred: Structured Output" section with 6 advisory fields | Phase 1 (all three proposed it independently) |
| 6 | Success criteria are P1 and block implementation planning | Phase 1 (unanimous from start) |
| 7 | SCs should use Given/When/Then format with observable outputs | Phase 3 |
| 8 | SC-010 is a string-presence check, not semantic parsing | Phase 3 (all three rewrote it independently) |
| 9 | All three citation enforcement surfaces are necessary (Option C) | Phase 1 (unanimous from start) |
| 10 | Template is the prevention surface; engine is the detection surface | Phase 3 (dissolved the weighting dispute) |
| 11 | FR-023 grounding check is MUST-level, scoped to string-presence | Phase 4 (Mechanist self-corrected from SHOULD) |
| 12 | Semantic citation-source analysis is deferred to v2 | Phase 3 |
| 13 | FR-015 must include a citation-boundary instruction (item 7) | Phase 1 (Purist and Pragmatist), Phase 3 (Mechanist) |
| 14 | Template authoring contract gains a citation-boundary invariant | Phase 1 (all three proposed it independently) |
| 15 | Engine validation is heuristic (not deterministic) for citation checks | Phase 3 (Mechanist conceded, others agreed) |
| 16 | Activation conditions for deferred work must be process-level, not spec-level | Phase 3 (Purist conceded) |

---

## Scorecard

### Blockers Won

| Agent | Blockers where their philosophy prevailed | Details |
|-------|------------------------------------------|---------|
| **Mechanist** | **3** (Blockers 1, 2, 4 -- engine detection) | Blocker 1: content-negative was the Mechanist's position from Phase 1. Blocker 2: headings-only was the Mechanist's position from Phase 1; both other agents moved toward it. Blocker 4: the engine-as-detection-surface framing originated from the Mechanist's insistence on engine validation, even though the Mechanist conceded it was heuristic rather than deterministic. |
| **Pragmatist** | **1.5** (Blocker 1 co-winner, Blocker 3 SC format, Blocker 4 -- template prevention) | Blocker 1: co-held with Mechanist from Phase 1. Blocker 3: the Given/When/Then format and SC-014 (vacuous output) were Pragmatist originals adopted by all. Blocker 4: the template-as-prevention-surface framing became half of the final functional decomposition. |
| **Purist** | **0.5** (Blocker 4 -- defense-in-depth architecture) | The three-surface architecture was the Purist's core thesis from Phase 1 and was unanimously adopted. The FR-015 asymmetry argument (if behavioral constraints get template restatement, citation boundaries should too) was decisive and uncontested. However, the Purist lost the primary contest on Blockers 1 and 2 and had to concede on both. |

### Concessions Made

| Agent | Concessions | Significance |
|-------|-------------|--------------|
| **Purist** | **3 material concessions** | Blocker 1: Abandoned Option A (pattern-match) entirely. Blocker 2: Withdrew machine-checkable activation condition. Blocker 3: Rewrote SC-010 to remove sub-field parsing dependency. The Purist made the largest positional shifts in the process. |
| **Pragmatist** | **3 material concessions** | Blocker 2: Retreated from SHOULD-level prose conventions to MAY-level guidance. Blocker 3: Expanded SC set from 4 to 7. Blocker 4: Conceded that deferring the engine check was "negligent" and adopted MUST-level engine validation. |
| **Mechanist** | **3 material concessions** | Blocker 2: Accepted process-level review trigger for deferred section. Blocker 3: Adopted Given/When/Then format and split SC-010 into engine/human tiers. Blocker 4: Withdrew claim that engine is "the only surface that matters" and conceded citation check is heuristic. The Mechanist's concessions were the most precisely targeted -- smaller positional shifts that addressed specific inconsistencies without abandoning the core position. |

### Summary Assessment

The **Mechanist** won the most blockers by holding firm on positions that proved defensible under cross-examination while making surgical concessions that resolved inconsistencies without retreating from core positions. The content-negative trigger (Blocker 1) and headings-only contract (Blocker 2) were both Mechanist positions from Phase 1 that survived all challenges and attracted concessions from the other two agents.

The **Purist** made the most concessions and the largest positional shifts, but also made the most distinctive contributions to the final spec: the standalone deferred section architecture (adopted by all), the FR-015 asymmetry argument for Blocker 4 (uncontested), the vacuous-output problem identification (addressed by SC-014), and the conditioned SC-012 refinement. The Purist's philosophy lost the headline contests but shaped the fine detail of every resolution.

The **Pragmatist** served as the swing vote and mediator. On Blocker 2, the Pragmatist's concession from Option B to Option A created the 2:1 majority that settled the dispute. On Blocker 4, the Pragmatist's concession on the engine check dissolved the weighting dispute entirely. The Pragmatist's SC-014 (vacuous output detection) was the single most original contribution from the final two phases, accepted by both other agents. The Pragmatist also originated the functional decomposition (template = prevention, engine = detection) that replaced the weighting argument -- the most substantive conceptual contribution of the entire process.
