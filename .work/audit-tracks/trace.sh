#!/bin/bash
# Track 7 redirect chain tracer (v3): marker-based parse, retry on 000, loop detect.
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
trace() {
  local url="$1" label="$2" max=6 hop=0 seen=""
  echo "== ${label:-$url}"
  while [ $hop -lt $max ]; do
    local marker code loc attempt=0
    while [ $attempt -lt 3 ]; do
      marker=$(curl -s -o /dev/null -A "$UA" --connect-timeout 12 --max-time 45 \
        -w $'\n###%{http_code}###%{redirect_url}###\n' "$url" 2>/dev/null | grep -a '^###' | tail -1)
      code=$(printf '%s' "$marker" | sed -E 's/^###([0-9]*)###.*$/\1/')
      if [ -n "$code" ] && [ "$code" != "000" ]; then break; fi
      attempt=$((attempt+1)); sleep 2
    done
    loc=$(printf '%s' "$marker" | sed -E 's/^###[0-9]*###(.*)###$/\1/')
    hop=$((hop+1))
    if [ -z "$code" ] || [ "$code" = "000" ]; then
      echo "  hop $hop: [TIMEOUT/000 after 3 tries] $url -- couldn't-check beyond here"
      return
    fi
    if [ -z "$loc" ]; then
      echo "  hop $hop: [$code] $url"
      echo "  FINAL: $code $url"
      return
    fi
    echo "  hop $hop: [$code] $url -> $loc"
    case "$loc" in
      http*://*) url="$loc" ;;
      /*) base=$(printf '%s' "$url" | sed -E 's|(https?://[^/]+).*|\1|'); url="${base}${loc}" ;;
      *) base=$(printf '%s' "$url" | sed -E 's|(https?://[^/]+).*|\1|'); url="${base}/${loc}" ;;
    esac
    case "$seen" in
      *"|$url|"*) echo "  LOOP DETECTED: $url already visited"; return ;;
    esac
    seen="${seen}|$url|"
  done
  echo "  FINAL: chain exceeded $max hops (possible loop) -- last: $url"
}
while IFS=$'\t' read -r url label; do
  [ -z "$url" ] && continue
  trace "$url" "$label"
  echo
done < "$1"
