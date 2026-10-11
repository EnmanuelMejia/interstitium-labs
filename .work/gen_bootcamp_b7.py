"""Bootcamp video Phase 2, Batch B7: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b5.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.

Batch B7 bootcamps (Security Certifications):
  cism, cissp, comptia-cyber, dod-8140, nice-framework, nsa-codebreaker, pentest, sc-200, sc-300, soc-analyst, fde-training, hackers-arise
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
# cism (bbg x1 + 3b1b x1 + story x1)
def scene_cism_domains(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, "CISM's Four Domains", CYAN)
    _boxes = ('governance', 'risk mgmt', 'incident mgmt', 'program dev')
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
        txt(dr, (W // 2, 500), 'governance first, technology last', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'think like a manager and the exam gets easy', font(F_SANS, 24), DIM, anchor="mm")
def scene_cism_risk(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Risk: Threat Times Vulnerability', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'no vulnerability, no risk', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'risk = threat × vulnerability × impact', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('threat actors', 12, '%d'), ('open vulns', 47, '%d'), ('high risks', 9, '%d')]
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
        txt(dr, (W // 2, 540), 'no vulnerability, no risk', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'quantify it or you cannot manage it', font(F_SANS, 24), DIM, anchor="mm")
def scene_cism_incident(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Breach at Midnight', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the plan you rehearsed is the plan you get', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('detect: anomaly pages the IR team', 5), ('contain: isolate hosts, kill sessions', 9), ('eradicate: remove persistence, rotate keys', 13), ('recover: restore service, verify integrity', 17), ('learn: blameless postmortem within 48h', 21)]
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
        txt(dr, (W // 2, 624), 'the plan you rehearsed is the plan you get', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'blameless postmortems fix systems, not people', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# cissp (bbg x2 + story x1)
def scene_cissp_domains(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Eight Domains, One Mindset', CYAN)
    _rows, _cols = 4, 2
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — domains lighting up' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'eight domains, one mindset', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), "the advisor's answer beats the technician's", font(F_SANS, 24), DIM, anchor="mm")
def scene_cissp_cia(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The CIA Triad: The Whole Field', CYAN)
    _layers = ('availability', 'integrity', 'confidentiality')
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
        txt(dr, (W // 2, 612), 'every control serves one of three', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'classify the control and the question answers itself', font(F_SANS, 24), DIM, anchor="mm")
def scene_cissp_bcp(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'RTO vs RPO: The Recovery Math', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'how much loss can you afford', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('BIA: rank every process by pain', 5), ('RTO declared: 4 hours for order processing', 9), ('RPO declared: 1 hour of transactions', 13), ('DR test: fail over, measure, adjust', 17), ('board signs the residual risk', 21)]
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
        txt(dr, (W // 2, 624), 'how much loss can you afford — the business decides', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'IT implements the numbers it does not set', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# comptia-cyber (bbg x1 + fireship x1 + primer x1)
def scene_cyb_killchain(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'The Kill Chain: Seven Steps', CYAN)
    _pts = [(140, 330), (320, 330), (500, 330), (680, 330), (860, 330), (1040, 330), (1180, 330)]
    _labels = ('recon', 'weaponize', 'deliver', 'exploit', 'install', 'C2', 'act')
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
        txt(dr, (W // 2, 540), 'break one link and the attack dies', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'defense in depth is just links in your favor', font(F_SANS, 24), DIM, anchor="mm")
def scene_cyb_siem(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'SIEM: The Security Nervous System', CYAN)
    _boxes = ('collect', 'normalize', 'correlate', 'alert', 'hunt')
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
        txt(dr, (W // 2, 500), 'correlate or drown in alerts', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the story is across sources, never in one log', font(F_SANS, 24), DIM, anchor="mm")
def scene_cyb_logread(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Reading Logs in 100 Seconds', MAGENTA)
    _lns = [('Oct 9 02:14:01 sshd[41]: Failed password', RED), ('Oct 9 02:14:03 sshd[41]: Failed password', RED), ('Oct 9 02:14:05 sshd[41]: Accepted key', GREEN), ('# 3 tries → key auth: brute force?', YELLOW), ('# check: source IP vs known hosts', DIM), ('# timestamps first — always', GREEN)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'auth.log', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'the timestamp is the alibi — sort first', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'read chronologically and the attack confesses', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# dod-8140 (bbg x2 + story x1)
def scene_dod_categories(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, '8140 Workforce Categories', CYAN)
    _boxes = ('operate', 'protect', 'analyze', 'oversee')
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
        txt(dr, (W // 2, 500), 'every billet maps to a work role', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'no exceptions — the matrix covers everyone', font(F_SANS, 24), DIM, anchor="mm")
def scene_dod_qualify(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Qualification Levels: The Ladder', CYAN)
    _layers = ('clearance', 'environment training', 'baseline cert')
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
        txt(dr, (W // 2, 612), 'certification plus clearance plus training', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the billet waits for the qualified — not the eager', font(F_SANS, 24), DIM, anchor="mm")
def scene_dod_path(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The 8140 Qualification Journey', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'from applicant to qualified', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('baseline cert earned — Security+', 5), ('environment training complete', 9), ('clearance adjudicated', 13), ('assigned to work role', 17), ('CE credits: the treadmill never stops', 21)]
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
        txt(dr, (W // 2, 624), 'from applicant to qualified — then stay qualified', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'a trophy gathers dust — a status needs feeding', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# nice-framework (bbg x2 + 3b1b x1)
def scene_nice_categories(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'NICE: Seven Categories', CYAN)
    _boxes = ('provision', 'operate', 'govern', 'protect', 'analyze', 'collect', 'investigate')
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
        txt(dr, (W // 2, 500), 'the common language of cyber work', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'speak NICE in interviews and hiring managers nod', font(F_SANS, 24), DIM, anchor="mm")
def scene_nice_ksa(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'KSAs: Knowledge, Skills, Abilities', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'the job description, decomposed', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'knowledge × skills × abilities', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('work roles', 52, '%d'), ('knowledge items', 630, '%d'), ('skill statements', 410, '%d')]
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
        txt(dr, (W // 2, 540), 'the job description, decomposed', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'match your KSAs to theirs, line by line', font(F_SANS, 24), DIM, anchor="mm")
def scene_nice_roles(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Work Roles: The Career Map', CYAN)
    _nodes = [('analyst', 300, 280), ('soc', 560, 200), ('vuln', 560, 380), ('forensics', 860, 280), ('intel', 1100, 280)]
    _edges = [(0, 1), (0, 2), (0, 3), (3, 4)]
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
        txt(dr, (W // 2, 560), 'fifty-two roles, one map', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'collect KSAs deliberately — careers are built, not found', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# nsa-codebreaker (fireship x1 + 3b1b x1 + primer x1)
def scene_nsa_rsa(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'RSA: Math as Armor', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'multiplying is easy — factoring is not', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'n = p × q · break n, break everything', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('key bits', 2048, '%d'), ('primes', 2, '%d'), ('years to factor', 300, '%d')]
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
        txt(dr, (W // 2, 540), 'multiplying is easy — factoring is not', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the armor is arithmetic, not obscurity', font(F_SANS, 24), DIM, anchor="mm")
def scene_nsa_puzzle(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'The Codebreaker Grid', CYAN)
    _rows, _cols = 6, 8
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — cells resolved by frequency + cribs' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'every solved cell constrains the rest', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'the crib is the crowbar', font(F_SANS, 24), DIM, anchor="mm")
def scene_nsa_pcap(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Reading Packets in 100 Seconds', MAGENTA)
    _lns = [('10.0.0.5 → 10.0.0.9  SYN', (200, 200, 255)), ('10.0.0.9 → 10.0.0.5  SYN, ACK', (200, 200, 255)), ('10.0.0.5 → 10.0.0.9  POST /login', YELLOW), ('user=admin&pass=Summer2026!', RED), ('# follow TCP stream → session reassembled', GREEN), ('# cleartext creds: game over', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'capture.pcap', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'follow the stream, not the packets', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'cleartext credentials are the eternal sin', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# pentest (bbg x1 + fireship x1 + primer x1)
def scene_pt_phases(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Five Phases', CYAN)
    _boxes = ('recon', 'scanning', 'exploit', 'persist', 'report')
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
        txt(dr, (W // 2, 500), 'get permission first — always', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the report is the deliverable — shells are evidence', font(F_SANS, 24), DIM, anchor="mm")
def scene_pt_nmap(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Nmap in 100 Seconds', MAGENTA)
    _lns = [('$ nmap -sV -sC 10.0.0.0/24', YELLOW), ('22/tcp  open  ssh     OpenSSH 8.9', (200, 200, 255)), ('80/tcp  open  http    nginx 1.18', (200, 200, 255)), ('443/tcp open  ssl     expired cert!', RED), ('# expired cert → note it, move on', GREEN), ('# in scope, authorized — scan on', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'nmap.out', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'scan like you own it — this time you do', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'authorization is the difference between test and crime', font(F_SANS, 24), DIM, anchor="mm")
def scene_pt_privesc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Privilege Escalation Path', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('foothold', 'enumerate', 'misconfig', 'exploit', 'root')
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
        txt(dr, (W // 2, 540), 'enumeration before exploitation — always', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the path hides in misconfigurations', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# sc-200 (bbg x1 + fireship x1 + primer x1)
def scene_sc200_sentinel(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Sentinel: The Cloud SIEM', CYAN)
    _boxes = ('connect', 'correlate', 'triage', 'respond')
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
        txt(dr, (W // 2, 500), 'connectors in, incidents out', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the playbook works the night shift', font(F_SANS, 24), DIM, anchor="mm")
def scene_sc200_kql(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'KQL in 100 Seconds', MAGENTA)
    _lns = [('SigninLogs', (200, 200, 255)), ('| where TimeGenerated > ago(1d)', YELLOW), ('| where ResultType != 0', YELLOW), ('| summarize fails=count() by UserPrincipalName', (200, 200, 255)), ('| sort by fails desc', (200, 200, 255)), ('# failed logins, ranked: the brute force confesses', GREEN)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'hunt.kql', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'pipe everything, summarize always', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'the query is the investigation', font(F_SANS, 24), DIM, anchor="mm")
def scene_sc200_playbook(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'SOAR Playbook: The Auto-Responder', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('trigger', 'enrich', 'decide', 'contain', 'ticket')
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
        txt(dr, (W // 2, 540), 'the machine does the boring parts', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'analysts investigate — playbooks administrate', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# sc-300 (bbg x1 + fireship x1 + primer x1)
def scene_sc300_identity(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Identity: The New Perimeter', CYAN)
    _layers = ('session', 'policy engine', 'device trust', 'user identity')
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
        txt(dr, (W // 2, 612), 'verify explicitly, every time', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the perimeter is identity now — firewalls are scenery', font(F_SANS, 24), DIM, anchor="mm")
def scene_sc300_mfa(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'MFA: The 99.9% Fix', CYAN)
    _pts = [(200, 330), (460, 330), (720, 330), (980, 330)]
    _labels = ('password', 'push sent', 'approved', 'token issued')
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
        txt(dr, (W // 2, 540), 'one extra factor stops nearly everything', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'go phishing-resistant — FIDO2 ends the push-bombing', font(F_SANS, 24), DIM, anchor="mm")
def scene_sc300_ca(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Conditional Access in 100 Seconds', MAGENTA)
    _lns = [('{', (200, 200, 255)), ('  "conditions": {"risk": "medium+"},', YELLOW), ('  "grant": ["mfa", "compliant-device"],', GREEN), ('  "state": "report-only  // then enforce",', DIM), ('}', (200, 200, 255)), ('# signals in → decision out', YELLOW)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'ca-policy.json', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'if this, then require that', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'report-only mode first — measure before you enforce', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# soc-analyst (bbg x1 + primer x1 + story x1)
def scene_soc_triage(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Alert Triage: The First Five Minutes', CYAN)
    _boxes = ('validate', 'scope', 'prioritize', 'verdict')
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
        txt(dr, (W // 2, 500), 'every alert gets a verdict in five minutes', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the queue never sleeps — neither does the method', font(F_SANS, 24), DIM, anchor="mm")
def scene_soc_escalation(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Escalation Ladder', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'know when to pull the cord', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('L1 triage: alert validated as real', 5), ('L2 hunt: lateral movement found', 9), ('IR declared: war room opens', 13), ('contained: hosts isolated, keys rotated', 17), ('exec brief: impact in plain language', 21)]
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
        txt(dr, (W // 2, 624), 'know when to pull the cord', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'escalation is a skill — not a failure', font(F_SERIF, 24), DIM, anchor="mm")
def scene_soc_ioc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'IOC Hunting: The Grid Search', CYAN)
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — endpoints swept for indicators' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'one indicator is a clue — ten is a campaign', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'hunt the friends, not just the felon', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# fde-training (bbg x1 + primer x1 + story x1)
def scene_fde_layers(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Full Disk Encryption Layers', CYAN)
    _layers = ('recovery key', 'PIN unlock', 'TPM seal', 'encrypted volume')
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
        txt(dr, (W // 2, 612), 'the data rests encrypted', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'theft gets hardware — not data', font(F_SANS, 24), DIM, anchor="mm")
def scene_fde_tpm(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'TPM Unlock: The Boot Handshake', CYAN)
    _pts = [(200, 330), (460, 330), (720, 330), (980, 330)]
    _labels = ('measure boot', 'compare seals', 'release key', 'unlock disk')
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
        txt(dr, (W // 2, 540), 'the chip vouches for the boot', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'evil maid meets sealed storage — and loses', font(F_SANS, 24), DIM, anchor="mm")
def scene_fde_recovery(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Lost PIN', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the recovery key is the spare tire', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('lockout: PIN forgotten at 8 AM', 5), ('identity verified per procedure', 9), ('recovery key pulled from escrow', 13), ('volume unlocked, new PIN set', 17), ('audit log: every step recorded', 21)]
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
        txt(dr, (W // 2, 624), 'the recovery key is the spare tire', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'escrow it before you need it — not during', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# hackers-arise (fireship x1 + primer x1 + story x1)
def scene_ha_recon(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Recon Commands in 100 Seconds', MAGENTA)
    _lns = [('$ whois target.com | grep -i admin', (200, 200, 255)), ('$ dig target.com ANY +short', (200, 200, 255)), ('$ sublist3r -d target.com', YELLOW), ('dev.target.com  ← forgotten, vulnerable', RED), ('# passive first — active second', GREEN), ('# touch nothing you cannot explain', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'recon.sh', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'enumerate everything, touch nothing', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'the quieter the recon, the louder the findings', font(F_SANS, 24), DIM, anchor="mm")
def scene_ha_wifi(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'WiFi Attack Chain', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('monitor', 'capture', 'handshake', 'crack', 'in')
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
        txt(dr, (W // 2, 540), 'the handshake is the prize', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the lab is the boundary — permission is the license', font(F_SANS, 24), DIM, anchor="mm")
def scene_ha_path(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'From Script Kiddie to Pro', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'curiosity plus discipline equals career', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('lab built: curiosity goes legal', 5), ('fundamentals: TCP/IP and Linux cold', 9), ('certified: the resume gets past the filter', 13), ('junior role: real alerts, real mentors', 17), ('never stop: the field moves monthly', 21)]
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
        txt(dr, (W // 2, 624), 'curiosity plus discipline equals career', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the tools are the easy part — fundamentals are the moat', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'cism': 'cism',
    'cissp': 'cissp',
    'cyb': 'comptia-cyber',
    'dod': 'dod-8140',
    'nice': 'nice-framework',
    'nsa': 'nsa-codebreaker',
    'pt': 'pentest',
    'sc200': 'sc-200',
    'sc300': 'sc-300',
    'soc': 'soc-analyst',
    'fde': 'fde-training',
    'ha': 'hackers-arise',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'cism': 'CISM · InfoSec Management',
    'cissp': 'CISSP · Security Professional',
    'cyb': 'CYSA+ · Cybersecurity Analyst',
    'dod': 'DOD 8140 · Cyber Workforce',
    'nice': 'NICE · Workforce Framework',
    'nsa': 'NSA · Codebreaker Challenge',
    'pt': 'PENTEST · Ethical Hacking',
    'sc200': 'SC-200 · Security Operations',
    'sc300': 'SC-300 · Identity Administrator',
    'soc': 'SOC · Security Analyst',
    'fde': 'FDE · Disk Encryption',
    'ha': 'HACKERS-ARISE · Hands-On Hacking',
}
VIDEOS = [
 # --- cism
 V(BOOTCAMP_K['cism'], 'cism', 'cism-domains', "CISM's Four Domains",
   'governance first, technology last', 'bbg', scene_cism_domains,
   "CISM's four domains: governance, risk management, incident management, program development. The exam is management-first — technology answers are usually the wrong answers.",
   [(4,10,'Governance: the security strategy answers to the business'),
    (10,16,'Risk management: identify, assess, treat — on repeat'),
    (16,22,'Incident management: detect, respond, recover'),
    (22,26,'Program development: build the machine that does all three')]),
 V(BOOTCAMP_K['cism'], 'cism', 'cism-risk', 'Risk: Threat Times Vulnerability',
   'no vulnerability, no risk', '3b1b', scene_cism_risk,
   'Risk = threat × vulnerability × impact. Remove any factor and risk collapses — patch the vulnerability, transfer the impact with insurance, accept what remains. The exam quantifies everything.',
   [(4,10,'Threat: the actor with motive and means'),
    (10,16,'Vulnerability: the weakness they can reach'),
    (16,22,'Impact: what breaks if they succeed'),
    (22,26,'Risk = T x V x I — zero any factor, kill the risk')]),
 V(BOOTCAMP_K['cism'], 'cism', 'cism-incident', 'The Breach at Midnight',
   'the plan you rehearsed is the plan you get', 'story', scene_cism_incident,
   'An incident timeline: detect the anomaly, contain the blast radius, eradicate the foothold, recover the service, then the blameless lessons-learned. The plan you rehearsed is the plan you get.',
   [(4,10,'Detect the anomaly — the 2 AM alert that matters'),
    (10,16,'Contain the blast radius — isolate first'),
    (16,22,'Eradicate the foothold — kill persistence'),
    (22,26,'Recover, then lessons-learned — blameless')]),
 # --- cissp
 V(BOOTCAMP_K['cissp'], 'cissp', 'cissp-domains', 'Eight Domains, One Mindset',
   'think like a risk advisor', 'bbg', scene_cissp_domains,
   'The eight CISSP domains: security and risk, asset security, architecture, network, IAM, assessment, operations, software security. One mindset across all eight — think like a risk advisor, not a technician.',
   [(4,10,'Eight domains — one exam, one mindset'),
    (10,16,'Risk management underpins every domain'),
    (16,22,"The exam rewards the advisor's answer"),
    (22,26,'Technician answers are usually the traps')]),
 V(BOOTCAMP_K['cissp'], 'cissp', 'cissp-cia', 'The CIA Triad: The Whole Field',
   'every control serves one of three', 'bbg', scene_cissp_cia,
   'The CIA triad: confidentiality keeps secrets secret, integrity keeps data trustworthy, availability keeps systems reachable. Every control in the field serves at least one — classify the control, ace the question.',
   [(4,10,'Confidentiality: secrets stay secret — encryption, access'),
    (10,16,'Integrity: data stays trustworthy — hashes, signatures'),
    (16,22,'Availability: systems stay reachable — redundancy, backups'),
    (22,26,'Every control serves at least one — classify it')]),
 V(BOOTCAMP_K['cissp'], 'cissp', 'cissp-bcp', 'RTO vs RPO: The Recovery Math',
   'how much loss can you afford', 'story', scene_cissp_bcp,
   'RTO is how long you can be down; RPO is how much data you can lose. Backups set the RPO, redundancy sets the RTO — and the business, not IT, declares both numbers.',
   [(4,10,'RTO: the downtime the business can survive'),
    (10,16,'RPO: the data loss the business can swallow'),
    (16,22,'Backups set the RPO — test the restore'),
    (22,26,'Redundancy sets the RTO — the business declares both')]),
 # --- comptia-cyber
 V(BOOTCAMP_K['cyb'], 'cyb', 'cyb-killchain', 'The Kill Chain: Seven Steps',
   'break one link, stop the attack', 'primer', scene_cyb_killchain,
   'The cyber kill chain: recon, weaponize, deliver, exploit, install, command-and-control, act. Defenders win by breaking ANY link — you do not have to stop every step, just one.',
   [(4,10,'Recon: they study you before they touch you'),
    (10,16,'Weaponize and deliver: the payload finds its carrier'),
    (16,22,'Exploit and install: the foothold lands'),
    (22,26,'C2 and actions: break ANY link — the chain snaps')]),
 V(BOOTCAMP_K['cyb'], 'cyb', 'cyb-siem', 'SIEM: The Security Nervous System',
   'correlate or drown in alerts', 'bbg', scene_cyb_siem,
   'The SIEM pipeline: collect logs from everything, normalize the formats, correlate across sources, alert on the patterns that matter. Correlate or drown — ten thousand raw events become three real incidents.',
   [(4,10,'Collect: every log, every device, one pipeline'),
    (10,16,'Normalize: one schema for fifty formats'),
    (16,22,'Correlate: the login plus the download equals the story'),
    (22,26,'Alert: three real incidents from ten thousand events')]),
 V(BOOTCAMP_K['cyb'], 'cyb', 'cyb-logread', 'Reading Logs in 100 Seconds',
   'the timestamp is the alibi', 'fireship', scene_cyb_logread,
   'Log reading: the timestamp orders everything, the source IP names the actor, the status code tells the outcome, and the user agent rats out the tool. Read chronologically — the attack tells its own story.',
   [(4,10,'Timestamps order everything — sort first'),
    (10,16,"Source IP: the actor's return address"),
    (16,22,'Status codes: 200s lie, 401s confess, 500s scream'),
    (22,26,'User agents rat out the scanning tools')]),
 # --- dod-8140
 V(BOOTCAMP_K['dod'], 'dod', 'dod-categories', '8140 Workforce Categories',
   'the DoD maps every cyber job', 'bbg', scene_dod_categories,
   'DoD 8140 maps the cyber workforce into categories — operate and maintain, protect and defend, analyze, and more. Every billet has a work role; every work role has qualification requirements.',
   [(4,10,'Operate & maintain: keep the networks running'),
    (10,16,'Protect & defend: the SOC and incident responders'),
    (16,22,'Analyze: forensics, intel, exploitation analysis'),
    (22,26,'Every billet maps to a work role — no exceptions')]),
 V(BOOTCAMP_K['dod'], 'dod', 'dod-qualify', 'Qualification Levels: The Ladder',
   'certification plus clearance plus training', 'bbg', scene_dod_qualify,
   '8140 qualification stacks in layers: baseline certification for the category, computing-environment training for the systems, and clearance for the mission. All three, or the billet stays empty.',
   [(4,10,'Baseline cert: Security+ and up, by category'),
    (10,16,'Environment training: the systems you will touch'),
    (16,22,"Clearance: the mission's trust requirement"),
    (22,26,'All three layers — or the billet stays empty')]),
 V(BOOTCAMP_K['dod'], 'dod', 'dod-path', 'The 8140 Qualification Journey',
   'from applicant to qualified', 'story', scene_dod_path,
   'The journey: earn the baseline cert, complete the environment training, clear the background investigation, then continuous learning forever. Qualification is a status you maintain, not a trophy you keep.',
   [(4,10,'Earn the baseline cert — Security+ opens the door'),
    (10,16,'Environment training — the systems you will defend'),
    (16,22,'Background investigation — trust, verified'),
    (22,26,'Continuous learning — qualification is maintained, not kept')]),
 # --- nice-framework
 V(BOOTCAMP_K['nice'], 'nice', 'nice-categories', 'NICE: Seven Categories',
   'the common language of cyber work', 'bbg', scene_nice_categories,
   "The NICE Framework's seven categories: secure provisioning, operate and maintain, oversee and govern, protect and defend, analyze, collect and operate, investigate. The common language of cyber work — speak it in interviews.",
   [(4,10,'Securely provision: build it right from the start'),
    (10,16,'Operate & maintain · oversee & govern'),
    (16,22,"Protect & defend: the blue team's home"),
    (22,26,'Analyze, collect, investigate: the intel pipeline')]),
 V(BOOTCAMP_K['nice'], 'nice', 'nice-ksa', 'KSAs: Knowledge, Skills, Abilities',
   'the job description, decomposed', '3b1b', scene_nice_ksa,
   'NICE decomposes every work role into KSAs — knowledge you hold, skills you perform, abilities you bring. The job description is just a KSA shopping list; match yours to theirs.',
   [(4,10,'Knowledge: what you know — protocols, threats, law'),
    (10,16,'Skills: what you do — analyze, configure, hunt'),
    (16,22,'Abilities: what you bring — judgment under pressure'),
    (22,26,'The posting is a KSA shopping list — match yours')]),
 V(BOOTCAMP_K['nice'], 'nice', 'nice-roles', 'Work Roles: The Career Map',
   'fifty-two roles, one map', 'bbg', scene_nice_roles,
   'Fifty-two NICE work roles form the career map: cyber defense analyst here, vulnerability analyst there, the forensics path branching off. Pick your node, then collect its KSAs deliberately.',
   [(4,10,"Cyber defense analyst: the SOC's front line"),
    (10,16,'Vulnerability analyst: find it before they do'),
    (16,22,'Forensics: the investigate branch'),
    (22,26,'Pick your node — then collect its KSAs')]),
 # --- nsa-codebreaker
 V(BOOTCAMP_K['nsa'], 'nsa', 'nsa-rsa', 'RSA: Math as Armor',
   'multiplying is easy — factoring is not', '3b1b', scene_nsa_rsa,
   'RSA: pick two primes, multiply for the public modulus, and the private key hides in the factorization. Multiplying is easy — factoring a 2048-bit product is the armor.',
   [(4,10,'Two primes: p and q — keep them secret'),
    (10,16,'Modulus n = p × q — publish it freely'),
    (16,22,'Encryption is modular exponentiation — fast'),
    (22,26,'Breaking it means factoring n — infeasible at 2048 bits')]),
 V(BOOTCAMP_K['nsa'], 'nsa', 'nsa-puzzle', 'The Codebreaker Grid',
   'every solved cell constrains the rest', 'primer', scene_nsa_puzzle,
   'A codebreaking grid: each solved cell constrains its neighbors, frequency analysis fills the common letters, and the crib — the guessed word — cracks the row open. Patience plus pattern.',
   [(4,10,'Frequency analysis: E fills first, always'),
    (10,16,'The crib: a guessed word cracks the row'),
    (16,22,'Every solved cell constrains its neighbors'),
    (22,26,'Patience plus pattern — that is the whole game')]),
 V(BOOTCAMP_K['nsa'], 'nsa', 'nsa-pcap', 'Reading Packets in 100 Seconds',
   'follow the stream, not the packets', 'fireship', scene_nsa_pcap,
   'Packet analysis: filter the noise, follow the TCP stream, and the session reassembles itself — credentials, commands, exfiltration. Follow the stream, not the packets.',
   [(4,10,'Filter first — the noise outnumbers signal 1000:1'),
    (10,16,'Follow the TCP stream — sessions reassemble'),
    (16,22,'Flags tell the story: SYN, SYN-ACK, secrets'),
    (22,26,'Credentials in cleartext — the eternal sin')]),
 # --- pentest
 V(BOOTCAMP_K['pt'], 'pt', 'pt-phases', 'The Five Phases',
   'get permission first — always', 'bbg', scene_pt_phases,
   'Pentest phases: recon, scanning, exploitation, post-exploitation, reporting. Written permission first — always — and the report is the real deliverable; the shells are just evidence.',
   [(4,10,'Recon: map the target without touching it'),
    (10,16,'Scanning: enumerate every open door'),
    (16,22,'Exploitation: prove it — carefully, in scope'),
    (22,26,'Post-exploitation + reporting: the report is the product')]),
 V(BOOTCAMP_K['pt'], 'pt', 'pt-nmap', 'Nmap in 100 Seconds',
   'scan like you own it — because you do', 'fireship', scene_pt_nmap,
   'Nmap: SYN scan the top ports, version-detect the services, script the vulnerabilities — all in scope, all authorized. Scan like you own it, because this time you do.',
   [(4,10,'SYN scan: half-open, fast, quiet-ish'),
    (10,16,'Version detection: the banner tells the vintage'),
    (16,22,'Scripts: vuln checks without the exploit'),
    (22,26,'Authorized and in scope — the difference between test and crime')]),
 V(BOOTCAMP_K['pt'], 'pt', 'pt-privesc', 'Privilege Escalation Path',
   'from www-data to root in four hops', 'primer', scene_pt_privesc,
   'The privesc path: land as a low user, enumerate SUID binaries, find the misconfigured service, ride it to root. Enumeration before exploitation — the path is always in the misconfigurations.',
   [(4,10,'Land as www-data — the foothold'),
    (10,16,'Enumerate: SUID binaries, sudo rights, cron jobs'),
    (16,22,'Find the misconfiguration — it is always there'),
    (22,26,'Ride it to root — then document, do not linger')]),
 # --- sc-200
 V(BOOTCAMP_K['sc200'], 'sc200', 'sc200-sentinel', 'Sentinel: The Cloud SIEM',
   'connectors in, incidents out', 'bbg', scene_sc200_sentinel,
   'Microsoft Sentinel: data connectors stream everything in, analytics rules correlate, incidents queue for analysts, playbooks respond automatically. Connectors in, incidents out.',
   [(4,10,'Connectors: Defender, Entra, firewalls — all streaming'),
    (10,16,'Analytics rules: the correlation logic'),
    (16,22,'Incidents: queued, scored, assigned'),
    (22,26,'Playbooks: SOAR responds while you sleep')]),
 V(BOOTCAMP_K['sc200'], 'sc200', 'sc200-kql', 'KQL in 100 Seconds',
   'pipe everything, summarize always', 'fireship', scene_sc200_kql,
   'KQL: take the table, filter the time window, summarize by the field that matters, sort the guilty to the top. Pipe everything, summarize always — the query is the investigation.',
   [(4,10,'The table first — SigninLogs, SecurityEvent'),
    (10,16,'where TimeGenerated > ago(1d) — bound the blast'),
    (16,22,'summarize count() by the suspicious field'),
    (22,26,'Sort descending — the guilty float up')]),
 V(BOOTCAMP_K['sc200'], 'sc200', 'sc200-playbook', 'SOAR Playbook: The Auto-Responder',
   'the machine does the boring parts', 'primer', scene_sc200_playbook,
   'A SOAR playbook: the alert fires, enrichment gathers context, the decision branches on severity, containment isolates the host, and the ticket documents everything. The machine does the boring parts at 3 AM.',
   [(4,10,'Alert fires — the trigger'),
    (10,16,'Enrich: who, what, where — automatically'),
    (16,22,'Branch on severity — low auto-closes, high pages'),
    (22,26,'Contain and ticket — the boring parts, automated')]),
 # --- sc-300
 V(BOOTCAMP_K['sc300'], 'sc300', 'sc300-identity', 'Identity: The New Perimeter',
   'verify explicitly, every time', 'bbg', scene_sc300_identity,
   'Identity layers: the user proves who they are, the device proves its health, the policy decides the risk, and access is granted per session — never trusted, always verified.',
   [(4,10,'User: MFA proves the human'),
    (10,16,'Device: compliance proves the endpoint'),
    (16,22,'Policy: Conditional Access weighs the risk'),
    (22,26,'Session: granted now, re-verified continuously')]),
 V(BOOTCAMP_K['sc300'], 'sc300', 'sc300-mfa', 'MFA: The 99.9% Fix',
   'one extra factor stops nearly everything', 'primer', scene_sc300_mfa,
   'The MFA flow: password first, then the push to the phone, approve, and the token issues. One extra factor blocks 99.9% of account attacks — phishing-resistant methods block the rest.',
   [(4,10,'Password: the thing you know — phishable'),
    (10,16,'Push to the phone: the thing you have'),
    (16,22,'Approve — 30 seconds, done'),
    (22,26,'99.9% of account attacks die here')]),
 V(BOOTCAMP_K['sc300'], 'sc300', 'sc300-ca', 'Conditional Access in 100 Seconds',
   'if this, then require that', 'fireship', scene_sc300_ca,
   'Conditional Access: if the user is risky or the device is unknown or the location is new — then require MFA, or block. If-this-then-that for identity, evaluated on every sign-in.',
   [(4,10,'Signals: user risk, device state, location'),
    (10,16,'Conditions: the if — risky sign-in, new country'),
    (16,22,'Controls: the then — require MFA, or block'),
    (22,26,'Evaluated every sign-in — no cached trust')]),
 # --- soc-analyst
 V(BOOTCAMP_K['soc'], 'soc', 'soc-triage', 'Alert Triage: The First Five Minutes',
   'every alert gets a verdict', 'bbg', scene_soc_triage,
   'Alert triage: validate it is real, scope how far it spread, prioritize by business impact, then escalate or close. Every alert gets a verdict in five minutes — the queue never sleeps.',
   [(4,10,'Validate: real or noise — check the source'),
    (10,16,'Scope: one host or fifty — count the blast'),
    (16,22,'Prioritize: business impact sets the order'),
    (22,26,'Verdict in five minutes — escalate or close')]),
 V(BOOTCAMP_K['soc'], 'soc', 'soc-escalation', 'The Escalation Ladder',
   'know when to pull the cord', 'story', scene_soc_escalation,
   'The escalation ladder: L1 triages, L2 investigates deeply, IR takes the confirmed breach, and the execs get the business-impact briefing. Know when to pull the cord — escalation is a skill, not a failure.',
   [(4,10,'L1: triage and the first verdict'),
    (10,16,"L2: deep investigation — the hunter's shift"),
    (16,22,'IR: confirmed breach — the team assembles'),
    (22,26,'Execs: business impact, plain language')]),
 V(BOOTCAMP_K['soc'], 'soc', 'soc-ioc', 'IOC Hunting: The Grid Search',
   'one indicator is a clue — ten is a campaign', 'primer', scene_soc_ioc,
   'IOC hunting: sweep the grid of endpoints for the hash, the domain, the IP — one hit is a clue, ten is a campaign. Hunt with the indicator, then hunt for its friends.',
   [(4,10,"Hashes: the malware's fingerprints"),
    (10,16,'Domains and IPs: the infrastructure'),
    (16,22,'One hit is a clue — ten is a campaign'),
    (22,26,'Pivot: every IOC has friends — find them')]),
 # --- fde-training
 V(BOOTCAMP_K['fde'], 'fde', 'fde-layers', 'Full Disk Encryption Layers',
   'the data rests encrypted', 'bbg', scene_fde_layers,
   'FDE layers: the volume encrypted at rest, the key sealed in the TPM, the PIN unlocking the key, recovery keys guarding the worst day. Data rests encrypted — theft gets hardware, not data.',
   [(4,10,'Volume: AES-XTS encrypts every sector'),
    (10,16,'TPM: the key sealed to the hardware'),
    (16,22,'PIN: the human unlocks the key'),
    (22,26,'Recovery key: the worst-day insurance')]),
 V(BOOTCAMP_K['fde'], 'fde', 'fde-tpm', 'TPM Unlock: The Boot Handshake',
   'the chip vouches for the boot', 'primer', scene_fde_tpm,
   'The TPM unlock flow: measure the boot, compare against sealed values, release the key only if the boot is clean. The chip vouches for the boot — tamper and the key stays locked.',
   [(4,10,'Measure: hash every boot stage'),
    (10,16,'Compare: sealed values must match'),
    (16,22,'Release: key only on a clean boot'),
    (22,26,'Tamper and the key stays locked — by design')]),
 V(BOOTCAMP_K['fde'], 'fde', 'fde-recovery', 'The Lost PIN',
   'the recovery key is the spare tire', 'story', scene_fde_recovery,
   'The lost-PIN drill: user locked out, identity verified, recovery key retrieved from escrow, volume unlocked, new PIN set. The recovery key is the spare tire — escrow it before you need it.',
   [(4,10,'Locked out: the PIN is gone — breathe'),
    (10,16,'Verify identity — the key guards data, not feelings'),
    (16,22,'Retrieve from escrow — this is why it exists'),
    (22,26,'Unlock, set a new PIN — document the lesson')]),
 # --- hackers-arise
 V(BOOTCAMP_K['ha'], 'ha', 'ha-recon', 'Recon Commands in 100 Seconds',
   'enumerate everything, touch nothing', 'fireship', scene_ha_recon,
   'Recon: whois the domain, dig the DNS, harvest subdomains, fingerprint the services — enumerate everything, touch nothing. The quieter the recon, the louder the findings.',
   [(4,10,"whois: who owns the target's name"),
    (10,16,'dig: the DNS tells the infrastructure story'),
    (16,22,'Subdomain harvest: the forgotten dev servers'),
    (22,26,'Fingerprint: versions are vulnerabilities wearing nametags')]),
 V(BOOTCAMP_K['ha'], 'ha', 'ha-wifi', 'WiFi Attack Chain',
   'the handshake is the prize', 'primer', scene_ha_wifi,
   'The WiFi chain: monitor mode on, capture the handshake, crack it offline, and you own the network — on YOUR lab network, with written permission. The handshake is the prize; the lab is the boundary.',
   [(4,10,'Monitor mode: listen to everything'),
    (10,16,'Capture the 4-way handshake — the prize'),
    (16,22,'Crack offline: dictionary vs the handshake'),
    (22,26,'Your lab, your permission — the boundary is the point')]),
 V(BOOTCAMP_K['ha'], 'ha', 'ha-path', 'From Script Kiddie to Pro',
   'curiosity plus discipline equals career', 'story', scene_ha_path,
   'The path: curiosity in the lab, fundamentals before tools, certifications that prove it, then the first junior role. Curiosity plus discipline equals career — the tools are the easy part.',
   [(4,10,'Curiosity: the lab, the questions, the 2 AM rabbit holes'),
    (10,16,'Fundamentals: networking and Linux before the tools'),
    (16,22,'Proof: certs that hiring managers recognize'),
    (22,26,'The first role: junior analyst, real tickets')]),
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
