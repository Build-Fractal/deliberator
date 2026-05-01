### Executive Summary

The v2.6.0 candidate amends Principle XVI (Mathematical Transparency) by elevating three structural requirements — parameter pinning, shape determinism, plain-language output pairing — as the headline constitutional claim, while demoting the prior "user MUST understand what is being optimized" framing to design intent. The amendment's stated purpose is to close the grandfathering gap surfaced by the v2.4.0 Constitutional Inclusion Criteria gate: the original headline fails Criterion 1 because "user understanding" is not mechanically checkable, whereas the elevated structural substrate passes.

From a cross-principle coherence perspective, the rewrite is largely sound: it preserves the body content that v2.3.2 carefully integrated with Principles VII and VIII, and the three structural requirements are cleanly distinct from XV, XXII, and XXIV's adjacent domains. However, the audit surfaces three genuine tensions and one precedent gap that require attention before ratification: (1) XV's "plugin failure MUST NOT block core execution" is not reconciled with XVI's MUST requirement for plain-language output pairing in plugin recommendations — runtime behavior for a violation is undefined; (2) the Governance gate does not explicitly cover headline rewrites of grandfathered principles, creating a new precedent category the SIR does not explicitly acknowledge as such; (3) the word "shape" is now used in two incompatible senses across Principles IX and XVI, creating a terminological collision that context alone may not reliably resolve as tooling matures.

**Most important recommendation**: Add an explicit enforcement-mode clause to XVI's plain-language output pairing requirement specifying that violations trigger XV's warn-and-continue mechanism, not a core execution gate — otherwise XVI's MUST and XV's "plugin failure MUST NOT block core execution" are in silent conflict with undefined runtime semantics.

---

### Alignment

- **VII↔XVI bilateral carve-out preserved** (Principle XVI, v2.3.2 Clarification block): The rewrite preserves the v2.3.2 clarification verbatim. The explicit exception to VII's unconditional reproducibility requirement — "the assembled objective function is the determinism boundary, not the LLM-resolved parameter values that feed into it" — is unchanged. VII's parenthetical "(narrowed by Principle XVI for LLM gap-filling output)" still has an accurate referent inside XVI's body, even though XVI's headline is now scoped to three structural requirements broader than the carve-out alone.

- **VIII vocabulary alignment intact** (Principle VIII parenthetical; Principle XVI stage 3 "Deterministic assembly"): The rewrite retains "Deterministic assembly" as stage 3's name. VIII's parenthetical — "(In v2.3.2, Principle XVI uses 'deterministic' for the post-pinning assembly stage; the term is co-extensive with VIII's 'mechanical' — both denote rule-based, non-inference-driven execution.)" — continues to hold. The new headline's "byte-identical on every assembly" is a stronger but compatible assertion: it specializes XVI's claim for objective function assembly without contradicting VIII's general "mechanical and predictable" template behavior.

- **XXIV enforcement integration correctly scoped** (Principle XVI, Enforcement sub-bullet): The Enforcement sub-bullet cross-references XXIV's contract-test requirement explicitly: "Principle XXIV applies — a contract test reproducing the re-resolution failure pattern is required." This is correctly scoped — it invokes XXIV's three-layer defense framework at a safety-critical path (parameter resolution). Spot-check against XXVIII confirms no collision: the contract test is new test creation, not a fix of a failing test, so XXVIII's test-fix discipline does not apply.

- **Constitutional Inclusion Criteria self-assessment substantive** (SIR comment block, Criterion 1/2/3 self-assessment): The SIR includes explicit Criterion 1/2/3 self-assessments with concrete mechanical-check sketches for each structural requirement — spec 014 FR-012/SC-004 lint for parameter pinning, parity test for shape determinism, schema lint for plain-language pairing. Each check is "concrete enough that an engineer reading the principle can sketch the check in one paragraph," satisfying the gate's stated standard (Governance, Constitutional Inclusion Criteria, Criterion 1).

- **Registry-as-extension-interface boundary respected** (Principle XV Clarification v2.3.1; Principle XVI third bullet): XVI's plain-language output pairing requirement targets plugin *output format* — what plugins must include in their recommendations. It does not modify the extension mechanism itself (how plugins register capabilities via the registry). This is consistent with XV's registry-as-extension-interface clarification, which reserves the registry as the only sanctioned extension point; XVI adds a constraint on output content, not on extension plumbing.

---

### Missed Opportunities

- **VII's parenthetical is now harder to navigate**: The parenthetical "(narrowed by Principle XVI for LLM gap-filling output)" was written when XVI's headline specifically concerned user understanding of optimization; the carve-out was the dominant scope of XVI's first bullet. Now XVI's headline names three structural requirements (parameter pinning, shape determinism, plain-language pairing), none of which is "LLM gap-filling output." A reader following VII's parenthetical to XVI encounters the new headline before reaching the v2.3.2 clarification block where the carve-out is defined. The parenthetical is accurate but requires more interpretive traversal. **Impact: low** (correctness preserved; navigability degrades).

- **Enforcement mode for plain-language MUST is unspecified**: XVI's headline and body use MUST for plain-language output pairing ("every plugin recommendation includes plain-language explanations alongside numerical outputs"). XV's Plugin Isolation says "Plugin failure MUST NOT block core execution — warnings only." If a plugin emits numerical output without plain-language pairing, is the violation (a) a schema-level rejection blocking plugin output, (b) a parser-level failure triggering XV's warn-and-continue, or (c) silently ignored? None of XVI, XV, or XXIV resolves this. The SIR does not address it. **Impact: high** (runtime behavior is undefined for a foreseeable and specified failure mode).

- **Gate precedent for headline rewrites is unacknowledged**: The Governance gate covers new principles (fully gated), Extension/Clarification blocks on grandfathered principles (Criterion 1 required for new normative requirements), and wording-level clarifications (exempt). A headline rewrite that restructures existing body content into a new headline claim fits none of these three categories. The SIR treats the rewrite as satisfying all three criteria — implicitly claiming the gate applies — but does not acknowledge that it creates a new precedent category. Future amendments to VI (Scripts Over Markdown) or X (Zen of Python Output) may cite this rewrite as license for broader gate bypass. **Impact: medium** (governance ambiguity that compounds on the next grandfathered-principle amendment).

- **Verification block is in SIR, not in principle body**: The Governance gate's Extension blocks paragraph says Extension/Clarification blocks added post-ratification MUST include the structured `Verification:` block when introducing new normative requirements. The SIR includes inline Criterion 1/2/3 self-assessments in comment block prose — not in a structured `Verification:` block inside the principle body. If the gate's Extension block requirement does apply to headline rewrites (itself unsettled), the SIR format may be non-compliant with the gate's structural requirement. Even if the gate does not apply, keeping verification evidence only in comment blocks means future principle readers cannot locate it by reading the principle text alone. **Impact: medium** (precedent for non-compliant verification-block format; audit burden increases).

- **Registry-emission enforcement chain is SIR-only**: The SIR's Criterion 1 self-assessment for plain-language pairing says enforcement is "validated at registry-emission time per Principle XV's registry-as-extension-interface clarification." But XVI's body does not reference this enforcement mechanism — the connection exists only in the SIR comment block, not in the principle text. XV's Clarification v2.3.1 establishes the registry as the extension interface; XVI's plain-language requirement relies on that registry-emission validation but does not say so, leaving the enforcement chain invisible to readers of the principle body. **Impact: medium** (enforcement chain is discoverable only by reading SIR alongside principle text).

- **"Shape" is used in two incompatible senses across IX and XVI**: Principle IX's behavior-over-shape extension defines "shape test" as checking structural properties of test assertions (field presence, type, non-null status) rather than behavioral properties. Principle XVI's v2.3.2 clarification uses "shape" for objective-function structure: "cross-run variance in the assembled objective function's *shape* (parameter names, template selection, gap-identifier set) is prohibited." These two senses are technically distinct and context-disambiguated within each principle, but a cross-principle compliance lint grepping for "shape" will surface both, requiring disambiguation logic. **Impact: low** (no runtime impact; tooling and future-author confusion risk as the codebase grows).

---

### Off-Base Assumptions

- **The gate implicitly applies to headline rewrites without gate text covering that case**: The SIR's Criterion 1/2/3 self-assessment presupposes that the Constitutional Inclusion Criteria gate applies to in-place rewrites of grandfathered principles. The gate text (Governance, Constitutional Inclusion Criteria) reads: "This gate applies **prospectively** — to amendments landing after v2.4.0. Existing principles I-XXVII are grandfathered." This is ambiguous: "prospective amendments" may mean all amendments landing after v2.4.0 (including modifications to grandfathered principles) or only new-principle additions. The Extension blocks paragraph suggests the former interpretation is partially correct — extensions to grandfathered principles ARE subject to Criterion 1. But a headline rewrite is neither a new principle nor an Extension block. The assumption that the gate applies and is satisfied by the SIR's self-assessment is plausible but not derivable from gate text as written; it creates an unacknowledged precedent rather than a documented one.

- **XVI has unilateral jurisdiction to MUST-require plugin output format**: The rewrite's headline elevation of plain-language output pairing treats this as XVI's structural requirement (mathematical transparency). But XVI's body says "Plugin recommendations (equilibrium scores, convergence predictions, config suggestions) MUST include plain-language explanations." Plugin recommendations are plugin output — that places the constraint in XV's domain (plugin output governance: "data flows one direction: core produces deliberation artifacts → plugins consume them"). XV governs what plugins can and cannot do with their output, including the warn-and-continue enforcement model. The assumption that XVI can impose a MUST on plugin output format independently of XV's enforcement machinery — without invoking XV's coordination protocol or specifying enforcement mode — is not grounded by either principle's text. The MUST is orphaned from the enforcement mechanism that would give it operational meaning.

---

### Actionable Recommendations

1. **Specify plain-language-pairing enforcement mode** (Priority: P1)
   - **Current state**: Principle XVI's body says "Plugin recommendations... MUST include plain-language explanations alongside numerical outputs." No enforcement mode is specified. Principle XV says "Plugin failure MUST NOT block core execution — warnings only."
   - **Proposed change**: Add one sentence to XVI's third bullet: "A plugin recommendation that omits plain-language pairing is treated as malformed plugin output under Principle XV's warn-and-continue protocol; it DOES NOT block core deliberation execution."
   - **Rationale**: Without this sentence, XVI's MUST and XV's "MUST NOT block" are in silent conflict. The warn-and-continue interpretation is almost certainly the intended behavior given the SIR's design-intent framing, but silent conflicts produce divergent implementations.
   - **Risk if ignored**: A future implementor adds schema-level rejection of non-paired plugin output, triggering a core execution failure — a direct XV violation — while citing XVI's MUST as justification. The conflict surfaces only after a production incident.

2. **Acknowledge headline-rewrite precedent in Governance gate text** (Priority: P2)
   - **Current state**: The Governance gate covers new principles (fully gated), Extension/Clarification blocks (Criterion 1 required), and wording-level clarifications (exempt). Headline rewrites of grandfathered principles are not named.
   - **Proposed change**: Add one sentence to the Governance gate's Extension blocks paragraph: "Headline rewrites of grandfathered principles that restructure existing body content into a new headline without introducing new normative requirements are treated as wording-level amendments; the SIR MUST include an explicit claim that no new normative requirements are introduced."
   - **Rationale**: The Option A rewrite creates this precedent de facto. Making it explicit prevents future amendments to VI or X from citing the XVI rewrite as license for broader gate bypass without the same constraint.
   - **Risk if ignored**: Future amendments to other grandfathered principles invoke the XVI rewrite as precedent for full gate bypass, introducing new normative requirements under the guise of headline restructuring.

3. **Update VII's parenthetical for navigability** (Priority: P2)
   - **Current state**: Principle VII says "structurally identical output (narrowed by Principle XVI for LLM gap-filling output)." XVI's headline now names three structural requirements unrelated to LLM gap-filling; the carve-out is in XVI's v2.3.2 Clarification block.
   - **Proposed change**: Update VII's parenthetical to "(narrowed by Principle XVI's v2.3.2 Clarification block for LLM gap-filling output)" to anchor the reader to the correct subsection of XVI.
   - **Rationale**: A reader following VII's parenthetical to XVI now encounters three structural requirements before reaching the carve-out. One additional word reduces audit traversal cost.
   - **Risk if ignored**: Readers auditing the VII↔XVI relationship must read past XVI's restructured headline to locate the carve-out; navigability degrades with each future XVI amendment.

4. **Add structured Verification block to XVI's principle body** (Priority: P2)
   - **Current state**: The Criterion 1/2/3 self-assessment exists in the SIR comment block (outside the principle body). The gate's Extension blocks paragraph requires a structured `Verification:` block in the principle body when new normative requirements are introduced.
   - **Proposed change**: Add a `**Verification (v2.6.0):**` block inside Principle XVI's body (after the headline paragraph), listing the three mechanical checks: (a) spec 014 FR-012/SC-004 lint for parameter pinning, (b) parity test for shape determinism, (c) schema lint for plain-language pairing. Reference the SIR for full Criterion 1/2/3 self-assessment.
   - **Rationale**: SIRs are preserved for audit trail but are comment blocks; the principle body is what future readers and agents load as constitutional text. Keeping verification evidence only in the SIR makes compliance audits dependent on reading comment blocks.
   - **Risk if ignored**: Future amendments modifying XVI cannot locate Criterion 1 verification evidence by reading the principle body alone; compliance audit burden increases with each amendment cycle.

5. **Cross-reference XV's registry-emission enforcement in XVI's plain-language bullet** (Priority: P2)
   - **Current state**: XVI's third bullet says "Plugin recommendations... MUST include plain-language explanations alongside numerical outputs." No reference to XV's enforcement machinery or the registry-emission validation described in the SIR.
   - **Proposed change**: Add a parenthetical to the bullet: "(enforced at registry-emission time per Principle XV's registry-as-extension-interface clarification; violations are malformed plugin output subject to XV's warn-and-continue protocol)."
   - **Rationale**: The enforcement chain is currently SIR-only. Surfacing it in the principle body makes the operational meaning of XVI's MUST self-contained.
   - **Risk if ignored**: See Recommendation 1's risk; this recommendation provides belt-and-suspenders clarity alongside Recommendation 1's explicit sentence.

6. **Disambiguate "shape" across Principles IX and XVI** (Priority: P3)
   - **Current state**: IX uses "shape test" for test-assertion quality (field presence, type, non-null status). XVI's v2.3.2 clarification uses "shape" for objective-function structure (parameter names, template selection, gap-identifier set).
   - **Proposed change**: In XVI's v2.3.2 clarification, replace "cross-run variance in the assembled objective function's *shape*" with "cross-run variance in the assembled objective function's *structure*" and update the inline parenthetical: "structure (parameter names, template selection, gap-identifier set)."
   - **Rationale**: "Structure" is not part of IX's behavior-over-shape vocabulary. The collision disappears. Meaning in XVI is unchanged.
   - **Risk if ignored**: Compliance lints or future authors grepping for "shape" to locate IX's behavioral testing requirements surface XVI's structural requirement as a false match; disambiguation logic is required rather than terminological clarity.

7. **Document headline-rewrite category in SIR's governance log entry** (Priority: P3)
   - **Current state**: The SIR describes the amendment as an "in-place refactor" but does not explicitly classify the gate category it occupies or acknowledge the precedent it creates.
   - **Proposed change**: Add one sentence to the SIR's Rationale section: "This amendment is classified as a headline rewrite of a grandfathered principle — a category not explicitly named in the gate text — and creates the precedent that such rewrites are treated as wording-level amendments when they introduce no new normative requirements and include an explicit SIR attestation to that effect."
   - **Rationale**: The gate's governance design includes precedent logging (referenced in the Extension blocks paragraph). Making the precedent explicit in the SIR allows future amendments to cite it cleanly rather than re-deriving the classification from first principles.
   - **Risk if ignored**: Future amendments to VI or X must re-argue the classification from scratch, with no canonical precedent to cite, increasing governance overhead and dispute likelihood.

---

### Referenced Documentation

- `CONSTITUTION-v2.6.0-candidate.md` — sections cited:
  - Principle VII: bilateral carve-out parenthetical ("narrowed by Principle XVI for LLM gap-filling output")
  - Principle VIII: vocabulary alignment parenthetical ("co-extensive with VIII's 'mechanical'")
  - Principle IX: behavior-over-shape extension ("shape test" definition, operational test examples)
  - Principle XV: Plugin Isolation (warn-and-continue enforcement, plugin output namespace, registry-as-extension-interface Clarification v2.3.1)
  - Principle XVI: headline paragraph (three structural requirements), 3-stage pipeline (stage 2 stochastic, stage 3 deterministic assembly), third bullet (plain-language pairing MUST), v2.3.2 Clarification block (deliberation-run definition, VII carve-out, cross-run variance prohibition, Observability sub-bullet, Enforcement sub-bullet, Falsification sub-bullet)
  - Principle XXIV: Safety-Critical Defense-in-Depth (three-layer defense framework)
  - Principle XXVIII: Test-Fix Boundary Preservation (skip discipline, diff-shape categorization — spot-checked for XVI Enforcement sub-bullet)
  - Governance: Constitutional Inclusion Criteria gate (Criterion 1/2/3 definitions, prospective-only clause, Extension blocks paragraph, worked examples, calibration guidance)
  - SIR comment block (v2.5.0→v2.6.0): Criterion 1/2/3 self-assessment, registry-emission enforcement claim, Rationale section, governance log entry