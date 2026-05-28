# Gotchas — a memo from one contributor to the next

> A hand-off memo of subtle bugs, tool behaviors that disagree with
> intuition, and constitutional constraints that bite mid-implementation.
> Primarily authored by AI coding agents for their future selves, but
> human contributors land here from the same nav and the content
> applies the same way.
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

## MCPB prompts must be declared in manifest.json AND registered in the MCP server

**Symptom**: Prompts appear in Claude Desktop's prompt picker. User
fills in the form and clicks "Add prompt". Error: "Failed to attach
prompt." The MCP server log shows: `Extension Conversus attempted
undeclared prompt: deliberate`.

**Cause**: Claude Desktop's extension security model validates prompts
against TWO sources: the MCP server's `prompts/list` response AND
the manifest.json `prompts` array. Both must agree. If the server
registers a prompt via `@mcp.prompt()` but the manifest doesn't
declare it in `prompts[]`, the client rejects it as "undeclared" —
even though `prompts/list` returned it successfully.

This mirrors how tools work: the manifest has `tools[]` that must
match what the server registers via `@mcp.tool()`.

**Fix**: Add a `prompts` array to manifest.json alongside `tools`:

```json
"prompts": [
  {
    "name": "deliberate",
    "description": "Run a cooperative deliberation",
    "arguments": ["question"]
  }
],
"tools": [...]
```

**How to avoid next time**: when adding a new `@mcp.prompt()` to the
server, also add the corresponding entry to `manifest.json`'s
`prompts[]` array. The prompt name, description, and argument names
must match between the two declarations.

---

## FastMCP `@mcp.prompt()` functions must return `list[dict]`, not `str`

**Symptom**: Claude Desktop shows the prompt dialog correctly (title,
description, input fields all render). The user fills in the question
and clicks "Add prompt". Error banner: "Failed to attach prompt. You
can try again." No further diagnostics.

**Cause**: FastMCP's `@mcp.prompt()` decorator expects the function to
return a `list[dict]` (or `list[Message]`) — each dict has `role` and
`content` keys matching the MCP `prompts/get` response format. Returning
a plain `str` causes FastMCP to fail silently when serializing the
response.

**Fix**: Return `[{"role": "user", "content": f"..."}]` not `f"..."`:

```python
# WRONG — returns str, fails silently
@mcp.prompt()
def deliberate(question: str) -> str:
    return f"Use conversus_decide on: {question}"

# CORRECT — returns list[dict], works
@mcp.prompt()
def deliberate(question: str) -> list[dict]:
    return [{"role": "user", "content":
        f"Use conversus_decide on: {question}"}]
```

**How to avoid next time**: always check FastMCP's `help(mcp.prompt)`
example — it shows `-> list[Message]` with dict-style message objects.
The `str` return type is tempting because it's simpler, but FastMCP
doesn't auto-wrap strings into messages for prompts (unlike tools
where the return value IS the tool output).

---

## `from __future__ import annotations` breaks Pydantic in bundled/deferred contexts

**Symptom**: All three MCP tools fail with `DecideResult is not fully
defined; you should define 'Any', then call DecideResult.model_rebuild()`
or `RunResult is not fully defined; you should define 'CostEstimate'`.
The error happens at tool INVOCATION time, not at import time. Tools
load and register fine; they crash when called.

**Cause**: `from __future__ import annotations` (PEP 563) turns all
type annotations into strings. Pydantic v2 must then lazily resolve
those strings back to real types. When the module runs in a standard
Python process (CLI, pytest), the module namespace has all symbols
and resolution works. But in bundled contexts (`.mcpb` extension,
claude.ai's deferred tool loading via `tool_search`), the module may
be imported in a namespace where the resolution fails — `typing.Any`
becomes the string `"Any"` which Pydantic can't find.

**Fix**: Remove `from __future__ import annotations` from files that
define Pydantic models used as MCP tool return types. Specifically:
`engine/results.py` and `mcp_server.py`. These files don't need
PEP 563 — all types are concrete and already imported by the time
they're annotated.

**How to avoid next time**: Never use `from __future__ import
annotations` in a file that defines Pydantic `BaseModel` subclasses
used by FastMCP's `@mcp.tool()` return type annotations. The eager
evaluation (no `__future__`) means Pydantic resolves types at class
definition time, which is always safe regardless of import context.

---

## MCPB `user_config` fields require `title` — not just `type` + `description`

**Symptom**: Claude Desktop shows "Failed to preview extension: Invalid
manifest: user_config: Required, Required, Required" when you try to
install a `.mcpb` bundle. The error says "Required" once per
`user_config` field but doesn't name WHICH property is missing.

**Cause**: The MCPB v0.3 `user_config` schema requires a `title` field
on every option — the human-readable label that Claude Desktop renders
in its extension settings UI. If you only provide `type` +
`description` (which is what most JSON schema conventions suggest),
the manifest validation fails.

**Fix**: Add `"title": "Human Label"` to every `user_config` entry:

```json
"user_config": {
  "ANTHROPIC_API_KEY": {
    "type": "string",
    "title": "Anthropic API Key",
    "description": "Get one at console.anthropic.com.",
    "sensitive": true
  }
}
```

**Also**: set `"sensitive": true` on API key fields. Claude Desktop
stores sensitive values in the OS keychain (macOS Keychain, Windows
Credential Manager) instead of plaintext. It's free security — one
boolean flag and the user's API key never touches disk unencrypted.

**How to avoid next time**: when writing `user_config` for a `.mcpb`
manifest, always include all four core fields: `type`, `title`,
`description`, and either `default` or `sensitive`. Check the schema
at https://github.com/modelcontextprotocol/mcpb/blob/main/MANIFEST.md
before shipping.

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
