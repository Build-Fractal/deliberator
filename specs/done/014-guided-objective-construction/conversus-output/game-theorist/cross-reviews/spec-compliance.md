# Cross-Review: game-theorist reviewing spec-compliance

## Dangerous Contradictions

### DC-1. FR-003 priority: P1 (spec-compliance) vs P2 (game-theorist)

Spec-compliance classifies FR-003 (multi-template user selection) as P1 because the spec uses "MUST present." I classify it as P2 because the pipeline functions correctly for the common case (single best candidate) and the alphabetical ordering rarely produces ambiguous results with the current template library. The contradiction matters: if FR-003 is truly P1, it blocks compliance sign-off and should be fixed before the source-map bug. If it's P2, the source-map and substitution bugs take priority because they produce *incorrect output* rather than *missing interaction*.

My position: bugs that produce wrong output (str.replace collision, source map misclassification) are more dangerous than missing features (FR-003 template selection) even when the missing feature is spec-MUST. Wrong output is silent corruption; missing features are visible gaps.

### DC-2. SC-002 assessment: NOT MET (spec-compliance) vs not raised (game-theorist)

Spec-compliance flags SC-002 (natural-language-to-weight mapping) as NOT MET. I don't mention it at all. Looking at the spec, SC-002 is a success criterion that requires "speed is twice as important as cost" to produce weight values. The current pipeline has no NLP interpretation -- the DictGapFiller in tests pre-maps values. Spec-compliance is correct that this is NOT MET. I missed this because I focused on the deterministic stages and treated Stage 2 as "pluggable via GapFiller." But pluggable doesn't mean implemented -- the spec requires this specific capability to exist.

### DC-3. FR-009 `gap_fill_model` config surface

Spec-compliance flags FR-009 as NOT MET (no config key for `gap_fill_model`). I don't mention FR-009. Spec-compliance is correct: the GapFiller protocol is a code-level abstraction, but the spec requires a *config-level* knob. These are different concerns -- you can have a pluggable protocol with no user-facing configuration, which is exactly what exists now. However, implementing FR-009 without FR-022 (LLMGapFiller) is meaningless -- you'd have a config key with no implementation to configure. These should be bundled.

## Tensions

### T-1. FR-014 `conversus.yml` integration priority

Spec-compliance classifies FR-014 (writing `objective` field to `conversus.yml`) as P1. I don't raise it. The tension: FR-014 is about downstream integration -- making the objective discoverable by other conversus components. Without it, the objective.yml file exists but nothing points to it. Spec-compliance argues this "breaks the downstream plugin consumption chain." I'd argue this is P2 because the file is still usable by path convention, and `conversus.yml` integration is a separate concern from the construction pipeline's correctness.

### T-2. FR-005 contextualized questions: depth of requirement

Spec-compliance marks FR-005 as PARTIALLY MET because questions are not contextualised beyond the raw `gap_question`. I don't specifically assess FR-005. The tension: the spec envisions questions like "You mentioned Redis is faster..." which requires NLP understanding of the problem text. The current implementation passes `problem_context` to the filler but doesn't weave it into the question text. Contextualization is arguably the filler's job (especially LLMGapFiller), not the pipeline's job. But spec-compliance reads FR-005 as requiring the pipeline to do the weaving.

### T-3. FR-015/SC-005 importability test

Spec-compliance notes that FR-015 and SC-005 are "tested indirectly" and argues for an explicit importability test. I don't raise this. Spec-compliance is right that an explicit test is better, but the risk is very low -- the import chain is trivial (stdlib + pydantic + yaml). This is P3 at most.

### T-4. LLMGapFiller as P1 requirement

Spec-compliance classifies the missing LLMGapFiller as P1 (R4). I don't raise it because the GapFiller protocol is clean and the LLM implementation is an integration concern. The tension: the spec names LLMGapFiller as a required implementation of FR-022, and spec-compliance reads MUST literally. However, implementing an LLMGapFiller requires choosing a model provider, which is a runtime dependency that the spec says should be configurable (FR-009). Shipping a stub LLMGapFiller that raises NotImplementedError satisfies the letter but not the spirit.

## Safe Agreements

### SA-1. FR-020 source structure is incomplete

Both reviews identify the flat `dict[str, str]` as missing the `problem_md` path. Spec-compliance frames it as spec non-compliance; I frame it as a missed opportunity for traceability. Same diagnosis, same fix needed.

### SA-2. FR-019 keyword fallback classification works correctly

Both reviews confirm that `classify_decision_type` correctly handles explicit type first, keyword fallback second. The implementation matches the spec's intent.

### SA-3. FR-021 deferred parameter handling is correct

Both reviews confirm that function-type parameters with `derived_from` are properly identified, deferred, and given placeholder values. No issues raised by either reviewer.

### SA-4. FR-012 determinism is achieved

Both reviews confirm no randomness exists in the pipeline and that determinism tests pass. The sorted glob, sorted-by-length substitution, and alphabetical template ordering all contribute.
