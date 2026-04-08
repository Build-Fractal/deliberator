# Schema Engineer Cross-Review of Spec-Compliance Review
# Spec: 013-objective-function-templates

**Cross-reviewer**: schema-engineer
**Reviewing**: spec-compliance's review at `conversus-output/spec-compliance/review.md`
**My review**: `conversus-output/schema-engineer/review.md`
**Target**: `conversus/conversus/schemas/objectives.py`
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1: Example field standardization — incompatible remediation paths

Spec-compliance (Missed Opportunity 3, Recommendation 3) frames the example format inconsistency as a documentation uniformity problem and recommends standardizing on the flat key-value format, optionally promoting `computed_objective` to all templates as a documentation-only convention. My review (M-3, M-4, R-3, R-4) agrees on the flat format but treats the inconsistency as a model correctness problem and recommends adding a model-level cross-validator that rejects example keys not present in the `parameters` list.

These two positions are mutually exclusive at the point of implementation. Spec-compliance's option to retain `computed_objective` as a formalized annotation key would cause every template to fail my proposed R-4 validator, because `computed_objective` is not a parameter name. Conversely, implementing R-4 first would force immediate removal of `computed_objective` from every cross-mode template before spec-compliance's "document-then-standardize" approach has time to decide whether to retain it. One of us must yield: either the cross-validator is relaxed to allow a whitelist of annotation keys (e.g., `computed_objective`, `example_note`), or `computed_objective` is removed outright before R-4 lands. The two reviews do not propose a compatible middle path.

**Resolution needed**: Decide whether `computed_objective` is a first-class schema concept (add to ObjectiveTemplate as a separate optional field), a tolerated annotation key (whitelist in R-4), or removed entirely. This decision gates both the YAML standardization and the model validation work.

### DC-2: `click` dependency — violation vs. exemption, with different urgency signals

Spec-compliance (Off-Base Assumption 1, Recommendation 6) flags the `click` dependency at project level as a potential Section 5 violation and recommends moving it to an optional dependency group (`[project.optional-dependencies] cli = ["click>=8.3.1"]`). The priority is MEDIUM. My review does not flag this issue at all — I read the Section 5 constraint as applying to the schema package's runtime imports, not to the top-level project tooling, and so treated `click` as out of scope.

The contradiction is in severity assessment, not in the underlying fact. If spec-compliance is correct that a strict reading of Section 5 counts project-level dependencies, then my review silently passed a violation that should have been flagged. If my implicit reading is correct that Section 5 governs runtime import behavior rather than packaging metadata, then spec-compliance is raising a concern that does not exist. The implementation of `objectives.py` itself imports nothing beyond pydantic and pyyaml (at runtime), which is the relevant constraint for a schema-only package. However, the `pyproject.toml` does declare `click` as a non-optional dependency, meaning `pip install conversus` installs click even for users who never touch the linter CLI. Spec-compliance's remediation is correct regardless of which reading of Section 5 is authoritative.

**Resolution needed**: Amend the spec to clarify whether Section 5 governs runtime imports, installed dependencies, or both. Apply spec-compliance's optional-dependency refactor independently of that clarification, since it is a packaging best practice regardless.

### DC-3: `cooperative-fairness` classification — undocumented addition vs. valid "at-least" extension

Spec-compliance (Missed Opportunity 6) treats `cooperative-fairness` as spec drift — an undocumented addition not listed in Section 2's catalog — and recommends updating the spec to document it. My review (A-6) dismisses this concern entirely, noting that the spec says "at least" for the per-mode count, making any additional cooperative template valid by definition.

These are contradictory dispositions toward the same fact. My reading is technically correct for the cardinality requirements (FR-013 says ">= 3 per mode"), but it elides spec-compliance's separate and valid point: Section 2 of the spec provides a named catalog, and `cooperative-fairness` does not appear in it. A catalog that omits an existing member is factually wrong, independent of whether the minimum count is met. My review should have flagged the catalog gap even while noting that FR-013 itself passes. The contradiction is that my review implies no action is needed while spec-compliance correctly identifies that the spec's catalog section must be updated.

**Resolution needed**: Update spec Section 2 to include `cooperative-fairness`. This is a spec amendment, not a code change. My review was wrong to dismiss it as non-actionable.

### DC-4: Constraint template forward-compatibility — model gap vs. intentional minimalism

Spec-compliance (Off-Base Assumption 3, Recommendations 4 and 8) treats the absence of `description` and `example` fields on `ConstraintTemplate` as a forward-compatibility gap that will force downstream spec-014 code to special-case constraints vs. objectives. My review (M-6, O-3, R-nothing-explicit) agrees that `description` is missing but does not recommend adding `example` to `ConstraintTemplate`, treating the FR-007 spec text as deliberately minimal for constraints.

The dangerous contradiction is in the projected spec-014 impact. Spec-compliance implies that if constraints lack `example` and `description`, the guided construction pipeline will need two separate code paths. My review's silence on `example` for `ConstraintTemplate` implicitly accepts that asymmetry. But if spec-014 is built assuming uniform schema (both objectives and constraints expose `description` and `example`), omitting these fields now creates a breaking change later. The reviews cannot both be right about the forward-compatibility risk while proposing different remediation scopes.

**Resolution needed**: Explicitly decide the contract for spec-014 consumption of constraint templates before closing this spec. If spec-014 will treat objectives and constraints uniformly, both fields must be added now.

---

## Tensions

### T-1: Constraint reference validation — closed set vs. filesystem lookup

My review (M-2, R-2) recommends a `VALID_CONSTRAINTS` frozenset in `objectives.py` that validates constraint references against a hardcoded list of six names. Spec-compliance does not raise this gap at all — neither in Missed Opportunities nor in Recommendations. The silence is a meaningful tension: spec-compliance read the constraint reference list as a documentation field rather than a referentially-validated pointer, which is consistent with the spec's FR-008 wording ("compatible constraint templates (references)"). My reading treats "references" as implying integrity checking.

The tension matters for maintenance: a `VALID_CONSTRAINTS` frozenset requires manual update when a new constraint template is added, creating a second source of truth alongside the `schema/objective-functions/constraints/` directory. Spec-compliance's implicit approach avoids this but accepts that typos in constraint references silently pass validation. Neither review proposes the third option: derive `VALID_CONSTRAINTS` dynamically from the filesystem at import time (consistent with my R-7 loader utility). That option resolves the tension but introduces a filesystem dependency in what is otherwise a pure-Pydantic module.

### T-2: Test infrastructure gap — who owns SC-001, SC-002, SC-003?

Spec-compliance (Missed Opportunities 4, 5 and Recommendation 2) gives HIGH priority to creating `tests/test_objectives.py` covering SC-001 through SC-003, treating the missing tests as the most urgent gap after the import path discrepancy. My review does not recommend creating a test file at all — I surface the gap (M-9 references the `load_mode_mapping` pattern as something that should be paralleled) but scope my recommendations to the schema module itself rather than the test suite.

This is a priority tension rather than a factual disagreement. Both reviews agree that SC-001, SC-002, and SC-003 are currently untestable in CI. Spec-compliance's urgency is appropriate: success criteria that cannot be verified in CI are not success criteria. My review's omission of a test recommendation is a gap in my analysis. However, the test infrastructure work depends on resolving DC-1 (example format) and DC-2 (import path) first, because a test that loads all 21 YAMLs will fail if example format validation is tightened before the YAMLs are updated, and SC-001 as written uses the wrong import path. Sequencing matters here, and neither review provides an explicit dependency ordering.

### T-3: `extra="forbid"` — correctness guard vs. compatibility risk

My review (R-10) recommends adding `model_config = ConfigDict(extra="forbid")` to all three models to prevent silent acceptance of unexpected YAML keys. Spec-compliance does not address this recommendation. The tension is that `extra="forbid"` would immediately break the current cross-mode YAML templates, which include `computed_objective` and other non-parameter keys inside `example` blocks. If R-10 is applied before DC-1 is resolved (the example format standardization), it causes cascading validation failures across seven of twenty-one templates.

Spec-compliance's more conservative approach — fix the YAMLs first, validate more strictly later — is implicitly the safer sequencing. My R-10 is technically sound but operationally premature given the current state of the YAML files. This creates a dependency ordering tension: my own recommendations (R-3 YAML standardization, then R-10 strict validation) must be sequenced correctly, and spec-compliance's framing helps establish that order more clearly than my review does.

### T-4: `boolean` parameter type — schema extension vs. spec scope control

My review (M-8, R-6) recommends adding `boolean` to the parameter type vocabulary, citing the `normalize` parameters in `weighted-sum` and `minimax` as concrete instances where `type: string` with values `"true"`/`"false"` degrades downstream usability. Spec-compliance (Off-Base Assumption 2) separately identifies the four-type system as "too narrow" but frames this as a concern about `string` being used for structured data (arrays, matrices), not booleans specifically.

Both reviews agree the type system has gaps; they disagree on which gaps to fill. Spec-compliance recommends an `array`/`object` type for structured parameters (weights, Q matrices, tolerance lists). My review recommends `boolean` for flag parameters. These are compatible extensions but imply different priorities: two affected parameters (boolean case) versus five or more affected parameters (array case). If only one extension is approved, spec-compliance's `array` type addresses a wider surface area. If both are approved, the spec must define how `array` parameters are validated (element type, shape), which is a non-trivial schema design question not addressed by either review.

### T-5: Loader utility placement — `objectives.py` vs. new `registry.py`

Both reviews recommend a loader/registry utility, but differ in scope and placement. My review (R-7) recommends `load_objective_template()` and `load_all_objective_templates()` functions added directly to `objectives.py`, mirroring `load_mode_mapping()` in `game_forms.py`. Spec-compliance (Missed Opportunity 8, Recommendation 9) recommends a `load_all_templates()` function but suggests it could live in a new `registry.py` module.

The tension is architectural. Placing the loader in `objectives.py` maintains the established pattern from `game_forms.py` and keeps the module self-contained, but it introduces a filesystem dependency into a module that is otherwise pure Pydantic. A `registry.py` separation keeps `objectives.py` as a pure schema definition while isolating the I/O concern, which is better for unit testing the models independently of the file system. Neither review acknowledges this trade-off explicitly. The `game_forms.py` precedent favors my approach, but `game_forms.py` predates this architectural concern and may itself be a flawed precedent.

---

## Safe Agreements

### SA-1: FR-011 import path discrepancy is the highest-priority blocking issue

Both reviews independently identify the mismatch between FR-011's specified import path (`from conversus_schemas.objectives import ...`) and the actual implementation path (`from conversus.schemas.objectives import ...`) as the most critical deviation. Spec-compliance (CRITICAL recommendation 1) and my review (O-1, R-8, HIGH priority) agree that this produces an ImportError against the current code and must be resolved before any downstream consumer can use the package. Both reviews prefer option (b): amend FR-011 to match the actual `conversus.schemas` namespace rather than renaming the package, on the grounds that the namespace was already established by spec-012's `game_forms.py`. There is no disagreement on the diagnosis, the priority, or the preferred resolution path.

### SA-2: Example format must be standardized to the flat key-value form

Despite the DC-1 contradiction over `computed_objective`'s fate, both reviews reach the same core conclusion: the flat parameter-name-to-value format (as seen in `cooperative-integration.yml`) is the correct structure for `example` blocks, and the nested full-template-structure format used by seven cross-mode templates (`weighted-sum`, `minimax`, `lexicographic`, `budget-constrained`, `time-constrained`, `general-linear`, `general-quadratic`) violates the spec's "minimal valid parameterization" intent in FR-002. Spec-compliance (Missed Opportunity 3, Recommendation 3) and my review (M-3, R-3) agree on the diagnosis and the target format. The disagreement is only about whether `computed_objective` is retained as an annotation, not whether the nesting structure is wrong.

### SA-3: `ConstraintTemplate` is missing `description` and the asymmetry is a real gap

Both reviews agree that the absence of a `description` field on `ConstraintTemplate` creates an asymmetry with `ObjectiveTemplate` that will become problematic when spec-014's guided construction pipeline consumes both. Spec-compliance (Missed Opportunity 7, Recommendation 8) and my review (M-6, O-3) converge on adding `description: Optional[str] = None` to the Pydantic model and promoting the existing YAML header comments to machine-readable description fields. Neither review disputes this as a LOW-to-MEDIUM priority addition with no downside risk.

### SA-4: No test file for objective templates is a CI gap that must be closed

Both reviews agree that the absence of `tests/test_objectives.py` leaves SC-001, SC-002, and SC-003 unverified in CI, reducing all three from "success criteria" to "author assertions." Spec-compliance (Missed Opportunities 4 and 5, Recommendation 2) catalogs the specific test cases needed. My review's R-7 loader utility directly enables that test infrastructure. Both agree that the existing `tests/test_game_forms.py` provides the pattern to follow and that writing these tests is straightforward once the loader utility and the import path are resolved. The only disagreement is sequencing (see T-2), not whether the tests are needed.
