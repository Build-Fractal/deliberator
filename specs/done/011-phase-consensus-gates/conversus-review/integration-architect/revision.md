# Cooperative Revision — Phase 3

**Agent**: integration-architect
**Iteration**: 1

---

### Recommendation Dispositions

#### Recommendation 1: Add Dispute-Parsing error propagation to gate verdict
- **Original position**: Parsing failures should produce ERROR verdict (exit code 2), not BLOCK.
- **Disposition**: Modified
- **Explanation**: devils-advocate's cross-review (Dangerous Contradictions, "Dispute-Parsing failure: ERROR vs. nuanced handling") proposed a two-tier approach. functional-typing's Recommendation 5 in revision also converged on the two-tier model. I now agree the distinction is important. Modified recommendation: "(1) No synthesis file = ERROR (exit code 2). (2) Synthesis exists but Dispute-Parsing uses fallback (no markers, heading-based or default) = BLOCK (exit code 1) with a note in gate-result.md: 'Dispute count determined via fallback parsing.' The deliberation ran and likely found issues — ERROR would misrepresent the situation." This is substantively the same as devils-advocate's proposal and functional-typing's modified Rec 5.

#### Recommendation 2: Include stagnation and iterations in gate config schema
- **Original position**: Gate config should include `stagnation` and `iterations` fields with pass-through to the generated config.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged the substance. functional-typing's cross-review (Tensions, "Stagnation and iterations in gate config") noted that new fields need validation rules. This is correct and does not undermine the recommendation — it strengthens it by requiring completeness. The recommendation stands with an addition: new fields must include validation rules consistent with the run engine (SKILL.md L224-232).

#### Recommendation 3: Support prior context for gate re-runs
- **Original position**: Automatic `prior_on_rerun: true` injects previous attempt's synthesis as prior context.
- **Disposition**: Modified
- **Explanation**: devils-advocate's cross-review (Dangerous Contradictions, "Prior context injection for re-runs") raised a legitimate concern: prior context from a false-positive run could bias the re-run. The modification: `prior_on_rerun` remains opt-in (default: false). When enabled, the gate handler injects the prior context AND emits: "Prior context from attempt {N-1} injected. Previous findings may influence this run." The gate-result.md should include `## Prior Context: attempt-{N-1}/summary/final.md` when active. This preserves the feature's value while making the influence visible and auditable.

#### Recommendation 4: Formalize SC-001 through SC-006 verification paths
- **Original position**: Add a verification mapping table from SC to SKILL.md implementation points.
- **Disposition**: Modified
- **Explanation**: devils-advocate's cross-review (Tensions, "SC verification formalism") argued this mapping is best as a review artifact, not embedded in the spec. I agree — embedding it in the spec creates maintenance burden. Modified recommendation: The SC mapping should be a review artifact (produced during review/test, not in the spec). However, the spec should ensure each SC is testable by including: "SC-001 is verified by: running a gate with `pass: converged` against an artifact that produces 0 disputes (expect PASS) and against one that produces 1+ disputes (expect BLOCK)." This makes SCs self-documenting for test design.

#### Recommendation 5: Define explicit flag-override behavior
- **Original position**: CLI flags override gate configuration values.
- **Disposition**: Surviving
- **Explanation**: functional-typing independently made the same recommendation (Rec 3). Both cross-reviews identified this as a safe agreement. No reviewer challenged it. Unanimous support.

#### Recommendation 6: Add validate_templates pass-through
- **Original position**: Include `validate_templates: true` in the generated config. Allow gate config override.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. Template validation catches config errors before agent launches, which is especially valuable in CI/CD where failed agent launches waste resources. The recommendation stands as stated.

#### Recommendation 7: Clarify generated config is passed by reference
- **Original position**: The gate writes the config for auditability, then uses the in-memory config for execution.
- **Disposition**: Surviving
- **Explanation**: No cross-review challenged this. functional-typing's cross-review (Tensions, "Generated config documentation") noted it as complementary to their Rec 8 (YAML comment headers). Both can be implemented together.

#### Recommendation 8: Specify max_disputes N validation
- **Original position**: N must be a non-negative integer. 0 is valid and equivalent to converged.
- **Disposition**: Surviving
- **Explanation**: functional-typing's revised Recommendation 2 now aligns with this position (non-negative integer, 0 valid). The internal inconsistency in functional-typing's original review has been resolved in their favor of the same constraint I proposed. Unanimous agreement.

### New Recommendations

- **Add gate-level arbiter defaults for strict gates** (Priority: P3)
  - **Triggered by**: My own Missed Opportunities section noted this gap, and no cross-review challenged it. However, during revision, I realize this is a P3 nice-to-have, not a structural requirement. Strict gates benefit from arbitration, but making it a default adds complexity to the gate schema.
  - **Proposed change**: Add to the gate documentation (not as a default, but as guidance): "For strict gates (pass: converged), consider adding an arbiter to resolve disputes that would otherwise block the gate. Example: `arbiter: { name: gate-arbiter, preset: role/balanced-arbiter, grounding: path/to/spec.md, trigger: disputes_remain }`."
  - **Rationale**: Guidance helps users configure effective gates without imposing defaults.

### Position Summary

I withdrew 0 recommendations, modified 3 (Recs 1, 3, 4), and maintained 5 (Recs 2, 5, 6, 7, 8). I added 1 new recommendation (gate-level arbiter guidance, P3).

The most significant change was the Dispute-Parsing error propagation (Rec 1). My original binary position (all parse failures = ERROR) was too aggressive. devils-advocate's two-tier approach correctly distinguishes between "engine failed" (ERROR) and "engine ran but output is hard to parse" (BLOCK). This is a meaningful improvement.

My remaining highest-priority recommendation is Recommendation 2 (stagnation and iterations in gate config), because these are core engine features that gates should expose to enable multi-round quality checks. Without them, gates with `rounds > 1` run without stagnation detection and cannot use multi-iteration depth.
