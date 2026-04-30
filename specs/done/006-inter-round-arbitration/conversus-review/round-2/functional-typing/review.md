# Review -- functional-typing (Round 2)

## Executive Summary

Round 1 produced unanimous convergence on the three P1 items: influence-aware heading data in ArbitrationConfig + cooperative.yml, wiring {ARBITRATION_PATHS} into the cross-round synthesis template, and wiring {ARBITRATION_RULINGS} into the cross-round synthesis template. The advisory arbitration confirmed all three as well-grounded in constitutional principles II and VIII. No Round 1 concessions are reversed.

Round 2 focuses on refining the implementation details of P1 items and advancing the P2 tier, particularly the Phase enum adoption (items 4, 5, 12), the config_conditions documentation (item 9), and the provisional-resolution marker design (item 7). The arbiter raised two substantive considerations that warrant engagement: the provisional-resolution marker lifecycle (AO-5) and the P2 internal prioritization (Consideration 3).

The most important recommendation for this round: finalize the `influence_headings` field type and YAML structure so that the P1 implementation is unambiguous.

## Alignment

- **StrEnum implementation is correct** (`models.py`, L24-43): InfluenceLevel and ArbiterTiming are properly implemented as StrEnums with factory extension documentation. This was confirmed by all three agents and the arbiter (AO-1). Reference: `constitution.md`, Principle IX — closed behavioral choices MUST use StrEnum.

- **Phase enum exists and is comprehensive** (`models.py`, L77-89): The Phase StrEnum covers all seven phases with correct string values. The VALID_PHASES alias maintains backward compatibility. Reference: `constitution.md`, Principle IX.

- **ArbitrationContext has typed INFLUENCE_LEVEL** (`models.py`, L360): The field uses `InfluenceLevel` enum type with a default of `BINDING`. This is correct per Principle IX — the type annotation constrains the value to the closed behavioral set. Reference: `constitution.md`, Principle IX.

- **Pydantic model immutability** (`models.py`, L247): `TemplateContext` uses `frozen=True` and `extra: "forbid"`, preventing runtime mutation and undeclared fields. This is correct functional programming practice. Reference: `python-functional-howto.md`.

## Missed Opportunities

- **Phase enum not used in validate.py function signatures** (`validate.py`, L248, L258, L270, L293): The `check_required_headings` and `check_structural_markers` functions accept `phase` as `str`, then compare it against string literals (`"arbitration"`, `"synthesis"`, `"cross-round-synthesis"`). The Phase enum exists in models.py but is imported only as `VALID_PHASES` (the frozenset alias). Impact: medium. This was P2 in Round 1 (item 4); the arbiter confirmed the constitutional grounding (AO-4).

- **VariableDefinition.phases remains list[str]** (`models.py`, L144): The field uses `list[str]` with a manual `validate_phases` validator (L160-169). Changing to `list[Phase]` would eliminate the validator entirely — Pydantic handles validation through the type. Impact: medium. This is Round 1 P2 item 5.

- **No match/case in phase-specific validation** (`validate.py`, L248-282): The `check_required_headings` function uses three sequential `if` blocks for phase-specific logic. `match`/`case` with `Phase` enum would make the branching exhaustive and the default case explicit. Impact: low-medium. This is Round 1 P2 item 12; the arbiter notes this is a maintainability improvement (AO-4).

- **config_conditions metadata-only gap undocumented** (`variables.yml`, L93-168): Seven variables declare config_conditions that the linter does not evaluate. The schema text creates false precision — it promises conditional enforcement that does not exist. Impact: medium. The arbiter specifically grounds this in Principle IV (AO-3): schema text IS the documentation, and if it makes promises the system cannot keep, that is a documentation-as-product problem.

- **ArbitrationConfig lacks influence_headings field** (`models.py`, L191-194): The model has only `required_headings: list[str]`. No field exists to hold influence-level-specific heading alternatives. This is the P1 gap — the YAML schema and Pydantic model must both gain this data. Impact: high.

- **PHASE_CONTEXT_MODELS uses str keys** (`models.py`, L378-386): The dict maps string keys to context model types. Using `Phase` enum keys would be consistent with the Phase enum adoption. Impact: low.

## Off-Base Assumptions

- No off-base assumptions about the type system domain. The spec and implementation are consistent in their type-system design. The gaps are omissions (unused enums, untyped fields), not incorrect assumptions.

## Actionable Recommendations

1. **Finalize influence_headings field type** (Priority: P1)
   - **Current state**: ArbitrationConfig has only `required_headings: list[str]` (models.py L194). cooperative.yml has four required headings (cooperative.yml L41-44).
   - **Proposed change**: Add `influence_headings: dict[str, list[str]] = Field(default_factory=dict)` to ArbitrationConfig. The keys are influence level strings (not InfluenceLevel enum, because YAML deserialization produces strings and mode schema files should not require enum awareness). The values are heading lists for non-binding influence levels. The existing `required_headings` serves as the `binding` headings — no duplication needed.
   - **Rationale**: Constitution Principle VIII — mechanical template-driven heading selection rather than agent inference. All three agents and the arbiter (AO-1) converge on this as the top gap.
   - **Risk if ignored**: Arbitration output validation uses binding headings for advisory/recommended runs, producing false positive validation warnings.

2. **Add influence_headings to cooperative.yml** (Priority: P1)
   - **Current state**: cooperative.yml arbitration section has only `required_headings` (L39-44).
   - **Proposed change**: Add:
     ```yaml
     arbitration:
       required_headings:
         - Process Note
         - Decision Framework
         - Binding Decisions
         - Summary of Changes Required
       influence_headings:
         recommended:
           - Process Note
           - Decision Framework
           - Recommended Resolutions
           - Suggested Changes
         advisory:
           - Process Note
           - Decision Framework
           - Advisory Opinions
           - Considerations for Next Round
     ```
   - **Rationale**: This makes the heading mapping declarative and lintable. The `binding` case uses `required_headings` directly — no duplication.
   - **Risk if ignored**: Heading validation has no structured source of truth for non-binding influence levels.

3. **Use Phase enum in validate.py** (Priority: P2)
   - **Current state**: validate.py uses string comparisons for phase-specific logic (L248, L258, L270).
   - **Proposed change**: Import `Phase` from models.py. Type the `phase` parameter in `check_required_headings` and `check_structural_markers` as `Phase`. Replace string literals with enum members.
   - **Rationale**: Constitution Principle IX — closed behavioral choices MUST use StrEnum. The arbiter confirms this grounding (AO-4).
   - **Risk if ignored**: New phases added to the Phase enum but not to the string comparisons would be silently ignored.

4. **Type VariableDefinition.phases as list[Phase]** (Priority: P2)
   - **Current state**: `phases: list[str]` with manual validator (models.py L144, L160-169).
   - **Proposed change**: Change to `phases: list[Phase]`. Remove `validate_phases` — Pydantic handles validation through the type.
   - **Rationale**: Eliminates redundant validation code. The type annotation is the validation.
   - **Risk if ignored**: Redundant validator code that can drift from the Phase enum.

5. **Document config_conditions as metadata-only** (Priority: P2)
   - **Current state**: variables.yml declares config_conditions on 7+ variables. The linter does not evaluate them. No documentation acknowledges this gap.
   - **Proposed change**: Add a comment block in the variables.yml header and in validate.py noting that config_conditions are schema metadata for documentation purposes and are not evaluated by the linter at runtime.
   - **Rationale**: Constitution Principle IV — documentation IS the product. The arbiter reinforces this (AO-3): if the schema makes a promise the system cannot keep, that is a Principle IV violation.
   - **Risk if ignored**: Future implementers may assume config_conditions are enforced and build incorrect logic on that assumption.

6. **Address provisional-resolution marker lifecycle** (Priority: P2)
   - **Current state**: Round 1 proposed PROVISIONALLY_RESOLVED_BEGIN/END markers (P2 item 7). The arbiter (AO-5) raises a lifecycle question: what happens when a provisionally resolved dispute is re-opened?
   - **Proposed change**: The marker design should specify that re-opened disputes move back inside DISPUTES_BEGIN/DISPUTES_END in the next round's synthesis. The PROVISIONALLY_RESOLVED markers exist only within a single round's synthesis — they are not carried forward. Each round's synthesizer categorizes disputes based on the current round's state.
   - **Rationale**: Principle II — structural markers are stable contracts. The lifecycle must be specified before the markers are declared stable.
   - **Risk if ignored**: Ambiguous marker semantics create unstable contracts, violating Principle II.

7. **Use PHASE_CONTEXT_MODELS with Phase keys** (Priority: P3)
   - **Current state**: `PHASE_CONTEXT_MODELS: dict[str, type[TemplateContext]]` (models.py L378).
   - **Proposed change**: Change to `dict[Phase, type[TemplateContext]]` with Phase enum keys.
   - **Rationale**: Consistency with Phase enum adoption. The runtime assertion (L390-394) already validates alignment — using Phase keys makes this structural rather than asserted.
   - **Risk if ignored**: Minor inconsistency between declared types and actual usage.

## Referenced Documentation

- `constitution.md` — Principle IV (L65-77), Principle VIII (L121-139), Principle IX (L141-194)
- `python-functional-howto.md` — pure functions, immutable data structures
- `models.py` — L24-43 (StrEnums), L77-89 (Phase), L191-194 (ArbitrationConfig), L247 (TemplateContext), L378-394 (PHASE_CONTEXT_MODELS)
- `validate.py` — L248-282 (check_required_headings), L285-312 (check_structural_markers)
- `variables.yml` — L93-168 (config_conditions variables)
- `cooperative.yml` — L39-44 (arbitration section)
- Round 1 synthesis — P1 items 1-3, P2 items 4-5, 9, 12
- Arbitration resolution — AO-1, AO-3, AO-4, AO-5
