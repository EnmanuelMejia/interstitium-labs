#!/usr/bin/env python3
"""Themed-content rollout (2026-10-09): inject data-topic-theme into static hub cards.

Reads the authoritative topicTheme from each bootcamp's content.json and adds
data-topic-theme="..." to every <a class="hub-card" href="SLUG/" ...> in
site/bootcamps/index.html. Idempotent: skips cards that already carry the attribute.
"""
import json, os, re

BOOT_DIR = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
HUB = os.path.join(BOOT_DIR, "index.html")

def main():
    themes = {}
    for d in sorted(os.listdir(BOOT_DIR)):
        p = os.path.join(BOOT_DIR, d, "content.json")
        if os.path.isfile(p):
            data = json.load(open(p, encoding="utf-8"))
            if data.get("topicTheme"):
                themes[d] = data["topicTheme"]
    print("themes known for %d bootcamps" % len(themes))

    with open(HUB, encoding="utf-8") as f:
        html = f.read()

    pat = re.compile(r'<a class="hub-card" href="([^"/]+)/"')
    out, last = [], 0
    added, skipped, unknown = 0, 0, []
    for m in pat.finditer(html):
        tag_end = html.find(">", m.start())
        tag = html[m.start():tag_end]
        if "data-topic-theme" in tag:
            skipped += 1
            continue
        slug = m.group(1)
        th = themes.get(slug)
        if th is None:
            unknown.append(slug)
            continue
        # m.end() sits right before the closing quote of the href value;
        # insert the attribute AFTER that quote.
        qpos = html.find('"', m.end())
        assert qpos > 0 and qpos < tag_end, "href quote not found for " + slug
        out.append(html[last:qpos + 1])
        out.append(' data-topic-theme="%s"' % th)
        last = qpos + 1
        added += 1
    out.append(html[last:])
    new_html = "".join(out)

    with open(HUB + ".tmp-theme", "w", encoding="utf-8") as f:
        f.write(new_html)
    os.replace(HUB + ".tmp-theme", HUB)

    with open(HUB, encoding="utf-8") as f:
        check = f.read()
    total_cards = len(pat.findall(check))
    themed = len(re.findall(r'<a class="hub-card"[^>]*data-topic-theme="[a-z0-9-]+"', check))
    print("added=%d skipped(already themed)=%d unknown_slugs=%s" % (added, skipped, sorted(set(unknown))))
    print("cards total=%d themed=%d" % (total_cards, themed))
    assert total_cards == themed, "not all hub cards themed!"
    print("OK: all hub cards carry data-topic-theme")

if __name__ == "__main__":
    main()
