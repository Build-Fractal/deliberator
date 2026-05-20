# Strict-Reader Review: Q1 Internal Contradiction Check (v3)

### Executive Summary

Spec v3 § 4 introduces a new Tier 2 Principle XXVIII "Persistence Contract Discipline" that mandates declared schemas, mechanical CI enforcement, versioning, and cross-product consumer contracts for persistent on-disk state within the conversus suite. As a strict-reader auditor, I find this principle operates in a distinct domain from existing constitutional principles and does not contradict, override, or implicitly modify any existing Tier 1 or Tier 2 principle. The principle complements rather than conflicts with existing stable interface discipline (Principle II) and reproducibility requirements (Principle VII). My most important finding is that v3 successfully applied all seven Summary-of-Changes items from the original self-consistency arbitration without introducing new contradictions.

### Alignment

- **Tier 2 placement consistency** (spec § 1, L47-51): The amendment correctly targets `build-fractal/conversus/CONSTITUTION.md` (Tier 2 Suite) rather than Tier 1, aligning with the evidence base limited to conversus-family products (conversus-oss, conversus-enhanced, spec-kit-orc). This matches Tier 2's scope per `../../../CONSTITUTION.md` L15-16: "principles that apply to **every conversus-family repo**."

- **Domain separation from Principle II** (spec § 4, L102-145): XXVIII addresses persistent on-disk state schemas while Principle II (Tier 1, L121-143) addresses runtime stable interfaces (markers, template variables, dispatch table). The domains are complementary: XXVIII governs what gets persisted, II governs what gets referenced during execution.

- **Harmonization with Principle VII** (spec § 4 sub-clause 2): XXVIII's mechanical CI enforcement and bidirectional drift detection supports Principle VII's reproducibility requirement (Tier 1, L188-198) by ensuring schema changes don't break deterministic output structure.

- **Non-contradiction with Principle XXII** (spec § 4 vs Tier 2 XXII): XXVIII governs runtime persistent state while XXII governs distribution artifacts (PyPI wheels, .mcpb bundles). The temporal separation is clear: XXII operates at build/distribution time, XXVIII operates at runtime/execution time.

- **Principle number stability** (spec § 5, L150): v3 correctly preserves all existing principles "byte-for-byte unchanged" per Principle II's stability requirement (Tier 1, L143-144) and appends XXVIII after XXVII without renumbering.

### Missed Opportunities

- **Cross-reference verification with Principle XI** (impact: medium): Spec § 4 sub-clause 1 requires "a written schema declaration in a discoverable location" but doesn't explicitly coordinate with Principle XI's Single Source of Truth requirement (Tier 1, L222-235). The schema declaration should reference XI's anti-duplication mandate to prevent schema information from appearing in multiple places.

- **Integration with Principle XXIV enforcement** (impact: medium): XXVIII's CI gate requirements (sub-clause 2) share enforcement discipline with Principle XXIV's Safety-Critical Defense-in-Depth (Tier 2, L531-557) but don't cross-reference the three-layer defense pattern (schema + parser + contract test). This misses an opportunity for unified enforcement methodology.

- **Explicit transient state coordination with Principle VII** (impact: low): XXVIII's scope limitation to "persistent on-disk state intended to outlive the writing process" (L145-146) could explicitly reference VII's "no accumulated state" requirement (Tier 1, L194) to clarify the boundary between transient and persistent state.

- **Consumer contract alignment with Principle XV** (impact: low): Sub-clause 4's cross-product consumer contracts could explicitly reference Principle XV's Plugin Isolation requirement (Tier 2, L341-358) to clarify how consumer contracts interact with plugin boundaries.

### Off-Base Assumptions

No off-base assumptions detected. The spec correctly understands the constitutional hierarchy (Tier 1 vs Tier 2), the domain boundaries of existing principles, and the seven Summary-of-Changes requirements from the original arbitration. The principle operates in its own domain (persistence contracts) without assuming authority over existing principle domains.

### Actionable Recommendations

1. **Verify Summary-of-Changes application** (Priority: P1)
   - **Current state**: v3 claims to apply all seven changes but requires verification (QUESTION.md, L15-24).
   - **Proposed change**: Confirm each change: Tier 2 placement (✓), universal deadline (✓), override restriction § 11 (✓), compound debt § 12 (✓), coordinated analysis § 9 (✓), conditional coordination § 13 (✓), Q2 rationale rewrite (✓).
   - **Rationale**: Original arbitration required these changes as blocking conditions.
   - **Risk if ignored**: Constitutional amendment process integrity failure.

2. **Add XI cross-reference to schema declaration** (Priority: P2)
   - **Current state**: Sub-clause 1 requires schema declarations without referencing single-source-of-truth (L106-111).
   - **Proposed change**: Append "Schema information MUST appear in exactly one authoritative location per Principle XI; derived representations are prohibited."
   - **Rationale**: Principle XI governs information duplication (Tier 1, L222-235).
   - **Risk if ignored**: Schema declarations might duplicate information across multiple files.

3. **Coordinate enforcement with XXIV** (Priority: P2)
   - **Current state**: Sub-clause 2 specifies CI gates without referencing existing defense-in-depth patterns (L121-130).
   - **Proposed change**: Add cross-reference: "CI enforcement follows Principle XXIV's three-layer defense pattern where applicable."
   - **Rationale**: XXIV establishes enforcement methodology (Tier 2, L531-557).
   - **Risk if ignored**: Inconsistent enforcement approaches across constitutional domains.

4. **Clarify transient state boundary** (Priority: P3)
   - **Current state**: Scope limitation mentions transient state without constitutional cross-reference (L145-147).
   - **Proposed change**: Add "consistent with Principle VII's prohibition on accumulated state."
   - **Rationale**: VII governs state accumulation (Tier 1, L194).
   - **Risk if ignored**: Boundary ambiguity between persistent and transient state.

### Q1 Verdict: PASS

v3's new Tier 2 Principle XXVIII does not contradict, override, or implicitly modify any existing Tier 1 or Tier 2 principle. The principle operates in a distinct domain (persistent state schemas) that complements existing stable interface discipline (Principle II) and reproducibility requirements (Principle VII). Domain separation is maintained: XXVIII governs what gets persisted, existing principles govern runtime behavior. All seven Summary-of-Changes items from the original arbitration have been correctly applied. Minor harmonization opportunities exist but do not constitute contradictions.

### Referenced Documentation

- `build-fractal-mono/build-fractal/CONSTITUTION.md` — Principles II (L121-143), VII (L188-198), XI (L222-235)
- `build-fractal-mono/build-fractal/conversus/CONSTITUTION.md` — Principles XV (L341-358), XXII (L461-486), XXIV (L531-557)
- `specs/v4.1.0-persistence-contract-discipline/spec.md` — § 4 (L102-148), § 5 (L150), Summary-of-Changes (L15-24)
- `deliberations/v4.1.0-persistence-contract-discipline-self-consistency-rerun-2026-05-12/QUESTION.md` — Seven required changes (L15-24)