"""
Cinematic PDF cover — universal visual identity for PDF guides.
Dark cyberpunk cover: circuit traces, hex badge, bold cyan/orange type.
Drop-in replacement for bbg_style.title_page (same signature).
"""
import math, random
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

PAGE_W, PAGE_H = letter

BG      = HexColor("#080C14")
CYAN    = HexColor("#00E5FF")
ORANGE  = HexColor("#FF8C00")
WHITE   = HexColor("#F5F8FC")
GRAY    = HexColor("#96A5B9")
DIM_CYAN = HexColor("#007896")
DIM_ORG  = HexColor("#96500A")

TITLE_FONT = "Helvetica-Bold"
BODY_FONT  = "Helvetica"


# --- Topic theme palettes (2026-10-09 themed-content rollout) ---
# theme key -> (primary accent, secondary accent). Matches the canonical
# accents in docs/assets/il-topic-themes.css (parallel CSS workstream).
TOPIC_THEME_COLORS = {
    "mr-robot":   ("#00ff41", "#008f11"),
    "cyberpunk":  ("#ff2a6d", "#05d9e8"),
    "tron":       ("#00e5ff", "#7df9ff"),
    "steampunk":  ("#b08d57", "#b87333"),
    "exmachina":  ("#f5f5f5", "#8a8a8a"),
    "oceandeep":  ("#39ffce", "#1b6f8f"),
    "hackers95":  ("#ff00ff", "#ccff00"),
    "alexandria": ("#d4af37", "#f8f5ec"),
    "industrial": ("#ffb000", "#cc7a00"),
    "sacredgeo":  ("#e8c15a", "#8a6d2f"),
    "vaporwave":  ("#ff71ce", "#b967ff"),
    "goldrush":   ("#ffd700", "#8a6d00"),
}


def _shade(hexcolor, factor):
    """Darken a #rrggbb hex string by factor; returns a HexColor."""
    h = str(hexcolor).lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (max(0, min(255, int(x * factor))) for x in (r, g, b))
    return HexColor("#%02x%02x%02x" % (r, g, b))


def theme_palette(theme):
    """Return (primary, secondary, dim_primary, dim_secondary) HexColors for a
    theme key, or None when the theme is unknown/None (caller keeps defaults)."""
    pal = TOPIC_THEME_COLORS.get(theme)
    if not pal:
        return None
    p1_hex, p2_hex = pal
    return (HexColor(p1_hex), HexColor(p2_hex),
            _shade(p1_hex, 0.45), _shade(p2_hex, 0.45))


def _circuit(c, seed=7):
    rng = random.Random(seed)
    c.setLineWidth(1)
    for i in range(22):
        x, y = rng.uniform(0, PAGE_W), rng.uniform(0, PAGE_H)
        c.setStrokeColor(DIM_CYAN if i % 3 else DIM_ORG)
        p = c.beginPath()
        p.moveTo(x, y)
        for _ in range(rng.randint(2, 4)):
            d = rng.choice(["h", "v"])
            ln = rng.randint(30, 130)
            if d == "h":
                x = min(max(x + rng.choice([-1, 1]) * ln, 0), PAGE_W)
            else:
                y = min(max(y + rng.choice([-1, 1]) * ln, 0), PAGE_H)
            p.lineTo(x, y)
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(DIM_CYAN if i % 3 else DIM_ORG)
        c.circle(x, y, 2.5, stroke=0, fill=1)


def _hexagon(c, cx, cy, r, color, width=2.5):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    p = c.beginPath()
    for k in range(6):
        a = math.pi / 6 + k * math.pi / 3
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        if k == 0:
            p.moveTo(x, y)
        else:
            p.lineTo(x, y)
    p.close()
    c.drawPath(p, stroke=1, fill=0)


def cinematic_cover(c, title, subtitle, category, page_num_ref, theme=None):
    """Cinematic cover page. Same signature as bbg_style.title_page, plus an
    optional theme key (one of the 12 topic themes) that recolors the cover's
    accent palette. theme=None keeps the default cyan/orange identity."""
    pal = theme_palette(theme)
    P1, P2 = (pal[0], pal[1]) if pal else (CYAN, ORANGE)          # primary/secondary accents
    DIM1, DIM2 = (pal[2], pal[3]) if pal else (DIM_CYAN, DIM_ORG)  # dim circuit traces
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    _circuit_themed(c, DIM1, DIM2)
    # corner brackets
    c.setStrokeColor(P1)
    c.setLineWidth(2.5)
    m, L = 28, 26
    for (x0, y0, dx, dy) in [(m, PAGE_H - m, 1, -1), (PAGE_W - m, PAGE_H - m, -1, -1),
                             (m, m, 1, 1), (PAGE_W - m, m, -1, 1)]:
        c.line(x0, y0, x0 + dx * L, y0)
        c.line(x0, y0, x0, y0 + dy * L)
    # header
    c.setFillColor(P1)
    c.setFont(TITLE_FONT, 10)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 64,
                        "INTERSTITIUM LABS \u00b7 SCIENTIA OMNIA VINCIT")
    # hex badge with category initial
    _hexagon(c, PAGE_W / 2, PAGE_H - 220, 64, P1)
    _hexagon(c, PAGE_W / 2, PAGE_H - 220, 54, DIM1, width=1.5)
    c.setFillColor(WHITE)
    c.setFont(TITLE_FONT, 40)
    initial = (category or "I").strip()[:1].upper()
    c.drawCentredString(PAGE_W / 2, PAGE_H - 208, initial)
    # category eyebrow
    c.setFillColor(P2)
    c.setFont(TITLE_FONT, 11)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 330, category.upper())
    # title
    c.setFillColor(WHITE)
    c.setFont(TITLE_FONT, 30)
    y = PAGE_H - 372
    for line in title.split("\n"):
        c.drawCentredString(PAGE_W / 2, y, line)
        y -= 38
    # subtitle
    c.setFillColor(GRAY)
    c.setFont(BODY_FONT, 13)
    y -= 10
    for line in subtitle.split("\n"):
        c.drawCentredString(PAGE_W / 2, y, line)
        y -= 20
    # animated-walkthrough badge
    c.setStrokeColor(P1)
    c.setLineWidth(1.5)
    c.roundRect(PAGE_W / 2 - 140, 150, 280, 52, 8, fill=0, stroke=1)
    c.setFillColor(P1)
    c.setFont(TITLE_FONT, 10)
    c.drawCentredString(PAGE_W / 2, 178, "ANIMATED WALKTHROUGH")
    c.setFillColor(GRAY)
    c.setFont(BODY_FONT, 9)
    c.drawCentredString(PAGE_W / 2, 162, "Step through pages to play the animation")
    # theme tag (proves which theme colored the cover)
    if theme:
        c.setFillColor(P2)
        c.setFont(TITLE_FONT, 8)
        c.drawCentredString(PAGE_W / 2, 128, "THEME \u00b7 " + str(theme).upper().replace("-", " "))
    # footer
    c.setFillColor(GRAY)
    c.setFont(BODY_FONT, 9)
    c.drawCentredString(PAGE_W / 2, 72,
                        "Interstitium Labs  \u00b7  interstitiumlabs.dev  \u00b7  Original diagrams")
    c.setPageTransition(effectname="Dissolve", duration=0.5)
    c.showPage()


def _circuit_themed(c, dim1, dim2, seed=7):
    rng = random.Random(seed)
    c.setLineWidth(1)
    for i in range(22):
        x, y = rng.uniform(0, PAGE_W), rng.uniform(0, PAGE_H)
        c.setStrokeColor(dim1 if i % 3 else dim2)
        p = c.beginPath()
        p.moveTo(x, y)
        for _ in range(rng.randint(2, 4)):
            d = rng.choice(["h", "v"])
            ln = rng.randint(30, 130)
            if d == "h":
                x = min(max(x + rng.choice([-1, 1]) * ln, 0), PAGE_W)
            else:
                y = min(max(y + rng.choice([-1, 1]) * ln, 0), PAGE_H)
            p.lineTo(x, y)
        c.drawPath(p, stroke=1, fill=0)
        c.setFillColor(dim1 if i % 3 else dim2)
        c.circle(x, y, 2.5, stroke=0, fill=1)
