# Developer Advocate Review -- Round 2

## Executive Summary

Round 1 produced 7 convergence points and 7 remaining disputes. This review re-evaluates the documentation suite from the developer-advocate perspective after that synthesis, honoring all prior concessions. The documentation has real strengths -- the plugin ABC walkthrough and the produces/consumes pattern are explained well enough to build from. But three critical developer tasks remain impossible from documentation alone: (1) shipping a domain plugin end-to-end (only 2 of 5 lifecycle stages are demonstrated), (2) wiring a custom plugin into a running system (dynamic loading steps are described from the engine's perspective, not the developer's), and (3) understanding how domains relate to the deliberation pipeline (architecture.md shows the pipeline but domains appear to float outside it). Round 1 converged on most of these gaps; this review refines priorities and addresses the unresolved disputes.

## Alignment

### Convergence I affirm from Round 1

**1. `plugins:` key in config-reference.md (Convergence #3).** This was my original DA-3. The unanimous convergence on placing it in an "Advanced / Extensibility" subsection is the right call. Without this key documented, a developer reading only config-reference.md cannot discover that plugins are configurable via YAML at all. The `building-plugins.md` guide shows the YAML snippet (L142-152) but config-reference.md -- the canonical schema reference -- omits it entirely.

**2. `determine_verdict` split (Convergence #5).** The current example at building-domains.md L126-132 teaches a `minimum_overall` threshold check as if it were the default behavior. The base class default actually checks hard blocks first, then per-dimension thresholds. Splitting into "Default behavior" and "Customizing verdict logic" prevents developers from overriding `determine_verdict` when they only need to adjust thresholds in their scaffold YAML. This is a documentation efficiency issue, not just accuracy.

**3. Scaffolds endpoint YAML fix (Convergence #2).** I accept this as code-fix-only. My Round 1 review praised the scaffold YAML documentation without catching that the API endpoint at `api.py` L208 silently drops YAML files. The documentation is YAML-first throughout; the code is the outlier.

**4. `decide` 4-mode restriction note (Convergence #1).** The CLI constrains `--mode` to 4 choices via `click.Choice`. The modes page documents 8 modes. A one-line cross-reference note in cli.md is the minimum viable fix.

**5. Provider precedence note (Convergence #6).** I accept code-verifier's more precise wording from the dispute resolution: "The `run` command always uses the `--provider` flag value. When omitted, it defaults to `mock` regardless of the config file's `provider` field." This is more accurate than "overrides" and I concede the distinction matters.

**6. API reference narrative prose (Convergence #4).** The layered approach -- one accessible sentence, key class listing, cross-link to developer guide -- is the right structure. I accept this over my original proposal to replace mkdocstrings directives entirely.

**7. `estimate_cost_usd()` documentation (Convergence #7).** A developer building a cost-aware pipeline needs this function documented. No dispute.

### Positions I maintain from Round 1

**End-to-end domain tutorial (DA-1).** The building-domains guide opens with "5-stage lifecycle: extract, score, persist, gate, serve" but the example only covers extract and score. A developer reading this guide cannot:
- Construct a `DomainContext` object (workspace, changed_files, metadata are listed but no construction example)
- Call `score()` with the correct arguments (the scaffold name parameter is not shown in any example)
- Create a `DomainRecord` from a score (the `create_record()` method is not demonstrated)
- Persist a record to a store (JSONLStore is described but not wired to a domain instance)
- Mount and test the API router (the router factory example exists but is disconnected from the domain example)

Each of these is individually documented in fragments; none is demonstrated as a connected flow. This is the single largest gap for the developer audience.

**Plugin wiring documentation (DA-2).** The "Dynamic loading" section (building-plugins.md L163-170) describes the engine's `importlib` behavior. A developer needs to know: (a) their module must be importable from the Python path, (b) `package` in the YAML is a dotted Python import path, (c) `pip install -e .` makes local packages importable, (d) failure is non-fatal (warning + skip). These are *developer* steps, not engine internals. Round 1 converged on adding `plugins:` to config-reference.md, which addresses schema discoverability, but not on updating building-plugins.md, which addresses developer workflow. Both are needed.

## Missed Opportunities

### 1. No domain-to-pipeline bridge in architecture.md

Architecture.md documents the 5-phase deliberation pipeline in detail (L46-91) but domains are not mentioned in the data flow diagram at all. The `conversus/domains/` package appears in the package boundaries table (L41) but there is no arrow showing how domain scoring consumes deliberation output. A developer looking at the architecture cannot answer: "When does my domain plugin run relative to the deliberation pipeline?"

The building-domains guide says domains "turn review into a quantifiable optimization problem" (L1) but does not explain the trigger mechanism. Is the domain invoked by the pipeline? By the API router? By the developer manually? The answer (based on the API router factory and store) appears to be "by the developer, outside the pipeline," but this is never stated.

### 2. No error handling guidance for plugin or domain authors

Neither building-plugins.md nor building-domains.md addresses what happens when a plugin or domain raises an exception during execution. The dynamic loading section mentions "a warning is logged and that plugin is skipped" for import failures, but execution-time failures are undocumented. A developer needs to know:
- Are exceptions caught by the orchestrator?
- Does a failed plugin prevent downstream consumers from running?
- Should plugins return empty/default data or raise?

### 3. No testing patterns for plugins or domains

A developer writing a plugin needs to construct a `DeliberationState` for unit testing. The schema is documented (building-plugins.md L56-67) but constructing one in a test is not demonstrated. Similarly, `DomainContext` construction for domain tests is undocumented. These are straightforward additions that significantly reduce the barrier to test-driven plugin development.

### 4. Import namespace ambiguity remains unresolved

The SDK guide uses two import namespaces without explaining the relationship:
- `from engine import Deliberation, Result, validate` (sdk.md L14)
- `from engine.sdk import classify` (sdk.md L134)
- `from conversus.schemas.construction import construct_objective` (sdk.md L147)

A developer encountering both `engine.*` and `conversus.*` imports in the same page cannot determine: Are these the same package? Is `engine` a legacy name? Is `conversus` a sub-package? The architecture page explains the package boundaries but the SDK page does not cross-reference it.

### 5. Scaffold parameter `score()` call convention undocumented

The building-domains guide shows scaffold YAML definitions and the scoring pipeline hooks but never shows the actual `score()` call. From the API router factory, the `/submit` endpoint presumably calls `extract()` then `score()`, but a developer building a CLI tool or script that invokes domain scoring directly does not know what arguments `score()` expects. Is the scaffold name a string? A Path? A loaded object?

## Off-Base Assumptions

### 1. Round 1 dispute on sync-first SDK ordering

The synthesis recommended leading with `asyncio.run()` as the first Quick Start code block. I concede this is the right call for the stated goal (first-contact success in a plain `.py` file). However, the synthesis understates a real risk: a developer who learns the sync pattern first may structure their entire integration around `asyncio.run()` wrappers, missing the event subscription pattern entirely (events require an async context). My Round 1 position on tabbed code blocks was contingent on a rendering framework being available; since the documentation is consumed as raw Markdown on GitHub, I accept the sync-first ordering with the caveat that the immediately-following note must explicitly say "Event subscriptions require async context -- see Event Subscription below."

### 2. The "parallel tracks" framing for implementation priority

The synthesis resolved the onboarding-vs-extensibility priority dispute by framing them as "parallel independent tracks." This is technically correct (they touch different files), but it assumes the implementation team has parallel capacity. If resources are serial, the synthesis's own note -- "onboarding changes have higher expected impact per hour due to audience breadth" -- effectively makes onboarding first. I accept this framing but note that the domain tutorial (DA-1) should not be deprioritized to P2 just because onboarding is broader. Both are P1 for their respective audiences.

## Actionable Recommendations

### P1 -- Must implement

**1. Add end-to-end domain tutorial to building-domains.md.**
The current guide demonstrates extract and score in isolation. Add a "Running your domain" section demonstrating the complete 5-stage lifecycle as a connected flow:
- Construct `DomainContext(workspace=Path("."), changed_files=["src/app.py"], metadata={"commit_message": "feat: add caching"})`
- Call extractors: `variables = domain.extract(context)`
- Score with scaffold: `score = domain.score(variables, "default")`
- Create record: `record = domain.create_record(score, context)`
- Persist: `store = JSONLStore(Path("./reviews")); store.append(record)`
- Serve: mount the API router (already documented, cross-reference it)

This is the single highest-impact change for the developer audience. A developer cannot ship a domain plugin from the current docs alone. *Carried forward from Round 1 DA-1. Not challenged on substance; priority dispute resolved by parallel-tracks framing.*

**2. Add practical plugin wiring steps to building-plugins.md.**
Update the "Dynamic loading" section with developer-facing instructions:
- (a) `package` is a Python dotted import path (e.g., `my_project.plugins.scorer`)
- (b) The module must be importable: either `pip install -e .` for local dev or ensure it is on `sys.path`
- (c) The loader finds the first `Plugin` subclass in the module -- name your module accordingly
- (d) If import fails, a warning is logged and the plugin is skipped (non-fatal, but silent failures are hard to debug; check logs)

This complements the `plugins:` config-reference addition (Convergence #3) but addresses a different question: config-reference says *what* the YAML accepts; building-plugins should say *how* to make your code loadable. *Carried forward from Round 1 DA-2. Enriched by code-verifier in Round 1.*

**3. Explain slash commands before the guided workflow in quickstart.md.**
The quickstart jumps from CLI commands (`uv run conversus decide ...`) to slash commands (`/conversus define ...`) at L58-63 without explaining the context switch. A developer reading top-to-bottom will try to type `/conversus define` into their terminal. Add 2-3 sentences: "The guided workflow uses slash commands inside an AI coding assistant (like Claude Code or Cursor). These are not terminal commands." *Carried forward from Round 1 synthesis P1-3. Unchallenged.*

### P2 -- Should implement

**4. Add domain-engine integration subsection to architecture.md.**
After the pipeline data flow diagram (L91), add a subsection explaining:
- Domains are invoked *outside* the deliberation pipeline, not as a pipeline phase
- The typical trigger is the API router's `/submit` endpoint or a developer's script
- `equilibrium_score` (from the nashopt plugin) can bridge the plugin and domain systems -- a domain extractor can consume it
- The architecture diagram should show domains as a separate layer that consumes pipeline output

*Carried forward from Round 1 DA-8. Unchallenged.*

**5. Add error handling guidance for plugin and domain authors.**
Add a subsection to both building-plugins.md and building-domains.md:
- Plugin `execute()` exceptions are caught by the orchestrator, logged at WARNING, and the plugin is skipped for that hook invocation
- Downstream consumers that declared `consumes` on the failed producer's keys will see absent data in `state.plugin_results` -- they must handle missing keys gracefully
- Domain extractor exceptions should return empty dicts rather than raising, to allow partial scoring
- Recommend defensive patterns: `state.plugin_results.get("key", default_value)`

*Carried forward from Round 1 DA-5. User-advocate acknowledged the gap.*

**6. Add testing examples for plugins and domains.**
Add "Testing your plugin" section to building-plugins.md with a minimal example:
```python
state = DeliberationState(mode="cooperative", round=1, agents=[...], ...)
result = MyPlugin().execute(state)
assert "my_metric" in result.data
```
Add equivalent for domains with `DomainContext` construction. These examples serve double duty: they teach testing and they demonstrate object construction, which is currently undocumented for both `DeliberationState` and `DomainContext`.

*Carried forward from Round 1 DA-6. User-advocate acknowledged the gap.*

**7. Add import namespace explanation to SDK guide.**
Add a brief note after the Quick Start imports explaining:
- `engine` is the core deliberation engine package (CLI, providers, phases, events, SDK)
- `conversus` is the solver and plugin infrastructure package (schemas, plugins, domains)
- Both are installed by `uv sync`; they are separate Python packages in the same repo
- `from engine import Deliberation` and `from conversus.schemas.construction import construct_objective` are both correct -- they come from different packages

Cross-reference architecture.md's package boundaries table. *Carried forward from Round 1 DA-9, refined. The `classify` re-export to `engine/__init__` is a code change tracked under CV-4.*

**8. Write SDK Quick Start with sync-first code block.**
Per the synthesis resolution on the async/sync dispute: lead with `asyncio.run()` wrapper as the first code block. Add note immediately below: "The SDK is async-native. Event subscriptions require async context -- see Event Subscription below for `await`-based usage." I accept the sync-first ordering with this strengthened caveat about events.

*Conceding to user-advocate's position per Round 1 synthesis. Adding the event-context note per my Round 1 concern.*

### P3 -- Consider implementing

**9. Add `conversus status` to quickstart after the "Try with a real provider" section.**
After the API key setup, a developer wants to verify their credentials work. `conversus status` provides this verification. Add:
```bash
# Verify your setup
uv run conversus status
```
*Carried forward from Round 1 DA-10. Unchallenged.*

**10. Add minimal "starter config" callout to config-reference.md.**
The config reference opens with the full schema (L7-73), which is 66 lines. A developer scanning for "what is the minimum viable config" must read the entire block to determine which fields are required. Add a 6-line minimal example at the top:
```yaml
mode: cooperative
target: docs/my-proposal.md
output: docs/my-proposal-review/
agents:
  - name: pragmatist
    preset: pragmatist
  - name: devils-advocate
    preset: devils-advocate
```
With the note: "This is all you need. Everything below documents optional fields." The "Common configs" section at L164-196 partially serves this purpose but is buried at the bottom.

*Carried forward from Round 1 UA-9, as modified. Coordinated with the `plugins:` addition but excluding `plugins:` from the minimal example per user-advocate's intimidation concern.*

## Referenced Documentation

| Document | Path | Key observations |
|----------|------|-----------------|
| Quickstart | `docs/user-guide/quickstart.md` | Slash command context switch at L58 is disorienting; no prerequisites callout |
| CLI Reference | `docs/user-guide/cli.md` | `decide` mode table lists 4 but modes page lists 8; no provider precedence note |
| Modes | `docs/user-guide/modes.md` | Complete and accurate; all 8 modes with examples |
| SDK Guide | `docs/user-guide/sdk.md` | Async-first Quick Start; dual import namespaces unexplained; `estimate_cost_usd` absent |
| Config Reference | `docs/user-guide/config-reference.md` | Missing `plugins:` key; full schema before minimal example |
| Architecture | `docs/developer-guide/architecture.md` | Clean pipeline diagram; domains absent from data flow |
| Building Plugins | `docs/developer-guide/building-plugins.md` | Strong produces/consumes explanation; dynamic loading is engine-perspective not developer-perspective |
| Building Domains | `docs/developer-guide/building-domains.md` | 5-stage lifecycle promised, 2 stages demonstrated; no `score()` call shown |
| Construction API | `docs/api/schemas/construction.md` | mkdocstrings directive with explicit member list; blank on GitHub |
| Plugin API | `docs/api/plugins/base.md` | mkdocstrings directive with explicit member list; blank on GitHub |
| Domain API | `docs/api/domains/base.md` | mkdocstrings directive with NO member list (inconsistent with siblings); blank on GitHub |
| Round 1 Synthesis | `specs/031-docs-and-vercel-compliance/conversus-review/round-1/summary/final.md` | 7 convergence points, 7 disputes; this review addresses all |
