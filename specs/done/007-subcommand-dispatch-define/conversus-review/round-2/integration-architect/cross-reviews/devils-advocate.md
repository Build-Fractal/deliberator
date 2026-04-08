# Cross-Review: devils-advocate Round 2

**Cross-reviewer**: integration-architect
**Reviewing**: devils-advocate Round 2 review
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: Rec-2's "P1 amendment" claim oversteps the consensus it amends

Devils-advocate labels Rec-2 (tighten validation contract prose to specify case-sensitive heading-level-2 matching) as a "P1 amendment to existing C-1 consensus." This framing is dangerous because it smuggles a new requirement into a closed consensus item.

C-1 is settled: the define handler validates all 7 headings after writing. The deliberation agreed on that obligation unanimously. Devils-advocate's Rec-2 does not amend C-1 -- it adds a new requirement (precise matching semantics: case sensitivity, heading level, content-presence rules). These are valid concerns, but packaging them as "precision refinement" of an existing P1 consensus is procedurally dishonest. If accepted at face value, any reviewer could reopen any consensus item by calling their new requirement a "refinement."

The actual recommendation is reasonable. The heading matching semantics should be defined. But it is a new P2 item, not a P1 amendment to C-1. The spec already shows the headings at `##` level with exact text in the schema (SKILL.md L822-850), and the spec's own schema block is the normative reference. Adding explicit prose restating what the schema already demonstrates is useful for implementers but not P1-critical. The schema is unambiguous: the headings are `## Decision`, `## Type`, etc. at level 2. An implementation that checks for `### Decision` or `## decision` is already wrong because it does not match the schema.

**My position**: Accept the substance of Rec-2 (explicit matching semantics are worth stating) but reject the P1 priority and the "amendment to C-1" framing. This is a new P2 recommendation. C-1 remains closed as-is.

---

### DC-2: OBA-1's "bridge that nothing walks across" argument contradicts the accepted concession

In OBA-1, devils-advocate accepts the arbiter's factual-annotation framing for `## Status`, withdraws RFC 2119 SHOULD language, and states "This is not a reversal of my concession." Then, in the same section, devils-advocate argues: "A bridge that nothing walks across is not a bridge." This is a reversal in everything but name.

The concession was: spec 007 defines `## Status` as a descriptive field; spec 007 does not prescribe consumer behavior; spec 008 decides how to use the field. The "bridge that nothing walks across" argument is an assertion that the `## Status` field is inadequate *unless* spec 008 implements enforcement -- which is exactly the consumer-side gate enforcement that devils-advocate withdrew in Round 1 (Concession #1, confirmed in this review).

If the concession genuinely stands, then spec 007's obligation is discharged when it writes the field. Whether spec 008 checks it is spec 008's concern, and expressing anxiety about spec 008's hypothetical choices reintroduces the consumer-prescriptive framing through the back door.

This matters because the "design risk" flag devils-advocate plants here creates implicit pressure on the spec 008 deliberation to treat `draft` status as blocking -- which is the gate behavior that was explicitly rejected in this spec's scope. If spec 008's reviewers read this flag, they inherit a loaded question rather than making an independent design decision.

**My position**: The concession is either real or it is not. If `## Status` is a fact about the artifact, the fact is useful regardless of what consumers do with it. Devils-advocate should either fully concede (the field is valuable as a descriptive annotation, full stop) or openly maintain the dispute (the field is only valuable if enforced). The current position attempts both and achieves neither.

---

## Tensions

### T-1: MO-1 (write-failure error specification) is directionally correct but architecturally misplaced

Devils-advocate identifies a real gap: the define handler's Report section (SKILL.md L856-875) has no failure mode for write operations. The recommendation ("If writing `problem.md` fails, report the error to the user and do not print the success report") is sensible.

The tension is architectural. The define handler operates within an agent runtime (SKILL.md L14: "Requires an agent runtime that supports background Agent tool dispatch"). The Write tool in that runtime already surfaces errors to the orchestrating agent. Specifying write-failure behavior in the SKILL.md handler section duplicates the runtime's error-handling contract. If the spec says "report the error," what does that mean operationally? The agent receives an error from the Write tool and... prints it? The agent already does that -- it is the runtime's default behavior.

The real concern underneath MO-1 is whether the Report section should be gated on write success. That is a valid concern, and it can be addressed with a single clause: "After successfully writing `problem.md`, print:" (adding "successfully" to SKILL.md L858). This is a one-word edit that closes the gap without introducing a redundant error-handling specification that competes with the runtime's own contract.

**My position**: Accept the intent (Report section should be gated on write success). Reject the form (a separate "write-failure error specification"). The fix is a one-word qualifier, not a new section.

---

### T-2: MO-2 (interactive mode termination) overlaps with existing ambiguity handling but raises a legitimate edge case

Devils-advocate argues that FR-012's interactive mode (SKILL.md L779-782) needs explicit behavior for vague or empty responses. The recommendation is that such responses produce `[CLARIFY:]` tags, consistent with SKILL.md L852 ("Vague descriptions should produce more `[CLARIFY:]` tags, not hallucinated specifics").

I agree with devils-advocate's own assessment: SKILL.md L852 already covers this implicitly. The ambiguity handling rule is universal ("Any field where the agent cannot confidently determine the content MUST include a `[CLARIFY: ...]` tag"), and interactive input is a field-determination pathway. The rule applies.

The tension is whether implicit coverage is sufficient for the non-expert user path. Devils-advocate argues it is not, because an agent might interpret "no input" as license to generate speculative content. This is a real risk -- but it is a risk inherent in agent behavior, not a gap in the specification. The spec says "MUST include a `[CLARIFY:]` tag" when content cannot be confidently determined. An agent that generates speculative content from empty input violates this MUST. Adding a redundant statement for the interactive path does not make the MUST stronger; it implies that the universal MUST is insufficient without per-path restatement.

**My position**: The recommendation is P3 at most, not P2. The universal ambiguity rule at SKILL.md L852 is normative and covers all input paths including interactive. If a specific note for the interactive path is added, it should be a cross-reference ("The ambiguity rule at [Ambiguity handling] applies to interactive input"), not a restated obligation.

---

### T-3: Rec-5's priority elevation (Change 14 from P3 to P2) has merit but weak grounding

Devils-advocate argues that the architectural note about future consumers applying the same heading validation (synthesis Change 14) should be elevated from P3 to P2 and co-located with the post-write validation text. The reasoning is that a P3 note is "easy to skip" when the spec 008 author reads spec 007.

The tension: priority tiers in this deliberation reflect implementation urgency, not importance to future readers. A P3 item is not "unimportant" -- it is "optional for this spec." The spec 008 author's reading of spec 007 is not governed by priority tiers; it is governed by the spec's structure and the sections relevant to the artifact they consume. If the validation contract is in the schema section (where I advocate it belongs, and devils-advocate now agrees), spec 008's author will find it there regardless of whether it is tagged P2 or P3.

Devils-advocate's real concern is discoverability, not priority. The fix for discoverability is placement (which we agree on: adjacent to the schema), not priority elevation.

**My position**: Accept co-location with the schema section. Maintain P3 priority. The priority tier is a signal to implementers of spec 007 about what to do now, not a reading guide for future spec authors.

---

### T-4: Rec-8's acceptance of arbiter's normative/recommended distinction is correct but could undermine observability

Devils-advocate accepts the arbiter's distinction between the four-rule normative contract and the diff summary as recommended practice. I agree with this distinction -- I proposed the four-rule formulation. The tension is that devils-advocate fully withdraws the observability concern by downgrading the diff summary from "structural requirement" to "recommended practice."

The diff summary is the only mechanism by which a user (especially the non-expert user at spec.md L87) can verify that a refine operation respected the four-rule contract. Without it, the user must manually diff the before/after `problem.md` to confirm headings were preserved and Source Documents were unioned. The four rules are testable post-conditions, but they are testable by the *implementer* (the agent), not by the *user*.

I maintain my Round 2 position that the diff summary is recommended practice, not normative. But I note the tension: the non-expert user principle that devils-advocate frequently invokes elsewhere in their review argues for making the refine operation's effects visible. The recommended-practice framing is correct, but it should be a strong recommendation, not a throwaway note.

**My position**: No change to the priority or classification. The tension is noted for completeness. The recommended-practice designation is correct.

---

## Safe Agreements

### SA-1: All convergence items (C-1 through C-13) survive Round 2 without reversal

Both reviews confirm all 13 convergence items from Round 1. Devils-advocate explicitly states "I affirm all Round 1 convergence points without reversal." My review confirms the same. The three P1 changes (post-write validation, path validation, dispatch matching) and all P2/P3 changes are settled. This is the deliberation's core output and it is stable.

---

### SA-2: All five Round 1 concessions from devils-advocate are maintained

Devils-advocate confirms all five concessions from Round 1: consumer-side gate enforcement withdrawn in favor of `## Status`, content hash over modification timestamp, taxonomy closure self-contradiction fixed, four-rule refine contract accepted, `--type` override flag withdrawn. No reversals. This narrows the remaining dispute surface significantly.

---

### SA-3: RD-3 (multi-path `--context`) and RD-4 (`--force`/`--dry-run`) are fully resolved

Devils-advocate accepts deferral on both disputes, adopting the 2-1 majority position and the arbiter's reasoning. On RD-3, devils-advocate accepts that SKILL.md L797's directory support is the designed multi-source mechanism, not a workaround. On RD-4, devils-advocate accepts the non-expert user principle as the grounding for fewer flags. Both are now consensus positions across all reviewers. The documentation notes (synthesis Changes 11 and 13) are agreed as sufficient.

---

### SA-4: `## Status` as factual annotation (the field itself)

Setting aside the DC-2 tension about enforcement, both reviews agree on the substance: `## Status` should be a factual annotation reporting the artifact's completeness state. Devils-advocate adopts the arbiter's descriptive framing. My review adopts it as well. The field is not advisory, not binding -- it is descriptive. It states a measurable property (count of `[CLARIFY:]` tags). The non-expert user benefits from seeing this in the artifact (spec.md L87). The define handler already computes the data (SKILL.md L865). Writing it into the artifact is low-cost and high-value.

---

### SA-5: Schema-layer validation contract placement

Devils-advocate withdraws the "Common Handler Utilities" dispatch-layer proposal from Round 1 and accepts the schema-layer placement for the validation contract. Both reviews now agree that the validation contract belongs alongside the `problem.md` schema (SKILL.md L822-850), not in the dispatch section (SKILL.md L18-34). The arbiter's one-sentence prose formulation is accepted by both reviewers as the right granularity for spec 007.

---

### SA-6: Four-rule refine contract with diff summary as recommended practice

Both reviews accept the four post-conditions (all headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated) as normative, and the diff summary as recommended practice. Devils-advocate explicitly adopts the arbiter's distinction between structural invariants and UX guidance. This resolves RD-5 with full agreement on both the rules and their classification.

---

### SA-7: The spec's dual identity (foundational and scoped) is a real tension

Both reviews acknowledge systemic contradiction SC-1 from the Round 1 synthesis. Devils-advocate calls it "the core tension" and notes the arbiter's characterization of it as "real but manageable." My review addresses it implicitly through the boundary-validation framing. We agree it exists, we agree it is manageable within spec 007, and we agree the `## Status` section and validation contract are the minimal bridges. The disagreement (DC-2 above) is about whether these bridges are sufficient, not about whether the tension is real.
