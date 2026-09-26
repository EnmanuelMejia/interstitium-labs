#!/usr/bin/env bash
# Launch smoke test for the Android build, run against a booted emulator or a
# connected device. Installs the APK, then checks that the app is still
# running after a cold start, a background/foreground cycle and an
# https://interstitiumlabs.dev link, with a screenshot at each step. Fails on
# a crash or ANR in the app's own process. Screenshots and logcat go to OUT.
#
#   scripts/launch-check-android.sh <app-debug.apk> [out-dir]
set -euo pipefail

APK="${1:?usage: launch-check-android.sh <app-debug.apk> [out-dir]}"
OUT="${2:-launch-android}"
PKG="dev.interstitiumlabs.app"
mkdir -p "$OUT"

running() { adb shell pidof "$PKG" > /dev/null 2>&1; }
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
running || fail "app is not running 25 s after a cold start"
shot 1-cold-start

adb shell input keyevent KEYCODE_HOME
sleep 3
adb shell am start -W -n "$PKG/.MainActivity"
sleep 6
running || fail "app did not survive a background/foreground cycle"
shot 2-resumed

adb shell am start -W -a android.intent.action.VIEW \
  -d "https://interstitiumlabs.dev/founders/" -p "$PKG"
sleep 8
running || fail "app did not survive opening an interstitiumlabs.dev link"
shot 3-link-opened

adb logcat -d > "$OUT/logcat.txt"
# A crash is logged as "FATAL EXCEPTION" followed by "Process: <package>".
if grep -A2 "FATAL EXCEPTION" "$OUT/logcat.txt" | grep -q "Process: $PKG"; then
  fail "the app crashed (see logcat.txt)"
fi
if grep -q "ANR in $PKG" "$OUT/logcat.txt"; then
  fail "the app stopped responding (see logcat.txt)"
fi

echo "--- Capacitor and web console output"
grep -E " Capacitor(/Console)?[ :]" "$OUT/logcat.txt" | tail -n 80 || true
echo "launch check passed"
