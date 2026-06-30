# Antipattern Catalog

> Agents: Read the summary index below. If your current work matches any
> entry's symptoms, read the full entry and adjust your approach.

## Summary Index

| Name | Summary | Keywords |
|------|---------|----------|
| redundant-cache | Do not create tracking documents that duplicate computable state | tracking, cache, artifact-creation, status, taxonomy, deliberation-drift, convention-over-content, speckit-duplication |
| unchecked-authority | Do not assert facts about code without citing specific lines — expert credibility does not substitute for evidence | authority, uncited, ungrounded, self-contradiction, impure-labeled-pure, expert-deference, bluffing |

> **Consumer note**: The Summary Index is consumed by spec 055's typed `AntipatternRef` validator (see `specs/055-challenge-loop-deliberation/spec.md` §11.3); format changes require coordinated updates to consumers.

---

## redundant-cache

**Status**: Active
**Observed**: 2026-03-20
**Summary**: Do not create tracking documents that duplicate computable state

### Symptoms

- Proposing new vocabulary or labels (e.g., "Implementation-complete," "Feature-complete," "Not assessed") for states already expressible by counting task checkboxes or reading existing speckit artifacts
- Deliberation cycles spent debating label names, transition criteria, or compound status formats — all for information that is a derived summary of existing data
- Gate reviews discovering "drift" between a manually-maintained status document and the actual project state, generating fix-it specs to reconcile the two
- Fix-it specs triggering their own deliberations, compounding overhead on top of the original housekeeping work

### Root Cause

Agents were not instructed to check whether speckit already tracked the information they were about to document. A self-audit (spec 005-p2p3-backlog-hardening) identified "no single status document" as a gap, but the actual gap was agent awareness of speckit conventions — not a missing artifact. Agents defaulted to creating a new document (STATUS.md with a custom taxonomy) rather than deriving status from existing task checkboxes in tasks.md files.

### Example

During spec 005-p2p3-backlog-hardening Phase 2-3 gate deliberations (2026-03-20), agents created a STATUS.md with a custom taxonomy of status labels. This spawned two additional specs — 007-status-taxonomy-updates and 008-status-enrichment-hardening — just to maintain the cache. Multiple deliberation cycles were consumed debating label formats and fixing drift between STATUS.md and actual spec state. The original artifacts are preserved at `antipatterns/examples/redundant-cache/`, including the redundant STATUS.md, the fix-it specs, and the Phase 2/3 gate deliberation summaries.

### Correction

Derive status from speckit artifacts instead of creating summary documents:
- **Implementation state** — count `[x]` vs `[ ]` in tasks.md
- **Acceptance state** — check spec.md acceptance scenarios against tasks.md completion
- **Gaps** — unchecked tasks with FR references
- **Dependencies** — declared in each spec.md

Do not create summary documents that cache computable information. If you need a cross-spec view, compute it on the fly from existing artifacts.

### When This Does NOT Apply

- When the information is genuinely not derivable from existing artifacts (e.g., subjective risk assessments, effort estimates requiring human judgment)
- When a cross-cutting view is needed that no single artifact provides AND cannot be computed by reading multiple artifacts
- When external stakeholders need a format different from speckit's internal structure

### Keywords

`tracking`, `cache`, `artifact-creation`, `status`, `taxonomy`, `deliberation-drift`, `convention-over-content`, `speckit-duplication`

---

## unchecked-authority

**Status**: Active
**Observed**: 2026-03-21 (spec 005 deliberation, Round 1)
**Summary**: Do not assert facts about code without citing specific lines — expert credibility does not substitute for evidence

### Symptoms

- An agent labels code as "pure," "well-structured," or "correct" without citing specific line numbers
- An agent's Alignment section praises something that contradicts their own Recommendations section
- Other agents defer to the "expert" assessment rather than independently verifying claims
- Uncited factual assertions survive through cross-review because no agent checks the source material
- A synthesis records "convergence" on a position that no agent actually verified against the code

### Root Cause

Agents operating in expert roles (e.g., "integration architect," "type safety advocate") develop implicit authority. When an expert agent asserts a fact about code, other agents are tempted to accept it on authority rather than independently reading the cited files. This creates a trust cascade where a single ungrounded claim propagates through multiple phases before being caught — or worse, makes it into the synthesis unchallenged.

### Example

During spec 005's Round 1 deliberation, **integration-architect** made two factual errors:

1. **Labeled impure functions as pure**: Praised `load_variables_schema` and `load_mode_schema` as "pure functions returning typed models" — but these functions called `sys.exit(2)` and `click.echo()` on failure paths, making them impure and untestable.

2. **Self-contradicted on MODE_PRESENCE**: Alignment section called the hardcoded table "the correct implementation" and "the right approach." Recommendation #7 in the same review called it "brittle coupling" and proposed replacing it.

**functional-typing** caught both errors in Phase 2 cross-review by independently reading the code and citing the specific lines (`validate.py` L43-45, L52-53, L63-64). integration-architect conceded both in Phase 3 revision.

Full example with cross-references: `antipatterns/examples/unchecked-authority/README.md`

### Correction

1. **Every factual claim about code MUST cite specific line numbers.** Template instructions should enforce: "Reference your documentation: `[file.md, L15-22]`" — which they already do, but agents don't always comply.
2. **Cross-reviewers MUST independently verify cited lines**, not accept claims on authority. The cross-review template should instruct: "For each factual claim in the reviewed agent's Alignment section, verify at least one cited line reference against the actual file."
3. **Uncited praise is lower-confidence than cited criticism.** The synthesizer should weight uncited Alignment claims lower than cited Missed Opportunities.
4. **Self-contradictions within a single review should be flagged automatically.** A future linter pass could detect when an agent praises X in Alignment and critiques X in Recommendations.

### When This Does NOT Apply

- When the claim is about domain knowledge (game theory concepts, architectural patterns) rather than specific code
- When the agent's documentation IS the source material (they are citing their own docs correctly)
- When the claim is about the spec text, not the implementation — spec text is visible to all agents

### Keywords

`authority`, `uncited`, `ungrounded`, `self-contradiction`, `impure-labeled-pure`, `expert-deference`, `bluffing`

---

## Maintenance

### Adding a New Entry

1. Observe a recurring agent behavioral mistake with a concrete, real-world example (SC-004: no hypothetical-only entries)
2. Append a new H2 section at the bottom of this file (before this Maintenance section), following the entry format: Status, Observed, Summary, Symptoms (≥2), Root Cause, Example (with real file/spec references), Correction, When This Does NOT Apply (≥1 exclusion), Keywords (≥2 tags)
3. Add a corresponding row to the Summary Index table at the top
4. Do NOT modify any existing entries (FR-010: append-only)

### Deprecating an Entry

1. Set the entry's Status to `**Status**: Deprecated`
2. Add a `### Deprecation Note` section after the Keywords section explaining why the guidance changed
3. Remove the entry's row from the Summary Index table (deprecated entries are excluded from the index per FR-009)
4. The entry remains in this file in its original position for historical reference