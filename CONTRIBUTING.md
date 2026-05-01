# Contributing to Conversus

This file collects authoring conventions and contribution guidance for
Conversus. The constitutional invariants live in
[`CONSTITUTION.md`](./CONSTITUTION.md); this document is the home for
operational guidance — judgment calls, rules of thumb, and authoring
conventions that benefit from being recommended uniformly without
being constitutionalized.

When the two diverge, the constitution governs. Operational guidance
SHOULD be followed unless a specific case justifies deviating; the
constitution MUST be followed unless an explicit, documented amendment
process changes it.

## Authoring Conventions

### Scripts Over Markdown (formerly Constitutional Principle VI)

Prefer executable scripts over static markdown when the artifact
drives behavior. If a document is consumed by automation or agents
to make decisions, it SHOULD be a script, config, or structured data
— not prose that must be parsed ambiguously.

- Orchestration logic SHOULD live in SKILL.md (executable spec) and
  templates (parameterized prompts), not in freeform documentation.
- Configuration SHOULD live in YAML (`conversus.yml`, preset files),
  not in markdown tables or inline instructions.
- When a markdown artifact exists purely for human orientation
  (quickstart, README), markdown is appropriate. When it drives
  agent behavior, prefer structured and executable formats.

The preference is operational guidance rather than a constitutional
invariant because the qualifier "when the artifact drives behavior"
requires interpretation in every application — the judgment call
"is this artifact driving behavior?" cannot be mechanized into a CI
lint without producing a long-tail of false positives and false
negatives. The discipline is real, but it lives here as a SHOULD
rather than a MUST so that contributors apply judgment in context
rather than being held to a check that doesn't exist and (under the
v2.4.0 Constitutional Inclusion Criteria) cannot be built.

### Output Conventions (cross-reference)

Authoring guidance for clean, readable output across CLI, MCP, and
plugin surfaces lives in [`docs/output-conventions.md`](./docs/output-conventions.md)
(formerly Constitutional Principle X). New output-emitting code
SHOULD follow those conventions; departures SHOULD be justified in
the change's PR description.

---

*Migrated from CONSTITUTION.md Principle VI in v2.6.0 → v3.0.0 per
spec 070 cycle 2 (2026-05-01).*
