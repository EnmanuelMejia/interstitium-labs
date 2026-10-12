#!/usr/bin/env python3
"""Batch 4 video generator: IL-22..IL-29, 24 videos x 30s, 1280x720 @ 24fps.
FINAL BATCH. Mirrors gen_batch3.py: silent h264 MP4s, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / 3b1b / fireship / bbg. Original animations only.

Course -> style map:
 IL-22 Esoteric & Secret Knowledge   : story x3
 IL-23 Frontier Knowledge            : story x3
 IL-24 ThreatLocker Assessment Prep  : bbg x2 + fireship
 IL-25 Cybersecurity Certificate     : bbg x2 + fireship
 IL-26 Data Analyst Senior Mastery   : 3b1b x2 + fireship
 IL-27 IT Infrastructure Specialist  : bbg x3
 IL-28 DevSecOps Cloud Infra         : bbg x2 + fireship
 IL-29 ThreatLocker AI Cyber Mastery : bbg x2 + fireship
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

# ============================================================ IL-22: Esoteric & Secret Knowledge (story x3)
def scene_kybalion(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)
    txt(dr, (W // 2, 80), "THE KYBALION", font(F_SERIFB, 42), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "seven principles of the hermetic philosophy", font(F_SERIF, 26),
        (200, 185, 160), anchor="mm")
    principles = [("I. Mentalism", "the all is mind", 5),
                  ("II. Correspondence", "as above, so below", 9),
                  ("III. Vibration", "nothing rests \u2014 everything moves", 13),
                  ("IV. Polarity", "opposites are the same in degree", 17),
                  ("V. Rhythm", "the pendulum swing manifests in all", 21)]
    for i, (p, sub, born) in enumerate(principles):
        if t < born:
            continue
        y = 200 + i * 82
        dr.ellipse([180 - 10, y - 10, 180 + 10, y + 10], fill=GOLD)
        txt(dr, (225, y - 12), p, font(F_SERIFB, 30), CREAM, anchor="lm")
        txt(dr, (225, y + 22), sub, font(F_SERIF, 24), (200, 185, 160), anchor="lm")
    if t > 24:
        txt(dr, (W // 2, 640), "master the principles \u2014 the rest is commentary",
            font(F_SERIF, 28), GOLD, anchor="mm")

def scene_golden_dawn(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)
    txt(dr, (W // 2, 80), "THE GOLDEN DAWN", font(F_SERIFB, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "a ladder of grades, climbed by ritual", font(F_SERIF, 26),
        (200, 185, 160), anchor="mm")
    grades = [("Neophyte", "the threshold", 5), ("Zelator", "earth", 9),
              ("Theoricus", "air", 13), ("Practicus", "water", 17),
              ("Philosophus", "fire", 21), ("Adeptus Minor", "the vault", 24)]
    for i, (g, sub, born) in enumerate(grades):
        if t < born:
            continue
        x = 160 + i * 190
        r = 62
        dr.ellipse([x - r, 340 - r, x + r, 340 + r], outline=GOLD, width=4)
        dr.ellipse([x - r + 10, 340 - r + 10, x + r - 10, 340 + r - 10],
                   outline=(90, 70, 40), width=2)
        txt(dr, (x, 340 - 16), g, font(F_SERIFB, 22), CREAM, anchor="mm")
        txt(dr, (x, 340 + 24), sub, font(F_SERIF, 20), (200, 185, 160), anchor="mm")
        if i > 0:
            arrow(dr, 160 + (i - 1) * 190 + 66, 340, x - 66, 340, DIM, 3)
    if t > 26:
        txt(dr, (W // 2, 560), "ten sephiroth, one tree \u2014 ascent by correspondence",
            font(F_SERIF, 26), GOLD, anchor="mm")

def scene_fools(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    txt(dr, (W // 2, 80), "THE FOOL'S JOURNEY", font(F_SERIFB, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "twenty-two arcana, one soul's itinerary", font(F_SERIF, 26),
        (200, 185, 160), anchor="mm")
    cards = [("0", "THE FOOL", "innocence steps off the cliff", 5),
             ("I", "THE MAGICIAN", "will, focused like a lens", 11),
             ("X", "THE WHEEL", "fortune turns \u2014 rise and fall", 17),
             ("XXI", "THE WORLD", "the dance completes the circle", 23)]
    for i, (num, nm, sub, born) in enumerate(cards):
        if t < born:
            continue
        x = 200 + i * 293
        glow_box(dr, [x - 110, 200, x + 110, 480], GOLD, rad=10, layers=2)
        dr.rectangle([x - 110, 200, x + 110, 480], fill=(22, 16, 10))
        txt(dr, (x, 260), num, font(F_SERIFB, 36), GOLD, anchor="mm")
        txt(dr, (x, 330), nm, font(F_SERIFB, 26), CREAM, anchor="mm")
        txt(dr, (x, 400), sub, font(F_SERIF, 21), (200, 185, 160), anchor="mm")
        if i > 0:
            arrow(dr, 200 + (i - 1) * 293 + 115, 340, x - 115, 340, DIM, 3)
    if t > 26:
        txt(dr, (W // 2, 580), "every life is the journey \u2014 the cards just name the stations",
            font(F_SERIF, 26), GOLD, anchor="mm")

# ============================================================ IL-23: Frontier Knowledge (story x3)
def scene_frontier_attention(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)
    txt(dr, (W // 2, 80), "ATTENTION IS ALL YOU NEED", font(F_SERIFB, 36), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "the transformer, distilled", font(F_SERIF, 26),
        (200, 185, 160), anchor="mm")
    tokens = ["the", "cat", "sat", "because", "tired"]
    tx = [300, 470, 640, 810, 980]
    for i, (tok, x) in enumerate(zip(tokens, tx)):
        if t < 5 + i * 1.5:
            continue
        dr.ellipse([x - 46, 300 - 46, x + 46, 300 + 46], fill=(22, 16, 10),
                   outline=GOLD, width=3)
        txt(dr, (x, 300), tok, font(F_SERIFB, 26), CREAM, anchor="mm")
    # attention arcs into "sat"
    if t > 13:
        for i, x in enumerate(tx):
            if i == 2:
                continue
            w = [0.9, 0.6, 0.0, 0.4, 0.75][i]
            col = (int(lerp(60, 255, w)), int(lerp(60, 190, w)), 40)
            x1, x2 = (x, 640) if x < 640 else (640, x)
            dr.arc([x1, 160, x2, 470], 200, 340, fill=col, width=int(2 + 6 * w))
            txt(dr, ((x1 + x2) / 2, 478), "%.2f" % w, font(F_MONO, 20), col, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 560), "every word weighs every other word \u2014 meaning emerges from the weights",
            font(F_SERIF, 28), CREAM, anchor="mm")

def scene_qubit(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    txt(dr, (W // 2, 80), "THE QUBIT", font(F_SERIFB, 42), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "both at once, until you ask", font(F_SERIF, 26),
        (200, 185, 160), anchor="mm")
    cx, cy, R = 480, 400, 200
    dr.ellipse([cx - R, cy - R, cx + R, cy + R], outline=GOLD, width=4)
    dr.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)
    txt(dr, (cx, cy - R - 30), "|0\u27e9", font(F_SERIFB, 30), CREAM, anchor="mm")
    txt(dr, (cx, cy + R + 30), "|1\u27e9", font(F_SERIFB, 30), CREAM, anchor="mm")
    k = clamp((t - 5) / 16)
    ang = lerp(0.2, 1.35, ease(k))
    px, py = cx + R * math.sin(ang), cy - R * math.cos(ang)
    dr.line([cx, cy, px, py], fill=YELLOW, width=6)
    dr.ellipse([px - 12, py - 12, px + 12, py + 12], fill=YELLOW)
    p0 = round(100 * math.cos(ang / 2) ** 2); p1 = 100 - p0
    txt(dr, (800, 330), "P(|0\u27e9) = %d%%" % p0, font(F_SERIFB, 32), CREAM, anchor="lm")
    txt(dr, (800, 390), "P(|1\u27e9) = %d%%" % p1, font(F_SERIFB, 32), CREAM, anchor="lm")
    txt(dr, (800, 470), "\u03b1|0\u27e9 + \u03b2|1\u27e9", font(F_SERIF, 30), (200, 185, 160), anchor="lm")
    if t > 23:
        txt(dr, (W // 2, 640), "measurement collapses the maybe \u2014 the act of asking decides",
            font(F_SERIF, 28), GOLD, anchor="mm")

def scene_fusion(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    txt(dr, (W // 2, 80), "FUSION: A STAR ON EARTH", font(F_SERIFB, 38), GOLD, anchor="mm")
    txt(dr, (W // 2, 130), "heat, squeeze, ignite", font(F_SERIF, 26),
        (200, 185, 160), anchor="mm")
    cx, cy, R = W // 2, 380, 150
    k = clamp((t - 5) / 15)
    glow_r = int(lerp(10, 90, k))
    for r2 in range(glow_r, 0, -12):
        a = int(lerp(30, 220, r2 / max(glow_r, 1)))
        dr.ellipse([cx - R - r2, cy - r2 // 2 - 40, cx + R + r2, cy + r2 // 2 + 40],
                   outline=(a, int(a * 0.55), 20), width=3)
    dr.ellipse([cx - R, cy - 60, cx + R, cy + 60], outline=ORANGE, width=8)
    # ions spiraling
    for i in range(14):
        a2 = t * 2.2 + i * math.pi / 7
        rr = lerp(120, 20, k) + 20 * math.sin(t * 3 + i)
        px, py = cx + (R + rr) * math.cos(a2) * 0.9, cy + rr * math.sin(a2) * 0.45
        dr.ellipse([px - 6, py - 6, px + 6, py + 6], fill=YELLOW)
    temp = int(lerp(10, 150, ease(k)))
    txt(dr, (W // 2, 560), "%d million \u00b0C" % temp, font(F_SERIFB, 40), ORANGE, anchor="mm")
    if t > 21:
        flash = int(120 + 100 * math.sin(t * 12))
        dr.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(flash, flash // 2, 10))
        txt(dr, (W // 2, 620), "IGNITION \u2014 the plasma heats itself",
            font(F_SERIFB, 34), YELLOW, anchor="mm")
    if t > 25:
        txt(dr, (W // 2, 670), "ten times the core of the sun \u2014 inside a magnetic bottle",
            font(F_SERIF, 24), (200, 185, 160), anchor="mm")
# ============================================================ IL-24: ThreatLocker Assessment Prep (bbg x2 + fireship)
def scene_triage(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "The Cyber Hero Triage Loop", BLUE)
    stages = [("ALERT", RED), ("ENRICH", YELLOW), ("DECIDE", CYAN), ("ACT", GREEN)]
    n = len(stages); bw = 220; gap = 40
    total = n * bw + (n - 1) * gap; x0 = (W - total) // 2
    for i, (name, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        on = t >= 4 + i * 2.5
        glow_box(dr, [x, 200, x + bw, 380], col if on else (60, 60, 90), rad=14)
        dr.rectangle([x, 200, x + bw, 380], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 260), name, font(F_BOLD, 30), col if on else DIM, anchor="mm")
        subs = ["fires in the portal", "hash \u00b7 signer \u00b7 behavior",
                "approve / deny / ringfence", "policy + note it"]
        txt(dr, (x + bw // 2, 320), subs[i], font(F_SANS, 21), DIM, anchor="mm")
        if i < n - 1:
            arrow(dr, x + bw + 4, 290, x + bw + gap - 4, 290, DIM, 5)
    if t > 16:
        arrow(dr, x0 + total - 40, 430, x0 + 40, 430, GREEN, 5)
        txt(dr, (W // 2, 470), "every decision feeds the next alert \u2014 the loop learns",
            font(F_BOLD, 26), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 540), "speed with judgment: triage in minutes, explain in seconds",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_defaultdeny(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Default-Deny: From Learning Mode to Least Privilege", BLUE)
    phases = [("LEARNING MODE", "observe everything", YELLOW),
              ("BASELINE", "known-good inventory", CYAN),
              ("ENFORCE", "deny the unknown", RED)]
    for i, (name, sub, col) in enumerate(phases):
        on = t >= 5 + i * 5
        y = 220 + i * 120
        glow_box(dr, [180, y - 45, 1100, y + 45], col if on else (60, 60, 90), rad=12)
        dr.rectangle([180, y - 45, 1100, y + 45], fill=(12, 16, 34))
        txt(dr, (280, y - 10), name, font(F_BOLD, 30), col if on else DIM, anchor="lm")
        txt(dr, (280, y + 24), sub, font(F_SANS, 22), DIM, anchor="lm")
        if on:
            k = clamp((t - (5 + i * 5)) / 3)
            for b in range(8):
                bx = 700 + b * 45
                dr.rectangle([bx, y - 14, bx + 30, y + 14],
                             fill=col if b / 8 < k else (40, 40, 60))
    if t > 22:
        txt(dr, (W // 2, 600), "default-deny: nothing runs unless the policy says so",
            font(F_BOLD, 30), RED, anchor="mm")

def scene_ringfence_fs(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "Ringfencing: Approve, Deny, Contain", font(F_BOLD, 38), WHITE, anchor="mm")
    lines = [("policy = {", (200, 200, 255)),
             ('  "app": "browser.exe",', (0, 229, 255)),
             ('  "action": "ringfence",', (255, 214, 0)),
             ('  "allow": ["corp-vpn"],', (255, 214, 0)),
             ('  "deny":  ["local-files", "camera"],', (255, 120, 120)),
             ("}", (200, 200, 255))]
    code_panel(dr, 60, 140, 560, 590, "ringfence.json", lines,
               hi_line=min(5, int((t - 4) / 3.2)), t=t)
    # app in a box, arrows filtered
    dr.rectangle([700, 220, 1180, 520], fill=(12, 12, 26), outline=MAGENTA, width=4)
    txt(dr, (940, 280), "browser.exe", font(F_BOLD, 32), WHITE, anchor="mm")
    txt(dr, (940, 330), "runs \u2014 but caged", font(F_SANS, 24), DIM, anchor="mm")
    flows = [("corp-vpn", GREEN, True), ("local-files", RED, False), ("camera", RED, False)]
    for i, (nm, col, ok) in enumerate(flows):
        if t < 8 + i * 2.5:
            continue
        y = 400 + i * 44
        dr.line([1185, y, 1260, y], fill=col if ok else RED, width=5)
        if not ok:
            dr.line([1240, y - 14, 1270, y + 14], fill=RED, width=5)
            dr.line([1270, y - 14, 1240, y + 14], fill=RED, width=5)
        txt(dr, (940, y), nm, font(F_MONO, 24), col if ok else DIM, anchor="mm")
    if t > 20:
        txt(dr, (940, 480), "contain, don\u2019t just block", font(F_BOLD, 28), MAGENTA, anchor="mm")
    if t > 24:
        txt(dr, (W // 2, 640), "the app works \u2014 the blast radius does not",
            font(F_BOLD, 28), WHITE, anchor="mm")

# ============================================================ IL-25: Cybersecurity Certificate (bbg x2 + fireship)
def scene_threatvuln(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Threats Meet Vulnerabilities: The Kill Chain", BLUE)
    chain = [("THREAT ACTOR", RED, "motive + capability"),
             ("VULNERABILITY", ORANGE, "an unpatched door"),
             ("EXPLOIT", YELLOW, "the key that fits"),
             ("IMPACT", MAGENTA, "breach, ransom, leak")]
    n = len(chain); bw = 240; gap = 36
    total = n * bw + (n - 1) * gap; x0 = (W - total) // 2
    for i, (name, col, sub) in enumerate(chain):
        x = x0 + i * (bw + gap)
        on = t >= 4 + i * 3
        glow_box(dr, [x, 220, x + bw, 420], col if on else (60, 60, 90), rad=14)
        dr.rectangle([x, 220, x + bw, 420], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 290), name, font(F_BOLD, 24), col if on else DIM, anchor="mm")
        txt(dr, (x + bw // 2, 350), sub, font(F_SANS, 20), DIM, anchor="mm")
        if i < n - 1:
            arrow(dr, x + bw + 4, 320, x + bw + gap - 4, 320, DIM, 5)
    if t > 18:
        txt(dr, (W // 2, 480), "remove ANY link \u2014 the chain breaks",
            font(F_BOLD, 32), GREEN, anchor="mm")
        for i in range(n):
            x = x0 + i * (bw + gap) + bw // 2
            dr.line([x - 50, 540, x + 50, 540], fill=GREEN, width=6)
            dr.line([x, 515, x, 565], fill=GREEN, width=6)
    if t > 24:
        txt(dr, (W // 2, 600), "defense in depth: break the chain everywhere you can",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_iam(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "IAM: Identity Is the New Perimeter", BLUE)
    layers = [("AUTHENTICATE", "prove who you are \u2014 MFA", CYAN),
              ("AUTHORIZE", "least privilege \u2014 RBAC", TEAL),
              ("ACCOUNT", "lifecycle \u2014 joiner/mover/leaver", YELLOW),
              ("AUDIT", "log everything \u2014 prove it", MAGENTA)]
    for i, (name, sub, col) in enumerate(layers):
        on = t >= 5 + i * 3.5
        y = 220 + i * 100
        glow_box(dr, [220, y - 38, 1060, y + 38], col if on else (60, 60, 90), rad=12)
        dr.rectangle([220, y - 38, 1060, y + 38], fill=(12, 16, 34))
        txt(dr, (300, y - 8), name, font(F_BOLD, 30), col if on else DIM, anchor="lm")
        txt(dr, (300, y + 24), sub, font(F_SANS, 22), DIM, anchor="lm")
        if on:
            dr.ellipse([990 - 20, y - 20, 990 + 20, y + 20], fill=col)
            txt(dr, (990, y), "\u2713", font(F_BOLD, 28), (10, 10, 20), anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 640), "no identity, no access \u2014 the perimeter moved to the person",
            font(F_BOLD, 30), WHITE, anchor="mm")

def scene_soc_fs(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "The SOC Pipeline: Detect \u2192 Respond", font(F_BOLD, 38), WHITE, anchor="mm")
    lines = [("index=edr earliest=-1h", (200, 200, 255)),
             ("| stats count by process", (0, 229, 255)),
             ("| where count > baseline * 3", (255, 214, 0)),
             ("| alert severity=high", (255, 120, 120))]
    code_panel(dr, 60, 140, 580, 520, "hunt.spl", lines,
               hi_line=min(3, int((t - 4) / 4)), t=t)
    stages = [("DETECT", RED, 700), ("TRIAGE", YELLOW, 880), ("RESPOND", GREEN, 1060)]
    for name, col, x in stages:
        idx = stages.index((name, col, x))
        on = t >= 7 + idx * 3.5
        glow_box(dr, [x - 80, 220, x + 80, 340], col if on else (60, 60, 100), rad=12)
        dr.rectangle([x - 80, 220, x + 80, 340], fill=(12, 12, 26))
        txt(dr, (x, 270), name, font(F_BOLD, 26), col if on else DIM, anchor="mm")
        if idx < 2:
            arrow(dr, x + 85, 280, stages[idx + 1][2] - 85, 280, DIM, 4)
    if t > 18:
        panel(dr, [640, 420, 1200, 540], "MTTR: 42 MIN \u2192 11 MIN", GREEN, 26)
        txt(dr, (920, 480), "playbooks turn panic into procedure",
            font(F_BOLD, 26), GREEN, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), "hunt, don\u2019t wait \u2014 the alert is the starting gun",
            font(F_BOLD, 28), WHITE, anchor="mm")
# ============================================================ IL-26: Data Analyst Senior Mastery (3b1b x2 + fireship)
def scene_normal(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "The Normal Distribution", font(F_BOLD, 42), WHITE, anchor="mm")
    ox, oy, sc = 640, 500, 200
    k = ease(clamp((t - 5) / 12))
    pts2 = [(ox + x * sc, oy - 260 * math.exp(-x * x / 2)) for x in
            [i * 0.02 for i in range(int(-320 * k), int(320 * k) + 1)]]
    if len(pts2) > 1:
        dr.line(pts2, fill=TEAL, width=5)
    # sigma bands
    for s_i, (lab, col) in enumerate([("68%", CYAN), ("95%", YELLOW), ("99.7%", MAGENTA)]):
        if t < 10 + s_i * 3.5:
            continue
        s = s_i + 1
        dr.line([ox - s * sc, oy, ox + s * sc, oy], fill=col, width=3)
        txt(dr, (ox + s * sc + 20, oy - 40), lab, font(F_BOLD, 26), col, anchor="lm")
        txt(dr, (ox - s * sc - 20, oy - 40), "\u00b1%d\u03c3" % s, font(F_MONO, 24), col, anchor="rm")
    if t > 22:
        txt(dr, (W // 2, 620), "the bell curve: averages cluster, extremes are rare",
            font(F_BOLD, 30), WHITE, anchor="mm")
    if t > 25:
        txt(dr, (W // 2, 662), "central limit theorem: sample means go normal \u2014 always",
            font(F_BOLD, 26), YELLOW, anchor="mm")

def scene_pvalue(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    txt(dr, (W // 2, 70), "The P-Value: How Surprised Should You Be?", font(F_BOLD, 38),
        WHITE, anchor="mm")
    ox, oy, sc = 640, 480, 190
    null_pts = [(ox + x * sc, oy - 240 * math.exp(-x * x / 2))
                for x in [i * 0.02 for i in range(-160, 161)]]
    dr.line(null_pts, fill=TEAL, width=5)
    txt(dr, (ox, oy + 44), "null hypothesis: nothing is happening", font(F_SANS, 24), DIM, anchor="mm")
    k = clamp((t - 5) / 12)
    z = lerp(0.4, 2.6, ease(k))
    zx = ox + z * sc
    dr.line([zx, oy, zx, oy - 240 * math.exp(-z * z / 2)], fill=RED, width=5)
    txt(dr, (zx, oy - 260), "z = %.1f" % z, font(F_BOLD, 28), RED, anchor="mm")
    if t > 14:
        shade = [(ox + x * sc, oy - 240 * math.exp(-x * x / 2))
                 for x in [i * 0.02 for i in range(int(z * 50), 161)]]
        if len(shade) > 1:
            dr.polygon(shade + [(ox + 3.2 * sc, oy), (zx, oy)], fill=(200, 60, 60))
        p = max(0.004, 1 - 0.5 * (1 + math.erf(z / math.sqrt(2))))
        txt(dr, (ox + 2.4 * sc, oy - 120), "p = %.3f" % p, font(F_BOLD, 30), RED, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 620), "p < 0.05: the data would be weird if nothing were happening",
            font(F_BOLD, 28), WHITE, anchor="mm")
    if t > 25:
        txt(dr, (W // 2, 662), "reject the null \u2014 but never prove the alternative",
            font(F_BOLD, 26), YELLOW, anchor="mm")

def scene_pandas_fs(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "pandas groupby: Split \u2014 Apply \u2014 Combine", font(F_BOLD, 36),
        WHITE, anchor="mm")
    lines = [("import pandas as pd", (200, 200, 255)),
             ("df = pd.read_csv('sales.csv')", (200, 200, 255)),
             ("df.groupby('region')['revenue']", (0, 229, 255)),
             ("  .agg(['sum', 'mean'])", (0, 229, 255)),
             ("  .sort_values('sum', ascending=False)", (255, 214, 0))]
    code_panel(dr, 60, 140, 580, 560, "analyze.py", lines,
               hi_line=min(4, int((t - 4) / 3.6)), t=t)
    rows = [("west", 412, 68.7), ("east", 388, 64.7), ("north", 301, 50.2)]
    x0, y0 = 660, 220
    for j, h in enumerate(["region", "sum $k", "mean $k"]):
        txt(dr, (x0 + j * 160, y0), h, font(F_MONOB, 24), CYAN, anchor="mm")
    for i, row in enumerate(rows):
        if t < 9 + i * 2.5:
            continue
        y = y0 + 60 + i * 60
        dr.line([x0 - 40, y + 26, x0 + 2 * 160 + 60, y + 26], fill=(50, 50, 80), width=2)
        for j, val in enumerate(row):
            txt(dr, (x0 + j * 160, y), str(val), font(F_MONO, 26),
                GREEN if (i == 0 and j == 1) else WHITE, anchor="mm")
    if t > 20:
        txt(dr, (900, 470), "one line \u2014 three aggregates",
            font(F_BOLD, 28), YELLOW, anchor="mm")
    if t > 24:
        txt(dr, (900, 520), "vectorized: a million rows in milliseconds",
            font(F_SANS, 24), DIM, anchor="mm")

# ============================================================ IL-27: IT Infrastructure Specialist (bbg x3)
def scene_subnet27(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Subnetting: Carving Networks from One Block", BLUE)
    txt(dr, (W // 2, 170), "192.168.10.0 /24 \u2014 254 hosts", font(F_MONO, 30), WHITE, anchor="mm")
    k = clamp((t - 5) / 12)
    nshow = 1 + int(k * 3.999)
    nets = [("/26 \u00b7 62 hosts \u00b7 servers", CYAN, 0),
            ("/26 \u00b7 62 hosts \u00b7 workstations", TEAL, 1),
            ("/26 \u00b7 62 hosts \u00b7 printers/iot", YELLOW, 2),
            ("/26 \u00b7 62 hosts \u00b7 guest wifi", MAGENTA, 3)]
    bw = 260; gap = 20; total = 4 * bw + 3 * gap; x0 = (W - total) // 2
    for i, (nm, col, _) in enumerate(nets):
        if i >= nshow:
            continue
        x = x0 + i * (bw + gap)
        glow_box(dr, [x, 260, x + bw, 460], col, rad=12)
        dr.rectangle([x, 260, x + bw, 460], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 330), nm, font(F_MONOB, 22), col, anchor="mm")
        if i > 0:
            arrow(dr, x - gap, 360, x, 360, DIM, 4)
    if t > 20:
        txt(dr, (W // 2, 540), "borrow 2 bits \u2014 four networks, zero waste of broadcast domains",
            font(F_BOLD, 28), WHITE, anchor="mm")
    if t > 24:
        txt(dr, (W // 2, 590), "mask math: 255.255.255.192 \u2014 the line between net and host",
            font(F_MONO, 24), DIM, anchor="mm")

def scene_dns27(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "DNS: The Internet's Phonebook Lookup", BLUE)
    hops = [("YOUR PC", CYAN, 180), ("RESOLVER", YELLOW, 430),
            ("ROOT \u00b7 .", ORANGE, 680), ("TLD \u00b7 .com", MAGENTA, 930)]
    for i, (name, col, x) in enumerate(hops):
        on = t >= 4 + i * 3
        glow_box(dr, [x - 105, 220, x + 105, 360], col if on else (60, 60, 90), rad=12)
        dr.rectangle([x - 105, 220, x + 105, 360], fill=(12, 16, 34))
        txt(dr, (x, 280), name, font(F_BOLD, 24), col if on else DIM, anchor="mm")
        if i < 3:
            arrow(dr, x + 110, 290, hops[i + 1][2] - 110, 290, DIM, 5)
    if t > 8:
        # query packet hopping
        ph = clamp((t - 8) / 8)
        px = lerp(180, 930, ease(ph))
        dr.ellipse([px - 12, 420 - 12, px + 12, 420 + 12], fill=WHITE)
        txt(dr, (px, 455), "?", font(F_BOLD, 22), (10, 10, 30), anchor="mm")
    if t > 17:
        glow_box(dr, [380, 500, 900, 600], GREEN, rad=12)
        dr.rectangle([380, 500, 900, 600], fill=(10, 34, 22))
        txt(dr, (640, 542), "93.184.216.34 \u2014 cached for TTL", font(F_MONOB, 28), GREEN, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 645), "recursive \u2194 iterative: the resolver does the legwork",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_ad27(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Active Directory: The Forest", BLUE)
    glow_box(dr, [W // 2 - 200, 160, W // 2 + 200, 260], BLUE, rad=14)
    dr.rectangle([W // 2 - 200, 160, W // 2 + 200, 260], fill=(12, 16, 34))
    txt(dr, (W // 2, 200), "FOREST: corp.local", font(F_BOLD, 30), BLUE, anchor="mm")
    domains = [("hq.corp.local", CYAN, 320), ("ops.corp.local", TEAL, 640),
               ("lab.corp.local", YELLOW, 960)]
    for i, (name, col, x) in enumerate(domains):
        on = t >= 6 + i * 2.5
        glow_box(dr, [x - 140, 330, x + 140, 450], col if on else (60, 60, 90), rad=12)
        dr.rectangle([x - 140, 330, x + 140, 450], fill=(12, 16, 34))
        txt(dr, (x, 380), name, font(F_BOLD, 24), col if on else DIM, anchor="mm")
        arrow(dr, W // 2, 265, x, 325, DIM, 4)
    if t > 15:
        ous = ["OU=Workstations", "OU=Servers", "OU=Users"]
        for j, ou in enumerate(ous):
            y = 510 + j * 0
            x = 320 + j * 320
            dr.rectangle([x - 130, 500, x + 130, 556], fill=(16, 22, 44),
                         outline=DIM, width=2)
            txt(dr, (x, 528), ou, font(F_MONO, 22), WHITE, anchor="mm")
            arrow(dr, x, 452, x, 498, DIM, 3)
    if t > 22:
        txt(dr, (W // 2, 610), "group policy flows down \u2014 trust flows up through the forest root",
            font(F_BOLD, 28), WHITE, anchor="mm")
# ============================================================ IL-28: DevSecOps Cloud Infra (bbg x2 + fireship)
def scene_perms28(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Linux Permissions: Who Can Do What", BLUE)
    txt(dr, (W // 2, 180), "-rwxr-xr--", font(F_MONOB, 44), WHITE, anchor="mm")
    tri = [("OWNER", "rwx \u00b7 7", GREEN), ("GROUP", "r-x \u00b7 5", YELLOW), ("OTHER", "r-- \u00b7 4", CYAN)]
    bw = 280; gap = 40; total = 3 * bw + 2 * gap; x0 = (W - total) // 2
    for i, (who, bits, col) in enumerate(tri):
        x = x0 + i * (bw + gap)
        on = t >= 5 + i * 3
        glow_box(dr, [x, 260, x + bw, 460], col if on else (60, 60, 90), rad=14)
        dr.rectangle([x, 260, x + bw, 460], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 330), who, font(F_BOLD, 28), col if on else DIM, anchor="mm")
        txt(dr, (x + bw // 2, 390), bits, font(F_MONOB, 34), col if on else DIM, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 520), "chmod 754 deploy.sh", font(F_MONOB, 36), YELLOW, anchor="mm")
        txt(dr, (W // 2, 570), "7 = rwx \u00b7 5 = r-x \u00b7 4 = r--", font(F_MONO, 26), DIM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 630), "least privilege starts at the file system",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_systemd28(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "systemd: The Init System That Runs Everything", BLUE)
    units = [("sysinit.target", CYAN), ("basic.target", TEAL),
             ("multi-user.target", YELLOW), ("app.service", GREEN)]
    bw = 230; gap = 30; total = 4 * bw + 3 * gap; x0 = (W - total) // 2
    for i, (nm, col) in enumerate(units):
        x = x0 + i * (bw + gap)
        on = t >= 5 + i * 3
        glow_box(dr, [x, 240, x + bw, 400], col if on else (60, 60, 90), rad=12)
        dr.rectangle([x, 240, x + bw, 400], fill=(12, 16, 34))
        txt(dr, (x + bw // 2, 300), nm, font(F_MONOB, 21), col if on else DIM, anchor="mm")
        if on:
            txt(dr, (x + bw // 2, 355), "active", font(F_BOLD, 24), col, anchor="mm")
        if i < 3:
            arrow(dr, x + bw + 4, 320, x + bw + gap - 4, 320, DIM, 5)
    if t > 17:
        panel(dr, [x0, 470, x0 + total, 600], "UNIT FILE: app.service", GREEN, 24)
        txt(dr, (x0 + 40, 530), "[Service]  ExecStart=/opt/app/run  Restart=always",
            font(F_MONO, 26), WHITE, anchor="lm")
    if t > 23:
        txt(dr, (W // 2, 650), "dependencies ordered, failures restarted \u2014 init done right",
            font(F_BOLD, 28), WHITE, anchor="mm")

def scene_bash28(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "Bash Pipes: Small Tools, Composed", font(F_BOLD, 38), WHITE, anchor="mm")
    lines = [("journalctl -u app --since today", (200, 200, 255)),
             ("  | grep -i error", (0, 229, 255)),
             ("  | awk '{print $5}'", (0, 229, 255)),
             ("  | sort | uniq -c | sort -rn", (255, 214, 0)),
             ("  | head -5", (255, 214, 0))]
    code_panel(dr, 60, 140, 600, 580, "triage.sh", lines,
               hi_line=min(4, int((t - 4) / 4)), t=t)
    tools = [("grep", CYAN, 700), ("awk", MAGENTA, 880), ("sort", YELLOW, 1060)]
    for nm, col, x in tools:
        idx = tools.index((nm, col, x))
        on = t >= 7 + idx * 3
        glow_box(dr, [x - 80, 220, x + 80, 340], col if on else (60, 60, 100), rad=12)
        dr.rectangle([x - 80, 220, x + 80, 340], fill=(12, 12, 26))
        txt(dr, (x, 270), nm, font(F_BOLD, 28), col if on else DIM, anchor="mm")
        if idx < 2:
            arrow(dr, x + 85, 280, tools[idx + 1][2] - 85, 280, DIM, 4)
    if t > 18:
        txt(dr, (880, 430), "text in \u2014 text out \u2014 no ceremony",
            font(F_BOLD, 28), WHITE, anchor="mm")
    if t > 23:
        txt(dr, (880, 490), "the unix philosophy: do one thing well",
            font(F_SANS, 24), DIM, anchor="mm")

# ============================================================ IL-29: ThreatLocker AI Cyber Mastery (bbg x2 + fireship)
def scene_allowlist29(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Allowlisting: Trust, But Verify First", BLUE)
    # known-good list
    panel(dr, [80, 200, 560, 560], "ALLOWLIST (HASH \u00b7 SIGNER \u00b7 PATH)", GREEN, 24)
    apps = [("chrome.exe", True), ("teams.exe", True), ("invoice.pdf.exe", False),
            ("svchost.exe", True), ("mimikatz.exe", False)]
    for i, (nm, ok) in enumerate(apps):
        if t < 6 + i * 2.2:
            continue
        y = 270 + i * 56
        dr.rectangle([120, y - 20, 520, y + 20], fill=(10, 34, 22) if ok else (40, 10, 10),
                     outline=GREEN if ok else RED, width=2)
        txt(dr, (150, y), nm, font(F_MONO, 22), GREEN if ok else RED, anchor="lm")
        txt(dr, (490, y), "\u2713" if ok else "\u2717", font(F_BOLD, 26),
            GREEN if ok else RED, anchor="mm")
    # gate
    if t > 17:
        arrow(dr, 570, 380, 700, 380, DIM, 5)
        glow_box(dr, [710, 280, 1210, 480], BLUE, rad=14)
        dr.rectangle([710, 280, 1210, 480], fill=(12, 16, 34))
        txt(dr, (960, 350), "EXECUTION GATE", font(F_BOLD, 30), BLUE, anchor="mm")
        txt(dr, (960, 410), "on the list \u2192 runs", font(F_SANS, 24), GREEN, anchor="mm")
        txt(dr, (960, 448), "not on the list \u2192 blocked", font(F_SANS, 24), RED, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 630), "allowlisting: guilty until proven innocent",
            font(F_BOLD, 30), WHITE, anchor="mm")

def scene_ringfence29(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Ringfencing: Contain the Blast Radius", BLUE)
    # caged app
    glow_box(dr, [W // 2 - 220, 200, W // 2 + 220, 440], MAGENTA, rad=16)
    dr.rectangle([W // 2 - 220, 200, W // 2 + 220, 440], fill=(26, 10, 30))
    txt(dr, (W // 2, 260), "outlook.exe", font(F_BOLD, 34), WHITE, anchor="mm")
    txt(dr, (W // 2, 310), "can read email \u2014 cannot touch files", font(F_SANS, 22), DIM, anchor="mm")
    txt(dr, (W // 2, 350), "can reach mail server \u2014 no camera, no shell",
        font(F_SANS, 22), DIM, anchor="mm")
    if t > 10:
        denied = [("C:\\secrets\\", 150, 520), ("powershell.exe", 640, 560), ("webcam", 1050, 520)]
        for nm, x, y in denied:
            dr.line([x, y, x + 120, y], fill=RED, width=5)
            dr.line([x + 100, y - 20, x + 120, y], fill=RED, width=5)
            dr.line([x + 100, y + 20, x + 120, y], fill=RED, width=5)
            txt(dr, (x + 60, y - 30), nm, font(F_MONO, 20), RED, anchor="mm")
            arrow(dr, x + 60, y + 20, W // 2 - 230 if x < 640 else W // 2 + 230, 380, DIM, 3)
    if t > 22:
        txt(dr, (W // 2, 610), "ringfencing: the app keeps working \u2014 the attacker does not",
            font(F_BOLD, 30), MAGENTA, anchor="mm")

def scene_zt29(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    txt(dr, (W // 2, 60), "Zero Trust: Never Trust, Always Verify", font(F_BOLD, 38), WHITE, anchor="mm")
    lines = [("def authorize(request):", (200, 200, 255)),
             ("  identity = verify_mfa(request)", (0, 229, 255)),
             ("  device   = check_posture(request)", (0, 229, 255)),
             ("  if policy.allows(identity, device):", (255, 214, 0)),
             ("      return GRANT   # least privilege", (255, 214, 0)),
             ("  return DENY", (255, 120, 120))]
    code_panel(dr, 60, 140, 600, 600, "zerotrust.py", lines,
               hi_line=min(5, int((t - 4) / 3.4)), t=t)
    gates = [("IDENTITY", CYAN, 730), ("DEVICE", YELLOW, 930), ("POLICY", GREEN, 1130)]
    for nm, col, x in gates:
        idx = gates.index((nm, col, x))
        on = t >= 7 + idx * 3
        glow_box(dr, [x - 85, 240, x + 85, 370], col if on else (60, 60, 100), rad=12)
        dr.rectangle([x - 85, 240, x + 85, 370], fill=(12, 12, 26))
        txt(dr, (x, 295), nm, font(F_BOLD, 26), col if on else DIM, anchor="mm")
        if on:
            txt(dr, (x, 340), "\u2713", font(F_BOLD, 30), col, anchor="mm")
    if t > 20:
        txt(dr, (930, 460), "every request re-verified", font(F_BOLD, 28), WHITE, anchor="mm")
    if t > 24:
        txt(dr, (930, 510), "no implicit trust \u2014 not even inside",
            font(F_SANS, 24), DIM, anchor="mm")

# ============================================================ VIDEO CONFIG
VIDEOS = [
 # --- IL-22: The Deep Library — Esoteric & Secret Knowledge
 dict(file="story-kybalion-seven.mp4", style="story", scene=scene_kybalion,
      kicker="IL-22 \u00b7 The Deep Library \u2014 Esoteric & Secret Knowledge", title="The Kybalion",
      sub="Seven hermetic principles", module=2,
      blurb="The seven principles of the hermetic philosophy \u2014 mentalism, correspondence, vibration, polarity, rhythm, cause and effect, gender \u2014 master these and the rest is commentary.",
      captions=[(4,10,"The All is mind \u2014 mentalism"),
                (10,16,"As above, so below \u2014 correspondence"),
                (16,22,"Nothing rests \u2014 vibration and polarity"),
                (22,26,"Master the principles \u2014 the rest is commentary")]),
 dict(file="story-golden-dawn-grades.mp4", style="story", scene=scene_golden_dawn,
      kicker="IL-22 \u00b7 The Deep Library \u2014 Esoteric & Secret Knowledge", title="The Golden Dawn",
      sub="A ladder of grades", module=9,
      blurb="The Hermetic Order of the Golden Dawn: a graded ladder from neophyte through the elemental grades to adept \u2014 ten sephiroth, one tree, ascent by correspondence.",
      captions=[(4,10,"The Golden Dawn: a ladder of ritual grades"),
                (10,16,"Neophyte, Zelator, Theoricus, Practicus"),
                (16,22,"Philosophus \u2014 then the vault of the adept"),
                (22,26,"Ten sephiroth, one tree \u2014 ascent by correspondence")]),
 dict(file="story-fools-journey.mp4", style="story", scene=scene_fools,
      kicker="IL-22 \u00b7 The Deep Library \u2014 Esoteric & Secret Knowledge", title="The Fool's Journey",
      sub="Twenty-two arcana, one itinerary", module=5,
      blurb="The tarot's major arcana as the soul's itinerary: the Fool steps off the cliff, the Magician focuses will, the Wheel turns fortune, the World completes the dance.",
      captions=[(4,10,"The Fool: innocence steps off the cliff"),
                (10,16,"The Magician: will, focused like a lens"),
                (16,22,"The Wheel: fortune turns \u2014 rise and fall"),
                (22,26,"The World: the dance completes the circle")]),
 # --- IL-23: The Frontier — Cutting-Edge Research Distilled
 dict(file="story-transformer-attention.mp4", style="story", scene=scene_frontier_attention,
      kicker="IL-23 \u00b7 The Frontier \u2014 Cutting-Edge Research Distilled", title="Attention Is All You Need",
      sub="The transformer, distilled", module=0,
      blurb="The transformer in thirty seconds: every token weighs every other token, attention scores decide what matters, and meaning emerges from the weights.",
      captions=[(4,10,"Tokens: the sentence becomes pieces"),
                (10,16,"Attention: every word weighs every other word"),
                (16,22,"The weights decide what \u2018sat\u2019 really means"),
                (22,26,"Meaning emerges from the weights")]),
 dict(file="story-qubit-superposition.mp4", style="story", scene=scene_qubit,
      kicker="IL-23 \u00b7 The Frontier \u2014 Cutting-Edge Research Distilled", title="The Qubit",
      sub="Both at once, until you ask", module=1,
      blurb="A qubit lives in superposition \u2014 part |0>, part |1> \u2014 until measurement collapses the maybe: the act of asking decides the answer.",
      captions=[(4,10,"A classical bit is 0 or 1 \u2014 a qubit is both"),
                (10,16,"Superposition: \u03b1|0\u27e9 + \u03b2|1\u27e9"),
                (16,22,"The probabilities tilt as the state vector turns"),
                (22,26,"Measurement collapses the maybe \u2014 asking decides")]),
 dict(file="story-fusion-ignition.mp4", style="story", scene=scene_fusion,
      kicker="IL-23 \u00b7 The Frontier \u2014 Cutting-Edge Research Distilled", title="Fusion: A Star on Earth",
      sub="Heat, squeeze, ignite", module=3,
      blurb="Magnetic confinement fusion: plasma heated past 150 million degrees inside a magnetic bottle until it ignites and heats itself \u2014 a star, on earth.",
      captions=[(4,10,"Heat the plasma \u2014 past 150 million degrees"),
                (10,16,"Squeeze it \u2014 inside a magnetic bottle"),
                (16,22,"Ignition: the plasma starts heating itself"),
                (22,26,"A star on earth \u2014 ten times the sun\u2019s core")]),
 # --- IL-24: ThreatLocker Assessment Prep CBT
 dict(file="bbg-triage-loop.mp4", style="bbg", scene=scene_triage,
      kicker="IL-24 \u00b7 ThreatLocker Assessment Prep CBT", title="The Cyber Hero Triage Loop",
      sub="Speed with judgment", module=1,
      blurb="The Cyber Hero triage loop: alert fires, enrich with hash/signer/behavior, decide approve-deny-ringfence, act and document \u2014 every decision feeds the next alert.",
      captions=[(4,10,"The alert fires in the portal"),
                (10,16,"Enrich: hash, signer, behavior"),
                (16,22,"Decide: approve, deny, or ringfence"),
                (22,26,"Speed with judgment \u2014 triage in minutes")]),
 dict(file="bbg-default-deny.mp4", style="bbg", scene=scene_defaultdeny,
      kicker="IL-24 \u00b7 ThreatLocker Assessment Prep CBT", title="Default-Deny",
      sub="Learning mode to least privilege", module=2,
      blurb="Default-deny operations: learning mode observes everything, a known-good baseline is built, then enforcement flips on \u2014 nothing runs unless the policy says so.",
      captions=[(4,10,"Learning mode: observe everything"),
                (10,16,"Baseline: the known-good inventory"),
                (16,22,"Enforce: deny the unknown"),
                (22,26,"Default-deny: nothing runs unless allowed")]),
 dict(file="fireship-ringfence-decision.mp4", style="fireship", scene=scene_ringfence_fs,
      kicker="IL-24 \u00b7 ThreatLocker Assessment Prep CBT", title="Ringfencing: Approve, Deny, Contain",
      sub="The third option", module=3,
      blurb="Ringfencing is the third triage option: the app runs but caged \u2014 corp-vpn allowed, local files and camera denied. Contain, don\u2019t just block.",
      captions=[(4,10,"The policy: ringfence the risky app"),
                (10,16,"Allowed: corp-vpn \u2014 work continues"),
                (16,22,"Denied: local files, camera \u2014 blast radius zero"),
                (22,26,"Contain, don\u2019t just block")]),
 # --- IL-25: Professional Certificate in Cybersecurity
 dict(file="bbg-threat-vuln-chain.mp4", style="bbg", scene=scene_threatvuln,
      kicker="IL-25 \u00b7 Professional Certificate in Cybersecurity", title="Threats Meet Vulnerabilities",
      sub="The kill chain", module=3,
      blurb="Threat actor plus vulnerability plus exploit equals impact \u2014 the kill chain. Remove any single link and the chain breaks: defense in depth.",
      captions=[(4,10,"Threat actor: motive plus capability"),
                (10,16,"Vulnerability: an unpatched door"),
                (16,22,"Exploit: the key that fits \u2014 impact follows"),
                (22,26,"Break any link \u2014 the chain fails")]),
 dict(file="bbg-iam-layers.mp4", style="bbg", scene=scene_iam,
      kicker="IL-25 \u00b7 Professional Certificate in Cybersecurity", title="IAM: Identity Is the Perimeter",
      sub="Authenticate \u00b7 authorize \u00b7 account \u00b7 audit", module=6,
      blurb="IAM in four layers: authenticate with MFA, authorize least privilege, manage the joiner-mover-leaver lifecycle, audit everything \u2014 identity is the new perimeter.",
      captions=[(4,10,"Authenticate: prove who you are \u2014 MFA"),
                (10,16,"Authorize: least privilege, RBAC"),
                (16,22,"Account: the joiner-mover-leaver lifecycle"),
                (22,26,"Audit: log everything \u2014 identity is the perimeter")]),
 dict(file="fireship-soc-pipeline.mp4", style="fireship", scene=scene_soc_fs,
      kicker="IL-25 \u00b7 Professional Certificate in Cybersecurity", title="The SOC Pipeline",
      sub="Detect \u2192 respond", module=10,
      blurb="The SOC pipeline: hunt with SPL, detect anomalies three times baseline, triage fast, respond from playbooks \u2014 MTTR crushed from 42 minutes to 11.",
      captions=[(4,10,"Hunt: the SPL query finds the anomaly"),
                (10,16,"Detect: three times baseline \u2014 alert fires"),
                (16,22,"Triage and respond: playbooks turn panic to procedure"),
                (22,26,"Hunt, don\u2019t wait \u2014 the alert is the starting gun")]),
 # --- IL-26: Data Analyst Certification & Senior Mastery
 dict(file="3b1b-normal-distribution.mp4", style="3b1b", scene=scene_normal,
      kicker="IL-26 \u00b7 Data Analyst Certification & Senior Mastery", title="The Normal Distribution",
      sub="The bell curve", module=5,
      blurb="The normal distribution: averages cluster, extremes are rare, and the empirical rule maps 68-95-99.7 percent to one-two-three sigma \u2014 the central limit theorem guarantees it.",
      captions=[(4,10,"The bell curve grows from the center out"),
                (10,16,"One sigma: 68 percent of the data"),
                (16,22,"Two, three sigma: 95, then 99.7 percent"),
                (22,26,"Central limit theorem: sample means go normal \u2014 always")]),
 dict(file="3b1b-p-value.mp4", style="3b1b", scene=scene_pvalue,
      kicker="IL-26 \u00b7 Data Analyst Certification & Senior Mastery", title="The P-Value",
      sub="How surprised should you be?", module=12,
      blurb="The p-value: assuming nothing is happening, how weird is this data? Below 0.05, reject the null \u2014 but never prove the alternative.",
      captions=[(4,10,"The null: assume nothing is happening"),
                (10,16,"The test statistic lands far from the center"),
                (16,22,"The tail area: that\u2019s the p-value"),
                (22,26,"p < 0.05: reject the null \u2014 never prove the alternative")]),
 dict(file="fireship-pandas-groupby.mp4", style="fireship", scene=scene_pandas_fs,
      kicker="IL-26 \u00b7 Data Analyst Certification & Senior Mastery", title="pandas groupby",
      sub="Split \u2014 apply \u2014 combine", module=10,
      blurb="pandas groupby in one line: split by region, apply sum and mean to revenue, combine into a sorted table \u2014 vectorized, a million rows in milliseconds.",
      captions=[(4,10,"Load the frame \u2014 a million rows, no sweat"),
                (10,16,"Split by region \u2014 groups form"),
                (16,22,"Apply sum and mean \u2014 combine into a table"),
                (22,26,"Vectorized: milliseconds, not minutes")]),
 # --- IL-27: IT Infrastructure Specialist
 dict(file="bbg-subnet-carving.mp4", style="bbg", scene=scene_subnet27,
      kicker="IL-27 \u00b7 IT Infrastructure Specialist \u2014 Zero Trust Infrastructure Mastery",
      title="Subnetting: Carving Networks", sub="One /24, four networks", module=4,
      blurb="Subnetting: borrow two bits from a /24 and carve four /26 networks \u2014 servers, workstations, printers, guest wifi \u2014 with a 255.255.255.192 mask.",
      captions=[(4,10,"One /24: 254 hosts, one broadcast domain"),
                (10,16,"Borrow two bits \u2014 four /26 networks"),
                (16,22,"Servers, workstations, IoT, guest \u2014 separated"),
                (22,26,"Mask math: 255.255.255.192 \u2014 net vs host")]),
 dict(file="bbg-dns-resolution.mp4", style="bbg", scene=scene_dns27,
      kicker="IL-27 \u00b7 IT Infrastructure Specialist \u2014 Zero Trust Infrastructure Mastery",
      title="DNS: The Phonebook Lookup", sub="Recursive \u2194 iterative", module=5,
      blurb="DNS resolution: your PC asks the resolver, which walks root to TLD to authoritative and caches the answer for the TTL \u2014 the resolver does the legwork.",
      captions=[(4,10,"Your PC asks the resolver"),
                (10,16,"The resolver walks: root, TLD, authoritative"),
                (16,22,"The answer comes back \u2014 cached for the TTL"),
                (22,26,"Recursive vs iterative \u2014 the resolver does the legwork")]),
 dict(file="bbg-active-directory.mp4", style="bbg", scene=scene_ad27,
      kicker="IL-27 \u00b7 IT Infrastructure Specialist \u2014 Zero Trust Infrastructure Mastery",
      title="Active Directory: The Forest", sub="Domains, OUs, and trust", module=11,
      blurb="Active Directory: one forest, child domains, organizational units beneath \u2014 group policy flows down, trust flows up through the forest root.",
      captions=[(4,10,"The forest: the security boundary"),
                (10,16,"Child domains: hq, ops, lab"),
                (16,22,"OUs: workstations, servers, users"),
                (22,26,"Policy flows down \u2014 trust flows up")]),
 # --- IL-28: DevSecOps & Cloud Infrastructure
 dict(file="bbg-linux-permissions.mp4", style="bbg", scene=scene_perms28,
      kicker="IL-28 \u00b7 DevSecOps & Cloud Infrastructure \u2014 Production Mastery",
      title="Linux Permissions", sub="Who can do what", module=6,
      blurb="Linux permissions: owner, group, other \u2014 read, write, execute in octal. chmod 754: full control for you, read-execute for the team, read-only for the world.",
      captions=[(4,10,"Three actors: owner, group, other"),
                (10,16,"Three rights: read, write, execute"),
                (16,22,"Octal: 7-5-4 \u2014 chmod 754 deploy.sh"),
                (22,26,"Least privilege starts at the file system")]),
 dict(file="bbg-systemd-units.mp4", style="bbg", scene=scene_systemd28,
      kicker="IL-28 \u00b7 DevSecOps & Cloud Infrastructure \u2014 Production Mastery",
      title="systemd", sub="The init system", module=8,
      blurb="systemd: targets boot in order \u2014 sysinit, basic, multi-user \u2014 then your app.service starts with Restart=always. Dependencies ordered, failures restarted.",
      captions=[(4,10,"Targets: the boot order, declared"),
                (10,16,"Units activate \u2014 dependencies resolved"),
                (16,22,"app.service: ExecStart, Restart=always"),
                (22,26,"Init done right: ordered, supervised, restarted")]),
 dict(file="fireship-bash-pipes.mp4", style="fireship", scene=scene_bash28,
      kicker="IL-28 \u00b7 DevSecOps & Cloud Infrastructure \u2014 Production Mastery",
      title="Bash Pipes", sub="Small tools, composed", module=10,
      blurb="Bash pipes: journalctl into grep into awk into sort into head \u2014 text in, text out, no ceremony. The unix philosophy: do one thing well.",
      captions=[(4,10,"journalctl: the logs, streaming"),
                (10,16,"grep, awk: filter and extract"),
                (16,22,"sort, uniq, head: the top five errors"),
                (22,26,"Text in \u2014 text out \u2014 no ceremony")]),
 # --- IL-29: ThreatLocker Zero-Trust CBT with AI
 dict(file="bbg-allowlist-ops.mp4", style="bbg", scene=scene_allowlist29,
      kicker="IL-29 \u00b7 ThreatLocker Zero-Trust CBT with AI \u2014 Cybersecurity Mastery",
      title="Allowlisting Operations", sub="Guilty until proven innocent", module=1,
      blurb="Allowlisting operations: every executable checked against hash, signer, and path \u2014 on the list it runs, off the list it\u2019s blocked. Guilty until proven innocent.",
      captions=[(4,10,"The allowlist: hash, signer, path"),
                (10,16,"Known-good: chrome, teams \u2014 they run"),
                (16,22,"Unknown: invoice.pdf.exe, mimikatz \u2014 blocked"),
                (22,26,"Guilty until proven innocent")]),
 dict(file="bbg-ringfencing-deep.mp4", style="bbg", scene=scene_ringfence29,
      kicker="IL-29 \u00b7 ThreatLocker Zero-Trust CBT with AI \u2014 Cybersecurity Mastery",
      title="Ringfencing Deep Dive", sub="Contain the blast radius", module=2,
      blurb="Ringfencing deep dive: outlook.exe keeps reading email and reaching the mail server \u2014 but cannot touch files, spawn shells, or reach the camera. The app works; the attacker doesn\u2019t.",
      captions=[(4,10,"The app, caged: outlook.exe"),
                (10,16,"Allowed: email, the mail server"),
                (16,22,"Denied: files, shells, the camera"),
                (22,26,"The app works \u2014 the attacker does not")]),
 dict(file="fireship-zero-trust-verify.mp4", style="fireship", scene=scene_zt29,
      kicker="IL-29 \u00b7 ThreatLocker Zero-Trust CBT with AI \u2014 Cybersecurity Mastery",
      title="Zero Trust: Always Verify", sub="Never trust, always verify", module=0,
      blurb="Zero trust in code: verify MFA identity, check device posture, consult policy \u2014 grant least privilege or deny. Every request re-verified, even inside the network.",
      captions=[(4,10,"Verify identity: MFA, every time"),
                (10,16,"Check the device: posture, patches"),
                (16,22,"Consult policy: grant least privilege \u2014 or deny"),
                (22,26,"No implicit trust \u2014 not even inside")]),
]

COURSE_FILES = {
    22: "il-22-esoteric-secret-knowledge.json",
    23: "il-23-frontier-knowledge.json",
    24: "il-24-threatlocker-assessment-prep-cbt.json",
    25: "il-25-cybersecurity-professional-certificate.json",
    26: "il-26-data-analyst-certification-senior-mastery.json",
    27: "il-27-it-infrastructure-specialist-threatlocker-mastery.json",
    28: "il-28-devsecops-cloud-infrastructure-mastery.json",
    29: "il-29-threatlocker-ai-cybersecurity-mastery.json",
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
