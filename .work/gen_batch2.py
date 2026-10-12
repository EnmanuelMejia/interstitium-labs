#!/usr/bin/env python3
"""Batch 2 video generator: IL-08..IL-14, 21 videos x 30s, 1280x720 @ 24fps.
Mirrors gen_batch1.py: silent h264 MP4s, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / 3b1b / fireship / bbg / primer. Original animations only.
"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import random as _r

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

# ============================================================ IL-08: Algorithms / Compilers / Distributed
_DIJ_NODES = {"A": (300, 230), "B": (530, 150), "C": (750, 190), "D": (990, 170),
              "E": (430, 490), "F": (710, 480), "G": (960, 480)}
_DIJ_EDGES = [("A", "B", 4), ("A", "E", 2), ("B", "C", 3), ("B", "F", 7),
              ("C", "D", 2), ("C", "F", 5), ("E", "F", 4), ("F", "G", 3),
              ("E", "B", 6)]
_DIJ_ORDER = ["A", "E", "B", "F", "C", "D", "G"]
_DIJ_DIST = {"A": 0, "E": 2, "B": 4, "F": 6, "C": 7, "D": 9, "G": 9}
_DIJ_TREE = [("A", "E"), ("A", "B"), ("E", "F"), ("B", "C"), ("F", "G"), ("C", "D")]

def scene_dijkstra(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "Dijkstra: shortest paths from A",
        font(F_BOLD, 44), WHITE, anchor="mm")
    born = {n: 4 + i * 2.0 for i, n in enumerate(_DIJ_ORDER)}
    settled = {n for n in born if t >= born[n]}
    for a, b, w in _DIJ_EDGES:
        x0, y0 = _DIJ_NODES[a]; x1, y1 = _DIJ_NODES[b]
        tree = (a, b) in _DIJ_TREE or (b, a) in _DIJ_TREE
        dr.line([x0, y0, x1, y1], fill=(60, 80, 140), width=3)
        if tree and b in settled and a in settled:
            dr.line([x0, y0, x1, y1], fill=GREEN, width=5)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 16
        txt(dr, (mx, my), str(w), font(F_MONO, 22), DIM, anchor="mm")
    for n, (x, y) in _DIJ_NODES.items():
        if n not in settled:
            dr.ellipse([x - 26, y - 26, x + 26, y + 26], outline=(70, 80, 120), width=3)
            continue
        pulse = 0.5 + 0.5 * math.sin(t * 5)
        glow = TEAL if n != "A" else YELLOW
        glow_box(dr, [x - 30, y - 30, x + 30, y + 30], glow, rad=14, layers=2)
        dr.ellipse([x - 30, y - 30, x + 30, y + 30], fill=(10, 20, 50), outline=glow, width=3)
        txt(dr, (x, y - 4), n, font(F_BOLD, 30), WHITE, anchor="mm")
        txt(dr, (x, y + 18), str(_DIJ_DIST[n]), font(F_MONO, 22), glow, anchor="mm")
    # final path A -> E -> F -> G highlighted
    if t > 22:
        path = ["A", "E", "F", "G"]
        for i in range(len(path) - 1):
            x0, y0 = _DIJ_NODES[path[i]]; x1, y1 = _DIJ_NODES[path[i + 1]]
            dr.line([x0, y0, x1, y1], fill=YELLOW, width=8)
        txt(dr, (W // 2, 640), "A \u2192 E \u2192 F \u2192 G  cost 9  \u2014 greedy, optimal",
            font(F_BOLD, 32), YELLOW, anchor="mm")

def scene_compiler(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    lines = [("int main() {", (200, 200, 255)),
             ("  return 40 + 2;", (0, 229, 255)),
             ("}", (200, 200, 255))]
    code_panel(dr, 40, 130, 400, 560, "main.c", lines,
               hi_line=min(1, int((t - 4) / 8)), t=t)
    phases = [("LEX", CYAN, 500), ("PARSE", MAGENTA, 680), ("IR", YELLOW, 860), ("CODEGEN", GREEN, 1040)]
    for name, col, x in phases:
        idx = phases.index((name, col, x))
        on = t >= 6 + idx * 4.5
        glow_box(dr, [x - 70, 150, x + 70, 220], col if on else (60, 60, 100), rad=10, layers=2)
        dr.rectangle([x - 70, 150, x + 70, 220], fill=(12, 12, 26))
        txt(dr, (x, 185), name, font(F_BOLD, 26), col if on else DIM, anchor="mm")
        if idx < 3:
            arrow(dr, x + 72, 185, x + 108, 185, DIM, 4)
    # tokens stream (phase 1)
    toks = ["int", "main", "(", ")", "{", "return", "40", "+", "2", ";", "}"]
    if t > 6:
        for i, tk in enumerate(toks):
            if t < 6 + i * 0.5:
                continue
            x = 470 + (i % 4) * 120; y = 280 + (i // 4) * 60
            if x > 1200:
                continue
            dr.rounded_rectangle([x, y, x + 105, y + 44], radius=8, outline=CYAN, width=2)
            txt(dr, (x + 52, y + 22), tk, font(F_MONO, 20), WHITE, anchor="mm")
    # asm output (phase 4)
    if t > 20:
        glow_box(dr, [470, 500, 1210, 640], GREEN, rad=12, layers=2)
        dr.rectangle([470, 500, 1210, 640], fill=(10, 14, 20))
        asm = ["mov eax, 42", "ret"]
        for i, ln in enumerate(asm):
            txt(dr, (500, 540 + i * 40), ln, font(F_MONO, 26), GREEN, anchor="lm")
        txt(dr, (900, 540), "the machine runs numbers", font(F_SANS, 24), DIM, anchor="lm")
    txt(dr, (W // 2, 60), "A compiler: text \u2192 tokens \u2192 tree \u2192 machine code",
        font(F_BOLD, 34), WHITE, anchor="mm")

def scene_paxos(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Paxos Consensus", BLUE)
    panel(dr, [60, 200, 300, 520], "PROPOSER", BLUE, 26)
    txt(dr, (180, 400), "P", font(F_BOLD, 60), BLUE, anchor="mm")
    accs = [("A1", 560), ("A2", 760), ("A3", 960)]
    for name, x in accs:
        glow_box(dr, [x - 70, 200, x + 70, 330], TEAL, rad=12, layers=2)
        dr.rectangle([x - 70, 200, x + 70, 330], fill=(12, 16, 34))
        txt(dr, (x, 245), name, font(F_BOLD, 28), TEAL, anchor="mm")
        txt(dr, (x, 295), "acceptor", font(F_SANS, 20), DIM, anchor="mm")
    panel(dr, [1060, 200, 1220, 520], "LEARNER", GREEN, 26)
    txt(dr, (1140, 400), "L", font(F_BOLD, 60), GREEN, anchor="mm")
    for i, (_, x) in enumerate(accs):
        arrow(dr, 310, 280 + i * 60, x - 70, 280 + i * 60, DIM, 4)
        arrow(dr, x + 70, 380 + i * 40, 1050, 380 + i * 40, DIM, 4)
    # Phase 1: prepare/promises
    if 4 < t < 14:
        k = ease((t - 4) / 3)
        for i, (_, x) in enumerate(accs):
            px = lerp(310, x - 70, clamp(k - i * 0.15))
            dr.ellipse([px - 9, 265 - 9, px + 9, 265 + 9], fill=YELLOW)
        txt(dr, (W // 2, 600), "phase 1: PREPARE(n) \u2192 PROMISE", font(F_BOLD, 30), YELLOW, anchor="mm")
    if 10 < t < 20:
        k = ease((t - 10) / 3)
        for i, (_, x) in enumerate(accs):
            px = lerp(x + 70, 1050, clamp(k - i * 0.15))
            dr.ellipse([px - 9, 400 - 9, px + 9, 400 + 9], fill=TEAL)
        if t >= 14:
            txt(dr, (W // 2, 600), "phase 2: ACCEPT(n, v) \u2192 ACCEPTED", font(F_BOLD, 30), TEAL, anchor="mm")
    if t >= 20:
        glow_box(dr, [1060, 200, 1220, 520], GREEN, rad=14)
        txt(dr, (W // 2, 600), "quorum reached \u2014 value COMMITTED", font(F_BOLD, 32), GREEN, anchor="mm")
        txt(dr, (1140, 460), "\u2713", font(F_BOLD, 48), GREEN, anchor="mm")

# ============================================================ IL-09: Certification Command
def scene_comptia(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "The CompTIA Certification Ladder", BLUE)
    tiers = [("SecurityX", "expert", MAGENTA, 560, 300),
             ("CySA+  \u00b7  PenTest+", "advanced", ORANGE, 460, 520),
             ("Network+  \u00b7  Security+", "core", TEAL, 380, 740),
             ("A+", "foundation", BLUE, 300, 960)]
    for name, sub, col, wdt, y in tiers:
        idx = tiers.index((name, sub, col, wdt, y))
        on = t >= 5 + idx * 3.5
        x0, x1 = W // 2 - wdt // 2, W // 2 + wdt // 2
        if on:
            glow_box(dr, [x0, y, x1, y + 90], col, rad=12, layers=2)
        dr.rectangle([x0, y, x1, y + 90], fill=(12, 16, 34), outline=col if on else (60, 60, 90), width=3)
        txt(dr, (W // 2, y + 34), name, font(F_BOLD, 30), col if on else DIM, anchor="mm")
        txt(dr, (W // 2, y + 66), sub, font(F_SANS, 20), DIM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 250 - 90 + 0), "stack credentials: each tier unlocks the next",
            font(F_BOLD, 28), WHITE, anchor="mm")
        txt(dr, (W // 2, 690), "vendor tracks (Cisco \u00b7 AWS \u00b7 Azure) run in parallel",
            font(F_SANS, 26), DIM, anchor="mm")

def scene_entropy(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    txt(dr, (W // 2, 70), "Password Entropy: length wins", font(F_BOLD, 44), WHITE, anchor="mm")
    k = ease(clamp((t - 5) / 15))
    L = int(lerp(4, 12, k))
    bits = L * 6.2
    pw = "Tr0ub4dor&3xQ"[:L]
    f = font(F_MONOB, 56)
    cx = W // 2
    x0 = cx - dr.textlength(pw, font=f) / 2
    for i, ch in enumerate(pw):
        col = GREEN if i < 8 else (YELLOW if i < 11 else CYAN)
        txt(dr, (x0 + dr.textlength(pw[:i], font=f) + dr.textlength(ch, font=f) / 2, 200),
            ch, f, col, anchor="mm")
    txt(dr, (cx, 300), "%d characters \u00d7 6.2 bits \u2248 %.0f bits of entropy" % (L, bits),
        font(F_BOLD, 32), WHITE, anchor="mm")
    # entropy bar
    dr.rectangle([180, 360, 1100, 410], fill=(20, 30, 50), outline=DIM, width=2)
    dr.rectangle([180, 360, 180 + 920 * clamp(bits / 80), 410], fill=CYAN)
    # crack time estimate (offline, 1e10 guesses/s): 2^(bits-1)/1e10 seconds
    import math as _m
    secs = 2 ** max(0, bits - 1) / 1e10
    if secs < 60:
        lbl = "%.0f seconds" % secs
    elif secs < 3600:
        lbl = "%.0f minutes" % (secs / 60)
    elif secs < 86400 * 365:
        lbl = "%.1f days" % (secs / 86400)
    else:
        lbl = "%.0f years" % (secs / (86400 * 365))
    txt(dr, (cx, 470), "offline crack time \u2248 " + lbl, font(F_BOLD, 36),
        RED if secs < 86400 else GREEN, anchor="mm")
    txt(dr, (cx, 540), "every extra character multiplies the search space \u00d7~72",
        font(F_SANS, 28), DIM, anchor="mm")
    if t > 22:
        txt(dr, (cx, 610), "use a password manager \u2014 humans are bad at randomness",
            font(F_BOLD, 28), YELLOW, anchor="mm")

def scene_oauth(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "OAuth 2.0: the authorization code flow", font(F_BOLD, 38), WHITE, anchor="mm")
    cols = [("USER", 180, MAGENTA), ("CLIENT", 480, CYAN), ("AUTH SRV", 800, YELLOW), ("RESOURCE", 1100, GREEN)]
    for name, x, col in cols:
        glow_box(dr, [x - 110, 120, x + 110, 190], col, rad=10, layers=2)
        dr.rectangle([x - 110, 120, x + 110, 190], fill=(12, 12, 26))
        txt(dr, (x, 155), name, font(F_BOLD, 24), col, anchor="mm")
        dr.line([x, 190, x, 660], fill=(60, 60, 100), width=2)
    steps = [
        (0, 1, "1. authorize?", MAGENTA),
        (1, 2, "2. redirect + code", CYAN),
        (0, 2, "3. approve (login)", YELLOW),
        (1, 2, "4. code \u2192 tokens", YELLOW),
        (1, 3, "5. access token \u2192 data", GREEN),
    ]
    for i, (a, b, label, col) in enumerate(steps):
        born = 5 + i * 3.6
        if t < born:
            continue
        y = 250 + i * 80
        xa, xb = cols[a][1], cols[b][1]
        arrow(dr, xa, y, xb, y, col, 5)
        mx = (xa + xb) / 2
        txt(dr, (mx, y - 22), label, font(F_BOLD, 22), col, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 620), "the client never sees your password \u2014 only scoped tokens",
            font(F_BOLD, 30), GREEN, anchor="mm")

# ============================================================ IL-10: Portfolio, Career & Professional Practice
def scene_career_arc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    for r in range(340, 0, -25):
        c = int(lerp(6, 40, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 12, c + 4, c - 2), width=2)
    txt(dr, (W // 2, 80), "THE CAREER ARC", font(F_SERIFB, 40), GOLD, anchor="mm")
    pts = [(140, 520), (430, 380), (700, 470), (980, 300), (1140, 200)]
    dr.line(pts, fill=(120, 100, 60), width=6)
    acts = [("APPRENTICE", "learn the craft", pts[1]),
            ("BUILDER", "ship real systems", pts[3]),
            ("FOUNDER", "own the outcome", pts[4])]
    for name, sub, (x, y) in acts:
        idx = acts.index((name, sub, (x, y)))
        on = t >= 5 + idx * 6
        if on:
            dr.ellipse([x - 46, y - 46, x + 46, y + 46], fill=(40, 30, 10), outline=GOLD, width=3)
            txt(dr, (x, y), str(idx + 1), font(F_SERIFB, 36), GOLD, anchor="mm")
            txt(dr, (x, y + 78), name, font(F_SERIFB, 28), CREAM, anchor="mm")
            txt(dr, (x, y + 112), sub, font(F_SERIF, 22), (200, 185, 160), anchor="mm")
        else:
            dr.ellipse([x - 30, y - 30, x + 30, y + 30], outline=(80, 70, 50), width=2)
    # traveler dot
    k = clamp((t - 5) / 18)
    seg = min(3, int(k * 4))
    if k > 0:
        x0, y0 = pts[seg]; x1, y1 = pts[seg + 1]
        u = k * 4 - seg
        tx, ty = lerp(x0, x1, u), lerp(y0, y1, u)
        dr.ellipse([tx - 12, ty - 12, tx + 12, ty + 12], fill=GOLD)
    if t > 23:
        txt(dr, (W // 2, 640), "careers compound like interest \u2014 skills reinvested yearly",
            font(F_SERIF, 28), (200, 185, 160), anchor="mm")

def scene_offer(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Negotiating the Offer", BLUE)
    rows = [("their first offer", 72, (150, 150, 180)),
            ("market band", 85, TEAL),
            ("your target", 105, GREEN)]
    scale = lambda k: 120 + k / 130 * 1040
    # market band
    dr.rectangle([scale(85), 300, scale(110), 380], fill=(10, 44, 42), outline=TEAL, width=3)
    txt(dr, (scale(97), 340), "$85\u2013$110k band", font(F_BOLD, 24), TEAL, anchor="mm")
    for i, (label, kval, col) in enumerate(rows):
        born = 5 + i * 4
        if t < born:
            continue
        y = 440 + i * 70
        dr.line([scale(60), y, scale(120), y], fill=(40, 50, 80), width=2)
        x = scale(kval)
        dr.ellipse([x - 10, y - 10, x + 10, y + 10], fill=col)
        dr.line([x, y, x, 400], fill=col, width=2)
        txt(dr, (140, y), label, font(F_BOLD, 24), col, anchor="lm")
        txt(dr, (x + 20, y), "$%dk" % kval, font(F_MONOB, 24), WHITE, anchor="lm")
    tips = ["never accept the first number", "anchor on market data, not history",
            "negotiate the whole package", "silence is a tactic"]
    for i, tip in enumerate(tips):
        if t < 15 + i * 2.2:
            continue
        txt(dr, (W // 2, 250 - 0 + 0 + 0), "", font(F_SANS, 1), DIM, anchor="mm")
    if t > 17:
        for i, tip in enumerate(tips):
            if t < 17 + i * 2:
                continue
            txt(dr, (1040, 170 + i * 34), "\u2713 " + tip, font(F_SANS, 24), GREEN, anchor="lm")

def scene_compound(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    txt(dr, (W // 2, 70), "Compound Interest: the eighth wonder", font(F_BOLD, 44), WHITE, anchor="mm")
    # stacked bars: $10k/yr for 30 years at 8%
    P, r = 10000, 0.08
    vals = []
    for yr in range(0, 31, 5):
        total = P * ((1 + r) ** yr - 1) / r if yr else 0
        contrib = P * yr
        vals.append((yr, contrib, total))
    k = clamp((t - 5) / 16)
    nshow = int(k * len(vals)) + (1 if k > 0 else 0)
    bw = 150
    x0 = 140
    for i, (yr, contrib, total) in enumerate(vals):
        if i >= nshow:
            continue
        x = x0 + i * 165
        h_tot = total / 1220000 * 400
        h_con = contrib / 1220000 * 400
        dr.rectangle([x, 580 - h_tot, x + bw, 580], fill=(0, 120, 130))
        dr.rectangle([x, 580 - h_con, x + bw, 580], fill=(0, 80, 160), outline=CYAN, width=2)
        txt(dr, (x + bw / 2, 610), "yr %d" % yr, font(F_BOLD, 22), DIM, anchor="mm")
        if h_tot > 40:
            txt(dr, (x + bw / 2, 580 - h_tot - 20), "$%dk" % int(total / 1000),
                font(F_BOLD, 22), YELLOW, anchor="mm")
    txt(dr, (200, 200), "contributions", font(F_BOLD, 24), CYAN, anchor="lm")
    txt(dr, (200, 240), "growth (interest)", font(F_BOLD, 24), TEAL, anchor="lm")
    if t > 22:
        txt(dr, (W // 2, 150), "$300k in \u2192 $1.22M out at 8% \u00b7 time does the work",
            font(F_BOLD, 32), YELLOW, anchor="mm")

# ============================================================ IL-11: Zero Trust & Endpoint Defense
def scene_ztt(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Zero Trust: Never Trust, Always Verify", BLUE)
    txt(dr, (180, 220), "USER +\nDEVICE", font(F_BOLD, 26), BLUE, anchor="mm")
    dr.ellipse([140, 260, 220, 340], outline=BLUE, width=3)
    txt(dr, (180, 300), "\U0001F464", font(F_SANS, 40), BLUE, anchor="mm")
    panel(dr, [420, 180, 860, 420], "POLICY ENGINE", CYAN, 28)
    checks = ["identity", "device health", "location", "risk score"]
    for i, c in enumerate(checks):
        on = t >= 6 + i * 1.8
        txt(dr, (640, 250 + i * 40), ("\u2713 " if on else "\u25cb ") + c,
            font(F_SANS, 24), GREEN if on else DIM, anchor="mm")
    for x, name in [(1000, "APP"), (1130, "DATA")]:
        glow_box(dr, [x - 60, 240, x + 60, 360], TEAL, rad=12, layers=2)
        dr.rectangle([x - 60, 240, x + 60, 360], fill=(12, 16, 34))
        txt(dr, (x, 300), name, font(F_BOLD, 26), TEAL, anchor="mm")
    # request 1: verified -> allow
    if 8 < t < 17:
        k = ease(clamp((t - 8) / 4))
        px = lerp(230, 420, k)
        dr.ellipse([px - 10, 300 - 10, px + 10, 300 + 10], fill=WHITE)
        if t > 13:
            k2 = ease(clamp((t - 13) / 3))
            for x in (1000, 1130):
                px2 = lerp(860, x - 60, k2)
                dr.ellipse([px2 - 10, 300 - 10, px2 + 10, 300 + 10], fill=GREEN)
        txt(dr, (W // 2, 500), "request 1: all checks pass \u2192 ALLOW", font(F_BOLD, 30), GREEN, anchor="mm")
    # request 2: compromised device -> deny
    if t >= 17:
        txt(dr, (W // 2, 500), "request 2: device unpatched \u2192 DENY", font(F_BOLD, 30), RED, anchor="mm")
        dr.line([860, 280, 1000, 280], fill=RED, width=6)
        txt(dr, (930, 250), "\u2717", font(F_BOLD, 48), RED, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 580), "every request re-verified \u2014 no implicit trust",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_allowlist(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Application Allowlisting", BLUE)
    apps = [("chrome.exe", "signed", GREEN, 300),
            ("updater.exe", "signed", GREEN, 640),
            ("malware.exe", "UNSIGNED", RED, 980)]
    panel(dr, [420, 420, 860, 620], "ALLOWLIST DB", CYAN, 26)
    txt(dr, (640, 510), "SHA-256 hashes\nof approved apps", font(F_MONO, 22), DIM, anchor="mm")
    for name, sig, col, x in apps:
        idx = apps.index((name, sig, col, x))
        born = 5 + idx * 3
        if t < born:
            continue
        glow_box(dr, [x - 130, 160, x + 130, 280], col, rad=12, layers=2)
        dr.rectangle([x - 130, 160, x + 130, 280], fill=(12, 16, 34))
        txt(dr, (x, 205), name, font(F_MONOB, 26), WHITE, anchor="mm")
        txt(dr, (x, 248), sig, font(F_BOLD, 22), col, anchor="mm")
        if t > born + 2:
            # check arrow down to DB
            arrow(dr, x, 290, 640, 410, DIM, 4)
        if t > born + 3.5:
            if col == GREEN:
                txt(dr, (x, 330), "RUN \u2713", font(F_BOLD, 30), GREEN, anchor="mm")
            else:
                txt(dr, (x, 330), "BLOCKED \u2717", font(F_BOLD, 30), RED, anchor="mm")
                dr.line([x - 40, 200, x + 40, 280], fill=RED, width=6)
                dr.line([x - 40, 280, x + 40, 200], fill=RED, width=6)
    if t > 22:
        txt(dr, (W // 2, 670), "default-deny: if it is not listed, it does not run",
            font(F_BOLD, 30), WHITE, anchor="mm")

def scene_condaccess(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "Conditional Access: policy as code", font(F_BOLD, 38), WHITE, anchor="mm")
    panel(dr, [60, 140, 420, 640], "SIGNALS", DIM, 26)
    sigs = [("location: office", GREEN), ("device: compliant", GREEN),
            ("risk: medium", YELLOW), ("app: email", CYAN)]
    for i, (s, col) in enumerate(sigs):
        on = t >= 5 + i * 1.5
        txt(dr, (240, 260 + i * 70), s, font(F_SANS, 26), col if on else DIM, anchor="mm")
    # decision tree
    nodes = [("risk < high?", 760, 200, YELLOW),
             ("device compliant?", 640, 360, CYAN),
             ("location known?", 880, 360, CYAN)]
    for name, x, y, col in nodes:
        on = t >= 10 + nodes.index((name, x, y, col)) * 2.5
        dr.rounded_rectangle([x - 130, y - 40, x + 130, y + 40], radius=14,
                             outline=col if on else (60, 60, 100), width=3)
        dr.rectangle([x - 130, y - 40, x + 130, y + 40], fill=(12, 12, 26))
        txt(dr, (x, y), name, font(F_BOLD, 24), col if on else DIM, anchor="mm")
    if t > 12:
        arrow(dr, 760, 240, 640, 318, DIM, 4)
        arrow(dr, 760, 240, 880, 318, DIM, 4)
    if t > 18:
        glow_box(dr, [560, 480, 960, 600], YELLOW, rad=14)
        dr.rectangle([560, 480, 960, 600], fill=(30, 26, 8))
        txt(dr, (760, 530), "GRANT + REQUIRE MFA", font(F_BOLD, 32), YELLOW, anchor="mm")
        txt(dr, (760, 570), "medium risk \u2192 step up auth", font(F_SANS, 24), DIM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 670), "signals in \u2192 policy evaluates \u2192 access decision out",
            font(F_BOLD, 28), WHITE, anchor="mm")

# ============================================================ IL-12: AI Engineering
def scene_attention(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "Attention: the query picks its context", font(F_BOLD, 42), WHITE, anchor="mm")
    toks = ["the", "cat", "sat", "on", "the", "mat"]
    wts = [0.05, 0.35, 0.10, 0.08, 0.07, 0.35]  # query = "sat" attends to cat/mat
    k = ease(clamp((t - 6) / 12))
    x0 = 200
    for i, tk in enumerate(toks):
        x = x0 + i * 150
        # key cell
        dr.rounded_rectangle([x - 60, 200, x + 60, 270], radius=10,
                             outline=TEAL, width=3)
        dr.rectangle([x - 60, 200, x + 60, 270], fill=(10, 20, 50))
        q = (i == 2)
        txt(dr, (x, 235), tk, font(F_BOLD, 30), YELLOW if q else WHITE, anchor="mm")
        # weight bar
        bw = wts[i] * 420 * k
        dr.rectangle([x - 60, 300, x + 60, 340], fill=(25, 30, 60))
        dr.rectangle([x - 60, 300, x - 60 + bw, 340], fill=MAGENTA)
        txt(dr, (x, 370), "%.2f" % (wts[i] * k), font(F_MONO, 22), MAGENTA, anchor="mm")
        # attention link from query
        if k > 0.05:
            qx = x0 + 2 * 150
            al = int(40 + 160 * wts[i])
            dr.line([qx, 270, x, 300], fill=(al, 40, 120), width=max(2, int(wts[i] * 14 * k)))
    txt(dr, (W // 2, 450), 'query "sat" \u2192 strongest links: cat, mat',
        font(F_BOLD, 32), YELLOW, anchor="mm")
    if t > 21:
        glow_box(dr, [340, 500, 940, 620], MAGENTA, rad=14)
        dr.rectangle([340, 500, 940, 620], fill=(30, 10, 28))
        txt(dr, (W // 2, 548), "output = \u03a3 weight\u1d62 \u00b7 value\u1d62",
            font(F_BOLD, 34), MAGENTA, anchor="mm")
        txt(dr, (W // 2, 590), "softmax(QK\u1d40/\u221ad) \u00b7 V", font(F_MONO, 26), DIM, anchor="mm")

def scene_embeddings(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "Word Embeddings: meaning as geometry", font(F_BOLD, 42), WHITE, anchor="mm")
    cx, cy, S = W // 2, 400, 90
    words = {"king": (-1.6, 0.8, TEAL), "queen": (-0.6, 1.0, TEAL),
             "man": (-1.5, -0.6, CYAN), "woman": (-0.5, -0.4, CYAN),
             "apple": (1.4, 0.6, GREEN), "car": (1.5, -0.7, GREEN)}
    k = ease(clamp((t - 5) / 12))
    for w, (wx, wy, col) in words.items():
        px = cx + wx * S * k + cx * (1 - k) * 0
        py = cy - wy * S * k
        dr.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col)
        txt(dr, (px, py - 28), w, font(F_BOLD, 26), col, anchor="mm")
    # king - man + woman = queen arrow demo
    if t > 18:
        k2p = (cx + -1.6 * S, cy - 0.8 * S)
        qp = (cx + -0.6 * S, cy - 1.0 * S)
        arrow(dr, k2p[0] + 30, k2p[1] - 30, qp[0] - 20, qp[1] + 10, YELLOW, 5)
        txt(dr, (cx - 2.2 * S, cy - 1.9 * S), "king \u2212 man + woman \u2248 queen",
            font(F_BOLD, 28), YELLOW, anchor="mm")
    txt(dr, (W // 2, 640), "similar meanings \u2192 nearby vectors",
        font(F_BOLD, 30), DIM, anchor="mm")

def scene_rag(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "RAG: Retrieval-Augmented Generation", BLUE)
    stages = [("QUERY", BLUE), ("EMBED", CYAN), ("SEARCH", YELLOW), ("RETRIEVE", ORANGE), ("GENERATE", GREEN)]
    n = len(stages); bw = 190; gap = 26
    total = n * bw + (n - 1) * gap; x0 = (W - total) // 2
    pk = clamp((t - 4) / 17)
    for i, (name, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        done = pk * n > i + 0.5
        active = (pk * n > i) and not done
        glow_box(dr, [x, 280, x + bw, 440], col if (done or active) else (60, 60, 90), rad=14)
        dr.rectangle([x, 280, x + bw, 440], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 340), name, font(F_BOLD, 28), col if (done or active) else DIM, anchor="mm")
        if done:
            txt(dr, (x + bw // 2, 400), "\u2713", font(F_BOLD, 36), GREEN, anchor="mm")
        if i < n - 1:
            arrow(dr, x + bw + 4, 360, x + bw + gap - 4, 360, DIM, 5)
    if pk > 0.01 and pk < 0.99:
        px = x0 + pk * total
        dr.ellipse([px - 12, 228, px + 12, 252], fill=WHITE)
        dr.ellipse([px - 7, 233, px + 7, 247], fill=CYAN)
    if t > 15:
        panel(dr, [x0, 500, x0 + total, 640], "ANSWER + CITATIONS [1][2][3]", GREEN, 26)
    if t > 22:
        txt(dr, (W // 2, 140), "grounded answers: the model cites what it read",
            font(F_BOLD, 30), GREEN, anchor="mm")

# ============================================================ IL-13: SWE Interview Prep
def scene_dp(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "Dynamic Programming: coin change", font(F_BOLD, 40), WHITE, anchor="mm")
    txt(dr, (W // 2, 110), "coins [1, 5, 10] \u00b7 amount 12 \u00b7 min coins?",
        font(F_MONO, 28), DIM, anchor="mm")
    # dp[a] = min coins
    dp = [0, 1, 2, 3, 4, 1, 2, 3, 4, 5, 1, 2, 3]
    n = 12
    cw = 84; x0 = (W - (n + 1) * cw) // 2
    k = clamp((t - 5) / 14)
    nfill = int(k * (n + 1))
    for a in range(n + 1):
        x = x0 + a * cw
        dr.rectangle([x, 260, x + cw - 8, 360], fill=(14, 14, 30),
                     outline=(80, 80, 120), width=2)
        txt(dr, (x + (cw - 8) // 2, 240), str(a), font(F_MONO, 22), DIM, anchor="mm")
        if a < nfill:
            hot = (a == 12)
            txt(dr, (x + (cw - 8) // 2, 310), str(dp[a]),
                font(F_MONOB, 32), GREEN if hot else WHITE, anchor="mm")
            if a >= 7:
                dr.line([x + (cw - 8) // 2, 360, x + (cw - 8) // 2, 400], fill=MAGENTA, width=2)
    txt(dr, (W // 2, 470), "dp[a] = 1 + min(dp[a\u22121], dp[a\u22125], dp[a\u221210])",
        font(F_MONO, 30), MAGENTA, anchor="mm")
    if t > 21:
        glow_box(dr, [x0 + 12 * cw, 260, x0 + 12 * cw + cw - 8, 360], GREEN, rad=10, layers=2)
        txt(dr, (W // 2, 560), "answer: 3 coins \u2014 10 + 1 + 1 \u00b7 solved bottom-up",
            font(F_BOLD, 32), GREEN, anchor="mm")

def scene_urlshort(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "System Design: URL Shortener", BLUE)
    comps = [("CLIENT", 170, BLUE), ("API", 420, CYAN), ("CACHE", 680, YELLOW),
             ("DB", 940, ORANGE), ("HASH", 420, MAGENTA)]
    for name, x, col in comps[:4]:
        glow_box(dr, [x - 100, 200, x + 100, 330], col, rad=12, layers=2)
        dr.rectangle([x - 100, 200, x + 100, 330], fill=(12, 16, 34))
        txt(dr, (x, 265), name, font(F_BOLD, 28), col, anchor="mm")
    glow_box(dr, [320, 420, 520, 540], MAGENTA, rad=12, layers=2)
    dr.rectangle([320, 420, 520, 540], fill=(12, 16, 34))
    txt(dr, (420, 465), "HASH", font(F_BOLD, 28), MAGENTA, anchor="mm")
    txt(dr, (420, 505), "base62(url)", font(F_MONO, 20), DIM, anchor="mm")
    for i in range(3):
        arrow(dr, comps[i][1] + 100, 265, comps[i + 1][1] - 100, 265, DIM, 5)
    # request packet
    if t > 5:
        k = clamp((t - 5) / 12)
        legs = [(170, 420), (420, 680), (680, 940), (940, 680), (680, 420), (420, 170)]
        seg = min(len(legs) - 1, int(k * len(legs)))
        u = k * len(legs) - seg
        x0l, x1l = legs[seg]
        px = lerp(x0l, x1l, u)
        dr.ellipse([px - 12, 265 - 12, px + 12, 265 + 12], fill=WHITE)
        dr.ellipse([px - 7, 265 - 7, px + 7, 265 + 7], fill=CYAN)
        lbls = ["POST /long-url", "cache?", "miss \u2192 query", "store mapping",
                "cache it", "201: il.dev/a8x2kQ"]
        txt(dr, (W // 2, 600), lbls[seg], font(F_BOLD, 30), CYAN, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 660), "read-heavy: cache the hot 20% \u00b7 1B URLs \u2248 100GB",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_recurrence(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "T(n) = 2T(n/2) + n", font(F_BOLD, 48), WHITE, anchor="mm")
    txt(dr, (W // 2, 125), "the recursion tree of mergesort", font(F_SANS, 28), DIM, anchor="mm")
    cx = W // 2
    levels = [(0, 1, 300, "n"), (1, 2, 160, "n/2 + n/2 = n"),
              (2, 4, 90, "4 \u00d7 n/4 = n"), (3, 8, 55, "8 \u00d7 n/8 = n")]
    k = ease(clamp((t - 5) / 14))
    for i, (lvl, cnt, r, lbl) in enumerate(levels):
        if k * 4 < lvl:
            continue
        y = 230 + lvl * 95
        for j in range(cnt):
            x = cx + (j - (cnt - 1) / 2) * (640 / cnt if cnt > 1 else 0)
            dr.ellipse([x - r / 3, y - r / 3, x + r / 3, y + r / 3],
                       outline=TEAL, width=3)
        txt(dr, (cx + 420, y), lbl, font(F_MONO, 24), YELLOW, anchor="lm")
    if t > 20:
        txt(dr, (W // 2, 620), "log n levels \u00d7 n work each = O(n log n)",
            font(F_BOLD, 36), GREEN, anchor="mm")

# ============================================================ IL-14: SRE / DevOps / Cloud / Security Interviews
def scene_slo(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "SLIs, SLOs & Error Budgets", BLUE)
    txt(dr, (W // 2, 150), "SLO 99.9% \u00b7 budget: 43.2 min downtime / 30 days",
        font(F_BOLD, 30), WHITE, anchor="mm")
    dr.rectangle([140, 260, 1140, 330], fill=(20, 28, 50), outline=DIM, width=2)
    k = clamp((t - 5) / 15)
    used = 43.2 * k * 0.9
    dr.rectangle([140, 260, 140 + 1000 * clamp(used / 43.2), 330], fill=RED)
    txt(dr, (640, 380), "budget consumed: %.1f / 43.2 min" % used,
        font(F_BOLD, 32), RED if used > 30 else WHITE, anchor="mm")
    # burn-rate ticks
    for d in range(30):
        x = 140 + d * 33.3
        hot = d < int(k * 30)
        dr.line([x, 440, x, 470], fill=RED if hot and d % 5 == 0 else (60, 70, 100), width=4)
    txt(dr, (140, 510), "day 1", font(F_SANS, 22), DIM, anchor="lm")
    txt(dr, (1140, 510), "day 30", font(F_SANS, 22), DIM, anchor="lm")
    if t > 20:
        glow_box(dr, [340, 550, 940, 640], YELLOW, rad=12)
        dr.rectangle([340, 550, 940, 640], fill=(30, 26, 8))
        txt(dr, (W // 2, 595), "burn rate > 14.4\u00d7 \u2192 page \u00b7 freeze deploys",
            font(F_BOLD, 30), YELLOW, anchor="mm")

def scene_incident(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Incident Response: the first 30 minutes", BLUE)
    stages = [("DETECT", RED), ("DECLARE", ORANGE), ("MITIGATE", YELLOW), ("RESOLVE", GREEN)]
    n = len(stages); bw = 230; gap = 30
    total = n * bw + (n - 1) * gap; x0 = (W - total) // 2
    k = clamp((t - 4) / 16)
    for i, (name, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        done = k * n > i + 0.5
        active = (k * n > i) and not done
        glow_box(dr, [x, 240, x + bw, 400], col if (done or active) else (60, 60, 90), rad=14)
        dr.rectangle([x, 240, x + bw, 400], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 300), name, font(F_BOLD, 28), col if (done or active) else DIM, anchor="mm")
        mins = ["0:00", "0:05", "0:12", "0:28"][i]
        txt(dr, (x + bw // 2, 350), mins, font(F_MONO, 24), DIM, anchor="mm")
        if i < n - 1:
            arrow(dr, x + bw + 4, 320, x + bw + gap - 4, 320, DIM, 5)
    roles = [("IC", "commands"), ("COMMS", "updates"), ("OPS", "fixes")]
    for i, (r, s) in enumerate(roles):
        on = t >= 6 + i * 2
        txt(dr, (240 + i * 400, 500), r + ": " + s, font(F_BOLD, 28),
            CYAN if on else DIM, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 580), "blameless retro within 48h \u2014 fix the system, not the person",
            font(F_BOLD, 30), GREEN, anchor="mm")

def scene_canary(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "Canary Deployments", font(F_BOLD, 44), WHITE, anchor="mm")
    steps = [(100, 0), (95, 5), (75, 25), (50, 50), (0, 100)]
    k = clamp((t - 5) / 15)
    idx = min(4, int(k * 5))
    v1, v2 = steps[idx]
    # traffic bar
    dr.rectangle([140, 220, 1140, 300], fill=(20, 24, 40), outline=DIM, width=2)
    dr.rectangle([140, 220, 140 + 1000 * v1 / 100, 300], fill=BLUE)
    dr.rectangle([140 + 1000 * v1 / 100, 220, 1140, 300], fill=GREEN)
    txt(dr, (140 + 1000 * v1 / 200, 260), "v1 %d%%" % v1, font(F_BOLD, 28), WHITE, anchor="mm")
    if v2 > 0:
        txt(dr, (140 + 1000 * v1 / 100 + 1000 * v2 / 200, 260), "v2 (canary) %d%%" % v2,
            font(F_BOLD, 28), WHITE, anchor="mm")
    txt(dr, (W // 2, 360), "step %d / 5" % (idx + 1), font(F_BOLD, 30), DIM, anchor="mm")
    # metrics gate
    gates = [("error rate < 1%", True), ("p99 latency OK", True), ("no new 5xx", idx < 4 or True)]
    for i, (g, ok) in enumerate(gates):
        on = t >= 8 + i * 2.5
        txt(dr, (W // 2, 430 + i * 50), ("\u2713 " if on else "\u25cb ") + g,
            font(F_SANS, 28), GREEN if on else DIM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 620), "gates green \u2192 promote \u00b7 gates red \u2192 automatic rollback",
            font(F_BOLD, 30), GREEN, anchor="mm")

# ============================================================ VIDEO CONFIG
VIDEOS = [
 # --- IL-08: Algorithms, Compilers, Distributed & Formal
 dict(file="3b1b-dijkstra.mp4", style="3b1b", scene=scene_dijkstra,
      kicker="IL-08 \u00b7 Algorithms, Compilers, Distributed & Formal", title="Dijkstra\u2019s Algorithm",
      sub="Shortest paths, greedily", module=3,
      blurb="A graph settles node by node: the closest unsettled node is always finalized, and the shortest-path tree grows in green.",
      captions=[(4,10,"Start at A \u2014 distance 0, everything else infinity"),
                (10,16,"Repeatedly settle the closest unsettled node"),
                (16,22,"Relax its edges: shorter paths replace longer ones"),
                (22,26,"Greedy works here \u2014 edge weights are never negative")]),
 dict(file="fireship-compiler-pipeline.mp4", style="fireship", scene=scene_compiler,
      kicker="IL-08 \u00b7 Algorithms, Compilers, Distributed & Formal", title="How a Compiler Works",
      sub="From text to machine code", module=3,
      blurb="main.c streams through lexing, parsing, IR, and codegen: tokens, a syntax tree, then two machine instructions.",
      captions=[(4,10,"Lexing: characters become tokens \u2014 int, main, (, ) \u2026"),
                (10,16,"Parsing: tokens become a syntax tree"),
                (16,22,"IR: one intermediate language for every target"),
                (22,26,"Codegen: mov eax, 42 \u2014 the machine runs numbers")]),
 dict(file="bbg-paxos.mp4", style="bbg", scene=scene_paxos,
      kicker="IL-08 \u00b7 Algorithms, Compilers, Distributed & Formal", title="Paxos Consensus",
      sub="Agreeing when machines fail", module=2,
      blurb="A proposer runs two phases against three acceptors: prepare/promise, then accept/accepted \u2014 quorum commits the value.",
      captions=[(4,10,"Phase 1: the proposer sends PREPARE(n)"),
                (10,16,"Acceptors reply PROMISE \u2014 no lower numbers accepted"),
                (16,22,"Phase 2: ACCEPT(n, v) goes out"),
                (22,26,"A majority accepts \u2014 the value is committed")]),
 # --- IL-09: Adaptive Certification Command
 dict(file="bbg-comptia-ladder.mp4", style="bbg", scene=scene_comptia,
      kicker="IL-09 \u00b7 Adaptive Certification Command", title="The CompTIA Ladder",
      sub="Stacking credentials strategically", module=2,
      blurb="The certification pyramid lights bottom-up: A+ foundation, Network+/Security+ core, CySA+/PenTest+ advanced, SecurityX expert.",
      captions=[(4,10,"A+: the foundation \u2014 hardware, OS, troubleshooting"),
                (10,16,"Network+ and Security+: the core stack"),
                (16,22,"CySA+ and PenTest+: the advanced tier"),
                (22,26,"SecurityX: the expert capstone")]),
 dict(file="primer-password-entropy.mp4", style="primer", scene=scene_entropy,
      kicker="IL-09 \u00b7 Adaptive Certification Command", title="Password Entropy",
      sub="Why length beats complexity", module=3,
      blurb="A live simulation: as the password grows from 4 to 12 characters, entropy climbs and offline crack time goes from seconds to centuries.",
      captions=[(4,10,"Each character adds ~6.2 bits of entropy"),
                (10,16,"Crack time doubles with every single bit"),
                (16,22,"12 characters: offline cracking takes centuries"),
                (22,26,"Length wins \u2014 and a manager remembers it for you")]),
 dict(file="fireship-oauth2.mp4", style="fireship", scene=scene_oauth,
      kicker="IL-09 \u00b7 Adaptive Certification Command", title="OAuth 2.0 in 100 Seconds",
      sub="The authorization code flow", module=2,
      blurb="A sequence diagram of the authorization code flow: the client gets scoped tokens and never touches your password.",
      captions=[(4,10,"The user asks the client to act on their behalf"),
                (10,16,"The auth server issues a one-time code"),
                (16,22,"The client trades the code for tokens"),
                (22,26,"Tokens are scoped and revocable \u2014 passwords never shared")]),
 # --- IL-10: Portfolio, Career & Professional Practice
 dict(file="story-career-arc.mp4", style="story", scene=scene_career_arc,
      kicker="IL-10 \u00b7 Portfolio, Career & Professional Practice", title="The Career Arc",
      sub="Apprentice \u2192 Builder \u2192 Founder", module=1,
      blurb="A candle-lit journey along the career path: apprentice learns the craft, builder ships systems, founder owns the outcome.",
      captions=[(4,10,"Every career begins as an apprenticeship"),
                (10,16,"The builder phase: ship real systems, earn trust"),
                (16,22,"The founder phase: own the outcome, not just the task"),
                (22,26,"Careers compound \u2014 skills reinvested yearly")]),
 dict(file="bbg-offer-negotiation.mp4", style="bbg", scene=scene_offer,
      kicker="IL-10 \u00b7 Portfolio, Career & Professional Practice", title="Negotiating the Offer",
      sub="Anchor on data, not history", module=1,
      blurb="Offer anatomy on a number line: their first offer, the market band, and your researched target \u2014 plus four field-tested tactics.",
      captions=[(4,10,"Their first offer is an anchor, not a verdict"),
                (10,16,"The market band is your leverage: $85\u2013$110k"),
                (16,22,"Counter with data \u2014 never with salary history"),
                (22,26,"Negotiate the whole package, then pause")]),
 dict(file="primer-compound-interest.mp4", style="primer", scene=scene_compound,
      kicker="IL-10 \u00b7 Portfolio, Career & Professional Practice", title="Compound Interest",
      sub="Time does the work", module=4,
      blurb="A living simulation: $10k a year at 8% for 30 years \u2014 contributions stay linear while growth goes exponential.",
      captions=[(4,10,"$10,000 a year, 8% return, 30 years"),
                (10,16,"Contributions grow linearly \u2014 $300k total"),
                (16,22,"Growth goes exponential: interest earning interest"),
                (22,26,"$1.22M out \u2014 time did most of the work")]),
 # --- IL-11: Zero Trust & Endpoint Defense
 dict(file="bbg-zero-trust-tenets.mp4", style="bbg", scene=scene_ztt,
      kicker="IL-11 \u00b7 Zero Trust & Endpoint Defense", title="Zero Trust Tenets",
      sub="Never trust, always verify", module=3,
      blurb="Every request passes the policy engine \u2014 identity, device health, location, risk \u2014 before touching any resource. One fails, access dies.",
      captions=[(4,10,"Zero trust: no implicit trust, anywhere"),
                (10,16,"Every request is verified: identity, device, context"),
                (16,22,"Verified request \u2192 allow. Failed check \u2192 deny."),
                (22,26,"The perimeter is dead \u2014 verify everything")]),
 dict(file="bbg-allowlisting.mp4", style="bbg", scene=scene_allowlist,
      kicker="IL-11 \u00b7 Zero Trust & Endpoint Defense", title="Application Allowlisting",
      sub="Default-deny execution", module=12,
      blurb="Three apps request execution; the allowlist database checks SHA-256 hashes \u2014 signed apps run, the unsigned one is blocked cold.",
      captions=[(4,10,"Every executable must prove itself before running"),
                (10,16,"The allowlist checks SHA-256 hashes of approved apps"),
                (16,22,"Signed apps run \u2014 the unsigned one is blocked"),
                (22,26,"Default-deny: unlisted means unrun")]),
 dict(file="fireship-conditional-access.mp4", style="fireship", scene=scene_condaccess,
      kicker="IL-11 \u00b7 Zero Trust & Endpoint Defense", title="Conditional Access",
      sub="Policy as code", module=21,
      blurb="Signals stream into a policy decision tree \u2014 medium risk means grant plus step-up MFA, not a flat deny.",
      captions=[(4,10,"Signals: location, device, risk, app"),
                (10,16,"Policy evaluates every signal in real time"),
                (16,22,"Medium risk \u2192 grant, but require MFA"),
                (22,26,"Access decisions are computed, not assumed")]),
 # --- IL-12: AI Engineering
 dict(file="3b1b-attention.mp4", style="3b1b", scene=scene_attention,
      kicker="IL-12 \u00b7 AI Engineering", title="The Attention Mechanism",
      sub="Queries pick their context", module=25,
      blurb="The query token 'sat' distributes softmax weights across every key: cat and mat win, and the output is their weighted mix.",
      captions=[(4,10,"Each token asks: who is relevant to me?"),
                (10,16,"Query meets keys \u2014 scores become softmax weights"),
                (16,22,"\u2018sat\u2019 attends to \u2018cat\u2019 and \u2018mat\u2019"),
                (22,26,"Output = weighted mix of values. That is attention.")]),
 dict(file="3b1b-embeddings.mp4", style="3b1b", scene=scene_embeddings,
      kicker="IL-12 \u00b7 AI Engineering", title="Word Embeddings",
      sub="Meaning as geometry", module=38,
      blurb="Words land as points in vector space: royalty clusters, objects cluster, and king minus man plus woman lands on queen.",
      captions=[(4,10,"Words become vectors \u2014 points in space"),
                (10,16,"Similar meanings land near each other"),
                (16,22,"Directions encode relationships: gender, royalty"),
                (22,26,"king \u2212 man + woman \u2248 queen")]),
 dict(file="bbg-rag-pipeline.mp4", style="bbg", scene=scene_rag,
      kicker="IL-12 \u00b7 AI Engineering", title="RAG: Retrieval-Augmented Generation",
      sub="Grounded answers", module=30,
      blurb="A query is embedded, vector-searched, and its retrieved chunks feed the LLM \u2014 the answer ships with citations.",
      captions=[(4,10,"The query becomes a vector"),
                (10,16,"Vector search finds the most relevant chunks"),
                (16,22,"Retrieved context feeds the generator"),
                (22,26,"Grounded answers \u2014 with citations, not hallucinations")]),
 # --- IL-13: Software Engineering Interview Prep
 dict(file="fireship-dp-coin-change.mp4", style="fireship", scene=scene_dp,
      kicker="IL-13 \u00b7 Software Engineering Interview Prep", title="DP: Coin Change",
      sub="Tabulation, bottom-up", module=5,
      blurb="The dp table fills left to right for coins [1,5,10] and amount 12: dp[a] = 1 + min of its predecessors \u2014 answer 3.",
      captions=[(4,10,"dp[a]: the fewest coins for amount a"),
                (10,16,"Fill the table left to right, bottom-up"),
                (16,22,"dp[a] = 1 + min(dp[a\u22121], dp[a\u22125], dp[a\u221210])"),
                (22,26,"Answer: 3 coins \u2014 10 + 1 + 1")]),
 dict(file="bbg-url-shortener.mp4", style="bbg", scene=scene_urlshort,
      kicker="IL-13 \u00b7 Software Engineering Interview Prep", title="System Design: URL Shortener",
      sub="The interview classic", module=6,
      blurb="A request flows client \u2192 API \u2192 cache \u2192 DB: base62 hashing mints short codes, the hot 20% lives in cache.",
      captions=[(4,10,"POST a long URL \u2014 get back a short code"),
                (10,16,"Base62 hash: the code space is enormous"),
                (16,22,"Cache the hot 20% \u2014 reads dominate writes"),
                (22,26,"Scale: 1B URLs fits in ~100GB")]),
 dict(file="3b1b-recurrence-tree.mp4", style="3b1b", scene=scene_recurrence,
      kicker="IL-13 \u00b7 Software Engineering Interview Prep", title="The Recurrence Tree",
      sub="Why mergesort is n log n", module=2,
      blurb="T(n) = 2T(n/2) + n unfolds into a tree: every level does exactly n work, and there are log n levels.",
      captions=[(4,10,"T(n) = 2T(n/2) + n \u2014 divide, conquer, combine"),
                (10,16,"Each level splits: 1, 2, 4, 8 subproblems"),
                (16,22,"But every level does exactly n total work"),
                (22,26,"log n levels \u00d7 n work = O(n log n)")]),
 # --- IL-14: SRE, DevOps, Cloud & Security Interview Prep
 dict(file="bbg-slo-error-budget.mp4", style="bbg", scene=scene_slo,
      kicker="IL-14 \u00b7 SRE, DevOps, Cloud & Security Interview Prep", title="SLIs, SLOs & Error Budgets",
      sub="Reliability as a budget", module=2,
      blurb="A 99.9% SLO means 43.2 minutes of downtime per month: the budget bar drains, burn-rate alerts fire at 14.4x, deploys freeze.",
      captions=[(4,10,"SLO 99.9% \u2014 the promise to users"),
                (10,16,"Error budget: 43.2 minutes of downtime a month"),
                (16,22,"Burn too fast and alerts fire \u2014 deploys freeze"),
                (22,26,"Budgets turn reliability into a number you manage")]),
 dict(file="bbg-incident-response.mp4", style="bbg", scene=scene_incident,
      kicker="IL-14 \u00b7 SRE, DevOps, Cloud & Security Interview Prep", title="Incident Response",
      sub="The first 30 minutes", module=3,
      blurb="Detect, declare, mitigate, resolve: the incident timeline with IC, comms, and ops roles \u2014 then a blameless retro.",
      captions=[(4,10,"Detect: the alert fires at 0:00"),
                (10,16,"Declare: one commander, clear roles"),
                (16,22,"Mitigate first \u2014 root cause later"),
                (22,26,"Blameless retro: fix the system, not the person")]),
 dict(file="fireship-canary-deploy.mp4", style="fireship", scene=scene_canary,
      kicker="IL-14 \u00b7 SRE, DevOps, Cloud & Security Interview Prep", title="Canary Deployments",
      sub="Ship without the blast radius", module=8,
      blurb="Traffic shifts 100/0 \u2192 95/5 \u2192 75/25 \u2192 50/50 \u2192 0/100 while metric gates watch: green promotes, red rolls back automatically.",
      captions=[(4,10,"Route 5% of traffic to the canary"),
                (10,16,"Gates watch: errors, latency, 5xx rate"),
                (16,22,"Green gates \u2192 shift more traffic"),
                (22,26,"Red gates \u2192 automatic rollback")]),
]

COURSE_FILES = {
    8: "il-08-algorithms-compilers-distributed-formal.json",
    9: "il-09-adaptive-certification-command.json",
    10: "il-10-portfolio-career-professional-practice.json",
    11: "il-11-zero-trust-endpoint-defense.json",
    12: "il-12-ai-engineering.json",
    13: "il-13-software-engineering-interview-prep.json",
    14: "il-14-sre-devops-cloud-security-interview-prep.json",
}

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
