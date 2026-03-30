from pathlib import Path

from src.render import base, entry_id, entry_title, render_entry_fragment


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_feed(
    entries: list[dict],
    bigram_scores: dict[str, float],
    dist: Path,
    per_page: int,
    site_title: str,
    quoteback_cache: dict | None = None,
) -> None:
    total = len(entries)
    total_pages = max(1, (total + per_page - 1) // per_page)

    for page_num in range(1, total_pages + 1):
        chunk = entries[(page_num - 1) * per_page : page_num * per_page]
        fragments = "\n".join(
            render_entry_fragment(e, bigram_scores=bigram_scores, quoteback_cache=quoteback_cache)
            for e in chunk
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

        pagination = f'<nav class="pagination">{prev_link}{next_link}</nav>' if total_pages > 1 else ''
        out = dist / "index.html" if page_num == 1 else dist / "page" / str(page_num) / "index.html"
        write(out, base(site_title, fragments + pagination, site_title=site_title, active="feed"))


def build_entries(
    entries: list[dict],
    bigram_scores: dict[str, float],
    dist: Path,
    site_title: str,
    quoteback_cache: dict | None = None,
) -> None:
    for entry in entries:
        eid = entry_id(entry)
        fragment = render_entry_fragment(
            entry, link_title=False, bigram_scores=bigram_scores,
            quoteback_cache=quoteback_cache, indexable=True
        )
        back = '<p style="font-size:0.85rem"><a href="/">← feed</a></p>'
        write(
            dist / "entry" / eid / "index.html",
            base(entry_title(entry) or eid, back + fragment, site_title=site_title),
        )


def build_search(dist: Path, site_title: str) -> None:
    body = """\
<h2 class="search-page-title">Search</h2>
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
    write(dist / "search" / "index.html", base("Search", body, site_title=site_title, active="search"))


def build_assets(dist: Path) -> None:
    src_assets = Path(__file__).parent.parent / "assets"
    assets_dir = dist / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "style.css").write_text(
        (src_assets / "style.css").read_text(encoding="utf-8"), encoding="utf-8"
    )
    import shutil
    shutil.copy(src_assets / "quoteback.js", assets_dir / "quoteback.js")
