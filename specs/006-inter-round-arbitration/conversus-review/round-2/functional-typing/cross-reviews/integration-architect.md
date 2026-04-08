# Cross-Review: functional-typing reviewing integration-architect (Round 2)

## Overall Assessment

integration-architect's Round 2 review is implementation-oriented and thorough. The focus on producing implementation-ready specifications for P1 items is the right priority for a final round. The concrete template wording proposals (Recs 1 and 2) provide exact text that could be inserted without further deliberation. The P2 sub-ordering (Rec 4) is a pragmatic contribution that the arbiter suggested (Consideration 3).

## Recommendation-by-Recommendation Assessment

### Rec 1: Wire {ARBITRATION_PATHS} into cross-round synthesis template (P1)

**Strong agreement.** The proposed template text is precise and actionable:
```markdown
3. **Per-round arbitration resolutions** (if inter-round arbitration was configured):
{ARBITRATION_PATHS}
```
This directly addresses the dead infrastructure gap. The conditional framing ("if inter-round arbitration was configured") is correct -- when `{ARBITRATION_PATHS}` is empty string (no inter-round arbitration), the section renders as a reading instruction with no paths, which the synthesizer can skip. No issues with this proposal.

### Rec 2: Wire {ARBITRATION_RULINGS} into cross-round synthesis template (P1)

**Strong agreement.** The proposed placement in the Resolution Attribution section is correct. The instruction "cite the specific round and ruling rather than summarizing from the round synthesis" is a direct application of Principle VIII -- use the structured data, do not infer. The template text is actionable.

### Rec 3: Add influence_headings to cooperative.yml and ArbitrationConfig (P1)

**Strong agreement with one type-system observation.** The proposed field type `dict[str, list[str]]` aligns with functional-typing's Round 2 Rec 1 and game-engine-advocate's Round 2 Rec 2. All three agents independently converge on string keys rather than enum keys for the YAML-facing field. Good.

The integration-architect also specifies the linter behavior: "use `influence_headings[level]` when the level is non-binding, falling back to `required_headings` for `binding`." This fallback logic is correct and should be added to the linter's `check_required_headings` function. The current function (validate.py L248-256) only uses `mode_schema.arbitration.required_headings`. The change would be: when the phase is `arbitration` and an `influence_level` parameter is provided (from the template's `{INFLUENCE_LEVEL}` variable... but wait: the linter validates templates statically, not at runtime. The linter does not know the influence level at validation time.

This is the SC1 boundary again. The linter validates that the template has the `{INFLUENCE_LEVEL}` variable and that the mode schema has influence_headings data. The runtime orchestrator validates that the actual headings in the arbitration output match the influence-level-specific headings. The linter cannot validate influence-specific headings statically.

Suggesting that the integration-architect clarify: the influence_headings data enables runtime heading validation (in SKILL.md L640-655), not linter-time validation. The linter continues to validate against `required_headings` (the binding default) for static template validation.

### Rec 4: Establish P2 implementation sub-ordering (P2-meta)

**Agreement.** The P2-easy vs. P2-structural distinction maps cleanly to implementation effort and risk. P2-easy items (documentation, path fixes) can be implemented in a single pass. P2-structural items (Phase enum, VariableDefinition.phases, provisional markers, match/case) require testing. This is pragmatic prioritization, not a priority override.

### Rec 5: Specify PRIOR_ARBITRATION_PATH formula explicitly (P2)

**Agreement.** The explicit formula (`{output}/round-{R-1}/arbitration/resolution.md`) with the conditional ("if arbitration did not fire, set to empty string") is deterministic and reproducible. This is Principle VII.

### Rec 6: Address provisional-resolution marker lifecycle (P2)

**Strong agreement.** The integration-architect's proposal aligns with both functional-typing (Round 2 Rec 6) and game-engine-advocate (Round 2 Rec 1): markers are round-scoped, re-opened disputes move back to DISPUTES_BEGIN/DISPUTES_END. The additional observation about Principle II stability (recommend marking as unstable until validated) is correct and adds value. New stable interfaces should prove themselves before being declared stable.

### Rec 7: Verify template last-mile coverage (P2)

**Agreement with same scope clarification as game-engine-advocate.** The manual audit practice is the immediate action. The linter `--audit` mode is a future enhancement. Both are valuable; the scope should be clear.

## Gaps or Missed Points

- **SC1 boundary in Rec 3**: The integration-architect's Rec 3 says "the linter's heading validation should use influence_headings[level]." This is a runtime validation change, not a linter change. The linter validates templates statically; influence level is a runtime config value. This needs clarification to avoid conflating static and runtime validation.

## Tensions or Contradictions

No substantive tensions. The integration-architect's positions are compatible with functional-typing's positions. The SC1 boundary clarification is a precision issue, not a disagreement.
