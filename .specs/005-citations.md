# 005 — Citations

## Overview

Academic references in entry bodies are written as `[@citekey]`. At build time each citation is looked up in a CSL-JSON library file, a full formatted reference string is assembled in Python, and the inline marker is replaced with a `<span>` carrying the string as a data attribute. A small JS click handler displays the reference in a `<dialog>` modal. No network requests at runtime. No JSON parsing in the browser.

---

## Writing syntax

Inside any jrnl entry body:

```
The concept was first articulated by [@wolf1982] and later expanded in [@said1978].
```

Syntax: `[@` + citekey + `]`. The citekey matches the `id` field in the CSL-JSON library. No spaces inside brackets.

The raw entry remains readable as plain text if the build step is skipped — the markers render as literal `[@...]` strings.

---

## Library

Path: read from the `LIBRARY_FILE` environment variable at build time.

Format: CSL-JSON array. Each entry has at minimum `id`, `type`, `title`, `author`, and `issued`. Coverage of `DOI`, `ISBN`, and `URL` is partial — see identifier priority below.

The library is read once at build start and held in memory as a dict keyed by `id`. It is never written to.

---

## Pipeline

```
entries.json
  → build.py: load library → {citekey: ref_string}   [new]
  → for each entry body: preprocess_citations()        [new, before quotebacks]
      → replace [@citekey] with <span class="cite" ...>
  → preprocess_quotebacks()                            [existing]
  → annotate_body() / mistune                          [existing]
```

Citation preprocessing runs before quotebacks and before the NLP step so the emitted `<span>` is opaque HTML that mistune and the bigram annotator leave untouched.

---

## Regex

```python
CITATION_RE = re.compile(r'\[@([\w:-]+)\]')
```

Group 1 is the citekey. The character class `[\w:-]` covers all Zotero/Pandoc-style keys (e.g. `wolf1982`, `acosta-marquez2021`, `smith:2010`).

---

## Reference formatting

Formatted in Python at build time. Output is a plain-text string — no HTML markup inside. The modal renders it inside a `<p>`, so no escaping concerns beyond the attribute value itself (handled by Python's `html.escape`).

### Author formatting

```python
def _format_authors(authors: list[dict]) -> str:
    # Each name dict has "family" and/or "given" (literal names use "literal")
    # First author: "Family, Given"
    # Subsequent authors: "Given Family"
    # More than 3 total: "First Author et al."
```

### Year

```python
def _format_year(entry: dict) -> str:
    parts = entry.get("issued", {}).get("date-parts", [[]])
    return str(parts[0][0]) if parts and parts[0] else "s.f."
```

`s.f.` (sine fecha) for entries without a year.

### Identifier priority

DOI → ISBN → URL → none. Shown as a bare string, e.g. `DOI: 10.3390/...` or `ISBN: 978-...`.

### Format per type

| Type | Format |
|------|--------|
| `article-journal` | `Author(s). "Title." Journal vol(issue), year, pp. pages. IDENTIFIER` |
| `book` | `Author(s). Title. Publisher, year. IDENTIFIER` |
| `chapter` | `Author(s). "Title." In Container, ed. Editor(s). Publisher, year, pp. pages. IDENTIFIER` |
| `thesis` | `Author(s). Title. [Thesis]. Publisher, year. IDENTIFIER` |
| `paper-conference` | `Author(s). "Title." Event. Publisher, year. IDENTIFIER` |
| `document` / others | `Author(s). "Title." Publisher, year. IDENTIFIER` |

Book and thesis titles are not quoted (they are the primary work). Article, chapter, and conference paper titles are quoted (they are contained works).

Fields that are absent are omitted silently. The string is always non-empty — at minimum it contains the title.

### Examples

```
Abel, Sarah. "Of African Descent?" Genealogy 2(1), 2018, p. 11. DOI: 10.3390/genealogy2010011

Wolf, Eric. Europa y la gente sin historia. Fondo de Cultura Económica, 1982. ISBN: 978-968-16-1787-0

Acosta Márquez, Eliana. "Relación ancestral y cuidado de la salud del territorio." In Pueblos y territorios frente al tren maya, ed. Giovanna Gasparello; Violeta Núñez Rodríguez. Centro Interdisciplinar para la Investigación de la Recreación, 2021, pp. 245-294.
```

---

## HTML output

```python
def preprocess_citations(text: str, refs: dict[str, str]) -> str:
    def _replace(m):
        key = m.group(1)
        ref = refs.get(key)
        if ref is None:
            return m.group(0)  # unknown key: leave [@citekey] intact
        safe_ref = html.escape(ref, quote=True)
        return f'<span class="cite" data-key="{key}" data-ref="{safe_ref}">[@{key}]</span>'
    return CITATION_RE.sub(_replace, text)
```

Unknown citekeys are left as-is and a warning is printed to stdout at build time.

---

## JavaScript

Added inline to the `base()` template in `src/render.py`, alongside the existing keydown handler.

```js
document.addEventListener("click", e => {
  const cite = e.target.closest(".cite");
  if (!cite) return;
  e.preventDefault();
  let dlg = document.getElementById("cite-dialog");
  if (!dlg) {
    dlg = document.createElement("dialog");
    dlg.id = "cite-dialog";
    dlg.innerHTML = '<button class="cite-close" aria-label="Close">×</button><p id="cite-ref"></p>';
    dlg.querySelector(".cite-close").addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); });
    document.body.appendChild(dlg);
  }
  document.getElementById("cite-ref").textContent = cite.dataset.ref;
  dlg.showModal();
});
```

The `<dialog>` element is created lazily on first use and reused on subsequent clicks. Clicking the backdrop or the × button closes it. `textContent` (not `innerHTML`) is used intentionally — the ref string is plain text.

---

## CSS

Added to `assets/style.css`.

```css
.cite {
  cursor: pointer;
  border-bottom: 1px dotted currentColor;
}

#cite-dialog {
  max-width: 36rem;
  padding: 1.25rem 1.5rem;
  border: 1px solid var(--border, #ccc);
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

#cite-dialog::backdrop {
  background: rgba(0,0,0,0.25);
}

#cite-dialog p {
  margin: 0;
  line-height: 1.6;
  font-size: 0.9rem;
}

.cite-close {
  float: right;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}
```

---

## New file: `src/citations.py`

```python
def load_refs() -> dict[str, str]:
    """Returns {citekey: formatted_ref_string} for all entries in the library.
    Reads the library path from the LIBRARY_FILE environment variable."""
    ...

def preprocess_citations(text: str, refs: dict[str, str]) -> str:
    """Replace [@citekey] spans with <span class="cite"> HTML."""
    ...
```

Public API mirrors `src/quoteback.py` in style. Estimated size: ~90 lines.

---

## Build changes

### `build.py`

```python
from src.citations import load_refs

def main():
    ...
    citation_refs = load_refs()
    build_feed(..., citation_refs=citation_refs)
    build_entries(..., citation_refs=citation_refs)
    ...
```

### `src/render.py`

`entry_body_html` gains a `citation_refs` parameter. `preprocess_citations` runs first, before `preprocess_quotebacks`:

```python
def entry_body_html(entry, bigram_scores=None, quoteback_cache=None, citation_refs=None):
    body = entry.get("body", "").strip()
    if not body:
        return ""
    if citation_refs is not None:
        body = preprocess_citations(body, citation_refs)
    if quoteback_cache is not None:
        body = preprocess_quotebacks(body, quoteback_cache)
    if bigram_scores:
        return annotate_body(body, bigram_scores)
    return md(body)
```

`render_entry_fragment`, `build_feed`, and `build_entries` pass `citation_refs` through.

### `src/render.py` — `base()`

The citation click handler JS is added to the existing `<script>` block at the bottom of the page.

---

## Failure modes

| Situation | Behavior |
|-----------|----------|
| Unknown citekey | Left as `[@citekey]` in output; warning printed to stdout |
| `LIBRARY_FILE` not set or path not found | `load_refs()` raises with a clear message; build aborts |
| Entry missing `title` | Uses `"[no title]"` as fallback |
| Entry missing `author` | Author field omitted from string |
| Entry missing `issued` | Year shown as `s.f.` |
| No identifier (DOI/ISBN/URL) | Identifier field omitted silently |
| `<dialog>` not supported | Not a concern — all modern browsers support it |

---

## Interaction with existing specs

- **003 (Heatmap):** no conflict. Citation spans are HTML before the NLP step runs; bigrams are not injected inside them.
- **004 (Quotebacks):** no conflict. Citations are processed first; a citation inside a blockquote body is resolved before the quoteback regex runs.

---

## Out of scope

- Rendering a formatted bibliography section at the bottom of an entry.
- Supporting multiple citation styles (APA, MLA, etc.) — plain-text with clear fields is sufficient.
- Linking the DOI as a clickable hyperlink inside the modal (the string is copyable as-is).
- Searching entries by citekey.
