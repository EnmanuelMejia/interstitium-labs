#!/usr/bin/env python3
"""Rebuild docs/_worker.bundle.js from payment-routes.js + _worker.js.

Recipe (per AGENTS.md): bundle = "// payment-routes.js" + payment-routes.js
+ blank + "// _worker.js" + blank + _worker.js with the leading /** */ header
block (lines 1-49) and the `import { handlePay }` line stripped.
Concatenated module scope: payment-routes.js keeps its export {} block,
_worker.js keeps export default + its export {} block. No hand edits.
"""
import re
import subprocess
import sys

ROOT = "/home/hatch/workspace/apex-audit/docs"

pay = open(f"{ROOT}/payment-routes.js", encoding="utf-8").read()
worker = open(f"{ROOT}/_worker.js", encoding="utf-8").read().splitlines(keepends=True)

# Strip leading /** ... */ header block (must start at line 1).
assert worker[0].rstrip() == "/**", f"unexpected first line: {worker[0]!r}"
end = next(i for i, ln in enumerate(worker) if ln.strip() == "*/")
stripped = worker[end + 1 :]

# Strip the `import { handlePay } from "./payment-routes.js";` line.
import_re = re.compile(r'^import\s*\{\s*handlePay\s*\}\s*from\s*["\']\./payment-routes\.js["\'];?\s*$')
before = len(stripped)
stripped = [ln for ln in stripped if not import_re.match(ln.rstrip("\n"))]
removed = before - len(stripped)
assert removed == 1, f"expected to strip exactly 1 import line, stripped {removed}"
# Drop leading blank lines so the bundle matches the canonical shape:
# "// _worker.js" + blank + "var NOINDEX_PREFIXES ..."
while stripped and stripped[0].strip() == "":
    stripped.pop(0)
assert stripped[0].startswith("var NOINDEX_PREFIXES"), f"unexpected: {stripped[0]!r}"

bundle = "// payment-routes.js\n" + pay
if not bundle.endswith("\n"):
    bundle += "\n"
bundle += "\n// _worker.js\n" + "".join(stripped)

out = f"{ROOT}/_worker.bundle.js"
with open(out, "w", encoding="utf-8") as f:
    f.write(bundle)

r = subprocess.run(["node", "--check", out], capture_output=True, text=True)
print(f"bundle written: {out} ({len(bundle.splitlines())} lines)")
print("node --check:", "OK" if r.returncode == 0 else f"FAILED\n{r.stderr}")
sys.exit(r.returncode)
