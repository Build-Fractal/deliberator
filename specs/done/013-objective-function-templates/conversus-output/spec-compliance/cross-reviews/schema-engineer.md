# Spec-Compliance Cross-Review of Schema-Engineer's Review
# Spec: 013-objective-function-templates

**Cross-Reviewer Role**: spec-compliance
**Reviewing**: schema-engineer's review (`conversus-output/schema-engineer/review.md`)
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1: Example Standardization Prescription Conflicts With Spec's Own Ambiguity

Schema-engineer's R-3 prescribes that the flat format is authoritative and that all seven cross-mode templates should have their `name`, `form`, `game_form`, and `computed_objective` keys stripped from their `example` blocks. Spec-compliance's Off-Base Assumption 3 identifies the same inconsistency but stops short of prescribing the flat format as canonical.

The danger is in what schema-engineer then adds in R-4: a model validator that rejects example keys not present in the `parameters` list. If R-3 and R-4 are both implemented together, any `computed_objective` key retained for documentation purposes would cause a `ValidationError`. However, schema-engineer's own M-3 notes that "`computed_objective`... belongs in a separate field (e.g., `example_note`) rather than mixed into the parameterization dict" — a structural change that FR-002 does not authorize. FR-002 defines `example` as "minimal valid parameterization" but does not define what keys are forbidden inside it.

Spec-compliance's Recommendation 3 is more conservative: remove the structurally redundant keys (`name`, `form`, `game_form`) but leave `computed_objective` disposition open. Schema-engineer's R-3+R-4 combination would break any template that keeps `computed_objective` as a documentation aid, even though the spec never prohibits it. The combined prescription goes meaningfully beyond what the spec requires, and if enacted naively it could silently invalidate templates that are spec-compliant by FR-002's actual text.

**Resolution needed**: The two reviews must agree on whether `computed_objective` is forbidden, ignored, or migrated to a new field before R-3 and R-4 are implemented together.

### DC-2: `click` Dependency Conflict is Real, But Schema-Engineer's Review Ignores It

Spec-compliance's Off-Base Assumption 1 identifies that the `click>=8.3.1` project-level dependency violates Section 5's explicit constraint: "Must NOT depend on any library beyond pydantic and pyyaml." Schema-engineer's review does not mention this at all — neither as an alignment, a missed opportunity, nor an off-base assumption.

The omission is not merely a coverage gap; it is a dangerous silence. Schema-engineer's M-9 recommends adding a `load_objective_template()` utility function to `objectives.py`, and R-7 proposes a `load_all_objective_templates()` function. If a future implementer follows schema-engineer's review in isolation, they will see no dependency constraint and may freely add further dependencies for convenience (e.g., `pathlib`, `importlib.resources` relative paths). Spec-compliance's Recommendation 6 addresses the `click` issue by moving it to an optional dependency group.

The contradiction: schema-engineer actively recommends expanding the module's surface area (loader utilities, registry patterns) without flagging that the implementation is already over the dependency constraint that governs the entire package. A reader following only schema-engineer's review would have no reason to apply any discipline to new dependencies.

**Resolution needed**: Schema-engineer's R-7 and any related utility recommendations must be conditioned on first resolving the Section 5 `click` violation. The utility functions themselves are pydantic/pyyaml-safe, but the pattern of silently accepting the existing violation invites further drift.

### DC-3: FR-011 Import Path — Both Reviews Agree on the Problem, But Prescribe Incompatible Fixes

Both reviews correctly identify that FR-011's prescribed import path (`from conversus_schemas.objectives import ...`) does not match the actual implementation (`from conversus.schemas.objectives import ...`). The contradiction is in the proposed resolutions.

Schema-engineer's R-8 presents two options but expresses a soft preference for option (b) — amend FR-011 to match the actual path — citing lower risk since the `conversus.schemas` namespace was established in spec 012.

Spec-compliance's Recommendation 1 also presents two options but expresses a clear preference for option (a) — amend FR-011 to match the actual path — and additionally suggests a `conversus_schemas` compatibility alias as option (b).

These are not identical: schema-engineer's option (b) (amend the spec) and spec-compliance's option (a) (also amend the spec) are the same recommendation, but schema-engineer's option (a) (rename the package) is a higher-risk change that spec-compliance's Recommendation 1 does not list. More importantly, spec-compliance does not propose a compatibility alias as a standalone option — it frames the alias as an alternative to spec amendment, whereas schema-engineer frames package rename as an alternative to spec amendment. The two reviews present different option sets, and if a stakeholder reads them as a unified set of options, they may believe a compatibility alias and a package rename are both on the table when only one is.

**Resolution needed**: The two reviews should converge on a single ordered recommendation. Both favor amending FR-011 as the lowest-risk path. The compatibility alias (spec-compliance's option b) and the package rename (schema-engineer's option a) should be explicitly ranked against each other, with only one carried forward.

### DC-4: Schema-Engineer's R-4 Example-Key Validation Would Break SC-005 for Constraint Templates

Schema-engineer's R-4 adds a cross-validator that rejects example keys not found in `parameters`. Spec-compliance's Recommendation 4 recommends adding `example` fields to all six constraint YAML files and a corresponding optional `example` field to `ConstraintTemplate`. Schema-engineer's O-3 and M-6 acknowledge the `description` and `example` asymmetry for constraint templates but do not recommend adding `example` to `ConstraintTemplate`.

If R-4 is applied to `ObjectiveTemplate` and constraint templates are simultaneously extended with `example` fields (per spec-compliance's Recommendation 4), then `ConstraintTemplate` would need an equivalent cross-validator. Schema-engineer's review, by omitting `example` from `ConstraintTemplate`, leaves this validator gap silent. A constraint template with an `example` block that contains a typo key would silently pass. The asymmetry in rigor between the two model types is a structural inconsistency the spec does not authorize.

---

## Tensions

### T-1: RangeSpec Model — Principled but Potentially Over-Engineered for v1

Schema-engineer's R-5 proposes replacing `range: Optional[dict[str, Any]]` with a typed `RangeSpec(min: Optional[float], max: Optional[float])` model with `extra="forbid"`. This is technically sound for catching typos like `maxx: 10`. Spec-compliance does not raise this issue at all.

The tension is that FR-010 only requires "range validation (min <= default <= max when all three are present)." The existing implementation satisfies FR-010. The `RangeSpec` model is an enhancement beyond spec requirements. Spec-compliance's mandate is to assess spec conformance, not to prescribe enhancements — its silence here is accurate. Schema-engineer's mandate to assess structural quality makes R-5 legitimate. However, schema-engineer's R-5 also assigns this "Medium" priority, which may overweight a non-spec-required change relative to genuine spec deviations. Given that FR-003 leaves `range` structure deliberately open (only bounding `min`/`max`/`default` interactions), a `RangeSpec` model that adds `extra="forbid"` could constrain future range semantics (e.g., adding `step` for integer parameters) that the spec does not prohibit.

### T-2: `cooperative-fairness` — Spec Section 2 Drift vs. FR-012 Compliance

Spec-compliance's Missed Opportunity 6 flags `cooperative-fairness` as an undocumented addition not listed in spec Section 2, noting the need to either update the spec or mark the template as an extension. Schema-engineer's A-6 treats it as a non-issue because FR-012/FR-013 set floor counts ("at least"), not ceiling counts, and the template counts still pass.

This is a genuine interpretive tension. Schema-engineer reads Section 2 as an illustrative catalog, not a normative enumeration. Spec-compliance reads Section 2 as a normative catalog with "at least" applying only to the count thresholds in FR-012/FR-013, not to the set of templates. The spec's Section 2 language does not resolve this: it uses imperative naming ("cooperative-integration:", "cooperative-quality:") without the hedging language "for example" or "including but not limited to."

The practical risk of schema-engineer's position: if Section 2 is merely illustrative, then any template can be added without spec review. The practical risk of spec-compliance's position: it treats Section 2 as over-specified, burdening spec amendments for every reasonable addition. Given that the spec is in Draft status, spec-compliance's call to explicitly update Section 2 is the more disciplined path — it closes the ambiguity rather than allowing it to persist into future reviews.

### T-3: Boolean Type Addition — Scope Creep vs. Semantic Precision

Schema-engineer's R-6 recommends adding `boolean` to the parameter type system and converting the `normalize` parameters in weighted-sum and minimax templates. This is assigned "Low" priority. Spec-compliance's Recommendation 7 proposes a different response to the same underlying observation: adding an `array` type to handle structured data like matrices and weight vectors. Both are type-system extensions not required by FR-003.

The tension: these are not compatible extensions — they address different parts of the type-inadequacy problem. Schema-engineer focuses on semantic precision for boolean flags. Spec-compliance focuses on the type mismatch between `type: string` declarations and native YAML list usage in examples. Both reviews identify the four-type vocabulary as insufficient, but they propose independent additions that, if both implemented, would result in a six-type system with no spec authorization for either addition. The correct path is to treat this as a single type-system extension decision rather than two independent recommendations.

### T-4: `extra="forbid"` — Schema-Engineer's R-10 vs. Spec-Compliance's Silence

Schema-engineer's R-10 recommends adding `model_config = ConfigDict(extra="forbid")` to all three Pydantic models. This would reject any YAML key not explicitly defined in the model — including `computed_objective` in example blocks if R-3 is not fully executed, and any future metadata fields added to templates before the model is updated. Spec-compliance does not raise this recommendation.

The tension is that `extra="forbid"` is a stronger guarantee than any spec requirement, and it interacts with the example format inconsistency (DC-1) and the `ConstraintTemplate` extension gap (DC-4). If applied prematurely — before example formats are standardized and constraint template extensions are decided — it would cause validation failures on currently valid (spec-compliant) templates. Schema-engineer's review does not sequence R-10 relative to R-3, M-6, and O-3, which is a dependency the implementation plan must resolve.

### T-5: Load Utilities — Schema-Engineer's M-9/R-7 vs. Spec-Compliance's Recommendation 9

Both reviews recommend adding template loading/registry utilities. Schema-engineer's R-7 focuses on `load_objective_template()` and `load_all_objective_templates()` mirroring the `load_mode_mapping()` pattern. Spec-compliance's Recommendation 9 proposes a `load_all_templates(directory: Path)` function with filtering by mode, primarily to make SC-003 directly testable.

The difference is scope: schema-engineer proposes a file-by-file loader and a batch loader; spec-compliance proposes a batch loader with query semantics. These are additive rather than contradictory, but assigning them separately risks duplicate implementation effort. The two reviews should converge on a single loader API design. Spec-compliance's filtering requirement (mode-based) is more directly tied to an SC, making it the higher-priority design constraint.

---

## Safe Agreements

### SA-1: FR-011 Import Path Is the Highest-Priority Deviation and Must Be Resolved

Both reviews independently flag the `conversus_schemas` vs. `conversus.schemas` import path mismatch as a critical or high-priority item (schema-engineer: R-8, Priority High; spec-compliance: Recommendation 1, CRITICAL). Both favor amending the spec over restructuring the package. This is the clearest consensus point across both reviews and should be the first issue resolved.

### SA-2: Test Coverage for SC-001, SC-002, SC-003 Is Absent and Required

Schema-engineer does not explicitly call out the missing test file (the review operates at the schema/model layer), but spec-compliance's Missed Opportunities 4 and 5 are unambiguous: there is no `tests/test_objectives.py`, and the three most concrete success criteria are untested. This gap is not in tension with anything in schema-engineer's review. The two reviews are in implicit agreement that schema-level correctness (schema-engineer's domain) and spec-level success criteria (spec-compliance's domain) both require automated test coverage to be verified. Spec-compliance's Recommendation 2 provides the most specific action plan.

### SA-3: Example Format Inconsistency Harms Downstream Consumers and Must Be Standardized

Both reviews agree that the `example` field format is inconsistent across templates — schema-engineer in M-3 and R-3, spec-compliance in Missed Opportunity 3 and Recommendation 3. Both identify the flat key-value format used by mode-specific templates as the correct baseline. The disagreement (see DC-1) is about what to do with `computed_objective`, not about whether standardization is required. On the core principle — that seven of 21 templates use a structurally different example format that undermines machine-parsability — both reviews are aligned.

### SA-4: Duplicate Parameter Name Detection and Range Validation Are Uncontested Improvements

Schema-engineer's M-1/R-1 (duplicate parameter name detection) and M-5/R-5 (RangeSpec model) address gaps that spec-compliance does not contradict. These are model-quality improvements within the spirit of FR-008 and FR-010. Spec-compliance's review does not flag them as concerns, and they do not interact with any of the dangerous contradictions above. The duplicate parameter name check in particular addresses a real data-integrity risk (the `lambda` parameter in `cooperative-integration` is a Python reserved word and a copy-paste target) with no downside. Both improvements are safe to implement without cross-review reconciliation.
