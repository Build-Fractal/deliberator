# Rename event: `conversus` → `deliberator` (2026-06-23)

This project was renamed from **`conversus`** to **`deliberator`** on **2026-06-23**, prior to its first PyPI publish.

## What changed

- **Project name** — Conversus → Deliberator
- **Python package on PyPI** — `pip install conversus` → `pip install deliberator`
- **CLI command** — `conversus run …` → `deliberator run …`
- **GitHub repo** — `Build-Fractal/conversus-oss` → `Build-Fractal/deliberator` (GitHub auto-redirects old URLs)
- **Python imports** — `from conversus.X import …` → `from deliberator.X import …`
- **Foundation Python package** — `conversus/` → `deliberator/` (the engine runtime stays at `engine/`)
- **MCP tool names** — `conversus_decide` / `conversus_run` / `conversus_validate` → `deliberator_*`
- **Slash commands** — `/conversus:*` → `/deliberator:*`
- **Config filename convention** — `conversus.yml` → `deliberator.yml`
- **User dotfile dir** — `~/.conversus/` → `~/.deliberator/`
- **Tier 2 suite name** — `build-fractal/conversus/` → `build-fractal/deliberator/` (governance event logged in `CONSTITUTIONAL_CONVERSATIONS.md`)

## What did NOT change

The audit-trail discipline of this project required preserving every pre-rename artifact verbatim. The following directories and files use the pre-rename name `conversus` intentionally and are **not historical artifacts to be edited**:

- `deliberations/` — 43+ archived deliberation runs from the project's own development, dated before 2026-06-23
- `specs/` — 87+ formal specifications, including `v4.0.0-tier-extraction/` and the rest of the constitutional amendment record
- `CHANGELOG.md` entries dated before 2026-06-23
- `CONSTITUTIONAL_CONVERSATIONS.md` entries dated before 2026-06-23

These are the project's history. Future contributors reading those files will see the old name and should treat references as historical (i.e., the project that existed *as `conversus`* up to 2026-06-23).

## Why

The pre-rename name `conversus` (Latin: "turned together") was distinctive but obscure. `deliberator` is plain English, accurately describes what the engine does (multi-agent deliberation), and is unique on PyPI. Done pre-PyPI-publish so no external users have to migrate.

The full rationale, name-decision deliberation, and governance event are documented in:

- `CONSTITUTIONAL_CONVERSATIONS.md` — Tier 2 governance log entry dated 2026-06-23
- `CHANGELOG.md` — Unreleased section, "Renamed" entry

## For people landing here from stale links

GitHub auto-redirects every URL that pointed at `Build-Fractal/conversus-oss/...` to the equivalent path under `Build-Fractal/deliberator/...`. Existing local clones continue to work — `git fetch` / `git pull` transparently follow the redirect. No action required from previously-installed users (there were no PyPI publishes pre-rename, so nothing to migrate).

If something IS broken because of the rename, please open an issue at https://github.com/Build-Fractal/deliberator/issues.
