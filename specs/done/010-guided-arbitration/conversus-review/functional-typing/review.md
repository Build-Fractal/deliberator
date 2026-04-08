# Cooperative Review — Phase 1: Initial Review

**Agent**: functional-typing
**Round**: 1 of 2
**Mode**: cooperative

---

### Executive Summary

Spec 010 (Guided Arbitration) defines a conversational UX layer over the Phase 6 arbitration engine from spec 001. Its purpose is clear: users who don't understand grounding documents, trigger conditions, or influence levels should be able to set up and run arbitration through plain-language prompts. The spec is well-scoped — it explicitly avoids redefining arbitration mechanics (L69) and positions itself as a pure delegation layer.

From a structural correctness perspective, the SKILL.md implementation covers all 12 FRs with reasonable fidelity. The handler follows the established subcommand pattern (dispatch table at SKILL.md L26-36), has proper prerequisite checks, and delegates execution to the Phase 6 engine without introducing new arbitration logic. The plain-language UX prompts are genuinely readable for non-expert users.

My most important recommendation: the grounding document generation from `problem.md` (FR-007, SKILL.md L1707-1721) needs stricter validation — the current spec allows generating a grounding document that may not actually contain actionable decision criteria, which would undermine the entire arbitration process.

### Alignment

- **FR-to-handler coverage** (spec L29-54, SKILL.md L1537-1855): All 12 FRs map to specific handler sections. FR-001 through FR-003 map to Input and Step 1. FR-004 through FR-008 map to Steps 2-3. FR-009-FR-010 map to Steps 4-5. FR-011-FR-012 map to Step 6 and the standalone design. Complete coverage with no orphaned FRs.

- **Zero new arbitration logic** (spec L69, SKILL.md L1541, L1803): The implementation explicitly states "Zero new arbitration logic" at L1803 and "This command adds no new arbitration logic" at L1541. Step 5 delegates entirely to the Phase 6 engine. This aligns with the constraint at spec L69.

- **Plain-language UX quality** (spec L14-16, SKILL.md L1636-1650, L1677-1690, L1733-1744): The user-facing prompts avoid arbitration jargon. The arbiter identity question (L1636-1650) offers three concrete examples. The grounding document explanation (L1677-1690) uses examples like "design principles" and "style guide." The influence level question (L1733-1744) uses "final authority" instead of "binding." These map well to FR-004 and FR-008.

- **Standalone operation** (spec L54, SKILL.md L1549-1553): The handler accepts any completed conversus output directory, not just those produced by the guided workflow. FR-012 is satisfied by the Input section's design.

- **Dispatch routing** (SKILL.md L33): `/conversus arbitrate [path] [--force]` is in the dispatch table with the correct route target `[Arbitrate: Guided Arbitration](#arbitrate-guided-arbitration)`.

### Missed Opportunities

- **Missing validation of generated grounding document quality**: SKILL.md L1707-1721 specifies generating a grounding document from `problem.md`, but there's no validation that the extracted Constraints and Success Criteria sections actually contain meaningful content. A `problem.md` with empty or single-word constraints would produce a grounding document that passes file-existence validation but provides no decision framework. Impact: high.

- **No arbiter prompt validation**: SKILL.md L1672 says "Validate it is non-empty" for the edit case, but there's no equivalent validation for the auto-generated prompt. If the user provides a vague description like "someone" and the handler generates a prompt, there's no check that the generated prompt contains actionable identity framing. Impact: medium.

- **Missing config backup before append**: SKILL.md L1795 says "Append the arbiter block to conversus.yml" but does not specify creating a backup of the existing config. If the append produces malformed YAML (e.g., indentation issues), the user loses their original config. Impact: medium.

- **No round-awareness in the arbitrate handler**: The handler reads `summary/final.md` (SKILL.md L1559) but does not account for multi-round output structures where `summary/final.md` is a cross-round synthesis. The spec should explicitly state whether the handler supports multi-round output directories and how it navigates `round-N/` subdirectories. Impact: medium.

- **Influence level mapping gap with spec 006**: FR-008 (spec L44) references "spec 006" for influence levels. SKILL.md L1747-1752 maps user responses to `binding`/`recommended`/`advisory`, but the mapping from "final authority" -> `binding` is only implicit in the UX prompt. The spec should state the canonical mapping explicitly. Impact: low.

- **No idempotency guarantee for grounding document generation**: SKILL.md L1707 says to write `grounding.md` but does not check whether `grounding.md` already exists. Re-running the arbitrate command could overwrite a user-customized grounding document. Impact: medium.

### Off-Base Assumptions

- **Assumption that `problem.md` always has Constraints and Success Criteria sections** (SKILL.md L1707-1708): The handler assumes `problem.md` follows the structure produced by `/conversus define`, which includes these sections. But FR-012 (spec L54) says the command works with "any completed conversus output directory" — including those created without the guided workflow. A hand-crafted `problem.md` may not have these sections. The handler should parse what's available rather than assuming structure.

- **Assumption that the arbiter block can always be cleanly appended to YAML** (SKILL.md L1795): YAML append is not trivial — if the existing file has trailing comments, document markers (`---`), or unusual formatting, a naive append could produce invalid YAML. The spec should specify that the arbiter block is appended as a top-level key using proper YAML serialization, not string concatenation.

### Actionable Recommendations

1. **Add grounding document content validation** (Priority: P1)
   - **Current state**: SKILL.md L1707-1721 generates `grounding.md` from `problem.md` without validating content quality.
   - **Proposed change**: After generating `grounding.md`, validate that the Constraints section contains at least one non-empty bullet point and the Success Criteria section contains at least one non-empty bullet point. If either is empty, warn: "The generated grounding document has no {constraints|success criteria}. The arbiter will have limited basis for decisions. Consider adding content manually."
   - **Rationale**: An empty grounding document passes file validation but produces arbitrary rulings, directly violating spec L71-72.
   - **Risk if ignored**: Users create grounding documents that look valid but provide no decision framework, producing rulings that appear authoritative but are ungrounded.

2. **Add config backup before append** (Priority: P1)
   - **Current state**: SKILL.md L1795 appends to `conversus.yml` without backup.
   - **Proposed change**: Before appending, copy `conversus.yml` to `conversus.yml.bak`. Report: "Backed up conversus.yml to conversus.yml.bak."
   - **Rationale**: YAML append can produce malformed output if the existing file has unexpected formatting. A backup provides recovery.
   - **Risk if ignored**: Users lose their working configuration if the append produces invalid YAML.

3. **Add grounding document overwrite protection** (Priority: P2)
   - **Current state**: SKILL.md L1707 writes `grounding.md` without checking for existing file.
   - **Proposed change**: Before writing, check if `grounding.md` exists. If it does, ask: "grounding.md already exists. Overwrite? (yes / no — use existing)" If no, use the existing file as the grounding document.
   - **Rationale**: Idempotency protection for re-runs. Users who customized `grounding.md` after initial generation should not lose their changes.
   - **Risk if ignored**: Re-running the arbitrate command silently overwrites user-customized grounding documents.

4. **Handle missing problem.md sections gracefully** (Priority: P2)
   - **Current state**: SKILL.md L1707-1708 assumes `problem.md` has Constraints and Success Criteria sections.
   - **Proposed change**: Parse `problem.md` for available sections. If Constraints is missing, use any section containing constraint-like content. If Success Criteria is missing, use any section containing criteria or objectives. If neither is found, warn: "problem.md does not contain recognizable constraints or criteria. Cannot generate grounding document automatically." Re-ask for a path.
   - **Rationale**: FR-012 requires standalone operation — hand-crafted problem.md files may not follow the guided workflow's output structure.
   - **Risk if ignored**: The handler fails ungracefully when `problem.md` doesn't follow the expected format.

5. **Explicitly document multi-round output support** (Priority: P2)
   - **Current state**: SKILL.md L1559 checks for `summary/final.md` but does not address multi-round directory structures.
   - **Proposed change**: Add a note that `summary/final.md` is the correct entry point for both single-round and multi-round outputs (since multi-round runs produce a cross-round synthesis at `{output}/summary/final.md`). Explicitly state the handler does not need to navigate `round-N/` directories.
   - **Rationale**: Prevents confusion about whether the handler works with multi-round output.
   - **Risk if ignored**: Users or future implementers may wonder whether the handler supports multi-round output.

6. **Add explicit influence level canonical mapping** (Priority: P2)
   - **Current state**: SKILL.md L1747-1752 maps responses but the UX prompt uses "final authority" while the config uses "binding."
   - **Proposed change**: Add a mapping table immediately after the UX prompt: `"final authority" | "binding" | default → binding; "recommended" → recommended; "advisory" → advisory`.
   - **Rationale**: The current implicit mapping is fragile — implementers must infer the mapping from context.
   - **Risk if ignored**: Implementation divergence if the mapping is interpreted differently.

7. **Validate generated arbiter prompt has identity framing** (Priority: P3)
   - **Current state**: SKILL.md L1652-1658 generates prompts from user descriptions but only validates non-emptiness in the edit case (L1672).
   - **Proposed change**: After generating the arbiter prompt, validate that it contains at least one of: "You are", "You ARE", "You have authority", or similar identity markers. Warn if not: "The generated prompt may not clearly establish the arbiter's identity."
   - **Rationale**: A prompt without identity framing produces weak arbitration because the arbiter lacks a clear perspective.
   - **Risk if ignored**: Vague user descriptions produce vague prompts, leading to non-committal rulings.

8. **Specify YAML serialization method for arbiter append** (Priority: P3)
   - **Current state**: SKILL.md L1795 says "Append the arbiter block to conversus.yml" without specifying how.
   - **Proposed change**: Specify: "Use YAML-aware serialization (read, parse, add key, write) rather than string concatenation. This ensures valid YAML output regardless of the existing file's formatting."
   - **Rationale**: String concatenation can break on trailing comments, document markers, or unusual whitespace.
   - **Risk if ignored**: Edge cases produce invalid YAML that breaks subsequent conversus runs.

### Referenced Documentation

- `specs/010-guided-arbitration/spec.md` — sections/lines cited: L6 (depends-on), L14-16 (summary), L29-54 (FRs), L60-63 (SCs), L69-72 (constraints)
- `SKILL.md` — sections/lines cited: L26-36 (dispatch), L1537-1543 (handler intro), L1549-1553 (input), L1559-1565 (prerequisite check), L1567-1602 (dispute detection), L1604-1628 (existing arbiter check), L1630-1752 (guided config), L1754-1797 (config generation), L1799-1815 (execution), L1817-1855 (post-arbitration report)
