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
import sys
from pathlib import Path
dest = Path(sys.argv[1])
index = dest / "index.html"
if not index.exists():
    raise SystemExit("www/index.html missing after sync")
text = index.read_text(encoding="utf-8")
if "/assets/il-bridge.js" not in text:
    snippet = '<script src="/assets/il-bridge.js" defer></script>\n'
    if "</body>" in text:
        text = text.replace("</body>", snippet + "</body>", 1)
    else:
        text += "\n" + snippet
    index.write_text(text, encoding="utf-8")
    print("injected bridge into www/index.html")
print("synced", dest, "ok")
PY

cat > "$DEST/IL-BUNDLE-NOTE.txt" << 'NOTE'
Interstitium Labs mobile www bundle
Source: docs/ | Trust: https://interstitiumlabs.dev
Secrets: none. See docs/ops/ENTERPRISE-SECURITY.md + MOBILE-SECURITY.md
NOTE

echo "sync-mobile-web: done → $DEST"
