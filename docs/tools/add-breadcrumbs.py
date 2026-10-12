#!/usr/bin/env python3
"""Add breadcrumbs to pages missing them. Re-runnable / idempotent.

Derives breadcrumb trail from URL path:
  /topics/cybersecurity/ -> Home / Topics / Cybersecurity
  /paths/devsecops-mastery/ -> Home / Paths / DevSecOps Mastery
  /university/ -> Home / Courses

Skips pages that already have .il-breadcrumbs or data-il-breadcrumbs.
Inserts after </nav> of the pillnav (or after <body> as fallback).

Usage: python3 tools/add-breadcrumbs.py
"""
import os
import re
import html as htmlmod

DOCS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# url segment -> display name
NAMES = {
    "topics": "Topics",
    "university": "Courses",
    "paths": "Paths",
    "prep": "Practice",
    "drills": "Drills",
    "labs": "Labs",
    "noah": "Noah AI",
    "jobs": "Jobs",
    "about": "About",
    "enroll": "Enroll",
    "account": "Account",
    "pdf-library": "Visual Guides",
    "bootcamp-catalog": "Bootcamps",
    "evidence": "Evidence",
    "subject-map": "Subject Map",
    "coach": "Coach",
    "play": "Play",
    "adapt": "Adapt",
    "library": "Library",
    "learn": "Learn",
    "academy": "Academy",
    "cybersecurity": "Cybersecurity",
    "system-design": "System Design",
    "networking": "Networking",
    "cloud-devops": "Cloud & DevOps",
    "ai-ml": "AI & ML",
    "data-eng": "Data Engineering",
    "programming": "Programming",
    "databases": "Databases",
    "linux-systems": "Linux & Systems",
    "math": "Mathematics (Turing)",
    "web-dev": "Web Development",
    "blockchain": "Blockchain",
    "crypto": "Cryptocurrency",
    "cybernetics": "Cybernetics",
    "esoteric": "Esoteric",
    "om": "Om",
}


def pretty(seg):
    if seg in NAMES:
        return NAMES[seg]
    s = seg.replace("-", " ").replace("_", " ")
    return s.title()


def breadcrumb_for(url, title):
    # url like /topics/cybersecurity/
    segs = [s for s in url.strip("/").split("/") if s]
    if not segs:
        return None  # homepage needs none
    items = ['<li><a href="/">Home</a></li>']
    accum = ""
    for i, seg in enumerate(segs):
        accum += "/" + seg
        last = (i == len(segs) - 1)
        if last:
            label = pretty(seg)
            # prefer page <title> for the leaf when it's cleaner
            if title and len(title) < 60 and seg not in NAMES:
                label = title
            items.append(f'<li aria-current="page">{htmlmod.escape(label)}</li>')
        else:
            items.append(f'<li><a href="{accum}/">{htmlmod.escape(pretty(seg))}</a></li>')
    return (
        '<nav class="il-breadcrumbs" aria-label="Breadcrumb" data-il-breadcrumbs>'
        "<ol>" + "".join(items) + "</ol></nav>"
    )


def main():
    added = 0
    skipped = 0
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if d not in ("assets", "data", "tools")
                   and not d.startswith(".") and d != "_deleted-backup"]
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(root, f)
            h = open(p, encoding="utf-8", errors="ignore").read()
            if "il-breadcrumbs" in h or 'http-equiv="refresh"' in h:
                skipped += 1
                continue
            rel = os.path.relpath(p, DOCS)
            if rel == "index.html":
                url = "/"
            elif rel.endswith("/index.html"):
                url = "/" + rel[:-11] + "/"
            else:
                url = "/" + rel
            url = re.sub(r"/{2,}", "/", url)
            m = re.search(r"<title>(.*?)</title>", h, re.S | re.I)
            title = ""
            if m:
                title = re.sub(r"\s+", " ", htmlmod.unescape(m.group(1)).strip())
                title = re.sub(r"\s*[·|–—-]\s*Interstitium Labs.*$", "", title).strip()
            crumb = breadcrumb_for(url, title)
            if not crumb:
                skipped += 1
                continue
            # insert after pillnav </nav>, else after <body>
            if '<nav class="il-pillnav"' in h:
                h = re.sub(r"(<nav class=\"il-pillnav\".*?</nav>)",
                           lambda m: m.group(1) + "\n" + crumb, h,
                           count=1, flags=re.S)
            elif "<body" in h:
                h = re.sub(r"(<body[^>]*>)",
                           lambda m: m.group(1) + "\n" + crumb, h,
                           count=1)
            else:
                skipped += 1
                continue
            open(p, "w", encoding="utf-8").write(h)
            added += 1
    print(f"breadcrumbs added: {added}, skipped: {skipped}")


if __name__ == "__main__":
    main()
