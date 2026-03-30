# 006 — Markdown File Migration

status: proposal

## Overview

Replace `entries.json` (jrnl export) as the content source with a `content/` directory of individual Markdown files. Each file is a self-contained entry: filename encodes the datetime, body contains the title heading, prose, inline tags, and references. The build pipeline's downstream stages (rendering, NLP, citations, quotebacks, search) are unchanged — only the loader in `build.py` is replaced.

---

## File format

**Filename:** `YYMMDDTHHMMSS.md`

Examples:
```
260330T011305.md
250109T192800.md
```

**Contents:**

```markdown
# Title of the entry

Body prose in Markdown. Inline tags like #autonomía and #tecnología appear anywhere
in the body. References use existing syntaxes: [@citekey] for academic citations and
quoteback blockquotes for web sources.

> "A quoted passage."
> -- [Source Title](https://example.com/source)
```

Rules:
- First line must be `# Title`. If absent, title is treated as empty.
- Everything after the title heading is the body.
- Tags are bare `#word` tokens in the body. No separate frontmatter field.
- No YAML/TOML frontmatter — all metadata comes from filename and body content.

---

## Entry ID

Derived from the filename. The 2-digit year is expanded to 4 digits at parse time:

```
260330T011305  →  20260330T011305
```

Permalinks remain `/entry/20260330T011305/` — same format as current.

---

## Tag extraction

Tags are scanned from the body with a regex before rendering:

```python
TAG_RE = re.compile(r'(?<!\w)#([\w\-]+)', re.UNICODE)
```

Extracted tags are stored in the entry dict under `"tags"` (same key as current), stripped of the `#` prefix — matching the existing `entry_tags()` contract in `src/render.py`. Tags remain visible in the rendered body as plain text.

---

## New loader: `src/loader.py`

Replaces the `json.load` call in `build.py`. Public API:

```python
def load_entries(content_dir: str = "content") -> list[dict]:
    """
    Scan content_dir for *.md files, parse each into an entry dict.
    Returns list sorted newest-first by datetime.

    Each dict has: title, body, date, time, tags, entry_id
    """
```

Internal steps per file:

1. Parse filename → `entry_id` (expand 2-digit year), `date`, `time`
2. Read file contents
3. Extract `# Title` from first line → `title`; remainder → `body`
4. Run `TAG_RE` over body → `tags`
5. Return dict with same keys as current JSON entries

Estimated size: ~50 lines.

---

## Build changes

### `build.py`

```python
# Before
import json
with open("entries.json") as f:
    data = json.load(f)
entries = data["entries"]

# After
from src.loader import load_entries
entries = load_entries("content")
```

Everything downstream receives the same list of dicts. No other changes to `build.py`.

### `update.sh`

```bash
# Before
jrnl --export json > entries.json && uv run build.py && uv run python -m pagefind --site dist/

# After
uv run build.py && uv run python -m pagefind --site dist/
```

jrnl dependency removed from the build step entirely.

---

## Migration script

One-time conversion of `entries.json` → `content/*.md`.

```python
# migrate.py
import json, re, pathlib

CONTENT = pathlib.Path("content")
CONTENT.mkdir(exist_ok=True)

with open("entries.json") as f:
    entries = json.load(f)["entries"]

for e in entries:
    date = e["date"].replace("-", "")[2:]   # "2026-03-30" → "260330"
    time = e["time"].replace(":", "")        # "01:13:05"   → "011305"
    name = f"{date}T{time}.md"

    title = e.get("title", "").strip()
    body  = e.get("body",  "").strip()
    tags  = [t.lstrip("#@") for t in e.get("tags", [])]

    lines = []
    if title:
        lines.append(f"# {title}\n")
    if body:
        lines.append(body)
    if tags:
        tag_line = "  ".join(f"#{t}" for t in tags)
        lines.append(f"\n{tag_line}")

    (CONTENT / name).write_text("\n\n".join(lines) + "\n")

print(f"Wrote {len(entries)} files to {CONTENT}/")
```

Tags are appended as a trailing line in the body. They render as visible text, consistent with the inline-tag convention.

---

## Failure modes

| Situation | Behavior |
|-----------|----------|
| File with no `# Title` | `title` is empty string; entry renders without a heading (same as current) |
| Malformed filename | Logged and skipped at load time |
| Duplicate filenames (same second) | Last file wins (filesystem sort order); log a warning |
| Body with no tags | `tags` is empty list; no change in rendering |
| `content/` missing | `load_entries` raises with a clear message; build aborts |

---

## Interaction with existing specs

- **001 (MVP):** Writing interface changes (no jrnl), but site structure and rendered output are identical.
- **003 (Heatmap):** No conflict. NLP operates on the body string after tag extraction; `#tag` tokens may appear as bigram candidates but will not meet the POS filter (they parse as punctuation or X).
- **004 (Quotebacks):** No conflict. Quoteback preprocessing runs on the body string as before.
- **005 (Citations):** No conflict. `[@citekey]` syntax is in the body and processed identically.

---

## Out of scope

- Tag index pages (filterable by tag).
- YAML/TOML frontmatter support.
- Subdirectory organization within `content/`.
- Watching `content/` for changes (live reload).
- Removing `entries.json` from the repo before migration is verified.
