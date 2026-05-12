# APM Specialist Review — Conversus SKILL.md Extractability Assessment

## Executive Summary

The conversus SKILL.md at 2200+ lines is a monolithic specification encoding seven subcommands (`run`, `define`, `interests`, `mode`, `converge`, `arbitrate`, `gate`), four competition modes with distinct template variable contracts, a preset composition system, a dispute-parsing subsystem, and a multi-round execution engine. From an APM packaging perspective, this file conflates three distinct distribution concerns: (1) the deliberation engine itself (run + template system + dispute parsing), (2) the guided workflow wizard (define/interests/mode/converge/arbitrate), and (3) the CI/CD gate integration. These map cleanly onto APM's primitive model — specifically, a core skill plus sub-skills — but only two of the three warrant extraction. The presets directory already behaves like a distributable artifact catalog, and the templates are mode-specific prompt engineering that APM's compilation system could optimize across consuming projects.

However, the overhead calculus matters. Conversus is currently used by one project (this monorepo). APM packaging adds `apm.yml` manifests, version management, dependency resolution, and multi-target skill deployment (`.github/skills/`, `.claude/skills/`, `.cursor/skills/`). That machinery pays for itself when multiple consumers exist or when composition with other packages is needed. For a single-project framework in active spec development (specs 001-011a and counting), premature packaging creates maintenance drag: every SKILL.md change requires version bumps, and the spec-driven development loop becomes slower. The right strategy is to identify the extraction boundaries now, implement them as internal structural splits (sub-skills within the same package), and defer full APM distribution until the spec suite stabilizes and a second consumer appears.

## Alignment

- **The spec's identification of SKILL.md size as the core problem is correct.** At 119KB / 2200+ lines, this exceeds any reasonable context window budget for a single skill. APM's sub-skill promotion mechanism (`.apm/skills/*/SKILL.md` promoted to `.github/skills/{name}/`) was designed precisely for this decomposition pattern.

- **The presets directory is already structured as a distributable catalog.** The `presets/` directory with `category/name.yml` naming, validation rules (name matches filename, category matches parent directory), and composition semantics (max 3, `composable: false` guard) mirrors APM's package discovery conventions. This is the lowest-friction extraction target.

- **The gate subcommand is architecturally independent.** Gate reads a `gates.yml`, generates a standard `conversus.yml`, delegates to the run engine, and produces a machine-readable `gate-result.md`. Its only dependency on the rest of SKILL.md is the run engine and the Dispute-Parsing Subsystem. This is a clean extraction boundary.

- **The guided workflow (define/interests/mode/converge/arbitrate) is a coherent unit.** These five commands form a linear prerequisite chain (`problem.md` -> `interests.md` -> `conversus.yml` -> execution -> arbitration) that represents a distinct user journey from the raw `run` engine. APM's skill model supports this as a "conversus-wizard" sub-skill.

- **APM's compilation system could reduce context pollution for conversus consumers.** A project consuming conversus does not need all four mode specifications loaded simultaneously. APM's `applyTo` pattern matching and distribution scoring could place mode-specific instructions closer to where they are needed, though this requires the skill to be restructured as instructions rather than a monolithic skill body.

- **The `apm.yml` already declares `type: skill` and `target: all`.** The package is APM-aware. The infrastructure for sub-skill promotion exists — the issue is that no `.apm/skills/` directory has been created yet.

## Missed Opportunities

- **No `.apm/skills/` directory exists despite the package declaring `type: skill`.** The conversus `apm.yml` sets `type: skill` and `target: all`, but the entire specification lives in a single root `SKILL.md`. APM's sub-skill promotion would deploy each sub-skill independently to `.github/skills/`, `.claude/skills/`, etc., enabling agent runtimes to load only the relevant subcommand's specification. This is a zero-cost structural change that immediately reduces context load.

- **Templates are not leveraging APM's resource bundling model.** The `templates/` directory contains mode-specific prompt engineering (7 templates per mode, 4 modes = 28 files). APM skills can bundle resources in `scripts/`, `references/`, `examples/`, and `assets/` subdirectories that stay in `apm_modules/` for agent reference. The templates could be organized as bundled resources within their respective mode sub-skills, making the template-to-mode relationship explicit in the package structure.

- **The preset system reinvents package-level dependency composition.** Preset resolution (qualified names, ambiguity detection, `composable` flags, composition templates for 2-3 presets) parallels APM's dependency resolution. If presets were individual APM packages (or sub-packages in a monorepo skill collection), consumers could `apm install conversus/presets/philosophy/mechanist` and get the preset integrated into their skill directory. The composition templates could be APM-level composition rather than runtime string interpolation.

- **The Dispute-Parsing Subsystem is a stable interface with no separate specification.** It has defined inputs (synthesis file path), outputs (boolean + integer), parsing rules (structural markers, heading fallback, defaults), and a stable interface contract. This is a reusable component that any conversus consumer or extension needs. It should be documented as a standalone context file (`.context.md`) or instruction set, not buried in the middle of the run engine specification.

- **The antipattern catalog (`antipatterns/catalog.md`) is not an APM context file.** APM's `.apm/context/` directory is designed for exactly this kind of project knowledge — background information agents should be aware of. Making it a context primitive would let APM's compilation system include it at the appropriate scope.

- **Mode-specific sections could be APM instructions with `applyTo` targeting.** The four competition modes (cooperative, winner-take-all, prisoners-dilemma, red-blue) have distinct review sections, cross-review sections, phase differences, and synthesis outputs. These could be `.instructions.md` files with `applyTo` patterns targeting the mode's template directory, enabling APM's context optimizer to load only the relevant mode's specification when an agent is working within that mode's templates.

- **No version pinning between SKILL.md and templates.** The SKILL.md references template variables (`{AGENT_NAME}`, `{CROSS_REVIEWS_OF_ME}`, etc.) that must match the actual template files. APM's version management could enforce this contract — a template package version must match the skill version that references it. Currently, drift between SKILL.md variable contracts and template content is caught only by the linter at `linter/validate.py`, not by the package system.

- **The `schema/` directory (variables.yml, modes/*.yml) is a natural APM context artifact.** The schema files define the authoritative variable contract for templates. This is reference documentation that APM's context primitive model handles well — it would be discoverable by agents working on template authoring.

- **The linter (`linter/validate.py`) could be an APM hook.** APM supports lifecycle hooks (PreToolUse, PostToolUse, Stop) that run scripts at specific points. A PostToolUse hook triggered on template file writes could run the linter automatically, ensuring template validity without manual invocation.

## Off-Base Assumptions

- **Extracting presets as fully independent APM packages is premature.** The spec (011a) implies presets could be an "APM package." But presets are tightly coupled to conversus's composition template system (the two-preset and three-preset composition templates in SKILL.md). A preset outside conversus has no meaning — it is not a general-purpose agent definition but a conversus-specific personality fragment. The right APM model is sub-skills within the conversus package (`.apm/skills/presets/SKILL.md`), not standalone packages. Distribution as independent packages only makes sense if presets develop a consumer base beyond conversus itself.

- **APM compile cannot currently optimize within a single SKILL.md.** The spec mentions that APM compile could "merge multiple sources into a single CLAUDE.md." This is true for instructions, but skills are not subject to the context optimization engine's `applyTo`-based placement algorithm. Skills are copied whole to `.github/skills/`. The benefit of splitting conversus into sub-skills is not compile-time optimization but load-time selectivity — agent runtimes can choose which sub-skill to read. This is a distribution benefit, not a compilation benefit.

- **The guided workflow is not separable from the run engine at the APM level.** While the wizard (define/interests/mode/converge/arbitrate) is conceptually a "separate skill," it deeply references the run engine's configuration schema, template variables, and dispute-parsing subsystem. Packaging it as a standalone APM skill that depends on a "conversus-engine" skill introduces a dependency chain that APM resolves at install time, but creates a two-package maintenance burden for what is currently a single-team, single-project framework. The right boundary is a sub-skill within the same package, not a separate package.

## Actionable Recommendations

1. **Create `.apm/skills/` directory with three sub-skills immediately.** Split the monolithic SKILL.md into: (a) `conversus-engine` — the run command, template system, dispute parsing, multi-round execution, and arbitration engine; (b) `conversus-wizard` — define, interests, mode, converge, and arbitrate commands with their prerequisite chain; (c) `conversus-gate` — the gate subcommand with its configuration schema, result schema, and CI/CD integration. Keep the root `SKILL.md` as a brief dispatcher that routes to sub-skills. This uses APM's sub-skill promotion to deploy each piece independently to `.github/skills/`, reducing per-invocation context load from 2200 lines to ~400-800 per sub-skill.

2. **Move mode specifications into separate context files.** Create `.apm/context/modes/cooperative.context.md`, `winner-take-all.context.md`, etc. Each context file contains that mode's review sections, cross-review sections, phase differences, and scoring rules. The engine sub-skill references these via APM's context linking (`[cooperative mode details]`). This eliminates the need for agents to process all four modes' specifications when only one is active.

3. **Register the presets directory as a sub-skill, not a separate package.** Create `.apm/skills/conversus-presets/SKILL.md` that documents the preset schema, resolution rules, composition templates, and lists available presets by category. The actual preset `.yml` files remain in `presets/` as bundled resources. This makes presets discoverable via APM's skill system without the overhead of independent package management. If presets later develop external consumers, they can be promoted to a standalone package at that point.

4. **Extract the Dispute-Parsing Subsystem into `.apm/context/dispute-parsing.context.md`.** This stable interface (structural markers, heading-based fallback, mode-specific parsing rules) is referenced by the run engine, the gate system, and the converge handler. Making it an explicit context file with APM linking ensures every sub-skill that depends on it references the same canonical definition. Changes to parsing rules propagate through the link graph.

5. **Convert the antipattern catalog to an APM context primitive.** Move `antipatterns/catalog.md` to `.apm/context/antipatterns.context.md` (or keep it in place and add a context primitive that references it). This makes it discoverable by APM's compilation system and linkable from other primitives. The antipattern check instruction in SKILL.md becomes a link to the context file rather than an inline reference.

6. **Add a PostToolUse hook for template validation.** Create `.apm/hooks/template-validation.json` that triggers `linter/validate.py` when files in `templates/` are modified. This replaces the manual "run `uv run python linter/validate.py`" instruction with automated enforcement. APM's hook integration deploys this to `.github/hooks/` or `.claude/settings.json` depending on the target.

7. **Add `schema/variables.yml` and `schema/modes/*.yml` as context primitives.** These define the authoritative template variable contract. Creating `.apm/context/template-schema.context.md` that references these files makes them available to agents authoring or modifying templates, without requiring them to know the schema directory exists.

8. **Defer full APM distribution (separate `apm install conversus` package) until spec suite stabilizes.** The conversus spec suite is actively evolving (011a is the current spec). Every SKILL.md structural change during this phase would require version bumps and potential dependency resolution changes if conversus were a distributed package. Keep conversus as a submodule with APM-aware internal structure (`.apm/` directory, sub-skills, context primitives) but do not publish it to a package registry until the spec development cadence slows. The structural improvements in recommendations 1-7 provide the context-reduction benefits without the distribution overhead.

9. **Use APM's `target: all` to validate sub-skill deployment across agent runtimes.** The current `apm.yml` already declares `target: all`. After splitting into sub-skills, run `apm install` locally to verify that sub-skills are correctly promoted to `.github/skills/`, `.claude/skills/`, and `.cursor/skills/`. This validates that the structural split works with APM's deployment machinery before any external distribution.

10. **Document the sub-skill dependency graph in the root SKILL.md.** After splitting, the root `SKILL.md` should contain: (a) the subcommand dispatch table (already present), (b) a dependency graph showing which sub-skill handles which subcommand, and (c) the shared interfaces (dispute-parsing, template variable contracts) that cross sub-skill boundaries. This keeps the root SKILL.md lightweight (~100-150 lines) while giving agents enough context to route to the right sub-skill.

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/SKILL.md` — the monolithic skill specification under review (2215 lines)
- `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md` — the spec motivating this review
- `<HOME>/code/payer-index-mono/apm/docs/src/content/docs/guides/skills.md` — APM skills guide: sub-skill promotion, SKILL.md format, bundled resources, multi-skill packages
- `<HOME>/code/payer-index-mono/apm/docs/src/content/docs/guides/compilation.md` — APM compilation guide: context optimization, `applyTo` placement, instruction distribution scoring
- `<HOME>/code/payer-index-mono/apm/docs/src/content/docs/introduction/key-concepts.md` — APM key concepts: primitive types (instructions, agents, skills, context, hooks), context linking, discovery
- `<HOME>/code/payer-index-mono/conversus/README.md` — conversus overview: game theory framework, competition modes, architectural invariant
- `<HOME>/code/payer-index-mono/conversus/apm.yml` — current APM manifest: `type: skill`, `target: all`, version 0.1.0
