# Integration Architect Review -- Spec 006 Inter-Round Arbitration

## Executive Summary

Spec 006 introduces two orthogonal arbiter capabilities -- inter-round timing and influence control -- that transform the arbiter from a terminal dictator into a configurable authority that can intervene between rounds with varying levels of weight. The implementation across SKILL.md, schema/variables.yml, linter/models.py, and the cooperative templates is comprehensive and structurally sound. All 23 functional requirements have corresponding implementation artifacts, the StrEnum conversion for `InfluenceLevel` and `ArbiterTiming` is complete and backward-compatible, and the template variable pipeline is fully wired from schema definition through Pydantic context models to template usage.

The implementation correctly preserves backward compatibility: omitting `timing` defaults to `final`, omitting `influence` defaults to `binding`, and both omitted together produce behavior identical to specs 001 + 004. The multi-round output structure, influence-aware dispute counting, and cross-round synthesis attribution are all documented in SKILL.md with sufficient precision for deterministic orchestration.

My most important finding: the cooperative mode schema (`schema/modes/cooperative.yml`) hardcodes only the `binding` headings in `required_headings` and does not account for influence-adjusted heading validation, creating a gap between the linter's static validation and the runtime heading validation described in SKILL.md.

## Alignment

- **FR-001/FR-002: Schema config fields** (SKILL.md L78-79, spec L115-116): The `timing` and `influence` fields are declared in the config YAML structure with correct value sets (`final | inter-round` and `binding | recommended | advisory`). SKILL.md L78-79 shows both in the config example block. Aligns with the spec's schema extension requirements.

- **FR-003: Inter-round + rounds:1 rejection** (SKILL.md L188): The validation rule "arbiter.timing: inter-round requires rounds > 1. With a single round, use timing: final (or omit timing)" is present verbatim. Error message matches spec FR-003 exactly.

- **FR-004: Default values** (SKILL.md L189-191): Explicit default documentation -- `timing` defaults to `final` (L189), `influence` defaults to `binding` (L191). Both use the same "If absent, default to X" pattern.

- **FR-013/FR-014: Prior arbitration context injection** (SKILL.md L399-402): The `{PRIOR_ARBITRATION_SECTION}` variable expansion includes all three influence-aware language variants matching FR-014's table verbatim: binding ("You MUST treat these as settled"), recommended ("You should adopt these unless you have grounded counter-evidence"), advisory ("You are not bound by these opinions").

- **FR-016/FR-017/FR-018/FR-019: Template variables** (schema/variables.yml L136-190): All four variables are defined -- `PRIOR_ARBITRATION_PATH` (L136-145), `ARBITRATION_PATHS` (L147-156), `ARBITRATION_RULINGS` (L158-167), `PRIOR_ARBITRATION_SECTION` (L169-181), and `INFLUENCE_LEVEL` (L183-190). Each has correct `phases`, `type`, `required`, and `config_conditions` metadata.

- **StrEnum implementation** (linter/models.py L24-43): `InfluenceLevel` and `ArbiterTiming` are properly defined as `StrEnum` subclasses with correct values. Constitution Principle IX compliance: closed behavioral choices use StrEnum, values are YAML-serialization-friendly strings. `ArbitrationContext` uses `InfluenceLevel` type with default `InfluenceLevel.BINDING` (L360).

## Missed Opportunities

- **Mode schema does not encode influence-adjusted headings** (schema/modes/cooperative.yml L40-44): The `required_headings` list is static: `["Process Note", "Decision Framework", "Binding Decisions", "Summary of Changes Required"]`. SKILL.md L651-655 documents the influence-adjusted headings at the orchestrator level, but the mode schema -- which the linter uses for heading validation -- has no mechanism to express conditional headings. This means the linter will incorrectly flag `recommended` or `advisory` arbitration templates that use "Recommended Resolutions" or "Advisory Opinions" instead of "Binding Decisions". Impact: high. [spec.md L173-180, schema/modes/cooperative.yml L40-44]

- **Linter does not validate influence-adjusted headings** (linter/validate.py L248-256): The `check_required_headings` function checks arbitration headings against `mode_schema.arbitration.required_headings` without any awareness of the influence level. Since the linter validates templates statically (before runtime), and the arbitration template uses `{INFLUENCE_LEVEL}` to conditionally emit different headings, the linter cannot statically validate these. However, the gap should be documented. The linter will pass the template because the template contains the static text "Binding Decisions" as fallback/instruction text -- but it would also pass a template that removed that text. Impact: medium. [linter/validate.py L248-256, spec.md L180]

- **No `INFLUENCE_LEVEL` in the `PRIOR_ARBITRATION_SECTION` expansion** (SKILL.md L399-402): The `{PRIOR_ARBITRATION_SECTION}` expansion includes the influence-aware language and the `{PRIOR_ARBITRATION_PATH}`, but does not include the influence level as a labeled field. Agents receiving the prior arbitration context can infer the influence level from the language ("MUST treat" vs. "should adopt" vs. "not bound"), but an explicit label like "Influence: binding" would make it unambiguous. The spec does not require this, so it is not a gap against the spec, but it is a missed opportunity for clarity. Impact: low.

- **Cross-round synthesis template does not reference `{ARBITRATION_PATHS}` or `{ARBITRATION_RULINGS}` in its "What to Read" section** (templates/cooperative/cross-round-synthesis.md L14-24): The template's "What to Read" section lists target files and round syntheses, but does not instruct the agent to read arbitration resolution files when they exist. The `{ARBITRATION_PATHS}` and `{ARBITRATION_RULINGS}` variables are defined in the schema and wired in the context model (`CrossRoundSynthesisContext.ARBITRATION_PATHS`, `CrossRoundSynthesisContext.ARBITRATION_RULINGS`), but the template does not use them in its reading instructions. The Resolution Attribution section references arbiter rulings conceptually but does not provide the file paths. Impact: medium. [schema/variables.yml L147-167, templates/cooperative/cross-round-synthesis.md L14-24]

- **Synthesis template FR-015 categorization is informal** (templates/cooperative/synthesis.md L103-112): FR-015 requires the synthesis template for Round R > 1 to handle arbiter-addressed disputes differently based on influence level (`binding` -> exclude from Remaining Disputes; `recommended` -> list as Provisionally Resolved; `advisory` -> keep in Remaining Disputes with note). The template includes an "Arbiter-Resolved Disputes (Prior Rounds)" section with influence-aware status labels, which partially satisfies FR-015. However, the categorization is an instruction to the synthesizer agent rather than a structural enforcement. The synthesizer could mis-categorize disputes. This is inherent to prompt-driven orchestration (Constitution Principle VIII acknowledges agent reasoning is sometimes necessary), but the lack of structural markers for provisionally-resolved disputes means the dispute-parsing subsystem cannot distinguish them from remaining disputes. Impact: medium. [spec.md L152-155, templates/cooperative/synthesis.md L103-112]

- **No structural markers for "Provisionally Resolved" disputes** (spec FR-012 + FR-009): The dispute-parsing subsystem uses `DISPUTES_BEGIN`/`DISPUTES_END` markers to count remaining disputes. For `recommended` influence, disputes should be "provisionally resolved" and excluded from the count. But the synthesis template has no separate marker block for provisionally-resolved disputes. The orchestrator relies on the agent to correctly categorize disputes, and the dispute-parsing subsystem's count may include provisionally-resolved disputes in the remaining count depending on where the synthesizer places them. Impact: medium. [spec.md L130-139]

## Off-Base Assumptions

- **The spec assumes static heading validation can be influence-aware** (spec.md L180): FR-023 states "The Phase 6 output validation (heading checks) MUST use the influence-adjusted headings, not the default binding headings." SKILL.md correctly implements this at the runtime level (L651-655), but the spec also implies the schema/mode YAML should reflect this. The mode schema (`cooperative.yml`) has a static `required_headings` list with no conditional mechanism. This is not wrong per se -- the runtime validation described in SKILL.md handles it correctly -- but the spec's phrasing could mislead someone into thinking the mode YAML needs modification. The implementation correctly chose to handle influence-adjusted heading validation at the orchestrator level rather than the schema level, which is the right architectural decision since the schema is mode-specific while influence is run-specific.

- **FR-018 scopes `PRIOR_ARBITRATION_SECTION` to Phase 1 only** (spec.md L161): The spec states "only Phase 1 templates receive this variable -- Phases 2-5 operate within a single round's artifacts and do not need prior-round arbitration context." The schema/variables.yml correctly limits `PRIOR_ARBITRATION_SECTION` to `phases: [review]` (L177). However, the Pydantic context models include `PRIOR_ARBITRATION_PATH` (not `PRIOR_ARBITRATION_SECTION`) on all five Phase 1-5 context models (ReviewContext, CrossReviewContext, RevisionContext, DisputesContext, SynthesisContext). This is correct: `PRIOR_ARBITRATION_PATH` is a raw path available to all phases for potential use, while `PRIOR_ARBITRATION_SECTION` is the pre-formatted conditional block only in Phase 1. The distinction is appropriate but could be confused by someone reading the spec's "only Phase 1" statement without understanding the `PATH` vs. `SECTION` distinction.

## Actionable Recommendations

1. **Add influence-aware heading alternatives to mode schema** (Priority: P1)
   - **Current state**: `schema/modes/cooperative.yml` L40-44 lists only binding headings: `["Process Note", "Decision Framework", "Binding Decisions", "Summary of Changes Required"]`.
   - **Proposed change**: Add `influence_headings` map to the `ArbitrationConfig` model and cooperative.yml:
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
   - **Rationale**: SKILL.md L651-655 documents influence-adjusted headings. The mode schema should be the single source of truth for heading requirements. Currently the mapping is duplicated between SKILL.md prose and the hardcoded cooperative.yml. A structured schema entry eliminates drift risk. [spec.md L173-180, Constitution Principle IV]
   - **Risk if ignored**: The linter validates against the static `required_headings`, which only matches `binding` headings. If a future linter enhancement adds runtime config awareness, it will need this data in the schema. More immediately, anyone reading the mode schema will incorrectly conclude that "Binding Decisions" is always required.

2. **Wire `{ARBITRATION_PATHS}` into cross-round synthesis "What to Read" section** (Priority: P1)
   - **Current state**: `templates/cooperative/cross-round-synthesis.md` L14-24 lists target files and round syntheses as reading material but does not reference arbitration resolution files.
   - **Proposed change**: Add a conditional reading section after round syntheses:
     ```
     3. **Arbitration resolutions** (if inter-round arbitration was active):
     {ARBITRATION_PATHS}
     ```
   - **Rationale**: The cross-round synthesizer produces Resolution Attribution (L90-100) which requires reading arbiter rulings. Without explicit paths, the agent must infer arbitration paths from round syntheses or the `{ARBITRATION_RULINGS}` pre-formatted content. Explicit paths align with Constitution Principle VIII (templating over inference). [schema/variables.yml L147-156, FR-017]
   - **Risk if ignored**: The cross-round synthesizer may produce inaccurate Resolution Attribution because it never read the actual arbitration files, relying solely on the pre-formatted `{ARBITRATION_RULINGS}` summary or inferences from round syntheses.

3. **Add `{ARBITRATION_RULINGS}` to cross-round synthesis template** (Priority: P1)
   - **Current state**: The `{ARBITRATION_RULINGS}` variable is defined in schema (variables.yml L158-167), wired in the context model (`CrossRoundSynthesisContext.ARBITRATION_RULINGS`), and documented in SKILL.md L570. But it does not appear in `templates/cooperative/cross-round-synthesis.md`.
   - **Proposed change**: Add `{ARBITRATION_RULINGS}` in the Resolution Attribution section instructions as pre-formatted arbiter ruling content the agent should reference.
   - **Rationale**: The variable is provisioned end-to-end (schema, model, SKILL.md) but the template -- the only consumer that would actually inject it into an agent prompt -- does not reference it. This makes it dead infrastructure. [schema/variables.yml L158-167, FR-020]
   - **Risk if ignored**: `ARBITRATION_RULINGS` is never consumed. The schema, model, and SKILL.md documentation for this variable become misleading: they suggest the cross-round synthesizer receives pre-formatted rulings, but it does not.

4. **Document the linter's static-vs-runtime heading validation gap** (Priority: P2)
   - **Current state**: The linter (`validate.py`) validates arbitration template headings statically. SKILL.md handles influence-adjusted headings at runtime. There is no documentation acknowledging this intentional gap.
   - **Proposed change**: Add a comment in `validate.py` `check_required_headings` function (around L248) noting that arbitration heading validation is influence-unaware by design and that runtime validation in SKILL.md handles the influence-adjusted case.
   - **Rationale**: Without this comment, a future maintainer may attempt to add influence awareness to the linter and hit the fundamental issue: the linter validates templates statically, and influence level is a runtime config value. The comment prevents wasted effort. [Constitution Principle IX -- code should be self-documenting, comments explain WHY]
   - **Risk if ignored**: A future contributor attempts to "fix" the linter by adding influence-aware heading checks, introducing unnecessary complexity or breaking static validation.

5. **Add `PRIOR_ARBITRATION_SECTION` to `ReviewContext` field documentation** (Priority: P2)
   - **Current state**: `linter/models.py` L262 declares `PRIOR_ARBITRATION_SECTION: str = ""` on `ReviewContext` with no docstring or comment distinguishing it from `PRIOR_ARBITRATION_PATH` on L267.
   - **Proposed change**: Add inline comment: `# Pre-formatted influence-aware block (FR-014). Distinct from PRIOR_ARBITRATION_PATH (raw file path).`
   - **Rationale**: The `SECTION` vs. `PATH` distinction is subtle and load-bearing. `SECTION` is a pre-formatted conditional block with influence-aware language (only on ReviewContext). `PATH` is a raw file path (on all Phase 1-5 contexts). A reader of models.py needs to understand this without reading the spec. [spec.md L161, Constitution Principle IX]
   - **Risk if ignored**: A maintainer confuses `PRIOR_ARBITRATION_SECTION` with `PRIOR_ARBITRATION_PATH` and either removes one as "duplicate" or adds `SECTION` to other context models unnecessarily.

6. **Verify `{PRIOR_ARBITRATION_PATH}` is set during inter-round arbitration dispatch** (Priority: P2)
   - **Current state**: SKILL.md L500 lists `{PRIOR_ARBITRATION_PATH}` as a variable for inter-round arbitration ("prior round's arbitration path (empty for Round 1)"). SKILL.md L399-402 documents it as part of `{PRIOR_ARBITRATION_SECTION}` expansion.
   - **Proposed change**: Ensure SKILL.md explicitly states when and how `{PRIOR_ARBITRATION_PATH}` is set for Phase 1 agents in Round R > 1. Currently the variable is mentioned in the `{PRIOR_ARBITRATION_SECTION}` expansion and in the inter-round arbitration variable list, but there is no explicit statement like "Set `{PRIOR_ARBITRATION_PATH}` to `{output}/round-{R-1}/arbitration/resolution.md` when arbitration fired in Round R-1."
   - **Rationale**: The path computation is inferrable but not explicit. Constitution Principle VII (reproducibility) requires deterministic path computation. An explicit formula prevents implementation ambiguity. [SKILL.md L495-500, Constitution Principle VII]
   - **Risk if ignored**: An implementer may set `PRIOR_ARBITRATION_PATH` to the wrong path or fail to clear it when arbitration did not fire in the prior round.

7. **Add `influence_headings` to `ArbitrationConfig` Pydantic model** (Priority: P2)
   - **Current state**: `linter/models.py` L191-194 defines `ArbitrationConfig` with only `required_headings: list[str]`.
   - **Proposed change**: Add `influence_headings: Optional[dict[str, list[str]]] = None` to `ArbitrationConfig`, keyed by influence level name.
   - **Rationale**: Complements recommendation #1. The Pydantic model should mirror the schema structure. Without this field, the model cannot load influence-aware heading data even if the YAML schema provides it. [linter/models.py L191-194, Constitution Principle IX]
   - **Risk if ignored**: If recommendation #1 adds `influence_headings` to the YAML, the Pydantic model will reject the extra field (strict validation) or silently ignore it.

8. **Add stagnation interaction documentation for influence levels** (Priority: P3)
   - **Current state**: SKILL.md L524-528 documents stagnation detection using dispute counts. SKILL.md L503-508 documents influence-aware dispute counting for termination. But the stagnation detection section does not explicitly reference the post-arbitration adjusted counts.
   - **Proposed change**: Add to SKILL.md L525 (stagnation detection): "When `arbiter.timing: inter-round`, use the post-arbitration adjusted dispute count (per the influence-aware dispute counting rules above) for stagnation comparison."
   - **Rationale**: FR-021 requires stagnation detection to use post-arbitration counts adjusted by influence level. The SKILL.md stagnation section references the dispute-parsing subsystem but does not explicitly connect to the influence-adjusted counts. The connection is inferrable from reading order but should be explicit. [spec.md L167, FR-021]
   - **Risk if ignored**: An implementer reads the stagnation section in isolation and uses raw dispute counts (pre-arbitration) for stagnation comparison, defeating the purpose of inter-round arbitration clearing disputes.

9. **Mark `ARBITRATION_RULINGS` as `required: true` when `arbiter.timing: inter-round`** (Priority: P3)
   - **Current state**: `schema/variables.yml` L158-167 defines `ARBITRATION_RULINGS` as `required: false`.
   - **Proposed change**: Change to `required: true` with a `config_conditions` gate on `arbiter.timing: inter-round`.
   - **Rationale**: If inter-round arbitration fires and produces rulings, the cross-round synthesis must receive them. Making the variable required when the condition is met ensures the template includes it (once recommendation #3 adds the reference). Currently the variable is optional, so the linter will not flag a template that omits it even when inter-round arbitration is configured. Note: this should align with `ARBITRATION_PATHS` which has the same condition but is also `required: false`. Both should be `required: true` under the condition. [schema/variables.yml L147-167]
   - **Risk if ignored**: A template author removes `{ARBITRATION_RULINGS}` from the cross-round synthesis template and the linter does not catch it, silently dropping arbitration context from the cross-round synthesizer's input.

## Referenced Documentation

- `specs/006-inter-round-arbitration/spec.md` -- sections/lines cited: L115-119 (FR-001 to FR-004), L122-126 (FR-005 to FR-008), L129-139 (FR-009 to FR-012), L143-155 (FR-013 to FR-015), L159-163 (FR-016 to FR-019), L163-164 (FR-020), L167-168 (FR-021), L169 (FR-022), L173-180 (FR-023), L217-219 (pre-provisioned schema)
- `SKILL.md` -- sections/lines cited: L78-79 (config example), L187-191 (validation rules), L234-248 (output structure), L315-337 (round loop diagram), L399-402 (PRIOR_ARBITRATION_SECTION expansion), L488-509 (inter-round arbitration), L524-528 (stagnation detection), L569-570 (ARBITRATION_PATHS/RULINGS), L643-655 (heading validation)
- `schema/variables.yml` -- sections/lines cited: L136-190 (all spec 006 variables)
- `schema/modes/cooperative.yml` -- sections/lines cited: L39-44 (arbitration required_headings)
- `linter/models.py` -- sections/lines cited: L24-43 (StrEnum definitions), L191-194 (ArbitrationConfig), L253-267 (ReviewContext), L347-360 (ArbitrationContext), L363-374 (CrossRoundSynthesisContext)
- `linter/validate.py` -- sections/lines cited: L248-256 (check_required_headings)
- `templates/cooperative/review.md` -- sections/lines cited: L23 (PRIOR_ARBITRATION_SECTION usage)
- `templates/cooperative/synthesis.md` -- sections/lines cited: L103-112 (Arbiter-Resolved Disputes section)
- `templates/cooperative/arbitration.md` -- sections/lines cited: L11 (INFLUENCE_LEVEL usage), L69-73 (influence-adjusted heading instructions)
- `templates/cooperative/cross-round-synthesis.md` -- sections/lines cited: L14-24 (What to Read section), L90-100 (Resolution Attribution section)
- `.specify/memory/constitution.md` -- sections/lines cited: Principle IV (Documentation Is the Product), Principle VII (Reproducibility), Principle VIII (Templating Over Inference), Principle IX (Functional Programming, StrEnum convention)
