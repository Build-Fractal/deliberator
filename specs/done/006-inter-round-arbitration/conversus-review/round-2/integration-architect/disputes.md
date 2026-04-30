# Disputes -- integration-architect (Round 2)

## Remaining Disputes

No remaining disputes. All Round 2 recommendations have three-agent consensus or no active opposition. The SC1 boundary correction from functional-typing was accepted without disagreement.

## Convergence

The following recommendations have full three-agent consensus after the Round 2 revision cycle:

**P1 (3 items, unchanged, implementation-ready):**
1. **Add influence_headings to ArbitrationConfig and cooperative.yml** -- Field type: `dict[str, list[str]]`. YAML structure: two entries (recommended, advisory) under `influence_headings` key. `required_headings` serves as binding default. Pydantic field: `influence_headings: dict[str, list[str]] = Field(default_factory=dict)`. Static-vs-runtime boundary: linter validates binding default; orchestrator validates influence-specific headings at runtime.
2. **Wire {ARBITRATION_PATHS} into cross-round synthesis template** -- Template text: conditional reading instruction in "What to Read" section. Exact wording specified.
3. **Wire {ARBITRATION_RULINGS} into cross-round synthesis template** -- Template text: pre-formatted arbiter rulings in Resolution Attribution section. Exact wording specified.

**P2 (upgraded to unanimous in Round 2):**
4. **Use Phase enum in validate.py** -- Three-agent consensus.
5. **Type VariableDefinition.phases as list[Phase]** -- Three-agent consensus.
6. **Use match/case for phase-specific validation** -- Three-agent consensus.
7. **Document linter static-vs-runtime boundary (extended)** -- Include influence_headings context.
8. **Provisional-resolution markers** -- Round-scoped lifecycle, unstable per Principle II.
9. **Document config_conditions as metadata-only** -- Principle IV.
10. **Fix conversus.yml doc paths** -- Trivial.
11. **Add PRIOR_ARBITRATION_SECTION documentation** -- Unchanged.
12. **Specify PRIOR_ARBITRATION_PATH formula** -- Explicit formula.
13. **P2 sub-ordering** -- P2-easy (documentation/fixes) vs. P2-structural (types/markers).
14. **Template last-mile audit practice** -- Manual practice now; advisory automated check later.

**P3 (unchanged from Round 1):**
15-21. All P3 items unchanged. No priority adjustments.

## Final Position Statement

The integration-architect's position after the Round 2 deliberation:

Round 2 achieved two critical outcomes for the integration pipeline:

1. **All P1 items are implementation-ready**: The three P1 items have exact specifications:
   - influence_headings: field type settled (`dict[str, list[str]]`), YAML structure settled, static-vs-runtime boundary documented.
   - {ARBITRATION_PATHS}: exact template text for the "What to Read" section.
   - {ARBITRATION_RULINGS}: exact template text for the Resolution Attribution section.

   These specifications are precise enough for single-pass implementation without further deliberation.

2. **SC1 boundary correction accepted**: functional-typing's cross-review identified that the integration-architect's Rec 3 conflated static and runtime validation. The correction is accepted: influence_headings data is consumed by the runtime orchestrator (SKILL.md L640-655), not by the static linter. The linter validates templates against binding-default headings. This correction prevents a future implementation error.

3. **P2 items gained three-agent consensus**: game-engine-advocate's explicit confirmation of Phase enum items (4, 5, 12) upgraded these from bilateral to unanimous. P2 sub-ordering provides an implementation plan. The provisional-resolution marker lifecycle is settled.

4. **No disputes remain**: The deliberation has resolved all disagreements across two rounds. Round 1 resolved the substantive design disputes (config_conditions sequencing, heading validation approach, plugin hook comments). Round 2 resolved the implementation precision questions (field types, static-vs-runtime boundaries, marker lifecycle, sub-ordering).

The integration-architect's core contribution across both rounds: identifying and resolving the template wiring gaps ({ARBITRATION_PATHS}, {ARBITRATION_RULINGS}) that represented dead infrastructure. The influence_headings gap was identified by all three agents. The P2 sub-ordering and template last-mile audit practice are pragmatic contributions that enable incremental implementation.
