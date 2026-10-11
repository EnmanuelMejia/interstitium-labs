#!/usr/bin/env python3
"""Rebuild docs/_worker.bundle.js per AGENTS.md recipe.
Bundle = '// payment-routes.js' + payment-routes.js
       + '\n// _worker.js' + _worker.js with leading /** */ header block
         and the `import { handlePay }` line stripped (concatenated scope).
"""
import re
import subprocess
import sys

DOCS = "/home/hatch/workspace/apex-audit/docs"

pay = open(f"{DOCS}/payment-routes.js").read()
worker = open(f"{DOCS}/_worker.js").read()

# Strip leading /** ... */ header block from _worker.js
worker = re.sub(r"\A\s*/\*.*?\*/\s*", "", worker, flags=re.DOTALL)
# Strip the import line (handlePay is defined by the concatenated payment-routes scope)
worker = re.sub(r'^\s*import\s+\{\s*handlePay\s*\}\s+from\s+["\']\./payment-routes\.js["\'];\s*$',
                "", worker, flags=re.MULTILINE)

bundle = "// payment-routes.js\n" + pay + "\n// _worker.js\n" + worker

out = f"{DOCS}/_worker.bundle.js"
with open(out, "w") as f:
    f.write(bundle)

r = subprocess.run(["node", "--check", out], capture_output=True, text=True)
if r.returncode != 0:
    print("node --check FAILED:")
    print(r.stderr)
    sys.exit(1)
print(f"OK: wrote {out} ({len(bundle)} bytes), node --check passed")
