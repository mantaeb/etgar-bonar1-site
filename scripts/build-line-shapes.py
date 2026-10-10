#!/usr/bin/env python3
"""Draw the bar charts on both serviceable-line pages and both social cards from the data below.

    python3 scripts/build-line-shapes.py

Each offering is a surface (what it asks of someone, per layer: the bar's length) and a line (how
much of that surface customers and their AI get through alone: the blue, ending at a white mark), on a 0 to 3 scale per layer. The values
are illustrative and say so on the page. The script rewrites the blocks between
<!-- shapes:NAME:start --> and <!-- shapes:NAME:end --> in the page, so edit the data here, never
the SVG in the HTML. Standard library only.
"""
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
     "Two short layers, each a few facts to look up, and the retailer carries most of both. Integrable and Fixable score zero: nothing to connect, nothing to fix."),
    ("Cordless drill", [2.2, 2.4, 2.0, 1.2, 2.0], [1.8, 1.5, 0.8, 1.0, 0.6], [2.0, 1.9, 1.1, 1.0, 1.3],
     "The battery platform is an Integrable layer. Error lights and spare parts make Fixable a procedure to follow. Forums and repair sites carry what the maker does not publish."),
    ("Payments platform", [2.6, 3.0, 3.0, 2.8, 3.0], [2.2, 1.0, 2.2, 1.0, 1.0], [2.3, 1.4, 2.6, 1.4, 1.4],
     "Authentication and a working sandbox connection are Integrable, a system to configure and keep running. Creating and verifying a payment are Operable. Required onboarding checks and payment disputes hold the line in, whatever the AI can do. Platforms that resell payments carry part of it."),
    ("Medical device", [1.8, 3.0, 2.6, 2.6, 3.0], [1.0, 0.7, 0.7, 0.8, 0.5], [1.5, 1.4, 1.4, 1.6, 2.0],
     "The longest Selectable: clinical evidence, approvals and a hospital committee. Distributors and hospital technicians carry much of the rest, and the AI doing that work is theirs, not the buyer's."),
    ("Clinic", [2.6, 2.6, 1.4, 2.2, 1.8], [2.0, 1.2, 0.6, 1.3, 0.7], [2.3, 1.6, 0.9, 1.4, 0.9],
     "A service has a surface too: coverage, preparation, follow-up and the bill. Insurer directories and booking sites answer part of it."),
    ("API-first software", [3, 3, 3, 3, 3], [2.5, 1.6, 2.2, 1.3, 1.5], [2.6, 2.0, 2.7, 1.6, 2.0],
     "All five layers, each at the top of the scale, and the one shape where every layer can be tested from outside today. Review sites and implementation partners carry part of it."),
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

# The hero offering. Bar length is the surface on every hero, so the layers differ in length from the
# first screen (Etgar, 2026-10-04). Both heroes and the main social card carry gold arrows for where the
# line is heading: on Findable and Selectable (Etgar, 2026-10-03), plus a small one on Operable, which
# moves last (Etgar, 2026-10-05). Integrable gets an almost complete arrow, because it usually moves
# before Operable (Etgar, 2026-10-07). The values do not fall steadily from top to bottom, so
# the five bars never read as a trend or a ranking.
HERO_SURFACE = [2.7, 3.0, 2.0, 2.4, 1.6]
HERO_LINE = [1.9, 1.3, 1.5, 0.9, 1.1]
HERO_ARROWS = {0: 2.5, 1: 2.3, 2: 1.9, 3: 1.25}
assert all(HERO_LINE[i] < v <= HERO_SURFACE[i] for i, v in HERO_ARROWS.items())
# The main page hero and the main social card follow Clip A (Etgar, 2026-10-10): blue is what customers
# carry, solid gold is what their AI carries on top, and the white mark sits at the end of the gold. The
# gold ends where the shapes-page arrows point, so both pages draw the same numbers. The shapes page keeps
# the arrows, because its six cards have no customer/AI split and share the hero's legend.
SIMPLE = (HERO_SURFACE, HERO_LINE, HERO_LINE)
FULL = (HERO_SURFACE, HERO_LINE, HERO_LINE)
# The main hero and the main card also put a little gold on Fixable, taken from its blue so its mark stays
# put: most fixes needed outside people, and AI now carries some (Etgar, 2026-10-10, matching Clip A v8).
# The shapes page keeps HERO_LINE and HERO_ARROWS until its new image replaces that hero.
MAIN_LINE = HERO_LINE[:4] + [0.85]
MAIN_AI = {**HERO_ARROWS, 4: 1.1}
MAIN = (HERO_SURFACE, MAIN_LINE, MAIN_LINE)
assert all(MAIN_LINE[i] < v <= HERO_SURFACE[i] for i, v in MAIN_AI.items())

FONT = 'font-family="Noto Sans, Liberation Sans, Arial, Helvetica, sans-serif"'
MINT, GOLD, BLUE, INK, PAPER = "#a8bdc1", "#dcb96f", "#2f72ff", "#101a1d", "#f4efe6"

# Inline styles for the standalone social-card SVGs; the pages use CSS classes instead.
CARD_STYLE = {
    "track": f'fill="{MINT}" fill-opacity=".14" stroke="{MINT}" stroke-opacity=".45"',
    "line": f'fill="{BLUE}"',
    "gain": f'fill="{GOLD}" fill-opacity=".35"',
    "ai": f'fill="{GOLD}"',
    "mark": f'stroke="{PAPER}" stroke-width="3" stroke-linecap="round"',
    "arrow": f'stroke="{GOLD}" stroke-width="3" stroke-linecap="round"',
    "arrowhead": f'fill="{GOLD}"',
    "name": f'{FONT} font-size="20" fill="{MINT}"',
    "none": f'{FONT} font-size="14" fill="{MINT}" opacity=".45"',
}


def size_word(v):
    return "short" if v < 1 else "medium" if v < 2 else "long"


def carried_word(s, l):
    f = l / s
    return "almost all" if f >= .8 else "most" if f >= .55 else "about half" if f >= .35 else "little"


def describe(name, surface, line, carried, arrows=None, ai=None):
    ai, parts = ai or {}, []
    for i, (n, s, l, c) in enumerate(zip(LAYERS, surface, line, carried)):
        if s == 0:
            parts.append(f"{n}: none")
        else:
            others = ", more by others" if c - l >= .2 else ""
            parts.append(f"{n}: {size_word(s)} surface, {carried_word(s, ai.get(i, l))} of it carried alone{others}")
    text = f"{name}, one bar per layer. " + "; ".join(parts) + ". A white mark on each bar is the serviceable line."
    if arrows:
        names = [LAYERS[i] for i in sorted(arrows)]
        text += f" Gold arrows on {', '.join(names[:-1])} and {names[-1]} show where the line is heading."
    if ai:
        names = [LAYERS[i] for i in sorted(ai)]
        text += (f" Blue is what customers carry. Gold on {', '.join(names[:-1])} and {names[-1]} is what their AI carries,"
                 " and the mark sits at its end.")
    return text


def bar_rows(surface, line, carried, *, x0, y0, unit, step, h, arrows=None, ai=None, old=None, labels=True,
             style=None, prefix="ld", ox=0, oy=0):
    """The five bars. Each row: the track (its length is the surface), teal for work someone else
    carries, gold for where the line is heading, blue for what customers and their AI carry alone,
    and a white mark at the end of the blue, which is the serviceable line on that layer.
    With ai, blue is what customers carry, solid gold runs on to ai[i] for what their AI carries,
    and the mark moves to the end of the gold.
    style=None draws with CSS classes (prefix-bar-*); a style dict draws with inline attributes."""
    att = (lambda k: style[k]) if style else (lambda k: f'class="{prefix}-bar-{k}"')
    arrows, ai, out = arrows or {}, ai or {}, []
    for i, n in enumerate(LAYERS):
        y = oy + y0 + i * step
        x = ox + x0
        if labels:
            name_att = style["name"] if style else f'class="{prefix}-name{" is-none" if surface[i] == 0 else ""}"'
            out.append(f'<text x="{x - 14}" y="{y + 6}" text-anchor="end" {name_att}>{n}</text>')
        if surface[i] == 0:
            none_att = style["none"] if style else f'class="{prefix}-none"'
            out.append(f'<text x="{x}" y="{y + 5}" {none_att}>none</text>')
            continue
        if old:
            out.append(f'<rect x="{x}" y="{y - h / 2}" width="{old[i] * unit:.1f}" height="{h}" rx="{h / 4}" {att("old")}/>')
        out.append(f'<rect x="{x}" y="{y - h / 2}" width="{surface[i] * unit:.1f}" height="{h}" rx="{h / 4}" {att("track")}/>')
        if carried[i] > line[i]:
            out.append(f'<rect x="{x}" y="{y - h / 2}" width="{carried[i] * unit:.1f}" height="{h}" rx="{h / 4}" {att("other")}/>')
        if i in arrows:
            out.append(f'<rect x="{x}" y="{y - h / 2}" width="{arrows[i] * unit:.1f}" height="{h}" rx="{h / 4}" {att("gain")}/>')
        if i in ai:
            out.append(f'<rect x="{x}" y="{y - h / 2}" width="{ai[i] * unit:.1f}" height="{h}" rx="{h / 4}" {att("ai")}/>')
        if line[i] > 0:
            out.append(f'<rect x="{x}" y="{y - h / 2}" width="{line[i] * unit:.1f}" height="{h}" rx="{h / 4}" {att("line")}/>')
        mx = x + ai.get(i, line[i]) * unit
        out.append(f'<line x1="{mx:.1f}" y1="{y - h / 2 - 6}" x2="{mx:.1f}" y2="{y + h / 2 + 6}" {att("mark")}/>')
        if i in arrows:
            tip, head = x + arrows[i] * unit, 10
            out.append(f'<line x1="{mx + 8:.1f}" y1="{y}" x2="{tip - head:.1f}" y2="{y}" {att("arrow")}/>')
            out.append(f'<polygon points="{tip:.1f},{y} {tip - head:.1f},{y - 6} {tip - head:.1f},{y + 6}" {att("arrowhead")}/>')
    return out


def svg(name, surface, line, carried, *, kind, arrows=None, ai=None, old=None, indent="          "):
    if kind == "hero":
        geo, prefix, w, hgt = dict(x0=132, y0=36, unit=148, step=62, h=22), "ld", 600, 320
    else:
        geo, prefix, w, hgt = dict(x0=100, y0=24, unit=88, step=40, h=16), "sh", 380, 208
    rows = bar_rows(surface, line, carried, arrows=arrows, ai=ai, old=old, prefix=prefix, **geo)
    label = describe(name, surface, line, carried, arrows, ai)
    out = [f'<svg viewBox="0 0 {w} {hgt}" role="img" aria-label="{label}">'] + ["  " + r for r in rows] + ["</svg>"]
    return "\n".join(indent + l for l in out)


def card(name, surface, line, carried, caption, old=None):
    for l, c, su in zip(line, carried, surface):
        assert l <= c <= su, f"{name}: line <= carried <= surface broken"
    body = svg(name, surface, line, carried, kind="card", old=old, indent="              ")
    return (f'            <figure class="shape-card">\n{body}\n'
            f'              <figcaption><h3>{name}</h3><p>{caption}</p></figcaption>\n'
            f'            </figure>')


def grid(items, cls="shape-grid"):
    cards = [card(*item) for item in items]
    return f'          <div class="{cls}">\n' + "\n".join(cards) + "\n          </div>"


def blocks():
    return {
        PAGE: {
            "hero": svg("An illustrative offering", *FULL, kind="hero", arrows=HERO_ARROWS),
            "grid": grid(OFFERINGS),
            "segments": grid(SEGMENTS, "shape-grid shape-pair"),
            "growth": grid(GROWTH, "shape-grid shape-pair"),
        },
        MAIN_PAGE: {
            "main-hero": svg("An illustrative offering", *MAIN, kind="hero", ai=MAIN_AI),
        },
    }


def card_svg(title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="cardtitle carddesc">\n'
            f'  <title id="cardtitle">{title}</title>\n  <desc id="carddesc">{desc}</desc>\n'
            f'  <rect width="1200" height="630" fill="{INK}"/>\n{body}\n</svg>\n')


def legend_row(x, y, kind, text):
    swatch = {
        "line": f'<rect x="{x}" y="{y - 12}" width="22" height="14" rx="3" fill="{BLUE}"/>',
        "gap": f'<rect x="{x}" y="{y - 12}" width="22" height="14" rx="3" fill="{MINT}" fill-opacity=".14" stroke="{MINT}" stroke-opacity=".45"/>',
        "surface": f'<rect x="{x}" y="{y - 12}" width="22" height="14" rx="3" fill="none" stroke="{MINT}" stroke-opacity=".7" stroke-width="1.5"/>',
        "mark": f'<line x1="{x + 11}" y1="{y - 15}" x2="{x + 11}" y2="{y + 3}" stroke="{PAPER}" stroke-width="3" stroke-linecap="round"/>',
        "ai": f'<rect x="{x}" y="{y - 12}" width="22" height="14" rx="3" fill="{GOLD}"/>',
        "move": f'<line x1="{x}" y1="{y - 5}" x2="{x + 14}" y2="{y - 5}" stroke="{GOLD}" stroke-width="3" stroke-linecap="round"/><polygon points="{x + 22},{y - 5} {x + 13},{y - 11} {x + 13},{y + 1}" fill="{GOLD}"/>',
    }[kind]
    return f'  {swatch}\n  <text x="{x + 34}" y="{y}" {FONT} font-size="17" fill="{MINT}" opacity=".8">{text}</text>'


def main_card():
    rows = bar_rows(*MAIN, x0=800, y0=110, unit=112, step=60, h=24, style=CARD_STYLE, ai=MAIN_AI)
    body = "\n".join(["  " + r for r in rows] + [
        legend_row(690, 450, "surface", "The surface: what your offering asks of someone"),
        legend_row(690, 482, "mark", "The serviceable line"),
        legend_row(690, 514, "line", "Carried by your customers"),
        legend_row(690, 546, "ai", "Carried by their AI"),
        legend_row(690, 578, "gap", "Your people step in, or revenue is lost"),
        f'  <text x="80" y="196" {FONT} font-size="68" font-weight="700" letter-spacing="-1" fill="{PAPER}">The serviceable</text>',
        f'  <text x="80" y="274" {FONT} font-size="68" font-weight="700" letter-spacing="-1" fill="{PAPER}">line</text>',
        f'  <text x="80" y="352" {FONT} font-size="30" fill="{MINT}">How far do your customers,</text>',
        f'  <text x="80" y="394" {FONT} font-size="30" fill="{MINT}">and their AI, get without you?</text>',
        f'  <text x="80" y="548" {FONT} font-size="21" fill="{GOLD}">A point of view by Etgar Bonar</text>',
        f'  <text x="80" y="580" {FONT} font-size="21" fill="{MINT}" opacity=".5">etgarbonar.com</text>',
    ])
    return card_svg("The serviceable line",
                    "Five bars, one per layer: Findable, Selectable, Integrable, Operable and Fixable, each as long as what the offering asks on that layer. A mark on each bar "
                    "is the serviceable line: how far your customers and their AI get on that layer on their own. Past it, your people step in "
                    "or revenue is lost. Blue is what customers carry; gold on all five layers is what their AI carries, and the mark sits at its end. "
                    "How far do your customers, and their AI, get without you? A point of view by Etgar Bonar.", body)


def shapes_card():
    picks = [OFFERINGS[0], OFFERINGS[3], OFFERINGS[5]]
    parts = []
    for gx, (name, surface, line, *_rest) in zip((80, 440, 800), picks):
        parts += ["  " + r for r in bar_rows(surface, line, line, x0=0, y0=70, unit=100, step=38, h=18,
                                              labels=False, style=CARD_STYLE, ox=gx)]
        parts.append(f'  <text x="{gx}" y="290" {FONT} font-size="20" fill="{MINT}">{name}</text>')
    parts += [
        f'  <path d="M80 340H1120" stroke="#233236" stroke-width="1"/>',
        f'  <text x="80" y="420" {FONT} font-size="56" font-weight="700" letter-spacing="-1" fill="{PAPER}">The shape of the serviceable line</text>',
        f'  <text x="80" y="474" {FONT} font-size="28" fill="{MINT}">How far do your customers, and their AI, get without you?</text>',
        f'  <text x="80" y="560" {FONT} font-size="21" fill="{GOLD}">A point of view by Etgar Bonar</text>',
        f'  <text x="1120" y="560" text-anchor="end" {FONT} font-size="21" fill="{MINT}" opacity=".5">etgarbonar.com</text>',
    ]
    return card_svg("The shape of the serviceable line",
                    "Three sets of five bars: a bag of rice with three short bars and two layers missing, a medical device with long bars "
                    "and little of each carried by the customer, and API-first software with five full bars. How far do your customers, and their AI, get without you? "
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
