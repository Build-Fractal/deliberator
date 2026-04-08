# Cooperative Review — agents-md-specialist

## Executive Summary

The conversus system currently maintains three agent-facing files at its root: `SKILL.md` (119KB, the full orchestration specification), `AGENTS.md` (a 51-line project overview and contribution guide), and `README.md` (human documentation). The existing AGENTS.md is well-positioned but underutilized. It covers project overview, structure, and basic contribution rules, but stops short of the contribution depth that would make it genuinely useful to agents working *on* conversus (as opposed to agents *using* conversus via `/conversus run`). The spec's central question — how to decompose the 2216-line SKILL.md — creates an opportunity to clarify what belongs in each file format, but also risks conflating two distinct audiences: agents executing the conversus skill versus agents contributing to the conversus codebase.

AGENTS.md and SKILL.md serve fundamentally different purposes and should not be viewed as alternatives. SKILL.md is an executable specification — it has YAML frontmatter, activation logic, tool permissions, and a runtime contract. No other agent besides Claude Code (or a compatible runtime) can interpret it. AGENTS.md is a universal contribution guide — every major coding agent reads it, and it requires no tooling integration. The decomposition discussion should preserve this separation: SKILL.md stays as the execution specification (ideally slimmed via reference files), and AGENTS.md grows into a proper contribution guide for the templates, schema, linter, and presets directories. The two formats are complementary layers, not competing approaches.

The missed opportunity is in the subdirectories. The `templates/`, `presets/`, `schema/`, and `linter/` directories each have their own conventions, file-naming rules, and validation requirements that any contributing agent needs to understand. Today, those rules are buried in the monolithic SKILL.md (template naming on line ~283, preset validation on line ~139, schema structure in `schema/variables.yml`, linter invocation on line ~309). Nested AGENTS.md files in each subdirectory would surface these rules to any agent — Claude Code, Copilot, Cursor, Windsurf, Junie — at the point where they are editing files. This is the highest-value use of AGENTS.md in conversus.

## Alignment

- **The existing AGENTS.md correctly separates from README.md.** The README is 14KB of human-facing documentation covering architecture, competition modes, and configuration. The AGENTS.md is a lean 51-line agent-oriented guide. This separation aligns with the agents.md standard's core principle: "README.md files are for humans; AGENTS.md complements this" (`conversus/references/agents-md.md`, line 27-29).

- **The existing AGENTS.md already covers the most critical agent need: how to run the system.** The "How to run" section with the three-step process (create config, run skill, check output) is exactly what an agent needs to use conversus as a tool. This is well-done.

- **The "When developing this package" section correctly identifies the template-mode invariant.** The rule that new modes require all 5 templates and that file names must match phases is the kind of structural constraint that prevents silent breakage. This belongs in AGENTS.md.

- **SKILL.md's frontmatter (`allowed-tools`, `compatibility`, activation) has no AGENTS.md equivalent.** The spec correctly notes that SKILL.md has features AGENTS.md cannot replicate: YAML frontmatter, tool permissions, activation triggers. The decomposition should not attempt to move executable specification into AGENTS.md.

- **The spec's proposal (line 4 of the spec.md) to look at agents.md as an offloading target is reasonable but bounded.** AGENTS.md can absorb contribution guidelines, code style, testing commands, and PR instructions. It cannot absorb execution logic, template variable contracts, or phase orchestration rules.

- **The conversus AGENTS.md's structure section is already slightly outdated.** It lists `tasks/` (no longer present based on the directory listing) and omits `schema/`, `linter/`, `presets/`, `antipatterns/`, and `.specify/`. This staleness is itself evidence that the AGENTS.md needs more active maintenance — or that nested AGENTS.md files in subdirectories would be more maintainable than a monolithic root-level structure map.

## Missed Opportunities

- **No nested AGENTS.md files in subdirectories.** The `templates/`, `presets/`, `schema/`, and `linter/` directories each have strict conventions. The agents.md standard explicitly supports nesting: "Place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree" (`conversus/references/agents-md.md`, line 146). A `templates/AGENTS.md` could specify: mode directories must contain exactly 7 files (review.md, cross-review.md, revision.md, disputes.md, synthesis.md, arbitration.md, cross-round-synthesis.md); template variables use `{UPPER_SNAKE}` syntax; the draft marker `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` blocks production use. This is pure contribution guidance — exactly what AGENTS.md was designed for.

- **No `presets/AGENTS.md` for preset contribution rules.** The SKILL.md (lines 139-200) defines preset file validation: `name` must match filename, `category` must match parent directory, `composable` field semantics, max 3 presets per composition. A `presets/AGENTS.md` would surface these rules at the point of contribution. Currently, an agent editing a preset in Cursor or Copilot has no way to discover these constraints — they are locked inside a Claude Code-specific SKILL.md.

- **No `schema/AGENTS.md` for schema contribution rules.** The `schema/variables.yml` file is the authoritative variable contract (SKILL.md line 300). The `schema/modes/` directory contains per-mode schemas. An agent adding or modifying a variable needs to know: update `variables.yml`, update the relevant `modes/{mode}.yml`, and run the linter. This workflow is invisible outside SKILL.md.

- **No `linter/AGENTS.md` for development workflow.** The linter is a Python package with `validate.py`, `models.py`, and `test_validate.py`. The testing command (`uv run python linter/validate.py`) is only documented in SKILL.md (line 309). A `linter/AGENTS.md` would tell any agent: how to run tests (`uv run pytest linter/`), how to run validation (`uv run python linter/validate.py`), and what the expected output looks like.

- **The root AGENTS.md does not mention the linter or schema validation.** An agent contributing a new template has no signal from AGENTS.md that validation exists or is required before submitting changes. The "When developing this package" section should reference template validation as a required pre-commit check.

- **No cross-agent testing instructions.** The AGENTS.md says "Test by running `/conversus run` against the example config" — but this only works in Claude Code. For agents that cannot invoke skills (Copilot, Cursor, Codex), there should be a fallback: run the linter, check template completeness, validate preset schemas. These are agent-agnostic checks that AGENTS.md should document.

- **The AGENTS.md does not mention the antipattern catalog.** The SKILL.md (line 239) requires agents to check `antipatterns/catalog.md` before proposing changes. This is a contribution guideline, not an execution rule — it belongs in AGENTS.md (or a nested `antipatterns/AGENTS.md`).

- **No PR or commit message conventions.** The agents.md standard highlights PR instructions as a core use case (examples section, line 87-90 of the reference). The conversus AGENTS.md has none. Even basic rules like "template changes require linter validation" or "preset additions must include a description field" would prevent common contribution errors.

- **AGENTS.md does not reference the CLAUDE.md.** The `CLAUDE.md` at the conversus root is auto-generated and contains active technologies and recent changes. The AGENTS.md should note the existence and purpose of CLAUDE.md so agents that read both understand the relationship.

## Off-Base Assumptions

- **AGENTS.md cannot replace any part of SKILL.md's execution specification.** The spec (line 5-7 of spec.md) lists agents.md alongside agentskills.io and APM as "opportunities to offload some of the work." For agentskills.io reference files and APM packages, this is accurate — they can absorb execution-relevant content into referenceable units. But AGENTS.md is contribution-oriented, not execution-oriented. Moving template variable contracts, phase orchestration rules, or dispute-parsing logic into AGENTS.md would make them invisible to the conversus runtime. AGENTS.md can reduce SKILL.md's size only by absorbing contribution guidelines currently mixed into the execution spec — a modest but real saving.

- **Cross-agent compatibility is valuable but not the primary driver.** The spec's framing (conversus.yml line 97: "if conversus is used in repos with Copilot, Cursor, etc.") implies that multi-agent compatibility is a key benefit. In practice, conversus is a Claude Code skill — other agents cannot execute `/conversus run`. The cross-agent benefit is for agents *contributing to* the conversus codebase, not agents *using* conversus. This is still valuable (the conversus repo could receive contributions from any agent), but the audience is narrower than implied.

- **Nearest-file-wins semantics do not create a hierarchy for execution.** The agents.md standard's nesting model (nearest file takes precedence) is designed for contribution context, not for building execution pipelines. Some decomposition proposals might assume nested AGENTS.md files can define a "template execution contract" that the skill runtime reads — they cannot. The runtime reads SKILL.md and its reference files. AGENTS.md is read by the IDE/agent at edit time, not by the conversus engine at run time.

## Actionable Recommendations

1. **Create `templates/AGENTS.md` with template contribution rules.** Content: required files per mode directory (7 files), variable syntax (`{UPPER_SNAKE_CASE}`), structural markers (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`, `<!-- CONVERSUS:DISPUTES_BEGIN/END -->`), the rule that template heading changes must be coordinated with the dispute-parsing subsystem, and the command to validate templates (`uv run python linter/validate.py`). Estimated scope: 40-60 lines.

2. **Create `presets/AGENTS.md` with preset contribution rules.** Content: directory structure (category directories containing `.yml` files), naming invariant (filename matches `name` field, directory matches `category` field), required fields (`name`, `category`, `prompt`, `description`), optional fields (`composable`, `docs`), composition rules (max 3, `composable: false` blocks composition), and examples of well-formed presets. Estimated scope: 30-50 lines.

3. **Create `schema/AGENTS.md` with schema contribution rules.** Content: the role of `variables.yml` as the authoritative variable contract, per-mode schemas in `modes/`, the relationship between schema and linter validation, and the workflow for adding a new variable (add to `variables.yml`, add to relevant `modes/{mode}.yml`, update templates, run linter). Estimated scope: 25-40 lines.

4. **Create `linter/AGENTS.md` with development workflow.** Content: Python version requirement (3.12, from `.python-version`), how to set up the environment (`uv sync`), how to run the linter (`uv run python linter/validate.py`), how to run tests (`uv run pytest linter/`), what the linter checks (variable existence, required variables per phase+mode, required headings, structural markers), and how to interpret failures. Estimated scope: 30-45 lines.

5. **Update the root `conversus/AGENTS.md` to reference nested files and fix staleness.** Remove the `tasks/` entry from the structure section. Add `schema/`, `linter/`, `presets/`, and `antipatterns/` to the structure. Add a note that each subdirectory has its own AGENTS.md with contribution-specific rules. Add a "Testing" section with the linter command as a pre-contribution check. Add a brief "Commit conventions" section (e.g., template changes require linter pass, preset additions must include description). Mention the antipattern catalog check.

6. **Do not move execution logic from SKILL.md to AGENTS.md.** The subcommand dispatch table, phase orchestration, template variable expansion, dispute-parsing subsystem, and agent isolation rules are all runtime specifications. They belong in SKILL.md (or in agentskills.io reference files that SKILL.md points to). AGENTS.md should reference SKILL.md for execution details, not duplicate them.

7. **Add a "Relationship between files" section to the root AGENTS.md.** Explicitly state: `SKILL.md` is the executable specification read by the conversus runtime (Claude Code); `AGENTS.md` (this file and nested copies) is the contribution guide read by all coding agents; `README.md` is the human documentation; `CLAUDE.md` is auto-generated context. This prevents agents from conflating the purposes of each file.

8. **Extract contribution-oriented content from SKILL.md into AGENTS.md.** Specifically: the antipattern check instruction (SKILL.md line 239-244), the template naming convention (line 283-289), the preset file validation rules (lines 139-145), and the linter invocation (line 309). These are contribution guidelines currently embedded in an execution spec. Moving them to AGENTS.md (or nested AGENTS.md files) makes them discoverable by all agents while reducing SKILL.md's size. Estimated token savings: 200-400 tokens from SKILL.md (modest, but these are the lines most relevant to AGENTS.md's purpose).

9. **Keep AGENTS.md files under 100 lines each.** The agents.md standard does not prescribe a length, but the value proposition — a quick-reference for agents — degrades if the file becomes another documentation dump. Each nested AGENTS.md should cover: what this directory contains, naming/structure rules, validation commands, and common mistakes. No architecture explanations, no execution flows.

10. **Consider an `antipatterns/AGENTS.md` if the catalog grows.** Currently the catalog is small (one directory, one file). If it grows to multiple antipattern files with their own schema, a nested AGENTS.md would document the contribution format. For now, a mention in the root AGENTS.md is sufficient.

## Referenced Documentation

- `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md` — the monolithic execution specification (2216 lines, 119KB)
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md` — the decomposition spec triggering this review
- `/Users/business-daddy/code/payer-index-mono/conversus/references/agents-md.md` — the agents.md community standard reference
- `/Users/business-daddy/code/payer-index-mono/conversus/README.md` — human-facing documentation for conversus
- `/Users/business-daddy/code/payer-index-mono/conversus/AGENTS.md` — the existing agents.md file (51 lines)
- `/Users/business-daddy/code/payer-index-mono/conversus/CLAUDE.md` — auto-generated project context
- `/Users/business-daddy/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus.yml` — the deliberation configuration for this review
