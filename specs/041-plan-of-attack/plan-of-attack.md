# Plan of Attack: Layer-by-Layer Build Order

**Created**: 2026-04-02
**Origin**: Brett + Slater strategy session
**Status**: Post-deliberation — mitigations incorporated
**Deliberation**: `conversus/summary/final.md` (red-blue, 4 agents, 2 iterations)

---

## Strategic Context

The 040-command-center spec captures the *destination*. This document captures the *route* — the ordered sequence of work that gets us there layer by layer, with each layer independently shippable and monetizable.

**Core insight from the session**: Don't build top-down (dashboard first). Build bottom-up: split → engine standalone → schemas free tier → data layer → co-pilot → chat → dashboard. Each layer validates the one below it. Each layer gets a conversus run, documentation, and a blog post.

**Product model**: Cursor forked VS Code for code. We package conversus for business processes. Local Postgres bundled. Connect to remote or run local.

**Deliberation verdict**: Strategic architecture validated. Bottom-up build order, freemium funnel, and developer-first sequencing all survived adversarial review. Five mitigations required before/during execution.

---

## Required Mitigations (from deliberation)

These are non-negotiable changes to the plan based on the red-blue review. See `conversus/summary/final.md` for full risk register.

### MIT-1: Runtime Coupling Validation (P0 — blocks Phase 0)

**Risk**: Template resolution in SKILL.md uses filesystem path walking that assumes monolith directory structure. Static import analysis isn't enough — runtime dependencies will break standalone packages.

**Action**: Before executing Phase 0, instrument all cross-package calls, run the complete test suite in split configuration, and redesign template resolution to use package-relative paths. The `conversus-schemas` package must resolve templates independently.

**Gate**: Extracted schemas package runs all template/preset resolution tests in isolation.

### MIT-2: Financial Context & Revenue Gates (P0 — plan-level)

**Risk**: 18+ months of development before meaningful revenue. No burn rate analysis or survival strategy in the plan.

**Action**: Document the funding context explicitly (startup constraints vs. enterprise R&D). Add revenue validation gates:
- **Phase 2 gate**: Schema adoption metrics (Claude Code plugin installs, usage). If adoption < threshold, reassess free tier approach.
- **Phase 5 gate**: Conversion rate from free schemas → paid engine. If conversion < threshold, compress Phases 6-7 into minimal viable dashboard and accelerate revenue path.

**Pivot trigger**: If runway < 12 months at any gate, switch to accelerated dashboard delivery with PostgreSQL-only data layer.

### MIT-3: Customer Development Before Phase 3 (P1)

**Risk**: Dogfooding validates technical functionality but not business user demand. Building 18 months toward Command Center without external validation risks discovering target users prefer unstructured AI chat.

**Action**: Before committing to Phase 3, interview 10+ organizations about decision-making processes. Demo Phase 2 schemas. Validate willingness to pay for optimization vs. free deliberation. Distinguish technical validation (internal) from market validation (external).

**Gate**: Documented evidence that structured deliberation solves a real problem for people outside the team.

### MIT-4: Apache AGE over Memgraph (P1 — changes Phase 3)

**Risk**: Memgraph adds an entire infrastructure domain (graph DB ops, backups, monitoring) to a small team already stretched across 6+ technical domains.

**Action**: Start Phase 3 with Apache AGE (PostgreSQL extension) instead of Memgraph. Same openCypher queries, zero new infrastructure — everything stays in a single RDS Postgres instance. Evaluate Memgraph upgrade only after customer validation confirms graph approach delivers value.

**Escape hatch**: All openCypher queries are portable. Migration to Memgraph is a deployment change, not a rewrite.

### MIT-5: Prototype Standalone Schemas (P1 — validates Phase 2)

**Risk**: "Free schemas without engine" may be technically impossible if schema validation requires engine components. Circular dependency between standalone schemas and validation requirements could break the monetization model.

**Action**: Prototype the standalone schemas package early. Validate that templates, game forms, and construction pipeline schemas function without any engine dependency. Resolve any circular dependencies before building the monetization model on top.

**Gate**: Working prototype where `pip install conversus-schemas` provides advertised functionality and demonstrates a clear conversion pathway to paid engine.

---

## Phase 0: Split the Monolith (spec 032)

**Goal**: Package extraction with validated runtime coupling. Not purely mechanical — template resolution must be redesigned first (MIT-1).

**What**:
- **First**: Instrument and validate all runtime dependencies (not just imports). Run complete test suite in simulated split configuration. Identify and fix any filesystem path assumptions.
- **Then**: Redesign template resolution to use package-relative paths with explicit imports instead of parent directory traversal.
- Extract `conversus-schemas` from `conversus/schemas/`
- Extract `conversus-plugins` (framework only) from `conversus/plugins/base.py`, `config.py`
- Extract `conversus-domains` (framework only) from `conversus/domains/base.py`, `store.py`, `api.py`
- Extract paid packages: `conversus-nashopt`, `conversus-ampl`, `conversus-scenarios`
- Extract `conversus-swe` from `conversus/domains/implementations/code_review/`
- Core `conversus` keeps engine, CLI, MCP server, web, SKILL.md

**Validation**:
- `pip install conversus` works standalone with zero paid dependencies
- `pip install conversus-schemas` works standalone — all template/preset resolution works in isolation
- All existing tests pass against the split packages
- Run conversus on the split to verify consistency with specs 032/033
- **Rollback**: Monorepo remains the development home. If extraction reveals unforeseen coupling, revert immediately (spec 032 provides rollback path).

**Outputs**: Split packages, updated pyproject.toml files, CI for each package, redesigned template resolution

**Dogfooding**: Run a conversus deliberation on the package boundaries before executing.

**Blog post**: "Splitting a monolith with zero coupling rules already enforced"

---

## Phase 1: Engine Works Standalone

**Goal**: Prove the engine layer works with everything else disconnected.

**What**:
- `pip install conversus` — engine runs all 8 modes, all 6 phases, multi-round, stagnation detection
- No dependency on schemas package for basic operation (templates + presets are in the engine)
- Complete the in-flight bug fix specs: 034 (Kalman), 035 (plugin framework), 036 (mode templates), 037 (validation), 038 (solver equilibrium), 039 (new mode payoffs)
- Engine works as CLI, MCP server, and Python SDK independently

**Validation**:
- All 8 modes produce correct output
- Plugin framework loads and runs without paid plugins installed
- Guided workflow (7 subcommands) works end-to-end
- Run conversus against the engine to self-audit

**Outputs**: Stable engine release, all bug fix specs closed

**Dogfooding**: Use conversus to review its own engine fixes (self-audit pattern already exists)

**Blog post**: "AI is the 4th best developer — why the harness matters more than the model"

---

## Phase 2: Schema/Template Layer (Free Community Tier)

**Goal**: A free Claude Code plugin / VS Code plugin/ other popular run times via APM.  APM can bethat gives anyone access to conversus schemas and templates WITHOUT the engine. This is the "dumb version" — no optimization, no back pressure, just structured templates.

**Prerequisite**: MIT-5 prototype validates standalone schemas actually work.

**What**:
- `conversus-schemas` as a standalone Claude Code plugin
- Includes: game form schemas, objective function templates, construction pipeline schemas
- Users get pre-baked templates they can set for their org (SWE, medical, legal, etc.)
- Works as a Claude Code plugin with just Claude — no engine needed
- If they like it, they upgrade to the engine for optimization + back pressure

**Key distinction**: Without the engine, users are "just running prompts" — the schemas give structure but no deterministic optimization. The engine adds objective functions as back pressure. This is the upsell. This follows proven open-core patterns (GitLab, Supabase, PostHog) where free tier provides genuine value but has clear functional boundaries that drive paid upgrades.

**Revenue gate (MIT-2)**: Track Claude Code plugin installs and usage patterns. This is the first monetization signal — if nobody adopts the free tier, the paid conversion funnel won't work.

**Validation**:
- `pip install conversus-schemas` works standalone
- Claude Code plugin loads schemas and presents them to users
- Templates are usable without any engine configuration
- Run conversus on the schema designs: "Do these templates make sense standalone?"

**Outputs**: Standalone schemas package, Claude Code plugin, template catalog

**Dogfooding**: Create the schema/template layer using conversus itself.

**Blog post**: "The free tier: structured deliberation templates for any team"

---

## Customer Development Checkpoint (MIT-3 — between Phase 2 and Phase 3)

**Goal**: Validate external demand before committing to the data layer investment.

**What**:
- Interview 10+ organizations about their decision-making processes
- Demo Phase 2 schemas — do they see value in structured deliberation?
- Validate willingness to pay for optimization (engine) vs. free templates
- Test the hypothesis: "Business users want AI deliberation for business processes"
- Distinguish technical validation (we find it useful) from market validation (customers will pay)

**Gate**: Documented evidence of demand. If evidence is weak, reassess Phase 3 scope before proceeding. This is where the startup vs. enterprise context matters most — with patient capital, proceed cautiously. Under startup constraints, pivot if signal is absent.

**Output**: Customer development report informing Phase 3 scope and technology choices.

---

## Phase 3: Data Layer

**Goal**: Graph-assisted semantic search. Markdown becomes a queryable knowledge graph.

**What**:
- **Apache AGE** (PostgreSQL extension) for graph structure — same openCypher queries as Memgraph but zero new infrastructure (MIT-4). Everything stays in a single RDS Postgres instance.
- **pgvector** (same Postgres instance) for embeddings / vector search
- Markdown parser that extracts hierarchical nodes (file → heading 1 → heading 2 → section content)
- Backlink parser that creates edges between markdown sections (the foreign key relationships already being created manually)
- Graph-assisted semantic search: traverse the graph, find connected context, pull only what's needed for a task
- Docker compose for local dev (single Postgres container with AGE + pgvector extensions)

**Why Apache AGE over Memgraph**: Red team demonstrated Memgraph adds an entire infrastructure domain to a small team. Apache AGE gives us openCypher queries inside the Postgres instance we already need for pgvector. Zero new infrastructure, zero new backup procedures, zero new monitoring. All queries are portable — migrate to Memgraph later if graph performance demands it.

**Why this order**: The data layer is the foundation for everything above. Co-pilot needs it. Dashboard needs it. The context graph that connects specs, code, conversus outputs, and human feedback lives here.

**Validation**:
- Index this repo (conversus itself) as the first test case
- Query: "What specs does the command center depend on?" → graph traversal returns correct results
- Semantic search: "equilibrium scoring" → finds relevant sections across specs, code, and docs
- Benchmark: measure context tokens needed WITH graph search vs WITHOUT
- Run conversus on the data layer design before building
- **Operational check**: Database operations must consume <10% of engineering time. If >15%, trigger Memgraph reconsideration.

**Outputs**: `conversus-graph` package, AGE schema, markdown parser, search API

**Dogfooding**: Index all conversus specs and outputs into the graph. Use graph search when running conversus on conversus.

**Blog post**: "Graph-assisted semantic search: why your CLAUDE.md will never scale"

---

## Phase 4: Project Layer

**Goal**: Project-level state management. A project has an ID, configuration history, stored flows, and linked context.

**What**:
- Project configuration persistence (which schemas, which engine settings, which objective functions)
- Run history: "you set these parameters last run, so for consistency run against these parameters"
- Flow storage: saved deliberation configurations that can be re-run
- Project-level knowledge base: all markdown, specs, code, outputs indexed in the data layer
- Links between project artifacts and their deliberation history

**Why this matters**: The engine is stateless today — each run is independent. The project layer adds memory. "Here's what you did last time, here's what changed, here's what you should do now."

**Validation**:
- Create a project, run a deliberation, store the config
- Re-run with different parameters, compare to stored history
- Project graph shows all artifacts and their relationships
- Run conversus on the project layer: "Does this persistence model make sense?"

**Outputs**: Project management API, config history, flow storage

**Blog post**: "From stateless runs to project memory"

---

## Phase 5: Co-Pilot Layer / VS Code Plugin / Cursor Plugin

**Goal**: Developers use the engine in their IDE. This is the first "real user" interface beyond CLI.

**Revenue gate (MIT-2)**: Measure conversion rate from free schemas (Phase 2) → paid engine features through VS Code plugin. If conversion < sustainability threshold, compress Phases 6-7 into minimal viable dashboard.

**What**:
- Consider Agent Package Manager or some other best way to maintain versions and host all these different runtimes.
- Consider a CLI that wraps the API inside of an agent skill within the plugin for agents to interact with the API
- VS Code extension that connects to the engine
- Cursor plugin / extension that connects to the engine.
- Project context from the data layer feeds into deliberations
- Developer can: run a deliberation, see results inline, answer co-pilot questions
- MCP server integration (already exists) enhanced with project context
- The engine tells the developer: "Based on your last 3 runs, here's what's consistent. This new run deviates here."

**Why this order**: Developers are the first users. They're already using Claude Code and MCP. Give them conversus inside their existing workflow before building a separate dashboard. Developer-first is disciplined market expansion from proven users to unknown users.

**Validation**:
- VS Code extension loads, connects to engine
- Developer submits a natural language change request → construction pipeline classifies → gap questions appear in VS Code → deliberation runs
- Results appear in VS Code with project context
- Run conversus on the co-pilot design

**Outputs**: VS Code extension, enhanced MCP integration

**Blog post**: "Co-piloting business processes from your IDE"

---

## Phase 6: Interactive Layer (Chat Interface)

**Goal**: Simple chat interface for non-developers. Open source chat UI, customized.

**Customer validation gate**: Phase 6 completion requires pilot customer validation of business user adoption and usage patterns before committing to full Command Center investment.

**What**:
- Chat-based interface (use an existing open source chat UI)
- Can set schema values, submit change requests, answer co-pilot questions
- Connects to the engine via REST API
- Project context from the data layer enriches conversations
- Not a full dashboard — just conversation

**Validation**:
- Non-technical user can submit a change request via chat
- Gap questions render as interactive cards
- Deliberation results appear as chat messages
- Run conversus on the chat interface design

**Outputs**: Chat UI, WebGapFiller implementation

**Blog post**: "From CLI to chat: making AI deliberation accessible"

---

## Phase 7: Dashboard / Command Center (spec 040)

**Goal**: Full dashboard with KPIs, artifact browser, team activity, voice. This is the product surface.

**What**:
- Everything in spec 040
- KPIs on objective functions ("are we hitting the numbers we care about?")
- Artifact browser (browse specs, decisions, features, goals)
- Team activity feed
- Voice interaction
- Mobile PWA

**Why last**: The dashboard consumes everything below. Without the data layer, project layer, and co-pilot, the dashboard has nothing to show.

**Validation**:
- All success criteria from spec 040
- Non-technical user can browse, submit, answer, and view end-to-end

**Outputs**: Full Command Center application

**Blog post**: "The Command Center: co-piloting your entire organization"

---

## Cross-Cutting Concerns (Every Phase)

### Documentation as Terraforming
Every phase produces documentation that becomes nodes in the data layer. Docs aren't an afterthought — they're the substrate of the context graph. Documentation overhead transforms into Command Center functionality — graph search, impact analysis, and co-pilot context all consume docs as product input.

### Conversus on Conversus
Every phase runs through conversus before and after implementation:
- **Before**: "Given existing specs, does this new layer make sense?"
- **After**: "Given what was built, update all outstanding specs"

**Limitation noted by deliberation**: Internal dogfooding validates technical functionality but not business user demand. This is why MIT-3 (customer development) exists as a separate validation stream.

### Blog Posts as Proof
Every phase produces at least one blog post. Blog posts are generated through the blog plugin (already exists). Each blog post is both marketing and dogfooding proof.

### Plugins/Domains/Schemas
Every phase should exercise the plugin/domain/schema system. If we need something new, build it as a plugin. The blog engine was an example — we didn't just write blog posts, we built a blog post plugin that uses conversus.

### Game Theory Exercise
Every phase should exercise game theory modes and objective functions with increasing complexity. This is how we build the benchmark data.

### Context Graph Growth
Every phase adds to the context graph. Specs backlink to code. Code backlinks to specs. Conversus outputs backlink to both. Human feedback backlinks to outputs. The graph grows organically.

---

## Risk Register Summary

From the red-blue deliberation (`conversus/summary/final.md`):

| Risk | Severity | Mitigation | Status |
|------|----------|------------|--------|
| Runtime coupling in template resolution | Critical | MIT-1: Validate + redesign before Phase 0 | Incorporated into Phase 0 |
| 18-month revenue desert | Critical | MIT-2: Revenue gates at Phase 2, 5 | Incorporated as gates |
| Business process demand unvalidated | Critical | MIT-3: Customer dev before Phase 3 | Added as checkpoint |
| Memgraph operational complexity | High | MIT-4: Apache AGE instead | Changed in Phase 3 |
| Standalone schemas may not work | Critical | MIT-5: Prototype early | Prerequisite for Phase 2 |
| Team capacity overstretch | High | AGE reduces domains; monitor eng time | Ongoing |
| Dogfooding circular validation | Medium | Separate internal vs external validation | Noted in cross-cutting |
| Startup vs enterprise context | Disputed | MIT-2 pivot triggers address either case | Revenue gates adapt |

### Mitigated (defended successfully)
- Bottom-up build order: validated, builds on proven systems not speculation
- Construction pipeline integration: existing APIs work for web UI
- Free tier cannibalization: intentional incomplete experience drives conversion
- Package extraction approach: import boundaries enforced 18+ months, rollback available

### Disputed (needs code inspection)
- Template resolution mechanism: Red claims filesystem walking, Blue claims package resource resolution. MIT-1 resolves this empirically before proceeding.

---

## Constitution Updates

Add to constitution.md (as a reference, not inline):
- This plan of attack as the strategic direction document
- Decision: build bottom-up, not top-down
- Decision: schema layer is free, engine is paid
- Decision: every layer goes through conversus
- Decision: documentation is terraforming, not afterthought
- Decision: direction decisions need to be in a knowledge base, not just a doc

---

## Spec Updates Needed

| Spec | Action | Notes |
|------|--------|-------|
| 032-package-splitting | Update | Add MIT-1 runtime coupling validation + template resolution redesign |
| 034-039 (bug fixes) | Execute | Must complete before engine standalone |
| NEW: schemas-as-plugin | Create | Free community Claude Code plugin (prototype first per MIT-5) |
| NEW: data-layer | Create | Apache AGE + pgvector (single Postgres) + markdown parser |
| NEW: project-layer | Create | Project state, config history, flow storage |
| NEW: copilot-vscode | Create | VS Code extension + enhanced MCP |
| NEW: chat-interface | Create | Simple chat UI for non-developers |
| 040-command-center | Update | Rewrite based on this build order, move to Phase 7 |

---

## Resolved Questions (from deliberation)

1. **Is Phase 0 truly mechanical?** No — template resolution has runtime coupling that static import analysis misses. MIT-1 addresses this.
2. **Memgraph vs Apache AGE?** Start with Apache AGE (MIT-4). Same openCypher, zero new infra. Migrate to Memgraph only if graph perf demands it.
3. **Is the free tier viable?** Architecturally yes (proven open-core pattern). Needs prototype validation (MIT-5) and market validation (MIT-3).

## Remaining Open Questions

1. Should the schema layer plugin support non-Claude Code agents (e.g., Copilot, Windsurf)?
2. Project layer: file-based or database-backed for the MVP?
3. VS Code extension: build custom or extend the existing MCP server?
4. Chat interface: which open source chat UI is the best starting point?
5. How do we benchmark graph-assisted search vs alternatives on a controlled codebase?
6. What is the explicit funding context — startup constraints or patient capital? (MIT-2 requires this answer)
