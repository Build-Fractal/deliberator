# User-Advocate Revision: Conversus Documentation Suite

**Reviewer role:** New user who has never seen conversus, evaluating the documentation for first-time usability.

**Revision iteration:** 1

---

## Recommendation Dispositions

#### Recommendation 1: Add prerequisites section to quickstart

- **Original position**: Add a "Prerequisites" section before "Install" listing Python 3.12+, `uv` with install link and `pip` fallback, and API key requirements.
- **Disposition**: Modified
- **Explanation**: The code-verifier's cross-review (Tensions, "Quickstart prerequisites: how much context is enough?") correctly invokes the project's documentation philosophy -- "succint and practical" -- and argues that a full prerequisites section with install links, pip fallbacks, and troubleshooting could double the quickstart's length. The developer-advocate's cross-review (Dangerous Contradictions, "`uv` dependency") confirms the problem is real ("Corporate environments, Docker containers with minimal tooling, and CI/CD pipelines that use `pip` would all hit this wall") but suggests showing both installation paths briefly. The modification: replace the proposed full "Prerequisites" section with a 2-3 line callout at the top of the quickstart: "Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/). Alternative: `pip install -e .`" -- enough to unblock a stuck user without bloating the page. The detailed troubleshooting belongs on a separate page (see modified Recommendation 5).

#### Recommendation 2: Explain slash commands before the guided workflow

- **Original position**: Add a 2-3 sentence explanation at the top of guided-workflow.md and before the `/conversus` block in quickstart.md explaining that slash commands are typed inside an AI coding assistant, not a terminal.
- **Disposition**: Surviving
- **Explanation**: Neither cross-review challenged this recommendation. The code-verifier's cross-review does not address the guided workflow (outside verification scope). The developer-advocate's cross-review (Tensions, "Guided workflow: explanation depth") acknowledges the recommendation falls outside their scope but notes that future developer-advocate edits to guided-workflow.md would need to coordinate with the new prerequisite section. This implicit acceptance, combined with the fact that a user who types `/conversus define` in their terminal will get a shell error with zero diagnostic value, means this recommendation stands. The risk of leaving it unfixed -- the entire guided workflow path being unusable for users unfamiliar with Claude Code -- remains the highest-severity user-facing gap in the documentation.

#### Recommendation 3: Fix "4 modes" claim on index page

- **Original position**: Update index.md to say "8 deliberation modes" and list all 8.
- **Disposition**: Modified
- **Explanation**: The code-verifier's cross-review (Dangerous Contradictions, "CLI `decide` mode count") provided critical new information: the `decide` command's Click definition at `engine/cli/__init__.py` L240-244 genuinely constrains `--mode` to exactly 4 modes via `click.Choice`. The remaining 4 modes require a config file via `conversus run`. This means the index page should not say a flat "8 modes" without qualification, because users will reasonably expect all 8 to work with `decide`. The developer-advocate's cross-review (Dangerous Contradictions, "Mode count inconsistency") reinforces this: "If user-advocate's fix is applied to the index page but not the CLI, users will see '8 modes' on the landing page, try `conversus decide --mode negotiation`, and get an error." The modification: update index.md to say "8 deliberation modes" with a qualifier such as "4 available via ad-hoc CLI, all 8 via config file." This respects the code-verifier's factual finding while still correcting the landing page's undercounting.

#### Recommendation 4: Put sync example first in SDK doc

- **Original position**: Move the sync `asyncio.run()` pattern to be the first "Quick start" example and demote the async pattern to a secondary section.
- **Disposition**: Modified
- **Explanation**: Both cross-reviews challenged this, and both made compelling arguments I accept. The code-verifier's cross-review (Dangerous Contradictions, "SDK async-first versus sync-first example ordering") correctly notes that the SDK is natively async -- `Deliberation.run()` is async by design, and the event subscription pattern requires an async context. Reordering to sync-first would create "a conceptual mismatch: the quickstart teaches sync, the architecture says async-first." The developer-advocate's cross-review (Dangerous Contradictions, "SDK async-vs-sync first example priority") proposes a concrete resolution: a two-tab code block with "Script (sync)" default-selected and "Async" as the second tab. This satisfies my concern (the first thing a new user sees must work in a plain script) without demoting the async pattern that is architecturally correct. The modification: keep `await` as the canonical form but add a prominent note at the top of the Quick Start section -- "The SDK is async-first. In a synchronous script, wrap with `asyncio.run()` (see Async Patterns below)" -- and, if the docs framework supports it, use a tabbed code block with sync as the default-visible tab. This is the developer-advocate's suggested resolution, which I adopt.

#### Recommendation 5: Add troubleshooting section to quickstart

- **Original position**: Add a "Troubleshooting" section at the bottom of quickstart.md covering common failure modes.
- **Disposition**: Modified
- **Explanation**: The code-verifier's cross-review (Tensions, "Quickstart prerequisites: how much context is enough?") argues that inline troubleshooting could double the quickstart's length, violating the project's "succint and practical" documentation philosophy. The developer-advocate's cross-review (Tensions, "Troubleshooting: where to put it") raises a structural concern: if troubleshooting is scattered across the quickstart, plugin guide, and domain guide with no cross-linking, content fragments with no single entry point. The modification: instead of an inline troubleshooting section in the quickstart, add a brief "Having trouble?" line at the bottom of the quickstart linking to a dedicated troubleshooting page (or a "Troubleshooting" section in the nav). The dedicated page can cover common quickstart failures (`uv` not found, Python version, missing API key) alongside plugin and domain issues, preventing fragmentation. This keeps the quickstart short while still giving stuck users somewhere to go.

#### Recommendation 6: Add introductory prose to API reference stubs

- **Original position**: Add 3-5 sentences above each `:::` directive describing what the module does, its key classes, and a one-line usage example, so GitHub readers get value from raw Markdown.
- **Disposition**: Modified
- **Explanation**: Both cross-reviews agree this recommendation is directionally correct but propose going further. The code-verifier's cross-review (Tensions, "API reference stub treatment") notes that the stubs are technically incomplete even within MkDocs -- `domains/base.md` has no member filter at all, and `DomainStore`, `JSONLStore`, and `SQLiteStore` are missing entirely. The developer-advocate's cross-review (Dangerous Contradictions, "API reference stubs: prose-first vs. autodoc-first") argues that prose alone is insufficient because it does not convey structural relationships between members. The developer-advocate proposes a layered approach: one plain-English sentence (for new users), then structural detail with key class descriptions and relationships (for developers), then links to developer guide pages (for both). I adopt this layered approach. The modification: write a single prose section per API page that opens with an accessible one-sentence summary (my original concern), then lists key classes with one-line descriptions and relationships (developer-advocate's concern), and also fix the member lists and add missing modules like DomainStore (code-verifier's concern). This is additive -- all three positions are complementary, not competing.

#### Recommendation 7: Add "Next steps" section to quickstart

- **Original position**: Add a "Next steps" section with 3-4 bullets pointing to modes, guided workflow, SDK, and MCP setup.
- **Disposition**: Modified
- **Explanation**: The developer-advocate's cross-review (Tensions, "'Next steps' navigation vs. developer onboarding path") makes a valid point: my proposed next-steps list omits the developer path (quickstart -> SDK -> building-plugins -> building-domains), which means the developer audience remains invisible from the primary entry point. The modification: add a "Next steps" section with two tracks: "Explore conversus" (modes, guided workflow, MCP setup) for users, and "Build with conversus" (SDK, building plugins, building domains) for developers. This costs one extra line of text but makes both paths discoverable from the quickstart exit point.

#### Recommendation 8: Add "What you will need" context to the guided workflow complete example

- **Original position**: Add a "Before you start" note to the complete example in guided-workflow.md specifying prerequisites (Claude Code open, MCP configured, project directory active).
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this recommendation directly. The developer-advocate's cross-review (Tensions, "Guided workflow: explanation depth") acknowledges that future edits to guided-workflow.md would need to coordinate with new prerequisite content, implicitly accepting that such content is needed. The code-verifier's review does not address the guided workflow. This recommendation is low-risk, low-effort, and partially redundant with Recommendation 2 (if the slash command explanation is adopted, users will already have some context), but the complete example at the bottom of the page is a likely copy-paste target and benefits from its own brief prerequisite note. It survives as originally stated.

#### Recommendation 9: Add a minimal "starter config" callout to config reference

- **Original position**: Add a "Start here" section at the top of the config reference with a 6-line minimal config and the sentence "This is all you need. Everything below is optional."
- **Disposition**: Modified
- **Explanation**: The developer-advocate's cross-review (Tensions, "Config reference: completeness vs. approachability") raises a coordination concern: the `plugins:` key is missing from the config reference entirely (developer-advocate's Recommendation #3, rated P1), and if a starter template is added without also adding `plugins:`, it reinforces the idea that plugins are an afterthought. On the other hand, if `plugins:` is added to the full schema without a starter template, the page becomes even more intimidating. The modification: add the starter template at the top as originally proposed, explicitly excluding `plugins:` (it is an advanced feature). Then ensure the full schema section below includes the `plugins:` key (adopting the developer-advocate's finding). The structure becomes: minimal starter template (top) -> full schema with all keys including `plugins:` (middle) -> common configs (bottom). This coordinates both recommendations without conflict.

#### Recommendation 10: Cross-link the CLI `decide` command back to modes

- **Original position**: Update the `--mode` description in cli.md to say "See Deliberation Modes for all 8 options" and list all 8 mode names.
- **Disposition**: Modified
- **Explanation**: The code-verifier's cross-review (Dangerous Contradictions, "CLI `decide` mode count") showed that my original recommendation was actively dangerous. The `decide` command's Click definition genuinely constrains `--mode` to 4 modes. If I had listed all 8 in the cli.md `--mode` description, users would try `conversus decide --mode negotiation` and get an unhelpful Click error. The code-verifier is right: "The docs would be actively misleading about what the CLI accepts." The modification: keep the cli.md `decide` section listing exactly the 4 supported modes, but add a note below the options table: "The `decide` command supports 4 modes for ad-hoc use. The remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design) require a config file via `conversus run`. See [Deliberation Modes](modes.md) for all 8." This preserves accuracy (code-verifier's concern) while ensuring discoverability (my original concern).

---

## New Recommendations

#### New Recommendation A: Document provider precedence (CLI flag vs. config file)

- **Source**: code-verifier's cross-review (Dangerous Contradictions, "Provider default: 'mock' or 'anthropic'?")
- **Proposed change**: Add a note to the config reference's `provider:` field and/or the CLI reference's `--provider` flag: "The `--provider` CLI flag overrides the `provider` field in the config file. When neither is specified, the CLI defaults to `mock`." Also note this in the `conversus run` section of cli.md.
- **Rationale**: My original review praised the auth resolution documentation as clear and did not notice the CLI-vs-config default tension. The code-verifier identified a real trap: a user who writes `provider: anthropic` in their config and runs `conversus run conversus.yml` without `--provider` may get mock responses because the CLI default silently overrides. This is a silent failure with no diagnostic output, which is the worst kind of user experience. I missed this because I was evaluating the mock-first default as a feature (it is, for onboarding) without considering the case where a user has explicitly chosen a different provider in their config.
- **Priority**: P2. Not a P1 because users following the quickstart will have `--provider` explicitly set, but it will bite users who graduate to config files.

#### New Recommendation B: Add `plugins:` key to config reference

- **Source**: developer-advocate's review (Recommendation #3, P1), surfaced in my cross-review of the developer-advocate
- **Proposed change**: Add a `plugins:` section to the full schema in config-reference.md, documenting the `name`, `package`, and `config` sub-keys with a brief example.
- **Rationale**: The config reference claims to be the single source of truth for the YAML schema, but it omits a top-level key. This is a factual gap. A developer who discovers plugins via the building-plugins guide will look for the config syntax in the config reference and not find it. The building-plugins guide (L142-152) shows the YAML syntax, but the config reference should be self-contained.
- **Priority**: P2. The building-plugins guide has the syntax, so this is not blocking, but the config reference's completeness is important for trust.

---

## Position Summary

The cross-review process sharpened my recommendations in three significant ways. First, the code-verifier's finding that `decide` only supports 4 of the 8 modes via Click constraint exposed a genuine error in my original Recommendations 3 and 10 -- I would have introduced a new inconsistency by telling users all 8 modes work everywhere. The fix is to qualify rather than flatten: say "8 modes" on the landing page with a note about the CLI subset, and keep cli.md listing exactly 4 with a cross-link to the full set. Second, both cross-reviewers challenged my sync-first SDK proposal. The developer-advocate's tabbed code block suggestion and the code-verifier's architectural argument convinced me that reordering is the wrong remedy; a prominent note plus a tabbed display (sync default-visible) preserves both accuracy and first-time-user success. Third, both reviews pushed me to keep the quickstart lean rather than loading it with prerequisites and troubleshooting. A brief callout plus a link to a dedicated troubleshooting page respects the project's "succint and practical" philosophy without abandoning the users who will hit `uv: command not found` on their first attempt.

My core position is unchanged: the documentation's biggest risks are at the front door, not in the advanced rooms. A user who cannot get past `uv sync` or who tries to run `/conversus define` in a terminal will never reach the plugin guide, the domain guide, or the config reference. The onboarding path (quickstart prerequisites, slash command explanation, mode count accuracy) must be fixed before or in parallel with the extensibility path (end-to-end domain tutorial, plugin wiring, error handling guidance). Both paths matter, but the onboarding path gates the audience for everything else.

The cooperative process also revealed a gap I missed entirely: the provider precedence trap (code-verifier's finding). A user who explicitly writes `provider: anthropic` in their config and gets mock responses because the CLI default silently overrides is experiencing a trust violation. This is now New Recommendation A. I also adopted the developer-advocate's finding that the config reference omits the `plugins:` key (New Recommendation B), which is a factual completeness gap in the document that claims to be the single source of truth for the YAML schema. Both new recommendations emerged from genuine blind spots in my original review -- the user-advocate lens optimizes for first contact and does not catch the traps that appear after a user has graduated to config files and plugin development.
