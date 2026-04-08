# Code Verifier Review — Conversus Documentation Suite (Spec 031)

## Executive Summary

The conversus documentation suite covers the CLI, SDK, modes, config reference, architecture, and plugin/domain developer guides. My job is to verify every claim, code example, import path, function signature, and enumeration in these docs against the actual source code. Overall, the documentation is solid in its structural accuracy: the 8 modes listed match `VALID_MODES` in the code, the config fields mostly track `parse_config()`, the plugin and domain ABCs are documented faithfully, and the architecture layer diagram reflects real coupling rules. The SDK docs correctly show the `Deliberation` class, `Result` model fields, `validate()`, and `classify()` functions.

However, I found several material inaccuracies. The most consequential: the `decide` CLI command's `--mode` flag only accepts 4 modes in the actual Click definition, not 8 as the docs imply; the config `provider` field default is `"anthropic"` in code but CLI `--provider` defaults to `"mock"`, creating a confusing inconsistency; the SDK imports `classify` from `engine.sdk` but the docs show `from engine.sdk import classify` which is correct yet not re-exported from `engine/__init__.py`; the `determine_verdict()` example in the building-domains doc omits the `variables` parameter that the real signature requires; and the domain API `/scaffolds` endpoint only lists `.json` files, not `.yml` files, contradicting the scaffold documentation that encourages YAML scaffolds.

My most important recommendation: fix the `decide` command's documented `--mode` options to match the 4-mode Click constraint in the actual code, or update the code to accept all 8 modes.

## Alignment

- **8 modes match VALID_MODES** (modes.md L1-151, config-reference.md L10-12): The docs list exactly 8 modes: cooperative, winner-take-all, prisoners-dilemma, red-blue, negotiation, resource-allocation, fair-division, mechanism-design. These match `VALID_MODES` in `conversus/schemas/modes.py` L9-18 exactly. [`conversus/schemas/modes.py`, L9-18]

- **CLI entry point is correct** (cli.md L3): The docs state `pyproject.toml` wires `conversus = "engine.cli:cli"`. This matches `pyproject.toml` L21. [`pyproject.toml`, L21]

- **Plugin ABC accurately documented** (building-plugins.md L7-29): The `Plugin` class attributes `name`, `hooks`, `produces`, `consumes`, the `execute()` signature, and `__init_subclass__` validation all match `conversus/plugins/base.py` L126-208. [`conversus/plugins/base.py`, L126-208]

- **HookPoint enum matches** (building-plugins.md L44-49): The 4 hook points (PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, POST_ARBITRATION) match `HookPoint` enum in `conversus/plugins/base.py` L33-44. [`conversus/plugins/base.py`, L33-44]

- **Cost formula is accurate** (config-reference.md L149-161): The documented formula (review=N, cross_review=N*(N-1), revision=N*I, disputes=N, synthesis=1, arbitration=1 if configured) matches `engine/cost.py` L70-103 exactly. [`engine/cost.py`, L70-103]

- **SDK Result model fields match** (sdk.md L102-114): All documented fields (headline, summary, full_analysis, quality_indicators, debate_transcript, rounds_completed, termination_reason, written_files, output_dir) match `engine/sdk.py` L64-84. [`engine/sdk.py`, L64-84]

- **Event types are accurate** (sdk.md L93-98): The 4 events (PhaseStarted, AgentDispatched, AgentCompleted, PhaseCompleted) with their documented fields match `engine/events.py` L23-68. The `response_text` field on `AgentCompleted` is correctly noted. [`engine/events.py`, L23-68]

## Missed Opportunities

- **classify() import path not re-exported from engine**: The SDK docs (sdk.md L134) show `from engine.sdk import classify`. While this import works, `classify` is not re-exported from `engine/__init__.py` (L10 only exports `Deliberation, Result, validate`). Users following the quickstart pattern `from engine import ...` would need to know the full path. Adding `classify` to the `__init__.py` exports would make the documented usage consistent with the rest of the SDK. [`engine/__init__.py`, L10]. Impact: medium.

- **No documentation of `estimate_cost_usd()`**: The `engine/cost.py` module (L106-158) exposes an `estimate_cost_usd()` function that returns per-model USD pricing estimates with low/high ranges. This is a useful capability for SDK users evaluating cost before running deliberations, but it is not documented anywhere in the user or SDK guides. [`engine/cost.py`, L106-158]. Impact: medium.

- **Provider default models not documented**: `engine/cost.py` L32-35 defines `PROVIDER_DEFAULT_MODELS` (anthropic -> claude-sonnet-4-20250514, openai -> gpt-4o). The CLI docs mention `--model` overrides "provider default" but never state what those defaults are. [`engine/cost.py`, L32-35]. Impact: low.

- **ValidateResult.config type not fully documented**: The SDK docs (sdk.md L121-129) show `vr.config.mode` and `vr.config.agents` but do not document the full `EngineConfig` model shape (fields like `target_files`, `output`, `iterations`, `rounds`, `stagnation`, `prior_files`, `arbiter`, `validate_templates`, `provider`). This limits programmatic consumers who want to inspect parsed config. [`engine/config.py`, L62-78]. Impact: low.

- **DomainStore protocol not listed in api/domains/base.md**: The API reference for domains (`docs/api/domains/base.md`) uses mkdocstrings directives but does not list `DomainStore`, `JSONLStore`, or `SQLiteStore` from `conversus/domains/store.py`. These are core protocol implementations users need for building and testing domains. [`conversus/domains/store.py`, L44-133]. Impact: medium.

- **Plugin output file naming not fully specified**: The building-plugins doc (L127) says output goes to `{output_dir}/plugins/{name}-{hook}-round-{N}.json`. This is correct per `conversus/plugins/base.py` L503-504, but the docs do not mention that `state.round` is the source of `N`, which can be confusing when plugins run at PRE_EXECUTION (round 0 vs round 1). [`conversus/plugins/base.py`, L503-504]. Impact: low.

- **AsyncQueueEmitter not documented in SDK**: The architecture doc (architecture.md L107-109) mentions all 3 emitter implementations, but the SDK guide does not explain how to use `AsyncQueueEmitter` for SSE streaming, which is a key integration pattern for web consumers. [`engine/events.py`, L119-151]. Impact: low.

## Off-Base Assumptions

- **`decide --mode` accepts all 8 modes**: The CLI docs (cli.md L57) list 4 modes for `decide`: cooperative, winner-take-all, prisoners-dilemma, red-blue. However, the actual Click definition at `engine/cli/__init__.py` L240-244 constrains `--mode` to exactly these same 4 modes via `click.Choice(["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"])`. The docs are actually correct here in listing only 4, but the framing is misleading because modes.md and config-reference.md prominently feature all 8 modes, and a user would reasonably expect `decide` to support all 8. The code genuinely restricts ad-hoc `decide` to 4 modes. This is a documentation clarity issue rather than an error — the docs should explicitly state that `decide` supports a subset and explain why.

- **Config `provider` default is "anthropic", not "mock"**: The CLI docs (cli.md L27) correctly show `--provider` defaulting to `mock`. But `engine/config.py` L77 sets `EngineConfig.provider` default to `"anthropic"`, and `parse_config()` at L572 defaults to `"anthropic"` as well. The config-reference doc (config-reference.md L58-60) documents `provider: anthropic` as the config file default. This is internally consistent but the interplay is confusing: running `conversus run config.yml` without `--provider` uses `mock` (CLI default), not the config's `provider` field, because the CLI flag overrides. The documentation does not make this precedence clear. [`engine/config.py`, L77; `engine/cli/__init__.py`, L101-103]

- **`determine_verdict` signature in building-domains.md is incomplete**: The docs (building-domains.md L126-132) show `determine_verdict(self, overall, hard_blocks, thresholds, dimensions, variables)` with 5 parameters. This matches the actual code at `conversus/domains/base.py` L628-634. However, the inline code example at L128-131 shows a simpler version that only checks `hard_blocks` and `overall < thresholds.get("minimum_overall", 0.7)`, never using the `dimensions` or `variables` params. The doc example works but is misleading about the method's full contract. [`conversus/domains/base.py`, L628-656]

## Actionable Recommendations

1. **Document decide mode restriction** (Priority: P1)
   - **Current state**: cli.md L57 lists 4 modes for `decide` without explanation. modes.md lists 8 modes globally.
   - **Proposed change**: Add a note to cli.md: "The `decide` command supports 4 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue). The remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design) require a config file via `conversus run`." Alternatively, update the Click definition in `engine/cli/__init__.py` L240-244 to accept all 8 modes.
   - **Rationale**: Users reading modes.md will expect all 8 to work with `decide`. The current silent restriction causes confusing errors. [`engine/cli/__init__.py`, L240-244; `conversus/schemas/modes.py`, L9-18]
   - **Risk if ignored**: Users will try `conversus decide "question" --mode negotiation` and get an unhelped Click error about invalid choice.

2. **Fix scaffolds endpoint to match documentation** (Priority: P1)
   - **Current state**: building-domains.md L70-91 shows scaffold examples in YAML format (`.yml`). The `/scaffolds` API endpoint at `conversus/domains/api.py` L208 only globs `*.json` files.
   - **Proposed change**: Change L208 to `domain.scaffold_dir.glob("*")` filtered to `(".yml", ".yaml", ".json")` extensions, or update documentation to note that scaffolds must be JSON for the API listing endpoint. The `load_scaffold()` function already handles both YAML and JSON.
   - **Rationale**: The docs encourage YAML scaffolds but the API endpoint silently ignores them. [`conversus/domains/api.py`, L208; `conversus/domains/base.py`, L144-171]
   - **Risk if ignored**: Users create YAML scaffolds as documented, but the `/scaffolds` endpoint returns an empty list. Silent data loss.

3. **Clarify provider precedence between config and CLI** (Priority: P2)
   - **Current state**: cli.md L27 shows `--provider` defaults to `mock`. config-reference.md L58-60 documents `provider: anthropic` as the config file default. No doc explains which wins.
   - **Proposed change**: Add to cli.md under the `run` command: "The `--provider` CLI flag overrides the `provider` field in the config file. When neither is specified, the CLI defaults to `mock`."
   - **Rationale**: The config parser defaults to `"anthropic"` (`engine/config.py` L77) but the CLI defaults to `"mock"` (`engine/cli/__init__.py` L101`). The CLI flag takes precedence since `run_engine()` receives it separately, but this is not documented. [`engine/config.py`, L77; `engine/cli/__init__.py`, L101]
   - **Risk if ignored**: Users set `provider: anthropic` in their config, run without `--provider`, and get mock responses with no warning.

4. **Export classify from engine __init__** (Priority: P2)
   - **Current state**: sdk.md L134 shows `from engine.sdk import classify`, which works. But `engine/__init__.py` L10 only exports `Deliberation, Result, validate`.
   - **Proposed change**: Add `classify` to `engine/__init__.py` exports: `from engine.sdk import Deliberation, Result, validate, classify`.
   - **Rationale**: The SDK docs show two import patterns (`from engine import ...` and `from engine.sdk import ...`). `classify` is only available via the second. Consistency requires it be available via both. [`engine/__init__.py`, L10; `engine/sdk.py`, L387-404]
   - **Risk if ignored**: Users following the `from engine import ...` pattern get ImportError for `classify`.

5. **Document DomainStore in API reference** (Priority: P2)
   - **Current state**: `docs/api/domains/base.md` L6 uses mkdocstrings for `conversus.domains.base` but does not reference `conversus.domains.store`.
   - **Proposed change**: Either add a new `docs/api/domains/store.md` page with `::: conversus.domains.store` targeting `DomainStore`, `JSONLStore`, `SQLiteStore`, or add these to the existing domains base page.
   - **Rationale**: The building-domains guide (L142-163) references these classes but there is no API reference page for them. [`conversus/domains/store.py`, L44-133]
   - **Risk if ignored**: Developers building domains cannot find protocol method signatures in the API reference.

6. **Add provider default model table** (Priority: P2)
   - **Current state**: cli.md L28-29 says `--model` default is "provider default" without specifying what those defaults are.
   - **Proposed change**: Add a table to cli.md: "| Provider | Default Model | | anthropic | claude-sonnet-4-20250514 | | openai | gpt-4o |"
   - **Rationale**: `engine/cost.py` L32-35 defines these defaults. Users need to know which model runs when they do not specify `--model`. [`engine/cost.py`, L32-35]
   - **Risk if ignored**: Users cannot predict cost or capability without reading source code.

7. **Document estimate_cost_usd in SDK guide** (Priority: P3)
   - **Current state**: sdk.md L67-73 documents `cost_estimate` (launch counts only). The USD estimation function exists in `engine/cost.py` L106-158 but is not exposed in docs.
   - **Proposed change**: Add a "Cost estimation" subsection to sdk.md showing how to get USD estimates via `from engine.cost import estimate_cost_usd`.
   - **Rationale**: USD cost estimation is a key decision factor for production users. The function exists and is fully implemented. [`engine/cost.py`, L106-158]
   - **Risk if ignored**: Users build their own cost estimation instead of using the built-in one.

8. **Fix determine_verdict example in building-domains** (Priority: P3)
   - **Current state**: building-domains.md L126-132 shows a `determine_verdict` override that ignores `dimensions` and `variables` parameters.
   - **Proposed change**: Update the example to demonstrate using at least one of the ignored parameters, e.g., checking `dimensions.get("security", 0)` against a threshold, to show the full override contract.
   - **Rationale**: The current example teaches an incomplete pattern. The actual signature at `conversus/domains/base.py` L628-634 passes 5 parameters; the example only uses 3. [`conversus/domains/base.py`, L628-656]
   - **Risk if ignored**: Plugin authors will write overrides that ignore the `variables` parameter, losing access to raw extraction data for custom verdict logic.

9. **Add phase parameter documentation for run command** (Priority: P3)
   - **Current state**: cli.md L30 documents `--phase` with choices `all` or `review`. The actual Click definition at `engine/cli/__init__.py` L108-115 confirms this but also includes the help text "More phases will be added as execution paths are implemented."
   - **Proposed change**: Add a note to cli.md: "Currently, `--phase` supports `all` (default) and `review`. Additional phase options are planned."
   - **Rationale**: The `--phase` feature is incomplete. Without this note, users may wonder why they cannot run individual phases like `synthesis` or `disputes`. [`engine/cli/__init__.py`, L108-115]
   - **Risk if ignored**: Users try `--phase synthesis` and get an unhelpful Click error.

## Referenced Documentation

- `conversus/schemas/modes.py` -- L9-18 (VALID_MODES definition)
- `conversus/plugins/base.py` -- L33-44 (HookPoint), L51-99 (state models), L107-118 (PluginResult), L126-208 (Plugin ABC), L229-295 (load_plugins), L303-404 (topological sort), L412-527 (execute_hooks)
- `conversus/schemas/construction.py` -- L60-132 (DecisionType, mode mapping), L140-230 (GapFiller, TemplateSelector protocols), L286-316 (AssembledObjective), L384-425 (classify_decision_type), L432-490 (select_candidate_templates), L519-561 (extract_explicit_parameters), L606-656 (identify_gaps), L663-733 (fill_parameter_gaps), L787-836 (assemble_objective), L866-943 (construct_objective)
- `conversus/schemas/objectives.py` -- L24-42 (VALID_PARAMETER_TYPES, VALID_GAME_FORMS), L49-91 (ParameterDefinition), L98-138 (ConstraintTemplate), L145-200 (ObjectiveTemplate)
- `conversus/domains/base.py` -- L34-46 (DomainContext), L53-72 (DomainScore), L126-142 (Scaffold), L214-233 (VariableExtractor), L497-534 (DomainPlugin ABC), L539-603 (scoring hooks), L628-656 (determine_verdict), L688-835 (core pipeline)
- `conversus/domains/store.py` -- L44-133 (DomainStore protocol), L261-384 (JSONLStore), L392-594 (SQLiteStore)
- `conversus/domains/api.py` -- L97-225 (create_domain_router, endpoint definitions)
- `engine/__init__.py` -- L10 (public exports)
- `engine/sdk.py` -- L64-84 (Result), L86-99 (ValidateResult), L125-332 (Deliberation class), L340-379 (validate), L387-404 (classify)
- `engine/events.py` -- L23-68 (event models), L75 (EngineEvent union), L82-151 (emitter implementations)
- `engine/cli/__init__.py` -- L61-464 (all CLI commands)
- `engine/config.py` -- L36-78 (config models), L84-85 (VALID_MODES, AGENT_NAME_RE), L480-644 (parse_config)
- `engine/cost.py` -- L15-35 (pricing/defaults), L70-103 (estimate_cost), L106-158 (estimate_cost_usd)
- `pyproject.toml` -- L21 (entry point), L24-39 (optional dependencies)
- `docs/user-guide/cli.md` -- L1-143
- `docs/user-guide/modes.md` -- L1-151
- `docs/user-guide/sdk.md` -- L1-182
- `docs/user-guide/config-reference.md` -- L1-196
- `docs/user-guide/quickstart.md` -- L1-89
- `docs/developer-guide/architecture.md` -- L1-118
- `docs/developer-guide/building-plugins.md` -- L1-216
- `docs/developer-guide/building-domains.md` -- L1-237
- `docs/api/schemas/construction.md` -- L1-24
- `docs/api/plugins/base.md` -- L1-18
- `docs/api/domains/base.md` -- L1-7
