# gh-aw Revised Position: Subject Arbitration (Phase 6)

**Reviewer**: gh-aw (GitHub Agentic Workflows)
**Date**: 2026-03-19
**Inputs**: APM cross-review, spec-kit cross-review, gh-aw cross-reviews of APM and spec-kit

---

## Disposition of Original Recommendations

### P1-1: Define Phase 6 failure semantics — SURVIVING

**Status**: Surviving (unchanged)

Neither APM nor spec-kit addressed failure semantics in their reviews. APM's cross-review of gh-aw notes the tension between graceful degradation (our position) and loud failure (T-4) but does not argue against the recommendation itself. Spec-kit's cross-review explicitly agrees this is complementary to their output-richness concerns and should take precedence (T-1: "execution safety should gate the initial release").

The recommendation stands as stated: Phase 6 failure falls back to Phase 5 output with a warning in the report. No partial `resolution.md` on disk. The absence of any counterargument from either cross-review strengthens this as a consensus gap in the spec.

### P1-2: Make trigger evaluation robust against template drift — MODIFIED

**Status**: Modified (narrowed to a single mechanism)

This was the most contested recommendation. Three competing proposals emerged:

- **gh-aw (original)**: HTML comment (`<!-- disputes_remaining: N -->`), sidecar metadata file, or locked-heading comment
- **APM**: Structural HTML markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`)
- **spec-kit**: Elevate the heading convention to a locked constraint with template validation

Both cross-reviews (APM DC-3, spec-kit DC-1) correctly identify that implementing multiple mechanisms creates competing contracts. In our own cross-review of spec-kit, we acknowledged that the spec must pick ONE strategy and that implementing both structured signals and locked headings creates a worse situation than the current single convention.

**Revised recommendation**: Adopt APM's structural HTML markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`) as the single canonical trigger mechanism. Rationale:

1. APM's markers serve both trigger evaluation (presence of content between markers) and dispute extraction (content itself can be parsed for the proposed `{REMAINING_DISPUTES}` variable). A scalar count (our original proposal) enables only the trigger check.
2. Markers embedded in the synthesis output keep the single-artifact-per-phase model intact, unlike our sidecar proposal.
3. Markers are invisible to human readers, unlike spec-kit's locked-heading approach which constrains template authoring.
4. The existing fallback-to-triggered behavior (FR-012) remains as the safety net when markers are absent.

We withdraw options (a) sidecar metadata file and (c) locked-heading comment from our original proposal. The HTML marker approach subsumes our original HTML comment option but adopts APM's superior boundary-marker design over our scalar-count design.

### P1-3: Add output validation for the arbitration resolution — MODIFIED

**Status**: Modified (coupled with structured output as a joint requirement)

In our cross-review of spec-kit (DC-1), we identified that spec-kit's structured output requirements (YAML front matter or `<!-- RULING: dispute-id -->` markers) compound with our validation gap into a dangerous combination: structured format requirements on an AI agent with no enforcement mechanism.

APM's cross-review notes the tension between built-in validation (our approach) and hook-based validation (APM's approach), concluding both have merit (T-2).

**Revised recommendation**: Output validation remains P1 but is now explicitly scoped as a two-layer system:

1. **Built-in heading-presence check** (P1): The engine verifies that `resolution.md` contains the four required sections from FR-018 (Process Note, Decision Framework, Binding Decisions, Summary of Changes Required) by checking for expected headings. If validation fails, the engine emits a warning in the report and marks the arbitration as "completed with validation warnings" rather than silently accepting malformed output. This is our original recommendation, unchanged.

2. **No structured format requirements on the arbiter for v1**: We explicitly align with the position from our spec-kit cross-review (DC-1): for the initial release, the resolution is human-readable prose. Machine-readable structured data should be extracted by the engine from the validated prose, not demanded of the LLM agent as a second output format. This withdraws any implicit support for requiring the arbiter to produce YAML or structured markers alongside prose.

Post-arbitration hooks (APM's P2-7) are a reasonable future extension but belong outside the initial spec.

### P2-4: Resolve the template/constraint mismatch for non-cooperative modes — SURVIVING

**Status**: Surviving (strengthened by cross-review analysis)

All three reviews agree the current state is contradictory. The cross-reviews diverge on resolution:

- **APM**: Enable all modes now (P1-1)
- **spec-kit**: Acknowledge templates as draft/experimental
- **gh-aw (original)**: Either remove templates or relax FR-004

In our cross-review of APM (DC-2), we identified that APM's recommendation to enable all modes is the most dangerous recommendation across all reviews. The spec explicitly states that PD and Red-Blue modes "change game dynamics fundamentally and need separate analysis." We provided concrete examples: in PD mode, a Phase 6 arbiter could rehabilitate trust scores, defeating the game mechanism; in Red-Blue mode, giving the attack target binding authority over attack findings is a security anti-pattern.

**Revised recommendation**: Remove the non-cooperative templates from the initial release. Retain them in a `templates/_future/` or `templates/_draft/` directory with a clear README noting they require game-dynamics analysis before activation. This is a narrowing of our original "either/or" recommendation to a specific direction, based on the cross-review evidence that enabling them is unsafe and that leaving them in the active template directory (spec-kit's "acknowledge" approach) still allows accidental discovery by template-scanning tooling.

### P2-5: Add a dry-run/preview arbitration mode — WITHDRAWN

**Status**: Withdrawn

APM's cross-review (DC-1) makes a compelling argument: a "preview ruling" is a contradiction in terms. The binding nature of arbitration IS the value proposition. A non-binding preview creates a category of output that looks like a ruling but carries no authority, and downstream consumers would need to distinguish binding from non-binding resolutions -- a distinction the output format was never designed to carry.

APM correctly identifies that the adoption-risk concern (our motivation) is better addressed by running a small conversus with few disputes, not by fragmenting the output contract.

Spec-kit's cross-review (T-2) suggests dry-run and confidence-based follow-up could coexist as different layers, but this reinforces APM's point: it adds complexity to solve a problem that has a simpler solution (start small).

We withdraw this recommendation entirely. The adoption path is operational (run on a low-stakes conversus first), not architectural (shadow mode).

### P2-6: Emit structured metadata alongside the resolution — WITHDRAWN

**Status**: Withdrawn

APM's cross-review (DC-2) correctly identifies that a sidecar file breaks the single-artifact-per-phase output model. The spec produces one file per phase per agent. Phase 5 produces `final.md`. Phase 6 produces `resolution.md`. A sidecar `metadata.yml` creates a new failure mode: disagreement between the prose resolution and the structured metadata.

Spec-kit's cross-review (DC-2) raises the same concern from a different angle: if structured data lives in both a sidecar and embedded in the resolution, downstream tools have two conflicting sources.

Our own cross-review of spec-kit (DC-1) argued that structured data should be extracted by the engine from validated prose, not produced by the LLM as a second artifact. This position is incompatible with our original recommendation to have Phase 6 produce a sidecar.

We withdraw the sidecar metadata recommendation. If structured metadata is needed, it should be a post-processing extraction step by the engine, not a Phase 6 output requirement. This is a future enhancement, not a v1 concern.

### P2-7: Expand grounding citation scope to include `arbiter.docs` — WITHDRAWN

**Status**: Withdrawn

This is the recommendation we reversed during our own cross-review of spec-kit (DC-3). The grounding document works precisely because it is singular -- it forces the arbiter to derive all rulings from one declared framework. Expanding citation scope to include supplementary docs allows an arbiter to cherry-pick whichever document supports a predetermined conclusion, defeating the transparency mechanism.

APM's cross-review (T-3) frames this as a tension between hierarchy preservation (our approach) and real-world complexity (APM's list-of-paths approach), but both approaches weaken the single-document accountability model that all three reviews independently praised as the spec's strongest design decision.

We withdraw this recommendation and affirm FR-019 as written: the grounding document is the sole citable authority. Supplementary `docs` provide context the arbiter can read and reason about but cannot cite as the basis for a ruling. This preserves the integrity model's auditability.

### P3-8: Document grounding document requirements — SURVIVING

**Status**: Surviving (unchanged)

No cross-review challenged this recommendation. Spec-kit's cross-review (T-4) notes the tension between prescriptive conventions (spec-kit: "use the constitution") and descriptive guidance (gh-aw: "here is what good looks like"), but calls it "low-stakes" and notes both can coexist.

The recommendation stands: add a non-normative section specifying minimum content expectations, recommended structure (numbered principles for easy citation), and anti-patterns for grounding documents.

### P3-9: Add idempotency semantics for re-runs — SURVIVING

**Status**: Surviving (unchanged)

No cross-review addressed this recommendation. It remains a low-cost documentation addition: specify whether re-running Phase 6 overwrites or preserves the previous `resolution.md`. The recommendation to rename previous output to `resolution-{timestamp}.md` stands as the preferred approach, though documenting either behavior explicitly is sufficient.

### P3-10: Consider a `trigger: quorum` option for future iterations — SURVIVING

**Status**: Surviving (unchanged, explicitly deferred)

No cross-review addressed this recommendation. It remains a future-iteration suggestion, not a v1 requirement. The observation that 9 disputes may warrant arbitration while 1 may not still stands, and the quorum trigger would address this without complicating the initial release.

---

## New Recommendations

### N-1: Couple trigger mechanism changes with template authoring documentation (P2)

The convergence across all three reviews on trigger fragility (every review flagged it as P1) and the divergence on solutions (three different hardening strategies) reveals a meta-problem: the spec does not document the contract between Phase 5 templates and Phase 6 trigger evaluation. Regardless of which mechanism is chosen (our revised position: APM's HTML markers), the spec needs a "Template Authoring Contract" section that explicitly declares:

- Which elements of Phase 5 output are consumed by Phase 6 trigger evaluation
- What invariants template authors must preserve
- How the engine validates these invariants at template load time

This is not the same as spec-kit's "elevate to a constraint" recommendation (which we partially withdrew in favor of structured markers). This is a documentation requirement that makes any chosen mechanism discoverable by future template authors, preventing the silent breakage all three reviews warned about.

### N-2: Define the arbiter's relationship to the observation loophole (P3)

In our cross-review of APM (T-5), we identified a genuine ambiguity: FR-015.5 prohibits new recommendations, but the template instructs the arbiter to "note observations in the Confidence Assessment." APM flagged this as a gap (Off-Base #3). We noted that if observations are formally exempted, arbiters can launder new recommendations as "observations."

The spec should add a clarifying constraint: observations in the Confidence Assessment are informational annotations that do not carry decision authority. They are explicitly excluded from the "Binding Decisions" section and from the "Summary of Changes Required" section. An observation that implies a required change is a new recommendation by another name and violates FR-015.5. This preserves the arbiter's ability to flag genuine insights while preventing scope creep through the observation loophole.

---

## Position Summary

### Withdrawn (3 recommendations)

| # | Original | Reason |
|---|----------|--------|
| P2-5 | Dry-run/preview arbitration mode | APM correctly argued that a non-binding ruling is a contradiction; adoption risk is better addressed operationally |
| P2-6 | Structured metadata sidecar | Breaks single-artifact-per-phase model; structured data should be engine-extracted, not LLM-produced |
| P2-7 | Expand grounding citation scope | Dissolves single-document accountability that all three reviews praised; reversed during our own cross-review of spec-kit |

### Modified (2 recommendations)

| # | Original | Modification |
|---|----------|-------------|
| P1-2 | Three options for trigger robustness | Narrowed to APM's structural HTML markers as the single canonical mechanism; sidecar and locked-heading options withdrawn |
| P1-3 | Output validation for resolution | Scoped to built-in heading-presence check only; explicitly excludes structured format requirements on the arbiter for v1 |

### Surviving (5 recommendations)

| # | Original | Confidence |
|---|----------|------------|
| P1-1 | Phase 6 failure semantics | High -- no counterargument from any review; spec-kit explicitly endorsed as prerequisite |
| P2-4 | Resolve template/constraint mismatch | High -- narrowed to "remove from active templates"; APM's "enable all" is unsafe per game-dynamics analysis |
| P3-8 | Document grounding document requirements | Medium -- uncontested but low priority |
| P3-9 | Idempotency semantics for re-runs | Medium -- uncontested but low priority |
| P3-10 | Trigger quorum option (future) | Low -- explicitly deferred; included for completeness |

### New (2 recommendations)

| # | Recommendation | Priority |
|---|---------------|----------|
| N-1 | Template authoring contract documentation | P2 -- prevents recurrence of the trigger fragility all reviews flagged |
| N-2 | Observation loophole clarification | P3 -- prevents scope creep through the confidence assessment section |

### Cross-Review Consensus Points

The following positions achieved agreement across all three reviews and both rounds of cross-review. These should be treated as high-confidence inputs to the spec revision:

1. **The grounding document requirement is the correct integrity mechanism.** Do not weaken it by expanding citation scope or making it optional.
2. **Trigger evaluation is the spec's most dangerous fragility.** A single hardened mechanism must replace or supplement heading-based parsing before shipping.
3. **The non-cooperative template/constraint mismatch must be resolved.** The current state is contradictory. Our revised position: remove from active templates.
4. **Backward compatibility is correctly designed.** No changes needed to the opt-in model.
5. **Template-driven extensibility with `{VARIABLE}` substitution is architecturally sound.** No changes needed to the template system.
