# 003 — Heatmap Highlighting

## Overview

Recurring bigrams (two-word phrases) in entry bodies are highlighted at build time with an amber background scaled to how often the phrase appears across the archive. Clicking a highlighted phrase navigates to the search page for that query.

spaCy is used for Spanish lemmatization and POS tagging, ensuring morphological variants count together and only linguistically meaningful phrases are highlighted. All processing is build-time — no JS required for the heatmap itself.

---

## Pipeline

```
entries.json
  → spaCy (lemmatize + POS tag all entry bodies)          [pass 1]
  → compute bigram scores                                  [pass 1]
  → for each entry: inject <a> spans into raw markdown     [pass 2]
  → mistune renders annotated markdown → HTML              [pass 2]
```

No `wordmap.json` emitted — scores are baked into the HTML.

---

## Scoring (Pass 1)

For each entry body, run spaCy (`es_core_news_sm`) to get a token list with lemmas and POS tags. Form bigram candidates from consecutive token pairs.

**POS filter** — keep only pairs matching:
- `NOUN + NOUN`
- `NOUN + ADJ`
- `ADJ + NOUN`
- `PROPN + NOUN`
- `PROPN + PROPN`

**Score:**
```
score(lemma_bigram) = entries_containing_lemma_bigram / total_entries
```

**Threshold:** ≥2 entries. Single-character tokens skipped.

Result: a dict `{ "sistema operativo": 0.42, "toma nota": 0.31, ... }` keyed by lemma pairs.

---

## Injection (Pass 2)

For each entry, run spaCy on the body to get tokens with character offsets and lemmas. Scan consecutive pairs: if `lemma_a + " " + lemma_b` is in the score dict, record the character span `(token_a.idx, token_b.idx + len(token_b))` in the **original (non-lemmatized) text**.

Collect all non-overlapping spans, sort by start offset, then reconstruct the text by interleaving plain segments and annotated `<a>` tags:

```python
score = bigram_scores[bigram_key]
intensity = round(score, 3)
href = f"/search/?q={quote(bigram_key)}"
tag = f'<a class="hm" style="--s:{intensity}" href="{href}">{original_text}</a>'
```

The annotated string is then passed to mistune. mistune allows inline HTML by default, so the `<a>` tags survive rendering.

---

## CSS

```css
a.hm {
  background: rgba(234, 179, 8, var(--s));
  border-radius: 2px;
  padding: 0 1px;
  text-decoration: none;
  color: inherit;
}

a.hm:hover {
  text-decoration: underline;
}
```

No JS needed.

---

## Build Changes

In `build.py`:

1. `import spacy` and load `es_core_news_sm` once at startup.
2. Pass 1: iterate all entries, collect scored bigrams.
3. Pass 2: `entry_body_html()` receives the scored dict, injects spans before calling `md()`.
4. Append heatmap CSS to the `CSS` constant.

New dependency: `spacy` + model download (one-time):
```bash
uv add spacy
uv run python -m spacy download es_core_news_sm
```

---

## Interaction with 002 (Selection Popover)

No conflict. The selection popover uses Pagefind client-side; the heatmap is static HTML. Both can coexist on the same page.

---

## Out of Scope

- Unigram fallback.
- Per-entry relative scoring.
- Trigrams.
- Adjustable intensity slider.
