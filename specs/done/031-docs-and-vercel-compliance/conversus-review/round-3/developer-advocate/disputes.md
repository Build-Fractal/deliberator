# Developer Advocate -- Round 3 Disputes (FINAL)

## Remaining Disputes

None. All disputes raised in Rounds 1 and 2 have been resolved through cross-review and revision. No new disputes emerged in Round 3. The three tensions identified across cross-reviews are editorial preferences that do not affect the implementation plan's content, scope, or ordering.

For the record, the three editorial tensions that remain are acknowledged but not escalated:

1. **Track ordering wording (Dispute 6):** I proposed priority-tier interleaving (all P1 items across tracks before P2); user-advocate and code-verifier prefer track-sequential ordering. Both produce identical documentation artifacts. The synthesizer may resolve this either way without affecting outcomes.

2. **Copy-paste test scope framing (Dispute 3):** Code-verifier frames the extensibility exemption by page audience, user-advocate derives it from the principle's literal text, and I frame it by content structure (standalone vs. incremental). All three framings exclude the same pages. No rewording needed.

3. **P2-Onboard-13 item text specificity (Dispute 4):** User-advocate asked that the actionable item text explicitly name the five phase headers and the output structure. Code-verifier and I both accepted this as a quality-of-life improvement. This is already reflected in all three revisions.

## Convergence

All 28 implementation items across three tracks are ratified by all three reviewers. All 6 formal disputes from Round 2 are closed with full three-way agreement. Below is the final convergence record.

### Dispute 1: Provider default warning priority -- RESOLVED
- **Resolution:** P2 with admonition/warning callout format in config-reference.md. Follow-up code issue for CLI fallback to `config.provider` filed outside spec 031 scope.
- **Agreeing agents:** code-verifier, user-advocate, developer-advocate.
- **Path to convergence:** The failure mode is safe (mock output, no money spent, no incorrect decisions). P2 with prominent callout gives adequate visibility without inflating priority.

### Dispute 2: Domain tutorial gating -- RESOLVED
- **Resolution:** No inter-track dependency. The domain tutorial includes a self-contained setup preamble (`git clone` + `uv sync` + `cd conversus`) and is independently shippable regardless of whether the index page install-path fix has landed.
- **Agreeing agents:** code-verifier, user-advocate, developer-advocate.
- **Path to convergence:** This was my strongest dispute in Round 2. The resolution landed exactly where I argued: parallel tracks with no gating. The self-contained preamble eliminates the coupling that concerned code-verifier and user-advocate.

### Dispute 3: Copy-paste test scope -- RESOLVED
- **Resolution:** First complete code example on each SDK and quickstart page must be self-contained and runnable as `python script.py`. Tutorial pages that build incrementally are exempt, but their opening setup block must be self-contained. YAML examples are exempt.
- **Agreeing agents:** code-verifier, user-advocate, developer-advocate.
- **Path to convergence:** All three reviewers arrive at the same practical set of affected pages from different definitional angles. The synthesizer's formulation is accepted verbatim.

### Dispute 4: Quickstart example output format -- RESOLVED
- **Resolution:** No literal terminal output block. Prose description naming the five phase headers (Review, Cross-review, Revision, Disputes, Synthesis) and the output structure (headline verdict + summary). Include a `--format json` verification note. Phase names are architecturally stable (derived from `engine/phases.py` and the template directory structure).
- **Agreeing agents:** code-verifier, user-advocate, developer-advocate.
- **Path to convergence:** My original concern about output fragility was addressed by replacing the literal block with durable prose. User-advocate's refinement to make the item text self-contained (explicitly naming the five headers) was accepted by both code-verifier and me.

### Dispute 5: Error handling documentation -- RESOLVED
- **Resolution:** Descriptive section on framework catch-and-skip behavior plus prescriptive section with three "recommended patterns" bullets: raise freely, use `.get()` with defaults for consumed data, check warning-level logs. Clearly labeled as "recommended patterns" -- an epistemic boundary reflecting observed framework behavior rather than contractual guarantees.
- **Agreeing agents:** code-verifier, user-advocate, developer-advocate.
- **Path to convergence:** Code-verifier corrected my original "return empty dicts" guidance; I accepted the correction and shifted to "raise freely." User-advocate's framing of the label as a deliberate epistemic boundary (not a soft hedge) is accepted for spec 031 scope. Three prescriptive bullets are source-verified at `domains/base.py` L697-708 and `plugins/base.py` L519-525.

### Dispute 6: Implementation plan ordering -- RESOLVED
- **Resolution:** Three parallel tracks (Code Fixes, Onboarding, Extensibility) with intra-track priority ordering. No inter-track hard dependencies. When resources are serial, track order (code fixes, onboarding, extensibility) reflects implementation priority. I acknowledge my preference for priority-tier interleaving is equally valid but will not escalate the difference.
- **Agreeing agents:** code-verifier, user-advocate, developer-advocate.
- **Path to convergence:** All three reviewers agree on the underlying structure. The divergence is a minor scheduling heuristic that does not affect what gets built or the final documentation artifacts.

### Documentation Principle -- RATIFIED
- **Copy-paste test:** Scoped to SDK and quickstart first examples, with tutorial and YAML exemptions.
- **Failure-mode annotations:** Every SDK function documented whose return type includes `| None` or whose implementation raises exceptions must include an inline annotation describing the failure case.
- **Agreeing agents:** code-verifier, user-advocate, developer-advocate.

### Cross-Review Findings -- CLEAN
Both cross-reviews of my Round 3 revision found zero dangerous contradictions. The editorial tensions listed under "Remaining Disputes" above are the only items that did not reach identical wording across all three agents, and none of them affect the implementation plan.

## Final Position Statement

The review pipeline has reached full convergence. Three reviewers, three rounds, six disputes raised, six disputes resolved. Zero items are disputed, deferred, or withdrawn. The 3-track, 28-item implementation plan is ratified unanimously.

**What was achieved for the developer audience:**

1. **End-to-end domain tutorial (P1-Ext-1):** The single largest documentation gap -- a developer could not ship a domain plugin from the existing docs alone. The converged plan delivers a complete extract-score-persist-gate-serve lifecycle tutorial with self-contained setup, all types verified against source.

2. **Plugin wiring lifecycle (P1-Ext-2):** Developer-facing wiring steps (make the module importable, set `package` to the dotted path, understand the failure mode) paired with the `plugins:` config-reference section. Single deliverable.

3. **Error handling guidance (P2-Ext-5):** Descriptive and prescriptive content, clearly labeled, giving a developer writing their first plugin three actionable patterns to follow.

4. **API reference structure (P2-Ext-3):** Narrative prose plus class catalogs on all API reference pages, with `domains/base.md` receiving the `members:` list it currently lacks.

5. **Hard block dispatch documentation (P3-Ext-8):** The behavioral difference between module-level `_check_hard_blocks` and `DomainPlugin.evaluate_hard_blocks()` is documented, preventing a subtle integration surprise.

**Concessions maintained (all 5 from prior rounds, not reversed):**

1. Withdrew "return empty dicts" error handling guidance. "Raise freely" is correct.
2. Corrected `DomainContext.changed_files` type from `list[str]` to `list[Path]`.
3. Accepted `score()` interface is typed and docstringed; the gap is demonstration coverage.
4. Decoupled import namespace documentation from `classify` re-export code change.
5. Accepted plugin loader uses alphabetical `dir()` order; documentation says "define exactly one per module."

**Assessment:** Once the P1 items ship, a developer will be able to go from zero to a working custom domain plugin without leaving the documentation. The plan meets the bar I set at the start of this review. The pipeline is ready for implementation.
