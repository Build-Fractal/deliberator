# Inter-Round Arbitration -- Spec 006

**Influence**: advisory
**Arbiter**: conversus-constitution
**Grounding**: constitution.md v1.5.0
**Round**: 1
**Date**: 2026-03-21

---

### Process Note

This arbitration operates at **advisory** influence. The observations below are perspectives grounded in the constitution and the spec under review. Agents are free to disagree with any position stated here. Nothing in this document binds the next round or forecloses any agent's reasoning.

The three agents -- functional-typing, game-engine-advocate, integration-architect -- conducted a substantive deliberation. The cross-review phase produced genuine movement: two recommendations withdrawn, two priorities downgraded, and three recommendations adopted across agent boundaries. The dispute phase resolved all significant disagreements, with one minor sequencing tension (D1/D3: config_conditions) resolved through concession. The synthesis correctly identifies zero dangerous contradictions and three systemic contradictions that are architectural boundaries rather than bugs.

This is a well-functioning deliberation. The advisory arbitration that follows is offered as perspective on the remaining structure, not as correction.

---

### Decision Framework

The constitution provides the grounding for these observations. The relevant principles, in order of applicability to the disputes and recommendations at hand:

1. **Principle II (Stable Interfaces)**: Structural markers, template variables, and dispute-parsing subsystems are stable contracts. This is directly relevant to the dead template variable findings ({ARBITRATION_PATHS}, {ARBITRATION_RULINGS}) and the proposed provisional-resolution markers.

2. **Principle III (Backward-Compatible Extension)**: New features extend existing behavior; omitting optional fields preserves prior behavior. This is the standard against which the `timing` and `influence` defaults should be evaluated, and it is the standard the spec satisfies.

3. **Principle IV (Documentation Is the Product)**: In a prompt-orchestrated system, specification text IS the implementation. This is relevant to the config_conditions documentation dispute -- if config_conditions are not evaluated, the schema text creates false expectations, which is a documentation-as-product problem.

4. **Principle VIII (Templating Engines Over Inference)**: Prefer mechanical template-driven behavior over LLM inference. This is relevant to the influence-aware heading data recommendation -- encoding headings as structured data in the schema rather than relying on the agent to infer them from the influence level is a direct application of this principle.

5. **Principle IX (Functional Programming and Clean Code / Explicit Typing)**: StrEnum for closed behavioral choices, Pydantic models for data structures, type annotations on all signatures. This grounds functional-typing's Phase enum and VariableDefinition.phases recommendations.

---

### Advisory Opinions

#### AO-1: The Three P1 Items Are Well-Grounded

The unanimous P1 recommendations -- (1) influence-aware heading data in ArbitrationConfig + cooperative.yml, (2) wiring {ARBITRATION_PATHS} into the cross-round synthesis template, and (3) wiring {ARBITRATION_RULINGS} into the cross-round synthesis template -- are well-grounded in constitutional principles.

Items 2 and 3 are particularly notable. Principle II treats template variables as stable contracts. If a variable is provisioned in the schema, declared in the Pydantic model, and documented in SKILL.md, but the template that is supposed to consume it does not reference it, that variable is dead infrastructure. The cross-round synthesizer would then produce Resolution Attribution by inferring from round syntheses rather than reading the actual arbitration files. This inverts the intent of Principle VIII: the system has the structured data available but forces the agent to infer instead of reading it. All three agents converging on this independently (integration-architect originally, the other two adopting after cross-review) is a signal that this gap is real and consequential.

Item 1 is a direct application of Principle VIII. The influence level determines which headings appear in arbitration output. Encoding those headings as structured YAML data keyed by influence level -- rather than embedding them only in prose instructions and expecting the agent to map influence to headings at runtime -- makes the system more deterministic and lintable.

#### AO-2: The Static-vs-Runtime Boundary Is Correctly Identified

Systemic Contradiction SC1 (static linting vs. runtime configuration) is correctly characterized as intentional architecture, not a bug. The constitution supports this reading: Principle VII (Reproducibility) requires deterministic orchestration, but the determinism operates at the level of "same config produces same prompts." The linter validates template structure; the orchestrator validates runtime content. Documenting this boundary (P2 item 6) is the right intervention -- it prevents a future contributor from treating the gap as a defect and attempting to push runtime logic into the linter.

#### AO-3: config_conditions Documentation Sequencing

The resolved dispute (RD1 / D1 / D3) on config_conditions sequencing was resolved correctly. functional-typing's documentation-first approach is the safer sequencing, and integration-architect's concession reflects sound reasoning: setting `required: true` without an evaluation mechanism creates unconditional enforcement, which is the wrong behavior for conditionally-required variables.

From the constitution's perspective, Principle IV applies here. If the schema declares `config_conditions` with precise operators and field references, but no mechanism evaluates them, the schema text is making a promise the system cannot keep. Documenting this gap is a Principle IV obligation -- the documentation (schema) must accurately describe the system's actual behavior. The gap between declared conditions and enforced conditions is exactly the kind of false precision that misleads future implementers.

#### AO-4: Phase Enum Usage and Exhaustive Matching

The Phase enum recommendations (P2 items 4, 5, 12) are grounded in Principle IX's explicit typing mandate. The constitution states: "Closed behavioral choices (where each value triggers distinct code paths) MUST use StrEnum." Phase names are closed behavioral choices -- adding a new phase requires code changes to the validator. Using string literals where a StrEnum exists creates a category of bug that the type system could prevent.

That said, the downgrade from P1 to P2 was reasonable. The code works correctly with string literals today. The enum exists but is not used in all call sites. This is a maintainability improvement, not a correctness fix.

#### AO-5: Provisional-Resolution Markers

The proposed `PROVISIONALLY_RESOLVED_BEGIN` / `PROVISIONALLY_RESOLVED_END` markers (P2 item 7) introduce a new stable interface. Principle II requires that structural markers be treated as stable contracts. The agents should consider whether these markers need to be documented as stable from their first use, or whether they should be introduced as unstable (subject to revision after one spec cycle consumes them successfully, per Principle II's guidance that "New interfaces SHOULD be marked stable only after at least one spec has consumed them successfully").

The naming convention (`PROVISIONALLY_RESOLVED_*`) parallels `DISPUTES_BEGIN` / `DISPUTES_END`, which is good. But the semantic distinction matters: disputes are a binary state (open/closed), while provisional resolution introduces a third state (open/provisionally-resolved/resolved). The agents may want to consider whether the marker design accounts for the possibility that a provisionally resolved dispute is re-opened -- does it move back inside `DISPUTES_BEGIN`/`DISPUTES_END`, or does it remain in the provisional section with a "re-opened" annotation? The spec (FR-012) defines the behavioral semantics but the marker design should be consistent with them.

#### AO-6: The Withdrawn Recommendations Were Correctly Withdrawn

game-engine-advocate's two withdrawals (plugin hook comments in SKILL.md, influence dispatch externalization) represent good deliberation outcomes. Principle IV states that SKILL.md is the executable truth. Comments referencing an archived spec would create stale references that mislead the orchestrator. The YAGNI argument for influence dispatch externalization is reinforced by the game-engine-advocate's own self-correction (OBA-1) -- when the agent that proposed the abstraction identifies a reason not to build it, that is strong evidence.

#### AO-7: ConversusConfig Pydantic Model (P3) and Extensibility

The ConversusConfig model recommendation (P3 item 15) is correctly prioritized. Principle IX mandates Pydantic models for data structures, but the current system works without this model. The extensibility discussion (`extra: "allow"` vs. `plugins: dict[str, Any]`) is a design decision that benefits from more usage data. P3 is appropriate -- build it when there is a concrete consumer that would benefit from typed config access.

---

### Considerations for Next Round

The following observations are offered for agents to consider in subsequent deliberation, if one occurs. They are not directives.

1. **Template last-mile auditing as a standing practice.** All three agents acknowledged missing the dead template variables in their original reviews. The synthesis correctly identifies this as a systemic blind spot (SC3: Typed Pipeline vs. Template Last-Mile). Future reviews of any conversus spec might benefit from including a final check: "For every variable provisioned in the schema, is there at least one template that references it?" This is a mechanical check that could eventually be automated in the linter.

2. **Provisional-resolution marker lifecycle.** If the markers are adopted, the spec should clarify the full lifecycle: what happens when a provisionally resolved dispute is re-opened (FR-012), and how the markers reflect that state change. This is a design question, not a correctness issue -- but the marker contract should be explicit before it is declared stable.

3. **Priority ordering within P2.** The P2 tier contains 9 items of varying scope: from trivial path fixes (item 8) to structural additions (item 7, provisional markers). Agents may find it useful to distinguish "P2-easy" (items 8, 10: documentation and path fixes) from "P2-structural" (items 4, 5, 7, 12: type system and marker changes) when planning implementation. This is a pragmatic observation, not a priority override.

4. **Stagnation-influence interaction.** P3 item 16 (documenting how influence-adjusted dispute counts interact with stagnation detection) is lower priority in isolation, but becomes important if `timing: inter-round` with `influence: recommended` is used in practice. The interaction between "provisionally resolved disputes reduce the count" and "stagnation detection requires count to decrease" creates a subtle feedback loop: an arbiter with `recommended` influence can prevent stagnation detection from firing by provisionally resolving disputes, even if agents subsequently re-open them. This is worth documenting explicitly, even if not in this spec cycle.

---

### Confidence Assessment

| Area | Confidence | Basis |
|------|-----------|-------|
| P1 items are correctly identified | High | All three agents converged independently; constitutional principles II and VIII directly support |
| Dispute resolution (config_conditions sequencing) was sound | High | Concession was well-reasoned; Principle IV supports documentation-first |
| Withdrawn recommendations were correctly withdrawn | High | YAGNI argument is strong; agent self-correction (OBA-1) reinforces |
| P2 priority tier is reasonable | Medium | Items vary significantly in scope and impact; internal ordering may warrant discussion |
| P3 items are correctly deferred | Medium | Some P3 items (especially stagnation-influence interaction) may become more important depending on real usage patterns |
| No dangerous contradictions exist | High | The three perspectives (type system, extensibility, integration pipeline) are genuinely orthogonal; recommendations compose without conflict |
| Process health | High | Cross-review produced genuine movement (withdrawals, priority changes, adopted findings); agents engaged substantively, not defensively |
