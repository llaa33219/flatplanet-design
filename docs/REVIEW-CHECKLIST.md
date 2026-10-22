# Review Checklist

A running list of open questions and pending decisions. Updated as the
library evolves.

---

## Open — awaiting feedback

### 1. Sub element border weight

Sub elements use a 4px border, 2px under 40px tall.

**Question:** is 4px right, or would 3px read better against the 6px main
shadow?

### 2. Border colour

Sub borders use `--fp-line-strong` (`#00193d`).

**Question:** would a lighter border read more quietly, letting the shadow
carry more of the depth?

### 3. Press travel

A main element with a 6px shadow descends 4px on hover (6 − 2).

**Question:** is that travel enough to read as a press, or should it be
larger?

---

## Settled

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
