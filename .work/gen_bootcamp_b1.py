#!/usr/bin/env python3
"""Bootcamp video Phase 2, Batch B1: 10 acad-* bootcamps x 3 videos = 30 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Mirrors gen_batch4.py: imports helpers from gen_batch1.

Filenames are bc- prefixed so they never collide with course videos.
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

def cl(lines, col=(200, 200, 255)):
    """Wrap plain strings as (code, color) tuples for code_panel."""
    return [(s, col) for s in lines]

def warm_rings(dr):
    for r in range(340, 0, -25):
        c = int(lerp(8, 42, r / 340))
        dr.ellipse([W // 2 - r, H // 2 - r, W // 2 + r, H // 2 + r],
                   outline=(c + 14, c + 5, c - 3), width=2)

# ============================================================ acad-career: Career (story x2 + fireship x1)
def scene_lowball(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE LOWBALL OFFER", font(F_SERIFB, 44), GOLD, anchor="mm")
    k1 = clamp((t - 5) / 3)
    bar(dr, 260, 220, 760, 52, k1 * 0.62, (150, 90, 60), "their offer", "$85k")
    k2 = clamp((t - 9) / 3)
    bar(dr, 260, 340, 760, 52, k2 * 0.92, GOLD, "your anchor (research-backed)", "$120k")
    if t > 13:
        txt(dr, (W // 2, 460), "the first number is never the last number",
            font(F_SERIF, 30), CREAM, anchor="mm")
    if t > 18:
        for i, w_ in enumerate(["know your range", "state your BATNA", "ask, then wait"]):
            y = 520 + i * 44
            dr.ellipse([300 - 8, y - 8, 300 + 8, y + 8], fill=GOLD)
            txt(dr, (330, y), w_, font(F_SERIF, 26), (200, 185, 160), anchor="lm")
    if t > 24:
        txt(dr, (W // 2, 640), "negotiation is information \u2014 prepare before you speak",
            font(F_SERIF, 26), GOLD, anchor="mm")

def scene_negotiation(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "NEGOTIATION LEVERAGE", MAGENTA)
    lines = ["# the 3 numbers that win salary talks", "BATNA  = best alternative to no agreement",
             "anchor = the first number (make it yours)", "range  = zone of possible agreement"]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 180, 150, W - 180, 560, "leverage.py", cl(lines), hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "anchor high, justify with data, stay silent after",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_cold_email(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE NETWORKING COLD EMAIL", font(F_SERIFB, 40), GOLD, anchor="mm")
    k = clamp((t - 5) / 4)
    ex, ey = W // 2, 330
    dr.rectangle([ex - 150, ey - 90, ex + 150, ey + 90], fill=(24, 20, 14), outline=GOLD, width=3)
    flap = int(90 * (1 - k))
    dr.polygon([(ex - 150, ey - 90), (ex + 150, ey - 90), (ex, ey - 90 + flap)], fill=(40, 32, 18))
    if t > 10:
        n = min(5, int((t - 10) / 1.2) + 1)
        for i in range(n):
            lx = ex - 240 + i * 120
            ly = ey - 200 - (int((t - 10 - i * 1.2) * 22) % 60)
            glow_box(dr, [lx - 40, ly - 26, lx + 40, ly + 26], GOLD, rad=6, layers=2)
            txt(dr, (lx, ly), "?", font(F_SERIFB, 28), CREAM, anchor="mm")
    if t > 16:
        k2 = clamp((t - 16) / 4)
        bar(dr, 340, 480, 600, 46, k2 * 0.38, TEAL, "reply rate of a great cold email", "38%")
    if t > 22:
        txt(dr, (W // 2, 590), "specific, short, curious \u2014 never ask for a job",
            font(F_SERIF, 28), CREAM, anchor="mm")

# ============================================================ acad-cloud: Cloud (bbg x2 + fireship x1)
def scene_surprise_bill(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE SURPRISE BILL", CYAN)
    svcs = [("compute", 0.72, 5, "$18,400"), ("storage", 0.35, 8, "$4,100"),
            ("egress", 0.55, 11, "$9,700"), ("idle VMs", 0.28, 14, "$3,300")]
    for i, (nm, frac, born, val) in enumerate(svcs):
        if t < born:
            continue
        k = clamp((t - born) / 2.5)
        y = 200 + i * 92
        hot = nm == "idle VMs"
        bar(dr, 300, y, 680, 46, k * frac, RED if hot else CYAN, nm, val)
        if hot and t > born + 2.5:
            txt(dr, (300, y + 56), "\u2190 40% of spend, 0 traffic \u2014 FinOps kill #1",
                font(F_SANS, 22), RED, anchor="lb")
    if t > 22:
        txt(dr, (W // 2, 620), "tag everything \u00b7 alert on anomaly \u00b7 shut down the idle",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_failover(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "REGION FAILOVER DRILL", CYAN)
    def region(x, label, live):
        col = GREEN if live else RED
        glow_box(dr, [x - 190, 210, x + 190, 430], col, rad=12, layers=2)
        dr.rectangle([x - 190, 210, x + 190, 430], fill=(10, 16, 28))
        txt(dr, (x, 250), label, font(F_BOLD, 30), WHITE, anchor="mm")
        st = "HEALTHY" if (live or t < 8) else "FAILED"
        txt(dr, (x, 330), st, font(F_MONOB, 34), GREEN if st == "HEALTHY" else RED, anchor="mm")
        tr = "100%" if (live or t < 8) else "0%"
        txt(dr, (x, 390), "traffic: " + tr, font(F_SANS, 24), DIM, anchor="mm")
    region(340, "us-east-1 (primary)", False)
    region(940, "us-west-2 (standby)", True)
    if t > 8:
        k = clamp((t - 8) / 3)
        arrow(dr, 540, 320, 740, 320, GREEN if k >= 1 else YELLOW, 8)
        txt(dr, (640, 290), "failover", font(F_BOLD, 24), GREEN, anchor="mm")
        pulse = 0.5 + 0.5 * math.sin(t * 4)
        txt(dr, (940, 470), "RTO 5 min \u00b7 RPO 0",
            font(F_SANS, 26), (int(120 + 120 * pulse), 255, int(120 + 120 * pulse)), anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 600), "game-day the failover before you need the failover",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_shared_resp(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "SHARED RESPONSIBILITY", MAGENTA)
    rows = [("IaaS", "you patch the OS", 5, CYAN), ("PaaS", "you secure the app", 10, TEAL),
            ("SaaS", "you guard the data", 15, MAGENTA)]
    for i, (nm, you, born, col) in enumerate(rows):
        if t < born:
            continue
        y = 190 + i * 110
        panel(dr, [180, y, W - 180, y + 90], nm, col)
        txt(dr, (210, y + 45), "cloud: hardware \u00b7 network \u00b7 hypervisor",
            font(F_SANS, 24), DIM, anchor="lm")
        txt(dr, (W - 210, y + 45), "YOU: " + you, font(F_BOLD, 24), col, anchor="rm")
    if t > 22:
        txt(dr, (W // 2, 560), "the cloud secures OF itself \u2014 you secure what is IN it",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ acad-command: Command (story x2 + bbg x1)
def scene_3am(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE 3 AM PAGE", font(F_SERIFB, 44), GOLD, anchor="mm")
    k = clamp((t - 5) / 2)
    glow_box(dr, [W // 2 - 200, 170, W // 2 + 200, 320], RED if k > 0.5 else GOLD, rad=14, layers=2)
    dr.rectangle([W // 2 - 200, 170, W // 2 + 200, 320], fill=(30, 10, 8))
    txt(dr, (W // 2, 220), "PAGER", font(F_BOLD, 30), RED, anchor="mm")
    txt(dr, (W // 2, 270), "checkout latency > 2000ms", font(F_MONO, 26), CREAM, anchor="mm")
    if t > 10:
        roles = [("Incident Commander", "declares, coordinates"), ("Ops Lead", "fingers on keys"),
                 ("Comms", "one voice outward")]
        for i, (r_, d) in enumerate(roles):
            y = 380 + i * 70
            dr.ellipse([230 - 10, y - 10, 230 + 10, y + 10], fill=GOLD)
            txt(dr, (265, y - 12), r_, font(F_SERIFB, 28), CREAM, anchor="lm")
            txt(dr, (265, y + 20), d, font(F_SERIF, 24), (200, 185, 160), anchor="lm")
    if t > 22:
        txt(dr, (W // 2, 630), "command is calm \u2014 the page is the job",
            font(F_SERIF, 28), GOLD, anchor="mm")

def scene_deploy_rollback(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "DEPLOY OR ROLLBACK?", CYAN)
    if t > 4:
        txt(dr, (W // 2, 200), "error budget burning?", font(F_BOLD, 32), WHITE, anchor="mm")
    if t > 8:
        arrow(dr, W // 2, 250, 380, 330, YELLOW, 5)
        panel(dr, [180, 330, 580, 470], "ROLLBACK", YELLOW)
        txt(dr, (380, 420), "safe path", font(F_SANS, 24), DIM, anchor="mm")
        arrow(dr, W // 2, 250, 900, 330, RED, 5)
        panel(dr, [700, 330, 1100, 470], "ROLL FORWARD", RED)
        txt(dr, (900, 420), "only with a proven fix", font(F_SANS, 24), DIM, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 530), "uncertainty is the input \u2014 the tree decides, not your gut",
            font(F_SANS, 26), CREAM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 600), "rule: canary red for 10 min \u2192 rollback, no debate",
            font(F_MONOB, 26), GREEN, anchor="mm")

def scene_postmortem(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE BLAMELESS POSTMORTEM", font(F_SERIFB, 38), GOLD, anchor="mm")
    evts = [("02:14", "deploy v2.4.1 ships", 5), ("02:41", "latency alarms fire", 9),
            ("03:05", "rollback completes", 13), ("10:00", "blameless review", 17)]
    for i, (tm, ev, born) in enumerate(evts):
        if t < born:
            continue
        y = 200 + i * 92
        txt(dr, (300, y), tm, font(F_MONOB, 28), GOLD, anchor="mm")
        dr.line([430, y - 6, 430, y + 6], fill=GOLD, width=4)
        txt(dr, (460, y), ev, font(F_SERIF, 28), CREAM, anchor="lm")
    if t > 21:
        txt(dr, (W // 2, 600), "blame fixes nothing \u2014 systems fail, people learn",
            font(F_SERIF, 28), GOLD, anchor="mm")

# ============================================================ acad-cyber: Cyber (bbg x2 + fireship x1)
def scene_phishing(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE 2 AM PHISHING REPORT", CYAN)
    stages = [("report", 5), ("triage", 9), ("isolate", 13), ("hunt", 17)]
    n = sum(1 for _, born in stages if t >= born)
    for i, (nm, born) in enumerate(stages):
        if t < born:
            continue
        x = 200 + i * 293
        col = GREEN if i < n - 1 else CYAN
        glow_box(dr, [x - 110, 300, x + 110, 430], col, rad=10, layers=2)
        dr.rectangle([x - 110, 300, x + 110, 430], fill=(10, 16, 28))
        txt(dr, (x, 365), nm.upper(), font(F_BOLD, 28), WHITE, anchor="mm")
        if i > 0:
            arrow(dr, 200 + (i - 1) * 293 + 115, 365, x - 115, 365, DIM, 3)
    if t > 20:
        txt(dr, (W // 2, 520), "every report is a gift \u2014 the user did the hard part",
            font(F_SANS, 26), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 580), "MTTR starts at the inbox, not the console",
            font(F_SANS, 26), TEAL, anchor="mm")

def scene_patch(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "PATCH TUESDAY STANDOFF", CYAN)
    txt(dr, (640, 165), "exploitability", font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (90, 380), "exposure", font(F_SANS, 24), DIM, anchor="mm")
    dr.rectangle([140, 190, 1140, 590], outline=DIM, width=2)
    dr.line([640, 190, 640, 590], fill=DIM, width=1)
    dr.line([140, 390, 1140, 390], fill=DIM, width=1)
    items = [("VPN gateway RCE", 980, 250, 6, RED), ("print spooler", 420, 300, 10, ORANGE),
             ("dev laptop lib", 900, 480, 14, YELLOW), ("test VM agent", 300, 500, 18, GREEN)]
    for nm, x, y, born, col in items:
        if t < born:
            continue
        k = clamp((t - born) / 1.5)
        r = int(14 * k)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col)
        txt(dr, (x, y - 28), nm, font(F_SANS, 22), CREAM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 630), "patch the top-right first \u2014 risk is a product, not a count",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_cred_hygiene(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "KILL THE SHARED ADMIN PASSWORD", MAGENTA)
    lines = ["# shared creds are invisible backdoors", "shared_admin = Password123!",
             "vault: 1 identity per human, MFA enforced", "break-glass: sealed, audited, rotated"]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 180, 150, W - 180, 560, "identity.py", cl(lines), hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "one human, one identity \u2014 or you have zero accountability",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ acad-data: Data (3b1b x2 + primer x1)
def scene_base_rate(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 80), "THE 99% ACCURATE TEST", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 130), "1,000 people \u00b7 10 are sick \u00b7 the test is 99% accurate",
        font(F_SANS, 26), DIM, anchor="mm")
    _r.seed(42)
    sick = set(_r.sample(range(1000), 10))
    k = clamp((t - 5) / 8)
    shown = int(1000 * k)
    flagged = 0
    for i in range(shown):
        x = 190 + (i % 40) * 24
        y = 190 + (i // 40) * 22
        is_sick = i in sick
        # 99% accurate: sick flagged 99%, healthy flagged 1%
        if is_sick:
            flagged += 1
            col = RED
        else:
            if _r.random() < 0.01:
                flagged += 1
                col = ORANGE
            else:
                col = (40, 60, 90)
        dr.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col)
    if t > 15:
        txt(dr, (W // 2, 560), "a positive test is more likely FALSE than true",
            font(F_BOLD, 30), YELLOW, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 610), "accuracy means nothing without the base rate",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_correlation(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 80), "CORRELATION IS NOT CAUSATION", font(F_BOLD, 40), TEAL, anchor="mm")
    ox, oy, pw, ph = 240, 560, 800, 380
    dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
    _r.seed(7)
    k = clamp((t - 5) / 7)
    npts = int(60 * k)
    for i in range(npts):
        xv = _r.random()
        yv = xv * 0.8 + _r.gauss(0, 0.12)
        x = ox + xv * pw
        y = oy - clamp(yv) * ph
        dr.ellipse([x - 5, y - 5, x + 5, y + 5], fill=CYAN)
    if t > 13:
        txt(dr, (W // 2, 180), "r = 0.91 \u2014 but look closer\u2026", font(F_BOLD, 32), YELLOW, anchor="mm")
    if t > 16:
        _r.seed(7)
        for i in range(npts):
            xv = _r.random()
            conf = 0.3 if i % 3 == 0 else 0.8
            yv = xv * conf + _r.gauss(0, 0.05)
            x = ox + xv * pw
            y = oy - clamp(yv) * ph
            col = MAGENTA if conf < 0.5 else TEAL
            dr.ellipse([x - 6, y - 6, x + 6, y + 6], outline=col, width=2)
        txt(dr, (W // 2, 640), "a hidden variable splits the cloud \u2014 confounders lie",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_dirty_csv_init():
    _r.seed(99)
    rows = []
    for i in range(26):
        bad = _r.random() < 0.22
        rows.append((i, bad, _r.choice(["NULL", "9999-99-99", '"O\'Brien, Jr"', "12.3.4", "NA"])))
    return rows

def scene_dirty_csv(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE DIRTY CSV", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 120), "1,000 rows in \u00b7 watch the pipeline clean them",
        font(F_SANS, 26), DIM, anchor="mm")
    rows = scene_dirty_csv_init()
    k = clamp((t - 5) / 12)
    nshow = int(len(rows) * k)
    clean = sum(1 for _, bad, _ in rows[:nshow] if not bad)
    rej = sum(1 for _, bad, _ in rows[:nshow] if bad)
    for i, (rid, bad, why) in enumerate(rows[:nshow]):
        y = 170 + i * 16
        x = 300
        col = RED if bad else GREEN
        dr.rectangle([x, y, x + 14, y + 10], fill=col)
        txt(dr, (x + 24, y + 5), "row %04d" % (rid * 38 + 7), font(F_MONO, 15), DIM, anchor="lm")
        if bad:
            txt(dr, (x + 420, y + 5), "\u2192 rejected: " + why, font(F_MONO, 15), RED, anchor="lm")
    bar(dr, 760, 200, 320, 40, nshow / len(rows), TEAL, "clean rows", str(clean))
    bar(dr, 760, 300, 320, 40, nshow / len(rows), RED, "rejected", str(rej))
    if t > 20:
        txt(dr, (W // 2, 640), "data quality is a pipeline, not a hope \u2014 validate at ingestion",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ acad-forge: Forge (fireship x1 + story x1 + bbg x1)
def scene_broken_build(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE BROKEN BUILD", MAGENTA)
    lines = ["$ git push origin main", "CI: lint PASS \u00b7 test FAIL \u00b7 build BLOCKED",
             "fix: 1 flaky test, 0 excuses", "green build = merged with confidence"]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 180, 150, W - 180, 560, "ci.sh", cl(lines), hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "red on main is a team emergency \u2014 fix or revert, fast",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_merge_close(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "MERGE OR CLOSE?", font(F_SERIFB, 44), GOLD, anchor="mm")
    k = clamp((t - 5) / 6)
    # diff lines grow
    for i in range(int(9 * k)):
        y = 200 + i * 30
        add = i % 3 != 2
        col = (60, 140, 80) if add else (150, 70, 70)
        dr.rectangle([380, y, 380 + int(560 * (0.3 + 0.7 * (i % 4) / 3)), y + 18], fill=col)
        txt(dr, (350, y + 9), "+" if add else "-", font(F_MONO, 20), col, anchor="rm")
    if t > 12:
        txt(dr, (W // 2, 500), "the PR started at 40 lines \u2014 it is now 400",
            font(F_SERIF, 28), CREAM, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 560), "scope creep is a kindness that kills: close it, split it, ship the core",
            font(F_SERIF, 26), GOLD, anchor="mm")

def scene_release_day(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "RELEASE DAY ROLLBACK", CYAN)
    stages = [("canary 5%", 5), ("canary 25%", 9), ("canary 50%", 13), ("full 100%", 17)]
    for i, (nm, born) in enumerate(stages):
        if t < born:
            continue
        x = 170 + i * 320
        bad = (i == 2)
        col = RED if bad else GREEN
        glow_box(dr, [x - 130, 260, x + 130, 400], col, rad=10, layers=2)
        dr.rectangle([x - 130, 260, x + 130, 400], fill=(10, 16, 28))
        txt(dr, (x, 305), nm.upper(), font(F_BOLD, 26), WHITE, anchor="mm")
        st = "ERRORS SPIKE" if bad else "HEALTHY"
        txt(dr, (x, 355), st, font(F_MONOB, 24), col, anchor="mm")
        if i > 0:
            arrow(dr, 170 + (i - 1) * 320 + 135, 330, x - 135, 330, DIM, 3)
    if t > 18:
        arrow(dr, 490, 440, 240, 440, YELLOW, 8)
        txt(dr, (365, 480), "ROLLBACK in 4 min", font(F_BOLD, 28), YELLOW, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 580), "canary caught it \u2014 that is the system working, not failing",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ acad-hermetica: Hermetica (story + 3b1b + primer)
def scene_fix_broke(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE FIX THAT BROKE MORE", font(F_SERIFB, 38), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 220), "you sped up the queue\u2026", font(F_SERIF, 32), CREAM, anchor="mm")
    if t > 9:
        txt(dr, (W // 2, 300), "\u2026and the database fell over", font(F_SERIF, 32), RED, anchor="mm")
    if t > 13:
        # reinforcing loop circle
        cx, cy, rr = W // 2, 470, 90
        pts = []
        for a_i in range(48):
            a = a_i / 48 * 6.283
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        dr.line(pts + [pts[0]], fill=GOLD, width=4)
        arrow(dr, cx + rr, cy, cx + rr - 40, cy - 40, GOLD, 5)
        txt(dr, (cx, cy - 14), "faster", font(F_SERIFB, 26), GOLD, anchor="mm")
        txt(dr, (cx, cy + 22), "\u2192 more load \u2192 slower", font(F_SERIF, 24), CREAM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 620), "every fix is an intervention in a system \u2014 expect pushback",
            font(F_SERIF, 26), GOLD, anchor="mm")

def scene_feedback(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 80), "FEEDBACK LOOPS, VISUALIZED", font(F_BOLD, 40), TEAL, anchor="mm")
    # reinforcing: exponential curve; balancing: damped oscillation
    ox, oy, pw, ph = 200, 600, 400, 360
    dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
    txt(dr, (ox + pw // 2, oy + 30), "reinforcing (R)", font(F_SANS, 24), YELLOW, anchor="mm")
    k = clamp((t - 5) / 8)
    pts = []
    for i in range(int(60 * k)):
        x = ox + i / 60 * pw
        y = oy - (math.exp(i / 60 * 2.2) - 1) / (math.exp(2.2) - 1) * ph
        pts.append((x, y))
    if len(pts) > 1:
        dr.line(pts, fill=YELLOW, width=4)
    ox2 = 680
    dr.rectangle([ox2, oy - ph, ox2 + pw, oy], outline=DIM, width=2)
    txt(dr, (ox2 + pw // 2, oy + 30), "balancing (B)", font(F_SANS, 24), TEAL, anchor="mm")
    pts2 = []
    for i in range(int(80 * k)):
        x = ox2 + i / 80 * pw
        y = oy - ph / 2 - math.sin(i / 80 * 12.56) * math.exp(-i / 80 * 2.5) * ph / 2.2
        pts2.append((x, y))
    if len(pts2) > 1:
        dr.line(pts2, fill=TEAL, width=4)
    if t > 18:
        txt(dr, (W // 2, 180), "R amplifies \u00b7 B stabilizes \u2014 find the loops before you touch the system",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_goodhart_init():
    _r.seed(2024)
    return [_r.uniform(0.3, 0.7) for _ in range(24)]

def scene_goodhart(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "GOODHART'S LAW", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 120), "when a measure becomes a target, it ceases to be a good measure",
        font(F_SANS, 24), DIM, anchor="mm")
    qual = scene_goodhart_init()
    k = clamp((t - 5) / 12)
    ngame = int(24 * k)
    for i, q in enumerate(qual):
        x = 180 + i * 41
        # metric bar: gamed ones inflate
        gamed = i < ngame
        mh = (q + (0.45 if gamed else 0)) * 300
        col = RED if gamed else TEAL
        dr.rectangle([x, 480 - mh, x + 28, 480], fill=col)
        # quality dot stays flat
        qy = 480 - q * 300
        dr.ellipse([x + 8, qy - 6, x + 20, qy + 6], fill=YELLOW)
    txt(dr, (180, 520), "bars = the metric (rises when gamed)", font(F_SANS, 22), RED, anchor="lm")
    txt(dr, (180, 552), "dots = real quality (flat)", font(F_SANS, 22), YELLOW, anchor="lm")
    if t > 20:
        txt(dr, (W // 2, 620), "measure outcomes, rotate metrics, never pay on one number",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ acad-math: Math (3b1b x2 + primer x1)
def scene_expected_value(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 80), "EXPECTED VALUE OF THE OUTAGE", font(F_BOLD, 38), TEAL, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 220), "P(outage this year) = 0.20", font(F_MONOB, 34), WHITE, anchor="mm")
    if t > 9:
        txt(dr, (W // 2, 300), "cost of one outage = $500k", font(F_MONOB, 34), WHITE, anchor="mm")
    if t > 13:
        k = clamp((t - 13) / 3)
        txt(dr, (W // 2, 400), "EV = 0.20 \u00d7 $500k = $%dk" % int(100 * k),
            font(F_MONOB, 44), YELLOW, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 490), "the fix costs $40k \u2014 EV says: buy it twice over",
            font(F_SANS, 28), CREAM, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 570), "expected value turns fear into arithmetic",
            font(F_SANS, 26), TEAL, anchor="mm")

def scene_misleading_avg(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 80), "THE MISLEADING AVERAGE", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 130), "10,000 requests \u00b7 mean latency 120ms \u00b7 is that good?",
        font(F_SANS, 26), DIM, anchor="mm")
    _r.seed(11)
    lats = [_r.expovariate(1 / 90) for _ in range(120)]
    k = clamp((t - 5) / 8)
    nshow = int(len(lats) * k)
    mx = 600.0
    for i, lat in enumerate(lats[:nshow]):
        x = 220 + i * 7
        hh = clamp(lat / mx) * 330
        col = RED if lat > 400 else TEAL
        dr.rectangle([x, 540 - hh, x + 5, 540], fill=col)
    dr.line([220, 540 - 120 / mx * 330, 1060, 540 - 120 / mx * 330], fill=YELLOW, width=3)
    txt(dr, (1075, 540 - 120 / mx * 330), "mean 120ms", font(F_SANS, 20), YELLOW, anchor="lm")
    if t > 16:
        txt(dr, (W // 2, 600), "but p99 = 480ms \u2014 100 users got the tail, not the average",
            font(F_BOLD, 28), RED, anchor="mm")

def scene_fermi_init():
    _r.seed(55)
    return [("engineers", 4), ("servers", 5), ("deploys/day", 2), ("users", 6), ("support tickets", 3)]

def scene_fermi(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "FERMI THE MIGRATION", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 120), "how many support tickets will the migration cause? estimate in powers of ten",
        font(F_SANS, 24), DIM, anchor="mm")
    items = scene_fermi_init()
    k = clamp((t - 5) / 12)
    for i, (nm, mag) in enumerate(items):
        y = 200 + i * 80
        frac = clamp(k * len(items) - i)
        bar(dr, 300, y, 620, 40, frac * mag / 6.5, TEAL, nm, "10^%d" % int(mag * frac))
    if t > 19:
        tot = sum(m for _, m in items)
        txt(dr, (W // 2, 600), "multiply the exponents: ~10^%d \u2014 within a factor of 10, good enough to plan" % tot,
            font(F_BOLD, 28), YELLOW, anchor="mm")

# ============================================================ acad-systems: Systems (bbg x2 + primer x1)
def scene_full_disk(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE FULL DISK AT 3 AM", CYAN)
    _r.seed(3)
    k = clamp((t - 5) / 10)
    nblocks = 160
    nfill = int(nblocks * (0.62 + 0.38 * k))
    cols = 20
    for i in range(nblocks):
        x = 240 + (i % cols) * 40
        y = 210 + (i // cols) * 44
        full = i < nfill
        hot = full and _r.random() < 0.3
        col = RED if hot else (CYAN if full else (25, 35, 55))
        dr.rectangle([x, y, x + 32, y + 36], fill=col, outline=DIM, width=1)
    pct = int((0.62 + 0.38 * k) * 100)
    txt(dr, (W // 2, 590), "disk %d%% full \u2014 and climbing" % pct,
        font(F_MONOB, 32), RED if pct > 95 else WHITE, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 640), "the fix: rotate logs, prune images \u2014 the lesson: alert at 80%, not 100%",
            font(F_SANS, 24), CREAM, anchor="mm")

def scene_split_brain(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "SPLIT BRAIN", CYAN)
    def part(x, label, live, writes):
        col = GREEN if live else RED
        glow_box(dr, [x - 220, 230, x + 220, 470], col, rad=12, layers=2)
        dr.rectangle([x - 220, 230, x + 220, 470], fill=(10, 16, 28))
        txt(dr, (x, 270), label, font(F_BOLD, 28), WHITE, anchor="mm")
        txt(dr, (x, 330), "WRITES: " + writes, font(F_MONOB, 26), col, anchor="mm")
        txt(dr, (x, 390), "thinks it is PRIMARY" if live else "thinks it is PRIMARY",
            font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        txt(dr, (W // 2, 165), "the network partition heals\u2026", font(F_SANS, 28), DIM, anchor="mm")
    if t > 8:
        part(360, "partition A", True, "1,204")
        part(920, "partition B", False, "1,187")
        txt(dr, (W // 2, 520), "two primaries \u00b7 two histories \u2014 who wins?",
            font(F_BOLD, 30), RED, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 580), "quorum decides: majority partition keeps the writes, minority replays",
            font(F_SANS, 26), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 630), "no quorum, no writes \u2014 availability bows to consistency",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_herd_init():
    _r.seed(77)
    return [int(40 + 60 * math.exp(-((i - 8) ** 2) / 6) * 8 + _r.gauss(0, 8)) for i in range(40)]

def scene_herd(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THUNDERING HERD ON DEPLOY", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 120), "10,000 clients retry at once \u2014 the server melts, then recovers",
        font(F_SANS, 24), DIM, anchor="mm")
    reqs = scene_herd_init()
    k = clamp((t - 5) / 14)
    nshow = int(len(reqs) * k)
    mx = max(reqs)
    jitter = t > 17
    for i in range(nshow):
        x = 200 + i * 22
        v = reqs[i]
        if jitter:
            v = int(v * (0.45 + 0.1 * math.sin(i * 2.1)))
        hh = clamp(v / mx) * 380
        col = RED if v / mx > 0.55 else TEAL
        dr.rectangle([x, 540 - hh, x + 16, 540], fill=col)
    dr.line([200, 540 - 0.55 * 380, 1080, 540 - 0.55 * 380], fill=YELLOW, width=2)
    txt(dr, (1090, 540 - 0.55 * 380), "capacity", font(F_SANS, 20), YELLOW, anchor="lm")
    if t > 17:
        txt(dr, (W // 2, 600), "jittered exponential backoff flattens the herd \u2014 retries with manners",
            font(F_SANS, 26), GREEN, anchor="mm")

# ============================================================ acad-theory: Theory (3b1b x2 + story x1)
def scene_halting(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE HALTING HELPDESK", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 120), "a program that predicts every program's fate \u2014 then meets itself",
        font(F_SANS, 24), DIM, anchor="mm")
    progs = ["P1", "P2", "P3", "P4", "P5"]
    cell = 110
    ox, oy = 365, 220
    k = clamp((t - 5) / 9)
    ncell = int(25 * k)
    _r.seed(21)
    grid = [[_r.choice(["H", "L"]) for _ in range(5)] for _ in range(5)]
    for idx in range(ncell):
        i, j = divmod(idx, 5)
        x, y = ox + j * cell, oy + i * cell
        diag = i == j
        col = RED if diag else (CYAN if grid[i][j] == "H" else DIM)
        dr.rectangle([x, y, x + cell - 8, y + cell - 8], fill=(14, 20, 34), outline=col, width=3)
        val = grid[i][j]
        if diag and t > 16:
            val = "L" if val == "H" else "H"
        txt(dr, (x + (cell - 8) // 2, y + (cell - 8) // 2), val,
            font(F_BOLD, 34), col, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 600), "flip the diagonal: the predictor contradicts itself \u2014 no such program exists",
            font(F_BOLD, 26), YELLOW, anchor="mm")

def scene_blowup(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "EXPONENTIAL BLOWUP", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 120), "fib(20): the naive recursion spawns 21,891 calls",
        font(F_SANS, 26), DIM, anchor="mm")
    k = clamp((t - 5) / 10)
    depth = int(k * 5) + 1
    def node(x, y, d, label):
        if d >= depth:
            return
        dr.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(14, 20, 34), outline=TEAL, width=2)
        txt(dr, (x, y), label, font(F_MONOB, 20), CREAM, anchor="mm")
        if d + 1 < depth:
            dx = 320 / (2 ** (d + 1))
            dy = 90
            for sgn, nl in [(-1, "n-1"), (1, "n-2")]:
                nx, ny = x + sgn * dx * 1.6, y + dy
                dr.line([x, y + 26, nx, ny - 26], fill=DIM, width=2)
                node(nx, ny, d + 1, nl)
    node(W // 2, 210, 0, "fib(n)")
    n = 2 ** depth - 1
    txt(dr, (W // 2, 600), "%d calls and counting \u2014 memoize it: O(n), done" % n,
        font(F_BOLD, 28), YELLOW, anchor="mm")

def scene_two_generals(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "TWO GENERALS, ONE DEPLOY", font(F_SERIFB, 38), GOLD, anchor="mm")
    # two hills, valley, messenger
    dr.polygon([(60, 620), (330, 300), (600, 620)], fill=(20, 26, 18))
    dr.polygon([(680, 620), (950, 300), (1220, 620)], fill=(20, 26, 18))
    txt(dr, (330, 250), "general A", font(F_SERIF, 26), CREAM, anchor="mm")
    txt(dr, (950, 250), "general B", font(F_SERIF, 26), CREAM, anchor="mm")
    if t > 5:
        prog = (t - 5) / 16
        mx = 330 + (950 - 330) * (prog % 1.0)
        my = 470 - math.sin((prog % 1.0) * math.pi) * 130
        dr.ellipse([mx - 14, my - 14, mx + 14, my + 14], fill=GOLD)
        txt(dr, (mx, my - 30), "attack at dawn?", font(F_SERIF, 20), GOLD, anchor="mm")
    if t > 13:
        txt(dr, (W // 2, 180), "the messenger might be captured\u2026", font(F_SERIF, 26), RED, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 660), "no protocol guarantees agreement over a lossy channel \u2014 consensus has limits",
            font(F_SERIF, 24), GOLD, anchor="mm")

SLUG_DIR = {
    "career": "acad-career", "cloud": "acad-cloud", "command": "acad-command",
    "cyber": "acad-cyber", "data": "acad-data", "forge": "acad-forge",
    "hermetica": "acad-hermetica", "math": "acad-math",
    "systems": "acad-systems", "theory": "acad-theory",
}

# ============================================================ VIDEOS registry
def V(kicker, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[slug.split("-")[0]],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    "career": "ACAD-CAREER \u00b7 Career", "cloud": "ACAD-CLOUD \u00b7 Cloud",
    "command": "ACAD-COMMAND \u00b7 Command", "cyber": "ACAD-CYBER \u00b7 Cyber",
    "data": "ACAD-DATA \u00b7 Data", "forge": "ACAD-FORGE \u00b7 Forge",
    "hermetica": "ACAD-HERMETICA \u00b7 Hermetica", "math": "ACAD-MATH \u00b7 Math",
    "systems": "ACAD-SYSTEMS \u00b7 Systems", "theory": "ACAD-THEORY \u00b7 Theory",
}

VIDEOS = [
 # --- acad-career
 V(BOOTCAMP_K["career"], "career-lowball-offer", "The Lowball Offer",
   "your anchor, not their first number", "story", scene_lowball,
   "The lowball offer meets its counter: a research-backed anchor, a stated BATNA, and the discipline to ask and wait.",
   [(4,10,"The offer lands low \u2014 $85k for a $120k market"),
    (10,16,"Your anchor is research-backed: comps, bands, and the value you ship"),
    (16,22,"Know your range, state your BATNA, ask \u2014 then wait"),
    (22,26,"Negotiation is information: prepare before you speak")]),
 V(BOOTCAMP_K["career"], "career-negotiation", "Negotiation Leverage in 100 Seconds",
   "BATNA, anchor, and the zone of possible agreement", "fireship", scene_negotiation,
   "A rapid explainer on the three numbers that win salary talks: your BATNA, your anchor, and the zone of possible agreement.",
   [(4,10,"Three numbers win every salary talk"),
    (10,16,"BATNA: your best alternative to no agreement"),
    (16,22,"Anchor: the first number \u2014 make it yours"),
    (22,26,"Anchor high, justify with data, then stay silent")]),
 V(BOOTCAMP_K["career"], "career-cold-email", "The Networking Cold Email",
   "38% reply rates are engineered, not luck", "story", scene_cold_email,
   "The cold email that actually gets answered: specific, short, and curious \u2014 and it never asks for a job.",
   [(4,10,"The envelope opens: a cold email leaves for a stranger"),
    (10,16,"Most are ignored \u2014 the great ones hit a 38% reply rate"),
    (16,22,"Specific, short, curious: make it easy to say yes"),
    (22,26,"Never ask for a job \u2014 ask for insight")]),
 # --- acad-cloud
 V(BOOTCAMP_K["cloud"], "cloud-surprise-bill", "The Surprise FinOps Bill",
   "idle VMs are the silent budget killer", "bbg", scene_surprise_bill,
   "A FinOps teardown of the surprise cloud bill: idle VMs burn 40% of spend with zero traffic \u2014 tag, alert, and shut them down.",
   [(4,10,"The bill lands: $35,500 \u2014 triple the forecast"),
    (10,16,"Idle VMs: 40% of spend, zero traffic \u2014 FinOps kill #1"),
    (16,22,"Egress and zombie storage leak the rest"),
    (22,26,"Tag everything, alert on anomaly, shut down the idle")]),
 V(BOOTCAMP_K["cloud"], "cloud-region-failover", "Region Failover Drill",
   "game-day the failover before you need it", "bbg", scene_failover,
   "An architecture walkthrough of a region failover drill: primary fails, traffic shifts, RTO five minutes, RPO zero.",
   [(4,10,"us-east-1 healthy \u00b7 us-west-2 warm on standby"),
    (10,16,"The primary fails \u2014 health checks declare it dead"),
    (16,22,"Traffic shifts west: RTO five minutes, RPO zero"),
    (22,26,"Game-day the failover before you need the failover")]),
 V(BOOTCAMP_K["cloud"], "cloud-shared-responsibility", "Shared Responsibility in 100 Seconds",
   "the cloud secures OF itself \u2014 you secure what is IN it", "fireship", scene_shared_resp,
   "A rapid explainer on the shared responsibility model: IaaS, PaaS, and SaaS each move the line between the cloud and you.",
   [(4,10,"IaaS: the cloud owns hardware \u2014 you patch the OS"),
    (10,16,"PaaS: the cloud owns the runtime \u2014 you secure the app"),
    (16,22,"SaaS: the cloud owns the app \u2014 you guard the data"),
    (22,26,"The cloud secures OF itself \u2014 you secure what is IN it")]),
 # --- acad-command
 V(BOOTCAMP_K["command"], "command-3am-page", "The 3 AM Page",
   "command is calm \u2014 the page is the job", "story", scene_3am,
   "Incident command under pressure: the 3 AM page arrives, the Incident Commander declares, and three roles turn chaos into a shift.",
   [(4,10,"3 AM: the pager screams \u2014 checkout latency past two seconds"),
    (10,16,"The Incident Commander declares: one voice, one plan"),
    (16,22,"Ops on keys, comms outward \u2014 roles turn chaos into a shift"),
    (22,26,"Command is calm \u2014 the page is the job")]),
 V(BOOTCAMP_K["command"], "command-deploy-or-rollback", "Deploy or Rollback?",
   "the decision tree decides, not your gut", "bbg", scene_deploy_rollback,
   "A decision-tree view of the deploy-versus-rollback call: uncertainty is the input, the error budget is the rule, the tree decides.",
   [(4,10,"The error budget is burning \u2014 deploy or rollback?"),
    (10,16,"Rollback: the safe path, always available"),
    (16,22,"Roll forward only with a proven fix in hand"),
    (22,26,"Canary red for ten minutes \u2192 rollback, no debate")]),
 V(BOOTCAMP_K["command"], "command-blameless-postmortem", "The Blameless Postmortem",
   "systems fail, people learn", "story", scene_postmortem,
   "The blameless postmortem: a timeline of the 2 AM outage and the review that fixed the system instead of naming a culprit.",
   [(4,10,"02:14 \u2014 deploy v2.4.1 ships"),
    (10,16,"02:41 \u2014 the latency alarms fire"),
    (16,22,"03:05 \u2014 rollback completes; 10:00 \u2014 the blameless review"),
    (22,26,"Blame fixes nothing \u2014 systems fail, people learn")]),
 # --- acad-cyber
 V(BOOTCAMP_K["cyber"], "cyber-phishing-triage", "The 2 AM Phishing Report",
   "MTTR starts at the inbox, not the console", "bbg", scene_phishing,
   "A SOC pipeline diagram for the 2 AM phishing report: report, triage, isolate, hunt \u2014 every report is a gift.",
   [(4,10,"2 AM: a user reports the phish \u2014 the pipeline starts"),
    (10,16,"Triage: scope the blast radius from the headers"),
    (16,22,"Isolate the clicked hosts, then hunt for the rest"),
    (22,26,"MTTR starts at the inbox, not the console")]),
 V(BOOTCAMP_K["cyber"], "cyber-patch-tuesday", "Patch Tuesday Standoff",
   "risk is a product, not a count", "bbg", scene_patch,
   "A risk-matrix approach to Patch Tuesday: plot exploitability against exposure, patch the top-right quadrant first.",
   [(4,10,"Forty patches, one maintenance window"),
    (10,16,"Plot them: exploitability against exposure"),
    (16,22,"Top-right quadrant ships first \u2014 the rest can wait"),
    (22,26,"Risk is a product, not a count")]),
 V(BOOTCAMP_K["cyber"], "cyber-credential-hygiene", "Kill the Shared Admin Password",
   "one human, one identity", "fireship", scene_cred_hygiene,
   "A rapid explainer on credential hygiene: shared admin passwords are invisible backdoors \u2014 one human, one identity, MFA everywhere.",
   [(4,10,"Shared creds are invisible backdoors"),
    (10,16,"One identity per human, MFA enforced"),
    (16,22,"Break-glass accounts: sealed, audited, rotated"),
    (22,26,"One human, one identity \u2014 or zero accountability")]),
 # --- acad-data
 V(BOOTCAMP_K["data"], "data-base-rate", "The 99% Accurate Test",
   "accuracy means nothing without the base rate", "3b1b", scene_base_rate,
   "A population visualization of the base-rate fallacy: a 99% accurate test on a rare condition still produces mostly false positives.",
   [(4,10,"One thousand people \u00b7 ten are sick \u00b7 the test is 99% accurate"),
    (10,16,"The positives pile up \u2014 but most flags are healthy people"),
    (16,22,"A positive result is more likely FALSE than true"),
    (22,26,"Accuracy means nothing without the base rate")]),
 V(BOOTCAMP_K["data"], "data-correlation", "Correlation Is Not Causation",
   "confounders lie", "3b1b", scene_correlation,
   "A scatter-plot walkthrough of correlation versus causation: r = 0.91 collapses when a hidden confounder splits the cloud.",
   [(4,10,"The scatter climbs: r = 0.91 \u2014 looks causal"),
    (10,16,"But look closer\u2026 a hidden variable splits the cloud"),
    (16,22,"Two flat clusters, one fake trend \u2014 confounders lie"),
    (22,26,"Correlation suggests; only design proves")]),
 V(BOOTCAMP_K["data"], "data-dirty-csv", "The Dirty CSV",
   "data quality is a pipeline, not a hope", "primer", scene_dirty_csv,
   "A living simulation of a data-ingestion pipeline: a thousand rows flow in, malformed rows are rejected with reasons, the clean set grows.",
   [(4,10,"A thousand rows arrive \u2014 watch the pipeline clean them"),
    (10,16,"Malformed rows rejected: NULLs, bad dates, broken quotes"),
    (16,22,"The clean set grows \u2014 every rejection has a reason"),
    (22,26,"Validate at ingestion \u2014 hope is not a pipeline")]),
 # --- acad-forge
 V(BOOTCAMP_K["forge"], "forge-broken-build", "The Broken Build",
   "red on main is a team emergency", "fireship", scene_broken_build,
   "A rapid explainer on CI discipline: a flaky test blocks the build, and red on main is a team emergency \u2014 fix or revert, fast.",
   [(4,10,"Push to main \u2014 CI runs: lint pass, test FAIL"),
    (10,16,"One flaky test blocks the whole build"),
    (16,22,"Fix the test or revert the commit \u2014 no third option"),
    (22,26,"Red on main is a team emergency")]),
 V(BOOTCAMP_K["forge"], "forge-merge-or-close", "Merge or Close?",
   "scope creep is a kindness that kills", "story", scene_merge_close,
   "The pull request that grew from 40 lines to 400: scope creep framed as kindness, and the discipline to close it, split it, ship the core.",
   [(4,10,"The PR started at forty lines \u2014 it is now four hundred"),
    (10,16,"Every \u2018while you're in there\u2019 added weight"),
    (16,22,"Scope creep is a kindness that kills"),
    (22,26,"Close it, split it, ship the core")]),
 V(BOOTCAMP_K["forge"], "forge-release-day", "Release Day Rollback",
   "canary caught it \u2014 the system working, not failing", "bbg", scene_release_day,
   "A canary-deployment diagram of release day: the 50% canary spikes errors, rollback completes in four minutes \u2014 the system working.",
   [(4,10,"Canary 5%, 25% \u2014 all healthy"),
    (10,16,"Canary 50%: errors spike \u2014 the canary caught it"),
    (16,22,"Rollback in four minutes \u2014 most users never noticed"),
    (22,26,"That is the system working, not failing")]),
 # --- acad-hermetica
 V(BOOTCAMP_K["hermetica"], "hermetica-fix-broke-more", "The Fix That Broke More",
   "every fix is an intervention in a system", "story", scene_fix_broke,
   "Systems thinking through the fix that broke more: speeding up the queue overloaded the database \u2014 the reinforcing loop, drawn.",
   [(4,10,"You sped up the queue\u2026"),
    (10,16,"\u2026and the database fell over"),
    (16,22,"The reinforcing loop: faster \u2192 more load \u2192 slower"),
    (22,26,"Every fix is an intervention \u2014 expect pushback")]),
 V(BOOTCAMP_K["hermetica"], "hermetica-feedback-loops", "Feedback Loops, Visualized",
   "R amplifies \u00b7 B stabilizes", "3b1b", scene_feedback,
   "A mathematical visualization of feedback loops: the reinforcing curve that amplifies and the balancing oscillation that stabilizes.",
   [(4,10,"Two loops govern every system"),
    (10,16,"Reinforcing (R): the exponential that amplifies"),
    (16,22,"Balancing (B): the oscillation that stabilizes"),
    (22,26,"Find the loops before you touch the system")]),
 V(BOOTCAMP_K["hermetica"], "hermetica-goodhart", "Goodhart's Law",
   "when a measure becomes a target\u2026", "primer", scene_goodhart,
   "A simulation of Goodhart's law: the metric rises as teams game it while real quality stays flat \u2014 measure outcomes, rotate metrics.",
   [(4,10,"The metric rises \u2014 everyone is optimizing it"),
    (10,16,"But the dots \u2014 real quality \u2014 stay flat"),
    (16,22,"A measure that became a target stopped measuring"),
    (22,26,"Measure outcomes, rotate metrics, never pay on one number")]),
 # --- acad-math
 V(BOOTCAMP_K["math"], "math-expected-value", "Expected Value of the Outage",
   "expected value turns fear into arithmetic", "3b1b", scene_expected_value,
   "Expected value applied to the outage decision: a 20% chance of a $500k outage makes a $40k fix the obvious buy.",
   [(4,10,"Probability of an outage this year: 0.20"),
    (10,16,"Cost of one outage: $500,000"),
    (16,22,"Expected value: 0.20 \u00d7 $500k = $100k"),
    (22,26,"The $40k fix is the obvious buy \u2014 twice over")]),
 V(BOOTCAMP_K["math"], "math-misleading-average", "The Misleading Average",
   "100 users got the tail, not the average", "3b1b", scene_misleading_avg,
   "A latency-histogram visualization of the misleading average: mean 120ms hides a p99 of 480ms \u2014 the tail is the experience.",
   [(4,10,"Ten thousand requests \u00b7 mean latency 120ms \u00b7 looks good?"),
    (10,16,"The red bars: requests past 400ms"),
    (16,22,"p99 = 480ms \u2014 one hundred users got the tail"),
    (22,26,"The average describes nobody \u2014 report the percentiles")]),
 V(BOOTCAMP_K["math"], "math-fermi", "Fermi the Migration",
   "within a factor of ten, good enough to plan", "primer", scene_fermi,
   "A Fermi-estimation simulation for the migration: multiply the orders of magnitude \u2014 within a factor of ten is good enough to plan.",
   [(4,10,"How many support tickets will the migration cause?"),
    (10,16,"Estimate in powers of ten: engineers, servers, deploys"),
    (16,22,"Multiply the exponents \u2014 no calculator needed"),
    (22,26,"Within a factor of ten: good enough to plan")]),
 # --- acad-systems
 V(BOOTCAMP_K["systems"], "systems-full-disk", "The Full Disk at 3 AM",
   "alert at 80%, not 100%", "bbg", scene_full_disk,
   "A disk-block visualization of the 3 AM full disk: blocks fill red, the percentage climbs, and the lesson is alert at 80%, not 100%.",
   [(4,10,"3 AM: the disk is 62% full \u2014 and climbing"),
    (10,16,"Blocks fill red \u2014 logs nobody rotated"),
    (16,22,"100%: the database halts mid-write"),
    (22,26,"Rotate logs, prune images \u2014 alert at 80%, not 100%")]),
 V(BOOTCAMP_K["systems"], "systems-split-brain", "Split Brain",
   "no quorum, no writes", "bbg", scene_split_brain,
   "A partition diagram of split brain: two sides each think they are primary, two histories diverge \u2014 quorum decides who wins.",
   [(4,10,"The network partition heals\u2026"),
    (10,16,"Two primaries \u00b7 two histories \u2014 who wins?"),
    (16,22,"Quorum decides: the majority keeps its writes"),
    (22,26,"No quorum, no writes \u2014 availability bows to consistency")]),
 V(BOOTCAMP_K["systems"], "systems-thundering-herd", "Thundering Herd on Deploy",
   "retries with manners", "primer", scene_herd,
   "A request-spike simulation of the thundering herd: ten thousand clients retry at once, then jittered backoff flattens the storm.",
   [(4,10,"Ten thousand clients retry at once"),
    (10,16,"The spike blows past capacity \u2014 the server melts"),
    (16,22,"Jittered exponential backoff flattens the herd"),
    (22,26,"Retries with manners \u2014 never retry in lockstep")]),
 # --- acad-theory
 V(BOOTCAMP_K["theory"], "theory-halting", "The Halting Helpdesk",
   "no such program exists", "3b1b", scene_halting,
   "Diagonalization visualized: a table of programs predicting halting, the diagonal flips, and the predictor contradicts itself \u2014 impossible.",
   [(4,10,"A program that predicts every program's fate"),
    (10,16,"Rows: programs \u00b7 columns: inputs \u00b7 cells: halts or loops"),
    (16,22,"Flip the diagonal \u2014 the predictor contradicts itself"),
    (22,26,"No such program exists \u2014 that is the proof")]),
 V(BOOTCAMP_K["theory"], "theory-exponential-blowup", "Exponential Blowup",
   "memoize it: O(n), done", "3b1b", scene_blowup,
   "The naive Fibonacci recursion tree doubles every level: 2^n calls for fib(n) \u2014 memoize it and it is O(n), done.",
   [(4,10,"fib(20), naive recursion \u2014 watch the tree grow"),
    (10,16,"Every call spawns two \u2014 the tree doubles"),
    (16,22,"21,891 calls for one small number"),
    (22,26,"Memoize it: O(n), done")]),
 V(BOOTCAMP_K["theory"], "theory-two-generals", "Two Generals, One Deploy",
   "consensus has limits", "story", scene_two_generals,
   "The two generals problem as a story: messengers cross the valley, any one may be captured \u2014 no protocol guarantees agreement.",
   [(4,10,"Two generals, one valley, a messenger between them"),
    (10,16,"\u2018Attack at dawn?\u2019 \u2014 the message crosses"),
    (16,22,"But the messenger might be captured\u2026"),
    (22,26,"No protocol guarantees agreement over a lossy channel")]),
]

# ============================================================ VIDEOS registry (SLUG_DIR defined above)
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
