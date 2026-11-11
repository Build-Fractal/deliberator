"""Parse an agent's JSON reply for one phase, leniently, never raising.

Agents are asked for one JSON object. Replies often arrive fenced or with a sentence around them,
so the first ``{`` to the last ``}`` is tried. A reply that still doesn't fit is returned as
``None``; the caller logs it as an ``unparsed`` move with the raw text (Principle V: malformed
output beats no output), so nothing is lost and the run reports the share.
"""

from __future__ import annotations

import json
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from engine.review.protocol import Severity

_LENIENT = ConfigDict(extra="ignore", str_strip_whitespace=True)

# Agent-local item ids (F1, O3) and references to another agent's item ("bob/F2").
_LOCAL_ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,15}")
_REF = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}/[A-Za-z][A-Za-z0-9_-]{0,15}")


class FindingOut(BaseModel):
    model_config = _LENIENT

    id: str
    sev: Severity
    claim: str = Field(min_length=1)
    at: str | None = None
    fix: str | None = None

    @field_validator("sev", mode="before")
    @classmethod
    def _sev(cls, v: object) -> object:
        aliases = {"blocker": "block", "blocking": "block", "high": "block", "critical": "block",
                   "medium": "major", "substantive": "major", "low": "minor", "nit": "minor"}
        return aliases.get(str(v).lower(), str(v).lower()) if isinstance(v, str) else v


class ReviewOut(BaseModel):
    model_config = _LENIENT

    findings: list[FindingOut] = Field(default_factory=list)


class ObjectionOut(BaseModel):
    model_config = _LENIENT

    to: str
    why: str = Field(min_length=1)
    at: str | None = None


class ChallengeOut(BaseModel):
    model_config = _LENIENT

    objections: list[ObjectionOut] = Field(default_factory=list)
    agree: list[str] = Field(default_factory=list)
    # Another reviewer's finding -> your own finding id that says the same thing.
    same: dict[str, str] = Field(default_factory=dict)


class ReplyOut(BaseModel):
    model_config = _LENIENT

    to: str
    act: Literal["withdraw", "defend", "revise"]
    why: str = Field(min_length=1)
    claim: str | None = None

    @field_validator("act", mode="before")
    @classmethod
    def _act(cls, v: object) -> object:
        aliases = {"concede": "withdraw", "withdrawn": "withdraw", "rebut": "defend",
                   "modify": "revise", "revised": "revise"}
        return aliases.get(str(v).lower(), str(v).lower()) if isinstance(v, str) else v


class RespondOut(BaseModel):
    model_config = _LENIENT

    replies: list[ReplyOut] = Field(default_factory=list)


class RulingOut(BaseModel):
    model_config = _LENIENT

    finding: str
    uphold: bool
    why: str = Field(min_length=1)


class ArbitrateOut(BaseModel):
    model_config = _LENIENT

    rulings: list[RulingOut] = Field(default_factory=list)


def extract_json(text: str) -> object | None:
    """The JSON object in a reply, or None."""
    if not text:
        return None
    candidates = [text.strip()]
    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        candidates.append(text[start : end + 1])
    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def parse_reply[T: BaseModel](text: str, model: type[T]) -> T | None:
    """The reply as `model`, or None when it isn't one. Never raises."""
    value = extract_json(text)
    if value is None:
        return None
    try:
        return model.model_validate(value)
    except ValidationError:
        return None


def clip(text: str | None, words: int) -> str | None:
    """Text cut to `words` words (an over-long reply is truncated, not refused)."""
    if text is None:
        return None
    parts = text.split()
    return text if len(parts) <= words else " ".join(parts[:words]) + " …"


def valid_local_id(value: str) -> bool:
    return _LOCAL_ID.fullmatch(value) is not None


def valid_ref(value: str) -> bool:
    return _REF.fullmatch(value) is not None
