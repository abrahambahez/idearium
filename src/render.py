from datetime import datetime
from urllib.parse import quote

import mistune

from src.nlp import MEANINGFUL_POS_PAIRS, nlp
from src.quoteback import preprocess_quotebacks

md = mistune.create_markdown(plugins=["strikethrough", "url"], escape=False)


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
    return [t.lstrip("@") for t in entry.get("tags", [])]


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


def entry_body_html(
    entry: dict,
    bigram_scores: dict[str, float] | None = None,
    quoteback_cache: dict | None = None,
) -> str:
    body = entry.get("body", "").strip()
    if not body:
        return ""
    if quoteback_cache is not None:
        body = preprocess_quotebacks(body, quoteback_cache)
    if bigram_scores:
        return annotate_body(body, bigram_scores)
    return md(body)


def render_entry_fragment(
    entry: dict,
    *,
    link_title: bool = True,
    bigram_scores: dict[str, float] | None = None,
    quoteback_cache: dict | None = None,
    indexable: bool = False,
) -> str:
    eid = entry_id(entry)
    date = entry_date_display(entry)
    title = entry_title(entry)
    body_html = entry_body_html(entry, bigram_scores, quoteback_cache)
    tags = entry_tags(entry)

    title_html = f'<a href="/entry/{eid}/">{title}</a>' if link_title else title
    tags_html = "".join(f'<span class="tag">#{t}</span> ' for t in tags) if tags else ""

    pf_body = ' data-pagefind-body' if indexable else ''
    pf_ignore = ' data-pagefind-ignore' if indexable else ''
    pf_meta_date = ' data-pagefind-meta="date"' if indexable else ''
    pf_meta_title = ' data-pagefind-meta="title"' if indexable else ''

    title_html_block = (
        f'<p class="entry-title"{pf_ignore}><span{pf_meta_title}>{title_html}</span></p>'
        if title else ""
    )
    tags_html_block = f'<div class="tags"{pf_ignore}>{tags_html}</div>' if tags_html else ""

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


def base(title: str, body: str, *, site_title: str, active: str = "") -> str:
    feed_active = 'class="active"' if active == "feed" else ""
    search_active = 'class="active"' if active == "search" else ""
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {site_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,700;1,6..72,400&family=Space+Grotesk:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/style.css">
  <script src="/assets/quoteback.js"></script>
</head>
<body>
<header>
  <h1><a href="/">{site_title}</a></h1>
  <nav>
    <a href="/" {feed_active}>feed</a>
    <a href="/search/" {search_active}>search</a>
  </nav>
</header>
{body}

<script>
document.addEventListener("keydown", e => {{
  if ((e.metaKey || e.ctrlKey) && e.key === "k") {{ e.preventDefault(); window.location.href = "/search/"; }}
  else if (e.key === "/" && document.activeElement.tagName !== "INPUT") {{ e.preventDefault(); window.location.href = "/search/"; }}
}});
</script>
</body>
</html>
"""
