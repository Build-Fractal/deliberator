# Cooperative Review — Phase 1: Initial Utilization Review

**Agent**: integration-architect

---

### Executive Summary

Spec 011 defines phase consensus gates as a new `/conversus gate` subcommand that provides CI/CD-friendly quality checks at workflow boundaries. The SKILL.md implementation (L1859-2156) implements this as a thin orchestration layer that generates standard conversus configs, delegates to the run engine, and interprets results. From an integration architecture perspective, this is well-designed: it reuses the existing engine, preset system, and Dispute-Parsing Subsystem rather than introducing parallel infrastructure.

The FR-to-implementation mapping is complete — all 12 FRs have corresponding SKILL.md sections. The success criteria (SC-001 through SC-006) are verifiable through the implemented flow. The dispatch routing at SKILL.md L34 correctly adds `gate` to the subcommand table. However, the integration surfaces reveal gaps: the gate handler's interaction with the multi-round system is underspecified, the generated `conversus.yml` does not include all features the run engine supports (notably `stagnation`, `iterations`, and `prior`), and the Dispute-Parsing Subsystem integration lacks error propagation semantics.

The most important recommendation is to define explicit error propagation from the Dispute-Parsing Subsystem to the gate verdict, since a parsing failure currently defaults to "has disputes" (L773) but the gate needs to distinguish between "disputes exist" and "could not determine."

### Alignment

- **FR-001 to FR-004 — Gate Configuration** (spec L31-37, SKILL.md L1882-1915): The gate definition schema correctly maps all configuration fields. The `gates.yml` / `conversus.yml` precedence rule (L1889) is explicit. Each gate defines phase name, agents, pass criteria, and optional fields (mode, rounds, arbiter, output).

- **FR-005 — Config-based execution** (spec L41, SKILL.md L1936-1963): The 8-step execution flow covers gate lookup, artifact validation, re-run handling, config generation, engine delegation, result parsing, gate-result writing, and reporting. This is a thorough implementation.

- **FR-006 — Inline execution** (spec L42, SKILL.md L1965-1970): Inline gates construct an ad-hoc gate definition and follow the same execution path, satisfying the one-off quality check requirement.

- **FR-007 — Dispute-Parsing integration** (spec L43, SKILL.md L1959): Step 6 delegates dispute counting to the subsystem defined at L750-777, which provides both boolean and integer outputs needed for pass criteria evaluation.

- **FR-008 — Exit codes** (spec L47, SKILL.md L2039-2055): Exit codes 0/1/2 are correctly mapped to PASS/BLOCK/ERROR. The post-execution reports (L2061-2112) include exit code indication.

- **FR-012 — Engine independence** (spec L56-57, SKILL.md L2127-2135): The gate generates standard configs and the run engine processes them without gate awareness. The generated `conversus.yml` is a valid standalone config.

### Missed Opportunities

- **Missing stagnation config in generated conversus.yml**: SKILL.md L1946-1954 shows the generated config template, which omits the `stagnation` field. Since gates can run with `rounds > 1`, stagnation detection should be configurable or defaulted. The run engine defaults stagnation to `detect` (L229), but explicitly including it in the generated config improves auditability. Impact: medium. [SKILL.md L229, L1946-1954]

- **Missing iterations config in generated conversus.yml**: The generated config at SKILL.md L1946-1954 omits `iterations`. Multi-iteration cross-review/revision cycles could improve gate deliberation quality, but there is no way to configure this in gate definitions. Impact: medium. [SKILL.md L370-380, L1946-1954]

- **No prior context support for gates**: Gates cannot specify `prior` files in their configuration. If a gate is re-run after a failed attempt, the new deliberation has no access to the previous attempt's synthesis — it starts fresh. Feeding the prior attempt's synthesis as `prior` context would improve re-run quality. Impact: high. [SKILL.md L120-124, L1891-1914]

- **Dispute-Parsing error propagation**: The Dispute-Parsing Subsystem defaults to "has disputes" when parsing fails (L773). For gate verdicts, this means a parsing failure produces a BLOCK verdict rather than an ERROR verdict. The gate should distinguish between "disputes exist" and "parsing failed." Impact: high. [SKILL.md L773, L2005-2007]

- **No gate-level arbiter defaults**: The gate schema (L1908-1913) supports arbiter configuration but does not provide defaults. For strict gates (`pass: converged`), an arbiter is valuable for resolving disputes that would otherwise block the gate. A default arbiter configuration for strict gates would reduce configuration burden. Impact: medium. [SKILL.md L1908-1913]

- **No gate chaining**: Gates operate independently. There is no mechanism to chain gates (e.g., spec gate must pass before plan gate runs). This is a workflow concern rather than a gate concern, but the lack of any mention of it in the spec or SKILL.md means users will need to implement chaining externally. Impact: low. [spec L59-83]

- **Generated conversus.yml location**: SKILL.md L1955 writes the generated config to `{output}/conversus.yml`, but if the run engine searches for `conversus.yml` in the working directory (L52), the generated config in the output directory would not be found. The gate execution (Step 5, L1957) proceeds directly to Run: Execution Step 1, so the file is used by reference, not by discovery — but this should be explicit. Impact: low. [SKILL.md L50-53, L1955-1957]

### Off-Base Assumptions

- **Assumption: preset resolves to multiple agents for gates**: Spec L65-66 shows `preset: review/thorough` as a gate agent config, implying this preset expands to multiple agents. However, the preset system (SKILL.md L126-200) resolves presets to single-agent definitions. The SKILL.md gate handler at L1924 catches this with an error, but the spec example is misleading. The correct understanding is that current presets are single-agent, and a multi-agent preset category would need to be defined separately.

- **Assumption: gates.yml is fully specified**: The spec mentions `gates.yml` as a standalone file (L31) but provides no schema validation rules beyond the `gates:` key structure. The SKILL.md (L1884-1889) implements precedence (gates.yml over conversus.yml gates section) but does not validate the standalone file format. Standalone `gates.yml` should be treated as a YAML file with a single `gates:` top-level key.

### Actionable Recommendations

1. **Add Dispute-Parsing error propagation to gate verdict** (Priority: P1)
   - **Current state**: SKILL.md L773 defaults to "has disputes" on parsing failure. Gate step 6 (L1959) uses the subsystem output for verdict.
   - **Proposed change**: Add to Step 6: "If the Dispute-Parsing Subsystem encounters a parse error (markers absent AND heading not found), the gate verdict is ERROR with exit code 2, not BLOCK. The gate-result.md Verdict field is ERROR and the Disputes section contains a single bullet: 'Synthesis output could not be parsed for disputes.'"
   - **Rationale**: A BLOCK verdict implies the deliberation ran correctly but found issues. A parse failure is a system error, not a quality finding.
   - **Risk if ignored**: CI/CD pipelines cannot distinguish between "artifact has quality issues" and "gate infrastructure failed."

2. **Include stagnation and iterations in gate config schema** (Priority: P1)
   - **Current state**: Gate definition schema (SKILL.md L1891-1914) omits stagnation and iterations fields.
   - **Proposed change**: Add optional fields: `stagnation: detect | ignore` (default: `detect`), `iterations: N` (default: 1). Pass these through to the generated conversus.yml.
   - **Rationale**: Without these, multi-round gates cannot use stagnation detection, and no gate can use multi-iteration depth — both are core engine features.
   - **Risk if ignored**: Gates with `rounds > 1` run without stagnation detection, potentially wasting resources.

3. **Support prior context for gate re-runs** (Priority: P2)
   - **Current state**: Re-runs (SKILL.md L2114-2125) archive previous output but do not feed it as context to the new run.
   - **Proposed change**: Add optional behavior: when re-running a gate (attempt > 1), automatically set `prior: [{output}/attempt-{N-1}/summary/final.md]` in the generated config. This is opt-in via a gate config flag: `prior_on_rerun: true` (default: false).
   - **Rationale**: Re-run deliberations benefit from knowing what the previous attempt found, avoiding re-discovery of the same issues.
   - **Risk if ignored**: Re-runs are independent deliberations that may repeat the same findings, wasting time.

4. **Formalize SC-001 through SC-006 verification paths** (Priority: P2)
   - **Current state**: Success criteria in the spec (L89-94) are human-readable but not mapped to SKILL.md verification points.
   - **Proposed change**: Add a verification mapping table in the spec or SKILL.md:
     - SC-001 → Gate execution step 6 + pass criteria `converged` (L1959, L1930)
     - SC-002 → Preset resolution (L126-200) + gate agent expansion (L1920)
     - SC-003 → Inline execution path (L1965-1970)
     - SC-004 → Exit codes section (L2039-2055)
     - SC-005 → Re-run behavior (L2114-2125)
     - SC-006 → Pass criteria `max_disputes` (L1931)
   - **Rationale**: Explicit mapping from success criteria to implementation enables verification without full-document analysis.
   - **Risk if ignored**: SC verification requires reading the entire SKILL.md to trace requirements.

5. **Define explicit flag-override behavior** (Priority: P2)
   - **Current state**: SKILL.md L1877-1880 lists override flags but does not state whether they override or conflict with gate config values.
   - **Proposed change**: Add: "CLI flags override gate configuration values. This is consistent with standard CLI convention (explicit flags beat file-based defaults)."
   - **Rationale**: Standard CLI convention and CI/CD pipeline flexibility require explicit override semantics.
   - **Risk if ignored**: Ambiguous behavior when both config and flags specify the same field.

6. **Add validate_templates pass-through** (Priority: P2)
   - **Current state**: The generated conversus.yml (L1946-1954) does not include `validate_templates`. Gate-generated configs should validate templates by default.
   - **Proposed change**: Add `validate_templates: true` to the generated config template. Allow gate config to override with `validate_templates: false`.
   - **Rationale**: Template validation catches config errors before agent launches. Gates running in CI/CD especially benefit from early failure.
   - **Risk if ignored**: Template errors in gate runs only surface after agent launches, wasting resources.

7. **Clarify generated config is passed by reference** (Priority: P3)
   - **Current state**: SKILL.md L1955-1957 writes the generated config and then proceeds to run engine execution. It is unclear whether the run engine reads the written file or uses the in-memory config.
   - **Proposed change**: Add: "The gate handler writes the generated config to {output}/conversus.yml for auditability, then proceeds to run engine execution using the in-memory config. The run engine does not re-read the file."
   - **Rationale**: Eliminates ambiguity about whether the file is an artifact or an input.
   - **Risk if ignored**: Minor confusion during debugging.

8. **Specify max_disputes N validation** (Priority: P3)
   - **Current state**: `max_disputes N` parsing at SKILL.md L1926-1934 does not specify N's type or range constraints.
   - **Proposed change**: Add: "N must be a non-negative integer. Non-integer values fail with: 'max_disputes requires a non-negative integer. Got: {value}'.'" Note: 0 is allowed and is equivalent to `converged`.
   - **Rationale**: Explicit type validation prevents runtime surprises.
   - **Risk if ignored**: Edge case errors with non-integer values.

### Referenced Documentation

- `specs/011-phase-consensus-gates/spec.md` — sections/lines cited: L31, L37, L41-43, L47-49, L53, L56-57, L59-83, L65-66, L89-94, L102
- `SKILL.md` — sections/lines cited: L34, L50-53, L120-124, L126-200, L209, L229, L370-380, L750-777, L773, L1859-1867, L1877-1880, L1882-1915, L1920-1924, L1926-1934, L1936-1963, L1942, L1946-1954, L1955-1957, L1959, L1965-1970, L1972-2015, L2005-2007, L2039-2055, L2061-2112, L2114-2125, L2127-2135
