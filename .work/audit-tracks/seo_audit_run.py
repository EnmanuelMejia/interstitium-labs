#!/usr/bin/env python3
"""SEO audit: fetch pages, extract tags, check og:image 200s. No changes made.
Writes incremental results to RESULTS_PATH so a crash doesn't lose data."""
import json, re, sys, urllib.request, urllib.parse, urllib.error, time, os

NORMAL_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
CRAWLER_UA = "LinkedInBot/1.0"
RESULTS_PATH = sys.argv[2] if len(sys.argv) > 2 else "seo_results.json"

from html.parser import HTMLParser

class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.in_title = False
        self.title_parts = []
        self.title_count = 0
        self.metas = []
        self.links = []
        self.done = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "head":
            self.in_head = True
        if tag == "title" and self.in_head:
            self.in_title = True
            self.title_count += 1
        if tag == "meta":
            self.metas.append({k.lower(): v for k, v in attrs})
        if tag == "link":
            self.links.append({k.lower(): v for k, v in attrs})
        if tag == "body":
            self.done = True

    def handle_endtag(self, tag):
        if tag.lower() == "head":
            self.in_head = False
            self.done = True
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)

    def get_title(self):
        t = "".join(self.title_parts).strip()
        return t if t else None

def fetch(url, ua, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), r.url
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except Exception:
            body = b""
        return e.code, body, url
    except Exception as e:
        return 0, b"", url

def head_status(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": NORMAL_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.url
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception:
        return 0, url

def abs_url(base, ref):
    return urllib.parse.urljoin(base, ref)

def audit_page(url, crawl_ua_too=False):
    results = {}
    uas = [("normal", NORMAL_UA)] + ([("crawler", CRAWLER_UA)] if crawl_ua_too else [])
    for label, ua in uas:
        status, body, final_url = fetch(url, ua)
        text = body.decode("utf-8", errors="replace") if body else ""
        p = HeadParser()
        try:
            p.feed(text)
        except Exception:
            pass
        title = p.get_title()
        desc = None
        robots_meta = None
        og = {}
        twitter = {}
        canonical = None
        canon_count = 0
        for m in p.metas:
            name = m.get("name", "").lower()
            prop = m.get("property", "").lower()
            if name == "description" and desc is None:
                desc = m.get("content", "")
            if name == "robots" and robots_meta is None:
                robots_meta = m.get("content", "")
            if prop.startswith("og:"):
                og.setdefault(prop, m.get("content", ""))
            if name.startswith("twitter:"):
                twitter.setdefault(name, m.get("content", ""))
        for l in p.links:
            if l.get("rel", "").lower() == "canonical":
                canon_count += 1
                if canonical is None:
                    canonical = l.get("href", "")
        canonical_abs = abs_url(final_url, canonical) if canonical else None
        ogimg_url = og.get("og:image")
        ogimg_abs = abs_url(final_url, ogimg_url) if ogimg_url else None
        ogimg_status = None
        if ogimg_abs:
            ogimg_status, _ = head_status(ogimg_abs)
        results[label] = {
            "http": status,
            "final_url": final_url,
            "title": title,
            "title_count": p.title_count,
            "description": desc,
            "description_len": len(desc) if desc else 0,
            "og": og,
            "og_image_abs": ogimg_abs,
            "og_image_status": ogimg_status,
            "canonical": canonical,
            "canonical_abs": canonical_abs,
            "canonical_count": canon_count,
            "twitter": twitter,
            "robots_meta": robots_meta,
        }
    return results

def save(data):
    tmp = RESULTS_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, RESULTS_PATH)

def main():
    pages = json.load(open(sys.argv[1]))
    out = {}
    if os.path.exists(RESULTS_PATH):
        try:
            out = json.load(open(RESULTS_PATH))
        except Exception:
            out = {}
    for p in pages:
        url = p["url"]
        if url in out and "error" not in out[url]:
            print("skip (have):", url, flush=True)
            continue
        print("fetch:", url, flush=True)
        try:
            out[url] = audit_page(url, crawl_ua_too=p.get("crawler", False))
        except Exception as e:
            out[url] = {"error": str(e)}
        save(out)
        time.sleep(0.5)
    print("DONE, pages:", len(out))

if __name__ == "__main__":
    main()
