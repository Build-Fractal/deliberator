# Cross-Review of Developer Advocate -- Round 2

**Reviewer**: code-verifier
**Reviewing**: developer-advocate Round 2 review
**Round**: 2 of 3

---

## Dangerous Contradictions

### 1. The `score()` call convention is documented in source but developer-advocate claims it is "undocumented"

Developer-advocate's Missed Opportunity #5 states: "the building-domains guide shows scaffold YAML definitions and the scoring pipeline hooks but never shows the actual `score()` call" and asks "Is the scaffold name a string? A Path? A loaded object?" This framing suggests the answer is unknowable, but the source code at `domains/base.py` L711-714 has an explicit type annotation and docstring:

```python
def score(
    self,
    variables: dict[str, Any],
    scaffold: str | Scaffold,
) -> DomainScore:
```

The docstring at L717-720 further states: "If `scaffold` is a string, it is treated as the scaffold name and resolved from `self.scaffold_dir` by trying extensions `.yml`, `.yaml`, and `.json` in order."

I agree the *documentation* does not show this call, and that is a real gap (my review's P2 recommendation #6 on API reference member lists would surface this). But developer-advocate's characterization implies the interface is ambiguous or undiscoverable. It is neither -- it is typed and documented in the docstring. The gap is that the developer guide does not demonstrate it, not that the contract is unclear.

**Why this matters**: If the implementation plan treats `score()` as having an undefined contract, someone may over-engineer the documentation (inventing conventions that diverge from the actual signature). The fix is straightforward: show the call with a string scaffold name in the end-to-end tutorial. No new design decisions needed.

**Both reviews agree** the building-domains guide needs a running example. We disagree on whether this is a "contract discovery" problem (developer-advocate) or a "documentation coverage" problem (code-verifier). The distinction affects scope: a coverage fix is a code snippet; a contract discovery fix implies restructuring the guide.

### 2. Error handling characterization is partially wrong for domain extractors

Developer-advocate's Missed Opportunity #2 asks: "Are exceptions caught by the orchestrator? Does a failed plugin prevent downstream consumers from running? Should plugins return empty/default data or raise?" and then in Actionable Recommendation #5 states: "Domain extractor exceptions should return empty dicts rather than raising, to allow partial scoring."

The source tells a different story. At `domains/base.py` L697-708, the `extract()` method already catches extractor exceptions:

```python
for extractor in self.get_extractors():
    try:
        result = extractor.extract(context)
        merged.update(result)
    except Exception:
        logger.warning(
            "Extractor '%s' in domain '%s' raised, skipping.",
            extractor.name,
            self.name,
            exc_info=True,
        )
```

And for plugins, `execute_hooks` at `plugins/base.py` L519-525 catches plugin exceptions:

```python
except Exception:
    logger.warning(
        "Plugin '%s' raised an exception at hook '%s', skipping.",
        plugin.name,
        hook.value,
        exc_info=True,
    )
```

Developer-advocate's recommendation to "return empty dicts rather than raising" is actively misleading: the framework already handles exceptions gracefully. Telling extractor authors to swallow exceptions would hide bugs. The correct documentation would say: "Raise freely -- the framework catches and logs. A failed extractor's variables are simply absent from the merged dict."

**Why this matters**: If the documentation tells authors to return empty dicts on error, they will mask failures that the framework was designed to surface in logs. My review (P2 recommendation #6) addresses this more precisely by proposing to document the actual catch-and-skip behavior.

**Developer-advocate correctly identifies** that the documentation gap exists. The recommended fix is wrong in its specifics. We should converge on documenting the framework's actual behavior rather than inventing a new convention.

### 3. The `CallbackEmitter` description conflates callable and `__call__`

Developer-advocate's Missed Opportunity #4 states: "`CallbackEmitter` calls `self._callback(event)` on the handler, meaning `RichProgressHandler` must be callable (implement `__call__`)."

Inspecting `engine/events.py` L94-105, `CallbackEmitter.__init__` takes `callback: Callable[[EngineEvent], None]`. The developer-advocate then infers that `RichProgressHandler` must implement `__call__` because the CLI passes `progress_handler` as the callback. But this is a standard Python pattern: any object that is callable (whether via `__call__` or being a function) satisfies `Callable`. The developer-advocate presents this as an undocumented requirement that "developers building custom emitters need to understand."

In reality, the documented `CallbackEmitter` interface is explicit: it takes a callable. A developer building a custom emitter does not need to use `CallbackEmitter` at all -- they implement the `EventEmitter` protocol (L82-91), which requires a single `emit(self, event: EngineEvent) -> None` method. `CallbackEmitter` is one convenience implementation, not a requirement.

**Why this matters**: If the documentation follows developer-advocate's framing, it would teach `CallbackEmitter` internals instead of the `EventEmitter` protocol. The protocol is the intended extension point; `CallbackEmitter` is an implementation detail.

**Both reviews agree** the event system deserves better documentation. We disagree on what to document: developer-advocate focuses on `CallbackEmitter` plumbing; I would focus on the `EventEmitter` protocol as the public API for extension.

---

## Tensions

### 1. End-to-end domain tutorial: scope and accuracy risk

Developer-advocate's P1 Recommendation #1 proposes a complete 5-stage lifecycle example including specific constructor calls:

```python
DomainContext(workspace=Path("."), changed_files=["src/app.py"], metadata={"commit_message": "feat: add caching"})
```

I support the tutorial's existence (it is the highest-impact gap for the developer audience). The tension is that developer-advocate's proposed example has a type error: `DomainContext.changed_files` is typed as `list[Path]` at `base.py` L44, not `list[str]`. The proposed example passes strings. Pydantic v2 would coerce these, so it would not fail at runtime, but showing `list[str]` in documentation for a `list[Path]` field teaches the wrong type.

This is not a reason to reject the tutorial. It is a reason to have code-verifier review every example against source before shipping, which developer-advocate themselves propose at the end of the Round 1 synthesis's domain tutorial recommendation: "Have code-verifier review every code example against source before shipping."

**Resolution path**: Both reviews support the tutorial. I would add a specific accuracy checkpoint: every constructor call in the tutorial must match the source type annotations. The `changed_files` field should show `[Path("src/app.py")]`, not `["src/app.py"]`.

### 2. Plugin wiring steps: developer-advocate says "first Plugin subclass," source says any

Developer-advocate's P1 Recommendation #2 includes: "(c) The loader finds the first `Plugin` subclass in the module -- name your module accordingly."

This is accurate to `_find_plugin_class` at `plugins/base.py` L216-226, which iterates `dir(module)` and returns the first match. However, developer-advocate's instruction "name your module accordingly" implies the author should ensure only one Plugin subclass exists per module. The code does not enforce this -- it just picks the first one alphabetically (since `dir()` returns names in alphabetical order). A module with `APlugin` and `BPlugin` will always load `APlugin`.

My review does not address this because it is a code-level detail, not a documentation gap I flagged. But developer-advocate's proposed documentation text would create a new accuracy issue: `dir()` ordering is alphabetical, not declaration order. "Name your module accordingly" is vague advice that could lead to confusion.

**Resolution path**: The documentation should say: "The loader finds the first `Plugin` subclass in the module (by alphabetical attribute name). Define exactly one `Plugin` subclass per module to avoid ambiguity." This is more precise than either review proposed.

### 3. Import namespace explanation: scope creep risk

Developer-advocate's P2 Recommendation #7 proposes adding a note explaining `engine` vs. `conversus` as "separate Python packages in the same repo." This is accurate, but the recommendation then extends to cross-referencing architecture.md's package boundaries table and coordinating with the `classify` re-export code change.

My review (Missed Opportunity #6) confirms the `classify` export gap as a code issue. The tension is that developer-advocate couples a simple documentation note (explain the two namespaces) with a cross-cutting change (re-export + architecture cross-reference). If the documentation note ships independently of the code change, it could say "both packages are installed by `uv sync`" without the `classify` re-export, and the import example `from engine.sdk import classify` would remain correct.

**Resolution path**: Decouple the documentation note from the code change. Ship the namespace explanation first (it requires no code changes). Track the `classify` re-export separately. Developer-advocate's sequencing creates an unnecessary dependency that could delay the simpler fix.

### 4. Sync-first SDK example: developer-advocate's concession has a new condition

Developer-advocate's Off-Base #1 accepts the sync-first `asyncio.run()` Quick Start ordering but adds a new condition: "the immediately-following note must explicitly say 'Event subscriptions require async context -- see Event Subscription below.'"

My review accepted the synthesizer's resolution without adding conditions. Developer-advocate's new condition is reasonable (event subscriptions do require async context, per `AsyncQueueEmitter` at `events.py` L119-151), but it was not part of the Round 1 resolution. This is not a reversal -- it is a new requirement attached to a concession.

**Resolution path**: I accept the condition. The note is factually accurate and adds one line. No structural disagreement.

### 5. Three-way provider default mismatch framing

Developer-advocate does not address my Missed Opportunity #5 (the three-way default mismatch between config `"anthropic"`, CLI `"mock"`, and SDK `"mock"`). My review extends the converged CV-3 recommendation with specific documentation text for config-reference.md. Developer-advocate's review accepts CV-3 (provider precedence note) but frames it as resolved by the Round 1 convergence without engaging with the deeper mismatch.

The tension: developer-advocate's P1/P2 priorities focus entirely on the developer guide (domains, plugins, wiring). The config-reference provider default issue affects a broader audience -- any user who writes a config file and expects `provider: anthropic` to be respected by the CLI.

**Resolution path**: This is a priority tension, not a factual disagreement. Both reviews accept that the provider precedence note belongs in cli.md. My review adds that config-reference.md should also clarify the default behavior. These are not conflicting; they are additive.

---

## Safe Agreements

### 1. The building-domains guide demonstrates only 2 of 5 lifecycle stages

Both reviews identify this as a major gap. Developer-advocate's DA-1 (carried forward from Round 1, now P1 Recommendation #1) and my review's convergence on the `determine_verdict` split (CV-8) both point to the building-domains guide being incomplete. Developer-advocate frames it as the "single largest gap for the developer audience" and I agree.

The source confirms the gap: `DomainPlugin` at `base.py` L497-834 provides `extract()`, `score()`, and `create_record()` as a connected pipeline, but the documentation only shows extract and score concepts without demonstrating the actual method calls in sequence.

Both reviews agree on the fix: add a running example that calls `extract()`, `score()`, `create_record()`, and persists with `JSONLStore`. The only nuance is type accuracy in the examples (see Tension #1 above).

### 2. The `plugins:` key must be added to config-reference.md with schema documentation

Both reviews affirm the unanimous Round 1 convergence (CV-B / DA-3). Developer-advocate specifically calls out the `name`, `package`, `config` sub-keys with fallback behaviors, which matches the `load_plugins()` signature at `plugins/base.py` L229-295. My review confirms the same function as the authoritative source for the schema.

There is no disagreement on placement (Advanced/Extensibility subsection), content (three sub-keys with defaults), or priority (both reviews carry it forward as agreed).

### 3. The scaffolds endpoint YAML glob bug is a code fix, not a docs fix

Both reviews carry forward the Round 1 bilateral convergence (CV-2 / DA-A) without modification. The code at `api.py` L208 globs `*.json` only, while `load_scaffold()` at `base.py` L144-171 handles `.yml`, `.yaml`, and `.json`. Developer-advocate's Round 2 review reaffirms: "I accept this as code-fix-only." My review confirms: "No further discussion needed."

### 4. The `determine_verdict` documentation must split into default behavior and custom override

Both reviews carry forward the Round 1 bilateral convergence (CV-8 / DA-7). Developer-advocate's Convergence #2 confirms: "The base class default actually checks hard blocks first, then per-dimension thresholds." My review confirms the source at `base.py` L628-656: `determine_verdict()` calls `_determine_verdict()` which checks hard blocks, then per-dimension thresholds, and never checks `minimum_overall`.

The building-domains example teaching `minimum_overall` as default behavior would cause developers to unnecessarily override `determine_verdict` when they could simply adjust scaffold thresholds. Both reviews agree this is a documentation efficiency issue worth fixing.
