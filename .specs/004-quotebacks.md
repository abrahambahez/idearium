# 004 — Quotebacks

## Overview

Quotebacks are web citations embedded as styled, attributed blockquotes. When writing a jrnl entry, a quote from any webpage is captured with a markdown-native syntax. At build time the raw text is resolved into a `<blockquote class="quoteback">` element, which `quoteback.js` upgrades into a full citation card at runtime.

The writing step requires no tooling beyond typing. The build step handles metadata fetching and caches results so rebuilds are instant and offline.

---

## Writing syntax

In a jrnl entry body, a quoteback is a standard markdown blockquote where the attribution line uses a markdown link:

```
> "The density of links in a document is a proxy for how well-connected its ideas are."
> -- [Hyperlink Maximalism](https://thesephist.com/posts/hyperlink/)
```

The `-- [Title](url)` form is the canonical syntax. The title is explicit in the source text, no network fetch is needed, and the raw entry reads as valid markdown — if the build step is ever skipped or stripped, mistune renders it as a normal blockquote with a working hyperlink.

A bare URL is also accepted as a fallback when writing quickly and the title is not known:

```
> "The density of links in a document is a proxy for how well-connected its ideas are."
> -- https://thesephist.com/posts/hyperlink/
```

In this case the build fetches the page title and caches it.

---

## Pipeline

```
entries.json
  → for each entry body: preprocess_quotebacks()             [new, before NLP]
      → parse QUOTEBACK_RE matches
      → resolve title: inline > cache > fetch
      → emit <blockquote class="quoteback"> HTML
  → annotate_body() (bigram heatmap, existing)
  → mistune renders → HTML
```

The preprocessing runs before `annotate_body` so the quoteback block is already HTML and mistune leaves it alone (it allows inline HTML).

---

## Regex

```python
QUOTEBACK_RE = re.compile(
    r'((?:^>[ \t]*.+\n)+?)'          # body: one or more blockquote lines (non-greedy)
    r'^>[ \t]*--[ \t]+'               # attribution prefix
    r'(?:'
        r'\[([^\]]+)\]\((https?://[^)]+)\)'  # form A: [Title](url)
        r'|'
        r'(https?://\S+)'             # form B: bare url
    r')[ \t]*$',
    re.MULTILINE,
)
```

Groups:
- `1` — raw blockquote body lines (including `> ` prefix)
- `2` — title from form A (may be None)
- `3` — url from form A (may be None)
- `4` — url from form B (may be None)

Active URL: `group(3) or group(4)`. Active inline title: `group(2)`.

---

## Cache

File: `quoteback_cache.json` at repo root. Committed to git — makes builds reproducible offline and prevents re-fetching on every rebuild.

Schema:
```json
{
  "https://thesephist.com/posts/hyperlink/": {
    "title": "Hyperlink Maximalism",
    "author": "Linus Lee"
  }
}
```

`author` may be an empty string if the page provides no author signal. The cache is append-only during a build run; existing entries are never overwritten.

---

## Metadata fetch

Used only when form B (bare URL) is matched and the URL is not in the cache.

```python
import httpx
from html.parser import HTMLParser

def fetch_metadata(url: str) -> dict:
    """Returns {"title": str, "author": str}. Returns {} on any failure."""
    try:
        r = httpx.get(url, timeout=8, follow_redirects=True,
                      headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
    except Exception as exc:
        print(f"  [quoteback] fetch failed for {url}: {exc}", flush=True)
        return {}
    return _parse_head(r.text)
```

`_parse_head` is a minimal `HTMLParser` subclass. It reads `<title>`, `<meta name="author">`, and `<meta property="og:site_name">` (author fallback), then stops at `</head>` to avoid parsing the full document.

Title resolution order per URL:
1. Inline title from `[Title](url)` — no fetch
2. Cache hit — no fetch
3. `<title>` tag from fetched page
4. Bare URL string (last resort, still builds)

---

## HTML output

```python
from urllib.parse import urlparse

def _resolve(match, cache: dict) -> str:
    raw_lines = match.group(1)
    inline_title = match.group(2)
    url = match.group(3) or match.group(4)

    # strip `> ` prefix from each body line
    body = re.sub(r'^>[ \t]?', '', raw_lines, flags=re.MULTILINE).strip()

    if url not in cache:
        if inline_title:
            cache[url] = {"title": inline_title, "author": ""}
        else:
            meta = fetch_metadata(url)
            cache[url] = {
                "title": meta.get("title") or url,
                "author": meta.get("author", ""),
            }

    title = cache[url]["title"]
    author = cache[url]["author"]

    return (
        f'<blockquote class="quoteback" '
        f'data-title="{title}" '
        f'data-author="{author}" '
        f'cite="{url}">'
        f'{body}'
        f'<footer>— <cite><a href="{url}">{title}</a></cite></footer>'
        f'</blockquote>\n\n'
    )
```

---

## New file: `src/quoteback.py`

Public API:

```python
def load_cache() -> dict: ...
def save_cache(cache: dict) -> None: ...
def preprocess_quotebacks(text: str, cache: dict) -> str: ...
```

`preprocess_quotebacks` applies `QUOTEBACK_RE.sub(_resolve, text)` with the cache passed through the lambda closure.

Estimated size: ~80 lines.

---

## Build changes

### `build.py`

```python
from src.quoteback import load_cache, save_cache

def main():
    ...
    quoteback_cache = load_cache()
    build_feed(entries, bigram_scores, DIST, PER_PAGE, SITE_TITLE, quoteback_cache)
    build_entries(entries, bigram_scores, DIST, SITE_TITLE, quoteback_cache)
    save_cache(quoteback_cache)
    ...
```

`save_cache` is called once after all pages are built, so a single fetch per URL regardless of how many entries reference it.

### `src/render.py`

`entry_body_html` gains a `quoteback_cache` parameter:

```python
def entry_body_html(entry, bigram_scores=None, quoteback_cache=None):
    body = entry.get("body", "").strip()
    if not body:
        return ""
    if quoteback_cache is not None:
        body = preprocess_quotebacks(body, quoteback_cache)
    if bigram_scores:
        return annotate_body(body, bigram_scores)
    return md(body)
```

`render_entry_fragment` passes `quoteback_cache` through to `entry_body_html`. `build_entries` and `build_feed` in `src/pages.py` pass it through to `render_entry_fragment`.

### `src/render.py` — `base()`

Add to `<head>`:

```html
<script src="/assets/quoteback.js"></script>
```

### `build.py` — `build_assets()`

```python
shutil.copy("assets/quoteback.js", dist / "assets" / "quoteback.js")
```

---

## One-time setup

```bash
curl -o assets/quoteback.js \
  https://cdn.jsdelivr.net/gh/Blogger-Peer-Review/quotebacks@1/quoteback.js
```

No new Python dependencies. `httpx` is already installed.

---

## Failure modes

| Situation | Behavior |
|---|---|
| Network timeout / HTTP error | Logs warning, uses URL as title, build continues |
| No `<title>` in page | Uses URL string as title |
| Inline `[Title](url)` provided | No fetch, no cache read needed |
| Cache hit | No fetch |
| Regex no match (normal blockquote) | Untouched, renders as standard `<blockquote>` |
| `quoteback.js` fails to load | Degrades to plain `<blockquote>` with footer link |

---

## Interaction with existing specs

- **003 (Heatmap):** no conflict. Quoteback preprocessing runs before `annotate_body`. The resolved HTML block is opaque to the NLP step — bigram spans are not injected inside quoteback content.
- **002 (Selection popover):** no conflict. Pagefind indexes the rendered text content of quoteback blocks normally.

---

## Out of scope

- Fetching author from structured data (JSON-LD, microformats).
- Favicon resolution.
- Dark mode toggle per quoteback.
- Quoteback library page (aggregated view of all sourced URLs).
