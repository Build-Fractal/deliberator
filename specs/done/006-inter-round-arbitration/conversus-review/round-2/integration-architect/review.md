# Review -- integration-architect (Round 2)

## Executive Summary

Round 1 established three unanimous P1 items and resolved all major disputes. The advisory arbitration confirmed the findings as well-grounded. No Round 1 concessions are reversed. The integration pipeline analysis from Round 1 identified the most consequential gaps (dead template variables), and all agents adopted these findings.

Round 2 narrows focus to three areas: (1) ensuring the P1 implementation specifications are precise enough for a single-pass implementation, (2) advancing the P2 items that the arbiter flagged for internal prioritization (Consideration 3), and (3) addressing the arbiter's substantive observations on provisional-resolution marker lifecycle (AO-5) and template last-mile auditing (Consideration 1).

The most important recommendation for this round: produce implementation-ready specifications for all three P1 items so that the spec 006 changes can be executed without further deliberation.

## Alignment

- **SKILL.md inter-round arbitration section is complete** (`SKILL.md`, L488-509): The inter-round arbitration flow, trigger evaluation, influence-aware dispute counting, and per-round output paths are all specified. The arbiter confirmed this (AO-1, AO-2).

- **Template variables are fully provisioned** (`variables.yml`, L136-190; `models.py`, L362-374): PRIOR_ARBITRATION_PATH, PRIOR_ARBITRATION_SECTION, INFLUENCE_LEVEL, ARBITRATION_PATHS, and ARBITRATION_RULINGS are all defined in the schema, modeled in Pydantic, and documented in SKILL.md. The only gap is the template reference — which is the P1 finding.

- **Backward compatibility preserved** (`SKILL.md`, L185-192; `spec.md`, L237-242): Omitting `timing` and `influence` produces identical behavior to spec 001 + spec 004. Defaults are correctly implemented. The arbiter confirms this is a correct application of Principle III.

- **Output structure is correctly specified** (`SKILL.md`, L234-248; `spec.md`, L80-94): Per-round arbitration at `{output}/round-N/arbitration/resolution.md`, final arbitration at `{output}/arbitration/resolution.md`. The directory structure is deterministic from config.

- **Dispute-parsing subsystem correctly specified** (`SKILL.md`, L626): The REMAINING_DISPUTES extraction logic uses structural markers (primary) with heading-based fallback (degraded). This is consistent with the existing DISPUTES_BEGIN/END contract.

## Missed Opportunities

- **Cross-round synthesis template "What to Read" section omits ARBITRATION_PATHS** (`cross-round-synthesis.md`, L14-24): The template lists target files, per-round syntheses, but no arbitration files. When inter-round arbitration fires, the cross-round synthesizer should read the arbitration resolutions to produce accurate Resolution Attribution. Impact: high — this is P1 item 2.

- **Cross-round synthesis template Resolution Attribution section omits ARBITRATION_RULINGS** (`cross-round-synthesis.md`, L91-100): The Resolution Attribution section instructs the synthesizer to track dispute resolution mechanisms but does not provide the actual arbiter rulings as pre-formatted content. The synthesizer must infer from round syntheses rather than reading the structured data. Impact: high — this is P1 item 3.

- **cooperative.yml lacks influence_headings** (`cooperative.yml`, L39-44): The arbitration section has only `required_headings`. No structured data for non-binding influence levels exists. Impact: high — this is P1 item 1.

- **P2 items lack implementation ordering**: The arbiter (Consideration 3) notes that the P2 tier contains 9 items of varying scope. Trivial fixes (item 8: doc paths, item 10: field documentation) should be distinguished from structural changes (items 4, 5, 7, 12: type system and markers). Impact: medium — implementation planning benefits from sub-ordering.

- **No explicit path formula for PRIOR_ARBITRATION_PATH in SKILL.md** (`SKILL.md`, L500): The variable is set to "prior round's arbitration path (empty for Round 1)" but the exact path formula (`{output}/round-{R-1}/arbitration/resolution.md`) is not stated. This is P2 item 11, still unaddressed.

## Off-Base Assumptions

- No off-base assumptions about the integration domain. The spec correctly maps all 23 FRs to implementation artifacts. The gaps are template wiring omissions, not architectural misunderstandings.

## Actionable Recommendations

1. **Wire {ARBITRATION_PATHS} into cross-round synthesis template** (Priority: P1)
   - **Current state**: `cross-round-synthesis.md` "What to Read" section lists target files and round syntheses but not arbitration files (L14-24).
   - **Proposed change**: Add a conditional reading instruction after the round syntheses section:
     ```markdown
     3. **Per-round arbitration resolutions** (if inter-round arbitration was configured):
     {ARBITRATION_PATHS}

     These contain the arbiter's positions from each round. Read them to attribute dispute resolutions accurately in the Resolution Attribution section.
     ```
   - **Rationale**: Principle VIII — the structured data exists; the template must consume it rather than forcing the synthesizer to infer. All three agents and the arbiter (AO-1) agree.
   - **Risk if ignored**: Cross-round synthesizer produces Resolution Attribution by inferring from round syntheses instead of reading actual arbitration files.

2. **Wire {ARBITRATION_RULINGS} into cross-round synthesis template** (Priority: P1)
   - **Current state**: Resolution Attribution section (cross-round-synthesis.md L91-100) instructs tracking but does not provide arbiter ruling content.
   - **Proposed change**: Add after the Resolution Attribution instructions:
     ```markdown
     **Pre-formatted arbiter rulings across rounds:**

     {ARBITRATION_RULINGS}

     Use this content to attribute dispute resolutions. When the arbiter addressed a dispute, cite the specific round and ruling rather than summarizing from the round synthesis.
     ```
   - **Rationale**: Same as item 1 — the variable is provisioned; the template must consume it.
   - **Risk if ignored**: Duplicate inference; the synthesizer reads round syntheses to reconstruct what the arbiter said instead of reading the actual rulings.

3. **Add influence_headings to cooperative.yml and ArbitrationConfig** (Priority: P1)
   - **Current state**: cooperative.yml has four binding headings. ArbitrationConfig has `required_headings: list[str]`.
   - **Proposed change**: Add `influence_headings` to cooperative.yml (keyed by influence level string, with heading lists for `recommended` and `advisory`). Add `influence_headings: dict[str, list[str]] = Field(default_factory=dict)` to ArbitrationConfig in models.py. The linter's heading validation should use `influence_headings[level]` when the level is non-binding, falling back to `required_headings` for `binding`.
   - **Rationale**: All three agents converge. The arbiter confirms (AO-1) this is a direct application of Principle VIII.
   - **Risk if ignored**: Heading validation produces false positive warnings for advisory/recommended arbitration runs.

4. **Establish P2 implementation sub-ordering** (Priority: P2-meta)
   - **Current state**: 9 P2 items with no internal ordering.
   - **Proposed change**: Group P2 items into two tiers:
     - **P2-easy** (documentation and path fixes, minimal risk): items 8 (doc paths), 10 (field documentation), 9 (config_conditions documentation), 11 (path formula), 6 (boundary documentation).
     - **P2-structural** (type system and marker changes, require testing): items 4 (Phase enum in validate.py), 5 (VariableDefinition.phases typing), 7 (provisional markers), 12 (match/case).
   - **Rationale**: Arbiter Consideration 3 — P2 items range from trivial path fixes to structural type system changes. Sub-ordering enables incremental implementation.
   - **Risk if ignored**: Implementation treats all P2 items as equal effort, potentially blocking easy wins behind complex changes.

5. **Specify PRIOR_ARBITRATION_PATH formula explicitly** (Priority: P2)
   - **Current state**: SKILL.md L500 says "prior round's arbitration path (empty for Round 1)" without the exact formula.
   - **Proposed change**: Add: "Set `{PRIOR_ARBITRATION_PATH}` to `{output}/round-{R-1}/arbitration/resolution.md` when `arbiter.timing: inter-round` and arbitration fired in Round R-1. If arbitration did not fire in Round R-1 (trigger not met), set to empty string."
   - **Rationale**: Principle VII (reproducibility) — the path must be deterministic from config. This is P2 item 11 from Round 1.
   - **Risk if ignored**: Implementers must infer the path formula from context; different implementations may compute different paths.

6. **Address provisional-resolution marker lifecycle** (Priority: P2)
   - **Current state**: P2 item 7 proposes markers. The arbiter (AO-5) asks about the re-opening lifecycle.
   - **Proposed change**: Specify: PROVISIONALLY_RESOLVED markers are round-scoped. Each round's synthesizer categorizes disputes based on current state. Re-opened disputes (FR-012) move back to DISPUTES_BEGIN/DISPUTES_END in the round where they are re-opened. The provisional section exists only for disputes that remain provisionally resolved (recommended rulings not challenged with counter-evidence). The arbiter also asks whether the markers should be stable from first use or marked unstable — per Principle II, new interfaces should be marked stable only after one spec has consumed them. Recommend marking as unstable until spec 006 implementation is validated.
   - **Rationale**: Principle II — stable contracts must have clear lifecycle semantics before they are declared stable.
   - **Risk if ignored**: Ambiguous marker semantics; different implementations may handle re-opened disputes differently.

7. **Verify template last-mile coverage** (Priority: P2)
   - **Current state**: The linter checks that required variables are present in templates and that template variables are known. It does not check that provisioned variables are consumed.
   - **Proposed change**: Document the manual audit practice: after adding a variable to variables.yml, verify at least one template in the corresponding phase references it. Long-term, add a linter `--audit` mode that reports unreferenced provisioned variables.
   - **Rationale**: Arbiter Consideration 1 — all three agents missed the dead template variables. A standing audit practice prevents recurrence.
   - **Risk if ignored**: Dead infrastructure accumulates silently as variables are provisioned for future specs.

## Referenced Documentation

- `spec.md` — FR-013 (L143), FR-014 (L144-151), FR-017 (L160), FR-020 (L163), FR-023 (L172-180)
- `SKILL.md` — L488-509 (inter-round arbitration), L500 (PRIOR_ARBITRATION_PATH), L559-573 (cross-round synthesis variables), L626 (REMAINING_DISPUTES extraction)
- `models.py` — L191-194 (ArbitrationConfig), L362-374 (CrossRoundSynthesisContext)
- `cooperative.yml` — L39-44 (arbitration section)
- `cross-round-synthesis.md` — L14-24 (What to Read), L91-100 (Resolution Attribution)
- `variables.yml` — L136-168 (arbitration-related variables)
- Round 1 synthesis — P1 items 1-3, P2 items 6-11
- Arbitration resolution — AO-1, AO-2, AO-5, Considerations 1, 3
