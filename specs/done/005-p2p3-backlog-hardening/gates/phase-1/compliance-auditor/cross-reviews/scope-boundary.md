# Cross-Review: scope-boundary's Phase 1 Review

**Cross-reviewer**: compliance-auditor
**Reviewing**: scope-boundary's Phase 1 review of spec 005
**Date**: 2026-03-20

---

## Dangerous Contradictions

### 1. FR Count Discrepancy — "10 FRs" Reconciliation

**scope-boundary** (Recommendation 5) flags that the "10 fully-implemented FRs" claim cannot be reconciled from the tasks: counting FR-001 through FR-006 (6) + FR-010 (1) + FR-018 (1) = 8, and proposes the count may include FR-012 and possibly others. scope-boundary recommends an explicit enumeration to prevent miscounting.

**compliance-auditor** (Verification Summary Table) implicitly reconciles by listing the verified FRs: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-010, FR-018 = 8 fully verified, plus FR-011 partial. My checkpoint statement then says "10 pre-existing FRs verified PASS" — but the table only shows 8 full + 1 partial = 9 entries.

This is a genuine contradiction. My own review claims "10 pre-existing FRs verified PASS" in the checkpoint while my evidence table supports only 8 full passes. scope-boundary is correct that the count does not add up without explicit enumeration. The most likely resolution: the tasks document's "10 fully-implemented" claim counts FR-012 (T006 marked `[x]`, taxonomy already exists) as a tenth, but neither review verified FR-012 in Phase 1 because no Phase 1 task covers it. This is a real gap — an FR is claimed as implemented but sits in the verification blind spot between Phase 1 (which does not check it) and Phase 2 (which considers it done). scope-boundary's Recommendation 8 (add T005b to verify FR-012) directly addresses this; my review does not.

**Resolution needed**: The "10 FRs" claim must be explicitly enumerated. Both reviews agree the count is opaque; they disagree on whether the gap is low-impact (scope-boundary: P3) or unaddressed (compliance-auditor: not flagged at all). I concede scope-boundary identified a verification gap my audit missed.

### 2. STATUS.md Baseline Verification — Required or Not

**scope-boundary** (Recommendation 3) argues that Phase 1 should verify STATUS.md's current state because Phase 2 tasks T006/T007 depend on it. scope-boundary proposes adding T005a to verify STATUS.md exists with entries for specs 001-004. Priority: P2.

**compliance-auditor** does not flag STATUS.md baseline verification at all. My review verifies FRs against SKILL.md and template files — the two artifact families that Phase 1 tasks explicitly target. I treat STATUS.md as out of Phase 1 scope because no Phase 1 task references it.

This is a contradiction about what Phase 1's verification boundary should be. scope-boundary treats Phase 1 as responsible for verifying all preconditions of downstream phases. I treat Phase 1 as responsible only for the FRs explicitly assigned to its tasks. The spec's assumption (L275) that STATUS.md "exists with basic per-spec status" is untested by either interpretation of Phase 1, but scope-boundary considers this a problem while I do not. scope-boundary's position is the more conservative one — if a precondition is assumed but unverified, the gate is weaker.

### 3. T019 Behavioral Change — Scope Leak or Intentional Enhancement

**scope-boundary** (Recommendation 7) focuses on Phase 3/Phase 4 parallel safety, noting that cross-file reads could break the parallel execution model. scope-boundary treats T019's cross-reference replacement as a scoping concern — will the replacement cause one phase to read the other's target file?

**compliance-auditor** (Recommendation 3, Missed Opportunity on structural-marker support) treats T019 as a behavioral change concern — the cross-reference introduces structural-marker support and case-insensitive heading matching that the inline logic did not have. I recommend T019's task description explicitly document these two behavioral expansions.

These are not merely different perspectives — they conflict on what the primary risk of T019 is. scope-boundary sees T019 as a parallel-safety risk (does it break the Phase 3/4 isolation?). I see T019 as a semantic-expansion risk (does it change what the system parses?). Both risks are real, but they lead to different recommendations. scope-boundary recommends a precondition note on the Parallel Example section. I recommend a behavioral-change note on T019's task description. If only one recommendation is adopted, the other risk goes undocumented.

---

## Tensions

### 1. Granularity of Pass/Fail Criteria

**scope-boundary** (Recommendation 1) calls for explicit pass/fail criteria on every Phase 1 task — e.g., "FAIL if marker is absent, on wrong line, or has different syntax." Priority: P2.

**compliance-auditor** provides implicit pass/fail by citing exact file locations and matching them against FR text (e.g., "All three non-cooperative arbitration templates contain `<!-- CONVERSUS:TEMPLATE_STATUS: draft -->` as their first line"). My review is itself the pass/fail determination, but does not propose formalizing criteria into the tasks document.

The tension: scope-boundary wants criteria embedded in the tasks for any future verifier; I produced a one-time audit that serves as the verification record but does not make the tasks self-documenting. Both are valid — scope-boundary's approach is more durable (any future re-run of Phase 1 would be unambiguous), while mine is sufficient for this execution. The practical question is whether Phase 1 will ever re-run. If it does (e.g., after a SKILL.md edit in Phase 4 shifts content), scope-boundary's criteria become essential.

### 2. Line Number Fragility — Severity Disagreement

**scope-boundary** (Recommendation 2) calls line number references in T002 and T003 a P2 issue and recommends replacing them with section heading references.

**compliance-auditor** (Alignment, T002 and T003 sections) uses the same line numbers (L249, L581) as verification evidence without flagging them as fragile. My review implicitly validates the line numbers as currently correct but does not note that they will drift.

The tension is about time horizon. For a single-pass audit (my approach), current line numbers are perfectly reliable evidence. For a living tasks document that may be re-executed after Phase 2-4 edits (scope-boundary's concern), they are fragile. Both assessments are correct for their respective time horizons. I acknowledge scope-boundary's concern is the more forward-looking one.

### 3. Negative Verification (Cooperative Template)

**scope-boundary** (Recommendation 4) notes that T001 should explicitly verify the cooperative template does NOT have a draft marker, citing acceptance scenario AS4 (spec.md L23). Priority: P3.

**compliance-auditor** (Alignment, T001/FR-001) actually performed this negative check: "The cooperative template (L1) correctly does NOT have the marker." However, I did this as part of my audit, not because T001 instructed it.

The tension: the negative check was performed but is not encoded in the task definition. If a different auditor runs Phase 1 using only the task descriptions, they would not perform the negative check. scope-boundary is right that the task description should include it; I am right that the check passes. The gap is in task specification, not in verification outcome.

### 4. FR-002 Error Message Mismatch — Severity Assessment

**compliance-auditor** (Off-Base Assumptions, Recommendation 1) flags that FR-002's specified error message is a strict subset of the actual SKILL.md L249 message (which appends "This template requires a separate game-dynamics analysis spec before activation"). I recommend updating FR-002 to match. Priority: P2.

**scope-boundary** does not flag this mismatch at all. scope-boundary's T002 verification (Alignment section) confirms the draft marker check exists with "correct error message" without noting the superset/subset discrepancy.

The tension: is a superset match a pass or a discrepancy? From a strict compliance perspective, the implementation exceeds the spec — which is usually acceptable but creates a documentation drift. scope-boundary implicitly treats it as a pass. I flag it as a documentation concern. Neither position is wrong, but they reflect different audit philosophies: scope-boundary audits for scope containment, I audit for spec-implementation correspondence.

### 5. FR-011 Partial Scope — Single Site vs. Dual Site

**compliance-auditor** (Off-Base Assumptions) flags that spec.md L278 only mentions Round Termination Check as the site of inline parsing, but Trigger Evaluation (L531-542) is also an inline-parsing site. I recommend expanding the assumption.

**scope-boundary** (Alignment section) notes FR-011's partial status is "acknowledged" and correctly deferred, but does not flag the single-site vs. dual-site discrepancy in the spec assumption.

The tension: scope-boundary focuses on whether the boundary between Phase 1 and Phase 4 is clean (it is — T004 reads, T019/T019a write). I focus on whether the spec's own assumption text is accurate (it is not — it omits Trigger Evaluation). Both are correct within their review mandates. The tasks document handles both sites (T019 + T019a), so the operational risk is low, but the spec text is imprecise.

---

## Safe Agreements

### 1. Phase 1 Is Correctly Scoped as Read-Only

**scope-boundary** (Alignment, first item): "All five Phase 1 tasks use the verb 'Verify' and describe reading existing files to confirm FR satisfaction. No task instructs the agent to create, edit, or delete any file."

**compliance-auditor** (Executive Summary): "Its Phase 1 work is strictly verification: confirming that 10 functional requirements previously implemented in SKILL.md and the template files remain correct."

Both reviews independently confirm that Phase 1 contains no write operations, no file creation, and no scope creep. The phase boundary between verification (Phase 1) and implementation (Phases 2-4) is clean.

### 2. FR-011 Remediation Is Correctly Deferred to Phase 4

**scope-boundary** (Alignment, fourth item; Recommendation 6): "Phase 1 reads and notes the gap; Phase 4 writes the fix. ... This boundary is correctly drawn."

**compliance-auditor** (Alignment, FR-011 partial): "Round Termination (L459-469) and Trigger Evaluation (L531-542) both use inline parsing; remediation deferred to T019/T019a."

Both reviews confirm that FR-011's partial status is properly handled: Phase 1 verifies the gap exists as expected, Phase 4 remediates it, and no Phase 1 task attempts a premature fix. The two reviews agree on the facts even though they emphasize different aspects (scope-boundary emphasizes boundary cleanliness, I emphasize the dual-site nature of the gap).

### 3. Phase Dependency Chain Is Sound

**scope-boundary** (Alignment, fifth item): "Phase 1 has no dependencies. Phase 2 depends on Phase 1. Phase 3 depends on Phase 2. Phase 4 depends on Phase 1 (not Phase 2 or 3). Phase 5 depends on Phases 3 and 4. No circular dependencies exist."

**compliance-auditor** does not explicitly audit the dependency chain (it is outside my FR-verification mandate), but my review implicitly relies on it — I verify Phase 1 FRs without needing any Phase 2-4 output. The dependency model holds under both reviews.

### 4. STATUS.md Staleness After T019 Is a Real Risk

**scope-boundary** (Recommendation 7) warns that Phase 3 and Phase 4 parallel execution could create scope leaks if one phase reads the other's target file, noting that T008's STATUS.md entry about stagnation detection will become inaccurate after T019.

**compliance-auditor** (Recommendation 4) explicitly flags this: "T008 creates an entry that T019 invalidates. Without a task to update it, STATUS.md becomes stale immediately." I recommend adding a post-T019 update task.

Both reviews identify the same staleness risk through different analytical lenses. scope-boundary arrives at it via parallel-safety analysis (what if the phases interact?). I arrive at it via temporal-consistency analysis (T008's content becomes false after T019). The convergence strengthens the case that a STATUS.md update task after T019 is necessary.
