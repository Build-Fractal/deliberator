# APM Revised Position: Subject Arbitration (Phase 6)

**Reviewer**: APM (Agent Package Manager)
**Date**: 2026-03-19
**Type**: Revised position after cross-review by spec-kit and gh-aw

---

## Original Recommendation Dispositions

### P1-1: Remove cooperative-only restriction (FR-004) and enable all four modes

**WITHDRAWN.**

Both cross-reviewers converge on this being the most dangerous recommendation in my review. Spec-kit's cross-review (DC-1) identifies the core error: I treated arbitration as a file-delivery problem ("templates exist, therefore ship them") when it is a mechanism-design problem. gh-aw's cross-review (DC-2) provides the concrete failure scenarios I failed to consider: in Prisoner's Dilemma mode, a Phase 6 arbiter can override trust scores and rehabilitate reputation regardless of revealed preferences, defeating the PD mechanism. In Red-Blue mode, giving the attack target binding arbitration authority over attack findings is a security anti-pattern.

My own cross-review of spec-kit (DC-1) already conceded this point: "resolve DC-1 by adopting spec-kit's position (keep cooperative-only, formally status the other templates as drafts)." I should have caught this in my original review. The existence of templates is necessary but not sufficient evidence that a mode is safe to deploy. Each non-cooperative mode's game dynamics change fundamentally under arbitration and require separate specification.

The correct action is spec-kit's P2-5: acknowledge the non-cooperative templates in the spec, define their status as drafts, and gate their activation behind a separate spec that analyzes per-mode game-theoretic implications.

---

### P1-2: Formalize the `### Remaining Disputes` / `**Dispute:` contract with machine-readable markers

**SURVIVING, modified.**

All three reviews independently identified this fragility. The diagnosis is unanimous (spec-kit SA-1, gh-aw SA-3). The disagreement is on mechanism: my original recommendation proposed `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` structural markers. Spec-kit proposed a template linting rule that validates heading presence. gh-aw proposed three options: HTML comment with scalar count, sidecar metadata, or locked-heading contract.

My cross-review of gh-aw (DC-3) argued that structural markers are preferable to scalar counts because they serve both trigger evaluation and content extraction for the proposed `{REMAINING_DISPUTES}` variable. I maintain this position. However, gh-aw's cross-review correctly notes that the marker approach "makes the synthesis template a dual-purpose document." The modification: structural markers in the synthesis template (APM's approach) combined with spec-kit's recommendation to elevate the contract from assumption to constraint. The linting rule is additive and compatible -- it validates that the markers are present in the template at load time, catching drift before execution.

Modified recommendation: Add `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers to the Phase 5 synthesis template. Elevate the parsing contract from an assumption to a formal constraint (per spec-kit P1-3). Add a template validation step that checks for marker presence during template loading.

---

### P1-3: Align "no new recommendations" constraint with the template's observation mechanism

**SURVIVING, modified.**

Spec-kit's cross-review (T-4) frames this as a genuine tension but does not take a position on resolution. gh-aw's cross-review (T-5) raises the critical counter-argument I underweighted: "If observations are formally exempted, a clever arbiter can launder new recommendations as 'observations' and circumvent the scope constraint entirely."

This is a real risk. My original recommendation asked the spec to "explicitly carve out the observation exception," which is too broad. The modification narrows the carve-out with a structural constraint: observations are permitted only in the Confidence Assessment section (where the template already places them), must be explicitly labeled as non-binding, and must not appear in the Binding Decisions or Summary of Changes Required sections. This preserves the information-capture value of observations while preventing laundering -- if it appears outside the Confidence Assessment section, it violates the constraint regardless of how it is labeled.

Modified recommendation: Add to FR-015 that the arbiter MAY note observations in the Confidence Assessment section that are explicitly labeled as non-binding and excluded from the Binding Decisions and Summary of Changes Required sections. Observations that appear in binding sections violate the "no new recommendations" constraint.

---

### P2-4: Support `grounding` as a list of paths

**WITHDRAWN.**

This is the recommendation where I was most clearly wrong. Both cross-reviewers identified the same fundamental error from different angles. Spec-kit's cross-review (DC-3) makes the definitive argument: "The singularity is a feature, not a limitation -- it prevents citation laundering, where a ruling claims grounding in a chain of linked documents that no single reader can verify." gh-aw's cross-review (DC-1) reinforces this: "If `grounding` becomes a list, the arbiter can cherry-pick whichever document supports a predetermined conclusion."

I was reasoning from APM's context-linking model where composability is always desirable. But grounding serves a different purpose than context. Context is background information that enriches reasoning. Grounding is a constraint mechanism that limits reasoning. Making a constraint mechanism composable weakens the constraint. A single grounding path forces the arbiter to derive all rulings from one declared, bounded, human-verifiable document. That is the integrity property the entire Phase 6 design depends on.

Spec-kit's P2-6 (convention that `arbiter.grounding` SHOULD be the constitution path) is the right complementary recommendation -- it gives the single grounding path semantic meaning without expanding its cardinality.

---

### P2-5: Add `schema` or `version` field to `conversus.yml`

**WITHDRAWN.**

gh-aw's cross-review (DC-3) makes a compelling argument I failed to consider: versioning creates a problem that does not yet exist. The `arbiter` field is fully optional and additive -- it is not a breaking change. Introducing a version field means every existing `conversus.yml` is implicitly "version 0" or "version 1," and future tooling must handle version detection, migration, and validation for each version. The conversus schema has exactly one extension so far.

I was projecting APM's own versioning history onto a younger system with different evolution dynamics. APM's `apm.yml` needed versioning because it underwent breaking changes during rapid early development. Conversus's `conversus.yml` has not yet had a breaking change. The right time to introduce versioning is when a breaking change forces it, not preemptively after the first additive extension. This is a YAGNI violation on my part.

---

### P2-6: Introduce `{REMAINING_DISPUTES}` as a Phase 6-specific template variable

**SURVIVING.**

Neither cross-reviewer challenged the substance of this recommendation. Spec-kit's cross-review (T-3) noted that this would be "a new category of template variable (derived rather than configured)" and that neither review fully addressed the implementation implications. gh-aw's cross-review did not address it. My cross-review of gh-aw (DC-3) argued that structural markers (P1-2) would provide the extraction mechanism.

The implementation concern is valid: all existing template variables are static substitutions from configuration. `{REMAINING_DISPUTES}` would be derived from Phase 5 output, which is a new pattern. However, this is a natural evolution -- Phase 6 is itself a new pattern where one phase's output feeds another phase's input. The structural markers from the modified P1-2 provide a clean extraction boundary. The engine reads between the markers and injects the content as `{REMAINING_DISPUTES}`.

This makes the arbiter's scope machine-defined rather than instruction-dependent. The arbiter receives exactly the remaining disputes, not all disputes with an instruction to ignore the resolved ones. This is a meaningful reduction in prompt fragility.

---

### P2-7: Add hook points for Phase 6 lifecycle

**WITHDRAWN.**

Spec-kit's cross-review (T-1) correctly identifies the philosophical tension: hooks say "let the user define what happens at this point" while behavioral requirements say "the spec defines what happens at this point." These are different extension models and the spec must choose. gh-aw's cross-review (T-3) reframes this as dry-run vs. hooks, but the deeper point is the same.

On reflection, hooks are an APM-specific extension mechanism that does not belong in the conversus spec. Conversus is a framework consumed as a SKILL.md; it is not an APM package with lifecycle events. If post-arbitration validation is needed, the right approach is gh-aw's P1-3 (built-in output validation as a correctness requirement) -- a heading-presence check that runs after Phase 6 and warns on malformed output. This is a behavioral requirement, not a hook point.

My recommendation for hook integration was projection from APM's architecture onto a system with different extension semantics. Withdrawn in favor of gh-aw's built-in validation approach.

---

### P3-8: Design an arbiter extraction/reuse pattern

**WITHDRAWN.**

Spec-kit's cross-review (DC-2) makes the decisive argument: "The arbiter is not a generic capability; it is a role that derives meaning from its relationship to a particular subject, a particular grounding document, and a particular set of disputes. A reusable, distributable arbiter package decouples the arbiter from the context that makes its rulings legitimate."

This is correct. I was reasoning about arbiters the way APM reasons about context files or instruction sets -- portable artifacts that gain value from reuse. But an arbiter's value comes from its contextual relationship to a specific subject and grounding document, not from its portability. An arbiter configuration extracted into `apm_modules/` carries its configuration but not its grounding relationship. The configuration (name, prompt, docs) without the grounding relationship is a hollow artifact.

gh-aw's cross-review (T-4) notes the tension between packaging (APM's view) and per-run configuration (gh-aw's view). For arbitration, gh-aw's implicit model is correct: each conversus run has its own arbiter configuration because each run has its own subject and disputes.

---

### P3-9: Add a machine-readable summary sidecar

**SURVIVING, modified.**

All three reviews identified structured output as a gap. The question is format and mechanism. My original recommendation proposed `resolution.summary.yml` as a sidecar. Spec-kit proposed inline structured markers or YAML frontmatter. gh-aw proposed `metadata.yml` with run-level data.

My cross-review of gh-aw (DC-2) argued that the sidecar should be engine-extracted, not arbiter-produced: "The arbiter produces one document; any structured extraction should be a post-processing step by the engine, not a requirement on the LLM agent to produce two consistent artifacts simultaneously." I maintain this position. Asking an LLM to produce both prose and structured data simultaneously creates a consistency risk that the engine can eliminate.

Spec-kit's cross-review (T-2) notes that APM's sidecar is oriented toward dispute metadata while spec-kit's structured block needs requirement identifiers for downstream SDD consumption. These are complementary needs that a single extraction mechanism can serve.

Modified recommendation: The engine (not the arbiter agent) should extract structured data from the resolution markdown after Phase 6 completes. The extraction produces a single structured file (YAML or JSON) containing both ruling-level data (dispute IDs, rulings, grounding citations, confidence levels) and run-level metadata (dispute counts, trigger type, arbiter name, timestamp). This is a post-processing step, not an additional burden on the arbiter agent. The specific schema should be defined in the spec to ensure the resolution template's headings and structure support reliable extraction.

---

### P3-10: Expand the information-asymmetry assumption

**SURVIVING, modified.**

Both cross-reviewers agreed the assumption is too narrow (spec-kit SA-2). The disagreement is on the reframe. My original recommendation focused on internal-perspective scenarios (integration scope). Spec-kit focused on decision authority. My cross-review of spec-kit (DC-2) identified these as "incompatible reframes" but then proposed a synthesis: "decision authority constrained by a grounding document, informed by the arbiter's unique integration perspective."

On further reflection, spec-kit's framing is the stronger foundation. Decision authority is the necessary condition. Information asymmetry or integration perspective is a common but not required supporting condition. A project owner with decision authority but no special operational knowledge is a valid arbiter (spec-kit's scenario). A system with deep operational knowledge but no decision authority is not a valid arbiter -- it is a consultant, and consultants belong as deliberation agents, not arbiters.

Modified recommendation: Rewrite the assumption around decision authority as the primary legitimacy criterion, with integration perspective as a supporting (but not required) factor. Adopt spec-kit's P2-7 language: "Subject arbitration is meaningful when the arbiter has both decision authority over the target artifact and a declared grounding document that constrains that authority."

---

## New Recommendations

### N-1: Adopt gh-aw's Phase 6 failure semantics (gh-aw P1-1)

gh-aw identified a gap my review missed entirely: the spec says nothing about what happens when the arbiter agent fails mid-execution. This is a correctness-level omission. gh-aw's recommendation is sound: treat Phase 6 failure as Phase 5 being the final state, emit a warning, do not leave a partial `resolution.md` on disk. My cross-review of gh-aw (T-4) explored the tension between graceful degradation and loud failure. For the initial release, graceful degradation with a clear warning is the right default -- it matches the conservative, additive design philosophy of the rest of the spec.

### N-2: Adopt gh-aw's post-arbitration output validation (gh-aw P1-3)

gh-aw's recommendation for a heading-presence check after Phase 6 completes addresses the same concern as my withdrawn P2-7 (hook points) but through a behavioral requirement rather than an extension mechanism. A built-in validation step that checks for required sections (Process Note, Decision Framework, Binding Decisions, Summary of Changes Required) and emits a warning on failure is the right approach. It is simple, reliable, and does not require operator configuration.

### N-3: Adopt spec-kit's low-confidence ruling behavior (spec-kit P1-4)

Spec-kit identified a gap my review missed: the Confidence Assessment section is informational but not actionable. When a binding decision has confidence "Low," nothing special happens. Spec-kit's recommendation -- requiring a `Requires follow-up:` field on low-confidence rulings -- makes the confidence assessment meaningful without adding complexity. This is a small addition with high signal value for downstream consumers.

### N-4: Adopt spec-kit's per-file attribution for multi-target conversus (spec-kit P3-8)

When a conversus runs against multiple target files, the resolution should attribute binding decisions to specific files. My review did not address multi-target scenarios. Spec-kit's recommendation is practical: add a template instruction requiring per-file attribution in the Required changes section. This enables surgical application of rulings without reading the entire resolution.

---

## Position Summary

Of my ten original recommendations, I withdraw four (P1-1, P2-4, P2-5, P3-8), modify three (P1-2, P1-3, P3-9, P3-10 -- four items with modifications), and maintain two without modification (P2-6).

**Withdrawn positions and what I learned:**
- **P1-1 (enable all modes)**: I conflated template availability with deployment readiness. Templates are artifacts; safe deployment requires game-theoretic analysis of how arbitration changes each mode's incentive structure. Spec-kit and gh-aw both caught this.
- **P2-4 (grounding as list)**: I applied APM's composability principle to a constraint mechanism where singularity is the integrity property. Spec-kit's "citation laundering" argument is decisive.
- **P2-5 (schema versioning)**: YAGNI violation. I projected APM's versioning history onto a system that has not yet needed it. gh-aw's argument that additive fields do not require version negotiation is correct.
- **P3-8 (arbiter reuse)**: I modeled the arbiter as a portable artifact when its legitimacy derives from contextual relationships that cannot be packaged. Spec-kit's argument that "you cannot install decision authority from a package manager" is correct.

**Strongest surviving positions:**
- **P1-2 (formalize dispute parsing contract)**: Unanimous agreement across all three reviews. Structural markers plus template validation is the synthesized mechanism.
- **P2-6 (`{REMAINING_DISPUTES}` variable)**: Unchallenged on substance. Makes the arbiter's scope machine-defined rather than instruction-dependent.
- **P1-3 (observation carve-out)**: Modified to be structurally constrained -- observations permitted only in Confidence Assessment, never in binding sections. Addresses gh-aw's laundering concern.

**Adopted from other reviews:**
- Phase 6 failure semantics (gh-aw P1-1)
- Post-arbitration output validation (gh-aw P1-3)
- Low-confidence ruling behavior (spec-kit P1-4)
- Per-file attribution for multi-target runs (spec-kit P3-8)

**Overall shift**: My original review over-indexed on APM's packaging and distribution concerns (reuse, composability, versioning, hooks) and under-indexed on the integrity properties that make arbitration trustworthy (singular grounding, contextual legitimacy, game-theoretic safety). The cross-reviews corrected this. The strongest parts of my original review were the mechanism-level recommendations (dispute parsing, template variables, observation handling) that dealt with the arbitration system on its own terms rather than through APM's lens.
