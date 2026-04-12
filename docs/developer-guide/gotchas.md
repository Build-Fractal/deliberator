# Gotchas — a memo from one AI agent to the next

> **This file is not part of the published documentation.** It is a
> hand-off memo from AI coding agents to their future selves and to
> other agents working on this codebase. Human developers are welcome
> to read it, but the audience is AI.
>
> **When to add to this file**: any time you hit a subtle bug, a tool
> behavior that disagreed with your mental model, or a constitutional
> constraint that bit you mid-implementation. Keep entries short and
> structured — symptom, cause, fix, and (where relevant) how to avoid
> hitting it next time.
>
> **When to read it**: before starting any non-trivial work on the
> capability registry, the projector, or generated surface files
> (`engine/cli/__init__.py`, `mcp_server.py`, `claude-code-plugin/`,
> `desktop-extension/manifest.json`). Also before writing tests that
> validate generated Python source code.

---

## `json.dumps(False)` emits lowercase `false` — breaks generated Python source

**Symptom**: The capability projector generates code like
`@click.option(..., default=false, ...)` or
`def conversus_hello(..., loud: bool = false)`. The generated code
parses cleanly with `ast.parse()` — no syntax error — but fails at
decorator evaluation or function call time with a `NameError: name
'false' is not defined`.

**Cause**: JSON literals are not the same as Python literals for three
types: `False` → `"false"`, `True` → `"true"`, `None` → `"null"`. Using
`json.dumps()` as a universal "emit this value as source" helper is
tempting because it handles strings correctly (with double quotes,
which the hand-written surface files prefer), but it silently breaks on
those three types.

**Fix**: `conversus/registry/adapters/_helpers.py::literal()` has type-
specific branches — `None` → `"None"`, `bool` → `"True"`/`"False"`
(before the int check, because `bool` is a subclass of `int`), and only
strings fall through to `json.dumps`. Do not revert to a single-line
`json.dumps` implementation.

**How to avoid next time**: never trust `json.dumps` as a source-code
emitter. When generating Python source literals, reach for a dedicated
helper that special-cases the three problem types, or use `repr()` with
an understanding of its quoting rules.

---

## `ast.parse()` is weaker than `exec()` for validating generated code

**Symptom**: A test asserts that generated source is "valid" by calling
`ast.parse(source)`. The parse succeeds. Later, running the generated
code raises `NameError`, `TypeError`, or similar at runtime — but the
test was green.

**Cause**: Python's AST parser accepts undefined identifiers as `Name`
nodes. It does not resolve references, check types, or run decorators.
So `default=false` parses as "identifier `false` passed as keyword arg"
— syntactically valid, semantically broken at the first invocation.

**Fix**: use `exec(compile(source, "<generated>", "exec"), ns)` in a
sandboxed namespace. This runs decorators at def time, so any undefined
identifier inside a decorator argument list raises immediately. For MCP
tests, stub out `mcp.server.fastmcp.FastMCP` via `sys.modules`
injection before the `exec()` call — see `test_projector.py`'s
`_exec_mcp_source()` for the pattern.

**How to avoid next time**: `ast.parse` tests pass for code that will
break at runtime. Never use it as the primary validation for generated
source. The cost of using `exec()` instead is one import and a
`sys.modules` dance for modules you don't want to actually load.

---

## Pydantic v2 `model_rebuild()` for forward-ref adapter slots

**Symptom**: `Capability(name="decide", ...)` raises
`pydantic.errors.PydanticUserError: Capability is not fully defined;
you should define CLIAdapter, then call Capability.model_rebuild()`.
The field annotations use forward-reference strings like
`"CLIAdapter | None"` because the adapter ABCs are imported under
`TYPE_CHECKING` to avoid circular imports.

**Cause**: Pydantic v2 resolves forward references lazily, but it
cannot resolve a string annotation that names a class it has never
actually imported. `TYPE_CHECKING` imports exist only for static type
checkers — at runtime, the symbols don't exist in the model's
namespace. So Pydantic has no way to turn `"CLIAdapter"` into an
actual class.

**Fix**: in the package `__init__.py`, after both `Capability` and all
four adapter ABCs have been imported, call:

```python
Capability.model_rebuild(
    _types_namespace={
        "CLIAdapter": CLIAdapter,
        "MCPAdapter": MCPAdapter,
        "PluginAdapter": PluginAdapter,
        "MCPBAdapter": MCPBAdapter,
    }
)
```

Passing `_types_namespace` explicitly beats relying on Pydantic's
frame-inspection fallback, which doesn't reliably find the symbols
when `model_rebuild()` is called from a different module than the one
that defines the adapters.

**How to avoid next time**: any Pydantic model with `TYPE_CHECKING`
forward-ref fields needs `model_rebuild()` called once after its
dependencies are loaded. The right place is the package `__init__.py`,
not the model's own module, because by the time the `__init__.py` runs
both the model and its dependencies have been imported.

---

## The decorator-registry pattern violates CONSTITUTION.md principle IX

**Symptom**: You reach for an idiomatic Python pattern — a
`@capability(...)` class decorator that appends to a module-level
`REGISTRY: list[Capability] = []` — because it's how Click, pytest,
FastAPI, and a thousand other frameworks work. Halfway through
implementation you discover the constitution explicitly forbids
"module-level mutable state" and "set_backend() patterns".

**Cause**: The idiomatic Python registry pattern is the textbook
violation of constitution principle IX ("No mutable global state.
Configuration is loaded once and passed explicitly."). The principle
was written to prevent test-isolation races and hidden reconfiguration,
and a once-at-import-time registry does not actually suffer those
failure modes — but the rule is literal, not interpretive.

**Fix**: `capabilities.py` at the repo root exports an explicit
`CAPABILITIES: list[Capability] = [...]` list. Capability instances are
constructed directly via the Pydantic constructor — no decorator, no
side effects at import time. The projector and the build script take
the list as an explicit parameter. See `conversus/registry/__init__.py`
and `scripts/build-surfaces.py` for the pattern.

**How to avoid next time**: when designing any new "registry" or
"plugin system" component in conversus-oss, start from the explicit-
list model. Reach for decorators only as pure constructors (returning
a value without side effects) — never as side-effect-producing
class transformers.

---

## `monkeypatch.setattr("old_module.name", ...)` silently no-ops after a function move

**Symptom**: A test that previously passed now fails with unexpected
errors downstream of a monkeypatched function. The patch doesn't seem
to be taking effect — the original function is still being called.

**Cause**: Python looks up bare name references inside a function's
body in the function's *defining module* namespace, not the namespace
of whatever module imported and called it. When you move a function
from ``old_module`` to ``new_module``, every bare reference inside
that function (``resolve_provider``, ``parse_config``, ``classify_question``)
now resolves through ``new_module``. Any test that patches
``monkeypatch.setattr("old_module.symbol", fake)`` becomes a no-op
because the function no longer reads from ``old_module``.

This is especially tricky when the function is re-exported from the
old module as an alias (e.g.
``from new_module import some_func as _some_func`` at the bottom of
``old_module``). The ``from old_module import some_func`` import still
resolves to the same function object, but the internal name lookups
still happen in ``new_module``.

**Fix**: update the monkeypatch target to point at the new defining
module. In practice: grep test files for
``monkeypatch.setattr("<moved_module>.`` and update each call site.

**How to avoid next time**: when planning a function move across
modules, also search for ``monkeypatch.setattr("<old_module>.`` in
the test suite. Any hit is a call site that needs updating alongside
the move. The symptom-to-cause distance is long (the test error is
often in a downstream assertion, not in the patch call), so catching
it at refactor time is far cheaper than debugging it later.

---

## `CostEstimate` / `DecideResult` duplication across modules (principle XI)

**Symptom**: You have a result type used in two places (e.g.
`CostEstimate` defined in `mcp_server.py` and needed in
`engine/handlers.py`). The temptation is to duplicate it "just for
this migration" and collapse the duplication later.

**Cause**: Constitution principle XI ("Single Source of Truth") is
unambiguous: *"If you find yourself writing the same fact in two
places, stop. One of them is wrong, or will be soon."* Temporary
duplication is still duplication under the principle — and once
duplicated, it tends to stay that way.

**Fix**: move the shared types into a neutral module
(`engine/results.py` is the natural location) and have every consumer
import from there. `mcp_server.py` can re-export the names for
backward compatibility with existing test imports, but the canonical
definition lives in the shared module.

**How to avoid next time**: before copy-pasting any type definition,
identify the neutral module that should own it. If no neutral module
exists, create one. The 10-minute refactor to extract a shared module
is always cheaper than the eventual divergence bug.
