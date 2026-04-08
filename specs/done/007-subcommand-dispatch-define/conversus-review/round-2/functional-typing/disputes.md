# Disputes: functional-typing (Round 2, Phase 4)

**Agent**: functional-typing
**Round**: 2 of 2
**Date**: 2026-03-22

---

## Remaining Disputes

### RD-1: `## Status` priority — P1 vs P2

**Parties**: devils-advocate (P1), integration-architect (P2), functional-typing (P2 conditional on placement and scope constraints)

**Status**: Two-against-one. Devils-advocate holds P1 (revision.md L21: "Priority: P1 (unchanged)"). Integration-architect explicitly settled at P2 (revision.md L88: "I register my position as P2"). I hold P2 (revision.md L82: conditions on Change 10).

**Substance**: The priority disagreement is narrow. All three reviewers now agree on the substance — `## Status` is a factual annotation, the define handler computes it from `[CLARIFY:]` tag count, no RFC 2119 SHOULD language governs downstream consumers. Devils-advocate's full concession on the factual-annotation framing (DA revision.md L17-19: "I concede the point fully. The 'bridge' rhetoric was a qualified concession functioning as a reversal") removes the last substantive objection. The remaining question is whether a unanimously-accepted-but-non-FR metadata field warrants P1 implementation priority. I hold P2: the field is not listed in FR-009 (spec.md L38), it is a schema enhancement, and P1 should be reserved for items that directly implement functional requirements or prevent specification ambiguity in the dispatch/define contract. The synthesizer should resolve this at P2 given 2-1 alignment.

**Impact on spec**: None. Priority assignment affects implementation ordering, not the content of the changes to SKILL.md or spec.md.

---

### RD-2: `## Status` placement — end-of-schema vs frontmatter

**Parties**: All three reviewers now converge on end-of-schema (after `## Source Documents`), but integration-architect's revision.md L94 leaves a secondary option open: "at the end of the schema (after `## Source Documents`) or as frontmatter metadata."

**Status**: Functionally converged with a trailing ambiguity. I withdrew my original placement (between `# Problem Definition` and `## Decision`) in revision.md L27 and proposed end-of-schema placement. Integration-architect proposes end-of-schema as the primary option but also allows frontmatter. Devils-advocate does not address placement in their revision.

**My position**: The synthesis should pick one placement and not leave a disjunction. End-of-schema is the correct choice for three reasons grounded in the target files:

1. The schema at SKILL.md L822-850 uses `##`-level headings for all sections. `## Status` at the end is structurally consistent. Frontmatter would be a YAML block or a different syntactic form — introducing a format not present anywhere in the current schema.
2. The non-expert user principle (spec.md L87) favors content-first reading order: Decision, Type, Context, Constraints, Success Criteria, Open Questions, Source Documents, then Status. Frontmatter places metadata before `# Problem Definition`, which the user must scroll past.
3. The post-write validation (Change 1) checks for `##`-level headings. Frontmatter is not a `##`-level heading and would require a separate validation mechanism — adding complexity for no benefit.

I ask the synthesizer to resolve the disjunction in favor of end-of-schema and eliminate the frontmatter alternative.

**Impact on spec**: The schema block in SKILL.md L822-850 and spec.md L45-71 must reflect whichever placement is chosen. A disjunction in the synthesis would force implementers to handle both formats.

---

### RD-3: Validation matching semantics — case-sensitive vs Phase 6 precedent

**Parties**: devils-advocate (revised to Phase 6 precedent: case-insensitive, level-agnostic; DA revision.md L37-39), integration-architect (case-sensitive exact text at `##` level; IA revision.md L150: "Headings are matched at `##` level with case-sensitive exact text"), functional-typing (defers to schema-as-normative-reference without specifying matching semantics independently)

**Status**: Two positions remain. Devils-advocate reversed from case-sensitive to Phase 6 precedent (case-insensitive, level-agnostic) after I identified the inconsistency with SKILL.md L763 in my cross-review. Integration-architect proposed a new NR-1 that specifies case-sensitive, `##`-level-only matching (IA revision.md L146-152). These are incompatible.

**My position**: The define handler writes the schema itself — it controls the output format completely. The case-sensitivity question is therefore less consequential than for Phase 6, where an uncontrolled arbiter produces headings. However, internal consistency within SKILL.md argues for a single validation model. SKILL.md L763 establishes the precedent: "Heading lookups are case-insensitive and match any heading level." Creating a second, stricter validation model for the define handler without explicit justification introduces a maintenance burden (two validation contracts in one file).

I lean toward devils-advocate's revised position: follow the Phase 6 precedent for consistency, while noting that the define handler's controlled output makes this a low-risk decision either way. If the synthesizer selects case-sensitive matching, it must explicitly justify the divergence from L763. If it selects case-insensitive matching, no justification is needed — the existing precedent applies.

This is a minor dispute. The practical difference is negligible because the define handler controls what it writes.

**Impact on spec**: Affects the prose in the post-write validation contract added to SKILL.md. Does not affect the schema itself.

---

### RD-4: Refine invariant (d) — testable structural check vs process obligation

**Parties**: devils-advocate (notes the distinction; DA revision.md L121: "the distinction between testable structural invariants (a-c, e) and process obligations (d) should be noted in the spec prose"), integration-architect (acknowledges the distinction without requesting prose; IA revision.md L60), functional-typing (rule (e) is a structural check like (a-c), rule (d) is the sole process obligation)

**Status**: All three agree on the five-rule refine contract. The dispute is whether the spec prose should explicitly classify rules into structural checks vs process obligations.

**My position**: Devils-advocate is correct that rules (a)-(c) and (e) are structurally testable (diff the output, check heading presence, count tags) while rule (d) is a process obligation (did the handler consider type re-evaluation?). This is a real distinction. However, annotating the classification in spec prose adds complexity to a section that is already dense. The spec should state the five invariants. If a future spec (e.g., spec 008 test harness) needs to distinguish testable invariants from process obligations, it can do so in its own context.

I do not oppose adding a brief note if the synthesizer finds it useful, but I do not advocate for it as a required change. P3 at most, subordinate to the five-rule contract itself.

**Impact on spec**: A single parenthetical or sentence in SKILL.md's refine section, if adopted.

---

## Convergence

The deliberation has reached strong convergence. The following positions are unanimous across all three reviewers after Round 2 revisions.

### Unanimous (all three reviewers, both rounds)

1. **P1: Post-write schema validation** (Change 1). The define handler validates all required headings after writing `problem.md`. Missing headings are added with `[CLARIFY:]` placeholders. The heading list references the schema as the single source of truth, not a hardcoded count.
   - *Grounding*: SKILL.md L822-850 (schema), spec.md L38 (FR-009).

2. **P1: `--context` path validation** (Change 2). Fail on non-existent paths, warn on empty directories.
   - *Grounding*: SKILL.md L797 (context path), spec.md L35 (FR-006).

3. **P1: Dispatch matching semantics** (Change 3). Exact, case-sensitive, exhaustive matching. "Did you mean: `/conversus run {cmd}`?" error message enhancement accepted.
   - *Grounding*: SKILL.md L18-33 (dispatch table), spec.md L30 (FR-004).

4. **P2: Single-agent execution model statement** (Change 4). The define handler runs as a single foreground agent, not a multi-agent pipeline.
   - *Grounding*: SKILL.md L769 (define handler entry).

5. **P2: Empty-section `[CLARIFY:]` coverage** (Change 5). Every empty section gets a `[CLARIFY:]` placeholder.
   - *Grounding*: SKILL.md L852-854 (ambiguity and empty sections).

6. **P2: `--output` directory creation** (Change 6). Create the output directory if it does not exist.
   - *Grounding*: SKILL.md L784 (output directory).

7. **P2: Five-rule refine contract** (Change 7, expanded). All headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated, Status re-evaluated based on `[CLARIFY:]` tag count. Diff summary as recommended practice.
   - *Grounding*: SKILL.md L791 (refine behavior), SKILL.md L865 (tag count).

8. **P2: Taxonomy closure design note** (Change 8). Document that problem types are a closed set.
   - *Grounding*: SKILL.md L806-818 (type classification table).

9. **P2: Pipeline overview scaled to single sentence** (Change 9). The spec summary should note that `/conversus define` does not invoke the multi-agent pipeline.
   - *Grounding*: spec.md L13 (feature summary).

10. **P2: `## Status` as factual annotation** (Change 10). The define handler sets `draft` or `ready` based on `[CLARIFY:]` tag count. No RFC 2119 SHOULD language for consumers. Enforcement deferred to spec 008. Substance is unanimous; priority is 2-1 (P2 vs P1).
    - *Grounding*: SKILL.md L865 (tag count already computed for Report section).

11. **P2: Report section gated on write success** (New). Change SKILL.md L858 from "After writing" to "After successfully writing." One-word fix closing a real gap.
    - *Grounding*: SKILL.md L858 (Report preamble), SKILL.md L653-657 (Phase 6 failure handling precedent).

12. **P3: Document single `--context` path as scoping decision** (Change 11). Framing adjusted per devils-advocate: "scoping decision with pragmatic multi-source mechanism," not "deliberate design."
    - *Grounding*: SKILL.md L797, spec.md L35 (FR-006).

13. **P3: Acknowledge frontmatter change in spec** (Change 12).
    - *Grounding*: spec.md L1-8 (frontmatter block).

14. **P3: `--force`/`--dry-run` as future consideration** (Change 13). Deferred from spec 007 scope with documentation note.
    - *Grounding*: spec.md L87-89 (constraints).

15. **P3: Shared validation as architectural direction** (Change 14). Co-located with the post-write validation text for discoverability. Priority P3 per 2-1 agreement (functional-typing, integration-architect hold P3; devils-advocate withdrew P2 elevation).
    - *Grounding*: SKILL.md L822-850 (schema location).

16. **P3: `problem.md` and `conversus.yml` artifact independence** (New, single-round). A single sentence noting these are independent artifacts for different workflow paths.
    - *Grounding*: SKILL.md L36-42 (run handler), SKILL.md L769-876 (define handler).

17. **P3: Interactive-mode `[CLARIFY:]` cross-reference** (Downgraded from P2). A cross-reference noting the ambiguity rule at SKILL.md L852 applies equally to interactive input.
    - *Grounding*: SKILL.md L852 (unconditional MUST for ambiguity handling).

18. **P2: Validation precision prose** (New). The post-write validation should specify matching semantics for headings. Substance agreed; exact semantics (case-sensitive vs Phase 6 precedent) is RD-3 above.
    - *Grounding*: SKILL.md L822-850 (schema block), SKILL.md L763 (Phase 6 validation precedent).

19. **P3 (if adopted): spec.md schema block update** (Rec #5). If `## Status` is adopted, the illustrative schema at spec.md L45-71 should include `## Status` for consistency. This is an illustrative update, not an FR-009 expansion. FR-009's named sections (spec.md L38) remain unchanged.
    - *Grounding*: spec.md L45-71 (illustrative schema), spec.md L38 (FR-009 section list).

---

## Final Position Statement

This deliberation has been monotonically convergent across two rounds. Every position has either been unanimously adopted, refined toward consensus, or narrowed to a residual disagreement on priority or prose detail. No position reversals have occurred. The remaining disputes (RD-1 through RD-4) are all resolvable by the synthesizer without compromising the spec's structural integrity.

### Non-negotiables

These positions are non-negotiable for functional-typing. Abandoning any of them would introduce type-level inconsistencies, specification ambiguities, or FR coverage gaps.

1. **The three P1 changes (Changes 1-3) must be adopted without modification.** Post-write schema validation, `--context` path validation, and dispatch matching semantics are the minimum correctness guarantees for spec 007. They implement FR-001, FR-004, FR-006, and FR-009 directly. Removing any of them leaves a functional requirement unverified. (spec.md L27-38, SKILL.md L18-33, L797, L822-850.)

2. **The five-rule refine contract is atomic with `## Status` adoption.** If `## Status` is adopted (Change 10), the refine contract must include rule (e): status re-evaluation based on `[CLARIFY:]` tag count. A factual annotation that becomes stale after a refine is worse than no annotation — it actively misleads the reader. The factual-annotation framing (championed by integration-architect, conceded by devils-advocate and myself) logically requires that facts are maintained on every write path. Four rules without (e) plus `## Status` is an internally inconsistent specification. (SKILL.md L791, L865.)

3. **`## Status` must not carry RFC 2119 SHOULD obligations for consumers.** The arbiter's resolution on RD-1 explicitly set aside consumer-prescriptive language. Re-introducing SHOULD obligations — even in softened form — would exceed spec 007's jurisdictional scope. The define handler sets the field; what consumers do with it is spec 008's decision. (Arbiter resolution RD-1, spec.md L87: non-expert user principle means status is informational, not gating.)

4. **The heading list must be derived from the schema, not hardcoded.** Validation checks "all headings defined in the schema block." If the schema gains or loses a heading, the validation adapts automatically. A hardcoded count (7, 8, or any number) creates coupling between independent recommendations and invites drift when the schema evolves. (SKILL.md L822-850.)

5. **`## Status` placement must be end-of-schema (after `## Source Documents`), not a disjunction.** A synthesis that says "end-of-schema or frontmatter" forces implementers to handle both formats and leaves the schema structurally ambiguous. One canonical placement. End-of-schema is consistent with the existing `##`-level heading structure, the content-first reading order, and the post-write validation contract that checks `##`-level headings. (SKILL.md L822-850, spec.md L87.)

### Negotiables

These positions I hold but will defer to the synthesizer if the majority disagrees.

- **`## Status` at P2 rather than P1.** I hold P2 because the field is not in FR-009, but if the synthesizer assigns P1, the spec is not harmed — only the implementation ordering changes.
- **Validation matching semantics.** I lean toward Phase 6 precedent (case-insensitive, level-agnostic) for internal consistency, but the define handler controls its own output, making either choice low-risk.
- **Refine invariant classification annotation.** I do not oppose noting the structural-vs-process distinction in prose but do not advocate for it as a required change.
- **Change 14 priority.** P3 is correct, but P2 would not damage the spec.

### Summary metrics

- **Total convergence points**: 19 (items 1-19 in the Convergence section above)
- **Remaining disputes**: 4 (RD-1 through RD-4), all on priority assignment or prose detail
- **Non-negotiables**: 5
- **FR coverage**: All 12 functional requirements (FR-001 through FR-012) remain correctly addressed. No FR coverage gaps exist.
- **Rounds completed**: 2 of 2. The deliberation is ready for final synthesis.
