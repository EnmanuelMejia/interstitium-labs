Brand icon/splash masters and generation.

Source of truth: `docs/assets/chrome/sigil-glyph.svg` — the glyph-only Interstitium
sigil (no wordmark; the `icon-512.png` / `icon-maskable-512.png` lockups bake the
wordmark in and do not survive launcher sizes).

Regenerate all densities with (from repo root):

    python3 apps/mobile/scripts/gen-brand-assets.py

which writes Android mipmap icons (legacy + round + adaptive foreground on the
void `#070B16` background), the `drawable-*/splash.png` set, the iOS
`AppIcon.appiconset` (1024 + dark + tinted variants), and the iOS
`Splash.imageset`. `npx capacitor-assets` remains optional and is not required.

Background: #070B16.
