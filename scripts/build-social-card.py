import base64, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
logo_b64 = base64.b64encode((root / "assets/logo-256.png").read_bytes()).decode()

GRID_H = "M0 80H1440M0 170H1440M0 260H1440M0 350H1440M0 440H1440M0 530H1440M0 620H1440M0 710H1440"
GRID_V = ("M90 0V820M180 0V820M270 0V820M360 0V820M450 0V820M540 0V820M630 0V820M720 0V820"
          "M810 0V820M900 0V820M990 0V820M1080 0V820M1170 0V820M1260 0V820M1350 0V820")

routes = [
    ("M-30 156 C210 156 304 212 498 310 S716 407 805 421", "plain"),
    ("M-30 282 C212 282 332 307 510 366 S718 416 805 425", "primary"),
    ("M-30 502 C217 502 338 463 506 427 S712 428 805 429", "plain"),
    ("M-30 666 C215 666 316 559 504 477 S714 447 805 433", "plain"),
    ("M-30 756 C183 756 326 604 512 499 S715 459 805 437", "plain"),
    ("M864 410 C932 360 970 294 1046 285 S1130 276 1214 270", "primary"),
    ("M864 440 C930 482 967 547 1042 555 S1134 563 1215 560", "plain"),
    ("M1254 270 C1330 271 1364 235 1470 188", "primary"),
    ("M1252 560 C1320 546 1370 491 1470 452", "plain"),
    ("M1280 591 C1234 754 930 748 728 708 C478 658 310 751 -20 716", "return"),
]
ROUTE_STYLE = {
    "plain": 'stroke="#a8bdc1" stroke-opacity=".33" stroke-width="1.25"',
    "primary": 'stroke="#a8bdc1" stroke-opacity=".55" stroke-width="1.55"',
    "return": 'stroke="#dcb96f" stroke-opacity=".44" stroke-width="1.35" stroke-dasharray="4 9"',
}
pulses = [
    "M-30 282 C212 282 332 307 510 366 S718 416 805 425 C932 360 970 294 1046 285 S1130 276 1214 270 C1330 271 1364 235 1470 188",
    "M-30 666 C215 666 316 559 504 477 S714 447 805 433 C930 482 967 547 1042 555 S1134 563 1215 560 C1320 546 1370 491 1470 452",
]
small_nodes = [
    (245, 151, 5, "plain"), (361, 223, 6, "accent"), (519, 375, 5, "plain"), (620, 398, 6, "plain"),
    (690, 418, 6, "accent"), (411, 486, 5, "plain"), (247, 591, 5, "plain"), (563, 465, 6, "accent"),
    (952, 340, 5, "plain"), (993, 300, 5, "plain"), (1315, 229, 6, "value"), (980, 532, 5, "plain"),
    (1092, 557, 6, "accent"), (1370, 491, 6, "value"),
]
NODE_FILL = {
    "plain": 'fill="#a8bdc1" fill-opacity=".6"',
    "accent": 'fill="#dcb96f" fill-opacity=".9"',
    "value": 'fill="#8ecbc0" fill-opacity=".95"',
}

parts = []
parts.append('<g fill="none" stroke="#a8bdc1" stroke-opacity=".12" stroke-width="1">')
parts.append('<path d="%s"/><path d="%s"/></g>' % (GRID_H, GRID_V))
parts.append('<circle cx="836" cy="427" r="132" fill="url(#coreGlow)"/>')
parts.append('<circle cx="1164" cy="272" r="132" fill="url(#valueGlow)"/>')
parts.append('<g fill="none" stroke-linecap="round">')
for d, kind in routes:
    parts.append('<path d="%s" fill="none" %s/>' % (d, ROUTE_STYLE[kind]))
for d in pulses:
    parts.append('<path d="%s" fill="none" stroke="#2f72ff" stroke-opacity=".8" '
                 'stroke-width="1.4" stroke-dasharray="2 22" stroke-linecap="round"/>' % d)
parts.append('</g>')
parts.append('<g>')
for x, y, s, kind in small_nodes:
    parts.append('<rect x="%d" y="%d" width="%d" height="%d" %s/>' % (x, y, s, s, NODE_FILL[kind]))
parts.append('</g>')
parts.append('''
<g>
  <g transform="translate(836 427)">
    <circle r="54" fill="none" stroke="#dcb96f" stroke-opacity=".4" stroke-width="1" stroke-dasharray="3 6"/>
    <circle r="34" fill="#17272b" stroke="#dcb96f" stroke-opacity=".95" stroke-width="2"/>
    <circle r="7" fill="#dcb96f"/>
    <path d="M-15 0H15M0-15V15" fill="none" stroke="#101a1d" stroke-width="2"/>
  </g>
  <g transform="translate(1047 285)">
    <circle r="23" fill="#101a1d" stroke="#a8bdc1" stroke-opacity=".8" stroke-width="1.5"/>
    <path d="M-9 0H9M0-9V9" fill="none" stroke="#a8bdc1" stroke-width="1.4"/>
  </g>
  <g transform="translate(1042 555)">
    <circle r="23" fill="#101a1d" stroke="#a8bdc1" stroke-opacity=".8" stroke-width="1.5"/>
    <circle r="7" fill="none" stroke="#a8bdc1" stroke-width="1.4"/>
  </g>
  <g transform="translate(1234 270)">
    <circle r="28" fill="#17282a" stroke="#8ecbc0" stroke-opacity=".95" stroke-width="2"/>
    <path d="M-12 1L-3 10 14-12" fill="none" stroke="#8ecbc0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</g>''')
system = "\n    ".join(parts)

FONT = "Noto Sans, Liberation Sans, Arial, Helvetica, sans-serif"

svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="630" viewBox="0 0 1200 630" role="img" aria-labelledby="title desc">
  <title id="title">Etgar Bonar, Revenue and GTM Executive</title>
  <desc id="desc">Strategy, revenue, technology, and execution</desc>
  <defs>
    <radialGradient id="coreGlow" cx="50%%" cy="50%%" r="50%%">
      <stop offset="0%%" stop-color="#dcb96f" stop-opacity=".2"/>
      <stop offset="100%%" stop-color="#dcb96f" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="valueGlow" cx="50%%" cy="50%%" r="50%%">
      <stop offset="0%%" stop-color="#8ecbc0" stop-opacity=".19"/>
      <stop offset="100%%" stop-color="#8ecbc0" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="scrim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%%" stop-color="#101a1d" stop-opacity="1"/>
      <stop offset="46%%" stop-color="#101a1d" stop-opacity=".94"/>
      <stop offset="72%%" stop-color="#101a1d" stop-opacity=".48"/>
      <stop offset="100%%" stop-color="#101a1d" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="logoClip"><circle cx="124" cy="116" r="44"/></clipPath>
  </defs>

  <rect width="1200" height="630" fill="#101a1d"/>
  <svg x="0" y="0" width="1200" height="630" viewBox="0 0 1440 820" preserveAspectRatio="xMidYMid slice">
    %s
  </svg>
  <rect width="1000" height="630" fill="url(#scrim)"/>

  <image xlink:href="data:image/png;base64,%s" x="80" y="72" width="88" height="88" clip-path="url(#logoClip)"/>
  <circle cx="124" cy="116" r="45" fill="none" stroke="#f4efe6" stroke-width="3" stroke-opacity=".92"/>

  <text x="80" y="288" font-family="%s" font-size="76" font-weight="700" letter-spacing="-1.6" fill="#f4efe6">Etgar Bonar</text>
  <text x="80" y="348" font-family="%s" font-size="34" font-weight="400" fill="#a8bdc1">Revenue &amp; GTM Executive</text>
  <path d="M80 404H300" stroke="#dcb96f" stroke-opacity=".7" stroke-width="2"/>
  <text x="80" y="466" font-family="%s" font-size="27" font-weight="500" fill="#f4efe6" fill-opacity=".92">Strategy &#183; Revenue &#183; Technology &#183; Execution</text>
  <text x="80" y="548" font-family="%s" font-size="25" font-weight="600" fill="#dcb96f">etgarbonar.com</text>
</svg>
''' % (system, logo_b64, FONT, FONT, FONT, FONT)

out = root / "assets/social-card-v2.svg"
out.write_text(svg)
print("wrote", out, len(svg), "bytes")
