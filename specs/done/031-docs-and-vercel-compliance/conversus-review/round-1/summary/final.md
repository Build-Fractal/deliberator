# Neutral Synthesis -- Conversus Documentation Suite (Spec 031)

---

## Process Summary

- **Agents**: 3 -- code-verifier, user-advocate, developer-advocate
- **Total artifacts**: 18 (3 reviews + 6 cross-reviews + 3 revisions + 3 disputes + 3 target specification clusters = 18 deliberation artifacts; 11 target documentation files reviewed)
- **Phase 1 reviews**: 3
- **Phase 2 cross-reviews**: 6
- **Phase 3 revisions**: 3
- **Phase 4 disputes**: 3
- **Recommendations proposed** (Phase 1 total): 29 (code-verifier: 9, user-advocate: 10, developer-advocate: 10)
- **Recommendations withdrawn** (Phase 3): 0
- **Recommendations modified** (Phase 3): 13 (code-verifier: 4, user-advocate: 7, developer-advocate: 4; some overlap where modifications absorbed cross-agent findings)
- **Recommendations surviving** (Phase 3): 16 (code-verifier: 5 surviving + 3 new, user-advocate: 3 surviving + 2 new, developer-advocate: 6 surviving + 3 new; total including new = 28 after deduplication)
- **New recommendations added** (Phase 3): 8 (code-verifier: 3, user-advocate: 2, developer-advocate: 3)
- **Disputes remaining** (Phase 4): 9 (code-verifier: 3, user-advocate: 3, developer-advocate: 3)
- **Convergence points** (Phase 4): 12 (code-verifier: 5, user-advocate: 5, developer-advocate: 5; deduplicated to 7 unique convergence items)

---

## Recommendation Scorecard

| # | Agent | Recommendation | Phase 1 Priority | Phase 3 Disposition | Challenged By | Convergence | Final Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------|--------------|
| CV-1 | code-verifier | Document `decide` 4-mode restriction in cli.md | P1 | Surviving | user-advocate, developer-advocate (both accepted) | Unanimous | Converged -- add one-line note to cli.md |
| CV-2 | code-verifier | Fix scaffolds endpoint to glob YAML, not just JSON | P1 | Modified (code-fix-only) | developer-advocate (agreed code is outlier) | Bilateral (CV + DA) | Converged -- code fix to `api.py` L208 |
| CV-3 | code-verifier | Clarify provider precedence (CLI vs. config) | P2 | Modified (targeted note in cli.md) | developer-advocate (config-ref already has note) | Unanimous | Converged -- one-line note in cli.md with cross-ref |
| CV-4 | code-verifier | Export `classify` from `engine/__init__` | P2 | Modified (code + docs) | developer-advocate (proposed dual-namespace docs) | None | Open -- code-verifier flexible, developer-advocate prefers both |
| CV-5 | code-verifier | Document DomainStore in API reference | P2 | Surviving | None | Bilateral (CV + UA via API stubs) | Converged into API reference prose convergence |
| CV-6 | code-verifier | Add provider default model table | P2 | Surviving | None | None | Unchallenged -- survives |
| CV-7 | code-verifier | Document `estimate_cost_usd` in SDK guide | P3 | Surviving | None | Bilateral (CV + DA) | Converged -- both agree function should be documented |
| CV-8 | code-verifier | Fix `determine_verdict` example | P3 | Modified (split default/custom) | developer-advocate (deeper structural issue) | Bilateral (CV + DA) | Converged -- split into two subsections |
| CV-9 | code-verifier | Add `--phase` parameter documentation note | P3 | Surviving | None | None | Unchallenged -- survives |
| CV-A | code-verifier | Add narrative prose to API reference pages (new) | P2 | New in Phase 3 | N/A | Unanimous | Converged -- layered prose approach |
| CV-B | code-verifier | Add `plugins:` key to config-reference.md (new) | P2 | New in Phase 3 | N/A | Unanimous | Converged -- in Advanced/Extensibility subsection |
| CV-C | code-verifier | Document hard block function dispatch differences (new) | P3 | New in Phase 3 | N/A | None | Unchallenged -- survives |
| UA-1 | user-advocate | Add prerequisites section to quickstart | P1 | Modified (brief callout) | code-verifier (length concern) | None | Disputed -- user-advocate wants inline hints, code-verifier wants brevity |
| UA-2 | user-advocate | Explain slash commands before guided workflow | P1 | Surviving | None (implicitly accepted) | None | Unchallenged -- survives as P1 |
| UA-3 | user-advocate | Fix "4 modes" claim on index page | P1 | Modified (qualified "8 modes") | code-verifier (4-mode CLI constraint) | Unanimous | Converged -- "8 modes" with CLI subset qualifier |
| UA-4 | user-advocate | Put sync example first in SDK doc | P2 | Modified (prominent note + tabs) | code-verifier, developer-advocate | None | Disputed -- user-advocate insists on sync-first for raw Markdown |
| UA-5 | user-advocate | Add troubleshooting section to quickstart | P2 | Modified (link to separate page) | code-verifier (length) | None | Disputed -- user-advocate wants inline micro-hints |
| UA-6 | user-advocate | Add introductory prose to API reference stubs | P2 | Modified (layered approach) | developer-advocate (structural listings) | Unanimous | Converged -- layered prose approach |
| UA-7 | user-advocate | Add "Next steps" section to quickstart | P2 | Modified (two-track) | developer-advocate (developer path missing) | None | Unchallenged as modified -- survives |
| UA-8 | user-advocate | Add "What you will need" to guided workflow example | P3 | Surviving | None | None | Unchallenged -- survives |
| UA-9 | user-advocate | Add minimal "starter config" to config reference | P3 | Modified (coordinated with plugins:) | developer-advocate (plugins: key) | None | Unchallenged as modified -- survives |
| UA-10 | user-advocate | Cross-link CLI `decide` to modes page | P3 | Modified (keep 4 modes, add note) | code-verifier (dangerous to list all 8) | Unanimous | Converged into CV-1 |
| UA-A | user-advocate | Document provider precedence (new) | P2 | New in Phase 3 | N/A | Unanimous | Converged into CV-3 |
| UA-B | user-advocate | Add `plugins:` key to config reference (new) | P2 | New in Phase 3 | N/A | Unanimous | Converged into CV-B |
| DA-1 | developer-advocate | Add end-to-end domain tutorial | P1 | Surviving | user-advocate (sequencing) | None | Disputed -- priority sequencing |
| DA-2 | developer-advocate | Document plugin wiring and discoverability | P1 | Surviving (enriched) | None (code-verifier enriched) | None | Disputed -- belongs in building-plugins guide |
| DA-3 | developer-advocate | Add `plugins:` key to config reference | P1 | Modified (Advanced subsection) | user-advocate (intimidation risk) | Unanimous | Converged -- see CV-B |
| DA-4 | developer-advocate | Replace API reference stubs with narrative docs | P2 | Modified (layered approach) | user-advocate, code-verifier | Unanimous | Converged -- see CV-A |
| DA-5 | developer-advocate | Add error handling guidance for plugin/domain authors | P2 | Surviving | None (user-advocate acknowledged gap) | None | Unchallenged -- survives |
| DA-6 | developer-advocate | Add testing examples for plugins and domains | P2 | Surviving | None (user-advocate acknowledged gap) | None | Unchallenged -- survives |
| DA-7 | developer-advocate | Fix `determine_verdict` documentation | P2 | Modified (add parameter demo) | code-verifier (complement structural fix) | Bilateral (CV + DA) | Converged -- see CV-8 |
| DA-8 | developer-advocate | Document domain-engine integration in architecture | P2 | Surviving | None (user-advocate agreed) | None | Unchallenged -- survives |
| DA-9 | developer-advocate | Add import path examples for dual namespaces | P3 | Modified (add classify re-export too) | code-verifier (code fix) | None | Unchallenged as modified -- survives |
| DA-10 | developer-advocate | Add `conversus status` to quickstart flow | P3 | Surviving | None | None | Unchallenged -- survives |
| DA-A | developer-advocate | Fix scaffolds endpoint YAML/JSON mismatch (new) | P1 | New in Phase 3 | N/A | Bilateral (CV + DA) | Converged into CV-2 |
| DA-B | developer-advocate | Add provider precedence note to CLI docs (new) | P2 | New in Phase 3 | N/A | Unanimous | Converged into CV-3 |
| DA-C | developer-advocate | Note `decide` 4-mode restriction in cli.md (new) | P2 | New in Phase 3 | N/A | Unanimous | Converged into CV-1 |

---

## Dangerous Contradictions Found

### Resolved in process

1. **CLI `decide` mode count: listing all 8 vs. listing only 4** (code-verifier cross-review of user-advocate). user-advocate's original Recommendation #10 would have listed all 8 modes in cli.md for the `decide` command. code-verifier identified that the Click definition at `engine/cli/__init__.py` L240-244 constrains `--mode` to exactly 4 via `click.Choice`. Listing all 8 would cause users to try unsupported modes and get unhelpful errors. **Resolution**: user-advocate withdrew the "list all 8" approach in Phase 3 and converged with code-verifier on a one-line cross-reference note.

2. **Scaffolds endpoint: fix the code vs. fix the docs** (developer-advocate cross-review of code-verifier). code-verifier originally presented both "update the code to glob YAML" and "update docs to require JSON" as equally valid options. developer-advocate argued the documentation is correct (every scaffold example uses YAML, `load_scaffold()` handles both formats) and the code is the outlier. **Resolution**: code-verifier accepted this framing in Phase 3 and modified the recommendation to code-fix-only.

3. **Provider precedence: "CLI overrides config" vs. reality** (code-verifier cross-review of developer-advocate). developer-advocate's cross-review noted that config-reference.md L60 already says "CLI --provider flag overrides this" and downgraded the severity. code-verifier's Phase 4 disputes argue the situation is worse than "override" -- the config `provider` field is never consulted by the CLI `run` command at all. **Resolution**: Partial convergence on a documentation note in cli.md; code-verifier's deeper claim about dead code remains a dispute.

4. **determine_verdict example: incomplete parameters vs. misleading logic** (mutual between code-verifier and developer-advocate). code-verifier saw it as an incomplete contract (missing parameter usage). developer-advocate saw it as a misleading example (teaches non-default behavior). **Resolution**: Both converged on a structural fix: split into "Default behavior" and "Customizing verdict logic" subsections.

### Unresolved

5. **SDK async-first vs. sync-first Quick Start** (user-advocate vs. code-verifier and developer-advocate). user-advocate insists the first code block must use `asyncio.run()` so it works when pasted into a plain script. code-verifier and developer-advocate argue the SDK is architecturally async-first and reordering creates a conceptual mismatch. developer-advocate proposed tabbed code blocks (sync default-visible). user-advocate counters that tabs do not render in raw Markdown on GitHub, so the fallback must still be sync-first. See Remaining Disputes below.

---

## Systemic Contradictions

1. **Audience segmentation without explicit scoping**. The documentation suite serves at least three audiences (new users exploring conversus, developers integrating the SDK, and developers extending via plugins/domains) but does not segment pages by audience. This surfaces repeatedly: user-advocate evaluates the SDK Quick Start for script-writing newcomers while developer-advocate evaluates it for pipeline builders; user-advocate rates the building-domains guide as having "no issues" while developer-advocate identifies it as the largest gap. The root cause is that individual pages attempt to serve multiple audiences without explicit "who this page is for" framing.

2. **Doc-only fixes vs. code fixes: different change approval thresholds**. Several findings reveal code bugs exposed through documentation review (scaffolds endpoint, provider dead-code path, `classify` export). The agents repeatedly must decide whether to fix the code or caveat the docs. This tension arises because spec 031 is a "docs-and-compliance" spec, and code changes have a different review and testing burden. The process would benefit from a clear policy: when documentation accurately describes the intended behavior but the code diverges, the code is the bug and must be fixed.

3. **Raw Markdown vs. rendered MkDocs as the evaluation surface**. The API reference pages pass code-verifier's review (mkdocstrings directives point to correct modules) but fail user-advocate's and developer-advocate's reviews (blank on GitHub). This reflects an unstated assumption about how documentation is consumed. The project has no documented position on whether GitHub or MkDocs is the primary reading surface. This ambiguity will recur in every documentation review.

---

## Convergence Achieved

1. **`decide` command 4-mode restriction needs a clarifying note in cli.md** (Unanimous -- all three agents). Add: "For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file. See [Deliberation Modes](modes.md) for all 8." Source: code-verifier Revision Rec 1, user-advocate Revision Rec 10, developer-advocate Revision New Rec C.

2. **Scaffolds endpoint must glob YAML files, not just JSON** (Bilateral -- code-verifier, developer-advocate). Fix `api.py` L208 to glob `("*.yml", "*.yaml", "*.json")`. The documentation is YAML-first; `load_scaffold()` handles both; the endpoint is the sole outlier. Source: code-verifier Revision Rec 2, developer-advocate Revision New Rec A.

3. **`plugins:` key must be added to config-reference.md** (Unanimous -- all three agents). Add a `plugins:` section documenting `name`, `package`, `config` sub-keys with fallback behaviors. Place in an "Advanced / Extensibility" subsection. Source: developer-advocate Revision Rec 3, code-verifier Revision New Rec B, user-advocate Revision New Rec B.

4. **API reference pages need narrative prose above autodoc directives** (Unanimous -- all three agents). Add layered prose: one accessible sentence (what the module is for), key class listing with relationships, cross-link to developer guide. Also fix `domains/base.md` member filter and add DomainStore/JSONLStore/SQLiteStore. Source: code-verifier Revision New Rec A, user-advocate Revision Rec 6, developer-advocate Revision Rec 4.

5. **`determine_verdict` example must be split into default behavior and custom override** (Bilateral -- code-verifier, developer-advocate). The current example at building-domains.md L126-132 teaches a `minimum_overall` check that is not the base class default (which checks per-dimension thresholds). Split into two subsections and show `dimensions`/`variables` parameters in the custom override. Source: code-verifier Revision Rec 8, developer-advocate Revision Rec 7.

6. **Provider precedence needs a note in cli.md** (Unanimous -- all three agents). Add a note under the `run` command: "When `--provider` is not specified, the CLI defaults to `mock`, overriding the config file's `provider` field." Cross-reference config-reference.md. Source: code-verifier Revision Rec 3, user-advocate Revision New Rec A, developer-advocate Revision New Rec B.

7. **`estimate_cost_usd()` should be documented in the SDK guide** (Bilateral -- code-verifier, developer-advocate). The function at `engine/cost.py` L106-158 is fully implemented but undocumented. Source: code-verifier Revision Rec 7, developer-advocate Phase 1 agreement.

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

- **Dispute: SDK Quick Start example ordering (sync vs. async)**
  - **Positions**: user-advocate insists the first code block must use `asyncio.run()` so it works in a plain `.py` file. code-verifier and developer-advocate argue async is the native interface and reordering creates architectural mismatch; developer-advocate proposes tabbed code blocks.
  - **Arguments**: user-advocate's strongest argument: "A SyntaxError on first contact is a trust violation that no amount of downstream documentation quality can recover from. The async-native pattern belongs in the Async Patterns section, which already exists." (user-advocate disputes). code-verifier's strongest argument: "The SDK genuinely is async-first. A developer who learns the sync pattern first may structure their entire integration around asyncio.run() wrappers, missing the event subscription pattern entirely." (code-verifier cross-review of user-advocate).
  - **Synthesizer assessment**: user-advocate's position is better supported for the stated goal (first-contact success). The counter-argument about "conceptual mismatch" assumes the reader progresses linearly through the SDK page and internalizes its architectural philosophy, which is not how most developers use Quick Start sections. However, code-verifier's point about event subscriptions requiring async context is material -- a sync-only framing would hide a key SDK capability. The strongest resolution is the one user-advocate proposed in Phase 4: write `asyncio.run()` as the first code block, immediately followed by a note explaining the SDK is async-native with a link to the async section. This works in raw Markdown (no tab framework dependency), produces a runnable first example, and clearly signals the async-first architecture.
  - **Recommended resolution**: Lead with `asyncio.run()` wrapper as the first Quick Start code block. Add a one-line note immediately below: "The SDK is async-native. See Async Patterns below for `await`-based usage." This satisfies first-run success without hiding the architectural truth.

- **Dispute: Onboarding track vs. extensibility track implementation priority**
  - **Positions**: user-advocate argues onboarding fixes (quickstart prerequisites, slash command explanation, mode count fix) must be implemented first because they gate the audience for everything downstream. developer-advocate argues the end-to-end domain tutorial is P1 for the developer audience and should not be sequenced behind onboarding.
  - **Arguments**: user-advocate: "Fixing the front door has a higher expected-value payoff per hour of work because it multiplies the audience for everything downstream." (user-advocate disputes). developer-advocate: "A developer integrating conversus into a CI pipeline or a FastAPI service will never touch the quickstart -- they arrive via the SDK page or the building-domains guide directly." (developer-advocate disputes).
  - **Synthesizer assessment**: Both positions have merit, but the dispute is partly illusory. developer-advocate's claim that CI/pipeline developers skip the quickstart is well-founded; these users arrive via search, direct links, or SDK imports. user-advocate's claim about audience gating is valid for organic discovery. The real question is whether these are independent work items or sequential dependencies. The evidence supports independence: quickstart changes and domain tutorial changes touch different files, different audiences, and have no technical dependencies.
  - **Recommended resolution**: Frame as parallel independent tracks in the implementation plan, not sequential batches. State explicitly: "Onboarding improvements and extensibility improvements are independent work streams. Neither blocks the other. When resources are constrained, onboarding changes have higher expected impact per hour due to audience breadth, but extensibility changes should not wait for onboarding to complete."

- **Dispute: Quickstart inline troubleshooting hints**
  - **Positions**: user-advocate wants two inline micro-hints (one after `uv sync`, one after the API key step) in addition to a link to a dedicated troubleshooting page. code-verifier argues inline troubleshooting violates the "succinct and practical" philosophy; developer-advocate accepts a link-only approach.
  - **Arguments**: user-advocate: "The quickstart is 88 lines. Adding two one-line hints does not double it. A user who hits `uv: command not found` and must navigate to a separate page has already lost momentum." (user-advocate disputes). code-verifier: Calibrated concern against the original full-section proposal, not the micro-hint alternative.
  - **Synthesizer assessment**: user-advocate's Phase 4 proposal is materially different from the original Phase 1 proposal that code-verifier challenged. The original was a full troubleshooting section; the current proposal is a comment in a code block (`# Requires Python 3.12+. Alternative: pip install -e .`) and a single sentence after the API key step. code-verifier's length objection was calibrated to the original proposal and has not been restated against the micro-hint version. The micro-hints are consistent with the "succinct and practical" philosophy -- they add approximately 2 lines and prevent the most common first-contact failure.
  - **Recommended resolution**: Accept user-advocate's micro-hint proposal. Add `# Requires Python 3.12+. Alternative: pip install -e .` as a comment in the install code block. Add "Run `conversus status` to check." after the API key section. Link to a dedicated troubleshooting page at the bottom for everything else.

- **Dispute: Provider precedence -- documentation note vs. dead code path**
  - **Positions**: code-verifier argues the config file's `provider` field is dead code on the CLI path -- `run_engine()` uses the CLI flag directly without consulting `config.provider`. The documentation note should say the config field is not consulted, not that it is "overridden." user-advocate and developer-advocate treat this as a documentation-only fix (add a precedence note).
  - **Arguments**: code-verifier: "Documenting 'CLI --provider overrides config provider' is misleading because it implies a precedence relationship. In reality, the config provider is ignored entirely." (code-verifier disputes). developer-advocate: Config-reference.md L60 already says "CLI --provider flag overrides this" and a cross-reference suffices.
  - **Synthesizer assessment**: code-verifier's technical analysis is correct -- the call chain at `run_engine()` L207 calls `resolve_provider(provider_name)` with the CLI flag value, never reading `config.provider`. The word "overrides" implies the config value is a fallback, which it is not. However, the practical difference is narrow: both framings tell the user that passing `--provider` on the CLI determines the provider. The deeper question (should `config.provider` be wired as a fallback?) is a code design decision outside the scope of spec 031.
  - **Recommended resolution**: Accept code-verifier's more precise wording for the cli.md note: "The `run` command always uses the `--provider` flag value. When omitted, it defaults to `mock` regardless of the config file's `provider` field." File a follow-up issue to decide whether `run_engine()` should fall back to `config.provider` when the CLI flag is at its default.

- **Dispute: `domains/base.md` member filtering**
  - **Positions**: code-verifier insists the page must have an explicit `members:` list (like plugins/base.md and construction.md) to define the public API contract. user-advocate and developer-advocate focus on narrative prose without addressing the member list gap.
  - **Arguments**: code-verifier: "The member list is the structural equivalent of `__all__` in a Python module. Without it, the page cannot be a reliable API reference even in MkDocs." (code-verifier disputes).
  - **Synthesizer assessment**: code-verifier is correct. The two sibling API reference pages both have explicit member lists. `domains/base.md` having none is an inconsistency that affects rendering behavior, not just style. The narrative prose convergence (agreed by all three agents) is complementary but does not substitute for the member filter.
  - **Recommended resolution**: Add an explicit `members:` list to `domains/base.md` covering: `DomainPlugin`, `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, `Scaffold`, `VariableExtractor`, `load_scaffold`. Add `DomainStore`, `JSONLStore`, `SQLiteStore` either on this page or a new `api/domains/store.md`.

- **Dispute: End-to-end domain tutorial existence and priority**
  - **Positions**: developer-advocate rates this P1 for the developer track. user-advocate acknowledges the gap but rates it lower priority than onboarding fixes.
  - **Arguments**: developer-advocate: "A developer cannot ship a domain plugin from the current docs alone. The five-stage lifecycle (extract, score, persist, gate, serve) is stated at building-domains.md L4 but only stages 1-2 are demonstrated." user-advocate: "A developer who cannot install conversus will never reach the domain tutorial."
  - **Synthesizer assessment**: The gap is real and significant. The building-domains guide promises a 5-stage lifecycle and delivers only 2 stages. This is a P1 for developers who have already committed to building a domain. The priority dispute is resolved under the "implementation priority" dispute above -- the tutorial should proceed in parallel, not wait for onboarding.
  - **Recommended resolution**: Add the end-to-end domain tutorial as a P1 deliverable on the extensibility track. Include: constructing `DomainContext`, calling `extract()` then `score()` (using string-based scaffold name), creating a record with `create_record()` (noting optional `equilibrium_score` and `convergence` params), persisting with `JSONLStore`, and mounting the API router. Have code-verifier review every code example against source before shipping.

- **Dispute: Plugin wiring documentation location**
  - **Positions**: developer-advocate insists the building-plugins guide's "Dynamic loading" section must explain how to make a plugin importable (practical developer steps), not just describe the engine's internal `importlib` behavior. code-verifier and user-advocate focused on adding the `plugins:` key to config-reference.md without addressing the building-plugins guide.
  - **Arguments**: developer-advocate: "Config-reference.md documents *what* the YAML accepts. The building-plugins guide documents *how* to author a plugin. The wiring question is a *how* question."
  - **Synthesizer assessment**: developer-advocate is correct that the two documents serve different purposes and both need updates. The `plugins:` config-reference addition (converged, all three agents) addresses schema discoverability. The building-plugins guide update addresses developer workflow. These are complementary, not alternative.
  - **Recommended resolution**: Both changes should be made. Add `plugins:` to config-reference.md (already converged). Also update the "Dynamic loading" section in building-plugins.md with developer-facing steps: (1) make the module importable (`pip install -e .` or add to project packages), (2) set `package` to the dotted import path, (3) failure mode: warning logged and plugin skipped (non-fatal).
<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

**P1 -- Must implement**:

1. **Add `decide` 4-mode clarifying note to cli.md** (converged, unanimous). Add under the `decide` command options table: "The `decide` command supports 4 modes for ad-hoc use. The remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design) require a config file via `conversus run`. See [Deliberation Modes](modes.md) for all 8." Also update index.md to say "8 deliberation modes" with a CLI subset qualifier. [Docs change]

2. **Fix scaffolds endpoint to glob YAML files** (converged, bilateral). Change `api.py` L208 from `domain.scaffold_dir.glob("*.json")` to iterate over `("*.yml", "*.yaml", "*.json")`. The documentation is YAML-first; `load_scaffold()` handles both formats; the endpoint is the sole outlier. [Code change]

3. **Explain slash commands before the guided workflow** (unchallenged, P1). Add 2-3 sentences at the top of guided-workflow.md and before the `/conversus` block in quickstart.md: "The guided workflow uses slash commands inside an AI coding assistant (like Claude Code or Cursor). These are not terminal commands -- you type them in the assistant's chat input. To set up your editor, see [MCP Setup](mcp-setup.md)." [Docs change]

4. **Add prerequisites callout to quickstart** (modified, all agents engaged). Add a brief callout at the top of quickstart.md: "Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/)." Add `# Requires Python 3.12+. Alternative: pip install -e .` as a comment in the install code block. [Docs change]

5. **Add end-to-end domain tutorial to building-domains.md** (developer-advocate P1, unchallenged on substance). Add a "Running your domain" section demonstrating: (a) constructing `DomainContext`, (b) calling `extract()` then `score(variables, "default")`, (c) `create_record(score, context)` with optional params, (d) persisting with `JSONLStore`, (e) mounting and testing the API router. [Docs change]

6. **Add plugin wiring documentation to building-plugins.md** (developer-advocate P1, enriched by code-verifier). Update the "Dynamic loading" section: (a) `package` is a Python dotted import path, (b) module must be on `sys.path`, (c) `pip install -e .` for local development, (d) failure mode: warning logged and plugin skipped. [Docs change]

**P2 -- Should implement**:

7. **Add `plugins:` key to config-reference.md** (converged, unanimous). Add in an "Advanced / Extensibility" subsection: `name` (string), `package` (Python import path), `config` (optional, defaults to `{}`). Note: missing package logs warning and skips; failed instantiation is non-fatal. [Docs change]

8. **Add narrative prose to API reference pages** (converged, unanimous). Add layered prose to `api/plugins/base.md`, `api/domains/base.md`, and `api/schemas/construction.md`: one accessible sentence, key class listing with relationships, cross-link to developer guide. Add explicit `members:` list to `domains/base.md`. Add DomainStore/JSONLStore/SQLiteStore coverage. [Docs change]

9. **Fix `determine_verdict` documentation** (converged, bilateral). Split into "Default behavior" (base class checks hard blocks then per-dimension thresholds) and "Customizing verdict logic" (show `minimum_overall` pattern as explicit override, demonstrate `dimensions`/`variables` params). [Docs change]

10. **Add provider precedence note to cli.md** (converged, unanimous). Under the `run` command: "The `run` command always uses the `--provider` flag value. When omitted, it defaults to `mock` regardless of the config file's `provider` field. See [Config Reference](config-reference.md) for details." File follow-up issue for whether `run_engine()` should fall back to `config.provider`. [Docs change + follow-up issue]

11. **Write SDK Quick Start with sync-first code block** (disputed, synthesizer-resolved). Lead with `asyncio.run()` wrapper as the first code block. Add note: "The SDK is async-native. See Async Patterns below for `await`-based usage." [Docs change]

12. **Add error handling guidance for plugin and domain authors** (unchallenged, P2). Add subsection to both building-plugins.md and building-domains.md: exceptions are caught, logged at WARNING, and skipped; downstream consumers will not see failed producer data; recommend returning empty/default data. [Docs change]

13. **Add testing examples for plugins and domains** (unchallenged, P2). Add "Testing your plugin" section with minimal `DeliberationState` construction and assertion examples. Add equivalent for domains with `DomainContext` construction. [Docs change]

14. **Document domain-engine integration in architecture.md** (unchallenged, P2). Add subsection after the pipeline data flow explaining: domains are invoked separately from the deliberation pipeline, they consume deliberation output as input, `equilibrium_score` bridges the plugin and domain systems. [Docs change]

15. **Add `estimate_cost_usd()` to SDK guide** (converged, bilateral). Add a "Cost estimation in USD" subsection showing `from engine.cost import estimate_cost_usd` with usage example. [Docs change]

16. **Export `classify` from `engine/__init__` and document dual namespaces** (unchallenged as modified). One-line code change to add `classify` to `engine/__init__.py` exports. Add brief note to SDK page explaining `engine.*` vs. `conversus.*` import namespaces. [Code change + docs change]

17. **Add "Next steps" section to quickstart** (unchallenged as modified). Two tracks: "Explore conversus" (modes, guided workflow, MCP setup) and "Build with conversus" (SDK, building plugins, building domains). [Docs change]

18. **Add provider default model table to cli.md** (unchallenged). Add: "| Provider | Default Model | | anthropic | claude-sonnet-4-20250514 | | openai | gpt-4o |" [Docs change]

**P3 -- Consider implementing**:

19. **Add `--phase` parameter documentation note** (unchallenged). Add to cli.md: "Currently, `--phase` supports `all` (default) and `review`. Additional phase options are planned." [Docs change]

20. **Add `conversus status` to quickstart flow** (unchallenged). Add after the "Try with a real provider" section. [Docs change]

21. **Add "What you will need" to guided workflow example** (unchallenged). Brief prerequisite note before the complete example in guided-workflow.md. [Docs change]

22. **Add minimal "starter config" callout to config reference** (unchallenged as modified). 6-line minimal config at top with "This is all you need. Everything below is optional." Exclude `plugins:`. [Docs change]

23. **Document hard block function dispatch differences** (unchallenged). Brief note that internal `_check_hard_blocks` only supports three-part comparison form, while `DomainPlugin.evaluate_hard_blocks()` supports all three forms. [Docs change]

---

## Key Concessions

1. **user-advocate withdrew "list all 8 modes in cli.md `decide` section"** (Phase 3, Recommendation 10). After code-verifier demonstrated the Click constraint at L240-244, user-advocate acknowledged the original recommendation "was actively dangerous" and would have introduced a new inconsistency. Replaced with a cross-reference note preserving accuracy.

2. **code-verifier withdrew "fix the code or fix the docs" equal framing for scaffolds** (Phase 3, Recommendation 2). After developer-advocate argued the documentation is YAML-first throughout and the code is the outlier, code-verifier accepted the code-fix-only position: "developer-advocate was right that framing 'fix the code' and 'fix the docs' as equally valid was irresponsible when every scaffold example in the docs uses YAML."

3. **user-advocate conceded on sync-first SDK ordering** (Phase 3, Recommendation 4). After both code-verifier and developer-advocate challenged the sync-first reordering, user-advocate accepted the tabbed code block approach conditionally. However, user-advocate partially retracted this concession in Phase 4, insisting the fallback for non-tab rendering must still be sync-first. The concession was on the presentation mechanism (tabs acceptable), not the core requirement (first visible code must work in a plain script).

4. **code-verifier acknowledged overstating the provider precedence gap** (Phase 3, Recommendation 3). After developer-advocate's cross-review pointed out config-reference.md L60 already says "CLI --provider flag overrides this," code-verifier narrowed the recommendation from a multi-page fix to a targeted one-line note in cli.md.

5. **developer-advocate acknowledged missing the scaffolds endpoint bug** (Phase 3, New Recommendation A). "This is the single most impactful finding I missed in my original review. I praised the scaffold YAML documentation as a strength without realizing the API endpoint silently ignores YAML files."

6. **user-advocate acknowledged missing the provider precedence trap** (Phase 3, New Recommendation A). "I missed this because I was evaluating the mock-first default as a feature without considering the case where a user has explicitly chosen a different provider in their config."

7. **code-verifier acknowledged missing the GitHub reading experience for API pages** (Phase 3, New Recommendation A). "My review treated mkdocstrings directives as adequate because they render in MkDocs. Both cross-reviews correctly identified that raw-Markdown consumption on GitHub is a primary path."
