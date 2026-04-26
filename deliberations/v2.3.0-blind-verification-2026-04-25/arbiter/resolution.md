I need to read the required files in order to conduct this arbitration. Let me start with my grounding document.

Now let me read the Phase 5 synthesis to understand the synthesizer's assessment.

Now let me read each agent's Phase 4 dispute document to understand their final positions.

Based on my review of all documents, I will now provide my arbitration resolution.

---

### Process Note

This arbitration was triggered by the `always` condition specified in the deliberation configuration. Three disputes remain from the Phase 5 synthesis following a **cooperative** deliberation involving three agents: skeptic, skeptic-2, and practitioner. This is a **cooperative** deliberation with subject arbitration, where I am the independent arbiter reviewing the conversus constitution itself based on the three agents' findings.

### Decision Framework

The key constitutional principles relevant to the remaining disputes are:

- **Principle XI (Single Source of Truth)**: "Every piece of information MUST have exactly one authoritative source. All other representations MUST be derived from that source, not maintained independently." (Lines 237-243)
- **Principle XV (Plugin Isolation)**: "Plugins consume core artifacts; they MUST NOT modify them... Plugin output goes to a separate namespace." (Lines 351-368) 
- **Principle XVI (Mathematical Transparency)**: "When optimization drives decisions, the user MUST understand what is being optimized... The 3-stage pipeline ensures the math reflects user intent." (Lines 374-404)
- **Principle XVIII (Progressive Disclosure Contract)**: "Every subcommand handler extracted to a reference file MUST have a specific, unambiguous load trigger in the root SKILL.md." (Lines 436-462)
- **Principle XXVII (Operator-Configurable Tool Surface)**: "The tool surface exposed by a deployed conversus instance MUST be configurable by the operator... This asymmetry preserves deterministic capability discovery while allowing deployment-time hardening." (Lines 701-722)
- **Architectural Invariant Concept**: Throughout the constitution, there's a distinction between system-breaking violations vs. system-degrading violations (referenced in principles requiring coordination across consumers, preventing silent failures, etc.)
- **Constitutional Scope Boundaries**: The governance section establishes that the constitution "supersedes conflicting guidance" and requires amendments for changes (Lines 758-772)

### Binding Decisions

#### Dispute: Plugin Registry Boundary Priority

**Positions:**
- **skeptic**: Plugin boundary concerns are lower priority compared to core constitutional scope reduction work, treating plugin boundaries as narrow interface concerns when broader constitutional scope inflation is the fundamental issue (skeptic disputes)
- **skeptic-2**: Maintains "Clarify Plugin Registry Boundary" as P1 architectural foundation, arguing architectural boundary integrity is prerequisite for implementation optimization and boundaries must be unambiguous (skeptic-2 disputes)

**Synthesizer's assessment:** The synthesizer found skeptic-2's position stronger because plugin boundaries represent architectural constraints unique to this system, while recommending that plugin boundary clarification be handled as part of broader architectural boundary work following architectural invariant classification.

**Ruling:** Adopt skeptic-2's position that plugin registry boundary clarification is architecturally foundational, but implement it as part of the broader architectural boundary work following architectural invariant classification.

**Grounding citation:** Principle XV (Plugin Isolation) states "plugins extend the registry; operators filter the registered set" and coordinates with Principle XXVII (Operator-Configurable Tool Surface) to create "clean separation," but this separation relies on a clearly defined registry interface. Principle XVIII (Progressive Disclosure Contract) requires "specific, unambiguous load triggers" and prohibits "Generic triggers like 'see references/'" which defeats "the context-reduction purpose of extraction." The same principle of unambiguous boundaries applies to plugin interfaces.

**Rationale:** Plugin boundaries represent architectural constraints unique to this prompt-orchestrated system, distinguishing them from general engineering practices. The constitution explicitly coordinates Principles XV and XXVII around registry boundaries, making this a constitutionally-mandated architectural invariant. While skeptic's scope reduction concerns are valid, the registry boundary is specifically called out in the constitutional text as requiring clarity.

**Rejected position:** skeptic's position treats plugin boundaries as operational detail when the constitution explicitly establishes the registry as a coordination point between plugin capabilities and operator control. The constitutional text makes this an architectural boundary question, not merely an operational interface refinement.

**Required changes:** Add clarifying language to Principle XV stating "the capability registry constitutes an explicit extension interface separate from core deliberation logic" and specify in Principle XXVII that "registry modifications are configuration changes affecting tool availability, not behavioral modifications to deliberation process."

#### Dispute: Mathematical Reproducibility Amendment Scope

**Positions:**
- **skeptic-2**: Wants constitutional clarification of Principle XVI to resolve determinism/LLM-involvement tension, arguing Principle XVI creates logical contradiction requiring constitutional resolution (skeptic-2 disputes)
- **skeptic**: Wants mathematical reproducibility handled in operational documentation to avoid constitutional expansion, arguing constitutional amendments should be reserved for architectural invariants (skeptic disputes)

**Synthesizer's assessment:** The synthesizer found skeptic-2's position stronger because the interaction between LLM gap-filling and determinism requirements creates genuine logical inconsistency within a principle that is clearly architectural.

**Ruling:** Adopt skeptic-2's position to add constitutional clarification to Principle XVI resolving the determinism/LLM-involvement tension.

**Grounding citation:** Principle XVI (Mathematical Transparency) simultaneously requires "deterministic assembly" and "pre-defined math" while acknowledging "LLM gap-filling" in parameter translation. This creates a direct logical contradiction within the constitutional text itself. Principle XI (Single Source of Truth) states "When two sources disagree, it is always a bug — and the fix is always to eliminate the duplicate, not reconcile it." The contradiction within Principle XVI violates this fundamental requirement.

**Rationale:** Mathematical transparency is clearly an architectural concern for optimization systems, as established by Principle XVI's placement and scope. The contradiction between determinism requirements and LLM involvement is not operational detail but a fundamental logical inconsistency within the constitutional text itself. This must be resolved constitutionally because operational documentation cannot override constitutional contradictions.

**Rejected position:** skeptic's position would leave a logical contradiction in the constitutional text while relegating the resolution to operational documentation. This violates the constitutional hierarchy established in the governance section and fails to address the internal inconsistency that undermines Principle XVI's enforceability.

**Required changes:** Add clarifying sentence to Principle XVI stating "LLM gap-filling occurs once during setup with results cached for deterministic reuse" or "prompts for gap-filling are engineered to be sufficiently deterministic to ensure reproducible parameter values."

#### Dispute: Scope of Automated Enforcement

**Positions:**
- **practitioner**: Wants automated enforcement for all surviving architectural invariants after classification, arguing many architectural constraints can be mechanically verified once properly defined (practitioner disputes)
- **skeptic-2**: Limits automation to mechanically verifiable compliance while reserving interpretive issues for formal governance, arguing formal governance requires human judgment (skeptic-2 revision)

**Synthesizer's assessment:** The synthesizer found practitioner's position stronger because architectural boundaries can be mechanically verifiable once interfaces are defined, and the hybrid approach risks creating compliance gaps.

**Ruling:** Adopt practitioner's position establishing mechanical verification as the test for constitutional inclusion, with principles that resist automatic verification belonging in operational guidance.

**Grounding citation:** The constitutional structure throughout establishes clear, enforceable boundaries (Principle XVIII requires "specific, unambiguous load triggers," Principle XV establishes clear plugin boundaries, Principle XI requires "exactly one authoritative source"). The constitution's emphasis on deterministic, mechanical processes (Principle VII "Reproducibility Over Inconsistency," Principle VIII "Templating Engines Over Inference") establishes mechanical verification as aligned with constitutional philosophy.

**Rationale:** The constitutional text consistently favors mechanical, deterministic processes over interpretive judgment. Architectural boundaries that can be mechanically verified once properly defined (like "plugins consume but never modify core artifacts" or "every subcommand handler has specific load trigger") represent the type of clear, enforceable invariants the constitution establishes throughout. Creating enforcement gaps through hybrid approaches contradicts the constitutional emphasis on clear boundaries.

**Rejected position:** skeptic-2's hybrid approach creates the kind of ambiguity the constitution works to eliminate. While formal governance has value, the constitutional text establishes mechanical verification and clear boundaries as foundational principles. Interpretive issues that resist mechanical verification belong in operational guidance, not constitutional requirements.

**Required changes:** Establish in the governance section that "mechanical verification capability is required for constitutional inclusion—principles that cannot be automatically verified belong in operational guidance where human judgment is appropriate."

### Summary of Changes Required

1. **Plugin Registry Boundary Clarification** (from Dispute: Plugin Registry Boundary Priority): Add clarifying language to Principles XV and XXVII defining the registry interface as an explicit architectural boundary. Priority: P1.

2. **Mathematical Reproducibility Clarification** (from Dispute: Mathematical Reproducibility Amendment Scope): Add sentence to Principle XVI resolving the determinism/LLM-involvement logical contradiction. Priority: P1.

3. **Mechanical Verification Requirement** (from Dispute: Scope of Automated Enforcement): Establish mechanical verification capability as requirement for constitutional inclusion in governance section. Priority: P2.

### Confidence Assessment

| Dispute | Ruling | Confidence | Basis |
|---------|--------|------------|-------|
| Plugin Registry Boundary Priority | Adopt skeptic-2's position with implementation integration | High | Clear constitutional text in XV and XXVII establishes registry as architectural boundary |
| Mathematical Reproducibility Amendment Scope | Adopt skeptic-2's constitutional clarification | High | Direct logical contradiction within Principle XVI text violates constitutional coherence |
| Scope of Automated Enforcement | Adopt practitioner's mechanical verification standard | Medium | Constitutional emphasis on mechanical processes supports this but requires interpretation of constitutional philosophy |

The deliberation quality was high, with all agents demonstrating intellectual honesty and modifying positions based on evidence. The remaining disputes represent genuine architectural questions rather than positions that could have been resolved through better analysis. The constitutional text provides sufficient grounding for resolution, though the enforcement mechanism dispute required interpreting the constitutional philosophy rather than citing explicit text. This indicates the constitution is generally well-structured but needs clarification in the identified areas.