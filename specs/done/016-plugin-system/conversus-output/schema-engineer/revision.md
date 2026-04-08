# Schema Engineer Revision: 016 Plugin System Infrastructure

**Reviewer**: schema-engineer
**Revision iteration**: 1
**Date**: 2026-03-24

---

## Recommendation Dispositions

#### Recommendation 1: Create PluginFacingConfig model

- **Original position**: Replace `config: dict[str, Any]` with typed PluginFacingConfig.
- **Disposition**: Modified
- **Explanation**: Spec-compliance T-1 proposes `extra="allow"` for forward-compatibility. Plugin-architect DC-1 proposes complementary fix (remove `config` param from execute()). Modified recommendation: create `PluginFacingConfig` with `mode: str`, `rounds: int = 1`, `iterations: int = 1`, `agent_names: list[str] = []`, and `model_config = {"extra": "allow", "frozen": True}`. Replace `DeliberationState.config: dict[str, Any]` with `DeliberationState.config: PluginFacingConfig`. The `extra="allow"` ensures unknown config fields are preserved for backward compatibility.

#### Recommendation 2: Add validation for Plugin.name and Plugin.hooks in __init__

- **Original position**: Catch missing class attributes at instantiation.
- **Disposition**: Surviving
- **Explanation**: Plugin-architect T-1 acknowledges this as a reasonable defensive measure. No cross-review challenges it.

#### Recommendation 3: Change load_plugins() to accept list[PluginConfigEntry]

- **Original position**: Type-connect config parsing and plugin loading.
- **Disposition**: Surviving
- **Explanation**: Plugin-architect DC-2 agrees the typed signature is better. Spec-compliance DC-2 agrees tests should use typed objects. No challenges.

#### Recommendation 4: Define minimal Position model or remove dead field

- **Original position**: Type the `positions` field or remove it.
- **Disposition**: Modified
- **Explanation**: Plugin-architect R-8 (revised) recommends removing `positions` from AgentState since features will be available on DeliberationState. Modified recommendation: remove `positions: list[dict[str, Any]]` from AgentState. The field is dead (never populated) and its intended content is superseded by the features pathway. Update the spec's Section 2 DeliberationState definition accordingly.

#### Recommendation 5: Add version field to Plugin class

- **Original position**: Enable schema evolution handling.
- **Disposition**: Surviving
- **Explanation**: Plugin-architect SA-5 agrees. No challenges. Add `version: str = "0.1.0"` as a class attribute with a default. The version is included in the output JSON for consumer awareness.

#### Recommendation 6: Remove or populate AgentState.positions

- **Original position**: Resolve the dead field.
- **Disposition**: Modified
- **Explanation**: Merged with R-4 above. Remove the field entirely.

#### Recommendation 7: Only create plugins/ dir when plugins produce output

- **Original position**: Avoid empty directory side effects.
- **Disposition**: Surviving
- **Explanation**: Plugin-architect T-1 (cross-review) argues `plugins/` is not core output, so FR-011 is MET regardless. Spec-compliance agrees the directory is outside core scope. However, the fix is trivial (move `mkdir` inside the success path) and eliminates even the theoretical FR-011 question. Maintaining at P3.

#### Recommendation 8: Add `__all__` to base.py

- **Original position**: Declare public API surface.
- **Disposition**: Surviving
- **Explanation**: Spec-compliance SA-5 agrees. No challenges.

---

## New Recommendations

- **Remove `config` parameter from Plugin.execute()** (Priority: P1)
  - Triggered by: Plugin-architect R-2 (revised) proposing `execute(self, state: DeliberationState)` with no config parameter.
  - Proposed change: Change the ABC's `execute()` signature to `execute(self, state: DeliberationState) -> PluginResult`. Plugins access deliberation config via `state.config` and plugin-specific config via `self.plugin_config`. Update `execute_hooks()` to call `plugin.execute(state)` instead of `plugin.execute(state, plugin.plugin_config)`.
  - Rationale: Eliminates the confusing double-config pattern where plugins receive both `state.config` and a `config` parameter. The simplified signature is cleaner for plugin authors.

---

## Position Summary

Withdrew 0, modified 3, maintained 4. Added 1 new recommendation.

The most significant change is R-4/R-6 (remove positions field). The cross-review consensus is that the field is dead and superseded by the features pathway. Removing it simplifies AgentState and eliminates a false API surface.

My highest-priority recommendation is the new NR-1 (remove config parameter from execute()). Combined with R-1 (PluginFacingConfig), this creates a clean two-channel config model: `state.config` for deliberation config (typed) and `self.plugin_config` for plugin-specific config (dict). The current three-channel model (state.config, config param, self.plugin_config) is confusing and redundant.
