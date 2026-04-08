# Code-Verifier -- Disputes (Round 2, Iteration 1)

## Remaining Disputes

### Dispute 1: User-advocate's New Recommendation 2 over-scopes code-verifier's mandate

User-advocate proposes that developer-advocate's error handling guidance (Recommendation #5) should be "flagged for code-verifier validation before shipping." I have already performed this validation. In my cross-review of developer-advocate, I identified and corrected the factual error: developer-advocate originally wrote "Domain extractor exceptions should return empty dicts rather than raising." I showed that `domains/base.py` L697-708 already catches extractor exceptions with a try/except that logs a warning and skips the failed extractor. Developer-advocate accepted this correction in their revision and updated the recommendation accordingly.

The verification user-advocate is requesting has already happened. Treating it as a "process flag" for future action implies the correction has not yet occurred. If the synthesizer includes this as an open action item, it creates busywork on a resolved finding. The corrected guidance -- "Raise freely; the framework catches and logs; a failed extractor's variables are simply absent from the merged dict" -- is source-verified. It should ship as stated, not be gated on a redundant re-verification pass.

**Position**: Drop user-advocate's New Recommendation 2 from the implementation plan. The verification it describes is complete.

### Dispute 2: Developer-advocate's domain tutorial (DA-1) should not block on install-path resolution

Developer-advocate's modification to Recommendation #1 adds an "explicit dependency on install-path consistency being resolved first or simultaneously." User-advocate endorses this dependency in their cross-review. I dispute the blocking relationship.

The domain tutorial teaches developers to build `DomainPlugin` subclasses, implement `VariableExtractor`, and call `domain.score()`. These are Python class inheritance patterns that work regardless of how the package was installed. A developer who has a working `conversus` checkout -- whether via `git clone` + `uv sync`, `pip install -e .`, or any other method -- can follow the tutorial. The tutorial's correctness does not depend on which install command the index page displays.

The install-path fix (my New-1, user-advocate's Recommendation 2) is P1 for the onboarding track. The domain tutorial (DA-1) is P1 for the extensibility track. Both should ship. But making one block the other introduces a false dependency that delays useful content for no actual benefit. A developer experienced enough to build domain plugins has already solved their own install problems.

**Position**: The domain tutorial and install-path fix should ship independently. Remove the blocking dependency from DA-1.

### Dispute 3: The "copy-paste test" should not be elevated to a standing documentation policy

User-advocate's modified Recommendation 8 proposes stating the copy-paste test as "a documentation principle in the implementation plan." Developer-advocate implicitly endorses this by calling it compatible with their async-context note. I originally endorsed the copy-paste test framing as more precise than my own, and I stand by that for the SDK Quick Start specifically. But there is a meaningful difference between "the first SDK example should be self-contained and runnable" and "every first code example on a page should be self-contained and runnable without modification."

The domain tutorial (DA-1) will include a 5-stage lifecycle example that builds incrementally. Making each stage independently copy-pasteable would require repeating imports, class definitions, and setup code at every stage, turning a connected tutorial into a bloated collection of standalone snippets. The plugin wiring steps (DA-2) depend on having a config file and an installed package, which are setup prerequisites, not runnable-on-their-own code blocks. The config-reference minimal example (DA-10) is YAML, not Python -- "runnable without modification" does not apply.

The copy-paste test is the right standard for entry-point pages (SDK Quick Start, quickstart.md). Generalizing it to a standing policy creates a constraint that conflicts with tutorial pedagogy and non-executable content.

**Position**: Apply the copy-paste test to the SDK Quick Start and quickstart.md first examples. Do not codify it as a blanket documentation principle.

## Convergence

### Convergence 1: Epilog fix coupled with `--phase review` documentation (Recommendations 1 + 9)

All three agents now agree these are a single P1 deliverable. Source verification confirms: `cli/__init__.py` L95 shows `--phase synthesis`, Click constrains to `["all", "review"]` at L108-111, and `run.py` L248-250 confirms `--phase review` calls `run_phase1()` only. Developer-advocate identified the coupling, user-advocate identified the compounding loop, and I verified both against source. This is fully resolved.

### Convergence 2: Scaffold endpoint glob fix (Recommendation 2)

All three agents confirm this P1 bug: `api.py` L208 globs `*.json` only while `load_scaffold()` at `base.py` L144-171 handles `.yml`, `.yaml`, and `.json`. No disputes remain. Round 1 bilateral convergence is now trilateral.

### Convergence 3: Three-way provider default as warning callout in config-reference.md (Recommendation 4)

All three agents agree the finding is accurate (`EngineConfig` defaults to `"anthropic"` at `config.py` L77, CLI defaults to `"mock"` at `cli/__init__.py` L103, SDK defaults to `"mock"` at `sdk.py` L155). All three agree on the admonition/warning callout presentation. I maintain P2 (safe failure mode: user gets mock output, not real API charges). User-advocate and developer-advocate's P1 arguments were about presentation, not severity -- the callout box addresses their concern without priority elevation. Convergence is on the fix; the priority dispute is resolved in favor of P2.

### Convergence 4: Error handling guidance corrected per source (Developer-advocate Recommendation 5)

Developer-advocate accepted my correction in full. The original "return empty dicts" guidance is withdrawn. The replacement -- "Raise freely; the framework catches and logs" -- is now verified against `domains/base.py` L697-708 (extractor catch-and-skip) and `plugins/base.py` L519-525 (plugin execute catch-and-skip). All three agents agree on the corrected content.

### Convergence 5: SDK happy-path-only documentation treated as individual inline annotations (Recommendation 7)

Both cross-reviewers identified the systemic pattern. I accepted the pattern identification but disputed the remedy. Both agents now accept my approach: inline failure-mode annotations at each documented call site rather than a single "error handling" section. The three source-verified instances (`cost_estimate` returns `None`, `construct_objective` raises `ValueError`/`RuntimeError`, `classify` raises `ValueError`) are documented individually. Recommendation 10 is absorbed. This is resolved.

## Final Position Statement

### Non-Negotiables

1. **Source-verified findings take priority over proposed conventions.** All documentation fixes must be checked against current source code before shipping. This includes developer-advocate's corrected error handling guidance, the type accuracy in tutorial examples (`list[Path]` not `list[str]` for `DomainContext.changed_files`), and the plugin loader alphabetical-order behavior (`dir()` returns names alphabetically, not by declaration order).

2. **The scaffold endpoint glob bug (Recommendation 2) is a code fix, not a documentation fix.** The `api.py` L208 glob pattern must change from `*.json` to include `*.yml` and `*.yaml`. This is the only recommendation in the entire pipeline that requires a code change rather than a documentation edit. It must not be lost in a documentation-only implementation plan.

3. **The epilog fix (Recommendation 1) must not ship without `--phase review` documentation (Recommendation 9).** Replacing a broken example with an unexplained one is not an improvement. These are a single deliverable.

### Flexibility

1. **Priority levels are negotiable for P2/P3 items.** I care that the three-way provider default gets a warning callout in config-reference.md. Whether it ships as P2 or P1 does not change the fix.

2. **The "copy-paste test" scope is negotiable within reason.** I support it for entry-point pages. If the synthesizer wants to state it as a "strong recommendation" rather than a "standing policy," with explicit exceptions for multi-stage tutorials and non-executable content, I can accept that framing.

3. **The `uv run` prefix consistency fix (my New-2) can be absorbed into a broader install-path consistency pass.** User-advocate and developer-advocate both proposed similar notes at the top of cli.md. The exact wording and placement can be determined during implementation as long as the inconsistency is addressed.
