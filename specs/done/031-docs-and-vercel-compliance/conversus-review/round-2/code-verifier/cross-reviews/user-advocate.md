# Code-Verifier Cross-Review of User-Advocate -- Round 2

## Dangerous Contradictions

### 1. The `pip install conversus` claim on the index page may be a fabrication

User-advocate's Missed Opportunity #1 identifies that `docs/index.md` L29 shows `pip install conversus` while the quickstart uses `git clone` + `uv sync`. User-advocate frames this as a discrepancy requiring resolution. I verified the index page source and confirm: line 29 reads `pip install conversus` with no qualification. The quickstart at L6-7 uses `git clone <repo-url> conversus && cd conversus` followed by `uv sync`.

This is more dangerous than user-advocate states. User-advocate asks "Is there a PyPI package?" and proposes determining which page is wrong. From a code-verification standpoint, the `pyproject.toml` wires `conversus = "engine.cli:cli"` as the entry point, which only works after a local install (either `uv sync` or `pip install -e .`). If there is no published PyPI package, then `pip install conversus` is not merely inconsistent -- it is a command that will either fail outright or install an unrelated package from PyPI. This is the single most dangerous first-contact failure in the documentation suite because it appears on the front page and will execute without error if a different `conversus` package exists on PyPI.

My Round 2 review did not examine the index page at all -- I focused on source code verification of claims already in the Round 1 pipeline. User-advocate correctly identified this as a gap that all three Round 1 agents missed. I fully support elevating this to P1 and agree with user-advocate's recommendation #2 that both pages must be reconciled.

**Danger**: If left unresolved, a user who reads the index page first will run a command that either fails or installs wrong software. Neither my review nor the Round 1 synthesis addresses this.

### 2. The `--phase synthesis` epilog bug and user-advocate's `uv run` prefix finding are complementary but distinct problems

My Round 2 review (Missed Opportunity #1) identified that the `run` command epilog at `engine/cli/__init__.py` L95 shows `--phase synthesis` but Click constrains `--phase` to `["all", "review"]` at L110-113. User-advocate's Missed Opportunity #3 identifies that the CLI reference uses bare `conversus ...` while the quickstart uses `uv run conversus ...`. These are different problems that compound: a user following the quickstart's install method who then reads the CLI reference will (a) omit `uv run` and get "command not found," and (b) if they figure out the prefix, the CLI's own `--help` text shows an example (`--phase synthesis`) that will produce a Click error.

The danger is in the compounding. User-advocate correctly identifies the `uv run` prefix as a systemic discrepancy across cli.md. I confirm this is accurate: every example in cli.md (L9-21, L39-49, L67-71, L98-99, L111-115, L122-123) uses bare `conversus` without `uv run`. The quickstart at L7, L19, L48, L51, L85 consistently uses `uv run conversus`. A user who learns from the quickstart and then consults the CLI reference will hit this mismatch on every single example.

Neither review alone captures the full picture. Together, they reveal a two-layer CLI documentation problem: the examples use the wrong invocation prefix (user-advocate's finding) and the CLI's own help text contains an invalid example (my finding). Both must be fixed.

**Danger**: Fixing only one layer leaves the other broken. The implementation plan must address both the `uv run` prefix discrepancy (user-advocate's recommendation #4) and the epilog bug (my recommendation #1) as coordinated fixes.

### 3. The three-way provider default mismatch is more severe than either review states in isolation

My Round 2 review (Missed Opportunity #5) documented the three-way default: `EngineConfig.provider` defaults to `"anthropic"` at `engine/config.py` L77, the CLI defaults to `"mock"` at `engine/cli/__init__.py` L101, and the SDK defaults to `"mock"` at `engine/sdk.py` L155. User-advocate does not address this specific finding in Round 2 but endorsed the Round 1 convergence on provider precedence (CV-3).

The contradiction arises because user-advocate's recommendation #2 (resolve `pip install conversus` vs `uv sync`) and my finding about provider defaults interact badly. Consider the user journey: a user reads the index page, runs `pip install conversus` (if it works), writes a config file without `provider:` (getting `anthropic` by default from `EngineConfig`), then runs `conversus run config.yml` without `--provider` (getting `mock` from the CLI default). They expect Anthropic because their config says `anthropic`. They get mock because the CLI ignores the config.

User-advocate's Round 2 framing focuses on the index page as "the real front door" and the `uv run` prefix as the systemic CLI problem. My Round 2 framing focuses on the three-way default as a deeper manifestation of CV-3. Neither review connects the dots between the install path contradiction and the provider default trap. The Round 1 synthesis addressed CV-3 with a one-line note in cli.md, but that note only helps if the user reads cli.md. A user who installs via `pip` and writes a config file may never see cli.md.

**Danger**: The converged CV-3 resolution (a note in cli.md) is necessary but insufficient. The config-reference.md must also clarify this, as my recommendation #4 proposes. User-advocate's index page fix and my config-reference clarification are both needed to close this gap for different user entry points.

### 4. User-advocate's "copy-paste test" reframing of the SDK sync-first dispute is stronger than my Round 2 position

User-advocate's Off-Base Assumption #2 argues the strongest case for sync-first SDK examples is the "copy-paste test": the first code block should be saveable as `script.py` and runnable with `python script.py`. My Round 2 review accepted the synthesizer's sync-first resolution without contesting it, noting my "conceptual mismatch" concern was "valid architecturally but the synthesizer correctly identified that Quick Start sections are not read linearly."

The contradiction is that I conceded on the wrong grounds. I framed my concession as accepting that Quick Start sections are not read linearly. User-advocate's copy-paste test framing is more precise: it is not about reading order but about whether the first code block is self-contained and executable. An `await`-based snippet cannot be pasted into a script and run. An `asyncio.run()` snippet can. This is a testable, falsifiable criterion that applies to all documentation, not just this one page.

This is not a reversal of my position -- I already accepted the sync-first resolution. It is an acknowledgment that user-advocate's framing provides a durable principle ("first code blocks must pass the copy-paste test") that I should have adopted in my own review. My Round 2 recommendation #7 (document `Deliberation.cost_estimate` nullability) and recommendation #10 (`construct_objective` failure modes) both describe cases where the SDK docs show happy-path code that would fail in practice -- the same principle applies.

**Danger**: None immediate, since both reviews agree on the resolution. But the copy-paste test principle should be stated explicitly in the implementation plan so it applies consistently to all first-example blocks, including the cost estimation and construction pipeline examples I identified.

## Tensions

### 1. Scope of the index page fix: number change vs. structural rework

User-advocate's recommendation #1 calls for fixing the index page "4 modes" claim across three locations: the Three Layers table (L20), the Quick Links section (L62-63), and the modes page. My Round 2 review did not revisit the index page, having accepted the Round 1 convergence on this item.

I verified the index page source. Line 20 says "4 competition modes." Lines 61-63 show `Competition Modes: Cooperative, winner-take-all, prisoner's dilemma, red-blue` -- listing exactly four by name. User-advocate is correct that the Round 1 synthesis scoped this too narrowly as a "change 4 to 8" fix. The Quick Links section explicitly enumerates four modes, which means changing the number alone creates a new inconsistency (the list still shows only four).

The tension is about work scope. The Round 1 convergence (P1 #1) says "update index.md to say '8 deliberation modes' with a CLI subset qualifier." User-advocate wants the Quick Links enumeration expanded or removed. I agree with user-advocate that the Quick Links list must also be addressed -- listing four modes by name while claiming eight is self-contradictory. However, I would add that the Quick Links card title `:material-sword-cross: **[Competition Modes]**` should also change to "Deliberation Modes" for consistency with the terminology shift from "competition" to "deliberation" that the Round 1 synthesis recommends. User-advocate did not flag the card title, only the enumerated list beneath it.

### 2. Visual break vs. textual explanation for the slash command context switch

User-advocate's recommendation #3 calls for a heading ("## Try the guided workflow (in your AI editor)") and a 2-sentence explanation before the slash commands in quickstart.md. The Round 1 synthesis (P1 #3) recommended "2-3 sentences" of explanation. User-advocate explicitly pushes back that 2-3 sentences are insufficient and demands a structural change (heading or callout box).

I did not address this in my Round 2 review. Looking at the quickstart source, lines 54-66 show the section with `## Try the guided workflow` as the heading and a code comment `# In Claude Code or any MCP-compatible editor:` as the only context. User-advocate is right that the code comment is easy to miss. The heading already exists but says nothing about the execution context change. User-advocate's proposed heading `## Try the guided workflow (in your AI editor)` embeds the context switch in the heading itself, which is a stronger signal than a paragraph that might be skipped.

The tension is between my general preference for minimal documentation changes (aligned with the "succinct and practical" philosophy) and user-advocate's argument that this specific transition is a broken quickstart, not a missing explanation. Having re-read the quickstart, I lean toward user-advocate's position: the heading change is one line and eliminates the most common failure mode (typing `/conversus define` into a terminal). The 2-sentence explanation below it is additional but justified.

### 3. Example output in the quickstart: useful vs. fragile

User-advocate's recommendation #5 proposes adding example output to the quickstart's "What just happened" section. My Round 2 review did not address output examples. The tension is that example output is helpful for first-contact verification (user-advocate's point) but becomes a maintenance burden because output format changes with every release. Mock provider output in particular may change as the mock implementation evolves.

I would accept this as a P2 recommendation (matching user-advocate's priority) but with a caveat: the example should be clearly marked as "approximate" or use a collapsed/abbreviated format that is less likely to drift. User-advocate acknowledges this implicitly ("Even 10-15 lines of representative output") but the implementation must resist the temptation to show complete output, which would create a new documentation maintenance surface.

### 4. `uv` prerequisite coverage in the quickstart micro-hint

User-advocate's recommendation #6 extends the quickstart micro-hint from `# Requires Python 3.12+. Alternative: pip install -e .` to `# Requires Python 3.12+ and uv (https://docs.astral.sh/uv/). Alternative: pip install -e .`. My Round 2 review accepted the micro-hint resolution from Round 1 without proposing extensions.

The tension is about comment length in a code block. The extended hint is 79 characters (within typical line limits) and adds material information -- a user who does not have `uv` installed is the most common first-contact failure for the `git clone` + `uv sync` path. I accept this extension as reasonable. The URL is the right addition because it answers the immediate question ("what is uv?") without requiring the user to leave the page. This is consistent with my general support for the micro-hint approach from Round 1.

### 5. MkDocs vs. GitHub reading surface remains unresolved

User-advocate's recommendation #7 proposes adding a sentence stating MkDocs is the primary reading surface and including `uv run mkdocs serve` build instructions. My Round 2 review (recommendation #6, under "narrative prose") addresses the same API reference pages but focuses on adding `members:` lists and DomainStore coverage without taking a position on the reading surface question.

The tension is that user-advocate's proposal resolves the Round 1 Systemic Contradiction #3 with a simple declaration ("MkDocs is primary"), while my approach treats the symptom (add prose that works in both formats) without resolving the root cause. User-advocate's solution is cleaner: stating the primary surface once eliminates the recurring debate about dual-format content. My prose additions are complementary -- they help regardless of whether GitHub or MkDocs is primary. Both should be implemented, but user-advocate's framing should come first because it sets the policy that informs all other API reference decisions.

## Safe Agreements

### 1. The Round 1 convergence items are correctly scoped and verified

Both reviews confirm all seven Round 1 convergence items without reversal. User-advocate's Alignment section endorses items 1-8 explicitly. My Round 2 review's Alignment section re-verifies each against source code with line references. There is no tension on any converged item.

Specific overlapping confirmations: the `decide` 4-mode restriction (CV-1) is verified against `engine/cli/__init__.py` L240-241 in both reviews; the scaffolds endpoint YAML bug (CV-2) is confirmed at `api.py` L208 in both; the `plugins:` config key (CV-B) is confirmed against `load_plugins()` at `plugins/base.py` L229-295 in both; the provider precedence note (CV-3) is confirmed against `engine/run.py` L207 in both.

### 2. The slash command context switch in quickstart.md is a P1 fix

Both reviews agree this is a critical gap. User-advocate's recommendation #3 calls it a "broken quickstart." My Round 2 review did not independently surface this (it was already in the Round 1 pipeline as P1 #3), but I support the Round 1 synthesis resolution and do not contest user-advocate's request to strengthen it with a structural heading change. The substance of the fix -- explaining that `/conversus` commands are slash commands for AI editors, not terminal commands -- is not disputed by any agent in any round.

### 3. The `determine_verdict` documentation split is the correct structural fix

Both reviews endorse the Round 1 converged resolution (CV-8) to split `determine_verdict` documentation into "Default behavior" and "Customizing verdict logic." My Round 2 verification confirmed the base class at `domains/base.py` L628-656 (now L355-376 for `_determine_verdict` and L628-656 for the method) checks hard blocks then per-dimension thresholds but does NOT check `minimum_overall`. User-advocate accepted this in alignment item #5. The implementation is straightforward and uncontested.

### 4. The `estimate_cost_usd()` function must be documented

Both reviews carry forward the Round 1 converged finding (CV-7) that `engine/cost.py` contains a fully implemented `estimate_cost_usd()` function that is not documented anywhere. Neither review contests the P2 priority or the proposed fix (add a subsection to the SDK guide). This is a clean gap with no ambiguity about what the fix should contain.
