# 008 — Post Footer & Social Sharing

status: proposal

## Overview

Each entry gets a minimal footer with two actions: **Compartir** (share the post URL) and **Responder** (reply by email). Both use native `<dialog>` elements — no external libraries. In the feed, a tonal separator follows each entry footer. Entry pages show the footer without a separator.

A social preview layer adds Open Graph and Twitter Card meta tags to individual entry pages so links shared to Slack, Twitter, iMessage, etc. unfurl correctly. This requires per-entry data flowing into `base()`.

No backend. No form submissions. No new dependencies.

---

## Post footer

### Placement

- **Feed** (`build_feed`): footer rendered inside each `<article>`, after the body and tags. A tonal separator follows outside the article.
- **Entry page** (`build_entries`): footer rendered inside the `<article>`. No separator.

### HTML

```html
<footer class="entry-footer">
  <button class="entry-action" data-action="share" data-url="/entry/20260330T011305/" data-title="Título del post">
    <svg ...><!-- share icon --></svg> Compartir
  </button>
  <button class="entry-action" data-action="reply" data-subject="Comentario a Título del post (20260330T011305)">
    <svg ...><!-- mail icon --></svg> Responder
  </button>
</footer>
```

Data attributes carry all entry-specific values; the JS handlers are generic and stateless.

### Icons

Inline SVG, sourced from Lucide (MIT). Two icons:
- `share-2` → Compartir
- `mail` → Responder

Rendered inline (not an external sprite) to avoid an extra network request and keep the build self-contained.

---

## Feed separator

CSS only — no Python changes to entry rendering.

```css
.feed-entry + .feed-entry {
  border-top: 1px solid var(--surface-highest);
}
```

`<article>` elements in the feed get class `feed-entry`. The footer sits inside the article, so the separator appears visually between footer and next entry's metadata — exactly the intended position.

Alternative if class addition is undesirable: `article + article` selector works identically if articles are direct siblings in the feed container.

---

## "Compartir" dialog

### Behaviour

1. Click → check `navigator.share` availability.
2. **If available** (mobile, modern browsers): call `navigator.share({ title, url })` directly. No dialog shown.
3. **If unavailable** (desktop): open `<dialog id="share-dialog">` showing the canonical URL and a copy button.
4. Copy button calls `navigator.clipboard.writeText(url)`. Button label changes to "Copiado ✓" for 2 seconds, then resets.

### HTML (dialog, injected once on first use)

```html
<dialog id="share-dialog">
  <button class="dialog-close" aria-label="Cerrar">×</button>
  <p class="dialog-label">Enlace</p>
  <div class="share-url-row">
    <input id="share-url-input" type="text" readonly>
    <button id="share-copy-btn">Copiar</button>
  </div>
</dialog>
```

---

## "Responder" dialog

### Behaviour

1. Click → open `<dialog id="reply-dialog">`.
2. Dialog contains a textarea for the message body.
3. Submit button constructs a `mailto:` URL:
   ```
   mailto:hi@sergio-barrera.com
     ?subject=Comentario%20a%20T%C3%ADtulo%20(20260330T011305)
     &body={encoded textarea value}
   ```
4. Opens the URL (`window.location.href = ...`) — launches user's email client prefilled.
5. Dialog closes.

### HTML (dialog, injected once on first use)

```html
<dialog id="reply-dialog">
  <button class="dialog-close" aria-label="Cerrar">×</button>
  <p class="dialog-label" id="reply-subject-display"></p>
  <textarea id="reply-body" rows="6" placeholder="Tu mensaje…"></textarea>
  <button id="reply-submit">Abrir cliente de correo →</button>
</dialog>
```

### Caveat

Requires a configured email client. On mobile this is reliable. On desktop (webmail users) it may do nothing. This is an accepted limitation for an editorial/personal blog audience.

---

## Environment configuration

Site-specific values are loaded from a `.env` file at the repository root. The existing `LIBRARY_FILE` env var is absorbed into this system.

**`.env`**

```
SITE_URL=https://idearium.sergio-barrera.com
LIBRARY_FILE=/path/to/references.json
```

**Loading** — add `python-dotenv` as a dev dependency (`uv add python-dotenv`). Load once at the top of `build.py`:

```python
from dotenv import load_dotenv
load_dotenv()

SITE_URL = os.environ.get("SITE_URL", "")
```

`SITE_URL` with no trailing slash. An empty string is accepted for local builds — OG tags are simply omitted if `SITE_URL` is unset.

`.env` is added to `.gitignore`. A `.env.example` is committed with placeholder values.

---

## Social preview meta tags

### Scope

Meta tags are injected only on **individual entry pages** (`/entry/{eid}/`). Feed, search, and other pages receive no OG tags.

### Tags

```html
<!-- Open Graph -->
<meta property="og:type"        content="article">
<meta property="og:title"       content="Notas de Sergio — {title}">
<meta property="og:description" content="{extracted description}">
<meta property="og:url"         content="{SITE_URL}/entry/{eid}/">
<meta property="og:image"       content="{SITE_URL}/assets/og-default.jpg">

<!-- Twitter / X Card -->
<meta name="twitter:card"        content="summary_large_image">
<meta name="twitter:title"       content="Notas de Sergio — {title}">
<meta name="twitter:description" content="{extracted description}">
<meta name="twitter:image"       content="{SITE_URL}/assets/og-default.jpg">
```

`og:title` always carries the prefix `"Idearium — "`. Since jrnl treats the first line of text as title, titleless entries are not expected; the prefix is always present.

### `og:image` — fallback asset

A static image at `assets/og-default.jpg`. Dimensions: **1200 × 630 px** (standard OG card ratio). Referenced as `{SITE_URL}/assets/og-default.jpg`. The file is committed to the repo and copied to `dist/assets/` by `build_assets()`. Per-entry images are out of scope.

`twitter:card` is `summary_large_image` (not `summary`) so the fallback image renders as a full banner card rather than a small thumbnail — this looks better for text-first content.

### Description extraction

Run on the **raw body string** before any build preprocessing. Strips presentation markup only; citation keys, quoteback quotes, and `#tags` are left intact as they read naturally in plain text.

**Stripping rules (in order):**

1. Headings — `^#{1,6}\s+` → `""` (multiline)
2. Bold/italic — `\*{1,3}([^*\n]+)\*{1,3}` → `\1`; `_{1,3}([^_\n]+)_{1,3}` → `\1`
3. Blockquote markers — `^>\s?` → `""` (multiline)
4. Collapse whitespace — `\s+` → `" "`, strip

Truncate to **160 characters**, breaking at the last word boundary before the limit. Append `"…"` if truncated.

```python
import re

def extract_og_description(body: str, max_len: int = 160) -> str:
    text = re.sub(r'^#{1,6}\s+', '', body, flags=re.MULTILINE)
    text = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_\n]+)_{1,3}', r'\1', text)
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)
    text = ' '.join(text.split())
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(' ', 1)[0]
    return cut + '…'
```

If the result is empty (body is blank), the `og:description` and `twitter:description` tags are omitted entirely.

---

## Build changes

### `src/render.py` — `render_entry_fragment`

Gains a `show_footer: bool = True` parameter. Footer is rendered on both feed and entry pages. The separator between feed items is CSS-driven (no Python change needed).

```python
def render_entry_fragment(..., show_footer: bool = True) -> str:
    ...
    footer_html = render_entry_footer(eid, title) if show_footer else ""
    return f"""
<article class="entry feed-entry"{pf_body}>
  ...
  {footer_html}
</article>
"""
```

### `src/render.py` — `render_entry_footer`

```python
def render_entry_footer(eid: str, title: str) -> str:
    subject = f"Comentario a {title} ({eid})" if title else f"Comentario ({eid})"
    return f"""\
<footer class="entry-footer">
  <button class="entry-action" data-action="share"
          data-url="/entry/{eid}/"
          data-title="{html.escape(title or eid)}">
    {ICON_SHARE} Compartir
  </button>
  <button class="entry-action" data-action="reply"
          data-subject="{html.escape(subject)}">
    {ICON_MAIL} Responder
  </button>
</footer>"""
```

`ICON_SHARE` and `ICON_MAIL` are module-level string constants holding the inline SVG.

### `src/render.py` — `base()`

Gains optional `meta: dict | None = None` parameter. OG tags are injected in `<head>` after the stylesheet link. Feed and search pages pass `None`.

```python
def base(title, body, *, site_title, active="", meta=None):
    og_tags = _render_og_tags(meta) if meta else ""
    # in <head>: ...existing tags... + og_tags
```

```python
def _render_og_tags(meta: dict) -> str:
    lines = [
        f'<meta property="og:type" content="article">',
        f'<meta property="og:title" content="{html.escape(meta["og_title"])}">',
        f'<meta property="og:url" content="{html.escape(meta["url"])}">',
        f'<meta property="og:image" content="{html.escape(meta["image"])}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html.escape(meta["og_title"])}">',
        f'<meta name="twitter:image" content="{html.escape(meta["image"])}">',
    ]
    if meta.get("description"):
        desc = html.escape(meta["description"])
        lines += [
            f'<meta property="og:description" content="{desc}">',
            f'<meta name="twitter:description" content="{desc}">',
        ]
    return "\n  ".join(lines)
```

### `src/pages.py` — `build_entries`

```python
def build_entries(
    entries, bigram_scores, dist, site_title,
    quoteback_cache=None, citation_refs=None, comments=None,
    site_url="",
):
    for entry in entries:
        eid = entry_id(entry)
        title = entry_title(entry)
        meta = None
        if site_url:
            meta = {
                "og_title": f"Idearium — {title}" if title else "Idearium",
                "description": extract_og_description(entry.get("body", "")),
                "url": f"{site_url}/entry/{eid}/",
                "image": f"{site_url}/assets/og-default.jpg",
            }
        ...
        write(..., base(..., meta=meta))
```

`extract_og_description` is imported from a new `src/og.py` module (alongside `_render_og_tags` if preferred, or both in `src/render.py`).

### `build.py`

```python
from dotenv import load_dotenv
load_dotenv()
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")

...
build_entries(..., site_url=SITE_URL)
```

### `build_assets()`

Add `og-default.jpg` to the copy list:

```python
shutil.copy(src_assets / "og-default.jpg", assets_dir / "og-default.jpg")
```

---

## JavaScript

Added to the existing `<script>` block in `base()`.

```js
document.addEventListener("click", e => {
  const btn = e.target.closest(".entry-action");
  if (!btn) return;

  if (btn.dataset.action === "share") {
    const url = new URL(btn.dataset.url, location.origin).href;
    if (navigator.share) {
      navigator.share({ title: btn.dataset.title, url });
      return;
    }
    let dlg = document.getElementById("share-dialog");
    if (!dlg) {
      dlg = document.createElement("dialog");
      dlg.id = "share-dialog";
      dlg.innerHTML = `
        <button class="dialog-close" aria-label="Cerrar">&times;</button>
        <p class="dialog-label">Enlace</p>
        <div class="share-url-row">
          <input id="share-url-input" type="text" readonly>
          <button id="share-copy-btn">Copiar</button>
        </div>`;
      dlg.querySelector(".dialog-close").addEventListener("click", () => dlg.close());
      dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
      dlg.querySelector("#share-copy-btn").addEventListener("click", () => {
        navigator.clipboard.writeText(document.getElementById("share-url-input").value);
        const btn = document.getElementById("share-copy-btn");
        btn.textContent = "Copiado ✓";
        setTimeout(() => btn.textContent = "Copiar", 2000);
      });
      document.body.appendChild(dlg);
    }
    document.getElementById("share-url-input").value = url;
    dlg.showModal();
  }

  if (btn.dataset.action === "reply") {
    let dlg = document.getElementById("reply-dialog");
    if (!dlg) {
      dlg = document.createElement("dialog");
      dlg.id = "reply-dialog";
      dlg.innerHTML = `
        <button class="dialog-close" aria-label="Cerrar">&times;</button>
        <p class="dialog-label" id="reply-subject-display"></p>
        <textarea id="reply-body" rows="6" placeholder="Tu mensaje…"></textarea>
        <button id="reply-submit">Abrir cliente de correo →</button>`;
      dlg.querySelector(".dialog-close").addEventListener("click", () => dlg.close());
      dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
      dlg.querySelector("#reply-submit").addEventListener("click", () => {
        const subject = encodeURIComponent(document.getElementById("reply-subject-display").dataset.subject);
        const body = encodeURIComponent(document.getElementById("reply-body").value);
        window.location.href = `mailto:hi@sergio-barrera.com?subject=${subject}&body=${body}`;
        dlg.close();
      });
      document.body.appendChild(dlg);
    }
    document.getElementById("reply-subject-display").dataset.subject = btn.dataset.subject;
    document.getElementById("reply-subject-display").textContent = btn.dataset.subject;
    document.getElementById("reply-body").value = "";
    dlg.showModal();
  }
});
```

---

## CSS

```css
/* ── Entry footer ────────────────────────────────── */
.entry-footer {
  display: flex;
  gap: 1.25rem;
  margin-top: 1.25rem;
  padding-top: 0.75rem;
}

.entry-action {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: none;
  border: none;
  padding: 0;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: var(--outline);
  cursor: pointer;
}

.entry-action:hover { color: var(--primary); }

.entry-action svg {
  width: 0.9rem;
  height: 0.9rem;
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}

/* Feed separator */
.feed-entry + .feed-entry {
  border-top: 1px solid var(--surface-highest);
  padding-top: 2rem;
  margin-top: 2rem;
}

/* ── Shared dialog chrome ────────────────────────── */
.dialog-close {
  float: right;
  background: none;
  border: none;
  font-size: 1.25rem;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  color: var(--outline);
}
.dialog-close:hover { color: var(--primary); }

.dialog-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--outline);
  margin: 0 0 0.75rem;
}

/* ── Share dialog ────────────────────────────────── */
#share-dialog {
  max-width: 32rem;
  width: calc(100% - 2rem);
  padding: 1.25rem 1.5rem;
  background: var(--surface-lowest);
  color: var(--on-surface);
  border: 1px solid var(--surface-highest);
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}
#share-dialog::backdrop { background: rgba(0,0,0,0.25); }

.share-url-row {
  display: flex;
  gap: 0.5rem;
}

#share-url-input {
  flex: 1;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.8rem;
  padding: 0.4rem 0.6rem;
  background: var(--surface-low);
  border: none;
  color: var(--on-surface);
}

#share-copy-btn {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.4rem 0.75rem;
  background: var(--primary);
  color: var(--on-primary);
  border: none;
  cursor: pointer;
}
#share-copy-btn:hover { background: var(--primary-container); }

/* ── Reply dialog ────────────────────────────────── */
#reply-dialog {
  max-width: 36rem;
  width: calc(100% - 2rem);
  padding: 1.25rem 1.5rem;
  background: var(--surface-lowest);
  color: var(--on-surface);
  border: 1px solid var(--surface-highest);
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}
#reply-dialog::backdrop { background: rgba(0,0,0,0.25); }

#reply-body {
  width: 100%;
  font-family: 'Newsreader', Georgia, serif;
  font-size: 0.95rem;
  line-height: 1.6;
  padding: 0.6rem;
  background: var(--surface-low);
  border: none;
  color: var(--on-surface);
  resize: vertical;
  margin-bottom: 0.75rem;
}

#reply-submit {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.5rem 1rem;
  background: var(--primary);
  color: var(--on-primary);
  border: none;
  cursor: pointer;
}
#reply-submit:hover { background: var(--primary-container); }
```

---

## Failure modes

| Situation | Behavior |
|-----------|----------|
| `navigator.share` unavailable | Falls back to copy dialog silently |
| `navigator.clipboard` unavailable | Copy button does nothing; URL still visible in input for manual copy |
| No email client configured | `mailto:` link does nothing; accepted limitation |
| `SITE_URL` unset in `.env` | `meta=None` passed to `base()`; OG tags omitted from all pages; local builds unaffected |
| `og:description` body is empty | `og:description` and `twitter:description` tags omitted |
| Body starts with a quoteback | `>` markers stripped; quoted text becomes the description — acceptable |

---

## Out of scope

- Server-side form submission (email sent without opening a mail client).
- Per-entry generated social card images.
- Copy-to-clipboard fallback for browsers without `navigator.clipboard` (selection + prompt is too disruptive).
- Feed-level OG tags (the feed URL is not a shareable "post").
