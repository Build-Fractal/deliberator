# Devil's Advocate Review — 008-interests-mode

## Executive Summary

Spec 008 proposes a two-command guided workflow (`/conversus interests` and `/conversus mode`) that bridges natural-language problem definitions to executable `conversus.yml` configs. The spec is well-structured and the user-facing design is clean. However, several assumptions deserve challenge before this hardens into SKILL.md: the decision matrix claims "High" confidence universally while papering over real ambiguity; the heuristic mode detection is underspecified to the point of non-reproducibility; the `interests.md` artifact introduces coupling that may not earn its keep; and the spec quietly narrows what conversus can do by forcing every deliberation through a four-bucket taxonomy.

The spec will survive these challenges if it addresses them. If it does not, it ships a guided workflow that feels authoritative while hiding fragile heuristics behind a clean UI.

---

## Alignment

### Strong alignment with SKILL.md

1. **Schema compatibility**: FR-011 (spec line 57) correctly mandates that generated YAML uses the exact same schema as hand-crafted configs. SKILL.md lines 52-104 define that schema. The generated YAML structure on spec lines 1236-1250 matches. This is the right call — no schema extensions means no bifurcation.

2. **Subcommand dispatch integration**: The spec correctly depends on 007's dispatch infrastructure (spec line 6). SKILL.md lines 19-37 already list `interests` and `mode` as routed subcommands. The handlers described in the spec (SKILL.md lines 926-1296) match what 008 specifies.

3. **Preset integration**: FR-006 (spec line 41) and the Preset Matching section (SKILL.md lines 985-992) correctly treat presets as optional. The soft dependency on spec 004 is appropriate — the interests command works without presets but is better with them.

4. **Agent name validation**: Spec line 964 and SKILL.md line 198 both enforce `[a-z0-9][a-z0-9-_]*`. Consistent.

5. **User confirmation gates**: Spec lines 38, 55, 103 all require user confirmation before writing. This aligns with SKILL.md's constraint on line 1020: "Do not write `interests.md` until the user confirms."

---

## Off-Base Assumptions

### 1. The decision matrix confidence is fabricated

The decision matrix (spec lines 44-52, SKILL.md lines 1137-1143) maps each problem type to a mode with "High" confidence for all four mappings. This is misleading.

`scoping` -> `prisoners-dilemma` at "High" confidence is the weakest link. The prisoners-dilemma mode is designed for scenarios where agents face incentives to misrepresent their capabilities — the classic "defect or cooperate" tension. But many scoping problems have no deception incentive at all. "Which team owns the data pipeline?" is often a coordination problem (cooperative mode) or a boundary-drawing exercise that does not map cleanly to game-theoretic defection. The spec acknowledges that scoping uses "honesty-calibrated" prompts (spec line 35), but honesty calibration is a prompt strategy, not a mode justification. The mode determines the synthesis template and dispute structure (SKILL.md lines 761-764), which for prisoners-dilemma includes "Disputed Boundaries" and responsibility maps. Those artifacts assume overlapping claims and strategic boundary-setting, which are not universal in scoping problems.

`integration` -> `cooperative` at "High" confidence is similarly fragile. Integration problems can have genuinely adversarial dynamics — two teams with incompatible technical requirements forced to share an interface. The cooperative mode's synthesis structure ("Remaining Disputes" and "Summary of Changes Required" per SKILL.md line 670) assumes agents are seeking alignment. But some integration problems are zero-sum on specific dimensions, and winner-take-all would surface that reality better.

**Challenge**: If the mapping is truly high-confidence, why does the spec need heuristic mode detection at all (spec lines 63-68)? The existence of the heuristic fallback reveals that the matrix is aspirational, not empirical. Either reduce the confidence labels to "Default" (removing the false authority) or provide evidence from actual conversus runs that these mappings produce better deliberation outcomes than alternatives.

### 2. Heuristic mode detection is a black box dressed as a spec

The heuristic detection section (spec lines 63-68) lists keyword signals ("choose between", "work together", "who owns", "what could go wrong") but specifies nothing about how to score them. Spec line 1156 says "Score each mode based on signal density" but defines neither the scoring function nor the threshold for "clear lead" vs. "mixed signals."

This matters because the mode command runs in the main conversation without subagents (SKILL.md line 1097). The executing LLM will interpret "signal density" however it sees fit. Two runs of the same problem description could produce different mode recommendations depending on the model's attention to different keywords.

The spec cannot claim reproducibility while delegating the core decision to undefined heuristics. Compare this with the Dispute-Parsing Subsystem (SKILL.md lines 743-770), which defines exact markers, fallback strategies, and default behaviors. That is a spec. The heuristic detection section is a suggestion.

**Challenge**: Either formalize the scoring (weighted keywords, minimum threshold for "clear lead," explicit tie-breaking rules) or acknowledge that mode recommendation is advisory and always requires user confirmation. The spec already requires confirmation (spec line 1210), so the honest path is to demote the heuristics from "detection" to "suggestion" and drop the pseudo-formal signal lists.

### 3. `interests.md` is a coupling artifact with unclear value

The spec introduces `interests.md` as an intermediate artifact between `problem.md` and `conversus.yml`. This creates a three-file chain: `problem.md` -> `interests.md` -> `conversus.yml`. Every link in this chain has staleness detection (spec line 59, SKILL.md lines 1117-1121) and existing-file checks (spec lines 39, 55, 1212-1227).

But `interests.md` duplicates information that ends up in `conversus.yml`. The agents section of `conversus.yml` (SKILL.md lines 1243-1250) contains name, prompt, docs, and role — exactly what `interests.md` stores. The only field in `interests.md` that does not transfer is `Perspective` (a one-sentence summary), which is human-readable metadata, not machine-consumed input.

The stated justification is that "interests determine mode" (spec line 18). But the mode is determined primarily by the problem type from `problem.md`, not by the interest structure. The decision matrix (spec lines 44-52) keys on problem type. The heuristic fallback (spec lines 63-68) reads problem description signals. Interest structure is mentioned as a secondary signal ("interests named after products/tools/approaches"), but this signal could be extracted at mode-selection time by reading `problem.md` directly.

**Challenge**: What user workflow actually benefits from `interests.md` as a separate file rather than `interests` and `mode` being a single combined step? If the answer is "users want to review and modify interests before choosing a mode," then the current design of requiring user confirmation before writing (spec line 1020) already provides that gate within a single command. The separate file introduces staleness risk (spec line 59) and file-management overhead without a demonstrated workflow benefit. Consider making `interests.md` optional — the `mode` command could generate agents directly from `problem.md` with an interactive interest-selection step, and only write `interests.md` if the user explicitly asks to save them.

---

## Missed Opportunities

### 1. No feedback loop from `/conversus run` results

The guided workflow flows in one direction: `define` -> `interests` -> `mode` -> `run`. But what happens after `run` reveals that the mode was wrong or the interests were miscalibrated? There is no `/conversus refine` or mechanism to feed synthesis results back into the guided workflow. The user must manually re-run `interests` or `mode` with overrides.

SKILL.md already has the `prior:` mechanism (lines 75-80) for feeding previous run context into new runs. The guided workflow should leverage this — after a `run`, suggest: "Based on the synthesis, consider refining interests or mode. Run `/conversus interests` to adjust, then `/conversus mode --prior conversus-output/summary/final.md`."

### 2. No interest count guidance beyond "2-5"

FR-001 (spec line 31) specifies 2-5 interests. But the agent count has massive cost implications. SKILL.md lines 1304-1313 show that 3 agents produce 13 agent launches per round, while 5 agents produce 31 agent launches per round (5^2 + 5 + 1). The spec does not ask the agent to inform the user of this cost before confirming interests.

The mode command's report (SKILL.md line 1295) does not include an agent-launch estimate either. This is a missed opportunity to set expectations — a 5-agent, 3-round, 2-iteration run with arbitration would launch 5 * (5 + 2*(5*4 + 5) + 5 + 1) + 1 + 1 = 252+ agents. Users should see that number before confirming.

### 3. Problem type re-evaluation at mode time is underspecified

The mode command reads the problem type from `problem.md` but does not validate or re-evaluate it against the actual interests. If a user defines a `selection` problem but then creates interests that look like integration interests (named after teams, focused on alignment), the mode command will recommend `winner-take-all` because the matrix keys on problem type. There is no cross-check.

The heuristic detection only fires "when the problem type is unset or ambiguous" (spec line 1145). It should also fire when the interest structure contradicts the stated problem type, with a warning: "Your problem type is 'selection' but your interests suggest integration. Consider changing the type or the interests."

### 4. No interest deduplication or conflict detection

The spec handles `--add <name>` (spec line 37) and existing-file modification (spec line 39) but does not address what happens when two interests have substantially overlapping perspectives. If a user adds "backend-team" and "infrastructure-team" with near-identical prompts, they will produce correlated reviews that waste agent launches without adding deliberation value. The interests command should detect high-overlap interests and warn.

---

## Actionable Recommendations

1. **Downgrade confidence labels** in the decision matrix (spec lines 44-52) from "High" to "Default" for all four mappings, reserving "High" for empirically validated mappings. Add a footnote: "These defaults produce good results in most cases. Override with `/conversus mode --mode` when your problem does not fit the default."

2. **Formalize or demote heuristic detection**. Either define a concrete scoring mechanism (keyword presence counts, minimum signal count for "clear lead," explicit tie-breaking) or rename the section from "Heuristic Mode Detection" to "Mode Suggestion Signals" and explicitly state that the recommendation is always soft.

3. **Add agent-launch cost estimate** to the interests confirmation step. After presenting suggested interests, include: "This will produce approximately {N^2 + N + 1} agent launches per round." This leverages the formula already documented in SKILL.md lines 1304-1306.

4. **Add interest-vs-type cross-validation** to the mode command. When the interest structure signals a different mode than the problem type, warn the user and suggest re-evaluating the problem type. This catches the case where `define` and `interests` were run at different times with evolving understanding.

5. **Evaluate whether `interests.md` should be optional**. If the primary value is user review before mode selection, that can happen interactively within a single `mode` command that reads `problem.md` directly. The separate file adds staleness tracking overhead (spec line 59, SKILL.md lines 1117-1121) and a mandatory intermediate step. At minimum, consider a `/conversus mode --from-problem` shortcut that skips `interests.md` and generates interests inline.

6. **Specify the behavior when `problem.md` has status: draft**. The define spec says status is "a factual annotation — whether downstream commands treat `draft` as blocking is defined by those commands' specs" (SKILL.md line 889). Spec 008 never defines this. Should `interests` warn when `problem.md` has unresolved `[CLARIFY:]` tags? Should it refuse to proceed? The current spec is silent, which means the behavior is undefined and implementation-dependent.

---

## Referenced Documentation

| Document | Lines Referenced | Topic |
|---|---|---|
| `specs/008-interests-mode/spec.md` | 6, 15-18, 31-41, 44-52, 55-59, 63-68, 70-87, 93-97, 103-106 | Spec requirements, decision matrix, schemas, constraints |
| `SKILL.md` | 19-37 | Subcommand dispatch table |
| `SKILL.md` | 52-104 | Config schema (run engine) |
| `SKILL.md` | 198-202 | Agent name validation |
| `SKILL.md` | 670-673 | Mode-specific required headings |
| `SKILL.md` | 743-770 | Dispute-Parsing Subsystem (contrast for heuristic formalization) |
| `SKILL.md` | 889 | Draft status annotation semantics |
| `SKILL.md` | 926-1296 | Interests and Mode handler implementations |
| `SKILL.md` | 1020 | User confirmation before writing interests.md |
| `SKILL.md` | 1117-1121 | Staleness warning |
| `SKILL.md` | 1137-1143 | Decision matrix in SKILL.md |
| `SKILL.md` | 1304-1313 | Agent launch count formulas |
| `specs/done/004-preset-agents/spec.md` | 1-18 | Preset agent motivation and design |
| `specs/007-subcommand-dispatch-define/spec.md` | 1-11 | Subcommand dispatch dependency |
