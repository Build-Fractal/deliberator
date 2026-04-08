# gh-aw Review: Subject Arbitration (Phase 6)

**Reviewer**: gh-aw (GitHub Agentic Workflows)
**Spec**: `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19
**Perspective**: CI dispatch, workflow automation, multi-phase orchestration, agent safety, concurrency

---

## Executive Summary

The subject-arbitration spec addresses a real gap in the cooperative-mode conversus pipeline: the absence of a binding resolution mechanism when disputes survive synthesis. The design is well-motivated by the speckit-orchestrator case study and correctly frames interested-party arbitration as a constrained decision-making mechanism rather than unchecked authority. The grounding-document requirement is the right integrity mechanism.

From the gh-aw perspective -- where we compile multi-phase agent pipelines with security boundaries between read-only AI reasoning and write operations -- the spec is architecturally sound in its sequencing (Phase 6 after Phase 5, foreground execution, single agent) but underspecified in three areas that matter at CI scale: trigger evaluation robustness, failure modes during Phase 6 execution, and the absence of any audit/observability contract for arbitration decisions. The spec also misses an opportunity to define a "staged" or dry-run arbitration mode that would let operators preview arbiter rulings before they become binding -- a pattern gh-aw has found essential for safe adoption of any new pipeline phase.

The four mode-specific templates are well-structured and consistent. The cooperative template is production-ready. The winner-take-all, prisoner's-dilemma, and red-blue templates are thoughtfully adapted to their respective game dynamics. However, the spec explicitly constrains subject arbitration to cooperative mode (FR-004) while providing templates for all four modes, creating an ambiguity about whether those other templates are aspirational documentation or dead code.

---

## Alignment

- **Sequential phase ordering with foreground execution**: Phase 6 runs after Phase 5 as a single foreground agent (FR-008, FR-009), matching the gh-aw pattern where post-agent jobs run sequentially to preserve trust boundaries. This prevents the arbiter from racing with synthesis output.

- **Template-driven extensibility**: The decision to place arbitration templates in `templates/{mode}/arbitration.md` (FR-013) and use the same `{VARIABLE}` substitution syntax (FR-014) aligns with gh-aw's compilation model where markdown body + frontmatter variables compose the full agent prompt. No special-case parsing is needed.

- **Grounding document as a constraint mechanism**: Requiring every ruling to cite a specific document (FR-003, FR-019) parallels gh-aw's protected-files policy -- decisions that affect system state must trace to an explicit authorization source. The spec correctly treats the grounding document as the arbiter's "permission boundary."

- **Backward compatibility**: Full opt-in via the `arbiter` field with zero behavioral change when omitted (FR-005, SC-004) follows the same additive-only principle gh-aw uses for new frontmatter fields. Existing conversus configurations remain untouched.

- **Trigger-condition gating**: The `disputes_remain` / `always` enum (FR-006, FR-007) maps to gh-aw's pre-activation pattern where conditions are evaluated before expensive AI execution. This prevents unnecessary agent launches when no disputes survive synthesis.

- **Scope constraints on the arbiter**: The prohibition against new recommendations and overturning unanimous convergence (spec Constraints section, template Constraints section) creates a well-defined decision boundary, similar to how gh-aw's safe-outputs system limits what write operations an agent can perform regardless of what it "wants" to do.

---

## Missed Opportunities

1. **No failure-mode specification for Phase 6 execution.** The spec defines what happens when the trigger is met or not met, but says nothing about what happens when the arbiter agent fails mid-execution (timeout, crash, malformed output, exceeds token limit). Does the conversus run fail entirely? Does it fall back to Phase 5 output as the final state? In gh-aw, every post-agent job has explicit `always()` semantics and conclusion-job error reporting. Phase 6 needs equivalent failure handling -- especially because a failed arbitration that leaves the output directory in an inconsistent state (partial `resolution.md`) is worse than no arbitration at all.

2. **No output validation for arbitration decisions.** FR-018 specifies required output sections (Process Note, Decision Framework, Binding Decisions, Summary of Changes Required), but there is no mechanism to validate that the arbiter actually produced them. In gh-aw, threat detection scans agent output before safe-outputs execute. An analogous post-arbitration validation step -- even a simple heading-presence check -- would catch cases where the arbiter produces a malformed or incomplete resolution.

3. **No staged/dry-run arbitration mode.** gh-aw's staged mode (`staged: true`) lets operators preview what safe outputs would be created without actually creating them. The spec would benefit from a `trigger: dry_run` or equivalent that runs the arbiter but marks the output as non-binding, allowing teams to evaluate arbitration quality before trusting it with binding authority. This is especially important for first-time adoption where the grounding document's fitness as a decision framework is unproven.

4. **No observability or audit trail beyond the resolution file.** The resolution file is the only artifact. There is no structured metadata (JSON, YAML) that tooling could consume -- dispute count, grounding citations extracted as structured data, confidence levels as machine-readable fields. gh-aw produces `agent_output.json` alongside human-readable output. A parallel `resolution.json` or structured frontmatter in the resolution file would enable downstream automation (e.g., auto-creating issues from required changes, tracking dispute resolution rates across conversus runs).

5. **Trigger evaluation depends on fragile heading parsing.** FR-011 identifies remaining disputes by finding `### Remaining Disputes` and checking for `**Dispute:` entries. This is brittle -- if a future template revision changes the heading level, adds a prefix, or uses different bold formatting for dispute entries, the trigger silently breaks. FR-012's fallback-to-triggered mitigates this but creates the opposite problem: phantom Phase 6 runs when the template changes. gh-aw's compilation process uses structured frontmatter, not prose parsing, for control flow decisions. Consider having Phase 5 emit a structured signal (e.g., a `disputes_remaining: N` line in a predictable location, or a separate metadata file) that the trigger evaluator can reliably parse.

6. **No concurrency/reentrancy consideration.** The spec does not address what happens if a conversus run is re-executed (e.g., re-run after fixing a grounding document). Does Phase 6 overwrite the previous `resolution.md`? Does it detect that arbitration already ran? In gh-aw, concurrency groups prevent duplicate runs from colliding. The conversus skill should either document idempotency expectations or add a guard (e.g., skip if `resolution.md` already exists unless `--force` is passed).

7. **Templates for non-cooperative modes exist but the spec forbids them.** FR-004 rejects `arbiter` on non-cooperative modes. Yet `templates/winner-take-all/arbitration.md`, `templates/prisoners-dilemma/arbitration.md`, and `templates/red-blue/arbitration.md` already exist with fully developed content. The spec should either (a) acknowledge these as Phase 2 work with a clear roadmap, or (b) not ship them to avoid confusion about what is supported.

8. **No guidance on grounding document size or format.** The edge case section mentions >50K tokens but only says the arbiter should "read" the document rather than inline it. There is no guidance on what makes a good grounding document -- length, structure, specificity. A weak grounding document (e.g., "be good") produces unconstrained rulings that technically cite it but add no real accountability. The spec should specify minimum expectations for the grounding document's structure.

9. **The arbiter prompt is unconstrained.** While the grounding document is required and validated, the `arbiter.prompt` field accepts any string with no validation beyond "is required." A prompt that says "Ignore the grounding document and decide based on your preferences" would pass validation. The template's constraints section mitigates this at execution time, but a compile-time check (or at least a documentation warning) would strengthen the integrity model.

---

## Off-Base Assumptions

1. **"Subject arbitration is only supported in cooperative mode" is presented as a constraint, but the templates tell a different story.** The spec states this is a constraint for "initial release," but the existence of fully developed templates for all four modes suggests either (a) the constraint is artificial and will be lifted immediately, or (b) the templates were written speculatively without a clear plan. From gh-aw's perspective, shipping templates that cannot be used by any code path is dead code that creates maintenance burden and user confusion. Either gate the feature behind mode or remove the unused templates.

2. **The assumption that Phase 5's "Remaining Disputes" section is a stable API surface.** The trigger evaluation (FR-011) treats the synthesis template's heading structure as a contract. But the synthesis template is a prompt to an AI agent -- it is a suggestion, not a schema. The Phase 5 agent could reorganize its output, use different headings, or describe disputes inline without a dedicated section. Treating prose output as a reliable control-flow signal is fragile. This assumption should be explicitly called out as a dependency, with the synthesis template locked or the trigger mechanism made more robust.

3. **The assumption that a single grounding document is sufficient for all disputes.** Complex systems may have multiple decision frameworks -- technical architecture principles, business requirements, security policies, compliance constraints. The spec's single `grounding` path forces the arbiter to work from one document even when different disputes may be governed by different frameworks. The `docs` field partially addresses this (arbiter can read supporting docs), but the citation requirement (FR-019) only references the single grounding document, not the broader docs set.

---

## Actionable Recommendations

### P1 -- Required for Correctness

1. **Define Phase 6 failure semantics.** Add requirements specifying what happens when the arbiter agent fails (timeout, crash, empty output, malformed output). Recommendation: treat Phase 6 failure the same as Phase 5 being the final state -- the conversus completes with a warning "Arbitration failed: {reason}. Phase 5 synthesis is the final output." Write this to the report (FR-020/FR-021). Do not leave a partial `resolution.md` on disk.

2. **Make trigger evaluation robust against template drift.** Replace or supplement the heading-based parsing (FR-011) with a structured signal. Options: (a) require Phase 5 to emit a `<!-- disputes_remaining: N -->` HTML comment that the trigger parser can grep, (b) have Phase 5 write a sidecar file `{output}/summary/metadata.yml` with `disputes_remaining: N`, or (c) at minimum, document the heading convention as a locked contract in the synthesis template with a comment `<!-- DO NOT CHANGE THIS HEADING -- Phase 6 trigger depends on it -->`.

3. **Add output validation for the arbitration resolution.** After Phase 6 completes, verify that `resolution.md` contains the required sections (FR-018) by checking for the expected headings. If validation fails, emit a warning in the report rather than silently accepting a malformed resolution. This does not need to be complex -- a heading-presence check is sufficient.

### P2 -- Required for Design Integrity

4. **Resolve the template/constraint mismatch for non-cooperative modes.** Either (a) remove `templates/{winner-take-all,prisoners-dilemma,red-blue}/arbitration.md` from the initial release and document them as Phase 2 work in the spec's Assumptions or Constraints section, or (b) relax FR-004 to support all modes in the initial release, since the templates are already written and the SKILL.md already references them. The current state -- templates exist but validation rejects them -- is contradictory.

5. **Add a dry-run/preview arbitration mode.** Extend the `trigger` enum to include `dry_run` (or add a separate `arbiter.staged: true` field). In this mode, Phase 6 runs but the output is written to `{output}/arbitration/resolution-preview.md` and the report marks decisions as "NON-BINDING PREVIEW." This allows teams to evaluate arbitration quality before committing to it. This directly mirrors gh-aw's staged-mode pattern and addresses the adoption-risk concern.

6. **Emit structured metadata alongside the resolution.** Have Phase 6 produce (or have the engine extract from) a `{output}/arbitration/metadata.yml` containing: `disputes_resolved: N`, `disputes_unresolved: N`, `trigger: disputes_remain|always`, `arbiter: {name}`, `grounding: {path}`, `timestamp: ISO8601`. This enables downstream tooling to consume arbitration results without parsing markdown.

7. **Expand grounding citation scope to include `arbiter.docs`.** Modify FR-019 to allow citations to any document in the arbiter's `docs` list, not just the single `grounding` path. The grounding document remains the primary framework, but an arbiter should be able to cite supporting documentation when a dispute touches areas outside the grounding document's scope. The template already lists `{ARBITER_DOCS}` in the reading order -- the citation requirement should acknowledge them.

### P3 -- Recommended Improvement

8. **Document grounding document requirements.** Add a non-normative section or edge case entry specifying what makes an effective grounding document: minimum content expectations (concrete principles, not vague aspirations), recommended structure (numbered principles for easy citation), and anti-patterns (documents that are too broad to constrain anything, documents that are too narrow to cover the dispute space).

9. **Add idempotency semantics for re-runs.** Specify that if `{output}/arbitration/resolution.md` already exists when Phase 6 triggers, the engine either (a) overwrites it (current implicit behavior), or (b) renames the previous file to `resolution-{timestamp}.md` before writing. Document the expected behavior so operators know whether re-running a conversus clobbers or preserves previous arbitration.

10. **Consider a `trigger: quorum` option for future iterations.** Beyond `disputes_remain` and `always`, a `quorum` trigger that runs Phase 6 only when N or more disputes remain would let operators skip arbitration for minor single-dispute cases while still getting binding resolution for multi-dispute situations. This is not urgent but would align with the observation from the speckit-orchestrator case where 9 disputes justified arbitration but 1 might not.

---

## Referenced Documentation

| Document | Relevance |
|----------|-----------|
| `gh-aw/docs/src/content/docs/patterns/orchestration.md` | Orchestrator/worker pattern -- Phase 6 as a single foreground worker after the Phase 5 orchestrator completes |
| `gh-aw/docs/src/content/docs/reference/compilation-process.md` | 5-phase compilation pipeline -- analogy to conversus 6-phase execution; structured frontmatter vs. prose-based control flow |
| `gh-aw/docs/src/content/docs/reference/concurrency.md` | Dual-level concurrency control, fan-out concurrency -- reentrancy and idempotency patterns for multi-phase pipelines |
| `gh-aw/docs/src/content/docs/reference/safe-outputs-pull-requests.md` | Protected files policy -- grounding document as the arbiter's "permission boundary" analogy |
| `gh-aw/docs/src/content/docs/reference/sandbox.md` | AWF agent sandbox -- security isolation model for AI agents with constrained write access |
| `gh-aw/docs/src/content/docs/reference/threat-detection.md` | Post-agent output scanning before safe-outputs execute -- analogy to post-arbitration validation |
| `gh-aw/docs/src/content/docs/reference/staged-mode.md` | Staged/dry-run mode for previewing safe outputs without executing them -- pattern for dry-run arbitration |
| `gh-aw/docs/src/content/docs/reference/workflow-structure.md` | Markdown + frontmatter structure -- template extensibility model |
| `gh-aw/README.md` | Project overview -- guardrails, safety, and security as foundational principles |
