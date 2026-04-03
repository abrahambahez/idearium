# 010 — Image Support

## Goal
Allow entries in `microblog/` to include images placed by Obsidian, automatically optimized to WebP at build time and served at correct absolute paths.

## File Structure

```
microblog/
  20260401T1829.md
  media/              ← Obsidian drops images here
    photo.jpg
    diagram.png

dist/
  media/              ← optimized output
    photo.webp
    diagram.webp
```

## Changes

**`build.py`**
- After `build_assets()`, call `build_media(ENTRIES_DIR, DIST)`

**`src/pages.py` — new `build_media(entries_dir, dist)`**
- If `entries_dir/media/` doesn't exist, no-op
- For each image in `microblog/media/`: convert to WebP via Pillow, write to `dist/media/{stem}.webp`
- Skip files that aren't images (unsupported formats)

**`src/render.py` — path rewriting in markdown output**
- After markdown → HTML conversion, rewrite `src="media/{name}.{ext}"` → `src="/media/{name}.webp"`
- Covers standard markdown `![alt](media/photo.jpg)` syntax
- Obsidian wikilinks `![[photo.jpg]]` are out of scope — use standard markdown syntax

## Config

New key in `config.toml`:

```toml
[media]
grayscale = true   # apply black & white filter to all images by default
```

Read in `build.py`, passed down to `build_media()` and the render layer.

---

## Styling

### Semantic HTML output

Markdown `![alt text](media/photo.jpg "Caption printed here")` renders as:

```html
<figure>
  <img src="/media/photo.webp" alt="alt text">
  <figcaption>Caption printed here</figcaption>
</figure>
```

If no title is provided, `<figcaption>` is omitted entirely.

The render layer must produce `<figure>` instead of a bare `<img>`. This requires either a custom markdown renderer or a post-processing pass on the HTML output.

### CSS definitions

Consistent with the design system (DESIGN.md):

```css
/* Figure — editorial block, Tufte-style */
figure {
  margin: 2.5rem 0;
}

/* Image — paper photograph sitting on the page */
figure img {
  display: block;
  width: 100%;
  box-shadow:
    0 2px 8px rgba(26, 26, 26, 0.10),
    0 8px 32px rgba(26, 26, 26, 0.07);
}

/* Caption — Newsreader small-caps, consistent with metadata labels */
figcaption {
  margin-top: 0.5rem;
  font-family: 'Newsreader', serif;
  font-variant-caps: all-small-caps;
  font-size: 0.75rem;
  color: var(--outline);
  letter-spacing: 0.04em;
}

/* Grayscale — applied when config media.grayscale = true */
figure img.img-grayscale {
  filter: grayscale(1);
}
```

### Design rationale

| Decision | Reason |
|---|---|
| Two-layer shadow (`0 2px 8px` + `0 8px 32px`) | Simulates physical photograph on desk — near shadow gives cut-edge lift, wide ambient gives room depth. Stronger than blockquotes (0.04) but same warm tone formula |
| No border radius | Absolute rule from design system |
| No ghost border on image | Shadow provides sufficient separation; ghost border reserved for white cards on canvas |
| Grayscale filter via CSS class | Config baked at build time into each `<img>`; no JS toggle needed. Class on `<img>`, not `<figure>`, so it doesn't affect the caption |
| `figcaption` uses Newsreader small-caps | Consistent with all metadata/label contexts in the system |
| Dark mode | Shadow formula uses `rgba(26,26,26,x)` — same warm ink tone already inverts naturally with `--surface` token changes. No extra dark mode rules needed |

## Dependency

- Add `Pillow` to `pyproject.toml`

## Out of Scope

- `srcset` / responsive sizes
- AVIF output
- Blur placeholders
- Wikilink `![[...]]` syntax support
- Subdirectories inside `media/`
