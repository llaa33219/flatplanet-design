# 03 — Usage

How to assemble FlatPlanet components into interfaces without breaking the
system's rules.

---

## 1. Composition rules

### Main and sub elements nest, and they do different things

The system has exactly two kinds of element, and the difference is
visible:

| | Main element | Sub element |
|---|---|---|
| Border | None | 4px |
| Shadow | Full ink | Soft ink |
| On hover | Presses down | Lifts up |
| Example | Card | List item inside it |

When a sub element sits inside a main element, the main element's hover
state does not automatically propagate. Each reacts to the pointer on its
own, and the two states together produce the system's characteristic
depth: the parent presses into the page while the child lifts off the
parent.

### Depth stacks

A main element inside a main element should use `fp-card--flat` or
`fp-panel--flat`. Two full-strength shadows stacked on top of each other
read as a mistake rather than as depth.

The same applies to a table: `fp-table-wrap` already carries the shadow,
so the table itself has none.

### Shadows are not decoration

If a component has a shadow, it is a floating surface. If it needs to sit
flush inside another surface, it should not have one. Reach for
`--fp-surface-sunken` to express "this area is inset" rather than
removing the shadow and leaving the element visually identical to its
surroundings.

### Radius is not a knob

36px is the radius. Do not reach for `--fp-radius-sm` because a component
looks slightly heavy — reach for a smaller size class, which carries its
own radius and its own shadow height as a matched set. The radius steps
down with the height, and the two are designed together.

---

## 2. The main colour

BLP White (`#fefeff`) is the main colour of the product. Most surfaces
are white because that is the base, not because white is a neutral
default.

A typical view is therefore:

- page canvas: `--fp-page-bg` (`#f5f5f5`)
- cards, panels, menus, modals: `--fp-surface` (`#fefeff`)
- sunken areas: `--fp-surface-sunken` (`#f5f5f5`)
- text: `--fp-text` (`#000309`)
- depth: `--fp-ink` (`#00193d`)

The page canvas and the sunken surface are the same colour in the light
theme. That is intentional: both are "not the main surface". The white
of a card reads as raised because of the ink shadow around it, not
because of a colour difference.

---

## 3. The accent discipline

`#007bff` is an accent. It marks the one thing in a view that matters
most.

**Budget: one accent-filled element per view.**

```html
<!-- Good: one primary, everything else neutral -->
<div class="fp-row">
  <button class="fp-btn fp-btn--primary">Save</button>
  <button class="fp-btn fp-btn--secondary">Cancel</button>
  <button class="fp-btn fp-btn--ghost">Discard</button>
</div>
```

```html
<!-- Bad: the accent stops meaning anything -->
<button class="fp-btn fp-btn--primary">Save</button>
<button class="fp-btn fp-btn--primary">Download</button>
<button class="fp-btn fp-btn--primary">Share</button>
```

When a second element needs to be prominent, reach for `fp-btn--dark` —
the same visual weight, in ink rather than blue. This is what makes the
single blue button in a view actually draw the eye.

Accent is also acceptable in these places, because none of them compete
for the same "main action" slot:

- focus rings
- text links
- the `--info` alert's border
- opt-in modifiers: `fp-card--accent`, `fp-badge--accent`,
  `fp-progress__bar--accent`
- the kicker label above a section heading

### The two sanctioned accent treatments

Beyond the single accent-filled element per view, the accent has exactly
two more uses, and both of them are about **emphasis** rather than
decoration. There is no third.

**One — the border of a sub element.** `.fp-sub--accent` recolours the
border a sub element already has, so the eye goes to that one element:

```html
<!-- Good: one sub element is pointed at -->
<div class="fp-list">
  <div class="fp-list__item">Ordinary item</div>
  <div class="fp-list__item fp-sub--accent">The one that matters</div>
</div>
```

```html
<!-- Bad: the accent border stops pointing at anything -->
<div class="fp-list__item fp-sub--accent">One</div>
<div class="fp-list__item fp-sub--accent">Two</div>
<div class="fp-list__item fp-sub--accent">Three</div>
```

The accent border is a pointer. It never makes the element bigger, never
moves it, and never gives it a resting shadow — a sub element stays flat
at rest whatever colour its border is.

**Two — a block of colour behind emphasised words.** `.fp-highlight`
puts bold text on a plain rectangle of accent colour:

```html
<p>Some <strong class="fp-highlight">emphasised words</strong> in a sentence.</p>
```

The rectangle has no radius: it is a print, not a pill. `mark` is the
neutral sibling — same shape, yellow instead of blue — for when the
highlight is editorial rather than emphatic.

### What the accent is not for

- **Not a border on everything.** An accent border on every sub element
  is the same mistake as an accent fill on every button.
- **Not a hover state.** Hover is expressed with movement and shadow,
  which is what the elevation system is for. Reach for `--fp-ink` or a
  surface change instead.
- **Not a status colour.** Red, green and yellow are for status. Blue is
  for emphasis and for actions.

---

## 4. Writing copy that fits the components

### Buttons

Label the action, not the object. "Save changes" beats "Submit". "Delete
project" beats "Delete". The button already sits next to the thing it
affects, so it does not need to name it.

Keep labels under three words. If a button needs a sentence, it probably
belongs in an alert or a confirmation modal.

### Empty states

An empty state has three parts: what is missing, why it is empty, and the
one action that fixes it. All three. "Nothing here yet" alone leaves the
user stuck.

### Errors

Say what happened and what to do next. "Enter a valid email address" is
an error message. "Invalid input" is not.

### Stat tiles

The label is a noun in caps. The value is the number, large. The delta is
optional and directional.

---

## 5. Accessibility

### Focus is never removed

The global `:focus-visible` rule gives every focusable element a 2px
accent outline with a 3px offset. It is never suppressed.

```css
:focus-visible {
  outline: var(--fp-border-width-sm) solid var(--fp-accent);
  outline-offset: 3px;
}
```

### Interactive elements are real elements

Use `<button>` for actions and `<a href>` for navigation. A `<div>` with a
click handler is not focusable, is not announced as a button, and does
not respond to Enter or Space.

### Icon-only controls need labels

```html
<button class="fp-btn fp-btn--icon" aria-label="Settings">…</button>
```

### Colour is never the only signal

Every status badge can take `fp-badge--dot`, which adds a coloured dot
alongside the text. Every alert pairs a colour with an icon and a
title.

### Motion respects the user

`prefers-reduced-motion: reduce` collapses all transitions to 0.01ms and
disables the skeleton shimmer. Hover transforms are neutralised; colour
changes are kept so the interface stays legible.

### Contrast

In the light theme, ink `#000309` on white `#fefeff` is a contrast ratio
of roughly 18:1. Muted text `#3e4d5f` on white is roughly 8:1. Both
comfortably clear WCAG AA at every text size.

Tinted surfaces are always paired with a dedicated foreground token, so
the pair stays legible in both themes rather than relying on the tint to
carry the contrast.

---

## 6. Dark mode

The dark theme is a token override. No component file changes.

```html
<html lang="en" data-theme="dark">
```

```js
document.documentElement.setAttribute('data-theme', 'dark');
```

The JavaScript in `flatplanet.js` handles the toggle and persists the
choice in `localStorage` under `flatplanet-theme`.

### How the dark theme is built

The canvas becomes `#000309` — the darkest colour in the palette.
Surfaces become `#1e2b3d` (BLP Soft Dark), one step above the canvas, so
the standard "elevated = lighter" hierarchy survives the inversion.

Shadows stay dark in the dark theme (`#000309` against the `#1e2b3d`
surface). A light shadow on a dark surface would read as a glow rather
than as a shadow, and the hard-shadow character of the system would be
lost.

The ink inverts to `#d4dce8` (BLP Light Dark) so that borders and
inverted fills still work.

Tints are remapped to deep backgrounds with light foregrounds:

| | Light | Dark |
|---|---|---|
| Info | `#dbedff` / `#0026a3` | `#16293f` / `#9fd0ff` |
| Success | `#eaf7ef` / `#007512` | `#12301f` / `#8fe0a4` |
| Warning | `#fff9bd` / `#b2a400` | `#3a3213` / `#ffe98a` |
| Danger | `#ffdbdb` / `#a30000` | `#3a1a1c` / `#ff9ea5` |

### Adding your own theme

Override the semantic tokens. Never override a raw palette token.

```css
[data-theme="high-contrast"] {
  --fp-ink: #000000;
  --fp-text: #000000;
  --fp-page-bg: #ffffff;
  --fp-surface: #ffffff;
}
```

---

## 7. Extending the system

### Adding a colour

1. Find the nearest palette entry in `색깔-3.pdf`. If no entry fits, the
   colour does not belong in the system.
2. Add it to the raw palette block in `tokens.css` with a comment naming
   its palette entry.
3. Add a semantic token that describes its *role*, not its hue.
4. Reference the semantic token from the component. Never the raw one.

### Adding a component

1. Decide whether it is a main or a sub element.
2. Use the existing tokens only. If you need a new value, add a token.
3. Use the standard transition bundle.
4. Respect the 36px ceiling — if the component is shorter than 48px, use
   `--fp-radius-sm`; under 32px, `--fp-radius-xs`.
5. Use the 4px border for sub elements, 2px for micro elements.
6. Add a dark-theme check. If the component uses a hardcoded colour, it
   will break.
7. Document it in `docs/02-components.md`.

### Using the elevation system directly

```html
<div class="fp-elev fp-elev--3">Floats with a 9px hard shadow.</div>
<div class="fp-elev fp-elev--3">The one direction, at a larger size.</div>
<div class="fp-sub">A sub element that lifts on hover.</div>
<div class="fp-sub fp-sub--accent">A sub element the accent points at.</div>
```

A main element's shadow is offset **equally and positively** on both
axes, so it reads as a block printed on the surface, falling to the
bottom-right. There is no upward shadow, no leftward shadow and no
four-sided band: the shadow's only variable is its size.

A sub element has no shadow at rest — the border is its outline, and the
shadow appears as it lifts. Add `.fp-sub--accent` to point at it.

---

## 8. JavaScript

`assets/js/flatplanet.js` is a small, dependency-free file providing
behaviour the CSS cannot:

| Feature | API |
|---------|-----|
| Theme toggle | `#themeToggle`, persisted to `localStorage` |
| Tabs | `[role="tab"]` inside `[role="tablist"]` |
| Segmented control | `.fp-segment__item` |
| Chips | `.fp-chip[aria-pressed]` |
| Modal | `data-modal-open="id"`, `data-modal-close` |
| Drawer | `data-drawer-open="id"`, `data-drawer-close` |
| Toast | `FlatPlanet.toast(message, type, title)` |
| Scroll spy | `.fp-toc__item[href^="#"]` |
| Palette swatches | `#swatches` |

Everything degrades gracefully. A modal without JavaScript will not open,
but a tab list without JavaScript still renders as a row of tabs.

---

## 9. Performance

- No CSS framework, no build step, no runtime dependency.
- The whole system is about 60KB of CSS and 12KB of JavaScript, unminified.
- Shadows are the only expensive paint operation, and they are static
  zero-blur offsets that browsers cache as simple layers.
- The skeleton shimmer is the only continuous animation. It respects
  `prefers-reduced-motion`.
