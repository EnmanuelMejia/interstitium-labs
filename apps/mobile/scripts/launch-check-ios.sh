#!/usr/bin/env bash
# Launch smoke test for the iOS build on the newest available iPhone
# simulator. Installs the .app, then checks that the same app process is
# still running after a cold start and after going to the background and
# coming back (the scene lifecycle Capacitor 8.5 moved to), with a screenshot
# at each step. A new process ID means the app died and was relaunched, which
# fails the check, as does a new crash report. Screenshots and the app's
# console output (Capacitor's log lines) go to OUT.
#
#   scripts/launch-check-ios.sh <path/to/App.app> [out-dir]
set -euo pipefail

APP="${1:?usage: launch-check-ios.sh <App.app> [out-dir]}"
OUT="${2:-launch-ios}"
BUNDLE="dev.interstitiumlabs.app"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"

udid="$(xcrun simctl list devices available -j | python3 -c '
import json, re, sys
best = None
for runtime, devices in json.load(sys.stdin)["devices"].items():
    m = re.search(r"iOS-(\d+)-(\d+)", runtime)
    if not m:
        continue
    version = (int(m.group(1)), int(m.group(2)))
    for d in devices:
        if d.get("isAvailable") and d["name"].startswith("iPhone"):
            if best is None or version > best[0]:
                best = (version, d["udid"], d["name"])
if best is None:
    sys.exit("no available iPhone simulator")
print(f"simulator: {best[2]}, iOS {best[0][0]}.{best[0][1]}", file=sys.stderr)
print(best[1])
')"
xcrun simctl boot "$udid" 2> /dev/null || true
xcrun simctl bootstatus "$udid" -b > /dev/null

pid_of_app() {
  xcrun simctl spawn "$udid" launchctl list |
    awk -v label="UIKitApplication:$BUNDLE" 'index($3, label) == 1 && $1 ~ /^[0-9]+$/ { print $1 }'
}
shot() {
  xcrun simctl io "$udid" screenshot "$OUT/$1.png" > /dev/null 2>&1
  echo "screenshot $1: $(wc -c < "$OUT/$1.png") bytes"
}
crash_reports() { ls "$HOME"/Library/Logs/DiagnosticReports/App[-_.]*.ips 2> /dev/null || true; }
fail() {
  echo "::error::$*"
  exit 1
}

before="$(crash_reports)"
xcrun simctl install "$udid" "$APP"
# Swift's print() is block-buffered when stdout is a file; NSUnbufferedIO
# makes Capacitor's log lines reach the file as they are written.
SIMCTL_CHILD_NSUnbufferedIO=YES xcrun simctl launch \
  --stdout="$OUT/app-stdout.txt" --stderr="$OUT/app-stderr.txt" "$udid" "$BUNDLE"
sleep 25
pid="$(pid_of_app)"
[ -n "$pid" ] || fail "app is not running 25 s after a cold start"
echo "app process: $pid"
shot 1-cold-start

# Background the app by opening Settings, then bring it back. simctl launch
# would also start a fresh process if the app had died, so the PID must not
# change.
xcrun simctl launch "$udid" com.apple.Preferences > /dev/null
sleep 4
xcrun simctl launch "$udid" "$BUNDLE" > /dev/null || true
sleep 6
now="$(pid_of_app)"
[ "$now" = "$pid" ] || fail "app did not survive a background/foreground cycle (process was $pid, now ${now:-gone})"
shot 2-resumed

if [ "$(crash_reports)" != "$before" ]; then
  crash_reports
  fail "the app left a crash report"
fi

echo "--- Capacitor and web console output"
grep -h -F "⚡️" "$OUT/app-stdout.txt" "$OUT/app-stderr.txt" 2> /dev/null | tail -n 80 || true
echo "launch check passed"
