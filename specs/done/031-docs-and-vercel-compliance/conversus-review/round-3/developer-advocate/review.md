# Developer Advocate -- Round 3 (Final Round)

## Executive Summary

This final round resolves the 6 remaining disputes from the Round 2 synthesis. As a developer trying to build plugins and domains from these docs, my priority has been ensuring the extensibility documentation is complete, accurate, and independently shippable. The Round 2 synthesis produced a well-structured actionable plan with 3 tracks and 28 items. I accept the synthesizer's recommended resolutions on all 6 disputes, with minor refinements on two of them. No new findings are introduced. All prior concessions stand.

**Dispute resolution summary:**

| Dispute | My R2 Position | Synthesizer Recommendation | My R3 Position |
|---------|---------------|---------------------------|----------------|
| 1. Provider default priority | No strong position | P2 with warning callout | Accept P2 |
| 2. Domain tutorial gating | No hard gating | Self-contained preamble, parallel tracks | Accept fully |
| 3. Copy-paste test scope | Entry-point code only | Scoped principle with tutorial exemption | Accept fully |
| 4. Quickstart example output | Prose description over literal block | Hybrid prose + `--format json` tip | Accept fully |
| 5. Error handling prescriptive vs. descriptive | Prescriptive patterns required | Both descriptive + 3 prescriptive bullets | Accept fully |
| 6. Implementation plan ordering | Parallel tracks, no gating | Track-level batching, serial preference note | Accept with one refinement |

All 6 disputes can converge in this round.

---

## Alignment with Synthesizer's Dispute Resolutions

### Dispute 1: Provider default warning priority (P1 vs. P2)

**I accept P2.** I did not take a strong priority position in Round 2, and the synthesizer's reasoning is sound. The failure mode is safe -- a user who gets mock output when expecting Anthropic output loses time but not money. The agreed-upon admonition callout format in config-reference.md makes this item trivially implementable regardless of its priority label. User-advocate's conditional acceptance (P2 if the callout format and placement are committed) is satisfied by the synthesis.

The follow-up code issue for CLI fallback to `config.provider` is the right long-term fix. I support filing it.

### Dispute 2: Domain tutorial gating on install-path resolution

**I accept the synthesizer's resolution fully.** This was my strongest dispute in Round 2, and the synthesizer landed exactly where I argued: no hard gating dependency, but the domain tutorial must include its own self-contained setup preamble. The key sentence from the synthesis -- "The domain tutorial's setup preamble provides a correct install path regardless of the index page state" -- captures the principle perfectly.

As a developer, I can confirm: if I clone a repo and run `uv sync`, I do not care what the index page says. The tutorial's preamble (`git clone` + `uv sync` + `cd conversus`) makes the domain lifecycle walkthrough independently shippable. This is the parallel-tracks agreement working as designed.

### Dispute 3: Copy-paste test scope

**I accept the synthesizer's scoped principle.** The formulation -- "The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block should be self-contained. YAML examples are exempt." -- threads the needle between user-advocate's recurrence prevention and my concern about tutorial pedagogy.

The building-domains tutorial is a multi-stage lifecycle walkthrough. Under this principle, the opening setup block (clone + install + import) must be self-contained, but stages 2-5 can build incrementally without repeating boilerplate. This is exactly the right balance for developer-facing documentation.

### Dispute 4: Quickstart example output

**I accept the hybrid approach.** The prose description ("You will see five phase headers -- Review, Cross-review, Revision, Disputes, Synthesis -- followed by a headline verdict and a summary") is durable because phase names are stable API contracts. The `--format json` tip gives users a programmatic verification path without creating a fragile literal output block on the highest-traffic page.

This resolves my core concern: no literal output block that becomes stale. It also addresses user-advocate's core concern: the user knows what to look for and has a verification mechanism.

### Dispute 5: Error handling prescriptive vs. descriptive

**I accept the synthesizer's resolution fully.** The three prescriptive bullet points are exactly what I argued for in Round 2:

1. "Raise freely -- exceptions are caught and logged."
2. "Use `state.plugin_results.get('key', default)` for consumed data in case the producer failed."
3. "Check warning-level logs for plugin/extractor skip messages during development."

Labeling these as "recommended patterns" rather than framework guarantees satisfies code-verifier's insistence on source accuracy while giving developers the actionable guidance they need. This is the right level of prescription for an introductory building-plugins page.

### Dispute 6: Implementation plan ordering

**I accept the track-level batching with one refinement.** The synthesizer's guidance -- "When resources are serial, prioritize by track order: code fixes first, then onboarding, then extensibility" -- is pragmatic and I support it. My refinement:

The serialization preference should be within-track, not across-track. The code fixes track has 3 items. Onboarding has 20 items. Extensibility has 8 items. If a single implementer works serially, they should complete all 3 code fixes, then work on P1 onboarding items, then P1 extensibility items, then P2 onboarding, then P2 extensibility, and so on. The priority labels (P1/P2/P3) already encode this. Saying "finish all 20 onboarding items before starting any extensibility work" would be an overcorrection.

In practice, I believe the synthesis already implies this with "items within a track are ordered by priority," but I want to make it explicit: a serial implementer should interleave P1 items across tracks before moving to P2 items. The track ordering (code > onboarding > extensibility) is a tiebreaker within the same priority tier, not a strict sequencing gate across tiers.

---

## Actionable Recommendations (Refined from R2)

All recommendations below are carried from Round 2 and refined per the synthesis. No new recommendations are introduced. Items are tagged with their synthesis identifiers for traceability.

### P1 -- Critical (must ship)

**DA-R1: End-to-end domain tutorial** (maps to P1-Ext-1)
Add "Running your domain" section to building-domains.md demonstrating the 5-stage lifecycle. Include self-contained setup preamble per Dispute 2 resolution. All code examples verified against source type annotations (`list[Path]` not `list[str]`, `scaffold: str | Scaffold`). Cross-reference API router mounting as step 6.

**DA-R2: Plugin wiring steps + config-reference pairing** (maps to P1-Ext-2)
Single deliverable. Update "Dynamic loading" section: dotted import path, `sys.path` requirement, loader finds first Plugin subclass by alphabetical attribute name, define exactly one per module, failure is non-fatal. Add `plugins:` section to config-reference.md. Ships together per unanimous convergence.

### P2 -- Important (should ship with the spec)

**DA-R4: Domain-engine integration in architecture.md** (maps to P2-Ext-7)
Add subsection after pipeline data flow diagram explaining that domains are invoked outside the pipeline. Note `equilibrium_score` as the bridge between plugin and domain systems.

**DA-R5: Error handling guidance** (maps to P2-Ext-5)
Descriptive section: framework catch-and-skip behavior from `domains/base.py` and `plugins/base.py`. Prescriptive section: the three recommended patterns, clearly labeled as recommended patterns per Dispute 5 resolution.

**DA-R6: Testing examples** (maps to P2-Ext-6)
Minimal `DeliberationState` construction for plugin testing. `DomainContext` construction for domain testing. All constructor calls match source type annotations.

**DA-R7: Import namespace explanation in SDK guide** (maps to P2-Onboard-16)
Minimal note: "The SDK spans two packages: `engine` for the deliberation runtime and `conversus` for schemas and plugins. Both are installed together." Decoupled from `classify` re-export code change per Round 2 concession.

**DA-R8: Sync-first SDK Quick Start** (maps to P2-Onboard-8)
Lead with `asyncio.run()` wrapper. Include `# Save as script.py and run: python script.py` comment. Async-context note immediately below. Converged unanimously.

### P3 -- Nice to have

**DA-R9: `conversus status` in quickstart** (maps to P3-Onboard-18)
After "Try with a real provider" section. Converged unanimously.

**DA-R10: Minimal starter config callout** (maps to P3-Onboard-20)
6-line minimal config at top of config-reference.md with "This is all you need" framing.

---

## Concessions Maintained (No Reversals)

All concessions from Round 2 stand without modification:

1. **Withdrew "return empty dicts" error handling guidance.** The framework catches and logs. "Raise freely" is the correct advice.
2. **Corrected `DomainContext.changed_files` type** from `list[str]` to `list[Path]` per code-verifier source verification.
3. **Accepted `score()` interface is typed and docstringed**, not ambiguous. The gap is demonstration coverage.
4. **Decoupled import namespace note from `classify` re-export** code change. Documentation ships independently.
5. **Accepted plugin loader uses alphabetical `dir()` order.** Documentation will say "define exactly one Plugin subclass per module."

---

## Referenced Documentation

| File | Relevance |
|------|-----------|
| `docs/user-guide/quickstart.md` | Install path, slash command heading, output description, `conversus status` |
| `docs/user-guide/cli.md` | `--phase review` docs, `uv run` note, provider defaults, `decide` mode note |
| `docs/user-guide/sdk.md` | Sync-first Quick Start, failure-mode annotations, import namespace note |
| `docs/user-guide/config-reference.md` | Provider warning callout, `plugins:` key, minimal starter config |
| `docs/user-guide/modes.md` | Per-mode output descriptions (P3) |
| `docs/developer-guide/architecture.md` | Domain-engine integration subsection |
| `docs/developer-guide/building-plugins.md` | Wiring steps, error handling, testing examples |
| `docs/developer-guide/building-domains.md` | End-to-end tutorial, setup preamble, lifecycle walkthrough |
| `docs/api/schemas/construction.md` | Narrative prose + class catalog above `:::` directive |
| `docs/api/plugins/base.md` | Narrative prose + class catalog above `:::` directive |
| `docs/api/domains/base.md` | Narrative prose + `members:` list + class catalog |

---

## Final Position

All 6 disputes are resolved from my perspective. The synthesizer's recommendations are well-reasoned and align with my core priorities: independently shippable extensibility content, prescriptive developer guidance, and durable documentation patterns. The 3-track implementation plan with 28 items provides a clear path forward.

My one refinement (Dispute 6, serial interleaving by priority tier rather than strict track ordering) is a minor implementation detail, not a substantive disagreement. If the other agents prefer strict track ordering for simplicity, I will not dispute it.

This documentation suite, once the P1 items ship, will take a developer from zero to a working custom domain plugin without leaving the docs. That is the bar I set at the start of this review, and the converged plan meets it.
