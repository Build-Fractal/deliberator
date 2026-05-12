# Cross-Review of integration-specialist's Review

Reviewer: **agentskills-specialist**
Target: integration-specialist's review of Spec 011a (SKILL.md Breakdown)

---

## Dangerous Contradictions

### 1. The run engine must NOT remain in the root SKILL.md

integration-specialist recommends: "Keep the subcommand dispatch table, multi-agent isolation rules, and run engine core in the root SKILL.md. [...] Estimate: root SKILL.md at ~400-500 lines covering dispatch + invariants + engine." (Actionable Recommendation 1)

This directly contradicts the agentskills.io specification's core design constraint. The specification states: "Keep your main SKILL.md under 500 lines" and "Instructions (< 5000 tokens recommended): The full SKILL.md body is loaded when the skill is activated" (agentskills-spec.md, Progressive Disclosure section). The run engine core -- the phase loop, round loop, iteration loop, output path computation, termination conditions, and agent count formulas spanning lines 324-580 of the current SKILL.md -- is approximately 250 lines of dense specification prose. Combined with the dispatch table (~25 lines), multi-agent rules (~15 lines), and necessary framing, the root SKILL.md hits 400-500 lines and approximately 6,000-8,000 tokens. That exceeds the 5,000-token recommendation before a single handler reference is loaded.

My own review (Actionable Recommendation 2) proposed keeping "the run engine's phase-level flow summary (Phases 1-5 at one paragraph each, not the full template variable specifications)" in the root SKILL.md, targeting 300-400 lines and under 5,000 tokens. The distinction is critical: a phase-level summary tells the agent the run engine exists and what it does; the full engine specification (template variables, path formulas, iteration state management) belongs in `references/handler-run.md` and loads only when `/conversus run` or `/conversus converge` is invoked.

integration-specialist's concern about tight coupling within the engine (round counters, iteration counters, output path formulas, termination conditions) is valid -- but the solution is to keep those tightly coupled elements together in `references/handler-run.md`, not to keep them in the root SKILL.md. Co-location does not require root-level placement. An agent invoking `/conversus define` should not pay 6,000+ tokens for run engine internals it will never execute.

### 2. "Do not decompose" boundaries contradict progressive disclosure fundamentals

integration-specialist's Recommendation 7 proposes: "Define explicit 'do not decompose' boundaries. The round loop + iteration loop + output path computation + termination check (lines 346-580) is a tightly coupled state machine. Document this as a cohesive unit that must remain in the root SKILL.md."

The agentskills.io best practices state: "Overly comprehensive skills can hurt more than they help -- the agent struggles to extract what's relevant and may pursue unproductive paths triggered by instructions that don't apply to the current task" (best practices, "Aim for moderate detail"). Declaring 235 lines of state machine logic as a "do not decompose" unit that lives in the root SKILL.md means every invocation of every subcommand loads this state machine. The `/conversus define` handler, the `/conversus interests` handler, and the `/conversus mode` handler never touch the round loop. They should never see it.

My review agrees that the round loop, iteration loop, and output path computation are tightly coupled and should remain together (I did not propose splitting them). The disagreement is about where that cohesive unit lives. integration-specialist places it in the root SKILL.md; the agentskills specification places it in a reference file loaded on demand. These are incompatible positions. The tight coupling argument is about internal cohesion within a unit, not about the unit's position in the file hierarchy. A reference file can be just as cohesive as root-level content.

### 3. The dependency map recommendation creates a maintenance liability the specification warns against

integration-specialist's Recommendation 10 proposes adding a dependency map table to the root SKILL.md showing all reference files, their dependencies, and their call sites. This table would consume approximately 15-20 lines and introduce a maintenance contract: every time a reference file's dependencies change, the root SKILL.md must be updated.

The agentskills.io specification explicitly recommends: "Keep file references one level deep from SKILL.md. Avoid deeply nested reference chains" (agentskills-spec.md, File References section). The dispatch table already serves as the dependency map for handlers -- each row routes to a handler, and each handler reference file declares its own dependencies. Adding a redundant dependency map in the root SKILL.md creates a second source of truth that can drift from the actual reference file contents. My review (Recommendation 9) proposed that each reference file declare its own conditional loading triggers ("If the config contains an `arbiter:` block, read `references/arbitration-engine.md`"), which keeps dependency information co-located with the dependent content rather than centralized in an easily-stale table.

The agentskills best practices document's emphasis on "add what the agent lacks, omit what it knows" applies here: an agent that has been told "read `references/handler-converge.md`" and finds within it "this handler invokes the run engine; read `references/handler-run.md`" does not also need a root-level table telling it the same thing.

### 4. Keeping multi-agent rules in root SKILL.md is correct but for the wrong reason

integration-specialist argues (Alignment point 6 and Recommendation 1): "These rules should remain in the root SKILL.md rather than being buried in a reference file, because they are the most important constraint an implementing agent must internalize. Extracting them to a reference file increases the risk that they are not loaded or are loaded after the agent has already begun execution."

My review agrees the multi-agent rules belong in the root SKILL.md (Recommendation 2c), but integration-specialist's reasoning -- that reference files might "not be loaded" -- mischaracterizes how the agentskills specification's progressive disclosure works. The specification's model is: metadata at discovery, full SKILL.md body at activation, reference files during execution. An instruction in the SKILL.md body to "read references/X.md before proceeding" is loaded at activation time, before any execution begins. The agent will read the reference file. The actual reason the multi-agent rules belong in the root SKILL.md is the best practices principle of "match specificity to fragility": these rules apply to every run and converge invocation (two of seven subcommands, but the two most consequential ones), and their violation is catastrophic. That makes them "gotchas" in the specification's terminology -- content that "the agent may not recognize the trigger" for, and therefore must be front-loaded. The risk is not that the reference file won't be loaded; the risk is that the agent begins Phase 1 agent dispatch before reaching the instruction to load the reference file. The distinction matters because integration-specialist's reasoning, if generalized, would argue against extracting anything important to reference files, defeating the entire purpose of decomposition.

---

## Tensions

### 1. Granularity of subsystem extraction

integration-specialist proposes five extraction targets: handlers (5 guided workflow + 1 gate), dispute parsing, preset resolution, template variables, and the dependency map -- totaling approximately 9-10 reference files. My review proposes those same extractions plus validation rules, arbitration engine mechanics, multi-round execution details, operational notes, and output schema templates in `assets/` -- totaling approximately 14 reference files plus 3 asset files.

integration-specialist's "Off-Base Assumptions" section warns against external standards driving internal decomposition boundaries. My review's additional extractions (validation rules, arbitration engine, multi-round execution) are driven by the agentskills specification's progressive disclosure model: load content only when the execution path requires it. An agent running a single-round, no-arbiter deliberation should not load arbitration engine mechanics or multi-round execution details.

The tension is real: more reference files mean more conditional loading instructions in handler files, which increases the cognitive overhead for maintaining the skill. But fewer reference files mean larger reference files, which partially defeats progressive disclosure. The resolution likely lies somewhere between the two proposals -- extract at the handler level (both reviews agree) and at the high-value subsystem level (dispute parsing, preset resolution -- both reviews agree), but be conservative about further granularity within the run engine until execution traces reveal specific context waste.

### 2. Where output schemas belong: references/ vs assets/

My review (Recommendation 6) proposes moving output schema templates (problem.md schema, interests.md schema, gate-result.md schema) to `assets/`, following the agentskills specification: "Templates (document templates, configuration templates)" belong in `assets/`. integration-specialist does not address output schemas at all -- they are not mentioned in any recommendation.

The tension is about whether these schemas are "templates" (static resources the agent pattern-matches against, belonging in `assets/`) or "specification content" (behavioral instructions the agent must follow, belonging in `references/` or inline). The agentskills best practices say: "Short templates can live inline in SKILL.md; for longer templates, or templates only needed in certain cases, store them in assets/" (best practices, "Templates for output format"). The problem.md schema is approximately 30 lines and needed only by the define handler. The gate-result.md schema is approximately 35 lines and needed only by the gate handler. These fit the "templates only needed in certain cases" criterion.

integration-specialist's silence on this point may reflect a view that schemas are part of the handler specification and should move with the handler to its reference file. That is a defensible position -- co-locating the schema with the handler that produces it keeps the behavioral contract in one place. The agentskills specification supports both approaches; the choice depends on whether reuse across handlers is expected (favoring `assets/`) or not (favoring inline in the handler reference file).

### 3. Error message contracts: centralized vs co-located

integration-specialist's Missed Opportunity 6 identifies error message strings as an interface contract that needs explicit handling after decomposition. My review (Recommendation 5) proposes consolidating validation rules including error messages into `references/validation-rules.md`.

integration-specialist frames this as a question -- "are error messages defined in the reference file or in the root SKILL.md?" -- without proposing an answer. My review proposes centralization in a dedicated reference file. The tension is that centralized error messages require every handler to load the validation reference file, adding a mandatory dependency to every handler. Co-located error messages (each handler defines its own) risk drift between handlers that share validation patterns (e.g., agent name validation is used by run, gate, and interests handlers). Neither review fully resolves this. The pragmatic answer may be: shared validation patterns (agent name regex, heading validation rules) go in a shared reference file; handler-specific error messages stay in their handler reference file.

### 4. The linter's post-decomposition role

integration-specialist (Missed Opportunity 4 and Recommendation 8) proposes expanding the linter to validate reference file consistency -- checking that variables in handler reference files match `schema/variables.yml`, error messages match a canonical catalogue, and subsystem interface contracts are consistent with call sites. My review does not address the linter's expanded role.

integration-specialist is right that decomposition increases the linter's importance. The tension is about scope: should the linter validate structural consistency of reference files (a mechanical check that catches drift), or should reference files be designed to minimize the need for cross-file validation (by co-locating contracts with their implementations)? The agentskills specification does not address linting at all -- it is a conversus-specific tool. Expanding the linter is a good idea in principle, but the linter currently validates templates against `schema/variables.yml`. Expanding it to validate reference file consistency against SKILL.md call sites requires the linter to parse Markdown prose for semantic intent, which is a significantly harder problem than validating YAML schemas. The recommendation is directionally correct but may be impractical without a more structured contract format.

### 5. Token budget: line count vs token count

My review (Off-Base Assumption 4) flags that the 2216-line count understates the problem because the specification's recommendation is both under 500 lines and under 5,000 tokens, and 500 lines of dense specification prose will likely exceed 5,000 tokens. integration-specialist targets "~400-500 lines" for the root SKILL.md without mentioning the token budget.

This is a tension because integration-specialist's 400-500 line target for a root SKILL.md that includes the full run engine would almost certainly exceed 5,000 tokens given the density of the specification prose (the current 2216 lines produce 31k tokens, roughly 14 tokens per line). At 14 tokens/line, 500 lines would be approximately 7,000 tokens. My review's target of 300-400 lines with phase-level summaries (less dense than the full engine specification) would be approximately 4,200-5,600 tokens -- closer to the recommendation but potentially still over. Both reviews should acknowledge that hitting the 5,000-token target may require the root SKILL.md to be closer to 300 lines with aggressive summarization of even the phase-level flow.

---

## Safe Agreements

### 1. The dispatch table is the correct anchor for the root SKILL.md

Both reviews agree without qualification. integration-specialist (Alignment point 1): "Decomposition proposals that preserve this table as the entry point in the root SKILL.md, with handlers referenced rather than inlined, align with progressive disclosure." My review (Recommendation 2b): keep the "Subcommand dispatch table with one-line descriptions and file references" in SKILL.md. The agentskills specification's "provide defaults, not menus" pattern is satisfied by the dispatch table's exact routing, and both reviews recognize it as the routing contract that must be present on every activation.

### 2. Each guided workflow handler should become a separate reference file

integration-specialist (Recommendation 2): "Extract each guided workflow handler (define, interests, mode, converge, arbitrate) to `references/handler-{name}.md`." My review (Recommendation 1): "Create `references/handler-run.md`, `references/handler-define.md`, [...] The SKILL.md dispatch table becomes: 'When the user invokes `/conversus define`, read `references/handler-define.md` and follow the instructions there.'" Both reviews identify the same file-mediated coupling between handlers (define writes problem.md, interests reads it) as evidence that decomposition will not break the inter-handler contract. Both reviews agree on the naming convention `handler-{name}.md`. This is the highest-confidence decomposition target.

### 3. The Dispute-Parsing Subsystem is a natural extraction candidate with a stable interface

integration-specialist (Recommendation 4): "Extract the Dispute-Parsing Subsystem to `references/subsystem-dispute-parsing.md`. This subsystem already has an explicitly documented stable interface (input: synthesis path; output: boolean + integer)." My review (Recommendation 3): "Extract the Dispute-Parsing Subsystem to `references/dispute-parsing.md`. It has a declared stable interface, is referenced by three handlers." Both reviews cite the same three call sites (Phase 6 trigger evaluation, round termination, post-execution reporting) and the same interface contract (structural markers, mode-specific headings, fallback behavior). The only difference is naming convention -- integration-specialist uses a `subsystem-` prefix, my review does not. This is a stylistic difference, not a substantive one.

### 4. Preset resolution should be extracted as a shared subsystem

integration-specialist (Recommendation 5): "Extract preset resolution to `references/subsystem-preset-resolution.md`. [...] The interface contract is: (a) input: preset name (qualified or unqualified), (b) output: resolved agent config." My review (Recommendation 7): "Move the preset resolution specification to `references/preset-resolution.md`. The single preset resolution, composition templates, validation rules, and inline override semantics are only needed when a config contains `preset:` fields." Both reviews identify the same three call sites (config parsing, interest generation, gate agent expansion) and agree that conditional loading is appropriate -- the agent reads this reference only when a `preset:` field is encountered. This is the second-highest-confidence subsystem extraction after dispute parsing, because both its interface and its call sites are well-defined.

---

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/integration-specialist/review.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/agentskills-specialist/review.md`
- `<HOME>/code/payer-index-mono/conversus/SKILL.md`
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md`
- `<HOME>/code/payer-index-mono/conversus/references/agentskills-spec.md`
- `<HOME>/code/payer-index-mono/conversus/references/agentskills-best-practices.md`
