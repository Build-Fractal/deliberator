### Remaining Disputes

- **Dispute: L1589 Replacement Text — Naming VI and X vs. Version/Cycle Reference**
  - **My claim**: The replacement text for L1589 MUST NOT name VI and X by number in the migrate-out clause. My revision proposes: "Grandfathered-principle remediation electing the migrate-out pattern is governed by the v3.0.0 MAJOR amendment (spec 070 cycle 2) as the canonical migrate-out precedent." This formulation uses version and cycle identifiers only, so the sentence remains accurate if the synthesis arbiter accepts rrs's Rec 2 (modified) and the substrate analysis concludes X should be retained via path (c) rather than removed. See crc/revision.md, Rec 1.
  - **Opposing position(s)**: migration-soundness (ms) New Recommendation proposes: "Principles VI and X were subsequently remediated via the migrate-out pattern in this (v3.0.0) amendment." This names VI and X directly. See ms/revision.md, New Recommendation, Proposed change paragraph.
  - **Why I will not concede**: ms's formulation bakes the migrate-out outcome for both VI and X into the constitutional body text before rrs's P1 substrate analysis for X has been resolved. If the arbiter accepts rrs's modified Rec 2 — requiring documented Criterion 3 analysis for X's "one clear purpose per output file" sub-bullet — and that analysis concludes the sub-bullet is independent of V and VII, a subsequent amendment may reconstitute X. At that point ms's body-text sentence ("Principles VI and X were subsequently remediated via the migrate-out pattern") would be constitutionally false. The conservative wording (version + cycle, naming only Principle XVI) survives any downstream outcome for X. Naming VI and X in body text is not merely premature — it forecloses the analytical question rrs's modified Rec 2 correctly requires to be left open.
  - **Counter-argument to their position**: ms argues the L1589 sentence needs concrete examples to be useful to future amendment authors. But version/cycle references are equally concrete — "the v3.0.0 MAJOR amendment (spec 070 cycle 2)" is unambiguous — and they do not encode an outcome that remains analytically contested. The navigational improvement ms seeks (make the migrate-out precedent findable) is fully achieved by version + cycle reference. The specific principle numbers add only one thing: premature commitment to a result that the arbiter must still adjudicate.
  - **Proposed resolution path**: Adopt crc's proposed wording (my revision, Rec 1) for the migrate-out clause: "governed by the v3.0.0 MAJOR amendment (spec 070 cycle 2) as the canonical migrate-out precedent." If the arbiter subsequently confirms both VI and X as migrate-out, a follow-up PATCH may name the principles explicitly. The cost of naming them in that PATCH (if warranted) is zero; the cost of un-naming them in a corrective PATCH (if X's disposition changes) is constitutional credibility. The synthesizer should choose the conservative formulation.

---

- **Dispute: Sequencing — Are Analytical Fixes Gating or Co-Equal with Operational Completions?**
  - **My claim**: The mkdocs.yml nav entry (crc New Rec 1, P1) and the L1589 fix (crc Rec 1, P1) are co-equal pre-ratification blockers that address different distribution surfaces and neither gates the other. See crc/revision.md, New Recommendations, first bullet; Rec 1 Explanation.
  - **Opposing position(s)**: removal-rigor-skeptic's New Recommendation explicitly declares that "analytical fixes from this review's scope (Recs 1–3, specifically the documented substrate analysis for X per Rec 2 modified) are sequencing gates for migration-soundness's operational completions (ms Recs 1 and 7 — mkdocs.yml nav entry and atomic commit boundary)." rrs argues the mkdocs.yml nav entry and atomic commit ratification should be held pending stable resolution of the analytical track. See rrs/revision.md, New Recommendations.
  - **Why I will not concede**: The mkdocs.yml nav entry's correctness does not depend on X's disposition. docs/output-conventions.md exists on disk (confirmed by ms's review: `?? docs/output-conventions.md` in git status) regardless of whether X is removed or retained via path (c). The nav entry makes the file discoverable via the built docs site. If X is subsequently retained via path (c), the file's content would need updating, but the nav entry is not rendered wrong — it would simply need to point at an updated file. Blocking the nav entry behind the analytical substrate analysis serves no protective function: it cannot produce a wrong nav entry, only a nav entry pointing at a file whose content is in flux. The only genuine gating requirement is that the atomic commit must hold until the entire pre-ratification P1 set is resolved; rrs's sequencing claim goes further and imposes an ordering within that set that is not justified by the operational dependency structure.
  - **Counter-argument to their position**: rrs's sequencing argument conflates "documents that depend on each other" with "work-tracks that depend on each other." The analytical question (is X's substrate independent?) is a different question from the nav infrastructure question (does the docs site expose the file?). They are co-present dependencies, not a dependency chain. rrs's framing would mean a CI infrastructure fix must wait for a constitutional analysis to conclude — a sequencing that generates no protective benefit and introduces scheduling risk (the analytical track has no hard deadline; the nav entry is a one-line edit).
  - **Proposed resolution path**: The synthesizer should declare the co-equal framing. Both P1 fixes are prerequisites for ratification and neither gates the other. The atomic commit must hold the full set — both P1 items plus any other pre-ratification P1 findings. The analytical substrate analysis (rrs Rec 2 modified) is also a prerequisite for the ratification commit, but it gates the commit as a whole, not specifically the nav entry or L1589 fix.

---

### Convergence

- **Converged: L1589 is stale and must be replaced before ratification**
  - **Shared position**: The current L1589 text — "The 2026-05-01 spec 070 cycle 1 amendment establishing this definition is the canonical path (c) precedent for future remediation of Principles VI and X" — is semantically incoherent in the post-removal document. It presents VI and X as future remediation targets when they are being removed in this amendment. This sentence must be replaced before tagging v3.0.0.
  - **Agreeing agents**: All three. crc/revision.md Rec 1; rrs/revision.md Rec 1 (Modified); ms/revision.md New Recommendation.
  - **Strength**: Unanimous
  - **Path to convergence**: This was a disputed claim in Phase 1 only because the cross-reference audit missed the plural form "Principles VI and X" in the regex search. Once rrs independently identified the plural-form miss and ms confirmed it from the infrastructure audit, all three agents converged rapidly. The dispute that remains is only over wording, not over whether the fix is required.

---

- **Converged: mkdocs.yml nav entry for docs/output-conventions.md is a P1 pre-ratification blocker**
  - **Shared position**: docs/output-conventions.md must be added to mkdocs.yml's `nav:` block before tagging v3.0.0. Without this entry, the file is invisible to every contributor who uses the built docs site (MkDocs with explicit nav excludes unlisted files from rendered navigation). The file exists on disk but is navigably orphaned.
  - **Agreeing agents**: All three. crc/revision.md New Recommendations first bullet; ms/revision.md Rec 1 (Modified); rrs/revision.md did not contest the finding (rrs confirmed this as uncontested in their cross-review of ms).
  - **Strength**: Unanimous
  - **Path to convergence**: ms identified this in Phase 1 from direct inspection of mkdocs.yml (L77-116 contain no entry for output-conventions.md). crc acknowledged the scope gap in Phase 2 (had verified file existence but not traversability) and adopted the finding in Phase 3. rrs acknowledged it as uncontested.

---

- **Converged: SIR's "zero body-text cross-references" claim is false; regex methodology must be corrected**
  - **Shared position**: The v3.0.0 SIR's cross-reference audit claim is factually incorrect: the plural form "Principles VI and X" at L1589 of the Governance body text was not found by the singular-form regex search. The SIR must acknowledge this miss, explain the plural-form gap, and the corrective methodology (include singular, plural, and adjacent-phrase forms of removed principle identifiers) must be documented for future amendments.
  - **Agreeing agents**: All three. crc/revision.md Rec 2 (Surviving) + Rec 5 (Surviving); rrs/revision.md Rec 1 (Modified, methodology correction co-packaged) + Rec 8 (Modified, upgraded to P2); ms/revision.md New Recommendation.
  - **Strength**: Unanimous
  - **Path to convergence**: Phase 1 discovery (rrs identified the plural-form miss, crc confirmed the SIR claim was false). Phase 3 convergence on co-packaging the claim correction with the methodology correction (rrs Rec 8 upgraded to P2 for precisely this reason).

---

- **Converged: Atomic commit must include five or more files**
  - **Shared position**: The v3.0.0 commit must atomically include at minimum: CONSTITUTION.md (with L1589 and Governance body text corrections), CONTRIBUTING.md, docs/output-conventions.md, mkdocs.yml, and any additional files required by other P1 findings. ms's original four-file enumeration was underspecified; the Governance body text edits add at least one more.
  - **Agreeing agents**: crc/revision.md New Recommendations (first bullet, co-equal P1 pair statement); ms/revision.md Rec 7 (Modified); rrs/revision.md New Recommendation (sequencing framing, which accepts the multi-file boundary).
  - **Strength**: Unanimous (on the expanded count; dispute on sequencing within the set, not on the set membership)
  - **Path to convergence**: ms identified the four-file boundary in Phase 1. In Phase 3, ms revised to five-or-more after crc's cross-review identified that Governance body text edits (which ms's Phase 1 scope excluded) add to the required file set.

---

- **Converged: CONTRIBUTING.md → docs/output-conventions.md cross-reference needs inline placement, not heading-level-only**
  - **Shared position**: The existing cross-reference at CONTRIBUTING.md L42-48 (a separate sibling subsection heading) is insufficient on its own because contributors who stop reading at the VI section body boundary (L40) will not encounter it. An inline closing sentence within the VI section body is required as a complementary navigation path.
  - **Agreeing agents**: ms/revision.md Rec 4 (Surviving); crc/revision.md New Recommendations second bullet. rrs did not contest (scope exclusion).
  - **Strength**: Bilateral (ms + crc)
  - **Path to convergence**: ms identified the structural isolation problem in Phase 2 (cross-review of crc's "coherent" characterization). crc conceded in Phase 3 that existence of a navigational path is not the same as likelihood of traversal, and adopted ms's structural observation as a new recommendation.

---

### Final Position Statement

**Non-Negotiables**

1. The L1589 replacement text MUST NOT name VI and X by principle number in the migrate-out clause. The replacement text must use version and cycle identifiers only (plus Principle XVI for the path (c) clause), leaving the migrate-out examples unspecified until the analytical substrate analysis for X resolves X's final disposition. This is non-negotiable because naming VI and X in body text would make the constitutional record factually contingent on the outcome of rrs's Rec 2 — a question that by rrs's own modified position remains open. A constitutional sentence whose truth-value depends on the outcome of a concurrently open analytical question is a structural defect, not a navigational preference. See crc/revision.md Rec 1.

2. The mkdocs.yml nav entry for docs/output-conventions.md must be included in the pre-ratification commit as a co-equal P1 item, not deferred or subordinated to the analytical track's resolution. The nav entry is correct under all possible outcomes for X (if X is retained via path (c), the file content updates but the nav entry remains valid). Holding the nav entry behind the analytical resolution provides no correctness guarantee and introduces unnecessary scheduling risk. See crc/revision.md New Recommendations, first bullet.

**Flexibility**

1. Recs 3 and 4 (Governance operational-guidance destinations list and migration pointer) are conditioned on the synthesis arbiter sustaining the analytical validity of the removals. If the arbiter accepts rrs's modified Rec 2 and the substrate analysis concludes X warrants reconstitution, these recommendations should be held. What must be preserved: the underlying navigability requirement — once the migration is analytically settled, the Governance body text MUST establish a navigable pointer to the operational-guidance destinations so amendment authors working in the Governance section can find them. The specific implementation (destinations list addition vs. migration pointer paragraph) is flexible if the synthesizer finds a combined form that serves both purposes.

2. The dual-surface reachability check (Rec 7 modified: README → CONTRIBUTING.md and docs/developer-guide/contributing.md → root CONTRIBUTING.md) is flexible on priority assignment. My revision treated the combined check as P2 (matching ms's priority for the docs-site surface). The synthesizer may assign different priorities to the two surfaces if evidence warrants. What must be preserved: both surfaces must be verified and updated in the same commit, not in separate PRs. A contributor arriving via GitHub and a contributor arriving via the built docs site are both legitimate primary paths; both must reach the VI/X authoring guidance without dead-ends.