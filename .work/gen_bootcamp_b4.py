#!/usr/bin/env python3
"""Bootcamp video Phase 2, Batch B4: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b3.py (do not modify the B3 file).

Filenames are bc- prefixed so they never collide with course videos.

Batch B4 bootcamps (data/ML cluster):
  data-analyst, data-analyst-to-ml, data-engineering,
  data-science-certs, datascience-ml, deep-learning,
  nlp-advanced, nlp-engineering, neuroai,
  quant-finance-ladder, quant-finance-math, sql
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

def bar(dr, x, y, w, h, frac, fill, label=None, val=None):
    dr.rectangle([x, y, x + w, y + h], fill=(18, 24, 40), outline=DIM, width=2)
    fw = int(w * clamp(frac))
    if fw > 4:
        dr.rectangle([x + 2, y + 2, x + fw - 2, y + h - 2], fill=fill)
    if label:
        txt(dr, (x, y - 8), label, font(F_SANS, 22), DIM, anchor="lb")
    if val:
        txt(dr, (x + w, y + h + 8), val, font(F_MONOB, 24), fill, anchor="rt")

def warm_rings(dr):
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)

# ============================================================ data-analyst (bbg x1 + 3b1b x1 + fireship x1)
def scene_da_dirty(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE DIRTY DATA TRIAGE", CYAN)
    rows = [("age: 34", "ok", GREEN), ("age: NULL", "missing", RED),
            ("age: -5", "impossible", RED), ("age: 34", "duplicate", ORANGE),
            ("age: thiry-four", "typo", ORANGE), ("age: 999", "outlier", YELLOW)]
    if t > 4:
        txt(dr, (W // 2, 180), "six rows land on your desk \u2014 four of them lie",
            font(F_SANS, 26), DIM, anchor="mm")
        nshow = int(clamp((t - 4) / 5) * len(rows))
        for i, (val, issue, col) in enumerate(rows[:nshow]):
            y = 250 + i * 62
            dr.rectangle([320, y - 24, 960, y + 24], fill=(12, 18, 32), outline=col, width=2)
            txt(dr, (360, y), val, font(F_MONO, 24), CREAM, anchor="lm")
            txt(dr, (920, y), issue.upper(), font(F_BOLD, 22), col, anchor="rm")
    if t > 12:
        txt(dr, (W // 2, 600), "missing \u2192 median \u00b7 dupes \u2192 drop \u00b7 typos \u2192 normalize",
            font(F_SANS, 24), YELLOW, anchor="mm")
    if t > 17:
        bar(dr, 340, 640 - 30, 600, 40, clamp((t - 17) / 4), GREEN, "clean rows", "100%")
    if t > 22:
        txt(dr, (W // 2, 668), "analysts spend 80% of the job cleaning \u2014 triage it like a pro",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_da_skew(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE AVERAGE THAT LIES", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "ten salaries \u2014 one CEO walks in, and the mean runs away",
        font(F_SANS, 24), DIM, anchor="mm")
    ox, oy, pw, ph = 200, 560, 880, 300
    dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
    heights = [0.45, 0.7, 0.85, 0.95, 0.9, 0.75, 0.55, 0.35, 0.2, 0.1]
    k = clamp((t - 4) / 8)
    for i, hh in enumerate(heights):
        bw = pw / len(heights)
        x = ox + i * bw
        dr.rectangle([x + 4, oy - hh * ph * k, x + bw - 4, oy], fill=TEAL)
    if t > 8:
        med_x = ox + pw * 0.42
        dr.line([med_x, oy - ph, med_x, oy], fill=GREEN, width=4)
        txt(dr, (med_x, oy - ph - 14), "median $62k", font(F_BOLD, 22), GREEN, anchor="mb")
        mean_x = ox + pw * (0.42 + 0.3 * clamp((t - 8) / 6))
        dr.line([mean_x, oy - ph, mean_x, oy], fill=RED, width=4)
        txt(dr, (mean_x, oy + 26), "mean $148k", font(F_BOLD, 22), RED, anchor="mt")
    if t > 15:
        txt(dr, (W // 2, 620), "one billionaire moved the mean $86k \u2014 the median didn't flinch",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 668), "skewed data? report the median \u2014 the mean is a hostage",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_da_pandas(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE PANDAS ONE-LINER IN 100 SECONDS", MAGENTA)
    lines = ["import pandas as pd",
             "df = pd.read_csv('sales.csv')",
             "df = df.dropna().drop_duplicates()",
             "top = df.groupby('region')['revenue'].sum()",
             "top.sort_values(ascending=False).head(3)",
             "# west: $4.2M \u00b7 east: $3.8M \u00b7 north: $2.1M"]
    cols = [(200, 200, 255), (200, 200, 255), YELLOW,
            (200, 200, 255), (200, 200, 255), GREEN]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "top_regions.py", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "read, clean, group, sort \u2014 eighty percent of analyst work in five lines",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ data-analyst-to-ml (bbg x1 + primer x1 + fireship x1)
def scene_daml_split(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE TEST SET YOU NEVER TOUCH", CYAN)
    if t > 4:
        txt(dr, (W // 2, 180), "1000 labeled rows \u2014 split before you train",
            font(F_SANS, 26), DIM, anchor="mm")
        k = clamp((t - 4) / 6)
        n = int(50 * k)
        for i in range(n):
            x = 180 + (i % 25) * 40
            y = 250 + (i // 25) * 46
            test = i >= 40
            col = ORANGE if test else TEAL
            dr.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col)
    if t > 12:
        dr.rectangle([140, 230, 180 + 25 * 40 + 20, 230 + 2 * 46 + 20], outline=TEAL, width=3)
        txt(dr, (640, 400), "TRAIN 80%", font(F_BOLD, 26), TEAL, anchor="mm")
        dr.rectangle([180 + 20 * 40 - 20, 230, 180 + 25 * 40 + 20, 230 + 2 * 46 + 20],
                     outline=ORANGE, width=3)
        txt(dr, (1010, 400), "TEST 20%", font(F_BOLD, 26), ORANGE, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 500), "the model trains on teal \u2014 orange stays sealed until the end",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 600), "peek at the test set and your score is fiction \u2014 lock it away",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_daml_overfit(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE MODEL THAT MEMORIZED THE EXAM", font(F_BOLD, 36), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "complexity rises \u2014 training error falls, test error turns",
        font(F_SANS, 24), DIM, anchor="mm")
    ox, oy, pw, ph = 200, 560, 880, 320
    dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
    txt(dr, (ox, oy + 24), "simple", font(F_SANS, 20), DIM, anchor="lm")
    txt(dr, (ox + pw, oy + 24), "complex", font(F_SANS, 20), DIM, anchor="rm")
    txt(dr, (ox - 14, oy - ph), "error", font(F_SANS, 20), DIM, anchor="rb")
    k = clamp((t - 5) / 12)
    train, test = [], []
    for i in range(int(70 * k)):
        x = ox + i / 70 * pw
        tr = oy - (0.9 - 0.75 * (i / 70)) * ph
        te = oy - (0.9 - 0.75 * (i / 70) + 1.6 * max(0, i / 70 - 0.55) ** 2) * ph
        train.append((x, tr)); test.append((x, te))
    if len(train) > 1:
        dr.line(train, fill=CYAN, width=4)
        dr.line(test, fill=ORANGE, width=4)
    txt(dr, (ox + pw - 160, oy - ph + 40), "train", font(F_BOLD, 22), CYAN, anchor="lm")
    txt(dr, (ox + pw - 160, oy - ph + 72), "test", font(F_BOLD, 22), ORANGE, anchor="lm")
    if t > 15:
        sx = ox + pw * 0.55
        dr.line([sx, oy - ph, sx, oy], fill=GREEN, width=3)
        txt(dr, (sx, oy - ph - 14), "sweet spot", font(F_BOLD, 22), GREEN, anchor="mb")
    if t > 21:
        txt(dr, (W // 2, 640), "past the sweet spot the model memorizes \u2014 and the test pays for it",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_daml_model(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "YOUR FIRST MODEL IN 100 SECONDS", MAGENTA)
    lines = ["from sklearn.ensemble import RandomForestClassifier",
             "model = RandomForestClassifier(n_estimators=100)",
             "model.fit(X_train, y_train)      # learn",
             "preds = model.predict(X_test)    # guess",
             "print(accuracy_score(y_test, preds))",
             "# 0.91 \u2014 your first model just beat a coin flip"]
    cols = [(200, 200, 255), (200, 200, 255), YELLOW,
            (200, 200, 255), (200, 200, 255), GREEN]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 120, 150, W - 120, 560, "first_model.py", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "fit, predict, score \u2014 the whole ritual in six lines",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ data-engineering (bbg x1 + fireship x1 + primer x1)
def scene_de_retry(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE PIPELINE THAT REFUSED TO DIE", CYAN)
    stages = [("extract", 200), ("transform", 520), ("load", 840)]
    if t > 4:
        for nm, x in stages:
            failed = (nm == "transform" and 10 < t < 18)
            col = RED if failed else (GREEN if t > 18 or nm != "transform" else CYAN)
            dr.rectangle([x - 130, 260, x + 130, 400], fill=(10, 16, 28), outline=col, width=4)
            txt(dr, (x, 320), nm.upper(), font(F_BOLD, 26), col, anchor="mm")
            txt(dr, (x, 360), "OK" if not failed else "FAILED", font(F_MONO, 22), col, anchor="mm")
        arrow(dr, 340, 330, 380, 330, DIM, 4)
        arrow(dr, 660, 330, 700, 330, DIM, 4)
    if t > 10 and t < 18:
        att = int(clamp((t - 10) / 8) * 3) + 1
        txt(dr, (520, 480), "attempt %d \u2014 backing off %ds" % (att, 2 ** att),
            font(F_MONO, 26), YELLOW, anchor="mm")
    if t > 18:
        txt(dr, (520, 480), "attempt 4 \u2014 success", font(F_MONO, 26), GREEN, anchor="mm")
        txt(dr, (W // 2, 560), "idempotent tasks + exponential backoff = pipelines that heal",
            font(F_SANS, 25), CREAM, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 640), "everything fails at 3 AM \u2014 design the retry before the page",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_de_dbt(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE DBT MODEL IN 100 SECONDS", MAGENTA)
    lines = ["-- models/marts/orders_clean.sql",
             "select order_id, customer_id,",
             "       amount,",
             "       coalesce(discount, 0) as discount",
             "from {{ ref('orders_raw') }}",
             "where amount > 0      -- kill the refunds"]
    cols = [(150, 160, 190), (200, 200, 255), (200, 200, 255),
            YELLOW, (200, 200, 255), GREEN]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "orders_clean.sql", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "SQL with tests and lineage \u2014 the warehouse grows up",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_de_drift(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE COLUMN THAT APPEARED OVERNIGHT", font(F_BOLD, 36), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "schemas drift \u2014 contracts catch them before the dashboards break",
        font(F_SANS, 24), DIM, anchor="mm")
    cols0 = ["id", "email", "plan"]
    days = ["mon", "tue", "wed", "thu", "fri"]
    k = clamp((t - 5) / 12)
    ndays = int(len(days) * k)
    for i in range(ndays):
        x = 190 + i * 190
        dr.rectangle([x, 220, x + 160, 420], fill=(14, 20, 34), outline=TEAL, width=3)
        txt(dr, (x + 80, 250), days[i].upper(), font(F_BOLD, 22), TEAL, anchor="mm")
        show = cols0 + (["signup_src"] if i >= 4 else [])
        for j, c in enumerate(show):
            col = RED if c == "signup_src" else CREAM
            txt(dr, (x + 80, 310 + j * 36), c, font(F_MONO, 20), col, anchor="mm")
    if t > 17:
        dr.rectangle([W // 2 - 320, 500, W // 2 + 320, 570], fill=(40, 30, 8), outline=YELLOW, width=3)
        txt(dr, (W // 2, 535), "contract check: new column \u2192 schema v2, dashboards warned",
            font(F_SANS, 22), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "schema drift is inevitable \u2014 surprise is optional",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ data-science-certs (story x1 + bbg x1 + fireship x1)
def scene_dsc_exam(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "EXAM DAY", font(F_SERIFB, 42), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "7:58 AM \u2014 the testing center smells like carpet and nerves",
            font(F_SERIF, 27), CREAM, anchor="mm")
        txt(dr, (W // 2, 270), "sixty questions \u2014 you have studied four hundred hours for this",
            font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    if t > 11:
        txt(dr, (W // 2, 380), "question 41: the p-value question \u2014 you smile, you know this one",
            font(F_SERIF, 27), YELLOW, anchor="mm")
    if t > 16:
        k = clamp((t - 16) / 5)
        bar(dr, 440, 480, 400, 40, k, GOLD, "progress", "%d/60" % int(60 * k))
    if t > 21:
        txt(dr, (W // 2, 590), "PASS \u2014 the cert is paper; the four hundred hours are the real credential",
            font(F_SERIF, 26), GOLD, anchor="mm")

def scene_dsc_ab(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "SHIP IT OR KILL IT: THE A/B TEST", CYAN)
    if t > 4:
        txt(dr, (W // 2, 180), "control vs treatment \u2014 10,000 users each",
            font(F_SANS, 26), DIM, anchor="mm")
    k = clamp((t - 6) / 8)
    bar(dr, 240, 280, 360, 60, 0.42, CYAN, "control", "4.2%")
    bar(dr, 680, 280, 360, 60, 0.42 + 0.11 * k, GREEN, "treatment", "%.1f%%" % (4.2 + 1.1 * k))
    if t > 14:
        p = 0.20 - 0.17 * clamp((t - 14) / 6)
        txt(dr, (W // 2, 440), "p-value: %.3f" % p, font(F_MONOB, 34),
            GREEN if p < 0.05 else YELLOW, anchor="mm")
        txt(dr, (W // 2, 490), "below 0.05 \u2014 the lift is real" if p < 0.05 else "still noise \u2014 keep waiting",
            font(F_SANS, 25), GREEN if p < 0.05 else YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 600), "no p-hacking, no peeking early \u2014 the test decides, not your hope",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_dsc_resume(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "RESUME BULLETS THAT GET INTERVIEWS", MAGENTA)
    lines = ["# weak:  'worked with data'",
             "# strong: quantified, specific, owned",
             "\u2022 cut churn-report runtime 6h \u2192 20min (dbt + partitions)",
             "\u2022 A/B framework: 40 experiments/yr, +3.1% conversion",
             "\u2022 dashboard adopted by 200+ sellers, $1.2M influenced",
             "numbers are the verbs \u2014 metrics are the proof"]
    cols = [(150, 160, 190), (150, 160, 190), GREEN, GREEN, GREEN, YELLOW]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 100, 150, W - 100, 560, "resume.md", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "every bullet: action, scale, outcome \u2014 or it doesn't ship",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ datascience-ml (3b1b x1 + bbg x1 + primer x1)
def scene_dsml_biasvar(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "BIAS, VARIANCE, AND THE SWEET SPOT", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "total error = bias\u00b2 + variance + noise \u2014 watch the tradeoff",
        font(F_SANS, 24), DIM, anchor="mm")
    ox, oy, pw, ph = 200, 560, 880, 320
    dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
    k = clamp((t - 5) / 12)
    bias, var, tot = [], [], []
    for i in range(int(70 * k)):
        x = ox + i / 70 * pw
        b = 0.9 - 0.7 * (i / 70)
        v = 0.05 + 1.1 * (i / 70) ** 2
        bias.append((x, oy - b * ph)); var.append((x, oy - v * ph))
        tot.append((x, oy - (b + v + 0.08) * ph))
    if len(bias) > 1:
        dr.line(bias, fill=BLUE, width=4)
        dr.line(var, fill=RED, width=4)
        dr.line(tot, fill=YELLOW, width=5)
    txt(dr, (ox + pw - 150, oy - ph + 36), "bias", font(F_BOLD, 22), BLUE, anchor="lm")
    txt(dr, (ox + pw - 150, oy - ph + 68), "variance", font(F_BOLD, 22), RED, anchor="lm")
    txt(dr, (ox + pw - 150, oy - ph + 100), "total", font(F_BOLD, 22), YELLOW, anchor="lm")
    if t > 16:
        sx = ox + pw * 0.52
        dr.line([sx, oy - ph, sx, oy], fill=GREEN, width=3)
        txt(dr, (sx, oy - ph - 14), "sweet spot", font(F_BOLD, 22), GREEN, anchor="mb")
    if t > 21:
        txt(dr, (W // 2, 640), "too simple: blind \u00b7 too complex: paranoid \u2014 the middle generalizes",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_dsml_leak(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE 99.8% THAT WAS A LIE", CYAN)
    feats = [("age", False), ("tenure_months", False), ("support_tickets", False),
             ("cancel_date", True), ("last_login", False)]
    if t > 4:
        txt(dr, (W // 2, 180), "churn model features \u2014 one of these knows the future",
            font(F_SANS, 26), DIM, anchor="mm")
        nshow = int(clamp((t - 4) / 6) * len(feats))
        for i, (f, leak) in enumerate(feats[:nshow]):
            y = 270 + i * 66
            hot = leak and t > 12
            col = RED if hot else (DIM if leak and t <= 12 else CREAM)
            dr.rectangle([340, y - 26, 940, y + 26], fill=(12, 18, 32), outline=col, width=2)
            txt(dr, (380, y), f, font(F_MONO, 24), col, anchor="lm")
            if hot:
                txt(dr, (900, y), "LEAK", font(F_BOLD, 22), RED, anchor="rm")
    if t > 10:
        txt(dr, (W // 2, 620), "accuracy: 99.8% \u2014 too good to be true is too good",
            font(F_MONOB, 30), YELLOW, anchor="mm")
    if t > 15:
        txt(dr, (W // 2, 620), "cancel_date only exists AFTER churn \u2014 drop it: 71%",
            font(F_MONOB, 28), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 668), "if it's too good, it's leaking \u2014 audit every feature's timestamp",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_dsml_imbalance(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "99% ACCURATE, 100% USELESS", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "fraud is 1 in 100 \u2014 accuracy lies, recall tells the truth",
        font(F_SANS, 24), DIM, anchor="mm")
    _r.seed(31337)
    k = clamp((t - 5) / 8)
    n = int(100 * k)
    fraud = 0
    for i in range(n):
        x = 200 + (i % 20) * 45
        y = 220 + (i // 20) * 52
        is_f = (i % 37 == 0)
        if is_f:
            fraud += 1
        col = RED if is_f else TEAL
        dr.ellipse([x - 15, y - 15, x + 15, y + 15], fill=col)
    if t > 12:
        txt(dr, (W // 2, 520), "predict 'not fraud' every time \u2192 accuracy 99%",
            font(F_SANS, 25), YELLOW, anchor="mm")
        txt(dr, (W // 2, 570), "fraud caught: 0 \u2014 recall 0%",
            font(F_BOLD, 28), RED, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 620), "fix: class weights, resampling, and optimize recall \u2014 not accuracy",
            font(F_SANS, 25), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 668), "imbalanced data punishes the lazy metric \u2014 choose the metric that matters",
            font(F_SANS, 24), CREAM, anchor="mm")

# ============================================================ deep-learning (3b1b x1 + fireship x1 + bbg x1)
def scene_dl_valley(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "DESCENT INTO THE LOSS VALLEY", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "gradient descent: follow the slope downhill, one step at a time",
        font(F_SANS, 24), DIM, anchor="mm")
    ox, oy, pw, ph = 200, 600, 880, 380
    pts = []
    for i in range(100):
        x = ox + i / 99 * pw
        y = oy - ((i / 99 - 0.55) ** 2 * 4 + 0.05) * ph * 0.9
        pts.append((x, y))
    dr.line(pts, fill=DIM, width=3)
    if t > 5:
        k = clamp((t - 5) / 14)
        s = 1 - math.exp(-k * 3.2)
        sx = ox + (0.08 + 0.47 * s) * pw
        sy = oy - (((0.08 + 0.47 * s) - 0.55) ** 2 * 4 + 0.05) * ph * 0.9
        dr.ellipse([sx - 16, sy - 16, sx + 16, sy + 16], fill=YELLOW)
        dr.ellipse([sx - 24, sy - 24, sx + 24, sy + 24], outline=YELLOW, width=2)
        txt(dr, (sx, sy - 40), "w", font(F_BOLD, 24), YELLOW, anchor="mb")
    if t > 14:
        txt(dr, (W // 2, 180), "learning rate too big \u2192 bouncing over the valley",
            font(F_SANS, 24), RED, anchor="mm")
        if t > 17:
            bx = ox + 0.55 * pw + 90 * math.sin((t - 17) * 6)
            by = oy - 0.5 * ph
            dr.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=RED)
    if t > 22:
        txt(dr, (W // 2, 660), "small steps converge \u2014 the learning rate is the whole game",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_dl_backprop(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "BACKPROP IN 100 SECONDS", MAGENTA)
    lines = ["# loss L depends on w through the layers",
             "dL/dw = dL/dy \u00b7 dy/dz \u00b7 dz/dw",
             "# chain rule: multiply the local gradients",
             "for layer in reversed(model):",
             "    grad = grad * layer.local_grad()",
             "    layer.w -= lr * grad   # descend"]
    cols = [(150, 160, 190), YELLOW, (150, 160, 190),
            (200, 200, 255), (200, 200, 255), GREEN]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "backprop.py", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "credit assignment, solved \u2014 every weight learns its share of the blame",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_dl_vanish(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE GRADIENT THAT VANISHED", CYAN)
    if t > 4:
        txt(dr, (W // 2, 180), "five layers deep \u2014 the gradient shrinks at every step back",
            font(F_SANS, 25), DIM, anchor="mm")
    k = clamp((t - 5) / 10)
    for i in range(5):
        x = 200 + i * 220
        mag = (0.5 ** i) * k
        bh = 260 * mag
        dr.rectangle([x - 70, 520 - bh, x + 70, 520], fill=CYAN if mag > 0.05 else DIM)
        txt(dr, (x, 560), "L%d" % (5 - i), font(F_BOLD, 22), CREAM, anchor="mm")
        if t > 12:
            txt(dr, (x, 490 - bh), "%.3f" % (0.5 ** i), font(F_MONO, 18), DIM, anchor="mb")
    if t > 15:
        txt(dr, (W // 2, 180), "layer 1 learns nothing \u2014 the signal died in transit",
            font(F_SANS, 25), RED, anchor="mm")
    if t > 18:
        dr.line([130, 440, 1150, 440], fill=GREEN, width=4)
        txt(dr, (W // 2, 410), "residual skip: the gradient takes the express lane",
            font(F_SANS, 24), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 640), "skip connections rescue deep nets \u2014 ResNet's one great trick",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ nlp-advanced (3b1b x1 + fireship x1 + story x1)
def scene_nlpa_attn(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "ATTENTION IS ALL YOU NEED", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "the word 'it' looks back \u2014 and finds 'cat'",
        font(F_SANS, 24), DIM, anchor="mm")
    toks = ["the", "cat", "sat", "it"]
    weights = [[0.4, 0.3, 0.2, 0.1], [0.1, 0.5, 0.3, 0.1],
               [0.2, 0.2, 0.5, 0.1], [0.05, 0.75, 0.1, 0.1]]
    if t > 5:
        k = clamp((t - 5) / 8)
        nshow = int(len(toks) * k) + 1
        cell = 110
        ox0, oy0 = 440, 240
        for i in range(min(nshow, 4)):
            txt(dr, (ox0 - 60, oy0 + i * cell + cell // 2), toks[i],
                font(F_BOLD, 26), CREAM, anchor="rm")
            txt(dr, (ox0 + i * cell + cell // 2, oy0 - 40), toks[i],
                font(F_BOLD, 26), CREAM, anchor="mm")
        for i in range(min(nshow, 4)):
            for j in range(min(nshow, 4)):
                wv = weights[i][j]
                a = int(30 + 225 * wv)
                dr.rectangle([ox0 + j * cell, oy0 + i * cell,
                              ox0 + j * cell + cell - 6, oy0 + i * cell + cell - 6],
                             fill=(a, int(a * 0.55), 20))
                if wv > 0.4:
                    txt(dr, (ox0 + j * cell + cell // 2, oy0 + i * cell + cell // 2),
                        "%.2f" % wv, font(F_BOLD, 22), WHITE, anchor="mm")
    if t > 15:
        txt(dr, (W // 2, 200), "'it' \u2192 0.75 on 'cat' \u2014 the model resolved the pronoun",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 668), "attention = learned relevance \u2014 every token votes on every other",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_nlpa_transformer(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE TRANSFORMER BLOCK IN 100 SECONDS", MAGENTA)
    lines = ["# one transformer block, the whole trick",
             "x = x + attention(norm(x))     # look around",
             "x = x + mlp(norm(x))           # think alone",
             "# stack it 96 times \u2192 GPT",
             "attention: O(n\u00b2) \u2014 context windows cost quadratically",
             "that's why 1M tokens needs a datacenter"]
    cols = [(150, 160, 190), (200, 200, 255), (200, 200, 255),
            YELLOW, (200, 200, 255), ORANGE]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "block.py", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "attend, transform, repeat \u2014 the architecture that ate the world",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_nlpa_halluc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE CITATION THAT NEVER EXISTED", font(F_SERIFB, 34), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "'cite your sources,' they said \u2014 the model obliged",
            font(F_SERIF, 27), CREAM, anchor="mm")
        txt(dr, (W // 2, 270), "'Smith et al. 2019, Journal of Applied Things' \u2014 perfect format",
            font(F_MONO, 23), YELLOW, anchor="mm")
    if t > 12:
        txt(dr, (W // 2, 380), "the journal doesn't exist \u2014 Smith doesn't exist \u2014 the finding doesn't exist",
            font(F_SERIF, 26), RED, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 480), "fluency is not truth \u2014 the model predicts words, not facts",
            font(F_SERIF, 27), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 590), "verify every citation \u2014 confidence is the cheapest thing to fake",
            font(F_SERIF, 26), GOLD, anchor="mm")

# ============================================================ nlp-engineering (bbg x1 + fireship x1 + primer x1)
def scene_nlpe_token(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE WORD IS NOT THE UNIT", CYAN)
    if t > 4:
        txt(dr, (W // 2, 220), "unbelievable", font(F_BOLD, 54), CREAM, anchor="mm")
        txt(dr, (W // 2, 280), "one word \u2014 or is it?", font(F_SANS, 24), DIM, anchor="mm")
    if t > 9:
        toks = [("un", "4831"), ("believ", "20934"), ("able", "1120")]
        k = clamp((t - 9) / 5)
        for i, (tk, tid) in enumerate(toks[:int(len(toks) * k) + 1]):
            x = 380 + i * 260
            dr.rectangle([x - 110, 380, x + 110, 500], fill=(14, 22, 40), outline=CYAN, width=3)
            txt(dr, (x, 430), tk, font(F_BOLD, 32), CYAN, anchor="mm")
            txt(dr, (x, 470), "id " + tid, font(F_MONO, 22), DIM, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 580), "3 tokens \u2014 the model never saw a 'word' at all",
            font(F_SANS, 25), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "tokenizers split the world into pieces \u2014 count tokens, not words",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_nlpe_embed(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "SEARCH BY MEANING IN 100 SECONDS", MAGENTA)
    lines = ["from sentence_transformers import SentenceTransformer",
             "model = SentenceTransformer('all-MiniLM-L6-v2')",
             "vecs = model.encode(docs)          # meaning \u2192 vectors",
             "q = model.encode('refund policy')",
             "hits = cosine_sim(q, vecs).topk(3)",
             "# 'returns & exchanges' \u2014 0.91, never shared a word"]
    cols = [(200, 200, 255), (200, 200, 255), YELLOW,
            (200, 200, 255), (200, 200, 255), GREEN]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 100, 150, W - 100, 560, "semantic_search.py", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "embeddings turn meaning into geometry \u2014 near in space, near in sense",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_nlpe_rag(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "GROUNDED OR GUESSING? SCORE THE RAG", font(F_BOLD, 36), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "five chunks retrieved \u2014 the answer must cite what it used",
        font(F_SANS, 24), DIM, anchor="mm")
    chunks = [("refund policy p.3", 0.91, True), ("shipping faq", 0.62, True),
              ("blog: 2019 sale", 0.31, False), ("ceo interview", 0.22, False),
              ("unrelated pdf", 0.08, False)]
    k = clamp((t - 5) / 8)
    for i, (nm, rel, used) in enumerate(chunks[:int(len(chunks) * k) + 1]):
        y = 220 + i * 78
        bar(dr, 240, y - 18, 560, 36, rel, GREEN if used else DIM, nm, "%.2f" % rel)
        if used:
            txt(dr, (1060, y), "CITED", font(F_BOLD, 20), GREEN, anchor="lm")
    if t > 16:
        bar(dr, 240, 620, 800, 36, clamp((t - 16) / 4), TEAL, "groundedness", "94%")
    if t > 21:
        txt(dr, (W // 2, 668), "RAG without eval is a demo \u2014 score every answer against its sources",
            font(F_SANS, 24), CREAM, anchor="mm")

# ============================================================ neuroai (story x1 + 3b1b x1 + bbg x1)
def scene_nai_spike(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE NEURON THAT LEARNED TO FIRE", font(F_SERIFB, 34), GOLD, anchor="mm")
    if t > 5:
        k = clamp((t - 5) / 6)
        v = -70 + 110 * math.exp(-((k - 0.5) * 4) ** 2)
        ox, oy, pw, ph = 340, 480, 600, 200
        dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
        dr.line([ox, oy - 70 / 110 * ph * 0 + 0, ox + pw, oy], fill=DIM, width=1)
        pts = []
        for i in range(int(80 * k)):
            x = ox + i / 80 * pw
            vv = -70 + 110 * math.exp(-((i / 80 - 0.5) * 4) ** 2)
            y = oy - (vv + 70) / 110 * ph
            pts.append((x, y))
        if len(pts) > 1:
            dr.line(pts, fill=GOLD, width=4)
        txt(dr, (ox, oy - ph - 12), "membrane potential (mV)", font(F_SANS, 20), DIM, anchor="lb")
    if t > 12:
        txt(dr, (W // 2, 560), "threshold crossed \u2014 the spike travels, the synapse listens",
            font(F_SERIF, 26), YELLOW, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 620), "spiking nets compute in events \u2014 sparse, fast, brain-like",
            font(F_SERIF, 26), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 668), "the brain's language is timing \u2014 neuromorphic chips are learning to speak it",
            font(F_SERIF, 23), GOLD, anchor="mm")

def scene_nai_hebbian(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "NEURONS THAT FIRE TOGETHER, WIRE TOGETHER", font(F_BOLD, 32), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "Hebb's rule: every paired firing thickens the synapse",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        dr.ellipse([280 - 60, 330 - 60, 280 + 60, 330 + 60], fill=(14, 20, 34), outline=TEAL, width=4)
        dr.ellipse([1000 - 60, 330 - 60, 1000 + 60, 330 + 60], fill=(14, 20, 34), outline=TEAL, width=4)
        txt(dr, (280, 330), "A", font(F_BOLD, 30), WHITE, anchor="mm")
        txt(dr, (1000, 330), "B", font(F_BOLD, 30), WHITE, anchor="mm")
        k = clamp((t - 4) / 14)
        pulses = int(k * 8)
        w = 2 + pulses * 2
        dr.line([340, 330, 940, 330], fill=YELLOW, width=w)
        for p in range(pulses):
            pt = (t * 2 + p * 0.5) % 1.0
            x = 340 + pt * 600
            dr.ellipse([x - 10, 320, x + 10, 340], fill=YELLOW)
        txt(dr, (W // 2, 420), "paired firings: %d \u2014 synaptic weight %.1f\u00d7" % (pulses, 1 + pulses * 0.25),
            font(F_MONO, 24), YELLOW, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 520), "the connection is now permanent \u2014 this is memory, physically",
            font(F_SANS, 25), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 620), "Hebbian learning needs no labels \u2014 correlation is the teacher",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_nai_dropout(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "TRAINING WITH HALF THE BRAIN OFF", CYAN)
    if t > 4:
        _r.seed(2024)
        train = t < 17
        k = clamp((t - 4) / 6)
        shown = int(12 * k)
        dropped = 0
        for i in range(shown):
            x = 240 + (i % 6) * 168
            y = 300 + (i // 6) * 130
            off = train and _r.random() < 0.5
            if off:
                dropped += 1
            col = DIM if off else CYAN
            dr.ellipse([x - 44, y - 44, x + 44, y + 44], fill=(14, 20, 34), outline=col, width=4)
            txt(dr, (x, y), "\u2717" if off else "n%d" % i, font(F_BOLD, 22), col, anchor="mm")
        txt(dr, (W // 2, 580), "TRAINING: random 50% dropped each step" if train else "INFERENCE: all units on \u2014 full brain",
            font(F_SANS, 25), YELLOW if train else GREEN, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 640), "dropout forces redundancy \u2014 no neuron becomes a single point of failure",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ quant-finance-ladder (primer x1 + bbg x1 + story x1)
def scene_qfl_backtest(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE BACKTEST THAT LIED", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "beautiful in-sample \u2014 then the live market arrives",
        font(F_SANS, 24), DIM, anchor="mm")
    ox, oy, pw, ph = 200, 560, 880, 320
    dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
    sx = ox + pw * 0.62
    dr.line([sx, oy - ph, sx, oy], fill=YELLOW, width=2)
    txt(dr, (sx, oy - ph - 12), "go-live", font(F_BOLD, 20), YELLOW, anchor="mb")
    _r.seed(555)
    k = clamp((t - 5) / 14)
    pts = []
    val = 0.5
    for i in range(int(90 * k)):
        f = i / 90
        val += 0.012 if f < 0.62 else (-0.004 + _r.uniform(-0.03, 0.03))
        x = ox + f * pw
        y = oy - clamp(val, 0, 1) * ph
        pts.append((x, y))
    if len(pts) > 1:
        dr.line(pts, fill=TEAL, width=4)
    if t > 15:
        txt(dr, (ox + pw * 0.3, oy - ph + 30), "in-sample: +38%/yr", font(F_BOLD, 24), TEAL, anchor="mm")
    if t > 18:
        txt(dr, (ox + pw * 0.82, oy - ph + 60), "live: -4%/yr", font(F_BOLD, 24), RED, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "overfit strategies die in production \u2014 walk-forward or walk away",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_qfl_sharpe(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "RETURNS ARE VANITY, SHARPE IS SANITY", CYAN)
    if t > 4:
        txt(dr, (W // 2, 200), "two strategies \u2014 which one would you trust with money?",
            font(F_SANS, 25), DIM, anchor="mm")
    k = clamp((t - 6) / 6)
    bar(dr, 240, 300, 360, 56, 0.8 * k, CYAN, "A: +8% return", "vol 20%")
    bar(dr, 680, 300, 360, 56, 0.6 * k, TEAL, "B: +6% return", "vol 8%")
    if t > 13:
        bar(dr, 240, 440, 360, 56, 0.4, RED, "sharpe A", "0.40")
        bar(dr, 680, 440, 360, 56, 0.75, GREEN, "sharpe B", "0.75")
        txt(dr, (W // 2, 560), "B earns less \u2014 and keeps more of it",
            font(F_BOLD, 27), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "risk-adjusted returns decide careers \u2014 Sharpe above 1.0 gets funded",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_qfl_drawdown(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE DRAWDOWN", font(F_SERIFB, 42), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "March: the fund is up 22% \u2014 the PM is buying a boat, mentally",
            font(F_SERIF, 27), CREAM, anchor="mm")
    if t > 10:
        k = clamp((t - 10) / 6)
        bar(dr, 440, 330, 400, 44, k, RED, "drawdown", "-%d%%" % int(30 * k))
        txt(dr, (W // 2, 430), "June: down 30% from the peak \u2014 the boat is gone",
            font(F_SERIF, 26), RED, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 520), "the investors redeem \u2014 at the bottom, as always",
            font(F_SERIF, 26), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 610), "survive the drawdown and the math compounds \u2014 size positions for the worst day",
            font(F_SERIF, 26), GOLD, anchor="mm")

# ============================================================ quant-finance-math (3b1b x1 + bbg x1 + fireship x1)
def scene_qfm_normal(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE BELL CURVE AND ITS LIES", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "daily returns look normal \u2014 until the tail event arrives",
        font(F_SANS, 24), DIM, anchor="mm")
    ox, oy, pw, ph = 200, 580, 880, 360
    k = clamp((t - 5) / 8)
    pts = []
    for i in range(int(100 * k)):
        x = ox + i / 100 * pw
        z = (i / 100 - 0.5) * 6
        y = oy - math.exp(-z * z / 2) * ph
        pts.append((x, y))
    if len(pts) > 1:
        dr.line(pts, fill=TEAL, width=4)
    if t > 10:
        for s, lab in [(-1, "-1\u03c3"), (1, "+1\u03c3")]:
            x = ox + pw * (0.5 + s * 0.1667)
            dr.line([x, oy - ph, x, oy], fill=DIM, width=2)
            txt(dr, (x, oy + 24), lab, font(F_SANS, 20), DIM, anchor="mt")
        txt(dr, (W // 2, 180), "68% of days land within one sigma",
            font(F_SANS, 24), DIM, anchor="mm")
    if t > 15:
        tx = ox + pw * 0.06
        dr.polygon([(tx, oy)] + [(ox + i / 100 * pw, oy - math.exp(-((i / 100 - 0.5) * 6) ** 2 / 2) * ph)
                                for i in range(0, 12)] + [(ox + 0.12 * pw, oy)], fill=(120, 20, 20))
        txt(dr, (tx + 40, oy - 120), "the 2008 tail:\n-9\u03c3 in a day", font(F_BOLD, 22), RED, anchor="lm")
    if t > 21:
        txt(dr, (W // 2, 640), "models assume thin tails \u2014 markets deliver fat ones. plan for the tail",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_qfm_var(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "HOW MUCH CAN WE LOSE TOMORROW?", CYAN)
    if t > 4:
        ox, oy, pw, ph = 240, 520, 800, 280
        pts = [(ox + i / 80 * pw, oy - math.exp(-((i / 80 - 0.5) * 6) ** 2 / 2) * ph)
               for i in range(81)]
        dr.line(pts, fill=CYAN, width=4)
        cut = ox + pw * 0.06
        dr.line([cut, oy - ph, cut, oy], fill=RED, width=4)
        dr.polygon([(ox, oy)] + [p for p in pts if p[0] <= cut] + [(cut, oy)], fill=(120, 20, 20))
        txt(dr, (cut, oy + 28), "5% tail", font(F_BOLD, 22), RED, anchor="mt")
    if t > 12:
        txt(dr, (W // 2, 620), "VaR 95%: -$2.3M \u2014 'we are 95% sure tomorrow costs less than this'",
            font(F_MONOB, 28), YELLOW, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 668), "VaR tells you the threshold \u2014 it never tells you how bad 'bad' gets",
            font(F_SANS, 24), CREAM, anchor="mm")

def scene_qfm_mc(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "10,000 FUTURES IN 100 SECONDS", MAGENTA)
    lines = ["import numpy as np",
             "paths = np.zeros((10000, 252))",
             "for i in range(10000):",
             "    shocks = np.random.normal(0, 0.01, 252)",
             "    paths[i] = 100 * np.cumprod(1 + shocks)",
             "# median year-end: $104 \u00b7 5th pct: $71 \u2014 that's the risk"]
    cols = [(200, 200, 255), (200, 200, 255), (200, 200, 255),
            YELLOW, (200, 200, 255), GREEN]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "montecarlo.py", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "one future is a guess \u2014 ten thousand futures is a distribution",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ sql (fireship x1 + bbg x1 + primer x1)
def scene_sql_join(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "JOINS IN 100 SECONDS", MAGENTA)
    lines = ["select c.name, o.total",
             "from customers c",
             "inner join orders o on o.cust_id = c.id",
             "-- inner: only matches",
             "-- left: all customers, nulls where no order",
             "-- full: everyone, matched or not"]
    cols = [(200, 200, 255), (200, 200, 255), YELLOW,
            (150, 160, 190), (200, 200, 255), (200, 200, 255)]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "joins.sql", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "inner keeps matches \u2014 left keeps the left \u2014 draw the Venn, then query",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_sql_slow(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE QUERY THAT TOOK LUNCH", CYAN)
    if t > 4:
        txt(dr, (W // 2, 200), "10M rows \u00b7 where status = 'shipped' \u00b7 no index",
            font(F_MONO, 26), DIM, anchor="mm")
    k = clamp((t - 6) / 8)
    bar(dr, 240, 300, 800, 60, k, RED, "sequential scan", "%ds" % int(47 * k))
    if t > 14:
        bar(dr, 240, 430, 800, 60, clamp((t - 14) / 3), GREEN, "with index", "0.2s")
        txt(dr, (W // 2, 560), "create index on orders(status) \u2014 47s becomes 0.2s",
            font(F_MONO, 26), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "EXPLAIN ANALYZE before you optimize \u2014 the plan tells you where it hurts",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_sql_window(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE RUNNING TOTAL THAT SLIDES", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "window functions: compute across rows without collapsing them",
        font(F_SANS, 24), DIM, anchor="mm")
    sales = [120, 200, 150, 300, 250, 400]
    k = clamp((t - 5) / 8)
    nshow = int(len(sales) * k)
    run = 0
    for i in range(nshow):
        run += sales[i]
        x = 240 + i * 140
        dr.rectangle([x, 300, x + 110, 440], fill=(14, 20, 34), outline=TEAL, width=3)
        txt(dr, (x + 55, 350), "$%d" % sales[i], font(F_BOLD, 24), CREAM, anchor="mm")
        txt(dr, (x + 55, 400), "\u03a3 $%d" % run, font(F_MONO, 20), GREEN, anchor="mm")
    if t > 14:
        fx = 240 + clamp((t - 14) / 6) * (len(sales) - 1) * 140
        dr.rectangle([fx - 70, 280, fx + 180, 460], outline=YELLOW, width=4)
        txt(dr, (W // 2, 540), "sum(amount) over (order by day) \u2014 the frame slides, rows survive",
            font(F_MONO, 24), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "windows aggregate without GROUP BY \u2014 running totals, ranks, moving averages",
            font(F_SANS, 25), CREAM, anchor="mm")

SLUG_DIR = {
    "da": "data-analyst", "daml": "data-analyst-to-ml",
    "de": "data-engineering", "dsc": "data-science-certs",
    "dsml": "datascience-ml", "dl": "deep-learning",
    "nlpa": "nlp-advanced", "nlpe": "nlp-engineering",
    "nai": "neuroai", "qfl": "quant-finance-ladder",
    "qfm": "quant-finance-math", "sql": "sql",
}

# ============================================================ VIDEOS registry
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    "da": "DATA ANALYST \u00b7 Dashboards, SQL & Storytelling",
    "daml": "ANALYST\u2192ML \u00b7 From Dashboards to Models",
    "de": "DATA ENG \u00b7 Pipelines at Scale",
    "dsc": "DS CERTS \u00b7 The Certification Playbook",
    "dsml": "DATA SCIENCE \u00b7 ML in Production",
    "dl": "DEEP LEARNING \u00b7 Neural Networks",
    "nlpa": "NLP ADVANCED \u00b7 Language Models",
    "nlpe": "NLP ENG \u00b7 Shipping Language Systems",
    "nai": "NEUROAI \u00b7 Brain-Inspired Computing",
    "qfl": "QUANT LADDER \u00b7 The Finance Career Path",
    "qfm": "QUANT MATH \u00b7 The Math of Markets",
    "sql": "SQL \u00b7 Query Mastery",
}

VIDEOS = [
 # --- data-analyst
 V(BOOTCAMP_K["da"], "da", "da-dirty-triage", "The Dirty Data Triage",
   "triage it like a pro", "bbg", scene_da_dirty,
   "Six rows land on the desk and four lie: missing values get the median, duplicates get dropped, typos get normalized \u2014 triage before analysis.",
   [(4,10,"Six rows land \u2014 four of them lie"),
    (10,16,"Missing, impossible, duplicate, typo \u2014 name the disease"),
    (16,22,"Median for missing \u00b7 drop the dupes \u00b7 normalize the typos"),
    (22,26,"Analysts spend 80% of the job cleaning \u2014 triage it like a pro")]),
 V(BOOTCAMP_K["da"], "da", "da-mean-median", "The Average That Lies",
   "the mean is a hostage", "3b1b", scene_da_skew,
   "Ten salaries, one CEO: the mean runs to $148k while the median holds at $62k \u2014 on skewed data, report the median.",
   [(4,10,"Ten salaries \u2014 the distribution leans right"),
    (10,16,"The median sits at $62k \u00b7 the mean starts drifting"),
    (16,22,"One billionaire moves the mean $86k \u2014 the median doesn't flinch"),
    (22,26,"Skewed data? Report the median \u2014 the mean is a hostage")]),
 V(BOOTCAMP_K["da"], "da", "da-pandas-oneliner", "The Pandas One-Liner in 100 Seconds",
   "five lines, eighty percent of the job", "fireship", scene_da_pandas,
   "Read the CSV, drop the nulls and dupes, group by region, sort \u2014 eighty percent of analyst work in five lines of pandas.",
   [(4,10,"Read the CSV \u2014 drop nulls, drop duplicates"),
    (10,16,"Group by region \u00b7 sum the revenue"),
    (16,22,"Sort descending \u00b7 take the top three"),
    (22,26,"West $4.2M, east $3.8M, north $2.1M \u2014 done")]),
 # --- data-analyst-to-ml
 V(BOOTCAMP_K["daml"], "daml", "daml-train-test", "The Test Set You Never Touch",
   "lock it away", "bbg", scene_daml_split,
   "One thousand labeled rows split 80/20 before training: the model learns on teal, the orange stays sealed \u2014 peek and your score is fiction.",
   [(4,10,"One thousand rows \u2014 split before you train"),
    (10,16,"Eighty percent teal for training \u00b7 twenty percent orange, sealed"),
    (16,22,"The model never sees orange until the final exam"),
    (22,26,"Peek at the test set and your score is fiction \u2014 lock it away")]),
 V(BOOTCAMP_K["daml"], "daml", "daml-overfit", "The Model That Memorized the Exam",
   "the sweet spot generalizes", "primer", scene_daml_overfit,
   "As complexity rises, training error falls but test error turns \u2014 past the sweet spot the model memorizes and the test pays for it.",
   [(4,10,"Complexity rises \u2014 training error falls"),
    (10,16,"Test error falls too \u2026 then turns upward"),
    (16,22,"The sweet spot: complex enough to learn, simple enough to generalize"),
    (22,26,"Past it, the model memorizes \u2014 and the test pays for it")]),
 V(BOOTCAMP_K["daml"], "daml", "daml-first-model", "Your First Model in 100 Seconds",
   "fit, predict, score", "fireship", scene_daml_model,
   "A random forest in six lines: fit on the train split, predict on the test split, score 0.91 \u2014 your first model beats a coin flip.",
   [(4,10,"RandomForest, one hundred trees \u2014 declared"),
    (10,16,"Fit: the model learns the training split"),
    (16,22,"Predict: guesses on the sealed test split \u00b7 score 0.91"),
    (22,26,"Fit, predict, score \u2014 the whole ritual in six lines")]),
 # --- data-engineering
 V(BOOTCAMP_K["de"], "de", "de-pipeline-retry", "The Pipeline That Refused to Die",
   "design the retry before the page", "bbg", scene_de_retry,
   "Extract, transform, load \u2014 transform fails at 3 AM: exponential backoff retries, attempt four succeeds. Idempotent tasks heal.",
   [(4,10,"Extract, transform, load \u2014 the nightly pipeline"),
    (10,16,"Transform fails \u2014 attempt one, two, three, backing off"),
    (16,22,"Attempt four: success \u2014 the pipeline healed itself"),
    (22,26,"Everything fails at 3 AM \u2014 design the retry before the page")]),
 V(BOOTCAMP_K["de"], "de", "de-dbt-model", "The dbt Model in 100 Seconds",
   "the warehouse grows up", "fireship", scene_de_dbt,
   "A dbt model: select from the raw ref, coalesce the discounts, kill the refunds \u2014 SQL with tests and lineage.",
   [(4,10,"The model file: orders_clean.sql"),
    (10,16,"Select, coalesce the discounts \u2014 handle the nulls"),
    (16,22,"Reference the raw table \u00b7 filter the refunds"),
    (22,26,"SQL with tests and lineage \u2014 the warehouse grows up")]),
 V(BOOTCAMP_K["de"], "de", "de-schema-drift", "The Column That Appeared Overnight",
   "surprise is optional", "primer", scene_de_drift,
   "Monday to Thursday the schema holds; Friday a signup_source column appears \u2014 the contract check bumps to schema v2 before dashboards break.",
   [(4,10,"Monday to Thursday: three columns, stable"),
    (10,16,"Friday: a fourth column appears \u2014 signup_source"),
    (16,22,"The contract check fires \u2014 schema v2, dashboards warned"),
    (22,26,"Schema drift is inevitable \u2014 surprise is optional")]),
 # --- data-science-certs
 V(BOOTCAMP_K["dsc"], "dsc", "dsc-exam-day", "Exam Day",
   "the hours are the credential", "story", scene_dsc_exam,
   "7:58 AM at the testing center: sixty questions, four hundred hours of study \u2014 the p-value question makes you smile. The cert is paper; the hours are the credential.",
   [(4,10,"7:58 AM \u2014 the testing center smells like carpet and nerves"),
    (10,16,"Sixty questions \u2014 four hundred hours behind them"),
    (16,22,"Question 41: the p-value question \u2014 you know this one"),
    (22,26,"Pass \u2014 the hours are the real credential")]),
 V(BOOTCAMP_K["dsc"], "dsc", "dsc-ab-test", "Ship It or Kill It: The A/B Test",
   "the test decides, not your hope", "bbg", scene_dsc_ab,
   "Control at 4.2%, treatment climbing \u2014 the p-value crosses 0.05 and the lift is real. No peeking early, no p-hacking: the test decides.",
   [(4,10,"Control vs treatment \u2014 ten thousand users each"),
    (10,16,"Treatment climbs \u00b7 the p-value falls"),
    (16,22,"Below 0.05 \u2014 the lift is real, ship it"),
    (22,26,"No p-hacking, no peeking \u2014 the test decides, not your hope")]),
 V(BOOTCAMP_K["dsc"], "dsc", "dsc-resume-bullets", "Resume Bullets That Get Interviews",
   "metrics are the proof", "fireship", scene_dsc_resume,
   "Weak: 'worked with data.' Strong: cut report runtime 6h to 20min, 40 experiments a year, dashboard adopted by 200 sellers \u2014 numbers are the verbs.",
   [(4,10,"Weak: 'worked with data' \u2014 strong: quantified"),
    (10,16,"Cut runtime six hours to twenty minutes"),
    (16,22,"Forty experiments a year \u00b7 two hundred dashboard users"),
    (22,26,"Action, scale, outcome \u2014 or the bullet doesn't ship")]),
 # --- datascience-ml
 V(BOOTCAMP_K["dsml"], "dsml", "dsml-bias-variance", "Bias, Variance, and the Sweet Spot",
   "the middle generalizes", "3b1b", scene_dsml_biasvar,
   "Total error is bias squared plus variance plus noise: too simple is blind, too complex is paranoid \u2014 the sweet spot generalizes.",
   [(4,10,"Total error = bias squared + variance + noise"),
    (10,16,"Bias falls with complexity \u00b7 variance rises"),
    (16,22,"The total dips \u2014 then climbs: the sweet spot"),
    (22,26,"Too simple: blind \u00b7 too complex: paranoid \u2014 the middle generalizes")]),
 V(BOOTCAMP_K["dsml"], "dsml", "dsml-feature-leak", "The 99.8% That Was a Lie",
   "audit every feature's timestamp", "bbg", scene_dsml_leak,
   "Churn model at 99.8% accuracy \u2014 too good to be true: cancel_date only exists after churn. Drop it and the score falls to 71%, honestly.",
   [(4,10,"Five features \u2014 one of them knows the future"),
    (10,16,"Accuracy 99.8% \u2014 too good to be true is too good"),
    (16,22,"cancel_date exists only AFTER churn \u2014 drop it: 71%"),
    (22,26,"If it's too good, it's leaking \u2014 audit every feature's timestamp")]),
 V(BOOTCAMP_K["dsml"], "dsml", "dsml-imbalance", "99% Accurate, 100% Useless",
   "choose the metric that matters", "primer", scene_dsml_imbalance,
   "Fraud is 1 in 100: predict 'not fraud' always and accuracy hits 99% while recall is zero \u2014 class weights and recall fix the lie.",
   [(4,10,"One hundred transactions \u2014 one is fraud"),
    (10,16,"Predict 'not fraud' every time \u2014 accuracy 99%"),
    (16,22,"Fraud caught: zero \u2014 recall 0%"),
    (22,26,"Optimize recall, not accuracy \u2014 choose the metric that matters")]),
 # --- deep-learning
 V(BOOTCAMP_K["dl"], "dl", "dl-loss-valley", "Descent Into the Loss Valley",
   "the learning rate is the whole game", "3b1b", scene_dl_valley,
   "Gradient descent walks the loss valley: small steps converge on the minimum, a big learning rate bounces over it \u2014 the rate is the whole game.",
   [(4,10,"The loss valley \u2014 the weight starts high on the slope"),
    (10,16,"Small steps downhill \u00b7 the loss falls every step"),
    (16,22,"Learning rate too big \u2014 bouncing over the valley"),
    (22,26,"Small steps converge \u2014 the learning rate is the whole game")]),
 V(BOOTCAMP_K["dl"], "dl", "dl-backprop", "Backprop in 100 Seconds",
   "every weight learns its blame", "fireship", scene_dl_backprop,
   "Backprop is the chain rule at scale: multiply the local gradients backward through the layers, then descend \u2014 credit assignment, solved.",
   [(4,10,"The loss depends on the weights through the layers"),
    (10,16,"Chain rule: multiply the local gradients"),
    (16,22,"Walk the layers in reverse \u2014 update every weight"),
    (22,26,"Credit assignment, solved \u2014 every weight learns its share of the blame")]),
 V(BOOTCAMP_K["dl"], "dl", "dl-vanishing", "The Gradient That Vanished",
   "ResNet's one great trick", "bbg", scene_dl_vanish,
   "Five layers deep and the gradient halves at every step back \u2014 layer one learns nothing. The residual skip gives it an express lane.",
   [(4,10,"Five layers \u2014 the gradient shrinks going back"),
    (10,16,"Halved, halved, halved \u2014 layer one gets crumbs"),
    (16,22,"The skip connection: an express lane for the gradient"),
    (22,26,"Skip connections rescue deep nets \u2014 ResNet's one great trick")]),
 # --- nlp-advanced
 V(BOOTCAMP_K["nlpa"], "nlpa", "nlpa-attention", "Attention Is All You Need",
   "every token votes on every other", "3b1b", scene_nlpa_attn,
   "The attention heatmap for 'the cat sat / it': the word 'it' puts 0.75 weight on 'cat' \u2014 the model resolved the pronoun. Attention is learned relevance.",
   [(4,10,"Four tokens \u2014 the attention grid fills in"),
    (10,16,"Every token scores every other token"),
    (16,22,"'it' puts 0.75 on 'cat' \u2014 the pronoun is resolved"),
    (22,26,"Attention = learned relevance \u2014 every token votes on every other")]),
 V(BOOTCAMP_K["nlpa"], "nlpa", "nlpa-transformer-block", "The Transformer Block in 100 Seconds",
   "the architecture that ate the world", "fireship", scene_nlpa_transformer,
   "One transformer block: attend, add, normalize, MLP, add \u2014 stack it 96 times and you have GPT. Attention costs quadratically, so context needs datacenters.",
   [(4,10,"The block: attention plus residual, MLP plus residual"),
    (10,16,"Attend: look around \u00b7 MLP: think alone"),
    (16,22,"Stack it 96 times \u2014 that's GPT"),
    (22,26,"Attention is O(n squared) \u2014 a million tokens needs a datacenter")]),
 V(BOOTCAMP_K["nlpa"], "nlpa", "nlpa-hallucination", "The Citation That Never Existed",
   "confidence is the cheapest thing to fake", "story", scene_nlpa_halluc,
   "Asked for sources, the model invents 'Smith et al. 2019' in perfect format \u2014 the journal, the author, the finding: none exist. Fluency is not truth.",
   [(4,10,"'Cite your sources' \u2014 the model obliges"),
    (10,16,"Perfect format: Smith et al. 2019, Journal of Applied Things"),
    (16,22,"The journal doesn't exist \u00b7 Smith doesn't exist"),
    (22,26,"Verify every citation \u2014 confidence is the cheapest thing to fake")]),
 # --- nlp-engineering
 V(BOOTCAMP_K["nlpe"], "nlpe", "nlpe-tokenizer", "The Word Is Not the Unit",
   "count tokens, not words", "bbg", scene_nlpe_token,
   "'Unbelievable' is one word and three tokens: un, believ, able \u2014 the model never saw a word at all. Tokenizers split the world; count tokens, not words.",
   [(4,10,"Unbelievable \u2014 one word, or is it?"),
    (10,16,"The tokenizer splits: un \u00b7 believ \u00b7 able"),
    (16,22,"Three token IDs \u2014 the model never saw a word"),
    (22,26,"Tokenizers split the world \u2014 count tokens, not words")]),
 V(BOOTCAMP_K["nlpe"], "nlpe", "nlpe-embeddings", "Search by Meaning in 100 Seconds",
   "near in space, near in sense", "fireship", scene_nlpe_embed,
   "Encode docs to vectors, encode the query, cosine-similarity the top three: 'returns & exchanges' matches 'refund policy' at 0.91 without sharing a word.",
   [(4,10,"Encode the documents \u2014 meaning becomes vectors"),
    (10,16,"Encode the query \u2014 one more vector"),
    (16,22,"Cosine similarity \u00b7 top three hits"),
    (22,26,"'Returns & exchanges' at 0.91 \u2014 never shared a word with the query")]),
 V(BOOTCAMP_K["nlpe"], "nlpe", "nlpe-rag-eval", "Grounded or Guessing? Score the RAG",
   "score every answer", "primer", scene_nlpe_rag,
   "Five chunks retrieved, two cited, groundedness 94%: RAG without eval is a demo \u2014 score every answer against the sources it used.",
   [(4,10,"Five chunks retrieved \u2014 relevance scored"),
    (10,16,"Two chunks cited \u00b7 three ignored"),
    (16,22,"Groundedness: 94% \u2014 the answer used its sources"),
    (22,26,"RAG without eval is a demo \u2014 score every answer against its sources")]),
 # --- neuroai
 V(BOOTCAMP_K["nai"], "nai", "nai-spike", "The Neuron That Learned to Fire",
   "the brain's language is timing", "story", scene_nai_spike,
   "The membrane potential climbs, crosses threshold, and spikes \u2014 spiking networks compute in events: sparse, fast, brain-like.",
   [(4,10,"The membrane potential climbs toward threshold"),
    (10,16,"Threshold crossed \u2014 the spike fires"),
    (16,22,"The spike travels \u00b7 the synapse listens"),
    (22,26,"Spiking nets compute in events \u2014 the brain's language is timing")]),
 V(BOOTCAMP_K["nai"], "nai", "nai-hebbian", "Neurons That Fire Together, Wire Together",
   "correlation is the teacher", "3b1b", scene_nai_hebbian,
   "Hebb's rule in motion: every paired firing of A and B thickens their synapse \u2014 eight pulses, double the weight. This is memory, physically.",
   [(4,10,"Neuron A and neuron B \u2014 a thin connection"),
    (10,16,"Paired firings \u00b7 the synapse thickens with each pulse"),
    (16,22,"Eight pulses \u2014 the weight has doubled"),
    (22,26,"The connection is permanent \u2014 this is memory, physically")]),
 V(BOOTCAMP_K["nai"], "nai", "nai-dropout", "Training With Half the Brain Off",
   "no single point of failure", "bbg", scene_nai_dropout,
   "Training drops a random 50% of units each step; at inference the full brain switches on \u2014 dropout forces redundancy, no neuron becomes load-bearing.",
   [(4,10,"Twelve units \u2014 training begins"),
    (10,16,"Random half dropped every step \u00b7 the net adapts"),
    (16,22,"Inference: all units on \u2014 the full brain"),
    (22,26,"Dropout forces redundancy \u2014 no neuron becomes a single point of failure")]),
 # --- quant-finance-ladder
 V(BOOTCAMP_K["qfl"], "qfl", "qfl-backtest-lie", "The Backtest That Lied",
   "walk-forward or walk away", "primer", scene_qfl_backtest,
   "In-sample: +38% a year. Go-live: -4%. The backtest was overfit to history \u2014 walk-forward validation or walk away from the strategy.",
   [(4,10,"The equity curve climbs \u2014 beautiful in-sample"),
    (10,16,"In-sample: +38% a year \u00b7 then go-live"),
    (16,22,"Live: -4% a year \u2014 the curve was a mirage"),
    (22,26,"Overfit strategies die in production \u2014 walk-forward or walk away")]),
 V(BOOTCAMP_K["qfl"], "qfl", "qfl-sharpe", "Returns Are Vanity, Sharpe Is Sanity",
   "Sharpe above 1.0 gets funded", "bbg", scene_qfl_sharpe,
   "Strategy A returns 8% with 20% volatility; B returns 6% with 8% \u2014 Sharpe 0.40 vs 0.75. B earns less and keeps more of it.",
   [(4,10,"Two strategies \u2014 which would you trust with money?"),
    (10,16,"A: +8% return, 20% vol \u00b7 B: +6% return, 8% vol"),
    (16,22,"Sharpe: A 0.40 \u00b7 B 0.75 \u2014 B keeps more of it"),
    (22,26,"Risk-adjusted returns decide careers \u2014 Sharpe above 1.0 gets funded")]),
 V(BOOTCAMP_K["qfl"], "qfl", "qfl-drawdown", "The Drawdown",
   "size positions for the worst day", "story", scene_qfl_drawdown,
   "March: up 22%, the PM is mentally buying a boat. June: down 30% from the peak, investors redeem at the bottom \u2014 size for the worst day.",
   [(4,10,"March: up 22% \u2014 the boat is being mentally purchased"),
    (10,16,"June: down 30% from the peak \u2014 the boat is gone"),
    (16,22,"Investors redeem \u2014 at the bottom, as always"),
    (22,26,"Survive the drawdown and the math compounds \u2014 size for the worst day")]),
 # --- quant-finance-math
 V(BOOTCAMP_K["qfm"], "qfm", "qfm-bell-curve", "The Bell Curve and Its Lies",
   "plan for the tail", "3b1b", scene_qfm_normal,
   "Daily returns look normal until the tail event: 68% of days inside one sigma, then a -9 sigma day in 2008 \u2014 models assume thin tails, markets deliver fat ones.",
   [(4,10,"Daily returns \u2014 the bell curve forms"),
    (10,16,"68% of days land within one sigma"),
    (16,22,"Then 2008: a -9 sigma day \u2014 the fat tail"),
    (22,26,"Models assume thin tails \u2014 markets deliver fat ones. Plan for the tail")]),
 V(BOOTCAMP_K["qfm"], "qfm", "qfm-var", "How Much Can We Lose Tomorrow?",
   "VaR never tells you how bad 'bad' gets", "bbg", scene_qfm_var,
   "Value at Risk 95%: -$2.3M \u2014 we are 95% sure tomorrow costs less than this. But VaR names the threshold, never the depth of the tail beyond it.",
   [(4,10,"The return distribution \u2014 the 5% tail is shaded"),
    (10,16,"The cut line: 95% of days are better than this"),
    (16,22,"VaR 95%: -$2.3M \u2014 tomorrow costs less than this, probably"),
    (22,26,"VaR names the threshold \u2014 never how bad 'bad' gets")]),
 V(BOOTCAMP_K["qfm"], "qfm", "qfm-monte-carlo", "10,000 Futures in 100 Seconds",
   "ten thousand futures is a distribution", "fireship", scene_qfm_mc,
   "Ten thousand simulated years: median year-end $104, 5th percentile $71 \u2014 one future is a guess, ten thousand futures is a distribution.",
   [(4,10,"Ten thousand paths \u00b7 252 trading days each"),
    (10,16,"Random shocks compound \u2014 the fan spreads"),
    (16,22,"Median year-end: $104 \u00b7 5th percentile: $71"),
    (22,26,"One future is a guess \u2014 ten thousand futures is a distribution")]),
 # --- sql
 V(BOOTCAMP_K["sql"], "sql", "sql-joins", "Joins in 100 Seconds",
   "draw the Venn, then query", "fireship", scene_sql_join,
   "Inner keeps the matches, left keeps the left table, full keeps everyone \u2014 draw the Venn diagram, then write the query.",
   [(4,10,"Customers join orders \u2014 the ON clause is the handshake"),
    (10,16,"Inner: only matches survive"),
    (16,22,"Left: all customers \u00b7 full: everyone, matched or not"),
    (22,26,"Inner keeps matches \u2014 left keeps the left \u2014 draw the Venn, then query")]),
 V(BOOTCAMP_K["sql"], "sql", "sql-slow-query", "The Query That Took Lunch",
   "the plan tells you where it hurts", "bbg", scene_sql_slow,
   "Ten million rows, no index: 47 seconds of sequential scan. One CREATE INDEX later: 0.2 seconds \u2014 EXPLAIN ANALYZE before you optimize.",
   [(4,10,"Ten million rows \u00b7 no index \u00b7 sequential scan"),
    (10,16,"47 seconds \u2014 the query took lunch"),
    (16,22,"One index later: 0.2 seconds"),
    (22,26,"EXPLAIN ANALYZE first \u2014 the plan tells you where it hurts")]),
 V(BOOTCAMP_K["sql"], "sql", "sql-window-frame", "The Running Total That Slides",
   "windows without GROUP BY", "primer", scene_sql_window,
   "sum(amount) over (order by day): the frame slides across rows computing running totals \u2014 aggregation without collapsing the rows.",
   [(4,10,"Six daily sales \u2014 no GROUP BY in sight"),
    (10,16,"The running total accumulates \u00b7 rows survive"),
    (16,22,"The window frame slides \u2014 sum over order by day"),
    (22,26,"Windows aggregate without collapsing \u2014 totals, ranks, moving averages")]),
]

# ============================================================ render loop (mirrors gen_bootcamp_b3)
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
