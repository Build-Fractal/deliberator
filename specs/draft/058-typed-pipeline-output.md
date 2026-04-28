# Feature Specification: Typed Pipeline Output (In-Memory Deliberation Representations)

**Feature ID**: `058-typed-pipeline-output`
**Created**: 2026-04-12
**Status**: Draft (placeholder — implement after 057)
**Depends On**: `055-capability-registry`, `056-deliberation-persistence`, `057-settings-architecture`
**Motivated by**: spec 056 §8 future consideration + constitutional alignment analysis

---

## 1. Problem

The conversus pipeline communicates between phases via **markdown files on disk**. Phase 1 writes `review.md`, Phase 2 reads it, pastes the text into an LLM prompt, and writes `cross-review.md`. Every downstream consumer (synthesis parsing, MCP tool responses, persistence, the `show` tool, quality linting) re-parses the same markdown to extract structured data.

This violates three constitutional principles:

- **VI (Scripts Over Markdown)**: "If a document is consumed by automation or agents to make decisions, it SHOULD be structured data — not prose that must be parsed ambiguously." The pipeline's inter-phase IPC is literally "write markdown, read markdown, hope the parser finds the right headings."

- **IX (Explicit Typing)**: "ALL data structures MUST use Pydantic models for validation and type safety." Pipeline output spends most of its lifecycle as untyped strings. `parse_synthesis` is an after-the-fact attempt to type what should have been typed at birth.

- **XI (Single Source of Truth)**: Every consumer re-parses the markdown independently, risking divergence between what the file says and what each parser extracts. The typed object should be the single source; files should be a serialization.

---

## 2. Proposed architecture

**In-memory typed objects are the pipeline's native output. Files become one serialization format among several.**

### 2.1 Typed output models

```python
from pydantic import BaseModel

class AgentReview(BaseModel):
    agent: str
    phase: str  # "review"
    text: str
    timestamp: datetime

class CrossReview(BaseModel):
    reviewer: str
    reviewee: str
    contradictions: list[str]
    tensions: list[str]
    agreements: list[str]
    text: str
    timestamp: datetime

class Revision(BaseModel):
    agent: str
    withdrawn: list[str]
    modified: list[str]
    surviving: list[str]
    new_recommendations: list[str]
    text: str
    timestamp: datetime

class Dispute(BaseModel):
    description: str
    agents_involved: list[str]
    unresolved_reason: str
    resolution_evidence: str

class Synthesis(BaseModel):
    headline: str
    convergence_points: list[str]
    surviving_disputes: list[Dispute]
    recommendations: list[dict[str, Any]]
    full_text: str
    timestamp: datetime

class DeliberationResult(BaseModel):
    """Complete typed output of a deliberation pipeline run."""
    question: str
    mode: str
    agents: list[str]
    reviews: list[AgentReview]
    cross_reviews: list[CrossReview]
    revisions: list[Revision]
    disputes: list[Dispute]
    synthesis: Synthesis
    rounds_completed: int
    termination_reason: str
```

### 2.2 Pipeline flow change

```
BEFORE (file-mediated IPC):
  Phase 1 → write review.md → Phase 2 reads review.md → write cross-review.md → ...

AFTER (typed-object IPC):
  Phase 1 → AgentReview objects → Phase 2 receives objects → CrossReview objects → ...
                ↓                                                    ↓
          serialize to md (optional)                          serialize to md (optional)
```

### 2.3 Typing boundary

LLM agents still return free-text responses. The typing happens at the **dispatch boundary** — when the dispatcher receives the agent's text and wraps it in a typed object:

```python
# Agent returns untyped text
review_text = await dispatch_agent(agent, prompt)

# Typed at the boundary (principle IX: "parse at the boundary, type internally")
review = AgentReview(
    agent=agent.name,
    text=review_text,
    phase="review",
    timestamp=datetime.now(timezone.utc),
)
```

For structured phases (disputes, synthesis), the dispatcher can optionally parse the LLM's response into typed fields (extracting dispute descriptions, convergence points). If parsing fails, the raw text survives in the `.text` field — graceful degradation per the "malformed output is better than no output" principle (V).

### 2.4 Serialization as projection

Same pattern as the capability registry: one source, multiple surface-specific projections.

```python
class MarkdownSerializer:
    """Writes the traditional markdown file tree."""
    def serialize(self, result: DeliberationResult, output_dir: Path) -> None: ...

class JSONSerializer:
    """Writes a single structured JSON file."""
    def serialize(self, result: DeliberationResult, output_path: Path) -> None: ...

class MCPResponseSerializer:
    """Converts to DecideResult/RunResult for MCP tool responses."""
    def to_decide_result(self, result: DeliberationResult) -> DecideResult: ...

class StreamSerializer:
    """Emits MCP progress events during pipeline execution."""
    def on_phase_complete(self, phase: str, output: BaseModel) -> None: ...
```

---

## 3. What this unlocks

| Capability | Current (file-based) | After (typed objects) |
|---|---|---|
| `show_deliberation` | Reads markdown files, returns text | Returns typed fields OR rendered markdown — caller's choice |
| `show disputes` (semantic API) | Must parse markdown to find dispute sections | `[d for d in result.disputes]` — trivial |
| `compare_deliberations` | Parse both, diff the parsed output | Diff two `DeliberationResult` objects directly |
| Real-time streaming | Not possible — output exists only after pipeline completes | Emit typed events as each phase completes |
| Quality linting | `parse_synthesis` does brittle heading-based extraction | `result.synthesis.convergence_points` — no parsing |
| `linter/output_contract.py` | ~200 lines of markdown parsing | Becomes a thin type check — "does the Synthesis have a headline?" |
| Plugin consumption | Plugins parse markdown files to extract what they need | Plugins receive typed objects directly (principle XV — plugin isolation) |

---

## 4. Migration strategy

### Phase A: Define the output models

Create `engine/output_models.py` with the Pydantic models. No pipeline changes — just the type definitions.

### Phase B: Wrap at the dispatch boundary

Modify `engine/dispatch.py` to wrap agent responses in typed objects AFTER receiving them. The pipeline still writes markdown files (backward compat), but also produces typed objects alongside.

### Phase C: Dual output

Both typed objects AND markdown files are produced at every phase boundary. Downstream phases can consume either. This is the compatibility bridge — nothing breaks, everything can gradually migrate to typed consumption.

### Phase D: Flip the default

Downstream phases consume typed objects. Markdown files are written by the serializer at the end (or at each phase boundary for observability). Inter-phase IPC is in-memory. Files are derived, not primary.

### Phase E: Remove file-based parsing

`parse_synthesis`, `linter/output_contract.py`'s markdown extraction, and any other file-parsing code becomes unnecessary. Replace with direct typed access. The semantic API (show disputes, compare) becomes trivial.

---

## 5. Scope boundaries

- **This spec covers**: the output model definitions, the dispatch-boundary typing, and the serialization/projection layer
- **This spec does NOT cover**: changing how agents receive their prompts (templates still fill `{REVIEW_TEXT}` with rendered markdown from the typed object — same templates, different source), changing the SKILL.md orchestration logic, or adding new deliberation modes

---

## 6. Constitutional alignment

| Principle | How this spec satisfies it |
|---|---|
| VI (Scripts Over Markdown) | Pipeline output becomes structured data, not prose that must be parsed |
| VIII (Templating Over Inference) | No inference needed to extract disputes/revisions from markdown — they're typed fields |
| IX (Explicit Typing) | All pipeline output is Pydantic models from the dispatch boundary onward |
| IX (Parse at boundary) | LLM text → typed object at the dispatch boundary, typed internally thereafter |
| XI (Single Source of Truth) | The `DeliberationResult` object is the one authoritative source; files are derived |
| XV (Plugin Isolation) | Plugins receive typed objects, not raw files they must parse independently |

---

## 7. Key design question

> Should the in-memory representation be the pipeline's **native output format** (with files as a serialization), or should files **remain primary** with in-memory as a parsed projection?

**Recommendation: native output format (option 1).** The constitutional analysis unambiguously supports this. Every principle that touches data representation (VI, VIII, IX, XI) points toward typed objects as primary. Files-as-serialization is the same pattern as the capability registry (capabilities are the source; CLI/MCP/Plugin/MCPB files are projections) applied to pipeline output.

**The risk**: this is an engine-level refactor touching `engine/phases.py`, `engine/dispatch.py`, and every provider adapter. The 5-phase migration strategy (A→E) mitigates this by allowing gradual adoption — the pipeline produces both typed objects and files during the transition, and downstream consumers can migrate one at a time.

## 7.1 Alternative approach: tree-sitter typed markdown

> **Research note** (added 2026-04-13): Before committing to a full
> engine refactor, evaluate
> [treesitter-types-markdown](https://crates.io/crates/treesitter-types-markdown)
> — a Rust crate that provides typed AST nodes for markdown documents
> via tree-sitter grammars. This could enable a **hybrid approach**
> where:
>
> - The pipeline continues to output markdown files (no engine refactor)
> - A tree-sitter-based parser provides typed access to the markdown
>   structure (headings → sections → disputes/recommendations/etc.)
> - The "typed objects" in Phase B-D of the migration strategy become
>   **parsed projections** from the markdown AST rather than native
>   engine output
>
> Advantages over the full refactor:
> - No changes to `engine/phases.py` or `engine/dispatch.py`
> - Markdown files remain the canonical output (backward compatible)
> - The typed access layer is read-only and additive
> - tree-sitter parsing is deterministic and fast (no LLM inference
>   needed to extract structure)
> - Python bindings available via `tree-sitter` + language grammar
>
> Disadvantages:
> - Depends on markdown being well-structured (templates enforce this)
> - Adds a Rust/tree-sitter dependency to the Python stack
> - Parsing is per-file, not per-pipeline (no cross-file typed views
>   without an assembly step)
>
> This approach could satisfy the semantic API (show disputes, compare
> deliberations) WITHOUT the engine refactor, making it a significantly
> cheaper path to the same user-facing capabilities. Evaluate before
> choosing between Phase A-E refactor and the tree-sitter hybrid.

## 7.2 Alternative approach: Markdoc schema-driven typed AST

> **Research note** (added 2026-04-13): [Markdoc](https://markdoc.dev/)
> (by Stripe) is a stronger candidate than tree-sitter for typed
> markdown access. Where tree-sitter gives a generic markdown AST that
> requires custom domain rules for typing, Markdoc provides a
> **schema system** that maps markdown structures to typed nodes with
> validated attributes — exactly the "typed deliberation output"
> problem this spec describes.
>
> How it would work for conversus:
>
> 1. Define Markdoc schemas for each deliberation artifact type:
>    `AgentReview`, `CrossReview`, `Dispute`, `Synthesis`, etc.
> 2. Schemas map heading patterns to typed nodes: an h2 "Disputes"
>    with bullet children becomes a `DisputeSection` node where each
>    bullet is a typed `Dispute` with `agent`, `description`,
>    `unresolved_reason` attributes.
> 3. Conversus templates already enforce the heading structure —
>    Markdoc schemas formalize what templates enforce informally.
> 4. Agents continue producing standard markdown (no new syntax).
>    Markdoc parses plain markdown AND can apply schema-driven
>    transforms to type the nodes after parsing.
> 5. The typed AST is JSON-serializable → can be consumed by Python
>    handlers, MCP tools, the semantic API, and the Desktop Extension.
>
> Advantages over tree-sitter:
> - Schema-driven typing (not custom post-parse rules)
> - Validation at parse time (a "Disputes" section missing required
>   attributes fails validation, not silently drops data)
> - Render to multiple formats from one AST (HTML, React, plain text)
> - Active ecosystem (Stripe-maintained, used in production docs)
>
> Advantages over the full engine refactor (Phase A-E):
> - No changes to engine/phases.py or engine/dispatch.py
> - Markdown files remain canonical — typing is a read-side concern
> - Additive and read-only — zero risk to existing pipeline
>
> Tradeoffs:
> - JavaScript/Node.js dependency (Markdoc is JS-native). Options:
>   (a) run as a subprocess, (b) use the JSON AST from a Node script,
>   (c) port the schema logic to Python (Markdoc's AST is simple
>   enough for a lightweight Python reimplementation)
> - Schema maintenance: every template change needs a corresponding
>   schema update (but this is a feature, not a bug — it catches
>   template-schema drift at parse time)
>
> **Update 2026-04-13**: Markdoc is JavaScript-only — no Python SDK
> exists. The `markdoc` PyPI package is an unrelated abandoned project.
> Options: (a) subprocess to Node.js for Markdoc, (b) implement the
> Markdoc schema philosophy natively in Python using `markdown-it-py`
> as the parser with a custom schema validation layer on top, or
> (c) skip the markdown parser entirely and use Pydantic models over
> heading-based regex extraction — the output is generated by templates
> we control, so general-purpose parsing may be overkill.
>
> **Revised recommendation**: adopt Markdoc's design philosophy
> (schema-driven typed content, validate at parse time) but implement
> in Python. The simplest path: Pydantic models that validate extracted
> sections from the existing `parse_synthesis` pattern, extended to
> cover all 5 phases (not just synthesis). This adds zero dependencies
> and builds on the stack we already have.

---

## 8. Sources

| Source | Use |
|---|---|
| `specs/056-deliberation-persistence.md` §8 | Origin of this spec — future consideration note about in-memory representations |
| `CONSTITUTION.md` principles VI, VIII, IX, XI, XV | Constitutional mandate for typed data over parsed prose |
| `specs/055-capability-registry.md` | The "one source, multiple projections" pattern this spec extends to pipeline output |
| `linter/output_contract.py` | The ~200 lines of markdown parsing that this spec would eventually eliminate |
| `engine/phases.py` | The pipeline implementation that would need refactoring in Phases B-D |
