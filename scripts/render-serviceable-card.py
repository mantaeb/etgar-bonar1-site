"""Render assets/serviceable-line-card.svg to the 1200x630 PNG used for og:image.

Chrome's headless screenshot clips roughly 110px off the bottom when --window-size
matches the content exactly, so the page is rendered taller and cropped back down.
Run:  python3 scripts/render-serviceable-card.py [card name, default serviceable-line-card]
"""
import pathlib, subprocess, sys, tempfile, zlib, struct

W, H = 1200, 630
root = pathlib.Path(__file__).resolve().parent.parent
name = sys.argv[1] if len(sys.argv) > 1 else "serviceable-line-card"
svg = root / f"assets/{name}.svg"
png = root / f"assets/{name}.png"


def decode(path):
    data = path.read_bytes()
    off, idat = 8, []
    while off < len(data):
        ln = struct.unpack(">I", data[off:off + 4])[0]
        kind = data[off + 4:off + 8]
        if kind == b"IHDR":
            w, h, _, color = struct.unpack(">IIBB", data[off + 8:off + 18])
        elif kind == b"IDAT":
            idat.append(data[off + 8:off + 8 + ln])
        off += 12 + ln
    bpp = 4 if color == 6 else 3
    raw = zlib.decompress(b"".join(idat))
    stride = w * bpp + 1
    out = bytearray(w * h * bpp)
    for y in range(h):
        filt = raw[y * stride]
        line = raw[y * stride + 1:y * stride + 1 + w * bpp]
        base, prev = y * w * bpp, (y - 1) * w * bpp
        for x in range(w * bpp):
            a = out[base + x - bpp] if x >= bpp else 0
            b = out[prev + x] if y else 0
            c = out[prev + x - bpp] if (x >= bpp and y) else 0
            v = line[x]
            if filt == 1:
                v += a
            elif filt == 2:
                v += b
            elif filt == 3:
                v += (a + b) >> 1
            elif filt == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                v += a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
            out[base + x] = v & 255
    return w, h, bpp, out


def encode(path, w, h, bpp, px):
    stride = w * bpp
    raw = b"".join(b"\x00" + bytes(px[y * stride:(y + 1) * stride]) for y in range(h))

    def chunk(kind, payload):
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body))

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6 if bpp == 4 else 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


with tempfile.TemporaryDirectory() as tmp:
    page = pathlib.Path(tmp) / "card.html"
    page.write_text('<!doctype html><meta charset="utf-8">'
                    '<style>html,body{margin:0;padding:0;background:#101a1d}'
                    'svg{display:block}</style>\n' + svg.read_text())
    shot = pathlib.Path(tmp) / "tall.png"
    subprocess.run(["google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=3000", f"--window-size={W},{H + 190}",
                    f"--screenshot={shot}", page.as_uri()],
                   check=True, capture_output=True)
    sw, sh, bpp, px = decode(shot)
    assert sw == W and sh >= H, f"unexpected render size {sw}x{sh}"
    crop = bytearray(W * H * bpp)
    for y in range(H):
        crop[y * W * bpp:(y + 1) * W * bpp] = px[y * sw * bpp:y * sw * bpp + W * bpp]
    encode(png, W, H, bpp, crop)

print(f"wrote {png.relative_to(root)} {W}x{H}")
