# notas

Static microblog built from [jrnl](https://jrnl.sh) entries. Paginated feed, full-text search, and bigram heatmap highlighting powered by spaCy.

## Dependencies

```bash
uv sync
uv run python -m spacy download es_core_news_sm
```

## Writing

```bash
jrnl "Primera oración como título. El resto es el cuerpo."
```

Supports inline Markdown. Tags with `@tag`.

## Building

```bash
# export entries
jrnl --export json > entries.json

# build site
uv run build.py

# index for search
uv run python -m pagefind --site dist/
```

Output goes to `dist/`.

## Preview

```bash
python -m http.server 8000 --directory dist/
```

Open `http://localhost:8000`.

## Features

- **Feed** — paginated, newest first, full entry content
- **Permalinks** — `/entry/20260327T143000/`
- **Search** — `/search/` powered by Pagefind, also reads `?q=` from URL
- **Heatmap** — recurring Spanish bigrams highlighted in amber; click to search

## Publishing

```bash
rsync -av dist/ user@host:/var/www/blog/
```

Or push `dist/` to Netlify / GitHub Pages.
