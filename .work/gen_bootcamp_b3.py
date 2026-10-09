#!/usr/bin/env python3
"""Bootcamp video Phase 2, Batch B3: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b2.py (do not modify the B2 file).

Filenames are bc- prefixed so they never collide with course videos.

Batch B3 bootcamps:
  con batch: cisco-ccna, comptia-a-plus, comptia-network-plus,
             comptia-security-plus, isc2-cc, m365-endpoint-admin
  cloud/devops: aws-cloud-practitioner-plus, devops-zero-to-hire,
             devsecops-mastery, iac-terraform-gitops, k8s-cka-exceed,
             kubernetes-sre
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

# ============================================================ cisco-ccna (bbg x2 + fireship x1)
def scene_ccna_vlan_dark(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "VLAN 30 GOES DARK", CYAN)
    if t > 4:
        panel(dr, [140, 240, 480, 440], "SW-A", GREEN)
        panel(dr, [800, 240, 1140, 440], "SW-B", GREEN)
        dr.line([480, 340, 800, 340], fill=CYAN, width=6)
        txt(dr, (640, 300), "trunk", font(F_MONOB, 24), CYAN, anchor="mm")
        for bx, lab in [(310, "VLAN 10"), (970, "VLAN 10")]:
            dr.rectangle([bx - 70, 470, bx + 70, 520], fill=(16, 24, 44), outline=GREEN, width=3)
            txt(dr, (bx, 495), lab, font(F_MONO, 20), GREEN, anchor="mm")
        for bx, lab in [(310, "VLAN 30"), (970, "VLAN 30")]:
            dr.rectangle([bx - 70, 540, bx + 70, 590], fill=(16, 24, 44), outline=DIM, width=3)
            txt(dr, (bx, 565), lab, font(F_MONO, 20), DIM, anchor="mm")
    if t > 9:
        k = clamp((t - 9) / 3)
        for i in range(int(6 * k)):
            x = 520 + i * 44
            dr.ellipse([x - 9, 331, x + 9, 349], fill=GREEN)
        txt(dr, (640, 390), "VLAN 10 crosses fine", font(F_SANS, 24), GREEN, anchor="mm")
    if t > 13:
        txt(dr, (640, 180), "switchport trunk allowed vlan 10", font(F_MONOB, 24), RED, anchor="mm")
        dr.line([560, 300, 720, 380], fill=RED, width=8)
        dr.line([560, 380, 720, 300], fill=RED, width=8)
        txt(dr, (640, 430), "VLAN 30: pruned at the trunk \u2014 frames die here",
            font(F_SANS, 24), RED, anchor="mm")
    if t > 18:
        dr.rectangle([380, 160, 900, 205], fill=(10, 20, 12))
        txt(dr, (640, 182), "switchport trunk allowed vlan add 30", font(F_MONOB, 24), GREEN, anchor="mm")
        for i in range(6):
            x = 520 + i * 44
            dr.ellipse([x - 9, 500, x + 9, 518], fill=GREEN)
        txt(dr, (640, 430), "VLAN 30 flows \u2014 the allowed list was the whole problem",
            font(F_SANS, 24), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 640), "VLANs don't cross trunks by magic \u2014 allowed lists do",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_ccna_ospf(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE NEIGHBOR THAT NEVER GOES FULL", CYAN)
    states = ["DOWN", "INIT", "2-WAY", "EXSTART", "EXCHANGE", "LOADING", "FULL"]
    if t > 4:
        panel(dr, [200, 200, 500, 360], "R1", CYAN)
        panel(dr, [780, 200, 1080, 360], "R2", CYAN)
        dr.line([500, 280, 780, 280], fill=DIM, width=5)
        txt(dr, (640, 240), "area 0", font(F_MONOB, 24), DIM, anchor="mm")
    if t > 6:
        prog = int(clamp((t - 6) / 8) * (len(states) - 1))
        for i, st in enumerate(states):
            x = 130 + i * 170
            stuck = (i == 3 and t > 14)
            col = RED if stuck and i == 3 else (GREEN if i <= prog else DIM)
            if i == 3 and t > 14 and i <= prog:
                col = RED
            dr.rectangle([x - 75, 460, x + 75, 510], fill=(14, 20, 34),
                         outline=col, width=3)
            txt(dr, (x, 485), st, font(F_MONOB, 19), col, anchor="mm")
            if i > 0:
                arrow(dr, 130 + (i - 1) * 170 + 78, 485, x - 78, 485, DIM, 3)
    if t > 14:
        txt(dr, (W // 2, 560), "stuck at EXSTART: MTU 1500 vs 9000 \u2014 DBDs never agree",
            font(F_SANS, 26), RED, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 560), "match the MTU \u2014 adjacency walks to FULL",
            font(F_SANS, 26), GREEN, anchor="mm")
        x = 130 + 6 * 170
        dr.rectangle([x - 75, 460, x + 75, 510], fill=(10, 24, 12), outline=GREEN, width=4)
        txt(dr, (x, 485), "FULL", font(F_MONOB, 19), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 640), "neighbors form on agreement \u2014 MTU, timers, area, auth",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_ccna_subnet(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "SUBNET A BRANCH OFFICE IN 100 SECONDS", MAGENTA)
    lines = ["# 192.168.10.0/24 \u2014 three subnets", "hq: 100 hosts  \u2192 /25  (126 usable)",
             "branch: 40 hosts \u2192 /26  (62 usable)", "iot: 12 hosts   \u2192 /28  (14 usable)",
             "192.168.10.0/25 | .128/26 | .192/28", "wasted: 6 addresses \u2014 not 200"]
    cols = [(200, 200, 255), (200, 200, 255), (200, 200, 255),
            (200, 200, 255), GREEN, YELLOW]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 180, 150, W - 180, 560, "branch_plan.txt", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "size the mask to the hosts, not the habit",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ comptia-a-plus (story x1 + bbg x1 + primer x1)
def scene_aplus_post(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE PC THAT WILL NOT POST", font(F_SERIFB, 38), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 200), "power on\u2026 fans spin\u2026 and nothing. no display, no beep of life.",
            font(F_SERIF, 28), CREAM, anchor="mm")
    if t > 9:
        txt(dr, (W // 2, 280), "the PC is talking \u2014 in beeps:", font(F_SERIF, 26), GOLD, anchor="mm")
        beeps = [("1 long, 2 short", "video card"), ("continuous", "power supply"),
                 ("no beeps at all", "CPU or RAM")]
        for i, (b, dev) in enumerate(beeps):
            if t > 9 + i * 2:
                y = 340 + i * 52
                txt(dr, (W // 2 - 260, y), b, font(F_MONOB, 24), RED, anchor="lm")
                txt(dr, (W // 2 + 260, y), "\u2192 " + dev, font(F_SERIF, 24), (200, 185, 160), anchor="lm")
    if t > 16:
        bar(dr, 340, 520, 600, 44, clamp((t - 16) / 3), GOLD, "reseating DIMM 1\u2026", "click")
    if t > 20:
        txt(dr, (W // 2, 600), "POST passes \u2014 the RAM just wasn't seated",
            font(F_SERIF, 28), GREEN, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 650), "diagnose before you replace \u2014 the cheapest part is the one you never buy",
            font(F_SERIF, 24), GOLD, anchor="mm")

def scene_aplus_ransom(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE RANSOMWARE MORNING", CYAN)
    if t > 4:
        for i, nm in enumerate(["WS-101", "WS-102", "WS-103"]):
            x = 300 + i * 340
            infected = (i == 1 and t > 8)
            col = RED if infected else GREEN
            dr.rectangle([x - 110, 240, x + 110, 400], fill=(10, 16, 28), outline=col, width=4)
            txt(dr, (x, 300), nm, font(F_BOLD, 26), WHITE, anchor="mm")
            txt(dr, (x, 350), "ENCRYPTED" if infected else "clean", font(F_MONO, 22), col, anchor="mm")
    if t > 10:
        steps = [("1. ISOLATE", "pull the cable", 470, YELLOW),
                 ("2. DON'T PAY", "no guarantee", 530, RED),
                 ("3. RESTORE", "last night's backup", 590, GREEN)]
        for lab, sub, y, col in steps:
            txt(dr, (W // 2, y), lab + " \u2014 " + sub, font(F_BOLD, 26), col, anchor="mm")
    if t > 15:
        bar(dr, 340, 620, 600, 40, clamp((t - 15) / 4), GREEN, "restoring WS-102", "100%")
    if t > 21:
        txt(dr, (W // 2, 130), "3-2-1 backups turn ransomware into a bad afternoon",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_aplus_tickets(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "TRIAGE THE MORNING TICKET QUEUE", font(F_BOLD, 34), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "twelve tickets, one tech \u2014 the queue is a sorting algorithm",
        font(F_SANS, 24), DIM, anchor="mm")
    _r.seed(777)
    tickets = [("ransomware?", 1), ("no internet", 1), ("printer jam", 4), ("slow PC", 3),
               ("password reset", 3), ("VPN down", 2), ("new hire setup", 3), ("email phish", 1),
               ("monitor flicker", 4), ("server alert", 2), ("wifi dead zone", 2), ("toner low", 4)]
    _r.shuffle(tickets)
    k = clamp((t - 5) / 6)
    nshow = int(len(tickets) * k)
    pcol = {1: RED, 2: ORANGE, 3: YELLOW, 4: DIM}
    for i, (nm, pr) in enumerate(tickets[:nshow]):
        x = 200 + (i % 6) * 150
        y = 190 + (i // 6) * 110
        dr.rectangle([x, y, x + 130, y + 80], fill=(14, 20, 34), outline=pcol[pr], width=3)
        txt(dr, (x + 65, y + 28), "P%d" % pr, font(F_BOLD, 24), pcol[pr], anchor="mm")
        txt(dr, (x + 65, y + 58), nm, font(F_SANS, 15), CREAM, anchor="mm")
    if t > 14:
        ordered = sorted(tickets, key=lambda x: x[1])
        txt(dr, (W // 2, 470), "sorted by impact \u00d7 urgency:", font(F_SANS, 26), TEAL, anchor="mm")
        for i, (nm, pr) in enumerate(ordered[:6]):
            x = 170 + i * 160
            dr.rectangle([x, 510, x + 140, 580], fill=(10, 18, 26), outline=pcol[pr], width=3)
            txt(dr, (x + 70, 545), "#%d %s" % (i + 1, nm), font(F_SANS, 16), WHITE, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "triage = impact \u00d7 urgency \u2014 work the P1s, batch the P4s",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ comptia-network-plus (bbg x1 + fireship x1 + 3b1b x1)
def scene_netplus_leak(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE VLAN THAT LEAKED", CYAN)
    if t > 4:
        panel(dr, [140, 240, 480, 440], "SW-A", TEAL)
        panel(dr, [800, 240, 1140, 440], "SW-B", TEAL)
        dr.line([480, 340, 800, 340], fill=CYAN, width=6)
        txt(dr, (640, 300), "trunk \u00b7 native VLAN 1", font(F_MONOB, 22), CYAN, anchor="mm")
        txt(dr, (310, 490), "attacker", font(F_SANS, 22), RED, anchor="mm")
        txt(dr, (970, 490), "VLAN 20: finance", font(F_SANS, 22), YELLOW, anchor="mm")
    if t > 9:
        k = clamp((t - 9) / 4)
        fx = 480 + k * 320
        dr.ellipse([fx - 12, 328, fx + 12, 352], fill=RED)
        dr.ellipse([fx - 20, 320, fx + 20, 360], outline=RED, width=2)
        txt(dr, (640, 390), "double-tagged: 802.1Q inside 802.1Q", font(F_MONO, 24), RED, anchor="mm")
    if t > 14:
        txt(dr, (W // 2, 180), "native VLAN mismatch + DTP auto = the leak",
            font(F_SANS, 26), RED, anchor="mm")
        txt(dr, (970, 560), "finance frames readable!", font(F_BOLD, 24), RED, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 180), "fix: native VLAN \u2192 999 (unused) \u00b7 DTP off",
            font(F_SANS, 26), GREEN, anchor="mm")
        txt(dr, (970, 560), "VLAN 20: sealed", font(F_BOLD, 24), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 640), "tag what you must, prune the rest \u2014 native VLANs are attack surface",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_netplus_carve(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "CARVE THE /24 IN 100 SECONDS", MAGENTA)
    lines = ["# 192.168.1.0/24 \u2192 four /26s", "borrow 2 bits: 2^2 = 4 subnets",
             ".0/26   .64/26   .128/26   .192/26", "new mask: 255.255.255.192",
             "62 usable hosts per subnet", "2^n - 2 \u2014 never forget the -2"]
    cols = [(200, 200, 255), YELLOW, GREEN, (200, 200, 255), (200, 200, 255), ORANGE]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 180, 150, W - 180, 560, "carve.py", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "borrow bits for subnets \u2014 host bits stay for hosts",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_netplus_storm(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "HALF THE OFFICE IS OFFLINE", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "two switches, one loop, no spanning tree \u2014 broadcasts multiply",
        font(F_SANS, 24), DIM, anchor="mm")
    if t > 4:
        dr.ellipse([340 - 60, 200 - 60, 340 + 60, 200 + 60], fill=(14, 20, 34), outline=TEAL, width=4)
        dr.ellipse([940 - 60, 200 - 60, 940 + 60, 200 + 60], fill=(14, 20, 34), outline=TEAL, width=4)
        txt(dr, (340, 200), "SW-A", font(F_BOLD, 24), WHITE, anchor="mm")
        txt(dr, (940, 200), "SW-B", font(F_BOLD, 24), WHITE, anchor="mm")
        dr.line([400, 200, 880, 200], fill=DIM, width=4)
        dr.line([340, 260, 940, 260], fill=DIM, width=4)
        txt(dr, (640, 300), "LOOP \u2014 no STP", font(F_BOLD, 24), RED, anchor="mm")
    ox, oy, pw, ph = 180, 620, 920, 220
    dr.rectangle([ox, oy - ph, ox + pw, oy], outline=DIM, width=2)
    txt(dr, (ox, oy - ph - 12), "broadcast pps", font(F_SANS, 22), RED, anchor="lb")
    k = clamp((t - 5) / 11)
    pts = []
    for i in range(int(70 * k)):
        x = ox + i / 70 * pw
        y = oy - (math.exp(i / 70 * 2.6) - 1) / (math.exp(2.6) - 1) * ph
        pts.append((x, y))
    if len(pts) > 1:
        dr.line(pts, fill=RED, width=4)
    if t > 16:
        dr.line([400, 260, 880, 260], fill=(10, 16, 28), width=8)
        txt(dr, (640, 300), "STP blocks the port", font(F_BOLD, 24), GREEN, anchor="mm")
        k2 = clamp((t - 16) / 6)
        pts2 = []
        for i in range(int(40 * k2)):
            x = ox + pw * 0.62 + i / 40 * pw * 0.36
            y = oy - ph * 0.85 * math.exp(-i / 40 * 3)
            pts2.append((x, y))
        if len(pts2) > 1:
            dr.line(pts2, fill=GREEN, width=4)
    if t > 22:
        txt(dr, (W // 2, 668), "loops amplify \u2014 spanning tree prunes",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ comptia-security-plus (bbg x1 + fireship x1 + story x1)
def scene_secplus_threat(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "KNOW THE ATTACKER'S MENU", CYAN)
    if t > 4:
        txt(dr, (W // 2, 180), "the threat actor menu: pick your poison", font(F_SANS, 26), DIM, anchor="mm")
    actors = [("script kiddie", 6, "low skill, loud tools", GREEN),
              ("hacktivist", 9, "cause over cash", YELLOW),
              ("organized crime", 12, "ransomware as a business", ORANGE),
              ("nation-state", 15, "patient, funded, silent", RED)]
    for i, (nm, born, note, col) in enumerate(actors):
        if t < born:
            continue
        y = 250 + i * 92
        k = clamp((t - born) / 1.2)
        w = int(880 * k)
        dr.rectangle([W // 2 - w // 2, y - 32, W // 2 + w // 2, y + 32],
                     fill=(12, 18, 32), outline=col, width=3)
        txt(dr, (W // 2 - 380, y), nm.upper(), font(F_BOLD, 24), col, anchor="lm")
        txt(dr, (W // 2 + 380, y), note, font(F_SANS, 22), DIM, anchor="rm")
    if t > 21:
        txt(dr, (W // 2, 640), "motive predicts method \u2014 defend against the actor, not the alert",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_secplus_crypto(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "CRYPTO THAT MATTERS IN 100 SECONDS", MAGENTA)
    lines = ["symmetric: one key, fast, AES-256     # bulk data",
             "asymmetric: two keys, RSA/ECC          # key exchange",
             "hashing: one way, SHA-256             # integrity",
             "TLS = asymmetric handshake, symmetric session",
             "never roll your own \u2014 use the vetted primitives",
             "key length is the moat: 256 bits is the standard"]
    cols = [(200, 200, 255), (200, 200, 255), (200, 200, 255),
            YELLOW, RED, (200, 200, 255)]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 120, 150, W - 120, 560, "crypto_cheatsheet.txt", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "confidentiality, integrity, authenticity \u2014 pick the primitive that fits",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_secplus_click(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE CLICK HEARD ROUND THE OFFICE", font(F_SERIFB, 34), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "an invoice from the CEO \u2014 except the CEO was on a plane",
            font(F_SERIF, 28), CREAM, anchor="mm")
        txt(dr, (W // 2, 270), "one click, and the macro reached out to its master",
            font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    if t > 11:
        txt(dr, (W // 2, 380), "the EDR caught the callback \u2014 the SOC had the host in four minutes",
            font(F_SERIF, 26), YELLOW, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 480), "the user reported it in six \u2014 no shame, just speed",
            font(F_SERIF, 27), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 590), "users are sensors, not liabilities \u2014 reward the report",
            font(F_SERIF, 26), GOLD, anchor="mm")

# ============================================================ isc2-cc (bbg x1 + fireship x1 + primer x1)
def scene_isc2_principles(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE FIVE PILLARS OF CC", CYAN)
    pillars = [("security\nprinciples", 5, CYAN), ("business\ncontinuity", 8, TEAL),
               ("access\ncontrol", 11, YELLOW), ("network\nsecurity", 14, ORANGE),
               ("security\noperations", 17, GREEN)]
    for i, (nm, born, col) in enumerate(pillars):
        if t < born:
            continue
        x = 170 + i * 230
        k = clamp((t - born) / 1.5)
        hh = int(300 * k)
        dr.rectangle([x - 90, 560 - hh, x + 90, 560], fill=(12, 18, 32), outline=col, width=3)
        for j, ln in enumerate(nm.split("\n")):
            txt(dr, (x, 590 + j * 28), ln.upper(), font(F_BOLD, 20), col, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 180), "five domains, one mindset: protect the mission",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_isc2_cia(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE CIA TRIAD IN 100 SECONDS", MAGENTA)
    lines = ["confidentiality: only the right eyes    # encryption, ACLs",
             "integrity: the data never changed       # hashes, signatures",
             "availability: there when you need it    # redundancy, backups",
             "break one \u2192 the triad collapses",
             "every control maps to a corner \u2014 learn the map",
             "CC exam day: if in doubt, pick the triad answer"]
    cols = [CYAN, YELLOW, GREEN, RED, (200, 200, 255), (150, 160, 190)]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 120, 150, W - 120, 560, "triad.txt", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "three corners, every question \u2014 the triad is the CC skeleton key",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_isc2_access(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "WHO GETS IN? AN ACCESS SIM", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "subjects request, objects decide \u2014 watch the policy engine work",
        font(F_SANS, 24), DIM, anchor="mm")
    reqs = [("alice: eng", "db-prod", True), ("bob: intern", "db-prod", False),
            ("carol: eng", "repo", True), ("dave: vendor", "vpn", False),
            ("erin: sec", "siem", True), ("frank: eng", "hr-files", False)]
    k = clamp((t - 5) / 12)
    nshow = int(len(reqs) * k)
    for i, (subj, obj, ok) in enumerate(reqs[:nshow]):
        y = 200 + i * 70
        col = GREEN if ok else RED
        txt(dr, (300, y), subj, font(F_MONO, 24), CREAM, anchor="lm")
        arrow(dr, 480, y, 560, y, DIM, 3)
        txt(dr, (600, y), obj, font(F_MONO, 24), CREAM, anchor="lm")
        dr.ellipse([900 - 18, y - 18, 900 + 18, y + 18], fill=col)
        txt(dr, (900, y), "\u2713" if ok else "\u2717", font(F_BOLD, 22), WHITE, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 640), "least privilege: default-deny, then grant what the role needs \u2014 nothing more",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ m365-endpoint-admin (bbg x1 + fireship x1 + story x1)
def scene_m365_compliance(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "COMPLIANT OR QUARANTINED", CYAN)
    if t > 4:
        txt(dr, (W // 2, 180), "Intune evaluates every device against the policy", font(F_SANS, 26), DIM, anchor="mm")
    checks = [("OS patched", 6, True), ("disk encrypted", 9, True),
              ("jailbreak detected", 12, False), ("antivirus current", 15, True)]
    for i, (nm, born, good) in enumerate(checks):
        if t < born:
            continue
        y = 260 + i * 70
        col = GREEN if good else RED
        dr.ellipse([340 - 16, y - 16, 340 + 16, y + 16], fill=col)
        txt(dr, (380, y), nm, font(F_SANS, 26), CREAM, anchor="lm")
        txt(dr, (760, y), "PASS" if good else "FAIL", font(F_MONOB, 26), col, anchor="lm")
    if t > 18:
        dr.rectangle([W // 2 - 280, 540, W // 2 + 280, 610], fill=(40, 14, 14), outline=RED, width=4)
        txt(dr, (W // 2, 575), "NONCOMPLIANT \u2192 conditional access blocks", font(F_BOLD, 26), RED, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 660), "one failing check sinks the device \u2014 compliance is binary",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_m365_autopilot(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "AUTOPILOT IN 100 SECONDS", MAGENTA)
    lines = ["# the laptop ships straight to the user",
             "1. unbox \u2192 sign in with Entra ID",
             "2. Autopilot profile applies: apps, policies, certs",
             "3. zero-touch: no imaging, no USB, no desk visit",
             "4. device lands compliant \u00b7 user productive in 20 min",
             "old way: 3 days in the queue \u00b7 new way: the box does it"]
    cols = [(150, 160, 190), (200, 200, 255), (200, 200, 255),
            YELLOW, GREEN, (200, 200, 255)]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 120, 150, W - 120, 560, "autopilot.md", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "the factory ships the shell \u2014 the cloud finishes the build",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_m365_wipe(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE LOST PHONE AT THE AIRPORT", font(F_SERIFB, 36), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "the sales lead's phone \u2014 left at the gate, flight boarding",
            font(F_SERIF, 28), CREAM, anchor="mm")
        txt(dr, (W // 2, 270), "it holds the customer list, the contracts, the pricing",
            font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    if t > 11:
        txt(dr, (W // 2, 380), "Intune: selective wipe \u2014 corporate data only",
            font(F_MONO, 26), YELLOW, anchor="mm")
        txt(dr, (W // 2, 440), "the family photos survive \u2014 the contracts evaporate",
            font(F_SERIF, 26), CREAM, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 540), "the phone is found at lost-and-found \u2014 a clean brick of glass",
            font(F_SERIF, 26), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 620), "manage the data, not just the device \u2014 wipe is a scalpel",
            font(F_SERIF, 26), GOLD, anchor="mm")

# ============================================================ aws-cloud-practitioner-plus (bbg x1 + fireship x1 + primer x1)
def scene_aws_shared(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "SECURITY: WHOSE JOB IS IT?", CYAN)
    if t > 4:
        dr.rectangle([W // 2 - 420, 200, W // 2 + 420, 330], fill=(14, 20, 34), outline=ORANGE, width=4)
        txt(dr, (W // 2, 250), "AWS: security OF the cloud", font(F_BOLD, 28), ORANGE, anchor="mm")
        txt(dr, (W // 2, 295), "hardware \u00b7 facilities \u00b7 hypervisor \u00b7 network fabric",
            font(F_SANS, 23), DIM, anchor="mm")
    if t > 9:
        dr.rectangle([W // 2 - 420, 360, W // 2 + 420, 520], fill=(14, 20, 34), outline=CYAN, width=4)
        txt(dr, (W // 2, 410), "YOU: security IN the cloud", font(F_BOLD, 28), CYAN, anchor="mm")
        txt(dr, (W // 2, 455), "data \u00b7 IAM \u00b7 OS patching \u00b7 firewall rules \u00b7 encryption",
            font(F_SANS, 23), DIM, anchor="mm")
    if t > 15:
        arrow(dr, W // 2, 335, W // 2, 355, WHITE, 5)
        txt(dr, (W // 2 + 450, 380), "the line\nmoves with\nthe service", font(F_SANS, 20), DIM, anchor="lm")
    if t > 21:
        txt(dr, (W // 2, 620), "misconfigured S3 is YOUR breach \u2014 the line is the exam's favorite question",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_aws_regions(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "REGIONS AND AZs IN 100 SECONDS", MAGENTA)
    lines = ["# region: a geography. AZ: a building (or three).",
             "us-east-1 = N. Virginia \u00b7 6 AZs",
             "deploy across 3 AZs \u2192 one fire can't take you down",
             "edge locations = CloudFront caches \u00b7 400+ globally",
             "data residency: pick the region the law picks",
             "multi-region = multi-bill \u2014 start with multi-AZ"]
    cols = [(150, 160, 190), (200, 200, 255), YELLOW, (200, 200, 255),
            (200, 200, 255), ORANGE]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 120, 150, W - 120, 560, "regions.txt", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "AZs are the unit of survival \u2014 regions are the unit of law",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_aws_bill(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "THE BILL THAT ATE THE BUDGET", font(F_BOLD, 36), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "watch a forgotten GPU instance burn money, hour by hour",
        font(F_SANS, 24), DIM, anchor="mm")
    k = clamp((t - 5) / 14)
    hours = int(720 * k)
    cost = hours * 3.06
    bar(dr, 240, 280, 800, 60, k, RED, "p3.2xlarge left running", "$%.0f" % cost)
    txt(dr, (240, 420), "hour %d / 720" % hours, font(F_MONO, 26), CREAM, anchor="lm")
    txt(dr, (1040, 420), "rate: $3.06/hr", font(F_MONO, 24), RED, anchor="rm")
    if t > 17:
        txt(dr, (W // 2, 520), "budgets + alerts + auto-shutdown \u2014 the FinOps trinity",
            font(F_SANS, 26), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 600), "the cloud bills by the second \u2014 idle is the most expensive state",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ devops-zero-to-hire (story x1 + bbg x1 + fireship x1)
def scene_devops_deploy(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE FRIDAY DEPLOY", font(F_SERIFB, 40), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "4:47 PM \u2014 'just one small change, straight to prod'",
            font(F_SERIF, 28), CREAM, anchor="mm")
        txt(dr, (W // 2, 270), "no tests, no canary, no rollback plan",
            font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    if t > 11:
        txt(dr, (W // 2, 380), "5:03 PM \u2014 checkout is down. the small change was not small.",
            font(F_SERIF, 27), RED, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 480), "the fix that took ten minutes to ship took four hours to undo",
            font(F_SERIF, 26), YELLOW, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 590), "no Friday deploys \u2014 and never a deploy you can't roll back",
            font(F_SERIF, 26), GOLD, anchor="mm")

def scene_devops_pipeline(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE PIPELINE THAT SAVES FRIDAYS", CYAN)
    stages = [("commit", 5, CYAN), ("build", 9, TEAL), ("test", 13, YELLOW),
              ("scan", 17, ORANGE), ("deploy", 21, GREEN)]
    for i, (nm, born, col) in enumerate(stages):
        if t < born:
            continue
        x = 170 + i * 230
        glow_box(dr, [x - 100, 260, x + 100, 420], col, rad=10, layers=2)
        dr.rectangle([x - 100, 260, x + 100, 420], fill=(10, 16, 28))
        txt(dr, (x, 320), nm.upper(), font(F_BOLD, 24), col, anchor="mm")
        txt(dr, (x, 375), "auto", font(F_SANS, 20), DIM, anchor="mm")
        if i > 0:
            arrow(dr, 170 + (i - 1) * 230 + 105, 340, x - 105, 340, DIM, 4)
    if t > 22:
        txt(dr, (W // 2, 560), "every commit walks the same gauntlet \u2014 humans review, machines verify",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_devops_git(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "GIT IN 100 SECONDS", MAGENTA)
    lines = ["git init \u00b7 git add . \u00b7 git commit -m 'ship it'",
             "branch: a parallel universe for your idea",
             "merge: the universes collide (resolve conflicts)",
             "rebase: rewrite history \u2014 only YOUR history",
             "push: share it \u00b7 pull: catch up",
             "force-push to main: how to make enemies"]
    cols = [(200, 200, 255), (200, 200, 255), (200, 200, 255),
            YELLOW, (200, 200, 255), RED]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "git.sh", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "commit early, branch often \u2014 main is sacred",
            font(F_SANS, 26), CREAM, anchor="mm")

# ============================================================ devsecops-mastery (bbg x1 + fireship x1 + story x1)
def scene_dso_shiftleft(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "SHIFT SECURITY LEFT", CYAN)
    if t > 4:
        dr.line([180, 400, 1100, 400], fill=DIM, width=5)
        for x, lab in [(180, "code"), (410, "build"), (640, "test"), (870, "deploy"), (1100, "prod")]:
            dr.ellipse([x - 12, 388, x + 12, 412], fill=CYAN)
            txt(dr, (x, 450), lab, font(F_SANS, 22), DIM, anchor="mm")
    if t > 9:
        k = clamp((t - 9) / 3)
        bx = 180 + (640 - 180) * k
        dr.rectangle([bx - 130, 240, bx + 130, 310], fill=(40, 10, 10), outline=RED, width=4)
        txt(dr, (bx, 275), "vuln found HERE ($)", font(F_BOLD, 24), RED, anchor="mm")
    if t > 14:
        k = clamp((t - 14) / 3)
        bx = 180 + (1100 - 180) * k
        dr.rectangle([bx - 160, 480, bx + 160, 550], fill=(50, 10, 10), outline=RED, width=4)
        txt(dr, (bx, 515), "vuln found HERE ($$$$$$)", font(F_BOLD, 24), RED, anchor="mm")
    if t > 20:
        txt(dr, (W // 2, 640), "the same bug costs 100\u00d7 more in prod \u2014 scan where the code is born",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_dso_sast(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "THE SAST SCAN IN 100 SECONDS", MAGENTA)
    lines = ["# the scanner reads code it never runs",
             "query = 'SELECT * FROM users WHERE id=' + user_input",
             "         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
             "CRITICAL: SQL injection, line 42",
             "fix: parameterized queries \u2014 never string concat",
             "the pipeline blocks the merge \u00b7 the vuln never ships"]
    cols = [(150, 160, 190), (200, 200, 255), RED, RED, GREEN, YELLOW]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 120, 150, W - 120, 560, "sast_report.txt", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "static analysis reads the code's mind \u2014 fix it before it compiles",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_dso_secret(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE SECRET IN THE REPO", font(F_SERIFB, 38), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "AWS_KEY = 'AKIA\u2026' \u2014 committed at 2 AM, pushed to public",
            font(F_MONO, 25), RED, anchor="mm")
        txt(dr, (W // 2, 270), "by 2:04 the bots had it \u2014 by 2:11 the bill was $4,000",
            font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    if t > 12:
        txt(dr, (W // 2, 380), "rotate the key \u2014 then purge the history, it never forgets",
            font(F_SERIF, 26), YELLOW, anchor="mm")
    if t > 17:
        txt(dr, (W // 2, 480), "vaults, not variables \u2014 secrets live in the manager, never the repo",
            font(F_SERIF, 27), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 590), "git history is forever \u2014 so are leaked keys. scan every commit.",
            font(F_SERIF, 26), GOLD, anchor="mm")

# ============================================================ iac-terraform-gitops (bbg x1 + fireship x1 + primer x1)
def scene_iac_state(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "THE STATE FILE IS THE TRUTH", CYAN)
    if t > 4:
        panel(dr, [140, 200, 480, 400], "YOUR CODE", CYAN)
        txt(dr, (310, 330), "main.tf:\n3 EC2", font(F_MONO, 22), DIM, anchor="mm")
        panel(dr, [800, 200, 1140, 400], "REALITY", TEAL)
        txt(dr, (970, 330), "AWS:\n3 EC2", font(F_MONO, 22), DIM, anchor="mm")
        dr.rectangle([540, 260, 740, 340], fill=(10, 16, 28), outline=YELLOW, width=3)
        txt(dr, (640, 300), "state", font(F_BOLD, 26), YELLOW, anchor="mm")
    if t > 11:
        txt(dr, (970, 450), "someone launched #4\nby hand \u2014 DRIFT", font(F_SANS, 24), RED, anchor="mm")
        arrow(dr, 800, 400, 800, 440, RED, 5)
    if t > 16:
        txt(dr, (W // 2, 540), "terraform plan: 1 to add, 0 to change, 0 to destroy?",
            font(F_MONO, 25), YELLOW, anchor="mm")
        txt(dr, (W // 2, 590), "the state file tattles \u2014 plan exposes the drift",
            font(F_SANS, 25), CREAM, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "click-ops is drift \u2014 the state file is the only truth",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_iac_apply(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "TERRAFORM APPLY IN 100 SECONDS", MAGENTA)
    lines = ["resource \"aws_instance\" \"web\" {",
             "  ami           = \"ami-0c55b159cbfafe1f0\"",
             "  instance_type = \"t3.micro\"",
             "}",
             "terraform plan   # preview: +3 to add",
             "terraform apply  # 'yes' \u2014 and the cloud obeys"]
    cols = [(200, 200, 255), (200, 200, 255), (200, 200, 255),
            (200, 200, 255), YELLOW, GREEN]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "main.tf", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "declare the end state \u2014 terraform computes the diff",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_iac_drift(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "DRIFT: THE CONFIG THAT WANDERED", font(F_BOLD, 34), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "git says one thing \u2014 the cluster says another. watch the gap grow.",
        font(F_SANS, 24), DIM, anchor="mm")
    k = clamp((t - 5) / 14)
    n = int(12 * k)
    _r.seed(4242)
    for i in range(12):
        x = 190 + i * 80
        synced = i >= n or _r.random() > 0.25
        col = TEAL if (i >= n or synced) else RED
        y_top = 300 if synced or i >= n else 300 + 60
        dr.rectangle([x, y_top, x + 56, y_top + 90], fill=col)
        txt(dr, (x + 28, y_top + 110), "svc-%d" % (i + 1), font(F_MONO, 16), DIM, anchor="mm")
    txt(dr, (W // 2, 540), "drifted: %d / 12 services" % sum(1 for i in range(n) if _r.Random(4242 + i).random() < 0.25),
        font(F_MONO, 24), RED, anchor="mm")
    if t > 17:
        dr.rectangle([W // 2 - 300, 570, W // 2 + 300, 620], fill=(8, 24, 16), outline=GREEN, width=3)
        txt(dr, (W // 2, 595), "argocd sync \u2014 git becomes truth again", font(F_BOLD, 24), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 660), "GitOps: the repo is the source of truth \u2014 the agent enforces it",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ k8s-cka-exceed (bbg x1 + fireship x1 + 3b1b x1)
def scene_cka_schedule(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "WHERE DOES THE POD LAND?", CYAN)
    if t > 4:
        for i, nm in enumerate(["node-1", "node-2", "node-3"]):
            x = 300 + i * 340
            dr.rectangle([x - 130, 200, x + 130, 420], fill=(12, 18, 32), outline=CYAN, width=3)
            txt(dr, (x, 240), nm, font(F_MONOB, 24), CYAN, anchor="mm")
            txt(dr, (x, 380), "4 CPU free" if i < 2 else "0 CPU free", font(F_MONO, 20),
                GREEN if i < 2 else RED, anchor="mm")
    if t > 10:
        txt(dr, (W // 2, 180), "pod requests 2 CPU \u2014 the scheduler filters, then scores",
            font(F_SANS, 24), DIM, anchor="mm")
        dr.rectangle([W // 2 - 110, 480, W // 2 + 110, 560], fill=(16, 26, 48), outline=YELLOW, width=3)
        txt(dr, (W // 2, 520), "pod: web-7", font(F_MONOB, 24), YELLOW, anchor="mm")
        k = clamp((t - 10) / 4)
        px = W // 2 + (300 - W // 2) * k
        dr.rectangle([px - 110, 480, px + 110, 560], fill=(16, 26, 48), outline=YELLOW, width=3)
        txt(dr, (px, 520), "pod: web-7", font(F_MONOB, 24), YELLOW, anchor="mm")
    if t > 16:
        txt(dr, (300, 600), "node-1: least loaded \u2192 scheduled", font(F_SANS, 24), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 660), "filter the infeasible, score the rest \u2014 the scheduler is an optimizer",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_cka_kubectl(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, "KUBECTL IN 100 SECONDS", MAGENTA)
    lines = ["kubectl get pods -A          # what's running where",
             "kubectl describe pod web-7   # why is it CrashLooping?",
             "kubectl logs web-7 --previous  # the last words",
             "kubectl exec -it web-7 -- sh   # step inside",
             "kubectl apply -f deploy.yaml   # declare, don't imperate",
             "kubectl delete pod web-7       # cattle, not pets"]
    cols = [(200, 200, 255)] * 5 + [ORANGE]
    lns = [(s, c) for s, c in zip(lines, cols)]
    hi = int(clamp((t - 5) / 12) * len(lines))
    code_panel(dr, 150, 150, W - 150, 560, "kubectl.sh", lns, hi_line=hi, t=t)
    if t > 20:
        txt(dr, (W // 2, 610), "get, describe, logs \u2014 the debugging trinity",
            font(F_SANS, 26), CREAM, anchor="mm")

def scene_cka_replicas(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "HOW MANY REPLICAS SURVIVE?", font(F_BOLD, 38), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "n replicas, one node dies \u2014 the math of quorum",
        font(F_SANS, 24), DIM, anchor="mm")
    k = clamp((t - 5) / 12)
    for r in [1, 2, 3, 5]:
        i = [1, 2, 3, 5].index(r)
        x = 240 + i * 260
        txt(dr, (x, 220), "replicas: %d" % r, font(F_BOLD, 28), CREAM, anchor="mm")
        nshow = int(r * k)
        for j in range(r):
            y = 280 + j * 66
            alive = j < nshow - (1 if (t > 16 and j == 0) else 0)
            col = TEAL if alive else RED
            dr.ellipse([x - 26, y - 26, x + 26, y + 26], fill=(14, 20, 34), outline=col, width=3)
            txt(dr, (x, y), "p%d" % j, font(F_MONO, 18), col, anchor="mm")
        quorum = r // 2 + 1
        ok = nshow - (1 if t > 16 else 0) >= quorum
        txt(dr, (x, 280 + r * 66 + 20), "quorum %d: %s" % (quorum, "HELD" if (t <= 16 or ok) else "LOST"),
            font(F_BOLD, 22), GREEN if (t <= 16 or ok) else RED, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 180), "one node dies \u2014 who still has quorum?",
            font(F_SANS, 24), RED, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 640), "odd numbers win elections \u2014 3 and 5 survive, 1 and 2 gamble",
            font(F_SANS, 25), CREAM, anchor="mm")

# ============================================================ kubernetes-sre (bbg x1 + primer x1 + story x1)
def scene_sre_budget(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"])
    dot_grid(dr)
    bbg_title(dr, "SPEND THE ERROR BUDGET", CYAN)
    if t > 4:
        txt(dr, (W // 2, 180), "SLO: 99.9% \u2014 the budget is 43 minutes of downtime a month",
            font(F_SANS, 26), DIM, anchor="mm")
    k = clamp((t - 6) / 12)
    bar(dr, 240, 300, 800, 64, k, RED if k > 0.8 else (YELLOW if k > 0.5 else GREEN),
        "error budget consumed", "%d%%" % int(k * 100))
    if t > 14:
        txt(dr, (W // 2, 440), "budget at 92% \u2014 feature freeze, reliability work only",
            font(F_BOLD, 28), RED, anchor="mm")
    if t > 18:
        txt(dr, (W // 2, 520), "budget healthy \u2014 ship fast, take risks",
            font(F_BOLD, 28), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 620), "the budget turns reliability into a currency \u2014 spend it deliberately",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_sre_chaos(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "BREAK IT ON PURPOSE", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), "chaos experiment: kill a zone at noon \u2014 on purpose",
        font(F_SANS, 24), DIM, anchor="mm")
    zones = [(300, "zone-a"), (640, "zone-b"), (980, "zone-c")]
    k = clamp((t - 5) / 12)
    _r.seed(99)
    for i, (x, nm) in enumerate(zones):
        dead = (i == 1 and t > 10)
        col = RED if dead else TEAL
        dr.rectangle([x - 110, 220, x + 110, 420], fill=(14, 20, 34), outline=col, width=4)
        txt(dr, (x, 260), nm, font(F_MONOB, 24), col, anchor="mm")
        txt(dr, (x, 320), "DEAD" if dead else "SERVING", font(F_BOLD, 26), col, anchor="mm")
        lvl = 0 if dead else clamp(0.4 + 0.3 * k + (0.2 if i != 1 else 0))
        bar(dr, x - 90, 360, 180, 26, lvl, col)
    if t > 14:
        txt(dr, (W // 2, 500), "traffic reroutes \u2014 p99 latency +40ms, zero errors",
            font(F_SANS, 26), YELLOW, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 580), "hypothesis confirmed: the system survives zone loss",
            font(F_SANS, 26), GREEN, anchor="mm")
    if t > 22:
        txt(dr, (W // 2, 640), "chaos is a vaccine \u2014 small controlled doses build immunity",
            font(F_SANS, 25), CREAM, anchor="mm")

def scene_sre_page(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    warm_rings(dr)
    txt(dr, (W // 2, 90), "THE 3 AM PAGE", font(F_SERIFB, 40), GOLD, anchor="mm")
    if t > 5:
        txt(dr, (W // 2, 210), "the pager screams \u2014 error rate 40%, climbing",
            font(F_SERIF, 28), RED, anchor="mm")
        txt(dr, (W // 2, 270), "the dashboard is red \u2014 the runbook is open",
            font(F_SERIF, 26), (200, 185, 160), anchor="mm")
    if t > 11:
        txt(dr, (W // 2, 380), "mitigate first: roll back the deploy, stop the bleed",
            font(F_SERIF, 27), YELLOW, anchor="mm")
    if t > 16:
        txt(dr, (W // 2, 480), "3:41 AM \u2014 green again. now the blameless postmortem.",
            font(F_SERIF, 27), GREEN, anchor="mm")
    if t > 21:
        txt(dr, (W // 2, 590), "blame the system, never the human \u2014 the page is a gift",
            font(F_SERIF, 26), GOLD, anchor="mm")

SLUG_DIR = {
    "ccna": "cisco-ccna", "aplus": "comptia-a-plus",
    "netplus": "comptia-network-plus", "secplus": "comptia-security-plus",
    "isc2": "isc2-cc", "m365": "m365-endpoint-admin",
    "awsclf": "aws-cloud-practitioner-plus", "devops0": "devops-zero-to-hire",
    "devsecops": "devsecops-mastery", "iac": "iac-terraform-gitops",
    "k8scka": "k8s-cka-exceed", "k8ssre": "kubernetes-sre",
}

# ============================================================ VIDEOS registry
def V(kicker, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[slug.split("-")[0]],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    "ccna": "CCNA \u00b7 Cisco Certified Network Associate",
    "aplus": "A+ \u00b7 CompTIA A+ Hardware & Troubleshooting",
    "netplus": "NET+ \u00b7 CompTIA Network+",
    "secplus": "SEC+ \u00b7 CompTIA Security+",
    "isc2": "CC \u00b7 ISC2 Certified in Cybersecurity",
    "m365": "M365 \u00b7 Endpoint Administrator",
    "awsclf": "AWS \u00b7 Cloud Practitioner Plus",
    "devops0": "DEVOPS \u00b7 Zero to Hire",
    "devsecops": "DEVSECOPS \u00b7 DevSecOps Mastery",
    "iac": "IAC \u00b7 Terraform & GitOps",
    "k8scka": "CKA \u00b7 Advanced Kubernetes Administration",
    "k8ssre": "SRE \u00b7 Kubernetes SRE",
}

VIDEOS = [
 # --- cisco-ccna
 V(BOOTCAMP_K["ccna"], "ccna-vlan-dark", "VLAN 30 Goes Dark",
   "allowed lists, not magic", "bbg", scene_ccna_vlan_dark,
   "VLAN 30 dies at the trunk: the allowed-VLAN list only carries VLAN 10 \u2014 one 'allowed vlan add 30' brings it back.",
   [(4,10,"Two switches, one trunk \u2014 VLAN 10 and VLAN 30"),
    (10,16,"VLAN 10 crosses fine \u00b7 VLAN 30: pruned at the trunk"),
    (16,22,"The allowed list was the whole problem \u2014 add VLAN 30"),
    (22,26,"VLANs don't cross trunks by magic \u2014 allowed lists do")]),
 V(BOOTCAMP_K["ccna"], "ccna-ospf-stuck", "The Neighbor That Never Goes Full",
   "neighbors form on agreement", "bbg", scene_ccna_ospf,
   "An OSPF adjacency stuck at EXSTART: MTU 1500 vs 9000 means the DBDs never agree \u2014 match the MTU and walk to FULL.",
   [(4,10,"R1 and R2 in area 0 \u2014 the adjacency begins"),
    (10,16,"DOWN, INIT, 2-WAY \u2014 then stuck at EXSTART"),
    (16,22,"MTU mismatch: 1500 vs 9000 \u2014 the DBDs never agree"),
    (22,26,"Match the MTU \u2014 neighbors form on agreement")]),
 V(BOOTCAMP_K["ccna"], "ccna-subnet-branch", "Subnet a Branch Office in 100 Seconds",
   "size the mask to the hosts", "fireship", scene_ccna_subnet,
   "Carving 192.168.10.0/24 for a branch: HQ gets a /25, the branch a /26, IoT a /28 \u2014 six wasted addresses, not two hundred.",
   [(4,10,"192.168.10.0/24 \u2014 three subnets to carve"),
    (10,16,"HQ: 100 hosts goes to a /25 \u00b7 branch: 40 hosts to a /26"),
    (16,22,"IoT: 12 hosts to a /28 \u00b7 the ranges line up"),
    (22,26,"Size the mask to the hosts, not the habit")]),
 # --- comptia-a-plus
 V(BOOTCAMP_K["aplus"], "aplus-no-post", "The PC That Will Not POST",
   "diagnose before you replace", "story", scene_aplus_post,
   "A PC that powers on with no display: the beeps say the RAM isn't seated \u2014 diagnose before you replace.",
   [(4,10,"Power on \u2026 fans spin \u2026 and nothing \u2014 no display"),
    (10,16,"The PC is talking in beeps \u2014 one long, two short: video"),
    (16,22,"Reseating DIMM 1 \u2026 click \u2014 POST passes"),
    (22,26,"Diagnose before you replace \u2014 the cheapest part is the one you never buy")]),
 V(BOOTCAMP_K["aplus"], "aplus-ransomware", "The Ransomware Morning",
   "3-2-1 backups turn ransomware into a bad afternoon", "bbg", scene_aplus_ransom,
   "Ransomware hits WS-102 in the morning: isolate, don't pay, restore from last night's backup \u2014 3-2-1 turns disaster into a bad afternoon.",
   [(4,10,"Morning: WS-102 is encrypted \u2014 the ransom note is on screen"),
    (10,16,"Step one: isolate \u00b7 step two: don't pay"),
    (16,22,"Step three: restore from last night's backup"),
    (22,26,"3-2-1 backups turn ransomware into a bad afternoon")]),
 V(BOOTCAMP_K["aplus"], "aplus-tickets", "Triage the Morning Ticket Queue",
   "triage = impact \u00d7 urgency", "primer", scene_aplus_tickets,
   "Twelve tickets, one tech: a living sort by impact times urgency \u2014 work the P1s, batch the P4s.",
   [(4,10,"Twelve tickets land \u2014 one technician"),
    (10,16,"The queue is a sorting algorithm: impact times urgency"),
    (16,22,"P1s first: ransomware, no internet \u00b7 P4s batch for later"),
    (22,26,"Triage = impact \u00d7 urgency \u2014 work the P1s, batch the P4s")]),
 # --- comptia-network-plus
 V(BOOTCAMP_K["netplus"], "netplus-vlan-leak", "The VLAN That Leaked",
   "native VLANs are attack surface", "bbg", scene_netplus_leak,
   "A VLAN-hopping attack via double-tagging: the native VLAN mismatch lets finance frames leak \u2014 move native to 999 and turn DTP off.",
   [(4,10,"The trunk carries a native VLAN \u2014 and an attacker"),
    (10,16,"Double-tagged frames: 802.1Q inside 802.1Q"),
    (16,22,"Finance frames readable \u2014 the leak is real"),
    (22,26,"Native VLAN to 999, DTP off \u2014 seal the trunk")]),
 V(BOOTCAMP_K["netplus"], "netplus-carve", "Carve the /24 in 100 Seconds",
   "borrow bits for subnets", "fireship", scene_netplus_carve,
   "Carving 192.168.1.0/24 into four /26s: borrow two bits, new mask 255.255.255.192 \u2014 62 usable hosts per subnet.",
   [(4,10,"192.168.1.0/24 \u2014 four subnets needed"),
    (10,16,"Borrow two bits: 2^2 = four subnets"),
    (16,22,".0, .64, .128, .192 \u2014 mask 255.255.255.192"),
    (22,26,"62 usable hosts each \u2014 never forget the minus two")]),
 V(BOOTCAMP_K["netplus"], "netplus-storm", "Half the Office Is Offline",
   "loops amplify \u2014 spanning tree prunes", "3b1b", scene_netplus_storm,
   "A broadcast storm from a switching loop with no spanning tree: broadcasts multiply exponentially \u2014 STP blocks the port and the storm dies.",
   [(4,10,"Two switches, one loop, no spanning tree"),
    (10,16,"Broadcasts multiply \u2014 the curve goes exponential"),
    (16,22,"STP blocks the redundant port \u2014 the storm collapses"),
    (22,26,"Loops amplify \u2014 spanning tree prunes")]),
 # --- comptia-security-plus
 V(BOOTCAMP_K["secplus"], "secplus-threat-actors", "Know the Attacker's Menu",
   "defend against the actor, not the alert", "bbg", scene_secplus_threat,
   "The threat-actor menu: script kiddies, hacktivists, organized crime, nation-states \u2014 motive predicts method.",
   [(4,10,"Four actors walk in \u2014 all with different motives"),
    (10,16,"Script kiddies: loud \u00b7 hacktivists: causes \u00b7 crime: cash"),
    (16,22,"Nation-states: patient, funded, silent"),
    (22,26,"Motive predicts method \u2014 defend against the actor")]),
 V(BOOTCAMP_K["secplus"], "secplus-crypto", "Crypto That Matters in 100 Seconds",
   "never roll your own", "fireship", scene_secplus_crypto,
   "The crypto that matters: AES for bulk, RSA/ECC for exchange, SHA-256 for integrity \u2014 TLS combines them all. Never roll your own.",
   [(4,10,"Symmetric: one key, fast \u00b7 AES-256 for bulk data"),
    (10,16,"Asymmetric: two keys \u00b7 hashing: one way, for integrity"),
    (16,22,"TLS: asymmetric handshake, symmetric session"),
    (22,26,"Never roll your own \u2014 use the vetted primitives")]),
 V(BOOTCAMP_K["secplus"], "secplus-click", "The Click Heard Round the Office",
   "users are sensors, not liabilities", "story", scene_secplus_click,
   "A phishing click from a fake CEO email: the EDR caught the callback in four minutes, the user reported it in six \u2014 reward the report.",
   [(4,10,"An invoice from the CEO \u2014 except the CEO was on a plane"),
    (10,16,"One click \u2014 the macro reaches out to its master"),
    (16,22,"EDR catches the callback in four minutes \u00b7 the user reports in six"),
    (22,26,"Users are sensors, not liabilities \u2014 reward the report")]),
 # --- isc2-cc
 V(BOOTCAMP_K["isc2"], "isc2-five-pillars", "The Five Pillars of CC",
   "protect the mission", "bbg", scene_isc2_principles,
   "The five CC domains as pillars: security principles, business continuity, access control, network security, security operations.",
   [(4,10,"Five domains, one exam \u2014 meet the pillars"),
    (10,16,"Security principles \u00b7 business continuity \u00b7 access control"),
    (16,22,"Network security \u00b7 security operations"),
    (22,26,"Five domains, one mindset: protect the mission")]),
 V(BOOTCAMP_K["isc2"], "isc2-cia-triad", "The CIA Triad in 100 Seconds",
   "the triad is the CC skeleton key", "fireship", scene_isc2_cia,
   "The CIA triad in sixty seconds: confidentiality, integrity, availability \u2014 every control maps to a corner. The CC skeleton key.",
   [(4,10,"Confidentiality: only the right eyes \u00b7 integrity: never changed"),
    (10,16,"Availability: there when you need it"),
    (16,22,"Break one corner \u2014 the triad collapses"),
    (22,26,"Every control maps to a corner \u2014 learn the map")]),
 V(BOOTCAMP_K["isc2"], "isc2-access-sim", "Who Gets In? An Access Sim",
   "default-deny, then grant the role", "primer", scene_isc2_access,
   "A living access-control simulation: six subjects request six objects \u2014 the policy engine grants the roles and denies the rest.",
   [(4,10,"Subjects request \u2014 objects decide"),
    (10,16,"The engineer reaches the repo \u00b7 the intern is denied prod"),
    (16,22,"The vendor: no VPN \u00b7 security: SIEM access granted"),
    (22,26,"Least privilege: default-deny, then grant what the role needs")]),
 # --- m365-endpoint-admin
 V(BOOTCAMP_K["m365"], "m365-compliance", "Compliant or Quarantined",
   "compliance is binary", "bbg", scene_m365_compliance,
   "Intune compliance: patched, encrypted, clean, current \u2014 one jailbreak fails the device and conditional access blocks it.",
   [(4,10,"Intune evaluates every device against the policy"),
    (10,16,"Patched: pass \u00b7 encrypted: pass \u00b7 jailbreak: FAIL"),
    (16,22,"One failing check sinks the device"),
    (22,26,"Noncompliant means blocked \u2014 compliance is binary")]),
 V(BOOTCAMP_K["m365"], "m365-autopilot", "Autopilot in 100 Seconds",
   "the box does it", "fireship", scene_m365_autopilot,
   "Windows Autopilot: the laptop ships to the user, Entra sign-in applies apps, policies, certs \u2014 productive in twenty minutes, zero imaging.",
   [(4,10,"The laptop ships straight to the user \u2014 no desk visit"),
    (10,16,"Sign in with Entra ID \u00b7 the profile applies everything"),
    (16,22,"Apps, policies, certs \u2014 zero-touch"),
    (22,26,"The factory ships the shell \u2014 the cloud finishes the build")]),
 V(BOOTCAMP_K["m365"], "m365-lost-phone", "The Lost Phone at the Airport",
   "wipe is a scalpel", "story", scene_m365_wipe,
   "A lost phone with the customer list: Intune selective wipe removes corporate data only \u2014 the family photos survive, the contracts evaporate.",
   [(4,10,"The phone is at the gate \u2014 the flight is boarding"),
    (10,16,"It holds the customer list, the contracts, the pricing"),
    (16,22,"Selective wipe: corporate data only \u00b7 photos survive"),
    (22,26,"Manage the data, not just the device \u2014 wipe is a scalpel")]),
 # --- aws-cloud-practitioner-plus
 V(BOOTCAMP_K["awsclf"], "awsclf-shared-resp", "Security: Whose Job Is It?",
   "the line is the exam's favorite question", "bbg", scene_aws_shared,
   "The shared responsibility model: AWS secures OF the cloud, you secure IN it \u2014 misconfigured S3 is your breach, not theirs.",
   [(4,10,"AWS: security OF the cloud \u2014 hardware, facilities, hypervisor"),
    (10,16,"You: security IN the cloud \u2014 data, IAM, patching, firewalls"),
    (16,22,"The line moves with the service \u2014 EC2 vs S3 vs RDS"),
    (22,26,"Misconfigured S3 is YOUR breach \u2014 know the line")]),
 V(BOOTCAMP_K["awsclf"], "awsclf-regions", "Regions and AZs in 100 Seconds",
   "AZs survive, regions obey law", "fireship", scene_aws_regions,
   "Regions are geography, AZs are buildings: deploy across three AZs so one fire can't take you down \u2014 data residency picks the region.",
   [(4,10,"Region: a geography \u00b7 AZ: isolated infrastructure"),
    (10,16,"Three AZs \u2014 one fire can't take you down"),
    (16,22,"Edge locations: 400+ CloudFront caches worldwide"),
    (22,26,"Multi-AZ first \u00b7 multi-region when the law or the budget says so")]),
 V(BOOTCAMP_K["awsclf"], "awsclf-bill-shock", "The Bill That Ate the Budget",
   "idle is the most expensive state", "primer", scene_aws_bill,
   "A forgotten GPU instance burns $3.06 an hour for a month: budgets, alerts, auto-shutdown \u2014 the FinOps trinity.",
   [(4,10,"A p3.2xlarge, left running \u2014 $3.06 an hour"),
    (10,16,"Watch the meter climb: hour by hour, day by day"),
    (16,22,"Month end: the budget is gone"),
    (22,26,"Budgets plus alerts plus auto-shutdown \u2014 idle is the most expensive state")]),
 # --- devops-zero-to-hire
 V(BOOTCAMP_K["devops0"], "devops0-friday-deploy", "The Friday Deploy",
   "never a deploy you can't roll back", "story", scene_devops_deploy,
   "4:47 PM: 'just one small change, straight to prod' \u2014 5:03 PM: checkout is down. No Friday deploys without a rollback.",
   [(4,10,"4:47 PM \u2014 just one small change, straight to prod"),
    (10,16,"No tests, no canary, no rollback plan"),
    (16,22,"5:03 PM: checkout is down \u2014 the change was not small"),
    (22,26,"No Friday deploys \u2014 never a deploy you can't roll back")]),
 V(BOOTCAMP_K["devops0"], "devops0-pipeline", "The Pipeline That Saves Fridays",
   "humans review, machines verify", "bbg", scene_devops_pipeline,
   "The CI/CD gauntlet every commit walks: commit, build, test, scan, deploy \u2014 humans review, machines verify.",
   [(4,10,"Every commit enters the same gauntlet"),
    (10,16,"Build \u00b7 test \u00b7 scan \u2014 automatically"),
    (16,22,"Deploy: only what passed everything"),
    (22,26,"Humans review, machines verify \u2014 the pipeline saves Fridays")]),
 V(BOOTCAMP_K["devops0"], "devops0-git", "Git in 100 Seconds",
   "main is sacred", "fireship", scene_devops_git,
   "Git in sixty seconds: branches are parallel universes, merges collide them, rebase rewrites only your history \u2014 and never force-push main.",
   [(4,10,"Init, add, commit \u2014 the holy trinity"),
    (10,16,"Branches: parallel universes for your idea"),
    (16,22,"Merge collides them \u00b7 rebase rewrites only YOUR history"),
    (22,26,"Commit early, branch often \u2014 main is sacred")]),
 # --- devsecops-mastery
 V(BOOTCAMP_K["devsecops"], "devsecops-shift-left", "Shift Security Left",
   "scan where the code is born", "bbg", scene_dso_shiftleft,
   "A vuln found in code review costs dollars; the same vuln in prod costs a fortune \u2014 shift security left, scan where code is born.",
   [(4,10,"The pipeline: code, build, test, deploy, prod"),
    (10,16,"A vuln found in code: cheap to fix"),
    (16,22,"The same vuln in prod: a hundred times the cost"),
    (22,26,"Shift left \u2014 scan where the code is born")]),
 V(BOOTCAMP_K["devsecops"], "devsecops-sast", "The SAST Scan in 100 Seconds",
   "fix it before it compiles", "fireship", scene_dso_sast,
   "A SAST scan catches SQL injection on line 42: string-concatenated query \u2014 parameterized queries fix it, the pipeline blocks the merge.",
   [(4,10,"The scanner reads code it never runs"),
    (10,16,"Line 42: user input concatenated into SQL \u2014 critical"),
    (16,22,"Fix: parameterized queries \u2014 never string concat"),
    (22,26,"The pipeline blocks the merge \u2014 the vuln never ships")]),
 V(BOOTCAMP_K["devsecops"], "devsecops-secret", "The Secret in the Repo",
   "scan every commit", "story", scene_dso_secret,
   "An AWS key committed at 2 AM: bots had it by 2:04, the bill was $4,000 by 2:11 \u2014 vaults, not variables; git history is forever.",
   [(4,10,"2 AM: an AWS key committed \u2014 pushed to public"),
    (10,16,"2:04: the bots have it \u00b7 2:11: the bill is $4,000"),
    (16,22,"Rotate the key \u2014 then purge the history, it never forgets"),
    (22,26,"Vaults, not variables \u2014 scan every commit")]),
 # --- iac-terraform-gitops
 V(BOOTCAMP_K["iac"], "iac-state-truth", "The State File Is the Truth",
   "click-ops is drift", "bbg", scene_iac_state,
   "Terraform's state file is the source of truth: someone launches a server by hand and 'terraform plan' tattles \u2014 click-ops is drift.",
   [(4,10,"Your code: three servers \u00b7 reality: three servers \u00b7 state: three"),
    (10,16,"Someone launches a fourth \u2014 by hand \u2014 DRIFT"),
    (16,22,"terraform plan exposes it \u2014 the state file tattles"),
    (22,26,"Click-ops is drift \u2014 the state file is the only truth")]),
 V(BOOTCAMP_K["iac"], "iac-apply", "Terraform Apply in 100 Seconds",
   "declare the end state", "fireship", scene_iac_apply,
   "Declare an EC2 in HCL, run plan to preview, apply to create \u2014 declare the end state and let Terraform compute the diff.",
   [(4,10,"The resource block: ami, instance type \u2014 declared"),
    (10,16,"terraform plan: preview \u2014 three to add"),
    (16,22,"terraform apply: yes \u2014 and the cloud obeys"),
    (22,26,"Declare the end state \u2014 Terraform computes the diff")]),
 V(BOOTCAMP_K["iac"], "iac-drift-sim", "Drift: The Config That Wandered",
   "the repo is the source of truth", "primer", scene_iac_drift,
   "A living drift simulation: services wander out of sync with git \u2014 ArgoCD syncs and the repo becomes truth again.",
   [(4,10,"Git says one thing \u2014 the cluster says another"),
    (10,16,"Watch the services drift out of sync, one by one"),
    (16,22,"ArgoCD sync: git becomes truth again"),
    (22,26,"GitOps: the repo is the source of truth \u2014 the agent enforces it")]),
 # --- k8s-cka-exceed
 V(BOOTCAMP_K["k8scka"], "k8scka-scheduler", "Where Does the Pod Land?",
   "the scheduler is an optimizer", "bbg", scene_cka_schedule,
   "The kube-scheduler in action: a pod requests 2 CPU, full nodes are filtered out, the least-loaded node wins \u2014 filter, then score.",
   [(4,10,"Three nodes \u00b7 one is full \u00b7 the pod needs 2 CPU"),
    (10,16,"Filter: the full node is out"),
    (16,22,"Score: the least-loaded node wins \u2014 scheduled"),
    (22,26,"Filter the infeasible, score the rest \u2014 the scheduler is an optimizer")]),
 V(BOOTCAMP_K["k8scka"], "k8scka-kubectl", "Kubectl in 100 Seconds",
   "get, describe, logs \u2014 the debugging trinity", "fireship", scene_cka_kubectl,
   "The kubectl debugging trinity: get what's running, describe why it's broken, read the logs' last words \u2014 cattle, not pets.",
   [(4,10,"get pods: what's running where"),
    (10,16,"describe: why is it CrashLooping?"),
    (16,22,"logs --previous: the container's last words"),
    (22,26,"Apply declares \u00b7 delete removes \u2014 cattle, not pets")]),
 V(BOOTCAMP_K["k8scka"], "k8scka-quorum", "How Many Replicas Survive?",
   "odd numbers win elections", "3b1b", scene_cka_replicas,
   "The math of quorum: a node dies \u2014 3 and 5 replicas hold their majority, 1 and 2 gamble. Odd numbers win elections.",
   [(4,10,"One, two, three, five replicas \u2014 all healthy"),
    (10,16,"One node dies \u2014 who still has quorum?"),
    (16,22,"Three and five: majority held \u00b7 one and two: lost"),
    (22,26,"Odd numbers win elections \u2014 size for the failure, not the happy path")]),
 # --- kubernetes-sre
 V(BOOTCAMP_K["k8ssre"], "k8ssre-error-budget", "Spend the Error Budget",
   "reliability is a currency", "bbg", scene_sre_budget,
   "The error budget as currency: 99.9% allows 43 minutes of downtime a month \u2014 at 92% consumed, features freeze and reliability work ships.",
   [(4,10,"SLO 99.9% \u2014 the budget: 43 minutes a month"),
    (10,16,"Watch it burn: deploys, incidents, the meter climbs"),
    (16,22,"At 92%: feature freeze \u2014 reliability work only"),
    (22,26,"Spend the budget deliberately \u2014 reliability is a currency")]),
 V(BOOTCAMP_K["k8ssre"], "k8ssre-chaos", "Break It on Purpose",
   "chaos is a vaccine", "primer", scene_sre_chaos,
   "A chaos experiment: kill a whole zone at noon on purpose \u2014 traffic reroutes, latency ticks up 40ms, zero errors. Hypothesis confirmed.",
   [(4,10,"The experiment: kill zone-b at noon \u2014 on purpose"),
    (10,16,"Zone-b dies \u00b7 the other zones absorb the traffic"),
    (16,22,"p99 up 40ms \u00b7 errors: zero \u2014 hypothesis confirmed"),
    (22,26,"Chaos is a vaccine \u2014 small controlled doses build immunity")]),
 V(BOOTCAMP_K["k8ssre"], "k8ssre-3am-page", "The 3 AM Page",
   "blame the system, never the human", "story", scene_sre_page,
   "3 AM: the pager screams, error rate 40% \u2014 mitigate first, roll back the deploy, then the blameless postmortem at 3:41.",
   [(4,10,"3 AM \u2014 the pager screams \u00b7 error rate 40%, climbing"),
    (10,16,"Mitigate first: roll back, stop the bleed"),
    (16,22,"3:41 AM: green again \u00b7 now the blameless postmortem"),
    (22,26,"Blame the system, never the human \u2014 the page is a gift")]),
]

# ============================================================ render loop (mirrors gen_bootcamp_b2)
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
