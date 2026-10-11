#!/usr/bin/env python3
"""REPAIR (2026-10-09): fix misplaced data-topic-theme in hub cards.

The patch script inserted the attribute after the WRONG quote (the regex had
already consumed the href closing quote), producing:
  data-group=" data-topic-theme="<theme>"<group>"
Repair to:
  data-group="<group>" data-topic-theme="<theme>"
"""
import os, re

HUB = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps/index.html")

with open(HUB, encoding="utf-8") as f:
    html = f.read()

corrupt_pat = re.compile(r'data-group=" data-topic-theme="([a-z0-9-]+)"([a-z-]*)"')
found = corrupt_pat.findall(html)
print("corrupted cards found:", len(found))

def fix(m):
    theme, group = m.group(1), m.group(2)
    return 'data-group="%s" data-topic-theme="%s"' % (group, theme)

new_html, n = corrupt_pat.subn(fix, html)
print("repaired:", n)

with open(HUB + ".tmp-repair", "w", encoding="utf-8") as f:
    f.write(new_html)
os.replace(HUB + ".tmp-repair", HUB)

# ---- validate ----
with open(HUB, encoding="utf-8") as f:
    check = f.read()

# 1. no corruption pattern remains
assert not corrupt_pat.search(check), "corruption remains!"

# 2. every hub card has well-formed data-group and data-topic-theme
cards = re.findall(r'<a class="hub-card" href="([^"/]+)/" data-group="([a-z-]+)" data-topic-theme="([a-z0-9-]+)"', check)
print("well-formed themed cards:", len(cards))
assert len(cards) == 75, "expected 75 cards, got %d" % len(cards)

# 3. theme values match content.json (authoritative)
import json
mismatches = []
for slug, group, theme in cards:
    p = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps/%s/content.json" % slug)
    try:
        want = json.load(open(p, encoding="utf-8")).get("topicTheme")
    except Exception:
        want = None
    if want != theme:
        mismatches.append((slug, theme, want))
print("theme mismatches vs content.json:", mismatches)
assert not mismatches

# 4. spot-check tag shape
m = re.search(r'<a class="hub-card" href="python/"[^>]*>', check)
print("sample:", m.group(0)[:120])
print("OK: hub cards repaired and validated")
