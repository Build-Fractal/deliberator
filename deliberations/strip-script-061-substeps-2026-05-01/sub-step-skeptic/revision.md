Looking at the cross-reviews of my position, I need to read the relevant files carefully before writing my revision.

The files have all been provided in the prompt. Let me compose the revision now based on thorough analysis of all cross-review materials.

### Recommendation Dispositions

#### Recommendation 1: Restate §7 Progress Header

- **Original position**: Replace the misleading "Steps 1–4 complete, remaining work starts at step 5" header with an accurate accounting that reflects non-sequential execution, names the eight strikethroughs correctly, and warns against running steps 7–8 before step 6 closes.
- **Disposition**: Surviving
- **Explanation**: Neither cross-review challenged this recommendation. The spec-061-completeness-auditor's Tensions section ("Scope of audit: individual step completeness vs. execution order correctness") explicitly preserves both audits as correct within their scopes and states the skeptic's §7 header rewrite is "the framing correction that describes the macro state." The script-end-to-end-tester's Safe Agreements section ("The CI tier produces false confidence") independently confirms the false-health-signal diagnosis. No cross-review offered a competing correction or argued the current header is adequate. The recommendation survives unchanged. It is the highest-leverage single change in this review because all other recommendations depend on operators accurately understanding the project's current state before acting.

---

#### Recommendation 2: Fix CI Smoke Tier to Exclude @pytest.mark.integration Tests

- **Original position**: Change the smoke pytest invocation from `pytest engine/tests/ -x -q --timeout=30` to `pytest engine/tests/ -x -q --timeout=30 -m "not integration and not live and not eval"` to enforce the §4.3 marker taxonomy.
- **Disposition**: Modified
- **Explanation**: The script-end-to-end-tester's cross-review raised a Dangerous Contradiction (section: "CI smoke job: augment before repair"): both my Rec 2 and their Rec 7 modify the same smoke job in the same file, and if their Rec 7 lands without my Rec 2, the structural violation persists while CI appears improved. They also raised a separate Dangerous Contradiction (section: "Integration test placement creates a double-bind on the marker taxonomy") noting that if their Rec 2 item 10 (a strip-script integration test) carries `@pytest.mark.integration`, my filter would exclude it from smoke, defeating their Rec 7's purpose.

The cross-review's own suggested resolution resolves this without requiring me to modify my recommendation's substance: the strip-script integration test should carry `@pytest.mark.integration` and run only pre-release per the taxonomy; their Rec 7 adds the strip script as a **bash shell step** in evals.yml, not as a pytest test. Bash steps are outside the pytest marker taxonomy entirely. The double-bind dissolves once the two mechanisms are kept separate.

The modification is therefore procedural, not substantive: the `-m` filter change and any bash step additions to the smoke job should land in a single coordinated PR. My filter remains correct. Adding the filter in isolation while leaving strip-script coverage absent is valid; adding the bash step in isolation while leaving the integration test in the wrong tier is a P1 violation. The recommended sequencing: Rec 2 (marker filter) is a prerequisite for any further pytest-taxonomy work; it may be implemented in the same PR as bash step additions.

---

#### Recommendation 3: File Tracking Issue for Step 11 and Mark Step 12 Blocked

- **Original position**: File a GitHub issue for step 11 with scope boundaries; add BLOCKED notation to step 12 citing the issue number; add to §6 criterion 3 "Not achievable until step 11 lands."
- **Disposition**: Surviving
- **Explanation**: The spec-061-completeness-auditor's Safe Agreements section ("Step 11/12 Dependency Requires Tracking Infrastructure") independently reached the same recommendation with the same language: "An untracked deferral of an architectural prerequisite is functionally abandoned." Their version adds complementary evidence — the SC#3 closure gate that prevents indefinite deferral. No cross-review challenged this recommendation. The completeness-auditor's SC#3 framing strengthens it: the tracking issue filed for step 11 must explicitly note that SC#3 cannot be marked ACHIEVED until step 11 lands. Without that language in the issue, a future contributor can defer step 11 indefinitely without triggering a spec-closure gate failure. I adopt the SC#3 consequence language as an addendum to the recommendation, not a modification — the core recommendation is unchanged.

---

#### Recommendation 4: Block Steps 7 and 8 on Step 6 Completion

- **Original position**: Add prerequisite annotation to steps 7 and 8: quality calibration and baseline snapshots MUST NOT run before step 6 (G2/G12 fixes) closes, because any quality baseline captured against a G12-broken engine misrepresents provider-matrix behavior permanently.
- **Disposition**: Modified
- **Explanation**: The spec-061-completeness-auditor's cross-review (Tensions: "§3.1.9 coverage gaps: both P1, but ordered differently relative to G12") identified a material correction to my framing: the completeness-auditor's P1 recommendations for step 13 coverage gaps (iterations=3 cost estimate, arbiter influence output headings) both use the mock provider via `test_sdk.py` and `test_phases.py`. These tests exercise Python-surface behavior through internal APIs and never touch the YAML-configured provider selection path that triggers G12. The completeness-auditor stated explicitly: "the conflict is therefore less severe than it appears... The skeptic's blocking logic applies to quality-tier calibration (step 7) and baseline snapshots (step 8), not to mock-provider behavioral unit tests."

My original recommendation was correct in its primary target — G12 blocks steps 7 and 8 — but it was stated in terms that could be read as blocking all new test work before step 6 closes. The modified recommendation narrows the scope: the G12 prerequisite applies to (a) quality-tier calibration runs using real providers (step 7), (b) baseline snapshots captured against real-provider output (step 8), and (c) any test that exercises the YAML-configured `conversus run` path where `VALID_PROVIDERS` is checked at parse time. Mock-provider behavioral unit tests that invoke `run_pipeline`, `run_decide_mcp`, or handler functions directly are not blocked by G12 and may proceed in parallel with step 6 remediation. The spec annotation for steps 7–8 should specify "YAML-configured or real-provider runs" rather than simply "steps 7 and 8," to prevent the blocking logic from being misapplied to mock-provider work.

---

#### Recommendation 5: Define @pytest.mark.smoke Marker or Rename Step 14's Cross-Axis Deliverable

- **Original position**: Either add `smoke` to §4.3 with a definition, or rename step 14's "6 cross-axis smoke combinations" deliverable to use an existing marker, before step 14's matrix tests are written.
- **Disposition**: Modified
- **Explanation**: The script-end-to-end-tester's cross-review (Tensions: "Bash-level vs. pytest-level smoke validation") surfaced a genuine tension my original recommendation did not address: I implicitly assumed the smoke tier is a pytest-marker category requiring a formal §4.3 entry, but script-end-to-end-tester's Rec 7 treats bash shell steps in evals.yml as a valid smoke-tier mechanism that operates outside the pytest marker taxonomy. These two models of the smoke tier are not mutually exclusive, but they have different implications for step 14's implementation.

The modified recommendation resolves the ambiguity rather than pre-deciding it: before step 14's matrix tests are written, §4.3 must record an explicit decision about the smoke tier's architecture. If bash steps constitute the smoke mechanism for non-Python validation (strip script, CLI integration), then step 14's matrix tests may be implemented as parametrized bash steps rather than pytest tests, and no new `@pytest.mark.smoke` is needed. If pytest is the canonical mechanism for all smoke-tier assertions, add the marker. Either path is acceptable; the gap is that no path has been chosen and recorded. The modification removes the prescriptive "option (a) or option (b)" framing in favor of: "document the smoke tier architecture decision in §4.3 before step 14's matrix tests are written, and ensure any future bash steps and any `@pytest.mark.smoke` usage are governed by the same documented decision."

---

#### Recommendation 6: Mark Step 10 DONE with Accurate CI Contribution Attribution

- **Original position**: Update the step 10 DONE note to credit PR #83 for the smoke tier's origin and PR #101 for the quality/deepeval tiers and workflow_dispatch inputs.
- **Disposition**: Modified
- **Explanation**: The script-end-to-end-tester's cross-review (Tensions: "Attribution of CI smoke-tier provenance across PRs") identified a sequencing problem: if their Rec 7 (strip-script addition to smoke) lands as a separate PR before my Rec 6 correction is applied, the step 10 DONE note must be expanded again to include the new PR. Two sequential single-PR DONE note corrections are worse than one coordinated correction.

The modified recommendation bundles the attribution correction with any further smoke-tier additions: the PR that implements any further changes to evals.yml's smoke job (including strip-script bash step if pursued) should apply the step 10 attribution correction atomically, naming all contributing PRs. The corrected annotation: "PR #83 established the smoke tier; PR #101 added the quality (Ollama) and deepeval (Anthropic) tiers and workflow_dispatch inputs; [subsequent PR] added [strip-script step or other addition]." This is a coordination requirement, not a change to the substantive correction.

---

#### Recommendation 7: Correct Node Version Requirement in Step 10

- **Original position**: Update step 10's runner requirement from "Node 18" to "Node 22 LTS." (Priority: P2)
- **Disposition**: Modified
- **Explanation**: The spec-061-completeness-auditor's cross-review (Dangerous Contradictions: "Node version fix priority: P1 vs. P2") challenged my P2 classification. The completeness-auditor assigned P1 to the identical fix, citing Principle XIV ("A spec that says X when the implementation does Y is a bug in the spec") and the concrete failure mode: a future contributor reading §7 step 10's runner requirements would pin `node-version: '18'`, restoring EOL behavior (Node 18 reached EOL April 2025) and potentially breaking the eval pipeline silently. The cross-review stated: "Both reviews describe the same failure mode with the same words. Defaulting to the higher priority (P1) is conservative and costs nothing. The skeptic should yield on the priority classification."

I yield. The risk is real and the fix is trivial. Node 18 EOL is not a theoretical future risk but an already-past date. Any contributor following the spec today would introduce a security exposure and runtime breakage. The recommendation is modified to P1 with the completeness-auditor's constitutional grounding as the stated rationale.

---

#### Recommendation 8: Document Step 14 Bundle Intent

- **Original position**: Add to step 14: "These three deliverables form the CI/CD consumer contract. The persistence round-trip sub-item MAY ship independently but does NOT close step 14."
- **Disposition**: Modified
- **Explanation**: The spec-061-completeness-auditor's cross-review (Dangerous Contradictions: "Step 14 Bundling: Legitimate Partial Delivery vs. False-Completeness Vector") challenged my framing in two directions simultaneously. The completeness-auditor gave a MATCH verdict on the PARTIALLY DONE marker, suggesting my concern was overstated; but they also acknowledged that without explicit tracking infrastructure, the combinatorial matrix could be deferred indefinitely. Their suggested resolution: the auditor should yield on the MATCH verdict classification (upgrade to REVISE), and I should yield on whether PARTIALLY DONE was appropriate as a snapshot.

The modification strengthens the recommendation to require tracking infrastructure, not just documentation: the spec annotation must state both (a) that persistence sub-item delivery does NOT close step 14, AND (b) that the exit-code and matrix sub-items require independent GitHub issues before step 14 can be marked done. Without the independent tracking issues, a contributor who closes the exit-code sub-item (when spec 048 lands) has no mechanism preventing them from marking the full step done while the combinatorial matrix remains permanently deferred. Documentation alone is insufficient; the tracking issues constitute the gate.

---

#### Recommendation 9: Require Step 5 (SKILL.md Parity) Before Any Quality-Tier Work

- **Original position**: Add to §7: "Step 5 is a prerequisite for steps 7–12. Without SKILL.md parity, the engine's Python surface and the SKILL.md surface can diverge silently."
- **Disposition**: Modified
- **Explanation**: The spec-061-completeness-auditor's cross-review (Tensions: "G2/G12 Severity") applied the same parallel-tracks logic to step 5 as to G12: mock-provider unit tests that test Python-surface behavior through internal APIs are not blocked by step 5's open status, because they don't exercise the SKILL.md surface. The same analysis that modified Rec 4 applies here.

The modification narrows the prerequisite scope: step 5 is a prerequisite for (a) quality-tier calibration using real providers (step 7), (b) cross-surface parity tests (step 12), and (c) any test that exercises the SKILL.md agent-dispatch surface. It is NOT a prerequisite for mock-provider Python-surface unit tests. The original framing "prerequisite for steps 7–12" overstated the blocking scope and would have incorrectly blocked the completeness-auditor's mock-provider §3.1.9 gap-filling tests. The modified language: "Step 5 is a prerequisite for quality-tier calibration (step 7) and cross-surface parity tests (step 12). Mock-provider Python-surface unit tests (steps 9, 13, and similar) may proceed independently of step 5."

---

### New Recommendations

#### New Recommendation A: File Tracking Issues for §3.1.9 Step 13 Coverage Gaps

- **Priority**: P1
- **Triggered by**: spec-061-completeness-auditor/cross-reviews/sub-step-skeptic.md, Tensions section ("§3.1.9 coverage gaps: both P1, but ordered differently relative to G12") and Safe Agreements section ("Step 13's §3.1.9 arbiter influence row is not closed at the pipeline output level").
- **Proposed change**: File two GitHub issues against step 13's DONE marker: (1) iterations=3 cost estimate assertion — `test_three_iterations_dispatch_counts` and `test_three_iterations_revision_naming` verify dispatch counts and file naming, but neither asserts that the cost estimate presented to the user at deliberation start reflects 3× the per-iteration cost; a user may see a cost estimate calibrated for 1 iteration and then pay 3×. (2) Arbiter influence=binding vs. advisory output heading — `_make_arbiter_config` in `test_phases.py` never sets the `influence` argument, meaning all three arbitration trigger tests (`test_always_trigger`, `test_disputes_remain_trigger_with_disputes`, `test_disputes_remain_trigger_no_disputes`) exercise only the default binding influence level. A regression in the advisory or informational heading text would pass all three tests. Step 13's DONE annotation should be revised to DONE WITH OPEN GAPS until these issues are filed.
- **Rationale**: My original macro-level audit of step 13 focused on the execution-order violation (steps 9/10/13/14a before 5/6/7/8) and noted the dispatch-count and revision-naming tests as "substantively written and not tautologies." I did not inspect the §3.1.9 coverage matrix row-by-row. The completeness-auditor did, and found two P1 rows uncovered. These gaps are verifiable by direct test inspection, are independent of G12 (mock provider, Python-surface unit tests), and support my original thesis that the step 13 DONE marker is overclaimed. The completeness-auditor's evidence makes my original contrarian position on step 13 stronger, not weaker — I was right that the DONE marker should be scrutinized, I simply missed the specific lines of evidence.

---

#### New Recommendation B: Record Smoke Tier Architecture Decision Before Step 14 Implementation

- **Priority**: P2
- **Triggered by**: script-end-to-end-tester/cross-reviews/sub-step-skeptic.md, Tensions section ("Bash-level vs. pytest-level smoke validation"), and my own cross-review of script-end-to-end-tester (Tensions: "Smoke vs not-smoke").
- **Proposed change**: Before step 14's matrix tests are written, add an explicit architecture note to §4.3 of spec 061 clarifying: "The smoke tier contains two types of validation: (1) pytest tests governed by the marker taxonomy (excluded from smoke via `-m` filter if they carry `@pytest.mark.integration` or higher-cost markers); (2) bash shell steps in evals.yml that validate CLI and script behavior without entering the pytest taxonomy. Bash steps are not subject to marker governance but are constrained to: mock provider only, structural validation, exit code 0 assertion. When implementing step 14's 6 cross-axis smoke combinations, choose the mechanism (pytest parametrize or bash parametrize) that matches this taxonomy."
- **Rationale**: My original Rec 5 and the script-end-to-end-tester's Rec 7 are pulling against each other because they implicitly hold different models of what the smoke tier is. My cross-review of script-end-to-end-tester identified this tension but did not resolve it — I noted that "the smoke tier architecture needs one explicit decision before either recommendation is implemented." That decision belongs in §4.3 as a written record, not in a cross-review tension summary. Without it, the contributor who closes step 14 will choose a mechanism inconsistently with whatever mechanism the strip-script bash step establishes, and future additions will compound the inconsistency. The documentation cost is one paragraph; the compound inconsistency cost is unbounded.

---

### Position Summary

I withdrew zero recommendations, modified seven of nine original recommendations, and maintained two unchanged. The modifications were primarily of three kinds: scope narrowing (Recs 4 and 9), priority escalation (Rec 7 from P2 to P1 on the strength of the completeness-auditor's Principle XIV constitutional grounding), and procedural coordination requirements (Recs 2, 6, and 8 now require atomic implementation with related changes to prevent partial-application failure modes).

The most significant change in my thinking was produced by the spec-061-completeness-auditor's analysis of which test paths are blocked by G12 versus which are independent. My original framing treated G12 as a global blocker — "any quality baseline captured before step 6 closes will reflect a broken provider matrix" — and I applied that logic broadly enough that it could have been read as blocking all new test work. The completeness-auditor correctly identified that mock-provider unit tests exercising Python-surface behavior through internal APIs never hit the YAML-configured `VALID_PROVIDERS` check. This distinction allows the completeness-auditor's §3.1.9 gap-filling work (New Recommendation A) and my original Recs 3, 5, 7, 8 to proceed in parallel with G12 remediation rather than being sequenced after it. I was wrong about the blocking scope; I was right about the blocking rationale.

My highest-priority recommendation that should survive into the final synthesis is Rec 1: restate the §7 progress header. Every other recommendation in this review — CI repair, step 11 tracking, G12 blocking scope, node version, step 14 bundle, §3.1.9 gaps — requires an operator who correctly understands the project's actual state before acting. The current header ("Steps 1–4 complete, remaining work starts at step 5") makes the non-sequential execution invisible. A contributor reading eight strikethroughs and following the header's navigational instruction will proceed to step 5 correctly — but will calibrate their trust against a false completion count, will not know that G12 and G2 remain P1-open, and will not know that steps 9/10/13/14a were done out of sequence with P1 bugs still present. The header correction is the single change that makes all other changes discoverable by any contributor who reads §7 in good faith.