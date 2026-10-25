# FlatPlanet — Design System Documentation

**Version** 1.0.0 · **Status** Active · **Palette source** `색깔-3.pdf`

FlatPlanet is a UI component library built on the BLP colour palette. It is a
collection of ready-to-use components with a shared visual language, not a
design language in the abstract.

---

## The Five Rules

Every component in this system obeys these five rules. They are the whole
system; everything else is detail.

| # | Rule | Why it exists |
|---|------|---------------|
| 1 | **36px radius ceiling** | One corner radius everywhere. Smaller radii only when a short height makes 36px unreadable. |
| 2 | **Zero gradients** | Depth comes from flat fills plus solid offset shadows. Never from a colour ramp. |
| 3 | **Hard shadows** | Every shadow is a solid block of ink with zero blur radius, offset equally and positively on both axes — it always falls to the bottom-right. |
| 4 | **Three speeds** | `0.1s` fast, `0.2s` default, `0.3s` slow. Nothing else. |
| 5 | **BLP colours only** | Every colour comes from the palette in `색깔-3.pdf`. |

---

## Documentation Map

| Document | Contents |
|----------|----------|
| [01-foundations.md](./01-foundations.md) | Colour tokens, radius scale, elevation model, motion, typography, spacing |
| [02-components.md](./02-components.md) | Every component: markup, modifiers, behaviour notes |
| [03-usage.md](./03-usage.md) | Composition rules, the accent discipline, accessibility, dark mode, theming |
| [04-changelog.md](./04-changelog.md) | Version history and the reasoning behind each change |

---

## Quick Start

```html
<link rel="stylesheet" href="assets/css/tokens.css">
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/elevation.css">
<link rel="stylesheet" href="assets/css/components.css">
<link rel="stylesheet" href="assets/css/components-2.css">
```

The stylesheet order matters. `tokens.css` defines the variables,
`base.css` the reset and primitives, `elevation.css` the shadow system, and
the two component files the components themselves.

Open `index.html` for the live component gallery. The gallery is split
by kind: `foundations/` holds the rules, elevation and palette, and
`components/<kind>/` holds one page per component family (actions,
forms, surfaces, navigation, feedback, data, overlays).

---

## Project Layout

```
flatplanet-design/
├── index.html                 Gallery landing — the hub card index
├── foundations/
│   └── index.html             Rules, elevation, the BLP palette
├── components/
│   ├── index.html             The shelf — every family and sub-page
│   ├── actions/               index + sub-elements/ + fab/
│   ├── forms/                 index + steppers/ + codes/
│   ├── surfaces/              index + footer/ + apps/ + content/
│   ├── navigation/            index + bars/ + wayfinding/ + structure/
│   ├── feedback/              index + banners/
│   ├── data/                  index + rows/ + loading/ + metrics/
│   └── overlays/              index + sheets/ + anchored/
├── assets/
│   ├── css/
│   │   ├── tokens.css         Colour, radius, elevation and motion tokens
│   │   ├── base.css           Reset, typography, layout primitives, utilities
│   │   ├── elevation.css      The hard-shadow system and press behaviour
│   │   ├── components.css     Buttons, forms, cards, data display
│   │   └── components-2.css   Overlays, navigation, feedback, layout shells
│   └── js/
│       └── flatplanet.js      Theme toggle, tabs, modals, drawer, toasts
├── docs/                      This documentation
└── 색깔-3.pdf                  The BLP colour palette (source of truth)
```
