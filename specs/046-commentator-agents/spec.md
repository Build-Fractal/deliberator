# Feature Specification: Commentator Agents — Verbose Narrative Mode

**Feature ID**: `046-commentator-agents`
**Created**: 2026-04-04
**Status**: Draft
**Depends On**: Core conversus engine (run orchestration, artifact storage, scenario storage spec 020)
**Docs Update**: New docs/user-guide/verbose-mode.md; update docs/user-guide/cli.md with `--verbose` flag; update docs/api/commentator-agents.md
**Origin**: User observation — "sometimes the most important thing for users is to feel like they understand what is happening." The synthesis document answers "what was decided" but not "what happened along the way." Users need a narrative view to internalize the deliberation dynamics.

---

## 1. Problem

Conversus produces rich artifacts during a deliberation: reviews, cross-reviews, revisions, disputes, synthesis, arbitration. The **synthesis document** tells users what was decided. It does NOT tell users:

- **The story of how agents moved** through the deliberation — who conceded, when, why
- **The dramatic beats** — where an agent produced decisive evidence, where a claim got retracted
- **The cross-round arc** — what changed between rounds, what stayed constant
- **The continuity across deliberations** — when a pattern repeats across multiple runs, who tends to dig in vs concede, which kinds of arguments win
- **The contextualization** — why this deliberation matters relative to prior ones, what it connects to

The synthesis is the **box score**. Users want the **game recap**.

The information is all there — in the reviews, cross-reviews, revisions, and disputes documents. But extracting the narrative requires reading 15-30+ files and holding the whole deliberation in your head. Most users won't do that.

## 2. Solution: Two Commentator Agents

Add an optional `verbose: true` flag (or equivalent mechanism) to `conversus.yml` that, after the synthesis phase completes, runs two additional agents:

### Agent 1: `play-by-play`
**Role**: Chronological, factual narrator of what happened.

**What they produce**:
- A time-ordered account of the deliberation
- Named agents, specific claims, concrete citations to artifacts
- Phase-by-phase transitions ("In Phase 2, sdet-agent cross-reviewed fp-guru...")
- Concessions with exact quotes
- Dispute emergence and resolution

**Style**: Sports play-by-play — direct, named, specific. "Smith passes to Jones. Jones shoots. He scores."

**Example output tone**:
> "Round 1 opened with FP-guru asserting that `engine/errors.py:79-83` was dead code. Fifteen minutes later, SDET filed their review. Without having seen FP-guru's position, SDET already had a response ready: they cited `engine/providers/anthropic.py:89, 124` showing that `ProviderError(category='unknown')` is raised on every generic API error. In the revision phase, FP-guru read SDET's cross-review and typed three words that are rare in conversus outputs: 'I was wrong.'"

### Agent 2: `color-commentator`
**Role**: Interpretive analyst explaining significance, context, and meaning.

**What they produce**:
- Why particular moves mattered
- Patterns across the deliberation (who tends to lead vs who tends to validate)
- Cross-run connections (when the pattern repeats from a prior deliberation)
- Drama and significance
- Predictions and implications
- What this deliberation reveals about the system being deliberated

**Style**: Sports color commentary — contextual, interpretive, narrative. "That pass Smith just made — he couldn't have done that three years ago. Watch his footwork — it's exactly the move his college coach drilled into him. This is the kind of decision that wins championships."

**Example output tone**:
> "This is the third deliberation this month where FP-guru has led with type theory and been pulled back by empirical evidence. It's not a weakness — it's a productive dynamic. FP-guru's type-first lens surfaces issues that SDET wouldn't have caught, then SDET's evidence-first lens prevents FP-guru's abstractions from overreaching. The `errors.py:79-83` moment wasn't a failure; it was the system working. If you removed either agent, the deliberation gets worse. The real insight here isn't about `errors.py` — it's that `ProviderError.category='unknown'` is load-bearing API surface that was typed as a bare `str`. That's the kind of latent risk that only surfaces when two different lenses collide."

---

## 3. Architecture

### 3.1 Execution model

Commentator agents run **after** the synthesis phase (and after arbitration, if the arbiter fires). They read the complete deliberation output as their input:

```
Phase 1: Reviews
Phase 2: Cross-Reviews
Phase 3: Revisions
Phase 4: Disputes
Phase 5: Synthesis
Phase 6: Arbitration (conditional)
──────────────────────────────────
Phase 7: Play-by-Play (conditional — verbose mode)
Phase 8: Color Commentary (conditional — verbose mode)
```

Phase 7 and Phase 8 run in parallel (they have no dependency on each other). Both read the same inputs:
- All `review.md` files
- All `cross-reviews/*.md` files
- All `revision.md` files (including iteration variants)
- All `disputes.md` files
- `summary/final.md` (and `round-{N}/summary/final.md` for multi-round)
- `arbitration/resolution.md` (if arbiter ran)
- `conversus.yml` (for deliberation config context)
- Target files (for grounding context)

### 3.2 Output structure

```
{output}/
├── ... (existing artifacts)
└── commentary/
    ├── play-by-play.md
    └── color-commentary.md
```

Both files live at the top level of the output directory (not inside `summary/` or `round-{N}/`), because they span the entire run.

### 3.3 Cross-run context (meta-commentary)

Commentators can optionally accept a `prior_runs` list — paths to other conversus output directories. When provided, they:

1. Read each prior run's artifacts (lazily — only summaries and commentary, not full transcripts)
2. Identify recurring patterns, participants, or themes
3. Reference them in the commentary by their timestamps or run IDs

```yaml
verbose:
  enabled: true
  prior_runs:
    - specs/031-docs-review/conversus-output/
    - specs/045-test-coverage-review/conversus-output/
    - specs/wave1-3-blog/conversus-output/
```

When `prior_runs` is absent, commentators only have the current run. When present, they produce **meta-commentary** that situates the current run in a broader context.

### 3.4 Composed runs

When a conversus run is composed (e.g., multiple rounds, or a run that uses another run's output as prior context), commentators handle the composition naturally — they read the full composed artifact tree and narrate across it.

This handles three cases:
- **Single run, single round**: Narrate the phases.
- **Single run, multi-round**: Narrate the rounds as an arc, highlighting what changed between them.
- **Multi-run composition**: Narrate as a sequence connected by `prior_runs`, identifying themes and drift.

---

## 4. Verbose Mode Activation

Three ways to enable commentator agents:

### 4.1 Config-level flag
```yaml
mode: cooperative
target: ...
agents: [...]

verbose: true  # enables both commentators

# OR granular control:
verbose:
  play_by_play: true
  color_commentary: true
  prior_runs:
    - path/to/other/output/
```

### 4.2 CLI flag
```bash
conversus run config.yml --verbose
conversus run config.yml --verbose --prior-runs specs/031/conversus-output/
```

### 4.3 Post-hoc invocation
Commentator agents can run AFTER a deliberation completes, on existing output:
```bash
conversus commentate specs/045-test-coverage-review/conversus-output/
conversus commentate specs/045-test-coverage-review/conversus-output/ --prior-runs specs/031/...
```

This is the most useful mode for users who want to generate commentary on runs that have already finished — including runs from days or weeks ago.

---

## 5. Output Format

### 5.1 Play-by-play structure

```markdown
---
type: conversus-commentary
kind: play-by-play
run_id: {hash}
mode: {mode}
rounds: {n}
agents: [list]
duration_minutes: {n}
generated_at: {iso8601}
---

# Play-by-Play: {Deliberation Title}

## The Setup
{Brief description of what was being deliberated, who the agents were, what mode ran}

## Round 1

### Phase 1: Initial Reviews
{Chronological account of each agent's opening position, with specific claims and evidence}

### Phase 2: Cross-Reviews
{Who reviewed whom, what they found, how positions diverged or converged}

### Phase 3: Revisions
{What changed, who conceded, who dug in}

### Phase 4: Disputes
{Remaining disagreements, articulated clearly}

### Phase 5: Synthesis
{What the synthesizer concluded, cited}

## Round 2 (if applicable)
{Same structure, with explicit references to what carried forward from Round 1}

## Arbitration (if applicable)
{The arbiter's rulings with rationale}

## Final Scorecard
- Findings: {n}
- Convergences: {n}
- Concessions: {list with citations}
- New insights discovered: {n}
- Arbiter interventions: {n}

## Referenced Artifacts
- [file path] — [why it mattered]
- ...
```

### 5.2 Color commentary structure

```markdown
---
type: conversus-commentary
kind: color-commentary
run_id: {hash}
mode: {mode}
themes: [list]
patterns_identified: [list]
prior_runs_referenced: [list]
generated_at: {iso8601}
---

# Color Commentary: {Deliberation Title}

## Why This Deliberation Mattered
{Context: what was at stake, what the system being deliberated needed}

## The Dynamic
{How the agents pushed and pulled — their characteristic moves, where they differed}

## Key Moments
### The {name-of-moment}
{A specific beat in the deliberation that carried disproportionate weight, with interpretation of why it mattered}

## Cross-Run Patterns (if prior_runs provided)
{Connections to prior deliberations — who's done this before, what's new, what's repeating}

## What Was Surprising
{Findings that neither agent had going in — the emergent insights}

## What Wasn't Surprising
{Confirmations of existing suspicions — what this deliberation reinforced}

## Implications
{What this deliberation means for future work, for the system's design, for the team}

## Prediction
{One or two concrete predictions about what will happen next, based on the dynamics observed}
```

### 5.3 Machine-readable metadata (graph/vector DB ingestion)

Both files include YAML frontmatter with structured metadata. Additionally, a separate `commentary/graph.jsonl` file is produced:

```jsonl
{"type": "entity", "kind": "agent", "id": "fp-guru", "name": "functional-programming-guru", "run_id": "..."}
{"type": "entity", "kind": "agent", "id": "sdet", "name": "sdet-agent", "run_id": "..."}
{"type": "relation", "source": "fp-guru", "target": "sdet", "kind": "conceded_to", "phase": "revision", "topic": "errors.py:79-83", "artifact": "functional-programming-guru/revision.md#section-1-3"}
{"type": "event", "kind": "concession", "agent": "fp-guru", "quote": "I was wrong", "phase": "revision", "run_id": "..."}
{"type": "pattern", "description": "Type-theory-first lens pulled back by empirical evidence", "occurrences": ["run-045", "run-042"], "significance": "productive dynamic"}
```

This structured output is directly ingestable by graph databases (Neo4j, ArangoDB), vector databases (pgvector, Qdrant, Weaviate), or custom indexing systems.

---

## 6. Functional Requirements

### Activation
- **FR-001**: Commentator agents MUST be opt-in. Default behavior (no `verbose` flag) preserves current conversus output exactly.
- **FR-002**: Three activation paths MUST be supported: config flag, CLI flag, post-hoc `conversus commentate` subcommand.
- **FR-003**: When `verbose: true` (boolean), both commentators run. When `verbose: {play_by_play: true, color_commentary: false}` (dict), granular control applies.

### Execution
- **FR-004**: Commentators run AFTER synthesis and arbitration complete. They never run during the main deliberation phases.
- **FR-005**: The two commentators run in parallel (no inter-dependency).
- **FR-006**: If a commentator fails, the main deliberation output is NOT invalidated. Commentary is additive.
- **FR-007**: Commentators MUST read all deliberation artifacts as input, not just the synthesis.
- **FR-008**: Commentators MUST accept an optional `prior_runs` list for cross-run context.

### Output
- **FR-009**: Play-by-play output MUST be chronological and factual with direct quotes.
- **FR-010**: Color commentary output MUST interpret significance, not restate facts.
- **FR-011**: Both outputs MUST include YAML frontmatter with machine-readable metadata.
- **FR-012**: A structured `commentary/graph.jsonl` file MUST be produced for graph/vector DB ingestion.
- **FR-013**: Output files MUST live at `{output}/commentary/` (top-level, not per-round).

### Cross-run continuity
- **FR-014**: When `prior_runs` is provided, commentators MUST read each prior run's commentary files (not full transcripts) and reference them.
- **FR-015**: Commentators MUST identify recurring patterns across runs when prior context is provided.
- **FR-016**: Cross-run references MUST be citable (run_id, artifact path, section).

### Post-hoc mode
- **FR-017**: `conversus commentate <output_dir>` MUST work on any completed conversus output directory, regardless of age.
- **FR-018**: Post-hoc mode MUST accept `--prior-runs` to add cross-run context retroactively.
- **FR-019**: Post-hoc mode MUST NOT modify any existing deliberation artifacts.

---

## 7. Success Criteria

- **SC-001**: Running `conversus run config.yml --verbose` produces `commentary/play-by-play.md` and `commentary/color-commentary.md` in addition to existing outputs.
- **SC-002**: The play-by-play file reads as a chronological narrative with at least 5 direct quotes from the deliberation and explicit phase transitions.
- **SC-003**: The color commentary file identifies at least 2 dynamics or patterns not explicitly stated in the synthesis.
- **SC-004**: Running `conversus commentate specs/045-.../conversus-output/` on an existing deliberation produces commentary without modifying any existing files.
- **SC-005**: With `prior_runs` provided, the color commentary references at least one pattern that spans runs.
- **SC-006**: The `commentary/graph.jsonl` file contains valid JSONL with at least 10 structured entities/relations/events per run.
- **SC-007**: A graph database can ingest `graph.jsonl` files from multiple runs and produce cross-run queries (e.g., "how many times has fp-guru conceded?").
- **SC-008**: Commentator failure (e.g., template not found, content generation error) produces a warning but does NOT invalidate the main deliberation output.

---

## 8. Templates

New template files in `conversus/templates/commentary/`:

- `play-by-play.md` — prompt template for the play-by-play agent
- `color-commentary.md` — prompt template for the color commentary agent
- `graph-extraction.md` — prompt template for extracting structured entities/relations to JSONL

The templates use the standard `{VARIABLE}` substitution pattern. Key variables:
- `{ALL_REVIEWS}` — paths to all review.md files
- `{ALL_CROSS_REVIEWS}` — paths to all cross-review files
- `{ALL_REVISIONS}` — paths to all revision files
- `{ALL_DISPUTES}` — paths to all disputes files
- `{SYNTHESIS_PATH}` — path to summary/final.md
- `{ARBITRATION_PATH}` — path to arbitration/resolution.md (or empty)
- `{PRIOR_RUNS_SECTION}` — expanded context block if prior_runs provided, empty otherwise
- `{RUN_METADATA}` — config summary (mode, agents, rounds, target)
- `{TARGET_FILES}` — the files the deliberation was about

---

## 9. Use Cases

### 9.1 Solo developer running a spec review
**Setup**: Single conversus run on a new spec.
**Commentary value**: User reads the play-by-play to understand how reviewers arrived at the synthesis. Saves 30 minutes of reading individual review files.

### 9.2 Team sharing deliberation outputs
**Setup**: Team member runs a conversus review, shares the output directory.
**Commentary value**: Colleagues get the full story without having to dig through 16+ artifact files. The color commentary explains why certain moves mattered.

### 9.3 Building institutional knowledge
**Setup**: Many deliberations accumulated over months.
**Commentary value**: Post-hoc `conversus commentate` runs on every output directory, producing a corpus of narratives. The `graph.jsonl` files feed a knowledge graph showing patterns across deliberations (who tends to agree, which topics recur, which agents are most effective in which modes).

### 9.4 Cross-run pattern discovery
**Setup**: Multiple related deliberations (e.g., spec 031 docs review + spec 045 test review).
**Commentary value**: With `prior_runs` set, the color commentary identifies that FP-guru's "type-first pulled back by empirical" pattern appears in both — a real recurring dynamic that neither individual run would surface on its own.

### 9.5 Content marketing
**Setup**: A deliberation produces a particularly interesting story (like spec 045's `errors.py:79-83` moment).
**Commentary value**: The color commentary can be directly repurposed as a blog post. The play-by-play provides the timeline; the color commentary provides the narrative hook.

### 9.6 LLM context for future runs
**Setup**: A new conversus run on a topic that has related prior deliberations.
**Commentary value**: The commentary files are dense, structured narratives ideal for loading into an agent's context. Instead of dumping 30 raw artifacts, load the two commentary files (~10KB) and get the full history.

---

## 10. Constraints

- Commentary is **additive**, never modifies existing artifacts.
- Commentator failures are non-blocking — the main deliberation output stays valid.
- Commentators run sequentially AFTER all main phases complete — they cannot influence the deliberation itself.
- The JSONL graph format is stable — schema changes require a major version bump.
- Commentators use the same model as the main deliberation (no per-agent model selection) unless explicitly configured.
- Commentary files do NOT count toward dispute parsing or stagnation detection — they're out-of-band artifacts.
- Post-hoc commentary does NOT re-run any prior phases; it only reads the existing artifacts.

---

## 11. Open Questions

1. **Should color commentary be allowed to disagree with the synthesis?** If the synthesizer concluded "converged" but the color commentator sees lingering tension, should they say so?
   - **Lean**: Yes, with caveats. Color commentary is interpretive; it's allowed to surface sub-text. But it should never contradict factual claims in the play-by-play.

2. **Should commentators have access to the target files themselves, or only the deliberation artifacts?**
   - **Lean**: Both. Without target files, the commentary is abstract; with them, it can cite specifics from the code/spec under review.

3. **How should prior_runs be limited?** Reading 50 prior runs of commentary could blow up context.
   - **Lean**: Max 10 prior runs. If users provide more, the agent loads the 10 most recent by timestamp. Future: vector search to load the most semantically relevant.

4. **Should the two commentators see each other's output?**
   - **Lean**: Probably not in v1. Keep them independent. In v2, consider letting color commentary read the play-by-play as input (since color is interpretive of facts the PbP established).

5. **What about multi-language output?** Some teams want narratives in their native language.
   - **Lean**: v1 is English-only. Template-based, so localization is additive later.

6. **Should graph.jsonl use a standard schema (schema.org, OpenLineage)?**
   - **Lean**: Define a conversus-specific schema in v1. Migrate to standards if/when a standard fits. Premature standardization is a trap.

7. **Can commentator agents be customized (user-provided templates)?**
   - **Lean**: v1 ships standard templates. v2 allows custom templates via `verbose.play_by_play_template: path/to/template.md` override.

---

## 12. Relationship to Other Specs

- **Spec 020 (scenario storage)**: Commentary is a form of scenario metadata. The graph.jsonl files could feed the scenario storage system directly.
- **Spec 031 (docs system)**: Commentary output fits naturally in a docs/blog pipeline — color commentary is blog-post material.
- **Spec 033 (free/paid tiers)**: Verbose mode could be a paid feature (premium narrative) while the free tier produces the synthesis only. OR: verbose mode is free, but cross-run pattern detection (prior_runs) is paid.
- **Spec 042 (execution providers, Accepted 2026-04-05)**: Commentators are regular agents — they run through whatever `ExecutionProvider` is configured for the main deliberation, per the 4-provider v1 set (`mock`, `anthropic`, `claude-code`, `opencode`) plus optional `LiteLLMProvider`. Commentators can be dispatched as post-synthesis "second pass" invocations without a special code path, per spec 042 validation battery §1.4. Spec 049 surfaces commentary inside the VSCode extension's Arbitration sub-view.
- **Spec 044 (AMPL model templates)**: The graph.jsonl pattern is identical to how ampl-templates metadata files work — same indexing philosophy applied to a different problem.

---

## 13. Phasing

### Phase 1: Core commentators (~1 week)
- Play-by-play and color commentary templates
- `verbose: true` flag in conversus.yml
- Post-hoc `conversus commentate` subcommand
- Tests covering both agents against spec 045's existing output

### Phase 2: Cross-run continuity (~1 week)
- `prior_runs` config field
- Cross-run pattern detection in color commentary
- Commentary file reading (summaries only, not full transcripts)

### Phase 3: Structured output for graph/vector DBs (~1 week)
- `commentary/graph.jsonl` generation
- Schema documentation
- Integration example with a graph DB (e.g., a sample Neo4j loader script)

### Phase 4: Post-hoc tooling (~3 days)
- Batch commentary generation on existing output directories
- CLI for listing runs, generating commentary, querying the graph

### Phase 5: Documentation + examples (~2 days)
- User guide for verbose mode
- Blog post showing spec 045's commentary as an example
- Graph DB integration tutorial
