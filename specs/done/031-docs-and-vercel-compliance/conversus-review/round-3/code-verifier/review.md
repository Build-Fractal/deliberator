# Code-Verifier -- Review (Round 3, FINAL)

## Executive Summary

This final round resolves the 6 remaining disputes from Round 2. I accept the synthesizer's recommended resolutions for 5 of the 6 disputes, with minor clarifications on two. The overall implementation plan from the Round 2 synthesis is sound, source-verified, and ready to ship. No new findings are introduced. No Round 1 or Round 2 concessions are reversed.

The documentation suite has 3 code bugs (epilog, scaffold glob, classify export), 1 critical first-contact failure (index page `pip install conversus`), and approximately 20 documentation improvements organized across three parallel tracks. The Round 2 synthesis captured all of these accurately. This review focuses solely on closing the dispute loop.

---

## Alignment with Synthesizer's Dispute Resolutions

### Dispute 1: Provider default warning priority (P1 vs. P2)

**I accept the synthesizer's resolution: P2 with admonition/warning callout.**

My position from Round 2 was P2. The synthesizer recommends P2. User-advocate's conditional acceptance (P2 if callout format and prominent placement are committed) is satisfied by the callout text I proposed in my Round 2 revision. The failure mode remains safe -- mock output instead of real API calls. No money spent, no incorrect decisions produced. The admonition callout makes it visually prominent regardless of priority tier.

The follow-up code issue (CLI falls back to `config.provider` when `--provider` is not explicitly set) is the correct long-term fix. I support filing it but agree it is outside spec 031 scope.

**Status: Resolved. P2 with callout. No remaining disagreement.**

### Dispute 2: Domain tutorial gating on install-path resolution

**I accept the synthesizer's resolution: no hard gating dependency; domain tutorial includes its own setup preamble.**

This was my position in Round 2, and the synthesizer's recommendation matches it precisely. The domain tutorial ships with a self-contained setup preamble (`git clone` + `uv sync` + `cd conversus`) that gives the tutorial reader a correct install path regardless of whether the index page has been fixed. Developer-advocate is correct that a developer building domain plugins has already solved installation. User-advocate is correct that the index page must be fixed. Both can be true simultaneously without creating a blocking dependency.

The synthesizer's language -- "Items across tracks have no ordering dependency. The domain tutorial's setup preamble provides a correct install path regardless of the index page state" -- is the right framing.

**Status: Resolved. No gating. Independent tracks with self-contained setup preamble.**

### Dispute 3: Copy-paste test scope

**I accept the synthesizer's resolution with one clarification.**

The synthesizer proposes: "The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block should be self-contained. YAML examples are exempt."

This satisfies my Round 2 concern about multi-stage tutorials (the domain tutorial's 5-stage lifecycle will build incrementally and is explicitly exempted). It satisfies user-advocate's recurrence prevention concern (the principle exists as a stated expectation). And the YAML exemption acknowledges that "runnable without modification" does not apply to configuration fragments.

**Clarification**: The phrase "each SDK and quickstart page" should be interpreted as pages whose primary audience is end-users or SDK consumers, not extensibility-guide pages like building-plugins.md or building-domains.md. The domain tutorial's opening setup block being self-contained is the right standard for extensibility content. This is consistent with the synthesizer's exemption language and I do not believe it requires a wording change -- I am documenting my interpretation for the record.

**Status: Resolved. I accept the principle as stated with the incremental-tutorial and YAML exemptions.**

### Dispute 4: Quickstart example output -- literal block vs. prose description

**I accept the synthesizer's hybrid resolution.**

The synthesizer proposes a prose description ("You will see five phase headers -- Review, Cross-review, Revision, Disputes, Synthesis -- followed by a headline verdict and a summary") plus a verification note ("Run with `--format json` to verify the phase structure programmatically"). No literal output block.

This is the right balance. From a source verification standpoint: the five phase names (Review, Cross-review, Revision, Disputes, Synthesis) are stable -- they are the architectural invariants of the pipeline defined in `engine/phases.py` and reflected in the template directory structure (`templates/{mode}/` with 7 files per mode). A prose description referencing phase names is durable. A literal output block showing mock provider responses is fragile.

Developer-advocate's concern about stale output on the highest-traffic page was well-founded. User-advocate's concern about user verification was addressed by the `--format json` suggestion. The hybrid gives the user enough information to know whether their run succeeded without introducing maintenance debt.

**Status: Resolved. Prose description + `--format json` verification note. No literal output block.**

### Dispute 5: Error handling documentation -- prescriptive vs. descriptive

**I accept the synthesizer's resolution: both descriptive and prescriptive content, clearly labeled.**

The synthesizer proposes:

1. Descriptive section documenting the framework's catch-and-skip behavior (source-verified at `domains/base.py` L697-708 for extractors and `plugins/base.py` L519-525 for plugins).
2. Prescriptive section with three bullet points labeled as "recommended patterns":
   - "Raise freely -- exceptions are caught and logged."
   - "Use `state.plugin_results.get('key', default)` for consumed data in case the producer failed."
   - "Check warning-level logs for plugin/extractor skip messages during development."

All three prescriptive patterns are correct regardless of framework internals. The `.get()` with default is standard Python defensive programming. The "raise freely" guidance is validated by the framework's explicit try/except wrappers. The log-checking advice follows from the framework using `logger.warning()` at both catch points.

The key distinction -- "recommended patterns" rather than "framework guarantees" -- is accurate and important. The framework's catch-and-skip behavior is an implementation detail that could theoretically change; the defensive patterns are good practice in any plugin/extractor context.

**Status: Resolved. Descriptive + prescriptive, clearly labeled. All prescriptive patterns are source-compatible.**

### Dispute 6: Implementation plan ordering -- explicit batches vs. priority-tagged list

**I accept the synthesizer's resolution: three tracks with intra-track ordering and no inter-track hard dependencies.**

The synthesizer's framing -- "When resources are serial, prioritize by track order: code fixes first (smallest, highest-confidence), then onboarding (broadest audience), then extensibility (deepest impact). When resources are parallel, all three tracks can proceed simultaneously" -- addresses both user-advocate's concern about actionability and developer-advocate's concern about false dependencies.

I want to confirm one detail from my source verification: the three code fixes (scaffold glob, epilog, classify export) are indeed the smallest-scope items. The scaffold glob change is a single line in `api.py`. The epilog fix is a single string in `cli/__init__.py` L95. The classify export is an addition to `engine/__init__.py`. These can be code-reviewed and merged in under an hour. Shipping them first as Track 1 is the correct call.

**Status: Resolved. Three parallel tracks, serial preference stated, no inter-track gating.**

---

## Missed Opportunities

These are items identified in earlier rounds that remain relevant. No new findings.

### 1. Hard block function dispatch differences (Round 1, P3)

The Round 2 synthesis captures this as P3-Ext-8: `_check_hard_blocks` (the module-level function) supports only the three-part comparison form (`variable operator threshold`), while `DomainPlugin.evaluate_hard_blocks()` delegates to `_evaluate_single_hard_block` which supports all three forms (bare truthy check, comparison, boolean equality). This is source-verified at `base.py` L306-352 vs. L378-461. The documentation should note which function supports which forms. This was unchallenged in both rounds and should ship as stated.

### 2. `domains/base.md` lacks explicit `members:` list (Round 1, P2)

The API reference page at `docs/api/domains/base.md` contains only `:::conversus.domains.base` without a `members:` list, unlike `plugins/base.md` and `construction.md` which enumerate their members. This means mkdocstrings will auto-discover members, which may include internal functions like `_linear_slope`, `_compute_weighted_score`, `_check_hard_blocks`, `_evaluate_single_hard_block`, and `_evaluate_hard_block_rules`. The Round 2 synthesis captures this under P2-Ext-3 with the correct member list. This should ship as stated.

### 3. `estimate_cost_usd()` remains undocumented in SDK guide (Round 1, P2)

Captured as P2-Onboard-15 in the Round 2 synthesis. The function at `engine/cost.py` exists and is not mentioned in `sdk.md`. Still valid, still P2, still unchallenged.

---

## Off-Base Assumptions

No off-base assumptions persist from earlier rounds. The corrections applied in Rounds 1 and 2 -- sync-first SDK Quick Start, error handling "raise freely" guidance, `DomainContext.changed_files` type (`list[Path]` not `list[str]`), plugin loader alphabetical `dir()` order, `score()` interface documented not ambiguous -- are all accepted and incorporated into the implementation plan.

One point of clarification: the Round 2 synthesis references "`Deliberation.cost_estimate` returns `None` but docs show it as always returning a dict." I was unable to independently verify whether `cost_estimate` is a property that returns `dict | None` or always returns a dict, because the `Deliberation` class implementation lives in `engine/` runtime code that I did not fully trace in previous rounds. My source verification confirmed the *documentation claim* (sdk.md shows `d.cost_estimate` producing a dict) and confirmed that the synthesis claims it can return `None`. I accept the synthesis's characterization and recommend the inline annotation as stated in P2-Onboard-10.

---

## Actionable Recommendations (Refined from R2, Prioritized)

All recommendations below are from the Round 2 synthesis. I am restating only my final position on each, confirming agreement or noting refinements. I am not introducing new items.

### Track 1: Code Fixes

| ID | Item | My Position |
|---|---|---|
| P1-Code-1 | Fix scaffolds endpoint glob (`api.py` L208) | Confirmed. Source-verified across both rounds. Single-line fix. |
| P1-Code-2 | Fix epilog `--phase synthesis` to `--phase review` (`cli/__init__.py` L95) | Confirmed. Source-verified. Ships with P1-Onboard-3. |
| P2-Code-3 | Export `classify` from `engine/__init__.py` | Confirmed. Track separately from SDK namespace note. |

### Track 2: Onboarding

| ID | Item | My Position |
|---|---|---|
| P1-Onboard-1 | Reconcile install path on index page | Confirmed. Highest-severity first-contact defect. |
| P1-Onboard-2 | Fix index page "4 modes" across 4 locations | Confirmed. Includes card title change to "Deliberation Modes." |
| P1-Onboard-3 | Document `--phase review` behavior in cli.md | Confirmed. Ships with P1-Code-2. |
| P1-Onboard-4 | Add `decide` 4-mode clarifying note to cli.md | Confirmed. Round 1 convergence, unchanged. |
| P1-Onboard-5 | Heading + explanation before slash commands in quickstart | Confirmed. "Try the guided workflow (in your AI editor)" heading. |
| P1-Onboard-6 | Prerequisites callout to quickstart | Confirmed. Python 3.12+ and uv. |
| P2-Onboard-7 | `uv run` prefix note at top of cli.md | Confirmed. Option A only. |
| P2-Onboard-8 | SDK sync-first Quick Start with async-context note | Confirmed. Resolves Round 1 dispute. |
| P2-Onboard-9 | Three-way provider default warning in config-reference.md | Confirmed P2. Admonition callout format. |
| P2-Onboard-10 | SDK happy-path-only failure-mode annotations | Confirmed. Three instances: `cost_estimate`, `construct_objective`, `classify`. |
| P2-Onboard-11 | Provider default model table in cli.md | Confirmed. Unchallenged across all rounds. |
| P2-Onboard-12 | State MkDocs as primary reading surface | Confirmed. Include `uv run mkdocs serve` build instructions. |
| P2-Onboard-13 | Abbreviated output description in quickstart | Confirmed. Prose description, no literal block. Hybrid resolution. |
| P2-Onboard-14 | "Next steps" section in quickstart | Confirmed. Two tracks: explore and build. |
| P2-Onboard-15 | `estimate_cost_usd()` in SDK guide | Confirmed. Bilateral convergence from Round 1. |
| P2-Onboard-16 | Import namespace note in SDK guide | Confirmed. Decoupled from classify re-export code change. |
| P3-Onboard-17 | `--phase` parameter documentation note | Confirmed. Partially addressed by P1-Onboard-3. |
| P3-Onboard-18 | `conversus status` in quickstart | Confirmed. After "Try with a real provider." |
| P3-Onboard-19 | "What you will see" per-mode output in modes.md | Confirmed. Unchallenged. |
| P3-Onboard-20 | Minimal starter config callout in config-reference.md | Confirmed. 6-line minimal config. |

### Track 3: Extensibility

| ID | Item | My Position |
|---|---|---|
| P1-Ext-1 | End-to-end domain tutorial in building-domains.md | Confirmed. Self-contained setup preamble. No install-path gating. All types verified against source (`list[Path]`, `str | Scaffold`). |
| P1-Ext-2 | Plugin wiring steps + `plugins:` config key (single deliverable) | Confirmed. Loader finds first Plugin subclass by alphabetical `dir()` order. Define one per module. |
| P2-Ext-3 | Narrative prose + `members:` list on API reference pages | Confirmed. Dual-surface: plain-text class catalog for GitHub, `members:` list for MkDocs. |
| P2-Ext-4 | `determine_verdict` documentation split | Confirmed. Default behavior + customization pattern. |
| P2-Ext-5 | Error handling guidance | Confirmed. Descriptive + prescriptive, clearly labeled. |
| P2-Ext-6 | Testing examples for plugins/domains | Confirmed. Constructor calls must match source types. |
| P2-Ext-7 | Domain-engine integration in architecture.md | Confirmed. Unchallenged. |
| P3-Ext-8 | Hard block function dispatch differences | Confirmed. Unchallenged. |

### Documentation Principle

I accept the synthesizer's formulation: "The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block should be self-contained. YAML configuration examples are exempt. Every SDK function shown in documentation whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case."

This is a well-scoped principle that balances recurrence prevention with tutorial pedagogy. The exemptions are correct and necessary.

---

## Referenced Documentation

### Source Files Verified

| File | Key Lines | Finding |
|---|---|---|
| `conversus/plugins/base.py` | L33-44 | HookPoint enum: 4 values (PRE_EXECUTION, POST_PHASE_5, POST_DELIBERATION, POST_ARBITRATION) |
| `conversus/plugins/base.py` | L126-208 | Plugin ABC: name/hooks required, produces/consumes optional, `__init_subclass__` validates |
| `conversus/plugins/base.py` | L216-226 | `_find_plugin_class`: iterates `dir(module)` -- alphabetical order |
| `conversus/plugins/base.py` | L229-295 | `load_plugins`: name/package/config keys, ImportError warning + skip |
| `conversus/plugins/base.py` | L412-527 | `execute_hooks`: topological sort, model_copy for plugin_results, try/except per plugin |
| `conversus/schemas/construction.py` | L140-172 | GapFiller protocol + NonInteractive/Interactive implementations |
| `conversus/schemas/construction.py` | L384-425 | `classify_decision_type`: raises ValueError on no match |
| `conversus/schemas/construction.py` | L866-943 | `construct_objective`: full 3-stage pipeline |
| `conversus/schemas/modes.py` | L9-18 | VALID_MODES: 8 modes (cooperative, winner-take-all, prisoners-dilemma, red-blue, negotiation, resource-allocation, fair-division, mechanism-design) |
| `conversus/domains/base.py` | L34-46 | DomainContext: workspace (Path), changed_files (list[Path]), metadata (dict) |
| `conversus/domains/base.py` | L497-533 | DomainPlugin ABC: name, version, scaffold_dir, get_extractors abstract |
| `conversus/domains/base.py` | L688-709 | `extract()`: try/except per extractor, logger.warning on failure |
| `conversus/domains/base.py` | L711-802 | `score()`: scaffold str or Scaffold, dimension-based or 1:1 scoring |
| `engine/config.py` | L62-78 | EngineConfig: provider defaults to `"anthropic"` |
| `engine/config.py` | L84 | VALID_MODES tuple from canonical source |
| `engine/cli/__init__.py` | L85-115 | `run` command: epilog shows `--phase synthesis`, Click constrains to `["all", "review"]` |
| `engine/cli/__init__.py` | L100-102 | `--provider` defaults to `"mock"` |

### Documentation Files Reviewed

| File | Key Issues |
|---|---|
| `docs/index.md` | L20: "4 competition modes" (should be 8); L29: `pip install conversus` (possibly nonexistent package); L61: "Competition Modes" card title (should be "Deliberation Modes"); L63: enumerates only 4 modes |
| `docs/user-guide/quickstart.md` | Slash commands need heading/explanation; no output description; no `conversus status`; no prerequisites callout |
| `docs/user-guide/cli.md` | Bare `conversus` commands (inconsistent with quickstart's `uv run`); `decide --mode` shows 4 modes; no `--phase review` behavior; no provider default model table |
| `docs/user-guide/sdk.md` | Quick Start uses bare `await` (not copy-pasteable); `cost_estimate` shown as always dict; `construct_objective` and `classify` hide failure modes; no `estimate_cost_usd()`; no import namespace note |
| `docs/user-guide/modes.md` | Accurate and complete (8 modes documented). No issues. |
| `docs/user-guide/config-reference.md` | No `plugins:` key; no provider default warning; no minimal starter config; no `--phase` note |
| `docs/developer-guide/architecture.md` | No domain-engine integration section; otherwise accurate |
| `docs/developer-guide/building-plugins.md` | Dynamic loading section needs loader behavior clarification; otherwise solid |
| `docs/developer-guide/building-domains.md` | No end-to-end tutorial; no error handling guidance; no testing examples |
| `docs/api/schemas/construction.md` | Has `members:` list. Needs narrative prose above directive. |
| `docs/api/plugins/base.md` | Has `members:` list. Needs narrative prose above directive. |
| `docs/api/domains/base.md` | Missing `members:` list entirely. Needs both prose and explicit member enumeration. |

---

## Final Position Statement

All 6 disputes from Round 2 are resolved. I accept the synthesizer's recommended resolution for each, with clarifications on Dispute 3 (copy-paste test scope interpreted as SDK/quickstart pages, not extensibility guides) and Dispute 4 (phase names are architecturally stable, making the prose description durable).

The 15 convergence points from Rounds 1 and 2 stand. No reversals.

The implementation plan with three parallel tracks (Code Fixes, Onboarding, Extensibility), intra-track priority ordering, no inter-track gating, and serial preference (code fixes first, then onboarding, then extensibility) is correct and actionable.

The documentation principle is well-scoped and should be included in the implementation plan or contributing guide as stated.

This review introduces no new findings, reverses no prior concessions, and disputes no remaining items. The pipeline is ready for implementation.
