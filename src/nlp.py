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
HEATMAP_MIN_ENTRIES = 2


def compute_bigram_scores(entries: list[dict]) -> dict[str, float]:
    """Pass 1: score lemma bigrams and monograms by fraction of entries that contain them."""
    total = len(entries)
    entry_counts: Counter = Counter()
    for entry in entries:
        body = entry.get("body", "").strip()
        if not body:
            continue
        doc = nlp(body)
        seen = set()
        tokens = [t for t in doc if not t.is_space]
        for a, b in zip(tokens, tokens[1:]):
            if (a.pos_, b.pos_) not in MEANINGFUL_POS_PAIRS:
                continue
            if len(a.lemma_) < 2 or len(b.lemma_) < 2:
                continue
            key = f"{a.lemma_.lower()} {b.lemma_.lower()}"
            if key not in seen:
                seen.add(key)
                entry_counts[key] += 1
        for t in tokens:
            if t.pos_ not in MEANINGFUL_POS or len(t.lemma_) < 2:
                continue
            key = t.lemma_.lower()
            if key not in seen:
                seen.add(key)
                entry_counts[key] += 1

    return {
        key: count / total
        for key, count in entry_counts.items()
        if count >= HEATMAP_MIN_ENTRIES
    }
