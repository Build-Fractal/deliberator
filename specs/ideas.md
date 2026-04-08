- Inter-round arbiter reviews each round's synthesis and feeds decisions into next round or consensus — **DONE** (spec 006: inter-round arbitration with influence control)
- Run conversus on each phase completion — **DONE** (spec 011: phase consensus gates)
- Agent antipattern tracking — maintain a searchable catalog of observed antipatterns (e.g., STATUS.md redundant-cache pattern from former specs 007/008) so agents avoid repeating mistakes. Eventually semantic search retrieval based on current task context rather than loading full catalog into context. — **DONE** (spec 010: antipattern steering)
- Former specs 007 (game engine) and 008 (executable conversus) removed. 007 archived to `specs/archive/game-engine-vision/` as long-term north star. 008 was already implemented by SKILL.md.
- Former spec 998 (phase consensus gates) folded into spec 011 with CI/CD-specific additions (exit codes, gate-result.md).
- Former spec 999 (decision framework) decomposed into specs 007-010 as smaller, ordered units.
- Preset discovery & management — `/conversus presets` list/filter/detail commands + `--save` custom preset creation. Extracted from spec 004 (FR-022–024, US-3, US-4). Small effort, pure CLI output formatting. No engine changes.
- Game engine vision — **DECOMPOSED INTO SPECS 012-020**. The monolithic vision (`specs/archive/game-engine-vision/`) has been broken into 9 independently reviewable specs: 012 (game form schemas), 013 (objective function templates), 014 (guided objective construction), 015 (feature extraction), 016 (plugin system), 017 (equilibrium scorer), 018 (convergence predictor), 019 (config optimizer), 020 (scenario storage). These are code specs (Python packages, pip installable), not SKILL.md edits. Original vision and decisions preserved in archive.

---

## Agent Credibility Scoring Across Rounds

**Origin**: Observed in spec 005's 2-round deliberation — integration-architect made two unchecked authority assertions (labeling impure functions as "pure," self-contradicting on MODE_PRESENCE). The cross-review phase caught both, but the system has no mechanism to track or penalize this pattern across rounds. See: `antipatterns/examples/unchecked-authority/README.md`.

**Problem**: Agents currently have no incentive structure beyond template instructions. An agent that makes ungrounded claims, cites non-existent line numbers, or self-contradicts faces no consequence beyond being corrected in the next phase. An agent that honestly concedes when wrong gets no credit for intellectual honesty. An agent that stubbornly defends a weak position wastes deliberation cycles. The system can't distinguish between an agent that was right 8 times and wrong twice versus one that was right 3 times and bluffed 7 times.

**Proposed Scoring Model**:

Track per-agent scores across all phases and rounds. Each recommendation or claim earns or costs points based on how it fares through the deliberation:

| Event | Points | Rationale |
|-------|--------|-----------|
| Recommendation survives unchallenged through synthesis | +10 | Solid, uncontested contribution |
| Recommendation challenged AND successfully defended with evidence | +12 | Battle-tested position — highest value |
| Successfully refuting another agent's recommendation (they concede) | +8 | Adversarial quality control — caught a problem |
| Honestly conceding a recommendation after valid challenge | +9 | Intellectual honesty — slightly less than unchallenged because the original was wrong, but conceding quickly is valuable |
| Recommendation withdrawn preemptively (before cross-review) | +5 | Self-correction, but suggests the original review was hasty |
| Making an uncited factual claim that is later disproven | -15 | Erodes trust in the entire review — heavy penalty |
| Self-contradicting within the same review (Alignment vs Recommendations) | -12 | Suggests the review wasn't internally audited |
| Conceding a position that was actually correct (caved under pressure) | -8 | Weak spine — the deliberation lost a correct position |
| Stubbornly defending after overwhelming evidence against | -6 | Wastes deliberation cycles but at least stands by their claim |
| Citing specific line numbers that are verifiable | +2 bonus | Encourages grounded claims |
| Making a claim without any citation | -3 | Discourages ungrounded authority assertions |

**Aggregate scoring** produces a credibility profile per agent:
- **Reliability**: (defended + unchallenged) / total recommendations
- **Honesty**: concessions / (concessions + stubbornly defended wrong positions)
- **Grounding**: cited claims / total claims
- **Net credibility**: total points / recommendations made

**How this feeds back into the system**:

1. **Synthesizer weight**: Phase 5 synthesizer could weight positions by running credibility score. High-credibility agent's surviving recommendation carries more weight in tie-breaks.

2. **Stagnation signal**: Agent with declining credibility across rounds suggests the perspective is not productive — system could suggest removal or replacement.

3. **Game engine integration** (archive/game-engine-vision): Agent credibility IS the payoff. The game engine could compute Nash equilibria over credibility scores to predict convergence.

4. **Anti-bluff mechanism**: Heavy penalty for uncited claims (-3) and disproven facts (-15) creates game-theoretic incentive to only assert what you can ground. The asymmetry (small per-claim penalty, massive if caught) mirrors real-world reputation dynamics.

**Concrete example from spec 005** (see `antipatterns/examples/unchecked-authority/`):
- integration-architect: -12 (self-contradiction) + -15 (mislabeled impure as pure) + +9 (concession) + +9 (concession) = **-9 net**
- functional-typing: +8 (caught impurity) + +8 (caught contradiction) = **+16 net**

This correctly reflects that functional-typing provided higher-value contributions on those interactions.

**Implementation path**: Post-hoc scoring agent reads all phases and computes scores mechanically from recommendation dispositions. Requires structured output (Phase 4 already produces "surviving/withdrawn/modified" classifications). Eventually feeds into game engine vision's payoff functions.

**Status**: Idea — requires spec before implementation. Candidate for spec `0XX-agent-credibility-scoring`.

---

## Schema Query Tool — Zero-Approval Context Lookup for Agents

**Origin**: During spec 006 implementation, the question arose of how agents should reference specific variables, mode schemas, and config fields without reading entire files. Evaluated XML (XPointer/XPath), JSON (JSON Pointer RFC 6901), and YAML (no native deep-linking). Concluded that the format is irrelevant when agents have a parsing tool — the tool returns exactly the subtree needed, minimizing tokens regardless of source format.

**Problem**: An agent reviewing a template or debugging a variable needs to know "what type is INFLUENCE_LEVEL? what phases does it appear in?" Currently the agent must Read the entire `schema/variables.yml` (~400+ lines, ~500 tokens). As the schema grows (spec 006 adds variables, game engine vision adds plugin variables, new modes add mode schemas), this cost increases linearly. Agents also can't deep-link to specific YAML locations when cross-referencing between documents.

**Design constraints** (from user):
- No MCP dependencies — function calls only
- No user approval required — must work via Read tool (auto-approved)
- Must minimize tokens per query
- Must work for LLM agents as the primary consumer

**Why not change formats?**
- **XML + XPointer**: Best deep-linking standard (W3C), but verbose (tags double token count), declining ecosystem for configs, requires `lxml` dependency. Deep-linking advantage disappears when agents have a parsing tool.
- **JSON + JSON Pointer (RFC 6901)**: Good standard (`/variables/INFLUENCE_LEVEL/type`), but GitHub/renderers don't resolve JSON Pointer fragments in YAML files. Same "tool makes it irrelevant" conclusion.
- **YAML stays**: Lowest tool complexity (`yaml.safe_load()` + dict traversal = 3 lines), Pydantic models already parse it, linter infrastructure already exists, human-readable when needed.

**Proposed solution: Pre-computed lookup index**

Generate a flat, minimal-token index file that agents can Read directly (auto-approved, no Bash needed):

```
schema/.index/variables.idx
```

Format — one line per variable, pipe-delimited:
```
INFLUENCE_LEVEL|string|[arbitration]|required
PRIOR_ARBITRATION_PATH|path|[review,cross-review,revision,disputes,synthesis]|optional|arbiter.timing==inter-round
AGENT_NAME|string|[review,revision,disputes]|required
```

An agent reads this file, finds the line they need. ~1 token per variable instead of ~12. For 45 variables, the full index is ~50 tokens vs ~500 for the raw YAML.

**Additional index files:**
```
schema/.index/modes.idx          # mode|mode_in_phases|dispute_heading|required_headings
schema/.index/error-types.idx    # error_type|description
```

**Generation**: `conversus-lint --reindex` regenerates all index files from the schema YAML. Run as part of the linter CI step. Index files are committed (not gitignored) so agents can Read them without running any commands.

**Alternative considered — agent-callable query function:**
```python
from linter.models import VariablesSchema
schema = VariablesSchema.model_validate(yaml.safe_load(open("schema/variables.yml")))
var = schema.variables["INFLUENCE_LEVEL"]
```
This requires Bash approval to execute Python. Rejected per user constraint (no approval needed).

**Alternative considered — inline the index in the schema file:**
Add a comment block at the top of `variables.yml` with the compact index. Agents read the first N lines via `Read(offset=1, limit=50)`. Works but conflates data with documentation and grows the file.

**Scaling trajectory**:
- Today (45 variables): ~500 tokens for full YAML — index is nice-to-have
- After game engine vision (plugin variables): potentially 100+ variables — index becomes necessary
- After executable runtime: programmatic queries via `validate_all()` — index is the agent-facing complement

**Relationship to other specs**:
- Spec 005 (Generalized Templates): Built the schema and Pydantic models this tool queries
- Game engine vision: Plugin variables will expand the schema significantly

**Status**: Idea — low urgency until schema exceeds ~100 variables. Candidate for spec `0XX-schema-query-tool`.

---

## Deliberation Telemetry — Per-Agent & Per-Phase Usage Tracking

**Origin**: Observed during spec 007's 2-round deliberation (35 agents launched). No visibility into which agents or phases consumed the most tokens. Cross-review is quadratic (N*(N-1)) and likely the most expensive phase, but without data this is a guess.

**Problem**: Users running conversus have no cost visibility. Game engine optimization requires a cost function — you can't optimize agent count vs quality without knowing the cost curve. Credibility scoring (see above) needs a value-per-token metric.

**Proposed output: `usage.yml`** in the conversus output root:

```yaml
run:
  total_tokens: 487230
  total_agents: 35
  rounds_completed: 2
  termination_reason: max_rounds

per_agent:
  functional-typing:
    launches: 10
    total_tokens: 142000
    avg_tokens_per_launch: 14200
  integration-architect:
    launches: 10
    total_tokens: 156000
    avg_tokens_per_launch: 15600
  devils-advocate:
    launches: 10
    total_tokens: 138000
    avg_tokens_per_launch: 13800
  synthesizer:
    launches: 3
    total_tokens: 276000
    avg_tokens_per_launch: 92000
  arbiter:
    launches: 2
    total_tokens: 110000
    avg_tokens_per_launch: 55000

per_phase:
  review:
    agents_launched: 6
    total_tokens: 268000
  cross_review:
    agents_launched: 12
    total_tokens: 456000
  revision:
    agents_launched: 6
    total_tokens: 284000
  disputes:
    agents_launched: 6
    total_tokens: 236000
  synthesis:
    agents_launched: 3
    total_tokens: 276000
  arbitration:
    agents_launched: 2
    total_tokens: 110000

per_round:
  round_1:
    agents_launched: 17
    total_tokens: 680000
    disputes_at_end: 5
  round_2:
    agents_launched: 16
    total_tokens: 640000
    disputes_at_end: 3
```

**Data source**: Agent tool already returns `total_tokens` in usage stats. The orchestrator just needs to capture it instead of discarding it.

**Game engine integration**:
- Cost function: `total_tokens` is the cost; convergence improvement is the payoff
- Agent optimization: `credibility_score / total_tokens` = value-per-token metric
- Phase optimization: cross-review cost is quadratic in N — is the marginal quality worth 2x tokens when going from 3→4 agents?
- Round optimization: `disputes_resolved_per_round / tokens_per_round` shows diminishing returns

**Convergence-based agent trimming** (optimization):

Agents that converge on all topics could be trimmed from subsequent rounds to save tokens. Trimming levels:

| Level | What gets trimmed | Savings | Risk |
|-------|------------------|---------|------|
| Cross-review pairs | Skip A↔B cross-review when A and B agree on everything | 2 agents per converged pair | Low |
| Topics | Mark converged topics as settled; agents skip them | Reduces review length | Medium |
| Agents | Remove fully-converged agent from next round | N-1 cross-reviews + review + revision + dispute | High |

Cross-review pair trimming is the safest. The game engine computes a convergence score between each agent pair and skips cross-reviews above a threshold. This feeds naturally into the payoff matrix — convergence reduces the marginal value of further interaction.

**Round context optimization**:

Currently each agent starts with completely fresh context per phase (context isolation rule). Between rounds, agents get the prior synthesis + arbitration. Optimization opportunities:
- Feed converged positions as settled facts (reduce re-derivation tokens)
- Feed only the disputes relevant to each agent's domain (reduce noise tokens)
- Compute "context relevance score" per file per agent to rank what they should read first

**Structured storage for deliberation data**:

| Store | What it unlocks |
|-------|----------------|
| **PostgreSQL + pgvector** | Semantic search over past deliberations, find similar disputes across runs, cluster agent positions by embedding distance |
| **Memgraph** (in-memory, Cypher-compliant) | Fast graph traversal of deliberation structure: agents → positions → disputes → resolutions. Real-time queries during deliberation for convergence detection |
| **Neo4j** | Persistent graph DB for cross-run analysis. "Which agent pairs always converge? Which dispute patterns recur?" |
| **Redis** | Cache convergence scores between agent pairs. O(1) lookup for trimming decisions |
| **Structured YAML/JSON** | Minimum viable — typed output, Pydantic-validatable, no database dependency. First step before DB integration |

The path: YAML output now → Memgraph/pgvector when game engine materializes → cross-run analysis when enough deliberation history exists.

**Status**: Idea — captures multiple related optimization features. Candidate for game engine spec or standalone `0XX-deliberation-telemetry`.

---

## Deliberation as Training Data — Model Improvement Flywheel

**Origin**: Observed that conversus deliberation output naturally maps to model training paradigms. Every concession is a labeled preference example. Every arbitration ruling is constitutional AI. The game engine vision becomes a data flywheel.

**What conversus naturally produces → training paradigms**:

| Conversus Output | Training Use | Paradigm |
|-----------------|-------------|----------|
| Position → challenge → concession | Preference pairs (winner/loser positions) | DPO / RLHF |
| Arbiter + grounding document → ruling | Principle-grounded decision making | Constitutional AI |
| Multi-agent adversarial phases | Debate traces with explicit reasoning chains | Debate training |
| Revision: withdrawn/modified/surviving labels | Self-correction demonstrated with evidence | Iterative refinement |
| `[CLARIFY:]` tags on vague input | Uncertainty calibration, knowing what you don't know | Calibration training |
| Convergence trajectories across rounds | Reward signal (did agents converge? how quickly?) | Process reward models |
| Cross-review contradictions with resolution | Conflict resolution with grounded evidence | Reasoning under disagreement |

**The key insight**: Every concession is a labeled preference example. When functional-typing withdraws a recommendation because devils-advocate provided counter-evidence, that's a `(rejected_position, accepted_position, evidence)` triple — exactly what DPO needs. This data is generated as a byproduct of doing real review work.

**With structured storage** (Memgraph + pgvector), training data extraction becomes a query:

```cypher
// Extract preference pairs from concessions
MATCH (a:Agent)-[:CONCEDED]->(p:Position)<-[:CHALLENGED]-(b:Agent)
WHERE b.evidence IS NOT NULL
RETURN a.claim AS rejected, b.counter_claim AS preferred,
       b.evidence AS reasoning, p.final_status

// Extract constitutional AI examples from arbitration
MATCH (arb:Arbiter)-[:RULED_ON]->(d:Dispute)
MATCH (arb)-[:GROUNDED_IN]->(g:GroundingDoc)
RETURN d.positions, arb.ruling, g.principle_cited, arb.rationale

// Extract self-correction examples
MATCH (a:Agent)-[:REVISED]->(rec:Recommendation)
WHERE rec.disposition = 'modified'
RETURN rec.original_position, rec.revised_position,
       rec.triggered_by, rec.rationale
```

**The data flywheel**:
1. Run deliberations to review specs → produce structured training data
2. Fine-tune models on concession patterns, grounded reasoning, and self-correction
3. Fine-tuned models deliberate better (fewer uncited claims, more honest concessions)
4. Better deliberations produce higher-quality training data
5. Repeat

**Training data volume**: A single 2-round, 3-agent deliberation (like spec 007's review) produces:
- ~25 recommendation lifecycle examples (proposed → challenged → withdrawn/modified/surviving)
- ~15 concession/preference pairs
- ~10 cross-review contradiction resolutions
- ~5 arbitration rulings with grounding citations
- ~18 convergence examples with evidence basis

At scale (running conversus on every spec, plan, and implementation), this generates thousands of high-quality examples per project lifecycle.

**Relationship to credibility scoring**: Credibility scores become the reward signal. An agent with high credibility (grounded claims, honest concessions) produces training examples that reinforce good reasoning behavior. An agent with low credibility (uncited claims, stubbornly defended wrong positions) produces negative examples.

**Relationship to game engine**: The Nash equilibrium optimizer isn't just about convergence quality — it's about maximizing training signal per token spent. The game engine's objective function could include a "training data value" term alongside convergence and cost.

**Status**: Idea — requires structured output (YAML minimum, graph DB optimal) before training data extraction is practical. Long-term north star that gives the game engine a dual purpose: better deliberations AND better models.
