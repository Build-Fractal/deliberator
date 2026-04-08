# Schema Integration Audit: Engine vs Specs 011a/012/013

**Reviewer**: schema-integration-auditor
**Date**: 2026-03-24
**Scope**: Engine package (`engine/`), schema package (`conversus/schemas/`), SKILL.md structure, MCP server

---

## Executive Summary

The schemas package (specs 012-013) and the engine package are **cleanly isolated with zero import dependencies in either direction**. This confirms the expected finding: schemas are purely additive. However, this isolation is stronger than it needs to be -- there are no integration points, no shared type registries, and no mechanism for the engine to consume game form definitions or objective templates. The engine's `VALID_MODES` tuple and the schemas' `VALID_MODES` frozenset define the same four modes independently, creating a latent consistency risk. SKILL.md has no awareness of the schemas package. The 011a decomposition has been partially implemented (the `references/` directory exists but contains only agentskills documentation, not handler extractions).

**Verdict**: No conflicts. No regressions. But no integration either -- the schemas are an island. The bridge specs (014+) will need explicit wiring work.

---

## Alignment

### 1. Import Isolation: Confirmed Clean

- `engine/` imports: `engine.*`, `linter.*`, `pydantic`, `yaml`, stdlib. **Zero imports from `conversus.schemas`.**
- `conversus/schemas/` imports: `pydantic`, `yaml`, `pathlib`, stdlib. **Zero imports from `engine`.**
- `mcp_server.py` imports: `engine.*`, `linter.*`, `mcp`, `pydantic`, `yaml`. **Zero imports from `conversus.schemas`.**

This matches spec 012's constraint: "The core conversus engine does not depend on `conversus-schemas`. Schemas are consumed by downstream specs (013-020), not by the core." The isolation is by design and correctly implemented.

### 2. Mode Enum Duplication: Consistent but Independent

Two independent definitions of the valid mode set exist:

- **Engine** (`engine/config.py:82`): `VALID_MODES = ("cooperative", "winner-take-all", "prisoners-dilemma", "red-blue")` -- a tuple
- **Schemas** (`conversus/schemas/objectives.py:30-35`): `VALID_MODES: frozenset[str] = frozenset({"cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"})` -- a frozenset

The values are identical today. The types differ (tuple vs frozenset) but this is irrelevant since both are used only for membership testing. The risk is drift: if a new mode is added to one but not the other, validation will silently disagree about what modes are valid.

### 3. Game Form Awareness: Engine Has None

The engine's `EngineConfig` model has a `mode: str` field validated against `VALID_MODES`. There is no `game_form` field, no reference to normal-form/gnep/parametric/stackelberg concepts, and no mechanism to associate a mode with its game-theoretic form. The engine treats mode as a string that selects a template directory (`templates/{mode}/`). It does not know that `cooperative` maps to `gnep` or that `winner-take-all` maps to `normal-form`.

This is correct per spec 012: "Must NOT modify SKILL.md. The game form schemas are consumed by Python code (plugins, feature extraction), not by the template orchestrator." The engine is the template orchestrator; it does not need game form awareness yet.

### 4. Config Parser Extensibility

`engine/config.py:parse_config()` is extensible for game form definitions but would require explicit work:

- Adding a `game_form` field to `EngineConfig` (straightforward Pydantic addition)
- Importing `load_mode_mapping()` from `conversus.schemas.game_forms` to auto-resolve mode-to-form
- Adding an optional `objective` section to the config YAML schema

The config parser currently ignores unknown YAML keys silently (Pydantic's default `model_config` does not set `extra = "forbid"`), so adding new keys to `conversus.yml` would not break existing engine parsing. However, the engine would not consume them without code changes.

### 5. SKILL.md: No Schema References

SKILL.md mentions `schema/` only in the context of `schema/variables.yml` and `schema/modes/{mode}.yml` (the template linter's variable contract). There is no mention of:
- `schema/game-forms/`
- `schema/objective-functions/`
- `conversus.schemas` package
- Game form models or objective templates

This is correct per both spec 012 and 013: "Must NOT modify SKILL.md."

### 6. 011a Decomposition: Partially Implemented

Spec 011a specifies extracting SKILL.md handlers into `references/handler-*.md` files. Current state:

- `references/` directory exists but contains only agentskills-related documentation (`agents-md.md`, `agentskills-best-practices.md`, `agentskills-quickstart.md`, `agentskills-spec.md`, `agentskills-what.md`)
- No `handler-gate.md`, `handler-define.md`, `handler-interests.md`, `handler-mode.md`, `handler-converge.md`, or `handler-arbitrate.md` exist
- SKILL.md dispatch table does not reference any handler files (no load triggers)
- SKILL.md is still a monolithic file (the original 2216-line problem described in 011a)

The engine's `templates.py:find_templates_dir()` and `config.py:_find_conversus_root()` use directory-structure heuristics (`schema/` + `templates/` existence) to locate the project root. These heuristics are unaffected by whether SKILL.md is decomposed. The engine does not load or parse SKILL.md at all -- it is a human/agent-facing document, not a runtime artifact.

### 7. Test Isolation: Clean Separation

- Schema tests: `tests/test_game_forms.py`, `tests/test_objectives.py` -- import only from `conversus.schemas.*`
- Engine tests: `engine/tests/test_config.py` -- imports only from `engine.*`
- No shared conftest.py at the project root
- No shared fixtures between schema tests and engine tests
- Both test suites use `VALID_MODES` but from their respective packages

No test conflicts exist.

### 8. `timing` and `influence` Fields: SKILL.md Spec vs Engine Implementation

SKILL.md (post-spec-006) specifies `arbiter.timing` (`final`/`inter-round`) and `arbiter.influence` (`binding`/`recommended`/`advisory`) as config fields. The engine's `ArbiterConfig` model does **not** include these fields:

```python
class ArbiterConfig(BaseModel):
    name: str
    prompt: str
    docs: list[Path] = []
    grounding: Path
    trigger: Literal["disputes_remain", "always"]
    # No timing field
    # No influence field
```

The engine's `parse_config()` silently ignores `timing` and `influence` in the YAML because Pydantic's default behavior does not reject extra fields. This means:
- A config with `timing: inter-round` will parse successfully but the engine will always behave as `timing: final`
- A config with `influence: advisory` will parse successfully but the engine will always behave as `influence: binding`
- No validation error is raised for invalid `timing`/`influence` values

This is a spec-006 gap in the engine, not a schemas issue, but it is relevant to the alignment check.

---

## Missed Opportunities

### M1. No Shared Mode Registry

The same four modes are defined in three places: `engine/config.py` (tuple), `conversus/schemas/objectives.py` (frozenset), and `conversus/schemas/game_forms.py` (implicitly via mode-mapping.yml). A single canonical source (e.g., `conversus/modes.py` or `schema/modes.yml`) consumed by both packages would prevent drift.

### M2. No Config-Level Game Form Exposure

The engine's config could expose an optional `game_form` field that auto-populates from the mode-mapping table. This would allow templates to include `{GAME_FORM}` as a variable, giving agents game-theoretic context without requiring full solver integration. Zero-cost extension that prepares the ground for spec 014.

### M3. No MCP Tool for Schema Validation

The MCP server exposes `conversus_validate`, `conversus_run`, and `conversus_decide`. There is no tool for validating game form instances or objective function templates. Adding `conversus_validate_schema` would allow editors to validate YAML game definitions in real-time.

### M4. No Cross-Package Type Re-Export

`engine/__init__.py` exports `Deliberation`, `Result`, `validate`. The schemas package exports game form models. There is no unified top-level import path (e.g., `from conversus import NormalFormGame, Deliberation`) because there is no top-level `conversus/__init__.py` that bridges both packages. This is fine for now but will become a friction point when spec 014 needs both.

---

## Off-Base Assumptions

### O1. None Identified on Schema Isolation

The specs correctly predicted that schemas would be additive with no engine impact. The implementation matches exactly. The only implicit assumption worth calling out is:

Spec 013, FR-011 specifies the import path as `from conversus_schemas.objectives import ...`, but the actual implementation uses `from conversus.schemas.objectives import ...` (note: `conversus.schemas` not `conversus_schemas`). This is a spec-vs-implementation naming discrepancy. The implementation path (`conversus.schemas`) is actually better -- it makes the schemas a subpackage of conversus rather than a separate package, which is more natural for a monorepo.

### O2. Engine Does Not Need Game Forms for Current Modes

The alignment check question asked whether the engine's config parser could be extended to accept game form definitions. It can, but the current four modes work fine without it. Game forms become necessary only when modes need parametric configuration (spec 019 config optimizer) or when new modes are added that require explicit game structure. For the four existing modes, the template directory convention (`templates/{mode}/`) is sufficient.

---

## Actionable Recommendations

### P1: Critical

**R1. Add `timing` and `influence` fields to `ArbiterConfig`** (engine gap, not schema issue but surfaces during this audit). Without these fields, the engine silently ignores spec-006 config values. Users writing configs per SKILL.md will get unexpected behavior. Add the fields, default to `final`/`binding`, validate values, and implement inter-round arbitration dispatch in `phases.py`.

**R2. Create a canonical mode list consumed by both packages.** Define `VALID_MODES` once in a lightweight shared module (e.g., `conversus/modes.py` or as the mode-mapping.yml file that already exists at `schema/game-forms/mode-mapping.yml`). Both `engine/config.py` and `conversus/schemas/objectives.py` should import from this single source. This prevents silent drift when modes are added.

**R3. Validate or reject unknown arbiter config fields.** Set `model_config = {"frozen": True, "extra": "forbid"}` on `ArbiterConfig` (and ideally on the raw config dict parsing). Currently, `timing: inter-round` silently passes validation -- this is a correctness trap. Either implement the fields (R1) or reject them with a clear error: "arbiter.timing is not yet supported by the engine."

### P2: Important

**R4. Implement the 011a SKILL.md decomposition.** The `references/` directory exists but contains no handler extractions. SKILL.md remains monolithic. Phase 1 of 011a (extract gate + define handlers) should proceed to validate the reference-file loading pattern. The engine is unaffected (it does not parse SKILL.md), but agent context window costs are.

**R5. Add `game_form` as an optional, auto-resolved field on `EngineConfig`.** When present in config YAML, validate it against `VALID_GAME_FORMS`. When absent, auto-resolve from mode via `load_mode_mapping()`. This prepares the config surface for spec 014 without breaking existing configs. The field would be informational in the current engine (no behavioral change), but templates could reference `{GAME_FORM}` for agent context.

**R6. Fix spec 013 FR-011 import path.** Spec says `from conversus_schemas.objectives import ...` but implementation uses `from conversus.schemas.objectives import ...`. Update the spec to match the implementation. This is a documentation-only fix but prevents confusion when future specs reference the import path.

### P3: Nice to Have

**R7. Add a `conversus_validate_schema` MCP tool.** Accept a YAML string and a schema type (`game-form`, `objective-template`, `constraint`), validate it against the appropriate Pydantic model, and return structured errors. This enables editor-time validation of game definitions authored via specs 014+.

**R8. Create an integration test that imports from both packages.** A single test file that imports `from engine.config import VALID_MODES as engine_modes` and `from conversus.schemas.objectives import VALID_MODES as schema_modes` and asserts `set(engine_modes) == schema_modes` would catch drift immediately. This is a 10-line test that provides high-value regression protection.

**R9. Add `conversus/schemas` to the project's AGENTS.md structure section.** The root AGENTS.md (per 011a, 1.4) should document the `conversus/schemas/` directory as part of the project structure, with a note that it contains game form and objective function Pydantic models independent of the engine.

**R10. Document the zero-dependency contract in `conversus/schemas/__init__.py`.** Add a module-level docstring note: "This package MUST NOT import from engine/ or linter/. It is consumed by downstream specs (013-020) and must remain importable with only pydantic and pyyaml." This makes the architectural boundary explicit in code, not just in specs.

---

## Referenced Documentation

| Document | Location | Relevance |
|----------|----------|-----------|
| Spec 012: Game Form Schemas | `specs/done/012-game-form-schemas/spec.md` | Defines schema package structure, FR-008 (no solver imports), FR-010 (package structure) |
| Spec 013: Objective Function Templates | `specs/done/013-objective-function-templates/spec.md` | Defines objective models, FR-011 (import path -- discrepancy noted), FR-016 (package constraint) |
| Spec 011a: SKILL.md Decomposition | `specs/done/011a-skill-breakdown/spec.md` | Decomposition plan, binding arbiter rulings, handler extraction phases |
| Alignment Check | `specs/011-adoption-harness/pr-review/alignment-check.md` | Questions driving this audit |
| Engine config parser | `engine/config.py` | `VALID_MODES`, `ArbiterConfig`, `EngineConfig`, `parse_config()` |
| Engine phases | `engine/phases.py` | Pipeline orchestration, no schema awareness |
| Engine templates | `engine/templates.py` | Template loading/filling, mode-specific context builders |
| Engine SDK | `engine/sdk.py` | Public API surface, no schema references |
| MCP server | `mcp_server.py` | Tool surface area, no schema tools |
| Schema game forms | `conversus/schemas/game_forms.py` | `NormalFormGame`, `GNEPGame`, `ParametricGame`, `StackelbergGame`, `load_mode_mapping()` |
| Schema objectives | `conversus/schemas/objectives.py` | `ObjectiveTemplate`, `ConstraintTemplate`, `ParameterDefinition`, `VALID_MODES` |
| Schema init | `conversus/schemas/__init__.py` | Public API re-exports |
| SKILL.md | `SKILL.md` | Monolithic, no schema references, no handler extractions |
| Schema tests | `tests/test_game_forms.py`, `tests/test_objectives.py` | Isolated from engine tests |
| Engine tests | `engine/tests/test_config.py` | Isolated from schema tests |
