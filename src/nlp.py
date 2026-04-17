from collections import Counter

import spacy

nlp = spacy.load("es_core_news_sm")

MEANINGFUL_POS_PAIRS = {
    ("NOUN", "NOUN"),
    ("NOUN", "ADJ"),
    ("ADJ", "NOUN"),
    ("PROPN", "NOUN"),
    ("PROPN", "PROPN"),
    ("NOUN", "PROPN"),
}
MEANINGFUL_POS = {"NOUN", "PROPN"}
MEANINGFUL_POS_CONTENT = {"NOUN", "PROPN", "ADJ"}
HEATMAP_MIN_ENTRIES = 2
MONOGRAM_MIN_ENTRIES = 4


def compute_ngram_scores(entries: list[dict]) -> dict[str, float]:
    """Pass 1: score lemma ngrams (monograms + bigrams) by fraction of entries that contain them."""
    total = len(entries)
    mono_counts: Counter = Counter()
    multi_counts: Counter = Counter()
    for entry in entries:
        body = entry.get("body", "").strip()
        if not body:
            continue
        doc = nlp(body)
        seen = set()
        tokens = [t for t in doc if not t.is_space]
        for a, b, c in zip(tokens, tokens[1:], tokens[2:]):
            if not all(t.pos_ in MEANINGFUL_POS_CONTENT for t in (a, b, c)):
                continue
            if not all(len(t.lemma_) >= 2 for t in (a, b, c)):
                continue
            key = f"{a.lemma_.lower()} {b.lemma_.lower()} {c.lemma_.lower()}"
            if key not in seen:
                seen.add(key)
                multi_counts[key] += 1
        for a, b in zip(tokens, tokens[1:]):
            if (a.pos_, b.pos_) not in MEANINGFUL_POS_PAIRS:
                continue
            if len(a.lemma_) < 2 or len(b.lemma_) < 2:
                continue
            key = f"{a.lemma_.lower()} {b.lemma_.lower()}"
            if key not in seen:
                seen.add(key)
                multi_counts[key] += 1
        for t in tokens:
            if t.pos_ not in MEANINGFUL_POS or len(t.lemma_) < 2:
                continue
            key = t.lemma_.lower()
            if key not in seen:
                seen.add(key)
                mono_counts[key] += 1

    raw = {
        **{k: c / total for k, c in multi_counts.items() if c >= HEATMAP_MIN_ENTRIES},
        **{k: c / total for k, c in mono_counts.items() if c >= MONOGRAM_MIN_ENTRIES},
    }
    if not raw:
        return raw
    mn, mx = min(raw.values()), max(raw.values())
    if mn == mx:
        return {k: 0.12 for k in raw}
    return {k: 0.08 + (v - mn) / (mx - mn) * 0.42 for k, v in raw.items()}
