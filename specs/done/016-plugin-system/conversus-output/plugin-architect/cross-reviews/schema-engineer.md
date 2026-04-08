# Plugin Architect Cross-Review of Schema Engineer
# Spec: 016-plugin-system

**Cross-reviewer**: plugin-architect
**Reviewing**: schema-engineer's review at `conversus-output/schema-engineer/review.md`
**My review**: `conversus-output/plugin-architect/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: PluginFacingConfig model vs. existing `state.config` dict

Schema-engineer R-1 recommends replacing `DeliberationState.config: dict[str, Any]` with a typed `PluginFacingConfig` model. My review M-2 identifies the same config confusion but recommends removing or renaming the `config` parameter on `execute()` instead. The contradiction is in the fix direction: schema-engineer types the state config; I simplify the execute() signature.

**Resolution needed**: Both fixes address different aspects of the same problem. Schema-engineer's PluginFacingConfig types the deliberation config on the state. My fix removes the redundant `config` parameter from `execute()`. Both can be applied: type the state config AND remove the parameter, so plugins read `state.config.mode` (typed) and `self.plugin_config` (instance config). These are complementary, not contradictory.

### DC-2: load_plugins() signature — raw dicts vs. PluginConfigEntry

Schema-engineer M-7 recommends changing `load_plugins()` to accept `list[PluginConfigEntry]` instead of `list[dict[str, Any]]`. This is correct from a type-safety perspective. However, the current raw-dict signature allows `load_plugins()` to be called without the config parser (e.g., in tests or ad-hoc scripts). Changing the signature creates a hard dependency on the config parser.

**My position**: The typed signature is better. Tests can construct PluginConfigEntry objects directly (they are Pydantic models with defaults). Ad-hoc callers benefit from the validation. Adopt schema-engineer's recommendation.

---

## Tensions

### T-1: Plugin.name/hooks validation timing

Schema-engineer M-4 recommends adding validation for `name` and `hooks` in `Plugin.__init__`. My review does not address validation timing. The tension is minor: the ABC already requires subclasses to define these as class attributes (they are in the class body, not `__init__`). Adding `__init__` validation catches the edge case where a subclass declares `name` and `hooks` but sets them to empty/None. This is a reasonable defensive measure.

### T-2: AgentState.positions vs. AgentFeatures

Schema-engineer O-1 identifies `positions` as a dead field. My review M-5 identifies the same field overlap between AgentState and AgentFeatures. We agree the field is problematic. Schema-engineer recommends removal; I recommend alignment with AgentFeatures. The resolution depends on M-1 in my review (adding features to DeliberationState): if features are on the state, AgentState.positions can be removed because plugins access features instead.

---

## Safe Agreements

- **SA-1: Frozen models are correctly applied** -- Both reviews agree all state models are properly frozen.

- **SA-2: HookPoint dual str/enum design is correct** -- Both reviews agree this pattern serves both type checking and filename construction.

- **SA-3: PluginResult.advisory defaults to True** -- Both reviews confirm this satisfies the spec's advisory principle.

- **SA-4: No engine imports in plugins package** -- Both reviews confirm FR-014 compliance at import time.

- **SA-5: Version field would improve schema evolution** -- Schema-engineer M-6 proposes a version field. My review does not address this but agrees it would help plugin consumers handle breaking changes.
