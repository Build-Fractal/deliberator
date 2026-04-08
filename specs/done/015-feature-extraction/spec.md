# Feature Specification: Feature Extraction Pipeline

**Feature ID**: `015-feature-extraction`
**Created**: 2026-03-22
**Status**: Draft
**Depends On**: `012-game-form-schemas` (game form definitions, mode-to-form mapping), `013-objective-function-templates` (parameter types, function derivation sources)
**Origin**: Decomposed from archived `007-game-engine` vision (Section 4: Feature Extraction: Text -> Numbers, Section 11 Approach 1: Structured Extraction). The bridge between LLM deliberation text and numerical game theory vectors.

---

## 1. Feature Summary

Convert conversus deliberation artifacts (markdown files from Phases 1-6) into numerical feature vectors suitable for game theory analysis. This is the critical bridge between the template-driven deliberation engine (text) and the mathematical plugin layer (numbers).

Feature extraction is deterministic: the same deliberation artifacts always produce the same feature vectors. Extraction uses structured parsing of conversus's predictable output format (headings, dispositions, structural markers). No LLM is involved in extraction.

The pipeline reads Phase 3 revisions (recommendation dispositions), Phase 4 disputes (counts and topics), and Phase 5 synthesis (convergence assessments). It produces a `features.json` file in the output directory that plugins consume.

**What changes**: New `conversus-features` package with per-mode feature schemas and extraction rules. New `features.json` output artifact.

**What does not change**: SKILL.md. Deliberation engine. Template system. Core output format.

---

## 2. Per-Mode Feature Schemas

### Cooperative Mode

| Feature | Source | Extraction Rule |
|---------|--------|-----------------|
| Position vector | Phase 1 review / Phase 3 revision | Per recommendation: P1=3, P2=2, P3=1, withdrawn=0. Vector length = max recommendations across agents. |
| Concession rate | Phase 3 revision | (withdrawn + modified) / total recommendations per agent |
| Dispute count | Phase 4 disputes | Count `DISPUTES_BEGIN`/`DISPUTES_END` entries or heading-based fallback |
| Convergence count | Phase 4 disputes / Phase 5 synthesis | Count `**Converged:**` entries |
| Agreement matrix | Phase 2 cross-review | Pairwise: did agent A agree with agent B's recommendation? Binary matrix. |

### Winner-Take-All Mode

| Feature | Source | Extraction Rule |
|---------|--------|-----------------|
| Ranking vector | Phase 5 synthesis | Position in ranking per agent per round |
| Score differential | Phase 5 synthesis | Pairwise score differences between ranked agents |
| Cross-review support | Phase 2 cross-review | Count of positive vs negative assessments per agent |

### Prisoners Dilemma Mode

| Feature | Source | Extraction Rule |
|---------|--------|-----------------|
| Territory claim vector | Phase 1 review | Binary per topic area: does this agent claim ownership? |
| Overreach count | Phase 2 cross-review | Count of contested claims (agent A claims what agent B also claims) |
| Boundary clarity | Phase 5 synthesis | Count of clearly delineated boundaries in synthesis |

### Red-Blue Mode

| Feature | Source | Extraction Rule |
|---------|--------|-----------------|
| Severity vector | Phase 1 review (red) | Per finding: critical=4, high=3, medium=2, low=1 |
| Mitigation rate | Phase 3 revision (blue) | Mitigated findings / total findings |
| Confirmed count | Phase 4 disputes | Findings confirmed as valid after adversarial challenge |
| Coverage score | Phase 5 synthesis | Proportion of attack surface addressed |

---

## 3. Functional Requirements

### Extraction Rules

- **FR-001**: Feature extraction MUST be deterministic -- same artifacts produce same feature vectors. No randomness, no LLM calls.
- **FR-002**: Extraction MUST use structured parsing of conversus output format: structural markers (`DISPUTES_BEGIN`/`DISPUTES_END`), heading patterns, and disposition labels (`Withdrawn`, `Modified`, `Surviving`).
- **FR-003**: Extraction MUST handle missing phases gracefully. If Phase 4 disputes file does not exist, dispute-derived features default to zero.
- **FR-004**: Extraction MUST support multi-round deliberations. Feature vectors are produced per round. Cross-round features (e.g., concession rate change between rounds) are derived from per-round vectors.

### Feature Schema Definition

- **FR-005**: Each mode MUST have a feature schema defined in `schema/features/{mode}.yml` specifying: feature names, types (scalar, vector, matrix), extraction source (phase, file pattern), and extraction rule (parsing logic reference).
- **FR-006**: Feature schemas MUST have corresponding Pydantic models for validation.
- **FR-007**: Feature schemas MUST be extensible -- new features can be added without breaking existing consumers.

### Output Format

- **FR-008**: Extracted features MUST be written to `{output}/features.json` containing: mode, round number, per-agent feature vectors, aggregate features (dispute count, convergence count).
- **FR-009**: The `features.json` schema MUST be defined by a Pydantic model (`FeatureSet`) that plugins can import and validate against.
- **FR-010**: Multi-round features MUST be structured as a list of per-round feature sets, enabling time-series analysis.

### Extraction Pipeline API

- **FR-011**: The pipeline MUST expose a Python API: `extract_features(output_dir: Path, mode: str) -> FeatureSet`.
- **FR-012**: The pipeline MUST also support CLI invocation: `conversus-features extract --output-dir <path> --mode <mode>`.
- **FR-013**: The pipeline MUST validate extracted features against the mode's feature schema before writing output.

### Package

- **FR-014**: The pipeline MUST ship as the `conversus-features` package (pip installable).
- **FR-015**: Dependencies MUST be limited to `pyyaml`, `pydantic`, and `conversus-schemas` (spec 012). No heavy ML dependencies (no numpy, no torch, no sentence-transformers).
- **FR-016**: The package MUST be importable by plugins: `from conversus_features import extract_features, FeatureSet`.

---

## 4. Success Criteria

- **SC-001**: Given a cooperative-mode deliberation output directory with standard Phase 1-5 artifacts, `extract_features()` produces a valid `FeatureSet` with position vectors and concession rates for each agent.
- **SC-002**: Running extraction twice on the same output directory produces byte-identical `features.json`.
- **SC-003**: Given a red-blue output with severity headings (Critical/High/Medium/Low), severity vectors are correctly encoded as 4/3/2/1.
- **SC-004**: A missing Phase 4 disputes file does not crash extraction -- dispute features default to zero with a warning.
- **SC-005**: `pip install conversus-features` in a clean environment installs only `pyyaml`, `pydantic`, and `conversus-schemas`. No heavyweight transitive dependencies.

---

## 5. Constraints

- **Must NOT use LLM calls for extraction.** Feature extraction is pure structured parsing. If an artifact cannot be parsed deterministically, the feature is zero/absent, not guessed.
- **Must NOT modify deliberation artifacts.** The pipeline reads output files; it never writes to agent directories, synthesis, or arbitration output.
- **Must NOT depend on heavyweight libraries.** No numpy, scipy, jax, or ML frameworks. Feature extraction is string parsing and arithmetic, not numerical computing.
- **Must NOT couple to a specific solver.** Feature schemas are consumed by multiple plugins (equilibrium scorer, convergence predictor). The extraction pipeline does not know which plugin will use its output.
