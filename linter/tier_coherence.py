"""Tier-coherence linter — Constitutional Inclusion Criterion 1 enforcement for v4.0.0.

Implements the four checks specified in spec v4.0.0-tier-extraction §6.8:
- Check (a): cross-tier duplication detection (dual-signal: identity-marker + 5-gram Jaccard).
- Check (b): post-relocation orphan detection.
- Check (c): cross-reference resolution validation.
- Check (d): version-field consistency.

Plus the cross-tier weakening prohibition flagged-words check (spec §6.10):
- Check (e): flag suspicious "weakening" terms near upper-tier principle names.

Run from conversus-oss directory:
    uv run python -m linter.tier_coherence

Exit codes:
    0 = all checks pass.
    1 = at least one check failed; specific failures named on stderr.
    2 = configuration error (missing files, etc.).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "CONSTITUTION.md"


def _find_build_fractal_root(start: Path) -> Path | None:
    """Walk up looking for a directory named 'build-fractal/' containing CONSTITUTION.md.

    Supports any monorepo layout that places conversus-oss anywhere under the
    monorepo root, including the post-Phase-C nested layout
    (build-fractal/conversus/conversus-oss/) and the original flat layout
    (conversus-oss/).
    """
    for ancestor in [start, *start.parents]:
        candidate = ancestor / "build-fractal" / "CONSTITUTION.md"
        if candidate.is_file():
            return ancestor / "build-fractal"
    return None


_BUILD_FRACTAL = _find_build_fractal_root(ROOT)
TIER1 = (_BUILD_FRACTAL / "CONSTITUTION.md") if _BUILD_FRACTAL else ROOT.parent / "build-fractal" / "CONSTITUTION.md"
TIER2 = (_BUILD_FRACTAL / "conversus" / "CONSTITUTION.md") if _BUILD_FRACTAL else ROOT.parent / "build-fractal" / "conversus" / "CONSTITUTION.md"

TIER1_PRINCIPLES = {"I", "II", "III", "IV", "VII", "VIII", "IX", "XI", "XIV", "XXVIII"}
TIER2_PRINCIPLES = {"V", "XII", "XIII", "XV", "XVI", "XXII", "XXIII", "XXIV", "XXV", "XXVII"}
COMPONENT_PRINCIPLES = {"XVII", "XVIII", "XIX", "XX", "XXI", "XXVI"}

EXCLUSION_PREFIXES = (
    "Origin: ",
    "**Extension (v",
    "see § Governance",
    "per CONSTITUTION.md",
    "### ",  # tombstone markers handled separately
)

WEAKENING_WORDS = {"relief", "exception", "adaptation", "exemption", "carve-out", "bypass"}
WEAKENING_TARGETS = {"Universal", "Tier 1"} | {f"Principle {r}" for r in TIER1_PRINCIPLES}


def parse_principle_blocks(text: str) -> dict[str, str]:
    """Return dict of {roman: normalized_body_text} for every `### {Roman}.` header."""
    lines = text.split("\n")
    header_re = re.compile(r"^### ([IVX]+)\. ")
    blocks: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        m = header_re.match(line)
        if m:
            current = m.group(1)
            blocks[current] = [line]
            continue
        if current is None:
            continue
        # Stop accumulating into a principle when a higher-level heading appears
        if line.startswith("## ") or line.startswith("# "):
            current = None
            continue
        blocks[current].append(line)
    return {roman: "\n".join(body).strip() for roman, body in blocks.items()}


def normalize_for_signature(body: str) -> str:
    """Strip exclusion-prefix lines + collapse whitespace runs."""
    keep = []
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in EXCLUSION_PREFIXES):
            continue
        keep.append(re.sub(r"\s+", " ", stripped))
    return " ".join(keep)


def fivegram_jaccard(a: str, b: str) -> float:
    """Jaccard similarity over 5-gram character sets."""
    def grams(s: str) -> set[str]:
        return {s[i : i + 5] for i in range(max(0, len(s) - 4))}

    sa, sb = grams(a), grams(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def check_cross_tier_duplication(
    component: dict[str, str], tier1: dict[str, str], tier2: dict[str, str]
) -> list[str]:
    """Check (a) — dual-signal: identity-marker + 5-gram Jaccard >0.85.

    Flags any cross-tier pair whose normalized signatures are identical (Signal 1)
    OR whose 5-gram Jaccard >0.85 (Signal 2).
    """
    failures: list[str] = []
    pairs: list[tuple[str, str, dict[str, str], dict[str, str]]] = [
        ("Component", "Tier 1", component, tier1),
        ("Component", "Tier 2", component, tier2),
        ("Tier 1", "Tier 2", tier1, tier2),
    ]
    for label_a, label_b, set_a, set_b in pairs:
        for r_a, body_a in set_a.items():
            sig_a = normalize_for_signature(body_a)
            for r_b, body_b in set_b.items():
                if r_a == r_b:
                    # same Roman numeral implies orphan, handled by check (b)
                    continue
                sig_b = normalize_for_signature(body_b)
                if sig_a and sig_a == sig_b:
                    failures.append(
                        f"check(a) Signal 1: identity-marker match between "
                        f"{label_a} Principle {r_a} and {label_b} Principle {r_b}"
                    )
                    continue
                similarity = fivegram_jaccard(sig_a, sig_b)
                if similarity > 0.85:
                    failures.append(
                        f"check(a) Signal 2: 5-gram Jaccard {similarity:.2f} > 0.85 "
                        f"between {label_a} Principle {r_a} and {label_b} Principle {r_b}"
                    )
    return failures


def check_post_relocation_orphans(component: dict[str, str]) -> list[str]:
    """Check (b) — relocated principles must NOT appear in the component file.

    Verifies that each principle in TIER1_PRINCIPLES or TIER2_PRINCIPLES is absent
    from the component-tier file. Cross-references (e.g., "Principle IX" without
    body text) are permitted.
    """
    failures: list[str] = []
    relocated = TIER1_PRINCIPLES | TIER2_PRINCIPLES
    for roman in relocated:
        if roman in component:
            # Found a header `### {Roman}.` in component file — orphan
            failures.append(
                f"check(b) post-relocation orphan: Principle {roman} body still "
                f"present in component file"
            )
    return failures


MONOREPO_URL_PREFIX = "https://github.com/Build-Fractal/build-fractal-mono/blob/main/"


def check_cross_references(text: str, name: str) -> list[str]:
    """Check (c) — verify cross-references resolve.

    Two reference forms supported:
    1. **Filesystem-relative paths** (legacy): `[text](relative-path)` resolves to a file on disk.
    2. **GitHub URLs** (canonical for cross-repo references per v4.0.0 erratum):
       `https://github.com/Build-Fractal/build-fractal-mono/blob/main/<path>` —
       the URL's path portion is validated against the monorepo's actual file tree.

    URL form is preferred for cross-tier references because it makes per-repo
    CONSTITUTION.md / CONFORMANCE.md self-contained for standalone reading.
    Filesystem paths still work for intra-document anchor refs and for repo-internal references.
    """
    failures: list[str] = []
    # Match both bare URLs and Markdown links + backtick-quoted paths.
    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    bare_url_re = re.compile(r"`(https://github\.com/Build-Fractal/build-fractal-mono/blob/main/[^`\s]+)`")

    base_dir = (
        ROOT if name == "component"
        else (TIER1.parent if name == "tier1" else TIER2.parent)
    )

    # Filesystem path resolution
    for match in link_re.finditer(text):
        path_part = match.group(2)
        # Strip any anchor (# or §)
        path_only = path_part.split("#")[0].split(" §")[0].strip()
        if not path_only or path_only.startswith(("http://", "https://", "mailto:")):
            # URL form — handled below
            continue
        target = (base_dir / path_only).resolve()
        if not target.exists():
            failures.append(
                f"check(c) broken filesystem link in {name}: {match.group(0)} → {target}"
            )

    # Validate URL form: must match monorepo prefix + resolve to existing file in monorepo.
    # `_BUILD_FRACTAL` is the monorepo's build-fractal/ dir if found — its parent is the
    # monorepo root, regardless of how deeply conversus-oss is nested. Falls back to
    # `ROOT.parent` for the original flat layout.
    monorepo_root = _BUILD_FRACTAL.parent if _BUILD_FRACTAL else ROOT.parent
    seen_urls: set[str] = set()
    url_candidates = [
        *bare_url_re.findall(text),
        *(m.group(2) for m in link_re.finditer(text) if m.group(2).startswith("https://github.com/")),
    ]
    for url in url_candidates:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        if not url.startswith(MONOREPO_URL_PREFIX):
            # Cross-org URL — accept (e.g., to anthropic.com docs) without validation
            if "github.com/Build-Fractal/build-fractal-mono" in url:
                failures.append(
                    f"check(c) URL ref in {name} uses non-canonical monorepo URL form: {url}"
                )
            continue
        rel_path = url[len(MONOREPO_URL_PREFIX):].split("#")[0].split(" ")[0].rstrip("/").rstrip(".,;:`)")
        if not rel_path:
            continue  # Bare prefix
        target = (monorepo_root / rel_path).resolve()
        if not target.exists():
            failures.append(
                f"check(c) URL ref in {name} points at missing monorepo file: {url} → {target}"
            )
    return failures


def check_version_consistency() -> list[str]:
    """Check (d) — Version: fields across the three constitutions must be mutually consistent.

    All three should declare v4.0.0 (or v1.0.0 for newly-established Tier 1/2).
    The component-tier file at v4.0.0 references Tier 1 and Tier 2 at v1.0.0.
    """
    failures: list[str] = []
    version_re = re.compile(r"^\*\*Version:\*\*\s*(\S+)", re.MULTILINE)

    expectations = [
        (COMPONENT, "4.0.0", "component"),
        (TIER1, "1.0.0", "tier1"),
        (TIER2, "1.0.0", "tier2"),
    ]
    for path, expected, name in expectations:
        if not path.exists():
            failures.append(f"check(d) missing file: {path}")
            continue
        text = path.read_text()
        m = version_re.search(text)
        if not m:
            failures.append(f"check(d) no Version: field in {name} ({path})")
            continue
        actual = m.group(1)
        if actual != expected:
            failures.append(
                f"check(d) version mismatch in {name}: expected {expected}, got {actual}"
            )
    return failures


def check_weakening_words(text: str, name: str) -> list[str]:
    """Check (e) — flag suspicious weakening terms near upper-tier principle names.

    Per spec §6.10 enforcement: any "relief," "exception," "adaptation,"
    "exemption," "carve-out," or "bypass" within 200 chars of a Tier 1 principle
    name or "Universal" / "Tier 1" → flag for impl-PR review.
    """
    if name not in {"tier2", "component"}:
        return []  # only Tier 2 / component need flagging
    flags: list[str] = []
    text_lower = text.lower()
    for word in WEAKENING_WORDS:
        for match in re.finditer(re.escape(word), text_lower):
            window_start = max(0, match.start() - 200)
            window_end = min(len(text_lower), match.end() + 200)
            window = text[window_start:window_end]
            for target in WEAKENING_TARGETS:
                if target.lower() in window.lower():
                    flags.append(
                        f"check(e) weakening flag in {name}: '{word}' within 200 chars "
                        f"of '{target}' (position {match.start()})"
                    )
                    break
    return flags


def main() -> int:
    if not all(p.exists() for p in [COMPONENT, TIER1, TIER2]):
        missing = [p for p in [COMPONENT, TIER1, TIER2] if not p.exists()]
        print(f"ERROR: missing constitution files: {missing}", file=sys.stderr)
        return 2

    component_text = COMPONENT.read_text()
    tier1_text = TIER1.read_text()
    tier2_text = TIER2.read_text()

    component_blocks = parse_principle_blocks(component_text)
    tier1_blocks = parse_principle_blocks(tier1_text)
    tier2_blocks = parse_principle_blocks(tier2_text)

    failures: list[str] = []

    failures.extend(check_cross_tier_duplication(component_blocks, tier1_blocks, tier2_blocks))
    failures.extend(check_post_relocation_orphans(component_blocks))
    failures.extend(check_cross_references(component_text, "component"))
    failures.extend(check_cross_references(tier1_text, "tier1"))
    failures.extend(check_cross_references(tier2_text, "tier2"))
    failures.extend(check_version_consistency())

    # Weakening-words check is FLAG, not FAIL — collected separately
    flags: list[str] = []
    flags.extend(check_weakening_words(tier2_text, "tier2"))
    flags.extend(check_weakening_words(component_text, "component"))

    print(f"tier_coherence: parsed {len(component_blocks)} component, "
          f"{len(tier1_blocks)} Tier 1, {len(tier2_blocks)} Tier 2 principles")

    if flags:
        print(f"tier_coherence: {len(flags)} weakening-words FLAGS for impl-PR review:", file=sys.stderr)
        for f in flags[:20]:  # Cap output to first 20 flags
            print(f"  FLAG: {f}", file=sys.stderr)
        if len(flags) > 20:
            print(f"  ... and {len(flags) - 20} more", file=sys.stderr)

    if failures:
        print(f"tier_coherence: {len(failures)} FAILURES:", file=sys.stderr)
        for f in failures:
            print(f"  FAIL: {f}", file=sys.stderr)
        return 1

    print("tier_coherence: all checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
