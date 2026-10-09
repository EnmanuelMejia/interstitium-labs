#!/bin/bash
# Track 7 redirect chain tracer: follows hops manually, prints full chain.
# Usage: trace.sh <url> [label]
trace() {
  local url="$1" label="$2" max=6 hop=0
  echo "== ${label:-$url}"
  while [ $hop -lt $max ]; do
    local out code loc
    out=$(curl -s -o /dev/null -D - --max-time 25 -w $'\n%{http_code}\n%{redirect_url}\n' "$url")
    # after cmdsubst+echo the last two lines are: <code>, <redirect_url>
    code=$(echo "$out" | tail -2 | head -1 | tr -d '\r')
    loc=$(echo "$out" | tail -1 | tr -d '\r')
    hop=$((hop+1))
    echo "  hop $hop: [$code] $url"
    if [ -z "$loc" ]; then
      echo "  FINAL: $code (no redirect)"
      return
    fi
    # resolve relative location
    case "$loc" in
      http*://*) url="$loc" ;;
      /*) base=$(echo "$url" | sed -E 's|(https?://[^/]+).*|\1|'); url="${base}${loc}" ;;
      *) base=$(echo "$url" | sed -E 's|(https?://[^/]+).*|\1|'); url="${base}/${loc}" ;;
    esac
  done
  echo "  FINAL: chain exceeded $max hops (LOOP?)"
}
while IFS=$'\t' read -r url label; do
  [ -z "$url" ] && continue
  trace "$url" "$label"
  echo
done < "$1"
