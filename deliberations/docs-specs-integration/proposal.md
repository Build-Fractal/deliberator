# Surfacing Specs and Deliberations in the Docs

## Context

The conversus-oss repo has two underused sources of documentation value:

1. **`specs/`** — 23 active feature specifications covering the game engine, execution providers, AMPL solvers, commentator agents, governance mode, and more. Plus `specs/distribution-strategy.md` (the spec that drove the PyPI/MCP/plugin architecture). Plus `specs/done/` with historical specs.

2. **`deliberations/`** — 2 multi-agent conversus deliberations:
   - `deliberations/packaging-strategy/` — 29 LLM launches, 4 agents, mechanism-design mode, produced the three-layer distribution architecture
   - `deliberations/docs-review/` — 17 LLM launches, 3 agents + arbiter, cooperative mode, evaluated the OSS docs

The docs site currently has no links to either. Readers can't:
- See *why* decisions were made (the specs)
- See *how* decisions were made (the deliberations)
- Learn from the conversus methodology by seeing real examples of it

## The Question

How should specs and deliberation outputs be surfaced in the MkDocs site so readers can find them, understand them, and learn from them — without bloating the navigation or overwhelming new users?

## Options Under Consideration

### Option A: Dedicated "Reference" section
Add a new top-level nav section with sub-pages:
- `reference/specs/` — index + per-spec pages (or rendered directly from `specs/`)
- `reference/deliberations/` — one page per deliberation with executive summary + links to raw output
- Pro: Clear location, discoverable, supports both audiences (readers + contributors)
- Con: New top-level section is heavy, specs are numerous (23+)

### Option B: ADR (Architecture Decision Records) pattern
Treat deliberation outputs as ADRs under `developer-guide/decisions/`:
- Each ADR is a short page with context, decision, consequences, links to deliberation
- Specs remain a separate reference, or linked from ADRs
- Pro: Industry-standard pattern, compact, decision-focused
- Con: Requires writing ADR summaries, doesn't fully expose specs

### Option C: Minimal inline linking
No new sections. Add cross-references from existing docs pages:
- `architecture.md` links to relevant specs
- `contributing.md` links to spec repo
- A single "Decisions" page links to deliberations
- Pro: Zero navigation bloat, uses existing structure
- Con: Not discoverable unless you know where to look

### Option D: Transparent methodology showcase
Make the conversus deliberation process itself a first-class documentation topic:
- `user-guide/using-conversus-on-itself.md` — meta-example showing real deliberations
- Links to the full deliberation outputs as case studies
- Specs link from the relevant `developer-guide/` pages
- Pro: Educational, shows conversus in action, differentiates the project
- Con: Mixes meta-content with user-facing docs

### Option E: Hybrid
Combine elements:
- Specs: curated "Decision Records" page listing the most important specs with one-line summaries and links
- Deliberations: included under `developer-guide/case-studies/` as executive summaries
- Methodology: a single `user-guide/` page showing "conversus deliberating on itself"

### Option F: Link-out to GitHub
Don't duplicate anything in the MkDocs site. Instead:
- GitHub already renders `specs/` as a browsable file tree
- GitHub already renders `deliberations/` with full markdown viewing
- Add a single "Specs & Deliberations" page in docs with curated outbound links:
  - https://github.com/Build-Fractal/conversus-oss/tree/main/specs (all specs)
  - https://github.com/Build-Fractal/conversus-oss/blob/main/specs/distribution-strategy.md (featured spec)
  - https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations/packaging-strategy (packaging deliberation)
  - https://github.com/Build-Fractal/conversus-oss/tree/main/deliberations/docs-review (docs review deliberation)
- Pro: Zero duplication, zero maintenance, GitHub handles rendering + search + history
- Pro: Users arriving at specs see the full repo context (file tree, commits, blame)
- Con: Leaves the docs site for external content (but MkDocs already links out for many things)
- Con: Deep-linking into specific spec sections is harder (no search integration)

## Constraints

- Specs are written for internal engineering audience — may need summaries for public docs
- Deliberation outputs are verbose (29+ files per run) — linking to raw output is fine but not ideal
- MkDocs nav structure: users expect User Guide → Developer Guide → API Reference, anything else is a departure
- Small team — can't write 23 spec summaries by hand
- The spec for this work is itself `specs/distribution-strategy.md` — a meta-case

## What We Need

A concrete plan with:
1. Nav structure changes (exact yaml additions to `mkdocs.yml`)
2. New pages to create (paths + purpose)
3. Spec coverage strategy (all 23? curated subset? auto-generated index?)
4. Deliberation coverage strategy (summary + link? inline the final.md? case-study format?)
5. Cross-linking rules (when do existing pages link to specs/deliberations?)
6. Migration path for future specs/deliberations (how does new content land in docs?)
