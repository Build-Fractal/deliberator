I'll read the required documents in order before producing the arbitration resolution.

Now let me read the Phase 4 dispute documents.

Now I have all required documents. Producing the arbitration resolution.

### Process Note

This arbitration was triggered by the `always` condition configured for subject arbitration in this conversus run. Four disputes remain unresolved from the Phase 5 synthesis. The deliberation involved two agents — **skeptical-reviewer** and **pragmatist-reviewer** — operating in **cooperative** mode over five phases, one iteration round. This is a subject-arbitration deliberation: the arbiter is the reviewed system, holding binding authority from operational knowledge and design intent. Disputes were identified in the synthesis's "Remaining Disputes" section (synthesis final.md, lines 160–186).

---

### Decision Framework

Principles from CONSTITUTION.md v2.5.0 bearing on the four remaining disputes:

- **[Principle V — Observable Deliberation]**: "Agents MUST NOT silently swallow errors." Extended here: a deliberation must not silently re-open confirmed findings after bilateral convergence. (CONSTITUTION.md §V.)

- **[Principle IX Extension (v2.3.0) — Behavior-over-shape testing]**: "Tests MUST assert behavioral properties (what the code *does*) rather than structural properties." A test that cannot be made to fail cannot validate that it catches the behavior it claims to cover. (CONSTITUTION.md §IX Extension.)

- **[Principle XXII §3 — End-to-end install testing]**: "Every distribution path MUST be tested from a fresh environment in CI (or a documented manual test) before tagging a release." This requirement is binary (was install testing performed?) and is not keyed to version-number increment size. (CONSTITUTION.md §XXII, bullet 3.)

- **[Principle XXVIII — Test-Fix Boundary Preservation]**: "When fixing a failing test, the fix MUST preserve the test's verification of real behavior." A test written against a code path with no exercisable precondition has no failing scenario and cannot be validated. (CONSTITUTION.md §XXVIII, clause 2.)

- **[Governance → Amendments → Constitutional Inclusion Criteria, Criterion 2 — Falsifiable scope]**: Governance and constitutional text "MUST be specific enough to flag a hypothetical future PR as violating, without requiring 'interpretation.'" A validity condition ("valid when X") does not prohibit overrides that lack X if other validity criteria are asserted; a mandatory obligation ("must quote X") does. (CONSTITUTION.md §Governance, Constitutional Inclusion Criteria, Criterion 2.)

- **[Known Antipatterns — Redundant Cache]**: "Do not create manually-maintained tracking documents that duplicate existing infrastructure." Retrospective process notes for no-adverse-outcome events are the recognized variant of this antipattern. (CONSTITUTION.md §Known Antipatterns.)

---

### Binding Decisions

#### Dispute: OAuth Verification Epistemic Authority

**Positions:**
- **Skeptical-reviewer**: The Phase 3 code quote (`grep -qE '"(access_token|oauth|subscription)"' "$HOME/.conversus/auth.json"`) is complete, locatable, and unambiguous; treating it as insufficient while calling for the identical read in synthesis is circular. (Skeptical Phase 4 disputes.md, "Remaining Disputes" §1.)
- **Pragmatist-reviewer**: New Rec 1 originally required independent synthesis verification as a blocking prerequisite; however, Phase 4 disputes.md "Convergence" §5 explicitly lists "OAuth Concern Filed as P2" as bilateral convergence and states the code verification satisfies the prerequisite. (Pragmatist Phase 4 disputes.md, "Convergence" §5.)

**Synthesizer's assessment:** The meta-dispute is effectively moot. Pragmatist's Phase 4 convergence resolved the process question; the substantive factual question is answered. (Synthesis final.md, "Remaining Disputes" §1, synthesizer assessment.)

**Ruling:** The meta-dispute is resolved in skeptical's favor. Skeptical's Phase 3 code verification is dispositive closing evidence. The OAuth P2 issue is filed per the synthesis Convergence §2 specification.

**Grounding citation:** Principle V (Observable Deliberation) — deliberations must not silently swallow confirmed findings. Once pragmatist's Phase 4 document explicitly listed "OAuth Concern Filed as P2" as a bilateral convergence point and accepted the verification as satisfying Modified Rec 2a's conditional, re-opening the factual question at the synthesis stage would violate V's completeness obligation. A code quote with a specific file reference and complete bash snippet is the same evidence an independent file read produces.

**Rationale:** The residual dispute was procedural: should the synthesizer independently re-verify before acting on a code claim made by one reviewer? Pragmatist's own Phase 4 document renders this question moot by accepting the verification. The "verify first" principle is sound in general — deliberations should not act on unverified unilateral factual claims — but that principle is satisfied by an exact, locatable code quote, not only by synthesizer-level re-reads. No circular process norm is introduced.

**Rejected position:** Pragmatist's New Rec 1 "verify first" framing was correct as an initial process norm. The reason it is rejected here is not that the norm is wrong but that pragmatist themselves applied and satisfied it in Phase 4. The rejected position is the hypothetical insistence on synthesis-level re-verification after bilateral convergence is already recorded.

**Required changes:** No document changes required from this dispute. Record: "OAuth preflight regex confirmed to target `auth.json`; `"subscription"` key is the actionable false-positive surface. File GitHub issue per synthesis Convergence §2: 'fix(skills): OAuth marker regex may match non-OAuth content in auth.json — evaluate removing `subscription` from preflight pattern or replacing with structural `jq -e '.access_token or .oauth'` check.' P2 priority."

---

#### Dispute: Spec Amendment Wording — Mandatory vs. Conditional Framing

**Positions:**
- **Skeptical-reviewer**: Mandatory framing, uniformity-scoped: "A uniformity override claim **must** quote the specific text from the affected existing principle that would be narrowed under uniform application." (Skeptical Phase 4 disputes.md, "Remaining Disputes" §2.)
- **Pragmatist-reviewer**: Conditional framing, all-overrides-scoped: "Override with rationale is **valid when** the rationale **quotes** the specific text of the existing principle that would be narrowed under uniform application." (Pragmatist Phase 4 disputes.md, "Convergence" §4.)

**Synthesizer's assessment:** Skeptical's mandatory framing is analytically stronger for falsifiability; pragmatist's broader scope (all override-with-rationale, not uniformity-only) is more robust. Adopts skeptical's framing with pragmatist's scope. (Synthesis final.md, "Remaining Disputes" §2, synthesizer assessment.)

**Ruling:** Adopt the synthesizer's merged formulation: "Any override-with-rationale claim must quote the specific text of the existing principle that would be narrowed under the override; the quoted passage and rationale are logged in SIR, governance log, and spec status."

**Grounding citation:** Governance → Amendments → Constitutional Inclusion Criteria, Criterion 2 (Falsifiable scope). The requirement is specifically that governance text must be "specific enough to flag a hypothetical future PR as violating, without requiring 'interpretation.'" Under "valid when X," a future override author can assert validity on non-X grounds and the text is silent about whether that is permitted — a reviewer must interpret whether alternative grounds are valid. Under "must quote X," no interpretation is required: an override without quoted text violates the anchor categorically. The Criterion 2 standard for governance text mirrors its standard for constitutional text.

**Rationale:** Both agents agreed the purpose is falsifiability — the override argument must be checkable without independent research. Pragmatist's "valid when" formulation correctly describes the intent but fails to enforce it: a sufficient condition for validity is not a prohibition on omitting the condition. Skeptical's observation that "valid when X allows override without X if other criteria are asserted" is analytically precise and not rebutted by pragmatist's revision. The scope question favors pragmatist: the falsifiability need exists for any override-with-rationale invocation, not only uniformity overrides, and limiting scope to uniformity invites second-guessing about whether a given override "counts" as uniformity-based.

**Rejected position:** Pragmatist's "valid when" framing was likely intended to merge both requirements into a single sentence. The intent is correct; the legal structure is not. Under conditional framing, the anchor would be satisfied by an override that cites "sufficient grounds" without quotation, provided the author argues those grounds are valid. That is the exact gap the requirement was designed to close.

**Required changes:** CONSTITUTION.md (Governance → Amendments section) — add the following sentence after the existing Amendments bullet: "Any override-with-rationale claim must quote the specific text of the existing principle that would be narrowed under the override; the quoted passage and rationale are logged in SIR, governance log, and spec status." Note in the same edit: the 2026-04-29 governance log entry (CONSTITUTIONAL_CONVERSATIONS.md L370) is the inaugural instance and predates this requirement; it is grandfathered but future overrides must include the quoted passage. Per SESSION-REVIEW.md acceptance bar, this Q3 finding is DEFER-eligible and is classified as DEFERRED pending the next CONSTITUTION.md amendment cycle.

---

#### Dispute: Multi-Pattern Parametrized Test for `_detect_provider_passthrough_error` as Pre-Emptive Filing

**Positions:**
- **Skeptical-reviewer**: File now as a low-cost P3 hedge; the `any()`/`all()` iteration error would require debugging rather than test-writing at the point the second pattern is added; filing now is cheap. (Skeptical Phase 4 disputes.md, "Final Position Statement" Rec 7.)
- **Pragmatist-reviewer**: The test for multi-entry iteration has no failing scenario today; a developer writing it cannot confirm it catches what it claims to catch; a PR-level convention delivers the same coverage at the moment the path is activated. (Pragmatist Phase 4 disputes.md, "Remaining Disputes" §1.)

**Synthesizer's assessment:** Pragmatist's position is stronger; grounding in Principle XXVIII is sound. Writing the test requires speculating about a second pattern that does not yet exist; the introducing PR is the correct location. (Synthesis final.md, "Remaining Disputes" §3, synthesizer assessment.)

**Ruling:** Adopt pragmatist's position. Skeptical's Rec 7 is not filed as a standalone issue. Record as a PR-level convention in deliberation output.

**Grounding citation:** Principle XXVIII (Test-Fix Boundary Preservation) and Principle IX Extension (behavior-over-shape testing). Principle XXVIII requires tests to preserve "verification of real behavior" and is grounded in the discipline that tests without exercisable failure scenarios teach false coverage lessons. Principle IX Extension states tests "MUST assert behavioral properties (what the code *does*)" — a test for iteration over a second tuple entry that does not exist cannot assert the behavioral outcome of that iteration, because the outcome depends on what the second entry matches, which is unknown.

**Rationale:** Skeptical's "debugging vs. testing" observation is accurate and compelling as a risk framing. However, it supports the PR-level convention, not a filed issue. A filed issue instructs a future PR author to write a test for behavior they may not yet understand, using a test that cannot be made to fail in its pre-existing state. A convention instructs the same author to write the test in the same PR where the behavior is created — at which point they know the expected semantics, can make the test fail first, and can validate coverage against a real case. The convention delivers identical safety-net value at the correct moment without generating premature backlog.

**Rejected position:** Skeptical's Rec 7 correctly identifies that a latent structural gap exists. The rejected position is not the identification of the gap but the proposed remedy. Filing a standalone issue for a test that cannot currently be validated produces a test artifact that the suite treats as green regardless of whether the iteration logic is correct — which is the definition of a misleading coverage signal under Principle IX Extension.

**Required changes:** No issue to file. Record in deliberation output (operational guidance note): "When a second detection pattern is added to `_detect_provider_passthrough_error`'s patterns tuple, the introducing PR must include a parametrized test covering multi-entry iteration semantics (both match and no-match cases with 2+ entries). The test must be made to fail against a broken implementation before it is considered valid. Do not file a standalone issue; the test belongs at the PR that activates the path."

---

#### Dispute: Version Bump Install Verification Gap as P3 Retrospective Filing

**Positions:**
- **Skeptical-reviewer**: The 0.1.0→0.3.0 jump implies skipped intermediate releases; Principle XXII §3 requires install testing before tagging a release; recommends future bumps >patch include a `pip install .` from a fresh environment as part of the PR checklist. (Skeptical Phase 4 disputes.md, "Final Position Statement" New Rec 2.)
- **Pragmatist-reviewer**: The bump is a label sync to the CLI ship version; no install regression occurred; the "monotonic increment" threshold has no basis in governance text; filing retrospective process notes for no-adverse-outcome events is the session's named anti-pattern. (Pragmatist Phase 4 disputes.md, "Remaining Disputes" §2.)

**Synthesizer's assessment:** Pragmatist's position is stronger on three independent grounds: the threshold has no governance basis, no install regression occurred, and the anti-pattern was explicitly named in the session. (Synthesis final.md, "Remaining Disputes" §4, synthesizer assessment.)

**Ruling:** Adopt pragmatist's position. "Routine sync" classification for the 0.1.0→0.3.0 version bump stands. No issue to file. Record as an informational note in deliberation output.

**Grounding citation:** Principle XXII §3 and Known Antipatterns (Redundant Cache). Principle XXII §3 requires install testing "before tagging a release" — this is a binary gate on the tagging event, not a threshold keyed to version-number jump size. No text in §3 creates a distinct requirement for multi-version jumps. The Known Antipatterns section prohibits creating tracking documents for no-adverse-outcome events, and skeptical's Phase 3 revision acknowledges the gap exists only in review coverage, not in actual project outcome.

**Rationale:** Skeptical grounds the concern in Principle XXII §3 but does not quote the text that creates a monotonic-increment threshold — because no such text exists. This is particularly notable given that Dispute 2 establishes a "must quote" standard for claims of principle violation; the same evidentiary discipline applies here. The label-sync nature of the bump (tracking CLI ship version 0.3.0, with 0.2.0 never published as a milestone) and the absence of any observed install regression together confirm routine-sync classification. Skeptical's honest acknowledgment of having missed the concern increases the deliberation record's credibility but does not transform an uninvoked principle into an invoked one.

**Rejected position:** Skeptical's concern is grounded in a real principle (XXII §3) and a real heuristic (larger version jumps warrant scrutiny). The rejected position is not the heuristic itself but its elevation into a governance requirement without textual basis. Skeptical's own proposed spec change (Dispute 2) requires quoting the governing text for any override or principle citation — that standard, applied consistently, defeats New Rec 2's textual grounding.

**Required changes:** No issue to file. Record in deliberation output (informational note): "0.1.0→0.3.0 version bump in PR #51 is correctly classified as routine sync to CLI ship version. For future PRs: plugin version bumps that skip intermediate version numbers should document in the PR body which CI step or manual test provided install verification (e.g., 'CI install smoke test passed at commit X'). This is an informational note, not a blocking checklist item."

---

### Summary of Changes Required

**P1 — Required for correctness (no blocking defects in engineering work; these are convergent unfiled actions from the deliberation):**

1. **File 1KB adversarial test issue** (from unanimous Convergence): GitHub issue "test(engine): add adversarial long-response test for `_detect_provider_passthrough_error` — error string past 1KB boundary." One parametrized test, preamble ≥1025 bytes + error indicator, asserts function returns False. No implementation change required. Unanimous convergence across all phases.

2. **File OAuth false-positive scoping issue** (from Dispute 1 + bilateral Convergence): GitHub issue "fix(skills): OAuth marker regex may match non-OAuth content in auth.json — evaluate removing `subscription` from preflight pattern." Scope: evaluate removing `"subscription"` from `grep -qE '"(access_token|oauth|subscription)"'` or replacing with `jq -e '.access_token or .oauth'` structural check. P2 priority.

**P2 — Required for design integrity:**

3. **File Bug 3b future-alias regression test** (from unanimous Convergence): Add `test_decide_unknown_model_does_not_trigger_blocklist_fallback` — asserts that a model alias not on the blocklist passes through to `run_engine` unchanged without triggering blocklist substitution. Lives in parallel with Issue #54, not as a substitute.

4. **Record architectural characterization of `_gated_dispatch` dispatch semantics** (from unanimous Convergence): Before this deliberation is considered complete, provide in deliberation output one positive sentence: "Cooperative dispatch is sequential; `_gated_dispatch` is not invoked concurrently in the current engine" — or file a bounded issue if the model cannot be stated confidently. Burden-shift alone is insufficient given `_gated_dispatch`'s position on PR #52's fix path.

**P3 — Recommended improvements:**

5. **Add monkeypatch target comment** in `engine/tests/test_cli.py::TestDecideCommand` adjacent to `monkeypatch.setattr("engine.run.run_engine", fake_run_engine)`. (From synthesis P3, Pragmatist Rec 5.)

6. **Record multi-pattern test PR-level convention** in deliberation output as operational guidance (from Dispute 3 ruling; not a filed issue).

7. **Record version bump documentation preference** in deliberation output as informational note (from Dispute 4 ruling; not a checklist requirement).

**DEFERRED:**

8. **CONSTITUTION.md override-with-rationale anchor** (from Dispute 2): Add "Any override-with-rationale claim must quote the specific text of the existing principle that would be narrowed under the override; the quoted passage and rationale are logged in SIR, governance log, and spec status." under Governance → Amendments, with note grandfathering the 2026-04-29 inaugural entry. DEFER-eligible per SESSION-REVIEW.md Q3 acceptance bar; target: next CONSTITUTION.md amendment cycle.

---

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| OAuth Verification Epistemic Authority | Skeptical's code verification is dispositive; OAuth P2 filed | High | Pragmatist's Phase 4 document resolves the meta-dispute in skeptical's favor; no residual factual ambiguity remains; Principle V completeness obligation makes re-opening the finding indefensible |
| Spec Amendment Wording — Mandatory vs. Conditional | Mandatory "must quote" framing + pragmatist's broader scope | High | Constitutional Inclusion Criterion 2 directly addresses sufficient-vs-necessary condition distinction; neither agent contests the underlying falsifiability purpose; the logical gap in conditional framing is unambiguous |
| Multi-Pattern Test as Pre-Emptive Filing | PR-level convention; do not file issue | High | Principle XXVIII grounding is direct; "test cannot be made to fail" is an unambiguous violation of XXVIII's validation requirement; pragmatist's proposed convention is strictly superior to filed issue at no cost |
| Version Bump Install Verification Gap | Routine sync classification stands; no issue | High | Principle XXII §3 text does not support the claimed monotonic-increment threshold; skeptical's own proposed evidentiary standard (Dispute 2) defeats the textual grounding of New Rec 2; Known Antipatterns directly applies |

The deliberation demonstrated strong process health: six of ten recommendations reached bilateral or unanimous convergence, the two most important concessions (skeptical's Rec 5 withdrawal, pragmatist's Phase 4 OAuth convergence) were well-reasoned and unsentimental, and the four remaining disputes were genuine analytical disagreements rather than failures of the deliberation process. The systemic contradictions identified by the synthesizer — particularly the Q1 "deliberation invitation" format and the pre-emptive vs. just-in-time test writing tension — are well-diagnosed operational guidance gaps. The pre-emptive test writing tension is now partially addressed by the Dispute 3 ruling, which establishes a PR-level convention that future deliberations can reference rather than re-litigating the principle from scratch. The most actionable systemic fix (classifying Q1 security sub-questions at point of identification rather than delegating to the deliberation) does not require constitutional amendment and should be adopted as an operational guidance update to session review templates.

---

## REQUIRED FIXES BEFORE ACCEPTANCE

None.

## RECOMMENDED FIXES

1. File 1KB adversarial test issue for `_detect_provider_passthrough_error` boundary (P1 convergent signal)
2. File OAuth `"subscription"` key false-positive scoping issue (P2 bilateral convergent signal)
3. Add `test_decide_unknown_model_does_not_trigger_blocklist_fallback` regression test (P2 unanimous convergent signal)
4. Provide one-sentence architectural characterization of `_gated_dispatch` dispatch semantics in deliberation output (P2 unanimous convergent signal)
5. Add monkeypatch target comment in `engine/tests/test_cli.py::TestDecideCommand` (P3)

## DEFERRED

1. CONSTITUTION.md override-with-rationale anchor amendment (Q3, DEFER-eligible per SESSION-REVIEW.md acceptance bar; mandatory "must quote" framing + all-overrides scope; target next amendment cycle)
2. Operational guidance note: multi-pattern test PR-level convention for `_detect_provider_passthrough_error`
3. Informational note: version bump documentation preference for skipped intermediate versions

## SESSION VERDICT: ACCEPTED WITH RECOMMENDATIONS