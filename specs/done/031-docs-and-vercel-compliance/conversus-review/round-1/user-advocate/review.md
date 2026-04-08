# User-Advocate Review: Conversus Documentation Suite

**Reviewer role:** New user who has never seen conversus, evaluating the documentation for first-time usability.

**Target:** All user-guide, developer-guide, and API documentation files under `conversus/docs/`.

---

## Executive Summary

Conversus is a multi-agent deliberation framework that uses game-theory-informed modes to let AI agents compete and collaborate on decisions. The documentation suite covers installation, CLI usage, SDK integration, configuration, architecture, and extensibility (plugins, domains). From a new user's perspective, the quickstart is strong -- it gets you from zero to a working mock deliberation in three commands, and the "What just happened" section immediately orients you on the pipeline. The mode descriptions are the highlight: each one opens with a bold imperative sentence, gives a clear "when to use" heuristic, and provides a copy-pasteable YAML block.

However, the documentation has significant gaps that would stall a new user after the initial quickstart euphoria wears off. The guided workflow (the primary interactive path) references Claude Code slash commands that are never explained as a concept -- a user unfamiliar with Claude Code would not know what `/conversus define` means or where to type it. The SDK doc jumps straight to async Python with no sync-first example at the top, which will confuse the majority of Python users who are not already comfortable with `asyncio`. The config reference is thorough but has no "working minimal example you can copy and modify" section. The API reference pages for construction, plugins/base, and domains/base are essentially empty -- they contain only `mkdocstrings` directives that will render in MkDocs but read as blank stubs in raw Markdown, which means anyone reading the docs on GitHub (the most common path for new users evaluating a project) gets nothing.

The single most important recommendation: add a "Prerequisites and Concepts" section before the guided workflow that explains what Claude Code slash commands are, what `uv` is, and what "MCP" means, so users without that context can follow the primary workflow path without hitting a wall.

---

## Alignment

- **[Mock provider for zero-cost exploration]** (quickstart.md, L19-22): The quickstart defaults to `--provider mock` on the very first command, letting a new user see the full pipeline output without configuring any API key. This removes the single biggest friction point in LLM tool onboarding.

- **[Imperative mode descriptions]** (modes.md, L5-8, L22-25, L42-44, L60-62): Each mode opens with a bold imperative ("Find common ground," "Pick the best option," "Figure out who owns what," "Stress-test the plan") that immediately communicates intent without jargon. The "When to use" bullets that follow give concrete scenarios. A new user can scan all 8 modes in under 2 minutes and identify their match.

- **[Cost estimation before execution]** (cli.md, L63-91; config-reference.md, L149-161): Both the `conversus validate` command and the SDK's `cost_estimate` property let users see exactly how many LLM launches will occur before spending money. The formula table (N agents, I iterations) is clear and the worked example (3 agents = 16 launches) makes it concrete.

- **[Auth resolution order]** (cli.md, L127-135): The three-step credential resolution (env var, OAuth store, error with instructions) is documented explicitly. A new user who sets `ANTHROPIC_API_KEY` will succeed immediately; one who does not gets actionable error output. No ambiguity.

- **[Progressive disclosure in the guided workflow]** (guided-workflow.md, L7-13): The workflow table showing step, command, and output artifact is an excellent orientation device. Each step consumes the previous step's artifact, making the dependency chain visible.

---

## Missed Opportunities

- **[No "What is conversus?" one-paragraph explanation at the top of the quickstart]**: The quickstart jumps directly to `git clone`. A new user landing on this page from a search result or GitHub link has no context for what they are about to install. The index.md has a one-liner, but quickstart.md does not link to it or reproduce it. A single paragraph saying "Conversus is X, it does Y, you give it Z and get back W" would prevent the "why am I installing this?" moment. **Impact: high.**

- **[No explanation of `uv` for users who do not have it]**: The quickstart (L7) and SDK doc (L8) both use `uv sync` and `uv run` without explaining what `uv` is, how to install it, or offering a `pip` fallback. The index.md (L29-37) shows `pip install conversus` as an alternative, but the quickstart -- the page most new users will land on -- does not. A user on a corporate laptop without `uv` installed will fail on the very first command. **Impact: high.**

- **[Guided workflow assumes Claude Code knowledge]**: The guided workflow (guided-workflow.md, L1-4) says these are "Claude Code skill subcommands" but never defines what that means. The commands are prefixed with `/` (L19, L39, L53, L73, L75, L101), which looks like a terminal command but is not -- it is a slash command typed inside an AI coding assistant. A user who tries to run `/conversus define` in their shell will get `zsh: no such file or directory`. There is no "Prerequisites" section explaining that you need Claude Code (or an MCP-compatible editor) and how to set it up. The MCP setup page exists but is not linked from the guided workflow page. **Impact: high.**

- **[No troubleshooting section in the quickstart]**: The quickstart has no "Common problems" section. Likely failure modes include: `uv` not installed, Python < 3.12, missing API key when switching from mock to real provider, and `git clone` failing because the repo is private. The MCP setup page (L109-113) has a small troubleshooting section, but the quickstart does not. **Impact: medium.**

- **[SDK doc starts with async, not sync]**: The SDK quick start (sdk.md, L13-25) shows `await Deliberation(...).run()` as the first example. The sync wrapper using `asyncio.run()` is buried at line 163. Most Python developers encountering this for the first time will try to paste the first example into a script, get a `SyntaxError` outside an async context, and be confused. The sync pattern should be the first example, with async as the "advanced" pattern below. **Impact: medium.**

- **[API reference pages are empty stubs when read as Markdown]**: The construction.md (L1-24), plugins/base.md (L1-18), and domains/base.md (L1-6) files contain only `mkdocstrings` directives (`::: conversus.schemas.construction`). These render correctly in a built MkDocs site, but anyone reading the docs on GitHub -- the most common discovery path for new open-source projects -- sees effectively blank pages. There should be at minimum a prose summary of what each module does and its key classes, even if the auto-generated API docs supplement it. **Impact: medium.**

- **[No "Next steps" at the end of the quickstart]**: The quickstart ends abruptly after the config file example (L88-89) with a link to the config reference. There is no signpost saying "Now that you have run your first deliberation, here is what to explore next" with links to modes, the guided workflow, the SDK, or the developer guide. A new user finishes the quickstart and has to figure out where to go on their own. **Impact: low.**

- **[Config reference lacks a "copy this and modify it" starter template]**: The config reference (config-reference.md) has a full schema block (L7-73) and common configs at the bottom (L164-196), but the full schema block includes every optional field with comments, making it intimidating. A minimal "starter template" section at the very top -- just mode, target, output, and two agents, nothing else -- would give users a safe starting point. The "Common configs" section at the bottom is close but is not presented as "start here." **Impact: low.**

---

## Off-Base Assumptions

- **[Users know what `uv` is]**: The quickstart (L7) and SDK (L8) assume the user has `uv` installed and knows what it does. `uv` is a relatively new Python package manager (by Astral) and is not yet ubiquitous. Many Python developers still use `pip`, `poetry`, or `conda`. The documentation should either explain `uv` briefly with an install link or provide `pip` alternatives alongside every `uv` command. The index.md partially addresses this (L29-30: `pip install conversus`) but the quickstart and SDK do not.

- **[Users understand "MCP" and "Claude Code slash commands"]**: The guided workflow (guided-workflow.md, L3-4) and MCP setup page (mcp-setup.md, L1-2) assume users know what the Model Context Protocol is and what Claude Code skill subcommands look like. MCP is a protocol that most developers have not encountered. The documentation uses terms like "MCP-compatible editor" (quickstart.md, L59) without defining them. For a framework targeting decision-making across teams (not just AI tool developers), this is a significant accessibility gap.

- **[The index.md "4 competition modes" claim]**: The index page (index.md, L20) says "4 competition modes" and the quick links section (L62) says "Cooperative, winner-take-all, prisoner's dilemma, red-blue." But the modes page (modes.md, L3) documents 8 modes, and the config reference (config-reference.md, L11-12) lists all 8. This is a factual inconsistency that will confuse users trying to understand the scope of the tool. Either the index page is outdated or the mode count needs to be corrected.

---

## Actionable Recommendations

1. **Add prerequisites section to quickstart** (Priority: P1)
   - **Current state**: quickstart.md jumps directly to `git clone` (L5-8) with no prerequisites.
   - **Proposed change**: Add a "Prerequisites" section before "Install" that lists: Python 3.12+, `uv` (with install link: `curl -LsSf https://astral.sh/uv/install.sh | sh`, or `pip` as fallback), and optionally an API key for real providers. Include a `pip install conversus` alternative path.
   - **Rationale**: The two most likely first-command failures are "uv not found" and "Python version too old." Both are preventable with a prerequisites section.
   - **Risk if ignored**: Users without `uv` fail on their first command and may abandon the tool.

2. **Explain slash commands before the guided workflow** (Priority: P1)
   - **Current state**: guided-workflow.md (L3-4) references "Claude Code skill subcommands" without explanation. quickstart.md (L59) says "In Claude Code or any MCP-compatible editor" without defining either.
   - **Proposed change**: Add a 2-3 sentence explanation at the top of guided-workflow.md: "The guided workflow uses slash commands inside an AI coding assistant (like Claude Code or Cursor). These are not terminal commands -- you type them in the assistant's chat input. To set up your editor, see [MCP Setup](mcp-setup.md)." Also add the same context before the `/conversus` block in quickstart.md (L58-64).
   - **Rationale**: A user who does not know what Claude Code is will try to run `/conversus define` in their terminal and fail with a confusing shell error.
   - **Risk if ignored**: The entire guided workflow path is unusable for users unfamiliar with Claude Code or MCP.

3. **Fix "4 modes" claim on index page** (Priority: P1)
   - **Current state**: index.md (L20) says "4 competition modes" and the quick links (L62) list only 4. modes.md documents 8. config-reference.md lists 8.
   - **Proposed change**: Update index.md L20 to "8 deliberation modes" and L62 to list all 8 (or say "8 modes including cooperative, winner-take-all, and more").
   - **Rationale**: A factual inconsistency on the landing page undermines trust in the documentation's accuracy.
   - **Risk if ignored**: Users who read the index first will believe only 4 modes exist and may not discover modes that better fit their problem.

4. **Put sync example first in SDK doc** (Priority: P2)
   - **Current state**: sdk.md (L13-25) shows `await` as the first example. The `asyncio.run()` sync wrapper is at L163-169.
   - **Proposed change**: Move the sync pattern to be the first "Quick start" example. Keep the async pattern as a second example labeled "Async usage." Most first-time SDK users will be writing scripts, not async applications.
   - **Rationale**: The majority of Python developers will try the first example in a plain script. `await` outside an async function is a `SyntaxError`.
   - **Risk if ignored**: New SDK users hit a syntax error on their first attempt, creating a negative first impression.

5. **Add troubleshooting section to quickstart** (Priority: P2)
   - **Current state**: No troubleshooting in quickstart.md. mcp-setup.md (L107-113) has a small one.
   - **Proposed change**: Add a "Troubleshooting" section at the bottom of quickstart.md covering: `uv` not found (install link), Python version error, `--provider anthropic` without API key (point to `conversus login` or env var), and empty/error output with mock provider.
   - **Rationale**: The quickstart is where most users will hit their first problem. Resolving it on the same page prevents drop-off.
   - **Risk if ignored**: Users who hit a common error will search externally, find nothing (new project), and give up.

6. **Add introductory prose to API reference stubs** (Priority: P2)
   - **Current state**: construction.md, plugins/base.md, and domains/base.md contain only `mkdocstrings` directives that render as empty when read as raw Markdown.
   - **Proposed change**: Add 3-5 sentences above each `:::` directive describing what the module does, its key classes, and a one-line usage example. This ensures GitHub readers get value even without a built MkDocs site.
   - **Rationale**: GitHub is the primary discovery surface for developer tools. Empty pages signal an incomplete or unmaintained project.
   - **Risk if ignored**: Developers evaluating the project via GitHub will see blank API pages and may conclude the project is immature.

7. **Add "Next steps" section to quickstart** (Priority: P2)
   - **Current state**: quickstart.md ends at L89 with a link to config-reference.md and no further guidance.
   - **Proposed change**: Add a "Next steps" section with 3-4 bullets: "Learn about all 8 modes (link)," "Try the guided workflow (link)," "Use the Python SDK (link)," "Set up MCP integration (link)."
   - **Rationale**: Users who complete the quickstart successfully are at peak engagement. A clear next-steps section converts that momentum into deeper adoption.
   - **Risk if ignored**: Users complete the quickstart, do not know where to go next, and do not discover the guided workflow or SDK.

8. **Add "What you will need" context to the guided workflow complete example** (Priority: P3)
   - **Current state**: guided-workflow.md L114-132 shows a complete example but does not specify what must be true before starting (Claude Code open, MCP configured, project directory active).
   - **Proposed change**: Add a "Before you start" note: "This example assumes you have Claude Code open in a project directory with MCP configured (see [MCP Setup](mcp-setup.md))."
   - **Rationale**: The complete example is the most likely copy-paste target. Without context, users will try to run it in the wrong environment.
   - **Risk if ignored**: Minor -- the earlier explanation (if recommendation #2 is adopted) would partially cover this.

9. **Add a minimal "starter config" callout to config reference** (Priority: P3)
   - **Current state**: config-reference.md (L7-73) opens with the full schema including every optional field. "Common configs" appear at L163.
   - **Proposed change**: Add a callout box or "Start here" section at the top with a 6-line minimal config (mode, target, output, two agents with presets) and the sentence: "This is all you need. Everything below is optional."
   - **Rationale**: The full schema is intimidating for first-time config authors. A minimal starting point reduces cognitive load.
   - **Risk if ignored**: Minor -- the common configs section partially serves this purpose, but its placement at the bottom means many users will not reach it.

10. **Cross-link the CLI `decide` command back to modes** (Priority: P3)
    - **Current state**: cli.md (L57) lists mode options as `cooperative, winner-take-all, prisoners-dilemma, red-blue` -- only 4 of the 8 modes. No link to the modes page.
    - **Proposed change**: Update the `--mode` description to say "See [Deliberation Modes](modes.md) for all 8 options" and list all 8 mode names.
    - **Rationale**: Consistency across pages and discoverability of the full mode set.
    - **Risk if ignored**: Users of the `decide` command may not discover modes beyond the 4 listed.

---

## Referenced Documentation

- `conversus/docs/user-guide/quickstart.md` -- sections/lines cited: L5-8, L7, L19-22, L58-64, L88-89
- `conversus/docs/user-guide/cli.md` -- sections/lines cited: L57, L63-91, L127-135, L139-143
- `conversus/docs/user-guide/modes.md` -- sections/lines cited: L3, L5-8, L22-25, L42-44, L60-62
- `conversus/docs/user-guide/sdk.md` -- sections/lines cited: L8, L13-25, L163-169
- `conversus/docs/user-guide/config-reference.md` -- sections/lines cited: L7-73, L11-12, L149-161, L163-196
- `conversus/docs/user-guide/guided-workflow.md` -- sections/lines cited: L1-4, L3-4, L7-13, L19, L39, L53, L73, L75, L101, L114-132
- `conversus/docs/user-guide/mcp-setup.md` -- sections/lines cited: L1-2, L107-113
- `conversus/docs/user-guide/web-interface.md` -- sections/lines cited: (read for completeness, not directly cited)
- `conversus/docs/index.md` -- sections/lines cited: L20, L29-37, L62
- `conversus/docs/developer-guide/architecture.md` -- sections/lines cited: (read for completeness, no issues found from user perspective)
- `conversus/docs/developer-guide/building-plugins.md` -- sections/lines cited: (read for completeness, no issues found from user perspective)
- `conversus/docs/developer-guide/building-domains.md` -- sections/lines cited: (read for completeness, no issues found from user perspective)
- `conversus/docs/api/schemas/construction.md` -- sections/lines cited: L1-24
- `conversus/docs/api/plugins/base.md` -- sections/lines cited: L1-18
- `conversus/docs/api/domains/base.md` -- sections/lines cited: L1-6
