# Cross-Review: game-theorist reviewing functional-architect

## Dangerous Contradictions

### DC-1. Shadowed `mode` parameter -- real bug or design choice?

Functional-architect's R2 identifies that the caller's `mode` parameter in `select_candidate_templates` is always ignored because all four decision types are mapped in `_DECISION_TYPE_MODE`. I did not flag this. The contradiction: functional-architect treats this as a correctness bug (P1), but the spec's FR-018 defines a fixed decision-type-to-mode mapping. If the mapping is *supposed* to be authoritative, the caller's `mode` is intentionally a fallback for unrecognized types, not an override. However, functional-architect correctly notes that `construct_objective` passes `mode` as a parameter, implying the caller expects it to be respected. This needs spec clarification -- is mode derived exclusively from decision type, or can a user override it?

### DC-2. File I/O in `construct_objective` -- purity violation or acceptable orchestrator behavior?

Functional-architect's R7 flags the YAML write in `construct_objective` as breaking the pure-function pattern and proposes extracting `write_objective`. I don't raise this issue. The tension: `construct_objective` is the *orchestrator*, not a pipeline stage. Orchestrators commonly have side effects (file I/O, logging). The purity mandate in the project CLAUDE.md applies to *service functions*, and the orchestrator may be a legitimate exception. However, functional-architect's point about testability is valid -- the current tests use `output_path=None` to skip the write, which means the write path is untested.

### DC-3. Logging absence -- functional gap or premature optimization?

Functional-architect identifies the absence of logging as a missed opportunity (R6, P2). I don't mention logging at all. Functional-architect correctly notes that `extraction.py` uses `logging.getLogger(__name__)` and the pattern is established. The contradiction is whether this matters for correctness. It doesn't, but for a pipeline where classification failures and retry loops are opaque, logging is operationally important. I should have flagged this.

## Tensions

### T-1. Priority of `str.replace` fix: P1 (game-theorist) vs P2 (functional-architect)

I classify the string substitution bug as P1 (correctness). Functional-architect classifies R5 as P2 (robustness). The difference: I argue it produces incorrect symbolic forms for existing templates; functional-architect treats it as a fragility that hasn't triggered yet. The competitive-selection template's form `"J = -w * score + penalty * overlap"` has `w` as a single-character parameter, which *will* match inside words if the sort-by-length mitigation fails (e.g., after a value substitution introduces a new `w`). I maintain P1 is correct because the current implementation is one template edit away from producing wrong output.

### T-2. Frozen dataclass mutable-contents gap

Functional-architect's off-base assumption #4 identifies that `GapList.gaps` is a mutable list inside a frozen dataclass. I don't raise this. Functional-architect is technically correct -- `gaps.append(...)` would succeed -- but pragmatically this is a Python language limitation, not an implementation bug. The frozen annotation communicates intent; enforcing true immutability requires `tuple` (which functional-architect suggests as R10). This is a P3 at most.

### T-3. Alias-based parameter extraction

Functional-architect's missed opportunity #3 proposes adding an alias map to `ParameterDefinition` for extraction recall. I characterize the extraction as "appropriately conservative." The tension: conservative extraction means fewer false positives but more gaps to fill interactively. Functional-architect's alias approach would reduce interactive burden but requires template authors to maintain alias lists. Neither is clearly better -- it depends on the expected ratio of interactive vs non-interactive use.

### T-4. Constraint wiring urgency

I flag constraint parameter gap-filling as P3 (Recommendation 8). Functional-architect flags constraint wiring as P1 (R4). The difference is significant: functional-architect argues FR-011 requires "selected constraints with parameters" in the output, making the absence a spec violation. I treat it as a completeness issue because constraints are referenced by name and the constraint templates *are* loaded. The distinction: are constraint parameters required in the assembled output, or just constraint names?

## Safe Agreements

### SA-1. Source map discarded by `fill_parameter_gaps`

Both reviews identify the same root cause, the same value-comparison fragility, and propose the same fix (typed return with source map). This is the highest-confidence cross-review finding.

### SA-2. FR-003 multi-template presentation is unimplemented

Both reviews confirm that `candidates[0]` is silently used and that the spec requires user-facing presentation. Both propose a protocol-based solution.

### SA-3. Pipeline architecture is sound

Both reviews affirm that the three-stage separation, GapFiller protocol, and frozen intermediate state are well-designed. The issues are refinements, not architectural flaws.
