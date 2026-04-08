# Cooperative Review — Phase 1: Initial Utilization Review

**Agent**: functional-typing

---

### Executive Summary

Spec 011 introduces phase consensus gates as an orchestration layer over the existing conversus deliberation engine. The feature defines a `/conversus gate` subcommand that reads gate configuration, generates a standard `conversus.yml`, delegates to the run engine, and interprets the synthesis output to produce a pass/fail verdict. The design correctly separates gate orchestration from the deliberation engine, and the SKILL.md implementation at L1859-2156 faithfully implements most of the spec's 12 functional requirements.

From a structural correctness perspective, the implementation is largely sound. All 12 FRs have corresponding handler sections in the SKILL.md, exit codes are correctly defined (0/1/2), and the gate-result.md schema matches the spec. However, there are meaningful gaps in how the SKILL.md handles edge cases around preset expansion to multi-agent sets, the `max_disputes` criteria parsing, and the re-run attempt numbering when interleaved with multi-round output.

The most important recommendation is to formalize the minimum agent count validation after preset expansion, since the spec requires "at least 2 agents" (run engine validation at SKILL.md L209) but the gate's preset path could yield a single agent without a clear error message specific to the gate context.

### Alignment

- **Engine independence** (spec L56-57, SKILL.md L2127-2135): The gate generates standard `conversus.yml` configs and delegates to the run engine. The run engine has zero gate awareness. This cleanly satisfies FR-012 and preserves the engine's boundary.

- **Exit code mapping** (spec L47, SKILL.md L2039-2055): The three exit codes (0=PASS, 1=BLOCK, 2=ERROR) are correctly defined and match FR-008. The post-execution report templates at SKILL.md L2061-2112 include exit code indication.

- **Gate-result.md schema** (spec L48-49, SKILL.md L1972-2015): The structured document schema matches FR-009's requirements: phase name, artifact path, verdict, dispute count, dispute summaries, timestamp, and attempt number are all present. The `Output` field provides traceability to the full conversus output (FR-010).

- **Re-run behavior** (spec L53, SKILL.md L2114-2125): The attempt-based archival system preserves previous output by moving it to `attempt-N/` directories, satisfying FR-011's audit requirement.

- **Dispute-Parsing Subsystem integration** (spec L43, SKILL.md L1959): Step 6 of gate execution explicitly delegates to the Dispute-Parsing Subsystem for dispute counting, satisfying FR-007.

- **No interactive prompts** (spec L102, SKILL.md L1867): The handler explicitly states "No interactive prompts" and emphasizes declarative configuration, satisfying the CI/CD constraint.

### Missed Opportunities

- **Preset expansion validation gap**: SKILL.md L1924 states that a single-agent preset fails with a specific error, but does not address what happens when a composition list (e.g., `preset: [a, b]`) resolves to fewer than 2 agents after composition. The run engine validation at L209 catches this, but the error message will reference agent count without gate context. Impact: medium.

- **Pass criteria parsing specification**: SKILL.md L1926-1934 defines `max_disputes N` but does not specify how `N` is parsed (integer only? what if the user writes `max_disputes 1.5` or `max_disputes -1`?). The error message at L1934 does not cover malformed N values. Impact: medium.

- **Attempt number persistence**: SKILL.md L2118-2123 describes scanning for `attempt-*` directories to determine the next attempt number. It does not specify whether the scan is lexicographic or numeric. `attempt-10` would sort before `attempt-2` lexicographically. Impact: low.

- **Error verdict in gate-result.md**: SKILL.md L2005-2011 defines the `ERROR` verdict but does not specify what happens when the run engine itself fails partway through (e.g., agent timeout during Phase 3). Does a partial deliberation produce a `BLOCK` or `ERROR` result? Impact: medium.

- **Config-based vs. inline flag interaction**: SKILL.md L1877-1880 defines override flags (`--pass`, `--output`, `--mode`, `--rounds`) that apply to "both forms," but for config-based invocation, the interaction between the gate definition's values and the flag overrides is not explicitly specified. Does the flag override the config, or fail if both are present? Impact: medium.

- **Multi-target artifact support**: SKILL.md L1942 handles directory artifacts, but the spec at L41 says `<artifact-path>` (singular). There is no support for multiple artifact paths in a single gate invocation, which limits gates to single-directory or single-file targets. Impact: low.

### Off-Base Assumptions

- **Assumption: preset always resolves to a list of agents**: The spec at L65-66 shows `preset: review/thorough` used as a gate agent config. SKILL.md L1920 says the `agents` field supports preset reference as `agents: { preset: name }`. However, presets as defined in the run engine (SKILL.md L126-200) resolve to a single agent entry (name, prompt, docs), not a list of agents. The gate requires at least 2 agents, but a standard preset is a single-agent definition. The SKILL.md error at L1924 catches this, but the spec example at L65-66 implies `review/thorough` resolves to multiple agents, which contradicts the existing preset system. This is a spec-level confusion, not an implementation error.

- **Assumption: gates.yml is a new file format**: The spec at L31 says "A `gates` section in `conversus.yml` (or standalone `gates.yml`) MUST define phase gates." SKILL.md L1884-1889 implements this correctly. However, neither the spec nor the SKILL.md defines the validation rules for `gates.yml` as a standalone file format — is it just the `gates:` key at the root, or does it support other keys? This ambiguity could cause parsing issues.

### Actionable Recommendations

1. **Clarify preset-to-multi-agent expansion** (Priority: P1)
   - **Current state**: SKILL.md L1920-1924 assumes presets can expand to agent lists, but the preset system (L126-200) defines presets as single-agent definitions.
   - **Proposed change**: Add a note in the gate handler that for preset-based agent configuration, the gate either requires a multi-agent preset category or falls back to inline agent definitions. Alternatively, define "review presets" as a new preset category that expands to multiple agents.
   - **Rationale**: The spec example at L65-66 is unimplementable with the current preset system. Either the spec or the preset system needs to change.
   - **Risk if ignored**: Users will hit the "Gate requires at least 2 agents" error when using any existing preset, making preset-based gates unusable.

2. **Specify max_disputes N parsing rules** (Priority: P1)
   - **Current state**: SKILL.md L1926-1934 lists `max_disputes N` as a pass criteria but does not define N's validation.
   - **Proposed change**: Add: "N must be a positive integer (1 or greater). Non-integer, negative, or zero values fail with: 'max_disputes requires a positive integer. Got: {value}'.'"
   - **Rationale**: Without explicit parsing rules, implementations will handle edge cases inconsistently.
   - **Risk if ignored**: Invalid criteria values may silently produce incorrect gate verdicts.

3. **Define flag-override precedence for config-based gates** (Priority: P2)
   - **Current state**: SKILL.md L1877-1880 lists override flags but does not state precedence over gate config values.
   - **Proposed change**: Add: "When both a gate definition value and a CLI flag are provided, the CLI flag takes precedence. This allows temporary overrides without modifying gate configuration."
   - **Rationale**: CI/CD pipelines often need to override defaults per-run (e.g., `--pass always` for a dry run).
   - **Risk if ignored**: Ambiguous behavior when config and flags disagree.

4. **Specify attempt-number scanning as numeric** (Priority: P2)
   - **Current state**: SKILL.md L2118-2123 says "scan for existing attempt-* directories" without specifying sort order.
   - **Proposed change**: Add: "Scan `attempt-*` directories, parse the numeric suffix, and use max(suffix) + 1 as the next attempt number. Non-numeric suffixes are ignored."
   - **Rationale**: Lexicographic sorting breaks at attempt-10.
   - **Risk if ignored**: Incorrect attempt numbering after 9 re-runs.

5. **Define partial execution handling** (Priority: P2)
   - **Current state**: SKILL.md does not specify gate behavior when the run engine fails partway through.
   - **Proposed change**: Add: "If the run engine fails before producing a synthesis, the gate verdict is ERROR. If a synthesis exists but is incomplete (no dispute markers), the gate uses the Dispute-Parsing Subsystem's default behavior (treat as having disputes)."
   - **Rationale**: CI/CD pipelines need deterministic behavior on failure.
   - **Risk if ignored**: Ambiguous gate results on partial failures.

6. **Add gates.yml standalone validation** (Priority: P2)
   - **Current state**: Neither spec nor SKILL.md defines validation for `gates.yml` as a standalone file.
   - **Proposed change**: Add: "A standalone `gates.yml` must contain exactly one top-level key: `gates`. Any additional top-level keys fail with: 'Invalid gates.yml: unexpected key {key}. gates.yml must contain only the gates: section.'"
   - **Rationale**: Prevents confusion between `gates.yml` and `conversus.yml`.
   - **Risk if ignored**: Users may put run-engine keys in `gates.yml` and expect them to work.

7. **Validate max_disputes 0 equivalence** (Priority: P3)
   - **Current state**: `max_disputes 0` is not explicitly addressed. It would be logically equivalent to `converged` but is an odd way to express it.
   - **Proposed change**: Add: "max_disputes 0 is valid and equivalent to converged. Emit info: 'max_disputes 0 is equivalent to converged.'"
   - **Rationale**: Prevents user confusion without adding complexity.
   - **Risk if ignored**: Minor user confusion.

8. **Document the generated conversus.yml audit trail** (Priority: P3)
   - **Current state**: SKILL.md L1955 mentions writing the generated config for auditability but does not describe its format or whether it includes comments about the gate origin.
   - **Proposed change**: Add a YAML comment header: `# Generated by /conversus gate for phase: {phase}` and `# Source: {gates.yml or conversus.yml gates section}`.
   - **Rationale**: Aids debugging when reviewing gate output.
   - **Risk if ignored**: Minor inconvenience during debugging.

### Referenced Documentation

- `specs/011-phase-consensus-gates/spec.md` — sections/lines cited: L31, L41, L43, L47-49, L53, L56-57, L65-66, L102
- `SKILL.md` — sections/lines cited: L126-200, L209, L1859-1867, L1884-1889, L1920-1924, L1926-1934, L1942, L1955, L1959, L1972-2015, L2039-2055, L2061-2112, L2114-2125, L2127-2135, L2156
