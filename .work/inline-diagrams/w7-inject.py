#!/usr/bin/env python3
"""W7: inject CSS-only animation into legacy static SVGs (non-destructive)."""
import re
import shutil
import sys
import xml.etree.ElementTree as ET

LIST = "/home/hatch/workspace/apex-audit/.work/inline-diagrams/w6-static-remaining.txt"


def style_block():
    lines = []
    lines.append("<style>")
    lines.append(
        "@keyframes il-pop{from{opacity:0;transform:scale(.85);transform-origin:center;transform-box:fill-box}"
        "to{opacity:1;transform:scale(1);transform-origin:center;transform-box:fill-box}}"
    )
    lines.append("@keyframes il-dash{to{stroke-dashoffset:-24}}")
    lines.append(
        "@keyframes il-pulse{0%,100%{opacity:1}50%{opacity:.55}}"
    )
    # base entrance for all direct children (overridden below per child)
    lines.append(
        "svg.il-anim > *{opacity:0;animation:il-pop .5s .05s ease both}"
    )
    # staggered entrances, children 2..60 (child 1 often a background rect / title / defs)
    for n in range(2, 61):
        delay = min((n - 2) * 0.07, 2.0)
        lines.append(
            f"svg.il-anim > :nth-child({n}){{animation:il-pop .5s {delay:.2f}s ease both}}"
        )
    # flowing dashes on any dashed line/path
    lines.append(
        "svg.il-anim line[stroke-dasharray],svg.il-anim path[stroke-dasharray]{animation:il-dash 1.2s linear infinite}"
    )
    # reduced motion
    lines.append(
        "@media (prefers-reduced-motion:reduce){svg.il-anim > *{animation:none!important;opacity:1!important}"
        "svg.il-anim line[stroke-dasharray],svg.il-anim path[stroke-dasharray]{animation:none!important}}"
    )
    lines.append("</style>")
    return "\n".join(lines)


SVG_TAG = re.compile(r"<svg\b[^>]*>", re.DOTALL)


def process(path):
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    if "il-anim" in src or "@keyframes il-pop" in src:
        return "skipped"

    m = SVG_TAG.search(src)
    if not m:
        return "error-no-svg-tag"

    tag = m.group(0)

    def add_class(tag):
        if 'class="' in tag or "class='" in tag:
            tag = re.sub(
                r'class="([^"]*)"',
                lambda mm: 'class="' + mm.group(1).rstrip() + ' il-anim"',
                tag,
                count=1,
            )
            tag = re.sub(
                r"class='([^']*)'",
                lambda mm: "class='" + mm.group(1).rstrip() + " il-anim'",
                tag,
                count=1,
            )
            return tag
        return tag.replace("<svg", '<svg class="il-anim"', 1)

    new_tag = add_class(tag)
    if "il-anim" not in new_tag:
        return "error-class-failed"

    new_src = src[: m.start()] + new_tag + "\n" + style_block() + src[m.end():]

    bak = path + ".w7bak"
    try:
        with open(bak, "x", encoding="utf-8") as bf:
            bf.write(src)
    except FileExistsError:
        pass

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_src)

    # XML validation
    try:
        ET.fromstring(new_src)
    except ET.ParseError as e:
        shutil.copy(bak, path)
        return f"error-xml:{e}"
    return "animated"


def main():
    with open(LIST, encoding="utf-8") as f:
        files = [ln.strip() for ln in f if ln.strip()]
    counts = {"animated": 0, "skipped": 0, "errors": []}
    for p in files:
        try:
            r = process(p)
        except Exception as e:  # noqa: BLE001
            r = f"error-exception:{e}"
        if r == "animated":
            counts["animated"] += 1
        elif r == "skipped":
            counts["skipped"] += 1
        else:
            counts["errors"].append(f"{p} :: {r}")
    print(f"total={len(files)} animated={counts['animated']} skipped={counts['skipped']} errors={len(counts['errors'])}")
    for e in counts["errors"]:
        print(e)


if __name__ == "__main__":
    main()
