I'll read the synthesis and dispute documents before writing the arbitration resolution.

Now let me read the Phase 4 dispute documents.

I now have all the information needed. Let me write the arbitration resolution.

### Process Note

This arbitration was triggered by the `always` condition — the conversus configuration mandates subject arbitration for this deliberation regardless of whether disputes remained unresolved at Phase 5. Five disputes survived Phase 4 into the synthesis, all identified in the synthesis's "Remaining Disputes" section. Three agents participated in this cooperative deliberation: script-end-to-end-tester, spec-061-completeness-auditor, and sub-step-skeptic. The deliberation mode is **cooperative**, meaning agents were tasked with adversarial review but sought resolution rather than victory; this arbitration resolves the five points where that resolution was not achieved.

---

### Decision Framework

The following principles from the grounding document (`specs/061-engine-eval-suite.md`) are the operative framework for these rulings. All binding decisions below trace to at least one of these principles.

- **[SC6 — CI Smoke Coverage]**: "Eval suite runs in CI — smoke tests on every push, quality evals on release tags" (spec 061 §6, success criterion 6). This establishes that the eval suite's health is measured against CI signal on every push. Gaps in CI coverage are gaps in the success criterion, not merely inconveniences.

- **[SC5 — Known Gaps Resolved with Regression Tests]**: "Known gaps G1, G3/G11, G6 resolved and covered by regression tests" (spec 061 §6, success criterion 5). The operative standard is that fixes require regression tests — documentation of known-broken states is an incomplete fix, but CI coverage (even with a documented-failure signal) is superior to no CI coverage.

- **[§4.3 — Marker Taxonomy Contract]**: "The permitted markers for cost-bearing tests are `live`, `integration`, and `security`... the taxonomy is the contract" (spec 061 §4.3). This makes marker governance a non-negotiable contractual obligation, not an advisory recommendation. Any CI step that runs integration-marked tests in the smoke tier violates this contract.

- **[§7 — Sequential Implementation Order with DONE Markers]**: Steps are presented as a sequenced queue with explicit DONE markers (spec 061 §7). These markers communicate the project's actual state to future contributors. An inaccurate DONE marker is a first-class spec defect, not an annotation style preference.

- **[§3.1.9 — Explicitly Required Test Scenarios]**: Section 3.1.9 specifies the multi-round, arbiter, and iteration test scenarios with explicit priority labels (P0, P1). A step 13 DONE marker that does not cover P1 scenarios from §3.1.9 is an overclaimed marker. The spec, not the annotation, defines what step 13 requires.

- **[§3.1.2 — Provider Matrix Test Taxonomy]**: "Test each provider at the appropriate level" with five defined tiers (spec 061 §3.1.2). This establishes that test coverage means covering the declared matrix, not a subset of it.

- **[§2.2 — Composability Contract]**: "Every consumer must be able to configure" the seven listed axes (spec 061 §2.2). This composability contract is the normative basis for requiring cross-surface parity tests — SC3 is not an aspirational goal but a derivation from the composability contract.

---

### Binding Decisions

#### Dispute: Stage B CI bash step timing — documented failure state vs. false-health concern

**Positions:**
- **script-end-to-end-tester**: Stage B (`|| true` with inline `echo "KNOWN BUG..."` banner) should land in the coordinated PR alongside the marker filter fix, before Rec 1 is merged. A `|| true` step with an explicit comment is materially different from an implicitly passing step; it documents the expected failure state and creates a concrete flippoint when Rec 1 lands (script-end-to-end-tester, Phase 4 disputes.md, Dispute §1).
- **sub-step-skeptic**: Stage B with `|| true` should not land until Rec 1 is merged. The false-health concern is about the CI step appearing in a list of "passing" steps regardless of annotation; a "4 passing steps" display while the date-path is broken misrepresents tool health and dilutes urgency (sub-step-skeptic, Phase 4 disputes.md, Dispute §2).

**Synthesizer's assessment:** script-end-to-end-tester's position is stronger on the operational merits. The `|| true` + KNOWN BUG banner is self-liquidating; sub-step-skeptic's sequencing leaves the date-path wholly uncovered for an unknown duration. The synthesizer recommends Stage B land with a strengthened step name that appears in the CI interface, not just the log.

**Ruling:** Adopt script-end-to-end-tester's Stage B design with the synthesizer's strengthened step-name requirement: Stage B lands in the coordinated PR alongside Stage A and the marker filter fix, with the CI step named `"Strip script date-path (KNOWN BUG: exits 1 until HTML-comment exclusion fix lands)"`.

**Grounding citation:** SC6 (spec 061 §6): "smoke tests on every push." The choice is not between documented-failure coverage and correct coverage; it is between documented-failure coverage and no date-path CI coverage at all. SC6 requires CI signal on every push. "No CI coverage" for the date-path fails SC6 more severely than "documented-failure CI coverage" for the date-path. The `|| true` + step-name design is a partial SC6 satisfaction; silence is a complete SC6 miss for this code path.

**Rationale:** sub-step-skeptic's false-health concern is real and deserves a direct response. The concern is that the CI interface shows a "passing step" count that includes Stage B. The synthesizer's step-name recommendation resolves this: the step name `"Strip script date-path (KNOWN BUG: exits 1 until HTML-comment exclusion fix lands)"` appears in the GitHub Actions step list, not only in run logs, making the known-failure state visible to anyone looking at the CI job summary — not only someone reading log output. This is materially different from an implicitly passing step, and it directly addresses the mechanism sub-step-skeptic identified (a passing-step count that misrepresents health). The self-liquidating property of `|| true` — that removing it when Rec 1 lands converts the step into an enforcement gate — is the correct design for a pre-fix CI signal.

**Rejected position:** sub-step-skeptic's sequencing requirement (wait for Rec 1) is rejected. sub-step-skeptic's strongest argument is that a P1 bug should not have a CI step that "passes." This argument is correct in the abstract but ignores the alternative: leaving the date-path wholly absent from CI is a worse state for SC6 than having a documented-failure signal. The urgency signal that sub-step-skeptic wants to preserve is actually better served by a `KNOWN BUG` step that is visibly unresolved in every CI run than by silence, which communicates nothing about the date-path's health at all.

**Required changes:** In `evals.yml`, Stage B of the two-stage CI bash step for the strip script (added in the same PR as Stage A and the Rec 17 marker filter) must use the YAML step-name field `name: "Strip script date-path (KNOWN BUG: exits 1 until HTML-comment exclusion fix lands)"` and include `|| true` with an inline comment `# expected exit 1 until verify_zero_leakage HTML-comment exclusion fix (Rec 1) lands`. When Rec 1 lands, the same PR removes `|| true` and updates the step name to `"Strip script date-path validation"`.

---

#### Dispute: Strip script test file location as prerequisite decision

**Positions:**
- **script-end-to-end-tester**: Defers the concrete file location decision but recommends `engine/tests/test_strip_constitution.py` as compatible with the existing CI discovery path; states the decision must be made explicitly before implementation but does not mandate it as a blocking prerequisite now (script-end-to-end-tester, Phase 4 disputes.md, Dispute §2).
- **sub-step-skeptic**: The location decision is a mandatory prerequisite to Rec 2 being considered complete — not a concurrent deferral — because the location has marker-taxonomy governance consequences that affect the scope of Rec 17's `-m` filter (sub-step-skeptic, Phase 4 disputes.md, Dispute §2).

**Synthesizer's assessment:** sub-step-skeptic's position is stronger on the operational consequence. A test that CI doesn't discover is worse than no test because it creates false coverage. `engine/tests/test_strip_constitution.py` satisfies both agents' constraints simultaneously and is the concrete recommendation.

**Ruling:** The test file location is `engine/tests/test_strip_constitution.py`; this is a binding prerequisite to Rec 2 implementation, not a concurrent deferral. No implementation of Rec 2 proceeds without the test file being placed at this path.

**Grounding citation:** §4.3 marker taxonomy contract (spec 061 §4.3): "the taxonomy is the contract." The marker filter (`-m "not integration and not live and not eval"`) applies specifically to `uv run pytest engine/tests/`. A test file placed outside this directory escapes the §4.3 contract entirely. sub-step-skeptic is correct that this is a governance consequence, not merely an organizational preference. The contract is binding on both the filter's scope and the test file's location.

**Rationale:** The positions are substantively aligned on the outcome (`engine/tests/`); the dispute is whether the decision is a prerequisite or a concurrent deferral. sub-step-skeptic is correct that it must be resolved before implementation because test placement at a non-discovered location produces false coverage — a problem worse than no test (it signals coverage where none exists). script-end-to-end-tester's formulation ("should be decided explicitly before implementation") reaches the same conclusion but with softer procedural framing that could be read as permissive. The `engine/tests/` answer satisfies both agents' constraints: it reuses the existing CI discovery path, and `@pytest.mark.integration` on item 10 is excluded from smoke by Rec 17's filter.

**Rejected position:** script-end-to-end-tester's "deferral to implementation PR" framing is rejected as the procedural framing (though not the substantive outcome). The specific concern is that "defer the decision to the PR" creates a gap where the decision is not recorded until a contributor opens the PR — at which point a path outside `engine/tests/` could be chosen without awareness of the governance consequence. Recording the decision here, as a synthesis output, eliminates that gap.

**Required changes:** In `specs/061-engine-eval-suite.md`, the step implementing Rec 2 must specify `engine/tests/test_strip_constitution.py` as the file location. The CI smoke job already discovers this path. No new CI step is required. If a future smoke tier architecture decision (New Rec B / Rec 26) relocates tests, that relocation requires an explicit new CI discovery step documented in `evals.yml` before any file is moved.

---

#### Dispute: Step 10 annotation correction timing — standalone PR vs. bundled with CI changes

**Positions:**
- **spec-061-completeness-auditor**: Both corrections (Node 18→22 and PR attribution) must land in a standalone PR immediately, without waiting for future evals.yml changes. Making a Principle XIV correction wait for CI coordination introduces indefinite delay on a past-EOL security exposure (spec-061-completeness-auditor, Phase 4 disputes.md, Dispute §1).
- **sub-step-skeptic**: The attribution correction should bundle with future evals.yml additions to avoid sequential DONE note corrections and ensure the note accurately names all contributing PRs when the strip script bash step (Rec 7) eventually lands (sub-step-skeptic, Phase 4 disputes.md, Dispute §6, Tension).

**Synthesizer's assessment:** spec-061-completeness-auditor's position is stronger for both corrections. The EOL date makes waiting unacceptable. The cost of a "third correction" when Rec 7 lands is low (one-line addition). Indefinite deferral of a P1 spec-parity fix to wait for CI coordination is the wrong tradeoff.

**Ruling:** Both corrections — Node 18→22 and the PR attribution correction — land together in a standalone PR immediately, without waiting for evals.yml CI changes. When the strip script bash step PR (Rec 7) eventually lands, that PR appends its PR number to the attribution record as a one-line addition.

**Grounding citation:** §7 DONE marker integrity (spec 061 §7): The DONE marker for step 10 contains two factual claims — a runner requirement ("Node 18") and a contributing PR attribution — both of which are wrong. These are not annotation style preferences; they are factual claims that contributors act on. A contributor reading step 10 today and following its runner requirements would pin `node-version: '18'`, restoring EOL behavior. This is a direct §7 implementation-state accuracy failure.

**Rationale:** The split ruling (both corrections now, attribution appended by Rec 7's PR later) resolves the genuine tension sub-step-skeptic identified. sub-step-skeptic's strongest argument is that two sequential DONE note corrections produce confusing git history. The split ruling avoids this: the standalone PR corrects the current factual errors; Rec 7's future PR appends its own attribution as a one-line addition rather than re-correcting the same note. This is not "two sequential corrections" — it is one correction PR and one append PR, which are different operations. The Node 18 EOL date (April 2025) is already past; waiting for CI coordination while contributors can introduce EOL behavior by following the spec is not acceptable under any priority framing.

**Rejected position:** sub-step-skeptic's bundling preference is rejected for the following specific reason: the bundling logic requires the attribution correction to wait for the Rec 7 bash step, which itself requires the Rec 17 marker filter to land first, which requires coordination. This creates a delivery chain with no committed timeline. The cost of an "additional append" when Rec 7 lands is one line in one file. The cost of deferring the Node 18 fix through that chain is an ongoing security exposure. The tradeoff is not symmetric.

**Required changes:** (a) Open a standalone PR immediately that edits `specs/061-engine-eval-suite.md` §7 step 10 DONE annotation to read: "Node 22 LTS (spec said Node 18 — Node 18 EOL April 2025; Principle XIV)"; attribution: "PR #83 established the smoke tier; PR #101 added the quality (Ollama) and deepeval (Anthropic) tiers and workflow_dispatch inputs." No other file needs to change in this PR. (b) When the strip script bash step PR lands, that PR's author appends the new PR number to the step 10 attribution as: "; PR #NNN added strip script bash step validation."

---

#### Dispute: §3.1.9 gap remediation delivery model — immediate implementation vs. issues-first

**Positions:**
- **spec-061-completeness-auditor**: GitHub issues AND concrete test implementations should land in the same PR for both §3.1.9 gaps; step 13 annotation updates to DONE once both implementations merge (spec-061-completeness-auditor, Phase 4 disputes.md, Dispute §2).
- **sub-step-skeptic**: Issues should be filed first, with implementations as follow-up milestone work; step 13 annotation should read DONE WITH OPEN GAPS until implementations merge. A PR that includes both issue-filing and implementation is acceptable, but the issue tracking vehicle must exist before the PR closes (sub-step-skeptic, Phase 3 New Rec A; Phase 4 convergence §4).

**Synthesizer's assessment:** The positions are compatible if GitHub issues are filed as part of the implementation PR. The remaining substantive difference — annotation state — favors spec-061-completeness-auditor: DONE WITH OPEN GAPS should not persist indefinitely. If both land in the same PR, DONE WITH OPEN GAPS is an unnecessary intermediate state.

**Ruling:** File GitHub issues AND commit test implementations in the same PR. The step 13 annotation updates in that PR to: "DONE (PR #NNN closes iterations=3 cost estimate and influence output heading gaps; see GitHub issues #X and #Y for tracking history)." DONE WITH OPEN GAPS is not used as the final annotation state when both issue and implementation land simultaneously.

**Grounding citation:** §3.1.9 (spec 061 §3.1.9, iterations and arbiter tests): The §3.1.9 matrix explicitly lists these test scenarios as P0/P1 requirements. The step 13 DONE marker claims this section is covered. An annotation that says DONE but leaves P1 §3.1.9 scenarios unimplemented is an overclaimed DONE by the spec's own standard. The correct resolution is the implementation that closes the gap — not an annotation that accurately describes a gap while deferring its closure.

**Rationale:** Both tests are fully specifiable: `TestCostEstimate` with `iterations=3` asserting `cost_estimate["cross_review"] == 6` in `test_sdk.py`; an `influence="advisory"` test in `test_phases.py TestArbitration` asserting heading differences in `arbitration/resolution.md`. Both use the mock provider, neither is blocked by G12 (per the bilateral convergence on G12 blocking scope). sub-step-skeptic's requirement — that tracking issues exist before the PR closes — is satisfied by filing them in the same PR. The only remaining disagreement is whether the annotation reads DONE or DONE WITH OPEN GAPS, and this resolves in spec-061-completeness-auditor's favor: DONE WITH OPEN GAPS as a permanent annotation state signals ongoing work where none exists if both issue and implementation land together.

**Rejected position:** sub-step-skeptic's "issues-first" delivery model is rejected for these two specific tests because the design uncertainty that justifies issues-first is absent. sub-step-skeptic's strongest argument is that issues provide owners, release-gate signals, and prioritization. These process benefits are preserved in the same-PR model: the issues are filed, they have owners (the PR author), and the implementations land before the PR closes. What sub-step-skeptic's model adds is an indefinite implementation gap after the issues are filed — which spec-061-completeness-auditor correctly identifies as unnecessary for fully-specifiable mock-provider unit tests.

**Required changes:** (a) File two GitHub issues: one for the `iterations=3` cost estimate coverage gap in `test_sdk.py TestCostEstimate`, one for the arbiter `influence="advisory"` output heading coverage gap in `test_phases.py TestArbitration`. (b) In the same PR, implement: a parametrized `TestCostEstimate` variant asserting `cost_estimate["cross_review"] == 6` for `iterations=3` in `engine/tests/test_sdk.py`; and an `influence="advisory"` test variant in `engine/tests/test_phases.py TestArbitration` that runs the pipeline and asserts heading differences in `arbitration/resolution.md`. (c) In the same PR, update step 13's DONE annotation in `specs/061-engine-eval-suite.md` §7 to: "DONE (PR #NNN closes iterations=3 cost estimate and influence output heading gaps; see GitHub issues #X and #Y for tracking history)."

---

#### Dispute: "Load-bearing fix" framing and priority ordering between strip-script Rec 1 and §7 header Rec 16

**Positions:**
- **script-end-to-end-tester**: HTML comment exclusion (Rec 1) is "the load-bearing fix" and "the unlock" — every downstream action (tests, CI, documentation) depends on the strip script being able to produce output (script-end-to-end-tester, Phase 3 revision Position Summary; Phase 4 Non-Negotiable #1).
- **sub-step-skeptic**: Both Rec 1s are co-equal P1 priorities for different audiences — HTML exclusion unblocks operators running the CLI; §7 header correction unblocks contributors reading the spec — and "global unlock" framing implicitly deprioritizes the §7 correction (sub-step-skeptic, Phase 4 disputes.md, Dispute §1).

**Synthesizer's assessment:** sub-step-skeptic's framing is correct: both are co-equal P1s for distinct audiences. script-end-to-end-tester is correct that the HTML exclusion has higher blast radius for the immediate governance workflow, but neither gates the other. "Global unlock" framing is imprecise.

**Ruling:** Both Rec 1s are co-equal P1 priorities for distinct audiences: the HTML comment exclusion is the P1 operational fix for operators who cannot produce output; the §7 progress header correction is the P1 orientational fix for contributors who cannot calibrate their work. Neither is a prerequisite for the other. The "global unlock" framing is retired.

**Grounding citation:** §7 implementation order (spec 061 §7): "Steps 1-4 are complete. Remaining work starts at step 5." The §7 header is the authoritative orientation statement for contributors implementing subsequent steps. An incorrect §7 header is not a style preference — it is a first-class spec accuracy failure that affects every contributor who reads §7 before acting. §6 SC5 ("known gaps G1, G3/G11, G6 resolved and covered by regression tests") also governs: the HTML exclusion fix is a G1-class known gap that must be resolved and covered. Both fixes satisfy independent §7 and §6 requirements; neither subsumes the other.

**Rationale:** script-end-to-end-tester's "global unlock" framing is operationally accurate for operators — they cannot produce strip-script output until Rec 1 lands. But "global unlock" implies that spec annotation fixes, tracking issues, and marker filter repairs are all gated on the HTML exclusion. This is factually false: those changes have no dependency on the strip script being functional. sub-step-skeptic correctly identifies that "global unlock" framing creates a rationalization vector: "we'll fix the spec annotations once the strip script works," which is the sequencing pattern that allowed G2 and G12 to remain open across eight DONE markers. The synthesis applies the same systemic-contradiction analysis here: priority framing that implicitly sequences independent P1 items is the root of the "verified-once culture" that both agents identified as a structural problem in this codebase.

**Rejected position:** script-end-to-end-tester's "global unlock" framing is rejected specifically because it is imprecise in a directionally consequential way. script-end-to-end-tester's strongest argument is that the HTML exclusion has higher blast radius for the immediate governance workflow (operators blocked from producing output today). This argument is correct in isolation but irrelevant to the question of whether §7 header corrections are gated on the strip script. They are not. The blast radius of the HTML exclusion fix does not make the §7 header fix a lower priority; it makes the HTML exclusion fix a higher urgency for a specific workflow. Both must land; one does not gate the other.

**Required changes:** In any communications about implementation priority and in the step 13 annotations updated by this deliberation, both fixes must be described as "co-equal P1 priorities": the HTML comment exclusion fix (P1 for operators) and the §7 progress header correction (P1 for contributors). The §7 progress header correction should land as the first documentation change in the first PR — parallel to the HTML exclusion fix, not after it.

---

### Summary of Changes Required

**P1 — Required for correctness:**

1. **HTML comment exclusion in `verify_zero_leakage`** (from Dispute: Stage B / Convergence §1): In `scripts/strip-constitution-for-blind.py`, add `comment_stripped = re.sub(r'<!--.*?-->', '', stripped, flags=re.DOTALL)` before the date needle scan; check `date` against `comment_stripped` rather than `stripped`. This is the operational P1 fix for operators. Priority: P1.

2. **Step 10 standalone annotation PR** (from Dispute: Step 10 timing): Edit `specs/061-engine-eval-suite.md` §7 step 10 DONE annotation atomically: Node 18→22 correction ("Node 22 LTS (spec said Node 18 — Node 18 EOL April 2025; Principle XIV)") + PR attribution correction ("PR #83 established the smoke tier; PR #101 added quality and deepeval tiers and workflow_dispatch inputs"). Land immediately as a standalone prose-only PR. Priority: P1.

3. **§7 progress header correction** (from Dispute: "Load-bearing fix" framing): Update `specs/061-engine-eval-suite.md` §7 header to accurately describe the current state: steps completed (1–4, 9, 10 annotation, 13 with open gaps, 14a persistence sub-item), steps open (5, 6, 7, 8, 11, 12, 14b/c), P1 open bugs (G2, G12). Land as the first documentation change, parallel to the HTML exclusion fix. Priority: P1.

4. **Stage B CI bash step in coordinated PR** (from Dispute: Stage B timing): Add Stage B to `evals.yml` smoke job in the same PR as Stage A and the Rec 17 marker filter fix. Step name: `"Strip script date-path (KNOWN BUG: exits 1 until HTML-comment exclusion fix lands)"`. Include `|| true` with inline comment naming the fix. Priority: P1 (gates CI smoke coverage for date-path).

5. **Smoke marker filter fix** (from Convergence §3): Change `uv run pytest engine/tests/ -x -q --timeout=30` to `uv run pytest engine/tests/ -x -q --timeout=30 -m "not integration and not live and not eval"` in `evals.yml` smoke job. This is an atomic prerequisite for the Stage A/B additions above. Priority: P1.

6. **§3.1.9 gap-filling test implementations + GitHub issues** (from Dispute: §3.1.9 delivery model): In a single PR: file two GitHub issues; add `TestCostEstimate` variant in `engine/tests/test_sdk.py` for `iterations=3`; add `influence="advisory"` test in `engine/tests/test_phases.py TestArbitration`; update step 13 DONE annotation in `specs/061-engine-eval-suite.md` §7. Priority: P1.

7. **Test file location declared as `engine/tests/test_strip_constitution.py`** (from Dispute: test file location): This is a binding prerequisite recorded in the deliberation record. No implementation of Rec 2 proceeds with the test file at any other location unless a new CI discovery step is explicitly added to `evals.yml` before the file is committed. Priority: P1 (governance prerequisite).

**P2 — Required for design integrity:**

8. **Step 14 verdict MATCH→REVISE with tracking infrastructure** (from Convergence §6): Update step 14 in `specs/061-engine-eval-suite.md` §7 to read REVISE, with explicit language that: persistence sub-item delivery does NOT close step 14; CI/CD exit code sub-item and combinatorial matrix sub-item require independent GitHub issues; the combinatorial matrix must have a tracking issue before step 14 can be indefinitely deferred. Priority: P2.

9. **Step 11/12 tracking issue with SC#3 consequence** (from Convergence §7): File a GitHub issue for step 11 stating step 12 is blocked and SC#3 is unreachable until step 11 lands. Update `specs/061-engine-eval-suite.md` §6 criterion 3 to read "Not achievable until step 11 lands (GitHub issue #N)." Update step 12 with BLOCKED notation. Priority: P2.

10. **Stage B → strict exit-0 assertion when Rec 1 lands** (from Dispute: Stage B / Convergence §4 xfail design): When the HTML comment exclusion fix (Rec 1 item 1 above) lands, the same PR removes `|| true` from the Stage B CI step and updates the step name to `"Strip script date-path validation"`. Priority: P2 (deferred until Rec 1 lands).

11. **Step 10 attribution append when Rec 7 lands** (from Dispute: Step 10 timing): The PR implementing the strip script bash step (Rec 7) must append its PR number to the step 10 attribution record in `specs/061-engine-eval-suite.md`. Priority: P2 (deferred until Rec 7 lands).

**P3 — Recommended improvements:**

12. **Smoke tier scope declaration in `evals.yml`** (from Convergence §12): Before step 14's matrix tests or further bash steps are added, add a comment block to `evals.yml`'s smoke job definition stating its authoritative scope. Priority: P3.

13. **§4.3 smoke tier architecture decision document** (from Convergence §12): Update `specs/061-engine-eval-suite.md` §4.3 with an explicit architecture decision on pytest markers vs. bash steps in the smoke tier. Priority: P3 (prerequisite to step 14 matrix implementation, but not blocking any P1/P2 work above).

---

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| Stage B CI bash step timing | Adopt script-end-to-end-tester's design with strengthened step name | High | SC6 clearly requires CI coverage on every push; the step-name mechanism directly addresses sub-step-skeptic's false-health mechanism concern; synthesizer agreement |
| Test file location as prerequisite | `engine/tests/test_strip_constitution.py`, binding prerequisite | High | §4.3 taxonomy contract is explicit; both agents substantively agree on the location; only procedural framing differs |
| Step 10 annotation timing | Standalone PR immediately; Rec 7 appends later | High | Node 18 EOL is a concrete past-date security exposure; the split avoids both indefinite deferral and "two sequential correction" concerns; synthesizer agrees |
| §3.1.9 delivery model | Same-PR issue + implementation; DONE annotation on merge | High | §3.1.9 is explicit; both tests are mock-provider and unblocked by G12; sub-step-skeptic's tracking-issue requirement is satisfied within the same-PR model |
| "Load-bearing fix" framing | Co-equal P1 for distinct audiences; retire "global unlock" | High | Both P1s have independent grounding (§6 SC operators; §7 contributors); "global unlock" is falsifiable (spec fixes have no strip script dependency) |

The deliberation quality is high. The five remaining disputes are all procedural or framing disagreements rather than substantive analytical conflicts — every dispute in this set has a clear factual answer once the grounding document's requirements are applied. The three-agent structure produced strong adversarial coverage: the dangerous contradiction resolutions (dead code, xfail test design, step 14 MATCH verdict) are all genuine quality improvements earned through deliberation rather than pre-existing agreement. The systemic contradiction analysis is particularly valuable — the five structural patterns identified (verified-once culture, undefined smoke tier scope, Principle XIV drift, false completion signals, priority label semantic divergence) are the load-bearing insights for future constitutional amendment cycles.

The one observation outside the dispute record: the `evals.yml` smoke job currently has no step that validates the CONSTITUTION.md file itself exists and is parseable. The strip script depends on a readable CONSTITUTION.md; a CI job that validates the strip script's output but not its input has a silent failure mode if CONSTITUTION.md is accidentally truncated or corrupted. This is not a dispute requiring resolution here, but it is worth noting as a candidate for a follow-up CI hardening step alongside the Stage A/B additions.

---

**STRIP-SCRIPT VERDICT: VALID WITH FIXES**

The script correctly executes Steps 1–4 of the stripping recipe for the version-string path. The concrete gap is in `verify_zero_leakage`: the date needle scan does not exclude HTML comment blocks, causing the script to exit code 1 whenever `--date 2026-05-01` is supplied against v3.1.3 CONSTITUTION.md (which contains "2026-05-01" in five or more prior SIR comment blocks). The fix is a single `re.sub` call (HTML comment exclusion before the date scan). Until this fix lands, operators cannot use the `--date` argument as documented. The version-string-only path (no `--date`) is functional and exercises Steps 1–4 correctly; Stage A of the CI bash step validates this path without exposing the date-path bug.

**SPEC-061-SUBSTEPS VERDICT: ACCURATE WITH FOLLOW-UP**

- **Step 9** (settings cascade + env var coercion tests): ACCURATE. The per-assertion analysis confirms substantive, non-tautological behavioral coverage. DONE marker stands.
- **Step 10** (CI workflow addition): NEEDS ANNOTATION CORRECTION. The DONE marker is not reverted to IN PROGRESS — the CI work was done — but the annotation contains two factual errors (Node 18 vs. Node 22 LTS; PR attribution miscount) that constitute Principle XIV violations. Annotation correction required per P1 binding decision above; no code revert.
- **Step 13** (multi-round, arbiter, iterations tests): DONE WITH OPEN GAPS. The iterations=3 dispatch count, naming, and events tests are present and accurate (PR #102). The arbiter trigger and multi-round tests are present and accurate (pre-existing in `test_phases.py`). Two P1 §3.1.9 rows are not covered: the `iterations=3` cost estimate assertion and the `influence="advisory"` output heading test. Step 13 annotation must be updated to reflect these open gaps with tracking issues and implementations per the P1 binding decision above.
- **Step 14a** (persistence round-trip sub-item): ACCURATE AS PARTIAL. `TestPersistListShowRoundTrip` is correctly implemented and covers the persist→list→show chain. The PARTIALLY DONE annotation for the sub-item is accurate. However, the overall step 14 Summary Verdict of MATCH is wrong and must change to REVISE — the combinatorial matrix and CLI surface tests have no tracking infrastructure, creating a false-closure vector as detailed in the binding decisions above.