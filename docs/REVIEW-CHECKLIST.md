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

### Directional variants are kept

`.fp-elev--down`, `--down-right`, `--right`, `--left` and `--up` all
exist, and each one's shadow direction agrees with its hover movement.

### The omni band is kept, but it is not the default

`.fp-elev--omni` (`0 0 0 6px`) stays available for surfaces that must
read as detached from the page. The offset shadow is the default.

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
