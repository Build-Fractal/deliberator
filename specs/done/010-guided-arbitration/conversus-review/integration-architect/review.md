# Cooperative Review — Phase 1: Initial Review

**Agent**: integration-architect
**Round**: 1 of 2
**Mode**: cooperative

---

### Executive Summary

Spec 010 establishes a guided arbitration subcommand that wraps the Phase 6 engine from spec 001 in a conversational UX. The integration architecture is sound: the handler follows the established subcommand dispatch pattern, performs prerequisite validation, and delegates execution without duplicating engine logic. The separation of concerns is clean — the handler owns UX and config generation; the Phase 6 engine owns arbitration mechanics.

The FR-to-implementation mapping is complete, with all 12 FRs covered by distinct handler sections. SC-001 through SC-004 are satisfiable by the current design. The dispatch routing is correct and the prerequisite checks follow the pattern established by the converge handler. The critical constraint — "must not redefine arbitration mechanics" — is respected throughout.

My most important recommendation: the handler's execution step (Step 5, SKILL.md L1799-1815) re-reads and re-validates the entire `conversus.yml` config, but this re-validation may reject configs that were valid before the arbiter block was appended, if the append introduced formatting issues. The execution step should validate only the arbiter section, not re-run full config validation.

### Alignment

- **Complete FR coverage**: All 12 FRs have corresponding handler sections:
  - FR-001 (spec L29): Input section (SKILL.md L1545-1553) — accepts path or finds output directory
  - FR-002 (spec L30): Step 1 (SKILL.md L1567-1569) — reads summary, uses Dispute-Parsing Subsystem
  - FR-003 (spec L31): Step 1 (SKILL.md L1582-1602) — no-disputes handling with `--force` override
  - FR-004 (spec L35-37): Step 3 (SKILL.md L1630-1650) — guided configuration prompts
  - FR-005 (spec L38-41): Step 3a (SKILL.md L1652-1658) — identity prompt generation patterns
  - FR-006 (spec L42): Step 3b (SKILL.md L1660-1672) — user may edit generated prompt
  - FR-007 (spec L43): Step 3c (SKILL.md L1674-1727) — grounding document with generation option
  - FR-008 (spec L44): Step 3d (SKILL.md L1729-1752) — influence level with spec 006 mapping
  - FR-009 (spec L48): Step 5 (SKILL.md L1799-1815) — delegates to Phase 6 engine
  - FR-010 (spec L49): Step 4 (SKILL.md L1754-1797) — appends config to conversus.yml
  - FR-011 (spec L53): Step 6 (SKILL.md L1817-1855) — plain-language ruling summaries
  - FR-012 (spec L54): Input section (SKILL.md L1549-1553) — standalone operation, any output directory

- **SC-001 verification** (spec L61): The handler generates the same `arbiter:` block structure that hand-configuration would produce (SKILL.md L1758-1766). The generated YAML uses identical keys: `name`, `prompt`, `grounding`, `trigger`, `influence`. Phase 6 engine processes this identically.

- **SC-002 verification** (spec L62): The UX prompts use plain language throughout. No arbitration jargon appears in user-facing text. Examples are concrete ("design principles", "tech lead", "project constitution").

- **SC-003 verification** (spec L63): The prerequisite check (SKILL.md L1555-1565) validates only `summary/final.md` existence, not workflow-specific artifacts. Any output directory with a completed synthesis is valid.

- **SC-004 verification** (spec L64): The influence level prompt (SKILL.md L1733-1744) explains all three levels with one-sentence descriptions and avoids technical terms ("final authority" not "binding").

- **Phase 6 delegation integrity** (spec L48, L69, SKILL.md L1803-1815): Step 5 is an explicit delegation. Items 1-7 at SKILL.md L1805-1813 map directly to the Phase 6 engine's existing flow. No new resolution logic, template modifications, or dispute-handling logic is introduced.

### Missed Opportunities

- **No validation that Phase 6 engine components exist**: SKILL.md L1811 loads `templates/{mode}/arbitration.md` but Step 5 does not pre-validate that the template file exists before launching the Phase 6 agent. The Run engine's Step 3 handles this, but the arbitrate handler's Step 5 says "Parse and validate the config using the same Step 1 validation" (L1806) — Step 1 of Run validates agent config, not template existence. Template validation happens in Step 3 of Run. The handler should either explicitly include template validation or clarify that "the same validation" includes Steps 1-3. Impact: high.

- **No explicit error path for arbiter block already in conversus.yml at Step 5**: If the user selects "reconfigure" at Step 2 (SKILL.md L1623), the handler removes the existing arbiter block and proceeds to Step 3. But the removal is not specified — how is the block removed? YAML parsing and rewriting? Line deletion? This is an integration gap. Impact: medium.

- **Missing timing field in generated config**: The generated arbiter config block (SKILL.md L1758-1766) does not include a `timing` field. Per the Run engine validation (SKILL.md L218-220), timing defaults to `final` if absent, which is correct. But since the arbitrate handler is designed for post-deliberation use, explicitly including `timing: final` would make the generated config self-documenting. Impact: low.

- **No handling for concurrent modifications to conversus.yml**: Between Step 1 (reading the config) and Step 4 (appending), another process could modify `conversus.yml`. The handler does not implement any locking or compare-and-swap mechanism. Impact: low (single-user tool, but worth noting).

- **Trigger re-evaluation in Step 5 creates a race-like gap**: SKILL.md L1807-1809 re-evaluates the trigger condition in Step 5, which could fail if the synthesis was modified between Step 1 and Step 5. While unlikely in practice, the spec should acknowledge this and specify that the handler should use the trigger determination from Step 1, not re-evaluate. Impact: low.

- **Post-arbitration report parsing fragility**: SKILL.md L1820-1850 extracts ruling summaries from `resolution.md`, but the extraction relies on the Phase 6 agent producing output in the expected format. If the agent deviates (which is plausible — LLM outputs are probabilistic), the fallback at L1852-1854 fires. The spec should define how to extract rulings structurally (e.g., by heading pattern) rather than assuming format compliance. Impact: medium.

### Off-Base Assumptions

- **Assumption that Step 1 validation from Run: Execution is sufficient for the arbitrate handler** (SKILL.md L1806): The Run engine's Step 1 validates the full config — agents, mode, targets. But the arbitrate handler has already identified the output directory and parsed the synthesis. Re-running full validation means re-checking agents, targets, and mode — all of which were already validated when the deliberation originally ran. The only new element is the arbiter block. Full re-validation is wasteful and risks rejecting the config on unrelated grounds (e.g., a target file that was since deleted).

- **Assumption that YAML append is atomic** (SKILL.md L1795): The spec says "Append the arbiter block to conversus.yml" as if this is a single atomic operation. In practice, this requires reading the file, parsing it as YAML, adding the arbiter key, serializing, and writing back. A naive file-append (string concatenation) could produce invalid YAML. The spec should specify the method.

### Actionable Recommendations

1. **Scope Step 5 validation to arbiter block only** (Priority: P1)
   - **Current state**: SKILL.md L1806 says "Parse and validate the config using the same Step 1 validation from Run: Execution."
   - **Proposed change**: "Parse `conversus.yml` and validate the `arbiter:` block using the arbiter-specific validation from Step 1 (SKILL.md L212-222). Do not re-validate agents, targets, or mode — these were validated when the deliberation originally ran."
   - **Rationale**: Full re-validation risks rejecting valid configs if external files changed since the deliberation ran.
   - **Risk if ignored**: Users encounter validation errors unrelated to arbitration (e.g., a renamed target file) that block the arbitrate command.

2. **Specify template validation in Step 5** (Priority: P1)
   - **Current state**: SKILL.md L1811 loads the arbitration template but does not specify pre-validation.
   - **Proposed change**: Add between L1810 and L1811: "Validate that `templates/{mode}/arbitration.md` exists. If not, fail with: 'Arbitration template not found: {path}. Ensure templates/ directory exists.'"
   - **Rationale**: Template validation is handled by Step 3 in the Run engine, but the arbitrate handler skips Step 3. Without this, a missing template produces an opaque error.
   - **Risk if ignored**: Missing templates produce confusing errors instead of clear guidance.

3. **Specify arbiter block removal method for reconfigure** (Priority: P2)
   - **Current state**: SKILL.md L1623 says "Remove the existing arbiter block and proceed to Step 3" without specifying how.
   - **Proposed change**: "Read `conversus.yml`, parse as YAML, remove the `arbiter` key, and write back. Preserve all other keys and formatting where possible."
   - **Rationale**: Without specifying the method, implementers may use string manipulation, which is fragile for YAML.
   - **Risk if ignored**: Reconfiguration corrupts the YAML file or leaves partial arbiter config.

4. **Add timing field to generated config** (Priority: P2)
   - **Current state**: SKILL.md L1758-1766 generates an arbiter block without `timing`.
   - **Proposed change**: Add `timing: final` to the generated config block. The arbitrate handler always runs post-deliberation, so `timing: final` is always correct.
   - **Rationale**: Self-documenting config. Prevents confusion if the user later adds `rounds > 1` to the config.
   - **Risk if ignored**: Generated configs rely on implicit defaults, which is less transparent for users.

5. **Define structural ruling extraction for post-arbitration report** (Priority: P2)
   - **Current state**: SKILL.md L1820-1850 extracts rulings but does not define the extraction method.
   - **Proposed change**: "Extract rulings by parsing `#### Dispute:` headings in `resolution.md`. For each heading, extract the `**Ruling:**` line as the decision summary and the first sentence of `**Rationale:**` as the rationale. If no `#### Dispute:` headings are found, use the fallback."
   - **Rationale**: Structural extraction is more reliable than assuming arbitrary LLM-generated format.
   - **Risk if ignored**: Post-arbitration reports frequently fall back to the generic message, reducing UX quality.

6. **Use Step 1 trigger determination instead of re-evaluating in Step 5** (Priority: P3)
   - **Current state**: SKILL.md L1807-1809 re-evaluates the trigger in Step 5.
   - **Proposed change**: "Use the trigger determination from Step 1. Do not re-read the synthesis in Step 5. If `--force` was used, set trigger to `always`. If disputes were detected in Step 1, set trigger to `disputes_remain` and do not re-evaluate."
   - **Rationale**: Re-evaluation creates a theoretical gap where the synthesis could change between detection and execution.
   - **Risk if ignored**: Minimal practical risk, but logically cleaner to avoid redundant evaluation.

7. **Add explicit multi-round output documentation** (Priority: P3)
   - **Current state**: SKILL.md L1559 checks for `summary/final.md` but does not discuss multi-round output.
   - **Proposed change**: Add a note after L1559: "For multi-round output directories, `summary/final.md` is the cross-round synthesis. The handler does not need to navigate individual round directories."
   - **Rationale**: Clarifies the handler's behavior for multi-round outputs.
   - **Risk if ignored**: Minor confusion for implementers.

8. **Include docs field in generated arbiter config** (Priority: P3)
   - **Current state**: SKILL.md L1758-1766 generates an arbiter block without `docs`.
   - **Proposed change**: Add an optional step 3e asking: "Are there additional documents the arbiter should reference? (paths, or 'none')". If provided, include `docs:` in the generated config.
   - **Rationale**: The arbiter schema supports `docs` (SKILL.md L105-106) but the guided flow never offers to populate it.
   - **Risk if ignored**: Users who need arbiter docs must manually edit the config after generation.

### Referenced Documentation

- `specs/010-guided-arbitration/spec.md` — sections/lines cited: L6 (depends-on), L29-54 (FRs), L60-64 (SCs), L48-49 (execution/config FRs), L53-54 (post-arbitration/standalone FRs), L69-72 (constraints)
- `SKILL.md` — sections/lines cited: L26-36 (dispatch table), L99-111 (arbiter schema), L204-232 (validation), L1537-1855 (arbitrate handler, all subsections)
