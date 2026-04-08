# Code-Verifier -- Round 2 Revision (Iteration 1)

## Recommendation Dispositions

### Recommendation 1 (P1): Fix the `run` command epilog `--phase synthesis` example
**Status: Modified**

The core finding stands -- `engine/cli/__init__.py` L95 shows `--phase synthesis` but Click constrains the choice to `["all", "review"]` at L110-113. This is a confirmed code bug. Both cross-reviewers accept the finding and validate it as the strongest new discovery in Round 2.

Developer-advocate's Dangerous Contradiction #2 raises a legitimate point: changing the epilog from `--phase synthesis` to `--phase review` replaces a broken example with a confusing one, since `--phase review` behavior is itself undocumented. I accept this coupling argument. The epilog fix should ship alongside Recommendation 9 (document what `--phase review` produces). Neither fix is useful in isolation -- a broken example and an unexplained example are both user traps.

**Modification**: Elevate Recommendation 9 to P1 and couple it with this fix. The epilog change and the `--phase review` behavior documentation are now a single deliverable. Credit to developer-advocate for identifying the compounding effect.

### Recommendation 2 (P1): Fix scaffolds endpoint to glob YAML files (Round 1 CV-2, converged)
**Status: Surviving**

No cross-reviewer challenges this. Both confirm the code at `api.py` L208 globs `*.json` only while `load_scaffold()` at `base.py` L144-171 handles `.yml`, `.yaml`, and `.json`. Round 1 bilateral convergence, re-confirmed in both cross-reviews. Proceeds unchanged.

### Recommendation 3 (P1): Add `decide` 4-mode clarifying note to cli.md (Round 1 CV-1, converged)
**Status: Modified**

User-advocate's cross-review (Tension #1) correctly notes that the Round 1 fix was scoped too narrowly as "change 4 to 8." The index page Quick Links section at L61-63 explicitly enumerates four modes by name (`Cooperative, winner-take-all, prisoner's dilemma, red-blue`). Changing the count alone creates a new inconsistency. I verified the index page source in my cross-review of user-advocate and confirmed this.

**Modification**: The scope of this fix must include the index page Quick Links enumeration, not just the modes count in the Three Layers table. This was already implicit in the Round 1 convergence but user-advocate correctly identified the enumeration list as an overlooked surface. I also agree with my own cross-review finding that the card title `:material-sword-cross: **[Competition Modes]**` should change to "Deliberation Modes" for terminology consistency.

### Recommendation 4 (P2): Document the three-way provider default mismatch
**Status: Modified**

Both cross-reviewers engage substantively with this finding. User-advocate's Dangerous Contradiction #1 argues that a prose note in config-reference.md is insufficient because users do not read linearly, and proposes P1 elevation with a "visually distinct warning box." Developer-advocate's Dangerous Contradiction #1 agrees the finding is accurate but argues the proposed text "reads as informational rather than alarming" and also recommends a warning callout.

I accept the presentation argument: a parenthetical about CLI behavior buried in the `provider:` field description will not register with a user scanning the config reference. The three-way default (`EngineConfig` defaults to `"anthropic"` at `config.py` L77, CLI defaults to `"mock"` at `cli/__init__.py` L101, SDK defaults to `"mock"` at `sdk.py` L155) is a behavioral trap, not an informational footnote.

However, I do not accept P1 elevation. The provider default mismatch is confusing but produces a safe failure mode: the user gets mock output instead of real API calls. No money is spent, no incorrect results are generated. P2 with stronger presentation is the right call.

**Modification**: The documentation fix should use an admonition/warning callout (not inline prose) at the `provider:` field in config-reference.md. Text: "Warning: When `provider` is omitted, the config defaults to `anthropic`. However, CLI `--provider` defaults to `mock` and takes full precedence over the config file. If you omit both, the CLI wins and you get mock output. Set `provider:` explicitly in your config to avoid surprises." Credit to user-advocate and developer-advocate for the callout-box framing.

Developer-advocate also suggests the deeper fix is to have the CLI consult `config.provider` as a fallback before defaulting to `mock`, collapsing the three-way mismatch to a two-way one. I agree this is the correct long-term solution and should be filed as a follow-up code issue, but it is outside spec 031's documentation scope.

### Recommendation 5 (P2): Add `plugins:` key to config-reference.md (Round 1 CV-B, converged)
**Status: Surviving**

No cross-reviewer challenges this. Both confirm the `load_plugins()` signature at `plugins/base.py` L229-295 with `name`, `package`, and `config` sub-keys. Round 1 unanimous convergence, unchanged.

### Recommendation 6 (P2): Add narrative prose and `members:` list to API reference pages (Round 1 CV-A, converged)
**Status: Modified**

Developer-advocate's Tension #4 raises a valid concern: the `members:` list is a MkDocs directive option that renders as nothing on GitHub. The narrative prose is visible on GitHub, but without autodoc output, the page becomes an introductory paragraph followed by an opaque `:::` block. Developer-advocate proposes including a plain-text summary of key classes and their relationships in the narrative prose itself, so GitHub readers get a useful class listing regardless of rendering surface.

I accept this. My original recommendation specified the `members:` list items (`DomainPlugin`, `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, `Scaffold`, `VariableExtractor`, `load_scaffold`, `DomainStore`, `JSONLStore`, `SQLiteStore`) but focused on the MkDocs rendering. The narrative prose should include these class names with one-sentence descriptions, making the page useful on both surfaces.

User-advocate's Tension #5 proposes declaring MkDocs as the primary reading surface and including `uv run mkdocs serve` build instructions. I accept the declaration as useful policy but believe both surfaces must be supported, not one declared "primary" and the other abandoned. The plain-text class summary in narrative prose serves both.

**Modification**: The narrative prose above the `:::` directive should include a brief class catalog (name + one-sentence purpose) for each member, not just a textual introduction. This makes the page functional on GitHub without autodoc rendering. Credit to developer-advocate for the dual-surface argument.

### Recommendation 7 (P2): Add `Deliberation.cost_estimate` nullability note to SDK docs
**Status: Modified**

User-advocate's Dangerous Contradiction #3 and developer-advocate's Dangerous Contradiction #3 both argue this is part of a systemic pattern: the SDK documentation consistently presents nullable returns and exception-raising functions as happy paths. Both propose treating "happy-path-only SDK documentation" as a systemic issue rather than fixing individual instances.

I accept the pattern identification. However, I disagree with the proposed remedy of a single sweeping audit. The systemic framing is correct for understanding the problem; the fix should still be instance-specific. Each nullable return or exception-raising function has different failure semantics (returning `None` vs. raising `ValueError` vs. raising `RuntimeError`). A blanket "error handling" section that says "check for None and catch exceptions" is less useful than inline annotations at each call site in the docs.

**Modification**: This recommendation now includes a broader scope: in addition to the `cost_estimate` nullability note, add inline annotations for all SDK functions shown in `sdk.md` whose return types include `| None` or whose implementations raise exceptions. The specific instances I have source-verified are: `Deliberation.cost_estimate` (returns `None`), `construct_objective()` (raises `ValueError`, `RuntimeError`), and `classify()` (calls `classify_decision_type` which raises `ValueError`). This absorbs Recommendation 10 into this item. Credit to both cross-reviewers for identifying the pattern.

### Recommendation 8 (P2): Document `estimate_cost_usd()` in SDK guide (Round 1 CV-7, converged)
**Status: Surviving**

No cross-reviewer challenges this. Round 1 bilateral convergence. The function at `engine/cost.py` L106-158 is fully implemented and unexposed in documentation. Proceeds unchanged.

### Recommendation 9 (P2 -> P1): Document what `--phase review` actually produces
**Status: Modified (priority elevated)**

Developer-advocate's Dangerous Contradiction #2 argues this must ship with Recommendation 1 (the epilog fix). User-advocate's Dangerous Contradiction #2 argues the epilog bug and `--phase review` gap "compound into a broken self-help loop" where a user tries the invalid `--phase synthesis`, falls back to `--phase review`, and cannot interpret the output.

I accept the compounding argument. The `run_engine()` function at `engine/run.py` L248-256 confirms `--phase review` runs `run_phase1()` only, producing agent reviews without cross-review, revision, disputes, or synthesis. Users need to know what output files to expect.

**Modification**: Elevated from P2 to P1. Coupled with Recommendation 1 as a single deliverable. The documentation should state: "`--phase review` runs Phase 1 only (individual agent reviews). Output: one review file per agent. Cross-review, revision, dispute, and synthesis phases are skipped." Credit to developer-advocate for the coupling argument and user-advocate for the compounding-loop framing.

### Recommendation 10 (P3): Note `construct_objective` failure modes in SDK docs
**Status: Withdrawn (absorbed)**

Absorbed into the modified Recommendation 7, which now covers all SDK happy-path-only documentation instances as a single deliverable. The specific `construct_objective()` failure modes (`NonInteractiveGapFiller` raises `RuntimeError` at `construction.py` L167-171; `classify_decision_type` raises `ValueError` at L417-421) will be documented as inline annotations alongside the `cost_estimate` nullability note.

## New Recommendations

### New-1 (P1): Reconcile `pip install conversus` on index page with `git clone` + `uv sync` in quickstart

User-advocate's Round 2 Missed Opportunity #1 identifies that `docs/index.md` L29 shows `pip install conversus` while the quickstart uses `git clone` + `uv sync`. In my cross-review of user-advocate, I confirmed this finding and identified it as potentially the most dangerous first-contact failure in the documentation. The `pyproject.toml` wires `conversus = "engine.cli:cli"` as the entry point, which only works after a local install. If there is no published PyPI package, then `pip install conversus` either fails or installs an unrelated package.

This was not in the Round 1 pipeline. Neither my Round 2 review nor developer-advocate's Round 2 review examined the index page. User-advocate is the sole discoverer. I have not verified whether a `conversus` package exists on PyPI, but the structural evidence (quickstart uses `git clone`, pyproject.toml uses local entry points) strongly suggests there is no published package.

**Fix**: Determine whether a PyPI package exists. If not, replace `pip install conversus` on the index page with the quickstart's `git clone` + `uv sync` flow, or at minimum replace it with `pip install -e .` (local editable install) consistent with the quickstart micro-hint. Credit to user-advocate for this finding.

### New-2 (P2): Reconcile `uv run conversus` (quickstart) vs. bare `conversus` (CLI reference)

User-advocate's Round 2 Missed Opportunity #3 identifies that every example in `cli.md` uses bare `conversus` while the quickstart consistently uses `uv run conversus`. In my cross-review of user-advocate, I confirmed this: cli.md L9-21, L39-49, L67-71, L98-99, L111-115, L122-123 all use bare `conversus`; quickstart L7, L19, L48, L51, L85 all use `uv run conversus`.

A user who follows the quickstart's install method (`uv sync`) and then consults the CLI reference will omit `uv run` and get "command not found." This interacts with the epilog bug (Recommendation 1) and the provider default mismatch (Recommendation 4) to create a cascading confusion path.

**Fix**: Choose one convention and apply it consistently. If `uv sync` is the install method, then `uv run conversus` is the invocation. If `pip install -e .` is also documented, bare `conversus` works. Add a note at the top of cli.md explaining both invocation styles. Credit to user-advocate for this finding.

## Position Summary

This revision processes feedback from both cross-reviewers against the 10 recommendations in my Round 2 review. No Round 1 concessions are reversed. One recommendation is withdrawn (absorbed into a broader item), two are elevated in priority, five are modified to incorporate cross-reviewer feedback, and two survive unchanged. Two new recommendations emerge from user-advocate findings that I verified in my cross-review but did not independently discover.

The most significant change is the coupling of Recommendations 1 and 9 into a single P1 deliverable. Developer-advocate and user-advocate independently identified that fixing the epilog `--phase synthesis` bug without documenting what `--phase review` produces creates a new trap. The compounding-loop argument -- user sees invalid example, falls back to the only other valid value, gets unexplained partial output -- is persuasive and well-sourced from both perspectives. I accept the elevation.

The second significant change is the systemic treatment of SDK happy-path-only documentation. Both cross-reviewers argue that my individual fixes (P2 for `cost_estimate` nullability, P3 for `construct_objective` failure modes) miss the pattern. They are right about the pattern but wrong about the remedy: a single "error handling" section is less effective than inline annotations at each documented call site. My modification absorbs both instances into a single P2 item that adds failure-mode annotations to all SDK examples in `sdk.md`, targeting the three source-verified instances (`cost_estimate`, `construct_objective`, `classify`). This captures the systemic concern while keeping the fixes precise and verifiable.

Finally, the two new recommendations (index page install command, `uv run` prefix consistency) address findings by user-advocate that fall squarely within code-verifier's mandate: they are cases where documentation commands diverge from what the codebase actually supports. I confirmed both in my cross-review of user-advocate and believe they warrant inclusion in the final implementation plan. The index page `pip install conversus` command is particularly urgent because it is the literal first command a new user encounters.
