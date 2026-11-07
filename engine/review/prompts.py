"""Terse prompts for the structured review protocol.

Token rules, in order of how much they save:

1. Every call starts with the same prefix (instructions + target), so providers that cache
   prompt prefixes (Anthropic, OpenAI, the Claude Code CLI) pay for the target once per run.
2. Later phases never see earlier replies in full. They get one line per item, and only the
   items they act on: other reviewers' findings when challenging, objections to your own
   findings when responding, contested threads when arbitrating.
3. Replies are one JSON object with short text fields (``text_words`` words), no prose.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

STYLE = (
    "Terse: fragments fine. No preamble, no markdown, no restating the target. "
    "At most {words} words per text field. Reply with ONE JSON object and nothing else."
)


def _number(text: str) -> str:
    return "\n".join(f"{i}|{line}" for i, line in enumerate(text.splitlines(), start=1))


def prefix(targets: Sequence[tuple[str, str]], words: int, *, number_lines: bool = True) -> str:
    """The shared prefix: identical for every call in a run, so it can be cached."""
    blocks = []
    for name, text in targets:
        body = _number(text) if number_lines else text
        blocks.append(f"=== TARGET {name} ===\n{body}\n=== END {name} ===")
    return (
        "You take part in a structured review of the TARGET below. "
        + STYLE.format(words=words)
        + (" Lines are numbered N|; cite as name:N." if number_lines else "")
        + "\n\n"
        + "\n\n".join(blocks)
        + "\n\n"
    )


def _one_line(*fields: str | None) -> str:
    return "|".join((f or "-").replace("\n", " ").replace("|", "/") for f in fields)


def review(name: str, lens: str, max_items: int) -> str:
    return (
        f'ROLE: reviewer "{name}". FOCUS: {lens}\n'
        f"TASK: list real problems only, at most {max_items}; none means an empty list. "
        "sev: block (must fix before use) | major (should fix) | minor. "
        '"at": name:line or a short quote. "fix": the smallest change that fixes it.\n'
        'JSON: {"findings":[{"id":"F1","sev":"major","claim":"...","at":"...","fix":"..."}]}'
    )


def challenge(
    name: str, lens: str, others: Iterable[tuple[str, str, str, str | None]], max_items: int
) -> str:
    """`others`: (ref, sev, claim, at) for each other reviewer's finding."""
    lines = "\n".join(_one_line(ref, sev, claim, at) for ref, sev, claim, at in others)
    return (
        f'ROLE: reviewer "{name}". FOCUS: {lens}\n'
        f"OTHER REVIEWERS' FINDINGS (ref|sev|claim|at):\n{lines}\n"
        f"TASK: object only to findings that are wrong, overstated or unsupported, at most "
        f'{max_items}; cite evidence in "at". Put refs you independently agree with in "agree". '
        "Leave out anything you have no view on.\n"
        'JSON: {"objections":[{"to":"bob/F1","why":"...","at":"..."}],"agree":["bob/F2"]}'
    )


def respond(
    name: str,
    threads: Iterable[tuple[str, str, str, Iterable[tuple[str, str, str | None]]]],
) -> str:
    """`threads`: (local id, sev, claim, [(objection ref, why, at)]) for each finding objected to."""
    parts = []
    for local, sev, claim, objections in threads:
        parts.append(_one_line(local, sev, claim))
        parts.extend("  " + _one_line(ref, why, at) for ref, why, at in objections)
    body = "\n".join(parts)
    return (
        f'ROLE: reviewer "{name}".\n'
        f"YOUR FINDINGS UNDER OBJECTION (id|sev|claim, then objection ref|why|at):\n{body}\n"
        "TASK: answer each objection: withdraw (it is right), defend (it is wrong: say why, cite), "
        'or revise (give the corrected claim in "claim").\n'
        'JSON: {"replies":[{"to":"carol/O1","act":"defend","why":"...","claim":null}]}'
    )


def arbitrate(
    threads: Iterable[tuple[str, str, str, str | None, Iterable[tuple[str, str, str | None]]]],
) -> str:
    """`threads`: (ref, sev, claim, at, [(who, why, at)]) for each contested finding."""
    parts = []
    for ref, sev, claim, at, exchanges in threads:
        parts.append(_one_line(ref, sev, claim, at))
        parts.extend("  " + _one_line(who, why, w_at) for who, why, w_at in exchanges)
    body = "\n".join(parts)
    return (
        "ROLE: arbiter. Decide each contested finding on the evidence in the TARGET.\n"
        f"CONTESTED (ref|sev|claim|at, then each exchange who|why|at):\n{body}\n"
        "TASK: for each finding, uphold (the finding stands) or not.\n"
        'JSON: {"rulings":[{"finding":"alice/F2","uphold":true,"why":"..."}]}'
    )
