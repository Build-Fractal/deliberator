# Spec-Kit Cross-Review of gh-aw's Review

**Cross-reviewer**: spec-kit (SDD framework)
**Reviewed review**: gh-aw review of Subject Arbitration (Phase 6)
**Date**: 2026-03-19
**Purpose**: Identify dangerous contradictions, productive tensions, and safe agreements between spec-kit and gh-aw perspectives.

---

## Dangerous Contradictions

These are points where gh-aw and spec-kit make incompatible recommendations that, if both followed, would produce an incoherent design.

### DC-1: Trigger robustness — structured signal vs. locked heading contract

gh-aw recommends replacing the heading-based trigger with a structured signal: an HTML comment (`<!-- disputes_remaining: N -->`), a sidecar metadata file, or at minimum a locked-heading comment in the template (gh-aw P1-2). Spec-kit recommends elevating the heading convention from an assumption to a constraint with a template validation step that checks for the heading's presence during template loading (spec-kit P1-3).

These pull in opposite directions. gh-aw wants to **abandon prose parsing** in favor of a machine-readable side-channel. Spec-kit wants to **harden the prose parsing** by enforcing the heading as a locked structural invariant. If both are implemented, Phase 5 would be required to emit both a structured signal AND a locked heading — redundant mechanisms that can drift out of sync. Worse, if the structured signal says `disputes_remaining: 0` but the heading section contains dispute entries (or vice versa), the system has two conflicting sources of truth for Phase 6 trigger evaluation.

**Resolution needed**: Pick one canonical trigger source. The structured signal (gh-aw's approach) is more robust for CI automation. The locked heading (spec-kit's approach) is more natural for human-readable synthesis output. The spec must choose a primary trigger source and, if it keeps both, define which one wins on conflict.

### DC-2: Output format philosophy — structured metadata alongside vs. structured block within

gh-aw recommends a sidecar `metadata.yml` file alongside `resolution.md` containing machine-readable fields: `disputes_resolved`, `disputes_unresolved`, `trigger`, `arbiter`, `grounding`, `timestamp` (gh-aw P2-6). Spec-kit recommends a YAML front matter or fenced code block **inside** `resolution.md` with structured summaries of each dispute ruling: ID, ruling type, grounding citation, required change (spec-kit P1-1).

These are architecturally contradictory. gh-aw wants resolution metadata **external** to the resolution document, consumed by downstream pipeline tooling. Spec-kit wants resolution metadata **embedded** in the resolution document, consumed by `/speckit.specify --input`. If both are implemented, machine-readable arbitration data lives in two places with overlapping but non-identical schemas. A downstream tool must know which file to read, and the data can diverge if one is updated and the other is not.

**Resolution needed**: Define a single canonical location for structured arbitration data. Either the sidecar file is the machine-readable source and `resolution.md` stays human-readable, or `resolution.md` carries its own structured block and no sidecar is produced. The spec cannot ship both without defining which is authoritative.

### DC-3: Scope of the arbiter's citation obligations

gh-aw recommends expanding FR-019 to allow citations to any document in the arbiter's `docs` list, not just the single `grounding` path (gh-aw P2-7). The argument: different disputes may be governed by different frameworks, and restricting citations to one document is artificially narrow. Spec-kit recommends the opposite emphasis: that `arbiter.grounding` SHOULD be the spec-kit constitution, and the citation requirement should stay anchored to that single grounding document as the primary constraint mechanism (spec-kit P2-6).

These contradict on what makes rulings legitimate. gh-aw broadens the citation scope to increase flexibility — the arbiter can cite architecture docs, security policies, or business requirements as the dispute demands. Spec-kit narrows it to increase accountability — the constitution is the single source of decision authority, and diluting citations across arbitrary docs weakens the constraint model. If both are followed, the arbiter can cite anything in its docs list (gh-aw) but SHOULD anchor to a single constitution (spec-kit), creating an ambiguous "should but can" that undermines the grounding document's role as a hard constraint.

**Resolution needed**: Either expand citation scope with a clear hierarchy (grounding document is primary, supporting docs may be cited only when the grounding document is silent on the matter), or keep citations strictly tied to the grounding document and treat supporting docs as read-only context that informs reasoning but cannot be cited as authority.

---

## Tensions

These are points where gh-aw and spec-kit disagree on priority, emphasis, or approach, but the disagreements are productive rather than destructive.

### T-1: Failure semantics — pipeline resilience vs. output correctness

gh-aw prioritizes defining failure modes explicitly: what happens on arbiter crash, timeout, or malformed output. The recommendation is to fall back to Phase 5 output as the final state and write a warning to the report (gh-aw P1-1). Spec-kit does not address failure modes at all — its focus is on making the successful output more useful to downstream SDD workflows.

The tension is between **graceful degradation** (gh-aw's CI-pipeline lens: the run must always produce a valid terminal state) and **output fidelity** (spec-kit's SDD lens: what matters is that the output is machine-consumable and traceable). Both are valid. The risk of prioritizing only gh-aw's concern: the spec defines how to fail gracefully but not how to succeed usefully. The risk of prioritizing only spec-kit's concern: the spec defines rich output but has no plan for when that output is not produced.

**Productive resolution**: Address both. Failure semantics (gh-aw) protect the pipeline. Structured output (spec-kit) makes success valuable. These are complementary, not competing — but the spec must sequence them (P1 for failure semantics since correctness precedes richness).

### T-2: Dry-run/staged mode vs. confidence-based follow-up

gh-aw recommends a dry-run arbitration mode where the arbiter runs but output is marked non-binding, allowing teams to evaluate arbitration quality before trusting it (gh-aw P2-5). Spec-kit recommends defining behavior for Low-confidence rulings — when the arbiter is uncertain, the ruling should include a follow-up action (spec-kit P1-4).

These address the same underlying concern (trust in arbitration quality) through different mechanisms. gh-aw's approach is binary: the entire arbitration run is either binding or preview. Spec-kit's approach is granular: individual rulings carry confidence levels that determine whether follow-up is needed. The tension: a dry-run mode makes ALL rulings non-binding even if the arbiter is highly confident on most, while confidence-based behavior trusts the arbiter's self-assessment, which may be unreliable for a new arbitration mechanism.

**Productive resolution**: These can coexist. Dry-run mode serves the adoption phase (first few runs). Confidence-based follow-up serves the steady-state phase (arbitration is trusted but individual rulings vary in certainty). The spec should clarify that dry-run is an operational safeguard and confidence is a per-ruling quality signal — different layers.

### T-3: Non-cooperative template status — remove vs. acknowledge

Both reviews flag the same issue (non-cooperative templates exist but FR-004 forbids their use), but the recommendations differ in tone. gh-aw leans toward removal: "shipping templates that cannot be used by any code path is dead code" (gh-aw Off-Base #1). Spec-kit leans toward acknowledgment: "define their status (draft/experimental/future)" and "define what validation error they trigger" (spec-kit P2-5).

The tension reflects different engineering philosophies. gh-aw's CI perspective penalizes dead code — it creates maintenance burden and confuses automated tooling that discovers templates. Spec-kit's SDD perspective values preparatory design — the templates document intent and reduce future implementation cost. Neither is wrong; the question is whether the spec is a production shipping manifest (gh-aw) or a design roadmap (spec-kit).

### T-4: What makes the arbiter legitimate — information asymmetry vs. decision authority

Both reviews challenge the spec's assumption that "subject arbitration is only meaningful when the deliberation agents represent external perspectives and the subject has its own distinct operational perspective." gh-aw frames this as an off-base assumption about the templates telling a different story (gh-aw Off-Base #1). Spec-kit directly reframes it: legitimacy comes from decision authority constrained by a grounding document, not from information asymmetry (spec-kit Off-Base #1, P2-7).

The tension: gh-aw's critique is practical (the templates already exist for non-cooperative modes, so the constraint is artificial). Spec-kit's critique is philosophical (the framing of WHY arbitration works is wrong, regardless of which modes support it). Both weaken the assumption, but they weaken different parts of it.

### T-5: Per-file attribution vs. structured pipeline metadata

Spec-kit recommends per-file attribution in binding decisions when multiple target files are involved (spec-kit P3-8) — the arbiter should say which target file each ruling affects. gh-aw recommends structured metadata at the run level (gh-aw P2-6) — dispute counts, timestamps, trigger conditions. These are complementary granularities (per-ruling vs. per-run), but they compete for implementation priority and both want the output format to accommodate their structure. Implementing both without coordination risks an overloaded output format that serves neither consumer well.

---

## Safe Agreements

These are points where both reviews converge without contradiction, making them high-confidence recommendations.

### SA-1: The trigger evaluation mechanism (FR-011) is fragile and must be hardened

gh-aw calls it "brittle heading parsing" and recommends structured signals (gh-aw Missed Opportunity #5, P1-2). Spec-kit calls it "cross-template coupling" and recommends elevating the convention from assumption to constraint (spec-kit Missed Opportunity #3, Off-Base Assumption #2, P1-3). They disagree on the fix (see DC-1), but they fully agree on the diagnosis: treating Phase 5 prose output as a reliable control-flow signal is the spec's most dangerous fragility. Both reviews independently classify this as P1. The spec must address this regardless of which hardening mechanism is chosen.

### SA-2: The non-cooperative mode template/constraint mismatch must be resolved

gh-aw flags it as an off-base assumption and a missed opportunity (gh-aw Off-Base #1, Missed Opportunity #7, P2-4). Spec-kit flags it as a missed opportunity (spec-kit Missed Opportunity #8, P2-5). Both agree the current state — fully developed templates that validation rejects — is contradictory and must be resolved before shipping. The disagreement on resolution approach (remove vs. acknowledge) is a tension (T-3), but the agreement that the status quo is unacceptable is unanimous.

### SA-3: Backward compatibility and opt-in design are correct

gh-aw endorses the additive-only principle: zero behavioral change when `arbiter` is omitted (gh-aw Alignment, point 4). Spec-kit endorses the same: "every extension is additive and never changes the default behavior" (spec-kit Alignment, point 6). Neither review raises any concern about FR-005 or SC-004. This is a settled design decision that both perspectives validate.

### SA-4: The grounding document requirement is the right integrity mechanism

gh-aw calls it the arbiter's "permission boundary" and draws a parallel to protected-files policy (gh-aw Alignment, point 3). Spec-kit calls it a direct parallel to the spec-kit constitution pattern (spec-kit Alignment, point 1). Both reviews affirm that requiring citation of a declared framework is what makes interested-party arbitration legitimate rather than arbitrary. No disagreement on the mechanism — only on its scope (DC-3).
