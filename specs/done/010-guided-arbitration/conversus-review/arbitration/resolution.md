# Cooperative Arbitration — Phase 6: Inter-Round Advisory Arbitration

**Arbiter**: conversus-constitution
**Influence**: advisory
**Trigger**: disputes_remain
**Round**: 1 of 2

---

### Process Note

- This arbitration was activated because disputes remain after Round 1's Phase 5 synthesis.
- 2 disputes remain from the synthesis.
- Agents participating: functional-typing, integration-architect, devils-advocate.
- This is a **cooperative** deliberation with inter-round advisory arbitration.
- As an advisory arbiter, these are opinions for the agents to consider, not binding rulings.

### Decision Framework

The following principles from the grounding document (`specs/010-guided-arbitration/spec.md`) are relevant to the remaining disputes:

- **UX Layer, Not Engine Override** (spec L69): "Must NOT redefine arbitration mechanics. This is a UX layer over spec 001's engine." The handler's role is to make the engine accessible, not to change the engine's behavior.

- **Implementation Gate** (spec L17): "This spec MUST NOT be implemented until spec 001 achieves spec-complete status." The handler depends on the Phase 6 engine being correct and complete.

- **Plain-Language Accessibility** (spec L14-16): "Most users don't know what a 'grounding document' is, what `trigger: disputes_remain` means, or how to write an arbiter identity prompt." The handler exists for non-expert users.

- **Default Influence** (spec L44): "Default to `binding` if the user doesn't have a preference." This is an explicit spec requirement.

- **Standalone Operation** (spec L54): "Works standalone — does not require the guided workflow." Any completed conversus output directory is valid.

- **No Grounding, No Arbiter** (spec L71-72): "Must NOT generate an arbiter without grounding. An arbiter without a decision framework produces arbitrary rulings."

### Advisory Opinions

#### Dispute: Default influence level (binding vs. recommended)

**Positions:**
- **functional-typing + integration-architect**: Keep `binding` as the default, per spec L44 and SKILL.md L222. Changing the handler default without changing the spec creates inconsistency.
- **devils-advocate**: Change to `recommended`. Users without a preference don't understand binding implications. UX wrappers should serve their users.

**Synthesizer's assessment:** Both arguments have merit. The consistency position is structurally correct. The user-safety position is substantively correct. First-time guidance is a viable compromise.

**Advisory opinion:** The spec is explicit at L44: "Default to `binding`." The handler is a UX layer over the engine (spec L69), not a policy override. The spec should be implemented as written. However, devils-advocate raises a legitimate UX concern. The compromise — first-time guidance suggesting `recommended` (devils-advocate modified Rec 5) — is the correct path because it preserves spec compliance while addressing user safety.

If the project later determines that `recommended` is the better universal default, that decision belongs in a spec revision that updates L44, not in a handler-level override. The handler should not silently deviate from the spec.

**Grounding citation:** "UX Layer, Not Engine Override" (spec L69) — the handler is a UX wrapper, not a policy engine. "Default Influence" (spec L44) — the spec explicitly states the default.

**Rationale:** The distinction between "implement the spec correctly" and "the spec itself should change" is important. Devils-advocate's recommendation is better framed as a spec revision proposal, not a handler implementation detail. The handler's job is to implement L44 faithfully. The guidance note is the correct mechanism to address user safety within the current spec.

**Consideration:** Keep `binding` as the handler default. Adopt first-time guidance. Consider a future spec revision to change L44 if user feedback supports it.

#### Dispute: Dispute preview as subsystem extension vs. additive change

**Positions:**
- **integration-architect**: Adding label extraction to the Dispute-Parsing Subsystem is an interface change requiring formal documentation.
- **devils-advocate**: It's an additive, non-breaking change that uses existing parsing logic.

**Synthesizer's assessment:** Both positions can be satisfied through documentation. The feature is valuable and the interface expansion is real.

**Advisory opinion:** Both agents are right, and the dispute is largely terminological. Integration-architect is correct that the subsystem's output types expand — this should be documented. Devils-advocate is correct that the expansion is additive and non-breaking — existing consumers are unaffected.

The productive framing is: "The Dispute-Parsing Subsystem evolves to support three output types: boolean, integer, and label list. This is an additive change. Existing consumers (Phase 6 trigger, stagnation detection) are unaffected." This satisfies integration-architect's documentation requirement and devils-advocate's argument that it's non-breaking.

**Grounding citation:** "Standalone Operation" (spec L54) — the handler needs to work with any completed output. Providing dispute context helps users make informed decisions about arbitration, which serves the plain-language accessibility goal (spec L14-16).

**Rationale:** The subsystem's stable interface contract (SKILL.md L777) protects the markers and headings, not the output types. Adding a new output type is consistent with the contract. The real requirement is documentation, not governance.

**Consideration:** Adopt dispute preview. Document the new label-list output type alongside existing outputs. Frame as additive subsystem evolution.

### Considerations for Next Round

1. **Default influence level** (from Dispute 1): Keep `binding`, adopt first-time guidance, consider spec revision for future. Priority: P2.
2. **Dispute preview** (from Dispute 2): Adopt feature, document subsystem evolution. Priority: P3.

### Confidence Assessment

| Dispute | Opinion | Confidence | Basis |
|---------|---------|------------|-------|
| Default influence level | Keep binding, adopt guidance | High | Spec L44 is explicit; the handler is a UX layer (L69), not a policy override |
| Dispute preview scope | Adopt and document as evolution | High | The expansion is clearly additive; documentation resolves both agents' concerns |

The deliberation quality is high. Both disputes are genuine design tensions, not misunderstandings. The agents engaged substantively with each other's positions and made meaningful concessions in Phase 3. The 2 remaining disputes reflect fundamental design questions (power-user defaults vs. guided-user safety; subsystem interface governance) that are best resolved through spec-level decisions rather than handler-level compromises.
