#!/usr/bin/env python3
"""
FlatPlanet — elevation rule verifier.

Parses the CSS and asserts the elevation contract:

  MAIN  = no border, hard shadow  (offset X == offset Y, blur 0)
  SUB   = inline border, NO default shadow
  hover MAIN = Y increases (element moves down) AND shadow shrinks
  hover SUB  = Y decreases (element moves up)   AND shadow APPEARS
  FORBIDDEN: the element moves up while its shadow shrinks or disappears

Exit code 0 = all rules hold.
"""
import re, sys, glob, os

CSS = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "assets", "css", "*.css")))

# --------------------------------------------------------------------------
# 1. PARSING
# --------------------------------------------------------------------------

def strip_comments(src):
    return re.sub(r"/\*.*?\*/", "", src, flags=re.S)


def split_top_level(value, sep=","):
    """Split on `sep` that is not inside parentheses."""
    out, depth, cur = [], 0, []
    for ch in value:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


class Rule:
    __slots__ = ("media", "selector", "body", "index")

    def __init__(self, media, selector, body, index):
        self.media = media
        self.selector = selector
        self.body = body
        self.index = index


def parse_rules(src, media=None, start_index=0):
    """Parse CSS into Rules. @media blocks are flattened into their rules
    (the media condition is kept on the rule); other at-rules are skipped."""
    out = []
    i, n = 0, len(src)
    while i < n:
        j = src.find("{", i)
        if j == -1:
            break
        sel = src[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if src[k] == "{":
                depth += 1
            elif src[k] == "}":
                depth -= 1
            k += 1
        inner = src[j + 1:k - 1]
        if sel.startswith("@media"):
            out.extend(parse_rules(inner, media=sel, start_index=len(out)))
        elif sel.startswith("@"):
            pass  # @keyframes, @supports, @font-face ... not component rules
        else:
            out.append(Rule(media, " ".join(sel.split()), inner, start_index + len(out)))
        i = k
    return out


def expand(rules):
    """Split grouped selectors so each individual selector is checked."""
    out = []
    for r in rules:
        for sel in split_top_level(r.selector):
            sel = " ".join(sel.split())
            if sel:
                out.append(Rule(r.media, sel, r.body, r.index))
    return out


# --------------------------------------------------------------------------
# 2. VALUE RESOLUTION
# --------------------------------------------------------------------------

def collect_vars(src):
    """Every custom property declaration in the file (name -> raw value)."""
    out = {}
    for m in re.finditer(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;{}]+);", src):
        out.setdefault(m.group(1), m.group(2).strip())
    return out


def resolve(value, var_map, depth=0):
    """Resolve var() references in a value."""
    if value is None or depth > 8:
        return value
    def repl(m):
        name = m.group(1).strip()
        if name in var_map:
            return resolve(var_map[name], var_map, depth + 1)
        return m.group(0)
    return re.sub(r"var\(\s*([a-zA-Z0-9_-]+)\s*\)", repl, value)


def resolve_vars(value, var_map):
    """Resolve var() references, leaving unresolvable ones untouched."""
    if value is None:
        return value
    for _ in range(8):
        new = resolve(value, var_map)
        if new == value:
            break
        value = new
    return value


def local_vars(body):
    """Custom properties declared inside a single rule body."""
    out = {}
    for m in re.finditer(r"(--[a-zA-Z0-9_-]+)\s*:\s*([^;{}]+);", body):
        out.setdefault(m.group(1), m.group(2).strip())
    return out


# --------------------------------------------------------------------------
# 3. SHADOW PARSING
# --------------------------------------------------------------------------

def eval_length(text, var_map):
    """Evaluate a CSS length expression to a float, or None."""
    if text is None:
        return None
    t = text.strip()
    if t.lower() in ("none", "inherit", "initial", "unset"):
        return None
    t = resolve_vars(t, var_map)
    if t.startswith("calc("):
        t = t[5:-1] if t.endswith(")") else t[5:]
    t = t.replace("px", "").strip()
    if not t or not re.match(r"^[-+*/(). 0-9]+$", t):
        return None
    try:
        return float(eval(t, {"__builtins__": {}}, {}))
    except Exception:
        return None


def parse_shadow(value, var_map):
    """Return a list of (dx, dy, blur, spread, colour) layers.

    Lengths may be written with or without a unit, may be calc() expressions
    and may be var() references — all of them are resolved here.
    """
    if value is None:
        return []
    value = value.strip()
    if value.lower() in ("none", "inherit", "initial", "unset"):
        return []
    layers = []
    for layer in split_top_level(value):
        layer = re.sub(r"\binset\b", "", layer).strip()
        if not layer:
            continue
        lengths, colour_parts = [], []
        tokens, depth, cur = [], 0, []
        for ch in layer:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if ch.isspace() and depth == 0:
                if cur:
                    tokens.append("".join(cur))
                    cur = []
            else:
                cur.append(ch)
        if cur:
            tokens.append("".join(cur))

        for tok in tokens:
            resolved = resolve_vars(tok, var_map)
            if re.match(r"^var\(", tok) or re.match(r"^var\(", resolved):
                # a var() may hold a length or a colour — decide by its value
                num = eval_length(resolved, var_map)
                if num is None:
                    colour_parts.append(resolved)
                else:
                    lengths.append(num)
                continue
            num = eval_length(tok, var_map)
            if num is not None:
                lengths.append(num)
            else:
                colour_parts.append(tok)

        while len(lengths) < 4:
            lengths.append(0.0)
        colour = " ".join(colour_parts).strip()
        layers.append((lengths[0], lengths[1], lengths[2], lengths[3], colour))
    return layers


def shadow_size(layer):
    """Thickness of the band a hard shadow produces."""
    if layer is None:
        return 0.0
    dx, dy, blur, spread, _ = layer
    return max(abs(dx), abs(dy), abs(spread))


# --------------------------------------------------------------------------
# 4. SELECTOR HELPERS
# --------------------------------------------------------------------------

STATE_PSEUDO = (":hover", ":focus-visible", ":focus-within", ":focus",
                ":active", ":checked", ":disabled", ":enabled", ":target")
STATE_ATTR_RE = re.compile(r"\[(?:open|selected|pressed|checked|disabled|expanded|active)[^\]]*\]")
STATE_CLASS_RE = re.compile(r"\.is-[a-z0-9-]+")


def is_state(selector):
    """A rule that describes a temporary state rather than the resting one."""
    for p in STATE_PSEUDO:
        if p in selector:
            return True
    if STATE_ATTR_RE.search(selector):
        return True
    if STATE_CLASS_RE.search(selector):
        return True
    return False


def base_of(selector):
    """The subject of a selector: its last compound, without state parts."""
    parts = re.split(r"\s*[>+~]\s*|\s+", selector)
    subject = parts[-1] if parts else selector
    subject = re.sub(r":(hover|focus-visible|focus-within|focus|active|checked|disabled|enabled|target)\b", "", subject)
    subject = STATE_ATTR_RE.sub("", subject)
    subject = STATE_CLASS_RE.sub("", subject)
    subject = re.sub(r":not\([^)]*\)", "", subject)
    return subject.strip()


def subject_of(selector):
    """The subject of a selector: its last compound, without state parts."""
    parts = re.split(r"\s*[>+~]\s*|\s+", selector)
    subject = parts[-1] if parts else selector
    subject = re.sub(r":(hover|focus-visible|focus-within|focus|active|checked|disabled|enabled|target)\b", "", subject)
    subject = STATE_ATTR_RE.sub("", subject)
    subject = STATE_CLASS_RE.sub("", subject)
    subject = re.sub(r":not\([^)]*\)", "", subject)
    return subject.strip()


def translate_y(transform, var_map):
    """The Y offset of a translateY() in a transform list, or None.

    The transform may be a list of functions; only the translateY() entries
    are of interest, and the last one wins.
    """
    dy = None
    for m in re.finditer(r"translateY\(", transform):
        # take the balanced parenthesised expression
        i = m.end()
        depth, j = 1, i
        while j < len(transform) and depth:
            if transform[j] == "(":
                depth += 1
            elif transform[j] == ")":
                depth -= 1
            j += 1
        inner = transform[i:j - 1].strip()
        if inner.startswith("calc(") and inner.endswith(")"):
            inner = inner[5:-1].strip()
        inner = resolve_vars(inner, var_map).replace("px", "").strip()
        if not inner or not re.match(r"^[-+*/(). 0-9]+$", inner):
            continue
        try:
            dy = float(eval(inner, {"__builtins__": {}}, {}))
        except Exception:
            continue
    return dy


def rule_props(body):
    """Last declaration of every property in a rule body."""
    out = {}
    for m in re.finditer(r"(?:^|;)\s*([a-zA-Z-]+)\s*:\s*([^;]+)", body):
        out[m.group(1)] = m.group(2).strip()
    return out


def decl(body, prop):
    return rule_props(body).get(prop)


def has_prop(body, prop):
    return re.search(r"(?:^|;)\s*" + re.escape(prop) + r"\s*:", body) is not None


# --------------------------------------------------------------------------
# 5. THE ELEMENT ROSTER
# --------------------------------------------------------------------------

MAIN_MARKERS = [
    ".fp-card", ".fp-panel", ".fp-hero", ".fp-feature", ".fp-stat",
    ".fp-modal", ".fp-price-card", ".fp-table-wrap", ".fp-btn",
    ".fp-dropdown__menu", ".fp-sidebar", ".fp-empty", ".fp-code-block",
    ".fp-icon-tile", ".fp-swatch", ".fp-spec", ".fp-elev",
    ".fp-fab", ".fp-phone", ".fp-sheet", ".fp-island-nav", ".fp-m-tabbar",
]
# PINNED mains: fixed/docked to the viewport or a frame edge, so there is
# nothing under them to press INTO. Their shadow must NOT change on
# hover — they never travel.
MAIN_PINNED = [
    ".fp-island-nav", ".fp-m-tabbar",
]

SUB_MARKERS = [
    ".fp-input", ".fp-select", ".fp-textarea", ".fp-list__item", ".fp-tag",
    ".fp-chip", ".fp-avatar", ".fp-accordion__item", ".fp-pagination__item",
    ".fp-badge", ".fp-timeline__dot",
    ".fp-check--card", ".fp-input-group__addon", ".fp-sub",
]
# The BORDERLESS sub tier: still sub behaviour (flat at rest, lifts on
# hover), but borderless by design — the same tier `.fp-sub--borderless`
# opts into. These are rostered separately so the border rule skips them
# while the hover rule below still applies.
SUB_BORDERLESS = [
]
# FILLED controls: a control's face is a FILLED shape, not a quiet sub
# element — the fill is the outline, so it carries no border and no
# resting shadow; hover still lifts it and makes the shadow appear.
SUB_FILLED = [
    ".fp-check__box", ".fp-switch__track", ".fp-range", ".fp-progress",
]


def main():
    files = []
    global_map = {}
    for path in CSS:
        name = os.path.basename(path)
        src = strip_comments(open(path, encoding="utf-8").read())
        files.append((name, src))
        for k, v in collect_vars(src).items():
            global_map.setdefault(k, v)

    # resolve the global chains once
    for k in list(global_map):
        global_map[k] = resolve_vars(global_map[k], global_map)

    failures = []
    notes = []

    def fail(msg):
        failures.append(msg)

    all_rules = []
    for name, src in files:
        for r in expand(parse_rules(src)):
            all_rules.append((name, r))

    # Group the rules by the element they describe, keeping source order so
    # that the cascade can be reproduced.
    by_base = {}
    for name, r in all_rules:
        by_base.setdefault(base_of(r.selector), []).append((name, r))

    # Custom properties declared on the element itself, so --fp-elev-h and
    # friends resolve the way the browser resolves them for that element.
    scope_vars = {}
    for base, group in by_base.items():
        merged = {}
        for _, r in group:
            merged.update(local_vars(r.body))
        scope_vars[base] = merged

    def ctx_for(base):
        merged = dict(global_map)
        merged.update(scope_vars.get(base, {}))
        return merged

    def specificity(selector):
        """(ids, classes, elements) — the CSS specificity of a selector."""
        s = re.sub(r":not\(([^)]*)\)", r"\1", selector)
        ids = len(re.findall(r"#[A-Za-z0-9_-]+", s))
        classes = len(re.findall(r"\.[A-Za-z0-9_-]+", s)) + len(re.findall(r":[A-Za-z-]+", s))
        elements = len(re.findall(r"(?:^|[\s>+~])[a-zA-Z][A-Za-z0-9-]*", s))
        return (ids, classes, elements)

    def effective(base, prop, state_rule=None):
        """The value a browser would use for the element's resting state:
        the winning declaration among the element's own rules.

        A rule whose selector also matches another element (a descendant or
        a compound selector) only applies to that element when it wins the
        cascade, so the rules that belong to the element alone are
        considered first.
        """
        candidates = [(r, specificity(r.selector)) for _, r in by_base.get(base, [])
                      if not is_state(r.selector)]
        # A rule for the element alone outranks a rule that merely also
        # matches it (a descendant or a compound selector). Among equals the
        # later rule wins, as in the cascade.
        own = [(r, s) for r, s in candidates if r.selector == base]
        contextual = [(r, s) for r, s in candidates if r.selector != base]

        def winner(rules):
            if not rules:
                return None
            best, best_spec = None, None
            for r, spec in rules:
                if best_spec is None or spec > best_spec:
                    best, best_spec = r, spec
            return best

        value = None
        for candidate in (winner(own), winner(contextual)):
            if candidate is None:
                continue
            v = decl(candidate.body, prop)
            if v is not None:
                value = v
        if state_rule is not None:
            v = decl(state_rule.body, prop)
            if v is not None:
                value = v
        return value

    def shadow_of_value(value, base):
        if value is None:
            return None
        layers = parse_shadow(value, ctx_for(base))
        return layers[0] if layers else None

    def shadow_of(base, state_rule=None):
        return shadow_of_value(effective(base, "box-shadow", state_rule), base)

    def resting_body(base):
        """The element's own resting rule — the one that declares its
        outline. A rule inside a media query only overrides the element for
        one viewport, so it is not the element's resting state."""
        own = None
        for _, r in by_base.get(base, []):
            if r.selector == base and not is_state(r.selector) and r.media is None:
                own = r
        return own.body if own is not None else ""

    # ---- 1. every shadow is hard, and square when it has no spread ------
    # ---- 1b. no gradients on any surface ------------------------------
    # The system bans gradients outright. A hard-stop gradient is still
    # a gradient, so "but it does not fade" is not an exemption.
    # The skeleton shimmer is the single documented exception: it is a
    # loading affordance, not a surface treatment.
    GRADIENT_EXEMPT = (".fp-skeleton",)
    for name, r in all_rules:
        value = ""
        for prop in ("background-image", "background"):
            v = decl(r.body, prop)
            if v:
                value += " " + v
        if "gradient(" not in value:
            continue
        if any(e in r.selector for e in GRADIENT_EXEMPT):
            continue
        fail(f"{name}: '{r.selector}' uses a gradient — the system bans gradients on every surface")

    # ---- 1c. every shadow is hard --------------------------------------
    for name, r in all_rules:
        if not has_prop(r.body, "box-shadow"):
            continue
        for (dx, dy, blur, spread, colour) in parse_shadow(decl(r.body, "box-shadow"), ctx_for(base_of(r.selector))):
            if blur != 0:
                fail(f"{name}: '{r.selector}' shadow has blur {blur:g}px — shadows must be hard (blur 0)")
            # THE SHADOW CONTRACT
            #   * X and Y offsets are both POSITIVE — a shadow always
            #     falls to the bottom-right. A negative offset means the
            #     shadow falls the wrong way, and the system forbids it.
            #   * X and Y are EQUAL — a square shadow, never a skewed one.
            #   * blur is 0 (checked above) and spread is 0. A positive
            #     spread paints a band on all four sides; that is a
            #     border, not a shadow, and it is forbidden.
            if spread != 0:
                fail(f"{name}: '{r.selector}' shadow has spread {spread:g}px — spread paints a band on all four sides, which is a border, not a shadow")
            if dx <= 0 or dy <= 0:
                fail(f"{name}: '{r.selector}' shadow offsets must be POSITIVE (x={dx:g}, y={dy:g}) — shadows always fall to the bottom-right")
            elif dx != dy:
                fail(f"{name}: '{r.selector}' shadow offsets differ (x={dx:g}, y={dy:g}) — shadows must be square (x == y)")

    # ---- 2. main elements: no border, and they do have a shadow --------
    for marker in MAIN_MARKERS:
        if marker not in by_base:
            fail(f"MAIN '{marker}' has no rule at all")
            continue
        bd = effective(marker, "border")
        if bd and not re.match(r"^(none|0)\b", bd.strip()):
            fail(f"MAIN '{marker}' must have no border, found: {bd}")
        # The element's OWN rule must carry the shadow. A variant rule
        # (a joined button group, a modifier) may take it away, but the
        # element itself must never be shadow-less.
        own_rule = None
        for _, r in by_base.get(marker, []):
            if r.selector == marker and not is_state(r.selector) and r.media is None:
                own_rule = r
        if own_rule is None:
            fail(f"MAIN '{marker}' has no rule of its own")
            continue
        if shadow_of_value(decl(own_rule.body, "box-shadow"), marker) is None:
            fail(f"MAIN '{marker}' has no shadow")

    # ---- 3. sub elements: inline border, no default shadow -------------
    for marker in SUB_MARKERS:
        if marker not in by_base:
            fail(f"SUB '{marker}' has no rule at all")
            continue
        own_rule = None
        for _, r in by_base.get(marker, []):
            if r.selector == marker and not is_state(r.selector) and r.media is None:
                own_rule = r
        if own_rule is None:
            fail(f"SUB '{marker}' has no rule of its own")
            continue
        bd = decl(own_rule.body, "border")
        if not bd:
            fail(f"SUB '{marker}' must have an inline border")
        elif re.match(r"^(none|0)\b", bd.strip()):
            fail(f"SUB '{marker}' border is {bd} — sub elements need a real border")
        sh = decl(own_rule.body, "box-shadow")
        if sh is not None and shadow_of_value(sh, marker) is not None:
            fail(f"SUB '{marker}' must have NO default shadow, found: {sh}")

    # ---- 3c. filled controls: NO border, NO resting shadow, lift on hover --
    for marker in SUB_FILLED:
        if marker not in by_base:
            fail(f"SUB(filled) '{marker}' has no rule at all")
            continue
        own_rule = None
        for _, r in by_base.get(marker, []):
            if r.selector == marker and not is_state(r.selector) and r.media is None:
                own_rule = r
        if own_rule is None:
            fail(f"SUB(filled) '{marker}' has no rule of its own")
            continue
        bd = decl(own_rule.body, "border")
        if bd and not re.match(r"^(none|0)\b", bd.strip()):
            fail(f"SUB(filled) '{marker}' must be borderless, found: {bd}")
        sh = decl(own_rule.body, "box-shadow")
        if sh is not None and shadow_of_value(sh, marker) is not None:
            fail(f"SUB(filled) '{marker}' must have NO default shadow, found: {sh}")

    # ---- 3b. borderless subs: NO border, NO resting shadow, but the lift --
    for marker in SUB_BORDERLESS:
        if marker not in by_base:
            fail(f"SUB(borderless) '{marker}' has no rule at all")
            continue
        own_rule = None
        for _, r in by_base.get(marker, []):
            if r.selector == marker and not is_state(r.selector) and r.media is None:
                own_rule = r
        if own_rule is None:
            fail(f"SUB(borderless) '{marker}' has no rule of its own")
            continue
        bd = decl(own_rule.body, "border")
        if bd and not re.match(r"^(none|0)\b", bd.strip()):
            fail(f"SUB(borderless) '{marker}' must be borderless, found: {bd}")
        sh = decl(own_rule.body, "box-shadow")
        if sh is not None and shadow_of_value(sh, marker) is not None:
            fail(f"SUB(borderless) '{marker}' must have NO default shadow, found: {sh}")
        # A rising borderless sub must still gain a shadow on hover.
        has_hover_shadow = False
        for _, r in by_base.get(marker, []):
            if ":hover" in r.selector and shadow_of_value(decl(r.body, "box-shadow") or "", marker) is not None:
                has_hover_shadow = True
        if not has_hover_shadow:
            fail(f"SUB(borderless) '{marker}' must gain a shadow on hover")

    # ---- 4. hover semantics ---------------------------------------------
    #   MAIN hover: translateY positive (moves down) AND shadow shrinks
    #   SUB  hover: translateY negative (moves up)   AND shadow APPEARS
    #   FORBIDDEN: the element moves up while its shadow shrinks
    for name, r in all_rules:
        if not any(p in r.selector for p in (":hover", ":focus-visible", ":focus-within", ":active")):
            continue
        tr = decl(r.body, "transform")
        if tr is None:
            continue
        base = base_of(r.selector)
        trr = resolve_vars(tr, ctx_for(base))
        dy = translate_y(trr, ctx_for(base))
        if dy is None:
            continue

        resting = shadow_of_value(decl(resting_body(base), "box-shadow"), base)
        hover = shadow_of(base, r)

        if base in MAIN_PINNED:
            hover_sh = shadow_of(base, r)
            resting_sh = resting
            if dy != 0:
                fail(f"{name}: '{r.selector}' is PINNED (fixed/docked) — it must never travel on hover")
                continue
            if resting_sh is not None and (hover_sh is None or shadow_size(hover_sh) != shadow_size(resting_sh)):
                fail(f"{name}: '{r.selector}' is PINNED — its shadow must not change on hover")
                continue
            notes.append(f"{name}: '{r.selector}' is pinned and stays put — OK")
            continue
        if dy < 0:
            if base in MAIN_MARKERS:
                fail(f"{name}: '{r.selector}' is a MAIN element and moves UP — mains only press down")
                continue
            if base in SUB_MARKERS + SUB_BORDERLESS + SUB_FILLED and resting is not None and shadow_size(hover or (0,0,0,0,"")) < shadow_size(resting):
                fail(f"{name}: '{r.selector}' moves UP while its shadow shrinks "
                     f"({shadow_size(resting):g}px -> {shadow_size(hover or (0,0,0,0,'')):g}px) — that combination is forbidden")
                continue
            if hover is None:
                fail(f"{name}: '{r.selector}' moves UP but has NO shadow — a rising element must gain a shadow")
                continue
            if resting is not None and shadow_size(hover) < shadow_size(resting):
                fail(f"{name}: '{r.selector}' moves UP while its shadow shrinks "
                     f"({shadow_size(resting):g}px -> {shadow_size(hover):g}px) — that combination is forbidden")
                continue
            notes.append(f"{name}: '{r.selector}' moves UP and gains a shadow — OK for SUB (the shadow appears while rising)")
        elif dy > 0:
            if base in SUB_MARKERS + SUB_BORDERLESS + SUB_FILLED and resting is None and hover is None:
                fail(f"{name}: '{r.selector}' is a SUB element but has no shadow at all")
                continue
            kind = "appears" if resting is None else (
                "shrinks" if shadow_size(hover or (0, 0, 0, 0, "")) < shadow_size(resting) else "keeps/grows")
            notes.append(f"{name}: '{r.selector}' moves DOWN (dy={dy:g}) — shadow {kind} — OK for MAIN (the press)")

    print("=" * 66)
    print("FlatPlanet — elevation verification")
    print("=" * 66)
    print(f"CSS files scanned: {len(files)}")
    print()
    if notes:
        print(f"Observations ({len(notes)}):")
        for n in notes:
            print("  ·", n)
        print()
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for f in failures:
            print("  ✗", f)
        print()
        sys.exit(1)
    print("All elevation rules hold.")
    sys.exit(0)


if __name__ == "__main__":
    main()
