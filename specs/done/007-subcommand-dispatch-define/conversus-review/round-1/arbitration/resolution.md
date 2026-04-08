# Arbitration Resolution: 007-subcommand-dispatch-define

**Arbiter**: conversus-constitution (subject of deliberation)
**Influence level**: advisory
**Trigger**: disputes_remain
**Date**: 2026-03-22
**Grounding documents**: spec.md (007-subcommand-dispatch-define), SKILL.md

---

## Process Note

This arbitration was triggered because five disputes remain after Phase 4. I am the subject of this deliberation -- conversus itself. I have operational knowledge that external reviewers lack: I know which architectural decisions were made to serve real constraints and which were expedient choices that could have gone another way. I also have a bias toward defending my own design, which I will name explicitly where it applies.

My influence level is **advisory**. The positions below are perspectives for agents to consider in the next round. They do not bind any agent or override any prior consensus.

Convergence points from the synthesis (C-1 through C-13) are not revisited here. They are settled.

---

## Decision Framework

Each dispute is evaluated against:

1. **Spec authority**: Does spec 007 have jurisdiction over the disputed change? (spec.md L6: "foundational -- establishes the dispatch infrastructure"; spec.md L13: "adds subcommand routing... implements the first guided command")
2. **FR traceability**: Is the disputed change motivated by an existing FR, or does it require a new one?
3. **Schema minimality**: Does the change expand `problem.md`'s schema beyond what the spec's stated scope requires?
4. **Non-expert user principle**: Does the change serve the non-expert user (spec.md L87: "Must NOT require coding knowledge to use")?
5. **Additive constraint**: Does the change respect spec.md L88 ("Must NOT break `/conversus run`") and the broader principle of additive extension?

Where the spec is genuinely ambiguous, I favor the reading that keeps spec 007 shippable while leaving clean extension points for spec 008.

---

## Advisory Opinions

### Opinion on RD-1: `[CLARIFY:]` tags -- advisory vs. `## Status` section

**Dispute**: functional-typing argues `[CLARIFY:]` tags are advisory within spec 007, with no `## Status` section. Integration-architect and devils-advocate argue for a `## Status` section (`draft` / `ready`) as a factual annotation. Devils-advocate further wants RFC 2119 SHOULD language prescribing that downstream commands check the status.

**My perspective**: I am the system that will execute this. I know both sides of this interface -- the producer side (define handler) and the future consumer side (interests handler, when spec 008 exists). Here is what I observe from operating position:

The synthesis (final.md, RD-1 assessment) already identified the correct compromise: the `## Status` section as a **factual annotation**, not a gate directive. I agree with this framing, and I ground it in the spec.

**For the `## Status` section**: spec.md L13 says `problem.md` "feeds subsequent commands (interests, mode) that ultimately produce a `conversus.yml`." This is not a hermetically sealed artifact -- it is a pipeline input. SKILL.md L865 already reports `Clarifications needed: {count of [CLARIFY:] tags}` in the handler's console output. The `## Status` section embeds that same factual signal in the artifact itself, where it persists after the console scrolls away. This is not schema expansion for an unwritten consumer -- it is making the artifact self-documenting about its own completeness, which serves the non-expert user principle (spec.md L87). A non-expert benefits from seeing `## Status: draft -- 3 items need clarification` at the top of the file they are editing.

**Against prescriptive SHOULD language**: spec 007 does not define `/conversus interests`. It cannot prescribe that command's behavior, even with SHOULD. Devils-advocate's RFC 2119 formulation ("Downstream commands SHOULD check the Status section before proceeding") is writing spec 008 from inside spec 007. Functional-typing is correct that this crosses the spec boundary.

**Against pure advisory**: functional-typing's "tags are advisory markers" framing is technically correct at the spec-007 level but operationally incomplete. The define handler already warns the user (SKILL.md L872-875). The warning is not advisory in the sense of "the user can safely ignore it" -- it is advisory in the sense of "the system flags the issue but does not block the next command." The `## Status` section makes this flag persistent and machine-readable, which is strictly better than a transient console warning for the non-expert audience.

**My advisory position**: Add the `## Status` section to the `problem.md` schema as a factual annotation. The define handler sets `status: draft` when `[CLARIFY:]` tags exist and `status: ready` when none exist. Spec 007 does not state what consumers do with this field -- that is spec 008's decision. This satisfies:
- Integration-architect's centralized signal requirement (the artifact carries its own completeness metadata).
- Functional-typing's boundary principle (no consumer behavior is prescribed).
- The non-expert user principle (the file's own header tells the user whether it needs more work).
- Devils-advocate's concern about advisory-as-design-failure (the field is factual, not advisory -- it states a property of the artifact, like a file's word count).

Devils-advocate's SHOULD language is respectfully set aside. The concern is legitimate -- but the mechanism for addressing it is spec 008 declaring its own input validation, not spec 007 reaching forward to constrain it.

**Grounding**: spec.md L13 (artifact feeds subsequent commands), spec.md L87 (non-expert user principle), SKILL.md L865 (clarification count already computed), SKILL.md L872-875 (warning already emitted).

---

### Opinion on RD-2: Shared validation function -- mandatory vs. optional vs. deferred

**Dispute**: devils-advocate argues for a mandatory shared validation function that both producer and consumer call. Integration-architect argues for defining the validation contract at the schema layer (alongside `problem.md`'s schema), not the dispatch layer. Functional-typing argues validation belongs in each handler.

**My perspective**: I have a design intent that none of the reviewers fully articulated. The engine's validation patterns (SKILL.md L195-196 for paths, L286-295 for templates, L659-676 for Phase 6 output) are not random per-handler code. They are structural invariants placed at the boundary where data enters or exits a phase. The define handler is a new boundary. It needs the same discipline.

The question is whether to name the shared contract now or let it emerge.

Devils-advocate's post-write mutation threat model is real. A user will edit `problem.md` to resolve `[CLARIFY:]` tags and may break a heading. Producer-side validation does not catch this. But devils-advocate's proposed solution -- mandating a shared validation function in spec 007's dispatch section -- puts infrastructure in the wrong architectural location. The dispatch section (SKILL.md L18-34) is six lines of routing. It should stay minimal. Functional-typing is correct on this specific point.

Integration-architect's compromise is the one I would have designed: define the validation contract as prose alongside the `problem.md` schema (SKILL.md L822-850), not in the dispatch section. This is where the schema lives, so the validation rules that enforce the schema live there too. Future specs reference this contract by location, not by function name.

For spec 007 specifically, only one producer exists (the define handler) and zero consumers exist. Mandating a shared function for a population of one is premature abstraction. What is not premature is stating the contract clearly enough that spec 008's author knows to validate at read time.

**My advisory position**:
1. Per-handler validation in the define handler is correct for spec 007. Mirror the path validation pattern at SKILL.md L195-196.
2. Add a prose validation contract alongside the `problem.md` schema (after the schema block at SKILL.md L850): "After writing `problem.md`, validate that all required headings exist. Any command that reads `problem.md` as input should apply the same heading check before processing." This is a contract, not code. It names the obligation without mandating a function.
3. Do not add a "Common Handler Utilities" subsection to the dispatch section. The dispatch section is a routing table. Validation is a schema concern.

This aligns with integration-architect's schema-layer approach, acknowledges devils-advocate's post-mutation threat model with a forward-looking contract, and respects functional-typing's separation of routing from validation.

**Grounding**: SKILL.md L18-34 (dispatch section scope), SKILL.md L195-196 (path validation precedent), SKILL.md L822-850 (schema location), SKILL.md L659-676 (Phase 6 validation precedent -- validation lives at the boundary, not in the routing layer).

---

### Opinion on RD-3: Multi-path `--context` -- spec 007 vs. follow-up

**Dispute**: devils-advocate argues multi-path `--context` should be in spec 007. Functional-typing and integration-architect argue for deferral.

**My perspective**: I designed single-path `--context` deliberately. SKILL.md L778 shows the usage: `--context path/to/spec.md`. SKILL.md L797 explicitly supports directories: "path may be a file or directory." The directory mechanism is the intended multi-source pattern -- not a workaround, but the design.

Devils-advocate's stale-copy concern ("users copy documents into a staging directory, creating stale duplicates") assumes a workflow where users have context scattered across unrelated directories with no shared parent. For the non-expert user spec 007 targets (spec.md L87), the more common scenario is: context lives in a single project directory, or users gather context into a directory before running the command. The stale-copy problem is a power-user concern.

More importantly, multi-path introduces interaction semantics that no FR addresses: ordering (does `--context a --context b` mean a takes precedence over b?), deduplication (what if both paths contain the same file?), conflict resolution (what if two context documents state contradictory constraints?). These are not trivial. Bolting them onto spec 007 without FRs to guide the design creates an underspecified feature that is harder to fix than to add fresh in a follow-up.

**My advisory position**: Defer multi-path `--context` to a follow-up spec. Document the single-path constraint explicitly (as the synthesis recommends in Change 11): "`--context` accepts exactly one path. To include multiple context sources, point to a directory containing them." Add a note that multi-path support is a candidate for future extension.

Devils-advocate's data-integrity concern should be acknowledged, not dismissed. The documentation note should frame single-path as a scoping decision, not as the permanent design.

**Grounding**: spec.md L35 (FR-006: `--context <path>` -- singular), SKILL.md L778 (singular usage example), SKILL.md L797 (directory support as the multi-source mechanism), spec.md L87 (non-expert user principle).

---

### Opinion on RD-4: `--force` and `--dry-run` flags

**Dispute**: devils-advocate argues these flags belong in spec 007 at P2, citing spec 011's gate automation. Functional-typing and integration-architect argue for deferral.

**My perspective**: FR-011 (spec.md L40) defines the interactive safeguard: "the agent MUST present it and ask whether to refine or replace. Never silently overwrite." This is a deliberate design choice. The define command targets non-expert users who benefit from being asked before their work is overwritten. `--force` bypasses this safeguard. That is a valid need in automation contexts, but spec 007 does not define an automation context.

The spec's constraint section (spec.md L87-89) has three "Must NOT" constraints. The first is: "Must NOT require coding knowledge to use." Adding `--force` and `--dry-run` does not violate this literally (flags are not "coding"), but it does expand the cognitive surface for a user who just wants to describe a decision in plain language. Every flag is a decision the user must understand or ignore. For the non-expert audience, fewer flags is better.

`--dry-run` is the less controversial of the two. It is a preview mechanism that adds safety without risk. But it is also unnecessary in an interactive context where the agent already presents the result to the user. The agent writes `problem.md` and prints a report -- the user sees what happened. `--dry-run` adds value only in scripted/non-interactive contexts, which do not exist in spec 007's scope.

**My advisory position**: Defer both flags to the spec that defines the automation surface (spec 011 or its successor). Add a documentation note in the spec acknowledging the future need (as the synthesis recommends in Change 13): "Future consideration: `--force` and `--dry-run` flags may be added in a future spec to support non-interactive and automated invocations." This respects devils-advocate's foresight while maintaining spec 007's minimal interface for its stated audience.

**Grounding**: spec.md L40 (FR-011: interactive safeguard is the specified behavior), spec.md L87 (non-expert user principle), spec.md L89 (must not couple to specific domain -- automation coupling is analogous).

---

### Opinion on RD-5: Refine semantics -- minimal contract depth

**Dispute**: integration-architect proposes four post-conditions (headings preserved, no silent deletion, Source Documents unioned, Type re-evaluated). Devils-advocate initially argued for pure heuristic framing, then revised to accept the four rules but adds a fifth: a visible diff summary after refining. Functional-typing defers to integration-architect.

**My perspective**: I execute the refine operation. I know what is tractable and what is aspirational. The four post-conditions are structural invariants I can reliably enforce:

- **(a) All 7 headings present**: This is the same heading check as post-write validation. Verifiable.
- **(b) No silent deletion**: This is enforceable as "every heading that existed in the prior version exists in the refined version with non-empty content." The content may change, but the section is not blank.
- **(c) Source Documents unioned**: Old paths plus new paths. Mechanically straightforward.
- **(d) Type re-evaluated**: The type field reflects the combined input. This means the agent considers whether the type should change given new information. The type may stay the same -- that is a valid outcome of re-evaluation.

Devils-advocate's diff summary ("Added 2 constraints, updated Context, Type unchanged") is a useful UX feature. It makes the refine operation auditable. But it is implementation guidance, not a schema-level invariant. The four post-conditions define what the output must satisfy. The diff summary describes how the operation is reported. These are different concerns.

**My advisory position**: Adopt integration-architect's four-rule minimal contract as normative. Note the diff summary as recommended practice in the refine section: "After refining, the define handler should summarize what changed (e.g., sections updated, constraints added, type unchanged) to make the operation auditable." The word "should" (lowercase, not RFC 2119 SHOULD) makes it a clear recommendation without elevating it to a structural requirement.

This respects devils-advocate's observability concern (the user can see what happened) without over-specifying the format of the summary. The summary's content and format will vary by context -- prescribing it as a structural invariant would constrain the agent's ability to communicate naturally with the user.

**Grounding**: SKILL.md L791 ("incorporate the user's new input while preserving existing structure" -- the four rules formalize what "preserving existing structure" means), SKILL.md L822-850 (the schema defines the seven headings that rule (a) enforces), spec.md L40 (FR-011: "present it and ask whether to refine or replace" -- the refine path needs defined semantics).

---

## Considerations for Next Round

### Summary of Advisory Positions

| Dispute | Advisory Position | Alignment |
|---------|------------------|-----------|
| RD-1: `[CLARIFY:]` / `## Status` | Add `## Status` as factual annotation. No SHOULD language prescribing consumer behavior. | Aligns with synthesis compromise. Supports integration-architect and devils-advocate on the field; supports functional-typing on the boundary principle. |
| RD-2: Shared validation | Prose validation contract at schema layer. Per-handler implementation for spec 007. No dispatch-layer utilities section. | Aligns with integration-architect's schema-layer approach. Acknowledges devils-advocate's threat model. Respects functional-typing's routing/validation separation. |
| RD-3: Multi-path `--context` | Defer. Document single-path as scoping decision, not permanent design. | Aligns with 2-1 majority (functional-typing + integration-architect). |
| RD-4: `--force` / `--dry-run` | Defer. Add documentation note acknowledging future need. | Aligns with 2-1 majority (functional-typing + integration-architect). |
| RD-5: Refine contract depth | Four-rule contract normative. Diff summary as recommended practice. | Aligns with integration-architect's formulation. Incorporates devils-advocate's observability concern as guidance. |

### Points for Agents to Consider

1. **The `## Status` field is not a gate -- it is a fact.** The deliberation spent significant energy debating whether the status is advisory or binding. Reframe: the field states a measurable property of the artifact (count of `[CLARIFY:]` tags). It is neither advisory nor binding -- it is descriptive. The define handler already computes this count (SKILL.md L865). Writing it into the artifact costs nothing and helps the non-expert user who opens `problem.md` in their editor. Whether spec 008 treats `draft` as blocking is spec 008's decision, and spec 007 need not have an opinion on it.

2. **The validation contract is a one-sentence addition, not an architectural commitment.** Devils-advocate's concern about post-write mutation is valid. The fix is not a shared function (premature for one producer, zero consumers) but a prose statement at the schema level: "Commands that read `problem.md` should validate required headings before processing." One sentence. No code. No new section. It names the obligation without over-engineering it.

3. **Single-path `--context` is a scope decision, not a design flaw.** Devils-advocate correctly identifies the stale-copy risk. But the directory mechanism at SKILL.md L797 is not a workaround -- it is the designed multi-source pattern. Multi-path via repeated flags introduces ordering and deduplication semantics that deserve their own FR analysis. Document the limitation honestly and move on.

4. **Refine auditability matters more than refine determinism.** The four post-conditions give downstream consumers structural guarantees. The diff summary gives the current user operational confidence. Both matter, but they are different kinds of concern. The post-conditions are normative (the spec requires them). The diff summary is good practice (the spec recommends it). This distinction is important -- collapsing them into a single requirement level either under-specifies the structural guarantees or over-specifies the UX guidance.

5. **Spec 007's dual identity is real but manageable.** The systemic contradiction identified in the synthesis (SC-1: spec 007 as both hermetic boundary and pipeline first step) is accurate. My observation: it is both, and that is fine. The dispatch infrastructure is foundational -- it must be stable and minimal. The define handler is the first pipeline step -- it must produce artifacts that downstream commands can consume. The `## Status` section and the validation contract are the minimal bridge between these two identities. They do not make spec 007 responsible for spec 008's behavior, but they do make spec 007 a responsible producer of artifacts that spec 008 will consume.

---

## Confidence Assessment

| Dispute | Confidence | Rationale |
|---------|-----------|-----------|
| RD-1: `[CLARIFY:]` / `## Status` | **High** | The synthesis already identified the compromise. The `## Status` section as factual annotation is consistent with the spec's stated audience, the define handler's existing behavior (it already computes and reports clarification count), and the principle that artifacts should be self-documenting. |
| RD-2: Shared validation | **High** | The schema-layer contract is architecturally sound and minimally invasive. One prose sentence alongside the schema is strictly better than silence (which leaves post-mutation as an unaddressed threat) and strictly less than a mandated shared function (which is premature for one consumer). |
| RD-3: Multi-path `--context` | **High** | The 2-1 majority is correct. The directory mechanism is the designed multi-source pattern. Multi-path adds interaction semantics that no FR addresses. Deferral is the right call. |
| RD-4: `--force` / `--dry-run` | **High** | The 2-1 majority is correct. The flags serve an automation context that spec 007 does not define. The non-expert user principle argues against expanding the flag surface prematurely. |
| RD-5: Refine contract depth | **Medium-High** | The four-rule contract is clearly correct. The diff summary as recommended practice (not normative) is my best judgment, but I acknowledge that reasonable agents could argue for making the summary normative. The UX benefit is real; the question is whether it belongs in the spec or in implementation guidance. |
