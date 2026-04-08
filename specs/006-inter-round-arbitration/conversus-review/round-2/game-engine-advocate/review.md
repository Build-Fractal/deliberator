# Review -- game-engine-advocate (Round 2)

## Executive Summary

Round 1 established that spec 006 makes no decisions requiring rework when the game engine ships. That finding stands. Two recommendations were correctly withdrawn (plugin hook comments, influence dispatch externalization) as premature for an archived spec. The three P1 items (influence-aware heading data, wiring ARBITRATION_PATHS, wiring ARBITRATION_RULINGS) achieved unanimous consensus and advisory arbitration confirmation.

Round 2 focuses on three areas where the game-engine-advocate perspective adds value to the remaining P2 items: (1) the provisional-resolution marker design, which directly affects the convergence predictor's accuracy; (2) the influence_headings YAML structure, which must be plugin-extensible; and (3) the template last-mile audit as a standing practice, which the arbiter flagged as a systemic observation (Consideration 1).

The most important recommendation for this round: ensure the provisional-resolution marker lifecycle is fully specified before the markers are declared stable, because the convergence predictor depends on accurate dispute state categorization.

## Alignment

- **InfluenceLevel StrEnum extensibility** (`models.py`, L24-33): The factory extension pattern documented in the docstring correctly supports plugin-defined influence levels. The arbiter's confirmation (AO-7) that building ConversusConfig should wait for a concrete consumer reinforces the game engine position — build abstractions when needed.

- **Inter-round execution ordering** (`SKILL.md`, L316-335): The Phase 5 -> Phase 6 (conditional) -> termination check ordering is correct for convergence prediction. The arbiter's AO-1 confirms that the dead template variables are the real gap, not the execution ordering itself.

- **Influence model taxonomy** (`spec.md`, L199-213): The three-tier influence model (binding/recommended/advisory) correctly maps to game-theoretic mechanism design roles (dictator/mediator/observer). This mapping is stable and extensible.

- **Backward compatibility** (`spec.md`, L237-242): Omitting `timing` and `influence` produces pre-spec-006 behavior. The defaults (`final`, `binding`) are correctly implemented. This was confirmed by all agents and the arbiter.

## Missed Opportunities

- **Provisional-resolution marker lifecycle unspecified**: The Round 1 synthesis included P2 item 7 (PROVISIONALLY_RESOLVED_BEGIN/END markers), but the arbiter (AO-5) identified a critical gap: the spec does not define what happens when a provisionally resolved dispute is re-opened (FR-012). For the convergence predictor, this matters: if re-opened disputes remain in the PROVISIONALLY_RESOLVED section with a "re-opened" annotation, the predictor must parse annotations. If they move back to DISPUTES_BEGIN/END, the predictor can rely on structural markers alone. Impact: high for game engine integration.

- **Template last-mile audit not formalized**: The arbiter (Consideration 1) notes that all three agents missed the dead template variables in their original Round 1 reviews. The arbiter suggests a standing practice: "For every variable provisioned in the schema, is there at least one template that references it?" This could eventually be automated in the linter. Impact: medium. This is a systemic improvement that would prevent the class of errors the integration-architect caught.

- **Cross-round synthesis template still lacks ARBITRATION_PATHS/RULINGS references**: This is the P1 gap identified in Round 1. The template at `templates/cooperative/cross-round-synthesis.md` does not reference `{ARBITRATION_PATHS}` or `{ARBITRATION_RULINGS}` despite both being fully provisioned. The game engine's post-deliberation hooks would consume these same variables. Impact: high — this is the P1 item.

- **No stagnation-influence interaction documentation**: The arbiter (Consideration 4) raises a subtle feedback loop: an arbiter with `recommended` influence can prevent stagnation detection from firing by provisionally resolving disputes, even if agents subsequently re-open them. This interaction should be documented. Impact: medium, especially for the convergence predictor.

## Off-Base Assumptions

- No off-base assumptions about the game engine domain. The spec correctly treats the game engine as an archived future direction. The arbiter's confirmation (AO-6) that the withdrawn recommendations were correctly withdrawn validates the YAGNI discipline applied in Round 1.

## Actionable Recommendations

1. **Specify provisional-resolution marker lifecycle** (Priority: P2)
   - **Current state**: Round 1 P2 item 7 proposes PROVISIONALLY_RESOLVED_BEGIN/END markers. The arbiter (AO-5) asks: what happens when a provisionally resolved dispute is re-opened?
   - **Proposed change**: Define the lifecycle explicitly: re-opened disputes move back to the DISPUTES_BEGIN/DISPUTES_END section in the next round's synthesis. PROVISIONALLY_RESOLVED markers are round-scoped — each round's synthesizer categorizes disputes fresh based on the current round's evidence. The markers are not carried forward between rounds.
   - **Rationale**: The convergence predictor needs unambiguous dispute state from structural markers. If re-opened disputes stay in PROVISIONALLY_RESOLVED with annotations, the predictor must parse prose. If they move to DISPUTES, the predictor can use markers alone. The latter is consistent with Principle VIII (templating over inference).
   - **Risk if ignored**: Convergence predictor accuracy degrades; dispute counting becomes inference-dependent.

2. **Ensure influence_headings YAML is plugin-extensible** (Priority: P1-design)
   - **Current state**: The proposed influence_headings structure uses string keys (influence level names) mapping to heading lists.
   - **Proposed change**: Confirm that the YAML structure uses string keys (not enum-constrained keys) so that plugin-defined influence levels can add entries without modifying the core schema file. The Pydantic model should use `dict[str, list[str]]` (not `dict[InfluenceLevel, list[str]]`) to accommodate future plugin-defined influence levels.
   - **Rationale**: Constitution Principle IX distinguishes closed behavioral choices (StrEnum) from open registries (str with validation). The influence_headings mapping is schema data, not runtime dispatch — it should be open to extension.
   - **Risk if ignored**: Plugin-defined influence levels cannot provide heading data without modifying the core cooperative.yml schema.

3. **Formalize template last-mile audit** (Priority: P2)
   - **Current state**: The linter validates that templates reference known variables and that required variables are present. It does not check whether schema-provisioned variables are consumed by at least one template.
   - **Proposed change**: Add a linter check (or document the manual audit practice) that verifies: for every variable in variables.yml with `required: false`, at least one template in the corresponding phase references it. Variables with `required: true` are already checked. This catches dead infrastructure like ARBITRATION_PATHS/RULINGS.
   - **Rationale**: Arbiter Consideration 1 — all three agents missed this gap. A mechanical check prevents the class of errors.
   - **Risk if ignored**: Dead infrastructure accumulates as new variables are provisioned for future specs.

4. **Document stagnation-influence interaction** (Priority: P3)
   - **Current state**: SKILL.md documents stagnation detection (L524-531) and influence-aware dispute counting (L503-508) separately. The interaction is not documented.
   - **Proposed change**: Add a paragraph to SKILL.md connecting the two: explicitly state that `recommended` influence provisionally reduces the dispute count for stagnation purposes, but re-opened disputes restore the count. Note the feedback loop: an arbiter that provisionally resolves disputes can prevent stagnation detection even if agents consistently re-open them.
   - **Rationale**: Arbiter Consideration 4 — the feedback loop is subtle and could produce surprising behavior in practice.
   - **Risk if ignored**: Users may not understand why stagnation is not detected when an arbiter with `recommended` influence is active.

5. **Maintain game engine structural compatibility** (Priority: confirmation)
   - **Current state**: All Round 1 findings confirmed by the arbiter. The spec makes no decisions requiring game engine rework.
   - **Proposed change**: No change needed. Confirm that the P1 influence_headings implementation (both YAML structure and Pydantic field type) preserves the extensibility the game engine will need.
   - **Rationale**: The game engine's convergence predictor and post-deliberation hooks depend on the data structures established in spec 006. Verifying compatibility in Round 2 prevents surprises.
   - **Risk if ignored**: Minimal — the architecture is sound. This is a confirmation, not a new finding.

## Referenced Documentation

- `specs/archive/game-engine-vision/spec.md` — convergence predictor, post-deliberation hooks
- `specs/archive/game-engine-vision/ideation-context.md` — plugin architecture vision
- `constitution.md` — Principle II (stable interfaces), Principle VIII (templating over inference), Principle IX (StrEnum vs open registries)
- `models.py` — L24-33 (InfluenceLevel), L191-194 (ArbitrationConfig)
- `SKILL.md` — L316-335 (execution ordering), L503-508 (influence-aware counting), L524-531 (stagnation)
- `templates/cooperative/cross-round-synthesis.md` — missing ARBITRATION_PATHS/RULINGS references
- Round 1 synthesis — P1 items 1-3, P2 item 7, P3 item 16
- Arbitration resolution — AO-1, AO-5, AO-6, AO-7, Considerations 1, 4
