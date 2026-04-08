# Final Synthesis: 001-Subject-Arbitration v2 Review

**Date**: 2026-03-19
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Synthesizer**: Neutral (post-process)
**Round**: v2 (post-synthesis integration review)

---

## Process

| Dimension | Value |
|-----------|-------|
| Artifacts produced | 15 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes) |
| Agents | APM (Agent Package Manager), spec-kit (SDD framework), gh-aw (GitHub Agentic Workflows) |
| Mode | Cooperative |
| Phases executed | Phase 1 (review), Phase 2 (cross-review), Phase 3 (revision), Phase 4 (disputes) |
| Review iteration | 2 of same spec (post v1 synthesis integration) |
| v1 synthesis changes recommended | 17 |
| v1 changes correctly integrated | 15 (per spec-kit assessment); all agents agree the majority landed well |

---

## v1 to v2 Comparison

### What improved

The spec absorbed the v1 conversus cycle with high fidelity. All three agents independently confirm that the spec is "materially stronger" than the pre-synthesis draft. The 17 actionable changes from the v1 synthesis were integrated as follows:

- **Fully integrated (15)**: Failure semantics (FR-022), output validation (FR-023), structural HTML trigger markers (FR-011), `{REMAINING_DISPUTES}` variable (FR-014), docs-vs-grounding distinction (FR-024), non-cooperative template gating (Constraints), per-file attribution (FR-026), requirement-identifier traceability (FR-025), grounding document stability (Assumptions), idempotency (FR-027), information-asymmetry reframe (Assumptions), backward compatibility (FR-005), template-per-mode extensibility, template authoring contract (Implementation Guidance), grounding document requirements.
- **Partially integrated (1)**: Structured output schema -- fields are listed in Implementation Guidance but as advisory, not normative. The v1 synthesis recommended normative definition of fields with deferred mechanism.
- **Structurally present but incomplete (1)**: Observation carve-out (FR-015.5) -- position adopted but rationale for rejected alternatives not documented.

### v1 disputes resolved

| v1 Dispute | v2 Status |
|------------|-----------|
| Structured output mechanism (YAML vs. engine extraction vs. defer) | **Resolved.** All three agents accept that the arbiter produces prose only, engine extraction is the future mechanism, and the schema is deferred. The mechanism question is settled. Remaining disagreement is narrower: normative weight of advisory schema fields. |
| Non-cooperative template file placement (markers vs. directory vs. frontmatter) | **Resolved.** gh-aw withdrew directory-separation preference (APM's packaging/distribution argument was decisive). All three agents accept in-place markers. The mechanism now has a proposed testable FR (draft template filtering). |
| Observation carve-out enforceability (structural vs. semantic vs. no formalization) | **Resolved.** FR-015.5 adopted structural + labeling approach. All agents accept the resolution, though spec-kit notes the audit trail for the decision is incomplete. |
| Low-confidence ruling behavior (justification vs. lightweight vs. no treatment) | **Resolved.** Not relitigated in v2. The v1 compromise (informational, no mandatory follow-up) holds. |

### v1 disputes that persisted in narrower form

| v1 Dispute | v2 Narrowed Form |
|------------|-----------------|
| Structured output | Schema field normative weight: MUST-level FR (APM) vs. SHOULD-level advisory (gh-aw, spec-kit) |
| Template enforcement | Citation boundary: spec-level FR sufficient (APM) vs. template-level instruction required (gh-aw, spec-kit) |

### New issues surfaced in v2

1. **SKILL.md trigger evaluation drift** -- SKILL.md describes only heading-based parsing, not the structural markers FR-011 now mandates as primary. All three agents flag this as P1.
2. **FR-022/FR-023 boundary ambiguity** -- "malformed output" appears in both requirements with unclear delineation. Resolved during v2 deliberation into a three-tier failure model.
3. **"Dispute entry" undefined for the primary trigger mechanism** -- FR-011 checks for "at least one dispute entry" between markers but never defines the term.
4. **Missing success criteria for post-conversus requirements** -- FR-022 through FR-027 have no corresponding SC entries.
5. **Content-presence gap between trigger evaluation and variable extraction** -- markers could contain only whitespace, causing Phase 6 to fire with empty dispute content.
6. **`trigger: always` endorsement path underspecified** -- no explicit output specification when Phase 6 runs with zero disputes.

---

## Recommendation Scorecard

| Tool | Original | Withdrawn | Modified | Surviving | New |
|------|:---:|:---:|:---:|:---:|:---:|
| APM | 8 | 2 (P1-3 prose conventions, OB-1 grounding hash) | 4 (P1-1, P1-2, P2-5, P3-8) | 4 (P2-4, P2-6, P3-7, P3-12 arbiter sizing) | 5 (N-1 schema endorsement, N-2 success criteria, N-3 three-tier failure, N-4 draft FR, N-5 content guard) |
| spec-kit | 8 | 1 (P3-7 trigger reason variable) | 4 (P1-3, P2-4, P2-5, P3-8) | 3 (P1-1, P1-2, P2-6) | 4 (N-1 FR-022/023 disambig, N-2 draft FR, N-3 per-file attribution, N-4 prose conventions) |
| gh-aw | 8 | 2 (OB-1 directory separation, OB-2 template branching) | 4 (P1-1, P1-2, P2-5, P3-8) | 4 (P2-3, P2-4, P3-6, P3-7) | 3 (N-1 success criteria, N-2 SKILL.md sequencing, N-3 hybrid enforcement) |
| **Totals** | **24** | **5** | **12** | **11** | **12** |

The v2 round shows higher recommendation retention (5 withdrawals vs. 8 in v1) and more new recommendations (12 vs. 9 in v1), reflecting a process that is refining details rather than correcting architectural errors.

---

## Convergence Achieved

The following positions are unanimous after two full deliberation rounds. These require no further discussion.

### 1. Three-tier failure model for FR-022/FR-023

All three agents converge on a three-tier disambiguation that APM originated and both others adopted:

1. **Agent-process failure** (FR-022): timeout, crash, no output. No `resolution.md` written. Phase 5 is terminal. Diagnostic emitted.
2. **Structural unintelligibility** (FR-022 sub-case): agent completed but output contains zero FR-018 section headings. No `resolution.md` written. Diagnostic emitted.
3. **Incomplete but parseable prose** (FR-023): agent completed, output has at least one FR-018 heading but is missing others. File IS written. Warning emitted.

The bright-line test between tiers 2 and 3 -- whether the output contains at least one FR-018 section heading -- is unanimously accepted as implementable.

### 2. SKILL.md sync must follow dispute-entry definition

All three agents agree that (a) SKILL.md is out of sync with FR-011 and must be updated, and (b) the "dispute entry" concept must be defined in FR-011 before SKILL.md is synced. Propagating an undefined term into the executable skill definition would compound the ambiguity. The ordering is settled; the dispute-entry definition itself remains contested.

### 3. Content-presence guard scoped to `trigger: disputes_remain` only

All three agents converge: for `trigger: disputes_remain`, if structural markers contain only whitespace or no qualifying content, the trigger evaluates to `false`. For `trigger: always`, the trigger fires regardless of content, with a diagnostic warning if `{REMAINING_DISPUTES}` extraction produces empty content. The subject-endorsement path (US1-AS3) is preserved.

### 4. Draft template filtering requires a testable FR

All three agents agree the Constraints-section MUST for draft template filtering needs a dedicated FR. The engine MUST NOT dispatch templates containing `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`. The engine MUST emit a diagnostic when a matching template is skipped. FR-004 is the primary gate (config-time); the new FR is defense-in-depth (dispatch-time). gh-aw's withdrawal of the directory-separation preference removes the last mechanism disagreement.

### 5. Template authoring contract must be scoped to cooperative mode with per-file attribution

All three agents agree that the current contract implicitly assumes cooperative-mode Phase 5 output and should state that explicitly. Non-cooperative modes produce fundamentally different outputs and will need their own contracts. APM's per-file attribution invariant (FR-026) is adopted within the cooperative-mode scope. The scoping and invariant additions land simultaneously, resolving the sequencing concern.

### 6. Endorsement-mode behavior under `trigger: always` with empty disputes

All three agents agree the `trigger: always` + empty `{REMAINING_DISPUTES}` path must be explicitly specified. When Phase 6 runs in this condition, the arbiter operates in endorsement mode. FR-018 required sections still apply: Process Note reflects the trigger reason, Binding Decisions contains a confirmation statement rather than dispute rulings, and Confidence Assessment evaluates the synthesis positions.

### 7. All v1 convergence points remain settled

The 8 convergence points from v1 -- grounding singularity, Phase 6 failure fallback, cooperative-only restriction, backward compatibility, template-per-mode extensibility, structural trigger markers, information-asymmetry reframe, schema versioning deferral -- were not relitigated and remain in force. The v2 spec integrates all of them correctly per unanimous assessment.

---

## Remaining Disputes

### Dispute 1: "Dispute entry" definition for the primary trigger mechanism

| Agent | Position |
|-------|----------|
| **APM** | Any line matching the `**Dispute:**` pattern (or `**Dispute` with formatting tolerance). Keeps primary and fallback mechanisms structurally aligned. Prevents false positives from template artifacts and preamble text. |
| **gh-aw** | Any line containing non-whitespace content that is not an HTML comment. Decouples the trigger from Markdown formatting conventions. A false-positive trigger surfaces a Phase 5 template bug rather than silently swallowing it. |
| **spec-kit** | Endorses gh-aw's content-negative definition. The structural markers exist to decouple evaluation from prose formatting; APM's pattern requirement re-couples them, making the primary mechanism functionally identical to the fallback. |

*Nature*: Strictness-vs-decoupling tradeoff. APM optimizes for trigger precision (no false positives). gh-aw and spec-kit optimize for trigger mechanism independence (markers serve a different purpose than heading parsing).

### Dispute 2: Structured output schema -- normative weight and v1 prose conventions

| Agent | Position |
|-------|----------|
| **APM** | Schema fields (`dispute_id`, `ruling_type`, `grounding_citation`, `required_changes`, `affected_target_files`, `confidence_level`) belong in a dedicated "Deferred: Structured Output" section with SHOULD-level language. Accepts gh-aw's advisory framing with APM's `affected_target_files` pluralization. The v1 contract is FR-018 section headings only -- no prose conventions, no normative schema. |
| **spec-kit** | Withdrew normative FR proposal. Adopted a hybrid: prose conventions (`**Dispute:**`, `**Ruling:**`, etc.) as SHOULD-level template instruction in FR-015 for v1, plus advisory schema fields in a dedicated section for v2 planning. Two contracts, one per version. |
| **gh-aw** | Schema fields in a standalone "Deferred: Structured Output" section with SHOULD-level language. No v1 prose-level structural requirements beyond FR-018 section headings. Adding labeled sub-field conventions to FR-015 is a softer version of requiring structured output from the LLM and creates a dependency downstream tooling will rely on. |

*Nature*: APM and gh-aw align on "section headings only for v1, advisory schema for v2." Spec-kit stands alone in wanting v1 prose conventions as an intermediate step. The core question is whether the v1 template should instruct the arbiter to use labeled sub-fields in Binding Decisions entries.

### Dispute 3: Success criteria priority classification

| Agent | Position |
|-------|----------|
| **spec-kit** | P1. Missing SCs are a spec-completeness defect. Without explicit SCs, independent implementors will produce incompatible failure behaviors. SCs are the bridge between normative language and test plans. |
| **APM** | P1. Concedes spec-kit's identification. "A spec without acceptance criteria for its requirements is incomplete by any consumption model." |
| **gh-aw** | P2. Accepts the SCs must be added but classifies as design integrity, not correctness. FRs with RFC 2119 language are implementable without SCs; the SCs formalize the acceptance boundary rather than creating it. |

*Nature*: Two agents (APM, spec-kit) say P1. One agent (gh-aw) says P2. The SCs will be added regardless; the dispute affects sequencing priority only.

### Dispute 4: Citation boundary enforcement -- spec-level FR vs. template-level instruction

| Agent | Position |
|-------|----------|
| **gh-aw** | The arbiter is an LLM agent that sees its prompt, not the spec. FR-024 in the spec is invisible at runtime. The template must contain the citation-boundary instruction or the constraint is unenforceable. FR-023 validates headings, not citation sourcing -- there is no post-hoc catch. |
| **spec-kit** | Endorses gh-aw. The enforcement surface for an LLM agent is the prompt. One sentence in the template closes the gap at low cost and can be kept in sync with FR-024 via a template authoring contract invariant. |
| **APM** | FR-024 is normatively sufficient. Restating spec requirements in templates creates maintenance drift where template and spec can diverge. The fix is to extend FR-023 validation scope to include citation-source checking, not to push enforcement into the template. |

*Nature*: Two agents (gh-aw, spec-kit) say the template is the enforcement surface for LLM agents. One agent (APM) says the engine should validate post-hoc. The disagreement is about where enforcement lives in an LLM-agent system.

---

## Actionable Spec Changes

Changes are presented as the DELTA from v1 -- what still needs to happen given that 15 of 17 v1 changes have already been integrated.

### P1 -- Required for Correctness

**1. Define "dispute entry" in FR-011 and sync SKILL.md.**
The term "dispute entry" used in the primary trigger mechanism has no definition. Define it (the exact definition is disputed -- see Dispute 1 -- but the need for a definition is unanimous). Then update SKILL.md to reference structural markers as primary with heading-based parsing as fallback. The two steps are a single logical unit; the definition must precede the sync. *(Unanimous on need; disputed on definition.)*

**2. Add disambiguating sentence to FR-022 for the three-tier failure model.**
Clarify that FR-022 covers (a) agent-process failure (timeout, crash) and (b) structurally unintelligible output (zero FR-018 section headings). FR-023 covers output with at least one FR-018 heading but incomplete structure. The bright-line test: presence of at least one FR-018 section heading. *(Unanimous.)*

**3. Add success criteria for FR-022, FR-023, FR-024, FR-027.**
At minimum: (a) Phase 6 failure produces Phase 5 terminal state with diagnostic warning, (b) malformed-but-parseable resolution triggers validation warning, (c) `docs` citations are never the sole basis for a binding ruling, (d) re-running Phase 6 overwrites previous output. *(Unanimous that SCs are needed; disputed P1 vs. P2 -- 2:1 in favor of P1.)*

**4. Scope template authoring contract to cooperative mode and add per-file attribution.**
Change the contract header to declare cooperative-mode applicability. Add a fifth invariant: "When multiple target files exist, binding decisions must specify which file each required change applies to (per FR-026)." *(Unanimous.)*

### P2 -- Required for Design Integrity

**5. Add normative FR for draft template filtering.**
New FR: "The engine MUST NOT dispatch templates containing a `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` marker. If a matching template contains this marker, the engine MUST skip it and emit a diagnostic message." Document the relationship between FR-004 (config-time gate) and this FR (dispatch-time gate) as layered defense. *(Unanimous.)*

**6. Add content-presence guard to FR-011 scoped to `trigger: disputes_remain`.**
For `trigger: disputes_remain`: if structural markers are present but contain no qualifying content, the trigger evaluates to `false`. For `trigger: always`: the trigger fires regardless, with a SHOULD-level diagnostic if extraction produces empty content. *(Unanimous on scoping; dispute-entry definition affects the qualifying-content test.)*

**7. Specify endorsement-mode behavior under `trigger: always` with empty disputes.**
Add to FR-015 or the template authoring contract: when Phase 6 runs under `trigger: always` and `{REMAINING_DISPUTES}` is empty, the arbiter operates in endorsement mode. FR-018 sections still apply; Binding Decisions contains a confirmation statement; Confidence Assessment evaluates the synthesis positions. *(Unanimous.)*

**8. Create a "Deferred: Structured Output" section with advisory schema fields.**
Move schema fields from Implementation Guidance to a standalone section. Include `dispute_id`, `ruling_type`, `grounding_citation`, `required_changes`, `affected_target_files` (list), `confidence_level`. Use SHOULD-level language: future structured extraction SHOULD target these fields, subject to revision after implementation experience. *(2:1 -- APM and gh-aw align on section headings only for v1; spec-kit wants additional prose conventions.)*

**9. Add rationale for the observation carve-out (FR-015.5) to the Conversus Review section.**
Document why "structural + labeling" was chosen over "structural-only" (APM v1) and "no formalization" (gh-aw v1). Scoped to FR-015.5 only -- the other three v1 dispute resolutions are adequately documented by their implementation text. *(2:1 -- APM conceded to spec-kit; gh-aw silent, implying non-objection.)*

**10. Cross-reference Phase 5 synthesis template in the template authoring contract.**
Point to the synthesis template or document its output schema so Phase 6 template authors can verify their templates consume correct inputs without reading the synthesis template source. *(APM originated; uncontested.)*

### P3 -- Recommended Improvement

**11. Add arbiter prompt sizing guidance to Edge Cases.**
Note that `arbiter.prompt` should be concise (role definition and constraints only) because the grounding document and disputes provide the substantive input. Prevents context-limit issues with large grounding documents. *(APM originated; uncontested.)*

**12. Clarify "binding" in Key Entities section.**
Add: "Binding refers to the finality of the deliberation record -- no further conversus phases revisit the decision. The arbiter's output is authoritative within the conversus process; its effect on downstream actors is governed by the consuming system's integration, not by this spec." *(APM originated; modified per gh-aw's tension on downstream authority.)*

**13. Add validation-error for unknown trigger values.**
Unknown `trigger` enum values MUST produce a validation error, not silent acceptance. Prevents typos from passing config validation. Defer the extensibility framing until existing values are fully specified. *(APM originated, narrowed per gh-aw.)*

**14. Add extraction validation diagnostic for `{REMAINING_DISPUTES}`.**
After extracting content for the `{REMAINING_DISPUTES}` variable, the engine SHOULD log a diagnostic if extraction is empty when the trigger evaluated to true. Non-blocking warning for data-flow observability. *(gh-aw originated; uncontested.)*

**15. Acknowledge the hybrid enforcement model in the template authoring contract.**
Add a sentence making explicit that engine enforcement (FR-023, draft template FR) validates output structure and template eligibility, while template authors are responsible for instructional completeness per the contract invariants. *(gh-aw originated; uncontested.)*

---

## Assessment

### Is the spec ready for implementation?

**Yes, with conditions.** All three agents independently conclude the spec is ready for implementation planning. The v1 synthesis integration was executed with high fidelity -- 15 of 17 changes landed correctly. The v2 deliberation resolved the deepest architectural disagreements from v1 (structured output mechanism, failure-state disambiguation, trigger scoping, template placement mechanism) and produced 7 new unanimous convergence points on top of the 8 from v1.

### What blocks implementation

Two items require resolution before implementation can proceed without ambiguity:

1. **"Dispute entry" definition (Dispute 1, P1).** The trigger mechanism cannot be implemented until this term is defined. The definition affects both FR-011 and SKILL.md. The 2:1 split (gh-aw + spec-kit favor content-negative; APM favors pattern-positive) provides a clear majority position but the spec author should record the rationale for the chosen approach.

2. **FR-022/FR-023 disambiguating sentence (P1).** The three-tier model is unanimous but the one-sentence clarification has not been written into the spec yet. This is a text change, not a design decision -- the design is settled.

### What does not block but should land before v1 ships

- Success criteria for FR-022 through FR-027 (P1 item 3) -- the requirements exist but have no acceptance tests.
- Template authoring contract scoping and per-file attribution (P1 item 4) -- prevents contract/requirement disconnect.
- Draft template filtering FR (P2 item 5) -- the MUST exists in Constraints but is not testable without an FR.

### What can be deferred

- Structured output schema normative weight (Dispute 2) -- all agents accept SHOULD-level advisory for v1.
- Citation boundary template instruction (Dispute 4) -- the risk is low because the grounding document is the dominant arbiter context.
- Prose conventions for Binding Decisions entries -- spec-kit's hybrid proposal can be evaluated after observing real arbiter output.

### Overall trajectory

The v1 cycle resolved architectural disputes (composability vs. constraint singularity, templates-as-artifacts vs. validated-mechanisms, LLM output structure). The v2 cycle resolved operational disputes (failure tiers, trigger semantics, template filtering mechanisms). The remaining disputes are calibration disagreements within a shared design -- they concern mechanism strictness and normative weight, not competing architectures. The spec is converging toward implementation readiness.
