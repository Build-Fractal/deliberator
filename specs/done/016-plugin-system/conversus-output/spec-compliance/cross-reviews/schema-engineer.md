# Spec Compliance Cross-Review of Schema Engineer
# Spec: 016-plugin-system

**Cross-reviewer**: spec-compliance
**Reviewing**: schema-engineer's review at `conversus-output/schema-engineer/review.md`
**My review**: `conversus-output/spec-compliance/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: FR-001 compliance assessment divergence

Schema-engineer implicitly treats the plugin framework as complete. My review marks FR-001 as PARTIALLY MET because the engine's EngineConfig does not include a `plugins` field. The contradiction is in scope: schema-engineer evaluates the `config.py` module; I evaluate the end-to-end config pipeline from YAML file to engine startup.

**My position**: FR-001 says the config field "MUST allow declaring plugins." The config.py parsing module allows it. But if the engine ignores the parsed config, the field is allowed but not consumed. PARTIALLY MET is the accurate assessment: the feature exists but is not connected.

### DC-2: load_plugins() signature change — type safety vs. backward compatibility

Schema-engineer M-7 recommends changing `load_plugins(list[dict])` to `load_plugins(list[PluginConfigEntry])`. My review does not address the function signature. The type-safe version is better for production code. However, the current dict-based signature allows the test suite to pass raw dicts without constructing PluginConfigEntry objects. If the signature changes, all tests must construct PluginConfigEntry objects instead.

**My position**: The typed signature is correct. Tests should use the typed config objects. The migration is mechanical.

---

## Tensions

### T-1: PluginFacingConfig — additional model vs. existing dict

Schema-engineer R-1 recommends a typed `PluginFacingConfig` model. My review does not recommend typing the config. The tension is in maintenance cost: a PluginFacingConfig model must be kept in sync with the engine's config schema. If the engine adds a field that plugins need, the PluginFacingConfig must also be updated. The `dict[str, Any]` avoids this coupling.

**My position**: If PluginFacingConfig is adopted, it should be defined in the plugins package (not the engine), contain only stable fields (mode, rounds, iterations), and use `extra="allow"` to pass through unknown fields. This provides typing for common fields without creating a tight coupling.

### T-2: Dead positions field

Schema-engineer O-1 identifies `AgentState.positions` as dead. My review does not flag this specifically. The field is part of the spec's Section 2 DeliberationState definition ("positions, concessions, recommendations") but is never populated. If the field is removed from the model, the spec's Section 2 must be updated.

---

## Safe Agreements

- **SA-1: Frozen models are correctly applied** -- Both reviews agree all state models are properly frozen.

- **SA-2: Config parsing is robust** -- Both reviews agree `parse_plugins_config()` handles all edge cases.

- **SA-3: Plugin.name/hooks validation would improve error messages** -- Schema-engineer M-4 proposes validation. I agree this is a good defensive measure.

- **SA-4: FR-013 dependencies are minimal** -- Both reviews confirm pydantic + stdlib only.

- **SA-5: __all__ should be added** -- Schema-engineer R-8 recommends this. Consistent with standard Python packaging practice.
