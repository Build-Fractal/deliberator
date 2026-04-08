# Dispute Resolution: 001-Subject-Arbitration Blockers

After two full conversus cycles (v1: 30 recs, v2: 24 recs, 32 independent agents), the spec converged on architecture but 4 mechanism-level disputes remain. These block implementation.

## Blocker 1: "Dispute entry" definition

The trigger mechanism uses `<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->` markers in Phase 5 output. The engine must determine if disputes exist between the markers. What counts as a "dispute entry"?

- **Option A (pattern-match):** Any line matching `**Dispute:**` or similar bold-label pattern. Precise, prevents false positives from preamble text, but re-couples the primary trigger to Markdown formatting.
- **Option B (content-negative):** Any non-whitespace content that is not an HTML comment. Decoupled from formatting, but risks false positives from template artifacts.

## Blocker 2: Structured output — normative weight for v1

The spec defers full structured extraction to v2. For v1, what is the output contract?

- **Option A (headings only):** FR-018 section headings are the sole v1 contract. No prose conventions, no advisory schema.
- **Option B (headings + prose conventions):** FR-018 headings plus labeled sub-fields (`**Dispute:**`, `**Ruling:**`, etc.) as SHOULD-level template instructions.
- **Option C (headings + advisory schema):** FR-018 headings as v1 contract, plus a SHOULD-level schema definition in a standalone section for v2 planning.

## Blocker 3: Success criteria priority

10 new FRs (FR-022 through FR-027) have no success criteria. When must they be written?

- **Option A (P1):** Missing SCs are a spec-completeness defect that blocks implementation planning.
- **Option B (P2):** SCs should be added but FRs with RFC 2119 language are implementable without them.

## Blocker 4: Citation boundary enforcement surface

FR-024 says only `grounding` may be cited as authority. Where is this enforced?

- **Option A (spec-level):** FR-024 in the spec is sufficient. Extend FR-023 validation to check citation sources post-hoc.
- **Option B (template-level):** Add the citation constraint as a one-sentence instruction in the arbitration template. LLM agents see prompts, not specs.
- **Option C (both):** FR-024 in the spec + instruction in the template + FR-023 validation covers all surfaces.
