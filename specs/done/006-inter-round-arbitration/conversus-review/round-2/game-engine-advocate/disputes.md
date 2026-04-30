# Disputes -- game-engine-advocate (Round 2)

## Remaining Disputes

No remaining disputes. All Round 2 recommendations have three-agent consensus or no active opposition.

## Convergence

The following recommendations have full three-agent consensus after the Round 2 revision cycle:

**P1 (3 items, unanimous across both rounds):**
1. **Influence-aware heading data in ArbitrationConfig + cooperative.yml** -- Field type `dict[str, list[str]]` with string keys settled unanimously. YAML structure finalized. Implementation-ready.
2. **Wire {ARBITRATION_PATHS} into cross-round synthesis template** -- Template text specified and endorsed by all.
3. **Wire {ARBITRATION_RULINGS} into cross-round synthesis template** -- Template text specified and endorsed by all.

**P2 (new three-agent convergence in Round 2):**
4. **Phase enum in validate.py** -- game-engine-advocate confirmed no objection (Round 2 NEW-1).
5. **VariableDefinition.phases as list[Phase]** -- game-engine-advocate confirmed no objection.
6. **match/case for phase-specific validation** -- game-engine-advocate confirmed no objection.
7. **Provisional-resolution marker lifecycle** -- Three-agent convergence: round-scoped, re-opened disputes return to DISPUTES_BEGIN/DISPUTES_END, marked as unstable per Principle II.
8. **P2 sub-ordering** -- P2-easy vs. P2-structural endorsed by game-engine-advocate (Round 2 NEW-2).
9. **Template last-mile audit practice** -- Manual practice now, automated check later (advisory, not blocking).
10. **SC1 boundary documentation for influence_headings** -- Linter validates binding default; orchestrator validates influence-specific headings at runtime.

**P2 (maintained from Round 1):**
11. **Fix conversus.yml doc paths** -- Trivial.
12. **Document config_conditions as metadata-only** -- Principle IV grounded.
13. **Add PRIOR_ARBITRATION_SECTION field documentation** -- Unchanged.
14. **Verify PRIOR_ARBITRATION_PATH formula** -- Explicit formula specified.
15. **Document static-vs-runtime boundary** -- Extended with influence_headings context.

**P3 (unchanged from Round 1):**
16. **Normalize ConfigCondition operators** -- game-engine-advocate.
17. **Document stagnation-influence interaction** -- game-engine-advocate + integration-architect.
18. **ConversusConfig Pydantic model** -- P3, deferred.
19. **Other P3 items** -- Unchanged.

## Final Position Statement

The game-engine-advocate's position after the Round 2 deliberation:

Round 2 achieved the game-engine-advocate's primary objective: ensuring the P1 implementation preserves game engine extensibility. The key results:

1. **String-keyed influence_headings**: The `dict[str, list[str]]` type uses string keys, not InfluenceLevel enum keys. Plugin-defined influence levels can add heading data by extending the YAML schema without modifying core Pydantic enums. This is the correct Principle IX application for schema data (open registry) vs. runtime dispatch (closed enum).

2. **Provisional-resolution marker lifecycle settled**: The convergence predictor can rely on structural markers alone (no prose parsing). Re-opened disputes move back to DISPUTES_BEGIN/DISPUTES_END, and the PROVISIONALLY_RESOLVED markers are round-scoped. This satisfies Principle VIII (templating over inference) for both the current system and the future game engine.

3. **Template last-mile audit**: The manual practice prevents the class of errors (dead template variables) that the game-engine-advocate missed in Round 1. The automated linter check is a future enhancement that should be advisory, not blocking, to accommodate variables provisioned for future specs.

4. **Phase enum items confirmed**: game-engine-advocate explicitly confirmed no objection to P2 items 4, 5, and 12. The factory extension pattern handles plugin phases correctly -- the match/case default branch is the right design for extensibility.

The game-engine-advocate's core finding remains unchanged across both rounds: spec 006 makes no decisions that would require rework when the game engine ships. The architecture is structurally sound, the extensibility is preserved, and the implementation specifications are precise enough for single-pass implementation.
