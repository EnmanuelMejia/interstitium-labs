#!/usr/bin/env python3
"""Layout/QA asset audit: resolve every img/video/poster/icon reference in key pages against the docs tree."""
import os, re, json
from html.parser import HTMLParser

DOCS = os.path.expanduser("~/workspace/apex-audit/docs")

PAGES = [
    "index.html",
    "university/index.html",
    "topics/index.html",
    "noah/index.html",
    "jobs/index.html",
    "about/index.html",
    "prep/drills/index.html",
    "bootcamp-catalog/index.html",
]

# course page: find the shell html for /university/course
COURSE_SHELLS = []
for root, dirs, files in os.walk(os.path.join(DOCS, "university")):
    for f in files:
        if f.endswith(".html") and "course" in f.lower():
            COURSE_SHELLS.append(os.path.relpath(os.path.join(root, f), DOCS))
print("Course shells found:", COURSE_SHELLS)
for c in COURSE_SHELLS:
    PAGES.append(c)

class RefParser(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.refs = []          # (tag, attr, url, line)
        self.inline_styles = []
        self.tag_stack = []
        self.unclosed = []
        self.voids = {"img","br","hr","input","meta","link","source","track","wbr","col","base","embed","area"}
        self.img_no_alt = 0
        self.img_alt_empty = 0
        self.img_with_alt = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        pos = self.getpos()
        if tag == "img":
            src = a.get("src","")
            self.refs.append(("img","src",src,pos[0]))
            if "alt" not in a: self.img_no_alt += 1
            elif a["alt"].strip()=="": self.img_alt_empty += 1
            else: self.img_with_alt += 1
        if tag in ("video","audio"):
            if a.get("src"): self.refs.append((tag,"src",a["src"],pos[0]))
            if a.get("poster"): self.refs.append((tag,"poster",a["poster"],pos[0]))
        if tag == "source" and a.get("src"):
            self.refs.append(("source","src",a["src"],pos[0]))
        if tag == "link" and a.get("rel")==["stylesheet"]:
            self.refs.append(("link","href",a.get("href",""),pos[0]))
        elif tag == "link" and a.get("href","").endswith((".png",".svg",".ico",".webmanifest")):
            self.refs.append(("link","href",a.get("href",""),pos[0]))
        if "style" in a:
            self.inline_styles.append((tag, a["style"], pos[0]))
        if tag not in self.voids:
            self.tag_stack.append((tag, pos[0]))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in self.tag_stack and self.tag_stack[-1][0]==tag:
            self.tag_stack.pop()
    def handle_endtag(self, tag):
        if tag in self.voids: return
        # find matching open tag from top of stack
        for i in range(len(self.tag_stack)-1, -1, -1):
            if self.tag_stack[i][0]==tag:
                # everything above is unclosed
                for t,l in self.tag_stack[i+1:]:
                    self.unclosed.append((t,l))
                del self.tag_stack[i:]
                return
        # stray close tag

PLACEHOLDER_RE = re.compile(r"(via\.placeholder\.com|placehold\.co|placeholder\.com|picsum\.photos|dummyimage\.com|loremflickr|unsplash\.source)", re.I)

def resolve(url, page):
    url = url.strip().split("#")[0].split("?")[0]
    if not url or url.startswith(("data:","http://","https://","//","mailto:","tel:")):
        return ("external-or-empty", url)
    page_dir = os.path.dirname(os.path.join(DOCS, page))
    if url.startswith("/"):
        full = os.path.join(DOCS, url.lstrip("/"))
    else:
        full = os.path.normpath(os.path.join(page_dir, url))
    return ("exists" if os.path.exists(full) else "MISSING", url)

results = {}
for page in PAGES:
    path = os.path.join(DOCS, page)
    if not os.path.exists(path):
        results[page] = {"error":"file not found"}; continue
    html = open(path, encoding="utf-8", errors="replace").read()
    p = RefParser(page)
    p.feed(html)
    missing, external, placeholders = [], [], []
    for tag, attr, url, line in p.refs:
        if not url:
            missing.append({"tag":tag,"attr":attr,"line":line,"issue":"EMPTY URL"})
            continue
        if PLACEHOLDER_RE.search(url):
            placeholders.append({"tag":tag,"attr":attr,"url":url,"line":line}); continue
        status, u = resolve(url, page)
        if status=="MISSING":
            missing.append({"tag":tag,"attr":attr,"url":u,"line":line})
    # inline CSS red flags
    inline_flags = []
    for tag, style, line in p.inline_styles:
        for m in re.finditer(r"width\s*:\s*(\d{3,})px", style):
            if int(m.group(1)) >= 500:
                inline_flags.append({"line":line,"tag":tag,"style":style.strip()[:120]})
    # unclosed tail: only report if stack non-empty at end and page large
    results[page] = {
        "missing_assets": missing,
        "placeholder_images": placeholders,
        "inline_fixed_widths": inline_flags,
        "unclosed_tags_at_eof": [{"tag":t,"opened_line":l} for t,l in p.tag_stack[:10]],
        "img_alt": {"with_alt":p.img_with_alt,"empty_alt":p.img_alt_empty,"no_alt":p.img_no_alt},
        "ref_count": len(p.refs),
        "file_lines": len(html.splitlines()),
        "has_doctype": html.lstrip().lower().startswith("<!doctype"),
        "has_viewport": 'name="viewport"' in html,
    }

print(json.dumps(results, indent=1))
