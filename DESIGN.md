# Design System Strategy: The Brutalist Librarian

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Brutalist Librarian."**

This system represents a deliberate collision between the rigorous, information-dense world of Edward Tufte and the raw, unapologetic energy of street-level DIY punk zines. We are moving away from the "friendly SaaS" aesthetic. There are no rounded corners here. There are no vibrant primary colors. Instead, we find beauty in high-contrast grayscale, massive typography scales, and a layout that breathes through expansive white space rather than structural lines.

The goal is to create an experience that feels like a rare, self-published academic manifesto: intellectually elite, yet visually disruptive.

---

## 2. Colors & Surface Logic
The palette is strictly grayscale, relying on tonal shifts to define hierarchy.

### Token Reference
| Token | Value | Role |
|---|---|---|
| `--surface` | `#f9f9f7` | Page canvas |
| `--surface-dim` | `#dadad8` | Subtle fill for interactive blocks (favicon bg, quoteback backlink) |
| `--surface-low` | `#f4f4f2` | Secondary context sections (quoteback head, pagination bg) |
| `--surface-highest` | `#e2e3e1` | Hover state on list items |
| `--surface-lowest` | `#ffffff` | Lifted paper (quoteback body, command palette) |
| `--primary` | `#000000` | High-impact ink |
| `--primary-container` | `#3c3b3b` | CTA gradient endpoint |
| `--primary-fixed` | `#5f5e5e` | Hover state for primary elements |
| `--on-primary` | `#e5e2e1` | Text on black backgrounds |
| `--on-surface` | `#1a1a1a` | Body text |
| `--outline` | `#777777` | Metadata, labels, strokes |
| `--highlight-rgb` | `26, 26, 26` | RGB base for highlight washes (mark, heatmap) |

### Dark Mode
Activated via `prefers-color-scheme: dark`. Token overrides on `:root` — no extra markup or JS needed. Custom properties cascade into Shadow DOM automatically, so the quoteback card adapts for free.

| Token | Light | Dark |
|---|---|---|
| `--surface` | `#f9f9f7` | `#111110` |
| `--surface-dim` | `#dadad8` | `#2a2a28` |
| `--surface-low` | `#f4f4f2` | `#1a1a18` |
| `--surface-highest` | `#e2e3e1` | `#333331` |
| `--surface-lowest` | `#ffffff` | `#0d0d0c` |
| `--primary` | `#000000` | `#f0ede8` |
| `--primary-container` | `#3c3b3b` | `#c8c5c0` |
| `--primary-fixed` | `#5f5e5e` | `#a8a5a0` |
| `--on-primary` | `#e5e2e1` | `#111110` |
| `--on-surface` | `#1a1a1a` | `#e8e5e0` |
| `--outline` | `#777777` | `#888885` |
| `--highlight-rgb` | `26, 26, 26` | `240, 237, 232` |

The dark palette is a warm near-black inversion — "light ink on dark paper" — preserving the editorial character of the light theme.

`--highlight-rgb` is stored as raw RGB components (not hex) to allow variable-opacity compositions via `rgba(var(--highlight-rgb), x)`. It uses the same warm tone as `--on-surface` in each mode.

### The "No-Line" Rule
Traditional 1px borders are strictly prohibited for **structural sectioning**. We define boundaries through **Tonal Carving**.
- Use a transition from `--surface` to `--surface-low` to denote a change in content context (e.g. pagination block, quoteback metadata footer).
- Use `--surface-dim` for a stronger tonal step within a section (e.g. quoteback backlink column).
- Contrast is our primary tool for focus. Use `--primary` (#000000) against `--surface` for an "ink-on-paper" punch.

**Structural Line Exceptions:** A `1px solid var(--outline)` stroke is permitted in the following specific cases where tonal carving alone is insufficient:
- Feed separator: `.feed-entry + .feed-entry { border-top }` — separates entries in the feed list.
- Single-entry footer: `article:only-of-type .entry-footer { border-bottom }` — closes the entry when viewed in isolation.
- Cite footnote separator: `#cite-ref p + p { border-top: 1px solid var(--surface-highest) }` — divides citation paragraphs within the dialog.

### The "Ghost Border" Fallback
When a white (`--surface-lowest`) card sits on the page canvas (`--surface`) and tonal contrast alone is insufficient, use a Ghost Border: `1px solid #c6c6c6`. Applied to quoteback cards and all `<dialog>` elements. If you can see the line clearly at arm's length, it is too heavy.

### Signature Textures
While the system is flat, use a subtle linear gradient on primary CTAs: `--primary` (#000000) to `--primary-container` (#3c3b3b). This prevents the black from feeling "dead" and gives it a heavy, metallic ink quality.

---

## 3. Typography: The High-Low Fusion
The system uses exactly **two typefaces**.

### Font Stack
| Role | Typeface | Usage |
|---|---|---|
| Display & Headlines | **Space Grotesk** | Site title, entry titles, search page title, search input, search result titles |
| Body, UI & Labels | **Newsreader** | All body text, and all label/metadata contexts using `font-variant-caps: all-small-caps` |

There is no third typeface. What was previously assigned to a sans-serif utility font (nav links, dates, tags, pagination, command palette metadata) is now handled by Newsreader in small-caps.

### Scale
- **Base:** `html { font-size: 125% }` — sets `1rem = 20px` globally, including inside Shadow DOM.
- **Body text:** `1rem` / `line-height: 1.8`
- **Entry title:** `2.25rem` — a deliberate 2.25× ratio over body text. Loud enough to anchor the page, controlled enough to coexist with dense prose.
- **Site title:** `1.5rem` Space Grotesk
- **Labels / metadata:** `0.75rem` Newsreader with `font-variant-caps: all-small-caps` and light letter-spacing

### Rules
- **Space Grotesk** always at tight letter-spacing (`-0.02em`) and `font-weight: 700`. It is our "Street" element — wheat-pasted poster energy.
- **Newsreader in small-caps** replaces any utility sans. Use `font-variant-caps: all-small-caps` — never `text-transform: uppercase` with a separate font. This brings an archival, editorial feel.
- **Newsreader italic** for blockquote and quoteback body content.
- `font-feature-settings: "ss01" 1` applied globally on `body` for Newsreader ligatures.

---

## 4. Elevation & Depth
We reject the standard "floating card" look in favor of **Physical Stacking**.

### The Layering Principle
Depth is achieved by placing `--surface-lowest` (#ffffff) content on a `--surface` (#f9f9f7) background, made legible by the Ghost Border fallback when needed.

### Shadows as "Ink Bleed"
Shadows are restricted to Paper Blocks (quoteback cards, blockquotes).
- **Quoteback card:** `box-shadow: 0 2px 32px rgba(26,26,26,0.07)` — an extra-diffused ambient shadow using `--on-surface` at ~7% opacity. Warm tone, not pure grey. It should look like a heavy sheet of paper on a desk.
- **Blockquote (Paper Block):** `box-shadow: 0 2px 32px rgba(26,26,26,0.04)` — same formula at 4% opacity. Slightly more recessed than quoteback cards, as they are embedded content rather than lifted documents.
- **No hover transform.** `translateY` effects are a SaaS affordance. Cards do not move.

---

## 5. Components

### Buttons
- **Shape:** Absolute `0px` radius. No exceptions.
- **Primary:** `--primary` (#000000) background, `--on-primary` (#e5e2e1) text.
- **Hover:** Shift to `--primary-fixed` (#5f5e5e).
- **Shadow:** Sharp `0px 2px 0px rgba(0,0,0,0.1)` "ink" underline.
- **Tertiary:** Heavy 2pt "ink" underline instead of a box.

### Quoteback Cards
Uses a Ghost Border (`1px solid #c6c6c6`) because its white background (`--surface-lowest`) does not carve tonally from the page canvas without it.

- **Card body:** Newsreader italic, `1rem`, `padding: 2rem`, white background, ambient shadow.
- **Metadata footer (`.quoteback-head`):** `background: --surface-low` — tonal separation, no border-top.
- **Backlink column:** `background: --surface-dim` — tonal separation, no border-left.
- **Author:** Space Grotesk bold, `0.8rem`.
- **Source title:** Newsreader small-caps, `0.72rem`, `--outline` color.
- **"Go to text" link:** Newsreader small-caps, `0.72rem`, letter-spaced.
- **Favicon:** Square (`border-radius: 0`), no border, `--surface-dim` fill.

### "Paper" Blocks (Blockquotes)
Blockquotes inside entry bodies use the Paper Block treatment: white background, ambient shadow, `padding: 2rem`, Newsreader italic. No left border stripe.

### External Link Indicator
Links inside `.entry-body` that point to external URLs get an automatic `↗` superscript via CSS `::after`. It renders at `0.65em`, `opacity: 0.5` — present but unobtrusive.

### Entry Footer & Actions
Each entry has a `.entry-footer` below its body that holds engagement actions (share, reply, cite, etc.).

- **Layout:** Flexbox row, `gap: 1.5rem`, `padding: 1rem 0 2.5rem`.
- **Actions (`.entry-action`):** Inline-flex, no box, no background. Newsreader small-caps `0.75rem`, `--outline` color. Hover shifts to `--primary`.
- **Icon:** SVG `0.8rem × 0.8rem`, `stroke: currentColor`, `stroke-width: 2`, no fill. Always accompanied by a label.
- **Feed separator:** `.feed-entry + .feed-entry` adds a `border-top: 1px solid var(--outline)` and `padding-top: 2.5rem` — one of the permitted structural line exceptions.

### Dialogs (Shared Chrome)
All dialogs share a base style via the `dialog` element selector.

- **Shape:** `border-radius: 0`. Absolute.
- **Border:** Ghost Border `1px solid #c6c6c6`.
- **Shadow:** `0 2px 32px rgba(26,26,26,0.07)` — same as quoteback card.
- **Background:** `--surface-lowest`. Color: `--on-surface`.
- **Backdrop:** `rgba(26,26,26,0.35)`.
- **Close button (`.dialog-close`):** Float right, no box, `1.25rem`, `--outline`. Hover → `--primary`.
- **Label (`.dialog-label`):** Newsreader small-caps `0.75rem`, `0.06em` letter-spacing, `--outline`.
- **Input / Textarea (`.dialog-input`, `.dialog-textarea`):** Transparent background, bottom-stroke only (`1px solid --outline`), focus thickens to `2px --primary`. Newsreader `1rem`.
- **Action button (`.dialog-action`):** Linear gradient `--primary` → `--primary-container`, `--on-primary` text, sharp `0px 2px 0px rgba(0,0,0,0.1)` underline shadow. Hover → flat `--primary-fixed`.
- **Max-widths:** `#share-dialog` `32rem` — `#reply-dialog` `36rem`.

### Citations
Inline citations are marked with `.cite` — a `cursor: pointer` span with a `border-bottom: 1px dotted var(--outline)` underline (dotted, not solid).

The cite dialog (`#cite-dialog`) follows the shared dialog chrome with `max-width: 36rem`. Citation paragraphs inside `#cite-ref` are separated by a `1px solid var(--surface-highest)` rule — the softest permitted line.

### Input Fields
- **Style:** No box. Only a bottom stroke using `--outline` (#777777).
- **Focus:** Stroke thickens to 2px `--primary` (#000000).
- **Search input:** Matches entry title scale — Space Grotesk `2.25rem` — but rendered in `--outline` grey when empty. Typed text uses `--on-surface`. Placeholder uses `--surface-dim`.

### Search Page
- **Title ("Search"):** `.search-page-title` — Space Grotesk `2.25rem`, full `--primary` black. Visually identical to an entry title.
- **Input:** Same scale and font as the title, greyed to `--outline` until focused. Creates a unified title-as-input feel.

### Lists & Cards
- **The Divider Ban:** Do not use horizontal rules. Separate list items using `margin-bottom: 4.5rem` of white space.
- **Hierarchy:** Body text for content, Newsreader small-caps at `0.75rem` for secondary metadata.

### Pagination
Rendered as a `background: --surface-low` block — tonal carving signals the end of the feed. Newsreader small-caps, `0.75rem`, letter-spaced. No border.

### Heatmap Links
`a.hm` renders inline text with a tonal wash of variable intensity controlled by the `--s` custom property set per element. Uses `rgba(var(--highlight-rgb), var(--s))` — dark ink wash in light mode, warm near-white wash in dark mode. No border radius. Color inherits from context.

### Search Result Highlights
`mark` inside `#search-results` uses `rgba(var(--highlight-rgb), 0.15)` — a fixed-opacity tonal wash equivalent in visual weight to the amber it replaces, but within the grayscale system.

### Command Palette
Sharp rectangle, `border-radius: 0`, `--surface-lowest` background, warm box-shadow. Input uses Newsreader at `1rem`. Result dates use Newsreader small-caps.

### Footer
Full-bleed via negative horizontal margins (`margin-left: -2rem; margin-right: -2rem`) that cancel the body padding. `background: --surface-low`. Newsreader small-caps `0.75rem`, `0.04em` letter-spacing, `--outline` color. Two-column flex: left text, right `.footer-links` column (flex-end, `gap: 0.25rem`). Links underlined in `--outline`, hover → `--primary`.

---

## 6. Do's and Don'ts

### Do:
- **Use only two fonts:** Space Grotesk for display/headlines, Newsreader for everything else.
- **Use Newsreader small-caps for all labels:** `font-variant-caps: all-small-caps` on any metadata, date, tag, nav link, or UI label.
- **Play with Scale:** Set a tiny Newsreader small-caps label next to a massive Space Grotesk `2.25rem` headline to create visual drama.
- **Embrace Asymmetry:** Let marginalia exist only on one side. Don't feel the need to "balance" horizontally.
- **Use the Ghost Border only as a fallback:** Only when white-on-near-white contrast is genuinely insufficient.

### Don't:
- **Never use Border Radius:** Even a 2px radius destroys the "Street Scholar" aesthetic.
- **Never add a third typeface:** The tension between Space Grotesk and Newsreader is the system. A third font breaks it.
- **Avoid Centered Layouts:** This is an editorial system. Left-aligned, asymmetrical grids only.
- **No `text-transform: uppercase`:** Use `font-variant-caps: all-small-caps` on Newsreader instead — it achieves the catalog effect with proper typographic small capitals.
- **No hover transforms:** Cards and blocks do not float or lift on hover. Interaction is expressed through color shifts only.
- **No Pure Grey Shadows:** Shadows must use `rgba(26,26,26,x)` — the warm `--on-surface` tone — never neutral grey.
- **No Icons without Labels:** Clarity is king. Icons should be rare and always accompanied by a Newsreader small-caps label.
