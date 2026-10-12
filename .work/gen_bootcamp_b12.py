"""Bootcamp video Phase 2, Batch B12: 8 bootcamps x 3 videos = 24 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b5.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.

Batch B12 bootcamps (Final):
  aleks-ops-math, math-tech, android-interview, ios-interview, tl-interview, threatlocker-assessment-prep, vendor-map, zerotrust
"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_batch1 as G
from gen_batch1 import (
    font, lerp, clamp, ease, wrap_text, txt, dot_grid, glow_box,
    panel, arrow, caption_bar, preview_tag, title_card, end_card,
    bbg_title, code_panel, write_vtt, write_narration, encode_video,
    STYLE_BG, ACCENTS,
    TEAL, YELLOW, CYAN, MAGENTA, ORANGE, BLUE, GREEN, RED, GOLD, CREAM, WHITE, DIM,
    F_SANS, F_BOLD, F_MONO, F_MONOB, F_SERIF, F_SERIFB,
)

W, H, FPS, DUR, NFR = G.W, G.H, G.FPS, G.DUR, G.NFR
OUT = "/home/hatch/workspace/apex-audit/docs/assets/videos"
SMOKE = os.environ.get("SMOKE") == "1"

def bar(dr, x, y, w, h, frac, fill, label=None, val=None):
    dr.rectangle([x, y, x + w, y + h], fill=(18, 24, 40), outline=DIM, width=2)
    fw = int(w * clamp(frac))
    if fw > 4:
        dr.rectangle([x + 2, y + 2, x + fw - 2, y + h - 2], fill=fill)
    if label:
        txt(dr, (x, y - 8), label, font(F_SANS, 22), DIM, anchor="lb")
    if val:
        txt(dr, (x + w, y + h + 8), val, font(F_MONOB, 24), fill, anchor="rt")

# ============================================================
# aleks-ops-math (3b1b x1 + primer x1 + story x1)
def scene_alx_topics(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'ALEKS Mastery: The Pie Fills', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'mastery is measured, not felt', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'mastery = assessed, not watched', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('topics', 380, '%d'), ('mastered', 342, '%d'), ('retention', 90, '%d%%')]
    _n = len(_stats)
    _w = 1000 // _n
    for _i, (_lb, _tg, _fm) in enumerate(_stats):
        _x = 140 + _i * _w + _w // 2
        _v = _tg * clamp((t - 6 - _i * 2.5) / 6)
        txt(dr, (_x, 320), _fm % int(_v), font(F_MONOB, 50), TEAL, anchor="mm")
        _lines = wrap_text(_lb, font(F_SANS, 22), _w - 24, dr)
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x, 390 + _ln * 30), _line, font(F_SANS, 22), DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 540), 'mastery is measured, not felt', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the pie does not lie — earn every slice', font(F_SANS, 24), DIM, anchor="mm")
def scene_alx_drill(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'The Drill Grid: Reps Until Automatic', CYAN)
    _rows, _cols = 5, 8
    _tot = _rows * _cols
    _k = int(clamp((t - 5) / 13) * _tot)
    _cw = min(96, 880 // _cols)
    _chh = min(62, 300 // _rows)
    _x0 = (W - _cols * _cw) // 2
    _y0 = 170
    for _i in range(_rows):
        for _j in range(_cols):
            _on = (_i * _cols + _j) < _k
            _x = _x0 + _j * _cw
            _y = _y0 + _i * _chh
            dr.rectangle([_x + 3, _y + 3, _x + _cw - 3, _y + _chh - 3],
                         fill=CYAN if _on else (20, 28, 48))
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — drill reps converting to reflex' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'automaticity is the goal', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'speed follows accuracy — never the reverse', font(F_SANS, 24), DIM, anchor="mm")
def scene_alx_review(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Review Week: The Consolidation', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the test is the learning', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('revisit: shaky slices', 5), ('retest: timed pressure', 9), ('sleep: consolidation', 13), ('assess: the honest pie', 17), ('mastered: the knowledge stays', 21)]
    _n = len(_ev)
    _x = 500
    _top = (H - (_n - 1) * 76) // 2 + 44
    dr.line([_x, _top - 20, _x, _top + (_n - 1) * 76 + 20], fill=DIM, width=4)
    for _i, (_lb, _ts) in enumerate(_ev):
        _y = _top + _i * 76
        _done = t > _ts
        dr.ellipse([_x - 14, _y - 14, _x + 14, _y + 14],
                   fill=GOLD if _done else (40, 40, 60), outline=GOLD, width=2)
        txt(dr, (_x + 36, _y), _lb, font(F_SANS, 24), CREAM if _done else DIM, anchor="lm")
        if _done:
            txt(dr, (_x - 36, _y), "t+%ds" % int(_ts), font(F_MONO, 19), GOLD, anchor="rm")
    if t > 19:
        txt(dr, (W // 2, 624), 'the test is the learning', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'retrieval strengthens memory — rereading does not', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# math-tech (bbg x1 + 3b1b x2)
def scene_mt_calculus(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Derivatives: The Rate of Change', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'the slope is the story', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'd/dx xⁿ = n·xⁿ⁻¹', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('rules', 7, '%d'), ('applied', 120, '%d'), ('mastered', 1, '%d')]
    _n = len(_stats)
    _w = 1000 // _n
    for _i, (_lb, _tg, _fm) in enumerate(_stats):
        _x = 140 + _i * _w + _w // 2
        _v = _tg * clamp((t - 6 - _i * 2.5) / 6)
        txt(dr, (_x, 320), _fm % int(_v), font(F_MONOB, 50), TEAL, anchor="mm")
        _lines = wrap_text(_lb, font(F_SANS, 22), _w - 24, dr)
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x, 390 + _ln * 30), _line, font(F_SANS, 22), DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 540), 'the slope is the story', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'differentiate to see how fast things change', font(F_SANS, 24), DIM, anchor="mm")
def scene_mt_linear(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Linear Algebra: The Data Pipeline', CYAN)
    _boxes = ('vectors', 'matrices', 'eigen', 'models')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'vectors in, transformations out', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the matrix is the machine — learn to read it', font(F_SANS, 24), DIM, anchor="mm")
def scene_mt_stats(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Distributions: The Shapes of Chance', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'know the shape before the test', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('normal', 1.0, '68-95-99.7', GREEN), ('binomial', 0.7, 'n trials', TEAL), ('poisson', 0.5, 'λ rate', YELLOW), ('uniform', 0.3, 'flat', ORANGE)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'know the shape before the test', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'the wrong distribution is a confident wrong answer', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# android-interview (bbg x2 + fireship x1)
def scene_ai_activity(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Activity Lifecycle: The Callbacks', CYAN)
    _boxes = ('create', 'start', 'resume', 'pause', 'destroy')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'the OS owns your activity', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'save state in onPause — the OS owes you nothing', font(F_SANS, 24), DIM, anchor="mm")
def scene_ai_compose(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Compose in 100 Seconds', MAGENTA)
    _lns = [('@Composable', YELLOW), ('fun Cart(items: List<Item>) {', (200, 200, 255)), ('  var count by remember { mutableStateOf(0) }', GREEN), ('  Button(onClick = { count++ }) {', (200, 200, 255)), ('    Text("items: $count")', (200, 200, 255)), ('  }', (200, 200, 255)), ('}', (200, 200, 255))]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'Screen.kt', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'UI as functions of state', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'remember the state — or lose the UI', font(F_SANS, 24), DIM, anchor="mm")
def scene_ai_mvvm(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'MVVM: The Layers', CYAN)
    _layers = ('view', 'viewmodel', 'repository', 'data sources')
    _n = len(_layers)
    _lit = int(clamp((t - 5) / 12) * _n)
    _y0 = (H - _n * 68) // 2 + 60
    for _i, _L in enumerate(_layers):
        _y = _y0 + _i * 68
        _on = _i < _lit
        dr.rectangle([300, _y, 980, _y + 52], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        txt(dr, (262, _y + 26), "L%d" % (_n - _i), font(F_MONO, 20), DIM, anchor="rm")
        txt(dr, (640, _y + 26), _L, font(F_BOLD, 23), CYAN if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 612), 'the view observes, never commands', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), "rotation survival is the ViewModel's whole job", font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# ios-interview (bbg x1 + fireship x1 + 3b1b x1)
def scene_ios_swiftui(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'SwiftUI in 100 Seconds', MAGENTA)
    _lns = [('struct ContentView: View {', (200, 200, 255)), ('  @State private var count = 0', GREEN), ('  var body: some View {', YELLOW), ('    Button("taps: \\(count)") { count += 1 }', (200, 200, 255)), ('  }', (200, 200, 255)), ('}', (200, 200, 255)), ('# state changes → view redraws', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'ContentView.swift', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'declare the UI, let the diff do the work', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'state drives — the framework diffs', font(F_SANS, 24), DIM, anchor="mm")
def scene_ios_lifecycle(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'ViewController Lifecycle', CYAN)
    _boxes = ('didLoad', 'willAppear', 'didAppear', 'willDisappear')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'load once, appear often', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'setup in didLoad — refresh in willAppear', font(F_SANS, 24), DIM, anchor="mm")
def scene_ios_arc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'ARC: Counting References', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'the compiler inserts the retains', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'strong × weak × unowned', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('retains', 0, '%d manual'), ('cycles', 1, '%d found'), ('leaks', 0, '%d')]
    _n = len(_stats)
    _w = 1000 // _n
    for _i, (_lb, _tg, _fm) in enumerate(_stats):
        _x = 140 + _i * _w + _w // 2
        _v = _tg * clamp((t - 6 - _i * 2.5) / 6)
        txt(dr, (_x, 320), _fm % int(_v), font(F_MONOB, 50), TEAL, anchor="mm")
        _lines = wrap_text(_lb, font(F_SANS, 22), _w - 24, dr)
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x, 390 + _ln * 30), _line, font(F_SANS, 22), DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 540), 'the compiler inserts the retains', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'you manage the graph — break the cycles', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# tl-interview (bbg x1 + fireship x1 + story x1)
def scene_tli_triage(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Triage: The ThreatLocker Way', CYAN)
    _boxes = ('deny', 'queue', 'verify', 'allowlist')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'default deny, then decide', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the allowlist is a list of decisions — not accidents', font(F_SANS, 24), DIM, anchor="mm")
def scene_tli_powershell(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'PowerShell Triage in 100 Seconds', MAGENTA)
    _lns = [('Get-Process | Sort CPU -Desc | Select -First 5', YELLOW), ('Get-NetTCPConnection -State Listen', (200, 200, 255)), ("Get-Service | ? {$_.StartType -eq 'Auto'}", GREEN), ('# processes, listeners, persistence', (200, 200, 255)), ('# the triage trinity', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'triage.ps1', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'the console is the fastest incident tool', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'know the three cmdlets cold — the interview will ask', font(F_SANS, 24), DIM, anchor="mm")
def scene_tli_scenario(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Interview Scenario: The Live Round', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'think aloud — they hire the reasoning', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('scenario lands: blocked app', 5), ('think aloud: triage narrated', 9), ('contain: the safe move', 13), ('verify: legitimate or not', 17), ('document: decision + reasons', 21)]
    _n = len(_ev)
    _x = 500
    _top = (H - (_n - 1) * 76) // 2 + 44
    dr.line([_x, _top - 20, _x, _top + (_n - 1) * 76 + 20], fill=DIM, width=4)
    for _i, (_lb, _ts) in enumerate(_ev):
        _y = _top + _i * 76
        _done = t > _ts
        dr.ellipse([_x - 14, _y - 14, _x + 14, _y + 14],
                   fill=GOLD if _done else (40, 40, 60), outline=GOLD, width=2)
        txt(dr, (_x + 36, _y), _lb, font(F_SANS, 24), CREAM if _done else DIM, anchor="lm")
        if _done:
            txt(dr, (_x - 36, _y), "t+%ds" % int(_ts), font(F_MONO, 19), GOLD, anchor="rm")
    if t > 19:
        txt(dr, (W // 2, 624), 'think aloud — they hire the reasoning', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'narrate every step — silence looks like guessing', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# threatlocker-assessment-prep (bbg x1 + primer x1 + story x1)
def scene_tlap_allowlist(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Allowlisting: The Layers', CYAN)
    _layers = ('applications', 'scripts', 'libraries', 'default deny')
    _n = len(_layers)
    _lit = int(clamp((t - 5) / 12) * _n)
    _y0 = (H - _n * 68) // 2 + 60
    for _i, _L in enumerate(_layers):
        _y = _y0 + _i * 68
        _on = _i < _lit
        dr.rectangle([300, _y, 980, _y + 52], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        txt(dr, (262, _y + 26), "L%d" % (_n - _i), font(F_MONO, 20), DIM, anchor="rm")
        txt(dr, (640, _y + 26), _L, font(F_BOLD, 23), CYAN if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 612), 'deny everything, permit deliberately', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the list is the security — curate it like it matters', font(F_SANS, 24), DIM, anchor="mm")
def scene_tlap_ringfence(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Ringfencing: The Containment', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('launch', 'fence up', 'attempt', 'blocked', 'logged')
    _m = len(_pts)
    _prog = clamp((t - 5) / 15)
    _pos = _prog * (_m - 1)
    _i = int(_pos)
    if _i >= _m - 1:
        _i = _m - 2
        _fr = 1.0
    else:
        _fr = _pos - _i
    for _k in range(_m - 1):
        _done = _pos > _k
        dr.line([_pts[_k][0], _pts[_k][1], _pts[_k + 1][0], _pts[_k + 1][1]],
                fill=CYAN if _done else DIM, width=4)
    for _k in range(_m):
        _px, _py = _pts[_k]
        _on = _pos >= _k - 0.001
        dr.ellipse([_px - 26, _py - 26, _px + 26, _py + 26],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_px, _py), str(_k + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_px, _py + 52), _labels[_k], font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    _tx = lerp(_pts[_i][0], _pts[_i + 1][0], _fr)
    _ty = lerp(_pts[_i][1], _pts[_i + 1][1], _fr)
    dr.ellipse([_tx - 13, _ty - 13, _tx + 13, _ty + 13], fill=YELLOW, outline=WHITE, width=2)
    if t > 19:
        txt(dr, (W // 2, 540), 'the app can run — but not roam', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'containment beats detection — the blast never starts', font(F_SANS, 24), DIM, anchor="mm")
def scene_tlap_socday(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'A Day in the ThreatLocker SOC', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the queue is the job', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('queue: overnight, risk-sorted', 5), ('triage: the obvious first', 9), ('escalate: ambiguous, with context', 13), ('verify: the hard ones', 17), ('log: the next shift thanks you', 21)]
    _n = len(_ev)
    _x = 500
    _top = (H - (_n - 1) * 76) // 2 + 44
    dr.line([_x, _top - 20, _x, _top + (_n - 1) * 76 + 20], fill=DIM, width=4)
    for _i, (_lb, _ts) in enumerate(_ev):
        _y = _top + _i * 76
        _done = t > _ts
        dr.ellipse([_x - 14, _y - 14, _x + 14, _y + 14],
                   fill=GOLD if _done else (40, 40, 60), outline=GOLD, width=2)
        txt(dr, (_x + 36, _y), _lb, font(F_SANS, 24), CREAM if _done else DIM, anchor="lm")
        if _done:
            txt(dr, (_x - 36, _y), "t+%ds" % int(_ts), font(F_MONO, 19), GOLD, anchor="rm")
    if t > 19:
        txt(dr, (W // 2, 624), 'the queue is the job', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'rhythm beats heroics — the log is the handoff', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# vendor-map (bbg x1 + 3b1b x1 + story x1)
def scene_vm_landscape(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Vendor Landscape', CYAN)
    _nodes = [('you', 640, 520), ('leader-a', 280, 280), ('leader-b', 640, 200), ('challenger', 1000, 280), ('niche', 1000, 480)]
    _edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    _order = (0, 1, 2, 3, 4)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), 'map the market before you buy', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'the RFP is not research — the map is', font(F_SANS, 24), DIM, anchor="mm")
def scene_vm_scorecard(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Scorecard: Decide by Numbers', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'weight what matters', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('security', 0.95, '38/40', GREEN), ('fit', 0.8, '24/30', TEAL), ('support', 0.7, '14/20', YELLOW), ('price', 0.5, '5/10', ORANGE)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'weight what matters', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'evidence required — no vibes on the scorecard', font(F_SANS, 24), DIM, anchor="mm")
def scene_vm_procure(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Procurement: The Gauntlet', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the process protects the buyer', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('requirements: written first', 5), ('RFP: the bake-off', 9), ('security review: non-negotiable', 13), ('negotiate: the terms', 17), ('sign: the relationship begins', 21)]
    _n = len(_ev)
    _x = 500
    _top = (H - (_n - 1) * 76) // 2 + 44
    dr.line([_x, _top - 20, _x, _top + (_n - 1) * 76 + 20], fill=DIM, width=4)
    for _i, (_lb, _ts) in enumerate(_ev):
        _y = _top + _i * 76
        _done = t > _ts
        dr.ellipse([_x - 14, _y - 14, _x + 14, _y + 14],
                   fill=GOLD if _done else (40, 40, 60), outline=GOLD, width=2)
        txt(dr, (_x + 36, _y), _lb, font(F_SANS, 24), CREAM if _done else DIM, anchor="lm")
        if _done:
            txt(dr, (_x - 36, _y), "t+%ds" % int(_ts), font(F_MONO, 19), GOLD, anchor="rm")
    if t > 19:
        txt(dr, (W // 2, 624), 'the process protects the buyer', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the terms are the product — read them', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# zerotrust (bbg x2 + primer x1)
def scene_zt_pillars(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Zero Trust: The Seven Pillars', CYAN)
    _layers = ('visibility', 'data', 'apps', 'networks', 'devices', 'identity')
    _n = len(_layers)
    _lit = int(clamp((t - 5) / 12) * _n)
    _y0 = (H - _n * 68) // 2 + 60
    for _i, _L in enumerate(_layers):
        _y = _y0 + _i * 68
        _on = _i < _lit
        dr.rectangle([300, _y, 980, _y + 52], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        txt(dr, (262, _y + 26), "L%d" % (_n - _i), font(F_MONO, 20), DIM, anchor="rm")
        txt(dr, (640, _y + 26), _L, font(F_BOLD, 23), CYAN if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 612), 'never trust, always verify', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the network location is not an identity', font(F_SANS, 24), DIM, anchor="mm")
def scene_zt_microseg(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Microsegmentation: Small Blast Radii', CYAN)
    _nodes = [('web', 280, 280), ('app', 640, 280), ('db', 1000, 280), ('policy', 640, 520)]
    _edges = [(0, 1), (1, 2), (3, 0), (3, 1), (3, 2)]
    _order = (0, 1, 2, 3)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), 'the breach stays in its room', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'flat networks are breach highways — segment them', font(F_SANS, 24), DIM, anchor="mm")
def scene_zt_verify(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Verify Every Request', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('auth', 'device', 'risk', 'authorize', 'access')
    _m = len(_pts)
    _prog = clamp((t - 5) / 15)
    _pos = _prog * (_m - 1)
    _i = int(_pos)
    if _i >= _m - 1:
        _i = _m - 2
        _fr = 1.0
    else:
        _fr = _pos - _i
    for _k in range(_m - 1):
        _done = _pos > _k
        dr.line([_pts[_k][0], _pts[_k][1], _pts[_k + 1][0], _pts[_k + 1][1]],
                fill=CYAN if _done else DIM, width=4)
    for _k in range(_m):
        _px, _py = _pts[_k]
        _on = _pos >= _k - 0.001
        dr.ellipse([_px - 26, _py - 26, _px + 26, _py + 26],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_px, _py), str(_k + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_px, _py + 52), _labels[_k], font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    _tx = lerp(_pts[_i][0], _pts[_i + 1][0], _fr)
    _ty = lerp(_pts[_i][1], _pts[_i + 1][1], _fr)
    dr.ellipse([_tx - 13, _ty - 13, _tx + 13, _ty + 13], fill=YELLOW, outline=WHITE, width=2)
    if t > 19:
        txt(dr, (W // 2, 540), 'trust is per-request, not per-network', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the VPN proves nothing — verify anyway', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'alx': 'aleks-ops-math',
    'mt': 'math-tech',
    'ai': 'android-interview',
    'ios': 'ios-interview',
    'tli': 'tl-interview',
    'tlap': 'threatlocker-assessment-prep',
    'vm': 'vendor-map',
    'zt': 'zerotrust',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'alx': 'ALEKS · Ops Math',
    'mt': 'MATH TECH · Technical Math',
    'ai': 'ANDROID · Interview Prep',
    'ios': 'IOS · Interview Prep',
    'tli': 'TL · ThreatLocker Interview',
    'tlap': 'TL ASSESS · Assessment Prep',
    'vm': 'VENDOR MAP · Market Landscape',
    'zt': 'ZERO TRUST · Never Trust',
}
VIDEOS = [
 # --- aleks-ops-math
 V(BOOTCAMP_K['alx'], 'alx', 'alx-topics', 'ALEKS Mastery: The Pie Fills',
   'mastery is measured, not felt', '3b1b', scene_alx_topics,
   'ALEKS: the pie chart of topics fills as you master them — each slice earned by assessment, not by watching. Mastery is measured, not felt — the pie does not lie.',
   [(4,10,'The pie: every topic, one slice'),
    (10,16,'Assessment earns slices — practice defends them'),
    (16,22,'The system retests — forgetting is priced in'),
    (22,26,'100%: the pie is full — the knowledge is yours')]),
 V(BOOTCAMP_K['alx'], 'alx', 'alx-drill', 'The Drill Grid: Reps Until Automatic',
   'automaticity is the goal', 'primer', scene_alx_drill,
   'Drills: the same skill from ten angles until it is automatic — automaticity is the goal. The grid fills as reps convert effort into reflex.',
   [(4,10,'One skill, ten angles — varied practice'),
    (10,16,'Spaced reps: the forgetting curve, defeated'),
    (16,22,'Speed follows accuracy — never the reverse'),
    (22,26,'Automatic: the skill runs without you')]),
 V(BOOTCAMP_K['alx'], 'alx', 'alx-review', 'Review Week: The Consolidation',
   'the test is the learning', 'story', scene_alx_review,
   'Review week: revisit every shaky slice, retest under time, sleep on it, then the assessment. The test is the learning — retrieval strengthens memory.',
   [(4,10,'Revisit: the shaky slices first'),
    (10,16,'Retest: timed — pressure is part of the skill'),
    (16,22,'Sleep: consolidation happens overnight'),
    (22,26,'Assess: the pie, full and honest')]),
 # --- math-tech
 V(BOOTCAMP_K['mt'], 'mt', 'mt-calculus', 'Derivatives: The Rate of Change',
   'the slope is the story', '3b1b', scene_mt_calculus,
   'Derivatives: the slope of the curve at a point — velocity from position, marginal cost from total cost. The slope is the story; the derivative tells it instantly.',
   [(4,10,'Slope at a point: the tangent line'),
    (10,16,"Velocity: position's derivative — motion decoded"),
    (16,22,"Marginal: cost's derivative — the next unit's price"),
    (22,26,'Chain rule: the composition — derivatives of derivatives')]),
 V(BOOTCAMP_K['mt'], 'mt', 'mt-linear', 'Linear Algebra: The Data Pipeline',
   'vectors in, transformations out', 'bbg', scene_mt_linear,
   'Linear algebra: vectors hold the data, matrices transform it, eigenvalues reveal the structure. Vectors in, transformations out — every ML model is this pipeline.',
   [(4,10,'Vectors: data with direction and size'),
    (10,16,'Matrices: transformations — rotate, scale, project'),
    (16,22,'Eigenvalues: the structure revealed'),
    (22,26,'Every ML model is this pipeline')]),
 V(BOOTCAMP_K['mt'], 'mt', 'mt-stats', 'Distributions: The Shapes of Chance',
   'know the shape before the test', '3b1b', scene_mt_stats,
   'Distributions: normal for the well-behaved, binomial for yes/no trials, Poisson for rare events. Know the shape before the test — the wrong distribution is a wrong answer with confidence.',
   [(4,10,'Normal: the bell — means and errors'),
    (10,16,'Binomial: yes/no trials — counted successes'),
    (16,22,'Poisson: rare events — arrivals per hour'),
    (22,26,'Match shape to question — or the p-value lies')]),
 # --- android-interview
 V(BOOTCAMP_K['ai'], 'ai', 'ai-activity', 'Activity Lifecycle: The Callbacks',
   'the OS owns your activity', 'bbg', scene_ai_activity,
   'The activity lifecycle: onCreate builds, onStart shows, onResume interacts, onPause/onStop retreat, onDestroy cleans. The OS owns your activity — the callbacks are your lease terms.',
   [(4,10,'onCreate: build it — once per birth'),
    (10,16,'onStart/onResume: visible, then interactive'),
    (16,22,'onPause/onStop: retreat gracefully — save state'),
    (22,26,'onDestroy: clean up — the lease ends')]),
 V(BOOTCAMP_K['ai'], 'ai', 'ai-compose', 'Compose in 100 Seconds',
   'UI as functions of state', 'fireship', scene_ai_compose,
   'Jetpack Compose: composables are functions of state — state changes, the UI recomposes. UI as functions of state; remember the state or lose the UI.',
   [(4,10,'@Composable: UI as functions'),
    (10,16,'remember: state survives recomposition'),
    (16,22,'State hoisting: lift it up — single source'),
    (22,26,'Recomposition: surgical — only what changed')]),
 V(BOOTCAMP_K['ai'], 'ai', 'ai-mvvm', 'MVVM: The Layers',
   'the view observes, never commands', 'bbg', scene_ai_mvvm,
   'MVVM: the View observes LiveData, the ViewModel holds state, the Repository fetches. The view observes, never commands — unidirectional data flow keeps the UI honest.',
   [(4,10,'View: observes — dumb by design'),
    (10,16,'ViewModel: state holder — survives rotation'),
    (16,22,'Repository: the single source of truth'),
    (22,26,'Unidirectional flow — the UI never lies about state')]),
 # --- ios-interview
 V(BOOTCAMP_K['ios'], 'ios', 'ios-swiftui', 'SwiftUI in 100 Seconds',
   'declare the UI, let the diff do the work', 'fireship', scene_ios_swiftui,
   'SwiftUI: views are structs, @State drives updates, the framework diffs and redraws. Declare the UI, let the diff do the work — value types all the way down.',
   [(4,10,'Views are structs — value semantics'),
    (10,16,'@State: the source of truth — changes redraw'),
    (16,22,'The framework diffs — you declare'),
    (22,26,'Previews: the canvas — iterate visually')]),
 V(BOOTCAMP_K['ios'], 'ios', 'ios-lifecycle', 'ViewController Lifecycle',
   'load once, appear often', 'bbg', scene_ios_lifecycle,
   'UIViewController: viewDidLoad once, viewWillAppear/viewDidAppear every appearance, disappear in reverse. Load once, appear often — put setup and refresh in the right callbacks.',
   [(4,10,'viewDidLoad: once — build the hierarchy'),
    (10,16,'viewWillAppear: every time — refresh data'),
    (16,22,'viewDidAppear: animations start here'),
    (22,26,'Disappear: reverse — pause, save, release')]),
 V(BOOTCAMP_K['ios'], 'ios', 'ios-arc', 'ARC: Counting References',
   'the compiler inserts the retains', '3b1b', scene_ios_arc,
   'ARC: the compiler inserts retain/release — strong keeps alive, weak goes nil, unowned assumes life. The compiler inserts the retains; you manage the graph.',
   [(4,10,'Strong: ownership — keeps it alive'),
    (10,16,'Weak: no ownership — nils on death'),
    (16,22,'Unowned: trust, but verify — crashes if wrong'),
    (22,26,'Cycles: the leak — break with weak')]),
 # --- tl-interview
 V(BOOTCAMP_K['tli'], 'tli', 'tli-triage', 'Triage: The ThreatLocker Way',
   'default deny, then decide', 'bbg', scene_tli_triage,
   'ThreatLocker triage: default deny blocks first, the request queues, analysts verify legitimacy, allowlist entries are deliberate. Default deny, then decide — the product is the policy.',
   [(4,10,'Default deny: block first — ask later'),
    (10,16,'Queue: every request waits its turn'),
    (16,22,'Verify: is this legitimate — evidence, not vibes'),
    (22,26,'Allowlist deliberately — each entry a decision')]),
 V(BOOTCAMP_K['tli'], 'tli', 'tli-powershell', 'PowerShell Triage in 100 Seconds',
   'the console is the fastest incident tool', 'fireship', scene_tli_powershell,
   'PowerShell triage: list the processes, check the listeners, inspect the services — the console is the fastest incident tool when the GUI is the crime scene.',
   [(4,10,'Get-Process: what is running — sorted by CPU'),
    (10,16,'Get-NetTCPConnection: who is listening'),
    (16,22,'Get-Service: what starts at boot — the persistence'),
    (22,26,'Speed matters — the console beats the GUI')]),
 V(BOOTCAMP_K['tli'], 'tli', 'tli-scenario', 'Interview Scenario: The Live Round',
   'think aloud — they hire the reasoning', 'story', scene_tli_scenario,
   'The live round: the scenario lands, you think aloud through triage, propose containment, and document the decision. Think aloud — they hire the reasoning, not just the answer.',
   [(4,10,'The scenario: a blocked app, an impatient user'),
    (10,16,'Think aloud: narrate the triage — every step'),
    (16,22,'Contain: the safe move first — then investigate'),
    (22,26,'Document: the decision, with reasons')]),
 # --- threatlocker-assessment-prep
 V(BOOTCAMP_K['tlap'], 'tlap', 'tlap-allowlist', 'Allowlisting: The Layers',
   'deny everything, permit deliberately', 'bbg', scene_tlap_allowlist,
   'Allowlisting layers: applications by hash, scripts by policy, libraries by trust, all under default deny. Deny everything, permit deliberately — the list is the security.',
   [(4,10,'Applications: hashed — identity by cryptography'),
    (10,16,'Scripts: policy-gated — no unsigned execution'),
    (16,22,'Libraries: trusted publishers — the supply chain'),
    (22,26,'Default deny underneath — the foundation')]),
 V(BOOTCAMP_K['tlap'], 'tlap', 'tlap-ringfence', 'Ringfencing: The Containment',
   'the app can run — but not roam', 'primer', scene_tlap_ringfence,
   'Ringfencing: the app runs, but its reach is fenced — no new processes, no registry writes, no network beyond the policy. The app can run, but not roam.',
   [(4,10,'Execute: the app launches — fenced'),
    (10,16,'No child processes — the breakout dies'),
    (16,22,'No registry writes — persistence denied'),
    (22,26,'Network fenced — exfiltration choked')]),
 V(BOOTCAMP_K['tlap'], 'tlap', 'tlap-socday', 'A Day in the ThreatLocker SOC',
   'the queue is the job', 'story', scene_tlap_socday,
   'A SOC day: the queue opens, requests triaged by risk, escalations for the ambiguous, the shift log for continuity. The queue is the job — rhythm beats heroics.',
   [(4,10,'Queue opens: overnight requests, sorted by risk'),
    (10,16,'Triage: verify fast — the obvious first'),
    (16,22,'Escalate: the ambiguous goes up — with context'),
    (22,26,'Shift log: continuity — the next analyst thanks you')]),
 # --- vendor-map
 V(BOOTCAMP_K['vm'], 'vm', 'vm-landscape', 'The Vendor Landscape',
   'map the market before you buy', 'bbg', scene_vm_landscape,
   'The landscape: leaders, challengers, niche players — mapped by capability and fit. Map the market before you buy — the RFP is not research.',
   [(4,10,'Leaders: the safe choices — priced accordingly'),
    (10,16,'Challengers: hungry, innovative, riskier'),
    (16,22,'Niche: the specialists — best at one thing'),
    (22,26,'Fit beats fame — map to YOUR requirements')]),
 V(BOOTCAMP_K['vm'], 'vm', 'vm-scorecard', 'The Scorecard: Decide by Numbers',
   'weight what matters', '3b1b', scene_vm_scorecard,
   'The scorecard: weight the criteria, score each vendor, let the math argue. Weight what matters — security at 40%, price at 20%, or whatever YOUR truth is.',
   [(4,10,'Criteria: security, fit, price, support — weighted'),
    (10,16,'Score 1-5: evidence required — no vibes'),
    (16,22,'The math argues — politics loses'),
    (22,26,'Revisit weights yearly — truths change')]),
 V(BOOTCAMP_K['vm'], 'vm', 'vm-procure', 'Procurement: The Gauntlet',
   'the process protects the buyer', 'story', scene_vm_procure,
   'Procurement: requirements, RFP, demos, security review, negotiation, signature. The process protects the buyer — skip steps and the vendor owns you.',
   [(4,10,'Requirements: what you need — written first'),
    (10,16,'RFP + demos: the bake-off'),
    (16,22,'Security review: the questionnaire — non-negotiable'),
    (22,26,'Negotiate, then sign — the terms are the product')]),
 # --- zerotrust
 V(BOOTCAMP_K['zt'], 'zt', 'zt-pillars', 'Zero Trust: The Seven Pillars',
   'never trust, always verify', 'bbg', scene_zt_pillars,
   'The seven pillars: identity, devices, networks, applications, data, infrastructure, visibility. Never trust, always verify — every pillar earns its keep per request.',
   [(4,10,'Identity + devices: who and what — verified'),
    (10,16,'Networks: transport, not trust — encrypted'),
    (16,22,'Apps + data: least privilege — per request'),
    (22,26,'Visibility: the all-seeing layer — assume breach')]),
 V(BOOTCAMP_K['zt'], 'zt', 'zt-microseg', 'Microsegmentation: Small Blast Radii',
   'the breach stays in its room', 'bbg', scene_zt_microseg,
   'Microsegmentation: workloads isolated, east-west traffic inspected, policy per segment. The breach stays in its room — lateral movement dies at the segment edge.',
   [(4,10,'Segments: small — one workload, one policy'),
    (10,16,'East-west inspected — not just north-south'),
    (16,22,'Default deny between segments'),
    (22,26,'Lateral movement dies at the edge')]),
 V(BOOTCAMP_K['zt'], 'zt', 'zt-verify', 'Verify Every Request',
   'trust is per-request, not per-network', 'primer', scene_zt_verify,
   'Every request: authenticate the identity, check the device, evaluate the risk, authorize the minimum. Trust is per-request, not per-network — the VPN proves nothing.',
   [(4,10,'Authenticate: who — every time'),
    (10,16,'Device check: healthy — or no entry'),
    (16,22,'Risk evaluation: the context — location, behavior'),
    (22,26,'Authorize minimum — just enough, just now')]),
]
# ============================================================ render loop (mirrors gen_bootcamp_b4)
def render_video(v):
    fname = v["file"]
    path = os.path.join(OUT, fname)
    style, scene = v["style"], v["scene"]
    accent = ACCENTS[style]
    caps = sorted(v["captions"])
    def frames():
        total = int(NFR / 8) if SMOKE else NFR
        for f in range(total):
            t = f / FPS
            img = Image.new("RGB", (W, H), STYLE_BG[style])
            dr = ImageDraw.Draw(img)
            if t < 4:
                title_card(dr, style, v["kicker"], v["title"], v["sub"], t)
            elif t < 26:
                scene(t, dr, img)
                cur = next((c for a, b, c in caps if a <= t < b), None)
                if cur:
                    caption_bar(dr, cur, accent)
            else:
                end_card(dr, style, v["title"], v["kicker"], t - 26)
            preview_tag(dr)
            yield img
            if f % 180 == 0:
                print("  %s frame %d/%d" % (fname, f, total), flush=True)
    encode_video(path, frames())
    base, _ = os.path.splitext(path)
    vtt_cues = [(4.0, 10.0, "Preview \u2014 narration coming. " + caps[0][2])]
    vtt_cues += [(float(a), float(b), c) for a, b, c in caps]
    vtt_cues.append((26.0, 30.0, "Preview ends. Full voiceover ships when TTS is restored."))
    write_vtt(base + ".vtt", vtt_cues)
    write_narration(base + ".narration.md", v["title"], v["kicker"], fname, caps, v["blurb"])
    sz = os.path.getsize(path)
    print("DONE %s (%d bytes)" % (fname, sz), flush=True)
    return fname, sz

def main():
    only = sys.argv[1:] or None
    vids = [v for v in VIDEOS if (only is None or v["file"] in only or v["file"].replace(".mp4", "") in only)]
    print("Rendering %d videos (SMOKE=%s)" % (len(vids), SMOKE), flush=True)
    for v in vids:
        print("START", v["file"], flush=True)
        try:
            render_video(v)
        except Exception as e:
            print("FAILED %s: %r" % (v["file"], e), flush=True)

if __name__ == "__main__":
    main()
