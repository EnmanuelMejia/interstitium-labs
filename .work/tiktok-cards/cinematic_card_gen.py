#!/usr/bin/env python3
"""
TikTok-Style Cinematic Card Generator
Recreates the IL-29 TikTok card style programmatically for all projects.

Style elements:
- Dark cyberpunk background with HUD panels
- Central hexagonal badge with circuit-board texture
- Thematic icon at top of badge
- Rotating text ring around badge (alternating words)
- Bold typography: project code (cyan), partner (orange), subtitle (cyan),
  main title (cyan + orange), INTERSTITIUM LABS branding
- Particle systems, glitch effects, glow accents

Original work - style recreation, not frame copying.
"""
import os, math, random, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Colors (matching TikTok IL-29)
BG_DARK = (5, 8, 16)
CYAN = (0, 212, 255)
CYAN_DIM = (0, 140, 180)
ORANGE = (255, 140, 0)
ORANGE_DIM = (180, 90, 0)
WHITE = (240, 246, 252)
GRAY = (100, 110, 125)
RED = (255, 60, 60)
BLUE = (60, 120, 255)
GREEN = (0, 220, 130)
PURPLE = (160, 100, 255)

FPS = 24
DURATION = 10.0

def get_font(size, bold=True):
    """Get DejaVu font."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for p in [f"/usr/share/fonts/truetype/dejavu/{name}",
              f"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def hex_points(cx, cy, r, rot=0):
    """Get 6 points of hexagon."""
    return [(cx + r * math.cos(rot + i * math.pi / 3),
             cy + r * math.sin(rot + i * math.pi / 3)) for i in range(6)]

def draw_circuit_texture(d, cx, cy, r, seed=42, color=CYAN_DIM):
    """Draw circuit board traces inside hexagon area."""
    rng = random.Random(seed)
    # Draw random circuit traces
    for _ in range(25):
        x = cx + rng.uniform(-r*0.7, r*0.7)
        y = cy + rng.uniform(-r*0.7, r*0.7)
        # Horizontal/vertical traces with 45-degree bends
        x2 = x + rng.uniform(-60, 60)
        y2 = y
        x3 = x2 + rng.uniform(-30, 30)
        y3 = y2 + rng.uniform(-60, 60)
        d.line([(x, y), (x2, y2), (x3, y3)], fill=color, width=1)
        # Via dots
        d.ellipse([x3-3, y3-3, x3+3, y3+3], fill=color)
    # Small squares (chips)
    for _ in range(8):
        x = cx + rng.uniform(-r*0.6, r*0.6)
        y = cy + rng.uniform(-r*0.6, r*0.6)
        s = rng.uniform(4, 10)
        d.rectangle([x-s/2, y-s/2, x+s/2, y+s/2], outline=color, width=1)

def draw_hud_panels(d, W, H, t, seed=1):
    """Draw HUD side panels with tiny text and charts."""
    rng = random.Random(seed)
    # Left panel
    for i in range(6):
        y = 80 + i * 140
        # Panel outline
        d.rectangle([15, y, 150, y+110], outline=(30, 50, 70), width=1)
        # Tiny text lines (simulated)
        for j in range(5):
            ly = y + 15 + j * 16
            lw = rng.uniform(40, 110)
            d.line([(25, ly), (25+lw, ly)], fill=(40, 70, 90), width=2)
        # Warning triangle occasionally
        if rng.random() > 0.6:
            d.polygon([(130, y+15), (140, y+35), (120, y+35)], outline=RED, width=1)
    # Right panel
    for i in range(6):
        y = 80 + i * 140
        d.rectangle([W-150, y, W-15, y+110], outline=(30, 50, 70), width=1)
        for j in range(5):
            ly = y + 15 + j * 16
            lw = rng.uniform(40, 110)
            d.line([(W-140, ly), (W-140+lw, ly)], fill=(40, 70, 90), width=2)
    # Binary code strips
    for i in range(3):
        y = 200 + i * 300
        txt = ''.join(rng.choice('01') for _ in range(12))
        d.text((20, y), txt, font=get_font(10), fill=(30, 60, 80))
        d.text((W-110, y+50), txt[::-1], font=get_font(10), fill=(30, 60, 80))

def draw_particles(d, W, H, t, n=80, seed=99):
    """Draw floating particles (cyan sparks, orange embers)."""
    rng = random.Random(seed)
    for i in range(n):
        # Pseudo-random but deterministic per particle
        px = (rng.random() * W + t * rng.uniform(-20, 20)) % W
        py = (rng.random() * H - t * rng.uniform(10, 50)) % H
        size = rng.uniform(1, 3)
        if rng.random() > 0.7:
            color = ORANGE  # embers
        else:
            color = CYAN  # sparks
        alpha = int(150 + 100 * math.sin(t * 3 + i))
        d.ellipse([px-size, py-size, px+size, py+size], fill=color)

def draw_rotating_ring(d, cx, cy, r, t, words, colors):
    """Draw rotating text ring around badge."""
    n_words = len(words)
    for i, (word, color) in enumerate(zip(words, colors)):
        # Angle for this word, rotating over time
        base_angle = (i / n_words) * 2 * math.pi
        angle = base_angle + t * 0.3  # slow rotation
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        # Rotate text to be tangent
        # PIL doesn't rotate text easily, so we draw at angle
        font = get_font(22)
        # Draw text centered at position
        d.text((x, y), word, font=font, fill=color, anchor="mm")

def draw_glow_text(d, pos, text, font, color, glow_color=None, anchor="mm"):
    """Draw text with glow effect (layered)."""
    if glow_color is None:
        glow_color = color
    x, y = pos
    # Glow layers (offset copies with lower opacity simulation)
    for offset in [(3, 0), (-3, 0), (0, 3), (0, -3), (2, 2), (-2, -2)]:
        d.text((x+offset[0], y+offset[1]), text, font=font, 
               fill=tuple(max(0, c-100) for c in glow_color), anchor=anchor)
    # Main text
    d.text((x, y), text, font=font, fill=color, anchor=anchor)

def draw_corner_brackets(d, x, y, w, h, color=CYAN, size=20, width=3):
    """Draw corner brackets like [ ] around text."""
    # Top-left
    d.line([(x, y+size), (x, y), (x+size, y)], fill=color, width=width)
    # Top-right
    d.line([(x+w-size, y), (x+w, y), (x+w, y+size)], fill=color, width=width)
    # Bottom-left
    d.line([(x, y+h-size), (x, y+h), (x+size, y+h)], fill=color, width=width)
    # Bottom-right
    d.line([(x+w-size, y+h), (x+w, y+h), (x+w, y+h-size)], fill=color, width=width)

# Project configurations
PROJECTS = {
    "il-26": {
        "code": "IL-26",
        "partner": "DATA ANALYST",
        "subtitle": "CERTIFICATION & SENIOR MASTERY",
        "title1": "DATA ANALYTICS",
        "title2": "BOOTCAMP",
        "icon": "chart",  # bar chart icon
        "ring_words": ["SQL", "PYTHON", "PANDAS", "TABLEAU"],
        "ring_colors": [CYAN, ORANGE, CYAN, ORANGE],
        "accent": CYAN,
        "secondary": BLUE,
    },
    "il-28": {
        "code": "IL-28",
        "partner": "DEVSECOPS",
        "subtitle": "CLOUD INFRASTRUCTURE MASTERY",
        "title1": "DEVSECOPS & CLOUD",
        "title2": "BOOTCAMP",
        "icon": "cloud",
        "ring_words": ["KUBERNETES", "TERRAFORM", "DOCKER", "AWS"],
        "ring_colors": [CYAN, PURPLE, CYAN, PURPLE],
        "accent": CYAN,
        "secondary": PURPLE,
    },
    "il-29": {
        "code": "IL-29",
        "partner": "THREATLOCKER",
        "subtitle": "ZERO-TRUST CBT WITH AI",
        "title1": "CYBERSECURITY MASTERY",
        "title2": "BOOTCAMP",
        "icon": "lock",
        "ring_words": ["ALLOWLIST", "DENYLIST", "ALLOWLIST", "DENYLIST"],
        "ring_colors": [CYAN, ORANGE, CYAN, ORANGE],
        "accent": CYAN,
        "secondary": ORANGE,
    },
    "devops-superlab": {
        "code": "SUPERLAB",
        "partner": "DEVOPS",
        "subtitle": "HANDS-ON INFRASTRUCTURE LAB",
        "title1": "DEVOPS SUPERLAB",
        "title2": "EXPERIENCE",
        "icon": "terminal",
        "ring_words": ["BASH", "GIT", "CI/CD", "LINUX"],
        "ring_colors": [GREEN, CYAN, GREEN, CYAN],
        "accent": GREEN,
        "secondary": CYAN,
    },
    "rhel-fabric": {
        "code": "RHEL-10",
        "partner": "RED HAT",
        "subtitle": "BARE-METAL AI SYSTEMS FABRIC",
        "title1": "RHEL AI & SYSTEMS",
        "title2": "FABRIC",
        "icon": "server",
        "ring_words": ["KVM", "PODMAN", "ANSIBLE", "SELINUX"],
        "ring_colors": [RED, CYAN, RED, CYAN],
        "accent": RED,
        "secondary": CYAN,
    },
    "bootcamp-catalog": {
        "code": "68×",
        "partner": "INTERSTITIUM",
        "subtitle": "INTERACTIVE PREP BOOTCAMPS",
        "title1": "CERTIFICATION BOOTCAMP",
        "title2": "CATALOG",
        "icon": "cap",
        "ring_words": ["COMPTIA", "AWS", "CISSP", "AZURE"],
        "ring_colors": [CYAN, ORANGE, CYAN, ORANGE],
        "accent": CYAN,
        "secondary": ORANGE,
    },
    "tl-interview": {
        "code": "TL-INT",
        "partner": "THREATLOCKER",
        "subtitle": "INTERVIEW PREPARATION",
        "title1": "THREATLOCKER INTERVIEW",
        "title2": "PREP BOOTCAMP",
        "icon": "shield",
        "ring_words": ["PREP", "MOCK", "PREP", "MOCK"],
        "ring_colors": [CYAN, ORANGE, CYAN, ORANGE],
        "accent": CYAN,
        "secondary": ORANGE,
    },
    "tl-assessment": {
        "code": "TL-ASM",
        "partner": "THREATLOCKER",
        "subtitle": "ASSESSMENT PREPARATION",
        "title1": "THREATLOCKER ASSESSMENT",
        "title2": "PREP CBT",
        "icon": "checklist",
        "ring_words": ["QUIZ", "DRILL", "QUIZ", "DRILL"],
        "ring_colors": [CYAN, ORANGE, CYAN, ORANGE],
        "accent": CYAN,
        "secondary": ORANGE,
    },
    "ai-vision": {
        "code": "AIV",
        "partner": "INTERSTITIUM",
        "subtitle": "END-TO-END AI AUTOMATION",
        "title1": "AI VISION DECK",
        "title2": "ARCHITECTURE",
        "icon": "eye",
        "ring_words": ["VISION", "NEURAL", "VISION", "NEURAL"],
        "ring_colors": [PURPLE, CYAN, PURPLE, CYAN],
        "accent": PURPLE,
        "secondary": CYAN,
    },
    "lps-enrollment": {
        "code": "LPS",
        "partner": "LAWRENCE PUBLIC SCHOOLS",
        "subtitle": "ENROLLMENT DATA ANALYSIS",
        "title1": "ENROLLMENT ANALYSIS",
        "title2": "CASE STUDY",
        "icon": "chart",
        "ring_words": ["DATA", "TRENDS", "DATA", "TRENDS"],
        "ring_colors": [BLUE, CYAN, BLUE, CYAN],
        "accent": BLUE,
        "secondary": CYAN,
    },
}

def fit_font_size(text, max_width, start_size=72, min_size=36):
    """Find font size that fits text within max_width."""
    size = start_size
    while size > min_size:
        font = get_font(size)
        # Approximate width (PIL 10+ has getbbox, fallback to estimate)
        try:
            bbox = font.getbbox(text)
            w = bbox[2] - bbox[0]
        except:
            w = len(text) * size * 0.6  # rough estimate
        if w <= max_width:
            return font, size
        size -= 4
    return get_font(min_size), min_size

def draw_icon(d, cx, cy, size, icon_type, color):
    """Draw thematic icon."""
    s = size
    if icon_type == "lock":
        # Padlock
        d.rectangle([cx-s//3, cy-s//6, cx+s//3, cy+s//3], outline=color, width=4)
        d.arc([cx-s//3, cy-s//2, cx+s//3, cy+s//6], 180, 360, fill=color, width=4)
    elif icon_type == "chart":
        # Bar chart
        bars = [0.4, 0.7, 0.5, 0.9, 0.6]
        bw = s // 7
        for i, h in enumerate(bars):
            x = cx - s//2 + i * (bw + 4)
            d.rectangle([x, cy+s//3-h*s//2, x+bw, cy+s//3], fill=color)
    elif icon_type == "cloud":
        # Cloud
        d.ellipse([cx-s//2, cy-s//6, cx+s//6, cy+s//3], outline=color, width=3)
        d.ellipse([cx-s//6, cy-s//3, cx+s//2, cy+s//6], outline=color, width=3)
    elif icon_type == "terminal":
        # Terminal >_
        d.rectangle([cx-s//2, cy-s//3, cx+s//2, cy+s//3], outline=color, width=3)
        d.text((cx-10, cy), ">_", font=get_font(28), fill=color, anchor="mm")
    elif icon_type == "server":
        # Server stack
        for i in range(3):
            y = cy - s//2 + i * (s//3)
            d.rectangle([cx-s//3, y, cx+s//3, y+s//4], outline=color, width=2)
            d.ellipse([cx-s//3+5, y+5, cx-s//3+12, y+12], fill=color)
    elif icon_type == "cap":
        # Graduation cap (simplified)
        d.polygon([(cx-s//2, cy), (cx, cy-s//3), (cx+s//2, cy), (cx, cy+s//6)], outline=color, width=3)
        d.line([(cx+s//2, cy), (cx+s//2, cy+s//3)], fill=color, width=2)
    elif icon_type == "shield":
        # Shield
        d.polygon([(cx, cy-s//2), (cx+s//3, cy-s//3), (cx+s//3, cy+s//6),
                   (cx, cy+s//2), (cx-s//3, cy+s//6), (cx-s//3, cy-s//3)],
                  outline=color, width=3)
    elif icon_type == "checklist":
        # Checklist
        d.rectangle([cx-s//3, cy-s//2, cx+s//3, cy+s//2], outline=color, width=3)
        for i in range(3):
            y = cy - s//4 + i * s//4
            d.line([(cx-s//4, y), (cx-s//6, y+8)], fill=color, width=2)
            d.line([(cx-s//6, y+8), (cx, y-8)], fill=color, width=2)
    elif icon_type == "eye":
        # Eye
        d.ellipse([cx-s//2, cy-s//4, cx+s//2, cy+s//4], outline=color, width=3)
        d.ellipse([cx-12, cy-12, cx+12, cy+12], fill=color)

def render_card(project_key, W=720, H=1280, out_path=None):
    """Render a cinematic card video."""
    cfg = PROJECTS[project_key]
    accent = cfg["accent"]
    secondary = cfg["secondary"]

    n_frames = int(FPS * DURATION)
    # Use workspace for temp frames (persistent, /tmp gets cleared)
    frames_dir = os.path.expanduser(f"~/workspace/apex-audit/.work/tiktok-cards/frames_{project_key}_{W}x{H}")
    os.makedirs(frames_dir, exist_ok=True)
    # Clear old
    for f in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, f))

    cx, cy_badge = W // 2, int(H * 0.28)
    badge_r = min(W, H) // 5

    for fi in range(n_frames):
        t = fi / FPS
        progress = fi / n_frames

        img = Image.new("RGB", (W, H), BG_DARK)
        d = ImageDraw.Draw(img)

        # Background HUD
        draw_hud_panels(d, W, H, t)
        draw_particles(d, W, H, t)

        # Phase 1 (0-1s): Particle burst intro
        if t < 1.0:
            burst_p = t / 1.0
            # Expanding ring of particles from center
            for i in range(60):
                ang = (i / 60) * 2 * math.pi
                r = burst_p * 300
                x = cx + r * math.cos(ang)
                y = cy_badge + r * math.sin(ang)
                d.ellipse([x-2, y-2, x+2, y+2], fill=accent)
        # Phase 2+ (1s+): Badge
        else:
            badge_p = min((t - 1.0) / 2.0, 1.0)  # 1-3s: badge forms
            # Scale in
            scale = 0.5 + 0.5 * badge_p
            r = int(badge_r * scale)

            # Hexagon badge (double outline for depth)
            pts = hex_points(cx, cy_badge, r)
            d.polygon(pts, outline=accent, width=4)
            pts2 = hex_points(cx, cy_badge, int(r * 0.85))
            d.polygon(pts2, outline=accent, width=2)

            # Circuit texture (fade in)
            if badge_p > 0.3:
                draw_circuit_texture(d, cx, cy_badge, r, seed=hash(project_key) % 1000)

            # Icon at top of badge
            if badge_p > 0.5:
                draw_icon(d, cx, cy_badge - r//3, 60, cfg["icon"], accent)
                # Project code in badge
                d.text((cx, cy_badge + r//4), cfg["code"],
                       font=get_font(int(48 * scale)), fill=accent, anchor="mm")

            # Rotating text ring (3s+)
            if t > 3.0:
                draw_rotating_ring(d, cx, cy_badge, int(r * 1.35), t - 3.0,
                                   cfg["ring_words"], cfg["ring_colors"])

            # Phase 3 (5s+): Badge moves up slightly, text appears below
            if t > 5.0:
                text_p = min((t - 5.0) / 1.5, 1.0)
                y_base = int(H * 0.52)

                # Project code HUGE
                if text_p > 0.1:
                    draw_glow_text(d, (cx, y_base),
                                   cfg["code"], get_font(110), accent)
                # Partner in secondary color - auto-fit
                if text_p > 0.3:
                    pfont, _ = fit_font_size(cfg["partner"], W - 80, 64, 28)
                    draw_glow_text(d, (cx, y_base + 110),
                                   cfg["partner"], pfont, secondary)
                # Subtitle
                if text_p > 0.5:
                    d.text((cx, y_base + 180), cfg["subtitle"],
                           font=get_font(32), fill=accent, anchor="mm")

            # Phase 4 (7s+): Main title
            if t > 7.0:
                title_p = min((t - 7.0) / 1.5, 1.0)
                y_title = int(H * 0.72)
                max_w = W - 100
                # Title line 1 (accent) - auto-fit
                font1, _ = fit_font_size(cfg["title1"], max_w, 72, 36)
                draw_glow_text(d, (cx, y_title),
                               cfg["title1"], font1, accent)
                # Title line 2 (secondary) - auto-fit
                font2, _ = fit_font_size(cfg["title2"], max_w, 72, 36)
                draw_glow_text(d, (cx, y_title + 85),
                               cfg["title2"], font2, secondary)
                # Corner brackets
                if title_p > 0.5:
                    draw_corner_brackets(d, 40, y_title - 60, W-80, 200, accent)

            # Phase 5 (8.5s+): Branding
            if t > 8.5:
                y_brand = int(H * 0.92)
                d.text((cx, y_brand), "INTERSTITIUM",
                       font=get_font(48), fill=accent, anchor="mm")
                d.text((cx, y_brand + 45), "LABS",
                       font=get_font(32), fill=GRAY, anchor="mm")
                draw_corner_brackets(d, cx-180, y_brand-30, 360, 100, accent, size=15)

        # Glitch effect (occasional)
        if random.random() < 0.05:
            # RGB shift lines
            for _ in range(3):
                y = random.randint(0, H)
                d.line([(0, y), (W, y)], fill=RED, width=2)

        img.save(f"{frames_dir}/f{fi:06d}.png")

    # Encode video
    if out_path is None:
        out_path = f"/tmp/card_renders/{project_key}_{W}x{H}.mp4"

    cmd = ["ffmpeg", "-y", "-framerate", str(FPS),
           "-i", f"{frames_dir}/f%06d.png",
           "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", "23", "-preset", "fast", out_path]
    subprocess.run(cmd, capture_output=True, check=True)

    # Save poster frame (near end, t=9s, all text visible)
    poster_path = out_path.replace(".mp4", "-poster.png")
    poster_frame = f"{frames_dir}/f{int(9*FPS):06d}.png"
    if os.path.exists(poster_frame):
        shutil.copy(poster_frame, poster_path)
    else:
        mid_frame = f"{frames_dir}/f{n_frames//2:06d}.png"
        shutil.copy(mid_frame, poster_path)

    # Cleanup frames
    shutil.rmtree(frames_dir, ignore_errors=True)

    return out_path, poster_path

if __name__ == "__main__":
    import sys
    # Test with il-29
    key = sys.argv[1] if len(sys.argv) > 1 else "il-29"
    W = int(sys.argv[2]) if len(sys.argv) > 2 else 720
    H = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
    out = sys.argv[4] if len(sys.argv) > 4 else None
    mp4, poster = render_card(key, W, H, out)
    print(f"Rendered: {mp4}")
    print(f"Poster: {poster}")
