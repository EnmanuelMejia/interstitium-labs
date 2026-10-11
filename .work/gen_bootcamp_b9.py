"""Bootcamp video Phase 2, Batch B9: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b5.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.

Batch B9 bootcamps (Data/AI):
  ai-lab, ai-product, alan-turing, il12-ai-engineering, llm-engineering, ml-defense, nvidia-ai, quantum, dp-203, mongodb, oracle-db, oracle-sql
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
# ai-lab (bbg x1 + 3b1b x1 + primer x1)
def scene_ailab_experiment(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Experiment Tracking: Science It', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'no tracking, no science', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'params × data × code = run', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('runs logged', 342, '%d'), ('reproduced', 341, '%d'), ('lost', 1, '%d')]
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
        txt(dr, (W // 2, 540), 'no tracking, no science', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the data version is the silent variable', font(F_SANS, 24), DIM, anchor="mm")
def scene_ailab_eval(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Eval Metrics: Beyond Accuracy', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'accuracy lies on imbalanced data', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('accuracy', 0.95, '95%', YELLOW), ('precision', 0.72, '72%', ORANGE), ('recall', 0.88, '88%', GREEN), ('F1', 0.79, '0.79', TEAL)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'accuracy lies on imbalanced data', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'the metric must match the cost of being wrong', font(F_SANS, 24), DIM, anchor="mm")
def scene_ailab_rag(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'RAG: Retrieval-Augmented Generation', CYAN)
    _boxes = ('chunk', 'embed', 'retrieve', 'generate')
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
        txt(dr, (W // 2, 500), 'ground the model in your data', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'chunking strategy is the hidden hyperparameter', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# ai-product (fireship x1 + 3b1b x1 + story x1)
def scene_aiprod_discovery(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Discovery to Launch', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'fall in love with the problem', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('discovery: 20 user conversations', 5), ('prototype: riskiest assumption tested', 9), ('validation: users pay or it pivots', 13), ('launch: instrumented from day one', 17), ('iterate: the roadmap is a hypothesis', 21)]
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
        txt(dr, (W // 2, 624), 'fall in love with the problem', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the demo is not the validation', font(F_SERIF, 24), DIM, anchor="mm")
def scene_aiprod_metrics(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'North Star Metrics', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'one metric to rule the roadmap', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'value = f(inputs) · guardrails hold', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('weekly value moments', 8400, '%d'), ('activation', 62, '%d%%'), ('churn', 4, '%d%%')]
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
        txt(dr, (W // 2, 540), 'one metric to rule the roadmap', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'if everything is a priority, nothing is', font(F_SANS, 24), DIM, anchor="mm")
def scene_aiprod_prompt(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Prompt Templates in 100 Seconds', MAGENTA)
    _lns = [('system: You are a precise analyst.', (200, 200, 255)), ('user: Summarize {{doc}} in 3 bullets.', YELLOW), ('examples: [{{ex1}}, {{ex2}}]  # few-shot', (200, 200, 255)), ('tests: [assert bullets == 3]', GREEN), ('# version it — prompts regress', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'prompt.j2', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'prompts are code — version them', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'untested prompts are just wishes', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# alan-turing (primer x2 + story x1)
def scene_turing_machine(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'The Turing Machine: Tape and Head', CYAN)
    _rows, _cols = 3, 12
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — tape cells visited by the head' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'simple enough to be universal', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'your laptop is this machine at a billion hertz', font(F_SANS, 24), DIM, anchor="mm")
def scene_turing_test(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Imitation Game', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'can machines think — or only imitate', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('1950: the paper that started it', 5), ('the game: fool the judge via text', 9), ('decades of philosophy: what is thinking', 13), ('2026: chatbots pass narrow versions', 17), ('the argument continues', 21)]
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
        txt(dr, (W // 2, 624), 'can machines think — or only imitate', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the test measures imitation, not understanding', font(F_SERIF, 24), DIM, anchor="mm")
def scene_turing_bombe(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'The Bombe: Breaking Enigma', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('intercept', 'crib', 'bombe runs', 'align', 'read key')
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
        txt(dr, (W // 2, 540), 'the crib makes the impossible routine', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'cribs plus machines beat math alone', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# il12-ai-engineering (bbg x1 + 3b1b x1 + primer x1)
def scene_il12_pipeline(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The AI Engineering Pipeline', CYAN)
    _boxes = ('data', 'train', 'eval', 'serve', 'monitor')
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
        txt(dr, (W // 2, 500), 'from notebook to production', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the evals are the gate — no score, no ship', font(F_SANS, 24), DIM, anchor="mm")
def scene_il12_attention(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Attention: The Math That Ate the World', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'queries, keys, values — weighted', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'Attention(Q,K,V) = softmax(QKᵀ/√d)V', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('heads', 12, '%d'), ('dim', 768, '%d'), ('params', 175, '%dB')]
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
        txt(dr, (W // 2, 540), 'queries, keys, values — weighted', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the scaling factor keeps gradients alive', font(F_SANS, 24), DIM, anchor="mm")
def scene_il12_evalharness(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Eval Harness: Trust, Then Ship', CYAN)
    _lp = ('regressions caught in CI', 'scores tracked per release', 'ship with evidence')
    _rp = ('works on my prompt', 'regressions found by users', 'ship on vibes')
    _nL = int(clamp((t - 5) / 6) * len(_lp))
    _nR = int(clamp((t - 12) / 6) * len(_rp))
    dr.rectangle([120, 190, 600, 470], fill=(16, 16, 30), outline=GREEN, width=3)
    txt(dr, (360, 232), 'WITH HARNESS', font(F_BOLD, 26), GREEN, anchor="mm")
    for _i in range(_nL):
        txt(dr, (160, 290 + _i * 46), "\u2713 " + _lp[_i], font(F_SANS, 22), GREEN, anchor="lm")
    dr.rectangle([680, 190, 1160, 470], fill=(16, 16, 30), outline=RED, width=3)
    txt(dr, (920, 232), 'WITHOUT', font(F_BOLD, 26), RED, anchor="mm")
    for _i in range(_nR):
        txt(dr, (720, 290 + _i * 46), "\u2717 " + _rp[_i], font(F_SANS, 22), RED, anchor="lm")
    if t > 20:
        dr.rectangle([300, 520, 980, 592], fill=(12, 24, 12), outline=GOLD, width=3)
        txt(dr, (W // 2, 556), 'evidence beats vibes — harness every model', font(F_BOLD, 25), GOLD, anchor="mm")
# ============================================================
# llm-engineering (bbg x1 + 3b1b x1 + primer x1)
def scene_llm_context(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Context Windows: The Growing Memory', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'attention is quadratic — memory is the bill', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'cost ∝ n²', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('tokens 2020', 2048, '%d'), ('tokens 2026', 1000000, '%d'), ('cost multiple', 16, '%dx')]
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
        txt(dr, (W // 2, 540), 'attention is quadratic — memory is the bill', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'long context is not long memory — test the middle', font(F_SANS, 24), DIM, anchor="mm")
def scene_llm_finetune(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Fine-Tuning: Teaching Manners', CYAN)
    _boxes = ('base model', 'SFT pairs', 'preferences', 'evals')
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
        txt(dr, (W // 2, 500), 'pretraining teaches, tuning civilizes', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'garbage pairs teach garbage manners — curate', font(F_SANS, 24), DIM, anchor="mm")
def scene_llm_serve(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Inference Serving: Tokens per Second', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('request', 'prefill', 'decode', 'stream', 'done')
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
        txt(dr, (W // 2, 540), 'prefill, then decode', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the two phases have different physics — optimize both', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# ml-defense (3b1b x1 + primer x2)
def scene_mldef_adversarial(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Adversarial Examples: The Invisible Ink', CYAN)
    _lp = ('invisible perturbation', '99% wrong confidence', 'transfers across models')
    _rp = ('adversarial training', 'certified bounds', 'input sanitization')
    _nL = int(clamp((t - 5) / 6) * len(_lp))
    _nR = int(clamp((t - 12) / 6) * len(_rp))
    dr.rectangle([120, 190, 600, 470], fill=(16, 16, 30), outline=GREEN, width=3)
    txt(dr, (360, 232), 'ATTACK', font(F_BOLD, 26), GREEN, anchor="mm")
    for _i in range(_nL):
        txt(dr, (160, 290 + _i * 46), "\u2713 " + _lp[_i], font(F_SANS, 22), GREEN, anchor="lm")
    dr.rectangle([680, 190, 1160, 470], fill=(16, 16, 30), outline=RED, width=3)
    txt(dr, (920, 232), 'DEFENSE', font(F_BOLD, 26), RED, anchor="mm")
    for _i in range(_nR):
        txt(dr, (720, 290 + _i * 46), "\u2717 " + _rp[_i], font(F_SANS, 22), RED, anchor="lm")
    if t > 20:
        dr.rectangle([300, 520, 980, 592], fill=(12, 24, 12), outline=GOLD, width=3)
        txt(dr, (W // 2, 556), 'vaccinate the model — train on attacks', font(F_BOLD, 25), GOLD, anchor="mm")
def scene_mldef_poison(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'Data Poisoning: The Slow Betrayal', CYAN)
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — training rows inspected — 3 poisoned' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'a few bad rows rot the whole model', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'provenance is the defense — audit the pipeline', font(F_SANS, 24), DIM, anchor="mm")
def scene_mldef_robust(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Robustness Metrics: Measuring Armor', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'accuracy under fire', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'robust acc ≤ clean acc — always', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('clean acc', 94, '%d%%'), ('robust acc', 61, '%d%%'), ('certified', 38, '%d%%')]
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
        txt(dr, (W // 2, 540), 'accuracy under fire', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the fair-weather number is a brochure', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# nvidia-ai (bbg x1 + fireship x1 + 3b1b x1)
def scene_nva_stack(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The CUDA Stack: Silicon to Model', CYAN)
    _layers = ('framework', 'cuDNN / NCCL', 'CUDA', 'GPU silicon')
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
        txt(dr, (W // 2, 612), 'every layer exists to feed the GPUs', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'utilization is the religion — profile everything', font(F_SANS, 24), DIM, anchor="mm")
def scene_nva_flops(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'FLOPS: Counting the Lightning', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'training is measured in petaflop-days', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), '1 petaflop-day ≈ $50k of compute', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('per GPU', 1000, '%d TF'), ('cluster', 50, '%d PF'), ('run cost', 120, '%d PF-days')]
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
        txt(dr, (W // 2, 540), 'training is measured in petaflop-days', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'precision is a dial — turn it for speed', font(F_SANS, 24), DIM, anchor="mm")
def scene_nva_nemo(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'NeMo Training in 100 Seconds', MAGENTA)
    _lns = [('import nemo.collections.nlp as nlp', (200, 200, 255)), ('model = nlp.models.MegatronGPTModel(cfg)', YELLOW), ('trainer = pl.Trainer(gpus=8, precision=16)', GREEN), ('trainer.fit(model)  # 3 AM checkpointing on', (200, 200, 255)), ('# recipes over raw scripts', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'train.py', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'recipes, not raw scripts', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'checkpoint everything — GPUs fail at 3 AM', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# quantum (bbg x1 + 3b1b x1 + primer x1)
def scene_qm_qubit(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Qubits: 0 and 1, Simultaneously', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'superposition is the resource', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), '|ψ> = α|0> + β|1> · |α|²+|β|²=1', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('qubits', 1000, '%d'), ('states', 300, '%d digits'), ('coherence', 99, '%dµs')]
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
        txt(dr, (W // 2, 540), 'superposition is the resource', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'measurement collapses — choose wisely when', font(F_SANS, 24), DIM, anchor="mm")
def scene_qm_gates(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Quantum Gates: The Circuit', CYAN)
    _boxes = ('|0>', 'H gate', 'CNOT', 'measure')
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
        txt(dr, (W // 2, 500), 'gates rotate, entanglement correlates', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the circuit is the program — depth is the cost', font(F_SANS, 24), DIM, anchor="mm")
def scene_qm_shor(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, "Shor's Algorithm: RSA's Nightmare", CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('RSA-2048', 'QFT', 'period found', 'factors', 'migrate PQC')
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
        txt(dr, (W // 2, 540), 'factoring becomes tractable', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'harvest-now-decrypt-later is already happening', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# dp-203 (bbg x1 + fireship x1 + 3b1b x1)
def scene_dp203_synapse(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Synapse: The Analytics Hub', CYAN)
    _boxes = ('pipelines', 'spark', 'serverless SQL', 'data lake')
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
        txt(dr, (W // 2, 500), 'one workspace, every engine', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the lake is the center — engines orbit it', font(F_SANS, 24), DIM, anchor="mm")
def scene_dp203_spark(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'PySpark in 100 Seconds', MAGENTA)
    _lns = [("df = spark.read.parquet('abfss://lake/')", (200, 200, 255)), ('agg = df.filter(df.year == 2026)', YELLOW), ("         .groupBy('sku').sum('qty')", YELLOW), ("agg.write.mode('overwrite').parquet(out)", GREEN), ('# lazy until the write — then the DAG fires', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'etl.py', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'transformations lazy, actions eager', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'the DAG runs at the action — not before', font(F_SANS, 24), DIM, anchor="mm")
def scene_dp203_partition(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Partitioning: Divide and Conquer', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'partition by the filter, not the fantasy', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'scanned = total × selectivity', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('partitions', 365, '%d'), ('pruned', 364, '%d'), ('scanned', 1, '%d%%')]
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
        txt(dr, (W // 2, 540), 'partition by the filter, not the fantasy', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'pruning is free performance — design for it', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# mongodb (bbg x2 + fireship x1)
def scene_mdb_documents(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Documents: Data That Looks Like Code', CYAN)
    _layers = ('application', 'document', 'BSON types', 'storage engine')
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
        txt(dr, (W // 2, 612), 'embed what you read together', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'reference what grows unbounded', font(F_SANS, 24), DIM, anchor="mm")
def scene_mdb_agg(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Aggregation in 100 Seconds', MAGENTA)
    _lns = [('db.orders.aggregate([', (200, 200, 255)), ('  {$match: {year: 2026}},', YELLOW), ("  {$group: {_id: '$sku', total: {$sum: '$qty'}}},", YELLOW), ('  {$sort: {total: -1}}', (200, 200, 255)), ('])', (200, 200, 255)), ('# match → group → sort: the pipeline', GREEN)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'agg.js', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'a pipeline of stages', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'match first — the index thanks you', font(F_SANS, 24), DIM, anchor="mm")
def scene_mdb_replica(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Replica Sets: Elections Included', CYAN)
    _nodes = [('primary', 320, 280), ('sec-1', 560, 420), ('sec-2', 880, 420), ('arbiter', 1100, 280)]
    _edges = [(0, 1), (0, 2), (1, 2)]
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
        txt(dr, (W // 2, 560), 'the primary is elected, not appointed', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'majority wins — even numbers need an arbiter', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# oracle-db (bbg x2 + story x1)
def scene_odb_arch(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Oracle Architecture: SGA and Friends', CYAN)
    _boxes = ('SGA', 'PGA', 'DBWn', 'LGWR', 'CKPT')
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
        txt(dr, (W // 2, 500), 'memory structures plus processes', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'instance is memory — database is files', font(F_SANS, 24), DIM, anchor="mm")
def scene_odb_rac(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'RAC: One Database, Many Instances', CYAN)
    _nodes = [('node-1', 280, 280), ('node-2', 640, 280), ('node-3', 1000, 280), ('shared DB', 640, 520)]
    _edges = [(0, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3)]
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
        txt(dr, (W // 2, 560), 'one database, many instances', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'the interconnect is the heartbeat — protect it', font(F_SANS, 24), DIM, anchor="mm")
def scene_odb_rman(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'RMAN: The Backup Religion', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'backup, validate, restore — in that order', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('full backup Sunday 2 AM', 5), ('incremental nightly', 9), ('validate: corruption check', 13), ('restore rehearsal to sandbox', 17), ('document RTO/RPO proof', 21)]
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
        txt(dr, (W // 2, 624), 'backup, validate, restore — in that order', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'untested backups are decorative', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# oracle-sql (bbg x1 + fireship x1 + 3b1b x1)
def scene_osql_joins(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'JOINs in 100 Seconds', MAGENTA)
    _lns = [('SELECT c.name, o.total', (200, 200, 255)), ('FROM customers c', (200, 200, 255)), ('LEFT JOIN orders o', YELLOW), ('  ON o.cust_id = c.id', YELLOW), ('WHERE o.total > 100;', (200, 200, 255)), ('# LEFT keeps customers with no orders', GREEN)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'joins.sql', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'the ON clause is the relationship', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'filter in WHERE, relate in ON — or the outer join lies', font(F_SANS, 24), DIM, anchor="mm")
def scene_osql_window(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Window Functions: Rows That See', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'partition, order, frame', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'OVER (PARTITION · ORDER · FRAME)', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('partitions', 12, '%d'), ('rows seen', 48000, '%d'), ('self-joins', 0, '%d')]
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
        txt(dr, (W // 2, 540), 'partition, order, frame', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'no GROUP BY collapse — every row survives', font(F_SANS, 24), DIM, anchor="mm")
def scene_osql_explain(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Execution Plans: Read the Truth', CYAN)
    _boxes = ('parse', 'optimize', 'execute', 'fetch')
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
        txt(dr, (W // 2, 500), 'the plan is what actually runs', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'stale statistics lie — gather them', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'ailab': 'ai-lab',
    'aiprod': 'ai-product',
    'turing': 'alan-turing',
    'il12': 'il12-ai-engineering',
    'llm': 'llm-engineering',
    'mldef': 'ml-defense',
    'nva': 'nvidia-ai',
    'qm': 'quantum',
    'dp203': 'dp-203',
    'mdb': 'mongodb',
    'odb': 'oracle-db',
    'osql': 'oracle-sql',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'ailab': 'AI LAB · Applied Experiments',
    'aiprod': 'AI PRODUCT · Building with AI',
    'turing': 'TURING · Computing Origins',
    'il12': 'IL-12 · AI Engineering',
    'llm': 'LLM · LLM Engineering',
    'mldef': 'ML DEFENSE · Adversarial ML',
    'nva': 'NVIDIA · Accelerated AI',
    'qm': 'QUANTUM · Quantum Computing',
    'dp203': 'DP-203 · Azure Data Engineer',
    'mdb': 'MONGO · Document Database',
    'odb': 'ORACLE DB · Database Admin',
    'osql': 'ORACLE SQL · SQL Mastery',
}
VIDEOS = [
 # --- ai-lab
 V(BOOTCAMP_K['ailab'], 'ailab', 'ailab-experiment', 'Experiment Tracking: Science It',
   'no tracking, no science', 'primer', scene_ailab_experiment,
   'Experiment tracking: log the params, version the data, record the metrics — every run reproducible. No tracking, no science — just vibes and lost GPUs.',
   [(4,10,'Log params: the knobs you turned'),
    (10,16,'Version the data — the silent variable'),
    (16,22,'Record metrics: the scoreboard'),
    (22,26,'Reproduce any run — or it did not happen')]),
 V(BOOTCAMP_K['ailab'], 'ailab', 'ailab-eval', 'Eval Metrics: Beyond Accuracy',
   'accuracy lies on imbalanced data', '3b1b', scene_ailab_eval,
   'Eval metrics: accuracy lies on imbalanced data — precision, recall, F1, and the ROC curve tell the truth. Pick the metric that matches the cost of being wrong.',
   [(4,10,'Accuracy: the liar on imbalanced data'),
    (10,16,'Precision vs recall: the eternal tradeoff'),
    (16,22,'F1: the harmonic handshake'),
    (22,26,'Match the metric to the cost of error')]),
 V(BOOTCAMP_K['ailab'], 'ailab', 'ailab-rag', 'RAG: Retrieval-Augmented Generation',
   'ground the model in your data', 'bbg', scene_ailab_rag,
   'RAG: chunk the documents, embed them, retrieve the top-k for each query, and let the model answer with citations. Ground the model in your data — hallucinations hate receipts.',
   [(4,10,'Chunk + embed: your docs become vectors'),
    (10,16,'Retrieve top-k: the relevant passages surface'),
    (16,22,'Generate with context — citations attached'),
    (22,26,'Hallucinations hate receipts')]),
 # --- ai-product
 V(BOOTCAMP_K['aiprod'], 'aiprod', 'aiprod-discovery', 'Discovery to Launch',
   'fall in love with the problem', 'story', scene_aiprod_discovery,
   'The AI product journey: discover the real problem, prototype the risky parts, validate with users, then launch and instrument. Fall in love with the problem — not your solution.',
   [(4,10,'Discover: the problem behind the request'),
    (10,16,'Prototype the riskiest assumption first'),
    (16,22,'Validate: users, not demos, decide'),
    (22,26,'Launch + instrument — the learning starts')]),
 V(BOOTCAMP_K['aiprod'], 'aiprod', 'aiprod-metrics', 'North Star Metrics',
   'one metric to rule the roadmap', '3b1b', scene_aiprod_metrics,
   'North star metrics: one number capturing core value, input metrics the team moves, guardrails that must not break. One metric to rule the roadmap — vanity metrics need not apply.',
   [(4,10,'North star: the value moment, quantified'),
    (10,16,'Inputs: the levers the team actually moves'),
    (16,22,'Guardrails: what must never break'),
    (22,26,'Vanity metrics need not apply')]),
 V(BOOTCAMP_K['aiprod'], 'aiprod', 'aiprod-prompt', 'Prompt Templates in 100 Seconds',
   'prompts are code — version them', 'fireship', scene_aiprod_prompt,
   'Prompt templates: system role sets the persona, variables inject context, few-shot examples steer format, and tests pin the behavior. Prompts are code — version them like it.',
   [(4,10,'System: the persona and the rules'),
    (10,16,'Variables: context injected, not pasted'),
    (16,22,'Few-shot: examples steer the format'),
    (22,26,'Tests: pin behavior — prompts regress too')]),
 # --- alan-turing
 V(BOOTCAMP_K['turing'], 'turing', 'turing-machine', 'The Turing Machine: Tape and Head',
   'simple enough to be universal', 'primer', scene_turing_machine,
   'The Turing machine: an infinite tape, a read-write head, a table of rules — simple enough to be universal. Every computer is this machine, sped up a billion times.',
   [(4,10,'The tape: infinite memory, one symbol at a time'),
    (10,16,'The head: reads, writes, moves'),
    (16,22,'The table: rules for every state'),
    (22,26,'Simple enough to be universal — that is the point')]),
 V(BOOTCAMP_K['turing'], 'turing', 'turing-test', 'The Imitation Game',
   'can machines think — or only imitate', 'story', scene_turing_test,
   '1950: Turing asks whether machines can think and proposes the imitation game — a judge, a human, a machine. The test measures imitation, not understanding — and we are still arguing about it.',
   [(4,10,"1950: 'Computing Machinery and Intelligence'"),
    (10,16,'The game: judge, human, machine — text only'),
    (16,22,'Passing means indistinguishable — not understanding'),
    (22,26,'Seventy-six years later — still arguing')]),
 V(BOOTCAMP_K['turing'], 'turing', 'turing-bombe', 'The Bombe: Breaking Enigma',
   'the crib makes the impossible routine', 'primer', scene_turing_bombe,
   'The Bombe: feed it a crib — a guessed plaintext — and it tests rotor positions at machine speed until the circuits align. The crib makes the impossible routine.',
   [(4,10,'Enigma: billions of daily settings'),
    (10,16,"The crib: guessed plaintext — 'wetterbericht'"),
    (16,22,'The Bombe tests rotors at machine speed'),
    (22,26,"Alignment: the circuits light up — read the day's key")]),
 # --- il12-ai-engineering
 V(BOOTCAMP_K['il12'], 'il12', 'il12-pipeline', 'The AI Engineering Pipeline',
   'from notebook to production', 'bbg', scene_il12_pipeline,
   'The AI engineering pipeline: data pipelines feed training, evals gate promotion, serving scales inference, monitoring watches for drift. From notebook to production — the evals are the gate.',
   [(4,10,'Data pipelines: versioned, tested inputs'),
    (10,16,'Training: tracked, reproducible runs'),
    (16,22,'Evals gate promotion — no score, no ship'),
    (22,26,'Serving + monitoring: inference with a watchtower')]),
 V(BOOTCAMP_K['il12'], 'il12', 'il12-attention', 'Attention: The Math That Ate the World',
   'queries, keys, values — weighted', '3b1b', scene_il12_attention,
   'Attention: queries meet keys, softmax weighs the matches, values mix by weight. QK^T over sqrt(d), softmax, times V — the equation that ate the world.',
   [(4,10,'Queries ask — keys advertise'),
    (10,16,'Scores: QK^T / sqrt(d) — scaled similarity'),
    (16,22,'Softmax: the weights sum to one'),
    (22,26,'Values mix by weight — context assembled')]),
 V(BOOTCAMP_K['il12'], 'il12', 'il12-evalharness', 'Eval Harness: Trust, Then Ship',
   'vibes are not a metric', 'primer', scene_il12_evalharness,
   'Eval harness: golden datasets with known answers, automated scoring on every change, human review for the edge cases. Vibes are not a metric — the harness decides what ships.',
   [(4,10,'Golden sets: known answers, versioned'),
    (10,16,'Auto-score every change — regressions caught'),
    (16,22,'Human review: the edge cases need eyes'),
    (22,26,'The harness decides — not the demo')]),
 # --- llm-engineering
 V(BOOTCAMP_K['llm'], 'llm', 'llm-context', 'Context Windows: The Growing Memory',
   'attention is quadratic — memory is the bill', '3b1b', scene_llm_context,
   'Context windows grew from 2K to millions of tokens — but attention is quadratic, so every doubling costs four times the compute. Memory is the bill; retrieval is the discount.',
   [(4,10,'2K: the early days — a page or two'),
    (10,16,'128K: whole codebases in one prompt'),
    (16,22,'Millions: the haystack era'),
    (22,26,'Quadratic attention — retrieval is the discount')]),
 V(BOOTCAMP_K['llm'], 'llm', 'llm-finetune', 'Fine-Tuning: Teaching Manners',
   'pretraining teaches, tuning civilizes', 'bbg', scene_llm_finetune,
   'Fine-tuning: supervised pairs teach the format, preference data teaches the manners, and evals confirm the manners stuck. Pretraining teaches the world — tuning civilizes the answers.',
   [(4,10,'SFT: instruction pairs teach the format'),
    (10,16,'Preference tuning: humans rank, model learns manners'),
    (16,22,'Evals: confirm the manners stuck'),
    (22,26,'Small data, big behavior shift')]),
 V(BOOTCAMP_K['llm'], 'llm', 'llm-serve', 'Inference Serving: Tokens per Second',
   'prefill, then decode', 'primer', scene_llm_serve,
   'Inference: prefill processes the prompt in parallel, decode generates one token at a time, batching and KV-cache squeeze the throughput. Prefill, then decode — the two phases have different physics.',
   [(4,10,'Prefill: the prompt, processed in parallel'),
    (10,16,'Decode: one token at a time — autoregressive'),
    (16,22,'KV-cache: remember the past, skip recompute'),
    (22,26,'Batching: many users, one GPU — throughput')]),
 # --- ml-defense
 V(BOOTCAMP_K['mldef'], 'mldef', 'mldef-adversarial', 'Adversarial Examples: The Invisible Ink',
   'imperceptible to you, decisive to the model', 'primer', scene_mldef_adversarial,
   'Adversarial examples: invisible noise flips the prediction — a panda becomes a gibbon with 99% confidence. Imperceptible to you, decisive to the model — robustness is the missing feature.',
   [(4,10,'Noise invisible to humans — epsilon-small'),
    (10,16,'The model flips: panda → gibbon, 99% sure'),
    (16,22,'Transferable: one attack fools many models'),
    (22,26,'Defense: adversarial training — vaccinate the model')]),
 V(BOOTCAMP_K['mldef'], 'mldef', 'mldef-poison', 'Data Poisoning: The Slow Betrayal',
   'a few bad rows rot the whole model', 'primer', scene_mldef_poison,
   'Data poisoning: a few crafted rows in the training set plant a backdoor — the model behaves until the trigger appears. A few bad rows rot the whole model; provenance is the defense.',
   [(4,10,'Crafted rows slip into training data'),
    (10,16,'The backdoor sleeps — normal inputs, normal outputs'),
    (16,22,'The trigger wakes it — targeted misbehavior'),
    (22,26,"Provenance: know every row's origin")]),
 V(BOOTCAMP_K['mldef'], 'mldef', 'mldef-robust', 'Robustness Metrics: Measuring Armor',
   'accuracy under fire', '3b1b', scene_mldef_robust,
   'Robustness metrics: clean accuracy, accuracy under attack, and the certified radius — the provable safe zone. Accuracy under fire is the only accuracy that counts in adversarial settings.',
   [(4,10,'Clean accuracy: the fair-weather number'),
    (10,16,'Robust accuracy: under attack — the real number'),
    (16,22,'Certified radius: provably safe — the gold standard'),
    (22,26,'Report all three — never just the first')]),
 # --- nvidia-ai
 V(BOOTCAMP_K['nva'], 'nva', 'nva-stack', 'The CUDA Stack: Silicon to Model',
   'every layer exists to feed the GPUs', 'bbg', scene_nva_stack,
   'The CUDA stack: GPUs at the bottom, CUDA and drivers above, cuDNN and NCCL for the math and the networking, frameworks on top. Every layer exists to feed the GPUs — utilization is the religion.',
   [(4,10,'GPUs: the silicon — thousands of cores'),
    (10,16,'CUDA + drivers: the programming model'),
    (16,22,'cuDNN / NCCL: the math and the collective comms'),
    (22,26,'Frameworks: PyTorch speaks CUDA fluently')]),
 V(BOOTCAMP_K['nva'], 'nva', 'nva-flops', 'FLOPS: Counting the Lightning',
   'training is measured in petaflop-days', '3b1b', scene_nva_flops,
   "FLOPS: a GPU's trillions of operations per second, a cluster's petaflops, a training run's petaflop-days. Training is measured in petaflop-days — the budget line of the AI era.",
   [(4,10,'TFLOPS: trillions per second — per GPU'),
    (10,16,'Mixed precision: double the throughput, keep the accuracy'),
    (16,22,'Petaflop-days: the training budget unit'),
    (22,26,'The AI era budgets in FLOPS')]),
 V(BOOTCAMP_K['nva'], 'nva', 'nva-nemo', 'NeMo Training in 100 Seconds',
   'recipes, not raw scripts', 'fireship', scene_nva_nemo,
   'NeMo: pick a recipe, point it at your data, launch the trainer — mixed precision and distributed strategy included. Recipes, not raw scripts — the framework handles the plumbing.',
   [(4,10,'Recipes: curated configs for common models'),
    (10,16,"Data: your corpus, the model's worldview"),
    (16,22,'Trainer: distributed, mixed-precision, checkpointed'),
    (22,26,'The plumbing is handled — you tune the recipe')]),
 # --- quantum
 V(BOOTCAMP_K['qm'], 'qm', 'qm-qubit', 'Qubits: 0 and 1, Simultaneously',
   'superposition is the resource', '3b1b', scene_qm_qubit,
   'A qubit: alpha-zero plus beta-one, probabilities summing to one — n qubits hold 2^n amplitudes. Superposition is the resource; measurement collapses it to one answer.',
   [(4,10,'|0> and |1> at once — the superposition'),
    (10,16,'Amplitudes: probabilities waiting to happen'),
    (16,22,'n qubits → 2^n states — exponential room'),
    (22,26,'Measurement collapses — one answer, probabilities honored')]),
 V(BOOTCAMP_K['qm'], 'qm', 'qm-gates', 'Quantum Gates: The Circuit',
   'gates rotate, entanglement correlates', 'bbg', scene_qm_gates,
   'Quantum gates: Hadamard creates superposition, CNOT entangles, measurement reads out. Gates rotate, entanglement correlates — the circuit is the program.',
   [(4,10,'Hadamard: 0 → superposition — the coin flip'),
    (10,16,'CNOT: entangle two qubits — spooky linkage'),
    (16,22,'Phase gates: rotate the amplitudes'),
    (22,26,'Measure: the circuit answers')]),
 V(BOOTCAMP_K['qm'], 'qm', 'qm-shor', "Shor's Algorithm: RSA's Nightmare",
   'factoring becomes tractable', 'primer', scene_qm_shor,
   "Shor's algorithm: quantum Fourier transform finds the period, the period reveals the factors — RSA's nightmare. Factoring becomes tractable; post-quantum crypto is the answer.",
   [(4,10,'The threat: RSA-2048 falls to enough qubits'),
    (10,16,'Quantum Fourier transform: find the period'),
    (16,22,'Period → factors — the math collapses'),
    (22,26,'Post-quantum crypto: migrate before the qubits arrive')]),
 # --- dp-203
 V(BOOTCAMP_K['dp203'], 'dp203', 'dp203-synapse', 'Synapse: The Analytics Hub',
   'one workspace, every engine', 'bbg', scene_dp203_synapse,
   'Azure Synapse: serverless SQL for instant queries, Spark pools for big processing, pipelines for orchestration — one workspace, every engine, one security model.',
   [(4,10,'Serverless SQL: query the lake directly'),
    (10,16,'Spark pools: big processing, scaled out'),
    (16,22,'Pipelines: orchestrate it all'),
    (22,26,'One workspace — one security model')]),
 V(BOOTCAMP_K['dp203'], 'dp203', 'dp203-spark', 'PySpark in 100 Seconds',
   'transformations lazy, actions eager', 'fireship', scene_dp203_spark,
   'PySpark: read the parquet, filter and group with lazy transformations, then count — the action that fires the job. Transformations lazy, actions eager — the DAG runs at the end.',
   [(4,10,'Read: parquet from the lake — columnar, fast'),
    (10,16,'Transform: filter, group — lazy, just a plan'),
    (16,22,'Action: count() — the DAG finally runs'),
    (22,26,'Partition wisely — shuffles are the tax')]),
 V(BOOTCAMP_K['dp203'], 'dp203', 'dp203-partition', 'Partitioning: Divide and Conquer',
   'partition by the filter, not the fantasy', '3b1b', scene_dp203_partition,
   'Partitioning: divide data by the column queries filter on — date, region — so scans skip whole partitions. Partition by the filter, not the fantasy; too many tiny files is its own disease.',
   [(4,10,'Partition column: the filter queries use'),
    (10,16,'Partition pruning: skip whole directories'),
    (16,22,'File size: ~1 GB sweet spot — not 10,000 tiny files'),
    (22,26,'Small-file disease: compact relentlessly')]),
 # --- mongodb
 V(BOOTCAMP_K['mdb'], 'mdb', 'mdb-documents', 'Documents: Data That Looks Like Code',
   'embed what you read together', 'bbg', scene_mdb_documents,
   'MongoDB documents: JSON-like BSON, nested naturally, schema flexible per document. Embed what you read together, reference what grows unbounded — the schema design mantra.',
   [(4,10,'BSON: JSON with types — dates, ObjectIds'),
    (10,16,'Nesting: the address lives inside the user'),
    (16,22,'Flexible schema: documents vary — deliberately'),
    (22,26,'Embed together-read — reference the unbounded')]),
 V(BOOTCAMP_K['mdb'], 'mdb', 'mdb-agg', 'Aggregation in 100 Seconds',
   'a pipeline of stages', 'fireship', scene_mdb_agg,
   "The aggregation pipeline: match filters, group accumulates, sort orders, project shapes — a pipeline of stages, each feeding the next. SQL's GROUP BY, wearing a pipeline.",
   [(4,10,'$match: filter first — use the index'),
    (10,16,'$group: accumulate — _id is the key'),
    (16,22,'$sort + $project: order and shape'),
    (22,26,'Stages compose — the pipeline is the query')]),
 V(BOOTCAMP_K['mdb'], 'mdb', 'mdb-replica', 'Replica Sets: Elections Included',
   'the primary is elected, not appointed', 'bbg', scene_mdb_replica,
   'Replica sets: one primary takes writes, secondaries replicate, and elections promote a new primary in seconds. The primary is elected, not appointed — majority wins.',
   [(4,10,'Primary: the only writer — all writes here'),
    (10,16,'Secondaries: replicate the oplog — read scaling'),
    (16,22,'Election: majority promotes — seconds, automatic'),
    (22,26,'Write concern: how many must acknowledge')]),
 # --- oracle-db
 V(BOOTCAMP_K['odb'], 'odb', 'odb-arch', 'Oracle Architecture: SGA and Friends',
   'memory structures plus processes', 'bbg', scene_odb_arch,
   'Oracle architecture: the SGA caches data and SQL, the PGA sorts per session, background processes do the writing. Memory structures plus processes — know which does what.',
   [(4,10,'SGA: shared memory — buffer cache, shared pool'),
    (10,16,'PGA: per-session — sorts and hashes'),
    (16,22,'DBWn writes dirty blocks — LGWR writes redo'),
    (22,26,'Instance = SGA + processes — database = files')]),
 V(BOOTCAMP_K['odb'], 'odb', 'odb-rac', 'RAC: One Database, Many Instances',
   'cache fusion keeps them honest', 'bbg', scene_odb_rac,
   'Oracle RAC: multiple instances, one database, Cache Fusion shipping blocks over the interconnect. One database, many instances — scale out without sharding.',
   [(4,10,'Many instances — one shared database'),
    (10,16,'Cache Fusion: blocks fly over the interconnect'),
    (16,22,'Survive node loss — the service relocates'),
    (22,26,'Scale out — no sharding required')]),
 V(BOOTCAMP_K['odb'], 'odb', 'odb-rman', 'RMAN: The Backup Religion',
   'backup, validate, restore — in that order', 'story', scene_odb_rman,
   'RMAN: full backups on schedule, incremental forever after, validate the backups, rehearse the restore. Backup, validate, restore — in that order, or the backups are decorative.',
   [(4,10,'Full backup: the baseline — weekly'),
    (10,16,'Incremental: the deltas — daily'),
    (16,22,'Validate: corrupt backups are worse than none'),
    (22,26,'Restore rehearsal: the only proof that matters')]),
 # --- oracle-sql
 V(BOOTCAMP_K['osql'], 'osql', 'osql-joins', 'JOINs in 100 Seconds',
   'the ON clause is the relationship', 'fireship', scene_osql_joins,
   'JOINs: INNER keeps matches, LEFT keeps all left rows, FULL keeps everything, and the ON clause is the relationship. Draw the Venn diagram, then write the query.',
   [(4,10,'INNER: matches only — the overlap'),
    (10,16,'LEFT: all left rows — NULLs where nothing matched'),
    (16,22,'FULL: everything — both sides, NULLs included'),
    (22,26,'ON is the relationship — WHERE is the filter')]),
 V(BOOTCAMP_K['osql'], 'osql', 'osql-window', 'Window Functions: Rows That See',
   'partition, order, frame', '3b1b', scene_osql_window,
   'Window functions: PARTITION BY slices the rows, ORDER BY sequences them, the frame decides what each row sees — running totals without GROUP BY. Rows that see their neighbors.',
   [(4,10,'PARTITION BY: slice into groups — no collapsing'),
    (10,16,'ORDER BY: sequence within each slice'),
    (16,22,'Frame: ROWS BETWEEN — what the row sees'),
    (22,26,'Running totals, ranks, lags — no self-joins')]),
 V(BOOTCAMP_K['osql'], 'osql', 'osql-explain', 'Execution Plans: Read the Truth',
   'the plan is what actually runs', 'bbg', scene_osql_explain,
   "Execution plans: EXPLAIN shows the optimizer's choice — full scans, index seeks, nested loops vs hash joins. The plan is what actually runs — the SQL is just a suggestion.",
   [(4,10,'EXPLAIN PLAN: the optimizer confesses'),
    (10,16,'Full scan vs index: the eternal fork'),
    (16,22,'Nested loops for few rows — hash for many'),
    (22,26,'The plan is truth — SQL is suggestion')]),
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
