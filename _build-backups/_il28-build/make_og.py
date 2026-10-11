#!/usr/bin/env python3
"""Build the IL-28 OG preview card (1200x630 PNG)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = "/home/hatch/workspace/apex-audit/docs/university/og/il-28-devsecops-og.png"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H))
px = img.load()
# vertical gradient: deep navy -> near black
for y in range(H):
    t = y / H
    r = int(6 + (4 - 6) * t)
    g = int(10 + (6 - 10) * t)
    b = int(28 + (14 - 28) * t)
    for x in range(W):
        # subtle radial glow behind center text
        dx, dy = x - W / 2, y - H / 2
        glow = max(0, 1 - (dx * dx + dy * dy) ** 0.5 / 700)
        px[x, y] = (min(255, r + int(14 * glow)), min(255, g + int(18 * glow)), min(255, b + int(38 * glow)))

d = ImageDraw.Draw(img)

def centered(y, text, fnt, fill):
    bb = d.textbbox((0, 0), text, font=fnt)
    tw = bb[2] - bb[0]
    d.text(((W - tw) / 2 - bb[0], y), text, font=fnt, fill=fill)

# top kicker
centered(64, "INTERSTITIUM LABS  ·  SCIENTIA OMNIA VINCIT", font(FR, 30), (150, 170, 205))
# accent rule
d.rectangle([W / 2 - 90, 116, W / 2 + 90, 120], fill=(64, 180, 255))
# big code
centered(150, "IL-28", font(FB, 150), (255, 255, 255))
# title (two lines to be safe)
centered(330, "DevSecOps & Cloud Infrastructure", font(FB, 54), (235, 242, 255))
centered(400, "Mastery Bootcamp", font(FB, 54), (235, 242, 255))
# bottom domain
centered(540, "interstitiumlabs.dev", font(FR, 34), (120, 145, 180))

img.save(OUT, "PNG")
print("saved", OUT)
