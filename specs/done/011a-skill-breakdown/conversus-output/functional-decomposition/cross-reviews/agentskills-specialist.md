# Cross-Review of agentskills-specialist's Phase 1 Review

Reviewer: **functional-decomposition**
Target: agentskills-specialist's review of conversus SKILL.md decomposition (spec 011a)

---

## Dangerous Contradictions

### 1. Important Notes extraction vs. retention — divergent handling of the same content

**agentskills-specialist** (Recommendation 8) proposes splitting the "Important Notes" section: keep the 3-5 "genuine gotchas" in SKILL.md and move agent count formulas, worked examples, round/iteration orthogonality explanation, and the baseline feature inventory to `references/operational-notes.md`. The justification is that "the agent can derive the formulas from the phase structure" and these items serve documentation, not execution.

**My review** (Recommendation 10) proposes retaining both "Important Notes" and "Baseline Features" in SKILL.md in their entirety, on the grounds that they are gotchas — the highest-value content type per `agentskills-best-practices.md` L255-279, which warns that "the agent may not recognize the trigger" for loading a reference file containing non-obvious gotchas.

This matters because the items agentskills-specialist would extract are not merely informational — they include operational constraints the agent needs during execution. "Rounds and iterations are orthogonal" (SKILL.md L2201) prevents the agent from conflating the two during multi-round config parsing. "All subagents use the orchestrator's model" (L2198) prevents the agent from attempting per-agent model selection. If these are in a reference file that loads conditionally, the agent encounters the config before it encounters the constraint. The agentskills best practices explicitly warn against this pattern: "for non-obvious issues, the agent may not recognize the trigger" (L277). Moving these to a reference file creates a race between the agent's config-parsing logic and its awareness of the constraints that govern that logic.

**Resolution needed**: Classify each item in "Important Notes" individually. Items that constrain config interpretation (orthogonality, model selection, overwrite semantics) must stay in the always-loaded SKILL.md core. Items that are purely informational (worked formula examples, baseline feature inventory) can safely move to a reference file. A blanket extract-or-retain for the entire section is wrong in both directions.

### 2. Run engine core size — 300 lines vs. 265 lines, and the missing accounting

**agentskills-specialist** (Recommendation 2) targets a SKILL.md of "300-400 lines, under 5,000 tokens" after extracting all seven handlers. The proposed retained content is: frontmatter, dispatch table, non-negotiable multi-agent rules, a phase-level flow summary (one paragraph per phase), and a gotchas section.

**My review** (Recommendation 7) arrives at "approximately 345 lines" by a different path: keep the run engine core (~265 lines after extracting multi-round orchestration, preset resolution, and Dispute-Parsing), plus the dispatch table (~25 lines), shared notes (~35 lines), and frontmatter (~20 lines). Crucially, my decomposition does NOT extract the single-round run engine to a reference file — it stays in SKILL.md because `/conversus converge` and `/conversus gate` both delegate to it.

The danger is that agentskills-specialist's "one paragraph per phase" summary means the run handler itself becomes a reference file (`references/handler-run.md`). If `/conversus converge` invokes the run engine, the agent must now load SKILL.md + `references/handler-converge.md` + `references/handler-run.md` — a three-file chain where the converge handler tells the agent to go read the run handler. This creates a progressive-disclosure chain depth of 2, which the agentskills specification cautions against. More critically, if the agent fails to follow the chain (reads converge handler, starts running, does not load the run handler), it will attempt multi-phase orchestration with only a one-paragraph summary of each phase — a high-fragility failure mode that silently degrades output quality rather than producing an obvious error.

**Resolution needed**: The single-round run engine core must remain in SKILL.md, not be summarized to one paragraph per phase. The agentskills-specialist's 300-line target is achievable only if the run handler is extracted, but extracting it creates a fragile two-hop loading dependency that violates the principle of keeping high-fragility instructions in the always-loaded core.

### 3. Output schema placement — assets/ vs. inline, with missing impact analysis

**agentskills-specialist** (Recommendation 6) proposes moving output schema templates (problem.md schema, interests.md schema, gate-result.md schema) to `assets/`. The justification cites agentskills-best-practices.md: "Short templates can live inline in SKILL.md; for longer templates, or templates only needed in certain cases, store them in `assets/`."

**My review** does not address schema extraction at all — I treated schemas as part of their respective handler specifications (each handler carries its own output schema) and assumed they would move with the handler to the handler's reference file.

The contradiction is in the destination, not the extraction itself. If schemas go to `assets/`, they become standalone files divorced from their handler context. The agent executing `/conversus define` would need to load `references/handler-define.md` AND `assets/problem-schema.md` — two files for one subcommand. If schemas stay embedded in their handler reference files, the agent loads one file and has everything it needs.

The agentskills best practices quote is about templates the agent fills with variable content. But the conversus output schemas (problem.md, interests.md) are not fill-in-the-blank templates — they are structural contracts with required headings and validation rules. Separating the schema from the validation rules that check it creates a seam where drift can occur: someone updates the schema in `assets/` without updating the validation in the handler reference, or vice versa.

**Resolution needed**: Keep output schemas co-located with their handler specifications in `references/handler-*.md`, not in a separate `assets/` directory. The agentskills "assets/" recommendation applies to reusable templates, not to handler-specific structural contracts.

### 4. Token budget target — 5,000 tokens as hard ceiling vs. practical floor

**agentskills-specialist** (Off-Base Assumptions, final bullet) warns that "even aggressive restructuring to 500 lines would likely still exceed the 5,000 token recommendation if those lines are dense specification prose" and argues the target should be "token-aware, not just line-aware."

**My review** (Recommendation 9) proposes documenting the token budget per invocation path, with examples like `/conversus define` at ~5k tokens (core + handler) and `/conversus run` with multi-round + arbiter at ~10.5k tokens.

The contradiction: agentskills-specialist treats 5,000 tokens as a hard ceiling for the SKILL.md body, while my per-invocation budgets accept that any `/conversus run` invocation will exceed 5,000 tokens once the run engine core loads. The agentskills specification says "under 500 lines and 5,000 tokens" for SKILL.md — this is the always-loaded content. But agentskills-specialist's framing implies the total per-invocation load (SKILL.md + references) should also stay under 5,000 tokens, which is neither stated nor achievable for a skill this complex. If taken literally, this constraint would force decomposing the run engine core itself into multiple reference files, creating the fragile multi-hop loading problem described above.

**Resolution needed**: The 5,000-token target applies to the always-loaded SKILL.md body, not to the total per-invocation context. My per-invocation budget approach (Recommendation 9) is the correct framing: document expected total load per invocation path, accept that complex paths will exceed 5k, and ensure no single invocation path approaches the original 31k.

---

## Tensions

### 1. Granularity of extraction — seven reference files vs. fourteen

**agentskills-specialist** proposes 14 reference files (7 handler files + dispute-parsing + template-variables + validation-rules + preset-resolution + arbitration-engine + multi-round-execution + operational-notes). **My review** proposes 8 reference files (6 handler files + dispute-parsing + multi-round-orchestration), keeping validation, presets, and the arbitration engine embedded in their respective handlers or the SKILL.md core.

Both approaches serve progressive disclosure, but the tradeoff is different. More files means finer-grained conditional loading and smaller per-file token cost, but also more load-trigger instructions in SKILL.md and more opportunities for the agent to miss a needed reference. Fewer files means coarser loading (some irrelevant content loads with each handler) but simpler dispatch with fewer failure modes.

This is a genuine design tension with no objectively correct answer. The right granularity depends on empirical testing: does the agent reliably follow conditional load instructions for 14 files, or does it start skipping references after 6-7?

### 2. Dispute-Parsing Subsystem priority — P1 vs. medium impact

**agentskills-specialist** lists Dispute-Parsing extraction as Recommendation 3 with no explicit priority label, but positions it after the two highest-priority items (handler extraction and core retention). **My review** assigns it P1 priority, matching the handler extractions.

The tension: the subsystem is only ~30 lines. Extracting 30 lines to a reference file saves negligible context. The value is not in token savings but in making the stable interface contract physically addressable and independently loadable by four consumers. Agentskills-specialist correctly identifies the benefit ("reference material with a stable interface, loaded on demand") but the framing as a size-reduction measure undersells the real value. My P1 priority reflects the architectural benefit (eliminating a cross-cutting inline dependency), not the token savings.

### 3. Guided handler patterns — shared skeleton vs. independent handlers

**My review** (Missed Opportunities, bullet 5) identifies that the five guided handlers (define, interests, mode, converge, arbitrate) all implement an identical workflow pattern: check prerequisites, ingest input, validate, present for confirmation, write, post-write validate, report. I propose a `references/guided-handler-patterns.md` that defines the shared skeleton.

**agentskills-specialist** does not identify this pattern. Each handler is treated as fully independent, extracted to its own reference file with no shared structure.

The tension: extracting a shared pattern reduces per-handler size and eliminates drift between handlers' implementations of the same workflow. But it also creates an additional reference file the agent must load alongside the handler-specific file — back to the two-file-per-invocation problem. The agentskills best practices "bundling reusable scripts" recommendation (L382-384) supports extracting repeated logic, but the "design coherent units" recommendation (L146-148) warns against forcing multiple loads for a single task.

### 4. Treatment of agent count formulas — redundant vs. operational

**agentskills-specialist** (Off-Base Assumptions, bullet 3) argues the inline formulas (N^2 + 2N + 1) are "arithmetic that any LLM can derive from the phase structure" and the worked examples are "helpful for human readers of the spec but redundant for an agent."

**My review** treats the formulas as part of the operational notes that should stay in SKILL.md (Recommendation 10), because the agent uses them in the pre-execution report (SKILL.md L322: "This configuration will launch up to {max_total_agents} agents across {rounds} rounds").

The tension: if the agent can derive N^2 + 2N + 1 from the phase structure, the formula is redundant. But derivation is unreliable — the agent must count N reviews + N*(N-1) cross-reviews + N revisions + N dispute reports + 1 synthesis, which requires correctly interpreting the Phase 2 cross-review combinatorics (each agent reviews each OTHER agent, not each agent including itself). The formula is a gotcha-style correction: "the agent will get this wrong without this instruction." Whether LLMs reliably derive this combinatorial count is an empirical question, not an architectural one.

### 5. Conditional loading trigger specificity — event-based vs. config-based

**agentskills-specialist** (Recommendation 9) proposes conditional loading based on config fields: "If the config contains an `arbiter:` block, read `references/arbitration-engine.md`." "If `rounds > 1`, read `references/multi-round-execution.md`."

**My review** (Recommendation 8) proposes the same pattern but phrases triggers as subcommand-based: "When `/conversus gate` is invoked, read `references/gate-handler.md`."

The tension: subcommand-based triggers are unambiguous (the dispatch table routes to exactly one handler) but coarse-grained (the handler loads regardless of config). Config-based triggers are finer-grained but require the agent to parse the config before knowing which references to load. This creates a sequencing problem: the agent must read the config, then load the appropriate references, then parse the config again with the reference material in context. If the agent parses the config before loading the arbitration reference, it may mishandle the arbiter block. Both reviews propose conditional loading but neither addresses this sequencing issue.

---

## Safe Agreements

### 1. Extract all subcommand handlers to references/ files

Both reviews independently arrive at the same core recommendation with high confidence. **agentskills-specialist** (Recommendation 1): "Extract each subcommand handler to its own reference file." **My review** (Recommendations 1-2): "Extract gate handler" (P1) and "Extract guided handlers" (P1). Both reviews estimate the same token savings (~25k tokens removed from the always-loaded context), propose the same file naming convention (`references/handler-{name}.md`), and justify the extraction with the same agentskills specification citation (SKILL.md under 500 lines, references/ for on-demand content).

This is the highest-impact, lowest-risk change. Both reviews agree it should happen first.

### 2. The dispatch table and non-negotiable multi-agent rules must stay in SKILL.md

**agentskills-specialist** (Alignment, bullets 2-3; Recommendation 2): The dispatch table is "an exemplary implementation" that stays in SKILL.md; the multi-agent rules "correctly apply 'match specificity to fragility'" and must always be in context. **My review** (Alignment, bullets 1 and 5): The dispatch table is "textbook functional decomposition"; the multi-agent rules are "cross-cutting invariants" that constitute the highest-value gotchas.

Both reviews agree these are the two non-extractable elements. The dispatch table is the routing layer; the multi-agent rules are the highest-fragility invariants. Neither review considers extracting either one. This consensus reflects a shared understanding that the always-loaded SKILL.md core must contain the routing logic and the invariants whose violation produces silent, correlated failures.

### 3. The existing references/ and schema/ infrastructure makes extraction low-risk

**agentskills-specialist** (Alignment, bullets 4-5; Off-Base Assumptions, bullet 1): "Template variable contracts are already externalized" in schema/; "The references/ directory already exists with substantial content"; "Adding references/handler-run.md to the read list is not a new capability." **My review** (Off-Base Assumptions, bullet 2): "The most impactful decomposition requires no tooling changes — it is purely structural, moving sections of SKILL.md into references/ files."

Both reviews agree that the decomposition is a content reorganization, not a technology migration. The infrastructure for progressive disclosure already exists — the SKILL.md simply has not been restructured to use it. This agreement de-risks the recommendation: no new directories need to be created, no new tools need to be approved, and the agent is already performing file I/O on every run.

---

## Referenced Documents

- agentskills-specialist review: `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/agentskills-specialist/review.md`
- functional-decomposition review: `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/conversus-output/functional-decomposition/review.md`
- SKILL.md: `<HOME>/code/payer-index-mono/conversus/SKILL.md`
- spec 011a: `<HOME>/code/payer-index-mono/conversus/specs/011a-skill-breakdown/spec.md`
- agentskills best practices: `<HOME>/code/payer-index-mono/conversus/references/agentskills-best-practices.md`
