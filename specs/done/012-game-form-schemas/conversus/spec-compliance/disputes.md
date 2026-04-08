# Spec Compliance — Final Disputes & Position

**Reviewer role**: spec-compliance
**Phase**: Final (post-revision deliberation)
**Date**: 2026-03-22

---

## Remaining Disputes

### Dispute 1: The FR-003 type-set expansion is a spec amendment, not an implementation fix — and the implementation must not change until FR-003 is amended.

game-theorist and schema-engineer both treat the YAML-Pydantic type divergence as an implementation bug to be fixed directly. I agree on the direction (expand the type set, not simplify the Pydantic models), and I agree the fix is urgent (P1). But the procedural point remains load-bearing: FR-003 explicitly enumerates a **closed** type set. Adding `map[string, string]`, `map[string, list[string]]`, or splitting `constraint_list` into `constraint_list` / `constraint_map` changes the text of FR-003 itself. This is not pedantry — it is the difference between "the implementation diverges from the spec" (a compliance finding) and "the spec is wrong" (an amendment request). If we fix the YAML declarations without first amending FR-003, we create an implementation that is correct but non-compliant. The spec must be amended first, and the compliance audit should track it as an FR-003 amendment, not as a code fix.

schema-engineer's atomic remediation (expand `VALID_FIELD_TYPES`, update YAML declarations, add enforcement test) is the right implementation plan. I endorse it. But I dispute the framing that treats it as self-contained. The deliverable sequence is: (1) FR-003 spec amendment adding map types and splitting constraint types, (2) code changes per the atomic remediation plan, (3) compliance re-verification. Steps 2-3 without step 1 produce a codebase that contradicts its own spec.

### Dispute 2: `Literal` type enforcement on `form` fields is P1, but the justification must be FR-007 interpretation, not downstream union needs.

All three agents now agree on `Literal` types. The dispute is about justification. schema-engineer frames it as infrastructure for the discriminated union (Rec 2). game-theorist frames it as prerequisite for solution-concept dispatch. Both framings reference downstream specs, not spec 012.

My position: `Literal` types are P1 because FR-007 says "enforce type constraints" and `form: str = "normal-form"` with no constraint is not enforcement — it is a default. This is a spec 012 compliance argument that stands on its own. The downstream benefits (union, dispatch) are real but they are not the reason for P1 priority within this spec's scope. This matters because if someone later argues that spec 012 does not need the union after all, the `Literal` fix should not be deprioritized — it is independently required by FR-007. Tying its priority to downstream specs creates a false dependency.

### Dispute 3: The `constraint_list` / `constraint_map` split must come with explicit YAML `description` updates, not just type label changes.

schema-engineer's New-1 and my Rec 6 agree on the split. game-theorist's DC-2 adds the mathematical documentation requirement (local constraints are per-player scoped, coupled constraints are shared). But no agent has explicitly flagged that the current YAML descriptions **already document the correct semantics** — the `gnep.yml` description for `local_constraints` says "A mapping from player name to a list of constraint expressions" and for `coupled_constraints` says "A list of constraint expressions." The problem is that the `type` field contradicts the `description` field: both say `constraint_list` despite describing structurally different things.

When the type labels are split, the descriptions must be reviewed for consistency with the new type vocabulary. Specifically: if `constraint_map` becomes the type for `local_constraints`, the description should explicitly state "type `constraint_map` represents `dict[str, list[str]]`" or the type vocabulary should be documented in a preamble. Otherwise we replace one inconsistency (wrong type label) with a different one (correct type label with no definition). This is a small but non-trivial documentation task that neither agent's remediation plan accounts for.

---

## Convergence

### Convergence 1: Unidirectional type-set fix — expand FR-003, do not simplify Pydantic.

All three agents agree without reservation. game-theorist provided the mathematical argument (simplifying Pydantic would destroy asymmetric game support). schema-engineer provided the engineering argument (the Pydantic types are the correct modeling choices). I provided the compliance argument (the Pydantic models implement FR-006 and FR-007 correctly; it is FR-003's enumeration that is incomplete). The direction is settled: the type set must grow to accommodate the models, not the reverse.

### Convergence 2: `ParametricGame` validation deduplication via mixin, not inheritance.

All three agents converge on this after game-theorist raised the mathematical objection to `isinstance` contracts and I raised the Pydantic MRO concern. The agreed approach: extract shared player-objective and player-decision-variable validation into a `_GNEPStructureValidator` mixin or private base class. Both `GNEPGame` and `ParametricGame` use the mixin. The `form` Literal discriminator handles dispatch; `isinstance` is explicitly not the polymorphism mechanism. This satisfies the spec's "inherits all GNEP fields" language (which describes field composition, not Python class hierarchy) while eliminating the 28-line verbatim duplication (lines 137-163 vs. 186-215) that creates validation drift risk.

### Convergence 3: Package data resolution (`_schema_dir()`) is broken for installed packages and must be fixed.

Universal P1 agreement. The `Path(__file__).resolve().parent.parent.parent` walk will fail in any pip-installed deployment. The agreed fix: `importlib.resources` with `[tool.setuptools.package-data]` configuration. schema-engineer's note that relocating YAML files into the package would require an FR-001 amendment is accepted — the `importlib.resources` approach with `package-data` configuration avoids that conflict by keeping files at the spec-mandated location while ensuring they are included in the distribution.

### Convergence 4: Package name mismatch (`conversus` vs. `conversus-schemas`) requires project-level resolution.

All agents agree this is P1 and blocks downstream consumers. The mismatch is between FR-010 (which says `conversus-schemas`) and `pyproject.toml` (which says `conversus`). The resolution direction — whether to rename the package or amend FR-010 — depends on the project's architectural intent (is `conversus` the umbrella name for a larger project?). This is a project-owner decision, not a reviewer decision. The compliance finding stands: the current state violates FR-010 as written.

### Convergence 5: Discriminated union is deferred to spec 013 or a spec 012 amendment.

schema-engineer downgraded from P1 to P2. game-theorist added a sequencing constraint (union should not precede optimization-sense addition). I identified that no FR or SC in spec 012 requires it. All three agents agree: the union is the right eventual design but does not belong in the initial spec 012 implementation. It should be introduced when a downstream spec (013 or 016) needs it, or via a spec 012 amendment that coordinates it with objective-type expansion.

---

## Final Position Statement

### Non-Negotiables

1. **FR-003 must be formally amended before YAML type declarations are changed.** The closed type set is an explicit spec requirement. Changing the YAML to use types not in FR-003 without amending FR-003 creates a compliant-looking codebase that actually contradicts its own spec. The amendment and the implementation fix must be sequenced, not conflated.

2. **`VALID_FIELD_TYPES` must be wired into enforcement as part of the type-set fix.** schema-engineer's argument is correct: an unenforced constant is worse than no constant, because it creates a false impression of validation. The FR-003 remediation must be atomic: amend the spec, expand the constant, update the YAML declarations, and add a test that asserts all YAML `type` values are members of `VALID_FIELD_TYPES`. Partial fixes are rejected.

3. **`_schema_dir()` must be fixed for installed-package resolution before any downstream spec consumes these schemas.** FR-011 is currently not implementable as deployed. This is a functional blocker, not a quality improvement.

4. **The package name discrepancy (FR-010) must be resolved with the project owner.** The compliance auditor cannot resolve architectural naming decisions, but can and does assert that shipping with a name that contradicts the spec is a P1 violation.

5. **`Literal` types on `form` fields are required by FR-007 independent of any downstream union needs.** The justification is intrinsic to spec 012. If the discriminated union is never built, the `Literal` constraint is still required. This non-negotiable is about the justification chain, not the recommendation itself.

### Flexibility

1. **Priority ordering among P1 items is negotiable.** I have five P1 findings. The implementation sequence among them is an engineering decision. I would suggest: (a) `Literal` types first (smallest change, unblocks testing), (b) FR-003 amendment + type-set remediation (largest impact, most interdependencies), (c) package data fix, (d) ParametricGame mixin extraction, (e) package name resolution. But I will not insist on this ordering.

2. **The specific type vocabulary for the FR-003 amendment is negotiable.** Whether we use `map[string, string]` and `map[string, list[string]]`, or `dict[string, string]` and `dict[string, list[string]]`, or some other syntax, is a design decision for the spec author. The compliance requirement is that the types used in YAML declarations must be members of FR-003's set — the specific labels are a convention choice.

3. **SC-001 test granularity is flexible (P2 or P3).** My original Rec 7 noted that SC-001 says "the example validates against the Pydantic model" but the test goes beyond this by asserting specific field values. The test is correct and arguably better than a minimal SC-001 interpretation. I am flexible on whether to add a comment clarifying this or to treat it as a non-issue. P3 is acceptable.

4. **game-theorist's mathematical enrichments (optimization sense, mixed-strategy indicator, variable bounds) are reasonable future work.** I do not contest the mathematical arguments. I contest only the scope: they are spec amendments for spec 012a or prerequisites for specs 017-019, not compliance findings against the current spec. I am flexible on whether they are tracked as spec amendments now or deferred to the downstream specs that need them, as long as they are not conflated with compliance against the existing FRs.

5. **The Stackelberg leader-not-in-followers validator and non-empty-leader-variables check are welcome additions at P2-P3.** These are defensive validators that do not conflict with any FR. They improve correctness without requiring spec amendments. I have no objection to including them in any implementation PR alongside the required fixes.
