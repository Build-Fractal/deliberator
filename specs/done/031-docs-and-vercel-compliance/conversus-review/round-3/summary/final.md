# Neutral Synthesis -- Round 3 (FINAL) -- Conversus Documentation Suite (Spec 031)

---

## Process Summary

- **Agents**: 3 -- code-verifier, user-advocate, developer-advocate
- **Mode**: cooperative (Round 3 of 3 -- FINAL)
- **Round 2 disputes entering this round**: 6
- **This round disputes**: 0 -- full convergence achieved

**Artifact counts (Round 3):**
- Phase 1 reviews: 3
- Phase 3 revisions: 3
- Phase 4 disputes: 3
- Round 1 convergence items carried forward: 7 (all reaffirmed, zero reversals)
- Round 2 convergence items carried forward: 8 (all reaffirmed, zero reversals)
- New convergence points in Round 3: 6 (all former disputes resolved)
- **Total convergence points: 21** (7 from Round 1 + 8 from Round 2 + 6 from Round 3)

**Recommendation flow (Round 3):**
- Recommendations entering Round 3: 28 items across 3 tracks + 1 documentation principle + track ordering guidance (all from the Round 2 synthesis)
- Recommendations modified in Phase 3: 0 structural modifications; 1 editorial refinement accepted (P2-Onboard-13 item text specificity)
- Recommendations surviving unmodified: 28 of 28
- New recommendations introduced: 0 (all three agents explicitly committed to no scope expansion)
- Disputes remaining: 0

**Dispute trajectory across all rounds:**
- Round 1: 7 disputes
- Round 2: 6 disputes (net -1; one Round 1 dispute resolved, several new emerged and others collapsed)
- Round 3: 0 disputes (net -6; all resolved with full three-way agreement)

**Deliberation health:** The pipeline achieved steady state. Three rounds produced monotonic convergence with no reversals of prior concessions, no re-opening of closed items, and no scope expansion in the final round. The three editorial tensions that remained after cross-review (track ordering wording, P2-Onboard-13 item text specificity, copy-paste test scope framing) are stylistic differences that do not affect what gets built, how it gets built, or in what order. All three agents independently confirmed readiness for implementation.

---

## Recommendation Scorecard

| # | Agent | Recommendation | Final Priority | Final Status | Notes |
|---|-------|---------------|----------------|-------------|-------|
| P1-Code-1 | code-verifier | Fix scaffolds endpoint YAML glob (`api.py` L208) | P1 | Converged (trilateral) | Single-line fix. Source-verified across all rounds. |
| P1-Code-2 | code-verifier | Fix epilog `--phase synthesis` to `--phase review` (`cli/__init__.py` L95) | P1 | Converged (trilateral) | Ships with P1-Onboard-3. |
| P2-Code-3 | code-verifier | Export `classify` from `engine/__init__.py` | P2 | Converged (trilateral) | Track separately from SDK namespace note. |
| P1-Onboard-1 | user-advocate | Reconcile install path on index page | P1 | Converged (trilateral) | Highest-severity first-contact defect. |
| P1-Onboard-2 | code-verifier / user-advocate | Fix index page "4 modes" across 4 locations | P1 | Converged (trilateral) | Includes card title "Deliberation Modes." |
| P1-Onboard-3 | code-verifier | Document `--phase review` behavior in cli.md | P1 | Converged (trilateral) | Ships with P1-Code-2. |
| P1-Onboard-4 | code-verifier | Add `decide` 4-mode clarifying note to cli.md | P1 | Converged (trilateral) | Round 1 convergence, unchanged. |
| P1-Onboard-5 | user-advocate / developer-advocate | Heading + explanation before slash commands in quickstart | P1 | Converged (trilateral) | "Try the guided workflow (in your AI editor)" heading. |
| P1-Onboard-6 | user-advocate | Prerequisites callout to quickstart | P1 | Converged (trilateral) | Python 3.12+ and uv. |
| P2-Onboard-7 | user-advocate / code-verifier | `uv run` prefix note at top of cli.md | P2 | Converged (trilateral) | Option A only. |
| P2-Onboard-8 | developer-advocate | SDK sync-first Quick Start with async-context note | P2 | Converged (trilateral) | Resolves Round 1 dispute. |
| P2-Onboard-9 | code-verifier | Three-way provider default warning in config-reference.md | P2 | Converged (trilateral) | Admonition callout format. Dispute 1 resolved. |
| P2-Onboard-10 | code-verifier | SDK happy-path-only failure-mode annotations | P2 | Converged (trilateral) | Three instances: `cost_estimate`, `construct_objective`, `classify`. |
| P2-Onboard-11 | code-verifier | Provider default model table in cli.md | P2 | Converged (trilateral) | Unchallenged across all rounds. |
| P2-Onboard-12 | user-advocate / developer-advocate | State MkDocs as primary reading surface | P2 | Converged (trilateral) | Include `uv run mkdocs serve` build instructions. |
| P2-Onboard-13 | user-advocate | Abbreviated output description in quickstart | P2 | Converged (trilateral) | Hybrid prose + `--format json` tip. Dispute 4 resolved. |
| P2-Onboard-14 | user-advocate | "Next steps" section in quickstart | P2 | Converged (trilateral) | Two tracks: explore and build. |
| P2-Onboard-15 | code-verifier | `estimate_cost_usd()` in SDK guide | P2 | Converged (trilateral) | Bilateral convergence from Round 1. |
| P2-Onboard-16 | developer-advocate | Import namespace note in SDK guide | P2 | Converged (trilateral) | Decoupled from classify re-export code change. |
| P3-Onboard-17 | code-verifier | `--phase` parameter documentation note | P3 | Converged (trilateral) | Partially addressed by P1-Onboard-3. |
| P3-Onboard-18 | developer-advocate | `conversus status` in quickstart | P3 | Converged (trilateral) | After "Try with a real provider." |
| P3-Onboard-19 | user-advocate | "What you will see" per-mode output in modes.md | P3 | Converged (trilateral) | Unchallenged across all rounds. |
| P3-Onboard-20 | developer-advocate | Minimal starter config callout in config-reference.md | P3 | Converged (trilateral) | 6-line minimal config. |
| P1-Ext-1 | developer-advocate | End-to-end domain tutorial in building-domains.md | P1 | Converged (trilateral) | Self-contained preamble. Dispute 2 resolved. |
| P1-Ext-2 | developer-advocate | Plugin wiring steps + `plugins:` config key | P1 | Converged (trilateral) | Single deliverable. Loader docs corrected. |
| P2-Ext-3 | code-verifier | Narrative prose + `members:` list on API reference pages | P2 | Converged (trilateral) | Dual-surface: GitHub + MkDocs. |
| P2-Ext-4 | code-verifier / developer-advocate | `determine_verdict` documentation split | P2 | Converged (trilateral) | Default behavior + customization pattern. |
| P2-Ext-5 | developer-advocate | Error handling guidance | P2 | Converged (trilateral) | Descriptive + prescriptive. Dispute 5 resolved. |
| P2-Ext-6 | developer-advocate | Testing examples for plugins/domains | P2 | Converged (trilateral) | Constructor calls match source types. |
| P2-Ext-7 | developer-advocate | Domain-engine integration in architecture.md | P2 | Converged (trilateral) | Unchallenged across all rounds. |
| P3-Ext-8 | code-verifier | Hard block function dispatch differences | P3 | Converged (trilateral) | Source-verified. Unchallenged. |

**Scorecard totals:** 31 items (28 implementation + 1 documentation principle + 1 track ordering guidance + 1 open implementer annotation). All 28 implementation items ratified by all 3 agents. Zero items disputed, deferred, or withdrawn.

---

## Convergence Achieved

### Round 1 Convergence (7 items -- all reaffirmed in Rounds 2 and 3)

1. `decide` 4-mode restriction note in cli.md (unanimous)
2. Scaffolds endpoint YAML glob fix (trilateral)
3. `plugins:` key in config-reference.md (unanimous)
4. API reference narrative prose above autodoc directives (unanimous)
5. `determine_verdict` split: default behavior + custom override (bilateral)
6. Provider precedence note in cli.md (unanimous)
7. `estimate_cost_usd()` in SDK guide (bilateral)

### Round 2 Convergence (8 items -- all reaffirmed in Round 3)

8. `pip install conversus` index page fix (unanimous)
9. CLI epilog fix + `--phase review` documentation as single P1 deliverable (unanimous)
10. `uv run` prefix note at top of cli.md, option A only (unanimous)
11. Slash command heading + explanation after CLI path completes (unanimous)
12. Plugin wiring steps paired with `plugins:` config-reference addition (unanimous)
13. Error handling documentation corrected per source -- "raise freely" (bilateral)
14. MkDocs declared as primary reading surface (unanimous)
15. SDK sync-first Quick Start with async-context note (unanimous)

### Round 3 Convergence (6 items -- all former disputes, now resolved)

16. **Provider default warning priority (Dispute 1):** Resolved at P2 with admonition/warning callout in config-reference.md. The failure mode is safe (mock output, no money spent, no incorrect decisions). The callout format gives adequate visibility. Follow-up code issue for CLI fallback to `config.provider` is outside spec 031 scope. All three agents accept.

17. **Domain tutorial gating (Dispute 2):** Resolved with no inter-track dependency. The self-contained setup preamble (`git clone` + `uv sync` + `cd conversus`) makes the domain tutorial independently shippable regardless of the index page state. All three agents accept.

18. **Copy-paste test scope (Dispute 3):** Resolved with scoped principle. First complete code example on each SDK and quickstart page must be self-contained and runnable as `python script.py`. Incremental tutorial pages are exempt (opening setup block must be self-contained). YAML examples are exempt. All three agents arrive at the same set of affected pages from different definitional framings (page audience, content structure, literal text). No rewording needed. All three agents accept.

19. **Quickstart output format (Dispute 4):** Resolved with hybrid prose description. No literal terminal output block. The prose names the five phase headers (Review, Cross-review, Revision, Disputes, Synthesis) and the output structure (headline verdict + summary). A `--format json` note provides programmatic verification. Phase names are architecturally stable (derived from `engine/phases.py` and the template directory structure). All three agents accept.

20. **Error handling documentation (Dispute 5):** Resolved with both descriptive and prescriptive content. Descriptive section documents the framework's catch-and-skip behavior (source-verified at `domains/base.py` L697-708 and `plugins/base.py` L519-525). Prescriptive section provides three "recommended patterns" bullets, clearly labeled as recommendations rather than framework guarantees: (1) "Raise freely -- exceptions are caught and logged." (2) "Use `state.plugin_results.get('key', default)` for consumed data in case the producer failed." (3) "Check warning-level logs for plugin/extractor skip messages during development." The "recommended patterns" label is an epistemic boundary, not a soft hedge. All three agents accept.

21. **Implementation plan ordering (Dispute 6):** Resolved with three parallel tracks (Code Fixes, Onboarding, Extensibility), intra-track priority ordering, and no inter-track hard dependencies. When resources are serial, prioritize by track order: code fixes first, then onboarding, then extensibility. Developer-advocate's priority-tier interleaving alternative and user-advocate's track-sequential preference both produce identical documentation artifacts; the divergence is a scheduling heuristic, not a substantive disagreement. All three agents accept.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

**Dispute count: 0**

No disputes remain. All 6 disputes from Round 2 were resolved with full three-way agreement in Round 3. No new disputes were raised. Three editorial tensions persist (track ordering wording, P2-Onboard-13 item text specificity, copy-paste test scope framing) but all three agents explicitly declined to escalate them, noting they do not affect the implementation plan's content, scope, or ordering.

<!-- CONVERSUS:DISPUTES_END -->

---

## Actionable Spec Changes

### Track 1: Code Fixes (smallest scope, highest confidence)

**P1-Code-1. Fix scaffolds endpoint to glob YAML files.** [Code change]
Change `api.py` L208 from `domain.scaffold_dir.glob("*.json")` to iterate over `("*.yml", "*.yaml", "*.json")`. Source-verified across all three rounds. Single-line fix.

**P1-Code-2. Fix `run` command epilog `--phase synthesis` example.** [Code change]
Change `engine/cli/__init__.py` L95 from `--phase synthesis` to `--phase review`. Ships with P1-Onboard-3. Source-verified.

**P2-Code-3. Export `classify` from `engine/__init__.py`.** [Code change]
Add `classify` to `engine/__init__.py` exports. Track separately from the SDK namespace documentation note (P2-Onboard-16). File follow-up code issue for CLI to fall back to `config.provider` when `--provider` is at its default.

### Track 2: Onboarding (broadest audience, highest expected impact per hour)

**P1-Onboard-1. Reconcile install path on index page.** [Docs change]
Determine whether a PyPI `conversus` package exists. If not, replace `pip install conversus` on `docs/index.md` L29 with the quickstart's `git clone` + `uv sync` path. Also fix Quick Install section prerequisites (Python 3.12+, uv). The most dangerous first-contact defect identified across all three rounds.

**P1-Onboard-2. Fix index page "4 modes" claim across 4 locations.** [Docs change]
(a) Three Layers table L20: "4 competition modes" to "8 deliberation modes." (b) Quick Links card title: "Competition Modes" to "Deliberation Modes." (c) Quick Links mode list: expand to all 8 or replace with link to modes.md. (d) Add CLI subset qualifier.

**P1-Onboard-3. Document `--phase review` behavior in cli.md.** [Docs change]
Add to cli.md under the `--phase` option: "`review` runs Phase 1 only (individual agent reviews). Output: one review file per agent. Cross-review, revision, dispute, and synthesis phases are skipped." Ships with P1-Code-2.

**P1-Onboard-4. Add `decide` 4-mode clarifying note to cli.md.** [Docs change]
Add under `decide` options: "The `decide` command supports 4 modes for ad-hoc use. For the remaining 4 modes (negotiation, resource-allocation, fair-division, mechanism-design), use `conversus run` with a config file. See [Deliberation Modes](modes.md) for all 8."

**P1-Onboard-5. Add heading + explanation before slash commands in quickstart.md.** [Docs change]
Add heading "## Try the guided workflow (in your AI editor)" after the CLI path completes (after "Try with a real provider"). Add 2-sentence explanation: "The following commands are slash commands for AI coding assistants like Claude Code or Cursor. They are not terminal commands. See [MCP Setup](mcp-setup.md) to configure your editor."

**P1-Onboard-6. Add prerequisites callout to quickstart.** [Docs change]
Add at top: "Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/)." In the install code block: `# Requires Python 3.12+ and uv (https://docs.astral.sh/uv/). Alternative: pip install -e .`.

**P2-Onboard-7. Add `uv run` prefix note at top of cli.md.** [Docs change]
"Examples below use bare `conversus` commands. If you installed via `uv sync` (as in the quickstart), prefix with `uv run` (e.g., `uv run conversus run config.yml`). If you installed via `pip install -e .`, the commands work directly." Option A only; options B and C explicitly rejected by all agents.

**P2-Onboard-8. Write SDK Quick Start with sync-first code block.** [Docs change]
Lead with `asyncio.run()` wrapper as the first code block. Add `# Save as script.py and run: python script.py` comment. Note immediately below: "The SDK is async-native. Event subscriptions require async context -- see Event Subscription below for `await`-based usage."

**P2-Onboard-9. Add three-way provider default warning to config-reference.md.** [Docs change]
Use admonition/warning callout at the `provider:` field: "Warning: When `provider` is omitted, the config defaults to `anthropic`. However, CLI `--provider` defaults to `mock` and takes full precedence over the config file. If you omit both, the CLI wins and you get mock output. Set `provider:` explicitly in your config to avoid surprises." Also add the provider precedence note to cli.md.

**P2-Onboard-10. Add SDK happy-path-only failure-mode annotations.** [Docs change]
Add inline annotations to `sdk.md` for: (a) `Deliberation.cost_estimate` -- "Returns `None` if the config cannot be parsed." (b) `construct_objective()` -- "Raises `ValueError` if no templates match. `NonInteractiveGapFiller` raises `RuntimeError` on parameters without defaults." (c) `classify()` -- "Raises `ValueError` if no keyword patterns match." **Implementer note**: None of the three reviewers independently verified the `cost_estimate` return type (`dict | None` vs. always `dict`). The annotation is safe regardless -- harmless if always `dict`, essential if `| None`. Verify the actual return type before writing the annotation text.

**P2-Onboard-11. Add provider default model table to cli.md.** [Docs change]
"| Provider | Default Model | | anthropic | claude-sonnet-4-20250514 | | openai | gpt-4o |"

**P2-Onboard-12. State MkDocs as primary reading surface.** [Docs change]
Add to index page or developer guide: "This documentation is built with MkDocs Material. API reference pages use mkdocstrings and require a built site to render fully. To build locally: `uv run mkdocs serve`."

**P2-Onboard-13. Add abbreviated output description to quickstart "What just happened" section.** [Docs change]
No literal terminal output block. The prose description should name the five phase headers (Review, Cross-review, Revision, Disputes, Synthesis) and the output structure (headline verdict + summary) so the user knows what to look for. Include a note: "Run with `--format json` to verify the phase structure programmatically."

**P2-Onboard-14. Add "Next steps" section to quickstart.** [Docs change]
Two tracks: "Explore conversus" (modes, guided workflow, MCP setup) and "Build with conversus" (SDK, building plugins, building domains).

**P2-Onboard-15. Export `estimate_cost_usd()` to SDK guide.** [Docs change]
Add "Cost estimation in USD" subsection showing `from engine.cost import estimate_cost_usd`.

**P2-Onboard-16. Add import namespace note to SDK guide.** [Docs change]
"The SDK spans two packages: `engine` for the deliberation runtime and `conversus` for schemas and plugins. Both are installed together." Cross-reference architecture.md. Decoupled from the `classify` re-export code change (P2-Code-3).

**P3-Onboard-17. Add `--phase` parameter documentation note.** [Docs change]
"Currently, `--phase` supports `all` (default) and `review`. Additional phase options are planned." Partially addressed by P1-Onboard-3.

**P3-Onboard-18. Add `conversus status` to quickstart.** [Docs change]
After the "Try with a real provider" section.

**P3-Onboard-19. Add "What you will see" per-mode output description to modes.md.** [Docs change]
One sentence per mode describing synthesis shape.

**P3-Onboard-20. Add minimal starter config callout to config-reference.md.** [Docs change]
6-line minimal config at top with "This is all you need. Everything below documents optional fields."

### Track 3: Extensibility (deepest impact for developer audience)

**P1-Ext-1. Add end-to-end domain tutorial to building-domains.md.** [Docs change]
Add "Running your domain" section demonstrating 5-stage lifecycle as a connected flow: (a) `DomainContext(workspace=Path("."), changed_files=[Path("src/app.py")], metadata={"commit_message": "feat: add caching"})` -- note `list[Path]` not `list[str]`; (b) `variables = domain.extract(context)`; (c) `score = domain.score(variables, "default")` -- scaffold name is a string, resolved to YAML; (d) `record = domain.create_record(score, context)`; (e) `store = JSONLStore(Path("./reviews")); store.append(record)`; (f) cross-reference API router mounting. Include self-contained setup preamble (`git clone` + `uv sync` + `cd conversus`). All code examples must be verified against source type annotations.

**P1-Ext-2. Add practical plugin wiring steps to building-plugins.md + `plugins:` key to config-reference.md.** [Docs change, single deliverable]
(a) Update "Dynamic loading" section: `package` is a Python dotted import path; module must be on `sys.path`; `pip install -e .` for local development; loader finds first Plugin subclass by alphabetical attribute name -- define exactly one per module; failure is non-fatal (warning + skip). (b) Add `plugins:` section to config-reference.md in "Advanced / Extensibility" subsection: `name` (string), `package` (Python import path), `config` (optional, defaults to `{}`).

**P2-Ext-3. Add narrative prose and `members:` list to API reference pages.** [Docs change]
Add layered prose to `api/plugins/base.md`, `api/domains/base.md`, `api/schemas/construction.md`: one accessible sentence, plain-text class catalog with one-sentence descriptions per member (works on GitHub), cross-link to developer guide. Add explicit `members:` list to `domains/base.md`: `DomainPlugin`, `DomainContext`, `DomainScore`, `DomainRecord`, `TrendResult`, `Scaffold`, `VariableExtractor`, `load_scaffold`. Add `DomainStore`, `JSONLStore`, `SQLiteStore` coverage.

**P2-Ext-4. Fix `determine_verdict` documentation.** [Docs change]
Split into "Default behavior" (base class checks hard blocks then per-dimension thresholds) and "Customizing verdict logic" (show `minimum_overall` pattern as explicit override, demonstrate `dimensions`/`variables` params).

**P2-Ext-5. Add error handling guidance for plugin and domain authors.** [Docs change]
Descriptive section: "The framework catches and logs exceptions from extractors and plugins. A failed extractor's variables are absent from the merged dict. A failed plugin's results are absent from `state.plugin_results`." Prescriptive section (labeled "Recommended patterns"): (1) "Raise freely -- exceptions are caught and logged." (2) "Use `state.plugin_results.get('key', default)` for consumed data in case the producer failed." (3) "Check warning-level logs for plugin/extractor skip messages during development."

**P2-Ext-6. Add testing examples for plugins and domains.** [Docs change]
Add "Testing your plugin" section with minimal `DeliberationState` construction and assertion. Add domain equivalent with `DomainContext`. All constructor calls must match source type annotations.

**P2-Ext-7. Add domain-engine integration subsection to architecture.md.** [Docs change]
After pipeline data flow diagram: domains are invoked outside the pipeline (via API router or developer script); `equilibrium_score` bridges plugin and domain systems.

**P3-Ext-8. Document hard block function dispatch differences.** [Docs change]
Note that `_check_hard_blocks` (module-level function) supports only three-part comparison form (`variable operator threshold`); `DomainPlugin.evaluate_hard_blocks()` via `_evaluate_single_hard_block` supports all three forms (bare truthy check, comparison, boolean equality). Source-verified at `base.py` L306-352 vs. L378-461.

### Documentation Principles

State in the implementation plan or contributing guide:

> "The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block should be self-contained. YAML configuration examples are exempt. Every SDK function shown in documentation whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case."

This principle comprises two sub-principles ratified by all three agents:

1. **Copy-paste test (scoped):** First complete code examples on SDK and quickstart pages must be self-contained and runnable. Incremental tutorials are exempt; their opening setup block must be self-contained. YAML examples are exempt.

2. **Failure-mode annotations:** Every SDK function documented whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case. This prevents the recurrence of the happy-path-only documentation pattern identified in Round 2.

### Track Ordering Guidance

Items across tracks have no hard ordering dependency. When resources are serial, the track order (code fixes, onboarding, extensibility) reflects implementation priority. The domain tutorial and plugin wiring steps include self-contained setup preambles that allow them to ship independently of onboarding fixes.

When resources are serial, prioritize by track order: code fixes first (smallest scope, highest confidence, mergeable in under an hour), then onboarding (broadest audience, highest expected impact per hour), then extensibility (deepest impact for developer audience). When resources are parallel, all three tracks can proceed simultaneously. Items within a track are ordered by priority (P1 before P2 before P3).

Developer-advocate's alternative serial model (interleave P1 items across all tracks before moving to P2, with track order as tiebreaker within a priority tier) is equally valid and produces the same documentation artifacts. The choice between track-sequential and priority-interleaved scheduling is left to the implementer.

---

## Documentation Principles

The two documentation principles below were ratified unanimously by all three agents across Rounds 2 and 3. They serve as standing guidelines for the conversus documentation suite to prevent recurrence of the two systemic issues identified during this review.

### Principle 1: Copy-Paste Test

The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification.

**Exemptions:**
- Tutorial pages that build incrementally are exempt, but their opening setup block must be self-contained.
- YAML configuration examples are exempt (not executable in the same sense).
- Extensibility guide pages (building-plugins.md, building-domains.md) are covered by the tutorial exemption -- their opening setup blocks must be self-contained, but subsequent stages build incrementally.

**Rationale:** This principle prevents the recurrence of non-runnable code examples (e.g., bare `await` in SDK Quick Start) by establishing a testable expectation for documentation contributors.

### Principle 2: Failure-Mode Annotations

Every SDK function shown in documentation whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case.

**Rationale:** This principle prevents the recurrence of happy-path-only documentation (e.g., `cost_estimate` shown as always returning a dict, `construct_objective()` not mentioning its `ValueError`/`RuntimeError` cases) by requiring failure-mode visibility wherever SDK functions are demonstrated.

---

## Key Concessions

### Code-verifier concessions (all stable, no reversals)

1. **Accepted sync-first SDK Quick Start** (Round 2). "The practical risk (SyntaxError on first paste) outweighs the architectural purism."
2. **Acknowledged the index page was a blind spot in Round 1** (Round 2). User-advocate correctly identified the `pip install conversus` defect that all three Round 1 agents missed.
3. **Accepted user-advocate's copy-paste test as a stronger framing** (Round 2). "User-advocate's framing provides a durable principle."
4. **Acknowledged `cost_estimate` return type unverified** (Round 3). The annotation is safe regardless; the implementer should verify the actual return type.

### User-advocate concessions (all stable, no reversals)

5. **Provider default warning priority lowered from P1 to P2** (Round 2, conditional; condition met in Round 3). Accepted P2 with admonition callout format and prominent placement.
6. **`uv run` note priority lowered from P1 to P2** (Round 2).
7. **`uv run` options (b) and (c) withdrawn** (Round 2). Developer-advocate demonstrated they create new contradictions.
8. **Literal output block in quickstart withdrawn** (Round 3). The hybrid prose description is a genuine improvement.
9. **Hard inter-track gating withdrawn** (Round 3). Self-contained preambles eliminate the dependency.
10. **Copy-paste test scope narrowed** (Round 3). Accepted the scoped principle with tutorial and YAML exemptions.

### Developer-advocate concessions (all stable, no reversals)

11. **Withdrew "return empty dicts" error handling guidance** (Round 2). After code-verifier showed the framework catches exceptions, accepted: "Raise freely -- the framework catches and logs."
12. **Corrected `DomainContext.changed_files` type** (Round 2). Changed from `list[str]` to `list[Path]` per source verification.
13. **Accepted `score()` interface is typed and documented** (Round 2). The gap is demonstration coverage, not specification ambiguity.
14. **Decoupled import namespace note from `classify` re-export** (Round 2). Documentation ships independently from the code change.
15. **Accepted plugin loader uses alphabetical `dir()` order** (Round 2). Documentation says "define exactly one Plugin subclass per module."

### Process-level concessions

16. **All three agents accepted the parallel-tracks implementation framing** (Round 2, reaffirmed Round 3). No agent reversed this position.

---

## Open Implementer Annotations

One non-blocking annotation for the implementer, noted by all three reviewers:

- **`Deliberation.cost_estimate` return type:** None of the three reviewers independently verified whether `Deliberation.cost_estimate` returns `dict | None` or always `dict`. The P2-Onboard-10 failure-mode annotation is safe regardless (harmless if always `dict`, essential if `| None`). The implementer should verify the actual return type before writing the annotation text.

---

## Systemic Issues Identified (Carried from Round 2, Addressed by Plan)

1. **Install-path fragmentation across entry points.** The documentation presents at least three install paths (`pip install conversus`, `git clone` + `uv sync`, `pip install -e .`), with CLI reference and quickstart using different invocation prefixes. Addressed by P1-Onboard-1 (reconcile index page), P1-Onboard-6 (prerequisites), P2-Onboard-7 (`uv run` note), and self-contained setup preambles in extensibility tutorials.

2. **SDK documentation systematically hides failure modes.** Three verified instances where return types or exceptions are undocumented. Addressed by P2-Onboard-10 (instance fixes) and Documentation Principle 2 (recurrence prevention).

3. **Audience segmentation without explicit scoping.** The documentation serves three audiences (new users, SDK integrators, plugin/domain developers) without page-level audience markers. No agent in any round proposed a concrete audience-labeling mechanism. This remains an observed structural property of the documentation, mitigated but not resolved by the three-track implementation structure.

4. **Documentation-only vs. code fixes: approval threshold ambiguity.** Spec 031 is a docs-and-compliance spec, but three items are code changes. The process has no stated policy for whether code changes discovered through documentation review ship in the same spec or require separate tickets. The code fixes are included in Track 1 with [Code change] tags.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total rounds | 3 |
| Total agents | 3 |
| Total convergence points | 21 (7 + 8 + 6) |
| Disputes raised across all rounds | 13 (7 in R1, 6 in R2) |
| Disputes resolved | 13 (all) |
| Disputes remaining | 0 |
| Implementation items ratified | 28 |
| Documentation principles ratified | 2 |
| Concessions made | 16 (stable, no reversals) |
| New findings in Round 3 | 0 |
| Dangerous contradictions in Round 3 | 0 |
| Items by priority | P1: 10, P2: 15, P3: 6 (includes doc principle + ordering guidance) |
| Items by track | Code Fixes: 3, Onboarding: 20, Extensibility: 8 |

**Pipeline status: COMPLETE. Full three-way convergence achieved. Ready for implementation.**
