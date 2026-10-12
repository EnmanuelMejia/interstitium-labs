#!/usr/bin/env python3
"""Batch 1 video generator: IL-01..IL-07, 21 videos x 30s, 1280x720 @ 24fps.
Styles: story / 3b1b / fireship / bbg / primer. Silent MP4s with burned-in
captions + "Preview -- narration coming" tag. Writes .vtt + .narration.md alongside.
"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR = 1280, 720, 24, 30
NFR = FPS * DUR
OUT = "/home/hatch/workspace/apex-audit/docs/assets/videos"

F_SANS  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_BOLD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F_MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIFB= "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

_fonts = {}
def font(path, size):
    k = (path, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(path, size)
    return _fonts[k]

def lerp(a, b, t): return a + (b - a) * t
def clamp(t, a=0.0, b=1.0): return max(a, min(b, t))
def ease(t):
    t = clamp(t); return t * t * (3 - 2 * t)

def wrap_text(text, fnt, maxw, dr):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def txt(dr, xy, s, fnt, fill, anchor="mm", stroke=0, sfill=(0,0,0)):
    dr.text(xy, s, font=fnt, fill=fill, anchor=anchor,
            stroke_width=stroke, stroke_fill=sfill)

# ---------------------------------------------------------------- palettes
STYLE_BG = {
    "story":    (10, 9, 8),
    "3b1b":     (10, 15, 46),
    "fireship": (5, 7, 15),
    "bbg":      (11, 16, 48),
    "primer":   (7, 18, 38),
}
TEAL=(0,220,200); YELLOW=(255,200,60); CYAN=(0,229,255); MAGENTA=(255,45,149)
ORANGE=(255,140,0); BLUE=(59,130,246); GREEN=(34,197,94); RED=(239,68,68)
GOLD=(212,175,55); CREAM=(240,230,210); WHITE=(255,255,255); DIM=(150,160,190)

def dot_grid(dr, step=64, color=(30,40,80)):
    for x in range(0, W+1, step):
        for y in range(0, H+1, step):
            dr.ellipse([x-1.5, y-1.5, x+1.5, y+1.5], fill=color)

def glow_box(dr, box, color, rad=18, layers=3):
    for i in range(layers, 0, -1):
        dim = tuple(max(0, int(v * (0.25 + 0.35 * (layers - i)))) for v in color)
        g = i * 8
        dr.rounded_rectangle([box[0]-g, box[1]-g, box[2]+g, box[3]+g],
                             radius=rad+g, outline=dim, width=5)
    dr.rounded_rectangle(box, radius=rad, outline=(255,255,255), width=2)

def panel(dr, box, title, accent, fsize=30):
    glow_box(dr, box, accent)
    dr.rectangle([box[0], box[1], box[2], box[1]+2], fill=(0,0,0))
    txt(dr, ((box[0]+box[2])//2, box[1]+34), title,
        font(F_BOLD, fsize), accent, anchor="mm")

def arrow(dr, x0, y0, x1, y1, color, w=6):
    dr.line([x0, y0, x1, y1], fill=color, width=w)
    ang = math.atan2(y1-y0, x1-x0); L = 18
    for d in (2.6, -2.6):
        dr.line([x1, y1, x1 - L*math.cos(ang+d), y1 - L*math.sin(ang+d)],
                fill=color, width=w)

def caption_bar(dr, text, accent):
    bar_h = 66
    dr.rectangle([0, H-bar_h, W, H], fill=(4, 7, 16))
    dr.line([0, H-bar_h, W, H-bar_h], fill=accent, width=3)
    f = font(F_SANS, 26)
    lines = wrap_text(text, f, W-140, dr)
    y = H-bar_h+8
    for ln in lines[:2]:
        txt(dr, (W//2, y+12), ln, f, WHITE, anchor="mm")
        y += 26

def preview_tag(dr):
    s = "PREVIEW \u2014 narration coming"
    f = font(F_BOLD, 18)
    tw = dr.textlength(s, font=f)
    x0, y0 = W-tw-46, 18
    dr.rounded_rectangle([x0, y0, x0+tw+32, y0+36], radius=10, fill=(60,42,8))
    dr.rounded_rectangle([x0, y0, x0+tw+32, y0+36], radius=10,
                         outline=(255,200,60), width=2)
    txt(dr, (x0+16, y0+18), s, f, (255,210,90), anchor="lm")

def title_card(dr, style, kicker, title, sub, t):
    k = ease(t / 1.0)
    bg = STYLE_BG[style]
    dr.rectangle([0, 0, W, H], fill=bg)
    if style in ("3b1b", "bbg"): dot_grid(dr)
    if style == "story":
        # candle-glow radial warmth
        for r in range(300, 0, -20):
            c = int(lerp(8, 46, r/300))
            dr.ellipse([W//2-r, H//2-r-40, W//2+r, H//2+r-40],
                       outline=(c+14, c+6, c-2), width=3)
    cx = W//2
    kf = font(F_BOLD if style!="story" else F_SERIFB, 30)
    kc = {"story":GOLD,"3b1b":TEAL,"fireship":MAGENTA,"bbg":CYAN,"primer":CYAN}[style]
    txt(dr, (cx, 218), kicker.upper(), kf, kc, anchor="mm")
    tf = font(F_BOLD if style!="story" else F_SERIFB, 78)
    tc = CREAM if style=="story" else WHITE
    yoff = int(lerp(24, 0, k))
    for ln in wrap_text(title, tf, W-200, dr)[:2]:
        txt(dr, (cx, 330+yoff), ln, tf, tc, anchor="mm",
            stroke=2 if style!="story" else 0, sfill=(0,0,0))
        yoff += 92
    underline = {"story":GOLD,"3b1b":YELLOW,"fireship":CYAN,"bbg":BLUE,"primer":TEAL}[style]
    tw = dr.textlength(title, font=tf)
    dr.line([cx-min(tw,900)//2, 400, cx+min(tw,900)//2, 400], fill=underline, width=5)
    sf = font(F_SANS if style!="story" else F_SERIF, 30)
    for ln in wrap_text(sub, sf, W-260, dr)[:2]:
        txt(dr, (cx, 452), ln, sf, DIM if style!="story" else (200,185,160), anchor="mm")

def end_card(dr, style, title, kicker, t):
    k = ease(t / 1.0)
    dr.rectangle([0, 0, W, H], fill=STYLE_BG[style])
    if style in ("3b1b", "bbg"): dot_grid(dr)
    cx = W//2
    kf = font(F_BOLD, 26)
    kc = {"story":GOLD,"3b1b":TEAL,"fireship":MAGENTA,"bbg":CYAN,"primer":CYAN}[style]
    txt(dr, (cx, 210), "INTERSTITIUM LABS", kf, kc, anchor="mm")
    txt(dr, (cx, 330), "Preview \u2014 narration coming",
        font(F_BOLD, 52), WHITE, anchor="mm")
    txt(dr, (cx, 410), "Narration script staged \u00b7 voiceover pending TTS restore",
        font(F_SANS, 26), DIM, anchor="mm")
    tf = font(F_BOLD, 30)
    for ln in wrap_text(title, tf, W-260, dr)[:1]:
        txt(dr, (cx, 500), ln, tf, kc, anchor="mm")
    txt(dr, (cx, 560), kicker, font(F_SANS, 24), DIM, anchor="mm")

# ---------------------------------------------------------------- writers
def write_vtt(path, cues):
    def ts(s):
        h = int(s//3600); m = int((s%3600)//60); sec = s%60
        return "%02d:%02d:%06.3f" % (h, m, sec)
    with open(path, "w") as f:
        f.write("WEBVTT\n\n")
        for a, b, text in cues:
            f.write("%s --> %s\n%s\n\n" % (ts(a), ts(b), text))

def write_narration(path, title, kicker, fname, cues, blurb):
    with open(path, "w") as f:
        f.write("# %s \u2014 Narration Script\n\n" % title)
        f.write("**Course:** %s  \n" % kicker)
        f.write("**Video:** `%s` (silent preview, 30s, 1280x720)  \n" % fname)
        f.write("**Status:** Preview \u2014 narration coming. Voiceover pending TTS service restore (auth token rejected 2026-10-08). Audio will be generated and burned in when TTS is restored.\n\n")
        f.write("## Concept\n\n%s\n\n" % blurb)
        f.write("## Voiceover cues\n\n")
        for a, b, text in cues:
            f.write("- `[%s\u2013%s]` %s\n" % ("%d:%02d" % (a//60, a%60),
                                               "%d:%02d" % (b//60, b%60), text))
        f.write("\n## Full script\n\n")
        f.write("Welcome to Interstitium Labs. ")
        f.write(" ".join(text for _, _, text in cues))
        f.write(" This is a captioned preview; full voiceover ships with the next render pass.\n")

def encode_video(path, frames_iter):
    cmd = ["ffmpeg", "-y", "-v", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
           "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
           "-t", str(DUR),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23",
           "-preset", "veryfast", "-c:a", "aac", "-b:a", "96k",
           "-shortest", "-movflags", "+faststart", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for img in frames_iter:
        p.stdin.write(img.tobytes())
    p.stdin.close(); p.wait()
    if p.returncode != 0:
        raise RuntimeError("ffmpeg failed for " + path)

SMOKE = os.environ.get("SMOKE") == "1"

# ============================================================ STORY (IL-01)
import random

def scene_emerald(t, dr, img):
    # As above, so below: starfield above mirrors geometry below
    random.seed(7)
    stars = [(random.random()*W, random.random()*300, random.random()*2+0.5)
             for _ in range(160)]
    dr.rectangle([0, 0, W, H], fill=(10, 9, 8))
    # warm glow center
    for r in range(340, 0, -25):
        c = int(lerp(6, 40, r/340))
        dr.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], outline=(c+12, c+4, c-2), width=2)
    # stars rotate slowly (above)
    cx, cy = W//2, 170
    for sx, sy, sz in stars:
        ang = t*0.05 + (sx/W)*6.28
        rr = 90 + (sy/300)*130
        x = cx + math.cos(ang)*rr; y = cy + math.sin(ang)*rr*0.45
        tw = 0.5 + 0.5*math.sin(t*3 + sx)
        dr.ellipse([x-sz, y-sz, x+sz, y+sz], fill=(int(220*tw)+30, int(200*tw)+30, int(150*tw)+40))
    txt(dr, (W//2, 60), "A S   A B O V E", font(F_SERIF, 34), GOLD, anchor="mm")
    # divider
    dr.line([60, 360, W-60, 360], fill=GOLD, width=3)
    txt(dr, (W//2, 660), "S O   B E L O W", font(F_SERIF, 34), GOLD, anchor="mm")
    # geometry below draws progressively
    k = clamp((t-4)/18)
    cx2, cy2 = W//2, 520
    for i, R in enumerate([50, 95, 140]):
        if k*3 > i:
            frac = clamp(k*3 - i)
            sweep = frac * 6.283
            for a_i in range(int(sweep*40)):
                a = a_i/40.0
                x = cx2 + math.cos(a)*R; y = cy2 + math.sin(a)*R
                dr.ellipse([x-2, y-2, x+2, y+2], fill=GOLD)
    # mirror beams connecting above/below
    for i in range(9):
        fx = 200 + i*110
        if random.random() < 0.0: continue
        pulse = 0.4 + 0.6*abs(math.sin(t*1.5 + i))
        col = (int(212*pulse), int(175*pulse), int(55*pulse))
        dr.line([fx, 300, fx, 420], fill=col, width=3)

def scene_enochian(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=(10, 9, 8))
    for r in range(340, 0, -25):
        c = int(lerp(6, 36, r/340))
        dr.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], outline=(c+10, c+4, c-3), width=2)
    # Great Table: 8x4 grid of Enochian-style glyphs (Latin capitals, conceptual)
    letters = "AOEIUYDLRXZCMBNPQSTVFGHWK"
    cols, rows = 8, 4
    gx0, gy0, cw, chh = 240, 130, 100, 95
    k = (t-4)
    for r in range(rows):
        for c in range(cols):
            i = r*cols + c
            x0, y0 = gx0 + c*cw, gy0 + r*chh
            born = 4 + i*0.55
            if t < born: 
                dr.rectangle([x0+6, y0+6, x0+cw-6, y0+chh-6], outline=(40,34,22), width=1)
                continue
            age = t - born
            flash = max(0, 1 - age*1.2)
            fill = (int(lerp(30,120,flash)), int(lerp(24,95,flash)), int(lerp(14,40,flash)))
            dr.rectangle([x0+6, y0+6, x0+cw-6, y0+chh-6], fill=fill, outline=GOLD, width=2)
            txt(dr, (x0+cw//2, y0+chh//2), letters[i % len(letters)],
                font(F_SERIFB, 44), CREAM, anchor="mm")
            # angelic row highlight sweeping
            if 16 < t < 22 and r == int((t-16)/1.5) % rows:
                dr.rectangle([x0+6, y0+6, x0+cw-6, y0+chh-6], outline=YELLOW, width=4)
    txt(dr, (W//2, 560), "THE GREAT TABLE \u00b7 12 \u00d7 13 SQUARES",
        font(F_SERIF, 28), (200,185,160), anchor="mm")

def scene_ccru(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=(10, 9, 8))
    for r in range(340, 0, -25):
        c = int(lerp(6, 34, r/340))
        dr.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], outline=(c+12, c+5, c-2), width=2)
    nodes = [("FICTION", W//2, 130, (255,120,120)),
             ("MACHINE", 320, 520, (150,200,255)),
             ("REALITY", 960, 520, (150,255,180))]
    for name, x, y, col in nodes:
        glow_box(dr, [x-130, y-55, x+130, y+55], col, rad=24)
        dr.rectangle([x-130, y-55, x+130, y+55], fill=(16,14,12))
        txt(dr, (x, y), name, font(F_SERIFB, 40), col, anchor="mm")
    # cyclic arrows with flowing particles
    pairs = [(0,1),(1,2),(2,0)]
    for pi, (a,b) in enumerate(pairs):
        x0,y0 = nodes[a][1], nodes[a][2]; x1,y1 = nodes[b][1], nodes[b][2]
        dx, dy = x1-x0, y1-y0; L = math.hypot(dx,dy)
        ux, uy = -dy/L, dx/L
        sx, sy = x0+dx*0.18+ux*40, y0+dy*0.18+uy*40
        ex, ey = x0+dx*0.82+ux*40, y0+dy*0.82+uy*40
        dr.line([sx, sy, ex, ey], fill=(90,80,60), width=5)
        for p in range(6):
            f = ((t*0.5 + p/6.0 + pi*0.33) % 1.0)
            px, py = lerp(sx, ex, f), lerp(sy, ey, f)
            pulse = int(150 + 105*math.sin(t*6+p))
            dr.ellipse([px-5, py-5, px+5, py+5], fill=(pulse, pulse-40, 60))
        arrow(dr, ex-ux*30, ey-uy*30, ex, ey, (160,140,100), 5)
    txt(dr, (W//2, 350), "hyperstition: fiction that bootstraps itself real",
        font(F_SERIF, 28), (200,185,160), anchor="mm")

# ============================================================ 3B1B (IL-02, IL-07)
def scene_bayes(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    # area model: hypothesis bar updates with evidence
    # Phase layout: left = prior/posterior bars, right = formula
    txt(dr, (300, 90), "PRIOR", font(F_BOLD, 30), TEAL, anchor="mm")
    txt(dr, (640, 90), "EVIDENCE", font(F_BOLD, 30), YELLOW, anchor="mm")
    txt(dr, (980, 90), "POSTERIOR", font(F_BOLD, 30), MAGENTA, anchor="mm")
    # prior bar 30%
    ph = 380
    dr.rectangle([220, 480-ph, 380, 480], fill=(0,90,80))
    dr.rectangle([220, 480-ph, 380, 480], outline=TEAL, width=3)
    txt(dr, (300, 520), "P(H) = 0.30", font(F_BOLD, 28), TEAL, anchor="mm")
    # evidence: likelihood ratio animates
    k = clamp((t-10)/8)
    eh = int(lerp(60, 300, ease(k)))
    dr.rectangle([560, 480-eh, 720, 480], fill=(120,90,10))
    dr.rectangle([560, 480-eh, 720, 480], outline=YELLOW, width=3)
    txt(dr, (640, 520), "likelihood \u00d74.0", font(F_BOLD, 28), YELLOW, anchor="mm")
    # posterior = prior*LR normalized: 0.3*4/(0.3*4+0.7*1)=1.2/1.9=0.63
    kh = int(lerp(60, int(380*0.63), ease(k)))
    dr.rectangle([900, 480-kh, 1060, 480], fill=(110,20,90))
    dr.rectangle([900, 480-kh, 1060, 480], outline=MAGENTA, width=3)
    txt(dr, (980, 520), "P(H|E) = 0.63", font(F_BOLD, 28), MAGENTA, anchor="mm")
    arrow(dr, 400, 340, 540, 340, DIM, 4)
    arrow(dr, 740, 340, 880, 340, DIM, 4)
    txt(dr, (640, 620),
        "P(H|E) = P(E|H)\u00b7P(H) / P(E)",
        font(F_BOLD, 40), WHITE, anchor="mm")

def scene_vectors(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    cx, cy, S = W//2, H//2+40, 46
    # morph parameter: matrix [[1,-1],[1,1]] scaled in over time
    k = ease(clamp((t-8)/12))
    # draw grid lines transforming: p' = (x + k*(-y)*0.8, y + k*(x)*0.8)... use M=[[1-k*0.5, -k],[k, 1-k*0.5]]
    def M(x, y):
        return (cx + (x*(1-0.4*k) - y*k)*S, cy - (y*(1-0.4*k) + x*k)*S)
    for gx in range(-8, 9):
        pts0 = [M(gx, gy) for gy in range(-6, 7)]
        dr.line(pts0, fill=(40,70,120), width=2)
    for gy in range(-6, 7):
        pts0 = [M(gx, gy) for gx in range(-8, 9)]
        dr.line(pts0, fill=(40,70,120), width=2)
    # basis vectors
    ix, iy = M(1, 0); jx, jy = M(0, 1)
    arrow(dr, cx, cy, ix, iy, YELLOW, 7); txt(dr, (ix+24, iy), "i\u0302", font(F_BOLD, 34), YELLOW, anchor="mm")
    arrow(dr, cx, cy, jx, jy, TEAL, 7);  txt(dr, (jx, jy-28), "j\u0302", font(F_BOLD, 34), TEAL, anchor="mm")
    # a vector v=(2,1) following
    vx, vy = M(2, 1)
    arrow(dr, cx, cy, vx, vy, MAGENTA, 7); txt(dr, (vx+24, vy-10), "v", font(F_BOLD, 34), MAGENTA, anchor="mm")
    txt(dr, (W//2, 90), "A matrix moves the basis \u2014 everything follows",
        font(F_BOLD, 36), WHITE, anchor="mm")
    txt(dr, (W//2, 640), "M = [ 1  \u22121 ]   morph: %.0f%%" % (k*100),
        font(F_MONO, 28), DIM, anchor="mm")
    txt(dr, (W//2, 680), "    [ 1   1 ]", font(F_MONO, 28), DIM, anchor="mm")

_galton_traj = None
def galton_init():
    global _galton_traj
    if _galton_traj is not None: return
    rng = random.Random(42)
    trajs = []
    ROWS, TOP, GAP = 11, 150, 40
    for i in range(170):
        f0 = int(4*FPS + i*2.6)
        x = W//2 - 260; y = TOP
        pts = []
        for r in range(ROWS):
            y = TOP + r*GAP
            x += rng.choice((-1, 1)) * 26
            pts.append((f0 + r*5, x, y))
        # fall into bins
        bin_i = int(clamp((x - (W//2-260) + 11*26) / 52, 0, 10))
        bx = (W//2-260) - 11*13 + bin_i*52 + 26
        for f in range(6):
            pts.append((f0 + ROWS*5 + f*3, x + (bx-x)*f/6, TOP + ROWS*GAP + f*14))
        trajs.append((f0, pts, bin_i))
    _galton_traj = trajs

def scene_galton(t, dr, img):
    galton_init()
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    # petri rim
    dr.ellipse([W//2-560-270, 60, W//2-560+270+560, 700], outline=CYAN, width=6)
    ROWS, TOP, GAP = 11, 150, 40
    # pegs
    for r in range(ROWS):
        y = TOP + r*GAP
        for c in range(r+1):
            x = (W//2-260) - r*13 + c*26
            dr.ellipse([x-4, y-4, x+4, y+4], fill=(120,180,220))
    fr = int(t*FPS)
    bins = [0]*11
    for f0, pts, bi in _galton_traj:
        if fr < f0: continue
        # find position
        pos = None
        for j in range(len(pts)-1):
            if pts[j][0] <= fr <= pts[j+1][0]:
                f1,x1,y1 = pts[j]; f2,x2,y2 = pts[j+1]
                u = (fr-f1)/max(1,f2-f1)
                pos = (lerp(x1,x2,u), lerp(y1,y2,u)); break
        if pos is None:
            if fr > pts[-1][0]:
                bins[bi] += 1
                continue
            pos = (pts[0][1], pts[0][2])
        dr.ellipse([pos[0]-7, pos[1]-7, pos[0]+7, pos[1]+7],
                   fill=(255,150,60), outline=(255,220,150), width=2)
    # histogram bins
    base_y = 640
    for i, n in enumerate(bins):
        bh = n*9
        x = (W//2-260) - 11*13 + i*52
        if bh > 0:
            dr.rectangle([x, base_y-bh, x+46, base_y], fill=(0,140,150))
            dr.rectangle([x, base_y-bh, x+46, base_y], outline=TEAL, width=2)
    dr.line([W//2-560, base_y, W//2+0, base_y], fill=CYAN, width=4)
    txt(dr, (W//2-260, 60), "balls dropped: %d" % sum(1 for f0,_,_ in _galton_traj if fr>=f0),
        font(F_BOLD, 30), WHITE, anchor="mm")

# ============================================================ FIRESHIP (IL-03)
def code_panel(dr, x0, y0, x1, y1, title, lines, hi_line=-1, t=0):
    glow_box(dr, [x0, y0, x1, y1], (120,80,255), rad=14)
    dr.rectangle([x0, y0, x1, y1], fill=(10,10,22))
    # title bar
    dr.rectangle([x0, y0, x1, y0+52], fill=(18,18,36))
    txt(dr, (x0+24, y0+26), title, font(F_BOLD, 24), (255,120,120), anchor="lm")
    f = font(F_MONO, 22)
    y = y0 + 92
    for i, (code, col) in enumerate(lines):
        if i == hi_line:
            dr.rectangle([x0+8, y-20, x1-8, y+14], fill=(40,30,70))
        txt(dr, (x0+64, y), code, f, col, anchor="lm")
        txt(dr, (x0+30, y), str(i+1), f, (90,90,120), anchor="lm")
        y += 34

def scene_recursion(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    lines = [("function fib(n) {", (200,200,255)),
             ("  if (n <= 1) return n;", (0,229,255)),
             ("  return fib(n-1) + fib(n-2);", (255,200,90)),
             ("}", (200,200,255)),
             ("fib(5);", (255,120,200))]
    code_panel(dr, 40, 120, 480, 620, "recursion.js", lines,
               hi_line=2 if 4 < t < 16 else (1 if t >= 16 else 0), t=t)
    panel(dr, [560, 120, 1240, 200], "CALL STACK", MAGENTA, 30)
    # stack frames
    calls = ["fib(5)", "fib(4)", "fib(3)", "fib(2)", "fib(1)"]
    vals  = ["5", "3", "2", "1", "1"]
    for i, c in enumerate(calls):
        born = 4 + i*2.2
        if t < born: continue
        age = t - born
        # unwinding: frames pop from top after t=16
        pop_at = 16 + (len(calls)-1-i)*1.4
        if t > pop_at:
            continue
        y = 240 + i*72
        slide = int(lerp(80, 0, ease(age*2)))
        glow = MAGENTA if t < 16 else GREEN
        glow_box(dr, [620+slide, y, 1180, y+58], glow, rad=12, layers=2)
        dr.rectangle([620+slide, y, 1180, y+58], fill=(14,14,30))
        txt(dr, (700+slide, y+29), c, font(F_MONOB, 30), WHITE, anchor="lm")
        if t > pop_at - 1.4 and t < pop_at + 3:
            txt(dr, (1100, y+29), "= " + vals[i], font(F_MONOB, 30), GREEN, anchor="lm")
    if t > 24:
        txt(dr, (900, 620), "fib(5) = 5", font(F_BOLD, 64), GREEN, anchor="mm")

def scene_pointers(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    lines = [("int x = 42;", (200,200,255)),
             ("int* p = &x;", (0,229,255)),
             ("int y = *p;", (255,200,90)),
             ("// y == 42", (110,110,140))]
    code_panel(dr, 40, 120, 480, 560, "pointers.cpp", lines,
               hi_line=min(2, int((t-4)/6)), t=t)
    # memory grid 4x4
    addrs = ["0x7FF0","0x7FF4","0x7FF8","0x7FFC"]
    cells = {"x": (2, 42, CYAN), "p": (3, "0x7FF8", MAGENTA)}
    for r in range(2):
        for c in range(4):
            x0, y0 = 580 + c*160, 220 + r*130
            hot = (r==0 and c==2 and t>6) or (r==0 and c==3 and t>10)
            glow_box(dr, [x0, y0, x0+130, y0+100], CYAN if hot else (60,60,100), rad=12, layers=2)
            dr.rectangle([x0, y0, x0+130, y0+100], fill=(12,12,26))
            name = { (0,2):"x", (0,3):"p" }.get((r,c), "")
            val = { (0,2):"42", (0,3):"0x7FF8" }.get((r,c), "...")
            txt(dr, (x0+65, y0+28), name or " ", font(F_BOLD, 26),
                CYAN if name=="x" else MAGENTA, anchor="mm")
            txt(dr, (x0+65, y0+64), val, font(F_MONOB, 24), WHITE, anchor="mm")
    for i, a in enumerate(addrs):
        txt(dr, (580+i*160+65, 200), a, font(F_MONO, 18), DIM, anchor="mm")
    # pointer arrow p -> x
    if t > 12:
        k = ease((t-12)/1.5)
        arrow(dr, lerp(580+3*160+65, 580+2*160+130, k), 270,
              580+2*160+130, 270, MAGENTA, 6)
        txt(dr, (905, 160), "p stores the ADDRESS of x", font(F_BOLD, 28), MAGENTA, anchor="mm")
    if t > 18:
        txt(dr, (905, 480), "*p dereferences \u2192 reads 42",
            font(F_BOLD, 30), GREEN, anchor="mm")
        glow_box(dr, [580+2*160, 220, 580+2*160+130, 320], GREEN, rad=12, layers=2)

def scene_bigo(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    ox, oy, ax, ay = 140, 600, 1140, 120
    dr.line([ox, oy, ax, oy], fill=DIM, width=3)
    dr.line([ox, oy, ox, ay], fill=DIM, width=3)
    txt(dr, (640, 650), "input size n", font(F_BOLD, 26), DIM, anchor="mm")
    txt(dr, (80, 360), "time", font(F_BOLD, 26), DIM, anchor="mm")
    k = ease(clamp((t-5)/14))
    def X(n): return ox + n/100*(ax-ox)
    def Yc(c): return oy - min(1, c)*(oy-ay)
    # O(1)
    dr.line([(X(0), Yc(0.05)), (X(100*k), Yc(0.05))], fill=CYAN, width=6)
    # O(n)
    pts = [(X(n), Yc(n/100*0.9)) for n in range(0, int(100*k)+1, 2)]
    if len(pts) > 1: dr.line(pts, fill=GREEN, width=6)
    # O(n^2)
    pts2 = [(X(n), Yc((n/100)**2)) for n in range(0, int(100*k)+1, 2)]
    if len(pts2) > 1: dr.line(pts2, fill=RED, width=6)
    # racing dots
    if k > 0.02:
        n = 100*k
        dr.ellipse([X(n)-10, Yc(0.05)-10, X(n)+10, Yc(0.05)+10], fill=CYAN)
        dr.ellipse([X(n)-10, Yc(n/100*0.9)-10, X(n)+10, Yc(n/100*0.9)+10], fill=GREEN)
        dr.ellipse([X(n)-10, Yc((n/100)**2)-10, X(n)+10, Yc((n/100)**2)+10], fill=RED)
    leg = [("O(1)", CYAN, 170), ("O(n)", GREEN, 250), ("O(n\u00b2)", RED, 330)]
    for name, col, y in leg:
        glow_box(dr, [950, y-34, 1210, y+34], col, rad=12, layers=2)
        dr.rectangle([950, y-34, 1210, y+34], fill=(12,12,26))
        txt(dr, (1080, y), name, font(F_BOLD, 32), col, anchor="mm")
    if t > 21:
        txt(dr, (640, 60), "at n=1M: 1 step vs 1M steps vs 1T steps",
            font(F_BOLD, 32), WHITE, anchor="mm")

# ============================================================ BBG (IL-04)
def bbg_title(dr, title, accent):
    txt(dr, (W//2, 66), title, font(F_BOLD, 56), WHITE, anchor="mm")
    tw = dr.textlength(title, font=font(F_BOLD, 56))
    dr.line([W//2-tw//2, 104, W//2+tw//2, 104], fill=accent, width=5)

def scene_scheduler(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Round-Robin Scheduling", BLUE)
    panel(dr, [60, 150, 380, 640], "READY QUEUE", BLUE, 28)
    panel(dr, [480, 300, 800, 560], "CPU", GREEN, 28)
    panel(dr, [900, 150, 1220, 640], "DONE", DIM, 28)
    procs = [("P1", BLUE), ("P2", ORANGE), ("P3", TEAL), ("P4", MAGENTA)]
    # quantum cycle: each proc runs 4s in order, cycling twice
    cyc = int((t-4)//4) % 4 if t > 4 else -1
    qpos = (t-4) % 4
    done = set()
    for rep in range(2):
        for i in range(4):
            idx = rep*4 + i
            if t-4 < idx*4 + 4: continue
            if rep == 1 and i <= cyc and t-4 >= 16 + i*4 + 4: done.add(i)
    for i, (name, col) in enumerate(procs):
        y = 230 + i*100
        if i in done:
            glow_box(dr, [930, y-8, 1190, y+62], GREEN, rad=12, layers=2)
            dr.rectangle([930, y-8, 1190, y+62], fill=(10,30,18))
            txt(dr, (1060, y+27), name + " \u2713", font(F_BOLD, 30), GREEN, anchor="mm")
            continue
        if i == cyc and t > 4:
            # on CPU
            k = qpos/4
            glow_box(dr, [520, 380, 760, 450], col, rad=12, layers=2)
            dr.rectangle([520, 380, 760, 450], fill=(12,16,34))
            txt(dr, (640, 415), name, font(F_BOLD, 34), col, anchor="mm")
            dr.rectangle([540, 470, 740, 492], fill=(30,30,60))
            dr.rectangle([540, 470, 540+200*k, 492], fill=col)
            txt(dr, (640, 520), "quantum %d%%" % int(k*100), font(F_BOLD, 22), WHITE, anchor="mm")
        else:
            glow_box(dr, [90, y-8, 350, y+62], col, rad=12, layers=2)
            dr.rectangle([90, y-8, 350, y+62], fill=(12,16,34))
            txt(dr, (220, y+27), name, font(F_BOLD, 30), col, anchor="mm")
    if cyc >= 0:
        arrow(dr, 400, 415, 470, 415, GREEN, 5)
        arrow(dr, 810, 415, 890, 415, DIM, 5)
    txt(dr, (W//2, 690), "quantum = 100ms \u00b7 preemptive \u00b7 fair",
        font(F_BOLD, 26), DIM, anchor="mm")

def scene_subnetting(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Subnetting 192.168.1.0/24", BLUE)
    txt(dr, (W//2, 150), "32 bits \u00b7 24 network + 8 host",
        font(F_BOLD, 30), WHITE, anchor="mm")
    # bit cells
    k = clamp((t-8)/6)
    for i in range(32):
        x = 96 + i*34
        if i < 24:
            col, fill = BLUE, (16,30,70)
        elif i < 26:
            col, fill = (YELLOW if k>0.5 else DIM), (50,42,10) if k>0.5 else (20,20,30)
        else:
            col, fill = TEAL, (10,44,42)
        dr.rectangle([x, 220, x+30, 264], fill=fill, outline=col, width=3)
    txt(dr, (96, 300), "network bits", font(F_BOLD, 24), BLUE, anchor="lm")
    txt(dr, (96+26*34, 300), "borrowed", font(F_BOLD, 24), YELLOW, anchor="lm")
    txt(dr, (96+28*34, 300), "host bits", font(F_BOLD, 24), TEAL, anchor="lm")
    # subnets appear
    if t > 14:
        subs = [("192.168.1.0/26", "hosts .1\u2013.62", BLUE),
                ("192.168.1.64/26", "hosts .65\u2013.126", ORANGE),
                ("192.168.1.128/26", "hosts .129\u2013.190", TEAL),
                ("192.168.1.192/26", "hosts .193\u2013.254", MAGENTA)]
        for i, (net, rng, col) in enumerate(subs):
            born = 14 + i*1.6
            if t < born: continue
            a = ease((t-born)/1.2)
            x = 96 + i*272
            y = int(lerp(80, 0, a))
            glow_box(dr, [x, 360+y, x+250, 520+y], col, rad=14)
            dr.rectangle([x, 360+y, x+250, 520+y], fill=(12,16,34))
            txt(dr, (x+125, 410+y), net, font(F_MONOB, 26), col, anchor="mm")
            txt(dr, (x+125, 460+y), rng, font(F_SANS, 24), DIM, anchor="mm")
        txt(dr, (W//2, 590), "2 borrowed bits \u2192 4 subnets \u00d7 62 usable hosts",
            font(F_BOLD, 32), WHITE, anchor="mm")

def scene_inode(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Inodes: How Linux Names Files", BLUE)
    panel(dr, [80, 220, 400, 560], "DIRECTORY", BLUE, 28)
    panel(dr, [480, 220, 800, 560], "INODE 1048576", ORANGE, 28)
    panel(dr, [880, 220, 1200, 560], "DATA BLOCKS", TEAL, 28)
    txt(dr, (240, 320), "report.pdf", font(F_MONOB, 32), WHITE, anchor="mm")
    txt(dr, (240, 380), "\u2192 inode 1048576", font(F_SANS, 26), DIM, anchor="mm")
    if t > 8:
        fields = ["owner: uid 1000", "size: 24812 B", "mode: -rw-r--r--",
                  "mtime: 2026-10-08", "blocks: 12, 47, 203"]
        for i, fl in enumerate(fields):
            if t < 8 + i*1.4: continue
            txt(dr, (640, 320+i*44), fl, font(F_MONO, 24), (255,210,140), anchor="mm")
    # packet traveling along arrows
    if t > 10:
        cyc = (t-10) % 8
        if cyc < 4:
            px = lerp(400, 480, cyc/4); py = 390
        else:
            px = lerp(800, 880, (cyc-4)/4); py = 390
        dr.ellipse([px-12, py-12, px+12, py+12], fill=YELLOW)
    arrow(dr, 400, 390, 470, 390, DIM, 5)
    arrow(dr, 800, 390, 870, 390, DIM, 5)
    if t > 20:
        for i in range(3):
            glow_box(dr, [930, 300+i*80, 1150, 356+i*80], TEAL, rad=10, layers=2)
            dr.rectangle([930, 300+i*80, 1150, 356+i*80], fill=(10,40,38))
            txt(dr, (1040, 328+i*80), "block %d" % (12 if i==0 else (47 if i==1 else 203)),
                font(F_MONO, 22), WHITE, anchor="mm")
    txt(dr, (W//2, 640), "names \u2192 inodes \u2192 blocks",
        font(F_BOLD, 32), WHITE, anchor="mm")

# ============================================================ BBG (IL-05)
def scene_k8s(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Kubernetes Architecture", BLUE)
    panel(dr, [340, 130, 940, 300], "CONTROL PLANE", BLUE, 28)
    comps = [("API server", 430), ("scheduler", 640), ("etcd", 840)]
    for name, x in comps:
        glow_box(dr, [x-90, 200, x+90, 250], BLUE, rad=10, layers=2)
        dr.rectangle([x-90, 200, x+90, 250], fill=(12,16,34))
        txt(dr, (x, 225), name, font(F_BOLD, 22), WHITE, anchor="mm")
    for nx, label in [(240, "NODE 1"), (1040, "NODE 2")]:
        panel(dr, [nx-190, 380, nx+190, 660], label, ORANGE, 28)
        txt(dr, (nx, 470), "kubelet", font(F_SANS, 24), DIM, anchor="mm")
    # pods placed over time; rolling update swaps colors
    pods_n1 = [BLUE, BLUE, GREEN if t > 18 else BLUE]
    pods_n2 = [BLUE, GREEN if t > 22 else BLUE]
    for i, col in enumerate(pods_n1):
        born = 8 + i*1.8
        if t < born: continue
        glow_box(dr, [90+i*105, 520, 180+i*105, 600], col, rad=12, layers=2)
        dr.rectangle([90+i*105, 520, 180+i*105, 600], fill=(12,16,34))
        txt(dr, (135+i*105, 560), "pod", font(F_BOLD, 22), WHITE, anchor="mm")
    for i, col in enumerate(pods_n2):
        born = 12 + i*1.8
        if t < born: continue
        glow_box(dr, [900+i*105, 520, 990+i*105, 600], col, rad=12, layers=2)
        dr.rectangle([900+i*105, 520, 990+i*105, 600], fill=(12,16,34))
        txt(dr, (945+i*105, 560), "pod", font(F_BOLD, 22), WHITE, anchor="mm")
    arrow(dr, 640, 300, 240, 380, DIM, 4)
    arrow(dr, 640, 300, 1040, 380, DIM, 4)
    if t > 18:
        txt(dr, (W//2, 690), "rolling update: v2 pods replace v1, zero downtime",
            font(F_BOLD, 26), GREEN, anchor="mm")

def scene_cicd(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "CI/CD Pipeline", BLUE)
    stages = [("COMMIT", BLUE), ("BUILD", CYAN), ("TEST", YELLOW),
              ("SCAN", ORANGE), ("DEPLOY", GREEN)]
    n = len(stages)
    bw = 190; gap = 26; total = n*bw + (n-1)*gap
    x0 = (W-total)//2
    # traveling packet
    pk = clamp((t-4)/18)
    for i, (name, col) in enumerate(stages):
        x = x0 + i*(bw+gap)
        done = pk*n > i+0.5
        active = (pk*n > i) and not done
        glow_box(dr, [x, 300, x+bw, 460], col if (done or active) else (60,60,90), rad=14)
        dr.rectangle([x, 300, x+bw, 460], fill=(12,16,34))
        txt(dr, (x+bw//2, 360), name, font(F_BOLD, 28), col if (done or active) else DIM, anchor="mm")
        if done:
            txt(dr, (x+bw//2, 420), "\u2713", font(F_BOLD, 40), GREEN, anchor="mm")
        elif active:
            txt(dr, (x+bw//2, 420), "\u25b6", font(F_BOLD, 34), col, anchor="mm")
        if i < n-1:
            arrow(dr, x+bw+4, 380, x+bw+gap-4, 380, DIM, 5)
    if pk > 0.01 and pk < 0.99:
        px = x0 + pk*total
        dr.ellipse([px-14, 240-14, px+14, 240+14], fill=WHITE)
        dr.ellipse([px-8, 240-8, px+8, 240+8], fill=CYAN)
    if t > 23:
        glow_box(dr, [x0, 520, x0+total, 620], GREEN, rad=14)
        dr.rectangle([x0, 520, x0+total, 620], fill=(10,30,18))
        txt(dr, (W//2, 570), "PRODUCTION \u00b7 v2.14.0 live", font(F_BOLD, 34), GREEN, anchor="mm")

def scene_terraform(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "Terraform: Infrastructure as Code", BLUE)
    panel(dr, [60, 140, 420, 640], "main.tf", (150,110,255), 26)
    cfg = ['resource "aws_instance" "web" {',
           '  ami           = "ami-0c55b159"',
           '  instance_type = "t3.medium"',
           '  count         = 3',
           '}']
    f = font(F_MONO, 21)
    for i, ln in enumerate(cfg):
        if t < 4 + i*0.9: continue
        txt(dr, (90, 240+i*44), ln, f, (210,190,255), anchor="lm")
    if t > 10:
        panel(dr, [480, 140, 800, 420], "terraform plan", YELLOW, 26)
        plan = ["+ aws_instance.web[0]", "+ aws_instance.web[1]", "+ aws_instance.web[2]",
                "Plan: 3 to add, 0 to change"]
        for i, ln in enumerate(plan):
            if t < 10 + i*1.2: continue
            txt(dr, (510, 250+i*40), ln, font(F_MONO, 22), GREEN if ln.startswith("+") else WHITE, anchor="lm")
    if t > 16:
        panel(dr, [860, 140, 1220, 640], "AWS", ORANGE, 26)
        for i in range(3):
            born = 16 + i*1.4
            if t < born: continue
            a = ease((t-born)/1.0)
            y = int(lerp(60, 0, a))
            glow_box(dr, [900, 230+i*120+y, 1180, 320+i*120+y], ORANGE, rad=12, layers=2)
            dr.rectangle([900, 230+i*120+y, 1180, 320+i*120+y], fill=(12,16,34))
            txt(dr, (1040, 275+i*120+y), "ec2 web-%d" % i, font(F_BOLD, 26), WHITE, anchor="mm")
        if t > 22:
            txt(dr, (640, 560), "terraform.tfstate \u2190 reality recorded",
                font(F_BOLD, 28), YELLOW, anchor="mm")

# ============================================================ BBG (IL-06)
def scene_pki(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "The PKI Trust Chain", BLUE)
    chain = [("ROOT CA", "self-signed", BLUE, 240),
             ("INTERMEDIATE CA", "signed by root", ORANGE, 640),
             ("LEAF CERT", "interstitiumlabs.dev", GREEN, 1040)]
    for name, sub, col, x in chain:
        glow_box(dr, [x-160, 260, x+160, 520], col, rad=16)
        dr.rectangle([x-160, 260, x+160, 520], fill=(12,16,34))
        txt(dr, (x, 330), name, font(F_BOLD, 30), col, anchor="mm")
        txt(dr, (x, 380), sub, font(F_SANS, 22), DIM, anchor="mm")
        txt(dr, (x, 450), "\U0001F512", font(F_SANS, 64), col, anchor="mm")
    for i in range(2):
        born = 8 + i*3
        if t < born: continue
        a = ease((t-born)/1.5)
        x0 = chain[i][3]+160; x1 = chain[i+1][3]-160
        mx = lerp(x0, x1, a)
        arrow(dr, x0, 390, x1, 390, DIM, 5)
        txt(dr, ((x0+x1)//2, 340), "signs", font(F_BOLD, 24), YELLOW, anchor="mm")
        dr.ellipse([mx-10, 390-10, mx+10, 390+10], fill=YELLOW)
    if t > 16:
        txt(dr, (W//2, 600), "browser verifies: leaf \u2192 intermediate \u2192 trusted root \u2713",
            font(F_BOLD, 32), GREEN, anchor="mm")

def scene_siem(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "SIEM Detection Pipeline", BLUE)
    panel(dr, [60, 140, 400, 640], "EVENT STREAM", DIM, 26)
    import random as _r
    _r.seed(11)
    logs = ["auth failed: admin", "dns query ok", "port scan :445",
            "login ok: user412", "auth failed: admin", "http 200 /api",
            "auth failed: admin", "smb share enum", "auth failed: admin"]
    f = font(F_MONO, 20)
    off = (t*40) % 60
    for i, ln in enumerate(logs):
        y = 230 + i*44 - off
        if y < 200 or y > 600: continue
        hot = "failed" in ln or "scan" in ln
        txt(dr, (90, y), ln, f, RED if hot else (140,150,180), anchor="lm")
    panel(dr, [470, 140, 810, 640], "SIEM", CYAN, 26)
    txt(dr, (640, 260), "normalize", font(F_BOLD, 26), WHITE, anchor="mm")
    txt(dr, (640, 330), "correlate", font(F_BOLD, 26), WHITE, anchor="mm")
    txt(dr, (640, 400), "enrich", font(F_BOLD, 26), WHITE, anchor="mm")
    arrow(dr, 400, 390, 460, 390, DIM, 5)
    if t > 14:
        flash = 0.5 + 0.5*math.sin(t*6)
        col = (int(lerp(120,255,flash)), 40, 40)
        glow_box(dr, [880, 240, 1220, 440], col, rad=16)
        dr.rectangle([880, 240, 1220, 440], fill=(30,10,10))
        txt(dr, (1050, 300), "\u26a0 ALERT", font(F_BOLD, 36), (255,120,120), anchor="mm")
        txt(dr, (1050, 360), "brute force:\n5 fails / 60s", font(F_SANS, 26), WHITE, anchor="mm")
        arrow(dr, 810, 390, 870, 390, RED, 5)
    if t > 20:
        txt(dr, (1050, 540), "SOC analyst\nnotified \u2713", font(F_BOLD, 28), GREEN, anchor="mm")

def scene_killchain(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["bbg"]); dot_grid(dr)
    bbg_title(dr, "The Cyber Kill Chain", RED)
    stages = ["RECON", "WEAPONIZE", "DELIVER", "EXPLOIT", "INSTALL", "C2", "ACT"]
    n = len(stages); bw = 140; gap = 20
    total = n*bw + (n-1)*gap; x0 = (W-total)//2; y = 330
    for i, name in enumerate(stages):
        born = 5 + i*2.4
        lit = t >= born
        col = RED if lit else (70,70,100)
        if lit:
            glow_box(dr, [x0+i*(bw+gap), y, x0+i*(bw+gap)+bw, y+120], RED, rad=10, layers=2)
        else:
            dr.rounded_rectangle([x0+i*(bw+gap), y, x0+i*(bw+gap)+bw, y+120], radius=10, outline=col, width=3)
        dr.rectangle([x0+i*(bw+gap), y, x0+i*(bw+gap)+bw, y+120], fill=(12,16,34) if not lit else (34,12,12))
        txt(dr, (x0+i*(bw+gap)+bw//2, y+60), name, font(F_BOLD, 22), WHITE if lit else DIM, anchor="mm")
        if i < n-1:
            arrow(dr, x0+i*(bw+gap)+bw+2, y+60, x0+(i+1)*(bw+gap)-2, y+60, DIM, 4)
    if t > 22:
        txt(dr, (W//2, 560), "defenders win by breaking ANY single link",
            font(F_BOLD, 32), GREEN, anchor="mm")
        txt(dr, (W//2, 610), "earlier = cheaper", font(F_BOLD, 28), DIM, anchor="mm")

# ============================================================ 3B1B (IL-07)
def scene_sql_joins(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    cx, cy, R = W//2, 360, 220
    lx, rx = cx-170, cx+170
    # phase: 4-10 intro, 10-15 inner, 15-20 left, 20-26 full
    mode = 0
    if 10 <= t < 15: mode = 1
    elif 15 <= t < 20: mode = 2
    elif t >= 20: mode = 3
    # circles
    for (x, col, fill_on) in [(lx, TEAL, mode in (2,3)), (rx, YELLOW, mode==3)]:
        dr.ellipse([x-R, cy-R, x+R, cy+R], outline=col, width=6)
    if mode == 1:
        # intersection highlight: lens approximation
        dr.ellipse([cx-95, cy-160, cx+95, cy+160], fill=(90,120,60))
        dr.ellipse([lx-R, cy-R, lx+R, cy+R], outline=TEAL, width=6)
        dr.ellipse([rx-R, cy-R, rx+R, cy+R], outline=YELLOW, width=6)
    elif mode == 2:
        dr.ellipse([lx-R, cy-R, lx+R, cy+R], fill=(0,90,80))
        dr.ellipse([rx-R, cy-R, rx+R, cy+R], outline=YELLOW, width=6)
        dr.ellipse([lx-R, cy-R, lx+R, cy+R], outline=TEAL, width=6)
    elif mode == 3:
        dr.ellipse([lx-R, cy-R, lx+R, cy+R], fill=(0,90,80))
        dr.ellipse([rx-R, cy-R, rx+R, cy+R], fill=(120,90,10))
        dr.ellipse([cx-95, cy-160, cx+95, cy+160], fill=(150,130,40))
    txt(dr, (lx, cy), "customers", font(F_BOLD, 30), WHITE, anchor="mm")
    txt(dr, (rx, cy), "orders", font(F_BOLD, 30), WHITE, anchor="mm")
    names = ["", "INNER JOIN", "LEFT JOIN", "FULL JOIN"]
    descs = ["two tables, one shared key: customer_id",
             "only rows with a match on both sides",
             "every customer \u2014 plus their orders, if any",
             "everything: matched and unmatched, both sides"]
    txt(dr, (W//2, 120), names[mode] if mode else "SQL JOINS",
        font(F_BOLD, 52), WHITE, anchor="mm")
    txt(dr, (W//2, 620), descs[mode], font(F_BOLD, 30), TEAL if mode else DIM, anchor="mm")

def scene_etl(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    tanks = [("EXTRACT", TEAL, 240), ("TRANSFORM", YELLOW, 640), ("LOAD", MAGENTA, 1040)]
    for name, col, x in tanks:
        glow_box(dr, [x-160, 200, x+160, 560], col, rad=18)
        dr.rectangle([x-160, 200, x+160, 560], fill=(10,14,38))
        txt(dr, (x, 250), name, font(F_BOLD, 30), col, anchor="mm")
    arrow(dr, 400, 380, 470, 380, DIM, 6)
    arrow(dr, 800, 380, 870, 380, DIM, 6)
    # particles flowing
    import random as _r
    _r.seed(23)
    parts = [( _r.random(), _r.random()*280+250, _r.choice([TEAL,YELLOW,MAGENTA,(150,150,200)]) ) for _ in range(46)]
    for seed, y, col in parts:
        px = ((t*160 + seed*1280) % 1280)
        if 60 < px < 1220 and y and abs(y-380) < 130:
            dr.ellipse([px-5, y-5, px+5, y+5], fill=col)
    # transform sparkles
    if t > 8:
        for i in range(8):
            a = t*2 + i*0.785
            sx, sy = 640 + math.cos(a)*90, 380 + math.sin(a)*70
            dr.ellipse([sx-4, sy-4, sx+4, sy+4], fill=YELLOW)
    # stage captions
    caps = [(240, "raw: CSVs, APIs, logs"), (640, "clean \u00b7 dedupe \u00b7 conform"), (1040, "warehouse tables")]
    for x, c in caps:
        txt(dr, (x, 600), c, font(F_SANS, 24), DIM, anchor="mm")
    if t > 22:
        txt(dr, (W//2, 120), "analytics begins where the pipeline ends",
            font(F_BOLD, 36), WHITE, anchor="mm")

def scene_gradient(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"]); dot_grid(dr)
    ox, oy = 140, 620
    # loss curve: parabola
    def curve(x):  # x in 0..1
        return oy - (0.15 + 0.75*(x-0.55)**2*2.2)*(oy-140)
    pts = [(140 + x*1000, curve(x)) for x in [i/200 for i in range(201)]]
    dr.line(pts, fill=(60,80,150), width=4)
    # ball rolls: x goes 0.95 -> 0.55 with easing + small oscillation
    k = ease(clamp((t-5)/16))
    bx = lerp(0.95, 0.55, k) + 0.02*math.sin(t*4)*(1-k)
    px, py = 140 + bx*1000, curve(bx)
    # trail
    for i in range(1, 24):
        kk = clamp((t-5)/16 - i*0.012)
        if kk <= 0: break
        bxx = lerp(0.95, 0.55, ease(kk))
        qx, qy = 140 + bxx*1000, curve(bxx)
        al = int(200*(1-i/24))
        dr.ellipse([qx-6, qy-6, qx+6, qy+6], fill=(al, al//3, al))
    dr.ellipse([px-14, py-14, px+14, py+14], fill=MAGENTA)
    dr.ellipse([px-14, py-14, px+14, py+14], outline=WHITE, width=2)
    # gradient arrow at ball
    slope = (curve(bx+0.01)-curve(bx-0.01))/0.02
    arrow(dr, px, py-40, px - 60, py-40, YELLOW, 5)
    txt(dr, (px-80, py-60), "-\u2207L", font(F_BOLD, 30), YELLOW, anchor="mm")
    txt(dr, (W//2, 90), "Gradient Descent", font(F_BOLD, 52), WHITE, anchor="mm")
    txt(dr, (W//2, 150), "follow the slope downhill, one step at a time",
        font(F_SANS, 28), DIM, anchor="mm")
    loss = (0.15 + 0.75*(bx-0.55)**2*2.2)
    txt(dr, (1100, 120), "loss = %.3f" % loss, font(F_MONOB, 30), MAGENTA, anchor="mm")

# ============================================================ VIDEO CONFIG
VIDEOS = [
 # --- IL-01 story cinema: Esoteric Foundations
 dict(file="story-emerald-tablet.mp4", style="story", scene=scene_emerald,
      kicker="IL-01 \u00b7 Esoteric Foundations", title="The Emerald Tablet",
      sub="As above, so below \u2014 the doctrine of correspondence", module=2,
      blurb="A cinematic scene on the Emerald Tablet and the Hermetic principle of correspondence: the macrocosm mirrored in the microcosm.",
      captions=[(4,10,"Hermes Trismegistus: legendary author of the Emerald Tablet"),
                (10,16,"\u2018As above, so below\u2019 \u2014 the macrocosm mirrors the microcosm"),
                (16,22,"Correspondence: every plane of being reflects every other"),
                (22,26,"The foundation of all Hermetic philosophy")]),
 dict(file="story-enochian-grid.mp4", style="story", scene=scene_enochian,
      kicker="IL-01 \u00b7 Esoteric Foundations", title="The Enochian Great Table",
      sub="John Dee & Edward Kelley, 1582\u20131589", module=3,
      blurb="The Great Table materializes square by square: Dee and Kelley's angelic system, the Renaissance's most complete magical framework.",
      captions=[(4,10,"Dee and Kelley recorded angelic communications in 49 \u2018calls\u2019"),
                (10,16,"The Great Table: a grid of lettered squares organizing the system"),
                (16,22,"Each square maps an angel, an element, a quarter of the world"),
                (22,26,"The most complete magical system of the Renaissance")]),
 dict(file="story-ccru-hyperstition.mp4", style="story", scene=scene_ccru,
      kicker="IL-01 \u00b7 Esoteric Foundations", title="Hyperstition",
      sub="The CCRU: when fiction makes itself real", module=4,
      blurb="The Cybernetic Culture Research Unit's hyperstition loop: fiction feeding machinery feeding reality until the loop closes.",
      captions=[(4,10,"The CCRU: Warwick\u2019s Cybernetic Culture Research Unit, 1990s"),
                (10,16,"Hyperstition: a fiction that bootstraps itself into reality"),
                (16,22,"Belief \u2192 signal \u2192 system \u2192 world: the loop closes"),
                (22,26,"Ideas that engineer their own conditions of existence")]),
 # --- IL-02: Mathematical Maturity Engine
 dict(file="3b1b-bayes.mp4", style="3b1b", scene=scene_bayes,
      kicker="IL-02 \u00b7 Mathematical Maturity Engine", title="Bayes\u2019 Theorem",
      sub="Updating beliefs with evidence", module=1,
      blurb="An area-model walkthrough of Bayes' theorem: prior times likelihood, normalized into a posterior.",
      captions=[(4,10,"Start with a prior belief: P(H) = 0.30"),
                (10,16,"New evidence arrives \u2014 how likely is it under each hypothesis?"),
                (16,22,"Multiply prior by likelihood, then normalize"),
                (22,26,"Posterior: the updated belief. Evidence compounds.")]),
 dict(file="3b1b-vectors.mp4", style="3b1b", scene=scene_vectors,
      kicker="IL-02 \u00b7 Mathematical Maturity Engine", title="Linear Transformations",
      sub="Matrices as geometric motion", module=2,
      blurb="Watch a matrix move the basis vectors i and j; every vector in the plane follows the grid as it morphs.",
      captions=[(4,10,"Two basis vectors span the plane: i and j"),
                (10,16,"A matrix remaps the basis: rotation plus stretch"),
                (16,22,"Every vector follows the basis \u2014 the whole grid transforms"),
                (22,26,"Linear algebra is geometry in disguise")]),
 dict(file="primer-galton.mp4", style="primer", scene=scene_galton,
      kicker="IL-02 \u00b7 Mathematical Maturity Engine", title="The Galton Board",
      sub="Order emerges from chaos", module=1,
      blurb="A living simulation: 170 balls bounce through a peg triangle and the bins fill into a bell curve \u2014 the central limit theorem, visible.",
      captions=[(4,10,"Balls fall through a triangle of pegs, bouncing left or right"),
                (10,16,"Each bounce is a coin flip \u2014 pure randomness"),
                (16,22,"Yet the bins fill into a perfect bell curve"),
                (22,26,"The normal distribution emerges from the central limit theorem")]),
 # --- IL-03: Programming Language Forge
 dict(file="fireship-recursion.mp4", style="fireship", scene=scene_recursion,
      kicker="IL-03 \u00b7 Programming Language Forge", title="Recursion in 100 Seconds",
      sub="Functions calling functions", module=2,
      blurb="fib(5) pushes frames onto the call stack, hits base cases, then unwinds with the answer: 5.",
      captions=[(4,10,"fib(5) calls fib(4) and fib(3) \u2014 the stack grows"),
                (10,16,"Base cases return: fib(1)=1, fib(0)=0 \u2014 the stack unwinds"),
                (16,22,"Each frame resolves: 1, 1, 2, 3, 5"),
                (22,26,"Recursion = base case + self-similar decomposition")]),
 dict(file="fireship-pointers.mp4", style="fireship", scene=scene_pointers,
      kicker="IL-03 \u00b7 Programming Language Forge", title="Pointers Explained",
      sub="Memory addresses, visualized", module=3,
      blurb="A memory grid shows x at 0x7FF8, p storing its address, and *p dereferencing to read 42.",
      captions=[(4,10,"x lives at 0x7FF8 \u2014 a box holding 42"),
                (10,16,"p = &x: a pointer storing the ADDRESS of x"),
                (16,22,"*p dereferences: follow the arrow to read 42"),
                (22,26,"Pointers are just addresses with a type attached")]),
 dict(file="fireship-big-o.mp4", style="fireship", scene=scene_bigo,
      kicker="IL-03 \u00b7 Programming Language Forge", title="Big-O in 100 Seconds",
      sub="How algorithms scale", module=0,
      blurb="Three curves race: O(1) flatlines, O(n) climbs, O(n\u00b2) explodes \u2014 pick the curve, not the constant.",
      captions=[(4,10,"O(1): constant \u2014 one step no matter the input"),
                (10,16,"O(n): linear \u2014 steps grow with input size"),
                (16,22,"O(n\u00b2): quadratic \u2014 doubling the input quadruples the work"),
                (22,26,"Pick the curve, not the constant")]),
 # --- IL-04: Systems, Linux, Windows & Networks
 dict(file="bbg-process-scheduler.mp4", style="bbg", scene=scene_scheduler,
      kicker="IL-04 \u00b7 Systems, Linux, Windows & Networks", title="Round-Robin Scheduling",
      sub="How the CPU shares time", module=3,
      blurb="Four processes take 100ms quanta on the CPU in rotation: fair, preemptive, simple round-robin.",
      captions=[(4,10,"Four processes wait in the ready queue"),
                (10,16,"Each gets a 100ms quantum on the CPU"),
                (16,22,"Quantum expires \u2192 context switch \u2192 next process"),
                (22,26,"Fair, preemptive, simple: round-robin")]),
 dict(file="bbg-subnetting.mp4", style="bbg", scene=scene_subnetting,
      kicker="IL-04 \u00b7 Systems, Linux, Windows & Networks", title="Subnetting",
      sub="Dividing 192.168.1.0/24", module=4,
      blurb="Borrowing two host bits splits a /24 into four /26 subnets of 62 usable hosts each.",
      captions=[(4,10,"A /24 network: 32 bits, 24 fixed, 8 for hosts"),
                (10,16,"Borrow 2 host bits \u2192 four /26 subnets"),
                (16,22,"Each subnet: 62 usable hosts, its own broadcast"),
                (22,26,"Subnetting = hierarchy inside the address")]),
 dict(file="bbg-inode.mp4", style="bbg", scene=scene_inode,
      kicker="IL-04 \u00b7 Systems, Linux, Windows & Networks", title="Inodes",
      sub="How Linux names files", module=2,
      blurb="A filename points to an inode; the inode holds metadata and the list of data blocks on disk.",
      captions=[(4,10,"A filename is just a pointer in a directory"),
                (10,16,"The inode holds metadata: owner, size, timestamps"),
                (16,22,"The inode lists the data blocks on disk"),
                (22,26,"Names point to inodes; inodes point to data")]),
 # --- IL-05: Cloud, DevSecOps, Platform & SRE
 dict(file="bbg-kubernetes.mp4", style="bbg", scene=scene_k8s,
      kicker="IL-05 \u00b7 Cloud, DevSecOps, Platform & SRE", title="Kubernetes Architecture",
      sub="The control plane and the fleet", module=3,
      blurb="Control plane components schedule pods onto worker nodes; a rolling update swaps v1 pods for v2 with zero downtime.",
      captions=[(4,10,"The control plane: API server, scheduler, etcd"),
                (10,16,"Worker nodes run kubelets and pods"),
                (16,22,"The scheduler places pods; the kubelet keeps them alive"),
                (22,26,"Desired state, continuously reconciled")]),
 dict(file="bbg-cicd.mp4", style="bbg", scene=scene_cicd,
      kicker="IL-05 \u00b7 Cloud, DevSecOps, Platform & SRE", title="CI/CD Pipeline",
      sub="From commit to production", module=2,
      blurb="A commit travels commit \u2192 build \u2192 test \u2192 scan \u2192 deploy, with quality gates at every stage.",
      captions=[(4,10,"A commit triggers the pipeline"),
                (10,16,"Build \u2192 test \u2192 scan: quality gates in sequence"),
                (16,22,"Artifacts promote: staging, then production"),
                (22,26,"Every change, shippable in minutes")]),
 dict(file="bbg-terraform.mp4", style="bbg", scene=scene_terraform,
      kicker="IL-05 \u00b7 Cloud, DevSecOps, Platform & SRE", title="Terraform",
      sub="Infrastructure as code", module=5,
      blurb="Declare desired state in main.tf, preview with terraform plan, converge reality with apply \u2014 state remembers.",
      captions=[(4,10,"You declare desired state in .tf files"),
                (10,16,"terraform plan: the diff \u2014 what will change"),
                (16,22,"terraform apply: providers converge reality to the plan"),
                (22,26,"State is the memory of your infrastructure")]),
 # --- IL-06: Cybersecurity & Secure Engineering
 dict(file="bbg-pki.mp4", style="bbg", scene=scene_pki,
      kicker="IL-06 \u00b7 Cybersecurity & Secure Engineering", title="The PKI Trust Chain",
      sub="Why your browser trusts a site", module=3,
      blurb="Root CA signs intermediate, intermediate signs the leaf; the browser walks the chain to a trusted root.",
      captions=[(4,10,"A root CA anchors trust \u2014 self-signed, widely distributed"),
                (10,16,"The root signs an intermediate; the intermediate signs the leaf"),
                (16,22,"Your browser walks the chain up to a trusted root"),
                (22,26,"Trust is delegated, verifiable, and revocable")]),
 dict(file="bbg-siem-pipeline.mp4", style="bbg", scene=scene_siem,
      kicker="IL-06 \u00b7 Cybersecurity & Secure Engineering", title="SIEM Detection Pipeline",
      sub="From log noise to alert", module=5,
      blurb="Millions of events stream in; the SIEM normalizes, correlates, and enriches until one rule fires: brute force.",
      captions=[(4,10,"Endpoints and firewalls stream millions of events"),
                (10,16,"The SIEM normalizes, correlates, and enriches"),
                (16,22,"A correlation rule fires: brute force detected"),
                (22,26,"The SOC analyst gets one alert \u2014 not a million logs")]),
 dict(file="bbg-killchain.mp4", style="bbg", scene=scene_killchain,
      kicker="IL-06 \u00b7 Cybersecurity & Secure Engineering", title="The Cyber Kill Chain",
      sub="Seven stages of an attack", module=5,
      blurb="Recon to actions-on-objectives: seven stages light up in sequence \u2014 defenders win by breaking any single link.",
      captions=[(4,10,"Reconnaissance \u2192 weaponization \u2192 delivery"),
                (10,16,"Exploitation \u2192 installation \u2192 command & control"),
                (16,22,"Actions on objectives: the defender\u2019s last chance is early"),
                (22,26,"Break any link \u2014 the chain fails")]),
 # --- IL-07: SQL, Data Engineering, Analytics & AI
 dict(file="3b1b-sql-joins.mp4", style="3b1b", scene=scene_sql_joins,
      kicker="IL-07 \u00b7 SQL, Data Engineering, Analytics & AI", title="SQL Joins as Venn Diagrams",
      sub="Set logic for tables", module=3,
      blurb="Customers and orders as overlapping sets: INNER keeps the intersection, LEFT keeps the left, FULL keeps everything.",
      captions=[(4,10,"Two tables: customers (teal) and orders (amber)"),
                (10,16,"INNER JOIN: only the intersection \u2014 matched rows"),
                (16,22,"LEFT JOIN: all of the left, plus matches"),
                (22,26,"FULL JOIN: everything, matched or not")]),
 dict(file="3b1b-etl-pipeline.mp4", style="3b1b", scene=scene_etl,
      kicker="IL-07 \u00b7 SQL, Data Engineering, Analytics & AI", title="The ETL Pipeline",
      sub="Extract, transform, load", module=3,
      blurb="Raw data pours into extract, sparkles through transform, and lands as curated warehouse tables in load.",
      captions=[(4,10,"Extract: raw data pours in from a dozen sources"),
                (10,16,"Transform: clean, dedupe, conform to schema"),
                (16,22,"Load: curated tables land in the warehouse"),
                (22,26,"Analytics starts where the pipeline ends")]),
 dict(file="3b1b-gradient-descent.mp4", style="3b1b", scene=scene_gradient,
      kicker="IL-07 \u00b7 SQL, Data Engineering, Analytics & AI", title="Gradient Descent",
      sub="Learning by rolling downhill", module=4,
      blurb="A ball rolls down the loss curve following the negative gradient, settling at the minimum \u2014 downhill walking is all of deep learning.",
      captions=[(4,10,"The loss curve: error as a function of the weights"),
                (10,16,"Start anywhere \u2014 the gradient points downhill"),
                (16,22,"Step, recompute, repeat: the ball rolls to the minimum"),
                (22,26,"All of deep learning is downhill walking")]),
]

COURSE_FILES = {
    1: "il-01-esoteric-foundations.json",
    2: "il-02-mathematical-maturity-engine.json",
    3: "il-03-programming-language-forge.json",
    4: "il-04-systems-linux-windows-networks.json",
    5: "il-05-cloud-devsecops-platform-sre.json",
    6: "il-06-cybersecurity-secure-engineering.json",
    7: "il-07-data-engineering-analytics-ai.json",
}
ACCENTS = {"story": GOLD, "3b1b": YELLOW, "fireship": MAGENTA, "bbg": BLUE, "primer": CYAN}

def render_video(v):
    fname = v["file"]
    path = os.path.join(OUT, fname)
    style, scene = v["style"], v["scene"]
    accent = ACCENTS[style]
    caps = sorted(v["captions"])
    def frames():
        total = int(NFR/8) if SMOKE else NFR
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
                end_card(dr, style, v["title"], v["kicker"], t-26)
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
    vids = [v for v in VIDEOS if (only is None or v["file"] in only or v["file"].replace(".mp4","") in only)]
    print("Rendering %d videos (SMOKE=%s)" % (len(vids), SMOKE), flush=True)
    for v in vids:
        print("START", v["file"], flush=True)
        try:
            render_video(v)
        except Exception as e:
            print("FAILED %s: %r" % (v["file"], e), flush=True)

if __name__ == "__main__":
    main()
