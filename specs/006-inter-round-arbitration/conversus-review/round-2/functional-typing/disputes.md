# Disputes -- functional-typing (Round 2)

## Remaining Disputes

No remaining disputes. All Round 2 recommendations have three-agent consensus or bilateral agreement with no active opposition.

## Convergence

The following recommendations have full three-agent consensus after the Round 2 revision cycle:

**P1 (3 items, unanimous):**
1. **Add influence_headings to ArbitrationConfig and cooperative.yml** -- Field type: `dict[str, list[str]]` with string keys. `required_headings` serves as binding default. YAML structure finalized. Implementation-ready.
2. **Wire {ARBITRATION_PATHS} into cross-round synthesis template** -- Exact template text specified by integration-architect. Endorsed by all.
3. **Wire {ARBITRATION_RULINGS} into cross-round synthesis template** -- Exact template text specified by integration-architect. Endorsed by all.

**P2 (upgraded to unanimous from Round 1):**
4. **Use Phase enum in validate.py** -- Three-agent consensus (was bilateral in Round 1; game-engine-advocate confirmed no objection in Round 2).
5. **Type VariableDefinition.phases as list[Phase]** -- Three-agent consensus (same upgrade).
6. **Use match/case for phase-specific validation** -- Three-agent consensus (same upgrade).
7. **Document linter static-vs-runtime heading validation boundary** -- Expanded to include influence_headings context: linter validates against binding default; orchestrator validates against influence-specific headings at runtime.
8. **Provisional-resolution marker lifecycle** -- Three-agent convergence on round-scoped markers. Re-opened disputes return to DISPUTES_BEGIN/DISPUTES_END. Mark as unstable per Principle II.
9. **Document config_conditions as metadata-only** -- Unchanged from Round 1.
10. **Template last-mile audit practice** -- Document manual audit practice. Automated linter check is a future spec. Advisory, not blocking.
11. **P2 sub-ordering** -- P2-easy (documentation/path fixes) vs. P2-structural (type system/markers). Integration-architect proposal endorsed by game-engine-advocate.

**P2 (maintained from Round 1):**
12. **Fix conversus.yml doc paths** -- Trivial.
13. **Add PRIOR_ARBITRATION_SECTION field documentation** -- Unchanged.
14. **Verify PRIOR_ARBITRATION_PATH path computation** -- Explicit formula specified by integration-architect.

**P3 (unchanged from Round 1):**
15. **Normalize ConfigCondition operators** -- game-engine-advocate.
16. **Reclassify ErrorType semantic misuses** -- functional-typing.
17. **Create ConversusConfig Pydantic model** -- functional-typing + game-engine-advocate.
18. **Add stagnation-influence interaction documentation** -- integration-architect + game-engine-advocate.
19. **Add PRIOR_ARBITRATION_PATH model_validator** -- functional-typing.
20. **Mark ARBITRATION_RULINGS as conditionally required** -- Deferred.
21. **PHASE_CONTEXT_MODELS with Phase keys** -- functional-typing.

## Final Position Statement

The functional-typing agent's position after the Round 2 deliberation:

Round 2 achieved two significant outcomes for the type-system domain:

1. **influence_headings field type settled**: All three agents converge on `dict[str, list[str]]` with string keys. The rationale is dual: YAML deserialization produces strings (functional-typing) and plugin extensibility requires open string keys (game-engine-advocate). The binding headings use the existing `required_headings` field -- no duplication. This is the correct application of Principle IX's distinction between closed behavioral choices (StrEnum for dispatch) and open registries (str for schema data).

2. **SC1 boundary re-applied to P1 implementation**: The influence_headings data enables runtime heading validation in the orchestrator, not static validation in the linter. Cross-reviewing integration-architect's Rec 3 identified this precision issue. The boundary is now documented for the P1 implementation: the linter validates against `required_headings` (binding default); the orchestrator validates against `influence_headings[level]` at runtime. This extends Round 1 P2 item 6 (document the static-vs-runtime boundary) with concrete influence_headings context.

3. **Phase enum items upgraded to unanimous**: game-engine-advocate's explicit confirmation (Round 2 NEW-1) upgrades P2 items 4, 5, and 12 from bilateral to three-agent consensus.

4. **Provisional-resolution marker lifecycle settled**: Three-agent convergence on round-scoped markers with clear re-opening semantics. Marked as unstable per Principle II.

The deliberation across two rounds has produced implementation-ready specifications for all P1 items and resolved all P2 design questions. No disputes remain. The functional-typing review's blind spot from Round 1 (template last-mile coverage) was addressed in Round 2 by adopting the manual audit practice.
