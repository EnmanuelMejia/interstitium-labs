#!/usr/bin/env python3
"""Regenerate docs/sitemap.xml and docs/assets/search-index.json from the docs/ tree.

Ownership: Worker C (site-fix op, 2026-10-04). Re-run after adding/removing public pages:

    python3 scripts/build-site-index.py

Rules:
  * Directory index pages (docs/<dir>/index.html) become https://interstitiumlabs.dev/<dir>/
  * Standalone *.html files (not index.html) become https://interstitiumlabs.dev/<path>/<file>.html
  * Public pages only. Exclusions:
      - robots.txt Disallow paths (/brand/ /ops/ /admin/ /_imports/ /analytics/ /measure/ /academy/ /desk/)
      - pages carrying <meta ... noindex ...>
      - 404.html, and non-html files
      - anything that looks like a draft (path segments starting with '_' or '.',
        filenames containing 'draft')
  * Dead URLs (pages removed from the repo) drop out automatically on regeneration.
"""

import html as htmlmod
import os
import re
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
BASE_URL = "https://interstitiumlabs.dev"

# First path segment(s) excluded from sitemap + search. Mirrors robots.txt Disallow.
EXCLUDED_PREFIXES = (
    "brand/", "ops/", "admin/", "_imports/", "analytics/", "measure/",
    "academy/", "desk/",
)

SITEMAP_OUT = os.path.join(DOCS, "sitemap.xml")
SEARCH_INDEX_OUT = os.path.join(DOCS, "assets", "search-index.json")

NOINDEX_RE = re.compile(
    r'<meta[^>]+name\s*=\s*["\']robots["\'][^>]*content\s*=\s*["\']([^"\']*)["\']',
    re.I)
NOINDEX_RE2 = re.compile(
    r'<meta[^>]+content\s*=\s*["\']([^"\']*)["\'][^>]*name\s*=\s*["\']robots["\']',
    re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
HEAD_RE = re.compile(r"<h[123][^>]*>(.*?)</h[123]>", re.I | re.S)
STRIP_BLOCK_RE = re.compile(
    r"<(script|style|nav|header|footer|noscript)[^>]*>.*?</\1>",
    re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def is_excluded(rel_path: str) -> bool:
    """True if this docs-relative path is non-public."""
    p = rel_path.replace(os.sep, "/")
    if p.startswith(EXCLUDED_PREFIXES):
        return True
    segs = p.split("/")
    if any(s.startswith(("_", ".")) for s in segs):
        return True  # drafts, partials, dotfiles
    if "draft" in p.lower():
        return True
    base = os.path.basename(p)
    if base in ("404.html",):
        return True
    return False


def read_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def is_noindex(html: str) -> bool:
    for m in list(NOINDEX_RE.finditer(html)) + list(NOINDEX_RE2.finditer(html)):
        if "noindex" in m.group(1).lower():
            return True
    return False


def clean_text(raw: str) -> str:
    txt = STRIP_BLOCK_RE.sub(" ", raw)
    txt = TAG_RE.sub(" ", txt)
    txt = htmlmod.unescape(txt)
    txt = WS_RE.sub(" ", txt).strip()
    return txt


def extract(html: str):
    m = TITLE_RE.search(html)
    title = WS_RE.sub(" ", htmlmod.unescape(TAG_RE.sub("", m.group(1)))).strip() if m else ""
    headings = [WS_RE.sub(" ", htmlmod.unescape(TAG_RE.sub("", h))).strip()
                for h in HEAD_RE.findall(html)]
    headings = [h for h in headings if h][:12]
    body = clean_text(html)
    # keep body useful: drop the title dup at the start
    snippet = body[:600]
    return title, headings, snippet


def collect_pages():
    """Return list of (rel_url, abs_path) for public pages."""
    pages = []
    for root, dirs, names in os.walk(DOCS):
        # prune excluded dirs early
        dirs[:] = [d for d in dirs
                   if not d.startswith(("_", ".")) and "draft" not in d.lower()]
        for name in names:
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, name), DOCS).replace(os.sep, "/")
            if is_excluded(rel):
                continue
            if name == "index.html":
                url = "/" + os.path.dirname(rel).replace(os.sep, "/")
                url = url if url == "/" else url + "/"
                if url == "//":
                    url = "/"
                if url != "/" and not url.startswith("/"):
                    url = "/" + url
                url = "/" if url.strip("/") == "" else url
            else:
                url = "/" + rel
            pages.append((url, os.path.join(root, name)))
    # keep only indexable pages
    public = []
    skipped_noindex = 0
    for url, path in pages:
        if is_noindex(read_file(path)):
            skipped_noindex += 1
            continue
        public.append((url, path))
    public.sort(key=lambda p: p[0])
    return public, skipped_noindex


def sitemap_xml(pages):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, path in pages:
        depth = url.strip("/").count("/") + (0 if url == "/" else 1)
        priority = {0: "1.0", 1: "0.9", 2: "0.8"}.get(depth, "0.7")
        if url == "/":
            priority = "1.0"
        changefreq = "weekly" if depth <= 1 else "monthly"
        if url.startswith("/jobs"):
            changefreq = "daily"
        lastmod = datetime.fromtimestamp(
            os.path.getmtime(path), tz=timezone.utc).strftime("%Y-%m-%d")
        loc = (BASE_URL + url).replace("&", "&amp;")
        lines.append(
            f'  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod>'
            f'<changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    pages, skipped_noindex = collect_pages()
    xml = sitemap_xml(pages)
    # validate
    from xml.dom.minidom import parseString
    parseString(xml)  # raises on malformed XML

    index = []
    for url, path in pages:
        title, headings, snippet = extract(read_file(path))
        if not title and not snippet:
            continue
        index.append({"u": url, "t": title, "h": headings, "s": snippet[:500]})

    with open(SITEMAP_OUT, "w", encoding="utf-8") as f:
        f.write(xml)
    import json
    with open(SEARCH_INDEX_OUT, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")

    # sanity: every sitemap URL must resolve to a real file
    for url, path in pages:
        assert os.path.isfile(path), f"missing file for {url}"

    print(f"pages in sitemap      : {len(pages)}")
    print(f"pages in search index : {len(index)}")
    print(f"skipped (noindex)     : {skipped_noindex}")
    print(f"wrote {SITEMAP_OUT}")
    print(f"wrote {SEARCH_INDEX_OUT} "
          f"({os.path.getsize(SEARCH_INDEX_OUT) / 1024:.0f} KB)")
    print("XML validation: OK")


if __name__ == "__main__":
    sys.exit(main())
