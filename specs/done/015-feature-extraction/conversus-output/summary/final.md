# Synthesis: 015 Feature Extraction Pipeline

**Synthesizer**: neutral
**Spec**: 015-feature-extraction
**Date**: 2026-03-24

---

## Process Summary

- **Agents**: 3 -- extraction-engineer, schema-engineer, spec-compliance
- **Total artifacts**: 16
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 23
- **Recommendations withdrawn** (Phase 3): 1
- **Recommendations modified** (Phase 3): 8
- **Recommendations surviving** (Phase 3): 14
- **New recommendations added** (Phase 3): 4
- **Disputes remaining** (Phase 4): 4
- **Convergence points** (Phase 4): 5

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| 1 | extraction-engineer | Normalize position vector lengths | P1 | Surviving | None | Unanimous | Accepted |
| 2 | extraction-engineer | Fix disposition regex boundary | P2 | Modified (two-pass) | schema-engineer T-1 | None | Disputed |
| 3 | extraction-engineer | Tighten safe agreement pattern | P2 | Surviving | None | None | Accepted |
| 4 | extraction-engineer | Pass red/blue role explicitly | P2 | Modified (meta.json) | schema-engineer T-2 | None | Accepted-Modified |
| 5 | extraction-engineer | Use model_copy for round override | P3 | Surviving | None | None | Accepted |
| 6 | extraction-engineer | Exclude plugins/ from iteration | P2 | Surviving | None | Bilateral | Accepted |
| 7 | extraction-engineer | Add write-time validation | P3 | Surviving | None | Bilateral | Accepted |
| 8 | extraction-engineer | Document priority-absent defaults | P2 | Surviving | None | None | Accepted |
| 9 | schema-engineer | Refactor AgentFeatures discriminated union | P1 | Modified (staged) | extraction-engineer DC-1 | None | Disputed |
| 10 | schema-engineer | Per-mode field validation on FeatureSet | P2 | Modified (soft check) | None | None | Accepted-Modified |
| 11 | schema-engineer | Deduplicate VALID_MODES | P2 | Surviving | None | None | Accepted |
| 12 | schema-engineer | AgreementMatrix type alias | P3 | Surviving | None | None | Accepted |
| 13 | schema-engineer | Implement territory_claim_vector and confirmed_count | P2 | Surviving | None | Unanimous | Accepted |
| 14 | schema-engineer | Typed FeatureSetMetadata model | P3 | Modified (extra=allow) | spec-compliance T-2 | Bilateral | Accepted-Modified |
| 15 | schema-engineer | Add __all__ to features.py | P3 | Surviving | None | None | Accepted |
| 16 | schema-engineer | Generate JSON Schema at build time | P3 | Modified (FR-005 artifact) | None | Bilateral | Accepted-Modified |
| 17 | spec-compliance | Create per-mode YAML schema files | P1 | Modified (JSON Schema) | extraction-engineer DC-1 | Bilateral | Accepted-Modified |
| 18 | spec-compliance | Implement CLI entry point | P1 | Modified (P2 priority) | extraction-engineer T-1 | None | Disputed |
| 19 | spec-compliance | Amend FR-014/FR-016 package naming | P1 | Surviving | None | Unanimous | Accepted |
| 20 | spec-compliance | Implement territory_claim_vector | P2 | Surviving | None | Unanimous | Accepted |
| 21 | spec-compliance | Implement confirmed_count | P2 | Surviving | None | Unanimous | Accepted |
| 22 | spec-compliance | Add pre-write validation | P2 | Surviving | None | Bilateral | Accepted |
| NR-1 | extraction-engineer | Add meta.json writing to engine | P2 | New | -- | -- | Accepted |
| NR-2 | schema-engineer | Add mode field to AgentFeatures | P2 | New | extraction-engineer disputes | -- | Disputed |
| NR-3 | spec-compliance | Amend spec Section 2 with defaults | P2 | New | -- | -- | Accepted |
| NR-4 | spec-compliance | Add plugins/ to exclusion list | P2 | New | -- | -- | Accepted |

---

## Dangerous Contradictions Found

**Resolved Contradictions**:

1. **FR-005 artifact format** -- extraction-engineer argued YAML schemas are redundant duplication of Pydantic models. Spec-compliance required YAML per the literal spec. Resolution: schema-engineer proposed JSON Schema generation, adopted by both. FR-005 will be amended to accept JSON Schema.

2. **FR-014/FR-016 package naming** -- spec-compliance flagged the `conversus-features` vs. `conversus.schemas` discrepancy. Resolution: unanimous agreement to amend the spec to match the actual namespace. No package restructuring.

3. **Position vector length normalization** -- extraction-engineer identified the bug. Spec-compliance confirmed it is a correctness issue. Schema-engineer agreed the fix belongs in extraction code. No remaining disagreement.

**Unresolved Contradictions**:

1. **Disposition regex approach** -- extraction-engineer insists on two-pass (strict primary + permissive fallback with logging). Schema-engineer insists on single-pass permissive (within recommendation-scoped sections) with logging. Assessment below.

2. **AgentFeatures interim `mode` field** -- schema-engineer wants `mode: str | None = None` added now. Extraction-engineer wants full deferral, arguing the field is informational noise. Assessment below.

---

## Systemic Contradictions

- **Template-to-extraction coupling without a formal contract**
  - **Manifests in**: Disposition regex debate (two-pass vs. permissive), safe agreement counting, role detection.
  - **Root cause**: The extraction pipeline parses markdown output that LLMs generate from templates, but there is no formal contract between templates and extraction rules. Templates prescribe output format; extraction assumes output format. When LLM output deviates slightly from the template prescription, extraction must decide between strictness (FR-002) and resilience (FR-003).
  - **Implication for spec**: Define a formal "extraction contract" section in each template that lists the exact structural markers, heading patterns, and label formats that the extraction pipeline targets. This makes the coupling explicit and testable.

- **God-object tension between flat extensibility and discriminated type safety**
  - **Manifests in**: AgentFeatures mode field dispute, per-mode validation dispute, unpopulated fields.
  - **Root cause**: The feature models must serve two masters: extraction code (which produces them) and plugin code (which consumes them). Extraction prefers flat models (simple construction). Plugins prefer discriminated models (clear field semantics). The spec's FR-007 does not specify which extensibility pattern to use.
  - **Implication for spec**: Add an FR-007a that explicitly requires mode-discriminated feature models, or explicitly permits the flat model with documented field-mode mapping. The current ambiguity generates recurring disputes.

- **Spec-vs-implementation reconciliation process**
  - **Manifests in**: FR-005 (YAML vs. JSON Schema), FR-012 (CLI priority), FR-014/FR-016 (package naming).
  - **Root cause**: The spec was written before implementation. Some spec requirements (standalone `conversus-features` package, YAML schema files, CLI command) reflected a pre-implementation architecture that the actual implementation diverged from for sound reasons. The review process exposed these divergences but there is no defined process for amending the spec as part of this review.
  - **Implication for spec**: Include spec amendments as explicit deliverables of the conversus review process. Each "NOT MET" FR should produce either an implementation fix or a spec amendment, documented in the synthesis.

---

## Convergence Achieved

- **Position vector normalization** -- Strength: Unanimous
  - **Agreed recommendation**: After extracting all agents in a round, compute `max_recs = max(af.recommendation_count for af in agent_features.values())` and pad all position vectors to length `max_recs`.
  - **Supporting agents**: extraction-engineer (R-1), schema-engineer (DC-1), spec-compliance (DC-1 cross-review)
  - **Evidence basis**: Spec Section 2 explicitly states "Vector length = max recommendations across agents."
  - **Pre-existing or earned**: Pre-existing -- extraction-engineer identified it in Phase 1 and no one disputed.

- **Implement territory_claim_vector and confirmed_count** -- Strength: Unanimous
  - **Agreed recommendation**: Add extraction logic for both fields. territory_claim_vector: binary encoding from PD Phase 1 review sections. confirmed_count: count from red-blue Phase 4/synthesis.
  - **Supporting agents**: All three reviewers (schema-engineer O-1/O-2, spec-compliance R-4/R-5, extraction-engineer acknowledges)
  - **Evidence basis**: Both features are defined in spec Section 2 and declared in the AgentFeatures model but have no extraction code.
  - **Pre-existing or earned**: Pre-existing -- identified by schema-engineer in Phase 1.

- **Amend FR-014/FR-016 to conversus.schemas namespace** -- Strength: Unanimous
  - **Agreed recommendation**: Change FR-014 to: "The pipeline MUST ship within the `conversus.schemas` package." Change FR-016 to: "The package MUST be importable by plugins: `from conversus.schemas import extract_features, FeatureSet`."
  - **Supporting agents**: All three reviewers.
  - **Evidence basis**: The extraction pipeline shares types with game_forms.py and objectives.py. A standalone package would require duplicating shared types.
  - **Pre-existing or earned**: Earned -- spec-compliance proposed the amendment in Phase 1; extraction-engineer and schema-engineer endorsed in Phase 2.

- **Add plugins/ to non-agent directory exclusion** -- Strength: Bilateral
  - **Agreed recommendation**: Add `"plugins"` to the exclusion set in `_discover_agent_names()`, `_extract_pd_agent_features()`, and `_extract_rb_agent_features()`.
  - **Supporting agents**: extraction-engineer (R-6), spec-compliance (NR-2)
  - **Evidence basis**: Spec 016 will create `{output}/plugins/` directories that the extraction pipeline must not iterate.
  - **Pre-existing or earned**: Earned -- extraction-engineer proposed in Phase 1 for forward-compatibility.

- **JSON Schema for FR-005 compliance** -- Strength: Bilateral
  - **Agreed recommendation**: Generate per-mode JSON Schema from Pydantic models at build time. Amend FR-005 to accept JSON Schema.
  - **Supporting agents**: schema-engineer (R-8 revised), spec-compliance (R-1 revised)
  - **Evidence basis**: JSON Schema is machine-generated (no drift from Pydantic models) and language-agnostic (satisfies FR-005's intent).
  - **Pre-existing or earned**: Earned -- schema-engineer proposed in Phase 1; spec-compliance adopted in Phase 3.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

- **Dispute: Disposition regex approach**
  - **Positions**: Extraction-engineer advocates two-pass parsing (strict primary regex `\*\*Disposition\*\*:` + permissive fallback with logging). Schema-engineer advocates single-pass permissive regex scoped within recommendation sections, with logging for malformed markers. Cite: extraction-engineer disputes R-2, schema-engineer disputes R-2.
  - **Arguments**: Extraction-engineer argues FR-002 requires matching the prescribed format, and the permissive-only pattern can produce false positives in non-label text. Schema-engineer argues the two-pass approach risks N-vs-N+1 count discrepancies and that scoping to recommendation sections eliminates the false-positive risk.
  - **Synthesizer assessment**: Schema-engineer's scoped-permissive approach is stronger. The disposition pattern is always evaluated within recommendation sections (split by `#### Recommendation N` headings), not against the full document. Within that scope, false positives are extremely unlikely. The N-vs-N+1 discrepancy in the two-pass approach is a real risk: if one recommendation uses a slightly malformed marker, the strict pass produces N counts while the permissive pass produces N+1, and the strict count is silently used, losing a recommendation. The scoped single-pass with anomaly logging is the safer design.
  - **Recommended resolution**: Adopt single-pass permissive regex, scoped within recommendation sections. Add `logger.warning()` when matched text has unbalanced bold markers. Document this as the extraction contract for disposition labels.

- **Dispute: AgentFeatures interim mode field**
  - **Positions**: Schema-engineer wants `mode: str | None = None` added to AgentFeatures now as an immediately useful consumer aid. Extraction-engineer argues this is informational noise that trains consumers against a pattern that will be deprecated by per-mode subclasses. Cite: schema-engineer disputes NR-1, extraction-engineer disputes R-2.
  - **Arguments**: Schema-engineer argues consumers currently have no programmatic way to determine which fields are semantically relevant for their mode. Extraction-engineer argues the field does not provide type-level discrimination and creates a false stepping stone.
  - **Synthesizer assessment**: Schema-engineer's position is stronger for the immediate term. The extraction pipeline's consumers (plugins in specs 017-019) need to know which features to read. Without a `mode` field, consumers must reach up to the parent FeatureSet to determine mode, then maintain their own mode-to-fields mapping. The `mode` field on AgentFeatures is a simple, non-breaking improvement. Extraction-engineer's concern about "training consumers against a deprecated pattern" is speculative -- the per-mode subclasses are not specified in any current spec, and when they arrive, the `mode` field becomes the discriminator, not a deprecated field.
  - **Recommended resolution**: Add `mode: str | None = None` to AgentFeatures. Extraction code sets it at construction time. Document in the model's docstring that this field indicates which mode's feature fields are semantically populated. If per-mode subclasses are later introduced, `mode` becomes the discriminator field.

- **Dispute: CLI implementation priority**
  - **Positions**: Spec-compliance insists FR-012 is a MUST requirement and must be P1 to move the spec to "done." Extraction-engineer argues the CLI is P2 since no current consumer uses it. Cite: spec-compliance disputes R-1, extraction-engineer revision R-2.
  - **Arguments**: Spec-compliance argues RFC 2119 "MUST" is not optional regardless of current consumer demand. Extraction-engineer argues practical urgency should determine priority.
  - **Synthesizer assessment**: Spec-compliance is correct on process: a MUST requirement that is NOT MET blocks "done" status. However, the implementation effort is minimal (a 15-line argparse or click wrapper around `extract_features()`). The resolution is not to change the priority but to acknowledge that the CLI is a small deliverable that should be included in the spec 015 implementation rather than deferred.
  - **Recommended resolution**: Implement a minimal CLI as part of spec 015 deliverables. Use `python -m conversus.schemas.extraction --output-dir <path> --mode <mode>` as the entry point, consistent with the amended package naming. Add a `[project.scripts]` entry if a top-level command is desired.

- **Dispute: FR-005 amendment process**
  - **Positions**: Spec-compliance insists the spec must be formally amended to accept JSON Schema instead of YAML. Other reviewers implicitly treat the change as agreed without formal amendment. Cite: spec-compliance disputes R-2.
  - **Arguments**: Spec-compliance argues that implementing a different artifact than what the spec describes without amending the spec is process-violating drift.
  - **Synthesizer assessment**: Spec-compliance is correct. The convergence on JSON Schema is substantive but must be formalized. The spec amendment is a documentation task, not an implementation task, and should be included in the actionable spec changes below.
  - **Recommended resolution**: Amend FR-005 in the spec. New text: "Each mode MUST have a feature schema defined as a JSON Schema file generated from the Pydantic model, stored in `schema/features/{mode}.schema.json`, specifying feature names, types, and extraction metadata via JSON Schema extensions."
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

**P1 -- Must implement** (blocking issues or unanimous convergence):

1. **Normalize position vector lengths**: After extracting all agents in a round, pad all position vectors to `max(recommendation_count)` across agents. Source: extraction-engineer R-1, unanimous convergence.

2. **Implement territory_claim_vector extraction**: Parse PD Phase 1 review sections into binary territory claim vectors. Source: schema-engineer O-1, spec-compliance R-4, unanimous convergence.

3. **Implement confirmed_count extraction**: Count confirmed findings from RB Phase 4/synthesis. Source: schema-engineer O-2, spec-compliance R-5, unanimous convergence.

4. **Amend FR-014**: Change to "The pipeline MUST ship within the `conversus.schemas` package." Source: spec-compliance R-3, unanimous convergence.

5. **Amend FR-016**: Change to "The package MUST be importable: `from conversus.schemas import extract_features, FeatureSet`." Source: spec-compliance R-3, unanimous convergence.

6. **Amend FR-005**: Change to "Each mode MUST have a feature schema defined as a JSON Schema file generated from the Pydantic model, stored in `schema/features/{mode}.schema.json`." Source: schema-engineer R-8, spec-compliance R-1, bilateral convergence.

7. **Implement minimal CLI**: Add `python -m conversus.schemas.extraction --output-dir <path> --mode <mode>` entry point. Source: spec-compliance R-2 (FR-012 MUST requirement).

**P2 -- Should implement** (majority convergence or strong single-agent case):

1. **Add `mode: str | None = None` to AgentFeatures**: Enable consumers to determine semantically relevant fields. Source: schema-engineer NR-1, synthesizer assessment.

2. **Add `plugins/` to non-agent directory exclusion**: Forward-compatibility with spec 016. Source: extraction-engineer R-6, spec-compliance NR-2, bilateral convergence.

3. **Use scoped single-pass permissive disposition regex with anomaly logging**: Replace current dual-regex approach. Source: synthesizer assessment of schema-engineer and extraction-engineer dispute.

4. **Document priority-absent position vector defaults in spec Section 2**: "When Priority label is absent, Surviving=2, Modified=1." Source: extraction-engineer R-8, spec-compliance NR-1.

5. **Tighten safe agreement pattern to top-level items only**: Source: extraction-engineer R-3.

6. **Write meta.json in engine for red/blue roles**: Engine writes `{"role": "red"|"blue"}` in agent output dirs. Extraction reads it with content-detection fallback. Source: extraction-engineer NR-1.

7. **Use model_copy for round number override**: Replace model_dump reconstruction. Source: extraction-engineer R-5.

8. **Deduplicate VALID_MODES to single canonical location**: Source: schema-engineer R-3.

**P3 -- Consider implementing** (bilateral agreement or strong but disputed):

1. **Create typed FeatureSetMetadata with extra="allow"**: Source: schema-engineer R-6 revised, spec-compliance T-2. Note: useful for discoverability but not blocking.

2. **Add __all__ to features.py**: Source: schema-engineer R-7.

3. **Add AgreementMatrix type alias**: Source: schema-engineer R-4.

4. **Add write-time validation**: Source: extraction-engineer R-7, spec-compliance R-6. Note: primarily benefits manual construction path.

5. **Generate per-mode JSON Schema at build time**: Implementation of amended FR-005. Source: schema-engineer R-8.

---

## Key Concessions

**extraction-engineer**:
- Modified R-2 (disposition regex) from strict-only to two-pass based on schema-engineer's resilience argument.
- Modified R-4 (role detection) from config-parameter to meta.json approach based on schema-engineer's filesystem-artifacts principle.

**schema-engineer**:
- Modified R-1 (discriminated union) from full refactoring to staged approach based on extraction-engineer's operational cost feedback.
- Modified R-6 (metadata typing) from strict typed model to extra="allow" compromise based on spec-compliance's extensibility concern.
- Modified R-8 (JSON Schema) from build convenience to FR-005 compliance artifact based on spec-compliance's spec-amendment framing.

**spec-compliance**:
- Modified R-1 (YAML schemas) from manual YAML files to machine-generated JSON Schema based on extraction-engineer's maintenance drift argument and schema-engineer's JSON Schema proposal.
- Modified R-2 (CLI priority) from P1 to P2 based on extraction-engineer's practical urgency argument. (Note: still insists on implementation, just at lower priority than parsing fixes.)
- Withdrew R-7 (pyyaml dependency) because JSON Schema generation makes pyyaml unnecessary.
