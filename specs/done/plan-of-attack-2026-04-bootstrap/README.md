# Plan-of-attack — 2026-04 bootstrap deliberation

**Status:** Historical artifact. Closed 2026-04 (pre-methodology).
**Type:** Pre-conversus-methodology multi-agent deliberation.
**Why preserved:** Documents the bootstrap process that produced the early conversus methodology, which has since been formalized through specs 067 (four-stage verification) + 069/070 (tier extraction).

## What this is

Five-agent deliberation (`architect`, `builder`, `product`, `strategist`, `summary`) on early plan-of-attack questions for conversus. Produced before conversus had its own deliberation engine, using a Cline-style coding agent that interleaved tool-use markup with file output.

The interleaving meant agent outputs originally contained Cline tool-use wrappers (`<write_to_file>`, `<path>`, `<content>`, `<antArtifact>`) inline with file content. The wrappers were stripped during the 2026-05-20 OSS-launch cleanup pass; the agent-produced text is preserved.

## What this is NOT

- Not a ratified deliberation under the current four-stage protocol (spec 067).
- Not a regression-corpus deliberation — it predates the v4.2.0 schema work.
- Not authoritative for any current spec.

## Why we kept it instead of deleting it

Conversus's current methodology was built on learnings from bootstrap runs like this one. Shipping the bootstrap artifact alongside the formalized methodology shows the project's evolution honestly. It also serves as a counter-example: this is what conversus deliberation looked like *before* the engine, the schemas, the linters, and the four-stage protocol existed.

If you arrived here looking for "how conversus deliberations work today," see [`specs/067-verification-methodology`](../067-verification-methodology) and the [`deliberations/`](../../../deliberations) archive of ratified outputs instead.

## Provenance

- Author: pre-conversus run by an early contributor
- Tool: Cline-style coding agent (not conversus engine)
- Date: 2026-04
- Cleanup: 2026-05-20 (Cline tool-use wrappers stripped, home-path leakage scrubbed)
