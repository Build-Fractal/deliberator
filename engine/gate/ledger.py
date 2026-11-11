"""The decision log: every gate decision and what happened after it, append-only.

`.deliberator/gate/log.jsonl` is the record (one JSON object per line). The graph is folded
from it (`engine.gate.graph`), so the log can rebuild the graph at any time.

Two kinds of line:

- ``decision``: a tool call the gate ruled on, with verdict, reason, the rule it cited, the
  earlier decisions it was shown as precedent, and how it was reached (model, reuse, skip,
  error).
- ``outcome``: written by the PostToolUse hook when the tool actually ran. A decision of
  ``ask`` followed by an outcome means the person approved it; that approval is precedent.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Verdict = Literal["allow", "deny", "ask"]
Source = Literal["model", "reuse", "approved", "skip", "error"]

LOG_PATH = Path(".deliberator") / "gate" / "log.jsonl"


# Redirection, pipes, chaining, substitution: a command with any of these does more than its
# first word says, so allow-lists and grants don't cover it unless the approved call had it.
_COMPOUND = re.compile(r"[<>;&|`\n]|\$\(")


def compound(subject: str) -> bool:
    return bool(_COMPOUND.search(subject))


def subject_of(tool: str, tool_input: dict[str, Any]) -> str:
    """The part of a tool call that decides whether it's safe, as one string."""
    if tool == "Bash":
        return str(tool_input.get("command", "")).strip()
    for key in ("file_path", "notebook_path", "path", "url"):
        if key in tool_input:
            return f"{tool_input[key]}"
    return json.dumps(tool_input, sort_keys=True, ensure_ascii=False)[:2000]


def call_key(tool: str, subject: str, cwd: str, rules_hash: str) -> str:
    """Identity of a call for reuse: same tool, same input, same folder, same rules."""
    raw = f"{tool}\0{subject}\0{cwd}\0{rules_hash}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


class Decision(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: Literal["decision"] = "decision"
    id: str
    at: str
    session: str | None = None
    tool_use_id: str | None = None
    tool: str
    subject: str
    cwd: str
    key: str
    verdict: Verdict
    reason: str
    rule: int | None = None  # 1-based index into the config's rules
    rules_hash: str
    source: Source
    model: str | None = None
    precedents: tuple[str, ...] = ()
    latency_ms: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    # On an ask: the pattern of calls the person's yes covers. Approved, it stands forever
    # (until revoked with `deliberator gate revoke`).
    grant: str | None = None


class Revoke(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: Literal["revoke"] = "revoke"
    decision: str
    at: str


class Outcome(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: Literal["outcome"] = "outcome"
    decision: str
    at: str
    ran: bool = True


class History(BaseModel):
    """The log read back: decisions in order, and which ones were followed by the tool running."""

    decisions: list[Decision] = Field(default_factory=list)
    ran: set[str] = Field(default_factory=set)
    revoked: set[str] = Field(default_factory=set)

    def approved(self, d: Decision) -> bool:
        """The gate asked and the person said yes (the tool ran)."""
        return d.verdict == "ask" and d.id in self.ran and d.id not in self.revoked

    def effective(self, d: Decision) -> Verdict:
        """What the decision came to: an approved ask counts as allow."""
        return "allow" if self.approved(d) else d.verdict

    def grants(self) -> list[Decision]:
        """Approved asks that carry a grant pattern and were not revoked, newest first."""
        return [d for d in reversed(self.decisions)
                if d.grant and self.approved(d) and d.id not in self.revoked]

    def granted(self, tool: str, subject: str) -> Decision | None:
        for d in self.grants():
            if d.tool != tool or (compound(subject) and not compound(d.subject)):
                continue
            try:
                if re.search(d.grant or "", subject):
                    return d
            except re.error:
                continue
        return None


def now() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def new_id(key: str) -> str:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
    return f"{stamp}-{key[:8]}"


def append(root: Path, *items: Decision | Outcome | Revoke) -> None:
    path = root / LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for item in items:
            fh.write(item.model_dump_json() + "\n")


def read(root: Path) -> History:
    path = root / LOG_PATH
    history = History()
    if not path.is_file():
        return history
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue  # a torn write: skip it, never fail the hook over the log
        if data.get("kind") == "decision":
            history.decisions.append(Decision.model_validate(data))
        elif data.get("kind") == "outcome" and data.get("ran", True):
            history.ran.add(str(data["decision"]))
        elif data.get("kind") == "revoke":
            history.revoked.add(str(data["decision"]))
    return history


def find_pending(history: History, *, tool_use_id: str | None, session: str | None,
                 tool: str, subject: str) -> Decision | None:
    """The decision a PostToolUse event belongs to: by tool_use_id, else the latest match."""
    for d in reversed(history.decisions):
        if tool_use_id and d.tool_use_id == tool_use_id:
            return d
    for d in reversed(history.decisions):
        if d.session == session and d.tool == tool and d.subject == subject:
            return d
    return None


# ---------------------------------------------------------------------------
# Precedent search
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[a-z][a-z0-9_]{1,}")


def _stems(text: str) -> frozenset[str]:
    return frozenset(w[:6] for w in _WORD.findall(text.lower()))


def similar(history: History, *, tool: str, subject: str, cwd: str, k: int,
            exclude: Iterable[str] = ()) -> list[Decision]:
    """The `k` earlier decisions most like this call (same tool first, then word overlap,
    same folder, and decisions the person confirmed weigh more)."""
    skip = set(exclude)
    words = _stems(subject)
    scored: list[tuple[float, int, Decision]] = []
    seen_keys: set[str] = set()
    for i, d in enumerate(history.decisions):
        if d.id in skip or d.source in ("error", "skip"):
            continue
        dw = _stems(d.subject)
        overlap = len(words & dw) / len(words | dw) if words and dw else 0.0
        if overlap == 0.0 and d.subject != subject:
            continue
        score = overlap + (0.3 if d.tool == tool else 0.0) + (0.1 if d.cwd == cwd else 0.0)
        score += 0.2 if history.approved(d) else 0.0
        scored.append((score, i, d))
    out = []
    for _, _, d in sorted(scored, key=lambda t: (-t[0], -t[1])):
        if d.key in seen_keys:
            continue  # one line per distinct call
        seen_keys.add(d.key)
        out.append(d)
        if len(out) >= k:
            break
    return out


def latest_for_key(history: History, key: str) -> Iterator[Decision]:
    """Decisions for exactly this call, newest first."""
    return (d for d in reversed(history.decisions) if d.key == key)
