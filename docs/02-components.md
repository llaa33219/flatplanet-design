# 02 — Components

Every component, with its markup, its modifiers and the behaviour that
cannot be inferred from the CSS alone.

Throughout, **main** marks an element with the full ink shadow and no
border; **sub** marks an element with the 4px border, no resting shadow,
that lifts on hover and gains one as it goes.

Every shadow in the library is `(positive px) (positive px) 0 <ink>` — it
always falls to the bottom-right, with zero blur and zero spread. There
is no four-sided band and no directional variant; a shadow differs only
in its **size**.

---

## 0. The accent treatments

The accent (`#007bff`) has two sanctioned uses, and both of them are
about emphasis rather than decoration.

### The accent border — `.fp-sub--accent`

A sub element may wear the accent as its border colour. This is the
sanctioned way to draw the eye to one specific sub element: it recolours
the border that is already there, so the element keeps its size, its
place and its flat resting state.

```html
<div class="fp-list__item fp-sub--accent">
  <div class="fp-list__content">
    <div class="fp-list__title">Storage at 72%</div>
    <div class="fp-list__meta">2 hours ago</div>
  </div>
</div>
```

| Rule | Value |
|------|-------|
| Border colour | `--fp-accent-border` (`#007bff`) |
| Border width | Unchanged — 4px, or 2px under 40px tall |
| Resting shadow | Still none. The accent border is not a shadow |
| Hover | Unchanged: the element lifts and its shadow appears |

The accent **border** is the bright blue (`#007bff`) and the accent
**fill** is the deep step (`#005bdd`). They are two decisions: a border
is a line and has to be seen; a fill carries white text, and white on
`#007bff` is only 3.95:1 while white on `#005bdd` is 5.88:1.

One modifier, applied to any sub element:

```html
<div class="fp-list__item fp-sub--accent">…</div>
<div class="fp-chip fp-sub--accent">…</div>
<div class="fp-tab fp-sub--accent">…</div>
```

It is a **generic** modifier rather than a per-component one
(`.fp-list__item--accent`, `.fp-chip--accent`, `.fp-tab--accent`, …) for
one reason: with sixty components in the library, sixty accent modifiers
would be a worse API than one. The colour travels through the
`--fp-sub-border-color` custom property, so the modifier never has to
out-specify the component's own `border:` rule — it just sets the
property, and the border declaration reads it.

Do not put an accent border on everything. The accent border is a
pointer, not a decoration; more than one per view and it stops pointing
at anything.

### The accent fill on a control — `.fp-check--accent` and `.fp-switch--accent`

A checked checkbox and an ON switch fill with the **ink** by default,
because a checked control is a statement about the state of a form, not
an emphasis. Sometimes exactly one control has to be pointed at instead —
the settings row that is the subject of the screen, say — and then the
accent does the pointing.

```html
<label class="fp-check fp-check--accent">
  <input type="checkbox" checked>
  <span class="fp-check__box"></span>
  <span class="fp-check__label">Remember this device</span>
</label>

<label class="fp-switch fp-switch--accent">
  <input type="checkbox" checked>
  <span class="fp-switch__track"><span class="fp-switch__thumb"></span></span>
  <span>Enable notifications</span>
</label>
```

| Rule | Value |
|------|-------|
| Checked / ON fill | `--fp-accent-fill` (`#005bdd`) |
| Tick mark and radio dot | `--fp-on-accent` (`#fefeff`) — always white |
| Unchecked / OFF | **Unchanged.** White surface, ink border, no accent anywhere |
| Resting shadow | None — a control is a sub element |
| Hover | Unchanged: the control lifts and its shadow appears |

The radio takes the same modifier: `fp-check--radio fp-check--accent`.

**The OFF state stays neutral in both variants.** A control that is off
should not shout: an accent-coloured unchecked box would be a claim
about a state that has not happened. The accent appears only once the
control is actually on.

The tick stays white in both variants, so the mark reads as a mark and
not as part of the fill.

### The highlight — `.fp-highlight`

When the accent emphasises *words* rather than an element, the treatment
is bold text on a plain rectangle of accent colour.

```html
<p>Some <strong class="fp-highlight">emphasised words</strong> in a sentence.</p>
```

| Rule | Value |
|------|-------|
| Font weight | `800` — bold |
| Background | `--fp-accent-fill` (`#005bdd`) |
| Border radius | `0` — a plain rectangle, not a pill |
| Text colour | `--fp-white` |
| Works on | `<strong>`, `<mark>`, `<span>`, any inline element |

`mark` is the neutral sibling of the same treatment. It keeps its own
yellow identity — an ordinary editorial highlight should not spend the
accent — but it follows the same shape rules, so the two read as one
family: bold, rectangular, no radius. A `<mark class="fp-highlight">`
takes the accent treatment.

---

## 1. The quietest sub element

### The borderless sub element — `.fp-sub--borderless`

A sub element with **no border at all**. It is still a sub element in
every other respect: flat at rest, and on hover it lifts and its shadow
appears.

```html
<a class="fp-navbar__link fp-sub--borderless" href="#">Foundations</a>
```

This is the **third tier** of the element model, and it is the one to
reach for when a sub element should be *present* but should not compete
for attention.

| Tier | Border | Resting shadow | Hover |
|------|--------|----------------|-------|
| Main element | none | hard shadow | presses down, shadow shrinks |
| Sub element | 4px | none | lifts, shadow appears |
| **Borderless sub** | **none** | **none** | **lifts, shadow appears** |

A row of bordered navbar links reads as a row of boxes. A row of
borderless links reads as a list of places.

**Why the modifier is a custom property.** It is written as

```css
.fp-sub--borderless {
  --fp-sub-border-width: 0;
  --fp-sub-border-width-sm: 0;
}
```

rather than as `border: none`, for two reasons.

*First*, `border: none` would lose the cascade: the component's own
`border:` rule lives in `components.css`, which is loaded after
`elevation.css`.

*Second* — and this is the important one — a component such as
`.fp-navbar__link` declares its border as
`border: 4px solid transparent`, not `border: none`. The transparent
border still **occupies space**, so when the link becomes active and
takes a real border colour, nothing around it moves. Setting the *width*
to zero removes the border while keeping the box exactly the size it was,
so **no neighbour ever moves**.

Every sub element in the library reads its border width from
`--fp-sub-border-width`, in the same way it already read its border
colour from `--fp-sub-border-color`. The modifier therefore works on any
sub element, with no specificity fight and no dependence on stylesheet
order.

The border *colour* is deliberately left alone: it is meaningless at
width zero, and a later `.fp-sub--accent` on the same element must still
be able to set it.

### The island nav — `.fp-island-nav`

A navigation bar that floats at the bottom of the viewport as a
detached, pill-shaped island.

```html
<nav class="fp-island-nav" aria-label="Island navigation">
  <a class="fp-island-nav__item is-active" href="#">Home</a>
  <a class="fp-island-nav__item" href="#">Foundations</a>
  <a class="fp-island-nav__item" href="#">Components</a>
</nav>

<!-- The room the island needs, so the last content is never trapped. -->
<div class="fp-island-nav-spacer" aria-hidden="true"></div>
```

| Part | Kind | Treatment |
|------|------|-----------|
| `.fp-island-nav` | **Main** | Fixed to the bottom, centred, 36px radius, **no border**, a 6px hard shadow |
| `.fp-island-nav__item` | **Sub** | No resting shadow; lifts 2px on hover and its shadow appears |
| `.fp-island-nav__item.is-active` | Sub | Fills with the ink and inverts its text |
| `.fp-island-nav-spacer` | Utility | Reserves the room the fixed island occupies |

**The container is a main element.** An island is *detached*: it floats
above the page rather than sitting inside it, so the shadow is what
makes it read as an object hovering over the content. That is why it
carries the main treatment — no border, a hard down-right shadow — and
why it presses **down** on hover, like every other main element.

The items inside it are **sub elements**: flat at rest, lifting on hover.

**It must not trap the content.** A fixed island sits on top of the page,
so without help the last row of a table or the final card ends up
underneath it. The `.fp-island-nav-spacer` utility reserves that room;
put it at the end of the page, after the last piece of content.

**Reduced motion** is respected: the global `prefers-reduced-motion`
block neutralises the island's press, keeping the centring translate.

---

## 2. Buttons

Main elements. The shadow is their outline, so they carry no border.

```html
<button class="fp-btn fp-btn--primary">Get Started</button>
```

### Variants

| Class | Fill | When to use |
|-------|------|-------------|
| `fp-btn--primary` | Accent blue, white text | **Once per view.** The main action. |
| `fp-btn--secondary` | White surface, ink text | Everything else that needs a button. |
| `fp-btn--ghost` | Transparent | Tertiary actions, icon buttons in a toolbar |
| `fp-btn--dark` | `#000309` | Actions on a light surface that need weight without the accent |
| `fp-btn--light` | White | Actions on a dark or tinted surface |
| `fp-btn--danger` | Red | Destructive actions only |
| `fp-btn--success` | Green | Confirming a positive outcome |
| `fp-btn--warning` | Yellow | Actions that need caution but not destruction |

### Sizes

| Class | Height | Radius | Shadow |
|-------|--------|--------|--------|
| `fp-btn--lg` | `60px` | `36px` | `5px` |
| *(default)* | `48px` | `36px` | `4px` |
| `fp-btn--sm` | `36px` | `18px` | `3px` |
| `fp-btn--xs` | `28px` | `12px` | `2px` |

The radius steps down with the height. A 36px-tall button cannot carry a
36px radius and still read as a button, so it takes 18px.

### Other modifiers

- `fp-btn--block` — full width
- `fp-btn--pill` — pill shape
- `fp-btn--square` — `12px` radius
- `fp-btn--icon` — square, icon only; combine with a size class
- `fp-btn-group` — a row of buttons with `--tight` and `--attached` variants

### Icons

Icons sit in an `fp-btn__icon` wrapper so they can shift on hover.

```html
<button class="fp-btn fp-btn--primary">
  <span class="fp-btn__icon fp-btn__icon--start">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2.5"
         stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 5v14M5 12h14"/>
    </svg>
  </span>
  Add Item
</button>
```

The start icon nudges left on hover, the end icon nudges right. Give every
icon-only button an `aria-label`.

### States

`disabled` and `aria-disabled="true"` drop the shadow entirely and reduce
opacity to 40%. The button does not press on hover.

---

## 3. Form controls

Sub elements. All carry a 4px border and lift by 2px on hover.

### Field wrapper

```html
<div class="fp-field">
  <label class="fp-field__label" for="f-name">
    Full name <span class="fp-field__required">*</span>
  </label>
  <input class="fp-input" id="f-name" type="text" placeholder="Ada Lovelace">
  <span class="fp-field__hint">As it appears on your ID.</span>
</div>
```

| Class | Purpose |
|-------|---------|
| `fp-field__label` | The label. Use a real `<label>` with a `for` attribute. |
| `fp-field__required` | The asterisk. |
| `fp-field__hint` | Secondary help text. |
| `fp-field__error` | Validation message, in danger colour. |
| `fp-field__success` | Validation confirmation. |

### Inputs

```html
<input class="fp-input" type="text">
<input class="fp-input is-invalid" type="email">
<input class="fp-input is-valid" type="text">
<select class="fp-select"><option>Starter</option></select>
<textarea class="fp-textarea"></textarea>
```

Size modifiers: `fp-input--sm` (36px), `fp-input--lg` (60px).

### Input group

```html
<div class="fp-input-group">
  <span class="fp-input-group__addon">https://</span>
  <input class="fp-input" type="text" value="flatplanet.dev">
</div>
```

Addons are sunken surfaces with a 4px border. The group rounds only at
its outer corners.

### Search

```html
<div class="fp-search">
  <span class="fp-search__icon">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2.5"
         stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>
    </svg>
  </span>
  <input class="fp-input" type="search" placeholder="Search…">
</div>
```

### Checkbox and radio

```html
<label class="fp-check">
  <input type="checkbox" checked>
  <span class="fp-check__box"></span>
  <span class="fp-check__label">Remember this device</span>
</label>

<label class="fp-check fp-check--radio">
  <input type="radio" name="plan" checked>
  <span class="fp-check__box"></span>
  <span class="fp-check__label">Monthly billing</span>
</label>
```

The native input is visually hidden but stays in the tab order. The box
is a 2px-bordered square (circle for radio) that lifts on hover. The
checked state fills with ink, not accent — a checked box is a fact about
the state, not an emphasis — unless the control carries
[`fp-check--accent`](#the-accent-fill-on-a-control--fp-check--accent-and-fp-switch--accent),
which fills it with the accent instead and keeps the tick white.

`fp-check--card` wraps the whole control in a bordered card that highlights
when checked.

### Switch

```html
<label class="fp-switch">
  <input type="checkbox" checked>
  <span class="fp-switch__track"><span class="fp-switch__thumb"></span></span>
  <span>Enable notifications</span>
</label>
```

The OFF track is a neutral sunken surface with an ink border; the ON
track fills with the ink. `fp-switch--accent` fills the ON track with the
accent instead — and leaves the OFF track exactly as it was.

### Range

```html
<input class="fp-range" type="range" min="0" max="100" value="65">
```

**The thumb is a horizontal rectangle that sits inside the track.** It is
not a disc riding on top of the rail: a handle that hangs over both edges
of the track reads as a separate object sitting on the slider rather
than as a handle *in* it.

| Part | Size |
|------|------|
| Track | 18px tall, 2px border, 36px radius |
| Thumb | 10px tall × 28px wide, 2px border, 12px radius |
| `margin-top` | 2px (Chromium correction) |

The geometry is exact, and it was measured in Chromium and Firefox:

| | Value |
|---|---|
| Track (rendered) | 18px tall |
| Thumb (rendered) | 10px tall × 28px wide |
| Thumb centre vs track centre | **delta 0** — exactly centred in both engines |
| Thumb inside the track | **yes** — 4px of clearance above and below |
| Thumb width vs height | 28px wide, 10px tall — clearly a rectangle |

The `margin-top` is the vertical correction for Chromium, where a native
thumb is positioned by its top edge. The obvious arithmetic is wrong by
exactly the track's border width:

```
margin-top = (track height - thumb height) / 2 = (18 - 10) / 2 = 4px   WRONG
```

Chromium aligns the thumb's top edge against the INNER edge of the
track, and the track's 2px border is inside its 18px box — so the thumb
already starts 2px below the track's top edge. The correction is the
remainder, not the whole:

```
margin-top = (track height - thumb height) / 2 - track border width
           = (18 - 10) / 2 - 2
           = 2px
```

Measured by painting the track and the thumb in flat probe colours and
scanning the rendered pixels, at `deviceScaleFactor: 2`:

| `margin-top` | Chromium thumb centre vs track centre |
|---|---|
| 0px | −2px |
| 1px | −1px |
| **2px** | **0 — centred** |
| 3px | +1px |
| 4px | +2px |

Firefox centres a `::-moz-range-thumb` on the track by itself and ignores
`margin-top` entirely — measured at 0px, 2px and 4px the thumb lands
within a pixel of the track centre every time — so the same 2px is a
no-op there and the handle lands in the identical place in both
engines. `box-sizing: border-box` is declared on both pseudo-elements,
because browser pseudo-elements are not matched by the global `*` reset
and would otherwise be content-box.

**The progress fill.** The filled portion of the track is a gradient on
the track itself, driven by the `--fp-range-progress` custom property.
The JavaScript in `flatplanet.js` keeps that property in step with the
input.

Without JavaScript the property is unset, the gradient falls back to
`0%`, and the bar is simply **empty**. That is the honest degradation:
the control still works, it just does not claim to know its own value.

The fill is the **ink**, not the accent. The accent is budgeted to one
element per view, and a slider that is being dragged is not the most
important thing on the screen.

The hover behaviour is unchanged: the thumb lifts 2px and its hard
shadow appears — it is a sub element, and a rising element never loses
its shadow.

---

## 4. Badges, tags and chips

### Badge

Sub elements. A 2px border at the default size.

```html
<span class="fp-badge">Draft</span>
<span class="fp-badge fp-badge--success fp-badge--dot">Healthy</span>
<span class="fp-badge fp-badge--accent">New</span>
```

| Modifier | Appearance |
|----------|-----------|
| *(default)* | White surface, ink border, ink text |
| `fp-badge--accent` | Accent fill, white text, no border |
| `fp-badge--success` | Green fill, white text |
| `fp-badge--danger` | Red fill, white text |
| `fp-badge--warning` | Yellow fill, dark text |
| `fp-badge--info` | Tinted info background |
| `fp-badge--neutral` | Grey fill |
| `fp-badge--outline` | Transparent fill |
| `fp-badge--soft` | Tinted, no border |
| `fp-badge--dot` | Adds a status dot before the label |
| `fp-badge--lg` | 34px tall, 18px radius |

### Tag

A removable label.

```html
<span class="fp-tag">
  Design System
  <button class="fp-tag__remove" aria-label="Remove Design System">
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="3" stroke-linecap="round">
      <path d="M18 6L6 18M6 6l12 12"/>
    </svg>
  </button>
</span>
```

### Chip

A selectable filter.

```html
<button class="fp-chip" aria-pressed="true">UI</button>
<button class="fp-chip" aria-pressed="false">Docs</button>
```

The pressed state fills with ink and inverts the text. Chips use
`aria-pressed`; the JavaScript in `flatplanet.js` toggles it.

### Avatar

```html
<span class="fp-avatar fp-avatar--lg">AR</span>
<span class="fp-avatar"><img src="…" alt=""></span>
```

Sizes: `--sm` (32px), default (48px), `--lg` (64px), `--xl` (96px).
`fp-avatar--square` swaps the circle for a 36px radius.

Colour modifiers: `--accent`, `--red`, `--yellow`, `--green`, `--purple`,
`--dark`. The default is a grey fill with an ink border, so avatars do not
compete with the accent.

Stack several with `fp-avatar-group`.

### Icon tile

```html
<span class="fp-icon-tile fp-icon-tile--sm">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
       stroke="currentColor" stroke-width="3" stroke-linecap="round"
       stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
</span>
```

Sizes: `--sm` (40px), default (56px), `--lg` (72px). A main element: it
carries no border, and on hover it presses down 1px while its shadow
contracts from 3px to 2px.

---

## 5. Cards

Main elements. No border — the shadow is the outline.

```html
<article class="fp-card">
  <div class="fp-card__media"><img src="…" alt=""></div>
  <div class="fp-card__body">
    <h3 class="fp-card__title">Composition</h3>
    <p class="fp-text-sm fp-text-muted">Build layouts from stacked blocks.</p>
  </div>
  <div class="fp-card__footer">
    <span class="fp-badge fp-badge--accent">New</span>
    <button class="fp-btn fp-btn--ghost fp-btn--sm">Learn more</button>
  </div>
</article>
```

| Part | Purpose |
|------|---------|
| `fp-card__header` | Title row, separated by a hairline rule |
| `fp-card__body` | Main content. `--tight` reduces padding to 16px. |
| `fp-card__footer` | Actions, on a sunken background |
| `fp-card__media` | 16:9 image or media area |

| Modifier | Effect |
|----------|--------|
| `fp-card--flat` | No shadow. For cards nested inside another card. |
| `fp-card--outlined` | A 4px border instead of a shadow — a sub element, so it is flat at rest and lifts on hover |
| `fp-card--accent` | Accent-coloured shadow |
| `fp-card--interactive` | Adds a pointer cursor |
| `fp-card--sm` / `fp-card--lg` | Shadow height 3px / 7px |

**Nesting rule.** A card inside a card should use `fp-card--flat`. The
inner card's job is to organise content, not to cast a second shadow.

---

## 6. Lists

```html
<div class="fp-list">
  <div class="fp-list__item">
    <span class="fp-icon-tile fp-icon-tile--sm fp-icon-tile--green">…</span>
    <div class="fp-list__content">
      <div class="fp-list__title">Backup complete</div>
      <div class="fp-list__meta">12 minutes ago</div>
    </div>
  </div>
</div>
```

Items are sub elements: 4px border, lift on hover.
`fp-list__item--active` fills with grey.

---

## 7. Tabs

```html
<div class="fp-tabs" role="tablist">
  <button class="fp-tab" role="tab" aria-selected="true">Overview</button>
  <button class="fp-tab" role="tab" aria-selected="false">Activity</button>
  <button class="fp-tab" role="tab" aria-selected="false">Settings</button>
</div>
```

| Modifier | Effect |
|----------|--------|
| `fp-tabs--pill` | No container background; the active tab fills with ink |
| `fp-tabs--underline` | Underline style, active tab marked with a bottom rule |

The selected tab is a white surface with a 3px ink shadow, sitting on the
sunken container. The JavaScript manages `aria-selected`.

---

## 8. Accordion

Built on native `<details>` so keyboard behaviour comes for free.

```html
<details class="fp-accordion__item" open>
  <summary class="fp-accordion__trigger">
    <span>What is the 36px radius rule?</span>
    <span class="fp-accordion__icon">…</span>
  </summary>
  <div class="fp-accordion__panel">…</div>
</details>
```

The icon is a plus that rotates 45° to become a cross when open. The open
item gains a 3px ink shadow.

The lighter `fp-disclosure` component is the alternative for secondary
information:

```html
<details class="fp-disclosure">
  <summary class="fp-disclosure__summary">
    Disclosure with a chevron
    <svg class="fp-disclosure__chevron" …>…</svg>
  </summary>
  <div class="fp-disclosure__body">…</div>
</details>
```

---

## 9. Tables

```html
<div class="fp-table-wrap">
  <table class="fp-table">
    <thead>
      <tr>
        <th>Component</th>
        <th class="fp-table__num">Shadow</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Button</td><td class="fp-table__num">4px</td></tr>
    </tbody>
  </table>
</div>
```

The wrapper carries a 5px ink shadow and handles horizontal overflow.
`fp-table--striped` adds alternating row fills. `fp-table__num` right-aligns
and switches to a monospace, tabular-numeral face.

---

## 10. Progress and meters

```html
<div class="fp-meter">
  <div class="fp-meter__head"><span>Uptime</span><span>99.98%</span></div>
  <div class="fp-progress">
    <div class="fp-progress__bar fp-progress__bar--success" style="width: 99%"></div>
  </div>
</div>
```

The default bar is ink. `fp-progress__bar--accent`, `--success`,
`--danger` and `--warning` are available but should be used
sparingly — a progress bar is usually not a status indicator.

Sizes: `fp-progress--sm` (12px), default (18px), `fp-progress--lg` (26px).

### Circular progress

```html
<div class="fp-ring">
  <svg width="120" height="120" viewBox="0 0 120 120">
    <circle class="fp-ring__track" cx="60" cy="60" r="52"
            fill="none" stroke-width="12"/>
    <circle class="fp-ring__fill" cx="60" cy="60" r="52"
            fill="none" stroke-width="12"
            stroke-dasharray="326.7" stroke-dashoffset="65.3"/>
  </svg>
  <span class="fp-ring__label">80%</span>
</div>
```

---

## 11. Alerts

```html
<div class="fp-alert fp-alert--warning">
  <span class="fp-alert__icon">…</span>
  <div class="fp-alert__content">
    <div class="fp-alert__title">Storage almost full</div>
    You have used 92% of your storage quota.
  </div>
</div>
```

| Modifier | Background | Border |
|----------|-----------|--------|
| *(default)* | White | Ink, 6px left edge |
| `fp-alert--info` | Info tint | Accent |
| `fp-alert--success` | Success tint | Green |
| `fp-alert--warning` | Warning tint | Yellow |
| `fp-alert--danger` | Danger tint | Red |

The left border is 6px on every variant so the alert keeps a consistent
silhouette regardless of severity.

An alert is a **sub element**: it carries a 4px inline border and has no
resting shadow. On hover it lifts and the shadow appears, like any other
sub element.

---

## 12. Stat tiles

```html
<div class="fp-stat">
  <span class="fp-stat__label">Components</span>
  <span class="fp-stat__value">60</span>
  <span class="fp-stat__delta fp-stat__delta--up">↑ 12 this month</span>
</div>
```

Main elements with a 5px ink shadow. On hover the tile presses **down**
3px and the shadow collapses to 2px — the same press every main element
uses.

---

## 13. Breadcrumbs

```html
<nav class="fp-breadcrumb">
  <a class="fp-breadcrumb__item" href="#">Home</a>
  <span class="fp-breadcrumb__sep">/</span>
  <a class="fp-breadcrumb__item" href="#">Projects</a>
  <span class="fp-breadcrumb__sep">/</span>
  <span class="fp-breadcrumb__item">FlatPlanet</span>
</nav>
```

---

## 14. Pagination

```html
<nav class="fp-pagination">
  <a class="fp-pagination__item" href="#">1</a>
  <a class="fp-pagination__item is-active" href="#">2</a>
  <span class="fp-pagination__ellipsis">…</span>
  <a class="fp-pagination__item" href="#">12</a>
</nav>
```

The active page fills with ink. Disabled pages use `is-disabled`.

---

## 15. Segmented control

```html
<div class="fp-segment">
  <button class="fp-segment__item is-active">Day</button>
  <button class="fp-segment__item">Week</button>
  <button class="fp-segment__item">Month</button>
</div>
```

The active segment is a white surface with a 3px ink shadow on the sunken
container.

---

## 16. Tooltip

CSS only, no JavaScript.

```html
<span class="fp-tooltip">
  <button class="fp-btn fp-btn--icon fp-btn--ghost">…</button>
  <span class="fp-tooltip__content">Copy to clipboard</span>
</span>
```

Positions: `--bottom`, `--right`. The tooltip is not keyboard-reachable —
for content that must be announced, use `title` or an `aria-describedby`
reference as well.

---

## 17. Timeline

```html
<div class="fp-timeline">
  <div class="fp-timeline__item">
    <span class="fp-timeline__dot">…</span>
    <div class="fp-timeline__content">
      <div class="fp-timeline__time">09:24</div>
      <div class="fp-text-md" style="font-weight:700">Pull request merged</div>
      <div class="fp-text-sm fp-text-muted">feat: add dark theme tokens</div>
    </div>
  </div>
</div>
```

The connector line is drawn by the item's `::before` pseudo-element and
is hidden on the last item.

---

## 18. Pricing cards

```html
<div class="fp-price-card fp-price-card--featured">
  <div>
    <div class="fp-text-xs fp-text-uppercase">Growth</div>
    <div class="fp-price-card__price">
      <span class="fp-price-card__amount">$29</span>
      <span class="fp-price-card__period">/mo</span>
    </div>
  </div>
  <ul class="fp-price-card__features">
    <li class="fp-price-card__feature">
      <svg …>…</svg> Unlimited projects
    </li>
  </ul>
  <button class="fp-btn fp-btn--primary fp-btn--block">Choose Growth</button>
</div>
```

The featured card is the one that may carry the accent — as an accent
shadow rather than an accent fill, so the primary button inside it still
reads as the primary button.

---

## 19. Overlays

### Modal

```html
<div class="fp-modal-backdrop" id="demoModal" role="dialog"
     aria-modal="true" aria-labelledby="demoModalTitle">
  <div class="fp-modal">
    <div class="fp-modal__header">
      <h2 class="fp-modal__title" id="demoModalTitle">Delete project?</h2>
      <button class="fp-btn fp-btn--ghost fp-btn--icon fp-btn--sm"
              data-modal-close aria-label="Close">…</button>
    </div>
    <div class="fp-modal__body">…</div>
    <div class="fp-modal__footer">
      <button class="fp-btn fp-btn--secondary" data-modal-close>Cancel</button>
      <button class="fp-btn fp-btn--danger" data-modal-close>Delete</button>
    </div>
  </div>
</div>
```

Open with `data-modal-open="demoModal"`. The JavaScript handles the
scrim, the Escape key, focus placement and body scroll locking.

Sizes: `fp-modal--sm` (400px), default (520px), `--lg` (720px),
`--xl` (960px).

### Drawer

```html
<div class="fp-drawer-backdrop" id="demoDrawer"></div>
<aside class="fp-drawer" id="demoDrawerPanel" role="dialog"
       aria-modal="true" aria-labelledby="drawerTitle">
  <div class="fp-drawer__header">…</div>
  <div class="fp-drawer__body">…</div>
  <div class="fp-drawer__footer">…</div>
</aside>
```

Opens with `data-drawer-open="demoDrawer"`, closes with
`data-drawer-close`. `fp-drawer--left` moves it to the left edge.

Both drawers cast their shadow to the **bottom-right**, like every other
surface in the library. The drawer used to lean its shadow up and to the
left, to match the edge it was anchored to — but a shadow that changes
direction with the element's position is not depth, it is a second
lighting model. The edge-anchored drawer and the free-floating card now
share one light source.

### Toast

```html
<div class="fp-toast-region" id="toastRegion" aria-live="polite"></div>
```

```js
FlatPlanet.toast('Your changes were saved.', 'success', 'Saved');
```

Types: `success`, `danger`, `warning`, `info`. Toasts dismiss after
4 seconds or on click, and the region is an `aria-live` region so
announcements are read out.

---

## 20. Navigation

### Navbar

```html
<nav class="fp-navbar">
  <a class="fp-navbar__brand" href="#">
    <span class="fp-navbar__logo">…</span>
    FlatPlanet
  </a>
  <div class="fp-navbar__links">
    <a class="fp-navbar__link is-active" href="#">Foundations</a>
  </div>
  <div class="fp-navbar__actions">…</div>
</nav>
```

### Island nav

```html
<nav class="fp-island-nav" aria-label="Island navigation">
  <a class="fp-island-nav__item is-active" href="#">Home</a>
  <a class="fp-island-nav__item" href="#">Foundations</a>
</nav>
<div class="fp-island-nav-spacer" aria-hidden="true"></div>
```

A floating bar at the bottom of the viewport. See
[1. The quietest sub element](#1-the-quietest-sub-element) for the full
description of its geometry and its main/sub split.

### Sidebar

```html
<nav class="fp-sidebar">
  <div class="fp-sidebar__group">
    <span class="fp-sidebar__title">Workspace</span>
    <a class="fp-sidebar__item is-active" href="#">Overview</a>
  </div>
</nav>
```

The active item fills with ink and inverts its text.

### Dropdown

```html
<div class="fp-dropdown">
  <button class="fp-btn fp-btn--secondary">Actions …</button>
  <div class="fp-dropdown__menu">
    <span class="fp-dropdown__label">Manage</span>
    <a class="fp-dropdown__item" href="#">Edit project</a>
    <span class="fp-dropdown__divider"></span>
    <a class="fp-dropdown__item fp-dropdown__item--danger" href="#">Delete</a>
  </div>
</div>
```

The menu opens on hover or focus-within. `--right` aligns it to the right
edge of the trigger.

### Menu bar

```html
<div class="fp-menubar">
  <button class="fp-menubar__item is-active">File</button>
  <button class="fp-menubar__item">Edit</button>
</div>
```

---

## 21. Layout shells

### Hero

```html
<div class="fp-hero">
  <span class="fp-kicker">BLP Design System · v1.0</span>
  <h1 class="fp-hero__title">FlatPlanet</h1>
  <p class="fp-hero__subtitle">…</p>
  <div class="fp-hero__actions">…</div>
</div>
```

### Feature panel

```html
<div class="fp-feature">
  <div class="fp-feature__art">…</div>
  <div class="fp-feature__body">…</div>
</div>
```

`fp-feature--reverse` swaps the art to the other side.

### Panel

```html
<div class="fp-panel">…</div>
```

A plain main surface. `fp-panel--flat` removes the shadow.

### Empty state

```html
<div class="fp-empty">
  <span class="fp-empty__icon">…</span>
  <h3 class="fp-empty__title">Nothing here yet</h3>
  <p class="fp-empty__text">When a list has no items, show the empty state.</p>
  <button class="fp-btn fp-btn--primary">Create the first item</button>
</div>
```

### Skeleton

```html
<div class="fp-skeleton fp-skeleton--title"></div>
<div class="fp-skeleton fp-skeleton--text"></div>
<div class="fp-skeleton fp-skeleton--circle"></div>
```

The shimmer sweep is the only gradient in the codebase. It is exempt from
the zero-gradient rule because it is a motion affordance signalling
"loading", not a surface treatment.

---

## 22. Colour swatches

```html
<div class="fp-swatch">
  <div class="fp-swatch__chip" style="background: #007bff"></div>
  <div class="fp-swatch__body">
    <span class="fp-swatch__name">BLP Blue</span>
    <span class="fp-swatch__hex">#007bff</span>
    <span class="fp-swatch__token">--fp-blue</span>
  </div>
</div>
```

The gallery in `index.html` renders these from a JavaScript array that
mirrors the token definitions.

---

## 23. Utilities

| Class | Effect |
|-------|--------|
| `fp-container` | Centred content wrapper, max 1200px |
| `fp-container--wide` / `--narrow` | 1440px / 760px |
| `fp-stack` / `--tight` / `--loose` | Vertical flex stack |
| `fp-row` / `--tight` / `--between` / `--center` / `--end` / `--top` | Horizontal flex row |
| `fp-grid` / `--2` / `--3` / `--4` / `--auto` / `--auto-sm` | Grid layouts |
| `fp-divider` / `--vertical` | Rules |
| `fp-text-xs` … `fp-text-6xl` | Type scale |
| `fp-text-muted` / `--subtle` / `--accent` / `--danger` / `--success` / `--warning` / `--inverse` | Text colour |
| `fp-text-center` / `--nowrap` / `--truncate` | Text utilities |
| `fp-lead` | Section intro paragraph |
| `fp-kicker` | Overline label |
| `fp-sr-only` | Visually hidden, screen-reader only |
| `fp-transition` / `--fast` / `--slow` | The standard transition bundle |
| `fp-dur-fast` / `--default` / `--slow` | Duration only |
| `fp-ease-default` / `--out` / `--in-out` | Easing only |
| `fp-shadow-1` … `fp-shadow-4` | Static hard shadows, `3px` … `14px` on both axes |
| `fp-shadow-none` | No shadow |
| `fp-sub--accent` | The accent as a sub element's border colour |
| `fp-sub--borderless` | A sub element with no border — the quietest tier |
| `fp-island-nav` / `__item` | A floating island navigation bar |
| `fp-island-nav-spacer` | The room a fixed island nav needs |
| `fp-highlight` | Bold text on a rectangular block of accent colour |
| `fp-code` / `fp-code-block` | Inline and block code |
| `fp-kbd` | Keyboard key |
| `fp-divider-label` | A rule with a centred label |
