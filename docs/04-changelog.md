# 04 — Changelog

## 1.2.0 — Current

Control variants, a rectangular range thumb, the borderless sub element,
a floating island nav and a dark theme that is a true inversion.

### Added

**Accent variants for the form controls**
- `--fp-accent-fill` (`#005bdd`) is a new token: the accent as a
  *background*. `--fp-accent` stays the brand blue (`#007bff`) and is
  what the accent IS — a focus ring, an accent border, an accent line.
  The split is a contrast decision: white on `#007bff` is 3.95:1, below
  the 4.5:1 that body text needs, so anything that carries white text
  on an accent background takes the deep step instead (5.88:1).
- `.fp-check--accent` — a checked checkbox or radio fills with the accent
  instead of the ink. The tick mark stays white.
- `.fp-switch--accent` — an ON switch fills with the accent instead of
  the ink.
- The UNCHECKED / OFF state is untouched in both variants: white surface,
  ink border, no accent anywhere. A control that is off does not shout.

**The borderless sub element — `.fp-sub--borderless`**
- The quietest tier of the element model. A sub element with no border,
  which is still a sub element in every other respect: flat at rest, and
  on hover it lifts and its shadow appears.
- Written as a custom property (`--fp-sub-border-width: 0`) rather than
  as `border: none`, because a component such as `.fp-navbar__link`
  reserves its border space with `border: 4px solid transparent`. Setting
  the *width* to zero keeps the box the same size, so no neighbour ever
  moves — a `border: none` would have caused a layout shift.

**The island nav**
- `.fp-island-nav` — a navigation bar that floats at the bottom of the
  viewport as a detached, 36px-radius pill. The container is a MAIN
  element (no border, a hard shadow). Being pinned to the viewport it
  never travels on hover: the shadow stays exactly as it is.
- The items are the system's ordinary **`.fp-btn--sub` buttons**,
  re-sized to the row — the earlier one-off item class (transparent
  resting border, ink-filled active state) was removed, and the current
  destination now wears the accent border, the same emphasis every sub
  element uses.
- `.fp-island-nav-spacer` — reserves the room the fixed island occupies,
  so the last content is never trapped underneath it.

**The range progress fill**
- The filled portion of the range track is drawn by a CSS gradient on the
  track itself, driven by the `--fp-range-progress` custom property.
- Without JavaScript the gradient falls back to `0%` and the bar is
  simply empty: the control still works, it just does not claim to know
  its own value.

### Changed

**The range thumb is now a rectangle that sits inside the track**
- It was a 28px disc on a 14px rail, so it overflowed the track by 7px
  above and 7px below — a handle hanging over both edges of the rail
  rather than a handle in it.
- It is now a 28×10px rectangle with a 12px radius, inside an 18px
  track, with 4px of clearance above and below. The geometry was
  measured in both Chromium and Firefox: the thumb's centre lands exactly
  on the track's centre line (delta 0) and never touches either edge.
- `margin-top: 2px` is the vertical correction for Chromium, where a
  native thumb is positioned by its top edge against the track's INNER
  edge — so the correction is `(18 − 10) / 2 − 2` (the track's 2px border
  is already accounted for), not `(18 − 10) / 2`. Firefox centres a
  `::-moz-range-thumb` by itself and ignores the property, so the handle
  lands identically in both engines.
- `box-sizing: border-box` is declared on the pseudo-elements, because
  browser pseudo-elements are not matched by the global `*` reset.
- The hover behaviour is unchanged: the thumb lifts 2px and its hard
  shadow appears.

**The sub element's border is no longer black**
- It was `--fp-line-strong` (`--fp-ink`, `#00193d`) — so close to black
  that every sub element wore a hard black outline and shouted, leaving
  the shadow with nothing to do.
- It is now `--fp-line-sub` (`#3e4d5f`, BLP SUB DARK): unmistakably a
  border at roughly 8:1 against white, but with tone in it.
- `--fp-line-strong` keeps its name and now points at `--fp-line-sub`,
  so every component that already read it picked the softer border up
  for free. The `--fp-sub-border-color` mechanism is untouched.

**The dark theme is now a true inversion**
- It used to be hand-picked colours (`#1e2b3d` surfaces, `#0b1524`
  canvas), which is not an inversion of anything.
- Now every colour is the light theme's colour inverted: the canvas
  becomes the palette's darkest (`#000309`), the main surface stays the
  palette's lightest (`#fefeff`), and text, fills, tracks, tints and
  code blocks all swap with it.
- **The shadow is the one exception.** It stays dark (`#000309`), because
  a light shadow on a dark surface reads as a glow rather than as depth.
- The accent and the status colours do not invert — they are signals,
  not surfaces.

**Text follows its context**
- The inverted theme has two polarities on the page at once, so text on
  the canvas and text on a card cannot share a colour.
- `--fp-text` now follows its **context**: it is the page value by
  default, and every surface re-points it at the surface value. A
  component never has to know which theme it is in.

### Fixed

- The footer in the dark theme was unreadable: its text token did not
  invert with the surface it sat on. The inverse-surface text tokens
  now invert with the inverse surface.
- The code block, which was dark in the light theme, is now light in the
  inverted theme.
- The select chevron, the switch thumb and the skeleton pulse all
  follow the polarity of the surface they sit on.

---

## 1.1.0

The elevation system, finalised. The shadow geometry, the hover contract
and the main/sub distinction are now the way the library is built.

### The shadow contract

**Every shadow in the library is `(positive px) (positive px) 0 <ink>`.**
Both offsets are positive, both are equal, the blur is zero and the
spread is zero. A shadow always falls to the bottom-right.

**Removed**
- `.fp-elev--omni` and `.fp-shadow-omni-1` … `--omni-4`. A shadow with a
  positive spread paints ink on all four sides; that is a border, not a
  shadow, and the library already has a border primitive. The classes are
  gone, not renamed.
- `.fp-elev--up` and `.fp-elev--left`. Both produced negative offsets,
  which is illegal.
- `.fp-elev--right` and `.fp-elev--down-right`. With the up-left
  diagonals gone, both would have been identical to `.fp-elev--down`.
  A variant that produces no distinct shadow does not exist.
- `.fp-elev--down-left`. Never legal, and never shipped.
- `.fp-elev--down`. It produced exactly the default shadow, so it was a
  second name for one thing. A hard shadow has one direction and one
  size scale; there is no modifier for either.

**Changed**
- `.fp-drawer` cast an up-left shadow (`-6px -6px 0`) because it is
  anchored to the right edge. It is now `6px 6px 0`, like everything
  else. A shadow that changes direction with the element's position is
  a second lighting model, not depth.
- `.fp-accordion__item[open]` carried a 4px shadow while its hover
  shadow was 3px — an open item that shrank its shadow as it rose, which
  is the forbidden combination. The open shadow is now the same size as
  the hover shadow.

### Changed

**Elevation**
- Hard shadows are offset **equally and positively** on both axes
  (`6px 6px 0`), not downwards only. The light source is in the
  top-left corner, so every shadow falls to the bottom-right like ink on
  paper.
- A **sub element has no resting shadow**. Its real inline border is the
  outline; the shadow appears on hover, as it lifts.
- A **main element never rises**. It only presses down, and its shadow
  contracts as it goes. The forbidden combination — moving up while the
  shadow shrinks — appears nowhere in the library.

**Accent**
- `.fp-sub--accent` — the accent as a **sub element's border**. This is
  the sanctioned way to emphasise a sub element: it recolours the
  border that is already there, without making the element bigger or
  moving it. The colour travels through the new
  `--fp-sub-border-color` custom property, so the modifier works on
  every sub element without out-specifying the component's own border
  rule.
- `.fp-highlight` — the accent on **emphasised words themselves**: bold
  text in the accent text colour, with no block of colour behind them.
  Works on `<strong>` and any inline element.
- `mark` keeps its own neutral yellow identity — bold, rectangular, no
  radius — and stays the only highlight that paints the paper.

**Components**
- `.fp-icon-tile` and `.fp-empty` are main elements: their borders are
  gone and their shadows are now hard and square.
- `.fp-btn--ghost` became a sub element — a real inline border, flat at
  rest, and it lifts with the shadow appearing.
- `.fp-card--outlined`, `.fp-alert`, `.fp-callout` and `.fp-toast` are
  bordered, so they are sub elements: flat at rest, lifting on hover.
- `.fp-navbar__link` and `.fp-sidebar__item` lost their resting shadow.
- The switch thumb, the range thumbs and the timeline dot became
  sub elements: flat at rest, shadow on hover.
- `.fp-switch__track`, `.fp-check__box`, `.fp-input`, `.fp-select`,
  `.fp-textarea` and `.fp-list__item` all lost their resting shadow.
- Every shadow that faked a border became a real `border:` declaration.

**Tooling**
- `tools/verify-elevation.py` — a rule verifier for the elevation
  contract. It parses the CSS and asserts that main elements have no
  border and a hard square shadow, that sub elements have a real border
  and no resting shadow, that **every shadow has positive, equal offsets
  with zero blur and zero spread**, and that the sign of the hover movement agrees
  with the direction of the shadow change.

---

## 1.0.0

The first complete release of FlatPlanet as a component library.

### Added

**Foundations**
- 60 raw colour tokens covering the full BLP palette from `색깔-3.pdf`
- Semantic token layer: surfaces, ink, text, lines, accent, status, tints
- Radius scale with a hard 36px ceiling
- Four elevation tiers plus a sub-element tier
- Motion tokens: 0.1s fast, 0.2s default, 0.3s slow, with three easing curves
- Type scale from 11px to 72px
- 4px-base spacing scale
- Three container widths and a three-step responsive grid

**Elevation**
- Omnidirectional hard shadows built on zero-blur positive-spread, so the
  band follows `border-radius` exactly with no corner notches
- Directional variants: down, up, left, right, down-right
- The press: the shadow collapses to 2px and the element descends by the
  difference
- The lift: sub elements rise and gain a shadow

*(Reworked in 1.1.0: the offset shadow became the default, sub elements
lost their resting shadow, and the hover contract was tightened.)*

**Components**
- Buttons: 8 variants, 4 sizes, block/pill/square/icon modifiers, groups
- Forms: field wrapper, input, select, textarea, input group, search,
  checkbox, radio, card checkbox, switch, range
- Display: badge (11 variants), tag, chip, avatar, avatar group, icon tile
- Surfaces: card (media/header/body/footer), panel, feature panel, hero
- Navigation: navbar, sidebar, dropdown, menu bar, tabs, segmented control,
  breadcrumb, pagination
- Data: table, list, progress, meter, circular ring, timeline, stat tile,
  key-value list, description list, code block
- Feedback: alert (5 severities), callout, tooltip, toast
- Overlays: modal (4 sizes), drawer, banner, empty state, skeleton
- Content: pricing card, swatch, spec card, disclosure, divider label, kbd
- Utilities: layout, typography, colour, transition, spacing, visibility

**Behaviour**
- Theme toggle with `localStorage` persistence
- Tabs, segmented controls and chips
- Modal and drawer with scrim, Escape handling, focus placement and scroll
  locking
- Toast API with four types and an `aria-live` region
- Scroll spy for documentation tables of contents
- A live palette gallery rendered from the token definitions

**Documentation**
- Four documents: foundations, components, usage, changelog
- A live component gallery at `index.html`, split into `foundations/`
  and `components/<kind>/` pages by component family

---

## Design decisions worth recording

**Why the four-sided band was removed.** The band was technically
correct: a single zero-blur shadow with positive spread is solid and
follows the element's `border-radius` exactly, so the corners stay clean
where four stacked offset shadows would have left notches. But a band on
all four sides is an *outline*, not depth, and the library already has a
primitive for outlines — the real inline `border:` that every sub element
carries. Two primitives for one job, and a second lighting model that
lit from everywhere instead of from the top-left corner. The band is
gone; an element that needs an outline on every side now uses a border.

**Why sub elements have no resting shadow.** The border already carries
the outline, so a shadow as well would double it. More importantly, a
shadow is a *response*: it appears when the pointer arrives and the
element lifts. A shadow that is already there has nothing left to
announce.

**Why the shadow offsets are equal on X and Y.** A shadow offset
downwards only reads as a drop shadow. Offsetting equally in both
directions puts the light source in the top-left corner, and the shadow
falls like ink on paper — the same gesture the rest of the system is
built from.

**Why main elements have no border.** A main element's shadow is a solid
band of ink around its entire silhouette. Adding a border on top of that
band doubles the outline and makes the element read as heavier than its
shadow alone. The border is reserved for sub elements, which have no
full-strength shadow of their own.

**Why 36px is a ceiling and not just a default.** A single radius value
gives the system a recognisable silhouette. Allowing 48px or 64px
corners would make the library look like a different product. The
concession for short elements is handled by the size scale, where a
radius step always accompanies a height step — never in isolation.

**Why the accent is budgeted to one per view.** A colour that appears on
everything marks nothing. Reserving `#007bff` for the single most
important action in a view is what gives it meaning, and it is why
`fp-btn--sub--accent` exists as the emphasised sub
alternative.

---

## 0.9.0 — Internal prototype

An earlier internal build. Not released.

- Flat single-file CSS with a smaller token set
- Downward-only shadows
- Accent blue used as the default surface for primary buttons, tabs, active
  states, chips and avatars
- Borders on all components, including main elements
- Shadow ink `#000309`

Reworked in 1.0.0 along the lines described above: white became the main
surface, the accent was demoted, borders were reserved for sub elements,
the shadow ink moved to `#00193d`, and shadows became omnidirectional.

---

## Roadmap

- **Data table** — sorting, column resize, selection, sticky headers
- **Combobox** — searchable select with keyboard navigation
- **Date picker** — built on the native date input
- **Carousel** — using the existing press and lift behaviours
- **Tree view** — nested list items with the sub-element treatment
- **Command palette** — a modal with a focus-trapped search field
- **Skeleton variants** for the table, list and card components
- **Motion documentation** — a page demonstrating the three speeds
  side by side
- **Component playground** — live prop editing for every component
