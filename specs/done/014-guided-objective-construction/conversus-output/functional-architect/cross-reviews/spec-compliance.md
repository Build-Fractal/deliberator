# Cross-Review: functional-architect reviewing spec-compliance

## Dangerous Contradictions

### DC-1. FR-003 and LLMGapFiller as P1s: blocking compliance vs shipping incrementally

Spec-compliance classifies five items as P1: FR-003 (R1), FR-020 source (R2), FR-014 conversus.yml (R3), LLMGapFiller (R4), and gap_fill_model config (R5). This is a heavy P1 list that would block any release. I classify FR-003 as P1 but not LLMGapFiller or gap_fill_model. The contradiction: implementing LLMGapFiller (R4) requires an LLM client dependency, which conflicts with FR-016 (no extra dependencies beyond pydantic/pyyaml). Spec-compliance doesn't address this conflict. You cannot satisfy both FR-022 (LLMGapFiller) and FR-016 (no extra deps) simultaneously unless the LLMGapFiller accepts the LLM client as an injected dependency. Even then, the class needs *some* interface to depend on. This is a spec conflict, not an implementation oversight.

### DC-2. FR-014 `conversus.yml` integration scope

Spec-compliance's R3 proposes that `construct_objective` should read/create/update `conversus.yml`. I disagree with placing this responsibility in the construction pipeline. The pipeline's job is to produce a valid `AssembledObjective` and optionally serialize it. Modifying `conversus.yml` is an orchestration concern that belongs in the CLI layer or a higher-level integration function. The construction pipeline should not need to know about `conversus.yml`'s schema. Spec-compliance reads FR-014 as a pipeline requirement; I read it as a system-level requirement that the pipeline enables but doesn't implement directly.

### DC-3. SC-002 as NOT MET: misattribution to the construction pipeline

Spec-compliance marks SC-002 ("speed is twice as important" mapped to weights) as NOT MET. I don't assess SC-002 because it's a GapFiller capability, not a pipeline feature. The contradiction: spec-compliance evaluates SC-002 against the construction pipeline code, but the scenario requires a GapFiller that can interpret natural language. The pipeline passes the problem text and gap questions to the filler -- interpretation is the filler's job. Marking SC-002 as NOT MET on `construction.py` is misplaced; it should be assessed against the GapFiller implementations (specifically the not-yet-implemented LLMGapFiller).

## Tensions

### T-1. FR-005 contextualised questions: pipeline vs filler responsibility

Spec-compliance marks FR-005 as PARTIALLY MET because questions aren't contextualised beyond the raw `gap_question`. I'd argue the pipeline does its part by passing `problem_context` to the filler. Contextualisation logic (weaving problem details into questions) belongs in the GapFiller implementation, not in `fill_parameter_gaps`. The tension: the spec says "generate plain-language contextualised question per gap," which could mean the pipeline generates the question or the filler generates it. The current design delegates to the filler, which is architecturally cleaner.

### T-2. Number of P1 items and release-blocking implications

Spec-compliance has 5 P1 items. I have 4 P1 items (3 from my review + 1 from cross-review reassessment). The tension: more P1s means a longer path to compliance. Not all P1s are equally urgent. I'd propose tiering:
- **Immediate P1** (bugs that corrupt output): source map return, str.replace fix
- **Near-term P1** (spec MUST items): FR-003 multi-template, FR-020 source structure
- **Deferred P1** (require spec clarification): LLMGapFiller (FR-022 vs FR-016 conflict), gap_fill_model (FR-009), conversus.yml (FR-014)

### T-3. FR-007 retry test: both flag the gap, different urgency

Spec-compliance notes FR-007 retry path has no test and classifies the test gap as P2 (R6). I note the same gap but don't assign a specific priority. The tension: the retry *implementation* exists and is correct by inspection, but without a test it could regress silently. P2 seems right for a test gap on implemented functionality.

### T-4. FR-015/SC-005 importability test: explicit vs implicit

Spec-compliance argues for an explicit importability test mirroring `test_game_forms.py`. I don't raise it. The tension: every test in the test suite imports the module, so any import error would be caught. An explicit test is documentation, not additional coverage. However, if the pattern exists in the sibling module's tests, consistency argues for adding it. P3.

## Safe Agreements

### SA-1. FR-020 source structure needs `problem_md`

Both reviews identify the flat `dict[str, str]` as missing the problem_md path. Compatible diagnosis, compatible fix direction.

### SA-2. FR-003 multi-template presentation is unimplemented

Both reviews confirm `candidates[0]` is silently used. Both propose protocol-based solutions.

### SA-3. FR-019 explicit type handling works correctly

Both reviews confirm `classify_decision_type` handles explicit type first, keyword fallback second. Implementation matches spec.

### SA-4. FR-023 non-interactive behavior is correct

Both reviews confirm `NonInteractiveGapFiller` raises on true gaps and uses defaults for default parameters. Tests cover both paths.
