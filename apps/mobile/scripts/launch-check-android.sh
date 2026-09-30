#!/usr/bin/env bash
# Launch smoke test for the Android build, run against a booted emulator or a
# connected device. Installs the APK, then checks that the same app process
# is still running after a cold start, a background/foreground cycle and an
# https://interstitiumlabs.dev link, with a screenshot at each step. A new
# process ID means the app died and was restarted, which fails the check, as
# does a crash or ANR logged for the app. Screenshots and logcat go to OUT.
#
#   scripts/launch-check-android.sh <app-debug.apk> [out-dir]
set -euo pipefail

APK="${1:?usage: launch-check-android.sh <app-debug.apk> [out-dir]}"
OUT="${2:-launch-android}"
PKG="dev.interstitiumlabs.app"
mkdir -p "$OUT"

pid_of_app() { adb shell pidof "$PKG" 2> /dev/null | tr -d '\r' || true; }
shot() {
  adb exec-out screencap -p > "$OUT/$1.png"
  echo "screenshot $1: $(wc -c < "$OUT/$1.png") bytes"
}
fail() {
  echo "::error::$*"
  adb logcat -d > "$OUT/logcat.txt" 2> /dev/null || true
  exit 1
}

adb install -r "$APK"
adb logcat -c

adb shell am start -W -n "$PKG/.MainActivity"
sleep 25
pid="$(pid_of_app)"
[ -n "$pid" ] || fail "app is not running 25 s after a cold start"
echo "app process: $pid"
shot 1-cold-start

# am start brings a running app to the front, but it would also quietly
# start a new process if the app had died, so the PID must not change.
same_process() {
  local now
  now="$(pid_of_app)"
  [ "$now" = "$pid" ] || fail "$1 (process was $pid, now ${now:-gone})"
}

adb shell input keyevent KEYCODE_HOME
sleep 3
adb shell am start -W -n "$PKG/.MainActivity"
sleep 6
same_process "app did not survive a background/foreground cycle"
shot 2-resumed

adb shell am start -W -a android.intent.action.VIEW \
  -d "https://interstitiumlabs.dev/founders/" -p "$PKG"
sleep 8
same_process "app did not survive opening an interstitiumlabs.dev link"
shot 3-link-opened

adb logcat -d > "$OUT/logcat.txt"
# A Java crash is logged as "FATAL EXCEPTION" with "Process: <package>" on
# one of the next two lines. awk reads the whole file, so nothing is cut
# short the way grep -q in a pipeline can be.
if awk -v pkg="Process: $PKG" '/FATAL EXCEPTION/ { at = NR } at && NR <= at + 2 && index($0, pkg) { hit = 1 } END { exit !hit }' "$OUT/logcat.txt"; then
  fail "the app crashed (see logcat.txt)"
fi
if awk -v anr="ANR in $PKG" 'index($0, anr) { hit = 1 } END { exit !hit }' "$OUT/logcat.txt"; then
  fail "the app stopped responding (see logcat.txt)"
fi

echo "--- Capacitor and web console output"
grep -E " Capacitor(/Console)?[ :]" "$OUT/logcat.txt" | tail -n 80 || true
echo "launch check passed"
