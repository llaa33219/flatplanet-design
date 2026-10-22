# 04 — Changelog

## 1.1.0 — Current

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
- `.fp-highlight` — the accent as a **block of colour behind emphasised
  text**. The words are bold and sit on a plain rectangle of accent
  colour with no radius. Works on `<strong>` and `<mark>` alike.
- `mark` keeps its own neutral yellow identity, but follows the same
  shape rules as `.fp-highlight`: bold, rectangular, no radius. A
  `<mark class="fp-highlight">` takes the accent treatment.

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
- A live component gallery at `index.html`

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
`fp-btn--dark` exists as a high-emphasis alternative.

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
