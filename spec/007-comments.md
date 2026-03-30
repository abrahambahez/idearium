# 007 — Comments

status: proposal

## Overview

Reader responses collected via email are stored in `comments.json` and threaded to their parent entries at build time. The operator (site owner) is the sole editorial gate: a comment exists in the file only because it was consciously added. No submission form, no server, no moderation queue. Comments render on individual entry pages (`/entry/{eid}/`) only — not in the feed.

---

## Storage format

**File:** `comments.json` at the repository root.

```json
{
  "20260330T011305": [
    {
      "author": "Jane Doe",
      "date": "2026-04-01",
      "body": "Your point about X reminded me of..."
    },
    {
      "author": "Sergio",
      "date": "2026-04-02",
      "body": "Exactly — and it also connects to Y.",
      "role": "owner"
    },
    {
      "author": "Jane Doe",
      "date": "2026-04-03",
      "body": "Right, but what about Z?"
    }
  ],
  "20250109T192800": [
    {
      "author": "Anon",
      "date": "2026-02-14",
      "body": "This changed how I think about the topic."
    }
  ]
}
```

**Key:** entry ID in `YYYYMMDDTHHMMSS` format, as returned by `entry_id()` in `src/render.py`.

**Comment fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `author` | string | yes | Display name, as provided or pseudonymized |
| `date` | string | yes | ISO date (`YYYY-MM-DD`). Defaults to today if omitted by script |
| `body` | string | yes | Plain text. No Markdown rendering — displayed as-is |
| `role` | string | no | `"owner"` marks a reply from the site owner. Absent or any other value = reader |

Comments are ordered as written; the build renders them in array order (chronological by convention). A linear email thread is represented as a flat chronological array — no parent IDs needed.

---

## `add-comment.py`

A standalone script at the repository root. Run after deciding a reader response is worth publishing.

### Usage

```bash
# reader comment
python add-comment.py --entry 20260330T011305 --author "Jane Doe" --body "Your point about X..."

# your reply in the thread
python add-comment.py --entry 20260330T011305 --author "Sergio" --role owner --body "Exactly — and..."

# body from stdin (paste from email client, or pipe)
echo "Your point about X..." | python add-comment.py --entry 20260330T011305 --author "Jane Doe"

# override date (preserve original email date)
python add-comment.py --entry 20260330T011305 --author "Jane Doe" --date 2026-03-28 --body "..."
```

### Behaviour

1. Load `comments.json`; create an empty `{}` if the file does not exist.
2. If `--body` is not given, read body from stdin.
3. Append `{"author": ..., "date": ..., "body": ...}` to the list at `comments[entry_id]`.
4. Write `comments.json` back with `indent=2, ensure_ascii=False`.
5. Run `git add comments.json && git commit -m "comment: {entry} by {author}" && git push`.

### Script

```python
#!/usr/bin/env python3
import json
import sys
import argparse
import subprocess
from datetime import date
from pathlib import Path

COMMENTS_FILE = Path("comments.json")

p = argparse.ArgumentParser()
p.add_argument("--entry",  required=True)
p.add_argument("--author", required=True)
p.add_argument("--body",   default=None)
p.add_argument("--date",   default=str(date.today()))
p.add_argument("--role",   default=None, choices=["owner"])
args = p.parse_args()

body = args.body if args.body is not None else sys.stdin.read().strip()
if not body:
    sys.exit("error: comment body is empty")

comment = {"author": args.author, "date": args.date, "body": body}
if args.role:
    comment["role"] = args.role

data = json.loads(COMMENTS_FILE.read_text(encoding="utf-8")) if COMMENTS_FILE.exists() else {}
data.setdefault(args.entry, []).append(comment)
COMMENTS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

subprocess.run(["git", "add", str(COMMENTS_FILE)], check=True)
subprocess.run(["git", "commit", "-m", f"comment: {args.entry} by {args.author}"], check=True)
subprocess.run(["git", "push"], check=True)
print(f"Published comment on {args.entry} by {args.author}")
```

---

## Pipeline

```
comments.json
  → build.py: load_comments() → dict[entry_id, list[comment]]   [new]
  → build_entries(): look up comments by eid, pass to render     [modified]
  → render_entry_fragment(): append <section class="comments">   [modified]
```

Comments are not passed to `build_feed()`. The feed renders `render_entry_fragment` with `link_title=True`; entry pages use `link_title=False`. Comments are passed only in `build_entries`.

---

## Build changes

### `build.py`

```python
COMMENTS_FILE = "comments.json"

def load_comments() -> dict:
    p = Path(COMMENTS_FILE)
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def main():
    ...
    comments = load_comments()
    ...
    build_entries(entries, bigram_scores, DIST, SITE_TITLE, quoteback_cache, citation_refs, comments)
```

`build_feed` signature is unchanged.

### `src/pages.py` — `build_entries`

```python
def build_entries(
    entries, bigram_scores, dist, site_title,
    quoteback_cache=None, citation_refs=None, comments=None
):
    for entry in entries:
        eid = entry_id(entry)
        entry_comments = (comments or {}).get(eid, [])
        fragment = render_entry_fragment(
            entry, link_title=False, bigram_scores=bigram_scores,
            quoteback_cache=quoteback_cache, citation_refs=citation_refs,
            indexable=True, comments=entry_comments or None
        )
        ...
```

`entry_comments or None` ensures an empty list is treated as absent (no section rendered).

### `src/render.py` — `render_entry_fragment`

```python
def render_entry_fragment(
    entry, *, link_title=True, bigram_scores=None,
    quoteback_cache=None, citation_refs=None,
    indexable=False, comments=None
):
    ...
    comments_html = render_comments(comments) if comments else ""

    return f"""\
<article class="entry"{pf_body}>
  ...
</article>
{comments_html}
"""
```

### `src/render.py` — `render_comments`

```python
def render_comments(comments: list[dict]) -> str:
    items = []
    for c in comments:
        role_attr = ' data-role="owner"' if c.get("role") == "owner" else ""
        items.append(
            f'<div class="comment"{role_attr}>'
            f'<p class="comment-meta">{html.escape(c["author"])} · {html.escape(c["date"])}</p>'
            f'<p class="comment-body">{html.escape(c["body"])}</p>'
            f'</div>'
        )
    return f'<section class="comments" data-pagefind-ignore>\n' + "\n".join(items) + "\n</section>"
```

`html.escape` on all user-supplied fields. `data-pagefind-ignore` keeps comment text out of the search index. No Markdown rendering — body is plain text.

---

## HTML output

```html
<section class="comments" data-pagefind-ignore>
  <div class="comment">
    <p class="comment-meta">Jane Doe · 2026-04-01</p>
    <p class="comment-body">Your point about X reminded me of...</p>
  </div>
  <div class="comment" data-role="owner">
    <p class="comment-meta">Sergio · 2026-04-02</p>
    <p class="comment-body">Exactly — and it also connects to Y.</p>
  </div>
  <div class="comment">
    <p class="comment-meta">Jane Doe · 2026-04-03</p>
    <p class="comment-body">Right, but what about Z?</p>
  </div>
</section>
```

---

## CSS

Added to `assets/style.css`. Follows tonal carving — no border lines.

```css
/* ── Comments ────────────────────────────────────── */
.comments {
  margin-top: 2.5rem;
  padding: 1.5rem;
  background: var(--surface-low);
}

.comments::before {
  content: "Respuestas";
  display: block;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--outline);
  margin-bottom: 1.25rem;
}

.comment + .comment {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
}

.comment[data-role="owner"] {
  background: var(--surface-dim);
  padding: 0.75rem 1rem;
}

.comment-meta {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  color: var(--outline);
  margin: 0 0 0.35rem;
}

.comment-body {
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.7;
}
```

---

## Failure modes

| Situation | Behavior |
|-----------|----------|
| `comments.json` absent | `load_comments()` returns `{}`; build proceeds normally, no comments rendered |
| Entry has no comments | Empty list → `None` → `render_comments` not called, no section in HTML |
| Unknown entry ID in `comments.json` | Silently ignored — `build_entries` only looks up IDs for entries being built |
| `body` field contains HTML | `html.escape` neutralizes it; renders as literal text |
| `add-comment.py` run for a non-existent entry ID | Script succeeds; comment is stored but never rendered until a matching entry exists |

---

## Limitations

**Multiple parallel threads per entry** (two readers emailing independently about the same post) are not modelled. Their exchanges would interleave in the flat array. In practice, publish each as its own chronological sequence or split them into separate entries. Branching/parent-ID threading is out of scope.

---

## Out of scope

- A reader-facing submission form.
- Markdown rendering in comment bodies.
- Showing comment count in the feed.
- Email notification on new emails from readers — handled outside the build system.
