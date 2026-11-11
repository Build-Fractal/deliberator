"""Mask secret values before anything is stored or sent: ``redact(text) -> str``.

The secret value becomes ``[REDACTED]``; the rest of the text (the command, the flag, the
variable name) stays readable, so a redacted command still says what it does. Hashes for
reuse are taken over the unredacted text (a hash leaks nothing).
"""

from __future__ import annotations

import re
from typing import Any

MASK = "[REDACTED]"

_NAME = (
    r"(?:[A-Za-z0-9_.-]*?(?:password|passwd|secret|token(?!s|iz)|api[_-]?key|access[_-]?key"
    r"|private[_-]?key|credentials?)[A-Za-z0-9_.-]*"
    r"|(?:[A-Za-z0-9_.-]*[_.-])?auth(?:[_.-][A-Za-z0-9_.-]*)?)"
)
# Commands whose `-p` takes a password (`mkdir -p` and friends do not).
_P_IS_PASSWORD = re.compile(
    r"(?i)\b(?:mysql|mysqldump|mariadb|mysqladmin|sshpass|redis-cli|mongo|mongosh)\b")
_DASH_P = re.compile(r"(?<![\w-])(-p\s*)(?!-)(\"[^\"]*\"|'[^']*'|[^\s\"']+)")



def _keep_quotes(m: re.Match[str]) -> str:
    """name + masked value, keeping the value's quotes (so masking twice changes nothing)."""
    value = m.group(2)
    if value.strip("\"'") == MASK:
        return m.group(0)
    q = value[0] if value[:1] in ("'", '"') and value[-1:] == value[:1] else ""
    return f"{m.group(1)}{q}{MASK}{q}"


_PATTERNS: tuple[tuple[re.Pattern[str], Any], ...] = (
    # PEM private keys: the whole block.
    (re.compile(r"-----BEGIN[A-Z0-9 ]*PRIVATE KEY-----[\s\S]*?"
                r"(?:-----END[A-Z0-9 ]*PRIVATE KEY-----|\Z)"),
     f"-----BEGIN PRIVATE KEY-----{MASK}-----END PRIVATE KEY-----"),
    # Authorization headers.
    (re.compile(r"(?i)(\b(?:authorization|proxy-authorization)\s*[:=]\s*[\"']?\s*"
                r"(?:bearer|basic|token|digest)\s+)[^\s\"']+"),
     rf"\1{MASK}"),
    (re.compile(r"(?i)(\bbearer\s+)([A-Za-z0-9._~+/=-]{8,})"), rf"\1{MASK}"),
    # URLs with user:pass@.
    (re.compile(r"(?i)\b([a-z][a-z0-9+.-]*://[^\s:/@\"']+:)[^\s@/\"']+(@)"), rf"\1{MASK}\2"),
    # Well-known token shapes.
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), MASK),
    (re.compile(r"\b(?:ghp|gho|ghs|ghu|ghr)_[A-Za-z0-9]{20,}\b"), MASK),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), MASK),
    (re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{16,}"), MASK),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), MASK),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}"), MASK),
    # --password x, --token=x, -p x (mysql style -pSECRET too).
    (re.compile(rf"(?i)(--{_NAME}(?:\s+|=))(?!-)(\"[^\"]*\"|'[^']*'|[^\s\"']+)"), _keep_quotes),
    # name=value, name: value, "name": "value" (env vars, config files, JSON, aws config).
    (re.compile(rf"(?i)([\"']?\b{_NAME}[\"']?\s*[:=]\s*)"
                r"(\"[^\"\n]*\"|'[^'\n]*'|[^\s\"',;&|)}]+)"),
     _keep_quotes),
)

def redact(text: str) -> str:
    """`text` with secret values replaced by ``[REDACTED]``."""
    if not text:
        return text
    out = text
    for rx, repl in _PATTERNS:
        out = rx.sub(repl, out)
    if _P_IS_PASSWORD.search(out):
        out = "\n".join(_DASH_P.sub(rf"\1{MASK}", line) if _P_IS_PASSWORD.search(line)
                        else line for line in out.split("\n"))
    # A value already masked by an earlier pattern, then wrapped again: tidy doubles.
    return out.replace(f"{MASK}{MASK}", MASK)


def has_secret(text: str) -> bool:
    return redact(text) != text
