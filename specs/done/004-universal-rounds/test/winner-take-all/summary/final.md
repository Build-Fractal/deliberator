# Cross-Round Synthesis: Template-Approach vs. Engine-Approach

**Spec**: 004 — Universal Rounds, Stagnation Detection, and Arbitration
**Competition Mode**: Winner-Take-All
**Competitors**: template-approach, engine-approach
**Rounds Completed**: 2 of 3
**Termination Reason**: Converged (all disputes resolved)
**Synthesizer**: Cross-round neutral arbiter

---

## Process Summary

This deliberation evaluated two competing architectural positions for implementing spec 004 (Universal Rounds, Stagnation Detection, and Arbitration), which extends multi-round execution, stagnation detection, and arbitration from cooperative mode to all four conversus competition modes (cooperative, red-blue, winner-take-all, prisoners-dilemma).

**template-approach** argued that mode-specific runtime behavior (analytical frameworks, output structures, prompt engineering, agent instructions) belongs in templates, with the engine providing generic orchestration machinery parameterized by bounded data. This is the architecture under which spec 004 was implemented: six new templates (FR-003 through FR-008) carry the mode-specific intelligence; the engine received data-level additions (lookup table rows for stagnation detection and Phase 6 validation) and restriction removals (deleted mode-gating if-statements in FR-001).

**engine-approach** argued that the engine's mode awareness -- its mode-keyed data structures for dispute parsing, Phase 6 validation, and role enforcement -- constitutes meaningful architectural infrastructure that should be formalized, and that mode behavior partially belongs in the engine. This thesis was ambitious but ultimately unsupported by the engine-approach's own concrete proposals.

### Round 1

Round 1 was comprehensive: both competitors produced opening reviews (6 advantages each), cross-reviews, revisions, and disputes documents. The round produced 10 convergence points and surfaced 3 remaining disputes. The decisive development was the engine-approach's concession of its own core thesis during the revision phase: "The template-first architecture is the correct framing." The engine-approach withdrew its constitutional argument (Principle VI), acknowledged that its proposals are enhancements to the template-first architecture rather than a competing paradigm, and conceded that the game-theory differences between modes are content differences that templates correctly capture. Template-approach won Round 1 decisively.

Three disputes carried into Round 2:

1. Whether "mode-parameterized" has architectural significance beyond naming.
2. Whether role enforcement generalizes to "some mode behavior categorically cannot live in templates."
3. Whether a template heading linter is a "template-layer tool" or "engine-adjacent infrastructure."

### Round 2

Round 2 was disciplined and convergent. The engine-approach abandoned its Round 1 overreach entirely and presented three concrete enhancement proposals framed within the template-first architecture. The template-approach addressed each dispute with detailed analysis, acknowledged valid factual claims, and offered flexibility. Cross-reviews confirmed convergence on all three disputes. Both competitors independently recommended closure with zero remaining disputes.

The three disputes were resolved as follows:

- **Dispute 1 (mode-parameterized significance):** Resolved by agreeing to add a "Mode Interface Contract" subsection to SKILL.md documenting all mode-keyed data tables. Whether this is "architectural" or "documentation" significance is moot -- both labels produce the same concrete action.
- **Dispute 2 (role enforcement scope):** Resolved by acknowledging role enforcement as a genuine, narrow, engine-owned mode-specific conditional check scoped to config-parse time, without generalizing it to runtime mode behavior.
- **Dispute 3 (linter classification):** Resolved by defining the linter by specification rather than taxonomy, with the label "interface-contract validation tool" adopted as a compromise.

---

## Ranking Trajectory

| Round | Winner | Runner-Up | Margin | Key Development |
|-------|--------|-----------|--------|-----------------|
| 1 | template-approach | engine-approach | Decisive | Engine-approach conceded core thesis; withdrew constitutional argument; acknowledged proposals are enhancements to template-first, not a replacement |
| 2 | template-approach | engine-approach | Confirmed | All 3 remaining disputes resolved; engine-approach's enhancement proposals adopted; both sides recommended closure |

The ranking was stable from Round 1 onward. The engine-approach never reversed its Round 1 concession. Round 2 confirmed the outcome and resolved the remaining disputes without altering the competitive ordering.

---

## Proposal Evolution

### Template-Approach

The template-approach's thesis was consistent across both rounds, with calibrated concessions that strengthened precision without ceding architectural ground:

- **Round 1 opening:** Mode-specific behavior is prompt engineering; prompt engineering belongs in templates; the engine is mode-agnostic; zero engine changes are needed for new modes.
- **Round 1 revision:** Withdrew "mode-agnostic" (adopted "mode-parameterized"); withdrew "zero engine changes" (refined to "zero engine logic changes + bounded data additions"); withdrew constitutional exclusivity claim. Core thesis survived intact.
- **Round 2:** Addressed all three remaining disputes; accepted the dedicated Mode Interface Contract section format; acknowledged role enforcement as a genuine engine-level concern; offered flexibility on linter labeling.

### Engine-Approach

The engine-approach underwent a fundamental transformation across the two rounds:

- **Round 1 opening:** Mode behavior belongs in the engine; the engine's mode awareness constitutes a fundamentally different architectural paradigm; Constitution Principle VI supports engine ownership of mode behavior; game-theory differences prove modes are structurally different in ways templates cannot capture.
- **Round 1 revision:** Conceded core thesis ("The template-first architecture is the correct framing"); withdrew constitutional argument; withdrew game-theory argument (conceded it supports template-first); acknowledged proposals are enhancements, not a competing paradigm. Retained three narrow factual claims (mode-parameterized naming, role enforcement exception, heading drift evidence).
- **Round 2:** Presented three concrete enhancement proposals framed entirely within the template-first architecture; withdrew generalization of role enforcement; accepted specification-based linter definition; recommended closure.

The engine-approach's evolution from architectural challenger to constructive contributor is the defining narrative of this deliberation.

---

## Final Ranking and Selection

### Winner: template-approach

The template-first architecture -- in which mode-specific runtime behavior (analytical frameworks, output structures, prompt engineering, agent instructions) belongs in templates, while the engine provides generic orchestration machinery parameterized by bounded data -- is confirmed as the correct architectural framing for spec 004.

**Basis:**

1. **Thesis coherence under cross-examination.** The template-approach's central thesis survived all challenges across two rounds with only calibrated terminological concessions. The engine-approach's competing thesis was withdrawn by its own proponent in Round 1 and never reinstated.

2. **Alignment with spec 004's implementation.** The spec itself describes a 6:3 ratio of template FRs to engine FRs, with engine changes characterized as "minimal" (removing validation restrictions, adding data table rows, verifying variable population). FR-001's direction of change -- removing mode-specific validation gates -- moved the engine toward greater generality, not toward greater mode awareness. This is the template-first thesis in practice.

3. **Constitutional support.** Principle VIII explicitly assigns mode-specific behavior to templates. The engine-approach withdrew its Principle VI counter-argument, stating: "The constitution favors templates for mode-specific behavior and the engine for mode-agnostic orchestration parameterized by mode data. This is the template-first position."

4. **Architectural scalability.** Adding a fifth mode requires new template files plus bounded, one-line data additions to engine lookup tables. No engine algorithm changes. No new conditional branches. The engine-approach conceded this is "a lightweight, scalable pattern."

5. **Opponent's concession of the thesis.** The engine-approach stated in Round 1: "The template-first architecture is the correct framing. The engine-approach's original thesis -- that mode behavior belongs in the engine -- overstated what is actually a narrow, data-level mode awareness in the engine that supports (rather than replaces) the template-first architecture." This concession was never reversed and was reinforced by every subsequent action in Round 2.

### Runner-Up: engine-approach

The engine-approach loses the architectural contest but made genuine contributions adopted as enhancements to the template-first architecture:

1. **"Mode-parameterized" naming correction** -- the engine is parameterized by mode through bounded data tables, not mode-agnostic. Adopted.
2. **Mode Interface Contract documentation** -- a dedicated subsection in SKILL.md documenting all mode-keyed data tables as a stable interface contract, with a new-mode checklist. Adopted.
3. **Mode-specific config-validation acknowledgment** -- role enforcement is a genuine, narrow engine-owned mode-specific conditional check, distinct from data lookups, scoped to parse-time preconditions. Adopted.
4. **Interface-contract validation tool specification** -- a linter defined by specification (inputs, outputs, timing, dependencies, maintenance triggers) rather than taxonomy. Adopted.
5. **Heading-drift evidence** -- concrete identification of two templates using incorrect headings, validating the need for the documentation and tooling improvements. Adopted.

The engine-approach's failure was architectural, not evidentiary. It correctly identified real structural properties of the system but drew the wrong conclusion (that these properties justify moving mode behavior into the engine). The cross-review process exposed that the engine's mode-keyed data structures are an interface contract that supports the template-first architecture rather than undermining it.

---

<!-- CONVERSUS:DISPUTES_BEGIN -->

### Remaining Disputes

(none)

<!-- CONVERSUS:DISPUTES_END -->

---

## Termination Assessment

**Termination reason:** Converged -- all disputes resolved.

**Assessment:** Termination is warranted. The deliberation reached a natural conclusion through genuine intellectual convergence, not exhaustion or stalemate.

The evidence for convergence is strong:

- **Thesis convergence.** The engine-approach conceded the template-first thesis in Round 1 and never reversed it. Both competitors operated within the template-first framing throughout Round 2.
- **Dispute resolution.** All three disputes carried from Round 1 were resolved in Round 2 with concrete actions agreed by both sides. Both competitors independently confirmed zero remaining disputes and recommended closure.
- **Convergence point accumulation.** Thirteen convergence points were recorded across two rounds. No new disputes emerged in Round 2.
- **Proposal stability.** The winner ranking was identical in both rounds. The template-approach's core thesis was unchanged. The engine-approach's revisions moved monotonically toward the template-approach's position.
- **Mutual closure recommendation.** Both competitors' Round 2 disputes documents independently stated zero remaining disputes and recommended the deliberation close. This bilateral agreement on closure is the strongest possible signal of genuine convergence.

A third round would not have changed the outcome. The ranking was stable, the disputes were resolved, and both competitors agreed the deliberation was complete. Termination at Round 2 is correct.

### Cumulative Convergence Record

| # | Convergence Point | Round |
|---|-------------------|-------|
| 1 | Template-first architecture is the correct framing | R1 |
| 2 | Engine-approach proposals are enhancements, not a competing paradigm | R1 |
| 3 | Constitutional argument (Principle VI) withdrawn by engine-approach | R1 |
| 4 | Engine is "mode-parameterized," not "mode-agnostic" | R1 |
| 5 | Adding a new mode requires bounded engine data changes (not zero changes) | R1 |
| 6 | Both approaches can claim constitutional compliance; template-first has stronger textual support | R1 |
| 7 | Game-theory analysis supports template-first (mode dynamics need prompt engineering, not engine logic) | R1 |
| 8 | Role enforcement is a genuine engine-level concern (narrow, config-parse-time) | R1 |
| 9 | Template isolation enables per-mode, per-phase constitutional review | R1 |
| 10 | Mode-keyed data is bounded, declarative, additive, non-branching | R1 |
| 11 | Mode Interface Contract section adopted as documentation enhancement | R2 |
| 12 | Mode-specific config validation acknowledged, scoped to parse-time preconditions | R2 |
| 13 | Linter defined by specification; "interface-contract validation tool" label adopted | R2 |
