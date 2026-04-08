# User-Advocate -- Round 3 (FINAL) Review

**Reviewer role:** user-advocate (new user evaluating from a first-time user's perspective)
**Phase:** Round 3 -- dispute resolution and convergence
**Focus:** Resolving the 6 remaining disputes from the Round 2 synthesis. No new findings.

---

## Executive Summary

The Round 2 synthesis produced a well-structured implementation plan with 3 tracks, 28 items, and recommended resolutions for all 6 remaining disputes. This final review accepts the synthesizer's resolutions on 5 of 6 disputes -- either fully or with minor clarifications. On the 6th (implementation plan ordering), I accept the synthesizer's track-based structure with one refinement to the track ordering guidance.

The documentation suite is ready for implementation. The 15 convergence points from Rounds 1-2 represent a strong foundation, and the dispute resolutions below close the remaining gaps without introducing new scope.

---

## Alignment with Synthesizer's Dispute Resolutions

### Dispute 1: Provider default warning priority (P1 vs. P2)

**Synthesizer recommendation:** P2 with admonition/warning callout format and prominent placement. File a follow-up code issue for CLI fallback to `config.provider`.

**My position:** I accept. My Round 2 disputes explicitly stated: "I will accept P2 if the synthesis commits to the warning callout format (not inline prose) and places it prominently in config-reference.md." The synthesizer commits to both. The admonition callout in P2-Onboard-9 uses strong wording ("Warning: When `provider` is omitted...") that surfaces the silent-failure risk I identified. The follow-up code issue for CLI fallback behavior addresses the root cause on a separate timeline. This is a reasonable resolution.

**Status:** Resolved. No further dispute.

### Dispute 2: Domain tutorial gating on install-path resolution

**Synthesizer recommendation:** No hard gating dependency. The domain tutorial includes its own self-contained setup preamble. The implementation plan states items across tracks have no ordering dependency.

**My position:** I accept. The self-contained setup preamble in P1-Ext-1 ("git clone + uv sync + cd conversus") makes the domain tutorial independently shippable regardless of the index page state. This was always my underlying concern: that a developer following the docs would hit a broken install command before reaching the tutorial. The preamble eliminates that dependency without creating a false gate. Developer-advocate was correct that a developer building domain plugins has typically already solved installation; the preamble ensures this even when they have not.

**Status:** Resolved. No further dispute.

### Dispute 3: Copy-paste test scope -- standing principle vs. entry-point-only

**Synthesizer recommendation:** State the principle with explicit scope: "The first complete code example on each SDK and quickstart page should be self-contained and runnable as `python script.py` without modification. Tutorial pages that build incrementally are exempt, but their opening setup block should be self-contained. YAML examples are exempt."

**My position:** I accept. The scoped principle satisfies my recurrence-prevention concern while respecting code-verifier's tutorial pedagogy point and developer-advocate's exemption for non-executable content. The addition of "their opening setup block should be self-contained" for tutorial pages is a good compromise -- incremental tutorials still need a working starting point. The YAML exemption is practical (YAML configs are not "runnable" in the same sense). The synthesizer also incorporated my failure-mode annotation principle in the Documentation Principle section: "Every SDK function shown in documentation whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case." Both principles together close the gap.

**Status:** Resolved. No further dispute.

### Dispute 4: Quickstart example output -- literal block vs. prose description

**Synthesizer recommendation:** Hybrid approach. Prose description of expected output ("You will see five phase headers -- Review, Cross-review, Revision, Disputes, Synthesis -- followed by a headline verdict and a summary") plus a note about `--format json` for programmatic verification. No literal output block.

**My position:** I accept with a minor clarification. The hybrid is a genuine middle ground that addresses both risks (stale output blocks degrade trust; missing output leaves users unable to verify success). The prose description names the five phases explicitly, which gives the user enough to verify that their run succeeded without creating a maintenance-fragile literal block. The `--format json` note is a good addition that I had not considered -- it provides a durable, machine-verifiable check for users who want certainty. Developer-advocate's durability concern was legitimate, and this resolution handles it.

The one clarification: P2-Onboard-13 as written says "No literal output block (maintenance fragility)." I would refine this to: "No literal terminal output block. The prose description should name the five phase headers and the output structure (headline + summary) so the user knows what to look for." This is what the synthesizer already describes in the recommended resolution text -- I am asking that the actionable item text match the recommendation.

**Status:** Resolved. No further dispute.

### Dispute 5: Error handling documentation -- prescriptive patterns vs. descriptive-only

**Synthesizer recommendation:** Include both descriptive and prescriptive content. Descriptive: framework's catch-and-skip behavior. Prescriptive: three bullet points labeled as "recommended patterns" -- raise freely, use `.get()` with defaults, check warning-level logs.

**My position:** I accept. The resolution correctly identifies that this dispute was narrower than it appeared. All agents agreed on the descriptive content (the framework catches and logs). The prescriptive patterns are standard defensive programming that cannot become factually incorrect even if the framework internals change. Labeling them "recommended patterns" rather than "framework guarantees" is the right framing -- it gives plugin/domain authors a concrete starting point without making claims about internal behavior that code-verifier would need to re-verify. Developer-advocate gets actionable guidance; code-verifier gets source-accurate descriptions.

**Status:** Resolved. No further dispute.

### Dispute 6: Implementation plan ordering -- explicit batches vs. priority-tagged list

**Synthesizer recommendation:** Three tracks (Code fixes, Onboarding, Extensibility) with items ordered within each track, no inter-track hard dependencies. Track ordering guidance: "When resources are serial, prioritize by track order: code fixes first, then onboarding, then extensibility."

**My position:** I accept the structure. The track ordering guidance is exactly what I asked for -- explicit sequencing when resources are serial, with parallel execution possible when resources allow it. The synthesizer's phrasing ("prioritize by track order") combined with the self-contained preambles in extensibility items eliminates the false-dependency concern developer-advocate raised while preserving the sequencing signal I need.

One refinement to the guidance text: the synthesizer writes "Items across tracks have no ordering dependency." I would strengthen this to: "Items across tracks have no hard ordering dependency. When resources are serial, the track order (code fixes, onboarding, extensibility) reflects implementation priority. The domain tutorial and plugin wiring steps include self-contained setup preambles that allow them to ship independently of onboarding fixes." This makes the "no hard dependency" statement specific about why -- the preambles -- rather than leaving it as a planning assertion.

**Status:** Resolved. No further dispute.

---

## Actionable Recommendations (Refined from R2)

All recommendations below reference the synthesizer's item IDs from the Round 2 Actionable Spec Changes. I am not introducing new items.

### Accepted without modification

The following items from the Round 2 synthesis are accepted exactly as written. They represent the full set of convergence points from Rounds 1-2 plus the synthesizer's dispute resolutions:

**Track 1 (Code Fixes):** P1-Code-1, P1-Code-2, P2-Code-3 -- all accepted.

**Track 2 (Onboarding):** P1-Onboard-1, P1-Onboard-2, P1-Onboard-3, P1-Onboard-4, P1-Onboard-5, P1-Onboard-6, P2-Onboard-7, P2-Onboard-8, P2-Onboard-9, P2-Onboard-10, P2-Onboard-11, P2-Onboard-12, P2-Onboard-14, P2-Onboard-15, P2-Onboard-16, P3-Onboard-17, P3-Onboard-18, P3-Onboard-19, P3-Onboard-20 -- all accepted.

**Track 3 (Extensibility):** P1-Ext-1, P1-Ext-2, P2-Ext-3, P2-Ext-4, P2-Ext-5, P2-Ext-6, P2-Ext-7, P3-Ext-8 -- all accepted.

**Documentation Principle:** Accepted as written. Both the copy-paste test and the failure-mode annotation principle.

**Track Ordering Guidance:** Accepted with the refinement noted in Dispute 6 above.

### Accepted with minor clarification

**P2-Onboard-13** (abbreviated output description): Accepted with the clarification from Dispute 4 above. The actionable item text should explicitly state that the prose description names the five phase headers and the output structure, matching the synthesizer's recommended resolution text.

---

## Concessions Made Across All Rounds (Cumulative)

1. **Provider default priority: P1 to P2.** Conceded in Round 2 disputes, conditional on callout format. Condition met by synthesizer. Not reversed.

2. **`uv run` note priority: P1 to P2.** Conceded in Round 2 disputes. Not reversed.

3. **`uv run` options (b) and (c) withdrawn.** Conceded in Round 2 revision after developer-advocate showed they create new contradictions. Not reversed.

4. **Literal output block in quickstart withdrawn.** Conceded in this round. The hybrid prose description is a genuine improvement over my original proposal.

5. **Hard inter-track gating withdrawn.** Conceded in this round. Self-contained preambles eliminate the dependency I was concerned about.

6. **Copy-paste test scope narrowed.** Accepted the synthesizer's scoped principle with tutorial and YAML exemptions. Not reversed -- this is a refinement, not a concession.

---

## Final Position Statement

### Non-Negotiables (carried from Round 2, all now addressed)

1. **Install path consistency across index page and quickstart.** Addressed by P1-Onboard-1 (unanimous convergence, Round 2).

2. **Failure-mode annotations in SDK documentation with a stated prevention principle.** Addressed by P2-Onboard-10 (instance fixes) and the Documentation Principle section (recurrence prevention).

3. **Ordered implementation plan.** Addressed by the three-track structure with serial-resource ordering guidance.

All three non-negotiables are satisfied by the Round 2 synthesis. I have no remaining non-negotiables.

### Assessment of Documentation Quality

Reading the 11 target files as a first-time user in Round 3, the documentation is strong in several areas:

- **quickstart.md** provides a fast, working path from clone to first deliberation. With the P1 onboarding fixes (slash command heading, prerequisites callout, `uv run` note), it will be excellent.
- **modes.md** is one of the best pages in the suite -- clear, concrete, with realistic YAML examples for all 8 modes.
- **cli.md** is thorough and well-structured. The P1 fixes (epilog, `--phase review` docs, `decide` 4-mode note) address the only traps.
- **config-reference.md** is comprehensive. The P2 additions (provider warning, plugins key, minimal starter config) round it out.
- **sdk.md** is well-organized for the async-experienced developer. The sync-first Quick Start and failure-mode annotations will make it accessible to the broader audience.
- **building-plugins.md** and **building-domains.md** provide solid reference material. The end-to-end tutorial and wiring steps will bridge the gap between "understand the API" and "build something."
- **architecture.md** is clear and the coupling rules diagram is genuinely useful.
- The API reference pages are thin (MkDocs directives only) but the planned narrative prose and class catalogs will address this.

The documentation suite, after the planned changes, will provide a coherent path from "What is this?" through "Run my first deliberation" to "Build a custom plugin/domain." The three-track implementation plan ensures the most impactful fixes ship first.

---

## Referenced Documentation

| File | Key Findings |
|------|-------------|
| `docs/user-guide/quickstart.md` | Strong base. Needs: slash command heading (P1-Onboard-5), prerequisites (P1-Onboard-6), `conversus status` (P3-Onboard-18), prose output description (P2-Onboard-13). |
| `docs/user-guide/cli.md` | Thorough. Needs: epilog fix (P1-Code-2), `--phase review` docs (P1-Onboard-3), `decide` 4-mode note (P1-Onboard-4), `uv run` prefix note (P2-Onboard-7), provider model table (P2-Onboard-11). |
| `docs/user-guide/modes.md` | Excellent. One P3 addition: per-mode output descriptions (P3-Onboard-19). |
| `docs/user-guide/sdk.md` | Good structure. Needs: sync-first Quick Start (P2-Onboard-8), failure-mode annotations (P2-Onboard-10), `estimate_cost_usd()` (P2-Onboard-15), import namespace note (P2-Onboard-16). |
| `docs/user-guide/config-reference.md` | Comprehensive. Needs: provider warning callout (P2-Onboard-9), `plugins:` key (P1-Ext-2), minimal starter config (P3-Onboard-20). |
| `docs/developer-guide/architecture.md` | Clear. Needs: domain-engine integration subsection (P2-Ext-7). |
| `docs/developer-guide/building-plugins.md` | Solid reference. Needs: wiring steps update (P1-Ext-2), error handling guidance (P2-Ext-5), testing examples (P2-Ext-6). |
| `docs/developer-guide/building-domains.md` | Good API reference. Needs: end-to-end tutorial (P1-Ext-1), error handling guidance (P2-Ext-5), testing examples (P2-Ext-6), hard block dispatch note (P3-Ext-8). |
| `docs/api/schemas/construction.md` | MkDocs directive only. Needs: narrative prose + class catalog (P2-Ext-3). |
| `docs/api/plugins/base.md` | MkDocs directive only. Needs: narrative prose + class catalog (P2-Ext-3). |
| `docs/api/domains/base.md` | MkDocs directive only. Needs: narrative prose + members list + class catalog (P2-Ext-3). |
