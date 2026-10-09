#!/bin/bash
# Batch B7 full render: one file per invocation, timeout 300s guard each.
cd /home/hatch/workspace/apex-audit/.work || exit 1
mkdir -p b7-logs
mapfile -t FILES < /tmp/b7_files.txt
ok=0; fail=0; tmo=0
for f in "${FILES[@]}"; do
  [ -z "$f" ] && continue
  timeout 300 python3 gen_bootcamp_b7.py "$f" > "b7-logs/$f.log" 2>&1
  rc=$?
  if [ $rc -eq 0 ]; then ok=$((ok+1)); echo "OK $f"
  elif [ $rc -eq 124 ]; then tmo=$((tmo+1)); echo "TIMEOUT $f"
  else fail=$((fail+1)); echo "FAIL $f (exit $rc)"
  fi
done
echo "RESULT ok=$ok fail=$fail timeout=$tmo total=${#FILES[@]}"
