#!/usr/bin/env python3
"""Generate Interstitium Labs brand launcher icons + splash screens from the
glyph-only sigil (docs/assets/chrome/sigil-glyph.svg).

Renders the sigil geometry directly with Pillow (no SVG rasterizer needed) so
`npx capacitor-assets` is optional. Deterministic: same input -> same pixels.

Usage: python3 gen-brand-assets.py   (run from repo root)

Outputs:
  apps/mobile/android/app/src/main/res/mipmap-*/ic_launcher{,_round,_foreground}.png
  apps/mobile/android/app/src/main/res/drawable*/splash.png (brand void + sigil)
  apps/mobile/android/app/src/main/res/drawable-nodpi/sigil_mark.png (launch drawable mark)
  apps/mobile/ios/App/App/Assets.xcassets/AppIcon.appiconset/*.png + Contents.json
  apps/mobile/ios/App/App/Assets.xcassets/Splash.imageset/*.png
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]  # repo root
RES = ROOT / "apps/mobile/android/app/src/main/res"
XC = ROOT / "apps/mobile/ios/App/App/Assets.xcassets"

VOID = (0x07, 0x0B, 0x16, 255)
GOLD = (0xD4, 0xA8, 0x53, 255)
CYAN = (0x5E, 0xEA, 0xD4, 255)

# Sigil geometry in a 64x64 viewBox, mirroring docs/assets/chrome/sigil-glyph.svg
TRI = [(32, 8), (52, 48), (12, 48)]
ELLIPSES = [
    (0, 1.35, 1.0),
    (60, 1.1, 0.75),
    (-60, 1.0, 0.55),
]
RECTS = [
    (21.5, 18, 2.4, 26),
    (40.1, 18, 2.4, 26),
    (40.1, 41.2, 10.5, 2.4),
]
CORE = (32, 32, 3.2)


def _with_opacity(layer: Image.Image, opacity: float) -> Image.Image:
    if opacity >= 1.0:
        return layer
    a = layer.getchannel("A").point(lambda v: int(v * opacity))
    layer = layer.copy()
    layer.putalpha(a)
    return layer


def render_sigil(px: int, *, background=VOID, mono=None, supersample=4) -> Image.Image:
    """Render the sigil glyph at px x px. mono: single RGB color for tinted icons."""
    n = px * supersample
    s = n / 64.0  # svg units -> pixels
    gold = mono + (255,) if mono else GOLD
    cyan = mono + (255,) if mono else CYAN

    base = Image.new("RGBA", (n, n), background if background else (0, 0, 0, 0))

    def layer():
        return Image.new("RGBA", (n, n), (0, 0, 0, 0))

    # Gold triangle
    l = layer()
    d = ImageDraw.Draw(l)
    d.polygon([(x * s, y * s) for x, y in TRI], outline=gold, width=max(1, round(1.35 * s)))
    base = Image.alpha_composite(base, _with_opacity(l, 0.9))

    # Cyan orbital ellipses
    for angle, w, op in ELLIPSES:
        l = layer()
        d = ImageDraw.Draw(l)
        d.ellipse(
            [(32 - 16) * s, (32 - 6.2) * s, (32 + 16) * s, (32 + 6.2) * s],
            outline=cyan,
            width=max(1, round(w * s)),
        )
        if angle:
            # PIL rotates counter-clockwise; SVG rotate() is clockwise.
            l = l.rotate(-angle, resample=Image.BICUBIC, center=(32 * s, 32 * s))
        base = Image.alpha_composite(base, _with_opacity(l, op))

    # Gold bars + core
    l = layer()
    d = ImageDraw.Draw(l)
    for x, y, w, h in RECTS:
        d.rounded_rectangle([x * s, y * s, (x + w) * s, (y + h) * s],
                            radius=0.4 * s, fill=gold)
    cx, cy, r = CORE
    d.ellipse([(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s], fill=gold)
    base = Image.alpha_composite(base, l)

    return base.resize((px, px), Image.LANCZOS)


def full_bleed(px: int, glyph_frac: float, **kw) -> Image.Image:
    """Void background with the glyph centered at glyph_frac of the canvas."""
    img = Image.new("RGBA", (px, px), VOID)
    g = render_sigil(round(px * glyph_frac), background=None, **kw)
    img.alpha_composite(g, ((px - g.width) // 2, (px - g.height) // 2))
    return img.convert("RGB")


def circle_mask(img: Image.Image) -> Image.Image:
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).ellipse([0, 0, img.width, img.height], fill=255)
    img = img.copy()
    img.putalpha(m)
    return img


def main() -> None:
    # ---- Android legacy + round icons (full-bleed) ----
    densities = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
    for name, px in densities.items():
        d = RES / f"mipmap-{name}"
        d.mkdir(parents=True, exist_ok=True)
        icon = full_bleed(px, 0.66)
        icon.save(d / "ic_launcher.png")
        circle_mask(icon).save(d / "ic_launcher_round.png")
        # Adaptive foreground: transparent 108dp canvas, glyph in the 72dp safe zone
        fg_px = {48: 108, 72: 162, 96: 216, 144: 324, 192: 432}[px]
        fg = Image.new("RGBA", (fg_px, fg_px), (0, 0, 0, 0))
        g = render_sigil(round(fg_px * 72 / 108), background=None)
        fg.alpha_composite(g, ((fg_px - g.width) // 2, (fg_px - g.height) // 2))
        fg.save(d / "ic_launcher_foreground.png")
        print("android", name, px)

    # ---- Android launch-drawable sigil mark (transparent, nodpi) ----
    nodpi = RES / "drawable-nodpi"
    nodpi.mkdir(parents=True, exist_ok=True)
    render_sigil(512, background=None).save(nodpi / "sigil_mark.png")
    print("android drawable-nodpi/sigil_mark.png")

    # ---- Android splash PNGs: keep existing sizes, brand artwork ----
    for p in sorted(RES.glob("drawable*/splash.png")):
        with Image.open(p) as im:
            w, h = im.size
        img = Image.new("RGB", (w, h), VOID[:3])
        g = render_sigil(round(min(w, h) * 0.40), background=None)
        img.paste(g, ((w - g.width) // 2, (h - g.height) // 2), g)
        img.save(p)
        print("splash", p.relative_to(RES), f"{w}x{h}")

    # ---- iOS app icon set: 1024 + dark + tinted variants ----
    appicon = XC / "AppIcon.appiconset"
    full_bleed(1024, 0.66).save(appicon / "AppIcon-1024.png")
    full_bleed(1024, 0.66).save(appicon / "AppIcon-dark-1024.png")
    tinted = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    g = render_sigil(round(1024 * 0.60), background=None, mono=GOLD[:3])
    tinted.alpha_composite(g, ((1024 - g.width) // 2, (1024 - g.height) // 2))
    tinted.save(appicon / "AppIcon-tinted-1024.png")
    old = appicon / "AppIcon-512@2x.png"
    if old.exists():
        old.unlink()
    contents = {
        "images": [
            {"filename": "AppIcon-1024.png", "idiom": "universal",
             "platform": "ios", "size": "1024x1024"},
            {"appearances": [{"appearance": "luminosity", "value": "dark"}],
             "filename": "AppIcon-dark-1024.png", "idiom": "universal",
             "platform": "ios", "size": "1024x1024"},
            {"appearances": [{"appearance": "luminosity", "value": "tinted"}],
             "filename": "AppIcon-tinted-1024.png", "idiom": "universal",
             "platform": "ios", "size": "1024x1024"},
        ],
        "info": {"author": "xcode", "version": 1},
    }
    (appicon / "Contents.json").write_text(json.dumps(contents, indent=2) + "\n")
    print("ios AppIcon.appiconset (1024 + dark + tinted)")

    # ---- iOS splash imageset: keep file names/structure, brand artwork ----
    splashset = XC / "Splash.imageset"
    for name in ("splash-2732x2732.png", "splash-2732x2732-1.png", "splash-2732x2732-2.png"):
        p = splashset / name
        if not p.exists():
            continue
        img = Image.new("RGB", (2732, 2732), VOID[:3])
        g = render_sigil(round(2732 * 0.30), background=None)
        img.paste(g, ((2732 - g.width) // 2, (2732 - g.height) // 2), g)
        img.save(p)
        print("ios", name)


if __name__ == "__main__":
    sys.exit(main())
