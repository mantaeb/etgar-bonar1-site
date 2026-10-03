#!/usr/bin/env python3
"""Draw the pentagon shapes on /serviceable-line/shapes/ from the data below.

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

# the hero introduces the idea, so it shows no work carried by others
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


def svg(name, surface, line, carried, *, prefix, r, viewbox, font_gap, old=None, labels=True, indent="          "):
    p = prefix
    out = [f'<svg viewBox="{viewbox}" role="img" aria-label="{describe(name, surface, line, carried)}">']
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


def blocks():
    hero = svg("An illustrative offering", *HERO, prefix="ld", r=168,
               viewbox="-296 -214 592 424", font_gap=18)
    return {
        "hero": hero,
        "grid": grid(OFFERINGS),
        "segments": grid(SEGMENTS, "shape-grid shape-pair"),
        "growth": grid(GROWTH, "shape-grid shape-pair"),
    }


def main():
    html = PAGE.read_text()
    for name, content in blocks().items():
        pattern = re.compile(rf"(<!-- shapes:{name}:start -->\n).*?(<!-- shapes:{name}:end -->)", re.S)
        html, n = pattern.subn(lambda m: m.group(1) + content + "\n" + m.group(2), html)
        if n != 1:
            raise SystemExit(f"marker shapes:{name} not found exactly once")
    PAGE.write_text(html)
    print(f"wrote {PAGE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
