### Executive Summary

The Conversus Constitution is a mature governance document for a multi-agent deliberation system. Its twenty-six active principles cover everything from spec-driven development (Principle I) through test-fix discipline (Principle XXVIII), and the document demonstrates unusual self-awareness: principles cite specific PRs and specs as origins, include worked examples, and impose a three-criterion gate on future amendments (Governance section, v2.4.0). The numbering system — Roman numerals, apparently stable across the document's history — is treated as load-bearing infrastructure, which makes the absent VI and X visible to any careful reader.

From a fresh-eyes reading, the document provides **no explanation** for the gaps. The Governance section discusses versioning class (MAJOR/MINOR/PATCH), amendment process, and the three-criterion inclusion gate in detail, but contains no statement about principle-number stability, gap preservation, or reuse prohibition. A first-time reader encountering the sequence I through V, then VII without VI, has only the document; the document is silent. This review's prompt asserts "the document explicitly says 'Future amendments MUST NOT reuse numbers VI or X'" — but this sentence does not appear anywhere in the constitution text. That is not a minor editorial oversight; it is a governance vacuum. The gap pattern is almost certainly intentional and correct by analogy to RFC/CVE numbering discipline, but "almost certainly" is not a stable foundation for a governance document that otherwise demands mechanical verifiability.

The single most important recommendation: add an explicit paragraph to the Governance section documenting that principle numbers are permanent identifiers, that VI and X correspond to removed principles, and that no future amendment may reuse them — identical in intent to what RFC and CVE number registries enforce, and in spirit with the document's own Principle XI (Single Source of Truth).

---

### Alignment

- **Origin citations as historical anchors** (every principle, *Origin* blocks): Each principle's *Origin* block cites a specific PR or spec: "PR #10 (red-blue contract break)", "spec 006 — Phase StrEnum was created". This practice directly supports stable numbering by making each principle traceable to a unique historical event. A principle whose origin is cited by PR number can be removed without renaming; citations in commit messages remain valid because the number is fixed. The discipline is coherent with RFC-style identifier stability.

- **Phase numbering is declared fixed** (Principle III, paragraph: "Phase numbering (1-6) is fixed. New orchestration capabilities are added as conditional behavior within existing phases or as new named phases after Phase 6."): The document already understands the value of stable sequential identifiers for a different enumerated set (phases). It locks phase numbers explicitly. This is exactly the right instinct — the same reasoning applies to principle numbers.

- **Three-criterion gate creates clear PATCH/MINOR/MAJOR boundaries** (Governance, "Versioning" and "Constitutional Inclusion Criteria" paragraphs): The v2.4.0 gate makes amendment classification mechanical. Stable numbering is a natural complement to this: if a principle is removed (triggering a MAJOR version bump), its number retires rather than being recycled into the new MINOR or PATCH. The version-class taxonomy already implies this — "MAJOR for principle removals or redefinitions" — but the number-retirement consequence is not spelled out.

- **Principle II's stable-interfaces concept provides direct precedent** (Principle II, opening sentence and bullets): "Structural markers, template variables, the dispute-parsing subsystem, the preset schema, reference file paths, and the dispatch table are stable contracts." Principle numbers are used exactly like structural markers: cited in PR descriptions, governance logs, cross-references within the document. The stable-interfaces concept should explicitly include principle numbers.

---

### Missed Opportunities

- **No stable-identifier policy for principle numbers**: The document defines stable interfaces for template markers, variable names, subcommand names, and reference file paths (Principle II), but principle numbers themselves are never added to that list. A PR description citing "Principle VI" in a git log is a consumer of the number VI in exactly the same way that `<!-- CONVERSUS:DISPUTES_BEGIN -->` is a consumer of that marker. The omission means the stability guarantee exists in practice but not in writing. Impact: **high** — a future contributor could propose renumbering (to "clean up the gaps") without realizing they are breaking a de facto stable interface.

- **The no-reuse rule is undocumented**: The prompt's assertion that "the document explicitly says 'Future amendments MUST NOT reuse numbers VI or X'" is false — this sentence does not appear in the text. The rule is the correct one (see RFC 2026 §3.3, CVE numbering authority policy), but an undocumented rule is an unenforced rule. Principle IV ("Documentation Is the Product") and Principle XI ("Single Source of Truth") both demand that governance rules be written down in their authoritative location. The no-reuse rule has no authoritative location. Impact: **high**.

- **No tombstone record for removed principles**: RFC and CVE registries handle retirements with explicit status records ("Obsoleted by RFC NNNN", "RESERVED", "REJECTED — duplicate"). The constitution removes a principle and leaves a gap but provides no equivalent tombstone. A reader cannot determine whether VI and X were: (a) removed after ratification, (b) drafted and withdrawn before ratification, or (c) never assigned. These are materially different governance events. Impact: **medium** — does not break the system, but creates historical opacity that the document otherwise works hard to avoid (see every *Origin* block).

- **Governance section's versioning entry does not mention number-retirement**: The Governance section states "MAJOR for principle removals or redefinitions" but does not complete the implication: removal → number retired, never reused, tombstone added. The three-criterion gate (v2.4.0) includes detailed worked examples for the inclusion case; there is no comparable worked example for the removal case. Impact: **medium**.

- **Calibration footnote creates implicit census**: The Governance section reads: "When drafting new principles, prefer the structural pattern of principles whose verification artifact is named explicitly (e.g., Principles XI, XII, XIII, XXII, XXIV, XXVI)." This list is fine as-is, but it implicitly invites a reader to count all principles with explicit verification artifacts. The gaps in numbering make that count ambiguous — is the total 26 (the highest assigned number minus 2 retired) or 28 (the raw highest number)? A reader trying to assess "how much of the constitution satisfies the verification criterion" gets two different answers depending on which denominator they use. Impact: **low** — readability friction, not a correctness problem.

- **No amendment template includes number-retirement step**: The Governance section describes the amendment process ("document the change, rationale, and impact on existing specs") but provides no checklist for the removal case. A contributor removing a principle today would have no guidance that they should add a tombstone entry rather than simply deleting the section. Impact: **medium** — the gap means the next removal will repeat the documentation error.

- **Principle number stability not covered by Principle XXIV's three-layer defense**: Principle XXIV requires schema-level, parser-level, and contract-test defense for safety-critical paths. Principle number stability is arguably a safety-critical governance path (a mis-reused number could silently refer to two different principles in different historical periods), but no verification layer exists. A lint that checks "no principle body contains a cross-reference to a retired number" would catch accidental reuse. Impact: **low** — speculative risk, but consistent with the document's own defense-in-depth philosophy.

---

### Off-Base Assumptions

- **The prompt claims the document states the no-reuse rule**: The review framing says "The document explicitly says 'Future amendments MUST NOT reuse numbers VI or X.'" This statement is not present anywhere in the constitution text. Treating an absent rule as documented is a first-class violation of Principle XI (Single Source of Truth) and Principle IV (Documentation Is the Product). The correct understanding: the no-reuse behavior may be the intention of the document's authors, but as of the current text, it has no authoritative location.

- **The gaps are assumed to be self-explanatory**: The document is written for sophisticated readers (contributors, governance participants), and the gaps appear without comment. The implicit assumption is that the principle-number stability rationale is obvious enough not to require documentation. But the document's own Principle V ("Observable Deliberation") demands that every phase report progress, and Principle XIX designates certain content as "non-extractable core" because it "must be impossible to accidentally violate." The numbering governance is exactly the kind of invariant that becomes easy to accidentally violate when it is not written down. Self-evidence is not a substitute for documentation in a system this careful about documentation.

- **No wrong assumptions about numbering mechanics**: The gaps themselves (preserving VI and X rather than renumbering to close them) reflect the correct decision — stable identifiers, never reused, analogous to RFC numbers. This is not an error in the document's approach; it is an error in the document's failure to explain and enforce the approach it is already following.

---

### Actionable Recommendations

1. **Document the no-reuse rule** (Priority: P1)
   - **Current state**: The Governance section discusses versioning and amendment process but contains no statement about principle number stability or the prohibition on reusing retired numbers. The phrase "Future amendments MUST NOT reuse numbers VI or X" does not appear in the document.
   - **Proposed change**: Add to the Governance section under "Amendments" or as a new "Principle Number Stability" subsection: "Principle numbers are permanent identifiers. A number assigned to a ratified principle is never reassigned, even after the principle is removed. Numbers VI and X are retired; they MUST NOT be reused by future amendments. This follows RFC and CVE numbering discipline: stable identifiers preserve the validity of historical citations in PR descriptions, governance logs, and external references."
   - **Rationale**: Principle IV states that in a prompt-orchestrated system, specification text IS the implementation. A rule that exists only in the authors' shared understanding, not in the document, is an undocumented rule — and undocumented rules are invisible to new contributors and automated checks alike.
   - **Risk if ignored**: A future contributor unfamiliar with the history could reasonably propose renumbering to "clean up" the gaps, invalidating every historical citation that uses principle numbers as stable identifiers.

2. **Add tombstone entries for VI and X** (Priority: P1)
   - **Current state**: VI and X are simply absent. The document provides no information about what occupied those numbers, when they were removed, or why.
   - **Proposed change**: Add stub entries in the numbered sequence:
     ```
     ### VI. [RETIRED]
     *Retired in v[X.Y.Z]. Number reserved; never reused.*
     [Optional: "Formerly: [principle name]. Superseded by / removed because...]"
     
     ### X. [RETIRED]
     *Retired in v[X.Y.Z]. Number reserved; never reused.*
     ```
   - **Rationale**: Every active principle has an *Origin* block. Retired principles should have an equivalent accountability record. The RFC "Historic" and CVE "RESERVED" statuses exist precisely for this purpose: to prevent the gap from being interpreted as an error and to provide audit continuity.
   - **Risk if ignored**: Readers cannot distinguish deliberate retirement from editing mistakes. The document's credibility as a carefully-maintained governance artifact is undermined by unexplained gaps.

3. **Add principle numbers to Principle II's stable-interfaces list** (Priority: P1)
   - **Current state**: Principle II lists stable contracts: "Structural markers, template variables, the dispute-parsing subsystem, the preset schema, reference file paths, and the dispatch table." Principle numbers are not listed.
   - **Proposed change**: Add to Principle II's list: "Principle numbers (Roman numerals I through the current highest) are stable identifiers. A principle's number is part of its identity and MUST NOT change. Retired numbers MUST NOT be reused (see Governance: Principle Number Stability)."
   - **Rationale**: Principle II is the canonical home for stable-interface declarations. Principle numbers are used in exactly the same way as structural markers — cited in PR descriptions, referenced in specs, cross-referenced within the document. Omitting them from this list creates an implicit stability guarantee that lacks the formal protection of an explicit one.
   - **Risk if ignored**: Breaking changes to principle numbers would not be recognized as breaking changes, bypassing the MAJOR version bump requirement.

4. **Extend the amendment process with a removal checklist** (Priority: P2)
   - **Current state**: Governance section says "Amendments: Require documentation of the change, rationale, and impact on existing specs" but provides no specific guidance for the removal case.
   - **Proposed change**: Add to the Amendments subsection: "When removing a principle: (1) Replace the principle body with a RETIRED tombstone (number, status, version removed, brief reason). (2) Bump the MAJOR version. (3) Search all active specs, templates, SKILL.md, and AGENTS.md for citations of the principle number; update or annotate each. (4) Add the retired number to the explicit no-reuse list in the Governance section."
   - **Rationale**: The three-criterion gate (v2.4.0) provides a detailed checklist for addition; removal has no equivalent. The asymmetry means additions are governed but removals are not.
   - **Risk if ignored**: The next principle removal will repeat the current state — a gap with no explanation, no tombstone, and no documented governance.

5. **Clarify denominator ambiguity in calibration footnote** (Priority: P2)
   - **Current state**: Governance calibration footnote: "When drafting new principles, prefer the structural pattern of principles whose verification artifact is named explicitly (e.g., Principles XI, XII, XIII, XXII, XXIV, XXVI)." The total principle count is ambiguous: 26 active principles (XXVIII minus 2 retired) or 28 (the highest assigned number).
   - **Proposed change**: Add a parenthetical: "(The constitution currently has 26 active principles; numbers VI and X are retired.)" This appears once, in the Governance section, and resolves all subsequent count ambiguities.
   - **Rationale**: The Governance section is where readers go to understand the document's structure. Stating the active count explicitly prevents the denominator confusion that arises from the gaps.
   - **Risk if ignored**: Readers assessing "what fraction of principles have explicit verification artifacts" get inconsistent answers; this undermines confidence in assessments that reference coverage or completeness.

6. **Bring principle-number stability under the three-criterion gate retroactively as a governance note** (Priority: P2)
   - **Current state**: The three-criterion gate (v2.4.0) applies to new principles. It does not address the governance of the numbering system itself as a stable interface.
   - **Proposed change**: Add to the three-criterion gate section: "Note: principle number retirement decisions (gap creation) are governed by the Principle Number Stability policy in Governance, not by this gate. The gate governs what is added; the retirement policy governs what is removed."
   - **Rationale**: The gate currently leaves an asymmetry: additions are carefully controlled, removals have no parallel discipline. This note does not fully close that gap (Recommendation 4 does), but it acknowledges the asymmetry within the gate's own text.
   - **Risk if ignored**: Contributors reading the gate may conclude it covers the full amendment lifecycle; the retirement path remains ungoverned by any formal mechanism.

7. **Extend Principle II's breaking-change definition to include principle-number reuse** (Priority: P3)
   - **Current state**: Principle II states: "Breaking changes MUST be coordinated across all consumers." It lists specific stable items but does not include principle-number reuse as an example of a breaking change.
   - **Proposed change**: Add to Principle II's bullet on coordination: "Reusing a retired principle number is a breaking change — any historical document that cited the retired number now references the wrong principle."
   - **Rationale**: Making the breaking-change consequence explicit converts an implicit norm into an enforceable rule. The mechanical check (lint for retired-number reuse) becomes straightforward to specify once the rule is written.
   - **Risk if ignored**: Low near-term risk; higher long-term risk as contributor turnover dilutes institutional memory about the numbering policy.

---

### Referenced Documentation

- `deliberations/070-cycle2-vi-x-blind-2026-05-01/CONSTITUTION-v3.0.0-blind.md` — all sections; specific citations: Principle I (introduction), Principle II (stable interfaces list and breaking-change coordination), Principle III (phase numbering fixedness), Principle IV (documentation as product), Principle V (observable deliberation), Principle IX (single source of truth), Principle XI (single source of truth), Principle XII (no dead infrastructure), Principle XVII (content classification), Principle XIX (non-extractable core), Principle XXIV (safety-critical defense-in-depth), Principle XXVIII (test-fix boundary); Governance section: "Amendments", "Versioning", "Constitutional Inclusion Criteria" (v2.4.0 gate), calibration footnote citing Principles XI, XII, XIII, XXII, XXIV, XXVI; all *Origin* blocks throughout.