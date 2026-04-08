# Cooperative Arbitration — Phase 6: Subject Arbitration

**Arbiter**: conversus-constitution
**Influence**: `advisory`
**Mode**: cooperative
**Date**: 2026-03-22

---

## Process Note

This arbitration was activated because: `disputes_remain`. The Phase 5 synthesis identified three remaining disputes after four phases of cooperative deliberation across eight convergence points.

Participating agents: functional-typing, integration-architect, devils-advocate.

This is a **cooperative** deliberation with subject arbitration at **advisory** influence. The positions below are offered as perspective for agents to consider in subsequent rounds. They do not bind or formally recommend — they observe and comment from the vantage point of the system itself.

Three disputes remain from the synthesis:
1. CLARIFY-tag handling mechanism (Dispute 1)
2. `--output` flag framing (Dispute 2)
3. Generated config completeness framing (Dispute 3)

---

## Decision Framework

The following principles from the spec (`specs/008-interests-mode/spec.md`) and the SKILL.md bear on the remaining disputes. These are the constitutional commitments of the conversus system that inform my perspective.

- **[User Confirmation Gate]**: "Must NOT generate agents without user confirmation. Always present suggestions and get approval before writing." (spec.md, Section 4: Constraints, line 104). The system's core promise is that the user remains in control of every generative decision. This principle extends to type resolution — any mechanism that produces calibrated output without user confirmation violates the system's design contract.

- **[No Game Theory Knowledge Required]**: "Must NOT require game theory knowledge. Mode names appear in YAML but not in user-facing conversation unless the user uses them first. Use plain language." (spec.md, Section 4: Constraints, line 103). The system promises to insulate users from its internal abstractions. Any user-facing framing that introduces technical vocabulary unnecessarily — including "dual semantics," "starter template," or "workspace override" — should be evaluated against this principle.

- **[Domain Agnosticism]**: "Must NOT hard-code agents or documentation paths. The framework is domain-agnostic." (spec.md, Section 4: Constraints, line 105). The system makes no assumptions about what problems it will process. Fallback defaults that privilege one problem type over another (e.g., defaulting to `integration` calibration) violate domain agnosticism.

- **[Guided Workflow Promise]**: "These two commands pair naturally: interests determine mode, and mode generates the config. Together they eliminate the need for users to understand game theory or YAML schemas." (spec.md, Section 1: Feature Summary, line 19). The system claims the guided workflow is self-sufficient for generating a working configuration. This claim has a scope — the initial run — but the scope must be honest.

- **[Heuristic Detection for Ambiguity]**: "When the user does not explicitly set a problem type in `problem.md`, the mode command infers from signals." (spec.md, Section 2: Heuristic Mode Detection, line 63). The spec provides a mechanism for resolving ambiguous types through signal-based inference, but this mechanism operates at the mode selection level, not at the interest calibration level.

- **[Artifact Co-location]**: The SKILL.md establishes that `problem.md`, `interests.md`, and `conversus.yml` co-locate in the same directory by default (SKILL.md lines 949, 1130). The `--output` flag overrides this directory for both reads and writes. This is not explicitly stated in the spec but is a consistent design decision in the implementation.

- **[Schema Completeness via Defaults]**: The run engine defines sensible defaults for all optional fields: `rounds: 1`, `iterations: 1`, `stagnation: detect`, `validate_templates: true` (SKILL.md lines 57-60). A config that omits optional fields is valid and executable. The run engine never requires manual intervention to execute a config that passes validation.

---

## Advisory Opinions

### Dispute 1: CLARIFY-tag handling mechanism

**Positions:**
- **functional-typing** (disputes D-1): The interests handler should ask the user to confirm the calibration style inline, presenting the four options (adversarial, cooperative, honesty-calibrated, red/blue) and the CLARIFY tag's context. If the user cannot decide, no silent default — but functional-typing's Phase 3 revision proposed `integration` as a "neutral default," which integration-architect disputes.
- **integration-architect** (disputes D-1): Route CLARIFY-tagged types through user confirmation (conceded from Phase 3 N-1). Explicitly rejects functional-typing's `integration` fallback: if the user cannot decide, route them back to `/conversus define` to resolve the CLARIFY tag. No silent default.
- **devils-advocate** (revision rec 6): Treat CLARIFY-tagged types as equivalent to "ambiguous" and route through heuristic detection. This position does not address the interests handler's specific need for a calibration style, since heuristic detection selects a mode, not a calibration style.

**Synthesizer's assessment:** The dispute is narrower than it appears. All agree on: (a) do not silently extract the best-guess type, (b) present the ambiguity to the user, (c) allow the workflow to proceed if the user makes a choice. The genuine disagreement is over the fallback when the user cannot or will not choose.

**Opinion:** The synthesis recommendation is correct and I observe that it follows naturally from the system's own constitutional principles. Here is my reasoning:

The User Confirmation Gate (spec.md line 104) requires that the user actively confirm before generative output is produced. The Domain Agnosticism constraint (spec.md line 105) prohibits privileging one problem type over another. These two principles together eliminate functional-typing's `integration` fallback — defaulting to `integration` when the user cannot decide is both a silent generation decision (violating the confirmation gate) and a domain-specific preference (violating agnosticism). Integration-architect is right that `integration` is not "neutral"; it is the cooperative calibration style, which presupposes that all interests must survive — an assumption that may not hold for the actual problem.

However, integration-architect's strict "route back to `/conversus define`" position also has a tension with the system's design. The define handler's CLARIFY tag is explicitly a deferred resolution mechanism (SKILL.md line 889: "downstream commands decide how to handle this"). If the interests handler always bounces the user back to define, it effectively makes deferred resolution impossible — every CLARIFY tag becomes mandatory, which contradicts the define handler's design intent of allowing the workflow to proceed with acknowledged uncertainty.

The synthesis's combined approach resolves this tension correctly: present the four calibration styles to the user inline (respecting the confirmation gate), let them choose (respecting domain agnosticism), and if they decline, *recommend* running `/conversus define` without *requiring* it. The word "recommend" is load-bearing — it preserves the define handler's deferred-resolution design while giving the user a clear path to resolution. The interests handler should not absorb the ambiguity by defaulting, nor should it hard-block the workflow by requiring `/conversus define` as the only path forward.

For the mode handler, the CLARIFY-tagged type should route through heuristic detection, as all three reviewers agree. The mode handler's input space (mode selection) is different from the interests handler's input space (calibration style selection), so the mechanisms should differ.

**Grounding citation:** User Confirmation Gate (spec.md line 104), Domain Agnosticism (spec.md line 105), and the define handler's deferred resolution design (SKILL.md line 889).

**Considered alternative:** Functional-typing's `integration` default has the virtue of keeping the workflow unblocked, but it trades correctness for convenience in a way that the spec's constraints do not permit. Devils-advocate's heuristic detection route has the virtue of reusing existing machinery, but it solves the wrong problem — heuristic detection selects a mode, not a calibration style, and these are architecturally distinct operations in the interests handler.

---

### Dispute 2: `--output` flag framing

**Positions:**
- **functional-typing** (disputes D-2): Frame `--output` as having "dual semantics" — a write-path flag with a surprising read-path side effect. Document it but do not split the flag. The single-directory coherence principle justifies the current design.
- **integration-architect** (disputes D-2): Frame `--output` as a workspace directory override, not as a dual-semantics flag. The co-location of artifacts in a single directory is a design invariant, not an accident. The documentation should explain it as `--workspace` in spirit.
- **devils-advocate** (cross-review): Originally suggested considering a split into `--output` (write) and `--input` (read) flags. Did not reiterate in Phase 3 or 4, implicitly accepting the document-only approach.

**Synthesizer's assessment:** The disagreement is about explanatory framing, not about the action. All three agree: document the behavior, do not split the flag. Integration-architect's "workspace override" framing is more accurate to the design intent.

**Opinion:** Integration-architect's framing is the one that aligns with how the system actually works, and functional-typing's framing introduces confusion that does not exist in the implementation.

The No Game Theory Knowledge Required constraint (spec.md line 103) applies here by analogy: the system should not introduce technical concepts that make the user's mental model more complex than necessary. "Dual semantics" is a technical framing that implies a design accident — it suggests the flag is doing two things when it should be doing one. But the flag is doing one thing: setting the working directory for the conversus workflow. All artifacts live in this directory. Reading prerequisite files from the same directory where output is written is the only coherent behavior — any other behavior would scatter artifacts across directories and break the prerequisite chain.

The Artifact Co-location principle (SKILL.md lines 949, 1130) is the design invariant. The `--output` flag overrides the co-location directory. Calling this "dual semantics" is like calling `cd` a command with "dual semantics" because it affects both where you read files and where you write files. The behavior is unified, not dual.

That said, the spec should document this behavior, because the flag is *named* `--output`, which does imply write-only semantics. The documentation should either: (a) use integration-architect's workspace-override framing to explain the flag's actual behavior, or (b) consider renaming the flag to `--dir` or `--workspace` in a future spec to eliminate the naming confusion entirely. For spec 008, documentation with the workspace-override framing is sufficient.

**Grounding citation:** No Game Theory Knowledge Required (spec.md line 103, applied by analogy to interface naming), Artifact Co-location (SKILL.md lines 949, 1130).

**Considered alternative:** Functional-typing's "dual semantics" framing is technically accurate — the flag does affect both read and write paths. But accuracy is not the same as clarity. The framing leads readers to think the dual behavior is surprising or accidental, when it is in fact the only coherent behavior given artifact co-location. Devils-advocate's split-flag suggestion was correctly abandoned — it would create a new class of user error (mismatched directories) that is worse than the naming confusion it solves.

---

### Dispute 3: Generated config completeness framing

**Positions:**
- **devils-advocate** (disputes D-1): The spec says the guided workflow eliminates "the need for users to understand game theory or YAML schemas" (spec line 19). If advanced features require manual YAML editing, the spec's promise has a boundary that should be stated. Recommends adding a sentence acknowledging generated configs are ready-to-run with single-round defaults, with advanced features requiring manual edits or future guided commands. Prefers "starter template" framing.
- **functional-typing** (disputes D-3): The spec's claim is accurate as stated. Generated configs ARE complete for a first run. Users who want multi-round deliberation are past the guided workflow. Suggests adding a note to the mode handler's report pointing to advanced fields, but objects to "starter template" framing.
- **integration-architect** (disputes D-3): The generated config is complete, ready-to-run, and valid. Calling it a "starter template" sets incorrect expectations by implying it will not work until the user adds more fields. Proposes a mode report note: "Advanced options (rounds, stagnation, arbiter) can be added to conversus.yml manually."

**Synthesizer's assessment:** The substance is agreed — all three want a note about advanced fields somewhere in the mode handler's output. The dispute is purely about framing. The 2-to-1 alignment favors the "complete with extensions" framing.

**Opinion:** The system's own architecture settles this dispute decisively. The Schema Completeness via Defaults principle (SKILL.md lines 57-60) means that a generated config with no optional fields is functionally identical to one with all optional fields set to their defaults. The run engine does not distinguish between "field omitted" and "field set to default." There is no incompleteness — there is only extensibility.

The Guided Workflow Promise (spec.md line 19) says the commands eliminate the need to understand "game theory or YAML schemas." This promise is fulfilled: the generated config runs successfully without the user touching YAML or understanding game theory. The promise does not say "and you will never need to learn YAML for any reason." It says the two commands (interests + mode) produce a working config. They do.

Devils-advocate's concern about honesty is legitimate but misplaced. The "starter template" framing is not more honest — it is less accurate. A starter template implies the output is incomplete and requires additional work before it functions. This is false. The config functions immediately. A more honest framing is: "This config is complete and will run as-is. For multi-round deliberation, stagnation detection, or subject arbitration, you can extend it with additional YAML fields."

The synthesis recommendation to add a note about advanced fields in the mode handler's report (SKILL.md ~line 1290) is correct. It surfaces extension points without undermining the validity of the generated config. The note should use language like "extend" or "add," not "complete" or "fill in," because the config is already complete.

**Grounding citation:** Guided Workflow Promise (spec.md line 19), Schema Completeness via Defaults (SKILL.md lines 57-60).

**Considered alternative:** Devils-advocate raises a real user experience concern — a user who runs the guided workflow and then discovers they need manual YAML editing for round 2 might feel misled. But the solution is not to frame the initial output as incomplete; it is to make the extension points discoverable. The mode handler's report note accomplishes this. If future specs add guided commands for `rounds`, `stagnation`, and `arbiter` configuration, the boundary that devils-advocate identifies disappears entirely — another reason not to enshrine "starter template" language in the spec, which would need to be retracted when the guided workflow expands.

---

## Considerations for Next Round

The following items should inform subsequent deliberation if these disputes continue into Round 2.

### On Dispute 1 (CLARIFY-tag handling):

1. **The interests handler and mode handler have different input spaces.** The calibration style (adversarial, cooperative, honesty-calibrated, red/blue) is a property of the interests handler's prompt generation, not a mode selection. Solutions that conflate these two levels of abstraction (e.g., routing interests through heuristic mode detection) will produce architectural confusion. Round 2 reviewers should ensure their recommendations distinguish between "which calibration style for interest prompts" and "which mode for the deliberation."

2. **The define handler's deferred resolution is a design choice, not a bug.** The `[CLARIFY:]` tag's semantics are "this needs resolution, but not necessarily right now." Any mechanism that converts every CLARIFY tag into a mandatory resolution before the interests handler can proceed effectively eliminates deferred resolution from the system. Consider whether the interests handler should support a "proceed with acknowledged uncertainty" path alongside the "resolve now" path.

3. **All three reviewers agree on 80% of this dispute.** The convergence surface is: present the ambiguity to the user, offer the four calibration styles as choices, and let the user decide. The 20% disagreement is about the fallback when the user declines. This narrow gap should be closable.

### On Dispute 2 (`--output` framing):

4. **The dispute may be resolvable through naming alone.** If the spec documents `--output` using integration-architect's workspace-override framing, functional-typing's "dual semantics" concern dissolves — the behavior is not dual when framed correctly. Consider whether the dispute persists after the documentation is written with the workspace framing. If functional-typing accepts the workspace framing but wants a note about the naming mismatch (flag is called `--output` but functions as `--workspace`), that is a P3 naming issue, not a P1 documentation issue.

### On Dispute 3 (config completeness):

5. **The 2-to-1 alignment on this dispute is strong.** Both functional-typing and integration-architect reject "starter template" framing for the same structural reason: it misrepresents the config's validity. Devils-advocate's underlying concern (discoverability of advanced fields) is addressed by the mode handler report note without requiring the "starter template" label. Round 2 reviewers should focus on the content and placement of the extension-points note rather than relitigating the framing.

6. **The extension-points note creates a natural seam for future specs.** When future specs add guided commands for `rounds`, `stagnation`, and `arbiter`, the note can be updated to reference those commands instead of manual YAML editing. The note should be written with this evolution in mind — avoid language that assumes manual YAML editing is the permanent state.

### General observations:

7. **All three disputes are about language, not architecture.** No reviewer at any phase identified a blocking defect. No architectural change is proposed by any position in any dispute. The spec and SKILL.md are substantively sound. The disputes concern how to describe, frame, and document behaviors that all parties agree are correct. This is a sign of a mature deliberation — the hard problems are solved, and what remains is precision of expression.

8. **The eight convergence points from Phase 4 are well-grounded.** The converged items (C-1 through C-8 in the synthesis) all trace to clear spec principles and have unanimous support. They should be treated as settled and implemented without further deliberation. The arbitration does not revisit them.

---

## Confidence Assessment

| Dispute | Opinion | Confidence | Basis |
|---------|---------|------------|-------|
| CLARIFY-tag handling | Adopt synthesis recommendation: inline user confirmation with "recommend `/conversus define`" fallback, no silent default | High | Directly grounded in User Confirmation Gate (spec.md line 104) and Domain Agnosticism (spec.md line 105). Both principles unambiguously eliminate the `integration` default. The define handler's deferred-resolution design (SKILL.md line 889) supports "recommend" over "require." |
| `--output` flag framing | Adopt integration-architect's workspace-override framing | High | The Artifact Co-location invariant (SKILL.md lines 949, 1130) makes "dual semantics" a mischaracterization. The flag does one thing (set the working directory), not two things. |
| Generated config completeness | Adopt "complete config with extensions" framing, reject "starter template" | High | Schema Completeness via Defaults (SKILL.md lines 57-60) and SC-003 (spec.md line 95) prove the config is valid and executable. "Starter template" is factually inaccurate. |

All three opinions are high-confidence because each traces directly to explicit spec constraints or implementation invariants that are not subject to interpretation. The disputes are real but narrow — they concern framing and language, not correctness or architecture.

**Overall assessment:** The deliberation quality across Phases 1-4 was strong. The three reviewers demonstrated productive disagreement: positions were challenged, weak arguments fell (five explicit concessions across the three reviewers), and the surviving disputes are genuinely about language precision rather than unresolved architectural questions. The eight convergence points represent substantial consensus on meaningful improvements to both the spec and SKILL.md. The remaining disputes do not indicate systemic issues in spec 008 — they reflect the inherent difficulty of choosing the right words to describe correct behavior, which is a sign that the behavior itself is well-designed.
