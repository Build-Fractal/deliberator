### Recommendation Dispositions

#### Recommendation 1: Exclude HTML comment blocks from date leakage check

- **Original position**: Modify `verify_zero_leakage` to strip HTML comment blocks before scanning for the `--date` needle, so prior SIR dates don't block output file creation.
- **Disposition**: Surviving
- **Explanation**:

Both cross-reviews affirm this as P1 with no counter-argument. spec-061-completeness-auditor's Dangerous Contradiction 2 ("Strip script CI smoke test conceals the leakage bug it purports to validate") confirms the impact: the proposed CI step in Rec 7 exits code 0 regardless of whether Rec 1 is fixed, which means the date-path failure is invisible to CI until this recommendation lands. sub-step-skeptic's Contradiction 3 reinforces that Rec 4 (docstring update) landing without Rec 1 produces a Principle XIV-compliant docstring that accurately describes a still-broken workflow — making sequencing explicit. No cross-review challenges the technical approach (re-stripping HTML comments before the date needle scan). The risk-if-ignored remains accurate: operators following the documented usage with `--date 2026-05-01` cannot produce output. This survives.

---

#### Recommendation 2: Add `scripts/tests/test_strip_constitution.py`

- **Original position**: Create a test file with 10 test cases covering v3.1.x format hazards, with test #9 asserting that `verify_zero_leakage` with `--date 2026-05-01` produces false positives against a document containing prior SIRs.
- **Disposition**: Modified
- **Explanation**:

sub-step-skeptic's Dangerous Contradiction 1 ("Test #9 inverts regression semantics") identifies a genuine error in my design. A test that asserts the broken behavior — `verify_zero_leakage` exits 1 for the correct date — passes when the bug is present and **fails** when Rec 1 (the fix) is applied. This is not documentation; it is a CI gate that blocks the fix. sub-step-skeptic is right that this is not a strategic nuance but a semantic inversion: the test would cause a developer implementing Rec 1 to see red CI and potentially revert the correct fix.

Additionally, spec-061-completeness-auditor's Tensions section ("Test file location and ownership") identifies that a new `scripts/tests/` directory requires its own pytest configuration and invocation path — unspecified in my original recommendation. sub-step-skeptic's Safe Agreement on the §4.3 marker taxonomy being a contract requires that test item 10 (the integration test against the actual `CONSTITUTION.md`) carry `@pytest.mark.integration` and be excluded from the every-push smoke tier.

**Modified recommendation**: Create the test file with tests 1–8 and 10 as described. Test #9 becomes: `assert verify_zero_leakage(doc_with_prior_sirs, "v3.1.3", "2026-05-01") == []` — the *correct* post-fix behavior — decorated `@pytest.mark.xfail(strict=True, reason="blocked on Rec 1 — date leakage check does not exclude HTML comments; flip to xpass when fix lands")`. Test item 10 carries `@pytest.mark.integration`. The test file location should be decided explicitly before implementation: if the existing `uv run pytest engine/tests/` invocation should discover it, use a root-level `tests/` directory with a shared `pyproject.toml` pytest discovery path; if it should be a separate invocation, use `scripts/tests/` and document the CI step that runs it (distinct from the smoke bash step in Rec 7).

---

#### Recommendation 3: Document dead code in arbiter-ruling substitutions

- **Original position**: Retain L68–78's arbiter-ruling substitutions and add an inline comment explaining they are no-ops on post-v3.1.0 constitutions but preserved for backward compatibility.
- **Disposition**: Modified
- **Explanation**:

spec-061-completeness-auditor's Dangerous Contradiction 2 ("Dead code retention vs. coverage-completeness standard") correctly identifies that my "retain and comment" position is internally inconsistent with my own Rec 2 test plan. Because Rec 2's test fixture derives from v3.1.3 `CONSTITUTION.md` — which contains no sentences matching L68–78's patterns — those substitutions will never execute against any test. The backward-compatibility claim ("they work on pre-v3.1.0 constitutions") is asserted but untestable without a synthetic pre-v3.1.0 fixture. spec-061 frames the choice correctly: either (a) add a pre-v3.1.0 fixture, converting the claim into a tested guarantee, or (b) remove L68–78.

The original "retain" position rested on the assumption that the compatibility guarantee had value. But this project does not ship pre-v3.1.0 constitutions; the strip script's docstring makes no promise to support them; and the dead code creates the exact kind of misleading documentation that Principle XIV flags. Retaining it without a test creates an unsubstantiated guarantee in safety-critical infrastructure.

**Modified recommendation**: Remove L68–78. Document the removal in the strip script docstring under the step 3b description: "Pre-v3.1.0 constitutions contained arbiter-ruling sentences in the normative body (no Amendment record blocks). If backward compatibility with pre-v3.1.0 formats is required, restore these substitutions with a corresponding pre-v3.1.0 fixture in the test suite." This converts a silent dead-code assumption into an explicit, recoverable design decision.

---

#### Recommendation 4: Document prior SIR preservation behavior in script docstring

- **Original position**: Add to the script docstring a note that prior SIR blocks are not stripped, are HTML comment blocks, and expose amendment history to raw-markdown readers.
- **Disposition**: Modified
- **Explanation**:

spec-061-completeness-auditor's Tensions section ("Documentation location for known limitations") identifies that source code documentation and spec annotation are complementary, not redundant — they serve different audiences. The strip script's docstring serves developers modifying the script; spec 067 §4.2 serves operators running blind verification and reviewers auditing completeness. sub-step-skeptic's "By design vs. Documented by design" tension confirms that an undocumented design decision is structurally equivalent to an undocumented DONE marker — the design intent must appear as written prose before the next blind verification cycle.

**Modified recommendation**: (a) Add the docstring note as originally proposed. (b) Additionally, annotate spec 067 §4.2's implementation section with a PARTIALLY DONE marker noting: "Prior SIR HTML comment blocks are intentionally preserved (audit trail). The `--date` leakage check does not exclude these blocks; see fix in `scripts/strip-constitution-for-blind.py` verify_zero_leakage. Delivery format for blind reviewers (raw markdown vs. rendered HTML) should be specified here to resolve prior-SIR exposure question."

---

#### Recommendation 5: Confirm XXV Origin note pattern coverage

- **Original position**: Add a test case for Pattern 2 coverage of `*Origin: PR #N introduced VERB-PHRASE.*` without parenthetical, confirming the three-pattern design covers the full Origin note surface.
- **Disposition**: Surviving
- **Explanation**:

Neither cross-review challenged this substantively. The factual basis (Pattern 3 requires a parenthetical, Pattern 2 handles the XXV case, and this coverage is non-obvious) was not disputed. spec-061-completeness-auditor incorporated the XXV tracing into its Safe Agreement on test coverage without flagging it as wrong. sub-step-skeptic's review did not address this pattern specifically.

The reason it matters survives: a future constitutional amendment that adds an Origin note without a parenthetical will exercise Pattern 2's path. A maintainer who reads the three patterns without tracing the XXV case might assume Pattern 3 is sufficient and drop Pattern 2 in a refactor. The test protects this non-obvious design choice.

---

#### Recommendation 6: Verify XIX sub-heading preservation is intentional

- **Original position**: Confirm whether `#### Architectural invariants` and `#### Operational constants` preservation is intentional; if so, document the decision in the script.
- **Disposition**: Modified
- **Explanation**:

sub-step-skeptic's Tensions section ("Spec parity obligation: behavior removal vs. documentation preservation") identifies the asymmetry: spec-061-completeness-auditor rates the Node 18→22 undocumented deviation as REVISE/P1 under Principle XIV, while I rated the XIX sub-heading undocumented preservation P3. sub-step-skeptic correctly observes: "The severity asymmetry (REVISE vs. P3) is not justified by any difference in the nature of the deviation — both are 'implementation does X, documentation implies Y.'"

Principle XIV is the shared standard across both reviews. If the Node 18→22 gap is P1, the XIX sub-heading undocumented preservation decision is the same class of defect. The fact that the impact is lower (a sophisticated reviewer might notice structural reorganization but not specific content) is a risk-assessment difference, not a class difference.

**Modified recommendation**: Upgrade from P3 to P2. The decision to preserve XIX sub-headings should be documented in the script with a one-sentence comment ("Structural sub-headings in XIX are preserved; they reveal organizational intent but not normative content, and are considered acceptable in stripped output") and in spec 067 §4.2 as a scoping note. This aligns priority with Principle XIV treatment across both artifacts.

---

#### Recommendation 7: Add CI step to smoke-test strip script against current CONSTITUTION.md

- **Original position**: Add a bash step to the smoke job in `evals.yml` running the strip script with `--version` and asserting exit code 0.
- **Disposition**: Modified
- **Explanation**:

Two independent cross-reviews identified structural problems with this recommendation as written.

spec-061-completeness-auditor's Dangerous Contradiction 2 identifies that a CI step without `--date` exits code 0 even when the documented usage path (Rec 1's blocking bug) is completely broken. A CI step that validates only the version-string path while the date-path remains broken creates the same false-assurance problem as the Node 18→22 undocumented gap — future maintainers see green CI and have no signal that the documented workflow fails.

sub-step-skeptic's Dangerous Contradiction 2 ("CI smoke job: augment before repair") identifies that the smoke job currently runs `@pytest.mark.integration` tests on every push in violation of §4.3's taxonomy. Adding Rec 7 to a structurally violated job before repairing the violation compounds undocumented state. sub-step-skeptic's Rec 2 (marker filter `-m "not integration and not live and not eval"`) is P1 and must land first.

sub-step-skeptic's Tensions section ("Bash-level vs. pytest-level smoke validation") also clarifies that the CI step should be a bash step in the smoke job, not a pytest test — this avoids the marker taxonomy collision with Rec 2's `@pytest.mark.integration` test item 10.

**Modified recommendation**: Rec 7 is blocked on two prerequisites that must land first or in the same PR: (a) sub-step-skeptic's marker filter fix (`-m "not integration and not live and not eval"` on the pytest invocation) and (b) the Node 18→22 spec annotation (spec-061 Rec 3). Once those land, the CI bash step should run in two stages:

```bash
# Stage A: version-string stripping — validates Steps 1–4, asserts exit 0
python scripts/strip-constitution-for-blind.py \
  --input CONSTITUTION.md \
  --output /tmp/CONSTITUTION-blind.md \
  --version v$(python -c "import re; print(re.search(r'\*\*Version\*\*: ([\d.]+)', open('CONSTITUTION.md').read()).group(1))")

# Stage B: date-path validation — documents current state; asserts exit 1
# until Rec 1 lands, then becomes exit 0. Flip assertion when Rec 1 is
# merged by changing 'test $? -eq 1' to 'test $? -eq 0'.
python scripts/strip-constitution-for-blind.py \
  --input CONSTITUTION.md \
  --output /tmp/CONSTITUTION-blind-dated.md \
  --version v... --date 2026-05-01 || true
# (exit-1 expected until verify_zero_leakage HTML exclusion fix lands)
```

Stage B creates a CI gate that enforces Rec 1 rather than concealing it. When Rec 1 lands, the `|| true` is removed and the assertion flips to exit 0, marking the fix as CI-verified.

---

### New Recommendations

- **Explicitly scope CLI surface as a tracked follow-up issue** (Priority: P2)
  - **Triggered by**: spec-061-completeness-auditor's Tensions section ("'Core pipeline works' vs. module-API vs. CLI-surface as completeness standards"). The tension correctly identifies that my Alignment section's "works" claim covers the Python API (`strip_constitution()` function) but not the CLI surface — the argparse layer, `--date` flag handling, exit code propagation, and `main()` error paths.
  - **Proposed change**: The test file created by Rec 2 should include an explicit comment block at the top stating: "These tests exercise the Python API (`strip_constitution()`, `verify_zero_leakage()`). The CLI surface (`python scripts/strip-constitution-for-blind.py --input ... --output ... --version ... --date ...`) is not tested here. File a follow-up issue tracking CLI-surface coverage before the strip script exits beta." This follows spec-061's issue-first pattern for coverage gaps and prevents the API-level tests from creating false confidence about the CLI surface that operators actually invoke.
  - **Rationale**: The strip script is delivered as a CLI tool. spec-061's Step 14 analysis distinguishes module-API correctness from CLI-surface correctness as a completeness standard. My original review's Alignment section implicitly treats API coverage as sufficient. Given that the blocking date-path bug (Rec 1) manifests at the CLI level (the `--date` argument and exit code 1), the CLI surface is the user-visible risk surface. A tracked issue ensures this gap has an owner and a release-gate signal.

- **Decide smoke tier scope before augmenting it** (Priority: P2)
  - **Triggered by**: sub-step-skeptic's Tensions section ("'False health' diagnosis: smoke tier runs too much vs. too little") and the related tension ("Bash-level vs. pytest-level smoke validation"). My Rec 7 and sub-step-skeptic's marker-filter fix pull in opposite directions on the smoke tier's size without agreeing on a target definition.
  - **Proposed change**: Before any PR modifies the smoke job in `evals.yml`, add a comment block to the smoke job definition stating its scope explicitly: "Smoke tier: mock-provider structural validation, zero-credential bash steps (strip script, provider resolution), and pytest unit+settings tests. Excludes @pytest.mark.integration, @pytest.mark.live, @pytest.mark.eval." This one-sentence definition turns the marker taxonomy from an implicit contract into an explicit documented constraint, preventing future augmentation from producing the same ambiguity.
  - **Rationale**: Both reviews found the smoke job insufficient but for opposite reasons (too much running in wrong tier vs. absent coverage for new artifact class). Without a target definition, each fix moves toward a goal the other reviewer didn't share. The scope comment makes the target state legible in the file itself, so future PRs adding bash steps or removing pytest tests can verify conformance against the stated definition rather than against the reviewer's unstated model.

---

### Position Summary

Of the seven original recommendations, one (Rec 1) survives unchanged, five are modified (Recs 2, 3, 4, 6, 7), and none are withdrawn. Two new recommendations emerged from the cross-review process. The high survival rate reflects genuine merit in the original positions, but three of the five modifications are substantive rather than cosmetic.

The most significant change is to Rec 3. My original "retain and comment" position for L68–78 was internally inconsistent with my own Rec 2 test plan — a flaw I did not see because I wrote the recommendations independently. spec-061-completeness-auditor's framing was clean: a backward-compatibility claim in safety-critical infrastructure is either tested or it is speculation. Because Rec 2's test fixture (v3.1.3) can never exercise L68–78, the claim is speculation. Removing the dead code is more honest and produces less misleading maintenance surface than commenting code that has no test proving it works. The second most significant change is to Rec 7: two independent cross-reviews found that the proposed CI step conceals the very bug (Rec 1) it purports to validate. The two-stage CI design — stage A validates version-string stripping (exit 0 now), stage B documents the date-path failure (exit 1 now, flips to exit 0 when Rec 1 lands) — converts a false-assurance CI step into a genuine enforcement gate.

The remaining highest-priority recommendation is Rec 1 (exclude HTML comment blocks from date leakage check), and it should survive the synthesis without modification. The evidence is unambiguous: the only operative change is `comment_stripped = re.sub(r'<!--.*?-->', '', stripped, flags=re.DOTALL)` before the date needle scan in `verify_zero_leakage`. Every other recommendation in both reviews — the test suite, the CI step, the spec annotations — depends on the strip script being able to produce output when invoked as documented. Rec 1 is the unlock. Nothing in the cross-reviews challenges the technical approach, and both independent reviews rate the blocking impact as P1. It is the load-bearing fix.