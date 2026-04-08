# gh-aw v2 Revised Position

**Agent**: gh-aw (GitHub Agentic Workflows)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Round**: v2 Revision (post-cross-review)
**Inputs**: APM cross-review of gh-aw, spec-kit cross-review of gh-aw, gh-aw cross-reviews of APM and spec-kit

---

## Disposition of Original Recommendations

### P1-1. Disambiguate FR-022 and FR-023 failure states
**Status: MODIFIED**

APM's cross-review (Dangerous Contradiction 1) correctly identifies that gh-aw's original two-tier disambiguation (process failure vs. content validation) leaves a gap: the agent completes but produces structurally unintelligible output (e.g., a refusal message, raw YAML, non-prose). This is neither a process failure (the agent ran) nor an FR-023 validation failure (there are no section headings to validate because the output is not prose at all). spec-kit's cross-review (Dangerous Contradiction 1) confirms the ambiguity is real -- two careful reviewers (spec-kit and gh-aw) reached opposite conclusions about whether the spec already resolves this, which is itself proof that the text is ambiguous.

**Revised recommendation**: Adopt APM's three-tier model.
1. **Agent-process failure** (FR-022): timeout, crash, no output produced. No `resolution.md` written. Phase 5 is terminal. Diagnostic emitted.
2. **Structural unintelligibility** (FR-022, new clause): agent completed but output contains zero recognizable section headings from FR-018 and cannot be parsed as prose. No `resolution.md` written. Diagnostic emitted with the raw output hash for debugging. This is the "garbage in 200 OK" case APM identified.
3. **Incomplete but parseable prose** (FR-023): agent completed, output is recognizable prose, but one or more FR-018 section headings are missing. File IS written. Warning emitted listing missing sections.

The boundary between tiers 2 and 3 is: does the output contain at least one FR-018 section heading? If yes, tier 3 (write with warning). If no, tier 2 (no file, diagnostic). This is a bright-line test that any engine can implement without semantic parsing.

### P1-2. Define "dispute entry" for the primary trigger mechanism in FR-011
**Status: MODIFIED**

APM's cross-review (Dangerous Contradiction 4) argues that "any non-whitespace content" is dangerously loose -- stray HTML comments, `&nbsp;`, or template artifacts between markers would trigger a spurious Phase 6 dispatch. APM recommends requiring the `**Dispute:**` pattern or at minimum a Markdown bold marker. spec-kit's cross-review (Tension 1) notes that gh-aw's positive definition ("what a dispute entry IS") is more extensible than spec-kit's negative definition ("when the trigger does NOT fire"), but does not challenge APM's concern about false positives.

APM's concern is valid. A false-positive trigger wastes an LLM arbitration call and produces a spurious `resolution.md`. However, coupling the primary mechanism to the `**Dispute:**` pattern would make the primary mechanism no more capable than the fallback, defeating the purpose of structural markers.

**Revised recommendation**: Define "dispute entry" as any line containing non-whitespace content that is not an HTML comment (`<!-- ... -->`). This excludes the stray-comment case APM identified, excludes pure whitespace, but does not couple the trigger to a specific Markdown formatting convention. Template artifacts that are plain text will still trigger -- this is acceptable because such artifacts indicate a Phase 5 template bug that should surface as a diagnostic rather than be silently swallowed.

### P2-3. Add a normative FR for draft template filtering
**Status: SURVIVING**

APM's cross-review agrees with this recommendation explicitly: "APM agrees with gh-aw's P2-3 recommendation (add a normative FR for draft template filtering) as the correct fix." spec-kit's cross-review (Tension 4) notes that spec-kit does not flag the absence of a corresponding FR as a gap but also does not oppose adding one. Both cross-reviews treat the underlying problem (a Constraints-section MUST with no testable FR) as real. This recommendation stands as written: add FR-028 requiring the engine to not dispatch templates containing the draft marker, with a specified diagnostic message.

### P2-4. Add explicit template instruction for the docs vs. grounding citation boundary
**Status: SURVIVING**

APM's cross-review (Tension 4) notes that APM "trusts FR-024 alone" and sees the spec requirement as sufficient without restating it in the template. spec-kit's cross-review does not oppose this recommendation. The tension between spec-level normativity and prompt-level enforceability is real: for LLM-based agents, the template IS the executable contract. An FR-024 requirement that never appears in the arbiter's prompt is a requirement the arbiter cannot follow. APM's position that "FR-024 is normative, the engine validates output, the template inherits the constraint" assumes output validation can detect citation-boundary violations, but FR-023 only validates section heading presence, not citation sourcing. The enforcement gap remains. This recommendation stands as written.

### P2-5. Address the trigger: always + no disputes endorsement path
**Status: MODIFIED**

APM's cross-review (Tension 5) is silent on this concern. spec-kit's cross-review (Tension 3) treats it as a documentation gap rather than a design gap, recommending annotation in the template authoring contract. APM's separate cross-review (Dangerous Contradiction 3) warns against template-level branching, arguing the endorsement path is a data-flow validation problem, not a template design problem, and that adding conditional template logic would violate the principle that templates are static instruction sets.

APM's argument against conditional template logic is persuasive. Templates should remain static instruction sets. The endorsement path does not need a new output format or template branching.

**Revised recommendation**: Add a single sentence to the template authoring contract (not to the template itself): "When `{REMAINING_DISPUTES}` is empty and Phase 6 runs under `trigger: always`, the arbiter's output constitutes a subject endorsement. The FR-018 required sections still apply; the Binding Decisions section contains a statement confirming the synthesis positions rather than dispute rulings." This documents the behavior without adding template complexity. It is spec-kit's lighter approach with gh-aw's specificity about what the FR-018 sections contain.

### P3-6. Add validation for {REMAINING_DISPUTES} extraction
**Status: SURVIVING**

Both APM and spec-kit flag the same extraction-validation gap. spec-kit wants a harder gate (empty markers cause trigger to evaluate false); gh-aw maintains the warning-based approach. APM's cross-review (Dangerous Contradiction 3) agrees the problem is a data-flow validation concern, not a template concern, which aligns with gh-aw's framing. The diagnostic-warning approach preserves `trigger: always` semantics while providing observability. This recommendation stands as written.

### P3-7. Specify the relationship between the draft template marker and FR-004
**Status: SURVIVING**

No cross-review challenged this recommendation. Both APM and spec-kit agree that FR-004 is the primary gate and the draft marker is a secondary mechanism. Documenting the layered defense model is a low-cost improvement. This recommendation stands as written.

### P3-8. Extract structured output schema to a standalone section
**Status: MODIFIED**

This is the sharpest three-way disagreement. spec-kit wants the schema fields elevated to a normative FR (proposed FR-028 with MUST weight). gh-aw recommended organizational relocation to a "Future Work" section. APM wants forward-compatibility conventions baked into prose now. spec-kit's cross-review (Dangerous Contradiction 3) correctly identifies that applying both gh-aw's relocation and spec-kit's normative elevation simultaneously would be contradictory.

gh-aw maintains that premature normative commitment to deferred features is how specs accumulate dead-letter requirements (see gh-aw cross-review of spec-kit, DC-1). The schema fields (`dispute_id`, `ruling_type`, `grounding_citation`, etc.) have zero implementation experience behind them. Locking them into a MUST-level FR before anyone has built the extraction pipeline constrains design flexibility for no current benefit.

However, gh-aw acknowledges spec-kit's concern that pure organizational relocation without any normative signal may cause the fields to be ignored entirely when v2 design begins.

**Revised recommendation**: Extract the schema to a standalone "Deferred: Structured Output" section (not buried under Implementation Guidance). Use SHOULD-level language rather than MUST: "A future version that implements structured extraction SHOULD support the following fields as a starting point, subject to revision based on implementation experience." This provides a normative signal (SHOULD, not MAY) without creating a binding obligation that forecloses implementation discovery. It splits the difference: more visible than gh-aw's original organizational-only proposal, less constraining than spec-kit's MUST-level FR.

---

## Withdrawn Recommendations

### Off-Base Assumption 1: Directory-based template separation (templates/_draft/)
**Status: WITHDRAWN**

APM's cross-review (Dangerous Contradiction 2) delivers the decisive argument: in APM's distribution model, templates ship as self-contained artifacts with declared file manifests. Directory-based separation requires the consumer's engine to understand a layout convention from the source repository. The content-based marker (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`) is self-describing and survives packaging flattening. gh-aw's preference for directory-based separation is correct within gh-aw's single-repo compilation model but incorrect for the broader ecosystem.

gh-aw withdraws the directory-separation preference. The marker-based approach is the right mechanism for a distributable spec. The remaining concern -- that no FR requires the engine to parse the marker -- is addressed by the surviving P2-3 recommendation (add FR-028).

### Off-Base Assumption 2: The endorsement path is a template design problem
**Status: WITHDRAWN (subsumed by modified P2-5)**

APM's argument that templates are static instruction sets, not programs, is correct. The endorsement path is a contract documentation concern, not a template branching concern. The modified P2-5 addresses this through the template authoring contract rather than through template conditionals or separate output formats.

---

## New Recommendations

### N-1. Adopt success criteria for post-conversus requirements
**Priority: P2 (Required for Design Integrity)**

spec-kit's cross-review (Dangerous Contradiction 3) correctly identifies that gh-aw's original review did not address success criteria coverage at all. spec-kit classifies the missing SCs as P1; gh-aw's silence was an omission, not a position. FR-022 through FR-027 are testable by their RFC 2119 language, but explicit success criteria make the acceptance boundary unambiguous for implementors working from different toolchains. gh-aw accepts spec-kit's finding and supports adding SC entries for at minimum:
- SC-008: Phase 6 failure falls back to Phase 5 (FR-022)
- SC-009: Output validation emits warnings for missing sections (FR-023)
- SC-010: Draft templates are not dispatched (Constraints / proposed FR-028)
- SC-011: Re-running Phase 6 overwrites existing resolution.md (FR-027)

gh-aw classifies this as P2 rather than spec-kit's P1 because the FRs themselves are implementable without SCs -- the SCs formalize the acceptance boundary, they do not create it.

### N-2. Sequence SKILL.md sync after dispute-entry definition
**Priority: P1 (Required for Correctness)**

APM's P1-1 (sync SKILL.md) and gh-aw's P1-2 (define "dispute entry") are both correct but order-dependent. gh-aw's cross-review of APM (DC-3) identified this: syncing SKILL.md to the current FR-011 text would propagate the undefined "dispute entry" term into the executable skill definition. The correct sequence is:
1. Define "dispute entry" in FR-011 (gh-aw's modified P1-2)
2. Then sync SKILL.md to the updated FR-011 (APM's P1-1)

This is a process recommendation, not a spec-text recommendation, but it prevents baking ambiguity into the runtime artifact.

### N-3. Acknowledge the hybrid enforcement model in the template authoring contract
**Priority: P3 (Recommended Improvement)**

APM's cross-review (Tension 1) correctly identifies that the spec currently uses a hybrid of engine-level enforcement (FR-023 validates output, Constraints requires engine filtering) and author-level enforcement (template authoring contract states invariants for template authors). This hybrid is not acknowledged anywhere in the spec. Adding a single sentence to the template authoring contract -- "Engine enforcement (FR-023, FR-028) validates output structure and template eligibility; template authors are responsible for instructional completeness per the invariants below" -- makes the division of responsibility explicit and prevents future contributors from assuming enforcement is purely engine-side or purely author-side.

---

## Position Summary

gh-aw entered this review round with 8 recommendations across three priority tiers. After cross-review:

| # | Recommendation | Original | Revised Status | Reason |
|---|---------------|----------|---------------|--------|
| P1-1 | FR-022/FR-023 disambiguation | Two-tier | **Modified** to three-tier | APM identified the "garbage 200 OK" gap; three tiers close it |
| P1-2 | Define "dispute entry" | Any non-whitespace | **Modified** to exclude HTML comments | APM's false-positive concern is valid; HTML comment exclusion is minimal and targeted |
| P2-3 | FR for draft template filtering | Add FR-028 | **Surviving** | Universal agreement the Constraints MUST needs a testable FR |
| P2-4 | Template instruction for citation boundary | Add to FR-015 | **Surviving** | LLM agents follow prompts, not spec requirements they cannot see |
| P2-5 | Endorsement path specification | Template branching or separate format | **Modified** to contract annotation | APM's "templates are not programs" argument is persuasive |
| P3-6 | Extraction validation warning | Diagnostic on empty extraction | **Surviving** | All three agents flag the gap; warning preserves trigger semantics |
| P3-7 | Draft marker / FR-004 relationship | Document layered defense | **Surviving** | Unchallenged |
| P3-8 | Structured output schema placement | Move to Future Work section | **Modified** to standalone section with SHOULD language | Splits difference between spec-kit's MUST and gh-aw's advisory |
| OB-1 | Directory-based template separation | Prefer `_draft/` directory | **Withdrawn** | APM's distribution model argument is decisive |
| OB-2 | Endorsement as template design problem | Template conditionals | **Withdrawn** | Subsumed by modified P2-5 |
| N-1 | Success criteria for post-conversus FRs | -- | **New (P2)** | spec-kit's finding accepted; gh-aw's silence was an omission |
| N-2 | Sequence SKILL.md sync after dispute-entry def | -- | **New (P1)** | Prevents propagating undefined terms into runtime artifact |
| N-3 | Hybrid enforcement model acknowledgment | -- | **New (P3)** | APM's tension finding warrants explicit documentation |

**Net position**: 4 surviving, 4 modified, 2 withdrawn, 3 new. Total active recommendations: 11.

### Key concessions
- **Directory separation withdrawn**: APM's packaging argument overrides gh-aw's filesystem-location preference. The marker-based approach is correct for a distributable spec.
- **Template branching withdrawn**: APM's "templates are static instruction sets" principle is sound. The endorsement path belongs in the contract, not the template.
- **Three-tier failure model accepted**: APM's identification of the "structurally unintelligible" middle tier is a genuine gap in gh-aw's original two-tier proposal.

### Key positions held
- **Citation boundary in templates (P2-4)**: The arbiter only sees its prompt. FR-024 in the spec is not FR-024 in the template. The enforcement gap is real.
- **Warning over gate for empty extraction (P3-6)**: spec-kit's harder gate would break `trigger: always` semantics. Observability via diagnostics is the correct severity.
- **SHOULD over MUST for deferred schema (modified P3-8)**: No implementation experience exists for the structured output fields. Normative commitment before implementation is premature.
- **Dispute-entry before SKILL.md sync (N-2)**: Process ordering matters. Syncing an ambiguous definition into a runtime artifact compounds the problem.
