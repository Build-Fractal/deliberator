# Spec Compliance Review — Revision 1

**Reviewer role**: spec-compliance
**Date**: 2026-03-22
**Revision trigger**: Cross-reviews from game-theorist and schema-engineer

---

### Recommendation Dispositions

**Rec 1 (P1 — Expand FR-003 type set or fix YAML type declarations): MODIFIED**

The finding stands: at least 6 YAML fields declare `type: list[string]` while examples and Pydantic models use `dict`-like structures. Both cross-reviewers independently confirmed this as the highest-impact bug (game-theorist DC-1, schema-engineer SA-1).

Modification: game-theorist correctly argues (DC-1) that only one direction is viable — the type set must be expanded, not the Pydantic models simplified. I originally framed this as a two-sided option ("expand type set or fix YAML"). That framing was wrong. The Pydantic models have the mathematically correct types (per-player mappings for asymmetric games); retrograding them to flat lists would destroy the mathematical structure. The resolution is unidirectional: add `map[string, string]` and `map[string, list[string]]` to FR-003, then update all YAML `type` declarations to match.

Additionally, schema-engineer (DC-2) correctly argues that this fix is incomplete without also wiring `VALID_FIELD_TYPES` into enforcement. My original Rec 9 (P3) proposed exactly this but at too low a priority. I now agree that Rec 1 and Rec 9 must be treated as a single P1 unit: expand the type set, update the YAML declarations, update the `VALID_FIELD_TYPES` constant, and add validation that YAML `type` values are members of that set. Doing one without the other creates a false sense of consistency.

**Rec 2 (P1 — Fix package name to `conversus-schemas`): MODIFIED**

The finding stands: the spec says `conversus-schemas`, the implementation says `conversus`. Both cross-reviewers confirmed this (schema-engineer T-4, game-theorist DC-4).

Modification: schema-engineer's T-4 raises a question I did not investigate — whether `conversus` is intentionally the umbrella package name for a project that will grow to include more modules (not just schemas). If so, FR-010 is the error, not `pyproject.toml`. I framed this as "fix pyproject.toml or update FR-010" but did not probe the project's intent. The cross-review makes clear this is a project-level architectural decision, not a simple compliance fix. The recommendation should be: resolve the naming intent with the project owner, then amend whichever artifact is wrong. Priority remains P1 because the mismatch blocks downstream consumers regardless of direction.

**Rec 3 (P1 — Configure YAML files as package data): SURVIVING**

Both cross-reviewers confirmed this finding with identical severity (game-theorist DC-4, schema-engineer SA-2). The `_schema_dir()` function using `Path(__file__).parent.parent.parent` will produce `FileNotFoundError` in any pip-installed deployment.

schema-engineer's T-3 adds a nuance I missed: moving YAML files into `src/conversus_schemas/` (one of my proposed fixes) would conflict with FR-001, which mandates `schema/game-forms/{form}.yml` as the file location. Any fix to FR-011 that relocates files also requires amending FR-001. I acknowledge this trade-off and note that `importlib.resources` with a `[tool.setuptools.package-data]` configuration can solve FR-011 without changing file locations, avoiding the FR-001 conflict entirely.

**Rec 4 (P2 — Add `form` field validation with `Literal` types): MODIFIED**

The finding stands. Both cross-reviewers confirmed this need (schema-engineer SA-3, game-theorist T-1).

Modification on priority: schema-engineer (T-2) makes a compelling argument that `Literal` types are a structural prerequisite for discriminated unions, and that treating `Literal` as P2 while the discriminated union (which depends on it) is deferred creates an unnecessary sequencing bottleneck. I originally rated this P2 because FR-007 says "type constraints" without specifically mentioning `Literal`. However, `form: str = "normal-form"` with no enforcement is a weak form of "type constraint" at best. I elevate this to P1 — not because a discriminated union is required by the current spec (it is not), but because FR-007's "enforce type constraints" is most naturally read as requiring the `form` field to be constrained to its expected value. A field with a default that accepts any string is a default, not a constraint.

game-theorist's T-1 raises whether the taxonomy is open or closed. This is a valid design question, but it does not change the recommendation: even in an open taxonomy, each model should enforce its own form identifier. Extensibility is handled by adding new models, not by allowing existing models to accept arbitrary form strings.

**Rec 5 (P2 — Make `ParametricGame` inherit from `GNEPGame`): MODIFIED**

The finding stands: `ParametricGame` duplicates all GNEP validation logic (lines 186-209 mirror lines 137-162), and the spec says "Inherits all GNEP fields."

Modification on implementation approach: schema-engineer (DC-1) elevates this to P1 based on `isinstance` type-identity concerns for downstream polymorphic dispatch. game-theorist (DC-3) notes the mathematical non-negotiability (parametric games must satisfy all GNEP invariants) but acknowledges Pydantic validator MRO subtleties.

In my original cross-review of schema-engineer (DC-2), I proposed extracting shared validators into a mixin or private base class rather than direct inheritance from `GNEPGame`, to avoid locking in an `isinstance` contract before downstream specs define whether they need it. I maintain that position. The spec says "inherits all GNEP fields" — this is a statement about field composition, not necessarily about Python class hierarchy. The fix should eliminate the code duplication (which is a correctness risk) while leaving the `isinstance` question for downstream specs to resolve. A shared validator mixin or a private `_GNEPBase` class achieves this.

I elevate to P1, agreeing with schema-engineer that the validation drift risk is too high for P2. But the implementation approach should be a shared base or mixin, not direct `class ParametricGame(GNEPGame)`.

**Rec 6 (P2 — `constraint_list` type consistency): MODIFIED**

The finding stands. schema-engineer's DC-3 sharpens the critique significantly: `constraint_list` is not merely ambiguous — it is a documentation fiction. The same YAML type name maps to `Optional[dict[str, list[str]]]` for local constraints and `Optional[list[str]]` for coupled constraints in the Pydantic layer. There is no Pydantic type alias, custom type, or validator that corresponds to the `constraint_list` label.

I originally framed this as "define semantics precisely or add a `constraint_map` type." schema-engineer is right that this understates the problem. The fix needs to: (a) split `constraint_list` into two distinct types in FR-003 (e.g., `constraint_list` for flat lists and `constraint_map` for per-player mappings), (b) update the YAML declarations, and (c) ensure `VALID_FIELD_TYPES` reflects the split. game-theorist's DC-2 adds that this also encodes a mathematical assumption about constraint scoping (per-player vs. shared), which should be documented in the schema description.

Elevated to P1 as part of the FR-003 type-set fix cluster.

**Rec 7 (P2 — SC-001 test granularity): SURVIVING**

Both cross-reviewers treat this as low-impact. game-theorist (T-5) agrees the test is correct and SC-001's wording is imprecise. schema-engineer (T-1) agrees but questions whether P2 overweights a documentation nit.

I maintain P2 but acknowledge the criticism. The test is correct; the spec wording is misleading. A comment in the test is sufficient. This is a documentation clarification, not a code change, and P2 may indeed be generous. I would not object to P3.

**Rec 8 (P3 — Negative tests for `form` field mismatch): SURVIVING**

No cross-reviewer contested this. It is a natural companion to Rec 4 (Literal types). If Rec 4 is implemented, these tests become the proof that the constraint works. Priority remains P3 because the tests would currently fail (validating that Rec 4 is needed first).

**Rec 9 (P3 — Test that `VALID_FIELD_TYPES` covers all YAML types): MODIFIED**

Elevated to P1. schema-engineer's DC-2 convinced me: expanding the type set (Rec 1) without also wiring enforcement creates a three-way inconsistency between the spec's FR-003 text, the `VALID_FIELD_TYPES` constant, and the YAML type declarations. The enforcement test is not a nice-to-have; it is the mechanism that keeps these three layers synchronized. This should be part of the same work unit as Rec 1.

**Rec 10 (P3 — Add `ModeMapping` and `ModeFormMapping` to exports): SURVIVING**

No cross-reviewer contested this. It remains a minor ergonomic improvement. P3 is appropriate.

---

### New Recommendations

**New-1 (P1 — Treat Recs 1, 6, and 9 as a single atomic FR-003 remediation)**

Source: schema-engineer DC-2, game-theorist DC-1 and DC-2.

The FR-003 type-set expansion, the `constraint_list`/`constraint_map` split, and the `VALID_FIELD_TYPES` enforcement wiring are interdependent. Doing any one without the others creates partial fixes that mask remaining inconsistencies. These three recommendations should be a single PR with a single test that loads every YAML schema, extracts all `type` values, and asserts membership in the updated `VALID_FIELD_TYPES` set.

**New-2 (P2 — Document constraint-scoping convention alongside type fix)**

Source: game-theorist DC-2.

When splitting `constraint_list` into flat and per-player variants, the YAML schema descriptions should explicitly document the variable-scoping convention: `local_constraints` are partitioned by player and each constraint depends only on that player's variables (`g_i(x_i)`), while `coupled_constraints` are shared and may depend on all players' variables (`h(x_1, ..., x_N)`). This is implicit in the current schema structure but not stated anywhere. Making it explicit prevents downstream specs from misinterpreting the constraint types.

**New-3 (P2 — Acknowledge that FR-011 fix may require FR-001 amendment)**

Source: schema-engineer T-3.

Neither my original review nor any cross-review explicitly noted that the two most natural fixes for FR-011 (moving YAML files into the package directory, or using `importlib.resources` with package-data config) interact with FR-001's mandated file paths. The spec should be amended to either: (a) update FR-001's paths if files are relocated, or (b) add a `[tool.setuptools.package-data]` requirement to FR-011 that explicitly includes the `schema/` directory from the project root. This is a spec-level coordination issue, not just an implementation task.

---

### Position Summary

After reading both cross-reviews, my overall compliance assessment tightens rather than loosens. The three P1 findings from my original review (FR-003 type mismatches, package naming, package data) all survive scrutiny and are reinforced by independent confirmation. The most significant revision is the elevation of two items: `VALID_FIELD_TYPES` enforcement (from P3 to P1, per schema-engineer's argument that unenforced type sets are worse than no type sets) and `Literal` types on the `form` field (from P2 to P1, per both cross-reviewers' arguments about type-system prerequisites). The `ParametricGame` inheritance recommendation also moves to P1, though I modify the implementation approach to favor a shared base or mixin over direct inheritance, to avoid prematurely committing to an `isinstance` contract.

The most important intellectual concession is on Rec 1's directionality. I originally presented the FR-003 type mismatch as a two-sided option (fix the spec or fix the YAML). game-theorist correctly identified that this framing obscures the mathematical reality: the Pydantic models have the right types, and the YAML declarations have the wrong ones. The fix is unidirectional. I withdraw the "or" framing and adopt the "expand the type set" direction exclusively.

The revised priority landscape is: five P1 items (FR-003 type remediation as an atomic cluster, package naming resolution, package data configuration, `Literal` types on `form`, `ParametricGame` validation deduplication), two P2 items (SC-001 clarification, constraint-scoping documentation), and two P3 items (negative `form` tests, export ergonomics). This is a net increase in urgency from the original review, driven by legitimate arguments from both cross-reviewers about the interconnected nature of the type-system issues.
