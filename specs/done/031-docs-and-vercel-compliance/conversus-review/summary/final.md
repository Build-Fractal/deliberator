# Cross-Round Synthesis -- Conversus Documentation Suite (Spec 031)

---

## Process Summary

| Metric | Round 1 | Round 2 | Round 3 | Total |
|--------|---------|---------|---------|-------|
| Agents | 3 | 3 | 3 | 3 (consistent) |
| Phase 1 reviews | 3 | 3 | 3 | 9 |
| Phase 2 cross-reviews | 6 | 6 | 0 | 12 |
| Phase 3 revisions | 3 | 3 | 3 | 9 |
| Phase 4 disputes | 3 | 3 | 3 | 9 |
| Recommendations proposed | 29 | 30 | 0 new | 37 unique (after dedup + merges) |
| Recommendations modified | 13 | 16 | 0 | 29 modifications |
| New recommendations added | 8 | 8 | 0 | 16 |
| Convergence points (cumulative) | 7 | 15 | 21 | 21 |
| Disputes remaining | 7 | 6 | 0 | 0 |
| Key concessions | 7 | 10 | 16 | 16 (cumulative, no reversals) |
| Dangerous contradictions found | 4 resolved + 1 unresolved | 5 resolved + 1 unresolved | 0 | 9 resolved + 0 unresolved |

**Termination**: Converged after 3 rounds. Round 3 resolved all 6 remaining disputes with full three-way agreement. No new disputes or recommendations were introduced in the final round. All 16 concessions made across the deliberation were stable with zero reversals.

**Documentation scope reviewed**: 11 target files across 3 documentation tiers (user guide: quickstart, CLI, modes, SDK, config-reference; developer guide: architecture, building-plugins, building-domains; API reference: schemas/construction, plugins/base, domains/base). The review also identified issues in `docs/index.md` (not an original target) and two source code files (`api.py`, `engine/cli/__init__.py`).

---

## Dispute Trajectory

### Summary Table

| Dispute | Appeared | Round 1 Status | Round 2 Status | Round 3 Status | Resolution Method |
|---------|----------|----------------|----------------|----------------|-------------------|
| SDK async-first vs. sync-first Quick Start | R1 | Open -- user-advocate vs. code-verifier + developer-advocate | Resolved (all accept sync-first with async note) | Reaffirmed | Agent convergence (R2): code-verifier conceded practical risk outweighs architectural purism |
| Onboarding vs. extensibility priority sequencing | R1 | Open -- user-advocate vs. developer-advocate | Evolved into Dispute: Domain tutorial gating | Resolved (parallel tracks, self-contained preambles) | Agent convergence (R3): user-advocate withdrew hard gating after developer-advocate demonstrated self-contained preamble removes dependency |
| Quickstart inline troubleshooting hints | R1 | Open -- user-advocate vs. code-verifier | Evolved into prerequisites callout (converged R2) | Reaffirmed | Agent convergence (R2): user-advocate narrowed scope to brief callout; code-verifier accepted |
| Provider precedence -- doc note vs. dead code | R1 | Open -- code-verifier vs. user-advocate + developer-advocate | Evolved into Dispute: Provider default warning priority | Resolved (P2 admonition callout + follow-up code issue) | Agent convergence (R3): user-advocate accepted P2 with admonition format; all agents accepted |
| `domains/base.md` member filtering | R1 | Open -- code-verifier vs. user-advocate + developer-advocate | Absorbed into API reference prose convergence (R2) | Reaffirmed | Synthesizer integration (R1): folded into API reference narrative prose work item with explicit `members:` list requirement |
| End-to-end domain tutorial priority | R1 | Open -- developer-advocate vs. user-advocate | Evolved into Dispute: Domain tutorial gating | Resolved (no gating, self-contained preamble) | Agent convergence (R3): merged with implementation ordering dispute |
| Plugin wiring documentation location | R1 | Open -- developer-advocate vs. code-verifier + user-advocate | Resolved (R2): paired with config-ref addition | Reaffirmed | Agent convergence (R2): user-advocate proposed pairing as single deliverable; all accepted |
| Provider default warning priority (P1 vs. P2) | R2 | N/A | Open -- user-advocate (P1) vs. code-verifier (P2) | Resolved (P2 with admonition callout) | Agent convergence (R3): user-advocate accepted P2 given admonition format and prominent placement |
| Domain tutorial gating on install-path resolution | R2 | N/A | Open -- user-advocate vs. developer-advocate + code-verifier | Resolved (no gating, self-contained preamble) | Agent convergence (R3): self-contained setup preamble eliminates dependency |
| Copy-paste test scope | R2 | N/A | Open -- user-advocate (all pages) vs. code-verifier (entry-point only) | Resolved (scoped principle with exemptions) | Agent convergence (R3): all three agents arrived at identical affected-page set from different definitional framings |
| Quickstart output format (literal vs. prose) | R2 | N/A | Open -- user-advocate (literal block) vs. developer-advocate (prose) | Resolved (hybrid prose + `--format json` tip) | Agent convergence (R3): user-advocate accepted hybrid as "genuine improvement" |
| Error handling -- prescriptive vs. descriptive | R2 | N/A | Open -- developer-advocate (prescriptive) vs. code-verifier (descriptive-only) | Resolved (both descriptive + prescriptive, clearly labeled) | Agent convergence (R3): all accept "recommended patterns" label as epistemic boundary |
| Implementation plan ordering | R2 | N/A | Open -- user-advocate (sequential batches) vs. developer-advocate (parallel tracks) | Resolved (three parallel tracks, intra-track priority ordering) | Agent convergence (R3): both scheduling models produce identical artifacts; choice left to implementer |

### Narrative: Multi-Round Dispute Evolution

**SDK sync-first vs. async-first (R1 -> R2 resolution).** This was the sharpest dispute in Round 1, with user-advocate arguing that a bare `await` as the first code block would cause `SyntaxError` on first paste, and code-verifier and developer-advocate arguing the SDK is architecturally async-first. The Round 1 synthesizer recommended leading with `asyncio.run()`. In Round 2, code-verifier made the pivotal concession: "The practical risk (SyntaxError on first paste) outweighs the architectural purism." Developer-advocate proposed tabbed code blocks; user-advocate accepted tabs but insisted the raw Markdown fallback must still be sync-first. By Round 2 revision, all three agents converged on `asyncio.run()` wrapper first with an async-context note below. This resolution held through Round 3 without challenge. The dispute resolved through code-verifier abandoning the "conceptual mismatch" argument after accepting the synthesizer's observation that Quick Start sections are not read linearly.

**Onboarding vs. extensibility priority (R1 -> R2 -> R3 resolution).** This dispute began in Round 1 as a disagreement between user-advocate (onboarding gates all downstream audiences) and developer-advocate (developers arrive via direct links, not the quickstart). The Round 1 synthesizer framed them as parallel independent tracks. In Round 2, the dispute evolved: user-advocate demanded explicit batching; developer-advocate resisted hard inter-track gating. A sub-dispute emerged about whether the domain tutorial depended on the install-path fix. The Round 2 synthesizer recommended self-contained setup preambles to eliminate the dependency. In Round 3, developer-advocate demonstrated that `git clone` + `uv sync` + `cd conversus` in the tutorial preamble makes it independently shippable. User-advocate withdrew hard gating: "Self-contained preambles eliminate the dependency." All three agents accepted the three-track structure with intra-track priority ordering and no inter-track hard dependencies. The dispute resolved through a design solution (self-contained preambles) rather than a priority negotiation.

**Provider default behavior (R1 -> R2 -> R3 resolution).** This dispute evolved across all three rounds with shifting scope. In Round 1, code-verifier identified that `config.provider` is dead code on the CLI path (never consulted by `run_engine()`). User-advocate and developer-advocate treated it as a documentation fix. In Round 2, the scope expanded: code-verifier discovered the three-way default mismatch (config defaults to `anthropic`, CLI defaults to `mock`, CLI wins silently). User-advocate elevated it to P1; code-verifier held at P2 because the failure mode is safe. In Round 3, user-advocate accepted P2 after the admonition callout format and prominent placement were committed. All agents agreed to file a follow-up code issue for the CLI to fall back to `config.provider`. The dispute resolved through a format commitment (admonition callout) that satisfied user-advocate's visibility concern at the lower priority level.

**Copy-paste test principle (R2 -> R3 resolution).** Emerged in Round 2 when user-advocate proposed "every first code example on a page should be self-contained and runnable" as a standing documentation principle. Code-verifier accepted it for entry-point pages but objected to generalizing it to multi-stage tutorials. Developer-advocate exempted YAML examples. The Round 2 synthesizer proposed scoped wording with explicit exemptions. In Round 3, all three agents arrived at the identical set of affected pages from different definitional framings (user-advocate by audience, code-verifier by content structure, developer-advocate by literal text). The agreement on scope was substantive despite the framing differences. The dispute resolved because the three distinct framings converged to the same practical outcome.

**Quickstart output format (R2 -> R3 resolution).** Emerged in Round 2 when user-advocate proposed a literal terminal output block and developer-advocate opposed it as a maintenance liability. The Round 2 synthesizer proposed a hybrid: prose description naming the five phase headers plus a `--format json` verification note. In Round 3, user-advocate accepted the hybrid as "a genuine improvement over both the literal block and the bare prose." Developer-advocate's maintenance concern and user-advocate's verification concern were both addressed. The dispute resolved through the synthesizer's hybrid proposal being accepted by both parties.

---

## Convergence Progression

### Round 1: Foundation Setting (7 convergence points, 7 disputes)

Round 1 established the factual foundation. The three agents -- code-verifier (source code accuracy), user-advocate (first-contact experience), developer-advocate (extensibility completeness) -- identified 29 recommendations across the 11-page documentation suite. Seven items converged immediately, generally where source code evidence was unambiguous: the `decide` command's 4-mode Click constraint, the scaffolds endpoint's JSON-only glob, the missing `plugins:` config key, the need for API reference prose, the `determine_verdict` documentation split, the provider precedence note, and the `estimate_cost_usd()` gap. Seven disputes remained, concentrated around two axes: (1) presentation ordering for mixed-audience content (SDK sync vs. async, onboarding vs. extensibility priority) and (2) scope boundaries for documentation changes (inline troubleshooting, domain tutorial priority, plugin wiring location).

**Convergence rate**: 7 of 14 contested items (50%).
**Character of disputes**: Primarily value-driven (audience prioritization) rather than factual. The one factual dispute (provider dead code) was partially resolved.

### Round 2: Discovery and Refinement (8 new convergence points, 6 disputes)

Round 2 introduced significant new findings that Round 1 missed entirely. The most consequential: the `pip install conversus` command on the index page (likely pointing to a nonexistent PyPI package), the `--phase synthesis` epilog bug (creating a broken self-help loop), and the systematic failure-mode omission pattern across SDK documentation. These discoveries widened the scope but also created new convergence opportunities -- all three agents immediately agreed on the P1 severity of the install-path and epilog defects.

Round 2 also resolved the sharpest Round 1 dispute (SDK sync-first) through code-verifier's concession, and produced important factual corrections: developer-advocate withdrew "return empty dicts" error handling guidance after code-verifier showed the framework catches exceptions; developer-advocate corrected `DomainContext.changed_files` type from `list[str]` to `list[Path]`.

Six disputes remained, but their character shifted from Round 1. Several were now scope/framing disagreements (copy-paste test scope, implementation ordering, error handling prescriptive vs. descriptive) rather than substantive content disagreements, which the Round 2 synthesizer noted as a signal that Round 3 should resolve most through precise wording.

**Convergence rate (cumulative)**: 15 of 21 total contested items (71%).
**Net dispute change**: -1 (7 to 6). One R1 dispute fully resolved; several new disputes emerged from new R2 findings while others collapsed. Convergence was occurring but not aggressively.

### Round 3: Full Convergence (6 new convergence points, 0 disputes)

Round 3 achieved complete convergence. All six remaining disputes were resolved with full three-way agreement. No new recommendations were introduced -- all three agents explicitly committed to no scope expansion. No prior convergence items were reversed. The resolution mechanisms varied:

- **Provider default priority**: Resolved through format commitment (admonition callout) that bridged the P1/P2 gap.
- **Domain tutorial gating**: Resolved through design solution (self-contained preamble) that eliminated the dependency.
- **Copy-paste test scope**: Resolved through convergence of three independent framings to the same affected-page set.
- **Quickstart output format**: Resolved through acceptance of the Round 2 synthesizer's hybrid proposal.
- **Error handling scope**: Resolved through the "recommended patterns" label as an epistemic boundary between framework guarantees and author guidance.
- **Implementation ordering**: Resolved by recognizing that both scheduling models (track-sequential and priority-interleaved) produce identical documentation artifacts.

Three editorial tensions persisted (track ordering wording, P2-Onboard-13 text specificity, copy-paste test framing) but all three agents explicitly declined to escalate them, noting they do not affect the implementation plan's content, scope, or ordering.

**Convergence rate (cumulative)**: 21 of 21 total contested items (100%).
**Net dispute change**: -6 (6 to 0). Full convergence.

---

## Final Recommendation Set

### Track 1: Code Fixes (3 items -- smallest scope, highest confidence)

| ID | Priority | Description | Type | Source |
|----|----------|-------------|------|--------|
| P1-Code-1 | P1 | Fix scaffolds endpoint to glob `("*.yml", "*.yaml", "*.json")` at `api.py` L208 | Code change | R1 convergence, R2 trilateral, R3 reaffirmed |
| P1-Code-2 | P1 | Fix `run` command epilog `--phase synthesis` to `--phase review` at `cli/__init__.py` L95 | Code change | R2 convergence (unanimous), R3 reaffirmed |
| P2-Code-3 | P2 | Export `classify` from `engine/__init__.py` | Code change | R1 unchallenged, R2 confirmed, R3 reaffirmed |

**Follow-up code issue**: File a separate issue for whether `run_engine()` should fall back to `config.provider` when `--provider` is at its default value.

### Track 2: Onboarding (20 items -- broadest audience, highest expected impact per hour)

| ID | Priority | Description | Type | Source |
|----|----------|-------------|------|--------|
| P1-Onboard-1 | P1 | Reconcile install path on index page (`pip install conversus` to `git clone` + `uv sync`) | Docs change | R2 convergence (unanimous), R3 reaffirmed. Most dangerous first-contact defect. |
| P1-Onboard-2 | P1 | Fix index page "4 modes" claim across 4 locations; change to "8 deliberation modes" with CLI subset qualifier | Docs change | R1 convergence, R2 expanded scope, R3 reaffirmed |
| P1-Onboard-3 | P1 | Document `--phase review` behavior in cli.md (ships with P1-Code-2) | Docs change | R2 convergence (unanimous), R3 reaffirmed |
| P1-Onboard-4 | P1 | Add `decide` 4-mode clarifying note to cli.md with cross-reference to modes.md | Docs change | R1 convergence (unanimous), stable across all rounds |
| P1-Onboard-5 | P1 | Add heading "Try the guided workflow (in your AI editor)" + 2-sentence slash command explanation in quickstart | Docs change | R1 unchallenged as P1, R2 placement refined, R3 reaffirmed |
| P1-Onboard-6 | P1 | Add prerequisites callout to quickstart (Python 3.12+, uv) | Docs change | R1 modified through cross-review, R2 converged, R3 reaffirmed |
| P2-Onboard-7 | P2 | Add `uv run` prefix note at top of cli.md (option A only) | Docs change | R2 convergence (unanimous), R3 reaffirmed |
| P2-Onboard-8 | P2 | Write SDK Quick Start with sync-first (`asyncio.run()`) code block + async-context note | Docs change | R1 dispute resolved in R2, R3 reaffirmed |
| P2-Onboard-9 | P2 | Add three-way provider default warning (admonition callout) to config-reference.md + cli.md precedence note | Docs change | R1 partial convergence, R2 format agreed, R3 priority resolved |
| P2-Onboard-10 | P2 | Add SDK failure-mode annotations for `cost_estimate`, `construct_objective`, `classify` | Docs change | R2 convergence (trilateral), R3 reaffirmed |
| P2-Onboard-11 | P2 | Add provider default model table to cli.md | Docs change | R1 unchallenged, stable across all rounds |
| P2-Onboard-12 | P2 | State MkDocs as primary reading surface with `uv run mkdocs serve` build instructions | Docs change | R2 convergence (unanimous), R3 reaffirmed |
| P2-Onboard-13 | P2 | Add abbreviated output description (hybrid prose + `--format json` tip) to quickstart "What just happened" | Docs change | R2 dispute, R3 resolved (hybrid accepted) |
| P2-Onboard-14 | P2 | Add "Next steps" section to quickstart (two tracks: explore + build) | Docs change | R1 unchallenged, stable across all rounds |
| P2-Onboard-15 | P2 | Document `estimate_cost_usd()` in SDK guide | Docs change | R1 bilateral convergence, stable across all rounds |
| P2-Onboard-16 | P2 | Add import namespace note to SDK guide (`engine` vs. `conversus` packages) | Docs change | R2 convergence (decoupled from code change), R3 reaffirmed |
| P3-Onboard-17 | P3 | Add `--phase` parameter documentation note (partially addressed by P1-Onboard-3) | Docs change | R1 unchallenged, stable across all rounds |
| P3-Onboard-18 | P3 | Add `conversus status` to quickstart after "Try with a real provider" | Docs change | R1 unchallenged, R2 converged, R3 reaffirmed |
| P3-Onboard-19 | P3 | Add "What you will see" per-mode output description to modes.md | Docs change | R2 unchallenged, R3 reaffirmed |
| P3-Onboard-20 | P3 | Add minimal 6-line starter config callout to config-reference.md | Docs change | R1 unchallenged, stable across all rounds |

### Track 3: Extensibility (8 items -- deepest impact for developer audience)

| ID | Priority | Description | Type | Source |
|----|----------|-------------|------|--------|
| P1-Ext-1 | P1 | Add end-to-end domain tutorial to building-domains.md (5-stage lifecycle with self-contained preamble) | Docs change | R1 disputed (priority), R2 disputed (gating), R3 resolved |
| P1-Ext-2 | P1 | Add plugin wiring steps to building-plugins.md + `plugins:` key to config-reference.md (single deliverable) | Docs change | R1 disputed (location), R2 converged (pairing), R3 reaffirmed |
| P2-Ext-3 | P2 | Add narrative prose + `members:` list to API reference pages (dual-surface: GitHub + MkDocs) | Docs change | R1 convergence, R2 dual-surface modification, R3 reaffirmed |
| P2-Ext-4 | P2 | Split `determine_verdict` docs into default behavior + customization pattern | Docs change | R1 bilateral convergence, stable across all rounds |
| P2-Ext-5 | P2 | Add error handling guidance (descriptive + prescriptive "recommended patterns") | Docs change | R1 unchallenged, R2 corrected per source, R3 dispute resolved |
| P2-Ext-6 | P2 | Add testing examples for plugins and domains (constructor calls match source types) | Docs change | R1 unchallenged, stable across all rounds |
| P2-Ext-7 | P2 | Add domain-engine integration subsection to architecture.md | Docs change | R1 unchallenged, stable across all rounds |
| P3-Ext-8 | P3 | Document hard block function dispatch differences (`_check_hard_blocks` vs. `evaluate_hard_blocks`) | Docs change | R1 unchallenged, stable across all rounds |

### Documentation Principles (ratified unanimously, all rounds)

Two standing principles for the conversus documentation suite:

1. **Copy-paste test (scoped)**: The first complete code example on each SDK and quickstart page must be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block must be self-contained. YAML configuration examples are exempt.

2. **Failure-mode annotations**: Every SDK function shown in documentation whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case.

### Track Ordering Guidance

Items across tracks have no hard ordering dependency. When resources are serial, prioritize by track order: code fixes first (smallest scope, highest confidence, mergeable in under an hour), then onboarding (broadest audience, highest expected impact per hour), then extensibility (deepest impact for developer audience). When resources are parallel, all three tracks can proceed simultaneously. Items within a track are ordered by priority (P1 before P2 before P3). The domain tutorial and plugin wiring steps include self-contained setup preambles that allow them to ship independently of onboarding fixes.

### Implementation Summary

| Priority | Code Fixes | Onboarding | Extensibility | Total |
|----------|-----------|------------|---------------|-------|
| P1 | 2 | 6 | 2 | 10 |
| P2 | 1 | 10 | 5 | 16 |
| P3 | 0 | 4 | 1 | 5 |
| **Total** | **3** | **20** | **8** | **31** |

Plus 2 documentation principles and 1 open implementer annotation (`cost_estimate` return type verification).

---

## Resolution Attribution

| Dispute | Resolution Type | Key Agent(s) | Mechanism |
|---------|----------------|--------------|-----------|
| SDK sync vs. async Quick Start | Agent convergence (R2) | code-verifier conceded | code-verifier accepted that practical SyntaxError risk outweighs architectural purism |
| Onboarding vs. extensibility priority | Agent convergence (R3) | user-advocate withdrew hard gating | Self-contained preamble design eliminated the dependency |
| Quickstart troubleshooting hints | Agent convergence (R2) | user-advocate narrowed scope | Evolved from full section to brief callout; absorbed into prerequisites convergence |
| Provider precedence -- doc vs. dead code | Agent convergence (R3) | user-advocate accepted P2 | Admonition callout format satisfied visibility concern at lower priority |
| `domains/base.md` member filtering | Synthesizer integration (R1) | code-verifier drove | Folded into API reference narrative prose work item |
| Domain tutorial priority | Agent convergence (R3) | Merged with implementation ordering | Parallel tracks + self-contained preamble |
| Plugin wiring location | Agent convergence (R2) | user-advocate proposed pairing | Single deliverable: building-plugins.md + config-reference.md |
| Provider default warning priority | Agent convergence (R3) | user-advocate accepted P2 | Conditional acceptance: admonition format + prominent placement committed |
| Domain tutorial install-path gating | Agent convergence (R3) | developer-advocate demonstrated independence | Self-contained `git clone` + `uv sync` preamble removes dependency |
| Copy-paste test scope | Agent convergence (R3) | All three agents independently | Three definitional framings converged to identical affected-page set |
| Quickstart output format | Agent convergence (R3) | user-advocate accepted hybrid | Synthesizer's R2 hybrid proposal accepted as "genuine improvement" |
| Error handling prescriptive scope | Agent convergence (R3) | All three agents | "Recommended patterns" label as epistemic boundary accepted by all |
| Implementation plan ordering | Agent convergence (R3) | All three agents | Both scheduling models produce identical artifacts; choice left to implementer |

**Resolution method summary**: 12 of 13 disputes resolved through agent convergence (agents voluntarily adjusted positions based on evidence or design solutions). 1 dispute resolved through synthesizer integration (folding into a broader work item). Zero disputes required synthesizer override.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->
## Remaining Disputes

**Dispute count: 0**

No disputes remain. All 13 disputes raised across 3 rounds were resolved with full agent agreement. No synthesizer overrides were necessary. Three editorial tensions persist at the wording level (track ordering phrasing, P2-Onboard-13 item text specificity, copy-paste test definitional framing) but all three agents explicitly declined to escalate them, confirming they do not affect the implementation plan's content, scope, or ordering.

<!-- CONVERSUS:DISPUTES_END -->

---

## Termination Assessment

**Was 3 rounds appropriate?** Yes. Each round served a distinct function:

- **Round 1** established the factual foundation and initial convergence set. It identified the core documentation issues through three complementary lenses (source accuracy, user experience, developer completeness) and converged on 7 items where source code evidence was unambiguous. The 7 remaining disputes were primarily value-driven (audience prioritization), which Round 1 alone could not resolve because they required the agents to internalize each other's priorities.

- **Round 2** was the most productive round for discovery. It found the three most dangerous defects in the documentation suite (the `pip install conversus` nonexistent package, the `--phase synthesis` broken epilog, and the systematic failure-mode omission pattern) -- all missed by all three agents in Round 1. It resolved the sharpest Round 1 dispute (SDK sync-first) through a genuine concession. It also produced critical factual corrections (error handling guidance, `DomainContext` type, plugin loader behavior). Without Round 2, the implementation plan would have shipped three dangerous defects.

- **Round 3** was essential for dispute resolution but produced no new findings. All 6 remaining disputes were resolved through precise wording, design solutions (self-contained preambles), or recognition that apparent disagreements mapped to identical practical outcomes. The zero-new-recommendations and zero-reversals pattern confirms the deliberation had reached steady state.

**Was convergence efficient?** The dispute trajectory (7 -> 6 -> 0) shows a slow first reduction followed by a sharp final resolution. The Round 2 net reduction of only 1 dispute (despite resolving the SDK sync-first dispute) was caused by new discoveries generating new disputes. This is a healthy pattern: Round 2 expanded the scope to include critical findings that Round 1 missed, which necessarily introduced new disagreements before they could converge. The sharp Round 3 resolution (6 -> 0) confirms that the remaining disputes were scope/framing disagreements rather than substantive conflicts, as the Round 2 synthesizer predicted.

**Would fewer rounds have sufficed?** No. Stopping at Round 1 would have missed the three most dangerous defects. Stopping at Round 2 would have left 6 disputes unresolved, including the implementation ordering dispute that determines how the 31 items are shipped. The three-round configuration was the minimum necessary for this documentation review.

**Would more rounds have been useful?** No. Round 3 produced zero new findings, zero new recommendations, and zero reversals. The three editorial tensions that persist are explicitly acknowledged as not affecting the implementation plan. A Round 4 would have consumed agent resources without changing any outcome.

---

## Systemic Issues Identified

Four systemic issues were identified across the deliberation. These are structural properties of the documentation suite that the implementation plan mitigates but does not fully resolve:

1. **Install-path fragmentation across entry points.** The documentation presented at least three install paths (`pip install conversus`, `git clone` + `uv sync`, `pip install -e .`) with inconsistent invocation prefixes. Addressed by P1-Onboard-1 (reconcile index page), P1-Onboard-6 (prerequisites), P2-Onboard-7 (`uv run` note), and self-contained setup preambles in extensibility tutorials.

2. **SDK documentation systematically hides failure modes.** Three verified instances where return types or exceptions were undocumented. Addressed by P2-Onboard-10 (instance fixes) and Documentation Principle 2 (recurrence prevention via standing annotation requirement).

3. **Audience segmentation without explicit scoping.** The documentation serves three audiences (new users, SDK integrators, plugin/domain developers) without page-level audience markers. No agent in any round proposed a concrete audience-labeling mechanism. This remains an observed structural property, mitigated but not resolved by the three-track implementation structure.

4. **Documentation-only vs. code fixes: approval threshold ambiguity.** Spec 031 is a docs-and-compliance spec, but three items are code changes. The process has no stated policy for whether code changes discovered through documentation review ship in the same spec or require separate tickets. The code fixes are included in Track 1 with [Code change] tags.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total rounds | 3 |
| Total agents | 3 |
| Deliberation mode | cooperative |
| Total convergence points | 21 (7 + 8 + 6) |
| Disputes raised across all rounds | 13 (7 in R1, 6 in R2, 0 in R3) |
| Disputes resolved | 13 (all) |
| Disputes remaining | 0 |
| Resolution by agent convergence | 12 |
| Resolution by synthesizer integration | 1 |
| Resolution by synthesizer override | 0 |
| Implementation items ratified | 31 (28 implementation + 2 documentation principles + 1 ordering guidance) |
| Items by priority | P1: 10, P2: 16, P3: 5 |
| Items by track | Code Fixes: 3, Onboarding: 20, Extensibility: 8 |
| Concessions made (cumulative) | 16 (stable, no reversals) |
| New findings in Round 3 | 0 |
| Open implementer annotations | 1 (`cost_estimate` return type verification) |

**Pipeline status: COMPLETE. Full three-way convergence achieved across all 3 rounds. Ready for implementation.**
