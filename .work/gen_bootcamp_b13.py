"""Bootcamp video Phase 2, Batch B13 (FINAL): 2 bootcamps x 3 videos = 6 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: bbg / fireship / story / primer / 3b1b. Original animations only.
Modeled on gen_bootcamp_b11.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.
Collision pre-check against docs/assets/videos/ ran clean for all six names.

Batch B13 bootcamps: roles-library, study-protocol (the last two without video).
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
# roles-library (bbg x1 + fireship x1 + story x1)
def scene_rl_skill(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Skill Mapping: The Career Grid', CYAN)
    _items = [('python', 0.85, '85%', CYAN), ('cloud', 0.70, '70%', GREEN),
              ('data', 0.75, '75%', TEAL), ('security', 0.60, '60%', YELLOW),
              ('leadership', 0.55, '55%', ORANGE)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 205 + _i * 76
        _here = t > 5 + _i * 2.0
        _f = clamp((t - 5 - _i * 2.0) / 2.0) * _fr if _here else 0.0
        bar(dr, 420, _y, 500, 36, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'the grid turns vague experience into evidence', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'map the skill, then target the gaps', font(F_SANS, 24), DIM, anchor="mm")
def scene_rl_ladder(t, dr, img):
    _acc = ACCENTS['fireship']
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['fireship'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Role Ladder', font(F_BOLD, 40), _acc, anchor="mm")
    txt(dr, (W // 2, 118), 'every level has a price and a skill check', font(F_SANS, 24), DIM, anchor="mm")
    _levels = [('L1 support', '$55k'), ('L2 analyst', '$80k'), ('L3 senior', '$120k'), ('L4 architect', '$170k')]
    _n = len(_levels)
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0 = 190
    _bh = 92
    _gap = 18
    for _i, (_lb, _py) in enumerate(_levels):
        _y = _y0 + _i * (_bh + _gap)
        _on = _i < _lit
        glow_box(dr, [380, _y, 900, _y + _bh], _acc if _on else (40, 40, 60))
        dr.rectangle([380, _y, 900, _y + _bh], fill=(12, 18, 32),
                     outline=_acc if _on else DIM, width=3 if _on else 2)
        txt(dr, (400, _y + _bh // 2), _lb, font(F_BOLD, 24),
            _acc if _on else DIM, anchor="lm")
        if _on:
            txt(dr, (880, _y + _bh // 2), _py, font(F_MONOB, 24), GREEN, anchor="rm")
        if _i < _n - 1:
            arrow(dr, 640, _y + _bh, 640, _y + _bh + _gap, GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 630), 'climb by skills, not by years', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 672), 'the library maps every rung to its skills', font(F_SANS, 24), DIM, anchor="mm")
def scene_rl_pivot(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Pivot: Changing Careers', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'transfer is faster than starting over', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('inventory: skills that transfer', 5), ('gap: the 20% that is new', 9),
           ('bridge: the project that proves it', 13), ('network: warm intros beat portals', 17),
           ('land: the first role at the new level', 21)]
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
        txt(dr, (W // 2, 624), 'transfer is faster than starting over', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'a pivot is a portfolio move — show the bridge work', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# study-protocol (primer x1 + 3b1b x1 + bbg x1)
def scene_sp_spaced(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Spaced Repetition: The Schedule', CYAN)
    _pts = [(140, 340), (360, 340), (580, 340), (800, 340), (1020, 340)]
    _labels = ('day 1', 'day 3', 'day 7', 'day 14', 'day 30')
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
        txt(dr, (W // 2, 560), 'review right before you would forget', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 612), 'the intervals grow as memory strengthens', font(F_SANS, 24), DIM, anchor="mm")
def scene_sp_forgetting(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Forgetting Curve', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'R = e^(-t/S) — retention decays without review', font(F_MONO, 24), DIM, anchor="mm")
    _ax, _ay, _aw, _ah = 200, 200, 880, 380
    dr.rectangle([_ax, _ay, _ax + _aw, _ay + _ah], fill=(8, 12, 24), outline=DIM, width=2)
    txt(dr, (_ax - 14, _ay), '100%', font(F_MONO, 20), DIM, anchor="rm")
    txt(dr, (_ax - 14, _ay + _ah), '0%', font(F_MONO, 20), DIM, anchor="rm")
    txt(dr, (_ax + _aw // 2, _ay + _ah + 34), 'time →', font(F_MONO, 20), DIM, anchor="mm")
    _p = clamp((t - 5) / 13)
    _nseg = 120
    _cut = max(2, int(_nseg * _p))
    _red_pts, _grn_pts = [], []
    for _j in range(_cut):
        _x = _ax + (_j / _nseg) * _aw
        _tt = (_j / _nseg)
        _r_red = math.exp(-_tt * 3.0)
        _red_pts.append((_x, _ay + _ah * (1 - _r_red)))
        # green: review bumps at day 1, 3, 7 (fractions 0.15, 0.35, 0.62)
        _bumps = [0.15, 0.35, 0.62]
        _since = 0.0
        _last = 0.0
        for _b in _bumps:
            if _tt >= _b:
                _last = _b
            else:
                break
        _since = _tt - _last
        _r_grn = max(0.0, 1.0 - _since * 2.2)
        _grn_pts.append((_x, _ay + _ah * (1 - _r_grn)))
    if len(_red_pts) >= 2:
        dr.line(_red_pts, fill=RED, width=4)
        dr.line(_grn_pts, fill=GREEN, width=4)
    txt(dr, (_ax + _aw + 18, _ay + 20), 'no review', font(F_SANS, 20), RED, anchor="lm")
    txt(dr, (_ax + _aw + 18, _ay + 52), 'spaced review', font(F_SANS, 20), GREEN, anchor="lm")
    if t > 19:
        txt(dr, (W // 2, 636), 'each review resets the clock higher', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 680), 'ebbinghaus measured it — the protocol beats it', font(F_SANS, 24), DIM, anchor="mm")
def scene_sp_active(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Active Recall: The Retrieval Loop', CYAN)
    _boxes = ('read', 'close the book', 'retrieve', 'check')
    _n = len(_boxes)
    _w = 240
    _gap = 28
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 22), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 15
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 30), _line, font(F_BOLD, 22),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'the test is the studying', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'rereading feels fluent — retrieval builds memory', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'rl': 'roles-library',
    'sp': 'study-protocol',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'rl': 'ROLES LIBRARY · Career Mapping',
    'sp': 'STUDY PROTOCOL · Learn Faster',
}

VIDEOS = [
 # --- roles-library
 V(BOOTCAMP_K['rl'], 'rl', 'rl-skill-mapping', 'Skill Mapping: The Career Grid',
   'the grid turns experience into evidence', 'bbg', scene_rl_skill,
   'Skill mapping: inventory your skills, rate them honestly against market demand, and let the gaps write your study plan. The grid turns vague experience into evidence.',
   [(4,10,'Inventory: list every skill you actually have'),
    (10,16,'Rate: honest levels — 1 to 5, no charity'),
    (16,22,'Compare: market demand vs your grid'),
    (22,26,'Target: the gaps become the study plan')]),
 V(BOOTCAMP_K['rl'], 'rl', 'rl-role-ladder', 'The Role Ladder',
   'every level has a skill check', 'fireship', scene_rl_ladder,
   'The ladder: support to analyst to senior to architect — every rung carries a comp band and a skill check. Climb by skills, not by years: the library maps each rung.',
   [(4,10,'L1 support: triage and tickets — the foundation'),
    (10,16,'L2 analyst: own the problem — diagnosis'),
    (16,22,'L3 senior: own the system — design'),
    (22,26,'L4 architect: own the direction — strategy')]),
 V(BOOTCAMP_K['rl'], 'rl', 'rl-pivot', 'The Pivot: Changing Careers',
   'transfer is faster than starting over', 'story', scene_rl_pivot,
   'The career pivot: eighty percent of your skills transfer — map what carries over, close the twenty-percent gap with one bridge project, and let warm intros beat the portals.',
   [(4,10,'Inventory: the skills that transfer'),
    (10,16,'Gap: the 20% that is genuinely new'),
    (16,22,'Bridge: one project that proves the new skill'),
    (22,26,'Land: the first role at the new level')]),
 # --- study-protocol
 V(BOOTCAMP_K['sp'], 'sp', 'sp-spaced-repetition', 'Spaced Repetition: The Schedule',
   'review right before you would forget', 'primer', scene_sp_spaced,
   'Spaced repetition: review on day 1, day 3, day 7, day 14, day 30 — right before you would forget. The intervals grow as memory strengthens; the schedule does the compounding.',
   [(4,10,'Day 1: the first review — the curve is steep'),
    (10,16,'Days 3 and 7: the intervals stretch'),
    (16,22,'Days 14 and 30: long memory takes hold'),
    (22,26,'The intervals grow as memory strengthens')]),
 V(BOOTCAMP_K['sp'], 'sp', 'sp-forgetting-curve', 'The Forgetting Curve',
   'each review resets the clock higher', '3b1b', scene_sp_forgetting,
   'The forgetting curve: retention decays exponentially without review — R = e^(-t/S). Each spaced review resets the clock higher. Ebbinghaus measured it; the protocol beats it.',
   [(4,10,'Retention decays: R = e^(-t/S) — the curve'),
    (10,16,'No review: the red line — memory drains'),
    (16,22,'Spaced review: the green line — each reset higher'),
    (22,26,'The protocol beats the curve — that is the whole game')]),
 V(BOOTCAMP_K['sp'], 'sp', 'sp-active-recall', 'Active Recall: The Retrieval Loop',
   'the test is the studying', 'bbg', scene_sp_active,
   'Active recall: read, close the book, retrieve from memory, then check. The test is the studying — retrieval builds the memory that rereading only pretends to.',
   [(4,10,'Read: one section — actively, once'),
    (10,16,'Close: the book shuts — no peeking'),
    (16,22,'Retrieve: write what you remember — from nothing'),
    (22,26,'Check: the gaps you found are the study plan')]),
]
# ============================================================ render loop (mirrors gen_bootcamp_b11)
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
