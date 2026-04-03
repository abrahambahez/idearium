# Markdown Source Files Spec

## Overview

Replace `jrnl` + `entries.json` with a folder of plain Markdown files as the source of truth. The build pipeline reads the folder directly — no manual export step, no committed JSON.

---

## Writing Interface

- **Tool:** Any text editor
- **Location:** `entries/` folder at repo root
- **Filename:** `YYYYMMDDTHHMM.md` — this is the entry ID and encodes date + time
- **Format:**

```markdown
---
title: Entry title here
tags:
  - tag1
  - tag2
---

Body in Markdown.
```

- `tags` is optional; omit or leave empty list for untagged entries
- Tags are plain strings (no `#` prefix in frontmatter — `#` only in body text for inline references)

---

## Build Pipeline

```
python build.py   # reads entries/ directly
pagefind --site dist/
```

CI runs `build.py`; no pre-export step. `entries/` is committed; `entries.json` is deleted.

---

## Parsing Logic

`build.py` replaces `open(ENTRIES_FILE)` with a loader that:

1. Globs `entries/*.md`
2. For each file:
   - Parses filename → `date` (`YYYY-MM-DD`) and `time` (`HH:MM`)
   - Parses frontmatter → `title`, `tags` (list, default `[]`)
   - Remainder after frontmatter → `body`
3. Produces the same entry dict shape the rest of the pipeline already expects:

```python
{
    "title": str,
    "body": str,       # raw Markdown, not rendered
    "date": str,       # "YYYY-MM-DD"
    "time": str,       # "HH:MM"
    "tags": list[str],
    "starred": False,  # dropped concept; always False
}
```

No other part of the pipeline changes.

---

## Entry ID

Derived from filename: `YYYYMMDDTHHMM` (drop `.md`). Matches existing URL pattern `/entry/<id>/`.

---

## Removed

- `jrnl` dependency
- `entries.json` (deleted from repo, added to `.gitignore`)
- `update.sh`

---

## Dependencies Added

- `python-frontmatter` — parses YAML frontmatter from Markdown files

---

## Out of Scope

- Migrating existing jrnl entries to `.md` files (manual one-time task)
- `starred` field (was always false for most entries; dropped)
