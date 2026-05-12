# User-Advocate Review -- Round 2

## Executive Summary

Reading the conversus documentation suite as a new user who has never encountered this tool, I find a product that is technically impressive but has a front door that loses people at several critical moments. The quickstart is close to working on first try but falls short due to missing prerequisite information and an unexplained jump from terminal commands to slash commands. The mode descriptions are strong in isolation but the mismatch between the index page ("4 competition modes"), the modes page (8 modes), and the CLI `decide` command (4 modes) creates genuine confusion about what the product actually offers. The SDK documentation assumes async fluency that most users arriving from a quickstart will not have. The developer-facing guides (building plugins, building domains) are well-structured but incomplete -- they teach the first two stages of a five-stage lifecycle and leave the developer to infer the rest.

Round 1 identified these issues comprehensively and produced strong convergence on most of them. In this Round 2 review, I focus on (a) validating that the Round 1 convergence items are correctly scoped, (b) pushing back on areas where the synthesis under-weighted the user impact, and (c) identifying gaps that Round 1 missed because all three agents were focused on the same subset of files.

## Alignment

I agree with the Round 1 synthesis on the following points and consider them well-resolved:

1. **`decide` 4-mode restriction note (P1, converged)**: Correct diagnosis, correct fix. The one-line cross-reference is the right weight for this problem. The index page's "4 competition modes" must also be fixed to say "8 deliberation modes" -- the synthesis captured this.

2. **Scaffolds endpoint YAML glob fix (P1, converged)**: Code bug, not a docs bug. The synthesis correctly sided with developer-advocate's framing that the docs are right and the code is wrong.

3. **`plugins:` key in config-reference.md (P2, converged)**: Placing this in an "Advanced / Extensibility" subsection is the right call. The config reference should be complete. I support the synthesizer's recommendation to keep it out of any "starter config" callout.

4. **API reference narrative prose (P2, converged)**: The layered approach (accessible sentence, key classes, cross-link) is the right structure. The `domains/base.md` missing `members:` list is a real inconsistency that should be fixed.

5. **`determine_verdict` split (P2, converged)**: The split into default behavior and custom override is a clean fix. No further comment.

6. **Provider precedence note (P2, converged)**: I accept code-verifier's more precise wording. "The `run` command always uses the `--provider` flag value. When omitted, it defaults to `mock` regardless of the config file's `provider` field." This is clearer than "overrides."

7. **`estimate_cost_usd()` documentation (P2, converged)**: Agreed. This function exists and should be documented.

8. **Parallel implementation tracks (disputed, synthesizer-resolved)**: I accept the synthesizer's resolution that onboarding and extensibility are independent work streams. My Round 1 concern about sequencing was about audience gating, but the synthesizer correctly noted these changes touch different files and serve different audiences. I do not reverse this concession.

## Missed Opportunities

### 1. The index page is the real front door, and it is actively misleading

The Round 1 synthesis focused heavily on quickstart.md, cli.md, and modes.md, but the index page (`docs/index.md`) is what most users see first and it has problems that no agent fully addressed:

- **"4 competition modes"** in the Three Layers table (line 20). The Round 1 synthesis noted this should say "8 deliberation modes," but the fix is more than a number change. The table says the Engine layer provides "4 competition modes" and the Quick Links section (line 62-63) says "Competition Modes: Cooperative, winner-take-all, prisoner's dilemma, red-blue." This lists exactly four modes, reinforcing the false claim. A user who reads the index page and then discovers the modes page has 8 modes will wonder if they are looking at outdated docs.

- **`pip install conversus`** (line 29). The quickstart says `uv sync`. The index page says `pip install conversus`. Are these equivalent? Is there a PyPI package? The quickstart does not mention pip. This is a contradiction that will confuse a user who reads the index first and the quickstart second. The Round 1 synthesis did not identify this discrepancy.

- **The Quick Install section has no prerequisites**. The index page shows `pip install conversus` with no mention of Python version, and `uv sync` with no mention of what uv is. At least the quickstart provides context with `# Python 3.12+ required`. The index page provides none.

### 2. The guided workflow section in quickstart.md is a trap for new users

The quickstart (lines 56-66) transitions from terminal commands (`uv run conversus decide ...`) to slash commands (`/conversus define ...`) with no explanation of the context switch. The comment "In Claude Code or any MCP-compatible editor" is a parenthetical in a code comment -- easy to miss. A user following the quickstart sequentially will type `/conversus define` into their terminal and get a "command not found" error.

The Round 1 synthesis captured this as P1 item #3 ("Explain slash commands before guided workflow"), but I want to emphasize the severity: this is not a missing explanation, it is a broken quickstart. A user who hits this wall does not know if they broke something or if the tool is broken. The fix must be more prominent than "2-3 sentences" -- it needs a visual break (horizontal rule, heading, or callout box) to signal that the execution context has changed.

### 3. The `uv run` prefix is inconsistent and unexplained

The quickstart uses `uv run conversus ...` for every command. The CLI reference uses bare `conversus ...` without `uv run`. A new user who follows the quickstart's install method (git clone + `uv sync`) will have `conversus` available only via `uv run`. When they open the CLI reference, every example will fail because they are all written as `conversus decide ...` without the `uv run` prefix.

This is a systemic discrepancy across the entire CLI reference page. Round 1 did not identify it. The fix is either: (a) add a note at the top of cli.md explaining "If you installed via `uv sync`, prefix all commands with `uv run`", or (b) add `uv run` to all CLI reference examples, or (c) add a note to the quickstart about activating the venv or installing globally.

### 4. The "What just happened" section assumes success but does not show output

The quickstart's "What just happened" section (lines 26-39) describes the 5-phase deliberation in abstract terms but never shows what the terminal output actually looks like. A user running `--provider mock` will see output, but they have no way to verify whether what they see matches what was expected. A single example output block (even abbreviated) would close this gap. Round 1 did not identify this.

### 5. No error recovery path anywhere in the quickstart

If `uv sync` fails (wrong Python version, missing build tools, network error), the user has no guidance. If the `conversus decide` command fails (provider error, malformed input), the user has no guidance. The quickstart assumes a happy path from start to finish.

The Round 1 synthesis discussed this under "Quickstart inline troubleshooting hints" and resolved it with micro-hints. I support that resolution and do not reverse it, but I want to note that the micro-hints proposed (a comment about Python 3.12 and `conversus status`) do not cover the `uv sync` failure case, which is the most likely first-contact failure for a user who does not have uv installed.

## Off-Base Assumptions

### 1. The Round 1 synthesis under-weighted the index page contradictions

The synthesis treated the "4 modes vs. 8 modes" issue as a simple number fix (change "4" to "8"). But the index page's Quick Links section explicitly lists only four modes by name. The modes page heading says "8 modes." The `decide` command supports exactly 4. The `run` command supports all 8. This is a three-way inconsistency that requires coordinated edits across three pages, not just a number change on the index page. The P1 item #1 in the synthesis's Actionable Spec Changes is scoped too narrowly.

### 2. The sync vs. async SDK dispute was resolved correctly but the reasoning missed the strongest argument

The synthesis resolved the SDK Quick Start ordering dispute in favor of sync-first (asyncio.run wrapper), which I support. But the strongest argument was not about "SyntaxError on first contact" -- it was about the copy-paste test. The quickstart shows a terminal command. The SDK Quick Start should follow the same principle: the first code block should be copy-pasteable into a `script.py` file and run with `python script.py`. The async example using bare `await` fails that test because it requires being inside an async function, which is not shown. The `asyncio.run()` wrapper passes the copy-paste test. This framing is more durable than the "trust violation" argument because it generalizes to all documentation: first examples should be self-contained and runnable.

### 3. The "raw Markdown vs. MkDocs" systemic contradiction was identified but not resolved

The Round 1 synthesis identified this as Systemic Contradiction #3 but did not recommend a resolution. The API reference pages (`api/plugins/base.md`, `api/domains/base.md`, `api/schemas/construction.md`) contain mkdocstrings directives that render as meaningful content in MkDocs but appear as opaque code blocks on GitHub. The synthesis recommended adding narrative prose above the directives, which helps, but did not answer the core question: is GitHub a supported reading surface? If yes, the API reference pages need dual-format content. If no, this should be stated somewhere so users know to use the MkDocs site. This remains unresolved.

## Actionable Recommendations

1. **P1: Fix the index page "4 modes" claim across all three locations.** The Three Layers table (line 20) says "4 competition modes." The Quick Links section (lines 62-63) says "Cooperative, winner-take-all, prisoner's dilemma, red-blue." The modes page has 8. Fix all three: change the table to "8 deliberation modes," expand or remove the named list in Quick Links, and add the CLI subset qualifier from Round 1 convergence. This extends Round 1 P1 #1 to cover the index page comprehensively.

2. **P1: Resolve the `pip install conversus` vs. `uv sync` discrepancy on the index page.** The index page shows `pip install conversus` as the primary install path. The quickstart shows `git clone` + `uv sync`. If there is no PyPI package, the `pip install conversus` line is a lie that will fail on first contact. If there is a PyPI package, the quickstart should mention it. One of these pages is wrong; determine which and fix both.

3. **P1: Add a visual break and explicit context-switch explanation before slash commands in quickstart.md.** The current transition from terminal commands to `/conversus define` is a code comment. Replace with a heading ("## Try the guided workflow (in your AI editor)") and a 2-sentence explanation: "The following commands are slash commands for AI coding assistants like Claude Code or Cursor. They are not terminal commands. See [MCP Setup](mcp-setup.md) to configure your editor." This strengthens Round 1 P1 #3 with a structural, not just textual, fix.

4. **P1: Add a note to cli.md about the `uv run` prefix.** At the top of the CLI reference, add: "If you installed via `git clone` + `uv sync`, prefix all commands with `uv run` (e.g., `uv run conversus run config.yml`). If you installed via `pip install conversus`, the commands work directly." This is a new finding not in Round 1.

5. **P2: Add example output to the quickstart "What just happened" section.** After the 5-phase explanation, add a collapsed or abbreviated output block showing what the terminal prints for a `--provider mock` run. Even 10-15 lines of representative output would help the user verify they succeeded. This is a new finding not in Round 1.

6. **P2: Expand the quickstart micro-hint to cover `uv` not being installed.** The Round 1 resolution accepted micro-hints in the install code block. Extend the hint from `# Requires Python 3.12+. Alternative: pip install -e .` to `# Requires Python 3.12+ and uv (https://docs.astral.sh/uv/). Alternative: pip install -e .`. This covers the most common first-contact failure. This refines the Round 1 synthesis resolution for the troubleshooting dispute.

7. **P2: State the primary documentation reading surface.** Add a sentence to the developer guide or contributing guide: "This documentation is built with MkDocs Material. API reference pages use mkdocstrings and require a built site to render fully. To build locally: `uv run mkdocs serve`." This resolves Round 1 Systemic Contradiction #3 without requiring dual-format content.

8. **P2: Reframe SDK sync-first resolution around the copy-paste test.** When implementing the Round 1 sync-first resolution, frame the `asyncio.run()` example with a comment like `# Save as script.py and run: python script.py`. This makes the rationale self-documenting and extends the principle to other first-example blocks.

9. **P3: Add a "What you will see" section to the modes page.** Each mode description explains when to use it and shows a YAML snippet, but none describe what the output looks like. A user choosing between modes cannot predict the shape of the synthesis. Even one sentence per mode ("Synthesis produces a converged position with surviving disputes" vs. "Synthesis declares a winner with runner-up conditions") would help. Some modes already have this partially ("Synthesis produces a deal structure" for negotiation) but it is inconsistent.

10. **P3: Add the `conversus status` command to the quickstart's "Try with a real provider" section.** Round 1 P3 item #20 recommended this. I re-endorse it as the simplest way to give the user confidence that their API key is configured correctly before running a real deliberation. Place it between the `export ANTHROPIC_API_KEY` line and the `conversus decide` line.

## Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus/docs/index.md` -- index page with "4 competition modes" claim and `pip install` discrepancy
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/quickstart.md` -- primary evaluation target for first-contact experience
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/cli.md` -- CLI reference with bare `conversus` commands (no `uv run` prefix)
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/modes.md` -- 8 modes documented, contradicting index page's 4
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/sdk.md` -- async-first Quick Start that fails the copy-paste test
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/config-reference.md` -- complete and well-structured; no new issues
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/guided-workflow.md` -- slash command workflow, well-written once you know the context
- `<HOME>/code/payer-index-mono/conversus/docs/user-guide/mcp-setup.md` -- MCP setup guide, good troubleshooting section
- `<HOME>/code/payer-index-mono/conversus/docs/developer-guide/architecture.md` -- clear three-layer diagram, good data flow
- `<HOME>/code/payer-index-mono/conversus/docs/developer-guide/building-plugins.md` -- solid but missing wiring steps (Round 1 captured)
- `<HOME>/code/payer-index-mono/conversus/docs/developer-guide/building-domains.md` -- promises 5-stage lifecycle, delivers 2 stages (Round 1 captured)
- `<HOME>/code/payer-index-mono/conversus/docs/api/schemas/construction.md` -- mkdocstrings stub, blank on GitHub
- `<HOME>/code/payer-index-mono/conversus/docs/api/plugins/base.md` -- mkdocstrings stub with member list, blank on GitHub
- `<HOME>/code/payer-index-mono/conversus/docs/api/domains/base.md` -- mkdocstrings stub without member list, blank on GitHub
- `<HOME>/code/payer-index-mono/conversus/specs/031-docs-and-vercel-compliance/conversus-review/round-1/summary/final.md` -- Round 1 synthesis with 7 convergence points and 7 remaining disputes
