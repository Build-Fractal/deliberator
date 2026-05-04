### Remaining Disputes

- **Dispute: Stage B CI timing — documented failure state vs. false health concern**
  - **My claim**: Stage B of the two-stage CI bash step (`|| true` with an inline comment documenting expected failure state) should land in the coordinated PR alongside the marker-filter fix (sub-step-skeptic Rec 2 modified), before Rec 1 lands. The `|| true` plus the comment "exit-1 expected until verify_zero_leakage HTML exclusion fix lands" documents current broken state and creates a concrete flippoint, rather than leaving the date-path entirely uncovered between the filter-fix PR and the Rec 1 PR. (My revision, Rec 7 modified.)
  - **Opposing position(s)**: Sub-step-skeptic's original Dangerous Contradiction 2 framing ("CI smoke job: augment before repair") argues that CI steps that return exit 0 for a known-broken path create false health. While sub-step-skeptic Rec 2 modified permits bash steps to land alongside the marker-filter fix, the general false-health concern — if read strictly — could require Stage B to either enforce failure (exit 1 assertion, impossible before Rec 1) or not exist yet. (Sub-step-skeptic, cross-review Dangerous Contradiction 2; Rec 2 modified.)
  - **Why I will not concede**: A `|| true` step that runs the script and includes an explicit comment is materially different from silence. The comment names the known bug and the fix that resolves it; the flippoint (replacing `|| true` with a strict assertion when Rec 1 lands) creates an actionable merge gate. The alternative — withholding Stage B until Rec 1 — produces a CI gap of unknown duration. If Rec 1 takes several weeks, the date-path remains wholly unexercised in CI throughout that window. The gap is worse than the documented-failure step.
  - **Counter-argument to their position**: Sub-step-skeptic's false-health concern applies to implicitly passing steps. Stage B is not implicit — the `|| true` and the comment make the expected failure state unavoidably visible in CI logs. A developer reading the step knows immediately that it documents a known bug, not a passing check. Implicit exits produce false health; explicitly annotated documented-failure states produce transparency. The two are not the same class of CI defect.
  - **Proposed resolution path**: The synthesizer should specify whether Stage B can land with `|| true` before Rec 1, or must wait until Rec 1 is merged. A concrete middle path: Stage B lands in the coordinated PR with an explicit `echo "KNOWN BUG: date-path exits 1 until Rec 1 (HTML comment exclusion) lands"` line before `|| true`, making the expected failure unavoidably visible in the CI run log and not just in the yaml comment.

---

- **Dispute: Test file location must be chosen before Rec 2 is implemented, not deferred to architecture process**
  - **My claim**: Implementing Rec 2 requires choosing a concrete test file location before writing code. The choice has immediate CI implications: `engine/tests/` reuses the existing `uv run pytest engine/tests/ -x -q --timeout=30` discovery path; `scripts/tests/` requires a separate CI step that does not currently exist. My revision leaves this decision explicitly open and says "should be decided explicitly before implementation." (My revision, Rec 2 modified.)
  - **Opposing position(s)**: Sub-step-skeptic New Rec B says to record the smoke tier architecture decision in §4.3 of spec 061 before step 14's matrix tests are written. This is correct governance process for the long run, but §4.3's decision timeline is decoupled from Rec 2's implementation timeline. If someone implements Rec 2 before New Rec B's §4.3 update, they will choose a location without governance backing and possibly outside the existing CI discovery path. (Sub-step-skeptic, New Rec B.)
  - **Why I will not concede**: The test file location is not adjustable post-hoc without CI system changes. The existing smoke job in `evals.yml` runs `uv run pytest engine/tests/` — a file placed at `scripts/tests/test_strip_constitution.py` is phantom: written, committed, and never executed by CI. A test file that CI does not discover is worse than no test file, because it creates false confidence about coverage that does not exist. This is a P0 implementation prerequisite for Rec 2, not a P2 architecture question. New Rec B governs future additions; Rec 2 needs an answer now.
  - **Counter-argument to their position**: Sub-step-skeptic's architecture decision process is correct for the long run but answers the wrong question for Rec 2's concrete timeline. A specific location decision for Rec 2 — made now, cited as precedent in §4.3 when New Rec B lands — is compatible with New Rec B's governance goal. The two do not conflict unless we assume §4.3 will be updated before anyone tries to implement Rec 2, which is an ordering assumption that has no enforcement mechanism.
  - **Proposed resolution path**: The synthesizer should specify a concrete test file location as part of Rec 2. My recommendation: `engine/tests/test_strip_constitution.py` — it reuses the existing CI discovery path, and the integration test (item 10) can be excluded from smoke by the `@pytest.mark.integration` marker once sub-step-skeptic Rec 2's filter (`-m "not integration and not live and not eval"`) lands. This is compatible with New Rec B's §4.3 governance process and gives implementers an unambiguous destination.

---

### Convergence

- **Converged: Rec 1 (HTML comment exclusion from date leakage check) is the load-bearing fix**
  - **Shared position**: `verify_zero_leakage` must strip HTML comment blocks before scanning for the `--date` needle. This is the P1 unblock for all other recommendations. The specific change is `re.sub(r'<!--.*?-->', '', stripped, flags=re.DOTALL)` before the date needle scan. No other work (CI, tests, documentation) produces a functional strip script until this lands.
  - **Agreeing agents**: All three — script-end-to-end-tester revision Rec 1 (surviving), spec-061-completeness-auditor revision position summary ("highest-priority recommendation is Rec 1"), sub-step-skeptic revision (Rec 1 surviving, confirms CI conceals this bug).
  - **Strength**: Unanimous
  - **Path to convergence**: Agreed from Phase 1; two independent cross-reviews confirmed the blocking impact from different analytical angles. No agent introduced any challenge to the technical approach.

---

- **Converged: Remove L68-78 dead code (Rec 3 modified)**
  - **Shared position**: Lines 68-78's arbiter-ruling substitutions (`The 2026-04-25 deliberation arbiter explicitly extended...`, `The 2026-04-25 deliberation arbiter ruled...`) should be removed, not retained with a comment. The backward-compatibility claim ("they work on pre-v3.1.0 constitutions") is untestable under Rec 2's v3.1.3 test fixture and constitutes an unsubstantiated guarantee in safety-critical infrastructure. The removal should be documented in the strip script docstring with a recovery path for anyone who needs pre-v3.1.0 compatibility in the future.
  - **Agreeing agents**: Script-end-to-end-tester revision Rec 3 (modified from retain to remove); spec-061-completeness-auditor revision Rec 3 (Dangerous Contradiction 2 identified the retain position as internally inconsistent with Rec 2's test plan). Sub-step-skeptic did not challenge this modified position.
  - **Strength**: Unanimous (no agent defended the original retain position after the cross-review)
  - **Path to convergence**: Emerged through cross-review. Spec-061-completeness-auditor identified the internal inconsistency (a backward-compatibility claim untestable by my own test plan), and I conceded in Phase 3. The framing — "either test it or remove it" — was the analytical move that resolved this.

---

- **Converged: Smoke tier marker-filter fix is a prerequisite for any CI bash step additions**
  - **Shared position**: The pytest invocation in `evals.yml`'s smoke job must be changed from `pytest engine/tests/ -x -q --timeout=30` to include `-m "not integration and not live and not eval"` before or alongside any bash step additions. The current smoke job runs `@pytest.mark.integration` tests on every push, violating §4.3's taxonomy. Adding bash steps to a structurally violated job compounds the undocumented state rather than repairing it.
  - **Agreeing agents**: Sub-step-skeptic revision Rec 2 modified (explicit prerequisite); script-end-to-end-tester revision Rec 7 modified (states Rec 7 is "blocked on two prerequisites... (a) sub-step-skeptic's marker filter fix"). Spec-061-completeness-auditor revision does not challenge this.
  - **Strength**: Majority
  - **Path to convergence**: Emerged through sub-step-skeptic's cross-review of my Rec 7. Their Dangerous Contradiction 2 ("CI smoke job: augment before repair") identified that my original Rec 7 would add a bash step to a structurally broken job. I adopted the prerequisite framing in my revision.

---

- **Converged: Stage A CI bash step is valid and should land immediately**
  - **Shared position**: Stage A — running the strip script with `--version` (version-string stripping, always exits 0) — is a valid CI step that validates Steps 1-4 of the strip recipe without touching the broken date-path. It should land in the coordinated PR with the marker-filter fix, regardless of how the Dispute about Stage B resolves.
  - **Agreeing agents**: Script-end-to-end-tester revision Rec 7 (Stage A defined and characterized as immediately valid); spec-061-completeness-auditor revision implicitly supports this (their Dangerous Contradiction 2 specifically objects to the absence of date-path validation, not to version-string validation). Sub-step-skeptic Rec 2 modified permits bash step additions in the coordinated PR.
  - **Strength**: Majority
  - **Path to convergence**: Implicit from the two-stage design I introduced in Phase 3. No agent challenged Stage A's validity; the dispute centers on Stage B. Stage A's convergence is the non-controversial component of my Rec 7 modification.

---

- **Converged: Test #9 must enforce Rec 1 landing, not document broken behavior**
  - **Shared position**: Test #9 in the strip script test file should assert the correct post-fix behavior (`assert verify_zero_leakage(doc_with_prior_sirs, "v3.1.3", "2026-05-01") == []`) decorated `@pytest.mark.xfail(strict=True)`. This creates a CI gate: before Rec 1 lands, the assertion fails as expected (xfail, CI green); when Rec 1 lands, the assertion passes (xpass with strict=True, CI red, prompting removal of the xfail decorator). The original design — asserting the broken behavior — would block the fix.
  - **Agreeing agents**: Script-end-to-end-tester revision Rec 2 modified (introduced this design); sub-step-skeptic revision Rec 2 Dangerous Contradiction 1 (originally identified the semantic inversion in the Phase 1 position, which my modification resolves). No agent challenged the xfail(strict=True) mechanism after my Phase 3 modification.
  - **Strength**: Bilateral (script-end-to-end-tester + sub-step-skeptic, with spec-061-completeness-auditor not objecting)
  - **Path to convergence**: Sub-step-skeptic's cross-review identified the regression-semantics inversion in my original test #9 design. I conceded and inverted the assertion in Phase 3. The xfail(strict=True) mechanism is the resolution that preserves CI enforcement while acknowledging the pre-Rec-1 state.

---

### Final Position Statement

**Non-Negotiables**

1. **Rec 1 (HTML comment exclusion) must land before any other recommendation in this set.** The strip script exits 1 whenever `--date 2026-05-01` is supplied against the current CONSTITUTION.md because prior SIR blocks contain that date. Every operator following the documented usage path cannot produce output until this is fixed. All downstream work — tests, CI, documentation — validates a tool that currently cannot complete its primary workflow. The fix is one `re.sub` call; the blocking impact is total.

2. **Stage A of the CI bash step should land in the coordinated marker-filter PR regardless of how the Stage B dispute resolves.** Stage A validates that the strip script exits 0 on a realistic input with `--version v3.1.3`. It has no dependency on Rec 1, no false-health concern, and fills the CI gap that currently exists for the strip script entirely. If the synthesizer rules that Stage B must wait, Stage A should not wait with it. The two stages are independent.

3. **L68-78 must be removed, not retained with a comment.** A backward-compatibility guarantee that has no test is speculation. The strip script is safety-critical infrastructure in the blind verification workflow. Safety-critical infrastructure that documents guarantees it cannot verify is worse than infrastructure that makes no claim. The recovery path (restore L68-78 with a pre-v3.1.0 fixture if backward compatibility is ever needed) is in the docstring; the claim is not silently maintained in dead code.

**Flexibility**

1. **Stage B's precise timing is negotiable, but its existence before step 14 closes is not.** I am flexible on whether Stage B lands before Rec 1 (with `|| true`) or after Rec 1 (with the strict exit-0 assertion). What I am not flexible on: Stage B must exist before the strip script exits beta. Operators need a CI signal that the date-path is being exercised. The exact mechanism for documenting current failure state is a detail; the requirement that date-path CI coverage exists is not.

2. **Test file location is flexible within the constraint that CI discovers it.** I am flexible on `engine/tests/test_strip_constitution.py` vs `scripts/tests/test_strip_constitution.py`. What must be preserved: the chosen location must be discovered by the current or an explicitly added CI step, and the CI step must be documented in `evals.yml` before the file is committed. A test file that CI does not discover is not a test file; it is documentation formatted as Python.

3. **The docstring annotation language for Rec 4 is flexible; the dual-location requirement is not.** I am flexible on the exact wording of the strip script docstring note about prior SIR preservation behavior. What must be preserved: the behavior must be documented in both the strip script docstring (for developers modifying the script) AND spec 067 §4.2 (for operators running blind verification). A single-location annotation satisfies one audience and leaves the other without the information they need to make correct decisions.