# Extraction Engineer Review: 015 Feature Extraction Pipeline

**Reviewer**: extraction-engineer
**Spec**: 015-feature-extraction
**Date**: 2026-03-24

---

## Executive Summary

The feature extraction pipeline in `conversus/schemas/extraction.py` implements a deterministic, LLM-free conversion of markdown deliberation artifacts into numerical feature vectors. The implementation is structurally sound: regex patterns target the exact structural markers emitted by conversus templates, disposition parsing correctly handles both structured (`**Disposition**: Surviving`) and standalone (`**SURVIVING.**`) formats, and the four mode extractors (cooperative, winner-take-all, prisoners-dilemma, red-blue) each map faithfully to their respective template output sections. However, I identify several parsing correctness gaps where regex patterns either over-match (producing false positives) or under-match (missing valid template output variants), a critical misalignment between the spec's position vector encoding rule and the implementation's fallback behavior, and fragility in cross-review agreement matrix construction that assumes a fixed directory naming convention not enforced by the engine.

---

## Alignment

### A-1: DISPUTES_BEGIN/END marker parsing is correct against synthesis template

The `_DISPUTES_BEGIN` and `_DISPUTES_END` patterns (`<!--\s*CONVERSUS:DISPUTES_BEGIN\s*-->`) exactly match the markers emitted by `templates/cooperative/synthesis.md` lines 114-124. The `re.IGNORECASE` flag is appropriate because the markers are in HTML comments and some LLM providers occasionally vary capitalization. The `_extract_between_markers()` function correctly requires both markers present with `end.start() > begin.end()`, preventing false extraction from malformed output. This is the primary extraction mechanism per FR-002 and it is implemented correctly.

### A-2: Disposition label extraction handles both template formats

The cooperative revision template (`templates/cooperative/revision.md` lines 48-50) instructs agents to write `**Disposition**: Withdrawn | Modified | Surviving`. The `_DISPOSITION_PATTERN` regex matches this format, and the `_STANDALONE_DISPOSITION` regex handles the alternative uppercase format (`**WITHDRAWN.**`, `**SURVIVING.**`) that some LLM responses produce. The fallback cascade (try structured first, then standalone if zero results) is the correct strategy for robustness without ambiguity.

### A-3: Position vector encoding rule is correctly implemented for the priority-aware path

When a recommendation section contains an explicit `Priority: P1/P2/P3` label, the encoding `max(0, 4 - level)` correctly produces P1=3, P2=2, P3=1, matching the spec's Section 2 table exactly. The withdrawn=0 case is handled by the disposition check preceding the priority lookup.

### A-4: Convergence counting targets the correct template output

The `_CONVERGENCE_ENTRY` pattern (`^\s*-\s*\*\*Converged:\s*`) matches the exact format prescribed by `templates/cooperative/disputes.md` line 57: `- **Converged: [Label]**`. The extraction correctly sums convergence entries across all agents' Phase 4 disputes, which is the right aggregation since each agent independently reports their view of convergence.

### A-5: Red-blue severity vector encoding is correct

The severity map `{"critical": 4, "high": 3, "medium": 2, "low": 1}` matches the spec's Section 2 table. The `_THREAT_ENTRY` regex targets the format `**[THREAT-001: SQL Injection]** (severity: critical)` which is the format the red-blue review template produces. The fallback to the simpler `_SEVERITY_PATTERN` handles cases where threats are listed without the catalog numbering convention.

### A-6: Agent discovery correctly excludes non-agent directories

The `_discover_agent_names()` function excludes `summary`, `arbitration`, and `__pycache__` directories. It requires either `review.md` or `revision.md` to exist, which correctly identifies agent directories across all phases. The `sorted()` call on `output_dir.iterdir()` ensures deterministic ordering (FR-001).

---

## Missed Opportunities

### M-1: Position vector fallback defaults are not spec-compliant

When a recommendation section lacks an explicit `Priority: P1/P2/P3` label, the implementation defaults Surviving to 2 and Modified to 1 (lines 302-308). The spec (Section 2) defines position vector encoding as `P1=3, P2=2, P3=1, withdrawn=0`. There is no spec provision for a priority-agnostic default. The template (`revision.md` line 48) does not require agents to include priority labels in their dispositions -- it only requires the disposition label itself. This means a well-formed agent revision that omits priority labels will produce a different position vector than one that includes them, even if both encode the same semantic positions.

The correct behavior when priority is missing should be documented in the spec as an explicit extraction rule. The current defaults (Surviving=2, Modified=1) are reasonable heuristics but violate FR-001's determinism guarantee in a subtle way: two semantically identical revisions with and without priority labels produce different vectors.

### M-2: `_DISPOSITION_PATTERN` regex has a double-star boundary error

The pattern `r"\*\*(?:Disposition|DISPOSITION)\*?\*?\s*:\s*"` uses `\*?\*?` at the closing boundary, making both closing asterisks optional. This means the pattern matches `**Disposition*:`, `**Disposition**:`, `**Disposition:` (with no closing stars), and even `**DISPOSITION*:`. In practice, LLM output almost always produces the balanced `**Disposition**:` form, but the regex should enforce it: `\*\*` instead of `\*?\*?`. The current pattern could match mid-word occurrences in edge cases where the text contains "Disposition" in a non-label context.

### M-3: Cross-review agreement matrix counts formatting artifacts, not semantic agreements

The `_build_agreement_matrix()` function counts occurrences of `_SAFE_AGREEMENT` pattern (`^\s*-\s*\*\*.*?\*\*`) under the "Safe Agreements" section. This pattern matches any bolded list item, not specifically agreement entries. If a cross-review's Safe Agreements section contains sub-bullets with bolded terms (e.g., `  - **Evidence**: strong`), these would be incorrectly counted as additional agreements. The pattern should be tightened to match only top-level list items, or better, should count the number of agreement entries by tracking the primary pattern (e.g., items starting with `- **[Agreement label]**`).

### M-4: Red-blue role detection is fragile and order-dependent

The `_extract_rb_agent_features()` function detects red/blue role by searching the review text for keywords like "attack surface", "threat catalog", "red team" (for red) and "defense brief", "safeguards in place", "blue team" (for blue). This heuristic works for the current red-blue templates but is fragile: a blue team agent that mentions "attack surface" in its defense brief would be misclassified as red. The role should be an explicit input parameter (derived from the config) rather than inferred from content. The function signature already accepts an optional `role` parameter but falls back to content detection when it is `None`, which is the default code path from `_extract_rb_features()`.

### M-5: Multi-round feature extraction overwrites round_number via model_dump() reconstruction

Lines 896-903 reconstruct `RoundFeatures` by calling `round_features.model_dump()`, filtering out `round_number`, and passing the rest as kwargs. This is fragile: if `RoundFeatures` gains a field with a default_factory (e.g., a `dict` or `list`), the `model_dump()` output will serialize it to a concrete value, and the re-construction will bypass the factory. A cleaner approach is `round_features.model_copy(update={"round_number": i})`, which Pydantic v2 supports natively and avoids the dump-then-reconstruct pattern.

### M-6: Cooperative extraction does not populate `territory_claim_vector` for cooperative mode

The spec's Section 2 defines cooperative mode features including "Position vector" but also defines it as `Per recommendation: P1=3, P2=2, P3=1, withdrawn=0. Vector length = max recommendations across agents.` The current implementation does not normalize vector lengths across agents to the maximum recommendation count. Each agent's position vector is padded to their own recommendation count (line 314), but agents with fewer recommendations than others will have shorter vectors, breaking the "Vector length = max recommendations across agents" invariant.

### M-7: `_extract_section()` heading-level detection has an off-by-one for `##` headings

The function determines heading level by counting `#` characters from the input string. But the termination pattern `(?=^#{1,{level}}\s|\Z)` will terminate at any heading of equal or lesser level. For a `### Section` input, it terminates at `###` or `##` or `#`. This is correct. However, for `## Section`, it terminates at `##` or `#` but not at `###`, meaning subsections within a `##` heading are included in the extracted text. This is actually the desired behavior for most extraction use cases, but it could over-capture content when a `###` subsection logically belongs to a different `##` parent.

### M-8: `write_features()` does not validate the FeatureSet before writing

FR-013 requires the pipeline to validate extracted features against the mode's feature schema before writing output. The `write_features()` function accepts a `FeatureSet` and serializes it to JSON without re-validation. While the `FeatureSet` was presumably validated at construction time (Pydantic validates on construction), there is no explicit validation step at write time that would catch a manually-constructed `FeatureSet` with invalid mode or missing fields.

---

## Off-Base Assumptions

### O-1: Agreement matrix assumes cross-review filenames match agent names exactly

The `_build_agreement_matrix()` function constructs cross-review file paths as `{reviewer}/cross-reviews/{reviewed}.md`. This assumes the engine always uses agent names as filenames. The engine's `OutputManager.get_cross_review_path()` does use this convention, but the assumption is implicit. If a future engine version changes the naming convention (e.g., slugifying agent names with special characters), the extraction pipeline would silently produce an empty agreement matrix.

### O-2: Prisoners-dilemma extraction iterates parent directory to find cross-reviews about an agent

The PD extraction (`_extract_pd_agent_features()`, lines 591-600) iterates `agent_dir.parent` to find cross-reviews written about the target agent by other agents. This correctly finds the files, but it also iterates over `summary/` and `arbitration/` directories before the filter excludes them. More critically, it uses `other_dir.name in ("summary", "arbitration")` as the exclusion list, but does not exclude `__pycache__`, `plugins/` (from spec 016), or any other non-agent directory. Adding a `plugins/` directory to the output structure would cause a warning per `_read_file()` when the function tries to read `plugins/cross-reviews/{agent}.md`.

---

## Actionable Recommendations

1. **Normalize position vector lengths to max recommendations across agents** (Priority: P1)
   - The spec requires "Vector length = max recommendations across agents." The current implementation pads each agent's vector independently. After extracting all agents, compute `max_recs = max(af.recommendation_count for af in agent_features.values())` and re-pad all vectors to `max_recs`.

2. **Fix the `_DISPOSITION_PATTERN` closing boundary** (Priority: P2)
   - Change `\*?\*?` to `\*\*` at the closing boundary so the regex requires balanced bold markers. This prevents false matches on non-label text containing "Disposition".

3. **Tighten `_SAFE_AGREEMENT` to match top-level agreement items only** (Priority: P2)
   - Replace `^\s*-\s*\*\*.*?\*\*` with a pattern that requires the item to start at zero or two spaces of indentation, excluding deeply-nested sub-bullets.

4. **Pass red/blue role explicitly from config rather than inferring from content** (Priority: P2)
   - Add a `roles: dict[str, str]` parameter to `_extract_rb_features()` populated from `conversus.yml` agent definitions, falling back to content detection only when roles are not configured.

5. **Use `model_copy(update=...)` instead of dump-reconstruct for round number override** (Priority: P3)
   - Replace the `model_dump()`-based reconstruction at lines 896-903 with `round_features.model_copy(update={"round_number": i})`.

6. **Exclude `plugins/` from non-agent directory iteration in PD/RB extraction** (Priority: P2)
   - Add `"plugins"` to the exclusion list in `_extract_pd_agent_features()` and `_extract_rb_agent_features()` to prevent warnings when plugin output directories exist.

7. **Add explicit write-time validation to `write_features()`** (Priority: P3)
   - Call `FeatureSet.model_validate(feature_set.model_dump())` before serialization to ensure FR-013 compliance even for manually-constructed FeatureSets.

8. **Document the priority-absent position vector default in the spec** (Priority: P2)
   - Add to Section 2's cooperative extraction rules: "When a recommendation section does not include a Priority label, Surviving defaults to 2 and Modified defaults to 1."
