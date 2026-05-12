# Code Verifier -- Round 2 Review

## Executive Summary

Round 1 produced strong convergence on the highest-impact issues: the `decide` 4-mode constraint, the scaffolds endpoint YAML bug, the `plugins:` config key gap, API reference prose, and the `determine_verdict` documentation split. I accept all seven convergence items and the synthesizer's disposition of the disputes. This round focuses on (a) confirming previously-identified issues are correctly characterized in the synthesis, (b) surfacing new code-level findings discovered while re-reading source for Round 2 verification, and (c) responding to the synthesizer's specific assessments on the remaining disputes.

No Round 1 concessions are reversed. Four recommendations are carried forward from Round 1 without modification. Six new findings emerge from deeper source code inspection.

## Alignment

### Convergence items I fully support

1. **CV-1 / `decide` 4-mode restriction** (converged, unanimous). Confirmed again: `engine/cli/__init__.py` L240-241 defines `click.Choice(["cooperative", "winner-take-all", "prisoners-dilemma", "red-blue"])`. The docs at `cli.md` L57 list exactly these four. The note agreed upon ("For the remaining 4 modes, use `conversus run`") is accurate and necessary.

2. **CV-2 / scaffolds endpoint YAML glob** (converged, bilateral). Confirmed: `api.py` L208 reads `domain.scaffold_dir.glob("*.json")`. The `load_scaffold()` function at `base.py` L144-171 handles `.yml`, `.yaml`, and `.json`. The endpoint is the sole outlier.

3. **CV-B / `plugins:` key in config-reference.md** (converged, unanimous). Confirmed: `load_plugins()` at `plugins/base.py` L229-295 consumes `name`, `package`, and `config` keys. `parse_config()` at `engine/config.py` does not parse or validate a `plugins:` key, meaning plugin config is consumed downstream by a separate loader. The docs must document this schema so users know the key exists and what it expects.

4. **CV-A / narrative prose on API reference pages** (converged, unanimous). The `domains/base.md` file is the weakest: it has no `members:` list at all (just `::: conversus.domains.base` with no options block), unlike `plugins/base.md` and `construction.md` which both have explicit member filters. I maintain this inconsistency must be fixed.

5. **CV-8 / `determine_verdict` split** (converged, bilateral). Confirmed: the base class `determine_verdict` at `base.py` L628-656 calls `_determine_verdict()` which checks hard blocks then per-dimension thresholds. It does NOT check `minimum_overall`. The building-domains.md example at L126-132 shows a `minimum_overall` check that is not the base class behavior. The agreed split into "Default behavior" and "Customizing verdict logic" is correct.

6. **CV-3 / provider precedence note** (converged, unanimous). Confirmed: `run_engine()` at `engine/run.py` L165-261 takes `provider_name` as a parameter and calls `resolve_provider(provider_name)` at L207. It never reads `config.provider`. The CLI `run` command passes its `--provider` flag value (default `"mock"`) directly. The config file's `provider` field is genuinely never consulted on the CLI path.

7. **CV-7 / `estimate_cost_usd()` documentation** (converged, bilateral). Confirmed: `engine/cost.py` L106-158 implements this function with full signature and return type. It is not exported from `engine/__init__.py`, not mentioned in the SDK guide, and not shown in the CLI reference.

### Round 1 dispositions I accept

- **Synthesizer's recommended resolution on sync-first SDK Quick Start**: I accept the synthesizer's recommendation to lead with `asyncio.run()` wrapper followed by an async-native note. My original concern about "conceptual mismatch" was valid architecturally but the synthesizer correctly identified that Quick Start sections are not read linearly. The practical risk (SyntaxError on first paste) outweighs the architectural purism.

- **Synthesizer's recommended resolution on implementation priority**: I accept that onboarding and extensibility are independent tracks, not sequential.

- **Synthesizer's recommended resolution on quickstart micro-hints**: I accept the micro-hint proposal. Two lines do not violate the brevity principle.

## Missed Opportunities

### 1. CLI epilog contains an invalid `--phase synthesis` example

The `run` command's epilog at `engine/cli/__init__.py` L95 shows:
```
conversus run config.yml --provider openai --phase synthesis
```

But the Click definition at L110-113 constrains `--phase` to `["all", "review"]` only:
```python
type=click.Choice(
    ["all", "review"],
    case_sensitive=False,
),
```

This means typing `--phase synthesis` at the CLI will produce a Click error. The docs at `cli.md` L30 correctly list only `all` and `review` for `--phase`, but the CLI's own help text (`conversus run --help`) displays the invalid example. This is a code bug in the epilog, not a docs bug.

### 2. `run` command `--phase` option accepts `review` but docs say nothing about what it does

The `cli.md` docs at L30 say: `--phase | all | Phase to run (all or review)`. The `run_engine()` function at `engine/run.py` L238-256 confirms that `"review"` runs Phase 1 only. But the docs do not explain what "Phase 1 only" means in practical terms (you get agent reviews but no cross-review, revision, disputes, or synthesis). This leaves users guessing what a partial run produces.

### 3. `AgentCompleted` event model has a `response_text` field not shown in SDK event table

The events documentation in `sdk.md` L93-98 lists `AgentCompleted` fields as: `phase`, `agent_name`, `success`, `error`, `duration_ms`, `response_text`. Actually, looking more carefully, `response_text` IS listed. Good -- this is accurate.

However, the `AgentCompleted` model at `engine/events.py` L44-56 shows `response_text: str | None = None` as an optional field with a default. The SDK docs list it without marking it as optional. Minor, but if someone destructures the event without checking for None, they will hit issues.

### 4. `CallbackEmitter` takes a callable, not a handler class

The `architecture.md` event system table at L107 says `CallbackEmitter` uses "Sync callback" transport and lists its use case as "CLI (Rich progress), SDK". The actual implementation at `engine/events.py` L94-105 takes a `Callable[[EngineEvent], None]`. But the CLI `run` command at `engine/cli/__init__.py` L128-129 instantiates it as `CallbackEmitter(progress_handler)` where `progress_handler` is a `RichProgressHandler` instance. The `CallbackEmitter` calls `self._callback(event)` on the handler, meaning `RichProgressHandler` must be callable (implement `__call__`). This is an implementation detail that developers building custom emitters need to understand and is not documented.

### 5. `EngineConfig.provider` defaults to `"anthropic"` in code, but CLI defaults to `"mock"`

The `EngineConfig` model at `engine/config.py` L77 has `provider: str = "anthropic"`. The CLI `run` command at L101-103 defaults `--provider` to `"mock"`. The `decide` command at L234 also defaults to `"mock"`. The `Deliberation` SDK class at `engine/sdk.py` L155 defaults `provider` to `"mock"`. This means:
- Config file default: `"anthropic"` (when `provider` key is omitted from YAML)
- CLI default: `"mock"` (when `--provider` flag is omitted)
- SDK default: `"mock"` (when `provider` kwarg is omitted)

The config-reference.md at L58-60 says `provider: anthropic` with the comment "CLI --provider flag overrides this." But this doesn't explain the three-way default mismatch. A user who writes a config file without `provider:` gets `anthropic`; a user who runs `conversus run config.yml` without `--provider` gets `mock`. This is the deeper manifestation of the provider precedence issue identified in Round 1.

### 6. `classify` function is defined in `engine/sdk.py` but not exported from `engine/__init__.py`

The SDK docs at `sdk.md` L134-138 show:
```python
from engine.sdk import classify
```

The function exists at `engine/sdk.py` L387-404. But `engine/__init__.py` at L10 exports only `Deliberation, Result, validate` -- not `classify`. The Round 1 synthesis actionable item #16 addresses this, so I am noting it here for completeness as a confirmed finding that persists.

## Off-Base Assumptions

### 1. The docs assume `construct_objective` returns an object with a `symbolic_form` string attribute

The SDK docs at `sdk.md` L155-157 show:
```python
print(objective.template_name)   # e.g., "competitive-selection"
print(objective.game_form)       # e.g., "normal-form"
print(objective.parameters)      # Extracted + filled parameters
print(objective.symbolic_form)   # Mathematical formulation
```

This is accurate to the `AssembledObjective` model at `construction.py` L286-316, which does have these fields. However, calling `construct_objective()` with just `problem_text` and `mode` may raise a `ValueError` if no templates match or if the `NonInteractiveGapFiller` (the default) encounters parameters without defaults. The docs show a clean happy path without mentioning these failure modes.

### 2. The docs present `Deliberation.cost_estimate` as always returning a dict

The SDK docs at `sdk.md` L70-73 show:
```python
d = Deliberation(config_path=Path("conversus.yml"))
print(d.cost_estimate)
# {'review': 3, 'cross_review': 6, 'revision': 3, 'disputes': 3, 'synthesis': 1}
```

The property at `engine/sdk.py` L182-205 returns `dict[str, int] | None`. It returns `None` if the config cannot be parsed. The docs should note this nullable return.

### 3. The docs assume all 8 modes work with the `decide` command

This was resolved in Round 1, but I want to confirm: the modes documentation at `modes.md` lists all 8 modes without indicating which ones are CLI-accessible. The Round 1 convergence item properly addresses this.

## Actionable Recommendations

### P1 -- Must implement

**1. Fix the `run` command epilog to remove the invalid `--phase synthesis` example.**
The CLI's own help text at `engine/cli/__init__.py` L95 shows `--phase synthesis`, but Click constrains this to `["all", "review"]` at L110-113. Running `conversus run --help` displays an example that will fail. This is a code bug.
- **Source**: `engine/cli/__init__.py` L95, L110-113.
- **Round 1 context**: This is a new finding in Round 2. Not addressed in Round 1.
- **Fix**: Change L95 from `conversus run config.yml --provider openai --phase synthesis` to `conversus run config.yml --provider openai --phase review`.

**2. Carry forward: Fix scaffolds endpoint to glob YAML files (Round 1 CV-2, converged).**
Code fix to `api.py` L208. No further discussion needed.

**3. Carry forward: Add `decide` 4-mode clarifying note to cli.md (Round 1 CV-1, converged).**
Docs fix. No further discussion needed.

### P2 -- Should implement

**4. Document the three-way provider default mismatch.**
The config file defaults `provider` to `"anthropic"` (`engine/config.py` L77). The CLI defaults to `"mock"` (`engine/cli/__init__.py` L101). The SDK defaults to `"mock"` (`engine/sdk.py` L155). This means a config file without `provider:` uses `anthropic`, but running it with `conversus run` without `--provider` uses `mock`. The Round 1 convergence item (CV-3) addresses part of this with a cli.md note, but the config-reference.md should also clarify: "When `provider` is omitted from the config, it defaults to `anthropic`. However, the CLI `--provider` flag has its own default (`mock`) that takes full precedence."
- **Source**: `engine/config.py` L77, `engine/cli/__init__.py` L101, `engine/sdk.py` L155.
- **Round 1 context**: Extends the converged CV-3 recommendation. Not a reversal -- this is a specific documentation text refinement.

**5. Carry forward: Add `plugins:` key to config-reference.md (Round 1 CV-B, converged).**
No further discussion needed.

**6. Carry forward: Add narrative prose and `members:` list to API reference pages (Round 1 CV-A, converged).**
The `domains/base.md` `members:` list should include at minimum: `DomainPlugin`, `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, `Scaffold`, `VariableExtractor`, `load_scaffold`. Also add `DomainStore`, `JSONLStore`, `SQLiteStore` from `conversus.domains.store`.

**7. Add `Deliberation.cost_estimate` nullability note to SDK docs.**
The SDK docs at `sdk.md` L70 show `d.cost_estimate` without noting it can return `None`. The property at `engine/sdk.py` L182-205 explicitly returns `dict[str, int] | None`. Add a note: "Returns `None` if the config cannot be parsed."
- **Source**: `engine/sdk.py` L182-205, `sdk.md` L70-73.
- **Round 1 context**: New finding in Round 2.

**8. Carry forward: Document `estimate_cost_usd()` in SDK guide (Round 1 CV-7, converged).**
No further discussion needed.

**9. Document what `--phase review` actually produces.**
The `cli.md` docs list `--phase` as supporting `all` and `review` without explaining that `review` runs Phase 1 only (agent reviews, no cross-review/revision/disputes/synthesis). The `run_engine()` function at `engine/run.py` L248-256 confirms this branches to `run_phase1()`. Users need to know what output files to expect from a partial run.
- **Source**: `engine/run.py` L248-256, `cli.md` L30.
- **Round 1 context**: This elaborates on the unchallenged Round 1 CV-9 recommendation. Not a reversal -- this adds specificity about what the user should expect.

### P3 -- Consider implementing

**10. Note `construct_objective` failure modes in SDK docs.**
The SDK docs at `sdk.md` L148-157 show a clean happy path for `construct_objective()`. In practice, `NonInteractiveGapFiller` (the default filler) raises `RuntimeError` on parameters without defaults (`construction.py` L167-171). The `classify_decision_type` function raises `ValueError` if no keyword patterns match (`construction.py` L417-421). The docs should add a brief note about common exceptions.
- **Source**: `construction.py` L167-171, L417-421, `sdk.md` L148-157.
- **Round 1 context**: New finding in Round 2.

## Referenced Documentation

### Target files reviewed
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/quickstart.md`
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/cli.md`
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/modes.md`
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/sdk.md`
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/config-reference.md`
- `<HOME>/code/payer-index-mono/conversus/docs/developer-guide/architecture.md`
- `<HOME>/code/payer-index-mono/conversus/docs/developer-guide/building-plugins.md`
- `<HOME>/code/payer-index-mono/conversus/docs/developer-guide/building-domains.md`
- `<HOME>/code/payer-index-mono/conversus/docs/api/schemas/construction.md`
- `<HOME>/code/payer-index-mono/conversus/docs/api/plugins/base.md`
- `<HOME>/code/payer-index-mono/conversus/docs/api/domains/base.md`

### Source files verified
- `<HOME>/code/payer-index-mono/conversus/conversus/plugins/base.py` -- Plugin ABC, HookPoint, DeliberationState, PluginResult, load_plugins, execute_hooks, topological sort
- `<HOME>/code/payer-index-mono/conversus/conversus/schemas/construction.py` -- Construction pipeline, DecisionType, AssembledObjective, GapFiller, TemplateSelector, construct_objective
- `<HOME>/code/payer-index-mono/conversus/conversus/schemas/modes.py` -- VALID_MODES canonical source (8 modes confirmed)
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/base.py` -- DomainPlugin ABC, DomainContext, DomainScore, DomainRecord, Scaffold, VariableExtractor, scoring pipeline
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/store.py` -- DomainStore protocol, JSONLStore, SQLiteStore
- `<HOME>/code/payer-index-mono/conversus/conversus/domains/api.py` -- create_domain_router, scaffolds endpoint (YAML bug confirmed at L208)
- `<HOME>/code/payer-index-mono/conversus/engine/config.py` -- parse_config, EngineConfig, AgentConfig, ArbiterConfig, VALID_MODES, AGENT_NAME_RE
- `<HOME>/code/payer-index-mono/conversus/engine/cli/__init__.py` -- CLI group, run, decide, validate, login, logout, status commands
- `<HOME>/code/payer-index-mono/conversus/engine/sdk.py` -- Deliberation, Result, ValidateResult, validate, classify
- `<HOME>/code/payer-index-mono/conversus/engine/events.py` -- PhaseStarted, AgentDispatched, AgentCompleted, PhaseCompleted, CallbackEmitter, NullEmitter, AsyncQueueEmitter
- `<HOME>/code/payer-index-mono/conversus/engine/cost.py` -- estimate_cost, estimate_cost_usd, MODEL_PRICING, PROVIDER_DEFAULT_MODELS
- `<HOME>/code/payer-index-mono/conversus/engine/run.py` -- run_engine, run_phase1
- `<HOME>/code/payer-index-mono/conversus/engine/__init__.py` -- Public exports (Deliberation, Result, validate; classify NOT exported)

### Prior round context
- `<HOME>/code/payer-index-mono/conversus/specs/031-docs-and-vercel-compliance/conversus-review/round-1/summary/final.md`
