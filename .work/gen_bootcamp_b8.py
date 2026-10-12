"""Bootcamp video Phase 2, Batch B8: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b5.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.

Batch B8 bootcamps (K8s/Linux/Infrastructure):
  cka, ckad, k8s-associate, openshift, linux-essentials, rhce, rhcsa, comptia-infra, comptia-core, m365, ms-fundamentals, windows-admin
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
# cka (bbg x2 + primer x1)
def scene_cka_pods(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Pod Lifecycle: Born to Die', CYAN)
    _boxes = ('pending', 'running', 'succeeded', 'failed', 'evicted')
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
        txt(dr, (W // 2, 500), 'cattle, not pets', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the deployment replaces them — you never nurse them', font(F_SANS, 24), DIM, anchor="mm")
def scene_cka_debug(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Pod Debug Flow', CYAN)
    _pts = [(180, 330), (440, 330), (700, 330), (960, 330)]
    _labels = ('describe', 'logs', 'exec', 'fixed')
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
        txt(dr, (W // 2, 540), 'describe, logs, exec — in that order', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the events confess before the logs do', font(F_SANS, 24), DIM, anchor="mm")
def scene_cka_etcd(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, "etcd Quorum: The Brain's Vote", CYAN)
    _nodes = [('etcd-1', 320, 280), ('etcd-2', 640, 280), ('etcd-3', 960, 280), ('api', 640, 500)]
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
        txt(dr, (W // 2, 560), 'lose quorum, lose the cluster', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'odd numbers only — even nodes buy nothing', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# ckad (bbg x2 + fireship x1)
def scene_ckad_deploy(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Deployment YAML in 100 Seconds', MAGENTA)
    _lns = [('apiVersion: apps/v1', (200, 200, 255)), ('kind: Deployment', YELLOW), ('spec:', (200, 200, 255)), ('  replicas: 3', GREEN), ('  template:', (200, 200, 255)), ('    containers: [{name: web, image: web:2.1}]', (200, 200, 255)), ('# 3 replicas → the controller delivers', YELLOW)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'deploy.yaml', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'declare the desired state — never the steps', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'the controller converges reality to your YAML', font(F_SANS, 24), DIM, anchor="mm")
def scene_ckad_svc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Services: The Stable Address', CYAN)
    _nodes = [('svc', 300, 320), ('pod-a', 640, 220), ('pod-b', 640, 320), ('pod-c', 640, 420)]
    _edges = [(0, 1), (0, 2), (0, 3)]
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
        txt(dr, (W // 2, 560), 'pods die — the service endures', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'labels are the wiring — get them right', font(F_SANS, 24), DIM, anchor="mm")
def scene_ckad_config(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Config Layers: Code vs Config', CYAN)
    _layers = ('pod spec', 'env / volumes', 'configmap', 'secret')
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
        txt(dr, (W // 2, 612), 'twelve-factor: config leaves the image', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'base64 is not encryption — the exam checks', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# k8s-associate (bbg x2 + primer x1)
def scene_k8sa_arch(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Cluster Anatomy', CYAN)
    _boxes = ('api', 'etcd', 'scheduler', 'controllers', 'kubelet')
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
        txt(dr, (W // 2, 500), 'control plane decides, nodes execute', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'kubectl only ever talks to the API server', font(F_SANS, 24), DIM, anchor="mm")
def scene_k8sa_sched(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Scheduling: Finding a Home', CYAN)
    _pts = [(180, 330), (440, 330), (700, 330), (960, 330)]
    _labels = ('pending', 'filtered', 'scored', 'bound')
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
        txt(dr, (W // 2, 540), 'filters, then scores', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the scheduler is a matchmaker with rules', font(F_SANS, 24), DIM, anchor="mm")
def scene_k8sa_net(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Pod Networking: Flat and Simple', CYAN)
    _nodes = [('pod-a', 280, 280), ('pod-b', 640, 280), ('pod-c', 1000, 280), ('svc', 640, 500)]
    _edges = [(0, 1), (1, 2), (0, 2), (3, 0), (3, 1), (3, 2)]
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
        txt(dr, (W // 2, 560), 'every pod gets an IP — no NAT', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'the flat network is the whole design', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# openshift (bbg x1 + fireship x1 + story x1)
def scene_ocp_route(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Route to Pod: The OpenShift Way', CYAN)
    _boxes = ('route', 'service', 'pod')
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
        txt(dr, (W // 2, 500), 'routes are the front door', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'TLS at the edge, plain inside — terminate early', font(F_SANS, 24), DIM, anchor="mm")
def scene_ocp_build(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'BuildConfig in 100 Seconds', MAGENTA)
    _lns = [('kind: BuildConfig', YELLOW), ('source: {git: {uri: ...}}', (200, 200, 255)), ('strategy: {sourceStrategy: {}}', (200, 200, 255)), ('output: {to: {name: web:latest}}', GREEN), ('triggers: [{type: GitHub}]', (200, 200, 255)), ('# push → build → new image', YELLOW)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'build.yaml', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'source in, image out', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'the cluster becomes the CI', font(F_SANS, 24), DIM, anchor="mm")
def scene_ocp_operator(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Operator Lifecycle: Day Two', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'install is day one — operate is forever', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('CRDs installed: the API learns new words', 5), ('controller deployed: the loop starts', 9), ('first CR applied: desire declared', 13), ('reconcile: drift corrected automatically', 17), ('upgrade: rolling, zero drama', 21)]
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
        txt(dr, (W // 2, 624), 'install is day one — operate is forever', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'the loop never sleeps, so you can', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# linux-essentials (bbg x1 + fireship x1 + 3b1b x1)
def scene_lx_fhs(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Filesystem Hierarchy', CYAN)
    _layers = ('/etc: configuration — text files rule here', '/var: changing data — logs live here', '/home: human territory', '/bin + /sbin: the essentials', '/tmp: transient — wiped without mercy')
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
        txt(dr, (W // 2, 612), 'everything is a file — even the devices', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'learn the map before you wander', font(F_SANS, 24), DIM, anchor="mm")
def scene_lx_perms(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Permissions: The Octal Truth', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), '4-2-1: read, write, execute', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'r=4 · w=2 · x=1', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('chmod 755', 755, '%d'), ('chmod 644', 644, '%d'), ('chmod 600', 600, '%d')]
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
        txt(dr, (W // 2, 540), '4-2-1: read, write, execute', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the exam loves 754 — do the addition', font(F_SANS, 24), DIM, anchor="mm")
def scene_lx_pipes(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Pipes in 100 Seconds', MAGENTA)
    _lns = [('$ ps aux | grep nginx', YELLOW), ("  | awk '{print $2}'", (200, 200, 255)), ('  | sort -n | uniq -c', (200, 200, 255)), ('# processes → PIDs → sorted → counted', GREEN), ('# right to left: the reading order', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'pipeline.sh', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'small tools, composed', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'read the pipeline right to left to understand it', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# rhce (bbg x1 + fireship x1 + primer x1)
def scene_rhce_playbook(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Playbooks in 100 Seconds', MAGENTA)
    _lns = [('- hosts: web', YELLOW), ('  become: true', (200, 200, 255)), ('  tasks:', (200, 200, 255)), ('    - dnf: {name: nginx, state: present}', GREEN), ('    - service: {name: nginx, state: started}', GREEN), ('# desired state — the modules converge', YELLOW)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'site.yaml', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'YAML that configures servers', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'idempotent by design — or it is not Ansible', font(F_SANS, 24), DIM, anchor="mm")
def scene_rhce_roles(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Roles: Playbooks Grow Up', CYAN)
    _boxes = ('tasks', 'handlers', 'templates', 'vars', 'meta')
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
        txt(dr, (W // 2, 500), 'reusable, shareable, tested', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'a playbook repeated three times wants to be a role', font(F_SANS, 24), DIM, anchor="mm")
def scene_rhce_idem(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Idempotence: Run It Twice', CYAN)
    _lp = ('converges, then rests', 'safe to re-run anytime', 'changed=0 is success')
    _rp = ('appends every run', 'fails on re-run', 'works once, maybe')
    _nL = int(clamp((t - 5) / 6) * len(_lp))
    _nR = int(clamp((t - 12) / 6) * len(_rp))
    dr.rectangle([120, 190, 600, 470], fill=(16, 16, 30), outline=GREEN, width=3)
    txt(dr, (360, 232), 'IDEMPOTENT', font(F_BOLD, 26), GREEN, anchor="mm")
    for _i in range(_nL):
        txt(dr, (160, 290 + _i * 46), "\u2713 " + _lp[_i], font(F_SANS, 22), GREEN, anchor="lm")
    dr.rectangle([680, 190, 1160, 470], fill=(16, 16, 30), outline=RED, width=3)
    txt(dr, (920, 232), 'SCRIPTED', font(F_BOLD, 26), RED, anchor="mm")
    for _i in range(_nR):
        txt(dr, (720, 290 + _i * 46), "\u2717 " + _rp[_i], font(F_SANS, 22), RED, anchor="lm")
    if t > 20:
        dr.rectangle([300, 520, 980, 592], fill=(12, 24, 12), outline=GOLD, width=3)
        txt(dr, (W // 2, 556), 'automation you can re-run without fear', font(F_BOLD, 25), GOLD, anchor="mm")
# ============================================================
# rhcsa (bbg x1 + fireship x1 + primer x1)
def scene_rhcsa_lvm(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'LVM: Disks, Abstracted', CYAN)
    _layers = ('filesystem', 'logical volume', 'volume group', 'physical volume')
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
        txt(dr, (W // 2, 612), 'resize without reinstalling', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'snapshots make backups boring — in a good way', font(F_SANS, 24), DIM, anchor="mm")
def scene_rhcsa_systemd(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Boot Targets: The systemd Flow', CYAN)
    _pts = [(160, 330), (420, 330), (680, 330), (940, 330), (1140, 330)]
    _labels = ('firmware', 'kernel', 'systemd', 'targets', 'login')
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
        txt(dr, (W // 2, 540), 'dependencies, not scripts', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'the boot is a graph — read it with list-dependencies', font(F_SANS, 24), DIM, anchor="mm")
def scene_rhcsa_users(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Users in 100 Seconds', MAGENTA)
    _lns = [('$ useradd -m -s /bin/bash dev', YELLOW), ('$ passwd dev', (200, 200, 255)), ('$ usermod -aG wheel dev', GREEN), ("$ visudo  # delegate, don't share root", (200, 200, 255)), ('# every process wears a user', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'users.sh', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'every process wears a user', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'UID 0 is root — everything else is a negotiation', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# comptia-infra (3b1b x2 + primer x1)
def scene_infr_raid(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'RAID Levels: Pick Your Paranoia', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'redundancy has a price in disks', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('RAID 0', 1.0, '0-disk safety', RED), ('RAID 1', 0.5, '50% usable', YELLOW), ('RAID 5', 0.75, 'n-1 usable', GREEN), ('RAID 6', 0.67, 'n-2 usable', TEAL), ('RAID 10', 0.5, '50% usable', CYAN)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'redundancy has a price in disks', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'RAID is not backup — it is uptime', font(F_SANS, 24), DIM, anchor="mm")
def scene_infr_subnet(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Subnetting: The Binary Truth', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'borrow bits, count subnets', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'hosts = 2^h - 2', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('borrowed bits', 2, '%d'), ('subnets', 4, '%d'), ('/26 hosts', 62, '%d')]
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
        txt(dr, (W // 2, 540), 'borrow bits, count subnets', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'subtract two — always subtract two', font(F_SANS, 24), DIM, anchor="mm")
def scene_infr_dns(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'DNS Lookup: The Full Walk', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('stub', 'recursive', 'root/TLD', 'authoritative', 'answer')
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
        txt(dr, (W // 2, 540), 'recursive asks, authoritative answers', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'flush the cache before you blame the zone', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# comptia-core (bbg x1 + primer x1 + story x1)
def scene_core_boot(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'POST to Desktop: The Boot Story', CYAN)
    _pts = [(140, 330), (360, 330), (580, 330), (800, 330), (1020, 330)]
    _labels = ('POST', 'bootloader', 'kernel', 'services', 'login')
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
        txt(dr, (W // 2, 540), 'every beep means something', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'one beep is good — three beeps is RAM', font(F_SANS, 24), DIM, anchor="mm")
def scene_core_ram(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'RAM Generations: Speed Doubles', CYAN)
    _items = [('DDR3', 0.25, '1600', ORANGE), ('DDR4', 0.5, '3200', YELLOW), ('DDR5', 1.0, '6400', GREEN)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'match the generation to the slot', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'speed doubles, the notch moves, slots stay honest', font(F_SANS, 24), DIM, anchor="mm")
def scene_core_troubleshoot(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Six-Step Method', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'method beats panic', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('identify: what changed, what broke', 5), ('theorize: most likely cause first', 9), ('test: one variable at a time', 13), ('implement the fix', 17), ('verify + document everything', 21)]
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
        txt(dr, (W // 2, 624), 'method beats panic', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'document — the step everyone skips and the exam loves', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# m365 (bbg x3)
def scene_m365_identity(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Entra ID: Identity Layers', CYAN)
    _layers = ('SSO tokens', 'conditional access', 'authentication', 'directory')
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
        txt(dr, (W // 2, 612), 'one identity, every app', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'passwordless is the destination', font(F_SANS, 24), DIM, anchor="mm")
def scene_m365_mailflow(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Mail Flow: The Exchange Path', CYAN)
    _boxes = ('receive', 'transport rules', 'hygiene', 'journal', 'deliver')
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
        txt(dr, (W // 2, 500), 'every message takes the tour', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'trace it in message trace — the mail never lies', font(F_SANS, 24), DIM, anchor="mm")
def scene_m365_compliance(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Compliance Pipeline', CYAN)
    _boxes = ('retain', 'hold', 'discover', 'audit')
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
        txt(dr, (W // 2, 500), 'retain, hold, discover', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'set retention before the lawyers call', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# ms-fundamentals (bbg x2 + story x1)
def scene_msf_cloudmodels(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'IaaS, PaaS, SaaS: The Pizza Story', CYAN)
    _boxes = ('on-prem', 'IaaS', 'PaaS', 'SaaS')
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
        txt(dr, (W // 2, 500), 'who manages what', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the line moves with each model — draw it', font(F_SANS, 24), DIM, anchor="mm")
def scene_msf_journey(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The Cloud Journey', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'from server room to cloud', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('assess: inventory everything', 5), ('lift: VMs to the cloud', 9), ('refactor: PaaS where it pays', 13), ('optimize: the never-ending tuning', 17), ('operate: cloud-native at last', 21)]
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
        txt(dr, (W // 2, 624), 'from server room to cloud', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'migration is a strategy — not a weekend', font(F_SERIF, 24), DIM, anchor="mm")
def scene_msf_zerotrust(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Zero Trust Pillars', CYAN)
    _layers = ('data', 'apps', 'identity', 'devices', 'network')
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
        txt(dr, (W // 2, 660), 'the VPN is not a moat', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# windows-admin (bbg x2 + fireship x1)
def scene_win_ad(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'AD Forest: The Trust Map', CYAN)
    _nodes = [('forest', 300, 280), ('tree-a', 560, 200), ('tree-b', 560, 380), ('domain', 900, 280)]
    _edges = [(0, 1), (0, 2), (0, 3)]
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
        txt(dr, (W // 2, 560), 'trusts are the roads between domains', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'draw the trust map before touching permissions', font(F_SANS, 24), DIM, anchor="mm")
def scene_win_gpo(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'GPO Processing Order', CYAN)
    _layers = ('OU', 'domain', 'site', 'local')
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
        txt(dr, (W // 2, 612), 'LSDOU — and enforced wins', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'gpupdate /force, then gpresult to prove it', font(F_SANS, 24), DIM, anchor="mm")
def scene_win_ps(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'PowerShell in 100 Seconds', MAGENTA)
    _lns = [('Get-Process |', (200, 200, 255)), ('  Where-Object {$_.CPU -gt 100} |', YELLOW), ('  Sort-Object CPU -Descending |', (200, 200, 255)), ('  Select-Object -First 5 Name, CPU', GREEN), ('# objects flow — properties, not text', DIM), ('# format last, never first', YELLOW)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'admin.ps1', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'objects, not text', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'format last — never first', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'cka': 'cka',
    'ckad': 'ckad',
    'k8sa': 'k8s-associate',
    'ocp': 'openshift',
    'lx': 'linux-essentials',
    'rhce': 'rhce',
    'rhcsa': 'rhcsa',
    'infr': 'comptia-infra',
    'core': 'comptia-core',
    'm365': 'm365',
    'msf': 'ms-fundamentals',
    'win': 'windows-admin',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'cka': 'CKA · K8s Administrator',
    'ckad': 'CKAD · K8s App Developer',
    'k8sa': 'K8S · Associate',
    'ocp': 'OPENSHIFT · Container Platform',
    'lx': 'LINUX · Essentials',
    'rhce': 'RHCE · Ansible Automation',
    'rhcsa': 'RHCSA · Linux Admin',
    'infr': 'INFRA+ · Server & Network',
    'core': 'CORE · A+ Essentials',
    'm365': 'M365 · Modern Workplace',
    'msf': 'MS-900 · MS Fundamentals',
    'win': 'WINDOWS · Server Admin',
}
VIDEOS = [
 # --- cka
 V(BOOTCAMP_K['cka'], 'cka', 'cka-pods', 'Pod Lifecycle: Born to Die',
   'cattle, not pets', 'bbg', scene_cka_pods,
   'Pod lifecycle: pending while scheduled, running while healthy, succeeded or failed when done — then garbage collected. Pods are cattle, not pets: design for their death.',
   [(4,10,'Pending: scheduled, waiting for resources'),
    (10,16,'Running: probes passing — liveness and readiness'),
    (16,22,'Succeeded/Failed: the job is done, one way or another'),
    (22,26,'Cattle, not pets — design for their death')]),
 V(BOOTCAMP_K['cka'], 'cka', 'cka-debug', 'Pod Debug Flow',
   'describe, logs, exec — in that order', 'primer', scene_cka_debug,
   'Debugging a pod: describe it for events, read the logs for the story, exec in for the live state. Describe, logs, exec — in that order, every time.',
   [(4,10,'Describe: the events confess first — OOMKilled?'),
    (10,16,"Logs: the application's own story"),
    (16,22,'Exec: live state — the shell of last resort'),
    (22,26,'In that order — discipline beats guessing')]),
 V(BOOTCAMP_K['cka'], 'cka', 'cka-etcd', "etcd Quorum: The Brain's Vote",
   'lose quorum, lose the cluster', 'bbg', scene_cka_etcd,
   'etcd needs a majority: 3 nodes survive 1 failure, 5 survive 2. Lose quorum and the cluster goes read-only — the brain cannot agree with itself.',
   [(4,10,'3 nodes: survive 1 failure — the minimum'),
    (10,16,'5 nodes: survive 2 — the production pick'),
    (16,22,'Quorum = majority — the math of agreement'),
    (22,26,'Lose quorum — the cluster goes read-only')]),
 # --- ckad
 V(BOOTCAMP_K['ckad'], 'ckad', 'ckad-deploy', 'Deployment YAML in 100 Seconds',
   'declare the desired state', 'fireship', scene_ckad_deploy,
   'A Deployment: apiVersion and kind, the replica count, the pod template with its container image. Apply it and the controller converges reality — declare the desired state, never the steps.',
   [(4,10,'apiVersion + kind: the what and the how-old'),
    (10,16,"Replicas: the desired count — the controller's promise"),
    (16,22,'Pod template: containers, image, ports'),
    (22,26,'kubectl apply — convergence, not commands')]),
 V(BOOTCAMP_K['ckad'], 'ckad', 'ckad-svc', 'Services: The Stable Address',
   'pods die — the service endures', 'bbg', scene_ckad_svc,
   "A Service gives dying pods a stable address: ClusterIP for inside, NodePort for a fixed port, LoadBalancer for the cloud's own balancer. Pods die — the service endures.",
   [(4,10,'ClusterIP: inside the cluster only — the default'),
    (10,16,'NodePort: a fixed port on every node'),
    (16,22,'LoadBalancer: the cloud provisions the front door'),
    (22,26,'Selectors bind it — labels are the wiring')]),
 V(BOOTCAMP_K['ckad'], 'ckad', 'ckad-config', 'Config Layers: Code vs Config',
   'twelve-factor: config leaves the image', 'bbg', scene_ckad_config,
   'Config layers: ConfigMaps for plain settings, Secrets for the sensitive, environment variables or mounted files to consume. Twelve-factor rule — config leaves the image.',
   [(4,10,'ConfigMap: plain settings — not secret, just separate'),
    (10,16,'Secret: base64, not encryption — know the difference'),
    (16,22,'Env vars or volume mounts — two ways to consume'),
    (22,26,'Config leaves the image — twelve-factor law')]),
 # --- k8s-associate
 V(BOOTCAMP_K['k8sa'], 'k8sa', 'k8sa-arch', 'Cluster Anatomy',
   'control plane decides, nodes execute', 'bbg', scene_k8sa_arch,
   'Cluster anatomy: the API server fronts everything, etcd remembers, the scheduler places, the controller manager converges — and kubelets on worker nodes just execute.',
   [(4,10,'API server: the front door — everything goes through it'),
    (10,16,'etcd: the memory — all state lives here'),
    (16,22,'Scheduler + controllers: place and converge'),
    (22,26,'Kubelet: the worker that executes')]),
 V(BOOTCAMP_K['k8sa'], 'k8sa', 'k8sa-sched', 'Scheduling: Finding a Home',
   'filters, then scores', 'primer', scene_k8sa_sched,
   'Scheduling: filter nodes by requirements, score the survivors, bind the pod to the winner. Taints repel, affinity attracts — the scheduler is a matchmaker with rules.',
   [(4,10,'Filter: requirements first — CPU, zones, taints'),
    (10,16,'Score: rank the survivors — spread the load'),
    (16,22,'Bind: the winner gets the pod'),
    (22,26,'Taints repel, affinity attracts')]),
 V(BOOTCAMP_K['k8sa'], 'k8sa', 'k8sa-net', 'Pod Networking: Flat and Simple',
   'every pod gets an IP — no NAT', 'bbg', scene_k8sa_net,
   'Pod networking: every pod gets a real IP, all pods talk without NAT, and the CNI plugin wires the flat network. No NAT inside the cluster — that simplicity is the whole design.',
   [(4,10,'Every pod gets an IP — real, routable'),
    (10,16,'No NAT inside — pods talk directly'),
    (16,22,'CNI plugin: the wiring — Calico, Cilium, Flannel'),
    (22,26,'Services add the stable front — kube-proxy routes')]),
 # --- openshift
 V(BOOTCAMP_K['ocp'], 'ocp', 'ocp-route', 'Route to Pod: The OpenShift Way',
   'routes are the front door', 'bbg', scene_ocp_route,
   "OpenShift traffic: the Route terminates TLS at the edge, the Service load-balances inside, the Pod serves. Routes are OpenShift's front door — Ingress wearing a Red Hat badge.",
   [(4,10,'Route: TLS terminates at the edge'),
    (10,16,'Service: load-balances to healthy pods'),
    (16,22,'Pod: serves the actual bytes'),
    (22,26,'oc expose — the fastest front door in the west')]),
 V(BOOTCAMP_K['ocp'], 'ocp', 'ocp-build', 'BuildConfig in 100 Seconds',
   'source in, image out', 'fireship', scene_ocp_build,
   'A BuildConfig: source in from git, strategy picks the builder, output to the image stream. Source in, image out — the cluster becomes the CI.',
   [(4,10,'Source: the git ref — what to build'),
    (10,16,'Strategy: source-to-image or Dockerfile'),
    (16,22,'Output: the image stream — versioned, triggerable'),
    (22,26,'Triggers: push code — the cluster builds')]),
 V(BOOTCAMP_K['ocp'], 'ocp', 'ocp-operator', 'Operator Lifecycle: Day Two',
   'install is day one — operate is forever', 'story', scene_ocp_operator,
   'The operator pattern: install the CRDs, deploy the controller, declare custom resources, and let the loop reconcile forever. Install is day one — operate is forever.',
   [(4,10,'CRDs: teach the API new words'),
    (10,16,'Controller: the loop that never sleeps'),
    (16,22,'Custom resources: declare what you want'),
    (22,26,'Reconcile forever — drift gets corrected')]),
 # --- linux-essentials
 V(BOOTCAMP_K['lx'], 'lx', 'lx-fhs', 'The Filesystem Hierarchy',
   'everything is a file', 'bbg', scene_lx_fhs,
   'The FHS: /bin for essentials, /etc for config, /var for changing data, /home for humans, /tmp for the transient. Everything is a file — learn the map before you wander.',
   [(4,10,'The root: every path starts here'),
    (10,16,'/etc holds config — /var holds change'),
    (16,22,'/home is human — /tmp is transient'),
    (22,26,'Learn the map before you wander')]),
 V(BOOTCAMP_K['lx'], 'lx', 'lx-perms', 'Permissions: The Octal Truth',
   '4-2-1: read, write, execute', '3b1b', scene_lx_perms,
   'Permissions: read is 4, write is 2, execute is 1 — add them per triplet. 755 for scripts, 644 for files, 600 for secrets. 4-2-1, and chmod stops being magic.',
   [(4,10,'Read=4, Write=2, Execute=1 — the only math'),
    (10,16,'Triplets: owner, group, other — three digits'),
    (16,22,'755: scripts — 644: files — 600: secrets'),
    (22,26,'4-2-1 and chmod stops being magic')]),
 V(BOOTCAMP_K['lx'], 'lx', 'lx-pipes', 'Pipes in 100 Seconds',
   'small tools, composed', 'fireship', scene_lx_pipes,
   "Pipes: each tool does one thing, stdout becomes the next tool's stdin, and ten small programs beat one big one. Small tools, composed — the Unix philosophy in one character.",
   [(4,10,'One tool, one job — grep finds, sort orders'),
    (10,16,'stdout → stdin: the composition'),
    (16,22,'Ten small tools beat one big program'),
    (22,26,'The pipe is the Unix philosophy in one character')]),
 # --- rhce
 V(BOOTCAMP_K['rhce'], 'rhce', 'rhce-playbook', 'Playbooks in 100 Seconds',
   'YAML that configures servers', 'fireship', scene_rhce_playbook,
   'An Ansible playbook: hosts to target, become for privilege, tasks in order — each task a module with arguments. YAML that configures servers, idempotent by design.',
   [(4,10,'Hosts: the targets — patterns, not lists'),
    (10,16,'become: privilege when needed — sudo, properly'),
    (16,22,'Tasks: modules with arguments — in order'),
    (22,26,'Idempotent: run it twice, change nothing twice')]),
 V(BOOTCAMP_K['rhce'], 'rhce', 'rhce-roles', 'Roles: Playbooks Grow Up',
   'reusable, shareable, tested', 'bbg', scene_rhce_roles,
   'Ansible roles: tasks, handlers, templates, and variables in a standard layout — reusable across playbooks, shareable via Galaxy, testable with Molecule. Playbooks grow up into roles.',
   [(4,10,'tasks/: the ordered work'),
    (10,16,'handlers/: restart-on-change logic'),
    (16,22,'templates/: Jinja2 configs with variables'),
    (22,26,'Galaxy + Molecule: share it, test it')]),
 V(BOOTCAMP_K['rhce'], 'rhce', 'rhce-idem', 'Idempotence: Run It Twice',
   'the second run changes nothing', 'primer', scene_rhce_idem,
   'Idempotence: the first run converges, the second run changes nothing — green means changed, and no-change is the goal. A script that appends every run is not automation, it is a bug on a schedule.',
   [(4,10,'First run: converges — packages installed, services on'),
    (10,16,'Second run: zero changes — the goal state holds'),
    (16,22,'Changed=0 is the passing grade'),
    (22,26,'Append-every-run scripts are bugs on a schedule')]),
 # --- rhcsa
 V(BOOTCAMP_K['rhcsa'], 'rhcsa', 'rhcsa-lvm', 'LVM: Disks, Abstracted',
   'resize without reinstalling', 'bbg', scene_rhcsa_lvm,
   'LVM layers: physical volumes join a volume group, logical volumes carve out space, filesystems sit on top. Resize, snapshot, migrate — without reinstalling anything.',
   [(4,10,'Physical volumes: raw disks, enlisted'),
    (10,16,'Volume group: the pooled capacity'),
    (16,22,'Logical volumes: carved slices — resizable live'),
    (22,26,'Snapshots: freeze time for backups')]),
 V(BOOTCAMP_K['rhcsa'], 'rhcsa', 'rhcsa-systemd', 'Boot Targets: The systemd Flow',
   'dependencies, not scripts', 'primer', scene_rhcsa_systemd,
   'systemd boot: targets pull in units, dependencies order them, and the default target decides where you land — multi-user or graphical. Dependencies, not scripts — the boot is a graph.',
   [(4,10,'Units: services, sockets, mounts — everything'),
    (10,16,'Dependencies order the graph — Wants and Requires'),
    (16,22,'Targets: multi-user vs graphical — the destination'),
    (22,26,'systemctl: the one command to rule the boot')]),
 V(BOOTCAMP_K['rhcsa'], 'rhcsa', 'rhcsa-users', 'Users in 100 Seconds',
   'every process wears a user', 'fireship', scene_rhcsa_users,
   "User management: useradd creates, passwd sets the secret, usermod adjusts, and sudo delegates precisely. Every process wears a user — identity is the OS's first security boundary.",
   [(4,10,'useradd: create — with a home and a shell'),
    (10,16,'passwd: the secret — never in the command line'),
    (16,22,'usermod -aG: groups grant powers'),
    (22,26,'sudo: delegate precisely — never share root')]),
 # --- comptia-infra
 V(BOOTCAMP_K['infr'], 'infr', 'infr-raid', 'RAID Levels: Pick Your Paranoia',
   'redundancy has a price in disks', '3b1b', scene_infr_raid,
   'RAID: 0 stripes for speed with zero safety, 1 mirrors for simple safety, 5 survives one disk, 6 survives two, 10 mirrors then stripes for both. Redundancy has a price in disks — pay it deliberately.',
   [(4,10,'RAID 0: striped, fast — one disk dies, all dies'),
    (10,16,'RAID 1: mirrored — simple, costs half'),
    (16,22,'RAID 5/6: parity — survive one, or two'),
    (22,26,'RAID 10: mirror then stripe — speed AND safety')]),
 V(BOOTCAMP_K['infr'], 'infr', 'infr-subnet', 'Subnetting: The Binary Truth',
   'borrow bits, count subnets', '3b1b', scene_infr_subnet,
   'Subnetting: the mask splits network from host, borrowing bits multiplies subnets, and each subnet loses two addresses — network and broadcast. Borrow bits, count subnets, subtract two.',
   [(4,10,'The mask: 1s are network, 0s are host'),
    (10,16,'Borrow n bits → 2^n subnets'),
    (16,22,'Each subnet loses 2 — network + broadcast'),
    (22,26,"/26 = 62 hosts — the exam's favorite")]),
 V(BOOTCAMP_K['infr'], 'infr', 'infr-dns', 'DNS Lookup: The Full Walk',
   'recursive asks, authoritative answers', 'primer', scene_infr_dns,
   'A DNS lookup: the stub asks the recursive resolver, which walks root to TLD to authoritative, caching every answer. Recursive asks, authoritative answers — and TTLs set the freshness.',
   [(4,10,'Stub: your machine asks its resolver'),
    (10,16,'Recursive: walks root → TLD → authoritative'),
    (16,22,"Authoritative: the domain's own truth"),
    (22,26,'Cache + TTL: speed with an expiry date')]),
 # --- comptia-core
 V(BOOTCAMP_K['core'], 'core', 'core-boot', 'POST to Desktop: The Boot Story',
   'every beep means something', 'primer', scene_core_boot,
   'Boot: POST checks the hardware, the bootloader finds the OS, the kernel loads drivers, services start, and the login appears. Every beep means something — count them before you panic.',
   [(4,10,'POST: hardware self-check — beeps are codes'),
    (10,16,"Bootloader: finds the OS — GRUB's menu"),
    (16,22,'Kernel + drivers: hardware meets software'),
    (22,26,'Services, then login — the desktop is the finish line')]),
 V(BOOTCAMP_K['core'], 'core', 'core-ram', 'RAM Generations: Speed Doubles',
   'match the generation to the slot', 'bbg', scene_core_ram,
   "RAM generations: DDR3 at 1600, DDR4 at 3200, DDR5 at 6400 — each doubles the last, none fit each other's slots. Match the generation to the slot — the notch is the enforcer.",
   [(4,10,'DDR3: 1600 MT/s — the old guard'),
    (10,16,'DDR4: 3200 MT/s — double, new notch'),
    (16,22,'DDR5: 6400 MT/s — double again, on-die ECC'),
    (22,26,'The notch enforces honesty — slots reject strangers')]),
 V(BOOTCAMP_K['core'], 'core', 'core-troubleshoot', 'The Six-Step Method',
   'method beats panic', 'story', scene_core_troubleshoot,
   "CompTIA's six steps: identify the problem, theorize, test the theory, plan, implement, verify and document. Method beats panic — the exam grades the process, not the guess.",
   [(4,10,'Identify: gather, question, reproduce'),
    (10,16,'Theorize: probable cause first — then test'),
    (16,22,'Test: one change at a time'),
    (22,26,'Implement, verify, document — close the loop')]),
 # --- m365
 V(BOOTCAMP_K['m365'], 'm365', 'm365-identity', 'Entra ID: Identity Layers',
   'one identity, every app', 'bbg', scene_m365_identity,
   'Entra ID layers: the user authenticates once, Conditional Access evaluates risk, SSO tokens flow to every app. One identity, every app — passwordless is the destination.',
   [(4,10,'Authentication: prove the human — MFA, FIDO2'),
    (10,16,'Conditional Access: risk-weighed decisions'),
    (16,22,'SSO: tokens, not passwords, to every app'),
    (22,26,'Passwordless: the destination — phishing dies here')]),
 V(BOOTCAMP_K['m365'], 'm365', 'm365-mailflow', 'Mail Flow: The Exchange Path',
   'every message takes the tour', 'bbg', scene_m365_mailflow,
   'Exchange mail flow: the message arrives, transport rules inspect, anti-spam and anti-malware scan, journaling archives a copy, then delivery. Every message takes the tour — even the spam.',
   [(4,10,'Transport rules: the policy checkpoints'),
    (10,16,'Anti-spam + anti-malware: the bouncers'),
    (16,22,'Journaling: the archive copy — compliance'),
    (22,26,'Delivery: inbox, finally')]),
 V(BOOTCAMP_K['m365'], 'm365', 'm365-compliance', 'Compliance Pipeline',
   'retain, hold, discover', 'bbg', scene_m365_compliance,
   'The compliance pipeline: retention policies keep what matters, holds freeze what is litigated, eDiscovery finds it for counsel. Retain, hold, discover — in that order, before the lawyers call.',
   [(4,10,'Retention: keep what matters — delete the rest'),
    (10,16,'Holds: freeze it — litigation waits for no one'),
    (16,22,'eDiscovery: search everything, export for counsel'),
    (22,26,'Audit logs: who did what — the permanent record')]),
 # --- ms-fundamentals
 V(BOOTCAMP_K['msf'], 'msf', 'msf-cloudmodels', 'IaaS, PaaS, SaaS: The Pizza Story',
   'who manages what', 'bbg', scene_msf_cloudmodels,
   'Cloud models: IaaS rents the kitchen, PaaS rents the kitchen with the recipe, SaaS serves the finished pizza. Who manages what — the shared responsibility line moves with each model.',
   [(4,10,'IaaS: you manage the OS up — VMs'),
    (10,16,'PaaS: you manage the app — the platform handles the rest'),
    (16,22,'SaaS: you use it — M365, done'),
    (22,26,'The line moves — know who owns what')]),
 V(BOOTCAMP_K['msf'], 'msf', 'msf-journey', 'The Cloud Journey',
   'from server room to cloud', 'story', scene_msf_journey,
   'The journey: lift the VMs, refactor the apps, go cloud-native, then optimize forever. From server room to cloud — migration is a strategy, not a weekend.',
   [(4,10,'Assess: what do we actually have'),
    (10,16,'Lift: VMs move first — quick wins'),
    (16,22,'Refactor: PaaS where it pays'),
    (22,26,'Optimize: rightsizing never ends')]),
 V(BOOTCAMP_K['msf'], 'msf', 'msf-zerotrust', 'Zero Trust Pillars',
   'never trust, always verify', 'bbg', scene_msf_zerotrust,
   'Zero Trust: verify identity explicitly, use least-privilege access, assume breach in every design. Never trust, always verify — the network location means nothing.',
   [(4,10,'Verify explicitly: identity, device, risk — every time'),
    (10,16,'Least privilege: just enough, just in time'),
    (16,22,'Assume breach: segment, encrypt, monitor'),
    (22,26,'Location means nothing — the VPN is not a moat')]),
 # --- windows-admin
 V(BOOTCAMP_K['win'], 'win', 'win-ad', 'AD Forest: The Trust Map',
   'trusts are the roads between domains', 'bbg', scene_win_ad,
   'Active Directory: domains group objects, trees share a namespace, forests share a schema — and trusts are the roads between them. Draw the trust map before you touch the permissions.',
   [(4,10,'Domain: the security boundary — users, computers, OUs'),
    (10,16,'Tree: contiguous namespace — child domains'),
    (16,22,'Forest: the schema boundary — the widest trust'),
    (22,26,'Trusts: the roads — transitive inside, explicit outside')]),
 V(BOOTCAMP_K['win'], 'win', 'win-gpo', 'GPO Processing Order',
   'LSDOU — and enforced wins', 'bbg', scene_win_gpo,
   "GPO order: Local, Site, Domain, OU — later wins, unless Enforced or Block Inheritance intervenes. LSDOU, and enforced wins — the exam's favorite acronym.",
   [(4,10,"Local: the machine's own policy — weakest"),
    (10,16,'Site, then Domain: widening scope'),
    (16,22,'OU: closest to the object — wins by default'),
    (22,26,'Enforced beats Block — know the exceptions')]),
 V(BOOTCAMP_K['win'], 'win', 'win-ps', 'PowerShell in 100 Seconds',
   'objects, not text', 'fireship', scene_win_ps,
   'PowerShell: cmdlets emit objects, the pipeline passes them whole, and Where-Object plus Select-Object shape the answer. Objects, not text — the pipeline is typed.',
   [(4,10,'Cmdlets: Verb-Noun — Get-Process, Stop-Service'),
    (10,16,'Objects flow — not text, real properties'),
    (16,22,'Where-Object filters — Select-Object shapes'),
    (22,26,'The pipeline is typed — format last, never first')]),
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
