# Code Verifier — Revision (Iteration 1)

---

### Recommendation Dispositions

#### Recommendation 1: Document decide mode restriction

- **Original position**: The `decide` command's `--mode` flag only accepts 4 modes in the Click definition, not all 8. The docs should either explicitly state the restriction or the code should be updated.
- **Disposition**: Surviving
- **Explanation**: Both cross-reviews engaged with this recommendation and converged on the same resolution. user-advocate's cross-review called this a "dangerous contradiction" because their Recommendation #10 (list all 8 mode names in cli.md) would conflict with my recommendation to document the 4-mode subset. developer-advocate's cross-review agreed this is a real issue but argued cli.md is "already technically correct" by listing 4 modes, reframing it as a usability gap rather than a documentation error. I accept developer-advocate's reframing on severity -- the docs do not claim `decide` accepts all 8 -- but the recommendation survives because the juxtaposition between modes.md (8 modes prominent) and cli.md (4 modes without explanation) creates a foreseeable user failure. The agreed resolution across all three reviews is a one-line note in cli.md: "For the remaining 4 modes, use `conversus run` with a config file." This is the documentation-only fix both cross-reviews endorse.

#### Recommendation 2: Fix scaffolds endpoint to match documentation

- **Original position**: The `/scaffolds` API endpoint at `api.py` L208 only globs `*.json`, but the docs show YAML scaffolds. Either fix the code or fix the docs.
- **Disposition**: Modified
- **Explanation**: developer-advocate's cross-review correctly identified that my original framing -- presenting "fix the code" and "fix the docs" as equally valid -- was irresponsible. The building-domains guide shows scaffold examples exclusively in YAML, `load_scaffold()` already handles both YAML and JSON, and the `DomainPlugin` ABC documentation says `scaffold_dir` contains "scaffold YAML/JSON files." developer-advocate concluded: "The documentation is correct; the code is the outlier." I agree. The modified recommendation is: fix `api.py` L208 to glob `("*.yml", "*.yaml", "*.json")`. Updating the docs to say "JSON only" would contradict every scaffold example in the developer guide. This is a code fix, not a docs fix.

#### Recommendation 3: Clarify provider precedence between config and CLI

- **Original position**: The CLI `--provider` defaults to `mock`, `EngineConfig.provider` defaults to `anthropic`, and the docs do not make the precedence clear.
- **Disposition**: Modified
- **Explanation**: developer-advocate's cross-review pointed out that `config-reference.md` L60 already says "CLI --provider flag overrides this." I re-verified this and it is correct -- the config reference does document the override relationship. My original framing overstated the gap by saying "no doc explains which wins." What is actually missing is simpler: cli.md's `run` command options table does not mention that the `--provider` default of `mock` will override a config file's `provider: anthropic` setting. The user-advocate cross-review agreed the precedence finding is real but suggested implementing it as a cross-reference rather than duplicating the rule. The modified recommendation: add a brief note under the `run` command in cli.md: "When `--provider` is not specified, the CLI defaults to `mock`, overriding the config file's `provider` field. See [Config Reference](config-reference.md) for details." This is a smaller fix than I originally proposed, targeted at the one page where the information is actually missing.

#### Recommendation 4: Export classify from engine __init__

- **Original position**: `classify` is available via `from engine.sdk import classify` but not re-exported from `engine/__init__.py`, creating an inconsistency with the import pattern shown elsewhere.
- **Disposition**: Modified
- **Explanation**: developer-advocate's cross-review offered an alternative framing: rather than fixing the code to add the re-export, document the dual-namespace architecture (`engine.*` vs `conversus.*`) explicitly in the SDK page. developer-advocate noted these are "not contradictory, but if only the code change is made, the broader confusion about dual namespaces remains." I accept that both are needed. The modified recommendation is two-part: (1) add `classify` to `engine/__init__.py` exports (a one-line code change that prevents ImportError for users following the `from engine import ...` pattern), and (2) add a brief note to the SDK guide explaining the two import namespaces. The code change alone is insufficient without the documentation context, and the documentation alone is insufficient without the code fix.

#### Recommendation 5: Document DomainStore in API reference

- **Original position**: The API reference for domains does not include `DomainStore`, `JSONLStore`, or `SQLiteStore` from `conversus/domains/store.py`.
- **Disposition**: Surviving
- **Explanation**: Both user-advocate and developer-advocate cross-reviews agreed with this finding, though from different angles. user-advocate connected it to the broader problem of API reference pages being "effectively blank" on GitHub. developer-advocate recommended narrative documentation before autodoc directives. Neither challenged the core claim that the store classes are missing. The recommendation survives as stated, with the addendum (from the cross-reviews) that when the store page is added, it should include narrative prose above the autodoc directive so it is readable on GitHub without a built MkDocs site.

#### Recommendation 6: Add provider default model table

- **Original position**: cli.md says `--model` default is "provider default" without specifying what those defaults are (`claude-sonnet-4-20250514` for anthropic, `gpt-4o` for openai).
- **Disposition**: Surviving
- **Explanation**: Neither cross-review challenged this recommendation. Both focused on higher-priority items. The recommendation is low-effort (a 2-row table) and prevents users from needing to read source code to predict cost or model capability. It survives unchanged.

#### Recommendation 7: Document estimate_cost_usd in SDK guide

- **Original position**: The `estimate_cost_usd()` function in `engine/cost.py` exists and is fully implemented but not documented anywhere.
- **Disposition**: Surviving
- **Explanation**: developer-advocate's cross-review explicitly agreed: "Both reviews converge on the position that USD cost estimation is a valuable undocumented capability that production users need." user-advocate's cross-review noted this as additive to the already-strong cost documentation section. No challenge to the recommendation; it survives unchanged.

#### Recommendation 8: Fix determine_verdict example in building-domains

- **Original position**: The `determine_verdict` example in building-domains.md only uses `hard_blocks` and `overall`, ignoring `dimensions` and `variables`.
- **Disposition**: Modified
- **Explanation**: developer-advocate's cross-review identified a deeper problem I missed: the example does not merely ignore parameters -- it implements logic that differs from the base class's default behavior. The base class `_determine_verdict` (L355-375) checks per-dimension thresholds, not `minimum_overall`. The documented example checks `overall < thresholds.get("minimum_overall", 0.7)`, which is a custom override pattern, not the default. developer-advocate recommended splitting the section into "Default behavior" vs. "Customizing verdict logic" (their Recommendation #7). user-advocate's cross-review noted the tension between "teaching simplicity" and "contract completeness" and proposed keeping the current example with a second advanced example below it. I accept developer-advocate's structural fix as the right framework. The modified recommendation: (1) add a "Default behavior" paragraph explaining the base class logic (hard blocks -> block, per-dimension thresholds -> revise, otherwise -> pass), (2) relabel the existing example as "Customizing verdict logic," and (3) within that custom example, add a comment noting `dimensions` and `variables` are available for domain-specific logic. This addresses both developer-advocate's "misleading" concern and my original "incomplete" concern.

#### Recommendation 9: Add phase parameter documentation for run command

- **Original position**: cli.md documents `--phase` with choices `all` or `review` but does not note that additional phases are planned.
- **Disposition**: Surviving
- **Explanation**: Neither cross-review engaged with this recommendation. It is low-priority (P3) and low-effort. The recommendation survives unchanged: add "Currently, `--phase` supports `all` (default) and `review`. Additional phase options are planned." to cli.md.

### New Recommendations

#### New Recommendation A: Add narrative prose to API reference pages

- **Source**: Convergence between user-advocate's cross-review (API pages are "effectively blank" on GitHub) and developer-advocate's cross-review (autodoc stubs provide "no narrative context, no usage examples").
- **Proposed change**: Add 3-5 sentences of introductory prose above each `:::` directive in `docs/api/schemas/construction.md`, `docs/api/plugins/base.md`, and `docs/api/domains/base.md`. The prose should explain what the module provides, the key classes, and their relationships. This is additive -- it does not break mkdocstrings rendering and fixes the GitHub readability gap.
- **Priority**: P2
- **Rationale**: My original review treated the autodoc directives as sufficient because they will render in MkDocs. Both cross-reviews correctly identified that the raw-Markdown reading experience (GitHub, IDE preview) is a primary consumption path for open-source projects. I missed this because I was focused on code-documentation parity, not on how the docs are consumed.

#### New Recommendation B: Add plugins key to config-reference.md

- **Source**: developer-advocate's cross-review (Recommendation #3, P1) and their Phase 1 review, which flagged the missing `plugins:` key from the config reference page.
- **Proposed change**: Add a `plugins:` section to `config-reference.md` documenting the schema (`name`, `package`, `config`), the fallback behaviors (missing `package` logs warning and skips, missing `config` defaults to `{}`), and the fact that failed plugin instantiation is non-fatal.
- **Priority**: P2
- **Rationale**: My original review verified the plugin config syntax against `load_plugins()` at `base.py` L229-295 but did not flag the absence of `plugins:` from the config reference page. developer-advocate correctly identified that the config reference is meant to be the single source of truth for the YAML schema, and omitting `plugins:` means developers will not discover plugin configuration exists when reading it. I verified the code: `load_plugins()` at L251-254 reads `name`, `package`, and `config` keys, defaulting `config` to `{}`. This should be documented in the config reference.

#### New Recommendation C: Document hard block function dispatch differences

- **Source**: developer-advocate's Phase 1 review (Off-Base Assumptions, item 2) and my cross-review of developer-advocate.
- **Proposed change**: Add a brief note to the architecture or API reference page that the internal `_check_hard_blocks` function (used by standalone scoring pure functions) only supports the three-part comparison form (`variable operator threshold`), while the `DomainPlugin.evaluate_hard_blocks()` method supports all three forms (bare truthy, comparison, boolean equality) via `_evaluate_hard_block_rules` -> `_evaluate_single_hard_block`. This prevents accidental misuse if someone imports the internal helper directly.
- **Priority**: P3
- **Rationale**: developer-advocate identified two separate hard block evaluation functions with different capabilities. The public `DomainPlugin` path is correct, but `_check_hard_blocks` at L302-352 silently rejects bare truthy checks like `secrets_exposed` (logging "Invalid hard block condition" and skipping). My original review did not trace this internal function dispatch at all. While the underscore prefix discourages direct use, the function is module-level and importable, making it a latent correctness trap.

### Position Summary

My original review focused narrowly on code-documentation parity -- verifying every claim, signature, and enumeration in the docs against the actual source code. This produced accurate findings but left blind spots that the cross-reviews correctly identified. The most significant adjustment is to Recommendation #2 (scaffolds endpoint): developer-advocate was right that framing "fix the code" and "fix the docs" as equally valid was misleading when every scaffold example in the docs uses YAML. The code is the outlier; the docs are correct. I should have been more decisive in my original recommendation.

The cross-reviews also exposed that my strict scoping -- evaluating only code-documentation parity within the target file list -- caused me to miss two categories of issues. First, the GitHub reading experience for API reference pages: my review treated mkdocstrings directives as adequate because they render in MkDocs, but both user-advocate and developer-advocate identified that raw-Markdown consumption on GitHub is a primary path. Second, the missing `plugins:` key in config-reference.md: I verified plugin config syntax against the code but did not notice the config reference page omits this entire schema section. Both are now incorporated as new recommendations.

On the items that survived, I remain confident. The `decide` 4-mode restriction needs a one-line clarifying note (all three reviews converge on this). The provider precedence confusion is real, though I now acknowledge it is smaller than I originally framed -- config-reference.md already documents the override, so only cli.md needs the note. The `determine_verdict` example issue is more nuanced than I originally stated: developer-advocate correctly identified that the example does not just omit parameters but teaches logic that differs from the base class default, so the fix should be structural (split into default vs. custom sections), not just parametric (add more parameter usage to the existing example). The DomainStore, cost estimation, default model table, and phase documentation recommendations stand unchallenged.
