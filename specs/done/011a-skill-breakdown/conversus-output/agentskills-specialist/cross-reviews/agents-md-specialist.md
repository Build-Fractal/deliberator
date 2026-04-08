# Cross-Review of agents-md-specialist

Reviewer: **agentskills-specialist**

---

## Dangerous Contradictions

### 1. Extracting contribution-oriented content from SKILL.md into AGENTS.md risks breaking execution correctness

agents-md-specialist recommends (Actionable Recommendation 8): "Extract contribution-oriented content from SKILL.md into AGENTS.md. Specifically: the antipattern check instruction (SKILL.md line 239-244), the template naming convention (line 283-289), the preset file validation rules (lines 139-145), and the linter invocation (line 309)."

My review (Missed Opportunities, bullet 1) recommends extracting each subcommand handler to its own reference file under `references/`, with the SKILL.md dispatch table routing to them on demand.

The contradiction: agents-md-specialist treats preset file validation rules (lines 139-145) as "contribution guidelines currently embedded in an execution spec." They are not. The preset validation rules are runtime specification -- the run engine executes them during config parsing before any agent launches. If an agent invokes `/conversus run` with a preset-bearing config, the engine must enforce `name` matching filename, `category` matching parent directory, `composable: false` blocking composition, and the 3-preset maximum. These rules are procedural execution logic, not contribution guidance. Moving them to AGENTS.md would remove them from the execution path entirely, since the conversus runtime reads SKILL.md and its reference files, not AGENTS.md. The correct destination for these rules is `references/preset-resolution.md` (my Recommendation 7), loaded on demand when the config contains a `preset:` field. agents-md-specialist's own Off-Base Assumptions section acknowledges this boundary ("AGENTS.md cannot replace any part of SKILL.md's execution specification") but Recommendation 8 contradicts it by moving validation rules that are invoked at runtime.

### 2. Nested AGENTS.md files create a maintenance burden that contradicts the staleness problem agents-md-specialist already identified

agents-md-specialist notes (Alignment, bullet 6): "The conversus AGENTS.md's structure section is already slightly outdated. It lists `tasks/` (no longer present) and omits `schema/`, `linter/`, `presets/`, `antipatterns/`." This staleness is cited as evidence that nested AGENTS.md files would be "more maintainable than a monolithic root-level structure map."

My review does not address AGENTS.md maintenance because AGENTS.md is outside the agentskills.io specification's scope. But the underlying logic is contradictory: if the root AGENTS.md (51 lines, covering one directory) already drifts out of sync, adding four more AGENTS.md files (templates/, presets/, schema/, linter/) at 30-60 lines each multiplies the surface area for staleness by 5x. The conversus project is a specification-only codebase with no CI pipeline to enforce AGENTS.md correctness. The linter validates template structure and schema variables, not AGENTS.md accuracy. Each new nested file is another document that silently decays.

The agentskills.io progressive disclosure model addresses the same need -- surfacing context-specific rules -- but through reference files that are actively loaded by the skill runtime and therefore fail visibly when they drift from the codebase. A `references/handler-run.md` that references a nonexistent template file will produce a runtime error. A `templates/AGENTS.md` that lists the wrong required files will silently mislead contributing agents with no feedback mechanism.

### 3. The "200-400 token savings" estimate understates the real decomposition opportunity and may anchor implementation too low

agents-md-specialist estimates (Recommendation 8): "Estimated token savings: 200-400 tokens from SKILL.md (modest, but these are the lines most relevant to AGENTS.md's purpose)."

My review (Executive Summary) identifies that the SKILL.md is approximately 31,000 tokens against a recommended budget of 5,000 tokens, and that restructuring via progressive disclosure could reduce the always-loaded body from 31k tokens to approximately 4,000-5,000 tokens -- a reduction of 26,000+ tokens. The dangerous contradiction is not in the math but in the framing: if the implementation team reads both reviews, agents-md-specialist's framing positions AGENTS.md extraction as the primary decomposition mechanism with a "modest" payoff, while the actual high-impact mechanism is subcommand handler extraction to reference files. An implementation that prioritizes AGENTS.md extraction first could consume the spec's budget (time, review cycles) on a 200-400 token improvement while leaving the 26,000-token problem unaddressed. The two approaches are not competing -- they address different audiences -- but the relative priority must be clear: progressive disclosure via reference files is the structural fix; AGENTS.md is a complementary improvement for cross-agent contribution discoverability.

### 4. Recommending AGENTS.md as an offloading target conflates two distinct audiences the spec must separate

agents-md-specialist correctly identifies two audiences (Executive Summary): "agents executing the conversus skill versus agents contributing to the conversus codebase." But several recommendations blur this distinction in practice. Recommendation 1 proposes a `templates/AGENTS.md` containing "the command to validate templates (`uv run python linter/validate.py`)" and "structural markers (`<!-- CONVERSUS:TEMPLATE_STATUS: draft -->`)." The draft marker is not a contribution guideline -- it is a runtime gate. The SKILL.md uses `TEMPLATE_STATUS: draft` to block production use of incomplete templates during execution. An agent contributing a new template does need to know the marker exists, but the authoritative definition of what that marker means to the runtime must remain in the execution specification (SKILL.md or a reference file). Duplicating it in AGENTS.md creates two sources of truth for a runtime-critical flag: one read by the execution engine, one read by contributing agents, with no mechanism to keep them synchronized.

---

## Tensions

### 1. Cross-agent discoverability versus single-runtime reality

agents-md-specialist frames nested AGENTS.md files as enabling contribution from Copilot, Cursor, Windsurf, and Junie (Missed Opportunities, bullets 1-4). My review acknowledges the single-runtime reality: "The `compatibility` field correctly notes the requirement for an agent runtime that supports background Agent tool dispatch." The tension is genuine -- conversus is a Claude Code skill today, but the codebase could receive contributions from any agent. However, agents-md-specialist's Recommendation 9 ("keep AGENTS.md files under 100 lines each") implicitly acknowledges that the contribution surface is small: template naming, preset schema, linter commands. The question is whether four new files averaging 40 lines each (160 lines total) justify the maintenance cost when the same information could live in a single expanded root AGENTS.md of ~120 lines. Both approaches serve cross-agent discoverability; the nested approach optimizes for directory-scoped context at the cost of more files to maintain.

### 2. Where validation rules belong: AGENTS.md contribution checks versus reference file execution contracts

agents-md-specialist recommends documenting validation rules in AGENTS.md files (Recommendations 1-4): template heading rules in `templates/AGENTS.md`, preset schema rules in `presets/AGENTS.md`, linter invocation in `linter/AGENTS.md`. My review recommends consolidating validation rules in `references/validation-rules.md` (Recommendation 5). Both serve the goal of surfacing validation expectations, but they serve different consumers: AGENTS.md tells a contributing agent what to check before submitting; a reference file tells the executing agent what to enforce at runtime. The tension: should the validation contract be documented once (in the reference file, with AGENTS.md pointing to it) or twice (authoritatively in the reference file, summarized in AGENTS.md)? Documenting once risks making validation invisible to non-Claude-Code contributors. Documenting twice risks drift between the summary and the authority.

### 3. Scope of the "file relationship" section: static explanation versus dynamic routing

agents-md-specialist's Recommendation 7 proposes a "Relationship between files" section in the root AGENTS.md explaining that SKILL.md is the executable spec, AGENTS.md is the contribution guide, README.md is human docs, and CLAUDE.md is auto-generated context. My review's Recommendation 2 proposes keeping the dispatch table, core invariants, and a phase-level flow summary in SKILL.md as the "always-loaded core." These are compatible, but there is tension in how much architectural context AGENTS.md should carry. agents-md-specialist's version is a static explanation of file purposes. The agentskills.io model would have the SKILL.md itself route to the right reference file dynamically based on the invocation. A contributing agent needs the static map; an executing agent needs the dynamic routing. The risk is that the static map in AGENTS.md becomes a parallel (and potentially stale) description of the routing that SKILL.md performs authoritatively.

### 4. Token budget awareness: agents-md-specialist's review does not engage with the 5,000-token recommendation

My review centers the 500-line / 5,000-token specification constraint as the primary decomposition driver. agents-md-specialist's review does not reference this constraint at all. The agents.md standard has no equivalent size constraint -- AGENTS.md files can be any length (though Recommendation 9 suggests under 100 lines as a practical guideline). This creates a tension in prioritization: from the agentskills.io perspective, the decomposition is urgent (6x over budget); from the agents.md perspective, it is an opportunity to improve contribution discoverability. Both are valid, but a spec implementation that does not prioritize the token budget risks leaving the core problem (context window waste on every invocation) unresolved while adding new files that address a secondary concern.

### 5. The antipattern catalog: contribution guidance versus execution prerequisite

agents-md-specialist notes (Missed Opportunity, bullet 7): "The AGENTS.md does not mention the antipattern catalog. The SKILL.md (line 239) requires agents to check `antipatterns/catalog.md` before proposing changes. This is a contribution guideline, not an execution rule -- it belongs in AGENTS.md." My review does not specifically address the antipattern catalog. The tension: the antipattern check is embedded in a SKILL.md instruction that fires during execution (the agent is told to read the catalog as part of its workflow). Is it a contribution guideline or an execution step? It functions as both -- a contributing agent should know antipatterns exist; an executing agent is instructed to consult them. Moving the instruction to AGENTS.md would remove it from the execution path. The resolution is likely to mention it in AGENTS.md while keeping the execution instruction in SKILL.md (or a handler reference file), but this again creates dual documentation of the same requirement.

---

## Safe Agreements

### 1. SKILL.md and AGENTS.md serve fundamentally different purposes and should not be conflated

agents-md-specialist (Executive Summary): "AGENTS.md and SKILL.md serve fundamentally different purposes and should not be viewed as alternatives. SKILL.md is an executable specification... AGENTS.md is a universal contribution guide."

My review (Off-Base Assumptions, bullet 1): "The current structure assumes all instructions must be immediately available" -- implicitly affirming that SKILL.md is the execution specification and that the decomposition should happen within the agentskills.io framework (reference files), not by migrating execution content to a different file format.

Both reviews agree that the two file formats are complementary layers addressing different audiences. Neither proposes replacing one with the other. This is the foundational agreement that makes the two reviews' recommendations composable rather than conflicting.

### 2. The existing SKILL.md frontmatter is well-crafted and should remain unchanged

agents-md-specialist (Alignment, bullet 4): "SKILL.md's frontmatter (`allowed-tools`, `compatibility`, activation) has no AGENTS.md equivalent. The decomposition should not attempt to move executable specification into AGENTS.md."

My review (Alignment, bullet 1): "The frontmatter is well-crafted. The `name`, `description`, `compatibility`, `license`, and `allowed-tools` fields follow the specification exactly."

Both reviews validate the frontmatter as correct and complete. Neither proposes changes to it. This agreement confirms that the decomposition work is entirely in the body content, not the metadata layer.

### 3. The linter and schema validation infrastructure should be more visible to contributors

agents-md-specialist (Missed Opportunity, bullet 5): "The root AGENTS.md does not mention the linter or schema validation. An agent contributing a new template has no signal from AGENTS.md that validation exists or is required before submitting changes."

My review (Alignment, bullet 4): "Template variable contracts are already externalized. The `schema/variables.yml` and `schema/modes/{mode}.yml` files, plus the linter at `linter/validate.py`, demonstrate that the project understands the value of separating machine-checkable contracts from prose instructions."

Both reviews recognize that the validation infrastructure exists but is insufficiently discoverable. agents-md-specialist recommends surfacing it in AGENTS.md files; my review recommends leveraging it as a natural seam for progressive disclosure into reference files. The mechanism differs, but the diagnosis is shared: the linter and schema validation are high-value assets that are currently invisible to agents that do not read the full 2216-line SKILL.md.

### 4. Contribution-oriented content that is currently mixed into SKILL.md can be separated without harming execution

agents-md-specialist (Recommendation 8): identifies specific lines in SKILL.md that are contribution guidelines embedded in an execution spec.

My review (Recommendation 8): recommends restructuring the "Important Notes" section to separate genuine gotchas from reference material.

Both reviews agree that SKILL.md contains content that is not execution logic -- contribution conventions, explanatory notes, worked examples for human readers. This content can be moved out of SKILL.md without affecting the runtime behavior of the skill. The disagreement is about destination (AGENTS.md vs. reference files), but the diagnosis that SKILL.md contains separable non-execution content is shared.
