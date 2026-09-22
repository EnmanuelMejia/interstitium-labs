#!/usr/bin/env bash
# Local + CI secret/pattern gate for Interstitium Labs.
# Fails on private-key material, common API secret shapes, and tracker leftovers.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAIL=0
SCAN_DIRS=(docs apps/mobile/src apps/mobile/android-security apps/mobile/ios-security scripts .github)

echo "== Interstitium Labs security-check =="

exclude_args=(
  --exclude-dir=node_modules
  --exclude-dir=.git
  --exclude-dir=www
  --exclude-dir=dist
  --exclude-dir=_imports
  --exclude-dir=deploy-shots
  --exclude=package-lock.json
  --exclude='*.png'
  --exclude='*.jpg'
  --exclude='*.webp'
  --exclude='*.woff*'
)

scan() {
  local label="$1"
  local pattern="$2"
  local hits
  hits="$(grep -RInE "$pattern" "${SCAN_DIRS[@]}" "${exclude_args[@]}" 2>/dev/null || true)"
  if [[ -n "$hits" ]]; then
    local filtered
    filtered="$(printf '%s\n' "$hits" | grep -vE 'docs/ops/|MOBILE-SECURITY|ENTERPRISE-SECURITY|STORE-PUBLISH|payments\.md|admin\.md|_worker_security|security-check\.sh|ANALYTICS\.md|\.gitignore|CODEOWNERS' || true)"
    if [[ -n "$filtered" ]]; then
      echo "FAIL [$label]:"
      printf '%s\n' "$filtered" | head -40
      FAIL=1
    else
      echo "OK   [$label] (docs-only mentions)"
    fi
  else
    echo "OK   [$label]"
  fi
}

scan "PEM/OpenSSH private keys" 'BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY'
scan "PKCS8 / generic PRIVATE KEY" 'BEGIN PRIVATE KEY'
scan "Stripe secret keys" 'sk_(live|test)_[A-Za-z0-9]{10,}'
scan "AWS access key id" 'AKIA[0-9A-Z]{16}'
scan "Google API key shape" 'AIza[0-9A-Za-z_-]{20,}'
scan "Slack bot token" 'xox[baprs]-[0-9A-Za-z-]{10,}'
scan "GitHub PAT" 'gh[pousr]_[A-Za-z0-9]{20,}'
scan "Grok App / grok tracker leftovers" 'grok-project-id|grok:app_id|/__grok|"Grok App"|grok-preview-bridge|__grokPreviewBridgeRoot|grok\.com'
scan "Third-party trackers (GA/Meta/Hotjar)" 'googletagmanager\.com|google-analytics\.com/analytics|connect\.facebook\.net|static\.hotjar\.com'

while IFS= read -r -d '' f; do
  echo "FAIL [key material file present]: $f"
  FAIL=1
done < <(find docs apps scripts .github -type f \( \
  -name '*.pem' -o -name '*.p8' -o -name '*.jks' -o -name '*.keystore' \
  -o -name 'google-services.json' -o -name 'GoogleService-Info.plist' \
  -o -name '.env' -o -name '.env.*' \
\) ! -path '*/node_modules/*' ! -name '.env.example' -print0 2>/dev/null)

if grep -E 'sk_(live|test)_' docs/enroll/config.js docs/analytics/config.js 2>/dev/null; then
  echo "FAIL [config secrets in enroll/analytics]"
  FAIL=1
else
  echo "OK   [enroll/analytics config — no sk_ secrets]"
fi

if grep -qiE 'Grok App|grok-project' docs/manifest.webmanifest docs/brand/manifest.webmanifest 2>/dev/null; then
  echo "FAIL [manifest Grok leftovers]"
  FAIL=1
else
  echo "OK   [manifest branding]"
fi

if [[ "$FAIL" -ne 0 ]]; then
  echo "== security-check FAILED =="
  exit 1
fi
echo "== security-check PASSED =="
