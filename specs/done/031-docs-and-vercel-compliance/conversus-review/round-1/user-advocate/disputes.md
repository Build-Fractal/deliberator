# User-Advocate — Final Disputes (Phase 4)

**Reviewer role:** user-advocate (new user perspective)
**Phase:** Final disputes and convergence

---

### Remaining Disputes

- **Dispute: SDK Quick Start example ordering and presentation**
  - **My claim**: The first code block a new user sees in the SDK page must produce a working result when pasted into a plain `.py` file. The current Quick Start opens with `await Deliberation(...).run()`, which raises `SyntaxError` outside an async function. A sync `asyncio.run()` wrapper should be the default-visible example, even if the async form is shown alongside it.
  - **Opposing position(s)**: Code-verifier argues the SDK is "natively async" and reordering to sync-first creates "a conceptual mismatch: the quickstart teaches sync, the architecture says async-first." Developer-advocate proposes a tabbed code block with sync as the default-visible tab. Both accept that the current bare `await` is broken for script users but want to preserve async as the canonical form.
  - **Why I will not concede**: The tabbed code block resolution depends on the docs framework supporting tabs. If it does not -- or if the docs are read on GitHub where custom tab components do not render -- the user sees raw `await` first and the sync pattern second, which is the same problem we have today. The fix must work in the lowest-fidelity rendering context (raw Markdown on GitHub), not just in the built MkDocs site. In my revision I accepted the tabbed approach conditionally ("if the docs framework supports it"), but I should have been firmer: the fallback for non-tab rendering must be sync-first, or the problem is not solved.
  - **Counter-argument to their position**: "Conceptual mismatch" is a concern for developers who already understand async/await. A new user who copies the first code block and gets a `SyntaxError` has a trust violation that no architectural rationale can recover. The async pattern section already exists lower on the page and is well-documented. The Quick Start's job is to produce a working result, not to teach the correct architectural paradigm.
  - **Proposed resolution path**: Write the Quick Start section with `asyncio.run()` as the first code block. Immediately below, add a one-line note: "The SDK is async-native. See [Async Patterns](#async-patterns) for `await`-based usage in async contexts." This requires zero framework support, works on GitHub, and preserves the async-first messaging without sacrificing first-run success.

- **Dispute: Onboarding track must gate extensibility track in implementation priority**
  - **My claim**: Quickstart prerequisites (Python version, `uv`/`pip`, API keys), the slash command explanation for the guided workflow, and the mode count correction on the landing page are P1 items that should be implemented before or in the same batch as the developer-facing extensibility improvements (end-to-end domain tutorial, plugin wiring docs, DomainStore API docs).
  - **Opposing position(s)**: Developer-advocate accepts the "two tracks" framing but maintains that the end-to-end domain tutorial is P1 "for the developer audience" and that both tracks should run in parallel with independent priority ratings. Code-verifier does not take a position on implementation sequencing.
  - **Why I will not concede**: "Parallel tracks with independent priorities" is a planning abstraction that does not survive contact with a single-person or small-team implementation reality. If resources are limited (which they always are), the question is which P1 gets done first. The onboarding path gates the audience for the extensibility path: a developer who cannot install conversus or who gets confused by the mode count on the landing page will never reach the domain tutorial. Fixing the front door has a higher expected-value payoff per hour of work because it multiplies the audience for everything downstream.
  - **Counter-argument to their position**: Developer-advocate's P1 rating for the domain tutorial reflects priority within a pre-qualified audience (people who have already installed conversus, run a deliberation, and decided to build a domain plugin). My P1 ratings reflect priority within the total addressable audience (everyone who visits the docs). These are not equivalent P1s, and treating them as parallel risks the extensibility docs being polished for an audience that the onboarding docs failed to create.
  - **Proposed resolution path**: Adopt explicit sequencing language in the synthesis: "Batch 1 (onboarding): quickstart prerequisites, slash command explanation, mode count fix, API reference prose. Batch 2 (extensibility): end-to-end domain tutorial, plugin wiring, DomainStore docs, testing examples." Both batches are important; the ordering reflects dependency, not relative value.

- **Dispute: Troubleshooting must be reachable from the quickstart, not just a separate page**
  - **My claim**: A "Having trouble?" line at the bottom of the quickstart linking to a dedicated troubleshooting page is necessary but not sufficient. The quickstart itself must contain inline micro-hints at the two most common failure points: the `uv sync` step (hint: "If `uv` is not installed, use `pip install -e .` instead") and the API key step (hint: "Run `conversus status` to verify your credentials").
  - **Opposing position(s)**: Code-verifier argues that inline troubleshooting could "double the quickstart's length" and violates the project's "succinct and practical" documentation philosophy. In my revision I conceded to a link-only approach, but on re-reading the quickstart, I believe I conceded too much.
  - **Why I will not concede**: The quickstart is 88 lines including code blocks. Adding two one-line hints does not double it. The "succinct and practical" philosophy is best served by preventing the user from leaving the page to solve a problem that can be addressed with 10 words. A user who hits `uv: command not found` and must navigate to a separate troubleshooting page has already lost momentum. The link to the full troubleshooting page handles edge cases; the inline hints handle the two most common failures.
  - **Counter-argument to their position**: Code-verifier's concern about page length was calibrated to my original proposal (a full "Troubleshooting" section with multiple failure modes). Two inline hints -- one after the install block, one after the API key block -- are a different proposal with a different cost-benefit profile. They add 2 lines, not 20.
  - **Proposed resolution path**: Add `# Requires Python 3.12+. Alternative: pip install -e .` as a comment in the install code block (zero additional lines outside the block), and add "Run `conversus status` to check." as a single sentence after the API key export line. Keep the link to the dedicated troubleshooting page at the bottom for everything else.

### Convergence

- **Converged: The `decide` command's 4-mode restriction needs a clarifying note in cli.md**
  - **Shared position**: Add a one-line note to the `decide` section of cli.md: "For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file. See [Deliberation Modes](modes.md) for all 8." The index page should say "8 deliberation modes" with qualification about CLI availability.
  - **Agreeing agents**: user-advocate (revision, Recommendation 10), code-verifier (revision, Recommendation 1), developer-advocate (revision, New Recommendation C)
  - **Strength**: Unanimous
  - **Path to convergence**: Code-verifier identified the factual basis (Click `choice` constraint at L240-244). User-advocate originally proposed listing all 8 in cli.md, which code-verifier correctly flagged as dangerous. All three agents converged on the documentation-only fix: keep 4 in the cli.md options table, add a cross-reference note for the other 4.

- **Converged: API reference pages need narrative prose above autodoc directives**
  - **Shared position**: Add a layered prose section to each API page: one accessible sentence summarizing the module, then key class descriptions with relationships, then links to developer guide pages. Also fix `domains/base.md` to include member filters and add `DomainStore`/`JSONLStore`/`SQLiteStore`.
  - **Agreeing agents**: user-advocate (revision, Recommendation 6), code-verifier (revision, New Recommendation A), developer-advocate (revision, Recommendation 4)
  - **Strength**: Unanimous
  - **Path to convergence**: User-advocate identified the GitHub readability gap. Code-verifier identified missing autodoc members. Developer-advocate proposed the layered approach (one-sentence summary, structural detail, cross-links). All three perspectives are additive and were merged in each agent's revision.

- **Converged: The `plugins:` key must be added to config-reference.md**
  - **Shared position**: Add a `plugins:` section to the config reference documenting the `name`, `package`, and `config` sub-keys, fallback behaviors, and non-fatal failure semantics. Place it in an "Advanced / Extensibility" subsection to avoid intimidating new users.
  - **Agreeing agents**: user-advocate (revision, New Recommendation B), code-verifier (revision, New Recommendation B), developer-advocate (revision, Recommendation 3)
  - **Strength**: Unanimous
  - **Path to convergence**: Developer-advocate identified the missing key in Phase 1. Code-verifier verified the schema against `load_plugins()` source. User-advocate flagged the intimidation risk and proposed the "Advanced" subsection placement. All three accepted the combined fix.

- **Converged: The scaffolds endpoint code must be fixed to glob YAML files**
  - **Shared position**: Fix `api.py` L208 to glob `("*.yml", "*.yaml", "*.json")`. The documentation is correct (YAML-first scaffolds throughout the building-domains guide); the code is the outlier. `load_scaffold()` already handles both formats.
  - **Agreeing agents**: code-verifier (revision, Recommendation 2), developer-advocate (revision, New Recommendation A)
  - **Strength**: Bilateral (code-verifier, developer-advocate). User-advocate did not independently identify this issue but does not dispute it.
  - **Path to convergence**: Code-verifier identified the mismatch. Developer-advocate initially praised the scaffold documentation without catching the code bug, then adopted the fix as their most significant correction. Both agree this is a code fix, not a docs fix.

- **Converged: Provider precedence (CLI flag vs. config file) needs clarification in cli.md**
  - **Shared position**: Add a note to the `run` command in cli.md: "When `--provider` is not specified, the CLI defaults to `mock`, overriding the config file's `provider` field. See [Config Reference](config-reference.md) for details."
  - **Agreeing agents**: user-advocate (revision, New Recommendation A), code-verifier (revision, Recommendation 3), developer-advocate (revision, New Recommendation B)
  - **Strength**: Unanimous
  - **Path to convergence**: Code-verifier identified the factual tension between CLI default (`mock`) and config default (`anthropic`). User-advocate recognized the silent failure risk for config-file users. Developer-advocate agreed on the one-line cross-reference approach. All three converge on cli.md as the right location for the note.

### Final Position Statement

**Non-Negotiables:**

1. **The SDK Quick Start must work when pasted into a plain Python script.** The first code block must use `asyncio.run()`, not a bare `await`. This is non-negotiable because a `SyntaxError` on first contact is a trust violation that no amount of downstream documentation quality can recover from. The async-native pattern belongs in the Async Patterns section, which already exists and is well-written.

2. **The quickstart must acknowledge `uv` as a dependency and provide a `pip` fallback.** A user who hits `uv: command not found` with no guidance in the same code block will assume the project is broken. This can be solved with a single comment line in the install block: `# Requires Python 3.12+. Alternative: pip install -e .` Zero page bloat.

3. **The slash command context must be explained before the guided workflow block.** A user who types `/conversus define` in their terminal gets a shell error with no diagnostic value. Two sentences explaining that slash commands are typed inside an AI coding assistant (Claude Code, Cursor, etc.) prevent the entire guided workflow path from being unusable for users unfamiliar with MCP tooling.

**Flexibility:**

1. **Troubleshooting page location and structure.** I am flexible on whether troubleshooting lives as a standalone page, a section within an existing page, or is integrated into the nav structure differently. My non-negotiable is that the quickstart contains micro-hints at failure points; the full troubleshooting content can live anywhere.

2. **Implementation sequencing language.** I strongly prefer explicit batching (onboarding first, extensibility second), but I can accept "parallel tracks" if the synthesis explicitly states that onboarding fixes should not be blocked by extensibility work and that a minimum viable quickstart (prerequisites, slash command explanation, mode count fix) ships independently.

3. **"Next steps" section structure.** I proposed a two-track "Next steps" section (explore vs. build). I am flexible on the exact phrasing, grouping, and number of bullets, as long as both user and developer paths are discoverable from the quickstart exit point.
