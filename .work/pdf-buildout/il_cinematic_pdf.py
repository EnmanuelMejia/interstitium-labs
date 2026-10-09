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


def cinematic_cover(c, title, subtitle, category, page_num_ref):
    """Cinematic cover page. Same signature as bbg_style.title_page."""
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    _circuit(c)
    # corner brackets
    c.setStrokeColor(CYAN)
    c.setLineWidth(2.5)
    m, L = 28, 26
    for (x0, y0, dx, dy) in [(m, PAGE_H - m, 1, -1), (PAGE_W - m, PAGE_H - m, -1, -1),
                             (m, m, 1, 1), (PAGE_W - m, m, -1, 1)]:
        c.line(x0, y0, x0 + dx * L, y0)
        c.line(x0, y0, x0, y0 + dy * L)
    # header
    c.setFillColor(CYAN)
    c.setFont(TITLE_FONT, 10)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 64,
                        "INTERSTITIUM LABS \u00b7 SCIENTIA OMNIA VINCIT")
    # hex badge with category initial
    _hexagon(c, PAGE_W / 2, PAGE_H - 220, 64, CYAN)
    _hexagon(c, PAGE_W / 2, PAGE_H - 220, 54, DIM_CYAN, width=1.5)
    c.setFillColor(WHITE)
    c.setFont(TITLE_FONT, 40)
    initial = (category or "I").strip()[:1].upper()
    c.drawCentredString(PAGE_W / 2, PAGE_H - 208, initial)
    # category eyebrow
    c.setFillColor(ORANGE)
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
    c.setStrokeColor(CYAN)
    c.setLineWidth(1.5)
    c.roundRect(PAGE_W / 2 - 140, 150, 280, 52, 8, fill=0, stroke=1)
    c.setFillColor(CYAN)
    c.setFont(TITLE_FONT, 10)
    c.drawCentredString(PAGE_W / 2, 178, "ANIMATED WALKTHROUGH")
    c.setFillColor(GRAY)
    c.setFont(BODY_FONT, 9)
    c.drawCentredString(PAGE_W / 2, 162, "Step through pages to play the animation")
    # footer
    c.setFillColor(GRAY)
    c.setFont(BODY_FONT, 9)
    c.drawCentredString(PAGE_W / 2, 72,
                        "Interstitium Labs  \u00b7  interstitiumlabs.dev  \u00b7  Original diagrams")
    c.setPageTransition(effectname="Dissolve", duration=0.5)
    c.showPage()
