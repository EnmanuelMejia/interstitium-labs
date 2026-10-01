#!/usr/bin/env bash
# Sync docs/ Learning OS → apps/mobile/www for Capacitor bundling.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/docs"
DEST="$ROOT/apps/mobile/www"

if [[ ! -d "$SRC" ]]; then
  echo "error: docs/ not found at $SRC" >&2
  exit 1
fi

rm -rf "$DEST"
mkdir -p "$DEST"

if command -v rsync >/dev/null 2>&1; then
  rsync -a \
    --exclude '_imports/' \
    --exclude '.DS_Store' \
    --exclude 'analytics/' \
    "$SRC/" "$DEST/"
else
  # Portable fallback (no rsync on minimal boxes)
  cp -a "$SRC"/. "$DEST"/
  rm -rf "$DEST/_imports" "$DEST/analytics"
  find "$DEST" -name '.DS_Store' -delete 2>/dev/null || true
fi

if [[ -f "$ROOT/apps/mobile/src/il-bridge.js" ]]; then
  mkdir -p "$DEST/assets"
  cp "$ROOT/apps/mobile/src/il-bridge.js" "$DEST/assets/il-bridge.js"
fi

python3 - "$DEST" <<'PY'
import shutil
import sys
from pathlib import Path
dest = Path(sys.argv[1])
coach_index = dest / "coach" / "index.html"
index = dest / "index.html"
if not index.exists():
    raise SystemExit("www/index.html missing after sync")
# Cold start is a SINGLE page load: the native shell opens webDir root, so the
# Lab Muse entry (coach) is served directly at / instead of loading the home
# page and then redirecting. All coach asset/link URLs are absolute, so the
# page is path-independent. Falls back to the plain home page if coach is ever
# absent. Web PWA behavior is untouched: it is served from docs/, not www/.
if coach_index.exists():
    shutil.copyfile(coach_index, index)
    print("served coach entry at www/ root (single-load cold start)")
else:
    print("warning: coach/index.html absent — www/ root keeps the home page", file=sys.stderr)
snippet = '<script src="/assets/il-bridge.js" defer></script>\n'
targets = [index, coach_index]
for path in targets:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    if "/assets/il-bridge.js" not in text:
        if "</body>" in text:
            text = text.replace("</body>", snippet + "</body>", 1)
        else:
            text += "\n" + snippet
        path.write_text(text, encoding="utf-8")
        print("injected bridge into", path.relative_to(dest))
print("synced", dest, "ok — Capacitor default home: Lab Muse /coach/ served at www/ root")
PY

cat > "$DEST/IL-BUNDLE-NOTE.txt" << 'NOTE'
Interstitium Labs mobile www bundle
Source: docs/ | Trust: https://interstitiumlabs.dev
Default native launch: Lab Muse companion — the coach entry is served directly at
www/ root (single page load; no redirect). il-bridge.js keeps the / -> /coach/
redirect only as a fallback for older bundles.
Secrets: none. See docs/ops/ENTERPRISE-SECURITY.md + MOBILE-SECURITY.md
NOTE

echo "sync-mobile-web: done → $DEST"
