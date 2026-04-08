# Spec Compliance Revision: 013-objective-function-templates

**Role**: spec-compliance
**Revision**: 1
**Date**: 2026-03-23

---

## Recommendation Dispositions

### R1 — CRITICAL: Reconcile Import Path (FR-011)
**Disposition**: MAINTAINED, reclassified to HIGH

The CRITICAL classification drew the sharpest pushback from all three cross-reviewers. functional-architect (DC-1) argued the import path is "spec noise" at an unreleased v1 stage; schema-engineer confirmed both reviews prefer amending FR-011 to match `conversus.schemas` rather than restructuring the package; game-theorist did not contest the finding but implicitly deprioritized it relative to mathematical correctness issues.

The reclassification to HIGH is warranted. The import path is a genuine FR-011 deviation and will produce an ImportError for any consumer following the spec's example verbatim — that is not noise. However, CRITICAL implies it must be resolved before all other work, and DC-1 from functional-architect and DC-3 from game-theorist correctly establish that mathematical correctness errors in the templates have operational consequences that are at least as severe. The import path also has a clear, low-risk resolution: amend FR-011 to `from conversus.schemas.objectives import ...`, which both schema-engineer and spec-compliance's own cross-reviews identify as the consensus path.

The compatibility alias option is withdrawn. Both schema-engineer (R-8) and spec-compliance's own cross-review of schema-engineer (DC-3) agree that a compatibility alias creates two sources of truth without adding value. Spec amendment only.

### R2 — HIGH: Add `tests/test_objectives.py` Covering SC-001, SC-002, SC-003
**Disposition**: MAINTAINED, scope refined

All three cross-reviews confirm this as the most urgently actionable shared finding (game-theorist SA-1, functional-architect SA-1, schema-engineer SA-4). The recommendation stands.

One refinement is adopted from game-theorist (DC-3): tests that load every YAML and validate it against `ObjectiveTemplate` will pass even for templates with mathematical errors, because `ObjectiveTemplate` validates structure not correctness. The test file should be understood as a schema compliance test suite, not a mathematical correctness guarantee. This distinction is not a reason to deprioritize the tests; it is a reason to be explicit about what they verify and what they do not.

A second refinement is adopted from functional-architect (T-4): a `validate_library_integrity()` pure function (or equivalent) should be the implementation backing the test assertions, not ad-hoc fixture logic inline in each test. The test file calls the function; the function is reusable by spec 014. These are complements, not alternatives.

Sequencing note from schema-engineer (T-2): the test file should be written after the FR-011 import path is resolved and after the example format is standardized (R3 below), otherwise the tests will need immediate rework.

### R3 — HIGH: Standardize `example` Block Format
**Disposition**: MAINTAINED, `computed_objective` disposition resolved

The recommendation to remove `name`, `form`, and `game_form` from example blocks in cross-mode templates is uncontested across all cross-reviews (functional-architect SA-2, schema-engineer SA-2, game-theorist SA-3).

The `computed_objective` question produced a dangerous contradiction between schema-engineer (DC-1) and spec-compliance's own position. The resolution: `computed_objective` is removed from example blocks in all templates. It is not promoted to a separate field and is not retained as a tolerated annotation key. The spec's FR-002 language — "minimal valid parameterization" — means parameter names and values only. A `computed_objective` key is not a parameter; it is a documentation annotation that belongs in the template's `description` field or in the spec's Section 2 narrative, not in the machine-readable example block. This forecloses schema-engineer's DC-1 and clears the path for the example-key cross-validator schema-engineer proposed (R-4), without which spec 014 cannot treat example blocks as safely machine-parseable.

One addition: this example standardization work must precede `extra="forbid"` enforcement (schema-engineer R-10, T-3). The sequencing is: (1) remove redundant keys from examples, (2) optionally add example-key cross-validator, (3) consider `extra="forbid"`.

### R4 — MEDIUM: Add Examples to Constraint Templates (SC-005)
**Disposition**: MAINTAINED

No cross-review contested this. schema-engineer (DC-4) raised the adjacent point that if `ConstraintTemplate` gains an `example` field, it should have an equivalent example-key validator consistent with whatever is adopted for `ObjectiveTemplate`. That is a valid sequencing note, not a reason to drop R4.

The SC-005 interpretation question — does "template" include constraint templates? — is not resolved by any cross-review. The conservative reading stands: SC-005 should apply to constraint templates. The cost of adding six minimal example parameterizations is low; the cost of leaving them absent and later finding SC-005 applies is a retroactive refactor.

### R5 — MEDIUM: Update Spec Section 2 to Include `cooperative-fairness`
**Disposition**: MAINTAINED, with prerequisite added

All cross-reviews confirm the template exists and is not in the spec's Section 2 catalog (game-theorist SA-2, schema-engineer DC-3, functional-architect SA-4). game-theorist (T-2) correctly establishes a prerequisite: the dimensional inconsistency in `cooperative-fairness`'s formula (`J = -min_i(allocation_i) + phi * variance(allocation)` mixes allocation units with allocation-squared units, making phi scale-dependent) should be corrected before the formula is canonized in the spec. The template should be updated to use normalized variance or Gini coefficient, then added to Section 2.

The sequencing is: (1) fix the dimensional inconsistency in the YAML, (2) amend spec Section 2 with the corrected formula. Ratifying a dimensionally unsound formula in the spec creates a spec-level error that is harder to correct later.

### R6 — MEDIUM: Isolate `click` Dependency
**Disposition**: MAINTAINED, scope clarified

The cross-reviews split three ways on this: schema-engineer (DC-2) endorsed the fix but questioned the interpretation; game-theorist (T-1) acknowledged the finding as plausible; functional-architect (DC-2 in its cross-review of spec-compliance) questioned whether the finding should have been in "Off-Base Assumptions" at all.

The finding is moved out of "Off-Base Assumptions" framing. The `click` dependency at project level means `pip install conversus` installs click for all users, including those who will never touch the linter CLI. This is a packaging hygiene issue regardless of how Section 5 is ultimately interpreted. Moving `click` to an optional dependency group (`[project.optional-dependencies] cli = ["click>=8.3.1"]`) is a net improvement under any reading of the spec. The spec should be clarified to state whether Section 5 governs runtime imports only or installed package dependencies — but that clarification is not a prerequisite for the packaging fix.

### R7 — LOW: Consider Adding `array` Parameter Type
**Disposition**: MAINTAINED, deferred to spec amendment track

This cannot be implemented unilaterally. FR-003 enumerates the type vocabulary exhaustively. Adding `array` without amending FR-003 creates the same kind of spec-vs-implementation drift that R1 (import path) represents. functional-architect (DC-2) correctly flags that extending the type system is a breaking change.

The `array` and `boolean` extensions (schema-engineer R-6 and spec-compliance R7) should be treated as a single type-system extension decision rather than two independent recommendations, as spec-compliance's cross-review of schema-engineer (T-3) established. Both gaps — structured parameters typed as `string` and boolean flags typed as `string` — stem from the same root cause: FR-003's four-type vocabulary is too narrow. A spec amendment to FR-003 is the prerequisite. This revision raises the visibility of the type system gap and recommends a spec amendment as the next action, but does not prescribe the specific types.

### R8 — LOW: Add `description` to `ConstraintTemplate`
**Disposition**: MAINTAINED, priority elevated to MEDIUM

functional-architect's cross-review of spec-compliance (T-3) provides the stronger rationale: Constitution XVI (Mathematical Transparency) requires plain-language explanations for user-facing prompts in the guided construction pipeline. That pipeline (spec 014) will consume constraint templates and cannot present constraints to users without machine-readable descriptions. The current YAML header comments are not machine-readable. This is a functional gap for spec 014, not merely an aesthetic improvement.

The implementation must use `Optional[str] = None` rather than a required field, to avoid breaking existing constraint YAML files during the transition. Both reviews agree on this.

### R9 — LOW: Implement Minimal Template Registry
**Disposition**: MAINTAINED, scope elevated and clarified

The "minimal" framing understated this. functional-architect (T-3 in its cross-review of spec-compliance) correctly argues that a minimal test-enabler loader built now will need to be rewritten when spec 014 arrives if it does not anticipate the production use case. The loader should be designed as spec 014's entry point, not just a test scaffold.

Placement question from schema-engineer (T-5): the loader should follow the `game_forms.py` pattern and live in `objectives.py` (or alongside it in `schemas/`), not in a separate `registry.py`. The established pattern in the codebase is for schema modules to include their own loading utilities. If the filesystem dependency becomes a testing concern, it can be abstracted later.

game-theorist (T-5) correctly establishes the sequencing: (1) fix mathematical errors in templates, (2) build the loader/registry, (3) add new templates. The registry should not be built while templates are known to contain errors, as it will surface those errors with equal authority as correct templates.

### R10 — LOW: Add `computed_objective` Documentation Convention
**Disposition**: WITHDRAWN

This recommendation is superseded by R3's resolution. `computed_objective` is removed from example blocks entirely. There is no documentation convention to formalize. Documentation of what the objective evaluates to for a given parameterization belongs in the spec's Section 2 narrative or in the template's `description` field.

---

## New Recommendations

### NR-1: Fix `mode-mapping.yml` Red-Blue / Stackelberg Contradiction
**Priority**: HIGH

game-theorist (O1, R2) identified that `mode-mapping.yml` declares `red-blue: form: gnep` while all three red-blue templates correctly use `game_form: stackelberg`. This file is not referenced in the spec and was not in spec-compliance's original referenced documentation table — an omission the original review acknowledges now.

The contradiction matters because spec 014's guided construction pipeline will read `mode-mapping.yml` to assign a game form to red-blue deliberations. If that file says GNEP, spec 014 will construct structurally incorrect games for red-blue mode. Updating `mode-mapping.yml` to declare `stackelberg` for red-blue is a straightforward internal consistency fix that requires no spec amendment. It is also the fix with the highest downstream impact of any internal-consistency issue found across all reviews.

### NR-2: Amend Spec Section 2 to Correct `risk-adversarial` Form Expression
**Priority**: MEDIUM

game-theorist (O3, R3) and spec-compliance's cross-review of game-theorist (SA-3) together establish that the `risk-adversarial` template's declared form (`J_red = -confirmed_risks; J_blue = -mitigated`) omits the `false_positive_penalty` parameter that the template defines and that shapes the actual equilibrium. Both reviews agree the form is incomplete; they differ only on the intervention layer. The YAML's form field is correct per the spec's Section 2 formula — the incompleteness originates in the spec.

The correct fix is to amend spec Section 2's `risk-adversarial` entry to include the penalty term in the form expression, then update the YAML to match. The YAML should not be updated before the spec is amended, or spec-compliance would flag the result as a new FR-002 deviation.

### NR-3: Empty `mode_compatibility` Must Be Rejected by Validation
**Priority**: LOW

functional-architect (M5, R5) identified that nothing prevents `mode_compatibility: []` from passing `ObjectiveTemplate` validation, despite such a template being unreachable by any mode filter and violating the intent of SC-003. spec-compliance's cross-review of functional-architect (T-5) confirmed this is a spec gap that should be closed by explicit validator logic rather than relying on Constitution XII alone.

The fix is a one-line addition to the `mode_compatibility` validator: reject empty lists. This does not require a spec amendment because FR-008 already requires mode entries to be valid (implying at least one entry), but adding an explicit note to FR-008 about non-emptiness would make the requirement unambiguous.

---

## Position Summary

The cross-review process has produced three substantive shifts in the original spec-compliance position.

**CRITICAL classification of the import path is relinquished.** game-theorist, functional-architect, and the evidence from the cross-review round collectively establish that the import path mismatch, while a genuine FR-011 deviation requiring resolution, does not outrank mathematical correctness issues in operational severity. HIGH is the correct classification. The fix remains the same: amend FR-011 to match `conversus.schemas.objectives`.

**`computed_objective` in example blocks is removed, not formalized.** The original review left `computed_objective`'s fate open as an optional convention. The cross-review process — particularly schema-engineer's DC-1 and functional-architect's DC-3 — established that retaining it in any form creates an irreconcilable tension with example-key cross-validation (schema-engineer's R-4) and with spec 014's requirement to treat examples as machine-parseable parameterizations. Removal is the clean resolution.

**The mathematical correctness findings from game-theorist are acknowledged as within-scope.** The original review operated exclusively at the structural/compliance layer and did not assess whether form expressions were mathematically sound. game-theorist's DC-1, DC-2, and DC-3 correctly identify that schema validation and mathematical correctness are distinct verification axes, and that a structurally valid template can still encode the wrong optimization behavior. spec-compliance does not claim authority over mathematical correctness — that is game-theorist's domain — but acknowledges that the `mode-mapping.yml` contradiction (NR-1) and the `risk-adversarial` form incompleteness (NR-2) have compliance-layer consequences: downstream specs will consume these artifacts as correct, and when they do not behave as intended, the error traces back to artifacts that spec 013 was responsible for delivering in a consistent state.

The original review's core conclusions stand: the implementation meets FR-001 through FR-015 at the template-file and Pydantic-model layer, and the primary gaps are the absent test infrastructure, the import path mismatch, and the example format inconsistency. The revision adds precision on sequencing, elevates the constraint template description gap, and adds three new recommendations addressing issues that were outside the original review's evidence set.
