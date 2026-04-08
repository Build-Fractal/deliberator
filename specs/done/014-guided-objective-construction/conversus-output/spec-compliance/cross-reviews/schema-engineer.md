# Cross-Review: spec-compliance reviewing schema-engineer

## Dangerous Contradictions

### DC-1. FR-003 as P2: spec non-compliance accepted too easily

Schema-engineer classifies FR-003 as P2, noting "the spec says MUST" in the description but then assigning P2 priority. I classify it as P1. The contradiction: schema-engineer acknowledges the MUST language but deprioritizes it because "the pipeline still produces a valid objective." This conflates *correct output* with *compliant behavior*. The spec does not say "present templates IF the auto-selected one might be wrong" -- it says "MUST present when multiple are viable." Downgrading a MUST to P2 without amending the spec creates a compliance gap that will persist.

### DC-2. `SourceProvenance` model vs spec language

Schema-engineer's R1 proposes `SourceProvenance` with `problem_md: str | None` and `filled_by: dict[str, str]`. I agree with the direction but the `| None` on `problem_md` is a contradiction: the spec says `source` contains `problem_md` path -- making it optional means a valid `AssembledObjective` can exist without recording the input problem file. If `problem_md` is the traceability anchor, it should be required (with a default of `"stdin"` or similar for programmatic use without a file). Making it optional undermines the traceability guarantee the spec intended.

### DC-3. P1 count inflation: 4 P1 items

Schema-engineer has four P1 items: source structure, source map return, str.replace fix, boolean coercion. I have five P1s (FR-003, FR-020, FR-014, LLMGapFiller, gap_fill_model). Both lists are arguably too long. The contradiction: if everything is P1, nothing is P1. However, the items differ in kind -- schema-engineer's P1s are *bugs* (code produces wrong behavior), mine are *spec violations* (code doesn't implement what the spec requires). These should be distinguished: bugs first, then spec gaps. Schema-engineer's source-map and str.replace fixes are higher urgency than boolean coercion (no current trigger) or FR-020 restructuring (cosmetic until problem_md is populated).

## Tensions

### T-1. LLMGapFiller omission: intentional deferral vs spec violation

Schema-engineer's M3 notes "the LLMGapFiller is absent, likely intentional (deferred to integration)." I classify it as NOT MET (FR-022). The tension: schema-engineer reads the omission charitably (deferred by design), I read it literally (spec says it's required). The reality is likely in between -- the GapFiller protocol is designed to accept an LLMGapFiller, and the implementation is deferred because it requires an LLM dependency. Schema-engineer's "likely intentional" framing is reasonable engineering judgment, but it shouldn't change the compliance assessment. The spec says MUST; the implementation doesn't have it; the status is NOT MET regardless of intent.

### T-2. `.yaml` extension support: robustness or convention enforcement

Schema-engineer raises `.yaml` extension support as P3. I don't raise it. The tension: the current convention is `.yml` (all templates use it). Adding `.yaml` support is permissive; failing on `.yaml` files is strict. The strict approach (warn/error on `.yaml`) is better for convention enforcement. But the spec doesn't mandate an extension convention, so either approach is compliant. This is P3 -- a team convention decision, not a compliance issue.

### T-3. Retry path test coverage

Schema-engineer's P3 raises the untested retry path with range guidance. I raise the same gap as P2 (R6) under FR-007. The priority tension: the retry *implementation* exists, so it's not a spec violation, but without a test it could regress. P2 is warranted because FR-007 is a MUST requirement -- having the code but no test is a partial compliance issue.

### T-4. `problem_md_path` parameter addition

Schema-engineer proposes adding `problem_md_path: str | None = None` to `construct_objective` as P2. I propose the same within the source restructuring (R2, P1). The tension is priority, not direction. Schema-engineer separates the parameter addition from the source restructuring; I bundle them. Bundling is cleaner -- you shouldn't add the parameter without restructuring the source to use it.

## Safe Agreements

### SA-1. Source map must be returned from `fill_parameter_gaps`

Identical diagnosis, compatible fix proposals. The value-comparison fragility is agreed upon.

### SA-2. `_substitute_symbolic_form` substring collision is a bug

Both reviews identify the same bug and propose the same regex word-boundary fix. Priority differs (P1 for both, which is agreement).

### SA-3. FR-021 deferred parameter handling is correct

Both reviews confirm function-type parameters with `derived_from` are properly handled.

### SA-4. GapFiller protocol design is clean

Both reviews affirm the `@runtime_checkable` protocol, the three implementations, and the extension point design. The only issue is the exception-based control flow, which both agree should use a custom exception.
