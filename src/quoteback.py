import json
import re
from html.parser import HTMLParser
from pathlib import Path

import httpx

CACHE_FILE = Path("quoteback_cache.json")

# Matches a markdown blockquote block whose attribution line is either:
#   > -- [Title](url)   (form A — inline title, no fetch needed)
#   > -- https://...    (form B — bare URL, title fetched at build time)
QUOTEBACK_RE = re.compile(
    r'((?:^>[ \t]*.+\n)+?)'
    r'^>[ \t]*--[ \t]+'
    r'(?:'
        r'\[([^\]]+)\]\((https?://[^)]+)\)'
        r'|'
        r'(https?://\S+)'
    r')[ \t]*$',
    re.MULTILINE,
)


class _HeadParser(HTMLParser):
    """Extract title and author from <head> only."""

    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.author: str = ""
        self._in_title = False
        self._done = False

    def handle_starttag(self, tag, attrs):
        if self._done:
            return
        attr = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attr.get("name", "").lower()
            prop = attr.get("property", "").lower()
            content = attr.get("content", "")
            if name == "author" and not self.author:
                self.author = content
            elif prop == "og:site_name" and not self.author:
                self.author = content

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "head":
            self._done = True

    def handle_data(self, data):
        if self._in_title and not self._done:
            self.title += data


def _parse_head(html: str) -> dict:
    parser = _HeadParser()
    # Only feed up to </head> to avoid parsing large bodies
    head_end = html.lower().find("</head>")
    parser.feed(html[:head_end + 7] if head_end != -1 else html[:4096])
    return {"title": parser.title.strip(), "author": parser.author.strip()}


def fetch_metadata(url: str) -> dict:
    """Fetch page title and author. Returns {} on any failure."""
    try:
        r = httpx.get(
            url,
            timeout=8,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        r.raise_for_status()
    except Exception as exc:
        print(f"  [quoteback] fetch failed for {url}: {exc}", flush=True)
        return {}
    return _parse_head(r.text)


def load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _resolve(match: re.Match, cache: dict) -> str:
    raw_lines = match.group(1)
    inline_title = match.group(2)
    url = match.group(3) or match.group(4)

    body = re.sub(r"^>[ \t]?", "", raw_lines, flags=re.MULTILINE).strip()

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
        f"{body}"
        f'<footer>— <cite><a href="{url}">{title}</a></cite></footer>'
        f"</blockquote>\n\n"
    )


def preprocess_quotebacks(text: str, cache: dict) -> str:
    """Replace quoteback syntax blocks with <blockquote class="quoteback"> HTML."""
    return QUOTEBACK_RE.sub(lambda m: _resolve(m, cache), text)
