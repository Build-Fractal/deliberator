# Final Arbitration Resolution: 007-subcommand-dispatch-define

**Arbiter**: conversus-constitution (subject of deliberation)
**Influence level**: advisory
**Trigger**: disputes_remain
**Round**: Final (after 2 rounds of deliberation)
**Date**: 2026-03-22
**Grounding documents**: spec.md (007-subcommand-dispatch-define), SKILL.md

---

## Process Note

This is the final arbitration, triggered because three narrow disputes remain after two full rounds of deliberation. I am the subject of this deliberation -- conversus itself. My Round 1 arbitration provided advisory opinions on five disputes; all five were adopted in substance by all three agents in Round 2. The remaining three disputes are priority/style questions with unanimous substance agreement. No agent contests any mechanism, schema element, or behavioral contract.

My influence level remains **advisory**. The positions below are perspectives for the spec author to weigh when applying the final recommendation set. They do not bind any agent, override any consensus, or prescribe implementation ordering.

The 19 convergence points from the cross-round synthesis (FR-1 through FR-20) are not revisited here. They are settled. This resolution addresses only the three residual disputes identified in the final synthesis (RD-1, RD-2, RD-3).

---

## Decision Framework

Each dispute is evaluated against the same five criteria used in the Round 1 arbitration, with one addition reflecting the maturity of the deliberation:

1. **Spec authority**: Does spec 007 have jurisdiction over the disputed change? (spec.md L6: "foundational -- establishes the dispatch infrastructure")
2. **FR traceability**: Is the disputed change motivated by an existing FR, or does it extend beyond the FR framework?
3. **Schema minimality**: Does the change expand `problem.md`'s schema beyond what the spec's stated scope requires?
4. **Non-expert user principle**: Does the change serve the non-expert user? (spec.md L87: "Must NOT require coding knowledge to use")
5. **Additive constraint**: Does the change respect the principle that spec 007 is additive and must not break existing behavior?
6. **Deliberation consensus weight**: Where all three agents agree on substance and disagree only on priority or prose precision, the advisory opinion should confirm the substance and defer to the majority on the administrative question.

---

## Advisory Opinions

### Opinion on RD-1 (Final): `## Status` priority -- P1 vs P2

**Dispute**: All three agents agree that `## Status` should be added to the `problem.md` schema as a factual annotation, placed at end-of-schema (after `## Source Documents`), with no RFC 2119 language prescribing consumer behavior, and with enforcement deferred to spec 008. The sole remaining question is whether this change is P1 or P2. Integration-architect and functional-typing hold P2. Devils-advocate holds P1 but concedes the P2 outcome.

**My perspective**: My Round 1 advisory reframed `## Status` as descriptive rather than advisory or binding. That reframing was adopted by all three agents and broke the Round 1 deadlock. The mechanism is settled. The priority question is administrative.

The three P1 items (post-write schema validation, `--context` path validation, dispatch matching semantics) earned P1 through a specific property: they were independently identified by all three agents in the first phase of the first round, never contested in any subsequent phase, and directly implement functional requirements (FR-001, FR-004, FR-006, FR-009). `## Status` does not share this property. It was disputed through Round 1, resolved only after arbitration reframing, and does not trace to any FR in the spec. FR-009 (spec.md L38) enumerates the required sections of `problem.md`; `## Status` is not among them.

Devils-advocate's argument -- that `## Status` is the only machine-readable completeness signal and therefore functionally important -- is correct about the signal's value but does not change the priority calculus. Functional importance and implementation priority are distinct. The field is valuable. It should be implemented. But placing it alongside the three foundational P1 items -- which have the strongest consensus in the entire deliberation -- would dilute the signal that P1 sends about what must be implemented first and without compromise.

**My advisory position**: P2 is correct. The 2-1 majority is well-grounded. Devils-advocate's P1 argument is noted for the record and reflects a legitimate perspective on the field's functional importance, but the administrative label should reflect the deliberation's consensus structure: P1 for unanimously uncontested items that directly implement FRs, P2 for unanimously accepted enhancements that extend the schema.

**Grounding**: spec.md L38 (FR-009 section list -- `## Status` is absent), SKILL.md L865 (the clarification count is already computed and reported to the terminal, so persistence in the artifact is an enhancement, not a functional gap), Round 1 arbitration Opinion on RD-1 (factual-annotation reframing), Round 2 synthesis C-10 (substance unanimous, priority 2-1).

**Confidence**: High. This is an administrative labeling question with no impact on the content of the spec changes.

---

### Opinion on RD-2 (Final): Validation matching semantics -- Phase 6 precedent vs handler-controlled strict matching

**Dispute**: Devils-advocate and functional-typing lean toward following the Phase 6 precedent (case-insensitive, level-agnostic heading matching, as established at SKILL.md L659-763). Integration-architect proposes case-sensitive, `##`-level exact matching, arguing that the define handler validates its own output and therefore a stricter model is natural. Integration-architect acknowledges both options are defensible and does not contest the synthesis decision.

**My perspective**: I execute both validation paths -- the Phase 6 output validation and the define handler's post-write validation. I have direct operational knowledge of both.

The Phase 6 validation at SKILL.md L659 was designed to be permissive because it validates output from an uncontrolled agent (the arbiter) whose heading formatting cannot be guaranteed. The text is explicit: "Heading lookups are case-insensitive and match any heading level." This permissiveness exists for a reason: free-writing agents may produce `### Process Note` instead of `## Process Note`, and the validation must not fail on stylistic variation.

The define handler is different. It controls its own output completely. The schema at SKILL.md L822-850 uses `##`-level headings exclusively. The handler writes these headings -- it knows the exact text and level. In this context, strict matching would catch implementation bugs (e.g., the handler accidentally writes `# Decision` instead of `## Decision`), while permissive matching would silently accept them.

However, the question is not which model is technically better for the define handler in isolation. The question is whether SKILL.md should contain two different validation models without an explicit architectural justification for the divergence. I observe that it should not -- at least not in spec 007.

The cost of the inconsistency is real but subtle. A future spec author reading SKILL.md will encounter two validation contracts: one at L659 (permissive) and one in the define handler section (strict). They will need to determine which model applies to their new handler. If the spec does not explain why the models differ, they must reverse-engineer the rationale (handler-controlled output vs uncontrolled agent output). This is a maintenance burden that grows with each new handler.

The cost of uniformity is also real but smaller: the define handler's validation would accept heading-level variations it does not produce, making the check slightly less precise. But the handler controls its output -- if it writes `## Decision`, the validation will find `## Decision` regardless of whether matching is strict or permissive. The permissive model is a superset of the strict model. It catches everything the strict model catches, and additionally tolerates variations that should not occur but might if the handler code is modified in the future.

**My advisory position**: Follow the Phase 6 precedent. Case-insensitive, level-agnostic matching provides a single validation model across SKILL.md, avoids unexplained divergence, and is a superset of strict matching for handler-controlled output. State the matching semantics explicitly in the validation contract prose, as integration-architect correctly insists -- implicit matching semantics are the actual risk both sides agree on.

If a future spec determines that handler-controlled output warrants stricter validation, it can introduce a second model with explicit rationale for the divergence. Spec 007 should not be the spec that creates the inconsistency without that rationale.

This aligns with the deliberation's conservative-default principle: when two options are low-risk and one is consistent with existing precedent, follow precedent.

**Grounding**: SKILL.md L659 (Phase 6 validation: "Heading lookups are case-insensitive and match any heading level"), SKILL.md L763 (heading matching rule in dispute-parsing subsystem: same permissive model), SKILL.md L822-850 (define handler schema -- all `##`-level headings), Round 2 synthesis RD-2 (adopted Phase 6 precedent as default), integration-architect disputes.md RD-2 (acknowledges both options defensible).

**Confidence**: Medium-High. The technical difference is negligible for the define handler's current use case. The consistency argument is the tiebreaker, and it favors Phase 6 precedent. Integration-architect's position is technically sound but introduces architectural divergence that is better deferred to a future spec with explicit justification.

---

### Opinion on RD-3 (Final): Refine invariant classification -- structural testability vs process obligation annotation

**Dispute**: All three agents agree on the five-rule refine contract. Devils-advocate requests that the spec prose annotate the distinction between structurally testable invariants (rules a, b, c, e -- verifiable from the output alone) and process obligations (rule d -- type re-evaluation, where the outcome cannot be verified from the output). Integration-architect accepts the annotation without advocating for it. Functional-typing considers it P3 at most.

**My perspective**: I execute the refine operation. The distinction devils-advocate identifies is real and operationally significant.

Rules (a), (b), (c), and (e) are structurally testable. After a refine, an independent observer can check:
- (a) Are all required headings present? (Diff the heading set.)
- (b) Was any existing content silently deleted? (Diff the sections.)
- (c) Does Source Documents contain the union of old and new paths? (Set comparison.)
- (e) Does the Status field reflect the current `[CLARIFY:]` tag count? (Count and compare.)

Rule (d) is different. "Type must be re-evaluated against the combined input" is a process obligation. The type may legitimately remain `selection` after a refine that adds new constraints -- re-evaluation does not mean re-classification. An observer examining the output cannot distinguish "the handler re-evaluated and confirmed the type" from "the handler skipped re-evaluation entirely." The obligation is about the handler's reasoning process, not the artifact's structure.

This distinction matters for two reasons:

1. **Testing**: A spec 008 test harness (if built) can automatically verify (a), (b), (c), and (e) by comparing pre-refine and post-refine artifacts. It cannot automatically verify (d). Annotating the distinction tells the test author which invariants are automatable and which require manual review or trust in the handler's implementation.

2. **Spec precision**: The five rules as currently stated appear to be a uniform list. A reader might assume all five are equally verifiable. The annotation prevents a false expectation of full automated testability.

However, the annotation is a documentation improvement, not a normative change. The five-rule contract is the normative content. The annotation is explanatory prose that helps implementers and test authors understand the nature of each rule. It does not change what the handler must do -- it changes what a reader can expect to verify.

**My advisory position**: Include the annotation as optional prose, P3. The suggested formulation from the synthesis (FR-20) is well-crafted: "(Rules (a), (b), (c), and (e) are structural invariants verifiable from the output. Rule (d) is a process obligation -- the handler must consider type re-evaluation, though the type may remain unchanged.)" This is one parenthetical sentence. It adds clarity without adding complexity. It is the kind of precision that pays forward when spec 008's author encounters the five-rule contract and asks "can I test all of these?"

The deliberation has correctly sized this as P3. It is optional, low-risk, and subordinate to the five-rule contract itself. The spec author may include or omit it without affecting the normative content of the specification.

**Grounding**: SKILL.md L791 (refine behavior), Round 2 synthesis C-7 (five-rule contract), Round 2 synthesis RD-3 (narrow residual), Round 1 arbitration Opinion on RD-5 (confirmed four rules as enforceable invariants, distinguished diff summary as guidance -- the same structural/process distinction applies here).

**Confidence**: Medium. The annotation is correct and useful. Whether it belongs in spec 007's prose or in a future spec's test plan is a judgment call. The deliberation's P3 assignment is appropriate -- it signals "include if convenient, omit without cost."

---

## Considerations for Next Round

### Summary of Advisory Positions

| Dispute | Advisory Position | Alignment |
|---------|-------------------|-----------|
| RD-1: `## Status` priority | P2. The 2-1 majority is well-grounded. P1 should be reserved for unanimously uncontested items that directly implement FRs. | Confirms the 2-1 majority (integration-architect + functional-typing at P2). |
| RD-2: Validation matching semantics | Follow Phase 6 precedent (case-insensitive, level-agnostic). State matching semantics explicitly. A future spec may introduce stricter matching with explicit rationale. | Confirms the 2-1 lean (devils-advocate + functional-typing toward Phase 6 precedent). Integration-architect's position is acknowledged as technically defensible. |
| RD-3: Refine invariant classification | Include the structural/process annotation as optional P3 prose. One parenthetical sentence. | Confirms devils-advocate's request at P3, consistent with integration-architect's acceptance and functional-typing's tolerance. |

### Observations for the Spec Author

1. **The deliberation is complete.** Two rounds produced 19 consensus items, resolved all five Round 1 disputes on substance, and reduced the remaining disagreements to priority labels and prose precision. The three residual disputes have zero impact on the normative content of the spec changes. The recommendation set in the final synthesis is ready for implementation.

2. **The three P1 items are the strongest foundation.** Post-write schema validation, `--context` path validation, and dispatch matching semantics were never contested by any agent in any phase of either round. They directly implement functional requirements. They should be implemented first and without modification.

3. **The `## Status` deferral language is load-bearing.** This observation from devils-advocate (endorsed by integration-architect) is correct and important. The synthesis must state that `## Status` is a producer-side annotation with enforcement deferred to spec 008. Without this language, spec 008's author may assume the quality checkpoint is operational. With it, spec 008's author inherits a clear design obligation to define consumer behavior for the `draft`/`ready` signal.

4. **The five-rule refine contract is the most significant consensus achievement of Round 2.** Round 1 could not settle on refine semantics. The arbiter's Round 1 opinion confirmed four structural invariants. Round 2 added a fifth (Status re-evaluation) as a mechanical consequence of adopting `## Status`. The contract is now unanimous and should be treated as settled.

5. **Validation precision is approaching the point where prose may be insufficient.** The accumulated validation specification -- heading count derived from schema, matching semantics (now resolved as Phase 6 precedent), content-presence rules, `[CLARIFY:]` handling for empty sections -- is growing complex. The deliberation has managed this complexity within prose. A future spec that adds additional handlers or validation rules should consider whether a structured rule set (e.g., a validation table analogous to the dispatch table) would be more maintainable than embedded prose paragraphs.

---

## Confidence Assessment

| Dispute | Confidence | Rationale |
|---------|-----------|-----------|
| RD-1: `## Status` priority | **High** | Administrative labeling question with no impact on spec content. The 2-1 majority has clear grounding in the deliberation's consensus structure and FR traceability. |
| RD-2: Validation matching semantics | **Medium-High** | Both options are technically defensible. The consistency argument (single validation model across SKILL.md) is the tiebreaker. Integration-architect's strict-matching position is sound but introduces divergence that is better justified explicitly in a future spec. |
| RD-3: Refine invariant classification | **Medium** | The annotation is correct and useful but optional. Whether it belongs in spec 007 or a future test spec is a judgment call. P3 is the right priority -- include if convenient, omit without cost. |

### Overall Deliberation Assessment

This deliberation achieved exceptionally high convergence. All five Round 1 disputes were resolved on substance. The three residual disputes affect implementation ordering (RD-1), a low-risk matching convention (RD-2), and optional prose annotation (RD-3). None affects the normative content of the specification.

The arbitration process functioned as designed. Round 1 advisory opinions provided new arguments grounded in operational knowledge (the factual-annotation reframing for `## Status`, the design-intent grounding for single-path `--context`, the non-expert user principle for `--force`/`--dry-run`). Agents evaluated these arguments on merit -- devils-advocate's two reversals in Round 2 were traced to better-grounded arguments, not majority pressure. The final synthesis correctly attributes resolution mechanisms across deliberation, arbitration, and concession.

The spec is ready for implementation.
