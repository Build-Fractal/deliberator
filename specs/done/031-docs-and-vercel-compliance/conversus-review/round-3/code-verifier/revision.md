# Code-Verifier -- Revision (Round 3, FINAL)

## Recommendation Dispositions

### Track 1: Code Fixes

| ID | Recommendation | Disposition | Notes |
|---|---|---|---|
| P1-Code-1 | Fix scaffolds endpoint glob (`api.py` L208) | **Confirmed -- no change.** | Single-line fix. Source-verified in Rounds 1-2. Zero cross-review challenges. |
| P1-Code-2 | Fix epilog `--phase synthesis` to `--phase review` (`cli/__init__.py` L95) | **Confirmed -- no change.** | Ships alongside P1-Onboard-3. Source-verified. Zero cross-review challenges. |
| P2-Code-3 | Export `classify` from `engine/__init__.py` | **Confirmed -- no change.** | Track separately from SDK namespace note (P2-Onboard-16). Zero cross-review challenges. |

### Track 2: Onboarding

| ID | Recommendation | Disposition | Notes |
|---|---|---|---|
| P1-Onboard-1 | Reconcile install path on index page | **Confirmed -- no change.** | Highest-severity first-contact defect. Both cross-reviewers agree. |
| P1-Onboard-2 | Fix index page "4 modes" across 4 locations | **Confirmed -- no change.** | Includes card title change to "Deliberation Modes." Both cross-reviewers agree. |
| P1-Onboard-3 | Document `--phase review` behavior in cli.md | **Confirmed -- no change.** | Ships with P1-Code-2. Both cross-reviewers agree. |
| P1-Onboard-4 | Add `decide` 4-mode clarifying note to cli.md | **Confirmed -- no change.** | Round 1 convergence, unchanged through all rounds. |
| P1-Onboard-5 | Heading + explanation before slash commands in quickstart | **Confirmed -- no change.** | "Try the guided workflow (in your AI editor)" heading. |
| P1-Onboard-6 | Prerequisites callout to quickstart | **Confirmed -- no change.** | Python 3.12+ and uv. |
| P2-Onboard-7 | `uv run` prefix note at top of cli.md | **Confirmed -- no change.** | Option A only (note at top of page, not per-command). |
| P2-Onboard-8 | SDK sync-first Quick Start with async-context note | **Confirmed -- no change.** | Resolves Round 1 dispute. Both cross-reviewers agree. |
| P2-Onboard-9 | Three-way provider default warning in config-reference.md | **Confirmed P2 -- no change.** | Admonition callout format. Dispute 1 fully resolved: all three reviewers accept P2 with callout. |
| P2-Onboard-10 | SDK happy-path-only failure-mode annotations | **Confirmed -- editorial note added.** | Three instances: `cost_estimate`, `construct_objective`, `classify`. Both cross-reviewers note that neither they nor I independently verified the `cost_estimate` return type (`dict | None` vs. always `dict`). The annotation is safe regardless -- if it always returns a dict, the annotation is harmless; if it can return None, the annotation is essential. Implementer should verify the actual return type before writing the annotation text. |
| P2-Onboard-11 | Provider default model table in cli.md | **Confirmed -- no change.** | Unchallenged across all three rounds and both cross-reviews. |
| P2-Onboard-12 | State MkDocs as primary reading surface | **Confirmed -- no change.** | Include `uv run mkdocs serve` build instructions. |
| P2-Onboard-13 | Abbreviated output description in quickstart | **Confirmed -- editorial refinement accepted.** | Prose description + `--format json` verification note. No literal output block. User-advocate's cross-review asks that the item text explicitly state the prose names the five phase headers and the output structure (headline + summary). I accept this refinement as a quality-of-life improvement for the implementer. The phase names (Review, Cross-review, Revision, Disputes, Synthesis) are architecturally stable -- they derive from `engine/phases.py` and the template directory structure. |
| P2-Onboard-14 | "Next steps" section in quickstart | **Confirmed -- no change.** | Two tracks: explore and build. |
| P2-Onboard-15 | `estimate_cost_usd()` in SDK guide | **Confirmed -- no change.** | Bilateral convergence from Round 1. Unchallenged in cross-reviews. |
| P2-Onboard-16 | Import namespace note in SDK guide | **Confirmed -- no change.** | Decoupled from classify re-export code change (P2-Code-3). |
| P3-Onboard-17 | `--phase` parameter documentation note | **Confirmed -- no change.** | Partially addressed by P1-Onboard-3. |
| P3-Onboard-18 | `conversus status` in quickstart | **Confirmed -- no change.** | After "Try with a real provider." |
| P3-Onboard-19 | "What you will see" per-mode output in modes.md | **Confirmed -- no change.** | Unchallenged across all rounds. |
| P3-Onboard-20 | Minimal starter config callout in config-reference.md | **Confirmed -- no change.** | 6-line minimal config. |

### Track 3: Extensibility

| ID | Recommendation | Disposition | Notes |
|---|---|---|---|
| P1-Ext-1 | End-to-end domain tutorial in building-domains.md | **Confirmed -- no change.** | Self-contained setup preamble (`git clone` + `uv sync` + `cd conversus`). No install-path gating (Dispute 2 resolved). All types verified against source (`list[Path]`, `str | Scaffold`). Both cross-reviewers agree. |
| P1-Ext-2 | Plugin wiring steps + `plugins:` config key (single deliverable) | **Confirmed -- no change.** | Loader finds first Plugin subclass by alphabetical `dir()` order. Define one per module. Both cross-reviewers agree. |
| P2-Ext-3 | Narrative prose + `members:` list on API reference pages | **Confirmed -- no change.** | Dual-surface: plain-text class catalog for GitHub, `members:` list for MkDocs. `domains/base.md` is the only page missing a `members:` list entirely. |
| P2-Ext-4 | `determine_verdict` documentation split | **Confirmed -- no change.** | Default behavior + customization pattern. |
| P2-Ext-5 | Error handling guidance | **Confirmed -- no change.** | Dispute 5 resolved: descriptive + prescriptive, clearly labeled as "recommended patterns." Three prescriptive bullets source-verified at `domains/base.py` L697-708 and `plugins/base.py` L519-525. Both cross-reviewers agree. |
| P2-Ext-6 | Testing examples for plugins/domains | **Confirmed -- no change.** | Constructor calls must match source types. |
| P2-Ext-7 | Domain-engine integration in architecture.md | **Confirmed -- no change.** | Unchallenged across all rounds. |
| P3-Ext-8 | Hard block function dispatch differences | **Confirmed -- no change.** | `_check_hard_blocks` (module-level) supports three-part comparison only; `DomainPlugin.evaluate_hard_blocks()` via `_evaluate_single_hard_block` supports all three forms (bare truthy, comparison, boolean equality). Source-verified at `base.py` L306-352 vs. L378-461. Unchallenged. |

### Documentation Principle

| Recommendation | Disposition | Notes |
|---|---|---|
| Copy-paste test for SDK/quickstart first examples; incremental-tutorial and YAML exemptions; failure-mode annotation requirement | **Confirmed -- no change.** | All three reviewers accept the synthesizer's formulation verbatim. My clarification that "each SDK and quickstart page" excludes extensibility guides is consistent with the synthesizer's tutorial exemption and with both cross-reviewers' interpretations -- we arrive at the same practical outcome through slightly different framing. No wording change needed. |

---

## New Recommendations

None. This final round introduces no new findings. All material issues were surfaced in Rounds 1 and 2, captured accurately in the Round 2 synthesis, and confirmed through cross-review. The 28-item implementation plan across three tracks is complete.

---

## Position Summary

### Disputes: All Resolved

All 6 disputes from Round 2 are closed with full three-reviewer convergence:

1. **Provider default warning priority** -- P2 with admonition callout. Failure mode is safe (mock output, no money spent, no incorrect decisions). Follow-up CLI code issue filed outside spec 031 scope.
2. **Domain tutorial gating** -- No hard dependency on index page fix. Self-contained setup preamble makes the tutorial independently shippable.
3. **Copy-paste test scope** -- SDK and quickstart first examples must be self-contained and runnable. Incremental tutorials exempt (opening setup block must be self-contained). YAML exempt. Extensibility guides covered by the tutorial exemption.
4. **Quickstart output format** -- Prose description naming the five phase headers (Review, Cross-review, Revision, Disputes, Synthesis) plus headline verdict and summary. `--format json` verification note. No literal output block.
5. **Error handling documentation** -- Descriptive section on framework catch-and-skip behavior plus prescriptive section with three "recommended patterns" bullets. Clearly labeled distinction.
6. **Implementation plan ordering** -- Three parallel tracks (Code Fixes, Onboarding, Extensibility) with intra-track priority ordering. No inter-track hard dependencies. Serial preference: code fixes first, then onboarding, then extensibility.

### Cross-Review Findings: Clean

Both cross-reviews (user-advocate and developer-advocate) found zero dangerous contradictions in my review. The tensions identified are all editorial:

- **Track ordering wording** (Dispute 6): User-advocate prefers embedding the rationale for track independence (self-contained preambles) in the guidance text. Developer-advocate proposes priority-interleaved scheduling as an alternative to strict track-sequential ordering. Both are compatible with my position. Neither affects the implementation plan's structure or content.
- **P2-Onboard-13 item text** (Dispute 4): User-advocate asks that the item text explicitly reference the five phase headers. I accept this as a quality-of-life refinement, reflected in my disposition table above.
- **Copy-paste test page scope** (Dispute 3): User-advocate frames the exemption by the synthesizer's literal text; developer-advocate frames it by content structure (standalone vs. incremental); I frame it by page audience (end-users vs. extension authors). All three framings produce the same set of affected pages. No wording change needed.
- **`cost_estimate` return type** (P2-Onboard-10): Neither cross-reviewer nor I independently verified whether `Deliberation.cost_estimate` returns `dict | None` or always `dict`. The annotation is the correct fix regardless. I have added a note in my disposition that the implementer should verify the actual return type.

### Concessions: Stable

No prior concessions from Rounds 1-2 are reversed. The corrections I accepted across earlier rounds remain in force:

1. SDK Quick Start uses sync-first pattern (not bare `await`).
2. Error handling guidance says "raise freely" (not "return empty dicts").
3. `DomainContext.changed_files` is `list[Path]` (not `list[str]`).
4. Plugin loader uses alphabetical `dir()` order -- documentation should say "define exactly one Plugin subclass per module."
5. `score()` interface is typed and documented; the gap was demonstration coverage, not specification ambiguity.
6. Import namespace documentation (P2-Onboard-16) ships independently from the classify re-export code change (P2-Code-3).

### Implementation Readiness

The 3-track, 28-item implementation plan is fully ratified by all three reviewers. No items are disputed, deferred, or withdrawn. The three code fixes (Track 1) are single-line changes mergeable in under an hour. The 20 onboarding items (Track 2) and 8 extensibility items (Track 3) are well-scoped with clear acceptance criteria. The documentation principle provides recurrence prevention for the two systemic issues identified (non-runnable code examples and undocumented failure modes).

The pipeline is ready for implementation.
