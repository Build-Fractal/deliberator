# Integration Specialist Review — Spec 011a: SKILL.md Breakdown

## Executive Summary

The conversus SKILL.md at 2216 lines and 31k tokens is a monolithic orchestration specification that encodes seven subcommand handlers, a shared run engine, a dispute-parsing subsystem, template variable expansion, preset resolution, round/iteration loops, and arbitration mechanics in a single file. From an integration perspective, this monolith has a hidden advantage: every interface contract is co-located, making it impossible for handler A to drift from handler B's assumptions about shared subsystems. Decomposition will create explicit interface boundaries where today only implicit co-location exists. The question is not whether to decompose — the file clearly exceeds agentskills.io's 500-line recommendation by 4x — but how to decompose without introducing fragile coupling, circular dependencies, or invariant violations.

The current SKILL.md already contains several stable seams that make it a strong decomposition candidate. The `schema/variables.yml` file formalizes the template variable contract independently of the SKILL.md. The `linter/validate.py` codifies template validation rules in executable form. The `templates/{mode}/` directory tree already externalizes prompt engineering. These are proven interface boundaries — they have been operating as separate artifacts for multiple specs without regression. The decomposition spec should leverage these existing seams and be cautious about creating new ones, particularly around the run engine's internal phase loop, which has tight coupling between iteration state, round state, output path computation, and termination logic.

The most dangerous decomposition boundary would be one that separates the run engine's phase execution from its state management (round counters, iteration counters, output path formulas, termination conditions). These are tightly coupled for good reason — separating them would require passing complex state objects across file boundaries, creating either a god-object anti-pattern or a distributed state management problem. The safest decompositions are at the subcommand level (each guided workflow handler as a reference file) and at the subsystem level (dispute parsing, preset resolution as reference files). The run engine should remain a single cohesive unit.

## Alignment

- **The subcommand dispatch table (lines 22-44) is the correct anchor for SKILL.md.** Decomposition proposals that preserve this table as the entry point in the root SKILL.md, with handlers referenced rather than inlined, align with progressive disclosure and maintain the routing contract.

- **Template variable contracts in `schema/variables.yml` are already a proven stable seam.** This is the strongest evidence that decomposition works for conversus — the schema has been decoupled from SKILL.md since spec 009 without breaking the orchestrator. Any decomposition proposal should follow this pattern.

- **The guided workflow prerequisite chain (define -> interests -> mode -> converge) is a sequential dependency graph, not a shared-state graph.** Each handler reads the previous handler's output file (`problem.md`, `interests.md`, `conversus.yml`). This file-mediated coupling is the safest form of inter-handler dependency — decomposition will not break it because the interface is the file format, not an in-memory contract.

- **The Dispute-Parsing Subsystem (lines 750-777) has an explicitly documented stable interface contract.** The SKILL.md itself calls out that changes to dispute markers and headings are "breaking changes" requiring coordination. This subsystem is a natural extraction candidate with a well-defined input (synthesis file path) and output (boolean + integer).

- **The `converge` and `gate` handlers both delegate to the run engine without adding execution logic.** This "thin wrapper" pattern means the run engine is the shared core, and decomposition must keep it accessible from both call sites. This is well-suited to a reference file model where SKILL.md's dispatch table routes to handler reference files, which in turn reference the shared run engine.

- **The multi-agent isolation rules (lines 324-336) are invariants that benefit from prominent placement.** These rules should remain in the root SKILL.md rather than being buried in a reference file, because they are the most important constraint an implementing agent must internalize. Extracting them to a reference file increases the risk that they are not loaded or are loaded after the agent has already begun execution.

## Missed Opportunities

- **The spec.md (011a) is only 11 lines and provides no concrete decomposition proposal.** It links to external resources (agentskills.io, agents.md, APM docs, openspec.dev) without proposing specific file boundaries, naming conventions, or interface contracts. This deliberation is running against a problem statement, not a solution — the proposals will need to be generated from scratch rather than evaluated.

- **No analysis of which sections are read-once vs read-repeatedly by the orchestrator.** The run engine's phase execution loop reads templates once per phase, but the dispatch table is consulted only at invocation. Understanding read frequency informs which content benefits most from being in the root SKILL.md (read on every invocation) vs reference files (loaded on demand).

- **The spec does not address the `antipatterns/catalog.md` integration.** The Antipattern Check (lines 237-244) is a pre-execution step that reads from a separate catalog file. This is already a reference-file pattern, but its interaction with decomposed handlers is not considered. If each handler becomes a reference file, does each handler need its own antipattern check, or is this an orchestrator-level concern?

- **No consideration of the linter's role as an integration test.** The `linter/validate.py` validates templates against `schema/variables.yml`. After decomposition, the linter becomes a critical integration test — it verifies that extracted reference files (template variable documentation, phase-specific contracts) remain consistent with the templates. The spec should mandate that the linter's scope expands to cover any new reference files.

- **The preset resolution algorithm (lines 126-200) is complex enough to warrant extraction, but the spec does not identify it as a candidate.** Preset resolution involves file discovery, disambiguation, composition templates, and inline override rules. It is called from three places: the run engine's config parsing, the interests handler's preset matching, and the gate handler's agent expansion. This is a shared subsystem with a clear interface (preset name -> resolved agent config).

- **No discussion of error message contracts.** The SKILL.md specifies exact error message strings for every validation failure (e.g., "Invalid agent name: {name}. Use lowercase alphanumeric with hyphens/underscores."). If validation logic moves to reference files, these error messages become part of the interface contract. The spec should address whether error messages are defined in the reference file or in the root SKILL.md.

- **The existing `references/` directory already has content (5 files) but these are external documentation snapshots, not conversus-internal reference files.** The decomposition should establish a naming convention that distinguishes external reference docs from internal subsystem specifications.

- **Round and iteration state management is deeply interleaved with output path computation (lines 346-395).** Any decomposition proposal that separates the round loop from path computation will need to define a state object contract that is complex enough to be error-prone. This coupling should be called out as a "do not decompose" boundary.

- **The `converge` handler's post-execution report (lines 1458-1533) duplicates the run engine's Step 5 report with mode-specific interpretation.** Extracting both to reference files without a shared "report vocabulary" would create drift risk between the two reports.

## Off-Base Assumptions

- **Assumption: decomposition primarily reduces token count.** While the agentskills.io recommendation of <500 lines is framed around token efficiency, the more important benefit of decomposition for conversus is **change isolation**. The current monolith means any change to the gate handler (a CI/CD concern) requires re-reading the full run engine (a deliberation concern). Token savings are a secondary benefit; the primary benefit is that agents working on guided workflow changes do not need to load run engine details, and vice versa. The spec's framing around file size misses this.

- **Assumption: all external standards (agentskills.io, agents.md, APM, openspec.dev) are equally relevant.** From an integration perspective, the decomposition must first serve the conversus orchestrator's internal coherence. External packaging (APM) or cross-agent compatibility (agents.md) are distribution concerns that should not drive internal decomposition boundaries. The internal seams should be identified first, then external standards can be applied as packaging on top.

- **Assumption: the run engine and guided workflow are peers.** They are not. The run engine is the foundation; the guided workflow (define/interests/mode/converge/arbitrate) is a UX layer that eventually produces a `conversus.yml` and invokes the run engine. The gate handler is a CI/CD layer that also invokes the run engine. This is a layered architecture: engine at the bottom, UX and CI/CD on top. Decomposition should respect this layering — extracting guided workflow handlers to reference files is low-risk because they have no downward coupling to the engine's internals. Extracting engine subsystems is higher risk because both upper layers depend on the engine's behavior.

## Actionable Recommendations

1. **Keep the subcommand dispatch table, multi-agent isolation rules, and run engine core in the root SKILL.md.** The dispatch table is the entry point contract. The isolation rules are non-negotiable invariants that must be front-loaded in every agent's context. The run engine's phase loop (Phases 1-6, round loop, iteration loop, termination conditions) has tight internal coupling that does not benefit from decomposition. Estimate: root SKILL.md at ~400-500 lines covering dispatch + invariants + engine.

2. **Extract each guided workflow handler (define, interests, mode, converge, arbitrate) to `references/handler-{name}.md`.** Each handler has a clean interface: it reads prerequisite files from disk, validates them, interacts with the user, and writes an output file. There is no shared in-memory state between handlers. The interface contract for each is: prerequisite files (input), output file (output), error messages (contract). Estimate: ~150-250 lines per handler, 5 handlers = ~900 lines extracted.

3. **Extract the gate handler to `references/handler-gate.md`.** The gate handler has a distinct concern (CI/CD integration) with its own configuration schema (`gates.yml`), result schema (`gate-result.md`), exit code contract, and re-run behavior. Its only coupling to the run engine is "generate a `conversus.yml` and invoke Step 1-5." Estimate: ~180 lines extracted.

4. **Extract the Dispute-Parsing Subsystem to `references/subsystem-dispute-parsing.md`.** This subsystem already has an explicitly documented stable interface (input: synthesis path; output: boolean + integer). It is called from three sites: Phase 6 trigger evaluation, round termination, and post-execution reporting. The interface contract should be: (a) the structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`), (b) the mode-specific heading table, (c) the fallback behavior, (d) the default-to-triggered safety measure. Mark these as breaking-change boundaries.

5. **Extract preset resolution to `references/subsystem-preset-resolution.md`.** Preset resolution is called from config parsing (run engine), interest generation (interests handler), and gate agent expansion (gate handler). The interface contract is: (a) input: preset name (qualified or unqualified), (b) output: resolved agent config (name, prompt, docs), (c) error conditions: not found, ambiguous, not composable. Include the composition templates in this reference file since they are only relevant to preset resolution.

6. **Extract template variable documentation to `references/contract-template-variables.md`.** The SKILL.md currently lists template variables for each phase (lines 401-435, 449-464, 471-478, 488-497, 503-517, 592-604, 643-658). This is duplicative with `schema/variables.yml`. The reference file should be the human-readable companion to the machine-readable schema, and the SKILL.md should reference both rather than inlining the variable lists. Interface contract: the reference file and schema must enumerate the same variables.

7. **Define explicit "do not decompose" boundaries.** The round loop + iteration loop + output path computation + termination check (lines 346-580) is a tightly coupled state machine. Document this as a cohesive unit that must remain in the root SKILL.md. Similarly, the phase execution block (Phases 1-6 agent dispatch) depends on output path state from the round loop and should not be separated from it. Any future proposal to split the engine should be evaluated through a state-dependency analysis first.

8. **Mandate that the linter validates reference file consistency after decomposition.** Extend `linter/validate.py` to check that: (a) every variable referenced in handler reference files exists in `schema/variables.yml`, (b) every error message string in handler reference files matches the canonical error catalogue, (c) every subsystem reference file's interface contract is consistent with its call sites in SKILL.md. This is the integration test that prevents decomposition-induced drift.

9. **Establish a naming convention for reference files that distinguishes type.** Proposed convention: `references/handler-{name}.md` for subcommand handlers, `references/subsystem-{name}.md` for shared subsystems (dispute parsing, preset resolution), `references/contract-{name}.md` for interface contracts (template variables, error messages). This makes the dependency graph legible from the directory listing alone.

10. **Add a dependency map to the root SKILL.md.** After decomposition, include a section like:
    ```
    ## Reference File Dependencies
    | Reference File | Depends On | Called By |
    |---|---|---|
    | handler-define.md | (none) | dispatch table |
    | handler-interests.md | handler-define.md output (problem.md) | dispatch table |
    | handler-mode.md | handler-interests.md output (interests.md) | dispatch table |
    | handler-converge.md | handler-mode.md output (conversus.yml), run engine | dispatch table |
    | handler-gate.md | run engine | dispatch table |
    | handler-arbitrate.md | run engine Phase 6, subsystem-dispute-parsing.md | dispatch table |
    | subsystem-dispute-parsing.md | (none — reads synthesis files) | run engine, handler-converge.md, handler-arbitrate.md |
    | subsystem-preset-resolution.md | presets/ directory | run engine, handler-interests.md, handler-gate.md |
    ```
    This makes circular dependency detection trivial and documents the integration topology.

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/SKILL.md` (lines 1-2199 — the decomposition target)
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md` (the decomposition problem statement)
- `<HOME>/code/payer-index-mono/conversus/README.md` (architectural invariants, competition modes, process phases, directory structure)
- `<HOME>/code/payer-index-mono/conversus/schema/variables.yml` (template variable contract — stable seam evidence)
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus.yml` (deliberation configuration for this run)
