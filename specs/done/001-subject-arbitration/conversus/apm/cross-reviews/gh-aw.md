# APM Cross-Review of gh-aw's Review: Subject Arbitration

**Cross-reviewer**: APM (Agent Package Manager)
**Reviewing**: gh-aw's review of `conversus/specs/001-subject-arbitration/spec.md`
**Date**: 2026-03-19

---

## Dangerous Contradictions

### DC-1: Dry-run mode undermines the binding-decision contract

gh-aw recommends adding a `trigger: dry_run` or `arbiter.staged: true` mode that produces non-binding preview rulings (gh-aw P2-5). This directly contradicts the spec's core value proposition. The entire integrity model rests on a single concept: the arbiter's rulings are binding *because* they are grounded in a cited document. Introducing a "non-binding" variant creates a category of arbitration output that looks like a ruling, reads like a ruling, but carries no authority. Downstream consumers (spec-kit's `/speckit.specify`, APM's compile pipeline, gh-aw's own issue-creation automation) would need to distinguish binding from non-binding resolutions -- a distinction the spec's output format was never designed to carry. Worse, operators who leave `staged: true` on permanently get the cost of Phase 6 (an additional agent launch) with none of the value (no disputes actually resolved). The adoption-risk concern gh-aw raises is real, but the correct mitigation is a low-stakes first run (a small conversus with few disputes), not a shadow mode that fragments the output contract. APM's own approach to this problem -- running `apm compile --dry-run` to preview file changes -- works because file operations are idempotent and reversible. Arbitration rulings are neither; a "preview ruling" is a contradiction in terms.

### DC-2: Structured metadata sidecar vs. the single-artifact output model

Both gh-aw (P2-6) and APM (P3-9) recommend emitting structured metadata alongside `resolution.md` -- gh-aw proposes `metadata.yml`, APM proposes `resolution.summary.yml`. But gh-aw goes further and frames this as required for design integrity (P2), while APM treats it as a recommended improvement (P3). The contradiction is not between the reviews but between gh-aw's recommendation and the spec's deliberate single-artifact output model. The spec produces one file per phase per agent. Phase 5 produces `final.md`. Phase 6 produces `resolution.md`. Introducing a sidecar file breaks this convention and creates a new failure mode: what happens when `resolution.md` and `metadata.yml` disagree? The arbiter produces one document; any structured extraction should be a post-processing step by the engine, not a requirement on the LLM agent to produce two consistent artifacts simultaneously. gh-aw's own threat-detection system scans a single `agent_output.json` -- it does not ask the agent to produce both prose and structured output. The engine should extract metadata from the resolution, not ask the arbiter to emit it.

### DC-3: Trigger robustness recommendations create competing contracts

gh-aw (P1-2) proposes three options for making trigger evaluation robust: HTML comments in the synthesis output (`<!-- disputes_remaining: N -->`), a sidecar metadata file (`metadata.yml`), or a locked-heading contract. APM (P1-2) proposes HTML markers (`<!-- CONVERSUS:DISPUTES_BEGIN -->` / `<!-- CONVERSUS:DISPUTES_END -->`). Both reviews correctly identify the fragility of heading-based parsing, but the solutions are incompatible. gh-aw's `disputes_remaining: N` comment is a scalar signal (count); APM's begin/end markers are a structural signal (content boundaries). A scalar count enables the trigger check but gives Phase 6 no way to extract *which* disputes remain. Structural markers enable both the trigger check and content extraction but impose a more invasive contract on the Phase 5 template. Implementing both would create two parallel contracts for the same information. The reviews agree on the problem but their solutions, if both adopted, would create a worse situation than the current heading convention -- two fragile contracts instead of one. A single mechanism must be chosen, and it should be the structural markers (APM's approach) because they serve both trigger evaluation and dispute extraction for the proposed `{REMAINING_DISPUTES}` variable.

---

## Tensions

### T-1: Scope of non-cooperative mode support

Both reviews identify the cooperative-only restriction (FR-004) as contradicting the delivered templates. gh-aw frames this as "dead code that creates maintenance burden" (Off-Base Assumptions #1) and recommends either gating or removing. APM frames it as "delays value delivery" (Missed Opportunities #4) and recommends enabling all modes. The tension: gh-aw's primary concern is operational cleanliness (don't ship what you can't use), while APM's primary concern is value delivery (the templates are ready, ship them). gh-aw would accept removing the templates as a valid resolution; APM explicitly recommends against removal (Option a: enable all modes). This is a prioritization disagreement, not a factual one -- both agree the current state is contradictory.

### T-2: Whether output validation should block or warn

gh-aw (P1-3) recommends post-arbitration output validation that checks for required headings and emits a warning if validation fails. APM (P2-7) recommends post-arbitration hooks that could run validation scripts. The tension: gh-aw wants built-in validation as a correctness requirement (P1), while APM wants pluggable validation via hooks as a design-integrity feature (P2). Built-in validation is more reliable but less flexible; hook-based validation is more extensible but depends on the operator configuring it. gh-aw's approach guarantees a baseline; APM's approach enables arbitrary sophistication. The right answer is probably both -- a built-in heading-presence check (gh-aw's P1) plus hook points for custom validation (APM's P2) -- but the priority disagreement reflects genuinely different values: gh-aw optimizes for safety floors, APM optimizes for composability.

### T-3: Single grounding document vs. multiple grounding sources

APM (P2-4) recommends accepting `grounding` as a list of paths. gh-aw (P2-7) recommends expanding citation scope to include `arbiter.docs`. These are different solutions to the same problem (single grounding path is too restrictive), but they have different implications. APM's approach elevates all grounding sources to equal status -- any document in the list can anchor a ruling. gh-aw's approach preserves the hierarchy: `grounding` is the primary framework, `docs` are supplementary and can be cited but are not the decision framework. gh-aw's approach is more aligned with the spec's intent (the grounding document is *the* integrity mechanism), while APM's approach is more aligned with real-world complexity (decision frameworks span multiple documents). The tension is between preserving a clean integrity model and accommodating messy reality.

### T-4: Failure semantics -- silent degradation vs. explicit failure

gh-aw (P1-1) recommends that Phase 6 failure should fall back to Phase 5 output as the final state, with a warning. This is a degradation model: the system produces a result, just not the best possible one. APM's review does not address failure modes at all, which implicitly accepts the current spec's silence on the topic. The tension: gh-aw's degradation model is operationally pragmatic (the conversus run still produces output) but could mask systematic arbitration failures. If the arbiter consistently fails (bad prompt, unreachable grounding document, token limits), the degradation path means the operator sees warnings but never gets arbitration -- and may stop noticing the warnings. An alternative model -- fail the entire conversus run when Phase 6 fails, since the operator explicitly requested arbitration -- would be noisier but would force the operator to fix the configuration. gh-aw's CI background favors graceful degradation; a packaging perspective might favor loud failure to prevent silent drift.

### T-5: Schema versioning urgency

APM (P2-5) recommends adding `schema: 1` or `version: 1` to `conversus.yml` now, citing APM's own `apm.yml` versioning as precedent. gh-aw does not mention schema versioning at all. The tension: APM sees schema evolution as an inevitable problem that is cheapest to solve now; gh-aw, whose compilation model uses frontmatter fields that are additive-only, implicitly assumes additive evolution is sufficient. The `arbiter` field *is* additive (optional, no behavioral change when absent), which supports gh-aw's implicit position. But APM's concern is forward-looking: the next schema change may not be additive (e.g., restructuring `agents` from a list to a map), and retrofitting versioning at that point is more painful. This is a genuine philosophical tension between YAGNI and forward-compatible design.

---

## Safe Agreements

### SA-1: The grounding-document-as-constraint-mechanism is the correct integrity model

Both reviews independently validate the grounding document as the spec's strongest design decision. gh-aw compares it to their protected-files policy ("decisions that affect system state must trace to an explicit authorization source"). APM compares it to their constitution injection pattern (`memory/constitution.md` injected during `apm compile`). Both reviews agree this is what makes interested-party arbitration legitimate rather than arbitrary, and both agree the citation requirement (FR-019) is necessary and correct. Neither review suggests weakening or removing the grounding requirement.

### SA-2: Template-driven extensibility with `{VARIABLE}` substitution is the right architecture

Both reviews explicitly endorse the template-per-mode convention and the reuse of `{VARIABLE}` substitution syntax. gh-aw notes it aligns with their "markdown body + frontmatter variables" compilation model with no special-case parsing needed. APM notes it mirrors their convention-based file discovery pattern. Both reviews agree this preserves clean separation between orchestration logic and prompt engineering and makes the framework extensible without code changes.

### SA-3: The Phase 5 heading-based trigger contract is fragile and must be hardened

Both reviews independently identify FR-011's reliance on `### Remaining Disputes` heading parsing as a fragile control-flow dependency. gh-aw calls it "brittle" and notes the fallback-to-triggered creates "phantom Phase 6 runs." APM calls it a "fragile contract" that should be "formalized rather than assumed." Both reviews recommend replacing prose parsing with a machine-readable mechanism. The specific solutions differ (see Tension T-3 above regarding the competing marker proposals), but the diagnosis and urgency are fully aligned.

### SA-4: Backward compatibility is correctly preserved

Both reviews agree that the `arbiter` field's fully optional nature (FR-005, SC-004) is the right approach. gh-aw calls it "the same additive-only principle gh-aw uses for new frontmatter fields." APM calls it "the correct approach -- additive features should never break existing configurations." No caveats, no qualifications -- both reviews treat this as unambiguously correct.
