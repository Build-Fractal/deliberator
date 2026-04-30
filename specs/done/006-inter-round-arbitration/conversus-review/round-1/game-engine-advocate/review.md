# Game Engine Advocate Review — Spec 006: Inter-Round Arbitration

**Reviewer**: game-engine-advocate
**Reviewing**: spec 006 implementation against game engine vision (archived spec 007)
**Date**: 2026-03-21

---

## Executive Summary

Spec 006 is a well-structured extension that introduces inter-round arbitration timing and influence control. From the game engine perspective, the implementation lands correctly on three of four evaluation axes: the `InfluenceLevel` StrEnum is properly extensible via factory pattern (documented in both `models.py` and the constitution), the influence model's three-tier authority system maps cleanly onto game-theoretic mechanism design roles (dictator/mediator/observer), and schema variables are correctly provisioned with forward-looking `config_conditions` that avoid premature coupling. The fourth axis -- inter-round execution hooks for game engine plugins -- is where spec 006 creates structural opportunity but does not explicitly accommodate it, which is the correct posture given the game engine vision's archived status.

The spec makes no decisions that would block the game engine vision. It makes several decisions that actively enable it. It misses a few low-cost opportunities to make the eventual integration smoother.

---

## Alignment

### 1. StrEnum Extensibility -- Can Plugins Extend InfluenceLevel via Factory?

**Assessment: Aligned.**

The `InfluenceLevel` StrEnum in `models.py` (L24-33) is correctly implemented as a closed behavioral enum with three members (`BINDING`, `RECOMMENDED`, `ADVISORY`). The constitution (Principle IX) explicitly mandates the extension pattern:

> "Plugins extend closed enums via factory functions that produce new StrEnum subclasses with additional members."

The docstring on `InfluenceLevel` (L26-29) explicitly states: "Plugins may extend via factory function that produces a new StrEnum with additional members." This is the correct forward reference. A plugin could define:

```python
def extended_influence_level(*extra_members):
    """Factory producing an InfluenceLevel subclass with additional members."""
    members = {m.name: m.value for m in InfluenceLevel}
    members.update(extra_members)
    return StrEnum("ExtendedInfluenceLevel", members)
```

The `ArbitrationContext` model (L347-361) uses `InfluenceLevel` as the type for `INFLUENCE_LEVEL` with a default of `InfluenceLevel.BINDING`. A plugin that extends `InfluenceLevel` via factory would need to also provide a corresponding context model variant or use Pydantic's discriminated union pattern. This is a spec-007 design concern, not a spec-006 gap.

The `ErrorType` StrEnum (L96-106) follows the same pattern with an identical docstring about factory extension. Consistency is good.

### 2. Influence Model Supports Plugin-Defined Influence Levels

**Assessment: Partially aligned -- structurally sound, but dispatch is template-driven not data-driven.**

The three-tier influence model (`binding`/`recommended`/`advisory`) maps directly onto game-theoretic mechanism design:

| Influence Level | Game Theory Role | Spec 006 Behavior | Game Engine Extension Point |
|-----------------|------------------|--------------------|-----------------------------|
| `binding` | Dictator | Disputes removed, no re-litigation | Nash equilibrium forced by authority |
| `recommended` | Mediator | Provisionally removed, re-openable with evidence | Correlated equilibrium suggestion |
| `advisory` | Observer | No effect on dispute count | Information signal, no payoff change |

This taxonomy is complete for the current system and extensible for the game engine. A plugin-defined influence level (e.g., `weighted` -- arbiter position carries proportional weight in payoff calculation) would require:

1. A new `InfluenceLevel` member via factory (supported by architecture)
2. A new dispute-counting rule in the termination check (SKILL.md L503-508)
3. A new template language block in `{PRIOR_ARBITRATION_SECTION}` (SKILL.md L399-402)
4. New heading variants in mode schema `arbitration.required_headings` (cooperative.yml L39-44)

Items 2-4 are all text-based dispatches in SKILL.md and YAML -- not code branches. This means a plugin adding a new influence level would need to modify SKILL.md text, which is problematic. The dispatch is embedded in the orchestration spec rather than externalized into a data structure plugins could extend. This is the correct design for now (YAGNI -- the game engine is archived), but it creates a migration cost when the game engine ships.

### 3. Inter-Round Execution Accommodates Game Engine Hooks

**Assessment: Structurally compatible, no explicit hook points.**

The inter-round execution model (SKILL.md L315-335) inserts Phase 6 between rounds:

```
Phase 1-5 -> Phase 6 (conditional) -> termination check -> next round
```

The game engine spec (archived) defines four lifecycle hooks:

| Game Engine Hook | Spec 006 Execution Point | Compatibility |
|-----------------|--------------------------|---------------|
| `PRE_EXECUTION` | Before Phase 1 of Round 1 | No conflict -- spec 006 does not touch pre-execution |
| `POST_PHASE_5` | After Phase 5, before Phase 6 | **Insertion point exists.** Spec 006 places Phase 6 here. A plugin hook would need to fire between Phase 5 and Phase 6 |
| `POST_DELIBERATION` | After all rounds complete | No conflict -- spec 006's cross-round synthesis is a natural predecessor |
| `POST_ARBITRATION` | After Phase 6 | **Insertion point exists.** Spec 006 runs termination check after Phase 6. Plugin hook fires between Phase 6 and termination check |

The critical compatibility point: the `POST_PHASE_5` hook and inter-round arbitration both want to execute after Phase 5. In the game engine vision, the convergence predictor fires at `POST_PHASE_5` to recommend whether to continue. In spec 006, the arbiter fires after Phase 5. The question is ordering:

- If `POST_PHASE_5` plugin fires first, it could recommend "stop, this will converge" -- but the arbiter hasn't yet intervened to clear deadlocks.
- If Phase 6 fires first, the plugin's prediction is based on post-arbitration state, which is more accurate.

Spec 006's ordering (Phase 5 -> Phase 6 -> termination check) is the correct sequence for game engine integration. The convergence predictor should see the post-arbitration state, not the pre-arbitration state. This means the game engine's `POST_PHASE_5` hook should be renamed or split into `POST_SYNTHESIS` (before arbitration) and `POST_ARBITRATION` (after). Spec 006's inter-round arbitration makes this distinction necessary and provides the structural foundation for it.

### 4. Schema Variables Correctly Provisioned

**Assessment: Aligned.**

The schema variables in `variables.yml` are correctly provisioned:

- `PRIOR_ARBITRATION_PATH` (L136-146): Correctly uses `config_conditions: arbiter.timing = inter-round`. The `ConfigCondition` model (models.py L122-132) supports the `field` + `operator` + `value` pattern needed for game engine conditions (e.g., `plugins.convergence-predictor.enabled = true`).

- `PRIOR_ARBITRATION_SECTION` (L169-182): Correctly scoped to `phases: [review]` with `required: true` and `config_conditions: arbiter.timing == inter-round`. The `operator` field using `"=="` is more explicit than the bare `value` pattern used by `PRIOR_ARBITRATION_PATH` -- this inconsistency is cosmetic but worth normalizing.

- `INFLUENCE_LEVEL` (L183-189): Correctly scoped to `phases: [arbitration]` with `required: true`. No `config_conditions` -- it is always required when arbitration runs, regardless of timing. This is correct because influence applies to both `timing: final` and `timing: inter-round`.

- `ARBITRATION_PATHS` and `ARBITRATION_RULINGS` (L147-167): Correctly provisioned for cross-round synthesis with `config_conditions: arbiter.timing = inter-round`.

The `variables.yml` header comment (L9-10) explicitly states: "Plugin-contributed variables are namespaced separately (mechanism defined by spec 007). Do not add plugin-specific variables to this file." This is the correct boundary -- plugin variables will live in a separate namespace, and the core schema remains clean.

---

## Missed Opportunities

### MO-1: Influence Level as Dispatch Table Rather Than Template Text

**Impact: Medium. Cost to address now: Low.**

The influence-aware behavior is dispatched through three mechanisms:
1. Template text in SKILL.md (L399-402) -- hardcoded `if/else` blocks for each influence value
2. Mode schema headings in `cooperative.yml` (L39-44) -- only `binding` headings listed
3. Dispute counting rules in SKILL.md (L503-508) -- text description of per-influence behavior

When the game engine ships and plugins need to add influence levels, all three dispatch points must be found and modified. If the dispatch were externalized into a data structure (e.g., a `schema/influence-levels.yml` mapping each level to its heading replacements, dispute counting rule, and template language), plugins could extend by adding entries rather than editing SKILL.md text.

This is not a spec-006 deficiency -- spec 006 correctly handles the three defined levels. But a small structural change now would reduce migration cost later.

**Recommendation**: Consider adding an `influence_dispatch` section to the mode schema or a dedicated `schema/influence-levels.yml` that maps each influence value to its behavioral parameters. Low priority -- only valuable if the game engine timeline is near.

### MO-2: `cooperative.yml` Arbitration Headings Are Binding-Only

**Impact: Low. Correctness concern.**

The cooperative mode schema (`cooperative.yml` L39-44) lists `required_headings` as:
```yaml
required_headings:
  - Process Note
  - Decision Framework
  - Binding Decisions
  - Summary of Changes Required
```

Per FR-023, when `influence` is `recommended` or `advisory`, the headings change:
- `recommended`: "Binding Decisions" -> "Recommended Resolutions", "Summary of Changes Required" -> "Suggested Changes"
- `advisory`: "Binding Decisions" -> "Advisory Opinions", "Summary of Changes Required" -> "Considerations for Next Round"

The linter's `check_required_headings()` in `validate.py` (L248-256) checks headings against `mode_schema.arbitration.required_headings` without awareness of the influence level. This means the linter will flag `recommended` and `advisory` arbitration templates as having missing headings if they use the influence-adjusted headings.

The spec acknowledges this at FR-023: "The Phase 6 output validation (heading checks) MUST use the influence-adjusted headings, not the default binding headings." But the current `cooperative.yml` schema and linter implementation do not reflect this requirement.

**Recommendation**: Either (a) the mode schema should list all three heading variants with their influence-level conditions, or (b) the linter should skip heading validation for arbitration templates that contain `{INFLUENCE_LEVEL}` (since the heading is dynamic). Option (b) is simpler and aligns with spec 006's template-variable approach.

### MO-3: No `POST_ARBITRATION` State Exposure for Plugins

**Impact: Low (game engine is archived). Strategic.**

The inter-round execution model creates a natural `POST_ARBITRATION` checkpoint where the game engine's convergence predictor and equilibrium scorer would want to run. The current termination check (SKILL.md L511-549) immediately follows Phase 6 with no extensibility point.

A one-line comment in SKILL.md at L510 like "Plugin hook point: POST_ARBITRATION (spec 007)" would cost nothing and signal the integration point to future implementers. The game engine spec's `POST_PHASE_5` hook (archived spec Section 3) would need to be split into `POST_SYNTHESIS` and `POST_ARBITRATION` because spec 006 created a meaningful distinction between those two states.

**Recommendation**: Add a comment in SKILL.md at the appropriate execution points noting the plugin hook opportunity. Zero behavioral change, pure documentation signal.

### MO-4: ConfigCondition Operator Inconsistency

**Impact: Cosmetic. Easy fix.**

In `variables.yml`, the config conditions use two different patterns:
- `PRIOR_ARBITRATION_PATH` (L144-145): `field: arbiter.timing`, `value: "inter-round"` (no explicit operator)
- `PRIOR_ARBITRATION_SECTION` (L179-181): `field: arbiter.timing`, `operator: "=="`, `value: "inter-round"`

The `ConfigCondition` model (models.py L122-132) defaults `operator` to `"=="`, so both are functionally identical. But the inconsistency is a minor maintenance hazard -- a future reader might wonder if omitting `operator` means something different.

**Recommendation**: Normalize all config conditions to include the explicit `operator: "=="`. This is a single-pass edit to `variables.yml`.

---

## Off-Base Assumptions

### OBA-1: The Game Engine Needs Influence Levels Beyond Three

**Confidence: Medium.**

The review prompt asks me to verify that "the influence model supports plugin-defined influence levels." Strictly, the factory pattern supports adding new StrEnum members. But the practical question is: does the game engine actually need more than three?

Reviewing the archived game engine spec:
- The equilibrium scorer produces a numerical quality score (0.0-1.0) -- it does not need a new influence level
- The convergence predictor recommends "continue" or "stop" -- it operates outside the influence model entirely
- The config optimizer recommends parameter changes -- also outside influence

The influence model governs how the ARBITER's positions affect AGENTS. Game engine plugins are not arbiters -- they are analytical observers that produce advisory output to the USER (or an autonomous orchestrator). The plugin output is written to `plugins/` (game engine spec Section 3), not injected into agent context.

The assumption that plugins need to extend `InfluenceLevel` may be premature. The more likely integration point is a new hook type (e.g., `PluginRecommendation`) that is structurally separate from the arbiter influence model. The factory extensibility of `InfluenceLevel` is still valuable (a custom arbiter personality might want a `weighted` influence level), but the game engine specifically is unlikely to need it.

### OBA-2: The docs Path Issue

The `conversus.yml` for this review (L45-46) references:
```yaml
docs:
  - specs/007-game-engine/spec.md
  - specs/007-game-engine/ideation-context.md
```

These paths do not exist. The game engine spec was archived to `specs/archive/game-engine-vision/`. This review was conducted using the archived files at their actual locations. The broken doc paths would cause a validation failure in the orchestrator (`arbiter.docs` path validation, SKILL.md L186), which means this review agent would not have launched in an actual conversus run. This is a config error in the review setup, not a spec-006 issue.

---

## Actionable Recommendations

### R1: Normalize ConfigCondition Operators in variables.yml

**Priority**: P3 (cosmetic consistency)
**Effort**: Trivial
**Files**: `schema/variables.yml`

Add `operator: "=="` to all `config_conditions` entries that currently omit it. Specifically, lines 95-96, 109-110, 122-123, 132-133, 144-145, 155-156, 165-166 should all include the explicit operator to match the pattern established by `PRIOR_ARBITRATION_SECTION` at L179-181.

### R2: Address Influence-Aware Heading Validation (FR-023)

**Priority**: P1 (correctness -- FR-023 is not yet implemented in the linter)
**Effort**: Small
**Files**: `schema/modes/cooperative.yml`, `linter/validate.py`

The linter currently validates arbitration headings against a static list that assumes `binding` influence. Two options:

- **Option A**: Add all three heading variants to the mode schema with influence-level conditions. This requires extending `ArbitrationConfig` in `models.py` to support per-influence heading sets.
- **Option B**: Skip heading validation for arbitration templates that reference `{INFLUENCE_LEVEL}`, since the actual headings are dynamic. Add a note in the mode schema that headings are influence-dependent.

Option B is simpler and more aligned with the existing template-variable approach. The arbitration template already instructs the agent to use influence-adjusted headings (L70-73 of `templates/cooperative/arbitration.md`).

### R3: Add Plugin Hook Comments to SKILL.md Execution Model

**Priority**: P3 (documentation signal, zero behavioral change)
**Effort**: Trivial
**Files**: `SKILL.md`

Add comments at the three game-engine-relevant execution points:

1. Before Phase 1 (PRE_EXECUTION hook point)
2. Between Phase 5 and Phase 6 (POST_SYNTHESIS hook point)
3. Between Phase 6 and termination check (POST_ARBITRATION hook point)

These are comments only -- no code changes, no behavioral changes. They signal to future game engine implementers where the integration points are.

### R4: Update conversus.yml Doc Paths

**Priority**: P2 (config correctness)
**Effort**: Trivial
**Files**: `specs/006-inter-round-arbitration/conversus.yml`

Update the game-engine-advocate docs paths from the non-existent `specs/007-game-engine/` to the actual archive location `specs/archive/game-engine-vision/`:

```yaml
docs:
  - specs/archive/game-engine-vision/spec.md
  - specs/archive/game-engine-vision/ideation-context.md
```

### R5: Consider Influence Dispatch Externalization (Future)

**Priority**: P3 (strategic, pre-game-engine preparation)
**Effort**: Medium
**Files**: New `schema/influence-levels.yml` or extension to mode schemas

Externalize the per-influence behavioral parameters (heading replacements, dispute counting rules, template language blocks) into a data structure rather than embedding them in SKILL.md prose. This makes influence levels data-driven rather than text-driven, which is the prerequisite for plugin-contributed influence levels.

Not blocking for spec 006. Relevant when the game engine vision moves from archived to active.

---

## Summary Assessment

Spec 006 is well-designed from the game engine perspective. The StrEnum extensibility is correctly documented and architecturally sound. The influence model maps cleanly onto game-theoretic mechanism design roles. The inter-round execution model creates natural plugin hook points even without explicitly naming them. Schema variables are correctly provisioned with forward-looking condition models.

The only P1 item is R2 (influence-aware heading validation), which is a gap between FR-023's requirement and the current linter implementation. Everything else is P2-P3 polish or strategic preparation for a future that may or may not arrive.

The spec makes no decisions that would require rework when the game engine ships. This is the most important finding.
