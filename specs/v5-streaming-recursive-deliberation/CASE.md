# CASE: Streaming Recursive Deliberation via Protocol Buffers + gRPC

**Status:** **CASE — pre-spec** (2026-05-13)
**Type:** Motivation argument for a future v5.0.0 MAJOR amendment. Not yet a formal spec; not yet under the four-stage verification protocol. Promotes to `spec.md` once the case is endorsed.
**Author:** Brian Slater (conceived 2026-05-13, in the conversation after v4.2.0 ratification + F1 implementation)
**Provisional version:** v5.0.0 (MAJOR — fundamental engine contract change)
**Depends on:** v4.2.0 (Component Principle XXIX — Structured Deliberation Outputs) ratified. The proto wire format extends, not replaces, the JSON Schema persistence format.

---

## 1. Motivation

The v4.X cycle (v4.0.0 tier extraction → v4.1.0 Tier 2 Principle XXVIII → v4.2.0 Component Principle XXIX) standardizes conversus-oss as a **file-producing engine**. Six output types (review, cross-review, revision, disputes, synthesis, arbitration) emit declared, schema-validated JSON envelopes to disk. Downstream consumers (orchestrator spec-kit adapter, conversus-enhanced) read those files asynchronously.

This architecture has a structural ceiling:

1. **Deliberations are flat, not recursive.** A `QUESTION.md` poses one set of questions; one synthesis integrates phase 1-4 outputs; one arbiter rules. Complex questions that decompose into hierarchies of sub-questions (each with its own sub-deliberation) cannot be expressed as a single conversus run. The workaround is manual orchestration: run multiple flat deliberations, hand-combine their verdicts. This was the pattern used implicitly in v4.1.0's split between Tier 1 / Tier 2 placement debates — they were treated as separate deliberations because the engine couldn't express "deliberate Tier-placement AS A FUNCTION OF the cross-tier-coherence verdict."

2. **Outputs are batch, not streamed.** A deliberation runs N minutes; consumers wait. Real-time progress visibility is limited to log tailing. Backpressure, cancellation, interleaving — all impossible. The Phase 5 synthesis-prompt overflow bug at 230K chars (logged 2026-05-06) was made worse by batch semantics: by the time the crash surfaced, all earlier phases had already paid their compute cost. A streaming architecture would have surfaced the prompt-size problem mid-flight.

3. **Consumers re-implement event semantics.** The orchestrator adapter currently grep-parses markdown files; it'll JSON-parse them after v4.2.0 lands. But what it actually wants is **events**: "Phase 5 just emitted a synthesis with disputes; please dispatch arbitration." It re-derives this from filesystem polling + content inspection. The engine has the event semantics internally — it just doesn't expose them.

4. **The objective function is implicit.** Each `QUESTION.md` encodes a deliberation goal as prose. There's no machine-readable representation of "the question this deliberation is answering," which makes it impossible to:
   - Decompose the question programmatically
   - Compose sub-deliberation verdicts into a parent verdict via a defined integration rule
   - Verify mechanically that the synthesis answers the question (it currently passes through prose into prose)

This CASE argues for a future v5.0.0 amendment that addresses (1)-(4) together by introducing:

- **A first-class objective-function model** (the deliberation goal as a typed structure).
- **A recursive engine** that decomposes an objective into sub-objectives, runs sub-deliberations, integrates verdicts.
- **A streaming wire format** that emits per-event progress to consumers in real-time.
- **Protocol Buffers + gRPC** as the wire format for the streaming + service contract surface.

JSON Schema (v4.2.0 ratified) remains the canonical **file** format. Proto is the **wire** format. They coexist; one does not displace the other.

---

## 2. Why proto + gRPC for the wire format

### 2.1 Streaming primitives are native, not bolted on

The v4.2.0 JSON-Schema-over-files architecture is request-response by nature: produce a complete file, consumer reads it. To do streaming on top of that, you'd add:

- A poll loop or filesystem-watcher in the consumer
- A line-delimited JSON event format (NDJSON / JSONL)
- An out-of-band signaling mechanism for completion / cancellation
- Custom retry / resume semantics if the consumer disconnects

That's reinventing what gRPC gives you for free. gRPC server-streaming RPC means:

```proto
service DeliberationService {
  rpc Deliberate(DeliberationRequest) returns (stream DeliberationEvent);
}
```

Each `DeliberationEvent` flows from server (the engine) to client (the consumer) as it happens, with native:

- **Flow control** — consumer-side backpressure via `ServerStreamingCall.Recv()` pacing
- **Cancellation** — client closes stream; server's context cancels mid-flight; pending agents abort cleanly
- **Resumption** — combine with cursor-based event IDs for resumable streams across reconnects
- **Multiplexing** — many concurrent deliberations on one connection (HTTP/2 underneath)

### 2.2 Bi-directional streaming unlocks interactive deliberation

```proto
rpc InteractiveDeliberate(stream DeliberationCommand) returns (stream DeliberationEvent);
```

The consumer sends commands (refine question, inject new evidence, override an agent's verdict for testing, request an early arbitration) while events stream back. This is the substrate for:

- A web UI watching a deliberation as it runs, with a "pause and inject context" button
- An orchestrator that intervenes mid-deliberation when its own state changes
- Human-in-the-loop arbitration where the arbiter is a person reviewing agent outputs in real-time
- Multi-tenant deliberation service where many clients have many concurrent streams

JSON-Schema-over-HTTP-REST could approximate this with WebSockets or Server-Sent Events, but you're hand-rolling what gRPC ships as the canonical pattern.

### 2.3 Field-number versioning safety for long-running services

For a file format that ratifies once and gets re-emitted forever, JSON Schema's name-based field identity is fine — SemVer governs field renames as MAJOR bumps.

For a wire format that a fleet of consumers in different languages keeps speaking over time, **field-number identity is much safer**. A proto file:

```proto
message ArbitrationRuling {
  string question_id = 1;
  string verdict = 2;
  string rationale = 3;
  repeated string citations = 4;
  // Added in v5.1.0
  optional ConfidenceInterval confidence = 5;
}
```

Field 5 can be added; old consumers ignore it. Field 2 can be renamed in the proto file (e.g., `verdict` → `ruling`); old consumers still read field 2 by number. Field 2 cannot be re-typed (string → int) without breaking the wire — which is exactly what we'd want for a stable interface.

This matters in proportion to how many independent consumers speak the wire and how often the schema evolves. For the v4.X file format with ~3 known consumers and a stable governance cadence, JSON Schema's name-based identity is adequate. For a v5.X wire format that could be spoken by orchestrator + conversus-enhanced + future siblings + third-party SDKs + a hosted UI + research-time analysis pipelines — proto's field-number safety net becomes load-bearing.

### 2.4 Multi-language SDK story

The v4.2.0 cycle assumes Python everywhere — the conversus engine is Python, the orchestrator adapter is Python, future siblings are likely Python. JSON Schema → Pydantic v2 via `datamodel-code-generator` is the F2 path.

A wire-format service contract opens the door to:

- **Orchestrator pulled out of Python** (e.g., Go or Rust for performance-critical orchestration)
- **Third-party arbiter implementations** (e.g., a research group writes an arbiter in Rust that plugs in over gRPC)
- **Consumer SDKs for Slack apps, CI bots, IDE plugins** — each language gets generated client stubs from one canonical proto

Proto's `protoc --python_out --go_out --rust_out --ts_out ...` is the canonical entry point. JSON Schema's equivalent is `quicktype` / `datamodel-code-generator` / OpenAPI codegen — strong but a multi-tool chain rather than a single canonical compiler. The integration cost is higher when you want first-class clients in five+ languages.

### 2.5 Wire efficiency for high-throughput recursive workloads

A 100KB synthesis as proto binary is roughly 25-40KB. That's a 60-75% reduction. For files-on-disk this is irrelevant. For recursive deliberations that emit thousands of events per parent run, multiplied across many concurrent deliberations on one server, the cumulative wire savings matter — both for bandwidth and for parse cost at the consumer.

---

## 3. Recursive deliberation — what it means concretely

The current engine treats a deliberation as a flat pipeline:

```
QUESTION → Phase 1 reviews → Phase 2 cross-reviews → Phase 3 revisions
        → Phase 4 disputes → Phase 5 synthesis → Phase 6 arbitration → VERDICT
```

Recursive deliberation makes the verdict at each phase potentially the **objective** of a sub-deliberation:

```
QUESTION (Q1 + Q2 + Q3 axes)
   ├─ sub-deliberation Q1 axis → sub-VERDICT_Q1
   ├─ sub-deliberation Q2 axis → sub-VERDICT_Q2
   └─ sub-deliberation Q3 axis → sub-VERDICT_Q3
META-ARBITER integrates {Q1, Q2, Q3 verdicts} → PARENT_VERDICT
```

Or even deeper:

```
QUESTION
   └─ Q3 axis "internal contradiction check"
       ├─ sub-deliberation: contradiction with Principle V?
       ├─ sub-deliberation: contradiction with Principle XXVIII?
       └─ sub-deliberation: contradiction with Principle II?
   META-ARBITER for Q3 integrates the three principle-specific verdicts
PARENT META-ARBITER integrates {Q1, Q2, Q3} as before
```

### 3.1 The objective-function framing

Each (sub-)deliberation has an **objective function** — a structured representation of what it's deciding. Sketch:

```proto
message Objective {
  string id = 1;                           // Stable across sub-tree
  string statement = 2;                    // Human-readable question

  oneof verdict_space {
    BinaryVerdict binary = 10;             // PASS / FAIL
    OrdinalVerdict ordinal = 11;           // tier-1 PASS-WITH-CLARIFICATIONS / etc.
    NumericVerdict numeric = 12;           // confidence in [0,1] or score
    CategoricalVerdict categorical = 13;   // one-of enum values
  }

  repeated Predicate predicates = 20;      // What the verdict must satisfy
  AggregationRule aggregation = 30;        // How child verdicts roll up
}

message Predicate {
  string description = 1;
  string field_path = 2;                   // Slot-path in synthesis output
  string operator = 3;                     // "MUST_BE_PRESENT" / "MUST_MATCH_REGEX" / etc.
  string expected = 4;
}
```

The objective function is **load-bearing for verification**: the engine can check post-deliberation whether the synthesis output satisfies the objective's predicates. If predicates fail, that's a mechanical signal that the deliberation didn't actually answer its question — separate from the arbiter's verdict.

This makes "the question" a typed first-class entity, not just prose. Compare to v4.2.0 JSON Schema:

- v4.2.0 schemas type the **outputs** of each phase (a synthesis has these fields, an arbitration has those fields).
- v5.0.0 objective function types the **input question** (this deliberation is answering this question, with these acceptance predicates).

Both are needed. Output schemas make Phase 6's trigger mechanical (no more grep miss). Objective schemas make question-answer verification mechanical (no more "the synthesis kind of answered Q3 but it's hard to tell").

### 3.2 Decomposition rules

A parent objective decomposes into sub-objectives via a declarative rule:

```proto
message Decomposition {
  oneof rule {
    AxisSplit axis = 1;                    // Split by Q1/Q2/Q3 axes
    PredicateExpansion predicate = 2;      // Each predicate becomes its own sub-deliberation
    SourceSplit source = 3;                // Split by which doc the question is about
    ManualEnumeration manual = 4;          // Author writes sub-objectives explicitly
  }

  uint32 max_depth = 10;                   // Hard cap on recursion depth
  uint32 max_breadth = 11;                 // Hard cap on siblings per node
  ResourceBudget budget = 20;              // Token / time / agent-count budget per sub-tree
}
```

Termination is **mechanical** (max depth + max breadth + budget exhaustion), not heuristic. A poorly-designed decomposition can't infinite-recurse.

### 3.3 Aggregation — meta-arbitration

A parent verdict is computed from child verdicts via a declared aggregation rule:

```proto
message AggregationRule {
  oneof method {
    AllMustPass all_pass = 1;              // ANY child FAIL → parent FAIL
    Majority majority = 2;                 // > 50% pass → parent PASS
    WeightedScore weighted = 3;            // Sum(weight_i * verdict_i) > threshold
    HierarchicalMetaArbiter meta = 4;      // Spawn a meta-arbiter to integrate
  }
}
```

The `HierarchicalMetaArbiter` method is the most powerful: spawn a small (e.g., 2-agent) sub-deliberation whose objective is "given these child verdicts, what's the integrated parent verdict?" — recursion all the way down.

Compare to the current engine's single arbiter (Phase 6): it integrates synthesis + disputes into one verdict via prose reasoning. In the recursive model, that integration is itself a deliberation, governed by an aggregation rule.

### 3.4 What recursion unlocks

- **Large specs decompose naturally.** A 1000-line spec doesn't need to fit one synthesis prompt. Each section gets its own sub-deliberation; a meta-arbiter integrates section verdicts. This is the architectural fix for the v4.1.0 Phase 5 synthesis-prompt-overflow bug at the engine level.
- **Cross-cutting concerns become first-class.** "Does this spec violate Tier 1 Principle II?" is one sub-deliberation. "Does it violate Tier 2 Principle V?" is another. Each runs against the same spec text but with focused agent prompts and focused verdict spaces.
- **Adversarial decomposition.** A skeptical sub-deliberation can be spawned alongside an optimistic one; the meta-arbiter integrates their independent verdicts. This is how the four-stage verification protocol could be expressed as a recursive structure rather than a sequential pipeline.
- **Composability with external tools.** A sub-deliberation could be replaced by a non-LLM evaluator: a CI check, a benchmark run, a static analyzer. As long as it returns a verdict matching the parent objective's `verdict_space`, the parent doesn't care if a deliberation or a Python function produced it.

---

## 4. Streaming events — the wire shape

```proto
message DeliberationEvent {
  string event_id = 1;
  string deliberation_id = 2;              // Root of the tree
  optional string parent_event_id = 3;     // Parent in the event-causal-graph
  google.protobuf.Timestamp ts = 4;

  oneof body {
    DeliberationStarted started = 10;
    PhaseEntered phase_entered = 11;
    AgentDispatched agent_dispatched = 12;
    AgentOutputChunk agent_chunk = 13;      // Token-stream from an agent
    AgentOutputCompleted agent_completed = 14;
    SubDeliberationSpawned sub_spawned = 15;
    SubDeliberationCompleted sub_completed = 16;
    ArbitrationVerdictRendered verdict = 17;
    DeliberationCompleted completed = 18;
    Error error = 99;
  }
}
```

Key properties:

- **Causal graph via `parent_event_id`**: events form a DAG, not just a sequence. An `AgentOutputCompleted` for agent X's Phase 1 review caused by a `PhaseEntered` for Phase 1, in turn caused by a `DeliberationStarted` at the root. Recursive sub-deliberations have their own `deliberation_id` but `parent_event_id` ties the spawn to the parent context.
- **Token-level streaming**: `AgentOutputChunk` carries partial output as agents generate. The consumer can render progress live, watch for early divergence, cancel a misbehaving agent before it finishes.
- **Verdict events are atomic**: `ArbitrationVerdictRendered` is the load-bearing payload — it carries the structured verdict per the objective's `verdict_space`. Consumers that only care about verdicts subscribe to this event type and filter the rest.
- **Errors are first-class**: `Error` events carry structured failure info (agent timeout, schema validation failure, budget exhaustion). Consumers can act on errors without parsing arbiter prose.

### 4.1 Bi-directional commands

```proto
message DeliberationCommand {
  oneof command {
    StartDeliberation start = 1;
    PauseDeliberation pause = 2;
    ResumeDeliberation resume = 3;
    CancelDeliberation cancel = 4;
    InjectEvidence inject = 5;             // Mid-flight context update
    OverrideAgent override = 6;             // Replace an agent's verdict (testing)
    BumpResourceBudget budget = 7;
  }
}
```

`InjectEvidence` is the most novel: a consumer that's watching the deliberation and notices the agents are working with stale context can push new context into the engine. The engine routes the injected evidence to relevant agents on their next turn. This is the substrate for orchestrator-conversus tight coupling: orchestrator owns the spec lifecycle, conversus deliberates against the current spec snapshot, but if the spec changes mid-deliberation, orchestrator can inject the diff rather than killing the run.

---

## 5. Coexistence with v4.2.0 JSON Schema

The proto wire format **does not replace** the JSON Schema file format. They coexist:

| Surface | Format | Use case |
|---|---|---|
| Persistence (`deliberations/.../agent/review.md`-equivalent) | JSON Schema (v4.2.0) | Audit trail, human review, mechanical CI validation, file-system durability |
| Wire (`grpc://engine.buildfractal/Deliberate(...)`) | Protocol Buffers (v5.0.0) | Streaming events, recursive composition, bi-directional commands, multi-language consumers |
| Service contract (`DeliberationService` in `.proto`) | Protocol Buffers + gRPC | RPC schema, generated SDKs, versioning safety |
| Objective function (the question being deliberated) | Protocol Buffers (v5.0.0) | Typed verdict spaces, predicates, decomposition rules, aggregation methods |

The mapping between proto messages and JSON envelopes is mechanical: each proto message has a one-to-one JSON Schema representation (proto3 already defines the canonical JSON encoding). The engine emits both: proto over the wire for live consumers, JSON Schema-validated files for the persistence layer.

This means a single source of truth for the data model — written in `.proto`, codegened into both Python Pydantic types (for the engine) and JSON Schemas (for file validation per v4.2.0). The proto compiler becomes the canonical entry point; the JSON Schemas are derived artifacts.

### 5.1 Migration path

- **v5.0.0 Phase 1**: stand up the proto schema as a parallel surface. Wire format defined, but no consumers required to migrate. JSON Schema files remain canonical for persistence.
- **v5.0.0 Phase 2**: orchestrator opts into the wire format for real-time event consumption. Files-on-disk still emitted for audit.
- **v5.0.0 Phase 3**: recursive deliberation engine implemented. Existing flat deliberations work as the special case (depth=0).
- **v5.0.0 Phase 4**: objective-function model required for new deliberations. `QUESTION.md` becomes a derived rendering of the proto `Objective` message.
- **v5.1.0+**: third-party arbiter SDKs in additional languages; UI consumers; hosted-service offering.

The cliff at v4.2.0's 2026-12-01 is independent of v5.0.0's introduction. v4.2.0 ratifies the file format. v5.0.0 would ratify a new wire format alongside it. Markdown-format templates are deprecated at the v4.2.0 cliff; JSON Schema files remain the canonical persistence format indefinitely; proto becomes available as a wire surface when v5.0.0 ratifies.

---

## 6. Costs and risks

### 6.1 Adoption costs

- **`protoc` toolchain in CI**: each repo that imports the proto schema needs the proto compiler at build time. This is well-trodden territory (protoc-gen-* plugins are mature) but it's a new build dependency.
- **Generated code management**: either commit generated stubs to repo (versionable but noisy diffs) or generate at build time (cleaner but slower CI). Most large proto consumers commit generated code; conversus-oss could follow that pattern.
- **gRPC operational complexity**: TLS termination, auth, load balancing, observability. For a single-tenant local engine these are trivial; for a hosted multi-tenant service they're real. The case argues for proto + gRPC; the operational scope depends on the use case.

### 6.2 Debuggability tradeoffs

A `review.proto.bin` file is not human-readable. Debugging requires `protoc --decode_raw <file>` or equivalent. The v4.2.0 JSON Schema files remain the human-readable audit trail; proto wire packets are not stored as files in the persistence layer.

Compare proto-as-wire-only vs proto-as-file-format:
- **Proto as wire only (this CASE's recommendation)**: human-readable audit trail preserved (JSON Schema files); streaming benefits gained; debuggability of stored artifacts unchanged.
- **Proto as file format too**: would lose the audit-trail readability; not recommended.

### 6.3 Versioning two formats in lockstep

Every schema change must update both the .proto file AND the JSON Schema files (or the JSON Schemas must be generated from the .proto). The latter is preferable — one source of truth.

Codegen flow:
```
*.proto (canonical)
  ├─ protoc-gen-python   → engine/schema/v1/*.pb.py (engine internal types)
  ├─ protoc-gen-pydantic → engine/schema/v1/*.py (Pydantic models for validator)
  ├─ protoc-gen-jsonschema → engine/schema/v1/*.schema.json (file format)
  └─ protoc-gen-grpc-* → engine/schema/v1/*_grpc.* (service stubs in each target language)
```

This way v4.2.0's `engine/schema/v1/*.schema.json` files become **generated artifacts** from the .proto source. JSON Schema correctness is then a function of .proto correctness, which is enforced by the compiler.

### 6.4 The principle V tension

The arbitration record for v4.2.0 made much of "malformed output is better than no output." JSON's text-based recovery semantics support this naturally: a corrupted file can be hand-edited; a missing closing brace is a one-character fix.

Proto binary recovery is harder. A single bit flip in a varint length field can desynchronize the rest of the parse.

**Mitigation**: the wire format is ephemeral (over-the-network packets, not files). The persistence format remains JSON Schema. Wire-format corruption affects in-flight events; consumers retry or resume. File-format corruption affects audit trail; JSON's text-recovery semantics still apply.

In other words: Principle V applies to the persistence layer (where it's load-bearing for audit trails). The wire layer is allowed stricter "fail fast and retry" semantics because wire corruption is a transport-layer event, not a content-layer event.

---

## 7. Cross-tier implications

This is a v5.0.0 MAJOR amendment. It affects:

- **Tier 1 Principle II (Stable Interfaces)**: the wire format is a new stable interface; the .proto file is its declaration. Principle II's coverage extends.
- **Tier 2 Principle XXVIII (Persistence Contract Discipline)**: unchanged. Persistence remains JSON Schema files. The wire format is a NEW surface, not a replacement for persistence.
- **Tier 3 Component Principle XXIX (Structured Deliberation Outputs)**: extended. The output structure now has two representations (proto wire + JSON file), but they're isomorphic and the .proto is the canonical source.
- **Suite admission for new sibling repos**: future siblings that produce deliberation-shaped outputs can implement the wire format directly without re-implementing the engine. This lowers the barrier to suite expansion.

### 7.1 New principle? Or amendment to XXIX?

Two options for the constitutional shape:

- **Option A**: Amend Component Principle XXIX to include the wire format as a new sub-clause. Single principle; two representations (file + wire).
- **Option B**: Add a new Tier 2 Principle XXX (Streaming Recursive Deliberation Discipline) for the engine architecture + a new Component Principle XXX-engine in conversus-oss for the proto implementation.

Option B has more ceremony but cleaner separation: XXVIII covers persistence, XXX covers streaming. XXIX (conversus-oss specific JSON Schema for deliberation outputs) becomes a Component-tier implementation of both.

The case doesn't decide this; the full v5.0.0 spec would.

---

## 8. Sequencing — what would have to happen before v5.0.0

This is a future-spec direction. Concrete sequencing:

1. **Complete v4.2.0 implementation.** F1 ratified 2026-05-13 (this PR's parent). F2 (parser, validator, CI workflow, performance budget framework) next. Through F2-F7 per v4.2.0 § 11.
2. **Validate the JSON Schema architecture at scale.** Re-render the v4.1.0 audit trail (~150 files) as JSON. Confirm the schema accommodates real production deliberations. Measure validator latency against the v4.1.0 synthesis corpus.
3. **Prototype a proto-wire implementation as a side experiment.** Not yet a spec; just a working demonstration. Probably as a `conversus.streaming` plugin module under conversus-enhanced (paid) initially, to keep the prototype out of OSS's ratification path.
4. **Run a recursive deliberation manually.** Decompose v4.2.0 itself retroactively: each Q-axis as a sub-deliberation; meta-arbiter integrates. Confirm the verdict matches the actual v4.2.0 arbitration record. This is the methodological self-check.
5. **Author v5.0.0 spec.** With prototype evidence + methodological validation + format-comparison data in hand. Full four-stage verification protocol.
6. **Ratification timeline.** Unconstrained — no constitutional cliff date driving v5.0.0. Implementation cost is large; ratification can wait for organic demand from a streaming consumer (web UI, hosted service, multi-language SDK consumer).

---

## 9. What "decomposable deliberation via objective function" buys

To restate the core thesis: the engine's value increases monotonically with how much of the deliberation logic is **declarative + machine-readable** rather than prose-encoded.

- v4.2.0 made the **outputs** declarative (JSON Schema).
- v5.0.0 (proposed) makes the **inputs** declarative (objective function as proto message).
- The phase pipeline itself becomes a function of the objective function: which agents to dispatch, which sub-deliberations to spawn, how to integrate verdicts — all derivable from the objective's declared decomposition rule.

The endgame: an engine where a "deliberation" is a typed call against a typed objective, returns a typed verdict, and emits typed events as it runs. The current prose-driven flow becomes a special case (objective with no decomposition; flat phase pipeline; arbiter integrates synthesis manually).

This isn't an argument against JSON Schema or against the v4.2.0 work. It's an argument that **JSON Schema is the right format for the file artifact** (human-readable, recovery-friendly, ecosystem-mature) AND **proto+gRPC is the right format for the wire/service contract surface** (streaming, multi-language, field-number-safe), AND the two coexist when you have both surfaces to support.

v4.2.0 doesn't yet need the wire surface — its consumers are happy with files. v5.0.0 is the inflection point where the wire surface starts paying its costs: real-time UI, multi-language consumers, recursive composition, hosted-service offering. When that inflection arrives, proto is the right answer.

---

## 10. Open questions for the future spec

These are NOT acceptance criteria for this CASE doc; they're the load-bearing decisions the v5.0.0 spec would need to resolve:

1. **Where does the .proto schema live?** Same repo as conversus-oss? Separate `Build-Fractal/conversus-proto` repo for canonical multi-language consumption? Versioned independently from the engine?
2. **Codegen artifact management.** Commit generated stubs vs build-time generation. Per-language repo vs polyglot monorepo.
3. **Service hosting model.** Local-only (in-process gRPC server)? Process-local (Unix socket)? Network (HTTP/2 + TLS)? All three?
4. **Auth model.** Anonymous? mTLS? OAuth? Different per hosting model?
5. **Backward compatibility scope.** Does the wire format need to support pre-v5.0.0 file-format-only consumers indefinitely? Probably yes during a transition window; spec the window.
6. **Failure semantics in recursion.** A sub-deliberation crashes — does the parent fail? Continue with partial verdicts? Re-spawn the sub? Retry policy is a load-bearing decision.
7. **Resource accounting.** Token budgets, time budgets, agent-count budgets — how are they declared, propagated to sub-deliberations, accounted at the parent?
8. **Determinism guarantees.** Recursive deliberation introduces non-determinism (which sub finishes first?). Are aggregation rules order-invariant by construction, or do we require canonical ordering for reproducibility?
9. **Relationship to existing Phase 6 arbiter.** Is the meta-arbiter the same engine machinery? Different machinery? Does the existing arbiter become a special case (depth=0)?
10. **The objective-function language itself.** How rich? Just predicates + verdict-space, or full propositional logic? Domain-specific language? Embedded in proto comments?

---

## 11. Recommendation

Endorse this CASE as a future-spec direction. Defer v5.0.0 drafting until:

- v4.2.0 implementation is substantially complete (F2 + F3a pilot through step 6 in § 11)
- A streaming-consumer demand surfaces concretely (web UI, hosted service, multi-language SDK consumer, etc.)
- A recursive deliberation prototype validates the engine semantics in a controlled experiment

This is not a near-term implementation target. It's a documented architectural direction that the v4.X cycle's work positions us for. The honest "free APIs" advantage of proto is real but it's a function of the use case — and v4.X's use case (file persistence + audit trail) is genuinely best served by JSON Schema. v5.X's use case (streaming + recursive + multi-language wire) is genuinely best served by proto + gRPC.

Both can be true. They're addressing different surfaces.
