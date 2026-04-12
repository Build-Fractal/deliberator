"""DefaultCLIAdapter — projects a Capability to Click command source code.

The adapter emits a single Click command block ready to be concatenated
into ``engine/cli/__init__.py`` by the projector. It is pure string-template
based; no AST manipulation, no imports of ``click`` at render time, and no
dependency on the handler being importable.

Shape of the generated output for a capability named ``hello`` with one
required string ``who`` and an optional ``--loud`` bool::

    @cli.command("hello", help="Say hello")
    @click.argument("who", type=str)
    @click.option(
        "--loud",
        type=bool,
        default=False,
        help="Shout instead of whispering.",
    )
    def hello(who: str, loud: bool = False) -> None:
        \"\"\"Say hello\"\"\"
        from conversus.demo import say_hello
        return say_hello(who=who, loud=loud)

The projector wraps the concatenated blocks with a file preamble
(``from __future__``, click import, ``@click.group``) so this adapter
does not emit any module-level scaffolding.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from conversus.registry.adapters._helpers import literal, split_handler
from conversus.registry.adapters.base import CLIAdapter
from conversus.registry.params import Surface

if TYPE_CHECKING:
    from conversus.registry.capability import Capability
    from conversus.registry.params import Param


class DefaultCLIAdapter(CLIAdapter):
    """Projects a capability to a Click command source fragment."""

    def render(self, capability: "Capability") -> str:
        params = capability.params_for(Surface.CLI)
        lines: list[str] = []
        lines.append(self._command_decorator(capability))
        for param in params:
            lines.append(self._param_decorator(param))
        lines.append(self._function_signature(capability, params))
        lines.append(f'    """{capability.summary}"""')
        lines.extend(self._handler_call(capability, params))
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Decorator emission
    # ------------------------------------------------------------------

    def _command_decorator(self, cap: "Capability") -> str:
        return f'@cli.command({literal(cap.name)}, help={literal(cap.summary)})'

    def _param_decorator(self, param: "Param") -> str:
        if param.required:
            return f'@click.argument({literal(param.name)}, type={_type_expr(param)})'

        flag = "--" + param.name.replace("_", "-")
        option_args: list[str] = [f"    {literal(flag)}"]

        # If hyphenation changed the name, rebind it to the Python identifier.
        if flag[2:] != param.name:
            option_args.append(f"    {literal(param.name)}")

        option_args.append(f"    type={_type_expr(param)}")
        option_args.append(f"    default={literal(param.default)}")

        if param.help:
            option_args.append(f"    help={literal(param.help)}")

        return "@click.option(\n" + ",\n".join(option_args) + ",\n)"

    # ------------------------------------------------------------------
    # Function body
    # ------------------------------------------------------------------

    def _function_signature(self, cap: "Capability", params: list["Param"]) -> str:
        sig_params = ", ".join(_sig_param(p) for p in params)
        # Python identifier form of the capability name (kebab → snake)
        py_name = cap.name.replace("-", "_")
        return f"def {py_name}({sig_params}) -> None:"

    def _handler_call(self, cap: "Capability", params: list["Param"]) -> list[str]:
        module, func = split_handler(cap.handler_for(Surface.CLI))
        kwargs = ", ".join(f"{p.name}={p.name}" for p in params)
        return [
            f"    from {module} import {func}",
            f"    return {func}({kwargs})",
        ]


# ---------------------------------------------------------------------------
# CLI-specific template helpers (signature rendering, Click type expr)
# ---------------------------------------------------------------------------


def _type_expr(param: "Param") -> str:
    """Emit the Click ``type=`` argument for a param.

    - ``choices`` → ``click.Choice([...], case_sensitive=False)``
    - everything else → the bare Python type name (``str``, ``int``, etc.)
    """
    if param.choices is not None:
        choices_src = ", ".join(literal(c) for c in param.choices)
        return f"click.Choice([{choices_src}], case_sensitive=False)"
    return param.type.__name__


def _sig_param(param: "Param") -> str:
    """Render one parameter for the ``def`` signature."""
    type_name = param.type.__name__
    if param.required:
        return f"{param.name}: {type_name}"
    return f"{param.name}: {type_name} = {literal(param.default)}"
