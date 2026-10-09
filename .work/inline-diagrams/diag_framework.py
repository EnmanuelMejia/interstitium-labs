#!/usr/bin/env python3
"""
Inline SVG Diagram Framework — rich, dark-themed technical diagrams
matching the DDL/DML module screenshot standard.

Style: dark background (#0d1117-ish), color-coded elements,
clean monospace typography, figure numbers + captions.

Usage:
    from diag_framework import Diagram
    d = Diagram(fig_num="M1", caption="CREATE TABLE is a contract...")
    d.table_schema("employees", [("id","INTEGER","PK"),("name","TEXT","NOT NULL")])
    svg = d.render_figure()
"""
import html

# Palette — matches screenshot dark theme
BG = "#0d1117"
SURFACE = "#161b22"
SURFACE2 = "#1c2128"
BORDER = "#30363d"
ACCENT = "#58a6ff"      # blue — structural elements
GREEN = "#3fb950"       # success / guarantees
ORANGE = "#d29922"      # warnings / constraints
RED = "#f85149"         # errors / critical
PURPLE = "#a371f7"      # special
CYAN = "#39c5cf"        # data flow
INK = "#f0f6fc"         # primary text
MUTED = "#8b949e"       # secondary text
MONO = "ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,monospace"

_fig_counter = [0]

def esc(t):
    return html.escape(str(t), quote=True)

class Diagram:
    def __init__(self, width=720, fig_num=None, caption="", alt=""):
        self.w = width
        self.h = 0
        self.elements = []
        self.fig_num = fig_num
        self.caption = caption
        self.alt = alt or caption
        self._y = 0

    # ---- primitives ----
    def _rect(self, x, y, w, h, fill=SURFACE, stroke=BORDER, rx=8, opacity=1.0):
        self.elements.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5" opacity="{opacity}"/>')

    def _text(self, x, y, s, size=13, fill=INK, anchor="middle", weight=400,
              family=MONO, opacity=1.0):
        self.elements.append(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" opacity="{opacity}">{esc(s)}</text>')

    def _line(self, x1, y1, x2, y2, stroke=MUTED, width=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.elements.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{width}"{d}/>')

    def _arrow(self, x1, y1, x2, y2, stroke=ACCENT, width=2, label=""):
        self.elements.append(
            f'<defs><marker id="ah{len(self.elements)}" markerWidth="8" markerHeight="8" '
            f'refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{stroke}"/></marker></defs>'
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{width}" marker-end="url(#ah{len(self.elements)})"/>')
        if label:
            self._text((x1+x2)/2, (y1+y2)/2 - 6, label, size=11, fill=MUTED)

    def _box(self, x, y, w, h, title, subtitle="", accent=ACCENT):
        self._rect(x, y, w, h, fill=SURFACE, stroke=accent)
        self._text(x + w/2, y + 24, title, size=14, weight=700, fill=INK)
        if subtitle:
            self._text(x + w/2, y + 44, subtitle, size=11, fill=MUTED)

    # ---- composite: database table schema (screenshot style) ----
    def table_schema(self, table_name, columns, x=20, y=10, col_w=300):
        """columns: list of (name, type, constraint) — constraint '' if none."""
        row_h = 26
        header_h = 34
        n = len(columns)
        h = header_h + n * row_h + 8
        w = col_w
        self._rect(x, y, w, h, fill=SURFACE, stroke=ACCENT, rx=10)
        self._text(x + w/2, y + 22, table_name, size=14, weight=700, fill=INK)
        for i, (cname, ctype, con) in enumerate(columns):
            ry = y + header_h + i * row_h
            if i > 0:
                self._line(x + 12, ry, x + w - 12, ry, stroke=BORDER, width=1)
            self._text(x + 18, ry + 18, cname, size=12, fill=INK, anchor="start")
            self._text(x + w/2, ry + 18, ctype, size=11, fill=MUTED)
            if con:
                cc = ORANGE if con in ("PK", "FK", "NOT NULL", "UNIQUE") else GREEN
                if con == "PK":
                    cc = ACCENT
                self._text(x + w - 14, ry + 18, con, size=11, fill=cc,
                           anchor="end", weight=600)
        self._y = max(self._y, y + h + 16)
        return h

    # ---- composite: concept box (screenshot right panel style) ----
    def concept_box(self, title, lines, x=20, y=10, w=300, accent=GREEN):
        row_h = 24
        h = 40 + len(lines) * row_h + 12
        self._rect(x, y, w, h, fill=SURFACE, stroke=BORDER, rx=10)
        self._text(x + w/2, y + 24, title, size=12, weight=700, fill=INK)
        for i, ln in enumerate(lines):
            self._text(x + w/2, y + 48 + i * row_h, ln, size=11, fill=MUTED)
        self._y = max(self._y, y + h + 16)
        return h

    # ---- composite: horizontal flow ----
    def flow(self, steps, y=60, box_w=130, box_h=64, gap=34, accent=ACCENT):
        """steps: list of (label, sublabel)."""
        x = 20
        total_w = len(steps) * box_w + (len(steps)-1) * gap
        x0 = (self.w - total_w) / 2
        for i, (label, sub) in enumerate(steps):
            bx = x0 + i * (box_w + gap)
            self._box(bx, y, box_w, box_h, label, sub, accent)
            if i < len(steps) - 1:
                self._arrow(bx + box_w, y + box_h/2, bx + box_w + gap, y + box_h/2)
        self._y = max(self._y, y + box_h + 16)

    # ---- composite: layered stack ----
    def layers(self, layers, x=120, y=20, w=480, layer_h=52, accent=ACCENT):
        """layers: list of (label, sublabel) top to bottom."""
        for i, (label, sub) in enumerate(layers):
            ly = y + i * (layer_h + 10)
            shade = SURFACE if i % 2 == 0 else SURFACE2
            self._rect(x, ly, w, layer_h, fill=shade, stroke=accent if i == 0 else BORDER, rx=8)
            self._text(x + 16, ly + 22, label, size=13, weight=600, fill=INK, anchor="start")
            if sub:
                self._text(x + 16, ly + 40, sub, size=11, fill=MUTED, anchor="start")
        self._y = max(self._y, y + len(layers) * (layer_h + 10) + 8)

    # ---- composite: comparison (two columns) ----
    def compare(self, left_title, left_items, right_title, right_items,
                left_accent=RED, right_accent=GREEN, y=20):
        w = (self.w - 60) / 2
        for col, (title, items, accent) in enumerate(
                [(left_title, left_items, left_accent),
                 (right_title, right_items, right_accent)]):
            x = 20 + col * (w + 20)
            h = 40 + len(items) * 26 + 10
            self._rect(x, y, w, h, fill=SURFACE, stroke=accent, rx=10)
            self._text(x + w/2, y + 24, title, size=13, weight=700, fill=accent)
            for i, it in enumerate(items):
                self._text(x + 16, y + 52 + i * 26, "• " + it, size=12,
                           fill=INK, anchor="start")
            self._y = max(self._y, y + h + 16)

    # ---- animation: CSS keyframes block (call once per diagram) ----
    def animate(self, stagger_step=0.35):
        """Inject animation CSS: staggered node entrances, flowing dashes,
        pulsing accents. Call after adding elements, before render."""
        css = """
<style>
.il-anim .a-node{opacity:0;animation:il-pop .55s cubic-bezier(.2,.9,.3,1.2) forwards}
.il-anim .a-flow{stroke-dasharray:8 6;animation:il-dash 1.1s linear infinite}
.il-anim .a-pulse{animation:il-pulse 2.2s ease-in-out infinite}
.il-anim .a-glow{filter:drop-shadow(0 0 6px currentColor)}
@keyframes il-pop{from{opacity:0;transform:scale(.82)}to{opacity:1;transform:scale(1)}}
@keyframes il-dash{to{stroke-dashoffset:-28}}
@keyframes il-pulse{0%,100%{opacity:1}50%{opacity:.45}}
@media (prefers-reduced-motion:reduce){.il-anim .a-node,.il-anim .a-flow,.il-anim .a-pulse{animation:none!important;opacity:1!important}}
</style>"""
        # wrap: add il-anim class hooks by post-processing element strings
        animated = []
        n = 0
        for el in self.elements:
            if el.startswith('<rect') or el.startswith('<text') or el.startswith('<line'):
                # stagger entrance on shapes (skip tiny divider lines)
                if 'stroke-dasharray' in el or (el.startswith('<line') and 'marker-end' in el):
                    el = el.replace('stroke-width=', 'class="a-flow" stroke-width=', 1)
                elif el.startswith('<line'):
                    pass  # plain divider, no animation
                else:
                    el = el.replace('/>', f' class="a-node" style="animation-delay:{n*stagger_step:.2f}s"/>', 1)
                    el = el.replace('</text>', '</text>', 1)
                    if el.startswith('<text'):
                        el = el.replace('>', f' class="a-node" style="animation-delay:{n*stagger_step:.2f}s">', 1)
                    n += 1
            animated.append(el)
        self.elements = animated
        self._anim_css = css

    # ---- render ----
    def render_svg(self):
        h = int(self._y + 10) if self._y else 120
        inner = "\n".join(self.elements)
        css = getattr(self, '_anim_css', '')
        return (
            f'<svg viewBox="0 0 {self.w} {h}" width="100%" role="img" '
            f'aria-label="{esc(self.alt)}" class="il-anim" '
            f'style="display:block;max-width:{self.w}px;margin:0 auto;background:{BG};border-radius:10px">'
            f'<rect width="{self.w}" height="{h}" fill="{BG}" rx="10"/>'
            f'{css}{inner}</svg>')

    def render_figure(self):
        fig_label = f"Fig. {self.fig_num} — " if self.fig_num else ""
        return (
            f'<figure class="il-diagram" style="margin:1.2em 0">'
            f'{self.render_svg()}'
            f'<figcaption style="margin-top:.6em;color:{MUTED};font-size:.85em;text-align:center">'
            f'<strong>{esc(fig_label)}</strong>{esc(self.caption)}</figcaption>'
            f'</figure>')
