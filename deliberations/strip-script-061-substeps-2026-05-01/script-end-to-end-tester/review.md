### Executive Summary

The `strip-constitution-for-blind.py` script implements spec 067 §4.2's stripping recipe against a targeted candidate version of `CONSTITUTION.md`. For the current v3.1.3 constitution, the core stripping pipeline works: the leading SIR block is correctly removed by Step 1, Amendment record subsections in Principles XXIV, XXV, and XXVII are correctly stripped by Step 3b, PR-referenced Origin notes are correctly stripped by Step 3's three patterns, and the version footer is correctly anonymized by Step 4. However, two substantive gaps exist. First, the prior SIR audit-trail blocks (labeled "Sync Impact Report (prior — preserved for audit trail)") are intentionally preserved by the script, but they contain repeated occurrences of the date "2026-05-01" — the same date as every v3.1.x amendment cycle. If `--date 2026-05-01` is passed to the script on the current v3.1.3 constitution, `verify_zero_leakage` will exit code 1 with at least five matches found in un-stripped prior SIR blocks. This is a self-defeating leakage check failure for the exact date the current amendment cycle used. Second, two of the arbiter-ruling sentence substitutions in Step 3b are now unreachable dead code on post-v3.1.0 constitutions because the sentences they targeted were moved from normative body text into Amendment record blocks in cycle 2B (v3.1.0), and those blocks are already consumed by the Amendment record regex earlier in Step 3b.

The script has zero automated test coverage. Every regex in the strip pipeline is exercised only by ad-hoc manual runs. Given the multi-version format hazards introduced in v3.1.x (Amendment records, sub-headings, bullet splits), the absence of tests means regressions in any future strip-script update would go undetected until a blind verification run fails.

**Most important recommendation**: add `scripts/tests/test_strip_constitution.py` with a fixture using the current `CONSTITUTION.md` that covers the v3.1.x-specific format hazards before the next blind verification run.

---

### Alignment

- **Step 1 SIR removal** (script L43-54): The first regex `r"^<!--\nSync Impact Report.*?-->\n\n"` with `count=1` and `DOTALL` correctly removes the v3.1.3 SIR block, which is the leading block starting with `<!--\nSync Impact Report\nVersion change: 3.1.2 → 3.1.3`. The `count=1` constraint ensures only the current SIR is consumed, not the preserved prior blocks.

- **Amendment record stripping** (script L62-66): The `r"\*Amendment record \([^)]*\):[^*]*\*\n+"` pattern with `DOTALL` correctly matches all three Amendment record blocks in the current constitution — XXIV, XXV, and XXVII — because none of those blocks has a nested parenthesis inside the date/label portion `(2026-04-25, arbiter ruling)`. The `[^)]*` inside `\([^)]*\)` safely captures "2026-04-25, arbiter ruling" and the trailing `[^*]*` captures the multi-sentence body up to the closing italic marker.

- **PR-referenced Origin stripping** (script L55-61): Pattern 3 (`\*Origin: PR #\d+ \([^)]*\)[^*]*\*\n+`) correctly strips the Origin notes for XXII (`PR #11 (mcp_server.py missing from wheel), PR #13...`), XXIII (`PR #5 (claude-code tool-use response), PR #6...`), XXIV (`PR #10 (red-blue contract break → false-PASS)...`), XXV (`PR #8 introduced @pytest.mark.live...` — note: this one may not match because it lacks the `\([^)]*\)` structure), XXVI (`PR #12 introduced the meta-test pattern...`), and XXVII (`PR #14 (CONVERSUS_DISABLED_TOOLS).*`). Origins referencing spec numbers rather than PR numbers (e.g., `*Origin: spec 005 — ...`) correctly survive because they don't match the `PR #` anchor.

- **Footer anonymization** (script L81-85): Step 4's regex correctly targets `**Version**: 3.1.3 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-05-01` and replaces it with `**Version**: (under review) | **Ratified**: 2026-03-20`, removing both the version number and the last-amended date while preserving the ratification date.

- **Leakage check for version string** (script L89-96): After Steps 1 and 4, "v3.1.3" and "3.1.3" have zero remaining occurrences in the document when `--date` is not provided. The string "3.1.3" appears only in the first SIR block (removed by Step 1) and the footer (anonymized by Step 4). No prior SIR references "3.1.3" because they predate it. The leakage check correctly PASSES for version-only verification.

---

### Missed Opportunities

- **Date leakage in un-stripped prior SIRs**: The script only strips the FIRST `<!-- Sync Impact Report ... -->` block (using `count=1`). The six preserved "prior" SIR blocks (v3.1.2, v3.1.1, v3.1.0, v3.0.0, v2.6.0, v2.5.0) all contain the line `Governance log entry: 2026-05-01 in CONSTITUTIONAL_CONVERSATIONS.md`. When the script is run with `--date 2026-05-01` against the current v3.1.3 constitution, `verify_zero_leakage` finds at least five matches of "2026-05-01" in the un-stripped prior SIRs and exits with code 1. The script that is meant to PRODUCE a blind-review artifact instead prevents its own output from being written. No mechanism exists to suppress this self-blocking. Impact: **high** — any operator who follows the docstring's usage example and passes `--date 2026-05-01` (the correct date for all v3.1.x amendments) cannot produce a stripped output file at all.

- **No prior-SIR date exclusion in leakage check**: `verify_zero_leakage` at script L89-96 scans the entire raw stripped text for the date needle, including HTML comment blocks. The prior SIRs are HTML comments and invisible in rendered markdown, but the leakage check operates on raw text. A targeted fix would be to exclude HTML comment content from the leakage scan when checking the `--date` needle, since those blocks are audit-trail artifacts whose dates are expected to be present. The version-string check should remain document-wide. Impact: **high** — this unblocks the usability issue above.

- **Dead code: arbiter-ruling substitutions** (script L68-78): The two substitutions `The \d{4}-\d{2}-\d{2} deliberation arbiter explicitly extended this scope to\s+` and `The \d{4}-\d{2}-\d{2} deliberation arbiter ruled[^.]*\.` target sentences that existed in the normative body of the constitution BEFORE v3.1.0. Cycle 2B (v3.1.0) moved those sentences from the normative body into Amendment record blocks. Step 3b's Amendment record regex now consumes those blocks before these substitutions run, leaving the substitutions with nothing to match on any post-v3.1.0 constitution. They are harmless but represent undocumented technical debt that a future maintainer would waste time understanding. Impact: **low** — no functional impact, but a comment documenting "these substitutions target pre-v3.1.0 body text; Amendment record stripping has subsumed them for post-v3.1.0 constitutions" would prevent confusion.

- **XXV Origin note may survive Pattern 3**: The XXV Origin reads `*Origin: PR #8 introduced @pytest.mark.live without codifying the discipline.*`. Pattern 3 is `\*Origin: PR #\d+ \([^)]*\)[^*]*\*\n+`, which requires a parenthetical immediately following the PR number. `PR #8 introduced` has no parenthetical, so Pattern 3 does not match. Pattern 1 (`\*Origin: PR #[\d, #]+\.[^*]*\*\n+`) requires digits/commas/#/spaces then a literal `.`; the text has `PR #8 introduced` which doesn't match after `#8`. Pattern 2 (`\*Origin: PR #[\d, #]+ introduced[^*]*\*\n+`) matches `PR #8 introduced @pytest.mark.live without codifying the discipline.` — so Pattern 2 DOES handle this case. Confirmed match; but this was non-obvious and warranted tracing. Impact: **low** — strip works, but the three-pattern design is not obviously complete without case-by-case analysis.

- **XIX sub-headings expose structural amendment history**: The `#### Architectural invariants` and `#### Operational constants` sub-headings added in v3.1.1 remain in the stripped output because no step targets them. A sophisticated blind reviewer would notice that XIX has organized sub-headings while other comparable list-heavy principles (like XXVIII) do not, suggesting recent structural reorganization. This is a minor information leak about amendment recency. Impact: **low** — does not reveal the specific content of any amendment, but does suggest the constitution has been actively structurally organized.

- **Prior SIR blocks expose amendment history to raw-markdown readers**: A blind reviewer reading the raw markdown (rather than rendered output) can see all 10+ prior SIR HTML comment blocks. These reveal the full amendment lineage (v2.2.0 through v3.1.3), recent governance dates (all 2026-05-01), and the specific principles modified in each cycle. The spec 067 strip recipe as implemented by this script does not address this exposure. This is by design (the script preserves audit trail), but there is no documentation explaining to blind verification operators whether reviewers should or should not see this content. Impact: **medium** — depends entirely on how blind verification is operationalized (raw file vs. rendered view).

- **No test coverage for any strip step**: The script has no corresponding test file anywhere in the repository (`engine/tests/`, `scripts/tests/`, or otherwise). Every regex that implements spec 067 §4.2 is exercised only by manual invocation. The v3.1.x format hazards (Amendment records, sub-headings, bullet splits) are tested only by PR #103's "unit-tested it on a sample" claim, which is apparently a manual trace, not an automated test. Impact: **high** — any future strip-script modification could introduce regressions affecting blind verification validity without any automated detection.

---

### Off-Base Assumptions

- **"Verify zero leakage" validates the full stripped document uniformly**: The prompt describes `verify_zero_leakage` as checking "zero leakage of the candidate version string" (script docstring, L27-28), implying the check applies uniformly to all text in the stripped output. This assumption is correct for the version string (which correctly reaches zero after Steps 1 and 4). But for the date parameter, applying it uniformly to raw text breaks on the prior SIR blocks, which are HTML comments containing the same date. The function treats raw text and comment blocks identically, but only the non-comment portion of the document is semantically "stripped." No wrong assumption is being made in the script design per se — the function does what it says — but the docstring's framing that passing `--date` "verifies" zero leakage creates a false expectation that the check is valid for the current constitution. Operators reading the usage example would reasonably pass `--date 2026-05-01` and then assume a code-1 exit means stripping failed, when in fact the stripping is correct and only the check is miscalibrated.

- **CONSTITUTIONAL_CONVERSATIONS.md is not in scope for stripping**: The strip script only processes `CONSTITUTION.md`. The prompt question asks whether this scope is appropriate. It is. `CONSTITUTIONAL_CONVERSATIONS.md` is a governance log, not a constitutional document, and spec 067's blind verification methodology (per the script's implementation of it) provides the reviewer only with `CONSTITUTION.md`. The stripping recipe is not responsible for sanitizing the governance log because the governance log is not part of the blind verification package. Confirmed appropriate.

---

### Actionable Recommendations

1. **Exclude HTML comment blocks from date leakage check** (Priority: P1)
   - **Current state**: `verify_zero_leakage` scans `stripped` raw text for the `--date` needle (script L89-96). The prior SIR HTML comment blocks contain "Governance log entry: 2026-05-01" in at least five places. Running `--date 2026-05-01` exits code 1 with leakage detected, blocking output file creation.
   - **Proposed change**: When checking the `date` needle, strip HTML comment blocks from the leakage scan scope. Version strings should still be checked document-wide. One approach: `comment_stripped = re.sub(r'<!--.*?-->', '', stripped, flags=re.DOTALL)` and check `date` against `comment_stripped` rather than `stripped`.
   - **Rationale**: The prior SIR blocks are audit trail, not constitutional content. Their dates are intentionally preserved by the script's design. The leakage check for dates is meant to catch date leakage in normative or visible content, not in preserved HTML comments.
   - **Risk if ignored**: Operators following the docstring usage example with `--date 2026-05-01` cannot produce a stripped output file for the current v3.1.3 constitution. The blind verification workflow is blocked for the entire v3.1.x amendment cycle.

2. **Add `scripts/tests/test_strip_constitution.py`** (Priority: P1)
   - **Current state**: No automated tests exist for the strip script. The v3.1.x format hazards are covered only by manual trace (per PR #103's description: "only unit-tested it on a sample").
   - **Proposed change**: Create `scripts/tests/test_strip_constitution.py` (or `tests/test_strip_constitution.py` if a root-level test directory is preferred) with the following minimum test set:
     1. Test that the first SIR block (version header pattern) is removed.
     2. Test that Amendment record blocks matching `*Amendment record (DATE, LABEL): BODY.*` are stripped.
     3. Test that `**Extension (vX.Y.Z):**` is rewritten to `**Extension:**`.
     4. Test that `(vX.Y.Z)` in-body markers are stripped.
     5. Test that PR-referenced Origin notes (`*Origin: PR #N (label) ...*`) are stripped.
     6. Test that spec-referenced Origin notes (`*Origin: spec 005 — ...`) survive.
     7. Test that the version footer is anonymized correctly.
     8. Test that `verify_zero_leakage` returns empty list when no leakage exists.
     9. Test that `verify_zero_leakage` with `--date 2026-05-01` produces false positives against a document containing prior SIRs (documents the known limitation until Rec 1 is applied).
     10. Integration test: run `strip_constitution` on a fixture derived from the actual `CONSTITUTION.md` and assert Amendment records are absent, footer is anonymized, and "3.1.3" is absent.
   - **Rationale**: Each regex in the strip pipeline handles a distinct format feature. Without tests, any future modification risks breaking an existing step silently.
   - **Risk if ignored**: Next time the script is modified (e.g., to add a new step for v3.2.x format hazards), existing steps may regress without detection.

3. **Document dead code in arbiter-ruling substitutions** (Priority: P2)
   - **Current state**: Steps at script L68-78 substitute "The YYYY-MM-DD deliberation arbiter explicitly extended this scope to" and "The YYYY-MM-DD deliberation arbiter ruled..." in the normative body. These sentences no longer appear in the normative body of any post-v3.1.0 constitution (they were moved to Amendment record blocks in cycle 2B and are now consumed by Step 3b's regex).
   - **Proposed change**: Add a comment above these two substitutions: `# These substitutions target pre-v3.1.0 body text where arbiter rulings appeared in normative paragraphs. Since v3.1.0 cycle 2B, arbiter rulings live in Amendment record blocks (already consumed above). These are no-ops on v3.1.x+ constitutions but retained for compatibility with older constitution versions.`
   - **Rationale**: The substitutions are not harmful, but a maintainer adding a new stripping step might not understand whether these are still load-bearing.
   - **Risk if ignored**: Future maintainer confusion; potential for accidental removal of load-bearing code that isn't actually load-bearing, or failure to remove actual dead code that should be cleaned up.

4. **Document prior SIR preservation behavior in script docstring** (Priority: P2)
   - **Current state**: The script docstring (L1-40) describes the five stripping steps but does not mention that prior `<!-- Sync Impact Report (prior — ...) -->` blocks are intentionally preserved.
   - **Proposed change**: Add to the docstring's "Stripping recipe" section: "Note: prior amendment SIR blocks (labeled '-- preserved for audit trail') are NOT stripped. They are HTML comment blocks and invisible in rendered markdown. If the blind verification workflow provides reviewers with rendered output, these blocks do not affect review. If reviewers receive raw markdown, the prior SIRs expose amendment history including governance dates."
   - **Rationale**: An operator who doesn't understand this behavior will be confused when prior SIR dates appear in the leakage check output.
   - **Risk if ignored**: Operators may attempt to work around the date leakage issue by editing prior SIRs manually, breaking the audit trail.

5. **Confirm XXV Origin note pattern coverage** (Priority: P2)
   - **Current state**: Pattern 3 requires a parenthetical immediately after the PR number. XXV's Origin (`*Origin: PR #8 introduced @pytest.mark.live without codifying the discipline.*`) has no parenthetical. Pattern 2 (`PR #[\d, #]+ introduced[^*]*\*\n+`) handles it, but this coverage is non-obvious.
   - **Proposed change**: Add a test case for the Pattern 2 path: `*Origin: PR #N introduced VERB-PHRASE.*` without parenthetical. This confirms the three-pattern design covers the full Origin note surface without a gap.
   - **Rationale**: The XXV case demonstrates that the three-pattern design requires specific pattern combinations that are not obvious from reading them individually.
   - **Risk if ignored**: A future constitutional amendment adds an Origin note without a parenthetical and one of the other PR-pattern variants; a maintainer assumes Pattern 3 covers it and doesn't test; the Origin leaks.

6. **Verify XIX sub-heading preservation is intentional** (Priority: P3)
   - **Current state**: The `#### Architectural invariants` and `#### Operational constants` sub-headings added to Principle XIX in v3.1.1 are preserved in the stripped output. The script has no step targeting these structural labels.
   - **Proposed change**: If the blind verification process intends for reviewers NOT to see evidence of structural reorganization within XIX, add a step to strip these sub-headings: `out = re.sub(r'####\s+(Architectural invariants|Operational constants)\s*\n', '', out)`. If preservation is intentional (sub-headings are structural, not content, and don't reveal the specific amendment), document this decision in the script.
   - **Rationale**: The sub-headings are minor structural markers. Their presence tells a reviewer that XIX was recently organized into categories, but not which specific content was changed. Low risk of biasing a v3.1.1-era blind review, but worth documenting the decision explicitly.
   - **Risk if ignored**: Future blind verification for an amendment to Principle XIX's structure might inadvertently expose that the sub-heading structure was recently introduced.

7. **Add CI step to smoke-test the strip script against current CONSTITUTION.md** (Priority: P2)
   - **Current state**: `.github/workflows/evals.yml` runs pytest and promptfoo but does not include any validation of the strip script. Script regressions are detected only when a blind verification run fails.
   - **Proposed change**: Add a step to the `smoke` job in `evals.yml` that runs: `python scripts/strip-constitution-for-blind.py --input CONSTITUTION.md --output /tmp/CONSTITUTION-blind.md --version v$(python -c "import re; print(re.search(r'Version\\*\\*: ([\\d.]+)', open('CONSTITUTION.md').read()).group(1))")` and asserts exit code 0.
   - **Rationale**: The smoke tier runs on every push. A strip-script regression would be caught on the same push that introduced the CONSTITUTION.md format change.
   - **Risk if ignored**: A CONSTITUTION.md format change (e.g., a future Amendment record with a nested parenthesis in the date field) silently breaks strip-script operation and is only discovered when a blind verification run is attempted.

---

### Referenced Documentation

- `scripts/strip-constitution-for-blind.py` — full file: docstring (L1-40), `strip_constitution` function (L43-87), `verify_zero_leakage` function (L89-96), `main` function (L99-130)
- `CONSTITUTION.md` — Principle XXIV (Amendment record block), Principle XXV (Amendment record block and Origin note), Principle XXVI (Origin note), Principle XXVII (Amendment record block), Principle XIX (sub-headings section), Principle II (stable interfaces enumeration), Governance § Principle Number Stability, Governance § Removal checklist, Version footer, all SIR HTML comment blocks (leading through v2.3.0)
- `specs/061-engine-eval-suite.md` — §5 (Known Gaps table), §7 (Implementation Order steps 9 and 14)
- `.github/workflows/evals.yml` — `smoke` job definition