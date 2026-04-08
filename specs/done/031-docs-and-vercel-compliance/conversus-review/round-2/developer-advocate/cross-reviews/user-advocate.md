# Developer-Advocate Cross-Review of User-Advocate -- Round 2

## Dangerous Contradictions

### 1. The `pip install conversus` vs. `uv sync` discrepancy is worse than either of us acknowledged

User-advocate identifies in Missed Opportunity #2 that the index page shows `pip install conversus` while the quickstart shows `git clone` + `uv sync`, and calls this "a lie that will fail on first contact" if no PyPI package exists. I did not flag this at all in my Round 2 review. The danger is compounded by my own finding (developer-advocate, Missed Opportunity #4) about import namespace ambiguity between `engine` and `conversus` -- if there *is* a PyPI package called `conversus`, does it install both `engine` and `conversus` namespaces? Or only `conversus`? A developer who installs via `pip install conversus` and then encounters `from engine import Deliberation` in the SDK guide will hit an `ImportError` and have no idea whether they installed the wrong package or missed a dependency. User-advocate scoped this as a user onboarding problem; I am escalating it as a developer integration hazard as well. The install path, the import namespace, and the SDK examples must all tell a consistent story. Neither of our Round 2 reviews connected these three dots.

**Risk**: A developer who enters the ecosystem through `pip install conversus` (index page) rather than `git clone` + `uv sync` (quickstart) may end up with incomplete packages, broken imports, and no diagnostic path. The Round 1 synthesis did not identify this because all three agents evaluated the quickstart as the primary entry point and treated the index page as ancillary.

### 2. User-advocate's `uv run` prefix recommendation could create a second consistency problem while solving the first

User-advocate's Missed Opportunity #3 correctly identifies that the quickstart uses `uv run conversus ...` while the CLI reference uses bare `conversus ...`. The proposed fix (add a note to the top of cli.md) is the right minimum intervention. However, user-advocate's option (b) -- adding `uv run` to all CLI reference examples -- would contradict the `pip install conversus` path on the index page, where the user *would* have `conversus` on their system PATH. My Round 2 review proposes practical plugin wiring steps (developer-advocate, Actionable Recommendation #2) that include `pip install -e .` for local development. If the CLI reference adds `uv run` to all examples, a developer who followed the `pip install -e .` path would see unnecessary prefixes everywhere.

User-advocate's option (a) -- a single note at the top of cli.md -- is the only safe fix. Options (b) and (c) each create new contradictions depending on which install path the reader followed. I want to explicitly endorse option (a) and flag options (b) and (c) as dangerous.

**Risk**: Solving the `uv run` inconsistency by adding it everywhere would embed a `uv`-specific assumption into the CLI reference, breaking it for developers who installed via pip or `pip install -e .`. The fix must be install-method-agnostic.

### 3. The "visual break before slash commands" recommendation may overcorrect and fragment the quickstart

User-advocate's Actionable Recommendation #3 strengthens the Round 1 P1 #3 convergence by proposing a heading ("## Try the guided workflow (in your AI editor)") and a structural break. I agree with the diagnosis -- the context switch from terminal commands to slash commands is genuinely broken (my Round 2 review carries this forward as developer-advocate Actionable Recommendation #3). But the structural fix matters: if the quickstart adds a new H2 heading for the guided workflow, it visually signals "this is still the quickstart." A developer who has never used Claude Code or Cursor might spend time trying to set up MCP when all they wanted was to run `conversus decide` from their terminal.

My concern is that elevating the slash command section to a full heading within the quickstart promotes it to co-equal status with the CLI path. The quickstart should complete the CLI path first (including the "What just happened" explanation and the "Try with a real provider" section) and then offer the guided workflow as an optional, clearly-labeled appendix or a cross-link to `guided-workflow.md`. User-advocate's framing ("in your AI editor" parenthetical in the heading) partially mitigates this, but the structural promotion within the quickstart still risks confusing developers who do not use AI editors.

**Risk**: A developer reading the quickstart to learn the CLI tool encounters a mid-page heading that redirects them to a different execution environment. The fix should separate paths more clearly, not merge them under a shared quickstart umbrella.

## Tensions

### 1. Index page comprehensiveness vs. quickstart as canonical entry

User-advocate's Missed Opportunity #1 treats the index page as "the real front door" and identifies three problems (4 modes, pip install, no prerequisites). My Round 2 review does not discuss the index page at all -- I focused entirely on developer-facing guides. The tension is about which page is the canonical entry point. If the index page is the front door, it needs to be accurate and self-sufficient. If the quickstart is the front door, the index page is a signpost that should be minimal and link-heavy.

User-advocate wants the index page to be correct and complete. I implicitly treated it as a marketing surface that developers skip. The right answer is probably user-advocate's -- a developer arriving from a search engine or a README link will land on the index page first. But the fix should make the index page a reliable signpost (correct numbers, correct install command, link to quickstart) rather than a redundant quickstart. User-advocate's recommendations are consistent with this signpost model; I want to make it explicit so future edits do not bloat the index page.

### 2. Example output in the quickstart vs. keeping it minimal

User-advocate's Missed Opportunity #4 proposes adding example output to the quickstart's "What just happened" section. My Round 2 review does not address quickstart output at all. The tension is real: showing output helps the user verify success (user-advocate's goal), but terminal output for a multi-phase deliberation system could be 50+ lines, and abbreviated output requires maintenance every time the output format changes.

I lean toward user-advocate's position here but with a constraint: the output block should be explicitly marked as approximate (`# Output (abbreviated, your results may vary)`) and should show only the phase markers and final verdict, not the full agent-by-agent output. This keeps maintenance burden low while giving the user a success signal.

### 3. Sync-first SDK framing: "copy-paste test" vs. "architectural truth"

User-advocate's Off-Base Assumption #2 reframes the sync-first SDK resolution around a "copy-paste test" -- the first code block should be runnable as `python script.py`. My Round 2 review (developer-advocate, Off-Base Assumption #1) concedes sync-first ordering but insists the note must say "Event subscriptions require async context." These are compatible positions, but the underlying tension remains: user-advocate optimizes for first-contact success of casual users, while I optimize for architectural correctness that serves long-term integrators.

User-advocate's "copy-paste test" framing is actually stronger than the "trust violation" argument from Round 1 because it generalizes: every first example in the docs should be self-contained and runnable. I endorse this principle. The tension resolves if both the `asyncio.run()` wrapper *and* the async-context note are present, which both reviews recommend. The remaining question is emphasis -- user-advocate would bury the async note; I would make it visually prominent. A bold inline note ("Note: Event subscriptions require async context") is the compromise.

### 4. Error recovery in the quickstart: scope of micro-hints

User-advocate's Missed Opportunity #5 expands the quickstart troubleshooting scope to cover `uv` not being installed, proposing to extend the micro-hint to include a URL to uv's documentation. My Round 2 review (developer-advocate, Actionable Recommendation #3) focuses on the slash command context switch without addressing install failures. User-advocate's expansion is reasonable for the user audience, but every additional micro-hint inches the quickstart toward the "troubleshooting section" that code-verifier objected to in Round 1.

The tension is between thoroughness and brevity. User-advocate's specific proposal -- changing the comment from `# Requires Python 3.12+. Alternative: pip install -e .` to `# Requires Python 3.12+ and uv (https://docs.astral.sh/uv/). Alternative: pip install -e .` -- is exactly one URL addition and stays within the micro-hint contract. I support it. But this should be the ceiling, not the floor. Any further troubleshooting belongs on a dedicated page.

### 5. The MkDocs vs. GitHub reading surface question

User-advocate's Off-Base Assumption #3 pushes for a resolution to the "raw Markdown vs. MkDocs" systemic contradiction that the Round 1 synthesis identified but left unresolved. User-advocate proposes a pragmatic fix: state that MkDocs is the primary surface and tell users how to build locally. My Round 2 review does not address this directly, though my Missed Opportunity #4 (import namespace ambiguity) is a symptom of the same problem -- the SDK page's imports make more sense with MkDocs cross-references than in raw Markdown.

I agree with user-advocate's recommendation (P2 #7) to add a sentence declaring MkDocs as the primary reading surface. This unblocks the API reference pages, which all three agents agreed need narrative prose but which will always be second-class on GitHub due to mkdocstrings. Stating the primary surface explicitly prevents future review cycles from re-litigating this question.

## Safe Agreements

### 1. The end-to-end domain tutorial is the highest-impact developer-facing change

User-advocate's review acknowledges the building-domains gap (referenced in Alignment #5 and Off-Base Assumption #3 under the parallel tracks discussion) without disputing its substance or priority within the developer track. My Round 2 review (developer-advocate, Actionable Recommendation #1) carries this forward as the single highest-impact change for the developer audience. Both reviews agree on the gap, the scope (5-stage lifecycle demonstrated as a connected flow), and the approach (parallel implementation alongside onboarding fixes). There is no tension here.

### 2. The `conversus status` command belongs in the quickstart

User-advocate's Actionable Recommendation #10 re-endorses adding `conversus status` after the "Try with a real provider" section. My Round 2 review (developer-advocate, Actionable Recommendation #9) independently carries this forward. Both reviews agree on placement, purpose (credential verification before running a real deliberation), and priority (P3). This is a small change with outsized confidence-building value for both audiences.

### 3. All Round 1 convergence points remain stable

Both reviews affirm all 7 Round 1 convergence points without reversal. User-advocate's Alignment section explicitly lists all 7 and marks them "well-resolved." My Alignment section affirms the same 7. Neither review introduces new challenges to any converged item. The convergence is durable heading into Round 3.

### 4. Plugin wiring and config-reference `plugins:` key are complementary, not alternative

User-advocate's Alignment #3 supports the `plugins:` key in config-reference.md. My Round 2 review (developer-advocate, Actionable Recommendation #2) separately advocates for updating the "Dynamic loading" section in building-plugins.md with developer-facing wiring steps. User-advocate's review does not contest this. Both changes address different questions -- config-reference says *what* the YAML accepts; building-plugins says *how* to make code loadable -- and both reviews implicitly or explicitly acknowledge they are needed together.
