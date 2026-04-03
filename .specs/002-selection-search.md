# 002 — Selection Search Popover

## Overview

When a user selects text on any page, a floating popover appears with the top Pagefind results for that selection. Inspired by Notation's heatmap/contextual linking idea, but trigger-on-select rather than heatmap.

---

## Behaviour

1. User selects text (mouse drag or double-click) anywhere on the page.
2. After a short debounce (~300ms), if selection is ≥4 characters, query Pagefind.
3. A popover appears anchored below the selection with up to 5 results.
4. Clicking a result navigates to that entry.
5. Popover dismisses on: click outside, `Escape` key, or selection cleared.
6. No popover shown when selecting text inside the search `<input>`.

---

## Popover Anatomy

```
┌─────────────────────────────────┐
│ "selected text"                 │  ← small header showing the query
├─────────────────────────────────┤
│ 2026-03-10                      │
│ Entry title                     │
│ …excerpt with <mark>match</mark>│
├─────────────────────────────────┤
│ 2026-02-14                      │
│ Another entry                   │
│ …                               │
└─────────────────────────────────┘
```

- Max 5 results. If 0 results, popover does not appear.
- Popover width: `min(400px, 90vw)`.
- Positioned below the selection rect; flips above if too close to viewport bottom.

---

## Implementation

### Loading Pagefind

Pagefind is already loaded on the search page. For other pages it must be loaded on demand (only once, lazily) to avoid bloating every page load.

```js
let _pf = null;
async function getPagefind() {
  if (!_pf) {
    _pf = await import("/pagefind/pagefind.js");
    await _pf.init();
  }
  return _pf;
}
```

### Positioning

```js
const rect = window.getSelection().getRangeAt(0).getBoundingClientRect();
const top = rect.bottom + window.scrollY + 8;
const left = Math.min(rect.left + window.scrollX, window.innerWidth - POPOVER_WIDTH - 16);
// flip above if below viewport fold
if (rect.bottom + POPOVER_HEIGHT > window.innerHeight) {
  top = rect.top + window.scrollY - POPOVER_HEIGHT - 8;
}
```

### Event flow

```
mouseup / selectionchange
  → debounce 300ms
  → read selection string
  → guard: length < 4 → dismiss & return
  → guard: active element is #search-input → return
  → getPagefind()
  → pf.search(query, { limit: 5 })
  → results.length === 0 → dismiss & return
  → render popover, position, show
```

### Dismissal

```js
document.addEventListener("mousedown", (e) => {
  if (!popover.contains(e.target)) dismiss();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") dismiss();
});
document.addEventListener("selectionchange", () => {
  if (window.getSelection().isCollapsed) dismiss();
});
```

---

## Styling

Popover is a `<div id="sel-popover">` injected once into `<body>`, hidden by default via `display:none`.

Key styles (added to `style.css`):

```css
#sel-popover {
  position: absolute;
  z-index: 100;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  width: min(400px, 90vw);
  font-size: 0.85rem;
  display: none;
}

#sel-popover.visible { display: block; }

#sel-popover .sp-header {
  padding: 0.4rem 0.75rem;
  border-bottom: 1px solid #eee;
  color: #888;
  font-style: italic;
}

#sel-popover .sp-result {
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

#sel-popover .sp-result:last-child { border-bottom: none; }
#sel-popover .sp-result:hover { background: #f9f9f9; }

#sel-popover .sp-result-date { color: #aaa; font-size: 0.78rem; }
#sel-popover .sp-result-title { font-weight: bold; margin-bottom: 0.2rem; }
#sel-popover mark { background: #fff3a0; padding: 0 2px; }
```

---

## Delivery

- All JS inlined in the base template `<script>` tag (no new files).
- CSS additions appended to the existing `CSS` constant in `build.py`.
- No new dependencies.

---

## Out of Scope

- Heatmap highlighting (which words have most connections).
- Pinning / saving results from the popover.
- Showing results from external sources.
