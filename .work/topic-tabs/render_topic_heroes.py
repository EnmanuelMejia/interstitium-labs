#!/usr/bin/env python3
"""
Topic hero loop renderer — 12 themed ambient animated backgrounds.
Original code. 6s @ 24fps, 960x540 frames -> 854x480 crf30 mp4 + jpg poster.
Usage: python3 render_topic_heroes.py [slug ...]   (default: all 12)
"""
import sys, os, math, random, subprocess, shutil
sys.path.insert(0, "/home/hatch/workspace/story-videos")
from il_anim import STYLES, get_font
from PIL import Image, ImageDraw, ImageFilter

W, H = 960, 540
FPS, SECS = 24, 6
NFRAMES = FPS * SECS
OUT_DIR = "/home/hatch/workspace/apex-audit/docs/assets/topics"
os.makedirs(OUT_DIR, exist_ok=True)

def cfg(theme):
    return STYLES[theme]

def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def paste(base, lay):
    base.alpha_composite(lay)

# ---------------- ambient painters: draw(lay, d, p, theme, rng) ; p in [0,1) ----------------
def p_mrrobot(lay, d, p, th, rng):
    acc = th["accent"]; f = get_font(22)
    cols = 48
    for c in range(cols):
        x = c * (W // cols) + 6
        speed = 0.5 + rng.random() * 0.9
        y0 = ((p * speed + rng.random()) % 1.0) * (H + 200) - 100
        for k in range(14):
            y = y0 - k * 26
            if -30 < y < H + 30:
                ch = "1" if rng.random() < 0.5 else "0"
                a = max(0, 200 - k * 16)
                d.text((x, y), ch, font=f, fill=acc + (a,))
    # scanlines
    for y in range(0, H, 4):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 70))

def p_cyberpunk(lay, d, p, th, rng):
    acc, sec = th["accent"], th["secondary"]
    for i in range(70):
        x = (rng.random() * W + p * 60 * (0.3 + rng.random())) % W
        y = (rng.random() * H - p * 160 * (0.4 + rng.random())) % H
        r = 1 + int(rng.random() * 3)
        col = acc if rng.random() < 0.55 else sec
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (200,))
    for i in range(26):  # rain streaks
        x = (rng.random() * W + p * 200) % (W + 200) - 100
        y = (rng.random() * H + p * 700) % (H + 200) - 100
        ln = 30 + rng.random() * 60
        col = acc if rng.random() < 0.5 else sec
        d.line([(x, y), (x - ln * 0.25, y + ln)], fill=col + (120,), width=2)

def p_tron(lay, d, p, th, rng):
    acc = th["accent"]
    cx, hy = W // 2, int(H * 0.42)
    # perspective grid: verticals to vanishing point
    for i in range(-14, 15):
        x2 = cx + i * 40
        d.line([(cx + i * 6, hy), (x2, H)], fill=acc + (70,), width=1)
    # horizontals scrolling toward viewer
    for k in range(12):
        t = ((p * 3 + k / 12) % 1.0)
        y = hy + (H - hy) * t * t
        a = int(40 + 160 * t)
        d.line([(0, y), (W, y)], fill=acc + (a,), width=1)
    # horizon glow pulse
    pulse = 0.5 + 0.5 * math.sin(p * 2 * math.pi * 2)
    d.line([(0, hy), (W, hy)], fill=acc + (int(90 + 110 * pulse),), width=3)

def p_steampunk(lay, d, p, th, rng):
    acc = th["accent"]
    # slow rotating gear silhouette
    g = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([60, 60, 300, 300], outline=acc + (50,), width=10)
    for a in range(0, 360, 30):
        r = math.radians(a)
        x1, y1 = 180 + 120 * math.cos(r), 180 + 120 * math.sin(r)
        x2, y2 = 180 + 150 * math.cos(r), 180 + 150 * math.sin(r)
        gd.line([(x1, y1), (x2, y2)], fill=acc + (50,), width=16)
    gd.ellipse([140, 140, 220, 220], outline=acc + (60,), width=6)
    rot = g.rotate(p * 360 * 0.25, resample=Image.BICUBIC, center=(180, 180))
    lay.alpha_composite(rot, (W - 380, 60))
    for i in range(50):  # brass dust
        x = rng.random() * W
        y = (rng.random() * H + p * 40 * (0.3 + rng.random())) % H
        r = 1 + int(rng.random() * 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=acc + (140,))

def p_exmachina(lay, d, p, th, rng):
    acc = th["accent"]
    for i in range(9):
        y = int((i + 0.5) * H / 9)
        ph = (p * 2 + rng.random()) % 1.0
        a = int(120 * max(0, math.sin(ph * math.pi)))
        x0 = int(rng.random() * W * 0.3)
        x1 = int(W - rng.random() * W * 0.3)
        d.line([(x0, y), (x1, y)], fill=acc + (a,), width=1)
    # single scanning line
    sy = int((p % 1.0) * H)
    d.line([(0, sy), (W, sy)], fill=acc + (60,), width=2)

def p_oceandeep(lay, d, p, th, rng):
    acc = th["accent"]
    for wv in range(4):
        pts = []
        base_y = H * (0.3 + 0.18 * wv)
        for x in range(0, W + 8, 8):
            y = base_y + 26 * math.sin(x / 130 + p * 2 * math.pi * (1 + wv * 0.3) + wv)
            pts.append((x, y))
        d.line(pts, fill=acc + (110 - wv * 18,), width=2)
    for i in range(60):  # rising plankton
        x = rng.random() * W
        y = (rng.random() * H - p * 90 * (0.4 + rng.random())) % H
        r = 1 + int(rng.random() * 2)
        tw = 0.5 + 0.5 * math.sin(p * 6.28 * 3 + i)
        d.ellipse([x - r, y - r, x + r, y + r], fill=acc + (int(90 + 110 * tw),))

def p_hackers95(lay, d, p, th, rng):
    acc, sec = th["accent"], th["secondary"]
    for i in range(30):  # fast diagonal streaks
        x = (rng.random() * (W + 400) + p * 900) % (W + 400) - 200
        y = rng.random() * H
        ln = 60 + rng.random() * 120
        col = acc if rng.random() < 0.5 else sec
        d.line([(x, y), (x - ln, y + ln * 0.4)], fill=col + (130,), width=3)
    for i in range(8):  # skewed blocks
        x = (rng.random() * W + p * 120) % W
        y = rng.random() * H
        w2, h2 = 40 + rng.random() * 80, 14
        col = acc if rng.random() < 0.5 else sec
        d.polygon([(x, y), (x + w2, y), (x + w2 - 18, y + h2), (x - 18, y + h2)], outline=col + (90,))

def p_alexandria(lay, d, p, th, rng):
    acc = th["accent"]
    for i in range(5):  # column silhouettes
        x = int((i + 0.7) * W / 6)
        d.rectangle([x - 34, 120, x + 34, H], fill=(0, 0, 0, 110))
        d.line([(x - 34, 120), (x + 34, 120)], fill=acc + (120,), width=2)
        d.line([(x - 34, 120), (x - 34, H)], fill=acc + (70,), width=1)
        d.line([(x + 34, 120), (x + 34, H)], fill=acc + (70,), width=1)
    for i in range(70):  # gold dust rising
        x = rng.random() * W
        y = (rng.random() * H - p * 60 * (0.4 + rng.random())) % H
        tw = 0.5 + 0.5 * math.sin(p * 6.28 * 2 + i * 1.7)
        r = 1 + int(rng.random() * 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=acc + (int(80 + 120 * tw),))

def p_industrial(lay, d, p, th, rng):
    acc = th["accent"]
    for y in range(0, H, 4):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 80))
    # hazard bar bottom, pulsing
    pulse = 0.5 + 0.5 * math.sin(p * 2 * math.pi * 3)
    y0 = H - 34
    for x in range(0, W, 44):
        col = acc + (int(120 + 100 * pulse),) if (x // 44) % 2 == 0 else (20, 12, 0, 200)
        d.polygon([(x, y0), (x + 22, y0), (x + 12, H), (x - 10, H)], fill=col)
    for i in range(40):  # sparks
        x = rng.random() * W
        y = H - rng.random() * 200 - p * 150 % 200
        r = 1 + int(rng.random() * 2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=acc + (170,))

def p_sacredgeo(lay, d, p, th, rng):
    acc = th["accent"]
    cx, cy = W // 2, H // 2
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for k, rad in enumerate([70, 130, 195, 265]):
        pts = []
        for a in range(0, 360, 45):
            r = math.radians(a)
            pts.append((cx + rad * math.cos(r), cy + rad * math.sin(r) * 0.62))
        gd.line(pts + [pts[0]], fill=acc + (70 + k * 12,), width=1)
    rot = g.rotate(p * 360 * 0.12, resample=Image.BICUBIC, center=(cx, cy))
    lay.alpha_composite(rot)
    for i in range(40):
        x = rng.random() * W; y = rng.random() * H
        tw = 0.5 + 0.5 * math.sin(p * 6.28 * 2 + i)
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=acc + (int(70 + 90 * tw),))

def p_vaporwave(lay, d, p, th, rng):
    acc, sec = th["accent"], th["secondary"]
    # sunset gradient
    for y in range(H):
        t = y / H
        r = int(24 + t * 60); gg = int(4 + t * 40); b = int(54 + t * 60)
        d.line([(0, y), (W, y)], fill=(r, gg, b, 255))
    # slit sun bobbing
    sy = int(H * 0.34 + 8 * math.sin(p * 2 * math.pi))
    sun = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    sd.ellipse([10, 10, 210, 210], fill=acc + (200,))
    for yy in range(120, 210, 14):
        sd.rectangle([10, yy, 210, yy + 6], fill=(0, 0, 0, 0))
    sun = sun.filter(ImageFilter.GaussianBlur(2))
    lay.alpha_composite(sun, (W // 2 - 110, sy - 110))
    # grid floor scrolling
    hy = int(H * 0.62)
    for i in range(-12, 13):
        d.line([(W // 2 + i * 8, hy), (W // 2 + i * 60, H)], fill=sec + (80,), width=1)
    for k in range(8):
        t = ((p * 2 + k / 8) % 1.0)
        y = hy + (H - hy) * t * t
        d.line([(0, y), (W, y)], fill=sec + (int(50 + 90 * t),), width=1)

def p_goldrush(lay, d, p, th, rng):
    acc = th["accent"]
    for i in range(90):
        x = rng.random() * W + 20 * math.sin(p * 6.28 + i)
        y = (rng.random() * H - p * 70 * (0.4 + rng.random())) % H
        tw = 0.5 + 0.5 * math.sin(p * 6.28 * 2.5 + i * 2.1)
        r = 1 + int(rng.random() * 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=acc + (int(80 + 130 * tw),))
    pulse = 0.5 + 0.5 * math.sin(p * 2 * math.pi * 1.5)
    gx, gy = W // 2, H // 2
    for rr, aa in [(180, 18), (120, 30), (60, 45)]:
        a2 = int(aa * (0.6 + 0.4 * pulse))
        d.ellipse([gx - rr, gy - rr, gx + rr, gy + rr], outline=acc + (a2,), width=2)

PAINTERS = {
    "mr-robot": p_mrrobot, "cyberpunk": p_cyberpunk, "tron": p_tron,
    "steampunk": p_steampunk, "exmachina": p_exmachina, "oceandeep": p_oceandeep,
    "hackers95": p_hackers95, "alexandria": p_alexandria, "industrial": p_industrial,
    "sacredgeo": p_sacredgeo, "vaporwave": p_vaporwave, "goldrush": p_goldrush,
}

TOPICS = [
    ("cybersecurity", "mr-robot"), ("system-design", "cyberpunk"),
    ("networking", "tron"), ("cloud-devops", "steampunk"),
    ("ai-ml", "exmachina"), ("data-eng", "oceandeep"),
    ("programming", "hackers95"), ("databases", "alexandria"),
    ("linux-systems", "industrial"), ("math", "sacredgeo"),
    ("web-dev", "vaporwave"), ("blockchain", "goldrush"),
]

def render_one(slug, theme):
    th = cfg(theme)
    bg = th["bg"]
    tmp = f"/tmp/topic_hero_{slug}"
    fdir = os.path.join(tmp, "frames")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(fdir, exist_ok=True)
    rng = random.Random(hash(slug) % (2 ** 32))
    # pre-roll rng state per frame deterministically
    states = [random.Random(hash(slug) % (2 ** 32) + i * 7919) for i in range(NFRAMES)]
    paint = PAINTERS[theme]
    for i in range(NFRAMES):
        prog = i / NFRAMES
        img = Image.new("RGBA", (W, H), bg + (255,))
        lay = layer()
        d = ImageDraw.Draw(lay)
        paint(lay, d, prog, th, states[i])
        img.alpha_composite(lay)
        img.convert("RGB").save(f"{fdir}/f{i:05d}.png")
    out = os.path.join(OUT_DIR, f"{slug}-hero.mp4")
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", f"{fdir}/f%05d.png",
                    "-vf", "scale=854:480", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "30", "-preset", "veryfast", "-an", out],
                   capture_output=True, check=True)
    # poster from mid frame
    mid = Image.open(f"{fdir}/f{72:05d}.png").convert("RGB").resize((854, 480))
    mid.save(os.path.join(OUT_DIR, f"{slug}-hero.jpg"), quality=82)
    shutil.rmtree(tmp, ignore_errors=True)
    sz = os.path.getsize(out)
    print(f"OK {slug}: {sz//1024}KB", flush=True)

if __name__ == "__main__":
    want = sys.argv[1:] or [s for s, _ in TOPICS]
    for slug, theme in TOPICS:
        if slug in want:
            render_one(slug, theme)
