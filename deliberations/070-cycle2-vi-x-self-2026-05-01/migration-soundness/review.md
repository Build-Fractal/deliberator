I'll read the target files before writing the review.

Now let me also check if there's a mkdocs.yml to assess discoverability:

### Executive Summary

The v3.0.0 migration removes Constitutional Principles VI (Scripts Over Markdown) and X (Zen of Python Output) and relocates their substantive guidance to CONTRIBUTING.md and docs/output-conventions.md respectively. This review audits whether the migrated documents faithfully preserve the original principle bodies, correctly apply the MUST → SHOULD strength reduction, and satisfy the structural commitments described in the v3.0.0 SIR.

The migration is substantially sound. All three VI sub-bullets survive in CONTRIBUTING.md with correct normative relaxation. Four of the five X bullets survive as main Conventions in docs/output-conventions.md; the fifth — "errors should never pass silently" — has been repositioned into a separate "Recommended implementation patterns" subsection, which is consistent with the v3.0.0 SIR's explicit intent but is not called out in the document itself, creating a silent structural demotion that a reader comparing to prior versions will notice without explanation. Provenance footers are accurate in both documents. The one concrete failure is discoverability: docs/output-conventions.md is absent from `mkdocs.yml`'s `nav:` block, meaning it will not appear in the built documentation site navigation despite existing on disk.

**Most important recommendation**: Add `docs/output-conventions.md` to `mkdocs.yml`'s `nav:` block under Developer Guide alongside the contributing entry, and add a one-sentence explanatory note in docs/output-conventions.md stating that "errors should never pass silently" was intentionally repositioned from the main Conventions list to the Recommended patterns section.

---

### Alignment

- **VI sub-bullet 1 preserved** (CONTRIBUTING.md L24-25): "Orchestration logic SHOULD live in SKILL.md (executable spec) and templates (parameterized prompts), not in freeform documentation." This is a faithful SHOULD-form translation of the original "orchestration logic in SKILL.md and templates, not freeform docs" requirement.

- **VI sub-bullet 2 preserved** (CONTRIBUTING.md L26-27): "Configuration SHOULD live in YAML (`conversus.yml`, preset files), not in markdown tables or inline instructions." Correctly preserves the "Configuration in YAML, not markdown tables" bullet with appropriate normative relaxation.

- **VI sub-bullet 3 preserved** (CONTRIBUTING.md L28-30): "When a markdown artifact exists purely for human orientation (quickstart, README), markdown is appropriate. When it drives agent behavior, prefer structured and executable formats." Preserves the human-orientation carve-out faithfully.

- **VI justification prose present** (CONTRIBUTING.md L33-40): The rationale for why the principle was migrated ("the qualifier 'when the artifact drives behavior' requires interpretation in every application") is present and accurate, correctly citing the v2.4.0 Constitutional Inclusion Criteria gate.

- **X bullets 1–4 in Conventions section** (docs/output-conventions.md L16-27): "One obvious way to find the result," "flat is better than nested," "sparse is better than dense," and "if the implementation is hard to explain" all appear as main Conventions bullets. Content is preserved verbatim in spirit; the predictable output tree concrete example (`summary/final.md`) is retained at L17.

- **X bullet 5 (errors/warnings) in Recommended patterns** (docs/output-conventions.md L34-41): The "errors should never pass silently" substance survives as the "Warnings for malformed output" pattern. The content — "code that processes output artifacts SHOULD emit a warning when expected fields are missing, documents are malformed, or edge cases are encountered. Silent failure is worse than warned-and-continued behavior" — accurately captures the original bullet. The v3.0.0 SIR explicitly calls out this repositioning: "the mechanically-checkable parts (e.g., 'warnings for malformed output') flagged as RECOMMENDED implementation patterns."

- **Provenance footers accurate** (CONTRIBUTING.md L52-53; docs/output-conventions.md L68-69): Both footers read "Migrated from CONSTITUTION.md Principle [VI|X] in v2.6.0 → v3.0.0 per spec 070 cycle 2 (2026-05-01)." Principle numbers, version range, spec citation, and date are all correct.

- **Cross-reference present** (CONTRIBUTING.md L43-48): The "Output Conventions (cross-reference)" subsection at L43-48 links to `./docs/output-conventions.md` with the correct relative path from the repo root.

---

### Missed Opportunities

- **mkdocs.yml nav entry absent**: `docs/output-conventions.md` exists on disk (confirmed at `docs/output-conventions.md` in the docs tree) but is not listed in the `nav:` block in `mkdocs.yml`. The nav block enumerates every routed page explicitly (`mkdocs.yml` L77-116); files not listed do not appear in site navigation. A contributor who reaches the docs site will find no path to this document through navigation. The cross-reference from CONTRIBUTING.md (`./docs/output-conventions.md`) is relative to the repo root and renders correctly on GitHub, but provides no navigation entry in the built documentation. Impact: **high** — the primary purpose of docs/output-conventions.md is discoverability for contributors; if it cannot be navigated to, the migration's operational-guidance framing is undermined.

- **Silent structural demotion of "errors should never pass silently"**: The repositioning of the errors/warnings bullet from the main Conventions list to the Recommended implementation patterns subsection is not explained in docs/output-conventions.md itself. A reader of the v2.6.0 constitution who consults this document will see four main Conventions bullets and then a separate Recommended patterns section, without any note that the fifth original bullet was intentionally placed there rather than in the main list. The v3.0.0 SIR explains the rationale (the mechanically-checkable parts are promoted to RECOMMENDED patterns), but that rationale is in the SIR comment block, not in docs/output-conventions.md. The "Why operational guidance, not constitutional" section (L49-64) explains the overall migration but does not address the within-document structural choice. Impact: **medium** — causes confusion for contributors cross-referencing against prior principle versions.

- **Redundancy between main Conventions and Recommended patterns for "predictable output tree"**: The predictable output tree concept appears twice: once in the main Conventions section (L16-17: "There SHOULD be one obvious way to find the result. The output tree follows a predictable structure: `summary/final.md` is always the starting point") and again in the Recommended patterns section (L43-44: "Predictable output tree: output emitters SHOULD write to paths derivable from the config"). The second entry is a subset of the first with different framing. This is not harmful but creates mild confusion about which is authoritative. Impact: **low**.

- **developer-guide/contributing.md not cross-referenced to root CONTRIBUTING.md**: `mkdocs.yml` L97 lists `developer-guide/contributing.md` under the Developer Guide nav. This is a separate file from the repo-root `CONTRIBUTING.md` that carries the VI migration. No evidence exists in the review that `docs/developer-guide/contributing.md` references or is aware of the root CONTRIBUTING.md's VI-migration content. If that page is the primary contributor entry point via the docs site, VI's new operational guidance is not surfaced there. Impact: **medium** — contributor reachability.

---

### Off-Base Assumptions

- **SIR claims CONTRIBUTING.md "cross-references" docs/output-conventions.md**: The SIR states CONTRIBUTING.md cross-references docs/output-conventions.md, implying the reference appears inline with or adjacent to the VI content. The actual document structure places the cross-reference in a separate subsection titled "Output Conventions (cross-reference)" (CONTRIBUTING.md L42-48) after the VI content concludes, rather than within or beneath the VI section itself. This is not incorrect, but a contributor reading the VI section (L17-40) who stops before the next subsection will not encounter the cross-reference. The subsection title "Output Conventions (cross-reference)" is clear, but it is a separate heading-level item, not a footer note under the VI content. This is a structural assumption discrepancy rather than a factual error, but it affects the navigation experience the SIR implies.

- **No wrong assumptions about migration mechanics**: The SIR's assertion that the migrate-out pattern "removes the principle entirely and the substantive guidance lives in operational guidance" is correctly reflected in both documents. Neither CONTRIBUTING.md nor docs/output-conventions.md contains inadvertent MUSTs that should have been relaxed (the only uses of MUST in both files are within quoted passages or in the introductory framing about the constitution governing, not in the migrated bullet content itself). The strength-reduction audit finds no mismatches.

---

### Actionable Recommendations

1. **Add docs/output-conventions.md to mkdocs.yml nav** (Priority: P1)
   - **Current state**: `docs/output-conventions.md` exists at the root of the docs/ directory but appears nowhere in `mkdocs.yml`'s `nav:` block (L77-116). It is unreachable via site navigation.
   - **Proposed change**: Add an entry under Developer Guide in `mkdocs.yml` nav:
     ```yaml
     - Developer Guide:
       ...
       - Contributing: developer-guide/contributing.md
       - Output Conventions: output-conventions.md
     ```
     Or alternatively under a new "Reference" section if the page's scope feels broader than Developer Guide.
   - **Rationale**: MkDocs with an explicit `nav:` block does not auto-discover unlisted pages in site navigation. The file exists but is navigably invisible.
   - **Risk if ignored**: docs/output-conventions.md is effectively a dead page in the built docs site. The Principle X migration succeeds in creating the file but fails to surface it to any contributor who consults the documentation rather than GitHub.

2. **Add structural-demotion note for "errors should never pass silently"** (Priority: P2)
   - **Current state**: docs/output-conventions.md moves the errors/warnings content to the Recommended implementation patterns section (L34-41) without explaining why it is there rather than in the main Conventions list.
   - **Proposed change**: Add a one-sentence lead-in to the Recommended implementation patterns section, e.g.: "The following patterns derive from the original principle's content; they are placed here rather than in the Conventions list above because they are mechanically checkable and warrant explicit implementation guidance, consistent with the v3.0.0 SIR's framing."
   - **Rationale**: The v3.0.0 SIR explicitly calls out this structural choice. Without it being reflected in the document, the repositioning appears arbitrary.
   - **Risk if ignored**: Future contributors editing the document may inadvertently move the errors/warnings bullet back to the main Conventions list, believing it was misplaced.

3. **Resolve predictable-output-tree duplication in docs/output-conventions.md** (Priority: P3)
   - **Current state**: The "predictable output tree" concept appears at both L16-17 (main Conventions: "There SHOULD be one obvious way to find the result. The output tree follows a predictable structure: `summary/final.md` is always the starting point") and L43-44 (Recommended patterns: "Predictable output tree: output emitters SHOULD write to paths derivable from the config").
   - **Proposed change**: Remove the Recommended patterns entry for "Predictable output tree" (L43-44 and its surrounding bullet), since the concept is already covered more concretely in the main Conventions section. Alternatively, make L16-17 the implementation-guidance form and remove the prose from Recommended patterns.
   - **Rationale**: Single source of truth (Principle XI) applies to operational guidance documents as much as to the codebase.
   - **Risk if ignored**: Low duplication risk — the two entries say slightly different things and a future edit to one may create drift with the other.

4. **Cross-reference VI content to X content within CONTRIBUTING.md** (Priority: P2)
   - **Current state**: The "Output Conventions (cross-reference)" subsection (L42-48) is a separate heading-level item following the VI content, not a closing note within the VI section. A contributor who reads L17-40 and stops at the section break may not encounter the cross-reference.
   - **Proposed change**: Add a closing sentence to the VI section body (before the provenance footer), e.g.: "See [`docs/output-conventions.md`](./docs/output-conventions.md) for companion guidance on clean output structure (formerly Principle X)."
   - **Rationale**: The SIR characterizes these as paired migrations; that relationship should be surfaced inline in the VI section, not only as a separate subsection header.
   - **Risk if ignored**: Contributor reads VI section, does not discover X migration, implements output-emitting code without awareness of the output conventions guidance.

5. **Verify docs/developer-guide/contributing.md references root CONTRIBUTING.md VI content** (Priority: P2)
   - **Current state**: `mkdocs.yml` L97 routes `developer-guide/contributing.md` as the "Contributing" page in the Developer Guide nav. The root `CONTRIBUTING.md` (which carries the VI migration and the cross-reference to X) is not listed in `mkdocs.yml` and is therefore a repo file, not a docs site page.
   - **Proposed change**: Inspect `docs/developer-guide/contributing.md` and either (a) add a reference to the root CONTRIBUTING.md's Scripts Over Markdown and Output Conventions sections, or (b) reproduce or transclude the relevant authoring conventions content.
   - **Rationale**: If contributors arrive at the docs site's "Contributing" page rather than GitHub's CONTRIBUTING.md, they will not encounter the VI or X operational guidance unless this page surfaces it.
   - **Risk if ignored**: The primary docs-site entry point for new contributors does not surface the migrated authoring conventions.

6. **Confirm no inadvertent MUSTs in migrated bullet bodies** (Priority: P1 — verification)
   - **Current state**: Both files avoid MUSTs in bullet content (verified: CONTRIBUTING.md L24-30 uses SHOULD throughout; docs/output-conventions.md L16-27 uses SHOULD throughout; Recommended patterns section L34-47 uses SHOULD and "RECOMMENDED"). No inadvertent MUSTs found.
   - **Proposed change**: No change required. Document as confirmed-clean in the v3.0.0 ratification record.
   - **Rationale**: The v3.0.0 SIR's strength-reduction claim (MUST → SHOULD "where the underlying judgment call cannot be mechanized") is verified as correctly implemented.
   - **Risk if ignored**: N/A — this is a clean finding, documented here for completeness.

7. **Add docs/output-conventions.md to mkdocs.yml before tagging v3.0.0** (Priority: P1 — ordering)
   - **Current state**: The git status shows `?? docs/output-conventions.md` (untracked), meaning it has not yet been committed alongside the CONSTITUTION-v3.0.0 candidate.
   - **Proposed change**: The commit that lands CONSTITUTION.md v3.0.0, CONTRIBUTING.md, and docs/output-conventions.md MUST also include the `mkdocs.yml` nav update as an atomic change. These four files form one logical migration unit; a release that ships the constitution change without the nav update leaves the migration incomplete.
   - **Rationale**: Principle XXII (Distribution Surface Integrity) requires all distribution surfaces to be updated atomically. The docs site is a distribution surface for operational guidance.
   - **Risk if ignored**: A window exists post-merge where docs/output-conventions.md is live but undiscoverable through site navigation, and any release tag in that window ships the incomplete state permanently to versioned docs.

---

### Referenced Documentation

- `<HOME>/code/payer-index-mono/conversus-oss/CONTRIBUTING.md` — all lines (L1-53); primary audit target for VI migration
- `<HOME>/code/payer-index-mono/conversus-oss/docs/output-conventions.md` — all lines (L1-69); primary audit target for X migration
- `<HOME>/code/payer-index-mono/conversus-oss/mkdocs.yml` — L77-116 (nav block); discoverability audit
- `CONSTITUTION-v3.0.0-candidate.md` (provided in prompt) — v3.0.0 SIR comment block (lines 1-160 of the candidate file header); versioning and migration rationale; Principle XXII (Distribution Surface Integrity)