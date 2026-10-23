# Review Checklist

A running list of open questions and pending decisions. Updated as the
library evolves.

---

## Open — awaiting feedback

### 1. Sub element border weight

Sub elements use a 4px border, 2px under 40px tall.

**Question:** is 4px right, or would 3px read better against the 6px main
shadow?

### 2. Press travel

A main element with a 6px shadow descends 4px on hover (6 − 2).

**Question:** is that travel enough to read as a press, or should it be
larger?

### 3. The island nav's resting shadow

The island nav carries a 6px hard shadow, like a card.

**Question:** a floating bar over the page might want to be more
separated from the content than a card in a grid is. Would a 9px shadow
read better, or does 6px already lift it off the page?

---

## Settled

### The sub element's border colour

**Settled: `--fp-line-sub`, BLP SUB DARK (`#3e4d5f`).**

The border used to be the ink (`#00193d`), which is so close to black
that every sub element wore a hard black outline and shouted for
attention. The shadow was supposed to carry the depth; the border was
taking it.

Of the two candidates, `#3e4d5f` and `#94989e`, the darker one wins:

- `#3e4d5f` against white is roughly **8:1** — unmistakably a border, so
  a sub element keeps its outline and never dissolves into the card it
  sits in.
- `#94989e` against white is roughly **2.9:1** — at that ratio a 4px line
  stops being an outline and starts being a smudge, which would leave
  sub elements defined by nothing at all.

`--fp-line-strong` keeps its name and points at `--fp-line-sub`, so
every component that already read it picked the softer border up for
free. The `--fp-sub-border-color` mechanism is unchanged.

### The borderless sub element

**Settled: `.fp-sub--borderless`, a third tier of the element model.**

A sub element with no border, which is still a sub element in every
other respect — flat at rest, and on hover it lifts and its shadow
appears.

It is written as a custom property (`--fp-sub-border-width: 0`) rather
than as `border: none`, for a specific reason: components such as
`.fp-navbar__link` declare `border: 4px solid transparent` so that the
border space is *reserved* and nothing shifts when the link becomes
active. Removing the border outright would release that space and cause
a layout shift. Setting the width to zero keeps the box the same size.

Measured and confirmed: a bordered nav link and a borderless one have
identical widths, and the anchor beside them does not move when either
changes state.

### The range thumb is a rectangle inside the track

**Settled: a 28×10px rectangle with a 12px radius, inside an 18px
track, centred.**

The thumb used to be a 28px disc on a 14px rail — it overflowed the
track by 7px above and 7px below. A handle that hangs over both edges
reads as an object sitting *on* the slider rather than a handle *in* it.

The geometry was measured in Chromium and Firefox rather than reasoned
about:

| | Value |
|---|---|
| Track (rendered) | y 3 → 20, 18px |
| Thumb (rendered) | y 7 → 16, 10px |
| Thumb centre vs track centre | delta 0 |
| Clearance above and below | 4px each |
| Thumb aspect | 26px wide, 10px tall |

`margin-top: 2px` is Chromium's correction — `(18 − 10) / 2 − 2`, the
remainder after the track's own 2px border. Firefox centres a
`::-moz-range-thumb` itself and ignores the property, so the handle lands
identically in both engines.

### The dark theme is a true inversion

**Settled: every colour is inverted except the shadow.**

The canvas becomes the palette's darkest (`#000309`), the main surface
stays the palette's lightest (`#fefeff`), and text, fills, tracks, tints
and code blocks all swap with them.

The **shadow** does not invert. It stays dark (`#000309`), because a
light shadow on a dark surface reads as a *glow* rather than as depth,
and the hard-shadow character of the system would be lost.

The **accent** and the **status colours** do not invert either — they
are signals, not surfaces.

Text follows its **context**: `--fp-text` is the page value by default
and every surface re-points it at the surface value, so a component
never has to know which theme it is in.

### Shadow offsets are equal on X and Y

A hard shadow is `6px 6px 0`, never `0 6px 0`. The light source sits in
the top-left corner, so every shadow falls to the bottom-right. A
directional variant is a diagonal, not an axis.

### Directional variants are gone

A hard shadow has exactly one legal direction — down-right. `--up` and
`--left` leaned the wrong way; `--right` and `--down-right` were
indistinguishable from `--down`. Only `--down` survives, as the explicit
spelling of the one direction.

### The omni band is gone

A band on all four sides is a border, not a shadow. `.fp-elev--omni` and
`.fp-shadow-omni-*` are removed; an element that needs an outline on
every side uses a real `border:`.

### Radius ceiling is 36px

Smaller radii are permitted only where a short height forces it.

### Accent discipline

One accent-filled element per view. `#007bff` marks the single most
important action.

`--fp-accent` is the brand blue and is used for lines: focus rings,
accent borders, accent-coloured rules. `--fp-accent-fill` (`#005bdd`) is
the accent used as a background, because white on `#007bff` is 3.95:1
and white on `#005bdd` is 5.88:1.

### BLP White is the main colour

`#fefeff` is the default surface for most components, not an accent.

### Shadow ink is `#00193d`

`#000309` read as a hole rather than as depth.

---

## Notes

### The inline border matters

A sub element's border is a real `border:` declaration, not a
`box-shadow` ring. A ring sits outside the layout box, so it does not
align with neighbouring borders, does not round with the element's own
radius, and makes a sub element look like a main element.

### The forbidden combination

An element that rises must never lose its shadow. Rising is a sub
element's cue; the shadow appearing is what confirms it. The reverse —
rising while the shadow shrinks — describes an element floating away and
getting smaller, which is never what a hover means.

### Mains press down, subs lift up

A main element's shadow is a footprint on the surface below it. When the
pointer arrives, the element sinks toward that surface and the footprint
contracts. A sub element's shadow is its own; it has none at rest, and
when the pointer arrives it rises and casts one.

---

## 2026-10-22 — Rule clarifications

### The shadow contract is now absolute

Every shadow is `(positive px) (positive px) 0 <ink>`. The shadow always
falls to the bottom-right. There is no upward shadow, no leftward shadow,
and no band on all four sides — a band is a border, not a shadow.

The omni variant and the up/left directional variants are gone. A hard
shadow has exactly one direction.

### Accent has two sanctioned uses

1. **On a sub element's border** — to draw the eye to that one sub
   element. This is how a sub element gets emphasised, not by making it
   bigger or moving it.
2. **On text** — the emphasised words are bold, on a rectangular block of
   accent colour behind them. A rectangle, not a pill.

### The accent border is one generic modifier

`.fp-sub--accent` is the single mechanism, usable on any sub element.
Sixty components cannot afford sixty accent modifiers. The colour
travels through the `--fp-sub-border-color` custom property, so the
modifier sets a property rather than fighting the component's own
`border:` declaration for specificity.

### `mark` stays neutral, but matches the shape

`mark` keeps its yellow identity — an editorial highlight should not
spend the accent — while `fp-highlight` is the accent-emphasis
primitive. The two are consistent in shape: bold, rectangular, no
radius. A `<mark class="fp-highlight">` takes the accent treatment.
