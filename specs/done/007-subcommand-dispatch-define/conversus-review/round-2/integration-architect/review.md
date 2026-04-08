# Integration Architect — Round 2 Review

**Reviewer**: integration-architect
**Round**: 2 of 2
**Date**: 2026-03-22
**Basis**: spec.md, SKILL.md, Round 1 synthesis (final.md), arbitration resolution (resolution.md), own Round 1 disputes

---

## Executive Summary

Round 1 produced strong convergence on the structural additions spec 007 needs: post-write schema validation, context path validation, and dispatch matching semantics are unanimous P1. The five remaining disputes (RD-1 through RD-5) are well-characterized. Having reviewed the arbiter's advisory opinions and the Round 1 synthesis, I confirm all my prior concessions and refine my positions on the disputed items. No reversals.

The arbiter's perspective -- as the system that will execute the spec -- adds operational grounding that strengthens the case for the `## Status` section and the schema-layer validation contract. I adopt the arbiter's framing on both. On the three scope disputes (multi-path `--context`, `--force`/`--dry-run`, shared validation), the 2-1 majority position to defer is correct and the arbiter concurs. I maintain all majority positions from Round 1.

---

## Alignment

### Confirmed Convergence (no changes from Round 1)

I reaffirm all convergence items C-1 through C-13 from the Round 1 synthesis. These are settled. The three P1 changes and the P2/P3 changes listed in the synthesis represent the deliberation's core output. I will not revisit them.

Specifically, I reaffirm:

- **C-1: Post-write schema validation** (P1 unanimous). The define handler validates all 7 required headings after writing `problem.md`. Missing headings are added with `[CLARIFY:]` placeholders. This mirrors the engine's template validation at SKILL.md L286-295 and Phase 6 output validation at SKILL.md L659-676.

- **C-2: `--context` path validation** (P1 unanimous). Fail on non-existent paths, warn on empty directories. Mirrors SKILL.md L195-196. The strongest consensus in the entire review.

- **C-3: Dispatch matching** (P1 consensus). Exact, case-sensitive, exhaustive. Fallback-to-`run` was correctly rejected. The "Did you mean: `/conversus run {cmd}`?" suggestion in the error message is a good UX addition.

- **C-4 through C-13**: All confirmed without modification.

### Confirmed Concessions (no reversals)

From Round 1, I conceded:

1. **Withdrew multi-path `--context`** (original Rec #3). Functional-typing's conservative scoping is correct for spec 007.
2. **Withdrew `--type` override flag** (original Rec #5). No FR motivates it.
3. **Reduced refine semantics** from six prescriptive rules to four post-conditions. Devils-advocate correctly identified that the original six rules presented heuristic operations as deterministic algorithms.
4. **Scaled pipeline overview** to a single sentence. Both other agents correctly identified speculative documentation.
5. **Upgraded `--context` path validation** from P3 to P1. Functional-typing's structural-consistency framing was decisive.
6. **Downgraded anchor link rendering** from P2 to P3.

All concessions stand. None are reversed.

---

## Engagement with Disputes (Round 2 Positions)

### RD-1: `[CLARIFY:]` tags -- `## Status` section (maintained: FOR)

**Round 1 position**: Add a `## Status` section to `problem.md` with `draft`/`ready` values and a clarification count. Spec 007 sets the status; spec 008 decides what to do with it.

**Arbiter's contribution**: The arbiter reframed the status field as neither advisory nor binding but **descriptive** -- it states a measurable property of the artifact, like a file's word count. The arbiter grounded this in the fact that the define handler already computes and reports the clarification count (SKILL.md L865) and emits a warning (SKILL.md L872-875). The `## Status` section makes this transient console output persistent in the artifact.

**Round 2 position**: I adopt the arbiter's "factual annotation" framing without reservation. It resolves the advisory-vs-gate debate by sidestepping it entirely. The field is not advisory (it does not suggest; it states). It is not a gate (it does not block; it describes). It is a fact: "this artifact has N unresolved items."

This framing should satisfy functional-typing's boundary concern. The `## Status` section adds no consumer-prescriptive language. It does not say "downstream commands MUST check this field" (devils-advocate's RFC 2119 SHOULD language is correctly set aside by the arbiter). It says: the artifact reports its own completeness. Whether spec 008 treats `draft` as blocking is spec 008's decision.

The non-expert user argument is particularly compelling. Spec.md L87 says the command "Must NOT require coding knowledge to use." A non-expert who opens `problem.md` in their editor benefits from seeing `## Status: draft -- 3 items need clarification` at the top of the file. This is better UX than hoping the user remembers a console warning that has already scrolled away.

**Grounding**: SKILL.md L865 (clarification count already computed), SKILL.md L872-875 (warning already emitted), spec.md L87 (non-expert user principle), spec.md L13 (artifact feeds subsequent commands).

---

### RD-2: Shared validation function (maintained: SCHEMA-LAYER)

**Round 1 position**: Define the validation contract as prose alongside the `problem.md` schema, not in the dispatch section. Per-handler implementation for spec 007.

**Arbiter's contribution**: The arbiter sided with my schema-layer approach and provided the specific grounding I did not fully articulate in Round 1. The engine's validation patterns at SKILL.md L195-196 (paths), L286-295 (templates), and L659-676 (Phase 6 output) are not random per-handler code -- they are **structural invariants placed at the boundary where data enters or exits a phase**. The define handler is a new boundary. The validation contract belongs at the schema level because that is where the schema lives.

The arbiter also provided the exact language I would adopt: "After writing `problem.md`, validate that all required headings exist. Any command that reads `problem.md` as input should apply the same heading check before processing." One sentence. No code. No new section. Names the obligation without mandating a function.

**Round 2 position**: I maintain my schema-layer position and adopt the arbiter's prose formulation. This resolves the dispute as follows:

- **Devils-advocate's concern** (post-write user edits break schema compliance) is acknowledged by the forward-looking contract: "Any command that reads `problem.md` as input should apply the same heading check." This is a named obligation, not mandated infrastructure.
- **Functional-typing's concern** (routing and validation are distinct) is respected: no validation logic enters the dispatch section at SKILL.md L18-34.
- **My concern** (centralized contract, not per-handler reimplementation) is satisfied: the contract is defined once at the schema level.

The arbiter correctly observes that mandating a shared function for a population of one producer and zero consumers is premature abstraction. The prose contract is the right granularity.

**Grounding**: SKILL.md L822-850 (schema location where the contract belongs), SKILL.md L195-196 (boundary validation precedent), SKILL.md L18-34 (dispatch section should stay minimal).

---

### RD-3: Multi-path `--context` (maintained: DEFER)

**Round 1 position**: Defer to follow-up spec. Single-path with directory workaround is sufficient.

**Arbiter's contribution**: The arbiter provided a detail I did not articulate: the directory mechanism at SKILL.md L797 ("path may be a file or directory") is not a workaround but **the designed multi-source pattern**. This reframes the single-path constraint from "limitation with workaround" to "deliberate design with a directory-based multi-source mechanism."

The arbiter also enumerated the interaction semantics multi-path would require (ordering, deduplication, conflict resolution) that no FR addresses. These are not trivial design decisions.

**Round 2 position**: Defer. The single-path constraint is a scoping decision, not a design flaw. Document it explicitly as the synthesis recommends (Change 11): "`--context` accepts exactly one path. To include multiple context sources, point to a directory containing them." Note multi-path as a candidate for future extension. The documentation should frame this as a deliberate design choice with a defined multi-source mechanism (directories), not as a limitation to apologize for.

**Grounding**: spec.md L35 (FR-006: `--context <path>` -- singular), SKILL.md L797 (directory support is the multi-source mechanism), spec.md L87 (non-expert user principle).

---

### RD-4: `--force` and `--dry-run` flags (maintained: DEFER)

**Round 1 position**: Defer to the spec that defines the automation surface.

**Arbiter's contribution**: The arbiter grounded the deferral in FR-011 (spec.md L40): the interactive safeguard ("present it and ask whether to refine or replace") is a deliberate design choice for non-expert users. `--force` bypasses this safeguard. `--dry-run` is unnecessary in an interactive context where the agent already presents the result. Both flags serve automation contexts that spec 007 does not define.

**Round 2 position**: Defer. Add the documentation note the synthesis recommends (Change 13): "Future consideration: `--force` and `--dry-run` flags may be added in a future spec to support non-interactive and automated invocations." This acknowledges devils-advocate's foresight without expanding spec 007's interface for a use case that does not yet exist.

**Grounding**: spec.md L40 (FR-011: interactive safeguard), spec.md L87 (non-expert user principle), spec.md L89 (must not couple to specific domain -- automation coupling is analogous).

---

### RD-5: Refine semantics -- minimal contract depth (maintained: FOUR RULES)

**Round 1 position**: Four verifiable post-conditions: (a) all headings preserved, (b) no silent deletion, (c) Source Documents unioned, (d) Type re-evaluated.

**Arbiter's contribution**: The arbiter confirmed all four post-conditions as "structural invariants I can reliably enforce" from the executing system's perspective. The arbiter distinguished between the four rules (structural invariants, normative) and the diff summary (UX feature, recommended practice). The arbiter proposed: "After refining, the define handler should summarize what changed... to make the operation auditable," using lowercase "should" to make it a recommendation, not a requirement.

**Round 2 position**: I adopt the arbiter's formulation in full. The four-rule contract is normative. The diff summary is recommended practice. This distinction matters because:

- The four rules define **what the output must satisfy** -- they are testable post-conditions a downstream consumer can depend on.
- The diff summary describes **how the operation is reported** -- it is a UX concern that varies by context.

Collapsing them into a single requirement level either under-specifies the structural guarantees or over-specifies the UX guidance. The arbiter articulated this clearly: "the post-conditions are normative (the spec requires them). The diff summary is good practice (the spec recommends it)."

Devils-advocate's observability concern is real and acknowledged. The recommended-practice framing ensures the concern is addressed without elevating an inherently variable UX output to a structural invariant.

**Grounding**: SKILL.md L791 ("incorporate the user's new input while preserving existing structure" -- the four rules formalize what "preserving existing structure" means), SKILL.md L822-850 (seven headings the rules enforce).

---

## Missed Opportunities

### MO-1: No explicit idempotency contract for `define` on a `ready` problem.md

If `## Status` is adopted (as I advocate), the spec should address the case where a user runs `/conversus define` against a `problem.md` that is already `status: ready` with zero `[CLARIFY:]` tags. FR-011 (spec.md L40) requires presenting the file and asking refine/replace, which handles the interaction. But the spec does not say whether a refine pass on a complete problem definition should re-evaluate all sections or only incorporate the new input. The four-rule contract (rule d: "Type re-evaluated") implies re-evaluation, but the scope of re-evaluation when no new information is provided is undefined.

This is P3 and not blocking. The define handler's judgment is adequate. But it is worth noting as a gap that will surface in practice when users run `/conversus define` reflexively.

**Grounding**: spec.md L40 (FR-011), SKILL.md L791 (refine behavior).

### MO-2: No guidance on `problem.md` interaction with `/conversus run`

Spec 007 correctly isolates the define handler from the engine internals. But it does not address the scenario where a user has both a `problem.md` and a `conversus.yml` in the same directory. These are currently independent artifacts. The spec should note -- even as a single sentence -- that `problem.md` is consumed by the guided workflow path (`define` -> `interests` -> `mode`) while `conversus.yml` is consumed by the direct execution path (`run`). This prevents user confusion about whether `problem.md` influences a `/conversus run` invocation.

**Grounding**: SKILL.md L36-42 (run handler looks for `conversus.yml`), SKILL.md L769-876 (define handler produces `problem.md`). The two artifacts coexist but have no interaction, which is a correct design choice that should be stated.

---

## Off-Base Assumptions

### OBA-1: Treating the four-type taxonomy as universally sufficient

The spec (spec.md L37, SKILL.md L806-813) defines four problem types: `selection`, `integration`, `scoping`, `stress-test`. The deliberation reached consensus (C-8) that this taxonomy is intentionally closed with a companion update required for extension. I do not contest this consensus.

However, I note that the taxonomy assumes decisions are decomposable into one of these four frames. Some decisions are genuinely multi-typed: "Which team should own the new service, and what technology should it use?" combines `scoping` and `selection`. The spec's mitigation (FR-008: "If ambiguous, mark the type as its best guess and list alternatives" at spec.md L37) handles this for classification ambiguity, but it does not address genuinely composite decisions where the user needs to decompose the problem before classifying it.

This is not a spec change recommendation -- the taxonomy closure decision is correct for spec 007. It is an observation that the `[CLARIFY:]` mechanism should guide users toward decomposition when a description maps to multiple types, and that guidance is currently implicit in FR-008's ambiguity handling rather than explicit.

**Grounding**: spec.md L37 (FR-008), SKILL.md L815-818 (ambiguity handling with `[CLARIFY:]` tag).

---

## Actionable Recommendations

### Priority Tier 1 (P1) -- Must adopt

These are unchanged from Round 1 consensus. I list them for completeness and to confirm they survive Round 2 without modification.

| ID | Recommendation | Status |
|----|---------------|--------|
| R1 | Post-write schema validation for `problem.md` (Change 1 in synthesis) | **Confirmed P1 unanimous** |
| R2 | `--context` path validation before ingestion (Change 2 in synthesis) | **Confirmed P1 unanimous** |
| R3 | Dispatch matching: exact, case-sensitive, exhaustive (Change 3 in synthesis) | **Confirmed P1 consensus** |

### Priority Tier 2 (P2) -- Should adopt

| ID | Recommendation | Status |
|----|---------------|--------|
| R4 | Single-agent execution model statement (Change 4) | Confirmed P2 consensus |
| R5 | Empty-section `[CLARIFY:]` coverage for Constraints and Success Criteria (Change 5) | Confirmed P2 consensus |
| R6 | `--output` directory creation semantics (Change 6) | Confirmed P2 uncontested |
| R7 | Refine semantics: four-rule minimal contract (Change 7) | Confirmed P2 majority, with diff summary as recommended practice |
| R8 | Taxonomy closure design note (Change 8) | Confirmed P2 consensus |
| R9 | Pipeline overview scaled to single sentence (Change 9) | Confirmed P2 consensus |
| R10 | `## Status` section in `problem.md` as factual annotation (Change 10) | **Maintained P1 from my position; synthesis rates disputed.** I accept the synthesis priority assignment while maintaining that the factual-annotation framing should resolve functional-typing's objection. |

### Priority Tier 3 (P3) -- Optional

| ID | Recommendation | Status |
|----|---------------|--------|
| R11 | Document single `--context` path constraint (Change 11) | Confirmed P3 majority |
| R12 | Acknowledge frontmatter change in spec (Change 12) | P3 single advocate |
| R13 | Note `--force`/`--dry-run` as future consideration (Change 13) | Confirmed P3 majority defers |
| R14 | Note shared validation as architectural direction (Change 14) | Confirmed P3 compromise |

### New Round 2 Recommendations

| ID | Recommendation | Priority |
|----|---------------|----------|
| R15 | Add a sentence noting that `problem.md` and `conversus.yml` are independent artifacts for different workflow paths (see MO-2) | P3 |

---

## Referenced Documentation

| Document | Location | Relevance |
|----------|----------|-----------|
| Spec 007 | `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/spec.md` | Target specification: 12 FRs, 5 SCs, 3 constraints |
| SKILL.md | `/Users/business-daddy/code/payer-index-mono/conversus/SKILL.md` | Implementation: dispatch table (L18-34), define handler (L769-876), run handler (L36-766) |
| Round 1 synthesis | `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/summary/final.md` | Prior round convergence (C-1 through C-13), disputes (RD-1 through RD-5), actionable changes (1-14) |
| Arbitration resolution | `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/arbitration/resolution.md` | Advisory opinions on all five disputes, operational grounding from the executing system |
| Round 1 integration-architect disputes | `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/integration-architect/disputes.md` | Own prior positions on disputes 1-5, convergence 1-10 |
| Round 1 integration-architect revision | `/Users/business-daddy/code/payer-index-mono/conversus/specs/007-subcommand-dispatch-define/conversus-review/round-1/integration-architect/revision.md` | Own revised recommendations: 8 disposition changes, 3 new recommendations |

### Key SKILL.md Line References

| Lines | Content | Referenced in |
|-------|---------|---------------|
| L18-34 | Subcommand dispatch table and error handling | R3, RD-2 |
| L195-196 | Run handler path validation | R2, RD-2 |
| L286-295 | Template schema validation | R1 |
| L659-676 | Phase 6 output validation | R1 |
| L769-876 | Define handler (full section) | All recommendations |
| L791 | Refine behavior ("incorporate... while preserving existing structure") | R7, RD-5 |
| L797 | Context path resolution (file or directory) | RD-3 |
| L822-850 | `problem.md` schema | R1, RD-2 |
| L852 | FR-010 universal `[CLARIFY:]` rule | R5 |
| L854 | Empty-section handling | R5 |
| L865 | Clarification count in report | RD-1 |
| L872-875 | Clarification warning | RD-1 |

### Key spec.md Line References

| Lines | Content | Referenced in |
|-------|---------|---------------|
| L6 | "foundational -- establishes dispatch infrastructure" | Scope boundary discussion |
| L13 | "artifact feeds subsequent commands" | RD-1 |
| L35 | FR-006: `--context <path>` (singular) | RD-3 |
| L37 | FR-008: type classification with ambiguity handling | OBA-1 |
| L40 | FR-011: interactive safeguard | RD-4, MO-1 |
| L87 | Non-expert user principle | RD-1, RD-3, RD-4 |
| L88-89 | Must not break `/conversus run`; must not couple to domain | Alignment, RD-4 |
