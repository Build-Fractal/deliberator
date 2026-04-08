# Code Verifier — Final Disputes and Convergence

---

### Remaining Disputes

- **Dispute: Scaffolds endpoint fix is a code change, not a documentation change**
  - **My claim**: The `/scaffolds` API endpoint at `api.py` L208 globs only `*.json`, but `load_scaffold()` supports `.yml`, `.yaml`, and `.json`, and every scaffold example in `building-domains.md` uses YAML. The fix is to change the code to glob `("*.yml", "*.yaml", "*.json")`. The documentation is correct; the code is the outlier. (Revision, Recommendation 2.)
  - **Opposing position(s)**: developer-advocate's revision (New Recommendation A) agrees the code is the outlier but hedges: "If the code fix is deferred, add a warning to the building-domains guide stating that the API listing endpoint currently only discovers JSON scaffolds." This introduces a documentation-side fallback that should not be necessary.
  - **Why I will not concede**: I verified the code paths. `load_scaffold()` at `base.py` L144-171 handles `.yml`, `.yaml`, and `.json`. The `_SCAFFOLD_EXTENSIONS` tuple at L175 defines the priority order as `(".yml", ".yaml", ".json")`. The `_resolve_scaffold_path()` function at L178-205 tries all three extensions when resolving by name. The only place that restricts to JSON is `api.py` L208: `domain.scaffold_dir.glob("*.json")`. This is a one-line code fix. A documentation warning about a known code bug is technical debt disguised as a deliverable.
  - **Counter-argument to their position**: developer-advocate's fallback framing ("if the code fix is deferred") implicitly accepts that the code fix might not ship with this documentation pass. But this is spec 031 — a docs-and-compliance spec. If the endpoint is broken relative to the documented behavior, shipping the docs without the code fix means shipping docs that describe a broken endpoint. The `/scaffolds` table in `building-domains.md` L190 promises scaffold listing; a developer who follows the guide, creates YAML scaffolds, and calls `/scaffolds` will get an empty list. The warning-in-docs fallback is worse than the fix.
  - **Proposed resolution path**: Ship the one-line code fix to `api.py` L208 in the same PR as the documentation changes. No fallback warning needed.

- **Dispute: Provider precedence is a silent override, not merely a documentation gap**
  - **My claim**: The CLI `--provider` flag defaults to `mock` at `cli/__init__.py` L101-103. `run_engine()` at `run.py` L168 also defaults `provider_name` to `"mock"`. The config file's `provider: anthropic` at `config.py` L77 is parsed but never used by the CLI path — `run_engine()` uses the `provider_name` parameter directly at L207 (`resolve_provider(provider_name)`) without consulting `config.provider`. This means a user who writes `provider: anthropic` in their config and runs `conversus run conversus.yml` (without `--provider`) will get mock responses. This is a code behavior issue that needs both a documentation note and a code-level decision about whether the config `provider` should be the fallback when the CLI flag is not explicitly set. (Revision, Recommendation 3.)
  - **Opposing position(s)**: user-advocate's revision (New Recommendation A, P2) and developer-advocate's revision (New Recommendation B) both treat this as a documentation-only fix: add a note to cli.md and config-reference.md. Neither proposes addressing the code-level question of whether `run_engine()` should fall back to `config.provider` when the CLI flag is at its default.
  - **Why I will not concede**: I traced the actual call chain. The CLI `run` command at L131-141 passes `provider` (the Click option value, always defaulting to `"mock"`) to `run_engine()` as `provider_name`. `run_engine()` at L207 calls `resolve_provider(provider_name)` without ever reading `config.provider`. The config's `provider` field is parsed and validated (L572-577) but dead on the CLI path — it is only useful if someone calls `run_engine()` programmatically and inspects the config object. Documenting "CLI `--provider` overrides config `provider`" is technically accurate but misleading: it implies a precedence relationship. In reality, the config `provider` is ignored entirely. The documentation fix should say: "The CLI always uses `--provider` (default: `mock`). The config file's `provider` field is not read by the CLI." And separately, the maintainers should decide whether to wire `config.provider` as a fallback in `run_engine()` when the CLI flag is not explicitly passed.
  - **Counter-argument to their position**: Both other agents frame this as "CLI overrides config," which implies the config value matters. It does not. A user who reads "CLI --provider flag overrides this" in config-reference.md L60 will reasonably conclude that if they do not pass `--provider`, the config value will be used. That is false. The documentation note, as proposed by the other agents, would perpetuate the misunderstanding. The note must say the config field is not consulted by the CLI, or the code must be changed to consult it.
  - **Proposed resolution path**: (1) Add a note to cli.md that reads: "The `run` command always uses the `--provider` flag value. When omitted, it defaults to `mock` regardless of the config file's `provider` field." (2) Open an issue or follow-up item to decide whether `run_engine()` should fall back to `config.provider` when the CLI flag is at its default. This separates the documentation fix (ship now) from the design decision (decide later).

- **Dispute: API reference for domains/base.md lacks member filtering**
  - **My claim**: `docs/api/domains/base.md` contains `:::  conversus.domains.base` with no `options.members` list. This means mkdocstrings will render every public symbol in the module, including internal helpers like `_check_hard_blocks`, `_compute_weighted_score`, `_determine_verdict`, `_build_recommendations`, `_evaluate_single_hard_block`, `_evaluate_hard_block_rules`, `_linear_slope`, `_resolve_scaffold_path`, and `_SCAFFOLD_EXTENSIONS`. By contrast, `plugins/base.md` and `schemas/construction.md` both have explicit member lists. The domains page should have an explicit member list to present a curated public API. (Revision, Recommendation 5; New Recommendation A.)
  - **Opposing position(s)**: developer-advocate's revision (Recommendation 4) proposes adding narrative prose and "See also" links but does not specifically address the missing member filter. user-advocate's revision (Recommendation 6) proposes layered prose above the directive but similarly does not address the member list gap.
  - **Why I will not concede**: The two other API reference pages (`plugins/base.md` L5-18 and `schemas/construction.md` L5-24) both have explicit `members:` lists. `domains/base.md` has none. This is not a stylistic preference — it determines what mkdocstrings renders. Without a member filter, internal functions with underscore prefixes may render (depending on mkdocstrings config), and the page provides no signal about which symbols are part of the public API. Adding prose above a bare `:::` directive does not fix this.
  - **Counter-argument to their position**: Both agents focus on the prose/narrative gap (which I agree with — see Convergence below) but treat the member list as a detail. It is not a detail. The member list is the structural equivalent of `__all__` in a Python module — it defines the public contract. Without it, the page cannot be a reliable API reference even in MkDocs, because the rendered content depends on mkdocstrings' default filtering behavior, which may or may not exclude underscore-prefixed symbols.
  - **Proposed resolution path**: Add an explicit `members:` list to `domains/base.md` covering: `DomainPlugin`, `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, `Scaffold`, `VariableExtractor`, `load_scaffold`. Also add `DomainStore`, `JSONLStore`, `SQLiteStore` (from `store.py`) either on this page or a new `api/domains/store.md` page. This is orthogonal to and compatible with the narrative prose both agents propose.

### Convergence

- **Converged: `decide` command 4-mode restriction needs a clarifying note in cli.md**
  - **Shared position**: Add a one-line note to cli.md under the `decide` command: "For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file. See [Deliberation Modes](modes.md) for all 8." The `decide` command at `cli/__init__.py` L240-244 genuinely constrains `--mode` to 4 modes via `click.Choice`.
  - **Agreeing agents**: code-verifier (Revision, Recommendation 1), user-advocate (Revision, Recommendation 10), developer-advocate (Revision, New Recommendation C)
  - **Strength**: Unanimous
  - **Path to convergence**: code-verifier identified the factual discrepancy in Phase 1. user-advocate initially proposed listing all 8 modes in cli.md (Recommendation 10), which would have been incorrect. Cross-review corrected this. All three agents converged on the same one-line note by Phase 3.

- **Converged: `plugins:` key must be added to config-reference.md**
  - **Shared position**: Add a `plugins:` section to config-reference.md documenting the `name`, `package`, and `config` sub-keys. The config reference claims to be the single source of truth for the YAML schema but omits this top-level key. Code evidence: `load_plugins()` at `base.py` L251-254 reads `name`, `package`, and `config` (defaulting `config` to `{}`).
  - **Agreeing agents**: code-verifier (Revision, New Recommendation B), user-advocate (Revision, New Recommendation B), developer-advocate (Revision, Recommendation 3)
  - **Strength**: Unanimous
  - **Path to convergence**: developer-advocate identified the gap in Phase 1 (Recommendation 3, P1). code-verifier and user-advocate both adopted it as new recommendations in Phase 3 after cross-review. developer-advocate's modification (place in an "Advanced / Extensibility" subsection) is agreed by all.

- **Converged: API reference pages need narrative prose above autodoc directives**
  - **Shared position**: Add 3-5 sentences of introductory prose above each `:::` directive in the API reference pages. The prose should open with a one-sentence summary, list key classes with one-line descriptions, and link to the relevant developer guide page. This ensures the pages are useful in raw Markdown (GitHub, IDE preview) and not only in rendered MkDocs.
  - **Agreeing agents**: code-verifier (Revision, New Recommendation A), user-advocate (Revision, Recommendation 6), developer-advocate (Revision, Recommendation 4)
  - **Strength**: Unanimous
  - **Path to convergence**: user-advocate identified the GitHub readability gap in Phase 1. developer-advocate proposed the layered prose structure. code-verifier adopted both during Phase 3 revision. All three agents now agree on the layered approach (accessible sentence, then structural detail, then cross-links).

- **Converged: `determine_verdict` example in building-domains.md is misleading**
  - **Shared position**: Split the `determine_verdict` section into "Default behavior" (base class checks hard blocks then per-dimension thresholds via `_determine_verdict` at `base.py` L355-375) and "Customizing verdict logic" (the `minimum_overall` pattern as an explicit override). The current example at `building-domains.md` L126-132 checks `overall < thresholds.get("minimum_overall", 0.7)`, which is a custom override, not the default behavior. The base class default ignores `overall` entirely and checks per-dimension thresholds.
  - **Agreeing agents**: code-verifier (Revision, Recommendation 8), developer-advocate (Revision, Recommendation 7)
  - **Strength**: Bilateral
  - **Path to convergence**: code-verifier identified the incomplete parameter usage in Phase 1. developer-advocate identified the deeper problem (example teaches different logic than the base class) in Phase 1. Cross-review aligned both on the structural fix (split into two subsections). user-advocate did not engage with this issue (outside new-user scope).

- **Converged: `estimate_cost_usd` should be documented in the SDK guide**
  - **Shared position**: Add a brief section to the SDK guide documenting `estimate_cost_usd()` from `engine/cost.py`. The function exists (L106-158), is fully implemented with provider-specific pricing and range estimates, but is not mentioned anywhere in the documentation. It is useful for production users who need to predict API spend before running deliberations.
  - **Agreeing agents**: code-verifier (Revision, Recommendation 7), developer-advocate (Phase 1 agreement)
  - **Strength**: Bilateral
  - **Path to convergence**: Agreed from Phase 1. Neither cross-review challenged it.

### Final Position Statement

**Non-Negotiables** (3 items):

1. **The scaffolds endpoint must glob YAML files, not just JSON.** `api.py` L208 globs `*.json` only. `load_scaffold()` handles `.yml`, `.yaml`, `.json`. Every scaffold example in the docs uses YAML. This is a code bug, not a documentation gap. A documentation warning is not an acceptable substitute for a one-line fix. The fix is: change `domain.scaffold_dir.glob("*.json")` to iterate over `("*.yml", "*.yaml", "*.json")`.

2. **The `domains/base.md` API reference page must have an explicit `members:` list.** The other two API reference pages have them. Without one, the page either renders internal helpers as public API or relies on mkdocstrings' default filtering, which is not documented in the conversus project. This must also include `DomainStore`, `JSONLStore`, and `SQLiteStore` from `store.py`.

3. **The provider precedence documentation must accurately describe the code behavior.** The config file's `provider` field is not consulted by the CLI `run` command. `run_engine()` uses the `provider_name` parameter from the CLI flag, which defaults to `"mock"`. Saying "CLI --provider flag overrides this" in config-reference.md is misleading because it implies the config value is a fallback. The documentation must state that the CLI does not read the config's `provider` field, or the code must be changed to use it as a fallback.

**Flexibility** (3 items):

1. **Narrative prose structure for API reference pages.** I agree prose is needed above autodoc directives. I am flexible on the exact layering (one-sentence summary vs. full class listing vs. relationship diagram). The user-advocate's and developer-advocate's proposed structures are both acceptable.

2. **Priority ordering between onboarding and extensibility tracks.** user-advocate argues onboarding fixes gate the audience for extensibility docs. developer-advocate argues the developer audience has independent P1 needs. I am agnostic on sequencing — my role is code-documentation parity, not implementation planning. Both tracks have verified factual gaps that need fixing.

3. **Whether `classify` should be re-exported from `engine/__init__.py`.** My revision proposed adding the re-export (Recommendation 4). developer-advocate proposed documenting the dual namespace instead. Either approach resolves the inconsistency. I am flexible on which ships first, as long as one of them does.
