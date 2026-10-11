#!/usr/bin/env python3
"""Batch 3 video generator: IL-15..IL-21, 21 videos x 30s, 1280x720 @ 24fps.
Mirrors gen_batch2.py: silent h264 MP4s, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / 3b1b / fireship / bbg / primer. Original animations only.

Course -> style map:
 IL-15 Data Engineering & Analytics : bbg x2 + fireship
 IL-16 ML & AI Engineering          : 3b1b x2 + fireship
 IL-17 Agentic AI Engineering       : fireship + bbg x2
 IL-18 Technical Leadership         : story + bbg x2
 IL-19 MultiCloud DevOps & AI       : bbg x2 + fireship
 IL-20 Mathematics                  : 3b1b x3
 IL-21 Humanities                   : story x3
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

# ============================================================ IL-15: Data Engineering & Analytics
def scene_lakehouse(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "The Lakehouse: Bronze, Silver, Gold", BLUE)
    zones = [("BRONZE", "raw landing", ORANGE, 250),
             ("SILVER", "cleaned + validated", TEAL, 640),
             ("GOLD", "business-ready", YELLOW, 1030)]
    for name, sub, col, x in zones:
        idx = zones.index((name, sub, col, x))
        on = t >= 5 + idx * 3.5
        glow_box(dr, [x - 160, 200, x + 160, 480], col if on else (60, 60, 90), rad=14)
        dr.rectangle([x - 160, 200, x + 160, 480], fill=(12, 16, 34))
        txt(dr, (x, 280), name, font(F_BOLD, 34), col if on else DIM, anchor="mm")
        txt(dr, (x, 340), sub, font(F_SANS, 22), DIM, anchor="mm")
        rows = 3 + idx
        for r in range(rows):
            rw = 200 - r * 20
            if t >= 6 + idx * 3.5 + r * 0.4:
                dr.rectangle([x - rw // 2, 390 + r * 22, x + rw // 2, 404 + r * 22],
                             fill=col)
        if idx < 2:
            arrow(dr, x + 165, 340, zones[idx + 1][3] - 165, 340, DIM, 5)
    if t > 20:
        glow_box(dr, [250 - 160, 520, 1030 + 160, 620], GREEN, rad=12)
        dr.rectangle([250 - 160, 520, 1030 + 160, 620], fill=(10, 34, 22))
        txt(dr, (W // 2, 570), "one copy of the truth \u2014 refined in stages, queried anywhere",
            font(F_BOLD, 28), GREEN, anchor="mm")

def scene_stream(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Stream Processing: Events Never Wait", BLUE)
    stages = [("SOURCES", BLUE), ("BROKER", CYAN), ("STREAM JOB", MAGENTA), ("SINKS", GREEN)]
    n = len(stages); bw = 220; gap = 40
    total = n * bw + (n - 1) * gap; x0 = (W - total) // 2
    for i, (name, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        on = t >= 4 + i * 2.5
        glow_box(dr, [x, 220, x + bw, 400], col if on else (60, 60, 90), rad=14)
        dr.rectangle([x, 220, x + bw, 400], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 290), name, font(F_BOLD, 28), col if on else DIM, anchor="mm")
        if i < n - 1:
            arrow(dr, x + bw + 4, 310, x + bw + gap - 4, 310, DIM, 5)
    # event dots flowing
    if t > 6:
        for k2 in range(10):
            ph = ((t - 6) * 0.9 + k2 * 0.28) % 1.0
            px = x0 + ph * total
            dr.ellipse([px - 10, 440 - 10, px + 10, 440 + 10], fill=WHITE)
            dr.ellipse([px - 6, 440 - 6, px + 6, 440 + 6], fill=MAGENTA)
    # tumbling windows
    if t > 12:
        panel(dr, [x0, 490, x0 + total, 630], "TUMBLING WINDOW: 5 MIN", CYAN, 24)
        for w_i in range(6):
            wx = x0 + 40 + w_i * (total - 80) // 5
            hot = (t - 12) // 1.6 % 6 == w_i
            dr.rectangle([wx - 45, 545, wx + 45, 600],
                         fill=(0, 120, 130) if hot else (20, 30, 50),
                         outline=CYAN, width=2)
            txt(dr, (wx, 572), str(100 + w_i * 37), font(F_MONO, 22), WHITE, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 665), "batch asks what happened \u2014 streaming answers as it happens",
            font(F_BOLD, 28), MAGENTA, anchor="mm")

def scene_windowfn(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "SQL Window Functions", font(F_BOLD, 42), WHITE, anchor="mm")
    lines = [("SELECT name, dept, salary,", (200, 200, 255)),
             ("  RANK() OVER (", (0, 229, 255)),
             ("    PARTITION BY dept", (255, 214, 0)),
             ("    ORDER BY salary DESC", (255, 214, 0)),
             ("  ) AS pay_rank", (0, 229, 255)),
             ("FROM employees;", (200, 200, 255))]
    code_panel(dr, 60, 130, 560, 560, "rank.sql", lines,
               hi_line=min(5, 1 + int((t - 4) / 3)), t=t)
    # mini table result
    rows = [("Ava", "eng", 150, 1), ("Ben", "eng", 140, 2), ("Cy", "ops", 130, 1),
            ("Di", "ops", 120, 2)]
    hdr = ["name", "dept", "k$", "rank"]
    x0, y0, cw = 640, 200, 150
    for j, h in enumerate(hdr):
        txt(dr, (x0 + j * cw, y0), h, font(F_MONOB, 24), CYAN, anchor="mm")
    for i, row in enumerate(rows):
        if t < 8 + i * 2:
            continue
        y = y0 + 60 + i * 55
        dr.line([x0 - 40, y + 24, x0 + 3 * cw + 40, y + 24], fill=(50, 50, 80), width=2)
        for j, val in enumerate(row):
            hot = (j == 3)
            txt(dr, (x0 + j * cw, y), str(val), font(F_MONO, 26),
                GREEN if hot else WHITE, anchor="mm")
    if t > 20:
        txt(dr, (920, 520), "aggregate without collapsing rows",
            font(F_BOLD, 28), YELLOW, anchor="mm")
        txt(dr, (920, 560), "partition = independent leaderboards",
            font(F_SANS, 24), DIM, anchor="mm")

# ============================================================ IL-16: ML & AI Engineering
def scene_backprop(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "Backprop: blame flows backwards", font(F_BOLD, 42), WHITE, anchor="mm")
    layers = [(200, 3), (520, 4), (840, 4), (1100, 2)]
    nodes = []
    for x, cnt in layers:
        col_nodes = []
        for j in range(cnt):
            y = 400 + (j - (cnt - 1) / 2) * 110
            col_nodes.append((x, y))
        nodes.append(col_nodes)
    k = clamp((t - 5) / 8)
    for li in range(len(nodes) - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                dr.line([a[0], a[1], b[0], b[1]], fill=(60, 80, 140), width=2)
    for li, coln in enumerate(nodes):
        if k * len(nodes) < li:
            continue
        for x, y in coln:
            dr.ellipse([x - 24, y - 24, x + 24, y + 24], fill=(10, 20, 50),
                       outline=TEAL, width=3)
    txt(dr, (1100, 130), "prediction", font(F_SANS, 24), DIM, anchor="mm")
    # forward pass sweep
    if 8 < t < 14:
        fx = lerp(200, 1100, ease((t - 8) / 6))
        dr.ellipse([fx - 12, 388, fx + 12, 412], fill=WHITE)
    # backward error wave
    if t >= 14:
        bk = clamp((t - 14) / 8)
        bx = lerp(1100, 200, ease(bk))
        dr.ellipse([bx - 14, 386, bx + 14, 414], fill=RED)
        dr.ellipse([bx - 8, 392, bx + 8, 408], fill=WHITE)
        for li in range(len(nodes) - 1, 0, -1):
            thr = (len(nodes) - li) / len(nodes)
            if bk >= thr:
                for a in nodes[li - 1]:
                    for b in nodes[li]:
                        dr.line([a[0], a[1], b[0], b[1]], fill=RED, width=4)
        txt(dr, (W // 2, 620), "\u2202 loss / \u2202 weight \u2014 every layer gets its share of blame",
            font(F_BOLD, 30), RED, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 665), "chain rule at scale: millions of gradients, one backward sweep",
            font(F_BOLD, 28), YELLOW, anchor="mm")

def scene_biasvar(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "Bias vs Variance: the fitting dilemma", font(F_BOLD, 42), WHITE, anchor="mm")
    _r.seed(7)
    pts = [(x, 420 + 120 * math.sin(x / 90) + _r.uniform(-28, 28)) for x in range(180, 1101, 60)]
    dr.rectangle([150, 150, 1130, 620], fill=(10, 16, 36), outline=DIM, width=2)
    for x, y in pts:
        dr.ellipse([x - 7, y - 7, x + 7, y + 7], fill=CYAN)
    k = clamp((t - 5) / 14)
    phase = min(2, int(k * 3))
    xs = [x for x, _ in pts]
    if phase == 0:
        # underfit: straight line
        y0, y1 = 460, 380
        dr.line([xs[0], y0, xs[-1], y1], fill=RED, width=5)
        lbl = "degree 1 \u2014 UNDERFIT: misses the pattern (high bias)"
    elif phase == 1:
        # good fit: smooth curve
        seq = [(x, 420 + 110 * math.sin(x / 95)) for x in range(xs[0], xs[-1] + 1, 8)]
        dr.line(seq, fill=GREEN, width=5)
        lbl = "degree 4 \u2014 JUST RIGHT: captures the signal"
    else:
        # overfit: wiggly through every point
        seq = []
        for i in range(len(pts) - 1):
            x0p, y0p = pts[i]; x1p, y1p = pts[i + 1]
            for s2 in range(11):
                u = s2 / 10
                wob = 60 * math.sin(u * math.pi) * (1 if i % 2 else -1)
                seq.append((lerp(x0p, x1p, u), lerp(y0p, y1p, u) + wob * 0.15))
        dr.line(seq, fill=ORANGE, width=4)
        lbl = "degree 15 \u2014 OVERFIT: memorizes noise (high variance)"
    col = [RED, GREEN, ORANGE][phase]
    txt(dr, (W // 2, 660), lbl, font(F_BOLD, 30), col, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 120), "validation error is U-shaped \u2014 tune complexity, not just fit",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_mlpipeline(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "The ML Pipeline: train \u2192 evaluate \u2192 ship", font(F_BOLD, 38), WHITE, anchor="mm")
    lines = [("pipeline = Pipeline([", (200, 200, 255)),
             ('  ("features", scaler),', (0, 229, 255)),
             ('  ("model", XGBRegressor()),', (0, 229, 255)),
             ("])", (200, 200, 255)),
             ("pipeline.fit(X_train, y_train)", (255, 214, 0)),
             ("score = pipeline.score(X_test)", (255, 214, 0))]
    code_panel(dr, 60, 140, 540, 560, "train.py", lines,
               hi_line=min(5, int((t - 4) / 3)), t=t)
    stages = [("TRAIN", CYAN, 640), ("EVALUATE", YELLOW, 830), ("DEPLOY", GREEN, 1020)]
    for name, col, x in stages:
        idx = stages.index((name, col, x))
        on = t >= 7 + idx * 4
        glow_box(dr, [x - 85, 200, x + 85, 330], col if on else (60, 60, 100), rad=12)
        dr.rectangle([x - 85, 200, x + 85, 330], fill=(12, 12, 26))
        txt(dr, (x, 255), name, font(F_BOLD, 26), col if on else DIM, anchor="mm")
        if on:
            txt(dr, (x, 300), "\u2713", font(F_BOLD, 32), col, anchor="mm")
        if idx < 2:
            arrow(dr, x + 90, 265, stages[idx + 1][2] - 90, 265, DIM, 5)
    if t > 20:
        panel(dr, [600, 400, 1220, 560], "METRICS GATE", GREEN, 26)
        txt(dr, (910, 480), "RMSE 0.42 \u00b7 drift check \u2014 PASS \u2192 shadow deploy",
            font(F_BOLD, 28), GREEN, anchor="mm")
    if t > 24:
        txt(dr, (W // 2, 610), "a model is code + data \u2014 version both",
            font(F_BOLD, 28), WHITE, anchor="mm")

# ============================================================ IL-17: Agentic AI Engineering
def scene_agentloop(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "The ReAct Loop: think, act, observe", font(F_BOLD, 38), WHITE, anchor="mm")
    lines = [("while not done:", (200, 200, 255)),
             ('  thought = llm(think_prompt)', (0, 229, 255)),
             ("  action  = parse_tool(thought)", (255, 214, 0)),
             ("  obs     = tool.run(action)", (0, 229, 255)),
             ("  memory.append(obs)", (255, 214, 0)),
             ("  done    = check_goal(obs)", (200, 200, 255))]
    code_panel(dr, 60, 140, 540, 600, "agent.py", lines,
               hi_line=min(5, int((t - 4) / 3.4)), t=t)
    nodes = [("THINK", MAGENTA, 660), ("ACT", CYAN, 880), ("OBSERVE", YELLOW, 1100)]
    for name, col, x in nodes:
        idx = nodes.index((name, col, x))
        on = t >= 6 + idx * 2
        dr.ellipse([x - 70, 230 - 70, x + 70, 230 + 70], fill=(12, 12, 26),
                   outline=col if on else (60, 60, 100), width=4)
        txt(dr, (x, 230), name, font(F_BOLD, 24), col if on else DIM, anchor="mm")
    # orbiting token
    if t > 6:
        ang = (t - 6) * 1.6
        cx, cy = 880, 230
        px, py = cx + 220 * math.cos(ang), cy + 120 * math.sin(ang)
        dr.ellipse([px - 12, py - 12, px + 12, py + 12], fill=WHITE)
    if t > 20:
        txt(dr, (880, 420), "agents = LLMs in a while-loop with tools",
            font(F_BOLD, 30), WHITE, anchor="mm")
        txt(dr, (880, 470), "guardrails bound every action",
            font(F_SANS, 26), DIM, anchor="mm")

def scene_agentmem(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Agent Memory: Short-Term + Long-Term", BLUE)
    # context window (short term)
    panel(dr, [60, 200, 560, 520], "CONTEXT WINDOW", CYAN, 26)
    k = clamp((t - 5) / 12)
    for i in range(8):
        if i / 8 > k:
            continue
        y = 270 + i * 30
        rw = 380 - i * 30
        dr.rectangle([90, y, 90 + rw, y + 18], fill=CYAN if i < 6 else YELLOW)
    txt(dr, (310, 540 - 0), "fills up \u2014 then it must forget", font(F_SANS, 22), DIM, anchor="mm")
    # vector memory (long term)
    panel(dr, [720, 200, 1220, 520], "VECTOR MEMORY", MAGENTA, 26)
    for i in range(12):
        if t < 8 + i * 0.8:
            continue
        x = 760 + (i % 4) * 105; y = 270 + (i // 4) * 70
        dr.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(40, 10, 50), outline=MAGENTA, width=3)
        txt(dr, (x, y), str(7 + i * 3), font(F_MONO, 20), MAGENTA, anchor="mm")
    txt(dr, (970, 540 - 0), "embeddings persist across sessions", font(F_SANS, 22), DIM, anchor="mm")
    # retrieval arrow
    if t > 16:
        arrow(dr, 720, 640, 560, 560, YELLOW, 5)
        txt(dr, (640, 620), "RAG recall", font(F_BOLD, 26), YELLOW, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 680 - 20), "short-term reasons \u2014 long-term remembers",
            font(F_BOLD, 30), WHITE, anchor="mm")

def scene_multiagent(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Multi-Agent Systems: Divide and Conquer", BLUE)
    glow_box(dr, [W // 2 - 150, 160, W // 2 + 150, 300], BLUE, rad=14)
    dr.rectangle([W // 2 - 150, 160, W // 2 + 150, 300], fill=(12, 16, 34))
    txt(dr, (W // 2, 215), "ORCHESTRATOR", font(F_BOLD, 30), BLUE, anchor="mm")
    txt(dr, (W // 2, 258), "plans + delegates", font(F_SANS, 22), DIM, anchor="mm")
    specs = [("RESEARCHER", TEAL, 250), ("CODER", CYAN, 530),
             ("REVIEWER", YELLOW, 810), ("DEPLOYER", GREEN, 1090)]
    for name, col, x in specs:
        idx = specs.index((name, col, x))
        on = t >= 6 + idx * 2.2
        glow_box(dr, [x - 120, 400, x + 120, 540], col if on else (60, 60, 90), rad=12)
        dr.rectangle([x - 120, 400, x + 120, 540], fill=(12, 16, 34))
        txt(dr, (x, 455), name, font(F_BOLD, 26), col if on else DIM, anchor="mm")
        if on:
            txt(dr, (x, 505), "\u2713 task done", font(F_SANS, 22), col, anchor="mm")
        arrow(dr, W // 2, 305, x, 395, DIM, 4)
        if on:
            arrow(dr, x, 395, W // 2, 305, col, 3)
    if t > 20:
        txt(dr, (W // 2, 600), "specialists in parallel \u2014 the orchestrator merges",
            font(F_BOLD, 30), WHITE, anchor="mm")

# ============================================================ IL-18: Technical Leadership
def scene_warroom(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)
    txt(dr, (W // 2, 80), "THE WAR ROOM", font(F_SERIFB, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "launch night, 2:47 AM", font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    phases = [("the page fires", 5), ("one voice commands", 11),
              ("mitigate, don\u2019t blame", 17), ("the blameless retro", 23)]
    for i, (ph, born) in enumerate(phases):
        if t < born:
            continue
        y = 240 + i * 90
        dr.ellipse([W // 2 - 14, y - 14, W // 2 + 14, y + 14], fill=GOLD)
        txt(dr, (W // 2 + 50, y), ph, font(F_SERIF, 30), CREAM, anchor="lm")
    if t > 26:
        txt(dr, (W // 2, 640), "leadership is calm made contagious",
            font(F_SERIF, 28), (200, 185, 160), anchor="mm")

def scene_raci(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "RACI: Who Owns What", BLUE)
    roles = ["R", "A", "C", "I"]
    tasks = ["launch plan", "rollback decision", "comms", "retro"]
    x0, y0, cw, rh = 340, 200, 190, 80
    for j, r in enumerate(roles):
        txt(dr, (x0 + j * cw, y0 - 40), r, font(F_BOLD, 34), CYAN, anchor="mm")
    full = {"R": "does the work", "A": "owns the outcome",
            "C": "consulted first", "I": "kept informed"}
    for j, r in enumerate(roles):
        txt(dr, (x0 + j * cw, 640), full[r], font(F_SANS, 20), DIM, anchor="mm")
    cells = [["R", "A", "C", "I"], ["C", "A", "R", "I"],
             ["I", "A", "R", "C"], ["R", "C", "I", "A"]]
    for i, row in enumerate(cells):
        txt(dr, (x0 - 160, y0 + 60 + i * rh), tasks[i], font(F_BOLD, 26), WHITE, anchor="lm")
        for j, r in enumerate(row):
            if t < 5 + (i * 4 + j) * 0.9:
                continue
            x, y = x0 + j * cw, y0 + 60 + i * rh
            hot = (r == "A")
            if hot:
                glow_box(dr, [x - 42, y - 34, x + 42, y + 34], YELLOW, rad=10, layers=2)
            dr.rectangle([x - 42, y - 34, x + 42, y + 34], fill=(12, 16, 34),
                         outline=YELLOW if hot else DIM, width=3)
            txt(dr, (x, y), r, font(F_BOLD, 32), YELLOW if hot else WHITE, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 590), "one A per task \u2014 accountability has a single name",
            font(F_BOLD, 30), YELLOW, anchor="mm")

def scene_timeline(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "The Delivery Timeline", BLUE)
    bars = [("API contract", 0, 4, BLUE), ("auth service", 2, 7, CYAN),
            ("data pipeline", 3, 9, TEAL), ("load testing", 7, 11, YELLOW),
            ("launch", 10, 12, GREEN)]
    x0 = 200; pxw = 80
    for q in range(13):
        txt(dr, (x0 + q * pxw, 200), "W%d" % (q + 1), font(F_MONO, 20), DIM, anchor="mm")
    for i, (name, s, e, col) in enumerate(bars):
        if t < 5 + i * 2.2:
            continue
        y = 260 + i * 70
        x1 = x0 + s * pxw
        grow = clamp((t - (5 + i * 2.2)) / 2)
        x2 = lerp(x1, x0 + e * pxw, grow)
        dr.rectangle([x1, y, x2, y + 40], fill=col)
        txt(dr, (x0 - 20, y + 20), name, font(F_BOLD, 24), WHITE, anchor="rm")
        if i == 3 and t > 16:
            # slip: load testing extends
            sx = x0 + e * pxw
            dr.rectangle([sx, y, sx + 1.5 * pxw * clamp((t - 16) / 3), y + 40], fill=RED)
            txt(dr, (sx + 130, y + 20), "slips +2w", font(F_BOLD, 24), RED, anchor="lm")
    if t > 22:
        txt(dr, (W // 2, 640), "replan in the open \u2014 dates move, trust must not",
            font(F_BOLD, 30), WHITE, anchor="mm")

# ============================================================ IL-19: MultiCloud DevOps & AI Bootcamp
def scene_multicloud(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Multi-Cloud: No Single Point of Failure", BLUE)
    clouds = [("AWS", ORANGE, 300), ("AZURE", CYAN, 640), ("GCP", RED, 980)]
    for name, col, x in clouds:
        idx = clouds.index((name, col, x))
        on = t >= 5 + idx * 2.5
        glow_box(dr, [x - 150, 180, x + 150, 420], col if on else (60, 60, 90), rad=16)
        dr.rectangle([x - 150, 180, x + 150, 420], fill=(12, 16, 34))
        txt(dr, (x, 270), name, font(F_BOLD, 36), col if on else DIM, anchor="mm")
        subs = ["us-east-1", "compute \u00b7 db", "active"]
        for s_i, s in enumerate(subs):
            txt(dr, (x, 330 + s_i * 34), s, font(F_SANS, 22), DIM, anchor="mm")
    # hub
    glow_box(dr, [W // 2 - 170, 480, W // 2 + 170, 600], GREEN, rad=14)
    dr.rectangle([W // 2 - 170, 480, W // 2 + 170, 600], fill=(10, 34, 22))
    txt(dr, (W // 2, 528), "CONTROL PLANE", font(F_BOLD, 30), GREEN, anchor="mm")
    txt(dr, (W // 2, 568), "terraform \u00b7 one state", font(F_SANS, 22), DIM, anchor="mm")
    if t > 13:
        for _, _, x in clouds:
            arrow(dr, x, 425, W // 2, 478, DIM, 4)
    if t > 20:
        txt(dr, (W // 2, 640), "portability is architecture \u2014 not an accident",
            font(F_BOLD, 30), WHITE, anchor="mm")

def scene_gitops(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "GitOps: Git Is the Source of Truth", BLUE)
    nodes = [("GIT", MAGENTA, 220), ("CI", CYAN, 480), ("REGISTRY", YELLOW, 740),
             ("OPERATOR", GREEN, 1000)]
    for name, col, x in nodes:
        idx = nodes.index((name, col, x))
        on = t >= 5 + idx * 2.5
        glow_box(dr, [x - 100, 200, x + 100, 330], col if on else (60, 60, 90), rad=12)
        dr.rectangle([x - 100, 200, x + 100, 330], fill=(12, 16, 34))
        txt(dr, (x, 255), name, font(F_BOLD, 26), col if on else DIM, anchor="mm")
        if idx < 3:
            arrow(dr, x + 105, 265, nodes[idx + 1][2] - 105, 265, DIM, 5)
    # commit dot traveling the loop
    if t > 7:
        legs = [(220, 480), (480, 740), (740, 1000), (1000, 640), (640, 220)]
        # simplified: ping-pong along x
        ph = ((t - 7) * 0.55) % 2.0
        if ph > 1:
            ph = 2 - ph
        px = lerp(220, 1000, ph)
        dr.ellipse([px - 12, 380 - 12, px + 12, 380 + 12], fill=WHITE)
        dr.ellipse([px - 7, 380 - 7, px + 7, 380 + 7], fill=MAGENTA)
    if t > 16:
        # drift correction
        txt(dr, (W // 2, 450), "drift detected \u2192 operator reconciles \u2192 cluster matches git",
            font(F_BOLD, 28), GREEN, anchor="mm")
        dr.line([480, 500, 780, 500], fill=RED, width=4)
        dr.line([780, 500, 780, 560], fill=RED, width=4)
        txt(dr, (630, 530), "manual change", font(F_SANS, 24), RED, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), "if it is not in git, it does not exist",
            font(F_BOLD, 30), MAGENTA, anchor="mm")

def scene_tfmod(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "Terraform Modules: compose, don\u2019t copy", font(F_BOLD, 38), WHITE, anchor="mm")
    lines = [('module "vpc" {', (200, 200, 255)),
             ('  source = "./modules/vpc"', (0, 229, 255)),
             ("  cidr   = var.cidr", (255, 214, 0)),
             ("}", (200, 200, 255)),
             ('module "eks" {', (200, 200, 255)),
             ('  source = "./modules/eks"', (0, 229, 255)),
             ("  vpc_id = module.vpc.id", (255, 214, 0)),
             ("}", (200, 200, 255))]
    code_panel(dr, 60, 140, 580, 620, "main.tf", lines,
               hi_line=min(7, int((t - 4) / 2.6)), t=t)
    mods = [("vpc", CYAN, 700), ("eks", MAGENTA, 900), ("rds", YELLOW, 1100)]
    for name, col, x in mods:
        idx = mods.index((name, col, x))
        on = t >= 7 + idx * 2.5
        glow_box(dr, [x - 85, 220, x + 85, 340], col if on else (60, 60, 100), rad=12)
        dr.rectangle([x - 85, 220, x + 85, 340], fill=(12, 12, 26))
        txt(dr, (x, 270), name, font(F_BOLD, 28), col if on else DIM, anchor="mm")
    if t > 8:
        arrow(dr, 700, 340, 900, 340, DIM, 4)
        arrow(dr, 700, 340, 1100, 280, DIM, 4)
    if t > 20:
        txt(dr, (900, 450), "one module \u2192 every environment",
            font(F_BOLD, 30), WHITE, anchor="mm")
        txt(dr, (900, 500), "dev, staging, prod from the same source",
            font(F_SANS, 24), DIM, anchor="mm")

# ============================================================ IL-20: Mathematics (3b1b x3)
def scene_limits(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "The Derivative: secants become tangents", font(F_BOLD, 40), WHITE, anchor="mm")
    ox, oy, sc = 640, 480, 130
    def f(x):
        return 0.35 * x * x
    seq = [(ox + x * sc / 2.4, oy - f(x) * sc / 2.4) for x in [i * 0.1 for i in range(-24, 25)]]
    dr.line(seq, fill=TEAL, width=5)
    txt(dr, (W // 2, 130), "f(x) = 0.35x\u00b2", font(F_MONO, 28), DIM, anchor="mm")
    k = clamp((t - 5) / 14)
    h = lerp(1.6, 0.08, ease(k))
    x0v = 0.6
    p0 = (ox + x0v * sc / 2.4, oy - f(x0v) * sc / 2.4)
    p1 = (ox + (x0v + h) * sc / 2.4, oy - f(x0v + h) * sc / 2.4)
    dr.line([ox - 420, oy - (f(x0v) + (f(x0v + h) - f(x0v)) / h * (x0v - 3)) * sc / 2.4,
             ox + 420, oy - (f(x0v) + (f(x0v + h) - f(x0v)) / h * (x0v + 3)) * sc / 2.4],
            fill=YELLOW, width=4)
    for p in (p0, p1):
        dr.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=YELLOW)
    txt(dr, (W // 2, 620), "slope = \u0394y/\u0394x \u2014 let \u0394x \u2192 0",
        font(F_BOLD, 30), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 665), "the secant melts into the tangent: f\u2032(x) = 0.7x",
            font(F_BOLD, 28), GREEN, anchor="mm")

def scene_eigen(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "Eigenvectors: directions the matrix spares", font(F_BOLD, 40), WHITE, anchor="mm")
    cx, cy, S = W // 2, 400, 90
    k = ease(clamp((t - 5) / 14))
    # transform: scale x by 2, y by 0.5
    def T(px, py):
        return (cx + (px - cx) * lerp(1, 2, k), cy + (py - cy) * lerp(1, 0.5, k))
    for gx in range(-4, 5):
        for gy in range(-3, 4):
            p = T(cx + gx * S, cy + gy * S)
            dr.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(70, 80, 120))
    # eigenvector along x-axis: stays on x-axis, stretched
    a = T(cx - 3 * S, cy); b = T(cx + 3 * S, cy)
    dr.line([a[0], a[1], b[0], b[1]], fill=YELLOW, width=6)
    txt(dr, (b[0] + 30, b[1]), "v", font(F_BOLD, 32), YELLOW, anchor="lm")
    # eigenvector along y-axis: stays on y-axis, squashed
    c = T(cx, cy - 2.4 * S); d = T(cx, cy + 2.4 * S)
    dr.line([c[0], c[1], d[0], d[1]], fill=MAGENTA, width=6)
    txt(dr, (d[0], d[1] + 36), "w", font(F_BOLD, 32), MAGENTA, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 620), "Av = 2v \u2014 stretched, never rotated",
            font(F_BOLD, 30), YELLOW, anchor="mm")
        txt(dr, (W // 2, 662), "Aw = 0.5w \u2014 squashed, never rotated",
            font(F_BOLD, 30), MAGENTA, anchor="mm")

def scene_taylor(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "Taylor Series: polynomials that learn curves", font(F_BOLD, 40), WHITE, anchor="mm")
    ox, oy, sc = 640, 400, 110
    terms = [0, 1, 3, 5, 7, 9]
    k = clamp((t - 5) / 14)
    nshow = min(len(terms), int(k * len(terms)) + (1 if k > 0 else 0))
    # target sin
    tgt = [(ox + x * sc / 3.4, oy - math.sin(x) * sc / 1.6) for x in [i * 0.08 for i in range(-40, 41)]]
    dr.line(tgt, fill=DIM, width=3)
    txt(dr, (ox + 400, oy - 120), "sin(x)", font(F_MONO, 26), DIM, anchor="lm")
    cols = [RED, ORANGE, YELLOW, GREEN, CYAN, MAGENTA]
    for i in range(nshow):
        n = terms[i]
        pts2 = []
        for xi in [j * 0.08 for j in range(-40, 41)]:
            s = 0.0
            for m in range(0, n + 1, 2):
                s += ((-1) ** (m // 2)) * (xi ** (m + 1)) / math.factorial(m + 1)
            pts2.append((ox + xi * sc / 3.4, oy - s * sc / 1.6))
        dr.line(pts2, fill=cols[i], width=4)
    txt(dr, (W // 2, 620), "add odd powers \u2014 the fit tightens toward sin(x)",
        font(F_BOLD, 30), WHITE, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 662), "infinite terms, exact curve \u2014 calculus as compression",
            font(F_BOLD, 28), YELLOW, anchor="mm")

# ============================================================ IL-21: Humanities (story x3)
def scene_socrates(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)
    txt(dr, (W // 2, 80), "THE AGORA, ATHENS \u2014 399 BC", font(F_SERIFB, 38), GOLD, anchor="mm")
    beats = [("what is justice?", "socrates asks", 5),
             ("the student answers", "with confidence", 10),
             ("the question turns", "the answer breaks", 15),
             ("aporia \u2014 not knowing", "the beginning of wisdom", 20)]
    for i, (q, sub, born) in enumerate(beats):
        if t < born:
            continue
        y = 220 + i * 100
        dr.ellipse([200 - 12, y - 12, 200 + 12, y + 12], fill=GOLD)
        txt(dr, (250, y - 14), q, font(F_SERIFB, 32), CREAM, anchor="lm")
        txt(dr, (250, y + 22), sub, font(F_SERIF, 24), (200, 185, 160), anchor="lm")
    if t > 25:
        txt(dr, (W // 2, 640), "\u201cthe unexamined life is not worth living\u201d",
            font(F_SERIF, 30), GOLD, anchor="mm")

def scene_cave(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    txt(dr, (W // 2, 80), "THE ALLEGORY OF THE CAVE", font(F_SERIFB, 38), GOLD, anchor="mm")
    # cave wall
    dr.rectangle([120, 180, 1160, 560], fill=(18, 12, 8), outline=(90, 70, 40), width=4)
    # fire glow behind
    k = 0.5 + 0.5 * math.sin(t * 3)
    glow = (int(120 + 40 * k), int(70 + 20 * k), 20)
    dr.ellipse([500, 420, 780, 560], fill=glow)
    # shadows on wall
    if t > 6:
        for i, (nm, xoff) in enumerate([("tree", 300), ("horse", 640), ("man", 940)]):
            if t < 6 + i * 3:
                continue
            x = 300 + i * 300
            sway = int(14 * math.sin(t * 2 + i))
            dr.ellipse([x - 60 + sway, 260, x + 60 + sway, 420], fill=(5, 3, 2))
            txt(dr, (x + sway, 470), nm, font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    if t > 18:
        # the escapee turns toward the light
        txt(dr, (W // 2, 600), "one prisoner turns \u2014 the shadows were never the world",
            font(F_SERIF, 30), GOLD, anchor="mm")
    if t > 24:
        txt(dr, (W // 2, 650), "philosophy: leaving the cave, and returning to free the rest",
            font(F_SERIF, 26), (200, 185, 160), anchor="mm")

def scene_turing(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)
    txt(dr, (W // 2, 80), "BLETCHLEY PARK \u2014 1950", font(F_SERIFB, 38), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "\u201cComputing Machinery and Intelligence\u201d", font(F_SERIF, 28),
        (200, 185, 160), anchor="mm")
    beats = [("a judge, two rooms", "one human, one machine", 5),
             ("typed questions", "typed answers", 11),
             ("the judge cannot tell", "which is which", 17),
             ("the imitation game", "can machines think?", 23)]
    for i, (q, sub, born) in enumerate(beats):
        if t < born:
            continue
        y = 230 + i * 95
        dr.ellipse([240 - 12, y - 12, 240 + 12, y + 12], fill=GOLD)
        txt(dr, (290, y - 14), q, font(F_SERIFB, 30), CREAM, anchor="lm")
        txt(dr, (290, y + 20), sub, font(F_SERIF, 24), (200, 185, 160), anchor="lm")
    if t > 26:
        txt(dr, (W // 2, 640), "the question outlived the machine \u2014 it is still being asked",
            font(F_SERIF, 28), GOLD, anchor="mm")

# ============================================================ VIDEO CONFIG
VIDEOS = [
 # --- IL-15: Data Engineering & Analytics Interview Prep
 dict(file="bbg-lakehouse.mp4", style="bbg", scene=scene_lakehouse,
      kicker="IL-15 \u00b7 Data Engineering & Analytics Interview Prep", title="The Lakehouse",
      sub="Bronze \u2192 Silver \u2192 Gold", module=4,
      blurb="Raw data lands in bronze, gets cleaned into silver, and ships as business-ready gold \u2014 one copy of the truth, refined in stages.",
      captions=[(4,10,"Bronze: raw data lands, exactly as it arrived"),
                (10,16,"Silver: cleaned, validated, deduplicated"),
                (16,22,"Gold: business-ready, queried everywhere"),
                (22,26,"One truth \u2014 refined in stages, never copied")]),
 dict(file="bbg-stream-processing.mp4", style="bbg", scene=scene_stream,
      kicker="IL-15 \u00b7 Data Engineering & Analytics Interview Prep", title="Stream Processing",
      sub="Events never wait", module=5,
      blurb="Events flow from sources through a broker into a stream job: tumbling windows aggregate every five minutes while the sinks drink continuously.",
      captions=[(4,10,"Sources emit events \u2014 clicks, orders, sensor ticks"),
                (10,16,"The broker buffers them \u2014 durable and ordered"),
                (16,22,"The stream job windows, aggregates, filters in flight"),
                (22,26,"Batch asks what happened \u2014 streaming answers live")]),
 dict(file="fireship-window-functions.mp4", style="fireship", scene=scene_windowfn,
      kicker="IL-15 \u00b7 Data Engineering & Analytics Interview Prep", title="SQL Window Functions",
      sub="Rank within partitions", module=2,
      blurb="RANK() OVER (PARTITION BY dept ORDER BY salary DESC): every department gets its own leaderboard without collapsing a single row.",
      captions=[(4,10,"PARTITION BY splits the table into independent groups"),
                (10,16,"ORDER BY ranks inside each group"),
                (16,22,"RANK() assigns the leaderboard position"),
                (22,26,"Aggregation \u2014 without losing a single row")]),
 # --- IL-16: Machine Learning & AI Engineering
 dict(file="3b1b-backprop.mp4", style="3b1b", scene=scene_backprop,
      kicker="IL-16 \u00b7 Machine Learning & AI Engineering", title="Backpropagation",
      sub="Blame flows backwards", module=0,
      blurb="A forward pass predicts; then error sweeps backwards through the layers, and the chain rule hands every weight its exact share of the blame.",
      captions=[(4,10,"Forward pass: inputs become a prediction"),
                (10,16,"The loss measures how wrong it was"),
                (16,22,"Backward pass: blame flows in reverse"),
                (22,26,"Chain rule at scale \u2014 millions of gradients, one sweep")]),
 dict(file="3b1b-bias-variance.mp4", style="3b1b", scene=scene_biasvar,
      kicker="IL-16 \u00b7 Machine Learning & AI Engineering", title="Bias vs Variance",
      sub="The fitting dilemma", module=2,
      blurb="A straight line underfits, degree-4 nails the signal, degree-15 memorizes noise \u2014 validation error is U-shaped, so tune complexity, not just fit.",
      captions=[(4,10,"Degree 1: too simple \u2014 it misses the pattern"),
                (10,16,"Degree 4: just right \u2014 it captures the signal"),
                (16,22,"Degree 15: too complex \u2014 it memorizes noise"),
                (22,26,"Validation error is U-shaped \u2014 tune complexity")]),
 dict(file="fireship-ml-pipeline.mp4", style="fireship", scene=scene_mlpipeline,
      kicker="IL-16 \u00b7 Machine Learning & AI Engineering", title="The ML Pipeline",
      sub="Train \u2192 evaluate \u2192 ship", module=3,
      blurb="A scikit-learn pipeline trains, the metrics gate checks RMSE and drift, and the model shadow-deploys \u2014 a model is code plus data, version both.",
      captions=[(4,10,"The pipeline binds features and model together"),
                (10,16,"Train on one split, judge on another"),
                (16,22,"The metrics gate: RMSE, drift \u2014 pass or stop"),
                (22,26,"Models are code + data \u2014 version both")]),
 # --- IL-17: Agentic AI Engineering
 dict(file="fireship-agent-loop.mp4", style="fireship", scene=scene_agentloop,
      kicker="IL-17 \u00b7 Agentic AI Engineering", title="The ReAct Loop",
      sub="Think, act, observe", module=1,
      blurb="An agent is an LLM in a while-loop: think, parse a tool call, run it, observe, append to memory \u2014 with guardrails bounding every action.",
      captions=[(4,10,"Think: the LLM reasons about the goal"),
                (10,16,"Act: it calls a tool \u2014 search, code, API"),
                (16,22,"Observe: the result feeds back into memory"),
                (22,26,"Loop until the goal checks out \u2014 then stop")]),
 dict(file="bbg-agent-memory.mp4", style="bbg", scene=scene_agentmem,
      kicker="IL-17 \u00b7 Agentic AI Engineering", title="Agent Memory",
      sub="Short-term + long-term", module=2,
      blurb="The context window fills fast and must forget; vector memory persists across sessions \u2014 short-term reasons, long-term remembers, RAG bridges them.",
      captions=[(4,10,"The context window: fast, small, forgetful"),
                (10,16,"Vector memory: embeddings that persist"),
                (16,22,"Retrieval bridges them \u2014 recall on demand"),
                (22,26,"Short-term reasons \u2014 long-term remembers")]),
 dict(file="bbg-multi-agent.mp4", style="bbg", scene=scene_multiagent,
      kicker="IL-17 \u00b7 Agentic AI Engineering", title="Multi-Agent Systems",
      sub="Divide and conquer", module=3,
      blurb="An orchestrator plans and delegates to researcher, coder, reviewer, and deployer specialists working in parallel \u2014 then merges their results.",
      captions=[(4,10,"The orchestrator plans \u2014 then delegates"),
                (10,16,"Specialists work in parallel: research, code, review"),
                (16,22,"Results stream back for merging"),
                (22,26,"Divide and conquer \u2014 at machine speed")]),
 # --- IL-18: Technical Leadership Interview Prep
 dict(file="story-tpm-war-room.mp4", style="story", scene=scene_warroom,
      kicker="IL-18 \u00b7 Technical Leadership Interview Prep", title="The War Room",
      sub="Leadership is calm made contagious", module=1,
      blurb="Launch night, 2:47 AM: the page fires, one voice commands, the team mitigates without blame \u2014 then runs a blameless retro at dawn.",
      captions=[(4,10,"The page fires at 2:47 AM"),
                (10,16,"One voice commands \u2014 the rest execute"),
                (16,22,"Mitigate first \u2014 root cause later"),
                (22,26,"Leadership is calm made contagious")]),
 dict(file="bbg-raci-program.mp4", style="bbg", scene=scene_raci,
      kicker="IL-18 \u00b7 Technical Leadership Interview Prep", title="RACI: Who Owns What",
      sub="Accountability has a single name", module=2,
      blurb="The RACI matrix maps every program task to who does it, who owns it, who is consulted, and who is informed \u2014 one A per task, always.",
      captions=[(4,10,"R: the hands that do the work"),
                (10,16,"A: the single owner of the outcome"),
                (16,22,"C and I: consulted early, informed always"),
                (22,26,"One A per task \u2014 accountability has a name")]),
 dict(file="bbg-delivery-timeline.mp4", style="bbg", scene=scene_timeline,
      kicker="IL-18 \u00b7 Technical Leadership Interview Prep", title="The Delivery Timeline",
      sub="Dates move \u2014 trust must not", module=7,
      blurb="Twelve weeks of delivery on a Gantt: load testing slips two weeks, the plan is replanned in the open, and trust survives the slip.",
      captions=[(4,10,"Twelve weeks, five workstreams, one launch"),
                (10,16,"Load testing slips \u2014 two weeks, no surprise"),
                (16,22,"Replan in the open: new dates, same trust"),
                (22,26,"Dates move \u2014 credibility must not")]),
 # --- IL-19: MultiCloud DevOps & AI Bootcamp
 dict(file="bbg-multi-cloud.mp4", style="bbg", scene=scene_multicloud,
      kicker="IL-19 \u00b7 MultiCloud DevOps & AI Bootcamp", title="Multi-Cloud Architecture",
      sub="No single point of failure", module=7,
      blurb="AWS, Azure, and GCP regions all answer to one control plane: a single Terraform state, portable workloads, and no vendor lock-in by accident.",
      captions=[(4,10,"Three clouds, three regions \u2014 all active"),
                (10,16,"One control plane rules them all"),
                (16,22,"Terraform: one state, every cloud"),
                (22,26,"Portability is architecture \u2014 not an accident")]),
 dict(file="bbg-gitops-pipeline.mp4", style="bbg", scene=scene_gitops,
      kicker="IL-19 \u00b7 MultiCloud DevOps & AI Bootcamp", title="GitOps",
      sub="Git is the source of truth", module=3,
      blurb="A commit flows through CI into the registry; the operator watches git and reconciles the cluster \u2014 manual drift gets reverted, not debated.",
      captions=[(4,10,"The commit is the deployment request"),
                (10,16,"CI builds \u2014 the registry stores"),
                (16,22,"The operator reconciles cluster to git"),
                (22,26,"If it is not in git, it does not exist")]),
 dict(file="fireship-terraform-modules.mp4", style="fireship", scene=scene_tfmod,
      kicker="IL-19 \u00b7 MultiCloud DevOps & AI Bootcamp", title="Terraform Modules",
      sub="Compose, don\u2019t copy", module=5,
      blurb="main.tf composes vpc, eks, and rds modules \u2014 dev, staging, and prod all instantiate the same source, so environments stop drifting apart.",
      captions=[(4,10,"A module: one reusable infrastructure unit"),
                (10,16,"Compose them: vpc feeds eks feeds rds"),
                (16,22,"Same source \u2014 every environment"),
                (22,26,"Compose, don\u2019t copy-paste")]),
 # --- IL-20: Mathematics for Engineers & Scientists
 dict(file="3b1b-limits-derivative.mp4", style="3b1b", scene=scene_limits,
      kicker="IL-20 \u00b7 Mathematics for Engineers & Scientists", title="The Derivative",
      sub="Secants become tangents", module=7,
      blurb="On f(x) = 0.35x^2, a secant line through two shrinking points melts into the tangent as delta-x approaches zero \u2014 that limit is the derivative.",
      captions=[(4,10,"The secant: slope between two points"),
                (10,16,"Pull the points together \u2014 \u0394x shrinks"),
                (16,22,"The limit: the secant becomes the tangent"),
                (22,26,"That limit is the derivative \u2014 f\u2032(x) = 0.7x")]),
 dict(file="3b1b-eigenvectors.mp4", style="3b1b", scene=scene_eigen,
      kicker="IL-20 \u00b7 Mathematics for Engineers & Scientists", title="Eigenvectors",
      sub="Directions the matrix spares", module=6,
      blurb="A grid stretches 2x in x and squashes 0.5x in y: the x-axis direction stretches but never rotates (Av = 2v), the y-axis squashes but never rotates.",
      captions=[(4,10,"The matrix stretches x, squashes y"),
                (10,16,"Most vectors rotate \u2014 these two don\u2019t"),
                (16,22,"v: stretched by 2, never rotated \u2014 Av = 2v"),
                (22,26,"w: squashed by half \u2014 Aw = 0.5w")]),
 dict(file="3b1b-taylor-series.mp4", style="3b1b", scene=scene_taylor,
      kicker="IL-20 \u00b7 Mathematics for Engineers & Scientists", title="Taylor Series",
      sub="Polynomials that learn curves", module=9,
      blurb="Odd-powered polynomials stack onto sin(x): each term tightens the fit near zero until the infinite series is the curve itself \u2014 calculus as compression.",
      captions=[(4,10,"Start with x \u2014 a line through the origin"),
                (10,16,"Add x\u00b3, x\u2075, x\u2077 \u2014 the fit tightens"),
                (16,22,"Each term hugs sin(x) a little further"),
                (22,26,"Infinite terms, exact curve \u2014 compression by calculus")]),
 # --- IL-21: Humanities for Technologists
 dict(file="story-socrates-dialogue.mp4", style="story", scene=scene_socrates,
      kicker="IL-21 \u00b7 Humanities for Technologists", title="The Socratic Dialogue",
      sub="The beginning of wisdom", module=0,
      blurb="In the Athenian agora, Socrates asks what justice is; the confident answer breaks under questioning \u2014 aporia, the not-knowing, is where philosophy starts.",
      captions=[(4,10,"Socrates asks: what is justice?"),
                (10,16,"The student answers \u2014 confidently"),
                (16,22,"The question turns \u2014 the answer breaks"),
                (22,26,"Aporia: not knowing is where wisdom begins")]),
 dict(file="story-allegory-cave.mp4", style="story", scene=scene_cave,
      kicker="IL-21 \u00b7 Humanities for Technologists", title="The Allegory of the Cave",
      sub="The shadows were never the world", module=4,
      blurb="Prisoners watch shadows flicker on a cave wall and call them reality \u2014 until one turns toward the fire, climbs out, and returns to free the rest.",
      captions=[(4,10,"Prisoners chained \u2014 shadows on the wall"),
                (10,16,"They name the shadows \u2014 and call it reality"),
                (16,22,"One turns toward the fire \u2014 the world is larger"),
                (22,26,"Philosophy: leave the cave, then return for the rest")]),
 dict(file="story-turing-test.mp4", style="story", scene=scene_turing,
      kicker="IL-21 \u00b7 Humanities for Technologists", title="The Turing Test",
      sub="Can machines think?", module=6,
      blurb="Bletchley Park, 1950: Turing proposes the imitation game \u2014 if a judge cannot tell human from machine by typed answers alone, the question changes.",
      captions=[(4,10,"1950: Turing asks \u2018can machines think?\u2019"),
                (10,16,"A judge, two rooms \u2014 typed questions only"),
                (16,22,"The judge cannot tell which is the machine"),
                (22,26,"The question outlived the machine \u2014 it is still asked")]),
]

COURSE_FILES = {
    15: "il-15-data-engineering-analytics-interview-prep.json",
    16: "il-16-machine-learning-ai-engineering.json",
    17: "il-17-agentic-ai-engineering.json",
    18: "il-18-technical-leadership-interview-prep.json",
    19: "il-19-multicloud-devops-ai-bootcamp.json",
    20: "il-20-mathematics.json",
    21: "il-21-humanities.json",
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
