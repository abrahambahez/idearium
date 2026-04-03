#!/usr/bin/env python3
import shutil
import subprocess
import tomllib
from pathlib import Path

import frontmatter

from src.citations import load_refs
from src.nlp import compute_ngram_scores
from src.pages import build_assets, build_entries, build_feed, build_media, build_search
from src.quoteback import load_cache, save_cache
from src.render import init_renderer

with open("config.toml", "rb") as f:
    _config = tomllib.load(f)

ENTRIES_DIR = Path(_config["entries"]["dir"])
DIST = Path("dist")
PER_PAGE = 20
SITE_TITLE = "idearium."
SITE_URL = _config["site"]["url"].rstrip("/")
LIBRARY_FILE = _config["site"]["library_file"]
GRAYSCALE = _config.get("media", {}).get("grayscale", True)

init_renderer(GRAYSCALE)


def load_entries() -> list[dict]:
    result = []
    for path in ENTRIES_DIR.glob("*.md"):
        stem = path.stem  # YYYYMMDDTHHMM
        date = f"{stem[0:4]}-{stem[4:6]}-{stem[6:8]}"
        time = f"{stem[9:11]}:{stem[11:13]}"
        post = frontmatter.load(path)
        result.append({
            "title": post.get("title", ""),
            "body": post.content,
            "date": date,
            "time": time,
            "tags": post.get("tags") or [],
            "starred": False,
        })
    return result


def main() -> None:
    entries = sorted(
        load_entries(),
        key=lambda e: f"{e['date']}T{e['time']}",
        reverse=True,
    )

    print("Scoring ngrams…", flush=True)
    ngram_scores = compute_ngram_scores(entries)
    print(f"  {len(ngram_scores)} ngrams scored", flush=True)

    quoteback_cache = load_cache()
    citation_refs = load_refs(LIBRARY_FILE)

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    build_assets(DIST)
    build_media(ENTRIES_DIR, DIST)
    build_feed(entries, ngram_scores, DIST, PER_PAGE, SITE_TITLE, quoteback_cache, citation_refs)
    build_entries(entries, ngram_scores, DIST, SITE_TITLE, quoteback_cache, citation_refs, site_url=SITE_URL)
    build_search(DIST, SITE_TITLE)

    save_cache(quoteback_cache)

    print(f"Built {len(entries)} entries → {DIST}/", flush=True)
    print("Indexing…", flush=True)
    subprocess.run(["uv", "run", "python", "-m", "pagefind", "--site", str(DIST)], check=True)


if __name__ == "__main__":
    main()
