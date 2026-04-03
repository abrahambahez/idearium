# Idearium
Status: Prototype

Python static microblog. Paginated feed, full-text search, and NLP heatmap highlighting powered by spaCy.

## Dependencies

```bash
uv sync
uv run python -m spacy download es_core_news_sm
```

## Configuration

Edit `config.toml`:

```toml
[entries]
dir = "microblog"

[site]
url = "https://example.com"
library_file = "./assets/library.json"

[media]
grayscale = true
```

## Writing

Entries are Markdown files in the configured `entries.dir`, named `YYYYMMDDTHHMM.md`:

```
microblog/20260401T1811.md
```

Each file uses YAML frontmatter:

```markdown
---
title: First sentence as title.
tags:
  - TagName
---

Body text. Supports inline Markdown.
```

## Building

```bash
uv run build.py
```

Builds to `dist/` and runs Pagefind indexing automatically.

## Preview

```bash
python -m http.server 8000 --directory dist/
```

Open `http://localhost:8000`.

## Features

- **Feed** — paginated, newest first, full entry content
- **Permalinks** — `/entry/20260327T143000/`
- **Search** — `/search/` powered by Pagefind, also reads `?q=` from URL
- **Heatmap** — recurring Spanish nouns and noun phrases (monograms + bigrams) highlighted in amber; scored by frequency across entries; click to search
- **Quotebacks** — `[url]` syntax embeds external quotes as styled blockquotes with source attribution
- **Citations** — `[@key]` syntax links to bibliography entries via a BibTeX-style refs file
- **Footnotes** — standard Markdown footnotes rendered inline as hover tooltips (no jump links)
- **Images** — `![alt](YYYYMMDDTHHMM.png "Caption")` co-located with entries; renders with `<figcaption>`; grayscale conversion optional via `config.toml`

## Publishing

```bash
rsync -av dist/ user@host:/var/www/blog/
```

Or push `dist/` to Netlify / GitHub Pages.
