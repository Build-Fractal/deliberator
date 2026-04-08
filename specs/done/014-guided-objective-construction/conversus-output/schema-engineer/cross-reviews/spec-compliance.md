# Cross-Review: schema-engineer reviewing spec-compliance

## Dangerous Contradictions

### DC-1. FR-003 as P1: spec letter vs implementation risk

Spec-compliance classifies FR-003 (multi-template user selection) as P1 because the spec uses MUST. I classify it as P2. The contradiction: spec-compliance reads the RFC 2119 MUST literally -- if the spec says MUST and the implementation doesn't, it's a P1 violation. My reading: P1 should be reserved for issues that produce *incorrect output*. Missing FR-003 means the user doesn't get to choose between templates, but the pipeline still produces a valid, correct objective for the auto-selected template. This is a feature gap, not a correctness bug. The distinction matters for triage: should FR-003 block a release, or can it ship as a known limitation?

### DC-2. LLMGapFiller and gap_fill_model as P1s

Spec-compliance's R4 (LLMGapFiller) and R5 (gap_fill_model config) are both P1. I don't raise either. The contradiction: implementing an LLMGapFiller requires choosing a model provider, which introduces a runtime dependency into `conversus-schemas` -- the package that FR-016 says must have "no extra dependencies beyond pydantic/pyyaml." An LLMGapFiller stub that satisfies the protocol but doesn't actually call an LLM is useless. A real implementation needs an LLM client library, which violates FR-016. Spec-compliance's P1 classification creates a conflict between FR-022 (must have LLMGapFiller) and FR-016 (no extra dependencies). This tension is in the *spec*, not the implementation.

### DC-3. SC-002 as NOT MET: is this the implementation's fault?

Spec-compliance marks SC-002 (natural-language-to-weight mapping: "speed is twice as important") as NOT MET. I don't assess success criteria. The contradiction: SC-002 requires NLP or LLM interpretation of relative importance statements. This is inherently a Stage 2 concern that depends on the GapFiller implementation. The construction pipeline passes the problem text to the filler -- whether the filler can interpret "twice as important" is the filler's capability, not the pipeline's. Marking SC-002 as NOT MET on the pipeline is arguably misplaced; it should be assessed against the GapFiller implementations.

## Tensions

### T-1. FR-014 `conversus.yml` integration

Spec-compliance classifies FR-014 as P1 (R3). I don't raise it. Spec-compliance argues this "breaks the downstream plugin consumption chain." The tension: the construction pipeline's job is to produce `objective.yml`. Writing to `conversus.yml` is an integration concern that couples the pipeline to the project configuration system. If `conversus.yml` doesn't exist yet, the pipeline would need to create it, which is outside its scope. FR-014 might belong in a higher-level orchestrator or CLI command, not in `construct_objective`.

### T-2. FR-020 source structure interpretation

Spec-compliance and I both flag the flat `source` dict as missing `problem_md`. We agree on the diagnosis. The tension is in the fix: spec-compliance proposes adding it to the existing `source` dict structure, I propose a `SourceProvenance` Pydantic model. Both achieve the same result. Spec-compliance's approach is simpler (add a key); mine is more type-safe (model validation). Given the project's Pydantic-first approach, the model is more consistent.

### T-3. FR-005 contextualised questions scope

Spec-compliance marks FR-005 as PARTIALLY MET because questions aren't contextualised. I don't assess FR-005. The tension: question contextualisation is a feature of the GapFiller implementation (specifically LLMGapFiller), not the pipeline itself. The pipeline passes `problem_context` to the filler -- contextualising the question is the filler's job. Spec-compliance's reading puts the burden on the pipeline; I'd put it on the filler. This affects whether the fix belongs in `fill_parameter_gaps` or in the GapFiller implementations.

### T-4. Explicit importability test necessity

Spec-compliance raises the lack of an explicit importability test for FR-015/SC-005. I don't raise it. The test file says "Tested indirectly." Spec-compliance wants an explicit test mirroring `test_game_forms.py`. The tension: the import chain is trivial (stdlib + pydantic + yaml), and any import error would be caught by *every other test* that imports the module. An explicit test adds no coverage -- it's a documentation gesture. P3 at most.

## Safe Agreements

### SA-1. FR-020 source dict is missing `problem_md`

Both reviews identify the flat `dict[str, str]` as structurally incomplete. Spec-compliance frames it as spec non-compliance; I frame it as a missed schema field. Same fix needed.

### SA-2. FR-019 explicit type + keyword fallback is correctly implemented

Both reviews confirm `classify_decision_type` handles explicit type first, keyword second. Tests cover both paths.

### SA-3. FR-021 deferred parameters work correctly

Both reviews confirm function-type parameters with `derived_from` are properly identified and deferred. Implementation matches spec.

### SA-4. FR-012 determinism is achieved

Both reviews confirm no randomness, deterministic ordering, and the determinism test passes.
