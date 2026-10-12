"""Fix stray '),' on plain-string list items inside "procedure" lists in content_embedded_qa.py.
Summary/project/honesty use parenthesized implicit-concat ("key": ("a " "b "),) which is valid;
only list items inside "procedure": [ ... ] get the fix."""
import re

path = "/home/hatch/workspace/apex-audit/retrofit_20261007/il13/content_embedded_qa.py"
lines = open(path).read().split("\n")
out = []
in_proc = False
fixed = 0
for ln in lines:
    s = ln.strip()
    if s.startswith('"procedure"'):
        in_proc = True
    if in_proc and s == "],":
        in_proc = False
    if in_proc and ln.rstrip().endswith('"),'):
        # plain string list item with stray ')':  "..."),
        # distinguish from tuple items which start with (" on the same line
        if not s.startswith('("'):
            ln = ln.rstrip()[:-3] + '",'
            fixed += 1
    out.append(ln)

open(path, "w").write("\n".join(out))
print("fixed lines:", fixed)

import ast
src = "\n".join(out)
ast.parse(src)
d = {}
exec(src, d)
print("modules:", len(d["M"]))
# sanity: every entry has all keys, procedures are lists of str
for mid, e in d["M"].items():
    assert set(e) == {"summary", "concepts", "proc_title", "procedure", "project", "honesty"}, mid
    assert isinstance(e["summary"], str) and e["summary"].startswith("Welcome to"), mid
    assert isinstance(e["procedure"], list) and all(isinstance(x, str) for x in e["procedure"]), mid
    assert isinstance(e["project"], str) and isinstance(e["honesty"], str), mid
    assert e["proc_title"] in ("Hands-on procedure", "Worked estimation"), mid
    for t, df in e["concepts"]:
        assert isinstance(t, str) and isinstance(df, str) and t and df, mid
print("all entries valid")
