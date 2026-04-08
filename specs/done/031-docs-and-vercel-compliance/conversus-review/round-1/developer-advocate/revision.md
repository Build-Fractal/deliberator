# Developer Advocate — Revised Position (Iteration 1)

**Reviewer role:** developer-advocate
**Revision date:** 2026-04-02
**Original review:** `developer-advocate/review.md`

---

## Recommendation Dispositions

#### Recommendation 1: Add end-to-end domain tutorial

- **Original position**: The building-domains guide stops at class definition and never shows how to run a domain plugin end-to-end (extract, score, persist, gate, serve). Add a complete walkthrough.
- **Disposition**: Surviving
- **Explanation**: The user-advocate cross-review acknowledges this is a legitimate gap but argues it should be sequenced after onboarding fixes (user-advocate cross-review, "Priority inversion on who the docs serve first"). The code-verifier cross-review does not challenge the recommendation itself but notes that any tutorial must be verified against actual method signatures -- `score()` accepts `variables: dict[str, Any]` and `scaffold: str | Scaffold`, and `create_record()` has optional `equilibrium_score` and `convergence` parameters (code-verifier cross-review, "End-to-end domain tutorial vs. code accuracy"). Both challenges are about implementation quality and sequencing, not about whether the tutorial is needed. The recommendation survives. I accept code-verifier's constraint that the tutorial must use the string-based scaffold name pattern and mention `create_record()`'s optional parameters, and I accept user-advocate's framing that this belongs to an "extensibility track" that runs in parallel with an "onboarding track" -- but it remains P1 for the developer audience.

#### Recommendation 2: Document plugin wiring and discoverability

- **Original position**: The building-plugins guide does not explain how to make a plugin importable (the `package` field is a Python dotted import path, the module must be on `sys.path`, etc.).
- **Disposition**: Surviving
- **Explanation**: The code-verifier cross-review confirms the factual basis -- `load_plugins()` uses `importlib.import_module(package)` at L251-254, missing `package` logs a warning and skips, and failed instantiation also logs a warning and skips (code-verifier cross-review, "Plugin wiring vs. config reference completeness"). Code-verifier enriches the recommendation by noting that the fallback behaviors (missing `package` -> skip, missing `config` -> `{}`, failed instantiation -> skip with warning) should also be documented. I accept this enrichment. The user-advocate cross-review does not challenge this recommendation. It survives unchanged in substance, enhanced with code-verifier's fallback behavior details.

#### Recommendation 3: Add `plugins:` key to config reference

- **Original position**: The config-reference page documents all top-level keys but omits `plugins:`, which should be added as a dedicated section.
- **Disposition**: Modified
- **Explanation**: The user-advocate cross-review raises a valid concern: adding `plugins:` to the config reference without clear labeling could intimidate new users who see it in the "full schema" section and assume they need to configure plugins (user-advocate cross-review, "Where plugin config documentation belongs"). The recommendation is modified to: add the `plugins:` key to the config reference, but place it in a clearly labeled "Advanced / Extensibility" subsection below the core fields, with an explicit note that plugins are optional and not needed for standard deliberations. If a minimal starter template is added (per user-advocate's recommendation), it should explicitly exclude `plugins:`. This coordination ensures the config reference is factually complete without raising the intimidation floor for new users.

#### Recommendation 4: Replace API reference stubs with narrative documentation

- **Original position**: Add 3-5 sentences of narrative context before each mkdocstrings directive, plus "See also" links to developer guide pages.
- **Disposition**: Modified
- **Explanation**: Both cross-reviews converge on the same diagnosis (the pages are useless in raw Markdown form) but diverge on implementation. The user-advocate wants standalone comprehensibility for GitHub readers (user-advocate cross-review, "API reference stubs: narrative prose vs. autodoc enhancement"). The code-verifier wants expanded autodoc coverage, specifically adding `DomainStore`, `JSONLStore`, and `SQLiteStore` to `api/domains/base.md` (code-verifier cross-review, "API reference stubs: narrative docs vs. autodoc directives"). Code-verifier proposes the correct sequencing: (1) add missing autodoc members, then (2) write narrative sections that reference all members. I adopt the user-advocate's suggestion for layered prose: open with one plain-English sentence saying what the module is for (serves newcomers), then list key classes with one-line descriptions and relationships (serves developers), then link to the relevant developer guide page (serves both). The modified recommendation combines all three perspectives into a single coordinated fix.

#### Recommendation 5: Add error handling guidance for plugin and domain authors

- **Original position**: Document that exceptions in `execute()`/`extract()` are caught, logged, and skipped, and recommend returning empty/default data rather than raising.
- **Disposition**: Surviving
- **Explanation**: The code-verifier cross-review lists this as a "Safe Agreement" and confirms the exception handling behavior at `base.py` L519-525 (plugins) and L700-708 (domains) (code-verifier cross-review, "Error handling documentation is missing and needed"). The user-advocate cross-review acknowledges this is a real gap that their review missed due to scope ("error handling in plugin development is outside the new-user scope") and does not challenge the recommendation itself (user-advocate cross-review, "Error handling documentation: who needs it and why"). The recommendation survives.

#### Recommendation 6: Add testing examples for plugins and domains

- **Original position**: Add a "Testing your plugin" section with minimal `DeliberationState` construction, `execute()` assertion, and equivalent for domains.
- **Disposition**: Surviving
- **Explanation**: The user-advocate cross-review acknowledges this as "a legitimate gap that my review's scope excluded" and notes the tension is only about prioritization, not existence (user-advocate cross-review, "Testing guidance for plugins and domains"). The code-verifier cross-review does not challenge this recommendation. It survives.

#### Recommendation 7: Fix `determine_verdict` documentation to match base class default

- **Original position**: Separate the `determine_verdict` example into "Default behavior" (base class checks hard blocks then per-dimension thresholds) and "Customizing verdict logic" (the `minimum_overall` pattern as an explicit override).
- **Disposition**: Modified
- **Explanation**: The code-verifier cross-review identifies the same defect but proposes a complementary fix: the override example should demonstrate the `dimensions` and `variables` parameters that the current example ignores (code-verifier cross-review, "`determine_verdict` documentation: misleading example vs. incomplete contract"). Code-verifier proposes a coordination: adopt my structural recommendation (split into two subsections) as the framework, then within the "Customizing verdict logic" subsection, ensure the override example uses at least `dimensions` or `variables` to show the method's full contract. I accept this enrichment. The modified recommendation is: (a) add a "Default behavior" subsection explaining that the base class checks hard blocks then per-dimension thresholds (not `minimum_overall`), and (b) revise the "Customizing verdict logic" example to demonstrate both the `minimum_overall` override pattern AND usage of the `dimensions` parameter, so developers see the full method contract.

#### Recommendation 8: Document domain-engine integration in architecture page

- **Original position**: Add a "Domain integration" subsection to the architecture page explaining how domains relate to the engine pipeline (invoked separately, consume deliberation output, `equilibrium_score` as the bridge).
- **Disposition**: Surviving
- **Explanation**: The user-advocate cross-review agrees that "the three-layer diagram in architecture.md mentions domains without explaining how data flows between the engine and domain layers" and notes this gap "would confuse any user who reads the architecture page expecting a complete picture of the system" (user-advocate cross-review, "Safe Agreements"). Neither cross-review challenges the recommendation. It survives.

#### Recommendation 9: Add import path examples that match actual package structure

- **Original position**: Document the dual package structure (`engine.*` for deliberation engine, `conversus.*` for schemas/plugins/domains) explicitly in the SDK page.
- **Disposition**: Modified
- **Explanation**: The code-verifier cross-review proposes a complementary code fix: add `classify` to `engine/__init__.py` exports so `from engine import classify` works alongside `from engine.sdk import classify` (code-verifier cross-review, "`classify` re-export: consistency fix vs. dual-namespace documentation"). Code-verifier correctly notes that the code fix alone does not resolve the broader dual-namespace confusion, and documentation alone does not fix the import inconsistency. I accept that both should be applied. The modified recommendation is: (a) add the documentation note about dual namespaces as originally proposed, AND (b) recommend the `classify` re-export as a code change to reduce the inconsistency surface area. The documentation note should reference the re-export once it exists.

#### Recommendation 10: Add `conversus status` to the quickstart flow

- **Original position**: After the "Try with a real provider" section, add `conversus status` to verify credentials are configured.
- **Disposition**: Surviving
- **Explanation**: Neither cross-review challenges this recommendation. The user-advocate's quickstart-focused recommendations (prerequisites, troubleshooting) are complementary additions that would appear in different sections of the page. The code-verifier's provider precedence finding (CLI `--provider` defaults to `mock`, overriding config `provider: anthropic`) is an additional point that could be addressed with a note near `conversus status`, but does not invalidate the recommendation itself. It survives.

---

## New Recommendations

#### New Recommendation A: Acknowledge the scaffolds endpoint YAML/JSON mismatch

- **Source**: Code-verifier cross-review, "Scaffolds endpoint: YAML vs. JSON file listing."
- **Issue**: My original review praised the scaffold YAML format as "well-documented with a concrete example" (Alignment, item 4) without realizing the `/scaffolds` API endpoint (`api.py` L208) only globs `*.json` files. Every scaffold example in the building-domains guide uses YAML. A developer following the docs would create YAML scaffolds, mount the API router, call `/scaffolds`, and get an empty list.
- **Recommendation**: Fix the code to glob `*.yml`, `*.yaml`, and `*.json` in the `/scaffolds` endpoint. The documentation is correct and YAML-first; the code is the outlier. `load_scaffold()` already handles both formats. If the code fix is deferred, add a warning to the building-domains guide stating that the API listing endpoint currently only discovers JSON scaffolds. This is the single most impactful finding I missed in my original review.

#### New Recommendation B: Add provider precedence clarification to CLI docs

- **Source**: Code-verifier cross-review, "Provider precedence documentation."
- **Issue**: My original review praised the provider documentation without noting that the CLI `--provider` flag defaults to `mock` while the config `provider` field defaults to `anthropic`, and the docs do not explain which wins when neither is explicitly specified. The config reference at L60 says "CLI --provider flag overrides this," but the interaction when neither is explicitly set is not stated.
- **Recommendation**: Add a one-line note to the `run` command docs in `cli.md`: "The `--provider` CLI flag overrides the `provider` field in the config file. When neither is explicitly specified, the CLI defaults to `mock`." Frame this as a cross-reference to the config reference rather than duplicating the precedence rule.

#### New Recommendation C: Note the `decide` command's 4-mode restriction in `cli.md`

- **Source**: Both user-advocate (Recommendation #10, Off-Base Assumptions) and code-verifier (Recommendation 1, P1) cross-reviews.
- **Issue**: My original review did not flag the discrepancy between `modes.md` (8 modes) and the `decide` command's `--mode` flag (4 modes). The `cli.md` page already correctly lists only 4 modes for `decide`, so it is not factually wrong, but the juxtaposition with `modes.md` creates a reasonable expectation mismatch. User-advocate additionally identifies that `index.md` claims "4 competition modes," which contradicts `modes.md`.
- **Recommendation**: Add a brief note to `cli.md` under the `decide` command: "For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file." This is a documentation-only fix that resolves the expectation mismatch without requiring code changes.

---

## Position Summary

My original review correctly identified the developer-facing documentation's most significant gaps: the missing end-to-end domain tutorial, the undocumented plugin wiring mechanism, the absent `plugins:` config key, and the misleading `determine_verdict` example. These recommendations all survive cross-review scrutiny, though several are enriched by code-verifier's source-level verification (the `create_record()` optional parameters, the `load_plugins()` fallback behaviors, the `determine_verdict` unused parameters).

The most significant correction to my original position comes from code-verifier's scaffolds endpoint finding. I praised the scaffold YAML documentation as a strength without realizing the API endpoint silently ignores YAML files -- a silent data loss scenario that I should have caught by tracing the full lifecycle from scaffold authoring through API serving. This is now my New Recommendation A and represents a genuine blind spot in my original review: I evaluated documentation surface quality without verifying the documented behavior against all code paths.

The user-advocate cross-review's challenge about priority sequencing is well-taken but does not change my recommendation set -- it changes the implementation plan. I accept the "two tracks" framing: onboarding improvements (prerequisites, `uv` fallbacks, quickstart troubleshooting) and extensibility improvements (domain tutorial, plugin wiring, config completeness) should run in parallel, with onboarding gating the audience for extensibility docs. My P1 ratings reflect priority within the developer audience; user-advocate's P1 ratings reflect priority within the new-user audience. Both are valid and both tracks should be resourced. Where the two tracks intersect -- the `plugins:` config key, the API reference stubs, the mode count inconsistency -- the modified recommendations in this revision coordinate the approaches to avoid conflicting implementations.
