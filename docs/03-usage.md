# 03 — Usage

How to assemble FlatPlanet components into interfaces without breaking the
system's rules.

---

## 1. Composition rules

### Main and sub elements nest, and they do different things

The system has three kinds of element, and the difference is visible:

| | Main element | Sub element | Borderless sub |
|---|---|---|---|
| Border | None | 4px | None |
| Shadow | Full ink | None at rest | None at rest |
| On hover | Presses down | Lifts up | Lifts up |
| Example | Card | List item inside it | Navbar link |

When a sub element sits inside a main element, the main element's hover
state does not automatically propagate. Each reacts to the pointer on its
own, and the two states together produce the system's characteristic
depth: the parent presses into the page while the child lifts off the
parent.

### Choosing between the two sub tiers

Both sub tiers lift on hover and gain their shadow. The only difference
is the border, and that difference is about **attention**.

| Use | Tier |
|-----|------|
| The control needs to be found — a list item, a chip, a tab | Sub element, with its border |
| The control should be there but must not compete — a navbar link, a quiet toolbar | `.fp-sub--borderless` |

```html
<!-- A sub element: the border is what makes it findable. -->
<a class="fp-btn fp-btn--ghost fp-btn--sm" href="#">Foundations</a>

<!-- The borderless sub: present, but it does not shout. -->
<a class="fp-navbar__link fp-sub--borderless" href="#">Foundations</a>
```

Do not use the borderless tier to hide a control that people are meant
to use. It is for the rows of controls that are *navigation*, not the
rows of controls that are *actions*.

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

**In the dark theme the canvas changes and the main surface does not.**
The canvas becomes the palette's darkest colour (`#000309`) and the
surface stays the palette's lightest (`#fefeff`), so the main colour is
still the main colour — it is the *background* that swapped ends. A card
reads as raised in both themes, because it is the lightest thing on the
page in one and the lightest thing on the page in the other, and the
hard shadow is behind it either way.

This is why components reference `--fp-surface` and never a raw white:
the token is what carries the relationship, and the relationship is what
survives the inversion.

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

When a *sub* element needs to be prominent, reach for
`fp-btn--sub fp-btn--sub--accent` (or `.fp-sub--accent` on any other
sub element) — the emphasis travels on the border, never on a fill.
This is what makes the single blue button in a view actually draw the
eye.

Accent is also acceptable in these places, because none of them compete
for the same "main action" slot:

- focus rings
- text links
- the `--info` alert's border
- opt-in modifiers: `fp-badge--accent`,
  `fp-progress__bar--accent`
- the kicker label above a section heading
- the accent variant of a checked control: `fp-check--accent`,
  `fp-switch--accent`

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

**Two — the accent colour on emphasised words.** `.fp-highlight`
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
stops the skeleton pulse. Hover transforms are neutralised; colour
changes are kept so the interface stays legible.

### Contrast

In the light theme, ink `#000309` on white `#fefeff` is a contrast ratio
of roughly 18:1. Muted text `#3e4d5f` on white is roughly 8:1. Both
comfortably clear WCAG AA at every text size.

Tinted surfaces are always paired with a dedicated foreground token, so
the pair stays legible in both themes rather than relying on the tint to
carry the contrast. The pairs invert together in the dark theme — a
deep background with a light foreground — so the ratio is preserved in
both directions.

**The inverted theme has two text contexts, and both are checked.**
Text on the canvas is `#fefeff` on `#000309` (roughly 19:1); text on a
surface is `#000309` on `#fefeff` (roughly 18:1). Neither polarity is
left to chance.

**The sub element's border is a real border.** `#3e4d5f` against white
is roughly 8:1, so a sub element keeps a clear outline. The lighter
`#94989e` was rejected for the light theme's border for exactly this
reason: at about 2.9:1 a 4px line in that colour stops reading as an
outline at all.

**The accent and the accent fill are one blue, two uses.** `--fp-accent`
is the brand blue (`#007bff`) and it is what the accent IS — a focus
ring, an accent border, an accent-coloured line. `--fp-accent-fill` is
the same `#007bff` used as a background; it carries the button's large
bold label at 3.95:1, and deepens to `#005bdd` on hover.

So: the accent is for lines and for the one filled element per view,
and the accent is never used for body copy.

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

**The dark theme is a true inversion of the light theme.** The rule is
one sentence:

> Swap the black and the white of the light theme and you get the dark
> theme. Every colour is the light theme's colour inverted — *except the
> shadow colour*.

So:

- the page canvas becomes the palette's **darkest** colour, `#000309`
- the main surface stays the palette's **lightest** colour, `#fefeff`
- text on that surface becomes the palette's darkest, `#000309`
- anything that was white-filled is now dark-filled, and vice versa

**The shadow is the one exception.** It is `rgba(0, 25, 61, 0.22)` in the
light theme and stays `#000309` in the dark theme. A light shadow on a
dark surface reads as a *glow* rather than as depth, and the hard-shadow
character of the system would be lost. It is one step darker than the
canvas it falls on, so it reads as a hole behind a light card.

**The accent does not invert.** `#007bff` is a brand colour, not a
surface; inverting it would turn the accent into a different accent.
The accent *fill* (`#007bff`) does not invert either — it is the same
fill in both themes, because it is the same surface with the same white
text on it in either one.

**The status colours do not invert.** Red is still red. Only the tint
*surfaces* invert, and each tint inverts as a **pair** so the
background and the foreground stay matched:

| | Light (bg / fg) | Dark (bg / fg) |
|---|---|---|
| Info | `#dbedff` / `#0026a3` | `#0026a3` / `#dbedff` |
| Success | `#eaf7ef` / `#007512` | `#007512` / `#ccffd4` |
| Warning | `#fff9bd` / `#b2a400` | `#b2a400` / `#fff9bd` |
| Danger | `#ffdbdb` / `#a30000` | `#a30000` / `#ffdbdb` |

**Text has two contexts.** The inverted theme has two polarities on the
page at once, so text on the canvas and text on a card cannot share a
colour. `--fp-text` follows its **context**: it is the page value by
default, and every surface re-points it at the surface value. A
component never has to know which theme it is in.

The full mapping is in
[01-foundations.md](./01-foundations.md#8-the-dark-theme-is-an-inversion).

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
<div class="fp-sub fp-sub--borderless">A sub element with no border.</div>
```

A main element's shadow is offset **equally and positively** on both
axes, so it reads as a block printed on the surface, falling to the
bottom-right. There is no upward shadow, no leftward shadow and no
four-sided band: the shadow's only variable is its size.

A sub element has no shadow at rest — the border is its outline, and the
shadow appears as it lifts. Add `.fp-sub--accent` to point at it, or
`.fp-sub--borderless` to remove the border and leave only the lift.

`.fp-sub--borderless` keeps the element's box exactly the same size in
every state, so applying it never shifts the layout.

---

## 8. A floating navigation island

An island nav is a navigation bar that floats at the bottom of the
viewport as a detached pill, filled with ordinary sub buttons.

```html
<nav class="fp-island-nav" aria-label="Island navigation">
  <a class="fp-btn fp-btn--sub is-current" href="#" aria-current="page">Home</a>
  <a class="fp-btn fp-btn--sub" href="#">Library</a>
</nav>
<div class="fp-island-nav-spacer" aria-hidden="true"></div>
```

Two rules make it work:

1. **The container is a main element.** It carries no border and a hard
   shadow. Without the shadow the pill would read as a strip of white
   stuck to the window rather than as an object floating over the page.
   Being pinned to the viewport, it never travels on hover — the shadow
   stays put; only the items inside it lift.

2. **The page reserves room for it.** A fixed island floats on top of
   the content, so `.fp-island-nav-spacer` reserves the room the island
   occupies; put it after the last piece of content.

The items are sub buttons: flat at rest, lifting on hover. The current
destination wears the accent border — the one sanctioned emphasis for a
sub element.

---

## 9. JavaScript

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
| Range progress | `input[type="range"]` — the `--fp-range-progress` custom property |

Everything degrades gracefully. A modal without JavaScript will not open,
but a tab list without JavaScript still renders as a row of tabs.

**The range slider is the clearest example of that rule.** Its progress
fill is drawn by a CSS gradient driven by the `--fp-range-progress`
custom property. The JavaScript keeps that property in step with the
input; without it the gradient falls back to `0%` and the bar is simply
**empty**. The control still works — it just does not pretend to know
its own value.

---

## 10. Performance

- No CSS framework, no build step, no runtime dependency.
- The whole system is about 60KB of CSS and 12KB of JavaScript, unminified.
- Shadows are the only expensive paint operation, and they are static
  zero-blur offsets that browsers cache as simple layers.
- The skeleton pulse is the only continuous animation. It respects
  `prefers-reduced-motion`.
