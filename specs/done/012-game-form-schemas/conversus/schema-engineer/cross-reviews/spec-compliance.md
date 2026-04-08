# Cross-Review: spec-compliance Phase 1 Review

**Cross-reviewer**: schema-engineer
**Reviewing**: spec-compliance's Phase 1 review of 012-game-form-schemas
**Date**: 2026-03-22

---

## Dangerous Contradictions

### DC-1: We disagree on the priority of `ParametricGame` inheritance vs. discriminated union

spec-compliance rates `ParametricGame` inheritance as P2 (Recommendation 5), treating it primarily as a code duplication concern. My review rates it P1 (Recommendation 4), because the inheritance gap has type-system consequences beyond maintenance: `isinstance(parametric_game, GNEPGame)` returning `False` will break polymorphic acceptance in downstream specs (016, 017, 019) that want to handle "any GNEP-like game." spec-compliance acknowledges the validation drift risk but does not connect it to the type identity problem. Both reviews agree on the fix (inherit from `GNEPGame`), but the priority difference matters for implementation order. If the discriminated union (my Recommendation 2) is built first without fixing inheritance, `ParametricGame` will be a separate branch in the union rather than a subtype of `GNEPGame`, and downstream specs that pattern-match on `GNEPGame | ParametricGame` will need to handle both explicitly. The inheritance fix must land before or concurrently with the discriminated union, not after.

### DC-2: Scope of the FR-003 type-set fix

spec-compliance proposes adding `map[string, string]` and `map[string, list[string]]` to the FR-003 closed type set (Recommendation 1). My review (Recommendation 8) frames this as a YAML-vs-Pydantic alignment issue but does not prescribe the exact type names. The contradiction is subtle but real: spec-compliance's proposal expands the FR-003 type vocabulary, which has ripple effects on any tooling that parses the `type` field from YAML. My concern, which spec-compliance does not address, is that `VALID_FIELD_TYPES` in `game_forms.py` (line 24-33) is a frozenset that is never actually validated against the YAML schemas. spec-compliance's Recommendation 1 fixes the YAML declarations but does not close the enforcement gap -- the constant remains dead code. If we add `map[string, ...]` types to the YAML and to `VALID_FIELD_TYPES` but still never validate YAML field types against that set, we have papered over a documentation inconsistency without solving the enforcement problem. Both fixes are needed together: expand the type set AND wire `VALID_FIELD_TYPES` into validation (spec-compliance's own Recommendation 9 at P3, which should be elevated to P1 alongside Recommendation 1).

### DC-3: `constraint_list` semantics are more broken than spec-compliance acknowledges

spec-compliance's Recommendation 6 (P2) notes that `constraint_list` is used for both flat lists (`coupled_constraints: list[str]`) and per-player mappings (`local_constraints: dict[str, list[str]]`). The recommendation is to either define semantics precisely or add a `constraint_map` type. My review (Off-Base Assumptions, point 4) goes further: `constraint_list` is a type name that appears in `VALID_FIELD_TYPES` and in the YAML schemas but has zero representation in the Pydantic validation layer. There is no Pydantic type alias, no custom type, no validator that corresponds to it. It is a documentation fiction -- the Pydantic models use `Optional[dict[str, list[str]]]` and `Optional[list[str]]` directly, with no connection to the `constraint_list` label. This is not a P2 "ambiguity" issue; it is a P1 type-system hole. Any downstream codegen tool (spec 013's template validation, spec 015's feature extraction) that reads `type: constraint_list` from the YAML will have no Pydantic-side contract to rely on, because the same type name maps to structurally different Python types depending on context.

---

## Tensions

### T-1: SC-001 test granularity -- how literally should success criteria be read?

spec-compliance (Recommendation 7, P2) flags that the test validates `data["example"]` rather than the entire YAML file as SC-001's literal code suggests. spec-compliance correctly notes the test is right in spirit but the SC wording is misleading. My review did not flag this, because from a schema-engineering perspective the test is doing the correct thing: the top-level YAML structure (`fields`, `description`) is metadata about the schema, not a game instance. The tension is about whether spec compliance requires matching the letter or the intent of success criteria. spec-compliance's recommendation to add a comment documenting the intentional deviation is proportionate and I agree with it -- but elevating this to P2 may overweight a documentation nit relative to the P1 type-system issues both reviews identify.

### T-2: `form` field -- `Literal` types vs. negative tests

Both reviews agree that `form: str = "normal-form"` should be `form: Literal["normal-form"]`. spec-compliance raises this as P2 (Recommendation 4) and separately proposes negative tests for `form` mismatch (P3, Recommendation 8). My review rates `Literal` types as P1 (Recommendation 1) because they are a prerequisite for discriminated unions (my Recommendation 2), which I also rate P1. The tension: spec-compliance treats `Literal` as a defensive measure against misuse; I treat it as a structural prerequisite for polymorphic deserialization. If we follow spec-compliance's P2 prioritization, discriminated unions cannot be built until after the `Literal` fix, creating an unnecessary sequencing dependency. The `Literal` fix, the discriminated union, and the `ParametricGame` inheritance fix are a single atomic unit of work from a type-system perspective and should all be P1.

### T-3: Package data resolution -- `importlib.resources` vs. moving YAML files

Both reviews identify `_schema_dir()` as broken for installed packages (spec-compliance Recommendation 3 at P1, my Recommendation 3 at P1). spec-compliance offers two alternatives: `importlib.resources` or moving YAML files into `src/conversus_schemas/`. My review additionally suggests embedding schema data as Python constants if the files are small. The tension is about which approach to choose. From a schema-engineering perspective, moving the YAML files into the package directory is the cleanest solution because it keeps the YAML files as actual YAML (preserving readability and editability) while making them automatically included in wheel builds. `importlib.resources` adds API complexity for a problem that directory layout solves. However, moving the files changes the directory structure that FR-001 mandates (`schema/game-forms/{form}.yml`), which would require a spec amendment. spec-compliance does not flag this conflict with FR-001; I did not either. Both reviews need to acknowledge that any fix here requires a spec update.

### T-4: Package naming -- `conversus` vs. `conversus-schemas`

Both reviews flag the FR-010 mismatch (spec-compliance Recommendation 2 at P1, my review in the Executive Summary). spec-compliance offers the alternative of updating FR-010 to match the actual name. My review does not take a position on which direction to go. The tension: if `conversus` is the correct pip name (because `conversus-schemas` is a sub-package of a broader `conversus` project), then FR-010 needs a spec amendment. If `conversus-schemas` is correct, then `pyproject.toml` needs renaming. This is a project-level architectural decision that neither review can resolve in isolation -- it depends on whether future specs (013-020) will add more modules to the same `conversus` package or ship as separate packages.

### T-5: `ModeMapping.lookup()` error handling

My review (Missed Opportunities, last bullet in the low-priority section) notes that `lookup()` raises a raw `KeyError` and suggests a custom `ModeNotFoundError` subclass. spec-compliance does not flag this at all. This is a minor tension: spec-compliance focuses on whether the mapping function exists and works (it does), while I focus on the ergonomics of the error type for downstream consumers. The current `KeyError` includes a helpful message (listing available modes), which partially addresses the concern. But for downstream specs that need to distinguish "mode not found" from other `KeyError` sources in a try/except chain, the custom exception remains worthwhile. Low priority for both reviews; noting for completeness.

---

## Safe Agreements

### SA-1: FR-003 YAML-to-Pydantic type mismatch is the highest-impact bug

Both reviews independently identify this as the most critical issue. spec-compliance catalogs 6+ specific fields where the YAML `type` declaration disagrees with both the Pydantic model type and the YAML example (Missed Opportunities, FR-003 entries). My review flags the same fields (Off-Base Assumptions, point 3; Recommendation 8). We agree the YAML schemas are the canonical documentation layer and must be self-consistent. We agree this is P1. The only difference is in the proposed fix approach (spec-compliance: expand FR-003 type set; my review: align types without prescribing names), which is a tension, not a disagreement on severity.

### SA-2: `_schema_dir()` path traversal will break in installed packages

Both reviews flag this as P1 and agree it violates FR-011. spec-compliance's Recommendation 3 and my Recommendation 3 describe the same problem with the same severity assessment. We agree that the current `Path(__file__).parent.parent.parent` approach is a development-only convenience that will produce `FileNotFoundError` in any pip-installed deployment.

### SA-3: No solver imports is correctly enforced

Both reviews confirm FR-008 compliance. spec-compliance notes the explicit comment on line 8 and the test coverage. My review notes the `sys.modules` check in `test_no_solver_imports`. We agree this boundary is cleanly respected and well-tested.

---

## Summary

The two reviews converge strongly on the critical issues: FR-003 type mismatches, broken package data resolution, and the `form` field needing `Literal` types. The primary disagreement is on prioritization: I rate `Literal` types, discriminated unions, and `ParametricGame` inheritance as a single P1 cluster (because they are type-system prerequisites for each other), while spec-compliance spreads these across P2 items. The actionable takeaway: the three type-identity fixes (Literal, discriminated union, inheritance) should be treated as one atomic P1 work unit, alongside the FR-003 type-set expansion and `VALID_FIELD_TYPES` enforcement wiring.
