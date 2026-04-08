# Schema Engineer Cross-Review of Spec Compliance
# Spec: 016-plugin-system

**Cross-reviewer**: schema-engineer
**Reviewing**: spec-compliance's review at `conversus-output/spec-compliance/review.md`
**My review**: `conversus-output/schema-engineer/review.md`
**Date**: 2026-03-24

---

## Dangerous Contradictions

### DC-1: FR-001 compliance — PARTIALLY MET vs. framework-complete

Spec-compliance marks FR-001 as PARTIALLY MET because the engine's `EngineConfig` does not include a `plugins` field. My review does not assess FR compliance but implicitly treats the framework as complete (the config parsing module exists and works). The contradiction is in what "MET" means: does FR-001 require (a) the parsing module to exist, or (b) the parsing module to be wired into the engine config? The spec says "A `plugins` field in `conversus.yml` MUST allow declaring plugins." This is about the config file format, not the engine parser. The parsing module can process the YAML field independently. If the engine does not consume it yet, the config format itself is still valid.

**My position**: FR-001 is MET at the config-parsing layer. The engine integration is a separate deliverable (FR-003/FR-006). Spec-compliance's PARTIALLY MET conflates two requirements.

### DC-2: FR-012 package naming — consistent treatment with spec 015

Spec-compliance marks FR-012 as NOT MET. My review does not address this. The same issue exists in spec 015 (FR-014). Both should be amended consistently: `conversus.plugins` is the actual namespace, and the spec should reflect it.

---

## Tensions

### T-1: FR-011 empty directory caveat

Spec-compliance's FR-011 caveat (empty `plugins/` directory changes output structure) is a minor point. My review M-8 flags the same issue but at a different severity. The tension is whether an empty `plugins/` directory violates FR-011's "identical" requirement. I agree with plugin-architect's position (in their cross-review): `plugins/` is not core output, so FR-011 is MET without caveat.

### T-2: Integration test scope

Spec-compliance R-3 recommends a P1 integration test. My review does not recommend integration tests. The existing test suite covers all plugin framework behavior in isolation. An integration test requires engine modifications that are not part of the plugin framework itself. The integration test should be part of the engine integration deliverable, not the framework spec.

---

## Safe Agreements

- **SA-1: FR-002 (empty config) is MET** -- Both reviews agree.

- **SA-2: FR-004 (importlib loading) is MET** -- Both reviews agree.

- **SA-3: FR-005 (missing package resilience) is MET** -- Both reviews agree.

- **SA-4: FR-007 (sequential execution) is MET** -- Both reviews agree.

- **SA-5: FR-008 (exception isolation) is MET** -- Both reviews agree.

- **SA-6: FR-013 (minimal dependencies) is MET** -- Both reviews agree.

- **SA-7: All five SC pass** -- Both reviews agree with identical test evidence.
