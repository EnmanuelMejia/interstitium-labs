"""Bootcamp video Phase 2, Batch B10: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b5.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.

Batch B10 bootcamps (Dev/Misc):
  blockchain-dev, creative-code, enochian-programming, git-devops, ides-tooling, platform-engineering, python-systems, sre-platform, sre-practices, systems-cs, vault-consul, fullstack-desk
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
# blockchain-dev (bbg x1 + fireship x1 + primer x1)
def scene_bcd_chain(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Blocks: The Chain Links', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('tx pool', 'block N', 'block N+1', 'block N+2', 'immutable')
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
        txt(dr, (W // 2, 540), 'each block commits to the last', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the chain is an append-only promise', font(F_SANS, 24), DIM, anchor="mm")
def scene_bcd_solidity(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Solidity in 100 Seconds', MAGENTA)
    _lns = [('contract Vault {', (200, 200, 255)), ('  mapping(address => uint) balances;', (200, 200, 255)), ('  function withdraw() external {', YELLOW), ('    uint amt = balances[msg.sender];', (200, 200, 255)), ('    balances[msg.sender] = 0;  // effects first', GREEN), ('    payable(msg.sender).transfer(amt);', (200, 200, 255)), ('  }', (200, 200, 255)), ('}', (200, 200, 255))]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'Vault.sol', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'the contract is the law — audit it', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'reentrancy killed the DAO — checks-effects-interactions', font(F_SANS, 24), DIM, anchor="mm")
def scene_bcd_consensus(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Consensus: Agreeing at Scale', CYAN)
    _boxes = ('PoW', 'PoS', 'BFT', 'finality')
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
        txt(dr, (W // 2, 500), 'trust without trusting anyone', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the mechanism is the trust — audit the incentives', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# creative-code (fireship x1 + primer x1 + story x1)
def scene_cr_generative(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'Generative Art: Rules That Bloom', CYAN)
    _rows, _cols = 6, 10
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — generations blooming from one seed' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'the artist writes the system', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'the system draws the piece — taste curates', font(F_SANS, 24), DIM, anchor="mm")
def scene_cr_shader(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Shaders in 100 Seconds', MAGENTA)
    _lns = [('vec2 uv = gl_FragCoord.xy / res;', (200, 200, 255)), ('float d = length(uv - 0.5);', (200, 200, 255)), ('vec3 col = vec3(sin(d*20.0 - t));', YELLOW), ('gl_FragColor = vec4(col, 1.0);', GREEN), ('# per pixel × 2M pixels × 60fps', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'art.frag', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'a program per pixel', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'sixty frames of math per second', font(F_SANS, 24), DIM, anchor="mm")
def scene_cr_installation(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Installation: Opening Night', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'code meets the physical world', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('concept: the feeling, sketched', 5), ('prototype: interaction works-ish', 9), ('build: hardware meets software', 13), ('rehearse: break it before the crowd does', 17), ('opening night: no debugger, just applause', 21)]
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
        txt(dr, (W // 2, 624), 'code meets the physical world', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the physical world has opinions — rehearse', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# enochian-programming (bbg x1 + primer x1 + story x1)
def scene_eno_calls(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Calls: A Formal Language', CYAN)
    _boxes = ('call 1', 'call 19', 'names', 'hierarchy')
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
        txt(dr, (W // 2, 500), 'structure before meaning', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'formality is the feature — precision is respect', font(F_SANS, 24), DIM, anchor="mm")
def scene_eno_tablets(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'The Elemental Tablets', CYAN)
    _rows, _cols = 4, 6
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — tablet cells revealing names' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'a grid that is also a map', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'the combinatorics are the meditation', font(F_SANS, 24), DIM, anchor="mm")
def scene_eno_ritual(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Ritual as Program', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'intention, compiled', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('prepare: space and mind', 5), ('declare: intention, precisely', 9), ('execute: the sequence exactly', 13), ('close: seal it properly', 17), ('record: the logbook never lies', 21)]
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
        txt(dr, (W // 2, 624), 'intention, compiled', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'precision is the point — the logbook is the test suite', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# git-devops (bbg x1 + fireship x1 + primer x1)
def scene_git_branch(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Branch and Merge: The Dance', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('main', 'branch', 'commit', 'PR review', 'merge')
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
        txt(dr, (W // 2, 540), 'branch for everything, merge deliberately', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'main is sacred — protect it with rules', font(F_SANS, 24), DIM, anchor="mm")
def scene_git_rebase(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Rebase in 100 Seconds', MAGENTA)
    _lns = [('$ git fetch origin', (200, 200, 255)), ('$ git rebase origin/main', YELLOW), ('# replay: your commits on fresh main', GREEN), ('$ git rebase -i HEAD~3  # squash', (200, 200, 255)), ('# shared history: hands off', RED)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'history.sh', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'rewrite history before you share it', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'never rebase what others have pulled', font(F_SANS, 24), DIM, anchor="mm")
def scene_git_cicd(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'CI/CD: The Conveyor', CYAN)
    _boxes = ('push', 'build', 'test', 'artifact', 'deploy')
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
        txt(dr, (W // 2, 500), 'every push gets the full treatment', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'red means stop — the gate is not decorative', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# ides-tooling (bbg x1 + 3b1b x1 + primer x1)
def scene_ide_debug(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Debug Session: The Hunt', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('reproduce', 'breakpoint', 'step', 'watch', 'fix')
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
        txt(dr, (W // 2, 540), 'breakpoints are questions', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the runtime answers — print statements are the fallback', font(F_SANS, 24), DIM, anchor="mm")
def scene_ide_keys(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Keystrokes: The Compound Interest', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'the mouse is a tax', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'seconds × actions × days', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('per action', 3, '%ds'), ('per day', 240, '%d'), ('per year', 60, '%dh')]
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
        txt(dr, (W // 2, 540), 'the mouse is a tax', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'one shortcut a week — the sustainable pace', font(F_SANS, 24), DIM, anchor="mm")
def scene_ide_extensions(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Extensions: The Ecosystem', CYAN)
    _boxes = ('lint', 'format', 'debug', 'test', 'AI')
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
        txt(dr, (W // 2, 500), 'the editor is a platform', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'curate yours — dotfiles are a resume', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# platform-engineering (bbg x1 + fireship x1 + story x1)
def scene_plat_idp(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'IDP: The Paved Road', CYAN)
    _boxes = ('golden path', 'self-service', 'guardrails', 'docs', 'support')
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
        txt(dr, (W // 2, 500), "pave the road, don't pave the cowpaths", font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'adoption is the metric — not features shipped', font(F_SANS, 24), DIM, anchor="mm")
def scene_plat_golden(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Golden Path Template in 100 Seconds', MAGENTA)
    _lns = [('scaffold: {repo: service, lang: go}', (200, 200, 255)), ('ci: {test: true, lint: true}', GREEN), ('deploy: {targets: [staging, prod]}', YELLOW), ('guardrails: {policy: standard}', (200, 200, 255)), ('# the paved road, versioned', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'template.yaml', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'the blessed way, as code', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'an afternoon, not a quarter', font(F_SANS, 24), DIM, anchor="mm")
def scene_plat_adopt(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Platform Adoption: The Long Game', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'build with them, not for them', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('listen: shadowing the pain', 5), ('ship: thinnest useful path', 9), ('first teams onboard', 13), ('iterate on real usage', 17), ('the platform becomes the default', 21)]
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
        txt(dr, (W // 2, 624), 'build with them, not for them', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'shelfware is the failure mode — adoption is the goal', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# python-systems (bbg x1 + fireship x1 + primer x1)
def scene_pys_asyncio(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'The Event Loop: One Thread, Many Waits', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('coroutine', 'await I/O', 'loop waits', 'resume', 'done')
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
        txt(dr, (W // 2, 540), 'never block the loop', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'await the waits — thread the CPU', font(F_SANS, 24), DIM, anchor="mm")
def scene_pys_cffi(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'CFFI in 100 Seconds', MAGENTA)
    _lns = [('from cffi import FFI', (200, 200, 255)), ('ffi = FFI()', (200, 200, 255)), ('ffi.cdef("int add(int, int);")', YELLOW), ('lib = ffi.dlopen("./fast.so")', YELLOW), ('lib.add(2, 3)  # C speed, Python syntax', GREEN)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'fast.py', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), "Python's handshake with C", font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'the GIL releases during the call', font(F_SANS, 24), DIM, anchor="mm")
def scene_pys_packaging(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Packaging: Ship It Right', CYAN)
    _boxes = ('pyproject', 'wheel', 'venv', 'pip install')
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
        txt(dr, (W // 2, 500), 'if it is not installable, it is not done', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'pin the deps — future-you says thanks', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# sre-platform (bbg x1 + 3b1b x1 + story x1)
def scene_srep_slo(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Error Budgets: Failure, Quantified', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'reliability is a budget, not a virtue', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'budget = 1 - SLO', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('SLO', 999, '%d‰'), ('minutes/mo', 43, '%d'), ('burn rate', 2, '%dx')]
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
        txt(dr, (W // 2, 540), 'reliability is a budget, not a virtue', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), '43 minutes a month — spend them deliberately', font(F_SANS, 24), DIM, anchor="mm")
def scene_srep_observability(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Observability: The Three Pillars', CYAN)
    _layers = ('traces', 'logs', 'metrics', 'request ID')
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
        txt(dr, (W // 2, 612), 'metrics, logs, traces — correlated', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the request ID is the thread through all three', font(F_SANS, 24), DIM, anchor="mm")
def scene_srep_incident(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Incident: The First Hour', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'mitigate first, understand second', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('detect: the alert that matters', 5), ('declare: incident commander named', 9), ('mitigate: rollback stops the bleeding', 13), ('communicate: status page updated', 17), ('resolve: the learning begins', 21)]
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
        txt(dr, (W // 2, 624), 'mitigate first, understand second', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'communicate early — silence breeds tickets', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# sre-practices (3b1b x1 + primer x1 + story x1)
def scene_srepr_blameless(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Blameless Postmortem', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'fix the system, not the person', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('timeline: minute-by-minute facts', 5), ('five whys: past the human error', 9), ('systemic causes named', 13), ('actions assigned with dates', 17), ('published: the org learns', 21)]
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
        txt(dr, (W // 2, 624), 'fix the system, not the person', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the action items are the deliverable', font(F_SERIF, 24), DIM, anchor="mm")
def scene_srepr_chaos(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['primer'])
    dot_grid(dr)
    bbg_title(dr, 'Chaos Experiments: The Fire Drill', CYAN)
    _rows, _cols = 5, 6
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
    txt(dr, (W // 2, _y0 + _rows * _chh + 46), '%d of %d — chaos cells — all recovered' % (_k, _tot),
        font(F_MONOB, 28), CYAN, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 606), 'break it on purpose, on schedule', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), 'the blast radius is always contained — always', font(F_SANS, 24), DIM, anchor="mm")
def scene_srepr_toil(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Toil Budget: Automate the Boring', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'toil is the work that scales with size', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('paging', 0.35, '35%', RED), ('manual deploys', 0.5, '50%', ORANGE), ('ticket ops', 0.4, '40%', YELLOW), ('engineering', 0.65, '65%', GREEN)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'toil is the work that scales with size', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'automate it or drown in it — the only options', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# systems-cs (bbg x1 + 3b1b x1 + primer x1)
def scene_sys_syscall(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, "Syscalls: The Kernel's API", CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('user code', 'trap', 'kernel', 'return', 'resume')
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
        txt(dr, (W // 2, 540), 'user space asks, kernel space does', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the boundary is the security — validate everything', font(F_SANS, 24), DIM, anchor="mm")
def scene_sys_virtual(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Virtual Memory: The Great Illusion', CYAN)
    _layers = ('process view', 'page tables', 'TLB', 'physical RAM', 'swap')
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
        txt(dr, (W // 2, 612), 'every process gets its own universe', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the MMU maintains the illusion — respect the page faults', font(F_SANS, 24), DIM, anchor="mm")
def scene_sys_amdahl(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "Amdahl's Law: The Parallel Ceiling", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'the serial part rules', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'S = 1 / (s + p/N)', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('serial %', 10, '%d%%'), ('max speedup', 10, '%dx'), ('cores wasted', 54, '%d')]
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
        txt(dr, (W // 2, 540), 'the serial part rules', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'cores beyond the ceiling buy nothing', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# vault-consul (bbg x1 + fireship x1 + primer x1)
def scene_vc_secrets(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Secret Retrieval: The Vault Dance', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('auth', 'policy check', 'issue lease', 'use', 'revoke')
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
        txt(dr, (W // 2, 540), 'authenticate, authorize, audit', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'short leases beat long secrets — rotate relentlessly', font(F_SANS, 24), DIM, anchor="mm")
def scene_vc_policy(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Vault Policy in 100 Seconds', MAGENTA)
    _lns = [('path "secret/data/prod/*" {', (200, 200, 255)), ('  capabilities = ["read", "list"]', GREEN), ('}', (200, 200, 255)), ('path "secret/data/*" {', (200, 200, 255)), ('  capabilities = ["deny"]', RED), ('}', (200, 200, 255)), ('# default deny — allow by path', YELLOW)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'policy.hcl', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'deny by default, allow by path', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'review policies like code — they are', font(F_SANS, 24), DIM, anchor="mm")
def scene_vc_mesh(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Service Mesh: The Sidecar Pattern', CYAN)
    _nodes = [('svc-a', 280, 280), ('proxy-a', 560, 280), ('proxy-b', 840, 280), ('svc-b', 1120, 280)]
    _edges = [(0, 1), (1, 2), (2, 3)]
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
        txt(dr, (W // 2, 560), 'the proxy handles the hard parts', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'the app stays dumb — the mesh gets smart', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# fullstack-desk (bbg x1 + primer x1 + story x1)
def scene_fsd_day(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'A Day at the Desk', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'the craft is in the routine', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('standup: aligned in fifteen', 5), ('deep work: the sacred block', 9), ('review: kindness with standards', 13), ('deploy: shipped, monitored', 17), ('shutdown: the day ends clean', 21)]
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
        txt(dr, (W // 2, 624), 'the craft is in the routine', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'protect the deep work — batch the rest', font(F_SERIF, 24), DIM, anchor="mm")
def scene_fsd_ticket(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Ticket Lifecycle: From Backlog to Done', CYAN)
    _boxes = ('triage', 'progress', 'review', 'done')
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
        txt(dr, (W // 2, 500), 'done means deployed and verified', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'WIP limits are the speed secret — finish before starting', font(F_SANS, 24), DIM, anchor="mm")
def scene_fsd_standup(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Standup vs Deep Work', CYAN)
    _lp = ('long uninterrupted blocks', 'compounds daily', 'ships the hard things')
    _rp = ('fragmented attention', 'context-switch tax', 'alignment only')
    _nL = int(clamp((t - 5) / 6) * len(_lp))
    _nR = int(clamp((t - 12) / 6) * len(_rp))
    dr.rectangle([120, 190, 600, 470], fill=(16, 16, 30), outline=GREEN, width=3)
    txt(dr, (360, 232), 'MAKER TIME', font(F_BOLD, 26), GREEN, anchor="mm")
    for _i in range(_nL):
        txt(dr, (160, 290 + _i * 46), "\u2713 " + _lp[_i], font(F_SANS, 22), GREEN, anchor="lm")
    dr.rectangle([680, 190, 1160, 470], fill=(16, 16, 30), outline=RED, width=3)
    txt(dr, (920, 232), 'MEETING TIME', font(F_BOLD, 26), RED, anchor="mm")
    for _i in range(_nR):
        txt(dr, (720, 290 + _i * 46), "\u2717 " + _rp[_i], font(F_SANS, 22), RED, anchor="lm")
    if t > 20:
        dr.rectangle([300, 520, 980, 592], fill=(12, 24, 12), outline=GOLD, width=3)
        txt(dr, (W // 2, 556), 'align fast — then protect the blocks', font(F_BOLD, 25), GOLD, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'bcd': 'blockchain-dev',
    'cr': 'creative-code',
    'eno': 'enochian-programming',
    'git': 'git-devops',
    'ide': 'ides-tooling',
    'plat': 'platform-engineering',
    'pys': 'python-systems',
    'srep': 'sre-platform',
    'srepr': 'sre-practices',
    'sys': 'systems-cs',
    'vc': 'vault-consul',
    'fsd': 'fullstack-desk',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'bcd': 'BLOCKCHAIN · dApp Development',
    'cr': 'CREATIVE CODE · Generative Art',
    'eno': 'ENOCHIAN · Esoteric Systems',
    'git': 'GIT · DevOps Workflows',
    'ide': 'IDES · Developer Tooling',
    'plat': 'PLATFORM · Internal Platforms',
    'pys': 'PYTHON SYS · Systems Programming',
    'srep': 'SRE · Platform Reliability',
    'srepr': 'SRE · Practices & Culture',
    'sys': 'SYSTEMS · Computer Systems',
    'vc': 'VAULT · Secrets & Service Mesh',
    'fsd': 'FULLSTACK · The Dev Desk',
}
VIDEOS = [
 # --- blockchain-dev
 V(BOOTCAMP_K['bcd'], 'bcd', 'bcd-chain', 'Blocks: The Chain Links',
   'each block commits to the last', 'primer', scene_bcd_chain,
   'A blockchain: transactions batch into blocks, each block hashes the previous, and the chain becomes tamper-evident. Each block commits to the last — rewriting history means rewriting everything after.',
   [(4,10,'Transactions batch into a block'),
    (10,16,'The block hashes its predecessor — the link'),
    (16,22,'Tamper-evident: change one byte, break every link after'),
    (22,26,'Rewriting history costs more than the history is worth')]),
 V(BOOTCAMP_K['bcd'], 'bcd', 'bcd-solidity', 'Solidity in 100 Seconds',
   'the contract is the law — audit it', 'fireship', scene_bcd_solidity,
   'A Solidity contract: state variables on chain, functions mutate them, modifiers guard access. The contract is the law and the law is immutable — audit it like lives depend on it.',
   [(4,10,'State variables: on-chain storage — expensive'),
    (10,16,'Functions: the only way state changes'),
    (16,22,'Modifiers: onlyOwner and friends — the guards'),
    (22,26,'Immutable once deployed — the audit is the test')]),
 V(BOOTCAMP_K['bcd'], 'bcd', 'bcd-consensus', 'Consensus: Agreeing at Scale',
   'trust without trusting anyone', 'bbg', scene_bcd_consensus,
   'Consensus: proof-of-work burns energy for security, proof-of-stake risks capital instead, BFT votes in rounds. Trust without trusting anyone — the mechanism is the trust.',
   [(4,10,'Proof-of-work: energy as the vote — expensive, proven'),
    (10,16,'Proof-of-stake: capital at risk — efficient, slashing'),
    (16,22,'BFT: rounds of votes — fast, needs known validators'),
    (22,26,'The mechanism IS the trust — pick by threat model')]),
 # --- creative-code
 V(BOOTCAMP_K['cr'], 'cr', 'cr-generative', 'Generative Art: Rules That Bloom',
   'the artist writes the system', 'primer', scene_cr_generative,
   'Generative art: simple rules iterate thousands of times and complexity blooms — the artist writes the system, the system draws the piece. Seeds make it reproducible; taste makes it art.',
   [(4,10,'Simple rules: the seed of everything'),
    (10,16,'Iteration: thousands of generations'),
    (16,22,'Emergence: complexity the artist never drew'),
    (22,26,'Seeds: reproducibility — taste: the rest')]),
 V(BOOTCAMP_K['cr'], 'cr', 'cr-shader', 'Shaders in 100 Seconds',
   'a program per pixel', 'fireship', scene_cr_shader,
   'A fragment shader: a program that runs per pixel — UV coordinates in, color out, time as the animator. A program per pixel, sixty times a second — the GPU is a paintbrush with a million bristles.',
   [(4,10,'Per-pixel programs — the GPU runs them all at once'),
    (10,16,'UV: where am I on the screen'),
    (16,22,'Time: the animator — everything moves'),
    (22,26,'Math becomes marble, fire, water')]),
 V(BOOTCAMP_K['cr'], 'cr', 'cr-installation', 'The Installation: Opening Night',
   'code meets the physical world', 'story', scene_cr_installation,
   'An installation timeline: concept, prototype the interaction, build the hardware, rehearse the failure modes, opening night. Code meets the physical world — and the physical world has opinions.',
   [(4,10,'Concept: the feeling before the form'),
    (10,16,'Prototype: the interaction, roughly'),
    (16,22,'Hardware: sensors, projectors, the real world'),
    (22,26,'Rehearse failure — opening night has no debugger')]),
 # --- enochian-programming
 V(BOOTCAMP_K['eno'], 'eno', 'eno-calls', 'The Calls: A Formal Language',
   'structure before meaning', 'bbg', scene_eno_calls,
   'The Enochian Calls: nineteen formal invocations with rigid structure — names, hierarchy, direction. Structure before meaning: a formal language where syntax carries the weight.',
   [(4,10,'Nineteen calls — a fixed corpus'),
    (10,16,'Rigid structure: names, ranks, directions'),
    (16,22,'Syntax carries weight — formality is the feature'),
    (22,26,'Study the structure before the meaning')]),
 V(BOOTCAMP_K['eno'], 'eno', 'eno-tablets', 'The Elemental Tablets',
   'a grid that is also a map', 'primer', scene_eno_tablets,
   'The four Elemental Tablets: grids of letters mapping the elements — a grid that is also a map. Permute the rows and new names surface; the combinatorics are the meditation.',
   [(4,10,'Four tablets — air, water, earth, fire'),
    (10,16,'Letters in grids — the map is the territory'),
    (16,22,'Permutations surface new names'),
    (22,26,'Combinatorics as contemplation')]),
 V(BOOTCAMP_K['eno'], 'eno', 'eno-ritual', 'Ritual as Program',
   'intention, compiled', 'story', scene_eno_ritual,
   'Ritual as program: prepare the space, declare the intention, execute the sequence, close and record. Intention, compiled — a procedure where precision is the point.',
   [(4,10,'Prepare: the space, the tools, the mind'),
    (10,16,'Declare: intention stated precisely'),
    (16,22,'Execute: the sequence, exactly as written'),
    (22,26,'Close and record — the logbook matters')]),
 # --- git-devops
 V(BOOTCAMP_K['git'], 'git', 'git-branch', 'Branch and Merge: The Dance',
   'branch for everything, merge deliberately', 'primer', scene_git_branch,
   'Branching: main stays deployable, features branch off, pull requests review, merges land deliberately. Branch for everything, merge deliberately — main is sacred.',
   [(4,10,'main: always deployable — the sacred branch'),
    (10,16,'Feature branches: one idea per branch'),
    (16,22,'Pull requests: review before merging'),
    (22,26,'Merge deliberately — squash or keep history, choose')]),
 V(BOOTCAMP_K['git'], 'git', 'git-rebase', 'Rebase in 100 Seconds',
   'rewrite history before you share it', 'fireship', scene_git_rebase,
   'Rebase: replay your commits onto the latest main — linear history, no merge bubbles. Rewrite history before you share it; never rebase what others have pulled.',
   [(4,10,'Your commits, replayed onto fresh main'),
    (10,16,'Linear history — no merge bubbles'),
    (16,22,'Interactive: squash, reword, reorder'),
    (22,26,'Golden rule: never rebase shared history')]),
 V(BOOTCAMP_K['git'], 'git', 'git-cicd', 'CI/CD: The Conveyor',
   'every push gets the full treatment', 'bbg', scene_git_cicd,
   'CI/CD: push triggers build, tests gate the merge, artifacts publish, deploy rolls out. Every push gets the full treatment — the conveyor never sleeps.',
   [(4,10,'Build: compile every push — no exceptions'),
    (10,16,'Test: the gate — red means stop'),
    (16,22,'Artifacts: versioned, immutable'),
    (22,26,"Deploy: the conveyor's end — and its pride")]),
 # --- ides-tooling
 V(BOOTCAMP_K['ide'], 'ide', 'ide-debug', 'Debug Session: The Hunt',
   'breakpoints are questions', 'primer', scene_ide_debug,
   'Debugging: reproduce it, breakpoint the suspicion, step through the truth, watch the variables confess. Breakpoints are questions — the runtime answers.',
   [(4,10,'Reproduce: the bug on demand — or it is folklore'),
    (10,16,'Breakpoint: question the suspicious line'),
    (16,22,'Step: through the truth, one frame at a time'),
    (22,26,'Watch: the variables confess')]),
 V(BOOTCAMP_K['ide'], 'ide', 'ide-keys', 'Keystrokes: The Compound Interest',
   'the mouse is a tax', '3b1b', scene_ide_keys,
   'Keyboard mastery: every shortcut compounds — seconds per action, hundreds per day. The mouse is a tax; the keyboard is compound interest on your career.',
   [(4,10,'Shortcuts: seconds saved per action'),
    (10,16,'Hundreds of actions daily — the math compounds'),
    (16,22,'Learn one per week — the sustainable pace'),
    (22,26,'The mouse is a tax — pay it rarely')]),
 V(BOOTCAMP_K['ide'], 'ide', 'ide-extensions', 'Extensions: The Ecosystem',
   'the editor is a platform', 'bbg', scene_ide_extensions,
   'IDE extensions: linters catch it early, formatters end the debates, debuggers see inside, AI assistants draft the boilerplate. The editor is a platform — curate yours.',
   [(4,10,'Linters: catch it before the commit'),
    (10,16,'Formatters: end the style debates forever'),
    (16,22,'Debuggers: see inside the running code'),
    (22,26,'AI assistants: draft the boilerplate')]),
 # --- platform-engineering
 V(BOOTCAMP_K['plat'], 'plat', 'plat-idp', 'IDP: The Paved Road',
   "pave the road, don't pave the cowpaths", 'bbg', scene_plat_idp,
   'The internal developer platform: golden paths for common work, self-service everything, guardrails not gates. Pave the road — developers will drive it.',
   [(4,10,'Golden paths: the blessed way to ship'),
    (10,16,'Self-service: no tickets for routine work'),
    (16,22,'Guardrails, not gates — safe by default'),
    (22,26,'Adoption is the metric — build what they use')]),
 V(BOOTCAMP_K['plat'], 'plat', 'plat-golden', 'Golden Path Template in 100 Seconds',
   'the blessed way, as code', 'fireship', scene_plat_golden,
   'A golden path template: the repo scaffold, CI wired, deploy targets declared — the blessed way, as code. New service in an afternoon, not a quarter.',
   [(4,10,'Scaffold: the repo, structured right'),
    (10,16,'CI wired: tests run from commit one'),
    (16,22,'Deploy declared: targets, not tickets'),
    (22,26,'Afternoon, not quarter — that is the pitch')]),
 V(BOOTCAMP_K['plat'], 'plat', 'plat-adopt', 'Platform Adoption: The Long Game',
   'build with them, not for them', 'story', scene_plat_adopt,
   'Platform adoption: listen to the pain, ship the thinnest useful path, celebrate the first teams, iterate on real usage. Build with them, not for them — or the platform becomes shelfware.',
   [(4,10,'Listen: the pain, in their words'),
    (10,16,'Thinnest useful path — ship early'),
    (16,22,'First teams: celebrate loudly'),
    (22,26,'Iterate on usage — not on opinions')]),
 # --- python-systems
 V(BOOTCAMP_K['pys'], 'pys', 'pys-asyncio', 'The Event Loop: One Thread, Many Waits',
   'never block the loop', 'primer', scene_pys_asyncio,
   'asyncio: one thread, coroutines that yield on I/O, the loop resuming whoever is ready. Never block the loop — await the waits, thread the CPU.',
   [(4,10,'Coroutines: functions that pause politely'),
    (10,16,'await: yield on I/O — the loop does errands'),
    (16,22,'The loop resumes whoever is ready'),
    (22,26,'CPU work goes to threads — never block')]),
 V(BOOTCAMP_K['pys'], 'pys', 'pys-cffi', 'CFFI in 100 Seconds',
   "Python's handshake with C", 'fireship', scene_pys_cffi,
   "CFFI: declare the C signatures, load the library, call it like Python. Python's handshake with C — the GIL releases during the call, speed arrives.",
   [(4,10,'Declare: the C signatures in Python'),
    (10,16,'Load: dlopen the library'),
    (16,22,'Call: like Python — the GIL releases'),
    (22,26,"Speed arrives — with C's sharp edges")]),
 V(BOOTCAMP_K['pys'], 'pys', 'pys-packaging', 'Packaging: Ship It Right',
   'if it is not installable, it is not done', 'bbg', scene_pys_packaging,
   'Python packaging: pyproject declares, wheels distribute, virtualenvs isolate. If it is not installable, it is not done — pip install is the acceptance test.',
   [(4,10,'pyproject.toml: the declaration — metadata, deps'),
    (10,16,'Wheels: the distribution — built once'),
    (16,22,'Virtualenvs: isolation — per project'),
    (22,26,'pip install: the acceptance test')]),
 # --- sre-platform
 V(BOOTCAMP_K['srep'], 'srep', 'srep-slo', 'Error Budgets: Failure, Quantified',
   'reliability is a budget, not a virtue', '3b1b', scene_srep_slo,
   'Error budgets: 99.9% allows 43 minutes of monthly downtime — spend it on velocity or hoard it, but the budget is the policy. Reliability is a budget, not a virtue.',
   [(4,10,'SLO: the promise — 99.9% monthly'),
    (10,16,'Budget: 43 minutes of allowed failure'),
    (16,22,'Spend on velocity — or freeze on safety'),
    (22,26,'The budget ends the reliability-vs-speed war')]),
 V(BOOTCAMP_K['srep'], 'srep', 'srep-observability', 'Observability: The Three Pillars',
   'metrics, logs, traces — correlated', 'bbg', scene_srep_observability,
   'Observability: metrics for the vital signs, logs for the story, traces for the journey — correlated by request ID. Three pillars, one incident narrative.',
   [(4,10,'Metrics: the vital signs — numbers over time'),
    (10,16,'Logs: the story — what happened, in words'),
    (16,22,'Traces: the journey — across services'),
    (22,26,'Correlate by request ID — one narrative')]),
 V(BOOTCAMP_K['srep'], 'srep', 'srep-incident', 'Incident: The First Hour',
   'mitigate first, understand second', 'story', scene_srep_incident,
   'The first hour: detect and declare, mitigate the bleeding, communicate status, then understand. Mitigate first, understand second — the users care about the fix, not the root cause.',
   [(4,10,'Detect + declare: name it, page the right humans'),
    (10,16,'Mitigate: stop the bleeding — rollback, shed load'),
    (16,22,'Communicate: status early and often'),
    (22,26,'Understand later — the postmortem is for learning')]),
 # --- sre-practices
 V(BOOTCAMP_K['srepr'], 'srepr', 'srepr-blameless', 'Blameless Postmortem',
   'fix the system, not the person', 'story', scene_srepr_blameless,
   'The blameless postmortem: timeline the facts, find the systemic causes, assign actions not blame. Fix the system, not the person — humans err, systems allow.',
   [(4,10,'Timeline: facts only — no adjectives'),
    (10,16,'Five whys: the systemic causes'),
    (16,22,'Actions: assigned, dated, tracked'),
    (22,26,'No blame — humans err, systems allow')]),
 V(BOOTCAMP_K['srepr'], 'srepr', 'srepr-chaos', 'Chaos Experiments: The Fire Drill',
   'break it on purpose, on schedule', 'primer', scene_srepr_chaos,
   'Chaos engineering: hypothesize the steady state, inject the failure, observe, and roll back. Break it on purpose, on schedule — production is the only honest lab.',
   [(4,10,'Hypothesis: steady state defined first'),
    (10,16,'Blast radius: contained — always'),
    (16,22,'Inject: kill the instance, cut the zone'),
    (22,26,'Observe and roll back — the drill teaches')]),
 V(BOOTCAMP_K['srepr'], 'srepr', 'srepr-toil', 'Toil Budget: Automate the Boring',
   'toil is the work that scales with size', '3b1b', scene_srepr_toil,
   'Toil: manual, repetitive, automatable work that scales with the system. Budget it under 50% — the rest is engineering. Toil is the tax; automation is the refund.',
   [(4,10,'Manual + repetitive + automatable = toil'),
    (10,16,'Scales with size — the hidden tax'),
    (16,22,'Budget: under 50% — the SRE law'),
    (22,26,'Automate the top toil — quarterly')]),
 # --- systems-cs
 V(BOOTCAMP_K['sys'], 'sys', 'sys-syscall', "Syscalls: The Kernel's API",
   'user space asks, kernel space does', 'primer', scene_sys_syscall,
   'Syscalls: user space traps into the kernel, arguments cross the boundary, the kernel does the privileged work, results return. User space asks, kernel space does — the boundary is the security.',
   [(4,10,'Trap: the intentional fault into the kernel'),
    (10,16,'Arguments cross — validated, never trusted'),
    (16,22,"Privileged work: the kernel's monopoly"),
    (22,26,'Return: results cross back — the boundary holds')]),
 V(BOOTCAMP_K['sys'], 'sys', 'sys-virtual', 'Virtual Memory: The Great Illusion',
   'every process gets its own universe', 'bbg', scene_sys_virtual,
   'Virtual memory: pages map to frames, the TLB caches translations, swap extends to disk. Every process gets its own universe — the MMU maintains the illusion.',
   [(4,10,"Pages: the process's view — contiguous illusion"),
    (10,16,'Frames: physical reality — scattered truth'),
    (16,22,'TLB: the translation cache — speed'),
    (22,26,'Swap: the overflow — slow, honest')]),
 V(BOOTCAMP_K['sys'], 'sys', 'sys-amdahl', "Amdahl's Law: The Parallel Ceiling",
   'the serial part rules', '3b1b', scene_sys_amdahl,
   "Amdahl's law: speedup is capped by the serial fraction — 10% serial means 10x max, no matter the cores. The serial part rules; parallelize it or accept the ceiling.",
   [(4,10,'Serial fraction: the unparallelizable remainder'),
    (10,16,'10% serial → 10x ceiling — forever'),
    (16,22,'Cores beyond the ceiling buy nothing'),
    (22,26,'Find the serial part — that is the optimization')]),
 # --- vault-consul
 V(BOOTCAMP_K['vc'], 'vc', 'vc-secrets', 'Secret Retrieval: The Vault Dance',
   'authenticate, authorize, audit', 'primer', scene_vc_secrets,
   'Vault: the app authenticates with its identity, policies authorize the path, the secret issues with a lease, and every access audits. Authenticate, authorize, audit — dynamic secrets, short leases.',
   [(4,10,'Auth: the app proves itself — identity, not password'),
    (10,16,'Policy: the path permissions — least privilege'),
    (16,22,'Lease: secrets expire — rotation by design'),
    (22,26,'Audit: every access logged — always')]),
 V(BOOTCAMP_K['vc'], 'vc', 'vc-policy', 'Vault Policy in 100 Seconds',
   'deny by default, allow by path', 'fireship', scene_vc_policy,
   'Vault policies: deny by default, capabilities granted per path — read here, list there, nothing elsewhere. Deny by default, allow by path — the policy is the perimeter.',
   [(4,10,'Default deny: nothing unless granted'),
    (10,16,'Paths: the resource addresses'),
    (16,22,'Capabilities: read, list, create, update'),
    (22,26,'The policy is the perimeter — review it like code')]),
 V(BOOTCAMP_K['vc'], 'vc', 'vc-mesh', 'Service Mesh: The Sidecar Pattern',
   'the proxy handles the hard parts', 'bbg', scene_vc_mesh,
   'Consul service mesh: sidecar proxies handle mTLS, discovery, and retries — the app just calls localhost. The proxy handles the hard parts; the app stays dumb.',
   [(4,10,'Sidecar: the proxy beside every service'),
    (10,16,'mTLS: identity per service — automatic'),
    (16,22,'Discovery: names, not IPs — the catalog'),
    (22,26,'Intentions: allow/deny per service pair')]),
 # --- fullstack-desk
 V(BOOTCAMP_K['fsd'], 'fsd', 'fsd-day', 'A Day at the Desk',
   'the craft is in the routine', 'story', scene_fsd_day,
   "A developer's day: standup aligns, deep work builds, review sharpens, deploy ships. The craft is in the routine — protect the deep work, batch the rest.",
   [(4,10,'Standup: align in fifteen — then build'),
    (10,16,'Deep work: the 10 AM block — sacred'),
    (16,22,"Review: sharpen others' code — kindly"),
    (22,26,"Deploy: ship it — the day's punctuation")]),
 V(BOOTCAMP_K['fsd'], 'fsd', 'fsd-ticket', 'Ticket Lifecycle: From Backlog to Done',
   'done means deployed and verified', 'bbg', scene_fsd_ticket,
   "Ticket lifecycle: triaged, estimated, in progress, in review, done — and done means deployed and verified, not just coded. The board is the team's shared memory.",
   [(4,10,'Triaged: prioritized, not just listed'),
    (10,16,'In progress: one thing at a time — WIP limits'),
    (16,22,'In review: two pairs of eyes minimum'),
    (22,26,'Done: deployed AND verified — the real definition')]),
 V(BOOTCAMP_K['fsd'], 'fsd', 'fsd-standup', 'Standup vs Deep Work',
   "protect the maker's schedule", 'primer', scene_fsd_standup,
   "Standup: fifteen minutes of alignment — then the maker's schedule takes over. Meetings fragment; deep work compounds. Protect the maker's schedule — batch the interruptions.",
   [(4,10,'Standup: yesterday, today, blockers — fifteen minutes'),
    (10,16,"Then: the maker's schedule — long blocks"),
    (16,22,'Interruptions: batched, not dripped'),
    (22,26,'Alignment without fragmentation — the goal')]),
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
