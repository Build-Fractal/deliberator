# Neutral Synthesis -- Round 2 -- Conversus Documentation Suite (Spec 031)

---

## Process Summary

- **Agents**: 3 -- code-verifier, user-advocate, developer-advocate
- **Mode**: cooperative (Round 2 of 3)
- **Prior round disputes**: 7 (Round 1)
- **This round disputes**: 6 (see below) -- net reduction of 1; convergence is occurring but slowly

**Artifact counts (Round 2):**
- Phase 1 reviews: 3
- Phase 2 cross-reviews: 6
- Phase 3 revisions: 3
- Phase 4 disputes: 3
- Round 1 convergence items carried forward: 7 (all reaffirmed by all agents without reversal)
- New convergence points in Round 2: 8 (total now 15)

**Recommendation flow (Round 2):**
- Recommendations entering Phase 1 (Round 2 reviews): code-verifier 10 (4 carried + 6 new), user-advocate 10 (all scoped to Round 2), developer-advocate 10 (7 carried + 3 new)
- Recommendations modified in Phase 3: code-verifier 6 modified + 1 withdrawn (absorbed) + 2 new; user-advocate 5 modified + 3 new; developer-advocate 5 modified + 3 new
- Recommendations surviving unmodified: code-verifier 3, user-advocate 5, developer-advocate 5
- Disputes remaining (Phase 4): code-verifier 3, user-advocate 3, developer-advocate 3 (deduplicated: 6 unique disputes)
- Convergence points (Phase 4): code-verifier 5, user-advocate 5, developer-advocate 5 (deduplicated: 8 unique new convergence items)

**Dispute trajectory**: Round 1 ended with 7 disputes. Round 2 ends with 6 disputes. One Round 1 dispute was fully resolved (sync-first SDK ordering -- all agents accepted the resolution). Several new disputes emerged from new Round 2 findings (install-path gating, copy-paste test scope, output example format), while other Round 1 disputes collapsed into convergence. The net decrease of 1 indicates convergence is happening but not aggressively. Two of the 6 remaining disputes are scope/framing disagreements rather than substantive content disagreements, which suggests Round 3 should resolve most of them through precise wording of the implementation plan.

---

## Recommendation Scorecard

| # | Agent | Recommendation | Round 2 Priority | Phase 3 Disposition | Challenged By | Convergence Status |
|---|-------|---------------|-------------------|---------------------|---------------|-------------------|
| CV-R1 | code-verifier | Fix `--phase synthesis` epilog bug (NEW R2) | P1 | Modified: coupled with CV-R9 | developer-advocate (coupling), user-advocate (compounding) | Converged -- single P1 deliverable with CV-R9 |
| CV-R2 | code-verifier | Fix scaffolds endpoint YAML glob (R1 CV-2) | P1 | Surviving | None | Converged (carried from R1, now trilateral) |
| CV-R3 | code-verifier | `decide` 4-mode note in cli.md + index page (R1 CV-1) | P1 | Modified: expanded to 4 index-page locations | user-advocate (index page scope) | Converged -- all agents agree on expanded scope |
| CV-R4 | code-verifier | Three-way provider default warning in config-reference.md (NEW R2) | P2 | Modified: admonition callout format | user-advocate (P1 elevation), developer-advocate (callout format) | Partial -- content agreed, priority disputed (P1 vs P2) |
| CV-R5 | code-verifier | `plugins:` key in config-reference.md (R1 CV-B) | P2 | Surviving | None | Converged (carried from R1) |
| CV-R6 | code-verifier | API reference prose + `members:` + dual-surface class catalog (R1 CV-A) | P2 | Modified: plain-text class catalog for GitHub | developer-advocate (dual-surface) | Converged -- all agents accept layered approach |
| CV-R7 | code-verifier | SDK happy-path-only inline annotations (NEW R2, absorbs CV-R10) | P2 | Modified: systemic pattern, 3 instances | user-advocate (pattern), developer-advocate (pattern) | Converged -- inline annotations for cost_estimate, construct_objective, classify |
| CV-R8 | code-verifier | `estimate_cost_usd()` in SDK guide (R1 CV-7) | P2 | Surviving | None | Converged (carried from R1) |
| CV-R9 | code-verifier | Document `--phase review` behavior (NEW R2) | P1 (elevated from P2) | Modified: coupled with CV-R1 | developer-advocate (coupling), user-advocate (compounding) | Converged -- single P1 deliverable with CV-R1 |
| CV-N1 | code-verifier | Fix `pip install conversus` on index page (NEW R2) | P1 | New in Phase 3 | N/A | Converged -- all agents agree P1, most dangerous defect |
| CV-N2 | code-verifier | `uv run` prefix note at top of cli.md (NEW R2) | P2 | New in Phase 3 | N/A | Converged -- all agents accept option (a) only |
| UA-R1 | user-advocate | Fix index page "4 modes" across 4 locations | P1 | Modified: 4th location (card title) added | code-verifier (card title) | Converged -- absorbed into CV-R3 expanded scope |
| UA-R2 | user-advocate | Resolve `pip install conversus` vs. `uv sync` | P1 | Surviving | None (both cross-reviewers validated) | Converged -- absorbed into CV-N1 |
| UA-R3 | user-advocate | Visual break + heading before slash commands | P1 | Modified: placement after CLI path completes | developer-advocate (placement) | Converged -- heading + 2 sentences after CLI path |
| UA-R4 | user-advocate | `uv run` prefix note in cli.md | P1 -> P2 | Modified: option (a) only per developer-advocate | developer-advocate (danger of options b/c) | Converged -- absorbed into CV-N2 |
| UA-R5 | user-advocate | Example output in quickstart "What just happened" | P2 | Modified: 8-10 lines, abbreviated, marked approximate | code-verifier (fragility), developer-advocate (scope) | Disputed -- developer-advocate prefers prose description over literal output |
| UA-R6 | user-advocate | Expand quickstart micro-hint to cover `uv` | P2 | Surviving | None | Unchallenged -- survives |
| UA-R7 | user-advocate | State MkDocs as primary reading surface | P2 | Surviving | None | Converged -- all agents agree |
| UA-R8 | user-advocate | Copy-paste test as documentation principle | P2 | Modified: generalized to all first-examples | code-verifier (endorses generalization) | Disputed -- code-verifier limits scope to entry-point pages |
| UA-R9 | user-advocate | "What you will see" section for modes page | P3 | Surviving | None | Unchallenged -- survives |
| UA-R10 | user-advocate | `conversus status` in quickstart | P3 | Surviving | None | Converged -- all agents agree |
| UA-N1 | user-advocate | Pair plugins config-ref + building-plugins as single deliverable | P1 (process) | New in Phase 3 | N/A | Converged -- all agents accept pairing |
| UA-N2 | user-advocate | Flag error handling for code-verifier validation | P2 (process) | New in Phase 3 | code-verifier (already done) | Resolved -- verification already completed in cross-review |
| UA-N3 | user-advocate | Provider default warning in config-reference.md | P2 | New in Phase 3 | N/A | Converged -- absorbed into CV-R4 |
| DA-R1 | developer-advocate | End-to-end domain tutorial (R1 DA-1) | P1 | Modified: type accuracy + correct setup preamble | code-verifier (type error), user-advocate (install-path dep) | Disputed -- gating dependency on install-path resolution |
| DA-R2 | developer-advocate | Plugin wiring steps in building-plugins.md (R1 DA-2) | P1 | Modified: loader behavior corrected, paired with config-ref | code-verifier (alphabetical order), user-advocate (pairing) | Converged -- ships paired with plugins config-ref |
| DA-R3 | developer-advocate | Slash command heading in quickstart (R1 P1-3) | P1 | Modified: heading after CLI path | user-advocate (heading needed), own concern (placement) | Converged -- absorbed into UA-R3 |
| DA-R4 | developer-advocate | Domain-engine integration in architecture.md (R1 DA-8) | P2 | Surviving | None | Unchallenged -- survives |
| DA-R5 | developer-advocate | Error handling guidance for plugin/domain authors (R1 DA-5) | P2 | Modified: corrected per code-verifier source verification | code-verifier (factual correction) | Disputed -- scope of prescriptive vs. descriptive patterns |
| DA-R6 | developer-advocate | Testing examples for plugins/domains (R1 DA-6) | P2 | Surviving | None | Unchallenged -- survives |
| DA-R7 | developer-advocate | Import namespace explanation in SDK guide (R1 DA-9) | P2 | Modified: decoupled from code change, simplified | code-verifier (unnecessary coupling), user-advocate (confusion risk) | Converged -- minimal note, independent of classify re-export |
| DA-R8 | developer-advocate | Sync-first SDK Quick Start with async-context note | P2 | Surviving | None | Converged -- all agents accept |
| DA-R9 | developer-advocate | `conversus status` in quickstart (R1 DA-10) | P3 | Surviving | None | Converged -- absorbed into UA-R10 |
| DA-R10 | developer-advocate | Minimal starter config callout (R1 UA-9 modified) | P3 | Surviving | None | Unchallenged -- survives |
| DA-NA | developer-advocate | Install-path + import namespace consistency pass (NEW R2) | P1 | New in Phase 3 | N/A | Converged -- absorbed into CV-N1 |
| DA-NB | developer-advocate | `uv run` note in cli.md option A (NEW R2) | P2 | New in Phase 3 | N/A | Converged -- absorbed into CV-N2 |
| DA-NC | developer-advocate | State MkDocs as primary surface (NEW R2) | P2 | New in Phase 3 | N/A | Converged -- absorbed into UA-R7 |

---

## Dangerous Contradictions Found

### Resolved in Round 2

1. **`pip install conversus` on index page vs. `git clone` + `uv sync` in quickstart** (user-advocate discovery, Round 2). The index page at `docs/index.md` L29 shows `pip install conversus` as the primary install path. The quickstart uses `git clone` + `uv sync`. The `pyproject.toml` wires entry points that work only after a local install. If no PyPI package exists (the structural evidence strongly suggests none does), `pip install conversus` either fails outright or installs an unrelated package. All three agents elevated this to P1 and called it "the most dangerous first-contact failure" in the documentation. Developer-advocate connected it to the import namespace confusion: a user who `pip install`s a wrong package and then encounters `from engine import Deliberation` has no diagnostic path. **Resolution**: All three agents converge on P1 -- determine whether a PyPI package exists, fix the index page to match reality.

2. **`--phase synthesis` epilog bug creates a broken self-help loop** (code-verifier discovery, Round 2). The CLI's `run` command epilog shows `--phase synthesis` but Click constrains `--phase` to `["all", "review"]`. A user who tries the invalid example gets a Click error. Developer-advocate identified that fixing the epilog alone (to `--phase review`) without documenting what a review-only run produces creates a new trap. User-advocate identified the compounding effect: the user falls back to `--phase review`, gets partial output, cannot interpret it. **Resolution**: All three agents converge -- the epilog fix and `--phase review` behavior documentation are a single P1 deliverable.

3. **Error handling guidance prescribed behaviors contradicted by framework source** (code-verifier correction, Round 2). Developer-advocate originally wrote "Domain extractor exceptions should return empty dicts rather than raising." Code-verifier showed `domains/base.py` L697-708 already catches extractor exceptions. Telling authors to swallow exceptions would mask failures the framework was designed to surface. **Resolution**: Developer-advocate withdrew the erroneous guidance and accepted: "Raise freely -- the framework catches and logs."

4. **Plugin loader uses alphabetical `dir()` order, not declaration order** (code-verifier correction, Round 2). Developer-advocate wrote "name your module accordingly." Code-verifier pointed out `dir()` returns names alphabetically, making "name accordingly" vague. **Resolution**: Developer-advocate accepted the correction. Documentation will say: "The loader finds the first Plugin subclass (by alphabetical attribute name). Define exactly one Plugin subclass per module."

5. **`score()` call convention is typed and docstringed, not ambiguous** (code-verifier correction, Round 2). Developer-advocate characterized the `score()` interface as undiscoverable. Code-verifier showed `base.py` L711-714 has explicit type annotations (`scaffold: str | Scaffold`) and a docstring. **Resolution**: Developer-advocate accepted -- the gap is documentation coverage (not demonstrating the call), not contract ambiguity.

### Unresolved

6. **SDK documentation systematically hides failure modes** (identified by all three agents). `Deliberation.cost_estimate` returns `None` but docs show it as always returning a dict. `construct_objective()` raises `ValueError`/`RuntimeError` but docs show only the happy path. `AgentCompleted.response_text` is optional but documented as required. All agents agree on inline annotations for the three verified instances. The dispute is whether to codify a standing principle preventing recurrence (user-advocate) or treat each instance individually (code-verifier). See Remaining Disputes.

---

## Systemic Contradictions

1. **Install-path fragmentation across entry points** (NEW in Round 2). The documentation presents at least three install paths: `pip install conversus` (index page), `git clone` + `uv sync` (quickstart), and `pip install -e .` (quickstart micro-hint, developer guide). The CLI reference uses bare `conversus` commands (implying pip-installed) while the quickstart uses `uv run conversus` (implying uv-managed). Import examples span two namespaces (`engine.*` and `conversus.*`). These inconsistencies compound: a user who enters through the index page and follows its install command may never reach a working state. This is the highest-severity systemic issue identified across both rounds and was not detected in Round 1 because all agents focused on the quickstart as the primary entry point.

2. **Audience segmentation without explicit scoping** (carried from Round 1, not resolved). The documentation serves three audiences (new users, SDK integrators, plugin/domain developers) without page-level audience markers. This manifests as priority disagreements: user-advocate evaluates pages for first-contact experience; developer-advocate evaluates for developer completeness; code-verifier evaluates for source accuracy. All three perspectives are valid but the documentation itself does not declare which audience each page serves. No agent in Round 2 proposed a concrete audience-labeling mechanism.

3. **Raw Markdown vs. rendered MkDocs as the evaluation surface** (carried from Round 1, now partially resolved). All three agents converge on declaring MkDocs as the primary reading surface and adding build instructions. The API reference pages (`:::` directives) will get plain-text class catalogs above the directives for GitHub fallback. This is a pragmatic resolution that avoids the "dual-format content" trap.

4. **Documentation-only vs. code fixes: approval threshold ambiguity** (carried from Round 1). Spec 031 is a "docs-and-compliance" spec, but two findings are code bugs (scaffolds endpoint `api.py` L208, CLI epilog `cli/__init__.py` L95), one is a code export gap (`classify` not in `engine/__init__.py`), and one is a behavioral design question (should CLI `run` fall back to `config.provider`?). The process has no stated policy for whether code changes discovered through documentation review ship in the same spec or require separate tickets. Round 2 did not resolve this -- the code fixes are included in the recommendation list with [Code change] tags, but the approval workflow remains ambiguous.

---

## Convergence Achieved

All 7 Round 1 convergence items were reaffirmed by all three agents in Round 2 without reversal. They are not restated here in full -- see Round 1 synthesis for details. Summary:

1. `decide` 4-mode restriction note in cli.md (R1 Convergence #1, unanimous)
2. Scaffolds endpoint YAML glob fix (R1 Convergence #2, now trilateral)
3. `plugins:` key in config-reference.md (R1 Convergence #3, unanimous)
4. API reference narrative prose above autodoc directives (R1 Convergence #4, unanimous)
5. `determine_verdict` split: default behavior + custom override (R1 Convergence #5, bilateral)
6. Provider precedence note in cli.md (R1 Convergence #6, unanimous)
7. `estimate_cost_usd()` in SDK guide (R1 Convergence #7, bilateral)

**New convergence in Round 2:**

8. **`pip install conversus` index page fix** (unanimous, all three agents). The index page install command must be reconciled with reality. Determine whether a PyPI package exists. If not, replace with the quickstart's `git clone` + `uv sync` path or `pip install -e .`. Source: user-advocate R2 Recommendation 2, code-verifier R2 New-1, developer-advocate R2 New Recommendation A.

9. **CLI epilog fix + `--phase review` documentation as single P1 deliverable** (unanimous). Fix `engine/cli/__init__.py` L95 from `--phase synthesis` to `--phase review`. Add to cli.md: "`--phase review` runs Phase 1 only (individual agent reviews). Output: one review file per agent. Cross-review, revision, dispute, and synthesis phases are skipped." These must ship together. Source: code-verifier R2 Recommendations 1+9, developer-advocate cross-review Dangerous Contradiction #2, user-advocate cross-review Dangerous Contradiction #2.

10. **`uv run` prefix note at top of cli.md (option A only)** (unanimous). Add: "Examples below use bare `conversus` commands. If you installed via `uv sync` (as in the quickstart), prefix with `uv run`." Options B (add `uv run` to all examples) and C (venv activation in quickstart) are explicitly rejected by all agents as creating new contradictions. Source: user-advocate R2 Recommendation 4, code-verifier R2 New-2, developer-advocate R2 New Recommendation B.

11. **Slash command heading + explanation after CLI path completes** (unanimous). Add heading "## Try the guided workflow (in your AI editor)" after the CLI path (after "Try with a real provider") with 2-sentence explanation. Not mid-flow. Source: user-advocate R2 Recommendation 3 (modified), developer-advocate R2 Recommendation 3 (modified), code-verifier cross-review Safe Agreement #2.

12. **Plugin wiring steps paired with `plugins:` config-reference addition** (unanimous). The building-plugins.md "Dynamic loading" section update and the config-reference.md `plugins:` key addition are a single deliverable. Plugin wiring documentation corrected: "The loader finds the first Plugin subclass (by alphabetical attribute name). Define exactly one Plugin subclass per module." Source: developer-advocate R2 Recommendation 2 (modified), user-advocate R2 New Recommendation 1, code-verifier cross-review Tension #2.

13. **Error handling documentation corrected per source** (bilateral -- code-verifier, developer-advocate). The framework catches and logs exceptions from extractors (`domains/base.py` L697-708) and plugins (`plugins/base.py` L519-525). Documentation must describe this actual behavior, not prescribe exception swallowing. Core message: "Raise freely -- the framework catches and logs." Source: code-verifier cross-review of developer-advocate Dangerous Contradiction #2, developer-advocate revision Recommendation 5.

14. **MkDocs declared as primary reading surface** (unanimous). Add a statement with `uv run mkdocs serve` build instructions. API reference pages get plain-text class catalogs above `:::` directives for GitHub fallback. Source: user-advocate R2 Recommendation 7, developer-advocate R2 New Recommendation C, code-verifier R2 Recommendation 6 (modified).

15. **SDK sync-first Quick Start with async-context note** (unanimous). Lead with `asyncio.run()` wrapper. Note immediately below: "The SDK is async-native. Event subscriptions require async context -- see Event Subscription below for `await`-based usage." Add `# Save as script.py and run: python script.py` comment. This resolves the Round 1 dispute. Source: all three agents' Round 2 revisions.

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

**Dispute count: 6** (down from 7 in Round 1 -- net reduction of 1)

- **Dispute 1: Provider default warning priority (P1 vs. P2)**
  - **Positions**: user-advocate argues P1 because silent failures are worse than loud ones -- a user who gets mock output when expecting Anthropic output may conclude the tool produces low-quality output rather than that their config was silently overridden. code-verifier argues P2 because the failure mode is safe (no money spent, no incorrect results) and the warning callout format (agreed by all) addresses the presentation concern. developer-advocate defers to the callout format without taking a strong priority position.
  - **Arguments**: user-advocate: "A silent default override is a worse trap than a broken example, because the user does not even know they are in one." code-verifier: "The provider default mismatch is confusing but produces a safe failure mode."
  - **Synthesizer assessment**: Both positions have merit. The content and format are agreed (admonition/warning callout in config-reference.md). The priority dispute is narrow. user-advocate's "silent failure" argument is persuasive for the user who writes a config file expecting Anthropic behavior and gets mock output. However, code-verifier is correct that the failure does not cause financial harm or incorrect decisions -- it causes confusion and wasted time. The practical resolution is that the callout format makes this item easy to implement regardless of priority.
  - **Recommended resolution**: P2 with the admonition/warning callout as agreed. User-advocate's flexibility statement accepts P2 if the callout format and prominent placement are committed. The callout text from code-verifier's revision is well-worded. File a follow-up code issue for the CLI to fall back to `config.provider` when `--provider` is not explicitly set.

- **Dispute 2: Domain tutorial gating on install-path resolution**
  - **Positions**: user-advocate and developer-advocate's own revision initially accepted a sequencing dependency ("the tutorial cannot land effectively if the install path remains contradictory"). code-verifier and developer-advocate's disputes argue the domain tutorial should not be blocked by the install-path fix because they touch different files, serve different audiences, and the tutorial can include its own self-contained setup preamble. user-advocate's dispute asks for explicit batching where onboarding fixes ship before or alongside extensibility content.
  - **Arguments**: developer-advocate (disputes): "A developer experienced enough to build domain plugins has already solved their own install problems." user-advocate (disputes): "If the index page install command fails, no one reaches the domain tutorial."
  - **Synthesizer assessment**: The Round 1 synthesis established parallel independent tracks. Both sides are now arguing about the same principle from different angles. Developer-advocate is correct that a developer building domain plugins has typically already solved installation. user-advocate is correct that if the index page is the entry point, a broken install command gates everything. The resolution is in the implementation plan structure, not in which content ships first. The domain tutorial should include a self-contained setup preamble (`git clone` + `uv sync` + `cd conversus`) that does not depend on the index page being fixed. This makes it independently shippable while the install-path fix proceeds in parallel.
  - **Recommended resolution**: No hard gating dependency. The domain tutorial must include its own setup preamble. The implementation plan should batch items into tracks (see Actionable Spec Changes) and state: "Items within a track are ordered by priority. Items across tracks have no ordering dependency. The domain tutorial's setup preamble provides a correct install path regardless of the index page state."

- **Dispute 3: Copy-paste test scope -- standing documentation principle vs. entry-point-only**
  - **Positions**: user-advocate proposes "every first code example on a page should be self-contained and runnable without modification" as a standing documentation principle. code-verifier accepts it for entry-point pages (SDK Quick Start, quickstart.md) but disputes generalizing it because multi-stage tutorials and YAML examples cannot pass the test. developer-advocate supports the principle for code examples but disputes extending it to output examples (see Dispute 4).
  - **Arguments**: code-verifier: "The domain tutorial will include a 5-stage lifecycle example that builds incrementally. Making each stage independently copy-pasteable would require repeating imports, class definitions, and setup code at every stage." user-advocate: "Without the principle, the next person who documents a new SDK function will omit failure modes because there is no stated expectation."
  - **Synthesizer assessment**: code-verifier's concern about tutorial pedagogy is valid -- a connected tutorial must build incrementally. user-advocate's concern about recurrence prevention is also valid -- principles prevent drift. The resolution is precision in the principle's scope.
  - **Recommended resolution**: State the principle with explicit scope: "The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block should be self-contained. YAML examples are exempt." This satisfies user-advocate's recurrence prevention, code-verifier's tutorial pedagogy concern, and developer-advocate's exemption for non-executable content.

- **Dispute 4: Quickstart example output -- literal block vs. prose description**
  - **Positions**: user-advocate proposes 8-10 lines of abbreviated terminal output after the "What just happened" section, marked as approximate. developer-advocate opposes literal output blocks because mock provider output changes between releases, creating a maintenance burden on the highest-traffic page. developer-advocate proposes prose descriptions instead ("You will see five phase headings followed by a final verdict"). code-verifier accepts the output block as P2 with fragility caveats.
  - **Arguments**: developer-advocate: "A stale output example on this page is worse than no output example at all, because it signals 'these docs are not maintained.'" user-advocate: "A user running `--provider mock` will see output, but they have no way to verify whether what they see matches what was expected."
  - **Synthesizer assessment**: Both sides identify real risks. Stale output blocks degrade trust. Missing output blocks prevent verification. The mock provider's output is inherently less stable than the CLI's input commands. developer-advocate's prose description is more durable but less verifiable. user-advocate's literal block is more verifiable but less durable.
  - **Recommended resolution**: Hybrid approach. Add a prose description of what to expect ("You will see five phase headers -- Review, Cross-review, Revision, Disputes, Synthesis -- followed by a headline verdict and a summary.") without a literal output block. Add a note: "Run with `--format json` to verify the phase structure programmatically." This is durable (phase names are stable), verifiable (the user knows what to look for), and low-maintenance (no literal output to keep current). If both agents accept the hybrid, the output example dispute is resolved.

- **Dispute 5: Error handling documentation -- prescriptive patterns vs. descriptive-only**
  - **Positions**: developer-advocate insists the error handling subsection must include prescriptive patterns (use `.get()` with defaults, raise exceptions freely, check logs) alongside the descriptive framework behavior. code-verifier's disputes note that user-advocate's "flag for validation" request is moot because the verification already happened. user-advocate's New Recommendation 2 is confirmed as resolved by code-verifier.
  - **Arguments**: developer-advocate: "A developer writing their first plugin needs a pattern to follow, not a catalog of every possible exception type." code-verifier (implicit): the prescriptive patterns should be source-verified.
  - **Synthesizer assessment**: This dispute is narrower than it appears. All agents agree the error handling subsection should describe the framework's catch-and-skip behavior (converged). developer-advocate wants to add three prescriptive lines: "Raise freely, use `.get()` with defaults for consumed data, check logs for skip warnings." code-verifier verified the framework behavior but did not explicitly endorse or reject the prescriptive additions (the dispute focused on the now-withdrawn "return empty dicts" guidance, which is resolved). The `.get()` pattern is standard Python and does not make a claim about framework behavior.
  - **Recommended resolution**: Include both descriptive and prescriptive content. The descriptive section documents the framework's catch-and-skip behavior (source-verified). The prescriptive section adds three bullet points of defensive patterns, clearly labeled as "recommended patterns" rather than framework guarantees: (1) "Raise freely -- exceptions are caught and logged," (2) "Use `state.plugin_results.get('key', default)` for consumed data in case the producer failed," (3) "Check warning-level logs for plugin/extractor skip messages during development." These are defensive programming patterns that are correct regardless of framework internals.

- **Dispute 6: Implementation plan ordering -- explicit batches vs. priority-tagged list**
  - **Positions**: user-advocate demands the synthesis produce an ordered implementation plan with explicit batches: "Batch 1 (onboarding) ships independently; Batch 2 (extensibility) should not ship before install-path contradictions are resolved." developer-advocate and code-verifier prefer parallel independent tracks without hard sequencing.
  - **Arguments**: user-advocate: "'Parallel tracks' is a planning abstraction that dissolves the moment a single implementer sits down to work." developer-advocate: "Coupling these as a single deliverable creates exactly the kind of 'all or nothing' release that the parallel-tracks resolution was designed to prevent."
  - **Synthesizer assessment**: user-advocate is correct that an unordered list is less actionable than a batched plan. developer-advocate is correct that hard inter-track gating creates false dependencies. The resolution is to provide track-level batching without inter-track gating, while stating a strong preference for onboarding fixes shipping first when resources are serial.
  - **Recommended resolution**: See Actionable Spec Changes below. The plan uses three tracks (Code fixes, Onboarding, Extensibility) with items ordered within each track. Across tracks, no hard dependencies. A note states: "When resources are serial, prioritize by track order: code fixes first (smallest, highest-confidence), then onboarding (broadest audience), then extensibility (deepest impact). When resources are parallel, all three tracks can proceed simultaneously."

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### Track 1: Code Fixes (smallest scope, highest confidence)

**P1-Code-1. Fix scaffolds endpoint to glob YAML files.** [Code change]
Change `api.py` L208 from `domain.scaffold_dir.glob("*.json")` to iterate over `("*.yml", "*.yaml", "*.json")`. Converged (R1 bilateral, R2 trilateral). Source: R1 CV-2, R2 all agents confirm.

**P1-Code-2. Fix `run` command epilog `--phase synthesis` example.** [Code change]
Change `engine/cli/__init__.py` L95 from `--phase synthesis` to `--phase review`. Converged (R2 unanimous). Source: code-verifier R2 Recommendation 1. Ships with P1-Onboard-3.

**P2-Code-3. Export `classify` from `engine/__init__.py`.** [Code change]
Add `classify` to `engine/__init__.py` exports. Track separately from the SDK namespace documentation note. Source: R1 CV-4, R2 code-verifier Missed Opportunity 6. File follow-up code issue for CLI to fall back to `config.provider` when `--provider` is at its default.

### Track 2: Onboarding (broadest audience, highest expected impact per hour)

**P1-Onboard-1. Reconcile install path on index page.** [Docs change]
Determine whether a PyPI `conversus` package exists. If not, replace `pip install conversus` on `docs/index.md` L29 with the quickstart's `git clone` + `uv sync` path. Also fix Quick Install section prerequisites (Python 3.12+, uv). Converged (R2 unanimous). Source: user-advocate R2 Recommendation 2, code-verifier R2 New-1, developer-advocate R2 New Recommendation A.

**P1-Onboard-2. Fix index page "4 modes" claim across 4 locations.** [Docs change]
(a) Three Layers table L20: "4 competition modes" to "8 deliberation modes." (b) Quick Links card title: "Competition Modes" to "Deliberation Modes." (c) Quick Links mode list: expand to all 8 or replace with link to modes.md. (d) Add CLI subset qualifier. Converged (R1 unanimous, R2 expanded scope). Source: R1 CV-1, R2 user-advocate Recommendation 1, code-verifier Recommendation 3.

**P1-Onboard-3. Document `--phase review` behavior in cli.md.** [Docs change]
Add to cli.md under the `--phase` option: "`review` runs Phase 1 only (individual agent reviews). Output: one review file per agent. Cross-review, revision, dispute, and synthesis phases are skipped." Ships with P1-Code-2. Converged (R2 unanimous). Source: code-verifier R2 Recommendations 1+9 (coupled).

**P1-Onboard-4. Add `decide` 4-mode clarifying note to cli.md.** [Docs change]
Add under `decide` options: "The `decide` command supports 4 modes for ad-hoc use. For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file. See [Deliberation Modes](modes.md) for all 8." Converged (R1 unanimous). Source: R1 CV-1.

**P1-Onboard-5. Add heading + explanation before slash commands in quickstart.md.** [Docs change]
Add heading "## Try the guided workflow (in your AI editor)" after the CLI path completes (after "Try with a real provider"). Add 2-sentence explanation: "The following commands are slash commands for AI coding assistants like Claude Code or Cursor. They are not terminal commands. See [MCP Setup](mcp-setup.md) to configure your editor." Converged (R2 unanimous). Source: R1 P1-3, R2 user-advocate Recommendation 3, developer-advocate Recommendation 3.

**P1-Onboard-6. Add prerequisites callout to quickstart.** [Docs change]
Add at top: "Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/)." In the install code block: `# Requires Python 3.12+ and uv (https://docs.astral.sh/uv/). Alternative: pip install -e .`. Converged (R1/R2). Source: R1 P1-4, R2 user-advocate Recommendation 6.

**P2-Onboard-7. Add `uv run` prefix note at top of cli.md.** [Docs change]
"Examples below use bare `conversus` commands. If you installed via `uv sync` (as in the quickstart), prefix with `uv run` (e.g., `uv run conversus run config.yml`). If you installed via `pip install -e .`, the commands work directly." Converged (R2 unanimous, option A only). Source: R2 user-advocate Recommendation 4, code-verifier New-2, developer-advocate New Recommendation B.

**P2-Onboard-8. Write SDK Quick Start with sync-first code block.** [Docs change]
Lead with `asyncio.run()` wrapper as the first code block. Add `# Save as script.py and run: python script.py` comment. Note immediately below: "The SDK is async-native. Event subscriptions require async context -- see Event Subscription below for `await`-based usage." Converged (R2 unanimous, resolves R1 dispute). Source: R1 dispute resolution, R2 all agents.

**P2-Onboard-9. Add three-way provider default warning to config-reference.md.** [Docs change]
Use admonition/warning callout at the `provider:` field: "Warning: When `provider` is omitted, the config defaults to `anthropic`. However, CLI `--provider` defaults to `mock` and takes full precedence over the config file. If you omit both, the CLI wins and you get mock output. Set `provider:` explicitly in your config to avoid surprises." Also add the provider precedence note to cli.md (R1 Convergence #6). File follow-up issue for whether CLI should fall back to `config.provider`. Source: R1 CV-3, R2 code-verifier Recommendation 4, all agents agree on callout format.

**P2-Onboard-10. Add SDK happy-path-only failure-mode annotations.** [Docs change]
Add inline annotations to `sdk.md` for: (a) `Deliberation.cost_estimate` -- "Returns `None` if the config cannot be parsed." (b) `construct_objective()` -- "Raises `ValueError` if no templates match. `NonInteractiveGapFiller` raises `RuntimeError` on parameters without defaults." (c) `classify()` -- "Raises `ValueError` if no keyword patterns match." Source: code-verifier R2 Recommendation 7 (modified).

**P2-Onboard-11. Add provider default model table to cli.md.** [Docs change]
"| Provider | Default Model | | anthropic | claude-sonnet-4-20250514 | | openai | gpt-4o |" Source: R1 CV-6 (unchallenged).

**P2-Onboard-12. State MkDocs as primary reading surface.** [Docs change]
Add to index page or developer guide: "This documentation is built with MkDocs Material. API reference pages use mkdocstrings and require a built site to render fully. To build locally: `uv run mkdocs serve`." Converged (R2 unanimous). Source: user-advocate R2 Recommendation 7, developer-advocate R2 New Recommendation C.

**P2-Onboard-13. Add abbreviated output description to quickstart "What just happened" section.** [Docs change]
Add prose description: "You will see five phase headers -- Review, Cross-review, Revision, Disputes, Synthesis -- followed by a headline verdict and a summary." Add: "Run with `--format json` to verify the phase structure programmatically." No literal output block (maintenance fragility). Source: user-advocate R2 Recommendation 5 (modified per dispute resolution), developer-advocate dispute.

**P2-Onboard-14. Add "Next steps" section to quickstart.** [Docs change]
Two tracks: "Explore conversus" (modes, guided workflow, MCP setup) and "Build with conversus" (SDK, building plugins, building domains). Source: R1 UA-7 (unchallenged).

**P2-Onboard-15. Export `estimate_cost_usd()` to SDK guide.** [Docs change]
Add "Cost estimation in USD" subsection showing `from engine.cost import estimate_cost_usd`. Converged (R1 bilateral). Source: R1 CV-7.

**P2-Onboard-16. Add import namespace note to SDK guide.** [Docs change]
"The SDK spans two packages: `engine` for the deliberation runtime and `conversus` for schemas and plugins. Both are installed together." Cross-reference architecture.md. Decouple from the `classify` re-export code change. Source: developer-advocate R2 Recommendation 7 (modified).

**P3-Onboard-17. Add `--phase` parameter documentation note.** [Docs change]
"Currently, `--phase` supports `all` (default) and `review`. Additional phase options are planned." Source: R1 CV-9 (unchallenged; now partially addressed by P1-Onboard-3).

**P3-Onboard-18. Add `conversus status` to quickstart.** [Docs change]
After the "Try with a real provider" section. Converged (R2 unanimous). Source: R1 DA-10, R2 all agents.

**P3-Onboard-19. Add "What you will see" per-mode output description to modes.md.** [Docs change]
One sentence per mode describing synthesis shape. Source: user-advocate R2 Recommendation 9 (unchallenged).

**P3-Onboard-20. Add minimal starter config callout to config-reference.md.** [Docs change]
6-line minimal config at top with "This is all you need. Everything below documents optional fields." Source: R1 UA-9, R2 developer-advocate Recommendation 10 (unchallenged).

### Track 3: Extensibility (deepest impact for developer audience)

**P1-Ext-1. Add end-to-end domain tutorial to building-domains.md.** [Docs change]
Add "Running your domain" section demonstrating 5-stage lifecycle as a connected flow: (a) `DomainContext(workspace=Path("."), changed_files=[Path("src/app.py")], metadata={"commit_message": "feat: add caching"})` -- note `list[Path]` not `list[str]`; (b) `variables = domain.extract(context)`; (c) `score = domain.score(variables, "default")` -- scaffold name is a string, resolved to YAML; (d) `record = domain.create_record(score, context)`; (e) `store = JSONLStore(Path("./reviews")); store.append(record)`; (f) cross-reference API router mounting. Include self-contained setup preamble (`git clone` + `uv sync`). All code examples must be verified against source type annotations. Source: R1 DA-1, R2 developer-advocate Recommendation 1 (modified).

**P1-Ext-2. Add practical plugin wiring steps to building-plugins.md + `plugins:` key to config-reference.md.** [Docs change, single deliverable]
(a) Update "Dynamic loading" section: `package` is a Python dotted import path; module must be on `sys.path`; `pip install -e .` for local development; loader finds first Plugin subclass by alphabetical attribute name -- define exactly one per module; failure is non-fatal (warning + skip). (b) Add `plugins:` section to config-reference.md in "Advanced / Extensibility" subsection: `name` (string), `package` (Python import path), `config` (optional, defaults to `{}`). These ship together. Converged (R2 unanimous). Source: R1 DA-2, R1 Convergence #3, R2 developer-advocate Recommendation 2, user-advocate New Recommendation 1.

**P2-Ext-3. Add narrative prose and `members:` list to API reference pages.** [Docs change]
Add layered prose to `api/plugins/base.md`, `api/domains/base.md`, `api/schemas/construction.md`: one accessible sentence, plain-text class catalog with one-sentence descriptions per member (works on GitHub), cross-link to developer guide. Add explicit `members:` list to `domains/base.md`: `DomainPlugin`, `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, `Scaffold`, `VariableExtractor`, `load_scaffold`. Add `DomainStore`, `JSONLStore`, `SQLiteStore` coverage. Converged (R2 unanimous with dual-surface modification). Source: R1 Convergence #4, R2 code-verifier Recommendation 6 (modified).

**P2-Ext-4. Fix `determine_verdict` documentation.** [Docs change]
Split into "Default behavior" (base class checks hard blocks then per-dimension thresholds) and "Customizing verdict logic" (show `minimum_overall` pattern as explicit override, demonstrate `dimensions`/`variables` params). Converged (R1 bilateral). Source: R1 CV-8/DA-7.

**P2-Ext-5. Add error handling guidance for plugin and domain authors.** [Docs change]
Descriptive: "The framework catches and logs exceptions from extractors and plugins. A failed extractor's variables are absent from the merged dict. A failed plugin's results are absent from `state.plugin_results`." Prescriptive: "Raise freely; use `state.plugin_results.get('key', default)` for consumed data; check warning-level logs for skip messages during development." Source: R1 DA-5, R2 developer-advocate Recommendation 5 (corrected), code-verifier cross-review correction.

**P2-Ext-6. Add testing examples for plugins and domains.** [Docs change]
Add "Testing your plugin" section with minimal `DeliberationState` construction and assertion. Add domain equivalent with `DomainContext`. All constructor calls must match source type annotations. Source: R1 DA-6, R2 developer-advocate Recommendation 6.

**P2-Ext-7. Add domain-engine integration subsection to architecture.md.** [Docs change]
After pipeline data flow diagram: domains are invoked outside the pipeline (via API router or developer script); `equilibrium_score` bridges plugin and domain systems. Source: R1 DA-8, R2 developer-advocate Recommendation 4 (unchallenged).

**P3-Ext-8. Document hard block function dispatch differences.** [Docs change]
Note that `_check_hard_blocks` supports only three-part comparison form; `DomainPlugin.evaluate_hard_blocks()` supports all three forms. Source: R1 CV-C (unchallenged).

### Documentation principle

State in the implementation plan or contributing guide: "The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block should be self-contained. YAML configuration examples are exempt. Every SDK function shown in documentation whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case."

### Track ordering guidance

When resources are serial, prioritize by track order: code fixes first (smallest scope, highest confidence), then onboarding (broadest audience), then extensibility (deepest impact). When resources are parallel, all three tracks can proceed simultaneously. Items within a track are ordered by priority. Items across tracks have no ordering dependency. The domain tutorial (P1-Ext-1) includes its own setup preamble and does not depend on the index page install-path fix (P1-Onboard-1) being complete, though both are P1.

---

## Key Concessions

1. **code-verifier accepted the sync-first SDK Quick Start resolution** (Round 2 Alignment). "My original concern about 'conceptual mismatch' was valid architecturally but the synthesizer correctly identified that Quick Start sections are not read linearly. The practical risk (SyntaxError on first paste) outweighs the architectural purism." This fully resolves the Round 1 sync-first dispute.

2. **developer-advocate withdrew "return empty dicts rather than raising" for error handling** (Round 2 Revision). After code-verifier showed the framework already catches exceptions, developer-advocate accepted: "This is a factual error in my recommendation, and I withdraw the specific guidance about returning empty dicts."

3. **developer-advocate corrected the `DomainContext.changed_files` type in the domain tutorial example** (Round 2 Revision). Changed from `["src/app.py"]` (strings) to `[Path("src/app.py")]` (paths) per code-verifier's source verification.

4. **developer-advocate accepted the `score()` interface is documented, not ambiguous** (Round 2 Revision). "Code-verifier shows that `domains/base.py` L711-714 has explicit type annotations and a docstring. The gap is real... but the contract is not unclear."

5. **developer-advocate decoupled the import namespace explanation from the `classify` re-export** (Round 2 Revision). Per code-verifier: "The documentation note can ship independently of the code change, and should."

6. **user-advocate accepted `uv run` option (a) only** (Round 2 Revision). After developer-advocate identified that options (b) and (c) would create new contradictions, user-advocate withdrew options (b) and (c) and accepted P2 for the single-note approach.

7. **user-advocate accepted P2 for provider default mismatch conditionally** (Round 2 Disputes). "I will accept P2 if the synthesis commits to the warning callout format (not inline prose) and places it prominently." The synthesis commits to the admonition callout format.

8. **code-verifier acknowledged the index page was a blind spot in Round 1** (Round 2 cross-review). "My Round 2 review did not examine the index page at all -- I focused on source code verification. User-advocate correctly identified this as a gap that all three Round 1 agents missed."

9. **All three agents accepted the parallel-tracks implementation framing** (Round 2 Revisions). No agent reverses this Round 1 synthesis resolution. developer-advocate notes it "should not be deprioritized" but accepts the framing.

10. **code-verifier acknowledged user-advocate's "copy-paste test" is a stronger framing** (Round 2 cross-review). "This is not a reversal of my position -- it is an acknowledgment that user-advocate's framing provides a durable principle that I should have adopted in my own review."
