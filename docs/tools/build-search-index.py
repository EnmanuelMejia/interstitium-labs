#!/usr/bin/env python3
"""Build client-side search index for interstitiumlabs.dev.

Walks all HTML pages under docs/, extracts title/heading/description,
classifies each page (course/path/guide/page + theme), and writes
assets/search-index.json. Re-runnable: just run again after content changes.

Usage: python3 tools/build-search-index.py
"""
import html as htmlmod
import json
import os
import re
import sys

DOCS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(DOCS, "assets", "search-index.json")

SKIP_DIRS = {"assets", "data", "tools", "_deleted-backup"}
SKIP_FILES = {"404.html"}

# url prefix -> theme slug
THEME_PREFIXES = {
    "/topics/cybersecurity/": "cybersecurity",
    "/topics/system-design/": "system-design",
    "/topics/networking/": "networking",
    "/topics/cloud-devops/": "cloud-devops",
    "/topics/ai-ml/": "ai-ml",
    "/topics/data-eng/": "data-eng",
    "/topics/programming/": "programming",
    "/topics/databases/": "databases",
    "/topics/linux-systems/": "linux-systems",
    "/topics/math/": "math",
    "/topics/web-dev/": "web-dev",
    "/topics/blockchain/": "blockchain",
    "/topics/crypto/": "crypto",
    "/topics/cybernetics/": "cybernetics",
    "/topics/esoteric/": "esoteric",
    "/topics/om/": "om",
}

THEME_NAMES = {
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


def classify(url, title, html):
    """Return (type, theme)."""
    theme = ""
    for prefix, slug in THEME_PREFIXES.items():
        if url.startswith(prefix):
            theme = slug
            break
    if url.startswith("/university/"):
        # course pages carry ?course= or /academy?id=
        return ("course", theme)
    if url.startswith("/paths/"):
        return ("path", theme)
    if url.startswith("/pdf-library/"):
        return ("guide", theme)
    if url.startswith("/topics/"):
        return ("theme", theme)
    if url.startswith("/prep/") or url.startswith("/labs/"):
        return ("practice", theme)
    if url.startswith("/noah/"):
        return ("ai", theme)
    if url.startswith("/jobs/"):
        return ("job", theme)
    return ("page", theme)


def extract(path):
    try:
        h = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return None
    # skip redirect stubs
    if 'http-equiv="refresh"' in h:
        return None
    m = re.search(r"<title>(.*?)</title>", h, re.S | re.I)
    title = (m.group(1).strip() if m else "")
    title = re.sub(r"\s+", " ", htmlmod.unescape(title))
    # strip site suffix
    title = re.sub(r"\s*[·|–—-]\s*Interstitium Labs.*$", "", title).strip()
    if not title:
        return None
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', h, re.I)
    desc = (m.group(1).strip() if m else "")
    desc = re.sub(r"\s+", " ", htmlmod.unescape(desc))[:200]
    if not desc:
        m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S | re.I)
        if m:
            desc = re.sub(r"<[^>]+>", "", m.group(1))
            desc = re.sub(r"\s+", " ", htmlmod.unescape(desc)).strip()[:200]
    # keywords: h2/h3 headings for better matching
    heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", h, re.S | re.I)[:8]
    keywords = []
    for hh in heads:
        t = re.sub(r"<[^>]+>", "", hh)
        t = re.sub(r"\s+", " ", htmlmod.unescape(t)).strip()
        if t and len(t) < 80:
            keywords.append(t)
    rel = os.path.relpath(path, DOCS)
    if rel == "index.html":
        url = "/"
    elif rel.endswith("/index.html"):
        url = "/" + rel[:-11] + "/"
    else:
        url = "/" + rel
    url = re.sub(r"/{2,}", "/", url)
    ptype, theme = classify(url, title, h)
    return {
        "t": title[:90],
        "u": url,
        "d": desc,
        "k": " ".join(keywords)[:200],
        "type": ptype,
        "theme": theme,
        "tn": THEME_NAMES.get(theme, ""),
    }


def main():
    entries = []
    seen = set()
    for root, dirs, files in os.walk(DOCS):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for f in files:
            if not f.endswith(".html") or f in SKIP_FILES:
                continue
            e = extract(os.path.join(root, f))
            if e and e["u"] not in seen:
                seen.add(e["u"])
                entries.append(e)
    # homepage first, then themes, then the rest
    order = {"page": 0}
    entries.sort(key=lambda e: (0 if e["u"] == "/" else 1, e["t"]))
    payload = {"v": 1, "count": len(entries), "items": entries}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    size = os.path.getsize(OUT)
    print(f"search-index.json: {len(entries)} entries, {size//1024}KB")


if __name__ == "__main__":
    main()
