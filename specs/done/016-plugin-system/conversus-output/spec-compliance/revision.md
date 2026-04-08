# Spec Compliance Revision: 016 Plugin System Infrastructure

**Reviewer**: spec-compliance
**Revision iteration**: 1
**Date**: 2026-03-24

---

## Recommendation Dispositions

#### Recommendation 1: Wire plugin loading and execution into engine pipeline

- **Original position**: Add `plugins` to EngineConfig, call load_plugins() and execute_hooks().
- **Disposition**: Surviving
- **Explanation**: Plugin-architect R-5 and DC-2 (cross-review) both endorse engine integration as the critical deliverable. All three reviews agree this is the highest-priority gap. FR-006 is NOT MET without it.

#### Recommendation 2: Amend FR-012 package naming

- **Original position**: Change FR-012 to reference `conversus.plugins`.
- **Disposition**: Surviving
- **Explanation**: Plugin-architect DC-2 agrees. Schema-engineer DC-2 agrees. Consistent with spec 015's FR-014 amendment. No challenges.

#### Recommendation 3: Add integration test for end-to-end plugin execution

- **Original position**: Run a deliberation with a configured plugin and verify output.
- **Disposition**: Modified
- **Explanation**: Schema-engineer T-2 argues the integration test should be part of the engine integration deliverable, not a separate test task. Plugin-architect T-2 notes the test depends on engine integration being done first. Modified: the integration test is a validation step for R-1 (engine integration), not a separate recommendation. Priority remains P1 as part of R-1's acceptance criteria.

#### Recommendation 4: Only create plugins/ dir when plugins produce output

- **Original position**: Strengthen FR-011 compliance.
- **Disposition**: Surviving
- **Explanation**: Plugin-architect T-1 argues FR-011 is MET regardless. Schema-engineer R-7 maintains the fix at P3. Both assessments are valid. The fix is trivial and eliminates ambiguity. Maintaining at P3.

#### Recommendation 5: Document engine integration contract

- **Original position**: Specify where hooks fire in the engine.
- **Disposition**: Surviving
- **Explanation**: Plugin-architect R-5 provides the exact integration points. This recommendation is complementary to R-1: R-1 says "do it," R-5 says "document where." Both are needed.

---

## New Recommendations

- **Remove `config` parameter from Plugin.execute()** (Priority: P1)
  - Triggered by: Plugin-architect R-2 (revised) and schema-engineer NR-1 both proposing the simplified signature.
  - Proposed change: Change `execute(self, state, config)` to `execute(self, state)`. This is a breaking change to the Plugin ABC, but no external plugins exist yet. All test plugins would be updated.
  - Rationale: Eliminates the confusing triple-config pattern. Plugin-architect and schema-engineer both independently converge on this simplification.

- **Add `plugins` field to EngineConfig** (Priority: P1)
  - Triggered by: FR-001 assessment as PARTIALLY MET.
  - Proposed change: Add `plugins: list[PluginConfigEntry] = []` to EngineConfig. The engine config parser calls `parse_plugins_config()` on the raw YAML and populates this field.
  - Rationale: Completes the config pipeline from YAML to engine startup. Without this, FR-001 remains PARTIALLY MET.

---

## Position Summary

Withdrew 0, modified 1, maintained 4. Added 2 new recommendations.

The most significant change is R-3 (integration test), which was folded into R-1 as an acceptance criterion rather than a standalone task. The two new recommendations (remove config param, add plugins to EngineConfig) emerged from cross-review consensus.

My highest-priority surviving recommendation is R-1 (engine integration). This is the single deliverable that moves FR-001, FR-003, and FR-006 from PARTIALLY MET to MET.
