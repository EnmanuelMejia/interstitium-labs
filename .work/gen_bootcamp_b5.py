#!/usr/bin/env python3
"""Bootcamp video Phase 2, Batch B5: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b4.py (do not modify the B4 file).

Filenames are bc- prefixed so they never collide with course videos.

Batch B5 bootcamps (programming/languages/dev cluster):
  python, python-web, java, cpp, c-lang, dsa,
  fullstack, react-frontend, spring, dotnet, docker, terraform
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

# ============================================================ python (fireship x1 + bbg x1 + primer x1)
def scene_py_walrus(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE WALRUS IN 100 SECONDS", MAGENTA)
    lns = [("if n := len(data):", YELLOW),
           ("    process(n)", (200, 200, 255)),
           ("# assign AND test in one breath", DIM),
           ("if (m := re.match(p, s)):", YELLOW),
           ("    return m.group(1)", (200, 200, 255)),
           ("# := is the walrus \u2014 tusked assignment", GREEN)]
    hi = int(clamp((t - 5) / 12) * len(lns))
    code_panel(dr, 190, 150, W - 190, 580, "walrus.py", lns, hi_line=hi, t=t)
    if t > 18:
        txt(dr, (W // 2, 620), "two lines become one \u2014 assign, test, and use in a single breath",
            font(F_SANS, 26), CREAM, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 660), "walrus: assignment you can see swimming through the condition",
            font(F_SANS, 24), DIM, anchor="mm")

def scene_py_gil(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE GIL: ONE LOCK FOR 16 CORES", CYAN)
    if t > 4:
        txt(dr, (W // 2, 170), "16 threads, 16 cores \u2014 but only one holds the lock",
            font(F_SANS, 26), DIM, anchor="mm")
        for i in range(16):
            x = 220 + (i % 8) * 108
            y = 260 + (i // 8) * 110
            active = int((t - 4) * 2) % 16 == i
            col = GREEN if active else (30, 40, 70)
            dr.rectangle([x, y, x + 88, y + 70], fill=col, outline=DIM, width=2)
            txt(dr, (x + 44, y + 35), "T%d" % (i + 1), font(F_MONO, 20),
                CREAM if active else DIM, anchor="mm")
        if t > 10:
            dr.rectangle([150, 480, 1130, 560], fill=(12, 18, 32), outline=YELLOW, width=2)
            txt(dr, (W // 2, 520), "GIL \u2014 the Global Interpreter Lock: one thread runs Python at a time",
                font(F_BOLD, 25), YELLOW, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 600), "threads for I/O, processes for CPU \u2014 multiprocessing escapes the lock",
            font(F_SANS, 25), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 650), "threads share memory \u2014 processes share nothing: pick the right tool",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_py_pip(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "PIP HELL: THE RESOLVER'S GAMBLE", font(F_BOLD, 38), CYAN, anchor="mm")
    txt(dr, (W // 2, 118), "thirty packages, one install \u2014 watch the resolver think",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        k = int(clamp((t - 4) / 14) * 30)
        for i in range(k):
            x = 200 + (i % 10) * 96
            y = 200 + (i // 10) * 110
            conflict = i in (7, 18, 23)
            col = RED if (conflict and t > 14) else TEAL
            dr.ellipse([x - 30, y - 30, x + 30, y + 30], fill=col)
            txt(dr, (x, y), "v%d" % (i % 5 + 1), font(F_MONO, 18), WHITE, anchor="mm")
    if t > 14:
        txt(dr, (W // 2, 560), "requests wants urllib3>=2 \u2014 botocore wants urllib3<1.27: CONFLICT",
            font(F_BOLD, 24), RED, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 610), "resolver backtracks, pins urllib3==1.26.18 \u2014 everything installs",
            font(F_SANS, 25), GREEN, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 656), "pip freeze > requirements.txt \u2014 pin it or lose it",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ python-web (fireship x1 + bbg x1 + story x1)
def scene_pyw_cycle(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "A REQUEST'S LIFE IN 100 SECONDS", MAGENTA)
    steps = ["URLconf", "view", "ORM", "template", "response"]
    n = int(clamp((t - 5) / 14) * len(steps))
    for i, s in enumerate(steps):
        x = 130 + i * 205
        y = 300
        lit = i < n
        glow_box(dr, [x, y, x + 170, y + 110], MAGENTA if lit else (40, 40, 60))
        dr.rectangle([x, y, x + 170, y + 110], fill=(16, 16, 30), outline=MAGENTA if lit else DIM, width=3)
        txt(dr, (x + 85, y + 55), s, font(F_BOLD, 22), MAGENTA if lit else DIM, anchor="mm")
        if i < n - 1:
            arrow(dr, x + 170, y + 55, x + 205, y + 55, GREEN if lit else DIM)
    if t > 20:
        txt(dr, (W // 2, 500), "route, compute, query, render \u2014 every request runs the same gauntlet",
            font(F_SANS, 26), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), "slow view? the ORM query is usually the suspect",
            font(F_SANS, 25), YELLOW, anchor="mm")

def scene_pyw_mw(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE MIDDLEWARE ONION", CYAN)
    layers = ["auth", "cors", "session", "csrf", "gzip"]
    n = int(clamp((t - 5) / 12) * len(layers))
    for i, L in enumerate(layers):
        x0 = 190 + i * 30
        x1 = W - 190 - i * 30
        y0, y1 = 210, 470
        lit = i < n
        dr.rectangle([x0, y0, x1, y1], outline=CYAN if lit else DIM, width=3 if lit else 2)
        txt(dr, ((x0 + x1) // 2, y1 + 34), L, font(F_MONO, 24), CYAN if lit else DIM, anchor="mt")
    if t > 18:
        txt(dr, (W // 2, 540), "request dives in through every layer \u2014 response climbs back out",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 600), "order matters: auth before the view, gzip after",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_pyw_deploy(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "FROM LOCALHOST TO PROD", font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), "the first real deploy \u2014 a developer's rite of passage",
        font(F_SERIF, 24), DIM, anchor="mm")
    if t > 4:
        stages = [("tests", 4), ("push", 8), ("CI green", 12), ("migrate", 16), ("LIVE", 21)]
        for i, (s, ts) in enumerate(stages):
            y = 200 + i * 80
            done = t > ts
            if done:
                bar(dr, 340, y, 600, 44, clamp((t - ts + 3) / 3), GOLD if s == "LIVE" else CYAN)
            col = GREEN if done else DIM
            txt(dr, (240, y + 22), s, font(F_BOLD, 26), col, anchor="lm")
            if s == "LIVE" and done:
                txt(dr, (W // 2, 620), "the site is live \u2014 someone on another continent just hit refresh",
                    font(F_SERIF, 26), GOLD, anchor="mm")

# ============================================================ java (fireship x1 + bbg x1 + 3b1b x1)
def scene_jv_stream(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "STREAMS IN 100 SECONDS", MAGENTA)
    lns = [("orders.stream()", (200, 200, 255)),
           ("  .filter(o -> o.total() > 100)", YELLOW),
           ("  .map(Order::customer)", (200, 200, 255)),
           ("  .distinct()", YELLOW),
           ("  .collect(toList());", (200, 200, 255)),
           ("# pipeline: lazy until the terminal op", GREEN)]
    hi = int(clamp((t - 5) / 12) * len(lns))
    code_panel(dr, 190, 150, W - 190, 560, "streams.java", lns, hi_line=hi, t=t)
    if t > 18:
        txt(dr, (W // 2, 610), "twelve lines of loops become one pipeline",
            font(F_SANS, 26), CREAM, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 652), "nothing runs until .collect \u2014 streams are lazy",
            font(F_SANS, 24), YELLOW, anchor="mm")

def scene_jv_gc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE GARBAGE COLLECTOR'S SWEEP", CYAN)
    gens = [("eden", 0.5, GREEN), ("survivor", 0.2, YELLOW), ("old gen", 0.9, RED)]
    if t > 4:
        txt(dr, (W // 2, 170), "objects are born in eden \u2014 survivors age, the old never die",
            font(F_SANS, 26), DIM, anchor="mm")
        for i, (name, fill0, col) in enumerate(gens):
            x = 200 + i * 320
            fill = clamp(fill0 + (t - 4) / 25) if i == 0 else fill0
            bar(dr, x, 300, 240, 200, fill if t < 15 else 0.05, col, label=name)
        if t > 15:
            txt(dr, (W // 2, 560), "minor GC: eden swept clean \u2014 the app pauses 20ms, nobody notices",
                font(F_BOLD, 25), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 616), "memory you forgot is memory you never owned \u2014 the GC just invoices you",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_jv_hash(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "HASHMAP: O(1) WITH AN ASTERISK", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "sixteen buckets \u2014 watch collisions stack up",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        k = int(clamp((t - 4) / 10) * 16)
        for i in range(16):
            x = 170 + (i % 8) * 125
            y = 210 + (i // 8) * 130
            filled = i < k
            chained = filled and i % 5 == 0
            dr.rectangle([x, y, x + 100, y + 90], fill=(12, 18, 32),
                         outline=TEAL if filled else DIM, width=3 if filled else 2)
            if filled:
                txt(dr, (x + 50, y + 30), "K", font(F_MONO, 22), TEAL, anchor="mm")
            if chained and t > 10:
                txt(dr, (x + 50, y + 65), "+2 chain", font(F_MONO, 16), ORANGE, anchor="mm")
    if t > 15:
        txt(dr, (W // 2, 510), "chains grow: lookup slides from O(1) toward O(n)",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 566), "resize at load factor 0.75 \u2014 rehash and the speed returns",
            font(F_SANS, 25), GREEN, anchor="mm")

# ============================================================ cpp (bbg x1 + fireship x1 + 3b1b x1)
def scene_cpp_move(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "MOVE: STEAL, DON'T COPY", CYAN)
    if t > 4:
        k = clamp((t - 4) / 8)
        dr.rectangle([240, 240, 520, 460], fill=(12, 18, 32), outline=DIM, width=2)
        txt(dr, (380, 220), "lvalue: 'name'", font(F_MONO, 24), DIM, anchor="mm")
        txt(dr, (380, 350), "std::string\n  name = \"huge\"", font(F_MONO, 24), CREAM, anchor="mm")
        x0 = int(lerp(380, 900, k))
        dr.rectangle([x0 - 140, 240, x0 + 140, 460], fill=(12, 18, 32), outline=GREEN, width=3)
        txt(dr, (900, 220), "std::move(name)", font(F_MONO, 24), GREEN, anchor="mm")
        txt(dr, (900, 350), "pointer\n  TRANSFERRED", font(F_MONO, 24), GREEN, anchor="mm")
        arrow(dr, 520, 350, 700, 350, YELLOW)
    if t > 14:
        bar(dr, 240, 520, 400, 36, 1.0, RED, label="copy: O(n) bytes moved")
        bar(dr, 240, 590, 400, 36, 0.06, GREEN, label="move: O(1) pointer swap")
    if t > 21:
        txt(dr, (W // 2, 662), "move semantics: steal the guts, leave the husk",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_cpp_template(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "TEMPLATES IN 100 SECONDS", MAGENTA)
    lns = [("template <typename T>", YELLOW),
           ("T max(T a, T b) {", (200, 200, 255)),
           ("  return a > b ? a : b;", (200, 200, 255)),
           ("}", (200, 200, 255)),
           ("max(3, 7);          // int", GREEN),
           ("max(2.5, 1.1);      // double", GREEN),
           ("max(\"a\", \"z\");       // string", GREEN),
           ("# one function \u2014 stamped out per type", DIM)]
    hi = int(clamp((t - 5) / 13) * len(lns))
    code_panel(dr, 190, 150, W - 190, 580, "templates.cpp", lns, hi_line=hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), "compile-time code generation \u2014 zero runtime cost",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_cpp_cache(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE CACHE MISS THAT COST 100x", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "row-major vs column-major on a 64x64 grid",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        k = clamp((t - 4) / 8)
        for j in range(2):
            x0 = 180 + j * 470
            lbl = "row-major" if j == 0 else "column-major"
            col = GREEN if j == 0 else RED
            txt(dr, (x0 + 130, 190), lbl, font(F_BOLD, 22), col, anchor="mm")
            for i in range(8):
                for jj in range(8):
                    if j == 0:
                        on = (i * 8 + jj) < k * 64
                    else:
                        on = (jj * 8 + i) < k * 64
                    c = (x0 + jj * 32, 230 + i * 32)
                    dr.rectangle([c[0], c[1], c[0] + 28, c[1] + 28],
                                 fill=col if on else (20, 28, 48))
        bar(dr, 180, 540, 440, 30, 0.15, GREEN, label="row-major", val="0.02s")
        bar(dr, 700, 540, 440, 30, 0.85, RED, label="column-major", val="0.31s")
    if t > 17:
        txt(dr, (W // 2, 630), "cache lines are 64 bytes \u2014 traverse memory the way it lies",
            font(F_SANS, 25), YELLOW, anchor="mm")

# ============================================================ c-lang (fireship x1 + bbg x1 + primer x1)
def scene_cc_ptr(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "POINTERS IN 100 SECONDS", MAGENTA)
    if t > 4:
        k = int(clamp((t - 4) / 10) * 8)
        for i in range(8):
            x = 220 + i * 105
            dr.rectangle([x, 260, x + 90, y if (y := 360) else 360], fill=(12, 18, 32), outline=DIM, width=2)
            txt(dr, (x + 45, 240), "0x%02X" % (0xA0 + i), font(F_MONO, 18), DIM, anchor="mm")
            if i < k:
                txt(dr, (x + 45, 310), str(i * 10 + 5), font(F_MONO, 24), TEAL, anchor="mm")
        if k > 0:
            px = 220 + (k - 1) * 105 + 45
            arrow(dr, px, 440, px, 375, YELLOW, w=8)
            dr.rectangle([px - 60, 440, px + 60, 490], fill=(30, 30, 10), outline=YELLOW, width=3)
            txt(dr, (px, 465), "*p", font(F_MONOB, 26), YELLOW, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 560), "a pointer is just an address \u2014 *p reads the value AT that address",
            font(F_SANS, 25), CREAM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 612), "p++ moves by sizeof(int), not by one \u2014 the type is the stride",
            font(F_SANS, 25), YELLOW, anchor="mm")

def scene_cc_mem(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "STACK vs HEAP: THE GREAT DIVIDE", CYAN)
    if t > 4:
        k = clamp((t - 4) / 8)
        x0, x1 = 420, 860
        dr.rectangle([x0, 220, x1, 520], outline=DIM, width=2)
        sh = int(lerp(20, 130, k))
        dr.rectangle([x0, 220, x1, 220 + sh], fill=TEAL)
        txt(dr, ((x0 + x1) // 2, 220 + sh // 2), "STACK", font(F_BOLD, 22), (10, 20, 20), anchor="mm")
        hh = int(lerp(20, 110, k))
        dr.rectangle([x0, 520 - hh, x1, 520], fill=ORANGE)
        txt(dr, ((x0 + x1) // 2, 520 - hh // 2), "HEAP", font(F_BOLD, 22), (10, 20, 20), anchor="mm")
        arrow(dr, x0 - 40, 260, x0 - 40, 300, TEAL, w=5)
        arrow(dr, x1 + 40, 480, x1 + 40, 440, ORANGE, w=5)
        txt(dr, (x0 - 90, 330), "grows\ndown", font(F_SANS, 20), DIM, anchor="mm")
        txt(dr, (x1 + 90, 410), "grows\nup", font(F_SANS, 20), DIM, anchor="mm")
    if t > 14:
        txt(dr, (W // 2, 580), "stack: automatic, fast, freed on return \u2014 heap: malloc'd, yours to free",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 636), "every malloc needs a free \u2014 leak the heap and the OOM killer comes",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_cc_seg(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE SEGFAULT SIMULATOR", font(F_BOLD, 38), CYAN, anchor="mm")
    txt(dr, (W // 2, 118), "array of eight \u2014 the cursor walks off the end",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        n = int(clamp((t - 4) / 14) * 12)
        for i in range(12):
            x = 160 + i * 82
            valid = i < 8
            here = i < n
            col = TEAL if (valid and here) else ((30, 40, 70) if not here else RED)
            dr.rectangle([x, 300, x + 70, y if (y := 380) else 380], fill=col,
                         outline=RED if (here and not valid) else DIM, width=4 if (here and not valid) else 2)
            txt(dr, (x + 35, 340), "A[%d]" % i, font(F_MONO, 16), WHITE if here else DIM, anchor="mm")
        if n >= 9:
            dr.rectangle([0, 0, W, H], outline=RED, width=10)
            txt(dr, (W // 2, 480), "Segmentation fault (core dumped)",
                font(F_MONOB, 34), RED, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 560), "bounds are YOUR job in C \u2014 the OS punishes the careless",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ dsa (3b1b x1 + fireship x1 + bbg x1)
def scene_ds_master(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE MASTER THEOREM", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "T(n) = a \u00b7 T(n/b) + f(n) \u2014 three cases decide the fate",
        font(F_MONO, 24), DIM, anchor="mm")
    if t > 4:
        depth = int(clamp((t - 4) / 9) * 3) + 1
        for lvl in range(depth):
            n = 2 ** lvl
            y = 220 + lvl * 90
            tot = 0
            for i in range(n):
                x = W // 2 + (i - (n - 1) / 2) * (min(700 / n, 120))
                r = 26 if lvl < 2 else 18
                dr.ellipse([x - r, y - r, x + r, y + r], fill=TEAL)
                tot += 1
            txt(dr, (120, y), "a=%d" % tot, font(F_MONO, 20), DIM, anchor="lm")
        if t > 15:
            txt(dr, (W // 2, 520), "Case 1: leaves dominate \u2014 mergesort lives here: O(n log n)",
                font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 580), "divide, conquer, combine \u2014 the theorem reads the tree's total",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_ds_bfs(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "BFS vs DFS IN 100 SECONDS", MAGENTA)
    nodes = [(0, 500, 260), (1, 700, 260), (2, 900, 260), (3, 600, 420), (4, 800, 420)]
    edges = [(0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4)]
    bfs_order = [0, 1, 3, 2, 4]
    n = int(clamp((t - 5) / 12) * len(nodes))
    for a, b in edges:
        ax, ay = nodes[a][1], nodes[a][2]
        bx, by = nodes[b][1], nodes[b][2]
        dr.line([ax, ay, bx, by], fill=DIM, width=3)
    for i, (idx, x, y) in enumerate(nodes):
        seen = bfs_order.index(idx) < n
        dr.ellipse([x - 34, y - 34, x + 34, y + 34], fill=MAGENTA if seen else (16, 16, 30),
                   outline=MAGENTA, width=3)
        txt(dr, (x, y), str(idx), font(F_BOLD, 24), WHITE if seen else DIM, anchor="mm")
    if t > 8:
        q = " \u2192 ".join(str(bfs_order[i]) for i in range(n))
        txt(dr, (W // 2, 520), "queue: " + q, font(F_MONO, 26), YELLOW, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 580), "BFS: level by level, shortest path \u2014 DFS: dig deep, backtrack",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_ds_lru(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE LRU CACHE: FORGET THE COLD", CYAN)
    ops = [("get(1)", 4, 10), ("get(3)", 8, 13), ("put(5)", 12, 17), ("get(2)", 17, 21)]
    if t > 4:
        items = [("1", True), ("2", True), ("3", True), ("4", False)]
        n = int(clamp((t - 4) / 9) * 4)
        for i in range(4):
            x = 260 + i * 180
            here = i < n
            dr.rectangle([x, 280, x + 150, y if (y := 420) else 420],
                         fill=(12, 18, 32), outline=CYAN if here else DIM, width=3 if here else 2)
            txt(dr, (x + 75, 330), "key " + items[i][0], font(F_MONO, 24), CREAM if here else DIM, anchor="mm")
            if i == 3 and t > 14:
                txt(dr, (x + 75, 390), "EVICTED", font(F_BOLD, 22), RED, anchor="mm")
        if t > 14:
            txt(dr, (W // 2, 500), "capacity 3 \u2014 key 4 hasn't been touched: it goes",
                font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 566), "hash map for O(1) lookup + doubly-linked list for order",
            font(F_SANS, 25), GREEN, anchor="mm")

# ============================================================ fullstack (story x1 + bbg x1 + fireship x1)
def scene_fs_localhost(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "GOODBYE, LOCALHOST", font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), "three months of building \u2014 the day it goes public",
        font(F_SERIF, 24), DIM, anchor="mm")
    if t > 4:
        k = clamp((t - 4) / 14)
        dr.rectangle([240, 240, 1040, 280], fill=(20, 20, 30), outline=DIM, width=2)
        dr.rectangle([240, 240, 240 + int(800 * k), 280], fill=GOLD)
        labels = ["dev", "DB wired", "auth done", "deploy", "DNS"]
        for i, L in enumerate(labels):
            x = 260 + i * 190
            on = k * 5 > i
            txt(dr, (x, 330), L, font(F_SANS, 24), GOLD if on else DIM, anchor="mm")
        if k > 0.95:
            txt(dr, (W // 2, 430), "https://yourapp.com \u2014 it's real, it's yours",
                font(F_MONOB, 30), GOLD, anchor="mm")
            txt(dr, (W // 2, 500), "first visitor from another timezone \u2014 then a hundred more",
                font(F_SERIF, 25), CREAM, anchor="mm")

def scene_fs_auth(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE JWT HANDSHAKE", CYAN)
    if t > 4:
        k = clamp((t - 4) / 6)
        x = int(lerp(200, 640, k))
        txt(dr, (x, 240), "POST /login", font(F_MONOB, 24), YELLOW, anchor="mm")
        arrow(dr, x + 90, 240, x + 190, 240, DIM)
        if t > 11:
            dr.rectangle([740, 300, 1120, 400], fill=(12, 18, 32), outline=GREEN, width=3)
            txt(dr, (930, 335), "eyJhbGciOi...", font(F_MONO, 20), GREEN, anchor="mm")
            txt(dr, (930, 372), "signed token \u2014 24h", font(F_SANS, 20), DIM, anchor="mm")
        if t > 16:
            txt(dr, (W // 2, 480), "every request carries the token \u2014 the server verifies, never stores",
                font(F_SANS, 25), YELLOW, anchor="mm")
        if t > 20:
            dr.rectangle([300, 540, 600, 600], fill=(20, 40, 20), outline=GREEN, width=2)
            txt(dr, (450, 570), "200 OK", font(F_BOLD, 24), GREEN, anchor="mm")
            dr.rectangle([680, 540, 980, 600], fill=(40, 20, 20), outline=RED, width=2)
            txt(dr, (830, 570), "401 expired", font(F_BOLD, 24), RED, anchor="mm")

def scene_fs_cors(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "CORS IN 100 SECONDS", MAGENTA)
    if t > 4:
        dr.rectangle([150, 220, 520, 400], fill=(16, 16, 30), outline=MAGENTA, width=3)
        txt(dr, (335, 260), "app.com", font(F_BOLD, 26), MAGENTA, anchor="mm")
        txt(dr, (335, 330), "fetch(api.io)", font(F_MONO, 22), CREAM, anchor="mm")
        dr.rectangle([760, 220, 1130, 400], fill=(16, 16, 30), outline=CYAN, width=3)
        txt(dr, (945, 260), "api.io", font(F_BOLD, 26), CYAN, anchor="mm")
        k = clamp((t - 6) / 8)
        xm = int(lerp(520, 760, k))
        dr.ellipse([xm - 12, 310 - 12, xm + 12, 310 + 12], fill=YELLOW)
        if t > 15:
            dr.rectangle([150, 460, 1130, 540], fill=(30, 20, 10), outline=ORANGE, width=3)
            txt(dr, (W // 2, 500), "OPTIONS preflight \u2192 Access-Control-Allow-Origin: app.com \u2713",
                font(F_MONO, 24), ORANGE, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 596), "CORS is the BROWSER's rule \u2014 the server just answers the preflight",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ react-frontend (fireship x1 + bbg x1 + primer x1)
def scene_rf_hooks(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "HOOKS IN 100 SECONDS", MAGENTA)
    lns = [("function Cart() {", (200, 200, 255)),
           ("  const [items, setItems] = useState([]);", YELLOW),
           ("  useEffect(() => {", (200, 200, 255)),
           ("    fetchCart().then(setItems);", (200, 200, 255)),
           ("  }, []);  // run once", YELLOW),
           ("  return <List items={items} />;", (200, 200, 255)),
           ("}", (200, 200, 255)),
           ("# state lives in the function now", GREEN)]
    hi = int(clamp((t - 5) / 13) * len(lns))
    code_panel(dr, 190, 140, W - 190, 580, "Cart.jsx", lns, hi_line=hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), "useState remembers \u2014 useEffect reaches out \u2014 no classes",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_rf_rerender(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE RE-RENDER CASCADE", CYAN)
    if t > 4:
        k = clamp((t - 4) / 8)
        boxes = [("App", 490, 200, 300, 80), ("Header", 280, 340, 220, 70),
                 ("Cart", 660, 340, 220, 70), ("Item x40", 660, 460, 220, 70)]
        for i, (lbl, x, y, w, h) in enumerate(boxes):
            lit = k * 4 > i
            dr.rectangle([x, y, x + w, y + h], fill=(12, 18, 32),
                         outline=RED if lit else DIM, width=3 if lit else 2)
            txt(dr, (x + w // 2, y + h // 2), lbl, font(F_MONO, 22), RED if lit else CREAM, anchor="mm")
        if t > 12:
            arrow(dr, 770, 340, 770, 460, RED, w=5)
        if t > 15:
            dr.rectangle([280, 340, 500, 410], outline=GREEN, width=4)
            txt(dr, (390, 450), "memoized \u2014 skipped", font(F_SANS, 22), GREEN, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 580), "one state change re-renders the tree \u2014 memo cuts the cascade",
            font(F_SANS, 25), YELLOW, anchor="mm")

def scene_rf_state(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "STATE DRIFT: TWO TRUTHS", font(F_BOLD, 38), CYAN, anchor="mm")
    txt(dr, (W // 2, 118), "two components, one cart \u2014 whose total is right?",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        k = int(clamp((t - 4) / 10) * 6)
        dr.rectangle([180, 220, 560, 420], fill=(16, 16, 30), outline=DIM, width=2)
        txt(dr, (370, 260), "Header", font(F_BOLD, 24), DIM, anchor="mm")
        dr.rectangle([720, 220, 1100, 420], fill=(16, 16, 30), outline=DIM, width=2)
        txt(dr, (910, 260), "Checkout", font(F_BOLD, 24), DIM, anchor="mm")
        if k >= 2:
            txt(dr, (370, 340), "$%.2f" % (42.0 + k), font(F_MONOB, 34), RED, anchor="mm")
            txt(dr, (910, 340), "$%.2f" % 42.0, font(F_MONOB, 34), ORANGE, anchor="mm")
        if t > 16:
            dr.rectangle([470, 480, 810, 560], fill=(12, 24, 12), outline=GREEN, width=3)
            txt(dr, (W // 2, 520), "ONE store \u2192 both read the same total",
                font(F_BOLD, 24), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 610), "single source of truth \u2014 state lives once, components subscribe",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ spring (fireship x1 + bbg x1 + story x1)
def scene_sp_di(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "DEPENDENCY INJECTION IN 100 SECONDS", MAGENTA)
    lns = [("@Service", YELLOW),
           ("class OrderService {", (200, 200, 255)),
           ("  @Autowired", YELLOW),
           ("  PaymentClient payments;", (200, 200, 255)),
           ("}", (200, 200, 255)),
           ("# the container builds the graph", GREEN),
           ("# you never call 'new'", GREEN)]
    hi = int(clamp((t - 5) / 12) * len(lns))
    code_panel(dr, 210, 150, W - 210, 570, "OrderService.java", lns, hi_line=hi, t=t)
    if t > 18:
        txt(dr, (W // 2, 615), "declare what you need \u2014 Spring supplies it",
            font(F_SANS, 26), CREAM, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 656), "inversion of control: the framework calls you",
            font(F_SANS, 24), DIM, anchor="mm")

def scene_sp_filter(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE FILTER CHAIN GAUNTLET", CYAN)
    filters = ["jwt", "cors", "csrf", "authz", "audit"]
    n = int(clamp((t - 5) / 12) * len(filters))
    for i, f in enumerate(filters):
        x = 120 + i * 210
        lit = i < n
        glow_box(dr, [x, 280, x + 180, 400], CYAN if lit else (40, 40, 60))
        dr.rectangle([x, 280, x + 180, 400], fill=(12, 18, 32),
                     outline=CYAN if lit else DIM, width=3 if lit else 2)
        txt(dr, (x + 90, 340), f, font(F_MONO, 24), CYAN if lit else DIM, anchor="mm")
        if i < n - 1:
            arrow(dr, x + 180, 340, x + 210, 340, GREEN if lit else DIM)
    if t > 18:
        txt(dr, (W // 2, 480), "request passes every filter \u2014 one rejection ends the chain",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 540), "security is a pipeline, not a checkpoint",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_sp_outage(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE 2 AM ROLLBACK", font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), "pager fires \u2014 the deploy that was supposed to be safe",
        font(F_SERIF, 24), DIM, anchor="mm")
    if t > 4:
        dr.rectangle([300, 220, 980, 300], fill=(40, 15, 15), outline=RED, width=3)
        txt(dr, (W // 2, 260), "ERROR RATE 38% \u2191", font(F_MONOB, 30), RED, anchor="mm")
        if t > 10:
            k = clamp((t - 10) / 6)
            txt(dr, (W // 2, 360), "kubectl rollout undo deployment/api",
                font(F_MONO, 24), YELLOW, anchor="mm")
            bar(dr, 340, 410, 600, 44, k, GREEN, label="rolling back")
        if t > 18:
            dr.rectangle([300, 500, 980, 570], fill=(15, 40, 15), outline=GREEN, width=3)
            txt(dr, (W // 2, 535), "ERROR RATE 0.2% \u2014 prod is breathing again",
                font(F_MONOB, 28), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 620), "rollback beats heroics \u2014 the deploy pipeline is the real on-call",
            font(F_SERIF, 25), CREAM, anchor="mm")

# ============================================================ dotnet (bbg x1 + fireship x1 + primer x1)
def scene_dn_clr(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "C# \u2192 IL \u2192 NATIVE: THE CLR PIPELINE", CYAN)
    stages = ["C#", "IL", "JIT", "native"]
    n = int(clamp((t - 5) / 12) * len(stages))
    for i, s in enumerate(stages):
        x = 130 + i * 260
        lit = i < n
        dr.rectangle([x, 260, x + 210, y if (y := 400) else 400], fill=(12, 18, 32),
                     outline=CYAN if lit else DIM, width=3 if lit else 2)
        txt(dr, (x + 105, 330), s, font(F_BOLD, 28), CYAN if lit else DIM, anchor="mm")
        if i < n - 1:
            arrow(dr, x + 210, 330, x + 260, 330, GREEN if lit else DIM)
    if t > 18:
        txt(dr, (W // 2, 480), "compile once to IL \u2014 the JIT compiles hot paths to native at runtime",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 540), "tiered compilation: fast start, then the JIT optimizes the hot loops",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_dn_linq(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "LINQ IN 100 SECONDS", MAGENTA)
    lns = [("var top = db.Orders", (200, 200, 255)),
           ("  .Where(o => o.Total > 100)", YELLOW),
           ("  .OrderByDescending(o => o.Total)", YELLOW),
           ("  .Take(10)", YELLOW),
           ("  .ToList();", (200, 200, 255)),
           ("# SQL-flavored C# \u2014 deferred until ToList()", GREEN)]
    hi = int(clamp((t - 5) / 12) * len(lns))
    code_panel(dr, 210, 150, W - 210, 570, "queries.cs", lns, hi_line=hi, t=t)
    if t > 18:
        txt(dr, (W // 2, 615), "query objects like tables \u2014 the provider translates to SQL",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_dn_null(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "NULLABLE: THE BILLION-DOLLAR FIX", font(F_BOLD, 38), CYAN, anchor="mm")
    txt(dr, (W // 2, 118), "null flows through four calls \u2014 watch the guardrails catch it",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        calls = ["GetUser()", ".Profile", ".Address", ".City"]
        n = int(clamp((t - 4) / 10) * len(calls))
        for i, c in enumerate(calls):
            x = 170 + i * 250
            here = i < n
            dr.rectangle([x, 280, x + 220, 400], fill=(16, 16, 30),
                         outline=TEAL if here else DIM, width=3 if here else 2)
            txt(dr, (x + 110, 340), c, font(F_MONO, 22), TEAL if here else DIM, anchor="mm")
            if i < n - 1:
                arrow(dr, x + 220, 340, x + 250, 340, DIM)
        if t > 15:
            dr.rectangle([300, 480, 980, 550], fill=(30, 20, 8), outline=ORANGE, width=3)
            txt(dr, (W // 2, 515), "string? city \u2014 the '?' makes null a compile-time question",
                font(F_MONO, 24), ORANGE, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 606), "nullability annotations move the crash from 3 AM to build time",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ docker (bbg x1 + fireship x1 + story x1)
def scene_dk_layers(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "LAYERS: REBUILD ONLY THE TOP", CYAN)
    layers = [("FROM python:3.12", 4, True), ("COPY reqs", 8, True),
              ("RUN pip install", 12, False), ("COPY . .", 17, False)]
    n = int(clamp((t - 4) / 12) * len(layers))
    for i, (L, ts, cached) in enumerate(layers):
        y = 230 + i * 85
        here = i < n
        col = GREEN if (here and cached) else (ORANGE if here else DIM)
        dr.rectangle([280, y, 1000, y + 64], fill=(12, 18, 32), outline=col, width=3 if here else 2)
        txt(dr, (320, y + 32), L, font(F_MONO, 24), col, anchor="lm")
        if here:
            txt(dr, (950, y + 32), "CACHED" if cached else "REBUILT", font(F_BOLD, 20),
                GREEN if cached else ORANGE, anchor="rm")
    if t > 19:
        txt(dr, (W // 2, 600), "changed one line of code \u2014 only the last layer rebuilt: 3s not 90s",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 650), "order the Dockerfile: stable layers first, churn last",
            font(F_SANS, 24), CREAM, anchor="mm")

def scene_dk_compose(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "COMPOSE IN 100 SECONDS", MAGENTA)
    svcs = ["web", "db", "redis"]
    n = int(clamp((t - 5) / 10) * len(svcs))
    for i, s in enumerate(svcs):
        x = 180 + i * 330
        lit = i < n
        glow_box(dr, [x, 260, x + 280, 430], MAGENTA if lit else (40, 40, 60))
        dr.rectangle([x, 260, x + 280, 430], fill=(16, 16, 30),
                     outline=MAGENTA if lit else DIM, width=3 if lit else 2)
        txt(dr, (x + 140, 310), s, font(F_BOLD, 28), MAGENTA if lit else DIM, anchor="mm")
        if lit and t > 12:
            txt(dr, (x + 140, 370), "healthy \u2713", font(F_SANS, 24), GREEN, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 500), "one file, one network \u2014 the whole stack with 'docker compose up'",
            font(F_SANS, 25), CREAM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 556), "depends_on + healthchecks \u2014 the DB is ready before the web boots",
            font(F_SANS, 24), YELLOW, anchor="mm")

def scene_dk_machine(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "IT WORKED ON MY MACHINE", font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), "the five most expensive words in software",
        font(F_SERIF, 24), DIM, anchor="mm")
    if t > 4:
        dr.rectangle([240, 220, 590, 420], fill=(20, 40, 20), outline=GREEN, width=3)
        txt(dr, (415, 280), "dev laptop", font(F_BOLD, 26), GREEN, anchor="mm")
        txt(dr, (415, 350), "\u2713 tests pass", font(F_SANS, 24), GREEN, anchor="mm")
        dr.rectangle([690, 220, 1040, 420], fill=(40, 20, 20), outline=RED, width=3)
        txt(dr, (865, 280), "production", font(F_BOLD, 26), RED, anchor="mm")
        if t > 10:
            txt(dr, (865, 350), "\u2717 glibc 2.28", font(F_SANS, 24), RED, anchor="mm")
            txt(dr, (865, 385), "  vs 2.34", font(F_SANS, 24), RED, anchor="mm")
        if t > 16:
            dr.rectangle([340, 470, 940, 550], fill=(15, 25, 15), outline=GOLD, width=3)
            txt(dr, (W // 2, 510), "one Dockerfile \u2192 identical everywhere",
                font(F_BOLD, 25), GOLD, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 600), "containers ship the environment with the code",
            font(F_SERIF, 25), CREAM, anchor="mm")

# ============================================================ terraform (bbg x1 + fireship x1 + primer x1)
def scene_tf_plan(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "PLAN BEFORE YOU APPLY", CYAN)
    lns = [("aws_s3_bucket.logs", GREEN),
           ("  + bucket = \"logs-prod\"     # create", GREEN),
           ("aws_instance.web", ORANGE),
           ("  ~ instance_type = \"t3.small -> t3.medium\"", ORANGE),
           ("aws_db.old", RED),
           ("  - # destroy", RED),
           ("Plan: 3 to add, 1 to change, 1 to destroy", YELLOW)]
    hi = int(clamp((t - 5) / 13) * len(lns))
    code_panel(dr, 190, 150, W - 190, 580, "terraform plan", lns, hi_line=hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), "read the plan like a contract \u2014 then type 'yes'",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_tf_state(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE STATE FILE IN 100 SECONDS", MAGENTA)
    if t > 4:
        lns = [('{', (200, 200, 255)),
               ('  "version": 4,', (200, 200, 255)),
               ('  "resources": [', (200, 200, 255)),
               ('    {"type": "aws_instance",', YELLOW),
               ('     "name": "web",', YELLOW),
               ('     "instances": [{ "id": "i-0abc", ... }]}', YELLOW),
               ('  ]', (200, 200, 255)),
               ('}', (200, 200, 255))]
        hi = int(clamp((t - 5) / 12) * len(lns))
        code_panel(dr, 210, 140, W - 210, 570, "terraform.tfstate", lns, hi_line=hi, t=t)
    if t > 18:
        txt(dr, (W // 2, 615), "the state is the memory of your infrastructure \u2014 lock it, version it",
            font(F_SANS, 25), CREAM, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 656), "hand-edit the state and Terraform will haunt you",
            font(F_SANS, 24), RED, anchor="mm")

def scene_tf_drift(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "DRIFT: SOMEONE CLICKED IN THE CONSOLE", font(F_BOLD, 36), CYAN, anchor="mm")
    txt(dr, (W // 2, 118), "declared vs actual \u2014 the plan catches the cheater",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        dr.rectangle([180, 220, 600, 480], fill=(16, 16, 30), outline=DIM, width=2)
        txt(dr, (390, 260), "declared (code)", font(F_BOLD, 24), TEAL, anchor="mm")
        txt(dr, (390, 340), "web x2", font(F_MONO, 26), TEAL, anchor="mm")
        dr.rectangle([680, 220, 1100, 480], fill=(16, 16, 30), outline=DIM, width=2)
        txt(dr, (890, 260), "actual (AWS)", font(F_BOLD, 24), ORANGE, anchor="mm")
        if t > 12:
            txt(dr, (890, 340), "web x3 !", font(F_MONO, 26), RED, anchor="mm")
            arrow(dr, 600, 350, 680, 350, RED, w=6)
        if t > 17:
            txt(dr, (W // 2, 540), "drift detected: 1 instance outside the code \u2014 plan removes it",
                font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 600), "clickops is debt \u2014 terraform plan is the audit",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ registry + render loop
SLUG_DIR = {
    "py": "python", "pyw": "python-web", "jv": "java",
    "cp": "cpp", "cc": "c-lang", "ds": "dsa",
    "fs": "fullstack", "rf": "react-frontend", "sp": "spring",
    "dn": "dotnet", "dk": "docker", "tf": "terraform",
}

def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    "py": "PYTHON \u00b7 Scripting & Automation",
    "pyw": "PYTHON WEB \u00b7 Django & APIs",
    "jv": "JAVA \u00b7 Enterprise & JVM",
    "cp": "C++ \u00b7 Systems & Performance",
    "cc": "C \u00b7 Memory & Pointers",
    "ds": "DSA \u00b7 Algorithms & Structures",
    "fs": "FULLSTACK \u00b7 Browser to Database",
    "rf": "REACT \u00b7 The Component Model",
    "sp": "SPRING \u00b7 Java Backend Framework",
    "dn": ".NET \u00b7 The CLR Platform",
    "dk": "DOCKER \u00b7 Containers",
    "tf": "TERRAFORM \u00b7 Infrastructure as Code",
}

VIDEOS = [
 # --- python
 V(BOOTCAMP_K["py"], "py", "py-walrus", "The Walrus in 100 Seconds",
   "assign and test in one breath", "fireship", scene_py_walrus,
   "The walrus operator := assigns and tests in a single expression \u2014 two lines become one. Assignment you can see swimming through the condition.",
   [(4,10,"The walrus operator: colon-equals, tusked assignment"),
    (10,16,"Assign AND test in one breath \u2014 if n := len(data)"),
    (16,22,"Two lines become one \u2014 assign, test, use"),
    (22,26,"The walrus: assignment swimming through the condition")]),
 V(BOOTCAMP_K["py"], "py", "py-gil", "The GIL: One Lock for 16 Cores",
   "threads for I/O, processes for CPU", "bbg", scene_py_gil,
   "Sixteen threads, sixteen cores \u2014 but only one holds the Global Interpreter Lock at a time. Threads for I/O, processes for CPU.",
   [(4,10,"Sixteen threads \u2014 sixteen cores \u2014 one lock"),
    (10,16,"The GIL: one thread runs Python bytecode at a time"),
    (16,22,"Threads for I/O \u2014 processes for CPU work"),
    (22,26,"Multiprocessing escapes the lock \u2014 pick the right tool")]),
 V(BOOTCAMP_K["py"], "py", "py-pip-hell", "Pip Hell: The Resolver's Gamble",
   "pin it or lose it", "primer", scene_py_pip,
   "Thirty packages, one install: the resolver hits a urllib3 version conflict and backtracks to a pinned version. pip freeze, pin it or lose it.",
   [(4,10,"Thirty packages \u2014 one install \u2014 the resolver thinks"),
    (10,16,"Conflict: requests wants urllib3>=2, botocore wants <1.27"),
    (16,22,"The resolver backtracks \u2014 pins urllib3 1.26.18"),
    (22,26,"pip freeze to requirements.txt \u2014 pin it or lose it")]),
 # --- python-web
 V(BOOTCAMP_K["pyw"], "pyw", "pyw-request-cycle", "A Request's Life in 100 Seconds",
   "every request runs the same gauntlet", "fireship", scene_pyw_cycle,
   "A request's life: URLconf routes, the view computes, the ORM queries, the template renders, the response returns. Slow view? Blame the ORM query first.",
   [(4,10,"A request arrives \u2014 URLconf routes it"),
    (10,16,"The view computes \u2014 the ORM queries"),
    (16,22,"The template renders \u2014 the response returns"),
    (22,26,"Route, compute, query, render \u2014 the same gauntlet every time")]),
 V(BOOTCAMP_K["pyw"], "pyw", "pyw-middleware", "The Middleware Onion",
   "order matters: auth before the view", "bbg", scene_pyw_mw,
   "Five middleware layers \u2014 auth, cors, session, csrf, gzip: the request dives in through every layer and the response climbs back out. Order matters.",
   [(4,10,"Five layers wrap every request \u2014 the middleware onion"),
    (10,16,"The request dives in \u2014 layer by layer"),
    (16,22,"The response climbs back out through the same layers"),
    (22,26,"Auth before the view \u2014 gzip after: order matters")]),
 V(BOOTCAMP_K["pyw"], "pyw", "pyw-first-deploy", "Goodbye, Localhost",
   "the first real deploy \u2014 a rite of passage", "story", scene_pyw_deploy,
   "Three months of building: tests, push, CI green, migrate, DNS \u2014 and yourapp.com is real. Someone on another continent just hit refresh.",
   [(4,10,"Three months of building \u2014 one localhost"),
    (10,16,"Tests \u00b7 push \u00b7 CI green \u00b7 migrate"),
    (16,22,"DNS propagates \u2014 yourapp.com is real"),
    (22,26,"First visitor from another timezone \u2014 goodbye, localhost")]),
 # --- java
 V(BOOTCAMP_K["jv"], "jv", "jv-stream", "Streams in 100 Seconds",
   "twelve lines of loops become one pipeline", "fireship", scene_jv_stream,
   "Streams: filter, map, distinct, collect \u2014 twelve lines of loops become one pipeline. Nothing runs until the terminal op: streams are lazy.",
   [(4,10,"The stream pipeline: filter, map, distinct, collect"),
    (10,16,"Filter by total \u2014 map to customer \u2014 distinct"),
    (16,22,"Collect: the terminal operation"),
    (22,26,"Twelve lines become one \u2014 lazy until collect")]),
 V(BOOTCAMP_K["jv"], "jv", "jv-gc", "The Garbage Collector's Sweep",
   "memory you forgot is memory you never owned", "bbg", scene_jv_gc,
   "Objects are born in eden, survivors age, the old never die \u2014 then a minor GC sweeps eden clean in 20ms. Memory you forgot is memory you never owned.",
   [(4,10,"Objects are born in eden \u2014 survivors age"),
    (10,16,"Eden fills \u2014 the garbage collector wakes"),
    (16,22,"Minor GC: eden swept clean \u2014 20ms pause"),
    (22,26,"Memory you forgot is memory you never owned")]),
 V(BOOTCAMP_K["jv"], "jv", "jv-hashmap", "HashMap: O(1) With an Asterisk",
   "resize at load factor 0.75", "3b1b", scene_jv_hash,
   "Sixteen buckets, collisions stack up into chains \u2014 lookup slides from O(1) toward O(n). Resize at load factor 0.75, rehash, and the speed returns.",
   [(4,10,"Sixteen buckets \u2014 keys land by hash"),
    (10,16,"Collisions chain up \u2014 +2 chain in bucket 5"),
    (16,22,"Chains grow: lookup slides from O(1) toward O(n)"),
    (22,26,"Resize at 0.75 load \u2014 rehash, speed returns")]),
 # --- cpp
 V(BOOTCAMP_K["cp"], "cp", "cpp-move", "Move: Steal, Don't Copy",
   "steal the guts, leave the husk", "bbg", scene_cpp_move,
   "Move semantics: std::move transfers the pointer instead of copying the bytes \u2014 copy is O(n), move is O(1). Steal the guts, leave the husk.",
   [(4,10,"A huge string \u2014 copy would duplicate every byte"),
    (10,16,"std::move: transfer the pointer, not the bytes"),
    (16,22,"Copy: O(n) \u2014 move: O(1) pointer swap"),
    (22,26,"Move semantics: steal the guts, leave the husk")]),
 V(BOOTCAMP_K["cp"], "cp", "cpp-templates", "Templates in 100 Seconds",
   "one function \u2014 stamped out per type", "fireship", scene_cpp_template,
   "template <typename T> max \u2014 one function stamped out per type at compile time: int, double, string. Compile-time codegen, zero runtime cost.",
   [(4,10,"template <typename T> \u2014 write max once"),
    (10,16,"Instantiate: int, double, string \u2014 three stamps"),
    (16,22,"The compiler generates each version"),
    (22,26,"Compile-time codegen \u2014 zero runtime cost")]),
 V(BOOTCAMP_K["cp"], "cp", "cpp-cache-miss", "The Cache Miss That Cost 100x",
   "traverse memory the way it lies", "3b1b", scene_cpp_cache,
   "Row-major vs column-major on a 64x64 grid: 0.02s vs 0.31s. Cache lines are 64 bytes \u2014 traverse memory the way it lies.",
   [(4,10,"A 64x64 grid \u2014 two traversal orders"),
    (10,16,"Row-major walks with the cache \u2014 0.02s"),
    (16,22,"Column-major thrashes it \u2014 0.31s, 15x slower"),
    (22,26,"Cache lines are 64 bytes \u2014 traverse memory the way it lies")]),
 # --- c-lang
 V(BOOTCAMP_K["cc"], "cc", "cc-pointers", "Pointers in 100 Seconds",
   "an address is just a number", "fireship", scene_cc_ptr,
   "A pointer is just an address \u2014 *p reads the value AT that address. And p++ moves by sizeof(int), not by one: the type is the stride.",
   [(4,10,"Eight memory cells \u2014 addresses 0xA0 to 0xA7"),
    (10,16,"*p: the pointer reads the value AT its address"),
    (16,22,"The arrow lands \u2014 dereference shows the value"),
    (22,26,"p++ strides by sizeof(int) \u2014 the type is the stride")]),
 V(BOOTCAMP_K["cc"], "cc", "cc-stack-heap", "Stack vs Heap: The Great Divide",
   "every malloc needs a free", "bbg", scene_cc_mem,
   "The stack grows down, the heap grows up. Stack: automatic, fast, freed on return. Heap: malloc'd, yours to free \u2014 leak it and the OOM killer comes.",
   [(4,10,"One address space \u2014 two tenants"),
    (10,16,"The stack grows down \u2014 automatic and fast"),
    (16,22,"The heap grows up \u2014 malloc'd, yours to free"),
    (22,26,"Every malloc needs a free \u2014 leak it and the OOM killer comes")]),
 V(BOOTCAMP_K["cc"], "cc", "cc-segfault", "The Segfault Simulator",
   "bounds are YOUR job in C", "primer", scene_cc_seg,
   "An array of eight, the cursor walks off the end: index 8 \u2014 Segmentation fault (core dumped). Bounds are YOUR job in C.",
   [(4,10,"An array of eight \u2014 the cursor starts walking"),
    (10,16,"Indices 0 through 7 \u2014 legal territory"),
    (16,22,"Index 8 \u2014 segmentation fault, core dumped"),
    (22,26,"Bounds are YOUR job in C \u2014 the OS punishes the careless")]),
 # --- dsa
 V(BOOTCAMP_K["ds"], "ds", "ds-master-theorem", "The Master Theorem",
   "divide, conquer, combine", "3b1b", scene_ds_master,
   "T(n) = a\u00b7T(n/b) + f(n): the recursion tree grows level by level \u2014 Case 1, leaves dominate, mergesort lives here: O(n log n).",
   [(4,10,"T(n) = a \u00b7 T(n/b) + f(n) \u2014 the recurrence"),
    (10,16,"The tree divides: a subproblems per level"),
    (16,22,"Case 1: leaves dominate \u2014 mergesort: O(n log n)"),
    (22,26,"Divide, conquer, combine \u2014 the theorem reads the tree")]),
 V(BOOTCAMP_K["ds"], "ds", "ds-bfs-dfs", "BFS vs DFS in 100 Seconds",
   "queue for breadth, stack for depth", "fireship", scene_ds_bfs,
   "BFS walks level by level with a queue \u2014 0, 1, 3, 2, 4 \u2014 shortest path guaranteed. DFS digs deep and backtracks. Queue for breadth, stack for depth.",
   [(4,10,"Five nodes \u2014 two traversal strategies"),
    (10,16,"BFS: the queue visits level by level \u2014 0, 1, 3"),
    (16,22,"Every node seen \u2014 order 0, 1, 3, 2, 4"),
    (22,26,"BFS: shortest path \u00b7 DFS: dig deep, backtrack")]),
 V(BOOTCAMP_K["ds"], "ds", "ds-lru", "The LRU Cache: Forget the Cold",
   "hash map + doubly-linked list", "bbg", scene_ds_lru,
   "LRU cache, capacity 3: key 4 hasn't been touched \u2014 it goes. Hash map for O(1) lookup plus a doubly-linked list for recency order.",
   [(4,10,"Capacity 3 \u2014 four keys want in"),
    (10,16,"Every get refreshes the key's recency"),
    (16,22,"Key 4 is coldest \u2014 evicted"),
    (22,26,"Hash map for O(1) \u00b7 linked list for order")]),
 # --- fullstack
 V(BOOTCAMP_K["fs"], "fs", "fs-localhost", "Goodbye, Localhost",
   "the first real deploy \u2014 a rite of passage", "story", scene_fs_localhost,
   "Three months of building: dev, DB wired, auth done, deploy, DNS \u2014 yourapp.com is real, and someone on another continent just hit refresh.",
   [(4,10,"Three months of building \u2014 one lonely localhost"),
    (10,16,"DB wired \u00b7 auth done \u00b7 deploy green"),
    (16,22,"DNS propagates \u2014 yourapp.com is real"),
    (22,26,"First visitor from another timezone \u2014 goodbye, localhost")]),
 V(BOOTCAMP_K["fs"], "fs", "fs-jwt", "The JWT Handshake",
   "the server verifies, never stores", "bbg", scene_fs_auth,
   "POST /login returns a signed token; every request carries it in the header \u2014 the server verifies, never stores. 200 OK, or 401 when it expires.",
   [(4,10,"POST /login \u2014 credentials over the wire"),
    (10,16,"The server signs a token \u2014 valid 24 hours"),
    (16,22,"Every request carries it \u2014 verify, never store"),
    (22,26,"200 OK with a live token \u00b7 401 when it expires")]),
 V(BOOTCAMP_K["fs"], "fs", "fs-cors", "CORS in 100 Seconds",
   "the browser's rule, the server's answer", "fireship", scene_fs_cors,
   "app.com fetches api.io: the browser fires an OPTIONS preflight, the server answers Access-Control-Allow-Origin \u2014 CORS is the browser's rule.",
   [(4,10,"app.com fetches api.io \u2014 different origins"),
    (10,16,"The browser fires an OPTIONS preflight"),
    (16,22,"Server answers: Access-Control-Allow-Origin: app.com"),
    (22,26,"CORS is the browser's rule \u2014 the server just answers")]),
 # --- react-frontend
 V(BOOTCAMP_K["rf"], "rf", "rf-hooks", "Hooks in 100 Seconds",
   "state lives in the function now", "fireship", scene_rf_hooks,
   "useState remembers, useEffect reaches out \u2014 the Cart component holds state in the function itself. No classes, no this, just hooks.",
   [(4,10,"function Cart() \u2014 no class in sight"),
    (10,16,"useState: the component remembers its items"),
    (16,22,"useEffect: fetch the cart \u2014 run once"),
    (22,26,"useState remembers \u00b7 useEffect reaches out \u00b7 no classes")]),
 V(BOOTCAMP_K["rf"], "rf", "rf-rerender", "The Re-Render Cascade",
   "memo cuts the cascade", "bbg", scene_rf_rerender,
   "One state change re-renders the whole tree \u2014 App, Cart, all forty Items light up red. memo() on the Header skips it. Memo cuts the cascade.",
   [(4,10,"One state change \u2014 the tree lights up"),
    (10,16,"App, Cart, forty Items \u2014 all re-rendering"),
    (16,22,"The Header is memoized \u2014 skipped, green"),
    (22,26,"One change re-renders the tree \u2014 memo cuts the cascade")]),
 V(BOOTCAMP_K["rf"], "rf", "rf-state-drift", "State Drift: Two Truths",
   "single source of truth", "primer", scene_rf_state,
   "The Header shows $48, Checkout shows $42 \u2014 two components, one cart, two truths. One store: both read the same total. Single source of truth.",
   [(4,10,"Two components \u2014 one cart \u2014 whose total is right?"),
    (10,16,"Header: $48 \u2014 Checkout: $42 \u00b7 drift!"),
    (16,22,"One store \u2014 both subscribe to the same total"),
    (22,26,"State lives once \u00b7 components subscribe \u2014 single source of truth")]),
 # --- spring
 V(BOOTCAMP_K["sp"], "sp", "sp-di", "Dependency Injection in 100 Seconds",
   "the framework calls you", "fireship", scene_sp_di,
   "@Autowired PaymentClient \u2014 the Spring container builds the whole object graph. You declare what you need; the framework supplies it. Inversion of control.",
   [(4,10,"@Service OrderService \u2014 it needs a PaymentClient"),
    (10,16,"@Autowired \u2014 declare what you need"),
    (16,22,"The container builds the graph \u2014 you never call new"),
    (22,26,"Inversion of control: the framework calls you")]),
 V(BOOTCAMP_K["sp"], "sp", "sp-filter-chain", "The Filter Chain Gauntlet",
   "security is a pipeline, not a checkpoint", "bbg", scene_sp_filter,
   "Five filters \u2014 jwt, cors, csrf, authz, audit: the request passes every one or the chain ends. Security is a pipeline, not a checkpoint.",
   [(4,10,"Five filters stand between the request and your code"),
    (10,16,"JWT, CORS, CSRF, authz, audit \u2014 in order"),
    (16,22,"One rejection ends the chain \u2014 the request dies"),
    (22,26,"Security is a pipeline \u2014 not a checkpoint")]),
 V(BOOTCAMP_K["sp"], "sp", "sp-2am-rollback", "The 2 AM Rollback",
   "rollback beats heroics", "story", scene_sp_outage,
   "The pager fires: error rate 38%. kubectl rollout undo \u2014 the error rate falls to 0.2% and prod breathes again. Rollback beats heroics.",
   [(4,10,"2 AM \u2014 the pager fires \u2014 error rate 38%"),
    (10,16,"kubectl rollout undo deployment/api"),
    (16,22,"Error rate 0.2% \u2014 prod is breathing again"),
    (22,26,"Rollback beats heroics \u2014 the pipeline is the real on-call")]),
 # --- dotnet
 V(BOOTCAMP_K["dn"], "dn", "dn-clr", "C# to IL to Native: The CLR Pipeline",
   "the JIT optimizes the hot loops", "bbg", scene_dn_clr,
   "Compile once to IL; the JIT compiles hot paths to native at runtime. Tiered compilation: fast start, then the hot loops get optimized.",
   [(4,10,"C# compiles to IL \u2014 one intermediate language"),
    (10,16,"The JIT compiles hot paths to native at runtime"),
    (16,22,"Tiered: fast start, then optimize the hot loops"),
    (22,26,"Write once \u2014 the CLR makes it native")]),
 V(BOOTCAMP_K["dn"], "dn", "dn-linq", "LINQ in 100 Seconds",
   "SQL-flavored C#", "fireship", scene_dn_linq,
   "Where, OrderByDescending, Take, ToList \u2014 query objects like tables, and the provider translates to SQL. Deferred until ToList().",
   [(4,10,"db.Orders \u2014 query objects like tables"),
    (10,16,"Where, OrderByDescending, Take \u2014 the chain"),
    (16,22,"ToList(): the query finally executes"),
    (22,26,"SQL-flavored C# \u2014 deferred until ToList()")]),
 V(BOOTCAMP_K["dn"], "dn", "dn-nullable", "Nullable: The Billion-Dollar Fix",
   "nullability moves the crash to build time", "primer", scene_dn_null,
   "Null flows through four calls: GetUser().Profile.Address.City \u2014 string? makes null a compile-time question. The crash moves from 3 AM to build time.",
   [(4,10,"Null flows through four calls \u2014 GetUser to City"),
    (10,16,"Any link could be null \u2014 the chain is fragile"),
    (16,22,"string? \u2014 the '?' makes null a compile-time question"),
    (22,26,"The crash moves from 3 AM to build time")]),
 # --- docker
 V(BOOTCAMP_K["dk"], "dk", "dk-layers", "Layers: Rebuild Only the Top",
   "stable layers first, churn last", "bbg", scene_dk_layers,
   "Four Dockerfile layers: the first two cached, the last two rebuilt. One line of code changed \u2014 3 seconds, not 90. Stable layers first, churn last.",
   [(4,10,"Four layers \u2014 base, deps, build, code"),
    (10,16,"FROM and pip install \u2014 cached, untouched"),
    (16,22,"Only the top layer rebuilt \u2014 3s, not 90s"),
    (22,26,"Order the Dockerfile: stable first, churn last")]),
 V(BOOTCAMP_K["dk"], "dk", "dk-compose", "Compose in 100 Seconds",
   "the whole stack with one command", "fireship", scene_dk_compose,
   "Web, DB, Redis: one file, one network, healthchecks green \u2014 the whole stack with 'docker compose up'. The DB is ready before the web boots.",
   [(4,10,"Three services \u2014 web, db, redis \u2014 one file"),
    (10,16,"Compose starts them on one network"),
    (16,22,"Healthchecks green \u2014 DB ready before web boots"),
    (22,26,"One file \u00b7 one network \u00b7 'docker compose up'")]),
 V(BOOTCAMP_K["dk"], "dk", "dk-works-on-my-machine", "It Worked on My Machine",
   "containers ship the environment with the code", "story", scene_dk_machine,
   "Tests pass on the laptop, production dies on glibc 2.28 vs 2.34 \u2014 the five most expensive words in software. One Dockerfile: identical everywhere.",
   [(4,10,"Dev laptop: all tests pass \u2014 green"),
    (10,16,"Production: glibc 2.28 vs 2.34 \u2014 red"),
    (16,22,"One Dockerfile \u2014 identical everywhere"),
    (22,26,"Containers ship the environment with the code")]),
 # --- terraform
 V(BOOTCAMP_K["tf"], "tf", "tf-plan", "Plan Before You Apply",
   "read the plan like a contract", "bbg", scene_tf_plan,
   "terraform plan: 3 to add, 1 to change, 1 to destroy \u2014 green creates, orange modifies, red destroys. Read the plan like a contract, then type 'yes'.",
   [(4,10,"terraform plan \u2014 the preview of everything"),
    (10,16,"Green: create \u2014 orange: modify \u2014 red: destroy"),
    (16,22,"Plan: 3 to add, 1 to change, 1 to destroy"),
    (22,26,"Read the plan like a contract \u2014 then type yes")]),
 V(BOOTCAMP_K["tf"], "tf", "tf-state", "The State File in 100 Seconds",
   "lock it, version it, never hand-edit it", "fireship", scene_tf_state,
   "terraform.tfstate is the memory of your infrastructure \u2014 every resource ID it tracks. Lock it, version it \u2014 and never hand-edit it.",
   [(4,10,"terraform.tfstate \u2014 the memory of your infra"),
    (10,16,"Every resource ID \u2014 mapped, tracked"),
    (16,22,"Remote backend \u2014 state locking on"),
    (22,26,"Lock it, version it \u2014 never hand-edit it")]),
 V(BOOTCAMP_K["tf"], "tf", "tf-drift", "Drift: Someone Clicked in the Console",
   "clickops is debt \u2014 terraform plan is the audit", "primer", scene_tf_drift,
   "Declared: web x2. Actual: web x3 \u2014 someone clicked in the console. Drift detected: the plan removes the rogue instance. ClickOps is debt.",
   [(4,10,"Declared in code: web x2 \u2014 actual in AWS: ?"),
    (10,16,"Actual: web x3 \u2014 someone clicked in the console"),
    (16,22,"Drift detected \u2014 the plan removes the rogue"),
    (22,26,"ClickOps is debt \u2014 terraform plan is the audit")]),
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
