# 04 — Changelog

## 1.0.0 — Current

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

**Why the omni shadow is built with spread, not offsets.** Stacking four
offset shadows to fake a four-sided hard shadow leaves square notches at
the corners. A single zero-blur shadow with positive spread is solid and
follows the element's `border-radius` exactly, producing a band of
uniform width on all four sides. This is the primitive the whole system
rests on.

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
