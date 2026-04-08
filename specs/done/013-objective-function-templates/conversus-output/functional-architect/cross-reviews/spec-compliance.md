# Cross-Review: functional-architect on spec-compliance's Review of 013

**Cross-Reviewer**: functional-architect
**Reviewing**: spec-compliance's review of 013-objective-function-templates
**Date**: 2026-03-23
**Source reviews**:
- spec-compliance: `conversus/specs/013-objective-function-templates/conversus-output/spec-compliance/review.md`
- functional-architect: `conversus/specs/013-objective-function-templates/conversus-output/functional-architect/review.md`

---

## Dangerous Contradictions

### DC-1. The import path deviation is misclassified as CRITICAL — it is spec noise

spec-compliance labels the FR-011 import path mismatch (`conversus.schemas.objectives` vs. `conversus_schemas.objectives`) as its single CRITICAL item and calls it a "direct deviation from the spec's letter." This framing is misleading in a way that could cause real harm: if the team acts on this, they will either rename the package unnecessarily or create a compatibility shim for a constraint that has no runtime significance. The functional-architect review does not mention this issue at all, and for good reason. The import path matters only if FR-011 is load-bearing as a public API contract — i.e., if external packages have already taken a dependency on `conversus_schemas`. At v1, with no released consumers, `conversus.schemas.objectives` is strictly superior (it groups schemas under the main package namespace). Treating a naming preference in an unreleased spec draft as CRITICAL blocks meaningful work on actual structural gaps. The correct classification is LOW or SPEC-AMENDMENT. Elevating it to CRITICAL over the type system's genuine deficiencies (which functional-architect classifies as High) inverts the priority order in a way that could misdirect implementation effort.

### DC-2. spec-compliance's "Off-Base Assumption" on click contradicts its own framing

spec-compliance raises the `click` dependency as an "Off-Base Assumption" violating Section 5's "Must NOT depend on any library beyond pydantic and pyyaml." It then immediately softens this by acknowledging `click` is used only by the linter CLI, not the schema package. The functional-architect review does not flag this at all. The contradiction is internal to spec-compliance's own review: if `click` is genuinely a Section 5 violation, it should appear in Actionable Recommendations at HIGH or CRITICAL priority, not buried under "Off-Base Assumptions." If it is not a real violation (because the spec clause refers to the schema module's imports, not the project's optional tooling dependencies), it should not be raised as a finding at all. The current treatment is neither fish nor fowl — it surfaces real concern but at the wrong severity and in the wrong section, which means a reader following spec-compliance's recommendations would deprioritize a potentially compliance-blocking issue. The functional-architect review's silence here is itself a gap: both reviews should have converged on a clear position. The contradiction between the reviews — one raising it, one ignoring it — leaves the team with no guidance on whether the `click` isolation work in recommendation #6 is urgent or optional.

### DC-3. spec-compliance endorses `dict[str, Any]` as adequate for `example`; functional-architect identifies it as a structural failure

spec-compliance's "Missed Opportunity #3" treats the inconsistent example format as an aesthetic problem (flat vs. nested keys) and recommends standardizing the format as HIGH. The functional-architect review (M6, R7) identifies the same inconsistency but correctly traces it to its architectural root: `example: dict[str, Any]` means the model cannot verify that example keys correspond to parameter names, that example values satisfy type constraints, or that required parameters (those without defaults) are covered. spec-compliance's recommendation to standardize format without adding a validating model_validator would produce cosmetically cleaner YAML that is still structurally unverified. Implementing spec-compliance's recommendation #3 alone — without functional-architect's R7 model_validator — would create a false sense of correctness: examples look right but are never checked. This is dangerous because the guided construction pipeline (spec 014) will treat example blocks as known-valid parameterizations and use them as seed inputs. A silently incorrect example poisons the pipeline.

### DC-4. spec-compliance treats constraint reference validation as out-of-scope; functional-architect identifies it as the central architectural gap

spec-compliance's only reference to constraint composition is Recommendation #8 ("add `load_all_templates()` function") framed as LOW priority to make SC-003 testable. It does not flag the absence of cross-reference validation — the fact that `constraints: ["nonexistent-constraint"]` passes ObjectiveTemplate validation — as any kind of defect. functional-architect's M1 and O1 treat this as the primary architectural risk: bare string references defer all resolution work to downstream consumers, contradict the "Templating Engines Over Inference" principle (Constitution VIII), and mean the schema layer cannot validate the library as a coherent whole. The severity gap is stark: spec-compliance rates this LOW; functional-architect rates it as the single most important structural finding. Acting on spec-compliance's rating would defer constraint resolution to spec 014 without providing any resolution mechanism, forcing spec 014 to implement what spec 013 should have provided.

---

## Tensions

### T-1. `cooperative-fairness` as spec drift vs. as valid extension

spec-compliance's Missed Opportunity #6 flags `cooperative-fairness` as "undocumented" and calls for either amending the spec's Section 2 catalog or marking the template as a bonus extension. The functional-architect review does not mention `cooperative-fairness` at all. This produces a genuine tension: spec-compliance is applying a strict letter-of-the-spec lens that treats any addition beyond the catalog as drift; functional-architect's silence implies this is either below the threshold of concern or is correctly handled by the implementation extending the spec's minimum. Both positions are defensible. The tension matters because it affects how the team treats future additions: if spec-compliance's position governs, every new template requires an explicit spec amendment before it can ship; if functional-architect's implicit position governs, templates can be added as long as they satisfy the structural requirements (FR-002, correct mode_compatibility, etc.). The team needs an explicit policy. The functional-architect review's silence is not endorsement — it is a gap that spec-compliance correctly surfaced.

### T-2. The type system gap: urgent structural defect vs. low-priority enhancement

Both reviews identify the `string` type overloading problem, but at incompatible severity levels. spec-compliance rates adding an `array` parameter type as LOW (Recommendation #7: "Consider Adding `array` Parameter Type"). functional-architect rates extending the type system as HIGH (R3), identifies four distinct semantic roles that `string` currently conflates (vector, matrix, boolean, enum), and argues this makes spec 014's gap-filling pipeline impossible to implement correctly without out-of-band knowledge. The disagreement is not about the existence of the problem — both reviews agree it exists — but about whether it must be fixed before spec 014 begins or can be deferred. This is a sequencing decision with real downstream cost: if the type system is extended during spec 014 rather than spec 013, every template YAML file will need to be updated at that point, and the spec 014 pipeline will have been designed around the weaker type model, potentially encoding the workaround into its architecture.

### T-3. Loader function scope: minimal test enabler vs. full library validator

Both reviews recommend a loader function (spec-compliance #9 "minimal `load_all_templates()`", functional-architect R1 `load_objective_templates()`), but at different scopes. spec-compliance frames it as a test enabler to make SC-003 testable and labels it LOW. functional-architect frames it as the authoritative entry point for the spec 014 pipeline, analogous to `load_mode_mapping()`, and labels it HIGH. The functional-architect review further calls for a separate `validate_library_integrity()` function (R2) that performs cross-reference and completeness checks — a function spec-compliance does not mention at all. The tension is between a minimal loader that unblocks tests and a complete loader that serves as the production entry point for downstream specs. A minimal loader implemented now may be insufficient when spec 014 arrives, requiring a rewrite rather than an extension.

### T-4. Description on ConstraintTemplate: optional improvement vs. Constitution XVI requirement

Both reviews recommend adding `description` to ConstraintTemplate (spec-compliance #8 LOW, functional-architect R6 MEDIUM). The reviews agree on the recommendation but disagree on the motivation. spec-compliance frames it as an aesthetic improvement ("improve self-documentation and consistency"). functional-architect grounds it in Constitution XVI (Mathematical Transparency) and the practical need for the guided construction pipeline to present plain-language constraint explanations to users. The motivation matters because it affects whether the team can defer this until spec 014 (if it is aesthetic) or must implement it in spec 013 (if it is a Constitution requirement). If the guided construction pipeline cannot explain constraints to users without a description field, the omission is a functional gap, not a cosmetic one.

### T-5. Range field typing: current behavior vs. semantic coherence

functional-architect's O2 identifies `range: Optional[dict[str, Any]]` as an "Off-Base Assumption" because it allows string-type parameters to carry numeric ranges (`range: {min: 0}` on a comma-separated string parameter), which is semantically incoherent. It recommends replacing the dict with a typed `ParameterRange` model (R8, LOW). spec-compliance does not flag this at all — the range field appears in its "MET" section without qualification. The tension is between spec-compliance's reading (the validator checks for `min`/`max` keys, so FR-010 is satisfied) and functional-architect's reading (the validator does not check whether range application is semantically meaningful for the parameter type, so FR-010 is satisfied in letter but not in spirit). If spec-compliance's reading governs, R8 is optional polish. If functional-architect's reading governs, the current range validator is creating a false sense of constraint enforcement on parameters where range has no meaning.

---

## Safe Agreements

### SA-1. Test infrastructure is the most urgent gap both reviews identify

Both reviews independently converge on the absence of test coverage as a high-priority problem. spec-compliance's Recommendation #2 calls for a `tests/test_objectives.py` covering SC-001 (YAML loads and validates), SC-002 (invalid mode raises ValidationError), SC-003 (mode filtering), and SC-005 (every template has a non-empty example). functional-architect's review identifies the same gaps implicitly through its recommendations for `load_objective_templates()` and `validate_library_integrity()`, which make these success criteria mechanically verifiable. Both reviews agree the current state — where SC-001 through SC-005 are asserted to pass but are not tested in CI — is the most immediately actionable gap. This agreement is trustworthy: it does not depend on resolving any of the tensions above, and the work is well-bounded.

### SA-2. Example field inconsistency is a real problem, and the flat format is the correct standard

Both reviews flag the inconsistency between flat examples (mode-specific templates) and nested examples that re-declare `name`, `form`, and `game_form` inside the example block (cross-mode templates). Both reviews agree the flat parameter-values-only format is correct, citing the spec's "minimal valid parameterization" language (FR-002). spec-compliance and functional-architect differ on whether validation should be added (only functional-architect recommends the model_validator), but both agree the nested format violates the Single Source of Truth principle (Constitution XI). Standardizing to the flat format is safe to implement immediately without resolving any of the other tensions.

### SA-3. `description` field should be added to ConstraintTemplate

Both reviews independently recommend adding a `description` field to ConstraintTemplate. The implementation currently has no description field on `ConstraintTemplate` (confirmed in the source at line 105-108), and constraint YAML files use YAML comments rather than a machine-readable field. Both reviews agree this is a gap. The action is straightforward: add `description: str` to `ConstraintTemplate` in objectives.py and promote the existing YAML header comments to YAML fields in each of the six constraint files. Neither review contests this. The only disagreement is on priority (spec-compliance: LOW, functional-architect: MEDIUM), but both rate it implementable without architectural decisions.

### SA-4. No loader function is a shared structural gap that will block spec 014

Both reviews identify the absence of a `load_all_templates()` style function as a gap, and both connect it to the need to make the template library queryable (for SC-003 mode filtering and for spec 014's guided construction pipeline). The reviews differ on scope and priority, but they share the underlying finding: the Pydantic models validate individual files but do not provide any mechanism to treat the library as a collection. This agreement is reliable because it is grounded in the observable state of the code — `objectives.py` has no loader, no path resolution helper, and no registry — and in the concrete requirement that spec 014 will need to select templates by mode.
