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

### The "No-Line" Rule
Traditional 1px borders are strictly prohibited for sectioning. We define boundaries through **Tonal Carving**.
- Use a transition from `--surface` to `--surface-low` to denote a change in content context (e.g. pagination block, quoteback metadata footer).
- Use `--surface-dim` for a stronger tonal step within a section (e.g. quoteback backlink column).
- Contrast is our primary tool for focus. Use `--primary` (#000000) against `--surface` for an "ink-on-paper" punch.

### The "Ghost Border" Fallback
When a white (`--surface-lowest`) card sits on the page canvas (`--surface`) and tonal contrast alone is insufficient, use a Ghost Border: `1px solid #c6c6c6`. Applied currently to the quoteback card container. If you can see the line clearly at arm's length, it is too heavy.

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
- **Base:** `html { font-size: 112.5% }` — sets `1rem = 18px` globally, including inside Shadow DOM.
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
The only component that uses a Ghost Border (`1px solid #c6c6c6`) because its white background (`--surface-lowest`) does not carve tonally from the page canvas without it.

- **Card body:** Newsreader italic, `1rem`, `padding: 2rem`, white background, ambient shadow.
- **Metadata footer (`.quoteback-head`):** `background: --surface-low` — tonal separation, no border-top.
- **Backlink column:** `background: --surface-dim` — tonal separation, no border-left.
- **Author:** Space Grotesk bold, `0.8rem`.
- **Source title:** Newsreader small-caps, `0.72rem`, `--outline` color.
- **"Go to text" link:** Newsreader small-caps, `0.72rem`, letter-spaced.
- **Favicon:** Square (`border-radius: 0`), no border, `--surface-dim` fill.

### "Paper" Blocks (Blockquotes)
Blockquotes inside entry bodies use the Paper Block treatment: white background, ambient shadow, `padding: 2rem`, Newsreader italic. No left border stripe.

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

### Command Palette
Sharp rectangle, `border-radius: 0`, `--surface-lowest` background, warm box-shadow. Input uses Newsreader at `1rem`. Result dates use Newsreader small-caps.

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
