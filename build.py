#!/usr/bin/env python3
import json
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import mistune
import spacy

# --- Config -------------------------------------------------------------------

ENTRIES_FILE = "entries.json"
DIST = Path("dist")
PER_PAGE = 20
SITE_TITLE = "notas"

# --- Helpers ------------------------------------------------------------------

md = mistune.create_markdown(plugins=["strikethrough", "url"], escape=False)
nlp = spacy.load("es_core_news_sm")

MEANINGFUL_POS_PAIRS = {
    ("NOUN", "NOUN"),
    ("NOUN", "ADJ"),
    ("ADJ", "NOUN"),
    ("PROPN", "NOUN"),
    ("PROPN", "PROPN"),
    ("NOUN", "PROPN"),
}
HEATMAP_MIN_ENTRIES = 2


def entry_id(entry: dict) -> str:
    """Normalize jrnl date+time to e.g. 20260327T143000."""
    dt = datetime.fromisoformat(f"{entry['date']}T{entry.get('time', '00:00')}")
    return dt.strftime("%Y%m%dT%H%M%S")


def entry_date_display(entry: dict) -> str:
    dt = datetime.fromisoformat(f"{entry['date']}T{entry.get('time', '00:00')}")
    return dt.strftime("%Y-%m-%d %H:%M")


def entry_title(entry: dict) -> str:
    return entry.get("title", "").strip()


def compute_bigram_scores(entries: list[dict]) -> dict[str, float]:
    """Pass 1: score lemma bigrams by fraction of entries that contain them."""
    total = len(entries)
    # count how many entries contain each lemma bigram
    entry_counts: Counter = Counter()
    for entry in entries:
        body = entry.get("body", "").strip()
        if not body:
            continue
        doc = nlp(body)
        seen = set()
        tokens = [t for t in doc if not t.is_space]
        for a, b in zip(tokens, tokens[1:]):
            if (a.pos_, b.pos_) not in MEANINGFUL_POS_PAIRS:
                continue
            if len(a.lemma_) < 2 or len(b.lemma_) < 2:
                continue
            key = f"{a.lemma_.lower()} {b.lemma_.lower()}"
            if key not in seen:
                seen.add(key)
                entry_counts[key] += 1

    return {
        key: count / total
        for key, count in entry_counts.items()
        if count >= HEATMAP_MIN_ENTRIES
    }


def annotate_body(body: str, bigram_scores: dict[str, float]) -> str:
    """Pass 2: inject <a class="hm"> spans for scored bigrams, then render markdown."""
    if not body or not bigram_scores:
        return md(body) if body else ""

    doc = nlp(body)
    tokens = [t for t in doc if not t.is_space]

    # collect non-overlapping spans to annotate (char start, char end, bigram key)
    spans: list[tuple[int, int, str]] = []
    last_end = -1
    for a, b in zip(tokens, tokens[1:]):
        if (a.pos_, b.pos_) not in MEANINGFUL_POS_PAIRS:
            continue
        key = f"{a.lemma_.lower()} {b.lemma_.lower()}"
        if key not in bigram_scores:
            continue
        start, end = a.idx, b.idx + len(b.text)
        if start < last_end:
            continue  # skip overlapping
        spans.append((start, end, key))
        last_end = end

    if not spans:
        return md(body)

    # reconstruct body with injected <a> tags
    parts: list[str] = []
    cursor = 0
    for start, end, key in spans:
        parts.append(body[cursor:start])
        score = round(bigram_scores[key], 3)
        href = f"/search/?q={quote(key)}"
        original = body[start:end]
        parts.append(f'<a class="hm" style="--s:{score}" href="{href}">{original}</a>')
        cursor = end
    parts.append(body[cursor:])

    return md("".join(parts))


def entry_body_html(entry: dict, bigram_scores: dict[str, float] | None = None) -> str:
    body = entry.get("body", "").strip()
    if not body:
        return ""
    if bigram_scores:
        return annotate_body(body, bigram_scores)
    return md(body)


def entry_tags(entry: dict) -> list[str]:
    return [t.lstrip("@") for t in entry.get("tags", [])]


def slug_path(eid: str) -> Path:
    return DIST / "entry" / eid


# --- CSS ----------------------------------------------------------------------

CSS = """\
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1.05rem;
  line-height: 1.7;
  max-width: 680px;
  margin: 3rem auto;
  padding: 0 1.5rem;
  color: #1a1a1a;
  background: #fafaf8;
}

a { color: #1a1a1a; }
a:hover { color: #555; }

header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid #ddd;
  margin-bottom: 2.5rem;
  padding-bottom: 0.75rem;
}

header h1 { margin: 0; font-size: 1.2rem; font-weight: normal; }
header nav a { margin-left: 1.25rem; font-size: 0.9rem; text-decoration: none; }

.entry { margin-bottom: 3rem; }

.entry-meta {
  font-size: 0.82rem;
  color: #888;
  margin-bottom: 0.4rem;
}

.entry-meta a { color: #888; text-decoration: none; }
.entry-meta a:hover { text-decoration: underline; }

.entry-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0 0 0.5rem;
}

.entry-title a { text-decoration: none; }
.entry-title a:hover { text-decoration: underline; }

.entry-body p:first-child { margin-top: 0; }
.entry-body p:last-child { margin-bottom: 0; }

.tags { margin-top: 0.5rem; font-size: 0.82rem; color: #888; }
.tags a { color: #888; text-decoration: none; }
.tags a:hover { text-decoration: underline; }

.pagination {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  font-size: 0.9rem;
  border-top: 1px solid #ddd;
  padding-top: 1rem;
}

.pagination a { text-decoration: none; }
.pagination .placeholder { visibility: hidden; }

/* Search */
#search-input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-bottom: 1.5rem;
  background: #fff;
}

#search-results .result { margin-bottom: 2rem; }
#search-results .result-title { font-weight: bold; }
#search-results .result-date { font-size: 0.82rem; color: #888; margin-bottom: 0.25rem; }
#search-results mark { background: #fff3a0; padding: 0 2px; }

/* Heatmap */
a.hm {
  background: rgba(234, 179, 8, var(--s));
  border-radius: 2px;
  padding: 0 1px;
  text-decoration: none;
  color: inherit;
}
a.hm:hover { text-decoration: underline; }

/* Command palette */
#cmd-backdrop {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.35);
  z-index: 200;
}
#cmd-backdrop.open { display: block; }

#cmd-palette {
  position: fixed;
  top: 20vh;
  left: 50%;
  transform: translateX(-50%);
  width: min(560px, 90vw);
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  z-index: 201;
  overflow: hidden;
}

#cmd-input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-family: inherit;
  border: none;
  border-bottom: 1px solid #eee;
  outline: none;
  background: #fff;
}

#cmd-results { max-height: 55vh; overflow-y: auto; }

#cmd-results a {
  display: block;
  padding: 0.6rem 1rem;
  text-decoration: none;
  color: #1a1a1a;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.9rem;
}
#cmd-results a:last-child { border-bottom: none; }
#cmd-results a.active,
#cmd-results a:hover { background: #f5f5f0; }
#cmd-results .cmd-date { font-size: 0.78rem; color: #aaa; margin-bottom: 0.1rem; }
#cmd-results mark { background: #fff3a0; padding: 0 2px; }
#cmd-empty { padding: 0.75rem 1rem; color: #aaa; font-size: 0.9rem; }
"""

# --- Base template ------------------------------------------------------------


def base(title: str, body: str, *, active: str = "") -> str:
    search_active = 'class="active"' if active == "search" else ""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {SITE_TITLE}</title>
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header>
  <h1><a href="/">{SITE_TITLE}</a></h1>
  <nav>
    <a href="/" {"class=\"active\"" if active == "feed" else ""}>feed</a>
    <a href="/search/" {search_active}>search</a>
  </nav>
</header>
{body}

<div id="cmd-backdrop">
  <div id="cmd-palette">
    <input id="cmd-input" type="search" placeholder="Buscar…" autocomplete="off">
    <div id="cmd-results"></div>
  </div>
</div>

<script>
(function() {{
  let pf = null;
  async function getPagefind() {{
    if (!pf) {{ pf = await import("/pagefind/pagefind.js"); await pf.init(); }}
    return pf;
  }}

  const backdrop = document.getElementById("cmd-backdrop");
  const input = document.getElementById("cmd-input");
  const results = document.getElementById("cmd-results");
  let activeIdx = -1;

  function open() {{
    backdrop.classList.add("open");
    input.value = "";
    results.innerHTML = "";
    activeIdx = -1;
    input.focus();
    getPagefind();
  }}

  function close() {{
    backdrop.classList.remove("open");
    activeIdx = -1;
  }}

  function setActive(idx) {{
    const links = results.querySelectorAll("a");
    links.forEach(l => l.classList.remove("active"));
    activeIdx = Math.max(0, Math.min(idx, links.length - 1));
    if (links[activeIdx]) links[activeIdx].classList.add("active");
  }}

  async function search() {{
    const q = input.value.trim();
    results.innerHTML = "";
    activeIdx = -1;
    if (!q) return;
    const engine = await getPagefind();
    const r = await engine.search(q);
    if (!r.results.length) {{
      results.innerHTML = '<div id="cmd-empty">Sin resultados</div>';
      return;
    }}
    for (const hit of r.results.slice(0, 8)) {{
      const data = await hit.data();
      const a = document.createElement("a");
      a.href = data.url;
      a.innerHTML = `<div class="cmd-date">${{data.meta?.date ?? ""}}</div><div>${{data.meta?.title ?? data.url}}</div>`;
      a.addEventListener("click", close);
      results.appendChild(a);
    }}
  }}

  input.addEventListener("input", search);

  input.addEventListener("keydown", e => {{
    const links = results.querySelectorAll("a");
    if (e.key === "ArrowDown") {{ e.preventDefault(); setActive(activeIdx + 1); }}
    else if (e.key === "ArrowUp") {{ e.preventDefault(); setActive(activeIdx - 1); }}
    else if (e.key === "Enter" && links[activeIdx]) {{ links[activeIdx].click(); }}
    else if (e.key === "Escape") {{ close(); }}
  }});

  backdrop.addEventListener("mousedown", e => {{
    if (e.target === backdrop) close();
  }});

  document.addEventListener("keydown", e => {{
    if ((e.metaKey || e.ctrlKey) && e.key === "k") {{ e.preventDefault(); open(); }}
    else if (e.key === "/" && document.activeElement.tagName !== "INPUT") {{ e.preventDefault(); open(); }}
  }});
}})();
</script>
</body>
</html>
"""


# --- Entry fragment -----------------------------------------------------------


def render_entry_fragment(
    entry: dict,
    *,
    link_title: bool = True,
    bigram_scores: dict[str, float] | None = None,
    indexable: bool = False,
) -> str:
    eid = entry_id(entry)
    date = entry_date_display(entry)
    title = entry_title(entry)
    body_html = entry_body_html(entry, bigram_scores)
    tags = entry_tags(entry)

    title_html = (
        f'<a href="/entry/{eid}/">{title}</a>' if link_title else title
    )
    tags_html = (
        "".join(f'<span class="tag">#{t}</span> ' for t in tags)
        if tags
        else ""
    )

    pf_body = ' data-pagefind-body' if indexable else ''
    pf_ignore = ' data-pagefind-ignore' if indexable else ''
    pf_meta_date = ' data-pagefind-meta="date"' if indexable else ''
    pf_meta_title = ' data-pagefind-meta="title"' if indexable else ''

    title_html_block = (
        f'<p class="entry-title"{pf_ignore}><span{pf_meta_title}>{title_html}</span></p>'
        if title else ""
    )
    tags_html_block = (
        f'<div class="tags"{pf_ignore}>{tags_html}</div>'
        if tags_html else ""
    )

    return f"""\
<article class="entry"{pf_body}>
  <div class="entry-meta"{pf_ignore}>
    <a href="/entry/{eid}/"{pf_meta_date}>{date}</a>
  </div>
  {title_html_block}
  <div class="entry-body">{body_html}</div>
  {tags_html_block}
</article>
"""


# --- Pages --------------------------------------------------------------------


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_feed(entries: list[dict], bigram_scores: dict[str, float]) -> None:
    total = len(entries)
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)

    for page_num in range(1, total_pages + 1):
        chunk = entries[(page_num - 1) * PER_PAGE : page_num * PER_PAGE]
        fragments = "\n".join(
            render_entry_fragment(e, bigram_scores=bigram_scores) for e in chunk
        )

        prev_link = (
            f'<a href="{"/page/" + str(page_num - 1) + "/" if page_num > 2 else "/"}">← newer</a>'
            if page_num > 1
            else '<span class="placeholder">←</span>'
        )
        next_link = (
            f'<a href="/page/{page_num + 1}/">older →</a>'
            if page_num < total_pages
            else '<span class="placeholder">→</span>'
        )

        pagination = f'<nav class="pagination">{prev_link}{next_link}</nav>'
        body = fragments + pagination

        if page_num == 1:
            out = DIST / "index.html"
        else:
            out = DIST / "page" / str(page_num) / "index.html"

        write(out, base(SITE_TITLE, body, active="feed"))


def build_entries(entries: list[dict], bigram_scores: dict[str, float]) -> None:
    for entry in entries:
        eid = entry_id(entry)
        fragment = render_entry_fragment(entry, link_title=False, bigram_scores=bigram_scores, indexable=True)
        back = '<p style="font-size:0.85rem"><a href="/">← feed</a></p>'
        write(
            slug_path(eid) / "index.html",
            base(entry_title(entry) or eid, back + fragment),
        )


def build_search() -> None:
    body = """\
<h2 style="font-size:1rem;font-weight:normal;margin-bottom:1rem">Search</h2>
<input id="search-input" type="search" placeholder="Search entries…" autofocus>
<div id="search-results"></div>
<script>
  async function loadPagefind() {
    const pf = await import("/pagefind/pagefind.js");
    await pf.init();
    const input = document.getElementById("search-input");
    const results = document.getElementById("search-results");

    async function search() {
      const q = input.value.trim();
      results.innerHTML = "";
      if (!q) return;
      const r = await pf.search(q);
      for (const result of r.results) {
        const data = await result.data();
        const div = document.createElement("div");
        div.className = "result";
        div.innerHTML = `
          <div class="result-date">${data.meta?.date ?? ""}</div>
          <div class="result-title"><a href="${data.url}">${data.meta?.title ?? data.url}</a></div>
          <div>${data.excerpt}</div>
        `;
        results.appendChild(div);
      }
    }

    input.addEventListener("input", search);
    const params = new URLSearchParams(window.location.search);
    if (params.get("q")) { input.value = params.get("q"); search(); }
  }
  loadPagefind();
</script>
"""
    write(DIST / "search" / "index.html", base("Search", body, active="search"))


def build_assets() -> None:
    assets = DIST / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "style.css").write_text(CSS, encoding="utf-8")


# --- Main ---------------------------------------------------------------------


def main() -> None:
    with open(ENTRIES_FILE, encoding="utf-8") as f:
        data = json.load(f)

    entries = sorted(
        data["entries"],
        key=lambda e: f"{e['date']}T{e.get('time', '00:00')}",
        reverse=True,
    )

    print("Scoring bigrams…", flush=True)
    bigram_scores = compute_bigram_scores(entries)
    print(f"  {len(bigram_scores)} bigrams scored", flush=True)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    build_assets()
    build_feed(entries, bigram_scores)
    build_entries(entries, bigram_scores)
    build_search()

    print(f"Built {len(entries)} entries → {DIST}/", flush=True)
    print("Indexing…", flush=True)
    subprocess.run(["uv", "run", "python", "-m", "pagefind", "--site", str(DIST)], check=True)


if __name__ == "__main__":
    main()
