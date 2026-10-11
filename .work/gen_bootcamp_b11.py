"""Bootcamp video Phase 2, Batch B11: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b5.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.

Batch B11 bootcamps (Career/Human):
  career-launch, deep-work, edward-bernays, electrician-apprentice, embedded-interview, entrepreneurship, frontier-path, full-spectrum-dominance, hermetica, humanmetrics, philosophy, occult-esoteric
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
# career-launch (bbg x1 + primer x1 + story x1)
def scene_cl_resume(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Resume: Your First Product', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'ten seconds to earn thirty more', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('audit: inventory every win', 5), ('quantify: numbers on bullets', 9), ('tailor: mirror the posting', 13), ('referral: the warm intro', 17), ('send: the portal is the last resort', 21)]
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
        txt(dr, (W // 2, 624), 'ten seconds to earn thirty more', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the scan decides — the interview confirms', font(F_SERIF, 24), DIM, anchor="mm")
def scene_cl_funnel(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Interview Funnel', CYAN)
    _boxes = ('apply', 'screen', 'manager', 'panel', 'offer')
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
        txt(dr, (W // 2, 500), 'each stage filters differently', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'prepare for the stage you are in — not the last one', font(F_SANS, 24), DIM, anchor="mm")
def scene_cl_offer(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Offer Negotiation: The Final Boss', CYAN)
    _lp = ('research the band first', 'anchor with data', 'whole package, not just base')
    _rp = ('first number wins', 'base-only thinking', 'verbal promises')
    _nL = int(clamp((t - 5) / 6) * len(_lp))
    _nR = int(clamp((t - 12) / 6) * len(_rp))
    dr.rectangle([120, 190, 600, 470], fill=(16, 16, 30), outline=GREEN, width=3)
    txt(dr, (360, 232), 'NEGOTIATE', font(F_BOLD, 26), GREEN, anchor="mm")
    for _i in range(_nL):
        txt(dr, (160, 290 + _i * 46), "\u2713 " + _lp[_i], font(F_SANS, 22), GREEN, anchor="lm")
    dr.rectangle([680, 190, 1160, 470], fill=(16, 16, 30), outline=RED, width=3)
    txt(dr, (920, 232), 'ACCEPT BLIND', font(F_BOLD, 26), RED, anchor="mm")
    for _i in range(_nR):
        txt(dr, (720, 290 + _i * 46), "\u2717 " + _rp[_i], font(F_SANS, 22), RED, anchor="lm")
    if t > 20:
        dr.rectangle([300, 520, 980, 592], fill=(12, 24, 12), outline=GOLD, width=3)
        txt(dr, (W // 2, 556), 'data beats desperation — negotiate', font(F_BOLD, 25), GOLD, anchor="mm")
# ============================================================
# deep-work (3b1b x1 + primer x1 + story x1)
def scene_dw_focus(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Focus Sessions: The 90-Minute Block', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'attention is the last scarcity', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), '4 blocks × 90 min = mastery', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('blocks today', 4, '%d'), ('phone checks', 0, '%d'), ('deep hours', 6, '%d')]
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
        txt(dr, (W // 2, 540), 'attention is the last scarcity', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the block is how you mine it', font(F_SANS, 24), DIM, anchor="mm")
def scene_dw_shallow(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Shallow vs Deep: The Audit', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'you cannot manage what you do not measure', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('email/chat', 0.8, '32h', RED), ('meetings', 0.5, '20h', ORANGE), ('deep work', 0.25, '10h', GREEN)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'you cannot manage what you do not measure', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'shallow feels productive — deep compounds', font(F_SANS, 24), DIM, anchor="mm")
def scene_dw_ritual(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Deep Work Ritual', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'routine protects the fragile state', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('same time: the appointment', 5), ('same place: the cues', 9), ('the block: 90 minutes, one task', 13), ('shutdown: the day ends clean', 17), ('repeat: the compound effect', 21)]
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
        txt(dr, (W // 2, 624), 'routine protects the fragile state', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'rituals beat motivation — motivation is weather', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# edward-bernays (bbg x1 + primer x1 + story x1)
def scene_eb_pr(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Bernays: The Father of Spin', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'he sold cigarettes as freedom', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [("1928: 'Propaganda' published", 5), ('torches of freedom march', 9), ('bacon-and-eggs campaign', 13), ('the engineering of consent', 17), ('modern PR: his grandchildren everywhere', 21)]
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
        txt(dr, (W // 2, 624), 'he sold cigarettes as freedom', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'study him to see the strings — then cut them', font(F_SERIF, 24), DIM, anchor="mm")
def scene_eb_torches(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Torches of Freedom: The Playbook', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('taboo', 'frame', 'stunt', 'press', 'sales')
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
        txt(dr, (W // 2, 540), 'the stunt that changed smoking', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'manufactured rebellion — sold by the pack', font(F_SANS, 24), DIM, anchor="mm")
def scene_eb_consent(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Engineering Consent: The Machine', CYAN)
    _boxes = ('symbols', 'authority', 'repetition', 'consent')
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
        txt(dr, (W // 2, 500), 'the invisible government', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'recognition is the first resistance', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# electrician-apprentice (3b1b x1 + primer x1 + story x1)
def scene_ea_current(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Current Flow: The River', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('source', 'push', 'load', 'return', 'loop')
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
        txt(dr, (W // 2, 540), 'voltage pushes, resistance resists', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the river metaphor never lies', font(F_SANS, 24), DIM, anchor="mm")
def scene_ea_ohms(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "Ohm's Law: V = IR", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'the three-variable tango', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'V = I·R · P = V·I', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('volts', 120, '%dV'), ('amps', 15, '%dA'), ('watts', 1800, '%dW')]
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
        txt(dr, (W // 2, 540), 'the three-variable tango', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'cover the unknown — read the triangle', font(F_SANS, 24), DIM, anchor="mm")
def scene_ea_years(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Apprenticeship: Four Years', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'hours plus schooling equals journeyman', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('year 1: foundations and safety', 5), ('years 2-3: circuits and code', 9), ('year 4: lead work, exam prep', 13), ('8,000 hours logged', 17), ('journeyman: licensed', 21)]
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
        txt(dr, (W // 2, 624), 'hours plus schooling equals journeyman', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'no shortcuts — only apprenticeships', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# embedded-interview (bbg x1 + 3b1b x1 + story x1)
def scene_ei_rtos(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'RTOS Interview Topics', CYAN)
    _boxes = ('tasks', 'sync', 'inversion', 'latency')
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
        txt(dr, (W // 2, 500), 'determinism is the whole game', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'think in deadlines — the interviewer does', font(F_SANS, 24), DIM, anchor="mm")
def scene_ei_bitwise(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Bitwise: The Register Game', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'masks, shifts, and flags', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'bit 3 set = 0b00001000', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('bits', 8, '%d'), ('flags set', 3, '%d'), ('mask', 255, '%d')]
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
        txt(dr, (W // 2, 540), 'masks, shifts, and flags', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the bits have names — read the datasheet', font(F_SANS, 24), DIM, anchor="mm")
def scene_ei_day(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Interview Day: Embedded', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), "whiteboard the driver, don't just describe it", font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('phone screen: C and curiosity', 5), ('whiteboard: the SPI driver, live', 9), ('system design: firmware architecture', 13), ('behavioral: the human behind it', 17), ('offer: the registers were worth it', 21)]
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
        txt(dr, (W // 2, 624), "whiteboard the driver, don't just describe it", font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'draw the timing diagram — interviewers love timing diagrams', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# entrepreneurship (bbg x1 + 3b1b x1 + story x1)
def scene_ent_mvp(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'MVP: The Smallest Bet', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the smallest thing that tests the riskiest assumption', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('assumption: name the riskiest', 5), ('mvp: the smallest test', 9), ('measure: one metric that matters', 13), ('learn: the data speaks', 17), ('persevere or pivot', 21)]
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
        txt(dr, (W // 2, 624), 'the smallest thing that tests the riskiest assumption', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'persevere or pivot — the only honest moves', font(F_SERIF, 24), DIM, anchor="mm")
def scene_ent_unit(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Unit Economics: The Business Math', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'CAC, LTV, and the ratio that matters', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'LTV:CAC ≥ 3 · payback < 12mo', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('CAC', 120, '$%d'), ('LTV', 540, '$%d'), ('ratio', 45, '%d‰')]
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
        txt(dr, (W // 2, 540), 'CAC, LTV, and the ratio that matters', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'growth without economics is just burning', font(F_SANS, 24), DIM, anchor="mm")
def scene_ent_pitch(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Pitch Deck: Ten Slides', CYAN)
    _boxes = ('problem', 'solution', 'traction', 'market', 'team')
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
        txt(dr, (W // 2, 500), 'problem, solution, traction — in that order', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'investors fund lines, not dots — show the slope', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# frontier-path (bbg x1 + primer x1 + story x1)
def scene_fp_explore(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Exploring the Frontier', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('survey', 'probe', 'map', 'share', 'repeat')
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
        txt(dr, (W // 2, 540), 'map as you go', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the frontier rewards the cartographers', font(F_SANS, 24), DIM, anchor="mm")
def scene_fp_milestones(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Milestones: The Long Arc', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the arc bends toward the prepared', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('foundations: the unglamorous years', 5), ('first expeditions: small bets', 9), ('the hard middle: persist', 13), ('breakthrough: the map fills in', 17), ('teaching: the cycle completes', 21)]
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
        txt(dr, (W // 2, 624), 'the arc bends toward the prepared', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the hard middle is the filter — pass through it', font(F_SERIF, 24), DIM, anchor="mm")
def scene_fp_stack(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Knowledge Stack', CYAN)
    _layers = ('teaching', 'judgment', 'mental models', 'facts')
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
        txt(dr, (W // 2, 612), 'every layer compounds', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'facts without models are trivia — models without facts are fantasy', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# full-spectrum-dominance (bbg x1 + primer x1 + story x1)
def scene_fspec_domains(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Five Domains of Conflict', CYAN)
    _boxes = ('land', 'sea/air', 'space', 'cyber', 'info')
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
        txt(dr, (W // 2, 500), 'war is waged everywhere now', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'perception is terrain — the info environment wraps all', font(F_SANS, 24), DIM, anchor="mm")
def scene_fspec_infoops(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Information Operations Flow', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('collect', 'craft', 'disseminate', 'amplify', 'assess')
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
        txt(dr, (W // 2, 540), 'the narrative is the maneuver', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'truth, well-timed, is the strongest munition', font(F_SANS, 24), DIM, anchor="mm")
def scene_fspec_doctrine(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Doctrine: Written in Lessons', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), "doctrine is the army's memory", font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('observe: the conflict teaches', 5), ('distill: lesson from anecdote', 9), ('write: doctrine published', 13), ('train: reflex, not reference', 17), ('the next war starts smarter', 21)]
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
        txt(dr, (W // 2, 624), "doctrine is the institution's memory", font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'written in lessons — paid for in advance', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# hermetica (bbg x1 + primer x1 + story x1)
def scene_her_principles(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Seven Principles', CYAN)
    _layers = ('gender', 'cause/effect', 'rhythm', 'polarity', 'vibration', 'correspondence', 'mentalism')
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
        txt(dr, (W // 2, 612), 'as above, so below', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the pattern repeats at every scale — learn to see it', font(F_SANS, 24), DIM, anchor="mm")
def scene_her_emerald(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Emerald Tablet', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'thirteen lines that launched alchemy', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('attributed: Hermes Trismegistus', 5), ('the axiom: as above, so below', 9), ('arabic to latin: the translation chain', 13), ('a millennium of commentary', 17), ('thirteen lines, infinite reading', 21)]
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
        txt(dr, (W // 2, 624), 'thirteen lines that launched alchemy', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'brevity plus mystery equals immortality', font(F_SERIF, 24), DIM, anchor="mm")
def scene_her_transmute(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Transmutation: The Great Work', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('calcine', 'dissolve', 'conjoin', 'ferment', 'stone')
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
        txt(dr, (W // 2, 540), 'lead to gold — and self to Self', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the outer work mirrors the inner', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# humanmetrics (3b1b x1 + primer x1 + story x1)
def scene_hm_big5(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Big Five: You, Quantified', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'traits, not types', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('openness', 0.82, '82nd %ile', TEAL), ('conscientiousness', 0.71, '71st', GREEN), ('extraversion', 0.45, '45th', YELLOW), ('agreeableness', 0.63, '63rd', CYAN), ('neuroticism', 0.3, '30th', ORANGE)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'traits, not types', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'a point in five dimensions — not a box', font(F_SANS, 24), DIM, anchor="mm")
def scene_hm_flowstate(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Flow State: The Metrics of Joy', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'challenge meets skill', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'flow = challenge ≈ skill', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('focus depth', 92, '%d%%'), ('time dilation', 3, '%dx'), ('sessions/wk', 5, '%d')]
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
        txt(dr, (W // 2, 540), 'challenge meets skill', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'boredom and anxiety are the guardrails — flow is between', font(F_SANS, 24), DIM, anchor="mm")
def scene_hm_journey(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Know Thyself: The Journey', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the examined life, scheduled', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('observe: patterns, no judgment', 5), ('name: triggers labeled', 9), ('test: small experiments', 13), ('integrate: lessons become defaults', 17), ('repeat: the examined life', 21)]
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
        txt(dr, (W // 2, 624), 'the examined life, scheduled', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'self-knowledge compounds like interest', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# philosophy (bbg x1 + 3b1b x1 + story x1)
def scene_phi_schools(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Schools of Thought', CYAN)
    _boxes = ('stoic', 'epicurean', 'skeptic', 'existentialist')
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
        txt(dr, (W // 2, 500), 'every argument has ancestors', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'meet yours — then argue with them properly', font(F_SANS, 24), DIM, anchor="mm")
def scene_phi_syllogism(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "The Syllogism: Logic's Atom", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'validity is about form, not truth', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'all A are B · x is A ∴ x is B', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('premises', 2, '%d'), ('terms', 3, '%d'), ('valid forms', 24, '%d')]
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
        txt(dr, (W // 2, 540), 'validity is about form, not truth', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'attack the form or the premises — those are the only moves', font(F_SANS, 24), DIM, anchor="mm")
def scene_phi_dialogue(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Socratic Dialogue', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the question is the method', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('ask: define courage', 5), ('counterexample: the rash soldier', 9), ('refine: the definition tightens', 13), ("aporia: knowing that you don't know", 17), ('the examined claim survives', 21)]
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
        txt(dr, (W // 2, 624), 'the question is the method', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'aporia is the doorway — confusion that teaches', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# occult-esoteric (bbg x1 + primer x1 + story x1)
def scene_occ_tree(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Tree of Life: Ten Sephiroth', CYAN)
    _nodes = [('kether', 640, 180), ('chokmah', 480, 300), ('binah', 800, 300), ('tiphareth', 640, 450), ('malkuth', 640, 600)]
    _edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
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
        txt(dr, (W // 2, 560), 'a map of everything', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'a filing system for the universe — use it that way', font(F_SANS, 24), DIM, anchor="mm")
def scene_occ_tarot(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'The Tarot Spread', CYAN)
    _rows, _cols = 3, 5
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — cards laid in the spread' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'positions give cards meaning', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'the spread is the syntax — cards are vocabulary', font(F_SANS, 24), DIM, anchor="mm")
def scene_occ_orders(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Esoteric Orders: The Lineage', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'lineage is the credential', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('golden dawn: the system', 5), ('thelema: the will', 9), ('modern lodges: the living current', 13), ('lineage claimed and tested', 17), ('the work continues', 21)]
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
        txt(dr, (W // 2, 624), 'lineage is the credential', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the reading list is the real initiation', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'cl': 'career-launch',
    'dw': 'deep-work',
    'eb': 'edward-bernays',
    'ea': 'electrician-apprentice',
    'ei': 'embedded-interview',
    'ent': 'entrepreneurship',
    'fp': 'frontier-path',
    'fspec': 'full-spectrum-dominance',
    'her': 'hermetica',
    'hm': 'humanmetrics',
    'phi': 'philosophy',
    'occ': 'occult-esoteric',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'cl': 'CAREER · Launch Sequence',
    'dw': 'DEEP WORK · Focus Mastery',
    'eb': 'BERNAYS · Propaganda & PR',
    'ea': 'ELECTRICIAN · Apprentice Path',
    'ei': 'EMBEDDED · Interview Prep',
    'ent': 'FOUNDER · Entrepreneurship',
    'fp': 'FRONTIER · Knowledge Path',
    'fspec': 'FULL SPECTRUM · Info Dominance',
    'her': 'HERMETICA · Hermetic Wisdom',
    'hm': 'HUMANMETRICS · Know Thyself',
    'phi': 'PHILOSOPHY · Think Clearly',
    'occ': 'OCCULT · Esoteric Systems',
}
VIDEOS = [
 # --- career-launch
 V(BOOTCAMP_K['cl'], 'cl', 'cl-resume', 'The Resume: Your First Product',
   'ten seconds to earn thirty more', 'story', scene_cl_resume,
   'The resume journey: audit the raw material, quantify every bullet, tailor per role, and let the referrals carry it in. Ten seconds to earn thirty more — the scan decides.',
   [(4,10,'Audit: the raw material — everything you have done'),
    (10,16,'Quantify: numbers on every bullet — impact, not duties'),
    (16,22,"Tailor: mirror the posting's language"),
    (22,26,'Referrals carry it in — the warm intro beats the portal')]),
 V(BOOTCAMP_K['cl'], 'cl', 'cl-funnel', 'The Interview Funnel',
   'each stage filters differently', 'bbg', scene_cl_funnel,
   'The funnel: application, recruiter screen, hiring manager, panel, offer. Each stage filters differently — the screen checks fit, the panel checks depth, the offer checks desire.',
   [(4,10,'Application: the keyword gate'),
    (10,16,'Recruiter screen: fit and comp — fifteen minutes'),
    (16,22,'Hiring manager: can you do the job'),
    (22,26,'Panel + offer: depth, then desire')]),
 V(BOOTCAMP_K['cl'], 'cl', 'cl-offer', 'Offer Negotiation: The Final Boss',
   'whoever names a number first loses', 'primer', scene_cl_offer,
   'Negotiation: whoever names a number first loses — anchor on research, negotiate the whole package, and get it in writing. The final boss is beaten with data, not desperation.',
   [(4,10,'Research: the market rate — levels.fyi and peers'),
    (10,16,'Anchor high — the first number sets the range'),
    (16,22,'Whole package: base, equity, bonus, remote'),
    (22,26,'Written offer — verbal promises evaporate')]),
 # --- deep-work
 V(BOOTCAMP_K['dw'], 'dw', 'dw-focus', 'Focus Sessions: The 90-Minute Block',
   'attention is the last scarcity', 'primer', scene_dw_focus,
   'Deep work: 90-minute blocks, phone in another room, one task per block. Attention is the last scarcity — the block is how you mine it.',
   [(4,10,'90 minutes: the ultradian sweet spot'),
    (10,16,'One task per block — monotasking is the method'),
    (16,22,'Phone in another room — willpower is unreliable'),
    (22,26,'Four blocks: a legendary day')]),
 V(BOOTCAMP_K['dw'], 'dw', 'dw-shallow', 'Shallow vs Deep: The Audit',
   'you cannot manage what you do not measure', '3b1b', scene_dw_shallow,
   'Audit your hours: shallow work feels productive and compounds nothing; deep work feels hard and compounds everything. You cannot manage what you do not measure — log the week.',
   [(4,10,'Email + chat: the shallow river — endless'),
    (10,16,'Meetings: necessary, minimized, batched'),
    (16,22,'Deep work: the compounding asset'),
    (22,26,'Log the week — the data will upset you')]),
 V(BOOTCAMP_K['dw'], 'dw', 'dw-ritual', 'The Deep Work Ritual',
   'routine protects the fragile state', 'story', scene_dw_ritual,
   'The ritual: same time, same place, same shutdown — the routine protects the fragile state of focus. Rituals beat motivation; motivation is weather.',
   [(4,10,'Same time: the brain learns the appointment'),
    (10,16,'Same place: the cues accumulate'),
    (16,22,'Shutdown ritual: the day ends — recovery begins'),
    (22,26,'Rituals beat motivation — motivation is weather')]),
 # --- edward-bernays
 V(BOOTCAMP_K['eb'], 'eb', 'eb-pr', 'Bernays: The Father of Spin',
   'he sold cigarettes as freedom', 'story', scene_eb_pr,
   "Bernays: Freud's nephew who turned propaganda into public relations — Torches of Freedom, bacon-and-eggs, the engineering of consent. He sold cigarettes as freedom; study him to see the strings.",
   [(4,10,"1920s: propaganda becomes 'public relations'"),
    (10,16,'Torches of Freedom: cigarettes as liberation'),
    (16,22,'Bacon and eggs: the manufactured breakfast'),
    (22,26,'Propaganda (1928): the engineering of consent, in print')]),
 V(BOOTCAMP_K['eb'], 'eb', 'eb-torches', 'Torches of Freedom: The Playbook',
   'the stunt that changed smoking', 'primer', scene_eb_torches,
   'The playbook: identify the taboo, recruit the influencers, stage the spectacle, let the press amplify. The stunt that changed smoking — manufactured rebellion, sold by the pack.',
   [(4,10,'The taboo: women smoking in public'),
    (10,16,"The frame: cigarettes as 'torches of freedom'"),
    (16,22,'The stunt: debutantes light up on Fifth Avenue'),
    (22,26,'The press: amplification, free and eager')]),
 V(BOOTCAMP_K['eb'], 'eb', 'eb-consent', 'Engineering Consent: The Machine',
   'the invisible government', 'bbg', scene_eb_consent,
   'The consent machine: symbols that bypass reason, third-party authorities that lend credibility, repetition that becomes truth. The invisible government — recognize the machine to resist it.',
   [(4,10,'Symbols: bypass reason — speak to desire'),
    (10,16,'Authorities: doctors, experts — rented credibility'),
    (16,22,'Repetition: the lie told a thousand times'),
    (22,26,'Recognize the machine — then resist it')]),
 # --- electrician-apprentice
 V(BOOTCAMP_K['ea'], 'ea', 'ea-current', 'Current Flow: The River',
   'voltage pushes, resistance resists', 'primer', scene_ea_current,
   'Current: voltage pushes, resistance resists, and the river flows from high potential to low. Voltage pushes, resistance resists — the river metaphor never lies.',
   [(4,10,'Voltage: the push — potential difference'),
    (10,16,'Current: the flow — amperes of charge'),
    (16,22,'Resistance: the rocks in the river'),
    (22,26,'Complete the circuit — or nothing flows')]),
 V(BOOTCAMP_K['ea'], 'ea', 'ea-ohms', "Ohm's Law: V = IR",
   'the three-variable tango', '3b1b', scene_ea_ohms,
   "Ohm's law: V = IR — cover the unknown, read the formula. Power adds P = VI. The three-variable tango — every circuit question is this dance.",
   [(4,10,'V = I × R: the law itself'),
    (10,16,'Cover the unknown — the triangle trick'),
    (16,22,'P = V × I: power, the heat bill'),
    (22,26,'Every circuit question is this dance')]),
 V(BOOTCAMP_K['ea'], 'ea', 'ea-years', 'The Apprenticeship: Four Years',
   'hours plus schooling equals journeyman', 'story', scene_ea_years,
   'The path: 8,000 hours of supervised work plus classroom theory, then the journeyman exam. Hours plus schooling equals journeyman — there are no shortcuts, only apprenticeships.',
   [(4,10,'Year 1: material, tools, safety — the foundations'),
    (10,16,'Years 2-3: circuits, code, independence grows'),
    (16,22,'Year 4: lead small jobs — the exam looms'),
    (22,26,'Journeyman: the license — earned, not given')]),
 # --- embedded-interview
 V(BOOTCAMP_K['ei'], 'ei', 'ei-rtos', 'RTOS Interview Topics',
   'determinism is the whole game', 'bbg', scene_ei_rtos,
   'RTOS topics: tasks and priorities, semaphores and mutexes, priority inversion, interrupt latency. Determinism is the whole game — the interview tests whether you think in deadlines.',
   [(4,10,'Tasks + priorities: who runs when'),
    (10,16,'Semaphores vs mutexes: signaling vs owning'),
    (16,22,'Priority inversion: the classic trap — and the fix'),
    (22,26,'Interrupt latency: the deadline you cannot miss')]),
 V(BOOTCAMP_K['ei'], 'ei', 'ei-bitwise', 'Bitwise: The Register Game',
   'masks, shifts, and flags', '3b1b', scene_ei_bitwise,
   'Bitwise ops: OR sets bits, AND clears with masks, shifts multiply by powers of two. Masks, shifts, and flags — the register game every embedded interview plays.',
   [(4,10,'OR sets — AND clears (with the mask)'),
    (10,16,'XOR toggles — the flip'),
    (16,22,'Shifts: << multiplies by 2^n — fast math'),
    (22,26,'Read the datasheet — the bits have names')]),
 V(BOOTCAMP_K['ei'], 'ei', 'ei-day', 'Interview Day: Embedded',
   "whiteboard the driver, don't just describe it", 'story', scene_ei_day,
   "Interview day: the phone screen filters, the technical round whiteboards a driver, the system round designs the firmware, the behavioral round checks the human. Whiteboard the driver — don't just describe it.",
   [(4,10,'Phone screen: the filter — C and curiosity'),
    (10,16,'Technical: whiteboard the SPI driver'),
    (16,22,'System design: the firmware architecture'),
    (22,26,'Behavioral: the human behind the registers')]),
 # --- entrepreneurship
 V(BOOTCAMP_K['ent'], 'ent', 'ent-mvp', 'MVP: The Smallest Bet',
   'the smallest thing that tests the riskiest assumption', 'story', scene_ent_mvp,
   'The MVP: not the smallest product — the smallest bet that tests the riskiest assumption. Build it, measure the one metric, learn, and either persevere or pivot.',
   [(4,10,'Riskiest assumption first — name it'),
    (10,16,'Smallest test: concierge, wizard-of-oz, landing page'),
    (16,22,'One metric: the learning, quantified'),
    (22,26,'Persevere or pivot — the only two honest moves')]),
 V(BOOTCAMP_K['ent'], 'ent', 'ent-unit', 'Unit Economics: The Business Math',
   'CAC, LTV, and the ratio that matters', '3b1b', scene_ent_unit,
   'Unit economics: CAC to acquire, LTV over the lifetime — the ratio must clear 3:1, and payback under 12 months. CAC, LTV, and the ratio that matters — growth without economics is just burning.',
   [(4,10,'CAC: the cost to acquire one customer'),
    (10,16,'LTV: the lifetime value — gross margin times tenure'),
    (16,22,'LTV:CAC ≥ 3:1 — the bar'),
    (22,26,'Payback < 12 months — cash is oxygen')]),
 V(BOOTCAMP_K['ent'], 'ent', 'ent-pitch', 'The Pitch Deck: Ten Slides',
   'problem, solution, traction — in that order', 'bbg', scene_ent_pitch,
   'The deck: problem, solution, traction, market, team — ten slides, eighteen minutes. Problem, solution, traction, in that order — investors fund lines, not dots.',
   [(4,10,'Problem: the pain — felt, expensive, now'),
    (10,16,"Solution: the demo — show, don't tell"),
    (16,22,'Traction: the line going up — the only slide that matters'),
    (22,26,'Team: why you win — the unfair advantage')]),
 # --- frontier-path
 V(BOOTCAMP_K['fp'], 'fp', 'fp-explore', 'Exploring the Frontier',
   'map as you go', 'primer', scene_fp_explore,
   'Exploring: survey the territory, probe the edges, map what you find, and share the map. Map as you go — the frontier rewards the cartographers.',
   [(4,10,'Survey: what is known — the literature'),
    (10,16,'Probe: the edges — where maps go blank'),
    (16,22,'Map: write it down — memory lies'),
    (22,26,'Share: the frontier grows by publication')]),
 V(BOOTCAMP_K['fp'], 'fp', 'fp-milestones', 'Milestones: The Long Arc',
   'the arc bends toward the prepared', 'story', scene_fp_milestones,
   'The long arc: foundations, first expeditions, the hard middle, breakthroughs, then teaching. The arc bends toward the prepared — luck favors the mapped.',
   [(4,10,'Foundations: the unglamorous years'),
    (10,16,'First expeditions: small bets, real data'),
    (16,22,'The hard middle: where most quit'),
    (22,26,'Breakthrough, then teaching — the cycle completes')]),
 V(BOOTCAMP_K['fp'], 'fp', 'fp-stack', 'The Knowledge Stack',
   'every layer compounds', 'bbg', scene_fp_stack,
   'The knowledge stack: facts at the base, mental models above, judgment at the top. Every layer compounds — facts without models are trivia; models without facts are fantasy.',
   [(4,10,'Facts: the base — collected deliberately'),
    (10,16,'Mental models: the structure — how things work'),
    (16,22,'Judgment: the top — when to trust the model'),
    (22,26,'Teaching: the layer that locks it in')]),
 # --- full-spectrum-dominance
 V(BOOTCAMP_K['fspec'], 'fspec', 'fspec-domains', 'Five Domains of Conflict',
   'war is waged everywhere now', 'bbg', scene_fspec_domains,
   'Five domains: land, sea, air, space, cyber — plus the information environment wrapping them all. War is waged everywhere now; the spectrum is the battlefield.',
   [(4,10,'Land, sea, air: the classical three'),
    (10,16,'Space: the high ground — satellites decide'),
    (16,22,'Cyber: the fifth domain — code as maneuver'),
    (22,26,'Information: the wraparound — perception is terrain')]),
 V(BOOTCAMP_K['fspec'], 'fspec', 'fspec-infoops', 'Information Operations Flow',
   'the narrative is the maneuver', 'primer', scene_fspec_infoops,
   'Info ops: collect the environment, craft the narrative, disseminate through channels, assess the effect. The narrative is the maneuver — effects measured in belief, not craters.',
   [(4,10,'Collect: the information environment, mapped'),
    (10,16,'Craft: the narrative — true, well-timed'),
    (16,22,'Disseminate: channels chosen for the audience'),
    (22,26,'Assess: belief shifted — measure the effect')]),
 V(BOOTCAMP_K['fspec'], 'fspec', 'fspec-doctrine', 'Doctrine: Written in Lessons',
   "doctrine is the army's memory", 'story', scene_fspec_doctrine,
   "Doctrine evolves: observe the conflict, distill the lesson, write it down, train it in. Doctrine is the institution's memory — written in lessons, paid for in advance.",
   [(4,10,'Observe: the conflict teaches'),
    (10,16,'Distill: the lesson, stripped of anecdote'),
    (16,22,'Write: doctrine published — the memory externalized'),
    (22,26,'Train: the lesson becomes reflex')]),
 # --- hermetica
 V(BOOTCAMP_K['her'], 'her', 'her-principles', 'The Seven Principles',
   'as above, so below', 'bbg', scene_her_principles,
   'The seven Hermetic principles: mentalism, correspondence, vibration, polarity, rhythm, cause and effect, gender. As above, so below — the pattern repeats at every scale.',
   [(4,10,'Mentalism: all is mind — the foundation'),
    (10,16,'Correspondence: as above, so below'),
    (16,22,'Vibration + polarity + rhythm: the mechanics'),
    (22,26,'Cause and effect + gender: the dynamics')]),
 V(BOOTCAMP_K['her'], 'her', 'her-emerald', 'The Emerald Tablet',
   'thirteen lines that launched alchemy', 'story', scene_her_emerald,
   "The Emerald Tablet: thirteen lines attributed to Hermes Trismegistus — 'as above, so below' — the seed of alchemy, translated and retranslated for a thousand years.",
   [(4,10,'Antiquity: attributed to Hermes Trismegistus'),
    (10,16,'The axiom: as above, so below'),
    (16,22,'Translation chains: Arabic to Latin to vernacular'),
    (22,26,'A thousand years of commentary — thirteen lines')]),
 V(BOOTCAMP_K['her'], 'her', 'her-transmute', 'Transmutation: The Great Work',
   'lead to gold — and self to Self', 'primer', scene_her_transmute,
   'The Great Work: calcination burns the dross, dissolution loosens, conjunction unites, and the stone — or the self — emerges. Lead to gold, and self to Self: the outer work mirrors the inner.',
   [(4,10,'Calcination: burn away the dross'),
    (10,16,'Dissolution + separation: loosen and purify'),
    (16,22,'Conjunction: unite the opposites'),
    (22,26,'The stone: the work completes — within and without')]),
 # --- humanmetrics
 V(BOOTCAMP_K['hm'], 'hm', 'hm-big5', 'The Big Five: You, Quantified',
   'traits, not types', '3b1b', scene_hm_big5,
   'The Big Five: openness, conscientiousness, extraversion, agreeableness, neuroticism — traits, not types. You are a point in five dimensions, not a box in sixteen.',
   [(4,10,'Openness: the appetite for the new'),
    (10,16,'Conscientiousness: the predictor — it forecasts success'),
    (16,22,'Extraversion + agreeableness: the social axes'),
    (22,26,'Neuroticism: the sensitivity dial — low is steadier')]),
 V(BOOTCAMP_K['hm'], 'hm', 'hm-flowstate', 'Flow State: The Metrics of Joy',
   'challenge meets skill', 'primer', scene_hm_flowstate,
   'Flow: challenge matched to skill, clear goals, immediate feedback — the metrics of joy. Challenge meets skill and time dilates; too easy bores, too hard anxieties.',
   [(4,10,'Challenge-skill balance: the channel'),
    (10,16,'Clear goals: the mind knows the target'),
    (16,22,'Immediate feedback: the loop stays tight'),
    (22,26,'Time dilates — the signature of flow')]),
 V(BOOTCAMP_K['hm'], 'hm', 'hm-journey', 'Know Thyself: The Journey',
   'the examined life, scheduled', 'story', scene_hm_journey,
   'The journey inward: observe the patterns, name the triggers, test the changes, integrate the lessons. The examined life, scheduled — self-knowledge compounds like interest.',
   [(4,10,'Observe: patterns without judgment'),
    (10,16,'Name: triggers, labeled precisely'),
    (16,22,'Test: small changes — experiments, not vows'),
    (22,26,'Integrate: the lessons become defaults')]),
 # --- philosophy
 V(BOOTCAMP_K['phi'], 'phi', 'phi-schools', 'Schools of Thought',
   'every argument has ancestors', 'bbg', scene_phi_schools,
   'The schools: Stoics on control, Epicureans on pleasure rightly understood, Skeptics on suspension, Existentialists on the absurd freedom. Every argument has ancestors — meet yours.',
   [(4,10,'Stoics: control the controllable — the dichotomy'),
    (10,16,'Epicureans: pleasure, rightly understood — not excess'),
    (16,22,'Skeptics: suspend judgment — the equipollent arguments'),
    (22,26,'Existentialists: the absurd freedom — choose anyway')]),
 V(BOOTCAMP_K['phi'], 'phi', 'phi-syllogism', "The Syllogism: Logic's Atom",
   'validity is about form, not truth', '3b1b', scene_phi_syllogism,
   'The syllogism: all men are mortal; Socrates is a man; therefore Socrates is mortal. Validity is about form, not truth — the machine checks the shape of the argument.',
   [(4,10,'Premises: the givens — granted for the argument'),
    (10,16,'Form: the shape — Barbara, Celarent, and friends'),
    (16,22,'Validity: follows or not — no partial credit'),
    (22,26,'Soundness: valid PLUS true premises — the gold')]),
 V(BOOTCAMP_K['phi'], 'phi', 'phi-dialogue', 'The Socratic Dialogue',
   'the question is the method', 'story', scene_phi_dialogue,
   'Socrates: ask for the definition, find the counterexample, refine, repeat — until the interlocutor discovers they knew less than they thought. The question is the method; aporia is the doorway.',
   [(4,10,'Ask: what IS courage — the definition demanded'),
    (10,16,'Counterexample: the brave-but-foolish soldier'),
    (16,22,'Refine: the definition tightens'),
    (22,26,'Aporia: productive confusion — the doorway')]),
 # --- occult-esoteric
 V(BOOTCAMP_K['occ'], 'occ', 'occ-tree', 'The Tree of Life: Ten Sephiroth',
   'a map of everything', 'bbg', scene_occ_tree,
   'The Tree of Life: ten sephiroth from Kether the crown to Malkuth the kingdom, twenty-two paths between. A map of everything — study it as a filing system for the universe.',
   [(4,10,'Kether: the crown — pure becoming'),
    (10,16,'The pillars: mercy, severity, balance'),
    (16,22,'Malkuth: the kingdom — the world you touch'),
    (22,26,'Twenty-two paths: the connections — study the map')]),
 V(BOOTCAMP_K['occ'], 'occ', 'occ-tarot', 'The Tarot Spread',
   'positions give cards meaning', 'primer', scene_occ_tarot,
   'A tarot spread: positions give cards meaning — past, present, the crossing card. The spread is the syntax; the cards are the vocabulary. Read the grammar, not just the words.',
   [(4,10,'Positions: the syntax — past, present, future'),
    (10,16,'Major arcana: the big archetypes'),
    (16,22,'Minor arcana: the daily texture'),
    (22,26,'Read the grammar — the spread speaks in sentences')]),
 V(BOOTCAMP_K['occ'], 'occ', 'occ-orders', 'Esoteric Orders: The Lineage',
   'lineage is the credential', 'story', scene_occ_orders,
   'The orders: Golden Dawn systematizes, Thelema wills, modern lodges adapt — lineage is the credential, and the reading list is the real initiation.',
   [(4,10,'Golden Dawn: the system — grades and rituals'),
    (10,16,"Thelema: the will — 'do what thou wilt'"),
    (16,22,'Modern lodges: adaptation — the living current'),
    (22,26,'The reading list: the real initiation')]),
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
