# User-Advocate Revision -- Round 2, Iteration 1

## Recommendation Dispositions

### Round 2 Recommendation 1: Fix the index page "4 modes" claim across all three locations
**Status**: Modified

Code-verifier's cross-review confirms the three-location inconsistency (Three Layers table, Quick Links enumeration, modes page) and adds a fourth location I missed: the Quick Links card title `:material-sword-cross: **[Competition Modes]**` should also change to "Deliberation Modes" to match the terminology shift. Code-verifier is right -- the card title is part of the same problem. Developer-advocate's cross-review frames the index page as a "signpost" that should be correct and link-heavy rather than a redundant quickstart. I accept that framing; it constrains the fix to accuracy corrections rather than content expansion.

**Modified recommendation**: Fix the index page "4 modes" claim across four locations: (1) Three Layers table line 20 ("4 competition modes" to "8 deliberation modes"), (2) Quick Links card title ("Competition Modes" to "Deliberation Modes"), (3) Quick Links mode list (expand to all 8 or replace with a link to modes.md), (4) add the CLI subset qualifier from Round 1 convergence. Credit: code-verifier for the card title catch.

### Round 2 Recommendation 2: Resolve the `pip install conversus` vs. `uv sync` discrepancy
**Status**: Surviving

Code-verifier's cross-review elevates this from "discrepancy" to "the single most dangerous first-contact failure in the documentation suite" and connects it to the import namespace confusion: if a user `pip install`s a different `conversus` package from PyPI and then encounters `from engine import Deliberation`, they hit an `ImportError` with no diagnostic path. Developer-advocate independently escalates it further by noting the `engine` vs. `conversus` import namespace ambiguity compounds the problem. Both cross-reviews validate this as P1 without modification. The recommendation stands as originally stated, strengthened by both cross-reviews' analysis.

### Round 2 Recommendation 3: Add a visual break and explicit context-switch before slash commands
**Status**: Modified

Developer-advocate's cross-review raises a legitimate concern: elevating the slash command section to a full H2 heading within the quickstart "promotes it to co-equal status with the CLI path" and may confuse developers who do not use AI editors. The concern is that a mid-page heading redirecting to a different execution environment fragments the quickstart. Code-verifier supports the heading change without reservation.

I accept developer-advocate's concern in part. The quickstart should complete the CLI path (including "What just happened" and "Try with a real provider") before introducing the guided workflow. However, the heading change is still necessary because the code comment is genuinely invisible. The modification is about placement and wording, not about removing the structural signal.

**Modified recommendation**: Keep the heading ("## Try the guided workflow (in your AI editor)") but ensure it appears after the CLI path is complete, not mid-flow. The heading itself serves as both a context switch signal and an opt-out point -- a developer who does not use AI editors can stop reading. The 2-sentence explanation remains: "The following commands are slash commands for AI coding assistants like Claude Code or Cursor. They are not terminal commands. See [MCP Setup](mcp-setup.md) to configure your editor."

### Round 2 Recommendation 4: Add a note to cli.md about the `uv run` prefix
**Status**: Modified

Developer-advocate's cross-review explicitly endorses option (a) (a single note at the top of cli.md) and flags options (b) and (c) as dangerous. Option (b) -- adding `uv run` to all CLI examples -- would contradict the `pip install conversus` path. Option (c) -- adding venv activation instructions to the quickstart -- embeds install-method assumptions. I accept this analysis. Options (b) and (c) are withdrawn.

**Modified recommendation**: Add a single note at the top of cli.md: "If you installed via `git clone` + `uv sync`, prefix all commands with `uv run` (e.g., `uv run conversus run config.yml`). If you installed via `pip install -e .`, the commands work directly." This is install-method-agnostic. Credit: developer-advocate for identifying the danger in options (b) and (c).

### Round 2 Recommendation 5: Add example output to the quickstart "What just happened" section
**Status**: Modified

Both cross-reviews accept this as P2 but add the same caveat: the output block must be clearly marked as approximate. Code-verifier notes that "example output is helpful for first-contact verification but becomes a maintenance burden because output format changes with every release." Developer-advocate recommends showing "only the phase markers and final verdict, not the full agent-by-agent output."

**Modified recommendation**: Add an abbreviated output block after the "What just happened" section, showing only phase markers and the final verdict line. Prefix with a comment: `# Output (abbreviated, your results may vary)`. Limit to 8-10 lines. This is a narrower scope than my original "10-15 lines of representative output" and is more maintainable. Credit: code-verifier for the fragility concern, developer-advocate for the scope constraint.

### Round 2 Recommendation 6: Expand the quickstart micro-hint to cover `uv` not being installed
**Status**: Surviving

Developer-advocate explicitly supports this extension and states it should be "the ceiling, not the floor." Code-verifier accepts the extension without objection (Tension #4 in their cross-review). Neither cross-review proposes modifications. The recommendation stands: extend the code comment to `# Requires Python 3.12+ and uv (https://docs.astral.sh/uv/). Alternative: pip install -e .`.

### Round 2 Recommendation 7: State the primary documentation reading surface
**Status**: Surviving

Code-verifier agrees that declaring MkDocs as the primary surface "eliminates the recurring debate about dual-format content" and is "cleaner" than treating the symptom with prose additions. Developer-advocate agrees and adds that the SDK page's imports "make more sense with MkDocs cross-references than in raw Markdown." Neither cross-review proposes modifications. The recommendation stands.

### Round 2 Recommendation 8: Reframe SDK sync-first resolution around the copy-paste test
**Status**: Modified

Code-verifier's cross-review provides the strongest endorsement I could have hoped for: "user-advocate's copy-paste test framing is more precise... This is not a reversal of my position -- it is an acknowledgment that user-advocate's framing provides a durable principle that I should have adopted in my own review." Code-verifier further connects the copy-paste test to their own findings about `cost_estimate` nullability and `construct_objective` failure modes. Developer-advocate accepts the copy-paste test principle and notes it is compatible with their "async-context note" requirement.

The modification incorporates code-verifier's insight: the copy-paste test is not just about the SDK Quick Start but should be stated as a general principle for all first-example blocks in the documentation.

**Modified recommendation**: When implementing the sync-first SDK Quick Start, add `# Save as script.py and run: python script.py` above the first code block. Additionally, state the copy-paste test as a documentation principle in the implementation plan: "Every first code example on a page should be self-contained and runnable without modification." Apply this principle also to the `estimate_cost_usd()` example and any new domain/plugin tutorial examples. Credit: code-verifier for generalizing the principle to cost estimation and construction pipeline examples.

### Round 2 Recommendation 9: Add a "What you will see" section to the modes page
**Status**: Surviving

Neither cross-review addresses this recommendation. It was not challenged or endorsed. The recommendation stands at P3 as originally stated.

### Round 2 Recommendation 10: Add `conversus status` to the quickstart
**Status**: Surviving

Both cross-reviews independently re-endorse this. Developer-advocate calls it "a small change with outsized confidence-building value." Code-verifier confirms it in Safe Agreements. No modifications needed.

## New Recommendations

### New Recommendation 1: Pair the `plugins:` config-reference addition with the building-plugins wiring steps as a single deliverable
**Priority**: P1 (implementation sequencing, not a new content recommendation)

My cross-review of developer-advocate identified a dangerous ordering dependency: if a developer reads building-plugins.md and follows the wiring steps before config-reference.md is updated to include the `plugins:` key, they will look for the `plugins:` field in the config reference, not find it, and lose confidence. Both changes are individually converged (Round 1 Convergence #3 and Round 1 P1 #6). The new recommendation is that these two changes must be explicitly paired in the implementation plan as a single deliverable, not treated as independent items that might ship at different times. This is a process recommendation, not a content recommendation.

### New Recommendation 2: Flag developer-advocate's error handling guidance for code-verifier validation before shipping
**Priority**: P2

My cross-review of developer-advocate identified that Recommendation #5 (error handling guidance for plugin/domain authors) prescribes specific defensive patterns without source-code verification. Developer-advocate states "plugin `execute()` exceptions are caught by the orchestrator, logged at WARNING, and the plugin is skipped" as fact, but this was not verified by code-verifier in Round 2. If the orchestrator's exception handling differs for certain exception types or has changed since the original review, the guidance becomes harmful. This is not a content recommendation -- it is a process flag: code-verifier should verify the claimed exception handling behavior against the current source before the error handling documentation ships. Credit: code-verifier's methodology of source-verifying all claims.

### New Recommendation 3: Connect the three-way provider default mismatch to the config-reference `provider:` field documentation
**Priority**: P2

Code-verifier's Round 2 finding about the three-way default (EngineConfig defaults to `"anthropic"`, CLI defaults to `"mock"`, SDK defaults to `"mock"`) combined with my index page findings creates a scenario where a user who writes a config file omitting `provider:` gets `anthropic` behavior from the config object but `mock` behavior from the CLI. The Round 1 converged fix (a note in cli.md, P2 #10) only reaches users who read cli.md. Code-verifier's recommendation to add a clarifying note in config-reference.md under the `provider:` field is the correct complementary fix -- it catches users who enter the ecosystem through config file authoring rather than CLI documentation. I endorse code-verifier's recommendation #4 and incorporate it here as a user-advocate-endorsed item. Credit: code-verifier for the three-way default discovery and the config-reference placement.

## Position Summary

This revision process has strengthened every one of my Round 2 recommendations. The cross-reviews validated my two strongest new findings -- the `pip install conversus` discrepancy (elevated by both code-verifier and developer-advocate to the single most dangerous documentation defect) and the `uv run` prefix inconsistency (confirmed by code-verifier with line-by-line evidence across all cli.md examples). Two recommendations were modified in ways that made them better: the index page fix now covers four locations instead of three (credit: code-verifier), and the slash command heading change now has clearer placement guidance (credit: developer-advocate's concern about fragmenting the CLI path). The example output recommendation was narrowed to be more maintainable without losing its core purpose.

The most productive outcome of this round is the emergence of the "copy-paste test" as a shared documentation principle. Code-verifier independently recognized its generalizability and connected it to their own findings about nullable returns and exception-raising functions. This means the principle now has backing from both the user-experience and code-verification perspectives, making it durable enough to include in the implementation plan as a standing policy rather than a one-off fix for the SDK Quick Start.

The three new recommendations are all process-oriented rather than content-oriented. They address implementation sequencing (pair the plugins changes), verification dependencies (validate error handling claims before shipping), and gap coverage (add the provider default warning to config-reference.md, not just cli.md). These reflect a shift in my focus from "what is wrong with the docs" to "how do we ensure the fixes land correctly." The content findings are now well-established across all three agents; the remaining risk is in execution -- shipping partial fixes that create new inconsistencies, or shipping guidance that has not been verified against the current codebase. My new recommendations target those execution risks specifically.
