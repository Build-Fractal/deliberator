# Phase 4 — Remaining Disputes, Convergence, and Final Position
## agents-md-specialist

---

## Remaining Disputes

### Dispute 1: Whether AGENTS.md contribution guidance should move before or after reference file extraction

**My position (New Recommendation B from revision):** AGENTS.md work should be sequenced *after* reference file extraction — with the sole exception of the root AGENTS.md staleness fix. The pointer-based AGENTS.md files I am proposing gain most of their value by pointing to well-bounded reference files. Creating them before those files exist forces pointers to sections of a monolithic SKILL.md, which is less precise and more likely to become stale as the decomposition proceeds.

**functional-decomposition's position (New Recommendation A):** Tag and move contribution-oriented content *before* the reference-file decomposition begins, as a preparatory step. Frame it as clearing the ground so that the remaining content is unambiguously execution logic.

**Nature of the dispute:** This is a sequencing question, not a disagreement about whether the work should happen. We agree on the destination; we disagree on when to travel there.

**Why I do not fully concede:** The AGENTS.md files I am proposing are pointer files — 15-30 lines each, containing the linter command and "see X for authoritative rules." The contribution-content-tagging exercise functional-decomposition proposes (lines 239-244, 283-289, 139-145, 309) takes maybe 30 minutes and produces a handful of sentences that will move into AGENTS.md pointer files later. Doing this first is not wrong, but calling it "P1 — should happen before Recommendations 1-2" overstates its criticality. The contribution-content tagging is a good hygiene exercise, not a prerequisite gate. If the team executes reference-file extraction first, the tagged content will be easy to identify and move afterward. If the team executes the tagging first, it produces a marginally cleaner extraction boundary. Either order is defensible.

**Residual disagreement:** I dispute the P1 designation for this preparatory step. It should be P2 — valuable, worth doing, but not a prerequisite for handler extraction. The gate handler extraction (universally agreed as highest priority) does not depend on having resolved the AGENTS.md/SKILL.md boundary first.

---

### Dispute 2: Whether the linter should validate AGENTS.md file-reference accuracy (my New Recommendation C vs. the other specialists' silence)

**My position:** Once nested AGENTS.md files exist, the linter should include a lightweight structural check: verify that any files or directories referenced in AGENTS.md actually exist on disk. This is a staleness-detection mechanism, not a semantic validation. It catches the most common failure mode (the root AGENTS.md currently references the nonexistent `tasks/` directory) without requiring the linter to parse prose for semantic intent.

**Other specialists' positions:** No reviewer explicitly opposed this in their revisions. integration-specialist (New Recommendation N2) endorsed linter expansion but scoped it to reference file consistency (variable name matching, file existence checks for SKILL.md load triggers). agentskills-specialist (New Recommendation B) proposed a similar expansion. Neither addressed the AGENTS.md-specific case.

**Nature of the dispute:** This is a scope question about what the linter should cover. The disagreement is not about opposing this — it is about whether it belongs in the decomposition spec or is a secondary improvement.

**Why this matters:** The root AGENTS.md staleness problem I identified in my original review (listing `tasks/` which does not exist) is independently verifiable today. The linter already exists and already validates file references in other contexts. Adding an AGENTS.md file-existence check is a natural extension. The other specialists' linter expansion proposals (checking that SKILL.md load triggers reference files that exist) are structurally identical to what I am proposing for AGENTS.md. If the linter should check that `references/handler-gate.md` exists when SKILL.md references it, it should also check that `tasks/` exists when AGENTS.md references it.

**Residual disagreement:** The other specialists did not include AGENTS.md in their linter expansion proposals. I maintain this is an oversight, not a deliberate exclusion. The linter expansion should cover AGENTS.md file references alongside SKILL.md load trigger file references.

---

### Dispute 3: Whether `templates/AGENTS.md` should describe the 7-files-per-mode convention

**My position (revised):** The 7-files-per-mode convention belongs in `templates/AGENTS.md` framed as "what to expect" (i.e., "each mode directory contains 7 template files: phases 1-6 plus a mode-overview template"), not as a rule the AGENTS.md enforces. The linter enforces the count; the AGENTS.md describes the structure for contributing agents who need to understand what they are editing.

**agentskills-specialist's position (implicit):** agentskills-specialist's New Recommendation A says "triage contribution-oriented content before extraction" and accepts that template naming conventions (line 283) are contribution guidance. This is compatible with my position but does not specifically address the 7-files convention.

**integration-specialist's position (New Recommendation N1):** Frames multi-agent isolation rules as having two audiences — SKILL.md for execution, AGENTS.md for contribution. Applies the same dual-audience logic I used, but for isolation rules, not template structure.

**Nature of the dispute:** This is a narrow question about what belongs in `templates/AGENTS.md`. No cross-reviewer objected directly. The residual tension is that integration-specialist's N1 endorses the dual-audience framing for isolation rules, which supports my position by analogy but does not resolve what goes into templates/AGENTS.md specifically.

**Residual disagreement:** Minor. I maintain the 7-files-per-mode description belongs in `templates/AGENTS.md` as structural orientation for contributing agents. This is not a runtime contract (the linter enforces file counts) and is not an execution rule (agents executing conversus never need to know how many template files exist in a directory). It is precisely the kind of contribution-oriented structural description that AGENTS.md is designed for.

---

### Dispute 4: Whether AGENTS.md files should be created as part of this spec's implementation or deferred to a follow-on spec

**My position:** Four AGENTS.md changes have clear scope and should be part of this spec's implementation: (1) root AGENTS.md staleness fix (15 minutes, no design questions), (2) `linter/AGENTS.md` (the linter is a developer tool with zero dual-ownership risk), (3) the pointer convention for nested AGENTS.md files should be decided now even if file creation is deferred. The remaining nested AGENTS.md files (`templates/`, `presets/`, `schema/`) are lower priority and could be a follow-on.

**Other specialists' positions:** apm-specialist (New Recommendation N3) explicitly positions AGENTS.md work as structural preparation that happens in parallel with or after APM packaging decisions. functional-decomposition (New Recommendation A) positions the contribution-content tagging as P1 pre-work. integration-specialist (New Recommendation N3) defers the AGENTS.md/reference authority question resolution.

**Nature of the dispute:** This is a scope question about what this spec implements vs. what goes in a follow-on. The disagreement is not about value — all reviewers accept AGENTS.md improvements have value — it is about whether they belong in spec 011a's implementation or in a spec 011b or 012.

**Residual disagreement:** I dispute deferring `linter/AGENTS.md` and the root AGENTS.md staleness fix to a follow-on. These are small, low-risk, high-certainty changes that should be bundled with this spec's implementation. Deferring them creates a planning overhead (track them in a new spec) that exceeds their implementation overhead (30 minutes total).

---

## Convergence

### Convergence 1: Reference files are authoritative for runtime; AGENTS.md files are authoritative for contribution workflow

All five reviews now explicitly accept this boundary. integration-specialist (New Recommendation N3) states it most clearly: "Reference files are authoritative for runtime behavior; AGENTS.md files are authoritative for contribution workflow." apm-specialist (Position Summary) accepts it. agentskills-specialist (New Recommendation A) applies it. functional-decomposition (New Recommendation A) uses it as the organizing principle for content tagging.

This is the foundational settlement. It eliminates the dual-ownership problem that dominated the cross-review phase. Every piece of content has a single authoritative home. AGENTS.md can point to that home but never restates the contract it holds.

### Convergence 2: The single-source-of-truth pointer convention

My New Recommendation A from the revision — "AGENTS.md files use 'See [file] for authoritative rules' pointers, never inline rule restatement, for any content that is also enforced at runtime" — has been implicitly accepted by all reviewers through their handling of overlapping content.

integration-specialist (N3): "AGENTS.md summaries are maintained manually but are lower stakes because they are contribution guidance, not execution contracts."
agentskills-specialist (Rec 7): "If a contributing agent editing preset YAML files needs to know the schema, a brief pointer in `presets/AGENTS.md` should reference `references/preset-resolution.md` as the canonical source."
functional-decomposition (New Rec A): "Move [contribution content] to the root AGENTS.md or nested AGENTS.md files... then decompose the remaining execution logic."

No reviewer disputes the pointer convention. The format I proposed in my revision is confirmed: "Preset naming rules are enforced at runtime. See `SKILL.md` section [Preset Resolution] for the authoritative contract. Run `uv run python linter/validate.py` to check compliance before committing."

### Convergence 3: `linter/AGENTS.md` is the strongest nested AGENTS.md recommendation

All reviewers who addressed the linter-AGENTS.md case agreed it is the cleanest application of the contribution-guidance pattern. The linter is a developer tool, not a runtime contract. Its invocation command, test command, and setup instructions are unambiguously contribution guidance. No reviewer objected to `linter/AGENTS.md`. This is the one nested AGENTS.md file that should be created as part of this spec's implementation with no conditions.

### Convergence 4: The root AGENTS.md staleness fix should proceed immediately

The root AGENTS.md lists `tasks/` (nonexistent) and omits `schema/`, `linter/`, `presets/`, `antipatterns/` (all present). This is wrong today, independent of any decomposition strategy. All reviewers who touched the root AGENTS.md question agreed it should be fixed without waiting for the broader decomposition. The fix is a ~15-line structural correction, below my 100-line guideline by a wide margin.

### Convergence 5: Sequencing — reference file extraction first, AGENTS.md pointer files second (except staleness fix and linter)

All reviewers now accept that AGENTS.md pointer files are more valuable when the reference files they point to already exist. The only active sequencing dispute (Dispute 1 above) concerns whether contribution-content tagging should be P1 pre-work or P2 post-work — not whether AGENTS.md file creation should precede reference extraction. The consensus ordering is:

1. Root AGENTS.md staleness fix (now, independent of everything else)
2. `linter/AGENTS.md` creation (now, no runtime dependency)
3. Reference file extraction per the agentskills/functional-decomposition/integration-specialist plan
4. Nested AGENTS.md pointer files for `templates/`, `presets/`, `schema/` (after reference files exist with clear boundaries)

---

## Final Position Statement

### Non-Negotiables

**1. AGENTS.md files must never restate runtime-enforced contracts.**

The AGENTS.md community standard — used by 60,000+ open-source projects — positions AGENTS.md as contribution guidance and project orientation for coding agents. It is not an execution specification. When a rule is enforced at runtime (by the conversus engine or its linter), the authoritative statement of that rule lives in the execution path (SKILL.md, a reference file, or schema YAML). AGENTS.md may point to it. AGENTS.md may summarize it in contribution-oriented language. AGENTS.md must not duplicate it verbatim or claim authorship over it.

This is not a preference. Dual ownership without a synchronization mechanism produces drift. Drift produces agents following stale contribution guidance while the engine enforces different rules. That outcome is worse than having no AGENTS.md at all. The single-source-of-truth pointer convention is the mechanism that makes AGENTS.md safe to create alongside runtime-enforced contracts.

**2. The root AGENTS.md staleness fix is a prerequisite for any nested AGENTS.md work.**

Creating nested AGENTS.md files before fixing the root file's structural errors sends a contradictory signal: "trust this nested file for accurate directory information, but not the root." The root fix must happen first. It is a 15-minute maintenance task. There is no justification for deferring it.

**3. `linter/AGENTS.md` must be included in this spec's implementation scope.**

The linter is a developer tool. Its AGENTS.md is not a pointer file — it contains genuine, inline contribution guidance (invocation command, test command, setup instructions) with zero dual-ownership risk. This is the canonical example of what AGENTS.md is designed for. Including it in spec 011a's implementation demonstrates the pattern; subsequent nested AGENTS.md files for `templates/`, `presets/`, and `schema/` follow the same template.

**4. AGENTS.md files must stay under 100 lines each.**

The AGENTS.md community standard is a README for agents, not a second SKILL.md. The 100-line guideline I established in my original review is the right ceiling. With the narrowed scope (pointer-based, not rule-restating), each nested file should be 15-30 lines. If a nested AGENTS.md approaches 100 lines, it is restating content that belongs in a reference file instead.

### Flexibility

**On sequencing relative to reference file extraction:** I accept that nested pointer AGENTS.md files (`templates/`, `presets/`, `schema/`) should be created after the reference files they will point to are stable. I will not insist on a specific ordering beyond: staleness fix first, linter AGENTS.md alongside or immediately after, nested pointer files after reference file structure is confirmed.

**On contribution-content tagging as P1 vs. P2:** I am flexible on this. functional-decomposition's proposal to tag contribution-oriented lines before extraction is a reasonable preparatory step. If the team finds it useful to tag lines 239-244, 283-289, 139-145, and 309 before beginning handler extraction, the result is a slightly cleaner extraction boundary. I do not insist on a specific priority level for this task. Either sequencing produces the same eventual outcome.

**On the linter expansion scope for AGENTS.md:** My New Recommendation C (linter should validate AGENTS.md file references) is a stretch goal, not a prerequisite for any other work. If the linter expansion from integration-specialist and agentskills-specialist proceeds in phases, AGENTS.md file-reference checking is appropriate as Phase 2 or Phase 3 work — after the more critical load-trigger file-existence checks are implemented. I will not block anything on this.

**On the number and scope of nested AGENTS.md files:** If the implementation team determines that only `linter/AGENTS.md` and the root staleness fix are worth doing in spec 011a, I accept that scope reduction. The pointer files for `templates/`, `presets/`, and `schema/` are valuable but not urgent. Their value increases as the reference files they point to stabilize. Deferring them to a follow-on spec is a reasonable implementation decision.

**On what the root AGENTS.md says about SKILL.md:** I do not insist on the exact wording of the root AGENTS.md update. The structural requirements are: fix the directory listing (remove `tasks/`, add `schema/`, `linter/`, `presets/`, `antipatterns/`), add one line noting subdirectories with their own AGENTS.md, add the linter as a pre-contribution check. Everything else — section ordering, exact phrasing, whether to include a brief project description — is at the implementer's discretion, subject to the 100-line ceiling.
