#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

import frontmatter
from dotenv import load_dotenv

load_dotenv()

from src.citations import load_refs
from src.nlp import compute_bigram_scores
from src.pages import build_assets, build_entries, build_feed, build_search
from src.quoteback import load_cache, save_cache

ENTRIES_DIR = Path("entries")
DIST = Path("dist")
PER_PAGE = 20
SITE_TITLE = "idearium."
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")


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

    print("Scoring bigrams…", flush=True)
    bigram_scores = compute_bigram_scores(entries)
    print(f"  {len(bigram_scores)} bigrams scored", flush=True)

    quoteback_cache = load_cache()
    citation_refs = load_refs()

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    build_assets(DIST)
    build_feed(entries, bigram_scores, DIST, PER_PAGE, SITE_TITLE, quoteback_cache, citation_refs)
    build_entries(entries, bigram_scores, DIST, SITE_TITLE, quoteback_cache, citation_refs, site_url=SITE_URL)
    build_search(DIST, SITE_TITLE)

    save_cache(quoteback_cache)

    print(f"Built {len(entries)} entries → {DIST}/", flush=True)
    print("Indexing…", flush=True)
    subprocess.run(["uv", "run", "python", "-m", "pagefind", "--site", str(DIST)], check=True)


if __name__ == "__main__":
    main()
