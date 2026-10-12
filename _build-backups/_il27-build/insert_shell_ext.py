"""Insert IL-27 shell extension into course-shell.js + boot() tab registration."""
import json

SHELL = "/home/hatch/workspace/apex-audit/docs/university/course-shell.js"
EXT = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il27-build/il27_shell_ext.js"

with open(SHELL) as f:
    lines = f.readlines()

# --- guard: not already inserted ---
blob = "".join(lines)
assert "isIL27()" not in blob or blob.count("function isIL27()") == 0, "extension already present"

# --- 1) boot() tab registration, right after the crosswalk TABS.push block ---
anchor = None
for i, ln in enumerate(lines):
    if "TABS.push({ id: 'crosswalk', num: '07', label: 'Crosswalk' });" in ln:
        anchor = i
        break
assert anchor is not None, "crosswalk TABS.push anchor not found"

tab_block = [
    "    /* IL-27: Fast Track + Objectives tabs (course-scoped; other courses unaffected) */\n",
    "    if (typeof isIL27 === 'function' && isIL27()) {\n",
    "      if (COURSE.fastTrack && !TABS.some(function (t) { return t.id === 'fasttrack'; })) {\n",
    "        TABS.push({ id: 'fasttrack', num: '08', label: 'Fast Track' });\n",
    "      }\n",
    "      if (!TABS.some(function (t) { return t.id === 'objectives'; })) {\n",
    "        TABS.push({ id: 'objectives', num: '09', label: 'Objectives' });\n",
    "      }\n",
    "    }\n",
]
lines[anchor + 1:anchor + 1] = tab_block

# --- 2) append extension body before the final })(); ---
ext = open(EXT).read()
# find the final IIFE close: last line that is exactly })(); (no indent)
close_idx = None
for i in range(len(lines) - 1, -1, -1):
    if lines[i].strip() == "})();":
        close_idx = i
        break
assert close_idx is not None, "IIFE close not found"

new_lines = lines[:close_idx] + ["\n", ext, "\n"] + lines[close_idx:]
with open(SHELL, "w") as f:
    f.writelines(new_lines)

print("inserted extension (%d bytes) at line %d; total lines now %d" % (len(ext), close_idx + 1, len(new_lines)))
