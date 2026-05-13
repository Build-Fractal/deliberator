# Schema Design Expert Review — v4.2.0 Structured Deliberation Outputs

## Executive Summary

The v4.2.0 spec proposes migrating conversus deliberation outputs from markdown to XML schema with structured validation. The core motivation is solid—three concrete production bugs (prompt overflow, cross-review persistence quirks, silent trigger failures) stem directly from parsing display text rather than structured data. The proposed schema correctly identifies the six output types and establishes a reasonable common envelope pattern.

However, the schema design contains several critical gaps: insufficient identity fields in the envelope, underspecified field constraints, and no handling of XML's syntactic challenges with agent prose content. The format choice analysis is superficial—XSD as "strawman" ignores significant tooling ecosystem and validation expressiveness differences. The versioning approach correctly adopts SemVer but lacks concrete bump policies for common schema evolution scenarios.

**Most important recommendation**: Switch from XSD to JSON Schema as the canonical format to eliminate XML syntax conflicts with agent prose content while maintaining structural validation strength.

## Alignment

- **Common envelope pattern** (`spec.md` L254-264): The `<conversus-output>` wrapper with namespace, schema_version, and output_type enum correctly establishes the foundational identity structure that enables downstream consumers to parse outputs deterministically.

- **Severity enum constraint** (`spec.md` L275): The `severity="blocking|substantive|nit"` enum on concern points provides the structural discrimination needed to route blocking concerns into dispute sets for phase 2, addressing the production bug where severity lived in prose.

- **Reference linking mechanism** (`spec.md` L290): The `ref` attribute pattern (`<point ref="S1">`) enables phase 5 synthesis to trace dispute lineage back to phase 1 origins, providing the structural queries needed for cross-phase analysis.

- **Structural dispute detection** (`spec.md` L335-340): Replacing grep-based `DISPUTES_BEGIN/END` markers with XPath `count(/conversus-output/synthesis/disputes/dispute[@severity='blocking']) > 0` eliminates the prose drift vulnerability that caused silent trigger failures in v4.1.0.

## Missed Opportunities

- **Type-safe field constraints**: The schema defines string fields like `<topic>` and `<rationale>` without length limits, format constraints, or required content patterns. JSON Schema's `minLength`, `maxLength`, and `pattern` properties could enforce non-empty content and prevent degenerate cases. **Impact: high**.

- **Namespace versioning strategy**: The schema uses a single namespace `https://build-fractal.org/conversus/schema/v1` but provides no mechanism for namespace evolution across MAJOR versions. A versioned namespace pattern (`/v1`, `/v2`) would enable schema consumers to declare version compatibility ranges. **Impact: medium**.

- **Extensibility anchor points**: The schemas are closed—no extension points for future mode-specific attributes (e.g., red-blue mode's role discrimination) or plugin-contributed metadata. JSON Schema's `additionalProperties: false` with explicit extension objects would allow controlled extensibility. **Impact: medium**.

- **Cross-reference validation**: The `ref` attributes reference other elements by ID but the schema doesn't validate referential integrity. JSON Schema's `$ref` mechanism or XSD's `IDREF` types could catch broken references at validation time. **Impact: high**.

- **Enum validation across contexts**: Output types use string enums but different phases accept different verdict vocabularies. The schema should validate that `<recommendation>` values in phase 1 match the allowed set for that phase, distinct from arbitration verdict enums. **Impact: medium**.

- **Content model precision**: The schemas allow arbitrary text content in most elements. JSON Schema's content validation (e.g., `format: "date-time"` for timestamps, `format: "uri"` for file paths) would catch malformed data at write time. **Impact: medium**.

- **Composition patterns**: The `<revision>` type needs to handle multiple iterations but the schema doesn't specify whether this is achieved via multiple files or repeated elements. A clear composition strategy would eliminate implementation ambiguity. **Impact: low**.

## Off-Base Assumptions

- **XSD as XML validation gold standard** (`spec.md` L175): The spec assumes XSD is the natural choice for XML validation, but modern schema validation has moved toward JSON Schema even for XML content validation via transformation layers. XSD's complexity and poor error messages make it unsuitable for agent-output validation where clear failure diagnostics are critical.

- **XML syntax compatibility with agent prose** (`spec.md` L280-300): The spec assumes agent prose content can be safely embedded in XML elements without syntax conflicts. Agent outputs routinely contain `<`, `>`, `&` characters in code examples, mathematical expressions, and structured text that would require CDATA escaping or entity encoding, complicating both generation and parsing.

- **Namespace stability across versions** (`spec.md` L260): The spec uses a single namespace URI but claims SemVer versioning. XML namespaces are identity mechanisms—changing the namespace breaks all existing consumers, making MAJOR version upgrades impossible without coordinated migration.

## Actionable Recommendations

1. **Switch to JSON Schema canonical format** (Priority: P1)
   - **Current state**: `spec.md` L175-180 proposes XSD as strawman with "product-choice" flexibility.
   - **Proposed change**: Mandate JSON Schema as canonical format; emit JSON rather than XML for deliberation outputs.
   - **Rationale**: Eliminates XML syntax conflicts with agent prose, provides superior validation expressiveness, and integrates cleanly with Python Pydantic models for runtime validation.
   - **Risk if ignored**: Ongoing XML escaping bugs, poor validation error messages, and tooling compatibility issues.

2. **Add required identity fields to envelope** (Priority: P1)
   - **Current state**: `spec.md` L254-264 envelope omits deliberation stage, parent commit SHA, and engine version.
   - **Proposed change**: Add `deliberation_stage`, `engine_version`, and `source_commit` as required envelope fields.
   - **Rationale**: Downstream consumers need full identity context for audit trails and cross-stage analysis.
   - **Risk if ignored**: Ambiguous output provenance in multi-stage deliberations and debugging failures.

3. **Specify field-level validation constraints** (Priority: P1)
   - **Current state**: `spec.md` L275-340 defines string fields without length or format constraints.
   - **Proposed change**: Add `minLength: 1`, `maxLength: 2048` bounds; require non-empty content for critical fields.
   - **Rationale**: Prevents degenerate outputs (empty rationales, zero-content summaries) that break downstream processing.
   - **Risk if ignored**: Silent validation passes for malformed agent outputs.

4. **Design namespace versioning strategy** (Priority: P2)
   - **Current state**: `spec.md` L260 uses single namespace URI across all schema versions.
   - **Proposed change**: Use versioned namespaces `/schema/v1`, `/schema/v2` with explicit compatibility declarations.
   - **Rationale**: Enables MAJOR version schema evolution without breaking existing consumers.
   - **Risk if ignored**: Impossible to ship breaking schema changes; locked into v1 design decisions permanently.

5. **Add cross-reference integrity validation** (Priority: P2)
   - **Current state**: `spec.md` L290 uses `ref` attributes without referential integrity checks.
   - **Proposed change**: Define ID/IDREF constraints to validate that all `ref` attributes point to existing elements within the same output.
   - **Rationale**: Catches broken cross-references at validation time rather than runtime failures in downstream consumers.
   - **Risk if ignored**: Silent reference failures in phase 5 synthesis lineage tracing.

6. **Define concrete SemVer bump policies** (Priority: P2)
   - **Current state**: `spec.md` L360-370 defines MAJOR/MINOR/PATCH semantics abstractly.
   - **Proposed change**: Specify exact scenarios: adding optional fields = MINOR, adding required fields = MAJOR, changing enum values = MAJOR.
   - **Rationale**: Eliminates interpretation ambiguity when schema evolution decisions arise.
   - **Risk if ignored**: Inconsistent versioning decisions across maintainers; consumer compatibility breakage.

7. **Add extension points for mode-specific data** (Priority: P2)
   - **Current state**: Schemas are closed with no provision for mode-specific extensions.
   - **Proposed change**: Add optional `mode_metadata` object in envelope for mode-specific attributes.
   - **Rationale**: Supports red-blue mode role attributes and future mode innovations without schema breakage.
   - **Risk if ignored**: Mode-specific features require invasive schema changes or external sidecar files.

8. **Specify content encoding handling** (Priority: P3)
   - **Current state**: No explicit handling of special characters in agent prose content.
   - **Proposed change**: If retaining XML, mandate CDATA sections for prose fields; if switching to JSON, specify Unicode normalization.
   - **Rationale**: Prevents syntax errors when agents output code examples or mathematical expressions.
   - **Risk if ignored**: Periodic parsing failures on outputs containing XML-reserved characters.

9. **Define validation error reporting format** (Priority: P3)
   - **Current state**: `spec.md` L180 mentions "specific error path" but doesn't define error message structure.
   - **Proposed change**: Specify error object schema with `field_path`, `error_code`, and `human_message` properties.
   - **Rationale**: Enables consistent error handling across validation implementations and clear debugging output.
   - **Risk if ignored**: Inconsistent validation error quality; difficult debugging for malformed outputs.

## Referenced Documentation

*Note: No specific documentation files were provided for this review. Recommendations are based on general schema design expertise and analysis of the target specification.*