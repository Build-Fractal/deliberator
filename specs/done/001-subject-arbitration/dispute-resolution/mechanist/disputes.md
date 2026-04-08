# The Mechanist: Final Disputes

**Agent**: The Mechanist (operational/engine perspective)
**Date**: 2026-03-19
**Stage**: Final disputes after revisions
**Inputs**: Revised positions from all three agents (Mechanist, Pragmatist, Purist)

---

## Remaining Disputes

### Dispute 1: FR-023 grounding-reference check -- MUST vs. SHOULD

All three agents now agree that the engine should perform a string-presence check for the grounding document in the Binding Decisions section. The remaining dispute is normative weight. The Pragmatist and I differ on whether this check is MUST or SHOULD.

The Pragmatist's revised FR-023 uses MUST: "the engine MUST additionally validate that [...] at least one reference to the grounding document path in the Binding Decisions section." The Purist also uses MUST. In my revision, I downgraded the citation heuristic from MUST to SHOULD, on the grounds that the check is heuristic and I had been rightly called out for overstating the engine's determinism. I was being honest about the check's nature.

On reflection, this honesty was misplaced. The check itself -- does the string appear in the section? -- is deterministic. The interpretation of the result is heuristic (presence does not prove authoritative citation). But MUST/SHOULD governs whether the engine performs the check, not whether the check's result is conclusive. A SHOULD on the check means an implementor can skip it entirely and remain compliant. That defeats the purpose. The check should be MUST (the engine always performs it); the warning it emits should be clearly labeled as heuristic (it flags likely violations, not proven ones).

I concede to the Pragmatist and the Purist: MUST for performing the check, with the warning text honestly stating the check's heuristic nature. My revised FR-023 text from the revision already contains the honest warning language. The only change is upgrading SHOULD back to MUST for the check itself.

This dispute is self-resolving. All three agents now converge on MUST.

### Dispute 2: Prose conventions in template guidance -- MAY vs. SHOULD

The Purist's revision introduces SHOULD-level prose conventions back into the deferred section: "Template authors SHOULD design prose to be consistent with these fields and SHOULD use labeled sub-fields (`**Dispute:**`, `**Ruling:**`, `**Changes Required:**`) to improve output regularity." The Pragmatist's revision uses MAY: "Template authors MAY use labeled sub-fields [...] as instructional hints." My revision also uses MAY, keeping prose conventions out of the spec as normative guidance.

The Purist conceded in their revision that they drew "an unprincipled distinction between constraint instructions and formatting instructions" in the original round. Yet the revised text reinstates SHOULD-level formatting instructions in the deferred section. This is the same position the Purist conceded was inconsistent, reintroduced at a different location in the document.

The distinction matters for the reason I identified in my original review and held through revision: SHOULD creates expectations. A template author reading the spec sees SHOULD and treats it as a directive, not an option. When the engine cannot validate compliance with that directive, the SHOULD is an obligation enforced by nothing. MAY communicates the same design intent -- "this is a good idea, you can do it" -- without creating a normative obligation the engine cannot discharge.

The Pragmatist and I agree on MAY. The Purist stands alone on SHOULD. This dispute is narrow (one keyword in one section) but it is the same dispute that drove Blocker 2 through the entire process. The Purist's SHOULD is the last remnant of the prose-convention contract that all three agents spent two rounds arguing about. It should be MAY.

### Dispute 3: Vacuous-output SC -- location and formulation

The Pragmatist identified the vacuous-output gap (arbiter produces structurally valid but substantively empty resolution) and proposed SC-014 to address it. I did not propose this SC in my revision. The Purist addressed it differently: by extending FR-022's failure model with a fourth tier ("arbiter completes but resolves zero disputes") and requiring the final report to distinguish "0 disputes resolved" from "N disputes resolved."

These are three different approaches to the same problem:
- The Pragmatist: a new SC (SC-014) that makes the condition detectable via validation warning.
- The Purist: a structural extension to the failure model (FR-022 tier 4) that makes the condition visible in the report.
- My revision: silent on this gap.

My silence was an error. The Purist's DC-2 in the original round identified this gap, and the Pragmatist correctly identified that it needs an addressable artifact in the spec. The question is where it belongs.

The Pragmatist's SC-014 is an acceptance criterion -- it defines what "correct engine behavior" looks like when the arbiter produces zero binding decisions. The Purist's FR-022 tier 4 is a failure-model extension -- it defines a new category of outcome. Both are needed. The failure model should categorize the outcome; the SC should define how the engine responds to it. The Pragmatist's SC-014 formulation ("emits a validation warning: 'Arbitration produced zero binding decisions -- verify dispute trigger content'") is the right engine behavior. The Purist's report-level distinction ("0 disputes resolved" vs. "N disputes resolved") is the right user-facing artifact. Both should be included.

I adopt the Pragmatist's SC-014 and the Purist's report-level distinction as complementary. This dispute is resolvable by inclusion of both.

---

## Convergence

### Convergence 1: All four blockers have a majority or unanimous resolution

| Blocker | Mechanist | Pragmatist | Purist | Result |
|---------|-----------|------------|--------|--------|
| 1: Dispute entry definition | Option B | Option B | Option B (revised from A) | **Unanimous: Option B** |
| 2: Structured output | Option A (headings only) | Option A (revised from B) | Option A core + SHOULD conventions | **Majority: Option A headings-only** |
| 3: Success criteria priority | P1 | P1 | P1 | **Unanimous: P1** |
| 4: Citation enforcement surface | Option C | Option C | Option C | **Unanimous: Option C** |

Every blocker that entered this process with a 2:1 or 3-way split has converged to at least a 2:1 majority. Blocker 1 moved from 2:1 (Mechanist + Pragmatist vs. Purist) to 3:0 after the Purist conceded that pattern-match optimizes for the wrong failure mode. Blocker 2 moved from a 3-way split to 2:1 (Mechanist + Pragmatist on headings-only MAY guidance vs. Purist on headings-only with SHOULD guidance). Blockers 3 and 4 were unanimous from the start and remain so.

### Convergence 2: The heuristic/deterministic distinction is shared vocabulary

All three agents now distinguish between what the engine can check deterministically (section headings, string presence, file existence, exit codes) and what requires heuristic or human review (citation authority, ruling quality, semantic completeness). This distinction was not shared at the start of the process. The Purist originally proposed SCs that depended on sub-field parsing and conceded the inconsistency. The Pragmatist originally weighted enforcement toward the template and conceded that deferring deterministic checks was negligent. I originally overclaimed that engine citation validation was deterministic and conceded it was heuristic.

The shared vocabulary is: **deterministic checks belong at MUST level in the engine; heuristic checks belong at SHOULD level with honest labeling; semantic analysis is deferred to v2.** All three revisions reflect this hierarchy.

### Convergence 3: Template and engine are co-load-bearing for different failure classes

My original position was that the engine is "the only surface that matters for correctness." The Pragmatist's original position was that the template is the primary enforcement surface. Both positions were wrong in their exclusivity.

All three revisions now converge on the same model: the template is the primary *prevention* mechanism (it shapes the LLM's output distribution at generation time), and the engine is the primary *detection* mechanism (it catches violations after the fact). Neither is sufficient alone. The template cannot guarantee compliance. The engine cannot prevent violations. Prevention and detection are different functions requiring different actors.

This convergence is the most substantive outcome of the dispute process. It replaces the original question ("which surface should enforcement be weighted toward?") with a functional decomposition ("which surface handles which failure class?") that all three agents accept.

### Convergence 4: The deferred structured-output section is a standalone spec section with advisory schema

All three agents agree on the following: (a) the deferred schema fields belong in a standalone section, not scattered across Implementation Guidance; (b) the schema is advisory for v1; (c) the section should communicate intent for v2 planning; (d) the six schema fields (dispute_id, ruling_type, grounding_citation, required_changes, affected_target_files, confidence_level) are the right fields. The remaining dispute is limited to SHOULD vs. MAY for template-author guidance and whether the transition trigger is a process note or an activation condition. The architectural decision -- standalone section, advisory status, six fields -- is settled.

### Convergence 5: SC format and scope

All three agents converge on: (a) P1 classification; (b) Given/When/Then or equivalent testable format; (c) observable outputs (stderr, file presence/absence, report content) rather than internal engine state; (d) coverage of FR-022 through FR-027. The Pragmatist's seven SCs (including SC-014 for vacuous output) represent the most complete set. The Purist's six SCs and my six SCs overlap substantially. The merge path is clear: adopt the Pragmatist's SC-014 into whichever agent's SC numbering the arbiter selects, retain Given/When/Then format, and specify observable output channels.

---

## Final Position Statement

The dispute resolution process worked. It exposed two genuine defects in my original review (overclaiming engine determinism on citation validation, inconsistency between Blocker 2 prose-convention rejection and Blocker 4 prose-semantic validation) and forced me to articulate a more honest version of the mechanist position.

The honest mechanist position is this: **the engine is the most reliable actor in the system, but its reliability is not uniform across check types.** String-presence checks (heading validation, grounding-path detection) are deterministic and belong at MUST level. Semantic checks (citation authority, ruling quality) are heuristic at best and belong at SHOULD level with explicit labeling. The spec should reflect this variance rather than treating all engine checks as equally authoritative or dismissing all of them as equally unreliable.

The four blockers resolve as follows:

**Blocker 1** is resolved. Unanimous Option B. Content-negative primary trigger with pattern-match fallback. The two mechanisms test different things, providing genuine defense-in-depth. FR-012's cost asymmetry (false positives are cheaper than false negatives) is the governing design value.

**Blocker 2** is resolved at the architectural level with one narrow keyword dispute remaining. Headings-only for v1. Advisory schema in a standalone deferred section. The Purist's SHOULD for template-author prose conventions should be MAY, for the reason that has been consistent throughout: the engine cannot validate prose conventions, and normative language the engine cannot validate creates obligations enforced by nothing. MAY communicates the same design intent without the false contract.

**Blocker 3** is resolved. Unanimous P1. The SC set should be the Pragmatist's seven (SC-008 through SC-014), in Given/When/Then format, specifying observable outputs. SC-014 (vacuous-output detection) closes the gap the Purist identified in the original round. SC-010 (grounding-reference presence) is a string-presence check, not semantic parsing, and is implementable in v1.

**Blocker 4** is resolved. Unanimous Option C. Template for prevention, engine for detection, spec for normative definition. FR-023 amended to include MUST-level grounding-path string-presence check with honestly labeled heuristic warning. Semantic citation-source analysis deferred to v2.

The remaining disputes (MUST vs. SHOULD on the grounding check, MAY vs. SHOULD on template conventions, vacuous-output SC formulation) are narrow refinements within settled architectural decisions. None blocks implementation. All are resolvable by the arbiter without revisiting the architectural choices that the three-agent process has converged on.
