#!/usr/bin/env python3
"""
Batch render all cinematic cards.
- 9:16 vertical (720x1280) for TikTok
- 16:9 horizontal (1280x720) for web embeds
- LinkedIn PNG (1200x627) static
"""
import os, sys, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cinematic_card_gen import render_card, PROJECTS, BG_DARK
from PIL import Image, ImageDraw

OUTPUT_DIR = os.path.expanduser("~/workspace/apex-audit/docs/assets/cards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_linkedin_png(project_key):
    """Generate 1200x627 LinkedIn static card from poster."""
    from cinematic_card_gen import get_font, draw_glow_text, CYAN, WHITE, GRAY
    cfg = PROJECTS[project_key]
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), BG_DARK)
    d = ImageDraw.Draw(img)
    
    # Simplified layout for LinkedIn: badge left, text right
    # Draw hexagon badge on left
    import math
    cx, cy = 280, H // 2
    r = 160
    pts = [(cx + r * math.cos(i * math.pi / 3),
            cy + r * math.sin(i * math.pi / 3)) for i in range(6)]
    d.polygon(pts, outline=cfg["accent"], width=4)
    
    # Icon and code in badge
    from cinematic_card_gen import draw_icon
    draw_icon(d, cx, cy - 30, 70, cfg["icon"], cfg["accent"])
    d.text((cx, cy + 60), cfg["code"], font=get_font(52), fill=cfg["accent"], anchor="mm")
    
    # Text on right
    tx = 520
    d.text((tx, 140), cfg["code"], font=get_font(72), fill=cfg["accent"], anchor="lm")
    d.text((tx, 230), cfg["partner"], font=get_font(48), fill=cfg["secondary"], anchor="lm")
    d.text((tx, 300), cfg["subtitle"], font=get_font(28), fill=cfg["accent"], anchor="lm")
    d.text((tx, 380), cfg["title1"], font=get_font(56), fill=cfg["accent"], anchor="lm")
    d.text((tx, 450), cfg["title2"], font=get_font(56), fill=cfg["secondary"], anchor="lm")
    d.text((tx, 540), "INTERSTITIUM LABS", font=get_font(32), fill=GRAY, anchor="lm")
    
    out = f"{OUTPUT_DIR}/{project_key}_linkedin_1200x627.png"
    img.save(out)
    return out

def main():
    projects = list(PROJECTS.keys())
    print(f"Rendering {len(projects)} projects...")
    
    for i, key in enumerate(projects, 1):
        print(f"\n[{i}/{len(projects)}] {key}")
        
        # 9:16 vertical
        out_916 = f"{OUTPUT_DIR}/{key}_9x16.mp4"
        if not os.path.exists(out_916):
            print(f"  Rendering 9:16...")
            mp4, poster = render_card(key, 720, 1280, out_916)
            print(f"  Done: {mp4}")
        else:
            print(f"  9:16 exists, skipping")
        
        # 16:9 horizontal
        out_169 = f"{OUTPUT_DIR}/{key}_16x9.mp4"
        if not os.path.exists(out_169):
            print(f"  Rendering 16:9...")
            mp4, poster = render_card(key, 1280, 720, out_169)
            print(f"  Done: {mp4}")
        else:
            print(f"  16:9 exists, skipping")
        
        # LinkedIn PNG
        out_li = f"{OUTPUT_DIR}/{key}_linkedin_1200x627.png"
        if not os.path.exists(out_li):
            print(f"  Generating LinkedIn PNG...")
            png = make_linkedin_png(key)
            print(f"  Done: {png}")
        else:
            print(f"  LinkedIn PNG exists, skipping")
    
    print("\n=== All renders complete ===")
    # List outputs
    for f in sorted(os.listdir(OUTPUT_DIR)):
        fp = os.path.join(OUTPUT_DIR, f)
        sz = os.path.getsize(fp)
        print(f"  {f} ({sz:,} bytes)")

if __name__ == "__main__":
    main()
