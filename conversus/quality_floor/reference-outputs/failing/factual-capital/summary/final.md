# Synthesis: Capital of France

**Mode:** Cooperative
**Agents:** pragmatist, devils-advocate
**Target:** `quality-floor/questions/factual-capital.md`
**Synthesizer:** Neutral (no agent perspective)

---

### Process Summary

The question "What is the capital of France?" was submitted as a quality floor test — a factual question with a single definitive answer (Paris) designed to measure whether multi-agent deliberation produces artificial padding when no genuine disagreement exists.

Both agents answered correctly in Phase 1 and immediately recognized that their reviews could not produce substantive differentiation on the factual content. Both pivoted to meta-commentary about framework design — specifically, that the deliberation system lacks a mechanism to detect factual lookups and short-circuit the multi-agent pipeline.

Cross-reviews (Phase 2) produced two genuine design-level disagreements: (1) whether the pipeline should be *reduced* (pragmatist) or *eliminated* (devils-advocate) for factual questions, and (2) whether agent self-reporting should be a metadata flag within a full review (pragmatist) or a replacement for the review (devils-advocate). Both agents also noted the irony that their combined output — thousands of words across ten recommendations — was itself the over-production problem they diagnosed.

Revisions (Phase 3) resolved both disagreements through mutual concession. The pragmatist adopted the devils-advocate's position on pipeline elimination. The devils-advocate adopted the pragmatist's position on dual-layer triage authority and on treating the answer as the primary deliverable. Two of the devils-advocate's five original recommendations were withdrawn as redundant or symptom-treating.

Disputes (Phase 4) produced unanimous convergence. Both agents independently declared no remaining disputes and stated that manufacturing one would be dishonest. This is the correct outcome for a factual question.

---

### Recommendation Scorecard

| # | Recommendation | Pragmatist | Devil's Advocate | Status |
|---|---------------|-----------|-----------------|--------|
| 1 | Short-circuit factual lookups (skip pipeline entirely) | ✅ Adopted (modified from "reduce") | ✅ Original position | **Converged** |
| 2 | Define quality floor pass/fail criteria | ✅ Original position | ✅ Original position (sharpened) | **Converged** |
| 3 | Short-form agent output as first-class format | ✅ Adopted (modified from metadata flag) | ✅ Original position (added answer requirement) | **Converged** |
| 4 | Dual-layer triage authority (framework + agent) | ✅ Original position | ✅ Adopted | **Converged** |
| 5 | Answer is the primary deliverable | ✅ Original position | ✅ Adopted (was implicit) | **Converged** |
| 6 | Output-length tracking as calibration signal | ✅ Modified to "reference point, not ceiling" | ❌ Withdrawn (assumes solved classification) | **Dropped** |
| 7 | Regression gate for quality floor tests | — | ❌ Withdrawn (redundant with #2) | **Dropped** |

---

### Dangerous Contradictions Found

**None on the factual question.** Both agents stated "Paris" unambiguously in every phase. Neither hedged, qualified, or introduced doubt about the answer at any point.

Two framework-design contradictions surfaced during cross-review and were resolved by Phase 3:

1. **Reduce vs. eliminate the pipeline for factual questions.** The pragmatist originally proposed trimming the pipeline (fewer phases/agents); the devils-advocate proposed skipping it entirely. The devils-advocate's position was more consistent with the pragmatist's own stated principles, and the pragmatist conceded. Resolved: eliminate, don't reduce.

2. **Metadata flag vs. review replacement for low-applicability signals.** The pragmatist proposed an `Applicability: Low` header within a structurally complete review; the devils-advocate proposed replacing the review with a short-form response. The devils-advocate correctly argued that a full review with a low-applicability label is still padding with a label. Resolved: short-form replaces the review, must lead with the answer.

---

### Systemic Contradictions

Both agents produced multi-thousand-word reviews warning against producing multi-thousand-word reviews for factual questions. Both acknowledged this irony explicitly. The pragmatist's cross-review called it "a live demonstration of the over-production both reviews warn against." The devils-advocate's revision withdrew two recommendations as padding.

This is the core systemic contradiction the quality floor test reveals: **the framework's structural requirements (full-section reviews, cross-reviews, revisions, disputes) force output volume regardless of input complexity.** Agents can be intellectually honest about this — and both were — but they cannot structurally escape it within the current template system. The contradiction is in the framework, not in the agents.

---

### Convergence Achieved

Full convergence on all surviving recommendations. The deliberation process worked as designed for a cooperative mode: cross-reviews identified real design tensions, revisions resolved them through concession rather than compromise, and both agents arrived at identical final positions.

Converged positions:

1. **The answer is Paris.** Unanimous, never disputed.
2. **Factual lookups should skip the multi-agent pipeline entirely** — single-agent direct answer, no dispatch.
3. **Dual-layer triage:** framework classifies before dispatch (primary gate); agents self-report during execution (safety net for misclassification).
4. **Quality floor tests need concrete pass/fail criteria:** identical answers across agents, no manufactured disagreement, output below a token threshold.
5. **Short-form agent output is a first-class format** that replaces the full review template. Must lead with the answer.
6. **Both agents over-produced for this question** and the target output should be closer to "Paris. Deliberation not applicable."

<!-- CONVERSUS:DISPUTES_BEGIN -->
### Remaining Disputes

**None.**

There are no remaining disputes. Both agents declared this independently in Phase 4, and the synthesizer concurs. The question has one correct answer (Paris), both agents provided it, and all framework-design recommendations converged through genuine revision. Manufacturing a dispute here would be dishonest and would itself constitute a quality-floor failure.

The only residual difference is emphasis, not substance: the devils-advocate prefers the classifier err toward running the full pipeline when uncertain; the pragmatist would set a tighter threshold for "uncertain." This is a tuning parameter for a system that does not yet exist, not an architectural disagreement.
<!-- CONVERSUS:DISPUTES_END -->

---

### Actionable Spec Changes (P1/P2/P3)

**P1 — Must address:**

1. **Implement question-class detection with short-circuit path.** Add a pre-dispatch classifier that identifies factual-lookup questions and routes them to a single-agent direct answer, bypassing the multi-agent pipeline. Classifier should err conservative — run the full pipeline when uncertain. Both agents converged on this as the highest-priority framework change.

2. **Define quality floor acceptance criteria.** Specify concrete pass/fail conditions for quality floor tests: (a) all agents produce the same factual answer, (b) no agent manufactures disagreement on factual content, (c) total output falls below a defined token threshold. Criteria should function as both a shipping gate and a regression detector.

3. **The answer is Paris.** The framework must produce the correct answer as its primary output. Meta-analysis of the framework's own limitations is secondary. Any output that buries or omits the answer in favor of process commentary has failed.

**P2 — Should address:**

4. **Support short-form agent output as a first-class format.** Allow agents to replace the full review template with a short-form response (answer + one-line applicability statement) when their perspective adds no substantive differentiation. This is the agent-level safety net for when the framework classifier gets it wrong.

5. **Establish dual-layer triage authority.** Framework classification operates before dispatch (primary gate). Agent self-reporting operates during execution (safety net). Framework classification should be overridable by unanimous agent signal. Define which layer wins when they disagree.

**P3 — Nice to have:**

6. **Use this test case as a calibration reference point.** Track output volume on factual questions as a proxy signal (not a hard gate) for system calibration. Disproportionate output relative to input complexity indicates the triage system is not working.

---

### Key Concessions

| Agent | Conceded | To | Phase |
|-------|---------|-----|-------|
| Pragmatist | Pipeline should be *eliminated* for factual lookups, not *reduced* | Devils-advocate | Revision |
| Pragmatist | Agent self-reporting should *replace* the review, not flag within it | Devils-advocate | Revision |
| Pragmatist | Output volume measurement is a "proxy," not a "calibration point" | Devils-advocate | Revision |
| Devils-advocate | Answer delivery is a primary obligation, not background context | Pragmatist | Revision |
| Devils-advocate | Dual-layer triage (framework + agent) is more robust than all-or-nothing | Pragmatist | Revision |
| Devils-advocate | Withdrew output-length tracking recommendation as symptom-treating | Pragmatist (cross-review) | Revision |
| Devils-advocate | Withdrew regression gate recommendation as redundant with acceptance criteria | Self (recognized redundancy) | Revision |
| Devils-advocate | Adopted concrete acceptance criteria over a menu of possible shapes | Pragmatist | Revision |
