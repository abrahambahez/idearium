#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

from src.nlp import compute_bigram_scores
from src.pages import build_assets, build_entries, build_feed, build_search
from src.quoteback import load_cache, save_cache

ENTRIES_FILE = "entries.json"
DIST = Path("dist")
PER_PAGE = 20
SITE_TITLE = "notas"


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

    quoteback_cache = load_cache()

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    build_assets(DIST)
    build_feed(entries, bigram_scores, DIST, PER_PAGE, SITE_TITLE, quoteback_cache)
    build_entries(entries, bigram_scores, DIST, SITE_TITLE, quoteback_cache)
    build_search(DIST, SITE_TITLE)

    save_cache(quoteback_cache)

    print(f"Built {len(entries)} entries → {DIST}/", flush=True)
    print("Indexing…", flush=True)
    subprocess.run(["uv", "run", "python", "-m", "pagefind", "--site", str(DIST)], check=True)


if __name__ == "__main__":
    main()
