# Developer Advocate Review — Conversus Documentation Suite

**Reviewer role:** developer-advocate
**Review date:** 2026-04-02
**Target:** Conversus documentation (user guide, developer guide, API reference)

---

## Executive Summary

The Conversus documentation suite provides a reasonably complete picture of the system from a user perspective. The quickstart gets a developer from zero to a working deliberation in under a minute, the CLI reference covers all six commands with option tables and exit codes, and the modes page gives clear guidance on when to use each of the eight modes. The SDK documentation provides working async patterns and the event subscription model is well-documented. For someone who wants to *use* Conversus, the docs are functional.

The developer-facing documentation -- building plugins and building domains -- is where the quality diverges sharply. The plugin guide successfully explains the Plugin ABC, the hook lifecycle, and the produces/consumes data flow pattern with enough detail that a developer could build a plugin from the guide alone. The domain guide, however, has significant gaps: the scoring pipeline documentation does not match the actual base class implementation in several places, the relationship between domains and the rest of the system is underspecified, and there is no explanation of how to actually *run* a domain plugin end-to-end. The API reference pages for plugins and domains are stub pages that delegate to mkdocstrings autodoc directives rather than providing narrative documentation, which means a developer without the source code installed gets nothing from them.

The single most important recommendation is: **add a complete end-to-end walkthrough for building and running a domain plugin, including the extraction, scoring, persistence, and API serving steps, because the current guide stops at class definition and never shows how to wire a domain into a running system.**

---

## Alignment

- **[Mock provider for zero-cost exploration]** (`quickstart.md`, L19-22): The quickstart immediately uses `--provider mock` so developers can explore the full pipeline without API keys or cost. This is the correct onboarding pattern -- it removes the highest friction point (credential setup) from the first-contact experience.

- **[Cost estimation before execution]** (`cli.md`, L63-91; `sdk.md`, L67-73): Both the CLI (`conversus validate`) and the SDK (`d.cost_estimate`) expose cost estimation before running any LLM calls. This is critical for developer trust -- you can reason about what a deliberation will cost before committing to it. The per-phase breakdown makes the formula transparent.

- **[Produces/consumes plugin data flow]** (`building-plugins.md`, L92-123): The cross-plugin data flow section explains the dependency graph clearly with a concrete producer/consumer example. The topological sort guarantee, cycle detection, and duplicate producer errors are all documented. A developer can understand and use this pattern from the guide alone.

- **[Scaffold-based scoring configuration]** (`building-domains.md`, L70-98): The scaffold YAML format is well-documented with a concrete example showing weights, thresholds, and hard blocks. The three hard block rule forms (truthy, comparison, boolean equality) are enumerated. A developer can write a scaffold from this documentation.

- **[Event subscription model]** (`sdk.md`, L77-98): The event system is documented with concrete lambda examples and a complete event type table with fields and timing. This is exactly the level of detail a developer needs to integrate Conversus into a CI/CD pipeline or monitoring system.

---

## Missed Opportunities

- **[No end-to-end domain tutorial]**: The building-domains guide (`building-domains.md`, L1-237) defines the ABC and shows class definitions, but never demonstrates how to run a domain plugin end-to-end. There is no example of: creating a `DomainContext`, calling `extract()` then `score()`, persisting with a store, or mounting the API router on a running FastAPI app. The API router factory section (L166-190) shows the wiring code but does not explain how to actually start the server or test the endpoints. A developer cannot build and *run* a domain from the guide alone. **Impact: high.**

- **[No plugin registration/wiring documentation]**: The building-plugins guide (`building-plugins.md`, L140-170) explains dynamic loading and the YAML config entry, but does not document how to make a plugin discoverable. Is the `package` field a Python import path? Must the plugin be installed as a package, or can it be a local file? The `importlib.import_module` detail (L166) implies it must be on the Python path, but this is not stated explicitly. A developer building their first plugin will not know how to wire it in. **Impact: high.**

- **[No error handling guidance for plugin/domain authors]**: Neither the plugin guide nor the domain guide explains what happens when `execute()` or `extract()` raises an exception. The source code (`base.py`, L486-525 in plugins; L697-709 in domains) shows that exceptions are caught, logged, and skipped -- but this is not documented. A developer needs to know: should they raise or return empty? What logging is available? What happens to downstream consumers when a producer fails? **Impact: medium.**

- **[No testing guidance for plugins or domains]**: Neither developer guide includes any information on how to test a plugin or domain. There are no test fixtures, no mock `DeliberationState` factory, no example test file. The `AgentState` and `RoundState` models are frozen Pydantic, which means a developer needs to construct them with all required fields. A "testing your plugin" section with a minimal pytest example would significantly lower the barrier. **Impact: medium.**

- **[API reference pages are autodoc stubs]**: The API reference pages (`api/plugins/base.md`, L1-18; `api/domains/base.md`, L1-6; `api/schemas/construction.md`, L1-24) contain only mkdocstrings directives (`::: conversus.plugins.base`, etc.). Without a running mkdocs build, these pages are unreadable. They provide no narrative context, no usage examples, and no explanation of the relationships between the listed members. A developer reading the docs on GitHub or in a static context gets nothing. **Impact: medium.**

- **[No documentation of the `VariableExtractor` protocol contract]**: The building-domains guide (`building-domains.md`, L36-68) shows the `VariableExtractor` protocol with `name`, `variables`, and `extract()`, but does not explain what happens when an extractor returns a key not in its `variables` list, or when it returns `{}` for a required variable. The source code does not enforce the `variables` declaration at extraction time -- it is purely informational. This should be stated explicitly. **Impact: low.**

- **[Config reference missing plugin configuration section]**: The config-reference page (`config-reference.md`, L1-196) documents all top-level config fields including agents, arbiter, targets, and iterations, but has no section for the `plugins:` key. The building-plugins guide (`building-plugins.md`, L140-152) shows the YAML syntax, but a developer looking at the config reference as the single source of truth will not find it. **Impact: medium.**

- **[No documentation of how domains relate to the engine pipeline]**: The architecture page (`architecture.md`, L1-118) describes the three-layer architecture and the engine pipeline phases, but does not explain where domain plugins fit into the execution flow. The domain layer is mentioned in the architecture diagram (L9-11) but the data flow section (L48-91) only covers the core deliberation pipeline, not the domain scoring pipeline. A developer cannot understand how the engine invokes a domain. **Impact: medium.**

---

## Off-Base Assumptions

- **[Domain guide `determine_verdict` signature mismatch]**: The building-domains guide (`building-domains.md`, L126-132) shows `determine_verdict(self, overall, hard_blocks, thresholds, dimensions, variables)` as a method the developer overrides. The example code (L126-132) checks `overall < thresholds.get("minimum_overall", 0.7)` -- but the base class's default `determine_verdict` implementation (`base.py`, L628-656) delegates to `_determine_verdict` (L355-375), which checks individual dimension thresholds, not `minimum_overall`. The guide's example implements logic that is *not* the default -- it is the code-review domain's override. A developer following the guide will assume the default behavior includes `minimum_overall` checking, which it does not. The default behavior only checks hard blocks and per-dimension thresholds.

- **[Hard blocks documentation inconsistency]**: The building-domains scaffold documentation (`building-domains.md`, L88-96) states hard blocks support "bare truthy checks (`secrets_exposed`), comparisons (`critical_vulns > 0`), boolean equality (`has_spec == false`)". However, the `_check_hard_blocks` function (`base.py`, L302-352) only supports the three-part comparison form (`variable operator threshold`), not bare truthy checks. The bare truthy form is only supported in `_evaluate_single_hard_block` (`base.py`, L378-441), which is called by `_evaluate_hard_block_rules`. The `DomainPlugin.evaluate_hard_blocks()` method (`base.py`, L605-626) correctly delegates to `_evaluate_hard_block_rules`, so the documented behavior is correct for domains, but the internal `_check_hard_blocks` function (which could be called independently) behaves differently. This is not a documentation error for the domain guide specifically, but the existence of two different hard block evaluation functions with different capabilities is confusing and should be clarified.

---

## Actionable Recommendations

1. **Add end-to-end domain tutorial** (Priority: P1)
   - **Current state**: `building-domains.md` stops at class definition (L192-237) and the API router section (L166-190) shows wiring but not execution.
   - **Proposed change**: Add a "Running your domain" section after the example that shows: (a) constructing a `DomainContext`, (b) calling `domain.extract(context)` then `domain.score(variables, "default")`, (c) creating a record with `domain.create_record(score, context)`, (d) persisting with `JSONLStore`, and (e) mounting and testing the API router. Include a `if __name__ == "__main__"` block that runs the full pipeline.
   - **Rationale**: The five-stage lifecycle (extract, score, persist, gate, serve) is stated at `building-domains.md`, L4 but only stages 1-2 are demonstrated. A developer cannot build a domain from the guide alone without this.
   - **Risk if ignored**: Developers will need to read the source code to understand how to wire a domain into a running system, defeating the purpose of a developer guide.

2. **Document plugin wiring and discoverability** (Priority: P1)
   - **Current state**: `building-plugins.md`, L140-170 mentions dynamic loading via `importlib.import_module` but does not explain how to make a plugin importable.
   - **Proposed change**: Add a "Making your plugin discoverable" section that explains: (a) the `package` field is a Python dotted import path, (b) the module must be on `sys.path` (installed via pip/uv or in the project's package list), (c) local development option (add to `packages` in pyproject.toml or use `pip install -e .`), and (d) a minimal pyproject.toml for a standalone plugin package.
   - **Rationale**: The `load_plugins` function in `base.py`, L229-295 uses `importlib.import_module(package)`, which requires the package to be importable, but this is never stated in the guide.
   - **Risk if ignored**: Developers will create plugin files that are not importable and receive silent warnings (the plugin is skipped, not crashed -- `base.py`, L264-269), making debugging extremely difficult.

3. **Add `plugins:` key to config reference** (Priority: P1)
   - **Current state**: `config-reference.md` documents all top-level keys but omits `plugins:`.
   - **Proposed change**: Add a "Plugins" section after "Arbiter" with the full schema:
     ```yaml
     plugins:
       - name: <string>       # Plugin identifier
         package: <string>    # Python import path
         config: {}           # Plugin-specific config (optional)
     ```
     Include a note that plugins are loaded in declaration order but executed in topological order based on produces/consumes.
   - **Rationale**: The config reference is the single source of truth for the YAML schema (`config-reference.md`, L1-2). Omitting `plugins:` means a developer must find it in a separate guide.
   - **Risk if ignored**: Developers will not know plugins exist when reading the config reference, and those who do find the plugin guide will have to context-switch between two documents to write a correct config.

4. **Replace API reference stubs with narrative documentation** (Priority: P2)
   - **Current state**: `api/plugins/base.md` (L5-18), `api/domains/base.md` (L5-6), and `api/schemas/construction.md` (L5-24) contain only mkdocstrings directives.
   - **Proposed change**: Add a brief narrative section (3-5 sentences) before each autodoc directive explaining what the module does, its key classes, and how they relate. For `api/domains/base.md`, add the full member list as is done in `api/plugins/base.md`. For all three, add a "See also" link to the relevant developer guide page.
   - **Rationale**: Autodoc directives are only useful in a built documentation site. When viewed on GitHub, in an IDE, or before the docs site is deployed, these pages are effectively empty.
   - **Risk if ignored**: The API reference section of the docs will be useless to anyone not running `mkdocs serve` locally.

5. **Add error handling guidance for plugin and domain authors** (Priority: P2)
   - **Current state**: Neither `building-plugins.md` nor `building-domains.md` documents exception behavior.
   - **Proposed change**: Add a "Error handling" subsection to each guide explaining: (a) exceptions in `execute()`/`extract()` are caught, logged at WARNING, and the plugin/extractor is skipped, (b) downstream consumers will not see the failed producer's data in `plugin_results`, (c) recommended pattern is to return empty/default data rather than raising, (d) use `logging.getLogger("conversus.plugins")` or `logging.getLogger("conversus.domains")` for debugging.
   - **Rationale**: The resilient skip-on-error behavior (`base.py`, L519-525 for plugins; L700-708 for domains) is a design choice that affects how developers structure their code, but it is invisible in the documentation.
   - **Risk if ignored**: Developers will raise exceptions expecting them to propagate, then wonder why their plugin silently does nothing.

6. **Add testing examples for plugins and domains** (Priority: P2)
   - **Current state**: No testing guidance exists in either developer guide.
   - **Proposed change**: Add a "Testing your plugin" section with: (a) constructing a minimal `DeliberationState` with required fields, (b) calling `plugin.execute(state)` and asserting on the `PluginResult`, (c) testing produces/consumes with `execute_hooks`. Add equivalent for domains: constructing `DomainContext`, calling `extract()` and `score()`.
   - **Rationale**: All state models are frozen Pydantic (`base.py`, L57, L69, L79, L90, L107, L114), which means construction requires explicit field values. Without examples, developers will struggle to create test fixtures.
   - **Risk if ignored**: Developers will skip testing their plugins, leading to runtime failures that are silently swallowed.

7. **Fix `determine_verdict` documentation to match base class default** (Priority: P2)
   - **Current state**: `building-domains.md`, L126-132 shows a `determine_verdict` override that checks `minimum_overall`, implying this is the default behavior.
   - **Proposed change**: Separate the example into two parts: (a) "Default behavior" explaining that the base class checks hard blocks then per-dimension thresholds (matching `base.py`, L628-656 -> `_determine_verdict`, L355-375), and (b) "Customizing verdict logic" showing the `minimum_overall` pattern as an explicit override example with a note that this is not the default.
   - **Rationale**: The current presentation conflates the base class default with a domain-specific override, which will mislead developers who expect the default to handle `minimum_overall`.
   - **Risk if ignored**: Developers will omit `determine_verdict` overrides expecting `minimum_overall` to work automatically, and their domains will pass reviews that should be flagged for revision.

8. **Document domain-engine integration in architecture page** (Priority: P2)
   - **Current state**: `architecture.md`, L9-11 mentions domains in the layer diagram, and L48-91 shows the engine data flow, but does not explain how domains connect to the engine pipeline.
   - **Proposed change**: Add a "Domain integration" subsection after the pipeline data flow that explains: domains are invoked separately from the deliberation pipeline (via the API router or direct SDK calls), they consume deliberation output (synthesis text, quality indicators) as input context, and the `equilibrium_score` field on `DomainRecord` is the bridge between the plugin system and the domain system.
   - **Rationale**: The architecture diagram shows three layers but does not explain how data flows between the engine layer and the domain layer. A developer reading the architecture page cannot understand where domains fit.
   - **Risk if ignored**: Developers will assume domains are invoked automatically during the deliberation pipeline (like plugins), when in fact they are a separate system.

9. **Add import path examples that match actual package structure** (Priority: P3)
   - **Current state**: `sdk.md`, L14 uses `from engine import Deliberation, Result, validate` and L134 uses `from engine.sdk import classify`. `building-domains.md`, L11-16 uses `from conversus.domains.base import ...`. The construction example (`sdk.md`, L147) uses `from conversus.schemas.construction import construct_objective`.
   - **Proposed change**: Add a note in the SDK page explaining the dual package structure: `engine` is the top-level namespace for the deliberation engine, while `conversus` is the top-level namespace for schemas, plugins, and domains. Confirm that both are importable after `uv sync` (which they are per `pyproject.toml`, L59: `packages = ["engine", "linter", "web", "conversus"]`).
   - **Rationale**: The two different top-level import namespaces (`engine.*` vs `conversus.*`) are confusing for a new developer. The architecture page explains the coupling rules but does not map them to import paths.
   - **Risk if ignored**: Minor confusion, but developers may try `from conversus.engine import ...` or `from engine.plugins import ...` and get import errors.

10. **Add `conversus status` to the quickstart flow** (Priority: P3)
    - **Current state**: `quickstart.md` jumps from mock provider (L19) to real provider (L41-52) without showing how to verify credentials are configured.
    - **Proposed change**: After the "Try with a real provider" section, add: `conversus status` to verify the provider is authenticated before running the deliberation.
    - **Rationale**: `cli.md`, L117-125 documents `conversus status` as showing auth state for all providers, but it is not mentioned in the quickstart flow where it would be most useful.
    - **Risk if ignored**: Developers will skip straight to running with a real provider, get a credential error, and not know `conversus status` exists.

---

## Referenced Documentation

- `docs/user-guide/quickstart.md` -- sections/lines cited: L19-22, L41-52
- `docs/user-guide/cli.md` -- sections/lines cited: L1-3, L63-91, L117-125
- `docs/user-guide/modes.md` -- sections/lines cited: L1-151 (full file read, mode descriptions verified)
- `docs/user-guide/sdk.md` -- sections/lines cited: L14, L67-73, L77-98, L134, L147, L159-170
- `docs/user-guide/config-reference.md` -- sections/lines cited: L1-2, L1-196 (full schema review)
- `docs/developer-guide/architecture.md` -- sections/lines cited: L1-118, L9-11, L48-91
- `docs/developer-guide/building-plugins.md` -- sections/lines cited: L1-216, L92-123, L140-170
- `docs/developer-guide/building-domains.md` -- sections/lines cited: L1-237, L4, L36-68, L70-98, L88-96, L126-132, L166-190, L192-237
- `docs/api/schemas/construction.md` -- sections/lines cited: L1-24
- `docs/api/plugins/base.md` -- sections/lines cited: L1-18
- `docs/api/domains/base.md` -- sections/lines cited: L1-6
- `conversus/plugins/base.py` -- sections/lines cited: L229-295, L264-269, L302-352, L378-441, L486-525, L519-525, L57, L69, L79, L90, L107, L114
- `conversus/domains/base.py` -- sections/lines cited: L355-375, L497-516, L605-626, L628-656, L697-709
- `pyproject.toml` -- sections/lines cited: L21, L59
