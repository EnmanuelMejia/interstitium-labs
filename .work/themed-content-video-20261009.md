# Themed Content Video — Theme Templates Builder (2026-10-09)

Part of the sitewide themed-content rollout (user order 2026-10-09).
Work done in `~/workspace/story-videos/il_anim.py` (programmatic video
animation framework). All visuals are original code — no copied footage.

## What was added

### 1. THEMES dict — 12 new styles (merged into STYLES, so `Scene(title, style="<theme>")` works directly)

| Theme key   | bg          | accent (primary) | secondary        | Look |
|-------------|-------------|------------------|----------------|------|
| mr-robot    | (5,5,5)     | (0,255,65)       | (0,180,40)     | terminal green, scanlines, glitch text |
| cyberpunk   | (13,2,33)   | (255,42,109)     | (5,217,232)    | neon pink / cyan, particles |
| tron        | (0,0,0)     | (0,229,255)      | (0,120,160)    | electric blue perspective grid |
| steampunk   | (26,20,16)  | (176,141,87)     | (135,206,235)  | brass frame w/ rivets, sky-blue rule |
| exmachina   | (10,10,10)  | (245,245,245)    | (120,120,120)  | stark white, thin rule lines, no glow |
| oceandeep   | (0,8,20)    | (57,255,206)     | (0,60,120)     | bioluminescent teal sine-wave field |
| hackers95   | (10,10,10)  | (255,0,255)      | (204,255,0)    | sheared magenta title, lime subtitle |
| alexandria  | (18,16,10)  | (212,175,55)     | (248,245,236)  | gold double-rule frame, marble inner |
| industrial  | (12,8,0)    | (255,176,0)      | (150,90,0)     | amber, hazard-stripe bars, scanlines |
| sacredgeo   | (8,6,4)     | (232,193,90)     | (180,140,60)   | gold diamond-lattice background |
| vaporwave   | (18,0,36)   | (255,113,206)    | (185,103,255)  | sunset gradient + slit sun + grid floor |
| goldrush    | (13,11,0)   | (255,215,0)      | (150,110,0)    | gold glow + floating particles |

### 2. TOPIC_TO_THEME mapping

```python
{"cybersecurity": "mr-robot", "system-design": "cyberpunk",
 "networking": "tron", "cloud-devops": "steampunk", "ai-ml": "exmachina",
 "data-eng": "oceandeep", "programming": "hackers95",
 "databases": "alexandria", "linux-systems": "industrial",
 "math": "sacredgeo", "web-dev": "vaporwave", "blockchain": "goldrush"}
```

### 3. Helper functions (all return the image, so they chain)

- `draw_scanlines(img, theme)` — CRT scanlines + faint accent phosphor tint (used by mr-robot/industrial).
- `draw_grid(img, theme, horizon=0.42)` — perspective grid to a vanishing point (tron/vaporwave).
- `draw_particles(img, theme, n)` — n floating accent-color particles (seeded RNG).
- `themed_title_card(theme_key, title, subtitle="")` — returns a `draw_fn(img, t)` matching the framework's draw contract (mutates img via paste): paints the theme background, renders the title with the theme treatment (glitch / skew / glow / stark rules), adds theme chrome (rivets, hazard bars, double frames, cyan underline), applies scanline overlays, then subtitle + "Interstitium Labs" footer.
- Internals: `_glow_text` (Gaussian-blur halo), `_glitch_title` (RGB-split ghosts + slice rects), `_skewed_title` (affine shear), `_hazard_bar`, `_paint_waves`, `_paint_diamonds`, `_paint_sunset`, `_dim`.

Also added `ImageFilter` to the PIL import line. Existing styles (bbg/3b1b/fireship/primer/story) untouched.

## Validation (2026-10-09 ~02:20 EDT)

- `python3 -c "import il_anim; print(il_anim.TOPIC_TO_THEME)"` — prints the full mapping (verified output matches spec exactly).
- Rendered one test frame per theme to `/tmp/theme_<key>.png` via `Scene.blank()` + `themed_title_card(key, ...)` at t=0.5, plus direct calls to `draw_scanlines`, `draw_grid`, `draw_particles` per theme, plus a bbg regression frame — **13/13 passed, zero crashes**.
- Visual spot-check: mr-robot frame shows green glitch title with red/cyan RGB-split ghosts, scanlines, green subtitle; vaporwave frame shows pink→purple→dark gradient, slit sun, perspective grid floor, glowing pink title. Both confirmed on-screen.
- Test script (ephemeral): `/tmp/validate_themes.py`.

## Usage example for future builders

```python
import sys
sys.path.insert(0, "/home/hatch/workspace/story-videos")
from il_anim import Scene, TOPIC_TO_THEME, themed_title_card, render_scene

topic = "cybersecurity"
theme = TOPIC_TO_THEME[topic]            # -> "mr-robot"

scene = Scene("Zero Trust Architecture", style=theme)
scene.add_step(themed_title_card(theme, "Zero Trust", "Never trust, always verify"),
               "Intro card", "Welcome to the zero trust module.")
# ... add content steps with draw_box/draw_arrow in theme colors ...
render_scene(scene, "/tmp/zero-trust-intro.mp4")
```

Notes:
- `Scene(title, style=theme)` picks up bg/accent automatically; use `scene.cfg["secondary"]` for two-tone diagrams.
- `themed_title_card` is a drop-in `add_step` draw_fn (signature `(img, t)`).
- `draw_scanlines/draw_grid/draw_particles` can be layered onto any step's draw_fn for texture.
- TTS is down — render previews with `render_scene` and the `-script.txt` narration file as before; narration stays manual until TTS returns.
