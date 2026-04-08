# Spec-Compliance Cross-Review of Functional-Architect's Review
## Spec: 013 — Objective Function Template Library

**Cross-Reviewer**: spec-compliance
**Reviewing**: functional-architect's review (`conversus-output/functional-architect/review.md`)
**Reference**: spec-compliance's own review (`conversus-output/spec-compliance/review.md`)
**Spec**: `specs/013-objective-function-templates/spec.md`
**Date**: 2026-03-23

---

## Dangerous Contradictions

### DC-1. functional-architect's R1 demands a loader function the spec explicitly excludes from scope

functional-architect's highest-priority recommendation (R1) calls for a `load_objective_templates()` function that discovers, bulk-loads, and validates the entire template library, with an embedded completeness check requiring "at least 20 templates, every mode has 3+ templates, 5+ cross-mode templates." This directly conflicts with the spec's scope boundary stated in Section 1: "What does not change: Template system. Execution engine." More concretely, FR-016 limits the deliverable to templates and Pydantic validation models with no additional dependencies beyond pydantic and pyyaml. A loader function is a runtime system component — it presupposes a deployment context, a resolved file path, and a runtime discovery mechanism. The spec makes no such commitment and deliberately defers collection-level operations to spec 014 (guided construction).

spec-compliance's review (Missed Opportunity 8: "No Programmatic Template Discovery or Registry") also notes this gap, but classifies it as LOW priority and frames it as making SC-003 testable, not as a spec requirement. functional-architect elevates this to HIGH without citing any spec clause that mandates it. Implementing R1 as specified — with inline completeness thresholds baked into the loader — would embed FR-012 through FR-015 validation logic in a runtime function rather than in tests or CI, conflating schema validation with operational discovery in a way the spec does not authorize.

**Why this is dangerous**: If an implementer follows functional-architect's R1 at face value, they will build infrastructure the spec does not require, tightly couple completeness invariants to a loader function that does not yet have a defined home, and potentially conflict with spec 014's authority over how the pipeline discovers templates at runtime.

---

### DC-2. functional-architect's R3 proposes a breaking schema change by adding parameter types the spec explicitly enumerates

FR-003 defines the exhaustive type vocabulary: `float`, `integer`, `string`, `function`. functional-architect's R3 (Priority: High) proposes extending this to include `vector`, `matrix`, `boolean`, and `enum`, and updating all existing YAML templates accordingly — explicitly acknowledging it is "a breaking change to the template schema."

spec-compliance's review (Off-Base Assumption 2: "Overloading type: string for Structured Data") identifies the same structural tension but recommends only adding an `array` or `list` type as a LOW priority consideration, explicitly framing it as a vocabulary extension to discuss rather than a breaking change to implement. functional-architect's framing goes further: it prescribes the specific types, adds a conditional `allowed_values` field to `ParameterDefinition`, and mandates that existing templates be retroactively reclassified. This would require amending FR-003 in the spec before implementation, which is outside the implementer's authority under a draft spec.

**Why this is dangerous**: Implementing R3 without a spec amendment means the implementation and spec diverge on a foundational schema contract — the same kind of drift that spec-compliance flagged as CRITICAL for the FR-011 import path mismatch. An implementer cannot selectively honor functional-architect's architectural judgment over the spec's explicit enumeration without a formal spec change. This is not a missed opportunity; it is a scope override.

---

### DC-3. functional-architect's O1 declares constraint references "architecturally insufficient" but the spec mandates exactly this design

functional-architect's Off-Base Assumption O1 argues that `constraints: ["budget", "non-negativity"]` as bare string references is not just incomplete but "an architectural assumption that contradicts the 'Templating Engines Over Inference' principle (Constitution VIII)." The recommendation implies that the schema layer must provide a deterministic resolution mechanism.

The spec is unambiguous: FR-002 defines `constraints` as "list of compatible constraint templates (references)" — the word "references" is intentional. FR-006 and FR-007 define constraint templates as separate files in a separate directory. The reference-by-name pattern is the spec's deliberate design choice for composability (each constraint template exists once; objective templates reference it by name). Resolution of those references at runtime is explicitly scoped to spec 014. functional-architect is applying a Constitution VIII critique to a design decision the spec already made.

spec-compliance's review does not contest the reference-by-name design at all. The only relevant observation (Missed Opportunity 9) concerns the absence of a loader for programmatic filtering, not the validity of string references.

**Why this is dangerous**: Treating O1 as an action item would require refactoring the fundamental relationship between ObjectiveTemplate and ConstraintTemplate — adding a resolution layer or `ComposedObjective` model (M1) that the spec neither requires nor anticipates. Any implementation following this path would be building against a spec that has not been revised.

---

### DC-4. functional-architect treats the `example` field inconsistency as a Constitution XI violation requiring standardization, while spec-compliance identifies it as a spec clarification issue

Both reviews agree the inconsistency exists: mode-specific templates use flat parameter-value examples; cross-mode templates include redundant structural keys (`name`, `form`, `game_form`) and a non-parameter `computed_objective` key. However, the two reviews reach different conclusions about what the inconsistency means and who has authority to resolve it.

functional-architect (M9, R7) frames this as a Constitution XI (Single Source of Truth) violation — a principled architectural error that should be corrected by standardizing all examples to the flat format. functional-architect also proposes adding a model_validator that enforces the flat format, making it a schema-level enforcement decision.

spec-compliance (Off-Base Assumption 3, Recommendation 3) frames this as a spec clarification issue: FR-002 says "minimal valid parameterization" but does not specify whether that means flat parameter values only or a broader example envelope. spec-compliance explicitly calls for a clarification or decision rather than unilateral standardization.

**Why this is dangerous at the boundary**: If functional-architect's validator is implemented before the spec is clarified, it would reject currently valid YAML files and break existing templates. spec-compliance's conservative framing — "remove redundant keys or the spec should clarify" — correctly sequences the decision (spec first, then implementation) rather than allowing the model_validator to impose the interpretation. Implementing functional-architect's R7 without the spec clarification encodes an assumption as enforcement.

---

## Tensions

### T-1. Priority inversion on the FR-011 import path mismatch

spec-compliance rates the import path deviation from FR-011 as CRITICAL — the highest severity in its framework — because FR-011 is an explicit, unambiguous requirement ("Models MUST be importable as `from conversus_schemas.objectives import ...`") and the implementation deviates from it with a different package path. spec-compliance's framing is: this is a spec-to-implementation gap that must be explicitly resolved, either by amending the spec or by adding a compatibility alias.

functional-architect does not mention the FR-011 import path at all. Its review focuses on model structure, composability, and type system design, but does not audit the public API surface against FR-011's literal text. This is a significant omission for a review focused on "type safety" and "stable interfaces" (Constitution Principle II, cited in R10 for exporting frozenset constants). The import path is the most visible interface the schema package exposes to downstream consumers (spec 014, plugin system) — more stable-interface-critical than whether `VALID_MODES` is exported from `__init__.py`.

The tension: spec-compliance found the highest-severity compliance gap; functional-architect missed it entirely while finding lower-severity architectural concerns. An implementer reading both reviews in isolation would not know that FR-011 is violated if they relied on functional-architect's review alone.

---

### T-2. The `click` dependency — legitimate constraint violation vs. reasonable exemption

spec-compliance (Off-Base Assumption 1, Recommendation 6) flags the `click>=8.3.1` dependency in `pyproject.toml` as a violation of the Section 5 constraint ("Must NOT depend on any library beyond pydantic and pyyaml") and recommends moving it to an optional dependency group as a MEDIUM priority fix. The spec's constraint is unambiguous: it applies to the `conversus-schemas` package as declared.

functional-architect does not mention the `click` dependency. Its review focuses on model design, not package configuration.

The tension is not between the two reviews but between spec-compliance's reading and what may be functional-architect's implicit assumption: that linter tooling is obviously out of scope for a "no extra dependencies" constraint. Both positions are defensible, but spec-compliance's is more conservative and more compliant with the spec's letter. This is a case where functional-architect's silence could mislead an implementer into treating the dependency as unproblematic.

---

### T-3. `ConstraintTemplate.description` — different motivations, same recommendation

Both reviews recommend adding a `description` field to `ConstraintTemplate`, but for different reasons that reveal a genuine prioritization disagreement.

functional-architect (M7, R6) derives the requirement from Constitution XVI (Mathematical Transparency) — the guided construction pipeline needs plain-language constraint explanations for user-facing prompts. It rates this MEDIUM priority.

spec-compliance (Missed Opportunity 7, Recommendation 8) derives it from consistency with ObjectiveTemplate and from FR-002's requirement pattern, noting that the asymmetry is defensible under a strict reading of FR-007 but creates forward-compatibility risk. It rates this LOW priority.

The tension: functional-architect's Constitution XVI argument is stronger as a design rationale, but spec-compliance is correct that FR-007 does not require `description`. functional-architect's priority elevation (MEDIUM vs. LOW) is justified by the spec 014 dependency it identifies, which spec-compliance did not consider. However, functional-architect's framing does not acknowledge that adding a required `description` field to `ConstraintTemplate` would break the existing constraint YAML files that lack it — a migration cost spec-compliance acknowledged with "optional `description: Optional[str] = None`" but functional-architect did not address.

---

### T-4. Test infrastructure: burden of proof vs. burden of creation

spec-compliance (Missed Opportunity 4, Recommendation 2: HIGH) identifies the absence of `tests/test_objectives.py` as a compliance gap because SC-001 through SC-003 are "currently unverifiable in CI." The recommendation is concrete: create a test file covering all success criteria.

functional-architect (R2: validate_library_integrity, Priority: High) proposes a different approach: a pure function `validate_library_integrity()` that takes the loaded template dicts and validates cross-references. This is more principled architecturally (pure function, composable, no I/O) but does not produce the test file SC-001 through SC-003 require. A `validate_library_integrity()` function with no test calling it leaves the success criteria as unverifiable as before.

The tension: both reviews agree tests are needed, but functional-architect proposes testable infrastructure while spec-compliance proposes tests directly. Neither review proposes both. An implementer needs both: a `validate_library_integrity()` function (functional-architect's R2) called from a `test_objectives.py` test file (spec-compliance's Recommendation 2). Treating these as alternatives rather than complements is a gap in both reviews.

---

### T-5. Empty `mode_compatibility` validation — missing from spec-compliance, overcorrected by functional-architect

functional-architect (M5, R5) recommends rejecting templates with `mode_compatibility: []` as "dead infrastructure" (Constitution XII). The recommendation is technically sound and consistent with the Constitution.

spec-compliance's review does not mention empty `mode_compatibility` at all. This is an omission: the spec requires that templates have valid mode entries (FR-008 cross-field invariant) and implies non-emptiness by requiring templates to be filterable by mode (SC-003). An empty list passes both the existing validator and spec-compliance's review without objection.

However, neither review asks whether the spec should explicitly add this as a validation requirement. Constitution XII ("no dead infrastructure") is functional-architect's frame; the spec's frame is "a template must apply to at least one mode." The spec could add this as an explicit requirement (FR-008 amendment), which would make the validation mandatory rather than a quality-of-life enhancement. spec-compliance should have caught this gap; functional-architect correctly identified it but without noting the spec amendment it implies.

---

## Safe Agreements

### SA-1. `string` as a type-theoretic junk drawer is a genuine design debt

Both reviews independently identify that `type: string` is overloaded to represent at least four structurally distinct data kinds — vectors (comma-separated), matrices (nested list notation), booleans, and enumerations — while the YAML examples for cross-mode templates use native YAML lists for these parameters. functional-architect (M2) calls this "dangerously loose" and documents the four distinct semantic roles. spec-compliance (Off-Base Assumption 2) identifies the same mismatch between declared type and example format.

Both reviews agree the current state is a debt, not a design choice. They diverge only on the remedy and urgency. This agreement provides sufficient grounds to flag the issue for the spec owner to decide whether to extend FR-003's type vocabulary before spec 014 consumes these templates, since spec 014 will need to generate type-appropriate gap-filling prompts and cannot do so reliably with `string`-typed parameters that are semantically lists or booleans.

---

### SA-2. Duplicate parameter name validation is an unambiguous gap both reviews missed or only one caught

functional-architect (M4, R4: Medium) is the only review to identify that nothing prevents two parameters with the same name within a single template, and provides a correct implementation. spec-compliance does not mention it. However, both reviews would agree on the fix if confronted with it: the model_validator pattern used in game_forms.py for other uniqueness checks extends cleanly to parameter name uniqueness, the cost of the fix is trivial, and the failure mode (silent shadowing) is exactly the kind of non-determinism both reviews are concerned about. This is a safe addition that does not conflict with any spec requirement and does not require a spec amendment.

---

### SA-3. YAML example inconsistency between mode-specific and cross-mode templates is real and must be resolved

Both reviews agree the `example` field inconsistency exists and that standardization is needed. functional-architect (M9) cites Constitution XI. spec-compliance (Off-Base Assumption 3) cites FR-002's "minimal valid parameterization" language. The reviews differ on sequencing (spec clarification first vs. immediate standardization) and on whether a model_validator should enforce the format, but both agree the status quo — where the model accepts two structurally incompatible example formats as equally valid — is incorrect.

The safe position: the spec owner should clarify FR-002's intent for the `example` field before a validator is added. The clarification cost is low (one sentence in the spec), the benefit is high (consistent machine-readable examples that spec 014 can consume programmatically), and both reviews support the outcome even if they differ on sequencing.

---

### SA-4. The `cooperative-fairness` template should be documented in the spec

Both reviews, read together, imply that the undocumented addition of `cooperative-fairness` requires a spec update. spec-compliance (Missed Opportunity 6, Recommendation 5: MEDIUM) explicitly calls for updating Section 2 of the spec to include the template. functional-architect (A4) notes that all four cooperative templates are "well-motivated" and implicitly endorses `cooperative-fairness` as consistent with GNEP game form selection. functional-architect does not flag it as undocumented, but its positive framing of cooperative templates as a group provides design confirmation for the addition.

The net position from both reviews: `cooperative-fairness` is a good template that belongs in the library, and the spec's Section 2 catalog should be updated to include it. This is a low-cost, low-risk spec maintenance item that brings the authoritative source of truth into alignment with the implementation.
