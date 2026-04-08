# Cross-Review of integration-specialist's Review

Reviewer: **agents-md-specialist**

---

## Dangerous Contradictions

### 1. Multi-Agent Isolation Rules: "Keep prominent" vs "Make discoverable to all agents"

integration-specialist argues that the multi-agent isolation rules (SKILL.md lines 324-336) "should remain in the root SKILL.md rather than being buried in a reference file, because they are the most important constraint an implementing agent must internalize" (Alignment, bullet 6). I agree these rules are critical for the conversus *runtime*. However, this framing assumes only Claude Code will ever need to understand these invariants. If an agent contributing to conversus via Copilot or Cursor modifies templates or adds a new mode, it needs to understand that templates are designed for isolated, parallel execution — otherwise it might introduce cross-agent dependencies into template prompts. My review (Missed Opportunities, bullet 6) identifies that cross-agent testing instructions are entirely absent.

The danger: if isolation rules live *only* in SKILL.md, a non-Claude-Code contributor can unknowingly violate the isolation contract when editing templates, because no AGENTS.md surfaces this constraint. integration-specialist's recommendation to keep these rules exclusively in the root SKILL.md creates a blind spot for the growing set of agents that read AGENTS.md but cannot read SKILL.md frontmatter or activation logic. The isolation rules have two audiences: the runtime executor (SKILL.md) and the template contributor (AGENTS.md). Both need a version — the AGENTS.md version as a contribution constraint ("templates must not assume cross-agent visibility"), the SKILL.md version as an execution invariant.

### 2. Reference Files for Handlers vs Nested AGENTS.md: Competing Discovery Mechanisms

integration-specialist proposes extracting each guided workflow handler to `references/handler-{name}.md` (Recommendation 2) and each subsystem to `references/subsystem-{name}.md` (Recommendations 4-5). My review proposes nested `AGENTS.md` files in `templates/`, `presets/`, `schema/`, and `linter/` (Recommendations 1-4). These are not the same thing, but they overlap dangerously in scope.

Consider the preset contribution rules. integration-specialist's `references/subsystem-preset-resolution.md` would contain the resolution algorithm, composition rules, and error conditions — visible only to agents loading SKILL.md reference files (Claude Code). My proposed `presets/AGENTS.md` would contain the same naming invariants, required fields, and composition limits — visible to any agent editing files in `presets/`. If both exist, we have two sources of truth for preset constraints. If they drift, a Cursor agent following `presets/AGENTS.md` and a Claude Code agent following `references/subsystem-preset-resolution.md` will enforce different rules on the same files. Neither review addresses how to prevent this duplication from becoming contradiction. One file must be authoritative and the other must explicitly defer.

### 3. "Do Not Decompose" Boundary Around the Run Engine Conflicts with AGENTS.md Contribution Needs

integration-specialist defines a hard "do not decompose" boundary around the round loop, iteration loop, output path computation, and termination logic (Recommendation 7, lines 346-580). The rationale is sound from a runtime perspective: these are tightly coupled state machines. But this creates a 230+ line block within the root SKILL.md that is irrelevant to agents contributing templates, presets, or schema files — yet they must load it if they load SKILL.md.

My review (Off-Base Assumptions, bullet 3) notes that AGENTS.md cannot replace execution specification. But integration-specialist's "do not decompose" stance means that even after all the proposed extractions, the root SKILL.md would still contain ~400-500 lines (their own estimate, Recommendation 1) of dense engine logic. This is the content most likely to confuse a contributing agent that loads SKILL.md looking for contribution context. The contradiction: integration-specialist wants SKILL.md to remain the single source for engine logic (correct for runtime), but this forces contribution-focused agents to wade through execution state machines they cannot act on. My nested-AGENTS.md proposal mitigates this by giving contributors a separate entry point, but integration-specialist's review does not acknowledge the need for this alternative entry point at all.

### 4. Error Message Contracts: Implicit Disagreement on Where Contribution Validation Lives

integration-specialist identifies error message contracts as a missed opportunity in the spec (Missed Opportunities, bullet 6): "If validation logic moves to reference files, these error messages become part of the interface contract." They recommend that error messages should be explicitly assigned to either the reference file or the root SKILL.md. My review (Recommendation 1, Recommendation 4) places validation commands and expected output descriptions in nested AGENTS.md files — specifically, the linter's expected output and how to interpret failures.

The danger is that integration-specialist's error catalogue would live in `references/contract-{name}.md` files (their naming convention, Recommendation 9), which are Claude Code-only artifacts. Meanwhile, my `linter/AGENTS.md` would describe linter failure messages for all agents. If a new validation error is added to the reference contract but not to the linter AGENTS.md (or vice versa), contributing agents will have inconsistent expectations about what validation failures mean. Neither review proposes a single-source-of-truth mechanism for error definitions that serves both audiences.

---

## Tensions

### 1. Internal Coherence First vs Cross-Agent Compatibility First

integration-specialist states: "the decomposition must first serve the conversus orchestrator's internal coherence. External packaging (APM) or cross-agent compatibility (agents.md) are distribution concerns that should not drive internal decomposition boundaries" (Off-Base Assumptions, bullet 2). My review argues that nested AGENTS.md files are the "highest-value use of AGENTS.md in conversus" (Executive Summary) and that contribution-oriented content should be extracted from SKILL.md into AGENTS.md (Recommendation 8).

These are not contradictory, but they create a priority tension. integration-specialist would design the decomposition entirely around runtime coherence and then apply AGENTS.md as a packaging layer. I would identify contribution boundaries first and let them inform where runtime content should be refactored. In practice, the decomposition boundaries are likely the same either way — but the *sequencing* matters for the spec's implementation plan. If internal coherence drives the work, AGENTS.md creation becomes a follow-up task that may be deprioritized. If contribution discoverability is a first-class concern, AGENTS.md creation happens in parallel with reference-file extraction.

### 2. Antipattern Catalog: Orchestrator-Level vs Handler-Level Check

integration-specialist raises a sharp question: "If each handler becomes a reference file, does each handler need its own antipattern check, or is this an orchestrator-level concern?" (Missed Opportunities, bullet 3). My review (Missed Opportunities, bullet 7) approaches the same artifact from the AGENTS.md angle: "The SKILL.md requires agents to check `antipatterns/catalog.md` before proposing changes. This is a contribution guideline, not an execution rule — it belongs in AGENTS.md."

The tension: integration-specialist frames the antipattern check as a runtime orchestration decision (where in the execution flow does it fire?), while I frame it as a contribution workflow step (agents should check the catalog before editing). Both are correct, but they imply different placements. If the antipattern check is an orchestrator-level pre-execution step, it stays in the root SKILL.md. If it is a contribution guideline, it moves to AGENTS.md. In reality, it is both — but neither review proposes a clean way to serve both purposes without duplication.

### 3. Naming Convention Scope

integration-specialist proposes a three-tier naming convention: `handler-{name}.md`, `subsystem-{name}.md`, `contract-{name}.md` (Recommendation 9). This is purely for the `references/` directory that SKILL.md points to. My proposed nested AGENTS.md files follow the agents.md standard's convention: just `AGENTS.md` in each subdirectory.

The tension: integration-specialist's naming convention makes the `references/` directory self-documenting from a listing, but it creates a conversus-specific convention that agents unfamiliar with the project must learn. The agents.md standard's `AGENTS.md` naming is universally recognized — any agent entering a directory looks for it automatically. If both conventions coexist (reference files for runtime, AGENTS.md for contribution), the project has two parallel documentation trees with different naming philosophies. This is manageable but increases the maintenance surface.

### 4. Linter as Integration Test vs Linter as Contribution Gate

integration-specialist frames the linter as an integration test that should expand scope post-decomposition (Missed Opportunities, bullet 4; Recommendation 8): "the linter becomes a critical integration test — it verifies that extracted reference files remain consistent." My review frames the linter as a contribution gate that every agent should know about (Recommendation 4): "how to run the linter, how to run tests, what the linter checks, and how to interpret failures."

These are complementary but imply different expansion strategies. integration-specialist would have the linter validate cross-file consistency (reference files match schema, error messages match catalogue). I would have the linter remain focused on template/schema validation but ensure every contributing agent knows to run it. If both expansions happen, the linter's scope grows significantly — from a template validator to a full decomposition consistency checker. This scope creep risk should be acknowledged.

### 5. Token Savings: Modest vs Primary

integration-specialist explicitly reframes the decomposition benefit: "Token savings are a secondary benefit; the primary benefit is that agents working on guided workflow changes do not need to load run engine details" (Off-Base Assumptions, bullet 1). My review similarly downplays token savings: "Estimated token savings: 200-400 tokens from SKILL.md (modest)" (Recommendation 8). We agree that change isolation matters more than raw token reduction. The tension is in emphasis: integration-specialist's framing might lead the implementation to optimize for minimal cross-file loading (fewer, larger reference files), while my framing optimizes for contribution discoverability (more, smaller AGENTS.md files). Both are valid priorities that pull the decomposition structure in subtly different directions.

---

## Safe Agreements

### 1. SKILL.md and AGENTS.md Serve Fundamentally Different Purposes

integration-specialist's entire architecture assumes SKILL.md is the execution specification and reference files are the decomposition mechanism (all 10 recommendations operate within the SKILL.md/references ecosystem). My review's central thesis is: "AGENTS.md and SKILL.md serve fundamentally different purposes and should not be viewed as alternatives" (Executive Summary); "Do not move execution logic from SKILL.md to AGENTS.md" (Recommendation 6). Both reviews reject the idea that AGENTS.md could replace SKILL.md content. Both agree that the dispatch table, phase orchestration, and engine logic are runtime concerns that belong in the SKILL.md ecosystem. This shared boundary is load-bearing for the entire decomposition — if it were violated, the conversus runtime would break.

### 2. The Subcommand Dispatch Table is the Correct Anchor for Root SKILL.md

integration-specialist: "The subcommand dispatch table (lines 22-44) is the correct anchor for SKILL.md" (Alignment, bullet 1). My review does not propose moving the dispatch table and implicitly preserves it by scoping AGENTS.md content to contribution guidance only. Both reviews agree the dispatch table is the entry point contract that should remain front-and-center in the root file. This is a foundational architectural decision that constrains all other decomposition choices.

### 3. Existing External Seams (schema/variables.yml, linter, templates/) Are Proven and Should Guide Decomposition

integration-specialist: "Template variable contracts in `schema/variables.yml` are already a proven stable seam... the schema has been decoupled from SKILL.md since spec 009 without breaking the orchestrator" (Alignment, bullet 2). My review builds on the same evidence: the `schema/`, `linter/`, `templates/`, and `presets/` directories already operate as semi-independent units, which is precisely why nested AGENTS.md files in those directories would be natural (Recommendations 1-4). Both reviews treat these existing filesystem boundaries as the safest decomposition seams, and both would be alarmed by any proposal that merged these back into a monolith or introduced new boundaries that cut across them.

### 4. The Spec (011a) Underspecifies the Problem

integration-specialist: "The spec.md is only 11 lines and provides no concrete decomposition proposal" (Missed Opportunities, bullet 1). My review implicitly agrees — every recommendation I make is generated from analysis of the SKILL.md and external standards, not from the spec, because the spec provides only a problem statement with four links. Both reviews had to independently derive decomposition proposals rather than evaluate one. This is not a disagreement but a shared observation that shapes expectations for the deliberation: the output must be a concrete proposal, not a review of one.