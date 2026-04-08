# Cross-Review: schema-engineer reviewing functional-architect

## Dangerous Contradictions

### DC-1. Shadowed mode parameter: bug or intentional fallback?

Functional-architect's R2 classifies the shadowed `mode` parameter in `select_candidate_templates` as P1 (correctness bug). I don't raise this at all. The contradiction: functional-architect argues that when `construct_objective` passes `mode="cooperative"` for a SELECTION problem, cooperative-compatible templates should be returned. But FR-018 defines a *fixed* decision-type-to-mode mapping: SELECTION always maps to winner-take-all. If the spec intends the mapping to be authoritative, the caller's mode *should* be ignored. The `mode` parameter exists as a fallback for custom/unknown decision types. Functional-architect's reading is valid if "mode" means "user override"; mine is valid if "mode" means "fallback for unmapped types." This needs spec clarification before either fix is correct.

### DC-2. File I/O in orchestrator: purity violation or appropriate?

Functional-architect's R7 (P2) proposes extracting `write_objective` from `construct_objective` to maintain function purity. I don't raise this. The contradiction: the CLAUDE.md says "service modules contain pure functions," but `construct_objective` is an *orchestrator*, not a service function. The extraction.py module has `write_features` as a separate function, which functional-architect correctly cites as precedent. However, this is a pattern preference, not a correctness issue. I'd classify it as P3 (code organization) not P2 (robustness), because the file write is guarded by `output_path is not None` and tests already exercise the pure path.

### DC-3. `str.replace` priority disagreement

Functional-architect classifies the string substitution fix as P2 (robustness). I classify it as P1 (correctness bug). Game-theorist also classifies it P1. The contradiction matters for implementation priority: if it's P2, it ships after source-map fixes and FR-003; if it's P1, it ships alongside them. The competitive-selection template has `w` as a parameter and the form contains `w` as a standalone token. The sort-by-length mitigation works for *current* templates, but any template edit that introduces a parameter name contained within another word creates silent corruption. I maintain P1: the code is one template away from wrong output, and the fix (regex word boundary) is trivial.

## Tensions

### T-1. Constraint wiring: P1 (functional-architect) vs not raised (schema-engineer)

Functional-architect's R4 classifies constraint wiring as P1, arguing FR-011 requires "selected constraints with parameters" in the output. I don't raise constraint wiring because `AssembledObjective` includes `constraints: list[str]` (constraint names), and the model validates successfully. The tension: are constraint *names* sufficient for FR-011, or must constraint *parameters and symbolic forms* be included? The spec says "selected constraints with parameters," which functional-architect reads as requiring full parameter data. I read the model's `constraints` field as satisfying the structural requirement, with parameter filling deferred. This is a spec-reading disagreement.

### T-2. Logging as P2 vs not raised

Functional-architect raises logging absence as P2 (R6). I don't mention logging because my scope is schema/type safety. Functional-architect correctly notes that `extraction.py` establishes the logging pattern. As a cross-reviewer, I agree this is a legitimate gap -- classification failures and retry loops need observability -- but P3 is more appropriate since the pipeline functions correctly without logging.

### T-3. Frozen dataclass mutable-contents concern

Functional-architect's off-base assumption #4 identifies that `GapList.gaps` is a mutable list inside a frozen dataclass. My review doesn't raise this because `frozen=True` on dataclasses is well-understood to only prevent attribute reassignment. Functional-architect's proposed fix (switch to `tuple`) would make the immutability genuine but requires changing all call sites that construct `GapList`. This is P3 -- a documentation/awareness item, not a correctness fix.

### T-4. Parameter extraction alias map

Functional-architect proposes an alias map on `ParameterDefinition` for better extraction recall. I don't raise this because it would change the schema. The tension: adding `aliases: list[str]` to `ParameterDefinition` is a schema change that affects template authors and the YAML format. It's a good idea but should be a separate spec amendment, not a drive-by addition.

## Safe Agreements

### SA-1. Source map must be returned from `fill_parameter_gaps`

Both reviews identify the same root cause and propose compatible fixes. Functional-architect proposes a `FilledParameters` dataclass; I propose a `FillResult` dataclass. Same pattern, different name.

### SA-2. FR-003 multi-template presentation is unimplemented

Both reviews confirm `candidates[0]` is silently chosen and propose a protocol-based solution. Functional-architect suggests reusing `GapFiller` or adding `TemplateSelector`; I suggest a `template_selector` callback parameter.

### SA-3. Pipeline architecture is well-designed

Both reviews affirm the three-stage separation, frozen intermediates, and protocol-based dependency injection. The implementation follows established codebase patterns closely.
