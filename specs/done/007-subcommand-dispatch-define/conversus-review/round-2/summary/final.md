# Neutral Synthesis: 007-subcommand-dispatch-define (Round 2)

**Synthesizer**: neutral (no agent affiliation)
**Date**: 2026-03-22
**Deliberation mode**: cooperative
**Agents**: functional-typing, integration-architect, devils-advocate
**Round**: 2 of 2 (final)

---

## Process Summary

Round 2 built on the Round 1 synthesis (13 convergence points, 5 disputes, 14 actionable changes) and the arbiter's advisory opinions on all 5 disputes. The three agents engaged the arbiter's operational grounding to resolve or narrow every remaining dispute from Round 1. The result is a substantially converged deliberation with 19 consensus items and 3 narrow residual disagreements on priority assignment and prose precision.

**Phase 1 (Reviews)**: All three agents reaffirmed the 13 Round 1 convergence points without reversal and confirmed that all 12 functional requirements (FR-001 through FR-012) remain correctly implemented. Functional-typing conceded on RD-1 (`## Status`) and RD-2 (shared validation), adopting the arbiter's factual-annotation and schema-layer-contract framings. Devils-advocate accepted deferral on RD-3 (multi-path `--context`) and RD-4 (`--force`/`--dry-run`), reversing two of its Round 1 positions. Integration-architect maintained all positions and concessions from Round 1 without reversal. All three agents identified new missed opportunities: functional-typing found the heading-count inconsistency between Change 1 and Change 10, integration-architect raised `problem.md`/`conversus.yml` artifact independence, and devils-advocate identified write-failure error handling and interactive-mode vague-input behavior.

**Phase 2 (Cross-reviews)**: The most consequential cross-review finding was functional-typing's identification that integration-architect's advocacy for `## Status` as a "fact" was inconsistent with a four-rule refine contract that does not maintain that fact across refine operations (functional-typing cross-review of integration-architect, DC-2). This forced integration-architect to accept a fifth refine invariant. Additionally, integration-architect's DC-2 on functional-typing's review corrected the `## Status` placement from between `# Problem Definition` and `## Decision` to end-of-schema, grounded in the non-expert user principle. Functional-typing's DC-1 on devils-advocate's review identified that stricter validation semantics for `problem.md` would conflict with Phase 6's established case-insensitive, level-agnostic model at SKILL.md L659. Both integration-architect and functional-typing flagged devils-advocate's "bridge that nothing walks across" language as contradicting the stated concession on RD-1.

**Phase 3 (Revisions)**: Functional-typing withdrew the between-title-and-decision placement for `## Status` and adopted end-of-schema placement. Functional-typing also revised the heading-count language from hardcoded "8" to "all headings defined in the schema block" to avoid coupling between recommendations. Devils-advocate fully withdrew the "bridge" rhetoric on `## Status`, downgraded validation precision from P1 to P2 and withdrew the "amendment to C-1" framing, accepted the one-word write-failure fix over a multi-sentence specification, downgraded interactive-mode guidance from P2 to P3, and withdrew the P2 elevation for Change 14. Integration-architect accepted the fifth refine invariant (Status re-evaluation), settled `## Status` priority at P2, accepted devils-advocate's framing for single-path `--context` documentation, and accepted validation precision as a new P2 item rather than a P1 amendment.

**Phase 4 (Disputes)**: Three disputes remain, all narrow: `## Status` priority (P1 vs P2, with 2-1 favoring P2), validation matching semantics (Phase 6 precedent vs handler-controlled strict matching), and the distinction between testable invariants and process obligations in the refine contract. A fourth item -- synthesis framing of `## Status` as explicitly deferred rather than solved -- is effectively settled with 2 of 3 reviewers agreeing on the language.

---

## Recommendation Scorecard

| ID | Recommendation | functional-typing | integration-architect | devils-advocate | Consensus Priority |
|----|---------------|-------------------|----------------------|-----------------|-------------------|
| R1 | Post-write schema validation for `problem.md` | P1 (reaffirmed) | P1 (reaffirmed) | P1 (reaffirmed) | **P1 -- unanimous** |
| R2 | `--context` path validation before ingestion | P1 (reaffirmed) | P1 (reaffirmed) | P1 (reaffirmed) | **P1 -- unanimous** |
| R3 | Dispatch matching: exact, case-sensitive, exhaustive | P1 (reaffirmed) | P1 (reaffirmed) | P1 (reaffirmed) | **P1 -- unanimous** |
| R4 | Single-agent execution model statement | P2 (reaffirmed) | P2 (reaffirmed) | P2 (reaffirmed) | **P2 -- unanimous** |
| R5 | Empty-section `[CLARIFY:]` coverage | P2 (reaffirmed) | P2 (reaffirmed) | P2 (reaffirmed) | **P2 -- unanimous** |
| R6 | `--output` directory creation semantics | P2 (reaffirmed) | P2 (reaffirmed) | P2 (reaffirmed) | **P2 -- unanimous** |
| R7 | Five-rule refine contract (expanded from four) | P2 (reaffirmed, fifth invariant added) | P2 (accepted fifth invariant) | P2 (accepted fifth invariant) | **P2 -- unanimous** |
| R8 | Taxonomy closure design note | P2 (reaffirmed) | P2 (reaffirmed) | P2 (reaffirmed) | **P2 -- unanimous** |
| R9 | Pipeline overview scaled to single sentence | P2 (reaffirmed) | P2 (reaffirmed) | P2 (reaffirmed) | **P2 -- unanimous** |
| R10 | `## Status` section as factual annotation | P2 (conceded, conditional) | P2 (settled) | P1 (minority) | **P2 -- majority (2-1)** |
| R11 | Report section gated on write success | P2 (accepted one-word fix) | P2 (proposed one-word fix) | P2 (accepted one-word fix) | **P2 -- unanimous** |
| R12 | Validation precision prose (matching semantics) | neutral (defers to schema) | P2 (strict matching) | P2 (Phase 6 precedent) | **P2 -- consensus on substance, disputed on semantics** |
| R13 | Single `--context` path documented as scoping decision | P3 (reaffirmed) | P3 (framing adjusted) | P3 (accepted deferral) | **P3 -- unanimous** |
| R14 | Acknowledge frontmatter change in spec | P3 (reaffirmed) | P3 (reaffirmed) | P3 (reaffirmed) | **P3 -- uncontested** |
| R15 | `--force`/`--dry-run` as future consideration | P3 (reaffirmed) | P3 (reaffirmed) | P3 (accepted deferral) | **P3 -- unanimous** |
| R16 | Shared validation as architectural direction, co-located | P3 (reaffirmed, co-location endorsed) | P3 (co-location accepted) | P3 (withdrew P2 elevation) | **P3 -- unanimous** |
| R17 | `problem.md`/`conversus.yml` artifact independence | not raised | P3 (new, single-round) | P3 (endorsed) | **P3 -- consensus, single-round** |
| R18 | Interactive-mode `[CLARIFY:]` cross-reference | not raised | not raised | P3 (downgraded from P2) | **P3 -- uncontested** |
| R19 | spec.md schema block update if `## Status` adopted | P3 (reaffirmed, illustrative only) | not addressed | not addressed | **P3 -- single advocate** |

---

## Dangerous Contradictions Found

### DC-1: Validation matching semantics -- two models in one SKILL.md (Round 2 only)

Phase 6's heading validation at SKILL.md L659 uses case-insensitive, level-agnostic matching. Integration-architect's NR-1 proposes case-sensitive, `##`-level matching for the define handler's post-write validation. If both models coexist in SKILL.md, a future spec author faces a design conflict about which to use. Functional-typing identified this in cross-review of devils-advocate (DC-1), and devils-advocate conceded by aligning with the Phase 6 precedent.

Integration-architect's defense -- that the define handler validates its own output (controlled authorship) while Phase 6 validates uncontrolled arbiter output -- is architecturally coherent but creates two validation conventions in the same file without explicit justification. Devils-advocate's position -- follow the established precedent and let a future spec introduce a stricter model with explicit rationale -- is the conservative default.

**Traced to**: functional-typing cross-review of devils-advocate DC-1 (SKILL.md L659 vs Rec-2); devils-advocate revision Rec-2 (L29-41, conceded to Phase 6 precedent); integration-architect revision NR-1 (L144-153, maintains strict matching); integration-architect disputes RD-2 (acknowledges both options are defensible).

### DC-2: `## Status` as factual annotation -- complete resolution vs explicit deferral framing

The three agents agree on the mechanism (factual annotation, no consumer prescriptions). The contradiction is in what the synthesis should *say* about the outcome. Integration-architect and devils-advocate both explicitly state the synthesis must label `## Status` as "producer-side annotation with enforcement deferred to spec 008" (integration-architect revision L92-93; devils-advocate disputes RD-3). Functional-typing does not contest this framing but does not explicitly endorse it either. The danger: presenting `## Status` as a completed quality-checkpoint solution when the enforcement chain is explicitly incomplete. This is a framing obligation for the synthesis, not a spec-level contradiction.

**Traced to**: devils-advocate revision Rec-1 (L17-19, full concession); integration-architect revision R10 (L92-93, deferral framing agreed); devils-advocate disputes RD-3 (L40-50, effectively settled).

---

## Systemic Contradictions

### SC-1: Spec 007's dual identity (carried from Round 1, managed via bridge mechanisms)

The Round 1 synthesis identified this tension: spec 007 simultaneously claims to be foundational (spec.md L6) and scoped (spec.md L13). Round 2 managed this through two bridge mechanisms: the `## Status` section (which makes the define handler's output self-documenting for future consumers) and the prose validation contract (which names the obligation for future readers of `problem.md` without mandating infrastructure). The arbiter called this "real but manageable." All three agents accepted this characterization in Round 2. The tension persists as an architectural property of the spec but is no longer an active dispute.

**Traced to**: Round 1 synthesis SC-1; arbiter resolution Point 5 ("the `## Status` section and the validation contract are the minimal bridge"); all three Round 2 reviews (alignment sections reaffirming this is manageable).

### SC-2: Validation precision increasing toward prose insufficiency

Devils-advocate's cross-review of functional-typing (T-3) observed that the validation specification -- heading count, matching semantics, content-presence rules -- is growing complex enough that "one-sentence prose contract" may no longer adequately describe it. The agents produced an expanded heading list (7 or 8 headings depending on `## Status`), matching-semantics requirements (case-sensitive or not, level-specific or not), and content-presence rules (`[CLARIFY:]` handling for empty sections). Together these constitute a multi-clause validation specification embedded in prose. No agent proposes crossing the line to a structured rule set in spec 007, but the accumulation is noted as a systemic trend that future specs should monitor.

**Traced to**: devils-advocate cross-review of functional-typing T-3 (L50-56); functional-typing revision Rec #1 (schema-as-source-of-truth); integration-architect revision NR-1 (matching semantics as prose).

---

## Convergence Achieved

The following items reached genuine consensus across all three agents in Round 2. Items C-1 through C-13 from Round 1 are reaffirmed without modification and are listed here with their Round 2 status. New consensus items from Round 2 are noted explicitly.

### C-1: Post-write schema validation for `problem.md` (P1 -- unanimous, both rounds)

The define handler must validate that `problem.md` contains all required headings as defined in the schema block after writing. If any heading is missing, add it with a `[CLARIFY:]` placeholder and re-write. Warn the user: "Added missing section: {heading}." The heading list is derived from the schema (SKILL.md L822-850), not hardcoded -- if the schema gains or loses a heading, the validation adapts automatically. If `## Status` is adopted, it joins the heading list.

**Traced to**: all three Phase 1 reviews (reaffirmed); functional-typing revision Rec #1 (schema-as-source-of-truth for count); integration-architect revision R1 (heading count updated if Status adopted); all three disputes files (confirmed unanimous).

### C-2: `--context` path validation before ingestion (P1 -- unanimous, both rounds)

Fail with "Context path does not exist: {path}" if the path does not exist. Warn "No .md files found in context directory: {path}" if the path is a directory containing no markdown files, and proceed without context. Mirrors the `run` handler's validation at SKILL.md L195-196. The strongest consensus item in the deliberation -- not challenged in any phase of either round.

**Traced to**: all three Phase 1 reviews (reaffirmed); all three disputes files (confirmed unanimous).

### C-3: Dispatch matching is exact and case-sensitive (P1 -- unanimous, both rounds)

Subcommand matching is exact and case-sensitive. The dispatch table is exhaustive. Any first argument that does not exactly match a known subcommand triggers the unknown-subcommand error, enhanced with: "Did you mean: `/conversus run {cmd}`?" Functional-typing's fallback-to-`run` proposal was withdrawn in Round 1 and never revisited.

**Traced to**: all three Phase 1 reviews (reaffirmed); all three disputes files (confirmed unanimous).

### C-4: `define` runs in main conversation, no subagents (P2 -- unanimous, both rounds)

Wording: "In this version, the define command executes entirely in the main conversation. No subagents are launched." The "In this version" scoping permits future evolution.

**Traced to**: all three Phase 1 reviews (reaffirmed); all three disputes files (confirmed P2 uncontested).

### C-5: Empty-section `[CLARIFY:]` coverage for Constraints and Success Criteria (P2 -- unanimous, both rounds)

If no constraints can be determined, the Constraints section must contain a `[CLARIFY:]` placeholder. Same for Success Criteria. This extends SKILL.md L854's existing rule uniformly.

**Traced to**: all three Phase 1 reviews (reaffirmed); all three disputes files (confirmed P2 uncontested).

### C-6: `--output` directory creation semantics (P2 -- unanimous, both rounds)

Create the output directory (including intermediates) if it does not exist. Fail with "Cannot create output directory: {path}" on failure.

**Traced to**: all three Phase 1 reviews (reaffirmed); all three disputes files (confirmed P2 uncontested).

### C-7: Five-rule refine contract (P2 -- unanimous, expanded in Round 2)

**New in Round 2**: The refine contract expanded from four to five invariants. Functional-typing proposed the fifth invariant (Status re-evaluation); integration-architect and devils-advocate accepted it. The contract is:

(a) All required headings must be present in the refined output.
(b) Existing content must not be silently deleted -- it may be revised, extended, or consolidated but not dropped without replacement.
(c) Source Documents must union old and new paths.
(d) Type must be re-evaluated against the combined input.
(e) Status must be re-evaluated based on `[CLARIFY:]` tag count in the refined output.

The diff summary ("Added 2 constraints, updated Context, Type unchanged") is recommended practice (lowercase "should"), not a structural invariant. The refined `problem.md` must pass the same post-write schema validation as a fresh definition.

Rule (e) is a mechanical consequence of adopting `## Status` (C-10). If `## Status` is not adopted, the contract reverts to four invariants.

**Traced to**: functional-typing review MO-2 (L107-111, fifth invariant proposed); integration-architect revision R7 (L54-66, accepted); devils-advocate revision Rec-8 (L111-123, accepted); all three disputes files (confirmed five-rule contract).

### C-8: Taxonomy closure design note (P2 -- unanimous, both rounds)

"This taxonomy is intentionally closed. Each type maps to a specific mode in `/conversus interests`. Extending this taxonomy requires a companion update to the mode mapping in spec 008."

**Traced to**: all three Phase 1 reviews (reaffirmed); all three disputes files (confirmed P2 uncontested).

### C-9: Pipeline overview as single sentence (P2 -- unanimous, both rounds)

"Next step: `/conversus interests` (not yet implemented -- this is the first of a series of guided setup commands)."

**Traced to**: all three Phase 1 reviews (reaffirmed); all three disputes files (confirmed P2 uncontested).

### C-10: `## Status` section as factual annotation (P2 -- majority on priority, unanimous on substance)

**New in Round 2**: The Round 1 dispute (RD-1) is resolved. Functional-typing conceded after the arbiter reframed the field as a factual annotation rather than an advisory marker or a gate directive. Devils-advocate withdrew the "bridge that nothing walks across" rhetoric and the RFC 2119 SHOULD language. All three agents now accept:

- The `## Status` section is a factual annotation reporting the artifact's completeness state.
- The define handler sets `status: draft` when any `[CLARIFY:]` tag is present, and `status: ready` when none are present.
- The section is placed after `## Source Documents` as the final section in the schema. (Functional-typing's original between-title-and-decision placement was withdrawn after integration-architect's UX critique.)
- Spec 007 does not prescribe what consumers do with this field. Enforcement is explicitly deferred to spec 008.
- No RFC 2119 SHOULD language governs downstream behavior.

**Priority**: P2 by majority (integration-architect and functional-typing). Devils-advocate holds P1 as a minority position but concedes the P2 outcome. The 2-1 split reflects different views on whether a non-FR metadata enhancement belongs in the same priority tier as foundational structural changes.

**Note**: This is a producer-side annotation. The quality checkpoint it enables is not operational until spec 008 defines consumer behavior for the `draft`/`ready` status. The synthesis labels this as an explicit, accepted deferral -- not a completed solution to the quality-checkpoint concern. Integration-architect and devils-advocate both explicitly requested this framing (integration-architect revision L92-93; devils-advocate disputes RD-3).

**Traced to**: functional-typing review RD-1 (L52-63, concession); integration-architect review RD-1 (L51-63, maintained); devils-advocate review OBA-1 (L76-86, accepted with caveats); devils-advocate revision Rec-1 (L13-22, full concession of "bridge" rhetoric); all three disputes files (confirmed substance unanimous, priority 2-1).

### C-11: Report section gated on write success (P2 -- unanimous, new in Round 2)

Change SKILL.md L858 from "After writing `problem.md`, print:" to "After successfully writing `problem.md`, print:". A one-word edit that closes an unguarded path where the Report section could run against a non-existent artifact.

**Traced to**: devils-advocate review MO-1 (L52-58, identified gap); integration-architect cross-review of devils-advocate T-1 (L39-48, proposed one-word fix); functional-typing revision New Rec #1 (L119-125, accepted); devils-advocate revision Rec-3 (L45-56, adopted one-word formulation); all three disputes files (confirmed unanimous P2).

### C-12: Single `--context` path documented as scoping decision (P3 -- unanimous)

Documentation language: "Single-path is a scoping decision for spec 007. Directory support provides a pragmatic multi-source mechanism. A follow-up spec may introduce multi-path syntax with explicit ordering and conflict semantics." Devils-advocate's deferral in Round 2 resolved the Round 1 dispute (RD-3). Integration-architect accepted devils-advocate's documentation framing, withdrawing the "deliberate design" characterization (integration-architect revision R11, L100-106).

**Traced to**: devils-advocate review (L43-44, accepted deferral); integration-architect revision R11 (L100-106, framing adjusted); functional-typing (held deferral from Round 1).

### C-13: `--force`/`--dry-run` as future consideration (P3 -- unanimous)

"Future consideration: `--force` (overwrite without interactive prompt) and `--dry-run` (preview output without writing) flags may be added in a future spec to support non-interactive and automated invocations." Devils-advocate's deferral in Round 2 resolved the Round 1 dispute (RD-4).

**Traced to**: devils-advocate review (L46-47, accepted deferral); all three disputes files (confirmed unanimous).

### C-14: Shared validation as architectural direction, co-located with schema (P3 -- unanimous)

All three agents agree: the architectural note about future consumers applying the same heading validation is P3 and should be co-located with the post-write validation text for discoverability. Devils-advocate withdrew the P2 elevation after both other agents correctly identified the conflation of discoverability (a placement concern) with priority (an implementation urgency signal).

**Traced to**: devils-advocate revision Rec-5 (L73-83, withdrew P2); functional-typing revision Rec #6 (L103-113, held P3 with co-location); integration-architect revision R14 (L122-128, P3 with co-location).

### C-15: `problem.md`/`conversus.yml` artifact independence (P3 -- consensus, single-round)

A single sentence noting that `problem.md` (guided workflow) and `conversus.yml` (direct execution) are independent artifacts for different workflow paths. The define handler does not read, modify, or depend on an existing `conversus.yml`. This is single-round material (introduced by integration-architect in Round 2) and weighted accordingly, but both other agents endorsed it.

**Traced to**: integration-architect review MO-2 (L142-147); devils-advocate cross-review SA-6 (L95-97, endorsed); functional-typing cross-review T-2 (L51-58, accepted as valid, noted single-round).

### C-16: Interactive-mode `[CLARIFY:]` cross-reference (P3 -- consensus)

A cross-reference in the interactive input section (SKILL.md L779-782) noting: "The ambiguity handling rule applies equally to interactive input -- vague or empty responses produce `[CLARIFY:]` tags, not speculative content." Devils-advocate originally proposed this at P2; both other agents argued the universal MUST at SKILL.md L852 already covers it. Devils-advocate downgraded to P3 and accepted the cross-reference form over a restated obligation.

**Traced to**: devils-advocate review MO-2 (L62-70); functional-typing cross-review T-2 (L45-51, already covered by L852); integration-architect cross-review T-2 (L51-59, P3 at most); devils-advocate revision Rec-4 (L59-69, downgraded to P3).

### C-17: spec.md schema block update if `## Status` adopted (P3 -- single advocate)

If `## Status` is adopted, the illustrative schema at spec.md L45-71 should include `## Status` for consistency with SKILL.md. This is an illustrative update, not an FR-009 expansion. FR-009's named sections (spec.md L38) remain unchanged.

**Traced to**: functional-typing review MO-3 (L113-115); functional-typing revision Rec #5 (L88-99, clarified as illustrative, not FR expansion).

### C-18: FR coverage is complete and unchanged

All 12 functional requirements (FR-001 through FR-012) are correctly implemented in SKILL.md. No reviewer in either round disputed any FR implementation. Adding `## Status` does not change FR-009; it is a non-FR schema enhancement. This is the strongest consensus position in the deliberation.

**Traced to**: functional-typing review (L31-46, full FR mapping); all three disputes files (confirmed FR coverage complete).

---

## Arbiter-Resolved Disputes (from Round 1)

The arbiter's advisory opinions on the five Round 1 disputes were engaged by all three agents in Round 2. The following summarizes how each dispute was resolved, tracing the arbiter's influence.

### RD-1 (Round 1): `[CLARIFY:]` tags -- advisory vs. `## Status` section

**Arbiter's contribution**: Reframed `## Status` as neither advisory nor binding but *descriptive* -- a measurable property of the artifact. Grounded in SKILL.md L865 (count already computed) and spec.md L87 (non-expert user principle).

**Resolution**: All three agents adopted the factual-annotation framing. Functional-typing conceded (review L56-63). Devils-advocate withdrew SHOULD language and eventually the "bridge" rhetoric (revision L17-19). The arbiter's reframing was the decisive factor in resolving this dispute.

### RD-2 (Round 1): Shared validation function

**Arbiter's contribution**: Proposed a prose validation contract at the schema layer, not the dispatch layer. One sentence, no code, no new section. Distinguished between mandating a function (premature) and naming an obligation (necessary).

**Resolution**: All three agents adopted the schema-layer approach. Functional-typing conceded (review L65-71). Devils-advocate withdrew the dispatch-layer utilities proposal (revision Rec-5 L73-83). The arbiter's distinction between routing and validation settled the architectural question.

### RD-3 (Round 1): Multi-path `--context`

**Arbiter's contribution**: Grounded the single-path constraint in design intent: SKILL.md L797's directory support is the multi-source mechanism, not a workaround. Enumerated interaction semantics (ordering, deduplication, conflict resolution) that multi-path would require without FR guidance.

**Resolution**: Devils-advocate accepted deferral (review L43-44). The arbiter's enumeration of unaddressed interaction semantics was persuasive where the 2-1 majority alone was not.

### RD-4 (Round 1): `--force` and `--dry-run` flags

**Arbiter's contribution**: Grounded deferral in FR-011's interactive safeguard and the non-expert user principle. Noted that `--dry-run` is unnecessary in an interactive context.

**Resolution**: Devils-advocate accepted deferral (review L46-47). The arbiter's observation about `--dry-run` redundancy in interactive contexts was a new argument that strengthened the majority position.

### RD-5 (Round 1): Refine semantics -- minimal contract depth

**Arbiter's contribution**: Confirmed the four rules as "structural invariants I can reliably enforce." Distinguished between normative post-conditions and the diff summary as recommended practice.

**Resolution**: All three agents adopted the four-rule contract (now expanded to five with Status re-evaluation). The arbiter's normative-vs-recommended distinction resolved the classification dispute between structural invariants and UX guidance.

---

## Remaining Disputes

DISPUTES_BEGIN

### RD-1 (Round 2): `## Status` priority -- P1 vs P2

**Positions**:
- **devils-advocate** (P1): The field is the only element making the artifact's completeness state machine-readable. The Report section already computes the data. Writing it into the file costs one line. P1 reflects functional importance, not just dispute history. (devils-advocate disputes RD-1, L14-22)
- **integration-architect** (P2): P1 should be reserved for the foundational structural changes (validation, path checking, dispatch matching) that were unanimous from Round 1. A formerly-disputed metadata field should not be placed alongside them. (integration-architect disputes RD-1, L10-18)
- **functional-typing** (P2): The field is not in FR-009. P1 should be reserved for items that directly implement functional requirements or prevent specification ambiguity. (functional-typing disputes RD-1, L11-19)

**Synthesis assessment**: The 2-1 split favors P2. Devils-advocate concedes the P2 outcome will stand (devils-advocate disputes RD-1, L22). This dispute is resolved at P2. The priority assignment affects implementation ordering, not the content of the spec changes.

### RD-2 (Round 2): Validation matching semantics -- Phase 6 precedent vs handler-controlled precision

**Positions**:
- **devils-advocate** (Phase 6 precedent): Follow the existing case-insensitive, level-agnostic model at SKILL.md L659 for consistency. Two incompatible validation models in the same file is an internal inconsistency. Let a future spec introduce a stricter model with explicit rationale. (devils-advocate revision Rec-2, L29-41; devils-advocate disputes RD-2, L26-36)
- **integration-architect** (strict matching): The define handler validates its own output. Case-sensitive, `##`-level matching is natural for a handler that is both author and validator. The only way validation fails is if the handler's own write logic is buggy, which is exactly what the check should catch. (integration-architect revision NR-1, L144-153; integration-architect disputes RD-2, L22-41)
- **functional-typing** (neutral): The validation should reference "all headings defined in the schema block." Either matching model is compatible with this formulation. Leans toward Phase 6 precedent for internal consistency but considers either choice low-risk since the define handler controls its own output. (functional-typing disputes RD-3, L41-53)

**Synthesis assessment**: Both positions are architecturally defensible. The Phase 6 precedent offers internal consistency; strict matching offers precision for controlled output. Given that (a) functional-typing leans toward Phase 6 precedent, (b) devils-advocate explicitly conceded to Phase 6 precedent, (c) integration-architect acknowledges both options are defensible and will not contest the synthesizer's decision, and (d) the define handler controls its own output (making the matching model a low-risk choice either way), the synthesis adopts the Phase 6 precedent as the default model with a note that a future spec may introduce a stricter model for handler-controlled output. This preserves internal consistency within SKILL.md and follows the conservative-default principle the deliberation has applied throughout (e.g., deferring multi-path, deferring `--force`/`--dry-run`).

### RD-3 (Round 2): Refine invariant classification -- testable structural check vs process obligation

**Positions**:
- **devils-advocate** (annotate in prose): Rules (a)-(c) and (e) are structurally testable by diffing artifacts and counting tags. Rule (d) is a process obligation -- if the type does not change, there is no way to verify whether the handler re-evaluated or copied. The spec prose should note this distinction. (devils-advocate revision Rec-8, L121; devils-advocate disputes RD-2 is adjacent but distinct)
- **integration-architect** (acknowledge without prose): Accepts the distinction as a valid methodological observation but does not request spec prose. (integration-architect revision R7, L60)
- **functional-typing** (optional, P3 at most): Does not oppose a brief note but does not advocate for it as a required change. The spec should state the five invariants; classification is a concern for a future spec's test harness. (functional-typing disputes RD-4, L57-67)

**Synthesis assessment**: The distinction is real but does not affect the normative status of the five-rule contract. All three agents agree on the five rules. The classification observation is worth preserving as a parenthetical note in the spec prose for implementers, consistent with devils-advocate's request and functional-typing's tolerance. This is a P3 addition subordinate to the five-rule contract itself.

DISPUTES_END

---

## Actionable Spec Changes

These are the primary deliverables of this synthesis, ordered by priority. Each change traces to specific Round 2 deliberation artifacts and is supported by consensus or majority position. Changes from Round 1 are updated to reflect Round 2 refinements.

### P1 Changes (must be adopted)

**Change 1: Add post-write schema validation for `problem.md`**

Add after the schema block in the define handler Output section (SKILL.md, after the schema at approximately L850):

> After writing `problem.md`, validate that the file contains all required headings as defined in the schema above. If any heading is missing, add it with a `[CLARIFY: ...]` placeholder and re-write the file. Warn the user: "Added missing section: {heading}."
>
> The heading list is derived from the schema block -- if the schema gains or loses a section, the validation adapts automatically.

*Round 2 refinement*: The heading list references the schema rather than a hardcoded count, per functional-typing revision Rec #1 (L25). This eliminates coupling between Change 1 and Change 10.

*Traced to*: C-1. Unanimous P1, both rounds.

**Change 2: Add `--context` path validation to the define handler**

Add to Context Ingestion in the define handler (SKILL.md, after the path resolution step at approximately L797):

> If the `--context` path does not exist, fail with: "Context path does not exist: {path}". If the path is a directory containing no `.md` files, warn: "No .md files found in context directory: {path}" and proceed without context.

*No Round 2 changes*.

*Traced to*: C-2. Unanimous P1, both rounds.

**Change 3: Add explicit dispatch matching semantics**

Add after the dispatch table (SKILL.md, after approximately L27):

> Subcommand matching is exact and case-sensitive. The dispatch table is exhaustive. Any first argument that does not exactly match a known subcommand triggers the unknown-subcommand error. To pass a config file to the run handler, use the explicit form: `/conversus run <config-path>`.

Enhance the error message at L31-32:

> Unknown subcommand: '{cmd}'. Available commands: run, define. (Future: interests, mode, converge, arbitrate, gate). Did you mean: `/conversus run {cmd}`?

*No Round 2 changes*.

*Traced to*: C-3. Unanimous P1, both rounds.

### P2 Changes (should be adopted)

**Change 4: Add single-agent execution model statement**

Add after the Define: Problem Definition heading (SKILL.md, after approximately L771):

> In this version, the define command executes entirely in the main conversation. No subagents are launched.

*No Round 2 changes*.

*Traced to*: C-4. Unanimous P2, both rounds.

**Change 5: Extend empty-section `[CLARIFY:]` coverage**

Extend the empty-section handling rules (SKILL.md, at approximately L854):

> If no constraints can be determined from the input, the Constraints section must contain: `- [CLARIFY: No constraints identified. What requirements or limitations apply?]`. If no success criteria can be determined, the Success Criteria section must contain: `[CLARIFY: What does a successful outcome look like?]`.

*No Round 2 changes*.

*Traced to*: C-5. Unanimous P2, both rounds.

**Change 6: Specify `--output` directory creation semantics**

Add to the Output section of the define handler (SKILL.md, after approximately L822):

> If the output directory does not exist, create it (including intermediate directories). If creation fails, fail with: "Cannot create output directory: {path}".

*No Round 2 changes*.

*Traced to*: C-6. Unanimous P2, both rounds.

**Change 7: Add five-rule refine contract (expanded from four)**

Expand the refine step in the define handler (SKILL.md, at approximately L791):

> Refine merges the new input with the existing `problem.md`. The following invariants apply:
>
> (a) All required headings (as defined in the schema) must be present in the refined output.
> (b) Existing content must not be silently deleted -- it may be revised, extended, or consolidated but not dropped without replacement.
> (c) Source Documents must union old and new paths.
> (d) Type must be re-evaluated against the combined input.
> (e) Status must be re-evaluated based on `[CLARIFY:]` tag count in the refined output.
>
> Within these constraints, the agent uses judgment to update sections. After refining, the define handler should summarize what changed (e.g., sections updated, constraints added, type unchanged) to make the operation auditable. The refined `problem.md` must pass the same post-write schema validation as a fresh definition.

*Round 2 refinement*: Rule (e) added. This is a mechanical consequence of adopting `## Status` (Change 10). If `## Status` is not adopted, the contract reverts to four invariants. Rule (a) references "all required headings (as defined in the schema)" rather than a hardcoded count. The diff summary is recommended practice ("should"), not normative.

*Traced to*: C-7. Unanimous P2. Fifth invariant proposed by functional-typing (review MO-2, L107-111), accepted by integration-architect (revision R7, L54-66) and devils-advocate (revision Rec-8, L111-123).

**Change 8: Add taxonomy closure design note**

Add after the problem type classification table (SKILL.md, after the four-type table at approximately L818):

> Design note: This taxonomy is intentionally closed. Each type maps to a specific mode in `/conversus interests`. Problems that do not fit these types should be reframed in terms of the closest type, or users should bypass the guided workflow and configure `conversus.yml` directly. Extending this taxonomy requires a companion update to the mode mapping in spec 008.

*No Round 2 changes*.

*Traced to*: C-8. Unanimous P2, both rounds.

**Change 9: Scale pipeline reference to single sentence**

Replace the "Next step" line in the define handler Report section (SKILL.md, at approximately L869):

> Next step: `/conversus interests` (not yet implemented -- this is the first of a series of guided setup commands).

*No Round 2 changes*.

*Traced to*: C-9. Unanimous P2, both rounds.

**Change 10: Add `## Status` section to `problem.md` schema**

Add a `## Status` section to the `problem.md` schema after `## Source Documents` as the final section:

> ```
> ## Status
> draft -- 3 items need clarification
> ```
>
> The define handler sets `status: draft` when any `[CLARIFY:]` tag is present in the output, with a count of unresolved items. It sets `status: ready` when no `[CLARIFY:]` tags are present. This is a factual annotation of the artifact's completeness state -- it reports a measurable property of the artifact.
>
> This is a producer-side annotation. Whether downstream commands treat `draft` status as blocking or advisory is defined by those commands' specifications (enforcement is deferred to spec 008). No RFC 2119 SHOULD language governs consumer behavior within spec 007.

*Round 2 refinement*: Placement changed from between `# Problem Definition` and `## Decision` (functional-typing's original proposal, withdrawn) to end-of-schema, after `## Source Documents`. This preserves content-first reading order for non-expert users (spec.md L87). The deferral framing is added per integration-architect (revision L92-93) and devils-advocate (disputes RD-3) request. Priority settled at P2 per 2-1 majority (integration-architect and functional-typing at P2; devils-advocate at P1, concedes outcome).

*Traced to*: C-10. Substance unanimous, priority P2 by majority. Functional-typing concession (review L56-63), integration-architect (review L51-63), devils-advocate full concession of "bridge" rhetoric (revision L17-19). Placement: integration-architect cross-review DC-2 of functional-typing, functional-typing revision (L27, withdrew original placement).

**Change 11: Gate the Report section on write success**

Change SKILL.md L858 from:

> After writing `problem.md`, print:

to:

> After successfully writing `problem.md`, print:

A one-word edit that gates the Report section on write success, closing an unguarded path.

*New in Round 2*.

*Traced to*: C-11. Unanimous P2. Devils-advocate identified the gap (review MO-1, L52-58); integration-architect proposed the one-word fix (cross-review of devils-advocate T-1, L39-48); all three accepted in revisions.

**Change 12: Add validation precision prose**

Add to the validation contract alongside the `problem.md` schema (SKILL.md, after the post-write validation text from Change 1):

> Validation follows the established heading-lookup convention: heading lookups are case-insensitive and match any heading level, consistent with Phase 6 validation (SKILL.md L659). A heading present with no content beneath it (only whitespace before the next heading) is treated as present but empty -- apply `[CLARIFY:]` handling per the ambiguity rule.

*Round 2 refinement*: Integration-architect originally proposed strict case-sensitive, `##`-level matching (NR-1). Devils-advocate initially proposed the same but reversed to Phase 6 precedent after functional-typing identified the SKILL.md L659 inconsistency. Functional-typing leaned toward Phase 6 precedent for internal consistency. The synthesis adopts Phase 6 precedent as the default for internal consistency, with a note that the define handler controls its own output and a future spec may introduce a stricter model if warranted.

*Traced to*: integration-architect revision NR-1 (L144-153, substance); devils-advocate revision Rec-2 (L25-41, Phase 6 alignment); functional-typing disputes RD-3 (L41-53, leans Phase 6); integration-architect disputes RD-2 (L22-41, acknowledges both defensible).

### P3 Changes (optional, low-risk)

**Change 13: Document single `--context` path as scoping decision**

Add to the define handler Input section (SKILL.md, at approximately L778):

> `--context` accepts exactly one path. Single-path is a scoping decision for spec 007. Directory support provides a pragmatic multi-source mechanism. A follow-up spec may introduce multi-path syntax with explicit ordering and conflict semantics.

*Round 2 refinement*: Framing adjusted from "deliberate design" to "scoping decision with pragmatic multi-source mechanism" per devils-advocate's cross-review of integration-architect (T-1, L41-49), accepted by integration-architect (revision R11, L100-106).

*Traced to*: C-12. Unanimous P3.

**Change 14: Acknowledge frontmatter change in spec**

Amend spec.md L17 ("What changes"):

> SKILL.md gains a "Subcommand Dispatch" section before Step 1, the frontmatter description is updated to list supported subcommands, and a new `/conversus define` command handler is added. The existing `/conversus run` handler headings are namespaced (Input to Run: Input, Execution to Run: Execution) but behaviorally unchanged.

*No Round 2 changes*.

*Traced to*: P3 single advocate (functional-typing).

**Change 15: Note `--force`/`--dry-run` as future consideration**

Add a documentation note (spec.md, Constraints section or define handler):

> Future consideration: `--force` (overwrite without interactive prompt) and `--dry-run` (preview output without writing) flags may be added in a future spec to support non-interactive and automated invocations.

*No Round 2 changes*.

*Traced to*: C-13. Unanimous P3. Devils-advocate reversed from P2 to deferred in Round 2.

**Change 16: Note shared validation as architectural direction, co-located with schema**

Add adjacent to the post-write validation text (Change 1) in the `problem.md` schema section:

> The post-write validation step above defines the canonical schema check for `problem.md`. Any command that reads `problem.md` as input should apply the same heading check before processing. See this validation as a shared contract, not a handler-specific check.

*Round 2 refinement*: Co-located with the schema section for discoverability, per agreement from all three agents. Priority remains P3 after devils-advocate withdrew the P2 elevation (revision Rec-5, L73-83).

*Traced to*: C-14. Unanimous P3 with co-location.

**Change 17: Document `problem.md`/`conversus.yml` artifact independence**

Add a single sentence to the Define: Problem Definition section:

> `problem.md` and `conversus.yml` are independent artifacts. The guided workflow produces `problem.md` first; subsequent commands transform it into `conversus.yml`. The define handler does not read, modify, or depend on an existing `conversus.yml`.

*New in Round 2*. Single-round material, endorsed by all three agents but weighted accordingly.

*Traced to*: C-15. Integration-architect proposed (review MO-2, L142-147); devils-advocate endorsed (cross-review SA-6, L95-97); functional-typing accepted as valid (cross-review T-2, L51-58).

**Change 18: Add interactive-mode `[CLARIFY:]` cross-reference**

Add to the interactive input section (SKILL.md, at approximately L779-782):

> The ambiguity handling rule applies equally to interactive input -- vague or empty responses produce `[CLARIFY:]` tags, not speculative content.

*New in Round 2*. Downgraded from P2 to P3 by devils-advocate after both other agents argued SKILL.md L852's universal MUST already covers this.

*Traced to*: C-16. Devils-advocate proposed (review MO-2, L62-70); downgraded to P3 and cross-reference form (revision Rec-4, L59-69).

**Change 19: Update spec.md schema block if `## Status` adopted**

If `## Status` is adopted (Change 10), update the illustrative schema at spec.md L45-71 to include `## Status` after `## Source Documents`. This is an illustrative update for consistency with SKILL.md, not an expansion of FR-009. FR-009's named sections (spec.md L38) remain unchanged.

*Round 2 refinement*: Clarified as illustrative update, not FR-009 expansion, per functional-typing revision Rec #5 (L88-99) and devils-advocate cross-review DC-2.

*Traced to*: C-17. Single advocate (functional-typing), P3.

**Change 20 (optional annotation): Note the structural/process distinction in refine invariants**

If deemed useful by the implementer, add a parenthetical to the five-rule refine contract (Change 7):

> (Rules (a), (b), (c), and (e) are structural invariants verifiable from the output. Rule (d) is a process obligation -- the handler must consider type re-evaluation, though the type may remain unchanged.)

*New in Round 2*. All three agents agree on the five-rule contract; this annotation addresses the classification distinction devils-advocate raised. Functional-typing and integration-architect accept without advocating; devils-advocate requests it.

*Traced to*: RD-3 (Round 2). Devils-advocate revision Rec-8 (L121); integration-architect revision R7 (L60); functional-typing disputes RD-4 (L57-67).

---

## Key Concessions

### Round 2 concessions by functional-typing

1. **Conceded on `## Status` (RD-1)**: Accepted the arbiter's factual-annotation framing. The field is a computed property embedded in the artifact, not consumer-prescriptive schema expansion. (review L56-63)
2. **Conceded on shared validation approach (RD-2)**: Accepted the schema-layer prose contract as articulated by the arbiter. Acknowledged that handler-local validation was too restrictive. (review L65-71)
3. **Withdrew `## Status` placement**: Abandoned between-title-and-decision placement after integration-architect's UX critique (spec.md L87: non-expert users should see the decision statement first). Adopted end-of-schema placement. (revision L27, Rec #1 disposition)
4. **Revised heading-count language**: Changed from hardcoded "8" to "all headings defined in the schema block" to eliminate coupling between recommendations. (revision Rec #1 disposition)

### Round 2 concessions by integration-architect

1. **Accepted fifth refine invariant**: Status re-evaluation on refine is a mechanical consequence of the factual-annotation framing integration-architect championed. (revision R7, L54-66)
2. **Settled `## Status` priority at P2**: Dropped the P1 aspiration in the absence of explicit P1 consensus from both other reviewers. (revision R10, L82-94)
3. **Accepted "scoping decision" framing for single-path `--context`**: Withdrew "deliberate design" characterization, accepted devils-advocate's more honest documentation language. (revision R11, L100-106)
4. **Accepted validation precision as new P2**: Rejected the "P1 amendment to C-1" framing but accepted the substance at P2. (revision NR-1, L144-153)

### Round 2 concessions by devils-advocate

1. **Fully withdrew "bridge that nothing walks across" rhetoric**: Both cross-reviewers identified it as a qualified concession functioning as a reversal. The factual-annotation framing is now accepted without reservation. (revision Rec-1, L17-19)
2. **Downgraded validation precision from P1 to P2**: Withdrew "P1 amendment to C-1" framing as procedurally improper. Accepted the content as a new P2 recommendation. (revision Rec-2, L25-41)
3. **Aligned validation semantics with Phase 6 precedent**: Reversed from strict case-sensitive matching to Phase 6's case-insensitive, level-agnostic model after functional-typing identified the SKILL.md L659 inconsistency. (revision Rec-2, L35-39)
4. **Accepted one-word write-failure fix**: Adopted integration-architect's "After successfully writing" formulation over own multi-sentence error specification. (revision Rec-3, L45-56)
5. **Downgraded interactive-mode guidance from P2 to P3**: Accepted that SKILL.md L852's universal MUST already covers the interactive path. Changed form to cross-reference. (revision Rec-4, L59-69)
6. **Withdrew P2 elevation for Change 14**: Conceded that discoverability is a placement concern, not a priority concern. Accepted P3 with co-location. (revision Rec-5, L73-83)
7. **Accepted deferral of multi-path `--context` (RD-3)**: Reversed Round 1 position after arbiter's grounding in SKILL.md L797 as the designed multi-source mechanism. (review L43-44)
8. **Accepted deferral of `--force`/`--dry-run` (RD-4)**: Reversed Round 1 position after arbiter's non-expert user principle analysis. (review L46-47)
