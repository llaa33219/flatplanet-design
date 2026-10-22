# 01 — Foundations

The token layer. Every component in FlatPlanet is assembled from the values
defined here — nothing is hardcoded in a component file except the value of
a modifier.

---

## 1. Colour

### 1.1 The two roles

FlatPlanet uses colour with two clearly separated roles.

**Main colour — BLP White (`#fefeff`)**

`--fp-surface` resolves to `#fefeff`. This is the default background of
cards, panels, menus, inputs, tables and modals. Most of the library is
white because white is the main colour, not because it is the absence of
a colour.

**Ink — BLP Dark (`#00193d`)**

`--fp-ink` is the single depth colour. It is used for:

- every hard shadow in the system
- the 4px border on sub elements
- primary text on tinted surfaces
- inverted surfaces (sidebars, footers, the navbar logo)

**Accent — BLP Blue (`#007bff`)**

`--fp-accent` is an accent, not a theme colour. It appears on:

- the single most important action in a view (one `fp-btn--primary`)
- focus rings
- text links
- the "info" alert border
- opt-in modifiers such as `fp-card--accent`

If a view contains more than one accent-filled element, the accent has
stopped meaning "important" and should be reduced to ink or a neutral
fill. See [03-usage.md](./03-usage.md#3-the-accent-discipline).

### 1.2 The raw palette

All 60 colours from `색깔-3.pdf` are exposed as raw tokens. The naming
pattern is `--fp-<hue>-<step>`.

**Blue**

| Token | Hex | Name in palette |
|-------|-----|-----------------|
| `--fp-blue` | `#007bff` | BLP BLUE |
| `--fp-blue-deep` | `#005bdd` | BLP DEEP BLUE |
| `--fp-blue-ultra-deep` | `#0026a3` | BLP ULTRA DEEP BLUE |
| `--fp-blue-soft` | `#7fbcff` | BLP SOFT BLUE |
| `--fp-blue-light` | `#dbedff` | BLP LIGHT BLUE |
| `--fp-blue-light-deep` | `#bdcbdb` | BLP LIGHT DEEP BLUE |
| `--fp-blue-light-ultra-deep` | `#8598ad` | BLP LIGHT ULTRA DEEP BLUE |
| `--fp-blue-neon` | `#00ddff` | BLP NEON BLUE |
| `--fp-blue-neon-plus` | `#00f2ff` | BLP NEON BLUE PLUS |
| `--fp-blue-cli-accent` | `#2fc2ff` | BLP CLI ACCENT BLUE |
| `--fp-blue-logo-sky` | `#00afff` | BLP LOGO SKY BLUE |
| `--fp-blue-logo-dark` | `#006dbd` | BLP LOGO DARK BLUE |
| `--fp-blue-paper` | `#f4f8fc` | BLP PAPER BLUE |
| `--fp-blue-bg` | `#eef5fc` | BLP BG BLUE |

**Red**

| Token | Hex | Name in palette |
|-------|-----|-----------------|
| `--fp-red` | `#ff0505` | BLP RED |
| `--fp-red-deep` | `#db0000` | BLP DEEP RED |
| `--fp-red-ultra-deep` | `#a30000` | BLP ULTRA DEEP RED |
| `--fp-red-soft` | `#ff7f7f` | BLP SOFT RED |
| `--fp-red-light` | `#ffdbdb` | BLP LIGHT RED |
| `--fp-red-light-deep` | `#dbbdbd` | BLP LIGHT DEEP RED |
| `--fp-red-light-ultra-deep` | `#ad8585` | BLP LIGHT ULTRA DEEP RED |
| `--fp-red-neon` | `#ff3f4a` | BLP NEON RED |

**Yellow**

| Token | Hex | Name in palette |
|-------|-----|-----------------|
| `--fp-yellow` | `#ffea00` | BLP YELLOW |
| `--fp-yellow-deep` | `#ebd700` | BLP DEEP YELLOW |
| `--fp-yellow-ultra-deep` | `#b2a400` | BLP ULTRA DEEP YELLOW |
| `--fp-yellow-soft` | `#ffeb7f` | BLP SOFT YELLOW |
| `--fp-yellow-light` | `#fff9bd` | BLP LIGHT YELLOW |
| `--fp-yellow-light-deep` | `#dbd9bd` | BLP LIGHT DEEP YELLOW |
| `--fp-yellow-light-ultra-deep` | `#adaa85` | BLP LIGHT ULTRA DEEP YELLOW |
| `--fp-yellow-neon` | `#fcff00` | BLP NEON YELLOW |

**Green**

| Token | Hex | Name in palette |
|-------|-----|-----------------|
| `--fp-green` | `#00d620` | BLP GREEN |
| `--fp-green-deep` | `#00b21b` | BLP DEEP GREEN |
| `--fp-green-ultra-deep` | `#007512` | BLP ULTRA DEEP GREEN |
| `--fp-green-soft` | `#6bd67b` | BLP SOFT GREEN |
| `--fp-green-light` | `#ccffd4` | BLP LIGHT GREEN |
| `--fp-green-light-deep` | `#bddbc1` | BLP LIGHT DEEP GREEN |
| `--fp-green-light-ultra-deep` | `#85ad8b` | BLP LIGHT ULTRA DEEP GREEN |
| `--fp-green-neon` | `#00ff0e` | BLP NEON GREEN |
| `--fp-green-paper` | `#eaf7ef` | BLP PAPER GREEN |
| `--fp-green-bg` | `#b8e1d8` | BLP BG GREEN |

**Purple**

| Token | Hex | Name in palette |
|-------|-----|-----------------|
| `--fp-purple` | `#ae00ff` | BLP PURPLE |
| `--fp-purple-deep` | `#9200d6` | BLP DEEP PURPLE |
| `--fp-purple-ultra-deep` | `#650094` | BLP ULTRA DEEP PURPLE |
| `--fp-purple-soft` | `#d67fff` | BLP SOFT PURPLE |
| `--fp-purple-light` | `#f4dbff` | BLP LIGHT PURPLE |
| `--fp-purple-light-deep` | `#d2bddb` | BLP LIGHT DEEP PURPLE |
| `--fp-purple-light-ultra-deep` | `#a085ad` | BLP LIGHT ULTRA DEEP PURPLE |
| `--fp-purple-neon` | `#fa00ff` | BLP NEON PURPLE |
| `--fp-purple-paper` | `#f1f0f5` | BLP PAPER PURPLE |
| `--fp-purple-bg` | `#d9b8e1` | BLP BG PURPLE |

**Neutrals and darks**

| Token | Hex | Name in palette |
|-------|-----|-----------------|
| `--fp-dark` | `#00193d` | BLP DARK |
| `--fp-dark-deep` | `#000a19` | BLP DEEP DARK |
| `--fp-dark-ultra-deep` | `#000309` | BLP ULTRA DEEP DARK |
| `--fp-dark-soft` | `#1e2b3d` | BLP SOFT DARK |
| `--fp-dark-light` | `#d4dce8` | BLP LIGHT DARK |
| `--fp-dark-light-deep` | `#c7cbd1` | BLP LIGHT DEEP DARK |
| `--fp-dark-light-ultra-deep` | `#94989e` | BLP LIGHT ULTRA DEEP DARK |
| `--fp-sub-dark` | `#3e4d5f` | BLP SUB DARK |

**White and paper**

| Token | Hex | Name in palette |
|-------|-----|-----------------|
| `--fp-white` | `#fefeff` | BLP WHITE |
| `--fp-white-deep` | `#fafcff` | BLP DEEP WHITE |
| `--fp-paper-orange` | `#f9f1e5` | BLP PAPER ORANGE |
| `--fp-paper-pink` | `#f1e8ec` | BLP PAPER PINK |
| `--fp-paper-lime` | `#f2f6ed` | BLP PAPER LIME |
| `--fp-bg-orange` | `#fcf5ee` | BLP BG ORANGE |
| `--fp-bg-gray` | `#f5f5f5` | BLP BG GRAY |
| `--fp-bg-brown` | `#d09c7b` | BLP BG BROWN |

### 1.3 Semantic tokens

Components never reference raw palette tokens. They reference the semantic
layer, which is what makes the dark theme possible without touching a
single component file.

**Surfaces**

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `--fp-surface` | `#fefeff` | `#1e2b3d` | The main surface. Cards, panels, menus, inputs. |
| `--fp-surface-raised` | `#fefeff` | `#27384f` | A surface above another surface. |
| `--fp-surface-sunken` | `#f5f5f5` | `#14202f` | Wells, tracks, table headers, sunken rows. |
| `--fp-page-bg` | `#f5f5f5` | `#000309` | The page canvas behind everything. |
| `--fp-surface-inverse` | `#000309` | `#fefeff` | Inverted surfaces such as the footer. |

**Ink**

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `--fp-ink` | `#00193d` | `#d4dce8` | The depth colour. Shadows, sub-element borders, inverted fills. |
| `--fp-ink-soft` | `#3e4d5f` | `#c7cbd1` | Secondary ink, muted text. |
| `--fp-ink-muted` | `#94989e` | `#94989e` | Hairline borders, disabled text. |
| `--fp-ink-faint` | `#c7cbd1` | `#2a3a52` | The lightest ink, used for rules and dividers. |

**Text**

| Token | Value | Use |
|-------|-------|-----|
| `--fp-text` | `#000309` | Body and heading text. |
| `--fp-text-muted` | `#3e4d5f` | Supporting copy, descriptions. |
| `--fp-text-subtle` | `#94989e` | Placeholders, hints, disabled text. |
| `--fp-text-inverse` | `#fefeff` | Text on ink fills. |
| `--fp-text-accent` | `#007bff` | Links. |

**Tints**

A tint is a background plus a matching foreground. They are always used as
a pair, which is why the foreground is a separate token rather than a
hardcoded colour.

| Background token | Foreground token | Meaning |
|------------------|------------------|---------|
| `--fp-tint-info` | `--fp-tint-info-fg` | Informational |
| `--fp-tint-success` | `--fp-tint-success-fg` | Success |
| `--fp-tint-warning` | `--fp-tint-warning-fg` | Warning |
| `--fp-tint-danger` | `--fp-tint-danger-fg` | Danger |
| `--fp-tint-neutral` | `--fp-tint-neutral-fg` | Neutral |

In the dark theme each tint maps to a deep background with a light
foreground, so contrast holds in both directions.

**Accent**

| Token | Value | Use |
|-------|-------|-----|
| `--fp-accent` | `#007bff` | Accent fills. One per view. |
| `--fp-accent-hover` | `#005bdd` | Accent fill on hover |
| `--fp-accent-active` | `#0026a3` | Accent fill, pressed |
| `--fp-accent-border` | `#007bff` | The accent as a **sub-element border** |
| `--fp-accent-ink` | `#0026a3` | Accent-coloured text that is not a link |

`--fp-accent-border` exists because the accent has a second sanctioned
use: as the border colour of a sub element that needs emphasising. It is
a separate token so that the border can be re-pointed without touching
every component that uses it — see [3.8 The accent border](#38-the-accent-border).

---

## 2. Radius

### 2.1 The 36px ceiling

`36px` is the maximum corner radius anywhere in the system. It is the
default for every container: cards, buttons, inputs, panels, modals,
drawers, menus, tables, badges at large size, avatars at square size.

A radius larger than 36px is never used. A radius smaller than 36px is
used only where the component's height makes a 36px radius physically
unreadable — at 36px tall, a 36px radius turns the element into a circle
and the shape stops reading as a control.

### 2.2 The scale

| Token | Value | Applied to | Why |
|-------|-------|-----------|-----|
| `--fp-radius-lg` | `36px` | Hero panels, large surfaces | The ceiling. |
| `--fp-radius-md` | `36px` | Buttons, inputs, cards, panels | The default. |
| `--fp-radius` | `36px` | Generic default | The ceiling. |
| `--fp-radius-sm` | `18px` | Elements under 48px tall | Height forces a smaller radius. |
| `--fp-radius-xs` | `12px` | Elements under 32px tall | Height forces a smaller radius. |
| `--fp-radius-pill` | `36px` | Chips, switches, progress bars | Capped at the ceiling. |
| `--fp-radius-circle` | `50%` | Avatars, radio buttons, status dots | Only for true circles. |

The `--fp-radius-pill` token is worth noting: a pill-shaped control
normally uses `9999px`, but FlatPlanet caps it at 36px so the system's
silhouette stays consistent. At typical pill heights (36–40px) the two
are visually identical anyway.

---

## 3. Elevation

### 3.1 The two element types

The system distinguishes two kinds of element, and the kind decides both
its border and its shadow.

| | **Main element** | **Sub element** |
|---|---|---|
| **Examples** | Cards, panels, buttons, modals, hero, stat tiles | List items, tabs, chips, tags, inputs, badges |
| **Border** | **None** | **4px** (`--fp-border-width`), 2px under 40px tall |
| **Shadow** | Full-strength ink, hard, offset equally on X and Y | **None at rest** — it appears on hover |
| **On hover** | Presses **down**, shadow shrinks | **Lifts up**, shadow appears |
| **Purpose** | Floats above the page | Sits inside a main element |

The rule is simple: a main element's shadow *is* its outline. Adding a
border on top of the shadow would double the outline and make the element
look heavier than it should. A sub element has no room to cast a full
shadow, so it gets a border instead — and its resting state is **flat**.
The border alone carries the outline until the pointer arrives, at which
point the element lifts and the shadow appears with it.

### 3.2 The shadow contract

**Every shadow in the library is `(positive px) (positive px) 0 <ink>`.**

That is the whole contract, and it is not negotiable:

- both offsets are **positive**
- both offsets are **equal**
- the blur radius is **0**
- the spread is **0**

```css
box-shadow: 6px 6px 0 var(--fp-shadow-color);
```

Three consequences follow, and all three are mandatory.

**A shadow always falls to the bottom-right.** There is no upward
shadow, no leftward shadow, and no diagonal that leans anywhere else.
The light source sits in the top-left corner, so the ink falls to the
bottom-right like a print on paper. If you want a different shadow, you
want a different *size* — never a different direction.

**There is no four-sided band.** A shadow with a positive spread
(`0 0 0 6px`) paints ink on all four sides. That is a border, not a
shadow, and it is forbidden. When an element needs an outline on every
side, it needs a real `border:` declaration — which is exactly what a
sub element already has.

**The offsets are equal.** Equal offsets are what make the shadow read as
a printed block rather than a glow. A shadow of `8px 8px 0` is the same
shape as `6px 6px 0`, only bigger.

The shadow colour is `--fp-shadow-color`, which is `--fp-ink`
(`#00193d`). The ink is the only depth colour in the system.

### 3.3 Sizes, not directions

Because a hard shadow keeps X and Y equal and always positive, a
directional *variant* has nothing left to express. The only two options
were "leans up-left" (illegal) and "identical to the default" (noise), so
the directional variants are gone.

What survives is the **size scale**. A variant changes how far the
shadow reaches, not where it points.

| Class | Shadow | Hover movement |
|-------|--------|-----------------|
| *(default)* | `6px 6px 0` | `translateY(4px)` |
| `.fp-elev--1` | `3px 3px 0` | `translateY(1px)` |
| `.fp-elev--2` | `6px 6px 0` | `translateY(4px)` |
| `.fp-elev--3` | `9px 9px 0` | `translateY(7px)` |
| `.fp-elev--4` | `14px 14px 0` | `translateY(12px)` |

There is no "down" modifier, because it would produce exactly the shadow
the default already produces. A variant that changes nothing but its
name is noise, and the library does not ship noise.

### 3.4 The hover invariant

**The direction of the movement and the direction of the shadow change
must always agree.**

| Movement | Shadow | Verdict |
|---|---|---|
| Down | Shrinks | Allowed — the press |
| Up | Appears | Allowed — the lift |
| Down | Grows | Allowed |
| Up | Shrinks or disappears | **Forbidden** |

A rising element must never lose its shadow. Rising is a sub element's
cue; the shadow appearing is what confirms it. The reverse — rising
while the shadow shrinks — describes an element floating away and getting
smaller, which is never what a hover means.

In practice this means main elements only ever press **down** and sub
elements only ever lift **up**.

### 3.5 The press and the lift

A main element rests on a shadow of height `H`. On hover:

1. the shadow collapses to a 2px block
2. the element descends by `H - 2px`

The shadow's absolute outer edge therefore never moves. The element
visibly presses **into** the surface it was floating on, and springs back
when the pointer leaves.

```css
.fp-elev:hover {
  box-shadow: 2px 2px 0 var(--fp-shadow-color);
  transform: translateY(calc((var(--fp-elev-h) - 2px)));
}
```

A sub element does the opposite. It rises by the sub-shadow height and
gains that shadow at the same time, so it lifts off the surface it was
resting on.

```css
.fp-sub:hover {
  box-shadow: var(--fp-elev-h-sub) var(--fp-elev-h-sub) 0 var(--fp-shadow-color-sub);
  transform: translateY(calc(var(--fp-elev-h-sub) * -1));
}
```

### 3.6 Shadow heights

| Token | Value | Use |
|-------|-------|-----|
| `--fp-elev-h` (default) | `6px` | Generic main element |
| `.fp-elev--1` | `3px` | Small main elements |
| `.fp-elev--2` | `6px` | Default |
| `.fp-elev--3` | `9px` | Cards, larger surfaces |
| `.fp-elev--4` | `14px` | Hero panels |
| `--fp-elev-h-sub` | `3px` | Sub elements |
| `.fp-sub--1` | `2px` | Dense sub elements |
| `.fp-sub--2` | `3px` | Default |
| `.fp-sub--3` | `5px` | Emphasised sub elements |

---

### 3.7 Shadow specification at a glance

| Property | Value |
|----------|-------|
| Shadow colour (light theme) | `#00193d` — BLP DARK |
| Shadow colour (dark theme) | `#000309` — BLP ULTRA DEEP DARK |
| Sub-element shadow | `rgba(0, 25, 61, 0.22)` |
| Blur radius | `0` — always |
| Offsets | **Positive and equal** on X and Y (`h h 0`) |
| Spread | `0` — always. A positive spread is a border, not a shadow |
| Direction | Bottom-right. Always. |
| Hover (main) | Shadow collapses to `2px`, element descends by `h - 2px` |
| Hover (sub) | Element rises by `h - sub`, shadow appears |
| Forbidden | Moving up while the shadow shrinks or disappears |

### 3.8 The accent border

The accent has exactly two sanctioned uses, and neither of them is "make
the element bigger" or "make the element move".

**One — as a sub element's border.** This is how a sub element gets
emphasised. The accent recolours the border that is already there; the
element keeps its size, its place and its resting flatness.

```html
<div class="fp-list__item fp-sub--accent">…</div>
```

`.fp-sub--accent` is the one mechanism. It is a generic modifier rather
than a per-component one (`.fp-list__item--accent`, `.fp-chip--accent`,
`.fp-tab--accent`, …) because a generic modifier can be attached to
*any* sub element, and a library with sixty components cannot afford
sixty accent modifiers. The colour travels through the
`--fp-sub-border-color` custom property rather than through a
`border-color` declaration, so the modifier never has to win a
specificity fight with the component's own border rule.

**Two — as a block of colour behind emphasised text.** See
[5. Typography](#5-typography) for the `fp-highlight` treatment.

---

### Why the ink changed to `#00193d`

`#000309` (BLP ULTRA DEEP DARK) is a near-black with a blue cast, and it
was the first ink used in the system. It reads as a hole rather than as
shadow — the eye treats near-black against white as a gap in the page
rather than as depth. `#00193d` is a deep navy that still belongs to the
palette but sits closer to the surface colours, so the band reads as
depth.

In the dark theme the ink inverts: `#d4dce8` (BLP LIGHT DARK) for borders
and inverted fills, while the shadow itself stays `#000309` so it reads as
shadow against the `#1e2b3d` surface.

### Why there is no four-sided band

The band used to be available as `.fp-elev--omni`, built from
`0 0 0 h` — a zero-blur shadow with a positive spread. It looked good,
and it was geometrically correct: the spread follows the element's own
`border-radius` exactly, so the corners stayed clean where four stacked
offset shadows would have left notches.

It is gone because it is not a shadow. A band on all four sides is an
outline, and the system already has a primitive for outlines: the real
inline `border:` that every sub element carries. Two primitives for the
same job is one too many, and the band quietly broke the rule that made
the library feel like one thing — one light source, in the top-left
corner, with every shadow falling to the bottom-right.

An element that needs an outline on every side now uses a border. An
element that needs depth uses a shadow. The two never swap.

---

## 4. Motion

Three durations, no exceptions.

| Token | Value | Use |
|-------|-------|-----|
| `--fp-duration-fast` | `0.1s` | Micro-feedback: colour swaps, small translations, checkmarks |
| `--fp-duration-default` | `0.2s` | The default. Hover presses, lifts, background changes |
| `--fp-duration-slow` | `0.3s` | Larger movements: drawers, progress bars, toast entry |

Three easing curves:

| Token | Value | Use |
|-------|-------|-----|
| `--fp-ease` | `cubic-bezier(0.4, 0, 0.2, 1)` | Default. Symmetric, settles cleanly |
| `--fp-ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Entrances that overshoot slightly |
| `--fp-ease-in-out` | `cubic-bezier(0.65, 0, 0.35, 1)` | Elements that move in both directions |

### The standard bundle

```css
transition:
  background-color var(--fp-duration-default) var(--fp-ease),
  color            var(--fp-duration-default) var(--fp-ease),
  border-color     var(--fp-duration-default) var(--fp-ease),
  box-shadow       var(--fp-duration-default) var(--fp-ease),
  transform        var(--fp-duration-default) var(--fp-ease),
  opacity          var(--fp-duration-fast)  var(--fp-ease);
```

Opacity is on the fast curve on purpose: fading should not feel slow even
when the movement does.

### Reduced motion

A global `prefers-reduced-motion` block collapses all durations to
`0.01ms` and disables the skeleton shimmer. Hover transforms are
neutralised but colour changes are kept, so the interface remains legible
without motion.

---

## 5. Typography

The system uses Inter, falling back to Pretendard for Korean glyphs.

| Token | Size | Typical use |
|-------|------|-------------|
| `--fp-text-6xl` | `72px` | Hero display |
| `--fp-text-5xl` | `56px` | Page title |
| `--fp-text-4xl` | `44px` | Section title |
| `--fp-text-3xl` | `36px` | Large heading, stat value |
| `--fp-text-2xl` | `30px` | Sub-heading |
| `--fp-text-xl` | `24px` | Card title, modal title |
| `--fp-text-lg` | `20px` | Sub-heading, list title |
| `--fp-text-md` | `18px` | Lead paragraph, accordion trigger |
| `--fp-text-base` | `16px` | Body |
| `--fp-text-sm` | `14px` | Secondary text, table cells, labels |
| `--fp-text-xs` | `12px` | Captions, badges, metadata |
| `--fp-text-2xs` | `11px` | Overline labels |

Headings are set at weight `800` with a `-0.02em` letter-spacing and
`text-wrap: balance`. Body copy uses `text-wrap: pretty` so lines break
without leaving orphans.

**The kicker** is a recurring overline pattern: 12px, weight 800, uppercase,
`0.14em` letter-spacing, in the accent colour. It appears once per
section, immediately above a heading.

**The lead** is a section-level intro paragraph: 18px, muted colour,
`1.7` line height, capped at 640px wide.

### Highlighted text

When the accent emphasises *words* rather than an element, the treatment
is a **rectangular block of accent colour** behind bold text:

```html
<p>Some <strong class="fp-highlight">emphasised words</strong> in a sentence.</p>
```

| Rule | Value | Why |
|------|-------|-----|
| Weight | `800` | The words must read as emphasised even without colour. |
| Background | `--fp-accent` (`#007bff`) | The accent itself. |
| Shape | A plain rectangle, `border-radius: 0` | A pill would soften the accent into a shape the system does not use. |
| Text colour | `--fp-white` | `#007bff` is a mid-dark blue; white is the readable colour on top of it. |

The class works on `<strong>` and on `<mark>` alike.

`mark` is the **neutral** sibling of the same idea: it keeps its own
yellow identity, so an ordinary editorial highlight does not spend the
accent. The two are consistent — both are bold, both are rectangles with
no radius — but they are not the same. `mark` is a primitive for
marking something in a document; `fp-highlight` is the accent-emphasis
primitive. A `<mark class="fp-highlight">` takes the accent treatment,
because the more specific class is declared last.

---

## 6. Spacing

A 4px base scale.

| Token | Value | | Token | Value |
|-------|-------|-|-------|-------|
| `--fp-space-1` | `4px` | | `--fp-space-10` | `40px` |
| `--fp-space-2` | `8px` | | `--fp-space-12` | `48px` |
| `--fp-space-3` | `12px` | | `--fp-space-16` | `64px` |
| `--fp-space-4` | `16px` | | `--fp-space-20` | `80px` |
| `--fp-space-5` | `20px` | | `--fp-space-24` | `96px` |
| `--fp-space-6` | `24px` | | `--fp-space-32` | `128px` |
| `--fp-space-8` | `32px` | | | |

Sections are separated by `--fp-space-20` (80px) vertically, or
`--fp-space-12` (48px) for tighter groupings.

---

## 7. Layout

| Token | Value | Use |
|-------|-------|-----|
| `--fp-container` | `1200px` | Default content width |
| `--fp-container-wide` | `1440px` | Wide layouts |
| `--fp-container-narrow` | `760px` | Article and prose |

The responsive grid collapses in three steps: 4 columns → 2 at 768px →
1 at 560px.

| Breakpoint | Behaviour |
|-----------|-----------|
| `1024px` | Footer grid becomes 2 columns; feature panels stack and centre |
| `768px` | 4- and 3-column grids become 2 columns; sidebar goes full width; toasts go full width |
| `560px` | All grids become 1 column; headings step down a size |
