#!/usr/bin/env python3
"""Draw the pentagon shapes on both serviceable-line pages and both social cards from the data below.

    python3 scripts/build-line-shapes.py

Each shape is a surface (what the offering asks of someone, per layer) and a line (how much of
that surface customers and their AI get through alone), on a 0 to 3 scale per layer. The values
are illustrative and say so on the page. The script rewrites the blocks between
<!-- shapes:NAME:start --> and <!-- shapes:NAME:end --> in the page, so edit the data here, never
the SVG in the HTML. Standard library only.
"""
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "serviceable-line/shapes/index.html"
MAIN_PAGE = ROOT / "serviceable-line/index.html"
LAYERS = ["Findable", "Selectable", "Integrable", "Operable", "Fixable"]
MAX = 3.0

# name, surface, line, carried, caption[, earlier surface]
# carried is how far the work gets once partners, dealers, service companies and third-party
# sites are counted too, so line <= carried <= surface on every layer.
OFFERINGS = [
    ("Bag of rice", [0.8, 0.8, 0, 0.4, 0], [0.2, 0.3, 0, 0.4, 0], [0.75, 0.75, 0, 0.4, 0],
     "Two short layers, and the retailer carries most of both. Nothing to connect, nothing to fix."),
    ("Cordless drill", [2.2, 2.4, 2.0, 1.2, 2.0], [1.8, 1.5, 0.8, 1.0, 0.6], [2.0, 1.9, 1.1, 1.0, 1.3],
     "The battery platform is an Integrable layer, error lights and spare parts a Fixable one. Forums and repair sites carry what the maker does not publish."),
    ("Payments platform", [2.6, 3.0, 3.0, 2.8, 3.0], [2.2, 1.0, 2.2, 1.0, 1.0], [2.3, 1.4, 2.6, 1.4, 1.4],
     "Documentation carries Integrable a long way. Required onboarding checks and payment disputes hold the line in, whatever the AI can do. Platforms that resell payments carry part of it."),
    ("Medical device", [1.8, 3.0, 2.6, 2.6, 3.0], [1.0, 0.7, 0.7, 0.8, 0.5], [1.5, 1.4, 1.4, 1.6, 2.0],
     "The longest Selectable: clinical evidence, approvals and a hospital committee. Distributors and hospital technicians carry much of the rest, and the AI doing that work is theirs, not the buyer's."),
    ("Clinic", [2.6, 2.6, 1.4, 2.2, 1.8], [2.0, 1.2, 0.6, 1.3, 0.7], [2.3, 1.6, 0.9, 1.4, 0.9],
     "A service has a surface too: coverage, preparation, follow-up and the bill. Insurer directories and booking sites answer part of it."),
    ("API-first software", [3, 3, 3, 3, 3], [2.5, 1.6, 2.2, 1.3, 1.5], [2.6, 2.0, 2.7, 1.6, 2.0],
     "All five layers, in depth, and the one shape where every layer can be tested from outside today. Review sites and implementation partners carry part of it."),
]

SEGMENTS = [
    ("Sold to a small business", [2.6, 1.8, 1.6, 2.0, 1.8], [2.2, 1.5, 1.3, 1.4, 1.2], [2.3, 1.6, 1.4, 1.5, 1.4],
     "A smaller surface, and the line close to its edge."),
    ("Sold to an enterprise", [3, 3, 3, 3, 3], [2.2, 1.2, 1.0, 1.0, 0.9], [2.4, 1.8, 2.0, 1.5, 1.4],
     "Security review, procurement and many systems to connect: a bigger surface, systems integrators carrying part of it, and a bigger gap."),
]

DRILL = OFFERINGS[1]
GROWTH = [
    ("A drill today", DRILL[1], DRILL[2], DRILL[3],
     "The cordless drill from the six offerings above."),
    ("The same drill, software-defined", [2.4, 2.8, 2.8, 2.4, 2.8], [2.0, 1.7, 1.0, 1.1, 0.8], [2.2, 2.1, 1.4, 1.3, 1.5],
     "An app, firmware updates and tool tracking. The surface grew on four layers, the line moved less, so the gap grew.",
     DRILL[1]),
]

# The main page hero: an offering with all five layers in depth, so the surface is full, plus the
# gold outline for where the line is moving. Same drawing code as the sub-page, so the two heroes
# follow one set of rules: dashed maximum, solid surface, grey gap, blue line.
MAIN_LINE = [2.46, 1.5, 1.98, 1.2, 1.68]
MAIN_HERO = ([3, 3, 3, 3, 3], MAIN_LINE, MAIN_LINE)
MAIN_MOVE = [2.91, 2.04, 2.52, 1.74, 2.22]

# the shapes hero introduces the idea, so it shows no work carried by others
HERO = ([2.4, 2.8, 1.4, 2.2, 1.0], [2.0, 1.5, 0.8, 1.1, 0.4], [2.0, 1.5, 0.8, 1.1, 0.4])


def pt(i, v, r):
    a = math.radians(-90 + i * 72)
    f = v / MAX
    return r * f * math.cos(a), r * f * math.sin(a)


def poly(vals, r):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in (pt(i, v, r) for i, v in enumerate(vals)))


def size_word(v):
    return "short" if v < 1 else "medium" if v < 2 else "long"


def carried_word(s, l):
    f = l / s
    return "almost all" if f >= .8 else "most" if f >= .55 else "about half" if f >= .35 else "little"


def describe(name, surface, line, carried):
    parts = []
    for n, s, l, c in zip(LAYERS, surface, line, carried):
        if s == 0:
            parts.append(f"{n}: none")
        else:
            others = ", more by others" if c - l >= .2 else ""
            parts.append(f"{n}: {size_word(s)} surface, {carried_word(s, l)} of it carried alone{others}")
    return f"{name}. " + "; ".join(parts) + "."


def label_pos(i, r, gap):
    x, y = pt(i, MAX, r)
    if i == 0:
        return x, y - gap, "middle"
    if i == 1:
        return x + gap, y + 5, "start"
    if i == 4:
        return x - gap, y + 5, "end"
    return x, y + gap + 12, "middle"


def svg(name, surface, line, carried, *, prefix, r, viewbox, font_gap, old=None, move=None, labels=True,
        indent="          "):
    p = prefix
    label = describe(name, surface, line, carried)
    if move:
        label += " A gold dotted outline further out shows where the line is moving."
    out = [f'<svg viewBox="{viewbox}" role="img" aria-label="{label}">']
    for f in (1, 2):
        out.append(f'  <polygon class="{p}-ring" points="{poly([f] * 5, r)}"/>')
    out.append(f'  <polygon class="{p}-ring {p}-max" points="{poly([MAX] * 5, r)}"/>')
    for i in range(5):
        x, y = pt(i, MAX, r)
        out.append(f'  <line class="{p}-spoke" x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}"/>')
    if old:
        out.append(f'  <polygon class="{p}-old" points="{poly(old, r)}"/>')
    out.append(f'  <polygon class="{p}-surface" points="{poly(surface, r)}"/>')
    if carried != line:
        out.append(f'  <polygon class="{p}-other" points="{poly(carried, r)}"/>')
    if move:
        out.append(f'  <polygon class="{p}-move" points="{poly(move, r)}"/>')
    out.append(f'  <polygon class="{p}-line" points="{poly(line, r)}"/>')
    for i, v in enumerate(line):
        if v > 0:
            x, y = pt(i, v, r)
            out.append(f'  <circle class="{p}-vtx" cx="{x:.1f}" cy="{y:.1f}" r="{3.5 if p == "sh" else 5}"/>')
    if labels:
        for i, n in enumerate(LAYERS):
            x, y, anchor = label_pos(i, r, font_gap)
            if surface[i] == 0:
                out.append(f'  <text class="{p}-name is-none" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{n}'
                           f'<tspan class="{p}-none" x="{x:.1f}" dy="1.15em">none</tspan></text>')
            else:
                out.append(f'  <text class="{p}-name" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{n}</text>')
    out.append("</svg>")
    return "\n".join(indent + l for l in out)


def card(name, surface, line, carried, caption, old=None):
    for l, c, su in zip(line, carried, surface):
        assert l <= c <= su, f"{name}: line <= carried <= surface broken"
    body = svg(name, surface, line, carried, prefix="sh", r=92, viewbox="-190 -124 380 244", font_gap=12, old=old,
               indent="              ")
    return (f'            <figure class="shape-card">\n{body}\n'
            f'              <figcaption><h3>{name}</h3><p>{caption}</p></figcaption>\n'
            f'            </figure>')


def grid(items, cls="shape-grid"):
    cards = [card(*item) for item in items]
    return f'          <div class="{cls}">\n' + "\n".join(cards) + "\n          </div>"


HERO_BOX = dict(prefix="ld", r=168, viewbox="-296 -214 592 424", font_gap=18)


def blocks():
    return {
        PAGE: {
            "hero": svg("An illustrative offering", *HERO, **HERO_BOX),
            "grid": grid(OFFERINGS),
            "segments": grid(SEGMENTS, "shape-grid shape-pair"),
            "growth": grid(GROWTH, "shape-grid shape-pair"),
        },
        MAIN_PAGE: {
            "main-hero": svg("An illustrative offering with all five layers in depth", *MAIN_HERO,
                             move=MAIN_MOVE, **HERO_BOX),
        },
    }


FONT = 'font-family="Noto Sans, Liberation Sans, Arial, Helvetica, sans-serif"'
MINT, GOLD, BLUE, INK, PAPER = "#a8bdc1", "#dcb96f", "#2f72ff", "#101a1d", "#f4efe6"


def card_pentagon(cx, cy, r, surface, line, move=None, labels=True, label_size=20):
    """The hero pentagon with inline styles, for the standalone social-card SVGs."""
    out = [f'  <g transform="translate({cx} {cy})">']
    for f in (1, 2):
        out.append(f'    <polygon points="{poly([f] * 5, r)}" fill="none" stroke="{MINT}" stroke-opacity=".12"/>')
    out.append(f'    <polygon points="{poly([MAX] * 5, r)}" fill="none" stroke="{MINT}" stroke-opacity=".38" stroke-dasharray="4 6"/>')
    for i in range(5):
        x, y = pt(i, MAX, r)
        out.append(f'    <line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{MINT}" stroke-opacity=".16"/>')
    out.append(f'    <polygon points="{poly(surface, r)}" fill="{MINT}" fill-opacity=".14" stroke="{MINT}" stroke-width="1.6" stroke-linejoin="round"/>')
    if move:
        out.append(f'    <polygon points="{poly(move, r)}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="0 9" stroke-linecap="round" stroke-linejoin="round" opacity=".8"/>')
    out.append(f'    <polygon points="{poly(line, r)}" fill="{BLUE}" fill-opacity=".26" stroke="{BLUE}" stroke-width="2.5" stroke-linejoin="round"/>')
    for i, v in enumerate(line):
        if v > 0:
            x, y = pt(i, v, r)
            out.append(f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{BLUE}" stroke="{INK}" stroke-width="2"/>')
    if labels:
        for i, n in enumerate(LAYERS):
            x, y, anchor = label_pos(i, r, 18)
            out.append(f'    <text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {FONT} font-size="{label_size}" fill="{MINT}">{n}</text>')
    out.append("  </g>")
    return "\n".join(out)


def card_svg(title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="cardtitle carddesc">\n'
            f'  <title id="cardtitle">{title}</title>\n  <desc id="carddesc">{desc}</desc>\n'
            f'  <rect width="1200" height="630" fill="{INK}"/>\n{body}\n</svg>\n')


def legend_row(x, y, kind, text):
    swatch = {
        "line": f'<rect x="{x}" y="{y - 12}" width="22" height="14" rx="2" fill="{BLUE}" fill-opacity=".26" stroke="{BLUE}" stroke-width="2"/>',
        "gap": f'<rect x="{x}" y="{y - 12}" width="22" height="14" rx="2" fill="{MINT}" fill-opacity=".14" stroke="{MINT}" stroke-opacity=".4"/>',
        "move": f'<path d="M{x + 3} {y - 5}H{x + 21}" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-dasharray="0 8" opacity=".85"/>',
    }[kind]
    return f'  {swatch}\n  <text x="{x + 34}" y="{y}" {FONT} font-size="17" fill="{MINT}" opacity=".8">{text}</text>'


def main_card():
    body = "\n".join([
        card_pentagon(890, 270, 172, MAIN_HERO[0], MAIN_HERO[1], move=MAIN_MOVE),
        legend_row(700, 520, "line", "Carried by your customers and their AI"),
        legend_row(700, 550, "gap", "Your people step in, or the customer is lost"),
        legend_row(700, 580, "move", "Where the line is moving"),
        f'  <text x="80" y="196" {FONT} font-size="68" font-weight="700" letter-spacing="-1" fill="{PAPER}">The serviceable</text>',
        f'  <text x="80" y="274" {FONT} font-size="68" font-weight="700" letter-spacing="-1" fill="{PAPER}">line</text>',
        f'  <text x="80" y="352" {FONT} font-size="30" fill="{MINT}">How far does your customer\'s</text>',
        f'  <text x="80" y="394" {FONT} font-size="30" fill="{MINT}">AI get without you?</text>',
        f'  <text x="80" y="548" {FONT} font-size="21" fill="{GOLD}">A point of view by Etgar Bonar</text>',
        f'  <text x="80" y="580" {FONT} font-size="21" fill="{MINT}" opacity=".5">etgarbonar.com</text>',
    ])
    return card_svg("The serviceable line",
                    "A pentagon with one spoke per layer: Findable, Selectable, Integrable, Operable and Fixable. "
                    "The blue shape is how far your customers and their AI get on each; past it, your people step in or the customer is lost; "
                    "a gold dotted outline further out shows where the line is moving. How far does your customer's AI get without you? "
                    "A point of view by Etgar Bonar.", body)


def shapes_card():
    picks = [OFFERINGS[0], OFFERINGS[3], OFFERINGS[5]]
    parts = []
    for cx, (name, surface, line, *_rest) in zip((240, 600, 960), picks):
        parts.append(card_pentagon(cx, 160, 100, surface, line, labels=False))
        parts.append(f'  <text x="{cx}" y="300" text-anchor="middle" {FONT} font-size="20" fill="{MINT}">{name}</text>')
    parts += [
        f'  <path d="M80 340H1120" stroke="#233236" stroke-width="1"/>',
        f'  <text x="80" y="420" {FONT} font-size="56" font-weight="700" letter-spacing="-1" fill="{PAPER}">The shape of the serviceable line</text>',
        f'  <text x="80" y="474" {FONT} font-size="28" fill="{MINT}">How far does your customer\'s AI get without you?</text>',
        f'  <text x="80" y="560" {FONT} font-size="21" fill="{GOLD}">A point of view by Etgar Bonar</text>',
        f'  <text x="1120" y="560" text-anchor="end" {FONT} font-size="21" fill="{MINT}" opacity=".5">etgarbonar.com</text>',
    ]
    return card_svg("The shape of the serviceable line",
                    "Three pentagons: a bag of rice with almost no surface, a medical device with a long Selectable and a short line, "
                    "and API-first software with all five layers in depth. How far does your customer's AI get without you? "
                    "Not every offering has five layers. A point of view by Etgar Bonar.", "\n".join(parts))


def main():
    for page, named in blocks().items():
        html = page.read_text()
        for name, content in named.items():
            pattern = re.compile(rf"(<!-- shapes:{name}:start -->\n).*?(<!-- shapes:{name}:end -->)", re.S)
            html, n = pattern.subn(lambda m: m.group(1) + content + "\n" + m.group(2), html)
            if n != 1:
                raise SystemExit(f"marker shapes:{name} not found exactly once in {page.name}")
        page.write_text(html)
        print(f"wrote {page.relative_to(ROOT)}")
    for name, svg_text in (("serviceable-line-card", main_card()), ("serviceable-shapes-card", shapes_card())):
        path = ROOT / "assets" / f"{name}.svg"
        path.write_text(svg_text)
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
