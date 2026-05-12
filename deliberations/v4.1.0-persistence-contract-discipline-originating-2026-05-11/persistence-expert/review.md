Looking at this task, I need to read all the target files and provide a detailed technical review from a persistence expert perspective.

---

### Executive Summary

The v4.1.0 Persistence Contract Discipline amendment addresses a critical gap in Build Fractal's infrastructure stability by codifying operational requirements for persistent data contracts. From a persistence expert perspective, the amendment correctly identifies the core problem: declared-but-unenforced schemas create the illusion of stability while allowing silent drift. The proposed sub-clause framework covering declared schemas, mechanical enforcement, versioning, and cross-product consumer contracts represents sound persistence architecture principles.

However, the amendment contains several technical gaps that compromise its effectiveness. The schema declaration mechanism assumes field-based schemas and may not cover streaming, positional, or hybrid formats adequately. The versioning flexibility creates coordination risks across products. Most critically, the mechanical enforcement only catches forward drift (producer violates schema) but misses reverse drift (schema updated without updating producer code), creating a false sense of validation completeness. The cross-product consumer contract requirement is unidirectional and lacks consumer-side validation to prevent accidental dependency on undeclared surfaces.

**Most important recommendation**: Add explicit coverage for bidirectional drift detection and consumer-side contract validation to ensure schema enforcement completeness.

### Alignment

- **Mechanical enforcement mandate** (spec L62-66): The requirement for "A CI gate validates that artifacts written during a run conform to the declared schema" aligns with established persistence validation practices that catch schema violations at CI time rather than runtime.

- **Schema versioning requirement** (spec L68-70): Mandating a `schema_version` field with documented bump procedures follows standard data evolution patterns for maintaining backward compatibility and tracking breaking changes.

- **Cross-product surface declaration** (spec L72-79): Requiring producers to publish `CONSUMER-CONTRACT.md` declaring stable surfaces aligns with interface segregation principles and explicit dependency management.

- **Display text exclusion** (spec L81-86): The principle that "Display text inside an artifact is NOT a stable contract unless explicitly declared" correctly separates presentation from data structure, preventing accidental coupling to formatting details.

- **Discoverable schema location** (spec L56-60): Requiring schema declarations in discoverable locations like `STATE-FILES.md` or `CONSUMER-CONTRACT.md` follows documentation-as-code practices for schema governance.

### Missed Opportunities

- **Bidirectional drift detection**: The current mechanical enforcement (L62-66) only validates artifacts against schemas but doesn't detect when schemas are updated without corresponding producer code changes. Schema evolution testing that validates both directions would prevent schema-code desynchronization. Impact: high.

- **Schema format interoperability**: The amendment allows product-choice for schema formats (L64-65) but doesn't address cross-product schema consumption where different products use different formats. A canonical schema exchange format or translation layer would enable better ecosystem integration. Impact: medium.

- **Consumer-side contract validation**: The cross-product contracts (L72-79) only mandate producer-side declarations but don't require consumer-side tests that pin the consumed surface. Consumer validation fixtures would catch contract violations at the consumer's CI rather than only at runtime. Impact: high.

- **Schema migration validation**: The versioning requirement (L68-70) mandates version bumps but doesn't require migration path validation. Testing that data written under schema version N can be read under schema version N+1 would prevent migration failures. Impact: medium.

- **Streaming/positional format coverage**: The schema declaration (L56-60) assumes "field names, types, structural requirements" which maps well to JSON/YAML but less clearly to JSONL streams, positional formats, or binary data. Explicit coverage of non-field-based schemas would close this gap. Impact: medium.

- **Schema composition for hybrid formats**: The state-files.md example shows YAML frontmatter + markdown body formats, but the amendment doesn't address how to declare schemas for such composite artifacts where different parts follow different structural rules. Impact: low.

- **Temporal schema validation**: The amendment doesn't address how to validate artifacts written under older schema versions when the schema evolves. Backward compatibility validation would ensure old data remains readable. Impact: medium.

- **Performance-aware schema validation**: The CI gate requirement (L62-66) doesn't consider validation performance on large artifact sets. Incremental or sampling-based validation strategies would prevent CI timeouts on large state directories. Impact: low.

- **Cross-repository schema coordination**: When artifacts from one repository are consumed by another, the amendment doesn't specify how schema changes should be coordinated across repository boundaries. Schema change notifications or dependency management would improve coordination. Impact: medium.

### Off-Base Assumptions

- **Field-based schema universality**: The specification assumes in L59-60 that all schemas can be expressed as "field names, types, structural requirements." This assumption breaks for streaming formats (JSONL where line order matters), positional formats (CSV with column significance), and binary formats (parquet with embedded metadata). Many persistence surfaces use positional or streaming semantics that don't map cleanly to field-based descriptions.

- **CI gate sufficiency**: The mechanical enforcement assumption in L62-66 that "A CI gate validates that artifacts written during a run conform to the declared schema" assumes this catches all drift. In practice, this only catches forward drift (producer violates schema) but completely misses reverse drift (schema document updated, producer code unchanged). This creates a false sense of validation completeness.

- **Deterministic conformance clarity**: The spec assumes in L65-66 that "deterministic conformance check" is self-evident and sufficient to prevent the prose-schema loophole. This assumption underestimates how products might interpret "deterministic" - regex matching, manual checklists, or informal validation could all be claimed as "deterministic" while providing no real enforcement.

### Actionable Recommendations

1. **Expand schema surface coverage** (Priority: P1)
   - **Current state**: L56-60 specifies "field names, types, structural requirements" which assumes field-based schemas.
   - **Proposed change**: Add explicit coverage for streaming formats (JSONL line semantics), positional formats (column-order significance), binary formats (embedded metadata), and hybrid formats (YAML frontmatter + markdown body).
   - **Rationale**: The state-files.md example already uses hybrid formats, and JSONL is common for execution logs. Without explicit coverage, these formats might not receive adequate schema enforcement.
   - **Risk if ignored**: Products with streaming or hybrid formats may implement minimal "compliance" that doesn't actually validate the complex semantics of their persistence surfaces.

2. **Add bidirectional drift detection** (Priority: P1)
   - **Current state**: L62-66 mandates CI gate validation of artifacts against schemas.
   - **Proposed change**: Require validation in both directions - artifacts must conform to schemas AND schema changes must be validated against existing producer code to ensure code can still generate conformant artifacts.
   - **Rationale**: Forward-only validation creates a false sense of completeness. Schema evolution often breaks producer code in ways only caught by reverse validation.
   - **Risk if ignored**: Schema updates will silently break producers, discovered only at runtime when the producer generates non-conformant artifacts.

3. **Strengthen deterministic conformance definition** (Priority: P1)
   - **Current state**: L64-66 requires "deterministic conformance check" but doesn't define what qualifies.
   - **Proposed change**: Define deterministic conformance as "machine-executable validation with binary pass/fail result and specific failure descriptions" and explicitly exclude prose descriptions, manual checklists, or subjective interpretation.
   - **Rationale**: The C1 condition in spec § 10 identifies the prose-schema loophole as a real risk. Tighter definition prevents trivial compliance.
   - **Risk if ignored**: Products will claim compliance with weak validation that provides no real drift protection.

4. **Add consumer-side contract validation** (Priority: P2)
   - **Current state**: L72-79 requires producer-side contract declaration but no consumer-side validation.
   - **Proposed change**: Require consumers to implement test fixtures that pin the specific contract surfaces they consume and validate those fixtures in their CI.
   - **Rationale**: Producer-side declarations are meaningless if consumers can still accidentally depend on undeclared surfaces. Consumer-side validation catches drift at the consumer's CI.
   - **Risk if ignored**: Consumers will continue to couple to implementation details despite producer-side declarations, recreating the exact problems the amendment tries to solve.

5. **Mandate SemVer-compatible versioning** (Priority: P2)
   - **Current state**: L68-70 requires "documented bump procedure" but allows product-specific schemes.
   - **Proposed change**: Require SemVer-compatible versioning (MAJOR.MINOR.PATCH) with standard semantics: MAJOR for breaking changes, MINOR for backward-compatible additions, PATCH for backward-compatible fixes.
   - **Rationale**: Different versioning schemes across products prevent cross-product schema dependency management and coordination.
   - **Risk if ignored**: Products will use incompatible versioning schemes, preventing effective cross-product schema evolution coordination.

6. **Add schema migration validation** (Priority: P2)
   - **Current state**: L68-70 mandates version bumps but doesn't validate migration paths.
   - **Proposed change**: Require CI validation that artifacts written under schema version N can be successfully read/parsed under schema version N+1, with explicit migration testing.
   - **Rationale**: Version bumps without migration validation lead to breaking changes that aren't discovered until runtime.
   - **Risk if ignored**: Schema evolution will break existing data consumption, discovered only when old artifacts are accessed.

7. **Define cross-repository schema coordination** (Priority: P2)
   - **Current state**: Cross-product contracts (L72-79) don't specify coordination across repository boundaries.
   - **Proposed change**: Require schema change notifications (via GitHub releases or dependency updates) when cross-product surfaces change, with mandatory consumer acknowledgment before changes take effect.
   - **Rationale**: Cross-repository schema changes need coordination mechanisms to prevent breaking downstream consumers.
   - **Risk if ignored**: Schema changes in upstream repositories will break downstream consumers without warning or coordination.

8. **Add temporal validation for hybrid formats** (Priority: P3)
   - **Current state**: L56-60 doesn't address how to validate composite artifacts with multiple schema domains.
   - **Proposed change**: For hybrid formats (YAML frontmatter + markdown body), require separate schema declarations for each component and composite validation rules.
   - **Rationale**: The state-files.md example shows this pattern is already in use and needs explicit schema support.
   - **Risk if ignored**: Hybrid format validation will be inconsistent across products, leading to partial schema enforcement.

9. **Add performance considerations for large artifact sets** (Priority: P3)
   - **Current state**: L62-66 mandates CI validation without performance considerations.
   - **Proposed change**: Allow incremental validation (only validate changed artifacts) or sampling-based validation for large artifact sets, with explicit performance budgets.
   - **Rationale**: Full validation of large state directories could cause CI timeouts, leading products to disable validation entirely.
   - **Risk if ignored**: Products with large artifact sets may implement token validation or disable enforcement to avoid CI performance problems.

10. **Define schema evolution backward compatibility** (Priority: P3)
    - **Current state**: L68-70 requires version bumps but doesn't define backward compatibility requirements.
    - **Proposed change**: Require that schema changes maintain backward compatibility within MINOR versions and provide explicit migration paths for MAJOR versions.
    - **Rationale**: Without backward compatibility rules, any schema change could break existing consumers even with version bumps.
    - **Risk if ignored**: Schema evolution will be unnecessarily breaking, forcing frequent coordination overhead for minor schema improvements.

### Referenced Documentation

- `specs/v4.1.0-persistence-contract-discipline/spec.md` — sections/lines cited: L56-60 (declared schema), L62-66 (mechanical enforcement), L68-70 (versioning), L72-79 (cross-product contracts), L81-86 (declaration scope)
- `build-fractal/CONSTITUTION.md` — sections/lines cited: L84-113 (Principle II current text)
- `build-fractal/spec-kit-orc/specs/001-orchestrator/contracts/state-files.md` — sections/lines cited: L10-27 (File Index showing hybrid formats), L31-45 (YAML frontmatter examples), L213-224 (JSONL execution log format)