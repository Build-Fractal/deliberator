# Schema Design Expert Revision — v4.2.0 Structured Deliberation Outputs

## Recommendation Dispositions

### Recommendation 1: Switch to JSON Schema canonical format

- **Original position**: Mandate JSON Schema as canonical format; emit JSON rather than XML for deliberation outputs.
- **Disposition**: Modified
- **Explanation**: Devils-advocate cross-review correctly identified that my "mandate" language contradicts the spec's explicit "product-choice" framing and potentially violates Principle XXVIII's format-choice non-mandate. However, my technical analysis of XML syntax conflicts with agent prose content containing `<`, `>`, `&` characters remains valid - this is a concrete technical constraint that all three other reviews acknowledged as a real problem. The modified recommendation respects the constitutional product-choice framework while providing strong evidence for the JSON Schema option.

**Modified recommendation**: Recommend JSON Schema as the preferred option within the product-choice framework, with explicit comparison criteria: (1) agent prose syntax compatibility, (2) Python ecosystem integration, (3) validation error message quality, (4) tooling ecosystem maturity. The format choice (OQ2) should be resolved through comparative evaluation as devils-advocate suggests, but heavily weighted toward JSON Schema based on the XML syntax conflict evidence.

### Recommendation 2: Add required identity fields to envelope

- **Original position**: Add `deliberation_stage`, `engine_version`, and `source_commit` as required envelope fields.
- **Disposition**: Surviving
- **Explanation**: Adapter-consumer cross-review confirmed this independently: "Both perspectives identify the same structural inadequacy from different angles—consumer needs and schema completeness." No cross-review challenged the technical necessity of these fields. The concern raised by engineer about timeline pressure is addressed by treating this as a 0.x requirement rather than delaying for post-v1.0.0.

### Recommendation 3: Specify field-level validation constraints

- **Original position**: Add `minLength: 1`, `maxLength: 2048` bounds; require non-empty content for critical fields.
- **Disposition**: Modified
- **Explanation**: Engineer cross-review raised valid performance concerns about validation complexity. The modified approach balances validation robustness with performance requirements by implementing basic constraints first (non-empty content) and deferring complex pattern validation to later schema versions.

**Modified recommendation**: Implement basic field validation constraints for v0.1.0: `minLength: 1` for critical fields to prevent degenerate outputs, basic type validation. Defer complex constraints (`maxLength`, pattern validation, content model precision) to v0.2.0 after performance testing establishes acceptable complexity budgets.

### Recommendation 4: Design namespace versioning strategy

- **Original position**: Use versioned namespaces `/schema/v1`, `/schema/v2` with explicit compatibility declarations.
- **Disposition**: Modified
- **Explanation**: Devils-advocate cross-review correctly warned against premature lock-in to v1.0.0 namespace without field testing. The schema versioning approach must coordinate with devils-advocate's 0.x versioning recommendation to avoid the exact migration debt they identified.

**Modified recommendation**: Implement namespace versioning strategy but start with 0.x namespaces: `https://build-fractal.org/conversus/schema/v0` for initial implementation. Promote to v1 namespace only after field testing with at least one production deliberation validates the design. This preserves versioning capability while avoiding premature lock-in.

### Recommendation 5: Add cross-reference integrity validation

- **Original position**: Define ID/IDREF constraints to validate that all `ref` attributes point to existing elements within the same output.
- **Disposition**: Modified
- **Explanation**: Engineer cross-review identified this as a P2 feature that conflicts with timeline pressure. Adapter-consumer cross-review confirmed the technical need but emphasized the complexity of testing semantic equivalence. The modification stages this feature to avoid blocking the core migration.

**Modified recommendation**: Defer cross-reference integrity validation to v0.2.0. For v0.1.0, implement basic reference syntax validation (valid identifier format) without referential integrity checking. This allows the core structural migration to proceed while establishing the foundation for future integrity validation.

### Recommendation 6: Define concrete SemVer bump policies

- **Original position**: Specify exact scenarios: adding optional fields = MINOR, adding required fields = MAJOR, changing enum values = MAJOR.
- **Disposition**: Modified
- **Explanation**: Devils-advocate cross-review identified fundamental SemVer limitations: "removing or renaming fields creates backward compatibility nightmares that SemVer doesn't adequately address." Engineer cross-review suggested automation tooling. The modification combines technical precision with explicit documentation of SemVer limitations.

**Modified recommendation**: Define concrete bump policies for common scenarios (add optional field = MINOR, add required field = MAJOR, change enum = MAJOR) AND explicitly document SemVer limitations for field removal/renaming scenarios. These require coordinated migration rather than automatic compatibility. Include devils-advocate's concern in the versioning policy documentation.

### Recommendation 7: Add extension points for mode-specific data

- **Original position**: Add optional `mode_metadata` object in envelope for mode-specific attributes.
- **Disposition**: Modified
- **Explanation**: Adapter-consumer cross-review emphasized immediate utility over future-proofing: "adapter-consumer wants the schema to serve current use cases well; schema-design-expert wants extensibility for future needs." The modification balances current needs with reasonable extensibility.

**Modified recommendation**: Defer dedicated mode-specific extension points to v0.2.0. For v0.1.0, ensure the envelope design doesn't preclude future extension (avoid `additionalProperties: false` in schema). This serves current needs while preserving future flexibility without adding complexity to the initial implementation.

### Recommendation 8: Specify content encoding handling

- **Original position**: If retaining XML, mandate CDATA sections for prose fields; if switching to JSON, specify Unicode normalization.
- **Disposition**: Surviving
- **Explanation**: All three cross-reviews acknowledged XML syntax conflicts as a real technical constraint. Engineer: "XML syntax conflicts with agent prose." Adapter-consumer: "schema-design-expert's core technical concern about XML syntax conflicts with agent prose content." Devils-advocate: "XML special character problems are real." This remains a critical technical issue regardless of format choice.

### Recommendation 9: Define validation error reporting format

- **Original position**: Specify error object schema with `field_path`, `error_code`, and `human_message` properties.
- **Disposition**: Modified
- **Explanation**: Engineer cross-review questioned whether custom error schemas are needed: "Verify that existing JSON Schema validation error formats meet schema-design-expert's requirements before implementing custom error schemas." The modification respects this concern while preserving error handling robustness.

**Modified recommendation**: For v0.1.0, rely on standard JSON Schema validator error formats with documented error handling patterns. Define custom error schema only if standard formats prove inadequate during field testing. This avoids premature complexity while ensuring error handling robustness.

## New Recommendations

### Timeline-constrained schema staging (Priority: P1)
- **Triggered by**: Engineer cross-review emphasis on timeline pressure and devils-advocate warning about premature lock-in. Multiple cross-reviews identified that my P1/P2 recommendations would push past 2026-12-01 deadline.
- **Proposed change**: Implement schema migration in two phases: v0.1.0 by 2026-10-01 with basic structural validation (envelope, required fields, type checking) and v0.2.0 by 2027-01-31 with advanced features (cross-reference validation, extension points, sophisticated constraints).
- **Rationale**: Meets constitutional deadline requirement while avoiding premature lock-in to incomplete schema design. Allows field testing to validate design decisions before v1.0.0 promotion.

### Consumer-producer coordination framework (Priority: P1)
- **Triggered by**: Adapter-consumer cross-review emphasis that "Both schema design improvements AND consumer protection mechanisms should be P1 requirements." My original review treated consumer migration as secondary to schema design quality.
- **Proposed change**: Schema design decisions must include consumer impact assessment. Every schema feature must specify: (1) consumer parsing complexity impact, (2) migration timeline implications, (3) fallback behavior for consumers during transition.
- **Rationale**: Prevents schema design decisions from creating operationally unmanageable consumer migrations. Addresses adapter-consumer concern that schema-first approach could force lockstep upgrades.

### Validation enforcement flexibility (Priority: P2)
- **Triggered by**: Engineer cross-review concern about validation brittleness: "Their strict validation approach could cause production outages I want to prevent." Adapter-consumer emphasis on "predictable failure modes."
- **Proposed change**: Implement tiered validation enforcement: strict validation in CI/development, with documented graceful degradation paths for production edge cases (operator flags, size thresholds, validation timeouts).
- **Rationale**: Balances constitutional mechanical enforcement requirements with operational reliability concerns. Satisfies both schema robustness and deployment safety requirements.

## Position Summary

I withdrew 0 recommendations completely, modified 7 of 9 recommendations, and maintained 2 in original form. The most significant change in my thinking is acknowledging that schema design quality must be balanced with implementation timeline pressure and consumer migration complexity, rather than pursuing technical perfection without regard for practical constraints.

My original approach treated constitutional compliance (Principle XXVIII mechanical enforcement) as an absolute requirement that overrides practical concerns. The cross-review process revealed that constitutional principles must be satisfied within operational constraints, not despite them. Devils-advocate's warning about premature lock-in was particularly valuable—pushing for comprehensive v1.0.0 schema without field testing risks exactly the migration debt that motivated this spec.

My highest-priority surviving recommendation is the timeline-constrained schema staging approach. This preserves the core structural benefits that address the three production bugs while respecting the 2026-12-01 deadline and avoiding premature lock-in. The v0.1.0/v0.2.0 staging allows field testing to validate design decisions before constitutional commitments are locked in, addressing both devils-advocate's procedural concerns and engineer's timeline pressure.