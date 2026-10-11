#!/usr/bin/env python3
"""Internal link integrity: check local href/src links on key pages resolve in docs tree."""
import os, re, json
from html.parser import HTMLParser

DOCS = os.path.expanduser("~/workspace/apex-audit/docs")
PAGES = ["index.html","university/index.html","topics/index.html","noah/index.html",
         "jobs/index.html","about/index.html","prep/drills/index.html",
         "bootcamp-catalog/index.html","university/course.html"]

class L(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]
    def handle_starttag(s,t,a):
        d=dict(a)
        if t=="a" and d.get("href"): s.links.append(("a",d["href"],s.getpos()[0]))
        if t=="form" and d.get("action"): s.links.append(("form",d["action"],s.getpos()[0]))

def exists_local(url, page):
    u = url.strip().split("#")[0].split("?")[0]
    if not u or u.startswith(("http://","https://","//","mailto:","tel:","data:","javascript:")):
        return None  # external, skip
    if u.startswith("/"):
        cand = [os.path.join(DOCS,u.lstrip("/"))]
    else:
        cand = [os.path.normpath(os.path.join(os.path.dirname(os.path.join(DOCS,page)),u))]
    for c in cand:
        if os.path.isdir(c):
            # dir needs index.html
            if os.path.exists(os.path.join(c,"index.html")): return True
            return False
        if os.path.exists(c): return True
    return False

out={}
for page in PAGES:
    html=open(os.path.join(DOCS,page),encoding="utf-8",errors="replace").read()
    p=L(); p.feed(html)
    broken=[]
    for tag,url,line in p.links:
        r=exists_local(url,page)
        if r is False:
            broken.append({"tag":tag,"url":url,"line":line})
    out[page]={"total_links":len(p.links),"broken_local":broken}
print(json.dumps(out,indent=1))
