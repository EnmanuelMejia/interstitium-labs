"""
BBG-style PDF framework — original diagrams in the visual language of
leading system-design explainers. Clean boxes, flow arrows, numbered steps,
annotations. No copied assets; all shapes drawn programmatically.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER

PAGE_W, PAGE_H = letter  # 612 x 792

# --- Palette (original, BBG-inspired) ---
BG        = HexColor("#FFFFFF")
INK       = HexColor("#1A1A2E")
MUTED     = HexColor("#5A5A6E")
ACCENT    = HexColor("#4361EE")   # blue
ACCENT2   = HexColor("#3A0CA3")   # deep purple
GREEN     = HexColor("#06D6A0")
ORANGE    = HexColor("#FF9F1C")
RED       = HexColor("#EF476F")
TEAL      = HexColor("#0AA6A6")
LIGHT_BG  = HexColor("#F4F6FB")
BOX_BLUE  = HexColor("#DCE6FF")
BOX_GREEN = HexColor("#D6F5E8")
BOX_ORANGE= HexColor("#FFEFD2")
BOX_RED   = HexColor("#FFDDE6")
BOX_TEAL  = HexColor("#D2F0F0")
BOX_PURP  = HexColor("#E6DDF7")

TITLE_FONT = "Helvetica-Bold"
BODY_FONT  = "Helvetica"
MONO_FONT  = "Courier"

styles = getSampleStyleSheet()


def new_canvas(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.setTitle("Interstitium Labs — Visual Guide")
    return c


def title_page(c, title, subtitle, category, page_num_ref, theme=None):
    """Cover page — cinematic standard (2026-10-09). Delegates to il_cinematic_pdf.

    theme: optional topic-theme key (one of the 12 themed-content themes);
    recolors the cover's accent palette. theme=None keeps the default
    cyan/orange identity (all existing gen_* scripts are unaffected)."""
    try:
        from il_cinematic_pdf import cinematic_cover
        return cinematic_cover(c, title, subtitle, category, page_num_ref, theme=theme)
    except Exception:
        pass
    # legacy fallback
    c.setFillColor(BG); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # top accent bar
    c.setFillColor(ACCENT); c.rect(0, PAGE_H - 14, PAGE_W, 14, fill=1, stroke=0)
    # eyebrow
    c.setFillColor(ACCENT); c.setFont(TITLE_FONT, 11)
    c.drawString(72, PAGE_H - 90, category.upper())
    # title
    c.setFillColor(INK); c.setFont(TITLE_FONT, 30)
    y = PAGE_H - 130
    for line in title.split("\n"):
        c.drawString(72, y, line); y -= 38
    # subtitle
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 13)
    y -= 12
    for line in subtitle.split("\n"):
        c.drawString(72, y, line); y -= 20
    # animated-walkthrough badge
    c.setFillColor(BOX_BLUE); c.roundRect(72, 200, 260, 44, 8, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.setFont(TITLE_FONT, 10)
    c.drawString(88, 226, "ANIMATED WALKTHROUGH")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawString(88, 212, "Step through pages to play the animation")
    # footer
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawString(72, 72, "Interstitium Labs  •  interstitiumlabs.dev  •  Original diagrams")
    c.setFont(BODY_FONT, 9); c.drawRightString(PAGE_W - 72, 72, "Page 1")
    # page transition: dissolve on present
    c.setPageTransition(effectname="Dissolve", duration=0.5)
    c.showPage()


def section_header(c, step_no, total_steps, heading, sub=None):
    """Step header bar used on every diagram page."""
    c.setFillColor(BG); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(0, PAGE_H - 14, PAGE_W, 14, fill=1, stroke=0)
    # step pill
    c.setFillColor(ACCENT2); c.roundRect(72, PAGE_H - 66, 92, 26, 13, fill=1, stroke=0)
    c.setFillColor(white); c.setFont(TITLE_FONT, 11)
    c.drawCentredString(118, PAGE_H - 49, f"STEP {step_no}/{total_steps}")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 17)
    c.drawString(176, PAGE_H - 49, heading)
    if sub:
        c.setFillColor(MUTED); c.setFont(BODY_FONT, 11)
        c.drawString(72, PAGE_H - 92, sub)
    return PAGE_H - 130  # content top y


def footer(c, page_no):
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 9)
    c.drawString(72, 48, "Interstitium Labs  •  Original visual guide")
    c.drawRightString(PAGE_W - 72, 48, f"Page {page_no}")
    c.setPageTransition(effectname="Dissolve", duration=0.4)


def box(c, x, y, w, h, fill, label, sublabel=None, font_size=11):
    c.setFillColor(fill); c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
    c.setStrokeColor(INK); c.setLineWidth(1.2); c.roundRect(x, y, w, h, 8, fill=0, stroke=1)
    c.setFillColor(INK); c.setFont(TITLE_FONT, font_size)
    c.drawCentredString(x + w/2, y + h/2 + (6 if sublabel else -4), label)
    if sublabel:
        c.setFillColor(MUTED); c.setFont(BODY_FONT, font_size - 3)
        c.drawCentredString(x + w/2, y + h/2 - 10, sublabel)


def arrow(c, x1, y1, x2, y2, color=ACCENT, width=2, label=None):
    c.setStrokeColor(color); c.setLineWidth(width)
    c.setFillColor(color)
    c.line(x1, y1, x2, y2)
    # arrowhead
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    ah = 10
    c.line(x2, y2, x2 - ah*math.cos(ang - 0.4), y2 - ah*math.sin(ang - 0.4))
    c.line(x2, y2, x2 - ah*math.cos(ang + 0.4), y2 - ah*math.sin(ang + 0.4))
    if label:
        c.setFont(BODY_FONT, 9); c.setFillColor(color)
        c.drawCentredString((x1+x2)/2, (y1+y2)/2 + 8, label)


def note(c, x, y, w, text, fill=BOX_ORANGE):
    """Annotation callout."""
    c.setFillColor(fill); c.roundRect(x, y, w, 44, 6, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(BODY_FONT, 9.5)
    p = Paragraph(text, styles["Normal"])
    # simple manual wrap
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if c.stringWidth(cur + " " + wd, BODY_FONT, 9.5) > w - 16:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    lines.append(cur)
    ty = y + 32
    for ln in lines[:3]:
        c.drawString(x + 8, ty, ln); ty -= 12


def bullet_list(c, x, y, items, font_size=11, gap=20):
    c.setFillColor(INK)
    for it in items:
        c.setFillColor(ACCENT); c.circle(x + 4, y - 4, 3.5, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(BODY_FONT, font_size)
        # wrap
        words, lines, cur = it.split(), [], ""
        for wd in words:
            if c.stringWidth(cur + " " + wd, BODY_FONT, font_size) > PAGE_W - x - 90:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        c.drawString(x + 16, y - 4, lines[0])
        y -= gap
        for ln in lines[1:]:
            c.drawString(x + 16, y - 4, ln); y -= gap - 6
    return y


def summary_page(c, title, takeaways, page_no):
    y = section_header(c, "✓", "✓", "Key Takeaways")
    c.setFillColor(INK); c.setFont(TITLE_FONT, 15)
    c.drawString(72, y, title)
    y -= 36
    y = bullet_list(c, 72, y, takeaways, font_size=11.5, gap=28)
    # related box
    c.setFillColor(BOX_TEAL); c.roundRect(72, 110, PAGE_W - 144, 70, 8, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(TITLE_FONT, 11)
    c.drawString(88, 160, "Keep exploring")
    c.setFillColor(MUTED); c.setFont(BODY_FONT, 10)
    c.drawString(88, 144, "Pair this guide with the matching video walkthroughs")
    c.drawString(88, 130, "and hands-on labs at interstitiumlabs.dev")
    footer(c, page_no)
    c.showPage()
