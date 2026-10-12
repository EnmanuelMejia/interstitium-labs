#!/usr/bin/env python3
"""W1 inline-diagram driver: builds ANIMATED diagrams via diag_framework and
embeds them at the end of the most topically-relevant note body per module.

Every diagram gets d.animate() before render_figure() (user order 2026-10-09:
all media animated, prefers-reduced-motion fallback included).

Writes preserve each file's original JSON formatting (indent + ascii mode),
via temp-file + json.load validation + os.replace.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_framework import (  # noqa: F401
    Diagram, SURFACE, SURFACE2, BORDER, ACCENT, GREEN, ORANGE, RED,
    PURPLE, CYAN, INK, MUTED,
)


def truth_table(d, title, headers, rows, x=20, y=10, cell_w=130):
    """Truth-table grid built from framework primitives (animate() picks it up)."""
    row_h, header_h = 26, 34
    w = len(headers) * cell_w
    h = header_h + len(rows) * row_h + 10
    d._rect(x, y, w, h, fill=SURFACE, stroke=ACCENT, rx=10)
    d._text(x + w / 2, y + 22, title, size=13, weight=700, fill=INK)
    for j, hd in enumerate(headers):
        cx = x + j * cell_w
        d._text(cx + cell_w / 2, y + header_h + 12, hd, size=12,
                weight=700, fill=ACCENT)
        if j > 0:
            d._line(cx, y + header_h - 8, cx, y + h - 8, stroke=BORDER, width=1)
    for i, row in enumerate(rows):
        ry = y + header_h + i * row_h
        if i > 0:
            d._line(x + 12, ry, x + w - 12, ry, stroke=BORDER, width=1)
        for j, val in enumerate(row):
            cx = x + j * cell_w
            if j == len(row) - 1 and val in ("T", "F"):
                fill = GREEN if val == "T" else RED
            else:
                fill = INK
            d._text(cx + cell_w / 2, ry + 18, val, size=12, fill=fill)
    d._y = max(d._y, y + h + 16)


KINDS = {
    "concept_box": lambda d, **k: d.concept_box(**k),
    "flow": lambda d, **k: d.flow(**k),
    "layers": lambda d, **k: d.layers(**k),
    "compare": lambda d, **k: d.compare(**k),
    "truth_table": truth_table,
}


def apply(path, indent, ensure_ascii, specs):
    """specs: list of (module_id, note_title_substr, fig_num, caption, alt,
    kind, kwargs). Returns (counts dict, animated_count)."""
    doc = json.load(open(path, encoding="utf-8"))
    counts = {}
    animated = 0
    for (mod_id, note_key, fig_num, caption, alt, kind, kw) in specs:
        dg = Diagram(fig_num=fig_num, caption=caption, alt=alt)
        KINDS[kind](dg, **kw)
        dg.animate()  # user order: every diagram animates
        assert getattr(dg, "_anim_css", ""), "animate() did not inject CSS"
        animated += 1
        fig = dg.render_figure()
        assert "il-anim" in fig, "rendered figure missing animation hooks"
        mod = next(m for m in doc["modules"] if m["id"] == mod_id)
        notes = mod["notes"]
        note = next(
            (n for n in notes if note_key.lower() in (n.get("title") or "").lower()),
            notes[-1],
        )
        body = note.get("body") or ""
        note["body"] = body + "\n\n" + fig
        counts[mod_id] = counts.get(mod_id, 0) + 1
    tmp = path + ".w1tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc, indent=indent, ensure_ascii=ensure_ascii))
    json.load(open(tmp, encoding="utf-8"))  # validate before replace
    os.replace(tmp, path)
    return counts, animated
