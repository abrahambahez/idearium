# Hyperlink Maximalism

Linus Lee's [hyperlink maximalism](https://thesephist.com/posts/hyperlink/) proposes that the density of links in a document is a proxy for how well-connected and navigable its ideas are. Rather than linking only explicit references, the goal is to make every meaningful concept, entity, or phrase a potential portal — transforming a flat feed of notes into a traversable graph of thought. Applied to a personal journal, this means surfacing the implicit structure already latent in your writing: recurring themes, related entries, co-occurring ideas, named people and places — all made clickable.

---

## Tier 1 — Pure NLP (spaCy, already installed)

**Named Entity Linking**
Annotate people, places, orgs, and dates with spaCy's NER. `"ChatGPT"`, `"Madrid"`, `"Anthropic"` become links to a filtered entry list. No new deps — just `es_core_news_sm` already loaded.

**Trigrams / Skip-grams**
Extend beyond bigrams. Skip-grams (`"sistema _ operativo"`) catch phrases with intervening words. More recall, similar precision.

**Keyword co-occurrence**
Build a co-occurrence matrix across entries. Surface pairs that appear in the same entry even if not adjacent. Links become "entries where both X and Y appear" — a kind of implicit tagging.

**Sentence-level topic similarity**
Use spaCy word vectors to compute pairwise similarity between entry sentences. If two sentences from different entries are semantically close (cosine > threshold), cross-link those entries. No LLM needed.

---

## Tier 2 — Lightweight embeddings (local, no GPU)

**`sentence-transformers` nearest neighbors**
`all-MiniLM-L6-v2` (~80MB, CPU-fast). Embed each entry, find nearest neighbors → automatic "related entries" section. Works cross-lingually too.

**`paraphrase-multilingual-MiniLM-L12-v2`**
Same approach, natively multilingual. Better fit for Spanish-dominant content.

**Topic clusters**
K-means on embeddings → auto-discovered topic clusters → entries link to cluster-mates. No manual tags needed.

---

## Tier 3 — Micro local LLMs (Ollama, quantized)

**`nomic-embed-text` via Ollama**
Tiny dedicated embedding model for retrieval. Same idea as sentence-transformers but running through Ollama's local API — fully offline, no API cost.

**Keyword/concept extraction with `gemma3:1b` or `qwen2.5:0.5b`**
At build time, send each entry to a tiny quantized model: extract 5 concepts, implicit references to earlier entries, mood/register. Cache results as a JSON sidecar. ~1–2s per entry, offline.

**Entity normalization**
`"GPT-4"`, `"gpt4"`, `"el modelo de OpenAI"` → same canonical entity. A tiny LLM resolves aliases that spaCy NER misses, so all variants link to the same search.

**Cross-entry narrative threads**
Ask the LLM: "does this entry continue a topic from these 5 candidate entries?" → explicit thread links. Like wiki's "see also" but auto-generated from your own writing.

---

## Tier 4 — Structural / graph-based

**Tag co-occurrence graph**
`@tag` links already exist. Build a full tag co-occurrence graph and link from each entry to a tag neighborhood page.

**Temporal proximity links**
Entries written within N days of each other are implicitly related. Chronological neighbor links surface what you were thinking about the week before.

**Implicit citations**
If entry B was written after entry A and shares ≥K similar terms, treat B as implicitly responding to A. Surface as "this might be a follow-up to..." links.

---

## Priority Matrix

| Idea | Effort | Payoff | Notes |
|---|---|---|---|
| NER links | Low | High | Already in spaCy, same pipeline |
| Sentence similarity (spaCy vectors) | Low | Medium | No new deps |
| `sentence-transformers` nearest neighbors | Medium | Very High | Best serendipity, one-time 80MB download |
| `nomic-embed-text` via Ollama | Medium | Very High | Best if Ollama already installed |
| Tiny LLM concept extraction | Medium | High | Needs caching layer to avoid rebuild cost |
| Tag co-occurrence graph | Low | Medium | Leverages existing `@tag` system |
