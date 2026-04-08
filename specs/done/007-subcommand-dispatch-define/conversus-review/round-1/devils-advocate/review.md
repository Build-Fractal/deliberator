# Devil's Advocate Review: 007-subcommand-dispatch-define

## Executive Summary

Spec 007 introduces subcommand dispatch to conversus and adds `/conversus define`, which takes natural-language input and produces a structured `problem.md`. The dispatch mechanism is clean and minimal -- a routing table in SKILL.md, backward-compatible defaulting to `run`, and a clear error for unknown subcommands. The `/conversus define` handler is a reasonable first guided command: it takes the user from vague intent to structured artifact without requiring YAML knowledge or game-theory literacy. The SKILL.md implementation appears to match the spec's 12 FRs and 5 success criteria faithfully.

My concern is not with what the spec says, but with what it leaves unchallenged. The spec treats `problem.md` as a freestanding artifact with no validation contract, no versioning hook, and no degradation model for downstream consumers. It also embeds several assumptions about user behavior and problem taxonomy that deserve scrutiny -- not because they are obviously wrong, but because they have been accepted without stress-testing. The spec's simplicity is its strength, but simplicity that has not been challenged is indistinguishable from incompleteness.

My most important recommendation: define what happens when `problem.md` is malformed, incomplete, or stale when consumed by `/conversus interests` (spec 008) -- because right now, nothing in the contract prevents a garbage-in-garbage-out cascade through the entire guided workflow.

## Alignment

- **[Backward-compatible dispatch]** (spec L29, L88): FR-003 defaults no-argument invocation to `run`, and constraint C2 (L88) explicitly gates the dispatch as additive-only. This aligns with the conversus principle that new features must not break existing behavior -- the same principle enforced in SKILL.md's rounds, presets, and arbitration features, all of which use optional fields with backward-compatible defaults. [SKILL.md, L356: "the flow is identical to the current system. Full backward compatibility."]

- **[Structured ambiguity marking]** (spec L39, L65-66): FR-010's `[CLARIFY: ...]` tags provide a machine-parseable signal that a field is uncertain. This is a direct analogue to the dispute-parsing subsystem's structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`) -- both establish grep-friendly contracts between producers and consumers. [SKILL.md, L750-751]

- **[Non-expert entry point]** (spec L15-16, L87): The constraint that `/conversus define` "Must NOT require coding knowledge to use" directly serves the guided-workflow thesis stated across specs 007-010. The spec correctly positions `define` as the first step in a progressive disclosure chain. [spec.md, L87]

- **[Problem type taxonomy]** (spec L37-38): The four-type classification (`selection`, `integration`, `scoping`, `stress-test`) maps 1:1 to the mode decision matrix in spec 008 (FR-007). This is deliberate -- the taxonomy was designed to feed downstream mode inference. The alignment is structural, not accidental. [008 spec.md, L44-52]

- **[Existing-file safeguard]** (spec L40): FR-011 requires explicit user consent before overwriting `problem.md`. This matches the pattern established by spec 008's FR-005 and FR-012 for `interests.md` and `conversus.yml` respectively -- the guided workflow consistently avoids silent overwrites. [SKILL.md, L787-793]

## Missed Opportunities

- **[No schema validation for problem.md consumers]**: The spec defines a `problem.md` schema (L44-71) but provides no validation contract for downstream consumers. Spec 008's `/conversus interests` will read `problem.md` -- what happens if the Type field is missing? If the Decision is multi-sentence? If `[CLARIFY:]` tags remain unresolved? The spec punts all of this to 008, but the validation responsibility belongs at the boundary: the producer should guarantee what the consumer requires. The `[CLARIFY:]` tags are particularly dangerous -- the spec never says that downstream commands should refuse to proceed when clarifications remain unresolved. Impact: **high**. [spec.md, L44-71; 008 spec.md, L31]

- **[No idempotency guarantee for `define`]**: FR-011 handles the "file already exists" case (L40), but only through user interaction. There is no `--force` flag, no `--dry-run` mode, no deterministic behavior for scripted or automated invocations. If `/conversus define` is ever called from a gate (spec 011) or a CI pipeline, the interactive prompt blocks indefinitely. The spec assumes a human is always present. Impact: **medium**. [spec.md, L40; 011 spec.md, L104-106]

- **[No problem.md versioning or staleness detection]**: Spec 008's FR-013 (L59) explicitly tracks staleness between `interests.md` and `conversus.yml`. But no equivalent mechanism exists between `problem.md` and `interests.md`. If the user refines `problem.md` after running `/conversus interests`, the interests become stale with no warning. The spec should at least define a timestamp or hash field in `problem.md` that downstream consumers can check. Impact: **medium**. [008 spec.md, L59]

- **[`--context` accepts only a single path]**: FR-006 says `--context <path>` reads "context documents" but the syntax is singular (L35). Context ingestion (SKILL.md L797-802) says "path may be a file or directory" which handles the multi-file case via directory resolution, but there is no way to specify multiple individual files from different directories. The `run` engine supports list-based targets (SKILL.md L57-68); `define` should too. Impact: **low**. [spec.md, L35; SKILL.md, L57-68, L797]

- **[No explicit error path for unreadable context documents]**: FR-006 says the command "MUST read context documents" but does not specify behavior when a context path does not exist or is unreadable. The `run` engine validates all `TARGET_FILES` exist (SKILL.md L195) and all `docs` paths exist (L196). The `define` handler should apply the same validation rigor. Impact: **medium**. [spec.md, L35-36; SKILL.md, L195-196]

- **[Problem type taxonomy is closed without escape hatch]**: FR-008 (L37) restricts types to exactly four values. The ambiguity clause allows marking a best guess, but there is no mechanism for a user or downstream consumer to add a custom type. If a problem genuinely does not fit any of the four categories (e.g., "prioritization" -- ranking N items by value, distinct from "selection" which chooses one), the system forces a misclassification. The taxonomy may be correct today, but the spec does not acknowledge its own closure as a conscious design choice vs. an oversight. Impact: **low**. [spec.md, L37-38]

- **[No explicit constraint on problem.md size or complexity]**: The schema allows unbounded Constraints and Open Questions sections. A user who provides a 50-page context document could generate a `problem.md` with 200 constraints. Downstream consumers (interests, mode) ingest this artifact in full -- there is no complexity budget. The `run` engine has implicit bounds (2-5 agents, 1-5 rounds), but the guided workflow's input artifact has none. Impact: **low**. [spec.md, L44-71]

## Off-Base Assumptions

- **[Users will resolve [CLARIFY:] tags before proceeding]** (spec L39, L81): The spec assumes that `[CLARIFY:]` tags create a natural pause point where users will edit `problem.md` before running `/conversus interests`. Nothing enforces this. The report (SKILL.md L872-875) warns about clarifications, but `/conversus interests` (spec 008 FR-001) reads `problem.md` unconditionally -- it does not check for unresolved `[CLARIFY:]` tags. The user workflow is: run `define`, see the warning, ignore it, immediately run `interests`. The spec treats `[CLARIFY:]` as a gate; the implementation treats it as decoration. Either the downstream consumer must enforce the gate, or the spec should acknowledge that `[CLARIFY:]` tags are advisory, not blocking.

- **[The four problem types are exhaustive]** (spec L37-38, L52): The spec presents `selection`, `integration`, `scoping`, and `stress-test` as a complete taxonomy without justifying its completeness. Real decisions include: prioritization (ranking, not choosing), migration (transitioning from A to B, not choosing between them), compliance (checking against external constraints), and decomposition (breaking a monolith into parts). Some of these can be shoe-horned into existing types, but the shoe-horning is itself a design decision that the spec does not discuss. The spec 008 mode matrix (L44-52) maps types 1:1 to modes, so a missing type means a missing mode pathway -- the taxonomy is load-bearing, not cosmetic.

- **[Interactive fallback is always available]** (spec L41, FR-012): FR-012 assumes that when no description and no `--context` are provided, the agent can ask clarifying questions interactively. This is true in a conversational agent context but may not hold in all runtimes. The SKILL.md compatibility note (L11-13) says conversus "requires an agent runtime that supports background Agent tool dispatch" -- but interactive questioning requires a different capability (synchronous user-input). The spec conflates "can dispatch agents" with "can hold a conversation with the user." In practice this works because the orchestrator is the conversational agent, but the assumption is implicit rather than stated.

## Actionable Recommendations

1. **Add [CLARIFY:] gate to spec 008** (Priority: P1)
   - **Current state**: Spec 007 produces `[CLARIFY:]` tags (L39, L65-66). Spec 008 reads `problem.md` unconditionally (008 FR-001).
   - **Proposed change**: Add to spec 007 section 2 or to spec 008 FR-001: "If `problem.md` contains unresolved `[CLARIFY:]` tags, `/conversus interests` MUST present them and ask the user to resolve them before proceeding. Unresolved clarifications produce unreliable interest discovery."
   - **Rationale**: The `[CLARIFY:]` tag system is the spec's primary mechanism for handling ambiguity. If downstream consumers ignore it, the mechanism is theater. The guided workflow promises non-expert users reliable outcomes -- delivering garbage interests from an ambiguous problem definition violates that promise. [spec.md, L39; 008 spec.md, L31]
   - **Risk if ignored**: Users will routinely skip clarification. `/conversus interests` will generate agents from vague problem definitions, producing low-quality prompts that waste deliberation tokens and produce meaningless results. The failure mode is silent -- the output looks like a valid `interests.md` but is grounded in nothing.

2. **Define problem.md validation contract** (Priority: P1)
   - **Current state**: The spec defines the schema (L44-71) but no validation rules for consumers.
   - **Proposed change**: Add a "problem.md Validation" subsection to spec 007 specifying: Decision must be exactly one sentence. Type must be one of the four enumerated values. Context must be 2-4 sentences. Constraints must be a bulleted list with at least one entry. Source Documents must list at least one path or contain the "(none)" sentinel. Any consumer of `problem.md` MUST validate these constraints before proceeding.
   - **Rationale**: The `run` engine validates every config field before execution (SKILL.md L192-222). The guided workflow should apply the same discipline to its artifacts. A `problem.md` that violates its own schema is a silent failure. [SKILL.md, L192-222; spec.md, L44-71]
   - **Risk if ignored**: Downstream commands will encounter malformed `problem.md` files and either crash (bad) or silently produce degraded output (worse). Every guided-workflow command becomes responsible for its own ad-hoc validation, leading to inconsistent behavior.

3. **Add staleness tracking between problem.md and interests.md** (Priority: P2)
   - **Current state**: Spec 008 FR-013 tracks staleness between `interests.md` and `conversus.yml` (008 L59). No equivalent exists for the `problem.md` to `interests.md` boundary.
   - **Proposed change**: Add a `## Generated From` section to the `interests.md` schema (spec 008) containing the path and modification timestamp of the `problem.md` used to generate it. `/conversus mode` checks this timestamp against the current `problem.md` and warns if stale.
   - **Rationale**: Spec 008 already established the staleness-detection pattern. Omitting it at the first boundary is an inconsistency that will confuse users who modify their problem definition and expect downstream artifacts to reflect the change. [008 spec.md, L59]
   - **Risk if ignored**: Users refine `problem.md`, run `mode`, and get a `conversus.yml` based on stale interests derived from the old problem definition. The error is invisible until the deliberation produces irrelevant results.

4. **Acknowledge taxonomy closure as a design decision** (Priority: P2)
   - **Current state**: FR-008 lists four types as if exhaustive (L37-38). No rationale for why these four and not others.
   - **Proposed change**: Add a "Design Note" after the type table (L52): "This taxonomy is intentionally closed. Problems that do not fit these types (e.g., prioritization, migration, compliance) should be reframed in terms of the closest type, or users should bypass `define` and write `conversus.yml` directly. The taxonomy may be extended in a future spec if patterns emerge."
   - **Rationale**: A closed taxonomy is a valid design choice, but only if it is acknowledged. Without acknowledgment, future maintainers will not know whether to extend the list or reframe edge cases. The spec should state its intent so the decision can be challenged or upheld on its merits. [spec.md, L37-38, L52]
   - **Risk if ignored**: Future specs will silently extend the taxonomy without understanding the downstream impact (every type maps 1:1 to a mode in spec 008). Alternatively, users will encounter problems that do not fit and assume the tool is broken rather than understanding the intended escape hatch.

5. **Support multiple --context paths** (Priority: P2)
   - **Current state**: FR-006 accepts `--context <path>` as a single path (L35). Directory resolution provides multi-file support only if files are co-located.
   - **Proposed change**: Allow `--context` to be specified multiple times: `/conversus define --context specs/001/spec.md --context docs/architecture.md`. Resolve each path independently (file or directory).
   - **Rationale**: The `run` engine supports list-based targets (SKILL.md L57-68). Context documents for a decision frequently span multiple directories (a spec, an architecture doc, a requirements doc). Forcing users to co-locate these into a single directory to use `--context` defeats the purpose of guided entry. [SKILL.md, L57-68; spec.md, L35]
   - **Risk if ignored**: Users with context spread across directories must either consolidate files or provide incomplete context. The resulting `problem.md` will underweight constraints from omitted documents.

6. **Add --force and --dry-run flags to define** (Priority: P2)
   - **Current state**: FR-011 handles existing files via interactive prompt only (L40).
   - **Proposed change**: Add `--force` (overwrite without asking) and `--dry-run` (print what would be written to stdout without writing). These are standard CLI conventions that enable scripted and automated usage.
   - **Rationale**: Spec 011 (gates) envisions automated conversus invocations in CI/CD pipelines. If `/conversus define` blocks on interactive prompts, it cannot be composed into automated workflows. The flags are also useful for experienced users who know what they want. [011 spec.md, L104-106; spec.md, L40]
   - **Risk if ignored**: `/conversus define` will be unusable in any non-interactive context, limiting its composability and making automated testing of the guided workflow impossible.

7. **Validate --context paths before ingestion** (Priority: P2)
   - **Current state**: The spec does not specify error handling for invalid `--context` paths (L35-36). The SKILL.md handler (L797) says "Resolve the path" but does not mandate existence checking.
   - **Proposed change**: Add: "If `--context <path>` does not exist or is unreadable, fail with: 'Context path does not exist: {path}'. Apply the same validation before reading any files." Mirror the `run` engine's validation pattern.
   - **Rationale**: The `run` engine validates all paths before execution (SKILL.md L195-196). The `define` handler should match this discipline. Silent path resolution failures produce incomplete `problem.md` files with no indication that context was lost. [SKILL.md, L195-196]
   - **Risk if ignored**: A typo in `--context` produces a `problem.md` that appears complete but is missing critical domain constraints. The user will not discover the error until the deliberation produces irrelevant results.

8. **Document the escape hatch from the guided workflow** (Priority: P3)
   - **Current state**: The spec positions `define` as "the entry point for non-experts" (L15). No guidance for when to skip it.
   - **Proposed change**: Add a note to section 1 or section 4: "Users who already have a `conversus.yml` should use `/conversus run` directly. The guided workflow (`define` -> `interests` -> `mode` -> `converge`) is optional -- it produces the same config format that power users write by hand."
   - **Rationale**: Without this note, the spec implies that `define` is a required step. This could lead to confusion when users see both `run` and `define` in the dispatch table and do not understand their relationship. [spec.md, L13-16, L27]
   - **Risk if ignored**: Power users will run `define` unnecessarily, or new users will skip `define` and struggle with `run`, not realizing the guided workflow exists to help them.

9. **Constrain problem.md artifact size** (Priority: P3)
   - **Current state**: No bounds on section lengths in the schema (L44-71). Context is bounded to "2-4 sentences" but Constraints, Open Questions, and Source Documents are unbounded.
   - **Proposed change**: Add soft guidance: "Constraints should be limited to the 5-10 most material constraints. If more than 10 constraints emerge, group related constraints or split the problem into sub-problems, each with its own `problem.md`."
   - **Rationale**: Every downstream consumer reads `problem.md` in full. An unbounded artifact becomes a context-window tax on every agent in the guided workflow. The `run` engine's bounded config (2-5 agents, 1-5 rounds) demonstrates that conversus values bounded complexity. [spec.md, L44-71; SKILL.md, L213-214]
   - **Risk if ignored**: Complex problems produce sprawling `problem.md` files that degrade prompt quality for downstream agents, particularly `/conversus interests` which must synthesize the entire problem definition into agent identities.

## Referenced Documentation

- `specs/007-subcommand-dispatch-define/spec.md` -- sections/lines cited: L13-16, L27, L29, L35-36, L37-38, L39, L40, L41, L44-71, L52, L65-66, L77-82, L87, L88
- `SKILL.md` -- sections/lines cited: L11-13, L18-33, L57-68, L192-222, L356, L750-751, L787-793, L797-802, L872-875
- `specs/008-interests-mode/spec.md` -- sections/lines cited: L31, L44-52, L59, L97
- `specs/009-guided-execution/spec.md` -- sections/lines cited: L51-54
- `specs/010-guided-arbitration/spec.md` -- sections/lines cited: L1-18
- `specs/011-phase-consensus-gates/spec.md` -- sections/lines cited: L104-106
- `specs/STATUS.md` -- sections/lines cited: L72-78 (007 status), L80-85 (008 status)
- `presets/role/devils-advocate.yml` -- sections/lines cited: L7-13 (prompt definition)
