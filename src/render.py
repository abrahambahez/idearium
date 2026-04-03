import html as _html
import re
from datetime import datetime
from pathlib import Path as _Path
from urllib.parse import quote

import mistune
from mistune.util import escape as _escape_text
from mistune.util import safe_entity as _safe_entity
from mistune.util import striptags as _striptags

from src.citations import preprocess_citations
from src.nlp import MEANINGFUL_POS, MEANINGFUL_POS_PAIRS, nlp
from src.quoteback import preprocess_quotebacks


class _ImageRenderer(mistune.HTMLRenderer):
    def __init__(self, grayscale: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._grayscale = grayscale

    def image(self, text: str, url: str, title: str | None = None) -> str:
        is_relative = not url.startswith(("http://", "https://", "/", "data:"))
        src = f"/media/{_Path(url).stem}.webp" if is_relative else self.safe_url(url)
        alt = _escape_text(_striptags(text))
        cls = ' class="img-grayscale"' if self._grayscale else ""
        img = f'<img src="{src}" alt="{alt}"{cls}>'
        if title:
            return f"<figure>{img}<figcaption>{_safe_entity(title)}</figcaption></figure>"
        return f"<figure>{img}</figure>"


def _make_md(grayscale: bool):
    renderer = _ImageRenderer(grayscale=grayscale, escape=False)
    return mistune.create_markdown(renderer=renderer, plugins=["strikethrough", "url", "footnotes"])


md = _make_md(False)


def init_renderer(grayscale: bool) -> None:
    global md
    md = _make_md(grayscale)

ICON_SHARE = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>'
ICON_MAIL  = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'


def entry_id(entry: dict) -> str:
    """Normalize jrnl date+time to e.g. 20260327T143000."""
    dt = datetime.fromisoformat(f"{entry['date']}T{entry.get('time', '00:00')}")
    return dt.strftime("%Y%m%dT%H%M%S")


def entry_date_display(entry: dict) -> str:
    dt = datetime.fromisoformat(f"{entry['date']}T{entry.get('time', '00:00')}")
    return dt.strftime("%Y-%m-%d %H:%M")


def entry_title(entry: dict) -> str:
    return entry.get("title", "").strip()


def entry_tags(entry: dict) -> list[str]:
    return [t.lstrip("#@") for t in entry.get("tags", [])]


def annotate_body(body: str, bigram_scores: dict[str, float]) -> str:
    """Pass 2: inject <a class="hm"> spans for scored bigrams, then render markdown."""
    if not body or not bigram_scores:
        return md(body) if body else ""

    doc = nlp(body)
    tokens = [t for t in doc if not t.is_space]

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
            continue
        spans.append((start, end, key))
        last_end = end

    bigram_ranges = [(s, e) for s, e, _ in spans]
    for t in tokens:
        if t.pos_ not in MEANINGFUL_POS:
            continue
        key = t.lemma_.lower()
        if key not in bigram_scores:
            continue
        start, end = t.idx, t.idx + len(t.text)
        if any(s <= start < e or s < end <= e for s, e in bigram_ranges):
            continue
        spans.append((start, end, key))

    spans.sort(key=lambda x: x[0])

    if not spans:
        return md(body)

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


def _inline_footnotes(html: str) -> str:
    section = re.search(r'<section class="footnotes">.*?</section>', html, re.DOTALL)
    if not section:
        return html
    notes = {}
    for m in re.finditer(r'<li id="fn-(\d+)"><p>(.*?)<a href="#fnref-\1"', section.group(), re.DOTALL):
        notes[m.group(1)] = m.group(2).strip()
    def _replace(m):
        content = _html.escape(notes.get(m.group(1), ""), quote=True)
        return f'<sup class="fn-ref" data-note="{content}">{m.group(1)}</sup>'
    result = re.sub(
        r'<sup class="footnote-ref" id="fnref-(\d+)"><a href="#fn-\1">\d+</a></sup>',
        _replace,
        html[:section.start()],
    )
    return result + html[section.end():]


def entry_body_html(
    entry: dict,
    bigram_scores: dict[str, float] | None = None,
    quoteback_cache: dict | None = None,
    citation_refs: dict[str, str] | None = None,
) -> str:
    body = entry.get("body", "").strip()
    if not body:
        return ""
    if citation_refs is not None:
        body = preprocess_citations(body, citation_refs)
    if quoteback_cache is not None:
        body = preprocess_quotebacks(body, quoteback_cache)
    result = annotate_body(body, bigram_scores) if bigram_scores else md(body)
    return _inline_footnotes(result)


def render_entry_footer(eid: str, title: str) -> str:
    subject = f"Comentario a {title} ({eid})" if title else f"Comentario ({eid})"
    return (
        f'<div class="entry-footer">'
        f'<button class="entry-action" data-action="share"'
        f' data-url="/entry/{eid}/"'
        f' data-title="{_html.escape(title or eid)}">'
        f'{ICON_SHARE} Compartir</button>'
        f'<button class="entry-action" data-action="reply"'
        f' data-subject="{_html.escape(subject)}">'
        f'{ICON_MAIL} Responder</button>'
        f'</div>'
    )


def _render_og_tags(meta: dict) -> str:
    lines = [
        f'<meta property="og:type" content="article">',
        f'<meta property="og:title" content="{_html.escape(meta["og_title"])}">',
        f'<meta property="og:url" content="{_html.escape(meta["url"])}">',
        f'<meta property="og:image" content="{_html.escape(meta["image"])}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{_html.escape(meta["og_title"])}">',
        f'<meta name="twitter:image" content="{_html.escape(meta["image"])}">',
    ]
    if meta.get("description"):
        desc = _html.escape(meta["description"])
        lines += [
            f'<meta property="og:description" content="{desc}">',
            f'<meta name="twitter:description" content="{desc}">',
        ]
    return "\n  ".join(lines)


def render_entry_fragment(
    entry: dict,
    *,
    link_title: bool = True,
    bigram_scores: dict[str, float] | None = None,
    quoteback_cache: dict | None = None,
    citation_refs: dict[str, str] | None = None,
    indexable: bool = False,
) -> str:
    eid = entry_id(entry)
    date = entry_date_display(entry)
    title = entry_title(entry)
    body_html = entry_body_html(entry, bigram_scores, quoteback_cache, citation_refs)
    tags = entry_tags(entry)

    title_html = f'<a href="/entry/{eid}/">{title}</a>' if link_title else title
    tags_html = "".join(
        f'<a class="tag" href="/search/?q={quote("#" + t)}" data-pagefind-filter="tag:{t}">#{t}</a> '
        for t in tags
    ) if tags else ""

    pf_body = ' data-pagefind-body' if indexable else ''
    pf_ignore = ' data-pagefind-ignore' if indexable else ''
    pf_meta_date = ' data-pagefind-meta="date"' if indexable else ''
    pf_meta_title = ' data-pagefind-meta="title"' if indexable else ''

    title_html_block = (
        f'<p class="entry-title"><span{pf_meta_title}>{title_html}</span></p>'
        if title else ""
    )
    tags_html_block = f'<div class="tags">{tags_html}</div>' if tags_html else ""
    footer_html = render_entry_footer(eid, title)

    return f"""\
<article class="entry feed-entry"{pf_body}>
  <div class="entry-meta"{pf_ignore}>
    <a href="/entry/{eid}/"{pf_meta_date}>{date}</a>
  </div>
  {title_html_block}
  <div class="entry-body">{body_html}</div>
  {tags_html_block}
  {footer_html}
</article>
"""


def base(title: str, body: str, *, site_title: str, active: str = "", meta: dict | None = None) -> str:
    feed_active = 'class="active"' if active == "feed" else ""
    search_active = 'class="active"' if active == "search" else ""
    og_tags = "\n  " + _render_og_tags(meta) if meta else ""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {site_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,700;1,6..72,400&family=Space+Grotesk:wght@400;700&display=swap" as="style">
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,700;1,6..72,400&family=Space+Grotesk:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css">{og_tags}
  <script src="/assets/quoteback.js"></script>
</head>
<body>
<header>
  <h1><a href="/">{site_title}</a></h1>
  <nav>
    <a href="/" {feed_active}>Inicio</a>
    <a href="/search/" {search_active}>Buscar</a>
  </nav>
</header>
{body}

<footer>
  <p>Impreso en el vacío digital.<br>Escrito por un humano ✌🏽</p>
  <p><a href="https://creativecommons.org/licenses/by-sa/4.0/">🄯 CC BY-SA 4.0</a></p>
  <div class="footer-links">
    <a href="https://sergio-barrera.com">Creado por Sergio Barrera</a>
    <a href="mailto:hi@sergio-barrera.com">hi@sergio-barrera.com</a>
  </div>
</footer>

<script>
document.querySelectorAll('.entry-body a[href^="http"]').forEach(a => {{
  a.target = "_blank";
  a.rel = "noopener noreferrer";
}});
document.addEventListener("keydown", e => {{
  if ((e.metaKey || e.ctrlKey) && e.key === "k") {{ e.preventDefault(); window.location.href = "/search/"; }}
  else if (e.key === "/" && document.activeElement.tagName !== "INPUT") {{ e.preventDefault(); window.location.href = "/search/"; }}
}});
document.addEventListener("click", e => {{
  const ref = e.target.closest(".fn-ref");
  if (ref) {{
    let dlg = document.getElementById("fn-dialog");
    if (!dlg) {{
      dlg = document.createElement("dialog");
      dlg.id = "fn-dialog";
      dlg.innerHTML = '<button class="dialog-close" aria-label="Cerrar">\u00d7</button><div id="fn-content"></div>';
      dlg.querySelector(".dialog-close").addEventListener("click", () => dlg.close());
      dlg.addEventListener("click", e => {{ if (e.target === dlg) dlg.close(); }});
      document.body.appendChild(dlg);
    }}
    document.getElementById("fn-content").innerHTML = ref.dataset.note;
    dlg.showModal();
  }}
}});
document.addEventListener("click", e => {{
  const cite = e.target.closest(".cite");
  if (!cite) return;
  e.preventDefault();
  let dlg = document.getElementById("cite-dialog");
  if (!dlg) {{
    dlg = document.createElement("dialog");
    dlg.id = "cite-dialog";
    dlg.innerHTML = '<button class="cite-close" aria-label="Close">\u00d7</button><div id="cite-ref"></div>';
    dlg.querySelector(".cite-close").addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", e => {{ if (e.target === dlg) dlg.close(); }});
    document.body.appendChild(dlg);
  }}
  const container = document.getElementById("cite-ref");
  container.innerHTML = "";
  JSON.parse(cite.dataset.refs).forEach(r => {{
    const p = document.createElement("p");
    p.textContent = r;
    container.appendChild(p);
  }});
  dlg.showModal();
}});
document.addEventListener("click", e => {{
  const btn = e.target.closest(".entry-action");
  if (!btn) return;
  if (btn.dataset.action === "share") {{
    const url = new URL(btn.dataset.url, location.origin).href;
    if (navigator.share) {{ navigator.share({{ title: btn.dataset.title, url }}); return; }}
    let dlg = document.getElementById("share-dialog");
    if (!dlg) {{
      dlg = document.createElement("dialog");
      dlg.id = "share-dialog";
      dlg.innerHTML = '<button class="dialog-close" aria-label="Cerrar">\u00d7</button><span class="dialog-label">Enlace</span><input id="share-url-input" class="dialog-input" type="text" readonly><button id="share-copy-btn" class="dialog-action">Copiar</button>';
      dlg.querySelector(".dialog-close").addEventListener("click", () => dlg.close());
      dlg.addEventListener("click", e => {{ if (e.target === dlg) dlg.close(); }});
      dlg.querySelector("#share-copy-btn").addEventListener("click", () => {{
        navigator.clipboard.writeText(document.getElementById("share-url-input").value);
        const b = document.getElementById("share-copy-btn");
        b.textContent = "Copiado \u2713";
        setTimeout(() => b.textContent = "Copiar", 2000);
      }});
      document.body.appendChild(dlg);
    }}
    document.getElementById("share-url-input").value = url;
    dlg.showModal();
  }}
  if (btn.dataset.action === "reply") {{
    let dlg = document.getElementById("reply-dialog");
    if (!dlg) {{
      dlg = document.createElement("dialog");
      dlg.id = "reply-dialog";
      dlg.innerHTML = '<button class="dialog-close" aria-label="Cerrar">\u00d7</button><span class="dialog-label" id="reply-subject-display"></span><textarea id="reply-body" class="dialog-textarea" rows="6" placeholder="Tu mensaje\u2026"></textarea><button id="reply-submit" class="dialog-action">Abrir correo \u2192</button>';
      dlg.querySelector(".dialog-close").addEventListener("click", () => dlg.close());
      dlg.addEventListener("click", e => {{ if (e.target === dlg) dlg.close(); }});
      dlg.querySelector("#reply-submit").addEventListener("click", () => {{
        const s = encodeURIComponent(document.getElementById("reply-subject-display").dataset.subject);
        const b = encodeURIComponent(document.getElementById("reply-body").value);
        window.location.href = "mailto:hi@sergio-barrera.com?subject=" + s + "&body=" + b;
        dlg.close();
      }});
      document.body.appendChild(dlg);
    }}
    document.getElementById("reply-subject-display").dataset.subject = btn.dataset.subject;
    document.getElementById("reply-subject-display").textContent = btn.dataset.subject;
    document.getElementById("reply-body").value = "";
    dlg.showModal();
  }}
}});
</script>
</body>
</html>
"""
