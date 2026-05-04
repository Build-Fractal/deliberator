### Executive Summary

The X restoration candidate proposes to reinstate Principle X with a refactored headline "Predictable Output Tree" that elevates structural invariants over the subjective "Zen of Python Output" framing. The candidate aims to satisfy Constitutional Inclusion Criterion 1 by providing mechanically verifiable assertions for output structure. From a verification concreteness perspective, the candidate makes significant progress toward mechanical enforceability but contains critical gaps in three of its four invariants. The Verification block provides concrete guidance for synthesis path verification but leaves substantial implementation gaps for depth-bound checking, malformed-output detection, and per-file focus enforcement. My assessment is that while the structural approach is sound, the verification mechanisms need significant clarification to meet the "sketchable in one paragraph" standard established by Principles XI, XII, XIII, and XVI.

### Alignment

- **Synthesis path verification specificity** (`L85-90`): The candidate names `engine/tests/test_phases.py` as the test surface and specifies "`summary/final.md` exists with non-empty content after every mock-provider cooperative run" which provides sufficient detail for direct implementation. This matches the concrete verification pattern established in Principle XVI's Clarification v2.3.2 Enforcement section.

- **Parity test framing** (`L85-87`): The candidate frames the synthesis verification as "analogous to existing tests covering Phase 5 synthesis output" which correctly leverages existing test infrastructure rather than requiring new test categories. This aligns with Principle XII's infrastructure reuse approach.

- **Multiple verification mechanisms** (`L85-93`): The candidate correctly identifies that different invariants require different verification approaches (parity tests, path-depth lints, warning-emission assertions, filename-purpose lints) rather than forcing a single verification pattern. This matches the multi-faceted verification approach in Principle XVI.

### Missed Opportunities

- **Mode-specific verification coverage** (`L85-87`): The verification only mentions "cooperative-mode run" but the principle claims to apply to all conversus runs. The Verification block should specify how other modes (deliberative, red-blue, etc.) are covered, particularly since the principle states "mode-specific equivalent at the documented path for other modes per `templates/<mode>/synthesis.md`". Impact: medium - leaves verification gaps for non-cooperative modes.

- **Depth-bound calculation specification** (`L90-91`): "Path-depth lint walking `output:`" lacks essential implementation details: what constitutes an "agent's own directory," how "ONE directory level below" is calculated, and how to distinguish agent-produced content from framework content. An engineer cannot implement this without additional specification. Impact: high - core invariant is unverifiable as written.

- **Malformed-output schema reference** (`L91-92`): "Warning-emission assertions in the artifacts test surface" assumes a definition of "malformed" exists but doesn't reference where. The verification needs either a schema reference or enumeration of malformed conditions (missing headers, invalid YAML frontmatter, etc.). Impact: high - cannot verify emission without defining what triggers it.

- **Per-mode whitelist structure** (`L92-93`): "Filename-purpose lint via a per-mode whitelist" references a whitelist that doesn't exist in current implementation. The verification should specify whitelist location (`schema/modes/*.yml`?) and structure, or acknowledge this as new infrastructure. Impact: medium - verification mechanism undefined.

- **Failure mode specification** (entire Verification block): None of the verification mechanisms specify their failure modes - CI red, warning annotations, exit codes, etc. Principle XVI's Enforcement section provides this detail ("contract test reproducing the failure scenario"). Impact: medium - engineers need to know how violations surface.

- **Cross-mode depth consistency** (`L70-72`): The depth-bound invariant mentions "agent's own directory" but doesn't address how this applies when agents share output directories or when framework components write to agent directories. The verification should address shared vs. isolated directory scenarios. Impact: medium - verification gaps in complex output scenarios.

### Off-Base Assumptions

- **"Artifacts test surface" assumption** (`L91-92`): The Verification block assumes an "artifacts test surface" exists as a distinct test category. Current test organization doesn't necessarily have this division - tests are organized by component/feature rather than by artifact type. The verification should reference specific test files or acknowledge new test infrastructure requirements.

- **Path-depth lint infrastructure assumption** (`L90-91`): The candidate assumes path-depth linting is straightforward to implement, but directory depth calculation in a multi-mode, multi-agent output tree requires significant parsing logic to distinguish legitimate nesting from violations. The complexity is understated.

### Actionable Recommendations

1. **Specify mode-specific synthesis paths** (Priority: P1)
   - **Current state**: Verification only covers "cooperative-mode run" (`L85-87`).
   - **Proposed change**: Add "Mode-specific synthesis paths verified via analogous tests in `engine/tests/test_phases.py` for each registered mode, asserting existence and non-empty content of the documented synthesis location per `templates/<mode>/synthesis.md`."
   - **Rationale**: The principle claims to apply to all modes but verification only covers one mode, creating a gap between claim and enforceability.
   - **Risk if ignored**: Mode-specific violations will not be caught, undermining the "predictable output tree" guarantee.

2. **Define depth-bound calculation** (Priority: P1)
   - **Current state**: "Path-depth lint walking `output:`" lacks implementation specification (`L90-91`).
   - **Proposed change**: Add "Depth-bound verification walks `output/` directory, identifies agent directories via `{agent_name}/` pattern, and flags any file more than one path component below the agent directory root (e.g., `agent1/subdir/subdir/file.md` violates; `agent1/subdir/file.md` complies)."
   - **Rationale**: Current wording cannot be implemented without defining the depth calculation and agent directory identification logic.
   - **Risk if ignored**: Core structural invariant remains unverifiable despite being the primary mechanical claim.

3. **Reference malformed-output schema** (Priority: P1)
   - **Current state**: "Malformed-output emission" lacks definition of "malformed" (`L91-92`).
   - **Proposed change**: Add "Malformed conditions defined in `schema/output-validation.yml` (missing required headers, invalid YAML frontmatter, empty content files). Warning-emission verified via log capture in `engine/tests/test_output_validation.py`."
   - **Rationale**: Cannot verify warning emission without defining what triggers warnings; needs schema reference or inline enumeration.
   - **Risk if ignored**: Warning-emission requirement is unenforceable, violating Criterion 1's mechanical verification requirement.

4. **Specify whitelist location and structure** (Priority: P2)
   - **Current state**: "Per-mode whitelist" referenced but undefined (`L92-93`).
   - **Proposed change**: Add "Per-mode whitelist in `schema/modes/{mode}.yml` under `output_files:` field, mapping filename patterns to purpose descriptions. Lint verifies each output file matches exactly one whitelist entry."
   - **Rationale**: Verification mechanism references undefined infrastructure; needs concrete location and structure.
   - **Risk if ignored**: Per-file focus verification cannot be implemented, leaving one of four invariants unenforceable.

5. **Add failure mode specification** (Priority: P2)
   - **Current state**: Verification mechanisms lack failure mode details (entire block).
   - **Proposed change**: Add sentence: "All verification failures surface as CI red via pytest assertions (synthesis path, malformed-output emission tests) or pre-commit hook failures (depth-bound lint, per-file focus lint)."
   - **Rationale**: Engineers need to understand how violations are detected and surfaced; matches Principle XVI's failure scenario specification pattern.
   - **Risk if ignored**: Unclear enforcement reduces confidence in mechanical verification claims.

6. **Acknowledge new infrastructure requirements** (Priority: P2)
   - **Current state**: Verification assumes infrastructure exists without noting what's new.
   - **Proposed change**: Add clarifying sentence: "Implementation requires new `schema/output-validation.yml` and extension of existing mode schemas with `output_files:` field."
   - **Rationale**: Transparent about implementation requirements; avoids false impression that verification can be implemented immediately.
   - **Risk if ignored**: Implementation effort is understated, potentially affecting feasibility assessment.

7. **Cross-reference existing test patterns** (Priority: P3)
   - **Current state**: Only synthesis path test references existing patterns.
   - **Proposed change**: Add "Warning-emission tests follow existing pattern in `engine/tests/test_validation.py`; lint implementations follow existing pattern in `scripts/lint-*.py`."
   - **Rationale**: Leverages established test and lint infrastructure patterns for consistency.
   - **Risk if ignored**: Minor - verification mechanisms might diverge from established patterns unnecessarily.

### Referenced Documentation

- `X-path-c-restoration-candidate.md` — sections/lines cited: L70-72, L85-93
- `CONSTITUTION.md` — sections/lines cited: XVI Clarification v2.3.2 Enforcement section