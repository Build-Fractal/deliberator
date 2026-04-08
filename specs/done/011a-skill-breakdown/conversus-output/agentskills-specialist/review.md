# Agent Skills Specialist Review

## Executive Summary

The conversus SKILL.md is 2216 lines and approximately 31,000 tokens. The agentskills.io specification recommends keeping SKILL.md under 500 lines and the body under 5,000 tokens. This is not a soft guideline -- it is a design constraint rooted in how agent runtimes handle progressive disclosure. When a skill activates, the entire SKILL.md body loads into the agent's context window alongside conversation history, system instructions, and any other active skills. At 31k tokens, conversus consumes a significant fraction of available context on every invocation, regardless of which subcommand the user runs. An agent invoking `/conversus define` pays the same context cost as one invoking `/conversus run`, even though the define handler needs roughly 3% of the total SKILL.md content.

The current SKILL.md conflates three structurally distinct concerns into a single file: (1) the subcommand dispatch table and core orchestration flow, (2) the run engine's detailed phase execution mechanics including template variable contracts and validation rules, and (3) seven independent subcommand handlers with their own input parsing, prerequisite checks, output schemas, and reporting formats. The agentskills.io specification explicitly addresses this pattern: "When a skill legitimately needs more content, move detailed reference material to separate files in `references/` or similar directories. The key is telling the agent _when_ to load each file" (best practices, "Structure large skills with progressive disclosure"). Conversus already has a `references/` directory (containing the agentskills.io documentation itself) and a `schema/` directory. The infrastructure for progressive disclosure exists; the SKILL.md simply has not been restructured to use it.

The restructuring opportunity is substantial. The dispatch table, core invariants, and run engine's phase-level flow can fit in under 400 lines. The remaining 1800+ lines -- subcommand handler specifications, the Dispute-Parsing Subsystem, template variable contracts, validation rules, gate configuration schemas, and arbitration mechanics -- are reference material that should load on demand when the agent resolves a specific subcommand. This aligns with the spec's progressive disclosure model: metadata at discovery time, core instructions at activation, detailed references when needed during execution.

## Alignment

- **The frontmatter is well-crafted.** The `name`, `description`, `compatibility`, `license`, and `allowed-tools` fields follow the specification exactly. The description is keyword-rich and mentions all seven subcommands, which helps activation accuracy. At 192 words it is within the 1024-character limit.

- **The dispatch table (lines 22-44) is an exemplary implementation of the "provide defaults, not menus" pattern.** It gives the agent a single lookup table with exact routing, an error message for unknown subcommands, and a default for bare invocation. This is the correct level of prescriptiveness for a fragile operation (subcommand routing).

- **The non-negotiable multi-agent rules (lines 324-336) correctly apply "match specificity to fragility."** These are the highest-fragility instructions in the entire skill -- violating them produces correlated outputs that defeat the deliberation's purpose. The explicit, prescriptive enumeration with a rationale ("why this matters") follows the best practice of being prescriptive where operations are fragile.

- **Template variable contracts are already externalized.** The `schema/variables.yml` and `schema/modes/{mode}.yml` files, plus the linter at `linter/validate.py`, demonstrate that the project understands the value of separating machine-checkable contracts from prose instructions. This is a natural seam for further extraction.

- **The `references/` directory already exists with substantial content.** The five files in `references/` total roughly 55k characters of documentation. The directory structure is one level deep from SKILL.md, which matches the specification's file reference recommendation.

- **The guided workflow handlers (define, interests, mode, converge, arbitrate) each have clean prerequisite chains.** The "Missing Prerequisite Check" sections form a directed graph: define -> interests -> mode -> converge -> run. This is exactly the kind of procedural, multi-step workflow that the best practices document recommends structuring with checklists and progressive disclosure.

## Missed Opportunities

- **No reference files for subcommand handlers.** Each of the seven subcommand handlers (run, define, interests, mode, converge, arbitrate, gate) is a self-contained specification ranging from 100 to 700 lines. The agent only needs one handler per invocation. Loading all seven on every activation wastes approximately 25,000 tokens of context on unreachable instructions. The specification explicitly recommends: "Read `references/api-errors.md` if the API returns a non-200 status code" as a pattern -- the equivalent here is "Read `references/handler-define.md` when the user invokes `/conversus define`."

- **The Dispute-Parsing Subsystem (lines 750-778) is referenced by three separate handlers but defined inline.** Phase 6 trigger evaluation, round termination, and the converge post-execution report all reference this subsystem. It has a declared "stable interface contract" (line 777). This is a textbook candidate for extraction to `references/dispute-parsing.md` -- it is reference material with a stable interface, loaded on demand when the agent needs to parse disputes.

- **Template variable documentation spans approximately 200 lines across multiple phases.** The variable definitions for Phases 1-6, cross-round synthesis, and path-list formatting rules are repeated or cross-referenced throughout the run engine section. Consolidating these into `references/template-variables.md` (or pointing to the already-existing `schema/variables.yml`) would eliminate redundancy and reduce the SKILL.md body by roughly 150-200 lines.

- **Validation rules are specified inline for every handler.** Each handler has its own post-write validation section, config validation section, or prerequisite check section. Many share patterns (heading validation is case-insensitive, agent names match `[a-z0-9][a-z0-9-_]*`, paths must exist). A consolidated `references/validation-rules.md` would eliminate this repetition and make the validation contract auditable in one place.

- **The gate subcommand (lines 1881-2178) is approximately 300 lines of CI/CD-specific specification** including exit codes, gate-result.md schemas, re-run behavior, and full output preservation rules. This is a coherent unit that serves a different audience (CI/CD pipeline authors) than the interactive subcommands. Extracting it to `references/handler-gate.md` reduces SKILL.md size and lets the agent load CI/CD semantics only when `/conversus gate` is invoked.

- **Output schema templates could live in `assets/`.** The problem.md schema (lines 863-892), interests.md schema (lines 1044-1064), gate-result.md schema (lines 2011-2044), and various report format templates are concrete output structures that agents pattern-match against. The best practices explicitly recommend: "Short templates can live inline in SKILL.md; for longer templates, or templates only needed in certain cases, store them in `assets/`." These schemas are needed only in certain cases (specific subcommand invocations).

- **The "Important Notes" section (lines 2181-2216) mixes gotchas with reference material.** The agent count formulas, round/iteration orthogonality explanation, and baseline feature inventory are reference material. The actual gotchas (re-running overwrites, use `run_in_background: true` for Phases 1-4) should stay in SKILL.md. The reference material should move out.

- **Preset resolution rules (lines 126-202) are detailed specification material** covering single preset resolution, preset composition with 2-preset and 3-preset templates, composition limits, `composable: false` handling, and inline overrides. This is approximately 75 lines that the agent only needs when a config contains `preset:` fields. A reference file `references/preset-resolution.md` would load on demand.

- **The arbiter configuration and Phase 6 execution (lines 612-692) include influence-aware heading validation, failure handling, and output validation** that totals approximately 80 lines of detailed conditional logic. This material is only relevant when an arbiter is configured and Phase 6 actually fires. It could be extracted to `references/arbitration-engine.md` alongside the Phase 6 template variable definitions.

## Off-Base Assumptions

- **The current structure assumes all instructions must be immediately available.** The SKILL.md appears designed under the assumption that the agent cannot or will not read additional files during execution. But the `allowed-tools` field already declares `Read` as pre-approved, and every subcommand handler already instructs the agent to read files (templates, config files, prior context). The agent is already doing file I/O on every run. Adding `references/handler-run.md` to the read list is not a new capability -- it is a refinement of existing behavior.

- **The monolithic SKILL.md assumes subcommands share enough context to justify co-location.** In practice, the handlers share only the dispatch table, the Dispute-Parsing Subsystem interface, and validation patterns. The define handler knows nothing about Phase 2 cross-review mechanics. The gate handler does not use the guided workflow prerequisite chain. Co-locating them forces the agent to process 2000+ lines of irrelevant instructions on every invocation, which the best practices document warns "can hurt more than they help -- the agent struggles to extract what's relevant."

- **The inline agent count formulas and worked examples (lines 2186-2196) assume the agent cannot compute.** The formulas `N^2 + 2N + 1` and `rounds * per_round_agents + 1` are arithmetic that any LLM can derive from the phase structure. The worked examples ("For 3 agents without arbiter: 16 total agent launches") are helpful for human readers of the spec but redundant for an agent executing the skill. This is a case of explaining "what the agent already knows" -- per the best practice of omitting what the agent knows.

- **The 2216-line count may be understating the problem.** The specification recommends under 500 lines and under 5,000 tokens. At 31k tokens, the SKILL.md is roughly 6x the recommended token budget, not just 4x the line count. Token density matters more than line count for context window consumption. Even aggressive restructuring to 500 lines would likely still exceed the 5,000 token recommendation if those lines are dense specification prose. The target should be token-aware, not just line-aware.

## Actionable Recommendations

1. **Extract each subcommand handler to its own reference file.** Create `references/handler-run.md`, `references/handler-define.md`, `references/handler-interests.md`, `references/handler-mode.md`, `references/handler-converge.md`, `references/handler-arbitrate.md`, and `references/handler-gate.md`. The SKILL.md dispatch table becomes: "When the user invokes `/conversus define`, read `references/handler-define.md` and follow the instructions there." This single change reduces the SKILL.md body from ~2200 lines to ~300 lines and transforms subcommand handling from eager loading to on-demand loading. Each reference file is one level deep from SKILL.md, satisfying the specification's file reference depth recommendation.

2. **Keep the following in SKILL.md (the always-loaded core):** (a) Frontmatter (unchanged), (b) Subcommand dispatch table with one-line descriptions and file references, (c) The non-negotiable multi-agent rules (lines 324-336) since these are the highest-fragility invariants that must be in context on every run, (d) The run engine's phase-level flow summary (Phases 1-5 at one paragraph each, not the full template variable specifications), (e) A gotchas section with the 3-5 most critical operational notes. Target: 300-400 lines, under 5,000 tokens.

3. **Extract the Dispute-Parsing Subsystem to `references/dispute-parsing.md`.** It has a declared stable interface, is referenced by three handlers, and is approximately 30 lines of specification. Reference it from the SKILL.md core flow and from each handler that uses it: "For dispute detection, see `references/dispute-parsing.md`."

4. **Extract template variable contracts to `references/template-variables.md`.** Consolidate all phase-specific variable definitions, path-list formatting rules, round-aware path variables, and the variable expansion rules into a single reference. Point the agent to this file from the run handler: "Before filling templates, read `references/template-variables.md` for the complete variable contract." This can complement the existing `schema/variables.yml` by providing the prose explanation alongside the machine-readable schema.

5. **Extract validation rules to `references/validation-rules.md`.** Consolidate agent name validation, heading validation rules, path existence checks, config schema validation, and post-write validation patterns into one reference. Each handler reference file then says "Apply the standard validation rules from `references/validation-rules.md`" instead of repeating the regex and error message format.

6. **Move output schema templates to `assets/`.** The problem.md schema, interests.md schema, gate-result.md schema, and conversus.yml schema are concrete document structures. Place them in `assets/problem-schema.md`, `assets/interests-schema.md`, `assets/gate-result-schema.md`. Reference them from the handler files: "Write `problem.md` following the schema in `assets/problem-schema.md`." This follows the specification's recommendation for templates and static resources.

7. **Move the preset resolution specification to `references/preset-resolution.md`.** The single preset resolution, composition templates, validation rules, and inline override semantics are only needed when a config contains `preset:` fields. The run handler and gate handler reference this file conditionally: "If any agent entry contains a `preset` field, read `references/preset-resolution.md` for resolution rules."

8. **Restructure the "Important Notes" section.** Keep the 3-5 genuine gotchas in SKILL.md (re-run overwrites, background vs foreground dispatch, template resolution path). Move the agent count formulas, worked examples, round/iteration orthogonality explanation, and baseline feature inventory to `references/operational-notes.md`. The agent can derive the formulas from the phase structure; the human-oriented explanations serve documentation, not execution.

9. **Add conditional loading instructions to each reference.** Do not use generic "see references/ for details." Instead, use specific triggers: "If the config contains an `arbiter:` block, read `references/arbitration-engine.md` before executing Phase 6." "If `rounds > 1`, read `references/multi-round-execution.md` for round loop mechanics and stagnation detection." This is the progressive disclosure pattern the specification recommends: the agent loads context on demand based on the specific execution path.

10. **Proposed directory layout after restructuring:**

```
conversus/
├── SKILL.md                          # ~350 lines: frontmatter + dispatch + core flow + invariants + gotchas
├── references/
│   ├── handler-run.md                # Run engine: config parsing, phase execution, template filling
│   ├── handler-define.md             # Define: problem definition workflow
│   ├── handler-interests.md          # Interests: interest discovery workflow
│   ├── handler-mode.md               # Mode: mode selection and config generation
│   ├── handler-converge.md           # Converge: guided execution wrapper
│   ├── handler-arbitrate.md          # Arbitrate: guided arbitration workflow
│   ├── handler-gate.md               # Gate: CI/CD consensus gates
│   ├── dispute-parsing.md            # Dispute-Parsing Subsystem (stable interface)
│   ├── template-variables.md         # Template variable contracts (all phases)
│   ├── validation-rules.md           # Shared validation patterns and error formats
│   ├── preset-resolution.md          # Preset resolution, composition, and override rules
│   ├── arbitration-engine.md         # Phase 6 mechanics, influence levels, failure handling
│   ├── multi-round-execution.md      # Round loop, stagnation detection, cross-round synthesis
│   ├── operational-notes.md          # Agent count formulas, baseline features, orthogonality notes
│   ├── agentskills-spec.md           # (existing)
│   ├── agentskills-best-practices.md # (existing)
│   ├── agentskills-quickstart.md     # (existing)
│   ├── agentskills-what.md           # (existing)
│   └── agents-md.md                  # (existing)
├── assets/
│   ├── problem-schema.md             # problem.md output schema template
│   ├── interests-schema.md           # interests.md output schema template
│   └── gate-result-schema.md         # gate-result.md output schema template
├── schema/                           # (existing, unchanged)
│   ├── variables.yml
│   └── modes/
├── templates/                        # (existing, unchanged)
├── presets/                          # (existing, unchanged)
├── linter/                           # (existing, unchanged)
└── antipatterns/                     # (existing, unchanged)
```

This restructuring reduces SKILL.md from 31k tokens to approximately 4,000-5,000 tokens while preserving every specification detail in reference files that load on demand. The agent pays the full context cost only for the specific subcommand and execution path it encounters, rather than loading all seven handlers, all four competition modes' Phase 6 variants, and all CI/CD gate mechanics on every invocation.

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/references/agentskills-spec.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/references/agentskills-best-practices.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/references/agentskills-quickstart.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/README.md`
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus.yml`
